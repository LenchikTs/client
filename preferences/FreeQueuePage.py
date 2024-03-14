# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Страница настройки - панель номерки
##
#############################################################################

from PyQt4 import QtGui

from library.Utils            import (
                                         forceInt,
                                         toVariant,
                                     )

from Ui_FreeQueuePage import Ui_freeQueuePage


class CFreeQueuePage(Ui_freeQueuePage, QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)


    def setProps(self, props):
        self.cmbDoubleClickQueueFreeOrder.setCurrentIndex(forceInt(props.get('doubleClickQueueFreeOrder', 0)))


    def getProps(self, props):
        props['doubleClickQueueFreeOrder'] = toVariant(self.cmbDoubleClickQueueFreeOrder.currentIndex())
