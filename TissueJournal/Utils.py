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
from PyQt4.QtCore import Qt, pyqtSignature, SIGNAL, QDateTime, QVariant

from RefBooks.Equipment.RoleInIntegration import CEquipmentRoleInIntegration
from Events.Utils                         import getExternalIdDateCond
from Events.Action                        import CAction, CActionTypeCache
from Events.ActionStatus                  import CActionStatus

from library.DialogBase                   import CDialogBase
from library.crbcombobox                  import CRBComboBox
from library.ProgressBar                  import CProgressBar
from library.Utils                        import forceBool, forceDouble, forceInt, forceRef, forceString, smartDict, trim


from .Ui_TissueJournalTotalEditor import Ui_TissueJournalTotalEditorDialog

probeIsFinished = 3
resultLost = u'[НЕТ РЕЗУЛЬТАТА]'

class CClientIdentifierSelector(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.vLayout = QtGui.QVBoxLayout()
        self.lblTitle = QtGui.QLabel(u'Значение', self)
        self.vLayout.addWidget(self.lblTitle)
        self.cmbIdentifierTypes = QtGui.QComboBox(self)
        self.vLayout.addWidget(self.cmbIdentifierTypes)
        self.lblOrderBy = QtGui.QLabel(u'Сортировка:', self)
        self.vLayout.addWidget(self.lblOrderBy)
        self.cmbOrderBy = QtGui.QComboBox(self)
        self.cmbOrderBy.addItems([u'по ИБМ', u'по ФИО', u'по дате забора биоматериала'])
        self.vLayout.addWidget(self.cmbOrderBy)

        self.chkNeedAmountAndUnit = QtGui.QCheckBox(u'Печатать \'Кол-во биоматериала\' и \'Ед.изм.\'', self)
        self.chkNeedStatus   = QtGui.QCheckBox(u'Печатать \'Статус\'', self)
        self.chkNeedDatetime = QtGui.QCheckBox(u'Печатать \'Время\'', self)
        self.chkNeedPerson   = QtGui.QCheckBox(u'Печатать \'Ответственный\'', self)
        self.chkNeedMKB      = QtGui.QCheckBox(u'Печатать \'МКБ\'', self)
        self.chkNeedClientBirthDate      = QtGui.QCheckBox(u'Печатать \'Дата рождения\'', self)

        self.vLayout.addWidget(self.chkNeedAmountAndUnit)
        self.vLayout.addWidget(self.chkNeedStatus)
        self.vLayout.addWidget(self.chkNeedDatetime)
        self.vLayout.addWidget(self.chkNeedPerson)
        self.vLayout.addWidget(self.chkNeedMKB)
        self.vLayout.addWidget(self.chkNeedClientBirthDate)

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.vLayout.addWidget(self.buttonBox)
        self.setLayout(self.vLayout)
        self.setWindowTitle(u'Условия формирования отчета \'Лабораторный журнал\'')
        self.connect(self.buttonBox, SIGNAL('accepted()'), self.accept)
        self.connect(self.buttonBox, SIGNAL('rejected()'), self.reject)

    def setEnabledOrderBy(self, value):
        self.cmbOrderBy.setEnabled(value)


    def orderBy(self):
        return self.cmbOrderBy.currentIndex()


    def getItem(self):
        ok = self.exec_()
        result = smartDict()
        result.clientIdType = self.cmbIdentifierTypes.currentText()
        result.needAmountAndUnit = self.chkNeedAmountAndUnit.isChecked()
        result.chkNeedStatus = self.chkNeedStatus.isChecked()
        result.chkNeedDatetime = self.chkNeedDatetime.isChecked()
        result.chkNeedPerson = self.chkNeedPerson.isChecked()
        result.chkNeedMKB = self.chkNeedMKB.isChecked()
        result.chkNeedClientBirthDate = self.chkNeedClientBirthDate.isChecked()
        result.orderBy = self.orderBy()
        return result, ok


    def setClientIdentifierTypesList(self, clientIdentifierTypesList):
        self.cmbIdentifierTypes.clear()
        self.cmbIdentifierTypes.addItems(clientIdentifierTypesList)


    def setPreviousSelectedClientIdentifier(self, previousSelectedClientIdentifier):
        self.cmbIdentifierTypes.setCurrentIndex(previousSelectedClientIdentifier)


class CTotalEditorDialog(QtGui.QDialog):
    def __init__(self, parent, subEditor):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle(u'Редактор общего значения')
        self.subEditor = subEditor
        self.vLayout = QtGui.QVBoxLayout()
        self.vLayout.addWidget(self.subEditor)
        self._isNullValue = False
        self.chkSetNull = QtGui.QCheckBox(u'Очистить', self)
        self.vLayout.addWidget(self.chkSetNull)
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.vLayout.addWidget(self.buttonBox)
        self.setLayout(self.vLayout)
        self.connect(self.buttonBox, SIGNAL('accepted()'), self.accept)
        self.connect(self.buttonBox, SIGNAL('rejected()'), self.reject)
        self.connect(self.chkSetNull, SIGNAL('clicked(bool)'), self.on_chkSetNull_clicked)


    def on_chkSetNull_clicked(self, value):
        self.subEditor.setEnabled(not value)
        self._isNullValue = value


    def isNullValue(self):
        return self._isNullValue


    def editor(self):
        return self.subEditor


class CSamplingApplyDialog(CDialogBase):
    def __init__(self, parent, tissueExternalId, equipmentId, testGroupVisible=False, autoEquipment=False):
        CDialogBase.__init__(self, parent)
        self.vLayout = QtGui.QVBoxLayout()
        self.lblExternalId = QtGui.QLabel(u'Идентификатор', self)
        self.vLayout.addWidget(self.lblExternalId)
        self.edtExternalId = QtGui.QLineEdit(tissueExternalId, self)
        self.vLayout.addWidget(self.edtExternalId)
        self.lblEquipment = QtGui.QLabel(u'Оборудование', self)
        self.vLayout.addWidget(self.lblEquipment)

        self.cmbEquipment = CRBComboBox(self)
        specialValues = ((-1, '-', u'Автоопределение оборудования'), ) if autoEquipment else None
        self.cmbEquipment.setTable('rbEquipment',
                                   addNone=True, 
                                   specialValues=specialValues,
                                   filter='status=1 AND roleInIntegration in %s' % ((CEquipmentRoleInIntegration.external, CEquipmentRoleInIntegration.internal),)
                                  )
        self.cmbEquipment.setValue(equipmentId)

        self.vLayout.addWidget(self.cmbEquipment)
        self.lblTestGroup = QtGui.QLabel(u'Группа тестов', self)
        self.vLayout.addWidget(self.lblTestGroup)
        self.cmbTestGroup = CRBComboBox(self)
        self.cmbTestGroup.setTable('rbTestGroup', addNone=True)
        self.vLayout.addWidget(self.cmbTestGroup)

        self.lblExternalId.setVisible(not testGroupVisible)
        self.edtExternalId.setVisible(not testGroupVisible)

        self.lblTestGroup.setVisible(testGroupVisible)
        self.cmbTestGroup.setVisible(testGroupVisible)

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.vLayout.addWidget(self.buttonBox)
        self.setLayout(self.vLayout)
        self.connect(self.buttonBox, SIGNAL('accepted()'), self.accept)
        self.connect(self.buttonBox, SIGNAL('rejected()'), self.reject)

        self._tissueJournalId = None
        self._tissueTypeId    = None
        self._datetimeTaken   = None
        self.setWindowTitle(u'Регистрация проб')


    def setSettings(self, tissueJournalId, tissueTypeId, datetimeTaken):
        self._tissueJournalId = tissueJournalId
        self._tissueTypeId    = tissueTypeId
        self._datetimeTaken   = datetimeTaken


    def checkDataEntered(self):
        result = True
        result = result and self.checkExternalId()
        return result


    def saveData(self):
        return self.checkDataEntered()


    def checkExternalId(self):
        result = True

        if self.edtExternalId.isVisible():
            message = u''
            externalId = trim(self.edtExternalId.text())
            if bool(externalId):
                if not externalId.isdigit():
                    result = False
                    message = u'корректный идентификатор'
            else:
                result = False
                message = u'идентификатор'

            result = result or self.checkInputMessage(message, False, self.edtExternalId)
            result = result and self.checkSelectedToSave(externalId, self._tissueJournalId)
        return result


    def checkSelectedToSave(self, externalId, tissueJournalId):
        db = QtGui.qApp.db
        tableProbe = db.table('Probe')
        tableTissueJournal = db.table('TakenTissueJournal')

        cond = [tableProbe['takenTissueJournal_id'].ne(tissueJournalId),
                tableProbe['externalId'].eq(externalId),
                tableTissueJournal['tissueType_id'].eq(self._tissueTypeId),
                tableTissueJournal['deleted'].eq(0)]

        dateCond = getExternalIdDateCond(self._tissueTypeId, self._datetimeTaken)

        if dateCond:
            cond.append(dateCond)

        queryTable = tableProbe.innerJoin(tableTissueJournal,
                                          tableTissueJournal['id'].eq(tableProbe['takenTissueJournal_id']))

        record = QtGui.qApp.db.getRecordEx(queryTable, tableProbe['id'].name(), cond)
        if record and forceRef(record.value('id')):
            return self.checkInputMessage(u'другой идентификатор.\nТакой уже существует', False, self.edtExternalId)
        return True


    def externalId(self):
#        result = trim(self.edtExternalId.text()).lstrip('0')
#        return (6-len(result))*'0'+result
        #TODO: если ИБМ назначено автоматом, ставить нули, если вручну - выдавать как есть
        return forceString(self.edtExternalId.text())


    def equipmentId(self):
        return self.cmbEquipment.value()


    def testGroupId(self):
        return self.cmbTestGroup.value()


# ###############################################################


class CTissueJournalTotalEditorDialog(QtGui.QDialog, Ui_TissueJournalTotalEditorDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setVisibleMKBWidgets(False)
        self.setVisibleAmountWidgets(False)
        self.valuesDict = {'personIdInJournal'  : None,
                           'personIdInAction'   : None,
                           'assistantIdInAction': None,
                           'status'             : None,
                           'mkb'                : None,
                           'morphologyMKB'      : None,
                           'amount'             : None, 
                           'actionSpecification' : None}
        self.cmbActionSpecification.setTable('rbActionSpecification', True)


    def exec_(self):
        self.chkStatus.setFocus(Qt.OtherFocusReason)
        return QtGui.QDialog.exec_(self)


    def values(self):
        if self.chkPersonInJournal.isChecked():
            self.valuesDict['personIdInJournal'] = self.cmbPersonInJournal.value()
        if self.chkPersonInAction.isChecked():
            self.valuesDict['personIdInAction'] = self.cmbPersonInAction.value()
        if self.chkAssistantInAction.isChecked():
            self.valuesDict['assistantIdInAction'] = self.cmbAssistantInAction.value()
        if self.chkStatus.isChecked():
            self.valuesDict['status'] = self.cmbStatus.value()
        if self.chkMKB.isChecked():
            self.valuesDict['mkb'] = unicode(self.cmbMKB.text())
        if self.chkMorphologyMKB.isChecked():
            self.valuesDict['morphologyMKB'] = self.cmbMorphologyMKB.validText()
        if self.chkAmount.isChecked():
            self.valuesDict['amount'] = self.edtAmount.value()
        if self.chkActionSpecification.isChecked():
            self.valuesDict['actionSpecification'] = self.cmbActionSpecification.value()
        return self.valuesDict


    def setPersonInJournal(self, value):
        self.cmbPersonInJournal.setValue(value)


    def setPersonIdInAction(self, value):
        self.cmbPersonInAction.setValue(value)


    def setAssistantInAction(self, value):
        self.cmbAssistantInAction.setValue(value)


    def setStatus(self, value):
        self.cmbStatus.setValue(value)


    def setMKB(self, mkb):
        self.cmbMKB.setText(mkb)


    def setMorphology(self, morphology):
        self.cmbMorphologyMKB.setText(morphology)


    def setAmount(self, amount):
        self.edtAmount.setValue(amount)


    def setActionSpecification(self, actionSpecification):
        self.cmbActionSpecification.setValue(actionSpecification)


    def setActionTypeId(self, actionTypeId):
        self.actionTypeId = actionTypeId
        self.setActionSpecificationFilter()

    
    def setActionSpecificationFilter(self):
        actionType = CActionTypeCache.getById(self.actionTypeId) if self.actionTypeId else None
        actionSpecificationIdList = actionType.getActionSpecificationIdList()
        if actionSpecificationIdList:
            setFilter = u'id IN (%s)' % (u', '.join(str(actionSpecificationId) for actionSpecificationId in actionSpecificationIdList if actionSpecificationId is not None))
            self.cmbActionSpecification.setTable('rbActionSpecification', True, filter=setFilter)


    def updateIsChecked(self, value = False):
        self.chkPersonInJournal.setChecked(value)
        self.chkPersonInAction.setChecked(value)
        self.chkAssistantInAction.setChecked(value)
        self.chkStatus.setChecked(value)
        self.chkMKB.setChecked(value)
        self.chkMorphologyMKB.setChecked(value)
        self.chkAmount.setChecked(value)
        self.chkActionSpecification.setChecked(value)


    def setVisibleMKBWidgets(self, value):
        self.setVisibleMKB(value)
        self.setVisibleMorphologyMKB(value)


    def setVisibleMKB(self, value):
        for widget in (self.chkMKB, self.cmbMKB):
            widget.setVisible(value)


    def setVisibleMorphologyMKB(self, value):
        for widget in (self.chkMorphologyMKB, self.cmbMorphologyMKB):
            widget.setVisible(value)


    def setVisibleAmountWidgets(self, value):
        self.chkAmount.setVisible(value)
        self.edtAmount.setVisible(value)


    def setVisibleJournalWidgets(self, value):
        self.chkPersonInJournal.setVisible(value)
        self.cmbPersonInJournal.setVisible(value)


    @pyqtSignature('QString')
    def on_cmbMKB_textChanged(self, value):
        if value[-1:] == '.':
            value = value[:-1]
        diagName = forceString(QtGui.qApp.db.translate('MKB', 'DiagID', value, 'DiagName'))
        if diagName:
            self.lblMKBText.setText(diagName)
        else:
            self.lblMKBText.clear()
#        self.cmbMorphologyMKB.setMKBFilter(self.cmbAPMorphologyMKB.getMKBFilter(unicode(value)))


    @pyqtSignature('QString')
    def on_cmbMorphologyMKB_textChanged(self, value):
        if self.cmbMorphologyMKB.isValid(value):
            name = forceString(QtGui.qApp.db.translate('MKB_Morphology', 'code', value, 'name'))
            if name:
                self.lblMorphologyMKBText.setText(name)
            else:
                self.lblMorphologyMKBText.clear()
        else:
            self.lblMorphologyMKBText.clear()


# #############


class CEmptyEditor(QtGui.QWidget):
    def value(self):
        return QVariant()

    def setValue(self, value):
        pass


# ############


class CInfoListHelper(list):
    def append(self, key, value):
        list.append(self, '<P><B>%s:</B> %s</P>'%(key, value))


# #############################################################


def getActionContextListByTissue(tissueJournalId):
    db = QtGui.qApp.db
    tableTissueJournal = db.table('TakenTissueJournal')
    tableAction = db.table('Action')
    tableActionType = db.table('ActionType')
    queryTable = tableTissueJournal.innerJoin(tableAction,
                                              tableAction['takenTissueJournal_id'].eq(tableTissueJournal['id']))
    queryTable = queryTable.innerJoin(tableActionType,
                                      tableActionType['id'].eq(tableAction['actionType_id']))
    cond = tableTissueJournal['id'].eq(tissueJournalId)
    field = tableActionType['context'].name()

    stmt = db.selectDistinctStmt(queryTable, field, cond)
    query = db.query(stmt)
    result = []
    while query.next():
        context = forceString(query.value(0))
        result.append(context)
    return result


def getDependentEventIdList(tissueJournalId):
    db = QtGui.qApp.db
    tableAction = db.table('Action')
    tableEvent  = db.table('Event')
    queryTable = tableEvent.innerJoin(tableAction, tableAction['event_id'].eq(tableEvent['id']))
    cond = [tableAction['deleted'].eq(0),
            tableEvent['deleted'].eq(0),
            tableAction['takenTissueJournal_id'].eq(tissueJournalId)]
    return db.getDistinctIdList(queryTable, tableEvent['id'].name(), cond)


def deleteEventsIfWithoutActions(eventIdList):
    for eventId in eventIdList:
        db = QtGui.qApp.db
        tableEvent  = db.table('Event')
        tableAction = db.table('Action')
        cond = [tableAction['deleted'].eq(0), tableEvent['id'].eq(eventId)]
        queryTable = tableEvent.innerJoin(tableAction, tableAction['event_id'].eq(tableEvent['id']))
        actionIdList = db.getDistinctIdList(queryTable, tableAction['id'].name(), cond)
        if not len(actionIdList) > 0:
            diagnosisIdList = db.getIdList('Diagnostic', idCol='diagnosis_id', where='event_id=%d'%eventId)
            db.deleteRecord(tableEvent, tableEvent['id'].eq(eventId))
            if diagnosisIdList:
                tableDiagnosis = db.table('Diagnosis')
                diagnosisDeleteCond = [
                            tableDiagnosis['id'].inlist(diagnosisIdList),
                            'NOT EXISTS (SELECT * FROM Diagnostic WHERE Diagnostic.diagnosis_id = Diagnosis.id)',
                            'NOT EXISTS (SELECT * FROM TempInvalid WHERE TempInvalid.diagnosis_id = Diagnosis.id)'
                                      ]
                db.deleteRecord(tableDiagnosis, diagnosisDeleteCond)


def checkActionPreliminaryResultByTissueJournalIdList(tissueJournalIdList):
    db = QtGui.qApp.db

    tableProbe              = db.table('Probe')
    tableAction             = db.table('Action')
    tableActionType         = db.table('ActionType')
    tableActionPropertyType = db.table('ActionPropertyType')

    queryTable = tableAction.innerJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
    queryTable = queryTable.innerJoin(tableActionPropertyType,
                                        tableActionPropertyType['actionType_id'].eq(tableActionType['id']))
    queryTable = queryTable.innerJoin(tableProbe,
                                        [tableProbe['takenTissueJournal_id'].eq(tableAction['takenTissueJournal_id']),
                                        tableProbe['test_id'].eq(tableActionPropertyType['test_id'])])

    allActionIdList = db.getDistinctIdList(tableAction, 'id',
                                            tableAction['takenTissueJournal_id'].inlist(tissueJournalIdList))
    okActionIdList = db.getDistinctIdList(queryTable, tableAction['id'].name(), tableAction['id'].inlist(allActionIdList))

    templateStmt = 'UPDATE `Action` SET preliminaryResult=0 WHERE id=%(actionId)d'
    for actionId in (set(allActionIdList) - set(okActionIdList)):
        db.query(templateStmt % {'actionId':actionId})


def setProbeResultToActionProperties(tissueJournalId, testId, result, norm, externalEvaluation, unitId,
                                     assistantId, personId, orderExecDate=None, closeAction=False, course=1, orderComment = None):
    db = QtGui.qApp.db

    tableAction = db.table('Action')
    tableActionPropertyType = db.table('ActionPropertyType')

    queryTable = tableAction.innerJoin(tableActionPropertyType,
                                        tableActionPropertyType['actionType_id'].eq(tableAction['actionType_id']))

    actionTakenTissueJournalId = forceRef(db.translate('TakenTissueJournal', 'id', tissueJournalId, 'parent_id')) or tissueJournalId

    cond = [tableAction['takenTissueJournal_id'].eq(actionTakenTissueJournalId),
            tableActionPropertyType['test_id'].eq(testId),
            tableActionPropertyType['course'].eq(course)]

    stmt = db.selectDistinctStmt(queryTable, 'Action.*', cond)
    query = db.query(stmt)
    while query.next():
        actionRecord = query.record()

        needSave = False

        action = CAction(record=actionRecord)

        if closeAction:
            actionId = forceRef(actionRecord.value('id'))
            setActionTestSetClosingController(actionId, assistantId, personId, orderExecDate)

        actionType = action.getType()
        propertyTypeItemsList = actionType.getPropertiesById().items()
        for propertyTypeId, propertyType in propertyTypeItemsList:
            if propertyType.testId == testId and not propertyType.isVector and propertyType.course == course:
                property = action.getPropertyById(propertyTypeId)
                if (isinstance(result, QVariant) and result.isValid()):
                    property.setValue(propertyType.convertQVariantToPyValue(result))
                elif not (isinstance(result, QVariant) or result is None):
                    property.setValue(result)
                if norm:
                    property.setNorm(norm)
                if externalEvaluation:
                    property.setEvaluation(_mapExternalEvaluationToPropertyEvaluation.get(externalEvaluation, None))
                if unitId:
                    property.setUnit(unitId)
                needSave = True

        if needSave:
            currentActionRecord = action.getRecord()
            if orderComment:
                currentActionRecord.setValue('note', QVariant(orderComment))
            currentActionRecord.setValue('endDate', orderExecDate)
            action.save(idx=-1)

_mapExternalEvaluationToPropertyEvaluation = {'L': -1,
                                              'H': 1,
                                              'LL': -2,
                                              'HH': 2,
                                              '<': -1,
                                              '>': 1,
                                              'N': 0,
                                              'A': None,
                                              'U': None,
                                              'D': None,
                                              'B': None,
                                              'W': None,
                                             }



# ################################################


def resetActionTestSetClosingController():
    CActionTestSetClosingController.reset()


def checkActionTestSetClosingController():
    CActionTestSetClosingController.check()
    resetActionTestSetClosingController()


def setActionTestSetClosingController(actionId, assistantId, personId, labExecDate=None):
    CActionTestSetClosingController.set(actionId, assistantId, personId, labExecDate)


class CActionTestSetClosingController():
    cache = {}
    labExecDate = None

    @classmethod
    def reset(cls):
        cls.cache.clear()

    @classmethod
    def set(cls, actionId, assistantId, personId, labExecDate=None):
        if assistantId or personId or actionId not in cls.cache:
            cls.cache[actionId] = (assistantId, personId)
        if labExecDate:
            cls.labExecDate = labExecDate


    @classmethod
    def check(cls):
        db = QtGui.qApp.db
        for actionId, (assistantId, personId) in cls.cache.items():
            actionRecord = db.getRecord('Action', '*', actionId)
            close = True
            existTest = False
            if actionRecord:
                action = CAction(record=actionRecord)
                actionType = action.getType()
                propertyTypeItemsList = actionType.getPropertiesById().items()
                for propertyTypeId, propertyType in propertyTypeItemsList:
                    if propertyType.testId and not propertyType.isVector:
                        existTest = True
                        property = action.getPropertyById(propertyTypeId)
                        if property.getValue() is None and property.getNorm() != resultLost and property.isAssigned():
                            close = False
                            break

                if close and existTest:
                    actionRecord.setValue('status', CActionStatus.finished)
                    if assistantId and personId:
                        actionRecord.setValue('assistant_id', assistantId)
                        actionRecord.setValue('person_id', personId)
                    elif personId or assistantId:
                        actionRecord.setValue('person_id', personId or assistantId)

                    if cls.labExecDate:
                        actionRecord.setValue('endDate', cls.labExecDate)
                    else:
                        actionRecord.setValue('endDate', QDateTime.currentDateTime())
                    action.save(idx=-1)


# ################################

def setActionPreliminaryResult(mapActionId2PreliminaryResult):
    db = QtGui.qApp.db
    templateStmt = 'UPDATE `Action` SET preliminaryResult=%(result)d WHERE id=%(actionId)d'
    for actionId, preliminaryResultList in mapActionId2PreliminaryResult.items():
        existsResult = any(result==probeIsFinished for result in preliminaryResultList[1:])
        db.query(templateStmt%{'result':1 if existsResult else 2, 'actionId':actionId})


def computeActionPreliminaryResult(probeItem, mapActionId2PreliminaryResult):
    testId = forceRef(probeItem.value('test_id'))
    tissueJournalId = forceRef(probeItem.value('takenTissueJournal_id'))

    db = QtGui.qApp.db
    tableTissueJournal      = db.table('TakenTissueJournal')
    tableAction             = db.table('Action')
    tableActionType         = db.table('ActionType')
    tableActionPropertyType = db.table('ActionPropertyType')

    queryTable = tableAction.innerJoin(tableTissueJournal,
                                        tableTissueJournal['id'].eq(tableAction['takenTissueJournal_id']))
    queryTable = queryTable.innerJoin(tableActionType,
                                        tableActionType['id'].eq(tableAction['actionType_id']))
    queryTable = queryTable.innerJoin(tableActionPropertyType,
                                        tableActionPropertyType['actionType_id'].eq(tableActionType['id']))

    cond = [tableTissueJournal['id'].eq(tissueJournalId),
            tableActionPropertyType['test_id'].eq(testId)]

    recordList = db.getRecordList(queryTable, 'Action.*', cond)

    for record in recordList:
        actionId = forceRef(record.value('id'))
        preliminaryResult = forceInt(record.value('preliminaryResult'))
        if preliminaryResult != 1:
            preliminaryResultList = mapActionId2PreliminaryResult.setdefault(actionId, [preliminaryResult])
            preliminaryResultList.append(forceInt(probeItem.value('status')))


# ##########################################################


class CTissueJournalActionTypeStack():
    cacheActionTypeTestIdList = {}

    def __init__(self, tissueJournalId):
        db = QtGui.qApp.db
        actionTissueJournalId = forceRef(db.translate('TakenTissueJournal', 'id', tissueJournalId, 'parent_id')) or tissueJournalId
        self.actionTypeIdList = db.getIdList('Action',
                                             'actionType_id',
                                             'deleted=0 AND takenTissueJournal_id=%d' % actionTissueJournalId)

        for actionTypeId in self.actionTypeIdList:
            if actionTypeId not in CTissueJournalActionTypeStack.cacheActionTypeTestIdList.keys():
                result = db.getDistinctIdList('ActionPropertyType',
                                              'test_id',
                                              'deleted=0 AND actionType_id=%d'%actionTypeId)
                CTissueJournalActionTypeStack.cacheActionTypeTestIdList[actionTypeId] = result
        self.testIdPosition = {}
        self.count = len(self.actionTypeIdList)


    def next(self, testId):
        position = self.testIdPosition.setdefault(testId, 0)
        while position < self.count:
            if testId in CTissueJournalActionTypeStack.cacheActionTypeTestIdList[self.actionTypeIdList[position]]:
                return self.actionTypeIdList[position]
            else:
                position += 1
                self.testIdPosition[testId] = position
        return None


class CTissueJournalActionTypeHelper():
    cache = {}

    @classmethod
    def reset(cls):
        cls.cache.clear()
        CTissueJournalActionTypeStack.cacheActionTypeTestIdList.clear()


    @classmethod
    def next(cls, tissueJournalId, testId):
        stack = cls.cache.get(tissueJournalId, None)
        if not stack:
            stack = CTissueJournalActionTypeStack(tissueJournalId)
            cls.cache[tissueJournalId] = stack
        return stack.next(testId)


def getNextTissueJournalActionType(tissueJournalId, testId):
    return CTissueJournalActionTypeHelper.next(tissueJournalId, testId)


def resetTissueJournalActionTypeStackHelper():
    CTissueJournalActionTypeHelper.reset()


class CContainerTypeCache():
    cache = {}

    @classmethod
    def reset(cls):
        cls.cache.clear()

    @classmethod
    def get(cls, actionTypeId, tissueTypeId):
        key = (actionTypeId, tissueTypeId)
        result = cls.cache.get(key, None)
        if not result:
            db = QtGui.qApp.db

            table = db.table('ActionType_TissueType')
            cond = [table['master_id'].eq(actionTypeId),
                    table['tissueType_id'].eq(tissueTypeId)]
            record = db.getRecordEx(table, 'containerType_id, amount', cond)
            if record:
                containerTypeId = forceRef(record.value('containerType_id'))
                containerRecord = db.getRecord('rbContainerType', '*', containerTypeId)
                if containerRecord:
                    container       = ' | '.join([forceString(containerRecord.value('code')),
                                                  forceString(containerRecord.value('name'))
                                                 ]
                                                )
                    color           = forceString(containerRecord.value('color'))
                    tissueAmount    = forceDouble(record.value('amount'))
                    containerCapacity = forceDouble(containerRecord.value('amount'))

                    result = ([None, container, QtGui.QColor(color), tissueAmount, tissueAmount, containerCapacity],
                              containerTypeId)
                else:
                    result = (None, containerTypeId)
            else:
                result = (None, None)

            cls.cache[key] = result

        return result

def getContainerTypeValues(actionTypeId, tissueTypeId):
    return CContainerTypeCache.get(actionTypeId, tissueTypeId)


def resetContainerTypeCache():
    CContainerTypeCache.reset()

# ##########################################################


class CSamplePreparationProgressBar(CProgressBar):
    def __init__(self, itemsCount=0, parent=None):
        CProgressBar.__init__(self, parent)
        self.setMaximum(itemsCount)


# ###########################################################

equipmentByEventCache = {}
equipmentByActionCache = {}
def getActualEquipmentId(testId, osId = None, actionId = None):
    db = QtGui.qApp.db
    osId = None
    if not actionId:
        osId = QtGui.qApp.currentOrgStructureId()
    else:
        tableAction = db.table('Action')
        tablePerson = db.table('Person')
        tableOS = db.table('OrgStructure')
        table = tableAction.innerJoin(tablePerson, tableAction['setPerson_id'].eq(tablePerson['id']))
        table = table.innerJoin(tableOS, tablePerson['orgStructure_id'].eq(tableOS['id']))
        cond = [tableAction['id'].eq(actionId)]
        recordList = db.getRecordList(table, [tableOS['id'].name()], cond)
        if recordList:
            osId = forceRef(recordList[0].value(0))
    table = db.table('rbEquipment_Test')
    result = db.getIdList(table, 'equipment_id', table['test_id'].eq(testId), 'isDefault DESC')
    if osId and result:
        orgStructureIdList = db.getTheseAndParents('OrgStructure', 'parent_id', [osId])
        tableOrgEquip = db.table('OrgStructure_Equipment')
        cond = [tableOrgEquip['master_id'].inlist(orgStructureIdList)]
        count = db.getCount(tableOrgEquip, where=cond)
        if count:
            cond.append(tableOrgEquip['equipment_id'].inlist(result))
            result = db.getIdList(tableOrgEquip, 'equipment_id', cond, 'priority DESC')
    if result:
        return result[0]
    return None


def getActualSpecimenTypeId(testId, equipmentId):
    db = QtGui.qApp.db
    table = db.table('rbEquipment_Test')
    cond = [table['test_id'].eq(testId), table['equipment_id'].eq(equipmentId)]
    result = db.getIdList(table, 'specimenType_id', cond, 'isDefault DESC')
    if result:
        return result[0]
    return None


# #############################################################

def getEquipmentInterface(equipmentId):
    db = QtGui.qApp.db
    record = db.getRecord('rbEquipment', '*', equipmentId)
    if record:
        return smartDict(id                     = equipmentId,
                         eachTestDetached       = forceBool(record.value('eachTestDetached')),
                         protocol               = forceInt(record.value('protocol')),
                         address                = forceString(record.value('address')),
                         ownName                = forceString(record.value('ownName')),
                         ownCode                = forceString(record.value('ownCode')),
                         labName                = forceString(record.value('labName')),
                         labCode                = forceString(record.value('labCode')),
                         specimenIdentifierMode = forceInt(record.value('specimenIdentifierMode')),
                         protocolVersion        = forceString(record.value('protocolVersion')),
                         resultOnFact           = forceBool(record.value('resultOnFact'))
                        )
    else:
        return None

# ##############################################################################


def getEquipmentFilterByOrgStructureId(orgStructureId):
    db = QtGui.qApp.db
    table = db.table('OrgStructure_Equipment')
    orgStructureEquipmentIdList = db.getIdList(table, 'equipment_id', table['master_id'].eq(orgStructureId))
    return db.table('rbEquipment')['id'].inlist(orgStructureEquipmentIdList)


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    w = CSamplePreparationProgressBar(10)
    w.show()
    app.exec_()
