# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Настройки соединения с базой данных
##
#############################################################################

from PyQt4 import QtGui

from preferences.Ui_connection import Ui_connectionDialog


class CConnectionDialog(QtGui.QDialog, Ui_connectionDialog):

    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)


    def setDriverName(self, val):
        self.cmbDriverName.setCurrentIndex(0 if val == 'mysql' else 1)


    def driverName(self):
        if self.cmbDriverName.currentIndex() == 0:
            return 'mysql'
        else:
            return 'postgres'


    def setServerName(self, val):
        self.edtServerName.setText(val)


    def serverName(self):
        return unicode(self.edtServerName.text()).strip()


    def setServerPort(self, val):
        self.edtServerPort.setValue(val)


    def serverPort(self):
        return self.edtServerPort.value()


    def setDatabaseName(self, val):
        self.edtDatabaseName.setText(val)


    def databaseName(self):
        return unicode(self.edtDatabaseName.text()).strip()


    def setCompressData(self, val):
        self.chkCompressData.setChecked(bool(val))


    def compressData(self):
        return self.chkCompressData.isChecked()


    def setUserName(self, val):
        self.edtUserName.setText(val)


    def userName(self):
        return unicode(self.edtUserName.text()).strip()


    def setPassword(self, val):
        self.edtPassword.setText(val)


    def password(self):
        return unicode(self.edtPassword.text()).strip()
