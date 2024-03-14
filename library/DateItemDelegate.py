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

from library.DateEdit import CDateEdit


class CDateItemDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        editor = CDateEdit(parent)
        return editor

    def setEditorData(self, editor, index):
        model = index.model()
        data = model.data(index, Qt.EditRole)
        editor.setDate(data.toDate())

    def setModelData(self, editor, model, index):
        model.setData(index, QVariant(editor.date()))
