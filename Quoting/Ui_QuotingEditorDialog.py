# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Quoting\QuotingEditorDialog.ui'
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

class Ui_QuotingEditorDialog(object):
    def setupUi(self, QuotingEditorDialog):
        QuotingEditorDialog.setObjectName(_fromUtf8("QuotingEditorDialog"))
        QuotingEditorDialog.resize(359, 145)
        self.gridLayout = QtGui.QGridLayout(QuotingEditorDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbQuotaType = CRBComboBox(QuotingEditorDialog)
        self.cmbQuotaType.setObjectName(_fromUtf8("cmbQuotaType"))
        self.gridLayout.addWidget(self.cmbQuotaType, 0, 1, 1, 2)
        self.lblLimit = QtGui.QLabel(QuotingEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblLimit.sizePolicy().hasHeightForWidth())
        self.lblLimit.setSizePolicy(sizePolicy)
        self.lblLimit.setObjectName(_fromUtf8("lblLimit"))
        self.gridLayout.addWidget(self.lblLimit, 3, 0, 1, 1)
        self.edtLimit = QtGui.QSpinBox(QuotingEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtLimit.sizePolicy().hasHeightForWidth())
        self.edtLimit.setSizePolicy(sizePolicy)
        self.edtLimit.setMaximum(131071)
        self.edtLimit.setObjectName(_fromUtf8("edtLimit"))
        self.gridLayout.addWidget(self.edtLimit, 3, 1, 1, 1)
        self.lblQyotaType = QtGui.QLabel(QuotingEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblQyotaType.sizePolicy().hasHeightForWidth())
        self.lblQyotaType.setSizePolicy(sizePolicy)
        self.lblQyotaType.setObjectName(_fromUtf8("lblQyotaType"))
        self.gridLayout.addWidget(self.lblQyotaType, 0, 0, 1, 1)
        self.edtBeginDate = QtGui.QDateEdit(QuotingEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBeginDate.sizePolicy().hasHeightForWidth())
        self.edtBeginDate.setSizePolicy(sizePolicy)
        self.edtBeginDate.setCalendarPopup(True)
        self.edtBeginDate.setObjectName(_fromUtf8("edtBeginDate"))
        self.gridLayout.addWidget(self.edtBeginDate, 1, 1, 1, 1)
        self.lblEndDate = QtGui.QLabel(QuotingEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblEndDate.sizePolicy().hasHeightForWidth())
        self.lblEndDate.setSizePolicy(sizePolicy)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 2, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 24, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 1, 1, 1)
        self.edtEndDate = QtGui.QDateEdit(QuotingEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 2, 1, 1, 1)
        self.lblBeginDate = QtGui.QLabel(QuotingEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblBeginDate.sizePolicy().hasHeightForWidth())
        self.lblBeginDate.setSizePolicy(sizePolicy)
        self.lblBeginDate.setObjectName(_fromUtf8("lblBeginDate"))
        self.gridLayout.addWidget(self.lblBeginDate, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(QuotingEditorDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 2, 2, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 1, 2, 1, 1)

        self.retranslateUi(QuotingEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), QuotingEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), QuotingEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(QuotingEditorDialog)

    def retranslateUi(self, QuotingEditorDialog):
        QuotingEditorDialog.setWindowTitle(_translate("QuotingEditorDialog", "Dialog", None))
        self.lblLimit.setText(_translate("QuotingEditorDialog", "Предел", None))
        self.lblQyotaType.setText(_translate("QuotingEditorDialog", "Название", None))
        self.lblEndDate.setText(_translate("QuotingEditorDialog", "Дата окончания", None))
        self.lblBeginDate.setText(_translate("QuotingEditorDialog", "Дата начала", None))

from library.crbcombobox import CRBComboBox
