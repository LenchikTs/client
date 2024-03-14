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


class CTextBrowser(QtGui.QTextBrowser):
    def __init__(self, parent=None):
        QtGui.QTextBrowser.__init__(self, parent)
        self.actions = []


    def contextMenuEvent(self, event):
        stdMenu = self.createStandardContextMenu()
        if self.actions:
            menu = QtGui.QMenu(self)
            for action in self.actions:
                menu.addAction(action)
            menu.addSeparator()
            for action in stdMenu.actions():
                menu.addAction(action)
        else:
            menu = stdMenu
        menu.exec_(event.globalPos())
