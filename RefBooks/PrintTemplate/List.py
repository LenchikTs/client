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

import os
import codecs

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature, SIGNAL, Qt, QObject

from library.ClientRecordProperties import CRecordProperties
from library.InDocTable import CInDocTableModel, CRBInDocTableCol, CEnumInDocTableCol
from library.interchange import (getCheckBoxValue, getComboBoxValue, getLineEditValue, getTextEditValue,
                                 setCheckBoxValue, setComboBoxValue, setLineEditValue, setTextEditValue)
from library.ItemsListDialog import CItemsListDialog, CItemEditorDialog
from library.TableModel import CBoolCol, CEnumCol, CTextCol, CTableModel
from library.Utils import forceRef, forceString, forceStringEx
from library.SortFilterProxyTableModel import CSortFilterProxyTableModel

from Users.Rights import urAdmin, urDeletePrintTemplate

from Ui_RBPrintTemplateListDialog import Ui_RBPrintTemplateListDialog
from Ui_RBPrintTemplateEditor import Ui_PrintTemplateEditorDialog


class CRBPrintTemplate(CItemsListDialog, Ui_RBPrintTemplateListDialog):
    setupUi = Ui_RBPrintTemplateListDialog.setupUi
    retranslateUi = Ui_RBPrintTemplateListDialog.retranslateUi

    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Контекст',                    ['context'], 20),
            CTextCol(u'Код',                         ['code'], 12),
            CTextCol(u'Наименование',                ['name'],   40),
            CTextCol(u'Группа',                      ['groupName'],   40),
            CTextCol(u'Файл',                        ['fileName'], 25),
            CBoolCol(u'Для отображения в Мед.карте', ['inAmbCard'], 7),
            CEnumCol(u'Тип',                         ['type'], [u'HTML', u'Exaro', u'SVG', u'CSS'], 10)
            ], 'rbPrintTemplate', ['context', 'code', 'groupName', 'name', 'type', 'id'])
        self.setWindowTitleEx(u'Шаблоны печати')

        self.actDuplicate = QtGui.QAction(u'Дублировать', self)
        self.actDuplicate.setObjectName('actDuplicate')
        self.connect(self.actDuplicate, SIGNAL('triggered()'), self.duplicateCurrentRow)

        popupItems = [self.actDuplicate]
        if QtGui.qApp.userHasAnyRight([urAdmin, urDeletePrintTemplate]):
            self.actDelete = QtGui.QAction(u'Удалить', self)
            self.actDelete.setObjectName('actDelete')
            self.connect(self.actDelete, SIGNAL('triggered()'), self.markCurrentRowDeleted)
            popupItems.append(self.actDelete)

        self.actShowInfo = QtGui.QAction(u'Свойства записи', self)
        self.actShowInfo.setObjectName('actShowInfo')
        self.connect(self.actShowInfo, SIGNAL('triggered()'), self.showRecordProperties)
        popupItems.append(self.actShowInfo)

        self.tblItems.createPopupMenu(popupItems)


    def setup(self, cols, tableName, order, forSelect=False, filterClass=None):
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.forSelect = forSelect
        self.filterClass = filterClass
        self.props = {}
        self.order = order
        self.addModels('', CTableModel(self, cols))
        self.addModels('PrintTemplateSort', CSortFilterProxyTableModel(self, self.model))
        self.model = self.modelPrintTemplateSort.sourceModel()
        self.model.idFieldName = self.idFieldName
        self.model.setTable(tableName, recordCacheCapacity=QtGui.qApp.db.getCount(tableName, 'id'))
        self.setModels(self.tblItems, self.modelPrintTemplateSort, self.selectionModelPrintTemplateSort)
        self.btnSelect.setEnabled(self.forSelect)
        self.btnSelect.setVisible(self.forSelect)
        self.btnSelect.setDefault(self.forSelect)
        self.btnFilter.setEnabled(self.forSelect and bool(self.filterClass))
        self.btnFilter.setEnabled(bool(self.filterClass))
        self.btnFilter.setVisible(bool(self.filterClass))
        self.btnEdit.setDefault(not self.forSelect)
        self.tblItems.setFocus(Qt.OtherFocusReason)
        self.btnNew.setShortcut('F9')
        self.btnEdit.setShortcut('F4')
        self.btnPrint.setShortcut('F6')
        QObject.connect(
            self.tblItems.horizontalHeader(), SIGNAL('sectionClicked(int)'), self.setSort)


    def getItemEditor(self):
        return CPrintTemplateEditor(self)


    def duplicateCurrentRow(self):
        currRow = self.tblItems.currentRow()
        if currRow is not None and currRow >= 0:
            sortIndex = self.modelPrintTemplateSort.index(currRow, 0)
            if sortIndex.isValid():
                sortRow = self.modelPrintTemplateSort.mapToSource(sortIndex).row()
                if sortRow is not None and sortRow >= 0:
                    itemsIndex = self.tblItems.model().index(sortRow, 0)
                    if itemsIndex.isValid():
                        itemId = self.tblItems.itemId(itemsIndex)
                        if itemId:
                            newItemId = self.duplicateRecord(itemId)
                            self.renewListAndSetTo(newItemId, sortIndex.row()+1)


    def markCurrentRowDeleted(self):
        currRow = self.tblItems.currentRow()
        if currRow is not None and currRow >= 0:
            sortIndex = self.modelPrintTemplateSort.index(currRow, 0)
            if sortIndex.isValid():
                sortRow = self.modelPrintTemplateSort.mapToSource(sortIndex).row()
                if sortRow is not None and sortRow >= 0:
                    itemsIndex = self.tblItems.model().index(sortRow, 0)
                    if itemsIndex.isValid():
                        itemId = self.tblItems.itemId(itemsIndex)
                        if itemId:
                            db = QtGui.qApp.db
                            table = db.table('rbPrintTemplate')
                            db.markRecordsDeleted(table, table['id'].eq(itemId))
                            self.renewListAndSetTo(None, sortIndex.row())


    def renewListAndSetTo(self, itemId=None, index=-1):
        idList = self.select(self.props)
        self.tblItems.setIdList(idList, itemId)
        self.label.setText(u'всего: %d' % len(idList))
        if index == -1 and itemId:
            index = self.tblItems.model().findItemIdIndex(itemId)
        if index >= 0:
            self.tblItems.selectRow(index)


    def showRecordProperties(self):
        idRecord = self.tblItems.currentItemId()
        CRecordProperties(self, 'rbPrintTemplate', idRecord).exec_()


    @pyqtSignature('QString')
    def on_edtCodeFilter_textChanged(self, text):
        if text.isEmpty():
            self.modelPrintTemplateSort.removeFilter('code')
        else:
            self.modelPrintTemplateSort.setFilter('code', text, CSortFilterProxyTableModel.MatchContains)


    @pyqtSignature('QString')
    def on_edtNameFilter_textChanged(self, text):
        if text.isEmpty():
            self.modelPrintTemplateSort.removeFilter('name')
        else:
            self.modelPrintTemplateSort.setFilter('name', text, CSortFilterProxyTableModel.MatchContains)


    @pyqtSignature('QString')
    def on_edtContextFilter_textChanged(self, text):
        if text.isEmpty():
            self.modelPrintTemplateSort.removeFilter('context')
        else:
            self.modelPrintTemplateSort.setFilter('context', text, CSortFilterProxyTableModel.MatchContains)


    @pyqtSignature('')
    def on_btnEdit_clicked(self):
        currRow = self.tblItems.currentRow()
        if currRow is not None and currRow >= 0:
            sortIndex = self.modelPrintTemplateSort.index(currRow, 0)
            if sortIndex.isValid():
                sortRow = self.modelPrintTemplateSort.mapToSource(sortIndex).row()
                if sortRow is not None and sortRow >= 0:
                    itemsIndex = self.tblItems.model().index(sortRow, 0)
                    if itemsIndex.isValid():
                        itemId = self.tblItems.itemId(itemsIndex)
                        if itemId:
                            dialog = self.getItemEditor()
                            try:
                                dialog.load(itemId)
                                if dialog.exec_():
                                    itemId = dialog.itemId()
                                    self.renewListAndSetTo(itemId, sortIndex.row())
                            finally:
                                dialog.deleteLater()
                        else:
                            self.on_btnNew_clicked()
        else:
            self.on_btnNew_clicked()


class CPrintTemplateEditor(Ui_PrintTemplateEditorDialog, CItemEditorDialog):
    def __init__(self,  parent):
        CItemEditorDialog.__init__(self, parent, 'rbPrintTemplate')
        self.setWindowTitleEx(u'Шаблон печати')
        self.exaroEditor = forceString(QtGui.qApp.preferences.appPrefs.get('exaroEditor', ''))
        self.addModels('ClientConsents', CClientConsentInDocTable(self))
        self.setModels(self.tblClientConsents, self.modelClientConsents, self.selectionModelClientConsents)
        self.tblClientConsents.addPopupDelRow()


    def setRecord(self, record):
        CItemEditorDialog.setRecord(self, record)
        setLineEditValue(self.edtContext, record, 'context')
        setLineEditValue(self.edtGroupName, record, 'groupName')
        setLineEditValue(self.edtFileName, record, 'fileName')
        setTextEditValue(self.edtDefault, record, 'default')
        setCheckBoxValue(self.chkInAmbCard, record, 'inAmbCard')
        setCheckBoxValue(self.chkPrintBlank, record, 'printBlank')
        setComboBoxValue(self.cmbType, record, 'type')
        self.modelClientConsents.loadItems(self.itemId())
#        self.setIsDirty(False)


    def getRecord(self):
        record = CItemEditorDialog.getRecord(self)
        getLineEditValue(self.edtContext, record, 'context')
        getLineEditValue(self.edtGroupName, record, 'groupName')
        getLineEditValue(self.edtFileName, record, 'fileName')
        getTextEditValue(self.edtDefault, record, 'default')
        getCheckBoxValue(self.chkInAmbCard, record, 'inAmbCard')
        getCheckBoxValue(self.chkPrintBlank, record, 'printBlank')
        getComboBoxValue(self.cmbType, record, 'type')
        return record


    def saveInternals(self, _id):
        self.modelClientConsents.saveItems(_id)


    def checkDataEntered(self):
        result = CItemEditorDialog.checkDataEntered(self)
        result = result and (forceStringEx(self.edtContext.text()) or self.checkInputMessage(u'контекст', False, self.edtContext))
        result = result and self.checkClientConsentTypeValues()
        return result


    def checkClientConsentTypeValues(self):
        for row, item in enumerate(self.modelClientConsents.items()):
            clientConsentTypeId = forceRef(item.value('clientConsentType_id'))
            if not clientConsentTypeId:
                return self.checkInputMessage(u'тип согласия пациента', False, self.tblClientConsents, row, self.modelClientConsents.clientConsentTypeColumn)
        return True


    @pyqtSignature('int')
    def on_cmbType_currentIndexChanged(self, index):
        self.btnEdit.setEnabled((index == 1) and (self.exaroEditor != ''))


    @pyqtSignature('')
    def on_btnEdit_clicked(self):
        fileName = forceString(self.edtFileName.text())
        tmpDir = None
        try:
            if not fileName:
                tmpDir = QtGui.qApp.getTmpDir('edit')
                fullPath = os.path.join(tmpDir, 'template.bdrt')
                txt = self.edtDefault.toPlainText()
                _file = codecs.open(unicode(fullPath), encoding='utf-8', mode='w+')
                _file.write(unicode(txt))
                _file.close()
            else:
                fullPath = os.path.join(QtGui.qApp.getTemplateDir(), fileName)

            cmdLine = u'"%s" "%s"' % (self.exaroEditor, fullPath)
            started, error, exitCode = QtGui.qApp.execProgram(cmdLine)
            if started:
                if not fileName:
                    for enc in ('utf-8', 'cp1251'):
                        try:
                            _file = codecs.open(fullPath, encoding=enc, mode='r')
                            txt = _file.read()
                            _file.close()
                            self.edtDefault.setPlainText(txt)
                            return
                        except:
                            pass
                    QtGui.QMessageBox.critical(None,
                                               u'Внимание!',
                                               u'Не удалось загрузить "%s" после' % fullPath,
                                               QtGui.QMessageBox.Close)
            else:
                QtGui.QMessageBox.critical(None,
                                           u'Внимание!',
                                           u'Не удалось запустить "%s"' % self.exaroEditor,
                                           QtGui.QMessageBox.Close)
        finally:
            if tmpDir:
                QtGui.qApp.removeTmpDir(tmpDir)


class CClientConsentInDocTable(CInDocTableModel):
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'rbPrintTemplate_ClientConsentType', 'id', 'master_id', parent)
        self.addCol(CRBInDocTableCol(u'Тип согласия', 'clientConsentType_id', 15, 'rbClientConsentType'))
        self.addCol(CEnumInDocTableCol(u'Значение', 'value', 10, [u'Нет', u'Да']))
        self.clientConsentTypeColumn = self.getColIndex('clientConsentType_id')
