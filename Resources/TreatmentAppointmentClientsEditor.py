# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4                    import QtGui
from PyQt4.QtCore             import Qt, pyqtSignature, QVariant

from Events.Utils             import getActionTypeIdListByFlatCode
from library.DialogBase       import CDialogBase
from library.TableModel       import CCol
from library.PreferencesMixin import CDialogPreferencesMixin
from library.Utils            import forceRef, forceString, forceStringEx, forceInt, forceDate, formatShortNameInt, formatSex, toVariant, addDots
from Reports.Utils            import getDataOrgStructureName
from Resources.TreatmentAppointmentDialog import CRecordsTableModel

from Resources.Ui_TreatmentAppointmentClientsEditor import Ui_TreatmentAppointmentClientsEditor


class CTreatmentAppointmentClientsEditor(CDialogBase, Ui_TreatmentAppointmentClientsEditor, CDialogPreferencesMixin):
    def __init__(self, parent, filter=None, clientCache=None):
        CDialogBase.__init__(self, parent)
        self.tableModel = CTreatmentClientsTableModel(self, clientCache)
        self.tableSelectionModel = QtGui.QItemSelectionModel(self.tableModel, self)
        self.tableSelectionModel.setObjectName('tableSelectionModel')
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setWindowTitle(u'Список пациентов')
        self.tblTreatmentClientList.setModel(self.tableModel)
        self.tblTreatmentClientList.setSelectionModel(self.tableSelectionModel)
        self.tblTreatmentClientList.installEventFilter(self)
        self.tblTreatmentClientList.addPopupDelRow()
        self._parent = parent
        self.params = {}
        self.dateSchedule = None
        self.busyClientIdList = []
        self.on_buttonBox_reset()
        self.clientCache = clientCache
        self.filter = filter
        self.loadDialogPreferences()


    @pyqtSignature('QModelIndex')
    def on_tblTreatmentClientList_doubleClicked(self, index):
        self.clientId = None
        self.eventId = None
        currentIndex = self.tblTreatmentClientList.currentIndex()
        if currentIndex.isValid():
            row = currentIndex.row()
            items = self.tblTreatmentClientList.model().items
            if row >= 0 and row < len(items):
                item = items[row]
                self.clientId = forceRef(item.value('client_id'))
                self.eventId = forceRef(item.value('id'))
        QtGui.QDialog.accept(self)


    @pyqtSignature('QAbstractButton*')
    def on_buttonBoxFilter_clicked(self, button):
        buttonCode = self.buttonBoxFilter.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Apply:
            self.on_buttonBox_apply()
        elif buttonCode == QtGui.QDialogButtonBox.Reset:
            self.on_buttonBox_reset()


    def on_buttonBox_reset(self):
        self.edtLastName.setText(u'')
        self.edtFirstName.setText(u'')
        self.edtPatrName.setText(u'')
        self.edtBirthDate.setDate(None)
        self.cmbSex.setCurrentIndex(0)


    def loadData(self, dateSchedule):
        self.dateSchedule = dateSchedule


    def setBusyClientIdList(self, busyClientIdList):
        self.busyClientIdList = busyClientIdList


    def on_buttonBox_apply(self):
        self.tblTreatmentClientList.model().items = []
        if not self.dateSchedule:
            self.tblTreatmentClientList.model().reset()
            return
        lastName = forceString(self.edtLastName.text())
        firstName = forceString(self.edtFirstName.text())
        patrName = forceString(self.edtPatrName.text())
        birthDate = forceDate(self.edtBirthDate.date())
        sex = forceInt(self.cmbSex.currentIndex())
        db = QtGui.qApp.db
        tableAPT = db.table('ActionPropertyType')
        tableAP = db.table('ActionProperty')
        tableActionType = db.table('ActionType')
        tableAction = db.table('Action')
        tableEvent = db.table('Event')
        tableClient = db.table('Client')
        tableAPHB = db.table('ActionProperty_HospitalBed')
        tableEventType = db.table('EventType')
        tableRBMedicalAidType = db.table('rbMedicalAidType')
        cols = [u'DISTINCT Event.*']
        cols.append(getDataOrgStructureName(u'Отделение пребывания'))
        queryTable = tableAction.innerJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
        queryTable = queryTable.innerJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))
        queryTable = queryTable.innerJoin(tableEventType, tableEventType['id'].eq(tableEvent['eventType_id']))
        queryTable = queryTable.innerJoin(tableRBMedicalAidType, tableRBMedicalAidType['id'].eq(tableEventType['medicalAidType_id']))
        queryTable = queryTable.innerJoin(tableClient, tableClient['id'].eq(tableEvent['client_id']))
        queryTable = queryTable.innerJoin(tableAPT, tableAPT['actionType_id'].eq(tableActionType['id']))
        queryTable = queryTable.innerJoin(tableAP, tableAP['type_id'].eq(tableAPT['id']))
        queryTable = queryTable.innerJoin(tableAPHB, tableAPHB['id'].eq(tableAP['id']))
        cond = [ tableActionType['id'].inlist(getActionTypeIdListByFlatCode(u'moving%%')),
                 tableAction['deleted'].eq(0),
                 tableEvent['deleted'].eq(0),
                 tableEventType['deleted'].eq(0),
                 tableRBMedicalAidType['code'].eq('8'),
                 tableAP['deleted'].eq(0),
                 tableClient['deleted'].eq(0),
                 tableAPT['deleted'].eq(0),
                 tableAP['action_id'].eq(tableAction['id']),
                 tableAPT['typeName'].eq('HospitalBed')
               ]
        if self.busyClientIdList:
            cond.append(tableClient['id'].notInlist(self.busyClientIdList))
        if lastName:
            cond.append(tableClient['lastName'].like(addDots(lastName)))
        if firstName:
            cond.append(tableClient['firstName'].like(addDots(firstName)))
        if patrName:
            cond.append(tableClient['patrName'].like(addDots(patrName)))
        if birthDate:
            cond.append(tableClient['birthDate'].eq(birthDate))
        if sex > 0:
            cond.append(tableClient['sex'].eq(sex))
        if self.dateSchedule:
            cond.append(tableAction['begDate'].dateLe(self.dateSchedule))
            cond.append(db.joinOr([tableAction['endDate'].isNull(), tableAction['endDate'].dateGe(self.dateSchedule)]))
        records = db.getRecordList(queryTable, cols, cond, [tableClient['lastName'].name(), tableClient['firstName'].name(), tableClient['patrName'].name()])
        for record in records:
            self.tblTreatmentClientList.model().items.append(record)
        self.tblTreatmentClientList.model().reset()


    def getValue(self):
        return self.eventId, self.clientId


    def saveData(self):
        return True


class CTreatmentClientsTableModel(CRecordsTableModel):
    class CLocNumberColumn(CCol):
        def __init__(self, title, fields, defaultWidth, alignment='l'):
            CCol.__init__(self, title, fields, defaultWidth, alignment)

        def format(self, values):
            return toVariant(forceInt(values[0]))

        def getValue(self, values):
            return forceInt(values[0])

    class CLocClientColumn(CCol):
        def __init__(self, title, fields, defaultWidth, clientCache):
            CCol.__init__(self, title, fields, defaultWidth, 'l')
            self.clientCache = clientCache

        def format(self, values):
            val = values[0]
            clientId  = forceRef(val)
            clientRecord = self.clientCache.get(clientId)
            if clientRecord:
                name = formatShortNameInt(forceString(clientRecord.value('lastName')),
                   forceString(clientRecord.value('firstName')),
                   forceString(clientRecord.value('patrName'))) + u',' + forceString(clientRecord.value('birthDate')) + u',' + formatSex(clientRecord.value('sex')) + u',' + forceString(clientId)
                return toVariant(name)
            return CCol.invalid

    class CLocOrgStructurePresenceColumn(CCol):
        def __init__(self, title, fields, defaultWidth):
            CCol.__init__(self, title, fields, defaultWidth, 'l')

        def format(self, values):
            eventId  = forceRef(values[0])
            if eventId:
                record = values[1]
                if record:
                    return toVariant(forceStringEx(record.value('nameOrgStructure')))
            return CCol.invalid

    def __init__(self, parent, clientCache):
        CRecordsTableModel.__init__(self, parent)
        self.addColumn(CTreatmentClientsTableModel.CLocNumberColumn(u'№', ['id'], 5))
        self.addColumn(CTreatmentClientsTableModel.CLocClientColumn( u'Ф.И.О.', ['client_id'], 60, clientCache))
        self.addColumn(CTreatmentClientsTableModel.CLocOrgStructurePresenceColumn(u'Отделение пребывания', ['id'], 25))
        self.setTable('Event')


    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if 0 <= row < len(self.items):
            if role == Qt.DisplayRole:
                col = self._cols[column]
                record = self.items[row]
                if column == 0:
                    return col.format([row+1, record])
                else:
                    return col.format([record.value(col.fields()[0]), record])
            if role == Qt.TextAlignmentRole:
                col = self._cols[column]
                return col.alignment()
            if role == Qt.CheckStateRole:
                col = self._cols[column]
                record = self.items[row]
                return col.checked([record.value(col.fields()[0]), record])
            elif role == Qt.ForegroundRole:
                col = self._cols[column]
                record = self.items[row]
                return col.getForegroundColor([record.value(col.fields()[0]), record])
        return QVariant()

