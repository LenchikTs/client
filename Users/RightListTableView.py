# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2014-2015 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4.QtCore import Qt

from library.InDocTable import CInDocTableView, CRecordListModel

__all__ = ['CRightListTableView',
          ]


class CRightListTableView(CInDocTableView):
    def __init__(self, parent):
        CInDocTableView.__init__(self, parent)
        self._CInDocTableView__sortColumn = None


    def on_sortByColumn(self, logicalIndex):
        currentIndex = self.currentIndex()
        currentItem = self.currentItem()
        model = self.model()
        if isinstance(model, CRecordListModel):
            header=self.horizontalHeader()
            if model.cols()[logicalIndex].sortable():
                if self._CInDocTableView__sortColumn == logicalIndex:
                    self._CInDocTableView__sortAscending = not self._CInDocTableView__sortAscending
                else:
                    self._CInDocTableView__sortColumn = logicalIndex
                    self._CInDocTableView__sortAscending = True
                header.setSortIndicatorShown(True)
                header.setSortIndicator(self._CInDocTableView__sortColumn, Qt.AscendingOrder if self._CInDocTableView__sortAscending else Qt.DescendingOrder)
                model.sortData(logicalIndex, self._CInDocTableView__sortAscending)
            elif self._CInDocTableView__sortColumn is not None:
                header.setSortIndicator(self._CInDocTableView__sortColumn, Qt.AscendingOrder if self._CInDocTableView__sortAscending else Qt.DescendingOrder)
            else:
                header.setSortIndicatorShown(False)
        if currentItem:
            newRow = model.items().values().index(currentItem)
            self.setCurrentIndex(model.index(newRow, currentIndex.column()))
        else:
            self.setCurrentIndex(model.index(0, 0))
