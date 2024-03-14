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

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature

from Events.EventTypeModel import CEventTypeTableModel, CEventTypePurposeTableModel
from library.Utils         import forceString

from Events.Ui_EventTypeListEditor import Ui_EventTypeListEditor


class CEventTypeListEditorDialog(QtGui.QDialog, Ui_EventTypeListEditor):
    def __init__(self, parent, filter=None):
        QtGui.QDialog.__init__(self, parent)
        self.tableModel = CEventTypeTableModel(self)
        self.tableSelectionModel = QtGui.QItemSelectionModel(self.tableModel, self)
        self.tableSelectionModel.setObjectName('tableSelectionModel')
        self.setupUi(self)
        self.tblEventTypeList.setModel(self.tableModel)
        self.tblEventTypeList.setSelectionModel(self.tableSelectionModel)
        self.tblEventTypeList.installEventFilter(self)
        self.tblEventTypeList.setSortingEnabled(True)
        self._parent = parent
        self.eventTypeIdList =  []
        self.filter = filter
        self.tblEventTypeList.model().setIdList(self.setEventTypeList())


    def setEventTypeList(self):
        db = QtGui.qApp.db
        tableEventType = db.table('EventType')
        cond = [tableEventType['deleted'].eq(0)]
        if self.filter:
            cond.append(self.filter)
        return db.getDistinctIdList(tableEventType, tableEventType['id'].name(),
                              where=cond,
                              order=u'EventType.code ASC, EventType.name ASC')


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Ok:
            self.getEventTypeList()
        elif buttonCode == QtGui.QDialogButtonBox.Cancel:
            self.close()


    def getEventTypeList(self):
        eventTypeIdList = self.tblEventTypeList.selectedItemIdList()
        self.eventTypeIdList = eventTypeIdList
        self.close()


    def values(self):
        return self.eventTypeIdList


    def setValue(self, eventTypeIdList):
        self.eventTypeIdList = eventTypeIdList



class CEventTypePurposeListEditorDialog(QtGui.QDialog, Ui_EventTypeListEditor):
    def __init__(self, parent, filter=None):
        QtGui.QDialog.__init__(self, parent)
        self.tableModel = CEventTypePurposeTableModel(self)
        self.tableSelectionModel = QtGui.QItemSelectionModel(self.tableModel, self)
        self.tableSelectionModel.setObjectName('tableSelectionModel')
        self.setupUi(self)
        self.tblEventTypeList.setModel(self.tableModel)
        self.tblEventTypeList.setSelectionModel(self.tableSelectionModel)
        self.tblEventTypeList.installEventFilter(self)
        self.eventTypePurposeIdList = []
        self.filter = filter
        self.tblEventTypeList.model().setIdList(QtGui.qApp.db.getIdList('rbEventTypePurpose', 'id'))
        self.setWindowTitle(u'Назначение типов событий')


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Ok:
            self.eventTypePurposeIdList = self.tblEventTypeList.selectedItemIdList()
        self.close()


    def values(self):
        return self.eventTypePurposeIdList


    def setValue(self, eventTypePurposeIdList):
        self.eventTypePurposeIdList = eventTypePurposeIdList


def formatEventTypeIdList(eventTypeIdList):
    if not eventTypeIdList:
        return u''
    db = QtGui.qApp.db
    tableET = db.table('EventType')
    records = db.getRecordList(tableET, [tableET['name']], [tableET['deleted'].eq(0), tableET['id'].inlist(eventTypeIdList)])
    nameList = []
    for record in records:
        nameList.append(forceString(record.value('name')))
    return u', '.join(name for name in nameList if name)

