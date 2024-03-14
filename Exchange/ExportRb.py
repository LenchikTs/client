#!/usr/bin/env python
# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
u"""Абстрактные классы для выгрузки справочников"""

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QFile, QXmlStreamWriter, pyqtSignature, SIGNAL

from library.TableModel import CTableModel
from library.TreeModel import CDBTreeModel
from library.Utils import (anyToUnicode, exceptionToUnicode, forceBool, forceString, toVariant)
from library.DialogBase import CConstructHelperMixin

from Exchange.Utils import compressFileInRar

from Exchange.Ui_ExportRbPage1WithTree import Ui_ExportRbPage1WithTree
from Exchange.Ui_ExportRbPage2 import Ui_ExportRbPage2

# ******************************************************************************

class CExportAbstractRbWizard(QtGui.QWizard):
    u"""Абстрактный класс мастера выгрузки справочников"""
    def __init__(self, prefix, rbName, parent=None):
        QtGui.QWizard.__init__(self, parent, Qt.Dialog)
        self.setWizardStyle(QtGui.QWizard.ModernStyle)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle(u'Экспорт справочника "%s"' % rbName)
        self.rbName = rbName
        self.prefix = prefix
        self.selectedItems = []

# ******************************************************************************

class CRbXmlStreamWriter(QXmlStreamWriter):
    u"""Абстрактный класс записи справочников в XML"""
    def __init__(self, parent, idList):
        QXmlStreamWriter.__init__(self)
        self._parent = parent
        self.setAutoFormatting(True)
        self._idList = idList
        self._db = QtGui.qApp.db


    def createQuery(self, idList):
        """ Запрос информации по справочнику. Если idList пуст,
            запрашиваются все элементы"""
        raise NotImplementedError


    def writeRecord(self, record):
        u"""Абстрактный метод для записи данных в XML"""
        raise NotImplementedError


    def writeHeader(self):
        u"""Абстрактный метод для записи заголовка XML"""
        raise NotImplementedError


    def writeFile(self, device, progressBar):
        u"""Записывает данные, полученные через createQuery в device
        с помощью функции writeRecord, обновляя progressBar"""
        try:
            from buildInfo import lastChangedRev, lastChangedDate
        except ImportError:
            lastChangedRev = 'unknown'
            lastChangedDate = 'unknown'

        try:
            progressBar.setText(u'Запрос данных')
            query = self.createQuery(self._idList)
            self.setDevice(device)
            progressBar.setMaximum(max(query.size(), 1))
            progressBar.reset()
            progressBar.setValue(0)

            self.writeStartDocument()
            self.writeHeader()

            self.writeAttribute("SAMSON",
                "2.0 revision(%s, %s)" %(lastChangedRev, lastChangedDate))

            while query.next():
                self.writeRecord(query.record())
                progressBar.step()

            self.writeEndDocument()

        except IOError, error:
            QtGui.qApp.logCurrentException()
            msg = ''

            if hasattr(error, 'filename'):
                msg = u'%s:\n[Errno %s] %s' % (
                   error.filename, error.errno, anyToUnicode(error.strerror))
            else:
                msg = u'[Errno %s] %s' % (
                    error.errno, anyToUnicode(error.strerror))

            QtGui.QMessageBox.critical(self._parent,
                u'Произошла ошибка ввода-вывода', msg, QtGui.QMessageBox.Close)
            return False

        except Exception, error:
            QtGui.qApp.logCurrentException()
            QtGui.QMessageBox.critical(self._parent,
                u'Произошла ошибка', exceptionToUnicode(error), QtGui.QMessageBox.Close)
            return False

        return True

# ******************************************************************************

class CExportAbstractRbPage1(QtGui.QWizardPage, CConstructHelperMixin):
    u"""Первая страница мастера экспорта: выбор элементов для выгрузки"""

    def __init__(self, tableName, parent):
        QtGui.QWizardPage.__init__(self, parent)
        self._parent = parent
        self.tableName = tableName
        self.setTitle(u'Параметры экспорта')
        self.setSubTitle(u'Выбор записей для экспорта')


    def isComplete(self):
        u"""Включает кнопку 'Вперед' в мастере экспорта"""
        # проверим, пустой ли у нас список выбранных элементов
        return self.chkExportAll.isChecked() or self._parent.selectedItems != []


    def preSetupUi(self):
        u"""Настройка моделей перед вызовом setupUi()"""
        self.addModels('Table', CTableModel(self, self.cols, self.tableName))


    def postSetupUi(self):
        u"""Настройка элементов после setupUi()"""
        self.setModels(self.tblItems, self.modelTable, self.selectionModelTable)
        self.tblItems.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        idList = self.select()
        self.modelTable.setIdList(idList)
        self.selectionModelTable.clearSelection()
        self.tblItems.setFocus(Qt.OtherFocusReason)
        exportAll = forceBool(QtGui.qApp.preferences.appPrefs.get('Export%sExportAll' % self._parent.prefix, 'False'))
        self.chkExportAll.setChecked(exportAll)
        self.exportAll(exportAll)


    def exportAll(self, val):
        self.tblItems.setEnabled(not val)
        self.btnClearSelection.setEnabled(not val)


    def _setSelectedItems(self, selectedItems):
        u"""Установка списка выбранных элементов"""
        self._parent.selectedItems = selectedItems


    def _selectedItems(self):
        u"""Возвращает список выбранных элементов"""
        return self._parent.selectedItems


    def select(self):
        u"""Получение списка идентификаторов всех элементов из справочника"""
        table = self.modelTable.table()
        return QtGui.qApp.db.getIdList(table.name(), order=self.order)


    @pyqtSignature('QModelIndex')
    def on_tblItems_clicked(self, _):
        u"""Обработчик кликов по таблице с элементами справочника"""
        self._parent.selectedItems = self.tblItems.selectedItemIdList()
        self.emit(SIGNAL('completeChanged()'))


    @pyqtSignature('')
    def on_btnClearSelection_clicked(self):
        u"""Обработчик кнопки очистки выбора"""
        self._parent.selectedItems = []
        self.selectionModelTable.clearSelection()
        self.emit(SIGNAL('completeChanged()'))


    @pyqtSignature('bool')
    def on_chkExportAll_clicked(self, checked):
        u"""Обработчик кнопки 'Выбрать все'"""
        self.exportAll(checked)
        self.emit(SIGNAL('completeChanged()'))

# ******************************************************************************

class CExportAbstractRbPage1WithTree(CExportAbstractRbPage1,
                                     Ui_ExportRbPage1WithTree):
    u"""Первая страница мастера экспорта: выбор элементов для выгрузки с
    выбором через TreeModel"""

    def __init__(self, tableName, parent):
        CExportAbstractRbPage1.__init__(self, tableName, parent)
        self.preSetupUi()
        self.setupUi(self)
        self.postSetupUi()


    def isComplete(self):
        # проверим пустой ли у нас список выбранных элементов
        if self.chkExportAll.isChecked():
            return True
        else:
            for key in self._selectedItems().keys():
                if self._selectedItems()[key] != []:
                    return True
            return False


    def preSetupUi(self):
        self.addModels('Tree', CDBTreeModel(self,
            self.tableName, 'id', 'group_id', 'name', order='code'))
        CExportAbstractRbPage1.preSetupUi(self)


    def postSetupUi(self):
        self.setModels(self.treeItems, self.modelTree, self.selectionModelTree)
        self.treeItems.header().hide()
        CExportAbstractRbPage1.postSetupUi(self)


    def exportAll(self, val):
        self.tblItems.setEnabled(not val)
        self.treeItems.setEnabled(not val)
        self.btnSelectAll.setEnabled(not val)
        self.btnClearSelection.setEnabled(not val)


    def select(self):
        table = self.modelTable.table()
        groupId = self.currentGroupId()
        return QtGui.qApp.db.getIdList(table.name(),
                            'id',
                            table['group_id'].eq(groupId),
                            self.order)


    def selectItem(self):
        return self.exec_()


    def setCurrentItemId(self, itemId):
        self.tblItems.setCurrentItemId(itemId)


    def currentItemId(self):
        return self.tblItems.currentItemId()


    def currentGroupId(self):
        return self.modelTree.itemId(self.treeItems.currentIndex())


    def renewListAndSetTo(self, itemId=None):
        if not itemId:
            itemId = self.tblItems.currentItemId()
        idList = self.select()
        self.tblItems.setIdList(idList, itemId)
        self.selectionModelTable.clearSelection()
        # восстанавливаем выбранные элементы в таблице
        groupId = self.currentGroupId()

        if groupId in self._selectedItems().keys():
            rows = []
            for _id in self._selectedItems()[groupId]:
                if idList.count(_id) > 0:
                    row = idList.index(_id)
                    rows.append(row)
            for row in rows:
                index = self.modelTable.index(row, 0)
                self.selectionModelTable.select(index,
                    QtGui.QItemSelectionModel.Select|
                    QtGui.QItemSelectionModel.Rows)


    def selectNestedElements(self, _id, selectedItems, select):
        if not select:
            # рекурсивно убираем выделение с дочерних элементов
            if selectedItems.has_key(_id):
                for i in selectedItems[_id]:
                    self.selectNestedElements(i, selectedItems, select)

                selectedItems.pop(_id)

            return

        itemIndex = self.modelTree.findItemId(_id)

        if itemIndex:
            table = self.modelTable.table()
            leafList = QtGui.qApp.db.getIdList(
               table.name(), 'id', table['group_id'].eq(_id), self.order)

            if not selectedItems.has_key(_id):
                selectedItems[_id] = []

            if leafList and leafList != []:
                selectedItems[_id].extend(leafList)

            for i in leafList:
                self.selectNestedElements(i, selectedItems, select)


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelTree_currentChanged(self, _, previous):
        # сохраняем индексы выбранных элементов в таблице
        if previous is not None:
            prevId = self.modelTree.itemId(previous)
            self._selectedItems()[prevId] = self.tblItems.selectedItemIdList()

        self.renewListAndSetTo(None)


    @pyqtSignature('QModelIndex')
    def on_tblItems_clicked(self, index):
        self._selectedItems()[self.currentGroupId()] = (
                self.tblItems.selectedItemIdList())

        # если стоит галка "выделять дочерние элементы", рекурсивно
        # выделаем все ветки выбранных элементов
        if self.chkRecursiveSelection.isChecked():
            self.selectNestedElements(self.currentItemId(),
              self._selectedItems(), self.selectionModelTable.isSelected(index))

        self.emit(SIGNAL('completeChanged()'))


    @pyqtSignature('')
    def on_btnSelectAll_clicked(self):
        selectionList = self.modelTable.idList()
        self._selectedItems()[self.currentGroupId()] = selectionList

        if self.chkRecursiveSelection.isChecked():
            for item in selectionList:
                self.selectNestedElements(item, self._selectedItems(), True)

        for _id in selectionList:
            index = self.modelTable.index(selectionList.index(_id), 0)
            self.selectionModelTable.select(index,
                QtGui.QItemSelectionModel.Select|
                QtGui.QItemSelectionModel.Rows)

        self.emit(SIGNAL('completeChanged()'))


    @pyqtSignature('')
    def on_btnClearSelection_clicked(self):
        if self.chkRecursiveSelection.isChecked():
            for _id in self.modelTable.idList():
                self.selectNestedElements(_id, self._selectedItems(), False)

        self._selectedItems().pop(self.currentGroupId())
        self.selectionModelTable.clearSelection()
        self.emit(SIGNAL('completeChanged()'))


# ******************************************************************************

class CExportAbstractRbPage2(QtGui.QWizardPage, Ui_ExportRbPage2):
    u"""Вторая страница класса экспорта. Выбирает имя файла и пишет XML.
    Необходимо определить метод _xmlWriter, возвращаюший потомка
    CRbXmlStreamWriter."""

    def __init__(self, xmlWriter, parent):
        self.done = False
        QtGui.QWizardPage.__init__(self, parent)
        self.setupUi(self)
        self._parent = parent
        self.setTitle(u'Параметры сохранения')
        self.setSubTitle(u'Выбор места для сохранения')
        self.progressBar.setFormat('%p%')
        self.progressBar.setValue(0)
        self.__selectedItems = None
        self._xmlWriter = xmlWriter

        fileName = forceString(QtGui.qApp.preferences.appPrefs.get('Export%sFileName' % parent.prefix, ''))
        compressRAR = forceBool(QtGui.qApp.preferences.appPrefs.get('Export%sCompressRAR' % parent.prefix, 'False'))

        self.edtFileName.setText(fileName)
        self.chkRAR.setChecked(compressRAR)


    def isComplete(self):
        u"""Включает кнопку 'Финиш' в мастере экспорта"""
        return self.done


    def initializePage(self):
        u"""Инициализация страницы при переходе на нее"""
        self.btnExport.setEnabled(not self.edtFileName.text().isEmpty())
        self._setSelectedItems(self._parent.selectedItems)
        self.done = False


    def _setSelectedItems(self, selectedItems):
        u"""Установка списка выбранных элементов"""
        self.__selectedItems = selectedItems


    def _selectedItems(self):
        u"""Возвращает список выбранных элементов"""
        return self.__selectedItems


    def _exportInt(self):
        u"""Метод, осуществляющий экспорт. Перед вызовом необходимо
        установить список выбранных элементов через _setSelectedItems"""
        assert (self._parent.page1.chkExportAll.isChecked() or
            self.__selectedItems)
        fileName = self.edtFileName.text()

        if fileName.isEmpty():
            return

        outFile = QFile(fileName)
        if not outFile.open(QFile.WriteOnly | QFile.Text):
            QtGui.QMessageBox.warning(self,
                  self.tr(u'Экспорт справочника "%s"' % self._parent.rbName),
                  self.tr(u'Не могу открыть файл для записи %1:\n%2.')
                        .arg(fileName)
                        .arg(outFile.errorString()))

        writer = self._xmlWriter(self, self.__selectedItems)

        if writer.writeFile(outFile, self.progressBar):
            self.progressBar.setText(u'Готово')
        else:
            self.progressBar.setText(u'Прервано')
            outFile.close()
            return

        outFile.close()
        compress = self.chkRAR.isChecked()

        if compress:
            self.progressBar.setText(u'Сжатие')
            compressFileInRar(fileName, fileName+'.rar')
            self.progressBar.setText(u'Сжато в "%s"' % (fileName+'.rar'))

        self.done = True
        self.btnExport.setEnabled(False)
        self.emit(SIGNAL('completeChanged()'))

        prefs = QtGui.qApp.preferences.appPrefs
        prefix = self._parent.prefix
        prefs['Export%sFileName' % prefix] = toVariant(fileName)
        prefs['Export%sExportAll' % prefix] = toVariant(
            self._parent.page1.chkExportAll.isChecked())
        prefs['Export%sCompressRAR' % prefix] = toVariant(compress)


    @pyqtSignature('')
    def on_btnSelectFile_clicked(self):
        u"""Обаботчик кнопки выбора файла для записи данных"""
        fileName = QtGui.QFileDialog.getSaveFileName(
            self, u'Укажите файл с данными', self.edtFileName.text(),
            u'Файлы XML (*.xml)')

        if fileName != '':
            self.edtFileName.setText(fileName)
            self.btnExport.setEnabled(True)


    @pyqtSignature('')
    def on_btnExport_clicked(self):
        u"""Обаботчик кнопки 'Начать экспорт'"""
        self._exportInt()


    @pyqtSignature('QString')
    def on_edtFileName_textChanged(self, text):
        u"""Обаботчик изменения названия файла"""
        self.btnExport.setEnabled(text != '')
        self.emit(SIGNAL('completeChanged()'))

# ******************************************************************************

class CExportAbstractRbPage2WithTree(CExportAbstractRbPage2):
    def __init__(self, xmlWriter, parent):
        CExportAbstractRbPage2.__init__(self, xmlWriter, parent)


    def _exportInt(self):
        idList = []
        if not self._parent.page1.chkExportAll.isChecked():
            for key in self._parent.selectedItems.keys():
                if key and key not in idList:
                    idList.append(key)

                for _id in self._parent.selectedItems[key]:
                    if _id not in idList:
                        idList.append(_id)

            if idList == []:
                QtGui.QMessageBox.warning(self,
                    u'Экспорт справочника "%s"' % self._parent.rbName,
                    u'Не выбрано ни одного элемента для выгрузки')
                self._parent.back() # вернемся на пред. страницу. пусть выбирают
                return

        self._setSelectedItems(idList)
        CExportAbstractRbPage2._exportInt(self)
