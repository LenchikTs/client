# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2020 SAMSON Group. All rights reserved.
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

from RefBooks.NomenclatureActiveSubstance.ActiveSubstanceComboBox import CActiveSubstanceComboBox
from RefBooks.NomenclatureActiveSubstance.Info import CNomenclatureActiveSubstanceInfo
from library.Utils           import forceRef, forceStringEx
from ActionPropertyValueType import CActionPropertyValueType


class CNomenclatureActiveSubstanceActionPropertyValueType(CActionPropertyValueType):
    variantType  = QVariant.Int
    name         = u'Действующее вещество ЛСиИМН'
    cacheText = True

    class CPropEditor(CActiveSubstanceComboBox):
        def __init__(self, action, domain, parent, clientId, eventTypeId, eventEditor=None):
            CActiveSubstanceComboBox.__init__(self, parent)
            self.action = action
            if self.action:
                propertyList = self.action.getProperties()
                for actionProperty in propertyList:
                    propertyType = actionProperty.type()
                    if propertyType.isNomenclatureValueType():
                        property = self.action.getPropertyById(propertyType.id)
                        self.setNomenclatureId(property.getValue())
                        break


        def setValue(self, value):
            if forceRef(value):
                CActiveSubstanceComboBox.setValue(self, forceRef(value))


    @staticmethod
    def convertDBValueToPyValue(value):
        return forceRef(value)


    convertQVariantToPyValue = convertDBValueToPyValue


    def toText(self, activeSubstanceId):
        if not activeSubstanceId:
            return ''
        result = u''
        db = QtGui.qApp.db
        table = db.table('rbNomenclatureActiveSubstance')
        if activeSubstanceId:
            record = db.getRecordEx(table, [table['name'], table['mnnLatin']], [table['id'].eq(activeSubstanceId)])
            if record:
                result = forceStringEx(record.value('name'))
                if not result:
                    result = forceStringEx(record.value('mnnLatin'))
        return result


    def toInfo(self, context, v):
        return context.getInstance(CNomenclatureActiveSubstanceInfo, forceRef(v))


    @classmethod
    def getTableName(cls):
        return cls.tableNamePrefix+'rbNomenclatureActiveSubstance'

