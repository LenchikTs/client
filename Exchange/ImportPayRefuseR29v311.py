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
u"""Импорт отказов для Архангельска"""

import os.path

from PyQt4 import QtGui
from PyQt4.QtCore import (Qt, QDate, QFile, pyqtSignature, QDir,
                          QXmlStreamWriter, QDateTime)

from library.Utils import (forceDate, forceDouble, forceInt, forceRef,
                           forceString, forceStringEx, toVariant)
from Accounting.Utils import updateAccounts, updateDocsPayStatus
from Events.Utils import CPayStatus, getPayStatusMask
from Exchange.Cimport import CXMLimport

from Exchange.Export29XMLCommon import Export29XMLCommon
from Exchange.XmlStreamReader import CXmlStreamReader
from Exchange.Utils import tbl, compressFileInZip

from Exchange.Ui_ImportPayRefuseR29 import Ui_Dialog


def ImportPayRefuseR29Native(widget, accountId, accountItemIdList):
    dlg = CImportPayRefuseR29Native(widget, accountId, accountItemIdList)
    prefs = QtGui.qApp.preferences.appPrefs
    dlg.edtFileName.setText(forceString(prefs.get(
        'ImportPayRefuseR29FileName', '')))
    dlg.edtConfirmationDir.setText(forceString(prefs.get(
        'ImportPayRefuseR29ConfirmationDir', '')))
    dlg.cmbChief.setValue(forceRef(prefs.get('ImportPayRefuseR29ChiefId', '')))
    dlg.cmbDelegate.setValue(forceRef(prefs.get(
        'ImportPayRefuseR29DelegateId', '')))
    dlg.exec_()
    prefs['ImportPayRefuseR29FileName'] = toVariant(dlg.edtFileName.text())
    prefs['ImportPayRefuseR29ConfirmationDir'] = toVariant(
        dlg.edtConfirmationDir.text())
    prefs['ImportPayRefuseR29ChiefId'] = toVariant(dlg.cmbChief.getValue())
    prefs['ImportPayRefuseR29DelegateId'] = toVariant(
        dlg.cmbDelegate.getValue())


class CImportPayRefuseR29Native(QtGui.QDialog, Ui_Dialog, CXMLimport):
    GROUP_NAMES = {
        'ZL_LIST' : ('ZGLV', 'SCHET', 'ZAP'),
        'ZAP': ('PACIENT', 'Z_SL'),
        'Z_SL': ('SL','DSVED'),
        'SL': ('USL', 'SANK','CONS', 'ONK_SL','DS2_N','NAPR','NAZ', 'LEK_PR'),
        'ONK_SL':('ONK_USL','B_DIAG','B_PROT'),
        'ONK_USL':('LEK_PR'),
        'USL': ('KSLP','DENTES', 'MR_USL_N', 'MED_DEV'),
        'KSLP': ('SL_KOEF'),
        'DENTES': ('DENT'),
        'DENT': ('SURFACES'),
        'KSLP': ('SL_KOEF'),
        'LEK_PR':('LEK_DOSE')
    }

    def __init__(self, parent, accountId, accountItemIdList):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        CXMLimport.__init__(self, self.log)
        self.cmbChief.setOrgStructureId(QtGui.qApp.currentOrgStructureId())
        self.cmbChief.setSpecialityPresent(False)
        self.cmbDelegate.setOrgStructureId(QtGui.qApp.currentOrgStructureId())
        self.cmbDelegate.setSpecialityPresent(False)

        self.accountId = accountId
        self.accountItemIdList = accountItemIdList
        self.progressBar.setFormat('%p%')
        self.checkName()
        self.errorPrefix = ''
        self.nProcessed = 0
        self.nPayed = 0
        self.nRefused = 0
        self.nNotFound = 0
        self.tableAccountItem = tbl('Account_Item')
        self.tableEvent = tbl('Event')
        self.tableAccount = tbl('Account')
        self.tableAcc = self.db.join(self.tableAccountItem, self.tableAccount,
                                     'Account_Item.master_id=Account.id')
        self.prevContractId = None
        self.financeTypeOMS = forceRef(self.db.translate(
            'rbFinance', 'code', '2', 'id'))
        self.refuseTypeIdCache = {}
        self.insurerCache = {}
        self.policyKindIdCache = {}
        self.policyTypeTerritorial = forceRef(self.db.translate(
            'rbPolicyType', 'code', '1', 'id'))
        self.policyTypeIndustrial = forceRef(self.db.translate(
            'rbPolicyType', 'code', '2', 'id'))
        self.confirmation = ''
        self.fileName = ''
        self.reader = CXmlStreamReader(self, self.GROUP_NAMES, 'ZL_LIST',
                                       self.log, 'ZAP')
        self._clientCredentialsCache = {}
        self._contractCache = {}
        self._financeCache = {}
        self._personListCache = {}
        self._refuseReasonCache = {}

        self._parent = parent
        self._onlyCurrentAccount = False
        self._isLookupRelevantSet = False
        self._accountNumber = None
        self._sumPayed = 0
        self._sumExposed = 0
        self._isAnySanctions = False
        self._accountIdSet = set()
        self.__acts = {}


    @pyqtSignature('')
    def on_btnImport_clicked(self):
        CXMLimport.on_btnImport_clicked(self)

    @pyqtSignature('')
    def on_btnSelectFile_clicked(self):
        oldFileName = forceString(self.edtFileName.text()).split('|')[0]
        files = QtGui.QFileDialog.getOpenFileNames(
            self, u'Укажите файлы с данными', oldFileName, u'Файлы XML (*.xml)')
        if files:
            files = '|'.join(forceString(
                QDir.toNativeSeparators(x)) for x in files)
            self.edtFileName.setText(files)
            self.checkName()


    @pyqtSignature('')
    def on_btnSelectConfirmationDir_clicked(self):
        dir = QtGui.QFileDialog.getExistingDirectory(
            self, u'Укажите каталог для сохранения подтверждений',
            self.edtConfirmationDir.text())
        if dir:
            self.edtConfirmationDir.setText(QDir.toNativeSeparators(dir))


    @pyqtSignature('')
    def on_btnManualConfirmation_clicked(self):
        files = forceStringEx(self.edtFileName.text()).split('|')
        for fileName in files:
            if fileName:
                self.writeConfirmation(fileName[:-4])


    @pyqtSignature('int')
    def on_cmbChief_currentIndexChanged(self, _):
        self.checkName()


    @pyqtSignature('int')
    def on_cmbDelegate_currentIndexChanged(self, _):
        self.checkName()

    def checkName(self):
        self.btnManualConfirmation.setEnabled(
            self.edtFileName.text() != '' and bool(self.cmbChief.getValue()) and
            bool(self.cmbDelegate.getValue()))
        CXMLimport.checkName(self)


    def err2log(self, e):
        self.log.append(self.errorPrefix + e)


    def startImport(self):
        self.insurerCache = {}
        files = forceStringEx(self.edtFileName.text()).split('|')
        self.confirmation = forceStringEx(self.edtConfirmation.text())
        self._onlyCurrentAccount = self.chkOnlyCurrentAccount.isChecked()
        self._isLookupRelevantSet = self.chkProcessRelevant.isChecked()
        self._chkImportInsurance = self.chkImportInsurance.isChecked()

        if not self.confirmation and self._chkImportInsurance == False:
            self.log.append(u'нет подтверждения')
            return

        self.prevContractId = None
        self._accountIdSet = set()
        self.__acts = {}
        totalProcessed = 0
        report = {}

        for fileName in files:
            self.nProcessed = 0
            self.nPayed = 0
            self.nRefused = 0
            self.nNotFound = 0
            txtFile = QFile(fileName)
            if not txtFile.open(QFile.ReadOnly | QFile.Text):
                self.err2log(u'Ошибка открытия файла {0} для чтения: {1}'
                             .format(fileName,
                                     forceString(txtFile.errorString())))
                continue

            self.labelNum.setText(u'размер источника: {0}'.format(txtFile.size()))
            self.progressBar.setFormat('%p%')
            self.progressBar.setMaximum(txtFile.size() - 1)

            if self.readFile(txtFile) and self.nProcessed and self._chkImportInsurance == False:
                self.writeConfirmation(self.fileName)
            if self.nProcessed:
                key = (u'загружен успешно. Оплачен частично. В счете есть отказанные позиции' if self.nRefused
                       else u'загружен успешно. В счете все позиции оплачены')
            else:
                key = u'не загружен'
            report.setdefault(key, []).append(fileName)
            self.err2log(u'---------------------------------')
            self.stat.setText(u'обработано: {0}; оплаченых: {1}; отказаных: {2}; '
                              u'не найдено: {3}'.format(
                                  self.nProcessed, self.nPayed, self.nRefused,
                                  self.nNotFound))
            totalProcessed += self.nProcessed
            txtFile.close()

        self.errorPrefix = ''

        if not totalProcessed and self._onlyCurrentAccount:
            self.err2log(u'Нет данных для текущего счета.')

        updateAccounts(self._accountIdSet)
        self.__createControlResultRecord()

        for key in report:
            self.err2log(u'{0}:'.format(key))
            for fileName in report[key]:
                self.err2log(u'`{0}`'.format(fileName))
            self.err2log(u'---------------------------------')


    def readFile(self, device):
        self.reader.setDevice(device)
        result = False
        if self.reader.readHeader():
            for name, row in self.reader.readData():
                if name == 'ZGLV':
                    self.fileName = row.get('FILENAME', '-')
                if name == 'SCHET':
                    self._accountNumber = row.get('NSCHET', '-')
                    if self._onlyCurrentAccount:
                        date = row.get('DSCHET', QDate())
                        _id = self.findAccount(self._accountNumber, date)
                        if self.accountId != _id:
                            self.errorPrefix = ''
                            self.err2log(u'Пропускаем счёт `{0}`.'.format(
                                self._accountNumber))
                            return False
                elif name == 'ZAP':
                    result = self.processXmlRecord(row)
                elif name == 'ACT_DATA':
                    number = row.get('ACT_NUM', '-')
                    date = row.get('ACT_DATE', QDate())
                    name = row.get('ACT_NAME', '-')
                    self.__acts[self.accountId] = (date, number, name)
                self.progressBar.setValue(device.pos())
                QtGui.qApp.processEvents()

            if self.reader.hasError() or self.abort:
                self.err2log(self.reader.errorString())

        return result

    def findAccount(self, number, date):
        record = self.db.getRecordEx(self.tableAccount, 'id',
            [self.tableAccount['number'].eq(number),
             self.tableAccount['date'].eq(date),
             self.tableAccount['deleted'].eq(0)])
        return forceRef(record.value(0)) if record else None


    def getRefuseReasonText(self, code):
        result = self._refuseReasonCache.get(code, -1)

        if result == -1:
            result = forceString(self.db.translate('rbPayRefuseType', 'code',
                                                   code, 'name'))
            self._refuseReasonCache[code] = result

        return result

    def processXmlRecord(self, row):
        clientInfo = row.get('PACIENT', {})
        clientId = forceInt(clientInfo.get('ID_PAC'))


        if not clientId:
            self.err2log(u'Поле ID_PAC не заполнено!')
            return False
        if not self.db.getRecord('Client', 'id', clientId):
            self.err2log(u'Пациент с id=%d не найден в БД.' % clientId)
            return False
        eventInfo = row.get('Z_SL', {})
        eventList = row.get('Z_SL', {}).get('SL', [])
        if isinstance(eventList, dict):
            eventList = [eventList]
        sankIt = forceDouble(eventInfo.get('SANK_IT', 0))
        refuseCode = forceInt(eventInfo.get('REFREASON'))
        self._sumPayed = forceDouble(eventInfo.get('SUMP', 0.0))
        self._sumExposed = forceDouble(eventInfo.get('SUMV', 0.0))
        attachCode = clientInfo.get('MCOD_RPN')
        for event in eventList:
            eventId = forceString(event.get('SID_MIS'))
            if not eventId:
                self.err2log(u'Поле NHISTORY не заполнено!')
                return False
            if self._chkImportInsurance:
                self.checkClient(clientInfo, eventId, clientId)

            else:
                self.processEvent(event, clientId, eventId, refuseCode, sankIt,
                                  attachCode)
        return True
        return True


    def checkClient(self, row, eventId, clientId):
        note = []
        self.nProcessed += 1
        policyNumber = forceString(row.get('NPOLIS'))
        policySerial = forceString(row.get('SPOLIS'))
        policyKindId = self.getPolicyKindId(forceString(row.get('VPOLIS')))
        policyBegDate  = forceDate(QtGui.qApp.db.translate(
            'Event', 'id', eventId , 'setDate'))
        if not policySerial and not policyNumber:
            msg = u'Пациент {0} Отсутствуют данные о полисе'.format(clientId)
            self.err2log(msg)
            note.append(msg)
        if str(forceString(row.get('MCOD_RPN'))):
            msg = u'Пациент {0} МО прикрепления на момент оказания услуги {1}'.format(clientId,
                forceString(row.get('MCOD_RPN')))
            if msg not in note:
                note.append(msg)
        insurerOGRN = forceString(row.get('SMO_OGRN'))
        insurerOKATO = forceString(row.get('SMO_OK'))
        insurerId = None
        smo = forceString(row.get('SMO'))
        if smo:
            insurerId = forceString(QtGui.qApp.db.translate(
                'Organisation', 'miacCode', smo, 'id'))
        elif not insurerOGRN and not insurerOKATO:
            msg = u'Пациент %s Не указано ОГРН и ОКАТО'%clientId
            self.err2log(msg)
            note.append(msg)
        else:
            insurerId = self.findInsurerByOGRNandOKATO(insurerOGRN,
                                                       insurerOKATO)
        if insurerId:
            eventBegDate = forceDate(self.db.translate(
                'Event', 'id', eventId, 'setDate'))
            eventEndDate = forceDate(self.db.translate(
                'Event', 'id', eventId, 'execDate'))
            isPolicyUpdated = self.updateClientPolicy(
                clientId, insurerId, policySerial, policyNumber, policyBegDate,
                insurerOGRN, policyKindId, eventBegDate, eventEndDate)
            if isPolicyUpdated:
                self.closeOpenedPolicy(clientId, eventBegDate)
        else:
            msg = u'Пациент {0} СМО с ОГРН {1} и ОКАТО {2} не найдена'.format(clientId,
                insurerOGRN, insurerOKATO)
            self.err2log(msg)
            note.append(msg)
            tblClient = tbl('Client')
            client = self.db.getRecord(tblClient, '*', clientId)
            clientNote = list(note)
            clientNote.append(forceString(client.value(u'notes')))
            clientNote.append(u'СТРАХОВАЯ ПРИНАДЛЕЖНОСТЬ НЕ ОПРЕДЕЛЕНА.'
                              u' ПРОВЕРЬТЕ ПЕРСОНАЛЬНЫЕ ДАННЫЕ')
            noteStr = ';'.join(i for i in clientNote)
            client.setValue(u'notes', noteStr)
            self.db.updateRecord(tblClient, client)
        if eventId == '1357146':
                pass
        contractId, oldContractId, k, isAmbiguitous, contractName = (
                self.getContract(eventId))
        if contractId == 'flag':
            note.append(u'Не удалось подобрать договор')

        if contractId == 'flag':
            note.append(u'Не удалось подобрать договор')

        if oldContractId != contractId and contractId:
            eventInfo = self.db.getRecord(self.tableEvent, '*', eventId)
            if eventInfo:
                msg  = u'Произошла смена договора после подгрузки файла %s;'%(unicode(self.edtFileName.text()))
                eventInfo.setValue('contract_id', toVariant(contractId))
                eventNote = {}
                notes = []
                notes.append(msg)
                eventNote = list(notes)
                eventNote.append(forceString(eventInfo.value(u'note')))
           #     eventNote.append(u'Произошла смена договора после подгрузки файла %s;'%(unicode(self.edtFileName.text())))
                noteStr = ';'.join(i for i in eventNote)
                eventInfo.setValue(u'note', noteStr)
                self.db.updateRecord(self.tableEvent, eventInfo)
                note.append(u'Произошла смена договора')
        if k > 1:
            note.append(u'Попадает под действие нескольких договоров '
                            u'{0}'.format(u', '.join(contractName)))
        if isAmbiguitous > 1:
            note.append(u'В рег. карте имеются пересекающиеся по датам '
                            u'действия прикрепления/полисы')
     #   return note


    def processEvent(self, event, clientId, eventId, refuseCode, sankIt, # note,
                     attachCode):
        refuseText = []
        refusedSum = 0
        refuseCode = 0
        note = []
        self._isAnySanctions = event.has_key('SANK')
        sankList = event.get('SANK')
        if sankList and sankIt > 0:
            if isinstance(sankList, dict):
                sankList = [sankList]
            for sank in sankList:
                refusedSum += forceDouble(sank.get('S_SUM', 0.0))
                if sank:
                    refuseCode = int(sank.get('S_OSN'))
                    refuseText.append(self.getRefuseReasonText(refuseCode))

        self.errorPrefix = u'Элемент ID_PAC={0}: '.format(clientId)
        prevEventId = forceRef(QtGui.qApp.db.translate(
            'Event', 'id', eventId, 'prevEvent_id'))
        accountItemIdList = []
        serviceList = event.get('USL', [])
        comment = forceString(event.get('COMENTSL'))
        if comment:
            note.append(comment)
        if isinstance(serviceList, dict):
            serviceList = [serviceList]

        isListParsed = False

        for service in serviceList:
            accountItemIdList, isListParsed = self.processService(
                service, clientId, eventId, accountItemIdList, attachCode,
                refuseCode, note)
            if prevEventId:
                accountItemIdList, flag = self.processService(
                    service, clientId, prevEventId, accountItemIdList,
                    attachCode, refuseCode, note)
                if flag:
                    isListParsed = True

        refuseText = ';'.join(refuseText)

        if not isListParsed or accountItemIdList:
            self.processAccountItemIdList(
                accountItemIdList, refuseCode, refuseText, note, refusedSum)


    def processService(self, row, clientId, eventId, accountItemIdList,
                       attachCode, refuseCode, note):
        accountItemId = row.get('UID_MIS')
        codeUsl = forceString(row.get('CODE_USL')).split(":")[0]
        sumUsl = forceDouble(row.get('ST_USL' if 'ST_USL' in row.keys()
                                     else 'SUMV_USL'))
    #    note = row.get('COMENTSL')

        if accountItemId and not self._onlyCurrentAccount:
            self.processAccountItem(accountItemId, eventId, codeUsl,
                                    attachCode, clientId, refuseCode, sumUsl, note)
            return accountItemIdList, True

        return self.getAccountItemIdListByClientAndEvent(
            clientId, eventId, codeUsl, sumUsl, accountItemIdList), False


    def processAccountItem(self, accountItemId, eventId, serviceCode,
                           attachCode, clientId, refuseCode, sumUsl, notes):
        u"""Обрабатывает элемент реестра счета, указанный в поле UID_MIS"""
        record = self.db.getRecord(self.tableAccountItem, '*', accountItemId)
        QtGui.qApp.processEvents()

        if not record and self._isLookupRelevantSet:
            accountItemId = self.findAccountItem(eventId, serviceCode)
            record = self.db.getRecord(self.tableAccountItem, '*',
                                       accountItemId)

        if not record:
            self.err2log(u'IDCASE={0}, CODE_USL={1}, UID_MIS={2}, NSCHET={3} -'
                         u' запись не обновлена'.format(
                             eventId, serviceCode, accountItemId,
                             self._accountNumber))
            self.nNotFound += 1
            return

   #     serviceCodeAcc = forceString(self.db.translate(
   #             'rbService', 'id', forceRef(record.value('service_id')), 'infis'))
   #     if serviceCodeAcc != serviceCode:
   #         return
        accountId = forceRef(record.value('master_id'))
        contractId, accountNumber = self.getContractIdAndAccNumber(accountId)
        financeId = self.getFinanceId(contractId)
        payStatusMask = getPayStatusMask(financeId)
        if attachCode:
            note = u'МО прикрепления на момент оказания услуги {0}'.format(
                attachCode)

 #       record.setValue('note', toVariant(note))
        record.setValue('number', toVariant(self.confirmation))
        record.setValue('date', toVariant(QDate.currentDate()))
        record.setValue('note', toVariant(';'.join(notes)))
        if sumUsl == 0:
            pass
        elif self._sumPayed >= self._sumExposed:
            updateDocsPayStatus(record, payStatusMask, CPayStatus.payedBits)
            record.setValue('payedSum', toVariant(sumUsl))
            self.nPayed += 1
        elif (self._isAnySanctions and self._sumExposed > self._sumPayed
              and self._sumPayed):
            updateDocsPayStatus(record, payStatusMask, CPayStatus.refusedBits)
            record.setValue('payedSum', toVariant(self._sumPayed))
            self.nRefused += 1
        elif not self._sumPayed:
            updateDocsPayStatus(record, payStatusMask, CPayStatus.refusedBits)
            refuseTypeId = self.getRefuseTypeId(refuseCode)
            record.setValue('refuseType_id', toVariant(refuseTypeId))
            self.nRefused += 1
        self.nProcessed += 1
        self.db.updateRecord(self.tableAccountItem, record)
        clientLastName, clientFirstName, clientPatrName = (
            self.getClientCredentials(clientId))
        self.err2log(u'{0}, {1}, {2}, {3}, {4}, {5} - запись обновлена'.format(
            accountNumber, clientLastName, clientFirstName, clientPatrName,
            serviceCode, eventId))
        self._accountIdSet.add(accountId)


    def findAccountItem(self, eventId, serviceCode):
        result = None
        stmt = """SELECT id FROM Account_Item
            WHERE Account_Item.event_id = {eventId}
              AND Account_Item.service_id IN (
               SELECT id FROM rbService
               WHERE infis = '{serviceCode}')
            LIMIT 1""".format(eventId=eventId, serviceCode=serviceCode)
        query = self.db.query(stmt)
        if query.first():
            record = query.record()
            result = forceRef(record.value(0))
        return result


    def getContractIdAndAccNumber(self, accId):
        result = self._contractCache.get(accId, -1)

        if result == -1:
            result = None, '-'
            record = self.db.getRecord(self.tableAccount, 'contract_id,number',
                                       accId)
            if record:
                contractId = forceRef(record.value(0))
                accountNumber = forceString(record.value(1))
                result = contractId, accountNumber
            self._contractCache[accId] = result

        return result


    def getFinanceId(self, contractId):
        result = self._financeCache.get(contractId, -1)

        if result == -1:
            result = forceRef(self.db.translate(
                'Contract', 'id', contractId, 'finance_id'))
            self._financeCache[contractId] = result

        return result


    def getClientCredentials(self, clientId):
        result = self._clientCredentialsCache.get(clientId, -1)
        if result == -1:
            result = None
            record = self.db.getRecord(
                self.tableClient, 'lastName,firstName,patrName', clientId)
            if record:
                result = (forceString(record.value(0)),
                          forceString(record.value(1)),
                          forceString(record.value(2)))
            self._clientCredentialsCache[clientId] = result

        return result

    def getAccountItemIdListByClientAndEvent(self, clientId, eventId, codeUsl,
                                             sumUsl, accountItemIdList):
        cond = ('AND Account_Item.master_id={0}'.format(self.accountId)
                if self.chkOnlyCurrentAccount.isChecked() else '')
        stmt = u"""SELECT Account_Item.id,
            Account.date as Account_date,
            Account_Item.date as Account_Item_date,
            Account_Item.master_id as Account_id,
            Account_Item.sum as payedSum,
            Account.contract_id as contract_id,
            Event.id as eventId
        FROM Account_Item
        LEFT JOIN Event ON Event.id = Account_Item.event_id
        LEFT JOIN EventType ON EventType.id = Event.eventType_id
        LEFT JOIN Account ON Account_Item.master_id = Account.id
        LEFT JOIN rbService On rbService.id = Account_Item.service_id
        LEFT JOIN Visit ON Visit.id = Account_Item.visit_id
        WHERE Account_Item.date IS NULL
          AND Event.client_id = '{clientId}'
          AND rbService.infis = '{serviceInfis}'
          AND Account_Item.sum = '{itemSum}'
          AND (
          Event.id='{eventId}'
               OR Event.externalId = '{eventId}'
               OR (SELECT numberCardCall FROM EmergencyCall
                    WHERE event_id = Event.id) = '{serviceInfis}'

                   )
          {cond} LIMIT 1""".format(
              clientId=clientId, serviceInfis=codeUsl, itemSum=sumUsl,
              eventId=eventId, cond=cond)

        query = self.db.query(stmt)
        while query.next():
            accountItemIdList.append(query.record())

        return accountItemIdList


    def getPersonIdList(self, snils, code):
        key = (snils, code)
        result = self._personListCache.get(key, -1)
        if result == -1:
            stmt = """SELECT Person.id FROM Person
                LEFT JOIN rbSpeciality ON rbSpeciality.id = Person.speciality_id
                WHERE SNILS = '{snils}'
                  AND (rbSpeciality.federalCode = '{code}'
                       OR rbSpeciality.usishCode = '{code}')""".format(
                           snils=snils, code=code)
            query = self.db.query(stmt)
            result = []
            while query.next():
                record = query.record()
                if record:
                    result.append(forceString(record.value(0)))
            self._personListCache[key] = result
        return result


    def findInsurerByOGRNandOKATO(self, ogrn, okato):
        u"""Поиск по ОГРН и ОКАТО"""
        key = (ogrn, okato)
        result = self.insurerCache.get(key, -1)
        if result == -1:
            record = self.db.getRecordEx(
                self.tableOrganisation, 'id', [
                    self.tableOrganisation['OGRN'].eq(ogrn),
                    self.tableOrganisation['OKATO'].eq(okato),
                    self.tableOrganisation['isInsurer'].eq(1)])
            result = forceRef(record.value(0)) if record else None
            self.insurerCache[key] = result

        return result


    def getPolicyKindId(self, code):
        result = self.policyKindIdCache.get(code, -1)
        if result == -1:
            result = forceRef(self.db.translate(
                'rbPolicyKind', 'regionalCode', code, 'id'))
            self.policyKindIdCache[code] = result

        return result


    def updateClientPolicy(self, clientId, insurerId, serial, number, begDate,
                           newInsurerOGRN, policyKindId, eventBegDate,
                           eventEndDate):
        (oldNpolis, _, _, _, _, _, _, oldInsurerId) = (
            Export29XMLCommon.getClientPolicy1(self.db, clientId, eventBegDate,
                                               eventEndDate))
        if not oldInsurerId:
            self.addClientPolicy(clientId, insurerId, serial, number, eventBegDate,
                                 self.policyTypeTerritorial, policyKindId)
            self.err2log(u'добавлен полис: `%s№%s (%s)`' % (
                serial, number, insurerId if insurerId else 0))
            return True

        if not newInsurerOGRN:
            newInsurerOGRN = forceString(self.db.translate(
                'Organisation', 'id', insurerId, 'OGRN'))
        if insurerId and not (str(oldInsurerId) == str(insurerId)
                              and oldNpolis == number):
            newInsurer = insurerId
            newSerial = serial
            newNumber = number
            self.addClientPolicy(clientId, insurerId, serial, number,
                                 eventBegDate, self.policyTypeTerritorial,
                                 policyKindId)
            self.err2log(u'обновлен полис: `%s№%s (%s)` на `%s№%s (%s)`' % (
                newSerial if newSerial else '',
                newNumber if newNumber else '',
                newInsurer if newInsurer else 0,
                serial if serial else '',
                number if number else '',
                insurerId if insurerId else 0))
            return True
        return False


    def closeOpenedPolicy(self, clientId, eventBegDate):
        recordList = self.db.getRecordList(
            'ClientPolicy', '*', 'client_id = {0} '
            'AND (endDate IS NULL OR endDate = \'0000-00-00\') '
            'AND deleted = 0 '.format(clientId), '', 'begDate')
        acc = []
        for record in recordList:
            count = {}
            count['policyId'] = forceRef(record.value('id'))
            count['begDate'] = forceDate(record.value('begDate'))
            acc.append(count)
        if acc:
            maxCP = max(acc)
            tblClientPolicy = self.db.table('ClientPolicy')
            while min(acc) != maxCP:
                record = acc.pop(acc.index(min(acc)))
                clientPolicy = self.db.getRecord(
                    tblClientPolicy, '*', record['policyId'])
                clientPolicy.setValue(
                    'endDate', toVariant(min(acc)['begDate'].addDays(-1)))
                self.db.updateRecord(tblClientPolicy, clientPolicy)
                self.err2log(u'закрыты полиса у пациента %s'%clientId)
            if maxCP['policyId'] != self.db.getRecord(
                    tblClientPolicy, '*', 'max(id)'):
                clientPolicy = self.db.getRecord(
                    tblClientPolicy, '*', maxCP['policyId'])
                clientPolicy.setValue('deleted', toVariant(1))
                self.db.updateRecord(tblClientPolicy, clientPolicy)
                clientPolicy.setValue('id', toVariant('Null'))
                clientPolicy.setValue('deleted', toVariant(0))
                self.db.insertRecord(tblClientPolicy, clientPolicy)


    def getContract(self, eventId):
        (eventType, oldContractId, _, _, eventEndDate, clientInsurerId,
         policyType, _, clientSex, clientAttachType, organizationArea,
         socStatus, clientWork, eventOrg, isAmbiguitous) = (
             self.getInfromationForContract(eventId))
        cond = []
        k = 0
        contractId = None
        contractName = []
        cond.append(u'Contract.deleted =0')
        if eventEndDate:
            dateStr = eventEndDate.toString(Qt.ISODate)
            cond.append(u"Contract.begDate <='{0}'".format(dateStr))
            cond.append(u"Contract.endDate >='{0}'".format(dateStr))
        else:
            return None, oldContractId, k, 0, contractName

        if eventType:
            cond.append(u'Contract_Specification.eventType_id =%s'%eventType)
        if clientInsurerId:
            if organizationArea == 29:
                cond.append(u'Contract_Contingent.insurer_id =%d'% clientInsurerId)
            else:
                cond.append(u'IF(Contract_Contingent.insurer_id IS NULL, 1 =1, Contract_Contingent.insurer_id =%d)'% clientInsurerId)
        if clientAttachType:
            cond.append(u'IF( Contract_Contingent.attachType_id IS NULL , 1 =1, Contract_Contingent.attachType_id =%d)'%clientAttachType)
        if policyType:
            cond.append(u'IF( Contract_Contingent.policyType_id IS NULL , 1 =1, Contract_Contingent.policyType_id =%d)'%policyType)
        if clientSex:
            cond.append(u'IF( Contract_Contingent.sex =0, 1 =1,Contract_Contingent.sex=%d)'%clientSex)
        if socStatus:
            cond.append(u'IF( Contract_Contingent.socStatusType_id IS NULL, 1 =1,Contract_Contingent.socStatusType_id=%d)'%socStatus)
        if clientWork:
            cond.append(u'IF( Contract_Contingent.org_id IS NULL, 1 =1,Contract_Contingent.org_id=%d)'%clientWork)
        if eventOrg:
            cond.append(u'Contract.recipient_id=%d'%eventOrg)

        cond.append(u'IF( Contract.finance_id IS NULL, 1 =1,Contract.finance_id=2)')
        if not cond:
            return 'flag', 'flag', 0, 0
        stmtContract = """SELECT DISTINCT(`Contract`.id) AS contractId,
                Contract.number AS contractName
            FROM `Contract`
            LEFT JOIN Contract_Contingent ON Contract_Contingent.master_id = Contract.id
            LEFT JOIN Contract_Specification ON Contract_Specification.master_id = Contract.id
            LEFT JOIN Organisation ON Contract_Contingent.insurer_id = Organisation.id
            WHERE `Contract_Specification`.deleted = 0
              AND Contract_Contingent.deleted = 0
              AND {0}""".format(self.db.joinAnd(cond))
        query = self.db.query(stmtContract)

        while query.next():
            k += 1
            record = query.record()
            contractId = forceInt(record.value('contractId'))
            contractName.append(forceString(record.value('contractName')))
        if contractId:
            return  contractId, oldContractId, k, isAmbiguitous, contractName
        return None, None, k, 0, contractName


    def getInfromationForContract(self, eventId):
        stmt = """SELECT Event.contract_id as oldContract,
                Event.eventType_id as eventType,
                Event.client_id as clientId,
                Event.setDate as eventBegDate,
                Event.execDate as eventEndDate,
                Event.org_id as eventOrg,
                ClientPolicy.insurer_id as clientInsurerId,
                ClientPolicy.policyType_id as policyType,
                ClientAttach.attachType_id as clientAttachType,
                ((YEAR(Event.setDate) - YEAR(Client.birthDate)) -
                (RIGHT(Event.setDate, 5) < RIGHT(Client.birthDate, 5))) as clientAge,
                Client.sex as clientSex,
                SUBSTRING( Organisation.area, 1, 2 ) as organizationArea,
                ClientSocStatus.socStatusType_id as socStatus,
                ClientWork.org_id as clientWork
            FROM  `Event`
            LEFT JOIN Client ON Client.id = Event.client_id
            LEFT JOIN EventType ON EventType.id = Event.eventType_id
            LEFT JOIN ClientAttach ON (ClientAttach.client_id = Client.id AND ClientAttach.begDate <= Event.execDate
                    AND (ClientAttach.endDate IS NULL or ClientAttach.endDate>=Event.execDate or ClientAttach.endDate='0000-00-00') AND ClientAttach.deleted =0)
            LEFT JOIN `rbAttachType` ON `rbAttachType`.id = ClientAttach.attachType_id
            LEFT JOIN ClientPolicy ON (ClientPolicy.client_id = Client.id AND
                    ClientPolicy.begDate <= Event.execDate AND
                    (ClientPolicy.endDate is NULL or ClientPolicy.endDate >= Event.execDate or ClientPolicy.endDate='0000-00-00') and ClientPolicy.insurer_id IS NOT NULL AND ClientPolicy.deleted =0)
            LEFT JOIN Organisation ON ClientPolicy.insurer_id = Organisation.id
            LEFT JOIN ClientSocStatus ON Client.id = ClientSocStatus.client_id
            LEFT JOIN ClientWork ON Client.id = ClientWork.client_id
            WHERE Event.id ='{0}'
              AND IF(ClientAttach.id IS NULL, 1=1, rbAttachType.code NOT IN (10,11,12))
            GROUP BY ClientPolicy.id, ClientAttach.id""".format(eventId)
        query = self.db.query(stmt)

        eventType = None
        oldContract = None
        clientId = None
        eventBegDate = None
        eventEndDate = None
        clientInsurerId = None
        policyType = None
        clientAge = None
        clientSex = None
        clientAttachType = None
        organizationArea = None
        socStatus = None
        clientWork = None
        eventOrg = None
        i = 0

        while query.next():
            i = i + 1
            eventType = forceRef(query.record().value('eventType'))
            oldContract = forceRef(query.record().value('oldContract'))
            clientId = forceRef(query.record().value('clientId'))
            eventBegDate = forceDate(query.record().value('eventBegDate'))
            eventEndDate = forceDate(query.record().value('eventEndDate'))
            clientInsurerId = forceRef(query.record().value('clientInsurerId'))
            policyType = forceRef(query.record().value('policyType'))
            clientAge = forceInt(query.record().value('clientAge'))
            clientSex = forceInt(query.record().value('clientSex'))
            clientAttachType = forceRef(query.record().value('clientAttachType'))
            organizationArea = forceInt(query.record().value('organizationArea'))
            eventOrg = forceInt(query.record().value('eventOrg'))
            socStatus = forceRef(query.record().value('socStatus'))
            clientWork = forceRef(query.record().value('clientWork'))
        return  eventType, oldContract, clientId, eventBegDate, \
                eventEndDate, clientInsurerId, policyType,   \
                clientAge, clientSex, clientAttachType, organizationArea, \
                socStatus, clientWork, eventOrg, i


    def addClientPolicy(self, clientId, insurerId, serial, number, begDate,
                        policyTypeId, policyKindId):
        table = self.db.table('ClientPolicy')
        record = table.newRecord()
        record.setValue('client_id', toVariant(clientId))
        record.setValue('insurer_id', toVariant(insurerId))

        if policyTypeId:
            record.setValue('policyType_id', toVariant(policyTypeId))

        if policyKindId:
            record.setValue('policyKind_id', toVariant(policyKindId))

        record.setValue('serial', toVariant(serial))
        record.setValue('number', toVariant(number))
        record.setValue('begDate', toVariant(begDate))
        self.db.insertRecord(table, record)


    def processAccountItemIdList(self, recordList, refuseCode, refuseText,
                                 note, refusedSum):
        if recordList == [] or recordList[0] is None:
            self.nNotFound += 1
            self.err2log(u'счёт не найден')
            return

        for record in recordList:
            QtGui.qApp.processEvents()
            self._accountIdSet.add(forceRef(record.value('Account_id')))
            eventId = forceRef(record.value('eventId'))
            if eventId == 1357146:
                pass
            contractId, oldContractId, k, isAmbiguitous, contractName = (
                self.getContract(eventId))
            financeId = forceRef(self.db.translate(
                'Contract', 'id', contractId, 'finance_id'))
            payStatusMask = getPayStatusMask(financeId)
            payedSum = forceDouble(record.value('payedSum'))
            if refusedSum > 0:
                if forceDouble(refusedSum) >= payedSum:
                    payedSum = 0
                else:
                    payedSum -= forceDouble(refusedSum)

            if contractId == 'flag':
                note.append(u'Не удалось подобрать договор')

            if oldContractId != contractId and contractId:
                eventInfo = self.db.getRecord(self.tableEvent, '*', eventId)
                if eventInfo:
                    msg  = u'Произошла смена договора после подгрузки файла %s;'%(unicode(self.edtFileName.text()))
                    eventInfo.setValue('contract_id', toVariant(contractId))
                    eventNote = {}
                    notes = []
                    notes.append(msg)
                    eventNote = list(notes)
                    eventNote.append(forceString(eventInfo.value(u'note')))
               #     eventNote.append(u'Произошла смена договора после подгрузки файла %s;'%(unicode(self.edtFileName.text())))
                    noteStr = ';'.join(i for i in eventNote)
                    eventInfo.setValue(u'note', noteStr)
                    self.db.updateRecord(self.tableEvent, eventInfo)
                    note.append(u'Произошла смена договора')
            if k > 1:
                note.append(u'Попадает под действие нескольких договоров '
                            u'{0}'.format(u', '.join(contractName)))
            if isAmbiguitous > 1:
                note.append(u'В рег. карте имеются пересекающиеся по датам '
                            u'действия прикрепления/полисы')

            if self.prevContractId != contractId:
                self.prevContractId = contractId
                financeId = forceRef(self.db.translate(
                    'Contract', 'id', contractId, 'finance_id'))
                payStatusMask = getPayStatusMask(financeId)

            accountItemId = forceRef(record.value('id'))
            self.nProcessed += 1

            accItem = self.db.getRecord(
                self.tableAccountItem, '*', accountItemId)
            if refuseCode <> 0:
                refuseTypeId = self.getRefuseTypeId(refuseCode)
                self.nRefused += 1
                accItem.setValue('refuseType_id', toVariant(refuseTypeId))
                updateDocsPayStatus(
                    accItem, payStatusMask, CPayStatus.refusedBits)
                accItem.setValue('payedSum', payedSum)
                self.err2log(
                    u'отказан, код: {0} {1}'.format(refuseCode, refuseText))
                accItem.setValue('date', toVariant(QDate.currentDate()))
            else:
                updateDocsPayStatus(
                    accItem, payStatusMask, CPayStatus.payedBits)
                accItem.setValue('payedSum', payedSum)
                accItem.setValue('date', toVariant(QDate.currentDate()))
                self.err2log(u'подтверждён')
                self.nPayed += 1

            accItem.setValue('number', toVariant(self.confirmation))
            accItem.setValue('note', toVariant(';'.join(note)))
            self.db.updateRecord(self.tableAccountItem, accItem)


    def writeConfirmation(self, fileName):
        outFileName = u'F{0}.XML'.format(os.path.basename(fileName)[1:])
        dir = forceString(self.edtConfirmationDir.text())
        if not dir:
            dir = os.path.dirname(fileName)
        outFileName = os.path.join(dir, outFileName)
        self.errorPrefix = ''
        chiefId = self.cmbChief.getValue()
        if not chiefId:
            self.err2log(u'Руководитель не выбран, '
                         u'подтверждение не сформировано')
            return
        deletegateId = self.cmbDelegate.getValue()
        if not deletegateId:
            self.err2log(u'Уполномоченное лицо не выбрано, '
                         u'подтверждение не сформировано')
            return
        out = QFile(outFileName)
        if out.open(QFile.WriteOnly | QFile.Text):
            self.err2log(u'Формируем подтверждение `{0}zip`'.format(
                outFileName[:-3]))
            writer = QXmlStreamWriter(out)
            writer.writeStartElement('ACCEPT_NOTE')
            writer.writeTextElement('FILENAME', os.path.basename(fileName))
            writer.writeTextElement('ACCEPT_DATE',
                QDate.currentDate().toString(Qt.ISODate))
            name, post = self.getPersonFullNameAndPost(chiefId)
            writer.writeTextElement('EXEC_NAME',  name)
            writer.writeTextElement('EXEC_POSITION', post)
            name, post = self.getPersonFullNameAndPost(deletegateId)
            writer.writeTextElement('PREP_BY_NAME', name)
            writer.writeTextElement('PREP_BY_POSITION', post)
            writer.writeEndElement() # ACCEPT_NOTE
            out.close()
            compressFileInZip(outFileName, u'{0}zip'.format(outFileName[:-3]))
            os.remove(outFileName)
        else:
            self.err2log(u'Ошибка открытия файла `{0}` для записи: {1}'.format(
                outFileName, forceString(out.errorString())))


    def getPersonFullNameAndPost(self, _id):
        u'Возвращает ФИО и должность сотрудника по идентификатору'
        table = self.tablePerson
        record = self.db.getRecord(table, 'post_id, TRIM(CONCAT(lastName, \' '
                                   '\' , firstName, \' \' , patrName))', _id)
        fullName, postName = '', ''
        if record:
            postId = forceRef(record.value(0))
            fullName = forceString(record.value(1))
            if postId:
                postName = forceString(self.db.translate(
                    'rbPost', 'id', postId, 'name'))
        return fullName, postName


    def __createControlResultRecord(self):
        if not self._accountIdSet:
            return
        table = tbl('Account_ControlResult')
        now = toVariant(QDateTime.currentDateTime())
        userId = toVariant(QtGui.qApp.userId)
        for accountId in self._accountIdSet:
            act = self.__acts.get(accountId)
            if act:
                record = table.newRecord()
                record.setValue('master_id', toVariant(accountId))
                record.setValue('modifyDatetime', toVariant(now))
                record.setValue('modifyPerson_id', toVariant(userId))
                record.setValue('createDatetime', toVariant(now))
                record.setValue('createPerson_id', toVariant(userId))
                date, number, name = act
                record.setValue('actName', toVariant(name))
                record.setValue('actNumber', toVariant(number))
                record.setValue('actDate',
                                toVariant(QDate.fromString(date, Qt.ISODate)))
                self.db.insertRecord(table, record)


if __name__ == '__main__':
    #pylint: disable=wrong-import-position,ungrouped-imports
    from Exchange.Utils import testAccountImport
    #pylint: enable=wrong-import-position,ungrouped-imports
    testAccountImport(ImportPayRefuseR29Native, u'238/ПР', 'rakitina_prim.ini')
