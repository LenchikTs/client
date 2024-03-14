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
from PyQt4.QtCore import Qt, QEvent

from library.DialogBase import CDialogBase
from library.Utils import firstMonthDay, lastMonthDay
from Resources.OrgStructureJobs import COrgStructureJobsModel

from Resources.Ui_JobFlexTemplateDialog import Ui_FlexTemplateDialog


class CJobFlexTemplateDialog(CDialogBase, Ui_FlexTemplateDialog):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.addModels('Jobs', COrgStructureJobsModel(self))
        self.setupUi(self)
        self.setModels(self.tblJobs, self.modelJobs, self.selectionModelJobs)
        self.modelJobs.setPeriod(0, 1)

        self.calendarView = self.calendarWidget.findChild(QtGui.QTableView)

        self.calendarView.installEventFilter(self) # для перехвата клавиатуры
        self.calendarView.viewport().installEventFilter(self) # для перехвата мыши

        self.calendarView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

        self.tblJobs.enableColsMove()


    def setDateRange(self, begDate, endDate):
        self.calendarWidget.setMinimumDate(begDate)
        self.calendarWidget.setMaximumDate(endDate)


    def setSelectedDate(self,  date):
        self.calendarWidget.setSelectedDate(date)
        row, column = self._cellForDate(date)
        index = self.calendarView.model().index(row, column)
        self.calendarView.setCurrentIndex(index)


    def getSelectedDates(self):
        result = []
        for index in self.calendarView.selectionModel().selectedIndexes():
            date = self._dateForCell(index.row(), index.column())
            result.append(date)
        result.sort()
        return result


    def getTemplates(self):
        return self.modelJobs.items()


    def removeExistingJobs(self):
        return self.chkRemoveExistingJobs.isChecked()


    def _cellForDate(self, date):
        doy  = date.dayOfWeek()
        currWeek, currYear = date.weekNumber()
        if currYear < date.year():
            currWeek = 0
        elif currYear > date.year():
            currWeek, currYear = date.addDays(-7).weekNumber()
            currWeek += 1

        firstDay = firstMonthDay(date)
        firstWeek, firstYear = firstDay.weekNumber()
        if firstYear < date.year():
            firstWeek = 0
        row = (currWeek-firstWeek
               +(1 if firstDay.dayOfWeek() == 1 else 0) # если неделя начинается с понедельника, то
                                                        # первая строка отводится на предыдущий месяц.
               +1 # 1 - названия дней недели
              )
        column = doy # т.к. 0 - это для номера недели
        return row, column


    def _dateForCell(self, row, column):
        currDate = self.calendarWidget.selectedDate()
        currRow, currColumn = self._cellForDate(currDate)
        return currDate.addDays((row-currRow)*7 + column-currColumn) # это только если неделя с понедельника.


    def _moveCalendarCursor(self, cursorAction, modifiers):
        index = self.calendarView.currentIndex()
        date = self._dateForCell(index.row(), index.column())
        if cursorAction == QtGui.QAbstractItemView.MoveUp:
            date = date.addDays(-7)
        elif  cursorAction == QtGui.QAbstractItemView.MoveDown:
            date = date.addDays(7)
        elif cursorAction == QtGui.QAbstractItemView.MovePrevious:
            date = date.addDays(-1)
        elif cursorAction == QtGui.QAbstractItemView.MoveLeft:
            date = date.addDays(-1)
        elif cursorAction == QtGui.QAbstractItemView.MoveNext:
            date = date.addDays(1)
        elif cursorAction == QtGui.QAbstractItemView.MoveRight:
            date = date.addDays(1)
        elif  cursorAction == QtGui.QAbstractItemView.MoveHome:
            date = firstMonthDay(date)
        elif  cursorAction == QtGui.QAbstractItemView.MoveEnd:
            date = lastMonthDay(date)
        date = min(max(date, self.calendarWidget.minimumDate()),
                   self.calendarWidget.maximumDate())
        row, column = self._cellForDate(date)
        index = self.calendarView.model().index(row, column)
        if modifiers & Qt.ControlModifier:
            command = QtGui.QItemSelectionModel.NoUpdate
        else:
            command = QtGui.QItemSelectionModel.ClearAndSelect
        self.calendarView.selectionModel().setCurrentIndex(index, command)


    def restoreSelection(self):
        selectionModel = self.calendarView.selectionModel()
        model = self.calendarView.model()
        command = QtGui.QItemSelectionModel.Select
        for row, column in self.selectedDays:
            selectionModel.select(model.index(row, column), command)


    def eventFilter(self, obj, event):
        if obj.parent() == self.calendarView:
            eventType = event.type()
            if eventType == QEvent.MouseButtonPress:
                pos = event.pos()
                index = self.calendarView.indexAt(pos)
                row = index.row()
                column = index.column()
                if row > 0 and column > 0:
                    self.calendarView.setCurrentIndex(index)
                    return True # filter out
                return True # filter out
        if obj == self.calendarView:
            eventType = event.type()
            if eventType == QEvent.KeyPress:
                key = event.key()
                if key == Qt.Key_Up:
                    self._moveCalendarCursor(QtGui.QAbstractItemView.MoveUp, event.modifiers())
                if key == Qt.Key_Down:
                    self._moveCalendarCursor(QtGui.QAbstractItemView.MoveDown, event.modifiers())
                elif key == Qt.Key_Left:
                    self._moveCalendarCursor(QtGui.QAbstractItemView.MovePrevious, event.modifiers())
                elif key == Qt.Key_Right:
                    self._moveCalendarCursor(QtGui.QAbstractItemView.MoveNext, event.modifiers())
                elif key == Qt.Key_Home:
                    self._moveCalendarCursor(QtGui.QAbstractItemView.MoveHome, event.modifiers())
                elif key == Qt.Key_End:
                    self._moveCalendarCursor(QtGui.QAbstractItemView.MoveEnd, event.modifiers())
                elif key == Qt.Key_Space:
                    index = self.calendarView.currentIndex()
                    if event.modifiers() & Qt.ControlModifier:
                        command = QtGui.QItemSelectionModel.Toggle
                    else:
                        command = QtGui.QItemSelectionModel.ClearAndSelect
                    self.calendarView.selectionModel().setCurrentIndex(index, command)
                return True # filter out
        return CDialogBase.eventFilter(self, obj, event)

