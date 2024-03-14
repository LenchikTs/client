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


from PyQt4.QtCore import Qt

from library.TableView    import CTableView


class CAddressesTableView(CTableView):
    def __init__(self, parent):
        CTableView.__init__(self, parent)
        self._order = None
        self._orderColumn = 0
        self._isDesc = True


    def order(self):
        return self._order


    def setOrder(self, column):
        if column is not None:
            self._isDesc = not self._isDesc if self._orderColumn == column else False
            self._order = self.getOrder(column) + (' DESC' if self._isDesc else ' ASC')
            self._orderColumn = column
            self.horizontalHeader().setSortIndicator(column, Qt.DescendingOrder if self._isDesc else Qt.AscendingOrder)
        else:
            self._order = None
            self._orderColumn = None
            self._isDesc = True


    def getOrder(self, column):
        return self.model().getOrder(self.model().cols()[column].fields()[0], column)

