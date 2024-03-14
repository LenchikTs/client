# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################


from PyQt4 import QtGui
from PyQt4.QtCore import QDate

from library.Utils      import forceString

from IncomingInvoiceEditDialog import CIncomingInvoiceEditDialog
from Mdlp.connection           import CMdlpConnection

def getBatchFromStockMotion(sgtin):

    db = QtGui.qApp.db
    tableStockMotion = db.table('StockMotion')
    tableStockMotionItem = db.table('StockMotion_Item')
    table = tableStockMotionItem.innerJoin(tableStockMotion,
                                           tableStockMotion['id'].eq(tableStockMotionItem['master_id']))
    currentDate  = QDate.currentDate()
    records = db.getRecordListGroupBy(table,
                                      cols=tableStockMotionItem['batch'],
                                      where=[ tableStockMotionItem['sgtin'].eq(sgtin),
                                              tableStockMotionItem['isMdlpRelated'].ne(0),
                                              tableStockMotionItem['shelfTime'].le(currentDate),
                                              tableStockMotion['deleted'].eq(0),
                                              tableStockMotion['type'].eq(CIncomingInvoiceEditDialog.stockDocumentType),
                                              tableStockMotion['date'].gt(currentDate.addYears(-5)),
                                            ],
                                      group=tableStockMotionItem['batch'].name(),
                                      limit=2)
    if len(records) == 1:
        return forceString(records[0].value('batch'))
    return None


def getBatchFromMdlp(sgtin):
    connection = CMdlpConnection()
    succ, fail = connection.getPublicSgtinsByList([sgtin])
    if succ:
        return succ[0].batch
    return None


def getBatch(sgtin):
    result = getBatchFromStockMotion(sgtin)
    if result is not None:
        return result

    if QtGui.qApp.isMdlpEnabled():
        ok, result = QtGui.qApp.call(None, getBatchFromMdlp, (sgtin,))
        if not ok:
            result = None
    return result

