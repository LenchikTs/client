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

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL

from library.Utils import CColsMovingFeature, forceInt, getPref, setPref, forceString, forceBool
#from library.DialogBase import CDialogBase
from library.PreferencesMixin import CPreferencesMixin

from Events.NomenclatureExpense.NomenclatureExpenseDayDialog import CNomenclatureExpenseDayDialog
from Events.NomenclatureExpense.NomenclatureExpenseItemDelegate import CLocItemDelegate

#from Events.NomenclatureExpense.Ui_ExtendAppointmentNomenclatureDialog import Ui_ExtendAppointmentNomenclatureDialog


class CNomenclatureExpenseView(QtGui.QTableView, CPreferencesMixin, CColsMovingFeature):
    __pyqtSignals__ = ('popupMenuAboutToShow()',
                       )

    def __init__(self, parent):
        QtGui.QTableView.__init__(self, parent)
        self.verticalHeader().hide()
        self.setItemDelegate(CLocItemDelegate(self))
        self._popupMenu = None
        self._actEditDayNomenclatureExpense = None
#        self._actExtendAppointmentNomenclature = None
        self._copiedDayData = None


    def headerMenu(self, pos):
        pos2 = QtGui.QCursor().pos()
        header = self.horizontalHeader()
        menu = QtGui.QMenu()
        checkedActions = []
        objectName = self.objectName()
        if objectName == u'tblNomenclatureExpense':
            firstCol = 0
            lastCol = 9
        elif objectName == u'tblNomenclatureExpenseDays':
            firstCol = 9
            lastCol = len(self.model().cols())
        for i, col in enumerate(self.model().cols()):
            if i >= firstCol and i < lastCol:
                action = QtGui.QAction(forceString(col.title()), self)
                action.setCheckable(True)
                action.setData(i)
                action.setEnabled(col.switchOff())
                if not header.isSectionHidden(i):
                    action.setChecked(True)
                    checkedActions.append(action)
                menu.addAction(action)
        if len(checkedActions) == 1:
            checkedActions[0].setEnabled(False)
        selectedItem = menu.exec_(pos2)
        if selectedItem:
            section = forceInt(selectedItem.data())
            if header.isSectionHidden(section):
                header.showSection(section)
            else:
                header.hideSection(section)


    def contextMenuEvent(self, event): # event: QContextMenuEvent
        if self._popupMenu:
            self._popupMenu.exec_(event.globalPos())
            event.accept()
        else:
            event.ignore()


    def createPopupMenu(self):
        menu = QtGui.QMenu(self)
        menu.setObjectName('popupMenu')
        self.setPopupMenu(menu)
        return self._popupMenu


    def setPopupMenu(self, menu):
        if self._popupMenu:
            self.disconnect(self._popupMenu, SIGNAL('aboutToShow()'), self.on_popupMenu_aboutToShow)
        self._popupMenu = menu
        if menu:
            self.connect(menu, SIGNAL('aboutToShow()'), self.on_popupMenu_aboutToShow)


    def setNomenclatureExpensePopupMenu(self, menu):
        if self._popupMenu:
            self.disconnect(self._popupMenu, SIGNAL('aboutToShow()'), self.on_nomenclatureExpensePopupMenu_aboutToShow)
        self._popupMenu = menu
        if menu:
            self.connect(menu, SIGNAL('aboutToShow()'), self.on_nomenclatureExpensePopupMenu_aboutToShow)


    def on_popupMenu_aboutToShow(self):
        index = self.currentIndex()
        model = self.model()

        exists = model.existsByIndex(index)
        isDone = model.existsDoneByIndex(index)
        isAfterLastDone = not model.existsDoneAfterIndex(index)
        isAfterBegDate = model.isIndexAfterBegDate(index)

        editable = exists and not isDone
        canPaste = editable or (not exists and isAfterLastDone) and isAfterBegDate
        canceledRow = False
        items = model._groups[index.row()].items
        for i in range(len(items)):
            if forceInt(model._groups[index.row()].items[i].action._record.value('status')) == 3:
                canceledRow = True
                break
        editableDel = editable and not self.model().existsDoneActionItemExecToDateByIndex(index) and not self.model().existsDoneActionAfterIndex(index)
        self._actCopyDayNomenclatureExpense.setEnabled(False if canceledRow else exists)
        self._actDeleteDayNomenclatureExpense.setEnabled(False if canceledRow else editableDel)
        self._actEditDayNomenclatureExpense.setEnabled(True)
        self._actPasteDayNomenclatureExpense.setEnabled(False if canceledRow else canPaste)

        self.emit(SIGNAL('popupMenuAboutToShow()'))


    def on_nomenclatureExpensePopupMenu_aboutToShow(self):
        index = self.currentIndex()
        model = self.model()
        enabled = False
        if index.row() <= len(model._groups)-1:
            items = model._groups[index.row()].items
            for i in range(len(items)):
                if (forceInt(items[i].action._record.value('status')) != 2 and forceInt(items[i].action._record.value('status')) != 3 and not enabled):
                    enabled = True
                if forceInt(items[i].action._record.value('status')) == 3:
                    enabled = False
                    break
        self._popupMenu.setEnabled(enabled)
        self.emit(SIGNAL('popupMenuAboutToShow()'))


    def addDeleteDays(self):
        if self._popupMenu is None:
            self.createPopupMenu()

        self._actDeleteDayNomenclatureExpense = QtGui.QAction(u'Удалить', self)
        self._popupMenu.addAction(self._actDeleteDayNomenclatureExpense)
        self.connect(self._actDeleteDayNomenclatureExpense, SIGNAL('triggered()'), self.on_deleteDays)


    def on_deleteDays(self):
        rowsColumns = {}
        for index in self.selectedIndexes():
            rowsColumns.setdefault(index.row(), []).append(index.column())

        model = self.model()
        for row, columns in rowsColumns.items():
            for column in columns:
                model.deleteItemsByIndex(model.index(row, column))
        model.emitAllDataChanged()


    def addEditDay(self):
        if self._popupMenu is None:
            self.createPopupMenu()

        self._actEditDayNomenclatureExpense = QtGui.QAction(u'Редактировать', self)
        self._popupMenu.addAction(self._actEditDayNomenclatureExpense)
        self.connect(self._actEditDayNomenclatureExpense, SIGNAL('triggered()'), self.on_editDayNomenclatureExpense)


    def addCopyDay(self):
        if self._popupMenu is None:
            self.createPopupMenu()

        self._actCopyDayNomenclatureExpense = QtGui.QAction(u'Копировать', self)
        self._popupMenu.addAction(self._actCopyDayNomenclatureExpense)
        self.connect(self._actCopyDayNomenclatureExpense, SIGNAL('triggered()'), self.on_copyDayNomenclatureExpense)


    def addPasteDay(self):
        if self._popupMenu is None:
            self.createPopupMenu()

        self._actPasteDayNomenclatureExpense = QtGui.QAction(u'Вставить', self)
        self._popupMenu.addAction(self._actPasteDayNomenclatureExpense)
        self.connect(self._actPasteDayNomenclatureExpense, SIGNAL('triggered()'), self.on_pasteDayNomenclatureExpense)


    def on_copyDayNomenclatureExpense(self):
        index = self.currentIndex()
        if not index.isValid():
            return

        row = index.row()
        items = self.model().getItemsByIndex(index) or []

        self._copiedDayData = {row: items}


    def on_pasteDayNomenclatureExpense(self):
        if not self._copiedDayData:
            return

        rowsColumns = {}
        for index in self.selectedIndexes():
            if index.row() not in self._copiedDayData:
                continue

            rowsColumns.setdefault(index.row(), []).append(index.column())

        model = self.model()

        for row, items in self._copiedDayData.items():
            for column in rowsColumns[row]:
                model.setItemsForDayIndex(model.index(row, column), items)
        self.model().emitAllDataChanged()


    def on_editDayNomenclatureExpense(self):
        index = self.currentIndex()
        if not index.isValid():
            return
        row = index.row()
        items = self.model().getItemsByIndex(index)
        if not items:
            return
        canceled = False
        groupItems = self.model()._groups[row].items
        for item in range(len(groupItems)):
            if forceInt(groupItems[item].record.value('status')) == 3:
                canceled = True
                break
        canceled = canceled or self.model().existsDoneActionAfterIndex(index)
        dosageUnitName = self.model().getDosageUnitName(row)
        dialog = CNomenclatureExpenseDayDialog(self, items, dosageUnitName=dosageUnitName, ignoreTime = self.model()._ignoreTime)
        dialog.load(readOnly=canceled)
        planItems, doneItems = self.getDayStatistics(items)
        dialog.setDayStatistics(planItems, doneItems)
        if dialog.exec_():
            items = dialog.itemsToSave()
            isApplyChangesCourseNextDays = dialog.getApplyChangesCourseNextDays()
            QtGui.qApp.preferences.appPrefs['NomenclatureExpenseIsApplyChangesCourseNextDays'] = forceBool(isApplyChangesCourseNextDays)
            isEditable = False
            for i in items:
                if not i.executedDatetime and not dialog.modelNomenclatureExpense._readOnly:
                    isEditable = True
                    break
            if isEditable:
                self.model().setItemsForDayIndex(index, items, isApplyChangesCourseNextDays=isApplyChangesCourseNextDays)
                self.model().reset()


    def getDayStatistics(self, items):
        planItems = 0
        if not items:
            return None
        planItems = len(items)

        not_done_items = []

        for item in items:
            executedDatetime = item.executedDatetime
            if executedDatetime is None:
                not_done_items.append(item)
            elif executedDatetime.isNull() or not executedDatetime.isValid():
                not_done_items.append(item)

        return planItems, planItems-len(not_done_items)


    def loadPreferences(self, preferences):
        model = self.model()
        self.horizontalHeader().setStretchLastSection(True)
        charWidth = self.fontMetrics().width('A0')/2
        cols = model.cols()
        i = 0
        for col in cols:
            width = forceInt(getPref(preferences, col.key, col.width*charWidth))
            if width:
                self.setColumnWidth(i, width)
            i += 1


    def savePreferences(self):
        preferences = {}
        model = self.model()
        cols = model.cols()
        i = 0
        for col in cols:
            width = self.columnWidth(i)
            setPref(preferences, col.key, QtCore.QVariant(width))
            i += 1
        return preferences

