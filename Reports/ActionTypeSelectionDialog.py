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

from library.TreeModel    import CDBTreeModel

from Ui_ActionTypeSelectionDialog import Ui_ActionTypeSelectionDialog


class CActionTypeSelectionDialog(QtGui.QDialog, Ui_ActionTypeSelectionDialog):
    def __init__(self, parent, filter=''):
        QtGui.QDialog.__init__(self, parent)
        self.modelTree = CDBTreeModel(self, 'ActionType', 'id', 'group_id', 'name', ['group_id', 'code', 'name'], filter=filter)
        self.selectionModelTree = QtGui.QItemSelectionModel(self.modelTree, self)
        self.selectionModelTree.setObjectName('selectionModelTree')
        self.setupUi(self)
        self.tblActionTypeList.setModel(self.modelTree)
        self.tblActionTypeList.setSelectionModel(self.selectionModelTree)
        self.modelTree.setLeavesVisible(True)
        self.tblActionTypeList.installEventFilter(self)
        self.tblActionTypeList.header().hide()
        self.tblActionTypeList.expand(self.modelTree.index(0, 0))
        self._parent = parent
        self.actionTypeListIdList = []


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Ok:
            self.getActionTypeList()
        elif buttonCode == QtGui.QDialogButtonBox.Cancel:
            self.close()


    def getActionTypeList(self):
        self.actionTypeListIdList = []
        for selectIndex in self.tblActionTypeList.selectedIndexes():
            if selectIndex.isValid():
                self.actionTypeListIdList.extend(self.modelTree.getItemIdList(selectIndex))
        self.close()


    def values(self):
        return self.actionTypeListIdList


    def setValue(self, actionTypeListIdList):
        self.actionTypeListIdList = actionTypeListIdList
