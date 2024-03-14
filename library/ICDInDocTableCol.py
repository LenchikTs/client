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

from library.ICDUtils       import getMKBName
from library.InDocTable     import CInDocTableCol
from library.ICDCodeEdit    import CICDCodeEdit, CICDCodeEditEx

from library.Utils          import forceString, trim


u"""Столбики для редактирования кодов МКБ"""



class CICDInDocTableCol(CInDocTableCol):
    def __init__(self, title, fieldName, width, **params):
        CInDocTableCol.__init__(self, title, fieldName, width, **params)
        self.cache = {}


    def createEditor(self, parent):
        editor = CICDCodeEdit(parent)
        return editor


    def getEditorData(self, editor):
        text = trim(editor.text())
        if text.endswith('.'):
            text = text[0:-1]
        if not text:
            return QVariant()
        return QVariant(text)


    def toStatusTip(self, val, record):
        code = forceString(val)
        if self.cache.has_key(code):
            descr = self.cache[code]
        else:
            descr = getMKBName(code) if code else ''
            self.cache[code] = descr
        return QVariant((code+': '+descr) if code else '')


class CICDExInDocTableCol(CICDInDocTableCol):
    def createEditor(self, parent):
        editor = CICDCodeEditEx(parent)
        return editor
