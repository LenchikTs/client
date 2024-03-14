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

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDate

from library.DialogBase import CDialogBase
from library.Utils      import forceRef, toVariant, forceInt, forceDate, forceStringEx

from Stock.Ui_StockChangeAgreementStatusEditor import Ui_StockChangeAgreementStatusEditor


class CStockChangeAgreementStatusDialog(CDialogBase, Ui_StockChangeAgreementStatusEditor):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.RTMsId = None
        self.record = None


    def saveData(self):
        if self.RTMsId and self.record:
            self.record.setValue('agreementStatus', toVariant(self.cmbAgreementStatus.currentIndex()))
            self.record.setValue('agreementDate', toVariant(self.edtAgreementDate.date()))
            self.record.setValue('agreementPerson_id', toVariant(self.cmbAgreementPerson.value()))
            self.record.setValue('agreementNote', toVariant(self.edtAgreementNote.text()))
            db = QtGui.qApp.db
            table = db.table('StockRequisition')
            db.updateRecord(table, self.record)
        return True


    def loadData(self, RTMsId):
        self.record = None
        self.RTMsId = RTMsId
        if self.RTMsId:
            db = QtGui.qApp.db
            table = db.table('StockRequisition')
            cond = [table['id'].eq(self.RTMsId),
                    table['deleted'].eq(0)
                   ]
            self.record = db.getRecordEx(table, '*', cond)
            if self.record:
                self.cmbAgreementStatus.setCurrentIndex(forceInt(self.record.value('agreementStatus')))
                agreementDate = forceDate(self.record.value('agreementDate'))
                self.edtAgreementDate.setDate(agreementDate if agreementDate else QDate.currentDate())
                agreementPersonId = forceRef(self.record.value('agreementPerson_id'))
                self.cmbAgreementPerson.setValue(agreementPersonId if agreementPersonId else QtGui.qApp.userId)
                self.edtAgreementNote.setText(forceStringEx(self.record.value('agreementNote')))

