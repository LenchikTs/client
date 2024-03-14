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

from library.crbcombobox import CRBComboBox, CRBModelDataCache
from library.TableModel  import CCol
from library.Utils       import forceRef, forceString, toVariant


class CActionTypeCol(CCol):
#    """
#      ActionType column for list of Actions
#    """
    def __init__(self, title, defaultWidth, showFields=CRBComboBox.showName, alignment='l'):
        CCol.__init__(self, title, ('actionType_id', 'specifiedName'), defaultWidth, alignment)
        self.data = CRBModelDataCache.getData('ActionType', True, '')
        self.showFields = showFields


    def format(self, values):
        id = forceRef(values[0])
        specifiedName = forceString(values[1])
        text = self.data.getStringById(id, self.showFields)
        if id:
            return toVariant(forceString(text) + (' ' + specifiedName if specifiedName else ''))
        else:
            return CCol.invalid
