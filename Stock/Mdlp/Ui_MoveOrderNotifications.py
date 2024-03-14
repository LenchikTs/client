# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_mdlp/Stock/Mdlp/MoveOrderNotifications.ui'
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

class Ui_moveOrderNotifications(object):
    def setupUi(self, moveOrderNotifications):
        moveOrderNotifications.setObjectName(_fromUtf8("moveOrderNotifications"))
        moveOrderNotifications.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(moveOrderNotifications)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblItems = CTableView(moveOrderNotifications)
        self.tblItems.setObjectName(_fromUtf8("tblItems"))
        self.gridLayout.addWidget(self.tblItems, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(moveOrderNotifications)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(moveOrderNotifications)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), moveOrderNotifications.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), moveOrderNotifications.reject)
        QtCore.QMetaObject.connectSlotsByName(moveOrderNotifications)

    def retranslateUi(self, moveOrderNotifications):
        moveOrderNotifications.setWindowTitle(_translate("moveOrderNotifications", "Список подходящих документов в МДЛП", None))

from library.TableView import CTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    moveOrderNotifications = QtGui.QDialog()
    ui = Ui_moveOrderNotifications()
    ui.setupUi(moveOrderNotifications)
    moveOrderNotifications.show()
    sys.exit(app.exec_())

