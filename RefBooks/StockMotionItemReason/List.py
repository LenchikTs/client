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

from library.ItemsListDialog import CItemEditorDialog, CItemsListDialog
from library.TableModel import CTextCol

from Stock.StockModel import CStockMotionType, CStockMotionItemReason


class CRBStockMotionItemReasonDialog(CItemsListDialog):
    def __init__(self, stockMotionType, title, editorTitle, parent=None):
        self._type = stockMotionType
        self._title = title
        self._editorTitle = editorTitle

        cols = [
            CTextCol(u'Код', ['code'], 15),
            CTextCol(u'Наименование', ['name'], 25)
        ]

        order = [
            CStockMotionItemReason.code.name,
            CStockMotionItemReason.name.name,
        ]
        CItemsListDialog.__init__(self, parent, cols, CStockMotionItemReason.tableName, order)
        self.setWindowTitle(self._title)

    def generateFilterByProps(self, props):
        cond = CItemsListDialog.generateFilterByProps(self, props)
        cond.append(CStockMotionItemReason.stockMotionType == self._type)
        return cond

    def getItemEditor(self):
        return CRBStockMotionItemReasonEditorDialog(self, self._type, self._editorTitle)


class CRBStockMotionItemReasonEditorDialog(CItemEditorDialog):
    def __init__(self, parent, stockMotionType, title):
        self._stockMotionType = stockMotionType
        CItemEditorDialog.__init__(self, parent, CStockMotionItemReason.tableName)
        self.setWindowTitle(title)

    def getRecord(self):
        record = CItemEditorDialog.getRecord(self)
        CStockMotionItemReason(record).stockMotionType = self._stockMotionType
        return record


def getStockMotionItemReasonDialog(stockMotionType, parent):
    if stockMotionType == CStockMotionType.utilization:
        dialog = CRBStockMotionItemReasonDialog(stockMotionType, u'Причины утилизации', u'Причина утилизации', parent)
    else:
        raise ValueError("Not supported stockMotionType, could not edit item reasons of type `%s`" % stockMotionType)

    return dialog
