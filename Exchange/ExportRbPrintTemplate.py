# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2023 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4              import QtGui
from PyQt4.QtCore       import Qt, QDir, QMetaObject, pyqtSignature, SIGNAL, QVariant
from library.Utils      import forceBool, forceString, forceInt, toVariant, getPref, setPref
from Exchange.Utils     import compressFileInZip
from library.DialogBase import CConstructHelperMixin
from library.TableView  import CTableView
from library.TableModel import CTableModel, CTextCol, CBoolCol, CEnumCol
from library.database   import decorateString

from xml.etree.ElementTree              import ElementTree, Element, SubElement
from Exchange.Ui_ExportEvents_Wizard_2  import Ui_ExportEvents_Wizard_2



def ExportRbPrintTemplate():
    prefs = QtGui.qApp.preferences
    fileName = forceString(getPref(prefs.appPrefs, 'ExportRbPrintTemplateFileName', ''))
    exportAll = forceBool(getPref(prefs.appPrefs, 'ExportRbPrintTemplateExportAll', False))
    compressRAR = forceBool(getPref(prefs.appPrefs, 'ExportRbPrintTemplateCompressRAR', False))
    tblItemsPrefs = getPref(prefs.appPrefs, 'ExportRbPrintTemplateTable', {})
    geometryPrefs = getPref(prefs.appPrefs, 'ExportRbPrintTemplateGeometry', QVariant()).toByteArray()
    orderItems = forceString(getPref(prefs.appPrefs, 'ExportRbPrintTemplateSortItems', 'context ASC'))
    orderSelectedItems = forceString(getPref(prefs.appPrefs, 'ExportRbPrintTemplateSortSelectedItems', 'context ASC'))
    splitterState = getPref(prefs.appPrefs, 'ExportRbPrintTemplateSplitterState', QVariant()).toByteArray()

    dlg = CExportRbPrintTemplate(fileName, exportAll, compressRAR, orderItems, orderSelectedItems)
    if geometryPrefs:
        dlg.restoreGeometry(geometryPrefs)
    page = dlg.page(0)
    tblItems = page.tblItems
    tblItems.loadPreferences(tblItemsPrefs)
    page.splitter.restoreState(splitterState)
    dlg.exec_()

    setPref(prefs.appPrefs, 'ExportRbPrintTemplateFileName', toVariant(dlg.fileName))
    setPref(prefs.appPrefs, 'ExportRbPrintTemplateExportAll', toVariant(dlg.exportAll))
    setPref(prefs.appPrefs, 'ExportRbPrintTemplateCompressRAR', toVariant(dlg.compressRAR))
    setPref(prefs.appPrefs, 'ExportRbPrintTemplateTable', page.tblItems.savePreferences())
    setPref(prefs.appPrefs, 'ExportRbPrintTemplateGeometry', QVariant(dlg.saveGeometry()))
    setPref(prefs.appPrefs, 'ExportRbPrintTemplateSortItems', toVariant(page.orderItems))
    setPref(prefs.appPrefs, 'ExportRbPrintTemplateSortSelectedItems', toVariant(page.orderSelectedItems))
    setPref(prefs.appPrefs, 'ExportRbPrintTemplateSplitterState', toVariant(page.splitter.saveState()))


class CExportRbPrintTemplate(QtGui.QWizard):
    def __init__(self, fileName, exportAll, compressRAR, orderItems, orderSelectedItems):
        QtGui.QWizard.__init__(self, None, Qt.Dialog)
        self.setWizardStyle(QtGui.QWizard.ClassicStyle)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle(u'Экспорт шаблонов печати')
        self.selectedItemIdList = []
        self.fileName = fileName
        self.exportAll = exportAll
        self.compressRAR = compressRAR
        self.addPage(CExportWizardPage1(self, orderItems, orderSelectedItems))
        self.addPage(CExportWizardPage2(self))


class CExportWizardPage1(QtGui.QWizardPage, CConstructHelperMixin):
    def __init__(self, parent, orderItems, orderSelectedItems):
        QtGui.QWizardPage.__init__(self, parent)
        self.cols = [
            CTextCol(u'Контекст', ['context'], 40),
            CTextCol(u'Код', ['code'], 20),
            CTextCol(u'Наименование', ['name'], 40),
            CTextCol(u'Группа', ['groupName'], 40),
            CBoolCol(u'Для отображения в мед.карте', ['inAmbCard'], 20),
            CEnumCol(u'Тип', ['type'], ('HTML', 'Exaro', 'SVG'), 20),
        ]
        self._wizard = parent
        self.tableName = 'rbPrintTemplate'
        self.orderItems = orderItems
        self.orderSelectedItems = orderSelectedItems
        self.preSetupUi()
        self.setupUi(self)
        self.postSetupUi()
        self.tblItems.horizontalHeader().setSortIndicatorShown(False)
        self.tblSelectedItems.horizontalHeader().setSortIndicatorShown(False)
        self.setTitle(u'Параметры экспорта')
        self.setSubTitle(u'Выбор записей для экспорта')


    @staticmethod
    def setupUi(dialog):
        dialog.setWindowTitle(u'Список записей')
        dialog.setObjectName(u'ExportEvents_Wizard_1')

        dialog.tblItems = CTableView(dialog)
        dialog.tblItems.setObjectName(u'tblItems')
        dialog.tblSelectedItems = CTableView(dialog)
        dialog.tblSelectedItems.setObjectName(u'tblSelectedItems')
        dialog.checkExportAll = QtGui.QCheckBox(u'Выгружать все')
        dialog.checkExportAll.setObjectName(u'checkExportAll')
        dialog.btnClearSelection = QtGui.QPushButton(u'Очистить')
        dialog.btnClearSelection.setObjectName(u'btnClearSelection')
        dialog.statusLabel = QtGui.QLabel(u'Выбрано 0 элементов для экспорта')
        dialog.edtContext = QtGui.QLineEdit()
        dialog.edtContext.setObjectName(u'edtContext')
        dialog.edtCode = QtGui.QLineEdit()
        dialog.edtCode.setObjectName(u'edtCode')
        dialog.edtName = QtGui.QLineEdit()
        dialog.edtName.setObjectName(u'edtName')

        dialog.splitter = QtGui.QSplitter(Qt.Horizontal, dialog)
        dialog.splitter.addWidget(dialog.tblItems)
        dialog.splitter.addWidget(dialog.tblSelectedItems)
        dialog.splitter.setChildrenCollapsible(False)
        dialog.splitter.setSizePolicy(
            QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding))

        layout1 = QtGui.QHBoxLayout()
        layout1.addWidget(QtGui.QLabel(u'Контекст'))
        layout1.addWidget(dialog.edtContext)
        layout1.addWidget(QtGui.QLabel(u'Код'))
        layout1.addWidget(dialog.edtCode)
        layout1.addWidget(QtGui.QLabel(u'Наименование'))
        layout1.addWidget(dialog.edtName)

        layout2 = QtGui.QHBoxLayout()
        layout2.addWidget(dialog.checkExportAll)
        layout2.addStretch()

        layout3 = QtGui.QHBoxLayout()
        layout3.addStretch()
        layout3.addWidget(dialog.btnClearSelection)

        layout = QtGui.QVBoxLayout(dialog)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addWidget(dialog.splitter)
        layout.addLayout(layout3)
        layout.addWidget(dialog.statusLabel)

        QMetaObject.connectSlotsByName(dialog)


    def isComplete(self):
        return self._wizard.exportAll or len(self._wizard.selectedItemIdList) > 0


    def preSetupUi(self):
        self.addModels('Items', CTableModel(self, self.cols, self.tableName))
        self.addModels('SelectedItems', CTableModel(self, self.cols, self.tableName))


    def postSetupUi(self):
        self.setModels(self.tblItems, self.modelItems, self.selectionModelItems)
        self.setModels(self.tblSelectedItems, self.modelSelectedItems, self.selectionModelSelectedItems)
        self.syncTables()
        self.selectionModelSelectedItems.clearSelection()
        self.tblItems.setFocus(Qt.OtherFocusReason)
        self.tblItems.setEnabled(not self._wizard.exportAll)
        self.tblSelectedItems.setEnabled(not self._wizard.exportAll)
        self.btnClearSelection.setEnabled(not self._wizard.exportAll)
        self.checkExportAll.setChecked(self._wizard.exportAll)
        self.tblItems.setSortingEnabled(True)
        self.tblItems.horizontalHeader().sectionClicked.connect(self.setItemsSort)
        self.tblSelectedItems.setSortingEnabled(True)
        self.tblSelectedItems.horizontalHeader().sectionClicked.connect(self.setSelectedItemsSort)


    def setItemsSort(self, col):
        self.tblItems.horizontalHeader().setSortIndicatorShown(True)
        self.orderItems = self.getOrder(self.tblItems, self.modelItems, col)
        self.tblItems.setIdList(self.select(onlyNotSelected=True))


    def setSelectedItemsSort(self, col):
        self.tblSelectedItems.horizontalHeader().setSortIndicatorShown(True)
        self.orderSelectedItems = self.getOrder(self.tblSelectedItems, self.modelSelectedItems, col)
        self.tblSelectedItems.setIdList(self.select(onlySelected=True))


    def getOrder(self, table, model, col):
        order = ','.join(self.cols[col].fields())
        if table.horizontalHeader().sortIndicatorOrder() == Qt.DescendingOrder:
            order += ' DESC'
        else:
            order += ' ASC'
        return order


    def select(self, onlySelected=False, onlyNotSelected=False):
        db = QtGui.qApp.db
        table = db.table(self.tableName)
        cond = [
            table['deleted'].eq(0),
        ]
        if onlySelected:
            cond.append(table['id'].inlist(self._wizard.selectedItemIdList))
        elif onlyNotSelected:
            cond.append(table['id'].notInlist(self._wizard.selectedItemIdList))
            context = forceString(self.edtContext.text())
            code = forceString(self.edtCode.text())
            name = forceString(self.edtName.text())
            if context:
                cond.append('LOCATE(%s, %s) > 0' % (decorateString(context), table['context'].name()))
            if code:
                cond.append('LOCATE(%s, %s) > 0' % (decorateString(code), table['code'].name()))
            if name:
                cond.append('LOCATE(%s, %s) > 0' % (decorateString(name), table['name'].name()))
        else:
            cond.append('FALSE')
        order = self.orderItems if onlyNotSelected else self.orderSelectedItems
        return db.getIdList(table, 'id', cond, order)


    def syncTables(self):
        self.modelItems.setIdList(self.select(onlyNotSelected=True))
        self.modelSelectedItems.setIdList(self.select(onlySelected=True))


    @pyqtSignature('QModelIndex')
    def on_tblItems_doubleClicked(self, index):
        if not index.isValid():
            return
        row = index.row()
        itemId = self.modelItems.idList()[row]
        self._wizard.selectedItemIdList.append(itemId)
        self.syncTables()
        self.statusLabel.setText(u'Выбрано %d элементов для экспорта' % len(self._wizard.selectedItemIdList))
        self.emit(SIGNAL('completeChanged()'))


    @pyqtSignature('QModelIndex')
    def on_tblSelectedItems_doubleClicked(self, index):
        if not index.isValid():
            return
        row = index.row()
        itemId = self.modelSelectedItems.idList()[row]
        self._wizard.selectedItemIdList.remove(itemId)
        self.syncTables()
        self.statusLabel.setText(u'Выбрано %d элементов для экспорта' % len(self._wizard.selectedItemIdList))
        self.emit(SIGNAL('completeChanged()'))


    @pyqtSignature('')
    def on_btnClearSelection_clicked(self):
        self._wizard.selectedItemIdList = []
        self.tblItems.clearSelection()
        self.tblSelectedItems.clearSelection()
        self.syncTables()
        self.emit(SIGNAL('completeChanged()'))


    @pyqtSignature('bool')
    def on_checkExportAll_toggled(self, checked):
        self._wizard.exportAll = checked
        self.tblItems.clearSelection()
        self.tblItems.setEnabled(not checked)
        self.tblSelectedItems.clearSelection()
        self.tblSelectedItems.setEnabled(not checked)
        self.btnClearSelection.setEnabled(not checked)
        self._wizard.selectedItemIdList = []
        self.syncTables()
        if checked:
            self.statusLabel.setText(u'Выбраны все элементы для экспорта')
        else:
            self.statusLabel.setText(u'Выбрано 0 элементов для экспорта')
        self.emit(SIGNAL('completeChanged()'))


    @pyqtSignature('QString')
    def on_edtContext_textChanged(self, text):
        self.tblItems.setIdList(self.select(onlyNotSelected=True))


    @pyqtSignature('QString')
    def on_edtCode_textChanged(self, text):
        self.tblItems.setIdList(self.select(onlyNotSelected=True))


    @pyqtSignature('QString')
    def on_edtName_textChanged(self, text):
        self.tblItems.setIdList(self.select(onlyNotSelected=True))



class CExportWizardPage2(QtGui.QWizardPage, Ui_ExportEvents_Wizard_2):
    def __init__(self, parent):
        QtGui.QWizardPage.__init__(self, parent)
        self.setupUi(self)
        self.checkRAR.setText(u'Архивировать zip')
        self._wizard = parent
        self.setTitle(u'Параметры сохранения')
        self.setSubTitle(u'Выбор места для сохранения')
        self.progressBar.setFormat('%p%')
        self.progressBar.setValue(0)
        self.edtFileName.setText(self._wizard.fileName)
        self.btnExport.setEnabled(self._wizard.fileName != '')
        self.checkRAR.setChecked(self._wizard.compressRAR)
        self.done = False


    def isComplete(self):
        return self.done


    @pyqtSignature('')
    def on_btnSelectFile_clicked(self):
        fileName = QtGui.QFileDialog.getSaveFileName(
            self, u'Укажите файл с данными', self.edtFileName.text(), u'Файлы XML (*.xml)')
        if fileName != '':
            fileName = QDir.toNativeSeparators(fileName)
            self.edtFileName.setText(fileName)
            self._wizard.fileName = fileName
            self.btnExport.setEnabled(True)


    @pyqtSignature('')
    def on_btnExport_clicked(self):
        assert self._wizard.exportAll or len(self._wizard.selectedItemIdList) > 0
        fileName = forceString(self.edtFileName.text())
        if not fileName:
            return

        db = QtGui.qApp.db
        table = db.table('rbPrintTemplate')
        cond = [
            table['deleted'].eq(0),
        ]
        if not self._wizard.exportAll and self._wizard.selectedItemIdList:
            cond.append(table['id'].inlist(self._wizard.selectedItemIdList))

        records = db.getRecordList('rbPrintTemplate', '*', cond)
        self.progressBar.setMaximum(len(records))
        xmlRoot = Element('items')
        for record in records:
            self.progressBar.setValue(self.progressBar.value() + 1)
            QtGui.qApp.processEvents()

            itemId = forceInt(record.value('id'))
            xmlItem = SubElement(xmlRoot, 'rbPrintTemplate', attrib={
                    'context': forceString(record.value('context')),
                    'name': forceString(record.value('name')),
                    'code': forceString(record.value('code')),
                    'groupName': forceString(record.value('groupName')),
                    'inAmbCard': forceString(record.value('inAmbCard')),
                    'type': forceString(record.value('type')),
                    'default': forceString(record.value('default')),
                    'fileName': forceString(record.value('fileName')),
                })

            consentTypes = db.getRecordList(
                'rbPrintTemplate_ClientConsentType',
                [
                'value',
                '(SELECT name FROM rbClientConsentType WHERE id = clientConsentType_id) AS name',
                '(SELECT code FROM rbClientConsentType WHERE id = clientConsentType_id) AS code',
                ],
                'master_id = %d' % itemId)
            for consentRecord in consentTypes:
                SubElement(xmlItem, 'rbClientConsentType', attrib={
                        'code': forceString(consentRecord.value('code')),
                        'name': forceString(consentRecord.value('name')),
                        'value': forceString(consentRecord.value('value')),
                    })

        try:
            with open(fileName, 'w') as file:
                ElementTree(xmlRoot).write(file, encoding='utf-8')
        except Exception as e:
            QtGui.QMessageBox.critical(None, u'Ошибка', u'Ошибка записи файла:\n' + unicode(e))
            return

        if self.checkRAR.isChecked():
            self.progressBar.setText(u'Сжатие')
            compressFileInZip(fileName, fileName+'.zip')
            self.progressBar.setText(u'Сжато в "%s"' % (fileName+'.zip'))

        self.done = True
        self.btnExport.setEnabled(False)
        self._wizard.setButtonLayout([QtGui.QWizard.FinishButton])
        self.emit(SIGNAL('completeChanged()'))


    @pyqtSignature('bool')
    def on_checkRAR_toggled(self, checked):
        self._wizard.compressRAR = checked
