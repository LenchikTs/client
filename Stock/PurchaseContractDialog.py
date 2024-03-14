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
from PyQt4.QtCore import Qt, pyqtSignature, QDate, QDateTime, QVariant

from library.crbcombobox         import CRBComboBox
from library.InDocTable          import (
                                         CInDocTableModel,
                                         CDateInDocTableCol,
                                         CFloatInDocTableCol,
                                         CInDocTableCol,
                                         CRBInDocTableCol,
                                        )
from library.ItemsListDialog     import CItemEditorBaseDialog
from library.interchange         import (
                                         getComboBoxValue,
                                         setComboBoxValue,
                                         getRBComboBoxValue,
                                         setRBComboBoxValue,
                                         getLineEditValue,
                                         setLineEditValue,
                                         setCheckBoxValue,
                                         getCheckBoxValue,
                                         setDateEditValue,
                                         getDateEditValue,
                                        )
from library.PrintInfo           import CInfoContext
from library.PrintTemplates      import (
                                         applyTemplate,
                                         CPrintAction,
                                         CPrintButton,
                                         getPrintTemplates,
                                        )
from library.Utils               import forceDouble, forceRef, forceInt, forceString, toVariant
from library.Counter             import CCounterController
from Reports.ReportBase          import CReportBase, createTable
from Reports.ReportView          import CReportViewDialog
from Stock.NomenclatureComboBox  import CNomenclatureInDocTableCol
from Stock.Utils                 import (
                                         getStockMotionItemQuantityColumn,
                                         getBatchShelfTimeFinance,
                                         CSummaryInfoModelMixin,
                                        )
from RefBooks.Nomenclature.List  import CRBNomenclatureEditor
from Orgs.Orgs                   import selectOrganisation


from Stock.Ui_PurchaseContractDialog import Ui_PurchaseContractDialog


class CPurchaseContractEditDialog(Ui_PurchaseContractDialog, CItemEditorBaseDialog):
    #Контракт на закупку

    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, 'StockPurchaseContract')
        self.addModels('Items', CItemsModel(self))
        self.addModels('AdditionallyAgreement', CAdditionallyAgreementModel(self))
        self.addObject('btnPrint', CPrintButton(self, u'Печать'))
        self.addObject('actOpenNomenclatureEditor', QtGui.QAction(u'Редактировать', self))
        self.setupUi(self)
        self.tblItems.setModel(self.modelItems)
        self.tblAdditionallyAgreement.setModel(self.modelAdditionallyAgreement)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setupDirtyCather()
        self.tblItems.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.tblItems.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblItems.addPopupAction(self.actOpenNomenclatureEditor)
        self.tblItems.addPopupDelRow()
        self.tblAdditionallyAgreement.addPopupDelRow()
        self.cmbFinance.setTable('rbFinance', addNone=True)
        self.cmbFinanceSource.setTable('rbFinanceSource', addNone=True)
        self.cmbSupplierOrg.setFilter('isSupplier = 1')
        self.btnPrint.setShortcut('F6')
        self.buttonBox.addButton(self.btnPrint, QtGui.QDialogButtonBox.ActionRole)
        templates = getPrintTemplates(self.getStockContext())
        if not templates:
            self.btnPrint.setId(-1)
        else:
            for template in templates:
                action = CPrintAction(template.name, template.id, self.btnPrint, self.btnPrint)
                self.btnPrint.addAction(action)
            self.btnPrint.menu().addSeparator()
            self.btnPrint.addAction(CPrintAction(u'Напечатать список', -1, self.btnPrint, self.btnPrint))


    def _checkStockMotionItemsData(self, tblItems):
        model = tblItems.model()
        items = model.items()
        for idx, item in enumerate(items):
            qnt = forceDouble(item.value('qnt'))
            if qnt <= 0:
                return self.checkValueMessage(
                    u'Количество должно быть больше нуля!', False, tblItems, idx, model.getColIndex('qnt')
                )
        return True


    def resetCounterNumber(self):
        return False


    def exec_(self):
        counterController = QtGui.qApp.counterController()
        if not counterController:
            QtGui.qApp.setCounterController(CCounterController(self))
        result = None
        try:
            result = CItemEditorBaseDialog.exec_(self)
        finally:
            if not counterController:
                if result:
                    QtGui.qApp.delAllCounterValueIdReservation()
                else:
                    QtGui.qApp.resetAllCounterValueIdReservation()
            elif self.resetCounterNumber() and counterController.lastReservationId:
                QtGui.qApp.resetCounterValueIdReservation(counterController.lastReservationId)
        if not counterController:
            QtGui.qApp.setCounterController(None)
        return result


    def getStockContext(self):
        return ['PurchaseContract']


    @pyqtSignature('int')
    def on_cmbFinance_currentIndexChanged(self, index):
        financeId = self.cmbFinance.value()
        if financeId:
            self.cmbFinanceSource.setFilter('master_id = %d' % financeId)
        else:
            self.cmbFinanceSource.setFilter('')


    @pyqtSignature('int')
    def on_btnPrint_printByTemplate(self, templateId):
        self.actPrintPurchaseContract(templateId)


    @pyqtSignature('')
    def on_btnSelectOrganisation_clicked(self):
        orgId = selectOrganisation(self, None, True, params={'isActive':2, 'isSupplier':2}, forSelect=True)
        if orgId:
            self.cmbSupplierOrg.setValue(orgId)


    @pyqtSignature('')
    def on_actOpenNomenclatureEditor_triggered(self):
        items = self.tblItems.getSelectedItems()
        if len(items) == 0:
            return
        nomenclatureId = forceInt(items[0].value('nomenclature_id'))
        record = QtGui.qApp.db.getRecord('rbNomenclature', '*', nomenclatureId)
        dialog = CRBNomenclatureEditor(self)
        dialog.setRecord(record)
        dialog.exec_()


    def actPrintPurchaseContract(self, templateId):
        from Stock.StockMotionInfo import CStockPurchaseContractInfo, CStockPurchaseContractItemInfoList, CStockPCAdditionallyAgreementInfoList
        if templateId == -1:
            self.getNomenclaturePrint()
        else:
            purchaseContractId = self.itemId()
            if purchaseContractId:
                context = CInfoContext()
                data = { 'purchaseContract':CStockPurchaseContractInfo(context, purchaseContractId), # Контракт на закупку
                         'purchaseContractList': CStockPurchaseContractItemInfoList(context, purchaseContractId), # Спецификация
                         'purchaseContractAAList': CStockPCAdditionallyAgreementInfoList(context, purchaseContractId) # Доп. соглашения
                        }
                QtGui.qApp.call(self, applyTemplate, (self, templateId, data))


    def dumpParams(self, cursor):
        db = QtGui.qApp.db
        description = []
        number = self.edtNumber.text()
        if number:
            description.append(u'Номер %s'%forceString(number))
        date = QDate(self.edtDate.date())
        if date:
           description.append(u'Дата %s'%forceString(date))
        name = self.edtName.text()
        if name:
            description.append(u'Наименование %s'%forceString(name))
        title = self.edtTitle.text()
        if title:
            description.append(u'Наименование для печати %s'%forceString(title))
        supplierId = self.cmbSupplierOrg.value()
        if supplierId:
            description.append(u'Поставщик %s'%forceString(db.translate('Organisation', 'id', supplierId, 'fullName')))
        begDate = self.edtBegDate.date()
        endDate = self.edtEndDate.date()
        if begDate or endDate:
           description.append(u'Период действия с %s по %s'%(forceString(begDate), forceString(endDate)))
        financeId = self.cmbFinance.value()
        if financeId:
            description.append(u'Тип финансирования %s'%forceString(db.translate('rbFinance', 'id', financeId, 'name')))
        description.append(u'Является государственным' if self.chkState.isChecked() else u'Не является государственным')
        description.append(u'Порядок подтверждения %s'%([u'не определено', u'прямой', u'обратный'][self.cmbConfirmationOrder.currentIndex()]))
        description.append(u'отчёт составлен: ' + forceString(QDateTime.currentDateTime()))
        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


    def getNomenclaturePrint(self):
        model = self.tblItems.model()
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.windowTitle())
        self.dumpParams(cursor)
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportSubTitle)
        cursor.insertText(u'Спецификация')
        cursor.setCharFormat(CReportBase.ReportBody)
        colWidths  = [ self.tblItems.columnWidth(i) for i in xrange(model.columnCount()-1) ]
        colWidths.insert(0,10)
        totalWidth = sum(colWidths)
        tableColumns = []
        iColNumber = False
        for iCol, colWidth in enumerate(colWidths):
            widthInPercents = str(max(1, colWidth*90/totalWidth))+'%'
            if iColNumber == False:
                tableColumns.append((widthInPercents, [u'№'], CReportBase.AlignRight))
                iColNumber = True
            tableColumns.append((widthInPercents, [forceString(model._cols[iCol].title())], CReportBase.AlignLeft))
        table = createTable(cursor, tableColumns)
        for iModelRow in xrange(model.rowCount()-1):
            iTableRow = table.addRow()
            table.setText(iTableRow, 0, iModelRow+1)
            for iModelCol in xrange(model.columnCount()):
                index = model.createIndex(iModelRow, iModelCol)
                text = forceString(model.data(index))
                table.setText(iTableRow, iModelCol+1, text)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        modelAA = self.modelAdditionallyAgreement
        cursor.setCharFormat(CReportBase.ReportSubTitle)
        cursor.insertText(u'Доп. соглашения')
        cursor.setCharFormat(CReportBase.ReportBody)
        colWidths  = [ self.tblItems.columnWidth(i) for i in xrange(modelAA.columnCount()-1) ]
        colWidths.insert(0,10)
        totalWidth = sum(colWidths)
        tableColumns = []
        iColNumber = False
        for iCol, colWidth in enumerate(colWidths):
            widthInPercents = str(max(1, colWidth*90/totalWidth))+'%'
            if iColNumber == False:
                tableColumns.append((widthInPercents, [u'№'], CReportBase.AlignRight))
                iColNumber = True
            tableColumns.append((widthInPercents, [forceString(modelAA._cols[iCol].title())], CReportBase.AlignLeft))
        table = createTable(cursor, tableColumns)
        for iModelRow in xrange(modelAA.rowCount()-1):
            iTableRow = table.addRow()
            table.setText(iTableRow, 0, iModelRow+1)
            for iModelCol in xrange(modelAA.columnCount()):
                index = modelAA.createIndex(iModelRow, iModelCol)
                text = forceString(modelAA.data(index))
                table.setText(iTableRow, iModelCol+1, text)
        cursor.movePosition(QtGui.QTextCursor.End)
        html = doc.toHtml('utf-8')
        view = CReportViewDialog(self)
        view.setText(html)
        view.exec_()


    def setDefaults(self):
        pass


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(  self.edtNumber,            record, 'number')
        setDateEditValue(  self.edtDate,              record, 'date')
        setLineEditValue(  self.edtName,              record, 'name')
        setLineEditValue(  self.edtTitle,             record, 'title')
        setRBComboBoxValue(self.cmbSupplierOrg,       record, 'supplierOrg_id')
        setDateEditValue(  self.edtBegDate,           record, 'begDate')
        setDateEditValue(  self.edtEndDate,           record, 'endDate')
        setRBComboBoxValue(self.cmbFinance,           record, 'finance_id')
        setRBComboBoxValue(self.cmbFinanceSource,     record, 'financeSource_id')
        setCheckBoxValue(  self.chkState,             record, 'isState')
        setComboBoxValue(  self.cmbConfirmationOrder, record, 'confirmationOrder')
        self.modelItems.loadItems(self.itemId())
        self.modelAdditionallyAgreement.loadItems(self.itemId())
        self.lblSummaryInfo.setText(self.modelItems.getSummaryInfo())


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(  self.edtNumber,            record, 'number')
        getDateEditValue(  self.edtDate,              record, 'date')
        getLineEditValue(  self.edtName,              record, 'name')
        getLineEditValue(  self.edtTitle,             record, 'title')
        getRBComboBoxValue(self.cmbSupplierOrg,       record, 'supplierOrg_id')
        getDateEditValue(  self.edtBegDate,           record, 'begDate')
        getDateEditValue(  self.edtEndDate,           record, 'endDate')
        getRBComboBoxValue(self.cmbFinance,           record, 'finance_id')
        getRBComboBoxValue(self.cmbFinanceSource,     record, 'financeSource_id')
        getCheckBoxValue(  self.chkState,             record, 'isState')
        getComboBoxValue(  self.cmbConfirmationOrder, record, 'confirmationOrder')
        return record


    def saveInternals(self, id):
        self.modelItems.saveItems(id)
        self.modelAdditionallyAgreement.saveItems(id)


    def checkDataEntered(self):
        result = self._checkStockMotionItemsData(self.tblItems)
        return result


    @pyqtSignature('int')
    def on_cmbSupplierOrg_currentIndexChanged(self, val):
        supplierOrgExists = bool(self.cmbSupplierOrg.value())
        self.modelItems.updateBatchShelfTimeFinance = not supplierOrgExists


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_modelItems_dataChanged(self,  topLeftIndex, bottomRightIndex):
        self.lblSummaryInfo.setText(self.modelItems.getSummaryInfo())


class CAdditionallyAgreementModel(CInDocTableModel):
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'StockPurchaseContract_AdditionallyAgreement', 'id', 'master_id', parent)
        self.addCol(CInDocTableCol(     u'Номер',      'number', 16))
        self.addCol(CDateInDocTableCol( u'Дата',       'date',   12))
        self.addCol(CInDocTableCol(     u'Примечание', 'note',   10))


class CItemsModel(CInDocTableModel, CSummaryInfoModelMixin):
    class CPriceCol(CFloatInDocTableCol):
        def toString(self, value, record):
            qnt = forceDouble(record.value('qnt'))
            if qnt:
                sum = forceDouble(record.value('sum'))
                return toVariant(self._toString(toVariant(sum/qnt)))
            return QVariant()

        def setEditorData(self, editor, value, record):
            qnt = forceDouble(record.value('qnt'))
            if qnt:
                sum = forceDouble(record.value('sum'))
                s = self._toString(toVariant(sum/qnt))
            else:
                s = ''
            editor.setText('' if s is None else s)
            editor.selectAll()

    class CSumCol(CFloatInDocTableCol):
        def _toString(self, value):
            if value.isNull():
                return None
            return format(forceDouble(value), '.2f')

    class CLocNomenclatureCol(CNomenclatureInDocTableCol):
        def __init__(self, title, fieldName, width, **params):
            CNomenclatureInDocTableCol.__init__(self, title, fieldName, width, **params)

        def createEditor(self, parent):
            editor = CNomenclatureInDocTableCol.createEditor(self, parent)
            editor.setOnlyNomenclature(True)
            return editor

    def __init__(self, parent, showExists=False):
        CInDocTableModel.__init__(self, 'StockPurchaseContract_Item', 'id', 'master_id', parent)
        self._nomenclatureColumn = self.CLocNomenclatureCol(u'ЛСиИМН', 'nomenclature_id', 50, showFields = CRBComboBox.showName)
        self._unitColumn = CRBInDocTableCol(u'Ед.Учета', 'unit_id', 12, 'rbUnit', addNone=False)
        self.addCol(self._nomenclatureColumn)
        self.addCol(CDateInDocTableCol( u'Годен до', 'shelfTime', 12, canBeEmpty=True))
        self.addCol(getStockMotionItemQuantityColumn(u'Кол-во', 'qnt', 12))
        self.addCol(self._unitColumn)
        sumCol = CItemsModel.CSumCol( u'Сумма', 'sum', 12)
        self.addCol(sumCol)
        self.addCol(CItemsModel.CPriceCol(u'Цена', 'id', 12, precision=2))
        self.priceColIndex = len(self.cols())-1
        self.priceCache = parent
        self.qntColumnIndex = self.getColIndex('qnt')
        self.updateBatchShelfTimeFinance = True


    def getNomenclatureNameById(self, nomenclatureId):
        return forceString(self._nomenclatureColumn.toString(nomenclatureId, None))


#    def getEmptyRecord(self):
#        record = CInDocTableModel.getEmptyRecord(self)
#        return record


    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False
        col = index.column()
        row = index.row()
        if col == self.getColIndex('shelfTime'):
            result = CInDocTableModel.setData(self, index, value, role)
        if col == 1:
            if not (0 <= row < len(self._items)):
                return False
            item = self._items[row]
            self.emitRowChanged(row)
            return True
        elif col == self.priceColIndex:
            if not (0 <= row < len(self._items)):
                return False
            item = self._items[row]
            qnt = forceDouble(item.value('qnt'))
            item.setValue('sum', QVariant(qnt*forceDouble(value)))
            self.emitRowChanged(row)
            return True
        elif col == self.getColIndex('qnt'):
            result = CInDocTableModel.setData(self, index, value, role)
            return result
        elif col == self.getColIndex('nomenclature_id'):
            if 0 <= row < len(self._items):
                oldNomenclatureId = forceRef(self._items[row].value('nomenclature_id'))
            else:
                oldNomenclatureId = None
            result = CInDocTableModel.setData(self, index, value, role)
            if result:
                item = self._items[row]
                nomenclatureId = forceRef(item.value('nomenclature_id'))
                if oldNomenclatureId != nomenclatureId:
                    unitId = self.getDefaultStockUnitId(nomenclatureId)
                    item.setValue('unit_id', toVariant(unitId))
                    if self.updateBatchShelfTimeFinance:
                        batch, shelfTime, financeId, medicalAidKind, price = getBatchShelfTimeFinance(forceRef(value))
                        result = CInDocTableModel.setData(self, index, value, role)
                        item.setValue('shelfTime', toVariant(shelfTime))
                    self.emitRowChanged(row)
            return result
        elif col == self.getColIndex('unit_id'):
            if not (0 <= row < len(self._items)):
                return False
            result = CInDocTableModel.setData(self, index, value, role)
            return result
        else:
            return CInDocTableModel.setData(self, index, value, role)


    def createEditor(self, index, parent):
        editor = CInDocTableModel.createEditor(self, index, parent)
        column = index.column()
        if column == self.getColIndex('nomenclature_id'):
            filterSetter = getattr(editor, 'setOrgStructureId', None)
            if not filterSetter:
                return editor
            if not editor._stockOrgStructureId:
                filterSetter(getattr(self, '_supplierId', None))

            editor.getFilterData()
            editor.setFilter(editor._filter)
            editor.reloadData()
        elif column == self.getColIndex('unit_id'):
            self._setUnitEditorFilter(index.row(), editor)
        return editor


    def _setUnitEditorFilter(self, row, editor):
        if 0 <= row < len(self._items):
            item = self._items[row]
            nomenclatureId = forceRef(item.value('nomenclature_id'))
            if not nomenclatureId:
                return
            editor.setFilter(self._getNomenclatureUnitFilter(nomenclatureId))


    @staticmethod
    def _getNomenclatureUnitFilter(nomenclatureId):
        if not nomenclatureId:
            return None
        result = set()
        records = QtGui.qApp.db.getRecordList('rbNomenclature_UnitRatio', where='master_id=%d AND deleted=0' % nomenclatureId)
        for record in records:
            targetUnitId = forceRef(record.value('targetUnit_id'))
            sourceUnitId = forceRef(record.value('sourceUnit_id'))
            if targetUnitId:
                result.add(targetUnitId)
            if sourceUnitId:
                result.add(sourceUnitId)
        return QtGui.qApp.db.table('rbUnit')['id'].inlist(result)


    def cellReadOnly(self, index):
        row = index.row()
        if 0 <= row < len(self._items):
            column = index.column()
            if column == self.getColIndex('unit_id'):
                item = self._items[row]
                nomenclatureId = forceRef(item.value('nomenclature_id'))
                stockUnitId = self.getDefaultStockUnitId(nomenclatureId)
                return not bool(stockUnitId)

        return False


    def getDefaultStockUnitId(self, nomenclatureId):
        return self._getNomenclatureDefaultUnits(nomenclatureId).get('defaultStockUnitId')


    def getDefaultClientUnitId(self, nomenclatureId):
        return self._getNomenclatureDefaultUnits(nomenclatureId).get('defaultClientUnitId')


    def _getNomenclatureDefaultUnits(self, nomenclatureId):
        if not nomenclatureId:
            return {}
        if nomenclatureId not in self._getCache():
            record = QtGui.qApp.db.getRecord(
                'rbNomenclature', 'defaultStockUnit_id, defaultClientUnit_id', nomenclatureId
            )
            if record:
                defaultStockUnitId = forceRef(record.value('defaultStockUnit_id'))
                defaultClientUnitId = forceRef(record.value('defaultClientUnit_id'))
            else:
                defaultStockUnitId = defaultClientUnitId = None
            self._getCache()[nomenclatureId] = {
                'defaultStockUnitId': defaultStockUnitId,
                'defaultClientUnitId': defaultClientUnitId
            }
        return self._getCache()[nomenclatureId]


    def _getCache(self):
        if not hasattr(self, '_modelInfoCache'):
            self._modelInfoCache = {}
        return self._modelInfoCache
