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

# wft?
from PyQt4 import QtGui
#from PyQt4.QtCore import QVariant

from library.StrComboBox import CDoubleComboBox
from library.Utils       import forceDouble

from DoubleActionPropertyValueType import CDoubleActionPropertyValueType


class CDoubleStringActionPropertyValueType(CDoubleActionPropertyValueType):
    class CComboBoxPropEditor(CDoubleComboBox):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            CDoubleComboBox.__init__(self, parent)
            self.setDomain(domain)


        def setValue(self, value):
            v = ("%.10f" %forceDouble(value)).rstrip('0').rstrip('.')
            CDoubleComboBox.setValue(self, v)


        def value(self):
            return CDoubleComboBox.value(self)#.toDouble()[0]


    @staticmethod
    def convertDBValueToPyValue(value):
        return ("%.10f" %forceDouble(value)).rstrip('0').rstrip('.')


    class CPropEditor(QtGui.QLineEdit):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            QtGui.QLineEdit.__init__(self, parent)
            self._validator = QtGui.QDoubleValidator(self)
            self.setValidator(self._validator)


        def setValue(self, value):
            v = ("%.10f" %forceDouble(value)).rstrip('0').rstrip('.')
            self.setText(str(v))


        def value(self):
            return self.text().toDouble()[0]

    convertQVariantToPyValue = convertDBValueToPyValue
