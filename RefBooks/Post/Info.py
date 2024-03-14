# -*- coding: utf-8 -*-
#############################################################################
##
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


class CPostInfo(CRBInfoWithIdentification):
    tableName = 'rbPost'

    def _initByRecord(self, record):
        self._regionalCode = forceString(record.value('regionalCode'))
        self._usishCode    = forceString(record.value('usishCode'))


    def _initByNull(self):
        self._regionalCode = ''
        self._usishCode    = ''


    def __str__(self):
        return self.load()._name


    regionalCode = property(lambda self: self.load()._regionalCode)
    usishCode = property(lambda self: self.load()._usishCode)
