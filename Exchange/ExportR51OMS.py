# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
u"""Экспорт реестра счета ОМС. Мурманск"""

import os.path

from PyQt4 import QtGui
from PyQt4.QtCore import QDate

from library.dbfpy.dbf import Dbf
from library.Utils import (forceBool, forceInt, toVariant, forceString,
                           forceRef, forceDouble, forceDate as _forceDate,
                           nameCase, pyDate, formatSNILS, formatSex,
                           firstMonthDay)

from Accounting.Tariff import CTariff
from Events.Action import CAction
from Events.ActionServiceType import CActionServiceType
from Orgs.Utils import getPersonShortName

from Exchange.Export import (CAbstractExportWizard, CAbstractExportPage1,
                             CAbstractExportPage2, CExportHelperMixin)
from Exchange.Ui_ExportR51OMSPage1 import Ui_ExportPage1

def forceDate(val):
    u'''Считаем даты до 1900 неправильными, т.к. это приводит
        к падению питона 2.6 под win32'''
    result = _forceDate(val)
    if result.isValid() and result.year() < 1900:
        return None
    return result

# ******************************************************************************

def exportR51OMS(widget, accountId, accountItemIdList, _=None):
    u"""Создает диалог экспорта реестра счета"""

    wizard = CExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.exec_()


def createServTmtDbf(tmpDir):
    u"""Информация об услугах с применением телемедицинских технологий"""
    dbfName = os.path.join(tmpDir, 'SERV_TMT.DBF')
    dbf = Dbf(dbfName, new=True, encoding='cp866')
    dbf.addField(
        ('CARD', 'C', 10), #Номер статталона
        ('TMT_MO', 'C', 6),
        ('PROFIL', 'N', 3),
        ('PRVS', 'N', 4),
        ('SERV_DATE', 'D'),
        ('FOR_POM', 'C', 1),
    )
    return dbf

def createDirectDbf(tmpDir):
    """ Создает структуру dbf для DIRECT.DBF """

    dbfName = os.path.join(tmpDir, 'DIRECT.DBF')
    dbf = Dbf(dbfName, new=True, encoding='cp866')
    dbf.addField(
        ('CARD', 'C', 10), #Номер статталона
        ('NAZR', 'N', 2), #Назначения
        ('NAZ_SP', 'N', 4), #Специальность врача
        ('NAZ_V', 'N', 1), #Вид обследования
        ('NAZ_PMP', 'N', 3), #Профиль медицинской помощи
        ('NAZ_PK', 'C', 3), #Профиль койки
    )
    return dbf


def createDs2nDbf(tmpDir):
    """ Создает структуру dbf для DS2_N.DBF """

    dbfName = os.path.join(tmpDir, 'DS2_N.DBF')
    dbf = Dbf(dbfName, new=True, encoding='cp866')
    dbf.addField(
        ('CARD', 'C', 10), #Номер статталона
        ('DS2', 'C', 6), #Код диагноза сопутствующего заболевания
        ('DS2_PR', 'N', 1), #Установлен впервые (сопутствующий)
    )
    return dbf


def createNaprDbf(tmpDir, exportType2019=False):
    """ Создает структуру dbf для NAPR.DBF """

    dbfName = os.path.join(tmpDir, 'NAPR.DBF')
    dbf = Dbf(dbfName, new=True, encoding='cp866')
    if exportType2019:
        dbf.addField(
            ('CARD', 'C', 10), # Номер статталона
            ('NAPR_DATE', 'D', 8),
            ('NAPR_MO', 'C', 3),
            ('NAPR_V', 'N', 2),
            ('MET_ISSL', 'N', 2),
            ('NAPR_USL', 'C', 15)
        )
    else:
        dbf.addField(
            ('CARD', 'C', 10), # Номер статталона
            ('IDSERV', 'C', 36),
            ('NAPR_DATE', 'D'),
            ('NAPR_V', 'N', 1),
            ('MET_ISSL', 'N', 1),
            ('NAPR_USL', 'C', 15)
        )
    return dbf


mapAcionStatusToNpl = {6:1, 3:2, 2:4}

def exportDs2n(dbf, record, params):
    u"""Выгрузка информации в DS2_N.DBF из record и params."""

    accMKB = forceString(record.value('accMKB'))

    if accMKB:
        eventId = params['eventId']
        exportedMKBs = params.setdefault(
            'ds2nCache', {}).setdefault(eventId, set())

        if accMKB not in exportedMKBs:
            row = dbf.newRecord()
            #Номер истории болезни
            row['CARD'] = params['eventId']
            row['DS2'] = accMKB
            row['DS2_PR'] = forceInt(record.value('DS2_PR'))
            row.store()
            params['ds2nCache'][eventId].add(accMKB)


def getIdsp(medicalAidUnitCode, isAttached, isHomeVisit):
    u"""Заполнение IDSP - Заполняем из регионального кода единицы учета
    (Account_Item.unit_id-->rbMedicalAidUnit.regionalCode)
    При этом, если IDSP = 26, проверяем, прикреплен ли пациент на момент
    выполнения События (Event.execDate) к организации, указанной в умолчаниях.
    - Если прикреплен, не меняем значение
    - Если не прикреплен и место визита в названии не содержит "на дому"
        (т.е. NOT LIKE "%на дому%") - меняем IDSP на 29.
    - Если не прикреплен и место визита в названии содержит "на дому"
        (т.е. LIKE "%на дому%") - меняем IDSP на 23.
    Если IDSP = 27, проверяем, прикреплен ли пациент на момент выполнения
        События (Event.execDate) к организации, указанной в умолчаниях.
    - Если прикреплен, не меняем значение
    - Если не прикреплен - меняем IDSP на 30.
    Если IDSP = 25, проверяем, прикреплен ли пациент на момент выполнения
        События (Event.execDate) к организации, указанной в умолчаниях.
    - Если прикреплен, не меняем значение
    - Если не прикреплен - меняем IDSP на 28.
    Если IDSP = 38, проверяем, прикреплен ли пациент на момент выполнения
        События (Event.execDate) к организации, указанной в умолчаниях.
    - Если прикреплен, не меняем значение
    - Если не прикреплен - меняем IDSP на 41. """

    result = medicalAidUnitCode

    if not isAttached:
        if medicalAidUnitCode == 26:
            result = 23 if isHomeVisit else 29
        elif medicalAidUnitCode == 27:
            result = 30
        elif medicalAidUnitCode == 25:
            result = 28
        elif medicalAidUnitCode == 38:
            result = 41

    return result

mapDiagRslt = {
    (1, u'Эпителиальный'): 1,
    (1, u'Неэпителиальный'): 2,
    (2, u'Светлоклеточный'): 3,
    (2, u'Несветлоклеточный'): 4,
    (3, u'Низкодифференцированная'): 5,
    (3, u'Умереннодифференцированная'): 6,
    (3, u'Высокодифференцированная'): 7,
    (3, u'Не определена'): 8,
    (4, u'Мелкоклеточный'): 9,
    (4, u'Немелкоклеточный'): 10,
    (5, u'Почечноклеточный'): 11,
    (5, u'Непочечноклеточный'): 12,
    (6, u'Папиллярный'): 13,
    (6, u'Фолликулярный'): 14,
    (6, u'Гюртклеточный'): 15,
    (6, u'Медуллярный'): 16,
    (6, u'Анапластический'): 17,
    (7, u'Базальноклеточный'): 18,
    (7, u'Не базальноклеточный'): 19,
    (8, u'Плоскоклеточный'): 20,
    (8, u'Не плоскоклеточный'): 21,
    (8, u'Эндометриоидные'): 22,
    (9, u'Не эндометриоидные'): 23,
    (10, u'Аденокарцинома'): 24,
    (10, u'Не аденокарцинома'): 25,

    (1, u'Гиперэкспрессия белка HER2'): 1,
    (1, u'Отсутствие гиперэкспрессии белка HER2'): 2,
    (1, u'Не определён Исследование не проводилось'): 3,
    (2, u'Наличие мутаций в гене BRAF'): 4,
    (2, u'Отсутствие мутаций в гене BRAF'): 5,
    (3, u'Наличие мутаций в гене c-Kit'): 6,
    (3, u'Отсутствие мутаций в гене c-Kit'): 7,
    (3, u'Не определён Исследование не проводилось'): 8,
    (4, u'Наличие мутаций в гене RAS'): 9,
    (4, u'Отсутствие мутаций в гене RAS'): 10,
    (5, u'Наличие мутаций в гене EGFR'): 11,
    (5, u'Отсутствие мутаций в гене EGFR'): 12,
    (6, u'Наличие транслокации в генах ALK или ROS1'): 13,
    (6, u'Отсутствие транслокации в генах ALK и ROS1'): 14,
    (7, u'Повышенная экспрессия белка PD-L1'): 15,
    (7, u'Отсутствие повышенной экспрессии белка PD-L1'): 16,
    (8, u'Наличие рецепторов к эстрогенам'): 17,
    (8, u'Отсутствие рецепторов к эстрогенам'): 18,
    (9, u'Наличие рецепторов к прогестерону'): 19,
    (9, u'Отсутствие рецепторов к прогестерону'): 20,
    (10, u'Отсутствие рецепторов к прогестерону'): 21,
    (10, u'Низкий Низкий индекс пролиферативной активности '
     u'экспрессии Ki-67') : 22,
    (11, u'Гиперэкспрессия белка HER2'): 23,
    (11, u'Отсутствие гиперэкспрессии белка HER2'): 24,
    (12, u'Наличие мутаций в генах BRCA'): 25,
    (12, u'Отсутствие мутаций в генах BRCA'): 26,
}

mapMetIssl = {
    u'на лабораторную диагностику': 1,
    u'на инструментальную диагностику': 2,
    u'на лучевую диагностику (кроме дорогостоящих)': 3,
    u'на ангиографию': 4,
}

def getOnkologyInfo(db, idList, exportType2019=False):
    if exportType2019:
        joinMKB = u'''    LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
        LEFT JOIN Diagnosis AS AccDiagnosis ON AccDiagnosis.id = (
                          SELECT MAX(ds.id)
                            FROM Diagnosis ds
                            INNER JOIN Diagnostic dc ON (ds.id = dc.diagnosis_id AND ds.deleted = 0 AND dc.deleted = 0)
                            WHERE dc.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code IN ('9', '10', '11'))
                            AND dc.event_id = Account_Item.event_id
                    )'''
        condMKB = u'''      AND (LEFT(Diagnosis.MKB, 1) = 'C' OR (LEFT(Diagnosis.MKB, 3) BETWEEN 'D00' AND 'D09')
          OR (LEFT(AccDiagnosis.MKB, 3) = 'D70' AND (LEFT(AccDiagnosis.MKB, 3) = 'C97' OR (LEFT(AccDiagnosis.MKB, 3) BETWEEN 'C00' AND 'C80'))))'''
    else:
        joinMKB = u''
        condMKB = u''

    u"""Возвращает словарь с записями по онкологии и направлениям,
        ключ - идентификатор события"""
    stmt = """SELECT Event.id AS eventId,
        Event.setDate AS eventSetDate,
        rbDiseasePhases.code AS diseasePhaseCode,
        rbTNMphase_Identification.value AS STAD,
        rbTumor_Identification.value AS ONK_T,
        rbNodus_Identification.value AS ONK_N,
        rbMetastasis_Identification.value AS ONK_M,
        rbMetastasis.code AS metastasisCode,
        Sod.value AS SOD,
        IF(GistologiaAction.id IS NOT NULL, 1,
            IF(ImmunohistochemistryAction.id IS NOT NULL, 2,
                0)) AS DIAG_TIP,
        GistologiaAction.id AS gistologiaActionId,
        ImmunohistochemistryAction.id AS immunohistochemistryActionId,
        ControlListOnkoAction.id AS ControlListOnkoActionId,
        DirectionAction.endDate AS NAPR_DATE,
        DirectionAction.id AS directionActionId
    FROM Account_Item
    LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
    LEFT JOIN Event ON Event.id = Account_Item.event_id
    LEFT JOIN Diagnostic ON (Diagnostic.event_id = Account_Item.event_id
        AND Diagnostic.diagnosisType_id IN (
            SELECT id
            FROM rbDiagnosisType
            WHERE code IN ('1', '2'))
        AND Diagnostic.person_id = Event.execPerson_id
        AND Diagnostic.deleted = 0)
    {joinMKB}
    LEFT JOIN rbDiseasePhases ON Diagnostic.phase_id = rbDiseasePhases.id
    LEFT JOIN rbTNMphase_Identification ON
        rbTNMphase_Identification.master_id = IFNULL(
            Diagnostic.cTNMphase_id, Diagnostic.pTNMphase_id)
        AND rbTNMphase_Identification.system_id = (
            SELECT MAX(id) FROM rbAccountingSystem
            WHERE rbAccountingSystem.code = 'tfoms51.N002'
        )
    LEFT JOIN rbTumor_Identification ON
        rbTumor_Identification.master_id = IFNULL(
            Diagnostic.cTumor_id, Diagnostic.pTumor_id)
        AND rbTumor_Identification.system_id = (
            SELECT MAX(id) FROM rbAccountingSystem
            WHERE rbAccountingSystem.code = 'tfoms51.N003'
        )
    LEFT JOIN rbNodus_Identification ON
        rbNodus_Identification.master_id = IFNULL(
            Diagnostic.cNodus_id, Diagnostic.pNodus_id)
        AND rbNodus_Identification.system_id = (
            SELECT MAX(id) FROM rbAccountingSystem
            WHERE rbAccountingSystem.code = 'tfoms51.N004'
        )
    LEFT JOIN rbMetastasis_Identification ON
        rbMetastasis_Identification.master_id = IFNULL(
            Diagnostic.cMetastasis_id, Diagnostic.pMetastasis_id)
        AND rbMetastasis_Identification.system_id = (
            SELECT MAX(id) FROM rbAccountingSystem
            WHERE rbAccountingSystem.code = 'tfoms51.N005'
        )
    LEFT JOIN rbMetastasis ON rbMetastasis.id = IFNULL(
        Diagnostic.cMetastasis_id, Diagnostic.pMetastasis_id)
    LEFT JOIN ActionProperty_String AS Sod ON Sod.id = (
        SELECT APS.id
        FROM Action A
        INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
        INNER JOIN ActionPropertyType AS APT ON APT.actionType_id = AT.id
        INNER JOIN ActionProperty AS AP ON AP.action_id = A.id AND AP.type_id = APT.id
        INNER JOIN ActionProperty_String AS APS ON APS.id = AP.id
        WHERE A.deleted = 0 AND A.event_id = Account_Item.event_id
            AND AP.deleted = 0
            AND AT.`flatCode` = 'ControlListOnko'
            AND APT.`shortName` = 'SOD'
        ORDER BY A.begDate DESC
        LIMIT 0, 1
    )
    LEFT JOIN Action AS GistologiaAction ON GistologiaAction.id = (
        SELECT MAX(A.id)
        FROM Action A
        LEFT JOIN Event E ON E.id = A.event_id
        WHERE E.client_id = Event.client_id
          AND A.deleted = 0
          AND A.actionType_id IN (
            SELECT AT.id
            FROM ActionType AT
            WHERE AT.flatCode ='Gistologia'
          )
    )
    LEFT JOIN Action AS ImmunohistochemistryAction ON ImmunohistochemistryAction.id = (
        SELECT MAX(A.id)
        FROM Action A
        LEFT JOIN Event E ON E.id = A.event_id
        WHERE E.client_id = Event.client_id
          AND A.deleted = 0
          AND A.actionType_id IN (
            SELECT AT.id
            FROM ActionType AT
            WHERE AT.flatCode ='Immunohistochemistry'
          )
    )
    LEFT JOIN Action AS ControlListOnkoAction ON ControlListOnkoAction.id = (
        SELECT MAX(A.id)
        FROM Action A
        LEFT JOIN Event E ON E.id = A.event_id
        WHERE E.client_id = Event.client_id
          AND A.deleted = 0
          AND A.actionType_id IN (
            SELECT AT.id
            FROM ActionType AT
            WHERE AT.flatCode ='ControlListOnko'
          )
    )
    LEFT JOIN Action AS DirectionAction ON DirectionAction.id = (
        SELECT MAX(A.id)
        FROM Action A
        LEFT JOIN Event E ON E.id = A.event_id
        WHERE E.client_id = Event.client_id
          AND A.deleted = 0
          AND A.actionType_id IN (
            SELECT AT.id
            FROM ActionType AT
            WHERE AT.flatCode IN ('inspectionDirection',
                'ConsultationDirection', 'hospitalDirection',
                'recoveryDirection')
          )
    )
    WHERE Account_Item.reexposeItem_id IS NULL
      AND (Account_Item.date IS NULL OR
           (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
      AND {idList}
      {condMKB}
      """ .format(joinMKB=joinMKB, idList=idList, condMKB=condMKB)
    query = db.query(stmt)
    result = {}

    while query.next():
        record = query.record()
        eventId = forceRef(record.value('eventId'))
        result[eventId] = record

    return result

# ******************************************************************************

def _exportBProt(dbf, _, params):
    u'Пишет сведения об имеющихся противопоказаниях и отказах'
    row = dbf.newRecord()
    row['CARD'] = params['eventId']
    onkRecord = params['onkologyInfo'].get(params['eventId'])
    if onkRecord:
        action = CAction.getActionById(forceRef(onkRecord.value(
            'controlListOnkoActionId')))
        prop = (action['PROT'] if action and action.hasProperty('PROT')
                else None)

        if prop:
            row['PROT'] = prop.type().descr % 10
            row['D_PROT'] = prop.getValueScalar()

    row.store()

# ******************************************************************************

def _exportOnkSl(dbf, _, params):
    u'Пишет cведения о случае лечения онкологического заболевания'
    row = dbf.newRecord()
    row['CARD'] = params['eventId']
    onkRecord = params['onkologyInfo'].get(params['eventId'])
    if onkRecord:
        row['DS1_T'] = forceInt(onkRecord.value('diseasePhaseCode')) % 10

        for field in ('STAD', 'ONK_T', 'ONK_M', 'ONK_N'):
            row[field] = forceInt(onkRecord.value(field)) % 1000
        metastasisCode = forceString(onkRecord.value('metastasisCode'))
        row['MTSTZ'] = 1 if (metastasisCode and metastasisCode not in ('M0', 'Mx')) else 0 % 10
        row['SOD'] = forceDouble(onkRecord.value('SOD'))
    row.store()

# ******************************************************************************

def _exportBDiag(dbf, _, params):
    u'Пишет сведения о проведенных исследованиях и их результатах'
    row = dbf.newRecord()
    row['CARD'] = params['eventId']
    onkRecord = params['onkologyInfo'].get(params['eventId'])
    if onkRecord:
        row['DIAG_TIP'] = forceInt(onkRecord.value('DIAG_TIP')) % 10

        gistologiaActionId = forceRef(onkRecord.value(
            'gistologiaActionId'))
        immunohistochemistryActionidId = forceRef(onkRecord.value(
            'immunohistochemistryActionId'))
        action = CAction.getActionById((
            gistologiaActionId if gistologiaActionId else
            immunohistochemistryActionidId))

        if action:
            actionProperty = action.getProperties()[0]
            text = actionProperty.getTextScalar()
            descr = forceInt(actionProperty.type().descr)
        else:
            text = None
            descr = 0

        row['DIAG_CODE'] = descr % 1000
        row['DIAG_RSLT'] = mapDiagRslt.get((descr, text), 0) % 100
    row.store()

# ******************************************************************************

def processVisitAct(dbf, record, params):
    u"""Заполняет таблицу VISITACT"""
    (_, _, _, _, _, dbfVisitAct, _, _, _, _, _, _, _, _, _, _) = dbf

    # заполняется только для CODE_HOSP=655
    if dbfVisitAct and params['lpuCode'] == '655':
        row = dbfVisitAct.newRecord()
        row['LPU'] = params['lpuCode']
        row['INS'] = params['payerInfis']
        #OKPO - не заполнять
        row['ACT'] = params['accNumber']
        row['DATE_LOW'] = pyDate(forceDate(record.value('endDate')))
        exposeDate = params['exposeDate']
        row['DATE_UP'] = pyDate(exposeDate if exposeDate else
                                QDate.currentDate())
        row['SPEC_PROF'] = '622'
        # количество услуг с кодом '946230300', оказанных врачом с SPEC=622
        row['VISITS'] = forceInt(record.value('visits'))
        #SERV_KIND - пока пустое
        #UNITS - пока пустое
        row.store()

def formatDocumentSerial(serial, docType):
    if docType == 3:
        serial = serial.strip().replace(' ', '-')
    return serial

# ******************************************************************************

class CExportWizard(CAbstractExportWizard):
    u"""Мастер экспорта в ОМС Мурманской области"""
    def __init__(self, parent=None):
        title = u'Мастер экспорта в ОМС Мурманской области'
        CAbstractExportWizard.__init__(self, parent, title)
        self.page1 = CExportPage1(self)
        self.page2 = CExportPage2(self)

        self.addPage(self.page1)
        self.addPage(self.page2)


    def getTmpDir(self):
        return CAbstractExportWizard.getTmpDirEx(self, 'R51OMS')

# ******************************************************************************

class CExportPage1(CAbstractExportPage1, Ui_ExportPage1, CExportHelperMixin):
    u"""Первая страница мастера экспорта"""

    exportType2019 = 0
    exportType2020 = 1
    exportType2021 = 2
    mapEventOrderToForPom = {2: 1, 6:2, 1:3}
    mapPrCons = {
        u'Первичное лечение': 0,
        u'Лечение при рецидиве': 1,
        u'Лечение при прогрессировании': 2,
        u'Динамическое наблюдение': 3,
        u'Диспансерное наблюдение (здоров/ремиссия)': 4,
    }

    def __init__(self, parent):
        CAbstractExportPage1.__init__(self, parent)
        CExportHelperMixin.__init__(self)
        self.prefix = 'ExportR51OMS'

        prefs = QtGui.qApp.preferences.appPrefs
        self.ignoreErrors = forceBool(
            prefs.get('%sIgnoreErrors' % self.prefix, False))
        self.chkVerboseLog.setChecked(forceBool(
            prefs.get('%sVerboseLog' % self.prefix, False)))
        self.cmbExportType.setCurrentIndex(
            forceInt(prefs.get('%sExportType' % self.prefix, 0)))
        self.chkIgnoreErrors.setChecked(self.ignoreErrors)

        self.exportType = self.cmbExportType.currentIndex()
        self.actionSkipList = []
        self.exportedEventSet = set()
        self.validActionTypeCache = {}
        self.actionTypeMultipleBirth = None
        self._personShortNameCache = {}
        self._nestedActionTypeSet = set()


    def validatePage(self):
        prefs = QtGui.qApp.preferences.appPrefs
        prefs['%sIgnoreErrors' % self.prefix] = toVariant(
            self.chkIgnoreErrors.isChecked())
        prefs['%sVerboseLog' % self.prefix] = toVariant(
            self.chkVerboseLog.isChecked())
        prefs['%sExportType' % self.prefix] = toVariant(
            self.cmbExportType.currentIndex())
        return CAbstractExportPage1.validatePage(self)


    def setExportMode(self, flag):
        self.btnCancel.setEnabled(flag)
        self.btnExport.setEnabled(not flag)
        self.chkIgnoreErrors.setEnabled(not flag)
        self.chkVerboseLog.setEnabled(not flag)
        self.btnExport.setEnabled(not flag)
        self.cmbExportType.setEnabled(not flag)

# ******************************************************************************

    def exportInt(self):
        params = {}
        self.actionSkipList = []
        self.exportedEventSet = set()
        self._personShortNameCache = {}
        self.ignoreErrors = self.chkIgnoreErrors.isChecked()
        self.exportType = self.cmbExportType.currentIndex()
        self._representativeInfo = dict(self._getRepresentativeInfo())
        params['exportType'] = self.exportType
        self.actionTypeMultipleBirth = forceRef(self.db.translate(
            'ActionType', 'flatCode', 'MultipleBirth', 'id'))

        if not self.actionTypeMultipleBirth:
            self.logError(u'Не найден тип действия "Многоплодные роды" '
                          u'(плоский код: "MultipleBirth")')
            if not self.ignoreErrors:
                self.abort()
                return

        checkResult = self._diagnosisCheck()

        if checkResult:
            for (clientId, (eventList, mkb)) in checkResult.iteritems():
                self.logError(u'У пациента %d одинаковый диагноз %s'
                              u' в событиях %s' % (clientId, mkb, eventList))

            if not self.ignoreErrors:
                self.abort()
                return

        self.log(u'Выгружаем счет в формате "%d".' % self.exportType)

        record = self.db.getRecordEx(
            'ActionType', 'id', 'code=\'51\' AND class=\'3\'', 'id')
        ref = forceRef(record.value(0)) if record else None

        if not ref:
            self.log(u'В справочнике типов действий (ActionType)'
                     u' отсутствует запись с кодом 51, класс "прочее"'
                     u' (Группа для мед. услуг Мурмансккой области)')
            if not self.ignoreErrors:
                self.abort()
                return

        self.validActionTypeCache[ref] = True
        lpuId = QtGui.qApp.currentOrgId()
        params['lpuOKPO'] = forceString(self.db.translate(
            'Organisation', 'id', lpuId, 'OKPO'))
        params['lpuCode'] = forceString(self.db.translate(
            'Organisation', 'id', lpuId, 'infisCode'))
        params['lpuOGRN'] = forceString(self.db.translate(
            'Organisation', 'id', lpuId, 'OGRN'))

        self.log(u'ЛПУ: ОКПО "%s", ОГРН "%s",код инфис: "%s".' % (
            params['lpuOKPO'], params['lpuOGRN'], params['lpuCode']))

        if not params['lpuCode']:
            self.log(u'<b><font color=red>ОШИБКА<\font><\b>:'
                     u'Для текущего ЛПУ не задан код инфис', True)
            if not self.ignoreErrors:
                self.abort()
                return

        params.update(self.accountInfo())
        accOrgStructId = params['accOrgStructureId']
        record = self.db.getRecord('OrgStructure', 'infisCode, tfomsCode',
                                   accOrgStructId)
        if record:
            params['orgStructureInfisCode'] = forceString(record.value(
                'infisCode'))
            params['orgStructureTfomsCode'] = forceString(record.value(
                'tfomsCode'))

        params['mapEventIdToSum'] = self.getEventsSummaryPrice()
        params['payerInfis'] = forceString(self.db.translate(
            'Organisation', 'id', params['payerId'], 'infisCode'))
        params['__serviceNumber'] = 1

        params['onkologyInfo'] = self.getOnkologyInfo(exportType2019=True)
        self.setProcessParams(params)
        self.setProcessFuncList((self.process, self.processAddServ,
                                 processVisitAct))
        CAbstractExportPage1.exportInt(self)


    def createDbf(self):
        result = (self._createAliensDbf(), self._createServiceDbf(),
                  self._createAddInfDbf(), self._createAddServDbf(),
                  self._createCountsDbf(), self._createVisitActDbf(),
                  self._createDirectDbf(), self._createDs2nDbf(),
                  self._createOnkSlDbf(), self._createBDiagDbf(),
                  self._createBProtDbf(), self._createNaprDbf(),
                  self._createOnkUslDbf(), self._createLekPrDbf(),
                  self._createConsDbf())

        if self.exportType >= self.exportType2020:
            result += (self._createServTmtDbf(), )
        else:
            result += (None, )

        return result


    def _createAliensDbf(self):
        """ Создает структуру dbf для ALIENS.DBF """

        dbfName = os.path.join(self.getTmpDir(), 'ALIENS.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')

        policyNumberLen = 20
        passportFieldType = 'C'

        dbf.addField(
            ('CODE_HOSP', 'C', 3),     # Код ЛПУ пребывания по справочнику фонда
            ('CODE_COUNT', 'C', 10),   # Номер счета представляемого в СМО
            ('DATE_LOW', 'D', 8),      # Начальная дата интервала дат выписки
            ('DATE_UP', 'D', 8),       # Конечная дата интервала дат выписки
            ('CARD', 'C', 10),         # Номер статталона
            ('INS', 'C', 2),           # Код СМО (по справочнику фонда)
            ('SERPOL', 'C', 10),       # Серия полиса
            ('NMBPOL', 'C', policyNumberLen), # Номер полиса
            ('WORK', 'C', 1), #Признак работающий- “1”/неработающий – “0”
            ('DATIN', 'D', 8), # Дата поступления
            ('DATOUT', 'D', 8), # Дата выписки
            ('DIAG', 'C', 6), # Диагноз МКБ Х
            ('DS1_PR', 'N', 1), #Установлен впервые (основной)
            ('DS0', 'C', 6), # Диагноз первичный
            ('FAM', 'C', 40),          # Фамилия пациента
            ('IMM', 'C', 40),          # Имя пациента
            ('OTC', 'C', 40),          # Отчество пациента
            ('SER_PASP', 'C', 8), # Серия документа, удостоверяющего личность
            # Номер документа, удостоверяющего личность
            ('NUM_PASP', passportFieldType, 8),
            # Тип документа, удостоверяющего личность
            ('TYP_DOC', 'N', 2),
            # Страховой номер индивидуального лицевого счета (СНИЛС)
            ('SS', 'C', 14),
            ('BIRTHDAY', 'D', 8), # Дата рождения пациента
            ('SEX', 'C', 1), # Пол пациента («М», «Ж»)
            # Код населенного пункта проживания пациента по справочнику фонда
            ('TAUN', 'C', 3),
            ('MASTER', 'C', 3), # Код ЛПУ приписки
            # Сумма из средств Федеральных субвенций
            ('STOIM_S', 'N', 10, 2),
            # Тип полиса:   1 – старого образца,
            # 2 – временное свидетельство, 3 – нового образца
            ('TPOLIS', 'N', 1),
            ('PRIZN_ZS', 'N', 2), # признак законченного случая
            ('RSLT', 'N', 3),  # Результат обращения/ госпитализации
            ('ISHOD', 'N', 3),  # Исход заболевания
            ('DET', 'N', 1),  # Признак детского профиля
            # Код врача, закрывшего талон/историю болезни
            ('P_CODE', 'C', 14),
            ('FOR_POM', 'N', 1), # Форма оказания медицинской помощи
            ('VIDPOM', 'N', 4), # Вид медицинской помощи
            ('PROFIL', 'N', 3), # Профиль медицинской помощи
            ('PRVS', 'N', 4), # Специальность врача, закрывшего талон
            ('VID_FIN', 'N', 1), # Источник финансирования Всегда код-1
            ('INV', 'N', 1), #Группа инвалидности
            ('PR_D_N', 'N', 1), #Признак диспансерного наблюдения
            ('VBR', 'N', 1), #Признак мобильной медицинской бригады
            ('PR_OS', 'N', 2), #Признак “Особый случай»
            ('IDSP', 'N', 2), #Код способа оплаты медицинской помощи
            ('DS2', 'C', 6), #Диагноз  сопутствующего заболевания
            ('DS2_PR', 'N', 1), #Установлен впервые (сопутствующий)
            ('DS_ONK', 'N', 1), #Признак подозрения на злокачественное
                                #новообразование
            ('PURPOSE', 'C', 3), #
            ('NPR_MO', 'C', 3), #
            ('NPR_DATE', 'D'), #
            ('C_ZAB', 'N', 1), #
            ('DOCDATE', 'D'), #
            ('DOCORG', 'C', 250), #
            ('mpcod', 'C', 8), #
            ('addr_code', 'C', 16), #
        )
        if self.exportType >= self.exportType2021:
            dbf.addField(
                ('DS_PZ', 'C', 6), #
            )

        return dbf


    def _createServiceDbf(self):
        """ Создает структуру dbf для SERVICE.DBF """

        dbfName = os.path.join(self.getTmpDir(), 'SERVICE.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')

        serviceFieldSize = 15

        dbf.addField(
            ('CARD', 'C', 10),         # Номер статталона
            ('IDSERV', 'C', 36), #Номер записи в реестре услуг
            ('CODE_COUNT', 'C', 10),   # Номер счета представляемого в СМО
            # Личный код  медицинского работника, оказавшего услугу
            ('P_CODE', 'C', 14),
            # Код специальности медицинского работника, оказавшего услугу
            ('SPEC', 'C', 3),
            ('PROFIL', 'N', 3), #Профиль медицинской помощи
            ('PRVS', 'N', 4), #Специальность медицинского работника,
            ('SERVICE', 'C', serviceFieldSize), # Код услуги
            ('UNITS', 'N', 3),         # Кол-во услуг
            ('PR_VISIT', 'N', 1),
            ('SERV_DATE', 'D', 8),     # Дата оказания услуги
            ('DS', 'C', 6),  # Диагноз
            # Код ЛПУ, направившего пациента на консультацию (обследование)
            ('DIRECT_LPU', 'C', 3),
            ('DIR_SUBLPU', 'C',  (3 if self.exportType >= self.exportType2021
                                 else 2)),#Код структурного подразделения МО,
            #направившего пациента на консультацию (обследование)
            ('DIR_TOWN', 'C', 3), #Код населенного пункта структурного
            #подразделения МО, направившего пациента на консультацию
            # Цель обращения (указывается при приеме врача или консультации)
            ('AIM', 'C', 2),
            # Сумма из средств Федеральных субвенций
            ('STOIM_S', 'N', 10, 2),
            # Код специальности медицинского работника,
            # направившего пациента на консультацию
            ('DIR_SPEC', 'N', 4, 0),
            ('VID_FIN', 'N', 1),  #Источник финансирования
            ('PURPOSE', 'C', 3), #Цель посещения
            ('REASON', 'N', 2),  #Основание самообращения
            ('P_MODE', 'N', 2),  #Код способа оплаты медицинской помощи
            ('SUB_HOSP', 'C',  (3 if self.exportType >= self.exportType2021
                                 else 2)), # Код структурного подразделения МО
            ('TOWN_HOSP', 'C', 3), # Код населенного пункта структурного
                                   # подразделения МО
            ('DS1_PR', 'N', 1), #Установлен впервые (основной)
            ('NPL', 'N', 1), #Неполный объём
            ('SERV_METOD', 'C',  (5 if self.exportType >= self.exportType2021
                                 else 3)), #Код метода услуги
            ('P_OTK', 'N', 1), #Признак отказа от услуги
            ('NPR_DATE', 'D'), #Дата направления на диагностику,консультацию
            ('mpcod', 'C', 8), #
            ('addr_code', 'C', 16), #
        )
        if self.exportType >= self.exportType2021:
            dbf.addField(
                ('VID_VME', 'C', 16), #
            )
        return dbf


    def _createAddInfDbf(self):
        """ Создает структуру dbf для ADD_INF.DBF """

        dbfName = os.path.join(self.getTmpDir(), 'ADD_INF.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('CARD', 'C', 10),       #Номер истории болезни
            ('MR', 'C', 100),  # Место рождения пациента или представителя
            ('OKATOG', 'C', 11), # Код места жительства по ОКАТО
            ('OKATOP', 'C', 11), # Код места пребывания по ОКАТО
            # Код ОКАТО территории страхования по ОМС (по справочнику фонда)
            ('OKATO_OMS', 'C', 5),
            ('FAMP', 'C', 40), #Фамилия (представителя) пациента
            ('IMP', 'C', 40), #Имя  (представителя) пациента
            ('OTP', 'C', 40), #Отчество родителя (представителя) пациента
            ('DRP', 'D'), #Дата рождения (представителя) пациента
            ('WP', 'C', 1), #Пол (представителя) пациента
            # Код типа документа, удостоверяющего
            # личность пациента (представителя)
            ('C_DOC', 'N', 2),
            # Серия документа, удостоверяющего
            # личность пациента (представителя)
            ('S_DOC', 'C', 9),
            # Номер документа, удостоверяющего
            # личность пациента (представителя)
            ('N_DOC', 'C', 8),
            ('NOVOR', 'C', 9), # Признак новорожденного
            # Признак «Особый случай» при регистрации
            # обращения  за медицинской помощью
            ('Q_G', 'C', 7),
            ('MSE', 'N', 1), # Направление на МСЭ
            ('DOCDATE', 'D'), #
            ('DOCORG', 'C', 250), #
        )
        return dbf


    def _createAddServDbf(self):
        """ Создает структуру dbf для ADDSERV.DBF """

        dbfName = os.path.join(self.getTmpDir(), 'ADDSERV.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')

        dbf.addField(
            ('CARD', 'C', 10),        # Номер статталона
            ('SERVICE', 'C', 15),     # Код услуги
            ('SERV_PMU', 'C', 15), # Код услуги
            ('SERV_DATE', 'D', 8),   # Дата оказания услуги
            ('SERV_METOD', 'C',  (5 if self.exportType >= self.exportType2021
                                 else 3)), # Код признака услуги
            ('PRVS', 'N', 4), # Специальность медицинского работника
        )

        return dbf


    def _createCountsDbf(self):
        """ Создает структуру dbf для COUNTS.DBF """

        dbfName = os.path.join(self.getTmpDir(), 'COUNTS.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('IMC', 'C', 2),          # Код СМО
            # Идентификатор сводного реестра СМО в базе Фонда
            ('METACOUNT', 'N', 15),
            ('CODE_HOSP', 'C', 3),    # Код ЛПУ
            ('CODE_COUNT', 'N', 15),  # Идентификатор реестра ЛПУ базе в СМО
            ('COUNT', 'C', 10),       # Идентификатор реестра в ЛПУ
            ('DATA_DO', 'D', 8),      # Начальная дата интервала дат выписки
            ('DATA_UP', 'D', 8),      # Конечная дата интервала дат выписки
            # Количество записей в основной таблице реестра
            ('KOL_SBO', 'N', 5),
            ('FILE_NAME', 'C', 80), # Перечень имен вложенных файлов
            ('DATA_R', 'D', 8), # Дата формирования реестра в СМО
            )
        return dbf


    def _createVisitActDbf(self):
        """ Создает структуру dbf для VISITACT.DBF """

        dbfName = os.path.join(self.getTmpDir(), 'VISITACT.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('LPU', 'C', 3),           # Код АПУ
            ('INS', 'C', 2),           # Код СМО
            ('OKPO', 'C', 8),          # Код ОКПО  ЛПУ пребывания
            ('ACT', 'C', 10),          # Номер акта представляемого в Фонд
            # Начальная дата интервала дат оказания услуг
            ('DATE_LOW', 'D', 8),
            # Конечная дата интервала дат оказания услуг
            ('DATE_UP', 'D', 8),
            ('SPEC_PROF', 'C', 3),     # Профиль специалиста
            ('VISITS', 'N', 10),       # Количество посещений
            ('SERV_KIND', 'C', 2),
            ('UNITS', 'N', 10, 2)
            )
        return dbf


    def _createDirectDbf(self):
        """ Создает структуру dbf для DIRECT.DBF """
        return createDirectDbf(self.getTmpDir())


    def _createDs2nDbf(self):
        """ Создает структуру dbf для DS2_N.DBF """
        return createDs2nDbf(self.getTmpDir())


    def _createOnkSlDbf(self):
        u'Сведения о случае лечения онкологического заболевания'
        dbfName = os.path.join(self.getTmpDir(), 'ONK_SL.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('CARD', 'C', 10), # Номер статталона
            ('DS1_T', 'N', 1), # Повод обращения
            ('STAD', 'N', 3), # Стадия заболевания
            ('ONK_T', 'N', 3), #
            ('ONK_N', 'N', 3), #
            ('ONK_M', 'N', 3), #
            ('MTSTZ', 'N', 1), #
            ('SOD', 'N', 6, 2), #
            ('K_FR', 'N', 2, 0), #
            ('WEI', 'N', 5, 1), #
            ('HEI', 'N', 3, 0), #
            ('BSA', 'N', 4, 2), #
        )
        return dbf


    def _createBDiagDbf(self):
        u"""Диагностический блок, содержит сведения о проведенных
            исследованиях и их результатах"""
        dbfName = os.path.join(self.getTmpDir(), 'B_DIAG.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('CARD', 'C', 10), # Номер статталона
            ('DIAG_DATE', 'D', 8),
            ('DIAG_TIP', 'N', 1),
            ('DIAG_CODE', 'N', 3),
            ('DIAG_RSLT', 'N', 3),
            ('REC_RSLT', 'N', 1),
        )
        return dbf


    def _createBProtDbf(self):
        u"""Сведения об имеющихся противопоказаниях и отказах"""
        dbfName = os.path.join(self.getTmpDir(), 'B_PROT.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('CARD', 'C', 10), # Номер статталона
            ('PROT', 'N', 1),
            ('D_PROT', 'D'), # Дата регистрации противопоказания или отказа
        )
        return dbf


    def _createConsDbf(self):
        u'Сведения о проведении консилиума'
        dbfName = os.path.join(self.getTmpDir(), 'CONS.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('CARD', 'C', 10),   # Номер статталона
            ('PR_CONS', 'N', 1), # Цель проведения консилиума
            ('DT_CONS', 'D', 8), # Дата проведения консилиума
        )
        return dbf


    def _createNaprDbf(self):
        u'Направления'
        return createNaprDbf(self.getTmpDir(), exportType2019=True)


    def _createOnkUslDbf(self):
        u"""Сведения об услуге при лечении онкологического заболевания"""
        dbfName = os.path.join(self.getTmpDir(), 'ONK_USL.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('CARD', 'C', 10), # Номер статталона
            ('IDSERV', 'C', 36), #
            ('USL_TIP', 'N', 1), #
            ('HIR_TIP', 'N', 1), #
            ('LEK_TIP_L', 'N', 1), #
            ('LEK_TIP_V', 'N', 1), #
            ('PPTR', 'N', 1), #
            ('LUCH_TIP', 'N', 1), #
        )

        return dbf


    def _createLekPrDbf(self):
        u'Сведения о введенном противоопухолевом лекарственном препарате'
        dbfName = os.path.join(self.getTmpDir(), 'LEK_PR.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('CARD', 'C', 10), # Номер статталона
            ('IDSERV', 'C', 36), #
            ('REGNUM', 'C', 6), #
            ('CODE_SH', 'C', 10), #
            ('DATE_INJ', 'D', 8), #
        )
        return dbf


    def _createServTmtDbf(self):
        return createServTmtDbf(self.getTmpDir())


    def getEventsSummaryPrice(self):
        u"""возвращает общую стоимость услуг за событие"""

        stmt = """SELECT event_id,
            SUM(Account_Item.sum) AS totalSum,
            SUM(Contract_Tariff.federalPrice) AS federalSum,
            (SELECT COUNT(DISTINCT Visit.id)
                FROM Visit
                WHERE Visit.event_id = Account_Item.event_id
                  )  AS visitCount
        FROM Account_Item
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        LEFT JOIN Contract_Tariff ON Account_Item.tariff_id = Contract_Tariff.id
        WHERE Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s
        GROUP BY event_id;
        """ % self.tableAccountItem['id'].inlist(self.idList)

        query = self.db.query(stmt)
        result = {}

        while query.next():
            record = query.record()
            eventId = forceRef(record.value('event_id'))
            _sum = forceDouble(record.value('totalSum'))
            federal = forceDouble(record.value(2))
            visits = forceInt(record.value('visitCount'))
            result[eventId] = (_sum, federal, visits)

        return result


    def createQuery(self):
        stmt = u"""SELECT Event.client_id,
                Account_Item.event_id,
                ClientPolicy.serial AS policySerial,
                ClientPolicy.number AS policyNumber,
                rbPolicyKind.regionalCode AS policyKind,
                IF(work.title IS NOT NULL,
                    work.title,
                    ClientWork.freeInput) AS clientWorkOrgName,
                Event.setDate AS begDate,
                Event.execDate AS endDate,
                Diagnosis.MKB,
                EventResult.regionalCode AS eventResultCode,
                IF(rbDiagnosticResult.regionalCode IS NULL,
                    EventResult.regionalCode,
                    rbDiagnosticResult.regionalCode) AS resultCode,
                Client.lastName,
                Client.firstName,
                Client.patrName,
                ClientDocument.serial AS documentSerial,
                ClientDocument.number AS documentNumber,
                rbDocumentType.regionalCode AS documentRegionalCode,
                ClientDocument.date AS DOCDATE,
                ClientDocument.origin AS DOCORG,
                Client.SNILS,
                Client.birthDate,
                Client.birthPlace,
                Client.sex,
                age(Client.birthDate, Event.execDate) as clientAge,
                RegAddressHouse.KLADRCode,
                RegAddressHouse.number,
                RegAddressHouse.corpus,
                RegAddress.flat,
                RegKLADR.infis AS placeCode,
                RegSOCR.infisCODE AS placeTypeCode,
                RegKLADR.NAME AS placeName,
                RegRegionKLADR.OCATD,
                RegStreet.NAME AS streetName,
                RegStreetSOCR.infisCODE AS streetType,
                AccDiagnosis.MKB AS accMKB,
                IF(Account_Item.visit_id IS NOT NULL, VisitPerson.SNILS,
                    IF(Account_Item.action_id IS NOT NULL,
                        IF(Action.person_id IS NOT NULL, ActionPerson.SNILS,
                            ActionSetPerson.SNILS), Person.SNILS)
                ) AS personCode,
                IF(Account_Item.visit_id IS NOT NULL, VisitSpeciality.regionalCode,
                    IF(Account_Item.action_id IS NOT NULL,
                        IF(Action.person_id IS NOT NULL, ActionSpeciality.regionalCode,
                            ActionSetSpeciality.regionalCode), rbSpeciality.regionalCode)
                )  AS specialityCode,
                IF(Account_Item.visit_id IS NOT NULL, VisitSpeciality.federalCode,
                    IF(Account_Item.action_id IS NOT NULL,
                        IF(Action.person_id IS NOT NULL, ActionSpeciality.federalCode,
                            ActionSetSpeciality.federalCode), rbSpeciality.federalCode)
                )  AS specialityFederalCode,
                rbService.infis AS service,
                Account_Item.amount,
                Visit.date AS visitDate,
                Action.endDate AS actionDate,
                Account_Item.`sum` AS `sum`,
                LEAST(IF(tariff.federalLimitation = 0,
                            Account_Item.amount,
                            LEAST(tariff.federalLimitation, Account_Item.amount)) * tariff.federalPrice,
                            Account_Item.sum)  AS federalSum,
                ClientPolicy.begDate AS policyBegDate,
                ClientPolicy.endDate AS policyEndDate,
                Insurer.OKATO AS insurerOKATO,
                Insurer.shortName AS insurerName,
                Insurer.OGRN AS insurerOGRN,
                Account_Item.id AS accountItem_id,
                Account_Item.action_id AS action_id,
                IF(BirthCertificate.id IS NOT NULL, 1, 0) AS hasBirthCertificate,
                EventType.regionalCode AS purposeCode,
                EventType.code AS eventTypeCode,
                RelegateOrg.infisCode AS relegateOrgCode,
                RelegateSpeciality.federalCode AS relegatePersonCode,
                tariff.tariffType,
                tariff.price,
                RelegateOrg.id AS relegateOrgId,
                Event.order AS eventOrder,
                rbPost.code AS postCode,
                Hospital.smoCode AS smoCode,
                Hospital.infisCode AS hospitalInfisCode,
                setOrgStruct.infisCode AS orgStructureInfisCode,
                rbMedicalAidKind.regionalCode AS medicalAidKindRegionalCode,
                (SELECT SId.value FROM rbSpeciality_Identification SId
                    WHERE SId.master_id = RelegatePerson.speciality_id
                      AND SId.deleted = 0
                      AND SId.system_id IN (
                        SELECT MAX(id) FROM rbAccountingSystem
                        WHERE code = 'tfoms51.dir_sublpu'
                          AND domain = 'rbSpeciality')
                LIMIT 1) AS relegatePersonSpecialityDirSubLpuCode,
                (SELECT SId.value FROM rbSpeciality_Identification SId
                    WHERE SId.master_id = RelegatePerson.speciality_id
                      AND SId.deleted = 0
                      AND SId.system_id IN (
                        SELECT MAX(id) FROM rbAccountingSystem
                        WHERE code = 'tfoms51.dir_spec'
                          AND domain = 'rbSpeciality')
                LIMIT 1) AS relegatePersonSpecialityDirSpecCode,
                RelegateOrg.tfomsExtCode AS relegateOrgTfomsExtCode,
                rbVisitType.regionalCode AS visitTypeRegionalCode,
                (SELECT infisCode FROM OrgStructure OS
                 WHERE OS.id = IFNULL(ActionPerson.orgStructure_id,
                                      VisitPerson.orgStructure_id)
                ) AS subHospital,
                VisitPerson.org_id AS visitPersonOrgId,
                ActionPerson.org_id AS actionPersonOrgId,
                (SELECT GROUP_CONCAT(S.note) FROM Account_Item A
                LEFT JOIN rbService S ON S.id = A.service_id
                WHERE A.event_id = Account_Item.event_id
                ) AS eventNote,
                IFNULL((SELECT SId.value FROM rbService_Identification SId
                    WHERE SId.master_id = rbService.id
                      AND SId.checkDate <= Event.execDate
                      AND SId.deleted = 0
                      AND SId.system_id IN (
                        SELECT MAX(id) FROM rbAccountingSystem
                        WHERE code = 'tfoms51.PURPOSE'
                          AND domain = 'rbService')
                ORDER BY SId.checkDate DESC LIMIT 1), rbService.note) AS serviceNote,
                rbSpeciality.regionalCode AS execPersonSpecialityRegionalCode,
                rbSpeciality.federalCode AS execPersonSpecialityFederalCode,
                rbMedicalAidProfile.regionalCode AS medicalAidProfileRegionalCode,
                ClientAttach.LPU_id AS clientAttachOrgId,
                ClientAttach.orgStructure_id AS clientAttachOrgStructId,
                ClientAttach.begDate AS clientAttachBegDate,
                ClientAttach.id AS clientAttachId,
                AttachOrg.smoCode AS attachOrgSmoCode,
                AttachOrg.infisCode AS attachOrgInfisCode,
                AttachOrg.tfomsExtCode AS attachOrgTfomsExtCode,
                rbScene.code AS sceneCode,
                Person.SNILS AS execPersonSNILS,
                CASE
                    WHEN rbDispanser.id IS NULL OR rbDispanser.name LIKE '%%нуждается%%' THEN 0
                    WHEN rbDispanser.observed = 1 AND rbDispanser.name LIKE '%%взят%%' THEN 2
                    WHEN rbDispanser.observed = 1 AND rbDispanser.name NOT LIKE '%%взят%%' THEN 1
                    WHEN rbDispanser.observed = 0 AND rbDispanser.name LIKE '%%выздор%%' THEN 4
                    WHEN rbDispanser.observed = 0 AND rbDispanser.name NOT LIKE '%%выздор%%' THEN 6
                    ELSE 0
                END AS dispanserObserved,
                Action.status AS actionStatus,
                rbService_Identification.value AS SERV_METOD,
                rbMedicalAidUnit.regionalCode AS medicalAidUnitCode,
                NOT ISNULL(CurrentOrgAttach.id) AS isAttached,
                rbScene.name LIKE "%%на дому%%" AS isHomeVisit,
                IF(AccCharacter.code = '2', 1, NULL) AS DS2_PR,
                IFNULL(Event.srcDate, Event.setDate) AS NPR_DATE,
                IF(rbDiseaseCharacter.code = '2', 1, 0) AS DS1_PR,
                IF(SUBSTR(Diagnosis.MKB, 1, 1) = 'Z', 0,
                    rbDiseaseCharacter_Identification.value) AS C_ZAB,
                (SELECT OSI.value
                 FROM OrgStructure_Identification OSI
                 WHERE OSI.master_id = IFNULL(Person.orgStructure_id,(
                        SELECT orgStructure_id
                        FROM Account WHERE Account.id = Account_Item.master_id))
                    AND OSI.deleted = 0
                    AND OSI.system_id = (
                        SELECT MAX(id) FROM rbAccountingSystem
                        WHERE rbAccountingSystem.code = 'mpcod')
                ) AS orgStructMpCod,
                (SELECT OSI.value
                 FROM OrgStructure_Identification OSI
                 WHERE OSI.master_id = setOrgStruct.id
                    AND OSI.deleted = 0
                    AND OSI.system_id = (
                        SELECT MAX(id) FROM rbAccountingSystem
                        WHERE rbAccountingSystem.code = 'addr_code')
                ) AS orgStructAddrCode,
                (SELECT SId.value FROM rbService_Identification SId
                    WHERE SId.master_id = rbService.id
                      AND SId.deleted = 0
                      AND SId.system_id IN (
                        SELECT MAX(id) FROM rbAccountingSystem
                        WHERE code = 'tfoms51.V001'
                          AND domain = 'rbService')
                LIMIT 1) AS vidVme
            FROM Account_Item
            LEFT JOIN Action ON Action.id = Account_Item.action_id
            LEFT JOIN Visit  ON Visit.id  = Account_Item.visit_id
            LEFT JOIN Event  ON Event.id  = Account_Item.event_id
            LEFT JOIN Client ON Client.id = Event.client_id
            LEFT JOIN ClientPolicy ON ClientPolicy.id =
                getClientPolicyIdForDate(Client.id, 1, Event.execDate)
            LEFT JOIN ClientAttach ON ClientAttach.id =
                getClientAttachIdForDate(Client.id, 0, Event.execDate)
            LEFT JOIN Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
            LEFT JOIN rbPolicyType ON rbPolicyType.id = ClientPolicy.policyType_id
            LEFT JOIN rbPolicyKind ON rbPolicyKind.id = ClientPolicy.policyKind_id
            LEFT JOIN ClientDocument ON ClientDocument.client_id = Client.id AND
                      ClientDocument.id = (SELECT MAX(CD.id)
                                         FROM   ClientDocument AS CD
                                         LEFT JOIN rbDocumentType AS rbDT ON rbDT.id = CD.documentType_id
                                         LEFT JOIN rbDocumentTypeGroup AS rbDTG ON rbDTG.id = rbDT.group_id
                                         WHERE  rbDTG.code = '1' AND CD.client_id = Client.id AND CD.deleted=0)
            LEFT JOIN rbDocumentType ON rbDocumentType.id = ClientDocument.documentType_id
            LEFT JOIN ClientDocument AS BirthCertificate ON BirthCertificate.client_id = Client.id AND
                      BirthCertificate.id = (SELECT MAX(CD.id)
                                         FROM   ClientDocument AS CD
                                         LEFT JOIN rbDocumentType AS rbDT ON rbDT.id = CD.documentType_id
                                         WHERE  rbDT.code = '3' AND CD.client_id = Client.id AND CD.deleted=0)
            LEFT JOIN ClientAddress ClientRegAddress ON ClientRegAddress.client_id = Client.id AND
                      ClientRegAddress.id = (SELECT MAX(CRA.id)
                                         FROM   ClientAddress AS CRA
                                         WHERE  CRA.type = 0 AND CRA.client_id = Client.id AND CRA.deleted=0)
            LEFT JOIN ClientAddress ClientLocAddress ON ClientLocAddress.client_id = Client.id AND
                      ClientLocAddress.id = (SELECT MAX(CLA.id)
                                         FROM   ClientAddress AS CLA
                                         WHERE  CLA.type = 1 AND CLA.client_id = Client.id AND CLA.deleted=0)
            LEFT JOIN Address   RegAddress ON RegAddress.id = ClientRegAddress.address_id
            LEFT JOIN AddressHouse RegAddressHouse ON RegAddressHouse.id = RegAddress.house_id
            LEFT JOIN kladr.KLADR RegKLADR ON RegKLADR.CODE = RegAddressHouse.KLADRCode
            LEFT JOIN (
                SELECT * FROM kladr.SOCRBASE AS SB
                GROUP BY SB.SCNAME
            ) AS  RegSOCR ON RegSOCR.SCNAME = RegKLADR.SOCR
            LEFT JOIN kladr.KLADR RegRegionKLADR ON RegRegionKLADR.CODE = (
                SELECT RPAD(LEFT(RegAddressHouse.KLADRCode,2),13,'0'))
            LEFT JOIN kladr.STREET RegStreet ON RegStreet.CODE = RegAddressHouse.KLADRStreetCode
            LEFT JOIN (
                SELECT * FROM kladr.SOCRBASE AS SB
                GROUP BY SB.SCNAME
            ) AS RegStreetSOCR ON RegStreetSOCR.SCNAME = RegStreet.SOCR
            LEFT JOIN Person ON Person.id = Event.execPerson_id
                AND Person.id IS NOT NULL
            LEFT JOIN Person AS VisitPerson ON VisitPerson.id = Visit.person_id
                AND VisitPerson.id IS NOT NULL
            LEFT JOIN Person AS ActionPerson ON ActionPerson.id = Action.person_id
                AND ActionPerson.id IS NOT NULL
            LEFT JOIN Person AS ActionSetPerson ON ActionSetPerson.id = Action.setPerson_id
                AND ActionSetPerson.id IS NOT NULL
            LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
                AND rbSpeciality.id IS NOT NULL
            LEFT JOIN rbSpeciality AS VisitSpeciality ON VisitPerson.speciality_id = VisitSpeciality.id
                AND VisitSpeciality.id IS NOT NULL
            LEFT JOIN rbSpeciality AS ActionSpeciality ON ActionPerson.speciality_id = ActionSpeciality.id
                AND ActionSpeciality.id IS NOT NULL
            LEFT JOIN rbSpeciality AS ActionSetSpeciality ON ActionSetPerson.speciality_id = ActionSetSpeciality.id
                AND ActionSetSpeciality.id IS NOT NULL
            LEFT JOIN Diagnostic ON ( Diagnostic.event_id = Account_Item.event_id
                                      AND Diagnostic.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code IN ('1', '2'))
                                      AND Diagnostic.person_id = Event.execPerson_id AND Diagnostic.deleted = 0)
            LEFT JOIN Diagnosis AS AccDiagnosis ON AccDiagnosis.id = (
                  SELECT MAX(ds.id)
                    FROM Diagnosis ds
                    INNER JOIN Diagnostic dc ON (ds.id = dc.diagnosis_id AND ds.deleted = 0 AND dc.deleted = 0)
                    WHERE dc.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code IN ('9', '10', '11'))
                    AND dc.event_id = Account_Item.event_id
            )
            LEFT JOIN ClientWork ON ClientWork.client_id=Event.client_id AND
                        ClientWork.id = (SELECT max(CW.id)
                                         FROM ClientWork AS CW
                                         WHERE CW.client_id=Client.id AND CW.deleted=0)
            LEFT JOIN Organisation AS work ON work.id=ClientWork.org_id AND work.deleted = 0
            LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
            LEFT JOIN rbDiagnosticResult ON rbDiagnosticResult.id=Diagnostic.result_id
            LEFT JOIN rbResult AS EventResult ON EventResult.id=Event.result_id
            LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
            LEFT JOIN EventType ON Event.eventType_id = EventType.id
            LEFT JOIN rbService ON rbService.id = IFNULL(Account_Item.service_id, IFNULL(Visit.service_id, EventType.service_id))
            LEFT JOIN OrgStructure AS setOrgStruct ON Person.orgStructure_id = setOrgStruct.id
            LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
            LEFT JOIN Contract_Tariff AS tariff ON Account_Item.tariff_id = tariff.id
            LEFT JOIN Person AS RelegatePerson ON Event.relegatePerson_id = RelegatePerson.id
            LEFT JOIN Organisation AS RelegateOrg ON Event.relegateOrg_id = RelegateOrg.id
            LEFT JOIN rbSpeciality AS RelegateSpeciality ON RelegatePerson.speciality_id = RelegateSpeciality.id
                AND  RelegatePerson.id IS NOT NULL
            LEFT JOIN rbPost ON rbPost.id = Person.post_id
            LEFT JOIN Organisation AS Hospital ON Hospital.id=Person.org_id AND Hospital.deleted = 0
            LEFT JOIN rbMedicalAidKind ON rbMedicalAidKind.id = EventType.medicalAidKind_id
            LEFT JOIN rbVisitType ON Visit.visitType_id = rbVisitType.id
            LEFT JOIN rbMedicalAidProfile ON rbMedicalAidProfile.id = rbService.medicalAidProfile_id
            LEFT JOIN rbScene ON rbScene.id = Visit.scene_id
            LEFT JOIN Organisation AS AttachOrg ON AttachOrg.id = ClientAttach.LPU_id
            LEFT JOIN rbDispanser ON Diagnostic.dispanser_id = rbDispanser.id
            LEFT JOIN rbService_Identification ON rbService_Identification.id = (
                SELECT MAX(SId.id)
                FROM rbService_Identification SId
                WHERE SId.master_id = rbService.id
                AND SId.system_id IN (SELECT id FROM rbAccountingSystem WHERE code = 'tfoms51.SERV3_METOD')
                AND SId.deleted = 0
            )
            LEFT JOIN rbMedicalAidUnit ON rbMedicalAidUnit.id = Account_Item.unit_id
            LEFT JOIN ClientAttach AS CurrentOrgAttach ON CurrentOrgAttach.id = (
                SELECT MAX(COA.id)
                FROM ClientAttach COA
                WHERE COA.LPU_id = %d AND COA.client_id = Client.id
                    AND (COA.begDate IS NULL OR COA.begDate <= Event.execDate)
                    AND (COA.endDate IS NULL OR COA.endDate >= Event.execDate)
            )
            LEFT JOIN rbDiseaseCharacter AS AccCharacter ON AccCharacter.id = AccDiagnosis.character_id
            LEFT JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnosis.character_id
            LEFT JOIN rbDiseaseCharacter_Identification ON rbDiseaseCharacter_Identification.id = (
                SELECT MAX(DId.id)
                FROM rbDiseaseCharacter_Identification DId
                WHERE DId.master_id = rbDiseaseCharacter.id
                AND DId.system_id IN (SELECT id FROM rbAccountingSystem WHERE urn = 'urn:tfoms51:V027')
                AND DId.deleted = 0
            )
            WHERE Account_Item.reexposeItem_id IS NULL
              AND (Account_Item.date IS NULL OR
                   (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
            AND %s
            ORDER BY Event.id
        """ % (QtGui.qApp.currentOrgId() if QtGui.qApp.currentOrgId() else 0,
               self.tableAccountItem['id'].inlist(self.idList))
        query = self.db.query(stmt)
        return (query, self.createAddServQuery, self.createVisitActQuery)

# ******************************************************************************

    def createAddServQuery(self):
        u"""Создает запрос для запослнения таблицы ADDSERV"""

        tableEvent = self.db.table('Event')
        tableAction = self.db.table('Action')
        financeId = forceRef(self.db.translate(
            'Contract', 'id', self.accountInfo()['contractId'], 'finance_id'))
        stmt = """SELECT rbService.infis AS code,
               DefaultService.infis AS defaultCode,
               Action.begDate AS begDate,
               Action.endDate AS endDate,
               Event.id AS eventId,
               Event.execDate AS execDate,
               Event.client_id,
               ActionType.id AS actionTypeId,
               ActionType.name AS actionTypeName,
               ActionType.serviceType,
               Action.id,
               rbService_Identification.value AS SERV_METOD,
               rbSpeciality.federalCode AS specialityFederalCode
        FROM Action
        LEFT JOIN Event ON Action.event_id = Event.id
        LEFT JOIN ActionType ON Action.actionType_id = ActionType.id
        LEFT JOIN ActionType_Service ON ActionType_Service.id =
            ( SELECT MIN(ATS.id) FROM ActionType_Service ATS
             WHERE ATS.master_id=ActionType.id %s)
        LEFT JOIN ActionType_Service AS DefaultATS ON DefaultATS.id =
            ( SELECT MIN(ATS2.id) FROM ActionType_Service ATS2
             WHERE ATS2.master_id=ActionType.id AND ATS2.finance_id IS NULL)
        LEFT JOIN rbService ON ActionType_Service.service_id = rbService.id
        LEFT JOIN rbService AS DefaultService ON DefaultATS.service_id = DefaultService.id
        LEFT JOIN rbService_Identification ON rbService_Identification.id = (
            SELECT MAX(SId.id)
            FROM rbService_Identification SId
            WHERE SId.master_id = IFNULL(rbService.id, DefaultService.id)
            AND SId.system_id IN (SELECT id FROM rbAccountingSystem WHERE code = 'tfoms51.SERV3_METOD')
            AND SId.deleted = 0
        )
        LEFT JOIN Person ON Action.person_id = Person.id
        LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
        WHERE %s AND %s
        """ % ('AND ATS.finance_id=%d' % financeId if financeId else '',
               tableEvent['id'].inlist(list(self.exportedEventSet)),
               tableAction['id'].notInlist(self.actionSkipList))

        query = self.db.query(stmt)
        return query


# ******************************************************************************

    def createVisitActQuery(self):
        u"""Создает запрос для запослнения таблицы VISITACT"""

        stmt = """SELECT endDate, SUM(amount) AS visits FROM (
            SELECT  IF(Account_Item.visit_id IS NOT NULL, VisitSpeciality.regionalCode,
                    IF(Account_Item.action_id IS NOT NULL,
                        IF(Action.person_id IS NOT NULL, ActionSpeciality.regionalCode,
                            ActionSetSpeciality.regionalCode), rbSpeciality.regionalCode)
                )  AS specialityCode,
                    IF(Account_Item.service_id IS NOT NULL,
                        rbItemService.infis,
                        IF(Account_Item.visit_id IS NOT NULL, rbVisitService.infis, rbEventService.infis)
                        ) AS service,
                Account_Item.amount,
                Event.execDate AS endDate
            FROM Account_Item
            LEFT JOIN Event ON Event.id = Account_Item.event_id
            LEFT JOIN Visit  ON Visit.id  = Account_Item.visit_id
            LEFT JOIN EventType ON Event.eventType_id = EventType.id
            LEFT JOIN Action ON Account_Item.action_id = Action.id
            LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
            LEFT JOIN rbService AS rbEventService ON rbEventService.id = EventType.service_id
            LEFT JOIN rbService AS rbVisitService ON rbVisitService.id = Visit.service_id
            LEFT JOIN rbService AS rbItemService ON rbItemService.id = Account_Item.service_id
            LEFT JOIN Person ON Person.id = Event.execPerson_id
                AND Person.id IS NOT NULL
            LEFT JOIN Person AS VisitPerson ON VisitPerson.id = Visit.person_id
                AND VisitPerson.id IS NOT NULL
            LEFT JOIN Person AS ActionPerson ON ActionPerson.id = Action.person_id
                AND ActionPerson.id IS NOT NULL
            LEFT JOIN Person AS ActionSetPerson ON ActionSetPerson.id = Action.setPerson_id
                AND ActionSetPerson.id IS NOT NULL
            LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
                AND rbSpeciality.id IS NOT NULL
            LEFT JOIN rbSpeciality AS VisitSpeciality ON VisitPerson.speciality_id = VisitSpeciality.id
                AND VisitSpeciality.id IS NOT NULL
            LEFT JOIN rbSpeciality AS ActionSpeciality ON ActionPerson.speciality_id = ActionSpeciality.id
                AND ActionSpeciality.id IS NOT NULL
            LEFT JOIN rbSpeciality AS ActionSetSpeciality ON ActionSetPerson.speciality_id = ActionSetSpeciality.id
                AND ActionSetSpeciality.id IS NOT NULL
            WHERE
                Account_Item.reexposeItem_id IS NULL
                AND (Account_Item.date IS NULL
                OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s) AS A
        WHERE specialityCode = '622' AND service = '946230300'""" % (
            self.tableAccountItem['id'].inlist(self.idList))

        query = self.db.query(stmt)
        return query


    def getOnkologyInfo(self, exportType2019=False):
        u'Возвращает информацию об онкологии'
        return getOnkologyInfo(self.db,
                               self.tableAccountItem['id'].inlist(self.idList),
                               exportType2019)

# ******************************************************************************

    regionNameCache = {}

    def getRegionName(self, code):
        u""" Возвращает название района. Области отфильтровываются."""

        result = self.regionNameCache.get(code, -1)

        if result != -1:
            result = ''

            if code != '':
                regionCode = code[:5].ljust(13, '0')
                result = (forceString(self.db.translate(
                    'kladr.KLADR', 'CODE', regionCode, 'NAME'))
                          if regionCode[2:5] != '000' else
                          self.getRegionCenterName(code))

            self.regionNameCache[code] = result

        return result

# ******************************************************************************

    regionCenterNameCache = {}

    def getRegionCenterName(self, code):
        u"""Возвращает название регионального центра."""

        result = self.regionCenterNameCache.get(code, -1)

        if result != -1:
            result = ''

            stmt = """SELECT `NAME` FROM kladr.KLADR
            WHERE `CODE` LIKE '%s%%' AND `STATUS` IN ('2','3')""" % code[:2]
            query = self.db.query(stmt)

            while query.next():
                record = query.record()

                if record:
                    result = forceString(record.value(0))

            self.regionCenterNameCache[code] = result

        return result


# ******************************************************************************

    def processAddServ(self, dbf, record, _):
        u"""Заполняет таблицу ADDSERV"""
        (_, _, _, dbfAddServ, _, _, _, _, _, _, _, _, _, _, _, _) = dbf

        eventId = forceRef(record.value('eventId'))
        actionTypeId = forceRef(record.value('actionTypeId'))
        servEndDate = forceDate(record.value('endDate'))
        servCode = forceString(record.value('code'))
        isValidServiceType = (forceInt(record.value('serviceType')) !=
                              CActionServiceType.initialInspection)

        if isValidServiceType:
            row = dbfAddServ.newRecord()
            row['CARD'] = eventId
            row['SERV_DATE'] = pyDate(servEndDate)
            row['SERV_METOD'] = forceString(record.value('SERV_METOD'))[:3]
            row['PRVS'] = (forceInt(record.value('specialityFederalCode')) %
                           10000)

            if self.isValidActionTypeId(actionTypeId):
                row['SERVICE'] = servCode if servCode else forceString(
                    record.value('defaultCode'))
            else:
                row['SERV_PMU'] = servCode if servCode else forceString(
                    record.value('defaultCode'))

            row.store()

# ******************************************************************************

    def process(self, dbf, record, params):
        localParams = {}
        localParams.update(params)

        localParams['birthDate'] = forceDate(record.value('birthDate'))
        localParams['begDate'] = forceDate(record.value('begDate'))
        localParams['endDate'] = forceDate(record.value('endDate'))
        # Номер стат.талона
        localParams['eventId'] = forceRef(record.value('event_id'))
        localParams['clientId'] = forceRef(record.value('client_id'))
        localParams['mkb'] = forceString(record.value('MKB'))
        localParams['kladrCode'] = forceString(record.value('KLADRCode'))

        if not localParams['kladrCode']:
            self.logWarning(u'Отсутвует КЛАДР адрес проживания и регистрации'
                            u' для клиента clientId=%d' % (
                                localParams['clientId']))

        attachOrgStructCode = ''
        localParams['isAttach'] = forceRef(record.value(
            'clientAttachId')) is not None
        localParams['attachOrgCode'] = ''

        if localParams['isAttach']:
            clientAttachOrgId = forceRef(record.value('clientAttachOrgId'))
            localParams['clientAttachOrgId'] = clientAttachOrgId
            clientAttachOrgStructId = forceRef(
                record.value('clientAttachOrgStructId'))
            localParams['clientAttachBegDate'] = forceDate(
                record.value('clientAttachBegDate'))

            if clientAttachOrgId:
                localParams.update(self._getAttachOrgCodes(clientAttachOrgId))

            if clientAttachOrgStructId:
                attachOrgStructCode = self.getOrgStructureInfisCode(
                    clientAttachOrgStructId)
            else:
                self.log(u'В записи прикрепления отсутствует код ЛПУ, пациент '
                         u'{0}'.format(localParams['clientId']))

        else:
            self.logWarning(u'Не задано ЛПУ постоянного прикрепления'
                            u' пациента. clientId=%d' % localParams['clientId'])

        localParams['attachOrgStructCode'] = attachOrgStructCode

        (dbfAliens, dbfService, dbfAddInf, _, _, _, _, dbfDs2n, dbfOnkSl,
        dbfBDiag, dbfBProt, dbfNapr, dbfOnkUsl, _, dbfCons, _) = dbf

        mkb = localParams['mkb']
        accMKB = forceString(record.value('accMKB'))
        onkDiag = (mkb[:1] == 'C'
                    or ('D00' <= mkb[:3] <= 'D09')
                    or ( mkb[:3] == 'D70' and ( accMKB[:3] == 'C97' or ( 'C00' <=  accMKB[:3] <= 'C80')))
                  )

        if localParams['eventId'] not in self.exportedEventSet:
            self._exportAliens(dbfAliens, record, localParams)
            self._exportAddInf(dbfAddInf, record, localParams)
            exportDs2n(dbfDs2n, record, localParams)
            params['ds2nCache'] = localParams.setdefault('ds2nCache', {})
            params['__serviceNumber'] = 1
            localParams.update(params)

            if (localParams.get('DS_ONK', 1) != 1 and onkDiag):
                _exportOnkSl(dbfOnkSl, record, localParams)
            if onkDiag:
                self._exportCons(dbfCons, record, localParams)
            if localParams.get('DS_ONK') == 1 or onkDiag:
                self._exportNapr(dbfNapr, record, localParams)
            if localParams.get('DS_ONK', 1) != 1 and onkDiag:
                self._exportOnkUsl(dbfOnkUsl, record, localParams)

        self._exportService(dbfService, record, localParams)
        actionId = forceRef(record.value('action_id'))

        if actionId:
            self.actionSkipList.append(actionId)

        self.exportedEventSet.add(localParams['eventId'])
        params['__serviceNumber'] = localParams['__serviceNumber']

# ******************************************************************************

    def _exportAliens(self, dbf, record, params):
        u"""Выгрузка информации в ALIENS.DBF из record и params"""

        endDate = params['endDate']
        eventId = params['eventId']
        exposeDate = params['exposeDate']
        mkb = params['mkb']

        row = dbf.newRecord()
        # Код ЛПУ пребывания по справочнику фонда
        infisCode = forceString(record.value('hospitalInfisCode'))
        row['CODE_HOSP'] = infisCode if infisCode else params['lpuCode']
        # Номер счета представляемого в СМО
        row['CODE_COUNT'] = params['accNumber']
        # Начальная дата интервала дат выписки
        row['DATE_LOW'] = pyDate(firstMonthDay(endDate))
        # Конечная дата интервала дат выписки
        row['DATE_UP'] = pyDate(exposeDate if exposeDate else
                                QDate.currentDate())
        # Номер статталона
        row['CARD'] = eventId
        # Код СМО (по справочнику фонда)
        row['INS'] = params['payerInfis']
        # Серия полиса
        row['SERPOL'] = forceString(record.value('policySerial'))
        # Номер полиса
        row['NMBPOL'] = forceString(record.value('policyNumber'))
        # Признак работающий- “1”/неработающий – “0”
        row['WORK'] = '1' if forceString(
            record.value('clientWorkOrgName')) != '' else '0'
        # Дата поступления
        row['DATIN'] = pyDate(params['begDate'])
        # Дата выписки
        row['DATOUT'] = pyDate(endDate)
        # Диагноз МКБ Х
        row['DIAG'] = mkb
        # Исход по справочнику фонда
        row['DS0'] = row['DIAG']
        # Фамилия пациента
        row['FAM'] = nameCase(forceString(record.value('lastName')))
        # Имя пациента
        row['IMM'] = nameCase(forceString(record.value('firstName')))
        # Отчество пациента
        row['OTC'] = nameCase(forceString(record.value('patrName')))

        docType = forceInt(record.value('documentRegionalCode'))
        # Серия документа, удостоверяющего личность
        row['SER_PASP'] = formatDocumentSerial(forceString(record.value(
            'documentSerial')), docType)
        # Номер документа, удостоверяющего личность
        row['NUM_PASP'] = forceString(record.value('documentNumber'))
        # Тип документа, удостоверяющего личность
        row['TYP_DOC'] = docType
        # Страховой номер индивидуального лицевого счета (СНИЛС)
        row['SS'] = formatSNILS(record.value('SNILS'))
        # Дата рождения пациента
        row['BIRTHDAY'] = pyDate(params['birthDate'])
        # Пол пациента   («М», «Ж»)
        row['SEX'] = formatSex(record.value('sex')).upper()
        # Код населенного пункта проживания пациента по справочнику фонда
        row['TAUN'] = forceString(record.value('placeCode'))
        if not row['TAUN']:
            self.log(u'Не задан инфис код для города "%s", clientId=%d' %\
                        (params['kladrCode'], params['clientId']))
        # Код ЛПУ приписки
        row['MASTER'] = params['attachOrgCode']
        row['TPOLIS'] = forceInt(record.value('policyKind'))

        (_sum, federalSum, _) = params['mapEventIdToSum'].get(
            eventId, (0.0, 0.0, 0))
        row['STOIM_S'] = _sum - federalSum
        # Результат обращения/ госпитализации
        row['RSLT'] = forceInt(record.value('eventResultCode')) % 1000
        # Исход заболевания
        row['ISHOD'] = forceInt(record.value('resultCode')) % 1000
        # Код врача, закрывшего талон/историю болезни
        row['P_CODE'] = formatSNILS(record.value('execPersonSNILS'))
        # Цель обращения 1 – профилактическая
        row['FOR_POM'] = self.mapEventOrderToForPom.get(
            forceInt(record.value('eventOrder')), 0) % 10

        if not row['FOR_POM']:
            self.logWarning(u'Cобытие `%d` имеет некорректный порядок'
                            u' `%d`, должен быть 1,2,6' % (
                                eventId, forceInt(record.value('eventOrder'))))

        row['VIDPOM'] = forceInt(record.value(
            'medicalAidKindRegionalCode')) % 10000
        row['PROFIL'] = forceInt(record.value(
            'execPersonSpecialityRegionalCode')) % 1000
        row['PRVS'] = forceInt(record.value(
            'execPersonSpecialityFederalCode')) % 10000
        row['VID_FIN'] = 1
        row['DS1_PR'] = forceInt(record.value('DS1_PR'))
        row['INV'] = 0
        row['PR_D_N'] = forceInt(record.value('dispanserObserved'))
        row['VBR'] = 0
        row['PR_OS'] = 0
        row['IDSP'] = (31 if params['attachOrgCode'] == params[
                           'lpuCode'] else forceInt(record.value(
                           'medicalAidUnitCode')))
        row['DS2'] = forceString(record.value('accMKB'))[:6]
        sign = forceInt(record.value('DS2_PR'))

        if sign:
            row['DS2_PR'] = sign

        accMKB = forceString(record.value('accMKB'))
        mkb = forceString(record.value('MKB'))
        onkRecord = params['onkologyInfo'].get(params['eventId'])
        phaseCode = forceInt(onkRecord.value('diseasePhaseCode')) if onkRecord else None
        row['DS_ONK'] = 1 if (phaseCode == 10 and (mkb[:1] == 'C' or (
            'D00' <= mkb[:3] <= 'D09') or (
            mkb[:3] == 'D70' and (
                ( 'C00' <= accMKB[:3] <= 'C80') or
                accMKB[:3] == 'C97')))) else 0

        params['DS_ONK'] = row['DS_ONK']

        codeSet = set(forceString(record.value('eventNote')).split(','))
        row['PURPOSE'] = '301' if '301' in codeSet else forceString(
            record.value('serviceNote'))
        row['NPR_MO'] = forceString(record.value('relegateOrgCode'))
        row['NPR_DATE'] = pyDate(forceDate(record.value('NPR_DATE')))
        row['C_ZAB'] = forceInt(record.value('C_ZAB')) % 10
        row['DOCDATE'] = pyDate(forceDate(record.value('DOCDATE')))
        row['DOCORG'] = forceString(record.value('DOCORG'))[:250]
        row['mpcod'] = forceString(record.value('orgStructMpCod'))[:8]
        row['addr_code'] = forceString(record.value('orgStructAddrCode'))[:16]
        if self.exportType >= self.exportType2021 and phaseCode == 10:
            row['DS_PZ'] = mkb
        row.store()

# ******************************************************************************

    def _exportService(self, dbf, record, params):
        u"""Выгрузка информации в SERVICE.DBF из record и params"""

        eventId = params['eventId']
        row = dbf.newRecord()
        # Номер статталона
        row['CARD'] = eventId
        # Номер счета представляемого в СМО
        row['CODE_COUNT'] = params['accNumber']
        # Личный код  медицинского работника, оказавшего услугу
        row['P_CODE'] = formatSNILS(record.value('personCode'))

        if not row['P_CODE']:
            self.log(u'Для события "%d" не задан региональный код'
                     u' исполнителя.' % eventId)

        # Код услуги
        row['SERVICE'] = forceString(record.value('service'))
        # Кол-во услуг
        row['UNITS'] = forceDouble(record.value('amount'))
        # Дата оказания услуги
        servDate = forceDate(record.value('actionDate'))

        if not servDate:
            servDate = forceDate(record.value('visitDate'))

            if not servDate:
                servDate = params['endDate']

        if not servDate:
            self.log(u'Не задана дата услуги: accountItemId=%d,'
                     u' код карточки "%d".' % (
                         forceRef(record.value('accountItem_id')), eventId))

        row['SERV_DATE'] = pyDate(servDate)
        row['DS'] = forceString(record.value('MKB'))

        # Для услуг с правилом тарификации Мероприятие по кол-ву:
        # Если НЕТ внешнего направителя - заполнять поле DIRECT_LPU кодом
        # ТФОМС текущего ЛПУ, а поле DIR_SPEC федеральным кодом
        # специальности врача, ответственного за событие.

        relegateOrgId = forceRef(record.value('relegateOrgId'))
        tariffType = forceInt(record.value('tariffType'))

        #Для типов событий с code=19-cz поле DIRECT_LPU заполняется таким
        # образом:
        #- тарификация 'Мероприятие по количеству' - ВСЕГДА
        #   заполнять поле DIRECT_LPU ИНФИС кодом подразделения,
        # сформировавшего счет (независимо от внешнего направителя)
        #- тарификация 'Посещение' - если НЕТ внешнего направителя - поле
        # пустое. Если ЕСТЬ внешний направитель - код ТФОМС ЛПУ-направителя.
        eventTypeCode = forceString(record.value('eventTypeCode'))

        if eventTypeCode == '19-cz':
            if tariffType == CTariff.ttActionAmount:
                row['DIRECT_LPU'] = self.getOrgStructureInfisCode(
                    QtGui.qApp.currentOrgStructureId())
            elif tariffType == CTariff.ttVisit:
                row['DIRECT_LPU'] = forceString(record.value(
                    'relegateOrgCode')) if relegateOrgId else ''
        else:
            # Если НЕТ внешнего направителя - заполнять поле DIRECT_LPU
            # кодом ТФОМС ЛПУ, к которому прикреплен пациент!! а поле
            # DIR_SPEC федеральным кодом специальности врача,
            # ответственного за событие - теперь необходимо сделать для
            # услуг ТОЛЬКО с правилом тарификации Мероприятие по количеству.
            # Т.е. для услуг с правилом тарификации Посещение -Если НЕТ
            # внешнего направителя - поля DIRECT_LPU и DIR_SPEC оставлять
            # пустыми! Дополняем логику заполнения поля DIRECT_LPU - Если
            # НЕТ внешнего направителя - заполнять поле DIRECT_LPU кодом
            # ТФОМС ЛПУ,к которому прикреплен пациент. Если у пациента в
            # прикреплении указано еще подразделение - тогда выгружать код
            # этого отделения по ИНФИС (аналогично полю CODE_HOSP),
            # учитывая условие  "При выставлении счетов учитывать текущее
            # подразделение"

            if not relegateOrgId:
                if tariffType == CTariff.ttActionAmount:
                    # Код ЛПУ, направившего пациента на
                    # консультацию (обследование)
                    if (QtGui.qApp.filterPaymentByOrgStructure() and
                            params['attachOrgStructCode']):
                        row['DIRECT_LPU'] = params['attachOrgStructCode']
                    else:
                        row['DIRECT_LPU'] = params['attachOrgCode']
            else:
                row['DIRECT_LPU'] = forceString(record.value(
                    'relegateOrgCode'))

        row['STOIM_S'] = (forceDouble(record.value('sum')) -
                          forceDouble(record.value('federalSum')))

        row['PROFIL'] = forceInt(record.value(
            'medicalAidProfileRegionalCode')) % 1000
        row['PRVS'] = forceInt(record.value(
            'specialityFederalCode')) % 10000

        if relegateOrgId:
            row['DIRECT_LPU'] = forceString(record.value(
                'relegateOrgCode'))
            row['DIR_TOWN'] = forceString(record.value(
                'relegateOrgTfomsExtCode'))
            row['DIR_SUBLPU'] = forceString(record.value(
                'relegatePersonSpecialityDirSubLpuCode'))
            row['DIR_SPEC'] = forceInt(record.value(
                'relegatePersonSpecialityDirSpecCode')) % 10000
        elif tariffType == CTariff.ttActionAmount:
            row['DIRECT_LPU'] = forceString(
                record.value('attachOrgInfisCode'))
            row['DIR_TOWN'] = forceString(
                record.value('attachOrgTfomsExtCode'))
            row['DIR_SUBLPU'] = forceString(record.value('attachOrgSmoCode'))
            age = forceInt(record.value('clientAge'))
            row['DIR_SPEC'] = 49 if age < 18 else 76

        row['VID_FIN'] = 1
        row['PURPOSE'] = forceString(record.value('serviceNote'))
        visitType = forceString(record.value('visitTypeRegionalCode'))

        if visitType == '04':
            row['REASON'] = 1
        elif visitType == '06':
            row['REASON'] = 2
        else:
            caBegDate = params.get('clientAttachBegDate', QDate())

            if (caBegDate and
                    caBegDate.year() == params['begDate'].year() and
                    caBegDate.month() == params['begDate'].month()):
                row['REASON'] = 3

        year = 0

        for field in ('visitDate', 'actionDate', 'begDate'):
            serviceDate = forceDate(record.value(field))

            if serviceDate.isValid():
                year = serviceDate.year()
                break

        visitPersonOrgId = forceRef(record.value('visitPersonOrgId'))

        if not visitPersonOrgId:
            visitPersonOrgId = forceRef(record.value('actionPersonOrgId'))

        clientAttachOrgId = params.get('clientAttachOrgId')
        pMode = 0

        if year == 2015:
            pMode = 8 if clientAttachOrgId == visitPersonOrgId else 9
        elif year >= 2016:
            if not params['isAttach']:
                pMode = 15
            else:
                pMode = 13 if clientAttachOrgId == visitPersonOrgId else 14

        row['P_MODE'] = pMode

        sceneCode = forceString(record.value('sceneCode'))

        if sceneCode in ('2', '3'):
            row['PR_VISIT'] = 1

        row['SUB_HOSP'] = (forceString(record.value('subHospital'))
                           if self.exportType >= self.exportType2021
                           else params.get('orgStructureInfisCode', ''))
        row['TOWN_HOSP'] = params.get('orgStructureTfomsCode', '')

        if row['SERV_DATE'].year == 2015:
            row['SPEC'] = forceString(record.value('specialityFederalCode'))

        row['NPL'] = mapAcionStatusToNpl.get(
            forceInt(record.value('actionStatus')), 0)
        if row['NPL'] == 4 and servDate >= params['begDate']:
            row['NPL'] = 0
        row['SERV_METOD'] = forceString(record.value('SERV_METOD'))
        row['P_OTK'] = 0
        row['NPR_DATE'] = pyDate(forceDate(record.value('NPR_DATE')))
        row['IDSERV'] = str(params['__serviceNumber'])
        params['__serviceNumber'] += 1
        row['mpcod'] = forceString(record.value('orgStructMpCod'))[:8]
        row['addr_code'] = forceString(record.value('orgStructAddrCode'))[:16]

        if self.exportType >= self.exportType2021:
            row['VID_VME'] = forceString(record.value('vidVme'))
        row.store()

# ******************************************************************************

    def _exportAddInf(self, dbf, record, params):
        u"""Выгрузка информации в ADD_INF.DBF из record и params."""

        clientId = params['clientId']
        row = dbf.newRecord()
        #Номер истории болезни
        row['CARD'] = params['eventId']
        # Место рождения пациента или представителя
        row['MR'] = forceString(record.value('birthPlace'))
        # Код места жительства по ОКАТО
        row['OKATOG'] = forceString(record.value('OCATD'))
        # Код места пребывания по ОКАТО
        row['OKATOP'] = forceString(record.value('OCATD'))
        # Код ОКАТО территории страхования по ОМС (по справочнику фонда)
        row['OKATO_OMS'] = forceString(record.value('insurerOKATO'))

        representativeInfo = self.getClientRepresentativeInfo(clientId)

        if representativeInfo:
            #Фамилия (представителя) пациента
            row['FAMP'] = representativeInfo.get('lastName')
            #Имя  (представителя) пациента
            row['IMP'] = representativeInfo.get('firstName')
            #Отчество родителя (представителя) пациента
            row['OTP'] = representativeInfo.get('patrName')
            #Дата рождения (представителя) пациента
            row['DRP'] = pyDate(representativeInfo.get('birthDate'))
            #Пол (представителя) пациента
            row['WP'] = formatSex(representativeInfo.get('sex')).upper()

        docType = forceInt(record.value('documentRegionalCode'))
        row['C_DOC'] = docType
        row['S_DOC'] = formatDocumentSerial(forceString(record.value(
            'documentSerial')), docType)
        row['N_DOC'] = forceString(record.value('documentNumber'))
        row['NOVOR'] = '0' # Признак новорожденного
        specState = ''
        multipleBirth = self.getActionPropertyText(
            params['eventId'], self.actionTypeMultipleBirth, u'Признак') != ''

        if multipleBirth:
            specState += '1'

        if not forceString(record.value('patrName')):
            specState += '2'

        row['Q_G'] = specState
        row['MSE'] = 0
        row['DOCDATE'] = pyDate(forceDate(record.value('DOCDATE')))
        row['DOCORG'] = forceString(record.value('DOCORG'))[:250]
        row.store()

# ******************************************************************************

    def _exportCons(self, dbf, _, params): #Задача №0010463:"ТФОМС Мурманск. Изменения по Приказу ФФОМС №285"
        u'Пишет Сведения о проведении консилиума'
        row = dbf.newRecord()
        row['CARD'] = params['eventId']
        onkRecord = params['onkologyInfo'].get(params['eventId'])
        if onkRecord:
            row['PR_CONS'] = 0
            row['DT_CONS'] = ''
        row.store()


# ******************************************************************************

    def _exportNapr(self, dbf, _, params):
        u'Пишет направления'
        row = dbf.newRecord()
        row['CARD'] = params['eventId']
        onkRecord = params['onkologyInfo'].get(params['eventId'])

        if onkRecord:
            row['NAPR_DATE'] = pyDate(forceDate(onkRecord.value('eventSetDate')))
            row['NAPR_MO'] = params['lpuCode']
            action = CAction.getActionById(forceRef(onkRecord.value(
                'directionActionId')))
            flatCode = action.getType().flatCode if action else None
            val = 0

            if (flatCode == 'ConsultationDirection' and
                    action.hasProperty[u'Профиль'] and
                    action[u'Профиль'].usishCode == 43):
                val = 1
            elif flatCode == 'inspectionDirection':
                val = (2 if action.hasProperty(u'Вид направления') and
                       action[u'Вид направления'] == u'на биопсию' else 3)

            row['NAPR_V'] = 4

            if (val == 3 and action.hasProperty(u'Вид направления') and
                    mapMetIssl.has_key(action[u'Вид направления'])):
                row['MET_ISSL'] = mapMetIssl.get(action[u'Вид направления'])

            if row['MET_ISSL']:
                prevAction = CAction.getActionById(
                    forceRef(action.getRecord().value('prevAction_id')))

                if prevAction:
                    serviceId = prevAction.getType().nomenclativeServiceId
                    row['NAPR_USL'] = self.getServiceCode(serviceId)

        row.store()

# ******************************************************************************

    def _exportOnkUsl(self, dbf, record, params):
        u'Пишет сведения об услуге при лечении онкологического заболевания'
        row = dbf.newRecord()
        row['CARD'] = params['eventId']
        row['IDSERV'] = forceString(params['__serviceNumber'])
        onkRecord = params['onkologyInfo'].get(params['eventId'])

        if onkRecord:
            action = CAction.getActionById(forceRef(record.value('controlListOnkoActionId')))
            if action:
                row['USL_TIP'] = action['ID_TLECH'].getValue() % 10

                if row['USL_TIP'] == 1:
                    row['HIR_TIP'] = action['ID_THIR'].getValue()
                else:
                    row['LUCH_TIP'] = action['ID_TLUCH'].getValue()

                row['LEK_TIP_L'] = action['ID_TLEK_L'].getValue()
                row['LEK_TIP_V'] = action['ID_TLEK_V'].getValue()
            else:
                row['USL_TIP'] = 6
                row['HIR_TIP'] = 0
                row['LUCH_TIP'] = 0
                row['LEK_TIP_L'] = 0
                row['LEK_TIP_V'] = 0
        row.store()

# ******************************************************************************

    def isValidActionTypeId(self, _id):
        u"""Проверка идентификатора типа действия на правильность"""
        result = self.validActionTypeCache.get(_id, -1)
        if result != -1:
            return result

        parentId = forceRef(self.db.translate(
            'ActionType', 'id', _id, 'group_id'))

        if parentId:
            if _id == parentId:
                QtGui.QMessageBox.critical (self.parent,
                    u'Ошибка в логической структуре данных',
                    u'Элемент id={id}, group_id={groupId} является сам себе группой'.format(id=_id,  groupId=parentId),
                    QtGui.QMessageBox.Close)
            elif parentId in self._nestedActionTypeSet:
                  QtGui.QMessageBox.critical (self.parent,
                u'Ошибка в логической структуре данных',
                u'Элемент id={id}: group_id={groupId} обнаружен в списке родительских групп "{groupList}"'.format(
                    id=_id, groupId=parentId, groupList=u'(' + '-> '.join([str(et) for et in self._nestedActionTypeSet])+ ')'),
                QtGui.QMessageBox.Close)
            else:
                self._nestedActionTypeSet.add(parentId)
                result = self.isValidActionTypeId(parentId)
                self._nestedActionTypeSet.remove(parentId)
                self.validActionTypeCache[_id] = result
                return result

        self.validActionTypeCache[_id] = False
        return False


    def _diagnosisCheck(self):
        u"""Проверка на предмет наличия у одного пациента одинаковых
        МКБ диапазона А00-Т98 в разных событиях, при условии что rbService.note
        содержит одно из чисел 301, 302, 401"""

        stmt = u"""SELECT clientId, MKB, eventList
            FROM (SELECT clientId,
                MKB,
                GROUP_CONCAT(DISTINCT eventList) AS eventList,
                SUM(noteCount) AS noteCount,
                sUM(dupCount) AS dupCount
                FROM (SELECT
                    SUBSTR(Diagnosis.MKB, 1, 3) AS MKB,
                    COUNT(DISTINCT Account_Item.event_id) AS dupCount,
                    GROUP_CONCAT(DISTINCT
                        CONCAT(Account_Item.event_id, '|', Event.execPerson_id)) AS eventList,
                    Event.client_id AS clientId,
                    SUM(IF(TRIM(rbService.note) IN (301, 302, 401),1,0)) AS noteCount
                FROM Account_Item
                LEFT JOIN `Event` ON `Event`.id = Account_Item.event_id
                LEFT JOIN rbService ON Account_Item.service_id = rbService.id
                LEFT JOIN Diagnostic ON ( Diagnostic.event_id = Account_Item.event_id
                     AND Diagnostic.diagnosisType_id IN (
                        SELECT id
                        FROM rbDiagnosisType
                        WHERE code IN ('1', '2'))
                     AND Diagnostic.person_id = Event.execPerson_id
                     AND Diagnostic.deleted = 0)
                LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
                LEFT JOIN rbPayRefuseType ON Account_Item.refuseType_id = rbPayRefuseType.id
                WHERE Account_Item.reexposeItem_id IS NULL
                     AND (Account_Item.date IS NULL
                        OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
                     AND %s
                     AND Diagnosis.MKB BETWEEN 'A00' AND 'T89'
                 GROUP BY clientId, MKB
            ) AS A
            GROUP BY clientId, MKB ) AS B
            WHERE B.dupCount > 1 AND B.noteCount > 1""" % (
                self.tableAccountItem['id'].inlist(self.idList))

        query = self.db.query(stmt)
        result = {}

        while query.next():
            record = query.record()

            if record:
                # через sql получить имя исполнителя события
                # не получается - битая кодировка
                eventInfoList = forceString(
                    record.value('eventList')).split(',')
                eventList = []

                for eventInfo in eventInfoList:
                    info = eventInfo.split('|')
                    eventList.append(u'%s (%s)'% (
                        info[0], self.getPersonShortName(forceRef(info[1]))))

                eventList = u','.join(str_ for str_ in eventList)
                mkb = forceString(record.value('MKB'))
                clientId = forceRef(record.value('clientId'))
                result[clientId] = (eventList, mkb)

        return result


    def getPersonShortName(self, personId):
        u"""Кэшированная версия getPersonShortName"""

        result = self._personShortNameCache.get(personId, -1)

        if result == -1:
            result = getPersonShortName(personId)
            self._personShortNameCache[personId] = result

        return result


    def getClientRepresentativeInfo(self, clientId):
        return self._representativeInfo.get(clientId)


    def _getRepresentativeInfo(self):
        selectClients = """SELECT DISTINCT Event.client_id FROM Account_Item
            LEFT JOIN Event ON Account_Item.event_id = Event.id
            LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
            WHERE Account_Item.reexposeItem_id IS NULL
              AND (Account_Item.date IS NULL OR
                   (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
            AND {idList}""".format(
                idList=self.tableAccountItem['id'].inlist(self.idList))

        stmt = """SELECT Client.id,
            Client.firstName,
            Client.lastName,
            Client.patrName,
            Client.sex,
            Client.birthDate,
            Client.birthPlace,
            ClientDocument.number,
            ClientDocument.serial,
            Client.SNILS,
            rbDocumentType.code AS documentTypeCode,
            rbDocumentType.regionalCode AS documentTypeRegionalCode,
            rbDocumentType.federalCode AS documentTypeFederalCode,
            T.regionalRelationTypeCode AS regionalRelationTypeCode
        FROM
    (SELECT rbRelationType.code, ClientRelation.relative_id AS client_id, rbRelationType.regionalReverseCode AS regionalRelationTypeCode
    FROM ClientRelation
    LEFT JOIN rbRelationType ON ClientRelation.relativeType_id = rbRelationType.id
    WHERE ClientRelation.deleted = 0
      AND ClientRelation.relative_id IN ({clientList})
      AND rbRelationType.isDirectRepresentative
    UNION
    SELECT rbRelationType.code, ClientRelation.client_id, rbRelationType.regionalCode AS regionalRelationTypeCode
    FROM ClientRelation
    LEFT JOIN rbRelationType ON ClientRelation.relativeType_id=rbRelationType.id
    WHERE ClientRelation.deleted = 0
      AND ClientRelation.client_id IN ({clientList})
      AND rbRelationType.isBackwardRepresentative
    ) AS T
    LEFT JOIN Client ON T.client_id = Client.id
    LEFT JOIN ClientDocument ON ClientDocument.client_id = Client.id AND
        ClientDocument.id = (SELECT MAX(CD.id)
                        FROM   ClientDocument AS CD
                        LEFT JOIN rbDocumentType AS rbDT ON rbDT.id = CD.documentType_id
                        LEFT JOIN rbDocumentTypeGroup AS rbDTG ON rbDTG.id = rbDT.group_id
                        WHERE  rbDTG.code = '1' AND CD.client_id = Client.id AND CD.deleted=0)
    LEFT JOIN rbDocumentType ON rbDocumentType.id = ClientDocument.documentType_id
    ORDER BY Client.id, T.code""".format(clientList=selectClients)

        query = self.db.query(stmt)
        lastId = None

        while query.next():
            record = query.record()
            _id = forceRef(record.value('id'))
            result = {}
            result['firstName'] = forceString(record.value('firstName'))
            result['lastName'] = forceString(record.value('lastName'))
            result['patrName'] = forceString(record.value('patrName'))
            result['serial'] = forceString(record.value('serial'))
            result['number'] = forceString(record.value('number'))
            result['sex'] = forceInt(record.value('sex'))
            result['birthDate'] = forceDate(record.value('birthDate'))
            result['birthPlace'] = forceString(record.value('birthPlace'))
            result['documentTypeCode'] = forceString(record.value('documentTypeCode'))
            result['documentTypeRegionalCode'] = forceInt(record.value('documentTypeRegionalCode'))
            result['documentTypeFederalCode'] = forceString(record.value('documentTypeFederalCode'))
            result['regionalRelationTypeCode'] = forceString(record.value('regionalRelationTypeCode'))
            result['SNILS'] = forceString(record.value('SNILS'))

            if _id != lastId:
                if lastId:
                    yield lastId, result

                lastId = _id

        if lastId:
            yield lastId, result

# ******************************************************************************

class CExportPage2(CAbstractExportPage2):
    u"""Вторая страница мастера экспорта"""

    def __init__(self, parent):
        self.prefix = 'R51OMS'
        CAbstractExportPage2.__init__(self, parent, self.prefix)


    def saveExportResults(self):
        exportType = self._parent.page1.exportType
        files = ('ALIENS.DBF', 'SERVICE.DBF', 'ADD_INF.DBF', 'ADDSERV.DBF',
                 'DIRECT.DBF', 'DS2_N.DBF', 'ONK_SL.DBF', 'ONK_USL.DBF',
                 'NAPR.DBF', 'B_DIAG.DBF', 'B_PROT.DBF', 'LEK_PR.DBF',
                 'CONS.DBF')

        if exportType >= CExportPage1.exportType2020:
            files += ('SERV_TMT.DBF', )

        return self.moveFiles(files)


if __name__ == '__main__':
    #pylint: disable=wrong-import-position,ungrouped-imports
    from Exchange.Utils import testAccountExport
    #pylint: enable=wrong-import-position,ungrouped-imports
    testAccountExport(exportR51OMS, u'17-1217', '75_38_s11.ini',
                      [4509756,4509754])
