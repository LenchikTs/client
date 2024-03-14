# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Logger.ui'
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

class Ui_Logger(object):
    def setupUi(self, Logger):
        Logger.setObjectName(_fromUtf8("Logger"))
        Logger.resize(400, 300)
        Logger.setModal(True)
        self.gridLayout = QtGui.QGridLayout(Logger)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textBrowser = QtGui.QTextBrowser(Logger)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Logger)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(Logger)
        QtCore.QMetaObject.connectSlotsByName(Logger)

    def retranslateUi(self, Logger):
        Logger.setWindowTitle(_translate("Logger", "Dialog", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Logger = QtGui.QDialog()
    ui = Ui_Logger()
    ui.setupUi(Logger)
    Logger.show()
    sys.exit(app.exec_())

