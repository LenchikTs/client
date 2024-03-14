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
from PyQt4.QtCore import QVariant

from library.Utils import getPref, setPref

__all__ = ( 'CPreferencesMixin',
            'CContainerPreferencesMixin',
            'CDialogPreferencesMixin',
          )


class CPreferencesMixin:
    def loadPreferences(self, preferences):
        pass

    def savePreferences(self):
        return {}


class CContainerPreferencesMixin(CPreferencesMixin):
    def loadPreferences(self, preferences):
        recursiveLoadPreferences(self, preferences)

    def savePreferences(self):
        return recursiveSavePreferences(self)


class CDialogPreferencesMixin(CContainerPreferencesMixin):
    def loadPreferences(self, preferences):
        geometry = getPref(preferences, 'geometry', None)
        if isinstance(geometry, QVariant) and geometry.type() == QVariant.ByteArray and not geometry.isNull():
            self.restoreGeometry(geometry.toByteArray())
        #        # похоже, что на сборке (qt 4.6.4)
        #        # либо self.windowState() & Qt.WindowMaximized не сохраняется в saveGeometry()
        #        # либо после restoreGeometry не отрабатывается showMaximized()
        #        maximized = getPref(preferences, 'maximized', None)          # for qt 4.6.4 (сборка)
        #        if isinstance(maximized, QVariant) and forceBool(maximized): # for qt 4.6.4 (сборка)
        #            self.showMaximized()                                     # for qt 4.6.4 (сборка)
        # гипотеза №2: в случае qt 4.6.4 (сборка) нехорошо делать self.showMaximized() в конструкторе
        CContainerPreferencesMixin.loadPreferences(self, preferences)

    def savePreferences(self):
        result = CContainerPreferencesMixin.savePreferences(self)
        setPref(result, 'geometry', QVariant(self.saveGeometry()))
        #        setPref(result,'maximized',QVariant((self.windowState() & Qt.WindowMaximized) == Qt.WindowMaximized)) # for qt 4.6.4 (сборка)
        return result


    def loadDialogPreferences(self):
        preferences = getPref(QtGui.qApp.preferences.windowPrefs, self.objectName(), {})
        self.loadPreferences(preferences)


    def saveDialogPreferences(self):
        preferences = self.savePreferences()
        setPref(QtGui.qApp.preferences.windowPrefs, self.objectName(), preferences)



def recursiveLoadPreferences(obj, preferences):
    for child in obj.children():
        childPreferences = getPref(preferences, child.objectName(), {})
        if isinstance(child, CPreferencesMixin):
            child.loadPreferences(childPreferences)
        if isinstance(child, QtGui.QSplitter):
            geometry = getPref(childPreferences, 'geometry', None)
            if type(geometry) == QVariant and geometry.type() == QVariant.ByteArray and not geometry.isNull():
                child.restoreState(geometry.toByteArray())
        recursiveLoadPreferences(child, childPreferences)


def recursiveSavePreferences(obj):
    localPreferences = {}
    for child in obj.children():
        childPreferences = {}
        if isinstance(child, CPreferencesMixin):
            childPreferences = child.savePreferences()
        if isinstance(child, QtGui.QSplitter):
            setPref(childPreferences, 'geometry', QVariant(child.saveState()))

        childPreferences.update(recursiveSavePreferences(child))
        if childPreferences:
            setPref(localPreferences, child.objectName(), childPreferences)
    return localPreferences

