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


from PyQt4.QtCore import QVariant
from PyQt4 import QtGui

from library.crbcombobox     import CRBComboBox
from library.PrintInfo       import CRBInfo
from library.Utils           import forceString, forceRef, forceDate

from ActionPropertyValueType import CActionPropertyValueType


class CEventCSGComboBox(CRBComboBox):
    def __init__(self, parent):
        CRBComboBox.__init__(self, parent)


class CCsgActionPropertyValueType(CActionPropertyValueType):
    name         = u'КСГ'
    variantType  = QVariant.String


    class CCsgInfo(CRBInfo):
        tableName = 'mes.CSG'


    class CPropEditor(QtGui.QComboBox):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            QtGui.QComboBox.__init__(self, parent)
            eventId = forceRef(action._record.value('event_id'))
            #self.setTable('Event_CSG', filter=filter)
            db = QtGui.qApp.CSGModelDB if hasattr(QtGui.qApp, 'CSGModelDB') else QtGui.qApp.db
            table = db.table('Event_CSG')
            if eventId:
                cond = [db.joinOr([table['master_id'].eq(eventId), table['master_id'].isNull()])]
            else:
                cond = [table['master_id'].isNull()]
            cond.append(table['CSGCode'].ne(''))
            recordList = db.getRecordList(table, '*', cond)
            self.mapIndexToId = {}
            self.mapIdToIndex = {}
            index = 0
            for record in recordList:
                csgCode = forceString(record.value('CSGCode'))
                csgEndDate = forceDate(record.value('endDate'))
                id = forceRef(record.value('id'))
                self.mapIndexToId[index] = id
                self.mapIdToIndex[id] = index
                index += 1
                code = '%s - %s'%(csgCode, forceString(csgEndDate)) if csgEndDate else csgCode
                self.addItem(code)


        def value(self):
            return self.mapIndexToId.get(self.currentIndex(), None)


        def setValue(self, value):
            self.setCurrentIndex(self.mapIdToIndex.get(forceRef(value), 0))


    @staticmethod
    def convertDBValueToPyValue(value):
        return forceString(value)


    convertQVariantToPyValue = convertDBValueToPyValue


    def toInfo(self, context, v):
        return CCsgActionPropertyValueType.CCsgInfo(context, v)


    def toText(self, value):
        db = QtGui.qApp.CSGModelDB if hasattr(QtGui.qApp, 'CSGModelDB') else QtGui.qApp.db
        table = db.table('Event_CSG')
        cols = [table['CSGCode'], table['endDate']]
        record = db.getRecord(table, cols, value)
        if record:
            csgCode = forceString(record.value(0))
            endDate = forceDate(record.value(1))
            return forceString('%s - %s'%(csgCode, forceString(endDate))) if endDate else csgCode
        return ''


    @classmethod
    def getTableName(cls):
        return cls.tableNamePrefix+'CSG'


