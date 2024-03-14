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

from library.PrintInfo  import CRBInfoWithIdentification
from library.Utils      import forceInt


class CEventTypePurposeInfo(CRBInfoWithIdentification):
    tableName = 'rbEventTypePurpose'


    def _initByRecord(self, record):
        self._purpose = forceInt(record.value('purpose'))


    def _initByNull(self):
        self._purpose = 0


    purpose = property(lambda self: self.load()._purpose)

