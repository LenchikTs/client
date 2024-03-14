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


from PyQt4.QtGui import QSortFilterProxyModel
from PyQt4.QtCore import QModelIndex, SIGNAL


class CSortFilterModelIndexProxy(QModelIndex):
    def internalPointer(self):
        proxyModel = self.model()
        return proxyModel.mapToSource(self).internalPointer()


class CSortFilterProxyTreeModel(QSortFilterProxyModel):

    # Для drag-and-drop моделей
    __pyqtSignals__ = ('saveExpandedState()',
                       'restoreExpandedState()')

    def __init__(self, parent, sourceModel):
        QSortFilterProxyModel.__init__(self, parent)
        self.setSourceModel(sourceModel)
        self.connect(sourceModel, SIGNAL('saveExpandedState()'), lambda: self.emit(SIGNAL('saveExpandedState()')))
        self.connect(sourceModel, SIGNAL('restoreExpandedState()'), lambda: self.emit(SIGNAL('restoreExpandedState()')))


    def model(self):
        return self.sourceModel()


    def acceptItem(self, item):
        raise NotImplementedError('abstract method call')


    def hasFilters(self):
        # raise NotImplementedError('abstract method call')
        return False


    def filterAcceptsRow(self, sourceRow, sourceParent, depth=0):
        if self.hasFilters():
            sourceIndex = self.sourceModel().index(sourceRow, self.filterKeyColumn(), sourceParent)
            if sourceIndex.isValid():
                rowCount = self.sourceModel().rowCount(sourceIndex)
                for i in xrange(rowCount):
                    if self.filterAcceptsRow(i, sourceIndex, depth+1):
                        return True

                item = sourceIndex.internalPointer()
                return self.acceptItem(item)
        return True


    def itemId(self, index):
        return self.sourceModel().itemId(self.mapToSource(index))


    def update(self):
        self.sourceModel().update()


    def index(self, row, column, parent=QModelIndex()):
        return CSortFilterModelIndexProxy(QSortFilterProxyModel.index(self, row, column, parent))
