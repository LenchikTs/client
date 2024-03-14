# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
from PyQt4 import QtGui

from library.PrintInfo import CRBInfoWithIdentification
from library.Utils import forceString


class CDocumentTypeInfo(CRBInfoWithIdentification):
    tableName = 'rbDocumentType'

    def _load(self):
        db = QtGui.qApp.db
        record = db.getRecord(self.tableName, '*', self.id) if self.id else None
        if record:
            self._code = forceString(record.value('code'))
            self._name = forceString(record.value('name'))
            self._title = forceString(record.value('title'))
            self._initByRecord(record)
            return True
        else:
            self._code = ''
            self._name = ''
            self._title = ''
            self._initByNull()
            return False

    title = property(lambda self: self.load()._title)
