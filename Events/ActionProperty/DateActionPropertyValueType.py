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

from PyQt4.QtCore import QDate, QVariant

from library.DateEdit      import CDateEdit
from library.PrintInfo     import CDateInfo
from library.Utils         import forceString

from ActionPropertyValueType       import CActionPropertyValueType


class CDateActionPropertyValueType(CActionPropertyValueType):
    name         = 'Date'
    variantType  = QVariant.Date

    class CPropEditor(CDateEdit):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            CDateEdit.__init__(self, parent)

        def setValue(self, value):
            v = value.toDate()
            self.setDate(v)

        def value(self):
            return self.date()


    @staticmethod
    def convertDBValueToPyValue(value):
        v = forceString(value)
        if v == 'currentDate':
            return QDate.currentDate()
        elif v == 'nextDate':
            return QDate.currentDate().addDays(1)
        return value.toDate()


    convertQVariantToPyValue = convertDBValueToPyValue


    def toText(self, v):
        return forceString(v)


    def toInfo(self, context, v):
        return CDateInfo(v)
#

