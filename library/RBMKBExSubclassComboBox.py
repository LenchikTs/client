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
from PyQt4.QtCore import Qt, QVariant

from library.crbcombobox import CRBComboBox, CRBModel, CRBPopupView, CRBSelectionModel


__all__ = ( 'CRBMKBExSubclassComboBox',
          )


class CRBMKBExSubclassComboBox(CRBComboBox):
    def __init__(self, parent):
        CRBComboBox.__init__(self, parent)
        self._searchString = ''
        self.showFields = CRBComboBox.showCode
        self.setModelColumn(self.showFields)
        self._model = CRBMKBExSubclassModel(self)
        self._selectionModel = CRBSelectionModel(self._model)
        self._tableName = ''
        self._addNone   = True
        self._needCache = True
        self._filier    = ''
        self._order     = ''
        self._specialValues = None
        self.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.preferredWidth = None
        self.popupView = CRBPopupView(self)
        self.setView(self.popupView)
        self.setModel(self._model)
        self.popupView.setSelectionModel(self._selectionModel)
        self.popupView.setFrameShape(QtGui.QFrame.NoFrame)
        self.dblClickEnabled = 0
        self.readOnly = False
        self.installEventFilter(self)


    def setShowFields(self, showFields):
        self.showFields = showFields
        self.setModelColumn(self.showFields)


    def code(self):
        u"""поле code записи"""
        rowIndex = self.currentIndex()
        code = self._model.getCode(rowIndex)
        if code and self.value():
            return unicode(code)
        return u''


class CRBMKBExSubclassModel(CRBModel):
    def __init__(self, parent):
        CRBModel.__init__(self, parent)


    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role == Qt.DisplayRole or role == Qt.EditRole:
            row = index.row()
            if row < self.d.getCount():
                code = self.d.getString(row, index.column())
                if index.column() == 0:
                    if not self.getId(row):
                        return QVariant()
                    return QVariant(code)
                else:
                    return QVariant(code)
        return QVariant()

