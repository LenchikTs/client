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

from library.interchange     import getDateEditValue, setDateEditValue
from library.ItemsListDialog import CItemEditorBaseDialog
from library.Utils           import forceDate

from Ui_ChangePeriodDiagnosisLUD import Ui_ChangePeriodDiagnosisLUD


class CChangePeriodDiagnosisLUD(CItemEditorBaseDialog, Ui_ChangePeriodDiagnosisLUD):
    def __init__(self, parent):
        CItemEditorBaseDialog.__init__(self, parent, 'Diagnosis')
        self.setupUi(self)
        self.setWindowTitleEx(u'Изменить период заболевания')
        self.setupDirtyCather()


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setDateEditValue(self.edtBegDate, record, 'setDate')
        setDateEditValue(self.edtEndDate, record, 'endDate')
        self.setIsDirty(False)


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getDateEditValue(self.edtBegDate, record, 'setDate')
        getDateEditValue(self.edtEndDate, record, 'endDate')
        return record


    def checkDataEntered(self):
        result = True
        begDate = forceDate(self.edtBegDate.date())
        endDate = forceDate(self.edtEndDate.date())
        result = result and (begDate or self.checkInputMessage(u'начало периода', True, self.edtBegDate))
        result = result and (endDate or self.checkInputMessage(u'окончание периода', True, self.edtEndDate))
        return result

