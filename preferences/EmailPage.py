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
## Страница настройки электронной почты
##
#############################################################################

import re

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature

from library.SendMailDialog   import DefaultSMTPPorts
from library.Utils            import (
                                        forceBool,
                                        forceInt,
                                        forceString,
                                        forceStringEx,
                                        toVariant,
                                     )

from Ui_EmailPage import Ui_emailPage


class CEmailPage(Ui_emailPage, QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)


    def setProps(self, props):
        self.edtSMTPServer.setText(forceString(props.get('SMTPServer', '')))
        encryption = max(0, min(2, forceInt(props.get('SMTPEncryption', 0))))
        self.cmbSMTPEncryption.setCurrentIndex(encryption)
        port = forceInt(props.get('SMTPPort', 0))
        self.edtSMTPPort.setValue(port if port>0 else DefaultSMTPPorts[encryption])
        self.edtMailAddress.setText(forceString(props.get('mailAddress', '')))
        self.chkSMTPAuthentification.setChecked(forceBool(props.get('SMTPAuthentification', False)))
        self.edtSMTPLogin.setText(forceString(props.get('SMTPLogin', '')))
        self.edtSMTPPassword.setText(forceString(props.get('SMTPPassword', '')))


    def getProps(self, props):
        encryption = self.cmbSMTPEncryption.currentIndex()
        port       = self.edtSMTPPort.value()

        props['SMTPServer']     = toVariant(forceStringEx(self.edtSMTPServer.text()))
        props['SMTPEncryption'] = toVariant(encryption)
        props['SMTPPort']       = toVariant(port if port>0 else DefaultSMTPPorts[encryption])
        props['mailAddress']    = toVariant(forceStringEx(self.edtMailAddress.text()))
        props['SMTPAuthentification'] = toVariant(self.chkSMTPAuthentification.isChecked())
        props['SMTPLogin']      = toVariant(forceStringEx(self.edtSMTPLogin.text()))
        props['SMTPPassword']   = toVariant(forceStringEx(self.edtSMTPPassword.text()))


    @pyqtSignature('int')
    def on_cmbSMTPEncryption_currentIndexChanged(self, index):
#        global DefaultSMTPPorts

        port = self.edtSMTPPort.value()
        if port == 0 or port in DefaultSMTPPorts:
            self.edtSMTPPort.setValue(DefaultSMTPPorts[index])


    @pyqtSignature('bool')
    def on_chkSMTPAuthentification_clicked(self, checked):
        if checked and self.edtSMTPLogin.text().isEmpty():
            match = re.compile(r'''^(?:.*\s+)?([^\s]+)@''').match(forceString(self.edtMailAddress.text()))
            if match:
                self.edtSMTPLogin.setText(match.group(1))
