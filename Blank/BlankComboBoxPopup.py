#!/usr/bin/env python
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

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QEvent, pyqtSignature, SIGNAL

from library.database import CTableRecordCache
from library.TableModel import CTableModel, CDateCol, CEnumCol, CIntCol, CTextCol
from library.Utils import forceInt, forceRef, forceString, getPref, setPref

from Blank.Ui_BlankComboBoxPopup import Ui_BlankComboBoxPopup

#__all__ = ( 'CBlankComboBoxPopup',
#            'CBlankComboBoxActionsPopup',
#            'CBlankNumberComboBoxActionsPopup',
#            'CBlankSerialNumberComboBoxActionsPopup',
#            'codeToTextForBlank',
#            'codeToTextForBlankNumber',
#            'codeToTextForBlankSerialNumber',
#          )


class CBlankComboBoxPopup(QtGui.QFrame, Ui_BlankComboBoxPopup):
    __pyqtSignals__ = ('BlankCodeSelected(int)',
                      )

    def __init__(self, parent = None, docTypeActions = False):
        QtGui.QFrame.__init__(self, parent, Qt.Popup)
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setAttribute(Qt.WA_WindowPropagation)
        self.tableModel = CBlankActionsTableModel(self) if docTypeActions else CBlankTableModel(self)
        self.tableSelectionModel = QtGui.QItemSelectionModel(self.tableModel, self)
        self.tableSelectionModel.setObjectName('tableSelectionModel')
        self.setupUi(self)
        self.tblBlank.setModel(self.tableModel)
        self.tblBlank.setSelectionModel(self.tableSelectionModel)
        self.code = None
        self.tblBlank.installEventFilter(self)
        preferences = getPref(QtGui.qApp.preferences.windowPrefs, 'CBlankComboBoxPopup', {})
        self.tblBlank.loadPreferences(preferences)
        self.docTypeActions = docTypeActions


    def mousePressEvent(self, event):
        parent = self.parentWidget()
        if parent!=None:
            opt=QtGui.QStyleOptionComboBox()
            opt.init(parent)
            arrowRect = parent.style().subControlRect(
                QtGui.QStyle.CC_ComboBox, opt, QtGui.QStyle.SC_ComboBoxArrow, parent)
            arrowRect.moveTo(parent.mapToGlobal(arrowRect.topLeft()))
            if (arrowRect.contains(event.globalPos()) or self.rect().contains(event.pos())):
                self.setAttribute(Qt.WA_NoMouseReplay)
        QtGui.QFrame.mousePressEvent(self, event)


    def closeEvent(self, event):
        preferences = self.tblBlank.savePreferences()
        setPref(QtGui.qApp.preferences.windowPrefs, 'CBlankComboBoxPopup', preferences)
        QtGui.QFrame.closeEvent(self, event)


    def eventFilter(self, watched, event):
        if watched == self.tblBlank:
            if event.type() == QEvent.KeyPress and event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Select):
                event.accept()
                index = self.tblBlank.currentIndex()
                self.tblBlank.emit(SIGNAL('doubleClicked(QModelIndex)'), index)
                return True
        return QtGui.QFrame.eventFilter(self, watched, event)


    def setBlankIdList(self, idList, posToId):
        self.tblBlank.setIdList(idList, posToId)
        self.tblBlank.setFocus(Qt.OtherFocusReason)


    def selectBlankCode(self, code):
        self.code = code
        self.emit(SIGNAL('BlankCodeSelected(int)'), code)
        self.close()


    def getCurrentBlankCode(self):
        db = QtGui.qApp.db
        if self.docTypeActions:
            table = db.table('BlankActions_Moving')
        else:
            table = db.table('BlankTempInvalid_Moving')
        id = self.tblBlank.currentItemId()
        code = None
        if id:
            record = db.getRecordEx(table, [table['id']], [table['deleted'].eq(0), table['id'].eq(id)])
            if record:
                code = forceInt(record.value(0))
            return code
        return None


    @pyqtSignature('QModelIndex')
    def on_tblBlank_doubleClicked(self, index):
        if index.isValid():
            if (Qt.ItemIsEnabled & self.tableModel.flags(index)):
                code = self.getCurrentBlankCode()
                self.selectBlankCode(code)


class CBlankComboBoxActionsPopup(QtGui.QFrame, Ui_BlankComboBoxPopup):
    __pyqtSignals__ = ('BlankCodeSelected(QString)',
                      )

    def __init__(self, parent = None, docTypeActions = False):
        QtGui.QFrame.__init__(self, parent, Qt.Popup)
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setAttribute(Qt.WA_WindowPropagation)
        self.tableModel = CBlankActionsTableModel(self) if docTypeActions else CBlankTableModel(self)
        self.tableSelectionModel = QtGui.QItemSelectionModel(self.tableModel, self)
        self.tableSelectionModel.setObjectName('tableSelectionModel')
        self.setupUi(self)
        self.tblBlank.setModel(self.tableModel)
        self.tblBlank.setSelectionModel(self.tableSelectionModel)
        self.code = None
#        self.parent = parent # скрывать Qt-шный parent - это плохая затея
        self.tblBlank.installEventFilter(self)
        preferences = getPref(QtGui.qApp.preferences.windowPrefs, 'CBlankComboBoxPopup', {})
        self.tblBlank.loadPreferences(preferences)
        self.docTypeActions = docTypeActions


    def mousePressEvent(self, event):
        parent = self.parentWidget()
        if parent is not None:
            opt=QtGui.QStyleOptionComboBox()
            opt.init(parent)
            arrowRect = parent.style().subControlRect(
                QtGui.QStyle.CC_ComboBox, opt, QtGui.QStyle.SC_ComboBoxArrow, parent)
            arrowRect.moveTo(parent.mapToGlobal(arrowRect.topLeft()))
            if (arrowRect.contains(event.globalPos()) or self.rect().contains(event.pos())):
                self.setAttribute(Qt.WA_NoMouseReplay)
        QtGui.QFrame.mousePressEvent(self, event)


    def closeEvent(self, event):
        preferences = self.tblBlank.savePreferences()
        setPref(QtGui.qApp.preferences.windowPrefs, 'CBlankComboBoxPopup', preferences)
        QtGui.QFrame.closeEvent(self, event)


    def eventFilter(self, watched, event):
        if watched == self.tblBlank:
            if event.type() == QEvent.KeyPress and event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Select):
                event.accept()
                index = self.tblBlank.currentIndex()
                self.tblBlank.emit(SIGNAL('doubleClicked(QModelIndex)'), index)
                return True
        return QtGui.QFrame.eventFilter(self, watched, event)


    def setBlankIdList(self, idList, posToId):
        self.tblBlank.setIdList(idList, posToId)
        self.tblBlank.setFocus(Qt.OtherFocusReason)


    def selectBlankCode(self, code):
        result = codeToTextForBlank(code, True)
        self.code = result
        self.emit(SIGNAL('BlankCodeSelected(QString)'), result)
        self.close()


    def getCurrentBlankCode(self):
        db = QtGui.qApp.db
        if self.docTypeActions:
            table = db.table('BlankActions_Moving')
            tableBlankTempInvalidParty = db.table('BlankActions_Party')
        else:
            table = db.table('BlankTempInvalid_Moving')
            tableBlankTempInvalidParty = db.table('BlankTempInvalid_Party')
        queryTable = tableBlankTempInvalidParty.innerJoin(table, table['blankParty_id'].eq(tableBlankTempInvalidParty['id']))
        id = self.tblBlank.currentItemId()
        code = None
        if id:
            record = db.getRecordEx(queryTable, [table['id']], [table['deleted'].eq(0), tableBlankTempInvalidParty['deleted'].eq(0), table['id'].eq(id)])
            if record:
                code = forceInt(record.value(0))
            return code
        return None


    @pyqtSignature('QModelIndex')
    def on_tblBlank_doubleClicked(self, index):
        if index.isValid():
            if (Qt.ItemIsEnabled & self.tableModel.flags(index)):
                code = self.getCurrentBlankCode()
                self.selectBlankCode(code)


class CBlankTableModel(CTableModel):
    def __init__(self, parent):
        CTableModel.__init__(self, parent)
        self.addColumn(CTextCol(u'Серия',          ['serial'], 30))
        self.addColumn(CTextCol(u'Номер с',        ['numberFrom'], 20))
        self.addColumn(CTextCol(u'Номер по',       ['numberTo'], 20))
        self.addColumn(CDateCol(u'Дата',           ['date'], 10))
        self.addColumn(CTextCol(u'Получено',       ['received'], 10))
        self.addColumn(CTextCol(u'Использовано',   ['used'], 10))
        self.addColumn(CTextCol(u'Возврат',        ['returnAmount'], 10))
        self.addColumn(CEnumCol(u'Контроль серии', ['checkingSerial'], [u'нет', u'мягко', u'жестко'], 5))
        self.addColumn(CEnumCol(u'Контроль номера',['checkingNumber'], [u'нет', u'мягко', u'жестко'], 5))
        self.addColumn(CEnumCol(u'Контроль количества',['checkingAmount'], [u'нет', u'использовано'], 5))
        self.addColumn(CIntCol( u'Длина КС',           ['checkSumLen'], 5))
        self.setTable('BlankTempInvalid_Moving')


    def flags(self, index):
        return Qt.ItemIsEnabled|Qt.ItemIsSelectable


    def setTable(self, tableName):
        db = QtGui.qApp.db
        tableRBBlankTempInvalids = db.table('rbBlankTempInvalids')
        tableBlankTempInvalidParty = db.table('BlankTempInvalid_Party')
        tableBlankTempInvalidMoving = db.table('BlankTempInvalid_Moving')
        loadFields = []
        loadFields.append(u'''DISTINCT BlankTempInvalid_Moving.id, BlankTempInvalid_Party.serial, BlankTempInvalid_Moving.numberFrom, BlankTempInvalid_Moving.numberTo, BlankTempInvalid_Moving.date, BlankTempInvalid_Moving.received, BlankTempInvalid_Moving.used, BlankTempInvalid_Moving.returnAmount, rbBlankTempInvalids.checkingSerial, rbBlankTempInvalids.checkingNumber, rbBlankTempInvalids.checkingAmount, rbBlankTempInvalids.checkSumLen''')
        queryTable = tableBlankTempInvalidMoving.innerJoin(tableBlankTempInvalidParty, tableBlankTempInvalidParty['id'].eq(tableBlankTempInvalidMoving['blankParty_id']))
        queryTable = queryTable.innerJoin(tableRBBlankTempInvalids, tableBlankTempInvalidParty['doctype_id'].eq(tableRBBlankTempInvalids['id']))
        self._table = queryTable
        self._recordsCache = CTableRecordCache(db, self._table, loadFields)


class CBlankActionsTableModel(CTableModel):
    def __init__(self, parent):
        CTableModel.__init__(self, parent)
        self.addColumn(CTextCol(u'Серия', ['serial'], 30))
        self.addColumn(CTextCol(u'Номер с', ['numberFrom'], 20))
        self.addColumn(CTextCol(u'Номер по', ['numberTo'], 20))
        self.addColumn(CDateCol(u'Дата', ['date'], 10))
        self.addColumn(CTextCol(u'Получено', ['received'], 10))
        self.addColumn(CTextCol(u'Использовано', ['used'], 10))
        self.addColumn(CTextCol(u'Возврат', ['returnAmount'], 10))
        self.addColumn(CEnumCol(u'Контроль серии', ['checkingSerial'], [u'нет', u'мягко', u'жестко'], 5))
        self.addColumn(CEnumCol(u'Контроль номера', ['checkingNumber'], [u'нет', u'мягко', u'жестко'], 5))
        self.addColumn(CEnumCol(u'Контроль количества', ['checkingAmount'], [u'нет', u'использовано'], 5))
        self.addColumn(CIntCol(u'Размер КС', ['checkSumLen'], 5))
        self.setTable('BlankActions_Moving')


    def flags(self, index):
        return Qt.ItemIsEnabled|Qt.ItemIsSelectable


    def setTable(self, tableName):
        db = QtGui.qApp.db
        tableRBBlankActions = db.table('rbBlankActions')
        tableBlankActionsParty = db.table('BlankActions_Party')
        tableBlankActionsMoving = db.table('BlankActions_Moving')
        loadFields = []
        loadFields.append(u'''DISTINCT BlankActions_Moving.id, BlankActions_Party.serial, BlankActions_Moving.numberFrom, BlankActions_Moving.numberTo, BlankActions_Moving.date, BlankActions_Moving.received, BlankActions_Moving.used, BlankActions_Moving.returnAmount, rbBlankActions.checkingSerial, rbBlankActions.checkingNumber, rbBlankActions.checkingAmount, rbBlankActions.checkSumLen''')
        queryTable = tableBlankActionsMoving.innerJoin(tableBlankActionsParty, tableBlankActionsParty['id'].eq(tableBlankActionsMoving['blankParty_id']))
        queryTable = queryTable.innerJoin(tableRBBlankActions, tableBlankActionsParty['doctype_id'].eq(tableRBBlankActions['id']))
        self._table = queryTable
        self._recordsCache = CTableRecordCache(db, self._table, loadFields)


class CBlankNumberComboBoxActionsPopup(CBlankComboBoxActionsPopup):

    def selectBlankCode(self, code):
        result = codeToTextForBlankNumber(code)
        self.code = result
        self.emit(SIGNAL('BlankCodeSelected(QString)'), result)
        self.close()


class CBlankSerialNumberComboBoxActionsPopup(CBlankComboBoxActionsPopup):

    def selectBlankCode(self, code):
        result = codeToTextForBlankSerialNumber(code)
        self.code = result
        self.emit(SIGNAL('BlankCodeSelected(QString)'), result)
        self.close()


def codeToTextForBlank(code, docTypeActions = False):
    text = ''
    if code:
        db = QtGui.qApp.db
        if docTypeActions:
#            tableRBBlankTempInvalids = db.table('rbBlankActions')
            tableBlankTempInvalidParty = db.table('BlankActions_Party')
            tableBlankTempInvalidMoving = db.table('BlankActions_Moving')
        else:
            #tableRBBlankTempInvalids = db.table('rbBlankTempInvalids')
            tableBlankTempInvalidParty = db.table('BlankTempInvalid_Party')
            tableBlankTempInvalidMoving = db.table('BlankTempInvalid_Moving')
        cols = [tableBlankTempInvalidParty['serial']]
        cond = [tableBlankTempInvalidParty['deleted'].eq(0),
                tableBlankTempInvalidMoving['deleted'].eq(0),
                tableBlankTempInvalidMoving['id'].eq(code)
                ]
        queryTable = tableBlankTempInvalidParty.innerJoin(tableBlankTempInvalidMoving, tableBlankTempInvalidMoving['blankParty_id'].eq(tableBlankTempInvalidParty['id']))
        records = db.getRecordEx(queryTable, cols, cond)
        text = forceString(records.value(0)) if records else u''
    return text


def codeToTextForBlankNumber(code):
    blankParams = {}
    blankIdList = []
    text = ''
    if code:
        db = QtGui.qApp.db
#        tableRBBlankTempInvalids = db.table('rbBlankActions')
        tableBlankTempInvalidParty = db.table('BlankActions_Party')
        tableBlankTempInvalidMoving = db.table('BlankActions_Moving')
        tableTempInvalid = db.table('TempInvalid')
#        tablePerson = db.table('Person')
        cols = [tableBlankTempInvalidMoving['id'].alias('blankMovingId'),
                tableBlankTempInvalidParty['serial'],
                tableBlankTempInvalidMoving['numberFrom'],
                tableBlankTempInvalidMoving['numberTo'],
                tableBlankTempInvalidMoving['returnAmount'],
                tableBlankTempInvalidMoving['used'],
                tableBlankTempInvalidMoving['received']
                ]
        cond = [tableBlankTempInvalidMoving['id'].eq(code),
                tableBlankTempInvalidParty['deleted'].eq(0),
                tableBlankTempInvalidMoving['deleted'].eq(0)
                ]
        cond.append('''BlankActions_Moving.received > (BlankActions_Moving.used - BlankActions_Moving.returnAmount)''')
        order = []
        queryTable = tableBlankTempInvalidParty.innerJoin(tableBlankTempInvalidMoving, tableBlankTempInvalidMoving['blankParty_id'].eq(tableBlankTempInvalidParty['id']))
        records = db.getRecordList(queryTable, cols, cond, order)
        for record in records:
            blankInfo = {}
            blankMovingId = forceRef(record.value('blankMovingId'))
            serial = forceString(record.value('serial'))
            numberFromString = forceString(record.value('numberFrom'))
            numberFromFirstChar = numberFromString[:1]
            numberFrom = int(numberFromString) if numberFromString else 0
            numberToString = forceString(record.value('numberTo'))
            numberTo = int(numberToString) if numberToString else 0
            returnAmount = forceInt(record.value('returnAmount'))
            used = forceInt(record.value('used'))
            received = forceInt(record.value('received'))
            blankInfo['serial'] = serial
            blankInfo['numberFromFirstChar'] = numberFromFirstChar
            blankInfo['numberFrom'] = numberFrom
            blankInfo['numberTo'] = numberTo
            blankInfo['returnAmount'] = returnAmount
            blankInfo['used'] = used
            blankInfo['received'] = received
            blankParams[blankMovingId] = blankInfo
            blankIdList.append(blankMovingId)
        if blankIdList:
            movingId = blankIdList[0]
        else:
            movingId = None
        if movingId:
            blankInfo = blankParams.get(movingId, None)
            if blankInfo:
                serial = forceString(blankInfo.get('serial', u''))
                numberFromFirstChar = blankInfo.get('numberFromFirstChar', u'')
                numberFrom = blankInfo.get('numberFrom', 0)
                numberTo = blankInfo.get('numberTo', 0)
                returnAmount = forceInt(blankInfo.get('returnAmount', 0))
                used = forceInt(blankInfo.get('used', 0))
                received = forceInt(blankInfo.get('received', 0))
                balance = received - used - returnAmount
                if balance > 0:
                    number = numberFrom + used + returnAmount
                    if number <= numberTo:
                        numberBlank = number
                        if numberFromFirstChar and numberFromFirstChar == u'0':
                            numberBlank = numberFromFirstChar + forceString(number)
                        record = db.getRecordEx(tableTempInvalid, [tableTempInvalid['id']], [tableTempInvalid['deleted'].eq(0), tableTempInvalid['serial'].eq(serial), tableTempInvalid['number'].eq(numberBlank)])
                        if not record:
                            text = forceString(numberBlank)
    return  text


def codeToTextForBlankSerialNumber(code):
    blankParams = {}
    blankIdList = []
    text = ''
    if code:
        db = QtGui.qApp.db
#        tableRBBlankTempInvalids = db.table('rbBlankActions')
        tableBlankTempInvalidParty = db.table('BlankActions_Party')
        tableBlankTempInvalidMoving = db.table('BlankActions_Moving')
        tableTempInvalid = db.table('TempInvalid')
#        tablePerson = db.table('Person')
        cols = [tableBlankTempInvalidMoving['id'].alias('blankMovingId'),
                tableBlankTempInvalidParty['serial'],
                tableBlankTempInvalidMoving['numberFrom'],
                tableBlankTempInvalidMoving['numberTo'],
                tableBlankTempInvalidMoving['returnAmount'],
                tableBlankTempInvalidMoving['used'],
                tableBlankTempInvalidMoving['received']
                ]
        cond = [tableBlankTempInvalidMoving['id'].eq(code),
                tableBlankTempInvalidParty['deleted'].eq(0),
                tableBlankTempInvalidMoving['deleted'].eq(0)
                ]
        cond.append('''BlankActions_Moving.received > (BlankActions_Moving.used - BlankActions_Moving.returnAmount)''')
        order = []
        queryTable = tableBlankTempInvalidParty.innerJoin(tableBlankTempInvalidMoving, tableBlankTempInvalidMoving['blankParty_id'].eq(tableBlankTempInvalidParty['id']))
        records = db.getRecordList(queryTable, cols, cond, order)
        for record in records:
            blankInfo = {}
            blankMovingId = forceRef(record.value('blankMovingId'))
            serial = forceString(record.value('serial'))
            numberFromString = forceString(record.value('numberFrom'))
            numberFromFirstChar = numberFromString[:1]
            numberFrom = int(numberFromString) if numberFromString else 0
            numberToString = forceString(record.value('numberTo'))
            numberTo = int(numberToString) if numberToString else 0
            returnAmount = forceInt(record.value('returnAmount'))
            used = forceInt(record.value('used'))
            received = forceInt(record.value('received'))
            blankInfo['serial'] = serial
            blankInfo['numberFromFirstChar'] = numberFromFirstChar
            blankInfo['numberFrom'] = numberFrom
            blankInfo['numberTo'] = numberTo
            blankInfo['returnAmount'] = returnAmount
            blankInfo['used'] = used
            blankInfo['received'] = received
            blankParams[blankMovingId] = blankInfo
            blankIdList.append(blankMovingId)
        if blankIdList:
            movingId = blankIdList[0]
        else:
            movingId = None
        if movingId:
            blankInfo = blankParams.get(movingId, None)
            if blankInfo:
                serial = forceString(blankInfo.get('serial', u''))
                numberFromFirstChar = blankInfo.get('numberFromFirstChar', u'')
                numberFrom = blankInfo.get('numberFrom', 0)
                numberTo = blankInfo.get('numberTo', 0)
                returnAmount = forceInt(blankInfo.get('returnAmount', 0))
                used = forceInt(blankInfo.get('used', 0))
                received = forceInt(blankInfo.get('received', 0))
                balance = received - used - returnAmount
                if balance > 0:
                    number = numberFrom + used + returnAmount
                    if number <= numberTo:
                        numberBlank = number
                        if numberFromFirstChar and numberFromFirstChar == u'0':
                            numberBlank = numberFromFirstChar + forceString(number)
                        record = db.getRecordEx(tableTempInvalid, [tableTempInvalid['id']], [tableTempInvalid['deleted'].eq(0), tableTempInvalid['serial'].eq(serial), tableTempInvalid['number'].eq(numberBlank)])
                        if not record:
                            text = forceString(serial) + u' ' + forceString(numberBlank)
    return  text


