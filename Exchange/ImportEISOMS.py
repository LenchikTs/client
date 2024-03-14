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

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDateTime, QDir, QVariant, pyqtSignature, SIGNAL

from library.dbfpy.dbf  import Dbf
from library.DbfViewDialog import CDbfViewDialog
from library.exception  import CException
from library.Utils      import checkBits, forceDouble, forceInt, forceRef, forceString, forceStringEx, toVariant

from Accounting.Utils import getRefuseTypeId, setActionPayStatus, setEventPayStatus, setVisitPayStatus, updateAccounts
from Events.Utils     import CFinanceType, CPayStatus, getPayStatusMask

from Exchange.ExportEISOMS import getAccountInfo
from Exchange.Ui_ImportEISOMSPage1 import Ui_ImportEISOMSPage1
from Exchange.Ui_ImportEISOMSPage2 import Ui_ImportEISOMSPage2
from Exchange.Utils import dbfCheckNames


def importEISOMS(widget, accountId):
    wizard = CImportEISOMSWizard(widget)
    wizard.setAccountId(accountId)
    wizard.exec_()


class CImportEISOMSWizard(QtGui.QWizard):
    def __init__(self, parent=None):
        QtGui.QWizard.__init__(self, parent)
        self.setWizardStyle(QtGui.QWizard.ModernStyle)
        self.page1 = CImportEISOMSPage1(self)
        self.page2 = CImportEISOMSPage2(self)
        self.addPage(self.page1)
        self.addPage(self.page2)
        self.setWindowTitle(u'Мастер обработки обменного файла ЕИС.ОМС.ВМУ.АПУ')
        self.dbfFileName = ''
        self.accountId = None
        self.dbf = None
        self.removeFileAfterImport = True
        self.importAfterSMOCheck = False

    def setAccountId(self, accountId):
        self.accountId = accountId
        date, number, self.dbfFileName = getAccountInfo(accountId)


#    def exec_(self):
#        QtGui.QWizard.exec_(self)
#        self.cleanup()


class CImportEISOMSPage1(QtGui.QWizardPage, Ui_ImportEISOMSPage1):

    def __init__(self, parent):
        QtGui.QWizardPage.__init__(self, parent)
        self.setupUi(self)
        self.setTitle(u'Импорт возвратных данных из ЕИС ОМС')
        self.setSubTitle(u'выберите файл')

        homePath = QDir.toNativeSeparators(QDir.homePath())
        self.exchangeDir = forceString(QtGui.qApp.preferences.appPrefs.get('EISOMSExportDir', homePath))
        self.edtFileName.setText(self.exchangeDir)


    def initializePage(self):
        filePath = os.path.join(self.exchangeDir, self.wizard().dbfFileName + '.dbf')
        self.edtFileName.setText(filePath)
        self.chkRemoveFileAfterImport.setChecked(self.wizard().removeFileAfterImport)
        self.chkImportAfterSMOCheck.setChecked(self.wizard().importAfterSMOCheck)


    @pyqtSignature('QString')
    def on_edtFileName_textChanged(self):
#        fileName = forceStringEx(self.edtFileName.text())
#        fileIsValid = os.path.isfile(fileName))
#        if fileIsValid:
        self.emit(SIGNAL('completeChanged()'))


    @pyqtSignature('')
    def on_btnSelectFile_clicked(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                u'Укажите файл с данными из ЕИС-ОМС',
                forceStringEx(self.edtFileName.text()),
                u'Файлы DBF (*.dbf)')
        if forceString(fileName):
            self.edtFileName.setText(QDir.toNativeSeparators(fileName))

    @pyqtSignature('')
    def on_btnView_clicked(self):
        fname=unicode(forceStringEx(self.edtFileName.text()))
        if fname:
            CDbfViewDialog(self, fileName=fname).exec_()

    def isComplete(self):
        fileName = forceStringEx(self.edtFileName.text())
        return os.path.isfile(fileName)


    def validatePage(self):
        success, result = QtGui.qApp.call(self, self.openDbf)
        return success and result


    def openDbf(self):
        dbf = None

        fileName = forceStringEx(self.edtFileName.text())
        result = os.path.isfile(fileName)
        if result:
            dbf = Dbf(fileName, readOnly=True, encoding='cp866')
#            fieldsList = ['SEND', 'ERROR', 'ACC_ID', 'ACCITEM_ID', 'CLIENT_ID']
            fieldsList = ['SEND', 'ERROR', 'ACC_ID', 'ACCITEM_ID']
            if not dbfCheckNames(dbf, fieldsList):
                raise CException(u'файл %s\nне содержит одного из полей:\n%s' % (fileName, ', '.join(fieldsList)))
            self.wizard().dbf = dbf
            self.wizard().removeFileAfterImport = self.chkRemoveFileAfterImport.isChecked()
            self.wizard().importAfterSMOCheck = self.chkImportAfterSMOCheck.isChecked()
        return result


class CImportEISOMSPage2(QtGui.QWizardPage, Ui_ImportEISOMSPage2):

    aisAccepted = 0         # account item state - принято
    aisRefused  = 1         # отказано
    aisIntegrityError = 2   # нарушение целостности
    aisChangeDisabled = 3   # нельзя изменить состояние account item
    aisUnchecked = 4        # запись не обработана в ЕИС ОМС
    aisCount = 5

    def __init__(self, parent):
        QtGui.QWizardPage.__init__(self, parent)
        self.setupUi(self)
        self.setTitle(u'Импорт возвратных данных из ЕИС ОМС')
        self.setSubTitle(u'дождитесь завершения работы и нажмите кнопку "финиш"')
        self.done = False
        self.aborted = False
        self.connect(self, SIGNAL('import()'), self.import_, Qt.QueuedConnection)
        self.connect(parent, SIGNAL('rejected()'), self.abort)
        self.indicators = [ self.lblAccepted,
                            self.lblRefused,
                            self.lblIntegrityError,
                            self.lblChangeDisabled,
                            self.lblUnchecked ]
        self.autoRegisterPayRefuseType = True

    def initializePage(self):
        self.counts = [0] * self.aisCount
        for indicator in self.indicators:
            indicator.setText('0')
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(1)
        self.progressBar.setValue(0)
        self.progressBar.setFormat('%v')
        self.emit(SIGNAL('import()'))


    def cleanupPage(self):
        self.abort()


    def import_(self):
        self.prepareImport()
        success,  result = QtGui.qApp.call(self, self.importInt)
        self.doneImport(self.aborted or not success)


    def prepareImport(self):
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(len(self.wizard().dbf))
        self.progressBar.setValue(0)
        self.done = False
        self.aborted = False


    def abort(self):
        self.aborted = True


    def doneImport(self, abnormal):
        if abnormal:
            self.progressBar.setText(u'прервано')
        else:
            if self.wizard().removeFileAfterImport:
                dbfName = self.wizard().dbf.name
                self.wizard().dbf = None
                dirname, basename = os.path.split(dbfName)
                main, ext = os.path.splitext(basename)
                for (prefix, suffix) in ( ('pat_', ''),
                                          ('',     ''),
                                          ('',     '_V'),
                                          ('',     '_add'),
                                          ('',     '_D')    ):
                    name = os.path.join(dirname, ''.join((prefix, main, suffix, ext)))
                    try:
                        os.unlink(name)
                    except:
                        pass
            self.progressBar.setText(u'готово')
        self.done = True
        self.aborted = False
        self.emit(SIGNAL('completeChanged()'))


    def importInt(self):
        dbf = self.wizard().dbf
        if dbf:
            self.docDate = toVariant(QDateTime.fromTime_t(int(os.path.getmtime(dbf.name))).date())
            self.docName = toVariant(os.path.basename(dbf.name))
            self.progressBar.setMinimum(0)
            self.progressBar.setMaximum(len(dbf))
            self.progressBar.setValue(0)
            self.progressBar.setFormat('%v')

            self.db = QtGui.qApp.db
            self.financeId = CFinanceType.getId(CFinanceType.CMI)
            assert self.financeId
            self.tableAccountItem = self.db.table('Account_Item')
            self.tableEvent = self.db.table('Event')
            self.tableVisit = self.db.table('Visit')
            self.tableAction = self.db.table('Action')
            self.payStatusMask = getPayStatusMask(self.financeId)
            self.mapErrorMessageToId = {}
            self.accountIdSet = set()

            self.processedAccountItemIds = set()
            try:
                for row in dbf:
                    QtGui.qApp.processEvents()
                    if self.aborted:
                        break
                    self.progressBar.step()
                    self.process(row)
            finally:
                updateAccounts(self.accountIdSet)


    def process(self, row):
        send = row['SEND']
        error = row['ERROR']
        if 'PRIM' in row.dbf.header.fields:
            note = row['PRIM']
        else:
            note = ''
        importAfterSMOCheck = self.wizard().importAfterSMOCheck
        needProcessAccountItem = send and not importAfterSMOCheck or error

        accountId = row['ACC_ID']
        accountItemIdList = unicode(row['ACCITEM_ID']).split()
        for accountItemIdAsStr in accountItemIdList:
            if needProcessAccountItem:
                if accountItemIdAsStr and accountItemIdAsStr.isdigit():
                    accountItemId = int(accountItemIdAsStr)
                    self.processAccountItem(accountId, accountItemId, send, error, note)
                else:
                    self.countRecord(self.aisIntegrityError) # запись в AccountItem не найдена
            else:
                self.countRecord(self.aisUnchecked) # запись не обработана в ЕИС ОМС


    def processAccountItem(self, accountId, accountItemId, send, error, note):
        importAfterSMOCheck = self.wizard().importAfterSMOCheck

        if accountItemId in self.processedAccountItemIds:
            return
        self.processedAccountItemIds.add(accountItemId)

        accountItem = self.db.getRecord(self.tableAccountItem,
                'id, master_id, date, number, refuseType_id, event_id, visit_id, action_id, reexposeItem_id, note, payedSum, sum',
                accountItemId
                )
        if accountItem:
            eventId  = forceRef(accountItem.value('event_id'))
            visitId  = forceRef(accountItem.value('visit_id'))
            actionId = forceRef(accountItem.value('action_id'))
        else:
            eventId  = None
            visitId  = None
            actionId = None

        if actionId:
            setPayStatus = setActionPayStatus
            payedEntityId = actionId
            payedEntityTable = self.tableAction
        elif visitId:
            setPayStatus = setVisitPayStatus
            payedEntityId = visitId
            payedEntityTable = self.tableVisit
        elif eventId:
            setPayStatus = setEventPayStatus
            payedEntityId = eventId
            payedEntityTable = self.tableEvent
        else:
            setPayStatus = None
            payedEntityId = None
            payedEntityTable = None

        if payedEntityId:
            payStatus = forceInt(self.db.translate(payedEntityTable, 'id', payedEntityId, 'payStatus'))
        else:
            payStatus = 0

        if not accountItem:
            self.countRecord(self.aisIntegrityError) # запись в AccountItem не найдена
        elif forceRef(accountItem.value('master_id')) != accountId:
            self.countRecord(self.aisIntegrityError) # запись в AccountItem найдена, но что-то не хорошо с целостностью данных
        elif not(accountItem.isNull('date') or
                 (not accountItem.isNull('date') and not accountItem.isNull('refuseType_id'))):
            self.countRecord(self.aisChangeDisabled) # запись в AccountItem уже имеет отметку об оплате
        elif not accountItem.isNull('reexposeItem_id'):
            self.countRecord(self.aisChangeDisabled) # запись в AccountItem уже перевыставлена
        elif not (   checkBits(payStatus, self.payStatusMask, CPayStatus.exposedBits)
                  or checkBits(payStatus, self.payStatusMask, CPayStatus.refusedBits)):
            self.countRecord(self.aisChangeDisabled) # состояние визита отличается от "выставлено" или "отказано"
        else:
            accountItem.setValue('date', self.docDate)
            if note:
                accountItem.setValue('note', toVariant(note))
            if send:
                accountItem.setValue('number', QVariant(u'Принято ЕИС'))
                accountItem.setValue('refuseType_id', QVariant())
                accountItem.setValue('payedSum', forceDouble(accountItem.value('sum')))
                payStatusBits = CPayStatus.payedBits
            else:
                accountItem.setValue('refuseType_id', self.encodeError(error))
                accountItem.setValue('number', QVariant(u'Отказано СМО' if importAfterSMOCheck else u'Отказано ЕИС'))
                payStatusBits = CPayStatus.refusedBits
            self.accountIdSet.add(accountId)
            self.db.transaction()
            try:
                self.db.updateRecord(self.tableAccountItem, accountItem)
                setPayStatus(payedEntityId, self.payStatusMask, payStatusBits)
                self.db.commit()
            except:
                self.db.rollback()
                QtGui.qApp.logCurrentException()
                raise
            if send:
                self.countRecord(self.aisAccepted)
            else:
                self.countRecord(self.aisRefused)


    def countRecord(self, code):
        self.counts[code]+=1
        self.indicators[code].setText(str(self.counts[code]))


    def findError(self, errorMessage):
        return toVariant(getRefuseTypeId(errorMessage, True, self.financeId, True))


    def encodeError(self, errorMessage):
        result = self.mapErrorMessageToId.get(errorMessage, None)
        if not result:
            result = self.findError(errorMessage)
            if not result:
                result = self.findError(u'Неизвестная ошибка')
            if not result:
                result = QVariant()
            self.mapErrorMessageToId[errorMessage] = result
        return result


    def isComplete(self):
        return self.done


#    def validatePage(self):
#        src = self.wizard().getFullDbfFileName()
#        dst = os.path.join(forceStringEx(self.edtDir.text()), os.path.basename(src))
#        success, result = QtGui.qApp.call(self, shutil.move, (src, dst))
#        if success:
#            QtGui.qApp.preferences.appPrefs['EISOMSExportDir'] = toVariant(self.edtDir.text())
#        return success
