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

from library.CRBSearchComboBox import CRBSearchComboBox
from library.PrintInfo       import CInfo, CRBInfo
from library.crbcombobox     import CRBComboBox
from library.Utils           import forceRef, forceString, trim

from ActionPropertyValueType import CActionPropertyValueType


class CReferenceActionPropertyValueType(CActionPropertyValueType):
    name         = 'Reference'
    variantType  = QVariant.Int

    def __init__(self, domain = None):
        domainList = domain.split(u';') # engl
        if len(domainList) != 3:
            domainList = domain.split(u';')  # rus
        if len(domainList) == 3:
            domain = trim(domainList[0])
        CActionPropertyValueType.__init__(self, domain)


    class CRBInfoEx(CRBInfo): #wtf
        def __init__(self, context, tableName, id):
            CInfo.__init__(self, context)
            self.id = id
            self.tableName = tableName


    class CPropEditor(CRBSearchComboBox):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            CRBSearchComboBox.__init__(self, parent)
            self.initializeEditor(action, domain)


        def initializeEditor(self, action, domain):
            if action and domain:
                domainList = domain.split(u';') # engl
                if len(domainList) != 3:
                    domainList = domain.split(u';') # rus
                if len(domainList) == 3:
                    tableName = trim(domainList[0])
                    fieldName = trim(domainList[1])
                    propertyName = trim(domainList[2])
                    valueId = action[propertyName] if (propertyName in action._actionType._propertiesByName) else None
                    if valueId:
                        self.setTable(tableName, filter = u'%s = %s'%(fieldName, forceString(valueId)))
                        return
            self.setTable(domain)


        def setValue(self, value):
            CRBSearchComboBox.setValue(self, forceRef(value))


    @staticmethod
    def convertDBValueToPyValue(value):
        return forceRef(value)


    convertQVariantToPyValue = convertDBValueToPyValue


    def toText(self, v):
        return forceString(QtGui.qApp.db.translate(self.domain, 'id', v, 'CONCAT(code,\' | \',name)'))


    def toInfo(self, context, v):
        return CReferenceActionPropertyValueType.CRBInfoEx(context, self.domain, v)


    def getTableName(self):
        return self.tableNamePrefix+self.domain

