#!/usr/bin/env python
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
from library.PrintInfo import CInfo
from library.Utils import forceString


class CRLSInfo(CInfo):
    def __init__(self, context, code):
        CInfo.__init__(self, context)
        self.code = code


    def _load(self):
        db = QtGui.qApp.db
        table = db.table('rls.vNomen')
        record = db.getRecordEx(table, ['tradeName', 'tradeNameLat', 'INPName', 'INPNameLat', 'form', 'dosage', 'filling', 'packing'], table['code'].eq(self.code))
        if record:
            self._tradeName = forceString(record.value('tradeName'))
            self._tradeNameLat = forceString(record.value('tradeNameLat'))
            self._INPName = forceString(record.value('INPName'))
            self._INPNameLat = forceString(record.value('INPNameLat'))
            self._form = forceString(record.value('form'))
            self._dosage = forceString(record.value('dosage'))
            self._filling = forceString(record.value('filling'))
            self._packing = forceString(record.value('packing'))
            return True
        else:
            self._tradeName = ''
            self._tradeNameLat = ''
            self._INPName = ''
            self._INPNameLat = ''
            self._form = ''
            self._dosage = ''
            self._filling = ''
            self._packing = ''
            return False

    tradeName = property(lambda self: self.load()._tradeName)
    tradeNameLat = property(lambda self: self.load()._tradeNameLat)
    INPName = property(lambda self: self.load()._INPName)
    INPNameLat = property(lambda self: self.load()._INPNameLat)
    form = property(lambda self: self.load()._form)
    dosage = property(lambda self: self.load()._dosage)
    filling = property(lambda self: self.load()._filling)
    packing = property(lambda self: self.load()._packing)


    def __str__(self):
        self.load()
        if self._ok:
            return ', '.join([field for field in (self._tradeName, self._form, self._dosage, self._filling)])
        else:
            return ''