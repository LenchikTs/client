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

u"""Экспорт реестра скорой медицинской помощи. Мурманск"""

import os.path

from PyQt4 import QtGui
from PyQt4.QtCore import QDate

from library.dbfpy.dbf import Dbf

from library.Utils import (forceBool, forceInt, toVariant, forceString,
                           forceRef, forceDouble, pyDate, nameCase,
                           firstMonthDay, formatSex)
from Exchange.Export import (CExportHelperMixin, CAbstractExportWizard,
                             CAbstractExportPage1, CAbstractExportPage2)
from Exchange.ExportR51OMS import mapAcionStatusToNpl, getIdsp, forceDate

from Exchange.Ui_ExportR08NativePage1 import Ui_ExportPage1


def exportR51Emergency(widget, accountId, accountItemIdList, _=None):
    u"""Создает диалог экспорта реестра счета"""

    wizard = CExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.exec_()

# ******************************************************************************

class CExportWizard(CAbstractExportWizard):
    u"""Мастер экспорта СМП Мурманской области"""

    def __init__(self, parent=None):
        title = u'Мастер экспорта реестра услуг СМП для Мурманской области'
        CAbstractExportWizard.__init__(self, parent, title)
        self.page1 = CExportPage1(self)
        self.page2 = CExportPage2(self)

        self.addPage(self.page1)
        self.addPage(self.page2)


    def getTmpDir(self, _=None):
        return CAbstractExportWizard.getTmpDirEx(self, 'R51SMP')

# ******************************************************************************

class CExportPage1(CAbstractExportPage1, Ui_ExportPage1, CExportHelperMixin):
    u"""Первая страница мастера экспорта"""

    def __init__(self, parent):
        CAbstractExportPage1.__init__(self, parent)
        CExportHelperMixin.__init__(self)
        self.prefix = 'ExportR51SMP'

        for widget in (self.cmbRegistryType, self.lblRegistryType,
                       self.edtPacketNumber, self.lblPacketNumber):
            widget.setVisible(False)

        prefs = QtGui.qApp.preferences.appPrefs
        self.ignoreErrors = forceBool(prefs.get(
            '%sIgnoreErrors' % self.prefix, False))
        self.chkVerboseLog.setChecked(forceBool(prefs.get(
            '%sVerboseLog' % self.prefix, False)))
        self.chkIgnoreErrors.setChecked(self.ignoreErrors)

        self.actionTypeMultipleBirth = None
        self.exportedActionsList = None


    def validatePage(self):
        prefs = QtGui.qApp.preferences.appPrefs
        prefs['%sIgnoreErrors' % self.prefix] = toVariant(
            self.chkIgnoreErrors.isChecked())
        prefs['%sVerboseLog' % self.prefix] = toVariant(
            self.chkVerboseLog.isChecked())
        return CAbstractExportPage1.validatePage(self)


    def setExportMode(self, flag):
        self.btnCancel.setEnabled(flag)
        self.btnExport.setEnabled(not flag)
        self.chkIgnoreErrors.setEnabled(not flag)
        self.chkVerboseLog.setEnabled(not flag)
        self.btnExport.setEnabled(not flag)

# ******************************************************************************

    def exportInt(self):
        self.ignoreErrors = self.chkIgnoreErrors.isChecked()
        params = {}

        lpuId = QtGui.qApp.currentOrgId()
        params['lpuCode'] = forceString(self.db.translate(
            'Organisation', 'id', lpuId, 'infisCode'))
        self.log(u'ЛПУ:  код инфис: "%s".' % params['lpuCode'])
        self.exportedActionsList = []

        if not params['lpuCode']:
            self.logError(u'Для текущего ЛПУ не задан код инфис')
            if not self.ignoreErrors:
                return

        self.actionTypeMultipleBirth = forceRef(self.db.translate(
            'ActionType', 'flatCode', 'MultipleBirth', 'id'))

        if not self.actionTypeMultipleBirth:
            self.logError(u'Не найден тип действия "Многоплодные роды" '
                          u'(плоский код: "MultipleBirth")')
            if not self.ignoreErrors:
                return

        if self.idList:
            params.update(self.accountInfo())
            params['payerCode'] = forceString(self.db.translate(
                'Organisation', 'id', params['payerId'], 'infisCode'))
            params['clientCount'] = self.clientCount()

        self.setProcessParams(params)
        CAbstractExportPage1.exportInt(self)


    def clientCount(self):
        u"""Подсчет количества уникальных пациентов в реестре счета"""
        stmt = """SELECT COUNT(DISTINCT Event.client_id)
        FROM Account_Item
        LEFT JOIN Event ON Event.id = Account_Item.event_id
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        WHERE Event.client_id IS NOT NULL AND
            Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s
        """ % self.tableAccountItem['id'].inlist(self.idList)

        query = self.db.query(stmt)
        result = 0

        if query and query.first():
            record = query.record()

            if record:
                result = forceInt(record.value(0))

        return result


    def createDbf(self):
        return (self._createSumExtrDbf(), self._createVisitExtrDbf(),
                self._createAddInfDbf())


    def _createSumExtrDbf(self):
        u""" Создает структуру dbf для файла типа SUMEXTR.DBF"""

        dbfName = os.path.join(self.getTmpDir(), 'SUMEXTR.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('LPU', 'C', 3), # Код МО
            ('INS', 'C', 2), # Код СМО
            ('SUB_HOSP', 'C', 3),
            ('TOWN_HOSP', 'C', 3),
            ('ACT', 'C', 10), # Номер реестра, представляемого в фонд
            ('DATE_LOW', 'D'), # Отчетный месяц
            ('KOL', 'N', 6), # Количество лиц, застрахованных в данной СМО
            ('STOIM_S', 'N', 10, 2), # Сумма по базовой программе гос. гарантий
        )
        return dbf


    def _createVisitExtrDbf(self):
        u"""Создает структуру dbf для файла типа VISIT_EXTR.DBF"""

        dbfName = os.path.join(self.getTmpDir(), 'VISIT_EXTR.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('LPU', 'C', 3), # Код МО
            ('SUB_HOSP', 'C', 3),
            ('TOWN_HOSP', 'C', 3),
            ('INS', 'C', 2), # Код СМО
            ('ACT', 'C', 10), # Номер реестра, представляемого в фонд
            ('DATE_LOW', 'D'), # Отчетный месяц
            ('DATE_UP', 'D'), #
            ('FAM', 'C', 40), #
            ('IM', 'C', 40), #
            ('OTC', 'C', 40), #
            ('BIRTHDAY', 'D'), #
            ('SEX', 'C', 1), #
            ('TAUN', 'C', 3), #
            ('SERPOL', 'C', 10), #
            ('NMBPOL', 'C', 20), #
            ('TPOLIS', 'N', 1), #
            ('SER_PASP', 'C', 8), #
            ('NUM_PASP', 'C', 8), #
            ('TYP_DOC', 'N', 2), #
            ('SERV_DATE', 'D'), #
            ('DIAG', 'C', 6), #
            ('PROF_BRIG', 'C', 3), #
            ('CARD', 'C', 10), #
            ('STOIM_S', 'N', 10, 2), #
            ('RSLT', 'N', 3), #
            ('ISHOD', 'N', 3), #
            ('FOR_POM', 'N', 1),
            ('VIDPOM', 'N', 4),
            ('PROFIL', 'N', 3),
            ('PRVS', 'N', 4),
            ('DOP_PR', 'N', 1),
            ('VID_FIN', 'N', 1),
            ('SERV_TIME', 'C', 5),
            ('DS_ONK', 'N', 1),
            ('NPL', 'N', 1), #Неполный объём
            ('IDSP', 'N', 2),  #Код способа оплаты медицинской помощи
            ('CNASP_V', 'C', 3), #Код населенного пункта, куда выезжала
                                 # бригада СМП
            ('LPU_DOST', 'C', 3), #Код МО, в которую доставлен пациент
            ('TOWN_DOST', 'C', 3), #Код населенного пункта структурного
            # подразделения МО, в которую доставлен пациент
            ('LPU_PEREV', 'C', 3), #Код МО, из которой осуществлена
            # перевозка пациента
            ('SUB_PEREV', 'C', 3), #Код структурного подразделения МО, из
            # которой осуществлена перевозка пациента
            ('TOWN_PEREV', 'C', 3), # Код населенного пункта структурного
            # подразделения МО, из которой осуществлена перевозка пациента
            ('DOCDATE', 'D'), #
            ('DOCORG', 'C', 250), #
            ('mpcod', 'C', 8), #
            ('addr_code', 'C', 16), #
            ('DS_PZ', 'C', 6), #
        )

        return dbf


    def _createAddInfDbf(self):
        u"""Создает структуру dbf для файла типа ADD_INF.DBF"""

        dbfName = os.path.join(self.getTmpDir(), 'ADD_INF.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('CARD', 'C', 10), # Номер истории болезни
            ('MR', 'C', 100), # Место рождения пациента или представителя
            ('OKATOG', 'C', 11), # Код места жительства по ОКАТО
            ('OKATOP', 'C', 11), # Код места пребывания по ОКАТО
            ('OKATO_OMS', 'C', 5), # Код ОКАТО территории страхования по ОМС
            ('FAMP', 'C', 40),   #Фамилия (представителя) пациента
            ('IMP', 'C', 40),   #Имя  (представителя) пациента
            ('OTP', 'C', 40),   #Отчество родителя (представителя) пациента
            ('DRP', 'D'),   #Дата рождения (представителя) пациента
            ('WP', 'C', 1),   #Пол  (представителя) пациента
            ('C_DOC', 'N', 2),   #Код типа документа, удостоверяющего личность
            ('S_DOC', 'C', 9),   #Серия документа, удостоверяющего личность
            ('N_DOC', 'C', 8),   #Номер документа, удостоверяющего личность
            ('NOVOR', 'C', 9),   #Признак новорожденного
            ('Q_G', 'C', 7),   #Признак «Особый случай»
            ('MSE', 'N', 1), # Направление на МСЭ
            ('DOCDATE', 'D'), #
            ('DOCORG', 'C', 250), #
        )

        return dbf


    def createQuery(self):
        stmt = u"""SELECT Account_Item.event_id AS eventId,
            Account_Item.`sum`,
            Event.execDate AS endDate,
            Event.client_id AS clientId,
            EventResult.regionalCode AS eventResultRegionalCode,
            IF(rbDiagnosticResult.regionalCode IS NULL,
                EventResult.regionalCode,
                    rbDiagnosticResult.regionalCode) AS resultRegionalCode,
            ClientDocument.serial AS documentSerial,
            ClientDocument.number AS documentNumber,
            rbDocumentType.regionalCode AS documentRegionalCode,
            ClientDocument.date AS DOCDATE,
            ClientDocument.origin AS DOCORG,
            Client.lastName AS lastName,
            Client.firstName AS firstName,
            Client.patrName AS patrName,
            Client.birthDate AS birthDate,
            Client.birthPlace,
            Client.sex AS sex,
            ClientPolicy.serial AS policySerial,
            ClientPolicy.number AS policyNumber,
            age(Client.birthDate, Event.execDate) as clientAge,
            rbPolicyKind.regionalCode AS policyKind,
            Diagnosis.MKB AS MKB,
            (SELECT code FROM rbDiseasePhases DP 
             WHERE DP.id = Diagnostic.phase_id) AS phaseCode,
            RegKLADR.OCATD AS regOKATO,
            LocKLADR.OCATD AS locOKATO,
            Insurer.area AS insurerArea,
            Insurer.OKATO AS insurerOKATO,
            EmergencyBrigade.codeRegional AS brigadeCode,
            EmergencyCall.numberCardCall,
            rbMedicalAidKind.regionalCode AS medicalAidKindRegionalCode,
            OrgStructure.infisCode AS orgStructInfisCode,
            OrgStructure.tfomsCode AS orgStructTfomsCode,
            rbSpeciality.federalCode AS specialityFederalCode,
            Action.status AS actionStatus,
            Action.endDate AS actionEndDate,
            EmergencyKLADR.infis AS emergencyTownInfis,
            rbMedicalAidUnit.regionalCode AS medicalAidUnitCode,
            NOT ISNULL(CurrentOrgAttach.id) AS isAttached,
            rbScene.name LIKE "%%на дому%%" AS isHomeVisit,
            TIME_FORMAT(EmergencyCall.arrivalDate, '%%H:%%i') AS servTime,
            EXISTS(SELECT D.id FROM Diagnostic D
                LEFT JOIN Diagnosis DS ON DS.id = D.diagnosis_id
                WHERE D.event_id = Account_Item.event_id
                  AND D.phase_id = (SELECT id FROM rbDiseasePhases WHERE code = '10')
                  AND D.deleted = 0 AND DS.deleted = 0
                  AND (DS.MKB LIKE 'C%%' OR DS.MKB LIKE 'Z03.1' OR
                       LEFT(Diagnosis.MKB, 3) BETWEEN 'D00' AND 'D09')) AS cancerSuspicion,
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
             WHERE OSI.master_id = OrgStructure.id
                AND OSI.deleted = 0
                AND OSI.system_id = (
                    SELECT MAX(id) FROM rbAccountingSystem
                    WHERE rbAccountingSystem.code = 'addr_code')
            ) AS orgStructAddrCode
        FROM Account_Item
        LEFT JOIN Event  ON Event.id  = Account_Item.event_id
        LEFT JOIN Client ON Client.id = Event.client_id
        LEFT JOIN ClientPolicy ON ClientPolicy.client_id = Client.id AND
                  ClientPolicy.id = (SELECT MAX(CP.id)
                                     FROM   ClientPolicy AS CP
                                     LEFT JOIN rbPolicyType AS CPT ON CPT.id = CP.policyType_id
                                     WHERE  CP.client_id = Client.id AND CP.deleted=0 AND CPT.code IN ('1','2'))
        LEFT JOIN rbPolicyKind ON rbPolicyKind.id = ClientPolicy.policyKind_id
        LEFT JOIN Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
        LEFT JOIN ClientDocument ON ClientDocument.client_id = Client.id AND
                  ClientDocument.id = (SELECT MAX(CD.id)
                                     FROM   ClientDocument AS CD
                                     LEFT JOIN rbDocumentType AS rbDT ON rbDT.id = CD.documentType_id
                                     LEFT JOIN rbDocumentTypeGroup AS rbDTG ON rbDTG.id = rbDT.group_id
                                     WHERE  rbDTG.code = '1' AND CD.client_id = Client.id AND CD.deleted=0)
        LEFT JOIN rbDocumentType ON rbDocumentType.id = ClientDocument.documentType_id
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
        LEFT JOIN kladr.KLADR AS RegKLADR ON RegKLADR.CODE = RegAddressHouse.KLADRCode
        LEFT JOIN Address   LocAddress ON LocAddress.id = ClientLocAddress.address_id
        LEFT JOIN AddressHouse LocAddressHouse ON LocAddressHouse.id = LocAddress.house_id
        LEFT JOIN kladr.KLADR AS LocKLADR ON LocKLADR.CODE = LocAddressHouse.KLADRCode
        LEFT JOIN Diagnostic ON ( Diagnostic.event_id = Account_Item.event_id
                                  AND Diagnostic.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code in ('1', '2'))
                                  AND Diagnostic.deleted = 0 )
        LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
        LEFT JOIN rbDiagnosticResult ON rbDiagnosticResult.id=Diagnostic.result_id
        LEFT JOIN rbResult AS EventResult ON EventResult.id=Event.result_id
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        LEFT JOIN EmergencyCall ON EmergencyCall.event_id = Account_Item.event_id
        LEFT JOIN EmergencyBrigade ON EmergencyBrigade.id = EmergencyCall.brigade_id
        LEFT JOIN Person ON Person.id = Event.execPerson_id
        LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
        LEFT JOIN EventType ON EventType.id = Event.eventType_id
        LEFT JOIN rbMedicalAidKind ON EventType.medicalAidKind_id = rbMedicalAidKind.id
        LEFT JOIN OrgStructure ON OrgStructure.id = Person.orgStructure_id
        LEFT JOIN Action ON Action.id = Account_Item.action_id
        LEFT JOIN Address AS EmergencyAddress ON EmergencyAddress.id = EmergencyCall.address_id
        LEFT JOIN AddressHouse AS EmergencyAddressHouse ON EmergencyAddressHouse.id = EmergencyAddress.house_id
        LEFT JOIN kladr.KLADR AS EmergencyKLADR ON EmergencyKLADR.CODE = EmergencyAddressHouse.KLADRCode
        LEFT JOIN Visit ON Visit.id  = Account_Item.visit_id
        LEFT JOIN rbScene ON rbScene.id = Visit.scene_id
        LEFT JOIN rbMedicalAidUnit ON rbMedicalAidUnit.id = Account_Item.unit_id
        LEFT JOIN ClientAttach AS CurrentOrgAttach ON CurrentOrgAttach.id = (
            SELECT MAX(COA.id)
            FROM ClientAttach COA
            WHERE COA.LPU_id = %d AND COA.client_id = Client.id
                AND (COA.begDate IS NULL OR COA.begDate <= Event.execDate)
                AND (COA.endDate IS NULL OR COA.endDate >= Event.execDate)
        )
        WHERE
            Account_Item.reexposeItem_id IS NULL
        AND (Account_Item.date IS NULL
             OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
            )
        AND %s""" % (QtGui.qApp.currentOrgId(),
                     self.tableAccountItem['id'].inlist(self.idList))

        return self.db.query(stmt)

# ******************************************************************************

    def process(self, dbf, record, params):
        insurerArea = forceString(record.value('insurerArea'))

        localParams = {
            'endDate': forceDate(record.value('endDate')),
            'birthDate': forceDate(record.value('birthDate')),
            'clientId': forceRef(record.value('clientId')),
            'eventId': forceRef(record.value('eventId')),
            'firstName': nameCase(forceString(record.value('firstName'))),
            'patrName': nameCase(forceString(record.value('patrName'))),
            'isAlien': insurerArea[:2] != QtGui.qApp.defaultKLADR()[:2],
            'policySerial': forceString(record.value('policySerial'))[:10],
            'policyNumber': forceString(record.value('policyNumber'))[:20],
            'documentSerial': forceString(record.value('documentSerial'))[:8],
            'documentNumber': forceString(record.value('documentNumber'))[:8],
            'documentRegionalCode': forceInt(record.value(
                'documentRegionalCode')),
            'defaultKladrInfis': forceString(self.db.translate(
                'kladr.KLADR', 'CODE', QtGui.qApp.defaultKLADR(), 'infis'))
        }

        (sumExtrDbf, visitExtrDbf, addInfDbf) = dbf
        localParams.update(params)

        if not params.get('isSummaryWritten', False):
            self._processSumExtr(sumExtrDbf, record, localParams)
            params['isSummaryWritten'] = True

        self._processVisitExtr(visitExtrDbf, record, localParams)

        if localParams['isAlien']:
            self._processAddInf(addInfDbf, record, localParams)

# ******************************************************************************

    def _processVisitExtr(self, dbf, record, params):
        u"""Запись информации в VISIT_EXTR.DBF"""
        endDate = params['endDate']
        exposeDate = params['exposeDate']
        row = dbf.newRecord()
        # Код МО
        row['LPU'] = params['lpuCode']
        # Код СМО
        row['INS'] = params['payerCode']
        # Номер реестра, представляемого в фонд
        row['ACT'] = params['accNumber']
        # Отчетный месяц
        row['DATE_LOW'] = pyDate(firstMonthDay(endDate))
        # Конечная дата интервала дат оказания услуг
        row['DATE_UP'] = pyDate(exposeDate if exposeDate else
                                QDate.currentDate())
        #Фамилия
        row['FAM'] = nameCase(forceString(record.value('lastName')))
        #Имя
        row['IM'] = params['firstName']
        #Отчество
        row['OTC'] = params['patrName']
        #Дата рождения пациента
        row['BIRTHDAY'] = pyDate(params['birthDate'])
        #Пол пациента («Ж» –жен, «М» – муж)
        row['SEX'] = formatSex(forceInt(record.value('sex')))

        locKLADRCode = forceString(record.value('locKLADRCode'))

        #Код населенного пункта проживания пациента по справочнику фонда
        if not locKLADRCode:
            locKLADRCode = forceString(record.value('regKLADRCode'))

        townCode = forceString(self.db.translate(
            'kladr.KLADR', 'CODE', locKLADRCode, 'infis'))

        if not townCode:
            self.log(u'Не задан инфис код для города "%s", clientId=%d' % (
                locKLADRCode, params['clientId']))

        row['TAUN'] = townCode[:3]
        #Серия полиса
        row['SERPOL'] = params['policySerial']
        #Номер полиса
        row['NMBPOL'] = params['policyNumber']
        #Тип полиса
        row['TPOLIS'] = forceInt(record.value('policyKind'))
        #Серия документа, удостоверяющего личность

        if params['documentRegionalCode'] == 3:
            params['documentSerial'] = params[
                'documentSerial'].strip().replace(' ', '-')

        row['SER_PASP'] = params['documentSerial']
        #Номер документа, удостоверяющего личность
        row['NUM_PASP'] = params['documentNumber']
        #Тип документа, удостоверяющего личность (приложение «Типы документов»)
        row['TYP_DOC'] = params['documentRegionalCode']
        # Дата оказания услуги
        row['SERV_DATE'] = pyDate(endDate)
        # Диагноз
        row['DIAG'] = forceString(record.value('MKB'))
        # Виды бригад скорой медицинской помощи
        row['PROF_BRIG'] = forceString(record.value('brigadeCode'))
        # Номер карты вызова скорой медицинской помощи
        row['CARD'] = forceString(record.value('numberCardCall'))
        # Для пациентов, застрахованных на территории других субъектов РФ
        row['STOIM_S'] = forceDouble(record.value('sum'))
        # Результат обращения/ госпитализации
        eventResult = forceInt(record.value('eventResultRegionalCode')) % 1000
        row['RSLT'] = eventResult
        # Исход заболевания
        row['ISHOD'] = forceInt(record.value('resultRegionalCode')) % 1000
        row['SUB_HOSP'] = forceString(record.value('orgStructInfisCode'))
        row['TOWN_HOSP'] = forceString(record.value('orgStructTfomsCode'))
        row['FOR_POM'] = 3 if row['DIAG'] in ('Z71.9', 'Z75.1') else 1
        row['VIDPOM'] = forceInt(record.value('medicalAidKindRegionalCode'))
        row['PROFIL'] = 84
        row['PRVS'] = forceInt(record.value('specialityFederalCode'))
        row['VID_FIN'] = 1
        row['NPL'] = mapAcionStatusToNpl.get(forceInt(
            record.value('actionStatus')), 0)
        if (row['NPL'] == 4 and
                forceDate(record.value('actionEndDate')) >= params['begDate']):
            row['NPL'] = 0

        row['CNASP_V'] = forceString(record.value('emergencyTownInfis'))[:3]

        if eventResult in (403, 402):
            row['LPU_DOST'] = params['lpuCode'][:3]
            row['TOWN_DOST'] = params['defaultKladrInfis'][:3]

        row['IDSP'] = getIdsp(forceInt(record.value('medicalAidUnitCode')),
                              forceBool(record.value('isAttached')),
                              forceBool(record.value('isHomeVisit')))
        row['SERV_TIME'] = forceString(record.value('servTime'))[:5]
        row['DS_ONK'] = forceInt(record.value('cancerSuspicion')) % 10
        row['DOCDATE'] = pyDate(forceDate(record.value('DOCDATE')))
        row['DOCORG'] = forceString(record.value('DOCORG'))[:250]
        row['mpcod'] = forceString(record.value('orgStructMpCod'))[:8]
        row['addr_code'] = forceString(record.value('orgStructAddrCode'))[:16]
        if forceInt(record.value('phaseCode')) == 10:
            row['DS_PZ'] = forceString(record.value('MKB'))
        row.store()

# ******************************************************************************

    def _processSumExtr(self, dbf, record, params):
        u"""Запись информации в SUMEXTR.DBF"""
        row = dbf.newRecord()
        # Код МО
        row['LPU'] = params['lpuCode']
        # Код СМО
        row['INS'] = params['payerCode']
        # Номер реестра, представляемого в фонд
        row['ACT'] = params['accNumber']
        # Отчетный месяц
        row['DATE_LOW'] = pyDate(firstMonthDay(params['endDate']))
        row['STOIM_S'] = params['accSum']
        row['KOL'] = params['clientCount']
        row['SUB_HOSP'] = forceString(record.value('orgStructInfisCode'))
        row['TOWN_HOSP'] = forceString(record.value('orgStructTfomsCode'))
        row.store()


# ******************************************************************************

    def _processAddInf(self, dbf, record, params):
        u"""Запись информации в ADD_INF.DBF"""
        row = dbf.newRecord()
        # Номер истории болезни
        row['CARD'] = forceString(record.value('numberCardCall'))
        # Место рождения пациента или представителя
        row['MR'] = forceString(record.value('birthPlace'))[:100]
        locOKATO = forceString(record.value('locOKATO'))
        regOKATO = forceString(record.value('regOKATO'))

        if not locOKATO:
            locOKATO = regOKATO

        # Код места жительства по ОКАТО
        row['OKATOG'] = regOKATO
        # Код места пребывания по ОКАТО
        row['OKATOP'] = locOKATO
        # Код ОКАТО территории страхования по ОМС (по справочнику фонда)
        row['OKATO_OMS'] = forceString(record.value('insurerOKATO'))
        representativeInfo = self.getClientRepresentativeInfo(
            params['clientId'])
        #Фамилия (представителя) пациента
        row['FAMP'] = representativeInfo.get('lastName', '')
        #Имя  (представителя) пациента
        row['IMP'] = representativeInfo.get('firstName', '')
        #Отчество родителя (представителя) пациента
        row['OTP'] = representativeInfo.get('patrName', '')
        #Дата рождения (представителя) пациента
        row['DRP'] = pyDate(representativeInfo.get('birthDate', QDate()))
        #Пол  (представителя) пациента
        if representativeInfo.has_key('sex'):
            row['WP'] = '1' if representativeInfo['sex'] == 1 else '0'
        #Код типа документа, удостоверяющего личность
        row['C_DOC'] = forceInt(representativeInfo.get(
            'documentTypeRegionalCode', params['documentRegionalCode'])) % 100
        #Серия документа, удостоверяющего личность
        row['S_DOC'] = representativeInfo.get(
            'serial', params['documentSerial'])
        #Номер документа, удостоверяющего личность
        row['N_DOC'] = representativeInfo.get('number',
                                              params['documentNumber'])

        age = forceInt(record.value('clientAge'))
        specialCase = []
        # Признак новорожденного
        row['NOVOR'] = '0' if age > 0 else  '%s%s0' % (
            forceString(record.value('sex'))[:1],
            params['birthDate'].toString('ddMMyy'))

        #Признак «Особый случай»
        multipleBirth = self.getActionPropertyText(
            params['eventId'], self.actionTypeMultipleBirth, u'Признак')
        #«1» -  медицинская помощь, оказанная новорожденному
        #при  многоплодных родах.
        if multipleBirth:
            specialCase.append('1')

        if (not forceString(params['patrName']) or
                not forceString(params['firstName'])):
            specialCase.append('2')

        row['Q_G'] = ''.join(specialCase)
        row['MSE'] = 0
        row['DOCDATE'] = pyDate(forceDate(record.value('DOCDATE')))
        row['DOCORG'] = forceString(record.value('DOCORG'))[:250]
        row.store()

# ******************************************************************************

class CExportPage2(CAbstractExportPage2):
    u"""Вторая страница мастера экспорта"""

    def __init__(self, parent):
        CAbstractExportPage2.__init__(self, parent, 'R51SMP')


    def saveExportResults(self):
        files = ('ADD_INF.DBF', 'SUMEXTR.DBF', 'VISIT_EXTR.DBF')
        return self.moveFiles(files)

# ******************************************************************************

if __name__ == '__main__':
    #pylint: disable=wrong-import-position,ungrouped-imports
    from Exchange.Utils import testAccountExport
    #pylint: enable=wrong-import-position,ungrouped-imports
    testAccountExport(exportR51Emergency, u'17_ОМС-57', 'art_msch118_0710.ini',
                      [3828352])
