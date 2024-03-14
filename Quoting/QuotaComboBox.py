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

from RefBooks.QuotaType.List import CQuotaTypeTreeModel
from library.TreeComboBox import CTreeComboBox, CTreeComboBoxGetIdSetIdMixin


class CQuotaComboBox(CTreeComboBoxGetIdSetIdMixin, CTreeComboBox):
    def __init__(self, parent, emptyRootName=None, purpose=None, filter=None):
        CTreeComboBox.__init__(self, parent)
        self.SizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
#        self.__searchString = ''
        self._model = CQuotaTypeTreeModel(self, 'QuotaType', 'id', 'group_code', 'name', 'class', ['class', 'group_code', 'code', 'name', 'id'])
        self._model.filterClassByExists(True)
        self._model.setLeavesVisible(True)
        self.setModel(self._model)
        self.setExpandAll(False)


    def setPurpose(self, purpose):
        currValue = self.value()
        self._model.setPurpose(purpose)
        self.setValue(currValue)


    def currentGroupId(self):
        modelIndex = self.currentModelIndex()
        return self._model.itemId(modelIndex)


    def currentClass(self):
        modelIndex = self.currentModelIndex()
        return self._model.itemClass(modelIndex)