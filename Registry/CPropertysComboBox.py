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
from PyQt4.QtCore import Qt, QVariant

from library.Utils import forceString


class CFilterPropertyOptionsItem(QtGui.QListWidgetItem):
    def __init__(self, strItem, parent):
        QtGui.QListWidgetItem.__init__(self, strItem, parent)
        self.statusChecked = True
        self.strItem = strItem
        self.freeInput = u''


    def flags(self, index):
        if not index.isValid():
            return 0
        item = index.internalPointer()
        return item.flags()|Qt.ItemIsEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEditable


    def data(self, role):
        if role == Qt.DisplayRole:
            return QVariant(self.strItem)
        elif role == Qt.EditRole:
            return QVariant(self.freeInput)
        elif role == Qt.CheckStateRole:
            return QVariant(Qt.Checked if not self.statusChecked else Qt.Unchecked)
        return QVariant()


    def setData(self, role, value):
        if role == Qt.CheckStateRole:
            self.statusChecked = not self.statusChecked
        elif role == Qt.EditRole:
            self.freeInput = forceString(value)


    def getFreeInput(self):
        return self.freeInput


    def setFreeInput(self, value):
        self.freeInput = forceString(value)
