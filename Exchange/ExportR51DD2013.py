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
u"""Экспорт реестра счета ДД 2013+ Мурманск"""

import os.path

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDate

from library.dbfpy.dbf import Dbf
from library.Utils import (forceBool, forceInt, toVariant, forceString,
                           forceRef, forceDouble, formatSNILS, formatSex,
                           pyDate, firstMonthDay, trim)
from Events.Action import CAction
from Exchange.Export import (CAbstractExportWizard, CAbstractExportPage1,
                             CAbstractExportPage2, CExportHelperMixin)
from Exchange.ExportR51OMS import (
    createDirectDbf, createDs2nDbf, createNaprDbf, mapAcionStatusToNpl,
    mapMetIssl, exportDs2n, getIdsp, getOnkologyInfo, forceDate,
    createServTmtDbf)

from Exchange.Ui_ExportR51DD2013Page1 import Ui_ExportPage1



def exportR51DD2013(widget, accountId, accountItemIdList, _=None):
    u"""Создает диалог экспорта реестра счета"""

    wizard = CExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.exec_()

# ******************************************************************************

mapEventTypeCodetoPMode = {3: 10, 4: 13, 7: 10}

def _processServiceExport2016(row, record, params):
    u"""Выгружает параметры для SERVICE.DBF, добавленные в формат 2016"""

    row['PROFIL'] = forceInt(record.value(
        'medicalAidProfileRegionalCode')) % 1000

    if not row['PROFIL']:
        row['PROFIL'] = forceInt(record.value(
            'serviceMedicalAidProfileRegionalCode')) % 1000

    row['PRVS'] = forceInt(record.value(
        'execSpecialityFederalCode')) % 10000

    orgStructInfisCode = forceString(record.value('execOrgInfisCode'))
    orgTfomsCode = forceString(record.value('execOrgTfomsCode'))
    orgInfisDepTypeCode = forceString(record.value('execOrgInfisDepTypeCode'))

    row['DIR_SUBLPU'] = orgStructInfisCode
    row['DIR_TOWN'] = orgTfomsCode
    row['DIRECT_LPU'] = orgInfisDepTypeCode

    if record.isNull('VID_FIN'):
        if trim(params['contractNote']):
            row['VID_FIN'] = forceInt(params['contractNote'])
    else:
        row['VID_FIN'] = forceInt(record.value('VID_FIN'))

    row['PURPOSE'] = forceString(record.value('serviceNote'))
    visitTypeCode = forceString(record.value('visitTypeCode'))
    attachBegDate = forceDate(record.value('attachBegDate'))
    reason = 0

    if visitTypeCode == '04':
        reason = 1
    elif visitTypeCode == '06':
        reason = 2
    elif params['begDate'] == attachBegDate:
        reason = 3

    row['REASON'] = reason
    row['P_MODE'] = mapEventTypeCodetoPMode.get(
        forceInt(record.value('eventTypeCode')), 0) % 100

    if not row['DIR_SPEC']:
        row['DIR_SPEC'] = forceInt(record.value(
            'execSpecialityFederalCode')) % 100000

    mesSpecificationLevel = forceInt(record.value('mesSpecificationLevel'))
    row['STOIM_S'] = (0 if mesSpecificationLevel == 2 else
                      forceDouble(record.value('price')))

    sceneCode = forceString(record.value('sceneCode'))

    if sceneCode == '2':
        row['PR_VISIT'] = 1

    row['SUB_HOSP'] = forceString(record.value('subHospital'))
    row['TOWN_HOSP'] = orgTfomsCode

    if row['SERV_DATE'] and row['SERV_DATE'].year == 2015:
        row['SPEC'] = forceString(record.value('specialityFederalCode'))

# ******************************************************************************

class CExportWizard(CAbstractExportWizard):
    u"""Мастер экспорта ДД для Мурманской области"""
    def __init__(self, parent=None):
        title = u'Мастер экспорта ДД для Мурманской области'
        CAbstractExportWizard.__init__(self, parent, title)
        self.page1 = CExportPage1(self)
        self.page2 = CExportPage2(self)

        self.addPage(self.page1)
        self.addPage(self.page2)


    def getTmpDir(self):
        return CAbstractExportWizard.getTmpDirEx(self, 'R51DD2013')

# ******************************************************************************

class CExportPage1(CAbstractExportPage1, Ui_ExportPage1,
                   CExportHelperMixin):
    u"""Первая страница мастера экспорта"""
    # Формат экспорта
    exportType2019 = 0
    exportType2020 = 1
    exportType2021 = 2
    mapEventOrderToForPom = {2: 1, 6: 2, 1: 3}

    def __init__(self, parent):
        CAbstractExportPage1.__init__(self, parent)
        CExportHelperMixin.__init__(self)

        prefs = QtGui.qApp.preferences.appPrefs
        self.chkVerboseLog.setChecked(
            forceBool(prefs.get('ExportR51DD2013VerboseLog', False)))
        self.cmbExportType.setCurrentIndex(
            forceInt(prefs.get('ExportR51DD2013ExportType', 0)))
        self.chkIgnoreErrors.setChecked(
            forceBool(prefs.get('ExportR51DD2013IgnoreErrors', False)))
        self.tableAccountItem = self.db.table('Account_Item')
        self.exportType = self.cmbExportType.currentIndex()
        self.exportedEvents = set()

        self._directionDateCache = {}


    def validatePage(self):
        prefs = QtGui.qApp.preferences.appPrefs
        prefs['ExportR51DD2013IgnoreErrors'] = toVariant(
            self.chkIgnoreErrors.isChecked())
        prefs['ExportR51DD2013VerboseLog'] = toVariant(
            self.chkVerboseLog.isChecked())
        prefs['ExportR51DD2013ExportType'] = toVariant(
            self.cmbExportType.currentIndex())
        return CAbstractExportPage1.validatePage(self)


    def setExportMode(self, flag):
        self.btnCancel.setEnabled(flag)
        self.btnExport.setEnabled(not flag)
        self.chkIgnoreErrors.setEnabled(not flag)
        self.chkVerboseLog.setEnabled(not flag)
        self.cmbExportType.setEnabled(not flag)


    def getDbfBaseName(self):
        u"""Возвращает базу имени DBF файла"""
        lpuCode = forceString(QtGui.qApp.db.translate(
            'Organisation', 'id', QtGui.qApp.currentOrgId(), 'infisCode'))
        info = self.accountInfo()
        accDate = info.get('accDate', QDate())
        return forceString(lpuCode + (accDate.toString('MMyy') if
                                      accDate else u'0000') + u'.DBF')

# ******************************************************************************

    def exportInt(self):
        ignoreErrors = self.chkIgnoreErrors.isChecked()
        self.exportType = self.cmbExportType.currentIndex()
        self.exportedEvents = set()

        params = {}

        params['lpuId'] = QtGui.qApp.currentOrgId()
        params['codeLPU'] = forceString(QtGui.qApp.db.translate(
            'Organisation', 'id', params['lpuId'], 'infisCode'))
        self.log(u'ЛПУ: код инфис: "%s".' % params['codeLPU'])

        if not params['codeLPU']:
            self.logError(u'Для текущего ЛПУ не задан код инфис')
            if not ignoreErrors:
                return

        params.update(self.accountInfo())
        params['exportedEvents'] = set()
        params['isExternalServiceExposed'] = forceBool(QtGui.qApp.db.translate(
            'Contract', 'id', params['contractId'], 'exposeExternalServices'))
        params['contractNote'] = forceString(QtGui.qApp.db.translate(
            'Contract', 'id', params['contractId'], 'note'))
        params['payerInfis'] = forceString(self.db.translate(
            'Organisation', 'id', params['payerId'], 'infisCode'))
        params['eventSum'] = self.getEventSum()
        params['directLpuField'] = 'setOrgStructCode'

        actionList, visitList = self._getVisitAndActionList()
        params['actionList'] = actionList
        params['visitList'] = visitList
        params['serviceNumber'] = 1
        accOrgStructId = params['accOrgStructureId']
        record = self.db.getRecord('OrgStructure', 'infisCode, tfomsCode',
                                   accOrgStructId)
        if record:
            params['orgStructureInfisCode'] = forceString(record.value(
                'infisCode'))
            params['orgStructureTfomsCode'] = forceString(record.value(
                'tfomsCode'))

        self.setProcessParams(params)

        CAbstractExportPage1.exportInt(self)


    def createDbf(self):
        result = (self._createAliensDbf(), self._createServiceDbf(),
                self._createAddInfDbf(), self._createDirectDbf(),
                self._createDs2nDbf(), self._createNaprDbf())

        if self.exportType >= self.exportType2020:
            result += (self._createServTmtDbf(), )
        else:
            result += (None, )

        return result


    def _createAliensDbf(self):
        u"""Создает структуру dbf для файла типа ALIENS"""

        dbfName = os.path.join(self.getTmpDir(), 'ALIENS.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('CODE_HOSP', 'C', 3), # Код ЛПУ пребывания по справочнику фонда
            ('CODE_COUNT', 'C', 10), # Номер реестра, представляемого в ТФОМС
            ('DATE_LOW', 'D', 8), # Отчетный месяц
            ('CARD', 'C', 10), # Номер статталона
            ('INS', 'C', 2), # Код СМО Код из справочника SMO
            ('SERPOL', 'C', 10), # Серия полиса
            ('NMBPOL', 'C', 20), # Номер полиса
            ('WORK', 'C', 1), # Статус пациента
            ('DATIN', 'D'), # Дата начала диспансеризации
            ('DATOUT', 'D'), # Дата окончания диспансеризации
            ('DIAG', 'C', 6), # Диагноз основной Код из справочника MKB
            ('DS1_PR', 'N', 1), # Код диагноза сопутствующего заболевания
            ('DS0', 'C', 6),  # Диагноз первичный
            ('FAM', 'C', 40), # Фамилия пациента
            ('IMM', 'C', 40), # Имя пациента
            ('OTC', 'C', 40), # Отчество пациента
            ('SER_PASP', 'C', 8), # Серия документа, удостоверяющего личность
            ('NUM_PASP', 'C', 8), # Номер документа, удостоверяющего личность
            ('TYP_DOC', 'N', 2), # Тип документа, удостоверяющего личность
            ('SS', 'C', 14), # Страховой номер индивидуального лицевого счета
            ('BIRTHDAY', 'D', 8), # Дата рождения пациента
            ('SEX', 'C', 1), # Пол пациента «М» или «Ж»
            ('TAUN', 'C', 3), # Код населенного пункта проживания
            ('MASTER', 'C', 3), # Код ЛПУ приписки
            ('STOIM_S', 'N', 10, 2), # Сумма по базовой программе гос. гарантий
                                     # Тип полиса:
                                     # 1 – старого образца,
                                     # 2 – временное свидетельство}
                                     # 3 – нового образца
            ('TPOLIS', 'N', 1),
            # признак законченного случая
            # «3» - 1-й этап диспансеризации взрослого населения
            # «4» - 2-й этап диспансеризации взрослого населения
            ('PRIZN_ZS', 'N', 1),
            ('RSLT', 'N', 3),  # Результат обращения/ госпитализации
            ('ISHOD', 'N', 3),  # Исход заболевания
            ('DET', 'N', 1),  # Признак детского профиля
            ('P_CODE', 'C', 14),  # Код врача, закрывшего талон
            ('FOR_POM', 'N', 1),#Форма оказания медицинской помощи
            ('VIDPOM', 'N', 4),#Вид медицинской помощи
            ('PROFIL', 'N', 3),#Профиль медицинской помощи
            ('PRVS', 'N', 4),#Специальность врача, закрывшего талон
            ('VID_FIN', 'N', 1),#Источник финансирования
            ('INV', 'N', 1),#Группа инвалидности
            ('PR_D_N', 'N', 1),#Признак диспансерного наблюдения
            ('VBR', 'N', 1),#Признак мобильной медицинской бригады
            ('PR_OS', 'N', 2), #Признак “Особый случай»
            ('IDSP', 'N', 2), #Код способа оплаты медицинской помощи
            ('DS2', 'C', 6), #Диагноз  сопутствующего заболевания
            ('DS2_PR', 'N', 1), #Установлен впервые (сопутствующий)
            ('DS_ONK', 'N', 1),
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
        u"""Создает структуру dbf для файла типа SERVICE"""

        serviceFieldSize = 15
        dbfName = os.path.join(self.getTmpDir(), 'SERVICE.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('CARD', 'C', 10),   # Номер статталона
            ('IDSERV', 'C', 36), # Номер записи в реестре услуг
        )

        dbf.addField(
            ('CODE_COUNT', 'C', 10),   # Номер реестра, представляемого в ТФОМС
            ('P_CODE', 'C', 14), # Личный код  мед. работника, оказавшего услугу
            ('SPEC', 'C', 3),  #Код специальности
            ('PROFIL', 'N', 3),#Профиль медицинской помощи
            #Специальность медработника, выполнившего услугу
            ('PRVS', 'N', 4),
            # Код услуги
            ('SERVICE', 'C', serviceFieldSize),
            ('UNITS', 'N', 3),# Кол-во услуг
            ('PR_VISIT', 'N', 1),
            ('SERV_DATE', 'D'),# Дата оказания услуги
            ('DS', 'C', 6),  # Диагноз
            ('DIRECT_LPU', 'C', 3), # Код ЛПУ, направившего пациента
            #Код структурного подразделения МО,
            # направившего пациента на консультацию (обследование)
            ('DIR_SUBLPU', 'C', (3 if self.exportType >= self.exportType2021
                                 else 2)),
            # Код населенного пункта структурного подразделения МО,
            # направившего пациента на консультацию (обследование)
            ('DIR_TOWN', 'C', 3),
            ('AIM', 'C', 2),   # Признак учета результатов  осмотров
            ('STOIM_S', 'N', 10, 2),#Сумма по базовой программе гос. гарантий
            # Код специальности медработника, направившего пациента
            ('DIR_SPEC', 'N', 4),
            ('VID_FIN', 'N', 1),#
            ('PURPOSE', 'C', 3),#
            ('REASON', 'N', 2),#
            ('P_MODE', 'N', 2),#
            ('SUB_HOSP', 'C', (3 if self.exportType >= self.exportType2021
                               else 2)),
            ('TOWN_HOSP', 'C', 3),
            ('NPL', 'N', 1),#Неполный объём
            ('SERV_METOD', 'C', (5 if self.exportType >= self.exportType2021
                               else 3)),#Код метода услуги
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
        u"""Создает структуру dbf для ADD_INF.DBF """

        dbfName = os.path.join(self.getTmpDir(), 'ADD_INF.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('CARD', 'C', 10),       #Номер истории болезни
            ('MR', 'C', 100),  # Место рождения пациента или представителя
            ('OKATOG', 'C', 11), # Код места жительства по ОКАТО
            ('OKATOP', 'C', 11), # Код места пребывания по ОКАТО
            ('OKATO_OMS', 'C', 5), # Код ОКАТО территории страхования по ОМС
            ('FAMP', 'C', 40), #Фамилия (представителя) пациента
            ('IMP', 'C', 40), #Имя  (представителя) пациента
            ('OTP', 'C', 40), #Отчество родителя (представителя) пациента
            ('DRP', 'D'), #Дата рождения (представителя) пациента
            ('WP', 'C', 1), #Пол (представителя) пациента
            ('C_DOC', 'N', 2), # Код типа документа, удостоверяющего личность
            ('S_DOC', 'C', 9), # Серия документа, удостоверяющего личность
            ('N_DOC', 'C', 8), # Номер документа, удостоверяющего личность
            ('NOVOR', 'C', 9), # Признак новорожденного
            ('Q_G', 'C', 7), # Признак «Особый случай» при регистрации обращения
            ('MSE', 'N', 1), # Направление на МСЭ
            ('DOCDATE', 'D'), #
            ('DOCORG', 'C', 250), #
        )
        return dbf


    def _createDirectDbf(self):
        """ Создает структуру dbf для DIRECT.DBF """
        return createDirectDbf(self.getTmpDir())


    def _createDs2nDbf(self):
        """ Создает структуру dbf для DS2_N.DBF """
        return createDs2nDbf(self.getTmpDir())


    def _createNaprDbf(self):
        """ Создает структуру dbf для NAPR.DBF """
        return createNaprDbf(self.getTmpDir(), exportType2019=True)

    def _createServTmtDbf(self):
        return createServTmtDbf(self.getTmpDir())


    def createQuery(self):
        stmt = u"""SELECT    Account_Item.event_id,
            Account_Item.visit_id AS visitId,
            Account_Item.action_id AS actionId,
            Event.client_id,
            Client.lastName,
            Client.firstName,
            Client.patrName,
            Client.birthDate,
            Client.sex,
            Client.SNILS,
            ClientPolicy.serial AS policySerial,
            ClientPolicy.number AS policyNumber,
            Insurer.infisCode   AS policyInsurer,
            rbPolicyKind.regionalCode   AS policyKind,
            ClientDocument.serial  AS documentSerial,
            ClientDocument.number  AS documentNumber,
            rbDocumentType.regionalCode AS documentRegionalCode,
            ClientDocument.date AS DOCDATE,
            ClientDocument.origin AS DOCORG,
            rbService.infis AS service,
            EventType.regionalCode AS eventTypeCode,
            Event.setDate   AS begDate,
            Event.execDate  AS endDate,
            Account_Item.price AS price,
            Account_Item.amount AS amount,
            Account_Item.`sum`  AS `sum`,
            AccDiagnosis.MKB AS accMKB,
            Diagnosis.MKB   AS MKB,
            rbDiseasePhases.code AS diseasePhaseCode,
            RegKLADR.infis AS placeCode,
            Visit.date AS visitDate,
            Action.endDate AS actionDate,
            Action.org_id AS actionOrgId,
            setOrgStruct.infisCode AS setOrgStructCode,
            Person.code AS personCode,
            Person.SNILS AS personRegionalCode,
            rbSpeciality.regionalCode AS specialityCode,
            rbSpeciality.federalCode AS specialityFederalCode,
            Employment.regionalCode AS clientStatus,
            rbVisitType.code AS visitTypeCode,
            EventResult.regionalCode AS eventResultCode,
            IF(rbDiagnosticResult.code IS NULL, EventResult.code, rbDiagnosticResult.code) AS resultCode,
            IF(rbDiagnosticResult.regionalCode IS NULL, EventResult.regionalCode, rbDiagnosticResult.regionalCode) AS resultRegionalCode,
            IF(Account_Item.visit_id IS NOT NULL, VisitSpeciality.regionalCode,
                IF(Account_Item.action_id IS NOT NULL,
                    IF(Action.person_id IS NOT NULL, ActionSpeciality.regionalCode,
                        ActionSetSpeciality.regionalCode), rbSpeciality.regionalCode)
            )  AS execSpecialityCode,
            IF(Account_Item.visit_id IS NOT NULL, VisitSpeciality.federalCode,
                IF(Account_Item.action_id IS NOT NULL,
                    IF(Action.person_id IS NOT NULL, ActionSpeciality.federalCode,
                        ActionSetSpeciality.federalCode), rbSpeciality.federalCode)
            )  AS execSpecialityFederalCode,
            IF(Account_Item.visit_id IS NOT NULL, VisitPerson.SNILS,
                IF(Account_Item.action_id IS NOT NULL,
                    IF(Action.person_id IS NOT NULL, ActionPerson.SNILS,
                        ActionSetPerson.SNILS), Person.SNILS)
            ) AS execPersonCode,
            age(Client.birthDate, Event.execDate) AS clientAge,
            Insurer.OKATO AS insurerOKATO,
            Client.birthPlace,
            RegRegionKLADR.OCATD,
            RelegateSpeciality.federalCode AS relegatePersonCode,
            RelegateOrg.infisCode AS relegateOrgCode,
            rbMesSpecification.code AS mesSpecificationCode,
            rbMesSpecification.id AS mesSpecificationId,
            rbMesSpecification.level AS mesSpecificationLevel,
            IF(work.title IS NOT NULL,
                work.title,
                ClientWork.freeInput) AS clientWorkOrgName,
            Hospital.smoCode,
            Hospital.infisCode AS hospitalInfisCode,
            OrgStructure.infisCode AS orgStructureInfisCode,
            OrgStructure.tfomsCode AS orgStructureTfomsExtCode,
            Event.order AS eventOrder,
            RelegateOrg.smoCode AS relegateSmoCode,
            RelegateOrg.tfomsExtCode AS relegateTfomsExtCode,
            rbMedicalAidProfile.regionalCode AS medicalAidProfileRegionalCode,
            ServiceMedicalAidProfile.regionalCode AS serviceMedicalAidProfileRegionalCode,
            rbMedicalAidKind.regionalCode AS medicalAidKindRegionalCode,
            rbScene.code AS sceneCode,
            ClientAttach.begDate AS attachBegDate,
            AttachOrg.tfomsExtCode AS attachOrgTfomsExtCode,
            AttachOrg.smoCode AS attachOrgSmoCode,
            AttachOrg.infisCode AS attachOrgInfisCode,
            IF(rbDiseaseCharacter.code = 2, 1, 0) AS DS1_PR,
            CASE
                WHEN rbDispanser.id IS NULL OR rbDispanser.name LIKE '%%нуждается%%' THEN 0
                WHEN rbDispanser.observed = 1 AND rbDispanser.name LIKE '%%взят%%' THEN 2
                WHEN rbDispanser.observed = 1 AND rbDispanser.name NOT LIKE '%%взят%%' THEN 1
                WHEN rbDispanser.observed = 0 AND rbDispanser.name LIKE '%%выздор%%' THEN 4
                WHEN rbDispanser.observed = 0 AND rbDispanser.name NOT LIKE '%%выздор%%' THEN 6
                ELSE 0
            END AS dispanserObserved,
            Action.status AS actionStatus,
            IF(AccCharacter.code = 2, 1, 0) AS DS2_PR,
            rbService_Identification.value AS SERV_METOD,
            rbMedicalAidUnit.regionalCode AS medicalAidUnitCode,
            NOT ISNULL(CurrentOrgAttach.id) AS isAttached,
            rbScene.name LIKE "%%на дому%%" AS isHomeVisit,
            IF(SUBSTR(Diagnosis.MKB, 1, 1) = 'Z', 0,
                rbDiseaseCharacter_Identification.value) AS C_ZAB,
            OrgStructure.infisDepTypeCode AS execOrgInfisDepTypeCode,
            OrgStructure.tfomsCode AS execOrgTfomsCode,
            OrgStructure.infisCode AS execOrgInfisCode,
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
            ) AS orgStructAddrCode,
            IFNULL((SELECT ETI.value FROM EventType_Identification ETI
                WHERE ETI.master_id = EventType.id
                  AND ETI.checkDate <= Event.execDate
                  AND ETI.deleted = 0
                  AND ETI.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE code = 'tfoms51.PURPOSE' AND domain = 'EventType'
            ) ORDER BY ETI.checkDate DESC LIMIT 1), rbService.note) AS serviceNote,
            (SELECT infisCode FROM OrgStructure OS
             WHERE OS.id = IFNULL(IFNULL(ActionPerson.orgStructure_id,
                                         VisitPerson.orgStructure_id),
                                  (SELECT orgStructure_id
                                   FROM Account
                                   WHERE Account.id = Account_Item.master_id))
            ) AS subHospital,
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
            LEFT JOIN Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
            LEFT JOIN rbPolicyKind ON rbPolicyKind.id = ClientPolicy.policyKind_id
            LEFT JOIN ClientDocument ON ClientDocument.client_id = Client.id AND
                      ClientDocument.id = (SELECT MAX(CD.id)
                                         FROM   ClientDocument AS CD
                                         LEFT JOIN rbDocumentType AS rbDT ON rbDT.id = CD.documentType_id
                                         LEFT JOIN rbDocumentTypeGroup AS rbDTG ON rbDTG.id = rbDT.group_id
                                         WHERE  rbDTG.code = '1' AND CD.client_id = Client.id AND CD.deleted=0)
            LEFT JOIN rbDocumentType ON rbDocumentType.id = ClientDocument.documentType_id
            LEFT JOIN Address   RegAddress ON RegAddress.id = getClientRegAddressId(Client.id)
            LEFT JOIN AddressHouse RegAddressHouse ON RegAddressHouse.id = RegAddress.house_id
            LEFT JOIN Address   LocAddress ON LocAddress.id = getClientLocAddressId(Client.id)
            LEFT JOIN AddressHouse LocAddressHouse ON LocAddressHouse.id = LocAddress.house_id
            LEFT JOIN kladr.KLADR RegKLADR ON RegKLADR.CODE = RegAddressHouse.KLADRCode
            LEFT JOIN kladr.KLADR RegRegionKLADR ON RegRegionKLADR.CODE = (
                SELECT RPAD(LEFT(RegAddressHouse.KLADRCode,2),13,'0'))
            LEFT JOIN Person       ON Person.id = Event.execPerson_id
            LEFT JOIN Diagnostic ON Diagnostic.id = (
                SELECT MAX(dc.id)
                    FROM Diagnostic dc
                    WHERE dc.event_id = Account_Item.event_id
                    AND dc.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code in ('1', '2'))
                    AND dc.deleted = 0
            )
            LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
            LEFT JOIN rbDiseaseCharacter ON Diagnostic.character_id = rbDiseaseCharacter.id
            LEFT JOIN rbDiseasePhases ON Diagnostic.phase_id = rbDiseasePhases.id
            LEFT JOIN EventType ON EventType.id = Event.eventType_id
            LEFT JOIN rbService ON rbService.id = IFNULL(Account_Item.service_id, IFNULL(Visit.service_id, EventType.service_id))
            LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
            LEFT JOIN OrgStructure ON OrgStructure.id = Person.orgStructure_id
            LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
            LEFT JOIN OrgStructure AS setOrgStruct ON Person.orgStructure_id = setOrgStruct.id
            LEFT JOIN Diagnostic AS AccDiagnostic ON AccDiagnostic.id = (
                SELECT MAX(dc.id)
                    FROM Diagnostic dc
                    WHERE dc.event_id = Account_Item.event_id
                    AND dc.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code = '9')
                    AND dc.deleted = 0
            )
            LEFT JOIN Diagnosis AS AccDiagnosis ON AccDiagnosis.id = AccDiagnostic.diagnosis_id AND AccDiagnosis.deleted = 0
            LEFT JOIN rbDiseaseCharacter AS AccCharacter ON AccDiagnostic.character_id = AccCharacter.id
            LEFT JOIN ClientSocStatus AS ClientEmploymentStatus ON ClientEmploymentStatus.id = (
                SELECT MAX(id) FROM ClientSocStatus AS CS
                WHERE CS.client_id = Client.id
                    AND CS.deleted = 0
                    AND CS.socStatusClass_id = (
                        SELECT rbSSC.id
                        FROM rbSocStatusClass AS rbSSC
                        WHERE rbSSC.code = '5' AND rbSSC.group_id IS NULL
                        LIMIT 0,1))
            LEFT JOIN rbSocStatusType AS Employment ON
                ClientEmploymentStatus.socStatusType_id =Employment.id
            LEFT JOIN rbVisitType ON rbVisitType.id = Visit.visitType_id
            LEFT JOIN rbDiagnosticResult ON rbDiagnosticResult.id=Diagnostic.result_id
            LEFT JOIN rbResult AS EventResult ON EventResult.id=Event.result_id
            LEFT JOIN Person AS VisitPerson ON VisitPerson.id = Visit.person_id
                AND VisitPerson.id IS NOT NULL
            LEFT JOIN Person AS ActionPerson ON ActionPerson.id = Action.person_id
                AND ActionPerson.id IS NOT NULL
            LEFT JOIN Person AS ActionSetPerson ON ActionSetPerson.id = Action.setPerson_id
                AND ActionSetPerson.id IS NOT NULL
            LEFT JOIN rbSpeciality AS VisitSpeciality ON VisitPerson.speciality_id = VisitSpeciality.id
                AND VisitSpeciality.id IS NOT NULL
            LEFT JOIN rbSpeciality AS ActionSpeciality ON ActionPerson.speciality_id = ActionSpeciality.id
                AND ActionSpeciality.id IS NOT NULL
            LEFT JOIN rbSpeciality AS ActionSetSpeciality ON ActionSetPerson.speciality_id = ActionSetSpeciality.id
                AND ActionSetSpeciality.id IS NOT NULL
            LEFT JOIN Person AS RelegatePerson ON Event.relegatePerson_id = RelegatePerson.id
            LEFT JOIN Organisation AS RelegateOrg ON Event.relegateOrg_id = RelegateOrg.id
            LEFT JOIN rbSpeciality AS RelegateSpeciality ON RelegatePerson.speciality_id = RelegateSpeciality.id
                AND  RelegatePerson.id IS NOT NULL
            LEFT JOIN rbMesSpecification ON Event.mesSpecification_id = rbMesSpecification.id
            LEFT JOIN ClientWork ON ClientWork.client_id=Event.client_id AND
                        ClientWork.id = (SELECT max(CW.id)
                                         FROM ClientWork AS CW
                                         WHERE CW.client_id=Client.id AND CW.deleted=0)
            LEFT JOIN Organisation AS work ON work.id=ClientWork.org_id AND work.deleted = 0
            LEFT JOIN Organisation AS Hospital ON Hospital.id=Person.org_id AND Hospital.deleted = 0
            LEFT JOIN rbService_Profile ON rbService_Profile.id = (SELECT MAX(id) FROM rbService_Profile rs
                WHERE rs.master_id = rbService.id AND rs.speciality_id = Person.speciality_id)
            LEFT JOIN rbMedicalAidProfile ON
                rbService_Profile.medicalAidProfile_id = rbMedicalAidProfile.id
            LEFT JOIN rbMedicalAidProfile AS ServiceMedicalAidProfile ON
                ServiceMedicalAidProfile.id = rbService.medicalAidProfile_id
            LEFT JOIN rbMedicalAidKind ON rbMedicalAidKind.id = EventType.medicalAidKind_id
            LEFT JOIN rbScene ON Visit.scene_id = rbScene.id
            LEFT JOIN ClientAttach ON ClientAttach.id = getClientAttachIdForDate(Client.`id`, 0, Event.execDate)
            LEFT JOIN Organisation AS AttachOrg ON AttachOrg.id = ClientAttach.LPU_id
            LEFT JOIN rbDispanser ON Diagnostic.dispanser_id = rbDispanser.id
            LEFT JOIN ActionType ON Action.actionType_id = ActionType.id
            LEFT JOIN rbService_Identification ON rbService_Identification.id = (
                SELECT MAX(SId.id)
                FROM rbService_Identification SId
                WHERE SId.master_id = IFNULL(rbService.id, ActionType.nomenclativeService_id)
                AND SId.system_id IN (SELECT id FROM rbAccountingSystem WHERE code = 'tfoms51.SERV3_METOD')
                AND SId.deleted = 0
                AND ((SId.checkDate = '2020-12-31' AND Action.endDate <= '2020-12-31') OR
                     (SId.checkDate = '2021-01-01' AND Action.endDate >= '2021-01-01'))
            )
            LEFT JOIN rbMedicalAidUnit ON rbMedicalAidUnit.id = Account_Item.unit_id
            LEFT JOIN ClientAttach AS CurrentOrgAttach ON CurrentOrgAttach.id = (
                SELECT MAX(COA.id)
                FROM ClientAttach COA
                WHERE COA.LPU_id = %d AND COA.client_id = Client.id
                    AND (COA.begDate IS NULL OR COA.begDate <= Event.execDate)
                    AND (COA.endDate IS NULL OR COA.endDate >= Event.execDate)
            )
            LEFT JOIN rbDiseaseCharacter_Identification ON rbDiseaseCharacter_Identification.id = (
                SELECT MAX(DId.id)
                FROM rbDiseaseCharacter_Identification DId
                WHERE DId.master_id = rbDiseaseCharacter.id
                AND DId.system_id IN (SELECT id FROM rbAccountingSystem WHERE urn = 'urn:tfoms51:V027')
                AND DId.deleted = 0
            )
            WHERE
                Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s
        """ % (0 if not QtGui.qApp.currentOrgId() else QtGui.qApp.currentOrgId(),
               self.tableAccountItem['id'].inlist(self.idList))

        return self.db.query(stmt)

# ******************************************************************************

    def _getServiceQuery(self, eventId, endDate):
        u"""Формирует запрос об услугах по идентификатору
            события и дате окончания услуги"""
        financeId = forceRef(self.db.translate(
            'Contract', 'id', self.accountInfo()['contractId'], 'finance_id'))

        stmt = """SELECT Action.endDate,
            Action.begDate,
            Action.org_id,
            Person.SNILS AS personCode,
            rbSpeciality.regionalCode AS specialityCode,
            setOrgStruct.infisCode AS setOrgStructCode,
            ActionType.code,
            Diagnosis.MKB,
            RelegateSpeciality.federalCode AS relegatePersonCode,
            rbMesSpecification.code AS mesSpecificationCode,
            rbMesSpecification.level AS mesSpecificationLevel,
            Action.id AS id,
            rbMedicalAidProfile.regionalCode AS medicalAidProfileRegionalCode,
            ServiceMedicalAidProfile.regionalCode AS serviceMedicalAidProfileRegionalCode,
            IFNULL((SELECT ETI.value FROM EventType_Identification ETI
                WHERE ETI.master_id = EventType.id
                  AND ETI.checkDate <= Event.execDate
                  AND ETI.deleted = 0
                  AND ETI.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE code = 'tfoms51.PURPOSE' AND domain = 'EventType'
            ) ORDER BY ETI.checkDate DESC LIMIT 1), rbService.note) AS serviceNote,
            EventType.regionalCode AS eventTypeCode,
            rbVisitType.code AS visitTypeCode,
            rbSpeciality.federalCode AS execSpecialityFederalCode,
            Action.amount,
            rbScene.code AS sceneCode,
            AttachOrg.tfomsExtCode AS attachOrgTfomsExtCode,
            AttachOrg.smoCode AS attachOrgSmoCode,
            AttachOrg.infisCode AS attachOrgInfisCode,
            rbService_Identification.value AS SERV_METOD,
            ExecOrgStruct.infisDepTypeCode AS execOrgInfisDepTypeCode,
            ExecOrgStruct.tfomsCode AS execOrgTfomsCode,
            ExecOrgStruct.infisCode AS execOrgInfisCode,
            ServiceFinance.value AS VID_FIN,
            (SELECT OSI.value
             FROM OrgStructure_Identification OSI
             WHERE OSI.master_id = IFNULL(Person.orgStructure_id,(
                    SELECT orgStructure_id
                    FROM Account WHERE Account.id = {accountId}))
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
            (SELECT infisCode FROM OrgStructure OS
             WHERE OS.id = IFNULL(Person.orgStructure_id,
                                  (SELECT orgStructure_id
                                   FROM Account
                                   WHERE Account.id = {accountId}))
            ) AS subHospital
        FROM Action
        LEFT JOIN ActionType ON Action.actionType_id = ActionType.id
        LEFT JOIN Person ON Action.person_id = Person.id
        LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
        LEFT JOIN OrgStructure AS setOrgStruct ON Person.orgStructure_id = setOrgStruct.id
        LEFT JOIN ActionType_Service ON ActionType_Service.master_id = ActionType.id
            AND (ActionType_Service.finance_id = '{financeId}' OR ActionType_Service.finance_id IS NULL)
        LEFT JOIN Event ON Action.event_id = Event.id
        LEFT JOIN Person AS ExecPerson ON Event.execPerson_id = ExecPerson.id
        LEFT JOIN OrgStructure AS ExecOrgStruct ON ExecOrgStruct.id = ExecPerson.orgStructure_id
        LEFT JOIN Person AS RelegatePerson ON Event.relegatePerson_id = RelegatePerson.id
        LEFT JOIN rbSpeciality AS RelegateSpeciality ON RelegatePerson.speciality_id = RelegateSpeciality.id
            AND  RelegatePerson.id IS NOT NULL
        LEFT JOIN Diagnostic ON ( Diagnostic.event_id = Action.event_id
                                  AND Diagnostic.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code= '1')
                                  AND Diagnostic.deleted = 0)
        LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
        LEFT JOIN rbMesSpecification ON Event.mesSpecification_id = rbMesSpecification.id
        LEFT JOIN Visit ON Action.visit_id = Visit.id
        LEFT JOIN rbVisitType ON Visit.visitType_id = rbVisitType.id
        LEFT JOIN EventType ON Event.eventType_id = EventType.id
        LEFT JOIN rbService ON ActionType_Service.service_id = rbService.id
        LEFT JOIN rbService_Profile ON rbService_Profile.id = (SELECT MAX(id) FROM rbService_Profile rs
            WHERE rs.master_id = rbService.id AND rs.speciality_id = Person.speciality_id)
        LEFT JOIN rbMedicalAidProfile ON
            rbService_Profile.medicalAidProfile_id = rbMedicalAidProfile.id
        LEFT JOIN rbMedicalAidProfile AS ServiceMedicalAidProfile ON
            ServiceMedicalAidProfile.id = rbService.medicalAidProfile_id
        LEFT JOIN rbScene ON Visit.scene_id = rbScene.id
        LEFT JOIN ClientAttach ON ClientAttach.id = getClientAttachIdForDate(Event.client_id, 0, Event.execDate)
        LEFT JOIN Organisation AS AttachOrg ON AttachOrg.id = ClientAttach.LPU_id
        LEFT JOIN rbService_Identification ON rbService_Identification.id = (
            SELECT MAX(SId.id)
            FROM rbService_Identification SId
            WHERE SId.master_id = IFNULL(rbService.id, ActionType.nomenclativeService_id)
            AND SId.system_id IN (SELECT id FROM rbAccountingSystem WHERE code = 'tfoms51.SERV3_METOD')
            AND SId.deleted = 0
            AND ((SId.checkDate = '2020-12-31' AND Action.endDate <= '2020-12-31') OR
                 (SId.checkDate = '2021-01-01' AND Action.endDate >= '2021-01-01'))
        )
        LEFT JOIN rbService_Identification AS ServiceFinance ON ServiceFinance.id = (
            SELECT MAX(SId1.id)
            FROM rbService_Identification SId1
            WHERE SId1.master_id = IFNULL(rbService.id, ActionType.nomenclativeService_id)
            AND SId1.system_id IN (SELECT id FROM rbAccountingSystem WHERE code = 'VID_FIN')
            AND SId1.deleted = 0
        )
        WHERE Action.event_id = '{eventId}' AND Action.endDate <= '{endDate}' AND Action.deleted = '0'
            AND ActionType_Service.service_id IS NOT NULL
        """.format(financeId=financeId, eventId=eventId,
                   endDate=endDate.toString(Qt.ISODate),
                   accountId=self.accountInfo()['accId'])
        return self.db.query(stmt)

# ******************************************************************************

    def _getVisitQuery(self, eventId, begDate, endDate, exportOther):
        u"""Формирует запрос о визитах события по его идентификатору"""
        _filter = (u"""rbVisitType.code = 'ВУ' AND NOT
            (Visit.date BETWEEN '%s' AND '%s')""" % (
                begDate.toString(Qt.ISODate), endDate.toString(Qt.ISODate))
                   if exportOther else
                   u"""Visit.date <= '%s'""" % (endDate.toString(Qt.ISODate)))

        stmt = u"""SELECT Visit.date,
            Person.SNILS AS personCode,
            rbSpeciality.regionalCode AS specialityCode,
            setOrgStruct.infisCode AS setOrgStructCode,
            rbVisitType.code AS visitTypeCode,
            rbService.infis,
            Diagnosis.MKB,
            RelegateOrg.infisCode AS relegateOrgCode,
            RelegateSpeciality.federalCode AS relegatePersonCode,
            Visit.id AS id,
            rbMedicalAidProfile.regionalCode AS medicalAidProfileRegionalCode,
            ServiceMedicalAidProfile.regionalCode AS serviceMedicalAidProfileRegionalCode,
            RelegateOrg.smoCode AS relegateSmoCode,
            RelegateOrg.tfomsExtCode AS relegateTfomsExtCode,
            IFNULL((SELECT ETI.value FROM EventType_Identification ETI
                WHERE ETI.master_id = EventType.id
                  AND ETI.checkDate <= Event.execDate
                  AND ETI.deleted = 0
                  AND ETI.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE code = 'tfoms51.PURPOSE' AND domain = 'EventType'
            ) ORDER BY ETI.checkDate DESC LIMIT 1), rbService.note) AS serviceNote,
            EventType.regionalCode AS eventTypeCode,
            rbSpeciality.federalCode AS execSpecialityFederalCode,
            rbMesSpecification.level AS mesSpecificationLevel,
            rbScene.code AS sceneCode,
            AttachOrg.tfomsExtCode AS attachOrgTfomsExtCode,
            AttachOrg.smoCode AS attachOrgSmoCode,
            AttachOrg.infisCode AS attachOrgInfisCode,
            rbService_Identification.value AS SERV_METOD,
            ExecOrgStruct.infisDepTypeCode AS execOrgInfisDepTypeCode,
            ExecOrgStruct.tfomsCode AS execOrgTfomsCode,
            ExecOrgStruct.infisCode AS execOrgInfisCode,
            (SELECT OSI.value
             FROM OrgStructure_Identification OSI
             WHERE OSI.master_id = IFNULL(Person.orgStructure_id,(
                    SELECT orgStructure_id
                    FROM Account WHERE Account.id = {accountId}))
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
            ) AS orgStructAddrCode
        FROM Visit
        LEFT JOIN Person ON Visit.person_id = Person.id
        LEFT JOIN rbVisitType ON rbVisitType.id = Visit.visitType_id
        LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
        LEFT JOIN OrgStructure AS setOrgStruct ON Person.orgStructure_id = setOrgStruct.id
        LEFT JOIN rbService ON Visit.service_id = rbService.id
        LEFT JOIN Event ON Visit.event_id = Event.id
        LEFT JOIN Person AS ExecPerson ON Event.execPerson_id = ExecPerson.id
        LEFT JOIN OrgStructure AS ExecOrgStruct ON ExecOrgStruct.id = ExecPerson.orgStructure_id
        LEFT JOIN Organisation AS RelegateOrg ON Event.relegateOrg_id = RelegateOrg.id
        LEFT JOIN Person AS RelegatePerson ON Event.relegatePerson_id = RelegatePerson.id
        LEFT JOIN rbSpeciality AS RelegateSpeciality ON RelegatePerson.speciality_id = RelegateSpeciality.id
            AND  RelegatePerson.id IS NOT NULL
        LEFT JOIN Diagnostic ON ( Diagnostic.event_id = Visit.event_id
                                  AND Diagnostic.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code= '1')
                                  AND Diagnostic.deleted = 0)
        LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
        LEFT JOIN rbService_Profile ON rbService_Profile.id = (SELECT MAX(id) FROM rbService_Profile rs
            WHERE rs.master_id = rbService.id AND rs.speciality_id = Person.speciality_id)
        LEFT JOIN rbMedicalAidProfile ON
            rbService_Profile.medicalAidProfile_id = rbMedicalAidProfile.id
        LEFT JOIN rbMedicalAidProfile AS ServiceMedicalAidProfile ON
            ServiceMedicalAidProfile.id = rbService.medicalAidProfile_id
        LEFT JOIN EventType ON Event.eventType_id = EventType.id
        LEFT JOIN rbMesSpecification ON Event.mesSpecification_id = rbMesSpecification.id
        LEFT JOIN rbScene ON Visit.scene_id = rbScene.id
        LEFT JOIN ClientAttach ON ClientAttach.id = getClientAttachIdForDate(Event.client_id, 0, Event.execDate)
        LEFT JOIN Organisation AS AttachOrg ON AttachOrg.id = ClientAttach.LPU_id
        LEFT JOIN rbService_Identification ON rbService_Identification.id = (
            SELECT MAX(SId.id)
            FROM rbService_Identification SId
            WHERE SId.master_id = rbService.id
            AND SId.system_id IN (SELECT id FROM rbAccountingSystem WHERE code = 'tfoms51.SERV3_METOD')
            AND SId.deleted = 0
            AND ((SId.checkDate = '2020-12-31' AND Visit.date <= '2020-12-31') OR
                 (SId.checkDate = '2021-01-01' AND Visit.date >= '2021-01-01'))
        )
        WHERE Visit.event_id = '{eventId}' AND {filter} AND Visit.deleted = '0'
        """.format(eventId=eventId, filter=_filter,
                   accountId=self.accountInfo()['accId'])
        return self.db.query(stmt)

# ******************************************************************************

    def getEventSum(self):
        u"""возвращает общую стоимость услуг за событие"""

        stmt = u"""SELECT A.event_id, SUM(A.sum) AS totalSum
        FROM (
            SELECT Account_Item.event_id,
                Account_Item.sum,
                rbVisitType.code AS visitTypeCode
            FROM Account_Item
            LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
            LEFT JOIN Event ON Account_Item.event_id = Event.id
            LEFT JOIN rbMesSpecification ON Event.mesSpecification_id = rbMesSpecification.id
            LEFT JOIN Visit ON Account_Item.visit_id = Visit.id
            LEFT JOIN rbVisitType ON Visit.visitType_id = rbVisitType.id
            WHERE Account_Item.reexposeItem_id IS NULL
                AND NOT ((Event.mesSpecification_id IS NULL OR rbMesSpecification.code = '10')
                    AND (Account_Item.visit_id IS NOT NULL OR Account_Item.action_id IS NOT NULL))
                AND NOT ((Event.mesSpecification_id IS NOT NULL AND rbMesSpecification.code != '10')
                    AND (Account_Item.visit_id IS NULL AND Account_Item.action_id IS NULL))
                AND (Account_Item.date IS NULL
                     OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                    )
                AND %s) AS A
        WHERE A.visitTypeCode IS NULL OR A.visitTypeCode != 'ВУ'
        GROUP BY A.event_id;""" \
            % self.tableAccountItem['id'].inlist(self.idList)

        query = self.db.query(stmt)
        result = {}

        while query.next():
            record = query.record()
            eventId = forceRef(record.value('event_id'))
            result[eventId] = forceDouble(record.value('totalSum'))

        return result

# ******************************************************************************

    def _exportServices(self, dbf, params):
        u"""Выгрузка услуг"""

        eventId = params['eventId']
        endDate = params['endDate']
        query = self._getServiceQuery(eventId, endDate)

        while query.next():
            record = query.record()
            actionId = forceRef(record.value('id'))
            actionList = params['actionList'].get(eventId, [])

            if actionId in actionList:
                continue

            if record:
                row = dbf.newRecord()
                # Номер статталона Используется для связи с файлом ALIENS
                row['CARD'] = forceString(eventId)
                row['IDSERV'] = forceString(params['serviceNumber'])
                params['serviceNumber'] += 1

                # Номер реестра, представляемого в ТФОМС
                row['CODE_COUNT'] = params.get('accNumber', '')
                # Личный код  медицинского работника, оказавшего услугу
                row['P_CODE'] = formatSNILS(record.value('personCode'))
                # Код услуги Код из приложения № 1
                row['SERVICE'] = forceString(record.value('code'))
                # Кол-во услуг
                row['UNITS'] = forceInt(record.value('amount'))
                # Дата оказания услуги
                actionStatus = forceInt(record.value('actionStatus'))
                isCanceled = actionStatus == 6
                servDate = forceDate(record.value(
                    'begDate' if isCanceled else 'endDate'))
                row['SERV_DATE'] = pyDate(servDate)
                #  Код ЛПУ, направившего пациента на консультацию
                # (обследование) Код из справочника HOSPITAL
                row['DIRECT_LPU'] = forceString(record.value(
                    params['directLpuField']))
                # Признак учета результатов  осмотров (исследований),
                # выполненных ранее:
                # «0» - услуга оказана в период диспансеризации, «1» - услуга
                # оказана до проведения диспансеризации или в другой МО
                orgId = forceRef(record.value('org_id'))
                row['AIM'] = '1' if ((orgId and orgId != params['lpuId'])
                                     or not ((servDate >= params['begDate'])
                                             and (servDate <= endDate))
                                    ) else '0'
                # Сумма по базовой программе гос. гарантий
                row['STOIM_S'] = params.get('actionSum', {}).get(
                    forceRef(record.value('id')), 0.0)
                #Диагноз
                row['DS'] = forceString(record.value('MKB'))
                # Код специальности медицинского работника,
                # направившего пациента на консультацию (обследование)
                row['DIR_SPEC'] = forceInt(record.value(
                    'relegatePersonCode')) % 10000
                _processServiceExport2016(row, record, params)
                row['NPL'] = mapAcionStatusToNpl.get(actionStatus, 0)
                if row['NPL'] == 4 and servDate >= params['begDate']:
                    row['NPL'] = 0
                row['SERV_METOD'] = forceString(record.value('SERV_METOD'))
                row['P_OTK'] = 1 if isCanceled else 0
                row['NPR_DATE'] = pyDate(self._getDirectionDate(eventId))
                if self.exportType >= self.exportType2020:
                    row['mpcod'] = params['mpcod']
                    row['addr_code'] = params['addr_code']
                row.store()

# ******************************************************************************

    def _exportVisits(self, dbf, params, exportOther=False):
        u"""Выгрузка визитов"""
        eventId = params['eventId']
        begDate = params['begDate']
        endDate = params['endDate']
        query = self._getVisitQuery(eventId, begDate, endDate, exportOther)

        while query.next():
            record = query.record()
            visitId = forceRef(record.value('id'))
            visitList = params['visitList'].get(eventId, [])

            if visitId in visitList:
                continue

            if record:
                row = dbf.newRecord()
                # Номер статталона
                row['CARD'] = forceString(eventId)
                row['IDSERV'] = str(params['serviceNumber'])
                params['serviceNumber'] += 1

                # Номер реестра, представляемого в ТФОМС
                row['CODE_COUNT'] = params.get('accNumber', '')
                # Личный код  медицинского работника, оказавшего услугу
                row['P_CODE'] = formatSNILS(record.value('personCode'))
                # Код услуги Код из приложения № 1
                row['SERVICE'] = forceString(record.value('infis'))
                # Кол-во услуг
                row['UNITS'] = 1
                # Дата оказания услуги
                servDate = forceDate(record.value('date'))
                row['SERV_DATE'] = pyDate(servDate)
                #  Код ЛПУ, направившего пациента на консультацию
                # (обследование) Код из справочника HOSPITAL
                row['DIRECT_LPU'] = forceString(record.value(
                    params['directLpuField']))
                # Признак учета результатов  осмотров (исследований),
                # выполненных ранее:
                # «0» - услуга оказана в период диспансеризации, «1» - услуга
                # оказана до проведения диспансеризации или в другой МО
                visitTypeCode = forceString(record.value('visitTypeCode'))

                if visitTypeCode == u'ВУ':
                    row['AIM'] = '1'
                else:
                    row['AIM'] = '0' if ((servDate >= begDate) and
                                         (servDate <= endDate)) else '1'
                    # Сумма по базовой программе гос. гарантий
                    row['STOIM_S'] = params.get('visitSum', {}).get(
                        forceRef(record.value('id')), 0.0)
                #Диагноз
                row['DS'] = forceString(record.value('MKB'))
                # Код специальности медицинского работника, направившего
                # пациента на консультацию (обследование)
                row['DIR_SPEC'] = forceInt(record.value(
                    'relegatePersonCode')) % 10000
                _processServiceExport2016(row, record, params)
                row['NPL'] = mapAcionStatusToNpl.get(
                    forceInt(record.value('actionStatus')), 0)
                if row['NPL'] == 4 and servDate >= params['begDate']:
                    row['NPL'] = 0
                row['SERV_METOD'] = forceString(record.value('SERV_METOD'))
                if self.exportType >= self.exportType2020:
                    row['mpcod'] = params['mpcod']
                    row['addr_code'] = params['addr_code']
                row.store()

# ******************************************************************************

    def preprocessQuery(self, query, params):
        while query.next():
            record = query.record()

            # МЭС выполнен, если код 10 или не заполнен
            isMesComplete = ((forceString(record.value(
                'mesSpecificationCode')) == '10') or
                             not forceRef(record.value('mesSpecificationId'))
                             or forceInt(record.value(
                                 'mesSpecificationLevel')) == 2)
            visitId = forceRef(record.value('visitId'))
            actionId = forceRef(record.value('actionId'))
            _sum = forceDouble(record.value('sum'))

            if not isMesComplete:
                if visitId:
                    params.setdefault('visitSum', {})[visitId] = _sum
                elif actionId:
                    params.setdefault('actionSum', {})[actionId] = _sum

        query.exec_()

# ******************************************************************************

    def process(self, dbf, record, params):
        eventTypeCode = forceInt(record.value('eventTypeCode'))
        localParams = {
            'birthDate': forceDate(record.value('birthDate')),
            'begDate': forceDate(record.value('begDate')),
            'endDate': forceDate(record.value('endDate')),
            'eventId': forceRef(record.value('event_id')),
            'clientId': forceRef(record.value('client_id')),
            '_sum' : forceDouble(record.value('sum')),
            # проф.осмотры и первый этап ДД
            'firstStage': eventTypeCode in (3, 7),
            'eventTypeCode': eventTypeCode,
            'actionOrgId' :forceRef(record.value('actionOrgId')),
            'mesSpecificationLevel': forceInt(record.value(
                'mesSpecificationLevel'))
        }

        localParams['isMesComplete'] = ((forceString(record.value(
            'mesSpecificationCode')) == '10') or
                                        not forceRef(record.value(
                                            'mesSpecificationId')))
        visitId = forceRef(record.value('visitId'))
        actionId = forceRef(record.value('actionId'))

        if localParams['isMesComplete'] and (visitId or actionId):
            # Если Особенности выполнения МЭС События имеет атрибут
            # "Выполнено полностью", строки реестра счета, связанные с
            # таковым Событием относящиеся к тарификации Визитов или
            # Действий (заполнены идентификаторы визита и действия)
            # - игнорируем.
            return

        (dbfAliens, dbfService, dbfAddInf, dbfDirect, dbfDs2n, dbfNapr, _) = dbf
        localParams['dbfService'] = dbfService
        localParams.update(params)

        if localParams['eventId'] not in params['exportedEvents']:
            self._processAliens(dbfAliens, record, localParams)

        if params.get('lastEventId') != localParams['eventId']:
            params['serviceNumber'] = 1
            localParams['serviceNumber'] = 1
            params['lastEventId'] = localParams['eventId']

        if (not localParams['firstStage'] or
                (localParams['mesSpecificationLevel'] != 2)):
            self._processService(dbfService, record, localParams)

        self._processAddInf(dbfAddInf, record, localParams)
        exportDs2n(dbfDs2n, record, localParams)
        params['ds2nCache'] = localParams.setdefault('ds2nCache', {})
        self._processDirect(dbfDirect, record, localParams)
        params['serviceNumber'] = localParams['serviceNumber']
        phaseCode = (forceInt(record.value('diseasePhaseCode'))
                     if record else None)
        mkb = forceString(record.value('MKB'))
        if ((mkb == 'Z03.1') or (
                phaseCode == 10 and (mkb.startswith(('C', 'D0'))))):
            localParams['onkologyInfo'] = getOnkologyInfo(
                self.db, self.tableAccountItem['id'].inlist(self.idList),
                exportType2019=True)
            self._exportNapr(dbfNapr, record, localParams)

# ******************************************************************************

    def _processAliens(self, dbf, record, params):
        u"""Выгрузка информации в ALIENS.DBF"""
        endDate = params['endDate']
        eventId = params['eventId']
        eventTypeCode = params['eventTypeCode']
        row = dbf.newRecord()
        # Код ЛПУ пребывания по справочнику фонда
        row['CODE_HOSP'] = forceString(record.value('hospitalInfisCode'))
        row['FOR_POM'] = self.mapEventOrderToForPom.get(
            forceInt(record.value('eventOrder')), 0)
        row['VIDPOM'] = forceInt(record.value(
            'medicalAidKindRegionalCode')) % 10000
        row['PROFIL'] = forceInt(record.value('execSpecialityCode')) % 1000
        row['PRVS'] = forceInt(record.value(
            'execSpecialityFederalCode')) % 10000
        row['VID_FIN'] = 1
        # Номер реестра, представляемого в ТФОМС
        row['CODE_COUNT'] = params.get('accNumber', '')
        # Отчетный месяц Указывается первое число месяца
        row['DATE_LOW'] = pyDate(firstMonthDay(endDate))
        # Номер статталона Уникальное поле для реестра
        row['CARD'] = forceString(eventId)
        # Код СМО Код из справочника SMO
        row['INS'] = params['payerInfis']
        # Серия полиса Для полисов нового образца не заполняется
        row['SERPOL'] = forceString(record.value('policySerial'))
        # Номер полиса
        row['NMBPOL'] = forceString(record.value('policyNumber'))
        # Статус пациента
        clientStatus = forceString(record.value('clientStatus'))
        work = '1' if forceString(record.value(
            'clientWorkOrgName')) else '0'
        row['WORK'] = clientStatus if clientStatus else work
        # Дата начала диспансеризации
        row['DATIN'] = pyDate(params['begDate'])
        # Дата окончания диспансеризации
        row['DATOUT'] = pyDate(endDate)
        # Диагноз основной Код из справочника MKB
        row['DIAG'] = forceString(record.value('MKB'))
        # Фамилия пациента
        row['FAM'] = forceString(record.value('lastName'))
        # Имя пациента
        row['IMM'] = forceString(record.value('firstName'))
        # Отчество пациента
        row['OTC'] = forceString(record.value('patrName'))
        # Серия документа, удостоверяющего личность
        row['SER_PASP'] = forceString(record.value('documentSerial'))
        # Номер документа, удостоверяющего личность
        row['NUM_PASP'] = forceString(record.value('documentNumber'))
        # Тип документа, удостоверяющего личность
        row['TYP_DOC'] = forceInt(record.value('documentRegionalCode'))
        # Страховой номер индивидуального лицевого счета
        row['SS'] = formatSNILS(record.value('SNILS'))
        # Дата рождения пациента
        row['BIRTHDAY'] = pyDate(params['birthDate'])
        # Пол пациента «М» или «Ж»
        row['SEX'] = formatSex(forceString(record.value('sex')))
        # Код населенного пункта проживания
        row['TAUN'] = forceString(record.value('placeCode'))
        # Код ЛПУ приписки
        row['MASTER'] = forceString(record.value('attachOrgInfisCode'))
        # Сумма по базовой программе гос. гарантий
        mesSpecificationLevel = forceInt(record.value(
            'mesSpecificationLevel'))
        row['STOIM_S'] = (forceDouble(record.value('sum')) if
                          mesSpecificationLevel == 2 else
                          params.get('eventSum', {}).get(eventId, 0))

        # Тип полиса:
        row['TPOLIS'] = forceInt(record.value('policyKind'))
        # признак законченного случая
        row['PRIZN_ZS'] = eventTypeCode % 10
        # Результат обращения/ госпитализации
        row['RSLT'] = forceInt(record.value('eventResultCode')) % 1000
        # Исход заболевания
        row['ISHOD'] = forceInt(record.value(
            'resultRegionalCode')) % 1000
        # Код врача, закрывшего талон/историю болезни
        row['P_CODE'] = formatSNILS(record.value('personRegionalCode'))
        row['DS1_PR'] = forceInt(record.value('DS1_PR'))
        row['INV'] = 0
        row['PR_D_N'] = forceInt(record.value('dispanserObserved'))
        row['PR_OS'] = 0
        row['IDSP'] = getIdsp(forceInt(record.value('medicalAidUnitCode')),
                              forceBool(record.value('isAttached')),
                              forceBool(record.value('isHomeVisit')))
        row['DS2'] = forceString(record.value('accMKB'))[:6]
        row['DS2_PR'] = forceInt(record.value('DS2_PR'))
        row['PURPOSE'] = forceString(record.value('serviceNote'))
        row['NPR_MO'] = forceString(record.value('relegateOrgCode'))
        row['NPR_DATE'] = pyDate(self._getDirectionDate(eventId))
        row['C_ZAB'] = forceInt(record.value('C_ZAB')) % 10

        phaseCode = forceInt(record.value(
            'diseasePhaseCode')) if record else None
        mkb = forceString(record.value('MKB'))
        row['DS_ONK'] = mkb == 'Z03.1' or (
            phaseCode == 10 and (mkb.startswith(('C', 'D0'))))
        row['DOCDATE'] = pyDate(forceDate(record.value('DOCDATE')))
        row['DOCORG'] = forceString(record.value('DOCORG'))[:250]

        if self.exportType >= self.exportType2020:
            row['mpcod'] = forceString(record.value('orgStructMpCod'))[:8]
            row['addr_code'] = forceString(record.value(
                'orgStructAddrCode'))[:16]
            params['mpcod'] = row['mpcod']
            params['addr_code'] = row['addr_code']

        if self.exportType >= self.exportType2021 and phaseCode == 10:
            row['DS_PZ'] = mkb

        row.store()
        params['exportedEvents'].add(eventId)
        dbfService = params['dbfService']

        if params['firstStage']:
            self._exportServices(dbfService, params)
            self._exportVisits(dbfService, params)
        elif not params['isExternalServiceExposed']:
            self._exportServices(dbfService, params)
            self._exportVisits(dbfService, params, True)


# ******************************************************************************

    def _processService(self, dbf, record, params):
        u"""Выгрузка услуг в SERVICE.DBF"""
        row = dbf.newRecord()
        # Номер статталона Используется для связи с файлом ALIENS
        row['CARD'] = forceString(params['eventId'])
        # Номер реестра, представляемого в ТФОМС
        row['CODE_COUNT'] = params.get('accNumber', '')
        # Личный код  медицинского работника, оказавшего услугу
        row['P_CODE'] = formatSNILS(record.value('execPersonCode'))
        # Код услуги Код из приложения № 1
        row['SERVICE'] = forceString(record.value('service'))
        # Кол-во услуг
        row['UNITS'] = forceInt(record.value('amount'))
        # Дата оказания услуги
        servDate = forceDate(record.value('actionDate'))
        if not servDate:
            servDate = forceDate(record.value('visitDate'))
        if not servDate:
            servDate = params['endDate']

        if not servDate:
            self.log(u'Не задана дата услуги: accountItemId=%d,'\
                u' код карточки "%d".' % (forceRef(
                    record.value('accountItem_id')), params['eventId']))

        row['SERV_DATE'] = pyDate(servDate)

        #Диагноз
        row['DS'] = forceString(record.value('MKB'))
        # Код специальности медицинского работника, направившего
        # пациента на консультацию (обследование)
        row['DIR_SPEC'] = forceInt(record.value(
            'relegatePersonCode')) % 10000

        if not row['DIR_SPEC']:
            row['DIR_SPEC'] = forceInt(record.value(
                'execSpecialityFederalCode')) % 100000

        #  Код ЛПУ, направившего пациента на консультацию
        # (обследование) Код из справочника HOSPITAL
        row['DIRECT_LPU'] = forceString(record.value(
            params['directLpuField']))

        visitTypeCode = forceString(record.value('visitTypeCode'))
        actionOrgId = params['actionOrgId']

        if (params['eventTypeCode'] == 4 and
                # Если визит с "типом визита" = "ВУ"
                (visitTypeCode == u'ВУ' or
                 # Если визит не попадает в рамки события, Если в действии
                 # "дата выполнения" не попадает в рамки события
                 (servDate < params['begDate']) or
                 (servDate > params['endDate'])) or
                # Если в действии "место выполнение" отличается от текущего
                (actionOrgId and actionOrgId != params.get('lpuId'))):
            row['STOIM_S'] = params['_sum'] if params[
                'isExternalServiceExposed'] else 0
            row['AIM'] = '1'
        else:
            row['AIM'] = '0'
            # Сумма по базовой программе гос. гарантий
            row['STOIM_S'] = params['_sum']

        _processServiceExport2016(row, record, params)
        row['NPL'] = mapAcionStatusToNpl.get(
            forceInt(record.value('actionStatus')), 0)
        if row['NPL'] == 4 and servDate >= params['begDate']:
            row['NPL'] = 0
        row['SERV_METOD'] = forceString(record.value('SERV_METOD'))
        row['NPR_DATE'] = pyDate(self._getDirectionDate(params['eventId']))
        row['IDSERV'] = str(params['serviceNumber'])
        params['serviceNumber'] += 1

        orgTfomsCode = forceString(record.value('orgStructureTfomsExtCode'))
        row['SUB_HOSP'] = (forceString(record.value('subHospital'))
                           if self.exportType >= self.exportType2021
                           else forceString(record.value('orgStructureInfisCode')))
        row['TOWN_HOSP'] = orgTfomsCode

        if self.exportType >= self.exportType2020:
            row['mpcod'] = forceString(record.value('orgStructMpCod'))[:8]
            row['addr_code'] = forceString(record.value(
                'orgStructAddrCode'))[:16]
        if self.exportType >= self.exportType2021:
            row['VID_VME'] = forceString(record.value('vidVme'))
        row.store()

# ******************************************************************************

    def _getDirectionDate(self, eventId):
        result = self._directionDateCache.get(eventId, -1)

        if result == -1:
            stmt = u"""SELECT B.begDate FROM (
                SELECT MAX(A.id), A.begDate
                FROM Action A
                WHERE A.event_id = {eventId} AND
                          A.deleted = 0 AND
                          A.actionType_id IN (
                                SELECT AT.id
                                FROM ActionType AT
                                WHERE AT.flatCode IN ('hospitalDirection', 'recoveryDirection', 'consultationDirection', 'inspectionDirection', 'researchDirection')
                          )
            ) AS B""".format(eventId=eventId)
            query = self.db.query(stmt)

            if query.first():
                record = query.record()
                result = forceDate(record.value(0))
                self._directionDateCache[eventId] = result

        return result

# ******************************************************************************

    def _processAddInf(self, dbf, record, params):
        u"""Выгрузка информации в ADD_INF.DBF"""
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

        if representativeInfo != {}:
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

        row['C_DOC'] = forceInt(record.value('documentRegionalCode'))
        row['S_DOC'] = forceString(record.value('documentSerial'))
        row['N_DOC'] = forceString(record.value('documentNumber'))
        row['NOVOR'] = '0' # Признак новорожденного
        specState = ''
        age = forceInt(record.value('clientAge'))

        if (not forceString(record.value('policySerial')) and
                not forceString(record.value('policyNumber'))):
            specState += '1'
        if age == 0:
            specState += '2'
        if age < 14 and self.getClientRepresentativeInfo(clientId) != {}:
            specState += '3'
        if not forceString(record.value('patrName')):
            specState += '4'

        row['Q_G'] = specState
        row['MSE'] = 0
        row['DOCDATE'] = pyDate(forceDate(record.value('DOCDATE')))
        row['DOCORG'] = forceString(record.value('DOCORG'))[:250]

        row.store()

# ******************************************************************************

    def _processDirect(self, dbf, _, params):
        eventId = params['eventId']

        if eventId not in self.exportedEvents:
            dirList = self._getDirectionList(params['eventId'])
            self.exportedEvents.add(eventId)

            for dirId, dirCode in dirList:
                r = self.db.getRecord('Action', '*', dirId)
                action = CAction(record=r)

                row = dbf.newRecord()
                row['CARD'] = params['eventId']
                row['NAZR'] = dirCode
                row['NAZ_V'] = (forceInt(action['NAZ_V'])
                                if r and dirCode == 3 else 0)
                try:
                    row['NAZ_SP'] = ((forceInt(self.getSpecialityFederalCode(
                        action['NAZ_SP'])) % 10000) if r and dirCode == 1
                                     else 0)
                except ValueError:
                    row['NAZ_SP'] = 0
                row.store()

# ******************************************************************************

    def _exportNapr(self, dbf, _, params):
        u'Пишет направления'
        row = dbf.newRecord()
        row['CARD'] = params['eventId']
        onkRecord = params['onkologyInfo'].get(params['eventId'])

        if onkRecord:
            #Задача №0010463:"ТФОМС Мурманск. Изменения по Приказу ФФОМС №285"
            row['NAPR_DATE'] = pyDate(forceDate(onkRecord.value(
                'eventSetDate')))
            lpuId = QtGui.qApp.currentOrgId()
            row['NAPR_MO'] = forceString(self.db.translate(
                'Organisation', 'id', lpuId, 'infisCode')) if lpuId else ''

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

            #Задача №0010463:"ТФОМС Мурманск. Изменения по Приказу ФФОМС №285"
            row['NAPR_V'] = 4

            if (val == 3 and action.hasProperty(u'Вид направления') and
                    mapMetIssl.has_key(action[u'Вид направления'])):
                row['MET_ISSL'] = mapMetIssl.get(action[u'Вид направления'])

            if row['MET_ISSL']:
                prevAction = CAction.getActionById(action.prevAction_id)

                if prevAction:
                    serviceId = prevAction.getType().nomenclativeServiceId
                    row['NAPR_USL'] = self.getServiceCode(serviceId)

        row.store()

# ******************************************************************************

    def _getDirectionList(self, eventId):
        u'Создает список направлений по событию'
        stmt = """SELECT A.id, IF(AT.flatCode = 'inspectionDirection', 3, 1)
            FROM Action A
            LEFT JOIN ActionType AT ON A.actionType_id = AT.id
            WHERE A.event_id = %d
                AND A.deleted = 0
                AND AT.deleted = 0
                AND AT.flatCode IN ('inspectionDirection', 'consultationDirection')
                """ % eventId

        query = self.db.query(stmt)
        result = set()

        while query.next():
            record = query.record()
            result.add((forceRef(record.value(0)), forceInt(record.value(1))))

        return result

# ******************************************************************************

    def _getVisitAndActionList(self):
        u"""Возвращает кортеж из 2ух словарей со списком оттарифицированных
            визитов и действий"""

        stmt = """SELECT event_id,
            group_concat(action_id) AS actionList,
            group_concat(visit_id) AS visitList
            FROM Account_Item
            LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
            WHERE
                Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s
            GROUP BY event_id
        """ % self.tableAccountItem['id'].inlist(self.idList)

        query = self.db.query(stmt)
        actions = {}
        visits = {}

        while query.next():
            record = query.record()

            if record:
                eventId = forceRef(record.value('event_id'))
                actionList = forceString(record.value('actionList'))
                visitList = forceString(record.value('visitList'))

                if actionList:
                    actions[eventId] = map(forceInt, actionList.split(','))

                if visitList:
                    visits[eventId] = map(forceInt, visitList.split(','))

        return actions, visits

# ******************************************************************************

class CExportPage2(CAbstractExportPage2):
    u"""Вторая страница мастера экспорта"""
    def __init__(self, parent):
        CAbstractExportPage2.__init__(self, parent, 'R51DD2013')

    def saveExportResults(self):
        files = ('ALIENS.DBF', 'SERVICE.DBF', 'ADD_INF.DBF',
                 'DIRECT.DBF', 'DS2_N.DBF', 'NAPR.DBF')

        if self._parent.page1.exportType >= CExportPage1.exportType2020:
            files += ('SERV_TMT.DBF', )

        return self.moveFiles(files)

if __name__ == '__main__':
    #pylint: disable=wrong-import-position,ungrouped-imports
    from Exchange.Utils import testAccountExport
    #pylint: enable=wrong-import-position,ungrouped-imports
    testAccountExport(exportR51DD2013, u'ДВН17-90/ДВН1эт', '75_18_s11.ini',
                      [80690342])
