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
from PyQt4.QtCore import SIGNAL

from library.Utils           import forceRef, forceDate, forceInt
from library.InDocTable      import CInDocTableView
from Events.ActionStatus     import CActionStatus
from Events.ActionEditDialog import CActionEditDialog
from Users.Rights            import urRegTabEditExpertMC


class CMedicalCommissionInDocTableView(CInDocTableView):
    def __init__(self, parent):
        CInDocTableView.__init__(self, parent)
        self.actEditDirectionMC = None


    def addPopupEditDirectionMC(self):
        if self._popupMenu is None:
            self.createPopupMenu()
        self.actEditDirectionMC = QtGui.QAction(u'Редактировать', self) # WTF?
        self.actEditDirectionMC.setObjectName('actEditDirectionMC') # WTF?
        self._popupMenu.addAction(self.actEditDirectionMC)
        self.connect(self.actEditDirectionMC, SIGNAL('triggered()'), self.on_editDirectionMC)


    def on_editDirectionMC(self):
        currentRow = self.currentIndex().row()
        items = self.model().items()
        if currentRow < len(items):
            item = items[currentRow]
            actionId = forceRef(item.value('id'))
            if actionId:
                dialog = CActionEditDialog(self)
                try:
                    dialog.load(actionId)
                    if dialog.exec_():
                        self.model().updateItems()
                        self.model().updateColumnsCaches(actionId)
                        self.model().reset()
                finally:
                    dialog.deleteLater()


    def addPopupDelRow(self):
        if self._popupMenu is None:
            self.createPopupMenu()
        self._CInDocTableView__actDeleteRows = QtGui.QAction(u'Удалить строку', self)
        self._CInDocTableView__actDeleteRows.setObjectName('actDeleteRows')
        self._popupMenu.addAction(self._CInDocTableView__actDeleteRows)
        self.connect(self._CInDocTableView__actDeleteRows, SIGNAL('triggered()'), self.on_deleteCurrentRow)


    def on_deleteCurrentRow(self):
        if QtGui.QMessageBox.question(self,
                u'Удаление документа', u'Вы действительно хотите удалить документ?',
                QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes:
            QtGui.qApp.setWaitCursor()
            try:
                currentRow = self.currentIndex().row()
                items = self.model().items()
                if currentRow < len(items):
                    item = items[currentRow]
                    actionId = forceRef(item.value('id'))
                    if actionId:
                        db = QtGui.qApp.db
                        tableAction = db.table('Action')
                        db.markRecordsDeleted(tableAction, [tableAction['id'].eq(actionId)])
                        self.model().updateColumnsCaches(actionId)
                        self.model().removeRow(currentRow)
            finally:
                QtGui.qApp.restoreOverrideCursor()


    def on_popupMenu_aboutToShow(self):
        CInDocTableView.on_popupMenu_aboutToShow(self)
        hasRight = QtGui.qApp.userHasRight(urRegTabEditExpertMC)
        model = self.model()
        row = self.currentIndex().row()
        rowCount = model.realRowCount() if hasattr(model, 'realRowCount') else model.rowCount()
#        actionTypeId = forceRef(model.items()[row].value('actionType_id'))
#        actionType = CActionTypeCache.getById(actionTypeId) if actionTypeId else None
#        flatCode = actionType.flatCode if actionType else None
#        if flatCode and u'inspection_mse' in flatCode:
#            hasRight = QtGui.qApp.userHasRight(urRegTabEditExpertMSI)
        if self._CInDocTableView__actDeleteRows:
            self._CInDocTableView__actDeleteRows.setText(u'Удалить текущую строку')
            isEnabled = False
            if 0<=row<rowCount:
                items = model.items()
                item = items[row]
                status = forceInt(item.value('status'))
                isEnabled = bool(status not in [CActionStatus.finished, CActionStatus.canceled, CActionStatus.refused])
            self._CInDocTableView__actDeleteRows.setEnabled(isEnabled and hasRight) # WTF?
        if self.actEditDirectionMC:
            isEnabled = False
            if 0<=row<rowCount:
                items = model.items()
                item = items[row]
                endDate = forceDate(item.value('endDate'))
                personId = forceRef(item.value('person_id'))
                isEnabled = bool(not endDate or (endDate and personId == QtGui.qApp.userId))
            self.actEditDirectionMC.setEnabled(isEnabled and hasRight) # WTF?

