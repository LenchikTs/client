# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2022 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
from PyQt4 import QtGui

from library.PrintInfo import CRBInfo
from library.Utils import forceString, forceBool


class CDiagnosticServiceInfo(CRBInfo):
    tableName = 'rbDiagnosticService'

    def _load(self):
        db = QtGui.qApp.db
        record = db.getRecord(self.tableName, '*', self.id) if self.id else None
        if record:
            self._code = forceString(record.value('code'))
            self._name = forceString(record.value('name'))
            self._fullName = forceString(record.value('fullName'))
            self._synonyms = forceString(record.value('synonyms'))
            self._method = forceString(record.value('method'))
            self._area = forceString(record.value('area'))
            self._localization = forceString(record.value('localization'))
            self._components = forceString(record.value('components'))
            self._applicability = forceBool(record.value('applicability'))
            self._initByRecord(record)
            return True
        else:
            self._code = ''
            self._name = ''
            self._fullName = ''
            self._synonyms = ''
            self._method = ''
            self._area = ''
            self._localization = ''
            self._components = ''
            self._applicability = ''
            self._initByNull()
            return False

    fullName = property(lambda self: self.load()._fullName)
    synonyms = property(lambda self: self.load()._synonyms)
    method = property(lambda self: self.load()._method)
    area = property(lambda self: self.load()._area)
    localization = property(lambda self: self.load()._localization)
    components = property(lambda self: self.load()._components)
    applicability = property(lambda self: self.load()._applicability)
