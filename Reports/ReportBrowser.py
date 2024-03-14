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

from PyQt4 import QtGui
from PyQt4.QtCore import Qt

from library.TextDocument import CResourceLoaderMixin


class CReportBrowser(CResourceLoaderMixin, QtGui.QTextBrowser):
    def __init__(self, parent=None):
        QtGui.QTextBrowser.__init__(self, parent)
        CResourceLoaderMixin.__init__(self)
        self.actFind = QtGui.QAction(u'Найти...', self)
        self.actFind.setShortcut(QtGui.QKeySequence.Find)
        if parent:
            parent.addAction(self.actFind)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContentMenu)


    def showContentMenu(self, point):
        menu = self.createStandardContextMenu()
        menu.addAction(self.actFind)
        menu.exec_(self.mapToGlobal(point))


    def qtLoadResource(self, type_, url):
        return QtGui.QTextBrowser.loadResource(self, type_, url)
