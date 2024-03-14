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
##
##
## AgeSelector -- это структура данных для описания ограничения возраста пациента
## по устройству - это кортеж из 4 значений: (begUnit, begCount, endUnit, endCount)
## begUnit и endUnit - единицы измерения времени:
## 0 - нет,
## 1 - дни
## 2 - недели
## 3 - месяцы
## 4 - года
## begCount и endCount - наименьший и наибольший подходящий возраст в
## указанных единицах
##
#############################################################################

import re

from PyQt4 import QtGui

from library.Utils import forceString

__all__ = [ 'parseAgeSelector',
            'parseAgeSelectorInt',
            'checkAgeSelectorSyntax',
            'composeAgeSelector',
            'checkAgeSelector',
            'convertAgeSelectorToAgeRange',
          ]

#from Ui_AgeSelector import Ui_Form

AgeSelectorUnits = u'днмг'

def parseAgeSelectorPart(val):
    if val:
        matchObject = re.match(r'^(\d+)\s*([^\d\s]+)$', val)
        if matchObject:
            strCount, strUnit = matchObject.groups()
            count = int(strCount) if strCount else 0
            unit  = AgeSelectorUnits.find(strUnit.lower())+1
            if unit == 0:
                raise ValueError, u'Неизвестная единица измерения "%s"' % strUnit
            return (unit, count)
        else:
            raise ValueError, u'Недопустимый синтаксис части селектора возраста "%s"' % val
    else:
        return 0, 0

def parseAgeSelectorInt(val):
    u""" selector syntax: "{NNN{д|н|м|г}-{MMM{д|н|м|г}}" -
    с NNN дней/недель/месяцев/лет по MMM дней/недель/месяцев/лет;
    пустая нижняя или верхняя граница - нет ограничения снизу или сверху"""
    parts = forceString(val).split('-')
    if len(parts) == 2:
        begUnit, begCount = parseAgeSelectorPart(parts[0].strip())
        endUnit, endCount = parseAgeSelectorPart(parts[1].strip())
        return begUnit, begCount, endUnit, endCount
    elif len(parts) == 1:
        if parts[0]:
            begUnit, begCount = parseAgeSelectorPart(parts[0].strip())
        else:
            begUnit, begCount = 0, 0
        return begUnit, begCount, 0, 0
#    elif len(parts) == 0: # не бывает
#        return 0, 0, 0, 0
    else:
        raise ValueError, u'Недопустимый синтаксис селектора возраста "%s"' % val


def parseAgeSelector(val):
    try:
        return parseAgeSelectorInt(val)
    except:
        QtGui.qApp.logCurrentException()
        return 0, 0, 0, 0


def checkAgeSelectorSyntax(val):
    try:
        parseAgeSelectorInt(val)
        return True
    except:
        return False


def composeAgeSelectorPart(unit, count):
    if unit == 0 or count == 0:
        return ''
    else:
        return str(count)+AgeSelectorUnits[unit-1]


def composeAgeSelector(begUnit, begCount, endUnit, endCount):
    if (begUnit == 0 or begCount == 0) and (endUnit == 0 or endCount == 0):
        return ''
    else:
        return composeAgeSelectorPart(begUnit,begCount)+'-'+composeAgeSelectorPart(endUnit,endCount)


def checkAgeSelector((begUnit, begCount, endUnit, endCount), ageTuple):
    if begUnit != 0:
        if ageTuple[begUnit-1]<begCount:
            return False
    if endUnit != 0:
        if ageTuple[endUnit-1]>endCount:
            return False
    return True


def convertAgeSelectorToAgeRange((begUnit, begCount, endUnit, endCount)):
    begAge = 0
    if begUnit == 1: # д
        begAge = begCount/365
    elif begUnit == 2: # н
        begAge = begCount*7/365
    elif begUnit == 3: # м
        begAge = begCount/12
    elif begUnit == 4: # г
        begAge = begCount

    endAge = 150
    if endUnit == 1: # д
        endAge = (endCount+364)/365
    elif endUnit == 2: # н
        endAge = (endCount*7+364)/365
    elif endUnit == 3: # м
        endAge = (endCount+11)/12
    elif endUnit == 4: # г
        endAge = endCount

    return begAge, endAge


#class CAgeSelector(QtGui.QWidget, Ui_Form):
#    def __init__(self,  parent=None):
#        QtGui.QWidget.__init__(self,  parent)
#        self.setupUi(self)
#        self.edtBegAgeCount.setEnabled(False)
#        self.edtBegAgeCount.setText('')
#        self.edtEndAgeCount.setEnabled(False)
#        self.edtEndAgeCount.setText('')
#        self.cmbBegAgeUnit.setCurrentIndex(0)
#        self.cmbEndAgeUnit.setCurrentIndex(0)
#
#    def setValue(self, val):
#        (begUnit, begCount, endUnit, endCount) = parseAgeSelector(val)
#        self.cmbBegAgeUnit.setCurrentIndex(begUnit)
#        self.edtBegAgeCount.setText(begCount)
#        self.cmbEndAgeUnit.setCurrentIndex(endUnit)
#        self.edtEndAgeCount.setText(endCount)
#
#    def getValue(self):
#        return compseAgeSelector(
#                                 self.cmbBegAgeUnit.currentIndex,  self.edtBegAgeCount.text(),
#                                 self.cmbEndAgeUnit.currentIndex,  self.edtEndAgeCount.text()
#                                )
#
#
#    @QtCore.pyqtSignature('int')
#    def on_cmbBegAgeUnit_currentIndexChanged(self, index):
#        self.edtBegAgeCount.setEnabled(index>0)
#        self.emitValueChanged
#
#
#    @QtCore.pyqtSignature('QString')
#    def on_edtBegAgeCount_textEdited(self, text):
#        self.emitValueChanged
#
#
#    @QtCore.pyqtSignature('int')
#    def on_cmbEndAgeUnit_currentIndexChanged(self, index):
#        self.edtEndAgeCount.setEnabled(index>0)
#        self.emitValueChanged
#
#
#    @QtCore.pyqtSignature('QString')
#    def on_edtEndAgeCount_textEdited(self, text):
#        self.emitValueChanged
#
#
#    def emitValueChanged(self):
#        self.emit(QtCore.SIGNAL('valueChanged()'))
