# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import QVariant, Qt, QPoint, QEvent, QAbstractTableModel

from library.Utils           import forceString, forceInt, forceDate, formatDate
from library.crbcombobox     import CRBComboBox
from library.InDocTable      import CRBInDocTableCol


class CPatientsModelComboBoxModel(QAbstractTableModel):
    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._items = []
        self._mapIdToIndex = {}


    def saveInternalData(self):
        return (self._items, self._mapIdToIndex)


    def restoreInternalData(self, state):
        if hasattr(self, 'beginResetModel'):
            self.beginResetModel()
        self._items = state[0]
        self._mapIdToIndex = state[1]
        if hasattr(self, 'endResetModel'):
            self.endResetModel()
        else:
            self.reset()


    def setTable(self, tableName, addNone=True, filter='', order=None, specialValues=None, *args):
        if specialValues:
            for fakeId, fakeCode, fakeDate, fakeName in specialValues:
                self._items.append((fakeId, fakeCode, fakeDate, fakeName))
        if addNone:
            self._items.append((None, '0', u'', u'не задано'))
            self._mapIdToIndex[None] = 0
        db = QtGui.qApp.db
        where = (' WHERE ' + filter) if filter else ''
        order = ' ORDER BY ' + (order if order else 'code, name')
        query = db.query('SELECT id, code, endDate, name FROM ' + tableName + where + order)
        index = len(self._items)
        if hasattr(self, 'beginResetModel'):
            self.beginResetModel()
        while query.next():
            id   = forceInt(query.value(0))
            code = forceString(query.value(1))
            endDate = forceDate(query.value(2))
            name = forceString(query.value(3))
            self._items.append((id, code, formatDate(endDate), name))
            self._mapIdToIndex[id] = index
            index += 1
        if hasattr(self, 'endResetModel'):
            self.endResetModel()
        else:
            self.reset()


    def columnCount(self, index=None):
        return 3


    def rowCount(self, index=None):
        return len(self._items)


    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role == Qt.DisplayRole or role == Qt.EditRole:
            row = index.row()
            if row < len(self._items):
                return QVariant(self._items[row][index.column()+1])
        return QVariant()


    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                if section == 0:
                    return QVariant(u'Код')
                elif section == 1:
                    return QVariant(u'Дата')
                elif section == 2:
                    return QVariant(u'Наименование')
        return QVariant()


    def searchId(self, itemId):
        result = self._mapIdToIndex.get(itemId, -1)
        if result < 0 and not itemId:
            result = self._mapIdToIndex.get(None, -1)
        return result


    def searchName(self, name):
        for i, item in enumerate(self._items):
            if item[3] == name:
                return i
        return -1


    def getId(self, index):
        return self._items[index][0]


    def getName(self, index):
        return self._items[index][3]


    def getCode(self, index):
        return self._items[index][1]


    def getDate(self, index):
        return self._items[index][2]


    def getString(self, index, showFields):
        if showFields == 0:
            return self.getCode(index)
        elif showFields == 1:
            return self.getDate(index)
        elif showFields == 2:
            return self.getName(index)
        elif showFields == 3:
            return '%-*s|%s' % ( self.maxCodeLen, self.getCode(index), self.getName(index))
        else:
            return 'bad field %s' % showFields


    def searchCode(self, code):
        code = unicode(code).upper()
        n = len(self._items)
        for i in xrange(n):
            if unicode(self.getCode(i)).upper().startswith(code):
                return i
        for i in xrange(n):
            if unicode(self.getName(i)).upper().startswith(code):
                return i
        return -1


    def searchCodeEx(self, code):
        def maxCommonLen(c1, c2):
            n = min(len(c1), len(c2))
            for i in xrange(n):
                if c1[i] != c2[i]:
                    return i
            return n

        code = unicode(code).upper()
        codeLen = len(code)
        n = len(self._items)
        maxLen = -1
        maxLenAt = -1
        for i in xrange(n):
            itemCode = unicode(self.getCode(i)).upper()
            commonLen = maxCommonLen(itemCode, code)
            if commonLen == codeLen == len(itemCode):
                return i, code
            if commonLen > maxLen:
                maxLen, maxLenAt = commonLen, i
        for i in xrange(n):
            itemName = unicode(self.getName(i)).upper()
            commonLen = maxCommonLen(itemName, code)
            if commonLen == codeLen == len(itemName):
                return i, code
            if commonLen > maxLen:
                maxLen, maxLenAt = commonLen, i
        return maxLenAt, code[:maxLen]



class CPatientsModelComboBoxPopupView(QtGui.QTableView):
    def __init__(self, parent):
        QtGui.QTableView.__init__(self, parent)
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        height = self.fontMetrics().height()
        self.sectionHeight = 3.0 * height / 2.0
        self.verticalHeader().setDefaultSectionSize(self.sectionHeight)
        self.verticalHeader().hide()
        self.horizontalHeader().hide()
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.horizontalHeader().setStretchLastSection(True)


    def resizeEvent(self, resizeEvent):
        QtGui.QTableView.resizeEvent(self, resizeEvent)
        self.resizeColumnToContents(0)


    def keyboardSearch(self, search):
        rowIndex, search = self.model().searchCodeEx(search)
        if rowIndex >= 0:
            index = self.model().index(rowIndex, 1)
            self.setCurrentIndex(index)


    def preferredWidth(self):
        return 100



class CPatientsModelComboBox(CRBComboBox):
    def __init__(self, parent=None):
        CRBComboBox.__init__(self, parent)
        self._model = CPatientsModelComboBoxModel(self)
        QtGui.QComboBox.setModel(self, self._model)
        self._selectionModel = QtGui.QItemSelectionModel(self._model)
        self.popupView = CPatientsModelComboBoxPopupView(self)
        QtGui.QComboBox.setView(self, self.popupView)
        self.popupView.setModel(self._model)
        self.popupView.setSelectionModel(self._selectionModel)
        self.popupView.setFrameShape(QtGui.QFrame.NoFrame)
        self.setShowFields(2)



class CPatientsModelTableCol(CRBInDocTableCol):
    def __init__(self, *args, **kwargs):
        CRBInDocTableCol.__init__(self, *args, **kwargs)
        self._state = None


    def createEditor(self, parent):
        editor = CPatientsModelComboBox(parent)
        if self._state:
            editor._model.restoreInternalData(self._state)
        else:
            editor.setTable(self.tableName)
            self._state = editor._model.saveInternalData()
        return editor


    def setEditorData(self, editor, value, record):
        result = CRBInDocTableCol.setEditorData(self, editor, value, record)

        # editor.showPopup() не хочет работать
        event = QtGui.QMouseEvent(QEvent.MouseButtonPress, QPoint(1,1),
            Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
        QtGui.qApp.postEvent(editor, event)
        return result
