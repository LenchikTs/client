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

from library.interchange import getCheckBoxValue, getLineEditValue, getRBComboBoxValue, getTextEditValue, setRBComboBoxValue, setTextEditValue, setCheckBoxValue
from library.Utils       import forceBool, forceDate, forceDateTime, forceRef, forceString, toVariant, trim

from Events.Utils        import (checkUniqueEventExternalId,
#                                 getActionTypeIdListByFlatCode,
                                 getEventCounterId,
                                 getEventIsExternal,
                                 getEventShowTime,
                                 hasEventAssistant,
                                 hasEventCurator,
#                                 getEventTypeForm,
                                )
from Orgs.OrgComboBox    import CPolyclinicComboBox
from Orgs.Orgs           import selectOrganisation
from Users.Rights        import urEditClosedEvent, urEditEventExpertise, urCanChangeEventExpose, urEditClosedEventCash

from Events.Ui_EventNotesPage   import Ui_EventNotesPageWidget


class CEventNotesPage(QtGui.QWidget, Ui_EventNotesPageWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.setFocusProxy(self.edtEventNote)
        self._externalIdIsChanged = False
        self.cmbCureType.setTable('rbCureType')
        self.cmbCureMethod.setTable('rbCureMethod')
        self.chkIsClosed.setEnabled(False)
        self.eventEditor = None
        self.edtExpertiseDate.setDate(QDate())
        self.btnAttachedFiles.setTable('Event_FileAttach')
        self.setCheckedChkExpose(True)
        self.chkExpose.setEnabled(QtGui.qApp.userHasRight(urCanChangeEventExpose))
        self.cmbRelegateOrg.setFilter('isMedical != 0 and deleted = 0 and isActive = 1')

        self._eventSetDate = QDate()


    def protectFromEdit(self, isProtected):
        widgets = [self.lblEventIdValue,
                  self.edtEventExternalIdValue,
                  self.cmbClientRelationConsents,
                  self.cmbRelegateOrg, self.btnSelectRelegateOrg,
                  self.cmbRelegatePerson,
                  self.cmbEventAssistant,
                  self.cmbEventCurator,
                  self.lblEventCreateDateTimeValue,
                  self.lblEventCreatePersonValue,
                  self.lblEventModifyDateTimeValue,
                  self.lblEventModifyPersonValue,
                  self.cmbPatientModel,
                  self.cmbCureType,
                  self.cmbCureMethod, self.chkIsClosed,
                  self.edtEventNote,self.edtEventSrcDate,self.edtEventSrcNumber
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
        relegateOrgId = forceRef(record.value('relegateOrg_id'))
        self.cmbRelegateOrg.setValue(relegateOrgId)
        self.cmbRelegatePerson.setOrganisationId(relegateOrgId)
        self.edtEventSrcNumber.setText(forceString(record.value('srcNumber')))
        self.edtEventSrcDate.setDate(forceDate(record.value('srcDate')))
        self.edtExpertiseDate.setDate(forceDate(record.value('expertiseDate')))
        self.cmbExpertPerson.setValue(forceRef(record.value('expert_id')))
        self.cmbRelegatePerson.setValue(forceRef(record.value('relegatePerson_id')))
        self.setId(self.lblEventIdValue, record, 'id')
        self.setId(self.edtEventExternalIdValue, record, 'externalId')
        setRBComboBoxValue(self.cmbEventAssistant, record, 'assistant_id')
        setRBComboBoxValue(self.cmbEventCurator, record, 'curator_id')
        self.setDateTime(self.lblEventCreateDateTimeValue, record, 'createDatetime')
        self.setPerson(self.lblEventCreatePersonValue, record, 'createPerson_id')
        self.setDateTime(self.lblEventModifyDateTimeValue, record, 'modifyDatetime')
        self.setPerson(self.lblEventModifyPersonValue, record, 'modifyPerson_id')
        setTextEditValue(self.edtEventNote, record, 'note')
        setCheckBoxValue(self.chkExpose, record, 'expose')
        clientId = forceRef(record.value('client_id'))
        self.cmbClientRelationConsents.setClientId(clientId)
        self.cmbClientRelationConsents.setValue(forceRef(record.value('relative_id')))
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
        self.chkExpose.setEnabled(QtGui.qApp.userHasRight(urCanChangeEventExpose))

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
        
        
    def setCheckedChkExpose(self, value):
        self.chkExpose.setChecked(value)


    def setEnabledChkCloseEvent(self, date):
        enableEdit = False
        if date:
            enableEdit = QtGui.qApp.userHasRight(urEditClosedEvent) or QtGui.qApp.userHasRight(urEditClosedEventCash)
        self.chkIsClosed.setEnabled(enableEdit)


    def setEnabledExpertiseEvent(self):
        enableEdit = QtGui.qApp.userHasRight(urEditEventExpertise)
        self.edtExpertiseDate.setEnabled(enableEdit)
        self.cmbExpertPerson.setEnabled(enableEdit)


    def setNotesEx(self, externalId, assistantId, curatorId, relegateOrgId, relegatePersonId, clientId, relegateInfo):
        self.cmbRelegateOrg.setValue(relegateOrgId)
        self.cmbRelegatePerson.setOrganisationId(relegateOrgId)
        self.cmbRelegatePerson.setValue(relegatePersonId)
        if relegateInfo:
            if not relegatePersonId and relegateInfo[0]:
                eventNote = forceString(self.edtEventNote.toPlainText())
                self.edtEventNote.setPlainText((eventNote + u'\n' + u'< Направитель: ' + relegateInfo[0] + u' >') if eventNote else (u'< Направитель: ' + relegateInfo[0] + u' >'))
            self.edtEventSrcNumber.setText(relegateInfo[1])
            self.edtEventSrcDate.setDate(relegateInfo[2])
        self.edtEventExternalIdValue.setText(externalId if externalId else '')
        self.cmbEventAssistant.setValue(assistantId)
        self.cmbEventCurator.setValue(curatorId)
        self.cmbClientRelationConsents.setClientId(clientId)
        self.setEnabledExpertiseEvent()
# этот вариант падает в случае формы 001.
# я думаю, что он в достаточной степени крив, чтобы
# сказать что пусть лучше поле останется доступным для редактирования
# чем исправлять такое...
#        disabledIdList = []
#        disabledIdList.extend(getActionTypeIdListByFlatCode(u'received%'))
#        disabledIdList.extend(getActionTypeIdListByFlatCode(u'planning%'))
#        if disabledIdList:
#            isActionType = False
#            for model in (self.eventEditor.tabStatus.modelAPActions,
#                          self.eventEditor.tabDiagnostic.modelAPActions,
#                          self.eventEditor.tabCure.modelAPActions,
#                          self.eventEditor.tabMisc.modelAPActions):
#                for actionTypeId in model.actionTypeIdList:
#                    if actionTypeId in disabledIdList:
#                        self.edtEventSrcDate.setEnabled(False)
#                        self.edtEventSrcNumber.setEnabled(False)
#                        self.cmbRelegateOrg.setEnabled(False)
#                        self.cmbRelegatePerson.setEnabled(False)
#                        isActionType = True
#                        break
#                if isActionType:
#                    break


    def enableEditors(self, eventTypeId):
        def _isExternalIdEnabled():
            result = getEventIsExternal(eventTypeId)
            result = result and not forceBool(QtGui.qApp.db.translate('rbCounter', 'id',
                                                                      getEventCounterId(eventTypeId), 'sequenceFlag'))
            return result
        self.edtEventExternalIdValue.setEnabled(_isExternalIdEnabled())
        self.cmbEventAssistant.setEnabled(hasEventAssistant(eventTypeId))
        self.cmbEventCurator.setEnabled(hasEventCurator(eventTypeId))


    def getNotes(self, record, eventTypeId):
        record.setValue('relegateOrg_id', toVariant(self.cmbRelegateOrg.value()))
        record.setValue('relegatePerson_id', toVariant(self.cmbRelegatePerson.value()))
        record.setValue('srcNumber', toVariant(self.edtEventSrcNumber.text()))
        record.setValue('srcDate', toVariant(self.edtEventSrcDate.date()))
        getTextEditValue(self.edtEventNote, record, 'note')
        if getEventIsExternal(eventTypeId):
            getLineEditValue(self.edtEventExternalIdValue, record, 'externalId')
        if hasEventAssistant(eventTypeId):
            getRBComboBoxValue(self.cmbEventAssistant, record, 'assistant_id')
        if hasEventCurator(eventTypeId):
            getRBComboBoxValue(self.cmbEventCurator, record, 'curator_id')
        getRBComboBoxValue(self.cmbPatientModel, record, 'patientModel_id')
        getRBComboBoxValue(self.cmbCureType, record, 'cureType_id')
        getRBComboBoxValue(self.cmbCureMethod, record, 'cureMethod_id')
        getCheckBoxValue(self.chkIsClosed, record, 'isClosed')
        getCheckBoxValue(self.chkExpose, record, 'expose')
        record.setValue('relative_id', toVariant(self.cmbClientRelationConsents.value()))
        record.setValue('expertiseDate', toVariant(self.edtExpertiseDate.date()))
        record.setValue('expert_id', toVariant(self.cmbExpertPerson.value()))


    def saveAttachedFiles(self, eventId):
        self.btnAttachedFiles.saveItems(eventId)


    def checkEventExternalId(self, date, eventId):
        if self._externalIdIsChanged:
            externalId = trim(self.edtEventExternalIdValue.text())
            if bool(externalId):
                eventTypeId = self.eventEditor.eventTypeId
                sameExternalIdListInfo = checkUniqueEventExternalId(externalId, eventTypeId, date, eventId)
                return sameExternalIdListInfo
        return []


    @pyqtSignature('')
    def on_btnSelectRelegateOrg_clicked(self):
        orgId = selectOrganisation(self, self.cmbRelegateOrg.value(), False, filter=CPolyclinicComboBox.filter)
        self.cmbRelegateOrg.updateModel()
        if orgId:
            self.cmbRelegateOrg.setValue(orgId)
            self.cmbRelegatePerson.setOrganisationId(orgId)

    @pyqtSignature('int')
    def on_cmbRelegateOrg_currentIndexChanged(self):
        orgId = self.cmbRelegateOrg.value()
        self.cmbRelegatePerson.setOrganisationId(orgId)

    @pyqtSignature('QString')
    def on_edtEventExternalIdValue_textEdited(self, value):
        self._externalIdIsChanged = True
        if self.eventEditor:
            self.eventEditor.setExternalId(self.edtEventExternalIdValue.text())


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


    @pyqtSignature('int')
    def on_cmbClientRelationConsents_currentIndexChanged(self, index):
        if hasattr(self.eventEditor,  "tabFeed"):
            relationId = self.cmbClientRelationConsents.value()
            self.eventEditor.tabFeed.setPatronId(relationId)
            db = QtGui.qApp.db
            tableClient = db.table('Client')
            record = db.getRecordEx(tableClient, ['''CONCAT_WS(' ', Client.lastName, Client.firstName,
    Client.patrName, CAST( Client.id AS CHAR)) AS patronName'''], [tableClient['deleted'].eq(0), tableClient['id'].eq(relationId)])
            patronName = forceString(record.value('patronName')) if record else u'не определен'
            self.eventEditor.tabFeed.lblPatronName.setText(u'Основное лицо по уходу: ' + patronName)
        if hasattr(self.eventEditor,  "tabClientData") and hasattr(self.eventEditor,  "cmbClientRelationRepresentative"):
            self.eventEditor.cmbClientRelationRepresentative.setValue(self.cmbClientRelationConsents.value())


    def getExternalId(self):
        return forceString(self.edtEventExternalIdValue.text())


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

