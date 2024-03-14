# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Reports\AttachmentList.ui'
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

class Ui_AttachmentListDialog(object):
    def setupUi(self, AttachmentListDialog):
        AttachmentListDialog.setObjectName(_fromUtf8("AttachmentListDialog"))
        AttachmentListDialog.resize(326, 80)
        self.gridLayout = QtGui.QGridLayout(AttachmentListDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(AttachmentListDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(AttachmentListDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 0, 1, 1, 1)
        self.label = QtGui.QLabel(AttachmentListDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 2)

        self.retranslateUi(AttachmentListDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AttachmentListDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AttachmentListDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AttachmentListDialog)

    def retranslateUi(self, AttachmentListDialog):
        AttachmentListDialog.setWindowTitle(_translate("AttachmentListDialog", "параметры отчета", None))
        self.label.setText(_translate("AttachmentListDialog", "Подразделение", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
