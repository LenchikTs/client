# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/RefBooks/RBMenu.ui'
#
# Created: Fri Feb 21 13:43:49 2014
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RBMenu(object):
    def setupUi(self, RBMenu):
        RBMenu.setObjectName(_fromUtf8("RBMenu"))
        RBMenu.resize(400, 233)
        RBMenu.setSizeGripEnabled(True)
        self.gridlayout = QtGui.QGridLayout(RBMenu)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.lblName = QtGui.QLabel(RBMenu)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridlayout.addWidget(self.lblName, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RBMenu)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 3, 0, 1, 2)
        self.tblMenuContent = CInDocTableView(RBMenu)
        self.tblMenuContent.setObjectName(_fromUtf8("tblMenuContent"))
        self.gridlayout.addWidget(self.tblMenuContent, 2, 0, 1, 2)
        self.lblCode = QtGui.QLabel(RBMenu)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridlayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.edtCode = QtGui.QLineEdit(RBMenu)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridlayout.addWidget(self.edtCode, 0, 1, 1, 1)
        self.edtName = QtGui.QLineEdit(RBMenu)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridlayout.addWidget(self.edtName, 1, 1, 1, 1)
        self.lblName.setBuddy(self.edtName)
        self.lblCode.setBuddy(self.edtCode)

        self.retranslateUi(RBMenu)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBMenu.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBMenu.reject)
        QtCore.QMetaObject.connectSlotsByName(RBMenu)
        RBMenu.setTabOrder(self.edtCode, self.edtName)
        RBMenu.setTabOrder(self.edtName, self.tblMenuContent)

    def retranslateUi(self, RBMenu):
        RBMenu.setWindowTitle(QtGui.QApplication.translate("RBMenu", "ChangeMe!", None, QtGui.QApplication.UnicodeUTF8))
        self.lblName.setText(QtGui.QApplication.translate("RBMenu", "&Наименование", None, QtGui.QApplication.UnicodeUTF8))
        self.lblCode.setText(QtGui.QApplication.translate("RBMenu", "&Код", None, QtGui.QApplication.UnicodeUTF8))

from library.InDocTable import CInDocTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RBMenu = QtGui.QDialog()
    ui = Ui_RBMenu()
    ui.setupUi(RBMenu)
    RBMenu.show()
    sys.exit(app.exec_())

