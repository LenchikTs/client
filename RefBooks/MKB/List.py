# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2022 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

import re
from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QObject, QVariant, pyqtSignature, SIGNAL

from library.AgeSelector            import composeAgeSelector, parseAgeSelector
from library.ItemEditorDialogWithIdentification import CItemEditorDialogWithIdentification
from library.database               import decorateString
from library.DialogBase             import CDialogBase
from library.interchange            import getComboBoxValue, getLineEditValue, getRBComboBoxValue, getSpinBoxValue, getTextEditValue, setComboBoxValue, setLineEditValue, setRBComboBoxValue, setSpinBoxValue, setTextEditValue
from library.ItemsListDialog        import CItemEditorBaseDialog
from library.TableModel             import CTableModel, CDateCol, CEnumCol, CRefBookCol, CTextCol
from library.Utils                  import forceDate, forceInt, forceString, forceStringEx, forceRef, formatRecordsCount, toVariant
from library.InDocTable             import CInDocTableModel, CRBInDocTableCol

from RefBooks.Service.SelectService import selectService
from RefBooks.Tables                import rbService
from Reports.ReportBase             import CReportBase, createTable
from Reports.ReportView             import CReportViewDialog

from .Ui_MKBListDialog import Ui_ItemsListDialog
from .Ui_MKBEditor     import Ui_ItemEditorDialog

#1 острое
#2 хроническое впервые установленное
#3 хроническое известное
#4 обострение хронического

MapMKBCharactersToCharacterCode = [
    (u'нет', []),                                      #0
    (u'острое', ['1']),                                #1
    (u'хроническое впервые выявленное', ['2']),        #2
    (u'хроническое ранее известное', ['3']),           #3
    (u'обострение хронического', ['4']),               #4
    (u'хроническое', ['3', '2', '4']),                 #5 такой порядок - для выбора 3 "по умолчанию"
    (u'хроническое или острое', ['3', '1', '2', '4']), #6 idem
                                  ]

MKBCharacters = [ t[0] for t in MapMKBCharactersToCharacterCode ]

SexList = ['', u'М', u'Ж']
RequiresFillingDispanserList = [u'0-никогда', u'1-иногда', u'2-всегда']


class CMKBList(CDialogBase, Ui_ItemsListDialog):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)

        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setWindowTitleEx(u'Коды МКБ X')
        self.props = {}
        self.order = ['DiagID']
##        self.setWindowFlags(Qt.Dialog | Qt.WindowMaximizeButtonHint | Qt.WindowContextHelpButtonHint)

        cols = [
            CTextCol(u'Класс',                   ['ClassID'], 10),
            CTextCol(u'Блок',                    ['BlockID'], 30),
            CTextCol(u'Код',                     ['DiagID'],  10),
            CTextCol(u'Прим',                    ['Prim'],     3),
            CTextCol(u'Наименование',            ['DiagName'],40),
            CEnumCol(u'Характер',                ['characters'], MKBCharacters, 10),
            CDateCol(u'Дата окончания применения',  ['endDate'], 5),
            CEnumCol(u'Пол',                     ['sex'], SexList, 10),
            CTextCol(u'Возраст',                 ['age'], 10),
            CTextCol(u'Длительность',            ['duration'], 4),
            CRefBookCol(u'Субклассификация',     ['MKBSubclass_id'], 'rbMKBSubclass', 10),
            CRefBookCol(u'Базовая услуга',       ['service_id'], rbService, 30),
            CEnumCol(u'Требует заполнения ДН',   ['requiresFillingDispanser'], RequiresFillingDispanserList, 10),
            ]

        self.model = CTableModel(self, cols, 'MKB')
        self.tblItems.setModel(self.model)
        self.tblItems.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
#        self.createPopupMenu(self.tblItems)
        self.btnNew.setShortcut(Qt.Key_F9)
        self.btnEdit.setShortcut(Qt.Key_F4)
        self.btnPrint.setShortcut(Qt.Key_F6)

        QObject.connect(
            self.tblItems.horizontalHeader(), SIGNAL('sectionClicked(int)'), self.setSort)


    def exec_(self):
        self.renewListAndSetTo()
        return CDialogBase.exec_(self)


    def select(self, props):
        table = self.model.table()
        cond  = []
        codeStart=forceString(self.edtCode.text())
        if codeStart:
            cond.append(table['DiagID'].like(codeStart+'%'))
        namePart=forceString(self.edtName.text())
        if namePart:
            cond.append(table['DiagName'].contain(namePart))
        return QtGui.qApp.db.getIdList(table.name(), 'id', where=cond, order=self.order)


    def currentItemId(self):
        return self.tblItems.currentItemId()


    def setSort(self, col):
        name=self.model.cols()[col].fields()[0]
        self.order = name
        header=self.tblItems.horizontalHeader()
        header.setSortIndicatorShown(True)
        header.setSortIndicator(col, Qt.AscendingOrder)
        self.renewListAndSetTo()


    def renewListAndSetTo(self, itemId=None):
        if itemId is None:
            itemId = self.currentItemId()
        idList = self.select(self.props)
        try:
            i = idList.index(itemId)
        except:
            i = 0
#                idList.append(itemId)
#                i = len(idList)-1

        self.model.setIdList(idList)
        self.tblItems.setCurrentRow(max(0, i))
        self.label.setText(formatRecordsCount(len(idList)))


    def getItemEditor(self):
        return CMKBEditor(self)


    def updateFieldInSelectedRecord(self, fieldName, fieldValue):
        db = QtGui.qApp.db
        tableMKB = db.table('MKB')
        indexList = self.tblItems.selectedIndexes()
        rows = set()
        for index in indexList:
            rows.add(index.row())
        idList = self.model.idList()
        for row in rows:
            id = idList[row]
            record = db.getRecord(tableMKB, ['id', fieldName], id)
            if record:
                record.setValue(fieldName, fieldValue)
                db.updateRecord(tableMKB, record)
        self.model.invalidateRecordsCache()
        self.tblItems.clearSelection()


    @pyqtSignature('QModelIndex')
    def on_tblItems_doubleClicked(self, index):
        self.on_btnEdit_clicked()


    @pyqtSignature('')
    def on_btnCharacters_clicked(self):
        item, ok = QtGui.QInputDialog.getItem(self, u'Выбери', u'Характер', MKBCharacters, 0, False)
        item = forceString(item)
        if ok and item in MKBCharacters:
            self.updateFieldInSelectedRecord('characters', QVariant(MKBCharacters.index(item)))


    @pyqtSignature('')
    def on_btnSex_clicked(self):
        item, ok = QtGui.QInputDialog.getItem(self, u'Выбери', u'Пол', SexList, 0, False)
        item = forceString(item)
        if ok and item in SexList:
            self.updateFieldInSelectedRecord('sex', QVariant(SexList.index(item)))


    @pyqtSignature('')
    def on_btnEdit_clicked(self):
        itemId = self.currentItemId()
        if itemId:
            try:
                dialog = self.getItemEditor()
                dialog.load(itemId)
                if dialog.exec_():
                    itemId = dialog.itemId()
                    self.renewListAndSetTo(itemId)
            finally:
                dialog.deleteLater()


    @pyqtSignature('')
    def on_btnNew_clicked(self):
        dialog = self.getItemEditor()
        try:
            if dialog.exec_():
                itemId = dialog.itemId()
                self.renewListAndSetTo(itemId)
        finally:
            dialog.deleteLater()


    @pyqtSignature('')
    def on_btnPrint_clicked(self):
        tbl=self.tblItems
        tbl.setReportHeader(u'Коды МКБ X')
        txt=u''
        codeStart=forceString(self.edtCode.text())
        if codeStart:
            txt+=u'код начинается на "%s"\n' % codeStart
        namePart=forceString(self.edtName.text())
        if namePart:
            txt+=u'название диагноза содержит "%s"\n' % namePart
        tbl.setReportDescription(txt)
        tbl.printContent()


    @pyqtSignature('')
    def on_btnPrintSelected_clicked(self):
        tbl=self.tblItems

        model = tbl.model()

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Коды МКБ X\n')
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertText(tbl.reportDescription())
        cursor.insertBlock()

        cols = model.cols()
        colWidths  = [tbl.columnWidth(i) for i in xrange(len(cols))]
        colWidths.insert(0,10)
        totalWidth = sum(colWidths)
        tableColumns = []
        for iCol, colWidth in enumerate(colWidths):
            widthInPercents = str(max(1, colWidth*90/totalWidth))+'%'
            if iCol == 0:
                tableColumns.append((widthInPercents, [u'№'], CReportBase.AlignRight))
            else:
                col = cols[iCol-1]
                colAlingment = Qt.AlignHorizontal_Mask & forceInt(col.alignment())
                format = QtGui.QTextBlockFormat()
                format.setAlignment(Qt.AlignmentFlag(colAlingment))
                tableColumns.append((widthInPercents, [forceString(col.title())], format))

        table = createTable(cursor, tableColumns)
        for index in tbl.selectedIndexes():
            iModelRow=index.row()
            if index.column():
                continue
            iTableRow = table.addRow()
            table.setText(iTableRow, 0, iModelRow+1)
            for iModelCol in xrange(len(cols)):
                index = model.createIndex(iModelRow, iModelCol)
                text = forceString(model.data(index))
                table.setText(iTableRow, iModelCol+1, text)

        html=doc.toHtml('utf-8')
        view = CReportViewDialog(self)
        view.setText(html)
        view.exec_()


    @pyqtSignature('QString')
    def on_edtCode_textChanged(self, text):
        self.renewListAndSetTo()



    @pyqtSignature('QString')
    def on_edtName_textChanged(self, text):
        self.renewListAndSetTo()


#
# ##########################################################################
#

class CMKBEditor(Ui_ItemEditorDialog, CItemEditorDialogWithIdentification):
    def __init__(self,  parent):
        CItemEditorDialogWithIdentification.__init__(self, parent, 'MKB')
        self.addObject('modelExSubclass', CMKBExSubclassModel(self))
        # self.setupUi(self)
        self.edtEndDate.setDate(None)
        self.tblExSubclass.setModel(self.modelExSubclass)
        self.setWindowTitleEx(u'Код МКБ Х')
        self.cmbMKBSubclass.setTable('rbMKBSubclass', True)
        self.cmbService.setTable(rbService, True)
        self.cmbCharacters.addItems(MKBCharacters)
        self.cmbCharacters.setCurrentIndex(0)
        self.cmbSex.setCurrentIndex(0)
        self.cmblRequiresFillingDispanser.setCurrentIndex(0)
        self.setIsDirty(False)
        self.setupDirtyCather()
        self.prevCode = None


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtCode, record, 'DiagID')
        self.chkPrim.setChecked(bool(forceString(record.value('Prim'))))
        setTextEditValue(self.edtName, record, 'DiagName')
        setRBComboBoxValue(self.cmbMKBSubclass, record, 'MKBSubclass_id')
        setComboBoxValue(self.cmbCharacters, record, 'characters')
        self.edtEndDate.setDate(forceDate(record.value('endDate')))
        setComboBoxValue(self.cmbSex, record, 'sex')
        setComboBoxValue(self.cmblRequiresFillingDispanser, record, 'requiresFillingDispanser')
        (begUnit, begCount, endUnit, endCount) = parseAgeSelector(forceString(record.value('age')))
        self.cmbBegAgeUnit.setCurrentIndex(begUnit)
        self.edtBegAgeCount.setText(str(begCount))
        self.cmbEndAgeUnit.setCurrentIndex(endUnit)
        self.edtEndAgeCount.setText(str(endCount))
        setSpinBoxValue(self.edtDuration, record, 'duration')
#        code=forceString(record.value('DiagID'))
        setRBComboBoxValue(self.cmbService, record, 'service_id')
        self.prevCode = forceStringEx(self.edtCode.text())
        self.modelExSubclass.loadItems(self.itemId())
        self.modelIdentification.loadItems(self.itemId())
#


    def getRecord(self):
        db = QtGui.qApp.db
        baseCode = forceString(self.edtCode.text())[:3]
        cond = '''%s BETWEEN REPLACE(REPLACE(REPLACE(SUBSTRING_INDEX(BlockId,'-',1),'(',''),')',''),' ','') ''' \
                      '''AND REPLACE(REPLACE(REPLACE(SUBSTRING_INDEX(BlockId,'-',-1),'(',''),')',''),' ','')''' % decorateString(baseCode)
        protoRecord = db.getRecordEx('MKB', ('ClassID', 'ClassName', 'BlockID', 'BlockName'), cond)
        record = CItemEditorBaseDialog.getRecord(self)
        if protoRecord:
            for fieldName in ('ClassID', 'ClassName', 'BlockID', 'BlockName'):
                record.setValue(fieldName, protoRecord.value(fieldName))
        getLineEditValue(self.edtCode, record, 'DiagID')
        record.setValue('Prim', QVariant('*' if self.chkPrim.isChecked() else ''))
        getTextEditValue(self.edtName, record, 'DiagName')
        if self.cmbMKBSubclass.isEnabled():
            getRBComboBoxValue(self.cmbMKBSubclass, record, 'MKBSubclass_id')
        else:
            record.setValue('MKBSubclass_id', QVariant())
        getComboBoxValue(self.cmbCharacters, record, 'characters')
        record.setValue('endDate', toVariant(self.edtEndDate.date()))
        getComboBoxValue(self.cmbSex,        record, 'sex')
        getComboBoxValue(self.cmblRequiresFillingDispanser, record, 'requiresFillingDispanser')
        record.setValue('age',        toVariant(composeAgeSelector(
            self.cmbBegAgeUnit.currentIndex(),  forceStringEx(self.edtBegAgeCount.text()),
            self.cmbEndAgeUnit.currentIndex(),  forceStringEx(self.edtEndAgeCount.text())
                        )))
        getSpinBoxValue(self.edtDuration, record, 'duration')
        getRBComboBoxValue(self.cmbService, record, 'service_id')
        return record


    def checkDataEntered(self):
        result = True
        code = forceStringEx(self.edtCode.text())
        name = forceStringEx(self.edtName.toPlainText())
        result = result and (code or self.checkInputMessage(u'код', False, self.edtCode))
        result = result and (re.match(r'^[A-Z]\d{2}(\.\d)?$', code)  or self.checkInputMessage(u'код правильно', False, self.edtCode))
        result = result and (name or self.checkInputMessage(u'наименование', False, self.edtName))
        result = result and (not self.prevCode or self.prevCode == code or self.checkValueMessage(u'Код МКБ изменён. Предыдущее значение "%s"' % self.prevCode, True, self.edtCode))
        return result


    def saveInternals(self, id):
        self.modelExSubclass.saveItems(id)
        self.modelIdentification.saveItems(id)


    @pyqtSignature('')
    def on_btnSelectService_clicked(self):
        serviceId = selectService(self, self.cmbService)
        if serviceId:
            self.cmbService.setValue(serviceId)


    @pyqtSignature('QString')
    def on_edtCode_textChanged(self, text):
        code = forceStringEx(text)
        self.cmbMKBSubclass.setEnabled(bool(re.match(r'^[A-Z]\d{2}(\.\d)?$', code)))


class CMKBExSubclassModel(CInDocTableModel):
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'MKB_ExSubclass', 'id', 'master_id', parent)
        self.addCol(CRBInDocTableCol(u'Расширенная субклассификация', 'exSubclass_id', 10, 'rbMKBExSubclass'))
        self.initItems()


    def initItems(self):
        for i in range(0, 5):
            self._addEmptyItem()
        self.reset()


    def flags(self, index):
        if index.row() >= 5:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled
        return CInDocTableModel.flags(self, index)


    def setData(self, index, value, role=Qt.EditRole):
        row = index.row()
        if row >= 5:
            return False
        return CInDocTableModel.setData(self, index, value, role)


    def loadItems(self, masterId):
        db = QtGui.qApp.db
        table = self._table
        filter = [table[self._masterIdFieldName].eq(masterId)]
        if self._filter:
            filter.append(self._filter)
        if table.hasField('deleted'):
            filter.append(table['deleted'].eq(0))
        if self._idxFieldName:
            order = [self._idxFieldName, self._idFieldName]
        else:
            order = [self._idFieldName]
        cols = []
        for col in self._cols:
            if not col.external():
                cols.append(col.fieldName())
        cols.append(self._idFieldName)
        cols.append(self._masterIdFieldName)
        if self._idxFieldName:
            cols.append(self._idxFieldName)
        for col in self._hiddenCols:
            cols.append(col)
        records = db.getRecordList(table, cols, filter, order)
        for record in records:
            exSubclassId = forceRef(record.value('exSubclass_id'))
            if exSubclassId:
                position = forceInt(db.translate('rbMKBExSubclass', 'id', exSubclassId, 'position'))
                self._items[position-6] = record
        self.reset()


    def saveItems(self, masterId):
        if self._items is not None:
            db = QtGui.qApp.db
            table = self._table
            masterId = toVariant(masterId)
            masterIdFieldName = self._masterIdFieldName
            idFieldName = self._idFieldName
            idList = []
            for idx, record in enumerate(self._items):
                record.setValue(masterIdFieldName, masterId)
                if self._idxFieldName:
                    record.setValue(self._idxFieldName, toVariant(idx))
                if self._extColsPresent:
                    outRecord = self.removeExtCols(record)
                else:
                    outRecord = record
                if forceRef(record.value('exSubclass_id')):
                    id = db.insertOrUpdate(table, outRecord)
                    record.setValue(idFieldName, toVariant(id))
                    idList.append(id)
                    self.saveDependence(idx, id)

            filter = [table[masterIdFieldName].eq(masterId),
                      'NOT ('+table[idFieldName].inlist(idList)+')']
            if self._filter:
                filter.append(self._filter)
            db.deleteRecord(table, filter)
