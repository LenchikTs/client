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

import xml.etree.ElementTree as ET

from PyQt4          import QtGui
from PyQt4.QtCore   import Qt, QVariant, pyqtSignature, SIGNAL
from library.Utils  import forceInt, forceString, toVariant, getPref, setPref

from Exchange.Ui_ImportRbResult_Wizard_1 import Ui_ImportRbResult_Wizard_1
from Exchange.Ui_ImportRbResult_Wizard_2 import Ui_ImportRbResult_Wizard_2
from Exchange.Ui_ImportRbResult_Wizard_3 import Ui_ImportRbResult_Wizard_3


def ImportRbPrintTemplate(parent=None):
    prefs = QtGui.qApp.preferences.windowPrefs
    fileName = forceString(getPref(prefs, 'ImportRbPrintTemplateFileName', ''))
    geomerty = getPref(prefs, 'ImportRbPrintTemplateGeometry', QVariant()).toByteArray()
    state = getPref(prefs, 'ImportRbPrintTemplateHeaderState', QVariant()).toByteArray()

    dlg = CImportRbPrintTemplate(parent, fileName, state)
    dlg.restoreGeometry(geomerty)
    dlg.exec_()

    setPref(prefs, 'ImportRbPrintTemplateFileName', toVariant(dlg.fileName))
    setPref(prefs, 'ImportRbPrintTemplateHeaderState',
        toVariant(dlg.page2.tblEvents.horizontalHeader().saveState()))
    setPref(prefs, 'ImportRbPrintTemplateGeometry', toVariant(dlg.saveGeometry()))


class CImportRbPrintTemplate(QtGui.QWizard):
    def __init__(self, parent, fileName, tblHeaderState):
        QtGui.QWizard.__init__(self, parent, Qt.Dialog)
        self.setWizardStyle(QtGui.QWizard.ModernStyle)
        self.setWindowTitle(u'Импорт шаблонов печати')
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.selectedItems = []
        self.fileName = fileName
        self.duplicatesResolveMethod = 0  # 0-спросить, 1-обновить, 2-пропустить

        self.page2 = CImportRbPrintTemplate_Page2(self)
        self.page2.tblEvents.horizontalHeader().restoreState(tblHeaderState)

        self.addPage(CImportRbPrintTemplate_Page1(self))
        self.addPage(self.page2)
        self.addPage(CImportRbPrintTemplate_Page3(self))


class CImportRbPrintTemplate_Page1(QtGui.QWizardPage, Ui_ImportRbResult_Wizard_1):
    def __init__(self, parent):
        QtGui.QWizardPage.__init__(self, parent)
        self._wizard = parent
        self.setupUi(self)
        self.chkFullLog.setVisible(False)
        self.progressBar.setVisible(False)
        self.statusLabel.setVisible(False)
        self.logBrowser.setVisible(False)
        self.edtFileName.setText(parent.fileName)


    def isComplete(self):
        return len(self.edtFileName.text()) > 0


    @pyqtSignature('bool')
    def on_btnSelectFile_clicked(self, checked=False):
        fileName = QtGui.QFileDialog.getOpenFileName(
            self, u'Укажите файл с данными', self.edtFileName.text(), u'Файлы XML (*.xml)')
        if fileName:
            self.edtFileName.setText(fileName)


    @pyqtSignature('QString')
    def on_edtFileName_textChanged(self, text):
        self.emit(SIGNAL('completeChanged()'))
        self._wizard.fileName = forceString(self.edtFileName.text())


    @pyqtSignature('bool')
    def on_rbAskUser_clicked(self, checked=False):
        self._wizard.duplicatesResolveMethod = 0  # спросить


    @pyqtSignature('bool')
    def on_rbUpdate_clicked(self, checked=False):
        self._wizard.duplicatesResolveMethod = 1  # обновить


    @pyqtSignature('bool')
    def on_rbSkip_clicked(self, checked=False):
        self._wizard.duplicatesResolveMethod = 2  # пропустить



class CImportRbPrintTemplate_Page2(QtGui.QWizardPage, Ui_ImportRbResult_Wizard_2):
    def __init__(self, parent):
        QtGui.QWizardPage.__init__(self, parent)
        self._wizard = parent
        self.setupUi(self)
        self.items = []
        self.tblEvents.setColumnCount(3)
        self.tblEvents.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.tblEvents.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblEvents.setHorizontalHeaderLabels((u'Код', u'Наименование', u'Контекст'))
        self.tblEvents.horizontalHeader().setStretchLastSection(True)
        self.tblEvents.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.tblEvents.verticalHeader().hide()
        self.tblEvents.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.statusLabel.setText(u'Выбрано 0 элементов для импорта')


    def initializePage(self):
        self.items = readItems(self._wizard.fileName)
        self.tblEvents.setRowCount(len(self.items))
        for i, item in enumerate(self.items):
            self.tblEvents.setItem(i, 0, QtGui.QTableWidgetItem(item[0]['code']))
            self.tblEvents.setItem(i, 1, QtGui.QTableWidgetItem(item[0]['name']))
            self.tblEvents.setItem(i, 2, QtGui.QTableWidgetItem(item[0]['context']))


    def isComplete(self):
        return len(self._wizard.selectedItems) > 0


    @pyqtSignature('bool')
    def on_chkImportAll_toggled(self, checked):
        self.tblEvents.setEnabled(not checked)
        self.btnClearSelection.setEnabled(not checked)
        self.tblEvents.clearSelection()
        if checked:
            self.statusLabel.setText(u'Выбраны все элементы для импорта')
            self._wizard.selectedItems = self.items
        else:
            self.statusLabel.setText(u'Выбрано 0 элементов для импорта')
            self._wizard.selectedItems = []
        self.emit(SIGNAL('completeChanged()'))


    @pyqtSignature('bool')
    def on_btnClearSelection_clicked(self, checked=False):
        self.tblEvents.clearSelection()


    @pyqtSignature('')
    def on_tblEvents_itemSelectionChanged(self):
        rows = list(set([index.row() for index in self.tblEvents.selectedIndexes()]))
        self._wizard.selectedItems = [self.items[i] for i in rows]

        self.statusLabel.setText(u'Выбрано %d элементов для импорта' % \
                                        len(self._wizard.selectedItems))
        self.emit(SIGNAL('completeChanged()'))


class CImportRbPrintTemplate_Page3(QtGui.QWizardPage, Ui_ImportRbResult_Wizard_3):
    def __init__(self, parent):
        QtGui.QWizardPage.__init__(self, parent)
        self._wizard = parent
        self.setupUi(self)
        self.aborted = False
        self.done = False
        self.progressBar.reset()
        self.btnAbort.setEnabled(False)
        self.statusLabel.setVisible(False)
        self.connect(self, SIGNAL('import()'), self.import_, Qt.QueuedConnection)
        self.connect(parent, SIGNAL('rejected()'), self.on_btnAbort_clicked)


    def initializePage(self):
        self.emit(SIGNAL('import()'))


    def isComplete(self):
        return self.done


    def import_(self):
        self.progressBar.reset()
        self.progressBar.setMaximum(len(self._wizard.selectedItems))
        self.progressBar.setValue(0)
        self.btnAbort.setEnabled(True)

        self._wizard.setButtonLayout([QtGui.QWizard.FinishButton])
        db = QtGui.qApp.db
        db.transaction()
        try:
            self.importItems(self._wizard.selectedItems)
        except Exception as e:
            db.rollback()
            QtGui.QMessageBox.critical(self, u'Ошибка импорта', unicode(e))
            self.btnAbort.setEnabled(False)
            raise
        else:
            db.commit()
            self.btnAbort.setEnabled(False)
        self.done = True
        self.emit(SIGNAL('completeChanged()'))


    @pyqtSignature('bool')
    def on_btnAbort_clicked(self, checked=False):
        self.aborted = True


    def importItems(self, items):
        db = QtGui.qApp.db
        tableRbPrintTemplate = db.table('rbPrintTemplate')
        tableRbPrintTemplateConsent = db.table('rbPrintTemplate_ClientConsentType')
        tableRbClientConsent = db.table('rbClientConsentType')

        for printTemplate, consentList in items:
            if self.aborted:
                raise Exception(u'Прервано пользователем')
            record = db.getRecordEx(tableRbPrintTemplate, '*', [
                    tableRbPrintTemplate['deleted'].eq(0),
                    tableRbPrintTemplate['code'].eq(printTemplate['code']),
                    tableRbPrintTemplate['name'].eq(printTemplate['name']),
                    tableRbPrintTemplate['context'].eq(printTemplate['context']),
                ])
            isExists = record is not None
            itemId = forceInt(record.value('id')) if isExists else None

            record = tableRbPrintTemplate.newRecord()
            record.setValue('code', printTemplate['code'])
            record.setValue('name', printTemplate['name'])
            record.setValue('context', printTemplate['context'])
            record.setValue('groupName', printTemplate['groupName'])
            record.setValue('inAmbCard', forceInt(printTemplate['inAmbCard']))
            record.setValue('type', forceInt(printTemplate['type']))
            record.setValue('default', forceString(printTemplate.get('default', '')))
            record.setValue('fileName', forceString(printTemplate.get('fileName', '')))
            if isExists:
                msg = u'код: %s, наименование: %s, контекст: %s' % (
                    printTemplate['code'],
                    printTemplate['name'],
                    printTemplate['context'],
                )
                method = getDuplicatesResolveMethod(self, self._wizard.duplicatesResolveMethod, msg)
                if method == 1:  # добавить
                    itemId = db.insertRecord(tableRbPrintTemplate, record)
                    self.logBrowser.append(u'Добавлена запись rbPrintTemplate.id = %d' % itemId)
                elif method == 2:  # обновить
                    record.setValue('id', itemId)
                    db.updateRecord(tableRbPrintTemplate, record)
                    self.logBrowser.append(u'Обновлена запись rbPrintTemplate.id = %d' % itemId)
                else:
                    self.logBrowser.append(u'Запись пропущена rbPrintTemplate.id = %d' % itemId)
                    self.progressBar.setValue(self.progressBar.value() + 1)
                    QtGui.qApp.processEvents()
                    continue
            else:
                itemId = db.insertRecord(tableRbPrintTemplate, record)
                self.logBrowser.append(u'Добавлена запись rbPrintTemplate.id = %d' % itemId)

            hasConsents = db.getCount(tableRbPrintTemplateConsent, where='master_id=%d'%itemId) > 0
            if hasConsents and len(consentList) > 0:
                db.query('DELETE FROM rbPrintTemplate_ClientConsentType WHERE master_id = %d' % itemId)

            for consent in consentList:
                if self.aborted:
                    raise Exception(u'Прервано пользователем')
                record = db.getRecordEx(tableRbClientConsent, '*', [
                        tableRbClientConsent['code'].eq(consent['code']),
                        tableRbClientConsent['name'].eq(consent['name']),
                    ])
                consentItemId = forceInt(record.value('id')) if record else None
                if consentItemId:
                    record = db.getRecordEx(tableRbPrintTemplateConsent, '*', [
                        'master_id = %d' % itemId,
                        'clientConsentType_id = %d' % consentItemId,
                    ])
                    if record is None:
                        record = tableRbPrintTemplateConsent.newRecord()
                        record.setValue('master_id', itemId)
                        record.setValue('clientConsentType_id', consentItemId)
                        record.setValue('value', consent['value'])
                        id = db.insertRecord(tableRbPrintTemplateConsent, record)
                        self.logBrowser.append(u'Добавлена запись rbPrintTemplate_ClientConsentType.id = %d' % id)

            self.progressBar.setValue(self.progressBar.value() + 1)
            QtGui.qApp.processEvents()



def hasAllAttributes(d, attrs):
    return all(a in d for a in attrs)

# 0-пропустить, 1-добавить, 2-обновить
def getDuplicatesResolveMethod(parent, duplicatesResolveMethod, msg):
    if duplicatesResolveMethod == 0:  # спросить у пользователя
        msgbox = QtGui.QMessageBox(parent)
        msgbox.setText(u'Обнаружено совпадение:\n' + msg)
        msgbox.addButton(u'Обновить', QtGui.QMessageBox.ActionRole)  # 0
        msgbox.addButton(u'Добавить', QtGui.QMessageBox.ActionRole)  # 1
        msgbox.addButton(u'Пропустить', QtGui.QMessageBox.ActionRole)# 2
        btn = msgbox.exec_()
        if btn == 0: # обновить
            return 2
        if btn == 1:  # добавить
            return 1
        return 0
    if duplicatesResolveMethod == 1:  # обновить
        return 2
    return 0


def readItems(fileName):
    tree = ET.parse(fileName)
    root = tree.getroot()
    items = []  # list[(rbPrintTemplate, list[rbClientConsent])]

    if root.tag != 'items':
        raise Exception(u'Неверный корневой элемент "%s"' % root.tag)
    for item in root:
        # if aborted:
        #     raise Exception(u'Прервано пользователем')
        if item.tag != 'rbPrintTemplate':
            raise Exception(u'Неожиданный элемент "%s"' % item.tag)
        if not hasAllAttributes(item.attrib, ('name', 'code', 'groupName', 'context', 'inAmbCard', 'type')):
            raise Exception(u'У записи не указаны все атрибуты')

        consentList = []
        for consentItem in item:
            if consentItem.tag != 'rbClientConsentType':
                raise Exception(u'Неожиданный элемент "%s"' % consentItem.tag)
            if not hasAllAttributes(consentItem.attrib, ('name', 'code', 'value')):
                raise Exception(u'У записи не указаны все атрибуты')
            consentList.append(consentItem.attrib)
        items.append((item.attrib, consentList))

    return items
