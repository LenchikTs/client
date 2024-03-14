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
u"""Выпадающий список с двумя элементами""" # WFT

from PyQt4 import QtGui

from Stock.StockMotion import stockMotionType

allowedTypes = (0, 4, 7, 8)

def getStockMotionTypeNames():
    return [value[0] for key, value in stockMotionType.items()
            if key in allowedTypes]


def getStockMotionTypeIds():
    return [key for key in stockMotionType.keys()
            if key in allowedTypes]


class CStockMotionTypeComboBox(QtGui.QComboBox):
    _items = [u''] + getStockMotionTypeNames()

    def __init__(self, parent=None):
        QtGui.QComboBox.__init__(self, parent)
        self.addItems(self._items)

# ******************************************************************************
