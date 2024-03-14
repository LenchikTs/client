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

from library.interchange       import getTextEditValue, setTextEditValue
from library.Utils             import forceDate, forceRef, forceString

from Users.Rights              import urEditClosedEvent

from F027.Ui_EventNotesPageProtocol import Ui_EventNotesPageWidget


class CEventNotesPageProtocol(QtGui.QWidget, Ui_EventNotesPageWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setFocusProxy(self.edtEventNote)
        self._externalIdIsChanged = False


    @staticmethod
    def setId(widget, record, fieldName):
        value = forceString(record.value(fieldName))
        if value:
            text = unicode(value)
        else:
            text = ''
        widget.setText(text)


    @staticmethod
    def setDateTime(widget, record, fieldName):
        value = record.value(fieldName).toDateTime()
        if value:
            text = value.toString('dd.MM.yyyy hh:mm:ss')
        else:
            text = ''
        widget.setText(text)


    @staticmethod
    def setPerson(widget, record, fieldName):
        personId = forceRef(record.value(fieldName))
        if personId:
            record = QtGui.qApp.db.getRecord('vrbPersonWithSpeciality', 'code, name', personId)
            if record:
                text = forceString(record.value('code'))+ ' | ' + forceString(record.value('name'))
            else:
                text = '{%d}' % personId
        else:
            text = ''
        widget.setText(text)

    def isEventClosed(self):
        return self.chkIsClosed.isChecked()

    def setNotes(self, record):
        self.setId(self.lblEventIdValue, record, 'id')
        self.setDateTime(self.lblEventCreateDateTimeValue, record, 'createDatetime')
        self.setPerson(self.lblEventCreatePersonValue, record, 'createPerson_id')
        self.setDateTime(self.lblEventModifyDateTimeValue, record, 'modifyDatetime')
        self.setPerson(self.lblEventModifyPersonValue, record, 'modifyPerson_id')
        setTextEditValue(self.edtEventNote, record, 'note')
        execDate = forceDate(record.value('execDate'))
        self.setEnabledChkCloseEvent(execDate)
        self.setCheckedChkCloseEvent(execDate)


    def getNotes(self, record, eventTypeId):
        getTextEditValue(self.edtEventNote, record, 'note')


    def checkEventExternalId(self, date, eventId):
        return []


    def enableEditors(self, eventTypeId):
        pass


    def setCheckedChkCloseEvent(self, date):
        self.chkIsClosed.setChecked(bool(date))


    def setEnabledChkCloseEvent(self, date):
        enableEdit = False
        if date:
            enableEdit = QtGui.qApp.userHasRight(urEditClosedEvent)
        self.chkIsClosed.setEnabled(enableEdit)


    def protectFromEdit(self, isProtected):
        widgets = [self.chkIsClosed,
                   self.edtEventNote
                  ]
        for widget in widgets:
            widget.setEnabled(not isProtected)

