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
from PyQt4.QtCore import QVariant, SIGNAL

from library.Utils import getPref, setPref
from library.PreferencesMixin import CContainerPreferencesMixin, CDialogPreferencesMixin


__all__ = ( 'CDockWidget',
          )

class CDockWidget(QtGui.QDockWidget, CDialogPreferencesMixin):
    __pyqtSignals__ = (
        'contentCreated(QDockWidget*)',
        'contentDestroyed(QDockWidget*)',
        'visibilityChanged(QDockWidget*, bool)'
    )

    def __init__(self, parent):
        QtGui.QDockWidget.__init__(self, parent)
#        self._sizeHint = QSize()


    def loadPreferences(self, preferences):
        CContainerPreferencesMixin.loadPreferences(self, preferences)
        floating = getPref(preferences, 'floating', None)
        if floating and type(floating) == QVariant:
            self.setFloating(floating.toBool())
        visible = getPref(preferences, 'visible', None)
        if visible and type(visible) == QVariant:
            self.setVisible(visible.toBool())
#        self.updateGeometry()


    def savePreferences(self):
        result = CContainerPreferencesMixin.savePreferences(self)
        setPref(result,'floating', QVariant(1 if self.isFloating() else 0))
        setPref(result,'visible',  QVariant(1 if self.isVisible() else 0))
        return result
    

    def showEvent(self, event):
        self.emit(SIGNAL('visibilityChanged(QDockWidget*, bool)'), self, True)
    

    def hideEvent(self, event):
        self.emit(SIGNAL('visibilityChanged(QDockWidget*, bool)'), self, False)


#    def setVisible(self, visible):
#        if not visible and self.isVisible():
#            self._sizeHint = self.size()
#        QtGui.QDockWidget.setVisible(self, visible)