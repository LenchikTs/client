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

from PyQt4                   import QtGui
from PyQt4.QtCore            import Qt, QAbstractTableModel, QObject, QVariant, pyqtSignature, SIGNAL

from library.DialogBase      import CConstructHelperMixin
from library.Utils           import forceString, formatShortName, toVariant

from Events.Ui_ClientPayersList     import Ui_ClientPayersList


class CClientPayersList(QtGui.QDialog, Ui_ClientPayersList, CConstructHelperMixin):
    def __init__(self,  parent, clientId, title):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle(title)
        if title!=u'Связи':
            self.addModels('PayersList', CPayersListModel(self))
        else:
            self.addModels('PayersList', CClientRelationsModel(self))
        self.setModels(self.tblPayersList, self.modelPayersList, self.selectionModelPayersList)
        self.tblPayersList.setColumnHidden(3, True)
        self.tblPayersList.setColumnHidden(4, True)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.clientId = clientId
        self.selectedRecord = None
        self.modelPayersList.loadData(clientId)
        self.payerOrCustomer = None
        QObject.connect(self.tblPayersList, SIGNAL("doubleClicked(QModelIndex)"), self.on_payersList_doubleClicked)


    def on_payersList_doubleClicked(self, index):
        index = self.tblPayersList.currentIndex()
        if index.isValid():
            row = index.row()
            item = self.modelPayersList.items[row]
            record = item[3]
            self.payerOrCustomer = item[4]
            self.selectedRecord = record
            self.close()


    def getSelectedRecord(self):
        return self.selectedRecord, self.payerOrCustomer


    def getCount(self):
        return self.modelPayersList.getCount()


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        self.close()


class CPayersListModel(QAbstractTableModel):
    column = [u'ФИО', u'Дата', u'Номер договора', 'record', 'payerOrCustomer']


    def __init__(self, parent):
        QAbstractTableModel.__init__(self, parent)
        self.items = []


    def columnCount(self, index = None):
        return 5


    def rowCount(self, index = None):
        return len(self.items)

    def getCount(self):
        return self.rowCount()


    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(self.column[section])
        return QVariant()


    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()
        if role == Qt.DisplayRole:
            item = self.items[row]
            return toVariant(item[column])
        return QVariant()


    def loadData(self, clientId):
        db = QtGui.qApp.db
        tableEvent = db.table('Event')
        tableEventLC = db.table('Event_LocalContract')
        table = tableEvent.leftJoin(tableEventLC, tableEventLC['master_id'].eq(tableEvent['id']))
        recordList = db.getRecordList(table, 'Event_LocalContract.*', [tableEvent['client_id'].eq(clientId),
                                                                                                                tableEventLC['deleted'].eq(0)], 'Event.setDate')
        for record in recordList:
            lastName = forceString(record.value('lastName'))
            firstName = forceString(record.value('firstName'))
            patrName = forceString(record.value('patrName'))
            customerLastName = forceString(record.value('customerLastName'))
            customerFirstName = forceString(record.value('customerFirstName'))
            customerPatrName = forceString(record.value('customerPatrName'))
            number = forceString(record.value('numberContract'))
            date = forceString(record.value('dateContract'))
            name1 = None
            if lastName:
                name1 = lastName
            if len(firstName) > 0:
                name1 += ' %s.'%firstName[0]
            if len(patrName) > 0:
                name1 += ' %s.'%patrName[0]
            name2 = None
            if customerLastName:
                name2 = customerLastName
            if len(customerFirstName) > 0:
                name2 += ' %s.'%customerFirstName[0]
            if len(customerPatrName) > 0:
                name2 += ' %s.'%customerPatrName[0]
            if name1:
                item = [name1, date, number, record, 0]
                self.items.append(item)
            if name2:
                item = [name2, date, number, record, 1]
                self.items.append(item)
        self.reset()


class CClientRelationsModel(CPayersListModel):
    column = [u'ФИО', u'Дата рождения', u'Связь', 'record', 'EmptyColumn']
    def __init__(self, parent):
        CPayersListModel.__init__(self, parent)
        self.count = 0


    def loadData(self, clientId):
        db = QtGui.qApp.db
        tableCR = db.table('ClientRelation')
        self.count = 0
        self.addSelf(clientId)
        self.addPatronItem(db, tableCR, 'relative_id', 'relativeId', [tableCR['client_id'].eq(clientId), tableCR['deleted'].eq(0)])
        self.addPatronItem(db, tableCR, 'client_id', 'clientId', [tableCR['relative_id'].eq(clientId), tableCR['deleted'].eq(0)])
        self.reset()


    def getCount(self):
        return self.count


    def addSelf(self, clientId):
        db = QtGui.qApp.db
        tableC  = db.table('Client')
        tableD = db.table('ClientDocument')
        queryTable = tableC.leftJoin(tableD, tableD['client_id'].eq(tableC['id']))
        cond = [tableC['id'].eq(clientId),
                tableC['deleted'].eq(0),
                tableD['deleted'].eq(0)
                ]
        fields = [tableC['lastName'].alias(), tableC['firstName'].name(),
                  tableC['patrName'].name(), tableC['birthDate'].name(),
                  'getClientRegAddress(Client.id) as regAddress', tableD['number'].name(),
                  tableD['date'].name(), tableD['origin'].name(), tableD['serial'].name(), tableD['documentType_id'].name()]
        relationRecord = db.getRecordEx(queryTable, fields, cond, order='ClientDocument.id DESC')
        if relationRecord:
            name = formatShortName(relationRecord.value('lastName'),
                                   relationRecord.value('firstName'),
                                   relationRecord.value('patrName'))
            item = [name,
                            forceString(relationRecord.value('birthDate')),
                            forceString(relationRecord.value('relationType')),
                            relationRecord, None]
            self.items.append(item)


    def addPatronItem(self, db, tableCR, colRelative, colFields, cond):
        tableRT = db.table('rbRelationType')
        tableC  = db.table('Client')
        tableD = db.table('ClientDocument')
        queryTable = tableCR
        queryTable = queryTable.leftJoin(tableRT, tableRT['id'].eq(tableCR['relativeType_id']))
        queryTable = queryTable.leftJoin(tableC, tableC['id'].eq(tableCR[colRelative]))
        queryTable = queryTable.leftJoin(tableD, tableD['client_id'].eq(tableC['id']))
        cond.append(tableC['deleted'].eq(0))
        cond.append(tableD['deleted'].eq(0))
        fields = ['CONCAT_WS(\' | \', rbRelationType.`code`, CONCAT_WS(\'->\', rbRelationType.`leftName`, rbRelationType.`rightName`)) AS relationType',
                  tableC['lastName'].alias(), tableC['firstName'].name(),
                  tableC['patrName'].name(), tableC['birthDate'].name(),
                  'getClientRegAddress(Client.id) as regAddress', tableD['number'].name(),
                  tableD['date'].name(), tableD['origin'].name(), tableD['serial'].name(), tableD['documentType_id'].name(),
                  tableC['id'].alias(colFields)]
        clientRelationRecordList = db.getRecordList(queryTable, fields, cond)
        for relationRecord in clientRelationRecordList:
            name = formatShortName(relationRecord.value('lastName'),
                                   relationRecord.value('firstName'),
                                   relationRecord.value('patrName'))
            item = [name,
                            forceString(relationRecord.value('birthDate')),
                            forceString(relationRecord.value('relationType')),
                            relationRecord, None]
            self.items.append(item)
            self.count += 1
