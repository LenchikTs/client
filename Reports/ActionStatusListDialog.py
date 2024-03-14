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
from PyQt4.QtCore import Qt, pyqtSignature, QVariant, QAbstractTableModel

from Events.ActionStatus      import CActionStatus

from Reports.Ui_ActionStatusListDialog import Ui_ActionStatusListDialog


class CActionStatusListDialog(QtGui.QDialog, Ui_ActionStatusListDialog):
    def __init__(self, parent, filter=None):
        QtGui.QDialog.__init__(self, parent)
        self.tableModel = CActionStatusTableModel(self)
        self.tableSelectionModel = QtGui.QItemSelectionModel(self.tableModel, self)
        self.tableSelectionModel.setObjectName('tableSelectionModel')
        self.setupUi(self)
        self.tblActionStatusList.setModel(self.tableModel)
        self.tblActionStatusList.setSelectionModel(self.tableSelectionModel)
        self.tblActionStatusList.horizontalHeader().setStretchLastSection(True)
        self._parent = parent
        self.actionStatusList =  []
        self.filter = filter


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Ok:
            self.getActionStatusList()
        elif buttonCode == QtGui.QDialogButtonBox.Cancel:
            self.close()


    def getActionStatusList(self):
        actionStatusList = self.tblActionStatusList.selectionModel().selectedRows()
        self.actionStatusList = actionStatusList
        self.close()


    def values(self):
        return self.actionStatusList


    def setValue(self, actionStatusList):
        self.actionStatusList = actionStatusList


class CActionStatusTableModel(QAbstractTableModel):
    def __init__(self, parent):
        QAbstractTableModel.__init__(self, parent)

    def flags(self, index):
        return Qt.ItemIsEnabled|Qt.ItemIsSelectable

    def rowCount(self, index = None):
            return len(CActionStatus.names)

    def columnCount(self, index = None):
            return 1

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(u'Статус действия')
        return QVariant()
        
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        row = index.row()
        if role == Qt.DisplayRole: 
            return CActionStatus.names[row]
        return QVariant()
