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
from PyQt4.QtCore import Qt, QObject, QVariant, QDate

from library.TableView   import CTableView
from library.StrComboBox import CStrComboBox
from library.DateEdit    import CDateEdit
from library.Utils       import forceString


class CDateStringItemDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)


    def createEditor(self, parent, option, index):
        model = index.model()
        if model.isHasJobTicket:
            editor = CStrComboBox(parent)
            editor.setDomain(model.domain)
        else:
            if bool(model.minimumDate):
                editor = CDateEdit(parent)
                editor.setMinimumDate(model.minimumDate)
        return editor


    def setEditorData(self, editor, index):
        model  = index.model()
        data = model.data(index, Qt.EditRole)
        if model.isHasJobTicket:
            editor.setValue(data)
        else:
            editor.setDate(data.toDate())


    def setModelData(self, editor, model, index):
        if model.isHasJobTicket:
            model.setData(index, QVariant(editor.text()))
        else:
            model.setData(index, QVariant(editor.date()))


    def getEditorData(self, editor, index):
        model  = index.model()
        if model.isHasJobTicket:
            value = editor.text()
            if value:
                return QVariant(QDate.fromString(forceString(value), "dd.MM.yyyy"))
        else:
            value = editor.date()
            if value.isValid():
                return QVariant(value)
        return QVariant()


class CExecutionPlanTableView(CTableView):
    def __init__(self, parent):
        CTableView.__init__(self, parent)
        self.setItemDelegateForColumn(0, CDateStringItemDelegate(self))


    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Space:
            QObject.parent(self).on_btnEdit_clicked() # FTF? Это просто редкостный говнокод!!!
        else:
            CTableView.keyPressEvent(self, event)
