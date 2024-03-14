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
u"""Экспорт реестра счета для стоматологии. Мурманск"""

import os.path
import shutil

from PyQt4 import QtGui
from PyQt4.QtCore import QDate

from library.dbfpy.dbf import Dbf
from library.Utils import (forceBool, forceInt, toVariant,
    forceString, forceRef, forceDouble, nameCase, pyDate,
    formatSNILS, forceStringEx, firstMonthDay)

from Registry.Utils import getAttachRecord
from Exchange.Export import (CExportHelperMixin, CAbstractExportWizard,
    CAbstractExportPage1, CAbstractExportPage2)
from Exchange.ExportR51OMS import (mapAcionStatusToNpl, getIdsp, forceDate)

from Exchange.Ui_ExportR51StomatologyPage1 import Ui_ExportPage1


def exportR51Stomatology(widget, accountId, accountItemIdList, _=None):
    u"""Создает диалог экспорта реестра счета"""

    wizard = CExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.exec_()

# ******************************************************************************

class CExportWizard(CAbstractExportWizard):
    u"""Мастер экспорта реестра услуг стоматологической помощи"""

    def __init__(self, parent=None):
        title = (u'Мастер экспорта реестра услуг стоматологической помощи'
            u' для Мурманской области')
        CAbstractExportWizard.__init__(self, parent, title)
        self.page1 = CExportPage1(self)
        self.page2 = CExportPage2(self)

        self.addPage(self.page1)
        self.addPage(self.page2)


    def getTmpDir(self):
        return CAbstractExportWizard.getTmpDirEx(self, 'R51ST')

# ******************************************************************************

class CExportPage1(CAbstractExportPage1, Ui_ExportPage1, CExportHelperMixin):
    u"""Первая страница мастера экспорта"""

    mapAttachCodeToDispType = {'1':'1', '2':'1', '5':'2', '3':'3', '4':'4'}
    mapDispReasonCode = {'4':'1', '3':'2', '5':'3'}
    mapEventOrderToForPom = {2: 1, 6: 2, 1:3}

    exportType2019 = 0
    exportType2020 = 1
    exportType2021 = 2

    def __init__(self, parent):
        CAbstractExportPage1.__init__(self, parent)
        CExportHelperMixin.__init__(self)

        prefs = QtGui.qApp.preferences.appPrefs
        self.ignoreErrors = forceBool(prefs.get('ExportR51STIgnoreErrors',
                                                 False))
        self.chkVerboseLog.setChecked(forceBool(prefs.get(
                                      'ExportR51STVerboseLog', False)))
        self.cmbExportType.setCurrentIndex(forceInt(prefs.get(
                                           'ExportR51STExportType', 0)))
        self.chkIgnoreErrors.setChecked(self.ignoreErrors)

        self.exportedEvents = set()
        self.exportType = 0
        self.tableAction = self.db.table('Action')
        self.exportedActionsList = []
        self.firstVisit = {}


    def validatePage(self):
        QtGui.qApp.preferences.appPrefs[
        'ExportR51STIgnoreErrors'] = toVariant(self.chkIgnoreErrors.isChecked())
        QtGui.qApp.preferences.appPrefs[
        'ExportR51STVerboseLog'] = toVariant(self.chkVerboseLog.isChecked())
        QtGui.qApp.preferences.appPrefs[
        'ExportR51STExportType'] = toVariant(self.cmbExportType.currentIndex())
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
        self.ignoreErrors = self.chkIgnoreErrors.isChecked()
        self.exportType = self.cmbExportType.currentIndex()
        self.exportedEvents = set()
        self.firstVisit = {}
        params = {}

        lpuId = QtGui.qApp.currentOrgId()
        params['lpuCode'] = forceString(self.db.translate(
            'Organisation', 'id', lpuId, 'infisCode'))
        self.log(u'ЛПУ:  код инфис: "%s".' % params['lpuCode'])
        self.exportedActionsList = []

        if not params['lpuCode']:
            self.log(u'<b><font color=red>ОШИБКА<\font><\b>:'
                     u'Для текущего ЛПУ не задан код инфис', True)
            if not self.ignoreErrors:
                self.abort()
                return

        if self.idList:
            params.update(self.accountInfo())

            self.progressBar.setText(u'Запрос в БД...')
            QtGui.qApp.processEvents()
            params['mapEventIdToSum'] = self.getEventsSummaryPrice()
            params['mapToothToVisitCount'] = self.getToothVisitInfo()
            params['mapSpecToVisitCount'] = self.getSpecVisitInfo()
            params['payerCode'] = forceString(self.db.translate(
                'Organisation', 'id', params['payerId'], 'infisCode'))
            params['registryId'] = forceString(self.accountId())
            params['specialityCodeFieldName'] = 'specialityOKSOCode'
            params['serviceNumber'] = 1

        self.setProcessParams(params)
        funcList = (self.process, self._processTooth, self._processSpeciality)
        self.setProcessFuncList(funcList)
        CAbstractExportPage1.exportInt(self)


    def createDbf(self):
        return (self.createStReestrDbf(),
                    self.createToothDbf(),
                    self.createSpecVisDbf(),
                    self.createServicesDbf(),
                    self.createGuestsDbf(),
                    self.createNaprDbf()
                    )


    def createNaprDbf(self):
        """ Создает структуру dbf для NAPR.DBF """
        dbfName = os.path.join(self.getTmpDir(), 'NAPR.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        cardFieldName = ('ID_TALON' if self.exportType >= self.exportType2021
                         else 'CARD')
        dbf.addField(
            (cardFieldName, 'C', 10), # Номер статталона
            ('NAPR_DATE', 'D', 8),
            ('NAPR_MO', 'C', 3),
            ('NAPR_V', 'N', 2),
            ('MET_ISSL', 'N', 2),
            ('NAPR_USL', 'C', 15)
        )
        return dbf


    def createStReestrDbf(self):
        u""" Создает структуру dbf для файла типа STREESTR.DBF"""

        dbfName = os.path.join(self.getTmpDir(), 'STREESTR.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('ID_TALON', 'C', 10),   #Номер талона
            ('INS', 'C', 2),   #Код СМО (по справочнику фонда)
            ('ADMITANCE', 'C', 1),   #Тип приема  (взрослый - 1/
                                                   #детский плановый - 2/
                                                   # детский  амбулаторный - 3 /
                                                   # ортодонтия - 4 )
            ('DATE_LO', 'D'),   #Дата с ...   |Интервал дат
            ('DATE_UP', 'D'),   #Дата по ...  |выписки
            ('PRIMARY', 'C', 1),   #Признак первичности
                                            #(Первич. - 1 / Повторн. – 2)
            ('WORK', 'C', 1),   #Признак: работающий-1/неработающий-0 (пациент)
            ('DATIN', 'D'),   #Дата начала лечения
            ('DATOUT', 'D'),   #Дата окончания лечения
            ('URGENT', 'C', 1),   #Признак оказания мед. Помощи
                                            #(0 – план./ 1- экстр.)
            ('VISITS', 'N', 2),   #Количество посещений
            ('UNITS', 'N', 6, 2),   #   Сумма единиц трудозатрат (УЕТ)
            ('FAM', 'C', 40),   #Фамилия
            ('IMM', 'C', 40),   #Имя
            ('OTC', 'C', 40),   #Отчество
            ('SER_PASP', 'C', 8),   #Серия документа, удостоверяющего личность
            ('NUM_PASP', 'C', 8),   #Номер документа, удостоверяющего личность
            ('TYP_DOC', 'N', 2),   # Тип документа, удостоверяющего личность
                # (приложение «Типы документов»)
            ('SS', 'C', 14),   # Страховой номер индивидуального лицевого счета
            ('SERPOL', 'C', 10),   #Серия полиса
            ('NMBPOL', 'C', 20),   #Номер полиса
            ('TAUN', 'C', 3), #Код населенного пункта проживания пациента
                                        #по справочнику фонда
            ('BIRTHDAY', 'D'),   #Дата рождения пациента
            ('SEX', 'C', 1),   #Пол пациента («0» –жен, «1» – муж)
            ('ID_REESTR', 'C', 10),   #Номер реестра
            ('ID_HOSP', 'C', 3),   #Код  стоматологического  АПУ
            ('SUB_HOSP', 'C',  (3 if self.exportType >= self.exportType2021
                                 else 2)),#
            ('TOWN_HOSP', 'C', 3),#
            ('STOIM_S', 'N', 10, 2), #Сумма из средств Федеральных субвенций
            ('TPOLIS', 'N', 1),   #Тип полиса:  1 – старого образца,
                # 2 – временное свидетельство 3 – нового образца
            ('MASTER', 'C', 3),   #Коды ЛПУ приписки по справочнику
                # фонда (стоматология)
            ('RSLT', 'N', 3), # Результат обращения/ госпитализации
            ('ISHOD', 'N', 3), # Исход заболевания
            ('DET', 'N', 1), # Признак детского профиля
            ('P_CODE', 'C', 14), # Код врача, закрывшего талон
                                            # /историю болезни
            ('FOR_POM', 'N', 1), # Форма оказания медицинской помощи
            ('VID_FIN', 'N', 1), # Источник финансирования
            ('VIDPOM', 'N', 4), #Вид медицинской помощи
            ('INV', 'N', 1), #Группа инвалидности
            ('IDSP', 'N', 2), #Код способа оплаты медицинской помощи
            ('DS_ONK', 'N', 1),
            ('PURPOSE', 'C', 3),
            ('C_ZAB', 'N', 1),
            ('DOCDATE', 'D'), #
            ('DOCORG', 'C', 250), #
            ('mpcod', 'C', 8), #
            ('addr_code', 'C', 16), #
        )
        return dbf


    def createToothDbf(self):
        u"""Создает структуру dbf для файла типа TOOTH.DBF"""

        dbfName = os.path.join(self.getTmpDir(), 'TOOTH.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('ID_TALON', 'C', 10), # Номер талона
            ('TOOTH', 'C', 2), # Номер зуба по международной классификации
            ('DIAG', 'C', 6), # Код диагноза
            ('PRVS', 'N', 4)
        )

        dbf.addField(
            ('SPEC', 'C', 3), # Код специальности медицинского работника,
                                       # оказавшего услугу
            ('VISITS', 'N', 2),   #Количество посещений по данному заболеванию
            ('UNITS_SUM', 'N', 6, 2),   #Сумма единиц трудозатрат услуг (УЕТ)
            ('ID_REESTR', 'C', 10),   #Номер реестра
        )
        return dbf


    def createSpecVisDbf(self):
        u"""Создает структуру dbf для файла типа SPEC_VIS.DBF"""

        dbfName = os.path.join(self.getTmpDir(), 'SPEC_VIS.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('ID_TALON', 'C', 10),   #Номер талона
            ('SPEC', 'C', 3), # Код специальности медицинского работника,
                                    # оказавшего услугу
            ('PRVS', 'N', 4),   #Специальность лечащего врача
            ('VISITS', 'N', 2), # Количество посещений по данной специальности
            ('UNITS_SUM', 'N', 6, 2), # Сумма единиц трудозатрат услуг (УЕТ)
            ('ID_REESTR', 'C', 10), # Номер реестра
            ('ID_HOSP', 'C', 3), # Код стоматологического  АПУ
        )
        return dbf


    def createServicesDbf(self):
        u"""Создает структуру dbf для файла типа SERVICES.DBF"""

        dbfName = os.path.join(self.getTmpDir(), 'SERVICES.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('ID_TALON', 'C', 10),   #Номер талона
            ('TOOTH', 'C', 2),   #Номер зуба по международной классификации
            ('DIAG', 'C', 6),   #Код диагноза
            ('DS0', 'C', 6),   #Код диагноза первичный
            ('SPEC', 'C', 3), # Код специальности медицинского работника,
                                        # оказавшего услугу
            ('P_CODE', 'C', 14),   #Личный код  медицинского работника,
                                    # оказавшего услугу

            ('ID_SERV', 'C', 15),   #Код услуги
            ('SERV_DATE', 'D'),   #Дата оказания услуги
            ('SERVNUMBER', 'N', 2),   #Кол-во услуг данного типа
            ('UNITS_SUM', 'N', 6, 2),   #Сумма единиц трудозатрат услуг (УЕТ)
            ('ID_REESTR', 'C', 10),   #Номер реестра
            ('STOIM_S', 'N', 10, 2), # Сумма из средств Федеральных субвенций
            ('PROFIL', 'N', 3),#
            ('PRVS', 'N', 4),#
            ('VID_FIN', 'N', 1),#
            ('PURPOSE', 'C', 3),#
            ('P_MODE', 'N', 2),#
            ('NPL', 'N', 1), #Неполный объём
            ('IDUSL', 'C', 36), #
            ('mpcod', 'C', 8), #
            ('addr_code', 'C', 16), #
        )
        return dbf


    def createGuestsDbf(self):
        u"""Создает структуру dbf для файла типа GUESTS.DBF"""

        dbfName = os.path.join(self.getTmpDir(), 'GUESTS.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('ID_TALON', 'C', 10), # Номер истории болезни
            ('MR', 'C', 100), # Место рождения пациента или представителя
            ('OKATOG', 'C', 11), # Код места жительства по ОКАТО
            ('OKATOP', 'C', 11), # Код места пребывания по ОКАТО
            ('OKATO_OMS', 'C', 5), # Код ОКАТО территории страхования по ОМС
                                                    # (по справочнику фонда)
            ('FAMP', 'C', 40),   #Фамилия (представителя) пациента
            ('IMP', 'C', 40),   #Имя  (представителя) пациента
            ('OTP', 'C', 40),   #Отчество родителя (представителя) пациента
            ('DRP', 'D'),   #Дата рождения (представителя) пациента
            ('WP', 'C', 1),   #Пол  (представителя) пациента
            ('C_DOC', 'N', 2), # Код типа документа, удостоверяющего личность
                # пациента (представителя) (по  справочнику фонда)
            ('S_DOC', 'C', 9),   #Серия документа, удостоверяющего личность
                # пациента (представителя) (по  справочнику фонда)
            ('N_DOC', 'C', 8),   #Номер документа, удостоверяющего личность
                # пациента (представителя) (по  справочнику фонда)
            ('NOVOR', 'C', 9),   #Признак новорожденного
            ('Q_G', 'C', 7),   #Признак «Особый случай» при регистрации
                # обращения  за медицинской помощью
            ('MSE', 'N', 1), # Направление на МСЭ
            ('DOCDATE', 'D'), #
            ('DOCORG', 'C', 250), #
        )
        return dbf


    def createQuery(self):
        return (self._createMainQuery(),
                self._createToothQuery(),
                self._createSpecQuery())


    def _createMainQuery(self):
        u"""Создает основной запрос в БД для заполнения реестра счета"""

        stmt = u"""SELECT Account_Item.event_id AS eventId,
            Account_Item.uet,
            Account_Item.`sum`,
            Account_Item.amount,
            Account_Item.price,
            Account_Item.tariff_id AS tariffId,
            Insurer.infisCode AS policyInsurer,
            Event.setDate AS begDate,
            Event.execDate AS endDate,
            Event.isPrimary,
            Event.client_id AS clientId,
            IF(rbDiagnosticResult.code IS NULL, EventResult.code, rbDiagnosticResult.code) AS resultCode,
            EventResult.regionalCode AS eventResultRegionalCode,
            IF(rbDiagnosticResult.regionalCode IS NULL, EventResult.regionalCode, rbDiagnosticResult.regionalCode) AS resultRegionalCode,
            work.id AS workId,
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
            Client.SNILS AS SNILS,
            ClientPolicy.serial AS policySerial,
            ClientPolicy.number AS policyNumber,
            ClientPolicy.note AS policyNote,
            age(Client.birthDate, Event.execDate) as clientAge,
            RegAddressHouse.KLADRCode AS regKLADRCode,
            LocAddressHouse.KLADRCode AS locKLADRCode,
            rbPolicyKind.regionalCode AS policyKind,
            Diagnosis.MKB AS MKB,
            rbSpeciality.regionalCode AS specialityCode,
            rbSpeciality.federalCode AS specialityFederalCode,
            RegKLADR.OCATD AS regOKATO,
            LocKLADR.OCATD AS locOKATO,
            Insurer.area AS insurerArea,
            Insurer.OKATO AS insurerOKATO,
            Person.code AS personCode,
            IF(Account_Item.service_id IS NOT NULL,
                rbItemService.infis,
                IF(Account_Item.visit_id IS NOT NULL, rbVisitService.infis, rbEventService.infis)
                ) AS serviceCode,
            IF(Account_Item.visit_id IS NOT NULL, Visit.person_id,
                    IF(Account_Item.action_id IS NOT NULL,
                            IF(Action.person_id IS NOT NULL, Action.person_id, Action.setPerson_id), Event.execPerson_id)
                ) AS execPersonId,
            Action.endDate AS actionDate,
            Action.MKB AS actionMKB,
            Action.id AS actionId,
            Person.SNILS AS personSNILS,
            ActionPersonSpeciality.federalCode AS actionPersonSpecialityFederalCode,
            OrgStructure.infisCode AS orgStructureInfis,
            OrgStructure.tfomsCode AS orgStructureTfomsCode,
            Event.order AS eventOrder,
            IFNULL((SELECT ETI.value FROM EventType_Identification ETI
                WHERE ETI.master_id = EventType.id
                  AND ETI.checkDate <= Event.execDate
                  AND ETI.deleted = 0
                  AND ETI.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE code = 'tfoms51.PURPOSE' AND domain = 'EventType'
            ) ORDER BY ETI.checkDate DESC LIMIT 1),
                EventType.regionalCode) AS purposeCode,
            rbPost.code AS postCode,
            Hospital.smoCode AS execOrgSmoCode,
            Hospital.infisCode AS hospitalInfisCode,
            rbMedicalAidKind.regionalCode AS medicalAidKindRegionalCode,
            IF(rbMedicalAidProfile.id IS NOT NULL,
                rbMedicalAidProfile.regionalCode,
                    ServiceMedicalAidProfile.regionalCode)
                AS medicalAidProfileRegionalCode,
            Action.status AS actionStatus,
            rbMedicalAidUnit.regionalCode AS medicalAidUnitCode,
            NOT ISNULL(CurrentOrgAttach.id) AS isAttached,
            rbScene.name LIKE "%%на дому%%" AS isHomeVisit,
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
             WHERE OSI.master_id = OrgStructure.id
                AND OSI.deleted = 0
                AND OSI.system_id = (
                    SELECT MAX(id) FROM rbAccountingSystem
                    WHERE rbAccountingSystem.code = 'addr_code')
            ) AS orgStructAddrCode
            FROM Account_Item
            LEFT JOIN Action ON Action.id = Account_Item.action_id
            LEFT JOIN Visit  ON Visit.id  = Account_Item.visit_id
            LEFT JOIN Event  ON Event.id  = Account_Item.event_id
            LEFT JOIN EventType ON Event.eventType_id = EventType.id
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
            LEFT JOIN Person       ON Person.id = Event.execPerson_id
            LEFT JOIN Person AS ActionPerson ON ActionPerson.id = Action.person_id
            LEFT JOIN Diagnostic ON ( Diagnostic.event_id = Account_Item.event_id
                                      AND Diagnostic.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code in ('1', '2'))
                                      AND Diagnostic.deleted = 0 )
            LEFT JOIN ClientWork ON ClientWork.client_id=Event.client_id AND
                        ClientWork.id = (SELECT max(CW.id)
                                         FROM ClientWork AS CW
                                         WHERE CW.client_id=Client.id AND CW.deleted=0)
            LEFT JOIN Organisation AS work ON work.id=ClientWork.org_id AND work.deleted = 0
            LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
            LEFT JOIN rbDiagnosticResult ON rbDiagnosticResult.id=Diagnostic.result_id
            LEFT JOIN rbResult AS EventResult ON EventResult.id=Event.result_id
            LEFT JOIN rbService AS rbEventService ON rbEventService.id = EventType.service_id
            LEFT JOIN rbService AS rbVisitService ON rbVisitService.id = Visit.service_id
            LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
            LEFT JOIN rbService AS rbItemService ON rbItemService.id = Account_Item.service_id
            LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
            LEFT JOIN rbSpeciality AS ActionPersonSpeciality ON ActionPerson.speciality_id = ActionPersonSpeciality.id
            LEFT JOIN OrgStructure ON Person.orgStructure_id = OrgStructure.id
            LEFT JOIN rbPost ON rbPost.id = Person.post_id
            LEFT JOIN Organisation AS Hospital ON Hospital.id = Person.org_id
            LEFT JOIN rbMedicalAidKind ON rbMedicalAidKind.id = EventType.medicalAidKind_id
            LEFT JOIN rbService_Profile ON rbService_Profile.id = (SELECT MAX(id) FROM rbService_Profile rs
                WHERE rs.master_id = rbItemService.id AND rs.speciality_id = Person.speciality_id)
            LEFT JOIN rbMedicalAidProfile ON
                rbService_Profile.medicalAidProfile_id = rbMedicalAidProfile.id
            LEFT JOIN rbMedicalAidProfile AS ServiceMedicalAidProfile ON
                ServiceMedicalAidProfile.id = rbItemService.medicalAidProfile_id
            LEFT JOIN rbMedicalAidUnit ON rbMedicalAidUnit.id = Account_Item.unit_id
            LEFT JOIN ClientAttach AS CurrentOrgAttach ON CurrentOrgAttach.id = (
                SELECT MAX(COA.id)
                FROM ClientAttach COA
                WHERE COA.LPU_id = %d AND COA.client_id = Client.id
                    AND (COA.begDate IS NULL OR COA.begDate <= Event.execDate)
                    AND (COA.endDate IS NULL OR COA.endDate >= Event.execDate)
            )
            LEFT JOIN rbScene ON rbScene.id = Visit.scene_id
            LEFT JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnosis.character_id
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
        """ % (QtGui.qApp.currentOrgId(),
               self.tableAccountItem['id'].inlist(self.idList))

        return self.db.query(stmt)

# ******************************************************************************

    def getEventsSummaryPrice(self):
        u"""возвращает общую стоимость услуг за событие"""

        stmt = """SELECT Account_Item.event_id,
            SUM(Account_Item.sum) AS totalPrice,
            SUM(Contract_Tariff.federalPrice) AS federalSum,
            SUM(Account_Item.uet) AS uet,
            (SELECT COUNT(DISTINCT Visit.id)
                FROM Visit
                WHERE Visit.event_id = Account_Item.event_id
                AND Visit.deleted = 0
                  )  AS visitCount
        FROM Account_Item
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        LEFT JOIN Action ON Action.id = Account_Item.action_id
        LEFT JOIN Contract_Tariff ON Account_Item.tariff_id = Contract_Tariff.id
        WHERE Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s
        GROUP BY Account_Item.event_id;""" \
            % self.tableAccountItem['id'].inlist(self.idList)

        query = self.db.query(stmt)
        result = {}

        while query.next():
            record = query.record()
            eventId = forceRef(record.value('event_id'))
            _sum = forceDouble(record.value('totalPrice'))
            uet = forceDouble(record.value('uet'))
            federal = forceDouble(record.value(2))
            visitCount = forceInt(record.value('visitCount')) % 100
            result[eventId] = (_sum, federal, uet,
                               visitCount if visitCount > 0 else 1)

        return result

# ******************************************************************************

    def _createToothQuery(self):
        u"""Создает запрос в БД для заполнения таблицы TOOTH.DBF"""

        stmt = u"""SELECT Account_Item.event_id AS eventId,
            Diagnosis.MKB,
            Action.MKB AS actionMKB,
            SUM(Account_Item.uet) AS uet,
            SUM(Account_Item.amount) AS amount,
            rbSpeciality.regionalCode AS specialityCode,
            rbSpeciality.federalCode AS specialityFederalCode,
            rbSpeciality.OKSOCode AS specialityOKSOCode,
            OrgStructure.infisCode AS orgStructureInfis,
            Tooth.value AS toothNumber
        FROM Account_Item
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        LEFT JOIN Action ON Action.id = Account_Item.action_id
        LEFT JOIN Event ON Account_Item.event_id = Event.id
        LEFT JOIN Person ON Person.id = Action.person_id
        LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
        LEFT JOIN Diagnostic ON ( Diagnostic.event_id = Account_Item.event_id
                                  AND Diagnostic.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code in ('1', '2'))
                                  AND Diagnostic.deleted = 0)
        LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
        LEFT JOIN EventType ON EventType.id = Event.eventType_id
        LEFT JOIN OrgStructure ON Person.orgStructure_id = OrgStructure.id
        LEFT JOIN ActionProperty_String AS Tooth ON Tooth.id = (
            SELECT APOS.id
            FROM ActionProperty AS AP
                LEFT JOIN ActionPropertyType ON ActionPropertyType.id = AP.type_id
                LEFT JOIN ActionProperty_String AS APOS ON APOS.id = AP.id
            WHERE AP.action_id = Action.id
                AND ActionPropertyType.name = '№ зуба'
        )
        WHERE Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s
        GROUP BY Account_Item.event_id, %s, Tooth.value""" % (
                self.tableAccountItem['id'].inlist(self.idList),
                'specialityOKSOCode')
        return self.db.query(stmt)

# ******************************************************************************

    def getToothVisitInfo(self):
        u"""Подсчитывает количество визитов по каждого набора
        'событие,мкб, специальность, № зуба'."""

        result = {}
        specialityCodeFieldName = 'specialityOKSOCode'

        stmt = u"""SELECT Account_Item.event_id AS eventId,
            Diagnosis.MKB,
            rbSpeciality.regionalCode AS specialityCode,
            rbSpeciality.OKSOCode AS specialityOKSOCode,
            rbSpeciality.federalCode AS specialityFederalCode,
            COUNT(DISTINCT Visit.id) AS visitCount,
            Action.id AS actionId
        FROM Account_Item
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        LEFT JOIN Action ON Action.id = Account_Item.action_id
        LEFT JOIN Event ON Account_Item.event_id = Event.id
        LEFT JOIN Person       ON Person.id = Action.person_id
        LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
        LEFT JOIN Diagnostic ON ( Diagnostic.event_id = Account_Item.event_id
                                  AND Diagnostic.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code in ('1', '2'))
                                  AND Diagnostic.deleted = 0)
        LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
        LEFT JOIN Visit ON Visit.event_id = Event.id
                    AND Visit.date >= Action.begDate
                    AND Visit.date < DATE_ADD(Action.endDate,INTERVAL 1 DAY)
                    AND Visit.deleted = 0
        WHERE Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s
        GROUP BY Account_Item.event_id, MKB, %s;""" % (
            self.tableAccountItem['id'].inlist(self.idList),
            specialityCodeFieldName)

        query = self.db.query(stmt)

        while query.next():
            record = query.record()

            if not record:
                continue

            actionId = forceRef(record.value('actionId'))
            eventId = forceString(record.value('eventId'))[:10]
            mkb = forceString(record.value('MKB'))[:6]
            specialityCode = forceString(record.value(specialityCodeFieldName))
            tooth = forceString(self.toothNumber(actionId))[:2]
            visitCount = forceInt(record.value('visitCount')) % 100
            key = (eventId, mkb, specialityCode, tooth)
            result[key] = visitCount if visitCount > 0 else 1

        return result

# ******************************************************************************

    def _createSpecQuery(self):
        u"""Создает запрос для заполнения таблицы SPEC_VIS.DBF"""

        stmt = u"""SELECT Account_Item.event_id AS eventId,
            SUM(Account_Item.uet) AS uet,
            SUM(Account_Item.amount) AS amount,
            rbSpeciality.regionalCode AS specialityCode,
            rbSpeciality.federalCode AS specialityFederalCode,
            rbSpeciality.OKSOCode AS specialityOKSOCode,
            OrgStructure.infisCode AS orgStructureInfis
        FROM Account_Item
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        LEFT JOIN Action ON Action.id = Account_Item.action_id
        LEFT JOIN Event ON Account_Item.event_id = Event.id
        LEFT JOIN Visit ON Visit.event_id = Account_Item.event_id
                    AND Visit.date >= Action.begDate
                    AND Visit.date < DATE_ADD(Action.endDate,INTERVAL 1 DAY)
                    AND Visit.deleted = 0
        LEFT JOIN Person ON Person.id = Visit.person_id
        LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
        LEFT JOIN OrgStructure ON Person.orgStructure_id = OrgStructure.id
        WHERE Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s
        GROUP BY Account_Item.event_id, %s;""" % (
            self.tableAccountItem['id'].inlist(self.idList),
            'specialityOKSOCode')
        return self.db.query(stmt)

# ******************************************************************************

    def getSpecVisitInfo(self):
        u"""Возвращает словарь с числом визитов по событию и специальности"""

        stmt = u"""SELECT Account_Item.event_id AS eventId,
            rbSpeciality.regionalCode AS specialityCode,
            COUNT(DISTINCT Visit.id) AS visitCount
        FROM Account_Item
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        LEFT JOIN Action ON Action.id = Account_Item.action_id
        LEFT JOIN Event ON Account_Item.event_id = Event.id
        LEFT JOIN Person ON Person.id = Event.execPerson_id
        LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
        LEFT JOIN Visit ON Visit.event_id = Account_Item.event_id
                    AND Visit.date >= Action.begDate
                    AND Visit.date < DATE_ADD(Action.endDate,INTERVAL 1 DAY)
                    AND Visit.deleted = 0
        WHERE Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s
        GROUP BY Account_Item.event_id, specialityCode;""" \
            % self.tableAccountItem['id'].inlist(self.idList)

        query = self.db.query(stmt)
        result = {}

        while query.next():
            record = query.record()

            if not record:
                continue

            eventId = forceString(record.value('eventId'))[:10]
            specialityCode = forceString(record.value('specialityCode'))
            visitCount = forceInt(record.value('visitCount')) % 100
            key = (eventId, specialityCode)
            result[key] = visitCount if visitCount > 0 else 1

        return result

# ******************************************************************************

    def process(self, dbf, record, params):
        insurerArea = forceString(record.value('insurerArea'))

        local_params = {
            'birthDate': forceDate(record.value('birthDate')),
            'begDate': forceDate(record.value('begDate')),
            'endDate': forceDate(record.value('endDate')),
            # Номер стат.талона
            'eventId': forceRef(record.value('eventId')),
            'clientId': forceRef(record.value('clientId')),
            'uet': forceDouble(record.value('uet')),
            'specialityCode': forceString(record.value('specialityCode'))[:3],
            'sum': forceDouble(record.value('sum')),
            'attachOrgCode': '',
            'federalSum':  forceDouble(record.value('federalSum')),
            'isAlien': insurerArea[:2] != QtGui.qApp.defaultKLADR()[:2],
            'lastName': nameCase(forceString(record.value('lastName'))),
            'firstName': nameCase(forceString(record.value('firstName'))),
            'patrName': nameCase(forceString(record.value('patrName'))),
            'sex': forceInt(record.value('sex')),
            'policySerial': forceString(record.value('policySerial'))[:10],
            'policyNumber': forceString(record.value('policyNumber'))[:20],
            'orgStructureCode': forceString(
                                    record.value('orgStructureInfis')).strip(),
            'documentRegionalCode': forceInt(
                                          record.value('documentRegionalCode')),
            'documentNumber': forceString(record.value('documentNumber')),
            'documentSerial': forceString(record.value('documentSerial')),
        }

        local_params.update(params)
        clientAttachRecord = getAttachRecord(local_params['clientId'], False)

        if clientAttachRecord:
            clientAttachOrgId = clientAttachRecord.get('LPU_id', None)

            if clientAttachOrgId:
                local_params['attachOrgCode'] = forceString(self.db.translate(
                    'Organisation', 'id', clientAttachOrgId, 'infisCode'))
            else:
                self.log(u'В записи прикрепления отсутствует код ЛПУ.')

        else:
            self.log(u'Внимание: не задано ЛПУ постоянного прикрепления'
                u' пациента. clientId=%d' % local_params['clientId'])

        (stReestrDbf, _, _, servicesDbf, guestsDbf, _) = dbf

        if local_params['eventId'] not in self.exportedEvents:
            params['serviceNumber'] = 1
            self.exportedEvents.add(local_params['eventId'])
            self._processStReestr(stReestrDbf, record, local_params)

            if local_params['isAlien']:
                self._processGuests(guestsDbf, record, local_params)

        self._processServices(servicesDbf, record, local_params)
        params['serviceNumber'] += 1


    def _processStReestr(self, dbf, record, params):
        u"""Заполняет таблицу STREESTR.DBF"""

        row = dbf.newRecord()
        (eventSum, _, eventUet, visitCount) = (params['mapEventIdToSum'].get(
                                               params['eventId'],
                                               (0.0, 0.0, 0.0, 1)))

        #Номер талона
        row['ID_TALON'] = forceString(params['eventId'])[:10]
        #Код СМО (по справочнику фонда)
        row['INS'] = params['payerCode'][:2]
        # Тип приема  (взрослый - 1/детский плановый - 2/
        # детский  амбулаторный - 3 / ортодонтия - 4 )
        row['ADMITANCE'] = '1'
        #Дата с ...   |Интервал дат
        row['DATE_LO'] = pyDate(firstMonthDay(params['endDate']))
        #Дата по ...  |выписки
        exposeDate = params['exposeDate']
        row['DATE_UP'] = pyDate(exposeDate if exposeDate else QDate.currentDate())
        #Признак первичности (Первич. - 1 / Повторн. – 2)
        row['PRIMARY'] = '1' if (forceInt(record.value(
            'isPrimary')) == 1) else '2'
        #Признак: работающий-1/неработающий-0 (пациент)
        row['WORK'] = '1' if forceRef(record.value('workId'))  else '0'
        #Дата начала лечения
        row['DATIN'] = pyDate(params['begDate'])
        #Дата окончания лечения
        row['DATOUT'] = pyDate(params['endDate'])
        #Признак оказания мед. Помощи (0 – план./ 1- экстр.)
        row['URGENT'] = '0' if forceInt(record.value(
            'eventOrder')) == 1 else '1'
        #Количество посещений
        row['VISITS'] = visitCount
        #Сумма единиц трудозатрат (УЕТ)
        row['UNITS'] = eventUet
        #Фамилия
        row['FAM'] = params['lastName']
        #Имя
        row['IMM'] = params['firstName']
        #Отчество
        row['OTC'] = params['patrName']

        #Серия документа, удостоверяющего личность
        documentSerial = params['documentSerial'][:8]

        if params['documentRegionalCode'] == 3:
            documentSerial = documentSerial.strip().replace(' ', '-')

        row['SER_PASP'] = documentSerial
        #Номер документа, удостоверяющего личность
        row['NUM_PASP'] = params['documentNumber'][:8]
        #Тип документа, удостоверяющего личность
        row['TYP_DOC'] = params['documentRegionalCode']
        #Страховой номер индивидуального лицевого счета
        row['SS'] = formatSNILS(forceString(record.value('SNILS')))
        #Персональный  индивидуальный номер застрахованного по ОМС
        #row['PIN'] = ''
        #Серия полиса
        row['SERPOL'] = params['policySerial']
        #Номер полиса
        row['NMBPOL'] = params['policyNumber']
        locKLADRCode = forceString(record.value('locKLADRCode'))

        if not locKLADRCode:
            locKLADRCode = forceString(record.value('regKLADRCode'))

        townCode = forceString(self.db.translate(
            'kladr.KLADR', 'CODE', locKLADRCode, 'infis'))

        if not townCode:
            self.log(u'Не задан инфис код для города "%s", clientId=%d' %\
                    (locKLADRCode, params['clientId']))

        #Код населенного пункта проживания пациента по справочнику фонда
        row['TAUN'] = townCode[:3]
        #Дата рождения пациента
        row['BIRTHDAY'] = pyDate(params['birthDate'])
        #Пол пациента («0» –жен, «1» – муж)
        row['SEX'] = '1' if params['sex'] == 1 else '0'
        #Номер реестра
        row['ID_REESTR'] = params['registryId']
        #Код  стоматологического  АПУ
        orgStructureCode = forceString(record.value('hospitalInfisCode'))
        row['ID_HOSP'] = (orgStructureCode if orgStructureCode
                          else params['lpuCode'])
        #Сумма из средств Федеральных субвенций
        row['STOIM_S'] = eventSum
        row['SUB_HOSP'] = forceString(record.value('orgStructureInfis'))
        row['TOWN_HOSP'] = forceString(record.value(
            'orgStructureTfomsCode'))
        #Тип полиса: 1 – старого образца,
        # 2 – временное свидетельство 3 – нового образца
        row['TPOLIS'] = forceInt(record.value('policyKind'))
        #Коды ЛПУ приписки по справочнику фонда (стоматология)
        row['MASTER'] = params['attachOrgCode']
        # Результат обращения/ госпитализации
        row['RSLT'] = forceInt(record.value(
            'eventResultRegionalCode')) % 1000
        # Исход заболевания
        row['ISHOD'] = forceInt(record.value(
            'resultRegionalCode')) % 1000
        # Код врача, закрывшего талон/историю болезни
        row['P_CODE'] = formatSNILS(record.value('personSNILS'))
        row['FOR_POM'] = self.mapEventOrderToForPom.get(forceInt(
                                 record.value('eventOrder')), 0) % 10
        row['VIDPOM'] = forceInt(record.value(
            'medicalAidKindRegionalCode')) % 10000
        row['VID_FIN'] = 1
        row['INV'] = 0
        row['IDSP'] = getIdsp(forceInt(record.value('medicalAidUnitCode')),
                              forceBool(record.value('isAttached')),
                              forceBool(record.value('isHomeVisit')))
        row['DS_ONK'] = 0
        row['C_ZAB'] = forceInt(record.value('C_ZAB')) % 10
        row['PURPOSE'] = forceString(record.value('purposeCode'))
        row['DOCDATE'] = pyDate(forceDate(record.value('DOCDATE')))
        row['DOCORG'] = forceString(record.value('DOCORG'))[:250]
        row['mpcod'] = forceString(record.value('orgStructMpCod'))[:8]
        row['addr_code'] = forceString(record.value('orgStructAddrCode'))[:16]

        row.store()


    def _processGuests(self, dbf, record, params):
        u"""Заполняет таблицу GUESTS.DBF"""

        row = dbf.newRecord()
        row['ID_TALON'] = forceString(params['eventId'])[:10]
         #Место рождения пациента или представителя
        row['MR'] = forceString(record.value('birthPlace'))[:100]
        locOKATO = forceString(record.value('locOKATO'))
        regOKATO = forceString(record.value('regOKATO'))

        if not locOKATO:
            locOKATO = regOKATO

        #Код места жительства по ОКАТО
        row['OKATOG'] = regOKATO
        #Код места пребывания по ОКАТО
        row['OKATOP'] = locOKATO
        row['OKATO_OMS'] = forceString(record.value('insurerOKATO'))
        #Код ОКАТО территории страхования по ОМС (по справочнику фонда)
        representativeInfo = self.getClientRepresentativeInfo(
                                                          params['clientId'])
        #Фамилия (представителя) пациента
        row['FAMP'] = representativeInfo.get('lastName', '')
        #Имя  (представителя) пациента
        row['IMP'] = representativeInfo.get('firstName', '')
        #Отчество родителя (представителя) пациента
        row['OTP'] = representativeInfo.get('patrName', '')
        #Дата рождения (представителя) пациента
        row['DRP'] = pyDate(representativeInfo.get(
            'birthDate', QDate()))
        #Пол  (представителя) пациента
        if representativeInfo.has_key('sex'):
            row['WP'] = '1' if representativeInfo['sex'] == 1 else '0'
        #Код типа документа, удостоверяющего личность
        #пациента (представителя) (по  справочнику фонда)
        row['C_DOC'] = forceInt(representativeInfo.get(
            'documentTypeRegionalCode', params['documentRegionalCode'])) % 100
        #Серия документа, удостоверяющего личность пациента
        #(представителя) (по справочнику фонда)

        documentSerial = representativeInfo.get('serial',
                                              params['documentSerial'])
        if row['C_DOC'] == 3:
            documentSerial = documentSerial.strip().replace(' ', '-')

        row['S_DOC'] = documentSerial
        #Номер документа, удостоверяющего личность пациента
        #(представителя) (справочник фонда)
        row['N_DOC'] = representativeInfo.get('number',
                                              params['documentNumber'])

        specialCase = []
        #Признак «Особый случай» при регистрации обращения
        #за медицинской помощью
        row['Q_G'] = ''.join(specialCase)
        row['MSE'] = 0
        row['DOCDATE'] = pyDate(forceDate(record.value('DOCDATE')))
        row['DOCORG'] = forceString(record.value('DOCORG'))[:250]

        row.store()


    def _processServices(self, dbf, record, params):
        u"""Заполняет таблицу SERVICES.DBF"""

        row = dbf.newRecord()
        eventId = params['eventId']
        actionDate = forceDate(record.value('actionDate'))
        row['ID_TALON'] = forceString(eventId)[:10]
        #Номер зуба по международной классификации
        actionId = forceRef(record.value('actionId'))
        toothNumber = self.toothNumber(actionId)
        row['TOOTH'] = toothNumber[:2]
        #Код диагноза
        row['DIAG'] = forceString(record.value('MKB'))[:6]
        #Код диагноза первичный
        row['DS0'] = forceString(record.value('MKB'))[:6]
        #Личный код  медицинского работника, оказавшего услугу
        row['P_CODE'] = formatSNILS(record.value('personSNILS'))[:14]
        #Код услуги
        row['ID_SERV'] = forceString(record.value('serviceCode'))
        #Дата оказания услуги
        row['SERV_DATE'] = pyDate(actionDate)
        #Кол-во услуг данного типа
        row['SERVNUMBER'] = forceInt(record.value('amount')) % 100
        #Сумма единиц трудозатрат услуг (УЕТ)
        row['UNITS_SUM'] = params['uet']
        row['ID_REESTR'] = params['registryId'][:10]  #Номер реестра
        #Сумма из средств Федеральных субвенций
        row['STOIM_S'] = params['sum']
        medicalAidProfile = forceInt(record.value(
            'medicalAidProfileRegionalCode'))
        row['PROFIL'] = (medicalAidProfile if medicalAidProfile else
                forceInt(record.value('eventMedicalAidProfileRegionalCode'))
            ) % 1000
        row['PRVS'] = forceInt(record.value(
            'actionPersonSpecialityFederalCode')) % 10000
        row['VID_FIN'] = 1
        purposeCode = forceString(record.value('purposeCode'))

        if purposeCode == u'301':
            firstVisitDate = self.firstVisit.get(eventId, QDate())

            if firstVisitDate and firstVisitDate < actionDate:
                purposeCode = u'302'
            else:
                self.firstVisit[eventId] = actionDate

        row['PURPOSE'] = purposeCode
        row['P_MODE'] = 16
        row['NPL'] = mapAcionStatusToNpl.get(
                forceInt(record.value('actionStatus')), 0)
        if row['NPL'] == 4 and actionDate >= params['begDate']:
            row['NPL'] = 0

        row['IDUSL'] = forceString(params['serviceNumber'])
        row['mpcod'] = forceString(record.value('orgStructMpCod'))[:8]
        row['addr_code'] = forceString(record.value('orgStructAddrCode'))[:16]
        row.store()

# ******************************************************************************

    def _processTooth(self, dbf, record, params):
        u"""Заполняет таблицу TOOTH.DBF"""

        (_, toothDbf, _, _, _, _) = dbf
        row = toothDbf.newRecord()
        _map = params['mapToothToVisitCount']

        row['ID_TALON'] = forceString(record.value('eventId'))[:10]
        #Номер зуба по международной классификации
        row['TOOTH'] = forceString(record.value('toothNumber'))[:2]
        #Код диагноза
        mkb = forceString(record.value('MKB'))
        row['DIAG'] = forceString(record.value('MKB'))[:6]
        #Код специальности медицинского работника, оказавшего услугу**
        row['SPEC'] = forceString(record.value(
                                           params['specialityCodeFieldName']))
        #Количество посещений по данному заболеванию
        key = (row['ID_TALON'], mkb, row['SPEC'], row['TOOTH'])
        row['VISITS'] = _map.get(key, 1)
        #Сумма единиц трудозатрат услуг (УЕТ)
        row['UNITS_SUM'] = forceDouble(record.value('uet'))
        #Номер реестра
        row['ID_REESTR'] = params['registryId']
        row['PRVS'] = forceInt(record.value('specialityFederalCode')) % 10000

        row.store()

# ******************************************************************************

    def _processSpeciality(self, dbf, record, params):
        u"""Заполняет таблицу SPEC_VIS.DBF"""

        (_, _, specVisDbf, _, _, _) = dbf
        _map = params['mapSpecToVisitCount']

        row = specVisDbf.newRecord()
        row['ID_TALON'] = forceString(record.value('eventId'))[:10]
        #Код специальности медицинского работника, оказавшего услугу
        row['SPEC'] = forceString(record.value(
                                        params['specialityCodeFieldName']))
        key = (row['ID_TALON'], row['SPEC'])
        row['VISITS'] = _map.get(key, 1)
        row['UNITS_SUM'] = forceDouble(record.value('uet'))
        #Номер реестра
        row['ID_REESTR'] = params['registryId']
        orgStructureCode = forceString(record.value(
            'orgStructureInfis')).strip()
        row['ID_HOSP'] = (orgStructureCode if orgStructureCode
            else params['lpuCode'])
        row['PRVS'] = forceInt(record.value('specialityFederalCode')) % 10000

        row.store()

# ******************************************************************************

class CExportPage2(CAbstractExportPage2):
    u"""Вторая страница мастера экспорта"""

    def __init__(self, parent):
        CAbstractExportPage2.__init__(self, parent, 'R51ST')


    def saveExportResults(self):
        for src in ('STREESTR.DBF', 'TOOTH.DBF', 'SPEC_VIS.DBF',
                        'SERVICES.DBF', 'GUESTS.DBF', 'NAPR.DBF'):
            srcFullName = os.path.join(forceStringEx(self.getTmpDir()), src)
            dst = os.path.join(forceStringEx(self.edtDir.text()), src)
            success, _ = QtGui.qApp.call(self,
                shutil.move, (srcFullName, dst))

            if not success:
                break

        return success

# ******************************************************************************

if __name__ == '__main__':
    #pylint: disable=wrong-import-position,ungrouped-imports
    from Exchange.Utils import testAccountExport
    #pylint: enable=wrong-import-position,ungrouped-imports
    testAccountExport(exportR51Stomatology, u'17-911', 'art_msch118_0710.ini',
                      [3828959,3828960,3828961,3828985,3829056,3829057])
