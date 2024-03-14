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
from PyQt4.QtCore import QVariant

from library.PrintInfo       import CInfo, CRBInfo
from library.crbcombobox     import CRBComboBox
from library.Utils           import forceRef, forceInt, forceString

from ActionPropertyValueType import CActionPropertyValueType


class COrgStructurePlacementActionPropertyValueType(CActionPropertyValueType):
    name         = 'OrgStructurePlacements'
    variantType  = QVariant.Int


    class CRBInfoEx(CRBInfo): #wtf
        def __init__(self, context, tableName, id):
            CInfo.__init__(self, context)
            self.id = id
            self.tableName = tableName


    class CPropEditor(CRBComboBox):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            CRBComboBox.__init__(self, parent)
            db = QtGui.qApp.db
            if u'moving' in action._actionType.flatCode.lower():
                orgStructureId = action[u'Отделение пребывания'] if u'Отделение пребывания' in action._actionType._propertiesByName else None
            if orgStructureId:
                orgStructureIdList = db.getDescendants('OrgStructure', 'parent_id', orgStructureId)
            if orgStructureIdList:
                table = db.table('OrgStructure_Placement')
                filter = table['master_id'].inlist(orgStructureIdList)
            else:
                filter = ''
            self.setTable('OrgStructure_Placement', True, filter)
            self.domain = domain

        def setValue(self, value):
            CRBComboBox.setValue(self, forceRef(value))


    @staticmethod
    def convertDBValueToPyValue(value):
        return forceRef(value)


    convertQVariantToPyValue = convertDBValueToPyValue


    def toInfo(self, context, v):
        return COrgStructurePlacementActionPropertyValueType.CRBInfoEx(context, 'OrgStructure_Placement', v)


    def toText(self, v):
        return forceString(QtGui.qApp.db.translate('OrgStructure_Placement', 'id', v, 'name'))


    @classmethod
    def getTableName(cls):
        return cls.tableNamePrefix+'OrgStructure_Placement'