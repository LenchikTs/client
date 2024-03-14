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
from PyQt4.QtCore import Qt, SIGNAL


from Ui_LabResultLogWidget import Ui_LabResultLogWidget

class CLabResultLogWidget(QtGui.QWidget, Ui_LabResultLogWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setupUi(self)

        self.edtLog.setReadOnly(True)
        self.setFindVisible(False)

        self.actFind = QtGui.QAction(u'Поиск', self)
        self.actFind.setShortcut(Qt.Key_F7)
        self.addAction(self.actFind)
        self.connect(self.actFind, SIGNAL('triggered()'), self.onActFindTriggered)
        self.connect(self.edtFind, SIGNAL('textEdited(QString)'), self.find)
        self.connect(self.btnNext, SIGNAL('clicked()'), self.findNext)
        self.connect(self.btnPrevious, SIGNAL('clicked()'), self.findPrevious)


    def setFindVisible(self, value):
        self.frmFind.setVisible(value)


    def clear(self):
        self.edtLog.clear()

    def append(self, txt):
        self.edtLog.append(txt)


    def onActFindTriggered(self):
        self.setFindVisible(not self.frmFind.isVisible())

    def findNext(self):
        self._findNext(self.edtFind.text())

    def _findNext(self, txt):
        return self.edtLog.find(txt)

    def _findPrevious(self, txt):
        return self.edtLog.find(txt, QtGui.QTextDocument.FindBackward)

    def findPrevious(self):
        self._findPrevious(self.edtFind.text())

    def find(self, txt):
        if self.edtLog.textCursor().hasSelection():
            self.edtLog.moveCursor(QtGui.QTextCursor.StartOfWord)
        if not self._findNext(txt):
            self._findPrevious(txt)

