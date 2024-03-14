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
from PyQt4.QtCore import Qt, SIGNAL, QAbstractTableModel, QString, QVariant, QObject

from library.Utils import forceBool, forceInt, forceString, forceStringEx, trim

from library.adjustPopup import adjustPopupToWidget
from library.crbcombobox import CRBModelDataCache


class CMultivalueComboBoxView(QtGui.QTableView):
    def __init__(self, parent=None):
        QtGui.QTableView.__init__(self, parent)
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.Fixed)
        h = self.fontMetrics().height()
        self.verticalHeader().setDefaultSectionSize(3*h/2)
        self.verticalHeader().hide()
        self.horizontalHeader().setStretchLastSection(True)
        self.resizeColumnsToContents()


class CMultivalueComboBoxModel(QAbstractTableModel):
    class CMultivalueItem():
        def __init__(self, value, code, name, isChecked=0):
            self._value = value
            self._isChecked = isChecked
            self._code = code
            self._name = name

        def eq(self, value):
            return self._value == value

        def value(self):
            return self._value

        def setValue(self, value):
            self._value = value

        def code(self):
            return self._code

        def setCode(self, code):
            self._code = code

        def name(self):
            return self._name

        def setName(self, name):
            self._name = name

        def isChecked(self):
            return self._isChecked

        def setIsChecked(self, isChecked):
            self._isChecked = isChecked


    class CMultivalueColumn():
        def __init__(self, model):
            self._model = model
        def model(self):
            return self._model
        def isCheckable(self):
            return False


    class CMultivalueDataColumn(CMultivalueColumn):
        def data(self, item):
            return item.value()

        def isChecked(self, item):
            return None

        def setData(self, item, value):
            item.setValue(value)

        def flags(self, index=None):
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    class CMultivalueDataColumnCode(CMultivalueColumn):
        def data(self, item):
            return item.code()

        def isChecked(self, item):
            return None

        def setData(self, item, value):
            item.setValue(value)

        def flags(self, index=None):
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    class CMultivalueDataColumnName(CMultivalueColumn):
        def data(self, item):
            return item.name()

        def isChecked(self, item):
            return None

        def setData(self, item, value):
            item.setValue(value)

        def flags(self, index=None):
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    class CMultivalueChekedColumn(CMultivalueColumn):
        def data(self, item):
            return None

        def isChecked(self, item):
            return item.isChecked()

        def setIsChecked(self, item, isChecked):
            item.setIsChecked(isChecked)

        def flags(self, index=None):
            if index.isValid():
                result = Qt.ItemIsEnabled | Qt.ItemIsSelectable
                if forceStringEx(self.model().getDataColumnValue(index.row())):
                    result |= Qt.ItemIsUserCheckable
                return result
            return Qt.NoItemFlags

        def isCheckable(self):
            return True


    def __init__(self, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._checkedColumnIsHidden = False
        self._dataColumn = CMultivalueComboBoxModel.CMultivalueDataColumn(self)
        self._dataColumnCode = CMultivalueComboBoxModel.CMultivalueDataColumnCode(self)
        self._dataColumnName = CMultivalueComboBoxModel.CMultivalueDataColumnName(self)
        self._checkedColumn = CMultivalueComboBoxModel.CMultivalueChekedColumn(self)
        self._columns = [self._checkedColumn, self._dataColumnCode, self._dataColumnName]
        self._items = []
        self._readOnly = False

    def headerData(self, section, orientation, role):
        if len(self._columns) == 3:
            if orientation == Qt.Horizontal:
                if role == Qt.DisplayRole:
                    if section == 0:
                        return QVariant(u'   ')
                    if section == 1:
                        return QVariant(u'Код')
                    elif section == 2:
                        return QVariant(u'Наименование')
            return QVariant()
        else:
            pass

    def setReadOnly(self, value=False):
        self._readOnly = value


    def isReadOnly(self):
        return self._readOnly


    def clear(self):
        self._items = []
        self.reset()


    def getCheckedRows(self):
        return [row for row, item in enumerate(self._items) if item.isChecked()]


    def checkedValueList(self):
        return [item.value() for item in self._items if item.isChecked()]


    def findRowIndex(self, value):
        for rowIndex, item in enumerate(self._items):
            if item.eq(value):
                return rowIndex
        return -1


    def getCheckedColumnIndex(self):
        return self._columns.index(self._checkedColumn)


    def isColumnIndexCheckable(self, index):
        return self._getCol(index.column()).isCheckable()


    def setCheckedColumnIsHiden(self, value):
        self._checkedColumnIsHidden = value


    def isCheckedColumnIsHiden(self):
        return self._checkedColumnIsHidden


    def addItem(self, value):
        self._items.append(CMultivalueComboBoxModel.CMultivalueItem(value, '', '', False))
        self._columns = [self._checkedColumn, self._dataColumn]
        self.reset()

    def addList(self, value):
        self._items.append(CMultivalueComboBoxModel.CMultivalueItem(value[0], value[1], value[2], value[3]))
        self._columns = [self._checkedColumn, self._dataColumnCode, self._dataColumnName]
        self.reset()


    def columnCount(self, index=None):
        return len(self._columns)-1 if self._checkedColumnIsHidden else len(self._columns)


    def itemCount(self):
        return self.rowCount()


    def rowCount(self, index=None):
        return len(self._items)


    def _getCol(self, column):
        return self._columns[1:][column] if self._checkedColumnIsHidden else self._columns[column]


    def getValue(self, row, column):
        return self._getCol(column).data(self._items[row])

    def getDataColumnValue(self, row):
        return self._dataColumn.data(self._items[row])

    def setValue(self, row, column, value):
        return self._getCol(column).setData(self._items[row], value)


    def isChecked(self, row, column):
        return self._getCol(column).isChecked(self._items[row])


    def isItemChecked(self, row):
        return self._checkedColumn.isChecked(self._items[row])


    def setCheckedRows(self, rows):
        for row, item in enumerate(self._items):
            self.setItemChecked(row, False)
        for row in rows:
            if row >= 0:
                self.setData(self.index(row, self.getCheckedColumnIndex()), QVariant(Qt.Checked), role=Qt.CheckStateRole)


    def clearItemChecked(self):
        rows = self.getCheckedRows()
        for row in rows:
            self.setItemChecked(row, False)


    def setItemChecked(self, row, value):
        self._checkedColumn.setIsChecked(self._items[row], value)


    def setIsChecked(self, row, column, value):
        self._checkedColumn.setIsChecked(self._items[row], value)


    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()

        if role == Qt.DisplayRole:
            column = index.column()
            row    = index.row()
            return QVariant(self.getValue(row, column))

        elif role == Qt.EditRole:
            column = index.column()
            row    = index.row()
            return QVariant(self.getValue(row, column))

        elif role == Qt.CheckStateRole and not self._checkedColumnIsHidden:
            row    = index.row()
            if forceStringEx(self.getDataColumnValue(row)):
                column = index.column()
                if column == self.getCheckedColumnIndex():
                    return QVariant(self.isChecked(row, column))

        return QVariant()


    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False

        if role == Qt.CheckStateRole:
            row = index.row()
            column = index.column()
            self.setIsChecked(row, column, forceInt(value))
            self.emitDataCheckedChanged(row, forceBool(value))
            self.emitDataChanged()
            return True

        return False


    def emitDataChanged(self):
        index1 = self.index(0, 0)
        index2 = self.index(self.rowCount(), self.columnCount())
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index1, index2)


    def emitDataCheckedChanged(self, row, added):
        data = QString(self.getDataColumnValue(row))
        self.emit(SIGNAL('dataCheckedChanged(QString, bool)'), data, added)


    def flags(self, index=None):
        if not index.isValid():
            return Qt.NoItemFlags
        if self._readOnly:
            return Qt.ItemIsEnabled
        return self._getCol(index.column()).flags(index)


# ##############################################################


class CMultivalueComboBoxPopup(QtGui.QFrame):
    def __init__(self, parent=None):
        QtGui.QFrame.__init__(self, parent, Qt.Popup)
        self._parent = parent
        self.vLayout = QtGui.QVBoxLayout(self)
        self._view   = CMultivalueComboBoxView(self)
        self._model  = CMultivalueComboBoxModel(self)
        self._view.setModel(self._model)
        self.vLayout.addWidget(self._view)
        self.vLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vLayout)

        self.connect(self._view, SIGNAL('clicked(QModelIndex)'), self.on_viewClicked)


    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Select):
            self.on_viewClicked(self._view.currentIndex())
            self.close()
        else:
            QtGui.QFrame.keyPressEvent(self, event)


    def model(self):
        return self._model


    def view(self):
        return self._view


    def on_viewClicked(self, index):
        if index.isValid():
            row = index.row()
            if self._model.isColumnIndexCheckable(index) and self.getValueByRow(row):
                pass
            else:
                if self.isCheckedColumnIsHiden():
                    self.setValue(self.getValueByRow(row))
                else:
                    if self.getValueByRow(row):
                        value = QVariant(Qt.Unchecked) if self._model.isItemChecked(index.row()) else QVariant(Qt.Checked)
                        self._model.setData(self._model.index(row, self._model.getCheckedColumnIndex()),
                                            value,
                                            role=Qt.CheckStateRole)
                    else:
                        rows          = self.getCheckedRows()
                        value         = QVariant(Qt.Unchecked)
                        checkedColumn = self._model.getCheckedColumnIndex()
                        for row in rows:
                            self._model.setData(self._model.index(row, checkedColumn), value, role=Qt.CheckStateRole)
                self.close()


    def getCheckedRows(self):
        return self._model.getCheckedRows()


    def setCheckedRows(self, rows):
        self._model.setCheckedRows(rows)


    def getValueByRow(self, row):
        return forceStringEx(self._model.getDataColumnValue(row))


    def setValue(self, value):
        self.emit(SIGNAL('valueSetted(QString)'), QString(value))


    def setCheckedColumnIsHiden(self, value):
        self._model.setCheckedColumnIsHiden(value)


    def isCheckedColumnIsHiden(self):
        return self._model.isCheckedColumnIsHiden()


    def addItem(self, item):
        self._model.addItem(item)

    def addList(self, item):
        self._model.addList(item)

# ################################################################


class CBaseMultivalue():
    def __init__(self, multivalue=True):
        self._popupView = CMultivalueComboBoxPopup(self)
        self._model = self._popupView.model()
        self.setModel(self._model)
        self.preferredWidth = 100
        self.setMultivalueChecking(multivalue)
        self.connect(self._model, SIGNAL('dataCheckedChanged(QString, bool)'), self.on_dataCheckedChanged)
        self.connect(self._popupView, SIGNAL('valueSetted(QString)'), self.on_valueSetted)
        self.readOnly = False


    def setReadOnly(self, value=False):
        self.readOnly = value
        self._model.setReadOnly(self.readOnly)


    def isReadOnly(self):
        return self.readOnly


    def isCheckedColumnIsHiden(self):
        return self._popupView.isCheckedColumnIsHiden()


    def setValue(self, value):
        value = forceString(value)
        if self.isCheckedColumnIsHiden():
            if self.isEditable():
                rowIndex = self._model.findRowIndex(value)
                self.setCurrentIndex(rowIndex)
                self.setEditText(value)
            else:
                rowIndex = self._model.findRowIndex(value)
                self.setCurrentIndex(rowIndex)
        else:
            valueList = [trim(val) for val in value.split(u'‚')]   # изменяю разделитель строки с простой запятой на "нижняя одиночная кавычка" http://htmlbook.ru/samhtml/tekst/spetssimvoly
            for value in valueList:
                rowIndex = self._model.findRowIndex(value)
                if rowIndex >= 0:
                    modelIndex = self._model.index(rowIndex, self._model.getCheckedColumnIndex())
                    value      = QVariant(Qt.Checked)
                    self._model.setData(modelIndex, value, role=Qt.CheckStateRole)



    def setEditable(self, value, readOnly=False):
        QtGui.QComboBox.setEditable(self, value)
        if self.isEditable():
            self.lineEdit().setReadOnly(readOnly)


    # Волшебство?
    # По какой-то причине, в во время QComboBox.focusOutEvent и если значени идентично элементу из списка combobox-а,
    # срабатывает сигнал editTextChanged при этом как аргумент передается пустая строка.
    # Откуда такое происходит пока не ясно, ввиду этого поставлена данная заплатка.
    def focusOutEvent(self, event):
        currentText = trim(self.text())
        QtGui.QComboBox.focusOutEvent(self, event)
        if not trim(self.text()) and currentText:
            self.setValue(currentText)


    def on_valueSetted(self, value):
        self.setValue(trim(value))


    def on_dataCheckedChanged(self, data, added):
        if self._model.checkedValueList():
            if "|" in self._model.checkedValueList()[0]:
                newTextValue = u'‚ '.join("|".join([checkedVal.split('|')[1], checkedVal.split('|')[2]]) for checkedVal in self._model.checkedValueList() if checkedVal) # изменяю разделитель строки с простой запятой на "нижняя одиночная кавычка" http://htmlbook.ru/samhtml/tekst/spetssimvoly
                newToolTip   = u'\n'.join("|".join([checkedVal.split('|')[1], checkedVal.split('|')[2]]) for checkedVal in self._model.checkedValueList() if checkedVal)
                self.setEditText(newTextValue)
                self.setToolTip(newToolTip)
            else:
                newTextValue = u'‚ '.join(checkedVal for checkedVal in self._model.checkedValueList() if checkedVal)
                self.setEditText(newTextValue)
        else:
            newTextValue = u''
            self.setEditText(newTextValue)

#        data = trim(data)
#        if data:
#            currentTextValue = forceStringEx(self.currentText())
#            if added:
#                if data not in self.checkedValueList():
#                    newTextValue = u', '.join([data, currentTextValue]) if currentTextValue else data
#                else:
#                    newTextValue = currentTextValue
#            else:
#                newTextValue = u', '.join([trim(value) for value in currentTextValue.split(',') if trim(value) != data])
#            self.setEditText(newTextValue)


    def checkedValueList(self):
        return self._model.checkedValueList()


    def showPopup(self):
        if not self.isReadOnly():
            if self.itemCount():
                view = self._popupView.view()
                view.clearSelection()
                selectionModel = view.selectionModel()
                command = QtGui.QItemSelectionModel.Select|QtGui.QItemSelectionModel.Current
                if self.isCheckedColumnIsHiden():
                    row = max(0, self.currentIndex())
                    selectionModel.setCurrentIndex(self._model.index(row, 0), command)
                else:
                    for row in self._model.getCheckedRows():
                        selectionModel.setCurrentIndex(self._model.index(row, 0), command)
                    if not selectionModel.hasSelection():
                        selectionModel.setCurrentIndex(self._model.index(0, 0), command)
                adjustPopupToWidget(self, self._popupView, True, max(self.preferredWidth, view.width()+2), view.height()+2)
                self._popupView.show()
                view.setFocus()
                view.horizontalScrollBar().setValue(0)


    def itemCount(self):
        return self._model.itemCount()


    def addItems(self, items):
        for item in items:
            self.addItem(item)


    def addItem(self, item):
        self._popupView.view().horizontalHeader().hide()
        self._popupView.addItem(item)
        self.on_dataCheckedChanged(1, 1)


    def addList(self, item):
        for i in item:
            self._popupView.addList(i)
        self.on_dataCheckedChanged(1, 1)


    def setMultivalueChecking(self, value):
        self.setCheckedColumnIsHiden(not value)
        self.setEditable(value, value)


    def setCheckedColumnIsHiden(self, value):
        self._popupView.setCheckedColumnIsHiden(value)


    def clear(self):
        self._model.clear()
        QtGui.QComboBox.clear(self)


    def clearItemChecked(self):
        self._model.clearItemChecked()


class CMultivalueComboBox(CBaseMultivalue, QtGui.QComboBox):
    def __init__(self, parent=None):
        QtGui.QComboBox.__init__(self, parent)
        CBaseMultivalue.__init__(self)


    def text(self):
        return unicode(self.currentText())
    
    def getCheckedRows(self):
        return self._popupView.getCheckedRows()
    
    def setCheckedRows(self, rows):
        self._popupView.setCheckedRows(rows)

    value = text


class CRBMultivalueComboBox(CMultivalueComboBox):
    def __init__(self, parent=None):
        CMultivalueComboBox.__init__(self, parent)
        self._tableName = ''
        self._addNone   = True
        self._needCache = True
        self._filter    = ''
        self._order     = ''
        self._specialValues = None
        self._data = None
        self._mapShown2Id = {}
        self._mapId2Shown = {}

        # Добавил возможность сортировка по столбцам
        QObject.connect(self._popupView._view.horizontalHeader(), SIGNAL('sectionClicked(int)'), self.setSort)
        self.colSorting = {}

    def setSort(self, col):
        preOrder = self.colSorting.get(col, None)
        name = 'code'
        if col == 1:
            name = 'code'
        elif col == 2:
            name = 'name'
        self.colSorting[col] = 'DESC' if preOrder and preOrder == 'ASC' else 'ASC'
        self._order = ' '.join([name, self.colSorting[col]])
        header = self._popupView._view.horizontalHeader()
        header.setSortIndicatorShown(True)
        header.setSortIndicator(col, Qt.AscendingOrder if self.colSorting[col] == 'ASC' else Qt.DescendingOrder)
        self._initRB()


    def clearValue(self):
        self.clearItemChecked()
        self.setEditText(u'')


    def _translateShownValue2Value(self, value):
        value = u'‚ '.join(checkedVal for checkedVal in self._model.checkedValueList() if checkedVal)
        if value:
            shownItems = [trim(item) for item in value.split(u'‚')] # изменяю разделитель строки с простой запятой на "нижняя одиночная кавычка" http://htmlbook.ru/samhtml/tekst/spetssimvoly
            if shownItems:
                value = [self._mapShown2Id[shownItem] for shownItem in shownItems]
                if value:
                    return u', '.join(value)
        return ''


    def _translateValue2ShownValue(self, value):
        if value:
            if not isinstance(value, list):
                idList = [trim(id.replace(' ', '')) for id in value.split(',')]
            else:
                idList = value
            if idList:
                value = [self._mapId2Shown[id] for id in idList]
                if value:
                    return u', '.join(value)
        return u''


    def _initRB(self):
        self._data = CRBModelDataCache.getData(self._tableName,
                                               self._addNone,
                                               self._filter,
                                               self._order,
                                               self._specialValues,
                                               self._needCache)

        shownItems = []
        for itemIndex in xrange(self._data.getCount()):
            id = self._data.getId(itemIndex)
            shown = u' | '.join([unicode(self._data.getId(itemIndex)), unicode(self._data.getCode(itemIndex)), unicode(self._data.getName(itemIndex))])

            items = []

            code = unicode(self._data.getCode(itemIndex))
            name = unicode(self._data.getName(itemIndex))
            chBox = 2 if shown in self.checkedValueList() else 0

            items.append(shown)
            items.append(code)
            items.append(name)
            items.append(chBox)

            self._mapId2Shown[str(id)] = shown
            self._mapShown2Id[shown] = unicode(id)

            shownItems.append(items)

        self.clear()
        self.addList(shownItems)

    def _setHorisontalTable(self):
        db = QtGui.qApp.db
        where = (' WHERE ' + self._filter) if self._filter else ''

        query = db.query("""
        SELECT 
        (SELECT LENGTH(code) FROM {0} {1} GROUP BY code ORDER BY LENGTH(code) DESC LIMIT 1) AS code,
        (SELECT LENGTH(name) FROM {2} {3} GROUP BY name ORDER BY LENGTH(name) DESC LIMIT 1) AS name;
        """.format(self._tableName, where, self._tableName, where))

        while query.next():
            prefWidthCode = query.record().value(0).toInt()[0]
            prefWidthName = query.record().value(1).toInt()[0]

        self._popupView.view().setColumnWidth(0, 30) # Изменяем ширину первого столбца
        self._popupView.view().setColumnWidth(1, 80 + (prefWidthCode * 2)) # Изменим ширину столбца code
        self._popupView.view().setColumnWidth(2, prefWidthName * 2) # Изменим ширину столбца name

        self._popupView.view().setMinimumWidth(int((20 + prefWidthName) * 2)*2)

        self.preferredWidth = (prefWidthCode + prefWidthName) * 2 # Изменяем ширину второго столбца


    def setTable(self, tableName, addNone=False, filter='', order=None, specialValues=None, needCache=True):
        self._tableName = tableName
        self._addNone   = addNone
        self._filter    = filter
        self._order     = order
        self._needCache = needCache
        self._specialValues = specialValues
        self._setHorisontalTable()
        self._initRB()


    def setText(self, value):
        self.setValue(value)


    def setValue(self, value):
        CMultivalueComboBox.setValue(self, self._translateValue2ShownValue(value))


    def text(self):
        return self.value()


    def value(self):
        return self._translateShownValue2Value(CMultivalueComboBox.value(self))



if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    cmb = CMultivalueComboBox()
#    cmb.setMultivalueChecking(False)
    cmb.addItems(
        [
            u'12sdklmsdl;dlsdkl;vdl;vsdlvsdmlvsdlfddfdfdf3',
            u'23412sdklmsdl;dlsdkl;vdl;vsdlvsdmlvdfsdfsdsdl',
            '',
            '345'
        ])
    cmb.show()
    app.exec_()


