# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

import email.utils
from PyQt4 import QtGui

from Accounting.Utils     import CContractTreeModel
from library.TreeComboBox import CTreeComboBox


class CContractComboBox(CTreeComboBox):
    def __init__(self, parent):
        CTreeComboBox.__init__(self, parent)
        self.SizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self._model = CContractTreeModel(self)
        self.setModel(self._model)


    def getPath(self):
        index = self.currentModelIndex()
        if index and index.isValid():
            item = index.internalPointer()
            parts = []
            while item:
                parts.append(email.utils.quote(item.name))
                item = item.parent
            return '\\'.join(parts[::-1])


    def setPath(self, path):
        names = [email.utils.unquote(part) for part in path.split('\\')][1:]
        item = self._model.getRootItem()
        for name in names:
            nextItem = item.mapNameToItem.get(name, None)
            if nextItem:
                item = nextItem
            else:
                break
        index = self._model.createIndex(item.row(), 0, item)
        self.setCurrentModelIndex(index)


    def getPathById(self, contractId):
        path = self._model.getPathById(contractId)
        return '\\'.join(path)


    def getIdByPath(self, path):
        return self._model.getIdByPath(path)


    def getIdList(self):
        index = self.currentModelIndex()
        item = index.internalPointer()
        return item.idList


#    def value(self):
#        modelIndex = self._model.index(self.currentIndex(), 0, self.rootModelIndex())
#        if modelIndex.isValid():
#            return self._model.itemId(modelIndex)
#        return None
