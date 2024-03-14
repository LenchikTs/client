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
from PyQt4.QtCore import QDateTime, pyqtSignature, SIGNAL

#from library.DialogBase   import CDialogBase
from library.DialogBase   import CConstructHelperMixin

from Ui_DateTimeNextEventDialog import Ui_DateTimeNextEventDialog

#wtf? почему QDialog а не CDialogBase ?
class CDateTimeNextEventDialog(QtGui.QDialog, CConstructHelperMixin, Ui_DateTimeNextEventDialog):
    def __init__(self, parent, begDateTime):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.begDateTime = begDateTime
        self.begDate = self.begDateTime.date()
        self.begTime = self.begDateTime.time()

        self.edtExecDateNew.setMinimumDate(self.begDate)
        self.edtExecTimeNew.setMinimumTime(self.begTime)

        self.edtExecDateNew.setDate(self.begDate)
        self.edtExecTimeNew.setTime(self.begTime.addSecs(121))
        self.connect(self.buttonBox, SIGNAL('accepted()'), self.accept)


    def getPrevDateTime(self):
        return self.begDateTime


    def accept(self):
        self.setPrevDateTime(QDateTime(self.edtExecDateNew.date(), self.edtExecTimeNew.time()))
        QtGui.QDialog.accept(self)


    def setPrevDateTime(self, value):
        self.begDateTime = value


    @pyqtSignature('QDate')
    def on_edtExecDateNew_dateChanged(self, date):
        if date == self.begDate:
            self.edtExecTimeNew.setMinimumTime(self.begTime)
        else:
            self.edtExecTimeNew.clearMinimumTime()
