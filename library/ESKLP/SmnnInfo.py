# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2023 SAMSON Group. All rights reserved.
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
from library.Utils     import forceStringEx


class CSmnnInfo(CInfo):
    def __init__(self, context, UUID):
        CInfo.__init__(self, context)
        self.UUID = UUID


    def _load(self):
        db = QtGui.qApp.db
        tableEsklp_Smnn = db.table('esklp.Smnn')
        tableEsklp_Smnn_Dosage = db.table('esklp.Smnn_Dosage')
        queryTable = tableEsklp_Smnn.leftJoin(tableEsklp_Smnn_Dosage, tableEsklp_Smnn_Dosage['master_id'].eq(tableEsklp_Smnn['id']))
        record = db.getRecordEx(queryTable, [u'esklp.Smnn.*, esklp.Smnn_Dosage.grls_value'], [tableEsklp_Smnn['UUID'].eq(self.UUID)])
        if record:
            self.initByRecord(record)
            return True
        else:
            self.initByRecord(db.dummyRecord())
            return False


    def initByRecord(self, record):
        self._smnnUUID = forceStringEx(record.value('UUID'))
        self._code = forceStringEx(record.value('code'))
        mnn = forceStringEx(record.value('mnn'))
        self._name = mnn
        self._mnn = mnn
        self._form = forceStringEx(record.value('form'))
        self._dosage = forceStringEx(record.value('grls_value'))


    def __str__(self):
        return self.load()._name


    smnnUUID = property(lambda self: self.load()._smnnUUID)
    code     = property(lambda self: self.load()._code)
    name     = property(lambda self: self.load()._name)
    mnn      = property(lambda self: self.load()._mnn)
    form     = property(lambda self: self.load()._form)
    dosage   = property(lambda self: self.load()._dosage)

