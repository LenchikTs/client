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

from library.PrintInfo import CRBInfoWithIdentification
from library.Utils     import forceString


class CMedicalAidUnitInfo(CRBInfoWithIdentification):
    tableName = 'rbMedicalAidUnit'

    def _initByRecord(self, record):
        self._descr = forceString(record.value('descr'))


    def _initByNull(self):
        self._descr = None


    descr = property(lambda self: self.load()._descr)
