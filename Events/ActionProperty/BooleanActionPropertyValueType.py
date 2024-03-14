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

#
from PyQt4 import QtGui
from PyQt4.QtCore import QVariant

from library.Utils                 import forceBool
from ActionPropertyValueType       import CActionPropertyValueType

class CBooleanActionPropertyValueType(CActionPropertyValueType):
    name         = 'Boolean'
    variantType  = QVariant.Bool

    class CPropEditor(QtGui.QCheckBox):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            QtGui.QCheckBox.__init__(self, parent)

        def setValue(self, value):
            v = forceBool(value)
            self.setChecked(v)

        def value(self):
            return self.isChecked()


    @staticmethod
    def convertDBValueToPyValue(value):
        return forceBool(value)


    convertQVariantToPyValue = convertDBValueToPyValue


    def getEditorClass(self):
        return self.CPropEditor


