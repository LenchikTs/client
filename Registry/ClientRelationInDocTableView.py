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

from library.InDocTable import CInDocTableView
from library.Utils      import forceBool, forceInt
from Users.Rights       import urAdmin, urRegTabWriteRegistry, urRegTabReadRegistry

__all__ = [ 'CClientRelationInDocTableView',
          ]

class CClientRelationInDocTableView(CInDocTableView):
    def __init__(self, parent):
        CInDocTableView.__init__(self, parent)
        self.__actRelativeClientEdit = None


    def addRelativeClientEdit(self):
        if self._popupMenu is None:
            self.createPopupMenu()
        self.__actRelativeClientEdit = QtGui.QAction(u'Регистрационная карточка связанного пациента', self)
        self.__actRelativeClientEdit.setObjectName('actRelativeClientEdit')
        self._popupMenu.addAction(self.__actRelativeClientEdit)
        self.connect(self.__actRelativeClientEdit, SIGNAL('triggered()'), self.showRelativeClientEdit)


    def showRelativeClientEdit(self):
        from Registry.ClientEditDialog  import CClientEditDialog
        row = self.currentIndex().row()
        #column = self.currentIndex().column()
        items = self.model().items()
        value = items[row].value(1) if row < len(items) else None
        if value and value.isValid() and QtGui.qApp.userHasAnyRight([urAdmin, urRegTabWriteRegistry, urRegTabReadRegistry]):
            QtGui.qApp.setWaitCursor()
            try:
                dialog = CClientEditDialog(self)
                dialog.tabWidget.setTabEnabled(7, False) # ;(
                dialog.tabRelations.setEnabled(False)
            finally:
                QtGui.qApp.restoreOverrideCursor()
            try:
                dialog.load(forceInt(value))
                dialog.exec_()
            finally:
                dialog.deleteLater()


    def createPopupMenu(self, actions=[]):
        self._popupMenu = QtGui.QMenu(self)
        self._popupMenu.setObjectName('popupMenu')
        self.connect(self._popupMenu, SIGNAL('aboutToShow()'), self.on_popupMenuShow)
        for action in actions:
            if isinstance(action, QtGui.QAction):
                self._popupMenu.addAction(action)
            elif action == '-':
                self._popupMenu.addSeparator()
        return self._popupMenu


    def on_popupMenuShow(self):
        if self.__actRelativeClientEdit:
            row = self.currentIndex().row()
            rowCount = len(self.model().items())
            column = self.currentIndex().column()
            items = self.model().items()
            value = items[row].value(column) if row < len(items) else None
            self.__actRelativeClientEdit.setEnabled(forceBool(0 <= row < rowCount and (value and value.isValid())))
        self.on_popupMenu_aboutToShow()
