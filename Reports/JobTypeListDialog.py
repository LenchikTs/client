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

from Ui_JobTypeListDialog import Ui_JobTypeListDialog


class CJobTypeListDialog(QtGui.QDialog, Ui_JobTypeListDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.modelTree = CDBTreeModel(self, 'rbJobType', 'id', 'group_id', 'name', ['group_id', 'code', 'name'])
        self.selectionModelTree = QtGui.QItemSelectionModel(self.modelTree, self)
        self.selectionModelTree.setObjectName('selectionModelTree')
        self.setupUi(self)
        self.tblJobTypeList.setModel(self.modelTree)
        self.tblJobTypeList.setSelectionModel(self.selectionModelTree)
        self.modelTree.setLeavesVisible(True)
        self.tblJobTypeList.installEventFilter(self)
        self.tblJobTypeList.header().hide()
        self.tblJobTypeList.expand(self.modelTree.index(0, 0))
        self._parent = parent
        self.jobTypeListIdList = []


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Ok:
            self.getJobTypeList()
        elif buttonCode == QtGui.QDialogButtonBox.Cancel:
            self.close()


    def getJobTypeList(self):
        self.jobTypeListIdList = []
        for selectIndex in self.tblJobTypeList.selectedIndexes():
            if selectIndex.isValid():
                self.jobTypeListIdList.extend(self.modelTree.getItemIdList(selectIndex))
        self.close()


    def values(self):
        return self.jobTypeListIdList


    def setValue(self, jobTypeListIdList):
        self.jobTypeListIdList = jobTypeListIdList
