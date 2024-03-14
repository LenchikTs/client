# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_mdlp/Stock/Mdlp/WithdrawalsByRegisrar.ui'
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

class Ui_withdrawalsByRegisrar(object):
    def setupUi(self, withdrawalsByRegisrar):
        withdrawalsByRegisrar.setObjectName(_fromUtf8("withdrawalsByRegisrar"))
        withdrawalsByRegisrar.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(withdrawalsByRegisrar)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblItems = CTableView(withdrawalsByRegisrar)
        self.tblItems.setObjectName(_fromUtf8("tblItems"))
        self.gridLayout.addWidget(self.tblItems, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(withdrawalsByRegisrar)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(withdrawalsByRegisrar)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), withdrawalsByRegisrar.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), withdrawalsByRegisrar.reject)
        QtCore.QMetaObject.connectSlotsByName(withdrawalsByRegisrar)

    def retranslateUi(self, withdrawalsByRegisrar):
        withdrawalsByRegisrar.setWindowTitle(_translate("withdrawalsByRegisrar", "Список подходящих документов в МДЛП", None))

from library.TableView import CTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    withdrawalsByRegisrar = QtGui.QDialog()
    ui = Ui_withdrawalsByRegisrar()
    ui.setupUi(withdrawalsByRegisrar)
    withdrawalsByRegisrar.show()
    sys.exit(app.exec_())

