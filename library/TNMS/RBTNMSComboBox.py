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
from PyQt4.QtCore import Qt, QVariant, QString

from library.crbcombobox import CRBComboBox, CRBModel, CRBSelectionModel, CRBPopupView


__all__ = ( 'CRBTNMSComboBox',
          )


class CRBTNMSComboBox(CRBComboBox):
    def __init__(self, parent):
        CRBComboBox.__init__(self, parent)
        self._searchString = ''
        self.showFields = CRBComboBox.showCode
        self._model = CRBTNMSModel(self)
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
        self.setModelColumn(self.showFields)
        self.setView(self.popupView)
        self.setModel(self._model)
        self.popupView.setSelectionModel(self._selectionModel)
        self.popupView.setFrameShape(QtGui.QFrame.NoFrame)
        self.dblClickEnabled = 0
        self.readOnly = False
        self.installEventFilter(self)
        self.isTrim = False


    def setShowFields(self, showFields, isTrim=False):
        self.isTrim = isTrim
        self.model().setIsTrim(self.isTrim)
        self.showFields = showFields
        self.setModelColumn(self.showFields)


    def code(self):
        u"""поле code записи"""
        rowIndex = self.currentIndex()
        code = self._model.getCode(rowIndex)
        if code and self.value():
            if self.isTrim:
                return unicode(code)
            code = QString(code)
            return unicode(code.right(code.length()-1))
        return ''


class CRBTNMSModel(CRBModel):
    def __init__(self, parent):
        CRBModel.__init__(self, parent)
        self.isTrim = False


    def setIsTrim(self, value):
        self.isTrim = value


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
                    if self.isTrim:
                        return QVariant(code)
                    else:
                        code = QString(code)
                        if code != u"Нет":
                            return QVariant(code.right(code.length()-1))
                        else:
                            return QVariant(code)
                else:
                    return QVariant(code)
        return QVariant()

