# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from library.PrintInfo  import CRBInfo
from library.Utils      import forceString


class CAccountExportFormatInfo(CRBInfo):
    tableName = 'rbAccountExportFormat'

    def _initByRecord(self, record):
        self._prog = forceString(record.value('prog'))

    def _initByNull(self):
        self._prog = ''

    prog = property(lambda self: self.load()._prog)


