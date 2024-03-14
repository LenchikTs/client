# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ReportPrimaryClientListSetupDialog.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
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

class Ui_CReportPrimaryClientListSetupDialog(object):
    def setupUi(self, CReportPrimaryClientListSetupDialog):
        CReportPrimaryClientListSetupDialog.setObjectName(_fromUtf8("CReportPrimaryClientListSetupDialog"))
        CReportPrimaryClientListSetupDialog.resize(423, 193)
        self.gridLayout = QtGui.QGridLayout(CReportPrimaryClientListSetupDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btnEventTypePurposeList = QtGui.QPushButton(CReportPrimaryClientListSetupDialog)
        self.btnEventTypePurposeList.setObjectName(_fromUtf8("btnEventTypePurposeList"))
        self.gridLayout.addWidget(self.btnEventTypePurposeList, 2, 0, 1, 1)
        self.lblBegDate = QtGui.QLabel(CReportPrimaryClientListSetupDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.edtBegDate = CDateEdit(CReportPrimaryClientListSetupDialog)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.lblEndDate = QtGui.QLabel(CReportPrimaryClientListSetupDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.edtEndDate = CDateEdit(CReportPrimaryClientListSetupDialog)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(CReportPrimaryClientListSetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.lblEventTypePurposeList = QtGui.QLabel(CReportPrimaryClientListSetupDialog)
        self.lblEventTypePurposeList.setWordWrap(True)
        self.lblEventTypePurposeList.setObjectName(_fromUtf8("lblEventTypePurposeList"))
        self.gridLayout.addWidget(self.lblEventTypePurposeList, 2, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 2)

        self.retranslateUi(CReportPrimaryClientListSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), CReportPrimaryClientListSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), CReportPrimaryClientListSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CReportPrimaryClientListSetupDialog)

    def retranslateUi(self, CReportPrimaryClientListSetupDialog):
        CReportPrimaryClientListSetupDialog.setWindowTitle(_translate("CReportPrimaryClientListSetupDialog", "Dialog", None))
        self.btnEventTypePurposeList.setText(_translate("CReportPrimaryClientListSetupDialog", "Назначение типов событий", None))
        self.lblBegDate.setText(_translate("CReportPrimaryClientListSetupDialog", "Дата начала периода", None))
        self.lblEndDate.setText(_translate("CReportPrimaryClientListSetupDialog", "Дата окончания периода", None))
        self.lblEventTypePurposeList.setText(_translate("CReportPrimaryClientListSetupDialog", "Не задано", None))

from library.DateEdit import CDateEdit
