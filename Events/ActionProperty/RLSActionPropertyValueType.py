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

from library.RLS.RLSComboBox import CRLSComboBox
from library.RLS.RLSInfo     import CRLSInfo

from library.Utils           import forceInt

from ActionPropertyValueType        import CActionPropertyValueType
from IntegerActionPropertyValueType import CIntegerActionPropertyValueType

class CRLSActionPropertyValueType(CActionPropertyValueType):
    name         = 'RLS'
    variantType  = QVariant.Int

    class CPropEditor(CRLSComboBox):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            CRLSComboBox.__init__(self, parent)

        def setValue(self, value):
            v = forceInt(value)
            CRLSComboBox.setValue(self, v)


    @staticmethod
    def convertDBValueToPyValue(value):
        return value.toInt()[0]


    convertQVariantToPyValue = convertDBValueToPyValue


    @classmethod
    def getTableName(cls):
        return cls.tableNamePrefix+CIntegerActionPropertyValueType.name


    def toText(self, v):
        return CRLSComboBox.codeToText(forceInt(v))


    def toInfo(self, context, v):
        return context.getInstance(CRLSInfo, forceInt(v))

