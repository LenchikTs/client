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

from PyQt4.QtCore import Qt

from library.InDocTable import CInDocTableView


#WFT?
class CInDocTableViewTabMod(CInDocTableView):
    def __init__(self, parent):
        CInDocTableView.__init__(self, parent)
        self.tabLeft = None
        self.tabRight = None


    def setTabLeftBorder(self, tab):
        self.tabLeft = tab


    def setTabRightBorder(self, tab):
        self.tabRight = tab


    def keyPressEvent(self, event):
        #self.tblItems.keyPressEventOrig(event)
        super(CInDocTableViewTabMod, self).keyPressEvent(event)
        if event.key() == Qt.Key_Tab:
            index = self.currentIndex()
            if self.tabLeft and index.column() < self.tabLeft:
                self.setCurrentIndex(self.model().index(index.row(), self.tabLeft))
            if self.tabRight and index.column() > self.tabRight:
                tab = self.tabLeft if self.tabLeft is not None else 0
                self.setCurrentIndex(self.model().index(index.row()+1, tab))
