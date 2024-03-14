# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/Events/ActionTypeListDialog.ui'
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

class Ui_ActionTypeListDialog(object):
    def setupUi(self, ActionTypeListDialog):
        ActionTypeListDialog.setObjectName(_fromUtf8("ActionTypeListDialog"))
        ActionTypeListDialog.resize(451, 359)
        self.gridLayout = QtGui.QGridLayout(ActionTypeListDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblActionTypeList = CInDocTableView(ActionTypeListDialog)
        self.tblActionTypeList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.tblActionTypeList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblActionTypeList.setObjectName(_fromUtf8("tblActionTypeList"))
        self.gridLayout.addWidget(self.tblActionTypeList, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ActionTypeListDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(ActionTypeListDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ActionTypeListDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ActionTypeListDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ActionTypeListDialog)

    def retranslateUi(self, ActionTypeListDialog):
        ActionTypeListDialog.setWindowTitle(_translate("ActionTypeListDialog", "Dialog", None))

from library.InDocTable import CInDocTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ActionTypeListDialog = QtGui.QDialog()
    ui = Ui_ActionTypeListDialog()
    ui.setupUi(ActionTypeListDialog)
    ActionTypeListDialog.show()
    sys.exit(app.exec_())

