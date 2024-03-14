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

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature

from library.TreeModel        import CDBTreeModel

from Ui_SelectOrgStructureListDialog import Ui_SelectOrgStructureListDialog

# WFT?
class CSelectOrgStructureListDialog(QtGui.QDialog, Ui_SelectOrgStructureListDialog):
    def __init__(self, parent, filter=''):
        QtGui.QDialog.__init__(self, parent)
        self.modelTree = CDBTreeModel(self, 'OrgStructure', 'id', 'parent_id', 'code', ['organisation_id', 'parent_id', 'code', 'name'], filter=filter)
        self.selectionModelTree = QtGui.QItemSelectionModel(self.modelTree, self)
        self.selectionModelTree.setObjectName('selectionModelTree')
        self.setupUi(self)
        self.tblSelectOrgStructureList.setModel(self.modelTree)
        self.tblSelectOrgStructureList.setSelectionModel(self.selectionModelTree)
        self.modelTree.setLeavesVisible(True)
        self.tblSelectOrgStructureList.installEventFilter(self)
        self.tblSelectOrgStructureList.header().hide()
        self.tblSelectOrgStructureList.expand(self.modelTree.index(0, 0))
        self._parent = parent
        self.selectOrgStructureIdList = []


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Ok:
            self.getSelectOrgStructureList()
        elif buttonCode == QtGui.QDialogButtonBox.Cancel:
            self.close()


    def getSelectOrgStructureList(self):
        self.selectOrgStructureIdList = []
        for selectIndex in self.tblSelectOrgStructureList.selectedIndexes():
            if selectIndex.isValid():
                self.selectOrgStructureIdList.extend(self.modelTree.getItemIdList(selectIndex))
        self.close()


    def values(self):
        return self.selectOrgStructureIdList


    def setValue(self, selectOrgStructureIdList):
        self.selectOrgStructureIdList = selectOrgStructureIdList

