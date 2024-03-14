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

from PyQt4.QtCore import pyqtSignature

from library.DialogBase import CDialogBase

from Ui_TNMSComboBoxTest import Ui_TestDialog

__all__ = ( 'testTNMSComboBox',
            'CTNMSComboBoxTestDialog',
          )


def testTNMSComboBox():
    dialog = CTNMSComboBoxTestDialog()
    dialog.exec_()


class CTNMSComboBoxTestDialog(CDialogBase, Ui_TestDialog):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.cmbTNMS.setIsTest(True)
        self.edtString.setText('cT3 cN2 cM0 cS1 pTis pN1 pM1 pS2')


    @pyqtSignature('QString')
    def on_edtString_textChanged(self, value):
        self.cmbTNMS.setValue(value)


    @pyqtSignature('')
    def on_cmbTNMS_editingFinished(self):
        self.edtString.setText(self.cmbTNMS.getValue()[0])
