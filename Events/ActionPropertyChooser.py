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
from PyQt4.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, pyqtSignature, SIGNAL

from library.DialogBase import CDialogBase
from library.Utils import forceInt, toVariant

from Events.Ui_ActionPropertyChooser import Ui_ActionPropertyChooserDialog


class CActionPropertyChooser(CDialogBase, Ui_ActionPropertyChooserDialog):
    def __init__(self, parent, actionPropertyTypeList):
        CDialogBase.__init__(self, parent)
        self.addModels('Choose', CActionChooseModel(self, actionPropertyTypeList))
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setWindowTitleEx(u'Выбор свойств для отчёта')
        self.setModels(self.tblChoose, self.modelChoose, self.selectionModelChoose)
        self.tblChoose.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)


    def getSelectedPropertyTypeList(self):
        return self.modelChoose.getSelectedPropertyTypeList()


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_modelChoose_dataChanged(self, topLeft, bottomRight):
        left = topLeft.column()
        right = bottomRight.column()
        if  left <= 1 <= right:
            self.chkShowUnit.setCheckState(self.modelChoose.getUnitCheckState())
        if  left <= 2 <= right:
            self.chkShowNorm.setCheckState(self.modelChoose.getNormCheckState())


    @pyqtSignature('int')
    def on_chkShowUnit_stateChanged(self, state):
        if state in (Qt.Unchecked, Qt.Checked):
            self.modelChoose.setShowUnit(state == Qt.Checked)


    @pyqtSignature('int')
    def on_chkShowNorm_stateChanged(self, state):
        if state in (Qt.Unchecked, Qt.Checked):
            self.modelChoose.setShowNorm(state == Qt.Checked)



class CActionChooseModel(QAbstractTableModel):
    headers = (u'Наименование', u'Ед.изм.', u'Норма')

    def __init__(self, parent, actionPropertyTypeList):
        QAbstractTableModel.__init__(self, parent)
        self.actionPropertyTypeList = actionPropertyTypeList
        self.selected = [True]*len(self.actionPropertyTypeList)
        self.showUnit = [False]*len(self.actionPropertyTypeList)
        self.showNorm = [False]*len(self.actionPropertyTypeList)


    def columnCount(self, index = None):
        return 3


    def rowCount(self, index = QModelIndex()):
        return len(self.actionPropertyTypeList)


    def flags(self, index = QModelIndex()):
        return Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsUserCheckable


    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return QVariant(CActionChooseModel.headers[section])
        return QVariant()


    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        column = index.column()
        if column == 0:
            if role == Qt.DisplayRole:
                return toVariant(self.actionPropertyTypeList[row].name)
            elif role == Qt.CheckStateRole:
                return QVariant(Qt.Checked if self.selected[row] else Qt.Unchecked)
        elif column == 1:
            if role == Qt.CheckStateRole:
                return QVariant(Qt.Checked if self.showUnit[row] else Qt.Unchecked)
        elif column == 2:
            if role == Qt.CheckStateRole:
                return QVariant(Qt.Checked if self.showNorm[row] else Qt.Unchecked)
        return QVariant()


    def setData(self, index, value, role=Qt.EditRole):
        row = index.row()
        column = index.column()
        if role == Qt.CheckStateRole:
            if column == 0:
                self.selected[row] = forceInt(value) == Qt.Checked
            elif column == 1:
                self.showUnit[row] = forceInt(value) == Qt.Checked
            elif column == 2:
                self.showNorm[row] = forceInt(value) == Qt.Checked
            self.emitDataChanged(row, column)
            return True
        return False


    def getSelectedPropertyTypeList(self):
        result = [(actionProperty, showUnit, showNorm)
                  for selected, actionProperty, showUnit, showNorm in zip(self.selected, self.actionPropertyTypeList, self.showUnit, self.showNorm)
                  if selected]
        return result


    def setChkColumn(self, data, checked, column):
        for i in xrange(len(data)):
            if data[i] != checked:
                data[i] = checked
                self.emitDataChanged(i, column)


    def getCheckState(self, data):
        numChecked = sum(data)
        if numChecked == len(data):
            return Qt.Checked
        elif numChecked:
            return Qt.PartiallyChecked
        else:
            return Qt.Unchecked


    def setShowUnit(self, checked):
        self.setChkColumn(self.showUnit, checked, 1)


    def setShowNorm(self, checked):
        self.setChkColumn(self.showNorm, checked, 2)


    def getUnitCheckState(self):
        return self.getCheckState(self.showUnit)


    def getNormCheckState(self):
        return self.getCheckState(self.showNorm)


    def emitDataChanged(self, row, column):
        index = self.index(row, column)
        self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)