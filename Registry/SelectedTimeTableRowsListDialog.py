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
from PyQt4.QtCore import Qt, pyqtSignature, QVariant, QAbstractTableModel, QDate

from library.Utils import toVariant

from Timeline.TimeTable                   import formatTimeRange
from Registry.Utils import CAppointmentPurposeCache

from Registry.Ui_SelectedTimeTableRowsListDialog import Ui_SelectedTimeTableRowsListDialog


class CSelectedTimeTableRowsListDialog(QtGui.QDialog, Ui_SelectedTimeTableRowsListDialog):
    def __init__(self, parent, scheduleList=None):
        QtGui.QDialog.__init__(self, parent)
        self.tableModel = CSelectedTimeTableRowsModel(self)
        self.tableSelectionModel = QtGui.QItemSelectionModel(self.tableModel, self)
        self.tableSelectionModel.setObjectName('tableSelectionModel')
        self.setupUi(self)
        self.tblSelectedTimeTableRowsList.setModel(self.tableModel)
        self.tblSelectedTimeTableRowsList.setSelectionModel(self.tableSelectionModel)
        self.tblSelectedTimeTableRowsList.setSelectionMode(self.tblSelectedTimeTableRowsList.SingleSelection)
        self.tblSelectedTimeTableRowsList.horizontalHeader().setStretchLastSection(True)
        self._parent = parent
        self.schedule =  None
        self.scheduleList = scheduleList
        self.tableModel.setScheduleList(self.scheduleList)
        verticalHeader = self.tblSelectedTimeTableRowsList.verticalHeader()
        verticalHeader.show()
        verticalHeader.setResizeMode(QtGui.QHeaderView.Fixed)


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Ok:
            self.getSchedule()
        elif buttonCode == QtGui.QDialogButtonBox.Cancel:
            self.close()


    def getSchedule(self):
        scheduleIndexes = self.tblSelectedTimeTableRowsList.selectionModel().selectedRows()
        self.schedule = self.scheduleList[scheduleIndexes[0].row()]
        self.close()


    def values(self):
        return self.schedule


    def setValue(self, schedule):
        self.schedule = schedule


class CSelectedTimeTableRowsModel(QAbstractTableModel):
    
    headerText = ( u'Назначение', u'Время', u'Каб', u'План', u'Готов' )
    
    def __init__(self, parent):
        QAbstractTableModel.__init__(self, parent)
        self.scheduleList = []
        self.redBrush = QtGui.QBrush(Qt.red)

    def setScheduleList(self, scheduleList):
        self.scheduleList = scheduleList

    def getAppointmentPurposeName(self, appointmentPurposeId):
        return CAppointmentPurposeCache.getName(appointmentPurposeId)

    def flags(self, index):
        return Qt.ItemIsEnabled|Qt.ItemIsSelectable

    def rowCount(self, index = None):
            return len(self.scheduleList)

    def columnCount(self, index = None):
            return 5

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(self.headerText[section])
        if orientation == Qt.Vertical:
            date = self.scheduleList[section].date
            if role == Qt.DisplayRole:
                return QVariant(QDate.shortDayName(date.dayOfWeek()))
            elif role == Qt.ToolTipRole:
                if self.begDate:
                    return QVariant(date)
            elif role == Qt.ForegroundRole:
                if date.dayOfWeek()>=6:
                    return QVariant(self.redBrush)
        return QVariant()

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            schedule = self.scheduleList[row]
            if column == 0: # Назначение
                appointmentPurposeId = schedule.appointmentPurposeId
                return toVariant(self.getAppointmentPurposeName(appointmentPurposeId))
            if column == 1: # Время
                timeRange = schedule.begTime, schedule.endTime
                reasonOfAbsenceId = schedule.reasonOfAbsenceId
                if reasonOfAbsenceId:
                    return toVariant(formatTimeRange(timeRange)+', '+self.getReasonOfAbsenceCode(reasonOfAbsenceId))
                else:
                    return toVariant(formatTimeRange(timeRange))
            elif column == 2: # Каб
                return toVariant(schedule.office)
            elif column == 3: # План
                return toVariant(schedule.capacity)
            elif column == 4: # Готов
                return toVariant(schedule.capacity-schedule.getQueuedClientsCount())
        elif role == Qt.FontRole:
            schedule = self.scheduleList[row]
            if schedule.reasonOfAbsenceId:
                result = QtGui.QFont()
                result.setBold(True)
                result.setStrikeOut(True)
                return QVariant(result)
        return QVariant()
