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
u"""Импорт отказов оплаты, Ленобласть"""


from PyQt4 import QtGui
from PyQt4.QtCore import QFile, QString

from library.Utils import forceString, toVariant, forceInt, forceRef

from Accounting.Utils import updateDocsPayStatus
from Events.Utils import CPayStatus, getPayStatusMask
from Exchange.Cimport import CXMLimport
from Exchange.Utils import tbl

from Exchange.Ui_ImportPayRefuseR29 import Ui_Dialog


def importPayRefuseR47Native(widget, accountId, accountItemIdList):
    u"""Создает диалог импорта отказов"""
    dlg = CImportPayRefuse(accountId, accountItemIdList)
    prefs = QtGui.qApp.preferences.appPrefs
    dlg.edtFileName.setText(
        forceString(prefs.get('importPayRefuseR47FileName', '')))
    dlg.exec_()
    prefs['importPayRefuseR47FileName'] = toVariant(dlg.edtFileName.text())


class CImportPayRefuse(QtGui.QDialog, Ui_Dialog, CXMLimport):

    prFields = ('OSHIB', 'IM_POL', 'BAS_EL', 'N_ZAP', 'IDCASE', 'IDSERV',
        'COMMENT')
    prGroupName = 'PR'
    flkpGroupName = 'FLK_P'
    flkpFields = ('FNAME', 'FNAME_I')

    def __init__(self, accountId, accountItemIdList):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        CXMLimport.__init__(self)
        self.accountId = accountId
        self.accountItemIdList = accountItemIdList
        self.progressBar.setFormat('%p%')
        self.checkName()
        self.aborted = False

        self.nProcessed = 0
        self.nUpdated = 0
        self.tblAccountItem = tbl('Account_Item')
        self.tblEvent = tbl('Event')
        self.tblAcc=self.db.join(self.tblAccountItem, self.tblEvent,
            'Account_Item.event_id=Event.id')

        self.chkOnlyCurrentAccount.setVisible(False)
        self.chkImportPayed.setVisible(False)
        self.chkImportRefused.setVisible(False)
        self.labelNum.setVisible(False)


    def setImportMode(self, flag):
        pass


    def startImport(self):
        self.nProcessed = 0
        self.nUpdated = 0
        params = {}

        contractId = forceRef(self.db.translate(
            'Account', 'id', self.accountId, 'contract_id'))
        financeId = forceRef(self.db.translate(
            'Contract', 'id', contractId, 'finance_id'))
        params['payStatusMask'] = getPayStatusMask(financeId)

        if not self.readFile(self.edtFileName.text(), params):
            self.logError(u'Ошибка импорта данных')
        else:
            self.err2log(u'Импорт завершен успешно')

        self.err2log(u'Импорт элементов: %d обновлено;'
            u' %d обработано' % (
            self.nUpdated, self.nProcessed))



    def processItem(self, item, params):
        self.nProcessed += 1
        refuseTypeId = self.getRefuseTypeId(item['OSHIB'])

        if not refuseTypeId:
            self.err2log(u'Неизвестный код причины отказа `%s`' % item['OSHIB'])
            return

        note = u'ФЛК не пройден. %s. Ошибка в поле %s, базовый элемент %s' % (
                item['COMMENT'], item['IM_POL'], item['BAS_EL'])

        try:
            accountItemNum = forceInt(item['IDSERV']) - 1
        except ValueError:
            accountItemNum = None

        try:
            eventId = forceRef(item['IDCASE'])
        except ValueError:
            eventId = None

        try:
            recordNum = forceInt(item['N_ZAP']) -1
        except ValueError:
            recordNum = None

        cond = [self.tblAccountItem['id'].inlist(self.accountItemIdList)]

        if eventId:
            cond.append(self.tblAccountItem['event_id'].eq(eventId))

        fields = 'Account_Item.id'
        order = 'Event.client_id, Account_Item.id'
        recordList = self.db.getRecordList(self.tblAcc, fields, cond, order)

        if recordList:
            if eventId and accountItemNum < len(recordList):
                itemList = [recordList[accountItemNum]]
            elif not eventId and recordNum < len(recordList):
                itemList = [recordList[recordNum]]
            elif eventId: # заполняем для всех
                itemList = recordList
            else:
                self.err2log(u'Невозможно определить элемент для отказа')
                return

            for i in itemList:
                _id = forceRef(i.value(0))
                accItem = self.db.getRecord(self.tblAccountItem, '*', _id)
                accItem.setValue('note', toVariant(note))
                accItem.setValue('refuseType_id', refuseTypeId)
                updateDocsPayStatus(accItem, params['payStatusMask'],
                    CPayStatus.refusedBits)
                self.db.updateRecord(self.tableAccountItem, accItem)

            self.nUpdated += 1
        else:
            self.err2log(u'Записи не найдены для IDSERV=`%s`, IDCASE=`%s`, '
                u'N_ZAP=`%s`' % (item['IDSERV'], item['IDCASE'], item['N_ZAP']))


    def readHeader(self, params):
        u''' Разбирает заголовок'''

        while not self.atEnd():
            self.readNext()

            if self.isStartElement():
                if (self.name() == self.flkpGroupName
                        or self.name() == 'FNAME'):
                    continue
                elif self.name() == 'FNAME_I':
                    while not (self.atEnd() or self.isEndElement()):
                        self.readNext()
                    return True
                else:
                    self.raiseError(u'Неверный формат экспорта данных.')

        return False


    def readData(self, params):
        #assert self.isStartElement()

        while not self.atEnd():
            QtGui.qApp.processEvents()
            self.readNext()

            if self.isEndElement():
                break

            if self.isStartElement():
                if self.name() == self.prGroupName:
                    yield self.readGroupEx(self.prGroupName, self.prFields)
                else:
                    self.readUnknownElement()

            if self.hasError() or self.aborted:
                break


    def readFile(self, fileName, params):
        u"""Разбирает указанный XML файл, отправляет данные в БД"""
        if not fileName:
            return False

        self.setImportMode(True)
        inFile = QFile(fileName)

        if not inFile.open(QFile.ReadOnly | QFile.Text):
            QtGui.QMessageBox.warning(self, u'Импорт данных из XML',
                  QString(u'Не могу открыть файл для чтения %1:\n%2.')
                  .arg(fileName)
                  .arg(inFile.errorString()))
            return False

        self.progressBar.setFormat(u'%v байт')
        self.progressBar.setMaximum(max(inFile.size(), 1))
        self.setDevice(inFile)

        if self.readHeader(params):
            for item in self.readData(params):
                self.progressBar.setValue(inFile.pos())
                QtGui.qApp.processEvents()

                if item:
                    self.processItem(item, params)

                if self.aborted:
                    break

        if not (self.hasError() or self.aborted):
            self.err2log(u'Готово')
            return True
        else:
            self.err2log(u'Прервано')

            if self.aborted:
                self.err2log(u'! Прервано пользователем.')
            else:
                self.err2log(u'! Ошибка: файл %s, %s' % (fileName,
                    self.errorString()))

            return False
