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

from PyQt4.QtCore import pyqtSignature, QDate

from library.DialogBase import CDialogBase
from library.Utils import forceStringEx

from Ui_CSGComboBoxTest import Ui_TestDialog


__all__ = ('testCSGComboBox',
           'CCSGComboBoxTestDialog'
          )

def testCSGComboBox():
    dialog = CCSGComboBoxTestDialog()
    dialog.exec_()


class CCSGComboBoxTestDialog(CDialogBase, Ui_TestDialog):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)


    @pyqtSignature('int')
    def on_edtAge_valueChanged(self, age):
        date = QDate.currentDate()
        self.cmbCSG.setEventBegDate(date)
        self.cmbCSG.setClientBirthDate(date.addYears(-age))


    @pyqtSignature('int')
    def on_cmbSex_currentIndexChanged(self, sex):
        self.cmbCSG.setClientSex(sex)


    @pyqtSignature('QString')
    def on_edtMKB_textChanged(self, text):
        self.cmbCSG.setMKB(forceStringEx(text))
