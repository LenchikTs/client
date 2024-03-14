# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2015 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
#TODO:
#для обычных услуг, которые имеют action мы берем даты begDate и endDate (из Action)
#для стационара, где больше 2х движений, берем из таблицы event setDate и execDate
#--
#Для услуг по гемодиализу, профосмотру и лечебно-диагностическая (КАК ОПРЕДЕЛИТЬ?!? - из типа события, вероятно)
# Брать из таблицы VISIT и количество гемодиализа проверить.
import os.path
import shutil
import uuid
from zipfile import ZIP_DEFLATED, ZipFile

from PyQt4 import QtGui
from PyQt4.QtCore import Qt,  QDate, QDir, QFile, QString, QTextCodec, QXmlStreamWriter, pyqtSignature, SIGNAL

#from PyQt4.QtXml import *


#from library.Utils import forceBool, forceDate, forceDouble, forceInt, forceRef, forceString, forceStringEx, formatSNILS, getVal, toVariant, trim

from library.Utils import forceBool, forceDate, forceDouble, forceInt, forceRef, forceString, forceStringEx, formatSNILS, toVariant, trim

from Accounting.Tariff import CTariff
from Exchange.Export29XMLCommon import Export29XMLCommon
from Exchange.Export29XMLCommon import SummSingleton
from Exchange.Export import CExportHelperMixin
#from Exchange.Utils import compressFileInZip

from Exchange.Ui_ExportR29XMLPage1 import Ui_ExportPage1
from Exchange.Ui_ExportR29XMLPage2 import Ui_ExportPage2

# contractBegDate = None
serviceInfoExportVersion = '1.0'
container = SummSingleton()

def getAccountInfo(accountId) :
    db = QtGui.qApp.db
    accountRecord = db.getRecord('Account', 'settleDate, number, exposeDate, contract_id, payer_id, date, amount', accountId)
    if accountRecord:
        date = forceDate(accountRecord.value('settleDate'))
        aDate  = forceDate(accountRecord.value('date'))
        exposeDate = forceDate(accountRecord.value('exposeDate'))
        number = forceString(accountRecord.value('number')).strip()
        contractId = forceRef(accountRecord.value('contract_id'))
        payerId = forceRef(accountRecord.value('payer_id'))
        amount = 0 #Export29XMLCommon.getAccountNumber(db, accountId)
    else:
        date = exposeDate = contractId = payerId = aDate =  None
        number = '0'
        amount= 0
    return date, number, exposeDate, contractId,  payerId,  aDate, amount


def exportR29DDv312(widget, accountId, accountItemIdList, type):
    wizard = CExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.setType(type)
    wizard.exec_()

# *****************************************************************************************

class CExportWizard(QtGui.QWizard):
    def __init__(self, parent=None):
        QtGui.QWizard.__init__(self, parent)
        self.setWizardStyle(QtGui.QWizard.ModernStyle)
        self.page1 = CExportPage1(self)
        self.page1.edtRegistryNumber.setRange(0, 9999)
        
        self.page2 = CExportPage2(self)
        self.addPage(self.page1)
        self.addPage(self.page2)
        self.setWindowTitle(u'Мастер экспорта в XML для Архангельской области')
        self.tmpDir = ''
        self.xmlFileName = ''
        
    def setType(self, type):
        self.page1.type = type
   
    def setAccountId(self, accountId):
        self.accountId = accountId
        date, number, exposeDate, contractId, payerId,  aDate, aAmount = getAccountInfo(accountId)
        strNumber = number if trim(number) else u'б/н'
        strDate = forceString(date) if date.isValid() else u'б/д'
        self.page1.setTitle(u'Экспорт данных реестра по счёту №%s от %s' %(strNumber, strDate))
        self.page2.setTitle(u'Укажите директорий для сохранения обменных файлов')


    def setAccountExposeDate(self):
        db = QtGui.qApp.db
        accountRecord = db.table('Account').newRecord(['id', 'exposeDate'])
        accountRecord.setValue('id', toVariant(self.accountId))
        accountRecord.setValue('exposeDate', toVariant(QDate.currentDate()))
        db.updateRecord('Account', accountRecord)


    def getTmpDir(self):
        if not self.tmpDir:
            self.tmpDir = QtGui.qApp.getTmpDir('R29XML')
        return self.tmpDir


    def getMiacCode(self, contractId):
        db = QtGui.qApp.db
        stmt = """SELECT Organisation.miacCode FROM Contract
                  LEFT JOIN Organisation ON Organisation.id = Contract.recipient_id
                  WHERE Contract.id = %s"""
        query = db.query(stmt % str(contractId))
        if query.next():
            record = query.record()
        return forceString(record.value(0))




    def getFullXmlFileName(self):
        if not self.xmlFileName:
            (date, number, exposeDate, contractId,  payerId,  aDate, aAmount) = getAccountInfo(self.accountId)

            payerCode = '29'
            try:
                strContractNumber = forceString(QtGui.qApp.db.translate('Contract', 'id', contractId , 'number'))
                strContractNote = forceString(QtGui.qApp.db.translate('Contract', 'id', contractId , 'note'))
                if strContractNumber.lower().find(u'иногород') != -1 or self.page1.chkExportTypeBelonging.isChecked() or forceString(QtGui.qApp.db.translate('Organisation', 'id', payerId, 'miacCode')) == '29':
                    infix = 'T'
                else:
                    infix = 'S'
                    payerCode = forceString(QtGui.qApp.db.translate(
                    'Organisation', 'id', payerId, 'miacCode'))

            except:
                self.log(str(contractId)+ ", strContractNumber, ")


            lpuInfis  = self.getMiacCode(contractId) #'292301'
            self.xmlFileName = os.path.join(self.getTmpDir(), \
                u'%sM%s%s%s_%s%d.xml' % (strContractNote[:2], lpuInfis, infix,  payerCode, date.toString('yyMM'),
                                        self.page1.edtRegistryNumber.value()))
        return self.xmlFileName


    def getFullXmlPersFileName(self):
        return os.path.join(self.getTmpDir(), u'L%s' % os.path.basename(self.getFullXmlFileName())[1:])
    
    def getFullXmlAccFileName(self):
        return os.path.join(self.getTmpDir(), u'S%s' % os.path.basename(self.getFullXmlFileName())[1:])


    def setAccountItemsIdList(self, accountItemIdList):
        self.page1.setAccountItemsIdList(accountItemIdList)


    def cleanup(self):
        if self.tmpDir:
            QtGui.qApp.removeTmpDir(self.tmpDir)
            self.tmpDir = ''


    def exec_(self):
        QtGui.QWizard.exec_(self)
        self.cleanup()

# *****************************************************************************************

class CExportPage1(QtGui.QWizardPage, Ui_ExportPage1, CExportHelperMixin):
    sexMap = {1: u'М',  2: u'Ж'}

    def __init__(self, parent):
        QtGui.QWizardPage.__init__(self, parent)
        self.setupUi(self)
        CExportHelperMixin.__init__(self)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(1)
        self.progressBar.setText('')
        self.setTitle(u'Экспорт данных реестра по счёту')
        self.setSubTitle(u'для выполнения шага нажмите кнопку "экспорт"')
        self.contractBegDate =  None
        self.setExportMode(False)
        
        self.aborted = False
        self.done = False
        self.idList = []
        self.parent = parent #wtf? скрывать Qt-шный parent - это плохая затея
        self.recNum= 0
        self.ignoreErrors = forceBool(QtGui.qApp.preferences.appPrefs.get('ExportR29XMLIgnoreErrors', False))
        self.connect(parent, SIGNAL('rejected()'), self.abort)
        self.chkVerboseLog.setChecked(forceBool(QtGui.qApp.preferences.appPrefs.get('ExportR29XMLVerboseLog', False)))
        self.chkIgnoreErrors.setChecked(self.ignoreErrors)
#        self.chkGroupByService.setChecked(forceBool(QtGui.qApp.preferences.appPrefs.get('ExportR29XMLGroupByService', True)))
        self.edtRegistryNumber.setValue(forceInt(QtGui.qApp.preferences.appPrefs.get('ExportR29XMLRegistryNumber', 0))+1)
        self.chkExportTypeBelonging.setChecked(forceBool(QtGui.qApp.preferences.appPrefs.get('ExportR29XMLBelonging', True)))


    def setExportMode(self, flag):
        self.btnCancel.setEnabled(flag)
        self.btnExport.setEnabled(not flag)
        self.chkIgnoreErrors.setEnabled(not flag)
        self.chkVerboseLog.setEnabled(not flag)
        self.chkClientLog.setEnabled(not flag)
        #self.btnExport.setEnabled(not flag)
        #self.chkGroupByService.setEnabled(not flag)
        self.edtRegistryNumber.setEnabled(not flag)


    def log(self, str, forceLog = False):
        if self.chkVerboseLog.isChecked() or forceLog:
            self.logBrowser.append(str)
            self.logBrowser.update()


    def setAccountItemsIdList(self, accountItemIdList):
        self.idList = accountItemIdList


    def prepareToExport(self, contractBegDate):
        self.done = False
        self.aborted = False
        self.emit(SIGNAL('completeChanged()'))
        self.setExportMode(True)
        output, clientOutput, accountOut = self.createXML(contractBegDate)
        self.progressBar.reset()
        self.progressBar.setMaximum(1)
        self.progressBar.setValue(0)
        self.progressBar.setText(u'Запрос в БД...')
        QtGui.qApp.processEvents()
        query = self.createQuery()
        self.progressBar.setMaximum(max(query.size(), 1))
        self.progressBar.reset()
        self.progressBar.setValue(0)
        return output, query,  clientOutput, accountOut


    def export(self):
        (result, rc) = QtGui.qApp.call(self, self.exportInt)
        self.setExportMode(False)
        if self.aborted or not result:
            self.progressBar.setText(u'прервано')
        else:
            self.progressBar.setText(u'готово')
            QtGui.qApp.preferences.appPrefs['ExportR29XMLIgnoreErrors'] = \
                    toVariant(self.chkIgnoreErrors.isChecked())
            QtGui.qApp.preferences.appPrefs['ExportR29XMLVerboseLog'] = \
                    toVariant(self.chkVerboseLog.isChecked())
#            QtGui.qApp.preferences.appPrefs['ExportR29XMLGroupByService'] = \
#                    toVariant(self.chkGroupByService.isChecked())
            QtGui.qApp.preferences.appPrefs['ExportR29XMLBelonging'] = \
                    toVariant(self.chkExportTypeBelonging.isChecked())
            self.done = True
            self.emit(SIGNAL('completeChanged()'))

# *****************************************************************************************

    def getFirstAccountInfo(self, begDate, endDate):
        db = QtGui.qApp.db
        table = db.table('Account')
        record = QtGui.qApp.db.getRecordEx(table, 'settleDate, number', table['settleDate'].between(begDate, endDate))

        if record:
            date = forceDate(record.value(0))
            strNumber = forceString(record.value('number')).strip()

            if strNumber.isdigit():
                number = forceInt(strNumber)
            else:
                # убираем номер договора с дефисом, если они есть в номере
                i = len(strNumber) - 1
                while (i>0 and strNumber[i].isdigit()):
                    i -= 1

                number = forceInt(strNumber[i+1:] if strNumber[i+1:] != '' else 0)

            #number = forceInt(record.value(1))
        else:
            date = QDate()
            number = 0

        return date, number



    def createQuery(self):
        db = QtGui.qApp.db
        tableAccountItem = db.table('Account_Item')
        cond = tableAccountItem['id'].inlist(self.idList)

        sumStr = """Account_Item.`sum` AS `sum`,
                Account_Item.amount AS amount,
                
                            """ #% CTariff.ttEventByMESLen

        stmt = """SELECT Account_Item.id AS accountItemId,
               --  IF(Event.prevEvent_id IS NULL, Account_Item.event_id, IF(prevEvent.code = '9208' or prevEvent.code =  %s or EventType.mesCodeMask = '3.19', Account_Item.event_id, Event.prevEvent_id))  AS event_id,
                Account_Item.event_id  AS event_id,
                Account_Item.event_id as eventId1,
                Account_Item.visit_id as visit_id,
                Account_Item.action_id as action_id,
                Account_Item.service_id,
                Event.client_id        AS client_id,
                EventType.service_id AS EventServiceId,
                EventType.name as EventTypeName,
                Contract_Tariff.uet as ContractTariffUet,
                Contract_Tariff.pg as pgCode,
                Client.lastName,
                Client.firstName,
                Client.patrName,
                Client.birthDate       AS birthDate,
                Client.sex AS sex,
                Client.SNILS AS SNILS,
                Client.birthPlace AS birthPlace,
                age(Client.birthDate, Event.execDate) as clientAge,
                CONCAT(ClientPolicy.serial, ' ', ClientPolicy.number) AS policySN,
                ClientPolicy.serial AS policySerial,
                ClientPolicy.number AS policyNumber,
                ClientPolicy.begDate   AS policyBegDate,
                ClientPolicy.endDate   AS policyEndDate,
                rbPolicyKind.regionalCode AS policyKindCode,
                rbPolicyKind.federalCode AS policyKindFederalCode,
                Insurer.OGRN AS insurerOGRN,
                Insurer.OKATO AS insurerOKATO,
                Insurer.area AS insurerArea,
                ClientDocument.serial  AS documentSerial,
                ClientDocument.number  AS documentNumber,
                ClientDocument.date AS documentDate,
                ClientDocument.origin AS documentOrg,
                ClientDocument.documentType_id AS clientDocTypeId,
                rbDocumentType.regionalCode AS documentRegionalCode,
                rbDocumentType.federalCode AS documentFederalCode,
                rbDocumentType.code AS documentTypeCode,
                IF(work.title IS NOT NULL,
                    work.title, ClientWork.freeInput) AS `workName`,
                IF(Account_Item.visit_id IS NOT NULL, Visit.person_id,
                    IF(Account_Item.action_id IS NOT NULL,
                        IF(Action.person_id IS NOT NULL, Action.person_id, Action.setPerson_id), Event.execPerson_id)
                ) AS execPersonId,
                Diagnosis.MKB          AS MKB,
                rbDiseaseCharacter.code as diagChatacter,
                rbTraumaType.code    AS traumaCode,
                Event.eventType_id    AS eventTypeId,
                IF(prevEvent.code = '9208' or prevEvent.code =  %s  or EventType.mesCodeMask = '3.19', NULL, Event.prevEvent_id)    AS preEventId,
                Event.setDate          AS begDateEvent,
                Event.execDate         AS endDateEvent,
                Visit.date         AS dateVisit,
                Visit.createDatetime,
                Visit.modifyDatetime,
                Contract_Tariff.federalPrice AS federalPrice,
                Contract_Tariff.regionalPrice AS regionalPrice,
                Contract_Tariff.price as contractTariffPrice,
                Contract_Tariff.id AS ContractTariffId,
                Contract_Tariff.tariffType AS ContractTariffType,
                Account_Item.uet,
                Account_Item.price AS price, %s
                Person.regionalCode AS personRegionalCode,
                rbDiagnosticResult.federalCode AS resultFederalCode,
                rbMedicalAidType.regionalCode AS medicalAidTypeRegionalCode,
                rbMedicalAidType.regionalCode AS medicalAidTypeFederalCode,
                IF(SpecialCaseAction.id IS NULL, 0, 1) AS specialCaseAction,
                IF(Account_Item.service_id IS NOT NULL,
                   ItemMedicalAidProfile.federalCode,
                   IF(Account_Item.visit_id IS NOT NULL, VisitMedicalAidProfile.federalCode, EventMedicalAidProfile.federalCode)
                  ) AS medicalAidProfileFederalCode,
                IF(Account_Item.service_id IS NOT NULL,
                   ItemMedicalAidType.code,
                   IF(Account_Item.visit_id IS NOT NULL, VisitMedicalAidType.code, EventMedicalAidType.code)
                  ) AS medicalAidTypeCode,
                IF(Account_Item.service_id IS NOT NULL,
                   ItemMedicalAidKind.code,
                   IF(Account_Item.visit_id IS NOT NULL, VisitMedicalAidKind.code, EventMedicalAidKind.code)
                  ) AS medicalAidKindCode,

                IF(Account_Item.service_id IS NOT NULL,
                    rbItemService.id,
                    IF(Account_Item.visit_id IS NOT NULL, rbVisitService.id, rbEventService.id)
                    ) AS serviceId,
                IF(Account_Item.service_id IS NOT NULL,
                    rbItemServiceGroup.regionalCode,
                    IF(Account_Item.visit_id IS NOT NULL, rbVisitServiceGroup.regionalCode, rbEventServiceGroup.regionalCode)
                    ) AS serviceGroupCode,
                AccDiagnosis.MKB AS AccMKB,
                CompDiagnosis.MKB AS CompMKB,
                PreDiagnosis.MKB AS PreMKB,
                rbEventProfile.regionalCode AS eventProfileRegCode,
                rbEventProfile.code AS eventProfileCode,
                OrgStructure.infisCode AS orgStructureCode,
                OrgStructure.infisInternalCode AS orgStructureInternalCode,
                rbMedicalAidUnit.federalCode AS medicalAidUnitFederalCode,
                rbEventTypePurpose.regionalCode AS eventTypePurpose,
                rbEventTypePurpose.federalCode AS eventTypePurposeFederalCode,
                Event.`order`,
                Event.id AS eventId,
                EventResult.code AS eventResultFederalCode,
                EventResult.regionalCode AS eventResultRegionalCode,
                RelegateOrg.miacCode AS relegateOrgMiac,
                rbTariffCategory.federalCode AS tariffCategoryFederalCode,
                EventType.code AS eventTypeCode,
                EventType.regionalCode AS eventTypeRegionalCode,
                Action.begDate AS begDateAction,
                Action.endDate AS endDateAction,
                if(`rbDispanser`.observed IN (1, 2), IF(`rbDispanser`.observed = 6, 2, `rbDispanser`.observed), 3) as dispanserStatus
            FROM Account_Item
            LEFT JOIN Action ON Action.id = Account_Item.action_id
            LEFT JOIN Action AS SpecialCaseAction ON SpecialCaseAction.id = (
                    SELECT SCA.id
                    FROM Action SCA
                    LEFT JOIN ActionType AS SCAType ON SCA.actionType_id = SCAType.id
                    WHERE SCA.event_id = Account_Item.event_id AND
                            SCAType.code = '111'
                    LIMIT 1
            )
            LEFT JOIN Event  ON Event.id  = Account_Item.event_id
            LEFT JOIN Event as prev  ON prev.id  = Event.prevEvent_id
            LEFT JOIN EventType as prevEvent ON prevEvent.id = prev.eventType_id
            LEFT JOIN EventType ON EventType.id = Event.eventType_id
            LEFT JOIN Visit  ON Visit.id  = Account_Item.visit_id
            LEFT JOIN Client ON Client.id = Event.client_id
            LEFT JOIN ClientPolicy ON ClientPolicy.client_id = Client.id AND
                      ClientPolicy.id = (SELECT MAX(CP.id)
                                         FROM   ClientPolicy AS CP
                                         LEFT JOIN rbPolicyType AS CPT ON CPT.id = CP.policyType_id
                                         WHERE  CP.client_id = Client.id AND CP.deleted=0 AND CPT.code IN ('1','2'))
            -- LEFT JOIN ClientRelation ON ClientRelation.client_id = Client.id
            LEFT JOIN rbPolicyKind ON ClientPolicy.policyKind_id = rbPolicyKind.id
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
            LEFT JOIN Address   RegAddress ON RegAddress.id = ClientRegAddress.address_id
            LEFT JOIN AddressHouse RegAddressHouse ON RegAddressHouse.id = RegAddress.house_id
            LEFT JOIN Person  ON Person.id = Event.execPerson_id
            LEFT JOIN Diagnostic ON Diagnostic.id = (
              SELECT MAX(D.id)
              FROM Diagnostic AS D
              WHERE D.event_id = Account_Item.event_id
                AND ((D.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code ='2') AND D.person_id = Event.execPerson_id)
                        OR (D.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code='1'
                            ))
                        OR (D.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE `code` ='2')
                        AND  EventType.medicalAidtype_id IN (SELECT id FROM rbMedicalAidType WHERE `code` = 4)))
                          AND D.deleted = 0)
            LEFT JOIN ClientWork ON ClientWork.client_id=Event.client_id AND
                        ClientWork.id = (SELECT max(CW.id)
                                         FROM ClientWork AS CW
                                         WHERE CW.client_id=Client.id AND CW.deleted=0)
            LEFT JOIN Organisation AS work ON work.id=ClientWork.org_id AND work.deleted = 0
            LEFT JOIN Organisation AS RelegateOrg ON Event.relegateOrg_id = RelegateOrg.id
            LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
            LEFT JOIN rbTraumaType ON rbTraumaType.id = Diagnosis.traumaType_id
            LEFT JOIN rbDiagnosticResult ON rbDiagnosticResult.id=Diagnostic.result_id
            LEFT JOIN rbResult AS EventResult ON EventResult.id=Event.result_id
            LEFT JOIN rbService AS rbEventService ON rbEventService.id = EventType.service_id
            LEFT JOIN rbService AS rbVisitService ON rbVisitService.id = Visit.service_id
            LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
            LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
            LEFT JOIN rbService AS rbItemService ON rbItemService.id = Account_Item.service_id
            LEFT JOIN rbServiceGroup as rbItemServiceGroup ON rbItemServiceGroup.id = rbItemService.group_id
            LEFT JOIN rbServiceGroup as rbEventServiceGroup ON rbEventServiceGroup.id = rbEventService.group_id
            LEFT JOIN rbServiceGroup as rbVisitServiceGroup ON rbVisitServiceGroup.id = rbVisitService.group_id
            LEFT JOIN rbDiseaseCharacter ON Diagnostic.character_id = rbDiseaseCharacter.id
            LEFT JOIN rbHealthGroup ON Diagnostic.healthGroup_id = rbHealthGroup.id
            LEFT JOIN rbDispanser ON rbDispanser.id = Diagnostic.dispanser_id
            LEFT JOIN rbMedicalAidType ON EventType.medicalAidType_id = rbMedicalAidType.id
            LEFT JOIN rbMedicalAidKind ON EventType.medicalAidKind_id = rbMedicalAidKind.id
            LEFT JOIN rbEventTypePurpose ON EventType.purpose_id = rbEventTypePurpose.id
            LEFT JOIN rbEventProfile ON EventType.eventProfile_id = rbEventProfile.id
            LEFT JOIN rbMedicalAidProfile AS EventMedicalAidProfile ON
                EventMedicalAidProfile.id = rbEventService.medicalAidProfile_id
            LEFT JOIN rbMedicalAidProfile AS VisitMedicalAidProfile ON
                VisitMedicalAidProfile.id = rbVisitService.medicalAidProfile_id
            LEFT JOIN rbMedicalAidProfile AS ItemMedicalAidProfile ON
                ItemMedicalAidProfile.id = rbItemService.medicalAidProfile_id

            LEFT JOIN rbMedicalAidKind AS EventMedicalAidKind ON
                EventMedicalAidKind.id = rbEventService.medicalAidKind_id
            LEFT JOIN rbMedicalAidKind AS VisitMedicalAidKind ON
                VisitMedicalAidKind.id = rbVisitService.medicalAidKind_id
            LEFT JOIN rbMedicalAidKind AS ItemMedicalAidKind ON
                ItemMedicalAidKind.id = rbItemService.medicalAidKind_id

            LEFT JOIN rbMedicalAidType AS EventMedicalAidType ON
                EventMedicalAidType.id = rbEventService.medicalAidType_id
            LEFT JOIN rbMedicalAidType AS VisitMedicalAidType ON
                VisitMedicalAidType.id = rbVisitService.medicalAidType_id
            LEFT JOIN rbMedicalAidType AS ItemMedicalAidType ON
                ItemMedicalAidType.id = rbItemService.medicalAidType_id

            LEFT JOIN Diagnostic AS AccDiagnostic ON AccDiagnostic.id = (
             SELECT id FROM Diagnostic AS AD
             WHERE AD.event_id = Account_Item.event_id AND
                AD.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code='9') AND
                AD.person_id = Event.execPerson_id AND
                AD.deleted = 0 LIMIT 1)
            LEFT JOIN Diagnosis AS AccDiagnosis ON
                AccDiagnosis.id = AccDiagnostic.diagnosis_id AND
                AccDiagnosis.deleted = 0

            LEFT JOIN Diagnostic AS CompDiagnostic ON CompDiagnostic.id = (
             SELECT id FROM Diagnostic AS CD

             WHERE CD.event_id = Account_Item.event_id AND CD.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code='3') AND
                CD.person_id = Event.execPerson_id AND
                CD.deleted = 0 LIMIT 1)
            LEFT JOIN Diagnosis AS CompDiagnosis ON
                CompDiagnosis.id = CompDiagnostic.diagnosis_id AND
                CompDiagnosis.deleted = 0
            LEFT JOIN Diagnostic AS PreDiagnostic ON PreDiagnostic.id = (
             SELECT id FROM Diagnostic AS PD
             WHERE PD.event_id = Account_Item.event_id AND
                PD.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code='7') AND
                PD.person_id = Event.execPerson_id AND
                PD.deleted = 0 LIMIT 1)
            LEFT JOIN Diagnosis AS PreDiagnosis ON
                PreDiagnosis.id = PreDiagnostic.diagnosis_id AND
                PreDiagnosis.deleted = 0

            LEFT JOIN OrgStructure ON Person.orgStructure_id = OrgStructure.id
            LEFT JOIN rbMedicalAidUnit ON Account_Item.unit_id = rbMedicalAidUnit.id
            LEFT JOIN Contract_Tariff ON Account_Item.tariff_id = Contract_Tariff.id
            LEFT JOIN rbTariffCategory ON  Contract_Tariff.tariffCategory_id = rbTariffCategory.id
            WHERE
                Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s ORDER BY  Client.id, Event.id DESC ,    Event.execDate, Account_Item.price DESC""" % (u'"УО"', u'"УО"', sumStr, cond)

        query = db.query(stmt)
        return query

# *****************************************************************************************

    def getEventsSummaryPrice(self):
        u"""возвращает общую стоимость услуг за событие"""

        db = QtGui.qApp.db
        tableAccountItem = db.table('Account_Item')

        stmt = """SELECT event_id,
            SUM(IF(Account_Item.uet!=0,TRUNCATE(Account_Item.price*Account_Item.uet + 0.006, 2),
                TRUNCATE(Account_Item.amount*Account_Item.price + 0.006,2))) AS totalSum,
            SUM(IF(Account_Item.uet!=0, Account_Item.uet, Account_Item.amount)) AS totalAmount,
            SUM(IF(Account_Item.uet!=0,TRUNCATE(Contract_Tariff.federalPrice*Account_Item.uet + 0.006, 2),
                TRUNCATE(Contract_Tariff.federalPrice*Account_Item.amount + 0.006,2))) AS federalSum

        FROM Account_Item
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        LEFT JOIN Contract_Tariff ON Account_Item.tariff_id = Contract_Tariff.id
        WHERE Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s
        GROUP BY event_id;
        """ % tableAccountItem['id'].inlist(self.idList)
        query = db.query(stmt)

        result = {}
        while query.next():
            record  = query.record()
            eventId = forceRef(record.value('event_id'))
            sum     = forceDouble(record.value('totalSum')) -forceDouble(record.value('federalSum'))


            amount = forceDouble(record.value('totalAmount'))
            result[eventId] = (amount,  sum)
        return result

# *****************************************************************************************



    def exportInt(self):
        self.ignoreErrors = self.chkIgnoreErrors.isChecked()
        lpuCode = forceString(QtGui.qApp.db.translate(
            'Organisation', 'id', QtGui.qApp.currentOrgId(), 'OGRN'))

        if not lpuCode:
            self.log(u'<b><font color=red>ОШИБКА<\font><\b>:'
                     u'Для текущего ЛПУ не задан ОГРН', True)
            if not self.ignoreErrors:
                return

        lpuOKATO = forceString(QtGui.qApp.db.translate(
            'Organisation', 'id', QtGui.qApp.currentOrgId(), 'OKATO'))

        if not lpuOKATO:
            self.log(u'<b><font color=red>ОШИБКА<\font><\b>:'
                     u'Для текущего ЛПУ не задан ОКАТО', True)
            if not self.ignoreErrors:
                return

        
        accDate, accNumber, exposeDate, contractId,  payerId, aDate, aAmount =\
            getAccountInfo(self.parent.accountId)

        contractBegDate = forceDate(QtGui.qApp.db.translate(
            'Contract', 'id', contractId , 'begDate'))
        self.contractBegDate = contractBegDate
        out, query, clientsFile, accountFile = self.prepareToExport(contractBegDate)
        payerCode = None

        if payerId:
            payerCode = forceString(QtGui.qApp.db.translate(
                    'Organisation', 'id', payerId, 'miacCode'))

        if not payerCode:
            self.log(u'<b><font color=red>ОШИБКА<\font><\b>:'
                     u'Для плательщика не задан код МИАЦ', True)
            if not self.ignoreErrors:
                return

        self.recNum = 1

        if self.idList:
            file = out
            out = CMyXmlStreamWriter(self)
            clientsOut = CPersonalDataStreamWriter(self)
            out.setCodec(QTextCodec.codecForName('cp1251'))
            clientsOut.setCodec(QTextCodec.codecForName('cp1251'))
            miacCode = forceString(QtGui.qApp.db.translate(
                'Organisation', 'id', QtGui.qApp.currentOrgId(), 'miacCode'))
#TODO: Переделать хранимку updateAccount
            accSum = forceDouble(QtGui.qApp.db.translate(
                'Account', 'id', self.parent.accountId, 'sum'))
            out.writeFileHeader(file, self.parent.getFullXmlFileName(), accNumber, aDate,
                                forceString(accDate.year()),
                                forceString(accDate.month()),
                                miacCode, payerCode, accSum, aAmount, contractBegDate, contractId)
            clientsOut.writeFileHeader(clientsFile, self.parent.getFullXmlFileName(), aDate, contractBegDate)
            eventsInfo = self.getEventsSummaryPrice()
            while query.next():
                QtGui.qApp.processEvents()
                if self.aborted:
                    break
                self.progressBar.step()
                out.writeRecord(query.record(), self.log, miacCode, eventsInfo, self.parent.accountId, contractBegDate, contractId)
                clientsOut.writeRecord(query.record(), contractBegDate, self.log)

            out.writeFileFooter()
            clientsOut.writeFileFooter()

            file.close()
            clientsFile.close()
            if self.parent.page1.type == 1:
                pass
            elif self.parent.page1.chkExportTypeBelonging.isChecked() == False and contractBegDate > QDate(2015, 12, 31):
                accountOut = CAccountDataStreamWriter(self)
                accountOut.setCodec(QTextCodec.codecForName('cp1251'))
                accountOut.writeFileHeader(accountFile, self.parent.getFullXmlFileName(), accDate)
                accountOut.writeRecord(contractId, payerId, aDate, accNumber, self.parent.getFullXmlFileName(), 
                                       forceString(accDate.year()), forceString(accDate.month()), accSum, self.log)
                accountOut.writeFileFooter()
                accountFile.close()
            fout = open(self.parent.getFullXmlFileName()+'_out', 'a')
            self.progressBar.setValue(0)
            for line in open(self.parent.getFullXmlFileName(), "r"):

                if str(line).find('<SD_Z>dummy</SD_Z>') != -1:
                    fout.write(str(line).replace('<SD_Z>dummy</SD_Z>',
                                                 '<SD_Z>'
                                                 +
                                                    str('%15.0f' % int(container.summCaseTotal)).strip()
                                                 +
                                                 '</SD_Z>'))
                    self.progressBar.step()
                else:
                    fout.write(line)
                    self.progressBar.step()
 
            fout.close()
 
            os.remove(self.parent.getFullXmlFileName())
            os.rename(self.parent.getFullXmlFileName()+'_out', self.parent.getFullXmlFileName())
 
 
            container.summTotal = 0
            container.summCaseTotal = 0
            container.dictSums = {1 : 0.0}
            container.date = {1: (2000, 1, 1)}

        else:
            self.log(u'Нечего выгружать.')
            self.progressBar.step()


# *****************************************************************************************


    def createXML(self, contractBegDate):
        outFile = QFile(self.parent.getFullXmlFileName())
        outFile.open(QFile.WriteOnly | QFile.Text)
        outFile2 = QFile( self.parent.getFullXmlPersFileName())
        outFile2.open(QFile.WriteOnly | QFile.Text)
        if self.parent.page1.chkExportTypeBelonging.isChecked() == False and self.parent.page1.contractBegDate > QDate(2015, 12, 31) and self.parent.page1.type == 0:
            outFile3 = QFile( self.parent.getFullXmlAccFileName())
            outFile3.open(QFile.WriteOnly | QFile.Text)
        else:
            outFile3 = None
        return outFile, outFile2, outFile3



# *****************************************************************************************

    def isComplete(self):
        return self.done


    def abort(self):
        self.aborted = True


    @pyqtSignature('')
    def on_btnExport_clicked(self):
        self.export()


    @pyqtSignature('')
    def on_btnCancel_clicked(self):
        self.abort()


# *****************************************************************************************

class CExportPage2(QtGui.QWizardPage, Ui_ExportPage2):
    def __init__(self, parent):
        QtGui.QWizardPage.__init__(self, parent)
        self.parent = parent #wtf? скрывать Qt-шный parent - это плохая затея
        self.setupUi(self)
        self.setTitle(u'Экспорт данных реестра по счёту')
        self.setSubTitle(u'для выполнения шага нажмите кнопку "финиш"')

        self.pathIsValid = True
        homePath = QDir.toNativeSeparators(QDir.homePath())
        exportDir = forceString(QtGui.qApp.preferences.appPrefs.get('ExportR29XMLExportDir', homePath))
        self.edtDir.setText(exportDir)

    def isComplete(self):
        return self.pathIsValid


    def validatePage(self):
        success = False
        baseName = os.path.basename(self.parent.getFullXmlFileName())
        (root, ext) = os.path.splitext(baseName)
        zipFileName = '%s.zip' % root
        zipFilePath = os.path.join(forceStringEx(self.parent.getTmpDir()),
                                                zipFileName)
        zf = ZipFile(zipFilePath, 'w', allowZip64=True)

        if self.parent.page1.chkExportTypeBelonging.isChecked() == False  and self.parent.page1.contractBegDate > QDate(2015, 12, 31) and self.parent.page1.type == 0:
            for src in (self.parent.getFullXmlFileName(),  self.parent.getFullXmlPersFileName(), self.parent.getFullXmlAccFileName() ):
                zf.write(src, os.path.basename(src), ZIP_DEFLATED)
        else:
            for src in (self.parent.getFullXmlFileName(),  self.parent.getFullXmlPersFileName()):
                zf.write(src, os.path.basename(src), ZIP_DEFLATED)


        zf.close()

        dst = os.path.join(forceStringEx(self.edtDir.text()), zipFileName)
        success, result = QtGui.qApp.call(self, shutil.move, (zipFilePath, dst))

        if success:
            QtGui.qApp.preferences.appPrefs['ExportR29XMLExportDir'] = toVariant(self.edtDir.text())
            QtGui.qApp.preferences.appPrefs['ExportR29XMLRegistryNumber'] = \
                    toVariant(self.parent.page1.edtRegistryNumber.value())
        #    self.wizard().setAccountExposeDate()

        return success


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
                u'Выберите директорий для сохранения файла выгрузки в ОМС Архангельской области',
                 forceStringEx(self.edtDir.text()),
                 QtGui.QFileDialog.ShowDirsOnly)
        if forceString(dir):
            self.edtDir.setText(QDir.toNativeSeparators(dir))

# *****************************************************************************************

class CMyXmlStreamWriter(QXmlStreamWriter, CExportHelperMixin):
    def __init__(self, parent):
        QXmlStreamWriter.__init__(self)
        CExportHelperMixin.__init__(self)
        self.parent = parent
        self.setAutoFormatting(True)
        self.recNum = 1 # номер записи
        self.caseNum = 1 # номер случая
        self.serviceNum = 1 # номер услуги
        self.summ = 0.0
        self.medicalAidKind = 0
        self.dateNum = 1
        self.ossString = ''
        self._lastClientId = None
        self._lastEventId = None
        self._lastActionId = None
        self._ActionId = None
        self.ossString = ""
        self.medicalAidProfileCache = {}
        self.rbPostFederalCache= {}
        self.rbPostRegionalCache = {}
        self.childrenNumber =0 


    def getStandartServiceIds(self):
        stmt = u"SELECT id FROM rbService WHERE name LIKE 'стандарт%медицинской%помощи%'"
        query = QtGui.qApp.db.query(stmt)
        while query.next():
            yield forceInt(query.record().value('id'))

    def writeRecord(self, record, log, miacCode, eventsInfo, accountId, contractBegDate, contractId):
        #Если есть более одного движения, и текущий action в строке не последний, то просто выкидываемся из метода
        hospitalDayAmount = 0
        eventId = forceInt(record.value('event_id'))
        actionId = forceInt(record.value('action_id'))
        accountItemId = forceInt(record.value('accountItemId'))
        latestMoveServiceId, latestaccItemId = Export29XMLCommon.getLatestActionMove(QtGui.qApp.db, accountId, eventId)
        latestMoveFlag = False
        if latestMoveServiceId and latestaccItemId:
            if (forceInt(record.value('serviceId')) != latestMoveServiceId or \
                accountItemId != latestaccItemId):
                return
            else:
                latestMoveFlag = True #необходим, чтобы ниже учесть возможные тонкости, например с amount = totalAmount

        clientId = forceRef(record.value('client_id'))
        age = forceInt(record.value('clientAge'))
        serviceNote = (forceString(QtGui.qApp.db.translate(QtGui.qApp.db.table('rbService'), 'id', forceInt(record.value('serviceId')), 'note')).split(";"))
        if forceInt(record.value('preEventId')) and 'isSelfCase' not in serviceNote:
            begDate = self.getDateForOneCase(forceInt(record.value('preEventId')))
            if not begDate:
                begDate = forceDate(record.value('begDateEvent'))
        else:
            begDate = forceDate(record.value('begDateEvent'))
        self.parent.endDate=begDate
        if record.value('endDateEvent'): endDate = forceDate(record.value('endDateEvent'))
        else:
            endDate = forceDate(Export29XMLCommon.getLatestDateOfVisitOrAction(QtGui.qApp.db, accountId, eventId))
        federalPrice = forceDouble(record.value('federalPrice'))
        regionalPrice = forceDouble(record.value('regionalPrice'))

        regionalSum = Export29XMLCommon.doubleToStrRounded(forceDouble(record.value('regionalSum')))
        personId = forceRef(record.value('execPersonId'))
        profile = self.getProfile(forceRef(record.value('serviceId')), personId)
        profileStr = (profile if profile else forceString(record.value('medicalAidProfileFederalCode')))[:3]
        amount = forceDouble(record.value('amount'))
        oss = ''
        if self._lastClientId != clientId  or (self._lastEventId != eventId and self._lastEventId != forceInt(record.value('preEventId'))): # новая запись, иначе - новый случай
            if self._lastClientId:
                self.caseNum += 1
                self.recNum += 1
                self.writeTextElement('COMENTSL', self.ossString)
                
                self.ossString = ''
                self.writeEndElement()
                if not forceString(record.value('medicalAidUnitFederalCode')):
                    pass
                self.writeTextElement('IDSP', forceString(record.value('medicalAidUnitFederalCode')))
                if forceString(record.value('medicalAidUnitFederalCode')) == '':
                    log(u'Выгрузка пациента (Код: %s) в догворе не указаны ед.учета мед. помощи '%(clientId), True)
                self.writeTextElement('SUMV', '%10.2f' % self.summ)
                self.writeBenefits(self._lastClientId, self._lastEventId)
                self.summ = 0.0
                self.writeEndElement() # SLUCH
                self.writeEndElement() # ZAP
                self._lastEventId = None
            self._lastClientId = clientId

            self.writeStartElement('ZAP')

            self.writeTextElement('N_ZAP', ('%4d' % self.recNum).strip())
            self.writeTextElement('PR_NOV', '0')
            self.writeStartElement('PACIENT')
            self.writeTextElement('ID_PAC',  ('%d' % clientId)[:36])
            if self.parent.chkClientLog.isChecked():
                log(u'Выгрузка пациента (Код: %s) '%(clientId), True)

            # Региональный код справочника ВИДЫ ПОЛИСОВ.
            npolis, spolis, vpolis, insurerOGRN, insurerOKATO, insurerName, smo, insurerId = Export29XMLCommon.getClientPolicy(QtGui.qApp.db, clientId, begDate, endDate)

        #    if docCode and  docCode > 1:
        #        oss += u'ОСС=2,'

         #   smo = forceString(record.value('insurerMiac'))[:5]
#Паспорт - ClientDocument ClientDocumentType (паспорт РФ)
#Ориентируемся на ___номер полиса___ и страховую компанию SMO
      #      if ((not npolis) and (not smo) and (docCode == 1)): #предъявил только паспорт
      #          oss += u'ОСС=1,'
            self.writeTextElement('VPOLIS', vpolis)
            if not vpolis:
                log(u'Не указан вид полиса (Код: %s) '%(clientId), True)
            if vpolis == '3':
                self.writeTextElement('ENP', npolis)
            else:
                self.writeTextElement('SPOLIS', spolis)
                self.writeTextElement('NPOLIS', npolis)
         #   self.writeTextElement('NPOLIS', npolis)
            if not npolis:
                log(u'Не указан номер полиса (Код: %s) '%(clientId), True)
            self.writeTextElement('SMO', smo)
            if not smo:
                self.writeTextElement('SMO_OGRN', insurerOGRN)
                self.writeTextElement('SMO_OK', insurerOKATO)
                if not insurerOGRN and not insurerOKATO:
                    if insurerName:
                        self.writeTextElement('SMO_NAM', insurerName, writeEmtpyTag = False)
                    else:
                        log(u'В регистрационной карточке пациента нет действуйствующий страховой на начало случая (Код: %s) '%(clientId), True)
            birthDate = forceDate(record.value('birthDate'))
            
            if '0009' in Export29XMLCommon.getSpecialCaseCode(QtGui.qApp.db, clientId, begDate):
                self.childrenNumber = self.childrenNumber + 1
                self.writeTextElement('NOVOR', '%s%s%s' % (forceString(record.value('sex'))[:1], birthDate.toString('ddMMyy'), self.childrenNumber ))
                 
            
            elif '0003' in Export29XMLCommon.getSpecialCaseCode(QtGui.qApp.db, clientId, begDate):
                self.childrenNumber = 1

                self.writeTextElement('NOVOR', '%s%s%s' % (forceString(record.value('sex'))[:1], birthDate.toString('ddMMyy'), self.childrenNumber ))

            
            else:
                self.writeTextElement('NOVOR', '0')
            
            self.writeEndElement() # PACIENT

#        if self._lastEventId != eventId:
#            if self._lastEventId:
     #           self.caseNum+= 1
#                self.writeBenefits(clientId, eventId)
#                self.writeEndElement() # SLUCH
#                self.writeEndElement() # SLUCH

            serviceId = forceRef(record.value('serviceId'))
            serviceStr = self.getServiceInfis(serviceId)
            serviceNote = (forceString(QtGui.qApp.db.translate(QtGui.qApp.db.table('rbService'), 'id', serviceId, 'note')).split(";"))
            if forceString(record.value('pgCode')) != '' and forceString(record.value('pgCode')) != ' ':
                serviceStr = serviceStr  + ':' +  forceString(record.value('pgCode'))

            serviceGroupCode = forceString(record.value('serviceGroupCode'))

            eventTypeCode = forceString(record.value('eventTypeCode'))

            visitId = forceInt(record.value('visit_id'))
            if (serviceStr[:4] == '3.2.' or serviceStr[:4] == '3.1.' or serviceStr[:4] == '3.3.'):
                begDate = endDate = Export29XMLCommon.getDatesForConsultVisit(QtGui.qApp.db, visitId)
            self._lastEventId = forceInt(record.value('preEventId'))  if forceInt(record.value('preEventId')) else eventId
            self._lastActionId = actionId
            self.writeStartElement('Z_SL')
            self.writeTextElement('IDCASE', '%d' % self.caseNum)
            self.writeTextElement('VIDPOM', forceString(record.value('medicalAidKindCode')))
            if forceString(record.value('medicalAidKindCode')) == '':
                log(u'Не указан вид медицинской помощи (Код  карточки: %s) '%(eventId), True)
            directionEIRNumber, flagDirection, flagExpertise, flagOncology = Export29XMLCommon.getDirectionEIRNumber(QtGui.qApp.db, eventId)

            self.writeTextElement('LPU', miacCode[:6])
            if miacCode == '':
                log(u'Не указан код организации (Код  карточки: %s) '%(eventId), True)
            strContractNote = forceString(QtGui.qApp.db.translate('Contract', 'id', contractId , 'note'))
            self.writeTextElement('VBR', '1' if 'isMobile' in serviceNote or 'isMobile' in strContractNote.split(';') else '0')

            self.writeTextElement('DATE_Z_1', begDate.toString(Qt.ISODate))
            if not begDate:
                log(u'Не указана даты начала события (Код  карточки: %s) '%(eventId), True)
            self.writeTextElement('DATE_Z_2', endDate.toString(Qt.ISODate))
            if not endDate:
                log(u'Не указана дата окончания события (Код  карточки: %s) '%(eventId), True)
            
            if actionId:
                if self.isActionCancelled(actionId) == True:
                    self.writeTextElement('P_OTK', '1')
                else:
                    self.writeTextElement('P_OTK', '0')
            else:
                self.writeTextElement('P_OTK', '0')
            self.writeTextElement('RSLT_D', forceString(record.value('eventResultFederalCode')))
            if forceString(record.value('eventResultFederalCode')) == '':
                log(u'Не указана результат в событии (Код  карточки: %s) '%(eventId), True)            
            if '0003' in Export29XMLCommon.getSpecialCaseCode(QtGui.qApp.db, clientId, begDate) or '0009' in Export29XMLCommon.getSpecialCaseCode(QtGui.qApp.db, clientId, begDate):
                self.writeTextElement('OS_SLUCH', '1')
            if  '0005' in Export29XMLCommon.getSpecialCaseCode(QtGui.qApp.db, clientId, begDate):
                self.writeTextElement('OS_SLUCH', '2')
                
            self.writeStartElement('SL')
            self.writeTextElement('SL_ID', ('%s' % uuid.uuid4()))
            if contractBegDate  > QDate(2019, 10, 30):
                self.writeTextElement('SID_MIS', ('%s' % eventId))
            lpu1Str = Export29XMLCommon.getMobileModule(QtGui.qApp.db, forceDouble(miacCode)) if eventTypeCode[:2] == '04' else ''
            self.writeTextElement('LPU_1', lpu1Str, writeEmtpyTag = False) #У Т(6) Подразделение МО Подразделение МО лечения из регионального справочника 
            self.writeTextElement('NHISTORY', ('%d' % eventId)[:50])
            self.writeTextElement('DATE_1', begDate.toString(Qt.ISODate))
            self.writeTextElement('DATE_2', endDate.toString(Qt.ISODate))
            self.writeTextElement('DS1',forceString(record.value('MKB')).replace(' ', ''))
            if forceString(record.value('diagChatacter')) == '2':
                   self.writeTextElement('DS1_PR','1') 
            flagOncology1 = Export29XMLCommon.isOncology(QtGui.qApp.db, eventId)
            self.writeTextElement('DS_ONK', forceString(flagOncology1) if forceString(flagOncology1) else '0')
            if forceString(record.value('dispanserStatus')) != '0':
                self.writeTextElement('PR_D_N', forceString(record.value('dispanserStatus')))
            accDiag = self.getAccDiag(eventId)
            if accDiag != {}:
                for mkb, type in accDiag.items():
                    self.writeStartElement('DS2_N')
                    self.writeTextElement('DS2',forceString(mkb))
                    if type[0] != 0:
                        if type[0] == '2':
                            self.writeTextElement('DS2_PR','1') 
                        if type[1] != '2':
                            if int(type[1]) > 2:
                                self.writeTextElement('PR_DS2_N', '3')
                            else:
                                self.writeTextElement('PR_DS2_N',forceString(type[1]))
                    self.writeEndElement() # DS2_N
            (totalAmount,  totalSum) = eventsInfo[eventId]

            
            
            directions = self.getDirection(forceString(record.value('eventId1')),  forceString(record.value('preEventId')) , log)
            i =0
            if directions:
                iddkt = ''
                if forceString(flagOncology1) == '1':
                    if contractBegDate < QDate(2021, 07, 01):
                        orderDir = ['NAZ_IDDOKT','NAZ_SP', 'NAZ_V', 
                                'NAZ_USL','NAPR_DATE','NAPR_MO','NAZ_PMP',
                                 'NAZ_PK', 'NAZ_DATE']
                    else:
                        orderDir = ['NAZ_IDDOKT', 'NAZ_V', 
                                'NAZ_USL','NAPR_DATE','NAPR_MO','NAZ_PMP',
                                 'NAZ_PK', 'NAZ_DATE']
                else:
                    orderDir = ['NAZ_SP', 'NAZ_V', 'NAZ_USL',
                                # 'NAPR_DATE','NAPR_MO',
                                'NAZ_PMP', 'NAZ_PK']

                for dir in directions.values():
                    i =i+1
                    self.writeStartElement('NAZ')
                    self.writeTextElement('NAZ_N', forceString(i))
                    self.writeTextElement('NAZ_R', forceString(dir["NAZR"]))
                    for tag in orderDir:
                        if tag in dir.keys():
                            if forceString(flagOncology1) != '1' and tag != 'NAPR_MO':
                                self.writeTextElement(tag, forceString(dir[tag]))  
                    self.writeEndElement() #  NAZ 
                    if forceString(flagOncology1) == '1':
                        iddkt = dir['iddokt']
                self.writeTextElement('IDDOKT', iddkt)
                    
            
            
         #   self.writeTextElement('ED_COL', '1' )
         #   self.writeTextElement('TARIF', forceString(record.value('price')))
            self.summ = forceDouble(QtGui.qApp.db.getSum(QtGui.qApp.db.table('Account_Item'), 
                                                        'sum', '(event_id = %s or event_id = %s) and master_id = %d'
                                                     # 'sum', '(event_id = %s ) and master_id = %d'
                                                        %(eventId, forceString(record.value('preEventId')), accountId)))
                                                     # %(eventId,  accountId)))
            self.medicalAidKind = forceString(record.value('medicalAidUnitFederalCode'))
            self.writeTextElement('SUM_M', forceString(self.summ))
            relId = forceInt(record.value('relativeId'))


            container.dictSums[self.caseNum] = 0.0
            
        serviceId = forceRef(record.value('serviceId'))
        serviceStr = self.getServiceInfis(serviceId)
        if forceString(record.value('pgCode')) != '' and forceString(record.value('pgCode')) != ' ':
            serviceStr = serviceStr  + ':' +  forceString(record.value('pgCode'))
        serviceGroupCode = forceString(record.value('serviceGroupCode'))
        serviceId = forceRef(record.value('serviceId'))
        eventTypeCode = forceString(record.value('eventTypeCode'))


        lpu1Str = Export29XMLCommon.getMobileModule(QtGui.qApp.db, forceDouble(miacCode)) if eventTypeCode[:2] == '04' else ''
        price = forceDouble(record.value('price')) - regionalPrice - federalPrice

        #TODO: Duplicate code! Fix!
        (totalAmount,  totalSum) = eventsInfo[eventId]
        composition, totalpercents = self.getContractCompositionInfo(forceString(record.value('contractTariffId')))

        summ = Export29XMLCommon.doubleToStrRounded(amount * price)
        container.summTotal +=                  Export29XMLCommon.doubleToStrRounded(summ + regionalSum+  totalpercents*amount)
        container.dictSums[self.caseNum] += Export29XMLCommon.doubleToStrRounded(summ + regionalSum+  totalpercents*amount)
        container.summCaseTotal =self.caseNum

#По требованию фомса, если было более 1 движения, записываем amount и сумму по всем услугам
#если мы достигли этого участка кода - значит автоматически предполагается, что речь идет о самом последнем action-е

        self.writeServices(contractBegDate, record, log, miacCode, age, profileStr, serviceStr, serviceGroupCode, price,
                           amount, summ, latestMoveFlag, lpu1Str, personId, serviceId, eventId, regionalPrice, 
                           1 if (serviceStr[:4] == '3.18' or serviceStr[:4] == '3.23' or serviceStr[:4] == '3.25' 
                                 or serviceStr[:4] == '3.20' or serviceStr[:4] == '3.36' or serviceStr[:4] == '3.98'
                                 or serviceStr[:4] == '3.96' or serviceStr[:4] == '3.97' 
                                 or serviceStr[:4] == '3.12'
                                 or serviceStr[:4] == '3.13'
                                 or serviceStr[:4] == '3.14') else None, None, actionId)
   #     self.writeTextElement('ED_COL', '1' )

        
        oss = forceString(QString(oss[:-1]))
        
        self.ossString += oss

    def writeServices(self, contractBegDate, record, log, miacCode, age, profileStr, serviceStr, serviceGroupCode, price, amount,
                      summ, latestMoveFlag, lpu1Str, personId,  serviceId, eventId, regionalPrice = None, hasVirtual=None,
                       visitId = None, actionId= None):
        self.writeService(contractBegDate, record, log,
                          miacCode,
                          age,
                          profileStr,
                          serviceStr,
                          price,
                          amount,
                          summ,
                          latestMoveFlag,
                          lpu1Str,
                          visitId, actionId)
        if hasVirtual:
            serviceCodes = []
            visits = {}
            visits = self.getVisits(eventId)
            visitPrice = 0.0
            for visitId, service in visits.items():
                personId, codeMd = Export29XMLCommon.getPcode(QtGui.qApp.db, record, visitId)
                if service:
                    if service not in serviceCodes and service[2]== '2':
                        self.writeService(contractBegDate, record,
                                      log, 
                              miacCode, 
                              age, 
                              profileStr, 
                              service,
                              visitPrice,
                              1,
                              visitPrice,
                              latestMoveFlag,
                              lpu1Str,
                              visitId)
                    serviceCodes.append(service)
            visitId = None

            actions = self.getActions(eventId)

            if actions != {} and self._ActionId != actions.keys()[-1]:

                visitId = ''
                for actionId in actions.keys():
                    self._ActionId = actionId
                    actionPrice = 0.0
                    service = self.getServicesOfAction(actionId)


                    if service and service not in serviceCodes:
                        self.writeService(contractBegDate, record, log,
                                      miacCode,
                                      age,
                                      profileStr,
                                      service,
                                      actionPrice,
                                      amount,
                                      actionPrice,
                                      latestMoveFlag,
                                      lpu1Str,
                                      visitId,
                                      actionId)
                        serviceCodes.append(service)



    def writeService(self, contractBegDate, record, log, miacCode, age, profileStr, serviceStr, price, amount,
                     summ, multiplyMovementLogicFlag,  lpu1Str='', visitId = '', actionId ='',
                     compCode = None, ):
        self.writeStartElement('USL')
        self.writeTextElement('IDSERV',  ('%8d' % self.serviceNum).strip()) # O N(8) номер записи в реестре услуг
        if contractBegDate  > QDate(2019, 10, 30):
                self.writeTextElement('UID_MIS',  ('%8d' %forceInt(record.value('accountItemId'))).strip())
        self.writeTextElement('LPU', miacCode[:6]) #O Т(6) Код МО МО лечения
        self.writeTextElement('LPU_1', lpu1Str, writeEmtpyTag = False) #У Т(6) Подразделение МО Подразделение МО лечения из регионального справочника
        dateIn = None
        dateOut = None
        db = QtGui.qApp.db

        dateIn = forceDate(record.value('begDateEvent'))
        dateOut = forceDate(record.value('endDateEvent'))

        if (Export29XMLCommon.isRegionalAdditionalPay(db, serviceStr) == True):
            dateIn = forceDate(record.value('begDateEvent'))
            dateOut = forceDate(record.value('endDateEvent'))

#        if forceInt(record.value('action_id')):
#            (dateIn, dateOut) = Export29XMLCommon.getDatesForAction(db,
#                                                                    forceInt(record.value('event_id')),
#                                                                    forceInt(record.value('action_id')),
#                                                                    serviceStr)
        elif (visitId and visitId != 0):
            dateIn = dateOut = self.getDateForVisits(visitId)

        if not dateIn and not dateOut:
            dateIn  = forceDate(record.value('dateVisit'))
            dateOut = forceDate(record.value('dateVisit'))

#        if dateOut and dateIn and actionId:
        if actionId:
            dateIn, dateOut = self.getDateForActions(actionId)
            if not dateOut:
                dateOut=dateIn
            elif not dateIn:
                dateIn = dateOut


        self.writeTextElement('DATE_IN', dateIn.toString(Qt.ISODate)) #O D Дата начала оказания услуги
        self.writeTextElement('DATE_OUT', dateOut.toString(Qt.ISODate)) #O D Дата окончания оказания услуги

#        self.writeTextElement('DS', forceString(record.value('MKB'))) #O Т(10) Диагноз Код из справочника МКБ до уровня подрубрики
        if actionId:
            if self.isActionCancelled(actionId) == True:
                self.writeTextElement('P_OTK', '1')
            else:
                self.writeTextElement('P_OTK', '0')
        else:
            self.writeTextElement('P_OTK', '0')
            
        if (serviceStr.lower().find('a16') != -1):
            pass

        if not compCode:
            self.writeTextElement('CODE_USL', serviceStr) #O Т(16) Код услуги Территориальный классификатор услуг
        else:
            self.writeTextElement('CODE_USL', compCode)

#        self.writeTextElement('KOL_USL', ('%6.2f' % amount).strip() ) #O N(6.2) Количество услуг (кратность услуги)
        self.writeTextElement('TARIF', ('%15.2f' % summ).strip()) #O N(15.2) Тариф
  #      self.writeTextElement('ST_USL', ('%15.2f' % summ).strip())
        self.writeTextElement('SUMV_USL', ('%15.2f' % summ).strip()) #O N(15.2) Стоимость медицинской услуги, выставленная к оплате (руб.)
#        self.writeTextElement('PRVS', forceString(self.parent.getPersonSpecialityFederalCode(forceRef(record.value('execPersonId'))))) #O N(9) Специальность медработника, выполнившего услугу
        if visitId == 1 or visitId== 0: visitId = None
        personId, codeMd = Export29XMLCommon.getPcode(db, record, visitId)
        if contractBegDate < QDate(2021, 07, 01):
            self.writeTextElement('PRVS', forceString(self.parent.getPersonSpecialityFederalCode(personId)))
            self.writeTextElement('CODE_MD', codeMd)
        else:
            self.writeStartElement('MR_USL_N')
            self.writeTextElement('MR_N', '1')
            self.writeTextElement('PRVS', forceString(self.parent.getPersonSpecialityFederalCode(personId)))
            self.writeTextElement('CODE_MD', codeMd)
            self.writeEndElement() # MR_USL_N
        if not personId:
            log(u'В событии %d у пациента %d не указан исполнитель у услуги %s' % (forceInt(record.value('eventId')), forceInt(record.value('client_id')), serviceStr), True)
        if not codeMd and personId:
            code = forceString(QtGui.qApp.db.translate('Person', 'id', personId, 'code'))
            log(u'В регистрационной карточке сотрудника (Код: %s) не указан СНИЛС - Справочники-Персонал-Сотрудники-Вкладка "Личные"- поле "СНИЛС" \n'%(code), True)
        if actionId:
            if self.isActionCancelled(actionId) == True:
                self.writeTextElement('COMENTU', u'ОТКАЗ' )
        self.writeEndElement() #USL
        self.serviceNum += 1
        
    def writeBenefits(self, clientId, eventId):            
            codes = Export29XMLCommon.getBenefitsType(self, clientId)
            osses = Export29XMLCommon.getOss(self, eventId, "'med.abort', 'protivoprav'")
            trombs = Export29XMLCommon.getOss(self, eventId, "'TLIZ'")
            isCancel = Export29XMLCommon.getCanses(self, eventId)
            if codes != [] or  osses != [] or isCancel == 1 or trombs != []:
                self.writeStartElement('DSVED')
                for oss in osses:
                    self.writeTextElement('OSS', forceString(oss))
                for code in codes:
                    self.writeTextElement('LGOTA', forceString(code))
                for tr in trombs:
                    self.writeTextElement('TLIZ', forceString(tr))
                if isCancel == 1:
                     self.writeTextElement('P_OTK2', u'1')
                self.writeEndElement() # DSVED


    def writeFileHeader(self,  device, fileName, accNumber, accDate, year, month, miacCode, payerCode, accSum, aAmount, contractBegDate, contractId):
        self.recNum = 1
        self.caseNum = 1
        self._lastClientId = None
        self.serviceNum = 1
        self.setDevice(device)
        self.writeStartDocument()
        self.writeStartElement('ZL_LIST')
        self.writeHeader(fileName, accNumber, accDate, year, month, miacCode, payerCode, accSum, aAmount, contractBegDate, contractId)


    def writeHeader(self, fileName, accNumber, accDate, year, month,
                     miacCode, payerCode, accSum, aAmount, contractBegDate, contractId):
        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION',  '3.2.0' if contractBegDate < QDate(2021, 07, 01) else '3.2.1')
        self.writeTextElement('DATA', accDate.toString(Qt.ISODate))
        (fname,  ext) = os.path.splitext(os.path.basename(fileName))
        self.writeTextElement('FILENAME', fname[:26])
        self.writeTextElement('SD_Z', forceString('dummy'))
        self.writeEndElement()

        if not self.parent.chkExportTypeBelonging.isChecked():
            self.writeStartElement('SCHET')
#            self.writeTextElement('CODE', ('%s%s' % (miacCode[-4:], accNumber.rjust(4, '0'))))
            self.writeTextElement('CODE', ('%d' % self.parent.parent.accountId)[:8])
            self.writeTextElement('CODE_MO', miacCode)
            self.writeTextElement('YEAR', year)
            self.writeTextElement('MONTH',  month)
            if self.parent.type == 0:
                self.writeTextElement('NSCHET',  forceString(accNumber)[:15])
                self.writeTextElement('DSCHET', accDate.toString(Qt.ISODate))
            if payerCode != '29':
                self.writeTextElement('PLAT', payerCode[:5], writeEmtpyTag = False)
#TODO: MOVE IT BACK!
#Примечание. Чтобы быстро изменить итоговую сумму придется пойти на этот быдлокод
#Затем мы все заменим на хранимки
#P.S. хранимка требует дебага. Да, я dummy и мне стыдно
#однако сейчас СРОЧНО необходимо, чтобы общая сумма где-то считалась
#            self.writeTextElement('SUMMAV', (caccSum).strip())
         #   self.writeTextElement('SUMMAV', 'dummy')
            self.writeTextElement('SUMMAV',('%10.2f' % round(accSum,2)).strip())
            dispType = None
          #  (date, number, exposeDate, contractId,  payerId,  aDate, aAmount) = getAccountInfo(self.accountId)
            strContractNote = forceString(QtGui.qApp.db.translate('Contract', 'id', contractId , 'note')).split(';')[0]
            
            if strContractNote != '':

                dispType = {
                                      'DP3': lambda x : u'ДВ1',
                                      'DP4': lambda x : u'ДВ4',
                                      'DP2': lambda x : u'ДВ3',
                                      'DP': lambda x : u'ДВ4',
                                      'DV': lambda x : u'ДВ2',
                                      'DO': lambda x : u'ОПВ',
                                      'DS': lambda x : u'ДС1',
                                      'DU': lambda x : u'ДС2',
                                      'DF': lambda x : u'ПН1',
                                      'DD': lambda x : u'ОН2',
                                      'DR': lambda x : u'ОН3',
                                      'DA': lambda x : u'УД1',
                                      'DB': lambda x : u'УД2'
                                }[strContractNote](dispType)
                  
                self.writeTextElement('DISP', dispType)
                if      u'НСЗ' in forceString(accNumber):
                    self.writeTextElement('IFIN', u'НСЗ')
                elif    u'ПР' in forceString(accNumber):
                    self.writeTextElement('IFIN', u'ПР')
                elif    u'НП' in forceString(accNumber):
                    self.writeTextElement('IFIN', u'НП')
                elif    u'ФП' in forceString(accNumber):
                    self.writeTextElement('IFIN', u'ФП')
                elif    u'ЛИ' in forceString(accNumber):
                    self.writeTextElement('IFIN', u'ЛИ')
                elif    u'МБТ' in forceString(accNumber):
                    self.writeTextElement('IFIN', u'МБТ')
                elif    u'ТМ' in forceString(accNumber):
                    self.writeTextElement('IFIN', u'ТМ')
                elif    u'КОВ' in forceString(accNumber):
                    self.writeTextElement('IFIN', u'КОВ')
                elif    u'ПЦР' in forceString(accNumber):
                    self.writeTextElement('IFIN', u'ПЦР')
                
                else:
                    self.writeTextElement('IFIN', '', writeEmtpyTag = True)
            self.writeEndElement()

    def writeTextElement(self, element,  value, writeEmtpyTag = False):
        if not writeEmtpyTag and (not value or value == ''):
            return
        QXmlStreamWriter.writeTextElement(self, element, value)

    def writeFileFooter(self):
        self.writeTextElement('COMENTSL', self.ossString)
        
        self.writeEndElement() # SLUCH
        if self.summ > 0:
            self.writeTextElement('IDSP',self.medicalAidKind)
            self.writeTextElement('SUMV',('%10.2f' % round(self.summ,2)).strip())
        self.writeBenefits(self._lastClientId, self._lastEventId)
        self.writeEndElement() # root
        self.writeEndDocument()

#TODO: Remove this out from there!
#TODO: Understand what happens with grouping!
    def getAmountByAccId(self, accItemId):
        db = QtGui.qApp.db
        stmt = """SELECT `amount` FROM `Account_Item`
                  WHERE `Account_Item`.`id` = %s
                  GROUP BY `Account_Item`.`event_id`"""
        query = db.query(stmt % str(accItemId))
        if query.next():
            record = query.record()
        return forceDouble(record.value(0))

    def getBenefitsType(self, clientId):
        stmt = """SELECT rbSocStatusType.code as code
                        FROM `ClientSocStatus`
                        LEFT JOIN rbSocStatusType ON rbSocStatusType.id = `ClientSocStatus`.`socStatusType_id`
                        WHERE `client_id` =  %s""" % clientId
        query = QtGui.qApp.db.query(stmt)
        if query:
            codeR = 3
            while query.next():
                record = query.record()
                code = forceString(record.value('code'))
                if code == u'010':
                    codeR = 1
                elif code == u'050':
                    codeR = 2
        return codeR



    def getContractCompositionInfo(self, contractTariffId):
        stmt = """SELECT `sum`, `code` FROM `Contract_Tariff`
                LEFT JOIN `Contract_CompositionExpense` ON `Contract_CompositionExpense`.master_id = `Contract_Tariff`.id
                LEFT JOIN `rbExpenseServiceItem` ON `rbExpenseServiceItem`.id = `Contract_CompositionExpense`.rbTable_id
                WHERE `Contract_Tariff`.id = %s""" % contractTariffId
        query = QtGui.qApp.db.query(stmt)
        if query:
            compose = {}
            sumpercents = 0
            while query.next():
                record = query.record()
                code = forceString(record.value('code'))
                percent = forceDouble(record.value('sum'))
                if (code and percent):
                    compose[code] = percent
                    sumpercents += percent
        return compose, sumpercents

    def getDateForOneCase(self, preEventId):
        stmt = """SELECT setDate
                  FROM Event
                  LEFT JOIN `EventType` ON `EventType`.`id` = `Event`.`eventType_id`
                  WHERE Event.id = %d and finance_id =2
                  """%(preEventId)
        query = QtGui.qApp.db.query(stmt)
        date = None
        if query and query.first():
            record = query.record()
            if record:
                date = forceDate(record.value(0))
        return date

    def getRelationInfo(self, relId):
        stmt = """SELECT `rbDocumentType`.`code` AS docTypeCode,
                         `rbRelationType`.`code`  AS relTypeCode
                  FROM ClientDocument
                  LEFT JOIN `rbDocumentType` ON `rbDocumentType`.`id` = `ClientDocument`.`documentType_id`
                  LEFT JOIN `ClientRelation` ON `ClientRelation`.`id` = %s
                  LEFT JOIN `rbRelationType` ON `rbRelationType`.`id` = `ClientRelation`.`relativeType_id`
                  WHERE ClientDocument.Client_id IN
                  (SELECT relative_id FROM ClientRelation WHERE
                  id = %s
                  )
                  """%(str(relId), str(relId))
        query = QtGui.qApp.db.query(stmt)
        record = None
        if query and query.first():
            record = query.record()
        return record




    def getProfile(self, serviceId, personId):
        key = (serviceId, personId)
        result = self.medicalAidProfileCache.get(key, -1)

        if result == -1:
#            if serviceId is None or personId is None:
#                print "Shit happens"
            result = None
            stmt = """SELECT rbMedicalAidProfile.regionalCode
            FROM rbService_Profile
            LEFT JOIN rbSpeciality ON rbSpeciality.id = rbService_Profile.speciality_id
            LEFT JOIN Person ON Person.speciality_id = rbSpeciality.id
            LEFT JOIN rbMedicalAidProfile ON rbService_Profile.medicalAidProfile_id = rbMedicalAidProfile.id
            WHERE rbService_Profile.master_id = %d AND Person.id = %d
            """ % (serviceId, personId)

            query = QtGui.qApp.db.query(stmt)

            if query and query.first():
                record = query.record()

                if record:
                    result = forceString(record.value(0))

            self.medicalAidProfileCache[key] = result

        return result

    def getVisits(self, eventId):
        stmt = """SELECT  `Visit`.`id` AS visitId, rbService.code as code
                    FROM  `Visit`
                    LEFT JOIN rbService ON rbService.id = Visit.service_id
                    WHERE  `Visit`.`event_id` =%d AND Visit.deleted !=1
                    """%(eventId)

        query = QtGui.qApp.db.query(stmt)
        if query:
            visits = {}
            while query.next():
                visits[forceInt(query.record().value('visitId'))] = forceString(query.record().value('code'))
            return visits
        else:
            return None

    def getDateForVisits(self, visitId):
        stmt = """SELECT  `date` as dateVisit
                    FROM  `Visit`
                    WHERE  `id` =%s"""%(visitId)
        query =  QtGui.qApp.db.query(stmt)
        if query.next():
            return (forceDate(query.record().value('dateVisit')))
        else:
            return None

    def getDateForActions(self, actionId):
        stmt = """SELECT  `begDate` as begDate, `endDate` as endDate
                    FROM  `Action`
                    WHERE  `id` =%d and deleted =0"""%(actionId)
        query =  QtGui.qApp.db.query(stmt)
        if query.next():
            return (forceDate(query.record().value('begDate'))), (forceDate(query.record().value('endDate')))
        else:
            return None

    def isActionCancelled(self, actionId):
        stmt = """SELECT  `Action`.`status` AS st
                    FROM  `Action`
                    WHERE  `Action`.`id` =%d
                    """%(actionId)
        query = QtGui.qApp.db.query(stmt)
        if query.next():
            st = forceInt(query.record().value('st'))
            if st == 3 or st == 6:
                return True
            else:
                return False
        else:
            return False
        
    def getDirection(self, eventId, eventId1, log):
         stmt = """SELECT Action.id as actionId, 
                            ActionType.code as code, 
                            `ActionProperty_String`.value as type, 
                            ActionPropertyType.descr as name, 
                            ActionType.flatCode as flatCode,
                            Person.`SNILS` as snils,
                            Action.plannedEndDate as plDate,
                            Action.directionDate as dDate
                     FROM `ActionProperty_String`
                     LEFT JOIN ActionProperty ON ActionProperty.id = `ActionProperty_String`.id
                     LEFT JOIN ActionPropertyType ON ActionPropertyType.id = type_id
                     LEFT JOIN ActionType On ActionType.id = ActionPropertyType.actionType_id
                     
                     LEFT JOIN Action ON Action.id = ActionProperty.action_id
                     LEFT JOIN Person  ON Person.id = Action.person_id
                     WHERE flatCode IN ('consultationDirection', 'consultionDirectionToHosp', 
                     'inspectionDirection2018', 'hospitalDirection', 'consultationDirection2018', 
                     'consultionDirectionToHosp2018', 'inspectionDirection2018', 'hospitalDirection2018') 
                      AND Action.deleted =0 AND ActionProperty.deleted = 0  AND Action.status NOT IN (3,6) 
                      AND event_id IN ( %s, %s)  AND ActionPropertyType.descr IN ('NAZ_SP', 'NAZ_V',  'consult', 'CaseAidPlace')
                   """%(eventId, eventId1)
                    
         stmt1 = """SELECT Action.id as actionId, ActionType.code as code, ActionType.flatCode as flatCode,  IF(ActionType.code = '6', rbHospitalBedProfile.regionalCode, rbMedicalAidProfile.regionalCode) as type, ActionPropertyType.descr as name
                     FROM  ActionProperty 
                     LEFT JOIN ActionPropertyType ON ActionPropertyType.id = type_id
                     LEFT JOIN ActionType On ActionType.id = ActionPropertyType.actionType_id
                     LEFT JOIN Action ON Action.id = ActionProperty.action_id
                     LEFT JOIN ActionProperty_rbHospitalBedProfile ON ActionProperty.id = `ActionProperty_rbHospitalBedProfile`.id
                     lEFT JOIN rbHospitalBedProfile ON rbHospitalBedProfile.id = `ActionProperty_rbHospitalBedProfile`.value
                     LEFT JOIN rbMedicalAidProfile ON medicalAidProfile_id = rbMedicalAidProfile.id
                       WHERE  flatCode IN ('hospitalDirection', 'recoveryDirection', 'hospitalDirection2018', 'recoveryDirection2018')
                        AND event_id IN (%s, %s)  AND Action.status NOT IN (3,6) AND ActionPropertyType.descr IN ( 'NAZ_PK',  'NAZ_PMP')  AND Action.deleted =0 AND ActionProperty.deleted = 0
                   """%(eventId, eventId1)
                    
         stmt2 = """SELECT Action.id as actionId, ActionType.code as code, rbSpeciality.federalCode as type, ActionPropertyType.descr as name, ActionType.flatCode as flatCode
                     FROM  ActionProperty 
                     LEFT JOIN ActionPropertyType ON ActionPropertyType.id = type_id
                     LEFT JOIN ActionType On ActionType.id = ActionPropertyType.actionType_id
                     LEFT JOIN Action ON Action.id = ActionProperty.action_id
                     LEFT JOIN ActionProperty_rbSpeciality ON ActionProperty.id = `ActionProperty_rbSpeciality`.id
                     lEFT JOIN rbSpeciality ON rbSpeciality.id = `ActionProperty_rbSpeciality`.value
                       WHERE  flatCode IN ('consultationDirection', 'consultionDirectionToHosp', 
                       'consultationDirection2018', 'consultionDirectionToHosp2018') 
                       AND event_id IN (%s, %s) AND ActionPropertyType.descr IN ( 'NAZ_SP')  AND Action.deleted =0 AND ActionProperty.deleted = 0  AND Action.status NOT IN (3,6) 
                   """%(eventId, eventId1)
                   
                   
         stmt3 = """SELECT Action.id as actionId, 
                            ActionType.code as code, 
                            Person.`SNILS` AS personSNILS,
                            Action.plannedEndDate as plDate
                     FROM Action
                     LEFT JOIN Event ON Event.id = Action.event_id
                     LEFT JOIN Person  ON Person.id = Event.curator_id
                     LEFT JOIN ActionType On ActionType.id = Action.actionType_id
                     WHERE flatCode IN ('consultationDirection', 'consultionDirectionToHosp', 
                     'inspectionDirection2018', 'hospitalDirection', 'consultationDirection2018', 
                     'consultionDirectionToHosp2018', 'inspectionDirection2018', 'hospitalDirection2018') 
                      AND Action.deleted =0  AND Action.status NOT IN (3,6) 
                      AND event_id IN ( %s, %s)  
                   """%(eventId, eventId1)
                   
         stmt4 = """SELECT Action.id as actionId, ActionType.code as code, Organisation.miacCode as mcode, ActionPropertyType.descr as name, ActionType.flatCode as flatCode
                     FROM  ActionProperty 
                     LEFT JOIN ActionPropertyType ON ActionPropertyType.id = type_id
                     LEFT JOIN ActionType On ActionType.id = ActionPropertyType.actionType_id
                     LEFT JOIN Action ON Action.id = ActionProperty.action_id
                     LEFT JOIN ActionProperty_Organisation ON ActionProperty.id = `ActionProperty_Organisation`.id
                     lEFT JOIN Organisation ON Organisation.id = ActionProperty_Organisation.value
                       WHERE  flatCode IN (
                       'consultationDirection2018', 'inspectionDirection2018') 
                       AND event_id IN (%s, %s) AND ActionPropertyType.descr IN ( 'NAPR_MO')  
                       AND Action.deleted =0 AND ActionProperty.deleted = 0  AND Action.status NOT IN (3,6) 
                   """%(eventId, eventId1)
                   
         stmt5 = """SELECT Action.id as actionId, ActionType.code as code, rbService.code as scode, 
                        ActionPropertyType.descr as name, ActionType.flatCode as flatCode
                     FROM  ActionProperty 
                     LEFT JOIN ActionPropertyType ON ActionPropertyType.id = type_id
                     LEFT JOIN ActionType On ActionType.id = ActionPropertyType.actionType_id
                     LEFT JOIN Action ON Action.id = ActionProperty.action_id
                     LEFT JOIN ActionProperty_rbService ON ActionProperty.id = `ActionProperty_rbService`.id
                     lEFT JOIN rbService ON rbService.id = ActionProperty_rbService.value
                       WHERE  flatCode IN ('inspectionDirection2018') 
                       AND event_id IN (%s, %s) AND ActionPropertyType.descr IN ( 'NAZ_USL')  
                       AND Action.deleted =0 AND ActionProperty.deleted = 0  AND Action.status NOT IN (3,6) 
                   """%(eventId, eventId1)
                   
         query = QtGui.qApp.db.query(stmt)
         query1 = QtGui.qApp.db.query(stmt1)
         query2 = QtGui.qApp.db.query(stmt2)
         query3 = QtGui.qApp.db.query(stmt3)
         query4 = QtGui.qApp.db.query(stmt4)
         query5 = QtGui.qApp.db.query(stmt5)
         mass = {}

         while query.next():
             actionId = forceString(query.record().value('actionId'))
             mass[actionId] = {'NAZ_V': '', 
                               'NAZ_PK': '', 
                               'NAZ_SP': '', 
                               'NAZ_PMP': '', 
                               'NAZR':'', 
                               'NAZ_IDDOKT':'', 
                               'NAZ_DATE':'',
                               'NAZ_USL':'',
                               'NAPR_MO':'',
                                'iddokt':''}
             code = forceString(query.record().value('code'))
             code1 = forceString(query.record().value('code'))
             flatCode = forceString(query.record().value('flatCode'))
             if '2018' in flatCode:
                    code = {
                                  '1': lambda x : u'5',
                                  '8': lambda x : u'3',
                                  '4': lambda x : u'5',
                                  '2': lambda x : u'1',
                            }[code1](code)
             name = forceString(query.record().value('name'))
             type = forceString(query.record().value('type'))
             
                
             if name in ['consult']:
                 mass[actionId]['NAZR'] = (forceString(query.record().value('type')).split('.')[0])
                 if mass[actionId]['NAZR'] == '2':
                    personSNILS = forceString(query.record().value('snils'))
                    personSNILS = personSNILS[0:3] + '-' +personSNILS[3:6]+'-' +personSNILS[6:9]+'-' +personSNILS[9:11]
                    mass[actionId]['NAZ_IDDOKT'] = personSNILS
                    mass[actionId]['NAZ_DATE'] =  (forceDate(query.record().value('plDate'))).toString(Qt.ISODate)
                 if mass[actionId]['NAZR'] in ('2', '3'):    
                    mass[actionId]['NAZR_DATE'] =  (forceDate(query.record().value('dDate'))).toString(Qt.ISODate)
             elif name in ['CaseAidPlace']:
                ts = (forceInt((forceString(query.record().value('type'))).split('.')[0]))
                if ts == 4:
                     mass[actionId]['NAZR'] = 5
                if ts == 3:
                     mass[actionId]['NAZR'] = 4
             else:
                 mass[actionId]['NAZR'] = code # (forceString(query.record().value('code')))
             if name in [ 'NAZ_PMP','NAZ_V']:  
                 mass[actionId][name] = forceString(query.record().value('type')).split('.')[0]
                 if mass[actionId]['NAZR'] in ('2', '3'):  
                     mass[actionId]['NAPR_DATE'] =  (forceDate(query.record().value('dDate'))).toString(Qt.ISODate)

         while query1.next():
             actionId = forceString(query1.record().value('actionId'))
             if actionId not in mass:
                 mass[actionId] = {'NAZ_V': '', 'NAZ_PK': '', 'NAZ_SP': '', 'NAZ_PMP': '', 'NAZR': ''}         
             name = forceString(query1.record().value('name'))
             if forceString(query1.record().value('code')) == '6':
                 mass[actionId]['NAZR'] =6
             if name in ['NAZ_PK',  'NAZ_PMP']:
                 mass[actionId][name] = forceString(query1.record().value('type'))
         while query2.next():
              actionId = forceString(query2.record().value('actionId'))
              name = forceString(query2.record().value('name'))
              if name in ['NAZ_SP'] and actionId  in mass.keys():  
                 mass[actionId][name] = forceString(query2.record().value('type'))
              else:
                  log(u'В событии %s  в направлении не заполнено обязательное поле' % eventId, True)
         while query3.next():
              actionId = forceString(query3.record().value('actionId'))
              personSNILS = forceString(query3.record().value('personSNILS'))
              personSNILS = personSNILS[0:3] + '-' +personSNILS[3:6]+'-' +personSNILS[6:9]+'-' +personSNILS[9:11]
              if actionId in mass.keys():
                  mass[actionId]['iddokt'] = personSNILS
              else:
                log(u'В событии %s в направлении не заполнено обязательное поле' % eventId, True)

         while query4.next():
              actionId = forceString(query4.record().value('actionId'))
              mass[actionId]['NAPR_MO'] = forceString(query4.record().value('mcode'))
         while query5.next():
              actionId = forceString(query5.record().value('actionId'))
              mass[actionId]['NAZ_USL'] = forceString(query5.record().value('scode'))
         return mass
        

        
    def getAccDiag(self, eventId):
        stmt = """SELECT  `Diagnosis`.`MKB` AS mkb,  rbDiseaseCharacter.code as code, if(`rbDispanser`.observed IN (1, 2), IF(`rbDispanser`.observed = 6, 2, `rbDispanser`.observed), 3) as dispanserStatus
                    FROM  `Diagnostic`
                    LEFT JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnostic.character_id
                    LEFT JOIN  `Diagnosis` ON `Diagnosis`.id = diagnosis_id
                    LEFT JOIN rbDispanser ON rbDispanser.id = Diagnostic.dispanser_id
                    WHERE  `event_id` =%d AND `Diagnostic`.diagnosisType_id = 5 AND Diagnostic.deleted =0
                    """%(eventId)
        query = QtGui.qApp.db.query(stmt)
        mkb = {}
        while query.next():
            mkb[forceString(query.record().value('mkb'))] = ['2', forceString(query.record().value('dispanserStatus'))]  if  forceString(query.record().value('code')) == '2' else [0, forceString(query.record().value('dispanserStatus'))] 
        return mkb

    def getHospitalDaysAmount(self, eventId):
        stmt = """SELECT SUM(  `Action`.`amount` ) AS amountHD
                            FROM  `Action`
                            LEFT JOIN  `ActionType` ON (  `Action`.`ActionType_id` =  `ActionType`.`id` )
                            WHERE  `ActionType`.`flatCode` =  "moving"
                            AND  `Action`.`event_id` =%d
                            AND Action.deleted !=1""" %(eventId)
        query =  QtGui.qApp.db.query(stmt)
        flag = self.isOneDay(eventId)
        if query.next():
            if flag == True:
                return (forceInt(query.record().value('amountHD'))-1)
            else:
                return (forceInt(query.record().value('amountHD')))
        else:
            return None

    def getVisitsAmount(self, eventId):
        stmt = """SELECT COUNT(  `Visit`.`id` ) AS visitAmount
                        FROM  `Visit`
                        WHERE  `Visit`.`event_id` =%d
                        AND Visit.deleted !=1""" %(eventId)
        query =  QtGui.qApp.db.query(stmt)
        if query.next():
            return (forceInt(query.record().value('visitAmount')))
        else:
            return None


    def getOperationCode(self, eventId):
        stmt = """SELECT ActionType.flatCode as operationCode
                    FROM `Action`
                    LEFT JOIN `ActionType` ON `Action`.`actionType_id` = `ActionType`.`id`
                    WHERE `Action`.`event_id`=%d AND
                            ActionType.serviceType = 4 AND
                            `Action`.`deleted` !=1
                    LIMIT 1""" %(eventId)
        query =  QtGui.qApp.db.query(stmt)
        if query.next():
            return (forceString(query.record().value('operationCode')))
        else:
            return None

    def getServicesOfAction(self, actionId):
        stmt = """SELECT rbService.`code` as serviceCode
                    FROM `rbService`
                    LEFT JOIN ActionType_Service ON ActionType_Service.service_id = rbService.id
                    LEFT JOIN Action ON Action.actionType_id= ActionType_Service.master_id
                    LEFT JOIN Event ON Event.id = Action.event_id
                    LEFT JOIN rbServiceGroup ON rbServiceGroup.id = rbService.group_id
                    WHERE Action.id =%d and Event.execDate > `rbService`.begDate
                     and (`rbService`.endDate IS NULL or Event.execDate < `rbService`.endDate) %s """ %(actionId, 
                                                                                                        "AND (rbServiceGroup.code LIKE '3.2%' or rbServiceGroup.code LIKE '3.9%')")
        query =  QtGui.qApp.db.query(stmt)
        if query.next():
            service = forceString(query.record().value('serviceCode'))
            return service
        else:
            return None

    def getRegionalCode(self, record, serviceCode):
        serviceStr = ''
        if serviceCode.startswith('2.'):
            if serviceCode.startswith('2.8.3') or serviceCode.startswith('2.8.4'):
                serviceStr = '2.23.3'
            elif serviceCode.startswith('2.5.23'):
                serviceStr = '1.4.2'
            elif serviceCode.startswith('3.11'):
                serviceStr = '2.23.4'
            elif serviceCode.startswith('3.12'):
                serviceStr = '2.23.1'
            else:
                serviceStr = {
                      2: lambda x : '2.13.1',
                      4: lambda x : '2.10.3',
                      5: lambda x : '2.10.2',
                      6: lambda x : '2.10.1',
                      8: lambda x : '2.6.1',
                            }[forceInt(serviceCode[2:3])](serviceStr)
        else:
            serviceStr = {
                      0: lambda x : '3.14.1',
                      1: lambda x : '1.4.1',
                      2: lambda x : '4.3.1',
                      3: lambda x : '2.13.1',
                      4: lambda x : '1.4.1',
                      5: lambda x : '3.15.1',
                      6: lambda x : '1.3.1',
                      9: lambda x : '1.7.1',
                      10: lambda x: '1.7.1',
                      11: lambda x: '3.13.1'
                            }[forceInt(record.value('ContractTariffType'))](serviceStr)
        return serviceStr



    def getPersonSpecialityUsishCode(self, personId):
        specialityId = self.getPersonSpecialityId(personId)
        result = None
        if specialityId:
                result = forceString(QtGui.qApp.db.translate('rbSpeciality', 'id', specialityId, 'usishCode'))
        return result

    def getPersonSpecialityId(self, personId):
        u"""Определяем id специальности врача по его id"""
        return forceRef(self.getTableFieldById(personId, 'Person',
                        'speciality_id', self._specialityCache))

    def getActions(self, eventId):
        stmt = """SELECT  `Action`.`id` AS actionId, status
                    FROM  `Action`
                    WHERE  `Action`.`event_id` =%d  AND Action.deleted =0 AND Action.payStatus = 0
                    """%(eventId)
        query = QtGui.qApp.db.query(stmt)
        if query:
            actions = {}
            while query.next():
                actions[forceInt(query.record().value('actionId'))] = forceInt(query.record().value('status'))
            return actions
        else:
            return None

    def getServiceCodeForUnexposedService(self, accountId, eventId):
        stmt = """SELECT  rbService.code as serviceCode, rbService.name
                    FROM `Action`
                                LEFT JOIN ActionType On ActionType.id = `Action`.actionType_id
                                LEFT JOIN rbService ON rbService.id = `ActionType`.`nomenclativeService_id`
                                LEFT JOIN rbServiceGroup ON rbServiceGroup.id = `rbService`.`group_id`
                                WHERE `event_id` = %d AND status !=3 AND Action.deleted =0
                    and
                        Action.id NOT IN
                                (
                                SELECT   Account_Item.action_id
                                FROM `Account_Item`
                    LEFT JOIN rbService ON rbService.id = `Account_Item`.`service_id`
                    LEFT JOIN rbServiceGroup ON rbServiceGroup.id = `rbService`.`group_id`
                    WHERE `event_id` = %d AND rbServiceGroup.code LIKE '%s' and Account_Item.deleted =0  and `Account_Item`.master_id = %s)
                   """%(eventId, eventId, u'29.%', accountId)
        query = QtGui.qApp.db.query(stmt)
        if query:
            servicesCode = []
            while query.next():
                servicesCode.append(forceString(query.record().value('serviceCode')))
            return servicesCode
        else:
             return None

    def getServiceCodeForExposedServiceInOtherAccount(self, accountId, eventId):
        stmt = """SELECT  rbService.code as serviceCode, rbService.name
                    FROM `Action`
                                LEFT JOIN ActionType On ActionType.id = `Action`.actionType_id
                                LEFT JOIN rbService ON rbService.id = `ActionType`.`nomenclativeService_id`
                                LEFT JOIN rbServiceGroup ON rbServiceGroup.id = `rbService`.`group_id`
                                WHERE `event_id` = %d AND status !=3 AND Action.deleted =0
                    and
                        Action.id IN
                                (
                                SELECT   Account_Item.action_id
                                FROM `Account_Item`
                    LEFT JOIN rbService ON rbService.id = `Account_Item`.`service_id`
                    LEFT JOIN rbServiceGroup ON rbServiceGroup.id = `rbService`.`group_id`
                    WHERE `event_id` = %d AND rbServiceGroup.code LIKE '%s' and Account_Item.deleted =0  and `Account_Item`.master_id != %s)
                   """%(eventId, eventId, u'29.%', accountId)
        query = QtGui.qApp.db.query(stmt)
        if query:
            servicesCode = []
            while query.next():
                servicesCode.append(forceString(query.record().value('serviceCode')))
            return servicesCode
        else:
             return None

# *****************************************************************************************

class CPersonalDataStreamWriter(QXmlStreamWriter):
    def __init__(self, parent):
        QXmlStreamWriter.__init__(self)
        self.parent = parent
        self.setAutoFormatting(True)
        self._clientsSet = None


    def writeTextElement(self, element,  value, writeEmtpyTag = False):
        if not writeEmtpyTag and (not value or value == ''):
            return

        QXmlStreamWriter.writeTextElement(self, element, value)


    def writeRecord(self, record, contractBegDate,log):

        clientId = forceRef(record.value('client_id'))
        sex = forceString(record.value('sex'))
        birthDate = forceDate(record.value('birthDate'))
        #замена дефиса в свидетельстве о рождении
        if forceDouble(record.value('documentFederalCode')) == 3:
            documentSerial= forceString(record.value('documentSerial')).replace(' ', '-')
        else: documentSerial=forceString(record.value('documentSerial'))
        if clientId in self._clientsSet:
            return

        self.writeStartElement('PERS')
        self.writeTextElement('ID_PAC',  ('%d' % clientId)[:36])
        #Фамилия пациента.
        dost = []
        if '0003' not in Export29XMLCommon.getSpecialCaseCode(QtGui.qApp.db, clientId, self.parent.endDate) and '0009' not  in Export29XMLCommon.getSpecialCaseCode(QtGui.qApp.db, clientId, self.parent.endDate):
            if forceString(record.value('lastName')) == u'нет' or forceString(record.value('lastName')) == u'Нет' or forceString(record.value('lastName')) == u'НЕТ':
#                self.writeTextElement('DOST', '2')
                dost.append(2)
            else:
                self.writeTextElement('FAM', forceString(record.value('lastName')))
        #Имя пациента
            if forceString(record.value('firstName')) == u'нет' or forceString(record.value('firstName')) == u'Нет' or forceString(record.value('lastName')) == u'НЕТ':
#                self.writeTextElement('DOST', '3')
                dost.append(3)
            else:
                self.writeTextElement('IM', forceString(record.value('firstName')))
        #Отчество пациента
            if forceString(record.value('patrName')) == u'нет' or forceString(record.value('patrName')) == u'Нет' or forceString(record.value('lastName')) == u'НЕТ':
 #               self.writeTextElement('DOST', '1')
                dost.append(1)
            else:
                self.writeTextElement('OT', forceString(record.value('patrName')))
        self.writeTextElement('W', sex)
        #Дата рождения пациента.
        self.writeTextElement('DR', birthDate.toString(Qt.ISODate))
        if dost:
            for ds in dost:
                self.writeTextElement('DOST', forceString(ds))
        elif '0003' in Export29XMLCommon.getSpecialCaseCode(QtGui.qApp.db, clientId, self.parent.endDate) or  '0009' in Export29XMLCommon.getSpecialCaseCode(QtGui.qApp.db, clientId, self.parent.endDate):
            fam, im, ot, birthDate, sex = Export29XMLCommon.getConnection(QtGui.qApp.db, clientId)
            #Фамилия представителя.
            if not fam and not im and not ot and not birthDate and not sex:
                log(u'В регистрационной карточке новорожденного пациента %d не указан представитель' % clientId, True)
            else:
                dostp = []
                if fam == u'нет' or fam == u'Нет':
                    dostp.append(2)
                else:
                    self.writeTextElement('FAM_P', fam)
                #Имя пациента
                if im == u'нет' or im == u'Нет':
                    dostp.append(3)
                else:
                    self.writeTextElement('IM_P', im)
                #Отчество пациента
                if ot == u'нет' or ot == u'Нет':
                    dostp.append(1)
                else:
                    self.writeTextElement('OT_P', ot)

            #Пол пациента.
                self.writeTextElement('W_P', forceString(sex))
            #Дата рождения пациента.
                self.writeTextElement('DR_P', birthDate.toString(Qt.ISODate))
#            self.writeTextElement('DR_P', birthDate)
                if dostp:
                    for ds in dostp:
                        self.writeTextElement('DOST_P', forceString(ds))

        self.writeTextElement('MR', forceString(record.value('birthPlace')), writeEmtpyTag=False)
        # Федеральный код из справочника ТИПЫ ДОКУМЕНТОВ. Из карточки пациента.
        self.writeTextElement('DOCTYPE',  forceString(record.value('documentFederalCode')))
        # Серия документа, удо-стоверяющего личность пациента.
        self.writeTextElement('DOCSER', documentSerial)
        # Номер документа, удостоверяющего личность пациента.
        self.writeTextElement('DOCNUM', forceString(record.value('documentNumber')))
        if contractBegDate > QDate(2019, 10, 31):
            self.writeTextElement('DOCDATE', (forceDate(record.value('documentDate'))).toString(Qt.ISODate))
            self.writeTextElement('DOCORG', forceString(record.value('documentOrg')))
        # СНИЛС пациента.
        self.writeTextElement('SNILS', formatSNILS(forceString(record.value('SNILS'))))
        # Код места жительства по ОКАТО. Берётся из адреса жительство.
        #self.writeTextElement('OKATOG', okatog)
        # Код места пребывания по ОКАТО. Берётся из ОКАТО организации, чей полис у пациента.
        #self.writeTextElement('OKATOP', forceString(record.value('insurerOKATO')))
        self.writeEndElement() # PERS
        self._clientsSet.add(clientId)


    def writeFileHeader(self,  device, fileName, accDate, contractBegDate):
        self._clientsSet = set()
        self.setDevice(device)
        self.writeStartDocument()
        self.writeStartElement('PERS_LIST')
        self.writeHeader(fileName, accDate, contractBegDate)


    def writeHeader(self, fileName, accDate, contractBegDate):
        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', '2.1.2' if contractBegDate < QDate(2019, 10, 31) else '3.2.0')
        self.writeTextElement('DATA', accDate.toString(Qt.ISODate))
        (fname,  ext) = os.path.splitext(os.path.basename(fileName))
        self.writeTextElement('FILENAME', 'L%s' % fname[1:26])
        self.writeTextElement('FILENAME1', fname[:26])
        self.writeEndElement()

    def writeFileFooter(self):
        self.writeEndElement() # root
        self.writeEndDocument()



class CAccountDataStreamWriter(QXmlStreamWriter):
    def __init__(self, parent):
        QXmlStreamWriter.__init__(self)
        self.parent = parent
        self.setAutoFormatting(True)
        self._clientsSet = None

    def writeFileHeader(self,  device, fileName, accDate):
        self._clientsSet = set()
        self.setDevice(device)
        self.writeStartDocument()
        self.writeStartElement('SCH')
        self.writeHeader(fileName, accDate)
    
    def writeTextElement(self, element,  value, writeEmtpyTag = False):
        if not writeEmtpyTag and (not value or value == ''):
            return
        QXmlStreamWriter.writeTextElement(self, element, value)
        
    def writeRecord(self, contractId, payerId, accDate, accNumber, fileName, year, month, accSum, log):
        db = QtGui.qApp.db
        table = db.table('Organisation')
        recipientId = forceString(db.translate('Contract', 'id', contractId , 'recipient_id'))
        recipientAccount_id = forceString(db.translate('Contract', 'id', contractId , 'recipientAccount_id'))
        payerAccount_id = forceString(db.translate('Contract', 'id', contractId , 'payerAccount_id'))
        recordRec = QtGui.qApp.db.getRecordEx(table, '*', table['id'].eq(recipientId))
        
        recordPay = QtGui.qApp.db.getRecordEx(table, '*', table['id'].eq(payerId))
        (fname,  ext) = os.path.splitext(os.path.basename(fileName))
        self.writeStartElement('SCH_DATA')
        self.writeTextElement('NSCHET',  forceString(accNumber)[:15])
        self.writeTextElement('MONTH',  month)
        self.writeTextElement('YEAR', year)
        self.writeTextElement('DSCHET', accDate.toString(Qt.ISODate))
        self.writeTextElement('FILE_NAME',  forceString(fname))
        self.writeTextElement('IFIN', '', writeEmtpyTag = True)
        
        self.writeTextElement('SUMMAV', forceString(accSum))
        if forceString(recordRec.value('chiefFreeInput')) != '':
            self.writeTextElement('RUK',  forceString(recordRec.value('chiefFreeInput')))
        else:
            self.writeTextElement('RUK',  forceString(recordRec.value('chiefFreeInput')))
        self.writeTextElement('BUH',  forceString(recordRec.value('accountant')))
        self.writeEndElement()
        self.writeOgr(db, 'POST', recordRec, contractId, recipientAccount_id, 'recipient_id', 0)
        self.writeOgr(db, 'PLAT', recordPay, contractId, payerAccount_id, 'payer_id', 1)
        self.writeOgr(db, 'POL', recordRec, contractId, recipientAccount_id,  'recipient_id', 0)

    
    def writeOgr(self, db, tag, record, contactId, accId, field, flag):
        bankId = forceString(db.translate('Organisation_Account', 'id', accId , 'bank_id'))
        bankAccount = forceString(db.translate('Organisation_Account', 'id', accId , 'name'))
        table = db.table('Bank')
        recordBank = QtGui.qApp.db.getRecordEx(table, '*', table['id'].eq(bankId))
        self.writeStartElement(tag)
        self.writeTextElement('NAM_MOP' if flag == 0 else 'NAME',  forceString(record.value('fullName')))
        self.writeTextElement('MCOD' if flag == 0 else 'COD',  forceString(record.value('miacCode')))
        self.writeTextElement('INN',  forceString(record.value('INN')))
        self.writeTextElement('KPP', forceString(record.value('KPP')))
        okved = forceString(record.value('OKVED'))
        if okved[:1].isalpha():
            okved = okved[1:]
        self.writeTextElement('OKVED', okved[:15])
        self.writeTextElement('OKPO', forceString(record.value('OKPO')))
        self.writeTextElement('BANK_NAME', forceString(recordBank.value('name')))
        self.writeTextElement('RASCH_SCH', forceString(bankAccount))
        self.writeTextElement('BIK',  forceString(recordBank.value('BIK')))
        self.writeTextElement('LIC_SCH', forceString(record.value('personalAccount')))
        self.writeTextElement('ADDR_J',  forceString(record.value('Address')))
        self.writeEndElement()
            
    def writeHeader(self, fileName, accDate):
        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', '1.1' if accDate < QDate(2022, 2, 1) else '1.2')

        self.writeEndElement()

    def writeFileFooter(self):
        self.writeEndElement() # root
        self.writeEndDocument()