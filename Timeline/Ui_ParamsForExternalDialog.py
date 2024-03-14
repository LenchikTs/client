# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Timeline\ParamsForExternalDialog.ui'
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

class Ui_ParamsForExternalDialog(object):
    def setupUi(self, ParamsForExternalDialog):
        ParamsForExternalDialog.setObjectName(_fromUtf8("ParamsForExternalDialog"))
        ParamsForExternalDialog.resize(344, 91)
        self.gridLayout = QtGui.QGridLayout(ParamsForExternalDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.edtTimelineAccessibilityDays = QtGui.QSpinBox(ParamsForExternalDialog)
        self.edtTimelineAccessibilityDays.setEnabled(False)
        self.edtTimelineAccessibilityDays.setMaximumSize(QtCore.QSize(50, 16777215))
        self.edtTimelineAccessibilityDays.setMaximum(999)
        self.edtTimelineAccessibilityDays.setObjectName(_fromUtf8("edtTimelineAccessibilityDays"))
        self.gridLayout.addWidget(self.edtTimelineAccessibilityDays, 1, 2, 1, 1)
        self.lblTimelineAccessibilityDaysSuffix = QtGui.QLabel(ParamsForExternalDialog)
        self.lblTimelineAccessibilityDaysSuffix.setEnabled(False)
        self.lblTimelineAccessibilityDaysSuffix.setObjectName(_fromUtf8("lblTimelineAccessibilityDaysSuffix"))
        self.gridLayout.addWidget(self.lblTimelineAccessibilityDaysSuffix, 1, 3, 1, 1)
        self.edtLastAccessibleTimelineDate = CDateEdit(ParamsForExternalDialog)
        self.edtLastAccessibleTimelineDate.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtLastAccessibleTimelineDate.sizePolicy().hasHeightForWidth())
        self.edtLastAccessibleTimelineDate.setSizePolicy(sizePolicy)
        self.edtLastAccessibleTimelineDate.setCalendarPopup(True)
        self.edtLastAccessibleTimelineDate.setObjectName(_fromUtf8("edtLastAccessibleTimelineDate"))
        self.gridLayout.addWidget(self.edtLastAccessibleTimelineDate, 0, 2, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(80, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 5, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(80, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 5, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ParamsForExternalDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 6)
        self.chkTimelineAccessibilityDays = QtGui.QCheckBox(ParamsForExternalDialog)
        self.chkTimelineAccessibilityDays.setObjectName(_fromUtf8("chkTimelineAccessibilityDays"))
        self.gridLayout.addWidget(self.chkTimelineAccessibilityDays, 1, 0, 1, 1)
        self.chkLastAccessibleTimelineDate = QtGui.QCheckBox(ParamsForExternalDialog)
        self.chkLastAccessibleTimelineDate.setChecked(False)
        self.chkLastAccessibleTimelineDate.setObjectName(_fromUtf8("chkLastAccessibleTimelineDate"))
        self.gridLayout.addWidget(self.chkLastAccessibleTimelineDate, 0, 0, 1, 1)

        self.retranslateUi(ParamsForExternalDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ParamsForExternalDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ParamsForExternalDialog.reject)
        QtCore.QObject.connect(self.chkLastAccessibleTimelineDate, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtLastAccessibleTimelineDate.setEnabled)
        QtCore.QObject.connect(self.chkTimelineAccessibilityDays, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtTimelineAccessibilityDays.setEnabled)
        QtCore.QObject.connect(self.chkTimelineAccessibilityDays, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.lblTimelineAccessibilityDaysSuffix.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(ParamsForExternalDialog)
        ParamsForExternalDialog.setTabOrder(self.chkLastAccessibleTimelineDate, self.edtLastAccessibleTimelineDate)
        ParamsForExternalDialog.setTabOrder(self.edtLastAccessibleTimelineDate, self.chkTimelineAccessibilityDays)
        ParamsForExternalDialog.setTabOrder(self.chkTimelineAccessibilityDays, self.edtTimelineAccessibilityDays)
        ParamsForExternalDialog.setTabOrder(self.edtTimelineAccessibilityDays, self.buttonBox)

    def retranslateUi(self, ParamsForExternalDialog):
        ParamsForExternalDialog.setWindowTitle(_translate("ParamsForExternalDialog", "Изменить параметры доступа к расписанию", None))
        self.edtTimelineAccessibilityDays.setToolTip(_translate("ParamsForExternalDialog", "Если это поле заполнено (не 0),\n"
"то указанная значение используется как количество дней начиная с текущего на которые видно расписание.", None))
        self.lblTimelineAccessibilityDaysSuffix.setText(_translate("ParamsForExternalDialog", "дней", None))
        self.edtLastAccessibleTimelineDate.setToolTip(_translate("ParamsForExternalDialog", "Если это поле заполнено,\n"
"то указанная дата используется как предельная дата до которой видно расписание.", None))
        self.chkTimelineAccessibilityDays.setText(_translate("ParamsForExternalDialog", "Расписание видимо на", None))
        self.chkLastAccessibleTimelineDate.setText(_translate("ParamsForExternalDialog", "Расписание видимо до", None))

from library.DateEdit import CDateEdit
