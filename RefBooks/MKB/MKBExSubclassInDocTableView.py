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

#from PyQt4 import QtGui, QtSql
#from PyQt4.QtCore import Qt

from library.InDocTable import CInDocTableView, CLocItemDelegate


class CExSubclassItemDelegate(CLocItemDelegate):
    def __init__(self, parent, tableName='rbMKBExSubclass', addNone=True):
        CLocItemDelegate.__init__(self, parent)
        self.tableName = tableName
        self.addNone = addNone


    def createEditor(self, parent, option, index):
        editor = CLocItemDelegate.createEditor(self, parent, option, index)
        if editor is not None:
            row    = index.row()
            model  = index.model()
            if 0 <= row < len(model.items()):
                editor.setTable(self.tableName, addNone=self.addNone, filter='position = %d'%(row+6))
        return editor


class CMKBExSubclassInDocTableView(CInDocTableView):
    def __init__(self, parent):
        CInDocTableView.__init__(self, parent)
        self.setItemDelegate(CExSubclassItemDelegate(self))


