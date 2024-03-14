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
from PyQt4.QtCore import Qt, SIGNAL, QString
from library.TableView import CTableView


class CKLADRTreeView(QtGui.QTreeView):
    def __init__(self, parent):
        QtGui.QTreeView.__init__(self, parent)
        self.header().hide()
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.connect(self, SIGNAL('expanded(QModelIndex)'), self.onExpanded)
#        self.connect(self, SIGNAL('collapsed(QModelIndex)'), self.onCollapsed)
        self.searchString = ''
        self.searchParent = None

    def setRootIndex(self, index):
        pass

    def onExpanded(self, index):
        self.scrollTo(index, QtGui.QAbstractItemView.PositionAtTop)
#        self.searchString = ''

#    def onCollapsed(self, index):
#        self.searchString = ''


#    def resizeEvent(self, AResizeEvent):
#        QtGui.QTreeView.resizeEvent(self, AResizeEvent)
#        self.resizeColumnToContents(0)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left or event.key() == Qt.Key_Minus:
            current = self.currentIndex()
            if self.isExpanded(current) and self.model().rowCount(current):
                self.collapse(current)
            else:
                self.setCurrentIndex(current.parent())
                current = self.currentIndex()
                self.collapse(current)
                self.scrollTo(current, QtGui.QAbstractItemView.PositionAtTop)
            event.accept()
            return
        if event.key() == Qt.Key_Right or event.key() == Qt.Key_Plus:
            current = self.currentIndex()
            if not self.isExpanded(current) and self.model().rowCount(current):
                self.expand(current)
            event.accept()
            return
        if event.key() == Qt.Key_Backspace:
            self.searchString = self.searchString[:-1]
            self.keyboardSearchBase(self.searchString)
            event.accept()
            return
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            event.accept()
            self.emit(SIGNAL('doubleClicked(QModelIndex)'), self.currentIndex())
            return
        return QtGui.QTreeView.keyPressEvent(self, event)


    def keyboardSearch(self, search):
        current = self.currentIndex()
        if self.searchParent != current.parent():
            self.searchString = u''
            self.searchParent = current.parent()
        self.keyboardSearchBase(self.searchString + unicode(search).upper())


    def keyboardSearchBase(self, searchString):
#        print len(searchString)
        found = self.model().keyboardSearch(self.searchParent, searchString)
        if found.isValid():
            if self.currentIndex() != found or len(self.searchString) > len(searchString):
                self.setCurrentIndex(found)
                self.searchString = searchString


class CKLADRSearchResult(CTableView):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            event.accept()
            self.emit(SIGNAL('doubleClicked(QModelIndex)'), self.currentIndex())
        else:
            CTableView.keyPressEvent(self, event)


class CStreetListView(QtGui.QListView):
    def __init__(self, parent):
        QtGui.QListView.__init__(self, parent)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.searchString = ''


    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Delete:
            self.searchString = ''
            self.keyboardSearchBase('')
            event.accept()
            return
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            event.accept()
            self.emit(SIGNAL('doubleClicked(QModelIndex)'), self.currentIndex())
            return
        if event.key() == Qt.Key_Backspace:
            self.searchString = self.searchString[:-1]
            self.keyboardSearchBase(self.searchString)
            event.accept()
            return
        elif not event.text().isEmpty():
            char = event.text().at(0)
            if char.isPrint():
                self.searchString = self.searchString + unicode(QString(char)).upper()
                self.keyboardSearchBase(self.searchString)
                event.accept()
                return
        else:
            return QtGui.QListView.keyPressEvent(self, event)
        return QtGui.QListView.keyPressEvent(self, event)
    

    def keyboardSearchBase(self, searchString):
        found = self.model().searchStreet(searchString)
        if found[0].row()>0 and self.currentIndex() != found[0]:
            self.setCurrentIndex(found[0])
            self.searchString = searchString
            if found[2] == 1:
               self.emit(SIGNAL('doubleClicked(QModelIndex)'), self.currentIndex()) 
        elif found[0].row() <= 0:
            self.searchString = self.searchString[-1]
            self.keyboardSearchBase(self.searchString)


class CStreetSearchResult(CTableView):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            event.accept()
            self.emit(SIGNAL('doubleClicked(QModelIndex)'), self.currentIndex())
        else:
            CTableView.keyPressEvent(self, event)