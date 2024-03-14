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

from library.crbcombobox     import CRBComboBox
from library.Utils           import forceRef, forceString

from RefBooks.Finance.Info   import CFinanceInfo
from ActionPropertyValueType import CActionPropertyValueType


class CFinanceActionPropertyValueType(CActionPropertyValueType):
    name         = 'rbFinance'
    variantType  = QVariant.Int


    class CPropEditor(CRBComboBox):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            CRBComboBox.__init__(self, parent)
            self.setTable('rbFinance')

        def setValue(self, value):
            CRBComboBox.setValue(self, forceRef(value))


    @staticmethod
    def convertDBValueToPyValue(value):
        return forceRef(value)


    convertQVariantToPyValue = convertDBValueToPyValue


    def toText(self, v):
        return forceString(QtGui.qApp.db.translate('rbFinance', 'id', v, 'CONCAT(code,\' | \',name)'))


    def toInfo(self, context, v):
        return CFinanceInfo(context, forceRef(v))


    @classmethod
    def getTableName(cls):
        return cls.tableNamePrefix+cls.name

