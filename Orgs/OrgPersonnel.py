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
from PyQt4.QtCore import Qt, QAbstractItemModel, QModelIndex, QVariant


from library.Utils import forceRef, forceString, formatShortName


class CPersonnelBaseTreeItem(object):
    def __init__(self, parent, name):
        self._parent = parent
        self._idList = []
        self._name   = name
        self._items  = []


    def addId(self, id):
        self._idList.append(id)
        if self._parent:
            self._parent.addId(id)


    def name(self):
        return self._name


    def child(self, row):
        return self._items[row]


    def childCount(self):
        return len(self._items)


    def columnCount(self):
        return 1


    def data(self, column):
        if column == 0:
            return QVariant(self._name)
        else:
            return QVariant()


    def flags(self):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable


    def parent(self):
        return self._parent


    def row(self):
        if self._parent:
            return self._parent._items.index(self)
        return 0


class CPersonnelTreeItem(CPersonnelBaseTreeItem):
    def __init__(self, parent, personId, name):
        CPersonnelBaseTreeItem.__init__(self, parent, name)
        self.addId(personId)


    def childCount(self):
        return 0


    def findPersonId(self, personId):
        if personId in self._idList:
            return self
        return None


    def findSpecialityId(self, specialityId):
        return None



class CPersonnelTreeSpecialityItem(CPersonnelBaseTreeItem):
    def __init__(self, parent, specialityId, name):
        CPersonnelBaseTreeItem.__init__(self, parent, name)
        self._specialityId = specialityId

    def findPersonId(self, personId):
        if personId in self._idList:
            for item in self._items:
                result = item.findPersonId(personId)
                if result:
                    return result
        return None


    def findSpecialityId(self, specialityId):
        if self._specialityId == specialityId:
            return self
        return None


class CPersonnelRootTreeItem(CPersonnelBaseTreeItem):
    def __init__(self, orgId):
        CPersonnelBaseTreeItem.__init__(self, None, 'all')
        self.orderBySpeciality = True


    def setOrgStructureIdList(self, orgId, orgStructureIdList, date):
        self._items = []
        if orgStructureIdList:
            db = QtGui.qApp.db
            tablePerson = db.table('Person')
            tableSpeciality = db.table('rbSpeciality')
            queryTable = tablePerson.leftJoin(tableSpeciality, tableSpeciality['id'].eq(tablePerson['speciality_id']))

            colSpecialityName = tableSpeciality['name']
            colSpecialityId   = tablePerson['speciality_id']
            colLastName       = tablePerson['lastName']
            colFirstName      = tablePerson['firstName']
            colPatrName       = tablePerson['patrName']
            colPersonId       = tablePerson['id']

            cols = [colSpecialityName,
                    colSpecialityId,
                    colLastName,
                    colFirstName,
                    colPatrName,
                    colPersonId,
                   ]
            if self.orderBySpeciality:
                order = [col.name() for col in colSpecialityName,
                                               colSpecialityId,
                                               colLastName,
                                               colFirstName,
                                               colPatrName,
                                               colPersonId,
                        ]
            else:
                order = [col.name() for col in colLastName,
                                               colFirstName,
                                               colPatrName,
                                               colSpecialityName,
                                               colSpecialityId,
                                               colPersonId,
                        ]
            cond = [tablePerson['org_id'].eq(orgId),
                    tablePerson['orgStructure_id'].inlist(orgStructureIdList),
                    tablePerson['deleted'].eq(0),
                    colSpecialityId.isNotNull(),
                    tablePerson['isHideQueue'].eq(0),
                   ]
            if date:
                cond.append(db.joinOr([tablePerson['retireDate'].isNull(), db.joinAnd([tablePerson['retireDate'].monthGe(date), tablePerson['retireDate'].yearGe(date)])]))
            records = db.getRecordList(queryTable, cols, cond, order)
            self.setItemsByRecords(records)


    def setActivityIdList(self, orgId, activityIdList, date):
        self._items = []
        if activityIdList:
            db = QtGui.qApp.db
            tablePersonActivity = db.table('Person_Activity')
            tablePerson = db.table('Person')
            tableSpeciality = db.table('rbSpeciality')
            queryTable = tablePerson.leftJoin(tableSpeciality, tableSpeciality['id'].eq(tablePerson['speciality_id']))
            queryTable = queryTable.leftJoin(tablePersonActivity, tablePersonActivity['master_id'].eq(tablePerson['id']))

            colSpecialityName = tableSpeciality['name']
            colSpecialityId   = tablePerson['speciality_id']
            colLastName       = tablePerson['lastName']
            colFirstName      = tablePerson['firstName']
            colPatrName       = tablePerson['patrName']
            colPersonId       = tablePerson['id']

            cols = [colSpecialityName,
                    colSpecialityId,
                    colLastName,
                    colFirstName,
                    colPatrName,
                    colPersonId,
                   ]
            if self.orderBySpeciality:
                order = [col.name() for col in colSpecialityName,
                                               colSpecialityId,
                                               colLastName,
                                               colFirstName,
                                               colPatrName,
                                               colPersonId,
                        ]
            else:
                order = [col.name() for col in colLastName,
                                               colFirstName,
                                               colPatrName,
                                               colSpecialityName,
                                               colSpecialityId,
                                               colPersonId,
                        ]
            cond = [tablePerson['org_id'].eq(orgId),
                    tablePersonActivity['activity_id'].inlist(activityIdList),
                    colSpecialityId.isNotNull(),
                   ]
            if date:
                cond.append(db.joinOr([tablePerson['retireDate'].isNull(), db.joinAnd([tablePerson['retireDate'].monthGe(date), tablePerson['retireDate'].yearGe(date)])]))
            records = db.getRecordList(queryTable, cols, cond, order)
            self.setItemsByRecords(records)


    def setItemsByRecords(self, records):
        specialityItem = None
        for record in records:
            specialityId   = forceRef(record.value('speciality_id'))
            specialityName = forceString(record.value('name'))
            personId  = forceRef(record.value('id'))
            personName = formatShortName(record.value('lastName'),
                                         record.value('firstName'),
                                         record.value('patrName'))
            if not specialityItem or specialityItem._specialityId != specialityId:
                specialityItem = CPersonnelTreeSpecialityItem(self, specialityId, specialityName)
                self._items.append(specialityItem)
            specialityItem._items.append(CPersonnelTreeItem(specialityItem, personId, personName))


    def findPersonId(self, personId):
        for item in self._items:
            result = item.findPersonId(personId)
            if result:
                return result
        return None


    def findSpecialityId(self, specialityId):
        for item in self._items:
            result = item.findSpecialityId(specialityId)
            if result:
                return result
        return None


class COrgPersonnelModel(QAbstractItemModel):
    def __init__(self, orgStructureIdList, parent=None):
        QAbstractItemModel.__init__(self, parent)
        self._rootItem = CPersonnelRootTreeItem(orgStructureIdList)

    def getRootItem(self):
        return self._rootItem

    def setOrgStructureIdList(self, orgId, orgStructureIdList, date):
        self.getRootItem().setOrgStructureIdList(orgId, orgStructureIdList, date)
        self.reset()


    def setActivityIdList(self, orgId, activityIdList, date):
        self.getRootItem().setActivityIdList(orgId, activityIdList, date)
        self.reset()


    def columnCount(self, parent=None):
        return 1


    def data(self, index, role):
        if not index.isValid():
            return QVariant()

        if role != Qt.DisplayRole:
            return QVariant()

        item = index.internalPointer()
        return item.data(index.column())


    def flags(self, index):
        if not index.isValid():
            return 0
        item = index.internalPointer()
        return item.flags()


    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            return QVariant(u'Персонал')
        return QVariant()


    def index(self, row, column, parent):
        if not parent.isValid():
            parentItem = self.getRootItem()
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()


#    def rootIndex(self):
#        return self.createIndex(0, 0, self.getRootItem())


    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.getRootItem() or parentItem is None:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)


    def rowCount(self, parent):
        if parent and parent.isValid():
            parentItem = parent.internalPointer()
        else:
            parentItem = self.getRootItem()
        return parentItem.childCount()


    def findPersonId(self, personId):
        item = self.getRootItem().findPersonId(personId)
        if item:
            return self.createIndex(item.row(), 0, item)
        else:
            return None


    def findSpecialityId(self, specialityId):
        item = self.getRootItem().findSpecialityId(specialityId)
        if item:
            return self.createIndex(item.row(), 0, item)
        else:
            return None


    def getItemIdList(self, index):
        item = index.internalPointer()
        if item:
            return item._idList
        else:
            return []


    def getFirstLeafIndex(self):
        result = QModelIndex()
        while self.rowCount(result):
            result = self.index(0, 0, result)
        return result

# #######################################################################

class CFlatPersonnelRootTreeItem(CPersonnelRootTreeItem):
    def __init__(self, orgId):
        CPersonnelRootTreeItem.__init__(self, orgId)
        self.orderBySpeciality = False


    def setItemsByRecords(self, records):
#        specialityItem = None
        for record in records:
            personId  = forceRef(record.value('id'))
            personName = formatShortName(record.value('lastName'),
                                         record.value('firstName'),
                                         record.value('patrName'))
            self._items.append(CPersonnelTreeItem(self, personId, personName))


class CFlatOrgPersonnelModel(COrgPersonnelModel):
    def __init__(self, orgStructureIdList, parent=None):
        COrgPersonnelModel.__init__(self, orgStructureIdList, parent)
        self._rootItem = CFlatPersonnelRootTreeItem(orgStructureIdList)

