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

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QEvent, pyqtSignature, SIGNAL
from library.Utils import getPref, setPref

from Events.EventTypeModel import CEventTypeTableModel
from Events.Ui_EventTypeComboBoxExPopup import Ui_EventTypeComboBoxExPopup


class CEventTypeComboBoxExPopup(QtGui.QFrame, Ui_EventTypeComboBoxExPopup):

    def __init__(self, parent = None):
        QtGui.QFrame.__init__(self, parent, Qt.Popup)
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setAttribute(Qt.WA_WindowPropagation)
        self.tableModel = CEventTypeTableModel(self)
        self.tableSelectionModel = QtGui.QItemSelectionModel(self.tableModel, self)
        self.tableSelectionModel.setObjectName('tableSelectionModel')
        self.setupUi(self)
        self.tblEventTypeList.setModel(self.tableModel)
        self.tblEventTypeList.setSelectionModel(self.tableSelectionModel)
        self.tblEventTypeList.installEventFilter(self)
        preferences = getPref(QtGui.qApp.preferences.windowPrefs, 'CEventTypeComboBoxExPopup', {})
        self.tblEventTypeList.loadPreferences(preferences)
        self._parent = parent
        self.eventTypeIdList =  []
        self.tblEventTypeList.model().setIdList(self.setEventTypeList())


    def mousePressEvent(self, event):
        parent = self.parentWidget()
        if parent!=None:
            opt=QtGui.QStyleOptionComboBox()
            opt.init(parent)
            arrowRect = parent.style().subControlRect(
                QtGui.QStyle.CC_ComboBox, opt, QtGui.QStyle.SC_ComboBoxArrow, parent)
            arrowRect.moveTo(parent.mapToGlobal(arrowRect.topLeft()))
            if (arrowRect.contains(event.globalPos()) or self.rect().contains(event.pos())):
                self.setAttribute(Qt.WA_NoMouseReplay)
        QtGui.QFrame.mousePressEvent(self, event)


    def closeEvent(self, event):
        preferences = self.tblEventTypeList.savePreferences()
        setPref(QtGui.qApp.preferences.windowPrefs, 'CEventTypeComboBoxExPopup', preferences)
        QtGui.QFrame.closeEvent(self, event)


    def eventFilter(self, watched, event):
        if watched == self.tblEventTypeList:
            if event.type() == QEvent.KeyPress and event.key() in (Qt.Key_Return, Qt.Key_Enter, Qt.Key_Select):
                event.accept()
                index = self.tblEventTypeList.currentIndex()
                self.tblEventTypeList.emit(SIGNAL('doubleClicked(QModelIndex)'), index)
                return True
        return QtGui.QFrame.eventFilter(self, watched, event)


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


    def setEventTypeList(self):
        db = QtGui.qApp.db
        tableEventType = db.table('EventType')
        cond = [tableEventType['deleted'].eq(0)]
        return db.getDistinctIdList(tableEventType, tableEventType['id'].name(),
                              where=cond,
                              order=u'EventType.code ASC, EventType.name ASC')

