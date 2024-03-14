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

from random import randint
from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QAbstractTableModel, QObject, SIGNAL, QDateTime, QEvent, QModelIndex, QString, QVariant

from library.DbEntityCache import CDbEntityCache
from library.adjustPopup import adjustPopupToWidget


def getRBCheckSum(tableName):
    return QtGui.qApp.db.rbChecksum(tableName)


#    query = QtGui.qApp.db.query('SELECT SUM(CRC32(CONCAT_WS(CHAR(127), id, code, name))) FROM %s' % tableName)
#    if query.next():
#        record = query.record()
#        return record.value(0).toInt()[0]
#    else:
#        return 0


class CAbstractRBModelData(object):
    def __init__(self):
        self.buff = []
        self.maxCodeLen = 0
        self.mapIdToIndex = {}

    def addItem(self, id, code, name):
        self.mapIdToIndex[id] = len(self.buff)
        self.buff.append((id, code, name))
        self.maxCodeLen = max(self.maxCodeLen, len(code))

    def getCount(self):
        return len(self.buff)

    def getId(self, index):
        if index < 0:
            return None
        return self.buff[index][0]

    def getCode(self, index):
        if index < 0:
            return None
        return self.buff[index][1]

    def getName(self, index):
        return self.buff[index][2]

    def getIndexById(self, id):
        result = self.mapIdToIndex.get(id, -1)
        if result < 0 and not id:
            result = self.mapIdToIndex.get(None, -1)
        return result

    def getIndexByCode(self, code):
        for i, item in enumerate(self.buff):
            if item[1] == code:
                return i
        return -1

    def getIndexByName(self, name):
        for i, item in enumerate(self.buff):
            if item[2] == name:
                return i
        return -1

    def getIndexByCodeName(self, code, name):
        for i, item in enumerate(self.buff):
            if item[1] == code and item[2] == name:
                return i
        return -1

    def getNameById(self, id):
        index = self.getIndexById(id)
        if index >= 0:
            return self.getName(index)
        return '{' + str(id) + '}'

    def getCodeById(self, id):
        index = self.getIndexById(id)
        if index >= 0:
            return self.getCode(index)
        return '{' + str(id) + '}'

    def getIdByCode(self, code):
        index = self.getIndexByCode(code)
        return self.getId(index)

    def getString(self, index, showFields):
        if showFields == 0:
            return self.getCode(index)
        elif showFields == 1:
            return self.getName(index)
        elif showFields == 2:
            return '%-*s | %s' % (self.maxCodeLen, self.getCode(index), self.getName(index))
        else:
            return 'bad field %s' % showFields

    def getStringById(self, id, showFields):
        index = self.getIndexById(id)
        if index >= 0:
            return self.getString(index, showFields)
        return '{' + str(id) + '}'


class CRBModelData(CAbstractRBModelData):
    """class for store data of ref book"""

    def __init__(self, tableName, addNone, filter, order, specialValues):
        CAbstractRBModelData.__init__(self)
        self._tableName = tableName
        self._addNone = addNone
        self._filter = filter
        self._order = order
        self._checkSum = None
        self._timestamp = None
        self._specialValues = specialValues
        self._notLoaded = True

    def getCount(self):
        if self._notLoaded:
            self.load()
        return len(self.buff)

    def getId(self, index):
        if self._notLoaded:
            self.load()
        return CAbstractRBModelData.getId(self, index)

    def getCode(self, index):
        if self._notLoaded:
            self.load()
        return CAbstractRBModelData.getCode(self, index)

    def getName(self, index):
        if self._notLoaded:
            self.load()
        return CAbstractRBModelData.getName(self, index)

    def getIndexById(self, id):
        if self._notLoaded:
            self.load()
        return CAbstractRBModelData.getIndexById(self, id)

    def getIndexByCode(self, code):
        if self._notLoaded:
            self.load()
        return CAbstractRBModelData.getIndexByCode(self, code)

    def getIndexByCodeName(self, code, name):
        if self._notLoaded:
            self.load()
        return CAbstractRBModelData.getIndexByCodeName(self, code, name)

    def getIndexByName(self, name):
        if self._notLoaded:
            self.load()
        return CAbstractRBModelData.getIndexByName(self, name)

    def getNameById(self, id):
        if self._notLoaded:
            self.load()
        return CAbstractRBModelData.getNameById(self, id)

    def getCodeById(self, id):
        if self._notLoaded:
            self.load()
        return CAbstractRBModelData.getCodeById(self, id)

    def getString(self, index, showFields):
        if self._notLoaded:
            self.load()
        return CAbstractRBModelData.getString(self, index, showFields)

    def getStringById(self, id, showFields):
        if self._notLoaded:
            self.load()
        return CAbstractRBModelData.getStringById(self, id, showFields)

    def load(self):
        if self._specialValues:
            for fakeId, fakeCode, name in self._specialValues:
                self.addItem(fakeId, fakeCode, name)
        if self._addNone:
            self.addItem(None, '0', u'не задано')
        db = QtGui.qApp.db
        where = (' WHERE ' + self._filter) if self._filter else ''
        # добавил cast(code as signed) для корректной сортировки
        order = ' ORDER BY ' + (self._order if self._order else 'cast(code as signed), code, name')
        query = db.query('SELECT id, code, name FROM ' + self._tableName + where + order)
        value = query.value
        while query.next():
            id = value(0).toInt()[0]
            code = value(1).toString()
            name = value(2).toString()
            self.addItem(id, code, name)
        self._timestamp = QDateTime.currentDateTime()
        self._checkSum = getRBCheckSum(self._tableName)
        self._notLoaded = False

    def isObsolete(self):
        now = QDateTime.currentDateTime()
        if self._timestamp and self._timestamp.secsTo(now) > randint(300, 600):  ## magic
            checkSum = getRBCheckSum(self._tableName)
            if self._checkSum == checkSum:
                self._timestamp = now
                return False
            return True
        else:
            return False

    def isLoaded(self):
        return not self._notLoaded


class CRBModelDataCache(CDbEntityCache):
    mapTableToData = {}

    @classmethod
    def getData(cls, tableName, addNone=True, filter='', order=None, specialValues=None, needCache=True, force=False):
        strTableName = unicode(tableName)
        if isinstance(specialValues, list):
            specialValues = tuple(specialValues)
        key = (strTableName, addNone, filter, order, specialValues)
        result = cls.mapTableToData.get(key, None)
        if not result or force or result.isObsolete():
            result = CRBModelData(strTableName, addNone, filter, order, specialValues)
            cls.connect()
            if needCache:
                cls.mapTableToData[key] = result
        return result

    @classmethod
    def reset(cls, tableName=None):
        if tableName:
            for key in cls.mapTableToData.keys():
                if key[0] == tableName:
                    del cls.mapTableToData[key]
        else:
            cls.mapTableToData.clear()

    @classmethod
    def purge(cls):
        cls.reset()


class CRBModel(QAbstractTableModel):
    def __init__(self, parent):
        QAbstractTableModel.__init__(self, parent)
        self.d = None
        self.resetRequired = False
        self.readOnly = False

    def setReadOnly(self, value=False):
        self.readOnly = value

    def isReadOnly(self):
        return self.readOnly

    def flags(self, index=QModelIndex()):
        result = QAbstractTableModel.flags(self, index)
        if self.readOnly:
            result = Qt.ItemIsEnabled
        return result

    def setTable(self, tableName, addNone=True, filter='', order=None, specialValues=None, needCache=True, force=False):
        d = self.d
        if d and d.isLoaded() or self.resetRequired:
            if hasattr(self, 'beginResetModel'):
                self.beginResetModel()
            self.d = CRBModelDataCache.getData(tableName, addNone, filter, order, specialValues, needCache, force)
            if hasattr(self, 'endResetModel'):
                self.endResetModel()
            else:
                self.reset()
        else:
            self.d = CRBModelDataCache.getData(tableName, addNone, filter, order, specialValues, needCache, force)

    def columnCount(self, index=None):
        return 3

    def rowCount(self, index=None):
        if self.d:
            return self.d.getCount()
        else:
            self.resetRequired = True
            return 0

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                if section == 0:
                    return QVariant(u'Код')
                elif section == 1:
                    return QVariant(u'Наименование')
        return QVariant()

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role == Qt.DisplayRole or role == Qt.EditRole:
            row = index.row()
            if row < self.d.getCount():
                return QVariant(self.d.getString(row, index.column()))
        return QVariant()

    #    def codes(self):
    #        return [forceString(self.data(self.index(i, 0), Qt.DisplayRole)) for i in xrange(self.rowCount())]

    #    def names(self):
    #        return [forceString(self.data(self.index(i, 1), Qt.DisplayRole)) for i in xrange(self.rowCount())]

    def searchId(self, itemId):
        return self.d.getIndexById(itemId)

    #    def searchCode(self, code):
    #        return self.d.getIndexByCode(code)

    def searchName(self, name):
        return self.d.getIndexByName(name)

    def getId(self, index):
        return self.d.getId(index)

    def getName(self, index):
        return self.d.getName(index)

    def getCode(self, index):
        return self.d.getCode(index)

    def searchCode(self, code):
        code = unicode(code).upper()
        n = self.d.getCount()
        for i in xrange(n):
            if unicode(self.d.getCode(i)).upper().startswith(code):
                return i
        for i in xrange(n):
            if unicode(self.d.getName(i)).upper().startswith(code):
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
        n = self.d.getCount()
        maxLen = -1
        maxLenAt = -1
        for i in xrange(n):
            itemCode = unicode(self.d.getCode(i)).upper()
            commonLen = maxCommonLen(itemCode, code)
            if commonLen == codeLen == len(itemCode):
                return i, code
            if commonLen > maxLen:
                maxLen, maxLenAt = commonLen, i
        for i in xrange(n):
            itemName = unicode(self.d.getName(i)).upper()
            commonLen = maxCommonLen(itemName, code)
            if commonLen == codeLen == len(itemName):
                return i, code
            if commonLen > maxLen:
                maxLen, maxLenAt = commonLen, i
        return maxLenAt, code[:maxLen]


class CRBLikeEnumModel(CRBModel):
    def __init__(self, parent):
        CRBModel.__init__(self, parent)
        self.d = None

    def setValues(self, values):
        self.d = CAbstractRBModelData()
        for i, val in enumerate(values):
            id = i
            code = str(i)
            name = val
            self.d.addItem(id, code, name)


class CRBSelectionModel(QtGui.QItemSelectionModel):
    def select(self, indexOrSelection, command):
        if isinstance(indexOrSelection, QModelIndex):
            index = indexOrSelection
            ##            print 'select-2', index.column()
            if index.column() > 1:
                correctIndex = self.model().index(index.row(), 1)
            else:
                correctIndex = index
            if command & QtGui.QItemSelectionModel.Select and not (command & QtGui.QItemSelectionModel.Current):
                self.setCurrentIndex(correctIndex,
                                     QtGui.QItemSelectionModel.Clear | QtGui.QItemSelectionModel.Select | QtGui.QItemSelectionModel.Current)
            else:
                QtGui.QItemSelectionModel.select(self, correctIndex, command)

        else:
            QtGui.QItemSelectionModel.select(self, indexOrSelection, command)


#        index = None
#        if isinstance(indexOrSelection, QtGui.QItemSelection):
#            QtGui.QItemSelectionModel.select(self, indexOrSelection, command)
#            indexes = indexOrSelection.indexes()
#            if indexes:
#                index = indexes[0]
#        elif isinstance(indexOrSelection, QModelIndex):
#            index = indexOrSelection
#        if index:
#            print 'select', index.column()
#            if index.column() > 1:
#                correctIndex = self.model().index(index.row(), 1)
#            else:
#                correctIndex = index
#            QtGui.QItemSelectionModel.select(self, correctIndex, command)
#        else:
#            QtGui.QItemSelectionModel.select(self, indexOrSelection, command)
#        QtGui.QItemSelectionModel.select(self, index, command)


class CRBPopupView(QtGui.QTableView):
    def __init__(self, parent):
        QtGui.QTableView.__init__(self, parent)
        ## does not work        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        ## does not work        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        h = self.fontMetrics().height()
        self.verticalHeader().setDefaultSectionSize(3 * h / 2)
        self.verticalHeader().hide()
        self.horizontalHeader().hide()
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


class CRBComboBox(QtGui.QComboBox):
    u"""ComboBox, в котором отображается содержимое таблицы - справочника"""
    showCode = 0
    showName = 1
    showCodeAndName = 2
    showNameAndCode = 2

    def __init__(self, parent):
        QtGui.QComboBox.__init__(self, parent)
        self._searchString = ''
        self.showFields = CRBComboBox.showName
        #        self._searchColumn = 0
        self._model = CRBModel(self)
        self._selectionModel = CRBSelectionModel(self._model)
        self._tableName = ''
        self._addNone = True
        self._needCache = True
        self._filier = ''
        self._order = ''
        self._specialValues = None
        self.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.preferredWidth = None
        self.popupView = CRBPopupView(self)
        self.setModelColumn(self.showFields)
        self.setView(self.popupView)
        self.setModel(self._model)
        self._prefWidthCode = 0
        self._prefWidthName = 0
        self.popupView.setSelectionModel(self._selectionModel)
        #        self.popupView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        #        self.popupView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.popupView.setFrameShape(QtGui.QFrame.NoFrame)
        self.readOnly = False
        self.installEventFilter(self)
        self.headerIsVisible = True
        self.setHeaderVisible(self.headerIsVisible)
        # Добавил возможность сортировка по столбцам
        QObject.connect(self.popupView.horizontalHeader(), SIGNAL('sectionClicked(int)'), self.setSort)
        self.colSorting = {}

    def setSort(self, col):
        preOrder = self.colSorting.get(col, None)
        name = 'name' if col else 'code'
        self.colSorting[col] = 'DESC' if preOrder and preOrder == 'ASC' else 'ASC'
        self._order = ' '.join([name, self.colSorting[col]])
        header = self.popupView.horizontalHeader()
        header.setSortIndicatorShown(True)
        header.setSortIndicator(col, Qt.AscendingOrder if self.colSorting[col] == 'ASC' else Qt.DescendingOrder)
        self.updateModel()

    def setReadOnly(self, value=False):
        self.readOnly = value
        self._model.setReadOnly(self.readOnly)

    def isReadOnly(self):
        return self.readOnly

    def setHeaderVisible(self, flag):
        self.headerIsVisible = flag
        self.popupView.horizontalHeader().setVisible(flag)

    def setDblClickBehavior(self, flag):
        self.dblClickEnabled = flag

    def setPreferredWidth(self, preferredWidth):
        self.preferredWidth = preferredWidth

    def setTable(self, tableName, addNone=True, filter='', order=None, specialValues=None, needCache=True, force=False):
        self._tableName = tableName
        self._addNone = addNone
        self._filier = filter
        self._order = order
        self._needCache = needCache
        self._specialValues = specialValues
        self._model.setTable(tableName, addNone, filter, order, specialValues, needCache, force=force)
        db = QtGui.qApp.db
        where = (' WHERE ' + self._filier) if self._filier else ''
        query = db.query('SELECT MAX(CHAR_LENGTH(code)), MAX(CHAR_LENGTH(name)) FROM ' + self._tableName + where)
        while query.next():
            self._prefWidthCode = query.record().value(0).toInt()[0]
            self._prefWidthName = query.record().value(1).toInt()[0]
        db = QtGui.qApp.db
        where = (' WHERE ' + self._filier) if self._filier else ''
        query = db.query('SELECT MAX(CHAR_LENGTH(code)), MAX(CHAR_LENGTH(name)) FROM ' + self._tableName + where)
        while query.next():
            self._prefWidthCode = query.record().value(0).toInt()[0]
            self._prefWidthName = query.record().value(1).toInt()[0]

    def setSpecialValues(self, specialValues):
        if self._specialValues != specialValues:
            self._specialValues = specialValues
            self.reloadData()

    def addFilterAnd(self, filter):  # WTF?
        if self._filier:
            self._filier = ' AND '.join([self._filier, filter])
        else:
            self._filier = filter
        self.reloadData()

    def setFilter(self, filter='', order=None):
        self._filier = filter
        self._order = order
        self.setTable(self._tableName, self._addNone, filter, order, self._specialValues, self._needCache)

    def reloadData(self):
        self._model.setTable(self._tableName, self._addNone, self._filier,
                             self._order, self._specialValues, self._needCache,
                             True)

    updateModel = reloadData

    def setShowFields(self, showFields):
        self.showFields = showFields
        self.setModelColumn(self.showFields)

    ###!!!        self.setModelColumn(0)

    #    def setSearchColumn(self, column):
    #        self._searchColumn = column

    def setMaxVisibleItems(self, count):
        QtGui.QComboBox.setMaxVisibleItems(self, count)

    def setModel(self, model):
        QtGui.QComboBox.setModel(self, model)
        self.popupView.hideColumn(2)
        self._model = model

    def setView(self, view):
        QtGui.QComboBox.setView(self, view)
        # count = min(self.maxVisibleItems(), self._model.rowCount(None))

    def setValue(self, itemId):
        u"""id записи"""
        rowIndex = self._model.searchId(itemId)
        self.setCurrentIndex(rowIndex)

    ##        print 'setValue, id=', itemId, ' index=', rowIndex, ' after set=', self.currentIndex()

    def getValue(self):
        u"""id записи"""
        return self.value()

    def value(self):
        u"""id записи"""
        rowIndex = self.currentIndex()
        return self._model.getId(rowIndex)

    def setCode(self, code):
        u"""поле code записи"""
        rowIndex = self._model.searchCode(code)
        self.setCurrentIndex(rowIndex)

    def code(self):
        u"""поле code записи"""
        rowIndex = self.currentIndex()
        return self._model.getCode(rowIndex)

    def addItem(self, item):
        pass

    def showPopup(self):
        totalItems = 0
        if not self.isReadOnly():
            totalItems = self._model.rowCount(None)
        if totalItems > 0:
            self._searchString = ''
            view = self.popupView
            selectionModel = view.selectionModel()
            selectionModel.setCurrentIndex(self._model.index(self.currentIndex(), 1),
                                           QtGui.QItemSelectionModel.ClearAndSelect)
            maxVisibleItems = self.maxVisibleItems()
            visibleItems = min(maxVisibleItems, totalItems)
            if visibleItems > 0:
                view.setFixedHeight(view.rowHeight(0) * (visibleItems + (1 if self.headerIsVisible else 0)))
            frame = view.parent()
            sizeHint = view.sizeHint()
            preferredWidthCode = view.fontMetrics().width('o' * self._prefWidthCode)
            preferredWidthName = view.fontMetrics().width('o' * self._prefWidthName)
            view.horizontalHeader().setDefaultSectionSize(preferredWidthCode + 30)
            adjustPopupToWidget(self, frame, True,
                                max(preferredWidthCode + preferredWidthName, self.preferredWidth, sizeHint.width()),
                                view.height() + 2)
            frame.show()
            view.setFocus()
            scrollBar = view.horizontalScrollBar()
            scrollBar.setValue(0)

    def focusOutEvent(self, event):
        self._searchString = ''
        QtGui.QComboBox.focusOutEvent(self, event)

    def keyPressEvent(self, event):
        if self.isReadOnly():
            event.accept()
        else:
            key = event.key()
        if key == Qt.Key_Escape:
            event.ignore()
        elif key == Qt.Key_Return or key == Qt.Key_Enter:
            event.ignore()
        if key == Qt.Key_Delete:
            self._searchString = ''
            self.lookup()
            event.accept()
        elif key == Qt.Key_Backspace:  # BS
            self._searchString = self._searchString[:-1]
            self.lookup()
            event.accept()
        elif key == Qt.Key_Space:
            QtGui.QComboBox.keyPressEvent(self, event)
        elif not event.text().isEmpty():
            char = event.text().at(0)
            if char.isPrint():
                self._searchString = self._searchString + unicode(QString(char)).upper()
                self.lookup()
                event.accept()
            else:
                QtGui.QComboBox.keyPressEvent(self, event)
        else:
            QtGui.QComboBox.keyPressEvent(self, event)

    def lookup(self):
        i, self._searchString = self._model.searchCodeEx(self._searchString)
        if i >= 0 and i != self.currentIndex():
            self.setCurrentIndex(i)

    def eventFilter(self, obj, event):
        if self.isReadOnly():
            event.accept()
            return False
        return False
