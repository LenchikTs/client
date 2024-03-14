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
from PyQt4.QtCore  import Qt, pyqtSignature, SIGNAL, QAbstractTableModel, QDate, QDateTime, QString, QTime, QVariant

from library.DialogBase import CConstructHelperMixin
from library.DialogBase import CDialogBase
from library.InDocTable import CFloatInDocTableCol, CInDocTableCol, CIntInDocTableCol
from library.TableModel import CDateCol, CDateTimeCol, CTextCol
from library.Utils      import forceDate, forceDateTime, forceRef, forceString, toVariant
from Events.Action      import CAction
#from Orgs.Utils         import getPersonChiefs
from Users.Rights       import urEditThermalSheetPastDate

from Ui_TemperatureListGroupEditor import Ui_TemperatureListGroupEditor
from Ui_GetTemperatureEditor       import Ui_GetTemperatureEditor


class CTemperatureListGroupEditorDialog(QtGui.QDialog, CConstructHelperMixin, Ui_TemperatureListGroupEditor):
    def __init__(self, parent, model, selectedRows, modelItems, actionTypeIdList):
        QtGui.QDialog.__init__(self, parent)
        self.addModels('ThermalSheet',   CThermalSheetModel(self, actionTypeIdList))
        self.addObject('btnTemperature', QtGui.QPushButton(u'Задать температуру', self))
        self.setupUi(self)
        self.setModels(self.tblThermalSheet, self.modelThermalSheet, self.selectionModelThermalSheet)
        self.buttonBox.addButton(self.btnTemperature, QtGui.QDialogButtonBox.ActionRole)
        self.isDirty = False
        currentDateTime = QDateTime.currentDateTime()
        self.edtDate.setDate(currentDateTime.date())
        self.edtTime.setTime(currentDateTime.time())
        self.loadDataItems(model, selectedRows, modelItems, actionTypeIdList)


    def loadDataItems(self, model, selectedRows, modelItems, actionTypeIdList):
        self.eventIdList = []
        self.actionIdList = {}
        self.model = model
        self.actionTypeIdList = actionTypeIdList
        self.selectedRows = selectedRows
        self.modelItems = modelItems
        date = self.edtDate.date()
        self.modelThermalSheet.setDate(date)
        time = self.edtTime.time()
        self.modelThermalSheet.setTime(time)
        dialogDateTime = QDateTime(date, time)
        execPersonId = self.cmbExecPerson.value()
        if not execPersonId:
            execPersonId = QtGui.qApp.userId
            self.cmbExecPerson.setValue(execPersonId)
        self.modelThermalSheet.setExecPerson(self.cmbExecPerson.value())
        if self.selectedRows:
            for row in self.selectedRows:
                eventId = self.model.getEventId(row) if row >= 0 else None
                clientId = self.model.getClientId(row) if row >= 0 else None
                if eventId and eventId not in self.eventIdList:
                    self.eventIdList.append(eventId)
                    self. createAction( eventId, clientId, dialogDateTime, execPersonId)
        else:
            for row, item in enumerate(self.modelItems):
                eventId = self.model.getEventId(row) if row >= 0 else None
                clientId = self.model.getClientId(row) if row >= 0 else None
                if eventId and eventId not in self.eventIdList:
                    self.eventIdList.append(eventId)
                    self. createAction( eventId, clientId, dialogDateTime, execPersonId)
        self.updatePropTable(self.actionIdList)
        self.modelThermalSheet.loadItems(self.eventIdList)
        if len(self.selectedRows) == 1:
            CDialogBase(self).setFocusToWidget(self.tblThermalSheet, 0,  7)


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Save:
            self.isDirty = False
            self.modelThermalSheet.saveItems(self.eventIdList)
        elif buttonCode == QtGui.QDialogButtonBox.Cancel:
            self.close()


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_modelThermalSheet_dataChanged(self, topLeft, bottomRight):
        self.isDirty = True


    def closeEvent(self, event):
        if self.canClose():
            self.isDirty = False
            self.modelThermalSheet.saveItems(self.eventIdList)
        QtGui.QDialog.closeEvent(self, event)


    def canClose(self):
        if self.isDirty:
            res = QtGui.QMessageBox.warning( self,
                                      u'Внимание!',
                                      u'Данные были изменены.\nСохранить изменения?',
                                      QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                      QtGui.QMessageBox.Yes)
            if res == QtGui.QMessageBox.Yes:
                self.isDirty = False
                return True
        return False


    def updatePropTable(self, actionList):
        self.tblThermalSheet.model().setAction(actionList)


    def createAction(self, eventId, selClientId, dialogDateTime, execPersonId):
        action = None
        if selClientId and eventId:
            db = QtGui.qApp.db
            tableAction = db.table('Action')
            cond = [tableAction['deleted'].eq(0),
                          tableAction['event_id'].eq(eventId),
                          tableAction['actionType_id'].inlist(self.actionTypeIdList)
                        ]
            cond.append(tableAction['endDate'].eq(dialogDateTime))
            record = db.getRecordEx(tableAction, '*', cond)
            if record:
                action = CAction(record=record)
            else:
                actionTypeId = self.actionTypeIdList[0]
                if actionTypeId:
                    record = tableAction.newRecord()
                    record.setValue('event_id', toVariant(eventId))
                    record.setValue('actionType_id', toVariant(actionTypeId))
                    record.setValue('directionDate', toVariant(dialogDateTime))
                    record.setValue('begDate', toVariant(dialogDateTime))
                    record.setValue('endDate', toVariant(dialogDateTime))
                    record.setValue('status',  toVariant(2))
                    record.setValue('person_id', toVariant(execPersonId))
                    record.setValue('org_id',  toVariant(QtGui.qApp.currentOrgId()))
                    record.setValue('amount',  toVariant(1))
                    action = CAction(record=record)
            if action:
                tableEvent = db.table('Event')
                cols = [tableEvent['setDate']]
                cond = [tableEvent['deleted'].eq(0)]
                cond.append('Event.id = IF(getFirstEventId(%s) IS NOT NULL, getFirstEventId(%s), %s)'%(eventId, eventId, eventId))
                recordEvent = db.getRecordEx(tableEvent, cols, cond)
                setDate = (forceDate(recordEvent.value('setDate'))  if recordEvent else None)
                begDate = forceDate(record.value('begDate'))
                if setDate and begDate:
                    action[u'День болезни'] = setDate.daysTo(begDate) + 1
        self.isDirty = False
        self.actionIdList[eventId] = action
        return self.actionIdList


    @pyqtSignature('')
    def on_btnTemperature_clicked(self):
        dialog = CGetTemperatureEditor(self)
        try:
            if dialog.exec_():
                self.modelThermalSheet.setNewTemperature(dialog.newTemperature)
        finally:
            dialog.deleteLater()


    @pyqtSignature('QTime')
    def on_edtTime_timeChanged(self, time):
        self.modelThermalSheet.setTime(time)


    @pyqtSignature('QDate')
    def on_edtDate_dateChanged(self, date):
        if QDate.currentDate() == date:
            isProtected = False
        else:
            isProtected = not QtGui.qApp.userHasRight(urEditThermalSheetPastDate)
        self.modelThermalSheet.setReadOnly(isProtected)
        self.modelThermalSheet.setDate(date)


    @pyqtSignature('int')
    def on_cmbExecPerson_currentIndexChanged(self, index):
        self.modelThermalSheet.setExecPerson(self.cmbExecPerson.value())


class CThermalSheetModel(QAbstractTableModel):
    column = [u'ФИО',u'Дата рождения', u'Карта', u'Помещение', u'Дата', u'Температура', u'День болезни']

    def __init__(self, parent, actionTypeIdList):
        QAbstractTableModel.__init__(self, parent)
        self._items = []
        self._cols = []
        self.actionList = {}
        self.eventInfoLast = {}
        self.clientInfoLast = {}
        self.actionInfoLast = {}
        self.cols(actionTypeIdList)
        self.actionTypeIdList = actionTypeIdList
        self.execPersonId = None
        self.dialogTime = QTime()
        self.dialogDate = QDate()
        self.readOnly = False


    def setReadOnly(self, value):
        self.readOnly = value


    def setAction(self, actionList):
        self.actionList = actionList
        self.reset()
        return self.actionList


    def setExecPerson(self, value):
        self.execPersonId = value


    def setTime(self, time):
        self.dialogTime = time


    def setDate(self, date):
        self.dialogDate = date


    def items(self):
        return  self._items


    def cols(self, actionTypeIdList):
        self._cols = [CTextCol(u'ФИО',           ['lastName', 'firstName', 'patrName'], 30, 'l'),
                      CDateCol(u'Дата рождения', ['birthDate'],                                        20, 'l'),
                      CTextCol(u'Карта',         ['eventId'],                                           20, 'l'),
                      CTextCol(u'Помещение',     ['orgStructure'],                                   20, 'l'),
                      CDateTimeCol(u'Дата',      [ 'date'],                                               20, 'l'),
                      CTextCol(u'Температура',   ['temperature'],                                   20, 'l'),
                      CTextCol(u'День болезни',  ['diseaseDay'],                                     20, 'l')
                      ]
        nameAPTList = self.getActionPropertyTypeName(actionTypeIdList)
        for nameAPT in nameAPTList:
            self._cols.append(nameAPT)
        return self._cols


    def columnCount(self, index = None):
        return len(self._cols)


    def rowCount(self, index = None):
        return len(self._items)


    def flags(self, index=None):
        if self.readOnly:
            return Qt.ItemIsEnabled|Qt.ItemIsSelectable
        column = index.column()
        result = Qt.ItemIsSelectable | Qt.ItemIsEnabled
        if column > 6:
            result |= Qt.ItemIsEditable
        return result


    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(self.column[section])
            elif role == Qt.ToolTipRole:
                if section == 4:
                    return QVariant(u'Дата и время последнего изменения температуры')
                elif section == 5:
                    return QVariant(u'Значение, соответствующее последней дате измерения температуры')
            elif role == Qt.FontRole:
                if section <= 6:
                    result = QtGui.QFont()
                    result.setBold(True)
                    return QVariant(result)
        return QVariant()


    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            item = self._items[row]
            return toVariant(item[column])
        elif role == Qt.EditRole:
            item = self._items[row]
            return toVariant(item[column])
        return QVariant()


    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            column = index.column()
            row = index.row()
            self._items[row][column] = value
            self.emitCellChanged(row, column)
            return True
        return False


    def emitCellChanged(self, row, column):
        index = self.index(row, column)
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)


    def emitRowChanged(self, row):
        self.emitRowsChanged(row, row)


    def emitRowsChanged(self, begRow, endRow):
        index1 = self.index(begRow, 0)
        index2 = self.index(endRow, self.columnCount())
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index1, index2)


    def emitColumnChanged(self, column):
        index1 = self.index(0, column)
        index2 = self.index(self.rowCount(), column)
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index1, index2)


    def emitAllChanged(self):
        index1 = self.index(0, 0)
        index2 = self.index(self.rowCount(), self.columnCount())
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index1, index2)


    def createEditor(self, index, parent):
        column = index.column()
        return self._cols[column].createEditor(parent)


    def setEditorData(self, column, editor, value, record):
        return self._cols[column].setEditorData(editor, value, record)


    def getEditorData(self, column, editor):
        return self._cols[column].getEditorData(editor)


    def afterUpdateEditorGeometry(self, editor, index):
        pass


    def getActionPropertyTypeName(self, actionTypeIdList):
        nameAPTList = []
        db = QtGui.qApp.db
        tableAPT = db.table('ActionPropertyType')
        cols = [tableAPT['name'],
                tableAPT['id'],
                tableAPT['typeName']
                ]
        cond = [tableAPT['deleted'].eq(0),
                tableAPT['actionType_id'].inlist(actionTypeIdList),
                tableAPT['name'].notlike(u'День болезни')
                ]
        records = db.getRecordList(tableAPT, cols, cond)
        for record in records:
            nameAPT = forceString(record.value('name'))
            typeName = forceString(record.value('typeName'))
            id = forceString(record.value('id'))
            addColumnBoolean = False
            if nameAPT and nameAPT not in nameAPTList:
                if u'integer' in typeName.lower():
                    nameAPTList.append(CIntInDocTableCol(nameAPT, [id], 20, low=0, high=99999))
                    addColumnBoolean = True
                elif u'temperature' in typeName.lower():
                    nameAPTList.append(CDoubleInDocTableCol(nameAPT, [id], 20, precision=2))
                    addColumnBoolean = True
                elif u'arterialpressure' in typeName.lower():
                    nameAPTList.append(CIntInDocTableCol(nameAPT, [id], 20, low=0, high=999))
                    addColumnBoolean = True
                elif u'pulse' in typeName.lower():
                    nameAPTList.append(CIntInDocTableCol(nameAPT, [id], 20, low=0, high=999))
                    addColumnBoolean = True
                elif u'string' in typeName.lower():
                    nameAPTList.append(CInDocTableCol(nameAPT, [id], 20, low=0, high=99999))
                    addColumnBoolean = True
                if addColumnBoolean:
                    self.column.append(nameAPT)
        return nameAPTList


    def loadItems(self, masterIdList):
        self._items = []
        self.eventInfoLast = {}
        self.clientInfoLast = {}
        self.actionInfoLast = {}
#        db = QtGui.qApp.db
#        tableClient = db.table('Client')
#        tableEvent = db.table('Event')
        for eventId in masterIdList:
            self.getClientInfoLast(eventId)
            self.getDataTimeLast(eventId)
            clientInfoLast = self.clientInfoLast.get(eventId, [None, u'', u''])
            dataTimeLast = self.eventInfoLast.get(eventId, [u'', u'', u''])
            action = self.actionList.get(eventId, None)
            item = [clientInfoLast[1],
                    clientInfoLast[2],
                    eventId,
                    u'',
                    dataTimeLast[0],
                    dataTimeLast[1],
                    dataTimeLast[2],
                    ]
            for i in range(7, len(self._cols)):
                name = forceString(self._cols[i]._title)
                item.append(action[name] if (action and name) else u'')
            self._items.append(item)
        self.reset()


    def saveItems(self, masterIdList):
        dialogDateTime = QDateTime(self.dialogDate, self.dialogTime)
        for item in self._items:
            eventId = item[2]
            if eventId:
                action = self.actionList.get(eventId, None)
                if action:
                    record = action.getRecord()
                    record.setValue('directionDate', toVariant(dialogDateTime))
                    record.setValue('begDate', toVariant(dialogDateTime))
                    record.setValue('endDate', toVariant(dialogDateTime))
                    record.setValue('person_id', toVariant(self.execPersonId))
                    eventInfo = self.eventInfoLast.get(eventId, [u'', u'', u'', u''])
                    setDate = eventInfo[3]
                    if setDate:
                        action[u'День болезни'] = setDate.daysTo(self.dialogDate) + 1
                    for i in range(7, len(self._cols)):
                        name = forceString(self._cols[i]._title)
                        action[name] = toVariant(item[i])
                    action.save(eventId)


    def setNewTemperature(self, newTemperature):
        for item in self._items:
            eventId = item[2]
            if eventId:
                action = self.actionList.get(eventId, None)
                if action:
                    name = forceString(self._cols[7]._title)
                    action[name] = toVariant(newTemperature)
                    item[7] = action[name]
        self.reset()


    def getClientInfoLast(self, eventId):
        if eventId and self.actionTypeIdList:
            db = QtGui.qApp.db
            tableClient = db.table('Client')
            tableEvent = db.table('Event')
            cols = [tableClient['id'],
                        tableClient['lastName'],
                        tableClient['firstName'],
                        tableClient['patrName'],
                        tableClient['sex'],
                        tableClient['birthDate']
                        ]
            cond = [tableEvent['id'].eq(eventId),
                          tableEvent['deleted'].eq(0),
                          tableClient['deleted'].eq(0)
                          ]
            queryTable =  tableEvent.innerJoin(tableClient, tableClient['id'].eq(tableEvent['client_id']))
            record = db.getRecordEx(queryTable, cols, cond, order='Client.lastName,Client.firstName,Client.patrName,Client.birthDate')
            if record:
                clientId = forceRef(record.value('id'))
                clientFIO = forceString(record.value('lastName')) + u' ' + forceString(record.value('firstName')) + u' ' + forceString(record.value('patrName'))
                birthDate = forceString(forceDate(record.value('birthDate')))
                self.clientInfoLast[eventId] = [clientId, clientFIO, birthDate]


    def getDataTimeLast(self, eventId):
        if eventId and self.actionTypeIdList:
            db = QtGui.qApp.db
            tableAction = db.table('Action')
            tableAP = db.table('ActionProperty')
            tableAPT = db.table('ActionPropertyType')
            tableAP_Temperature = db.table('ActionProperty_Temperature')
            cols =  [tableAP_Temperature['value'].alias('temperatureLast'),
                         tableAction['endDate'],
                         tableAction['event_id'].alias('eventId')
                         ]
            cols.append('(SELECT Event.setDate FROM Event WHERE Event.deleted = 0 AND  Event.id = IF(getFirstEventId(Action.event_id) IS NOT NULL, getFirstEventId(Action.event_id), Action.event_id)) AS setDate')
            cond = [  tableAction['event_id'].eq(eventId),
                            tableAP['deleted'].eq(0),
                            tableAPT['deleted'].eq(0),
                            tableAction['deleted'].eq(0),
                            tableAction['actionType_id'].inlist(self.actionTypeIdList),
                            tableAPT['id'].eq(tableAP['type_id']),
                            tableAPT['actionType_id'].inlist(self.actionTypeIdList),
                            tableAPT['name'].like(u'Температура')
                         ]
            queryTable =  tableAction.innerJoin(tableAP, tableAP['action_id'].eq(tableAction['id']))
            queryTable =  queryTable.innerJoin(tableAPT, tableAPT['actionType_id'].eq(tableAction['actionType_id']))
            queryTable =  queryTable.innerJoin(tableAP_Temperature, tableAP_Temperature['id'].eq(tableAP['id']))
            record = db.getRecordEx(queryTable, cols, cond, order='Action.endDate DESC')
            if record:
                eventId = forceRef(record.value('eventId'))
                setDate = forceDate(record.value('setDate'))
                endDate = forceDateTime(record.value('endDate'))
                if endDate:
                    diseaseDay = setDate.daysTo(endDate.date()) + 1
                else:
                    diseaseDay = 0
                self.eventInfoLast[eventId] = [endDate, forceString(record.value('temperatureLast')), diseaseDay, setDate]


class CDoubleInDocTableCol(CFloatInDocTableCol):
    def __init__(self, title, fieldName, width, **params):
        CFloatInDocTableCol.__init__(self, title, fieldName, width, **params)


    def createEditor(self, parent):
        editor = QtGui.QLineEdit(parent)
        validator = QtGui.QDoubleValidator(editor)
        editor.setValidator(validator)
        editor.setMaxLength(4)
        editor.validator().setTop(99.9)
        editor.setInputMask(QString('00.0'))
        return editor


class CGetTemperatureEditor(QtGui.QDialog, CConstructHelperMixin, Ui_GetTemperatureEditor):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.newTemperature = None


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Ok:
            self.newTemperature = self.edtNewTemperature.value()
            self.close()
        elif buttonCode == QtGui.QDialogButtonBox.Cancel:
            self.close()

