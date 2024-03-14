# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2022 SAMSON Group. All rights reserved.
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

from library.crbcombobox     import CRBComboBox
from library.Utils           import forceRef, forceStringEx
from ActionPropertyValueType import CActionPropertyValueType
from Stock.StockMotionInfo   import CNomenclatureUsingTypeInfo


class CNomenclatureUsingTypeActionPropertyValueType(CActionPropertyValueType):
    variantType  = QVariant.Int
    name         = u'Способ применения ЛСиИМН'
    cacheText = True

    class CPropEditor(CRBComboBox):
        def __init__(self, action, domain, parent, clientId, eventTypeId, eventEditor=None):
            CRBComboBox.__init__(self, parent)
            usingTypeIdList = []
            self.action = action
            if self.action:
                db = QtGui.qApp.db
                table = db.table('rbNomenclature_UsingType')
                propertyList = self.action.getProperties()
                for actionProperty in propertyList:
                    propertyType = actionProperty.type()
                    if propertyType.isNomenclatureValueType():
                        property = self.action.getPropertyById(propertyType.id)
                        nomenclatureId = property.getValue()
                        if nomenclatureId:
                            usingTypeIdList = db.getDistinctIdList(table, table['usingType_id'].name(), [table['master_id'].eq(nomenclatureId)], order = table['idx'].name())
            if usingTypeIdList:
                filter = 'rbNomenclatureUsingType.id IN (%s)'%(u','.join(str(usingTypeId) for usingTypeId in usingTypeIdList if usingTypeId))
            else:
                filter = u''
            self.setTable('rbNomenclatureUsingType', addNone=True, filter=filter)


        def setValue(self, value):
            if forceRef(value):
                CRBComboBox.setValue(self, forceRef(value))


    @staticmethod
    def convertDBValueToPyValue(value):
        return forceRef(value)


    convertQVariantToPyValue = convertDBValueToPyValue


    def toText(self, usingTypeId):
        if not usingTypeId:
            return ''
        result = u''
        db = QtGui.qApp.db
        table = db.table('rbNomenclatureUsingType')
        if usingTypeId:
            record = db.getRecordEx(table, [table['name']], [table['id'].eq(usingTypeId)])
            if record:
                result = forceStringEx(record.value('name'))
        return result


    def toInfo(self, context, v):
        return context.getInstance(CNomenclatureUsingTypeInfo, forceRef(v))


    @classmethod
    def getTableName(cls):
        return cls.tableNamePrefix+'rbNomenclatureUsingType'
