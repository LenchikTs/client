# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2023 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature, Qt, QVariant, SIGNAL, QDate

from library.DialogBase import CDialogBase
from library.TableModel import CTableModel, CBoolCol, CDateCol, CEnumCol, CRefBookCol, CTextCol
from library.Utils import forceRef, forceInt, forceDate, forceString

from Events.Action import CAction
from Events.ActionPropertiesTable import CActionPropertiesTableModel
from Events.ActionStatus import CActionStatus
from Events.ActionTypeCol import CActionTypeCol
from Events.Utils import setActionPropertiesColumnVisible, getActionTypeDescendants

from Orgs.Utils import getOrgStructurePersonIdList

from Events.Ui_PropertyEditorAmbCardDialog import Ui_PropertyEditorAmbCardDialog


class CPropertyEditorAmbCard(CDialogBase, Ui_PropertyEditorAmbCardDialog):
    def __init__(self, parent, clientId, clientSex, clientAge, eventTypeId, actionProperty):
        CDialogBase.__init__(self, parent)
        self.clientId = clientId
        self.clientSex = clientSex
        self.clientAge = clientAge
        self.eventTypeId = eventTypeId
        self.actionProperty = actionProperty

        self.addModels('Actions', CAmbCardActionsCheckTableModel(self))
        self.addModels('ActionProperties', CActionPropertiesTableModel(self))
        self.addObject('actPrintActions', QtGui.QAction(u'Преобразовать в текст и вставить в блок', self))
        self.setupUi(self)

        self.setWindowTitle(self.actionProperty.type().name)
        propValue = self.actionProperty.getValue()
        if propValue:
            self.edtPropertyText.setPlainText(propValue)
        self.setModels(self.tblActions, self.modelActions, self.selectionModelActions)
        self.setModels(self.tblActionProperties, self.modelActionProperties, self.selectionModelActionProperties)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)

        self.tblActions.createPopupMenu([self.actPrintActions])
        self.tblActionProperties.setEditTriggers(QtGui.QAbstractItemView.SelectedClicked
                                                 | QtGui.QAbstractItemView.DoubleClicked)
        self.tblActionProperties.model().setReadOnly(True)
        self.tblActionProperties.addPopupCopyCell()
        self.tblActionProperties.addPopupSeparator()

        self.cmbSpeciality.setTable('rbSpeciality')
        self.cmbGroup.setClasses([0, 1, 2, 3])
        self.cmbGroup.setClassesVisible(True)
        self.resetFilters()
        self.loadActions()


    def loadActions(self):
        db = QtGui.qApp.db
        tableAction = db.table('Action')
        tableEvent = db.table('Event')
        tablePerson = db.table('Person')
        tableActionType = db.table('ActionType')
        queryTable = tableAction.leftJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))
        queryTable = queryTable.leftJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))

        specialityId = self.cmbSpeciality.value()
        status = self.cmbStatus.value()
        begDate = self.edtBegDate.date()
        endDate = self.edtEndDate.date()
        actionGroupId = self.cmbGroup.value()
        orgStructureId = self.cmbOrgStructure.value()
        actionTypeclass = self.cmbGroup.getClass()
        hasAttachedFiles = self.chkHasAttachedFiles.isChecked()
        hasProperties = self.chkHasProperties.isChecked()
        cond = [tableAction['deleted'].eq(0),
                tableEvent['deleted'].eq(0),
                tableEvent['client_id'].eq(self.clientId)]
        if begDate:
            cond.append(tableAction['begDate'].dateGe(begDate))
        if endDate:
            cond.append(tableAction['begDate'].dateLe(endDate))
        if specialityId:
            queryTable = queryTable.leftJoin(tablePerson, tablePerson['id'].eq(tableAction['person_id']))
            cond.append(tablePerson['speciality_id'].eq(specialityId))
        if status is not None:
            cond.append(tableAction['status'].eq(status))
        if actionGroupId:
            cond.append(tableAction['actionType_id'].inlist(getActionTypeDescendants(actionGroupId)))
        elif actionTypeclass is not None:
            cond.append(tableActionType['class'].eq(actionTypeclass))
        if orgStructureId:
            cond.append(tableAction['person_id'].inlist(getOrgStructurePersonIdList(orgStructureId)))
        if hasAttachedFiles:
            tableAFA = db.table('Action_FileAttach')
            cond.append(db.existsStmt(tableAFA, [tableAFA['master_id'].eq(tableAction['id']),
                                                 tableAFA['deleted'].eq(0)]))
        if hasProperties:
            tableAPT = db.table('ActionPropertyType')
            cond.append(db.existsStmt(tableAPT, [tableAPT['actionType_id'].eq(tableActionType['id']),
                                                 tableAPT['deleted'].eq(0)]))
        order = ['Action.endDate DESC', 'Action.begDate DESC', 'Action.id']
        try:
            QtGui.QApplication.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor))
            idList = db.getIdList(queryTable, tableAction['id'].name(), cond, order)
            self.tblActions.setIdList(idList)
        finally:
            QtGui.QApplication.restoreOverrideCursor()


    @pyqtSignature('')
    def on_actPrintActions_triggered(self):
        selectedIdList = self.modelActions.getSelectedIdList()
        actionDictValues = self.getSelectedActions(selectedIdList)
        if actionDictValues:
            oldValue = self.edtPropertyText.toPlainText()
            oldValue = oldValue.replace('\0', '')
            newValue = u'\n'.join((val[0] + val[1]) for val in actionDictValues if val)
            newValue = newValue.replace('\0', '')
            value = (oldValue + u'\n' + newValue) if oldValue else newValue
            self.edtPropertyText.setText(value)


    @staticmethod
    def getSelectedActions(selectedIdList):
        actionDict = {}
        db = QtGui.qApp.db
        table = db.table('Action')
        for _id in selectedIdList:
            if _id and _id not in actionDict.keys():
                record = db.getRecordEx(table, '*', [table['id'].eq(_id), table['deleted'].eq(0)])
                if record:
                    action = CAction(record=record)
                    if action:
                        endDate = forceDate(record.value('endDate'))
                        actionType = action.getType()
                        actionLine = [u'', u'']
                        valuePropertyList = []
                        actionLine[0] = unicode(endDate.toString('dd.MM.yyyy')) + u' ' + actionType.name + u': '
                        propertiesById = action.getPropertiesById()
                        properties = propertiesById.values()
                        properties.sort(key=lambda item: item.type().idx)
                        for prop in properties:
                            propType = prop.type()
                            if prop.getValue() and not propType.isJobTicketValueType():
                                valuePropertyList.append(propType.name + u' - ' + (
                                    forceString(prop.getText()) if not propType.isBoolean() else (
                                        u'Да' if prop.getValue() else u'Нет')))
                        actionLine[1] = u'; '.join(val for val in valuePropertyList if val)
                        actionDict[_id] = actionLine
        actionDictValues = actionDict.values()
        actionDictValues.sort(key=lambda x: x[0])
        return actionDictValues


    @pyqtSignature('')
    def on_tblActions_popupMenuAboutToShow(self):
        notEmpty = self.modelActions.rowCount() > 0
        self.actPrintActions.setEnabled(notEmpty)


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelActions_currentRowChanged(self, current, previous):
        self.updateAmbCardPropertiesTable(current, self.tblActionProperties, previous)


    def updateAmbCardPropertiesTable(self, index, tbl, previous=None):
        if previous:
            tbl.savePreferencesLoc(previous.row())
        row = index.row()
        record = index.model().getRecordByRow(row) if row >= 0 else None
        if record:
            clientId = self.clientId
            clientSex = self.clientSex
            clientAge = self.clientAge
            action = CAction(record=record)
            tbl.model().setAction2(action, clientId, clientSex, clientAge, eventTypeId=self.eventTypeId)
            setActionPropertiesColumnVisible(action.actionType(), tbl)
            tbl.resizeColumnsToContents()
            tbl.resizeRowsToContents()
            tbl.horizontalHeader().setStretchLastSection(True)
            tbl.loadPreferencesLoc(tbl.preferencesLocal, row)
        else:
            tbl.model().setAction2(None, None)


    @pyqtSignature('QAbstractButton*')
    def on_btnFiltersButtonBox_clicked(self, button):
        buttonCode = self.btnFiltersButtonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Apply:
            self.loadActions()
        elif buttonCode == QtGui.QDialogButtonBox.Reset:
            self.resetFilters()
            self.loadActions()


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Ok:
            self.actionProperty.setValue(self.edtPropertyText.toPlainText())
        elif buttonCode == QtGui.QDialogButtonBox.Cancel:
            self.close()


    def resetFilters(self):
        self.cmbSpeciality.setValue(None)
        self.cmbStatus.setValue(2)
        self.cmbGroup.setValue(None)
        self.cmbOrgStructure.setValue(None)
        self.edtBegDate.setDate(QDate.currentDate().addDays(-30))
        self.edtEndDate.setDate(None)
        self.chkHasAttachedFiles.setChecked(False)
        self.chkHasProperties.setChecked(False)


    def destroy(self):
        self.tblActionProperties.setModel(None)
        self.tblActions.setModel(None)
        del self.modelActionProperties
        del self.modelActions


class CAmbCardActionsCheckTableModel(CTableModel):
    class CEnableCol(CBoolCol):
        def __init__(self, title, fields, defaultWidth, selector):
            CBoolCol.__init__(self, title, fields, defaultWidth)
            self.selector = selector

        def checked(self, values):
            _id = forceRef(values[0])
            if self.selector.isSelected(_id):
                return CBoolCol.valChecked
            else:
                return CBoolCol.valUnchecked


    def __init__(self, parent):
        CTableModel.__init__(self, parent)
        self.enableIdList = []
        self.actionsPropertiesRegistry = {}
        self.includeItems = {}
        self.addColumn(CAmbCardActionsCheckTableModel.CEnableCol(u'Выбрать', ['id'], 5, self))
        self.addColumn(CDateCol(u'Назначено', ['directionDate'], 15))
        self.addColumn(CActionTypeCol(u'Тип', 15))
        self.addColumn(CEnumCol(u'Состояние', ['status'], CActionStatus.names, 4))
        self.addColumn(CDateCol(u'Начато', ['begDate'], 15))
        self.addColumn(CDateCol(u'Окончено', ['endDate'], 15))
        self.addColumn(CRefBookCol(u'Назначил', ['setPerson_id'], 'vrbPersonWithSpeciality', 20))
        self.addColumn(CRefBookCol(u'Выполнил', ['person_id'], 'vrbPersonWithSpeciality', 20))
        self.addColumn(CTextCol(u'Примечания', ['note'], 6))
        self.setTable('Action')
        self._mapColumnToOrder = {u'directionDate': u'Action.directionDate',
                                  u'actionType_id': u'ActionType.name',
                                  u'status': u'Action.status',
                                  u'begDate': u'Action.begDate',
                                  u'endDate': u'Action.endDate',
                                  u'setPerson_id': u'vrbPersonWithSpeciality.name',
                                  u'person_id': u'vrbPersonWithSpeciality.name',
                                  u'note': u'Action.note'}
        self.basicAdditionalDict = {}
        self.eventId = None
        self.eventIdDict = {}
        self._idList = []

    def sort(self, col, sortOrder=Qt.AscendingOrder):
        if self._idList:
            db = QtGui.qApp.db
            table = db.table('Action')
            cond = [table['id'].inlist(self._idList)]
            colClass = self.cols()[col]
            colName = colClass.fields()[0]
            if col in [2, 9, 10]:
                tableSort = db.table('ActionType' if col == 2 else colClass.tableName).alias('fieldSort')
                table = table.leftJoin(tableSort, tableSort['id'].eq(table[colName]))
                colName = 'fieldSort.name'
            order = '{} {}'.format(colName, u'DESC' if sortOrder else u'ASC')
            self._idList = db.getIdList(table, table['id'].name(), where=cond, order=order)
            self.reset()

    def setEventId(self, eventId):
        self.eventId = eventId

    def setEventIdDict(self, eventIdDict):
        self.eventIdDict = eventIdDict

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

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            (col, values) = self.getRecordValues(column, row)
            return col.format(values)
        elif role == Qt.TextAlignmentRole:
            col = self._cols[column]
            return col.alignment()
        elif role == Qt.CheckStateRole:
            (col, values) = self.getRecordValues(column, row)
            return col.checked(values)
        elif role == Qt.ForegroundRole:
            (col, values) = self.getRecordValues(column, row)
            return col.getForegroundColor(values)
        elif role == Qt.BackgroundRole:
            (col, values) = self.getRecordValues(column, row)
            return col.getBackgroundColor(values)
        elif role == Qt.FontRole:
            if 0 <= row < len(self._idList):
                actionId = forceRef(self._idList[row])
                if self.eventId == self.eventIdDict.get(actionId, None):
                    result = QtGui.QFont()
                    result.setBold(True)
                    return QVariant(result)
        return QVariant()

    def setData(self, index, value, role=Qt.EditRole):
        row = index.row()
        column = index.column()
        if role == Qt.CheckStateRole and column == 0:
            _id = self._idList[row]
            if _id:
                self.setSelected(_id, forceInt(value) == Qt.Checked)
                self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)
            return True
        return CTableModel.setData(self, index, value, role)

    def setSelected(self, _id, value):
        present = self.isSelected(_id)
        if value:
            if not present:
                self.enableIdList.append(_id)
        else:
            if present:
                self.enableIdList.remove(_id)

    def isSelected(self, _id):
        return _id in self.enableIdList

    def getSelectedIdList(self):
        return self.enableIdList
