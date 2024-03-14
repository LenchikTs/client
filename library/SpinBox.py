# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2022 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui, QtCore


class CSpinBox(QtGui.QSpinBox):
    u'QSpinBox, который при очистке устанавливает минимальное значение, а не восстанавливает предыдущее'

    def __init__(self, parent=None):
        QtGui.QSpinBox.__init__(self, parent)
        self.installEventFilter(self)


    def eventFilter(self, watched, event):
        if event.type() == QtCore.QEvent.CloseSoftwareInputPanel:
            if not self.text():
                self.setValue(self.minimum())
        return False


    def fixup(self, value):
        if not value:
            self.setValue(self.minimum())
        else:
            QtGui.QSpinBox.fixup(self, value)


class CDoubleSpinBox(QtGui.QDoubleSpinBox):
    u'QDoubleSpinBox, который при очистке устанавливает минимальное значение, а не восстанавливает предыдущее'

    def __init__(self, parent=None):
        QtGui.QDoubleSpinBox.__init__(self, parent)
        self.installEventFilter(self)


    def eventFilter(self, watched, event):
        if event.type() == QtCore.QEvent.CloseSoftwareInputPanel:
            if not self.text():
                self.setValue(self.minimum())
        return False


    def fixup(self, value):
        if not value:
            self.setValue(self.minimum())
        else:
            QtGui.QDoubleSpinBox.fixup(self, value)
