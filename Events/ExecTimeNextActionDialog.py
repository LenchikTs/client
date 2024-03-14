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

from library.DialogBase   import CConstructHelperMixin

from Events.Ui_ExecTimeNextActionDialog import Ui_ExecTimeNextActionDialog

#wtf? почему QDialog?
class CExecTimeNextActionDialog(QtGui.QDialog, CConstructHelperMixin, Ui_ExecTimeNextActionDialog):
    def __init__(self, parent, begDateTime, execPersonId, execTimePlanManager=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.cmbPerson.setValue(execPersonId)
        self.begDateTime = begDateTime
        self.begTime = self.begDateTime.time()
        self.edtExecTimeNew.setMinimumTime(self.begTime)
        self.execTimePlanManager = execTimePlanManager
        self.btnExecTimeOld.setText(self.execTimePlanManager.toString('hh:mm') if self.execTimePlanManager else self.begTime.toString('hh:mm'))
        currentDateTime = QDateTime.currentDateTime()
        self.execTime = currentDateTime.time()
        self.edtExecTimeNew.setTime(self.execTime if self.begTime <= self.execTime else self.begTime)
        self.connect(self.buttonBox, SIGNAL('accepted()'), self.accept)
        self.setCourseVisible(False)


    def setCourseVisible(self, value):
        self._courseVisible = value
        self.cmbCourse.setVisible(value)
        self.lblCourse.setVisible(value)


    def execCourse(self):
        return self.cmbCourse.currentIndex()


    @pyqtSignature('')
    def on_btnExecTimeOld_clicked(self):
        self.setExecTime(self.begTime)
        QtGui.QDialog.accept(self)


    def accept(self):
        self.setExecTime(self.edtExecTimeNew.time())
        QtGui.QDialog.accept(self)


    def getExecTime(self):
        return self.execTime


    def getExecPersonId(self):
        return self.cmbPerson.value()


    def setExecTime(self, execTime):
        self.execTime = execTime
