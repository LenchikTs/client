# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_merge\preferences\JobsOperatingPage.ui'
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

class Ui_jobsOperatingPage(object):
    def setupUi(self, jobsOperatingPage):
        jobsOperatingPage.setObjectName(_fromUtf8("jobsOperatingPage"))
        jobsOperatingPage.resize(651, 405)
        jobsOperatingPage.setToolTip(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(jobsOperatingPage)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.chkJobTicketEndDateAskingIsRequired = QtGui.QCheckBox(jobsOperatingPage)
        self.chkJobTicketEndDateAskingIsRequired.setText(_fromUtf8(""))
        self.chkJobTicketEndDateAskingIsRequired.setObjectName(_fromUtf8("chkJobTicketEndDateAskingIsRequired"))
        self.gridLayout.addWidget(self.chkJobTicketEndDateAskingIsRequired, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(168, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 2)
        self.lblJobsOperatingIdentifierScan = QtGui.QLabel(jobsOperatingPage)
        self.lblJobsOperatingIdentifierScan.setObjectName(_fromUtf8("lblJobsOperatingIdentifierScan"))
        self.gridLayout.addWidget(self.lblJobsOperatingIdentifierScan, 1, 0, 1, 1)
        self.lblJobTicketEndDateAskingIsRequired = QtGui.QLabel(jobsOperatingPage)
        self.lblJobTicketEndDateAskingIsRequired.setObjectName(_fromUtf8("lblJobTicketEndDateAskingIsRequired"))
        self.gridLayout.addWidget(self.lblJobTicketEndDateAskingIsRequired, 0, 0, 1, 1)
        self.cmbJobsOperatingIdentifierScan = QtGui.QComboBox(jobsOperatingPage)
        self.cmbJobsOperatingIdentifierScan.setObjectName(_fromUtf8("cmbJobsOperatingIdentifierScan"))
        self.cmbJobsOperatingIdentifierScan.addItem(_fromUtf8(""))
        self.cmbJobsOperatingIdentifierScan.addItem(_fromUtf8(""))
        self.cmbJobsOperatingIdentifierScan.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbJobsOperatingIdentifierScan, 1, 1, 1, 3)
        self.lblJobsOperatingIdentifierScan.setBuddy(self.cmbJobsOperatingIdentifierScan)
        self.lblJobTicketEndDateAskingIsRequired.setBuddy(self.chkJobTicketEndDateAskingIsRequired)

        self.retranslateUi(jobsOperatingPage)
        QtCore.QMetaObject.connectSlotsByName(jobsOperatingPage)
        jobsOperatingPage.setTabOrder(self.chkJobTicketEndDateAskingIsRequired, self.cmbJobsOperatingIdentifierScan)

    def retranslateUi(self, jobsOperatingPage):
        jobsOperatingPage.setWindowTitle(_translate("jobsOperatingPage", "Выполнение работ", None))
        self.lblJobsOperatingIdentifierScan.setText(_translate("jobsOperatingPage", "Выбор &идентификатора", None))
        self.lblJobTicketEndDateAskingIsRequired.setText(_translate("jobsOperatingPage", "Требовать подтверждения &времени исполнения Работы", None))
        self.cmbJobsOperatingIdentifierScan.setItemText(0, _translate("jobsOperatingPage", "Идентификатор направления", None))
        self.cmbJobsOperatingIdentifierScan.setItemText(1, _translate("jobsOperatingPage", "Идентификатор биоматериала", None))
        self.cmbJobsOperatingIdentifierScan.setItemText(2, _translate("jobsOperatingPage", "Идентификатор пробы", None))

