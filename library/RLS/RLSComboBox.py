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
from PyQt4.QtCore import Qt, SIGNAL, QDate

from library.Utils import forceString
from library.RLS.RLSComboBoxPopup import CRLSComboBoxPopup


class CRLSComboBox(QtGui.QComboBox):
    __pyqtSignals__ = ('textChanged(QString)',
                       'textEdited(QString)'
                      )

    def __init__(self, parent = None):
        QtGui.QComboBox.__init__(self, parent)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self._popup=None
        self.code=None
        self.date = QDate.currentDate()


    def showPopup(self):
        if not self._popup:
            self._popup = CRLSComboBoxPopup(self)
            self.connect(self._popup,SIGNAL('RLSCodeSelected(int)'), self.setValue)
        pos = self.rect().bottomLeft()
        pos2 = self.rect().topLeft()
        pos = self.mapToGlobal(pos)
        pos2 = self.mapToGlobal(pos2)
        size = self._popup.sizeHint()
        width= max(size.width(), self.width())
#        size.setWidth(width+20) # magic. похоже, что sizeHint считается неправильно. русские буквы виноваты?
        size.setWidth(width)
        screen = QtGui.QApplication.desktop().availableGeometry(pos)
        pos.setX( max(min(pos.x(), screen.right()-size.width()), screen.left()) )
        pos.setY( max(min(pos.y(), screen.bottom()-size.height()), screen.top()) )
#
##        if (pos.y() + size.height() > screen.bottom()):
##            pos.setY(pos2.y() - size.height())
##        elif (pos.y() < screen.top()):
##            pos.setY(screen.top())
##        if (pos.y() < screen.top()):
##            pos.setY(screen.top())
##        if (pos.y()+size.height() > screen.bottom()):
##            pos.setY(screen.bottom()-size.height())
        self._popup.move(pos)
        self._popup.resize(size)
        self._popup.show()
        self._popup.setDate(self.date)
        self._popup.setRLSCode(self.code)


#    def focusInEvent(self, event):
#        QtGui.QComboBox.focusInEvent(event)
#        self.setCursorPosition(0)


    def setDate(self, date):
        self.date = date


    def setValue(self, code):
        self.code = code
        self.updateText()


    def value(self):
        return self.code


    @staticmethod
    def codeToText(code):
        if code:
            db = QtGui.qApp.db
            table = db.table('rls.vNomen')
            record = db.getRecordEx(table, ['tradeName', 'form', 'dosage', 'filling', 'packing'], table['code'].eq(code))
            if record:
                name = forceString(record.value('tradeName'))
                form = forceString(record.value('form'))
                dosage = forceString(record.value('dosage'))
                filling = forceString(record.value('filling'))
                packing = forceString(record.value('packing'))
                text = ', '.join([field for field in (name, form, dosage, filling, packing) if field])
            else:
                text = '{%s}' % code
        else:
            text = ''
        return text


    def updateText(self):
        self.setEditText(self.codeToText(self.code))


    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Delete:
            self.setValue(None)
            event.accept()
        elif key == Qt.Key_Backspace: # BS
            self.setValue(None)
            event.accept()
        else:
            QtGui.QComboBox.keyPressEvent(self, event)

