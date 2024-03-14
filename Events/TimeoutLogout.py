# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import QObject, QTimer, QEvent, Qt


class CTimeoutLogout(QObject):
    def __init__(self, time, obj):
        QObject.__init__(self)
        self.timer = QTimer()
        self.time = time
        self.notAlert = True
        self.timeoutWindow = None
        self.windows = []
        self.windows.append(obj)
        
        
    def eventFilter(self, obj, event):
        if self.notAlert and (event.type() == QEvent.KeyRelease or event.type() == QEvent.MouseButtonRelease or event.type() == QEvent.MouseMove or event.type() == QEvent.ShortcutOverride):
            self.timer.start(self.time)
        if event.type() == QEvent.Show:
            check = getattr(obj, "reject", None)
            if callable(check) and obj not in self.windows:
                self.windows.append(obj)
        elif event.type() == QEvent.Hide:
            if obj in self.windows:
                self.windows.remove(obj)
        return QObject.eventFilter(self, obj, event)
    
    
    def close(self):
        if self.timeoutWindow:
            self.timeoutWindow.done(0)
        for window in reversed(self.windows):
            window.reject()
        self.disconnectAll()
    
    
    def timeoutWindowAlert(self):
        self.timeoutWindow = QtGui.QMessageBox()
        self.timeoutWindow.setWindowFlags(self.timeoutWindow.windowFlags() | Qt.WindowStaysOnTopHint)
        self.timeoutWindow.setText(u'Через 1 минуту обращение будет закрыто из-за отсутствия действий пользователя')
        self.timeoutWindow.setWindowTitle(u'Внимание!')
        self.timeoutWindow.setStandardButtons(QtGui.QMessageBox.Cancel)
        return self.timeoutWindow.exec_()
    
    
    def disconnectAll(self):
        self.timer.timeout.disconnect()
        
        
    def timerActivate(self, func, time = None, notAlert = True):
        self.timer.timeout.connect(func)
        if time: self.timer.start(time)
        else: self.timer.start(self.time)
        if notAlert: self.notAlert = notAlert
        else: self.notAlert = notAlert