# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/preferences/ScanTestDialog.ui'
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

class Ui_ScanTestDialog(object):
    def setupUi(self, ScanTestDialog):
        ScanTestDialog.setObjectName(_fromUtf8("ScanTestDialog"))
        ScanTestDialog.resize(494, 315)
        ScanTestDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(ScanTestDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtSample = QtGui.QPlainTextEdit(ScanTestDialog)
        self.edtSample.setReadOnly(True)
        self.edtSample.setObjectName(_fromUtf8("edtSample"))
        self.gridLayout.addWidget(self.edtSample, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ScanTestDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Reset)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(ScanTestDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ScanTestDialog.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("clicked(QAbstractButton*)")), self.edtSample.clear)
        QtCore.QMetaObject.connectSlotsByName(ScanTestDialog)

    def retranslateUi(self, ScanTestDialog):
        ScanTestDialog.setWindowTitle(_translate("ScanTestDialog", "Проверка сканера", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ScanTestDialog = QtGui.QDialog()
    ui = Ui_ScanTestDialog()
    ui.setupUi(ScanTestDialog)
    ScanTestDialog.show()
    sys.exit(app.exec_())

