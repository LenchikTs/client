# -*- coding: utf-8 -*-
#############################################################################
##
# Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
# Copyright (C) 2012-2023 SAMSON Group. All rights reserved.
##
#############################################################################
##
# Это программа является свободным программным обеспечением.
# Вы можете использовать, распространять и/или модифицировать её согласно
# условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4                    import QtGui
from PyQt4.QtCore             import Qt, QVariant, SIGNAL, pyqtSignature, QDate

from Events.ActionInfo            import CActionInfoProxyList, CActionSelectedInfoProxyList
from Events.Action                import CAction
from Events.ActionPropertiesTable import CActionPropertiesTableModel
from Events.ActionStatus          import CActionStatus
from Events.ActionTypeCol         import CActionTypeCol
from Events.Utils                 import setActionPropertiesColumnVisible, getActionTypeDescendants
from Orgs.PersonComboBoxEx import CPersonFindInDocTableCol
from Orgs.Utils                   import getOrgStructurePersonIdList
from Registry.Utils               import CClientInfo
from Registry.ProphylaxisPlanningInfo import CProphylaxisPlanningInfoProxyList
from library.Attach.AttachButton import CAttachButton
from library.InDocTable           import (CDateInDocTableCol,
                                          CInDocTableCol,
                                          CRBInDocTableCol,
                                          CInDocTableModel
                                          )
from library.TableModel       import CTableModel, CDateCol, CTextCol, CBoolCol, CEnumCol, CRefBookCol
from library.ItemsListDialog  import CItemEditorBaseDialog
from library.ICDInDocTableCol import CICDExInDocTableCol
from library.DialogBase       import CDialogBase
from library.database         import CTableRecordCache
from library.PrintTemplates   import getPrintButton, applyTemplate
from library.PrintInfo        import CInfoContext
from library.Utils            import forceDate, forceRef, forceStringEx, toVariant, forceInt, forceString, calcAgeTuple

from Surveillance.Ui_SurveillancePlanningCardDialog import Ui_SurveillancePlanningCardDialog

# Планирование Диспансерного наблюдения - Контрольная карта #CSurveillancePlanningCard


class CSurveillancePlanningCard(CItemEditorBaseDialog, Ui_SurveillancePlanningCardDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, 'Diagnostic')
        self.eventEditor = None
        self.addModels('PlanningSurveillance', CPlanningSurveillanceCardModel(self))
        self.addModels('ControlSurveillance', CControlSurveillanceCardModel(self))
        self.addModels('MeasuresStatusActions', CMeasuresActionsCheckTableModel(self))
        self.addModels('MeasuresStatusActionProperties', CActionPropertiesTableModel(self))
        self.addModels('MeasuresDiagnosticActions', CMeasuresActionsCheckTableModel(self))
        self.addModels('MeasuresDiagnosticActionProperties', CActionPropertiesTableModel(self))
        self.addModels('MeasuresCureActions', CMeasuresActionsCheckTableModel(self))
        self.addModels('MeasuresCureActionProperties', CActionPropertiesTableModel(self))
        self.addModels('MeasuresMiscActions', CMeasuresActionsCheckTableModel(self))
        self.addModels('MeasuresMiscActionProperties', CActionPropertiesTableModel(self))
        self.addObject('btnPrint', getPrintButton(self, 'surveillancePlanningCard', u'Печать'))
        self.addObject('btnAttachedFiles', CAttachButton(self, u'Прикреплённые файлы'))
        self.btnAttachedFiles.setTable('ProphylaxisPlanning_FileAttach')
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setWindowTitleEx(u'Контрольная карта')
        self.setWindowState(Qt.WindowMaximized)
        self.grpPlanningSurveillance.setStyleSheet('QGroupBox {font-weight: bold;}')
        self.grpControlSurveillance.setStyleSheet('QGroupBox {font-weight: bold;}')
        self.grpMeasuresSurveillance.setStyleSheet('QGroupBox {font-weight: bold;}')
        self.planningSurveillanceRecord = None
        self.controlSurveillanceItems = []
        self.MKB = u''
        self.clientId = None
        self.clientSex       = None
        self.clientBirthDate = None
        self.clientAge       = None
        self.eventId = None
        self.measuresBegDate = None
        self.measuresEndDate = None
        self.MKBList = []
        self.prophylaxisPlanningTypeId = self.getProphylaxisPlanningType()
        self.tblPlanningSurveillance.setModel(self.modelPlanningSurveillance)
        self.tblPlanningSurveillance.setSelectionModel(self.selectionModelPlanningSurveillance)
        self.tblControlSurveillance.setModel(self.modelControlSurveillance)
        self.setModels(self.tblMeasuresStatusActions, self.modelMeasuresStatusActions, self.selectionModelMeasuresStatusActions)
        self.setModels(self.tblMeasuresStatusActionProperties, self.modelMeasuresStatusActionProperties, self.selectionModelMeasuresStatusActionProperties)
        self.setModels(self.tblMeasuresDiagnosticActions, self.modelMeasuresDiagnosticActions, self.selectionModelMeasuresDiagnosticActions)
        self.setModels(self.tblMeasuresDiagnosticActionProperties, self.modelMeasuresDiagnosticActionProperties, self.selectionModelMeasuresDiagnosticActionProperties)
        self.setModels(self.tblMeasuresCureActions, self.modelMeasuresCureActions, self.selectionModelMeasuresCureActions)
        self.setModels(self.tblMeasuresCureActionProperties, self.modelMeasuresCureActionProperties, self.selectionModelMeasuresCureActionProperties)
        self.setModels(self.tblMeasuresMiscActions, self.modelMeasuresMiscActions, self.selectionModelMeasuresMiscActions)
        self.setModels(self.tblMeasuresMiscActionProperties, self.modelMeasuresMiscActionProperties, self.selectionModelMeasuresMiscActionProperties)
        self.modelPlanningSurveillance.setEventEditor(self)
        self.modelControlSurveillance.setEventEditor(self)
        self.buttonBox.addButton(self.btnPrint, QtGui.QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.btnAttachedFiles, QtGui.QDialogButtonBox.ActionRole)
        self.btnAttachedFiles.setEnabled(True)


    def setEventEditor(self, eventEditor):
        self.eventEditor = eventEditor


    @pyqtSignature('int')
    def on_btnPrint_printByTemplate(self, templateId):
        context = CInfoContext()
        self.on_btnMeasuresStatusButtonBox_reset()
        self.on_btnMeasuresStatusButtonBox_apply()
        self.on_btnMeasuresDiagnosticButtonBox_reset()
        self.on_btnMeasuresCureButtonBox_reset()
        self.on_btnMeasuresCureButtonBox_apply()
        self.on_btnMeasuresMiscButtonBox_reset()
        self.on_btnMeasuresMiscButtonBox_apply()
        planningSurveillances = CProphylaxisPlanningInfoProxyList(context, [self.modelPlanningSurveillance])
        controlSurveillances = CProphylaxisPlanningInfoProxyList(context, [self.modelControlSurveillance])
        measuresActions = CActionInfoProxyList(context, [self.modelMeasuresStatusActions, self.modelMeasuresDiagnosticActions,
        self.modelMeasuresCureActions, self.modelMeasuresMiscActions], eventInfo=None)
        measuresActionsSelected = CActionSelectedInfoProxyList(context, [self.modelMeasuresStatusActions.getSelectedItems(), self.modelMeasuresDiagnosticActions.getSelectedItems(),
        self.modelMeasuresCureActions.getSelectedItems(), self.modelMeasuresMiscActions.getSelectedItems()], eventInfo=None)
        data = {'client': context.getInstance(CClientInfo, self.clientId, QDate.currentDate()),
                'planningSurveillances': planningSurveillances,
                'controlSurveillances': controlSurveillances,
                'measuresActions': measuresActions,
                'measuresActionsSelected': measuresActionsSelected
                }
        signAndAttachResult = applyTemplate(self, templateId, data, signAndAttachHandler=self.btnAttachedFiles.getSignAndAttachHandler())
        if signAndAttachResult:
            self.setIsDirty(True)


    def getClientActions(self, clientId, filter, classCode, order=['Action.endDate DESC', 'Action.id'], fieldName=None):
        db = QtGui.qApp.db
        tableAction = db.table('Action')
        queryTable = tableAction
        tableEvent = db.table('Event')
        queryTable = queryTable.innerJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))
        tableActionType = db.table('ActionType')
        queryTable = queryTable.leftJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
        if fieldName in [u'setPerson_id', u'person_id']:
            tableSPWS = db.table('vrbPersonWithSpeciality')
            queryTable = queryTable.leftJoin(tableSPWS, tableSPWS['id'].eq(tableAction[fieldName]))
        cond = [tableAction['deleted'].eq(0),
                tableEvent['deleted'].eq(0),
                tableEvent['client_id'].eq(clientId)]
        if not self.MKBList and not self.controlSurveillanceItems:
            return []
        tableDiagnosis = db.table('Diagnosis')
        tableDiagnostic = db.table('Diagnostic')
        tableDispanser = db.table('rbDispanser')
        queryTable = queryTable.innerJoin(tableDiagnostic, tableDiagnostic['event_id'].eq(tableEvent['id']))
        queryTable = queryTable.innerJoin(tableDiagnosis, tableDiagnosis['id'].eq(tableDiagnostic['diagnosis_id']))
        queryTable = queryTable.innerJoin(tableDispanser, tableDispanser['id'].eq(tableDiagnostic['dispanser_id']))
        cond.append(tableDiagnosis['MKB'].inlist(self.MKBList))
        cond.append(tableDiagnostic['dispanser_id'].isNotNull())
        cond.append(tableDiagnosis['deleted'].eq(0))
        cond.append(tableDiagnostic['deleted'].eq(0))
        cond.append(tableEvent['deleted'].eq(0))
        if classCode is not None:
            cond.append(tableActionType['class'].eq(classCode))
        serviceType = filter.get('serviceType', None)
        if serviceType is not None:
            cond.append(tableActionType['serviceType'].eq(serviceType))
        begDate = filter.get('begDate', None)
        if begDate:
            cond.append(db.joinOr([tableAction['endDate'].isNull(), tableAction['endDate'].dateGe(begDate)]))
        endDate = filter.get('endDate', None)
        if endDate:
            cond.append(db.joinOr([tableAction['endDate'].isNull(), tableAction['endDate'].dateLe(endDate)]))
        actionGroupId = filter.get('actionGroupId', None)
        if actionGroupId:
            cond.append(tableAction['actionType_id'].inlist(getActionTypeDescendants(actionGroupId, classCode)))
        office = filter.get('office', '')
        if office:
            cond.append(tableAction['office'].like(office))
        orgStructureId = filter.get('orgStructureId', None)
        if orgStructureId:
            cond.append(tableAction['person_id'].inlist(getOrgStructurePersonIdList(orgStructureId)))
        try:
            QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor))
            return db.getIdList(queryTable,
                   tableAction['id'].name(),
                   cond,
                   order)
        finally:
            QtGui.QApplication.restoreOverrideCursor()


    @pyqtSignature('int')
    def on_tabMeasuresContent_currentChanged(self, index):
        widget = self.tabMeasuresContent.widget(index)
        if widget is not None:
            focusProxy = widget.focusProxy()
            if focusProxy:
                focusProxy.setFocus(Qt.OtherFocusReason)
        if index == 0:
            self.on_btnMeasuresStatusButtonBox_reset()
            self.on_btnMeasuresStatusButtonBox_apply()
        elif index == 1:
            self.on_btnMeasuresDiagnosticButtonBox_reset()
            self.on_btnMeasuresDiagnosticButtonBox_apply()
        elif index == 2:
            self.on_btnMeasuresCureButtonBox_reset()
            self.on_btnMeasuresCureButtonBox_apply()
        elif index == 3:
            self.on_btnMeasuresMiscButtonBox_reset()
            self.on_btnMeasuresMiscButtonBox_apply()


    def selectMeasuresActions(self, filter, classCode, order, fieldName):
        return self.getClientActions(self.clientId, filter, classCode, order, fieldName)


    def getMeasuresFilter(self, edtBegDate, edtEndDate, cmbGroup, edtOffice, cmbOrgStructure):
        filter = {}
        filter['begDate'] = edtBegDate.date()
        filter['endDate'] = edtEndDate.date()
        filter['actionGroupId'] = cmbGroup.value()
        filter['office'] = forceString(edtOffice.text())
        filter['orgStructureId'] = cmbOrgStructure.value()
        return filter


    def resetMeasuresFilter(self, edtBegDate, edtEndDate, cmbGroup, edtOffice, cmbOrgStructure):
        edtBegDate.setDate(self.measuresBegDate)
        edtEndDate.setDate(self.measuresEndDate)
        cmbGroup.setValue(None)
        edtOffice.setText('')
        cmbOrgStructure.setValue(None)


    @pyqtSignature('QAbstractButton*')
    def on_btnMeasuresStatusButtonBox_clicked(self, button):
        buttonCode = self.btnMeasuresStatusButtonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Apply:
            self.on_btnMeasuresStatusButtonBox_apply()
        elif buttonCode == QtGui.QDialogButtonBox.Reset:
            self.on_btnMeasuresStatusButtonBox_reset()


    @pyqtSignature('QAbstractButton*')
    def on_btnMeasuresDiagnosticButtonBox_clicked(self, button):
        buttonCode = self.btnMeasuresDiagnosticButtonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Apply:
            self.on_btnMeasuresDiagnosticButtonBox_apply()
        elif buttonCode == QtGui.QDialogButtonBox.Reset:
            self.on_btnMeasuresDiagnosticButtonBox_reset()


    @pyqtSignature('QAbstractButton*')
    def on_btnMeasuresCureButtonBox_clicked(self, button):
        buttonCode = self.btnMeasuresCureButtonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Apply:
            self.on_btnMeasuresCureButtonBox_apply()
        elif buttonCode == QtGui.QDialogButtonBox.Reset:
            self.on_btnMeasuresCureButtonBox_reset()


    @pyqtSignature('QAbstractButton*')
    def on_btnMeasuresMiscButtonBox_clicked(self, button):
        buttonCode = self.btnMeasuresMiscButtonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Apply:
            self.on_btnMeasuresMiscButtonBox_apply()
        elif buttonCode == QtGui.QDialogButtonBox.Reset:
            self.on_btnMeasuresMiscButtonBox_reset()


    def on_btnMeasuresDiagnosticButtonBox_reset(self):
        self.resetMeasuresFilter(
            self.edtMeasuresDiagnosticBegDate,
            self.edtMeasuresDiagnosticEndDate,
            self.cmbMeasuresDiagnosticGroup,
            self.edtMeasuresDiagnosticOffice,
            self.cmbMeasuresDiagnosticOrgStructure
        )


    def on_btnMeasuresDiagnosticButtonBox_apply(self):
        filter = self.getMeasuresFilter(
            self.edtMeasuresDiagnosticBegDate,
            self.edtMeasuresDiagnosticEndDate,
            self.cmbMeasuresDiagnosticGroup,
            self.edtMeasuresDiagnosticOffice,
            self.cmbMeasuresDiagnosticOrgStructure
        )
        self.updateMeasuresDiagnostic(filter)
        self.focusMeasuresDiagnosticActions()


    def updateMeasuresDiagnostic(self, filter, posToId=None, fieldName=None):
        self.__measuresDiagnosticFilter = filter
        order = self.tblMeasuresDiagnosticActions.order() if self.tblMeasuresDiagnosticActions.order() else ['Action.endDate DESC', 'id']
        self.tblMeasuresDiagnosticActions.setIdList(self.selectMeasuresActions(filter, 1, order, fieldName), posToId)


    def focusMeasuresDiagnosticActions(self):
        self.tblMeasuresDiagnosticActions.setFocus(Qt.TabFocusReason)


    def on_btnMeasuresStatusButtonBox_reset(self):
        self.resetMeasuresFilter(
            self.edtMeasuresStatusBegDate,
            self.edtMeasuresStatusEndDate,
            self.cmbMeasuresStatusGroup,
            self.edtMeasuresStatusOffice,
            self.cmbMeasuresStatusOrgStructure
        )


    def on_btnMeasuresCureButtonBox_reset(self):
        self.resetMeasuresFilter(
            self.edtMeasuresCureBegDate,
            self.edtMeasuresCureEndDate,
            self.cmbMeasuresCureGroup,
            self.edtMeasuresCureOffice,
            self.cmbMeasuresCureOrgStructure
        )


    def on_btnMeasuresMiscButtonBox_reset(self):
        self.resetMeasuresFilter(
            self.edtMeasuresMiscBegDate,
            self.edtMeasuresMiscEndDate,
            self.cmbMeasuresMiscGroup,
            self.edtMeasuresMiscOffice,
            self.cmbMeasuresMiscOrgStructure
        )


    def on_btnMeasuresStatusButtonBox_apply(self):
        filter = self.getMeasuresFilter(
            self.edtMeasuresStatusBegDate,
            self.edtMeasuresStatusEndDate,
            self.cmbMeasuresStatusGroup,
            self.edtMeasuresStatusOffice,
            self.cmbMeasuresStatusOrgStructure
        )
        self.updateMeasuresStatus(filter)
        self.focusMeasuresStatusActions()


    def on_btnMeasuresCureButtonBox_apply(self):
        filter = self.getMeasuresFilter(
            self.edtMeasuresCureBegDate,
            self.edtMeasuresCureEndDate,
            self.cmbMeasuresCureGroup,
            self.edtMeasuresCureOffice,
            self.cmbMeasuresCureOrgStructure
        )
        self.updateMeasuresCure(filter)
        self.focusMeasuresCureActions()


    def on_btnMeasuresMiscButtonBox_apply(self):
        filter = self.getMeasuresFilter(
            self.edtMeasuresMiscBegDate,
            self.edtMeasuresMiscEndDate,
            self.cmbMeasuresMiscGroup,
            self.edtMeasuresMiscOffice,
            self.cmbMeasuresMiscOrgStructure
        )
        self.updateMeasuresMisc(filter)
        self.focusMeasuresMiscActions()


    def updateMeasuresStatus(self, filter, posToId=None, fieldName=None):
        self.__measuresStatusFilter = filter
        order = self.tblMeasuresStatusActions.order() if self.tblMeasuresStatusActions.order() else ['Action.endDate DESC', 'id']
        self.tblMeasuresStatusActions.setIdList(self.selectMeasuresActions(filter, 0, order, fieldName), posToId)


    def updateMeasuresCure(self, filter, posToId=None, fieldName=None):
        self.__measuresCureFilter = filter
        order = self.tblMeasuresCureActions.order() if self.tblMeasuresCureActions.order() else ['Action.endDate DESC', 'id']
        self.tblMeasuresCureActions.setIdList(self.selectMeasuresActions(filter, 2, order, fieldName), posToId)


    def updateMeasuresMisc(self, filter, posToId=None, fieldName=None):
        self.__measuresMiscFilter = filter
        order = self.tblMeasuresMiscActions.order() if self.tblMeasuresMiscActions.order() else ['Action.endDate DESC', 'id']
        self.tblMeasuresMiscActions.setIdList(self.selectMeasuresActions(filter, 3, order, fieldName), posToId)


    def focusMeasuresStatusActions(self):
        self.tblMeasuresStatusActions.setFocus(Qt.TabFocusReason)


    def focusMeasuresCureActions(self):
        self.tblMeasuresCureActions.setFocus(Qt.TabFocusReason)


    def focusMeasuresMiscActions(self):
        self.tblMeasuresMiscActions.setFocus(Qt.TabFocusReason)


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelMeasuresStatusActions_currentRowChanged(self, current, previous):
        self.updateMeasuresPropertiesTable(current, self.tblMeasuresStatusActionProperties, previous)


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelMeasuresDiagnosticActions_currentRowChanged(self, current, previous):
        self.updateMeasuresPropertiesTable(current, self.tblMeasuresDiagnosticActionProperties, previous)


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelMeasuresCureActions_currentRowChanged(self, current, previous):
        self.updateMeasuresPropertiesTable(current, self.tblMeasuresCureActionProperties, previous)


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelMeasuresMiscActions_currentRowChanged(self, current, previous):
        self.updateMeasuresPropertiesTable(current, self.tblMeasuresMiscActionProperties, previous)


    def updateMeasuresPropertiesTable(self, index, tbl, previous=None):
        if previous:
            tbl.savePreferencesLoc(previous.row())
        row = index.row()
        record = index.model().getRecordByRow(row) if row >= 0 else None
        if record:
            clientId = self.clientId
            clientSex = self.clientSex
            clientAge = self.clientAge
            action = CAction(record=record)
            tbl.model().setAction2(action, clientId, clientSex, clientAge)
            setActionPropertiesColumnVisible(action._actionType, tbl)
            tbl.resizeColumnsToContents()
            tbl.resizeRowsToContents()
            tbl.horizontalHeader().setStretchLastSection(True)
            tbl.loadPreferencesLoc(tbl.preferencesLocal, row)
        else:
            tbl.model().setAction2(None, None)


    def getProphylaxisPlanningType(self):
        db = QtGui.qApp.db
        table = db.table('rbProphylaxisPlanningType')
        record = db.getRecordEx(table, [table['id']], [table['code'].eq(u'ДН')])
        return forceRef(record.value('id'))if record else None


    def setControlSurveillanceItems(self, items):
        self.controlSurveillanceItems = items


    def setPlanningSurveillanceRecord(self, record):
        self.MKB = u''
        self.planningSurveillanceRecord = record


    def setEventId(self, eventId):
       self.eventId = eventId


    def setClientId(self, clientId):
        self.clientId = clientId


    def exec_(self):
        if self.lock(self._tableName, self._id):
            try:
                self.setRecord(self.planningSurveillanceRecord)
                self.setIsDirty(False)
                if not self.checkDataBeforeOpen():
                    return QtGui.QDialog.Rejected
                result = CDialogBase.exec_(self)
            finally:
                self.releaseLock()
        else:
            result = QtGui.QDialog.Rejected
            self.setResult(result)
        return result


    def setRecord(self, record):
        self.clientSex = None
        self.clientBirthDate = None
        self.clientAge = None
        self.measuresBegDate = None
        self.measuresEndDate = None
        self.MKBList = []
        baseDate = QDate.currentDate()
        CItemEditorBaseDialog.setRecord(self, record)
        self.MKB = forceStringEx(record.value('MKB'))
        db = QtGui.qApp.db
        if self.eventId:
            tableEvent = db.table('Event')
            recordEvent = db.getRecordEx(tableEvent,
                                         [tableEvent['client_id'], tableEvent['setDate'], tableEvent['execDate']],
                                         [tableEvent['id'].eq(self.eventId), tableEvent['deleted'].eq(0)])
            if not self.clientId:
                self.clientId = forceRef(recordEvent.value('client_id'))if recordEvent else None
            setDate = forceDate(recordEvent.value('setDate'))
            execDate = forceDate(recordEvent.value('execDate'))
            baseDate = execDate if execDate else setDate
        if self.clientId:
            tableClient = db.table('Client')
            recordClient = db.getRecordEx(tableClient, [tableClient['sex'], tableClient['birthDate']],
                                          [tableClient['id'].eq(self.clientId), tableClient['deleted'].eq(0)])
            if recordClient:
                self.clientSex = forceInt(recordClient.value('sex'))
                self.clientBirthDate = forceDate(recordClient.value('birthDate'))
                self.clientAge = calcAgeTuple(self.clientBirthDate, baseDate)
        self.modelPlanningSurveillance.setProphylaxisPlanningTypeId(self.prophylaxisPlanningTypeId)
        self.modelPlanningSurveillance.setClientId(self.clientId)
        self.modelPlanningSurveillance.setMKB(self.MKB)
        self.modelControlSurveillance.setProphylaxisPlanningTypeId(self.prophylaxisPlanningTypeId)
        self.modelControlSurveillance.setClientId(self.clientId)
        self.modelControlSurveillance.setMKB(self.MKB)
        self.modelPlanningSurveillance.setItems([self.planningSurveillanceRecord] if self.planningSurveillanceRecord else [])
        self.tblPlanningSurveillance.setCurrentRow(0)
        self.modelControlSurveillance.setItems(self.controlSurveillanceItems)
        self.btnAttachedFiles.loadItems(forceRef(record.value('id')))
        if self.controlSurveillanceItems:
            for item in self.controlSurveillanceItems:
                MKB = forceStringEx(item.value('MKB'))
                if MKB and MKB not in self.MKBList:
                    self.MKBList.append(MKB)
            CSItems = self.controlSurveillanceItems
            CSItems.sort(key=lambda x: forceDate(x.value('removeDate')), reverse=True)
            self.measuresEndDate = forceDate(CSItems[0].value('removeDate'))
            CSItems.sort(key=lambda x: forceDate(x.value('takenDate')), reverse=False)
            self.measuresBegDate = forceDate(CSItems[0].value('takenDate'))
            self.on_tabMeasuresContent_currentChanged(0)


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        return record


    def save(self):
        return True


    def checkDataEntered(self):
        return True


    def saveData(self):
        self.btnAttachedFiles.saveItems(self.itemId())
        return self.checkDataEntered() and self.save()


class CPersonInDocTableCol(CRBInDocTableCol):
    def __init__(self, title, fieldName, width, tableName, **params):
        CRBInDocTableCol.__init__(self, title, fieldName, width, tableName, **params)
        self.eventEditor = None
        self.filterLoc = u''
        self.isFilterAddSpeciality = True


    def setFilterAddSpeciality(self, value):
        self.isFilterAddSpeciality = value


    def setFilter(self, filter):
        self.filterLoc = filter


    def setEventEditor(self, eventEditor):
        self.eventEditor = eventEditor


    def setEditorData(self, editor, value, record):
        filterRetired = u''
        if self.eventEditor is not None:
            orgId = self.eventEditor.orgId
            begDate = forceDate(record.value('begDate'))
            endDate = forceDate(record.value('endDate'))
            filterDate = None
            if endDate:
                filterDate = u'DATE(retireDate) > DATE(%s)' % QtGui.qApp.db.formatDate(endDate)
            elif begDate:
                filterDate = u'DATE(retireDate) > DATE(%s)' % QtGui.qApp.db.formatDate(begDate)
            filterRetired = u' AND (retireDate IS NULL %s)' % ((u' OR (%s)' % filterDate) if filterDate else u'')
        else:
            orgId = QtGui.qApp.currentOrgId()
        if self.isFilterAddSpeciality:
            filter = 'speciality_id IS NOT NULL AND org_id=\'%s\' %s' % (orgId, filterRetired)
        else:
            filter = 'org_id=\'%s\' %s' % (orgId, filterRetired)
        if self.filterLoc:
            filter += u' AND ' + self.filterLoc
        editor.setTable(self.tableName, self.addNone, filter, 'name')
        editor.setShowFields(self.showFields)
        editor.setValue(forceRef(value))


class CPlanningSurveillanceCardModel(CInDocTableModel):
    Col_MKB = 0
    Col_DispanserId = 1
    Col_TakenDate = 2
    Col_PersonId = 3
    Col_VisitId = 4
    Col_RemoveDate = 5
    Col_RemoveReasonId = 6

    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'ProphylaxisPlanning', 'id', 'parent_id', parent)
        db = QtGui.qApp.db
        self.personCache = CTableRecordCache(db, db.forceTable('vrbPersonWithSpeciality'), u'*', capacity=None)
        self.addCol(CICDExInDocTableCol( u'МКБ',            'MKB',             7), QVariant.String).setReadOnly(True)
        self.addCol(CRBInDocTableCol(    u'ДН',             'dispanser_id',    10, 'rbDispanser')).setReadOnly(True)
        self.addCol(CDateInDocTableCol(  u'Дата взятия',    'takenDate',       10   )).setReadOnly(True)
        self.addCol(CPersonFindInDocTableCol(u'Врач',       'person_id',       20, 'vrbPersonWithSpecialityAndOrgStr')).setReadOnly(True)
        self.addCol(CDateInDocTableCol(  u'Дата снятия',    'removeDate',      10   )).setReadOnly(True)
        self.addCol(CRBInDocTableCol(    u'Причина снятия', 'removeReason_id', 10, 'rbSurveillanceRemoveReason')).setReadOnly(True)
        self.addHiddenCol('orgStructure_id')
        self.addHiddenCol('speciality_id')
        self.addHiddenCol('scene_id')
        self.addHiddenCol('prophylaxisPlanningType_id')
        self.addHiddenCol('client_id')
        self.eventEditor = None
        self.prophylaxisPlanningTypeId = None
        self.MKB = u''
        self.clientId = None


    def setClientId(self, clientId):
        self.clientId = clientId


    def setMKB(self, MKB):
        self.MKB = MKB


    def setProphylaxisPlanningTypeId(self, prophylaxisPlanningTypeId):
        self.prophylaxisPlanningTypeId = prophylaxisPlanningTypeId


    def setEventEditor(self, eventEditor):
        self.eventEditor = eventEditor


    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled


class CControlSurveillanceCardModel(CInDocTableModel):
    class CVisitInDocTableCol(CInDocTableCol):
        def __init__(self, title, fieldName, width, **params):
            CInDocTableCol.__init__(self, title, fieldName, width, **params)
            self.caches = {}
            self.MKBCaches = {}

        def toString(self, val, record):
            visitId = forceRef(val)
            date = u''
            db = QtGui.qApp.db
            if visitId:
                visitRecord = self.caches.get(visitId, None)
                if not visitRecord:
                    table = db.table('Visit')
                    visitRecord = db.getRecordEx(table, '*', [table['id'].eq(visitId)])
                if visitRecord:
                    date = forceStringEx(forceDate(visitRecord.value('date')))
                self.caches[visitId] = visitRecord
                MKB = forceStringEx(record.value('MKB'))
                if MKB:
                    MKBRecord = self.MKBCaches.get((visitId, MKB), None)
                    if not MKBRecord:
                            table = db.table('Visit')
                            tableEvent = db.table('Event')
                            tableDiagnosis = db.table('Diagnosis')
                            tableDiagnostic = db.table('Diagnostic')
                            tableDispanser = db.table('rbDispanser')
                            queryTable = tableEvent.innerJoin(table, table['event_id'].eq(tableEvent['id']))
                            queryTable = queryTable.innerJoin(tableDiagnostic, tableDiagnostic['event_id'].eq(tableEvent['id']))
                            queryTable = queryTable.innerJoin(tableDiagnosis, tableDiagnosis['id'].eq(tableDiagnostic['diagnosis_id']))
                            queryTable = queryTable.innerJoin(tableDispanser, tableDispanser['id'].eq(tableDiagnostic['dispanser_id']))
                            cond = [table['id'].eq(visitId),
                                    db.joinOr([tableDiagnosis['MKB'].eq(MKB), tableDiagnosis['MKB'].like(MKB[:3]+'%')]),
                                    tableDiagnostic['dispanser_id'].isNotNull(),
                                    table['deleted'].eq(0),
                                    tableDiagnosis['deleted'].eq(0),
                                    tableDiagnostic['deleted'].eq(0),
                                    tableEvent['deleted'].eq(0)
                                    ]
                            MKBRecord = db.getRecordEx(queryTable, 'Diagnosis.MKB', cond)
                            if MKBRecord:
                                self.MKBCaches[(visitId, MKB)] = MKBRecord
            return toVariant(date)

        def setEditorData(self, editor, value, record):
            editor.setValue(forceRef(value))

        def getEditorData(self, editor):
            return toVariant(editor.value())

    Col_MKB = 0
    Col_PlannedDate = 1
    Col_BegDate = 2
    Col_EndDate = 3
    Col_VisitId = 4
    Col_RemoveDate = 5
    Col_RemoveReasonId = 6

    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'ProphylaxisPlanning', 'id', 'parent_id', parent)
        self._parent = parent
        db = QtGui.qApp.db
        self.personCache = CTableRecordCache(db, db.forceTable('vrbPersonWithSpeciality'), u'*', capacity=None)
        self.addCol(CICDExInDocTableCol(u'МКБ',                    'MKB', 7), QVariant.String).setReadOnly(True)
        self.addCol(CDateInDocTableCol( u'Дата планирования',      'plannedDate',     10   )).setReadOnly(True)
        self.addCol(CDateInDocTableCol( u'Дата начала периода',    'begDate',         10   )).setReadOnly(True)
        self.addCol(CDateInDocTableCol( u'Дата окончания периода', 'endDate',         10   )).setReadOnly(True)
        self.addCol(CControlSurveillanceCardModel.CVisitInDocTableCol(u'Явился', 'visit_id', 20)).setReadOnly(True)
        self.addCol(CDateInDocTableCol( u'Дата снятия',            'removeDate',      10   )).setReadOnly(True)
        self.addCol(CRBInDocTableCol(   u'Причина снятия',         'removeReason_id', 10, 'rbSurveillanceRemoveReason')).setReadOnly(True)
        self.addHiddenCol('person_id')
        self.addHiddenCol('orgStructure_id')
        self.addHiddenCol('speciality_id')
        self.addHiddenCol('scene_id')
        self.addHiddenCol('prophylaxisPlanningType_id')
        self.addHiddenCol('client_id')
        self.addHiddenCol('takenDate')
        self.addHiddenCol('dispanser_id')
        self.eventEditor = None
        self.prophylaxisPlanningTypeId = None
        self.MKB = u''
        self.clientId = None


    def setClientId(self, clientId):
        self.clientId = clientId


    def setMKB(self, MKB):
        self.MKB = MKB


    def setProphylaxisPlanningTypeId(self, prophylaxisPlanningTypeId):
        self.prophylaxisPlanningTypeId = prophylaxisPlanningTypeId


    def setEventEditor(self, eventEditor):
        self.eventEditor = eventEditor


    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled


class CMeasuresActionsCheckTableModel(CTableModel):
    class CEnableCol(CBoolCol):
        def __init__(self, title, fields, defaultWidth, selector):
            CBoolCol.__init__(self, title, fields, defaultWidth)
            self.selector = selector

        def checked(self, values):
            id = forceRef(values[0])
            if self.selector.isSelected(id):
                return CBoolCol.valChecked
            else:
                return CBoolCol.valUnchecked

    def __init__(self, parent):
        CTableModel.__init__(self, parent)
        self.enableIdList = []
        self._items = []
        self.addColumn(CMeasuresActionsCheckTableModel.CEnableCol(u'Выбрать', ['id'], 5, self))
        self.addColumn(CDateCol(u'Назначено',      ['directionDate'], 15))
        self.addColumn(CActionTypeCol(u'Тип',                         15))
        self.addColumn(CBoolCol(u'Срочно',         ['isUrgent'],      15))
        self.addColumn(CEnumCol(u'Состояние',      ['status'], CActionStatus.names, 4))
        self.addColumn(CDateCol(u'План',           ['plannedEndDate'],15))
        self.addColumn(CDateCol(u'Начато',         ['begDate'],       15))
        self.addColumn(CDateCol(u'Окончено',       ['endDate'],       15))
        self.addColumn(CRefBookCol(u'Назначил',    ['setPerson_id'], 'vrbPersonWithSpeciality', 20))
        self.addColumn(CRefBookCol(u'Выполнил',    ['person_id'],    'vrbPersonWithSpeciality', 20))
        self.addColumn(CTextCol(u'Каб',            ['office'],                                6))
        self.addColumn(CTextCol(u'Примечания',     ['note'],                                  6))
        self.setTable('Action')
        self._mapColumnToOrder = {u'directionDate'      :u'Action.directionDate',
                                  u'actionType_id'      :u'ActionType.name',
                                  u'isUrgent'           :u'Action.isUrgent',
                                  u'status'             :u'Action.status',
                                  u'plannedEndDate'     :u'Action.plannedEndDate',
                                  u'begDate'            :u'Action.begDate',
                                  u'endDate'            :u'Action.endDate',
                                  u'setPerson_id'       :u'vrbPersonWithSpeciality.name',
                                  u'person_id'          :u'vrbPersonWithSpeciality.name',
                                  u'office'             :u'Action.office',
                                  u'note'               :u'Action.note'
                                  }


    def getOrder(self, fieldName, column):
        if hasattr(self._cols[column], 'extraFields'):
            if len(self._cols[column].extraFields) > 0:
                fieldName = self._cols[column].extraFields[0]
        return self._mapColumnToOrder[fieldName]


    def flags(self, index):
        result = CTableModel.flags(self, index)
        if index.column() == 0:
            result |= Qt.ItemIsUserCheckable
        return result


    def setData(self, index, value, role=Qt.EditRole):
        row = index.row()
        column = index.column()
        if role == Qt.CheckStateRole and column == 0:
            id = self._idList[row]
            if id:
                self.setSelected(id, forceInt(value) == Qt.Checked)
                self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)
            return True
        return CTableModel.setData(self, index, value, role)


    def setSelected(self, id, value):
        present = self.isSelected(id)
        if value:
            if not present:
                self.enableIdList.append(id)
        else:
            if present:
                self.enableIdList.remove(id)


    def isSelected(self, id):
        return id in self.enableIdList


    def getSelectedIdList(self):
        return self.enableIdList


    def getSelectedItems(self):
        selectedItems = []
        idList = self.getSelectedIdList()
        for id in idList:
            if id:
                record = self.getRecordById(id)
                selectedItems.append((record, CAction(record=record)))
        return selectedItems


    def setIdList(self, idList, realItemCount=None):
        self._items = []
        self._idList = idList
        self._realItemCount = realItemCount
        self._prevColumn = None
        self._prevRow    = None
        self._prevData   = None
        self.invalidateRecordsCache()
        self.reset()
        self.emitItemsCountChanged()
        for id in self._idList:
            if id:
                record = self.getRecordById(id)
                self._items.append((record, CAction(record=record)))


    def items(self):
        return self._items

