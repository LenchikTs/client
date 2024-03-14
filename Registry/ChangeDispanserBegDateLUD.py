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

from library.interchange     import getDateEditValue, setDateEditValue
from library.ItemsListDialog import CItemEditorBaseDialog
from library.Utils           import forceDate, forceRef, forceString

from Ui_ChangeDispanserBegDateLUD import Ui_ChangeDispanserBegDateLUD


class CChangeDispanserBegDateLUD(CItemEditorBaseDialog, Ui_ChangeDispanserBegDateLUD):
    def __init__(self, parent):
        CItemEditorBaseDialog.__init__(self, parent, 'Diagnosis')
        self.setupUi(self)
        self.setWindowTitleEx(u'Изменить дату постановки на учет')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setDateEditValue(self.edtBegDate, record, 'dispanserBegDate')
        self.setIsDirty(False)


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getDateEditValue(self.edtBegDate, record, 'dispanserBegDate')
        return record


    def checkDataEntered(self):
        result = True
        begDate = forceDate(self.edtBegDate.date())
        result = result and (begDate or self.checkInputMessage(u'дату постановки на диспансерный учет', True, self.edtBegDate))
        return result


    def afterSave(self):
        record = CItemEditorBaseDialog.getRecord(self)
        db = QtGui.qApp.db
        table = db.table('ProphylaxisPlanning')
        db.updateRecords(table,
                         table['takenDate'].eq(forceDate(record.value('dispanserBegDate'))),
                         [table['MKB'].eq(forceString(record.value('MKB'))),
                          table['client_id'].eq(forceRef(record.value('client_id'))),
                          table['deleted'].eq(0)
                          ])