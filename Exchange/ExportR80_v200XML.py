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
from zipfile import ZIP_DEFLATED, ZipFile


from PyQt4 import QtGui
from PyQt4.QtCore import Qt, SIGNAL, pyqtSignature, QDate, QDir, QFile, QTextCodec, QXmlStreamWriter

from library.Utils import forceBool, forceDate, forceDouble, forceInt, forceRef, forceString, forceStringEx, formatSNILS, toVariant, trim

from Accounting.Tariff import CTariff
from Events.Action import CAction
from Exchange.Export import CExportHelperMixin

from Export29XMLCommon import Export29XMLCommon
from Export29XMLCommon import SummSingleton


from Ui_ExportR29XMLPage1 import Ui_ExportPage1
from Ui_ExportR29XMLPage2 import Ui_ExportPage2

serviceInfoExportVersion = '1.0'
container = SummSingleton()

#TODO: remove this logic as fast as u can!
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
        amount = forceRef(accountRecord.value('amount'))
    else:
        date = exposeDate = contractId = payerId = aDate =  None
        number = '0'
        amount= 0
    return date, number, exposeDate, contractId,  payerId,  aDate, amount


def exportR80_v200(widget, accountId, accountItemIdList):
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
        date, number, exposeDate, contractId, payerId,  aDate, aAmount= getAccountInfo(accountId)
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
        stmt = """SELECT Organisation.smoCode FROM Contract
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

            payerCode = '80'
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
        return os.path.join(self.getTmpDir(), u'L%s' % #os.path.basename(self.getFullXmlFileName())[1:])
                            os.path.basename(self.getFullXmlFileName())[1:] if os.path.basename(self.getFullXmlFileName())[:2] != 'CM' else 'L%s' % os.path.basename(self.getFullXmlFileName()))
#     def getFullXmlAccFileName(self):
#         return os.path.join(self.getTmpDir(), u'S%s' % os.path.basename(self.getFullXmlFileName())[1:])

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
        self.flagBuffer = 0
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
  #      output, clientOutput, accountOut = self.createXML()
        output, clientOutput= self.createXML()
        self.progressBar.reset()
        self.progressBar.setMaximum(1)
        self.progressBar.setValue(0)
        self.progressBar.setText(u'Запрос в БД...')
        QtGui.qApp.processEvents()
        query = self.createQuery()
        self.progressBar.setMaximum(max(query.size(), 1))
        self.progressBar.reset()
        self.progressBar.setValue(0)
        return output, query,  clientOutput #, accountOut


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
                Account_Item.amount AS amount,
                IF(Contract_Tariff.federalLimitation = 0,
                            Account_Item.amount,
                            LEAST(Contract_Tariff.federalLimitation, Account_Item.amount)) * Contract_Tariff.federalPrice AS federalSum,
                IF((Contract_Tariff.tariffType = %d or (rbEventService.code like '2.5%%' or rbEventService.code like '2.6%%' or rbEventService.code like '2.4%%') or
(rbVisitService.code like '2.5%%' or rbVisitService.code like '2.6%%' or rbVisitService.code like '2.4%%') or
(rbItemService.code like '2.5%%' or rbItemService.code like '2.6%%' or rbItemService.code like '2.4%%')), 1,  IF(Contract_Tariff.regionalLimitation = 0,
                            Account_Item.amount,
                            LEAST(Contract_Tariff.regionalLimitation, Account_Item.amount))) * Contract_Tariff.regionalPrice AS regionalSum,
                            """ % CTariff.ttEventByMESLen

        stmt = """SELECT Account_Item.id AS accountItemId,
                Account_Item.event_id  AS event_id,
                Account_Item.visit_id as visit_id,
                Account_Item.action_id as action_id,
                Account_Item.service_id,
                Event.client_id        AS client_id,
                EventType.service_id AS EventServiceId,
                EventType.name as EventTypeName,
                Event.externalId AS eventExternalId,
                Contract_Tariff.uet as ContractTariffUet,
                Client.lastName,
                Client.firstName,
                Client.patrName,
                Client.birthDate       AS birthDate,
                Client.sex AS sex,
                `Client`.`SNILS` AS SNILS,
                Client.birthPlace AS birthPlace,
                age(Client.birthDate, Event.execDate) as clientAge,
                CONCAT(ClientPolicy.serial, ' ', ClientPolicy.number) AS policySN,
                ClientDocument.serial  AS documentSerial,
                ClientDocument.number  AS documentNumber,
                ClientDocument.date AS documentDate,
                ClientDocument.origin,
                ClientDocument.documentType_id AS clientDocTypeId,
                rbDocumentType.regionalCode AS documentRegionalCode,
                rbDocumentType.federalCode AS documentFederalCode,
                rbDocumentType.code AS documentTypeCode,
          --      IF(work.title IS NOT NULL,
          --          work.title, ClientWork.freeInput) AS `workName`,
                IF(Account_Item.visit_id IS NOT NULL, Visit.person_id,
                    IF(Account_Item.action_id IS NOT NULL,
                        IF(Action.person_id IS NOT NULL, Action.person_id, Action.setPerson_id), Event.execPerson_id)
                ) AS execPersonId,
                Diagnostic.TNMS          AS TNMS,
                Diagnosis.MKB          AS MKB,
                rbDiseaseCharacter_Identification.value as diseaseCharacter,
             --   rbTraumaType.code    AS traumaCode,
                Event.eventType_id    AS eventTypeId,
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
                CONCAT(CONCAT_WS('-',SUBSTRING(Person.`SNILS`, 1, 3), SUBSTRING(Person.`SNILS`, 4, 3), SUBSTRING(Person.`SNILS`, 7, 3)), ' ', SUBSTRING(Person.`SNILS`, 10, 2)) AS personSNILS,
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
                    rbItemServiceGroup.regionalCode,
                    IF(Account_Item.visit_id IS NOT NULL, rbVisitServiceGroup.regionalCode, rbEventServiceGroup.regionalCode)
                    ) AS serviceGroupCode,

                AccDiagnosis.MKB AS AccMKB,
                CompDiagnosis.MKB AS CompMKB,
                PreDiagnosis.MKB AS PreMKB,
                rbEventProfile.regionalCode AS eventProfileRegCode,
                rbEventProfile.code AS eventProfileCode,
                OrgStructure.infisCode AS orgStructureCode,
                rbMedicalAidUnit.federalCode AS medicalAidUnitFederalCode,
                rbEventTypePurpose.code AS eventTypePurposeCode,
                rbEventTypePurpose.regionalCode AS eventTypePurpose,
                rbEventTypePurpose.federalCode AS eventTypePurposeFederalCode,
                Event.`order`,
                Event.id AS eventId,
                EventType.regionalCode as eventTypeRegionalCode,
                EventResult.federalCode AS eventResultFederalCode,
                EventResult.regionalCode AS eventResultRegionalCode,
                RelegateOrg.miacCode AS relegateOrgMiac,
                Event.srcDate AS directionDate,
                rbTariffCategory.federalCode AS tariffCategoryFederalCode,
                EventType.code AS eventTypeCode,
                Action.begDate AS begDateAction,
                Action.endDate AS endDateAction,
                Account_Item.master_id As accountId,
                Account_Item.usedCoefficients as usedCoefficients,
                OrgStructure_Identification.value as lpu1Str,
                `rbDispanser`.observed as dispanserStatus,
                rbDiseaseStage.code  as diagStage,
                HospitalAction.id AS hospitalActionId
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
                            (ClientPolicy.endDate is NULL or ClientPolicy.endDate >= Event.setDate or ClientPolicy.endDate='0000-00-00')
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
  --          LEFT JOIN ClientAddress ClientRegAddress ON ClientRegAddress.client_id = Client.id AND
  --                    ClientRegAddress.id = (SELECT MAX(CRA.id)
 --                                        FROM   ClientAddress AS CRA
  --                                       WHERE  CRA.type = 0 AND CRA.client_id = Client.id AND CRA.deleted=0)
   --         LEFT JOIN Address   RegAddress ON RegAddress.id = ClientRegAddress.address_id
  --          LEFT JOIN AddressHouse RegAddressHouse ON RegAddressHouse.id = RegAddress.house_id
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
            LEFT JOIN rbDiseaseStage ON rbDiseaseStage.id = Diagnostic.`stage_id`
      --      LEFT JOIN ClientWork ON ClientWork.client_id=Event.client_id AND
      --                  ClientWork.id = (SELECT max(CW.id)
      --                                   FROM ClientWork AS CW
       --                                  WHERE CW.client_id=Client.id AND CW.deleted=0)
       --     LEFT JOIN Organisation AS work ON work.id=ClientWork.org_id AND work.deleted = 0
            LEFT JOIN Organisation AS RelegateOrg ON Event.relegateOrg_id = RelegateOrg.id
            LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
       --     LEFT JOIN rbTraumaType ON rbTraumaType.id = Diagnosis.traumaType_id
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
            LEFT JOIN OrgStructure_Identification ON OrgStructure_Identification.master_id = OrgStructure.id 
            AND OrgStructure_Identification.system_id IN (SELECT id from rbAccountingSystem where code like 'nao')
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
            AND %s ORDER BY Client.id, Event.id, Event.execDate,  Account_Item.id DESC""" % (sumStr, cond)

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

    #    out, query, clientsFile, accountFile = self.prepareToExport()
        out, query, clientsFile = self.prepareToExport()
        accDate, accNumber, exposeDate, contractId,  payerId, aDate, aAmount =\
            getAccountInfo(self.parent.accountId)

        contractBegDate = forceDate(QtGui.qApp.db.translate(
            'Contract', 'id', contractId , 'begDate'))
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
      #      accountOut = CAccountDataStreamWriter(self)
            out.setCodec(QTextCodec.codecForName('cp1251'))
            clientsOut.setCodec(QTextCodec.codecForName('cp1251'))
       #     accountOut.setCodec(QTextCodec.codecForName('cp1251'))
            miacCode = forceString(QtGui.qApp.db.translate(
                'Organisation', 'id', QtGui.qApp.currentOrgId(), 'smoCode'))
            comm = forceDouble(QtGui.qApp.db.translate(
                'Account', 'id', self.parent.accountId, '    note'))
#TODO: Переделать хранимку updateAccount
            accSum = forceDouble(QtGui.qApp.db.translate(
                'Account', 'id', self.parent.accountId, 'sum'))
            out.writeFileHeader(file, self.parent.getFullXmlFileName(), accNumber, aDate,
                                forceString(accDate.year()),
                                forceString(accDate.month()),
                                miacCode, payerCode, accSum, aAmount, comm)
            clientsOut.writeFileHeader(clientsFile, self.parent.getFullXmlFileName(), aDate)
        #    accountOut.writeFileHeader(accountFile, self.parent.getFullXmlFileName(), aDate)
            eventsInfo = self.getEventsSummaryPrice()
            while query.next():
                QtGui.qApp.processEvents()
                if self.aborted:
                    break
                self.progressBar.step()
                out.writeRecord(query.record(), miacCode, eventsInfo, self.parent.accountId, contractBegDate, self.log, self.parent.getFullXmlFileName())
                clientsOut.writeRecord(query.record(), contractBegDate, self.log)
      #      accountOut.writeRecord(contractId, payerId, accDate, accNumber, self.parent.getFullXmlFileName(), forceString(accDate.year()), forceString(accDate.month()), accSum, self.log)
            out.writeFileFooter(query.record())
            clientsOut.writeFileFooter()
       #     accountOut.writeFileFooter()
            file.close()
            clientsFile.close()
        #    accountFile.close()
            fout = open(self.parent.getFullXmlFileName()+'_out', 'a')
            count = 1
            self.progressBar.setValue(0)
            for line in open(self.parent.getFullXmlFileName(), "r"):
                if str(line).find('<SUMV>') != -1:
                    fout.write(str(line).replace('<SUMV>'+str(count)+'</SUMV>',
                                                '<SUMV>'
                                                +
                                                 #   ('%10.2f' % container.dictSums[count]).strip()
                                                # +
                                                '</SUMV>'))
                    count +=1
                    self.progressBar.step()
                elif str(line).find('<SUMMAV>dummy</SUMMAV>') != -1:
                    fout.write(str(line).replace('<SUMMAV>dummy</SUMMAV>',
                                               '<SUMMAV>'
                                                +
                                               #     str('%15.2f' % container.summTotal).strip()
                                               # +
                                                '</SUMMAV>'))
                    self.progressBar.step()
                else:
                    fout.write(line)
                    self.progressBar.step()

            fout.close()

            os.remove(self.parent.getFullXmlFileName())
            os.rename(self.parent.getFullXmlFileName()+'_out', self.parent.getFullXmlFileName())
#           

            container.summTotal = 0
            container.dictSums = {1 : 0.0}
            container.date = {1: (2000, 1, 1)}

        else:
            self.log(u'Нечего выгружать.')
            self.progressBar.step()


# *****************************************************************************************

    def createXML(self):
        outFile = QFile(self.parent.getFullXmlFileName())
        outFile.open(QFile.WriteOnly | QFile.Text)
        outFile2 = QFile( self.parent.getFullXmlPersFileName())
        outFile2.open(QFile.WriteOnly | QFile.Text)
#         outFile3 = QFile( self.parent.getFullXmlAccFileName())
#         outFile3.open(QFile.WriteOnly | QFile.Text)
        return outFile, outFile2#, outFile3


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
        self.summ = 0
        self.dateNum = 1
        self.ossString = ''
        self.eventTypeCode = ''
        self.medicalUnit = ''
        self._lastClientId = None
        self._lastEventId = None
        self._lastActionId = None
        self._emergencyCase = None
        self.medicalAidProfileCache = {}
        self.medicalAidKindCache = {}
        self.medicalAidTypeCache = {}
        self.rbPostFederalCache= {}
        self.rbPostRegionalCache = {}
        self.buffer = 0
        


    def getStandartServiceIds(self):
        stmt = u"SELECT id FROM rbService WHERE name LIKE 'стандарт%медицинской%помощи%'"
        query = QtGui.qApp.db.query(stmt)
        while query.next():
            yield forceInt(query.record().value('id'))

    def writeRecord(self, record, miacCode, eventsInfo, accountId, contractBegDate, log, fileName):
        #Если есть более одного движения, и текущий action в строке не последний, то просто выкидываемся из метода
        hospitalDayAmount = 0


        eventId = forceInt(record.value('event_id'))
       # if self.visitAmount <1:
        visitAmount = (self.getVisitsAmount(eventId))
        if self.visitAmount <1:
            self.visitAmount = visitAmount
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
        begDate = forceDate(record.value('begDateEvent'))
        self.parent.endDate=begDate 
        if record.value('endDateEvent'): endDate = forceDate(record.value('endDateEvent'))
        else:
            endDate = forceDate(Export29XMLCommon.getLatestDateOfVisitOrAction(QtGui.qApp.db, accountId, eventId))
        self.parent.endDate=endDate 
#         federalPrice = forceDouble(record.value('federalPrice'))
#         regionalPrice = forceDouble(record.value('regionalPrice'))
#         federalSum = Export29XMLCommon.doubleToStrRounded(forceDouble(record.value('federalSum')))
#         regionalSum = Export29XMLCommon.doubleToStrRounded(forceDouble(record.value('regionalSum')))
        personId = forceRef(record.value('execPersonId'))
        profile, kindStr, typeStr  = self.getProfile(forceRef(record.value('serviceId')), personId)
        profileStr = (profile if profile else forceString(record.value('medicalAidProfileFederalCode')))[:3]
        amount = forceDouble(record.value('amount'))
        oss = u''
        self.eventTypeCode  = forceString(record.value('eventTypeCode'))
        if not self.medicalUnit:
            self.medicalUnit = forceString(record.value('medicalAidUnitFederalCode'))
        
#         if self._lastClientId != clientId: # новая запись, иначе - новый случай
#             if self._lastClientId:
#                 self.recNum += 1
#                 self.writeTextElement('COMENTSL', self.ossString)
# #                 if forceString(record.value('eventTypeCode')) == "011_80":
# #                     if self.medicalUnit == '29':
# #                         self.writeTextElement('CEL_POS', forceString(2))
# #                         self.writeTextElement('ST_ONKO', forceString(record.value('diagStage'))[1:] if  forceString(record.value('diagStage'))[1:] else '0') 
# #                     elif self.medicalUnit == '30':
# #                         self.writeTextElement('CEL_POS', forceString(1))
# #                         self.writeTextElement('ST_ONKO', forceString(record.value('diagStage'))[1:] if  forceString(record.value('diagStage'))[1:] else '0') 
#                 self.writeEndElement() # SLUCH
#                 self.writeEndElement() # ZAP
#                 self._lastEventId = None
        self._lastClientId = clientId
        if self._lastEventId != eventId:# and self._emergencyCase == None:
      #      self.visitAmount  = visitAmount
            self.recNum += 1
            
            if self._lastEventId:

                    self.writeTextElement('COMENTSL', self.ossString)
                    self.writeEndElement() # SLUCH
                    self.writeEndElement() # ZAP
            self.writeStartElement('ZAP')

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
            if docCode and  docCode > 1:
                oss += u'ОСС=2,'

#            smo = forceString(record.value('insurerMiac'))[:5]
#Паспорт - ClientDocument ClientDocumentType (паспорт РФ)
#Ориентируемся на ___номер полиса___ и страховую компанию SMO
            if ((not npolis) and (not smo) and (docCode == 1)): #предъявил только паспорт
                oss += u'ОСС=1,'
            if not vpolis:
                log(u'В регистрационной карте пациента %d не указан вид полиса' % clientId, True)
            if not vpolis and not spolis and not npolis:
                log(u'В регистрационной карте пациента %d нет действующего полиса на начало обращения' % clientId, True)
            self.writeTextElement('VPOLIS', vpolis)

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
            
            if '0003' in Export29XMLCommon.getSpecialCaseCode(QtGui.qApp.db, clientId, begDate):
                self.childrenNumber = 1
                self.writeTextElement('NOVOR', '%s%s%s' % (forceString(record.value('sex'))[:1], birthDate.toString('ddMMyy'), self.childrenNumber ))
            elif '0009' in Export29XMLCommon.getSpecialCaseCode(QtGui.qApp.db, clientId, begDate):
                 self.writeTextElement('NOVOR', '%s%s%s' % (forceString(record.value('sex'))[:1], birthDate.toString('ddMMyy'), self.childrenNumber ))
                 self.childrenNumber = self.childrenNumber + 1
            else:
                self.writeTextElement('NOVOR', '0')

            self.writeEndElement() # PACIENT
        serviceId = forceRef(record.value('serviceId'))
        
        serviceStr = self.getServiceInfis(serviceId)
        serviceNote = (forceString(QtGui.qApp.db.translate(QtGui.qApp.db.table('rbService'), 'id', forceRef(record.value('serviceId')), 'note')).split(";"))
        if forceDouble(record.value('sum')) > 0:
                self.summ = Export29XMLCommon.doubleToStrRounded(forceDouble(record.value('sum')))
        
        if self.eventTypeCode == "011_80":
            if forceDouble(record.value('sum')) > 0:
                self.summ = Export29XMLCommon.doubleToStrRounded(forceDouble(record.value('sum')))
            if visitAmount > 1: #visitAmount > 1:
                if 'isSecondService' in serviceNote:
                    if self.visitAmount  == visitAmount:
                        self.flagBuffer = 2
                    else:
                        self.flagBuffer = 3
                else: 
                    self.flagBuffer =0
            else:
                self.flagBuffer = 1
        else: 
            self.flagBuffer = 1
        self.visitAmount  = self.visitAmount  -1
        
                        

        serviceGroupCode = forceString(record.value('serviceGroupCode'))
        eventTypeCode = forceString(record.value('eventTypeCode'))

        personSNILS = forceString(record.value('personSNILS'))
        visitId = forceInt(record.value('visit_id'))
        if forceInt(record.value('ContractTariffType')) == CTariff.ttEventAsCoupleVisits:
            personSNILS = Export29XMLCommon.getPersonRegionalCodeForConsultVisit(QtGui.qApp.db, visitId)
        self.medicalUnit  = forceString(record.value('medicalAidUnitFederalCode'))
        self._lastEventId = eventId
        self._lastActionId = actionId
        
        if self.flagBuffer in (1, 2):
            self.writeStartElement('Z_SL')
            self.writeTextElement('IDCASE', '%d' % self.caseNum)
            self.writeTextElement('USL_OK',  forceString(record.value('medicalAidTypeCode') if not typeStr else  typeStr))
            self.writeTextElement('VIDPOM', forceString(record.value('medicalAidKindCode') if not kindStr else kindStr))
            forPom = Export29XMLCommon.getHelpForm(QtGui.qApp.db, eventId, forceString(record.value('order')))
            self.writeTextElement('FOR_POM', forceString(forPom))
            self.writeTextElement('NPR_MO', forceString(record.value('relegateOrgMiac')),  writeEmtpyTag = False)
            self.writeTextElement('NPR_DATE', (forceDate(record.value('directionDate'))).toString(Qt.ISODate))

            lpu1Str = forceString(record.value('lpu1Str')) #Export29XMLCommon.getMobileModule(QtGui.qApp.db, forceDouble(miacCode)) if eventTypeCode[:2] == '04' else ''
            self.writeTextElement('LPU', miacCode[:6])
            
         #   self.writeTextElement('VBR', '0')
            if not begDate:
                 log(u'Пациент %d не указана дата начала события' % clientId, True)
            else:
                self.writeTextElement('DATE_Z_1', begDate.toString(Qt.ISODate))
            if not endDate:
                log(u'Пациент %d не указана дата окончкания события' % clientId, True)
            else:
                self.writeTextElement('DATE_Z_2', endDate.toString(Qt.ISODate))
            if self.eventTypeCode not in ("011_80", '013_80'):
                self.writeTextElement('KD_Z', forceString(self.getHospitalDaysAmount(eventId)))
            self.writeTextElement('RSLT', forceString(record.value('eventResultFederalCode')))
            self.writeTextElement('ISHOD', forceString(record.value('resultFederalCode'))) 
            if Export29XMLCommon.getSpecialCaseCode(QtGui.qApp.db, clientId, begDate) == '0003':
                self.writeTextElement('OS_SLUCH', '1')
            transferName = Export29XMLCommon.getTransferName(QtGui.qApp.db, eventId)
            if transferName == 4:
                self.writeTextElement('P_PER', ('1'))
            ot = forceString(record.value('patrName'))
            if ot == u'нет' or ot == u'Нет' :
                self.writeTextElement('OS_SLUCH', '2')
                
            self.writeStartElement('SL')
            self.writeTextElement('SL_ID', '%d' % self.sluchNum)
            self.writeTextElement('LPU_1', lpu1Str, writeEmtpyTag = False) #У Т(6) Подразделение МО Подразделение МО лечения из регионального справочника
            self.writeTextElement('PODR', forceString(record.value('orgStructureCode')))
            self.writeTextElement('PROFIL', profileStr)
            hospitalActionId = forceRef(record.value('hospitalActionId'))
            if hospitalActionId:
                bedProfile= self.getHospitalBedProfile(hospitalActionId)
                self.writeTextElement('PROFIL_K', bedProfile)
            self.writeTextElement('DET', (u'1' if age < 18 else u'0'))
            if self.eventTypeCode  in ("011_80", '013_80'):
                if self.medicalUnit == '29':
                    self.writeTextElement('P_CEL', forceString(1.0))
                elif self.medicalUnit in ('28'):
#                    self.writeTextElement('P_CEL', forceString(30)) таня подправила
                     self.writeTextElement('P_CEL', forceString(3.0))
                elif self.medicalUnit in ('30'):
                    self.writeTextElement('P_CEL', forceString(3.0))
    
            self.writeTextElement('NHISTORY', ('%s' % eventId)[:50])
            
            if transferName:
                    self.writeTextElement('P_PER', ('%s' % transferName ))
            if not begDate:
                 log(u'Пациент %d не указана дата начала события' % clientId, True)
            else:
                self.writeTextElement('DATE_1', begDate.toString(Qt.ISODate))
            if not endDate:
                log(u'Пациент %d не указана дата окончкания события' % clientId, True)
            else:
                self.writeTextElement('DATE_2', endDate.toString(Qt.ISODate))
            if self.eventTypeCode not in ("011_80", '013_80'):
                self.writeTextElement('KD', forceString(self.getHospitalDaysAmount(eventId)))
            self.writeTextElement('DS0', forceString(record.value('PreMKB')))
            self.writeTextElement('DS1',forceString(record.value('MKB')))
     #       if self.medicalUnit == '29':
     #           self.writeTextElement('PR_D_N', forceString(record.value('dispanserStatus')))
            self.writeTextElement('DS2', forceString(record.value('AccMKB')))
            self.writeTextElement('DS3', forceString(record.value('CompMKB')))
            self.writeTextElement('C_ZAB', forceString(record.value('diseaseCharacter')))
         #   if forceString(record.value('dispanserStatus')) != '0' and 'isPossibleDispanObserve' in self.serviceNote and flagOncology != 0 and self.isOncology ==1:
          #  self.writeTextElement('DS_ONK','1')
           #     flagOncology1 = 1
            flagOncology1 = Export29XMLCommon.isOncology(QtGui.qApp.db, eventId)
            if os.path.splitext(os.path.basename(fileName))[0][:1] != 'C':
                flagOncology1 ='2'
 #           if self.eventTypeCode not in ('013_80') and flagOncology1 in [0, '1']:
            if  flagOncology1 in [0, '1']:
                self.writeTextElement('DS_ONK', flagOncology1 if flagOncology1 else '0')
            if self.medicalUnit in ('29', '30'):       
                self.writeTextElement('DN', forceString(record.value('dispanserStatus')))      
            if self.eventTypeCode not in ("011_80", '013_80') :
                if forceString(record.value('usedCoefficients')) !='':
                    com = json.loads(forceString(record.value('usedCoefficients')))
                    coefTarif = {}
                    koef = ['KZ', 'KUP', 'KU', 'KD']
                    if '1' in com.keys():
                        for k in com['1']:
                            val = com['1'][k]
                            if k not in koef:
                                coefTarif[k[:2]]= val
                            else:
                                coefTarif[k] = val
                    if '0' in com.keys():    
                        com = com['0']
                        all = com[u'__all__']
                else:
                    st = dict()
                    st['__all__'] = 1
                    com['0'] = st
                    all = 0
            if self.eventTypeCode not in ('013_80'):
                self.writeTextElement('CODE_MES1', serviceStr)
            TNMS = forceString(record.value('TNMS'))
            TNMS = '' if (TNMS == '' or TNMS ==u'cTx cNx cMx cSx pTx pNx pMx pSx') else self.getPhaseId(TNMS, forceString(record.value('MKB')), contractBegDate)
            TNMS1 = TNMS
         #   TNMS = '' if (TNMS == '' or TNMS ==u'cTx cNx cMx cSx pTx pNx pMx pSx') else self.getPhaseId(TNMS, forceString(record.value('MKB')))
            if flagOncology1 == 0:
           # if ((flagOncology1 == 0 and 'isPossibleDispanObserve' not in self.serviceNote) or 
                 #   (forceString(record.value('dispanserStatus')) == '0' and 'isPossibleDispanObserve' in self.serviceNote and flagOncology1 == 0)):
                self.writeCons(eventId)
                schema = self.getSchema( eventId)
                (MKB, resultFederalCode, traumaCode, AccMKB, CompMKB, 
                 PreMKB, TNMS, characterDiag, flagOncology1, onk, dispanserStatus) =  Export29XMLCommon.getDiagnosis(self,
                                                                                                   eventId, 
                                                                                                   personId, 
                                                                                                   forceRef(record.value('eventExecPersonId')),
                                                                                                   contractBegDate)
                Export29XMLCommon.writeOncology1(self,eventId, TNMS, TNMS1, schema,  0, onk)
               # self.writeOncology1(self,eventId, TNMS, TNMS1, schema,  0)
                
            if flagOncology1 == 1:
                self.writeDirection(eventId)
          #      schema = self.getSchema( eventId)
          #      self.writeTextElement('CODE_MES2', schema)
            
            
            if self.eventTypeCode not in ("011_80", '013_80') : 
                self.writeStartElement('KSG_KPG')
                self.writeTextElement('N_KSG', serviceStr )
                self.writeTextElement('VER_KSG',  '2020')
                self.writeTextElement('KSG_PG', '0')
                self.writeTextElement('KOEF_Z', forceString(coefTarif['KZ'[:2]]))
                self.writeTextElement('KOEF_UP', forceString(coefTarif['KUP']))
                self.writeTextElement('BZTSZ', forceString(( '%10.2f' % round(Export29XMLCommon.doubleToStrRounded(forceDouble(record.value('price'))), 2)).strip()))
                self.writeTextElement('KOEF_D', forceString( coefTarif['KD']))
                self.writeTextElement('KOEF_U', forceString(coefTarif['KU']))
                
                schema = self.getSchema( eventId)
                for sch in schema:
                    self.writeTextElement('CRIT', sch)
             #   if len(schema) > 0:
             #       self.writeTextElement('CRIT', schema[0])

              #  if len(schema) > 1:
              #      self.writeTextElement('CRIT', schema[1])
                    
                if '__all__' in com.keys():
                    self.writeTextElement('SL_K', '1' if com != [] else '0')
                    self.writeTextElement('IT_SL', ('%6.2f' % all).strip() )
                    for item, coeff in com.items():
                            if item != '__all__':
                                self.writeStartElement('SL_KOEF')
                                self.writeTextElement('IDSL', forceString(item))
                                self.writeTextElement('Z_SL', ('%6.2f' % coeff).strip() )
                                self.writeEndElement() #SL_KOEF
                 #   self.writeEndElement()
                else:
                    self.writeTextElement('SL_K', '0')
                    
                self.writeEndElement() # KSG_KPG
                
                
            self.writeTextElement('REAB', '')
            self.writeTextElement('PRVS', forceString(self.parent.getPersonSpecialityFederalCode(personId)))
          #  personCode = forceString(self.getPersonSpecialityUsishCode(personId))
           # self.writeTextElement('PRVS', personCode)
          #  if not personCode:
          #      log(u'Не указан исполнитель визита/мероприятия в событии %d у пациента %d' % (eventId, clientId), True)
#            self.writeTextElement('PRVS', forceString(self.parent.getPersonSpecialityFederalCode(personId)))
            self.writeTextElement('VERS_SPEC', u'V021')
            self.writeTextElement('IDDOKT', personSNILS)
            self.writeTextElement('ED_COL', ('%6.2f' % amount).strip())
            self.writeTextElement('TARIF', ('%10.2f' % round(Export29XMLCommon.doubleToStrRounded(forceDouble(record.value('price'))), 2)).strip())
            self.writeTextElement('SUM_M',('%10.2f' % round(Export29XMLCommon.doubleToStrRounded(forceDouble(record.value('sum'))), 2)).strip())

            self.sluchNum+= 1

            birthDate = forceDate(record.value('birthDate'))

            (totalAmount,  totalSum) = eventsInfo[eventId]
            container.dictSums[self.caseNum] = 0.0
            self.caseNum+= 1
        
        serviceId = forceRef(record.value('serviceId'))
        serviceStr = self.getServiceInfis(serviceId)
        serviceGroupCode = forceString(record.value('serviceGroupCode'))
        serviceId = forceRef(record.value('serviceId'))
        lpu1Str = forceString(record.value('lpu1Str')) #Export29XMLCommon.getMobileModule(QtGui.qApp.db, forceDouble(miacCode)) if eventTypeCode == '04' else ''
        price = forceDouble(record.value('price'))
        (totalAmount,  totalSum) = eventsInfo[eventId]
        composition, totalpercents = self.getContractCompositionInfo(forceString(record.value('contractTariffId')))
        summm = Export29XMLCommon.doubleToStrRounded(forceDouble(record.value('sum')))

        ContractTariffType = forceInt(record.value('ContractTariffType'))
        schema = self.getSchema(eventId)
        if ContractTariffType == CTariff.ttEventByMESLen:
            if self.getOperationCode(forceInt(record.value('event_id'))):
                serviceStr = self.getOperationCode(forceInt(record.value('event_id'))) 
          #  elif len(schema) > 0:
          #      serviceStr = schema[0]
            else:
               serviceStr = None                 
        if serviceStr:
            self.writeServices(record, log, miacCode, age, profileStr,
                                serviceStr, serviceGroupCode, price, amount, 
                                summm, latestMoveFlag, lpu1Str, personId, serviceId,
                                 eventId,  contractBegDate, None, composition,forceInt(record.value('visit_id')))
        com = dict()
        telemed = self.getTelemed(eventId)

     
        if self.eventTypeCode not in ("011_80", '013_80'):
              #  schema = self.getSchema( eventId)
              #  self.writeTextElement('KSG_DOP', schema)
          #      self.writeTextElement('ST_ONKO', forceString(record.value('diagStage'))[1:] if  forceString(record.value('diagStage'))[1:] else '0') 
                self.writeTextElement('CRIM', '0')
                self.writeTextElement('TELEMED', telemed)
              #  self.writeTextElement('IDSP', forceString(record.value('medicalAidUnitFederalCode')))
              #  self.writeTextElement('SUMV',  ('%10.2f' % round(Export29XMLCommon.doubleToStrRounded(forceDouble(record.value('sum'))), 2)).strip())
    #         oss = forceString(QString(oss[:-1]))
        if  self.eventTypeCode  in ('013_80'):
             self.writeTextElement('CEL_POS', forceString(30))
             self.writeTextElement('CRIM', '0')
             self.writeTextElement('TELEMED', telemed)
    #         self.ossString = oss
        if self.flagBuffer in (0,1):
            if self.eventTypeCode == "011_80":
                
                if self.getVisitsAmount(eventId) == 1:
                    self.writeTextElement('CEL_POS', forceString(17))
                else:
                    self.writeTextElement('CEL_POS', forceString(1))
            #   self.writeTextElement('ST_ONKO', forceString(record.value('diagStage'))[1:] if  forceString(record.value('diagStage'))[1:] else '0') 
                self.writeTextElement('CRIM', '0')
                self.writeTextElement('TELEMED', telemed)

                
            self.writeEndElement() #SL
            if self.eventTypeCode == "011_80":
                if self.getVisitsAmount(eventId) == 1:
                    self.writeTextElement('IDSP', forceString(record.value('medicalAidUnitFederalCode')))
                else:
                    self.writeTextElement('IDSP', '30')
            else:
                self.writeTextElement('IDSP', forceString(record.value('medicalAidUnitFederalCode')))
            self.writeTextElement('SUMV',  ('%10.2f' % round(Export29XMLCommon.doubleToStrRounded(self.summ), 2)).strip())
                                           


    def writeServices(self, record, log, miacCode, age, profileStr, serviceStr, serviceGroupCode, price, amount,
                      summ, latestMoveFlag, lpu1Str, personId,  serviceId, eventId, contractBegDate, hasVirtual=None, composition= None, visitId = None):

        self.writeService(record,
                          log,
                          miacCode,
                          age,
                          profileStr,
                          serviceStr,
                          price,
                          amount,
                          summ,
                          contractBegDate,
                          latestMoveFlag,
                          lpu1Str,
                          personId,
                          visitId)




    def writeService(self, record, log, miacCode, age, profileStr, serviceStr, price, amount,
                     summ, contractBegDate, multiplyMovementLogicFlag,  lpu1Str='', personId = '', visitId = '',
                     compCode = None):
        ContractTariffType = forceInt(record.value('ContractTariffType'))
        self.writeStartElement('USL')
        self.writeTextElement('IDSERV',  ('%8d' % self.serviceNum).strip()) # O N(8) номер записи в реестре услуг
        self.writeTextElement('LPU', miacCode[:6]) #O Т(6) Код МО МО лечения
        self.writeTextElement('LPU_1', lpu1Str, writeEmtpyTag = False) #У Т(6) Подразделение МО Подразделение МО лечения из регионального справочника
        self.writeTextElement('PODR', forceString(record.value('orgStructureCode')), writeEmtpyTag = False) #У N(8) Код отделения Отделение МО лечения из регионального справочника
        self.writeTextElement('PROFIL', profileStr) #O N(3) Профиль Классификатор V002

        if ContractTariffType == CTariff.ttEventByMESLen:
            operationCode = self.getOperationCode(forceInt(record.value('event_id')))
            self.writeTextElement('VID_VME', operationCode)

        self.writeTextElement('DET', (u'1' if age < 18 else u'0')) #О N(1) Признак детского профиля 0-нет, 1-да.

        dateIn = None
        dateOut = None
        db = QtGui.qApp.db

        dateIn = forceDate(record.value('begDateEvent'))
        dateOut = forceDate(record.value('endDateEvent'))
        if not profileStr and Export29XMLCommon.isRegionalAdditionalPay(db, serviceStr) == False:
            log(u'Ошибка: у услуги %s не указан профиль Справочники-Финансовые-Услуги(Профили оплаты)' %serviceStr, True)
#        if forceInt(record.value('visit_id')):
#            dateIn = dateOut = self.getDateForVisits(forceInt(record.value('visit_id')))

        if (Export29XMLCommon.isRegionalAdditionalPay(db, serviceStr) == True):
            dateIn = forceDate(record.value('begDateEvent'))
            dateOut = forceDate(record.value('endDateEvent'))

        if forceInt(record.value('action_id')):
               dateIn = forceDate(db.translate('Action', 'id',  forceString(record.value('action_id')), 'begDate'))
               dateOut = forceDate(db.translate('Action', 'id', forceString(record.value('action_id')), 'endDate'))
#             (dateIn, dateOut) = Export29XMLCommon.getDatesForAction(db,
#                                                                     forceInt(record.value('event_id')),
#                                                                     forceInt(record.value('action_id')),
#                                                                     serviceStr)
        elif (visitId and visitId != 0):
            dateIn = dateOut = self.getDateForVisits(visitId)

        if not dateIn and not dateOut:
            dateIn  = forceDate(record.value('dateVisit'))
            dateOut = forceDate(record.value('dateVisit'))


        self.writeTextElement('DATE_IN', dateIn.toString(Qt.ISODate)) #O D Дата начала оказания услуги
        self.writeTextElement('DATE_OUT', dateOut.toString(Qt.ISODate)) #O D Дата окончания оказания услуги
        code = forceString(QtGui.qApp.db.translate('Person', 'id', personId, 'code'))
        if not dateOut:
            log(u'Ошибка: Врач %s - В событии %d у пациента %d не указан дата окончания визита/мероприятия' % (code, forceInt(record.value('eventId')), forceInt(record.value('client_id'))), True)
        self.writeTextElement('DS', forceString(record.value('MKB'))) #O Т(10) Диагноз Код из справочника МКБ до уровня подрубрики
        if not forceString(record.value('MKB')):
            log(u'Ошибка: Врач %s - В событии %d у пациента %d не указан диагноз' % (code, forceInt(record.value('eventId')), forceInt(record.value('client_id'))), True)
        if len(forceString(record.value('MKB')))<4 and Export29XMLCommon.diagnosisHasSpecification(db, forceString(record.value('MKB'))) == True:
            log(u'Ошибка: Врач %s - В событии %d у пациента %d у диагноза не указана подрубрика' % (code, forceInt(record.value('eventId')), forceInt(record.value('client_id'))), True)
        if (serviceStr.lower().find('a16') != -1):
            pass

        if not compCode:
         #   if forceString(record.value('eventTypeCode'))!= '011_80' :
     #            operationCode = self.getOperationCode(forceInt(record.value('event_id')))
     #            self.writeTextElement('CODE_USL', operationCode)
     #       else:
                self.writeTextElement('CODE_USL', serviceStr) #O Т(16) Код услуги Территориальный классификатор услуг
       
        else:
                self.writeTextElement('CODE_USL', compCode)

        self.writeTextElement('KOL_USL', ('%6.2f' % 1).strip() ) #O N(6.2) Количество услуг (кратность услуги)

        self.writeTextElement('TARIF', ('%15.2f' % 0).strip()) #O N(15.2) Тариф
        
        self.writeTextElement('SUMV_USL', ('%15.2f' % 0).strip()) #O N(15.2) Стоимость медицинской услуги, выставленная к оплате (руб.)
        

        
        if visitId == 1 or visitId== 0: visitId = None
        personId, codeMd = Export29XMLCommon.getPcode(db, record, visitId)

        if not personId:
            log(u'Ошибка:  В событии %d у пациента %d не указан исполнитель визита/мероприятия' % (forceInt(record.value('eventId')), forceInt(record.value('client_id'))), True)
        else:
            self.writeTextElement('PRVS', forceString(self.parent.getPersonSpecialityFederalCode(personId)))
         #   self.writeTextElement('PRVS', forceString(self.getPersonSpecialityUsishCode(personId)))
        if not codeMd and personId:
            code = forceString(QtGui.qApp.db.translate('Person', 'id', personId, 'code'))
            log(u'Ошибка: В регистрационной карточке сотрудника (Код: %s) не указан СНИЛС - Справочники-Персонал-Сотрудники-Вкладка "Личные"- поле "СНИЛС" \n'%(code), True)
        self.writeTextElement('CODE_MD', forceString(record.value('personSNILS')))
        serviceNote = (forceString(QtGui.qApp.db.translate(QtGui.qApp.db.table('rbService'), 'id', forceRef(record.value('serviceId')), 'note')).split(";"))
        TNMS = forceString(record.value('TNMS'))
        TNMS = '' if (TNMS == '' or TNMS ==u'cTНет cNНет cMНет cSНет pTx pNx pMx pSx' or TNMS ==u'cTx cNx cMx cSx pTx pNx pMx pSx') else self.getPhaseId(TNMS, forceString(record.value('MKB')), contractBegDate)
      #  if (forceString(record.value('eventTypeCode'))== '011_80' and  'isSecondService' not in serviceNote) or forceString(record.value('eventTypeCode'))!= '011_80':
      #      self.writeOncology1(forceInt(record.value('eventId')), TNMS, TNMS1, 1)            
        if 'isIncompleteCase' in serviceNote:
            self.writeTextElement('NPL', forceString(Export29XMLCommon.getIncompleteReason(QtGui.qApp.db, forceInt(record.value('eventId')))))
        self.writeEndElement() #USL
        self.serviceNum += 1
        
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
            if forceString(query.record().value('v2')) != '' and forceString(query.record().value('v2')) != ' ':
         
                cons[forceString(query.record().value('actionId'))]['PR_CONS'] =  (forceString(query.record().value('v2'))).split('.')[0]
            if (forceDate(query.record().value('v3'))).toString(Qt.ISODate):
                cons[forceString(query.record().value('actionId'))]['DT_CONS'] =  (forceDate(query.record().value('v3'))).toString(Qt.ISODate)
        for key, el in  cons.items():
        
            self.writeStartElement('CONS')
            if 'PR_CONS' in el.keys():
                self.writeTextElement('PR_CONS', el['PR_CONS'])
            if 'DT_CONS' in el.keys():
                self.writeTextElement('DT_CONS', el['DT_CONS'])
            self.writeEndElement() #CONS
        

        
    def writeDirection(self, eventId):
        str1 = u"Да"
        stmt3 = """select a1.begDate as directionDate, at2.code as code,  at1.flatCode as serviceCode
                    from Action as a1
                     left join ActionType at1 on at1.id=a1.actionType_id 
                     left join ActionPropertyType on ActionPropertyType.actionType_id=at1.id 
                     left join ActionProperty on ActionProperty.action_id=a1.id 
                     left join ActionProperty_String on ActionProperty_String.id=ActionProperty.id 
                     left join Action a2 on a1.prevAction_id=a2.id 
                     left join ActionType at2 on at2.id=a2.actionType_id 
                     where at1.flatCode in ('consultationDirection', 'inspectionDirection') and 
                     ActionPropertyType.descr like  'DS_ONK'
                     and ActionProperty.action_id=a1.id and ActionProperty_String.value='%s' and a1.event_id = %s"""%( str1, eventId)
        
        stmt = """select a1.begDate as directionDate, at2.code as code,  at1.flatCode as serviceCode, ActionProperty_String.value as value
                    from Action as a1
                     left join ActionType at1 on at1.id=a1.actionType_id 
                     left join ActionPropertyType on ActionPropertyType.actionType_id=at1.id 
                     left join ActionProperty on ActionProperty.action_id=a1.id 
                     left join ActionProperty_String on ActionProperty_String.id=ActionProperty.id 
                     left join Action a2 on a1.prevAction_id=a2.id 
                     left join ActionType at2 on at2.id=a2.actionType_id 
                     where at1.flatCode in ('inspectionDirection') and 
                     ActionPropertyType.descr like  'NAZ_V'
                     and ActionProperty.action_id=a1.id  and a1.event_id = %s"""%(eventId)

                  
        query = QtGui.qApp.db.query(stmt3)  
        query1 = QtGui.qApp.db.query(stmt)
        while query.next():
            date = forceDate(query.record().value('directionDate'))
            code = forceString(query.record().value('serviceCode'))
            self.writeStartElement('NAPR')
            self.writeTextElement('NAPR_DATE', date.toString(Qt.ISODate))
            
            if code == 'consultationDirection':
                self.writeTextElement('NAPR_V', '1')
            elif code == 'inspectionDirection':
                if query1.next():
                    type = forceString(query.record().value('value'))
                    serviceCode = forceString(query.record().value('code'))
                    if type[:1] == '5':
                        self.writeTextElement('NAPR_V', '2')
                    else:
                        self.writeTextElement('NAPR_V', '3')
                        self.writeTextElement('MET_ISSL', type[:1])
                        self.writeTextElement('NAPR_USL', serviceCode)
            self.writeEndElement() #NAPR     


    def writeFileHeader(self,  device, fileName, accNumber, accDate, year, month, miacCode, payerCode, accSum, aAmount, comm):
        self.recNum = 0
        self.caseNum = 1
        self.sluchNum = 1
        self.flagBuffer =1
        self.visitAmount = 0
        self._lastClientId = None
        self.serviceNum = 1
        self.setDevice(device)
        self.writeStartDocument()
        self.writeStartElement('ZL_LIST')
        self.writeHeader(fileName, accNumber, accDate, year, month, miacCode, payerCode, accSum, aAmount, comm)


    def writeHeader(self, fileName, accNumber, accDate, year, month, miacCode, payerCode, accSum, aAmount,  comm):
        self.writeStartElement('ZGLV')
#        if accDate < QDate(2018, 09, 29):
        self.writeTextElement('VERSION',  '3.1.1')
        self.writeTextElement('DATA', accDate.toString(Qt.ISODate))
        (fname,  ext) = os.path.splitext(os.path.basename(fileName))
        self.writeTextElement('FILENAME', fname[:26])
        self.writeTextElement('SD_Z', forceString(aAmount))
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
            self.writeTextElement('SUMMAV',('%10.2f' % round(accSum,2)).strip())
            self.writeTextElement('COMENTS',  forceString(comm))
#            self.writeTextElement('SUMMAV', 'dummy')
            self.writeEndElement()


    def writeTextElement(self, element,  value, writeEmtpyTag = False):
        if not writeEmtpyTag and (not value or value == ''):
            return
        QXmlStreamWriter.writeTextElement(self, element, value)

    def writeFileFooter(self, record):
        self.writeTextElement('COMENTSL', self.ossString)
#         if self.eventTypeCode == "011_80":
#             if self.medicalUnit == '29':
#                 self.writeTextElement('CEL_POS', forceString(2))
#                 self.writeTextElement('ST_ONKO', forceString(record.value('diagStage'))[1:] if  forceString(record.value('diagStage'))[1:] else '0') 
#             elif self.medicalUnit == '30':
#                 self.writeTextElement('CEL_POS', forceString(1))
#                 self.writeTextElement('ST_ONKO', forceString(record.value('diagStage'))[1:] if  forceString(record.value('diagStage'))[1:] else '0') 
           # self.writeTextElement('CEL_POS', forceString(1))
        self.writeEndElement() # SLUCH
        self.writeEndElement() # root
        self.writeEndDocument()
        
    def getTelemed(self, eventId):
        stmt = """SELECT `ActionProperty_String`.value AS str
                            FROM  `ActionProperty_String`
                            lEFT JOIN ActionProperty ON ActionProperty.id = `ActionProperty_String`.id
                            LEFT JOIN ActionPropertyType ON ActionPropertyType.id = type_id
                            LEFT JOIN `Action` ON    ActionProperty.action_id =  Action.id
                            LEFT JOIN  `ActionType` ON `Action`.`ActionType_id` =  `ActionType`.`id` 
                            WHERE  `ActionType`.`flatCode` IN ('tele_concult',
'tele_medecine') AND ActionPropertyType.descr = "TELEMED"
                            AND  `Action`.`event_id` =%d
                            AND Action.deleted !=1""" %(eventId)
        query =  QtGui.qApp.db.query(stmt)
        if query.next():
            code = (forceString(query.record().value('str'))).split('.')[0]
            return code
        else:
            return '0'
        

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
    
    def getPhaseId(self, TNMS, MKB, contractBegDate):
        # cTНет cNНет cMНет cSНет pTx pNx pMx pSx
        a = ''
        translate = {'cS':'rbTNMphase', 'cT':'rbTumor', 'cN':'rbNodus', 'cM':'rbMetastasis', 'pS':'rbTNMphase', 'pT':'rbTumor', 'pN':'rbNodus', 'pM':'rbMetastasis'}
   #     TNMS = TNMS.replace(u'MМ', u'М')
        TNMS = TNMS.replace(u'pTx pNx pMx pSx', u'')
        TNMS = TNMS.replace(u'cTx cNx cMx cSx ', u'')
        TNMS = TNMS.replace(u'pT pN pM pS', u'')
        TNMS = TNMS.replace(u'cT cN cM cS ', u'')
        for s in TNMS.split(' '):
            if s != '':
                t =s[0:2] 
                a =  s[1:] if s[0:2] !='cS' and s[0:2] !='pS' else s[2:] #s.split(t)[1]

                if s[0:2] == 'cT':
                    pass
                if s.split(t)[1] == u'Нет':
                    a = u'Нет'
         #       if s[-1:] != 'x':
                phase =a
                if s[0:2] in translate.keys():
                    pass
                    table = QtGui.qApp.db.table(translate[s[0:2]])
                    tableIdentification = QtGui.qApp.db.table(translate[s[0:2]] + '_Identification')
                    tableSystem = QtGui.qApp.db.table('`rbAccountingSystem`')
                    table = table.leftJoin(tableIdentification, tableIdentification['master_id'].eq(table['id']))
                    table = table.leftJoin(tableSystem, tableSystem['id'].eq(tableIdentification['system_id']))
    #                addCondLike(cond, table['MKB'], MKB)
                    cond = [ table['MKB'].eq(MKB), table['code'].eq(a)]
                    cond.append( table['endDate'].lt(contractBegDate))
                    cond.append(tableSystem['code'].eq(translate[s[0:2]][2:]))
                    
                    stmt = QtGui.qApp.db.selectStmt(table, ['value'], where=cond)
                    MKB1 = MKB.split('.')[0]
                    query = QtGui.qApp.db.query(stmt)
                    cond.append(table['MKB'].eq(MKB1) )
                    cond.append(table['code'].eq(a))
                    stmt1 = QtGui.qApp.db.selectStmt(table, ['value'], where=cond)
                    query1 = QtGui.qApp.db.query(stmt1)
                    if query.next():
                        phase =  forceString(query.record().value('value'))
                    elif query1.next():
                        phase =  forceString(query1.record().value('value'))
                    if s[1:] != phase:
                        TNMS = TNMS.replace(s, t+phase)
        return TNMS


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


    def getPersonPostFederalCode(self, personId, serviceStr):
        result = self.rbPostFederalCache.get(personId, -1)
        if personId:
            if result == -1:
                if serviceStr[:2] != '17':
                    stmt = """SELECT rbPost.federalCode
                        FROM Person
                        LEFT JOIN rbPost ON rbPost.id = Person.post_id
                        WHERE Person.id = %d""" % personId
                else:
                    stmt = """SELECT rbPost.regionalCode
                        FROM Person
                        LEFT JOIN rbPost ON rbPost.id = Person.post_id
                        WHERE Person.id = %d""" % personId
    
                query = QtGui.qApp.db.query(stmt)
    
                if query and query.first():
                    record = query.record()
    
                    if record:
                        result = forceString(record.value(0))
    
                self.rbPostFederalCache[personId] = result
        return result


    def getPersonPostRegionalCode(self, personId):
        result = self.rbPostRegionalCache.get(personId, -1)

        if result == -1:
            stmt = """SELECT rbPost.regionalCode
                FROM Person
                LEFT JOIN rbPost ON rbPost.id = Person.post_id
                WHERE Person.id = %d""" % personId

            query = QtGui.qApp.db.query(stmt)

            if query and query.first():
                record = query.record()

                if record:
                    result = forceString(record.value(0))

            self.rbPostRegionalCache[personId] = result
        return result


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
            WHERE rbService_Profile.master_id = %d AND Person.id = %d
            """ % (serviceId, personId)

        query = QtGui.qApp.db.query(stmt)

        if query and query.first():
                record = query.record()

                if record:
                    result1 = forceString(record.value(0))
                    result2 = forceString(record.value(1))
                    result3 = forceString(record.value(2))

        self.medicalAidProfileCache[key] = result1
        self.medicalAidKindCache[key] = result2
        self.medicalAidTypeCache[key] = result3

        return result1, result2, result3

    def getVisits(self, eventId, serviceId, serviceStr = None):
        if serviceStr:
            if serviceStr[:4] == '2.26' or serviceStr[:4] == '2.28':
                stmt = """SELECT  `Visit`.`id` AS visitId
                        FROM  `Visit`
                        WHERE  `Visit`.`event_id` =%d AND Visit.deleted !=1
                        """%(eventId)
            elif serviceStr.startswith('3.7.') or serviceStr.startswith('3.38.'):
                stmt = """SELECT  `Visit`.`id` AS visitId
                        FROM  `Visit`
                        LEFT JOIN rbVisitType ON rbVisitType.id = Visit.visitType_id
                        WHERE  `Visit`.`event_id` =%d AND rbVisitType.regionalCode = 1 AND Visit.deleted !=1
                        """%(eventId)
        else:
        
                    stmt = """SELECT  `Visit`.`id` AS visitId
                        FROM  `Visit`
                        WHERE  `Visit`.`event_id` =%d AND Visit.service_id =%d AND Visit.deleted !=1
                        """%(eventId, serviceId)

        query = QtGui.qApp.db.query(stmt)
        if query:
            visits = []
            while query.next():
                visits.append(forceInt(query.record().value('visitId')))
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
        
    def getTransferName(self, eventId):
        stmt = """SELECT `ActionProperty_String`.value AS str
                            FROM  `ActionProperty_String`
                            lEFT JOIN ActionProperty ON ActionProperty.id = `ActionProperty_String`.id
                            LEFT JOIN ActionPropertyType ON ActionPropertyType.id = type_id
                            LEFT JOIN `Action` ON    ActionProperty.action_id =  Action.id
                            LEFT JOIN  `ActionType` ON `Action`.`ActionType_id` =  `ActionType`.`id` 
                            WHERE  `ActionType`.`flatCode` =  "received" AND ActionPropertyType.descr = "perevod"
                            AND  `Action`.`event_id` =%d
                            AND Action.deleted !=1""" %(eventId)
        query =  QtGui.qApp.db.query(stmt)
        if query.next():
            code = (forceString(query.record().value('str'))).split('.')[0]
            return code
        else:
            return 1

    def getHospitalDaysAmount(self, eventId):
        stmt = """SELECT SUM(  `Action`.`amount` ) AS amountHD
                            FROM  `Action`
                            LEFT JOIN  `ActionType` ON (  `Action`.`ActionType_id` =  `ActionType`.`id` )
                            WHERE  `ActionType`.`flatCode` =  "moving"
                            AND  `Action`.`event_id` =%d
                            AND Action.deleted !=1""" %(eventId)
        query =  QtGui.qApp.db.query(stmt)
        if query.next():
            return (forceInt(query.record().value('amountHD')))
        else:
            return None
        
    def isOneDay(self, eventId):
        stmt = """SELECT  Action.`begDate` ,  Action.`endDate` 
                    FROM  `Action` 
                    LEFT JOIN  `ActionType` ON (  `Action`.`ActionType_id` =  `ActionType`.`id` ) 
                    WHERE  `ActionType`.`flatCode` =  "moving"
                    AND  `Action`.`event_id` =%d
                    AND Action.deleted !=1"""%(eventId) 
        query =  QtGui.qApp.db.query(stmt)
        flag = False
        while query.next():
            begDate = (forceDate(query.record().value('begDate')))
            endDate = (forceDate(query.record().value('endDate')))
            if begDate == endDate:
                flag = True
        return flag 

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
        
    def getHospitalBedProfile(self, hospitalActionId):
        action = CAction.getActionById(hospitalActionId)
        bedId = forceRef(action[u'койка'])
    
        if bedId:
            bedProfileId = self.getHospitalBedProfileId(bedId)
            exportId = forceString(QtGui.qApp.db.translate('rbAccountingSystem', 'code', 'V020', 'id'))
            stmt = """SELECT `rbHospitalBedProfile_Identification`.value as code
                    FROM `rbHospitalBedProfile_Identification`
                    WHERE `rbHospitalBedProfile_Identification`.`system_id`=%s AND 
                            rbHospitalBedProfile_Identification.master_id = %s""" %(exportId, bedProfileId)
            query =  QtGui.qApp.db.query(stmt)
            while query.next():
                if forceString(query.record().value('code')):
                    return (forceString(query.record().value('code')))
            return None
    
    def getSchema(self, eventId):
        str = u"(ActionType.code LIKE 'sh%' or ActionType.code LIKE 'it%' or ActionType.code LIKE 'rb%' or ActionType.code LIKE 'mt%')"
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
        #    if forceString(query.record().value('cCode')):
        #        return (forceString(query.record().value('cCode')))
#         while query1.next():
#             if forceString(query1.record().value('cCode')):
#                 return (forceString(query1.record().value('cCode')))
        return mass

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
        while query.next():
            if forceString(query.record().value('operationCode')):
                return (forceString(query.record().value('operationCode')))
        while query2.next():
            if forceString(query2.record().value('operationCode')):
                return (forceString(query2.record().value('operationCode')))
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
                              2: '2.13.1',
                              4: '2.10.3',
                              5: '2.10.2',
                              6: '2.10.1',
                              8: '2.6.1',
                             }[forceInt(serviceCode[2:3])]
        else:
            serviceStr = {
                          CTariff.ttVisit:                '3.14.1',
                          CTariff.ttEvent:                '1.4.1',
                          CTariff.ttActionAmount:         '4.3.1',
                          CTariff.ttEventAsCoupleVisits:  '2.13.1',
                          CTariff.ttHospitalBedDay:       '1.4.1',
                          CTariff.ttActionUET:            '3.15.1',
                          CTariff.ttHospitalBedService:   '1.3.1',
                          CTariff.ttEventByMES:           '1.7.1',
                          CTariff.ttEventByMESLen:        '1.7.1',
                          CTariff.ttCoupleVisits:         '3.13.1'
                         }[forceInt(record.value('ContractTariffType'))]
        return serviceStr


    def getVirtualCode(self, serviceCode, personId = None):
        serviceStr = {
                      2: '2.20.1',
                      3: lambda: self.getPersonPostFederalCode(personId, serviceCode),
                      4: '2.20.1',
                      5: '2.20.1',
                      6: '2.20.1',
                      7: lambda: self.getPersonPostFederalCode(personId, serviceCode),
                      9: '2.20.1',
                     }[forceInt(serviceCode[2:3])]
        return serviceStr() if callable(serviceStr) else serviceStr


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
        if self.parent.chkClientLog.isChecked():
            log(u'Выгрузка пациента (Код: %s) '%(clientId), True)
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
                if im == u'нет' or im == u'Нет':
                    dostp.append(1)
                else:
                    self.writeTextElement('OT_P', ot)

            #Пол пациента.
                self.writeTextElement('W_P', forceString(sex))
            #Дата рождения пациента.
                self.writeTextElement('DR_P', birthDate.toString(Qt.ISODate))
#            self.writeTextElement('DR_P', birthDate)
                if dostp:
                    for ds in dost:
                        self.writeTextElement('DOST_P', forceString(ds))

        self.writeTextElement('MR', forceString(record.value('birthPlace')), writeEmtpyTag=False)
        # Федеральный код из справочника ТИПЫ ДОКУМЕНТОВ. Из карточки пациента.
        
        if forceInt(record.value('documentFederalCode')) != 4:
                self.writeTextElement('DOCTYPE',  forceString(record.value('documentFederalCode')))
                self.writeTextElement('DOCSER', documentSerial)
                self.writeTextElement('DOCNUM', forceString(record.value('documentNumber')))
  
        # Серия документа, удо-стоверяющего личность пациента.
  #      self.writeTextElement('DOCSER', documentSerial)
        # Номер документа, удостоверяющего личность пациента.
  #      self.writeTextElement('DOCNUM', forceString(record.value('documentNumber')))
        # СНИЛС пациента.
        self.writeTextElement('SNILS', formatSNILS(forceString(record.value('SNILS'))))
        
        # Код места жительства по ОКАТО. Берётся из адреса жительство.
        #self.writeTextElement('OKATOG', okatog)
        # Код места пребывания по ОКАТО. Берётся из ОКАТО организации, чей полис у пациента.
        #self.writeTextElement('OKATOP', forceString(record.value('insurerOKATO')))
        self.writeEndElement() # PERS
        self._clientsSet.add(clientId)


    def writeFileHeader(self,  device, fileName, accDate):
        self._clientsSet = set()
        self.setDevice(device)
        self.writeStartDocument()
        self.writeStartElement('PERS_LIST')
        self.writeHeader(fileName, accDate)


    def writeHeader(self, fileName, accDate):
        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', '3.2')
        self.writeTextElement('DATA', accDate.toString(Qt.ISODate))
        (fname,  ext) = os.path.splitext(os.path.basename(fileName))
        self.writeTextElement('FILENAME', 'L%s' % fname[1:26] if fname[:2] != 'CM' else 'L%s' % fname[0:26])
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
        self.writeStartElement('SCH_DATA')
        self.writeHeader(fileName, accDate)
    
    def writeTextElement(self, element,  value, writeEmtpyTag = False):
        if not writeEmtpyTag and (not value or value == ''):
            return
        QXmlStreamWriter.writeTextElement(self, element, value)
        
    def writeRecord(self, contractId, payerId, accDate, accNumber, fileName, year, month, accSum, log):
        db = QtGui.qApp.db
        table = db.table('Organisation')
        recipientId = forceString(db.translate('Contract', 'id', contractId , 'recipient_id'))
        recordRec = QtGui.qApp.db.getRecordEx(table, '*', table['id'].eq(recipientId))
        
        recordPay = QtGui.qApp.db.getRecordEx(table, '*', table['id'].eq(payerId))
        (fname,  ext) = os.path.splitext(os.path.basename(fileName))
        self.writeStartElement('SCH_DATA')
        self.writeTextElement('NSCHET',  forceString(accNumber)[:15])
        self.writeTextElement('MONTH',  month)
        self.writeTextElement('YEAR', year)
        self.writeTextElement('DSCHET', accDate.toString(Qt.ISODate))
        self.writeTextElement('FILENAME',  forceString(fname))
        self.writeTextElement('SUMMAV', forceString(accSum))
        self.writeTextElement('RUK',  forceString(recordRec.value('chiefFreeInput')))
        self.writeTextElement('BUH',  forceString(recordRec.value('accountant')))
        self.writeEndElement()
        self.writeOgr(db, 'POST', recordRec, 0)
        self.writeOgr(db, 'PLAT', recordPay, 1)
        self.writeOgr(db, 'POL', recordRec, 0)
    
    def writeOgr(self, db, tag, record, flag):
        bankId = forceString(db.translate('Organisation_Account', 'organisation_id', forceString(record.value('id')) , 'bank_id'))
        bankAccount = forceString(db.translate('Organisation_Account', 'organisation_id', forceString(record.value('id')) , 'name'))
        table = db.table('Bank')
        recordBank = QtGui.qApp.db.getRecordEx(table, '*', table['id'].eq(bankId))
        self.writeStartElement(tag)
        self.writeTextElement('NAM_MOP' if flag == 0 else 'NAME',  forceString(record.value('fullName')))
        self.writeTextElement('MCOD' if flag == 0 else 'COD',  forceString(record.value('miacCode')))
        self.writeTextElement('INN',  forceString(record.value('INN')))
        self.writeTextElement('KPP', forceString(record.value('KPP')))
        self.writeTextElement('OKONH', forceString(record.value('OKVED')))
        self.writeTextElement('OKPO', forceString(record.value('OKPO')))
        self.writeTextElement('BANK_NAME', forceString(recordBank.value('name')))
        self.writeTextElement('RASCH_SCH', forceString(bankAccount))
        self.writeTextElement('BIK',  forceString(recordBank.value('BIK')))
        self.writeTextElement('ADDR_J',  forceString(record.value('Address')))
        self.writeEndElement()
            
    def writeHeader(self, fileName, accDate):
        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', '1.0')
      #  self.writeTextElement('DATA', accDate.toString(Qt.ISODate))
        self.writeEndElement()

    def writeFileFooter(self):
        self.writeEndElement() # root
        self.writeEndDocument()
        
