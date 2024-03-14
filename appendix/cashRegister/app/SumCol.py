# -*- coding: utf-8 -*-

#############################################################################
##
## Copyright (C) 2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4.QtCore       import Qt, QVariant

from library.InDocTable import CFloatInDocTableCol
from library.Utils      import forceDouble


class CSumCol(CFloatInDocTableCol):
    def _toString(self, value):
        if value.isNull():
            return None
        sum = forceDouble(value)
        if sum == -0:
            sum = 0.0
        return format(sum, '.2f')


    def alignment(self):
        return QVariant(Qt.AlignRight + Qt.AlignVCenter)


