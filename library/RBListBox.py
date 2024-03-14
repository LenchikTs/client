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

from library.crbcombobox import CRBModel


class CRBListBox(QtGui.QTableView):
    def __init__(self, parent=None):
        QtGui.QTableView.__init__(self, parent)
        self.__tableName = ''
        self.__filier    = ''
        self.__model = CRBModel(self)
        self.setModel(self.__model)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().hideSection(2)
        self.horizontalHeader().resizeSections(QtGui.QHeaderView.Stretch)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.horizontalHeader().setStretchLastSection(True)


    def setTable(self, tableName, filter=''):
        self.__tableName = tableName
        self.__filier    = filter
        self.__model.setTable(tableName, False, filter)
        self.resizeRowsToContents()


    def setValues(self, values):
        selectionModel = self.selectionModel()
        selectionModel.clear()
        for value in values:
            i = self.__model.searchId(value)
            if i>=0:
#                selectionModel.select(self.__model.index(i, 0), QtGui.QItemSelectionModel.Select|QtGui.QItemSelectionModel.Columns)
                selectionModel.select(self.__model.index(i, 0), QtGui.QItemSelectionModel.Select|QtGui.QItemSelectionModel.Rows)


    def values(self):
        result = []
        selectionModel = self.selectionModel()
        for index in selectionModel.selectedRows():
            result.append(self.__model.getId(index.row()))
        return result
