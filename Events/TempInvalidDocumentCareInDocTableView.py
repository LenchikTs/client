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
from PyQt4.QtCore import Qt, SIGNAL, QVariant

from library.Utils           import forceRef, toVariant
from library.InDocTable      import CInDocTableView
from Registry.ClientRelationSimpleComboBox import CClientRelationSimpleComboBox


class CClientRelationDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)


    def commit(self):
        editor = self.sender()
        self.emit(SIGNAL('commitData(QWidget *)'), editor)


    def commitAndCloseEditor(self):
        editor = self.sender()
        self.emit(SIGNAL('commitData(QWidget *)'), editor)
        self.emit(SIGNAL('closeEditor(QWidget *,QAbstractItemDelegate::EndEditHint)'), editor, QtGui.QAbstractItemDelegate.NoHint)


    def createEditor(self, parent, option, index):
        model = index.model()
        clientId = model.getTempInvalidClientId()
        clientLowerIdList = []
        if index.isValid():
            items = model.items()
            for item in items:
                clientLowerId = forceRef(item.value('client_id'))
                if clientLowerId and clientLowerId not in clientLowerIdList:
                    clientLowerIdList.append(clientLowerId)
        editor = CClientRelationSimpleComboBox(parent, clientId)
        editor.setClientLowerId(clientLowerIdList)
        self.connect(editor, SIGNAL('commit()'), self.commit)
        self.connect(editor, SIGNAL('editingFinished()'), self.commitAndCloseEditor)
        return editor


    def alignment(self):
        return QVariant(Qt.AlignLeft + Qt.AlignTop)


    def setEditorData(self, editor, index):
        model = index.model()
        value = model.data(index, Qt.EditRole)
        editor.setValue(forceRef(value))


    def setModelData(self, editor, model, index):
        model = index.model()
        value = editor.value()
        model.setData(index, toVariant(value))


class CTempInvalidDocumentCareInDocTableView(CInDocTableView):
    def __init__(self, parent):
        CInDocTableView.__init__(self, parent)
        self.clientRelationDelegate = CClientRelationDelegate(self)
        self.setItemDelegateForColumn(0, self.clientRelationDelegate)
