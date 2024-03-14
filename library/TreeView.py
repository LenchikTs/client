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


class CTreeView(QtGui.QTreeView):
    def __init__(self, parent):
        QtGui.QTreeView.__init__(self, parent)
        self.__popupMenu = None

#        h = self.fontMetrics().height()
#        self.verticalHeader().setDefaultSectionSize(3*h/2)
#        self.verticalHeader().hide()
#        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
#        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
#        self.setAlternatingRowColors(True)
#        self.horizontalHeader().setStretchLastSection(True)


    def createPopupMenu(self, actions=[]):
        self.__popupMenu = QtGui.QMenu(self)
        self.__popupMenu.setObjectName('popupMenu')
        for action in actions:
            if isinstance(action, QtGui.QAction):
                self.__popupMenu.addAction(action)
            elif action == '-':
                self.__popupMenu.addSeparator()
#        self.connect(self.__popupMenu, QtCore.SIGNAL('aboutToShow()'), self.popupMenuAboutToShow)
        return self.__popupMenu


    def setPopupMenu(self, menu):
        self.__popupMenu = menu


    def popupMenu(self):
        return self.__popupMenu


    def popupMenuAboutToShow(self):
        pass
#        if self.__actDeleteRow:
#            self.__actDeleteRow.setEnabled(self.model().rowCount()>0)


    def contextMenuEvent(self, event): # event: QContextMenuEvent
        if self.__popupMenu:
            self.__popupMenu.exec_(event.globalPos())
            event.accept()
        else:
            event.ignore()


class CMultiSelectionTreeView(CTreeView):
    def __init__(self, parent):
        CTreeView.__init__(self, parent)
        self.__popupMenu = None
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        #self.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

