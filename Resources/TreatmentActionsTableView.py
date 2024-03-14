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
from PyQt4.QtCore import SIGNAL

from library.TableView import CTableView
from library.Utils     import forceRef


class CTreatmentActionsTableView(CTableView):
    def __init__(self, parent):
        CTableView.__init__(self, parent)
        self._actDeleteTreatmentRow = None
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)


    def addPopupDelRow(self):
        self._actDeleteRow = QtGui.QAction(u'Удалить выделенные строки', self)
        self._actDeleteRow.setObjectName('actDeleteRow')
        self.connect(self._actDeleteRow, SIGNAL('triggered()'), self.removeSelectedRows)
        self.addPopupAction(self._actDeleteRow)


    def removeSelectedRows(self):
        def removeSelectedRowsInternal():
            currentRow = self.currentIndex().row()
            newSelection = []
            deletedCount = 0
            rows = self.selectedRowList()
            rows.sort()
            for row in rows:
                actualRow = row-deletedCount
                self.setCurrentRow(actualRow)
                clientId = forceRef(self.model().items[actualRow].value('client_id'))
                if clientId and clientId in self.model().clientIdList:
                    confirm = self.confirmRemoveRow(actualRow, len(rows)>1)
                else:
                    confirm = False
                if confirm is None:
                    newSelection.extend(x-deletedCount for x in rows if x>row)
                    break
                if confirm:
                    self.model().removeRow(actualRow)
                    deletedCount += 1
                    if currentRow>row:
                        currentRow-=1
                else:
                    newSelection.append(actualRow)
            if newSelection:
                self.setSelectedRowList(newSelection)
            else:
                self.setCurrentRow(currentRow)
        QtGui.qApp.call(self, removeSelectedRowsInternal)


    def addPopupTreatmentDelRow(self):
        self._actDeleteTreatmentRow = QtGui.QAction(u'Удалить выделенные строки с цикла', self)
        self._actDeleteTreatmentRow.setObjectName('actDeleteTreatmentRow')
        self.connect(self._actDeleteTreatmentRow, SIGNAL('triggered()'), self.removeTreatmentSelectedRows)
        self.addPopupAction(self._actDeleteTreatmentRow)


    def removeTreatmentSelectedRows(self):
        def removeSelectedRowsInternal():
            currentRow = self.currentIndex().row()
            newSelection = []
            deletedCount = 0
            rows = self.selectedRowList()
            rows.sort()
            for row in rows:
                actualRow = row-deletedCount
                self.setCurrentRow(actualRow)
                clientId = forceRef(self.model().items[actualRow].value('client_id'))
                if clientId and clientId in self.model().clientIdList:
                    confirm = self.confirmRemoveRow(actualRow, len(rows)>1)
                else:
                    confirm = False
                if confirm is None:
                    newSelection.extend(x-deletedCount for x in rows if x>row)
                    break
                if confirm:
                    self.model().removeTreatmentRow(actualRow)
                    deletedCount += 1
                    if currentRow>row:
                        currentRow-=1
                else:
                    newSelection.append(actualRow)
            if newSelection:
                self.setSelectedRowList(newSelection)
            else:
                self.setCurrentRow(currentRow)
        QtGui.qApp.call(self, removeSelectedRowsInternal)


    def on_popupMenu_aboutToShow(self):
        CTableView.on_popupMenu_aboutToShow(self)
        enable = False
        rows = self.selectedRowList()
        rows.sort()
        items = self.model().items
        for row in rows:
            if row >= 0 and row < len(items):
                item = items[row]
                clientId = forceRef(item.value('client_id')) if item else None
                actionId = forceRef(item.value('id')) if item else None
                if clientId and actionId and clientId in self.model().clientIdList:
                    enable = True
                    break
        if self._actDeleteRow:
            self._actDeleteRow.setEnabled(enable)
        if self._actDeleteTreatmentRow:
            self._actDeleteTreatmentRow.setEnabled(enable)

