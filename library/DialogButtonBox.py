# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, SIGNAL


__all__ = ('CApplyResetDialogButtonBox',
          )


class CApplyResetDialogButtonBox(QtGui.QDialogButtonBox):
    def __init__(self, *args):
        QtGui.QDialogButtonBox.__init__(self, *args)
        self.returnShortcut = QtGui.QShortcut(QtGui.QKeySequence(Qt.Key_Return), self)
        self.enterShortcut  = QtGui.QShortcut(QtGui.QKeySequence(Qt.Key_Enter), self)
        self.ctrlMShortcut  = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+M'), self)
        self.resetShortcut  = QtGui.QShortcut(QtGui.QKeySequence(Qt.Key_Clear), self)
        self.connect(self.returnShortcut, SIGNAL('activated()'), self.apply)
        self.connect(self.enterShortcut, SIGNAL('activated()'), self.apply)
        self.connect(self.ctrlMShortcut, SIGNAL('activated()'), self.apply)
        self.connect(self.resetShortcut, SIGNAL('activated()'), self.reset)

    def apply(self):
        button = self.button(QtGui.QDialogButtonBox.Apply)
        if button:
            button.animateClick()

    def reset(self):
        button = self.button(QtGui.QDialogButtonBox.Reset)
        if button:
            button.animateClick()
