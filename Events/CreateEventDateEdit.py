# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2015 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4.QtCore import Qt, QDate, QEvent, QObject

from library.DateEdit            import CDateEdit

# WTF???

class CCreateEventDateEdit(CDateEdit):
    def event(self, event):
        if event.type() == QEvent.KeyPress:
            key = event.key()
            if key == Qt.Key_Equal or (key == Qt.Key_Space and not self.date().isValid()):
                self.setDate(QDate.currentDate())
                parent = QObject.parent(self).parent() if (QObject.parent(self) is not None) else None
                if parent is not None and hasattr(parent, 'setCurTime'):
                    parent.setCurTime(self)
                event.accept()
                return True
        return CDateEdit.event(self, event)
