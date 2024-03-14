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
from PyQt4.QtCore import Qt, SIGNAL

from library.InDocTable import CInDocTableView
from library.DateEdit   import CDateEdit
from library.Utils      import toVariant, forceDate, forceRef
from library.ROComboBox import CROEditableComboBox
from library.crbcombobox import CRBComboBox


class CTreatmentScheduleItemDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)
        self.editor = None


    def createEditor(self, parent, option, index):
        model = index.model()
        row = index.row()
        column = index.column()
        sourceType = model.getSourceType(row, column)
        if sourceType > 0:
            editor = CROEditableComboBox(parent)
        else:
            editor = CRBComboBox(parent)
            editor.setTable('TreatmentType')
            self.connect(editor, SIGNAL('activated(QModelIndex)'), self.emitCommitData)
            self.connect(editor, SIGNAL('commit()'), self.emitCommitData)
            self.connect(editor, SIGNAL('editingFinished()'), self.commitAndCloseEditor)
        self.editor   = editor
        return editor


    def emitCommitData(self):
        self.emit(SIGNAL('commitData(QWidget *)'), self.sender())


    def commitAndCloseEditor(self):
        editor = self.sender()
        self.emit(SIGNAL('commitData(QWidget *)'), editor)
        self.emit(SIGNAL('closeEditor(QWidget *,QAbstractItemDelegate::EndEditHint)'), editor, QtGui.QAbstractItemDelegate.NoHint)


    def setEditorData(self, editor, index):
        model  = index.model()
        row = index.row()
        column = index.column()
        sourceType = model.getSourceType(row, column)
        if sourceType > 0:
            editor.setValue(sourceType)
        else:
            data = model.data(index, Qt.EditRole)
            editor.setShowFields(editor.showFields)
            editor.setValue(forceRef(data))
            editor.showPopup()


    def getEditorData(self, editor, index):
        return toVariant(editor.value())


    def setModelData(self, editor, model, index):
        model  = index.model()
        model.setData(index, toVariant(editor.value()))


class CDateEditItemDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)


    def createEditor(self, parent, option, index):
        editor = CDateEdit(parent)
        return editor


    def setEditorData(self, editor, index):
        model  = index.model()
        data = model.data(index, Qt.EditRole)
        editor.setDate(forceDate(data))


    def setModelData(self, editor, model, index):
        model.setData(index, toVariant(editor.date()))


class CTreatmentScheduleInDocTableView(CInDocTableView):
    __pyqtSignals__ = ('activated(QModelIndex)',
                      )
    # Типы для использования делегата
    treatmentType = 0
    isStart       = 1
    isEnd         = 2

    def __init__(self, parent):
        CInDocTableView.__init__(self, parent)
        self.setItemDelegate(CTreatmentScheduleItemDelegate(self))
        self.setItemDelegateForColumn(0, CDateEditItemDelegate(self))
        self.__actTreatmentFromRow = None
        self.__actStartFromRow = None
        self.__actEndFromRow = None


    def addTreatmentFromRow(self):
        if self._popupMenu is None:
            self.createPopupMenu()
        self.__actTreatmentFromRow = QtGui.QAction(u'Добавить цикл', self)
        self.__actTreatmentFromRow.setObjectName('actTreatmentFromRow')
        self.__actTreatmentFromRow.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self._popupMenu.addAction(self.__actTreatmentFromRow)
        self.addAction(self.__actTreatmentFromRow)
        self.connect(self.__actTreatmentFromRow, SIGNAL('triggered()'), self.on_treatmentFromRow)


    def addStartFromRow(self):
        if self._popupMenu is None:
            self.createPopupMenu()
        self.__actStartFromRow = QtGui.QAction(u'Добавить Заезд', self)
        self.__actStartFromRow.setObjectName('actStartFromRow')
        self.__actStartFromRow.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self._popupMenu.addAction(self.__actStartFromRow)
        self.addAction(self.__actStartFromRow)
        self.connect(self.__actStartFromRow, SIGNAL('triggered()'), self.on_startFromRow)


    def addEndFromRow(self):
        if self._popupMenu is None:
            self.createPopupMenu()
        self.__actEndFromRow = QtGui.QAction(u'Добавить Разъезд', self)
        self.__actEndFromRow.setObjectName('actEndFromRow')
        self.__actEndFromRow.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self._popupMenu.addAction(self.__actEndFromRow)
        self.addAction(self.__actEndFromRow)
        self.connect(self.__actEndFromRow, SIGNAL('triggered()'), self.on_endFromRow)


    def on_treatmentFromRow(self):
        index = self.currentIndex()
        row = index.row()
        column = index.column()
        self.model().setSourceType(row, column, CTreatmentScheduleInDocTableView.treatmentType)
        self.model().setData(index, toVariant(None))
        self.emit(SIGNAL('activated(QModelIndex)'), index)


    def on_startFromRow(self):
        index = self.currentIndex()
        row = index.row()
        column = index.column()
        self.model().setSourceType(row, column, CTreatmentScheduleInDocTableView.isStart)
        self.model().setData(index, toVariant(CTreatmentScheduleInDocTableView.isStart))


    def on_endFromRow(self):
        index = self.currentIndex()
        row = index.row()
        column = index.column()
        self.model().setSourceType(row, column, CTreatmentScheduleInDocTableView.isEnd)
        self.model().setData(index, toVariant(CTreatmentScheduleInDocTableView.isEnd))


    def on_popupMenu_aboutToShow(self):
        model = self.model()
        rowCount = model.rowCount()
        row = self.currentIndex().row()
        column = self.currentIndex().column()
        enable = rowCount > 0 and column > 0 and 0 <= row < rowCount
        self.__actTreatmentFromRow.setEnabled(enable)
        self.__actStartFromRow.setEnabled(enable)
        self.__actEndFromRow.setEnabled(enable)
        self.emit(SIGNAL('popupMenuAboutToShow()'))

