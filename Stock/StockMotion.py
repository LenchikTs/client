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

from library.Utils                         import forceInt

from Stock.IncomingInvoiceEditDialog       import CIncomingInvoiceEditDialog
from Stock.InternalInvoiceEditDialog       import CInternalInvoiceEditDialog
from Stock.InventoryEditDialog             import CInventoryEditDialog
from Stock.FinTransferEditDialog           import CFinTransferEditDialog
from Stock.ProductionEditDialog            import CProductionEditDialog
from Stock.StockUtilizationEditDialog      import CStockUtilizationEditDialog, CStockInternalConsumptionEditDialog
from Stock.ClientInvoiceEditDialog         import (
                                                    CClientInvoiceEditDialog,
                                                    CClientRefundInvoiceEditDialog,
                                                    CClientInvoiceReservationEditDialog,
                                                  )
from Stock.StockSupplierRefundEditDialog   import CStockSupplierRefundEditDialog

stockMotionType = {
    0  : (u'Внутренняя накладная',       CInternalInvoiceEditDialog),
    1  : (u'Инвентаризация',             CInventoryEditDialog),
    2  : (u'Финансовый перенос',         CFinTransferEditDialog),
    3  : (u'Производство',               CProductionEditDialog),
    4  : (u'Списание на пациента',       CClientInvoiceEditDialog),
    5  : (u'Возврат от пациента',        CClientRefundInvoiceEditDialog),
    6  : (u'Резервирование на пациента', CClientInvoiceReservationEditDialog),
    7  : (u'Утилизация',                 CStockUtilizationEditDialog),
    8  : (u'Внутреннее потребление',     CStockInternalConsumptionEditDialog),
    9  : (u'Возврат поставщику',         CStockSupplierRefundEditDialog),
    10 : (u'Накладная от поставщика',    CIncomingInvoiceEditDialog),
}


def getDialogName(type):
    if type in stockMotionType:
        return stockMotionType[type][0]
    else:
        return '{%s}' % type


def getDialogClass(type):
    return stockMotionType[type][1]


def getStockMotionTypeNames():
    return [value[0] for value in stockMotionType.values()]


def editStockMotion(widget, id):
    type = forceInt(QtGui.qApp.db.translate('StockMotion', 'id', id, 'type'))
    dialogClass = getDialogClass(type)
    dialog = dialogClass(widget)
    try:
        dialog.load(id)
        return dialog.exec_()
    finally:
        dialog.deleteLater()


def openReadOnlyMotion(widget, id):
    type = forceInt(QtGui.qApp.db.translate('StockMotion', 'id', id, 'type'))
    dialogClass = getDialogClass(type)
    dialog = dialogClass(widget)
    try:
        dialog.load(id)
        setReadOnly(dialog)
        return dialog.exec_()
    finally:
        dialog.deleteLater()


def setReadOnly(dialog):
        if hasattr(dialog, 'edtNumber'):
            dialog.edtNumber.setEnabled(False)
        if hasattr(dialog, 'edtDate'):
            dialog.edtDate.setEnabled(False)
        if hasattr(dialog, 'edtReason'):
            dialog.edtReason.setEnabled(False)
        if hasattr(dialog, 'edtReasonDate'):
            dialog.edtReasonDate.setEnabled(False)
        if hasattr(dialog, 'edtTime'):
            dialog.edtTime.setEnabled(False)
        if hasattr(dialog, 'cmbSupplier'):
            dialog.cmbSupplier.setEnabled(False)
        if hasattr(dialog, 'cmbSupplierPerson'):
            dialog.cmbSupplierPerson.setEnabled(False)
        if hasattr(dialog, 'edtNote'):
            dialog.edtNote.setEnabled(False)
        if hasattr(dialog, 'tblItems'):
            dialog.tblItems.setEnabled(False)
        if hasattr(dialog, 'cmbSupplierOrg'):
            dialog.cmbSupplierOrg.setEnabled(False)
        if hasattr(dialog, 'edtSupplierOrgPerson'):
            dialog.edtSupplierOrgPerson.setEnabled(False)
        if hasattr(dialog, 'tblInItems'):
            dialog.tblInItems.setEnabled(False)
        if hasattr(dialog, 'tblOutItems'):
            dialog.tblOutItems.setEnabled(False)
        if hasattr(dialog, 'cmbReceiver'):
            dialog.cmbReceiver.setEnabled(False)
        if hasattr(dialog, 'cmbReceiverPerson'):
            dialog.cmbReceiverPerson.setEnabled(False)
