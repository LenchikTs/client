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

# Свойство типа "число с плавающей точкой"

from PyQt4 import QtGui
from PyQt4.QtCore import QVariant

from library.StrComboBox import CDoubleComboBox
from library.Utils import forceDouble, forceInt

from ActionPropertyValueType import CActionPropertyValueType


class CDoubleActionPropertyValueType(CActionPropertyValueType):
    name = 'Double'
    variantType = QVariant.Double

    class CPropEditor(QtGui.QLineEdit):
        badDomain = u'Неверное описание диапазона свойства Double:\n%(domain)s'
        badKey = u'Недопустимый ключ "%(key)s" в описании диапазона свойства Double:\n%(domain)s'
        badValue = u'Недопустимое значение "%(val)s" ключа "%(key)s" в описании диапазона свойства Double:\n%(domain)s'

        def __init__(self, action, domain, parent, clientId, eventTypeId):
            QtGui.QLineEdit.__init__(self, parent)
            self._validator = QtGui.QDoubleValidator(self)
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
                    if not val.replace('-', '', 1).replace('.', '', 1).isdecimal():
                        raise ValueError, self.badValue % locals()
                    if keylower == u'min':
                        self._validator.setBottom(forceDouble(val))
                    elif keylower == u'max':
                        self._validator.setTop(forceDouble(val))
                    elif keylower == u'dec':
                        self._validator.setDecimals(forceInt(val))
                    else:
                        raise ValueError, self.badKey % locals()
            self._validator.setNotation(QtGui.QDoubleValidator.StandardNotation)

        def setValue(self, value):
            v = forceDouble(value)
            self.setText(str(v))

        def value(self):
            return self.text().toDouble()[0]


    class CComboBoxPropEditor(CDoubleComboBox):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            CDoubleComboBox.__init__(self, parent)
            self.setDomain(domain)

        def setValue(self, value):
            v = forceDouble(value)
            CDoubleComboBox.setValue(self, str(v))

        def value(self):
            return forceDouble(CDoubleComboBox.value(self))

    @staticmethod
    def convertDBValueToPyValue(value):
        res = value.toDouble()
        if not res[1]:
            _str = value.toString()
            _str.replace(',', '.')
            res = QVariant(_str).toDouble()
        return res[0]


    convertQVariantToPyValue = convertDBValueToPyValue


    def toInfo(self, context, v):
        return v if v else 0.0


    def getEditorClass(self):
        if self.domain and all(['min' not in self.domain, 'max' not in self.domain, 'dec' not in self.domain]):
            return self.CComboBoxPropEditor
        else:
            return self.CPropEditor
