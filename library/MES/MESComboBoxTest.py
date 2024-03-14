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
from library.Utils import forceStringEx

from .Ui_MESComboBoxTest import Ui_TestDialog

def testMESComboBox():
    dialog = CMESComboBoxTestDialog()
    dialog.exec_()


class CMESComboBoxTestDialog(CDialogBase, Ui_TestDialog):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.cmbEventProfile.setTable('rbEventProfile', True)
        self.cmbSpeciality.setTable('rbSpeciality', True)


    @pyqtSignature('int')
    def on_edtAge_valueChanged(self, age):
        def fakeAgeTuple(age):
            return (age*365,
                    age*365/7,
                    age*12,
                    age
                   )

        self.cmbMES.setClientAge(fakeAgeTuple(age))


    @pyqtSignature('int')
    def on_cmbSex_currentIndexChanged(self, sex):
        self.cmbMES.setClientSex(sex)


    @pyqtSignature('int')
    def on_cmbEventProfile_currentIndexChanged(self, sex):
        self.cmbMES.setEventProfile(self.cmbEventProfile.value())


    @pyqtSignature('QString')
    def on_edtMESCodeTemplate_textChanged(self, text):
        self.cmbMES.setMESCodeTemplate(forceStringEx(text))


    @pyqtSignature('QString')
    def on_edtMESNameTemplate_textChanged(self, text):
        self.cmbMES.setMESNameTemplate(forceStringEx(text))


    @pyqtSignature('int')
    def on_cmbSpeciality_currentIndexChanged(self, sex):
        self.cmbMES.setSpeciality(self.cmbSpeciality.value())


    @pyqtSignature('QString')
    def on_edtMKB_textChanged(self, text):
        self.cmbMES.setMKB(forceStringEx(text))