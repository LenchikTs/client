# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2022 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4          import QtGui
from PyQt4.QtCore   import Qt
from library.Utils  import forceString


class CVaccinationTypeComboBox(QtGui.QComboBox):
    def __init__(self, parent=None):
        QtGui.QComboBox.__init__(self, parent)
        self._tableName = 'rbVaccine_Schema'
        self._filter = ''
        self.__searchString = ''
        self._select()


    def setTable(self, tableName='rbVaccine_Schema', filter=''):
        assert QtGui.qApp.db.table(tableName).hasField('vaccinationType')
        self._tableName = tableName
        self.setFilter(filter)


    def tableName(self):
        return self._tableName


    def _select(self):
        stmt = 'SELECT DISTINCT vaccinationType FROM ' + self._tableName
        if self._filter:
            stmt += ' WHERE ' + self._filter
        stmt += ' ORDER BY vaccinationType'
        query = QtGui.qApp.db.query(stmt)
        self.clear()
        while query.next():
            self.addItem(forceString(query.value(0)))


    def text(self):
        return forceString(self.currentText())


    def setText(self, text):
        self.__searchString = text
        self.lookup()
        self.__searchString = ''


    def keyPressEvent(self, event):
        key = event.key()
        if key in (Qt.Key_Escape, Qt.Key_Return, Qt.Key_Enter):
            event.ignore()
        if key in (Qt.Key_Delete, Qt.Key_Clear):
            self.__searchString = ''
            self.setCurrentIndex(0)
            event.accept()
        elif key == Qt.Key_Backspace:
            self.__searchString = self.__searchString[:-1]
            self.lookup()
            event.accept()
        elif key == Qt.Key_Space:
            QtGui.QComboBox.keyPressEvent(self, event)
        elif not event.text().isEmpty():
            char = event.text().at(0)
            if char.isPrint():
                self.__searchString += unicode(char).upper()
                self.lookup()
                event.accept()
            else:
                QtGui.QComboBox.keyPressEvent(self, event)
        else:
            QtGui.QComboBox.keyPressEvent(self, event)


    def lookup(self):
        i = self.findText(self.__searchString, Qt.MatchStartsWith)
        if i >= 0 and i != self.currentIndex():
            self.setCurrentIndex(i)


    def setFilter(self, filter):
        self._filter = forceString(filter)
        self._select()


    def filter(self):
        return self._filter

