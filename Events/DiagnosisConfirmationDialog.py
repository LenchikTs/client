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

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature
from library.ICDUtils import getMKBName

from Events.Ui_DiagnosisConfirmationDialog   import Ui_DiagnosisConfirmationDialog

class CDiagnosisConfirmationDialog(QtGui.QDialog, Ui_DiagnosisConfirmationDialog):
    acceptOld = 101
    acceptNew = 102
    accentNewAndModifyOld = 103

    def __init__(self,  parent, oldMKB, newMKB):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setup(oldMKB, newMKB)


    def setup(self, oldMKB, newMKB):
        oldMKBName = getMKBName(oldMKB)
        newMKBName = getMKBName(newMKB)

        self.lblMessage.setText(u'Ведён код %s (%s)\nРанее был указан код %s (%s)\nИзменить на этот код?' % (newMKB, newMKBName, oldMKB, oldMKBName))
        self.btnAcceptOld.setText(u'Изменить на %s' % oldMKB)
        self.btnAcceptNew.setText(u'Принять %s' % newMKB)
        self.btnAcceptNewAndModifyOld.setText(u'Применить %s взамен %s' % (newMKB, oldMKB))


    @pyqtSignature('')
    def on_btnAcceptOld_clicked(self):
        self.done(self.acceptOld)


    @pyqtSignature('')
    def on_btnAcceptNew_clicked(self):
        self.done(self.acceptNew)


    @pyqtSignature('')
    def on_btnAcceptNewAndModifyOld_clicked(self):
        self.done(self.accentNewAndModifyOld)
