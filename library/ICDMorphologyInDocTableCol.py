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

from PyQt4.QtCore import QVariant

from library.ICDMorphologyCodeEdit import CICDMorphologyCodeEditEx
from library.InDocTable            import CCodeRefInDocTableCol
from library.Utils                 import forceString


class CMKBMorphologyCol(CCodeRefInDocTableCol):
    def __init__(self, title, fieldName, width, tableName, **params):
        CCodeRefInDocTableCol.__init__(self, title, fieldName, width, tableName, **params)
        self.filterCache = {}
    

    def createEditor(self, parent):
        editor = CICDMorphologyCodeEditEx(parent)
        editor.setTable(self.tableName, addNone=self.addNone, filter=self.filter)
        editor.setShowFields(self.showFields)
        editor.setPreferredWidth(self.preferredWidth)
        return editor
        

    def getEditorData(self, editor):
        return QVariant(editor.text())
        

    def setEditorData(self, editor, value, record):
        MKB = forceString(record.value('MKB'))
        if bool(MKB):
            filter = self.filterCache.get(MKB, None)
            if not filter:
                filter = editor.getMKBFilter(MKB)
                self.filterCache[MKB] = filter
#            editor.setMKBFilter(self.tableName, addNone=self.addNone, filter=filter)
            editor.setMKBFilter(filter)
        editor.setText(forceString(value))
