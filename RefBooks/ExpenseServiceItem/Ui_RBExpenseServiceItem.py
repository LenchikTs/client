# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/RefBooks/RBExpenseServiceItem.ui'
#
# Created: Wed Feb 19 22:55:52 2014
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RBExpenseServiceItem(object):
    def setupUi(self, RBExpenseServiceItem):
        RBExpenseServiceItem.setObjectName(_fromUtf8("RBExpenseServiceItem"))
        RBExpenseServiceItem.resize(320, 115)
        RBExpenseServiceItem.setSizeGripEnabled(True)
        self.gridlayout = QtGui.QGridLayout(RBExpenseServiceItem)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.edtCode = QtGui.QLineEdit(RBExpenseServiceItem)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridlayout.addWidget(self.edtCode, 0, 1, 1, 1)
        self.lblName = QtGui.QLabel(RBExpenseServiceItem)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridlayout.addWidget(self.lblName, 1, 0, 1, 1)
        self.edtName = QtGui.QLineEdit(RBExpenseServiceItem)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridlayout.addWidget(self.edtName, 1, 1, 1, 1)
        self.lblCode = QtGui.QLabel(RBExpenseServiceItem)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridlayout.addWidget(self.lblCode, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(103, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RBExpenseServiceItem)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.chkIsBase = QtGui.QCheckBox(RBExpenseServiceItem)
        self.chkIsBase.setObjectName(_fromUtf8("chkIsBase"))
        self.gridlayout.addWidget(self.chkIsBase, 3, 0, 1, 2)
        self.lblName.setBuddy(self.edtName)
        self.lblCode.setBuddy(self.edtCode)

        self.retranslateUi(RBExpenseServiceItem)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBExpenseServiceItem.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBExpenseServiceItem.reject)
        QtCore.QMetaObject.connectSlotsByName(RBExpenseServiceItem)
        RBExpenseServiceItem.setTabOrder(self.edtCode, self.edtName)

    def retranslateUi(self, RBExpenseServiceItem):
        RBExpenseServiceItem.setWindowTitle(QtGui.QApplication.translate("RBExpenseServiceItem", "ChangeMe!", None, QtGui.QApplication.UnicodeUTF8))
        self.lblName.setText(QtGui.QApplication.translate("RBExpenseServiceItem", "&Наименование", None, QtGui.QApplication.UnicodeUTF8))
        self.lblCode.setText(QtGui.QApplication.translate("RBExpenseServiceItem", "&Код", None, QtGui.QApplication.UnicodeUTF8))
        self.chkIsBase.setText(QtGui.QApplication.translate("RBExpenseServiceItem", "является базовой", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RBExpenseServiceItem = QtGui.QDialog()
    ui = Ui_RBExpenseServiceItem()
    ui.setupUi(RBExpenseServiceItem)
    RBExpenseServiceItem.show()
    sys.exit(app.exec_())

