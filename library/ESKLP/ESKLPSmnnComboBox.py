# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2023 SAMSON Group. All rights reserved.
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

from library.ESKLP.ESKLPSmnnComboBoxPopup import CESKLPSmnnComboBoxPopup
from library.ROComboBox import CROComboBox
from library.Utils import forceStringEx

__all__ = ['CESKLPSmnnComboBox',
           ]


class CESKLPSmnnComboBox(CROComboBox):
    __pyqtSignals__ = ('textChanged(QString)',
                       'textEdited(QString)'
                       )

    def __init__(self, parent=None):
        CROComboBox.__init__(self, parent)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self._popup = None
        self.UUID = None
        self.installEventFilter(self)

    def showPopup(self):
        if not self._popup:
            self._popup = CESKLPSmnnComboBoxPopup(self)
            self.connect(self._popup, SIGNAL('ESKLPSmnnUUIDSelected(QString)'), self.setValue)
        pos = self.rect().bottomLeft()
        pos = self.mapToGlobal(pos)
        size = self._popup.sizeHint()
        screen = QtGui.QApplication.desktop().availableGeometry(pos)
        size.setWidth(screen.width())
        pos.setX(max(min(pos.x(), screen.right() - size.width()), screen.left()))
        pos.setY(max(min(pos.y(), screen.bottom() - size.height()), screen.top()))
        self._popup.move(pos)
        self._popup.resize(size)
        self._popup.setUUIDESKLPPopupUpdate(self.UUID)
        self._popup.show()

    def setValue(self, UUID):
        self.UUID = UUID
        self.updateText()
        self.lineEdit().setCursorPosition(0)

    def value(self):
        return self.UUID

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

    def text(self):
        return self.lineEdit().text()

    def setText(self, text):
        self.lineEdit().setText(text)

    def updateText(self):
        self.setEditText(self.ESKLPSmnnNameToText(self.UUID))

    def ESKLPSmnnNameToText(self, UUID):
        text = u''
        if UUID:
            db = QtGui.qApp.db
            tableESKLP_Smnn = db.table('esklp.Smnn')
            cols = [tableESKLP_Smnn['mnn']]
            cond = [tableESKLP_Smnn['UUID'].eq(UUID)]
            record = db.getRecordEx(tableESKLP_Smnn, cols, cond)
            if record:
                text = forceStringEx(record.value('mnn'))
        return text
