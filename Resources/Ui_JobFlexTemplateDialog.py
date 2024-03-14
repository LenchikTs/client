# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Resources\JobFlexTemplateDialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_FlexTemplateDialog(object):
    def setupUi(self, FlexTemplateDialog):
        FlexTemplateDialog.setObjectName(_fromUtf8("FlexTemplateDialog"))
        FlexTemplateDialog.resize(447, 516)
        self.gridLayout = QtGui.QGridLayout(FlexTemplateDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.calendarWidget = CCalendarWidget(FlexTemplateDialog)
        self.calendarWidget.setObjectName(_fromUtf8("calendarWidget"))
        self.gridLayout.addWidget(self.calendarWidget, 0, 0, 1, 1)
        self.tblJobs = COrgSrtuctureJobsView(FlexTemplateDialog)
        self.tblJobs.setObjectName(_fromUtf8("tblJobs"))
        self.gridLayout.addWidget(self.tblJobs, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(FlexTemplateDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 1)
        self.chkRemoveExistingJobs = QtGui.QCheckBox(FlexTemplateDialog)
        self.chkRemoveExistingJobs.setObjectName(_fromUtf8("chkRemoveExistingJobs"))
        self.gridLayout.addWidget(self.chkRemoveExistingJobs, 2, 0, 1, 1)

        self.retranslateUi(FlexTemplateDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), FlexTemplateDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), FlexTemplateDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(FlexTemplateDialog)
        FlexTemplateDialog.setTabOrder(self.calendarWidget, self.tblJobs)
        FlexTemplateDialog.setTabOrder(self.tblJobs, self.chkRemoveExistingJobs)
        FlexTemplateDialog.setTabOrder(self.chkRemoveExistingJobs, self.buttonBox)

    def retranslateUi(self, FlexTemplateDialog):
        FlexTemplateDialog.setWindowTitle(_translate("FlexTemplateDialog", "Шаблон скользящего графика", None))
        self.chkRemoveExistingJobs.setText(_translate("FlexTemplateDialog", "Удалить предыдущее расписание", None))

from Resources.OrgStructureJobs import COrgSrtuctureJobsView
from library.CalendarWidget import CCalendarWidget
