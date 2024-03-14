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


class CProgressBar(QtGui.QProgressBar):
    def __init__(self, parent=None):
        QtGui.QProgressBar.__init__(self, parent)
        self._format = QtGui.QProgressBar.format(self)


    def setFormat(self, format):
        QtGui.QProgressBar.setFormat(self, format)
        self._format = format


    def step(self, val=1):
        self.setValue( self.value()+val )


    def reset(self):
        self.setFormat(self._format)
        QtGui.QProgressBar.reset(self)


    def setText(self, msg):
        QtGui.QProgressBar.setFormat(self, msg)
        self.update()
