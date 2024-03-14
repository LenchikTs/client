#!/usr/bin/env python
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

from Blank.BlankComboBoxPopup import ( CBlankComboBoxPopup,
                                       CBlankComboBoxActionsPopup,
                                       CBlankNumberComboBoxActionsPopup,
                                       CBlankSerialNumberComboBoxActionsPopup,
                                       codeToTextForBlank,
                                       codeToTextForBlankNumber,
                                       codeToTextForBlankSerialNumber,
                                     )
from library.ROComboBox import CROComboBox

class CBlankComboBox(CROComboBox):
    __pyqtSignals__ = ('textChanged(QString)',
                       'textEdited(QString)'
                      )

    def __init__(self, parent = None, blankIdList = [], docTypeActions = False):
        CROComboBox.__init__(self, parent)
        self.setEditable(True)
        self.lineEdit().setReadOnly(False)
        self._popup = None
        self.code = None
        self.blankIdList = blankIdList
        self.docTypeActions = docTypeActions


    def showPopup(self):
        if not self.isReadOnly():
            if not self._popup:
                self._popup = CBlankComboBoxPopup(self, self.docTypeActions)
                self.connect(self._popup,SIGNAL('BlankCodeSelected(int)'), self.setValue)
            pos = self.rect().bottomLeft()
            pos = self.mapToGlobal(pos)
            size = self._popup.sizeHint()
            screen = QtGui.QApplication.desktop().availableGeometry(pos)
            size.setWidth(screen.width())
            pos.setX( max(min(pos.x(), screen.right()-size.width()), screen.left()) )
            pos.setY( max(min(pos.y(), screen.bottom()-size.height()), screen.top()) )
            self._popup.move(pos)
            self._popup.resize(size)
            self._popup.setBlankIdList(self.blankIdList, self.code)
            self._popup.show()


    def setValue(self, code):
        self.code = code
        self.updateText()


    def value(self):
        return self.code


    def setText(self, text):
        self.lineEdit().setText(text)


    def setCursorPosition(self, position):
        self.lineEdit().setCursorPosition(position)


    def text(self):
        return self.lineEdit().text()


    def updateText(self):
        self.setEditText(codeToTextForBlank(self.code))


    def setTempInvalidBlankIdList(self, blankIdList):
        self.blankIdList = blankIdList


    def keyPressEvent(self, event):
        if self.model().isReadOnly():
            event.accept()
        else:
            key = event.key()
            if key == Qt.Key_Delete:
                self.setValue(None)
                event.accept()
            elif key == Qt.Key_Backspace: # BS
                self.setValue(None)
                event.accept()
            else:
                CROComboBox.keyPressEvent(self, event)


class CBlankComboBoxActions(CROComboBox):
    __pyqtSignals__ = ('textChanged(QString)',
                       'textEdited(QString)'
                      )

    def __init__(self, parent = None, blankIdList = [], docTypeActions = False):
        CROComboBox.__init__(self, parent)
        self.setEditable(True)
        self.lineEdit().setReadOnly(False)
        self._popup = None
        self.code = None
        self.blankIdList = blankIdList
        self.docTypeActions = docTypeActions


    def showPopup(self):
        if not self.isReadOnly():
            if not self._popup:
                self._popup = CBlankComboBoxActionsPopup(self, self.docTypeActions)
                self.connect(self._popup,SIGNAL('BlankCodeSelected(QString)'), self.setValue)
            pos = self.rect().bottomLeft()
            pos2 = self.rect().topLeft()
            pos = self.mapToGlobal(pos)
            pos2 = self.mapToGlobal(pos2)
            size = self._popup.sizeHint()
            width= max(size.width(), self.width())
            size.setWidth(width)
            screen = QtGui.QApplication.desktop().availableGeometry(pos)
            pos.setX( max(min(pos.x(), screen.right()-size.width()), screen.left()) )
            pos.setY( max(min(pos.y(), screen.bottom()-size.height()), screen.top()) )
            self._popup.move(pos)
            self._popup.resize(size)
            self._popup.show()
            self._popup.setBlankIdList(self.blankIdList, None)


    def setValue(self, code):
        self.code = code
        self.setText(self.code)
        self.code = None


    def value(self):
        if self.code:
            return self.code
        else:
            return self.text()


    def setText(self, text):
        self.lineEdit().setText(text)


    def setCursorPosition(self, position):
        self.lineEdit().setCursorPosition(position)


    def text(self):
        return self.lineEdit().text()


    def updateText(self):
        self.setEditText(codeToTextForBlank(self.code))


    def setTempInvalidBlankIdList(self, blankIdList):
        self.blankIdList = blankIdList


class CBlankNumberComboBoxActions(CBlankComboBoxActions):

    def showPopup(self):
        if not self.isReadOnly():
            if not self._popup:
                self._popup = CBlankNumberComboBoxActionsPopup(self, self.docTypeActions)
                self.connect(self._popup, SIGNAL('BlankCodeSelected(QString)'), self.setValue)
            pos = self.rect().bottomLeft()
            pos2 = self.rect().topLeft()
            pos = self.mapToGlobal(pos)
            pos2 = self.mapToGlobal(pos2)
            size = self._popup.sizeHint()
            width= max(size.width(), self.width())
            size.setWidth(width)
            screen = QtGui.QApplication.desktop().availableGeometry(pos)
            pos.setX( max(min(pos.x(), screen.right()-size.width()), screen.left()) )
            pos.setY( max(min(pos.y(), screen.bottom()-size.height()), screen.top()) )
            self._popup.move(pos)
            self._popup.resize(size)
            self._popup.show()
            self._popup.setBlankIdList(self.blankIdList, None)

    def updateText(self):
        self.setEditText(codeToTextForBlankNumber(self.code))



class CBlankSerialNumberComboBoxActions(CBlankComboBoxActions):
    readOnly = False

    def showPopup(self):
        if not self.isReadOnly():
            if not self._popup:
                self._popup = CBlankSerialNumberComboBoxActionsPopup(self, self.docTypeActions)
                self.connect(self._popup, SIGNAL('BlankCodeSelected(QString)'), self.setValue)
            pos = self.rect().bottomLeft()
            pos2 = self.rect().topLeft()
            pos = self.mapToGlobal(pos)
            pos2 = self.mapToGlobal(pos2)
            size = self._popup.sizeHint()
            width= max(size.width(), self.width())
            size.setWidth(width)
            screen = QtGui.QApplication.desktop().availableGeometry(pos)
            pos.setX( max(min(pos.x(), screen.right()-size.width()), screen.left()) )
            pos.setY( max(min(pos.y(), screen.bottom()-size.height()), screen.top()) )
            self._popup.move(pos)
            self._popup.resize(size)
            self._popup.show()
            self._popup.setBlankIdList(self.blankIdList, None)

    def updateText(self):
        self.setEditText(codeToTextForBlankSerialNumber(self.code))


