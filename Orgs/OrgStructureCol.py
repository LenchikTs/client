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

from library.InDocTable    import CInDocTableCol
from library.Utils         import toVariant, forceInt

from Utils import getOrgStructureName, getOrgStructureFullName
from OrgStructComboBoxes import COrgStructureComboBox


#FIXME: modeldatacache - отсутствует.
class COrgStructureInDocTableCol(CInDocTableCol):
    def __init__(self, title, fieldName, width, **params):
        CInDocTableCol.__init__(self, title, fieldName, width, **params)
        self.filter         = params.get('filter', '')
        self.preferredWidth = params.get('preferredWidth', None)


    def toString(self, val, record):
        return toVariant(getOrgStructureName(val))


    def toStatusTip(self, val, record):
        return toVariant(getOrgStructureFullName(val))


    def createEditor(self, parent):
        editor = COrgStructureComboBox(parent)
        if self.preferredWidth:
            editor.setPreferredWidth(self.preferredWidth)
        return editor


    def setEditorData(self, editor, value, record):
        editor.setValue(forceInt(value))


    def getEditorData(self, editor):
        return toVariant(editor.value())
