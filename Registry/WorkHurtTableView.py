# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rights reserved.
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


class CWorkHurtTableView(CInDocTableView):
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Tab:
            index = self.currentIndex()
            model = self.model()
            if index.column() == model.columnCount()-1:
                self.parent().focusNextChild()
                event.accept()
                return
        elif key == Qt.Key_Backtab:
            index = self.currentIndex()
            if index.column() == 0:
                self.parent().focusPreviousChild()
                event.accept()
                return
        CInDocTableView.keyPressEvent(self, event)
