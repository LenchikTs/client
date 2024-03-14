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

from library.Utils import forceStringEx, toVariant
from Events.MedicalDiagnosisComboBoxPopup import CMedicalDiagnosisComboBoxPopup


class CMedicalDiagnosisComboBox(QtGui.QComboBox):
    __pyqtSignals__ = ('textChanged(QString)',
                       'textEdited(QString)'
                      )

    def __init__(self, parent, eventId, date=None):
        QtGui.QComboBox.__init__(self, parent)
        self.setEditable(True)
        self.lineEdit().setReadOnly(False)
        self._popup = None
        self.eventId = eventId
        self.date = date
        self.property = u''


    def showPopup(self):
        if not self._popup:
            self._popup = CMedicalDiagnosisComboBoxPopup(self, self.eventId, self.date)
            self.connect(self._popup, SIGNAL('medicalDiagnosisSelected(QString)'), self.setText)
        pos = self.rect().bottomLeft()
        pos = self.mapToGlobal(pos)
        size = self._popup.sizeHint()
        screen = QtGui.QApplication.desktop().availableGeometry(pos)
        size.setWidth(screen.width())
        size.setHeight(screen.height()-pos.y())
        pos.setX( max(min(pos.x(), screen.right()-size.width()), screen.left()) )
        pos.setY( max(min(pos.y(), screen.bottom()-size.height()), screen.top()) )
        self._popup.move(pos)
        self._popup.resize(size)
        self._popup.show()


    def setDate(self, date):
        return self.date


    def setValue(self, value):
        self.property = value
        self.setText(self.property)


    def value(self):
        if self.property:
            return self.property
        else:
            return self.text()


    def setText(self, value):
        self.property = forceStringEx(value)
        self.lineEdit().setText(self.property)


    def text(self):
        self.property = forceStringEx(self.lineEdit().text())
        return toVariant(self.property)

