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
##
## Поддержка MDI:
##    - рисование картинки
##    - лучшее отслеживание закрытия mdi child
##
#############################################################################


from PyQt4 import QtGui
from PyQt4.QtCore import Qt, SIGNAL, QEvent, QObject

# как оказалось через CMdiArea.eventFilter идёт большой поток обращений,
# и что удивительно идут обращения от не только от детей, но и от внуков/правнуков,
# которых на первый взгляд не подписывали на installEventFilter

class CMdiSubwindowEventFilter(QObject):
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Show:
            self.parent().emitSubwindowShow(obj)
        if event.type() == QEvent.Close:
            self.parent().emitSubwindowClose(obj)
        return False


class CMdiArea(QtGui.QMdiArea):
    __pyqtSignals__ = (
        'mdiSubwindowShow(QWidget*)',
        'mdiSubwindowClose(QWidget*)',
    )
    def __init__(self, parent = None):
        QtGui.QMdiArea.__init__(self, parent)
        self.__eventFilterObject = CMdiSubwindowEventFilter(self)

# as default:
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
#        self.setViewMode(QtGui.QMdiArea.SubWindowView)

        self._bgPixmap = None
        self._bgPosition = 0
        self._bgFitSize = False


    def addSubWindow(self, widget, windowFlags=0):
        subwindow = QtGui.QMdiArea.addSubWindow(self, widget, windowFlags)
        subwindow.installEventFilter(self.__eventFilterObject)
        return subwindow


    def emitSubwindowShow(self, subwindow):
        if isinstance(subwindow, QtGui.QMdiSubWindow):
            self.emit(SIGNAL('mdiSubwindowShow(QWidget*)'), subwindow.widget())


    def emitSubwindowClose(self, subwindow):
        if isinstance(subwindow, QtGui.QMdiSubWindow):
            self.emit(SIGNAL('mdiSubwindowClose(QWidget*)'), subwindow.widget())


    def setBackground(self, params):
        imagePath = params.get('image', None)
        size      = params.get('size', None)
        position  = params.get('position', None)

        if imagePath:
            self._bgPixmap = QtGui.QPixmap(imagePath)
            if size:
                try:
                    size = size.split(',')
                    if len(size) > 1:
                        widWidth = int(size[0])
                        widHeight = int(size[1])
                        aspectRatio = Qt.IgnoreAspectRatio
                        if len(size) == 3:
                            aspectRatio = Qt.KeepAspectRatio
                        self._bgPixmap = self._bgPixmap.scaled(widWidth, widHeight, aspectRatio, Qt.SmoothTransformation)
                    else:
                        if size[0] == 'max':
                            self._bgFitSize = True
                        else:
                            size = int(size[0])
                            if size>0:
                                w = self._bgPixmap.width()
                                h = self._bgPixmap.height()
                                rw = w*size/100
                                rh = h*size/100
                                self._bgPixmap = self._bgPixmap.scaled(rw, rh, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                except:
                    pass

            if position == 'center':
                self._bgPosition = 1
            elif position == 'topRight':
                self._bgPosition = 2
            elif position == 'bottomRight':
                self._bgPosition = 3
            elif position == 'bottomLeft':
                self._bgPosition = 4


    def paintEvent(self, event):
        QtGui.QMdiArea.paintEvent(self, event)
        if self._bgPixmap:
            pixmap = self._bgPixmap
            if self._bgFitSize:
                w = self.width()
                h = self.height()
                pixmap = self._bgPixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            rectOfPixmap = pixmap.rect()
            if self._bgPosition == 1:
                direction = self.rect().center()
                rectOfPixmap.moveCenter(direction)
            if self._bgPosition == 2:
                direction = self.rect().topRight()
                rectOfPixmap.moveTopRight(direction)
            if self._bgPosition == 3:
                direction = self.rect().bottomRight()
                rectOfPixmap.moveBottomRight(direction)
            if self._bgPosition == 4:
                direction = self.rect().bottomLeft()
                rectOfPixmap.moveBottomLeft(direction)
            painter = QtGui.QPainter(self.viewport())
            painter.drawPixmap(rectOfPixmap.topLeft(), pixmap)


    # это от отчаяния, а по сути исправление пары ошибок в Qt:
    # - QComboBox заедает ctrl+tab, хотя на мой взгляд это как-то нелогично
    # - MdiArea напрочь выносит обработку ctrl+tab в QTabWidget
    # с большим удовольствием ликвидирую...
    def eventFilter(self, obj, event):
        if (     event.type() in ( QEvent.KeyPress, QEvent.KeyRelease)
             and event.key() in (Qt.Key_Tab, Qt.Key_Backtab)
           ):
            modifiers = event.modifiers()
            if not modifiers & ~Qt.ShiftModifier: # [sS]cam
                return False # таб пусть обрабатывает как знает

            if (    isinstance(obj, QtGui.QComboBox) # это комбо-бокс
                and modifiers & ~Qt.ShiftModifier == Qt.ControlModifier # [sS]Cam
               ):
                parent = obj.parent()
                if parent is not None:
                    parent.event(event)
                    return True
                return False

            if modifiers & ~Qt.ShiftModifier == Qt.ControlModifier: # [sS]Cam
                return False # отдайте нам наш ctrl+tab!
        return QtGui.QMdiArea.eventFilter(self, obj, event)

