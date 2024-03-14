# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/RefBooks/SRSUserEditor.ui'
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

class Ui_ItemEditorDialog(object):
    def setupUi(self, ItemEditorDialog):
        ItemEditorDialog.setObjectName(_fromUtf8("ItemEditorDialog"))
        ItemEditorDialog.resize(411, 383)
        self.gridLayout = QtGui.QGridLayout(ItemEditorDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtQuota = QtGui.QSpinBox(ItemEditorDialog)
        self.edtQuota.setMaximum(100)
        self.edtQuota.setObjectName(_fromUtf8("edtQuota"))
        self.gridLayout.addWidget(self.edtQuota, 5, 1, 1, 1)
        self.lblName = QtGui.QLabel(ItemEditorDialog)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 3, 0, 1, 1)
        self.lblCode = QtGui.QLabel(ItemEditorDialog)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.lblQuota = QtGui.QLabel(ItemEditorDialog)
        self.lblQuota.setObjectName(_fromUtf8("lblQuota"))
        self.gridLayout.addWidget(self.lblQuota, 5, 0, 1, 1)
        self.lblFinances = QtGui.QLabel(ItemEditorDialog)
        self.lblFinances.setObjectName(_fromUtf8("lblFinances"))
        self.gridLayout.addWidget(self.lblFinances, 6, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 212, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 0, 1, 1)
        self.lblPosition = QtGui.QLabel(ItemEditorDialog)
        self.lblPosition.setObjectName(_fromUtf8("lblPosition"))
        self.gridLayout.addWidget(self.lblPosition, 2, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 5, 2, 1, 1)
        self.tblAvailableFinances = CInDocTableView(ItemEditorDialog)
        self.tblAvailableFinances.setObjectName(_fromUtf8("tblAvailableFinances"))
        self.tblAvailableFinances.horizontalHeader().setHighlightSections(True)
        self.tblAvailableFinances.verticalHeader().setVisible(False)
        self.tblAvailableFinances.verticalHeader().setHighlightSections(True)
        self.gridLayout.addWidget(self.tblAvailableFinances, 6, 1, 2, 2)
        self.edtName = QtGui.QLineEdit(ItemEditorDialog)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 3, 1, 1, 2)
        self.edtPosition = QtGui.QLineEdit(ItemEditorDialog)
        self.edtPosition.setObjectName(_fromUtf8("edtPosition"))
        self.gridLayout.addWidget(self.edtPosition, 2, 1, 1, 2)
        self.edtCode = QtGui.QLineEdit(ItemEditorDialog)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout.addWidget(self.edtCode, 0, 1, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(ItemEditorDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 3)
        self.lblIsLocal = QtGui.QLabel(ItemEditorDialog)
        self.lblIsLocal.setObjectName(_fromUtf8("lblIsLocal"))
        self.gridLayout.addWidget(self.lblIsLocal, 4, 0, 1, 1)
        self.chkIsLocal = QtGui.QCheckBox(ItemEditorDialog)
        self.chkIsLocal.setText(_fromUtf8(""))
        self.chkIsLocal.setObjectName(_fromUtf8("chkIsLocal"))
        self.gridLayout.addWidget(self.chkIsLocal, 4, 1, 1, 1)
        self.lblName.setBuddy(self.edtName)
        self.lblCode.setBuddy(self.edtCode)
        self.lblQuota.setBuddy(self.edtQuota)
        self.lblFinances.setBuddy(self.tblAvailableFinances)
        self.lblPosition.setBuddy(self.edtPosition)
        self.lblIsLocal.setBuddy(self.chkIsLocal)

        self.retranslateUi(ItemEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ItemEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ItemEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ItemEditorDialog)
        ItemEditorDialog.setTabOrder(self.edtCode, self.edtPosition)
        ItemEditorDialog.setTabOrder(self.edtPosition, self.edtName)
        ItemEditorDialog.setTabOrder(self.edtName, self.chkIsLocal)
        ItemEditorDialog.setTabOrder(self.chkIsLocal, self.edtQuota)
        ItemEditorDialog.setTabOrder(self.edtQuota, self.tblAvailableFinances)
        ItemEditorDialog.setTabOrder(self.tblAvailableFinances, self.buttonBox)

    def retranslateUi(self, ItemEditorDialog):
        ItemEditorDialog.setWindowTitle(_translate("ItemEditorDialog", "Dialog", None))
        self.lblName.setText(_translate("ItemEditorDialog", "&Наименование", None))
        self.lblCode.setText(_translate("ItemEditorDialog", "&Код", None))
        self.lblQuota.setText(_translate("ItemEditorDialog", "К&вота", None))
        self.lblFinances.setText(_translate("ItemEditorDialog", "&Доступно", None))
        self.lblPosition.setText(_translate("ItemEditorDialog", "&Роль", None))
        self.lblIsLocal.setText(_translate("ItemEditorDialog", "&Локальный", None))

from library.InDocTable import CInDocTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ItemEditorDialog = QtGui.QDialog()
    ui = Ui_ItemEditorDialog()
    ui.setupUi(ItemEditorDialog)
    ItemEditorDialog.show()
    sys.exit(app.exec_())

