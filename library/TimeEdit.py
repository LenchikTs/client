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
from PyQt4.QtCore import SIGNAL, QTime

from library.Utils import trim


class CTimeRangeValidator(QtGui.QValidator):
     def validate(self, input, pos):
        #times = self.text().split('-')
        return  1


class CTimeRangeEdit(QtGui.QLineEdit):
    validator = None

    def __init__(self, parent=None):
        QtGui.QLineEdit.__init__(self, parent)
        self.setInputMask('09:99 - 09:99')
#        self.setValidator(self.getRangeValidator())

    def getValidator(self):
        if not CTimeRangeEdit.validator:
            CTimeRangeEdit.validator = CTimeRangeValidator()
        return CTimeRangeEdit.validator


    def setTimeRange(self, range):
        if range:
            start, finish = range
            self.setText(start.toString('HH:mm')+' - ' +finish.toString('HH:mm'))
        else:
            self.setText('')
        self.setCursorPosition(0)


    def timeRange(self):
        times = self.text().split('-')
        if len(times) == 2:
            start = stringToTime(times[0])
            finish = stringToTime(times[1])
            if start.isValid() and finish.isValid():
                return start, finish
        return None



#class CTimeEdit(QtGui.QLineEdit):
#    validator = None
#
#    def __init__(self, parent=None):
#        QtGui.QLineEdit.__init__(self, parent)
#        self.setInputMask('09:99')
##        self.setValidator(self.getRangeValidator())
#
#    def getValidator(self):
#        if not CTimeEdit.validator:
#            CTimeEdit.validator = CTimeValidator()
#        return CTimeEdit.validator
#
#
#    def setTime(self, time):
#        self.setText(time.toString('HH:mm'))
#        self.setCursorPosition(0)
#
#
#    def time(self):
#        return stringToTime(self.text())

class CTimeEdit(QtGui.QTimeEdit):
    def __init__(self, parent=None):
        QtGui.QTimeEdit.__init__(self, parent)
        self.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.setDisplayFormat("HH:mm")
        self.validTime = False
        self.connect(self, SIGNAL('timeChanged(QTime)'), self.on_timeChanged)

    def setTime(self, time):
        if time is None or time.isNull():
            self.validTime = False
            super(CTimeEdit, self).setTime(QTime(0, 0, 0, 0))
            self.emit(SIGNAL('dateChanged'), QTime())
        else:
            self.validTime = True
            super(CTimeEdit, self).setTime(time)

    def on_timeChanged(self, time):
        self.validTime = False
        if time.isValid():
            self.validTime = True

    def time(self):
        return super(CTimeEdit, self).time() if self.validTime else QTime()


def stringToTime(s):
    try:
        parts = s.split(':')
        if parts>=2:
            hours = trim(parts[0])
            minuts = trim(parts[1])
            if hours or minuts:
                return QTime(int('0'+hours), int('0'+minuts))
    except:
        pass
    return QTime()
