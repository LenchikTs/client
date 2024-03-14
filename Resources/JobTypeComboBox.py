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

from library.crbcombobox  import CRBModelDataCache, CRBComboBox
from library.InDocTable   import CInDocTableCol
from library.TreeComboBox import CTreeComboBox, CTreeComboBoxGetIdSetIdMixin
from library.TreeModel    import CDBTreeModel
from library.Utils        import forceRef, toVariant


class CJobTypeModel(CDBTreeModel):
    def __init__(self, parent):
        CDBTreeModel.__init__(self, parent, 'rbJobType', 'id', 'group_id', 'concat(code," | ",name)', order='code')
#            self.treeModel.setRootItem(CDBTreeItem(None, domain, rootItemId, self.treeModel))
        self.setRootItemVisible(True)
        self.setLeavesVisible(True)


class CJobTypeComboBox(CTreeComboBoxGetIdSetIdMixin, CTreeComboBox):
    def __init__(self, parent):
        CTreeComboBox.__init__(self, parent)
        self.SizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self._model = CJobTypeModel(self)
        self.setModel(self._model)
        self.setExpandAll(True)


class CJobTypeInDocTableCol(CInDocTableCol):
    def __init__(self, title, fieldName, width):
        CInDocTableCol.__init__(self, title, fieldName, width)


    def toString(self, val, record):
        cache = CRBModelDataCache.getData('rbJobType', True)
        text = cache.getStringById(forceRef(val), CRBComboBox.showName)
        return toVariant(text)


    def toStatusTip(self, val, record):
        cache = CRBModelDataCache.getData('rbJobType', True)
        text = cache.getStringById(forceRef(val), CRBComboBox.showCodeAndName)
        return toVariant(text)


    def createEditor(self, parent):
        editor = CJobTypeComboBox(parent)
        editor.model().getRootItem()._name = u'не задано'
        return editor


    def setEditorData(self, editor, value, record):
        editor.setValue(forceRef(value))


    def getEditorData(self, editor):
        return toVariant(editor.value())
