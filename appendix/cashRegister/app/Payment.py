#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
##
## Copyright (C) 2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, pyqtSignature


#from library.DialogBase       import CConstructHelperMixin
#from library.PreferencesMixin import CDialogPreferencesMixin

from Ui_Payment import Ui_CPayment


class CPaymentDialog(QtGui.QDialog, Ui_CPayment):
    u"""
    """
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)


    def setAmount(self, amount):
        self.edtAmount.setValue(amount)
        self.edtFee.setValue(amount)
        self.edtFee.selectAll()


    def getFee(self):
       return self.edtFee.value()


    def calcChange(self):
        change = round(self.edtFee.value() - self.edtAmount.value(), 2)
        self.edtChange.setValue(change)
        palette = QtGui.QPalette(self.palette())
        if change < 0:
            palette.setColor(palette.Text, Qt.red)
        self.edtChange.setPalette(palette)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled( change >= 0 )


    @pyqtSignature('double')
    def on_edtAmount_valueChanged(self, val):
        self.calcChange()


    @pyqtSignature('double')
    def on_edtFee_valueChanged(self, val):
        self.calcChange()



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    d = CPaymentDialog(None)
    d.setAmount(1234.56)

    d.show()

    sys.exit(app.exec_())
