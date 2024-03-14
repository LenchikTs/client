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
from PyQt4.QtCore import Qt, QEvent

from library.Utils      import toVariant, forceDate, forceBool
from library.InDocTable import CInDocTableView, CLocItemDelegate


class CDatePeriodsItemDelegate(CLocItemDelegate):
    def __init__(self, parent):
        CLocItemDelegate.__init__(self, parent)


    def setEditorData(self, editor, index):
        if editor is not None:
            column = index.column()
            row    = index.row()
            model  = index.model()
            if row < len(model.items()):
                record = model.items()[row]
            else:
                record = model.table.newRecord()
                if len(model.items()) >= 1:
                    item = model.items()[row-1]
                    begDate = forceDate(item.value('begDate'))
                    endDate = forceDate(item.value('endDate'))
                    if begDate < endDate:
                        model.setEditorData(column, editor, toVariant(endDate.addDays(1)), record)
                        return
            model.setEditorData(column, editor, model.data(index, Qt.EditRole), record)


class CDurationPeriodsItemDelegate(CLocItemDelegate):
    def __init__(self, parent):
        CLocItemDelegate.__init__(self, parent)


    def eventFilter(self, object, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Tab:
                if self.editor is not None:
                    self.editor.keyPressEvent(event)
                    return True
            elif event.key() == Qt.Key_Backtab:
                if self.editor is not None:
                    self.editor.keyPressEvent(event)
                    return True
            elif event.key() == Qt.Key_Return:
                return True
        return QtGui.QItemDelegate.eventFilter(self, object, event)


class CTempInvalidPeriodsInDocTableView(CInDocTableView):

    Col_BegDate       = 0
    Col_EndDate       = 1
    Col_Duration      = 2
    Col_ChairPersonId = 4

    def __init__(self, parent):
        CInDocTableView.__init__(self, parent)
        self.datePeriodsItemDelegate = CDatePeriodsItemDelegate(self)
        self.durationPeriodsItemDelegate = CDurationPeriodsItemDelegate(self)
        self.setItemDelegateForColumn(CTempInvalidPeriodsInDocTableView.Col_BegDate, self.datePeriodsItemDelegate)
        self.setItemDelegateForColumn(CTempInvalidPeriodsInDocTableView.Col_EndDate, self.datePeriodsItemDelegate)
        self.setItemDelegateForColumn(CTempInvalidPeriodsInDocTableView.Col_Duration, self.durationPeriodsItemDelegate)
        self.resizeRowsToContents()


    def on_popupMenu_aboutToShow(self):
        CInDocTableView.on_popupMenu_aboutToShow(self)
        model = self.model()
        row = self.currentIndex().row()
        rowCount = model.realRowCount() if hasattr(model, 'realRowCount') else model.rowCount()
        if self._CInDocTableView__actDeleteRows:
            self._CInDocTableView__actDeleteRows.setText(u'Удалить текущую строку')
            enabledDeleteRows = bool(0 <= row < rowCount)
            if model.documentsSignatureR:
                enabledDeleteRows = False
            if model.documentsSignatureExternalR:
                if 0 <= row < len(model._items):
                    record = model._items[row]
                    if forceBool(record.value('isExternal')):
                        enabledDeleteRows = False
            if model.periodsSignaturesC:
                if 0 <= row < len(model._items):
                    if model.periodsSignaturesC.get(row, False):
                        enabledDeleteRows = False
                    else:
                        record = model._items[row]
                        isExternal = forceBool(record.value('isExternal'))
                        if isExternal:
                            for periodsSignatureC in model.periodsSignaturesC.values():
                                if periodsSignatureC:
                                    enabledDeleteRows = False
                                    break
            if model.periodsSignaturesD:
                if 0 <= row < len(model._items):
                    if model.periodsSignaturesD.get(row, False):
                        enabledDeleteRows = False
                    else:
                        record = model._items[row]
                        isExternal = forceBool(record.value('isExternal'))
                        if isExternal:
                            for periodsSignatureD in model.periodsSignaturesC.values():
                                if periodsSignatureD:
                                    enabledDeleteRows = False
                                    break
            self._CInDocTableView__actDeleteRows.setEnabled(enabledDeleteRows)

