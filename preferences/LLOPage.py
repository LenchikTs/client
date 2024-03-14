# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Страница настроек проверки орфографии
##
#############################################################################

from PyQt4              import QtGui
#from PyQt4.QtCore       import pyqtSignature, QUrl, QDir

from library.Utils      import toVariant, forceString, forceBool
from Ui_LLOPage         import Ui_LLOPage


class CLLOPage (Ui_LLOPage, QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)


    def setProps(self, props):
        lloUrl = forceString(props.get('edtlloUrl', ''))
        self.edtlloUrl.setText(lloUrl)
        
        recipientCode = forceString(props.get('edtRecipientCode', ''))
        self.edtRecipientCode.setText(recipientCode)
        
        recipientName = forceString(props.get('edtRecipientName', ''))
        self.edtRecipientName.setText(recipientName)
        
        isTestMode = forceBool(props.get('chkRecipeTestIsOn', True))
        self.chkRecipeTestIsOn.setChecked(isTestMode)

        lloLogin = forceString(props.get('edtlloLogin', ''))
        self.edtlloLogin.setText(lloLogin)
        
        lloPassword = forceString(props.get('edtlloPassword', ''))
        self.edtlloPassword.setText(lloPassword)

    def getProps(self, props):
        props['edtlloUrl']        = toVariant(self.edtlloUrl.text())
        props['edtRecipientCode'] = toVariant(self.edtRecipientCode.text())
        props['edtRecipientName'] = toVariant(self.edtRecipientName.text())
        props['chkRecipeTestIsOn'] = toVariant(self.chkRecipeTestIsOn.isChecked())
        props['edtlloLogin']       = toVariant(self.edtlloLogin.text())
        props['edtlloPassword']    = toVariant(self.edtlloPassword.text())
