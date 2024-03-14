# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from library.InDocTable import CInDocTableView
from library.Utils      import toVariant, copyFields


class CInventoryInDocTableView(CInDocTableView):
    def __init__(self, parent):
        CInDocTableView.__init__(self, parent)


    def on_duplicateCurrentRow(self):
        currentRow = self.currentIndex().row()
        items = self.model().items()
        if currentRow < len(items):
            newRecord = self.model().getEmptyRecord()
            copyFields(newRecord, items[currentRow])
            newRecord.setValue(self.model()._idFieldName, toVariant(None))
            newRecord.setValue('oldQnt', toVariant(0))
            newRecord.setValue('oldPrice', toVariant(0))
            newRecord.setValue('oldSum', toVariant(0))
            self.model().insertRecord(currentRow+1, newRecord)

