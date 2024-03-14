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

from library.Utils           import forceInt

from ActionPropertyValueType import CActionPropertyValueType


class CPulseActionPropertyValueType(CActionPropertyValueType): #wtf
    name         = 'Pulse'
    variantType  = QVariant.Int

    class CPropEditor(QtGui.QLineEdit):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            QtGui.QLineEdit.__init__(self, parent)
            self._validator = QtGui.QIntValidator(0, 200, self)
            self.setValidator(self._validator)
            self.setMaxLength(3)


        def setValue(self, value):
            v = forceInt(value)
            self.setText(str(v))

        def value(self):
            return self.text().toInt()[0]


    @staticmethod
    def convertDBValueToPyValue(value):
        return value.toInt()[0]


    convertQVariantToPyValue = convertDBValueToPyValue


    def toInfo(self, context, v):
        return v if v else 0

