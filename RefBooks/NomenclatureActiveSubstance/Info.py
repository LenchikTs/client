# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2022 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
from PyQt4 import QtGui

from RefBooks.Unit.Info import CUnitInfo
from library.PrintInfo import CRBInfoWithIdentification
from library.Utils import forceString, forceRef


class CNomenclatureActiveSubstanceInfo(CRBInfoWithIdentification):
    tableName = 'rbNomenclatureActiveSubstance'

    def setRecord(self, record):
        if record:
            self._code     = forceString(record.value('code'))
            self._name     = forceString(record.value('name'))
            self._mnnLatin = forceString(record.value('mnnLatin'))
            self._unit     = self.getInstance(CUnitInfo, forceRef(record.value('unit_id')))
            self.setOkLoaded()


    def _load(self):
        db = QtGui.qApp.db
        cols = '`code`, `name`, `mnnLatin`, `unit_id`'
        record = db.getRecord('rbNomenclatureActiveSubstance', cols, self.id) if self.id else None
        if record:
            self.setRecord(record)
            return True
        else:
            self._code      = u''
            self._name      = u''
            self._mnnLatin  = u''
            self._unit      = self.getInstance(CUnitInfo, None)
            return False

    # code и name наследованы от CRBInfo
    mnnLatin = property(lambda self: self.load()._mnnLatin)
    unit     = property(lambda self: self.load()._unit)
