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

import os.path
import shutil

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature, QDate, QDir, SIGNAL

from library.database  import decorateString
from library.dbfpy.dbf import Dbf
from library.ICDUtils  import MKBwithoutSubclassification
from library.Utils     import calcAgeInDays, calcAgeInYears, calcAgeTuple, forceDate, forceDateTime, forceDouble, forceInt, forceRef, forceString, forceStringEx, formatSex, formatSNILS, getInfisCodes, nameCase, pyDate, toVariant, trim

from Accounting.ServiceDetailCache import CServiceDetailCache
from Accounting.Tariff import CTariff
from Exchange.Utils    import getClientRepresentativeInfo
from KLADR.KLADRModel  import getExactCityName, getRegionName, getStreetNameParts
from Registry.Utils    import getClientWork, formatWorkPlace, CCheckNetMixin

from Exchange.Ui_ExportINFISOMSPage1 import Ui_ExportINFISOMSPage1
from Exchange.Ui_ExportINFISOMSPage2 import Ui_ExportINFISOMSPage2


def getAccountInfo(accountId):
    db = QtGui.qApp.db
    accountRecord = db.getRecord('Account', 'date, number', accountId)
#            settleDate = forceDate(accountRecord.value('settleDate'))
    if accountRecord:
        date = forceDate(accountRecord.value('date'))
        number = forceString(accountRecord.value('number'))
    else:
        date = None
        number = ''
    return date, number, 'data'


def exportINFISOMS(widget, accountId, accountItemIdList):
    wizard = CExportINFISOMSWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.exec_()


class CExportINFISOMSWizard(QtGui.QWizard):
    def __init__(self, parent=None):
        QtGui.QWizard.__init__(self, parent)
        self.setWizardStyle(QtGui.QWizard.ModernStyle)
        self.page1 = CExportINFISOMSPage1(self)
        self.page2 = CExportINFISOMSPage2(self)
        self.addPage(self.page1)
        self.addPage(self.page2)
        self.setWindowTitle(u'Мастер экспорта в ИнФИС')
        self.dbfFileName = ''
        self.tmpDir = ''


    def setAccountId(self, accountId):
        self.accountId = accountId
        date,  number, fileName = getAccountInfo(accountId)
        self.dbfFileName = fileName
        strNumber = number if trim(number) else u'б/н'
        strDate = forceString(date) if date else u'б/д'
        self.page1.setTitle(u'Экспорт данных реестра по счёту №%s от %s' %(strNumber, strDate))
        self.page2.setTitle(u'Укажите директорий для сохранения обменного файла "%s.dbf"' %(self.dbfFileName))


    def setAccountExposeDate(self):
        db = QtGui.qApp.db
        accountRecord = db.table('Account').newRecord(['id', 'exposeDate'])
        accountRecord.setValue('id', toVariant(self.accountId))
        accountRecord.setValue('exposeDate', toVariant(QDate.currentDate()))
        db.updateRecord('Account', accountRecord)


    def getTmpDir(self):
        if not self.tmpDir:
            self.tmpDir = QtGui.qApp.getTmpDir('infisoms')
        return self.tmpDir


    def getFullDbfFileName(self):
        return os.path.join(self.getTmpDir(), self.dbfFileName + '.dbf')


    def setAccountItemsIdList(self, accountItemIdList):
        self.page1.setAccountItemsIdList(accountItemIdList)


    def cleanup(self):
        if self.tmpDir:
            QtGui.qApp.removeTmpDir(self.tmpDir)
            self.tmpDir = ''


    def exec_(self):
        QtGui.QWizard.exec_(self)
        self.cleanup()


class CExportINFISOMSPage1(QtGui.QWizardPage, Ui_ExportINFISOMSPage1, CCheckNetMixin):
    mapDocTypeToINFIS = { '1' : '1', '14': '2', '3':'3', '2':'6', '5':'7', '6':'9', '16':'8' }
    mapDocTypeToINFISName = {'1':u'ПАСПОРТ РОССИИ', '3':u'СВИД О РОЖД','14':u'ПАСПОРТ СССР', '9':u'ИНПАСПОРТ', '0':u'НЕТ ДОКУМЕНТА', \
                             '11':u'ВИД НА ЖИТЕЛЬ', None:u'др.док-т удост.личн.'}
    mapPolicyTypeToINFIS = {'1':u'т',  '2':u'п' }
    mapEventOrderToIDFORPOM = { 1: 3, 2:1,  3:3,  4:3,  5:3,  6:2 }

    def __init__(self, parent):
        QtGui.QWizardPage.__init__(self, parent)
        CCheckNetMixin.__init__(self)
        self.setupUi(self)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(1)
        self.progressBar.setText('')
        self.cmbRepresentativeOutRule.setCurrentIndex(forceInt(QtGui.qApp.preferences.appPrefs.get('INFISOMSRepresentativeOutRule', 1)))

        self.setTitle(u'Экспорт данных реестра по счёту')
        self.setSubTitle(u'для выполнения шага нажмите кнопку "экспорт"')

        self.setExportMode(False)
        self.aborted = False
        self.done = False
        self.idList = []
        self.tariffCache = {}
        self.connect(parent, SIGNAL('rejected()'), self.abort)
        self.serviceDetailCache = CServiceDetailCache()
        self.profileCache = {}
        self.profileSpecCache = {}
        self.kindCache = {}
        self.typeCache = {}
        self.representativeInfoCache = {}


    def setExportMode(self, flag):
        self.btnCancel.setEnabled(flag)
        self.btnExport.setEnabled(not flag)


    def setAccountItemsIdList(self, accountItemIdList):
        self.idList = accountItemIdList


    def prepareToExport(self):
        self.done = False
        self.aborted = False
        self.emit(SIGNAL('completeChanged()'))
        self.setExportMode(True)
        dbf = self.createDbf()
        query = self.createQuery()
        self.progressBar.setMaximum(max(query.size(), 1))
        self.progressBar.reset()
        self.progressBar.setValue(0)
        return dbf, query


    def export(self):
        QtGui.qApp.call(self, self.exportInt)
        self.setExportMode(False)
        if self.aborted:
            self.progressBar.setText(u'прервано')
        else:
            self.progressBar.setText(u'готово')
            self.done = True
            self.emit(SIGNAL('completeChanged()'))


    def exportInt(self):
        orgInfisCode = forceString(QtGui.qApp.db.translate('Organisation', 'id', QtGui.qApp.currentOrgId(), 'infisCode'))
        representativeOutRule = self.cmbRepresentativeOutRule.currentIndex()
        mapCPDToIndex = {}
        dbf, query = self.prepareToExport()
        if self.idList:
            while query.next():
                QtGui.qApp.processEvents()
                if self.aborted:
                    break
                self.progressBar.step()
                self.process(dbf, query.record(), orgInfisCode, representativeOutRule, mapCPDToIndex)
        else:
            self.progressBar.step()
        dbf.close()


    def createDbf(self):
        dbf = Dbf(self.wizard().getFullDbfFileName(), new=True, encoding='cp866')
        dbf.addField(
                        ('RECIEVER','C',5),     # ИНФИС код подразделения
                        ('PAYER','C',5),        # Код СМО, выдавшей полис
                        ('TMO','C',5),          # Код ЛПУ
                        ('SURNAME','C',18),     # Фамилия пациента
                        ('NAME1','C',15),       # Имя пациента
                        ('NAME2','C',15),       # Отчество пациента
                        ('SEX','C',1),          # Пол (М/Ж)
                        ('AGE','N',3,0),        # Возраст (на какую дату?)
                        ('HSNET','C',1),        # "в"-взрослая/"д"-детская/"ж"-женская
                        ('STREET','C',5),       # Адрес пациента: код улицы
                        ('STREETYPE','C',2),    # Адрес пациента: тип улицы
                        ('AREA','C',3),         # Адрес пациента: код районa
                        ('HOUSE','C',7),        # Адрес пациента: номер дома
                        ('KORP','C',2),         # Адрес пациента: корпус
                        ('FLAT','N',4,0),       # Адрес пациента: номер квартиры
                        ('WHO','C',5),          # ИНФИС-код базового ЛПУ
                        ('ORDER','C',1),        # Код порядка направления
                        ('HSOBJECT','C',5),     # ИНФИС-код подразделения
                        ('DEPART','N',2,0),     # "внутренний код отделения"
                        ('PROFILENET','C',1),   # "в"-взрослая/"д"-детская
                        ('PROFILE','C',6),      # Код профиля лечения, код услуги, "ДСтац"
                        ('COMPLEXITY','C',1),   # -
                        ('DATEIN','D'),         # Дата начала услуги
                        ('DATEOUT','D'),        # Дата окончания услуги
                        ('AMOUNT','N',5,1),     # Объем лечения
                        ('OUTCOME','C',1),      # "код исхода лечения" ("в")
                        ('DIAGNOSIS','C',5),    # Код диагноза
                        ('DIAGNPREV','C',5),    # Код диагноза
                        ('HISTORY','C',9),      # eventId
                        ('REMARK','M'),         # !!!
#                        ('REMARK','C', 200),    #
                        ('BIRTHDAY','D'),       # Дата рождения
                        ('SUM','N',11,2),       # Сумма
                        ('CARDFLAGS','N',4,0),  # -
                        ('PROFTYPE','C',1),     # "код типа отделения" ("д")
                        ('POLIS_S','C',10),     # Серия полиса
                        ('POLIS_N','C',20),     # Номер полиса
                        ('POLIS_W','C',5),      # Код СМО, выдавшей полис
                        ('PIN','C',15),         # -
                        ('CARD_ID','C',8),      # -
                        ('INSURE_ID','C',8),    # -
                        ('INSURE_LOG','C',8),   # -
                        ('TYPER','C',1),        # -
                        ('IDQ','C',15),         # -
                        ('DATEQ','D'),          # -
                        ('TYPEQ','C',1),        # -
                        ('DATEREAL','D'),       # -
                        ('TYPEINS','C',1),      # - тип страхования (т - терр., п - произв.)
                        ('DATER','D'),          # -
                        ('TGROUP','C',2),       # Признак превышения предела количества по тарифу
                        ('SEND','L'),           # Флаг обработки записи
                        ('ERROR','C',15),       # Описание ошибки
                        ('TYPEDOC','C',1),      # Тип документа
                        ('SER1','C',10),        # Серия документа, левая часть
                        ('SER2','C',10),        # Серия документа, правая часть
                        ('NPASP','C',10),       # Номер документа
                        ('CHK','C',10),         #
                        ('ORDER_A','C', 1),     #
                        ('PROF79', 'C', 3),     # профиль лечения по классификатору профилей по 79 приказу
                        ('PRVS79', 'C', 6),     # код специальности врача по 79 приказу
                        ('VPOLIS', 'C', 1),     # вид полиса, региональный код
                        ('W_P',    'C', 1),     # пол представителя ребенка
                        ('DR_P',   'D', 8),     # день рождения представителя ребенка
                        ('SNILS',  'C', 14),    # СНИЛС
                        ('DS2',    'C', 5),     # диагноз сопутствующий
                        ('VIDPOM', 'C', 1),     # виды медицинской помощи (По умолчанию - 1, 2 - для событий с типом мед помощи 4 и 5, 3 - для Событий с типом мед.помощи 2 и 3)
                        ('RSLT',   'C', 3),     # результат обращения (Результат Обращения /События/: Региональный код)
                        ('IDSP',   'C', 3),     # способы оплаты медицинской помощи
                        ('MR',     'C', 100),   # место рождения
# ######### наши доп.поля:
                        ('ACC_ID',    'N',15,0),# id счета
                        ('ACCITEM_ID','N',15,0),# id элемента счета
                        ('CLIENT_ID', 'N',15,0),# id пациента
                        ('EVENT_ID',  'N',15,0),# id события
                        ('EXTERNALID','C',64),  # externalId события
                    )
        return dbf

    def createQuery(self):
        db = QtGui.qApp.db
        tableAccountItem = db.table('Account_Item')

        stmt = """
            SELECT
              Account_Item.id        AS accountItem_id,
              Account_Item.master_id AS account_id,
              Account_Item.event_id  AS event_id,
              Account_Item.action_id AS action_id,
              Action.begDate         AS actionBegDate,
              Action.endDate         AS actionEndDate,
              Account_Item.visit_id  AS visit_id,
              Visit.date             AS visitDate,
              Event.client_id        AS client_id,
              Event.externalId       AS externalId,
              Event.`order`          AS `order`,
              rbMedicalAidKind.code  AS medicalAidKindCode,
              rbMedicalAidType.code  AS medicalAidTypeCode,
              Client.lastName        AS lastName,
              Client.firstName       AS firstName,
              Client.patrName        AS patrName,
              Client.birthDate       AS birthDate,
              Client.sex             AS sex,
              Client.SNILS           AS SNILS,
              Client.birthPlace      AS birthPlace,
              ClientPolicy.serial    AS policySerial,
              ClientPolicy.number    AS policyNumber,
              ClientPolicy.begDate   AS policyBegDate,
              ClientPolicy.endDate   AS policyEndDate,
              Insurer.infisCode      AS policyInsurer,
              Insurer.fullName       AS policyInsurerName,
              Insurer.area           AS policyInsurerArea,
              rbPolicyType.code      AS policyType,
              rbPolicyKind.regionalCode AS policyKind,
              ClientDocument.serial  AS documentSerial,
              ClientDocument.number  AS documentNumber,
              rbDocumentType.code    AS documentType,
              rbDocumentType.regionalCode AS documentRegionalCode,
              AddressHouse.KLADRCode AS KLADRCode,
              AddressHouse.KLADRStreetCode AS KLADRStreetCode,
              AddressHouse.number    AS number,
              AddressHouse.corpus    AS corpus,
              Address.flat           AS flat,
              formatClientAddress(ClientAddress.id) as freeInput,
              getClientCitizenship(Client.id, Event.setDate) as citizenship,
              IF(Account_Item.service_id IS NOT NULL,
                rbItemService.id,
                IF(Account_Item.visit_id IS NOT NULL, rbVisitService.id, rbEventService.id)
                ) AS service_id,
              Diagnosis.MKB          AS MKB,
              MKB.Prim               AS prim,
              Action.MKB            AS ActionMKB,
              Event.setDate          AS begDate,
              Event.execDate         AS endDate,
              Event.relegateOrg_id   AS relegateOrgId,
              IF(Event.relegateOrg_id IS NOT NULL, (SELECT Org.infisCode FROM Organisation AS Org WHERE Org.deleted = 0 AND Org.id = Event.relegateOrg_id LIMIT 1), NULL) AS relegateOrgInfisCode,
              IF(Event.client_id IS NOT NULL, %s, NULL) AS attachInfisCode,
              Event.note as note,
              Account_Item.amount    AS amount,
              Account_Item.`sum`     AS `sum`,
              Account_Item.tariff_id AS tariff_id,
              rbMedicalAidUnit.regionalCode AS unitCode,
              rbDiagnosticResult.federalCode  AS diagnosticResultFederalCode,
              EventResult.federalCode AS eventResultFederalCode,
              OrgStructure.infisCode,
              OrgStructure.infisInternalCode,
              OrgStructure.infisDepTypeCode,
              OrgStructure.infisTariffCode,
              Person.id              AS person_id,
              rbSpeciality.id        AS speciality_id,
              rbSpeciality.OKSOCode  AS OKSOCode,
              rbSpeciality.federalCode  AS specialityFederalCode,
              Contract_Tariff.frag2Start AS tariffBorder
            FROM Account_Item
            LEFT JOIN Account ON Account.id = Account_Item.master_id
            LEFT JOIN Contract ON Contract.id = Account.contract_id
            LEFT JOIN rbFinance ON rbFinance.id = Contract.finance_id
            LEFT JOIN Action ON Action.id = Account_Item.action_id
            LEFT JOIN Visit  ON Visit.id  = Account_Item.visit_id
            LEFT JOIN Event  ON Event.id  = Account_Item.event_id
            LEFT JOIN Client ON Client.id = Event.client_id
            LEFT JOIN ClientPolicy ON ClientPolicy.id = getClientPolicyId(Client.id, rbFinance.code != '3')
            LEFT JOIN Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
            LEFT JOIN rbPolicyType ON rbPolicyType.id = ClientPolicy.policyType_id
            LEFT JOIN rbPolicyKind ON rbPolicyKind.id = ClientPolicy.policyKind_id
            LEFT JOIN ClientDocument ON ClientDocument.client_id = Client.id AND
                      ClientDocument.id = (SELECT MAX(CD.id)
                                         FROM   ClientDocument AS CD
                                         LEFT JOIN rbDocumentType AS rbDT ON rbDT.id = CD.documentType_id
                                         LEFT JOIN rbDocumentTypeGroup AS rbDTG ON rbDTG.id = rbDT.group_id
                                         WHERE  rbDTG.code = '1' AND CD.client_id = Client.id)
            LEFT JOIN rbDocumentType ON rbDocumentType.id = ClientDocument.documentType_id
            LEFT JOIN ClientAddress ON ClientAddress.client_id = Client.id AND
                      ClientAddress.id = (SELECT MAX(CA.id)
                                         FROM   ClientAddress AS CA
                                         WHERE  CA.type = 0 AND CA.client_id = Client.id)
            LEFT JOIN Address      ON Address.id = ClientAddress.address_id
            LEFT JOIN AddressHouse ON AddressHouse.id = Address.house_id
            LEFT JOIN Person       ON Person.id = IF(Visit.person_id IS NOT NULL, Visit.person_id,
                                                     IF(Action.person_id IS NOT NULL, Action.person_id, Event.execPerson_id))

            LEFT JOIN Diagnostic ON Diagnostic.id = getEventDiagnostic(Event.id)
            LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id
            LEFT JOIN MKB       ON MKB.DiagID = Diagnosis.MKB
            LEFT JOIN rbDiagnosticResult ON rbDiagnosticResult.id=Diagnostic.result_id
            LEFT JOIN rbResult AS EventResult ON EventResult.id=Event.result_id
            LEFT JOIN EventType ON EventType.id = Event.eventType_id
            LEFT JOIN rbMedicalAidKind ON rbMedicalAidKind.id = EventType.medicalAidKind_id
            LEFT JOIN rbMedicalAidType ON rbMedicalAidType.id = EventType.medicalAidType_id
            LEFT JOIN rbService AS rbEventService ON rbEventService.id = EventType.service_id
            LEFT JOIN rbService AS rbVisitService ON rbVisitService.id = Visit.service_id
            LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
            LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
            LEFT JOIN OrgStructure ON OrgStructure.id = Person.orgStructure_id
            LEFT JOIN rbSpeciality ON rbSpeciality.id = Person.speciality_id
            LEFT JOIN rbService AS rbItemService ON rbItemService.id = Account_Item.service_id
            LEFT JOIN Contract_Tariff ON Contract_Tariff.id = Account_Item.tariff_id
            LEFT JOIN rbMedicalAidUnit ON rbMedicalAidUnit.id = Contract_Tariff.unit_id
            WHERE
                Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s
            ORDER BY Client.lastName, Client.firstName, Client.patrName, Client.birthDate, Client.id
        """ % (self.getClientAttach(), tableAccountItem['id'].inlist(self.idList))
        query = db.query(stmt)
        return query


    def getClientAttach(self):
        return u'''(SELECT OrgAttach.infisCode
                    FROM Organisation AS OrgAttach
                    INNER JOIN ClientAttach ON ClientAttach.LPU_id = OrgAttach.id
                    INNER JOIN rbAttachType ON rbAttachType.id = ClientAttach.attachType_id
                    WHERE OrgAttach.deleted = 0
                    AND ClientAttach.deleted = 0
                    AND ClientAttach.client_id = Event.client_id
                    AND (rbAttachType.code = 1 OR rbAttachType.code = 2)
                    AND
                    ((Event.setDate IS NULL AND Event.execDate IS NULL)
                    OR
                    (ClientAttach.begDate IS NULL AND ClientAttach.endDate IS NULL)
                    OR
                    (Event.setDate IS NOT NULL
                    AND (
                    (ClientAttach.begDate IS NOT NULL AND ClientAttach.endDate IS NOT NULL
                    AND ((ClientAttach.begDate <= DATE(Event.setDate) AND ClientAttach.endDate > DATE(Event.setDate))
                    OR (ClientAttach.begDate >= DATE(Event.setDate) AND (Event.execDate IS NULL OR ClientAttach.begDate < DATE(Event.execDate)))))
                    OR (ClientAttach.begDate IS NOT NULL AND ClientAttach.endDate IS NULL
                    AND (Event.execDate IS NULL OR ClientAttach.begDate < DATE(Event.execDate)))
                    OR (ClientAttach.begDate IS NULL AND ClientAttach.endDate IS NOT NULL
                    AND (ClientAttach.endDate > DATE(Event.setDate)))
                    ))
                    OR
                    (Event.execDate IS NOT NULL
                    AND (
                    (ClientAttach.begDate IS NOT NULL AND ClientAttach.endDate IS NOT NULL
                    AND (((Event.setDate IS NULL OR ClientAttach.begDate <= DATE(Event.setDate)) AND ClientAttach.begDate < DATE(Event.execDate))
                    OR ((Event.setDate IS NULL OR ClientAttach.begDate >= DATE(Event.setDate)) AND (ClientAttach.begDate < DATE(Event.execDate)))))
                    OR (ClientAttach.begDate IS NOT NULL AND ClientAttach.endDate IS NULL AND ClientAttach.begDate < DATE(Event.execDate))
                    OR (ClientAttach.begDate IS NULL AND ClientAttach.endDate IS NOT NULL
                    AND (Event.setDate IS NULL OR ClientAttach.endDate > DATE(Event.setDate)))
                    )))
                    ORDER BY rbAttachType.code
                    LIMIT 1)'''


    def process(self, dbf, record, orgInfisCode, representativeOutRule, mapCPDToIndex):
        eventId  = forceInt(record.value('event_id'))
        actionId = forceRef(record.value('action_id'))
        visitId = forceRef(record.value('visit_id'))
        externalId = forceString(record.value('externalId'))
        clientId = forceInt(record.value('client_id'))
        birthDate = forceDate(record.value('birthDate'))
        if actionId is None:
            begDate = forceDate(record.value('begDate'))
            endDate = forceDate(record.value('endDate'))
        else:
            begDate = forceDate(record.value('actionBegDate'))
            endDate = forceDate(record.value('actionEndDate'))
#        relegateOrgId = forceRef(record.value('relegateOrgId'))
        relegateOrgInfisCode = forceString(record.value('relegateOrgInfisCode'))
        attachInfisCode = forceString(record.value('attachInfisCode'))
        sex = forceInt(record.value('sex'))
        age = max(0, calcAgeInYears(birthDate, endDate))
        if age<18:
            net = u'д'
        else:
            personId = forceRef(record.value('person_id'))
            net = self.getPersonNet(personId)
            net = u'ж' if net and net.sex == 2 else u'в'
        diagnosis = MKBwithoutSubclassification(forceString(record.value('ActionMKB')))
        if not diagnosis:
            diagnosis = MKBwithoutSubclassification(forceString(record.value('MKB')))
        if len(diagnosis) == 3:
            diagnosis += '.'
        preliminaryDiagnosis = diagnosis
        specialityId = forceRef(record.value('speciality_id'))
        serviceId = forceRef(record.value('service_id'))
        serviceDetail = self.serviceDetailCache.get(serviceId)
        eventAidKindCode = forceString(record.value('medicalAidKindCode'))
        eventAidTypeCode = forceString(record.value('medicalAidTypeCode'))
        aidProfileRegionalCode, aidProfileFederalCode, serviceAidKindCode, serviceAidTypeCode = self.getAidCodes(serviceDetail, endDate, specialityId, birthDate, sex, diagnosis)
        aidKindCode = serviceAidKindCode or eventAidKindCode
        aidTypeCode = serviceAidTypeCode or eventAidTypeCode
        orgStructureInfisCode = forceString(record.value('infisCode'))
        infisTariffCode = forceString(record.value('infisTariffCode'))
        infisInternalCode = forceInt(record.value('infisInternalCode'))
        proftype = forceStringEx(record.value('infisDepTypeCode'))
        resultCode = forceString(record.value('eventResultFederalCode'))
        prvs79 = forceString(record.value('specialityFederalCode'))
        eventOrder = forceInt(record.value('order'))
        idforpom = self.mapEventOrderToIDFORPOM.get(eventOrder, 3)
        outcome = u'в'
        if not actionId and not visitId:
            if resultCode == u'102':
                outcome = u'п'
            elif resultCode == u'104':
                outcome = u'о'
            elif resultCode == u'105':
                outcome = u'у'
        note = forceString(record.value('note'))
        if not proftype:
            proftype = u'у'
        complexity = ''
        if aidTypeCode in ('1', '2', '3'): # услуги стационара
            dateTime = None
            if actionId:
                dateTime = forceDateTime(record.value('actionEndDate'))
                endDate = forceDate(record.value('endDate')) # действия просят предъявлять к оплате последним днём события
            elif visitId:
                dateTime = forceDateTime(record.value('visitDate'))
            (orgStructureInfisCode,
             infisTariffCode,
             infisInternalCode,
             proftype) = self.getOrgStructureDetailsForHospital(eventId, dateTime)

        amount =  forceDouble(record.value('amount'))
        sum = forceDouble(record.value('sum'))

        tariffBorder = forceDouble(record.value('tariffBorder'))
        if self.cbCardflag.isChecked() and tariffBorder < amount:
            cardflag = forceInt(self.edtCardflag.text())
        else:
            cardflag = 0

        renunciate = self.findRenunciate(eventId)

        # велено "склеивать" записи, у которых одинаковые пациент-профиль-дата, см.
        # «0005408: Особенности выгрузки в ИНФИС однопрофильный услуг,
        #           оказанных пациенту в один и тот же день»
        # очевидно, что кое-что из предыдущего кода окажется ненужным, но
        # я не готов всерьёз разделять - что повлияет на c-p-d, а что - нет
        # .toJulianDay() - это потому, что использование QDate в качестве ключа невозможно.
        # годится любая функция для которой f(date1) != f(date2) при date1 != date2
        cpdKey = (clientId, serviceDetail.infisCode, endDate.toJulianDay(), specialityId, diagnosis)
        index = mapCPDToIndex.get(cpdKey)
        if index is not None:
            dbfRecord = dbf[index]
            dbfRecord['AMOUNT']  = dbfRecord['AMOUNT'] + amount # Объем лечения
            dbfRecord['SUM']     = dbfRecord['SUM'] + sum       # Сумма
            dbfRecord.store()
            return

        if aidTypeCode in ('1', '2', '3'): # услуги стационара
            aidProfileTuple = None
            if actionId is None and visitId is None:
                complexity, preliminaryDiagnosis = self.getComplexityAndPreliminaryDiagnosis(eventId)
                if not preliminaryDiagnosis:
                    preliminaryDiagnosis = diagnosis
                aidProfileTuple = self.getProfileCodesForEvent(eventId, dateTime)
            elif serviceDetail.infisCode == u'уПЛсР':
                aidProfileTuple = self.getProfileCodesForEvent(eventId, dateTime)
                prvs79 = self.getEventPersonSpeciality(eventId)
            if aidProfileTuple:
                aidProfileRegionalCode, aidProfileFederalCode = aidProfileTuple

        policyBegDate = forceDate(record.value('policyBegDate'))
        policyEndDate = forceDate(record.value('policyEndDate'))
        policyInsurer = forceString(record.value('policyInsurer'))
        policyInsurerArea = forceString(record.value('policyInsurerArea'))
        policyInsurerAreaIsSpb = policyInsurerArea.startswith('78') or not policyInsurerArea
        number = forceString(record.value('number'))
        KLADRCode = forceString(record.value('KLADRCode'))
        KLADRStreetCode = forceString(record.value('KLADRStreetCode'))
        corpus = forceString(record.value('corpus'))
        area, region, npunkt, street, streettype = getInfisCodes(KLADRCode, KLADRStreetCode, number, corpus)
        citizenship = forceString(record.value('citizenship'))
        if citizenship == u'м643': # Россия
            citizenship = ''
        if citizenship:
            payer = u'иКом'
            tmo   = u'ИН'
        elif policyInsurerAreaIsSpb:
            payer = policyInsurer
            tmo   = self.getTMO(street, number) #(attachInfisCode or orgInfisCode)
            if not tmo:
                tmo = attachInfisCode or orgInfisCode
        else:
            payer = tmo = u'кФонд'
        docType   = forceString(record.value('documentType'))
        if not docType:
            docType = '0'
        documentRegionalCode = forceString(record.value('documentRegionalCode'))
        docSerial = forceStringEx(record.value('documentSerial'))
        docNumber = forceString(record.value('documentNumber'))
        flat   = forceString(record.value('flat'))
        freeInput = forceString(record.value('freeInput'))
        if area == u'ЛО':
            area = u'Ф89' # ?
        if citizenship:
            area = region = forceString(QtGui.qApp.db.translate('rbSocStatusType', 'code', citizenship, 'regionalCode'))
        clientWork = getClientWork(clientId)
        # представитель нужен для ребёнка-без паспорта-при подходящем условии:
        representativeInfo = ( self.getClientRepresentativeInfo(clientId)
                               if age<18             # ребёнок
                                  and docType != '1' # или представлен не паспорт
                                  and (   representativeOutRule == 0
                                       or representativeOutRule == 1 and street == '*'
                                       or representativeOutRule == 2 and payer != u'кФонд' and payer != u'иКом'
                                      )
                               else None
                             )
        docText = ''
        if representativeInfo:
            popDocType = representativeInfo['documentTypeCode']
            popDocSerial = representativeInfo['serial']
            popDocNumber = representativeInfo['number']
            if docType == '3':
                seri = docSerial.split()
                if len(seri) > 1:
                    docSerial = u'%s-%s'%(seri[0], seri[1])
                docText = u'свид о рожд %s №%s' %(docSerial, docNumber)
            if docType == '24':
                seri = docSerial.split()
                if len(seri) > 1:
                    docSerial = u'%s-%s'%(seri[0], seri[1])
                docText = u'свид о рожд не рф %s №%s' %(docSerial, docNumber)
        else:
            popDocType = docType
            popDocSerial = docSerial
            popDocNumber = docNumber
        if popDocType in ('3','14'): # это плохое решение, но для хорошего нужно гораздо больше хлопот...
            popDocSerial = '-'.join(popDocSerial.split(' ', 1))

        memoList = ['%s\x11[DOPCARD]'%note,
                            'SER_TYPE='+self.mapDocTypeToINFISName.get(popDocType, self.mapDocTypeToINFISName[None]),
                            'PASPORT_S='+popDocSerial,
                            'PASPORT_N='+popDocNumber,
                            'WorkType='+(u'Работ' if clientWork and age>=18 else u'НеРаб'),
                            'CodeCompany='+policyInsurer,
                            'Snils='+formatSNILS(forceString(record.value('SNILS'))),
                            'Vpolis='+(forceString(record.value('policyKind')) or ''),
                    ]

        if renunciate:
            memoList.insert(0, u'отказ от госпитализации')
        if docText:
            memoList.insert(0, docText)

        if policyBegDate:
            memoList.append('Pol_begin='+unicode(policyBegDate.toString('dd.MM.yyyy')))
        if policyEndDate:
            memoList.append('Pol_end='+unicode(policyEndDate.toString('dd.MM.yyyy')))

        if representativeInfo:
            memoList.append('_mtrpar_=Y')
            memoList.append('Parstatus='+representativeInfo['status'])
            memoList.append('W_p='+formatSex(representativeInfo['sex']).lower())
            memoList.append('Dr_p='+unicode(representativeInfo['birthDate'].toString('dd.MM.yy')))
            memoList.append('Parsurname='+representativeInfo['lastName'])
            memoList.append('Parname1='+representativeInfo['firstName'])
            memoList.append('Parname2='+representativeInfo['patrName'])
            memoList.append('Parname='+representativeInfo['lastName'] + ' '+ representativeInfo['firstName']+' '+representativeInfo['patrName'])
        else:
            memoList.append(u'Parstatus=Отсутствует')

        ageDays = max(0, calcAgeInDays(birthDate, endDate))
        if ageDays < 28:
            patStatus = u'Новорожденный'
        elif age<=6:
            patStatus = u'Дошкольник'
        elif age<=13:
            patStatus = u'Ребенок до 14 лет'
        elif age<=17:
            patStatus = u'Студент/учащийся'
        else:
            patStatus = ''
        if clientWork:
            post = forceString(clientWork.value('post')).lower()
            if u'студ' in post or u'учащ' in post:
                patStatus = u'Студент/учащийся'
        if patStatus:
            memoList.append('patStatus='+patStatus)
        if clientWork:
            memoList.append('Job='+formatWorkPlace(clientWork))
        memoList.append('Mr='+forceString(record.value('birthPlace')))
        if street == '*':
            if not policyInsurerAreaIsSpb:
                memoList.append('_mtr_=Y')
                infisAreaInsure = forceString(QtGui.qApp.db.translate('kladr.KLADR', 'CODE', policyInsurerArea[:2]+'0'*11, 'infis'))
                memoList.append('AreaInsure='+(infisAreaInsure or area))
            memoList.append('Company='+forceString(record.value('policyInsurerName')))
            memoList.append('Region='+region)
            memoList.append('MTRegion='+getRegionName(KLADRCode))
            memoList.append('F_Placename='+getExactCityName(KLADRCode))
            if KLADRStreetCode:
                streetName, streetType = getStreetNameParts(KLADRStreetCode)
            else:
                streetName = streetType = ''
            memoList.append('F_Street='+(streetName or '-'))
            memoList.append('F_Streetype='+(streetType or '-'))
            memoList.append('F_House='+(number or '-'))
            memoList.append('F_Korp='+(corpus or '-'))
            memoList.append('F_Flat='+(flat or '-'))
#            address = ' '.join(ai
#                               for ai in (streetType, streetName,
#                                          (u'д.'+number) if number else '',
#                                          (u'к.'+corpus) if corpus else '',
#                                          (u'кв.'+flat) if flat else ''
#                                         ) if ai
#                              )
            memoList.append('F_Address='+freeInput)

            OKSOCode = forceString(record.value('OKSOCode'))
            memoList.append('MedSpec='+OKSOCode.lstrip('0'))
            memoList.append('MTRProf='+aidProfileRegionalCode)
        if citizenship:
            memoList.append('Country='+forceString(QtGui.qApp.db.translate('rbSocStatusType', 'code', citizenship, 'name')))
        memoList.append('Vidpom='+aidKindCode)
        memoList.append('Rslt='+resultCode)
        memoList.append('Idsp='+forceString(record.value('unitCode')))
        memoList.append('Prof79='+aidProfileFederalCode)
        memoList.append('Prvs79='+prvs79)
        memoList.append('Ishod='+forceString(record.value('diagnosticResultFederalCode')))
        memoList.append('MTRPOLIS_S='+ forceString(record.value('policySerial')))
        memoList.append('MTRPOLIS_N='+ forceString(record.value('policyNumber')))
        memoList.append('Pr_nov=0')
        serviceInfisCode = serviceDetail.infisCode
#        memoList.append('Typecrd=%d' % (0 if len(serviceInfisCode)>=2 # см. #0003973 в мантисе.
#                                             and serviceInfisCode[:2].isalpha()
#                                             and serviceInfisCode[0].islower() # а про то - русские это буквы или нет речи не шло.
#                                             and serviceInfisCode[1].isupper()
#                                          else
#                                        1
#                                       )
#                       )
        memoList.append('Typecrd=%d' % (0 if (actionId or visitId) # см. #0005567 в мантисе.
                                          else
                                        1
                                       )
                       )
        if len(serviceInfisCode) > 1:
            if serviceInfisCode[:2] == '43':
                infisInternalCode = 14
        memoList.append('crim=0')
        memoList.append('Forpom="%i"'%idforpom)
        memoList.append('\x1A\x1A')
        memo = '\r\n'.join(memoList)

        dbfRecord = dbf.newRecord()

        dbfRecord['RECIEVER']= orgStructureInfisCode or orgInfisCode # ИНФИС код подразделения
#        dbfRecord['RECIEVER']= forceString(record.value('infisInternalCode'))  # Код подразделения
        #dbfRecord['PAYER']   = policyInsurer if policyInsurerAreaIsSpb else u'кФонд'  # Код СМО, выдавшей полис
        dbfRecord['PAYER']   = payer
        #dbfRecord['TMO']     = (attachInfisCode or orgInfisCode) if policyInsurerAreaIsSpb else u'кФонд' # ИНФИС-код организации прикрепления, если нет, то ИНФИС-код базового ЛПУ
        dbfRecord['TMO'] = tmo
        dbfRecord['SURNAME'] = nameCase(forceString(record.value('lastName')))  # Фамилия пациента
        dbfRecord['NAME1']   = nameCase(forceString(record.value('firstName'))) # Имя пациента
        dbfRecord['NAME2']   = nameCase(forceString(record.value('patrName')))  # Отчество пациента
        dbfRecord['SEX']     = formatSex(sex).lower()                           # Пол (м/ж)
        dbfRecord['AGE']     = age                                              # Возраст (на какую дату?)
        dbfRecord['BIRTHDAY']= pyDate(birthDate)                                # дата рождения
        dbfRecord['SNILS']   = formatSNILS(forceString(record.value('SNILS')))  # СНИЛС
        dbfRecord['MR']      = forceString(record.value('birthPlace'))          # место рождения
        dbfRecord['STREET']  = street                                           # Адрес пациента: код улицы
        dbfRecord['STREETYPE']= streettype if street != '*' else u''            # Адрес пациента: тип улицы
        dbfRecord['AREA']    = area                                             # Адрес пациента: код районa
        dbfRecord['HOUSE']   = number if street != '*' else u''                 # Адрес пациента: номер дома
        dbfRecord['KORP']    = corpus if street != '*' else u''                 # Адрес пациента: корпус
        dbfRecord['FLAT']    = forceInt(record.value('flat')) if street != '*' else 0 # Адрес пациента: номер квартиры
        dbfRecord['TYPEDOC'] = documentRegionalCode if documentRegionalCode else self.mapDocTypeToINFIS.get(docType, '5') # Тип документа
        docSeries = docSerial.split()
        dbfRecord['SER1']    = docSeries[0] if len(docSeries)>=1 else '' # Серия документа, левая часть
        dbfRecord['SER2']    = docSeries[1] if len(docSeries)>=2 else '' # Серия документа, правая часть
        dbfRecord['NPASP']   = docNumber # Номер документа
        dbfRecord['POLIS_S'] = forceString(record.value('policySerial'))      # Серия полиса
        dbfRecord['POLIS_N'] = forceString(record.value('policyNumber'))      # Номер полиса
        dbfRecord['POLIS_W'] = policyInsurer if policyInsurerAreaIsSpb else u'Проч' # Код СМО, выдавшей полис
        dbfRecord['TYPEINS'] = self.mapPolicyTypeToINFIS.get(forceString(record.value('policyType')), '')
        dbfRecord['VPOLIS']  = forceString(record.value('policyKind')) or ''
        dbfRecord['HSNET']   = net                                              # Тип сети профиля (в - взрослая, д - детская)
        dbfRecord['WHO']     = relegateOrgInfisCode or orgInfisCode # ИНФИС-код организации направителя, если нет, то ИНФИС-код базового ЛПУ
        dbfRecord['ORDER']   = u'э' if forceInt(record.value('order')) == 2 else u'п'  # Признак экстренности случая лечения (если случай экстренный - принимает значение "э" или "Э")
        dbfRecord['HSOBJECT']= infisTariffCode    # ИНФИС-код подразделения
        dbfRecord['DEPART']  = infisInternalCode  # "внутренний код отделения"
        dbfRecord['PROFILENET'] = net             # Тип сети профиля (в - взрослая, д - детская)
        dbfRecord['PROFILE'] = serviceDetail.infisCode # Код профиля лечения, код услуги, "ДСтац"
        dbfRecord['COMPLEXITY'] = complexity
        if proftype != u'п' and not actionId: # типа в приёмном отделении ненужно указывать DATEIN
            dbfRecord['DATEIN']  = pyDate(begDate)    # Дата начала услуги
        dbfRecord['DATEOUT'] = pyDate(endDate)    # Дата окончания услуги
        dbfRecord['AMOUNT']  = amount             # Объем лечения
        dbfRecord['SUM']     = sum                # Сумма
        dbfRecord['OUTCOME']   = outcome            # "код исхода лечения" ("в")
        dbfRecord['DIAGNOSIS'] = diagnosis              # Код диагноза
        if proftype != u'п' and not actionId: # типа в приёмном отделении ненужно указывать DIAGNPREV
            dbfRecord['DIAGNPREV'] = preliminaryDiagnosis # Код диагноза
        dbfRecord['VIDPOM']    = aidKindCode
        dbfRecord['PROF79']    = aidProfileFederalCode
        dbfRecord['PRVS79']    = forceString(record.value('specialityFederalCode'))
        dbfRecord['RSLT']      = forceString(record.value('eventResultFederalCode'))
        dbfRecord['IDSP']      = forceString(record.value('unitCode'))
        dbfRecord['REMARK']    = memo
        dbfRecord['PROFTYPE']  = proftype              # "код типа отделения" ("д")
        if actionId: # попрошено услуги приёмного отденения выставлять с другим кодом. Upd, все услуги выставлять как с
            dbfRecord['PROFTYPE']  = u'с'
        dbfRecord['TGROUP']    = self.getTariffGroup(record) # Признак превышения предела количества по тарифу
        dbfRecord['HISTORY']   = externalId          # eventId
        dbfRecord['SEND']      = False                 # Флаг обработки записи
        dbfRecord['ERROR']     = ''                    # Описание ошибки
#
        dbfRecord['ACC_ID']    = forceInt(record.value('account_id'))
        dbfRecord['ACCITEM_ID']= forceInt(record.value('accountItem_id'))
        dbfRecord['CLIENT_ID'] = clientId
        dbfRecord['EVENT_ID']  = eventId
        dbfRecord['EXTERNALID']= externalId
        dbfRecord['CARDFLAGS']=cardflag
#------------------------------------
        dbfRecord.store()
        mapCPDToIndex[cpdKey] = dbfRecord.index


    def getEventPersonSpeciality(self, eventId):
        db = QtGui.qApp.db
        tableEvent = db.table('Event')
        tablePerson = db.table('Person')
        tableSpeciality = db.table('rbSpeciality')
        table = tableEvent.innerJoin(tablePerson, tableEvent['execPerson_id'].eq(tablePerson['id']))
        table = table.innerJoin(tableSpeciality, tablePerson['speciality_id'].eq(tableSpeciality['id']))
        cond = [tableEvent['id'].eq(eventId)]
        cols = [tableSpeciality['federalCode']]
        record = db.getRecordEx(table, cols, cond)
        if record:
            return forceString(record.value('federalCode'))
        return u''


    def getTariff(self, tariffId):
        result = self.tariffCache.get(tariffId, False)
        if result == False:
            result = None
            if tariffId:
                record = QtGui.qApp.db.getRecord('Contract_Tariff', '*', tariffId)
                if record:
                    result = CTariff(record)
            self.tariffCache[tariffId] = result
        return result


    def getTariffGroup(self, record):
        amount = forceDouble(record.value('amount'))
        tariffId = forceRef(record.value('tariff_id'))
        tariff = self.getTariff(tariffId)
        if tariff and tariff.limitationIsExceeded(amount):
            return u'кд'
        return ''


    def getMedicalAidProfileCodes(self, profileId):
        if profileId:
            item = self.profileCache.get(profileId, None)
            if item is None:
                record = QtGui.qApp.db.getRecord('rbMedicalAidProfile', ['regionalCode', 'federalCode'], profileId)
                if record:
                    item = ( forceString(record.value(0)),
                             forceString(record.value(1))
                           )
                    self.profileCache[profileId] = item
            if item:
                return item
        return None


    def getAidCodes(self, serviceDetail, date, specialityId, birthDate, sex, diagnosis):
        age = calcAgeTuple(birthDate, date)
        profileId, kindId, typeId = serviceDetail.getMedicalAidIds(specialityId, sex, age, diagnosis)
        profileCodesTuple = self.getMedicalAidProfileCodes(profileId)
        if profileCodesTuple:
            profileRegionalCode, profileFederalCode = profileCodesTuple
        else:
            profileRegionalCode = profileFederalCode = '0' # это ноль
            db = QtGui.qApp.db
            tableSpeciality = db.table('rbSpeciality')
            tableProfile = db.table('rbMedicalAidProfile')
            table = tableSpeciality.leftJoin(tableProfile, tableSpeciality['OKSOName'].eq(tableProfile['name']))
            record = db.getRecordEx(table,
                                    tableProfile['id'],
                                    tableSpeciality['id'].eq(specialityId))
            if record:
                aidTypeId = forceInt(record.value(0))
                if aidTypeId:
                    item = self.profileSpecCache.get(profileId, None)
                    if item is None:
                        item = (forceString(db.translate('rbMedicalAidProfile', 'id', aidTypeId, 'federalCode')),
                                forceString(db.translate('rbMedicalAidProfile', 'id', aidTypeId, 'regionalCode'))
                               )
                        self.profileSpecCache[specialityId] = item
                    profileFederalCode = item[0]
                    profileRegionalCode = item[1]
        if kindId:
            kindCode = self.kindCache.get(typeId, None)
            if kindCode is None:
                kindCode = forceString(QtGui.qApp.db.translate('rbMedicalAidKind', 'id', kindId, 'code'))
                self.kindCache[kindId] = kindCode
        else:
            kindCode = '3'
        if typeId:
            typeCode = self.typeCache.get(typeId, None)
            if typeCode is None:
                typeCode = forceString(QtGui.qApp.db.translate('rbMedicalAidType', 'id', typeId, 'code'))
                self.typeCache[typeId] = typeCode
        else:
            typeCode = '3'
        return profileRegionalCode, profileFederalCode, kindCode, typeCode


    def getClientRepresentativeInfo(self, clientId):
        result = self.representativeInfoCache.get(clientId, None)
        if result is None:
            result = getClientRepresentativeInfo(clientId)
            if result:
                result['status'] = result['regionalRelationTypeCode'] or u'Опекун'
            self.representativeInfoCache[clientId] = result
        return result


    def getOrgStructureDetailsForHospital(self, eventId, dateTime):
        # 1. Если в Событии есть действие Движение,
        # то подразделение оказания услуги определяется по значению свойства "Отделение пребывания"
        # (для События - последнего, для Действий - на дату выполнения).
        # При этом если длительность Движения составляет один день, то поле ProfType="0".
        db = QtGui.qApp.db
        if dateTime:
            # есть дата (ищем последний, начавшийся до заданной даты)
            dateCond = 'AND (Action.begDate<=%s)' % db.formatDate(dateTime)
        else:
            dateCond = ''
        stmt = u'SELECT ActionProperty_OrgStructure.value AS orgStructure_id,'   \
               u'       Action.id AS action_id,'                                 \
               u'       Action.begDate,'                                         \
               u'       Action.endDate'                                          \
               u' FROM Action'                                                   \
               u' INNER JOIN ActionType ON ActionType.id = Action.actionType_id' \
               u' INNER JOIN ActionPropertyType ON ActionPropertyType.actionType_id = ActionType.id'\
               u' INNER JOIN ActionProperty ON ActionProperty.action_id = Action.id AND ActionProperty.type_id = ActionPropertyType.id'\
               u' INNER JOIN ActionProperty_OrgStructure ON ActionProperty_OrgStructure.id = ActionProperty.id'\
               u' INNER JOIN OrgStructure on OrgStructure.id = ActionProperty_OrgStructure.value' \
               u' WHERE Action.deleted = 0' \
               u' AND Action.event_id = %(eventId)d %(dateCond)s' \
               u' AND ActionType.`flatCode` = \'moving\' '\
               u' AND ActionPropertyType.`name` = \'Отделение пребывания\' '\
               u' AND ActionProperty_OrgStructure.value IS NOT NULL' \
               u' ORDER BY Action.begDate DESC' \
               u' LIMIT 1' % { 'eventId' : eventId,
                              'dateCond': dateCond,
                            }
        query = db.query(stmt)
        if query.next():
            record = query.record()
            motionActionId = forceRef(record.value('action_id'))
            orgStructureId = forceRef(record.value('orgStructure_id'))
            begDateTime    = forceDateTime(record.value('begDate'))
            endDateTime    = forceDateTime(record.value('endDate'))
        else:
            motionActionId = orgStructureId = begDateTime = endDateTime = None

        # 2. Если в Событии нет действия Движение,
        # то подразделение оказания услуги определяется как "Приемное отделение".
        # При этом выбирается первое подразделение с типом "Приемное отделение стационара".
        table = db.table('OrgStructure')
        if motionActionId is None:
            cond = [table['type'].eq(4), table['organisation_id'].eq(QtGui.qApp.currentOrgId())]
            idList = db.getIdList(table, 'id', cond, 'id', 1)
            if idList:
                orgStructureId = idList[0]

        if orgStructureId:
            record = db.getRecord(table, ['infisCode', 'infisInternalCode', 'infisDepTypeCode', 'infisTariffCode'], orgStructureId)
            orgStructureInfisCode = forceString(record.value('infisCode'))
            infisTariffCode = forceString(record.value('infisTariffCode'))
            infisInternalCode = forceInt(record.value('infisInternalCode'))
            proftype = forceStringEx(record.value('infisDepTypeCode'))
            if not proftype:
                proftype = u'г'
            if begDateTime and endDateTime and begDateTime.secsTo(endDateTime)<86400:
                proftype = u'0'
        else:
            orgStructureInfisCode = infisTariffCode = infisInternalCode = proftype = ''
        return orgStructureInfisCode, infisTariffCode, infisInternalCode, proftype

    def findRenunciate(self, eventId):
        if eventId:
            db = QtGui.qApp.db
            tableEvent = db.table('Event')
            tableAPT = db.table('ActionPropertyType')
            tableAP = db.table('ActionProperty')
            tableAPS = db.table('ActionProperty_String')
            tableActionType = db.table('ActionType')
            tableAction = db.table('Action')
            cols = [tableAction['id'],
                tableEvent['id'].alias('eventId'),
                tableAPS['value'].alias('nameRenunciate')
                ]
            cond = [tableEvent['id'].eq(eventId),
                tableAction['deleted'].eq(0),
                tableEvent['deleted'].eq(0),
                tableAP['deleted'].eq(0),
                tableAPT['deleted'].eq(0),
                tableAP['action_id'].eq(tableAction['id']),
                tableAction['endDate'].isNotNull()
               ]
            queryTable = tableEvent.leftJoin(tableAction,  tableAction['event_id'].eq(tableEvent['id']))
            queryTable = queryTable.innerJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
            #queryTable = queryTable.innerJoin(tableEvent, tableAction['event_id'].eq(tableEvent['id']))
            queryTable = queryTable.innerJoin(tableAPT, tableAPT['actionType_id'].eq(tableActionType['id']))
            queryTable = queryTable.innerJoin(tableAP, tableAP['type_id'].eq(tableAPT['id']))
            queryTable = queryTable.innerJoin(tableAPS, tableAPS['id'].eq(tableAP['id']))
            cond.append(tableAPT['name'].like(u'Причина отказа%'))
            cond.append(u'ActionProperty_String.value LIKE \'отказ пациента\'')
            recordList = db.getRecordList(queryTable, cols, cond)
            if recordList:
                return True
            return False

    def getTMO(self, street, house):
        tmo = u''
        if street == u'*':
            return tmo
        houses = house.split('/')
        try:
            db = QtGui.qApp.db
            table = db.table('kladr.infisAddress')
            cond = [table['STREET'].eq(street)]
            if len(houses) > 1:
                house = houses[1]
                cond.append(table['HOUSE1'].eq(houses[0]))
            cond.append(table['HOUSE2'].eq(house))
            cols = [table['id'],
                table['PAYER']
                ]
            recordList = db.getRecordList(table, cols, cond)
            if recordList:
                tmo = forceString(recordList[0].value('PAYER'))
        except:
            return tmo
        return tmo


    def getComplexityAndPreliminaryDiagnosis(self, eventId):
        # получить состояние пациента, см.
        # #0005401: Выгрузка состояния при поступлении в ИНФИС
        # Необходимо значение свойства "Состояние при поступлении" действия "приёмное отделение"
        # до двоеточия выгружать в графу COMPLEXITY
        # я буду выгружать первую букву, так как поле имеет ширину 1 символ.
        # upd: и диагноз по 0005413: выгрузка диагноза при поступлении в ИНФИС
        # благо, оно берётся из одного источника
        db = QtGui.qApp.db
        stmt = u'SELECT ActionProperty_String.value AS state, Action.MKB'       \
               u' FROM Action'                                                  \
               u' INNER JOIN ActionType ON ActionType.id = Action.actionType_id'\
               u' INNER JOIN ActionPropertyType ON ActionPropertyType.actionType_id = ActionType.id'\
               u' INNER JOIN ActionProperty ON ActionProperty.action_id = Action.id AND ActionProperty.type_id = ActionPropertyType.id'\
               u' INNER JOIN ActionProperty_String ON ActionProperty_String.id = ActionProperty.id'\
               u' WHERE Action.deleted = 0'                                     \
               u' AND Action.event_id = %(eventId)d'                            \
               u' AND ActionType.`flatCode` = \'received\''                     \
               u' AND ActionPropertyType.`name` = \'Состояние при поступлении\''\
               u' ORDER BY Action.begDate DESC'                                 \
               u' LIMIT 1' % { 'eventId' : eventId,
                             }
        query = db.query(stmt)
        if query.next():
            record = query.record()
            state  = forceString(record.value('state'))
            diagnosis = MKBwithoutSubclassification(forceString(record.value('MKB')))
            if len(diagnosis) == 3:
                diagnosis += '.'
            return state[:1].lower(), diagnosis
        return '', ''


    def getHospialBedInfo(self, eventId, flatCode):
        db = QtGui.qApp.db
        stmt = u'SELECT'                                                        \
               u' ActionProperty_rbHospitalBedProfile.value AS hospitalBedProfile_id,'   \
               u' ActionProperty_HospitalBed.value AS hospitalBed_id'           \
               u' FROM Action'                                                  \
               u' INNER JOIN ActionType ON ActionType.id = Action.actionType_id'\
               u' INNER JOIN ActionPropertyType AS APTHBP ON APTHBP.actionType_id = ActionType.id AND APTHBP.`name` = \'профиль\''\
               u' LEFT  JOIN ActionProperty     AS APHBP  ON APHBP.action_id = Action.id AND APHBP.type_id = APTHBP.id'\
               u' LEFT  JOIN ActionProperty_rbHospitalBedProfile ON ActionProperty_rbHospitalBedProfile.id = APHBP.id'\
               u' LEFT  JOIN ActionPropertyType AS APTHB  ON APTHB.actionType_id = ActionType.id AND APTHB.`name`  = \'койка\''\
               u' LEFT  JOIN ActionProperty     AS APHB   ON APHB.action_id = Action.id AND APHB.type_id = APTHB.id'\
               u' LEFT  JOIN ActionProperty_HospitalBed   ON ActionProperty_HospitalBed.id = APHB.id'\
               u' WHERE Action.deleted = 0' \
               u' AND Action.event_id = %(eventId)d' \
               u' AND ActionType.`flatCode` = %(flatCode)s '\
               u' ORDER BY Action.begDate DESC' \
               u' LIMIT 1' % { 'eventId' : eventId,
                               'flatCode': decorateString(flatCode)
                             }
        query = db.query(stmt)
        if query.next():
            record = query.record()
            hospitalBedProfileId  = forceRef(record.value('hospitalBedProfile_id'))
            hospitalBedId = forceRef(record.value('hospitalBed_id'))
        else:
            hospitalBedProfileId = hospitalBedId = None
        return hospitalBedProfileId, hospitalBedId


    def getProfileCodesForEvent(self, eventId, dateTime):
        # 0005407: Сопоставление профиля мед.помощи госпитальному событию при экспорте в ИНФИС/ЕИС
        # При экспорте реестра счета в ИНФИС (во вторую очередь в ЕИС) необходимо для записей,
        # связанных с тарификаций госпитального События (тип мед.помощи: 1,2,3),
        # определять профиль мед.помощи следующим образом:
        # 1. проверять наличие в Событии действия "выбытие" (leaved )
        #    и значение его свойства "Профиль", по которому определять профиль
        #    мед.помощи.
        # 2. Если нет "выбытия" проверять наличие действия "движение" (moving)
        #    и значение его свойства "Профиль". Если действий "движение"
        #    более одного, то останавливать выбор на последнем из них.
        # 3. При этом учитывать, что если значение в свойстве "Профиль"
        #    не определено, то проверять значение свойства "койка".
        # 4. Если нет "движения", проверять наличие действия
        #    "Поступление" (received) и значение его свойства "Профиль".
        db = QtGui.qApp.db
        hospitalBedProfileId, hospitalBedId = self.getHospialBedInfo(eventId, 'leaved')
        if hospitalBedProfileId is None:
            hospitalBedProfileId, hospitalBedId = self.getHospialBedInfo(eventId, 'moving')
            if hospitalBedProfileId is None and hospitalBedId:
                hospitalBedProfileId = forceRef(db.translate('OrgStructure_HospitalBed', 'id', hospitalBedId, 'profile_id'))
        if hospitalBedProfileId is None:
            hospitalBedProfileId, hospitalBedId = self.getHospialBedInfo(eventId, 'received')
        profileId = forceRef(db.translate('rbHospitalBedProfile', 'id', hospitalBedProfileId, 'medicalAidProfile_id'))
        if profileId:
            return self.getMedicalAidProfileCodes(profileId)
        else:
            return None

        if dateTime:
            # есть дата (ищем последний, начавшийся до заданной даты)
            dateCond = 'AND (Action.begDate<=%s)' % db.formatDate(dateTime)
        else:
            dateCond = ''
        stmt = u'SELECT ActionProperty_OrgStructure.value AS orgStructure_id,'   \
               u'       Action.id AS action_id,'                                 \
               u'       Action.begDate,'                                         \
               u'       Action.endDate'                                          \
               u' FROM Action'                                                   \
               u' INNER JOIN ActionType ON ActionType.id = Action.actionType_id' \
               u' INNER JOIN ActionPropertyType ON ActionPropertyType.actionType_id = ActionType.id'\
               u' INNER JOIN ActionProperty ON ActionProperty.action_id = Action.id AND ActionProperty.type_id = ActionPropertyType.id'\
               u' INNER JOIN ActionProperty_OrgStructure ON ActionProperty_OrgStructure.id = ActionProperty.id'\
               u' INNER JOIN OrgStructure on OrgStructure.id = ActionProperty_OrgStructure.value' \
               u' WHERE Action.deleted = 0' \
               u' AND Action.event_id = %(eventId)d %(dateCond)s' \
               u' AND ActionType.`flatCode` = \'moving\' '\
               u' AND ActionPropertyType.`name` = \'Отделение пребывания\' '\
               u' AND ActionProperty_OrgStructure.value IS NOT NULL' \
               u' ORDER BY Action.begDate DESC' \
               u' LIMIT 1' % { 'eventId' : eventId,
                              'dateCond': dateCond,
                            }
        query = db.query(stmt)
        if query.next():
            record = query.record()
            motionActionId = forceRef(record.value('action_id'))
            orgStructureId = forceRef(record.value('orgStructure_id'))
            begDateTime    = forceDateTime(record.value('begDate'))
            endDateTime    = forceDateTime(record.value('endDate'))
        else:
            motionActionId = orgStructureId = begDateTime = endDateTime = None

        # 2. Если в Событии нет действия Движение,
        # то подразделение оказания услуги определяется как "Приемное отделение".
        # При этом выбирается первое подразделение с типом "Приемное отделение стационара".
        table = db.table('OrgStructure')
        if motionActionId is None:
            cond = [table['type'].eq(4), table['organisation_id'].eq(QtGui.qApp.currentOrgId())]
            idList = db.getIdList(table, 'id', cond, 'id', 1)
            if idList:
                orgStructureId = idList[0]

        if orgStructureId:
            record = db.getRecord(table, ['infisCode', 'infisInternalCode', 'infisDepTypeCode', 'infisTariffCode'], orgStructureId)
            orgStructureInfisCode = forceString(record.value('infisCode'))
            infisTariffCode = forceString(record.value('infisTariffCode'))
            infisInternalCode = forceInt(record.value('infisInternalCode'))
            proftype = forceStringEx(record.value('infisDepTypeCode'))
            if not proftype:
                proftype = u'г'
            if begDateTime and endDateTime and begDateTime.secsTo(endDateTime)<86400:
                proftype = u'0'
        else:
            orgStructureInfisCode = infisTariffCode = infisInternalCode = proftype = ''
        return orgStructureInfisCode, infisTariffCode, infisInternalCode, proftype


    def isComplete(self):
        return self.done


    def validatePage(self):
        QtGui.qApp.preferences.appPrefs['INFISOMSRepresentativeOutRule'] = toVariant(self.cmbRepresentativeOutRule.currentIndex())
        return True


    def abort(self):
        self.aborted = True


    @pyqtSignature('')
    def on_btnExport_clicked(self):
        self.export()


    @pyqtSignature('')
    def on_btnCancel_clicked(self):
        self.abort()

    @pyqtSignature('int')
    def on_cbCardflag_stateChanged(self,  state):
        self.edtCardflag.setEnabled(state)

class CExportINFISOMSPage2(QtGui.QWizardPage, Ui_ExportINFISOMSPage2):
    def __init__(self, parent):
        QtGui.QWizardPage.__init__(self, parent)
        self.setupUi(self)
        self.setTitle(u'Экспорт данных реестра по счёту')
        self.setSubTitle(u'для выполнения шага нажмите кнопку "финиш"')

        self.pathIsValid = True
        homePath = QDir.toNativeSeparators(QDir.homePath())
        exportDir = forceString(QtGui.qApp.preferences.appPrefs.get('INFISOMSExportDir', homePath))
        self.edtDir.setText(exportDir)


    def isComplete(self):
        return self.pathIsValid


    def validatePage(self):
        src = self.wizard().getFullDbfFileName()
        dst = os.path.join(forceStringEx(self.edtDir.text()), os.path.basename(src))
        success1, result = QtGui.qApp.call(self, shutil.move, (src, dst))
        src = os.path.splitext(src)[0] + '.dbt'
        if os.path.exists(src):
            dst = os.path.join(forceStringEx(self.edtDir.text()), os.path.basename(src))
            success2, result = QtGui.qApp.call(self, shutil.move, (src, dst))
        else:
            success2 = True
        if success1 and success2:
            QtGui.qApp.preferences.appPrefs['INFISOMSExportDir'] = toVariant(self.edtDir.text())
            self.wizard().setAccountExposeDate()
            return True
        else:
            return False


    @pyqtSignature('QString')
    def on_edtDir_textChanged(self):
        dir = forceStringEx(self.edtDir.text())
        pathIsValid = os.path.isdir(dir)
        if self.pathIsValid != pathIsValid:
            self.pathIsValid = pathIsValid
            self.emit(SIGNAL('completeChanged()'))


    @pyqtSignature('')
    def on_btnSelectDir_clicked(self):
        dir = QtGui.QFileDialog.getExistingDirectory(self,
                u'Выберите директорий для сохранения файла выгрузки в ИнФИС',
                 forceStringEx(self.edtDir.text()),
                 QtGui.QFileDialog.ShowDirsOnly)
        if forceString(dir):
            self.edtDir.setText(QDir.toNativeSeparators(dir))
