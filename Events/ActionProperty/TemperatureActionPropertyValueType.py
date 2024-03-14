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

from library.Utils         import forceDouble

from ActionPropertyValueType       import CActionPropertyValueType


class CTemperatureActionPropertyValueType(CActionPropertyValueType):
    name         = 'Temperature'
    variantType  = QVariant.Double

    class CPropEditor(QtGui.QLineEdit):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            QtGui.QLineEdit.__init__(self, parent)
            self._validator = QtGui.QDoubleValidator(self)
            self.setValidator(self._validator)
            self.setMaxLength(4)
            self.validator().setTop(99.9)
            self.setInputMask('00.0')

        def setValue(self, value):
            v = forceDouble(value)
            self.setText(str(v))

        def value(self):
            return self.text().toDouble()[0]


    @staticmethod
    def convertDBValueToPyValue(value):
        return value.toDouble()[0]


    convertQVariantToPyValue = convertDBValueToPyValue


    def toInfo(self, context, v):
        return v if v else 0.0

