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
from PyQt4.QtCore import SIGNAL, QEvent

from library.adjustPopup import adjustPopupToWidget


__all__ = [ 'CCustomComboBoxLike',
          ]


class CCustomComboBoxLike(QtGui.QComboBox):
    __pyqtSignals__ = ('editingFinished()',
                      )

    def __init__(self, parent = None):
        QtGui.QComboBox.__init__(self, parent)
        self.addItem('')
        self.setCurrentIndex(0)
        self._popup = None
        self._deletePopupOnClose = True
        self._value = None
        self._valueIdDict = {}


    def setValue(self, value):
        self._value = value[0]
        self._valueIdDict = value[1]
        self.setItemText(0, self.valueAsString(self._value))


    def getValue(self):
        return self._value, self._valueIdDict


    def createPopup(self):
        return None


    def valueAsString(self, value):
        return unicode(value)


    def setValueToPopup(self):
        pass


    def showPopup(self):
        if self._popup is None:
            self._popup = self.createPopup()
        self._popup.installEventFilter(self)
        adjustPopupToWidget(self, self._popup)
        self.setValueToPopup()
        self._popup.show()
        self._popup.setFocus()


    def eventFilter(self, obj, event):
        if event.type() == QEvent.Close:
            self.hidePopup()
            return True
        return QtGui.QComboBox.eventFilter(self, obj, event)


    def hidePopup(self):
        if self._popup and self._popup.isVisible():
            self._popup.removeEventFilter(self)
            self._popup.close()
            if self._deletePopupOnClose:
                if self._popup:
                    self._popup.deleteLater()
                self._popup = None
        QtGui.QComboBox.hidePopup(self)
        self.setFocus()
        self.emit(SIGNAL('editingFinished()'))
