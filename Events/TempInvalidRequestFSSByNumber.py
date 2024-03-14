# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2015-2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
from PyQt4.QtCore import Qt, QDate, pyqtSignature

from library.DialogBase import CDialogBase

from Events.Ui_TempInvalidRequestFSSByNumberDialog import Ui_TempInvalidRequestFSSByNumberDialog

class CTempInvalidRequestFSSByNumber(CDialogBase, Ui_TempInvalidRequestFSSByNumberDialog):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.btnQuery.setEnabled(False)
        self.edtQuery.setFocus(Qt.OtherFocusReason)

    @pyqtSignature('const QString &')
    def on_edtQuery_textChanged(self, text):
        self.btnQuery.setEnabled(len(text)==12)


    def on_btnQuery_clicked(self):
        if bool(self.edtQuery.text()):
            self.accept()
