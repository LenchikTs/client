# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Resources\JobPlanNumbersDialog.ui'
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

class Ui_JobPlanNumbersDialog(object):
    def setupUi(self, JobPlanNumbersDialog):
        JobPlanNumbersDialog.setObjectName(_fromUtf8("JobPlanNumbersDialog"))
        JobPlanNumbersDialog.resize(608, 470)
        self.verticalLayout_3 = QtGui.QVBoxLayout(JobPlanNumbersDialog)
        self.verticalLayout_3.setMargin(4)
        self.verticalLayout_3.setSpacing(4)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.splitter = QtGui.QSplitter(JobPlanNumbersDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.grplJobAmbNumbers = QtGui.QGroupBox(self.splitter)
        self.grplJobAmbNumbers.setObjectName(_fromUtf8("grplJobAmbNumbers"))
        self.verticalLayout = QtGui.QVBoxLayout(self.grplJobAmbNumbers)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tblJobAmbNumbers = CTableView(self.grplJobAmbNumbers)
        self.tblJobAmbNumbers.setObjectName(_fromUtf8("tblJobAmbNumbers"))
        self.verticalLayout.addWidget(self.tblJobAmbNumbers)
        self.grpOrgStructureGaps = QtGui.QGroupBox(self.splitter)
        self.grpOrgStructureGaps.setObjectName(_fromUtf8("grpOrgStructureGaps"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.grpOrgStructureGaps)
        self.verticalLayout_2.setMargin(4)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tblJobOrgStructureGaps = CTableView(self.grpOrgStructureGaps)
        self.tblJobOrgStructureGaps.setObjectName(_fromUtf8("tblJobOrgStructureGaps"))
        self.verticalLayout_2.addWidget(self.tblJobOrgStructureGaps)
        self.verticalLayout_3.addWidget(self.splitter)
        self.buttonBox = QtGui.QDialogButtonBox(JobPlanNumbersDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(JobPlanNumbersDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), JobPlanNumbersDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), JobPlanNumbersDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(JobPlanNumbersDialog)
        JobPlanNumbersDialog.setTabOrder(self.tblJobAmbNumbers, self.tblJobOrgStructureGaps)
        JobPlanNumbersDialog.setTabOrder(self.tblJobOrgStructureGaps, self.buttonBox)

    def retranslateUi(self, JobPlanNumbersDialog):
        JobPlanNumbersDialog.setWindowTitle(_translate("JobPlanNumbersDialog", "Номерки", None))
        self.grplJobAmbNumbers.setTitle(_translate("JobPlanNumbersDialog", "Амбулаторный прием", None))
        self.grpOrgStructureGaps.setTitle(_translate("JobPlanNumbersDialog", "Перерывы подразделения", None))

from library.TableView import CTableView
