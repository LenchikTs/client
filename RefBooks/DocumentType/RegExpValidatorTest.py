# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2016-2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################


from library.DialogBase import CDialogBase

from .Ui_RegExpValidatorTest import Ui_RegExpValidatorTest


def testRegExpValidator(regExp):
    dialog = CRegExpValidatorTestDialog()
    dialog.setRegExp(regExp)
    dialog.exec_()


class CRegExpValidatorTestDialog(CDialogBase, Ui_RegExpValidatorTest):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)


    def setRegExp(self, regExp):
        self.edtSample.setRegExp(regExp)
