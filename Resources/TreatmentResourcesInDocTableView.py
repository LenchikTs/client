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

import json

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, SIGNAL, QVariant

from library.InDocTable import CInDocTableView
from library.Utils      import forceString, forceInt, getPref, setPref
from Events.Action      import CActionTypeCache


class CTreatmentResourcesInDocTableView(CInDocTableView):
    def __init__(self, parent):
        CInDocTableView.__init__(self, parent)
        self.__actAppointmentToDate = None
        self.__actAppointmentToTreatment = None


    def addAppointmentToDate(self):
        if self._popupMenu is None:
            self.createPopupMenu()
        self.__actAppointmentToDate = QtGui.QAction(u'Назначить на дату', self)
        self.__actAppointmentToDate.setObjectName('actAppointmentToDate')
        self.__actAppointmentToDate.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self._popupMenu.addAction(self.__actAppointmentToDate)
        self.addAction(self.__actAppointmentToDate)
        self.connect(self.__actAppointmentToDate, SIGNAL('triggered()'), self.on_appointmentToDate)


    def addAppointmentToTreatment(self):
        if self._popupMenu is None:
            self.createPopupMenu()
        self.__actAppointmentToTreatment = QtGui.QAction(u'Назначить на цикл', self)
        self.__actAppointmentToTreatment.setObjectName('actAppointmentToTreatment')
        self.__actAppointmentToTreatment.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self._popupMenu.addAction(self.__actAppointmentToTreatment)
        self.addAction(self.__actAppointmentToTreatment)
        self.connect(self.__actAppointmentToTreatment, SIGNAL('triggered()'), self.on_appointmentToTreatment)


    def on_appointmentToDate(self):
        index = self.currentIndex()
        row = index.row()
        column = index.column()
        self.model().on_appointmentToDate(row, column)
        eventEditor = self.model().eventEditor
        if eventEditor:
            currentRow = eventEditor.tblEvents.model().getItemIdCheckedRow()
            self.model().setActionCountBusy(eventEditor.getActionCountBusy())
            eventEditor.tblEvents.setCurrentRow(currentRow)


    def on_appointmentToTreatment(self):
        index = self.currentIndex()
        row = index.row()
        column = index.column()
        self.model().on_appointmentToTreatment(row, column)
        eventEditor = self.model().eventEditor
        if eventEditor:
            currentRow = eventEditor.tblEvents.model().getItemIdCheckedRow()
            self.model().setActionCountBusy(eventEditor.getActionCountBusy())
            eventEditor.tblEvents.setCurrentRow(currentRow)


    def on_popupMenu_aboutToShow(self):
        model = self.model()
        rowCount = model.rowCount()
        row = self.currentIndex().row()
        column = self.currentIndex().column()
        enable = rowCount > 0 and column > 0 and 0 <= row < rowCount and bool(model.eventIdList) and bool(model.selectedDate)
        if enable:
            datetimePrev, datetimeLast = model.dates[row]
            if model.headers[column] and (((datetimePrev, datetimeLast), model.headers[column]) in model.items.keys()):
                keyScheme = ((datetimePrev, datetimeLast), model.headers[column])
                enable = bool(model.items.get(keyScheme, None))
            else:
                enable = False
        self.__actAppointmentToDate.setEnabled(enable)
        self.__actAppointmentToTreatment.setEnabled(enable)
        self.emit(SIGNAL('popupMenuAboutToShow()'))


    def loadPreferences(self, preferences):
        model = self.model()
        horizontalHeader = self.horizontalHeader()
        headerCount = horizontalHeader.count()
        charWidth = self.fontMetrics().width('A0')/2
        for col in range(0, headerCount):
            actionTypeId = model.headers[col]
            if actionTypeId:
                title = forceString(CActionTypeCache.getById(actionTypeId).name) + forceString(u'(10-10)')
            else:
                title = forceString(u'00:00 - 00:00')
            width = forceInt(getPref(preferences, unicode('width '+title.lower()), horizontalHeader.sectionSize(col)*charWidth))
            if width:
                self.setColumnWidth(col, width)
        self.horizontalHeader().setStretchLastSection(True)
        state = getPref(preferences, 'headerState', QVariant()).toByteArray()
        if state:
            header = self.horizontalHeader()
            try:
                state = json.loads(forceString(state))
            except:
                header.restoreState(state)
                return
            maxVIndex = 0
            for col in range(0, headerCount):
                actionTypeId = model.headers[col]
                if actionTypeId:
                    title = forceString(CActionTypeCache.getById(actionTypeId).name) + forceString(u'(10-10)')
                else:
                    title = forceString(u'00:00 - 00:00')
                name = title.lower()
                curVIndex = header.visualIndex(col)
                if name in state:
                    vIndex = state[name][0]
                    isHidden = state[name][1]
                    if vIndex > maxVIndex:
                        maxVIndex = vIndex
                    if vIndex != curVIndex:
                        header.moveSection(curVIndex, vIndex)
                    if isHidden:
                        header.setSectionHidden(col, True)
                else:
                    header.moveSection(curVIndex, headerCount-1)


    def savePreferences(self):
        preferences = {}
        model = self.model()
        horizontalHeader = self.horizontalHeader()
        headerCount = horizontalHeader.count()
        for col in range(0, headerCount):
            width = self.columnWidth(col)
            actionTypeId = model.headers[col]
            if actionTypeId:
                title = forceString(CActionTypeCache.getById(actionTypeId).name) + forceString(u'(10-10)')
            else:
                title = forceString(u'00:00 - 00:00')
            setPref(preferences, unicode('width '+title.lower()), QVariant(width))
        header = self.horizontalHeader()
        if header.isMovable() or self.headerColsHidingAvailable():
            params = {}
            needSave = False
            for col in range(0, headerCount):
                if col != header.visualIndex(col)  or header.isSectionHidden(col):
                    needSave = True
                    break
            if needSave:
                for col in range(0, headerCount):
                    actionTypeId = model.headers[col]
                    if actionTypeId:
                        title = forceString(CActionTypeCache.getById(actionTypeId).name) + forceString(u'(10-10)')
                    else:
                        title = forceString(u'00:00 - 00:00')
                    name = title.lower()
                    params[name] = (header.visualIndex(col), header.isSectionHidden(col))
            setPref(preferences, 'headerState', QVariant(json.dumps(params)))
        return preferences

