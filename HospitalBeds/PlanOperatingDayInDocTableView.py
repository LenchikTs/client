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
from PyQt4.QtCore import Qt, SIGNAL, QString, QVariant, QSize

from library.ClientRecordProperties import CRecordProperties
from library.Utils            import copyFields, forceBool, forceRef, forceStringEx, toVariant
from library.InDocTable       import CInDocTableView, CRecordListModel, CLocItemDelegate
from Events.Action            import CAction
from Events.ActionProperty    import CJobTicketActionPropertyValueType
from Events.ActionPropertiesTable import CActionPropertyDelegate, CActionPropertyBaseDelegate


updateEditorHeight = 1
updateRowHeight = 10


class CLocPlanOperatingItemDelegate(CLocItemDelegate):
    def __init__(self, parent, lineHeight):
        CLocItemDelegate.__init__(self, parent)
        self.lineHeight = lineHeight


    def updateEditorGeometry(self, editor, option, index):
        QtGui.QItemDelegate.updateEditorGeometry(self, editor, option, index)
        index.model().afterUpdateEditorGeometry(editor, index)
        if isinstance(editor, QtGui.QTextEdit):
            editor.resize(editor.width(), updateEditorHeight*editor.height())


    def sizeHint(self, option, index):
        result = QSize(10, self.lineHeight*updateRowHeight)
        return result


class CJobTicketsDelegate(QtGui.QItemDelegate):
    def __init__(self, lineHeight, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)
        self.lineHeight = lineHeight


    def commit(self):
        editor = self.sender()
        self.emit(SIGNAL('commitData(QWidget *)'), editor)


    def commitAndCloseEditor(self):
        editor = self.sender()
        self.emit(SIGNAL('commitData(QWidget *)'), editor)
        self.emit(SIGNAL('closeEditor(QWidget *,QAbstractItemDelegate::EndEditHint)'), editor, QtGui.QAbstractItemDelegate.NoHint)


    def createEditor(self, parent, option, index):
        model = index.model()
        action, domain, clientId, eventTypeId, reservedJobTickets = model.getEditorInitValues(index)
        domain = CJobTicketActionPropertyValueType.parseDomain(domain)
        editor = CJobTicketActionPropertyValueType.CPropEditor(action, domain,
                                                               parent, clientId, eventTypeId, reservedJobTickets)
        self.connect(editor, SIGNAL('commit()'), self.commit)
        self.connect(editor, SIGNAL('editingFinished()'), self.commitAndCloseEditor)
        return editor


    def setEditorData(self, editor, index):
        model = index.model()
        value = model.data(index, Qt.EditRole)
        editor.setValue(value)


    def setModelData(self, editor, model, index):
        model = index.model()
        value = editor.value()
        model.setData(index, toVariant(value))


    def sizeHint(self, option, index):
        result = QSize(10, self.lineHeight*updateRowHeight)
        return result


class CMedicalDiagnosisDelegate(CActionPropertyDelegate):
    def __init__(self, lineHeight, parent=None):
        CActionPropertyDelegate.__init__(self, lineHeight, parent)
        self.lineHeight = lineHeight


    def paint(self, painter, option, index):
        CActionPropertyBaseDelegate.paint(self, painter, option, index)


    def commit(self):
        editor = self.sender()
        self.emit(SIGNAL('commitData(QWidget *)'), editor)


    def commitAndCloseEditor(self):
        editor = self.sender()
        self.emit(SIGNAL('commitData(QWidget *)'), editor)
        self.emit(SIGNAL('closeEditor(QWidget *,QAbstractItemDelegate::EndEditHint)'), editor, QtGui.QAbstractItemDelegate.NoHint)


    def createEditor(self, parent, option, index):
        editor = QtGui.QTextEdit(parent)
        editor.setLineWrapMode(QtGui.QTextEdit.WidgetWidth)
        editor.setWordWrapMode(QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.connect(editor, SIGNAL('commit()'), self.commit)
        self.connect(editor, SIGNAL('editingFinished()'), self.commitAndCloseEditor)
        return editor


    def alignment(self):
        return QVariant(Qt.AlignLeft + Qt.AlignTop)


    def setEditorData(self, editor, index):
        model = index.model()
        value = model.data(index, Qt.EditRole)
        editor.setPlainText(forceStringEx(value))


    def setModelData(self, editor, model, index):
        model = index.model()
        value = editor.toPlainText()
        model.setData(index, toVariant(value))


    def sizeHint(self, option, index):
        result = QSize(10, self.lineHeight*updateRowHeight)
        return result


    def updateEditorGeometry(self, editor, option, index):
        QtGui.QItemDelegate.updateEditorGeometry(self, editor, option, index)
        index.model().afterUpdateEditorGeometry(editor, index)
        if isinstance(editor, QtGui.QTextEdit):
            editor.resize(editor.width(), updateEditorHeight*editor.height())


class CPlanOperatingDayVerticalHeaderView(QtGui.QHeaderView):
    def __init__(self, orientation, parent=None):
        QtGui.QHeaderView.__init__(self, orientation, parent)


    def sectionSizeFromContents(self, logicalIndex):
        model = self.model()
        if model:
            orientation = self.orientation()
            opt = QtGui.QStyleOptionHeader()
            self.initStyleOption(opt)
            var = model.headerData(logicalIndex, orientation, Qt.FontRole)
            if var and var.isValid() and var.type() == QVariant.Font:
                fnt = var.toPyObject()
            else:
                fnt = self.font()
            opt.fontMetrics = QtGui.QFontMetrics(fnt)
            sizeText = QSize(4,4)
            opt.text = model.headerData(logicalIndex, orientation, Qt.DisplayRole).toString()
            sizeText = self.style().sizeFromContents(QtGui.QStyle.CT_HeaderSection, opt, sizeText, self)
            sizeFiller = QSize(4,4)
            opt.text = QString('x'*CPlanOperatingDayInDocTableView.titleWidth)
            sizeFiller = self.style().sizeFromContents(QtGui.QStyle.CT_HeaderSection, opt, sizeFiller, self)
            return QSize(max(sizeText.width(), sizeFiller.width()),
                         max(sizeText.height(), sizeFiller.height())
                        )
        else:
            return QtGui.QHeaderView.sectionSizeFromContents(self, logicalIndex)


class CPlanOperatingDayInDocTableView(CInDocTableView):
    titleWidth = 0

    Col_Number                 = 0
    Col_Fio                    = 1
    Col_Placement              = 2
    Col_ExternalId             = 3
    Col_MKB                    = 4
    Col_MedicalDiagnosis       = 5
    Col_Status                 = 6
    Col_ActionTypeId           = 7
    Col_PersonId               = 8
    Col_AssistantId            = 9
    Col_AssistantTeam          = 10
    Col_AnestesiaTeam          = 11
    Col_AssistantAnestesiaTeam = 12
    Col_Note                   = 13
    Col_PlanedTime             = 14
    Col_JobTicked              = 15


    def __init__(self, parent):
        CInDocTableView.__init__(self, parent)
        self.__sortAscending = None
        h = self.fontMetrics().height()
        self._verticalHeader = CPlanOperatingDayVerticalHeaderView(Qt.Vertical, self)
        self.setVerticalHeader(self._verticalHeader)
        self.verticalHeader().setDefaultSectionSize(3*h/2)
        #self.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        #self.verticalHeader().setResizeMode(QtGui.QHeaderView.Interactive)
        #self.verticalHeader().setCascadingSectionResizes(True)
        #self.verticalHeader().hide()
        self.setWordWrap(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setItemDelegate(CLocPlanOperatingItemDelegate(self, h))
        self.setItemDelegateForColumn(CPlanOperatingDayInDocTableView.Col_MedicalDiagnosis, CMedicalDiagnosisDelegate(h, self))
        self.setItemDelegateForColumn(CPlanOperatingDayInDocTableView.Col_JobTicked, CJobTicketsDelegate(h, self))
        self.resizeRowsToContents()


    def on_popupMenu_aboutToShow(self):
        model = self.model()
        rowCount = model.realRowCount() if hasattr(model, 'realRowCount') else model.rowCount()
        row = self.currentIndex().row()
        if self._CInDocTableView__actUpRow:
            self._CInDocTableView__actUpRow.setEnabled(0<row<rowCount)
        if self._CInDocTableView__actDownRow:
            self._CInDocTableView__actDownRow.setEnabled(0<=row<rowCount-1)
        if self._CInDocTableView__actDuplicateCurrentRow:
            self._CInDocTableView__actDuplicateCurrentRow.setEnabled(0<=row<rowCount)
        if self._CInDocTableView__actAddFromReportRow:
            self._CInDocTableView__actAddFromReportRow.setEnabled(rowCount <= 0)
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
            if canDeleteRow and self._CInDocTableView__delRowsIsExposed:
                canDeleteRow = self._CInDocTableView__delRowsIsExposed(rows)
            self._CInDocTableView__actDeleteRows.setEnabled(canDeleteRow)
            if self._CInDocTableView__actDuplicateSelectRows:
                self._CInDocTableView__actDuplicateSelectRows.setEnabled(canDeleteRow)
        if self._CInDocTableView__actSelectAllRow:
            self._CInDocTableView__actSelectAllRow.setEnabled(0<=row<rowCount)
        if self._CInDocTableView__actSelectRowsByData:
            column = self.currentIndex().column()
            items = self.model().items()
            record, action = items[row] if items else (None, None)
            value = record.value(column) if record and row < len(items) else None
            self._CInDocTableView__actSelectRowsByData.setEnabled(forceBool(0<=row<rowCount and (value and value.isValid())))
        if self._CInDocTableView__actClearSelectionRow:
            self._CInDocTableView__actClearSelectionRow.setEnabled(0<=row<rowCount)
        if self._CInDocTableView__actCheckedAllRow:
            self._CInDocTableView__actCheckedAllRow.setEnabled(0<=row<rowCount)
        if self._CInDocTableView__actClearCheckedAllRow:
            self._CInDocTableView__actClearCheckedAllRow.setEnabled(0<=row<rowCount)
        if self._CInDocTableView__actRecordProperties:
            self._CInDocTableView__actRecordProperties.setEnabled(0<=row<rowCount)
        for act, checker in self._CInDocTableView__actionsWithCheckers:
            act.setEnabled(checker())
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
        pass


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

