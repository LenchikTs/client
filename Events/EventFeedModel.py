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
from PyQt4.QtCore import Qt, SIGNAL, QAbstractTableModel, QDate, QDateTime, QModelIndex, QVariant

from library.crbcombobox import CRBModel, CRBComboBox
from library.DateEdit import CDateEdit
from library.InDocTable import CInDocTableView
from library.Utils import forceBool, forceDate, forceInt, forceRef, forceString, formatShortName, pyDate, toVariant

from Registry.Utils import CClientRelationComboBoxPatron
from Users.Rights import urAdmin, urHBEditCurrentDateFeed


class CFeedModel(QAbstractTableModel):
    def __init__(self, parent, typeFeed):
        QAbstractTableModel.__init__(self, parent)
        self.headers = []
        self.items = {}
        self.dates = []
        self.typeFeed = typeFeed
        self.modelRBDiet = CRBModel(self)
        self.modelRBDiet.setTable('rbDiet')
        self.modelRBFinance = CRBModel(self)
        self.modelRBFinance.setTable('rbFinance')
        self.relationItems = {None: u'не задано'}
        self.financeId = None
        self.patronId = None
        self.readOnly = False


    def setReadOnly(self, value):
        self.readOnly = value


    def columnCount(self, index = None):
        return len(self.headers)


    def rowCount(self, index = None):
        return len(self.dates)


    def flags(self, index = QModelIndex()):
        begDate = QDateTime.currentDateTime().addSecs(-32400) # сдвиг на 9 часов назад
        row = index.row()
        if self.readOnly:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled
        if row < len(self.dates)-1:
            date = self.dates[row]
            if date:
                if QDateTime(date) <= begDate and not self.getHBEditFeedRight():
                    return Qt.ItemIsSelectable | Qt.ItemIsEnabled
        if index.column() == len(self.headers)-1:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsUserCheckable
        return Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsEditable


    def getHBEditFeedRight(self):
        app = QtGui.qApp
        loggedIn = bool(app.db) and (app.demoMode or app.userId is not None)
        return app.userHasRight(urHBEditCurrentDateFeed) or (loggedIn and app.userHasRight(urAdmin))


    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                header = self.headers[section]
                if header:
                    return QVariant(header[1])
        return QVariant()


    def data(self, index, role=Qt.DisplayRole):
        refusedCol = len(self.headers)-1
        featuresClientCol = len(self.headers)-2
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole and column != refusedCol:
            if row < len(self.dates)-1:
                date = self.dates[row]
                if column == 0:
                    if date:
                        return QVariant(QDate(date))
                elif column == featuresClientCol:
                    if len(self.headers[column]) == 2:
                        for header in self.headers:
                            if ((date, header[0]) in self.items.keys()):
                                item = self.items.get((date, header[0]), None)
                                if len(item) > 1:
                                    featuresToEat = forceString(item[1].value('featuresToEat'))
                                    if featuresToEat:
                                        return toVariant(featuresToEat)
                elif column == 1 or (column == 2 and self.typeFeed):
                    if len(self.headers[column]) == 2:
                        for header in self.headers:
                            if ((date, header[0]) in self.items.keys()):
                                item = self.items.get((date, header[0]),None)
                                if item and item[1] and item[0]:
                                    if column == 1:
                                        val = forceRef(item[1].value('finance_id'))
                                        index = self.modelRBFinance.searchId(val)
                                        if index >= 0:
                                            name = self.modelRBFinance.getName(index)
                                        else:
                                            name = '{%d}'%val
                                        return toVariant(name)
                                    elif column == 2 and self.typeFeed:
                                        val = forceRef(item[1].value('patron_id'))
                                        return toVariant(self.relationItems.get(val, u''))
                else:
                    if self.headers[column] and self.headers[column][0] and ((date, self.headers[column][0]) in self.items.keys()):
                        item = self.items.get((date, self.headers[column][0]),None)
                        if item and item[0]:
                            val = item[0]
                            index = self.modelRBDiet.searchId(val)
                            if index >= 0:
                                name = self.modelRBDiet.getName(index)
                            else:
                                name = '{%d}'%val
                            return toVariant(name)
        elif role == Qt.EditRole and column != refusedCol:
            if row < len(self.dates)-1:
                date = self.dates[row]
                if column == 0:
                    if date:
                        return QVariant(QDate(date))
                elif column == featuresClientCol:
                    if len(self.headers[column]) == 2:
                        for header in self.headers:
                            if ((date, header[0]) in self.items.keys()):
                                item = self.items.get((date, header[0]), None)
                                if len(item) > 1:
                                    return toVariant(forceString(item[1].value('featuresToEat')))
                elif column == 1 or (column == 2 and self.typeFeed):
                    if len(self.headers[column]) == 2:
                        for header in self.headers:
                            if ((date, header[0]) in self.items.keys()):
                                item = self.items.get((date, header[0]), None)
                                if column == 1 and item[1]:
                                    financeId = forceRef(item[1].value('finance_id'))
                                    return toVariant(financeId)
                                elif column == 2 and item[1] and self.typeFeed:
                                    patronId = forceRef(item[1].value('patron_id'))
                                    return toVariant(patronId)
                else:
                    if self.headers[column] and self.headers[column][0] and ((date, self.headers[column][0]) in self.items.keys()):
                        item = self.items.get((date, self.headers[column][0]),None)
                        if item and item[0]:
                            return toVariant(item[0])
        elif role == Qt.CheckStateRole and column == refusedCol:
            if row < len(self.dates)-1:
                date = self.dates[row]
                if len(self.headers[column]) == 2:
                    refusalToEatMin = 0
                    for header in self.headers:
                        if ((date, header[0]) in self.items.keys()):
                            item = self.items.get((date, header[0]), None)
                            if len(item) > 1:
                                refusalToEat = forceInt(item[1].value('refusalToEat'))
                                if refusalToEatMin < refusalToEat:
                                    refusalToEatMin = refusalToEat
                    return toVariant(Qt.Checked if refusalToEatMin else Qt.Unchecked)
        return QVariant()


    def loadHeader(self):
        self.headers = [[None, u'Дата'],
                        [None, u'Источник финансирования']]
        if  self.typeFeed:
            self.headers.append([None, u'Лицо по уходу'])
        db = QtGui.qApp.db
        table = db.table('rbMealTime')
        records = db.getRecordList(table, '*', where='', order='code')
        for record in records:
            header = [forceRef(record.value('id')),
                      forceString(record.value('name'))
                      ]
            self.headers.append(header)
        self.headers.append([None, u'Особенности'])
        self.headers.append([None, u'Отказ'])
        self.reset()


    def setFinanceId(self, financeId):
        self.financeId = financeId


    def setPatronId(self, patronId):
        self.patronId = patronId


    def loadClientRelation(self, clientId):
        self.relationItems = {None: u'не задано'}
        db = QtGui.qApp.db
        tableCR = db.table('ClientRelation')
        self.addPatronItem(db, tableCR, 'relative_id', 'relativeId', [tableCR['client_id'].eq(clientId)])
        self.addPatronItem(db, tableCR, 'client_id', 'clientId', [tableCR['relative_id'].eq(clientId)])


    def addPatronItem(self, db, tableCR, colRelative, colFields, cond):
        tableRT = db.table('rbRelationType')
        tableC  = db.table('Client')
        queryTable = tableCR
        queryTable = queryTable.leftJoin(tableRT, tableRT['id'].eq(tableCR['relativeType_id']))
        queryTable = queryTable.leftJoin(tableC, tableC['id'].eq(tableCR[colRelative]))

        fields = ['CONCAT_WS(\' | \', rbRelationType.code, CONCAT_WS(\'->\', rbRelationType.leftName, rbRelationType.rightName)) AS relationType',
                  tableC['lastName'].alias(), tableC['firstName'].name(),
                  tableC['patrName'].name(), tableC['birthDate'].name(),
                  tableC['id'].alias(colFields)]
        clientRelationRecordList = db.getRecordList(queryTable, fields, cond)

        for relationRecord in clientRelationRecordList:
            name = formatShortName(relationRecord.value('lastName'),
                                   relationRecord.value('firstName'),
                                   relationRecord.value('patrName'))
            itemText = u', '.join([name,
                                  forceString(relationRecord.value('birthDate')),
                                  forceString(relationRecord.value('relationType'))])
            relativeId = forceRef(relationRecord.value(colFields))
            if relativeId not in self.relationItems.keys():
                self.relationItems[relativeId] = itemText


    def loadData(self, eventId, typeFeed):
        self.items = {}
        self.dates = []
        if eventId:
            itemsHeader = {}
            db = QtGui.qApp.db
            tableEventFeed = db.table('Event_Feed')
            cond = [tableEventFeed['event_id'].eq(eventId),
                    tableEventFeed['deleted'].eq(0),
                    tableEventFeed['typeFeed'].eq(typeFeed)
                    ]
            records = db.getRecordList(tableEventFeed, '*', cond, 'Event_Feed.date ASC, Event_Feed.featuresToEat DESC')
            for record in records:
                date = pyDate(forceDate(record.value('date')))
                itemsHeader[(date, forceRef(record.value('mealTime_id')))] = (forceInt(record.value('diet_id')), record)
                if date and (date not in self.dates):
                    if len(self.dates) > 0:
                        nextDate = pyDate(QDate(self.dates[len(self.dates) - 1]).addDays(1))
                        while date > nextDate:
                            self.dates.append(nextDate)
                            nextDate = pyDate(QDate(self.dates[len(self.dates) - 1]).addDays(1))
                    self.dates.append(date)
            self.dates.sort()
            for colDate in self.dates:
                for mealTimeId, mealTimeName in self.headers:
                    if mealTimeId:
                        item = itemsHeader.get((colDate, mealTimeId), None)
                        if item:
                            self.items[(colDate, mealTimeId)] = item
                        else:
                            record = self.getEmptyRecord()
                            record.setValue('date', toVariant(colDate))
                            record.setValue('mealTime_id', toVariant(mealTimeId))
                            self.items[(colDate, mealTimeId)] = (0, record)
        self.dates.append(None)
        self.reset()


    def setData(self, index, value, role=Qt.EditRole):
        refusedCol = len(self.headers)-1
        featuresClientCol = len(self.headers)-2
        column = index.column()
        row = index.row()
        if role == Qt.CheckStateRole and column == refusedCol:
            if row < len(self.dates) - 1:
                date = self.dates[row]
                if date:
                    for header in self.headers:
                        itemValue = self.items.get((date, header[0]), None)
                        if itemValue and len(itemValue) == 2:
                            dietId, record = itemValue
                            record.setValue('refusalToEat', toVariant(forceInt(value) == Qt.Checked))
                            self.items[(date, header[0])] = (dietId, record)
            self.emitCellChanged(row, column)
            return True
        elif role == Qt.EditRole and column != refusedCol:
            if row == len(self.dates) - 1:
                if value.isNull():
                    return False
                for headerId, headerName in self.headers:
                    self.items[pyDate(QDate()), headerId] = (0, self.getEmptyRecord())
                self.dates.append(pyDate(QDate()))
                vCnt = len(self.dates)
                vIndex = QModelIndex()
                self.beginInsertRows(vIndex, vCnt, vCnt)
                self.insertRows(vCnt, 1, vIndex)
                self.endInsertRows()
            date = self.dates[row]
            if column == 0:
                newDate = pyDate(forceDate(value))
                if newDate and (newDate not in self.dates):
                    self.dates[row] = newDate
                    if len(self.items) > 0:
                        for headerId, headerName in self.headers:
                            if headerId:
                                for key, item in self.items.items():
                                    if key == (date, headerId):
                                        itemValue = item
                                        if itemValue and len(itemValue) == 2:
                                            dietId, record = itemValue
                                            record.setValue('date', value)
                                        if (date, headerId) in self.items.keys():
                                            del self.items[(date, headerId)]
                                        self.items[(newDate, headerId)] = (dietId, record)
            elif column == featuresClientCol:
                if date:
                    for header in self.headers:
                        itemValue = self.items.get((date, header[0]), None)
                        if itemValue and len(itemValue) == 2:
                            dietId, record = itemValue
                            record.setValue('featuresToEat', toVariant(forceString(value)))
                            self.items[(date, header[0])] = (dietId, record)
            elif column == 1 or (column == 2 and self.typeFeed):
                if date:
                    for header in self.headers:
                        itemValue = self.items.get((date, header[0]), None)
                        if itemValue and len(itemValue) == 2:
                            dietId, record = itemValue
                            if column == 1:
                                record.setValue('finance_id', toVariant(value))
                            elif column == 2 and self.typeFeed:
                                record.setValue('patron_id', toVariant(value))
                            self.items[(date, header[0])] = (dietId, record)
            else:
                header = self.headers[column]
                if date and header and header[0]:
                    itemValue = self.items.get((date, header[0]), None)
                    if itemValue and len(itemValue) == 2:
                        dietId, record = itemValue
                        record.setValue('date', toVariant(date))
                        record.setValue('diet_id', value)
                        record.setValue('mealTime_id', toVariant(header[0]))
                        if not forceRef(record.value('finance_id')):
                            record.setValue('finance_id', toVariant(self.financeId))
                            prevDate = pyDate(QDate(date).addDays(-1))
                            for prevHeader in self.headers:
                                if prevHeader[0]:
                                    prevItem = self.items.get((prevDate, prevHeader[0]), None)
                                    if prevItem and len(prevItem) == 2:
                                        prevDietId, prevRecord = prevItem
                                        if prevRecord:
                                            prevFinanceId = forceRef(prevRecord.value('finance_id'))
                                            record.setValue('finance_id', toVariant(prevFinanceId))
                        if not forceRef(record.value('patron_id')):
                            record.setValue('patron_id', toVariant(self.patronId))
                        self.items[(date, header[0])] = (forceInt(value), record)
            self.emitCellChanged(row, column)
            return True
        return False


    def saveData(self, masterId, typeFeed, idList):
        if self.items is not None:
            db = QtGui.qApp.db
            table = db.table('Event_Feed')
            masterId = toVariant(masterId)
            for dietId, record in self.items.values():
                if forceDate(record.value('date')) and forceRef(record.value('diet_id')):
                    record.setValue('event_id', masterId)
                    record.setValue('typeFeed', toVariant(typeFeed))
                    id = db.insertOrUpdate(table, record)
                    record.setValue('id', toVariant(id))
                    idList.append(id)
        return idList


    def getEmptyRecord(self):
        db = QtGui.qApp.db
        tableEventFeed = db.table('Event_Feed')
        record = tableEventFeed.newRecord()
        return record


    def upRow(self, row):
        if 0 < row < len(self.dates):
            self.dates[row-1], self.dates[row] = self.dates[row], self.dates[row-1]
            self.emitRowsChanged(row-1, row)
            return True
        else:
            return False


    def downRow(self, row):
        if 0 <= row < len(self.dates)-1:
            self.dates[row+1], self.dates[row] = self.dates[row], self.dates[row+1]
            self.emitRowsChanged(row, row+1)
            return True
        else:
            return False


    def removeRows(self, row, count, parentIndex = QModelIndex()):
        if 0<=row and row+count<=len(self.dates):
            self.beginRemoveRows(parentIndex, row, row+count-1)
            del self.dates[row:row+count]
            self.endRemoveRows()
            return True
        else:
            return False


    def removeRow(self, row, parent = QModelIndex()):
        if self.dates and 0<= row < len(self.dates):
            date = self.dates[row]
            if date:
                QtGui.qApp.setWaitCursor()
                try:
                    self.beginRemoveRows(parent, row, row)
                    for header in self.headers:
                        if header[0] and self.dates[row]:
                            if (self.dates[row], header[0]) in self.items.keys():
                                del self.items[(self.dates[row], header[0])]
                    del self.dates[row]
                    self.endRemoveRows()
                    self.emitItemsCountChanged()
                    return True
                finally:
                    QtGui.qApp.restoreOverrideCursor()
        return False


    def emitItemsCountChanged(self):
        self.emit(SIGNAL('itemsCountChanged(int)'), len(self.dates) if self.dates else 0)


    def emitCellChanged(self, row, column):
        index = self.index(row, column)
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)


    def emitRowsChanged(self, row1, row2):
        index1 = self.index(row1, 0)
        index2 = self.index(row2, self.columnCount())
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index1, index2)


    def emitColumnChanged(self, column):
        index1 = self.index(0, column)
        index2 = self.index(self.rowCount(), column)
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index1, index2)


class CPatronItemDelegate(QtGui.QItemDelegate):
    def __init__(self, parent = None):
        QtGui.QItemDelegate.__init__(self, parent)

    def setClientId(self, clientId):
        self.clientId = clientId


    def createEditor(self, parent, option, index):
        editor = CClientRelationComboBoxPatron(parent)
        editor.setClientId(self.clientId)
        return editor


    def setEditorData(self, editor, index):
        model  = index.model()
        data = model.data(index, Qt.EditRole)
        editor.setValue(forceRef(data))


    def setModelData(self, editor, model, index):
        model.setData(index, toVariant(editor.value()))


class CDietItemDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)
        self.filter = u''


    def setFilter(self, date, clientId):
        if date:
            db = QtGui.qApp.db
            self.filter = u'''(rbDiet.begDate IS NULL OR rbDiet.begDate <= %s) AND (rbDiet.endDate IS NULL OR rbDiet.endDate >= %s)'''%(db.formatDate(date), db.formatDate(date))
            if clientId:
                self.filter += u''' AND (SELECT isSexAndAgeSuitable(0, (SELECT MAX(Client.birthDate) FROM Client WHERE Client.id = %s AND Client.deleted = 0), 0, rbDiet.age, %s))'''%(clientId, db.formatDate(date))
        else:
            self.filter = u''


    def createEditor(self, parent, option, index):
        editor = CRBComboBox(parent)
        editor.setTable('rbDiet', filter = self.filter)
        return editor


    def setEditorData(self, editor, index):
        model  = index.model()
        data = model.data(index, Qt.EditRole)
        editor.setShowFields(editor.showFields)
        editor.setValue(forceRef(data))


    def setModelData(self, editor, model, index):
        model.setData(index, toVariant(editor.value()))


class CFinanceItemDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)


    def createEditor(self, parent, option, index):
        editor = CRBComboBox(parent)
        editor.setTable('rbFinance')
        return editor


    def setEditorData(self, editor, index):
        model  = index.model()
        data = model.data(index, Qt.EditRole)
        editor.setShowFields(editor.showFields)
        editor.setValue(forceRef(data))


    def setModelData(self, editor, model, index):
        model.setData(index, toVariant(editor.value()))


class CRefusalToEatDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)


    def createEditor(self, parent, option, index):
        editor = QtGui.QCheckBox(parent)
        return editor


    def setEditorData(self, editor, index):
        model  = index.model()
        data = model.data(index, Qt.EditRole)
        editor.setChecked(forceBool(data))


    def setModelData(self, editor, model, index):
        model.setData(index, toVariant(editor.isChecked()))


class CDateEditItemDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)

    def getHBEditFeedRight(self):
        app = QtGui.qApp
        loggedIn = bool(app.db) and (app.demoMode or app.userId is not None)
        return app.userHasRight(urHBEditCurrentDateFeed) or (loggedIn and app.userHasRight(urAdmin))

    def createEditor(self, parent, option, index):
        editor = CDateEdit(parent)
        begDate = QDate.currentDate().addDays(1)
        editor.setDate(begDate)
        if not self.getHBEditFeedRight():
            editor.setMinimumDate(begDate)
        return editor


    def setEditorData(self, editor, index):
        model  = index.model()
        data = model.data(index, Qt.EditRole)
        editor.setDate(forceDate(data))


    def setModelData(self, editor, model, index):
        model.setData(index, toVariant(editor.date()))


class CFeaturesToEatDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)


    def createEditor(self, parent, option, index):
        editor = QtGui.QLineEdit(parent)
        return editor


    def setEditorData(self, editor, index):
        model  = index.model()
        data = model.data(index, Qt.EditRole)
        editor.setText(forceString(data))


    def setModelData(self, editor, model, index):
        model.setData(index, QVariant(editor.text()))


class CFeedInDocTableView(CInDocTableView):
    def __init__(self, parent):
        CInDocTableView.__init__(self, parent)
        self.dietItemDelegate = CDietItemDelegate(self)
        self.dateEditItemDelegate = CDateEditItemDelegate(self)
        self.featuresToEatDelegate = CFeaturesToEatDelegate(self)
        self.refusalToEatDelegate = CRefusalToEatDelegate(self)
        self.patronItemDelegate = CPatronItemDelegate(self)
        self.financeItemDelegate = CFinanceItemDelegate(self)


    def on_popupMenu_aboutToShow(self):
        row = self.currentIndex().row()
        rowCount = self.model().rowCount()
        if self._CInDocTableView__actUpRow:
            self._CInDocTableView__actUpRow.setEnabled(0<row<rowCount)
        if self._CInDocTableView__actDownRow:
            self._CInDocTableView__actDownRow.setEnabled(0<=row<rowCount-1)
        if self._CInDocTableView__actDeleteRows:
            rows = self.getSelectedRows()
            canDeleteRow = bool(rows)
            if canDeleteRow and self._CInDocTableView__delRowsChecker:
                canDeleteRow = self._CInDocTableView__delRowsChecker(rows)
            if len(rows) == 1 and rows[0] == row:
                self._CInDocTableView__actDeleteRows.setText(u'Удалить текущую строку')
            elif len(rows) == 1:
                self._CInDocTableView__actDeleteRows.setText(u'Удалить выделенную строку')
            else:
                self._CInDocTableView__actDeleteRows.setText(u'Удалить выделенные строки')
            self._CInDocTableView__actDeleteRows.setEnabled(canDeleteRow)
            if self._CInDocTableView__actDuplicateSelectRows:
                self._CInDocTableView__actDuplicateSelectRows.setEnabled(canDeleteRow)
        if self._CInDocTableView__actSelectAllRow:
            self._CInDocTableView__actSelectAllRow.setEnabled(0<=row<rowCount)
        if self._CInDocTableView__actSelectRowsByData:
            column = self.currentIndex().column()
            dates = self.model().dates
            header = self.model().headers[column]
            value = None
            if column == 0:
                value = dates[row] if row < len(self.model().dates) else None
            else:
                date = dates[row]
                if date and header and header[0]:
                    itemValue = self.model().items.get((date, header[0]), None)
                    if (itemValue and len(itemValue) == 2):
                        value = itemValue[0]
                    else:
                        value = None
            self._CInDocTableView__actSelectRowsByData.setEnabled(forceBool(0<=row<rowCount and (value)))
        if self._CInDocTableView__actClearSelectionRow:
            rows = self.getSelectedRows()
            self._CInDocTableView__actClearSelectionRow.setEnabled(bool(rows))


    def getSelectedRows(self):
        rowCount = self.model().rowCount()
        rowSet = set([index.row() for index in self.selectedIndexes() if index.row()<rowCount])
        result = list(rowSet)
        result.sort()
        return result


    def on_deleteRows(self):
        rows = self.getSelectedRows()
        rows.sort(reverse=True)
        for row in rows:
            self.model().removeRow(row)


    def on_selectRowsByData(self):
        items = self.model().items
        dates = self.model().dates
        currentRow = self.currentIndex().row()
        if currentRow < len(dates):
            currentColumn = self.currentIndex().column()
            selectIndexes = self.selectedIndexes()
            selectRowList = []
            for selectIndex in selectIndexes:
                selectRow = selectIndex.row()
                if selectRow not in selectRowList:
                    selectRowList.append(selectRow)
            date = dates[currentRow]
            header = self.model().headers[currentColumn]
            if currentColumn == 0:
                if date:
                    for row, item in enumerate(dates):
                        if (item == date) and (row not in selectRowList):
                            self.selectRow(row)
            else:
                if date and header and header[0]:
                    itemValue = items.get((date, header[0]), None)
                    dietId = itemValue[0] if (itemValue and len(itemValue) == 2) else None
                    if dietId:
                        for key, item in items.items():
                            if key:
                                row = dates.index(key[0])
                                if key[1] == header[0] and (item and item[0] == dietId) and (row not in selectRowList):
                                    self.selectRow(row)


    def on_duplicateSelectRows(self):
        currentRow = self.currentIndex().row()
        if currentRow < len(self.model().dates):
            selectIndexes = self.selectedIndexes()
            selectRowList = []
            for selectIndex in selectIndexes:
                selectRow = selectIndex.row()
                if selectRow not in selectRowList:
                    selectRowList.append(selectRow)
            selectRowList.sort()
            headers = self.model().headers
            for row in selectRowList:
                date = self.model().dates[row]
                maxDates = []
                for dat in self.model().dates:
                    if dat:
                        maxDates.append(QDate(dat))
                maxDates.sort()
                newDate = maxDates[len(maxDates)-1].addDays(1)
                for mealTimeId, mealTimeName in headers:
                    if mealTimeId:
                        itemValue = self.model().items.get((date, mealTimeId), None)
                        record = itemValue[1] if (itemValue and len(itemValue) == 2) else None
                        newRecord = self.model().getEmptyRecord()
                        if record:
                            newRecord.setValue('diet_id', record.value('diet_id'))
                        else:
                            newRecord.setValue('diet_id', toVariant(0))
                        newRecord.setValue('date', toVariant(newDate))
                        newRecord.setValue('finance_id', record.value('finance_id'))
                        newRecord.setValue('typeFeed', record.value('typeFeed'))
                        newRecord.setValue('mealTime_id', toVariant(mealTimeId))
                        newRecord.setValue('patron_id', record.value('patron_id'))
                        newRecord.setValue('featuresToEat', record.value('featuresToEat'))
                        pyNewDate = pyDate(newDate)
                        self.model().items[(pyNewDate, mealTimeId)] = (forceRef(newRecord.value('diet_id')), newRecord)
                vCnt = len(self.model().dates)-1
                vIndex = QModelIndex()
                self.model().beginInsertRows(vIndex, vCnt, vCnt)
                self.model().insertRows(vCnt, 1, vIndex)
                self.model().dates.insert(vCnt, pyNewDate)
                self.model().endInsertRows()
            self.model().reset()


    def colKey(self, col):
        pass


    def resetSorting(self):
        pass


    def loadPreferences(self, preferences):
        pass


    def savePreferences(self):
        preferences = {}
        return preferences


    def addContentToTextCursor(self, cursor):
        pass
