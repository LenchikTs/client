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
from PyQt4.QtCore import Qt, pyqtSignature

from library.Utils import forceString

from Registry.Ui_UpdateEventTypeByEvent import Ui_UpdateEventTypeByEvent


class CUpdateEventTypeByEvent(QtGui.QDialog, Ui_UpdateEventTypeByEvent):
    def __init__(self,  parent, eventTypeIdList, eventTypeId):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.eventTypeIdList = eventTypeIdList
        filterNew = ('''id IN (%s) '''%((u','.join(forceString(tmpEventTypeId) for tmpEventTypeId in self.eventTypeIdList)))) if self.eventTypeIdList else ''
        self.cmbEventType.setTable('EventType', True, filter=filterNew)
        self.setNewEventTypeId(eventTypeId)


    def setNewEventTypeId(self, eventTypeId):
        self.cmbEventType.setValue(eventTypeId)


    def getNewEventTypeId(self):
        return self.cmbEventType.value()


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Ok:
            self.getNewEventTypeId()
        elif buttonCode == QtGui.QDialogButtonBox.Cancel:
            self.close()
