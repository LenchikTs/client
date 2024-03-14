# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\user\Documents\svn\Registry\SelectedTimeTableRowsListDialog.ui'
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

class Ui_SelectedTimeTableRowsListDialog(object):
    def setupUi(self, SelectedTimeTableRowsListDialog):
        SelectedTimeTableRowsListDialog.setObjectName(_fromUtf8("SelectedTimeTableRowsListDialog"))
        SelectedTimeTableRowsListDialog.resize(542, 270)
        self.gridLayout = QtGui.QGridLayout(SelectedTimeTableRowsListDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(SelectedTimeTableRowsListDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.lblSelectedTimeTableRowsList = QtGui.QLabel(SelectedTimeTableRowsListDialog)
        self.lblSelectedTimeTableRowsList.setObjectName(_fromUtf8("lblSelectedTimeTableRowsList"))
        self.gridLayout.addWidget(self.lblSelectedTimeTableRowsList, 0, 0, 1, 1)
        self.tblSelectedTimeTableRowsList = QtGui.QTableView(SelectedTimeTableRowsListDialog)
        self.tblSelectedTimeTableRowsList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.tblSelectedTimeTableRowsList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblSelectedTimeTableRowsList.setObjectName(_fromUtf8("tblSelectedTimeTableRowsList"))
        self.gridLayout.addWidget(self.tblSelectedTimeTableRowsList, 1, 0, 1, 1)

        self.retranslateUi(SelectedTimeTableRowsListDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SelectedTimeTableRowsListDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SelectedTimeTableRowsListDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SelectedTimeTableRowsListDialog)

    def retranslateUi(self, SelectedTimeTableRowsListDialog):
        SelectedTimeTableRowsListDialog.setWindowTitle(_translate("SelectedTimeTableRowsListDialog", "Выбранные периоды приема", None))
        self.lblSelectedTimeTableRowsList.setText(_translate("SelectedTimeTableRowsListDialog", "Выберите период приема, для которого требуется осуществить сверхплановую запись:", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SelectedTimeTableRowsListDialog = QtGui.QDialog()
    ui = Ui_SelectedTimeTableRowsListDialog()
    ui.setupUi(SelectedTimeTableRowsListDialog)
    SelectedTimeTableRowsListDialog.show()
    sys.exit(app.exec_())

