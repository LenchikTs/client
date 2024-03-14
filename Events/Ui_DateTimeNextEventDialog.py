# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Events\DateTimeNextEventDialog.ui'
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

class Ui_DateTimeNextEventDialog(object):
    def setupUi(self, DateTimeNextEventDialog):
        DateTimeNextEventDialog.setObjectName(_fromUtf8("DateTimeNextEventDialog"))
        DateTimeNextEventDialog.resize(246, 66)
        self.gridLayout = QtGui.QGridLayout(DateTimeNextEventDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtExecTimeNew = QtGui.QTimeEdit(DateTimeNextEventDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtExecTimeNew.sizePolicy().hasHeightForWidth())
        self.edtExecTimeNew.setSizePolicy(sizePolicy)
        self.edtExecTimeNew.setObjectName(_fromUtf8("edtExecTimeNew"))
        self.gridLayout.addWidget(self.edtExecTimeNew, 0, 2, 1, 2)
        self.edtExecDateNew = CDateEdit(DateTimeNextEventDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtExecDateNew.sizePolicy().hasHeightForWidth())
        self.edtExecDateNew.setSizePolicy(sizePolicy)
        self.edtExecDateNew.setCalendarPopup(True)
        self.edtExecDateNew.setObjectName(_fromUtf8("edtExecDateNew"))
        self.gridLayout.addWidget(self.edtExecDateNew, 0, 1, 1, 1)
        self.lblExecTimeNew = QtGui.QLabel(DateTimeNextEventDialog)
        self.lblExecTimeNew.setObjectName(_fromUtf8("lblExecTimeNew"))
        self.gridLayout.addWidget(self.lblExecTimeNew, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(DateTimeNextEventDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 4)

        self.retranslateUi(DateTimeNextEventDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DateTimeNextEventDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DateTimeNextEventDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DateTimeNextEventDialog)
        DateTimeNextEventDialog.setTabOrder(self.edtExecDateNew, self.edtExecTimeNew)
        DateTimeNextEventDialog.setTabOrder(self.edtExecTimeNew, self.buttonBox)

    def retranslateUi(self, DateTimeNextEventDialog):
        DateTimeNextEventDialog.setWindowTitle(_translate("DateTimeNextEventDialog", "Время выполнения", None))
        self.lblExecTimeNew.setText(_translate("DateTimeNextEventDialog", "Дата и время", None))

from library.DateEdit import CDateEdit
