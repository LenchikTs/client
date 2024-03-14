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
#import re

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt



class CEventLoopExecutingContext(QtCore.QObject):
    STATUS_STOPPED = 0
    STATUS_WORK = 1

    ACTION_GOON = 0
    ACTION_STOP = 1

    def __init__(self, parent, canStarted=True):
        QtCore.QObject.__init__(self, parent)
        self._parent = parent
        self._inited = False
        self.__canStarted = self._canStarted = canStarted
        self._status = self.STATUS_STOPPED
        self._failed = False
        self.__onStop = None
        self.__onFail = None


    def _init(self, settings, dependencies):
        if not self._inited:
            self._canStarted = self.__canStarted
            self._failed = False
            self._status = self.STATUS_STOPPED
            self._settings = settings
            self._dependencies = dependencies
            self.__onStop = None
            self.__onFail = None
            self._inited = True

    def resetDependincies(self):
        self._dependencies = None

    @property
    def canStarted(self):
        return self._canStarted

    def setCanStarted(self, value):
        self._canStarted = value

    @property
    def failed(self):
        return self._failed

    def __callback(self, target):
        if isinstance(target, (tuple, list)):
            func, args, kwargs = self.__onStop
            return func(*args, **kwargs)
        else:
            return target()

    def _onFail(self):
        self._failed = True
        if self.__onFail is not None:
            return self.__callback(self.__onFail)

    def _onStop(self):
        if self.__onStop is not None:
            return self.__callback(self.__onStop)

    def setOnFail(self, onFail, *args, **kwargs):
        self.__onFail = (onFail, args, kwargs)

    def setOnStop(self, onStop, *args, **kwargs):
        self.__onStop = (onStop, args, kwargs)

    def start(self):
        if not self._dependencies:
            return

        self._status = self.STATUS_WORK
        for w in self._dependencies:
            w.installEventFilter(self)

    def stopEventFilter(self):
        if self._dependencies:
            for w in self._dependencies:
                w.removeEventFilter(self)

    def _removeOnStop(self):
        self.__onStop = None

    def stop(self):
        self._inited = False
        if self._status == self.STATUS_STOPPED:
            return False

        self.stopEventFilter()
        self._onStop()
        self.__onStop = None
        self._status = self.STATUS_STOPPED
        return False

    def isWork(self):
        return self._status == self.STATUS_WORK

    def eventFilter(self, receiver, event):
        result = False
        if self._status == self.STATUS_STOPPED:
            return result
        else:
            try:
                result = self._analyze(receiver, event)
            except:
                self.__onStop = None
                self.stop()
                QtGui.qApp.logCurrentException()
                result = True
        return result

    def _analyze(self, receiver, event):
        eventType = event.type()
        eventTypeSettings = self._settings.get(eventType)
        if eventTypeSettings is None:
            # Если зависимости для данного типа событий None
            # Работаем дальше
            return False

        elif callable(eventTypeSettings):
            return eventTypeSettings(receiver, event)

        elif eventType == QtCore.QEvent.KeyPress:
            return self._analyzeKeyPress(receiver, event, eventTypeSettings)

        # Не сработали реализованные условия, останавливаем контекст выполнения
        return self.stop()

    def _analyzeKeyPress(self, receiver, event, eventTypeSettings):
        modifiers = event.modifiers()
        key = event.key()
        if modifiers | QtCore.Qt.NoModifier == QtCore.Qt.NoModifier:
            key = (key, )
        else:
            key = (key, modifiers)

        todo = eventTypeSettings.get(key)
        if todo is None:
            self.stop()

        elif callable(todo):
            todo = todo()

        if todo == self.ACTION_STOP:
            receiver.event(event)
            self.stop()
            return True

        return False


class CBarCodeActionExecutingContext(CEventLoopExecutingContext):
    def __init__(self, parent, canStarted=True, *dependencies):
        CEventLoopExecutingContext.__init__(self, parent, canStarted)
        if dependencies:
            self.init(*dependencies)

    def init(self, *dependencies):
        self._init({QtCore.QEvent.KeyPress: self._checkKeyPressedValue}, dependencies)

    def _checkKeyPressedValue(self, receiver, event):
        key = event.key()
        keyText = unicode(event.text())

        if key in (Qt.Key_Return, Qt.Key_Enter):
            receiver.event(event)
            event.accept()
            self.stop()
            return True

        elif keyText and keyText != ' ':
            return False

        self.stopEventFilter()
        self._onFail()
        self._status = self.STATUS_STOPPED
        self._removeOnStop()
        return False
