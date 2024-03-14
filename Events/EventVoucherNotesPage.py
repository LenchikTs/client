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
from PyQt4.QtCore import pyqtSignature, QDate, QTime, SIGNAL

from library.interchange import getCheckBoxValue, getRBComboBoxValue, getTextEditValue, setRBComboBoxValue, setTextEditValue
from library.Utils       import forceBool, forceDate, forceDateTime, forceRef, forceString, toVariant

from Events.Utils        import (getEventCounterId,
                                 getEventIsExternal,
                                 getEventShowTime,
                                 hasEventAssistant,
                                 hasEventCurator,
                                )
#from Orgs.OrgComboBox    import CPolyclinicComboBox
#from Orgs.Orgs           import selectOrganisation
from Users.Rights        import urEditClosedEvent, urEditEventExpertise

from Events.Ui_EventVoucherNotesPage   import Ui_EventVoucherNotesPageWidget


class CEventVoucherNotesPage(QtGui.QWidget, Ui_EventVoucherNotesPageWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setFocusProxy(self.edtEventNote)
        self.cmbCureType.setTable('rbCureType')
        self.cmbCureMethod.setTable('rbCureMethod')
        self.chkIsClosed.setEnabled(False)
        self.eventEditor = None
        self.edtExpertiseDate.setDate(QDate())
        self.btnAttachedFiles.setTable('Event_FileAttach')
        self._eventSetDate = QDate()


    def protectFromEdit(self, isProtected):
        widgets = [self.lblEventIdValue,
                  self.cmbEventAssistant,
                  self.cmbEventCurator,
                  self.lblEventCreateDateTimeValue,
                  self.lblEventCreatePersonValue,
                  self.lblEventModifyDateTimeValue,
                  self.lblEventModifyPersonValue,
                  self.cmbPatientModel,
                  self.cmbCureType,
                  self.cmbCureMethod, self.chkIsClosed,
                  self.edtEventNote
                 ]
        for widget in widgets:
            widget.setEnabled(not isProtected)
        enableEdit = QtGui.qApp.userHasRight(urEditEventExpertise)
        for widget in [self.edtExpertiseDate, self.cmbExpertPerson]:
            widget.setEnabled(enableEdit and not isProtected)
        if not isProtected:
            self.enableEditors(self.eventEditor.eventTypeId)


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
#                text = value.toString(Qt.DefaultLocaleLongDate)
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
                text = '{'+str(personId)+'}'
        else:
            text = ''
        widget.setText(text)


    def isEventClosed(self):
        return self.chkIsClosed.isChecked()


    def setNotes(self, record):
        from F110.F110Dialog import CF110Dialog
        self.edtExpertiseDate.setDate(forceDate(record.value('expertiseDate')))
        self.cmbExpertPerson.setValue(forceRef(record.value('expert_id')))
        self.setId(self.lblEventIdValue, record, 'id')
        setRBComboBoxValue(self.cmbEventAssistant, record, 'assistant_id')
        setRBComboBoxValue(self.cmbEventCurator, record, 'curator_id')
        self.setDateTime(self.lblEventCreateDateTimeValue, record, 'createDatetime')
        self.setPerson(self.lblEventCreatePersonValue, record, 'createPerson_id')
        self.setDateTime(self.lblEventModifyDateTimeValue, record, 'modifyDatetime')
        self.setPerson(self.lblEventModifyPersonValue, record, 'modifyPerson_id')
        setTextEditValue(self.edtEventNote, record, 'note')
#        clientId = forceRef(record.value('client_id'))
        execDateTime = forceDateTime(record.value('execDate'))
        execDate = execDateTime.date()
        if getEventShowTime(self.eventEditor.eventTypeId):
            if isinstance(self.eventEditor, CF110Dialog):
                execTime = execDateTime.time()
                if execTime == QTime() or execTime == QTime(0, 0):
                    execDate = QDate()
        self.setEnabledChkCloseEvent(execDate)
        self.setCheckedChkCloseEvent(execDate)
        self.setEnabledExpertiseEvent()
        self.btnAttachedFiles.loadItems(forceRef(record.value('id')))

        setDate = forceDate(record.value('setDate'))
        self.updateFilters(setDate)
        setRBComboBoxValue(self.cmbPatientModel, record, 'patientModel_id')
        setRBComboBoxValue(self.cmbCureType,     record, 'cureType_id')
        setRBComboBoxValue(self.cmbCureMethod,   record, 'cureMethod_id')

        if hasattr(self.eventEditor, 'edtBegDate'):
            self.connect(self.eventEditor.edtBegDate,
                         SIGNAL('dateChanged(const QDate &)'),
                         self.on_edtBegDate_dateChanged)


    def setCheckedChkCloseEvent(self, date):
        self.chkIsClosed.setChecked(bool(date))


    def setEnabledChkCloseEvent(self, date):
        enableEdit = False
        if date:
            enableEdit = QtGui.qApp.userHasRight(urEditClosedEvent)
        self.chkIsClosed.setEnabled(enableEdit)


    def setEnabledExpertiseEvent(self):
        enableEdit = QtGui.qApp.userHasRight(urEditEventExpertise)
        self.edtExpertiseDate.setEnabled(enableEdit)
        self.cmbExpertPerson.setEnabled(enableEdit)


    def setNotesEx(self, assistantId, curatorId):
        self.cmbEventAssistant.setValue(assistantId)
        self.cmbEventCurator.setValue(curatorId)
        self.setEnabledExpertiseEvent()


    def enableEditors(self, eventTypeId):
        def _isExternalIdEnabled():
            result = getEventIsExternal(eventTypeId)
            result = result and not forceBool(QtGui.qApp.db.translate('rbCounter', 'id',
                                                                      getEventCounterId(eventTypeId), 'sequenceFlag'))
            return result
        self.eventEditor.edtEventExternalIdValue.setEnabled(_isExternalIdEnabled())
        self.cmbEventAssistant.setEnabled(hasEventAssistant(eventTypeId))
        self.cmbEventCurator.setEnabled(hasEventCurator(eventTypeId))


    def getNotes(self, record, eventTypeId):
        getTextEditValue(self.edtEventNote, record, 'note')
        if hasEventAssistant(eventTypeId):
            getRBComboBoxValue(self.cmbEventAssistant, record, 'assistant_id')
        if hasEventCurator(eventTypeId):
            getRBComboBoxValue(self.cmbEventCurator, record, 'curator_id')
        getRBComboBoxValue(self.cmbPatientModel, record, 'patientModel_id')
        getRBComboBoxValue(self.cmbCureType, record, 'cureType_id')
        getRBComboBoxValue(self.cmbCureMethod, record, 'cureMethod_id')
        getCheckBoxValue(self.chkIsClosed, record, 'isClosed')
        record.setValue('expertiseDate', toVariant(self.edtExpertiseDate.date()))
        record.setValue('expert_id', toVariant(self.cmbExpertPerson.value()))


    def saveAttachedFiles(self, eventId):
        self.btnAttachedFiles.saveItems(eventId)


    def setEventEditor(self, eventEditor):
        self.cmbPatientModel.setEventEditor(eventEditor)
        self.eventEditor = eventEditor


    def on_cmbPatientModel_valueChanged(self):
        patientModelId = self.cmbPatientModel.value()
        db = QtGui.qApp.db
        tablePatientModelItem = db.table('rbPatientModel_Item')
        cond = [tablePatientModelItem['master_id'].eq(patientModelId)]
        dateFilter = (u'AND (endDate IS NULL OR endDate >= %s)' % db.formatDate(
                      self._eventSetDate)
                      if self._eventSetDate.isValid() else '')
        cureTypeIdList = db.getDistinctIdList(tablePatientModelItem, [tablePatientModelItem['cureType_id']], cond)
        if cureTypeIdList:
            self.cmbCureType.setFilter('rbCureType.id IN (%s) %s'%(u','.join(str(cureTypeId) for cureTypeId in cureTypeIdList if cureTypeId), dateFilter))
            cureTypeId = self.cmbCureType.value()
            cond = [tablePatientModelItem['cureType_id'].eq(cureTypeId),
                    tablePatientModelItem['master_id'].eq(patientModelId)]
            cureMethodIdList = db.getDistinctIdList(tablePatientModelItem, [tablePatientModelItem['cureMethod_id']], cond)
            if cureMethodIdList:
                self.cmbCureMethod.setFilter('rbCureMethod.id IN (%s) %s'%(u','.join(str(cureMethodId) for cureMethodId in cureMethodIdList if cureMethodId), dateFilter))
            else:
                cond = [tablePatientModelItem['master_id'].eq(patientModelId)]
                cureMethodIdList = db.getDistinctIdList(tablePatientModelItem, [tablePatientModelItem['cureMethod_id']], cond)
                if cureMethodIdList:
                    self.cmbCureMethod.setFilter('rbCureMethod.id IN (%s) %s'%(u','.join(str(cureMethodId) for cureMethodId in cureMethodIdList if cureMethodId), dateFilter))
                else:
                    self.cmbCureMethod.setFilter('rbCureMethod.id IS NULL')
            self.cmbCureMethod.setCurrentIndex(0)
        else:
            self.cmbCureType.setFilter('rbCureType.id IS NULL')
        self.cmbCureType.setCurrentIndex(0)


    @pyqtSignature('int')
    def on_cmbCureType_currentIndexChanged(self, index):
        db = QtGui.qApp.db
        cureTypeId = self.cmbCureType.value()
        patientModelId = self.cmbPatientModel.value()
        tablePatientModelItem = db.table('rbPatientModel_Item')
        dateFilter = (u'AND (endDate IS NULL OR endDate >= %s)' % db.formatDate(
                      self._eventSetDate)
                      if self._eventSetDate.isValid() else '')
        if cureTypeId:
            cond = [tablePatientModelItem['cureType_id'].eq(cureTypeId),
                    tablePatientModelItem['master_id'].eq(patientModelId)]
            cureMethodIdList = db.getDistinctIdList(tablePatientModelItem, [tablePatientModelItem['cureMethod_id']], cond)
            if cureMethodIdList:
                self.cmbCureMethod.setFilter('rbCureMethod.id IN (%s) %s'%(u','.join(str(cureMethodId) for cureMethodId in cureMethodIdList if cureMethodId), dateFilter))
            else:
                self.cmbCureMethod.setFilter('rbCureMethod.id IS NULL')
        elif patientModelId:
            cond = [tablePatientModelItem['master_id'].eq(patientModelId)]
            cureMethodIdList = db.getDistinctIdList(tablePatientModelItem, [tablePatientModelItem['cureMethod_id']], cond)
            if cureMethodIdList:
                self.cmbCureMethod.setFilter('rbCureMethod.id IN (%s) %s'%(u','.join(str(cureMethodId) for cureMethodId in cureMethodIdList if cureMethodId), dateFilter))
            else:
                self.cmbCureMethod.setFilter('rbCureMethod.id IS NULL')
        else:
            self.cmbCureMethod.setFilter('rbCureMethod.id IS NULL')
        self.cmbCureMethod.setCurrentIndex(0)
        

    @pyqtSignature('QDate')
    def on_edtBegDate_dateChanged(self, date):
        self.updateFilters(date)


    def updateFilters(self, date):
        u'Обновляет списки методов, видов лечения и модели пациента с по дате'
        self._eventSetDate = date
        self.cmbPatientModel.setDateFilter(date)
        self.on_cmbPatientModel_valueChanged()


    @pyqtSignature('QDate')
    def on_edtExpertiseDate_dateChanged(self, date):
        if not self.cmbExpertPerson.value() and date and QtGui.qApp.userHasRight(urEditEventExpertise):
            self.cmbExpertPerson.setValue(QtGui.qApp.userId)

