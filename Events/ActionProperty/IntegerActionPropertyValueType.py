# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

# Свойство типа "целое число"

from PyQt4 import QtGui
from PyQt4.QtCore import QVariant


from library.StrComboBox import CIntComboBox
from library.Utils import forceInt

from ActionPropertyValueType import CActionPropertyValueType


class CIntegerActionPropertyValueType(CActionPropertyValueType):
    name = 'Integer'
    variantType = QVariant.Int

    class CPropEditor(QtGui.QLineEdit):
        badDomain = u'Неверное описание диапазона свойства Integer:\n%(domain)s'
        badKey = u'Недопустимый ключ "%(key)s" в описании диапазона свойства Integer:\n%(domain)s'
        badValue = u'Недопустимое значение "%(val)s" ключа "%(key)s" в описании диапазона свойства Integer:\n%(domain)s'

        def __init__(self, action, domain, parent, clientId, eventTypeId):
            QtGui.QLineEdit.__init__(self, parent)
            self._validator = QtGui.QIntValidator(self)
            self.parseDomain(domain)
            self.setValidator(self._validator)

        def parseDomain(self, domain):
            for word in domain.split(';'):
                if word:
                    parts = word.split(':')
                    if len(parts) == 2:
                        key, val = parts[0].strip(), parts[1].strip()
                    else:
                        raise ValueError, self.badDomain % locals()
                    keylower = key.lower()
                    if not val.replace('-', '', 1).isdecimal():
                        raise ValueError, self.badValue % locals()
                    if keylower == u'min':
                        self._validator.setBottom(forceInt(val))
                    elif keylower == u'max':
                        self._validator.setTop(forceInt(val))
                    else:
                        raise ValueError, self.badKey % locals()

        def setValue(self, value):
            v = forceInt(value)
            self.setText(str(v))

        def value(self):
            return self.text().toInt()[0]


    class CComboBoxPropEditor(CIntComboBox):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            CIntComboBox.__init__(self, parent)
            self.setDomain(domain)

        def setValue(self, value):
            v = forceInt(value)
            CIntComboBox.setValue(self, str(v))

        def value(self):
            return forceInt(CIntComboBox.value(self))


    def getEditorClass(self):
        if self.domain and all(['min' not in self.domain, 'max' not in self.domain]):
            return self.CComboBoxPropEditor
        else:
            return self.CPropEditor


    @staticmethod
    def convertDBValueToPyValue(value):
        return forceInt(value)


    convertQVariantToPyValue = convertDBValueToPyValue


    def toInfo(self, context, v):
        return v if v else 0
