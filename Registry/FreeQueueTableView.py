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
from PyQt4.QtCore import QObject, QPoint, SIGNAL

from library.TableView          import CTableView


class CFreeQueueTableView(CTableView):
    def __init__(self, parent=None):
        CTableView.__init__(self, parent)
        self.currentItemKey = None
        self.offset = 0
        self.currentColumn = 0
        self.horizontalPosition = 0


    def setModel(self, model):
        oldModel = self.model()
        if oldModel:
            QObject.disconnect(oldModel, SIGNAL('beforeReset()'), self.storeRowPos)
            QObject.disconnect(oldModel, SIGNAL('afterReset()'), self.restoreRowPos)
        CTableView.setModel(self, model)
        if model:
            QObject.connect(model, SIGNAL('beforeReset()'), self.storeRowPos)
            QObject.connect(model, SIGNAL('afterReset()'), self.restoreRowPos)


    def storeRowPos(self):
        topIndex = self.indexAt(QPoint(0,0))
        topRow = topIndex.row() if topIndex.isValid() else 0
        currentIndex = self.currentIndex()
        currentRow = currentIndex.row() if currentIndex.isValid() else max(0, topRow)
        self.currentColumn = currentIndex.column() if currentIndex.isValid() else 0
        model = self.model()
        if 0<=currentRow<model.rowCount():
            self.currentItemKey = model.getKey(currentRow)
            self.offset = currentRow-topRow
        else:
            self.currentItemKey = None
            self.offset = topRow
        self.horizontalPosition = self.horizontalScrollBar().value()


    def restoreRowPos(self):
        model = self.model()
        if self.currentItemKey:
            row = model.lookupRowByKey(self.currentItemKey)
            self.scrollTo(model.index(max(0, row-self.offset), 0), QtGui.QAbstractItemView.PositionAtTop)
            self.setCurrentIndex(model.index(max(0, row), self.currentColumn))
        else:
            self.scrollTo(model.index(self.offset, 0), QtGui.QAbstractItemView.PositionAtTop)
            self.setCurrentIndex(model.index(0, 0))
        self.horizontalScrollBar().setValue(self.horizontalPosition)
