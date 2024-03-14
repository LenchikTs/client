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
from PyQt4.QtCore        import (
                                    Qt,
                                    pyqtSignature,
                                    SIGNAL,
#                                    QDate,
#                                    QTime,
                                    QModelIndex,
                                    QVariant,
                                    QDateTime,
                                )

#from library.interchange import (
#                                    getCheckBoxValue,
#                                    getLineEditValue,
#                                    getRBComboBoxValue,
#                                    getTextEditValue,
#                                    setRBComboBoxValue,
#                                    setTextEditValue,
#                                )
from library.Utils       import forceDateTime, forceRef, forceString, forceStringEx, toVariant, trim, forceInt
from library.InDocTable  import CInDocTableModel, CInDocTableCol, forcePyType
from library.database    import CTableRecordCache
from library.DialogBase  import CDialogBase, CConstructHelperMixin
from library.TableModel  import CTableModel, CTextCol
from Events.Action       import CAction
from Events.ActionPropertiesTable import CActionPropertiesTableModel
from Events.ActionStatus import CActionStatus
from Events.Utils        import inMedicalDiagnosis, setActionPropertiesColumnVisible
from Orgs.Utils          import getPersonOrgStructureChiefs
from Reports.Utils       import getActionTypeIdListByFlatCode
from Users.Rights        import (
#                                    urEditClosedEvent,
#                                    urEditEventExpertise,
                                    urEditOtherpeopleAction,
                                    urReadMedicalDiagnosis,
                                    urEditMedicalDiagnosis,
                                    urEditSubservientPeopleAction,
                                    urEditOtherPeopleActionSpecialityOnly,
                                )

from Events.Ui_EventMedicalDiagnosisPage    import Ui_EventMedicalDiagnosisPageWidget
from Events.Ui_EventMedicalDiagnosisEditor  import Ui_EventMedicalDiagnosisEditor
from Events.Ui_EventMedicalDiagnosisCreator import Ui_EventMedicalDiagnosisCreator


class CEventMedicalDiagnosisPage(QtGui.QWidget, CConstructHelperMixin, Ui_EventMedicalDiagnosisPageWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.personsCache = CTableRecordCache(QtGui.qApp.db, 'vrbPersonWithSpeciality', '*')
        self.modelEventMedicalDiagnosis = CEventMedicalDiagnosisTableModel(self, self.personsCache)
        self.selectionModelEventMedicalDiagnosis = QtGui.QItemSelectionModel(self.modelEventMedicalDiagnosis, self)
        self.selectionModelEventMedicalDiagnosis.setObjectName('selectionModelEventMedicalDiagnosis')
        self.setupUi(self)
        self.tblEventMedicalDiagnosis.setModel(self.modelEventMedicalDiagnosis)
        self.tblEventMedicalDiagnosis.setSelectionModel(self.selectionModelEventMedicalDiagnosis)
        self.setFocusProxy(self.tblEventMedicalDiagnosis)
        self.eventEditor = None
        self.eventId = None
        self.addPopupUpdateAction()
        self.tblEventMedicalDiagnosis.installEventFilter(self)
        self.tblEventMedicalDiagnosis.addPopupDelRow()
        self.connect(self.tblEventMedicalDiagnosis._popupMenu, SIGNAL('aboutToShow()'), self.on_mnuEventMedicalDiagnosis_aboutToShow)


    def addPopupUpdateAction(self):
        if self.tblEventMedicalDiagnosis._popupMenu is None:
            self.tblEventMedicalDiagnosis.createPopupMenu()
        self.actUpdateAction = QtGui.QAction(u'Редактировать действие (F2)', self)
        self.actUpdateAction.setObjectName('actUpdateAction')
        self.tblEventMedicalDiagnosis._popupMenu.addAction(self.actUpdateAction)
        self.connect(self.actUpdateAction, SIGNAL('triggered()'), self.updateAction)
        self.addObject('qshcUpdateAction', QtGui.QShortcut('F2', self.tblEventMedicalDiagnosis, self.updateAction))
        self.addObject('qshcCreateAction', QtGui.QShortcut('F9', self.tblEventMedicalDiagnosis, self.createAction))
        self.qshcUpdateAction.setContext(Qt.WidgetShortcut)
        self.qshcCreateAction.setContext(Qt.WidgetShortcut)


    @pyqtSignature('')
    def on_mnuEventMedicalDiagnosis_aboutToShow(self):
        self.tblEventMedicalDiagnosis.on_popupMenu_aboutToShow()
        rowCount = self.modelEventMedicalDiagnosis.rowCount()
        row = self.tblEventMedicalDiagnosis.currentIndex().row()
        record, action = self.modelEventMedicalDiagnosis._items[row] if 0 <= row < len(self.modelEventMedicalDiagnosis._items) else (None, None)
        actionTypeId = forceRef(record.value('actionType_id')) if record else None
        self.actUpdateAction.setEnabled(bool(0 <= row < rowCount and actionTypeId and QtGui.qApp.userHasRight(urReadMedicalDiagnosis) and QtGui.qApp.userHasRight(urEditMedicalDiagnosis)))


    def protectFromEdit(self, isProtected):
        self.modelEventMedicalDiagnosis.setReadOnly(isProtected)


    def setEventEditor(self, eventEditor):
        self.eventEditor = eventEditor


    def load(self, eventId):
        self.eventId = eventId
        self.modelEventMedicalDiagnosis.loadItems(self.eventId)
        self.tblEventMedicalDiagnosis.setRowHeightLoc()
        self.tblEventMedicalDiagnosis.setModel(self.modelEventMedicalDiagnosis)
        self.tblEventMedicalDiagnosis.setSelectionModel(self.selectionModelEventMedicalDiagnosis)


    def save(self, eventId):
        self.modelEventMedicalDiagnosis.saveItems(eventId)


    def createAction(self):
        if QtGui.qApp.userHasRight(urReadMedicalDiagnosis) and QtGui.qApp.userHasRight(urEditMedicalDiagnosis):
            dialogCreator = CEventMedicalDiagnosisCreator(self)
            try:
                dialogCreator.load()
                dialogCreator.exec_()
                actionTypeId = dialogCreator.getActionTypeId()
                if actionTypeId:
                    db = QtGui.qApp.db
                    tableAction = db.table('Action')
                    record = tableAction.newRecord()
                    record.setValue('actionType_id', toVariant(actionTypeId))
                    action = CAction(record=record)
                    if action:
                        actionType = action.getType()
                        dialogEditor = CEventMedicalDiagnosisEditor(self, self.eventId, self.eventEditor.clientId, self.eventEditor.clientAge, self.eventEditor.clientSex)
                        dialogEditor.setWindowTitle(actionType.name)
                        dialogEditor.createAction(action.getRecord(), action)
                        try:
                            if dialogEditor.exec_():
                                newRecord, newAction = dialogEditor.getRecord()
                                if newAction:
                                    self.modelEventMedicalDiagnosis.items().append((newRecord, newAction))
                                    self.modelEventMedicalDiagnosis.items().sort(key=lambda x: forceDateTime(x[0].value('endDate')), reverse=True)
                                    self.modelEventMedicalDiagnosis.reset()
                                    self.tblEventMedicalDiagnosis.setRowHeightLoc()
                        finally:
                            dialogEditor.deleteLater()
            finally:
                dialogCreator.deleteLater()


    def updateAction(self):
        if QtGui.qApp.userHasRight(urReadMedicalDiagnosis) and QtGui.qApp.userHasRight(urEditMedicalDiagnosis):
            currentIndex = self.tblEventMedicalDiagnosis.currentIndex()
            if currentIndex and currentIndex.isValid():
                record, action = self.tblEventMedicalDiagnosis.currentItem()
                if action:
                    actionType = action.getType()
                    dialog = CEventMedicalDiagnosisEditor(self, self.eventId, self.eventEditor.clientId, self.eventEditor.clientAge, self.eventEditor.clientSex)
                    dialog.setWindowTitle(actionType.name)
                    dialog.createAction(action.getRecord(), action)
                    try:
                        if dialog.exec_():
                            newRecord, newAction = dialog.getRecord()
                            if newAction:
                                self.modelEventMedicalDiagnosis.items().append((newRecord, newAction))
                                self.modelEventMedicalDiagnosis.items().sort(key=lambda x: forceDateTime(x[0].value('endDate')), reverse=True)
                                self.modelEventMedicalDiagnosis.reset()
                                self.tblEventMedicalDiagnosis.setRowHeightLoc()
                    finally:
                        dialog.deleteLater()


class CEventMedicalDiagnosisTableModel(CInDocTableModel):

    class CLocActionRecordColumn(CInDocTableCol):
        def __init__(self, title, fieldName, width, **params):
            CInDocTableCol.__init__(self, title, fieldName, width, **params)
            self.caches = params.get('caches', [])


        def toString(self, val, record, action):
            if action:
                actionType = action.getType()
                endDate = forceDateTime(record.value('endDate'))
                personId = forceRef(record.value('person_id'))
                actionInfo = [unicode(endDate.toString('dd.MM.yyyy hh:mm:ss')) if endDate else u'',
                              forceString(self.caches.get(personId).value('name')) if personId else u'',
                              actionType.name]
                return toVariant(u'\n'.join(val for val in actionInfo))
            return QVariant()


        def toSortString(self, val, record, action):
            return forcePyType(self.toString(val, record, action))


        def toStatusTip(self, val, record, action):
            return self.toString(val, record, action)


        def createEditor(self, parent):
            editor = QtGui.QLineEdit(parent)
            if self._maxLength:
                editor.setMaxLength(self._maxLength)
            if self._inputMask:
                editor.setInputMask(self._inputMask)
            return editor


        def setEditorData(self, editor, value, record):
            editor.setText(forceStringEx(value))


        def getEditorData(self, editor):
            text = trim(editor.text())
            if text:
                return toVariant(text)
            else:
                return QVariant()


        def alignment(self):
            return QVariant(Qt.AlignLeft + Qt.AlignTop)



    class CLocActionProperyColumn(CInDocTableCol):
        def __init__(self, title, fieldName, width, **params):
            CInDocTableCol.__init__(self, title, fieldName, width, **params)
            self.name = params.get('name', '')


        def toString(self, val, record, action):
            if action and self.name:
                actionType = action.getType()
                properties = []
                for name, propertyType in actionType._propertiesByName.items():
                    if propertyType.inMedicalDiagnosis and inMedicalDiagnosis[propertyType.inMedicalDiagnosis].lower() in self.name:
                        properties.append((propertyType, action[name]))
                properties.sort(key=lambda prop:prop[0].idx)
                return toVariant(u'\n'.join(((properti[0].name + u'. ' + forceString(properti[1])) if properti[1] else u'') for properti in properties))
            return QVariant()


        def toSortString(self, val, record, action):
            return forcePyType(self.toString(val, record, action))

        def toStatusTip(self, val, record, action):
            return self.toString(val, record, action)

        def createEditor(self, parent):
            editor = QtGui.QLineEdit(parent)
            if self._maxLength:
                editor.setMaxLength(self._maxLength)
            if self._inputMask:
                editor.setInputMask(self._inputMask)
            return editor

        def setEditorData(self, editor, value, record):
            editor.setText(forceStringEx(value))

        def getEditorData(self, editor):
            text = trim(editor.text())
            if text:
                return toVariant(text)
            else:
                return QVariant()

        def alignment(self):
            return QVariant(Qt.AlignLeft + Qt.AlignTop)

    def __init__(self, parent, personsCache):
        CInDocTableModel.__init__(self, 'Action', 'id', 'event_id', parent)
        self.addCol(CEventMedicalDiagnosisTableModel.CLocActionRecordColumn(u'Запись',        'id', 50, caches = personsCache)).setReadOnly(True)
        self.addCol(CEventMedicalDiagnosisTableModel.CLocActionProperyColumn(u'Формулировка', 'id', 50, name = [u'основной', u'осложнения', u'сопутствующие'])).setReadOnly(True)
        self.readOnly = False
        self.personsCache = personsCache
        self.removeActions = []
        self.setEnableAppendLine(False)


    def setReadOnly(self, value):
        self.readOnly = value


    def flags(self, index):
        if self.readOnly:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled
        column = index.column()
        flags = self._cols[column].flags()
        if self.cellReadOnly(index):
            flags = flags & (~Qt.ItemIsEditable) & (~Qt.ItemIsUserCheckable)
        return flags


    def getEmptyRecord(self):
        return QtGui.qApp.db.table('Action').newRecord()


    def setItems(self, items):
        recordNew, actionNew = items
        record, action = self._items
        if id(record) != id(recordNew):
            self._items = items
            self.reset()


    def insertRecord(self, row, record, action):
        self.beginInsertRows(QModelIndex(), row, row)
        self._items.insert(row, (record, action))
        self.endInsertRows()


    def addRecord(self, record, action):
        self.insertRecord(len(self._items), (record, action))


    def setValue(self, row, fieldName, value):
        if 0<=row<len(self._items):
            record, action = self._items[row]
            valueAsVariant = toVariant(value)
            if record.value(fieldName) != valueAsVariant:
                record.setValue(fieldName, valueAsVariant)
                self.emitValueChanged(row, fieldName)


    def value(self, row, fieldName):
        if 0<=row<len(self._items):
            record, action = self._items[row]
            return record.value(fieldName)
        return None


    def sortData(self, column, ascending):
        pass


    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if 0 <= row < len(self._items):
            if role == Qt.EditRole:
                col = self._cols[column]
                record, action = self._items[row]
                if column == 0:
                    if action:
                        actionType = action.getType()
                        endDate = forceDateTime(record.value('endDate'))
                        personId = forceString(record.value('person_id'))
                        actionInfo = [unicode(endDate.toString('dd.MM.yyyy hh:mm:ss')) if endDate else u'',
                                      forceString(self.personsCache.get(personId).value('name')) if personId else u'',
                                      actionType.name]
                        return toVariant(u'\n'.join(val for val in actionInfo))
                elif column == 1:
                    if action:
                        actionType = action.getType()
                        properties = []
                        for name, propertyType in actionType._propertiesByName.items():
                            if propertyType.inMedicalDiagnosis and inMedicalDiagnosis[propertyType.inMedicalDiagnosis].lower() in col.name:
                                properties.append((propertyType, action[name]))
                        properties.sort(key=lambda prop:prop[0].idx)
                        return toVariant(u'\n'.join(((properti[0].name + u'. ' + forceString(properti[1])) if properti[1] else u'') for properti in properties))
                return QVariant()

            if role == Qt.DisplayRole:
                col = self._cols[column]
                record, action = self._items[row]
                return col.toString(record.value(col.fieldName()), record, action)

            if role == Qt.StatusTipRole:
                col = self._cols[column]
                record, action = self._items[row]
                return col.toStatusTip(record.value(col.fieldName()), record, action)

            if role == Qt.TextAlignmentRole:
                col = self._cols[column]
                return col.alignment()

            if role == Qt.CheckStateRole:
                col = self._cols[column]
                record, action = self._items[row]
                return col.toCheckState(record.value(col.fieldName()), record)

            if role == Qt.ForegroundRole:
                col = self._cols[column]
                record, action = self._items[row]
                return col.getForegroundColor(record.value(col.fieldName()), record)

        return QVariant()


    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            column = index.column()
            row = index.row()
            if row == len(self._items):
                if value.isNull():
                    return False
                record = self.getEmptyRecord()
                self._items.append(record, CAction(record=record))
                count = len(self._items)
                rootIndex = QModelIndex()
                self.beginInsertRows(rootIndex, count, count)
                self.insertRows(count, 1, rootIndex)
                self.endInsertRows()
            record, action = self._items[row]
            col = self._cols[column]
            record.setValue(col.fieldName(), value)
            self.emitCellChanged(row, column)
            return True
        if role == Qt.CheckStateRole:
            column = index.column()
            row = index.row()
            state = value.toInt()[0]
            if row == len(self._items):
                if state == Qt.Unchecked:
                    return False
                record = self.getEmptyRecord()
                self._items.append(record, CAction(record=record))
                count = len(self._items)
                rootIndex = QModelIndex()
                self.beginInsertRows(rootIndex, count, count)
                self.insertRows(count, 1, rootIndex)
                self.endInsertRows()
            record, action = self._items[row]
            col = self._cols[column]
            record.setValue(col.fieldName(), QVariant(0 if state == Qt.Unchecked else 1))
            self.emitCellChanged(row, column)
            return True
        return False


    def loadItems(self, masterId):
        self._items = []
        self.removeActions = []
        self.actionList = {}
        actionTypeIdList = getActionTypeIdListByFlatCode(u'medicalDiagnosis%')
        if actionTypeIdList:
            db = QtGui.qApp.db
            table = self._table
            tableAT = db.table('ActionType')
            queryTable = table.innerJoin(tableAT, tableAT['id'].eq(table['actionType_id']))
            filter = [table['event_id'].eq(masterId),
                      tableAT['deleted'].eq(0),
                      table['deleted'].eq(0),
                      table['actionType_id'].inlist(actionTypeIdList)
                      ]
            if self._filter:
                filter.append(self._filter)
            order = ['Action.endDate DESC']
            records = db.getRecordList(queryTable, u'Action.*', filter, order)
            for record in records:
                action = CAction(record=record)
                self._items.append((record, action))
        self.reset()


    def saveItems(self, masterId):
        if masterId:
            actionIdList = []
            removeActions = set(self.removeActions)
            db = QtGui.qApp.db
            for idx, (record, action) in enumerate(self._items):
                if not action:
                    action = CAction(record = record)
                record.setValue('event_id', toVariant(masterId))
                id = action.save(masterId)
                if id and id not in actionIdList:
                    actionIdList.append(id)
                removeActions = removeActions - set([id])
            self.removeActions = list(removeActions)
            if self.removeActions:
                tableAction = db.table('Action')
                filter = [tableAction['id'].inlist(self.removeActions)]
                db.deleteRecord(tableAction, filter)

                tableActionProperty = db.table('ActionProperty')
                filter = [tableActionProperty['action_id'].inlist(self.removeActions)]
                db.deleteRecord(tableActionProperty, filter)

                tableActionExecutionPlan = db.table('Action_ExecutionPlan')
                filter = [tableActionExecutionPlan['master_id'].inlist(self.removeActions)]
                db.deleteRecord(tableActionExecutionPlan, filter)
        self.removeActions = []


class CActionTypesModel(CTableModel):
    def __init__(self, parent):
        CTableModel.__init__(self, parent, [
            CTextCol(u'Код',            ['code'], 20),
            CTextCol(u'Наименование',   ['name'], 20)
            ], 'ActionType')


class CEventMedicalDiagnosisCreator(CDialogBase, Ui_EventMedicalDiagnosisCreator):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.addModels('ActionTypes', CActionTypesModel(self))
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setModels(self.tblActionTypes, self.modelActionTypes, self.selectionModelActionTypes)
        self.actionTypeId = None


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Ok:
            self.on_tblActionTypes_doubleClicked(self.tblActionTypes.currentIndex())
        elif buttonCode == QtGui.QDialogButtonBox.Cancel:
            self.actionTypeId = None
            self.close()


    def load(self):
        db = QtGui.qApp.db
        table = db.table('ActionType')
        idList = db.getDistinctIdList(table, [table['id']],
                                             [table['flatCode'].like(u'medicalDiagnosis%'), table['deleted'].eq(0)],
                                             u'ActionType.code, ActionType.name')
        self.modelActionTypes.setIdList(idList)


    @pyqtSignature('QModelIndex')
    def on_tblActionTypes_doubleClicked(self, index):
        self.actionTypeId = self.tblActionTypes.currentItemId()
        self.close()


    def getActionTypeId(self):
        return self.actionTypeId


class CEventMedicalDiagnosisEditor(CDialogBase, Ui_EventMedicalDiagnosisEditor):
    def __init__(self, parent, eventId, clientId, clientAge, clientSex):
        CDialogBase.__init__(self, parent)
        self.addModels('APActionProperties', CActionPropertiesTableModel(self))
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setModels(self.tblAPProps, self.modelAPActionProperties, self.selectionModelAPActionProperties)
        self.action = None
        self.clientId = clientId
        self.clientAge = clientAge
        self.clientSex = clientSex
        self.eventId = eventId
        self.isDirty = False
        currentDateTime = QDateTime.currentDateTime()
        self.edtDate.setDate(currentDateTime.date())
        self.edtTime.setTime(currentDateTime.time())
        self.cmbExecPerson.setReadOnly(True)


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_modelAPActionProperties_dataChanged(self, topLeft, bottomRight):
        self.isDirty = True


    def updatePropTable(self, action):
        self.tblAPProps.model().setAction(action, self.clientId, self.clientSex, self.clientAge)
        self.tblAPProps.resizeRowsToContents()


    def createAction(self, recordPrev, actionPrev):
        actionTypeId = forceRef(recordPrev.value('actionType_id'))
        if actionTypeId:
            date = self.edtDate.date()
            time = self.edtTime.time()
            execPersonId = QtGui.qApp.userId
            self.cmbExecPerson.setUserId(execPersonId)
            self.cmbExecPerson.setValue(execPersonId)
            dialogDateTime = QDateTime(date, time)
            db = QtGui.qApp.db
            tableAction = db.table('Action')
            record = tableAction.newRecord() if not self.action else self.action.getRecord()
            record.setValue('event_id', toVariant(self.eventId))
            record.setValue('actionType_id', toVariant(actionTypeId))
            record.setValue('directionDate', toVariant(dialogDateTime))
            record.setValue('begDate', toVariant(dialogDateTime))
            record.setValue('endDate', toVariant(dialogDateTime))
            record.setValue('status',  toVariant(CActionStatus.finished))
            record.setValue('person_id', toVariant(self.cmbExecPerson.value()))
            record.setValue('setPerson_id', toVariant(self.cmbExecPerson.value()))
            record.setValue('org_id',  toVariant(QtGui.qApp.currentOrgId()))
            record.setValue('amount',  toVariant(1))
            if not self.action:
                newAction = CAction(record=record)
                newAction.updateByAction(actionPrev)
                self.action = newAction
            if self.action:
                setActionPropertiesColumnVisible(self.action._actionType, self.tblAPProps)
                self.updatePropTable(self.action)
                self.tblAPProps.setEnabled(self.getIsLocked(self.action._record))
            self.isDirty = False
        return self.action.getRecord() if self.action else None, self.action


    def getRecord(self):
        return self.action.getRecord() if self.action else None, self.action


    def getIsLocked(self, record):
        if record:
            status = forceInt(record.value('status'))
            personId = forceRef(record.value('person_id'))
            if status == CActionStatus.finished and personId:
                return (QtGui.qApp.userId == personId
                                 or (QtGui.qApp.userHasRight(urEditOtherPeopleActionSpecialityOnly) and QtGui.qApp.userSpecialityId == self.getSpecialityId(personId))
                                 or QtGui.qApp.userHasRight(urEditOtherpeopleAction)
                                 or (QtGui.qApp.userHasRight(urEditSubservientPeopleAction) and QtGui.qApp.userId in getPersonOrgStructureChiefs(personId))
                               )
        return False

    def getSpecialityId(self, personId):
        specialityId = None
        if personId:
            db = QtGui.qApp.db
            tablePerson = db.table('Person')
            record = db.getRecordEx(tablePerson, [tablePerson['speciality_id']], [tablePerson['deleted'].eq(0), tablePerson['id'].eq(personId)])
            specialityId = forceRef(record.value('speciality_id')) if record else None
        return specialityId

    @pyqtSignature('QTime')
    def on_edtTime_timeChanged(self, time):
        if self.action:
            date = self.edtDate.date()
            if date:
                dialogDateTime = QDateTime(date, time)
                record = self.action.getRecord()
                record.setValue('directionDate', toVariant(dialogDateTime))
                record.setValue('begDate', toVariant(dialogDateTime))
                record.setValue('endDate', toVariant(dialogDateTime))
                self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)
            else:
                self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)


    @pyqtSignature('QDate')
    def on_edtDate_dateChanged(self, date):
        if self.action and date:
            time = self.edtTime.time()
            dialogDateTime = QDateTime(date, time)
            record = self.action.getRecord()
            record.setValue('directionDate', toVariant(dialogDateTime))
            record.setValue('begDate', toVariant(dialogDateTime))
            record.setValue('endDate', toVariant(dialogDateTime))
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)
        if not date:
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)


    @pyqtSignature('int')
    def on_cmbExecPerson_currentIndexChanged(self, index):
        if self.action:
            record = self.action.getRecord()
            execPersonId = self.cmbExecPerson.value()
            record.setValue('person_id', toVariant(execPersonId))
            record.setValue('setPerson_id', toVariant(execPersonId))


def getMedicalDiagnosisContext():
    return ['medicalDiagnosis']
