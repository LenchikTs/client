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

from PyQt4.QtCore import QVariant, QDateTime, QTime

from library.PrintInfo       import CTimeInfo
from library.Utils           import forceString
from library.DateTimeEdit    import CDateTimeEdit
from ActionPropertyValueType import CActionPropertyValueType


class CTimeActionPropertyValueType(CActionPropertyValueType):
    name         = 'Time'
    variantType  = QVariant.Time

    class CPropEditor(CDateTimeEdit):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            CDateTimeEdit.__init__(self, parent)
            self.setMaximumDate(QDateTime(2099,12,31, 23, 59, 59))
            self.setMinimumDate(QDateTime(1900, 1, 1, 0, 0, 0))
            self.setDisplayFormat('HH:mm')
            self.lineEdit.setInputMask('00:00')
            self.canBeEmpty(True)
            self.setStyleSheet("QComboBox::drop-down { image:none}")

        def setValue(self, value):
            v = QDateTime.currentDateTime()
            v.setTime(value.toTime())
            self.setDate(v)

        def value(self):
            return self.date()
        
        def showPopup(self):
            pass

    @staticmethod
    def convertDBValueToPyValue(value):
        if forceString(value) == 'currentTime':
            return QTime.currentTime()
        return value.toTime()


    convertQVariantToPyValue = convertDBValueToPyValue


    def toText(self, v):
        return forceString(v)


    def toInfo(self, context, v):
        return CTimeInfo(v)
