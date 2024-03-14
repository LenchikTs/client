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
from PyQt4.QtCore import Qt

class CDocSerialEdit(QtGui.QLineEdit):
    def __init__(self, parent=None):
        QtGui.QLineEdit.__init__(self, parent)
        self.format = 0


    def setFormat(self, format):
        self.format = format
        text = unicode(self.text())
        text = ''.join(self.filterChar(char) for char in text)
        self.setText(text)


    def keyPressEvent(self, event):
        if self.format                                          \
           and Qt.Key_Space <= event.key() < Qt.Key_Escape      \
           and len(unicode(event.text())) == 1:
            chars = self.filterChar(unicode(event.text()))
            if chars:
                for char in chars:
                    myEvent = QtGui.QKeyEvent(event.type(), ord(char), event.modifiers(), char, False, 1)
                    QtGui.QLineEdit.keyPressEvent(self, myEvent)
            event.accept()
        else:
            QtGui.QLineEdit.keyPressEvent(self, event)


class CDocSerialLeftEdit(CDocSerialEdit):
    anyToRoman = { '1': 'I',  'i': 'I',  'I': 'I', u'ш': 'I', u'Ш': 'I',
                   '2': 'II',
                   '3': 'III',
                   '4': 'IV',
                   '5': 'V',  'v': 'V',  'V': 'V', u'м': 'V', u'М': 'V',
                   '6': 'VI',
                   '7': 'VII',
                   '8': 'VIII',
                   '9': 'IX',
                   '0': 'X',  'x': 'X',  'X': 'X', u'ч': 'X', u'Ч': 'X',
                              'l': 'L',  'L': 'L', u'д': 'L', u'Д': 'L',
                              'c': 'C',  'C': 'C', u'с': 'C', u'С': 'C',
                              'd': 'D',  'D': 'D', u'в': 'D', u'В': 'D',
                              'm': 'M',  'M': 'M', u'ь': 'M', u'Ь': 'M'
                 }

    def __init__(self, parent=None):
        CDocSerialEdit.__init__(self, parent)


    def filterChar(self, char):
        if self.format == 1:
            if char.isalpha() or 0x20 <= ord(char) <= 0xFF:
               return self.anyToRoman.get(char, '')
            else:
                return char
        if self.format == 2:
            if char.isdigit():
                return char
            else:
                return ''
        return char


class CDocSerialRightEdit(CDocSerialEdit):
    def __init__(self, parent=None):
        CDocSerialEdit.__init__(self, parent)


    def filterChar(self, char):
        if self.format == 1:
            if char.isalpha():
                return char.upper()
            else:
                return ''
        if self.format == 2:
            if char.isdigit():
                return char
            else:
                return ''
        return char
