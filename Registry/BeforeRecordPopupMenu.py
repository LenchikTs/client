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

from PyQt4  import QtGui
from PyQt4.QtCore import SIGNAL
from library.TableView import CTableView

# WFT? всё ради parent.printOrderQueueItem? 
# если этот класс используется только в одном месте, то он не нужен.
# а если в двух - то должно выпускать свой сигнал.

class CBeforeRecordPopupMenu(CTableView):
    def addPopupPrintRow(self, parent):
        self._actPrintRow = QtGui.QAction(u'Напечатать направление', self)
        self._actPrintRow.setObjectName('actPrintRow')
        self.connect(self._actPrintRow, SIGNAL('triggered()'), parent.printOrderQueueItem)
        self.addPopupAction(self._actPrintRow)