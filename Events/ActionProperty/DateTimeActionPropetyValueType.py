# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2023 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
from PyQt4.QtCore import QVariant, Qt, QDateTime

from ActionPropertyValueType import CActionPropertyValueType
from library.PrintInfo import CDateTimeInfo
from library.Utils import forceString
from library.DateTimeEdit import CDateTimeEdit

class CDateTimeActionPropertyValueType(CActionPropertyValueType):
    name = 'DateTime'
    variantType = QVariant.DateTime
    flagNullStr = False

    class CPropEditor(CDateTimeEdit):
        def __init__(self, action, domain, parent, clientId, eventTypeId, *__args):
            CDateTimeEdit.__init__(self, parent)

        def setValue(self, value):
            v = value.toDateTime()
            self.setDate(v)

        def value(self):
            return self.date()

        def keyPressEvent(self, event):
            if int(event.modifiers()) == Qt.ControlModifier and event.key() == Qt.Key_Delete:
                self.lineEdit().setText('')
                event.accept()
                CDateTimeActionPropertyValueType.flagNullStr = True
            else:
                CDateTimeEdit.keyPressEvent(self, event)
                CDateTimeActionPropertyValueType.flagNullStr = False

    @staticmethod
    def convertDBValueToPyValue(value):
        if forceString(value) == 'currentDateTime':
            return QDateTime.currentDateTime()
        return value.toDateTime()

    convertQVariantToPyValue = convertDBValueToPyValue

    def toText(self, v):
        return forceString(v)

    def toInfo(self, context, v):
        return CDateTimeInfo(v)
