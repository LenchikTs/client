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
import json
import uuid
from xml.sax.saxutils import unescape
from Export29XMLCommon import Export29XMLCommon
from Export29XMLCommon import SummSingleton

from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtXml import *
from zipfile import *

from Accounting.Tariff import CTariff
from Exchange.Export import CExportHelperMixin
from library.dbfpy.dbf import *
from library.database  import *
from library.Utils     import *
from Events.Utils      import updateDurationEvent
from Events.Action     import CAction

from Ui_ExportR29XMLPage1 import Ui_ExportPage1
from Ui_ExportR29XMLPage2 import Ui_ExportPage2

serviceInfoExportVersion = '1.0'
container = SummSingleton()

def getAccountInfo(accountId):
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


def exportR29v312Stomotology(widget, accountId, accountItemIdList):
    wizard = CExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
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
        self.endDate = None


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

    def log(self, str, forceLog = False):
        if self.chkVerboseLog.isChecked() or forceLog:
            self.logBrowser.append(str)
            self.logBrowser.update()

    
    def getFullXmlFileName(self):
       if not self.xmlFileName:
           (date, number, exposeDate, contractId,  payerId,  aDate, aAmount) = getAccountInfo(self.accountId)
    
           payerCode = '29'
           #    infix = 'S'
           try:
               
               strContractNumber = forceString(QtGui.qApp.db.translate('Contract', 'id', contractId , 'number'))
               if strContractNumber.lower().find(u'иногород') != -1 or self.page1.chkExportTypeBelonging.isChecked() or forceString(QtGui.qApp.db.translate('Organisation', 'id', payerId, 'miacCode')) == '29':
                   infix = 'T'
               else:
                   infix = 'S'
                   payerCode = forceString(QtGui.qApp.db.translate(
                   'Organisation', 'id', payerId, 'miacCode'))
               if  (u'ОНК') in number or (u'онк') in number:
                   prefix = 'C'
               else:
                   prefix = 'H'
           except:
               self.log(str(contractId)+ ", strContractNumber, ")
    
    
           lpuInfis  = self.getMiacCode(contractId) #'292301'
           self.xmlFileName = os.path.join(self.getTmpDir(), 
               u'%sM%s%s%s_%s%d.xml' % (prefix,lpuInfis, infix,  payerCode, date.toString('yyMM'),
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
        self.setExportMode(False)
        self.aborted = False
        self.done = False
        self.idList = []
        self.parent = parent #wtf? скрывать Qt-шный parent - это плохая затея
        self.recNum= 0
        self.ignoreErrors = forceBool(QtGui.qApp.preferences.appPrefs.get(
            'ExportR29XMLIgnoreErrors', False))
        self.connect(parent, SIGNAL('rejected()'), self.abort)
        self.chkVerboseLog.setChecked(forceBool(QtGui.qApp.preferences.appPrefs.get(
            'ExportR29XMLVerboseLog', False)))
        self.chkIgnoreErrors.setChecked(self.ignoreErrors)
#        self.chkGroupByService.setChecked(forceBool(getVal(QtGui.qApp.preferences.appPrefs,
#            'ExportR29XMLGroupByService', True)))
        self.edtRegistryNumber.setValue(forceInt(QtGui.qApp.preferences.appPrefs.get(
            'ExportR29XMLRegistryNumber', 0))+1)
        self.chkExportTypeBelonging.setChecked(forceBool(QtGui.qApp.preferences.appPrefs.get(
            'ExportR29XMLBelonging', True)))


    def setExportMode(self, flag):
        self.btnCancel.setEnabled(flag)
        self.btnExport.setEnabled(not flag)
        self.chkClientLog.setEnabled(not flag)
        self.chkIgnoreErrors.setEnabled(not flag)
        self.chkVerboseLog.setEnabled(not flag)
        self.edtRegistryNumber.setEnabled(not flag)



    def log(self, str, forceLog = False):
        if self.chkVerboseLog.isChecked() or forceLog:
            self.logBrowser.append(str)
            self.logBrowser.update()


    def setAccountItemsIdList(self, accountItemIdList):
        self.idList = accountItemIdList


    def prepareToExport(self):
        self.done = False
        self.aborted = False
        self.emit(SIGNAL('completeChanged()'))
        self.setExportMode(True)
        output, clientOutput, accountOut = self.createXML()
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
                            """ 

        stmt = """SELECT Account_Item.id AS accountItemId,
                CSGEvent.endDate as csgEndDate,
                Account_Item.event_id  AS event_id,
                Account_Item.visit_id as visit_id,
                Account_Item.action_id as action_id,
                Account_Item.service_id,
                Event.client_id        AS client_id,
                EventType.service_id AS EventServiceId,
                EventType.name as EventTypeName,
                Event.externalId AS eventExternalId,
                Contract_Tariff.uet as ContractTariffUet,
                Contract_Tariff.pg as pgCode,
                Client.lastName,
                Client.firstName,
                Client.patrName,
                Client.birthDate       AS birthDate,
                Client.sex AS sex,
                `Client`.`SNILS` AS SNILS,
                Client.birthPlace AS birthPlace,
                age(Client.birthDate, Event.setDate) as clientAge,
                Client.birthWeight AS birthWeight,
             --   age(Client.birthDate, CSGEvent.begDate) as clientAge,
                CONCAT(ClientPolicy.serial, ' ', ClientPolicy.number) AS policySN,
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
				Diagnosis.TNMS          AS TNMS,
                rbTraumaType.code    AS traumaCode,
                Event.eventType_id    AS eventTypeId,
                Event.prevEvent_id    AS preEventId,
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
                CONCAT_WS('-',SUBSTRING(Person.`SNILS`, 1, 3), SUBSTRING(Person.`SNILS`, 4, 3), SUBSTRING(Person.`SNILS`, 7, 3), SUBSTRING(Person.`SNILS`, 10, 2)) AS personSNILS,
                rbDiagnosticResult.federalCode AS resultFederalCode,
                rbMedicalAidType.regionalCode AS medicalAidTypeRegionalCode,
                rbMedicalAidType.regionalCode AS medicalAidTypeFederalCode,
                IF(Account_Item.service_id IS NOT NULL,
                   ItemMedicalAidProfile.federalCode,
                   IF(Account_Item.visit_id IS NOT NULL, VisitMedicalAidProfile.federalCode, EventMedicalAidProfile.federalCode)
                  ) AS medicalAidProfileFederalCode,
                  IF(Account_Item.service_id IS NOT NULL,
                   ItemMedicalAidProfile.code,
                   IF(Account_Item.visit_id IS NOT NULL, VisitMedicalAidProfile.code, EventMedicalAidProfile.code)
                  ) AS medicalAidProfileCode,
                IF(Account_Item.service_id IS NOT NULL,
                   ItemMedicalAidType.regionalCode,
                   IF(Account_Item.visit_id IS NOT NULL, VisitMedicalAidType.regionalCode, EventMedicalAidType.regionalCode)
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
                    rbItemService.note,
                    IF(Account_Item.visit_id IS NOT NULL, rbVisitService.note, rbEventService.note)
                    ) AS serviceNote,
                
                AccDiagnosis.MKB AS AccMKB,
                CompDiagnosis.MKB AS CompMKB,
                PreDiagnosis.MKB AS PreMKB,
                rbDiseaseCharacter_Identification.value as diseaseCharacter,
                rbEventProfile.regionalCode AS eventProfileRegCode,
                rbEventProfile.code AS eventProfileCode,
                OrgStructure.infisCode AS orgStructureCode,
                OrgStructure.infisInternalCode AS orgStructureInternalCode,
                rbMedicalAidUnit.federalCode AS medicalAidUnitFederalCode,
                rbEventTypePurpose.regionalCode AS eventTypePurpose,
                rbEventTypePurpose.federalCode AS eventTypePurposeFederalCode,
                Event.`order`,
                Event.id AS eventId,
                EventType.regionalCode as eventTypeRegionalCode,
                EventResult.federalCode AS eventResultFederalCode,
                EventResult.regionalCode AS eventResultRegionalCode,
                RelegateOrg.miacCode AS relegateOrgMiac,
                rbTariffCategory.federalCode AS tariffCategoryFederalCode,
                EventType.code AS eventTypeCode,
                Action.begDate AS begDateAction,
                Action.endDate AS endDateAction,
                Account_Item.master_id As accountId,
                Account_Item.usedCoefficients as usedCoefficients,
                apCSGEvent.CSGCode as stgCode,
                if (apCSGEvent.MKB IS NULL, CSGEvent.MKB, apCSGEvent.MKB) as stgMKB,
                IF(CSGEvent.parentCSG_id IS NOT NULL, CSGEvent.parentCSG_id, IF(apCSGEvent.parentCSG_id IS NOT NULL,  apCSGEvent.parentCSG_id, IF (`Action`.eventCSG_id IS NOT NULL, `Action`.eventCSG_id, CSGEvent.id))) as STGid,
                rbCSGService.code,
                CSGEvent.id as CSGEventId,
                CSGEvent.begDate as csgBegDate,
                Event.srcDate AS directionDate,
                Contract_Tariff.uet,
                HospitalAction.id AS hospitalActionId, 
                 if(`rbDispanser`.observed IN (1, 2, 4), IF(`rbDispanser`.observed = 6, 2,  IF(`rbDispanser`.observed iN (3, 5), 6, `rbDispanser`.observed)), 0) as dispanserStatus
            FROM Account_Item
            LEFT JOIN Action ON Action.id = Account_Item.action_id
            LEFT JOIN Event  ON Event.id  = Account_Item.event_id
            LEFT JOIN EventType ON EventType.id = Event.eventType_id
            LEFT JOIN Visit  ON Visit.id  = Account_Item.visit_id
            LEFT JOIN Client ON Client.id = Event.client_id
            LEFT JOIN ClientPolicy ON ClientPolicy.client_id = Client.id AND
                      ClientPolicy.id = (SELECT MAX(CP.id)
                                         FROM   ClientPolicy AS CP
                                         LEFT JOIN rbPolicyType AS CPT ON CPT.id = CP.policyType_id
                                         WHERE  CP.client_id = Client.id AND CP.deleted=0 AND CPT.code IN ('1','2') AND CP.insurer_id IS NOT NULL AND CP.deleted =0)  AND ClientPolicy.begDate <= Event.setDate AND
                            (ClientPolicy.endDate is NULL or ClientPolicy.endDate >= Event.execDate or ClientPolicy.endDate='0000-00-00')
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
            LEFT JOIN Person  ON Person.id = execPerson_id
            LEFT JOIN Diagnostic ON Diagnostic.id = (
              SELECT MAX(D.id)
              FROM Diagnostic AS D
              WHERE D.event_id = Account_Item.event_id
                AND ((D.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code ='2' or code ='4') AND D.person_id = Event.execPerson_id)
                        OR (D.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code='1'
                            ))
                        OR (D.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE `code` ='2' or code ='4')
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
          --  LEFT JOIN ActionProperty ON ActionProperty.action_id = Action.id and type_id in (SELECT id  FROM `ActionPropertyType` WHERE `name` LIKE '%s')
          --  lEFT JOIN `ActionProperty_CSG` ON `ActionProperty_CSG`.id = ActionProperty.id
            LEFT JOIN `Event_CSG` as apCSGEvent ON apCSGEvent.id = `Action`.eventCSG_id and apCSGEvent.master_id = Event.id
            LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
            LEFT JOIN rbService AS rbItemService ON rbItemService.id = Account_Item.service_id
            LEFT JOIN rbServiceGroup as rbItemServiceGroup ON rbItemServiceGroup.id = rbItemService.group_id
            LEFT JOIN rbServiceGroup as rbEventServiceGroup ON rbEventServiceGroup.id = rbEventService.group_id
            LEFT JOIN rbServiceGroup as rbVisitServiceGroup ON rbVisitServiceGroup.id = rbVisitService.group_id
            LEFT JOIN rbService as rbCSGService ON rbCSGService.code =  IF(apCSGEvent.CSGCode IS NULL, rbItemService.code, apCSGEvent.CSGCode)
            LEFT JOIN `Event_CSG` as CSGEvent ON Event.id =  CSGEvent.master_id AND CSGEvent.id =  Account_Item.eventCSG_id
        --    LEFT JOIN `Event_CSG` as addtionalCSGEvent ON Event.id =  addtionalCSGEvent.parentCSG_id
            LEFT JOIN rbDiseaseCharacter ON Diagnosis.character_id = rbDiseaseCharacter.id
            LEFT JOIN `rbDiseaseCharacter_Identification` ON `rbDiseaseCharacter`.id = `rbDiseaseCharacter_Identification`.master_id 
                            AND Diagnostic.setDate > rbDiseaseCharacter_Identification.checkDate
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
            LEFT JOIN Action AS HospitalAction ON
                HospitalAction.id = (
                    SELECT MAX(A.id)
                    FROM Action A
                    WHERE A.event_id = Event.id AND
                              A.deleted = 0 AND
                              A.actionType_id IN (
                                    SELECT AT.id
                                    FROM ActionType AT
                                    WHERE AT.flatCode ='moving'
                              )
                )
            WHERE
                Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s ORDER BY Client.id, Event.id DESC, STGid,   %s DESC, CSGEvent.endDate DESC, Account_Item.price DESC  """ % (sumStr, u'СТГ',cond, "IF(rbCSGService.note like '%additional%', 0, 1)")
            
        query = db.query(stmt)
     #   print stmt
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
        lpuName = forceString(QtGui.qApp.db.translate(
            'Organisation', 'id', QtGui.qApp.currentOrgId(), 'fullName'))
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

        out, query, clientsFile, accountFile = self.prepareToExport()
        accDate, accNumber, exposeDate, contractId,  payerId, aDate, aAmount =\
            getAccountInfo(self.parent.accountId)
        strAccNumber = accNumber if trim(accNumber) else u'б/н'
        strContractNumber = forceString(QtGui.qApp.db.translate(
            'Contract', 'id', contractId , 'number')) if contractId else u'б/н'
        contractBegDate = forceDate(QtGui.qApp.db.translate(
            'Contract', 'id', contractId , 'begDate'))
        payerCode = None
        payerName = ''

        if payerId:
            payerCode = forceString(QtGui.qApp.db.translate(
                    'Organisation', 'id', payerId, 'miacCode'))

        if not payerCode:
            self.log(u'<b><font color=red>ОШИБКА<\font><\b>:'
                     u'Для плательщика не задан код МИАЦ', True)
            if not self.ignoreErrors:
                return

        self.recNum = 0

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
                                miacCode, payerCode, accSum, aAmount, contractBegDate)
            clientsOut.writeFileHeader(clientsFile, self.parent.getFullXmlFileName(), aDate, contractBegDate)
            
            eventsInfo = self.getEventsSummaryPrice()
            bufferForConsult =[]
            while query.next():
                QtGui.qApp.processEvents()
                if self.aborted:
                    break
                self.progressBar.step()
                out.writeRecord(query.record(), miacCode, eventsInfo, self.parent.accountId, bufferForConsult, contractBegDate, self.log)
                while bufferForConsult:
                    out.writeRecord(query.record(), miacCode, eventsInfo, self.parent.accountId, bufferForConsult, contractBegDate, self.log)
                clientsOut.writeRecord(query.record(), contractBegDate, self.log)
            
            out.writeFileFooter()
            clientsOut.writeFileFooter()
            
            file.close()
            clientsFile.close()
            fout = open(self.parent.getFullXmlFileName()+'_out', 'a')
            count = 1
            countDate = 1
            self.progressBar.setValue(0)
            for line in open(self.parent.getFullXmlFileName(), "r"):
                if str(line).find('<SUMV>') != -1:
                    fout.write(str(line).replace('<SUMV>'+str(count)+'</SUMV>',
                                                 '<SUMV>'
                                                 +
                                                    ('%10.2f' % container.dictSums[count]).strip()
                                                 +
                                                 '</SUMV>'))
                    count +=1
                    self.progressBar.step()
                elif str(line).find('<SUMMAV>dummy</SUMMAV>') != -1:
                    fout.write(str(line).replace('<SUMMAV>dummy</SUMMAV>',
                                                 '<SUMMAV>'
                                                 +
                                                    str('%15.2f' % container.summTotal).strip()
                                                 +
                                                 '</SUMMAV>'))
                elif str(line).find('<SD_Z>dummy</SD_Z>') != -1:
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
            container.dictSums = {1 : 0.0}
            container.date = {1: (2000, 1, 1)}
            container.summCaseTotal = 0
                    
            if self.parent.page1.chkExportTypeBelonging.isChecked() == False:
                accountOut = CAccountDataStreamWriter(self)
                accountOut.setCodec(QTextCodec.codecForName('cp1251'))
                accountOut.writeFileHeader(accountFile, self.parent.getFullXmlFileName(), accDate)
                accountOut.writeRecord(contractId, payerId, aDate, accNumber, self.parent.getFullXmlFileName(), 
                                       forceString(accDate.year()), forceString(accDate.month()), accSum, self.log)
                accountOut.writeFileFooter()
                accountFile.close()
    #        container.summTotal = 0
    #        container.dictSums = {1 : 0.0}
    #        container.date = {1: (2000, 1, 1)}

        else:
            self.log(u'Нечего выгружать.')
            self.progressBar.step()


# *****************************************************************************************

    def createXML(self):
        outFile = QFile(self.parent.getFullXmlFileName())
        outFile.open(QFile.WriteOnly | QFile.Text)
        outFile2 = QFile( self.parent.getFullXmlPersFileName())
        outFile2.open(QFile.WriteOnly | QFile.Text)
        if self.parent.page1.chkExportTypeBelonging.isChecked() == False:
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
        exportDir = forceString(QtGui.qApp.preferences.appPrefs.get( 'ExportR29XMLExportDir', homePath))
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
        if self.parent.page1.chkExportTypeBelonging.isChecked() == False:
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
        self.recNum = 0 # номер записи
        self.caseNum = 1 # номер случая
        self.serviceNum = 1 # номер услуги
        self.dateNum = 1
        self.ossString = ''
        self.summ =0.0
        self.medicalAidKind = 0
        self._lastClientId = None
        self._lastEventId = None
        self._lastActionId = None
        self._emergencyCase = None
        self.medicalAidProfileCache = {}
        self.medicalAidKindCache = {}
        self.medicalAidTypeCache = {}
        self.rbPostFederalCache= {}
        self.rbPostRegionalCache = {}
        self.childrenNumber =0 
        self.childrenFlag = 0
        self.isOncology = 0


    def getStandartServiceIds(self):
        stmt = u"SELECT id FROM rbService WHERE name LIKE 'стандарт%медицинской%помощи%'"
        query = QtGui.qApp.db.query(stmt)
        while query.next():
            yield forceInt(query.record().value('id'))

    def writeRecord(self, record, miacCode, eventsInfo, accountId, bufferForConsult, contractBegDate, log):
        accountNumber = forceString(QtGui.qApp.db.translate(QtGui.qApp.db.table('Account'), 'id', accountId, 'number'))
        self.contractBegDate = contractBegDate
        self.isOncology = 1 if u'ОНК' in accountNumber  or u'онк' in accountNumber or u'Онк' in accountNumber else 0
        #Если есть более одного движения, и текущий action в строке не последний, то просто выкидываемся из метода
        hospitalDayAmount = 0
        anes =0 
        eventId = forceInt(record.value('event_id'))
        eventExternalId = forceString(record.value('eventExternalId'))
        actionId = forceInt(record.value('action_id'))
        accountItemId = forceInt(record.value('accountItemId'))


        clientId = forceRef(record.value('client_id'))

        age = forceInt(record.value('clientAge'))
        if forceInt(record.value('preEventId')):
            begDate = self.getDateForStationary(forceInt(record.value('preEventId')))
            if not begDate:
                begDate = forceDate(record.value('begDateEvent'))
        else:
            begDate = forceDate(record.value('begDateEvent'))
        self.parent.endDate=begDate 
        if record.value('endDateEvent'): endDate = forceDate(record.value('endDateEvent'))
        else:
            endDate = forceDate(Export29XMLCommon.getLatestDateOfVisitOrAction(QtGui.qApp.db, accountId, eventId))
        self.parent.endDate=endDate 
        federalPrice = forceDouble(record.value('federalPrice'))
        regionalPrice = forceDouble(record.value('regionalPrice'))
        federalSum = Export29XMLCommon.doubleToStrRounded(forceDouble(record.value('federalSum')))
        regionalSum = Export29XMLCommon.doubleToStrRounded(forceDouble(record.value('regionalSum')))
        personId = forceRef(record.value('execPersonId'))
        profileStr = forceString(record.value('medicalAidProfileFederalCode'))
        kindStr = None 
        typeStr = None
        if personId:
            profile, kindStr, typeStr  = self.getProfile(forceRef(record.value('serviceId')), personId)
            profileStr = (profile if profile else forceString(record.value('medicalAidProfileFederalCode')))[:3]
        else:
            log(u'У пациента %d в событии %d не указан исполнитель' % (clientId, eventId), True)
        serviceId = forceRef(record.value('serviceId'))
        serviceNote = (forceString(QtGui.qApp.db.translate(QtGui.qApp.db.table('rbService'), 'id', serviceId, 'note')).split(";"))
        if 'isSumAmount' in serviceNote:
             tableAI = QtGui.qApp.db.table('Account_Item')
             tableECSG = QtGui.qApp.db.table('Event_CSG')
             tableECSG = tableECSG.leftJoin(tableAI, tableECSG['id'].eq(tableAI['eventCSG_id']))
             amount = forceDouble(QtGui.qApp.db.getSum(tableECSG, 
                                                    'Account_Item.amount', '(Event_CSG.parentCSG_id =%s OR Event_CSG.id =%s)  AND Event_CSG.id IS NOT NULL and Account_Item.master_id = %s'
                                                    %(forceString(record.value('CSGEventId')), forceString(record.value('CSGEventId')), accountId)))
        else:
            amount = forceDouble(record.value('amount'))
        oss = u''
        if forceString(record.value('eventTypeRegionalCode')) == '3010' and not bufferForConsult:
            bufferForConsult = bufferForConsult + Export29XMLCommon.getActionForHealthCentr(QtGui.qApp.db, accountId, eventId)
        
        # if self._lastClientId != clientId: # новая запись, иначе - новый случай
            # if self._lastClientId:
                # self.recNum += 1
                # self.writeTextElement('COMENTSL', self.ossString)
                # self.writeBenefits(clientId, eventId)
                # self.writeEndElement() # SLUCH
                # self.writeEndElement() # ZAP
                # self._lastEventId = None
            # self._lastClientId = clientId
        
        self._lastClientId = clientId
        if self._lastEventId != eventId: # or (self._lastEventId == eventId and 'isSelfCase' in serviceNote) or ('isSTG' in serviceNote and forceString(record.value('STGid')) != self._lastStgID):# and self._emergencyCase == None:
          #  self.visitAmount  = visitAmount
            
            
            if self._lastEventId:
                    self.recNum += 1
                 #   self.writeTextElement('COMENTSL', self.ossString)                
                 #   self.writeEndElement() # SL  
                    self.writeTextElement('IDSP', self.medicalAidKind)
                    self.writeTextElement('SUMV',('%10.2f' % round(self.summ,2)).strip())
                    self.summ = 0
                    self.writeBenefits(self._lastClientId, self._lastEventId)
                    self.writeEndElement() # SLUCH
                    self.writeEndElement() # ZAP
            self.writeStartElement('ZAP')
        
#         if self._lastClientId != clientId: # новая запись, иначе - новый случай
#             if self._lastClientId:
#                 self.recNum += 1
#                 self.writeTextElement('COMENTSL', self.ossString)
#                 self.writeBenefits(self._lastClientId, self._lastEventId)
#                 self.writeEndElement() # SLUCH
#                 self.writeEndElement() # ZAP
#                 self._lastEventId = None
#             self._lastClientId = clientId
# 
#             self.writeStartElement('ZAP')
            self.medicalAidKind = forceString(record.value('medicalAidUnitFederalCode'))
            self.writeTextElement('N_ZAP', ('%4d' % self.recNum).strip())
            self.writeTextElement('PR_NOV', '0')
            self.writeStartElement('PACIENT')
            self.writeTextElement('ID_PAC',  ('%d' % clientId)[:36])
            # Региональный код справочника ВИДЫ ПОЛИСОВ.
            npolis, spolis, vpolis, insurerOGRN, insurerOKATO, insurerName, smo, insurerId = Export29XMLCommon.getClientPolicy(QtGui.qApp.db, clientId, begDate, endDate)
#            npolis = forceString(record.value(u'policyNumber'))[:20]
#            vpolis = forceString(record.value('policyKindCode'))[:1]
            docCode = forceInt(record.value('documentTypeCode'))
            if vpolis == '1' and not docCode:
                log(u'В регистрационной карте пациента %d не указан документ' % clientId, True)
       #     if docCode and  docCode > 1:
       #         oss += u'ОСС=2,'

#            smo = forceString(record.value('insurerMiac'))[:5]
#Паспорт - ClientDocument ClientDocumentType (паспорт РФ)
#Ориентируемся на ___номер полиса___ и страховую компанию SMO
       #     if ((not npolis) and (not smo) and (docCode == 1)): #предъявил только паспорт
       #         oss += u'ОСС=1,'
            if not vpolis:
                log(u'В регистрационной карте пациента %d не указан вид полиса' % clientId, True)
            if not vpolis and not spolis and not npolis:
                log(u'В регистрационной карте пациента %d нет действующего полиса на начало обращения' % clientId, True)
            self.writeTextElement('VPOLIS', vpolis)
            if vpolis == '3':
                self.writeTextElement('ENP', npolis)
            else:
                self.writeTextElement('SPOLIS', spolis)
                self.writeTextElement('NPOLIS', npolis)
            self.writeTextElement('SMO', smo)

            if not smo:
                self.writeTextElement('SMO_OGRN', insurerOGRN)
                self.writeTextElement('SMO_OK', insurerOKATO)
                if not insurerOGRN and not insurerOKATO: 
                    if not insurerName or insurerName == (u'',):
                        log(u'У пациента %d не указана страховая' % clientId, True)
                    else:
                        self.writeTextElement('SMO_NAM', insurerName, writeEmtpyTag = False)
              
            birthDate = forceDate(record.value('birthDate'))

            groupInvalid = Export29XMLCommon.getSpecialCaseCode(QtGui.qApp.db, clientId, endDate, 1)
            if groupInvalid !=[]:
                self.writeTextElement('INV', forceString(groupInvalid[0]))
            directionEIRNumber, flagDirection, flagExpertise, flagOncology = Export29XMLCommon.getDirectionEIRNumber(QtGui.qApp.db, forceInt(record.value('preEventId')) if forceInt(record.value('preEventId')) >0 else eventId)
            if flagExpertise == 1:
                 self.writeTextElement('MSE', '1')
                 
            if '0003' in Export29XMLCommon.getSpecialCaseCode(QtGui.qApp.db, clientId, begDate):
                self.childrenNumber = 1
                self.writeTextElement('NOVOR', '%s%s%s' % (forceString(record.value('sex'))[:1], birthDate.toString('ddMMyy'), self.childrenNumber ))
                if '0010' in Export29XMLCommon.getSpecialCaseCode(QtGui.qApp.db, clientId, begDate) and forceInt(record.value('birthWeight')) > 0 :
                    self.writeTextElement('VNOV_D', (forceString(record.value('birthWeight'))))
            elif '0009' in Export29XMLCommon.getSpecialCaseCode(QtGui.qApp.db, clientId, begDate):
                 self.writeTextElement('NOVOR', '%s%s%s' % (forceString(record.value('sex'))[:1], birthDate.toString('ddMMyy'), self.childrenNumber ))
                 self.childrenNumber = self.childrenNumber + 1
                 if '0010' in Export29XMLCommon.getSpecialCaseCode(QtGui.qApp.db, clientId, begDate) and forceInt(record.value('birthWeight')) > 0 :
                    self.writeTextElement('VNOV_D', (forceString(record.value('birthWeight'))))
            else:
                self.writeTextElement('NOVOR', '0')

            self.writeEndElement() # PACIENT
        
        service = {}
        serviceId = forceRef(record.value('serviceId'))
        serviceNote = (forceString(QtGui.qApp.db.translate(QtGui.qApp.db.table('rbService'), 'id', serviceId, 'note')).split(";"))
        service['id'] = serviceId
        serviceStr = self.getServiceInfis(serviceId)
   #     serviceNote = forceString(QtGui.qApp.db.translate(QtGui.qApp.db.table('rbService'), 'id', serviceId, 'note'))
        if forceString(record.value('pgCode')) != '' and forceString(record.value('pgCode')) != ' ':
            service['CODE_USL'] = serviceStr  + ':' +  forceString(record.value('pgCode'))
        else: 
            service['CODE_USL'] = serviceStr
        service['note'] = serviceNote

        eventTypeCode = forceString(record.value('eventTypeCode'))
        personRegionalCode = forceString(record.value('personRegionalCode'))
        personSNILS = forceString(record.value('personSNILS'))
        visitId = forceInt(record.value('visit_id'))
        if (self._lastEventId != eventId): # or ('isSelfCase' in serviceNote) or ('isSTG' in serviceNote and forceString(record.value('STGid')) != self._lastStgID)) :# and self._emergencyCase == None:
            if self._lastEventId:
                service = {}

            
            if 'isSelfCase' in serviceNote   and serviceStr[:4] != '3.45':
                begDate = endDate = Export29XMLCommon.getDatesForConsultVisit(QtGui.qApp.db, visitId)
                personSNILS = Export29XMLCommon.getPersonRegionalCodeForConsultVisit(QtGui.qApp.db, visitId)
            
            self._lastEventId = eventId
            self._lastStgID = forceString(record.value('CSGEventId'))
            self._lastActionId = actionId
            
            self.writeStartElement('Z_SL')
            self.writeTextElement('IDCASE', '%d' % self.caseNum)
            self.writeTextElement('USL_OK',  forceString(record.value('medicalAidTypeCode') if not typeStr else  typeStr))
            self.writeTextElement('VIDPOM', forceString(record.value('medicalAidKindCode') if not kindStr else kindStr))
            forPom = Export29XMLCommon.getHelpForm(QtGui.qApp.db, eventId, forceString(record.value('order')))
            self.writeTextElement('FOR_POM', forceString(forPom))
            if ((miacCode[:6] !=forceString(record.value('relegateOrgMiac')) and forPom != 1) 
                or ('isStacionary' in serviceNote and forPom != 1)  or ('isGema' in serviceNote and forPom != 1)):
                self.writeTextElement('NPR_MO', forceString(record.value('relegateOrgMiac')),  writeEmtpyTag = False)

            directionEIRNumber, flagDirection, flagExpertise, flagOncology = Export29XMLCommon.getDirectionEIRNumber(QtGui.qApp.db, eventId)
            if flagDirection == 1:
                if (directionEIRNumber != '' or directionEIRNumber):
                    self.writeTextElement('ORD_NO', directionEIRNumber)
            direcrionDate =  forceDate(record.value('directionDate'))
            if ((miacCode[:6] !=forceString(record.value('relegateOrgMiac')) and forceString(record.value('relegateOrgMiac')) != '' and forPom != 1)
                or ('isStacionary' in serviceNote and forPom != 1)
                or ('isGema' in serviceNote and forPom != 1)
                ):
                self.writeTextElement('NPR_DATE', direcrionDate.toString(Qt.ISODate))
            lpu1Str = Export29XMLCommon.getMobileModule(QtGui.qApp.db, forceDouble(miacCode)) if eventTypeCode[:2] == '04' else ''
            self.writeTextElement('LPU', miacCode[:6])
            serviceNote = (forceString(QtGui.qApp.db.translate(QtGui.qApp.db.table('rbService'), 'id', serviceId, 'note')).split(";"))
            begDate = forceDate(record.value('begDateEvent'))
            endDate = forceDate(record.value('endDateEvent'))
            self.writeTextElement('DATE_Z_1', begDate.toString(Qt.ISODate))

            self.writeTextElement('DATE_Z_2', endDate.toString(Qt.ISODate))
            service['flagOncology'] = flagOncology

            if forceInt(record.value('preEventId')): 
                begDate = forceDate(record.value('begDateEvent'))
        #    service['DATE_IN'] = begDate.toString(Qt.ISODate)
        #    service['DATE_OUT'] = endDate.toString(Qt.ISODate)
            
            birthDate = forceDate(record.value('birthDate'))
      #      if (begDate.toPyDate() - birthDate.toPyDate()).days < 29:
      #          oss += u'ОСС=3,'
            serviceNote = forceString(QtGui.qApp.db.translate(QtGui.qApp.db.table('rbService'), 'id', serviceId, 'note'))
            duration = self.getVisitsAmount(eventId) 
            if duration == 0:
                if forceInt(record.value('ContractTariffType')) == CTariff.ttEventByMES or forceInt(record.value('ContractTariffType')) == CTariff.ttEventByMESLen: 
                    duration = forceInt(updateDurationEvent(begDate, endDate,  forceString(record.value('eventTypeId)')))) - 1
                if duration == 0:
                    duration = 1
                    
            if 'isStacionary' in serviceNote  or 'isGema' in serviceNote :
                self.writeTextElement('KD_Z', forceString(duration)) #serviceStr[:4] != '2.38' and serviceStr[:4] != '1.25' else '1')

            
            service['DS'] = forceString(record.value('stgMKB') if ('isSTG'  in serviceNote or 'isAdditionalSTG'  in serviceNote) else forceString(record.value('MKB')))
            self.writeTextElement('RSLT', forceString(record.value('eventResultFederalCode')))
            # Федеральный код из справочника РЕЗУЛЬТАТ ОСМОТРА. Результат ЗАКЛЮЧИТЕЛЬНОГО ДИАГНОЗА.
            self.writeTextElement('ISHOD', forceString(record.value('resultFederalCode')))

            
            if '0003' in Export29XMLCommon.getSpecialCaseCode(QtGui.qApp.db, clientId, begDate):
                self.writeTextElement('OS_SLUCH', '1')
            if ( serviceStr[:4] == '3.18' or serviceStr[:4] == '3.20' or serviceStr[:4] == '3.23'):
                self.writeTextElement('OS_SLUCH', '3')
            if (serviceStr[:4] == '3.19'):
                self.writeTextElement('OS_SLUCH', '4')
            ot = forceString(record.value('patrName')) 
            if '0005' in Export29XMLCommon.getSpecialCaseCode(QtGui.qApp.db, clientId, begDate):
                self.writeTextElement('OS_SLUCH', '2')
                
        case = {}
        service = {}
        service['LPU'] = miacCode[:6]

        duration = self.getVisitsAmount(eventId) 
        if duration == 0:
            if forceInt(record.value('ContractTariffType')) == CTariff.ttEventByMES or forceInt(record.value('ContractTariffType')) == CTariff.ttEventByMESLen: 
                duration = forceInt(updateDurationEvent(forceDate(record.value('begDateEvent')), endDate,  forceString(record.value('eventTypeId)')))) - 1
            if duration == 0:
                duration = 1
        
        service['VID_VME'] = None
        if forceInt(record.value('ContractTariffType')) == CTariff.ttEventByMES or forceInt(record.value('ContractTariffType')) == CTariff.ttEventByMESLen:
            service['VID_VME'] = self.getOperationCode(forceInt(record.value('event_id')))
            
        if 'hasOperation' in serviceNote:
            service['VID_VME'] = self.getOperationService(serviceId)
        if 'isNotKSG' not in serviceNote:
            service['N_KSG'] = self.getNumberKSG(eventId)
        if contractBegDate  > QDate(2019, 10, 30):
            service['UID_MIS']= forceInt(record.value('accountItemId'))
#             if visitId:
#                 service['UID_MIS']= visitId
#             elif actionId:
#                 service['UID_MIS']= actionId
#             else:
#                 service['UID_MIS']= eventId
            
        if 'isStacionary' in serviceNote  or 'isGema' in serviceNote :
             case['KD'] = forceString(duration) if 'isOneDay' not in serviceNote else '1'
        service['PROFIL'] = profileStr
        if contractBegDate > QDate(2019, 10, 31):
            service['PODR'] =forceString(record.value('orgStructureCode'))
            service['ADDR_CODE'] =forceString(record.value('orgStructureInternalCode'))
            case['ADDR_CODE'] =forceString(record.value('orgStructureInternalCode'))
        hospitalActionId = forceRef(record.value('hospitalActionId'))
        if hospitalActionId:
            bedProfile= self.getHospitalBedProfile(hospitalActionId)
           # self.writeTextElement('PROFIL_K', bedProfile)
          #  service['PROFIL_K'] = bedProfile
            case['PROFIL_K'] = bedProfile
            

        service['DET'] = u'1' if age < 18 else u'0'
        birthDate = forceDate(record.value('birthDate'))
        service['DS'] = forceString(record.value('stgMKB') if ('isSTG'  in serviceNote or 'isAdditionalSTG'  in serviceNote) else forceString(record.value('MKB')))
        serviceNote = (forceString(QtGui.qApp.db.translate(QtGui.qApp.db.table('rbService'), 'id', serviceId, 'note')).split(";"))
        if 'isSTG' in serviceNote or 'isAdditionalSTG' in serviceNote:
            begDate = forceDate(record.value('csgBegDate'))
            endDate = forceDate(record.value('csgEndDate'))


        service['DATE_IN'] = begDate.toString(Qt.ISODate)
        service['DATE_OUT'] = endDate.toString(Qt.ISODate)
        directionEIRNumber, flagDirection, flagExpertise, flagOncology = Export29XMLCommon.getDirectionEIRNumber(QtGui.qApp.db, eventId)

        case['NHISTORY'] = eventId if 'isDiagnosticResearch' not in serviceNote else forceInt(record.value('action_id'))
        
        case['PROFIL'] = profileStr
        
        if 'isSelfCaseForVisit' in serviceNote: # and serviceStr[:4] != '3.45' and serviceStr[:4] != '3.39' and serviceStr[:4] != '2.34':
                begDate = endDate = Export29XMLCommon.getDatesForConsultVisit(QtGui.qApp.db, visitId)

            
        if 'isDateByAction' in serviceNote and forceInt(record.value('action_id')): # :
            (begDate, endDate) = Export29XMLCommon.getDatesForAction(QtGui.qApp.db,
                                                                forceInt(record.value('event_id')),
                                                                forceInt(record.value('action_id')),
                                                                serviceNote)    
                
        if not begDate:
             log(u'Пациент %d не указана дата начала события' % clientId, True)
        else:
            case['DATE_1'] = begDate.toString(Qt.ISODate)
        if not endDate:
            log(u'Пациент %d не указана дата окончкания события' % clientId, True)
        else:
            case['DATE_2'] = endDate.toString(Qt.ISODate)
        
        
        # диагноз
        case['DS0'] = forceString(record.value('PreMKB'))
        if 'isSTG' in serviceNote or 'isAdditionalSTG'  in serviceNote:
            case['DS1'] = forceString(record.value('stgMKB')) 
        else:   
            case['DS1'] = forceString(record.value('MKB'))
        case['DS2'] = forceString(record.value('AccMKB'))
        case['DS3'] = forceString(record.value('CompMKB'))
        case['C_ZAB'] = forceString(record.value('diseaseCharacter'))
        if self.isOncology == 1:
            if flagOncology != 0:
                case['DS_ONK' ] = forceString(flagOncology)
            else: 
                case['DS_ONK' ] = '0'
                flagOncology = 0
        if forceString(record.value('dispanserStatus')) != '0':
            case['DN' ] = forceString(record.value('dispanserStatus'))  
        case['eventId'] = eventId
        if personId or forceRef(record.value('eventExecPersonId')):
       # TNMS = forceString(record.value('TNMS'))
            (MKB, resultFederalCode, traumaCode, AccMKB, CompMKB, 
             PreMKB, TNMS, characterDiag, 
             flagOncology1, onk, dispanserStatus) =  Export29XMLCommon.getDiagnosis(self,
                                                                           eventId, 
                                                                           personId, 
                                                                           forceRef(record.value('eventExecPersonId')),
                                                                           contractBegDate)
        MKB = forceString(record.value('MKB'))
        if not MKB:
            log(u'Не указан диагноз в событии %d у пациента %d' % (eventId, clientId), True)
        case['DET'] =  (u'1' if age < 18 else u'0')
                
        if 'isVisit' in serviceNote:
            p_cel = forceString(serviceNote[serviceNote.index('isVisit')+1].split(':')[1] )
            if MKB[:1] == 'Z' and  MKB != 'Z03.1' and (p_cel == '3.0'):
                case['P_CEL'] = '3.1'
            elif MKB[:1] == 'Z' and  MKB != 'Z03.1' and (p_cel == '1.0'): 
                case['P_CEL'] = '2.6'  
            else:
                case['P_CEL'] = p_cel
        case['TNMS1'] = TNMS
        case['onk'] = onk
        TNMS = '' # if (TNMS == '' or TNMS ==u'cTx cNx cMx cSx pTx pNx pMx pSx') # else self.getPhaseId(TNMS, MKB, contractBegDate)

            
        case['flagOncology']= flagOncology
        case['TNMS'] = TNMS

        personCode = forceString(self.parent.getPersonSpecialityFederalCode(personId))
        case['PRVS'] = personCode
        service['PRVS'] = personCode
        service['MR_USL_N'] = 1 if self.isOncology == 0 else 0 
        
        if not personCode:
            log(u'Не указан исполнитель визита/мероприятия в событии %d у пациента %d' % (eventId, clientId), True)
#            self.writeTextElement('PRVS', forceString(self.parent.getPersonSpecialityFederalCode(personId)))
        case['VERS_SPEC'] = u'V021'
        case['IDDOKT'] = personSNILS
        case['ED_COL'] =  ('%6.2f' % amount).strip()
       # if forceString(record.value('accountItemId')) == '4347998':
        tableAI = QtGui.qApp.db.table('Account_Item')
        tableECSG = QtGui.qApp.db.table('Event_CSG')
        tableECSG = tableECSG.leftJoin(tableAI, tableECSG['id'].eq(tableAI['eventCSG_id']))
        summ = forceDouble(QtGui.qApp.db.getSum(tableECSG, 
                                                    'sum', 'Event_CSG.parentCSG_id =%s AND Event_CSG.id IS NOT NULL and Account_Item.master_id = %s'
                                                    %(forceString(record.value('CSGEventId')), accountId)))
        summ = Export29XMLCommon.doubleToStrRounded(forceDouble(record.value('sum')))  + summ 
        self.summ = self.summ +Export29XMLCommon.doubleToStrRounded(forceDouble(record.value('sum')))
        price = forceDouble(record.value('price')) - regionalPrice - federalPrice
        case['TARIF'] = ('%10.2f' % summ)

        case['SUM_M'] = ('%10.2f' % summ)

        container.dictSums[self.caseNum] = 0.0
        self.caseNum+= 1

        serviceId = forceRef(record.value('serviceId'))
        service['id'] = serviceId
        serviceStr = self.getServiceInfis(serviceId)
        serviceNote = forceString(QtGui.qApp.db.translate(QtGui.qApp.db.table('rbService'), 'id', serviceId, 'note'))
        if 'isSTG' in serviceNote:
            service['DENT'] = self.getDent(forceString(record.value('STGid')))
            if service['DENT']:
                service['COMENTU'] = ''
        else:
            service['COMENTU'] = ''
        if 'isImpossibleIncompleteCase' not in serviceNote :
            service['NPL'] = forceString(Export29XMLCommon.getIncompleteReason(QtGui.qApp.db, eventId))
        elif 'isIncompleteCase' in serviceNote:
            service['NPL'] = forceString(self.getIncompleteReason(forceString(record.value('STGid')), eventId))
            
        transferName = Export29XMLCommon.getTransferName(QtGui.qApp.db,  eventId)
        if transferName:
            case['P_PER']  = ('%s' % transferName )
        
        if forceString(record.value('pgCode')) != '' and forceString(record.value('pgCode')) != ' ':
            service['CODE_USL'] = serviceStr  + ':' +  forceString(record.value('pgCode'))
        else: 
            service['CODE_USL'] = serviceStr
        service['note'] = serviceNote
        service['LPU'] = miacCode[:6]
        if self.parent.endDate > QDate(2019, 10, 31):
            case['PODR'] = forceString(record.value('orgStructureCode'))
            service['PODR'] =forceString(record.value('orgStructureCode'))
        service['PROFIL'] = profileStr
        service['DET'] = u'1' if age < 18 else u'0'

        if 'isDateByAction' in serviceNote and forceInt(record.value('action_id')): # :
                (begDate, endDate) = Export29XMLCommon.getDatesForAction(QtGui.qApp.db,
                                                                    forceInt(record.value('event_id')),
                                                                    forceInt(record.value('action_id')),
                                                                    serviceNote)
        if 'isSTG' in serviceNote or 'isAdditionalSTG'  in serviceNote:
                begDate = forceDate(record.value('csgBegDate'))
                endDate = forceDate(record.value('csgEndDate'))

        service['DATE_IN'] = begDate.toString(Qt.ISODate)
        service['DATE_OUT'] = endDate.toString(Qt.ISODate)
        service['DS'] = forceString(record.value('stgMKB') if ('isSTG'  in serviceNote or 'isAdditionalSTG'  in serviceNote) else forceString(record.value('MKB')))
        if not endDate:
            log(u'Ошибка:  В событии %d у пациента %d не указан дата окончания визита/мероприятия' % ( forceInt(record.value('eventId')), forceInt(record.value('client_id'))), True)
        if not forceString(record.value('MKB')) and not forceString(record.value('stgMKB')):
            log(u'Ошибка:  В событии %d у пациента %d не указан диагноз' % ( forceInt(record.value('eventId')), forceInt(record.value('client_id'))), True)
        if len(forceString(record.value('MKB')))<4 and Export29XMLCommon.diagnosisHasSpecification(QtGui.qApp.db, forceString(record.value('MKB'))) == True:
            log(u'Ошибка:- В событии %d у пациента %d у диагноза не указана подрубрика' % ( forceInt(record.value('eventId')), forceInt(record.value('client_id'))), True)
            
        summ = Export29XMLCommon.doubleToStrRounded(forceDouble(record.value('sum')))
        serviceId = forceRef(record.value('serviceId'))
        serviceNote = (forceString(QtGui.qApp.db.translate(QtGui.qApp.db.table('rbService'), 'id', serviceId, 'note')).split(";"))
        serviceStr = self.getServiceInfis(serviceId)
        service['personId'] = personId
        personCode = forceString(self.parent.getPersonSpecialityFederalCode(personId))
        service['PRVS'] = personCode
        if not personId:
            log(u'Ошибка:  В событии %d у пациента %d не указан исполнитель визита/мероприятия' % (forceInt(record.value('eventId')), forceInt(record.value('client_id'))), True)
        personSNILS = forceString(QtGui.qApp.db.translate('Person', 'id', personId, 'SNILS'))
        
        if not personSNILS:
            log(u'В регистрационной карте сотрудника %d не указан СНИЛС' % clientId, True)
        else:
            service['CODE_MD'] = personSNILS[0:3] + '-' +personSNILS[3:6]+'-' +personSNILS[6:9]+'-' +personSNILS[9:11]
        eventTypeCode = forceString(record.value('eventTypeCode'))
        lpu1Str = Export29XMLCommon.getMobileModule(QtGui.qApp.db, forceDouble(miacCode)) if eventTypeCode == '04' else ''
        service['LPU_1'] = lpu1Str    
        service['KOL_USL'] =  forceDouble(record.value('amount'))
        service['TARIF'] = price

        service['SUMV_USL'] = summ
        service['eventId'] = eventId
        service['REFERRAL_NO'] = self.getInfoFromAP(eventId, 'REFERRAL_NO')
        if forceString(record.value('usedCoefficients')) != ' ' and forceString(record.value('usedCoefficients')) != '':

            service['COMENTU']  = json.loads(forceString(record.value('usedCoefficients')))


        
        container.summTotal +=                  Export29XMLCommon.doubleToStrRounded(summ + regionalSum)
        container.dictSums[self.caseNum - 1] += Export29XMLCommon.doubleToStrRounded(summ + regionalSum)
        if 'isAdditionalSTG' not in serviceNote: 
            container.summCaseTotal = container.summCaseTotal + 1

        oss = forceString(QString(oss[:-1]))
        self.ossString = oss
        case['COMENTSL'] =  self.ossString
        if 'isAdditionalSTG' not in serviceNote:
            addCsg = forceInt(QtGui.qApp.db.translate(QtGui.qApp.db.table('Event_CSG'), 'parentCSG_id', forceString(record.value('CSGEventId')), 'id'))
            if addCsg == 0:
                self.writeCases(case, service, log, contractBegDate, 0, miacCode)
            elif addCsg > 0: #and accountId == forceInt(QtGui.qApp.db.getRecordEx(
                             #                                       QtGui.qApp.db.table('Account_Item'), '', 'eventCSG_id', addCsg, 'master_id')):
                self.writeCases(case, service, log, contractBegDate, 2, miacCode)
            else: 
                self.writeCases(case, service, log, contractBegDate, 0, miacCode)
        else:
            self.writeCases(case, service, log, contractBegDate, 1, miacCode)
            
        
    def writeCases(self, case, service, log, contractBegDate, flag, miacCode):
        order = [ 'LPU_1', 'PODR', 'ADDR_CODE', 'PROFIL', 'PROFIL_K', 'DET',  
                  'P_CEL', 'NHISTORY', 'P_PER', 'DATE_1','DATE_2',
                   'KD', 'DS0', 'DS1', 'DS2', 'DS3', 'C_ZAB', 'DS_ONK', 
                   'DN', 'CODE_MES1', 'CODE_MES2', 
                   'NAPR', 'CONS', 'ONK_SL', 'REAB', 
                   'PRVS', 'VERS_SPEC', 'IDDOKT', 'ED_COL', 'TARIF', 
                   'SUM_M', 'SANK', 'USL', 'COMENTSL']
        if flag == 1:
            self.writeService(service, contractBegDate)
            self.writeEndElement()
        else:
            self.writeStartElement('SL')
            self.writeTextElement('SL_ID', ('%s' % uuid.uuid4()))
            if contractBegDate  > QDate(2019, 10, 30):
                self.writeTextElement('SID_MIS', ('%s' % case['eventId']))
            for tag in order:
 #               if tag == 'DS2':
 #                   for ds in case['DS2']:
 #                       self.writeTextElement(tag, forceString(ds), writeEmtpyTag = False)
                if tag == 'USL':
                    self.writeService(service, contractBegDate)
                elif tag == 'NAPR' and case['flagOncology'] == 1 and self.isOncology == 1:
                    self.writeDirection(case['eventId'], miacCode)
                elif tag == 'CONS' and case['flagOncology'] in (0, 1):
                    self.writeCons(case['eventId'])
                elif tag == 'ONK_SL' and case['flagOncology'] == 0:
                     Export29XMLCommon.writeOncology1(self,case['eventId'], case['TNMS'], case['TNMS1'], self.getSchema(case['eventId']), 0, case['onk'])
                elif tag in case.keys():
                    self.writeTextElement(tag, forceString(case[tag]), writeEmtpyTag = False)
            if flag == 0:
                self.writeEndElement()
                


    def writeService(self, service, contractBegDate):
     #   order = [ 'LPU', 'LPU_1', 'PODR', 'PROFIL', 'VID_VME', 'DET', 'DATE_IN', 'DATE_OUT','DS', 'CODE_USL', 'KOL_USL', 'TARIF', 'SUMV_USL', 'PRVS', 'CODE_MD', 'NPL', 'COMENTU']
        if contractBegDate < QDate(2021, 12, 31):
            order = ['UID_MIS', 'N_KSG', 'DKK1', 'DKK2', 'LPU', 'LPU_1', 'PODR',
                  'ADDR_CODE', 'PROFIL',  'PROFIL_K', 'VID_VME', 'DET', 'DATE_IN', 
                  'DATE_OUT','DS', 'CODE_USL', 'KOL_USL', 'TARIF', 'ST_USL',
                   'SUMV_USL', 'PRVS', 'CODE_MD', 'NAPR', 'ONK_USL', 'NPL', 'COMENTU']
        else:
             order = ['UID_MIS', 'N_KSG', 'DKK1', 'DKK2', 'LPU', 'LPU_1', 'PODR',
                  'ADDR_CODE', 'PROFIL',  'PROFIL_K', 'VID_VME', 'DET', 'DATE_IN', 
                  'DATE_OUT','DS', 'CODE_USL', 'KOL_USL', 'TARIF', 'ST_USL',
                   'SUMV_USL', 'MR_USL_N', 'NAPR', 'ONK_USL', 'NPL', 'COMENTU']
        self.writeStartElement('USL')
        self.writeTextElement('IDSERV', ('%8d' % self.serviceNum).strip()) # O N(8) номер записи в реестре услуг
        for tag in order:
            if tag in service.keys():
            #    if tag == 'ONK_USL' and service['flagOncology'] == 0:
            #        self.writeOncology1(service['eventId'], service['TNMS'], 1)
                if tag == 'COMENTU':
                    self.writeStartElement('COMENTU')
                    self.writeEndElement()
                    com = service[tag]
                    if com:
                        self.writeStartElement('KSLP')
                        
                        for coefficient in com.values():
                            self.writeTextElement('IT_SL', forceString(forceString(coefficient['__all__'])))
                            for item, coeff in coefficient.items(): 
                                if forceString(item) != u'__all__':
                                    self.writeStartElement('SL_KOEF')
                                    self.writeTextElement('IDSL', forceString(forceString(item)))
                                    self.writeTextElement('Z_SL', forceString(Export29XMLCommon.doubleToStrRounded(coeff)))
                                    self.writeEndElement() #SL_KOEF
                        self.writeEndElement() #KSLP
                    if contractBegDate  > QDate(2016, 12, 31):
                        if 'DENT' in service.keys():
                            dents = service['DENT']
                            service['DENT'] = []
                            if dents != {}:
                                self.writeStartElement('DENTES')
                                for dent, surfs in dents.items():
                                    self.writeStartElement('DENT')
                                    self.writeTextElement('DENT_NUM', forceString(forceString(dent)))
                                    if surfs != [''] and  surfs != [' ']  and surfs and surfs[0] != '' :
                                        if surfs[0] !='' and surfs[0] !=' ':
                                            self.writeStartElement('SURFACES')
                                            for surf in surfs:
                                                self.writeTextElement('SURF', forceString(forceString(surf)))
                                            self.writeEndElement() #SURFACES
                                    self.writeEndElement() #DENT
                                self.writeEndElement() #DENTES
                           #     self.writeEndElement()
                elif tag == 'MR_USL_N':
                    if service['MR_USL_N'] == 1:
                        self.writeStartElement('MR_USL_N')
                        self.writeTextElement('MR_N', '1')
                    self.writeTextElement('PRVS', forceString(service['PRVS']) )
                    self.writeTextElement('CODE_MD', forceString(service['CODE_MD']))
                    if service['MR_USL_N'] == 1:
                        self.writeEndElement() # MR_USL_N   
                        
                else:
                    self.writeTextElement(tag, forceString(service[tag]))
        self.writeEndElement() #USL
        self.serviceNum += 1
        
    def getInfoFromAP(self, eventId, descr):
        stmt = """SELECT `ActionProperty_String`.value as cCode
                     FROM `Action`
                     LEFT JOIN `ActionType` ON `Action`.`actionType_id` = `ActionType`.`id`
                     LEFT JOIN ActionProperty ON ActionProperty.action_id = Action.id
                     LEFT JOIN ActionPropertyType ON ActionProperty.type_id = ActionPropertyType.id
                     LEFT JOIN ActionProperty_String ON ActionProperty_String.id =  ActionProperty.id
                     WHERE `Action`.`event_id`=%d AND ActionPropertyType.descr = '%s'
                             AND  `Action`.`deleted` =0""" %(eventId, descr)
        query =  QtGui.qApp.db.query(stmt)
        
     #   query1 =  QtGui.qApp.db.query(stmt1)
        if query.next():
            return forceString(query.record().value('cCode'))
        
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
        
    def writeDirection(self, eventId, lpu):
        str1 = u"Да"
        stmt3 = """select a1.id as actionId, a1.begDate as directionDate, at2.code as code,  at1.flatCode as serviceCode, Organisation.miacCode as NAPR_MO
                    from ActionProperty as ap1
                    left join Action as a1 on ap1.action_id=a1.id 
                    left join ActionType at1 on at1.id=a1.actionType_id 
                     left join ActionProperty_String on ActionProperty_String.id=ap1.id 
                     left JOIN ActionProperty as ap2 ON ap1.action_id = ap2.action_id
                     left join ActionPropertyType as apt2 on  apt2.actionType_id=at1.id   AND ap2.type_id = apt2.id
                     left join ActionProperty_Organisation on ActionProperty_Organisation.id=ap2.id 
                     left JOIN Organisation  On Organisation.id  = ActionProperty_Organisation.value
                     left join Action a2 on a1.prevAction_id=a2.id 
                     left join ActionType at2 on at2.id=a2.actionType_id 
                     where at1.flatCode in ('consultationDirection', 'inspectionDirection', 'consultationTaktikInspectionDirection', 'consultationDirection2018', 'inspectionDirection2018', 'consultationTaktikInspectionDirection2018') and 
                     apt2.descr IN  ('DS_ONK', 'NAPR_MO')
                     and ap1.action_id=a1.id and ActionProperty_String.value='%s' and a1.event_id = %s AND a1.deleted = 0 -- group by a1.begDate, at2.code,at1.flatCode,Organisation.miacCode 
                      """%( str1, eventId)
        
        stmt = """select a1.id as actionId, a1.begDate as directionDate, at2.code as code,  at1.flatCode as serviceCode, ActionProperty_String.value as value, Organisation.miacCode as NAPR_MO
                    from Action as a1
                     left join ActionType at1 on at1.id=a1.actionType_id 
                  --   left join ActionPropertyType on ActionPropertyType.actionType_id=at1.id 
                     left join ActionProperty on ActionProperty.action_id=a1.id 
                     left join ActionPropertyType on ActionPropertyType.id=ActionProperty.type_id
                     left join ActionProperty_String on ActionProperty_String.id=ActionProperty.id 
                    left join ActionProperty_Organisation on ActionProperty_Organisation.id=ActionProperty.id 
                     left JOIN Organisation  On Organisation.id  = ActionProperty_Organisation.value
                     left join Action a2 on a1.prevAction_id=a2.id 
                     left join ActionType at2 on at2.id=a2.actionType_id 
                     where at1.flatCode in ('inspectionDirection', 'inspectionDirection2018') and 
                     ActionPropertyType.descr IN  ('NAZ_V', 'NAPR_MO')
                     and ActionProperty.action_id=a1.id  and a1.event_id = %s """%(eventId)
                  
        query = QtGui.qApp.db.query(stmt3)  
        query1 = QtGui.qApp.db.query(stmt)
        directions = {}
        
        while query.next():
            actionId = forceString(query.record().value('actionId'))
            if actionId not in directions.keys():
                directions[actionId] = {}
            directions[actionId]['NAPR_DATE'] = forceDate(query.record().value('directionDate')).toString(Qt.ISODate)
            code = forceString(query.record().value('serviceCode'))
            if forceString(query.record().value('NAPR_MO')) != '' and lpu != forceString(query.record().value('NAPR_MO')):
                directions[actionId]['NAPR_MO'] = forceString(query.record().value('NAPR_MO'))
            if code == 'consultationDirection' or 'consultationDirection2018':
                directions[actionId]['NAPR_V'] = '1'
            elif code == 'inspectionDirection' or code == 'inspectionDirection2018':
                if query1.next():
                    type = forceString(query1.record().value('value'))
                    serviceCode = forceString(query1.record().value('code'))
                    if type[:1] == '5':
                        directions[actionId]['NAPR_V'] = '2'
                    else:
                        directions[actionId]['NAPR_V'] = '3'
                        directions[actionId]['MET_ISSL'] = type[:1]
                        directions[actionId]['NAPR_USL'] = serviceCode
        order = ['NAPR_DATE', 'NAPR_MO', 'NAPR_V', 'MET_ISSL', 'NAPR_USL']
        for dir in directions:
            self.writeStartElement('NAPR')
            
            for element in order:
                if element in directions[dir].keys():
                    self.writeTextElement(element, directions[dir][element])
            self.writeEndElement() #NAPR   
            
    def writeCons(self, eventId):
        stmt = """SELECT ActionType.flatCode as flatCode, ActionPropertyType.descr as descr, ActionPropertyType.shortName as name, ActionProperty.id,  
                        ActionProperty_Double.value as v1, 
                        ActionProperty_String.value as v2, 
                        ActionProperty_Date.value as v3,
                        Action.id AS actionId
                        FROM Action 
                        LEFT JOIn ActionProperty ON ActionProperty.action_id = Action.id 
                        LEFT JOIN ActionPropertyType ON ActionPropertyType.id = ActionProperty.type_id 
                        LEFT JOIN ActionType ON ActionType.id = Action.actionType_id 
                        LEFT JOIN ActionProperty_Double ON ActionProperty_Double.id = ActionProperty.id
                        LEFT JOIN ActionProperty_String ON ActionProperty_String.id = ActionProperty.id
                        LEFT JOIN ActionProperty_Date ON ActionProperty_Date.id = ActionProperty.id
                        WHERE flatCode IN ('ControlListOnko', 'Consilium') AnD Action.deleted =0 AND ActionProperty.deleted =0  and Action.event_id = %d and ActionPropertyType.shortName IN ('kosilium', 'kosiliumDate') """ %eventId
        query = QtGui.qApp.db.query(stmt)
        cons = {}
        while query.next(): 
            if forceString(query.record().value('actionId')) not in cons.keys() and ((forceDate(query.record().value('v3'))).toString(Qt.ISODate) or forceString(query.record().value('v2')) != ''):
                cons[forceString(query.record().value('actionId'))] = {}
            if forceString(query.record().value('v2')) != '' and forceString(query.record().value('v2')) != ' ' and forceString(query.record().value('v2')) != ' ':
         
                cons[forceString(query.record().value('actionId'))]['PR_CONS'] =  (forceString(query.record().value('v2'))).split('.')[0]
            if (forceDate(query.record().value('v3'))).toString(Qt.ISODate):
                cons[forceString(query.record().value('actionId'))]['DT_CONS'] =  (forceDate(query.record().value('v3'))).toString(Qt.ISODate)
        for key, el in  cons.items():
            if el != {}:
                self.writeStartElement('CONS')
                if 'PR_CONS' in el.keys():
                    self.writeTextElement('PR_CONS', el['PR_CONS'])
                if 'DT_CONS' in el.keys():
                    self.writeTextElement('DT_CONS', el['DT_CONS'])
                self.writeEndElement() #CONS
            
    def getSchema(self, eventId):
        str = u"(ActionType.code LIKE 'sh%' or ActionType.code LIKE 'it%' or ActionType.code LIKE 'rb%' or ActionType.code LIKE 'mt%' or ActionType.code LIKE 'pn%')"
        stmt = """SELECT `ActionType`.code as cCode, `Action`.note as note
                    FROM `Action`
                    LEFT JOIN `ActionType` ON `Action`.`actionType_id` = `ActionType`.`id`
                    WHERE `Action`.`event_id`=%d AND `Action`.note =1 AND
                            %s AND 
                            `Action`.`deleted` =0""" %(eventId, str)
                            
        
        stmt1 = """SELECT `ActionProperty_String`.value as cCode
                     FROM `Action`
                     LEFT JOIN `ActionType` ON `Action`.`actionType_id` = `ActionType`.`id`
                     LEFT JOIN ActionProperty ON ActionProperty.action_id = Action.id
                     LEFT JOIN ActionPropertyType ON ActionProperty.type_id = ActionPropertyType.id
                     LEFT JOIN ActionProperty_String ON ActionProperty_String.id =  ActionProperty.id
                     WHERE `Action`.`event_id`=%d AND ActionPropertyType.shortName = 'CRIT'
                             AND  `Action`.`deleted` =0""" %(eventId)
        query =  QtGui.qApp.db.query(stmt)
        query1 =  QtGui.qApp.db.query(stmt1)
        mass = []
     #   query1 =  QtGui.qApp.db.query(stmt1)
        while query.next():
            mass.append(forceString(query.record().value('cCode')))
        while query1.next():
            mass.append(forceString(query1.record().value('cCode')).split('.')[0])

        return mass
    
    def getHospitalBedProfile(self, hospitalActionId):
        action = CAction.getActionById(hospitalActionId)
        bedId = forceRef(action[u'койка'])
    
        if bedId:
            bedProfileId = self.getHospitalBedProfileId(bedId)
            if bedProfileId:
                exportId = forceString(QtGui.qApp.db.translate('rbAccountingSystem', 'code', 'V020', 'id'))
                stmt = """SELECT `rbHospitalBedProfile_Identification`.value as code
                        FROM `rbHospitalBedProfile_Identification`
                        WHERE `rbHospitalBedProfile_Identification`.`system_id`=%s AND 
                                rbHospitalBedProfile_Identification.master_id = %s""" %(exportId, bedProfileId)
                query =  QtGui.qApp.db.query(stmt)
                while query.next():
                    if forceString(query.record().value('code')):
                        return (forceString(query.record().value('code')))
            else:
                pass
    
    def getOperationCode(self, eventId):
        stmt = """SELECT `rbService`.infis as operationCode
                    FROM `Action`
                    LEFT JOIN `ActionType` ON `Action`.`actionType_id` = `ActionType`.`id`
                    LEFT JOIN `rbService` ON `rbService`.`id` = `ActionType`.nomenclativeService_id
                    lEFT JOIN Event ON Event.id = Action.event_id
                    LEFT JOIN EventType On EventType.id = Event.eventType_id
                    LEFT JOIN mes.MES on mes.MES.id = Event.MES_id
                    WHERE `Action`.`event_id`=%d AND 
                            ActionType.serviceType = 4 AND 
                            `Action`.`deleted` !=1 AND `Action`.note ='1' and mes.MES.active =1""" %(eventId)
                            
        stmt2 = """SELECT `rbService`.infis as operationCode
                    FROM `Action`
                    LEFT JOIN `ActionType` ON `Action`.`actionType_id` = `ActionType`.`id`
                    LEFT JOIN `rbService` ON `rbService`.`id` = `ActionType`.nomenclativeService_id
                    lEFT JOIN Event ON Event.id = Action.event_id
                    LEFT JOIN mes.MES on mes.MES.id = Event.MES_id
                    WHERE `Action`.`event_id`=%d AND 
                            ActionType.serviceType = 4 AND 
        
                            `Action`.`deleted` != 1  and mes.MES.active =1""" %(eventId)
                            

                            
        
        query =  QtGui.qApp.db.query(stmt)
        query2 =  QtGui.qApp.db.query(stmt2)
     #   query1 =  QtGui.qApp.db.query(stmt1)
      #  query3 =  QtGui.qApp.db.query(stmt3)
        while query.next():
            if forceString(query.record().value('operationCode')):
                return (forceString(query.record().value('operationCode')))
        while query2.next():
            if forceString(query2.record().value('operationCode')):
                return (forceString(query2.record().value('operationCode')))
        else:
            return None
        
    def getOperationService(self, serviceId):
        db = QtGui.qApp.db
        stmt = """SELECT `rbService`.code FROM `rbService_Contents` 
                LEFT JOIN `rbService` ON `rbService`.`id` = `rbService_Contents`.`service_id`
        
                  WHERE `rbService_Contents`.`master_id` = %s
              --    GROUP BY `Account_Item`.`event_id`"""
        query = db.query(stmt % serviceId)
        if query.next():
            record = query.record()
            return forceString(record.value(0))
        else:
            return None

    def getNumberKSG(self, eventId):
        stmt = """SELECT mes.`MES`.descr as cCode
                    FROM `Event`
                    LEFT JOIN mes.`MES` ON `MES`.`id` = `Event`.`MES_id`
                    WHERE `Event`.id = %d""" %(eventId)
        query =  QtGui.qApp.db.query(stmt)
        while query.next():
            if forceString(query.record().value('cCode')):
                return (forceString(query.record().value('cCode')))


    def writeBenefits(self, clientId, eventId):
            codes = Export29XMLCommon.getBenefitsType(self, clientId)
            osses = Export29XMLCommon.getOss(self, eventId, "'med.abort', 'protivoprav'")
            trombs = Export29XMLCommon.getOss(self, eventId, "'TLIZ'")
            if codes != [] or  osses != [] or trombs != []:
                self.writeStartElement('DSVED')
                for oss in osses:
                    self.writeTextElement('OSS', forceString(oss))
                for code in codes:
                    self.writeTextElement('LGOTA', forceString(code))
                    
                for tr in trombs:
                    self.writeTextElement('TLIZ', forceString(tr))
                self.writeEndElement() # DSVED

    def writeFileHeader(self,  device, fileName, accNumber, accDate, year, 
                         month, miacCode, payerCode, accSum, aAmount, contractBegDate):
        self.recNum = 1
        self.caseNum = 1
        self._lastClientId = None
        self.serviceNum = 1
        self.setDevice(device)
        self.writeStartDocument()
        self.writeStartElement('ZL_LIST')
        self.writeHeader(fileName, accNumber, accDate, year, month, 
                         miacCode, payerCode, accSum, aAmount, contractBegDate)


    def writeHeader(self, fileName, accNumber, accDate, year, month, 
                    miacCode, payerCode, accSum, aAmount, contractBegDate):
        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', '3.2.0' if contractBegDate < QDate(2021, 12, 31) else '3.2.1')
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
            self.writeTextElement('NSCHET',  forceString(accNumber)[:15])
            self.writeTextElement('DSCHET', accDate.toString(Qt.ISODate))
            if payerCode != '29':
                self.writeTextElement('PLAT', payerCode[:5], writeEmtpyTag = False)
#TODO: MOVE IT BACK!
#Примечание. Чтобы быстро изменить итоговую сумму придется пойти на этот быдлокод
#Затем мы все заменим на хранимки
#P.S. хранимка требует дебага. Да, я dummy и мне стыдно
#однако сейчас СРОЧНО необходимо, чтобы общая сумма где-то считалась
            self.writeTextElement('SUMMAV', 'dummy')
#            self.writeTextElement('SUMMAV', 'dummy')
            self.writeTextElement('IFIN', '', writeEmtpyTag = True)
            self.writeEndElement()


    def writeTextElement(self, element,  value, writeEmtpyTag = False):
        if not writeEmtpyTag and (not value or value == ''):
            return
        QXmlStreamWriter.writeTextElement(self, element, value)

    def writeFileFooter(self):
        self.writeTextElement('COMENTSL', self.ossString)
        self.writeBenefits(self._lastClientId, self._lastEventId)
        
        if self.summ > 0:
            self.writeTextElement('IDSP',self.medicalAidKind)
            self.writeTextElement('SUMV',('%10.2f' % round(self.summ,2)).strip())
        self.writeEndElement() # SLUCH
        self.writeEndElement() # root
        self.writeEndDocument()


    
    def getDent(self, id):
        db = QtGui.qApp.db
        stmt = """SELECT ActionType.code as code
                    FROM `Action`
                    LEFT JOIN ActionType On ActionType.id = actionType_id
                      WHERE eventCSG_id = %s AND flatCode = 'surf' and Action.deleted =0
                  """
        query = db.query(stmt % str(id))
        dent = {}
        while query.next():
            record = query.record()
            dent_num = None
            surf = ''
            if record:
                if forceString(record.value('code')).find("-") >0:
                    dent_num, surf = forceString(record.value('code')).split("-")
                    dent_num = dent_num.split(".")[2]
                else:
                    dent_num = forceString(record.value('code')).split(".")[2]
            if dent_num in dent.keys():
                dent[dent_num].append(surf)
            else:
                dent[dent_num] = [surf]
        return dent


    
    def getDateForStationary(self, preEventId):
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
    

    def getProfile(self, serviceId, personId):
        key = (serviceId, personId)
        result1 = None
        result2 = None
        result3 = None
#            if serviceId == None or personId == None:
#                print "Shit happens"

        stmt = """SELECT rbMedicalAidProfile.regionalCode, rbMedicalAidKind.code, rbMedicalAidType.regionalCode
            FROM rbService_Profile
            LEFT JOIN rbSpeciality ON rbSpeciality.id = rbService_Profile.speciality_id
            LEFT JOIN Person ON Person.speciality_id = rbSpeciality.id
            LEFT JOIN rbMedicalAidProfile ON rbService_Profile.medicalAidProfile_id = rbMedicalAidProfile.id
            LEFT JOIN rbMedicalAidType ON rbService_Profile.medicalAidType_id = rbMedicalAidType.id
            LEFT JOIN rbMedicalAidKind ON rbService_Profile.medicalAidKind_id = rbMedicalAidKind.id
            WHERE rbService_Profile.master_id = %s AND Person.id = %s
            """ % (serviceId, personId)
            
        stmt2 = """SELECT rbMedicalAidProfile.regionalCode, rbMedicalAidKind.code, rbMedicalAidType.regionalCode
                FROM rbService
            LEFT JOIN rbMedicalAidProfile ON rbService.medicalAidProfile_id = rbMedicalAidProfile.id
            LEFT JOIN rbMedicalAidType ON rbService.medicalAidType_id = rbMedicalAidType.id
            LEFT JOIN rbMedicalAidKind ON rbService.medicalAidKind_id = rbMedicalAidKind.id
            WHERE rbService.id = %s 
            """ % (serviceId)

        query = QtGui.qApp.db.query(stmt)
        query2 = QtGui.qApp.db.query(stmt2)
        if query and query.first():
                record = query.record()

                if record:
                    result1 = forceString(record.value(0))
                    result2 = forceString(record.value(1))
                    result3 = forceString(record.value(2))
                    
        else:
            if query2 and query2.first():
                record = query2.record()

                if record:
                    result1 = forceString(record.value(0))
                    result2 = forceString(record.value(1))
                    result3 = forceString(record.value(2))

        self.medicalAidProfileCache[key] = result1
        self.medicalAidKindCache[key] = result2
        self.medicalAidTypeCache[key] = result3

        return result1, result2, result3












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


    def writeRecord(self, record,  contractBegDate, log):

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
        #Пол пациента.
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
                log(u'Ошибка: В регистрационной карточке новорожденного пациента %d не указан представитель' % clientId, True)
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
        
        if forceInt(record.value('documentFederalCode')) != 4:
                self.writeTextElement('DOCTYPE',  forceString(record.value('documentFederalCode')))
                self.writeTextElement('DOCSER', documentSerial)
                self.writeTextElement('DOCNUM', forceString(record.value('documentNumber')))
                if contractBegDate > QDate(2019, 10, 31):
                    self.writeTextElement('DOCDATE', (forceDate(record.value('documentDate'))).toString(Qt.ISODate))
                    self.writeTextElement('DOCORG', forceString(record.value('documentOrg')))
  

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
        personalAccount = forceString(db.translate('Organisation_Account', 'id', accId , 'personalAccount'))
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
        self.writeTextElement('LIC_SCH',  personalAccount)
        self.writeTextElement('ADDR_J',  forceString(record.value('Address')))
        self.writeEndElement()
            
    def writeHeader(self, fileName, accDate):
        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', '1.1' if accDate < QDate(2022, 2, 1) else '1.2')

        self.writeEndElement()

    def writeFileFooter(self):
        self.writeEndElement() # root
        self.writeEndDocument()