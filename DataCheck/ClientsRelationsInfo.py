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
from PyQt4.QtCore import Qt, QDate, QVariant, pyqtSignature

from library.DialogBase         import CDialogBase
from library.RecordLock         import CRecordLockMixin
from library.database           import CTableRecordCache
from library.Utils              import forceRef, toVariant
from library.TableModel         import CTableModel, CTextCol
from Registry.Utils             import getClientString
from Registry.ClientRelationComboBoxPopupEx import CClientRelationTableModel

from DataCheck.Ui_ClientsRelationsInfoDialog   import Ui_ClientsRelationsInfoDialog


class CClientsRelationsInfo(CDialogBase, CRecordLockMixin, Ui_ClientsRelationsInfoDialog):
    def __init__(self,  parent):
        CDialogBase.__init__(self, parent)
        CRecordLockMixin.__init__(self)
        self.addModels('Clients', CClientsTableModel(self))
        self.addModels('Relations', CClientRelationTableModel(self))
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setWindowTitleEx(u'Информация о пациентах')
        self.setWindowState(Qt.WindowMaximized)
        self.grpRelations.setStyleSheet("QGroupBox {font-weight: bold;}")
        self.setModels(self.tblClients, self.modelClients, self.selectionModelClients)
        self.setModels(self.tblRelations, self.modelRelations, self.selectionModelRelations)
        self.showMaximized()


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelClients_currentRowChanged(self, current, previous):
        self.updateRelations(self.tblClients.currentItemId())


    def getClientRelationIdList(self, clientId):
        idList = [clientId]
        db = QtGui.qApp.db
        tableClient = db.table('Client')
        tableDocument = db.table('ClientDocument')
        tableAddress = db.table('ClientAddress')
        tableDocumentType = db.table('rbDocumentType')
        tableCRR = db.table('ClientRelation').alias('CRR')
        tableCRC = db.table('ClientRelation').alias('CRC')
        queryTable = tableClient.leftJoin(tableCRR, db.joinAnd([tableCRR['relative_id'].eq(tableClient['id']), tableCRR['deleted'].eq(0)]))
        queryTable = queryTable.leftJoin(tableCRC, db.joinAnd([tableCRC['client_id'].eq(tableClient['id']), tableCRC['deleted'].eq(0)]))
        queryTable = queryTable.leftJoin(tableAddress, db.joinAnd([tableClient['id'].eq(tableAddress['client_id']), tableAddress['deleted'].eq(0)]))
        queryTable = queryTable.leftJoin(tableDocument, db.joinAnd([tableClient['id'].eq(tableDocument['client_id']), tableDocument['deleted'].eq(0)]))
        queryTable = queryTable.leftJoin(tableDocumentType, tableDocument['documentType_id'].eq(tableDocumentType['id']))
        cond = [tableClient['deleted'].eq(0)
                ]
        orderList = ['Client.lastName', 'Client.firstName', 'Client.patrName']
        if clientId:
           cond.append(tableClient['id'].eq(clientId))
        orderStr = ', '.join([fieldName for fieldName in orderList])
        cols = [u'DISTINCT Client.id AS clientId',
                tableCRR['client_id'].alias('cRRClientId'),
                tableCRC['relative_id'].alias('relativeId')
                ]
        records = db.getRecordList(queryTable, cols,
                              where=cond,
                              order=orderStr)
        for record in records:
            clientId = forceRef(record.value('id'))
            if clientId and clientId not in idList:
                idList.append(clientId)
            cRRClientId = forceRef(record.value('cRRClientId'))
            if cRRClientId and cRRClientId not in idList:
                idList.append(cRRClientId)
            relativeId = forceRef(record.value('relativeId'))
            if relativeId and relativeId not in idList:
                idList.append(relativeId)
        if idList:
            queryTable = tableClient.leftJoin(tableAddress, db.joinAnd([tableClient['id'].eq(tableAddress['client_id']), tableAddress['deleted'].eq(0)]))
            queryTable = queryTable.leftJoin(tableDocument, db.joinAnd([tableClient['id'].eq(tableDocument['client_id']), tableDocument['deleted'].eq(0)]))
            queryTable = queryTable.leftJoin(tableDocumentType, tableDocument['documentType_id'].eq(tableDocumentType['id']))
            cond = [tableClient['id'].inlist(idList),
                    tableClient['deleted'].eq(0)
                    ]
            idList = db.getDistinctIdList(queryTable, tableClient['id'].name(),
                                          where=cond,
                                          order=orderStr)
        return idList


    def loadData(self, clientIdList):
        if clientIdList:
            self.modelClients.setIdList(clientIdList, 0)
            self.updateRelations(clientIdList[0])


    def updateRelations(self, clientId):
        relationIdList = []
        if clientId:
            relationIdList = self.getClientRelationIdList(clientId)
        self.modelRelations.setIdList(relationIdList, 0)


class CClientsTableModel(CTableModel):
    class CClientInfoCol(CTextCol):
        def __init__(self, title, fields, defaultWidth, alignment='l'):
            CTextCol.__init__(self, title, fields, defaultWidth, alignment)
            self.clientCaches = {}

        def format(self, values):
            clientId = forceRef(values[0])
            if clientId:
                info = self.clientCaches.get(clientId, None)
                if info:
                    return toVariant(info)
                else:
                    info = getClientString(clientId)
                    if info:
                        self.clientCaches[clientId] = info
                        return toVariant(info)
            return QVariant()

        def alignment(self):
            return QVariant(Qt.AlignLeft + Qt.AlignTop)

        def clearClientCaches(self):
            self.clientCaches = {}


    def __init__(self, parent):
        CTableModel.__init__(self, parent)
        self.addColumn(CClientsTableModel.CClientInfoCol(u'Пациент', ['id'], 100))
        self.setTable('Client')
        self.date = QDate.currentDate()


    def flags(self, index):
        return Qt.ItemIsEnabled|Qt.ItemIsSelectable


    def setTable(self, tableName):
        db = QtGui.qApp.db
        tableClient = db.table('Client')
        loadFields = [u'''DISTINCT Client.id''']
        self._table = tableClient
        self._recordsCache = CTableRecordCache(db, self._table, loadFields)
