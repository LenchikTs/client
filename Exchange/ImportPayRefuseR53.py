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

import re
import os
from zipfile import ZipFile

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, pyqtSignature, QDate, QDir, QFile


from library.dbfpy.dbf import Dbf
from library.Utils import forceDate, forceInt, forceRef, forceString, forceStringEx, nameCase, toVariant


from Registry.Utils import selectLatestRecord
from Events.Utils import CPayStatus, getPayStatusMask
from Accounting.Utils import updateAccounts, updateDocsPayStatus

from Exchange.Utils import tbl
from Exchange.Ui_ImportPayRefuseR53 import Ui_Dialog
from Exchange.Import131XML import CXMLimport


def ImportPayRefuseR53Native(widget, accountId, accountItemIdList):
    dlg = CImportPayRefuseR53Native(accountId, accountItemIdList)
    dlg.edtFileName.setText(forceString(QtGui.qApp.preferences.appPrefs.get('ImportPayRefuseR53FileName', '')))
    dlg.exec_()
    QtGui.qApp.preferences.appPrefs['ImportPayRefuseR53FileName'] = toVariant(dlg.edtFileName.text())


class CImportPayRefuseR53Native(QtGui.QDialog, Ui_Dialog, CXMLimport):
    version = '2.1'
    version201112 = '2.1'
    version201202 = '2.1'
    headerFields = ('Version', 'Sender', 'C_OGRN', 'Addressee',
                            'M_OGRN', 'Theme', 'Accounting_period', 'NUM_S', 'DATE_S')
    accountItemFields = ('N_PP', 'DEP_ID', 'VID_P', 'SN_POL', 'FAM', 'IM', 'OT',
                         'DR', 'W', 'PR_PR', 'DRP', 'WP', 'Q_G', 'Q_V',
                         'Q_U', 'V_ED', 'V_V', 'DS', 'DS_S', 'PRMP', 'C_LC',
                         'NUM_CAR', 'DATE_1', 'DATE_2', 'IDRB', 'MED_ST',
                         'PRVS', 'RSLT', 'IDSP', 'TARIF', 'S_ALL', 'S_OPL',
                         'I_TYPE', 'C_OGRN', 'C_OKATO', 'SS', 'C_P', 'SN_DOC',
                         'DATE_DOC', 'NAME_VP', 'ADS_B', 'C_SHIP', 'ATTACH_SIGN', 'Q_R',
                         'NUM_CARD', 'RES_CTRL')

    importNormal = 0
    import201112 = 1
    import201202 = 2
    #Новые импорты - будем переходить к ним
    importTFOMS1 = 10
    importSMO1    = 11
    importTFOMS2 = 12
    importTypeFlag = 100
    importType=None
    zglvFields = ('VERSION', 'DATA', 'FILENAME')
    schetFields = ('CODE', 'CODE_MO', 'YEAR', 'MONTH', 'NSCHET', 'DSCHET', 'PLAT', 'SUMMAV', 'COMENTS',
                            #При наличие нижеидущих тэгов считаем что этот реестр из страховой, иначе Предварит реестр
                            'SUMMAP', 'SANK_MEK', 'SANK_MEE', 'SANK_EKMP')
    pacientFields = ('ID_PAC', 'VPOLIS', 'SPOLIS', 'NPOLIS', 'ST_OKATO', 'SMO', 'SMO_OGRN', 'SMO_OK',
                     'SMO_NAM', 'FAM', 'IM', 'NOVOR', 'VNOV_D')
    sluchFields = ('IDCASE', 'USL_OK', 'VIDPOM', 'FOR_POM', 'NPR_MO', 'EXTR', 'LPU', 'LPU_1','PODR', 'PROFIL', 'DET',
                   'NHISTORY', 'DATE_1', 'DATE_2', 'DS0', 'DS1', 'DS2', 'DS2', 'VNOV_M', 'CODE_MES1', 'CODE_MES2', 'RSLT',
                   'ISHOD', 'PRVS', 'VERS_SPEC', 'IDDOKT', 'OS_SLUCH', 'IDSP', 'ED_COL', 'TARIF', 'SUMV', 'OPLATA',
                   'SUMP', 'COMENTSL')
    uslFields = ('IDSERV', 'LPU', 'PROFIL', 'DET', 'DATE_IN', 'DATE_OUT', 'DS', 'KOL_USL',
                        'TARIF', 'SUMV_USL', 'PRVS', 'COMENTU')
#    sankFields = {'S_CODE', 'S_SUM', 'S_TIP', 'S_OSN', 'S_COM', 'S_IST'}
    sexMap = {u'М':1, u'Ж':2}
    flagUpdatePolicy = 0


    def __init__(self, accountId, accountItemIdList):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        CXMLimport.__init__(self, self.log)
        self.accountId=accountId
        self.accountItemIdList=accountItemIdList
        self.progressBar.setFormat('%p%')
        self.checkName()
        self.errorPrefix = ''
        self.nProcessed = 0
        self.nPayed = 0
        self.nRefused = 0
        self.nNotFound = 0
        self.tableAccountItem = tbl('Account_Item')
        self.tableAccount = tbl('Account')
        self.tableClient = tbl('Client')
        self.tableAcc=self.db.join(self.tableAccountItem, self.tableAccount,
            'Account_Item.master_id=Account.id')
        self.prevContractId = None
        self.financeTypeOMS = forceRef(self.db.translate('rbFinance',
            'code', '2', 'id'))
        self.policyTypeTerritorial = forceRef(self.db.translate('rbPolicyType',
            'code', '1', 'id'))
        self.policyTypeIndustrial = forceRef(self.db.translate('rbPolicyType',
            'code', '2', 'id'))
        self.currentAccountOnly = False
        self.confirmation = ''
        self.serviceCache = {}
        self.accountItemIdListCache = {}
        self.clientCache = {}
        self.clientByAccountItemIdCache = {}
        self.clientByEventIdCache = {}
        self.accountIdSet = set()
        self.refuseTypeIdCache = {}
        self.insurerArea = QtGui.qApp.defaultKLADR()[:2]
        self.insurerCache = {}
        self.policyKindIdCache = {}
        self.isDBF = True
        self.tmpDir = ''
        self.commentsl = ''


    def getTmpDir(self):
        if not self.tmpDir:
            self.tmpDir = QtGui.qApp.getTmpDir('R53ImportPayRefuse')
        return self.tmpDir


    def cleanup(self):
        if self.tmpDir:
            QtGui.qApp.removeTmpDir(self.tmpDir)
            self.tmpDir = ''


    @pyqtSignature('')
    def on_btnSelectFile_clicked(self):
        fileName = QtGui.QFileDialog.getOpenFileName(
            self, u'Укажите файл с данными', self.edtFileName.text(), u'Файлы XML, DBF, ZIP (*.xml *.dbf *.zip)')
        if fileName != '':
            self.edtFileName.setText(QDir.toNativeSeparators(fileName))
            self.btnImport.setEnabled(True)


    def err2log(self, e):
        if self.isDBF:
            self.log.append(self.errorPrefix+e)
        else:
            CXMLimport.err2log(self, self.errorPrefix+e)


    def startImport(self):
        self.progressBar.setFormat('%p%')
#        n=0
        self.nProcessed = 0
        self.nPayed = 0
        self.nRefused = 0
        self.nNotFound = 0
        fileName = forceStringEx(self.edtFileName.text())
#        (name,  fileExt) = os.path.splitext(fileName)
#        s=string.split(name, "\\")
#        i=len(s)
#        self.log.append(u'Ипорт %s' % s[len(s)-1][:2])
        filePath, pureFileName = os.path.split(fileName)
        fileBaseName, fileExt = os.path.splitext(pureFileName)
        self.log.append(u'Импорт %s' % fileBaseName[:2])
        TypeImp=fileBaseName[:2]
        if  fileExt.lower() == '.zip':
            zf = ZipFile(fileName, 'r', allowZip64=True)
            zf.extract(zf.namelist()[0], self.getTmpDir())
            fileName = os.path.join(self.getTmpDir(), zf.namelist()[0])
            (name,  fileExt) = os.path.splitext(fileName)
        if not (fileExt.lower() in ('.dbf', '.xml')):
            self.log.append(u'распакованный файл `%s` должен быть в формате XML или DBF' % fileName)
            self.cleanup()
            return
        self.isDBF = (fileExt.lower() == '.dbf')
        self.currentAccountOnly = self.chkOnlyCurrentAccount.isChecked()
        self.confirmation = self.edtConfirmation.text()
        self.accountIdSet = set()
        if not self.confirmation:
            self.log.append(u'нет подтверждения')
            self.cleanup()
            return
        if self.isDBF:
            inFile = Dbf(fileName, readOnly=True, encoding='cp866')
        else:
            inFile = QFile(fileName)
            self.log.append(u'%s' % fileName)
            if not inFile.open(QFile.ReadOnly | QFile.Text):
                QtGui.QMessageBox.warning(self, u'Импорт данных из XML',
                                      u'Не могу открыть файл для чтения %s:\n%s.' \
                                      % (fileName, inFile.errorString()))
                self.cleanup()
                return
        self.progressBar.reset()
        self.progressBar.setValue(0)
        self.progressBar.setFormat(u'%v записей' if self.isDBF else u'%v байт')
        self.stat.setText("")
        size = max(len(inFile) if self.isDBF else inFile.size(), 1)
        self.progressBar.setMaximum(size)
        self.labelNum.setText(u'размер источника: '+str(size))
        self.btnImport.setEnabled(False)
        proc = self.readDbf if self.isDBF else self.readFile
        if (not proc(inFile, TypeImp)):
            if self.abort:
                self.err2log(u'! Прервано пользователем.')
            else:
                self.err2log(u'! Ошибка: файл!!! %s, %s' % (fileName,
                                            self.errorString()))
        inFile.close()
        self.cleanup()
        self.err2log(u'ОК2')
        self.stat.setText(
            u'обработано: %d; оплаченых: %d; отказаных: %d; не найдено: %d' % \
            (self.nProcessed, self.nPayed, self.nRefused, self.nNotFound))
        if list(self.accountIdSet):
            updateAccounts(list(self.accountIdSet))


    def readDbf(self, dbf):
        for row in dbf:
            self.processRow(row.asDict(), True)
            QtGui.qApp.processEvents()
            self.progressBar.step()
            if self.abort:
                return False
        return True


    def readFile(self, device, typeImp):
        #if typeImp=='HM':
        self.ImportSMO(device)
        #elif typeImp=='HM':
        #    self.ImportFOMS(device)
       # else:
        #    self.err2log(u'Неизвестный Формат имени файла')
        return True


    def initHistory(self):
        historyData={
        'comment':'',
        'numHistory':'',
        'flagOplata':'',
        'sanctOsn':'',
        'endHistory':'',
        'sumSluch':''}
        return historyData


    def ImportSMO(self, device):
        self.setDevice(device)
#        i=0
        historyData=self.initHistory()
        while (not self.atEnd()):
            self.readNext()
            tagName=self.name()
            isStart=self.isStartElement()
            if isStart and tagName == 'NHISTORY':
                historyData['numHistory']=self.readElementText()
            elif isStart and tagName == 'OPLATA':
                historyData['flagOplata']=self.readElementText()
            elif isStart and tagName == 'S_OSN':
                historyData['sanctOsn']=self.readElementText()
            elif isStart and tagName == 'COMENTSL':
                historyData['comment']=self.readElementText()
            elif isStart and tagName == 'SUMV':
                historyData['sumSluch']=self.readElementText()
            elif self.isEndElement() and tagName== 'SLUCH':
                self.err2log(u'код причины отказа %s' % historyData['sanctOsn'])
                if  historyData['sanctOsn']=='':
                    self.processRowImport1SMO(historyData['numHistory'], historyData['sumSluch'])
                else:
                    self.processRowImporSMO(historyData['numHistory'], historyData['sanctOsn'], historyData['comment'])
                historyData=self.initHistory()


    def ImportFOMS(self, device):
        self.setDevice(device)
        while (not self.atEnd()):
            self.readNext()
            if self.isStartElement():
                if self.name() == 'ZL_LIST':
                    self.readList() # Новый формат 201112, 201202
                else:
                    self.raiseError(u'Неверный формат экспорта данных.')


    def processRowImporSMO(self, eventID, refCode, temp):
        accountItemIdList = self.getAccountItemIdListByEvent(eventID)
        reason = forceString(self.db.translate('rbPayRefuseType', 'code', refCode, 'id'))
        if not reason:
            self.err2log(u'<b><font color=red>ОШИБКА<\font><\b>:' \
                         u'Причины отказа с кодом (%s) не найден ' % refCode)
        for record in accountItemIdList:
            accountItemId = forceRef(record.value('id'))
            accItem = self.db.getRecord(self.tableAccountItem, '*', accountItemId)
            if accItem:
                #self.err2log(u'Отказ789 %s' % temp)
                accItem.setValue('note', toVariant(temp))
                accItem.setValue('refuseType_id', toVariant(reason))
                updateDocsPayStatus(accItem, 2, CPayStatus.refusedBits)
                accItem.setValue('date', toVariant(QDate.currentDate()))
                accItem.setValue('number', toVariant('HS'))
                self.db.updateRecord(self.tableAccountItem, accItem)
            else:
                self.err2log(u'Событие не найдено')


    def processRowImport1SMO(self, eventID, UpdateSumm):
        accountItemIdList = self.getAccountItemIdListByEvent(eventID)
        for record in accountItemIdList:
            accountItemId = forceRef(record.value('id'))
            accItem = self.db.getRecord(self.tableAccountItem, '*', accountItemId)
            if accItem:
                accItem.setValue('price', UpdateSumm)
                accItem.setValue('sum', UpdateSumm)
                accItem.setValue('note', toVariant(u'Одобрено'))
                updateDocsPayStatus(accItem, 2, CPayStatus.payedBits)
                accItem.setValue('date', toVariant(QDate.currentDate()))
                accItem.setValue('number', toVariant('HS'))
                self.db.updateRecord(self.tableAccountItem, accItem)
            else:
                self.err2log(u'Событие не найдено')


    def readData(self):
        assert self.isStartElement() and self.name() == 'root'
        while (not self.atEnd()):
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                if self.name() == 'heading':
                    result = self.readGroup('heading', self.headerFields)
                    if not self.hasError():
                        self.processHeader(result, self.importNormal)
                elif self.name() == 'Rendering_assistance':
                    result = self.readGroup('Rendering_assistance', self.accountItemFields)
                    if not self.hasError():
                        self.processRow(result)
                else:
                    self.readUnknownElement()
            if self.hasError():
                break


    def readList(self):
        assert self.isStartElement() and self.name() == 'ZL_LIST'
        importType = self.import201112
        while (not self.atEnd()):
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                if self.name() == 'ZGLV':
                    result = self.readGroup('ZGLV', self.zglvFields)
                    if not self.hasError():
                        importType = self.import201202 if result.get('FILENAME') else self.import201112
                        self.processHeader(result, importType)
                elif self.name() == 'SCHET':
                    result = self.readGroup('SCHET', self.schetFields)
                    if not self.hasError():
                        self.importTypeFlag = self.importTFOMS1
                elif self.name() == 'ZAP':
                    self.readZap(importType)
                else:
                    self.readUnknownElement()


    def readZap(self, importType):
        assert self.isStartElement() and self.name() == 'ZAP'
        result = {}
#        resultTFOMS1 = {}
        while (not self.atEnd()):
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                if self.name() == 'N_ZAP':
                    #Флаг сбрасываем здесь потому то в предварительном реестре зартст теперь тоже группируются
                    self.flagUpdatePolicy = 0
                    result['N_ZAP'] = forceString(self.readElementText())
                elif self.name() == 'PR_NOV':
                    result['PR_NOV'] = forceString(self.readElementText())
                elif self.name() == 'COMENTSL':
                    result['COMENTSL'] = forceString(self.readElementText())
                elif self.name() == 'PACIENT':
                    self.readGroup('PACIENT', self.pacientFields, result)
                    if not self.hasError() and self.importTypeFlag == self.importTFOMS1:
                        self.processRowImportTFOMS1(result, importType)
                elif self.name() == 'SLUCH':
                    if self.importTypeFlag == self.importTFOMS1:
                        result = self.readGroup('SLUCH', self.sluchFields, result, silent=True)
                        self.processRowImportTFOMS2(result)
                    else:
                        result = self.readSluch(result)
                else:
                    self.readUnknownElement()
            if self.hasError():
                break


    def readSluch(self, importType):
        assert self.isStartElement() and self.name() == 'SLUCH'
        result = {}
        while (not self.atEnd()):
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                if self.name() == 'SANK':
                    if not self.hasError():
                        self.processRowImport(result, importType)
                else:
                    self.readUnknownElement()


    def readGroup(self, name, fields, result = {}, silent = False):
        r = CXMLimport.readGroup(self, name, fields, silent)
        for key, val in r.iteritems():
            result[key] = val
        return result


    def processHeader(self, row, importType):
        if importType == self.importNormal:
            ver = row.get('Version', '')
            if ver != self.version:
                self.err2log(u'Формат версии `%s` не поддерживается.'
                                    u' Должен быть `%s`.' % (ver, self.version))
        elif importType == self.import201112:
            ver = row.get('VERSION', '')

            if ver != self.version201112:
                self.err2log(u'Формат версии `%s` не поддерживается.'
                                    u' Должен быть `%s`.' % (ver, self.version201112))
        elif importType == self.import201202:
            ver = row.get('VERSION', '')

            if ver != self.version201202:
                self.err2log(u'Формат версии `%s` не поддерживается.'
                                    u' Должен быть `%s`.' % (ver, self.version201202))


    def findInsurerByOGRN(self, OGRN):
        u"""Поиск по ОГРН с учётом области страхования"""
        result = self.insurerCache.get(OGRN, -1)
        if result == -1:
            record = self.db.getRecordEx(self.tableOrganisation, 'id',
                                      [self.tableOrganisation['OGRN'].eq(OGRN),
                                      self.tableOrganisation['area'].like(self.insurerArea+'...')])
            result = forceRef(record.value(0)) if record else self.OGRN2orgId(OGRN)
            self.insurerCache[OGRN] = result
        return re


    def findInsurerBySmoCode(self, smoCode):
        u"""Поиск по smoCode в принцепе smoCode уникально иденитифицирует страховую на всей тер рос"""
        result = self.insurerCache.get(smoCode, -1)
        if result == -1:
            record = self.db.getRecordEx(self.tableOrganisation, 'id',
                                      [self.tableOrganisation['smoCode'].eq(smoCode)])
            result = forceRef(record.value(0)) if record else ''
            self.insurerCache[smoCode] = result
        return result


    def findInsurerByOGRNandOKATO(self, OGRN, OKATO):
        u"""Поиск по ОГРН и ОКАТО с учётом области страхования"""
        key = (OGRN, OKATO)
        result = self.insurerCache.get(key, -1)
        if result == -1:
            record = self.db.getRecordEx(self.tableOrganisation, 'id',
                                      [self.tableOrganisation['OGRN'].eq(OGRN),
                                      self.tableOrganisation['OKATO'].eq(OKATO)])
            if record:
                result = forceRef(record.value(0))
            else:
                self.err2log(u'ОШИБКА: не найдена страховая')
            self.insurerCache[key] = result
        return result


    def processRow(self, row, isDBF=False, importType = import201112):
        lastName = nameCase(row.get('FAM', ''))
        firstName = nameCase(row.get('IM', ''))
        patrName = nameCase(row.get('OT', ''))
        sex = self.sexMap.get(row.get('W'), 0) if isDBF else forceInt(row.get('W'))
        if isDBF:
            birthDate = QDate(row.get('DR')) if row.has_key('DR') else QDate()
        else:
            birthDate = QDate().fromString(row['DR'], Qt.ISODate) if row.has_key('DR') else QDate()
        policySN = row.get('SN_POL')
        policyKindId = self.getPolicyKindId(row.get('VID_P'))

        if isDBF:
            sum = row.get('S_ALL', 0.0)
            accNum = row.get('NUM_S', '')
            accDate = QDate(row.get('DATE_S')) if row.has_key('DATE_S') else QDate()
            accountItemId = self.findAccountItemId(lastName, firstName,
                patrName, sum, accNum, accDate)
        else:
            accountItemId = forceInt(row.get('NUM_CARD'))
        refuseReasonCodeList =  forceString(row.get('I_TYPE', '')).split(' ')
        refuseDate = QDate().currentDate() if refuseReasonCodeList != [u''] else None
        refuseComment = row.get('COMMENT' if isDBF else 'RES_CTRL', '')
        accountItemIdList = self.getAccountItemIdList(accountItemId)
        recNum = forceInt(row.get('N_PP', 0))
        self.errorPrefix = u'Элемент №%d (%s %s %s): ' % (recNum, lastName, firstName, patrName)
        if accountItemIdList == []:
            self.err2log(u'не найден в реестре.')
            self.nNotFound += 1
            return
        cond=[]
        cond.append(self.tableAccountItem['id'].inlist(accountItemIdList))
        if self.currentAccountOnly:
            cond.append(self.tableAccount['id'].eq(toVariant(self.accountId)))
        fields = 'Account_Item.id, Account.date as Account_date, Account_Item.date as Account_Item_date, Account_Item.master_id as Account_id, Account.contract_id as contract_id'
        recordList = self.db.getRecordList(self.tableAcc, fields, where=cond)
        if (not isDBF) and policySN and recordList != []:
            clientId = self.getClientId(accountItemId)
            if not clientId:
                clientId = self.findClientByNameSexAndBirthDate(lastName, firstName, patrName, sex, birthDate)
            if clientId:
                self.checkClientPolicy(clientId, policySN, row.get('C_OGRN'), row.get('C_OKATO'), policyKindId, '')
            else:
                self.err2log(u'пациент не найден в БД')
        self.processAccountItemIdList(recordList, refuseDate, refuseReasonCodeList, refuseComment)


    def processAccountItemIdList(self, recordList, refuseDate, refuseReasonCodeList, refuseComment = ''):
        payStatusMask = 0
        for record in recordList:
            QtGui.qApp.processEvents()
            self.accountIdSet.add(forceRef(record.value('Account_id')))
            contractId = forceRef(record.value('contract_id'))
            if self.prevContractId != contractId:
                self.prevContractId = contractId
                financeId = forceRef(self.db.translate('Contract', 'id', contractId, 'finance_id'))
                payStatusMask = getPayStatusMask(financeId)
            accDate = forceDate(record.value('Account_date'))
            accItemDate = forceDate(record.value('Account_Item_date'))
            accountItemId = forceRef(record.value('id'))
            if accItemDate or (refuseDate and (accDate > refuseDate)):
                self.err2log(u'счёт уже отказан')
                return
            self.nProcessed += 1
            accItem = self.db.getRecord(self.tableAccountItem, '*', accountItemId)
            accItem.setValue('date', toVariant(refuseDate if refuseDate else QDate.currentDate()))
            refuseTypeId = None
            if refuseDate:
                self.nRefused += 1
                refuseTypeId= self.getRefuseTypeId(refuseReasonCodeList[0])
                if not refuseTypeId:
                    refuseTypeId = self.addRefuseTypeId(refuseReasonCodeList[0], refuseComment, self.financeTypeOMS)
                    self.refuseTypeIdCache[refuseReasonCodeList[0]] = refuseTypeId
                accItem.setValue('refuseType_id', toVariant(refuseTypeId))
                updateDocsPayStatus(accItem, payStatusMask, CPayStatus.refusedBits)
                self.err2log(u'отказан, код `%s`:`%s`' % (refuseReasonCodeList[0], refuseComment))
            else:
                self.err2log(u'подтверждён')
                self.nPayed += 1
            accItem.setValue('number', toVariant(self.confirmation))
            if self.flagUpdatePolicy == 1:
                accItem.setValue('note', toVariant(u'Изменения в полисе'))
            else:
                accItem.setValue('note', toVariant(refuseComment))
            self.db.updateRecord(self.tableAccountItem, accItem)
        if recordList == []:
            self.nNotFound += 1
            self.err2log(u'счёт не найден')


    #Выставляем комментарий для позиций счёта у которых произошли изменения в полисе
    def processRowImportTFOMS2(self, row):
        eventIdFieldName = 'NHISTORY' if row.has_key('NHISTORY') else 'IDCASE'
        eventId = forceRef(row.get(eventIdFieldName, None))
        if eventId:
            accountItemIdList = self.getAccountItemIdListByEvent(eventId)
        else:
            self.err2log(u'Для записи `%d` не заполнено поле NHISTORY' % forceInt(row.get('N_ZAP', 0)))
        for record in accountItemIdList:
            accountItemId = forceRef(record.value('id'))
            accItem = self.db.getRecord(self.tableAccountItem, '*', accountItemId)
            if self.flagUpdatePolicy == 1:
                accItem.setValue('note', toVariant(u'Изменения в полисе'))
            self.db.updateRecord(self.tableAccountItem, accItem)
        if accountItemIdList == []:
            self.nNotFound += 1
            self.err2log(u'счёт не найден')


    #Проверка необходимости обновления информации о полисе и само обновление
    def processRowImportTFOMS1(self, row, importType):
        clientId = forceString(row.get('ID_PAC', ''))
        kindPolicy = forceString(row.get('VPOLIS', ''))
        policySerial = forceString(row.get('SPOLIS', ''))
        policyNumber = forceString(row.get('NPOLIS', ''))
#        refuseComment = forceString(row.get('COMENTSL', ''))
        smoCode = forceString(row.get('SMO', ''))
#        smoOGRN = forceString(row.get('SMO_OGRN', ''))
        OKATO1 = forceString(row.get('ST_OKATO', ''))
        OKATO2 = forceString(row.get('SMO_OK', ''))
        smoOKATO = OKATO1 if OKATO1 != '' else OKATO2
        if policySerial or policyNumber:
            if clientId:
                policySN = u'%s№%s' % (policySerial, policyNumber)
                self.checkClientPolicy(clientId, policySN, row.get('SMO_OGRN'), smoOKATO, kindPolicy, smoCode)
            else:
                self.err2log(u'пациент не найден в БД')


    def processRowImport(self, row, importType):
        eventIdFieldName = 'NHISTORY' if row.has_key('NHISTORY') else 'IDCASE'
        eventId = forceRef(row.get(eventIdFieldName, None))
        refuseCode = forceString(row.get('REFREASON', ''))
        policySerial = forceString(row.get('SPOLIS', ''))
        policyNumber = forceString(row.get('NPOLIS', ''))
        refuseComment = forceString(row.get('COMENTSL', ''))
        if policySerial or policyNumber:
            clientId = self.getClientIdByEventId(eventId)
            if not clientId:
                lastName = forceString(row.get('FAM', ''))
                firstName = forceString(row.get('IM', ''))
                patrName = forceString(row.get('OT', ''))
                sex = forceInt(row.get('W', 0))
                birthDate = QDate.fromString(row.get('DR', ''), Qt.ISODate)
                clientId = self.findClientByNameSexAndBirthDate(lastName, firstName,
                    patrName, sex, birthDate)
            if clientId:
                pass
#                policySN = u'%s№%s' % (policySerial, policyNumber)
            else:
                self.err2log(u'пациент не найден в БД')
        # 2013 формат импорта ошибок
        if not refuseCode:
            refuseCode = forceString(row.get('ZP_RESULT', ''))
        if refuseCode:
            reason = forceString(self.db.translate('rbPayRefuseType', 'reason', refuseCode, 'code'))
            if not reason:
                self.err2log(u'<b><font color=red>ОШИБКА<\font><\b>:' \
                                    u'Для кода причины отказа %s не найден' \
                                    u' элемент таблицы rbPayRefuseType' % refuseCode)
                return
            refuseCode = reason
        refuseDate = QDate.currentDate() if refuseCode else None
        refuseCodeList = []
        if refuseCode:
            refuseCodeList.append(refuseCode)
        if eventId:
            accountItemIdList = self.getAccountItemIdListByEvent(eventId)
            self.processAccountItemIdList(accountItemIdList, refuseDate, refuseCodeList, refuseComment)
        else:
            self.err2log(u'Для записи `%d` не заполнено поле NHISTORY' % forceInt(row.get('N_ZAP', 0)))


    def getAccountItemIdListByEvent(self, eventId):
        fields = 'Account_Item.id, Account.date as Account_date, Account_Item.date as Account_Item_date, Account_Item.master_id as Account_id, Account.contract_id as contract_id'
        cond = [ self.tableAccountItem['event_id'].eq(eventId), ]
        if self.currentAccountOnly:
            cond.append(self.tableAccount['id'].eq(toVariant(self.accountId)))
        return self.db.getRecordList(self.tableAcc, fields, where =cond)


    def findAccountItemId(self, lastName, firstName, patrName, sum, accNum, accDate):
        stmt = """SELECT Account_Item.id
            FROM Account_Item
            LEFT JOIN Account ON Account.id = Account_Item.master_id
            LEFT JOIN Event ON Account_Item.event_id = Event.id
            LEFT JOIN Client ON Event.client_id = Client.id
            WHERE %s
            LIMIT 1
        """ % self.db.joinAnd([
                    self.tableAccountItem['sum'].eq(sum),
                    self.tableClient['lastName'].eq(lastName),
                    self.tableClient['firstName'].eq(firstName),
                    self.tableClient['patrName'].eq(patrName),
                ])
        query = self.db.query(stmt)
        if query and query.first():
            record = query.record()
            if record:
                return forceRef(record.value(0))
        return None


    def getPolicyKindId(self, code):
        result = self.policyKindIdCache.get(code, -1)
        if result == -1:
            result =forceRef(self.db.translate(
                'rbPolicyKind', 'regionalCode', code, 'id'))
            self.policyKindIdCache[code] = result
        return result


    def getAccountItemIdList(self, accountItemId):
        result =  self.accountItemIdListCache.get(accountItemId)
        if not result and accountItemId:
            result=[accountItemId, ]
            serviceId = self.getServiceId(accountItemId)
            if serviceId:
                stmt = """SELECT Account_Item.id,
                    IF(Account_Item.service_id IS NOT NULL,
                        Account_Item.service_id,
                        IF(Account_Item.visit_id IS NOT NULL,
                            Visit.service_id,
                            EventType.service_id)
                        ) AS serviceId
                    FROM Account_Item
                    LEFT JOIN Visit ON Visit.id  = Account_Item.visit_id
                    LEFT JOIN Event ON Event.id  = Account_Item.event_id
                    LEFT JOIN EventType ON EventType.id = Event.eventType_id
                    WHERE (Account_Item.service_id=%d
                        OR Visit.service_id=%d
                        OR EventType.service_id=%d)
                      AND Account_Item.event_id = (
                        SELECT AI.event_id
                        FROM Account_Item AS AI
                        WHERE AI.id=%d
                    )""" % (serviceId, serviceId, serviceId, accountItemId)
                query = self.db.query(stmt)
                if query:
                    while query.next():
                        record = query.record()
                        if not record:
                            break
                        result.append(forceRef(record.value(0)))
        return result


    def getServiceId(self, accountItemId):
        result = self.serviceCache.get(accountItemId, -1)
        if result == -1:
            result = None
            stmt = """SELECT
            IF(Account_Item.service_id IS NOT NULL,
                Account_Item.service_id,
                IF(Account_Item.visit_id IS NOT NULL,
                    Visit.service_id,
                    EventType.service_id)
                ) AS serviceId
            FROM Account_Item
            LEFT JOIN Visit ON Visit.id  = Account_Item.visit_id
            LEFT JOIN Event ON Event.id  = Account_Item.event_id
            LEFT JOIN EventType ON EventType.id = Event.eventType_id
            WHERE %s""" % self.tableAccountItem['id'].eq(accountItemId)
            query = self.db.query(stmt)
            if query.first():
                record = query.record()
                if record:
                    result = forceRef(record.value(0))
            self.serviceCache[accountItemId] = result
        return result


    def findClientByNameSexAndBirthDate(self, lastName, firstName, patrName, sex, birthDate):
        key = (lastName, firstName, patrName, sex, birthDate)
        result = self.clientCache.get(key, -1)
        if result == -1:
            result = None
            table = self.db.table('Client')
            filter = [table['deleted'].eq(0),
                        table['lastName'].eq(lastName),
                        table['firstName'].eq(firstName),
                        table['patrName'].eq(patrName),
                        table['birthDate'].eq(birthDate)]
            if sex != 0:
                filter.append(table['sex'].eq(sex))
            record = self.db.getRecordEx(table, 'id', filter, 'id')
            if record:
                result = forceRef(record.value(0))
            self.clientCache[key] = result
        return result


    def getClientId(self, accountItemId):
        result = self.clientByAccountItemIdCache.get(accountItemId, -1)
        if result == -1:
            result = None
            stmt = """SELECT Event.client_id
            FROM Account_Item
            LEFT JOIN Event ON Event.id = Account_Item.event_id
            WHERE %s""" % self.tableAccountItem['id'].eq(accountItemId)
            query = self.db.query(stmt)
            if query and query.first():
                record = query.record()
                if record:
                    result = forceRef(record.value(0))
            self.clientByAccountItemIdCache[accountItemId] = result
        return result


    def getClientIdByEventId(self, eventId):
        result = self.clientByEventIdCache.get(eventId, -1)
        if result == -1:
            result = forceRef(self.db.translate('Event', 'id', eventId, 'client_id'))
            self.clientByEventIdCache[eventId] = result
        return result


    def addClientPolicy(self, clientId, insurerId, serial, number, policyTypeId, policyKindId):
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
        self.db.insertRecord(table, record)


    def updateClientPolicy(self, clientId, insurerId, serial, number, newInsurerOGRN, policyKindId):
        logAp = ''
        record = selectLatestRecord('ClientPolicy', clientId,
            '(Tmp.`policyType_id` IN (%d,%d))' % \
              (self.policyTypeIndustrial, self.policyTypeTerritorial))
        if record:
             oldInsurerId = forceRef(record.value('insurer_id'))
             oldInsurerOGRN = forceString(self.db.translate('Organisation', 'id', oldInsurerId, 'OGRN'))
        else:
            logAp = u'Отсутствовали полисные данные / '
        if not record or (
                (insurerId and (forceRef(record.value('insurer_id')) != insurerId)
                    and (oldInsurerOGRN != newInsurerOGRN)) or
                (forceString(record.value('serial')) != serial) or
                (forceString(record.value('number')) != number)
            ):
            if record:
                oldInsurer = forceRef(record.value('insurer_id'))
                oldSerial = forceString(record.value('serial'))
                oldNumber = forceString(record.value('number'))
            else:
                oldInsurer = oldSerial = oldNumber = forceString(u'XXX')
            #Тип полиса не передаётся, поэтому всем выставляем производственный - forceRef(record.value('policyType_id'))
            policyType_id = forceRef('2')
            self.addClientPolicy(clientId, insurerId, serial, number, policyType_id, policyKindId)
            self.err2log(u'%sобновлен полис: `%s№%s (%s)` на `%s№%s (%s)`' % (logAp if logAp else '',
                         oldSerial if oldSerial else '', oldNumber if oldNumber else '',
                         oldInsurer if oldInsurer else 0, serial, number, insurerId if insurerId else 0))
            self.flagUpdatePolicy = 1


    def checkClientPolicy(self, clientId, policySN, OGRN, OKATO, policyKindId, smoCode):
        policy = policySN.split(u'№')
        insurerId = self.findInsurerByOGRNandOKATO(OGRN, OKATO)

#        insurerId = self.findInsurerBySmoCode(smoCode) if smoCode else self.findInsurerByOGRNandOKATO(OGRN, OKATO)
        if insurerId == '':
            return
        if policy == []:
            return
        policySerial = ''
        policyNumber = policy[0].strip()
        if len(policy)>1:
            policySerial = policy[0].strip()
            policyNumber = policy[1].strip()
        self.updateClientPolicy(clientId, insurerId, policySerial, policyNumber, OGRN, policyKindId)

