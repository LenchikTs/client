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

from Orgs.ContractFindComboBox import CARMSContractTreeFindComboBox
from library.Utils             import forceRef, forceString
from ActionPropertyValueType   import CActionPropertyValueType


class CContractActionPropertyValueType(CActionPropertyValueType):
    name         = 'Contract'
    variantType  = QVariant.Int
    isCopyable   = False

    class CPropEditor(CARMSContractTreeFindComboBox):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            filter = {}
            financeId = action[u'Источник финансирования'] if u'Источник финансирования' in action._actionType._propertiesByName else None
            if financeId:
                filter['financeId'] = financeId
            CARMSContractTreeFindComboBox.__init__(self, parent, filter)


        def setValue(self, value):
            CARMSContractTreeFindComboBox.setValue(self, forceRef(value))


    @staticmethod
    def convertDBValueToPyValue(value):
        return forceRef(value)


    convertQVariantToPyValue = convertDBValueToPyValue


    def toText(self, v):
        if v:
            names = ['number', 'date', 'resolution']
            record = QtGui.qApp.db.getRecord('Contract', ['number', 'date', 'resolution'], v)
            return ' '.join([forceString(record.value(name)) for name in names])
        return ''


    def toInfo(self, context, v):
        from Events.EventInfo import CContractInfo
        return context.getInstance(CContractInfo, forceRef(v))

