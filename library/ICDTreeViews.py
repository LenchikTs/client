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
from PyQt4.QtCore import Qt, SIGNAL

from library.TableView import CTableView


class CICDTreeView(QtGui.QTreeView):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            event.accept()
            self.emit(SIGNAL('doubleClicked(QModelIndex)'), self.currentIndex())
        else:
            QtGui.QTreeView.keyPressEvent(self, event)

#    def toolTip(self):
#        return 'hello!'


class CICDSearchResult(CTableView):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            event.accept()
            self.emit(SIGNAL('doubleClicked(QModelIndex)'), self.currentIndex())
        else:
            CTableView.keyPressEvent(self, event)