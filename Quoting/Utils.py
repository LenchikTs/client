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

from library.Utils import forceString
from library.crbcombobox import CRBPopupView


def getValueFromRecords(records, col, func=forceString):
        result = [ func(rec.value(col))
                   for rec in records
                 ]
        return result


class CQuotaTypeComboBoxPopupView(CRBPopupView):
    def resizeEvent(self, resizeEvent):
        QtGui.QTableView.resizeEvent(self, resizeEvent)