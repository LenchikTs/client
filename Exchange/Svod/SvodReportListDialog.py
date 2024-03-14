# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *

import Exchange.AttachService as AttachService

from Exchange.Svod.SvodF12 import autoCalcF12
from Exchange.Svod.SvodNewReportDialog import CSvodNewReportDialog
from Exchange.Svod.SvodEditReportDialog import CSvodEditReportDialog
from library.DialogBase import CConstructHelperMixin
from library.TableModel import CTableModel, CTextCol, CDateCol, CEnumCol, CDesignationCol
from library.Utils import *

from SvodReportTable import CReportTableModel
from Ui_SvodReportListDialog import Ui_SvodReportListDialog

AutoCalculators = {
    u'Стат.Форма12': autoCalcF12
}

class CSvodReportListDialog(QtGui.QDialog, CConstructHelperMixin, Ui_SvodReportListDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.addModels('ReportList', CReportListModel(self))
        self.addModels('ReportTables', CReportTablesTreeModel(self))
        self.setupUi(self)
        self.progressBar.setVisible(False)
        self.setModels(self.tblReportList, self.modelReportList, self.selectionModelReportList)
        header = self.tblReportList.horizontalHeader()
        header.setSortIndicatorShown(True)
        header.setSortIndicator(0, Qt.AscendingOrder)
        QObject.connect(header, SIGNAL('sectionClicked(int)'), self.setSort)
        self.setModels(self.tvReportTables, self.modelReportTables, self.selectionModelReportTables)
        self.tvReportTables.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.btnCalcReportValues.setEnabled(False)
        self.btnExportReport.setEnabled(True)
        self.clearReportEditor()
        self.reportSelectionChanged()

    def showEvent(self, event):
        QTimer.singleShot(0, self.updateList)
        
    def disableControls(self):
        self.grpReportList.setEnabled(False)
        self.grpCurrentReport.setEnabled(False)
        QtGui.qApp.processEvents()

    def enableControls(self):
        self.grpReportList.setEnabled(True)
        self.grpCurrentReport.setEnabled(True)
        QtGui.qApp.processEvents()
        
    def updateList(self):
        self.clearReportEditor()
        self.modelReportList.update()
        self.reportSelectionChanged()
    
    def export(self):
        reportId = self.currentReportId()
        self.disableControls()
        try:
            result = AttachService.svodSendReport(reportId)
            self.updateList()
        except Exception as e:
            QtGui.QMessageBox.critical(self, u'Произошла ошибка', exceptionToUnicode(e), QtGui.QMessageBox.Close)
        finally:
            self.enableControls()
    
    def currentReportId(self):
        return self.tblReportList.currentItemId()
    
    def currentReportCode(self):
        itemId = self.currentReportId()
        if itemId:
            itemRecord = self.modelReportList.recordCache().get(itemId)
            if itemRecord:
                return forceString(itemRecord.value('externalCode'))
        return None

    def setSort(self, newColumn):
        newOrderField = self.modelReportList.orderByColumn[newColumn]
        if newOrderField is None:
            return
        column, asc = self.modelReportList.order
        if column == newColumn:
            newAsc = not asc
        else:
            newAsc = True
        self.modelReportList.order = (newColumn, newAsc)
        self.updateList()
    
    def clearReportEditor(self):
        self.modelReportTables.setReportId(None)
        self.tblReportTable.setModel(None)

    def generateReportEditor(self):
        self.tblReportTable.setModel(None)
        reportId = self.currentReportId()
        self.progressBar.setVisible(True)
        self.disableControls()
        try:
            self.modelReportTables.setReportId(reportId, self.progressBar)
        finally:
            self.progressBar.setVisible(False)
            self.enableControls()

    def deleteReport(self):
        if QtGui.QMessageBox.question(
            self,
            u"Внимание!",
            u"Вы действительно хотите удалить отчет?",
            QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
            QtGui.QMessageBox.No
        ) != QtGui.QMessageBox.Yes:
            return
        reportId = self.currentReportId()
        if reportId is None:
            return
        self.clearReportEditor()
        db = QtGui.qApp.db
        db.transaction()
        self.disableControls()
        try:
            db.deleteRecord('SvodIndex', where='reportSection_id in (select id from SvodReportSection where report_id = %d)' % reportId)
            db.deleteRecord('SvodTableRow', where='table_id in (select id from SvodTable where report_id = %d)' % reportId)
            db.deleteRecord('SvodTableColumn', where='table_id in (select id from SvodTable where report_id = %d)' % reportId)
            db.deleteRecord('SvodTable', where='report_id = %d' % reportId)
            db.deleteRecord('SvodReportSection', where='report_id = %d' % reportId)
            db.deleteRecord('SvodReport', where='id = %d' % reportId)
            db.commit()
        except Exception, e:
            db.rollback()
            raise e
        finally:
            self.enableControls()
        self.updateList()
    
    def reportSelectionChanged(self):
        reportId = self.currentReportId()
        if reportId:
            QtGui.qApp.callWithWaitCursor(self, self.generateReportEditor)
            code = self.currentReportCode()
            self.btnCalcReportValues.setEnabled(code in AutoCalculators)
            self.btnEditReport.setEnabled(True)
            self.btnDeleteReport.setEnabled(True)
        else:
            self.btnCalcReportValues.setEnabled(False)
            self.btnEditReport.setEnabled(False)
            self.btnDeleteReport.setEnabled(False)


    @pyqtSignature('')
    def on_btnClose_clicked(self):
        self.reject()

    @pyqtSignature('')
    def on_btnExportReport_clicked(self):
        self.export()
    
    @pyqtSignature('')
    def on_btnNewReport_clicked(self):
        if CSvodNewReportDialog(self).exec_():
            self.updateList()
    
    @pyqtSignature('')
    def on_btnEditReport_clicked(self):
        reportId = self.currentReportId()
        if reportId is None:
            return
        if CSvodEditReportDialog(self, reportId).exec_():
            self.updateList()
    
    @pyqtSignature('')
    def on_btnCalcReportValues_clicked(self):
        code = self.currentReportCode()
        if code in AutoCalculators:
            calculator = AutoCalculators[code]
            calculator(self.modelReportTables)
    
    @pyqtSignature('')
    def on_btnDeleteReport_clicked(self):
        self.deleteReport()
    
    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelReportList_currentRowChanged(self, current, previous):
        self.reportSelectionChanged()
    
    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelReportTables_currentRowChanged(self, current, previous):
        if current.isValid():
            item = current.internalPointer()
            tableModel = item.tableModel
        else:
            tableModel = None
        self.tblReportTable.setModel(tableModel)
        self.tblReportTable.resizeRowsToContents()

class CReportListModel(CTableModel):
    def __init__(self, parent):
        self.orderByColumn = [
            'SvodReport.externalCode',
            'SvodReport.date',
            'OrgStructure.name',
            'SvodReport.exportStatus',
        ]
        self.order = (0, True)
        CTableModel.__init__(self, parent)
        self.addColumn(CTextCol(u'Форма', ['externalCode'], 20))
        self.addColumn(CDateCol(u'Дата', ['date'], 20))
        self.addColumn(CDesignationCol(u'Подразделение', ['orgStructure_id'], ('OrgStructure', 'name'), 20))
        self.addColumn(CEnumCol(u'Статус', ['exportStatus'], (u"не отправлен", u"отправлен"), 20))
        self.setTable('SvodReport')

    def update(self):
        db = QtGui.qApp.db

        sql = u"""
            select SvodReport.id
            from SvodReport
                left join OrgStructure on OrgStructure.id = SvodReport.orgStructure_id
        """
        orderColumnIndex, isAscending = self.order
        orderBy = self.orderByColumn[orderColumnIndex]
        orderBy += (' asc' if isAscending else ' desc')
        sql += (' order by ' + orderBy)
        
        idList = []
        query = db.query(sql)
        while query.next():
            record = query.record()
            reportId = record.value('id').toInt()[0]
            idList.append(reportId)
        self.setIdList(idList)

class CReportTablesTreeModel(QAbstractItemModel):
    def __init__(self, parent):
        QAbstractItemModel.__init__(self, parent)
        self.rootItem = CReportTablesTreeItem(None, u"")
        self.tableModels = {}
    
    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        if role != Qt.DisplayRole:
            return QVariant()
        item = index.internalPointer()
        return item.data(index.column())
    
    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            if section == 0:
                return u"Наименование"
            elif section == 1:
                return u"Заполнено"
        return QVariant()

    def flags(self, index):
        if not index.isValid():
            return 0
        item = index.internalPointer()
        return item.flags()

    def index(self, row, column, parent = QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        if parent.isValid():
            parentItem = parent.internalPointer()
        else:
            parentItem = self.rootItem
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        item = index.internalPointer()
        parentItem = item.parentItem
        if parentItem == self.rootItem:
            return QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent = QModelIndex()):
        if parent.isValid():
            parentItem = parent.internalPointer()
            return parentItem.childCount()
        else:
            return self.rootItem.childCount()

    def columnCount(self, parent = QModelIndex()):
        return 2
    
    def setReportId(self, reportId, progressBar = None):
        if hasattr(self, 'beginResetModel'):
            self.beginResetModel()
        try:
            self.rootItem.clear()
            self.tableModels = {}
            if reportId:
                db = QtGui.qApp.db
                tableRecords = db.getRecordList('SvodTable', cols='id, code, name', where='report_id = %d' % reportId, order='code')
                sectionRecords = db.getRecordList('SvodReportSection', cols='id, externalCode', where='report_id = %d' % reportId, order='id')
                if progressBar:
                    progressBar.setMaximum(len(tableRecords) * len(sectionRecords))
                    progressBar.setValue(0)
                for sectionRecord in sectionRecords:
                    sectionId = forceRef(sectionRecord.value('id'))
                    sectionName = forceString(sectionRecord.value('externalCode'))
                    if sectionName:
                        parentItem = self.rootItem.addChild(sectionName)
                    else:
                        parentItem = self.rootItem
                    self.tableModels[sectionName] = {}
                    for tableRecord in tableRecords:
                        tableId = forceRef(tableRecord.value('id'))
                        tableCode = forceString(tableRecord.value('code'))
                        tableName = forceString(tableRecord.value('name'))
                        tableModel = CReportTableModel(self, sectionId, tableId)
                        parentItem.addChild(tableName, tableModel)
                        self.tableModels[sectionName][tableCode] = tableModel
                        if progressBar:
                            progressBar.setValue(progressBar.value() + 1)
                            QtGui.qApp.processEvents()
        finally:
            if hasattr(self, 'endResetModel'):
                self.endResetModel()
            else:
                self.reset()


class CReportTablesTreeItem:
    def __init__(self, parentItem, name, tableModel = None):
        self.parentItem = parentItem
        self.name = name
        self.tableModel = tableModel
        self.children = []
    
    def addChild(self, name, tableModel = None):
        newItem = CReportTablesTreeItem(self, name, tableModel)
        self.children.append(newItem)
        return newItem

    def data(self, column):
        if column == 0:
            return QVariant(self.name)
        elif column == 1:
            return QVariant("%d%%" % self.fillPercentage())

    def flags(self):
        result = Qt.ItemIsEnabled
        if self.tableModel is not None:
            result |= Qt.ItemIsSelectable
        return result

    def child(self, row):
        return self.children[row]
    
    def childCount(self):
        return len(self.children)
    
    def row(self):
        if self.parentItem:
            return self.parentItem.children.index(self)
        else:
            return 0
    
    def clear(self):
        self.children = []
    
    def totalIndexes(self):
        if self.tableModel:
            return self.tableModel.totalIndexes()
        else:
            return sum([child.totalIndexes() for child in self.children])
    
    def filledIndexes(self):
        if self.tableModel:
            return self.tableModel.filledIndexes()
        else:
            return sum([child.filledIndexes() for child in self.children])
    
    def fillPercentage(self):
        totalIndexes = self.totalIndexes()
        if totalIndexes == 0:
            return None
        else:
            return self.filledIndexes() * 100 / totalIndexes