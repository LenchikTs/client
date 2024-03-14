# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2023 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

# Редактор одного action

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDate, QDateTime, QMimeData, QString, QTime, QVariant, pyqtSignature, SIGNAL

from Events.ActionsModel import CActionRecordItem
from Events.PropertyEditorAmbCard import CPropertyEditorAmbCard
from library.Attach.AttachAction     import getAttachAction
from library.Attach.AttachButton     import CAttachButton
from library.Calendar                import wpFiveDays, wpSixDays, wpSevenDays
from library.Counter                 import CCounterController
from library.DialogBase              import CDialogBase
from library.ICDUtils                import MKBwithoutSubclassification
from library.interchange import (
    getDatetimeEditValue,
    getDoubleBoxValue,
    getLineEditValue,
    getRBComboBoxValue,
    setCheckBoxValue,
    setDatetimeEditValue,
    setDoubleBoxValue,
    setLabelText,
    setLineEditValue,
    setRBComboBoxValue, getCheckBoxValue,
)

from library.ItemsListDialog         import CItemEditorBaseDialog
from library.JsonRpc.client          import CJsonRpcClent
from library.PrintInfo               import CInfoContext
from library.PrintTemplates          import applyTemplate, customizePrintButton, getPrintButton
from library.Utils                   import (
                                              calcAgeTuple,
                                              exceptionToUnicode,
                                              forceDate,
                                              forceDateTime,
                                              forceInt,
                                              forceRef,
                                              forceString,
                                              forceStringEx,
                                              formatName,
                                              toDateTimeWithoutSeconds,
                                              toVariant,
                                              forceBool,
                                              forceDouble,
                                            )

from Events.Action                   import CAction, CActionType, selectNomenclatureExpense, CActionTypeCache
from Events.ActionInfo import CCookedActionInfo, CActionInfoProxyList, CActionInfoList
from Events.ActionPropertiesTable    import CActionPropertiesTableModel
from Events.ActionStatus             import CActionStatus
from Events.ActionTemplateChoose     import (
                                              CActionTemplateCache,
                                              CActionTemplateSelectButton,
                                              # CActionTemplateChooseButton,
                                            )
from Events.ActionTemplateSaveDialog import CActionTemplateSaveDialog
from Events.ActionTemplateSelectDialog import CActionTemplateSelectDialog
from Events.EventEditDialog          import CEventEditDialog
from Events.EventInfo                import CEventInfo
from Events.ExecTimeNextActionDialog import CExecTimeNextActionDialog
from Events.ExecutionPlanDialog      import CGetExecutionPlan
from Events.GetPrevActionIdHelper    import CGetPrevActionIdHelper
from Events.Utils import (
    checkDiagnosis,
    checkAttachOnDate,
    checkPolicyOnDate,
    checkTissueJournalStatusByActions,
    getEventEnableActionsBeyondEvent,
    getEventDuration,
    getEventShowTime,
    setActionPropertiesColumnVisible,
    validCalculatorSettings,
    getEventMedicalAidKindId,
    getDeathDate,
    getEventPurposeId,
    updateNomenclatureDosageValue, CFinanceType, getEventContextData
)
from Events.TimeoutLogout         import CTimeoutLogout
#from Events.ExecutionPlan.ExecutionPlanType import CActionExecutionPlanType
from Orgs.Orgs                       import selectOrganisation
from Registry.ClientEditDialog       import CClientEditDialog
from Registry.Utils                  import formatClientBanner, getClientInfo
from Resources.CourseStatus          import CCourseStatus
from Resources.Utils                 import getNextDateExecutionPlan
from Stock.ClientInvoiceEditDialog   import CClientInvoiceEditDialog, CClientRefundInvoiceEditDialog
from Stock.Utils import getExistsNomenclatureAmount, getStockMotionItemQntEx, getStockMotionItemQnt, getRatio
from Users.Rights import (
    urAdmin,
    urCanUseNomenclatureButton,
    urCopyPrevAction,
    urEditCoordinationAction,
    urLoadActionTemplate,
    urEditOtherpeopleAction,
    urRegTabWriteRegistry,
    urRegTabReadRegistry,
    urSaveActionTemplate,
    urNomenclatureExpenseLaterDate,
    urNoRestrictRetrospectiveNEClient,
    urCanDeleteActionNomenclatureExpense,
    canChangeActionPerson,
    urEditOtherPeopleActionSpecialityOnly,
    urCanSaveEventWithMKBNotOMS
)

from Events.Ui_ActionEditDialog      import Ui_ActionDialog


_RECIPE = 1
_DOSES  = 2
_SIGNA  = 3
_ACTIVESUBSTANCE = 4


class CActionEditDialog(CItemEditorBaseDialog, Ui_ActionDialog):
    _saveAsExecutionPlan = False

    def __init__(self, parent):
# ctor
        CItemEditorBaseDialog.__init__(self, parent, 'Action')
        self.eventId     = None
        self.eventRecord = None
        self._eventExecDate = None
        self.eventTypeId = None
        self.eventPurposeId = None
        self.eventSetDate = None
        self.clientId    = None
        self.forceClientId = None
        self.clientSex   = None
        self.clientAge   = None
        self.clientBirthDate = None
        self.clientDeathDate = None
        self.personId    = None
        self.personSNILS = u''
        self.showTypeTemplate = 0
        self.personSpecialityId = None
        self.newActionId = None
        self.newAction = None
        self.clientInfo = None
        self.eventInfo = None
        self._mainWindowState = QtGui.qApp.mainWindow.windowState()
        self.getPrevActionIdHelper = CGetPrevActionIdHelper()
# create models
        self.addModels('ActionProperties', CActionPropertiesTableModel(self))
# ui
        self.addObject('actEditClient', QtGui.QAction(u'Открыть регистрационную карточку', self))
        self.addObject('actPortal_Doctor', QtGui.QAction(u'Перейти на портал врача', self))
        self.addObject('actShowAttachedToClientFiles', getAttachAction('Client_FileAttach',  self))
        self.addObject('btnPrint', getPrintButton(self, ''))
        #self.addObject('btnLoadTemplate', CActionTemplateChooseButton(self))
        self.addObject('btnLoadTemplate', CActionTemplateSelectButton(self))
        self.addObject('btnAttachedFiles', CAttachButton(self, u'Прикреплённые файлы'))
        self.btnLoadTemplate.setText(u'Загрузить шаблон')
        self.addObject('btnSaveAsTemplate', QtGui.QPushButton(u'Сохранить шаблон', self))
        self.addObject('btnLoadPrevAction', QtGui.QPushButton(u'Копировать из предыдущего', self))
        self.addObject('btnDelete', QtGui.QPushButton(u'Удалить', self))
        self.addObject('mnuLoadPrevAction',  QtGui.QMenu(self))
        self.addObject('actLoadSameSpecialityPrevAction', QtGui.QAction(u'Той же самой специальности', self))
        self.addObject('actLoadOwnPrevAction',            QtGui.QAction(u'Только свои', self))
        self.addObject('actLoadAnyPrevAction',            QtGui.QAction(u'Любое', self))
        self.addObject('actCopyInputActionProperty',            QtGui.QAction(u'Наследование', self))
        self.addObject('actPropertyEditorAmbCard', QtGui.QAction(u'Заполнить данные из мед карты', self))
        self.mnuLoadPrevAction.addAction(self.actLoadSameSpecialityPrevAction)
        self.mnuLoadPrevAction.addAction(self.actLoadOwnPrevAction)
        self.mnuLoadPrevAction.addAction(self.actLoadAnyPrevAction)
        self.mnuLoadPrevAction.addAction(self.actCopyInputActionProperty)
        self.btnLoadPrevAction.setMenu(self.mnuLoadPrevAction)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setWindowTitleEx(u'Мероприятие')
        self.isCmbMKBTextChanged = False
        self.edtDirectionDate.canBeEmpty(True)
        self.edtEndDate.canBeEmpty(True)
        self.edtBegDate.canBeEmpty(True)
        self.buttonBox.addButton(self.btnPrint, QtGui.QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.btnLoadTemplate, QtGui.QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.btnSaveAsTemplate, QtGui.QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.btnLoadPrevAction, QtGui.QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.btnAttachedFiles, QtGui.QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.btnDelete, QtGui.QDialogButtonBox.ActionRole)
        self.setModels(self.tblProps, self.modelActionProperties, self.selectionModelActionProperties)
# popup menus
        self.txtClientInfoBrowser.actions.append(self.actEditClient)
        self.txtClientInfoBrowser.actions.append(self.actPortal_Doctor)
        self.txtClientInfoBrowser.actions.append(self.actShowAttachedToClientFiles)
        self.actEditClient.setEnabled(QtGui.qApp.userHasAnyRight([urAdmin, urRegTabWriteRegistry, urRegTabReadRegistry]))
        self.setupActionPropertyPopupMenu()
# default values
        self.setupDirtyCather()
        self.setIsDirty(False)

        self.actionTemplateCache = CActionTemplateCache(self, self.cmbPerson)
        action = QtGui.QAction(self)
        self.addObject('actSetLaboratoryCalculatorInfo', action)
        action.setShortcut('F3')
        self.addAction(action)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.connect(self.actSetLaboratoryCalculatorInfo, SIGNAL('triggered()'), self.on_actSetLaboratoryCalculatorInfo)
        self.connect(self.btnCloseWidgets, SIGNAL('arrowTypeChanged(bool)'), self.on_arrowTypeChanged)
        self.connect(self.modelActionProperties, SIGNAL('actionAmountChanged(double)'), self.on_actionAmountChanged)
        self.cmbMKB.connect(self.cmbMKB._lineEdit, SIGNAL('editingFinished()'), self.on_cmbMKB_editingFinished)
        self.setVisibleBtnCloseWidgets(False)
        self._canUseLaboratoryCalculatorPropertyTypeList = None
        self.connect(self.modelActionProperties,
                     SIGNAL('setCurrentActionPlannedEndDate(QDate)'), self.setCurrentActionPlannedEndDate)
        self.btnDelete.setVisible(False)
## done
        if not QtGui.qApp.userHasRight(canChangeActionPerson):
            self.cmbPerson.setEnabled(False)
        if parent.__class__.__name__ != "CActionsTableView" and QtGui.qApp.getEventTimeout() != 0:
            self.timeoutFilter = CTimeoutLogout(QtGui.qApp.getEventTimeout()*60000 - 60000, self) 
            QtGui.qApp.installEventFilter(self.timeoutFilter)
            self.timeoutFilter.deleteLater()
            self.timeoutFilter.timerActivate(self.timeoutAlert)


    def setupActionPropertyPopupMenu(self):
        tbl = self.tblProps
        tbl.createPopupMenu([self.actPropertyEditorAmbCard])
        self.connect(tbl.popupMenu(), SIGNAL('aboutToShow()'), self.popupMenuPropertyAboutToShow)


    def popupMenuPropertyAboutToShow(self):
        model = self.tblProps.model()
        row = self.tblProps.currentIndex().row()
        if 0 <= row < model.rowCount() - 1:
            actionPropertyType = model.getPropertyType(row)
            if model.readOnly or (model.action and model.action.isLocked()):
                self.actPropertyEditorAmbCard.setEnabled(False)
            elif model.hasCommonPropertyChangingRight(row):
                self.actPropertyEditorAmbCard.setEnabled(actionPropertyType.typeName in ['Text', 'Constructor'])
            else:
                self.actPropertyEditorAmbCard.setEnabled(False)
        else:
            self.actPropertyEditorAmbCard.setEnabled(False)


    @pyqtSignature('')
    def on_actPropertyEditorAmbCard_triggered(self):
        index = self.tblProps.currentIndex()
        model = self.tblProps.model()
        row = index.row()
        if 0 <= row < model.rowCount():
            actionProperty = model.getProperty(row)
            dialog = CPropertyEditorAmbCard(self, self.clientId, self.clientSex, self.clientAge, self.eventTypeId, actionProperty)
            try:
                if dialog.exec_():
                    actionProperty = dialog.actionProperty
            finally:
                dialog.deleteLater()


    def timeoutAlert(self):
        self.timeoutFilter.disconnectAll()
        self.timeoutFilter.timerActivate(lambda: self.timeoutFilter.close(), 60000, False)
        if self.timeoutFilter.timeoutWindowAlert() == QtGui.QMessageBox.Cancel:
            self.timeoutFilter.disconnectAll()
            self.timeoutFilter.timerActivate(self.timeoutAlert)


    def setCurrentActionPlannedEndDate(self, date):
        self.edtPlannedEndDate.setDate(date)


    def on_actionAmountChanged(self, value):
        self.edtAmount.setValue(value)


    def on_arrowTypeChanged(self, value):
        self.frmWidgets.setVisible(value)


    def setActionCoordinationEnable(self, isRequiredCoordination):
        canEdit = QtGui.qApp.userHasRight(urEditCoordinationAction) and isRequiredCoordination
        editWidgets = [self.edtCoordDate,
                       self.edtCoordTime,
                       self.lblCoordText
                      ]
        for widget in editWidgets:
            widget.setEnabled(canEdit)


    def setVisibleBtnCloseWidgets(self, value):
        self.btnCloseWidgets.setVisible(value)
        if value:
            self.btnCloseWidgets.applayArrow()


    def setEventDate(self, date):
        eventRecord = self._getEventRecord()
        if eventRecord:
            execDate = forceDate(eventRecord.value('execDate'))
            if not execDate:
                self._eventExecDate = date


    def _getEventRecord(self):
        if not self.eventRecord and self.eventId:
            self.eventRecord = QtGui.qApp.db.getRecordEx('Event', 'id, execDate, isClosed, contract_id', 'id=%d'%self.eventId)
        return self.eventRecord


    def setReduced(self, value):
        self.txtClientInfoBrowser.setVisible(not value)
        if self.clientInfo is None:
            self.clientInfo = getClientInfo(self.clientId, date=self.edtDirectionDate.date())
        name = formatName(self.clientInfo.lastName, self.clientInfo.firstName, self.clientInfo.patrName)
        self.setWindowTitle(forceString(self.windowTitle()) + u' : ' + name)
        self.setVisibleBtnCloseWidgets(value)


    def exec_(self):
        QtGui.qApp.setCounterController(CCounterController(self))
        QtGui.qApp.setJTR(self)
        result = None
        try:
            result = CItemEditorBaseDialog.exec_(self)
        finally:
            if result:
                QtGui.qApp.delAllCounterValueIdReservation()
            else:
                QtGui.qApp.resetAllCounterValueIdReservation()
            QtGui.qApp.unsetJTR(self)
        QtGui.qApp.setCounterController(None)
        QtGui.qApp.disconnectClipboard()
        return result


#    def saveData(self):
#        self.scdSave = bool(self.checkDataEntered() and self.save())
#        return self.scdSave


    def setForceClientId(self, clientId):
        self.forceClientId = clientId


    def checkNeedLaboratoryCalculator(self, propertyTypeList, clipboardSlot):
        actualPropertyTypeList = [propType for propType in propertyTypeList if validCalculatorSettings(propType.laboratoryCalculator)]
        if actualPropertyTypeList:
            QtGui.qApp.connectClipboard(clipboardSlot)
        else:
            QtGui.qApp.disconnectClipboard()
        return actualPropertyTypeList


    @pyqtSignature('')
    def on_btnPlanNextAction_clicked(self):
        record = self.getRecord()
        if record and self.action:
            orgStructureIdList = []
            if not self.action.getType().isNomenclatureExpense:
                currentOrgStructureId = QtGui.qApp.currentOrgStructureId()
                userOrgStructureId = QtGui.qApp.userOrgStructureId
                currentOrgStructureIdList = []
                userOrgStructureIdList = []
                db = QtGui.qApp.db
                tableOrgStructure = db.table('OrgStructure')
                if currentOrgStructureId:
                    recordOS = db.getRecordEx(tableOrgStructure, [tableOrgStructure['parent_id']], [tableOrgStructure['id'].eq(currentOrgStructureId), tableOrgStructure['deleted'].eq(0)])
                    parentOSId = forceRef(recordOS.value('parent_id')) if recordOS else None
                    currentOrgStructureIdList = db.getDescendants('OrgStructure', 'parent_id', parentOSId if parentOSId else currentOrgStructureId)
                if userOrgStructureId:
                    recordOS = db.getRecordEx(tableOrgStructure, [tableOrgStructure['parent_id']], [tableOrgStructure['id'].eq(userOrgStructureId), tableOrgStructure['deleted'].eq(0)])
                    parentOSId = forceRef(recordOS.value('parent_id')) if recordOS else None
                    userOrgStructureIdList = db.getDescendants('OrgStructure', 'parent_id', parentOSId if parentOSId else userOrgStructureId)
                orgStructureIdList = list(set(currentOrgStructureIdList)|set(userOrgStructureIdList))
            dialog = CGetExecutionPlan(self, record, self.action.getExecutionPlan(), action = self.action, orgStructureIdList = orgStructureIdList)
            dialog.setVisibleBtn(False)
            dialog.exec_()
            self.action.executionPlanManager.setExecutionPlan(dialog.model.executionPlan)

    def executeAction(self, params):
        self.newActionId = None
        self.newAction = None
        prevRecord = self.getRecord()
        if not prevRecord:
            return
        currentDateTime = execDateTime = params.get('execDate', None)
        execCourse = params.get('course', None)
        nextChiefId = execPersonId = params.get('execPersonId', None)
        actionType = self.action.actionType()
        needCutFeed = True
        if any([actionType and i in actionType.flatCode.lower() for i in
                ['moving', 'received', 'inspectpigeonhole']]):
            jobTicketEndDateAskingIsRequired = forceBool(
                QtGui.qApp.preferences.appPrefs.get('jobTicketEndDateAskingIsRequired', QVariant(True)))
        else:
            jobTicketEndDateAskingIsRequired = False
        record = self.action.getRecord()
        if u'received' in actionType.flatCode.lower():
            self._onNextActionIsReceived(self.action, actionType, record, jobTicketEndDateAskingIsRequired,
                                         nextChiefId, currentDateTime, prevRecord)
        elif u'moving' in actionType.flatCode.lower():
            self._onNextActionIsMoving(self.action, actionType, record, jobTicketEndDateAskingIsRequired,
                                       nextChiefId, currentDateTime, needCutFeed, prevRecord)
        else:
            if self.action and self.action.actionType().isDoesNotInvolveExecutionCourse and self.cmbStatus.value() != CActionStatus.canceled:
                prevRecord.setValue('status', toVariant(CActionStatus.finished))
                endDate = forceDateTime(prevRecord.value('endDate'))
                if not endDate:
                    prevRecord.setValue('endDate', toVariant(QDateTime.currentDateTime()))
                prevRecord.setValue('person_id', toVariant(QtGui.qApp.userId if (
                            QtGui.qApp.userId and QtGui.qApp.userSpecialityId) else self.cmbAPSetPerson.value()))
                if self.action.nomenclatureExpense:
                    self.action = updateNomenclatureDosageValue(self.action)
                    isControlExecWriteOffNomenclatureExpense = QtGui.qApp.controlExecutionWriteOffNomenclatureExpense()
                    if isControlExecWriteOffNomenclatureExpense:
                        db = QtGui.qApp.db
                        message = u''
                        nomenclatureLine = []
                        tableNomenclature = db.table('rbNomenclature')
                        if self.action.nomenclatureExpense:
                            stockMotionItems = self.action.nomenclatureExpense.stockMotionItems()
                            for stockMotionItem in stockMotionItems:
                                price = forceDouble(stockMotionItem.value('price'))
                                oldPrice = price
                                nomenclatureId = forceRef(stockMotionItem.value('nomenclature_id'))
                                if nomenclatureId and nomenclatureId not in nomenclatureLine:
                                    qnt = round(forceDouble(stockMotionItem.value('qnt')),
                                                QtGui.qApp.numberDecimalPlacesQnt())
                                    unitId = forceRef(stockMotionItem.value('unit_id'))
                                    stockUnitId = self.getDefaultStockUnitId(nomenclatureId)
                                    ratio = self.getRatio(nomenclatureId, stockUnitId, unitId)
                                    if ratio is not None:
                                        price = price * ratio
                                        qnt = qnt / ratio
                                    financeId = forceRef(stockMotionItem.value('finance_id'))
                                    batch = forceString(stockMotionItem.value('batch'))
                                    shelfTime = forceDate(stockMotionItem.value('shelfTime'))
                                    shelfTime = shelfTime.toPyDate() if bool(shelfTime) else None
                                    medicalAidKindId = forceRef(stockMotionItem.value('medicalAidKind_id'))
                                    otherHaving = [u'(shelfTime>=curDate()) OR shelfTime is NULL']
                                    existsQnt = getExistsNomenclatureAmount(nomenclatureId, financeId, batch,
                                                                            unitId=stockUnitId,
                                                                            medicalAidKindId=medicalAidKindId,
                                                                            shelfTime=shelfTime,
                                                                            otherHaving=otherHaving, exact=True,
                                                                            price=price, isStockUtilization=False,
                                                                            precision=QtGui.qApp.numberDecimalPlacesQnt())
                                    prevQnt = round(
                                        getStockMotionItemQntEx(nomenclatureId, stockMotionId=None, batch=batch,
                                                                financeId=financeId, clientId=self.clientId,
                                                                medicalAidKindId=medicalAidKindId, price=None,
                                                                oldPrice=oldPrice, oldUnitId=stockUnitId),
                                        QtGui.qApp.numberDecimalPlacesQnt())
                                    resQnt = (existsQnt + prevQnt) - qnt
                                    if resQnt <= 0:
                                        nomenclatureLine.append(nomenclatureId)
                            if nomenclatureLine:
                                nomenclatureName = u''
                                records = db.getRecordList(tableNomenclature, [tableNomenclature['name']],
                                                           [tableNomenclature['id'].inlist(nomenclatureLine)],
                                                           order=tableNomenclature['name'].name())
                                for recordNomenclature in records:
                                    nomenclatureName += u'\n' + forceString(recordNomenclature.value('name'))
                                message += u'''Действие типа %s.\nОтсутствуют ЛСиИМН: %s!\n''' % (
                                self.action._actionType.name, nomenclatureName)
                            if message:
                                if isControlExecWriteOffNomenclatureExpense == 1:
                                    button = QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel
                                    message2 = u'Списываемое ЛСиИМН отсутствует на остатке подразделения. Выполнить списание?'
                                else:
                                    button = QtGui.QMessageBox.Cancel
                                    message2 = u'Списываемое ЛСиИМН отсутствует на остатке подразделения. Списание невозможно!'
                                res = QtGui.QMessageBox.warning(None, u'Внимание!', message2, button,
                                                                QtGui.QMessageBox.Cancel)
                                if res == QtGui.QMessageBox.Cancel:
                                    return
                    if not self._openNomenclatureEditor(self.action, prevRecord, requireItems=True):
                        return
                return

            actionTypeId = forceRef(prevRecord.value('actionType_id'))
            plannedEndDate = forceDateTime(prevRecord.value('plannedEndDate'))
            duration = self.edtDuration.value()
            aliquoticity = self.edtAliquoticity.value() or 1
            quantity = self.edtQuantity.value()
            if not (duration > 0 or aliquoticity > 0) and actionTypeId:
                return

            periodicity = self.edtPeriodicity.value()

            db = QtGui.qApp.db
            tableAction = db.table('Action')
            eventId = forceRef(prevRecord.value('event_id'))

            if not eventId:
                raise RuntimeError()

            begDate = forceDateTime(prevRecord.value('begDate'))
            if not execPersonId:
                if QtGui.qApp.userId and QtGui.qApp.userSpecialityId:
                    execPersonId = QtGui.qApp.userId
                else:
                    execPersonId = self.cmbSetPerson.value()

            if self.action.nomenclatureExpense:
                executionPlanItem = self.action.executionPlanManager.currentItem
                if executionPlanItem and executionPlanItem.nomenclature and executionPlanItem.nomenclature.nomenclatureId:
                    if executionPlanItem.nomenclature.nomenclatureId:
                        if not self.action.nomenclatureExpense.stockMotionItems() or not self.action.nomenclatureExpense.getNomenclatureIdItem(
                                executionPlanItem.nomenclature.nomenclatureId):
                            nomenclatureIdDict = {}
                            nomenclatureIdDict[executionPlanItem.nomenclature.nomenclatureId] = (self.action.getRecord(), executionPlanItem.nomenclature.dosage)
                            self.action.nomenclatureExpense.updateNomenclatureIdListToAction(nomenclatureIdDict)
                        if executionPlanItem.nomenclature and executionPlanItem.nomenclature.dosage and not executionPlanItem.executedDatetime:
                            self.action.nomenclatureExpense.updateNomenclatureDosageValue(
                                executionPlanItem.nomenclature.nomenclatureId,
                                executionPlanItem.nomenclature.dosage, force=True)
                    isControlExecWriteOffNomenclatureExpense = QtGui.qApp.controlExecutionWriteOffNomenclatureExpense()
                    if isControlExecWriteOffNomenclatureExpense:
                        db = QtGui.qApp.db
                        message = u''
                        nomenclatureLine = []
                        tableNomenclature = db.table('rbNomenclature')
                        if self.action.nomenclatureExpense:
                            stockMotionItems = self.action.nomenclatureExpense.stockMotionItems()
                            for stockMotionItem in stockMotionItems:
                                price = forceDouble(stockMotionItem.value('price'))
                                oldPrice = price
                                nomenclatureId = forceRef(stockMotionItem.value('nomenclature_id'))
                                if nomenclatureId and nomenclatureId not in nomenclatureLine:
                                    unitId = forceRef(stockMotionItem.value('unit_id'))
                                    qnt = round(forceDouble(stockMotionItem.value('qnt')),
                                                QtGui.qApp.numberDecimalPlacesQnt())
                                    stockUnitId = self.getDefaultStockUnitId(nomenclatureId)
                                    ratio = self.getRatio(nomenclatureId, stockUnitId, unitId)
                                    if ratio is not None:
                                        price = price * ratio
                                        qnt = qnt / ratio
                                    financeId = forceRef(stockMotionItem.value('finance_id'))
                                    batch = forceString(stockMotionItem.value('batch'))
                                    shelfTime = forceDate(stockMotionItem.value('shelfTime'))
                                    shelfTime = shelfTime.toPyDate() if bool(shelfTime) else None
                                    medicalAidKindId = forceRef(stockMotionItem.value('medicalAidKind_id'))
                                    otherHaving = [u'(shelfTime>=curDate()) OR shelfTime is NULL']
                                    existsQnt = getExistsNomenclatureAmount(nomenclatureId, financeId, batch,
                                                                            unitId=stockUnitId,
                                                                            medicalAidKindId=medicalAidKindId,
                                                                            shelfTime=shelfTime,
                                                                            otherHaving=otherHaving, exact=True,
                                                                            price=price, isStockUtilization=False,
                                                                            precision=QtGui.qApp.numberDecimalPlacesQnt())
                                    prevQnt = round(
                                        getStockMotionItemQntEx(nomenclatureId, stockMotionId=None, batch=batch,
                                                                financeId=financeId, clientId=self.clientId,
                                                                medicalAidKindId=medicalAidKindId, price=None,
                                                                oldPrice=oldPrice, oldUnitId=stockUnitId),
                                        QtGui.qApp.numberDecimalPlacesQnt())
                                    resQnt = (existsQnt + prevQnt) - qnt
                                    if resQnt <= 0:
                                        nomenclatureLine.append(nomenclatureId)
                            if nomenclatureLine:
                                nomenclatureName = u''
                                records = db.getRecordList(tableNomenclature, [tableNomenclature['name']],
                                                           [tableNomenclature['id'].inlist(nomenclatureLine)],
                                                           order=tableNomenclature['name'].name())
                                for recordNomenclature in records:
                                    nomenclatureName += u'\n' + forceString(recordNomenclature.value('name'))
                                message += u'''Действие типа %s.\nОтсутствуют ЛСиИМН: %s!\n''' % (
                                self.action._actionType.name, nomenclatureName)
                            if message:
                                if isControlExecWriteOffNomenclatureExpense == 1:
                                    button = QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel
                                    message2 = u'Списываемое ЛСиИМН отсутствует на остатке подразделения. Выполнить списание?'
                                else:
                                    button = QtGui.QMessageBox.Cancel
                                    message2 = u'Списываемое ЛСиИМН отсутствует на остатке подразделения. Списание невозможно!'
                                res = QtGui.QMessageBox.warning(None, u'Внимание!', message2, button,
                                                                QtGui.QMessageBox.Cancel)
                                if res == QtGui.QMessageBox.Cancel:
                                    return
            if not self._openNomenclatureEditor(requireItems=True):
                return
            executionPlan = self.action.getExecutionPlan()
            nextPlanDate = None
            jobTicketOrgStructureId = None
            self.action.executionPlanManager.setCurrentItemIndex(
                self.action.executionPlanManager.executionPlan.items.index(
                    self.action.executionPlanManager._currentItem))
            nextExecutionPlanItem = self.action.executionPlanManager.getNextItem()
            #        if executionPlan and not self.action.getType().isNomenclatureExpense and nextExecutionPlanItem and not bool(nextExecutionPlanItem.date):
            #            nextPlanDate, jobData = getNextDateExecutionPlan(self, jobTicketId=None, prevActionDate=begDate, executionPlan=executionPlan, lastAction=self.action, nextExecutionPlanItem=nextExecutionPlanItem)
            #            jobTicketOrgStructureId = jobData[2] if len(jobData) >= 3 else None
            #            if bool(nextPlanDate):
            #                if self.action and self.action.executionPlanManager:
            #                    self.action.executionPlanManager.setExecutionPlan(executionPlan)
            specifiedName = forceString(prevRecord.value('specifiedName'))
            prevRecord.setValue('person_id', toVariant(execPersonId))
            prevRecord.setValue('aliquoticity', toVariant(aliquoticity))
            prevRecord.setValue('begDate', toVariant(begDate))
            prevRecord.setValue('endDate', toVariant(execDateTime))
            prevRecord.setValue('status', toVariant(CActionStatus.finished))
            if not self.action.getType().isNomenclatureExpense and execCourse > CCourseStatus.proceed:
                if execCourse in [CCourseStatus.skipRefusalClient, CCourseStatus.finishRefusalClient]:
                    prevRecord.setValue('status', QVariant(CActionStatus.refused))
                if execCourse in [CCourseStatus.skipRefusalMO, CCourseStatus.finishRefusalMO]:
                    prevRecord.setValue('status', QVariant(CActionStatus.canceled))
                if execCourse in [CCourseStatus.skipRefusalClient, CCourseStatus.skipRefusalMO,
                                  CCourseStatus.finishRefusalClient, CCourseStatus.finishRefusalMO]:
                    self.freeJobTicketFirstCourse()
            if not self.action.getType().isNomenclatureExpense and execCourse not in [
                CCourseStatus.finishRefusalClient, CCourseStatus.finishRefusalMO]:
                if executionPlan and not self.action.getType().isNomenclatureExpense and nextExecutionPlanItem and not bool(
                        nextExecutionPlanItem.date):
                    nextPlanDate, jobData = getNextDateExecutionPlan(self, jobTicketId=None, prevActionDate=begDate,
                                                                     executionPlan=executionPlan,
                                                                     lastAction=self.action,
                                                                     nextExecutionPlanItem=nextExecutionPlanItem)
                    jobTicketOrgStructureId = jobData[2] if len(jobData) >= 3 else None
                    if bool(nextPlanDate):
                        if self.action and self.action.executionPlanManager:
                            self.action.executionPlanManager.setExecutionPlan(executionPlan)
            #                nextExecutionPlanItem = self.action.executionPlanManager.getNextItem()
            self.action.executionPlanManager.setCurrentItemExecuted()
            if nextExecutionPlanItem:
                if self.action.executionPlanManager.getDuration() > 0:
                    duration = max(
                        nextExecutionPlanItem.date.daysTo(self.action.executionPlanManager.plannedEndDate()), 1)
            else:
                if self.action.nomenclatureClientReservation:
                    self.action.nomenclatureClientReservation.cancel()
                prevRecord.setValue('quantity', toVariant(quantity - (1 if quantity > 0 else 0)))
                self.setRecordByNext(prevRecord)
                try:
                    self._saveAsExecutionPlan = True
                    self.done(self.cdSave)
                finally:
                    self._saveAsExecutionPlan = False
                return
            if executionPlan:
                aliquoticity = 1
                aliquoticityToDate = executionPlan.getCountItemsByDate(
                    nextExecutionPlanItem.getDateTime().date() if nextExecutionPlanItem else begDate.date())
                if aliquoticityToDate:
                    aliquoticity = aliquoticityToDate
                else:
                    aliquoticityEP = executionPlan.getAliquoticity()
                    if aliquoticityEP:
                        aliquoticity = aliquoticityEP
            prevRecord.setValue('periodicity', toVariant(periodicity))
            if jobTicketOrgStructureId and not forceRef(prevRecord.value('orgStructure_id')):
                prevRecord.setValue('orgStructure_id', toVariant(jobTicketOrgStructureId))
            if actionType.requiredActionSpecification:
                prevRecord.setValue('actionSpecification_id', toVariant(self.cmbActionSpecification.value()))
            executionPlan = self.action.getExecutionPlan()
            if not (not self.action.getType().isNomenclatureExpense and execCourse in [
                CCourseStatus.finishRefusalClient, CCourseStatus.finishRefusalMO]):
                newRecord = tableAction.newRecord()
                newRecord.setValue('event_id', toVariant(prevRecord.value('event_id')))
                newRecord.setValue('begDate', toVariant(nextExecutionPlanItem.getDateTime()))
                newRecord.setValue('status', toVariant(CActionStatus.started))
                #                        newRecord.setValue('specifiedName', toVariant(specifiedName))
                newRecord.setValue('duration', toVariant(duration))
                newRecord.setValue('periodicity', toVariant(periodicity))
                newRecord.setValue('aliquoticity', toVariant(aliquoticity))
                newRecord.setValue('quantity', toVariant(quantity - (1 if quantity > 0 else 0)))
                newRecord.setValue('plannedEndDate', toVariant(plannedEndDate))
                newRecord.setValue('actionType_id', toVariant(actionTypeId))
                newRecord.setValue('directionDate', toVariant(prevRecord.value('directionDate')))
                newRecord.setValue('setPerson_id', toVariant(prevRecord.value('setPerson_id')))
                newRecord.setValue('org_id', toVariant(prevRecord.value('org_id')))
                newRecord.setValue('amount', toVariant(prevRecord.value('amount')))
                newRecord.setValue('orgStructure_id', toVariant(
                    jobTicketOrgStructureId) if jobTicketOrgStructureId else prevRecord.value('orgStructure_id'))
                if actionType.requiredActionSpecification:
                    newRecord.setValue('actionSpecification_id',
                                       toVariant(prevRecord.value('actionSpecification_id')))

                personId = QtGui.qApp.userId if (
                            QtGui.qApp.userId and QtGui.qApp.userSpecialityId) else self.cmbSetPerson.value()

                newRecord.setValue('person_id', toVariant(personId))

                newAction = CAction(record=newRecord)
                newAction.updateByAction(self.action)
                if nextExecutionPlanItem:
                    if newAction and newAction.executionPlanManager:
                        newAction.executionPlanManager.setExecutionPlan(executionPlan)
                    newAction.setExecutionPlanItem(nextExecutionPlanItem)
                    newAction.executionPlanManager.bindAction(newAction)

                newAction.initPropertiesBySameAction(self.action)
                orgStructureId = forceRef(record.value('orgStructure_id'))
                medicalAidKindId = self.action.getMedicalAidKindId()
                if QtGui.qApp.controlSMFinance() == 0:
                    newAction.initNomenclature(self.clientId, medicalAidKindId=medicalAidKindId)
                    newAction.nomenclatureReservationFromAction(self.action, medicalAidKindId=medicalAidKindId,
                                                                supplierId=orgStructureId)
                else:
                    newAction.initNomenclature(self.clientId, financeId=forceRef(record.value('finance_id')),
                                               medicalAidKindId=medicalAidKindId)
                    newAction.nomenclatureReservationFromAction(self.action,
                                                                financeId=forceRef(record.value('finance_id')),
                                                                medicalAidKindId=medicalAidKindId,
                                                                supplierId=orgStructureId)
                #                newAction.initNomenclature(self.clientId)
                #                newAction.nomenclatureReservationFromAction(self.action)

                if newAction.getType().isNomenclatureExpense:
                    newAction.updateDosageFromExecutionPlan()
                    newAction.updateSpecifiedName()
                else:
                    newRecord.setValue('specifiedName', toVariant(specifiedName))

                if executionPlan and not self.action.getType().isNomenclatureExpense:
                    for property in newAction.getType()._propertiesById.itervalues():
                        if property.isJobTicketValueType() and property.valueType.initPresetValue:
                            prop = newAction.getPropertyById(property.id)
                            if prop._type:
                                prop._type.valueType.setIsExceedJobTicket(True)
                                prop._type.valueType.setIsNearestJobTicket(True)
                                prop._type.valueType.setDateTimeExecJob(
                                    nextExecutionPlanItem.getDateTime() if nextExecutionPlanItem else begDate)
                    #                                    if jobTicketOrgStructureId:
                    #                                        prop._type.valueType.setExecOrgStructureId(jobTicketOrgStructureId)
                    newAction.initPresetValues()
                newAction.finalFillingPlannedEndDate()
                self.newAction = newAction

            self.setRecordByNext(prevRecord)
            try:
                self._saveAsExecutionPlan = True
                self.done(self.cdSave)
            finally:
                self._saveAsExecutionPlan = False


    @pyqtSignature('')
    def on_btnNextAction_clicked(self):
        if self.cmbStatus.value() == CActionStatus.canceled:
            currentDateTime = QDateTime.currentDateTime()
            db = QtGui.qApp.db
            table = db.table('vrbPersonWithSpeciality')
            personId = QtGui.qApp.userId if (QtGui.qApp.userId and QtGui.qApp.userSpecialityId) else self.cmbSetPerson.value()
            record = db.getRecordEx(table, [table['name']], [table['id'].eq(personId)]) if personId else None
            personName = forceString(record.value('name')) if record else ''
            self.edtNote.setText(u'Отменить: %s %s'%(currentDateTime.toString('dd-MM-yyyy hh:mm'), personName))
            return

        self.newActionId = None
        self.newAction = None
        prevRecord = self.getRecord()
        if not prevRecord:
            return

        if self.action and self.action.actionType().isDoesNotInvolveExecutionCourse and self.cmbStatus.value() != CActionStatus.canceled:
            prevRecord.setValue('status', toVariant(CActionStatus.finished))
            endDate = forceDateTime(prevRecord.value('endDate'))
            if not endDate:
                prevRecord.setValue('endDate', toVariant(QDateTime.currentDateTime()))
            prevRecord.setValue('person_id', toVariant(
                QtGui.qApp.userId if (QtGui.qApp.userId and QtGui.qApp.userSpecialityId) else self.cmbAPSetPerson.value())
            )
            if self.action.nomenclatureExpense:
                self.action = updateNomenclatureDosageValue(self.action)
                isControlExecWriteOffNomenclatureExpense = QtGui.qApp.controlExecutionWriteOffNomenclatureExpense()
                if isControlExecWriteOffNomenclatureExpense:
                    db = QtGui.qApp.db
                    message = u''
                    nomenclatureLine = []
                    tableNomenclature = db.table('rbNomenclature')
                    if self.action.nomenclatureExpense:
                        stockMotionItems = self.action.nomenclatureExpense.stockMotionItems()
                        for stockMotionItem in stockMotionItems:
                            price = forceDouble(stockMotionItem.value('price'))
                            nomenclatureId = forceRef(stockMotionItem.value('nomenclature_id'))
                            if nomenclatureId and nomenclatureId not in nomenclatureLine:
                                qnt = round(forceDouble(stockMotionItem.value('qnt')), QtGui.qApp.numberDecimalPlacesQnt())
                                unitId = forceRef(stockMotionItem.value('unit_id'))
                                stockUnitId = self.getDefaultStockUnitId(nomenclatureId)
                                ratio = self.getRatio(nomenclatureId, stockUnitId, unitId)
                                if ratio is not None:
                                    price = price*ratio
                                    qnt = qnt / ratio
                                financeId = forceRef(stockMotionItem.value('finance_id'))
                                batch = forceString(stockMotionItem.value('batch'))
                                shelfTime = forceDate(stockMotionItem.value('shelfTime'))
                                shelfTime = shelfTime.toPyDate() if bool(shelfTime) else None
                                medicalAidKindId = forceRef(stockMotionItem.value('medicalAidKind_id'))
                                otherHaving=[u'(shelfTime>=curDate()) OR shelfTime is NULL']
                                existsQnt = getExistsNomenclatureAmount(nomenclatureId, financeId, batch, unitId=stockUnitId, medicalAidKindId = medicalAidKindId, shelfTime=shelfTime, otherHaving=otherHaving, exact=True, price=price, isStockUtilization=False, precision=QtGui.qApp.numberDecimalPlacesQnt())
                                prevQnt = round(getStockMotionItemQnt(nomenclatureId, stockMotionId=None, batch=batch,
                                                                      financeId=financeId, clientId=self.clientId,
                                                                      medicalAidKindId=medicalAidKindId, price=price),
                                                QtGui.qApp.numberDecimalPlacesQnt())
                                resQnt = (existsQnt + prevQnt) - qnt
                                if resQnt <= 0:
                                    nomenclatureLine.append(nomenclatureId)
                        if nomenclatureLine:
                            nomenclatureName = u''
                            records = db.getRecordList(tableNomenclature, [tableNomenclature['name']], [tableNomenclature['id'].inlist(nomenclatureLine)], order = tableNomenclature['name'].name())
                            for recordNomenclature in records:
                                nomenclatureName += u'\n' + forceString(recordNomenclature.value('name'))
                            message += u'''Действие типа %s.\nОтсутствуют ЛСиИМН: %s!\n'''%(self.action._actionType.name, nomenclatureName)
                        if message:
                            if isControlExecWriteOffNomenclatureExpense == 1:
                                button = QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel
                            else:
                                button = QtGui.QMessageBox.Cancel
                            res = QtGui.QMessageBox().warning(None,
                                                              u'Внимание!',
                                                              u'Списываемое ЛСиИМН отсутствует на остатке подразделения. Выполнить списание?',
                                                              button,
                                                              QtGui.QMessageBox.Cancel)
                            if res == QtGui.QMessageBox.Cancel:
                                return
                if not self._openNomenclatureEditor(self.action, prevRecord, requireItems=True):
                    return
            return

        actionTypeId = forceRef(prevRecord.value('actionType_id'))
        plannedEndDate = forceDateTime(prevRecord.value('plannedEndDate'))
        duration = self.edtDuration.value()
        aliquoticity = self.edtAliquoticity.value() or 1
        quantity = self.edtQuantity.value()
        if not (duration > 0 or aliquoticity > 0) and actionTypeId:
            return

        periodicity = self.edtPeriodicity.value()

        db = QtGui.qApp.db
        tableAction = db.table('Action')
        eventId = forceRef(prevRecord.value('event_id'))

        if not eventId:
            raise RuntimeError()

        begDate = forceDateTime(prevRecord.value('begDate'))
        if QtGui.qApp.userId and QtGui.qApp.userSpecialityId:
            execPersonId = QtGui.qApp.userId
        else:
            execPersonId = self.cmbSetPerson.value()

        if self.action.nomenclatureExpense:
            executionPlanItem = self.action.executionPlanManager.currentItem
            if executionPlanItem and executionPlanItem.nomenclature and executionPlanItem.nomenclature.nomenclatureId:
                if executionPlanItem.nomenclature.nomenclatureId:
                    if not self.action.nomenclatureExpense.stockMotionItems() or not self.action.nomenclatureExpense.getNomenclatureIdItem(executionPlanItem.nomenclature.nomenclatureId):
                        nomenclatureIdDict = {}
                        nomenclatureIdDict[executionPlanItem.nomenclature.nomenclatureId] = (self.action.getRecord(), executionPlanItem.nomenclature.dosage)
                        self.action.nomenclatureExpense.updateNomenclatureIdListToAction(nomenclatureIdDict)
                    if executionPlanItem.nomenclature and executionPlanItem.nomenclature.dosage and not executionPlanItem.executedDatetime:
                        self.action.nomenclatureExpense.updateNomenclatureDosageValue(
                            executionPlanItem.nomenclature.nomenclatureId,
                            executionPlanItem.nomenclature.dosage,
                            force=True
                        )
            isControlExecWriteOffNomenclatureExpense = QtGui.qApp.controlExecutionWriteOffNomenclatureExpense()
            if isControlExecWriteOffNomenclatureExpense:
                db = QtGui.qApp.db
                message = u''
                nomenclatureLine = []
                tableNomenclature = db.table('rbNomenclature')
                if self.action.nomenclatureExpense:
                    stockMotionItems = self.action.nomenclatureExpense.stockMotionItems()
                    for stockMotionItem in stockMotionItems:
                        price = forceDouble(stockMotionItem.value('price'))
                        nomenclatureId = forceRef(stockMotionItem.value('nomenclature_id'))
                        if nomenclatureId and nomenclatureId not in nomenclatureLine:
                            qnt = round(forceDouble(stockMotionItem.value('qnt')), QtGui.qApp.numberDecimalPlacesQnt())
                            unitId = forceRef(stockMotionItem.value('unit_id'))
                            ratio = getRatio(nomenclatureId, None, unitId)
                            if ratio is not None:
                                price = price*ratio
                            financeId = forceRef(stockMotionItem.value('finance_id'))
                            batch = forceString(stockMotionItem.value('batch'))
                            shelfTime = forceDate(stockMotionItem.value('shelfTime'))
                            shelfTime = shelfTime.toPyDate() if bool(shelfTime) else None
                            medicalAidKindId = forceRef(stockMotionItem.value('medicalAidKind_id'))
                            otherHaving=[u'(shelfTime>=curDate()) OR shelfTime is NULL']
                            existsQnt = getExistsNomenclatureAmount(nomenclatureId, financeId, batch, unitId=unitId, medicalAidKindId = medicalAidKindId, shelfTime=shelfTime, otherHaving=otherHaving, exact=True, price=price, isStockUtilization=False, precision=QtGui.qApp.numberDecimalPlacesQnt())
                            prevQnt = round(getStockMotionItemQnt(nomenclatureId, stockMotionId=None, batch=batch,
                                                                  financeId=financeId, clientId=self.clientId,
                                                                  medicalAidKindId=medicalAidKindId, price=price),
                                            QtGui.qApp.numberDecimalPlacesQnt())
                            resQnt = (existsQnt + prevQnt) - qnt
                            if resQnt <= 0:
                                nomenclatureLine.append(nomenclatureId)
                    if nomenclatureLine:
                        nomenclatureName = u''
                        records = db.getRecordList(tableNomenclature, [tableNomenclature['name']], [tableNomenclature['id'].inlist(nomenclatureLine)], order = tableNomenclature['name'].name())
                        for recordNomenclature in records:
                            nomenclatureName += u'\n' + forceString(recordNomenclature.value('name'))
                        message += u'''Действие типа %s.\nОтсутствуют ЛСиИМН: %s!\n'''%(self.action._actionType.name, nomenclatureName)
                    if message:
                        if isControlExecWriteOffNomenclatureExpense == 1:
                            button = QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel
                        else:
                            button = QtGui.QMessageBox.Cancel
                        res = QtGui.QMessageBox().warning(None,
                                                          u'Внимание!',
                                                          u'Списываемое ЛСиИМН отсутствует на остатке подразделения. Выполнить списание?',
                                                          button,
                                                          QtGui.QMessageBox.Cancel)
                        if res == QtGui.QMessageBox.Cancel:
                            return
        if not self._openNomenclatureEditor(requireItems=True):
            return
        executionPlan = self.action.getExecutionPlan()
        nextPlanDate = None
        jobTicketOrgStructureId = None
        self.action.executionPlanManager.setCurrentItemIndex(self.action.executionPlanManager.executionPlan.items.index(self.action.executionPlanManager._currentItem))
        nextExecutionPlanItem = self.action.executionPlanManager.getNextItem()
#        if executionPlan and not self.action.getType().isNomenclatureExpense and nextExecutionPlanItem and not bool(nextExecutionPlanItem.date):
#            nextPlanDate, jobData = getNextDateExecutionPlan(self, jobTicketId=None, prevActionDate=begDate, executionPlan=executionPlan, lastAction=self.action, nextExecutionPlanItem=nextExecutionPlanItem)
#            jobTicketOrgStructureId = jobData[2] if len(jobData) >= 3 else None
#            if bool(nextPlanDate):
#                if self.action and self.action.executionPlanManager:
#                    self.action.executionPlanManager.setExecutionPlan(executionPlan)
        execTimePlanManager = None
        epManagerCurrentItem = self.action.executionPlanManager._currentItem if (not self.action.getType().isNomenclatureExpense and self.action.executionPlanManager) else None
        if epManagerCurrentItem:
            execDateTimePlanManager = epManagerCurrentItem.getDateTime()
            if execDateTimePlanManager:
                execTimePlanManager = execDateTimePlanManager.time()
        dialog = CExecTimeNextActionDialog(self, begDate, execPersonId, execTimePlanManager=execTimePlanManager)
        try:
            dialog.setCourseVisible(bool(epManagerCurrentItem))
            if dialog.exec_():
                execTime = dialog.getExecTime()
                execCourse = dialog.execCourse()
                execPersonId = dialog.getExecPersonId()
                specifiedName = forceString(prevRecord.value('specifiedName'))
                prevRecord.setValue('person_id', toVariant(execPersonId))
                prevRecord.setValue('aliquoticity',  toVariant(aliquoticity))
                prevRecord.setValue('begDate', toVariant(begDate))
                prevRecord.setValue('endDate', toVariant(QDateTime(begDate.date(), execTime)))
                prevRecord.setValue('status', toVariant(CActionStatus.finished))
                if not self.action.getType().isNomenclatureExpense and execCourse > CCourseStatus.proceed:
                    if execCourse in [CCourseStatus.skipRefusalClient, CCourseStatus.finishRefusalClient]:
                        prevRecord.setValue('status', QVariant(CActionStatus.refused))
                    if execCourse in [CCourseStatus.skipRefusalMO, CCourseStatus.finishRefusalMO]:
                        prevRecord.setValue('status', QVariant(CActionStatus.canceled))
                    if execCourse in [CCourseStatus.skipRefusalClient, CCourseStatus.skipRefusalMO, CCourseStatus.finishRefusalClient, CCourseStatus.finishRefusalMO]:
                        self.freeJobTicketFirstCourse()
                if not self.action.getType().isNomenclatureExpense and execCourse not in [CCourseStatus.finishRefusalClient, CCourseStatus.finishRefusalMO]:
                    if executionPlan and not self.action.getType().isNomenclatureExpense and nextExecutionPlanItem and not bool(nextExecutionPlanItem.date):
                        nextPlanDate, jobData = getNextDateExecutionPlan(self, jobTicketId=None, prevActionDate=begDate, executionPlan=executionPlan, lastAction=self.action, nextExecutionPlanItem=nextExecutionPlanItem)
                        jobTicketOrgStructureId = jobData[2] if len(jobData) >= 3 else None
                        if bool(nextPlanDate):
                            if self.action and self.action.executionPlanManager:
                                self.action.executionPlanManager.setExecutionPlan(executionPlan)
#                nextExecutionPlanItem = self.action.executionPlanManager.getNextItem()
                self.action.executionPlanManager.setCurrentItemExecuted()
                if nextExecutionPlanItem:
                    if self.action.executionPlanManager.getDuration() > 0:
                        duration = max(
                            nextExecutionPlanItem.date.daysTo(
                                self.action.executionPlanManager.plannedEndDate()
                            ), 1)
                else:
                    if self.action.nomenclatureClientReservation:
                        self.action.nomenclatureClientReservation.cancel()
                    prevRecord.setValue('quantity', toVariant(quantity-(1 if quantity > 0 else 0)))
                    self.setRecordByNext(prevRecord)
                    try:
                        self._saveAsExecutionPlan = True
                        self.done(self.cdSave)
                    finally:
                        self._saveAsExecutionPlan = False
                    return
                if executionPlan:
                    aliquoticity = 1
                    aliquoticityToDate = executionPlan.getCountItemsByDate(
                        nextExecutionPlanItem.getDateTime().date() if nextExecutionPlanItem else begDate.date())
                    if aliquoticityToDate:
                        aliquoticity = aliquoticityToDate
                    else:
                        aliquoticityEP = executionPlan.getAliquoticity()
                        if aliquoticityEP:
                            aliquoticity = aliquoticityEP
                prevRecord.setValue('periodicity',   toVariant(periodicity))
                if jobTicketOrgStructureId and not forceRef(prevRecord.value('orgStructure_id')):
                    prevRecord.setValue('orgStructure_id', toVariant(jobTicketOrgStructureId))
                if self.action.getType().requiredActionSpecification:
                    prevRecord.setValue('actionSpecification_id', toVariant(self.cmbActionSpecification.value()))
                executionPlan = self.action.getExecutionPlan()
                if not (not self.action.getType().isNomenclatureExpense and execCourse in [CCourseStatus.finishRefusalClient, CCourseStatus.finishRefusalMO]):
                    newRecord = tableAction.newRecord()
                    newRecord.setValue('event_id',      toVariant(prevRecord.value('event_id')))
                    newRecord.setValue('begDate',       toVariant(nextExecutionPlanItem.getDateTime()))
                    newRecord.setValue('status',        toVariant(CActionStatus.started))
                    # newRecord.setValue('specifiedName', toVariant(specifiedName))
                    newRecord.setValue('duration',      toVariant(duration))
                    newRecord.setValue('periodicity',   toVariant(periodicity))
                    newRecord.setValue('aliquoticity',  toVariant(aliquoticity))
                    newRecord.setValue('quantity',      toVariant(quantity-(1 if quantity > 0 else 0)))
                    newRecord.setValue('plannedEndDate', toVariant(plannedEndDate))
                    newRecord.setValue('actionType_id', toVariant(actionTypeId))
                    newRecord.setValue('directionDate', toVariant(prevRecord.value('directionDate')))
                    newRecord.setValue('setPerson_id',  toVariant(prevRecord.value('setPerson_id')))
                    newRecord.setValue('org_id',        toVariant(prevRecord.value('org_id')))
                    newRecord.setValue('amount',        toVariant(prevRecord.value('amount')))
                    newRecord.setValue('orgStructure_id', toVariant(jobTicketOrgStructureId) if jobTicketOrgStructureId else prevRecord.value('orgStructure_id'))
                    if self.action.getType().requiredActionSpecification:
                        newRecord.setValue('actionSpecification_id', toVariant(prevRecord.value('actionSpecification_id')))

                    personId = QtGui.qApp.userId \
                        if (QtGui.qApp.userId and QtGui.qApp.userSpecialityId) \
                        else self.cmbSetPerson.value()

                    newRecord.setValue('person_id', toVariant(personId))

                    newAction = CAction(record=newRecord)
                    newAction.updateByAction(self.action)
                    if nextExecutionPlanItem:
                        if newAction and newAction.executionPlanManager:
                            newAction.executionPlanManager.setExecutionPlan(executionPlan)
                        newAction.setExecutionPlanItem(nextExecutionPlanItem)
                        newAction.executionPlanManager.bindAction(newAction)

                    newAction.initPropertiesBySameAction(self.action)
                    newAction.initNomenclature(self.clientId)
                    newAction.nomenclatureReservationFromAction(self.action)

                    if newAction.getType().isNomenclatureExpense:
                        newAction.updateDosageFromExecutionPlan()
                        newAction.updateSpecifiedName()
                    else:
                        newRecord.setValue('specifiedName', toVariant(specifiedName))

                    if executionPlan and not self.action.getType().isNomenclatureExpense:
                        for property in newAction.getType()._propertiesById.itervalues():
                            if property.isJobTicketValueType() and property.valueType.initPresetValue:
                                prop = newAction.getPropertyById(property.id)
                                if prop._type:
                                    prop._type.valueType.setIsExceedJobTicket(True)
                                    prop._type.valueType.setIsNearestJobTicket(True)
                                    prop._type.valueType.setDateTimeExecJob(nextExecutionPlanItem.getDateTime() if nextExecutionPlanItem else begDate)
#                                    if jobTicketOrgStructureId:
#                                        prop._type.valueType.setExecOrgStructureId(jobTicketOrgStructureId)
                        newAction.initPresetValues()
                    newAction.finalFillingPlannedEndDate()
                    self.newAction = newAction

                self.setRecordByNext(prevRecord)

                try:
                    self._saveAsExecutionPlan = True
                    self.done(self.cdSave)
                finally:
                    self._saveAsExecutionPlan = False

        finally:
            dialog.deleteLater()

    def freeJobTicketFirstCourse(self):
        if self.action:
            for property in self.action.getType()._propertiesById.itervalues():
                if property.isJobTicketValueType():
                    prop = self.action.getPropertyById(property.id)
                    if prop._type:
                        QtGui.qApp.setJTR(self)
                        try:
                            prop._value = None
                            prop._changed = True
                        finally:
                            QtGui.qApp.unsetJTR(self)
                        self.tblProps.model().reset()


    def getCurrentTimeAction(self, actionDate):
        currentDateTime = QDateTime.currentDateTime()
        if currentDateTime == actionDate:
            currentTime = currentDateTime.time()
            return currentTime.addSecs(60)
        else:
            return currentDateTime.time()


    def setRecordByNext(self, record):
        self.eventId = forceRef(record.value('event_id'))
        self.eventTypeId = forceRef(QtGui.qApp.db.translate('Event', 'id', self.eventId, 'eventType_id'))
        self.eventSetDate = forceDate(QtGui.qApp.db.translate('Event', 'id', self.eventId, 'setDate'))
        self.idx = forceInt(record.value('idx'))
        self.clientId = forceRef(QtGui.qApp.db.translate('Event', 'id', self.eventId, 'client_id'))
        self.action._record = record
        actionType = self.action.getType()
        setActionPropertiesColumnVisible(actionType, self.tblProps)
        showTime = actionType.showTime
        self.edtDirectionTime.setVisible(showTime)
        self.edtPlannedEndTime.setVisible(showTime)
        self.edtCoordTime.setVisible(showTime)
        self.edtBegTime.setVisible(showTime)
        self.edtEndTime.setVisible(showTime)
        self.lblAssistant.setVisible(actionType.hasAssistant)
        self.cmbAssistant.setVisible(actionType.hasAssistant)
        self.lblActionSpecification.setVisible(actionType.requiredActionSpecification)
        self.cmbActionSpecification.setVisible(actionType.requiredActionSpecification)
        if actionType.requiredActionSpecification:
            actionSpecificationId = forceRef(record.value('actionSpecification_id'))
            actionSpecificationIdList = actionType.getActionSpecificationIdList()
            setFilter = u'id IN (%s)' % (u', '.join(str(actionSpecificationId) for actionSpecificationId in actionSpecificationIdList if actionSpecificationId is not None))
            self.cmbActionSpecification.setTable('rbActionSpecification', True, filter=setFilter)
            self.cmbActionSpecification.setValue(actionSpecificationId)
        self.setWindowTitle(actionType.code + '|' + actionType.name)
        setCheckBoxValue(self.chkIsUrgent, record, 'isUrgent')
        setDatetimeEditValue(self.edtDirectionDate,    self.edtDirectionTime,    record, 'directionDate')
        setDatetimeEditValue(self.edtPlannedEndDate,   self.edtPlannedEndTime,   record, 'plannedEndDate')
        setDatetimeEditValue(self.edtCoordDate, self.edtCoordTime, record, 'coordDate')
        setLabelText( self.lblCoordText, record, 'coordText')
        setDatetimeEditValue(self.edtBegDate,          self.edtBegTime,          record, 'begDate')
        setDatetimeEditValue(self.edtEndDate,          self.edtEndTime,          record, 'endDate')
        setRBComboBoxValue(self.cmbStatus,      record, 'status')
        setDoubleBoxValue(self.edtAmount,       record, 'amount')
        setDoubleBoxValue(self.edtUet,          record, 'uet')
        setRBComboBoxValue(self.cmbPerson,      record, 'person_id')
        setRBComboBoxValue(self.cmbSetPerson,   record, 'setPerson_id')
        setLineEditValue(self.edtOffice,        record, 'office')
        setRBComboBoxValue(self.cmbAssistant,   record, 'assistant_id')
        setLineEditValue(self.edtNote,          record, 'note')
        self.cmbOrgStructure.setValue(forceRef(record.value('orgStructure_id')))
        self.edtQuantity.setValue(forceInt(record.value('quantity')))
        self.edtDuration.setValue(forceInt(record.value('duration')))
        self.edtPeriodicity.setValue(forceInt(record.value('periodicity')))
        self.edtAliquoticity.setValue(forceInt(record.value('aliquoticity')))

        mkbVisible = bool(actionType.defaultMKB)
        mkbEnabled = actionType.defaultMKB in (CActionType.dmkbByFinalDiag,
                                               CActionType.dmkbBySetPersonDiag,
                                               CActionType.dmkbUserInput
                                              )
        self.cmbMKB.setVisible(mkbVisible)
        self.lblMKB.setVisible(mkbVisible)
        self.cmbMKB.setEnabled(mkbEnabled)
        self.cmbMKB.setText(forceString(record.value('MKB')))

        morphologyMKBVisible = mkbVisible and QtGui.qApp.defaultMorphologyMKBIsVisible()
        self.cmbMorphologyMKB.setVisible(morphologyMKBVisible)
        self.lblMorphologyMKB.setVisible(morphologyMKBVisible)
        self.cmbMorphologyMKB.setEnabled(mkbEnabled)
        self.cmbMorphologyMKB.setText(forceString(record.value('morphologyMKB')))

        self.cmbOrg.setValue(forceRef(record.value('org_id')))
        if (self.cmbPerson.value() is None
                and actionType.defaultPersonInEditor in (CActionType.dpUndefined, CActionType.dpCurrentUser, CActionType.dpCurrentMedUser)
                and QtGui.qApp.userSpecialityId):
            self.cmbPerson.setValue(QtGui.qApp.userId)
        self.setPersonId(self.cmbPerson.value())
        self.modelActionProperties.setAction(self.action, self.clientId, self.clientSex, self.clientAge, self.eventTypeId)
        # self.modelActionProperties.reset()
        self.tblProps.resizeRowsToContents()

        canEdit = not self.action.isLocked() if self.action else True
        canEditPlannedEndDate = canEdit and actionType.defaultPlannedEndDate != CActionType.dpedBegDatePlusAmount
        canEditIsExecutionPlan = not bool(self.action.getExecutionPlan() and self.action.executionPlanManager.hasItemsToDo())
        self.edtPlannedEndDate.setEnabled(canEditPlannedEndDate and canEditIsExecutionPlan)
        self.edtPlannedEndTime.setEnabled(canEditPlannedEndDate and canEditIsExecutionPlan)
        if not self.action.nomenclatureExpense:
            self.btnAPNomenclatureExpense.setVisible(False)
        self.on_edtDuration_valueChanged(forceInt(record.value('duration')))
        self.cmbMKB.setFilter('''IF(MKB.endDate IS NOT NULL, MKB.endDate >= %s, 1)'''%(QtGui.qApp.db.formatDate(self.edtBegDate.date())))
        self.setActionCoordinationEnable(actionType.isRequiredCoordination)


    def btnNextActionMustBeEnabled(self):
        return bool(self.action and ((self.action.getExecutionPlan() and self.action.executionPlanManager.hasItemsToDo()) or self.action.getType().isDoesNotInvolveExecutionCourse) and self.cmbStatus.value() not in (CActionStatus.canceled, CActionStatus.refused))


    def isEnabledNomenclatureExpense(self, action):
        record = action.getRecord() if action else None
        begDate = forceDate(record.value('begDate')) if record else None
        currentDate = QDate().currentDate()
        minimumDate = None
        isEnabled = bool(begDate)
        if not QtGui.qApp.userHasRight(urNoRestrictRetrospectiveNEClient):
            if QtGui.qApp.admissibilityNomenclatureExpensePostDates() == 1:
                minimumDate = currentDate.addDays(-1)
            elif QtGui.qApp.admissibilityNomenclatureExpensePostDates() == 2:
                minimumDate = QDate(currentDate.year(), currentDate.month(), 1)
        if minimumDate:
            if QtGui.qApp.userHasRight(urNomenclatureExpenseLaterDate):
                isEnabled = begDate >= minimumDate
            else:
                isEnabled = begDate >= minimumDate and begDate <= currentDate
        else:
            if not QtGui.qApp.userHasRight(urNomenclatureExpenseLaterDate):
                isEnabled = begDate <= currentDate
        return isEnabled


    @pyqtSignature('int')
    def on_edtDuration_valueChanged(self, value):
        if value > 0:
            self.btnPlanNextAction.setEnabled(True)
            if not self.action.getType().isNomenclatureExpense:
                record = self.action.getRecord()
                if record and forceInt(record.value('duration')) != value:
                    self.action.getRecord().setValue('duration', toVariant(value))
                self.btnPlanNextAction.setEnabled(bool(self.edtQuantity.value()))
        else:
            self.btnPlanNextAction.setEnabled(False)
            if not self.action.getType().isNomenclatureExpense:
                self.btnPlanNextAction.setEnabled(bool(self.edtQuantity.value()))
                record = self.action.getRecord()
                if forceInt(record.value('duration')) != value:
                    self.action.getRecord().setValue('duration', toVariant(value))
        if self.action and not self.action.getType().isDoesNotInvolveExecutionCourse:
            canEdit = not self.action.isLocked() if self.action else True
            canEditIsExecutionPlan = not bool(self.action.getExecutionPlan() and self.action.executionPlanManager.hasItemsToDo())
            self.edtDirectionDate.setEnabled(bool(not value > 0) and canEdit)
            self.edtDirectionTime.setEnabled(bool(not value > 0) and canEdit)
            self.cmbSetPerson.setEnabled(bool(not value > 0) and canEdit)
            self.edtPlannedEndDate.setEnabled(bool(not value > 0) and canEdit and canEditIsExecutionPlan)
            self.edtPlannedEndTime.setEnabled(bool(not value > 0) and canEdit and canEditIsExecutionPlan)
            self.edtBegDate.setEnabled(bool(not value > 0) and canEdit)
            self.edtBegTime.setEnabled(bool(not value > 0) and canEdit)
            self.edtEndDate.setEnabled(bool(not value > 0) and canEdit)
            self.edtEndTime.setEnabled(bool(not value > 0) and canEdit)
            actionType = self.action.getType()
            if actionType.defaultPlannedEndDate == CActionType.dpedBegDatePlusDuration:
                begDate = self.edtBegDate.date()
                date = begDate.addDays(value-1) if begDate and value else QDate()
                self.edtPlannedEndDate.setDate(date)
        isEnable = self.btnNextActionMustBeEnabled()
        if self.action.getType().isNomenclatureExpense:
            isEnable = isEnable and self.isEnabledNomenclatureExpense(self.action)
        self.btnNextAction.setEnabled(isEnable)
        if self.action and self.action.getType().isDoesNotInvolveExecutionCourse and self.action.nomenclatureExpense:
            self.action = updateNomenclatureDosageValue(self.action)
            self.edtQuantity.setValue(forceInt(self.action.getRecord().value('quantity')))


    @pyqtSignature('int')
    def on_edtPeriodicity_valueChanged(self, value):
        if not self.action.getType().isNomenclatureExpense:
            record = self.action.getRecord()
            if record and forceInt(record.value('periodicity')) != value:
                self.action.getRecord().setValue('periodicity', toVariant(value))
            self.btnPlanNextAction.setEnabled(bool(self.edtQuantity.value()))
            isEnable = self.btnNextActionMustBeEnabled()
            if self.action.getType().isNomenclatureExpense:
                isEnable = isEnable and self.isEnabledNomenclatureExpense(self.action)
            self.btnNextAction.setEnabled(isEnable)
        if self.action and self.action.getType().isDoesNotInvolveExecutionCourse and self.action.nomenclatureExpense:
            self.action = updateNomenclatureDosageValue(self.action)
            self.edtQuantity.setValue(forceInt(self.action.getRecord().value('quantity')))


    @pyqtSignature('int')
    def on_edtAliquoticity_valueChanged(self, value):
        if not self.action.getType().isNomenclatureExpense:
            record = self.action.getRecord()
            if record and forceInt(record.value('aliquoticity')) != value:
                self.action.getRecord().setValue('aliquoticity', toVariant(value))
            self.btnPlanNextAction.setEnabled(bool(self.edtQuantity.value()))
            isEnable = self.btnNextActionMustBeEnabled()
            if self.action.getType().isNomenclatureExpense:
                isEnable = isEnable and self.isEnabledNomenclatureExpense(self.action)
            self.btnNextAction.setEnabled(isEnable)
        if self.action and self.action.getType().isDoesNotInvolveExecutionCourse and self.action.nomenclatureExpense:
            self.action = updateNomenclatureDosageValue(self.action)
            self.edtQuantity.setValue(forceInt(self.action.getRecord().value('quantity')))


    @pyqtSignature('int')
    def on_edtQuantity_valueChanged(self, value):
        if not self.action.getType().isNomenclatureExpense:
            record = self.action.getRecord()
            if record and forceInt(record.value('quantity')) != value:
                self.action.getRecord().setValue('quantity', toVariant(value))
            self.btnPlanNextAction.setEnabled(bool(self.edtQuantity.value()))
            isEnable = self.btnNextActionMustBeEnabled()
            if self.action.getType().isNomenclatureExpense:
                isEnable = isEnable and self.isEnabledNomenclatureExpense(self.action)
            self.btnNextAction.setEnabled(isEnable)

    @pyqtSignature('')
    def on_actCopyInputActionProperty_triggered(self):
        if not self.parent()._parent.eventEditor.applyChanges():
            return
        model = self.parent()._parent.tblAPActions.model()
        items = model.items()
        row = self.parent()._parent.tblAPActions.currentIndex().row()
        data = getEventContextData(self.parent()._parent.eventEditor)
        eventInfo = data['event']
        currentActionIndex = eventInfo.actions._rawItems.index(items[row])
        actionId = eventInfo.actions[currentActionIndex].id
        from library.PrintInfo import CInfoContext
        context = CInfoContext()
        union_value = ''
        current_action = self.action
        from library.copyInput import searchActionIn, searchActionOut
        queryIn = searchActionIn(actionId)
        if queryIn.size() == 0:
            return
        while queryIn.next():
            recordIn = queryIn.record()

            temp_settings = forceString(recordIn.value('dataInheritance')).split('][')
            if len(temp_settings) > 1:
                settings = temp_settings[0][1:]
                current_dataInheritance = temp_settings[1][:-1]
            else:
                settings = None
                current_dataInheritance = forceString(recordIn.value('dataInheritance')).replace('[', '').replace(
                    ']', '')

            current_name = forceString(recordIn.value('name'))
            if not current_action[current_name]:
                current_action[current_name] = ''
            if len(current_dataInheritance.split(',')) > 1:
                current_dataInheritance_temp = []
                for short in current_dataInheritance.split(','):
                    if 'in_' in short.strip():
                        current_dataInheritance_temp.append(short.strip())
                queryOut = searchActionOut(current_dataInheritance_temp, eventInfo.id)
                checkAction = 0
                while queryOut.next():
                    recordOut = queryOut.record()
                    value = forceString(recordOut.value('value'))
                    if checkAction != forceString(recordOut.value('action_id')):
                        checkAction = 0
                    if settings:
                        union_value = ''
                        from Events.ActionInfo import CActionInfo
                        temp_action = context.getInstance(CActionInfo, forceString(recordOut.value('action_id')))
                        if len(settings.split(',')) > 1:
                            for short_settings in settings.split(','):
                                if 'property' in short_settings:
                                    if union_value != '':
                                        union_value += '\n'
                                    code = "union_value += temp_action[forceString(recordOut.value('name'))]." + short_settings.replace(
                                        'property.', '')
                                    exec (code)
                                    union_value += ' '
                                elif 'action' in short_settings and checkAction == 0:
                                    code = "union_value += temp_action." + short_settings.replace('action.', '')
                                    exec (code)
                                    union_value += ' '
                        else:
                            if 'property' in settings:
                                if union_value != '':
                                    union_value += '\n'
                                code = "union_value += temp_action[forceString(recordOut.value('name'))]." + settings.replace(
                                    'property.', '')
                                exec (code)
                                union_value += ' '
                            elif 'action' in settings and checkAction == 0:
                                code = "union_value += temp_action." + settings.replace('action.', '')
                                exec (code)
                                union_value += ' '
                    else:
                        union_value = ''
                    if checkAction == 0:
                        checkAction = forceString(recordOut.value('action_id'))

                    if (union_value + '\n' + value) not in current_action[current_name] and (
                            union_value + ' - ' + value) not in current_action[current_name]:
                        if current_action[current_name] != '':
                            current_action[current_name] += '\n'
                        if union_value != '':
                            if settings and 'property' in settings:
                                current_action[current_name] += union_value + ' - ' + value
                            else:
                                current_action[current_name] += union_value + '\n' + value
                        else:
                            current_action[current_name] += value
            else:
                queryOut = searchActionOut(current_dataInheritance, eventInfo.id)
                checkAction = 0
                while queryOut.next():
                    recordOut = queryOut.record()
                    value = forceString(recordOut.value('value'))
                    if checkAction != forceString(recordOut.value('action_id')):
                        checkAction = 0
                    if settings:
                        union_value = ''
                        from Events.ActionInfo import CActionInfo
                        temp_action = context.getInstance(CActionInfo, forceString(recordOut.value('action_id')))
                        if len(settings.split(',')) > 1:
                            for short_settings in settings.split(','):
                                if 'property' in short_settings:
                                    if union_value != '':
                                        union_value += '\n'
                                    code = "union_value += temp_action[forceString(recordOut.value('name'))]." + short_settings.replace(
                                        'property.', '')
                                    exec (code)
                                    union_value += ' '
                                elif 'action' in short_settings and checkAction == 0:
                                    code = "union_value += temp_action." + short_settings.replace('action.', '')
                                    exec (code)
                                    union_value += ' '
                        else:
                            if 'property' in settings:
                                if union_value != '':
                                    union_value += '\n'
                                code = "union_value += temp_action[forceString(recordOut.value('name'))]." + settings.replace(
                                    'property.', '')
                                exec (code)
                                union_value += ' '
                            elif 'action' in settings and checkAction == 0:
                                code = "union_value += temp_action." + settings.replace('action.', '')
                                exec (code)
                                union_value += ' '
                    else:
                        union_value = ''

                    if checkAction == 0:
                        checkAction = forceString(recordOut.value('action_id'))

                    if (union_value + '\n' + value) not in current_action[current_name] and (
                            union_value + ' - ' + value) not in current_action[current_name]:
                        if current_action[current_name] != '':
                            current_action[current_name] += '\n'
                        if union_value != '':
                            if settings and 'property' in settings:
                                current_action[current_name] += union_value + '- ' + value
                            else:
                                current_action[current_name] += union_value + '\n' + value
                        else:
                            current_action[current_name] += value
        self.tblProps.model().reset()


    def on_actSetLaboratoryCalculatorInfo(self):
        result = self.checkNeedLaboratoryCalculator(self.modelActionProperties.propertyTypeList,
                                                    self.on_laboratoryCalculatorClipboard)
        self._canUseLaboratoryCalculatorPropertyTypeList = result
        self.setInfoToLaboratoryCalculatorClipboard()


    def setInfoToLaboratoryCalculatorClipboard(self):
        def chooseLabCode(propType):
            code = propType.laboratoryCalculator
            if code in ('LL*', 'GG*', 'EE*', 'CI*'):
                return '%s%s'%(code, unicode(self.modelActionProperties.action.getPropertyById(propType.id).getValue()))
            else:
                return code
        if self._canUseLaboratoryCalculatorPropertyTypeList:
            propertyTypeList = self._canUseLaboratoryCalculatorPropertyTypeList
            #actual = unicode('; '.join(['('+','.join([forceString(propType.id), propType.laboratoryCalculator, propType.name])+')' for propType in propertyTypeList]))
            actual = unicode('; '.join(['('+','.join([forceString(propType.id),
                chooseLabCode(propType),
                propType.name])+')' for propType in propertyTypeList]))
            mimeData = QMimeData()
            mimeData.setData(QtGui.qApp.inputCalculatorMimeDataType,
                             QString(actual).toUtf8())
            QtGui.qApp.clipboard().setMimeData(mimeData)
            self._mainWindowState = QtGui.qApp.mainWindow.windowState()
            QtGui.qApp.mainWindow.showMinimized()


    def on_laboratoryCalculatorClipboard(self):
        mimeData = QtGui.qApp.clipboard().mimeData()
        baData = mimeData.data(QtGui.qApp.outputCalculatorMimeDataType)
        if baData:
            QtGui.qApp.mainWindow.setWindowState(self._mainWindowState)
            data = forceString(QString.fromUtf8(baData))
            self.modelActionProperties.setLaboratoryCalculatorData(data)

    def destroy(self):
        pass

    def getClientId(self, eventId):
        if self.forceClientId:
            return self.forceClientId
        return forceRef(QtGui.qApp.db.translate('Event', 'id', eventId, 'client_id'))

    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        self.eventId = forceRef(record.value('event_id'))
        self.eventTypeId = forceRef(QtGui.qApp.db.translate('Event', 'id', self.eventId, 'eventType_id'))
        self.eventSetDate = forceDate(QtGui.qApp.db.translate('Event', 'id', self.eventId, 'setDate'))
        self.idx = forceInt(record.value('idx'))
        self.clientId = self.getClientId(self.eventId)
        self.action = CAction(record=record)
        self.action.executionPlanManager.load()
        self.action.executionPlanManager.setCurrentItemIndex()
        actionType = self.action.getType()
        setActionPropertiesColumnVisible(actionType, self.tblProps)
        showTime = actionType.showTime
        self.edtDirectionTime.setVisible(showTime)
        self.edtPlannedEndTime.setVisible(showTime)
        self.edtCoordTime.setVisible(showTime)
        self.edtBegTime.setVisible(showTime)
        self.edtEndTime.setVisible(showTime)
        self.lblAssistant.setVisible(actionType.hasAssistant)
        self.cmbAssistant.setVisible(actionType.hasAssistant)
        self.setWindowTitle(actionType.code + '|' + actionType.name)
        setCheckBoxValue(self.chkIsUrgent, record, 'isUrgent')
        setDatetimeEditValue(self.edtDirectionDate,    self.edtDirectionTime,    record, 'directionDate')
        setDatetimeEditValue(self.edtPlannedEndDate,   self.edtPlannedEndTime,   record, 'plannedEndDate')
        setDatetimeEditValue(self.edtCoordDate, self.edtCoordTime, record, 'coordDate')
        setLabelText( self.lblCoordText, record, 'coordText')
        setDatetimeEditValue(self.edtBegDate,          self.edtBegTime,          record, 'begDate')
        setDatetimeEditValue(self.edtEndDate,          self.edtEndTime,          record, 'endDate')
        setRBComboBoxValue(self.cmbStatus,      record, 'status')
        setDoubleBoxValue(self.edtAmount,       record, 'amount')
        setDoubleBoxValue(self.edtUet,          record, 'uet')
        setRBComboBoxValue(self.cmbPerson,      record, 'person_id')
        setRBComboBoxValue(self.cmbSetPerson,   record, 'setPerson_id')
        setLineEditValue(self.edtOffice,        record, 'office')
        setRBComboBoxValue(self.cmbAssistant,   record, 'assistant_id')
        if actionType.requiredActionSpecification:
            actionSpecificationIdList = actionType.getActionSpecificationIdList()
            setFilter = u'id IN (%s)' % (u', '.join(str(actionSpecificationId) for actionSpecificationId in actionSpecificationIdList if actionSpecificationId is not None))
            self.cmbActionSpecification.setTable('rbActionSpecification', True, filter=setFilter)
            setRBComboBoxValue(self.cmbActionSpecification,   record, 'actionSpecification_id')
        setLineEditValue(self.edtNote,          record, 'note')
        self.edtQuantity.setValue(forceInt(record.value('quantity')))
        self.edtDuration.setValue(forceInt(record.value('duration')))
        self.edtPeriodicity.setValue(forceInt(record.value('periodicity')))
        self.edtAliquoticity.setValue(forceInt(record.value('aliquoticity')))

        mkbVisible = bool(actionType.defaultMKB)
        mkbEnabled = actionType.defaultMKB in (CActionType.dmkbByFinalDiag,
                                               CActionType.dmkbBySetPersonDiag,
                                               CActionType.dmkbUserInput
                                              )
        self.cmbMKB.setVisible(mkbVisible)
        self.lblMKB.setVisible(mkbVisible)
        self.cmbMKB.setEnabled(mkbEnabled)
        self.cmbMKB.setText(forceString(record.value('MKB')))

        morphologyMKBVisible = mkbVisible and QtGui.qApp.defaultMorphologyMKBIsVisible()
        self.cmbMorphologyMKB.setVisible(morphologyMKBVisible)
        self.lblMorphologyMKB.setVisible(morphologyMKBVisible)
        self.cmbMorphologyMKB.setEnabled(mkbEnabled)
        self.cmbMorphologyMKB.setText(forceString(record.value('morphologyMKB')))

        self.cmbOrg.setValue(forceRef(record.value('org_id')))
#        if not actionType.isRequiredCoordination:
#            self.lblCoordDate.setVisible(False)
#            self.frmCoordDate.setVisible(False)
#            self.lblCoordText.setVisible(False)
        if (self.cmbPerson.value() is None
                and actionType.defaultPersonInEditor in (CActionType.dpUndefined, CActionType.dpCurrentUser, CActionType.dpCurrentMedUser)
                and QtGui.qApp.userSpecialityId):
            self.cmbPerson.setValue(QtGui.qApp.userId)

        self.setPersonId(self.cmbPerson.value())
        self.updateClientInfo()
        self.cmbOrgStructure.setValue(forceRef(record.value('orgStructure_id')))

        self.modelActionProperties.setAction(self.action, self.clientId, self.clientSex, self.clientAge, self.eventTypeId)
        self.modelActionProperties.reset()
        self.tblProps.resizeRowsToContents()

        context = actionType.context if actionType else ''
        if QtGui.qApp.defaultKLADR()[:2] == u'23' and actionType.context == u'recipe':
            self.btnPrint.setText(u'Сохранить и распечатать')
        customizePrintButton(self.btnPrint, context)
        self.btnAttachedFiles.setAttachedFileItemList(self.action.getAttachedFileItemList())

        if QtGui.qApp.userHasRight(urLoadActionTemplate) and (self.cmbStatus.value() != CActionStatus.finished
                                                              or not self.cmbPerson.value()
                                                              or QtGui.qApp.userId == self.cmbPerson.value()
                                                              or (QtGui.qApp.userHasRight(urEditOtherPeopleActionSpecialityOnly) and QtGui.qApp.userSpecialityId == self.personSpecialityId)
                                                              or QtGui.qApp.userHasRight(urEditOtherpeopleAction)):
            actionTemplateTreeModel = self.actionTemplateCache.getModel(actionType.id)
            self.btnLoadTemplate.setModel(actionTemplateTreeModel)
        else:
            self.btnLoadTemplate.setEnabled(False)
        self.btnSaveAsTemplate.setEnabled(QtGui.qApp.userHasRight(urSaveActionTemplate))
        executionPlan = self.action.getExecutionPlan()
        self.edtQuantity.setEnabled(QtGui.qApp.userHasRight(urCopyPrevAction)
                                    and QtGui.qApp.userId == self.cmbSetPerson.value()
                                    and bool(executionPlan)
                                    and not executionPlan #executionPlan.type == CActionExecutionPlanType.type
                                    and self.cmbStatus.value() in (CActionStatus.appointed, )
                                    and not self.edtEndDate.date())
        self.edtDuration.setEnabled(QtGui.qApp.userHasRight(urCopyPrevAction)
                                    and QtGui.qApp.userId == self.cmbSetPerson.value()
                                    and not executionPlan
                                    and self.cmbStatus.value() in (CActionStatus.started, CActionStatus.appointed)
                                    and not self.edtEndDate.date())
        self.edtPeriodicity.setEnabled(QtGui.qApp.userHasRight(urCopyPrevAction)
                                       and QtGui.qApp.userId == self.cmbSetPerson.value()
                                       and not executionPlan
                                       and self.cmbStatus.value() in (CActionStatus.started, CActionStatus.appointed)
                                       and not self.edtEndDate.date())
        self.edtAliquoticity.setEnabled(QtGui.qApp.userHasRight(urCopyPrevAction)
                                        and QtGui.qApp.userId == self.cmbSetPerson.value()
                                        and not executionPlan
                                        and self.cmbStatus.value() in (CActionStatus.started, CActionStatus.appointed)
                                        and not self.edtEndDate.date())

        canEdit = not self.action.isLocked() if self.action else True
        for widget in (self.edtPlannedEndDate, self.edtPlannedEndTime,
                       self.edtBegDate, self.edtBegTime,
                       self.edtOffice,
                       self.cmbOrgStructure,
                       self.cmbAssistant,
                       self.edtUet,
                       self.cmbOrg,
                       self.buttonBox.button(QtGui.QDialogButtonBox.Ok),
                       self.chkIsUrgent
                      ):
                widget.setEnabled(canEdit)
        actionTypeId = forceRef(record.value('actionType_id')) if record else None
        actionType = CActionTypeCache.getById(actionTypeId) if actionTypeId else None
        self.cmbStatus.setEnabled(actionType.editStatus)
        self.cmbPerson.setEnabled(actionType.editExecPers)
        self.edtNote.setEnabled(actionType.editNote)
        
        self.btnLoadPrevAction.setEnabled(QtGui.qApp.userHasRight(urCopyPrevAction) and canEdit)
        self.edtAmount.setEnabled(actionType.amountEvaluation == 0 and canEdit)
        if not QtGui.qApp.userHasRight(urLoadActionTemplate) and not (self.cmbStatus.value() != CActionStatus.finished
                                                                      or not self.cmbPerson.value()
                                                                      or QtGui.qApp.userId == self.cmbPerson.value()
                                                                      or (QtGui.qApp.userHasRight(urEditOtherPeopleActionSpecialityOnly) and QtGui.qApp.userSpecialityId == self.personSpecialityId)
                                                                      or QtGui.qApp.userHasRight(urEditOtherpeopleAction)) and not canEdit:
            self.btnLoadTemplate.setEnabled(False)

        canEditPlannedEndDate = canEdit and actionType.defaultPlannedEndDate not in (CActionType.dpedBegDatePlusAmount,
                                                                                     CActionType.dpedBegDatePlusDuration)
        canEditIsExecutionPlan = not bool(self.action.getExecutionPlan() and self.action.executionPlanManager.hasItemsToDo())
        self.edtPlannedEndDate.setEnabled(canEditPlannedEndDate and canEditIsExecutionPlan)
        self.edtPlannedEndTime.setEnabled(canEditPlannedEndDate and bool(self.edtPlannedEndDate.date()) and canEditIsExecutionPlan)

        if self.edtDuration.value() > 0:
            self.btnPlanNextAction.setEnabled(True)
        else:
            self.btnPlanNextAction.setEnabled(False)
#        self.initFocus()
        self.on_edtDuration_valueChanged(forceInt(record.value('duration')))
        self.edtBegDate.setEnabled(actionType.editBegDate)
        self.edtEndDate.setEnabled(actionType.editEndDate)
        self.edtBegTime.setEnabled(bool(self.edtBegDate.date()) and canEdit and actionType.editBegDate)
        self.edtEndTime.setEnabled(bool(self.edtEndDate.date()) and canEdit and actionType.editEndDate)
        # self.edtPlannedEndTime.setEnabled(bool(self.edtPlannedEndDate.date()) and canEdit)
        if not self.action.nomenclatureExpense:
            self.btnAPNomenclatureExpense.setVisible(False)
        elif not QtGui.qApp.userHasAnyRight([urCanUseNomenclatureButton]):
            self.btnAPNomenclatureExpense.setEnabled(False)
        self.setActionCoordinationEnable(actionType.isRequiredCoordination)
        isEnable = self.btnNextActionMustBeEnabled()
        if self.action.getType().isNomenclatureExpense:
            isEnable = isEnable and self.isEnabledNomenclatureExpense(self.action)
        self.btnNextAction.setEnabled(isEnable)
        if actionType:
            stockMotionId = None
            if self.action and actionType.isNomenclatureExpense:
                recordExpense = self.action.getRecord()
                stockMotionId = forceRef(recordExpense.value('stockMotion_id'))
            self.cmbOrgStructure.setEnabled(self.cmbOrgStructure.isEnabled() and not actionType.hasJobTicketPropertyType() and not stockMotionId)
        self.btnDelete.setVisible(self.isBtnDeleteEnabled())

        tableActionTypePFSpeciality = QtGui.qApp.db.table('ActionType_PFSpeciality')
        recordes = QtGui.qApp.db.getRecordList(tableActionTypePFSpeciality, u'speciality_id', where=u'master_id = %s' % (actionType.id))
        specIdList = []
        for specid in recordes:
            specIdList.append(forceString(specid.value('speciality_id')))
        if specIdList:
            db = QtGui.qApp.db
            table = db.table('vrbPersonWithSpecialityAndPost')
            self.cmbPerson.setFilter(table['speciality_id'].inlist(specIdList))


#    def loadDialogPreferences(self):
#        CItemEditorBaseDialog.loadDialogPreferences(self)

    def getSpecialityId(self, personId):
        specialityId = None
        if personId:
            db = QtGui.qApp.db
            tablePerson = db.table('Person')
            record = db.getRecordEx(tablePerson, [tablePerson['speciality_id']],
                                    [tablePerson['deleted'].eq(0), tablePerson['id'].eq(personId)])
            specialityId = forceRef(record.value('speciality_id')) if record else None
        return specialityId


    def getRecord(self):
        record = self.record()
        showTime = self.action.getType().showTime
        eventRecord = self._getEventRecord()
        actionType = self.action.getType()
        if eventRecord:
            eventExecDate = forceDate(eventRecord.value('execDate'))
            if not eventExecDate:
                getDatetimeEditValue(self.edtDirectionDate, self.edtDirectionTime, record, 'directionDate', showTime)
        getDatetimeEditValue(self.edtPlannedEndDate, self.edtPlannedEndTime, record, 'plannedEndDate', showTime)
        getDatetimeEditValue(self.edtBegDate, self.edtBegTime, record, 'begDate', showTime)
        getDatetimeEditValue(self.edtEndDate, self.edtEndTime, record, 'endDate', showTime)
        getDatetimeEditValue(self.edtCoordDate, self.edtCoordTime, record, 'coordDate', showTime)
        record.setValue('coordText', QVariant(self.lblCoordText.text()))
        getCheckBoxValue(self.chkIsUrgent,      record, 'isUrgent')
        getRBComboBoxValue(self.cmbStatus,      record, 'status')
        getDoubleBoxValue(self.edtAmount,       record, 'amount')
        getDoubleBoxValue(self.edtUet,          record, 'uet')
        getRBComboBoxValue(self.cmbPerson,      record, 'person_id')
        getRBComboBoxValue(self.cmbSetPerson,   record, 'setPerson_id')
        getRBComboBoxValue(self.cmbAssistant,   record, 'assistant_id')
        if actionType.requiredActionSpecification:
            getRBComboBoxValue(self.cmbActionSpecification,   record, 'actionSpecification_id')
        getLineEditValue(self.edtOffice,        record, 'office')
        getLineEditValue(self.edtNote,          record, 'note')
        record.setValue('MKB', QVariant(self.cmbMKB.text()))
        record.setValue('morphologyMKB', QVariant(self.cmbMorphologyMKB.validText()))
        record.setValue('org_id', QVariant(self.cmbOrg.value()))
        record.setValue('quantity', toVariant(self.edtQuantity.value()))
        record.setValue('duration', toVariant(self.edtDuration.value()))
        record.setValue('periodicity', toVariant(self.edtPeriodicity.value()))
        record.setValue('aliquoticity', toVariant(self.edtAliquoticity.value()))
        record.setValue('orgStructure_id', toVariant(self.cmbOrgStructure.value()))
        # Это хак: удаляем payStatus из записи
        result = type(record)(record) # copy record
        result.remove(result.indexOf('payStatus'))
        return result


    def saveInternals(self, id):
        # TODO: Почему так? saveInternals должно вызываться уже после того как checkDataEntered вызвано.
        if self.checkDataEntered(secondTry=True):
            id = self.action.save(self.eventId, self.idx, checkModifyDate=False)
            checkTissueJournalStatusByActions([(self.action.getRecord(), self.action)])
            eventRecord = self._getEventRecord()
            if self.action.getType().closeEvent:
                if eventRecord:
                    eventExecDate = forceDate(eventRecord.value('execDate'))
                    if not eventExecDate and self._eventExecDate:
                        eventRecord.setValue('execDate', QVariant(self._eventExecDate))
                        eventRecord.setValue('isClosed', QVariant(1))
                    #
            if eventRecord:
                QtGui.qApp.db.updateRecord('Event', eventRecord)

            if self.newAction:
                self.newAction.executionPlanManager.setCurrentItemIndex()
                idx = QtGui.qApp.db.getCount(
                    'Action', where='deleted=0 and event_id=%d' % self.eventId
                )
                self.newActionId = self.newAction.save(idx=idx)
        return id


    def updateClientInfo(self):
        db = QtGui.qApp.db
        self.clientInfo = getClientInfo(self.clientId, date=self.edtDirectionDate.date())
        self.txtClientInfoBrowser.setHtml(formatClientBanner(self.clientInfo))
        table  = db.table('Client')
        record = db.getRecord(table, '*', self.clientId)
        if record:
            directionDate = self.edtDirectionDate.date()
            self.clientSex       = forceInt(record.value('sex'))
            self.clientBirthDate = forceDate(record.value('birthDate'))
            self.clientAge       = calcAgeTuple(self.clientBirthDate, directionDate)
#            self.actionTemplateCache.reset()
        self.actShowAttachedToClientFiles.setMasterId(self.clientId)
        self.clientDeathDate = getDeathDate(self.clientId)


    def updateAmount(self):
        def getActionDuration(weekProfile):
            startDate = self.edtBegDate.date()
            stopDate  = self.edtEndDate.date()
            if startDate and stopDate:
                return getEventDuration(startDate, stopDate, weekProfile, self.eventTypeId)
            else:
                return 0

        def setAmount(amount):
            self.edtAmount.setValue(amount)

        actionType = self.action.getType()

        if actionType.amountEvaluation == CActionType.actionPredefinedNumber:
            setAmount(actionType.amount)
        elif actionType.amountEvaluation == CActionType.actionDurationWithFiveDayWorking:
            setAmount(actionType.amount*getActionDuration(wpFiveDays))
        elif actionType.amountEvaluation == CActionType.actionDurationWithSixDayWorking:
            setAmount(actionType.amount*getActionDuration(wpSixDays))
        elif actionType.amountEvaluation == CActionType.actionDurationWithSevenDayWorking:
            setAmount(actionType.amount*getActionDuration(wpSevenDays))
        elif actionType.amountEvaluation == CActionType.actionFilledPropsCount:
            setAmount(actionType.amount*self.action.getFilledPropertiesCount())
        elif actionType.amountEvaluation == CActionType.actionAssignedPropsCount:
            setAmount(actionType.amount*self.action.getAssignedPropertiesCount())

        if actionType.defaultPlannedEndDate == CActionType.dpedBegDatePlusAmount:
            begDate = self.edtBegDate.date()
            amountValue = int(self.edtAmount.value())
            date = begDate.addDays(amountValue-1) if begDate and amountValue else QDate()
            self.edtPlannedEndDate.setDate(date)
        elif actionType.defaultPlannedEndDate == CActionType.dpedBegDatePlusDuration:
            begDate = self.edtBegDate.date()
            durationValue = self.edtDuration.value()
            date = begDate.addDays(durationValue) if begDate else QDate()
            self.edtPlannedEndDate.setDate(date)


    def checkDataEntered(self, secondTry=False):
        result = True
        begDate = self.edtBegDate.date()
        endDate = self.edtEndDate.date()
        if endDate:
            if QtGui.qApp.isStrictCheckPolicyOnEndAction() in (0, 1):
                if not checkPolicyOnDate(self.clientId, endDate):
                    skippable = QtGui.qApp.isStrictCheckPolicyOnEndAction() == 0
                    result = result and self.checkInputMessage(u'время закрытия действия соответствующее полису',
                                                               skippable, self.edtEndDate)
            if QtGui.qApp.isStrictCheckAttachOnEndAction() in (0, 1):
                if not checkAttachOnDate(self.clientId, endDate):
                    skippable = QtGui.qApp.isStrictCheckAttachOnEndAction() == 0
                    result = result and self.checkInputMessage(u'время закрытия действия соответствующее прикреплению',
                                                               skippable, self.edtEndDate)
        showTime = self.action._actionType.showTime and getEventShowTime(self.eventTypeId)
        if showTime:
            begDate = toDateTimeWithoutSeconds(QDateTime(begDate, self.edtBegTime.time()))
            endDate = toDateTimeWithoutSeconds(QDateTime(endDate, self.edtEndTime.time()))
            result = result and (endDate.isNull() or endDate >= begDate or self.checkValueMessage(u'Дата выполнения действия %s не должна быть раньше даты начала действия % s'%(forceString(endDate), forceString(begDate)), False, self.edtEndTime))
        if begDate and endDate:
            if showTime:
                result = result and (endDate.isNull() or endDate >= begDate or self.checkValueMessage(u'Дата выполнения действия %s не должна быть раньше даты начала действия % s'%(forceString(endDate), forceString(begDate)), False, self.edtEndTime))
            else:
                result = result and (endDate.isNull() or endDate >= begDate or self.checkValueMessage(u'Дата выполнения действия %s не должна быть раньше даты начала действия % s'%(forceString(endDate), forceString(begDate)), False, self.edtEndDate))
        if result and self.eventId:
            db = QtGui.qApp.db
            record = db.getRecord('Event', 'setDate, execDate, eventType_id',  self.eventId)
            if record:
                actionType = self.action.getType()
                eventTypeId = forceRef(record.value('eventType_id'))
                self.eventPurposeId = getEventPurposeId(eventTypeId)
                setDate = forceDateTime(record.value('setDate')) if showTime else forceDate(record.value('setDate'))
                execDate = forceDateTime(record.value('execDate')) if showTime else forceDate(record.value('execDate'))
                if execDate and setDate:
                    if actionType and u'received' in actionType.flatCode.lower():
                        isControlActionReceivedBegDate = QtGui.qApp.isControlActionReceivedBegDate()
                        if isControlActionReceivedBegDate:
                            eventBegDate = forceDateTime(record.value('setDate')) if showTime else forceDate(record.value('setDate'))
                            eventBegDate = toDateTimeWithoutSeconds(eventBegDate)
                            actionBegDate = begDate
                            if eventBegDate != actionBegDate:
                                if isControlActionReceivedBegDate == 1:
                                    message = u'Дата начала случая обслуживания %s не совпадает с датой начала действия Поступление %s. Исправить?'%(forceString(eventBegDate), forceString(actionBegDate))
                                    skippable = True
                                else:
                                    message = u'Дата начала случая обслуживания %s не совпадает с датой начала действия Поступление %s. Необходимо исправить.'%(forceString(eventBegDate), forceString(actionBegDate))
                                    skippable = False
                                result = result and self.checkValueMessage(message, skippable, self.edtBegDate)

                if setDate and endDate:
                    result = result and (endDate.isNull() or endDate >= setDate or self.checkValueMessage(u'Дата выполнения действия %s не должна быть раньше даты начала события % s'%(forceString(endDate), forceString(setDate)), True, self.edtEndDate))
                actionsBeyondEvent = getEventEnableActionsBeyondEvent(self.eventTypeId)
                if execDate and endDate and actionsBeyondEvent:
                    result = result and (endDate.isNull() or execDate >= endDate or self.checkValueMessage(u'Дата выполнения действия %s не должна быть позже даты выполнения события % s'%(forceString(endDate), forceString(execDate)), True if actionsBeyondEvent == 1 else False, self.edtEndDate))
                elif setDate and endDate:
                    currentDate = QDate.currentDate()
                    if currentDate and not secondTry:
                        endDateCur = endDate.date() if showTime else endDate
                        # secondTry - это заглушка потому что я "ниасилил" по каким причинам сделали чтобы checkDataEntered вызывается два раза.
                        # Поправте, пожалуйста, чтобы вызывался один раз.
                        # Я верю что были серьезные причины, но это не правильно.
                        if not self._saveAsExecutionPlan:
                            result = result and (endDateCur.isNull() or currentDate >= endDateCur or self.checkValueMessage(
                                u'Дата выполнения действия %s не должна быть позже текущей даты % s'%(forceString(endDateCur), forceString(currentDate)), True, self.edtEndDate)
                            )
                actionRecord = self.action.getRecord()
                status = forceInt(actionRecord.value('status'))
                actionShowTime = self.action._actionType.showTime
                directionDate = QDateTime(self.edtDirectionDate.date(), self.edtDirectionTime.time()) if actionShowTime else self.edtDirectionDate.date()
                nameActionType = actionType.name
                eventEditDialog = CEventEditDialog(self)
                eventEditDialog.setClientBirthDate(self.clientBirthDate)
                eventEditDialog.setClientDeathDate(self.clientDeathDate)
                eventEditDialog.setEventPurposeId(self.eventPurposeId)
                eventEditDialog.setClientSex(self.clientSex)
                eventEditDialog.setClientAge(self.clientAge)
                eventEditDialog.setEventTypeIdToAction(eventTypeId)
                if execDate and u'leaved' in actionType.flatCode.lower():
                    result = result and CEventEditDialog(self).checkLeavedEndDate(execDate, None, self.action, None, self.edtEndDate)
                result = result and CEventEditDialog(self).checkActionDataEntered(directionDate, begDate, endDate, None, self.edtDirectionDate, self.edtBegDate, self.edtEndDate, None, 0)
                result = result and CEventEditDialog(self).checkEventActionDateEntered(setDate, execDate, status, directionDate, begDate, endDate, None, self.edtEndDate, self.edtBegDate, None, 0, nameActionType, actionShowTime=actionShowTime, enableActionsBeyondEvent=actionsBeyondEvent)
#        result = result and (begDate or self.checkInputMessage(u'дату назначения', False, self.edtBegDate))
#        result = result and (endDate or self.checkInputMessage(u'дату выполнения', False, self.edtEndDate))
#        if not endDate:
#            maxEndDate = self.getMaxEndDateByVisits()
#            if maxEndDate:
#                if QtGui.QMessageBox.question(self,
#                                    u'Внимание!',
#                                    u'Дата выполнения обращения не указана.\nУстановить дату завершения по максимальной дате посещений',
#                                    QtGui.QMessageBox.No|QtGui.QMessageBox.Yes,
#                                    QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes:
#                    self.edtEndDate.setDate(maxEndDate)
#                    endDate = maxEndDate
        result = result and CEventEditDialog(self).checkActionProperties(None, self.action, self.tblProps, None)
        result = result and self.checkActualMKB()
        result = result and self.checkActionMKB()
        result = result and self.checkActionMorphology()
        result = result and self.checkSetPerson()
        result = result and self.checkExecPerson()
        result = result and self.checkPlannedEndDate()
        return result


    def checkPlannedEndDate(self):
        action = self.action
        if action:
            actionType = action.getType()
            if actionType and actionType.isPlannedEndDateRequired in [CActionType.dpedControlMild, CActionType.dpedControlHard]:
                if not self.edtPlannedEndDate.date():
                    skippable = True if actionType.isPlannedEndDateRequired == CActionType.dpedControlMild else False
                    message = u'Необходимо указать Плановую дату выполнения у действия %s'%(actionType.name)
                    return self.checkValueMessage(message, skippable, self.edtPlannedEndDate)
        return True


    def checkActionMorphology(self):
        actionStatus = self.cmbStatus.value()
        if QtGui.qApp.defaultMorphologyMKBIsVisible() \
           and actionStatus in (CActionStatus.finished, CActionStatus.withoutResult):
            action = self.action
            actionType = action.getType()
            defaultMKB = actionType.defaultMKB
            isMorphologyRequired = actionType.isMorphologyRequired
            morphologyMKB = self.cmbMorphologyMKB.text()
            if not self.cmbMorphologyMKB.isValid(morphologyMKB) and defaultMKB > 0 and isMorphologyRequired > 0:
                if actionStatus == CActionStatus.withoutResult and isMorphologyRequired == 2:
                    return True
                skippable = True if isMorphologyRequired == 1 else False
                message = u'Необходимо ввести корректную морфологию диагноза действия `%s`' % actionType.name
                return self.checkValueMessage(message, skippable, self.cmbMorphologyMKB)
        return True
    
    
    def checkActionMKB(self):
        actionStatus = self.cmbStatus.value()
        if actionStatus in (CActionStatus.finished, CActionStatus.withoutResult):
            action = self.action
            actionType = action.getType()
            isMKBRequired = actionType.isMKBRequired
            MKB = self.cmbMKB.text()
            if not MKB and isMKBRequired > 0:
                if actionStatus == CActionStatus.withoutResult and isMKBRequired == 2:
                    return True
                skippable = True if isMKBRequired == 1 else False
                message = u'Необходимо ввести корректную МКБ действия `%s`' % actionType.name
                return self.checkValueMessage(message, skippable, self.cmbMKB)
        return True
    
    
    def checkExecPerson(self):
        actionStatus = self.cmbStatus.value()
        if actionStatus in (CActionStatus.finished, CActionStatus.withoutResult):
            actionType = self.action.getType()
            ExecPerson = self.cmbPerson.value()
            isExecPersonRequired = actionType.isExecPersonRequired
            if not ExecPerson and isExecPersonRequired > 0:
                if actionStatus == CActionStatus.withoutResult and isExecPersonRequired == 2:
                    return True
                skippable = True if isExecPersonRequired == 1 else False
                message = u'Необходимо указать корректного исполнителя действия `%s`' % actionType.name
                return self.checkValueMessage(message, skippable, self.cmbPerson)
        return True


    def checkSetPerson(self):
        setPerson = self.cmbSetPerson.value()
        if not setPerson:
            actionType = self.action.getType()
            if actionType and actionType.defaultSetPersonInEvent != CActionType.dspUndefined:
                message = u'Необходимо указать назначившего действия `%s`' % actionType.name
                return self.checkValueMessage(message, False, self.cmbSetPerson)
        return True


    def checkActualMKB(self):
        result = True
        MKB = unicode(self.cmbMKB.text())
        if MKB:
            db = QtGui.qApp.db
            tableMKB = db.table('MKB')
            cond = [tableMKB['DiagID'].eq(MKBwithoutSubclassification(MKB))]
            cond.append(db.joinOr([tableMKB['endDate'].isNull(), tableMKB['endDate'].dateGe(self.edtBegDate.date())]))
            recordMKB = db.getRecordEx(tableMKB, [tableMKB['DiagID']], cond)
            result = result and (forceString(recordMKB.value('DiagID')) == MKBwithoutSubclassification(MKB) if recordMKB else False) or self.checkValueMessage(u'Диагноз %s не доступен для применения' % MKB, False, self.cmbMKB)

            # проверка на "оплачиваемость" диагноза в системе ОМС для КК
            eventRecord = self._getEventRecord()
            if eventRecord:
                contractId = forceRef(eventRecord.value('contract_id'))
                financeId = forceRef(self.record().value('finance_id'))
                if financeId is None:
                    financeId = forceRef(db.translate('Contract', 'id', contractId, 'finance_id'))
                if result and QtGui.qApp.provinceKLADR()[:2] == u'23' and CFinanceType.getCode(financeId) == 2:
                    tableSpr20 = db.table('soc_spr20')
                    cond = [db.joinOr([tableSpr20['code'].eq(MKB), tableSpr20['code'].eq(MKB[:3])]),
                            db.joinOr([tableSpr20['dato'].isNull(), tableSpr20['dato'].dateGe(self.edtBegDate.date())]),
                            tableSpr20['datn'].dateLe(self.edtBegDate.date())]
                    recordMKB = db.getRecordEx(tableSpr20, [tableSpr20['code']], cond)
                    if not recordMKB:
                        result = self.checkValueMessage(u'Диагноз %s не оплачивается в системе ОМС!' % MKB, QtGui.qApp.userHasRight(urCanSaveEventWithMKBNotOMS), self.cmbMKB)
        return result


    def onActionDataChanged(self, name, value):
        CItemEditorBaseDialog.getRecord(self).setValue(name, toVariant(value))
        if self.action.getType().defaultSetPersonInEvent == CActionType.dspExecPerson and name in ('person_id'):
            self.cmbSetPerson.setValue(self.cmbPerson.value())


    def setPersonId(self, personId):
        self.personId = personId
        record = QtGui.qApp.db.getRecord('Person', 'speciality_id, tariffCategory_id, SNILS, showTypeTemplate',  self.personId)
        if record:
            self.personSpecialityId     = forceRef(record.value('speciality_id'))
            self.personTariffCategoryId = forceRef(record.value('tariffCategory_id'))
            self.personSNILS            = forceStringEx(record.value('SNILS'))
            self.showTypeTemplate       = forceInt(record.value('showTypeTemplate'))
            self.actionTemplateCache.setPersonSNILS(self.personSNILS)
            self.actionTemplateCache.setShowTypeTemplate(self.showTypeTemplate)
        # self.actionTemplateCache.reset()

    def getEventInfo(self, context):
        return self.eventInfo

    def setEventInfo(self, eventInfo):
        self.eventInfo = eventInfo
        self.eventInfo.actions._items.insert(0, CActionRecordItem(self.getRecord(), self.action))
        self.eventInfo.actions._rawItems.insert(0, (self.getRecord(), self.action))


    def setCurrentProperty(self, row, column=1):
        index = self.modelActionProperties.index(row, column)
        self.tblProps.setCurrentIndex(index)
# # #


    @pyqtSignature('')
    def on_actEditClient_triggered(self):
        if QtGui.qApp.userHasAnyRight([urAdmin, urRegTabWriteRegistry, urRegTabReadRegistry]):
            dialog = CClientEditDialog(self)
            try:
                dialog.load(self.clientId)
                if dialog.exec_():
                    self.updateClientInfo()
            finally:
                dialog.deleteLater()

    @pyqtSignature('')
    def on_actPortal_Doctor_triggered(self):
        templateId = None
        result = QtGui.qApp.db.getRecordEx('rbPrintTemplate', 'id',
                                           '`default` LIKE "%s" AND deleted = 0' % ('%/EMK_V3/indexV2.php%'))
        context = CInfoContext()
        eventInfo = context.getInstance(CEventInfo, self.eventId)
        data = {'event': eventInfo,
                'client': eventInfo.client
                }

        if result:
            templateId = result.value('id').toString()
            if templateId:
                QtGui.qApp.call(self, applyTemplate, (self, templateId, data))
            else:
                QtGui.QMessageBox.information(self, u'Ошибка', u'Шаблон для перехода на портал врача не найден',
                                              QtGui.QMessageBox.Close, QtGui.QMessageBox.Close)
        else:
            QtGui.QMessageBox.information(self, u'Ошибка', u'Шаблон для перехода на портал врача не найден',
                                          QtGui.QMessageBox.Close, QtGui.QMessageBox.Close)


    @pyqtSignature('double')
    def on_edtAmount_valueChanged(self, value):
        actionType = self.action.getType()
        if actionType.defaultPlannedEndDate == CActionType.dpedBegDatePlusAmount:
            begDate = self.edtBegDate.date()
            amountValue = int(value)
            date = begDate.addDays(amountValue-1) if begDate and amountValue else QDate()
            self.edtPlannedEndDate.setDate(date)


    @pyqtSignature('QString')
    def on_cmbMKB_textChanged(self, value):
        if value[-1:] == '.':
            value = value[:-1]
        diagName = forceString(QtGui.qApp.db.translate('MKB', 'DiagID', value, 'DiagName'))
        if diagName:
            self.lblMKBText.setText(diagName)
        else:
            self.lblMKBText.clear()
        self.cmbMorphologyMKB.setMKBFilter(self.cmbMorphologyMKB.getMKBFilter(unicode(value)))


    def on_cmbMKB_editingFinished(self):
        if self.focusWidget() != self.cmbMKB:
            if not self.isCmbMKBTextChanged:
                value = self.cmbMKB.text()
                if value[-1:] == '.':
                    value = value[:-1]
                if value and len(value) >= 3:
                    diagFilter = u''
                    if self.personSpecialityId:
                        diagFilter = forceString(QtGui.qApp.db.translate('rbSpeciality', 'id', self.personSpecialityId, 'mkbFilter'))
                    self.isCmbMKBTextChanged = True
                    acceptable = checkDiagnosis(self, unicode(value), diagFilter, self.clientId, self.clientSex, self.clientAge, self.eventSetDate)
                    if not acceptable:
                        self.cmbMKB.setText(u'')
                        CDialogBase(self).setFocusToWidget(self.cmbMKB)
        self.isCmbMKBTextChanged = False


    @pyqtSignature('')
    def on_btnSelectOrg_clicked(self):
        orgId = selectOrganisation(self, self.cmbOrg.value(), False, self.cmbOrg.filter)
        self.cmbOrg.updateModel()
        if orgId:
            self.cmbOrg.setValue(orgId)


    @pyqtSignature('int')
    def on_cmbOrgStructure_currentIndexChanged(self, index):
        record = self.getRecord()
        orgStructureId = self.cmbOrgStructure.value()
        if forceRef(record.value('orgStructure_id')) != orgStructureId:
            record.setValue('orgStructure_id', toVariant(orgStructureId))
            self.action.getRecord().setValue('orgStructure_id', toVariant(orgStructureId))
            if orgStructureId and self.action and self.action.getType().isNomenclatureExpense:
                recordExpense = self.action.getRecord()
                stockMotionId = forceRef(recordExpense.value('stockMotion_id'))
                if not stockMotionId:
                    if self.action.nomenclatureClientReservation:
                        self.action.nomenclatureClientReservation.cancel()
                        self.action.nomenclatureClientReservation = None
                        financeId = self.action.getFinanceId()
                        if self.action.getMedicalAidKindId():
                            medicalAidKindId = self.action.getMedicalAidKindId()
                        else:
                            medicalAidKindId = getEventMedicalAidKindId(self.eventTypeId)
                        self.action.initNomenclatureReservation(self.clientId, financeId=financeId,
                                                                medicalAidKindId=medicalAidKindId, supplierId=orgStructureId)
                    if self.action.nomenclatureExpense:
                        self.action.nomenclatureExpense.setSupplierId(orgStructureId)


    @pyqtSignature('int')
    def on_cmbPerson_currentIndexChanged(self):
        self.onActionDataChanged('person_id', self.cmbPerson.value())

        self.setPersonId(self.cmbPerson.value())
        actionTemplateTreeModel = self.actionTemplateCache.getModel(self.action.getType().id)
        self.btnLoadTemplate.setModel(actionTemplateTreeModel)
        if not(QtGui.qApp.userHasRight(urLoadActionTemplate) and (self.cmbStatus.value() != CActionStatus.finished
                                                                  or not self.cmbPerson.value()
                                                                  or QtGui.qApp.userId == self.cmbPerson.value()
                                                                  or (QtGui.qApp.userHasRight(urEditOtherPeopleActionSpecialityOnly) and QtGui.qApp.userSpecialityId == self.personSpecialityId)
                                                                  or QtGui.qApp.userHasRight(urEditOtherpeopleAction))):
            self.btnLoadTemplate.setEnabled(False)


    @pyqtSignature('int')
    def on_cmbSetPerson_currentIndexChanged(self):
        self.onActionDataChanged('setPerson_id', self.cmbSetPerson.value())


    @pyqtSignature('bool')
    def on_chkIsUrgent_toggled(self, checked):
        self.onActionDataChanged('isUrgent', checked)


    @pyqtSignature('QDate')
    def on_edtDirectionDate_dateChanged(self, date):
        self.edtDirectionTime.setEnabled(bool(date))


    @pyqtSignature('QDate')
    def on_edtBegDate_dateChanged(self, date):
        self.edtBegTime.setEnabled(bool(date))
        self.updateAmount()
        self.cmbMKB.setFilter('''IF(MKB.endDate IS NOT NULL, MKB.endDate >= %s, 1)'''%(QtGui.qApp.db.formatDate(self.edtBegDate.date())))


    @pyqtSignature('QDate')
    def on_edtEndDate_dateChanged(self, date):
        self.edtEndTime.setEnabled(bool(date))
        self.updateAmount()
        if date:
            self.cmbStatus.setValue(CActionStatus.finished)
            if self.eventSetDate and date < self.eventSetDate:
                self.edtBegDate.setDate(QDate())
                self.edtBegTime.setTime(QTime())
                self.edtDirectionDate.setDate(QDate())
                self.edtDirectionTime.setTime(QTime())
            if self.cmbStatus.value() == CActionStatus.finished:
                self.freeJobTicket(QDateTime(self.edtEndDate.date(), self.edtEndTime.time()) if self.edtEndTime.isVisible() else self.edtEndDate.date())
        else:
            if self.cmbStatus.value() == CActionStatus.finished:
                self.cmbStatus.setValue(CActionStatus.canceled)

        isEnable = self.btnNextActionMustBeEnabled()
        if self.action.getType().isNomenclatureExpense:
            isEnable = isEnable and self.isEnabledNomenclatureExpense(self.action)
        self.btnNextAction.setEnabled(isEnable)

        if self.edtDuration.value() > 0:
            self.btnPlanNextAction.setEnabled(True)
        else:
            self.btnPlanNextAction.setEnabled(False)

        if self.action.getType().closeEvent:
            self.setEventDate(date)


    @pyqtSignature('int')
    def on_cmbStatus_currentIndexChanged(self, index):
        actionStatus = self.cmbStatus.value()
        if actionStatus in (CActionStatus.finished, CActionStatus.withoutResult):
            if not self.edtEndDate.date():
                now = QDateTime.currentDateTime()
                self.edtEndDate.setDate(now.date())
                if self.edtEndTime.isVisible():
                    self.edtEndTime.setTime(now.time())
        elif actionStatus in (CActionStatus.canceled, CActionStatus.refused):
            self.edtEndDate.setDate(QDate())
            self.edtEndTime.setTime(QTime())
            if QtGui.qApp.userId and QtGui.qApp.userSpecialityId:
                self.cmbPerson.setValue(QtGui.qApp.userId)
            else:
                self.cmbPerson.setValue(self.cmbSetPerson.value())
        else:
            self.edtEndDate.setDate(QDate())
            self.edtEndTime.setTime(QTime())

        isEnable = self.btnNextActionMustBeEnabled()
        if self.action.getType().isNomenclatureExpense:
            isEnable = isEnable and self.isEnabledNomenclatureExpense(self.action)
        self.btnNextAction.setEnabled(isEnable)


    def freeJobTicket(self, endDate):
        if self.action:
            jobTicketIdList = []
            jobTicketId = None
            for property in self.action.getType()._propertiesById.itervalues():
                if property.isJobTicketValueType():
                    jobTicketId = self.action[property.name]
                    if jobTicketId and jobTicketId not in jobTicketIdList:
                        jobTicketIdList.append(jobTicketId)
            db = QtGui.qApp.db
            tableJobTicket = db.table('Job_Ticket')
            cond = [tableJobTicket['id'].eq(jobTicketId),
                    tableJobTicket['deleted'].eq(0)
                    ]
            if self.edtEndTime.isVisible():
                cond.append(tableJobTicket['datetime'].ge(endDate))
            else:
                cond.append(tableJobTicket['datetime'].dateGe(endDate))
            records = db.getRecordList(tableJobTicket, '*', cond)
            for record in records:
                datetime = forceDateTime(record.value('datetime')) if self.edtEndTime.isVisible() else forceDate(record.value('datetime'))
                if datetime > endDate:
                    self.action[property.name] = None
            self.tblProps.model().reset()


    @pyqtSignature('')
    def on_btnAllocateIdMq_clicked(self):
        action = self.action
        flatCode = action.actionType().flatCode
        hospitalBedProfileId = action[u'Профиль'] if action.hasProperty(u'Профиль') else None
        specialityId         = action[u'Профиль'] if action.hasProperty(u'Профиль') else None
        serviceId            = action[u'Услуга']  if action.hasProperty(u'Услуга') else None

        serviceUrl = QtGui.qApp.getMqHelperUrl()
        client = CJsonRpcClent(serviceUrl)
        try:
            result = client.call('allocateIdMq',
                                 params={ 'clientId'            : self.clientId,
                                          'actionTypeFlatCode'  : flatCode,
                                          'hospitalBedProfileId': hospitalBedProfileId,
                                          'specialityId'        : specialityId,
                                          'serviceId'           : serviceId
                                        }
                                )
            action[u'Идентификатор УО'] = result['IdMq']
#            self.tblProps.update()
        except Exception as e:
            QtGui.QMessageBox.critical(self,
                    u'Ошибка регистрации направления',
                    exceptionToUnicode(e),
                    QtGui.QMessageBox.Ok,
                    QtGui.QMessageBox.Ok)


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_modelActionProperties_dataChanged(self, topLeft, bottomRight):
        record = self.getRecord()
        if record and self.action:
            property = self.modelActionProperties.getPropertyType(self.tblProps.currentIndex().row())
            if self.action and record and property and property.isJobTicketValueType():
                prop = self.action.getPropertyById(property.id)
                if prop:
                    jobTicketId = prop.getValue()
                    jobTicketOrgStructureId = self.action.getJobTicketOrgStructureId(jobTicketId) if jobTicketId else None
                    if jobTicketOrgStructureId:
                        record.setValue('orgStructure_id', toVariant(jobTicketOrgStructureId))
                        self.action.getRecord().setValue('orgStructure_id', toVariant(jobTicketOrgStructureId))
        self.updateAmount()
        property = self.modelActionProperties.getPropertyType(self.tblProps.currentIndex().row())
        if self.action and self.action.getType().isDoesNotInvolveExecutionCourse and self.action.nomenclatureExpense and record and property and property.inActionsSelectionTable == _DOSES: # doses
            self.action = updateNomenclatureDosageValue(self.action)

    @pyqtSignature('int')
    def on_btnPrint_printByTemplate(self, templateId):
        context = CInfoContext()

        if not self.eventInfo:
            self.eventInfo = context.getInstance(CEventInfo, self.eventId)
            if not self.eventInfo.actions:
                self.eventInfo.actions._idList.append(self.itemId())
                self.eventInfo.actions._items.append(CCookedActionInfo(context, self.getRecord(), self.action))
                self.eventInfo.actions._loaded = True
                action = self.eventInfo.actions[0]
                currentActionIndex = 0
            else:
                for i, actionId in enumerate(self.eventInfo.actions._idList):
                    if actionId == self.itemId():
                        self.eventInfo.actions._idList[i] = self.itemId()
                        self.eventInfo.actions._items[i] = CCookedActionInfo(context, self.getRecord(), self.action)
                        self.eventInfo.actions._loaded = True
                        action = self.eventInfo.actions[i]
                        currentActionIndex = i

        eventInfo = self.eventInfo
        eventActions = eventInfo.actions
        if isinstance(eventActions, CActionInfoList):
            for i, act in enumerate(eventActions._items):
                if act._action == self.action:
                    eventActions._idList[i] = self.itemId()
                    eventActions._items[i] = CCookedActionInfo(context, self.getRecord(), self.action)
                    eventActions._loaded = True
                    action = eventInfo.actions[i]
                    currentActionIndex = i
        elif isinstance(eventActions, CActionInfoProxyList):
            for i, (rec, act) in enumerate(eventActions._rawItems):
                if act == self.action:
                    eventActions._rawItems[i] = (self.getRecord(), self.action)
                    eventActions._items[i] = CCookedActionInfo(context, self.getRecord(), self.action)
                    action = eventInfo.actions[i]
                    currentActionIndex = i

        action._isDirty = self.isDirty()
        action.setCurrentPropertyIndex(self.tblProps.currentIndex().row())
        data = {'event': eventInfo,
                'action': action,
                'client': eventInfo.client,
                'actions': eventActions,
                'currentActionIndex': currentActionIndex,
                'tempInvalid': None
                }
        applyTemplate(self, templateId, data, signAndAttachHandler=self.btnAttachedFiles.getSignAndAttachHandler())


    @pyqtSignature('')
    def on_btnLoadTemplate_clicked(self):
        if QtGui.qApp.userHasRight(urLoadActionTemplate) and (self.cmbStatus.value() != CActionStatus.finished
                                                              or not self.cmbPerson.value()
                                                              or QtGui.qApp.userId == self.cmbPerson.value()
                                                              or (QtGui.qApp.userHasRight(urEditOtherPeopleActionSpecialityOnly) and QtGui.qApp.userSpecialityId == self.personSpecialityId)
                                                              or QtGui.qApp.userHasRight(urEditOtherpeopleAction)):
            record = self.getRecord()
            templateAction = None
            isMethodRecording = CAction.actionNoMethodRecording
            db = QtGui.qApp.db
            personId = QtGui.qApp.userId if QtGui.qApp.userSpecialityId else self.personId
            specialityId = QtGui.qApp.userSpecialityId if QtGui.qApp.userSpecialityId else self.personSpecialityId
            personSNILS  = forceString(db.translate(db.table('Person'), 'id', personId, 'SNILS')) if QtGui.qApp.userSpecialityId else self.personSNILS
            dlg = CActionTemplateSelectDialog(parent=self,
                                            actionRecord=record,
                                            action=self.action,
                                            clientSex=self.clientSex,
                                            clientAge=self.clientAge,
                                            personId=personId,
                                            specialityId=specialityId,
                                            orgStructureId=QtGui.qApp.currentOrgStructureId(),
                                            SNILS=personSNILS,
                                            showTypeTemplate=self.showTypeTemplate,
                                            model=self.actionTemplateCache.getModel(self.action.getType().id)
                                           )
            try:
                if dlg.exec_():
                    templateAction = dlg.getSelectAction()
                    isMethodRecording = dlg.getMethodRecording()
            finally:
                dlg.deleteLater()
            if templateAction:
                self.action.updateByAction(templateAction, checkPropsOnOwner=True, clientSex=self.clientSex, clientAge=self.clientAge, isMethodRecording=isMethodRecording)
            self.tblProps.model().reset()
            self.tblProps.resizeRowsToContents()
            self.updateAmount()


    def getPrevActionId(self, action, type):
        self.getPrevActionIdHelper._clientId = self.clientId
        return self.getPrevActionIdHelper.getPrevActionId(action, type)


    def loadPrevAction(self, type):
        if QtGui.qApp.userHasRight(urCopyPrevAction):
                prevActionId = self.getPrevActionId(self.action, type)
                if prevActionId:
                    self.action.updateByActionId(prevActionId)
                    self.tblProps.model().reset()
                    self.tblProps.resizeRowsToContents()


    @pyqtSignature('')
    def on_mnuLoadPrevAction_aboutToShow(self):
        self.actLoadSameSpecialityPrevAction.setEnabled(bool(
                self.action and self.getPrevActionId(self.action, CGetPrevActionIdHelper.sameSpecialityPrevAction))
                                                         )
        self.actLoadOwnPrevAction.setEnabled(bool(
                self.action and self.getPrevActionId(self.action, CGetPrevActionIdHelper.ownPrevAction))
                                              )

        self.actLoadAnyPrevAction.setEnabled(bool(
                self.action and self.getPrevActionId(self.action, CGetPrevActionIdHelper.anyPrevAction))
                                              )
        if self.action:
            check_Yes = False
            for prop in self.action.getPropertiesBydataInheritance():
                if u'in_' in prop:
                    check_Yes = True
            if check_Yes:
                self.actCopyInputActionProperty.setEnabled(True)
            else:
                self.actCopyInputActionProperty.setEnabled(False)
        else:
            self.actCopyInputActionProperty.setEnabled(False)


    @pyqtSignature('')
    def on_actLoadSameSpecialityPrevAction_triggered(self):
        self.loadPrevAction(CGetPrevActionIdHelper.sameSpecialityPrevAction)


    @pyqtSignature('')
    def on_actLoadOwnPrevAction_triggered(self):
        self.loadPrevAction(CGetPrevActionIdHelper.ownPrevAction)


    @pyqtSignature('')
    def on_actLoadAnyPrevAction_triggered(self):
        self.loadPrevAction(CGetPrevActionIdHelper.anyPrevAction)


    def isBtnDeleteEnabled(self):
        db = QtGui.qApp.db
        tableEvent = db.table('Event')
        record = self.action.getRecord()
        if record:
            actionTypeId = forceRef(record.value('actionType_id'))
            actionType = CActionTypeCache.getById(actionTypeId) if actionTypeId else None
            if actionType and actionType.isNomenclatureExpense:
                if not QtGui.qApp.userHasRight(urCanDeleteActionNomenclatureExpense):
                    return False
            # if actionType and u'inspection_mse' in actionType.flatCode.lower():
            #     return False
        actionId = forceRef(record.value('id')) if record else None
        payStatusAction = forceInt(record.value('payStatus')) if record else 0
        isPayStatus = forceBool(payStatusAction)
        payStatusEvent = False
        eventId = forceRef(record.value('event_id')) if record else None
        if eventId and not isPayStatus:
            recordEvent = db.getRecordEx(tableEvent, [tableEvent['payStatus'], tableEvent['id']], [tableEvent['id'].eq(eventId), tableEvent['deleted'].eq(0)])
            payStatusEvent = forceInt(recordEvent.value('payStatus')) if recordEvent else 0
        isPayStatus = isPayStatus and forceBool(payStatusEvent)
        createPersonId = forceRef(record.value('createPerson_id')) if record else None
        return bool(actionId and ((createPersonId and QtGui.qApp.userId == createPersonId) or not forceRef(record.value('person_id'))) and not isPayStatus)


    @pyqtSignature('')
    def on_btnDelete_clicked(self):
        if QtGui.QMessageBox.question(self,
                u'Удаление Действия!', u'Вы действительно хотите удалить Действие?',
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes:
            db = QtGui.qApp.db
            table = db.table('Action')
            tableEvent = db.table('Event')
            record = self.action.getRecord()
            actionId = forceRef(record.value('id')) if record else None
            payStatusAction = forceInt(record.value('payStatus')) if record else 0
            isPayStatus = forceBool(payStatusAction)
            payStatusEvent = False
            eventId = forceRef(record.value('event_id')) if record else None
            if eventId and not isPayStatus:
                recordEvent = db.getRecordEx(tableEvent, [tableEvent['payStatus'], tableEvent['id']], [tableEvent['id'].eq(eventId), tableEvent['deleted'].eq(0)])
                payStatusEvent = forceInt(recordEvent.value('payStatus')) if recordEvent else 0
            isPayStatus = isPayStatus and forceBool(payStatusEvent)
            if isPayStatus:
                message = u'%s включено в счёт\nи его данные не могут быть изменены!'%(u'Данное Действие' if payStatusAction else (u'Событие, содержащее данное Действие,' if payStatusEvent else u'Данное Действие'))
                QtGui.QMessageBox.critical(self, u'Внимание!', message)
                return
            createPersonId = forceRef(record.value('createPerson_id')) if record else None
            if actionId and createPersonId and QtGui.qApp.userId == createPersonId and not isPayStatus:
                tableActionProperty = db.table('ActionProperty')
                filter = [tableActionProperty['action_id'].eq(actionId), tableActionProperty['deleted'].eq(0)]
                db.deleteRecord(tableActionProperty, filter)

                tableActionExecutionPlan = db.table('Action_ExecutionPlan')
                filter = [tableActionExecutionPlan['master_id'].eq(actionId), tableActionExecutionPlan['deleted'].eq(0)]
                db.deleteRecord(tableActionExecutionPlan, filter)

                tableStockMotion = db.table('StockMotion')
                tableActionNR = db.table('Action_NomenclatureReservation')
                filter = [tableActionNR['action_id'].eq(actionId)]
                reservationIdList = db.getDistinctIdList(tableActionNR, [tableActionNR['reservation_id']], filter)
                if reservationIdList:
                    filter = [tableStockMotion['id'].inlist(reservationIdList), tableStockMotion['deleted'].eq(0)]
                    db.deleteRecord(tableStockMotion, filter)

                filter = [table['id'].eq(actionId), table['deleted'].eq(0)]
                stockMotionIdList = db.getDistinctIdList(table, [table['stockMotion_id']], filter)
                if stockMotionIdList:
                    tableStockMotionItem = db.table('StockMotion_Item')
                    filter = [tableStockMotionItem['master_id'].inlist(stockMotionIdList), tableStockMotionItem['deleted'].eq(0)]
                    db.deleteRecord(tableStockMotionItem, filter)
                    filter = [tableStockMotion['id'].inlist(stockMotionIdList), tableStockMotion['deleted'].eq(0)]
                    db.deleteRecord(tableStockMotion, filter)

                db.deleteRecord(table, [table['id'].eq(actionId)])
                self.close()


    @pyqtSignature('')
    def on_btnSaveAsTemplate_clicked(self):
        if QtGui.qApp.userHasRight(urSaveActionTemplate):
            record = self.getRecord()
            db = QtGui.qApp.db
            personId = QtGui.qApp.userId if QtGui.qApp.userSpecialityId else self.personId
            specialityId = QtGui.qApp.userSpecialityId if QtGui.qApp.userSpecialityId else self.personSpecialityId
            personSNILS  = forceString(db.translate(db.table('Person'), 'id', personId, 'SNILS')) if QtGui.qApp.userSpecialityId else self.personSNILS
            dlg = CActionTemplateSaveDialog(parent=self,
                                            actionRecord=record,
                                            action=self.action,
                                            clientSex=self.clientSex,
                                            clientAge=self.clientAge,
                                            personId=personId,
                                            specialityId=specialityId,
                                            orgStructureId=QtGui.qApp.currentOrgStructureId(),
                                            SNILS=personSNILS,
                                            showTypeTemplate=self.showTypeTemplate
                                           )
            dlg.exec_()
            dlg.deleteLater()
            actionType = self.action.getType()
            self.actionTemplateCache.reset()
            actionTemplateTreeModel = self.actionTemplateCache.getModel(actionType.id)
            self.btnLoadTemplate.setModel(actionTemplateTreeModel)
            if not(QtGui.qApp.userHasRight(urLoadActionTemplate) and (self.cmbStatus.value() != CActionStatus.finished
                                                                      or not self.cmbPerson.value()
                                                                      or QtGui.qApp.userId == self.cmbPerson.value()
                                                                      or (QtGui.qApp.userHasRight(urEditOtherPeopleActionSpecialityOnly) and QtGui.qApp.userSpecialityId == self.personSpecialityId)
                                                                      or QtGui.qApp.userHasRight(urEditOtherpeopleAction))):
                self.btnLoadTemplate.setEnabled(False)


    @pyqtSignature('')
    def on_btnAPNomenclatureExpense_clicked(self):
        self._openNomenclatureEditor()


    def _openNomenclatureEditor(self, requireItems=False):
        # Результат может влиять на продолжение работы функционала "Выполнить"
        action = self.action
        if not action:
            return False
        if not action.getType().isNomenclatureExpense:
            return True
        if action.getType().isNomenclatureExpense and forceInt(action.getRecord().value('status')) == CActionStatus.finished:
            actionTypeId = forceRef(action.getRecord().value('actionType_id'))
            if actionTypeId:
                db = QtGui.qApp.db
                tableATN = db.table('ActionType_Nomenclature')
                nomenclatureIdList = db.getDistinctIdList(tableATN, [tableATN['id']], [tableATN['master_id'].eq(actionTypeId)])
                if nomenclatureIdList:
                    result, (record, action) = selectNomenclatureExpense(self, action)
                    if not result or not action:
                        return False

        if not action.nomenclatureExpense:
            return True

        if action.nomenclatureExpense.stockMotionRecord():
            supplierId = forceRef(action.getRecord().value('orgStructure_id'))
            if supplierId:
                action.nomenclatureExpense.setSupplierId(supplierId)
            if requireItems and not action.nomenclatureExpense.stockMotionItems():
                nomenclatureIdDict = {}
                nomenclatureId = action.findNomenclaturePropertyValue()
                if not nomenclatureId:
                    return True
                nomenclatureIdDict[nomenclatureId] = (action.getRecord(), action.findDosagePropertyValue())
                action.nomenclatureExpense.updateNomenclatureIdListToAction(nomenclatureIdDict)
                if not action.nomenclatureExpense.stockMotionItems():
                    return True

            if QtGui.qApp.keyboardModifiers() & Qt.ShiftModifier:
                dlg = CClientRefundInvoiceEditDialog(self)
                dlg.setData(action.nomenclatureExpense)
            else:
                dlg = CClientInvoiceEditDialog(self, fromAction=True)
                dlg.setFinanceId(forceRef(self.record().value('finance_id')))
                dlg.setData(action.nomenclatureExpense)
                dlg.setClientId(self.clientId)
            try:
                dlg.exec_()
                dlg.getRecord()
                result = dlg.closeByOkButton
                action.setNomenclatureExpensePreliminarySave(result)
            finally:
                dlg.deleteLater()

            return result
        else:
            QtGui.QMessageBox.warning(self,
                                      u'Внимание!',
                                      u'Не удалось инициализировать записи ЛСиИМН \nсвязанные с данным действием!',
                                      QtGui.QMessageBox.Ok,
                                      QtGui.QMessageBox.Ok)
