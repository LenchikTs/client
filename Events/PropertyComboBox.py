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

u'''Свойства Actions'''

from PyQt4 import QtGui
from PyQt4.QtCore import QVariant
from library.ROComboBox import CEnumComboBox
from library.Utils      import forceRef, forceStringEx


class CPropertyComboBox(CEnumComboBox):
    def __init__(self, actionIdList, parent=None):
        CEnumComboBox.__init__(self, parent)
        self._actionIdList = actionIdList


    def addPropertyItem(self, actionIdList):
        self._actionIdList = actionIdList
        if self._actionIdList:
            self.addItem(u'не задано', QVariant(None))
            db = QtGui.qApp.db
            tableAction = db.table('Action')
            tableAP = db.table('ActionProperty')
            tableAPT = db.table('ActionPropertyType')
            tableAPInt = db.table('ActionProperty_Integer')
            tableAPDouble = db.table('ActionProperty_Double')
            queryTable = tableAction.innerJoin(tableAP, tableAP['action_id'].eq(tableAction['id']))
            queryTable = queryTable.innerJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
            queryTable = queryTable.leftJoin(tableAPInt, tableAPInt['id'].eq(tableAP['id']))
            queryTable = queryTable.leftJoin(tableAPDouble, tableAPDouble['id'].eq(tableAP['id']))
            cond = [tableAction['id'].inlist(self._actionIdList),
                    tableAction['deleted'].eq(0),
                    tableAP['deleted'].eq(0),
                    tableAPT['deleted'].eq(0),
                    tableAction['endDate'].isNotNull(),
                    db.joinOr([tableAPInt['value'].isNotNull(), tableAPDouble['value'].isNotNull()])
                    ]
            cols = [tableAPT['id'].alias('propertyTypeId'),
                    tableAPT['name'].alias('propertyTypeName')
                    ]
            records = db.getRecordListGroupBy(queryTable, cols, cond, group=u'propertyTypeId, propertyTypeName', order=u'ActionPropertyType.name')
            for record in records:
                itemText = forceStringEx(record.value('propertyTypeName'))
                propertyTypeId = forceRef(record.value('propertyTypeId'))
                self.addItem(itemText, QVariant(propertyTypeId))
        else:
            self.clear()


    def getActionIdList(self):
        return self._actionIdList

