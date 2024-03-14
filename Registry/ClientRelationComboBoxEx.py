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
from PyQt4.QtCore import QDate, SIGNAL, Qt

from Registry.ClientRelationComboBox        import CClientRelationComboBox
from Registry.ClientRelationComboBoxPopupEx import CClientRelationComboBoxPopupEx


__all__ = [ 'CClientRelationComboBoxEx',
          ]


class CClientRelationComboBoxEx(CClientRelationComboBox):
    __pyqtSignals__ = ('textChanged(QString)',
                       'textEdited(QString)'
                      )

    def __init__(self, parent = None, mainClientId = None, regAddressInfo = {}, logAddressInfo = {}):
        CClientRelationComboBox.__init__(self, parent, mainClientId, regAddressInfo, logAddressInfo)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self._popup=None
        self.mainClientId = mainClientId
        self.clientId = None
        self.regAddressInfo = regAddressInfo
        self.logAddressInfo = logAddressInfo
        self.date = QDate.currentDate()
        self.installEventFilter(self)


    def showPopup(self):
        if not self._popup:
            self._popup = CClientRelationComboBoxPopupEx(self)
            self.connect(self._popup, SIGNAL('relatedClientIdSelected(int)'), self.setValue)
        pos = self.rect().bottomLeft()
        pos = self.mapToGlobal(pos)
        size = self._popup.sizeHint()
        screen = QtGui.QApplication.desktop().availableGeometry(pos)
        size.setWidth(screen.width())
        pos.setX( max(min(pos.x(), screen.right()-size.width()), screen.left()) )
        pos.setY( max(min(pos.y(), screen.bottom()-size.height()), screen.top()) )
        self._popup.move(pos)
        self._popup.resize(size)
        self._popup.setDate(self.date)
        self._popup.setClientRelationCode(self.clientId, self.mainClientId, self.regAddressInfo, self.logAddressInfo)
        self._popup.regAddressInfo = self.regAddressInfo
        self._popup.logAddressInfo = self.logAddressInfo
        self._popup.on_buttonBox_apply()
        self._popup.show()


    def setClientId(self, clientId):
        self.mainClientId = clientId


    def setValue(self, clientId):
        self.clientId = clientId
        self.updateText()
        self.lineEdit().setCursorPosition(0)


    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            event.ignore()
        elif key == Qt.Key_Return or key == Qt.Key_Enter:
            event.ignore()
        if key == Qt.Key_Delete or key == Qt.Key_Backspace:
            self.setValue(None)
            event.accept()
        else:
            QtGui.QComboBox.keyPressEvent(self, event)

