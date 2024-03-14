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
from PyQt4.QtCore import SIGNAL, QObject


class CDbEntityCache:
    _connected = False

    @classmethod
    def connect(cls):
        if not cls._connected:
            QObject.connect(QtGui.qApp, SIGNAL('dbConnectionChanged(bool)'), cls.onConnectionChanged)
            cls._connected = True


    @classmethod
    def onConnectionChanged(cls, connected):
        cls.purge()
        cls._connected = False
        QObject.disconnect(QtGui.qApp, SIGNAL('dbConnectionChanged(bool)'), cls.onConnectionChanged)


    @classmethod
    def purge(cls):
        pass
