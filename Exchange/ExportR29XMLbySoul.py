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
#TODO:
#для обычных услуг, которые имеют action мы берем даты begDate и endDate (из Action)
#для стационара, где больше 2х движений, берем из таблицы event setDate и execDate
#--
#Для услуг по гемодиализу, профосмотру и лечебно-диагностическая (КАК ОПРЕДЕЛИТЬ?!? - из типа события, вероятно)
# Брать из таблицы VISIT и количество гемодиализа проверить.

import datetime
import os.path
import shutil
from zipfile import ZIP_DEFLATED, ZipFile

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDate, QDir, QFile, QString, QTextCodec, QXmlStreamWriter, pyqtSignature, SIGNAL

from library.Utils import forceBool, forceDate, forceDouble, forceInt, forceRef, forceString, forceStringEx, formatSNILS, toVariant, trim
from Events.ActionServiceType import CActionServiceType

from Exchange.Export29XMLCommon import Export29XMLCommon
from Exchange.Export29XMLCommon import PriceType, SummSingleton
from Exchange.Export import CExportHelperMixin

from Exchange.Ui_ExportR29XMLPage1 import Ui_ExportPage1
from Exchange.Ui_ExportPage2 import Ui_ExportPage2


serviceInfoExportVersion = '1.0'
container = SummSingleton()

#TODO: remove this logic as fast as u can!
def getAccountInfo(accountId):
    db = QtGui.qApp.db
    accountRecord = db.getRecord('Account', 'settleDate, number, exposeDate, contract_id, payer_id, date', accountId)
    if accountRecord:
        date = forceDate(accountRecord.value('settleDate'))
        aDate  = forceDate(accountRecord.value('date'))
        exposeDate = forceDate(accountRecord.value('exposeDate'))
        number = forceString(accountRecord.value('number')).strip()
        contractId = forceRef(accountRecord.value('contract_id'))
        payerId = forceRef(accountRecord.value('payer_id'))
    else:
        date = exposeDate = contractId = payerId = aDate = None
        number = '0'
    return date, number, exposeDate, contractId,  payerId,  aDate


def exportR29XMLbySoul(widget, accountId, accountItemIdList):
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


    def setAccountId(self, accountId):
        self.accountId = accountId
        date, number, exposeDate, contractId, payerId,  aDate = getAccountInfo(accountId)
        strNumber = number if trim(number) else u'б/н'
        strDate = forceString(date) if date else u'б/д'
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
            (date, number, exposeDate, contractId,  payerId,  aDate) = getAccountInfo(self.accountId)

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

            except:
                self.log(str(contractId)+ ", strContractNumber, ")


            lpuInfis  = self.getMiacCode(contractId) #'292301'
            self.xmlFileName = os.path.join(self.getTmpDir(), \
                u'HM%s%s%s_%s%d.xml' % (lpuInfis, infix,  payerCode, date.toString('yyMM'),
                                        self.page1.edtRegistryNumber.value()))
        return self.xmlFileName


    def getFullXmlPersFileName(self):
        return os.path.join(self.getTmpDir(), u'L%s' % os.path.basename(self.getFullXmlFileName())[1:])


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
#        self.chkGroupByService.setChecked(forceBool(QtGui.qApp.preferences.appPrefs.get(
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
        #self.btnExport.setEnabled(not flag)
        #self.chkGroupByService.setEnabled(not flag)
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
        output, clientOutput = self.createXML()
        self.progressBar.reset()
        self.progressBar.setMaximum(1)
        self.progressBar.setValue(0)
        self.progressBar.setText(u'Запрос в БД...')
        QtGui.qApp.processEvents()
        query = self.createQuery()
        self.progressBar.setMaximum(max(query.size(), 1))
        self.progressBar.reset()
        self.progressBar.setValue(0)
        return output, query,  clientOutput


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


# *****************************************************************************************
    #it was added to test SP
    #===========================================================================
    # def runStoredProc(self, accountId):
    #    db = QtGui.qApp.db
    #    tableAccountItem = db.table('Account_Item')
    #    stmt = "SELECT `master_id` AS `mid` from Account_Item WHERE " + tableAccountItem['id'].inlist(accountId)
    #    query = db.query(stmt)
    #    while query.next():
    #        record  = query.record()
    #        id = forceInt(record.value('mid'))
    #        r = QtGui.qApp.db.query('SELECT updateAccountF(%d);' % id).record()
    #        print forceDouble(r.value(0))
    #===========================================================================

    #
    def createQuery(self):
        db = QtGui.qApp.db
        tableAccountItem = db.table('Account_Item')
        cond = tableAccountItem['id'].inlist(self.idList)
#                SUM(Account_Item.amount) AS amount,
        #self.runStoredProc(self.idList)

#TODO: remove this!
#        if (False):
#            pass
#            sumStr = """SUM(Account_Item.`sum`) AS `sum`,
#                SUM(IF(Contract_Tariff.federalLimitation = 0,
#                            Account_Item.amount,
#                            LEAST(Contract_Tariff.federalLimitation, Account_Item.amount)) * Contract_Tariff.federalPrice) AS federalSum,"""
#            cond += ' GROUP BY `Account_Item`.`event_id`, serviceId'
#        else:
        sumStr = """Account_Item.`sum` AS `sum`,
                Account_Item.amount AS amount,
                IF(Contract_Tariff.federalLimitation = 0,
                            Account_Item.amount,
                            LEAST(Contract_Tariff.federalLimitation, Account_Item.amount)) * Contract_Tariff.federalPrice AS federalSum,
                IF((Contract_Tariff.tariffType = 10 or (rbEventService.code like '2.5%' or rbEventService.code like '2.6%' or rbEventService.code like '2.4%') or
(rbVisitService.code like '2.5%' or rbVisitService.code like '2.6%' or rbVisitService.code like '2.4%') or
(rbItemService.code like '2.5%' or rbItemService.code like '2.6%' or rbItemService.code like '2.4%')), 1,  IF(Contract_Tariff.regionalLimitation = 0,
                            Account_Item.amount,
                            LEAST(Contract_Tariff.regionalLimitation, Account_Item.amount))) * Contract_Tariff.regionalPrice AS regionalSum,
                            """

        stmt = """SELECT Account_Item.id AS accountItemId,
                Account_Item.event_id  AS event_id,
                Account_Item.visit_id as visit_id,
                Account_Item.action_id as action_id,
                Account_Item.service_id,
                Event.client_id        AS client_id,
                EventType.service_id AS EventServiceId,
                EventType.name as EventTypeName,
                Contract_Tariff.uet as ContractTariffUet,
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
                ClientDocument.origin,
                ClientDocument.documentType_id AS clientDocTypeId,
                --- ClientRelation.relative_id AS relativeId,
                rbDocumentType.regionalCode AS documentRegionalCode,
                rbDocumentType.federalCode AS documentFederalCode,
                rbDocumentType.code AS documentTypeCode,
                -- RegAddressHouse.number AS number,
                -- RegAddressHouse.corpus AS corpus,
                -- RegAddressHouse.KLADRCode AS regKLADRCode,
                -- RegAddress.flat AS flat,
                -- kladr.KLADR.infis AS placeCode,
                -- kladr.KLADR.OCATD AS placeOKATO,
                -- kladr.KLADR.NAME AS cityName,
                -- kladr.SOCRBASE.infisCode AS streetType,
                -- kladr.STREET.NAME AS streetName,

                IF(work.title IS NOT NULL,
                    work.title, ClientWork.freeInput) AS `workName`,
                IF(Account_Item.visit_id IS NOT NULL, Visit.person_id,
                    IF(Account_Item.action_id IS NOT NULL,
                        IF(Action.person_id IS NOT NULL, Action.person_id, Action.setPerson_id), Event.execPerson_id)
                ) AS execPersonId,
                Diagnosis.MKB          AS MKB,
                rbTraumaType.code    AS traumaCode,
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
                rbDiagnosticResult.federalCode AS resultFederalCode,
                --- rbMedicalAidType.code AS medicalAidTypeCode,
                --- rbMedicalAidKind.code AS medicalAidKindCode,
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
                AccDiagnosis.MKB AS AccMKB,
                rbEventProfile.regionalCode AS eventProfileRegCode,
                rbEventProfile.code AS eventProfileCode,
                OrgStructure.infisCode AS orgStructureCode,
                rbMedicalAidUnit.federalCode AS medicalAidUnitFederalCode,
                -- RegSOCR.infisCODE AS placeTypeCode,
                -- RegRegionKLADR.NAME AS regionName,
                rbEventTypePurpose.regionalCode AS eventTypePurpose,
                rbEventTypePurpose.federalCode AS eventTypePurposeFederalCode,
                Event.`order`,
                Event.id AS eventId,
                EventResult.federalCode AS eventResultFederalCode,
                EventResult.regionalCode AS eventResultRegionalCode,
                RelegateOrg.miacCode AS relegateOrgMiac,
                rbTariffCategory.federalCode AS tariffCategoryFederalCode,
                EventType.code AS eventTypeCode,
                Action.begDate AS begDateAction,
                Action.endDate AS endDateAction
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
            -- LEFT JOIN kladr.STREET ON kladr.STREET.CODE =RegAddressHouse.KLADRStreetCode
            -- LEFT JOIN kladr.KLADR ON kladr.KLADR.CODE = RegAddressHouse.KLADRCode
            -- LEFT JOIN kladr.SOCRBASE ON kladr.SOCRBASE.KOD_T_ST = (SELECT KOD_T_ST
            --            FROM kladr.SOCRBASE AS SB
            --            WHERE SB.SCNAME = kladr.STREET.SOCR
            --            LIMIT 1)
            -- LEFT JOIN kladr.SOCRBASE RegSOCR ON RegSOCR.KOD_T_ST = (SELECT KOD_T_ST
            --            FROM kladr.SOCRBASE AS SB
            --            WHERE SB.SCNAME = kladr.KLADR.SOCR
            --            LIMIT 1)
            -- LEFT JOIN kladr.KLADR RegRegionKLADR ON RegRegionKLADR.CODE = (
            --        SELECT RPAD(LEFT(RegAddressHouse.KLADRCode,5),13,'0') LIMIT 1)
            LEFT JOIN Person  ON Person.id = execPerson_id
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
            LEFT JOIN rbDiseaseCharacter ON Diagnosis.character_id = rbDiseaseCharacter.id
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
            LEFT JOIN OrgStructure ON Person.orgStructure_id = OrgStructure.id
            LEFT JOIN rbMedicalAidUnit ON Account_Item.unit_id = rbMedicalAidUnit.id
            LEFT JOIN Contract_Tariff ON Account_Item.tariff_id = Contract_Tariff.id
            LEFT JOIN rbTariffCategory ON  Contract_Tariff.tariffCategory_id = rbTariffCategory.id
            WHERE
                Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s ORDER BY Client.id, Event.id, Event.execDate""" % (sumStr, cond)

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
#        lpuName = forceString(QtGui.qApp.db.translate('Organisation', 'id', QtGui.qApp.currentOrgId(), 'fullName'))
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

        out, query, clientsFile = self.prepareToExport()
        accDate, accNumber, exposeDate, contractId,  payerId, aDate =\
            getAccountInfo(self.parent.accountId)
#        strAccNumber = accNumber if trim(accNumber) else u'б/н'
#        strContractNumber = forceString(QtGui.qApp.db.translate('Contract', 'id', contractId , 'number')) if contractId else u'б/н'

        payerCode = None
#        payerName = ''

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
                                miacCode, payerCode, accSum)
            clientsOut.writeFileHeader(clientsFile, self.parent.getFullXmlFileName(), aDate)
            eventsInfo = self.getEventsSummaryPrice()
            bufferForConsult =[]
            while query.next():
                QtGui.qApp.processEvents()
                if self.aborted:
                    break
                self.progressBar.step()
                out.writeRecord(query.record(), miacCode, eventsInfo, self.parent.accountId, bufferForConsult)
                while bufferForConsult:
                    out.writeRecord(query.record(), miacCode, eventsInfo, self.parent.accountId, bufferForConsult)
                clientsOut.writeRecord(query.record())

            out.writeFileFooter()
            clientsOut.writeFileFooter()

            file.close()
            clientsFile.close()
            fout = open(self.parent.getFullXmlFileName()+'_out', 'a')
            count = 1
#            countDate = 1
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
#                elif str(line).find('<DATE_1>'+str(countDate)+'</DATE_1>') != -1:
#                    fout.write(str(line).replace('<DATE_1>'+str(countDate)+'</DATE_1>',
#                                                 '<DATE_1>'
#                                                 +
#                                                    (container.date[countDate]).toString(Qt.ISODate)
#                                                 +
#                                                 '</DATE_1>'))
#                    countDate +=1
##                    self.progressBar.step()
 #               elif str(line).find('<DATE_2>'+str(countDate)+'</DATE_2>') != -1:
#                    fout.write(str(line).replace('<DATE_2>'+str(countDate)+'</DATE_2>',
#                                                 '<DATE_2>'
#                                                 +
#                                                    (container.date[countDate]).toString(Qt.ISODate)
#                                                 +
#                                                 '</DATE_2>'))
#                    countDate +=1
#                   self.progressBar.step()
                elif str(line).find('<SUMMAV>dummy</SUMMAV>') != -1:
                    fout.write(str(line).replace('<SUMMAV>dummy</SUMMAV>',
                                                 '<SUMMAV>'
                                                 +
                                                    str('%15.2f' % container.summTotal).strip()
                                                 +
                                                 '</SUMMAV>'))
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

        else:
            self.log(u'Нечего выгружать.')
            self.progressBar.step()


# *****************************************************************************************

    def createXML(self):
        outFile = QFile(self.parent.getFullXmlFileName())
        outFile.open(QFile.WriteOnly | QFile.Text)
        outFile2 = QFile( self.parent.getFullXmlPersFileName())
        outFile2.open(QFile.WriteOnly | QFile.Text)
        return outFile, outFile2


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
        self.dateNum = 1
        self.ossString = ''
        self._lastClientId = None
        self._lastEventId = None

        self.medicalAidProfileCache = {}
        self.rbPostFederalCache= {}
        self.rbPostRegionalCache = {}


    def getStandartServiceIds(self):
        stmt = u"SELECT id FROM rbService WHERE name LIKE 'стандарт%медицинской%помощи%%'"
        query = QtGui.qApp.db.query(stmt)
        while query.next():
            yield forceInt(query.record().value('id'))

    def writeRecord(self, record, miacCode, eventsInfo, accountId, bufferForConsult):
        #Если есть более одного движения, и текущий action в строке не последний, то просто выкидываемся из метода
        hospitalDayAmount = 0
        eventId = forceInt(record.value('event_id'))
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
        if record.value('endDateEvent'): endDate = forceDate(record.value('endDateEvent'))
        else:
            endDate = forceDate(Export29XMLCommon.getLatestDateOfVisitOrAction(QtGui.qApp.db, accountId, eventId))
#        if bufferForConsult:
#            begDate= endDate = forceDate(Export29XMLCommon.getDatesForConsultVisit(QtGui.qApp.db, bufferForConsult))

        federalPrice = forceDouble(record.value('federalPrice'))
        regionalPrice = forceDouble(record.value('regionalPrice'))
        federalSum = Export29XMLCommon.doubleToStrRounded(forceDouble(record.value('federalSum')))
        regionalSum = Export29XMLCommon.doubleToStrRounded(forceDouble(record.value('regionalSum')))
        personId = forceRef(record.value('execPersonId'))
        profile = self.getProfile(forceRef(record.value('serviceId')), personId)
        profileStr = (profile if profile else forceString(record.value('medicalAidProfileFederalCode')))[:3]
        amount = forceDouble(record.value('amount'))
#        amount = self.getAmountByAccId(forceRef(record.value('accountItemId')))

        oss = u''
        if self._lastClientId != clientId: # новая запись, иначе - новый случай
            if self._lastClientId:
                self.recNum += 1
                self.writeTextElement('COMENTSL', self.ossString)
                self.writeEndElement() # SLUCH
                self.writeEndElement() # ZAP
                self._lastEventId = None
            self._lastClientId = clientId
            self.writeStartElement('ZAP')

            self.writeTextElement('N_ZAP', ('%4d' % self.recNum).strip())
#            if ('%4d' % self.recNum).strip() == '2061':
#                pass
            self.writeTextElement('PR_NOV', '0')

            self.writeStartElement('PACIENT')
            self.writeTextElement('ID_PAC',  ('%d' % clientId)[:36])
            # Региональный код справочника ВИДЫ ПОЛИСОВ.
            npolis = forceString(record.value(u'policyNumber'))[:20]
            vpolis = forceString(record.value('policyKindCode'))[:1]
            docCode = forceInt(record.value('documentTypeCode'))

            if docCode and  docCode > 1:
                oss += u'ОСС=2,'

            smo = forceString(record.value('insurerMiac'))[:5]
#Паспорт - ClientDocument ClientDocumentType (паспорт РФ)
#Ориентируемся на ___номер полиса___ и страховую компанию SMO
            if ((not npolis) and (not smo) and (docCode == 1)): #предъявил только паспорт
                oss += u'ОСС=1,'
            self.writeTextElement('VPOLIS', vpolis)
            self.writeTextElement('SPOLIS', forceString(record.value(u'policySerial'))[:10])
            self.writeTextElement('NPOLIS', npolis)
            self.writeTextElement('SMO', smo)
            self.writeTextElement('SMO_OGRN', forceString(record.value('insurerOGRN'))[:15])
            self.writeTextElement('SMO_OK', forceString(record.value('insurerOKATO'))[:5])
            self.writeTextElement('SMO_NAM', forceString(record.value('insurerName'))[:100], writeEmtpyTag = False)
            birthDate = forceDate(record.value('birthDate'))

            if endDate.toJulianDay()-birthDate.toJulianDay() < 29 and Export29XMLCommon.getSpecialCaseCode(QtGui.qApp.db, clientId) == '0003':
                self.writeTextElement('NOVOR', '0''%s%s1' % (forceString(record.value('sex'))[:1], birthDate.toString('ddMMyy')))
            else:
                self.writeTextElement('NOVOR', '0')
            self.writeEndElement() # PACIENT



        if self._lastEventId != eventId or not bufferForConsult:
            if self._lastEventId and not bufferForConsult:
                self.writeEndElement() # SLUCH


            serviceId = forceRef(record.value('serviceId'))
            serviceStr = self.getServiceInfis(serviceId)
            eventTypeCode = forceString(record.value('eventTypeCode'))
            personRegionalCode = forceString(record.value('personRegionalCode'))
            visitId = forceInt(record.value('visit_id'))
            if forceInt(record.value('ContractTariffType')) == 3:
                hospitalDayAmount = (self.getVisitsAmount(eventId))
            if (serviceStr[:3] == '1.4' or serviceStr[:3] == '1.7' or
                serviceStr[:4] == '3.2.' or serviceStr[:4] == '3.1.' or serviceStr[:4] == '3.3.'):
                begDate = endDate = Export29XMLCommon.getDatesForConsultVisit(QtGui.qApp.db, visitId)
                personRegionalCode = Export29XMLCommon.getPersonRegionalCodeForConsultVisit(QtGui.qApp.db, visitId)
#            if serviceStr[:3] == '1.4' or serviceStr[:3] == '1.7':
#                begDate = endDate = forceDate(Export29XMLCommon.getDatesForConsultVisit(QtGui.qApp.db, serviceId,))
            if eventTypeCode in ('2', '7'):
                serviceStr += self.getPersonPostRegionalCode(personId)

            lpu1Str = '7' if eventTypeCode == '7' else ''

            self._lastEventId = eventId
            self.writeStartElement('SLUCH')
            self.writeTextElement('IDCASE', '%d' % self.caseNum)
            # Федеральный код справочника НАЗНАЧЕНИЕ ТИПА СОБЫТИЯ
            self.writeTextElement('USL_OK',  forceString(record.value('medicalAidTypeFederalCode')))
            self.writeTextElement('VIDPOM', forceString(record.value('medicalAidKindCode')))
            forPom = Export29XMLCommon.getHelpForm(QtGui.qApp.db, eventId, forceString(record.value('order')))
            self.writeTextElement('FOR_POM', forceString(forPom))
            self.writeTextElement('NPR_MO', forceString(record.value('relegateOrgMiac')),  writeEmtpyTag = False)
            # 1 – плановая; 2 – экстренная ИЗ СОБЫТИЯ

            if forceInt(record.value('ContractTariffType')) == 10:
                self.writeTextElement('EXTR', forceString(record.value('order')))

            lpu1Str = Export29XMLCommon.getMobileModule(QtGui.qApp.db, forceDouble(miacCode)) if eventTypeCode == '04' else ''
            self.writeTextElement('LPU', miacCode[:6])
            self.writeTextElement('LPU_1', lpu1Str, writeEmtpyTag = False) #У Т(6) Подразделение МО Подразделение МО лечения из регионального справочника
            self.writeTextElement('PODR', forceString(record.value('orgStructureCode')))
            self.writeTextElement('PROFIL', profileStr)
            self.writeTextElement('DET', (u'1' if age < 18 else u'0'))
            self.writeTextElement('NHISTORY', ('%d' % eventId)[:50])
            # Дата начала события


            # Дата окончания события
            self.writeTextElement('DATE_1', begDate.toString(Qt.ISODate))
            self.writeTextElement('DATE_2', endDate.toString(Qt.ISODate))
            birthDate = forceDate(record.value('birthDate'))
            if (begDate.toPyDate() - birthDate.toPyDate()).days < 27:
                oss += u'ОСС=3,'


            self.writeTextElement('DS1', forceString(record.value('MKB')))
            self.writeTextElement('DS2', forceString(record.value('AccMKB')))
            self.writeTextElement('RSLT', forceString(record.value('eventResultFederalCode')))
            # Федеральный код из справочника РЕЗУЛЬТАТ ОСМОТРА. Результат ЗАКЛЮЧИТЕЛЬНОГО ДИАГНОЗА.
            self.writeTextElement('ISHOD', forceString(record.value('resultFederalCode')))
#            self.writeTextElement('VERS_SPEC', u'V015')
            self.writeTextElement('PRVS', forceString(self.parent.getPersonSpecialityFederalCode(personId)))
            self.writeTextElement('IDDOKT', personRegionalCode)
            if endDate.toJulianDay()-birthDate.toJulianDay() < 29 and Export29XMLCommon.getSpecialCaseCode(QtGui.qApp.db, clientId) == '0003':
                self.writeTextElement('OS_SLUCH', '1')
            if (serviceStr[:2] == '30' or
                serviceStr[:2] == '31' or
                serviceStr[:2] == '34'or
                serviceStr[:4] == '3.18' or
                serviceStr[:4] == '3.20' or
                serviceStr[:4] == '3.23'):
                self.writeTextElement('OS_SLUCH', '3')
            if (serviceStr[:2] == '33' or serviceStr[:4] == '3.19'):
                self.writeTextElement('OS_SLUCH', '4')
            ot = forceString(record.value('patrName'))
            if ot == u'нет' or ot == u'Нет' :
                self.writeTextElement('OS_SLUCH', '2')
            (totalAmount,  totalSum) = eventsInfo[eventId]
            self.writeTextElement('IDSP', forceString(record.value('medicalAidUnitFederalCode')))
            if (serviceStr[:3] == '1.4' or
                serviceStr[:3] == '1.7' or
                serviceStr[:2] == '17' or
                serviceStr[:3] == '3.2' or
                serviceStr[:3] == '3.1' or
                serviceStr[:3] == '3.7' or
                serviceStr[:3] == '3.3'
                ):
                self.writeTextElement('ED_COL', ('1'))
            else:
                self.writeTextElement('ED_COL', ('%6.2f' % totalAmount).strip() )
            self.writeTextElement('SUMV', str(self.caseNum)) #('%10.2f' % round(totalSum,2))
            ot = forceString(record.value('patrName'))
            if not ot:
                oss += u'ОСС=5,'
            traumaCode = forceInt(record.value('traumaCode'))

            if traumaCode in range(1,5):
                oss += u'ОСС=8,'
            elif traumaCode == 13:  #противоправные действия
                oss += u'ОСС=6,'

#TODO: Если является удостоверением и не паспорт см. поля таблицы ClientDocument

            relId = forceInt(record.value('relativeId'))
            relInfo = self.getRelationInfo(relId)
            if relInfo:
                relType = forceInt(relInfo.value('relTypeCode'))
                parentDocType = forceInt(relInfo.value('docTypeCode'))
#у пациента нет паспорта, есть связь, связь по одному из родителей, и родитель предъявил паспорт
                if not docCode and relId and relType in range(1, 4) and parentDocType == 1:
                    oss += u'ОСС=4,'


            if (eventTypeCode == 926): #доп. диспансеризация сирот
                oss += u'ОСС=7,'
#TODO проверить условие
#Лучше сделать по МЭС
#Почему visit? выделять особый event.
            if forceInt(record.value('EventServiceId')) in self.getStandartServiceIds():
                oss += u'ОСС=9,'
#            self.writeTextElement('COMENTSL', QString(oss[:-1]))
            container.dictSums[self.caseNum] = 0.0
            self.caseNum+= 1
        serviceId = forceRef(record.value('serviceId'))
        serviceStr = self.getServiceInfis(serviceId)
        eventTypeCode = forceString(record.value('eventTypeCode'))

#        if eventTypeCode in ('2', '7'):
#            serviceStr += self.getPersonPostRegionalCode(personId)
        lpu1Str = Export29XMLCommon.getMobileModule(QtGui.qApp.db, forceDouble(miacCode)) if eventTypeCode == '04' else ''

        uet = forceDouble(record.value('uet'))
        price = forceDouble(record.value('price')) - regionalPrice - federalPrice
#        priceTotal = price
        ctUet = forceDouble(record.value('ContractTariffUet'))

        if (uet > 0):
            #Делаем цены за единицу УЕТ согласно контракту
            price = Export29XMLCommon.doubleToStrRounded(price / ctUet )
            regionalPrice = Export29XMLCommon.doubleToStrRounded(regionalPrice / ctUet)
            federalPrice = Export29XMLCommon.doubleToStrRounded(federalPrice / ctUet)
            amount = uet

        #TODO: Duplicate code! Fix!
        (totalAmount,  totalSum) = eventsInfo[eventId]
        composition, totalpercents = self.getContractCompositionInfo(forceString(record.value('contractTariffId')))
#        if hospitalDayAmount <4 and  hospitalDayAmount>0 and serviceStr[:4] == '2.5.':
#            totalpercents = totalpercents/2
        summ = Export29XMLCommon.doubleToStrRounded(amount * price)
        if not bufferForConsult:
#            container.summTotal +=                  Export29XMLCommon.doubleToStrRounded(summ + regionalSum+forceDouble(record.value('price')) *  totalpercents*amount/100.00)
#            container.dictSums[self.caseNum - 1] += Export29XMLCommon.doubleToStrRounded(summ + regionalSum+forceDouble(record.value('price')) *  totalpercents*amount/100.00)
            container.summTotal +=                  Export29XMLCommon.doubleToStrRounded(summ + regionalSum+  totalpercents*amount)
            container.dictSums[self.caseNum - 1] += Export29XMLCommon.doubleToStrRounded(summ + regionalSum+  totalpercents*amount)

#        else:
#            amount = totalAmount
#            summ = totalAmount * price
#По требованию фомса, если было более 1 движения, записываем amount и сумму по всем услугам
#если мы достигли этого участка кода - значит автоматически предполагается, что речь идет о самом последнем action-е


        if (serviceStr[:3] == '1.4' or
            serviceStr[:3] == '1.7' or
            bufferForConsult or
            serviceStr[:2] == '2.' or
            serviceStr[:3] == '3.2' or
            serviceStr[:3] == '3.1' or
            serviceStr[:3] == '1.5'):
                if not composition:
                    self.writeService(record, miacCode, age, profileStr,
                                            serviceStr,
                                            price,
                                            amount,
                                            summ,
                                            latestMoveFlag,
                                            PriceType.basePrice,
                                            lpu1Str
                                            )
                else:
                    self.writeService(record, miacCode, age, profileStr,
                                            serviceStr,
                                            price,
                                            amount,
                                            summ,
                                            latestMoveFlag,
                                            PriceType.basePrice,
                                            lpu1Str
                                            )

                    for code, percent in composition.items():
                        #p = forceDouble(record.value('contractTariffPrice'))
#                        compprice = Export29XMLCommon.doubleToStrRounded(price * percent / 100.00)
#                        if hospitalDayAmount <4 and  hospitalDayAmount>0 and serviceStr[:4] == '2.5.':
#                            percent = percent/2
                        compsumm =  Export29XMLCommon.doubleToStrRounded(percent * amount)
                        visitId = ''
                        self.writeService(record, miacCode, age, profileStr,
                                                serviceStr,
                                                percent,
                                                amount,
                                                compsumm,
                                                lpu1Str,
                                                latestMoveFlag,
                                                PriceType.basePrice,
                                                visitId,
                                                code
                                                )
                if (forceInt(record.value('ContractTariffType')) == 3) and (serviceStr[:4] == '2.5.' or
                                                                            serviceStr[:4] == '2.6.' or
                                                                            serviceStr[:4] == '2.4.' and
                                                                            (serviceStr[:6] != '2.5.13' and
                                                                            serviceStr[:6] != '2.5.14' and
                                                                            serviceStr[:6] != '2.5.15')):# виртуальные услуги для дневного стационар
                        serviceStr1 = '2.20.1' # if (serviceStr[2] == '2.') else  '81.1'
#                       serviceStr = '81.1'
                        self.writeService(record,
                              miacCode,
                              age,
                              profileStr,
                              serviceStr1,
                              federalPrice,
                              hospitalDayAmount,
                              federalSum,
                              latestMoveFlag,
                              PriceType.federalPrice,
                              lpu1Str)
#
#            if federalPrice > 0.0:
#                serviceCode = self.getServiceCode(serviceId)
#                serviceStr = self.getServiceInfis(serviceId)
#                eventName = forceString(record.value('EventTypeName'))
#                if (serviceCode and serviceCode[:4] == 'STD_') or eventName.lower().find(u"стандарт") >-1 :
#                    serviceStr = '51.%s' % serviceStr[3:5]
#                else:
#                    postFederalCode = self.getPersonPostFederalCode(personId)
#                    if postFederalCode:
#                        serviceStr = postFederalCode

#                self.writeService(record, miacCode, age,
#                                  profileStr,
#                                  serviceStr,
#                                  federalPrice,
#                                  amount,
#                                  federalSum,
#                                  latestMoveFlag,
#                                  PriceType.federalPrice,
#                                  lpu1Str
#                                  )
                if (serviceStr[:2] == '17' or
                    federalPrice > 0.0 or
                    serviceStr[:3]== '3.7' ): # виртуальные услуги для обращений
                    visits = self.getVisits(eventId, serviceId)
                    postFederalCode = self.getPersonPostFederalCode(personId, serviceStr)
                    if postFederalCode:
                        serviceStr = postFederalCode
                    for visitId in visits:
                        self.writeService(record, miacCode, age,
                                  profileStr,
                                  serviceStr,
                                  federalPrice,
                                  amount,
                                  federalSum,
                                  latestMoveFlag,
                                  PriceType.federalPrice,
                                  lpu1Str,
                                  visitId
                                  )
    #----------------------------------------
                if regionalPrice > 0.0:
                    consultVisit = 1 if (serviceStr[:3] == '1.4' or serviceStr[:3] == '1.7' or serviceStr[:4] == '3.2.' or serviceStr[:4] == '3.1.') else ''
                    serviceCode = serviceStr
                    serviceStr = ''
                                     # serviceCode = self.getServiceCode(serviceId)
                    if forceInt(record.value('ContractTariffType')) == 3 and uet > 0.0:
                        serviceStr = '3.15.1' if datetime.date(2014,1,1) else '53.4'
                    elif (forceInt(record.value('ContractTariffType')) == 0 and (serviceCode.startswith('6.') or
                            serviceCode.startswith('8.') or serviceCode.startswith('2.2') or serviceCode.startswith('2.3.1'))):
                        serviceStr = '2.13.1' if forceDate(record.value('endDateEvent')) >= datetime.date(2014,1,1) else '53.3'
                    elif serviceCode.startswith('4.6') or serviceCode.startswith('2.8'):
                            serviceStr = '2.23.2' if forceDate(record.value('endDateEvent')) >= datetime.date(2014,1,1) else '53.13'
                    elif (forceInt(record.value('ContractTariffType')) == 3 and
                      (serviceCode.startswith('20.') or
                      serviceCode.startswith('2.5'))):
                        serviceStr = '2.10.3' if forceDate(record.value('endDateEvent')) >= datetime.date(2014,1,1) else '53.9'
                    elif (forceInt(record.value('ContractTariffType')) == 3 and
                      (serviceCode.startswith('21.')
                       or serviceCode.startswith('2.6.1'))):
                        serviceStr = '2.10.1' if forceDate(record.value('endDateEvent')) >= datetime.date(2014,1,1) else '53.10'
                    elif (forceInt(record.value('ContractTariffType')) == 2 and
                      (serviceCode.startswith('12.') or
                       serviceCode.startswith('3.9') or
                       serviceCode.startswith('3.10'))):
                        serviceStr = '3.14.1' if forceDate(record.value('endDateEvent')) >= datetime.date(2014,1,1) else '53.2'
                    else:
                        if forceDate(record.value('endDateEvent')) >= datetime.date(2014,1,1):
                            serviceStr = {
                                  0: lambda x : '3.14.1',
                                  1: lambda x : '3.4.1',
                                  2: lambda x : '4.3.1',
                                  3: lambda x : '2.13.1',
                                  4: lambda x : '1.4.1',
                                  5: lambda x : '3.15.1',
                                  6: lambda x : '1.3.1',
                                  9: lambda x : '1.7.1',
                                  10: lambda x: '1.7.1',
                                  11: lambda x: '3.13.1'
                            }[forceInt(record.value('ContractTariffType'))](serviceStr)
                        else:
                            serviceStr = {
                                  0: lambda x : '53.2',
                                  1: lambda x : '53.1',
                                  2: lambda x : '53.5',
                                  3: lambda x : '53.3',
                                  4: lambda x : '53.1',
                                  5: lambda x : '53.4',
                                  6: lambda x : '53.7',
                                  9: lambda x : '53.1',
                                  10: lambda x: '53.1',
                                  11: lambda x: '53.6'
                            }[forceInt(record.value('ContractTariffType'))](serviceStr)
                    if forceInt(record.value('ContractTariffType')) == 10 or serviceCode.startswith('2.5.'):
                        amount = 1
                    if serviceCode.startswith('2.5.') or serviceCode.startswith('2.6.') or serviceCode.startswith('2.7.'):
                        regionalSum = regionalPrice
                    self.writeService(record, miacCode, age,
                                  profileStr,
                                  serviceStr,
                                  regionalPrice,
                                  amount,
                                  regionalSum,
                                  latestMoveFlag,
                                  PriceType.regionalPrice,
                                  lpu1Str,
                                  consultVisit
                                  )
                if bufferForConsult: del bufferForConsult[0]
        else:
                visitId = Export29XMLCommon.getVisit(QtGui.qApp.db, accountId, eventId, serviceId)
                bufferForConsult.append(visitId)



        oss = forceString(QString(oss[:-1]))
        self.ossString = oss


    def writeService(self, record, miacCode, age, profileStr, serviceStr, price, amount,
                     summ, multiplyMovementLogicFlag, priceType,  lpu1Str='', visitId = '',
                     compCode = None):
        self.writeStartElement('USL')
        self.writeTextElement('IDSERV',  '1' if (serviceStr[:3] =='1.4' or serviceStr[:3] == '3.2') else ('%8d' % self.serviceNum).strip()) # O N(8) номер записи в реестре услуг
        self.writeTextElement('LPU', miacCode[:6]) #O Т(6) Код МО МО лечения
        self.writeTextElement('LPU_1', lpu1Str, writeEmtpyTag = False) #У Т(6) Подразделение МО Подразделение МО лечения из регионального справочника
        self.writeTextElement('PODR', forceString(record.value('orgStructureCode')), writeEmtpyTag = False) #У N(8) Код отделения Отделение МО лечения из регионального справочника
        self.writeTextElement('PROFIL', profileStr) #O N(3) Профиль Классификатор V002

        self.writeTextElement('VID_VME', self.getOperationCode(forceInt(record.value('event_id'))))

        self.writeTextElement('DET', (u'1' if age < 18 else u'0')) #О N(1) Признак детского профиля 0-нет, 1-да.

        dateIn = None
        dateOut = None
        #Проверить полноту всех нижеследующтх if
        #услуга обычная, берем по action
        db = QtGui.qApp.db

        if forceInt(record.value('action_id')) == 0 and forceInt(record.value('visit_id'))==0:
            dateIn = forceDate(record.value('begDateEvent'))
            dateOut = forceDate(record.value('endDateEvent'))

        if forceInt(record.value('action_id')):
            (dateIn, dateOut) = Export29XMLCommon.getDatesForAction(db,
                                                                    forceInt(record.value('event_id')),
                                                                    forceInt(record.value('action_id')),
                                                                    serviceStr)
        #Гемодиализ, профосмотр, лечебно-диагностическая, etc
        else:
            if not dateIn and not dateOut:
                dateIn  = forceDate(record.value('dateVisit'))
                dateOut = forceDate(record.value('dateVisit'))

        if dateOut and dateIn and visitId:
            dateIn = dateOut = self.getDateForVisits(visitId)

#        if serviceStr[:3] == '1.4' or serviceStr[:3] == '1.7':
#            container.date[self.dateNum -1] = dateIn


        if (serviceStr[:2] == '17' or
            serviceStr[:2] == '53' or
            serviceStr[:3] == '3.7' or
            Export29XMLCommon.isRegionalAdditionalPay(db, serviceStr) == True):
            if visitId == 1 or serviceStr[:5] == '3.14.':
                if forceInt(record.value('action_id')):
                    pass
                else:
                    dateIn = dateOut = self.getDateForVisits(forceRef(record.value('visit_id')))
            else:
                dateIn = forceDate(record.value('begDateEvent'))
                dateOut = forceDate(record.value('endDateEvent'))

        self.writeTextElement('DATE_IN', dateIn.toString(Qt.ISODate)) #O D Дата начала оказания услуги
        self.writeTextElement('DATE_OUT', dateOut.toString(Qt.ISODate)) #O D Дата окончания оказания услуги

        self.writeTextElement('DS', forceString(record.value('MKB'))) #O Т(10) Диагноз Код из справочника МКБ до уровня подрубрики

        if (serviceStr.lower().find('a16') != -1):
            pass

        if not compCode:
            self.writeTextElement('CODE_USL', serviceStr) #O Т(16) Код услуги Территориальный классификатор услуг
        else:
            self.writeTextElement('CODE_USL', compCode)

        self.writeTextElement('KOL_USL', ('%6.2f' % amount).strip() ) #O N(6.2) Количество услуг (кратность услуги)
        self.writeTextElement('TARIF', ('%15.2f' % price).strip()) #O N(15.2) Тариф
        self.writeTextElement('SUMV_USL', ('%15.2f' % summ).strip()) #O N(15.2) Стоимость медицинской услуги, выставленная к оплате (руб.)
#        self.writeTextElement('PRVS', forceString(self.parent.getPersonSpecialityFederalCode(forceRef(record.value('execPersonId'))))) #O N(9) Специальность медработника, выполнившего услугу
        if visitId == 1 or visitId== 0: visitId = None
        personId, codeMd = Export29XMLCommon.getPcode(db, record, visitId)
        self.writeTextElement('PRVS', forceString(self.parent.getPersonSpecialityFederalCode(personId)))
        self.writeTextElement('CODE_MD', codeMd)

#        schTStr = ''
#        if priceType == PriceType.federalPrice:
#            schTStr = u'Мод-доступность'
#        elif priceType == PriceType.regionalPrice:
#            schTStr = u'Прикреп-доп'
#        elif priceType == PriceType.basePrice:
#            schTStr = u'Прикреп'

        # if serviceStr.startswith('13.'):
        #    schTStr = u'Мод-стандарт'
#        if (Export29XMLCommon.isPatientAttached(QtGui.qApp.db, forceInt(record.value('client_id')))):


#=====================
#Это для основного блока USL
#Если человек является прикрепленным
#ClientAttach, rbAttachType CODE = 1
#        self.writeTextElement('SCH_T', schTStr )
        self.writeEndElement() #USL
        self.serviceNum += 1


    def writeFileHeader(self,  device, fileName, accNumber, accDate, year, month, miacCode, payerCode, accSum):
        self.recNum = 1
        self.caseNum = 1
        self._lastClientId = None
        self.serviceNum = 1
        self.setDevice(device)
        self.writeStartDocument()
        self.writeStartElement('ZL_LIST')
        self.writeHeader(fileName, accNumber, accDate, year, month, miacCode, payerCode, accSum)


    def writeHeader(self, fileName, accNumber, accDate, year, month, miacCode, payerCode, accSum):
        self.writeStartElement('ZGLV')
        self.writeTextElement('VERSION', '1.0')
        self.writeTextElement('DATA', accDate.toString(Qt.ISODate))
        (fname,  ext) = os.path.splitext(os.path.basename(fileName))
        self.writeTextElement('FILENAME', fname[:26])
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
#            self.writeTextElement('SUMMAV', (caccSum).strip())
            self.writeTextElement('SUMMAV', 'dummy')

#            self.writeTextElement('SUMMAP', '0.00')
#            self.writeTextElement('SANK_MEK', '0.00')
#            self.writeTextElement('SANK_MEE', '0.00')
#            self.writeTextElement('SANK_EKMP', '0.00')
            self.writeEndElement()

    def writeTextElement(self, element,  value, writeEmtpyTag = False):
        if not writeEmtpyTag and (not value or value == ''):
            return

        QXmlStreamWriter.writeTextElement(self, element, value)

    def writeFileFooter(self):
        self.writeEndElement() # SLUCH
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
        result = self.medicalAidProfileCache.get(key, -1)

        if result == -1:
#            if serviceId is None or personId is None:
#                print "Shit happens"
            result = None
            stmt = """SELECT rbMedicalAidProfile.code
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

    def getVisits(self, eventId, serviceId):
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
                            ActionType.serviceType = %d AND
                            `Action`.`deleted` = 0
                    LIMIT 1""" %(eventId, CActionServiceType.operation)

        query =  QtGui.qApp.db.query(stmt)
        if query.next():
            return (forceString(query.record().value('operationCode')))
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


    def writeRecord(self, record):

        clientId = forceRef(record.value('client_id'))
        sex = forceString(record.value('sex'))
        birthDate = forceDate(record.value('birthDate'))
        #замена дефиса в свидетельстве о рождении
        if forceDouble(record.value('documentFederalCode')) == 3:
            documentSerial= forceString(record.value('documentSerial')).replace(' ', '-')
        else: documentSerial=forceString(record.value('documentSerial'))
#        okatog = Export29XMLCommon.changeOkato(forceString(record.value('placeOKATO')))
        if clientId in self._clientsSet:
            return

        self.writeStartElement('PERS')
        self.writeTextElement('ID_PAC',  ('%d' % clientId)[:36])
        #Фамилия пациента.



        self.writeTextElement('FAM', forceString(record.value('lastName')))
        #Имя пациента

        self.writeTextElement('IM', forceString(record.value('firstName')))
        #Отчество пациента

        self.writeTextElement('OT', forceString(record.value('patrName')))
        #Пол пациента.
        self.writeTextElement('W', sex)
        #Дата рождения пациента.
        self.writeTextElement('DR', birthDate.toString(Qt.ISODate))

        self.writeTextElement('MR', forceString(record.value('birthPlace')), writeEmtpyTag=False)
        # Федеральный код из справочника ТИПЫ ДОКУМЕНТОВ. Из карточки пациента.
        self.writeTextElement('DOCTYPE',  forceString(record.value('documentFederalCode')))
        # Серия документа, удо-стоверяющего личность пациента.
        self.writeTextElement('DOCSER', documentSerial)
        # Номер документа, удостоверяющего личность пациента.
        self.writeTextElement('DOCNUM', forceString(record.value('documentNumber')))
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
        self.writeTextElement('VERSION', '1.0')
        self.writeTextElement('DATA', accDate.toString(Qt.ISODate))
        (fname,  ext) = os.path.splitext(os.path.basename(fileName))
        self.writeTextElement('FILENAME', 'L%s' % fname[1:26])
        self.writeTextElement('FILENAME1', fname[:26])
        self.writeEndElement()

    def writeFileFooter(self):
        self.writeEndElement() # root
        self.writeEndDocument()



