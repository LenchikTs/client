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

from Events.Action import CActionTypeCache
from library.Utils import forceRef


class CSortFilterProxyInDocTableModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent, sourceModel):
        QtGui.QSortFilterProxyModel.__init__(self, parent)
        self.__codeFilter = ''
        self.__nameFilter = ''
        self.setSourceModel(sourceModel)


    def model(self):
        return self.sourceModel()


    def __invalidateFilter(self):
        self.reset()


    def setCodeFilter(self, value):
        value = value.upper()
        if self.__codeFilter != value:
            self.__codeFilter = value
            self.__invalidateFilter()


    def setNameFilter(self, value):
        value = value.upper()
        if self.__nameFilter != value:
            self.__nameFilter = value
            self.__invalidateFilter()


    def filterAcceptsRow(self, sourceRow, sourceParent):
        sourceModel = self.sourceModel()
        actionType = CActionTypeCache.getById(forceRef(self.sourceModel().value(sourceRow, 'actionType_id')))
        if self.__codeFilter and actionType:
            sourceModel.getRecordByRow(sourceRow)
            code = actionType.code.upper()
            if self.__codeFilter not in code:
                return False
        if self.__nameFilter and actionType:
            name = actionType.name.upper()
            if self.__nameFilter not in name:
                return False
        return True


    def __getItemId(self, row):
        index = self.index(row, 0)
        sourceRow = self.mapToSource(index).row()
        return forceRef(self.sourceModel().value(sourceRow, 'id'))
