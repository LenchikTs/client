# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/dmitrii/s11/Notifications/ConfirmationTimeDialog.ui'
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

class Ui_ConfirmationTimeDialog(object):
    def setupUi(self, ConfirmationTimeDialog):
        ConfirmationTimeDialog.setObjectName(_fromUtf8("ConfirmationTimeDialog"))
        ConfirmationTimeDialog.resize(354, 126)
        self.layoutWidget = QtGui.QWidget(ConfirmationTimeDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(6, 6, 346, 116))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblNoteConfirmDate = QtGui.QLabel(self.layoutWidget)
        self.lblNoteConfirmDate.setObjectName(_fromUtf8("lblNoteConfirmDate"))
        self.gridLayout.addWidget(self.lblNoteConfirmDate, 0, 0, 1, 1)
        self.lblNoteConfirmTime = QtGui.QLabel(self.layoutWidget)
        self.lblNoteConfirmTime.setObjectName(_fromUtf8("lblNoteConfirmTime"))
        self.gridLayout.addWidget(self.lblNoteConfirmTime, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 1, 1, 1)
        self.edtNoteConfirmDate = CDateEdit(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtNoteConfirmDate.sizePolicy().hasHeightForWidth())
        self.edtNoteConfirmDate.setSizePolicy(sizePolicy)
        self.edtNoteConfirmDate.setCalendarPopup(True)
        self.edtNoteConfirmDate.setObjectName(_fromUtf8("edtNoteConfirmDate"))
        self.gridLayout.addWidget(self.edtNoteConfirmDate, 0, 1, 1, 1)
        self.edtNoteConfirmTime = CTimeEdit(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtNoteConfirmTime.sizePolicy().hasHeightForWidth())
        self.edtNoteConfirmTime.setSizePolicy(sizePolicy)
        self.edtNoteConfirmTime.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.edtNoteConfirmTime.setObjectName(_fromUtf8("edtNoteConfirmTime"))
        self.gridLayout.addWidget(self.edtNoteConfirmTime, 2, 1, 1, 1)

        self.retranslateUi(ConfirmationTimeDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ConfirmationTimeDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ConfirmationTimeDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ConfirmationTimeDialog)

    def retranslateUi(self, ConfirmationTimeDialog):
        ConfirmationTimeDialog.setWindowTitle(_translate("ConfirmationTimeDialog", "Дата и время подтверждения оповещения", None))
        self.lblNoteConfirmDate.setText(_translate("ConfirmationTimeDialog", "Дата подтверждения", None))
        self.lblNoteConfirmTime.setText(_translate("ConfirmationTimeDialog", "Время подтверждения", None))
        self.edtNoteConfirmTime.setDisplayFormat(_translate("ConfirmationTimeDialog", "HH:mm", None))

from library.DateEdit import CDateEdit
from library.TimeEdit import CTimeEdit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ConfirmationTimeDialog = QtGui.QDialog()
    ui = Ui_ConfirmationTimeDialog()
    ui.setupUi(ConfirmationTimeDialog)
    ConfirmationTimeDialog.show()
    sys.exit(app.exec_())

