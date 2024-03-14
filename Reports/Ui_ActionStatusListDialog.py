# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/lampa/Docs/svn/trunk/Reports/ActionStatusListDialog.ui'
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

class Ui_ActionStatusListDialog(object):
    def setupUi(self, ActionStatusListDialog):
        ActionStatusListDialog.setObjectName(_fromUtf8("ActionStatusListDialog"))
        ActionStatusListDialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(ActionStatusListDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblActionStatusList = QtGui.QTableView(ActionStatusListDialog)
        self.tblActionStatusList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.tblActionStatusList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblActionStatusList.setObjectName(_fromUtf8("tblActionStatusList"))
        self.gridLayout.addWidget(self.tblActionStatusList, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ActionStatusListDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(ActionStatusListDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ActionStatusListDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ActionStatusListDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ActionStatusListDialog)

    def retranslateUi(self, ActionStatusListDialog):
        ActionStatusListDialog.setWindowTitle(_translate("ActionStatusListDialog", "Статус действия", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ActionStatusListDialog = QtGui.QDialog()
    ui = Ui_ActionStatusListDialog()
    ui.setupUi(ActionStatusListDialog)
    ActionStatusListDialog.show()
    sys.exit(app.exec_())

