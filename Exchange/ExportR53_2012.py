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
from PyQt4.QtCore import Qt, QDate, QDir, QFile, QString, QTextCodec, QXmlStreamWriter, pyqtSignature, SIGNAL

from library.Utils     import calcAgeTuple, forceBool, forceDate, forceDouble, forceInt, forceRef, forceString, forceStringEx, formatSNILS, toVariant, trim

from Accounting.ServiceDetailCache import CServiceDetailCache
from Events.Action import CAction
from Exchange.Export import CExportHelperMixin
from Exchange.ExportR53Native import CServiceInfoXmlStreamReader, CServiceInfoXmlStreamWriter
from Exchange.Utils import compressFileInZip

from Exchange.Ui_ExportR53_2012Page1 import Ui_ExportPage1
from Exchange.Ui_ExportPage2 import Ui_ExportPage2

# Форматы экспорта
exportType2012 = 0
exportType2013TFOMS = 1
exportTypeServiceInfo = 2

def getAccountInfo(accountId):
    db = QtGui.qApp.db
    accountRecord = db.getRecord('Account', 'settleDate, number, exposeDate, contract_id, payer_id, date', accountId)
    if accountRecord:
        date = forceDate(accountRecord.value('settleDate'))
        aDate  = forceDate(accountRecord.value('date'))
        exposeDate = forceDate(accountRecord.value('exposeDate'))
        strNumber = forceString(accountRecord.value('number')).strip()
        if strNumber.isdigit():
            number = forceInt(strNumber)
        else:
            # убираем номер договора с дефисом, если они есть в номере
            i = len(strNumber) - 1
            while (i>0 and strNumber[i].isdigit()):
                i -= 1

            number = forceInt(strNumber[i+1:] if strNumber[i+1:] != '' else 0)

        contractId = forceRef(accountRecord.value('contract_id'))
        payerId = forceRef(accountRecord.value('payer_id'))
    else:
        date = exposeDate = contractId = payerId = aDate = None
        number = 0
    return date, number, exposeDate, contractId,  payerId,  aDate


def exportR53_2012(widget, accountId, accountItemIdList):
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
        self.page2 = CExportPage2(self)
        self.addPage(self.page1)
        self.addPage(self.page2)
        self.setWindowTitle(u'Мастер экспорта в Новгородской области')
        self.tmpDir = ''
        self.xmlLocalFileName = ''


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
            self.tmpDir = QtGui.qApp.getTmpDir('R53_2012')
        return self.tmpDir


    def getFullXmlFileName(self):
        u"""HPiNiPpNp_YYMMN.XML, где
            H – константа, обозначающая передаваемые данные.
            Pi – Параметр, определяющий организацию-источник:
            T – ТФОМС;
            S – СМО;
            M – МО.     -   в нашем случаи M
            Ni – Номер источника (Код МИАЦ ЛПУ).
            Pp – Параметр, определяющий организацию -получателя:
            T – ТФОМС;
            S – СМО;
            M – МО  в нашем случаи S
            Np – Номер получателя (Код МИАЦ СМО).
            YY – две последние цифры порядкового номера года отчетного периода.
            MM – порядковый номер месяца отчетного периода - из даты на которую формируется счёт.
            N – порядковый номер пакета. Присваивается в порядке возрастания, начиная со значения «1»,
            увеличиваясь на единицу для каждого следующего пакета в данном отчетном периоде."""
        if not self.xmlLocalFileName:
            lpuInfis = forceString(QtGui.qApp.db.translate(
                'Organisation', 'id', QtGui.qApp.currentOrgId(), 'miacCode'))
#            orgStructCode = forceString(QtGui.qApp.db.translate(
#                'OrgStructure', 'id', QtGui.qApp.currentOrgStructureId(), 'infisCode'))
            (date, number, exposeDate, contractId,  payerId,  aDate) = getAccountInfo(self.accountId)

            payerCode = forceString(QtGui.qApp.db.translate(
                    'Organisation', 'id', payerId, 'miacCode'))
            exportType = self.page1.cmbExportType.currentIndex()

            if exportType == exportType2012:
                self.xmlLocalFileName = os.path.join(self.getTmpDir(), \
                    u'HM530%sS53%s_%s%d.xml' % (lpuInfis, payerCode, date.toString('yyMM'), self.page1.edtRegistryNumber.value()))
            elif exportType == exportType2013TFOMS:
                self.xmlLocalFileName = os.path.join(self.getTmpDir(),
                    u'PM530%sT%s_%s%05d.xml' % (lpuInfis, payerCode, date.toString('yyyyMM'), self.page1.edtRegistryNumber.value()))
            elif exportType == exportTypeServiceInfo:
                self.xmlLocalFileName = os.path.join(self.getTmpDir(),
                    u'ServiceInfo_%s%05d.xml' % (date.toString('yyyyMM'), self.page1.edtRegistryNumber.value()))

        return self.xmlLocalFileName


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

        self.aborted = False
        self.done = False
        self.idList = []
        self.parent = parent #wtf? скрывать Qt-шный parent - это плохая затея
        self.recNum= 0
        self.exportType = exportType2012
        self.setExportMode(False)

        self.edtBegDate.canBeEmpty()
        self.edtEndDate.canBeEmpty()

        self.ignoreErrors = forceBool(QtGui.qApp.preferences.appPrefs.get(
            'ExportR53_2012IgnoreErrors', False))
        self.connect(parent, SIGNAL('rejected()'), self.abort)
        self.chkVerboseLog.setChecked(forceBool(QtGui.qApp.preferences.appPrefs.get(
            'ExportR53_2012VerboseLog', False)))
        self.chkIgnoreErrors.setChecked(self.ignoreErrors)
        self.edtRegistryNumber.setValue(forceInt(QtGui.qApp.preferences.appPrefs.get(
            'ExportR53_2012RegistryNumber', 0))+1)
        self.chkGroupByService.setChecked(forceBool(QtGui.qApp.preferences.appPrefs.get(
            'ExportR53_2012GroupByService', True)))
        self.edtServiceInfoFileName.setText(forceString(QtGui.qApp.preferences.appPrefs.get(
            'ExportR53_2012ServiceInfoFileName', '')))
        self.cmbExportType.setCurrentIndex(forceInt(QtGui.qApp.preferences.appPrefs.get(
            'ExportR53_2012ExportType', 0)))
        self.edtBegDate.setDate(forceDate(QtGui.qApp.preferences.appPrefs.get(
            'ExportR53_2012BegDate', QDate())))
        self.edtEndDate.setDate(forceDate(QtGui.qApp.preferences.appPrefs.get(
            'ExportR53_2012EndDate', QDate())))


    def setExportMode(self, flag):
        self.btnCancel.setEnabled(flag)
        self.btnExport.setEnabled(not flag)
        self.chkIgnoreErrors.setEnabled(not flag)
        self.chkVerboseLog.setEnabled(not flag)
        self.btnExport.setEnabled(not flag)
        self.edtRegistryNumber.setEnabled(not flag)
        self.chkGroupByService.setEnabled(not flag)
        self.cmbExportType.setEnabled(not flag)

        enableDateFields = ((not flag) and\
            self.exportType in (exportType2013TFOMS, exportTypeServiceInfo))

        enableServiceInfoFields = ((not flag) and\
            self.exportType != exportTypeServiceInfo)

        self.edtBegDate.setEnabled(enableDateFields)
        self.edtEndDate.setEnabled(enableDateFields)

        self.edtServiceInfoFileName.setEnabled(enableServiceInfoFields)
        self.btnSelectServiceInfoFileName.setEnabled(enableServiceInfoFields)


    def log(self, str, forceLog = False):
        if self.chkVerboseLog.isChecked() or forceLog:
            self.logBrowser.append(str)
            self.logBrowser.update()


    def setAccountItemsIdList(self, accountItemIdList):
        self.idList = accountItemIdList


    def prepareToExport(self, exportType):
        self.done = False
        self.aborted = False
        self.emit(SIGNAL('completeChanged()'))
        self.setExportMode(True)
        output, clientOutput = self.createXML(exportType)
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
            QtGui.qApp.preferences.appPrefs['ExportR53_2012IgnoreErrors'] = \
                    toVariant(self.chkIgnoreErrors.isChecked())
            QtGui.qApp.preferences.appPrefs['ExportR53_2012VerboseLog'] = \
                    toVariant(self.chkVerboseLog.isChecked())
            QtGui.qApp.preferences.appPrefs['ExportR53_2012GroupByService'] = \
                    toVariant(self.chkGroupByService.isChecked())
            QtGui.qApp.preferences.appPrefs['ExportR53_2012ServiceInfoFileName'] = \
                    toVariant(self.edtServiceInfoFileName.text())
            QtGui.qApp.preferences.appPrefs['ExportR53_2012ExportType'] = \
                    toVariant(self.cmbExportType.currentIndex())
            QtGui.qApp.preferences.appPrefs['ExportR53_2012BegDate'] = \
                    toVariant(self.edtBegDate.date())
            QtGui.qApp.preferences.appPrefs['ExportR53_2012EndDate'] = \
                    toVariant(self.edtEndDate.date())

            self.done = True
            self.emit(SIGNAL('completeChanged()'))


# *****************************************************************************************

    def getPreliminaryInfo(self):
        u"""Загрузка информации о предварительном реестре из XML"""

        if self.edtServiceInfoFileName.text().isEmpty():
            return {}

        inFile = QFile(self.edtServiceInfoFileName.text())
        if not inFile.open(QFile.ReadOnly | QFile.Text):
            QtGui.QMessageBox.warning(self, u'Импорт данных о предварительном реестре счета',
                                      QString(u'Не могу открыть файл для чтения %1:\n%2.')
                                      .arg(self.edtServiceInfoFileName.text())
                                      .arg(inFile.errorString()))
            return {}

        myXmlStreamReader = CServiceInfoXmlStreamReader(self, self.chkVerboseLog.isChecked())
        if (not myXmlStreamReader.readFile(inFile)):
            if self.aborted:
                self.log(u'! Прервано пользователем.')
            else:
                self.log(u'! Ошибка: файл %s, %s' % (self.edtServiceInfoFileName.text(), myXmlStreamReader.errorString()))

        return myXmlStreamReader.registryInfo

# *****************************************************************************************

    def createQuery(self):
        db = QtGui.qApp.db
        tableAccountItem = db.table('Account_Item')
        idList = []

        if self.cmbExportType.currentIndex()  in (
                exportType2013TFOMS, exportTypeServiceInfo):
            begDate = self.edtBegDate.date()
            endDate = self.edtEndDate.date()

            stmt= """SELECT Account_Item.id
                    FROM Account
                    LEFT JOIN Account_Item ON Account_Item.master_id = Account.id
                    LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
                    LEFT JOIN Contract ON Account.contract_id = Contract.id
                    LEFT JOIN rbFinance ON Contract.finance_id = rbFinance.id
                    WHERE Account.settleDate BETWEEN '%s' AND '%s'
                    AND rbFinance.code = '2'
                    AND Account_Item.reexposeItem_id IS NULL
                    AND (Account_Item.date IS NULL
                    OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
                """ % (begDate.toString(Qt.ISODate) if begDate else '0000-00-00',
                          endDate.toString(Qt.ISODate) if endDate else '2999-12-31')

            query = db.query(stmt)
            while query.next():
                record = query.record()
                if record:
                    idList.append(forceRef(record.value(0)))
        else:
            idList = self.idList

        cond = tableAccountItem['id'].inlist(idList)

        if self.chkGroupByService.isChecked():
            sumStr = """SUM(Account_Item.`sum`) AS `sum`,
                SUM(Account_Item.amount) AS amount,
                SUM(LEAST(IF(Contract_Tariff.federalLimitation = 0,
                            Account_Item.amount,
                            LEAST(Contract_Tariff.federalLimitation, Account_Item.amount)) * Contract_Tariff.federalPrice,
                            Account_Item.sum)) AS federalSum,
                        SUM(LEAST(IF(Contract_Tariff.regionalLimitation = 0,
                            Account_Item.amount,
                            LEAST(Contract_Tariff.regionalLimitation, Account_Item.amount)) * Contract_Tariff.regionalPrice,
                            Account_Item.sum)) AS regionalSum,"""
            cond += ' GROUP BY `Account_Item`.`event_id`, serviceId'
        else:
            sumStr = """Account_Item.`sum` AS `sum`,
                Account_Item.amount AS amount,
                 LEAST(IF(Contract_Tariff.federalLimitation = 0,
                            Account_Item.amount,
                            LEAST(Contract_Tariff.federalLimitation, Account_Item.amount)) * Contract_Tariff.federalPrice,
                            Account_Item.sum) AS federalSum,
                 LEAST(IF(Contract_Tariff.regionalLimitation = 0,
                            Account_Item.amount,
                            LEAST(Contract_Tariff.regionalLimitation, Account_Item.amount)) * Contract_Tariff.regionalPrice,
                            Account_Item.sum) AS regionalSum,"""

        stmt = """SELECT Account_Item.id AS accountItemId,
                Account_Item.event_id  AS event_id,
                Account_Item.visit_id,
                Account_Item.action_id,
                Account_Item.service_id,
                Event.client_id        AS client_id,
                Client.lastName,
                Client.firstName,
                Client.patrName,
                Client.birthDate       AS birthDate,
                Client.sex AS sex,
                Client.SNILS AS SNILS,
                Client.birthPlace AS birthPlace,
                age(Client.birthDate, Event.execDate) as clientAge,
                ClientPolicy.serial AS policySerial,
                ClientPolicy.number AS policyNumber,
                ClientPolicy.begDate   AS policyBegDate,
                ClientPolicy.endDate   AS policyEndDate,
                rbPolicyKind.federalCode AS policyKindFederalCode,
                Insurer.OGRN AS insurerOGRN,
                Insurer.OKATO AS insurerOKATO,
                Insurer.area AS insurerArea,
                Insurer.miacCode AS insurerMiac,
                ClientDocument.serial  AS documentSerial,
                ClientDocument.number  AS documentNumber,
                rbDocumentType.federalCode AS documentFederalCode,
                kladr.KLADR.OCATD AS placeOKATO,
                locKLADR.OCATD AS locPlaceOKATO,
                IF(Account_Item.visit_id IS NOT NULL, Visit.person_id,
                    IF(Account_Item.action_id IS NOT NULL,
                        IF(Action.person_id IS NOT NULL, Action.person_id, Action.setPerson_id), Event.execPerson_id)
                ) AS execPersonId,
                Diagnosis.MKB          AS MKB,
                Event.setDate          AS begDate,
                Event.execDate         AS endDate,
                Contract_Tariff.federalPrice AS federalPrice,
                Contract_Tariff.regionalPrice AS regionalPrice,
                Contract_Tariff.price AS price, %s
                rbDiagnosticResult.federalCode AS resultFederalCode,
                rbMedicalAidType.federalCode AS medicalAidTypeFederalCode,
                rbMedicalAidKind.federalCode AS medicalAidKindFederalCode,
                IF(Account_Item.service_id IS NOT NULL,
                    rbItemService.id,
                    IF(Account_Item.visit_id IS NOT NULL, rbVisitService.id, rbEventService.id)
                    ) AS serviceId,
                AccDiagnosis.MKB AS AccMKB,
                OrgStructure.infisCode AS orgStructureCode,
                rbMedicalAidUnit.federalCode AS medicalAidUnitFederalCode,
                Event.`order`,
                Event.id AS eventId,
                EventResult.federalCode AS eventResultFederalCode,
                OldAccountItem.id AS oldAccItemId
            FROM Account_Item
            LEFT JOIN Action ON Action.id = Account_Item.action_id
            LEFT JOIN Visit  ON Visit.id  = Account_Item.visit_id
            LEFT JOIN Event  ON Event.id  = Account_Item.event_id
            LEFT JOIN Client ON Client.id = Event.client_id
            LEFT JOIN ClientPolicy ON ClientPolicy.client_id = Client.id AND
                      ClientPolicy.id = (SELECT MAX(CP.id)
                                         FROM   ClientPolicy AS CP
                                         LEFT JOIN rbPolicyType AS CPT ON CPT.id = CP.policyType_id
                                         WHERE  CP.client_id = Client.id AND CP.deleted=0 AND CPT.code IN ('1','2'))
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
            LEFT JOIN ClientAddress ClientLocAddress ON ClientLocAddress.client_id = Client.id AND
                      ClientLocAddress.id = (SELECT MAX(CLA.id)
                                         FROM   ClientAddress AS CLA
                                         WHERE  CLA.type = 1 AND CLA.client_id = Client.id AND CLA.deleted=0)
            LEFT JOIN Address RegAddress ON RegAddress.id = ClientRegAddress.address_id
            LEFT JOIN Address LocAddress ON LocAddress.id = ClientLocAddress.address_id
            LEFT JOIN AddressHouse RegAddressHouse ON RegAddressHouse.id = RegAddress.house_id
            LEFT JOIN AddressHouse LocAddressHouse ON LocAddressHouse.id = LocAddress.house_id
            LEFT JOIN kladr.KLADR ON kladr.KLADR.CODE = RegAddressHouse.KLADRCode
            LEFT JOIN kladr.KLADR AS locKLADR ON locKLADR.CODE = LocAddressHouse.KLADRCode
            LEFT JOIN Diagnostic ON Diagnostic.id = (
              SELECT MAX(D.id)
              FROM Diagnostic AS D
              WHERE D.event_id = Account_Item.event_id
                AND ((D.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code ='2')
                        AND D.person_id = Event.execPerson_id) OR (
                          D.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code='1')))
                          AND D.deleted = 0)
            LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
            LEFT JOIN rbDiagnosticResult ON rbDiagnosticResult.id=Diagnostic.result_id
            LEFT JOIN rbResult AS EventResult ON EventResult.id=Event.result_id
            LEFT JOIN EventType ON EventType.id = Event.eventType_id
            LEFT JOIN rbService AS rbEventService ON rbEventService.id = EventType.service_id
            LEFT JOIN rbService AS rbVisitService ON rbVisitService.id = Visit.service_id
            LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
            LEFT JOIN rbService AS rbItemService ON rbItemService.id = Account_Item.service_id
            LEFT JOIN rbMedicalAidType ON EventType.medicalAidType_id = rbMedicalAidType.id
            LEFT JOIN rbMedicalAidKind ON EventType.medicalAidKind_id = rbMedicalAidKind.id
            LEFT JOIN Diagnostic AS AccDiagnostic ON AccDiagnostic.id = (
             SELECT id FROM Diagnostic AS AD
             WHERE AD.event_id = Account_Item.event_id AND
                AD.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code='9') AND
                AD.person_id = Event.execPerson_id AND
                AD.deleted = 0 LIMIT 1)
            LEFT JOIN Diagnosis AS AccDiagnosis ON
                AccDiagnosis.id = AccDiagnostic.diagnosis_id AND
                AccDiagnosis.deleted = 0
            LEFT JOIN Person ON Person.id = Event.execPerson_id
            LEFT JOIN OrgStructure ON Person.orgStructure_id = OrgStructure.id
            LEFT JOIN rbMedicalAidUnit ON Account_Item.unit_id = rbMedicalAidUnit.id
            LEFT JOIN Contract_Tariff ON Account_Item.tariff_id = Contract_Tariff.id
            LEFT JOIN Account_Item AS OldAccountItem ON OldAccountItem.reexposeItem_id = Account_Item.id
            WHERE
                Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s ORDER BY `Client`.lastName, `Client`.firstName, `Client`.patrName, Event.execDate""" % (sumStr, cond)

        query = db.query(stmt)
        return query

# *****************************************************************************************

    def exportInt(self):
        self.ignoreErrors = self.chkIgnoreErrors.isChecked()
        exportType = self.cmbExportType.currentIndex()

#        lpuName = forceString(QtGui.qApp.db.translate('Organisation', 'id', QtGui.qApp.currentOrgId(), 'fullName'))
        lpuCode = forceString(QtGui.qApp.db.translate('Organisation', 'id', QtGui.qApp.currentOrgId(), 'OGRN'))

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

        file, query, clientsFile = self.prepareToExport(exportType)
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

        if exportType != exportTypeServiceInfo:
            # загружаем информацию о предварительном реестре для формата 2011.10
            self.preliminaryRegistryInfo = self.getPreliminaryInfo()

        if self.idList:
            if exportType == exportTypeServiceInfo:
                out = CServiceInfoXmlStreamWriter(self)
            else:
                out = CMyXmlStreamWriter(self, exportType)
            out.setCodec(QTextCodec.codecForName('cp1251'))

            if exportType == exportType2012:
                clientsOut = CPersonalDataStreamWriter(self)
                clientsOut.setCodec(QTextCodec.codecForName('cp1251'))
                clientsOut.writeFileHeader(clientsFile, self.parent.getFullXmlFileName(), aDate)

            miacCode = forceString(QtGui.qApp.db.translate(
                'Organisation', 'id', QtGui.qApp.currentOrgId(), 'miacCode'))
            accSum = forceDouble(QtGui.qApp.db.translate(
                'Account', 'id', self.parent.accountId, 'sum'))
            if exportType == exportTypeServiceInfo:
                    out.writeFileHeader(file, accDate)
            else:
                out.writeFileHeader(file, self.parent.getFullXmlFileName(),
                        accNumber, aDate, forceString(accDate.year()),
                        forceString(accDate.month()), miacCode, payerCode,
                        accSum)

            while query.next():
                QtGui.qApp.processEvents()
                if self.aborted:
                    break
                self.progressBar.step()

                if exportType == exportTypeServiceInfo:
                    out.writeRecord(query.record())
                else:
                    out.writeRecord(query.record(), miacCode)

                if exportType == exportType2012:
                    clientsOut.writeRecord(query.record())

            out.writeFileFooter()

            if exportType == exportType2012:
                clientsOut.writeFileFooter()
                clientsFile.close()

            file.close()
        else:
            self.log(u'Нечего выгружать.')
            self.progressBar.step()

# *****************************************************************************************

    def createXML(self, exportType):
        outFile = QFile(self.parent.getFullXmlFileName())
        outFile.open(QFile.WriteOnly | QFile.Text)

        outFile2 = None

        if exportType == exportType2012:
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


    @pyqtSignature('')
    def on_btnSelectServiceInfoFileName_clicked(self):
        fileName = QtGui.QFileDialog.getOpenFileName(
            self, u'Укажите файл с данными предварительного счета', self.edtServiceInfoFileName.text(), u'Файлы XML (*.xml)')
        if fileName != '':
            self.edtServiceInfoFileName.setText(QDir.toNativeSeparators(fileName))


    @pyqtSignature('int')
    def on_cmbExportType_currentIndexChanged(self, index):
        enableDateFields = (index in (exportType2013TFOMS,
                                     exportTypeServiceInfo))

        self.edtBegDate.setEnabled(enableDateFields)
        self.edtEndDate.setEnabled(enableDateFields)

        self.edtServiceInfoFileName.setEnabled(
                                               index != exportTypeServiceInfo)
        self.btnSelectServiceInfoFileName.setEnabled(
                                            index != exportTypeServiceInfo)

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
        exportDir = forceString(QtGui.qApp.preferences.appPrefs.get('R53_2012ExportDir', homePath))
        self.edtDir.setText(exportDir)


    def isComplete(self):
        return self.pathIsValid


    def validatePage(self):
        success = False
        fileList = [self.parent.getFullXmlFileName()]
        exportType = self.parent.page1.cmbExportType.currentIndex()

        if exportType == exportType2012:
            fileList.append(self.parent.getFullXmlPersFileName())

        for src in fileList:
            (root, ext) = os.path.splitext(src)
            zipFileName = '%s.zip' % root

            if self.parent.page1.cmbExportType.currentIndex() == exportTypeServiceInfo:
                zipFileName = src
            else:
                if not compressFileInZip(src, zipFileName):
                    break

            dst = os.path.join(forceStringEx(self.edtDir.text()), os.path.basename(zipFileName))
            success, result = QtGui.qApp.call(self, shutil.move, (zipFileName, dst))

            if not success:
                break

        if success:
            QtGui.qApp.preferences.appPrefs['R53_2012ExportDir'] = toVariant(self.edtDir.text())
            QtGui.qApp.preferences.appPrefs['ExportR53_2012RegistryNumber'] = \
                    toVariant(self.parent.page1.edtRegistryNumber.value())
            self.wizard().setAccountExposeDate()

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
                u'Выберите директорий для сохранения файла выгрузки в ОМС Новгородской области',
                 forceStringEx(self.edtDir.text()),
                 QtGui.QFileDialog.ShowDirsOnly)
        if forceString(dir):
             self.edtDir.setText(QDir.toNativeSeparators(dir))

# *****************************************************************************************

class CMyXmlStreamWriter(QXmlStreamWriter, CExportHelperMixin):
    def __init__(self, parent, exportType):
        QXmlStreamWriter.__init__(self)
        CExportHelperMixin.__init__(self)
        self.parent = parent
        self.setAutoFormatting(True)
        self.recNum = 1
        self.caseNum = 1
        self.serviceNum = 1
        self._lastClientId = None
        self.serviceDetailCache = CServiceDetailCache()
        self.exportType = exportType


    def writeTextElement(self, element,  value, writeEmtpyTag = True):
        if not writeEmtpyTag and (not value or value == ''):
            return

        QXmlStreamWriter.writeTextElement(self, element, value)


    def writeRecord(self, record, miacCode):
        clientId = forceRef(record.value('client_id'))
        age = forceInt(record.value('clientAge'))
#        specialCase = []
        birthDate = forceDate(record.value('birthDate'))
        eventId = forceInt(record.value('event_id'))

        if self._lastClientId != clientId: # новая запись, иначе - новый случай
            if self._lastClientId:
                self.recNum += 1
                self.writeEndElement() # ZAP

            # отключаем группировку случаев для 2013 ТФОМС
            if self.exportType != exportType2013TFOMS:
                self._lastClientId = clientId

            self.writeStartElement('ZAP')

            self.writeTextElement('N_ZAP', ('%4d' % self.recNum).strip())

            if self.exportType == exportType2012:
                self.writeTextElement('PR_NOV', '1' if forceRef(record.value('oldAccItemId')) else  '0')

            self.writeStartElement('PACIENT')

            if self.exportType == exportType2012:
                self.writeTextElement('ID_PAC',  ('%d' % clientId)[:36])

            # Региональный код справочника ВИДЫ ПОЛИСОВ.
            self.writeTextElement('VPOLIS', forceString(record.value('policyKindFederalCode'))[:1])
            self.writeTextElement('SPOLIS', forceString(record.value(u'policySerial'))[:10])
            self.writeTextElement('NPOLIS', forceString(record.value(u'policyNumber'))[:20])

            if self.exportType == exportType2012:
                self.writeTextElement('SMO', '53%s' % forceString(record.value('insurerMiac'))[:5])
                self.writeTextElement('SMO_OGRN', forceString(record.value('insurerOGRN'))[:15])
                self.writeTextElement('SMO_OK', forceString(record.value('insurerOKATO'))[:5])
                self.writeTextElement('SMO_NAME', forceString(record.value('insurerName'))[:100], writeEmtpyTag = False)
            elif self.exportType == exportType2013TFOMS:
                self.writeTextElement('OKATO_OMS', forceString(record.value('insurerOKATO'))[:5])
                self.writeTextElement('C_OGRN', forceString(record.value('insurerOGRN'))[:15], writeEmtpyTag = False)
                # Фамилия пациента
                self.writeTextElement('FAM', forceString(record.value('lastName'))[:40])
                # Имя пациента
                self.writeTextElement('IM', forceString(record.value('firstName'))[:40])
                # Отчество пациента
                self.writeTextElement('OT', forceString(record.value('patrName'))[:40], writeEmtpyTag = False)
                # Пол пациента
                self.writeTextElement('W', forceString(record.value('sex'))[:1])
                # Дата рождения пациента
                self.writeTextElement('DR', forceDate(record.value('birthDate')).toString(Qt.ISODate))
                info = self.getClientRepresentativeInfo(clientId)

                if info != {}:
                    # Фамилия представителя пациента
                    self.writeTextElement('FAM_P', info.get('lastName')[:40], writeEmtpyTag = False)
                    # Имя представителя пациента
                    self.writeTextElement('IM_P', info.get('firstName')[:40], writeEmtpyTag = False)
                    # Отчество представителя пациента
                    self.writeTextElement('OT_P', info.get('patrName')[:40],  writeEmtpyTag = False)
                    # Пол представителя пациента
                    self.writeTextElement('W_P',  forceString(info.get('sex'))[:1], writeEmtpyTag = False)
                    # Дата рождения представителя пациента
                    self.writeTextElement('DR_P', info.get('birthDate').toString(Qt.ISODate))

                # Место рождения пациента или представителя
                self.writeTextElement('MR', forceString(record.value('birthPlace'))[:100], writeEmtpyTag = False)
                # Тип документа, удостоверяющего личность пациента или представителя
                self.writeTextElement('DOCTYPE', forceString(record.value('documentFederalCode'))[:2], writeEmtpyTag = False)
                # Серия документа, удостоверяющего личность пациента или представителя
                self.writeTextElement('DOCSER', forceString(record.value('documentSerial'))[:10], writeEmtpyTag = False)
                # Номер документа, удостоверяющего личность пациента или представителя
                self.writeTextElement('DOCNUM', forceString(record.value('documentNumber'))[:20], writeEmtpyTag = False)
                # СНИЛС
                self.writeTextElement('SNILS', forceString(record.value('SNILS'))[:14], writeEmtpyTag = False)
                # Код места жительства по ОКАТО
                self.writeTextElement('OKATOG',  forceString(record.value('placeOKATO'))[:11], writeEmtpyTag = False)
                # Код места пребывания по ОКАТО
                #self.writeTextElement('OKATOP', forceString(record.value('locPlaceOKATO'))[:11], writeEmtpyTag = False)

            self.writeTextElement('NOVOR', '0')#if age > 0 else '%s%s0' % (forceString(record.value('sex'))[:1], birthDate.toString('ddMMyy')))
            self.writeEndElement() # PACIENT

        self.writeStartElement('SLUCH')
#        idCase = eventId if self.exportType == exportType2013TFOMS else self.caseNum
        self.writeTextElement('IDCASE', '%d' % eventId)
        # Федеральный код справочника НАЗНАЧЕНИЕ ТИПА СОБЫТИЯ
        self.writeTextElement('USL_OK',  forceString(record.value('medicalAidTypeFederalCode')))

        if self.exportType == exportType2012:
            self.writeTextElement('VIDPOM', forceString(record.value('medicalAidKindFederalCode')))
            #self.writeTextElement('NPR_MO','')
            # 1 – плановая; 2 – экстренная ИЗ СОБЫТИЯ
            self.writeTextElement('EXTR', '2' if forceInt(record.value('order')) in(2, 6) else '1')
            #self.writeTextElement('PODR', '')

        self.writeTextElement('LPU', '530%s' % miacCode[:6])

        personId = forceRef(record.value('execPersonId'))
        serviceId = forceRef(record.value('serviceId'))
        serviceDetail = self.serviceDetailCache.get(serviceId)
        specialityId = self.getPersonSpecialityId(personId)
        mkb = forceString(record.value('MKB'))
        sex = forceInt(record.value('sex'))
        ageTuple = calcAgeTuple(birthDate, forceDate(record.value('endDate')))

        (medicalAidProfileId, medicalAidKindId, medicalAidTypeId) = \
            serviceDetail.getMedicalAidIds(specialityId, sex, ageTuple, mkb)
        medicalAidProfileFederalCode = self.getMedicalAidProfileFederalCode(medicalAidProfileId)[:3]
        kindList = self.getMedicalAidProfileRegionalCode(medicalAidProfileId).split('.', 1)
        profileKind = '' if len(kindList) < 2 else kindList[1]

        self.writeTextElement('PROFIL', medicalAidProfileFederalCode)
        self.writeTextElement('PROFIL_KIND', profileKind, writeEmtpyTag=False)

        if self.exportType == exportType2012:
            self.writeTextElement('DET', (u'1' if age < 18 else u'0'))
            self.writeTextElement('HOSP_PARENT', (u'1' if self.getServiceCode(serviceId)[-3:] == 'zsg' else '0'))
            self.writeTextElement('DISP_14', '0')
            self.writeTextElement('NHISTORY', forceString(record.value('eventId'))[:50])

        # Дата начала события
        self.writeTextElement('DATE_1', forceDate(record.value('begDate')).toString(Qt.ISODate))
        # Дата окончания события
        self.writeTextElement('DATE_2', forceDate(record.value('endDate')).toString(Qt.ISODate))

        if self.exportType == exportType2012:
            self.writeTextElement('DS1', mkb)
            self.writeTextElement('DS2', forceString(record.value('AccMKB')), writeEmtpyTag = False)
            self.writeTextElement('RSLT', forceString(record.value('eventResultFederalCode')))
            # Федеральный код из справочника РЕЗУЛЬТАТ ОСМОТРА. Результат ЗАКЛЮЧИТЕЛЬНОГО ДИАГНОЗА.
            self.writeTextElement('ISHOD', forceString(record.value('resultFederalCode')))
            self.writeTextElement('PRVS', forceString(self.parent.getPersonSpecialityFederalCode(personId)))
            self.writeTextElement('IDDOKT', forceString(self.parent.getPersonFederalCode(personId)))

            if forceString(record.value('patrName')) == '':
                self.writeTextElement('OS_SLUCH', '2', writeEmtpyTag = False)

            self.writeTextElement('IDSP', forceString(record.value('medicalAidUnitFederalCode')))

        self.writeTextElement('ED_COL', forceString(record.value('amount')))

        if self.exportType == exportType2012:
            price = forceDouble(record.value('price'))
            sum = forceDouble(record.value('sum'))

            self.writeTextElement('TARIF', ('%10.2f' % price).strip().replace('.',','))
            self.writeTextElement('SUMV', ('%10.2f' % sum).strip().replace('.',','))

        if self.exportType != exportType2013TFOMS:
            # Работа со словарем данных о предварительном реестре
            visitId = forceInt(record.value('visit_id'))
            actionId = forceInt(record.value('action_id'))
            key = (eventId, serviceId, visitId, actionId)
            (pAccNum, pAccDate, pRecNum) = \
                self.parent.preliminaryRegistryInfo.get(key, ('', '', ''))
            # номер предварительного реестра (порядковый номер счёта, в клиенте)
            self.writeTextElement('PREPARE_ACC', pAccNum)
            # дата предварительного реестра (дата экспорта)
            self.writeTextElement('PREPARE_DATE', pAccDate)
            # номер позиции предварительного реестра (значение поля <N_PP>, в предварительном реестре)
            self.writeTextElement('PREPARE_NUM', pRecNum)

        if self.exportType == exportType2012:
            federalSum = forceDouble(record.value('federalSum'))
            federalPrice = forceDouble(record.value('federalPrice'))

            regionalSum = forceDouble(record.value('regionalSum'))
            regionalPrice = forceDouble(record.value('regionalPrice'))

            self.writeService(record, miacCode, age, price-federalPrice-regionalPrice,
                              sum-federalSum-regionalSum, '1', medicalAidProfileFederalCode,
                              profileKind, personId, mkb)

            if federalPrice > 0:
                self.writeService(record, miacCode, age, federalPrice,
                                  federalSum, '2', medicalAidProfileFederalCode,
                                  profileKind, personId, mkb)

            if regionalPrice > 0:
                self.writeService(record, miacCode, age, regionalPrice,
                                  regionalSum, '3', medicalAidProfileFederalCode,
                                  profileKind, personId, mkb)

            self.exportNomenclativeServices(eventId, mkb, personId, sex, age, record, miacCode, ageTuple)
            self.serviceNum = 1

        self.caseNum+= 1
        self.writeEndElement() # SLUCH

        if self.exportType == exportType2013TFOMS:
            self.recNum += 1
            self.writeEndElement() # ZAP



    def exportNomenclativeServices(self, eventId, eventMKB, eventPersonId, sex, age, record,  miacCode, ageTuple):
        db = QtGui.qApp.db
        table = db.table('Action')
        actionList = db.getRecordList(table, where=[table['event_id'].eq(eventId)])

        for r in actionList:
            action = CAction(record=r)
            actionType = action.getType()
            serviceId = actionType.nomenclativeServiceId

            if serviceId:
                serviceDetail = self.serviceDetailCache.get(serviceId)
                personId = forceRef(record.value('setPerson_id'))
                specialityId = self.getPersonSpecialityId(personId)
                mkb = forceString(record.value('MKB'))

                if not mkb:
                    mkb = eventMKB

                if not personId:
                    personId = eventPersonId

                (medicalAidProfileId, medicalAidKindId, medicalAidTypeId) = \
                    serviceDetail.getMedicalAidIds(specialityId, sex, ageTuple, mkb)

                kindList = self.getMedicalAidProfileRegionalCode(medicalAidProfileId).split('.', 1)
                profileKind = '' if len(kindList) < 2 else kindList[1]
                self.writeService(record, miacCode, age, 0, 0,
                                  serviceDetail.infisCode, self.getMedicalAidProfileFederalCode(medicalAidProfileId),
                                  profileKind, personId, mkb)


    def writeService(self, record, miacCode, age, price, sum,
                     code,  medicalAidProfileFederalCode,  profileKind,
                     personId,  mkb):
#        serviceId = forceRef(record.value('serviceId'))
        self.writeStartElement('USL')
        self.writeTextElement('IDSERV',  ('%8d' % self.serviceNum).strip()) # O N(8) номер записи в реестре услуг
        self.writeTextElement('LPU', '530%s' % miacCode[:6]) #O Т(6) Код МО МО лечения
        #self.writeTextElement('LPU_1', forceString(record.value('orgStructureCode'), writeEmtpyTag = False) #У Т(6) Подразделение МО Подразделение МО лечения из регионального справочника
        self.writeTextElement('PODR', forceString(record.value('orgStructureCode')), writeEmtpyTag = False) #У N(8) Код отделения Отделение МО лечения из регионального справочника
        self.writeTextElement('PROFIL', medicalAidProfileFederalCode) #O N(3) Профиль Классификатор V002
        self.writeTextElement('PROFIL_KIND', profileKind, writeEmtpyTag=False)
        self.writeTextElement('DET', (u'1' if age < 18 else u'0')) #О N(1) Признак детского профиля 0-нет, 1-да.
        self.writeTextElement('DATE_IN', forceDate(record.value('begDate')).toString(Qt.ISODate)) #O D Дата начала оказания услуги
        self.writeTextElement('DATE_OUT', forceDate(record.value('endDate')).toString(Qt.ISODate)) #O D Дата окончания оказания услуги
        self.writeTextElement('DS', mkb) #O Т(10) Диагноз Код из справочника МКБ до уровня подрубрики
        self.writeTextElement('CODE_USL', code) #O Т(16) Код услуги Территориальный классификатор услуг
        self.writeTextElement('KOL_USL', ('%6.2f' % forceDouble(record.value('amount'))).strip().replace('.',',')) #O N(6.2) Количество услуг (кратность услуги)
        self.writeTextElement('TARIF', ('%15.2f' % price).strip().replace('.',',')) #O N(15.2) Тариф
        self.writeTextElement('SUMV_USL', ('%15.2f' % sum).strip().replace('.',',')) #O N(15.2) Стоимость медицинской услуги, выставленная к оплате (руб.)
        self.writeTextElement('PRVS', forceString(self.parent.getPersonSpecialityFederalCode(personId))) # - специальность работника выполнившего действие.
        self.writeTextElement('CODE_MD', self.getPersonFederalCode(personId)) # - федеральный код работника выолнившего действи
        self.writeEndElement() #USL
        self.serviceNum += 1


    def writeFileHeader(self,  device, fileName, accNumber, accDate, year, month, miacCode, payerCode, accSum=0.0):
        self._lastClientId = None
        self.recNum = 1
        self.caseNum = 1
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
        self.writeStartElement('SCHET')
        self.writeTextElement('CODE', ('53%s%s' % (miacCode, accNumber))[:8])

        if self.exportType == exportType2012:
            self.writeTextElement('CODE_MO',  u'530%s' % miacCode)

        self.writeTextElement('YEAR', year)
        self.writeTextElement('MONTH',  month)
        self.writeTextElement('NSCHET',  forceString(accNumber))
        self.writeTextElement('DSCHET', accDate.toString(Qt.ISODate))

        if self.exportType == exportType2012:
            self.writeTextElement('PLAT', '53%s' % payerCode[:5], writeEmtpyTag = False)
            self.writeTextElement('SUMMAV', ('%15.2f' % accSum).strip().replace('.',','))

        self.writeEndElement()


    def writeFileFooter(self):
        self.writeEndElement() # root
        self.writeEndDocument()

# *****************************************************************************************

class CPersonalDataStreamWriter(QXmlStreamWriter):
    def __init__(self, parent):
        QXmlStreamWriter.__init__(self)
        self.parent = parent
        self.setAutoFormatting(True)
        self._clientsSet = None


    def writeTextElement(self, element,  value, writeEmtpyTag = True):
        if not writeEmtpyTag and (not value or value == ''):
            return

        QXmlStreamWriter.writeTextElement(self, element, value)


    def writeRecord(self, record):
        clientId = forceRef(record.value('client_id'))
        sex = forceString(record.value('sex'))
        birthDate = forceDate(record.value('birthDate'))

        if clientId in self._clientsSet:
            return

        self.writeStartElement('PERS')
        self.writeTextElement('ID_PAC',  ('%d' % clientId)[:36])

        #Фамилия пациента.
        self.writeTextElement('FAM', forceString(record.value('lastName')))
        #Имя пациента
        self.writeTextElement('IM', forceString(record.value('firstName')))
        #Отчество пациента
        patrName = forceString(record.value('patrName'))
        self.writeTextElement('OT', patrName if patrName else u'НЕТ')
        #Пол пациента.
        self.writeTextElement('W', sex)
        #Дата рождения пациента.
        self.writeTextElement('DR', birthDate.toString(Qt.ISODate))
        self.writeTextElement('MR', forceString(record.value('birthPlace')), writeEmtpyTag=False)
        # Федеральный код из справочника ТИПЫ ДОКУМЕНТОВ. Из карточки пациента.
        self.writeTextElement('DOCTYPE',  forceString(record.value('documentFederalCode')))
        # Серия документа, удо-стоверяющего личность пациента.
        self.writeTextElement('DOCSER', forceString(record.value('documentSerial')))
        # Номер документа, удостоверяющего личность пациента.
        self.writeTextElement('DOCNUM', forceString(record.value('documentNumber')))
        # СНИЛС пациента.
        self.writeTextElement('SNILS', formatSNILS(forceString(record.value('SNILS'))))
        # Код места жительства по ОКАТО. Берётся из адреса жительство.
        locPlaceOKATO = forceString(record.value('locPlaceOKATO'))

        if not locPlaceOKATO:
            locPlaceOKATO = forceString(record.value('placeOKATO'))

        if locPlaceOKATO:
            self.writeTextElement('OKATOG', locPlaceOKATO.ljust(11,'0'))
        else:
            self.parent.log(u'У пациента %d отсутствует'
                                    u' ОКАТО адреса проживания' % (clientId))

        # Код места пребывания по ОКАТО. Берётся из адреса регистрации
        placeOKATO = forceString(record.value('placeOKATO'))

        if placeOKATO:
            self.writeTextElement('OKATOP', placeOKATO.ljust(11,'0'))
        else:
            self.parent.log(u'У пациента %d отсутствует'
                                    u' ОКАТО адреса регистрации' % (clientId))

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

# *****************************************************************************************
