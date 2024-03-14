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
from PyQt4.QtCore import (
                                    Qt,
                                    SIGNAL,
#                                    QAbstractTableModel,
#                                    QDate,
#                                    QDateTime,
#                                    QEvent,
#                                    QEventLoop,
#                                    QModelIndex,
#                                    QString,
#                                    QVariant,
#                                    QObject,
                         )

#from Reports.ReportBase       import CReportBase, createTable
from library.ClientRecordProperties import CRecordProperties
#from library.crbcombobox      import CRBModelDataCache, CRBLikeEnumModel, CRBComboBox
#from library                  import database
from library.Utils            import (
#                                        CColsMovingFeature,
                                        copyFields,
                                        forceBool,
#                                        forceDate,
#                                        forceDateTime,
#                                        forceInt,
                                        forceRef,
#                                        forceString,
#                                        forceStringEx,
#                                        formatDate,
#                                        formatDateTime,
#                                        formatName,
#                                        formatSex,
#                                        formatTime,
                                        #getPref,
#                                        setPref,
                                        toVariant,
#                                        trim,
                                     )
from library.InDocTable       import CInDocTableView, CRecordListModel
from Events.Action            import CAction
from Events.Utils             import inMedicalDiagnosis
from Users.Rights             import urReadMedicalDiagnosis, urEditMedicalDiagnosis


class CEventMedicalDiagnosisInDocTableView(CInDocTableView):
    def __init__(self, parent):
        CInDocTableView.__init__(self, parent)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)


    def on_popupMenu_aboutToShow(self):
        model = self.model()
        rowCount = model.realRowCount() if hasattr(model, 'realRowCount') else model.rowCount()
        row = self.currentIndex().row()
        column = self.currentIndex().column()
        hasRight = QtGui.qApp.userHasRight(urReadMedicalDiagnosis) and QtGui.qApp.userHasRight(urEditMedicalDiagnosis)
        if self._CInDocTableView__actUpRow:
            self._CInDocTableView__actUpRow.setEnabled(0<row<rowCount and hasRight)
        if self._CInDocTableView__actDownRow:
            self._CInDocTableView__actDownRow.setEnabled(0<=row<rowCount-1 and hasRight)
        if self._CInDocTableView__actDuplicateCurrentRow:
            self._CInDocTableView__actDuplicateCurrentRow.setEnabled(0<=row<rowCount and hasRight)
        if self._CInDocTableView__actAddFromReportRow:
            self._CInDocTableView__actAddFromReportRow.setEnabled(rowCount <= 0 and hasRight)
        if self._CInDocTableView__actDeleteRows:
            rows = self.getSelectedRows()
            canDeleteRow = False
            items = self.model().items()
            record, action = items[row] if items else (None, None)
            if action:
                record = action.getRecord()
                if QtGui.qApp.userId == forceRef(record.value('person_id')):
                    canDeleteRow = True
            if canDeleteRow and self._CInDocTableView__delRowsChecker:
                canDeleteRow = self._CInDocTableView__delRowsChecker(rows)
            if len(rows) == 1 and rows[0] == row:
                self._CInDocTableView__actDeleteRows.setText(u'Удалить текущую строку')
            elif len(rows) == 1:
                self._CInDocTableView__actDeleteRows.setText(u'Удалить выделенную строку')
            else:
                self._CInDocTableView__actDeleteRows.setText(u'Удалить выделенные строки')
            if canDeleteRow and self._CInDocTableView__delRowsIsExposed:
                canDeleteRow = canDeleteRow and self._CInDocTableView__delRowsIsExposed(rows)
            self._CInDocTableView__actDeleteRows.setEnabled(canDeleteRow and hasRight)
            if self._CInDocTableView__actDuplicateSelectRows:
                self._CInDocTableView__actDuplicateSelectRows.setEnabled(canDeleteRow and hasRight)
        if self._CInDocTableView__actSelectAllRow:
            self._CInDocTableView__actSelectAllRow.setEnabled(0<=row<rowCount and hasRight)
        if self._CInDocTableView__actSelectRowsByData:
            items = self.model().items()
            record, action = items[row] if items else (None, None)
            value = record.value(column) if record and row < len(items) else None
            self._CInDocTableView__actSelectRowsByData.setEnabled(forceBool(0<=row<rowCount and (value and value.isValid())) and hasRight)
        if self._CInDocTableView__actClearSelectionRow:
            self._CInDocTableView__actClearSelectionRow.setEnabled(0<=row<rowCount and hasRight)
        if self._CInDocTableView__actCheckedAllRow:
            self._CInDocTableView__actCheckedAllRow.setEnabled(0<=row<rowCount and hasRight)
        if self._CInDocTableView__actClearCheckedAllRow:
            self._CInDocTableView__actClearCheckedAllRow.setEnabled(0<=row<rowCount and hasRight)
        if self._CInDocTableView__actRecordProperties:
            self._CInDocTableView__actRecordProperties.setEnabled(0<=row<rowCount and hasRight)
        for act, checker in self._CInDocTableView__actionsWithCheckers:
            act.setEnabled(checker() and hasRight)
        self.emit(SIGNAL('popupMenuAboutToShow()'))


    def on_deleteRows(self):
        rows = self.getSelectedRows()
        rows.sort(reverse=True)
        for row in rows:
            currentRecord, currentAction = self.model().items()[row]
            actionId = forceRef(currentRecord.value('id'))
            if actionId and actionId not in self.model().removeActions:
                self.model().removeActions.append(actionId)
            self.model().removeRow(row)
        self.model().reset()
        self.setRowHeightLoc()


    def on_selectRowsByData(self):
        items = self.model().items()
        currentRow = self.currentIndex().row()
        if currentRow < len(items):
            currentColumn = self.currentIndex().column()
            selectIndexes = self.selectedIndexes()
            selectRowList = []
            for selectIndex in selectIndexes:
                selectRow = selectIndex.row()
                if selectRow not in selectRowList:
                    selectRowList.append(selectRow)
            currentRecord, currentAction = items[currentRow]
            data = currentRecord.value(currentColumn)
            if data.isValid():
                for row, (item, action) in enumerate(items):
                    if (item.value(currentColumn) == data) and (row not in selectRowList):
                        self.selectRow(row)


    def on_duplicateCurrentRow(self):
        currentRow = self.currentIndex().row()
        items = self.model().items()
        if currentRow < len(items):
            newRecord = self.model().getEmptyRecord()
            currentRecord, currentAction = items[currentRow]
            copyFields(newRecord, currentRecord)
            newRecord.setValue(self.model()._idFieldName, toVariant(None))
            newAction = CAction(record=newRecord)
            for id in currentAction._propertiesById:
                property = newAction.getPropertyById(id)
                if property.type().valueType.isCopyable:
                    property.copy(currentAction._propertiesById[id])
            self.model().insertRecord(currentRow+1, newRecord, newAction if forceRef(newRecord.value('actionType_id')) else None)
            self.model().reset()
            self.setRowHeightLoc()


    def on_duplicateSelectRows(self):
        currentRow = self.currentIndex().row()
        items = self.model().items()
        if currentRow < len(items):
            selectIndexes = self.selectedIndexes()
            selectRowList = []
            for selectIndex in selectIndexes:
                selectRow = selectIndex.row()
                if selectRow not in selectRowList:
                    selectRowList.append(selectRow)
            selectRowList.sort()
            for row in selectRowList:
                newRecord = self.model().getEmptyRecord()
                currentRecord, currentAction = items[row]
                copyFields(newRecord, currentRecord)
                newRecord.setValue(self.model()._idFieldName, toVariant(None))
                newAction = CAction(record=newRecord)
                for id in currentAction._propertiesById:
                    property = newAction.getPropertyById(id)
                    if property.type().valueType.isCopyable:
                        property.copy(currentAction._propertiesById[id])
                items.append((newRecord, newAction if forceRef(newRecord.value('actionType_id')) else None))
            self.model().reset()
            self.setRowHeightLoc()


    def on_checkedAllRow(self):
        items = self.model().items()
        for row, (record, action) in items.items():
            record.setValue('include', toVariant(2))
            if action:
                recordAction = action.getRecord()
                recordAction.setValue('include', toVariant(2))
            items[row] = (record, action)


    def on_clearCheckedAllRow(self):
        items = self.model().items()
        for row, (record, action) in items.items():
            record.setValue('include', toVariant(0))
            items[row] = (record, action)


    def showRecordProperties(self):
        currentRow = self.currentIndex().row()
        items = self.model().items()
        if currentRow < len(items):
            (record, action) = items[currentRow]
            itemId = forceRef(record.value('id'))
        else:
            return
        table = self.model().table
        CRecordProperties(self, table, itemId).exec_()


    def setRowHeightLoc(self):
        items = self.model().items()
        h = self.fontMetrics().height()
        heightRow = 3*h/2
        for row, item in enumerate(items):
            record, action = item
            if action:
                heightMax = heightRow
                propertyLineMax = 3
                actionType = action.getType()
                propertyLine = 0
                for name, propertyType in actionType._propertiesByName.items():
                    if propertyType.inMedicalDiagnosis and inMedicalDiagnosis[propertyType.inMedicalDiagnosis].lower() in [u'основной', u'осложнения', u'сопутствующие']:
                        if action[name]:
                            cnt = len(action[name])/64 + 1 if len(action[name]) % 64 > 0 else 0
                            propertyLine += cnt if cnt else 1
                propertyLineMax = max(propertyLineMax, propertyLine)
                height = heightRow * propertyLineMax
                heightMax = max(heightMax, height)
                self.setRowHeight(row, heightMax)


    def on_sortByColumn(self, logicalIndex):
        currentIndex = self.currentIndex()
        currentItem = self.currentItem()
        model = self.model()
        if isinstance(model, CRecordListModel):
            header=self.horizontalHeader()
            if model.cols()[logicalIndex].sortable():
                if self._CInDocTableView__sortColumn == logicalIndex:
                    self._CInDocTableView__sortAscending = not self.__sortAscending
                else:
                    self._CInDocTableView__sortColumn = logicalIndex
                    self._CInDocTableView__sortAscending = True
                header.setSortIndicatorShown(True)
                header.setSortIndicator(self._CInDocTableView__sortColumn, Qt.AscendingOrder if self._CInDocTableView__sortAscending else Qt.DescendingOrder)
                model.sortData(logicalIndex, self._CInDocTableView__sortAscending)
            elif self._CInDocTableView__sortColumn is not None:
                header.setSortIndicator(self._CInDocTableView__sortColumn, Qt.AscendingOrder if self._CInDocTableView__sortAscending else Qt.DescendingOrder)
            else:
                header.setSortIndicatorShown(False)
            if currentItem:
                newRow = model.items().index(currentItem)
                self.setCurrentIndex(model.index(newRow, currentIndex.column()))
            else:
                self.setCurrentIndex(model.index(0, 0))
        else:
            header=self.horizontalHeader()
            if self._CInDocTableView__sortColumn == logicalIndex:
                self._CInDocTableView__sortAscending = not self._CInDocTableView__sortAscending
            else:
                self._CInDocTableView__sortColumn = logicalIndex
                self._CInDocTableView__sortAscending = True
            sortOrder = Qt.AscendingOrder if self._CInDocTableView__sortAscending else Qt.DescendingOrder
            header.setSortIndicatorShown(True)
            header.setSortIndicator(self._CInDocTableView__sortColumn, sortOrder)
            model.sort(logicalIndex, sortOrder)

