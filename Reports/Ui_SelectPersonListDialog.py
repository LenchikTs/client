# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\user\Documents\svn\Reports\SelectPersonListDialog.ui'
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

class Ui_SelectPersonListDialog(object):
    def setupUi(self, SelectPersonListDialog):
        SelectPersonListDialog.setObjectName(_fromUtf8("SelectPersonListDialog"))
        SelectPersonListDialog.resize(812, 300)
        self.gridLayout = QtGui.QGridLayout(SelectPersonListDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblSelectPersonList = CTableView(SelectPersonListDialog)
        self.tblSelectPersonList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.tblSelectPersonList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblSelectPersonList.setObjectName(_fromUtf8("tblSelectPersonList"))
        self.gridLayout.addWidget(self.tblSelectPersonList, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(SelectPersonListDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(SelectPersonListDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SelectPersonListDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SelectPersonListDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SelectPersonListDialog)

    def retranslateUi(self, SelectPersonListDialog):
        SelectPersonListDialog.setWindowTitle(_translate("SelectPersonListDialog", "Сотрудники", None))

from library.TableView import CTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SelectPersonListDialog = QtGui.QDialog()
    ui = Ui_SelectPersonListDialog()
    ui.setupUi(SelectPersonListDialog)
    SelectPersonListDialog.show()
    sys.exit(app.exec_())

