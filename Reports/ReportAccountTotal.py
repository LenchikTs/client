# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from Reports.Report import CReport, CVoidSetupDialog
from Reports.ReportAccountTotalSetup import makeReportAccountTotal


class CReportAccountingTotal(CReport):
    def __init__(self, parent, currentAccountId, accountItemIdList, selectedItemIdList=[]):
        CReport.__init__(self, parent)
        self.parent = parent
        self.setTitle(u'Счет итоговый')
        self.invoice = None
        self.selectedItemIdList = selectedItemIdList
        self.currentAccountId = currentAccountId
        self.accountItemIdList = accountItemIdList

    def getSetupDialog(self, parent):
        result = CVoidSetupDialog(parent)
        return result

    def getInvoice(self, currentAccountId, accountItemIdList, selectedItemIdList):
        invoice = makeReportAccountTotal(self.parent, currentAccountId, accountItemIdList, selectedItemIdList)
        self.invoice = invoice.getInvoice()

    def build(self, params):
        self.getInvoice(self.currentAccountId, self.accountItemIdList, self.selectedItemIdList)
        if self.invoice:
            return self.invoice
