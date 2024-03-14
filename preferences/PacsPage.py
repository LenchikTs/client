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
## Страница настройки соединения с PACS
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature

#from library.Pacs.RestToolbox import checkPacsConnection
from library.Utils            import (
                                         forceInt,
                                         forceString,
                                         toVariant,
                                     )

from Ui_PacsPage import Ui_pacsPage


class CPacsPage(Ui_pacsPage, QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)


    def setProps(self, props):
        self.cmbPacsType.setCurrentIndex(forceInt(props.get('pacsType')))
        self.edtPacsParams.setText(forceString(props.get('pacsParams')))
        self.edtPacsWado.setText(forceString(props.get('pacsWado')))

        pacsType = forceInt(props.get('pacsType'))
        self.edtPacsWado.setEnabled(pacsType == 1)
        self.lblPacsWado.setEnabled(pacsType == 1)


    def getProps(self, props):
        props['pacsType']   = toVariant(self.cmbPacsType.currentIndex())
        props['pacsParams'] = toVariant(self.edtPacsParams.text())
        props['pacsWado']   = toVariant(self.edtPacsWado.text())


    @pyqtSignature('int')
    def on_cmbPacsType_currentIndexChanged(self, pacsType):
        self.edtPacsWado.setEnabled(pacsType == 1)
        self.lblPacsWado.setEnabled(pacsType == 1)


#    @pyqtSignature('')
#    def on_btnCheckPacs_clicked(self):
#        addr = forceString(self.edtPacsAddress.text())
#        port = forceString(self.edtPacsPort.value())
#        authNeeded = self.grpPacsAutentification.isChecked()
#        login = None
#        password = None
#        if authNeeded:
#            login = forceString(self.edtPacsLogin.text())
#            password = forceString(self.edtPacsPassword.text())
#        message = u'Успешно' if checkPacsConnection('%s:%s'%(addr, port), login, password) else u'Ошибка'
#
#        QtGui.QMessageBox.information(self, u'Проверка соединения',
#                message, QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
