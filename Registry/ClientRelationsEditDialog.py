#455046, 728913, 587889, 728944, 522365
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
from PyQt4.QtCore import Qt

from library.DialogBase         import CDialogBase
from library.ItemsListDialog    import CItemEditorBaseDialog
from Registry.ClientEditDialog  import (
#                                         CClientRelationInDocTableCol,
                                         CDirectRelationsModel,
                                         CBackwardRelationsModel,
                                       )

from Registry.Ui_ClientRelationsEditDialog   import Ui_ClientRelationsEditDialog


class CClientRelationsEditDialog(CItemEditorBaseDialog, Ui_ClientRelationsEditDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, 'ClientRelation')
        self.addObject('modelDirectRelations', CDirectRelationsModel(self))
        self.addObject('modelBackwardRelations', CBackwardRelationsModel(self))
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setWindowTitleEx(u'Связи')
        self.setWindowState(Qt.WindowMaximized)
        self.tblDirectRelations.setModel(self.modelDirectRelations)
        self.tblBackwardRelations.setModel(self.modelBackwardRelations)
        self.tblDirectRelations.addPopupDelRow()
        self.tblDirectRelations.addPopupRecordProperies()
        self.tblDirectRelations.addRelativeClientEdit()
        self.tblBackwardRelations.addPopupDelRow()
        self.tblBackwardRelations.addPopupRecordProperies()
        self.tblBackwardRelations.addRelativeClientEdit()
        self.showMaximized()


    def destroy(self):
        self.tblDirectRelations.setModel(None)
        self.tblBackwardRelations.setModel(None)
        del self.modelDirectRelations
        del self.modelBackwardRelations


    def exec_(self):
        if self.lock(self._tableName, self._id):
            try:
                if self._id:
                    self.setRecord(None)
                    self.setIsDirty(False)
                    if not self.checkDataBeforeOpen():
                        return QtGui.QDialog.Rejected
                result = CDialogBase.exec_(self)
            finally:
                self.releaseLock()
        else:
            result = QtGui.QDialog.Rejected
            self.setResult(result)
        return result


    def checkDataEntered(self):
        return True


    def save(self):
        id = self.itemId()
        self.modelDirectRelations.saveItems(id)
        self.modelBackwardRelations.saveItems(id)
        return True


    def setRecord(self, record):
        id = self.itemId()
        self.modelDirectRelations.loadItems(id)
        self.modelDirectRelations.setClientId(id)
        self.modelBackwardRelations.loadItems(id)
        self.modelBackwardRelations.setClientId(id)


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        return record

