# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/library/TestRegExpValidator.ui'
#
# Created: Thu Sep 29 18:51:04 2016
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_RegExpValidatorTester(object):
    def setupUi(self, RegExpValidatorTester):
        RegExpValidatorTester.setObjectName(_fromUtf8("RegExpValidatorTester"))
        RegExpValidatorTester.resize(295, 67)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RegExpValidatorTester.sizePolicy().hasHeightForWidth())
        RegExpValidatorTester.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(RegExpValidatorTester)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(RegExpValidatorTester)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.lblSample = QtGui.QLabel(RegExpValidatorTester)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblSample.sizePolicy().hasHeightForWidth())
        self.lblSample.setSizePolicy(sizePolicy)
        self.lblSample.setObjectName(_fromUtf8("lblSample"))
        self.gridLayout.addWidget(self.lblSample, 0, 0, 1, 1)
        self.edtSample = QtGui.QLineEdit(RegExpValidatorTester)
        self.edtSample.setObjectName(_fromUtf8("edtSample"))
        self.gridLayout.addWidget(self.edtSample, 0, 1, 1, 2)
        self.lblSample.setBuddy(self.edtSample)

        self.retranslateUi(RegExpValidatorTester)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RegExpValidatorTester.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RegExpValidatorTester.reject)
        QtCore.QMetaObject.connectSlotsByName(RegExpValidatorTester)
        RegExpValidatorTester.setTabOrder(self.edtSample, self.buttonBox)

    def retranslateUi(self, RegExpValidatorTester):
        RegExpValidatorTester.setWindowTitle(_translate("RegExpValidatorTester", "Проверка маски ввода", None))
        self.lblSample.setText(_translate("RegExpValidatorTester", "Образец", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RegExpValidatorTester = QtGui.QDialog()
    ui = Ui_RegExpValidatorTester()
    ui.setupUi(RegExpValidatorTester)
    RegExpValidatorTester.show()
    sys.exit(app.exec_())

