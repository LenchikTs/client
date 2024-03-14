# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\preferences\calendarChangeday.ui'
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

class Ui_ChangeDayDialog(object):
    def setupUi(self, ChangeDayDialog):
        ChangeDayDialog.setObjectName(_fromUtf8("ChangeDayDialog"))
        ChangeDayDialog.resize(305, 122)
        self.gridLayout = QtGui.QGridLayout(ChangeDayDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(ChangeDayDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.date = CDateEdit(ChangeDayDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.date.sizePolicy().hasHeightForWidth())
        self.date.setSizePolicy(sizePolicy)
        self.date.setMinimumSize(QtCore.QSize(120, 0))
        self.date.setObjectName(_fromUtf8("date"))
        self.gridLayout.addWidget(self.date, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(90, 22, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.label_2 = QtGui.QLabel(ChangeDayDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.dateChange = CDateEdit(ChangeDayDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateChange.sizePolicy().hasHeightForWidth())
        self.dateChange.setSizePolicy(sizePolicy)
        self.dateChange.setMinimumSize(QtCore.QSize(120, 0))
        self.dateChange.setObjectName(_fromUtf8("dateChange"))
        self.gridLayout.addWidget(self.dateChange, 1, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(90, 22, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(73, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 4, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ChangeDayDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 3)
        self.text = QtGui.QLineEdit(ChangeDayDialog)
        self.text.setObjectName(_fromUtf8("text"))
        self.gridLayout.addWidget(self.text, 2, 1, 1, 2)
        self.label_3 = QtGui.QLabel(ChangeDayDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.retranslateUi(ChangeDayDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ChangeDayDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ChangeDayDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ChangeDayDialog)
        ChangeDayDialog.setTabOrder(self.date, self.dateChange)
        ChangeDayDialog.setTabOrder(self.dateChange, self.text)
        ChangeDayDialog.setTabOrder(self.text, self.buttonBox)

    def retranslateUi(self, ChangeDayDialog):
        ChangeDayDialog.setWindowTitle(_translate("ChangeDayDialog", "Календарный перенос", None))
        self.label.setText(_translate("ChangeDayDialog", "Дата", None))
        self.label_2.setText(_translate("ChangeDayDialog", "Дата переноса", None))
        self.label_3.setText(_translate("ChangeDayDialog", "Комментарий", None))

from library.DateEdit import CDateEdit
