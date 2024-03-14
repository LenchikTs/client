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
from PyQt4.QtCore import Qt

from library.TableView  import CTableView


class COperatingMedicalDiagnosisView(CTableView):
    def __init__(self, parent):
        CTableView.__init__(self, parent)
        h = self.fontMetrics().height()
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.verticalHeader().setDefaultSectionSize(3*h/2)
        self.verticalHeader().hide()
        self.setWordWrap(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.resizeRowsToContents()


    def setRowHeightLoc(self):
        pass
