# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/Orgs/OrgStructureListDialog.ui'
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

class Ui_OrgStructureListDialog(object):
    def setupUi(self, OrgStructureListDialog):
        OrgStructureListDialog.setObjectName(_fromUtf8("OrgStructureListDialog"))
        OrgStructureListDialog.resize(795, 470)
        self.gridLayout = QtGui.QGridLayout(OrgStructureListDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblOrgStructureList = CTableView(OrgStructureListDialog)
        self.tblOrgStructureList.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.tblOrgStructureList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblOrgStructureList.setObjectName(_fromUtf8("tblOrgStructureList"))
        self.gridLayout.addWidget(self.tblOrgStructureList, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(OrgStructureListDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(OrgStructureListDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), OrgStructureListDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), OrgStructureListDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(OrgStructureListDialog)

    def retranslateUi(self, OrgStructureListDialog):
        OrgStructureListDialog.setWindowTitle(_translate("OrgStructureListDialog", "Dialog", None))

from library.TableView import CTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    OrgStructureListDialog = QtGui.QDialog()
    ui = Ui_OrgStructureListDialog()
    ui.setupUi(OrgStructureListDialog)
    OrgStructureListDialog.show()
    sys.exit(app.exec_())

