# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/Reports/SpecialityListDialog.ui'
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

class Ui_SpecialityListDialog(object):
    def setupUi(self, SpecialityListDialog):
        SpecialityListDialog.setObjectName(_fromUtf8("SpecialityListDialog"))
        SpecialityListDialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(SpecialityListDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblSpecialityList = CTableView(SpecialityListDialog)
        self.tblSpecialityList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.tblSpecialityList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblSpecialityList.setObjectName(_fromUtf8("tblSpecialityList"))
        self.gridLayout.addWidget(self.tblSpecialityList, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(SpecialityListDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(SpecialityListDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SpecialityListDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SpecialityListDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SpecialityListDialog)

    def retranslateUi(self, SpecialityListDialog):
        SpecialityListDialog.setWindowTitle(_translate("SpecialityListDialog", "Специальность", None))

from library.TableView import CTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SpecialityListDialog = QtGui.QDialog()
    ui = Ui_SpecialityListDialog()
    ui.setupUi(SpecialityListDialog)
    SpecialityListDialog.show()
    sys.exit(app.exec_())

