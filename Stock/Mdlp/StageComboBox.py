# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2020 SAMSON Group. All rights reserved.
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

from library.Utils import forceRef

from Stage import CMdlpStage

class CMdlpStageComboBox(QtGui.QComboBox):
    def __init__(self, parent=None):
        QtGui.QComboBox.__init__(self, parent)
        self.addItem(CMdlpStage.text(None), QVariant())
        for i, name in enumerate(CMdlpStage.names):
            self.addItem(name, QVariant(i))


    def setValue(self, value):
        index = self.findData(QVariant(value), Qt.UserRole, Qt.MatchExactly)
        self.setCurrentIndex(index)


    def value(self):
        index = self.currentIndex()
        return forceRef(self.itemData(index, Qt.UserRole))
