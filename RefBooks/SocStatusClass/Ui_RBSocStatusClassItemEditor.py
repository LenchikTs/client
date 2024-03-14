# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/RefBooks/RBSocStatusClassItemEditor.ui'
#
# Created: Wed Feb 19 22:52:37 2014
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SocStatusClassItemEditorDialog(object):
    def setupUi(self, SocStatusClassItemEditorDialog):
        SocStatusClassItemEditorDialog.setObjectName(_fromUtf8("SocStatusClassItemEditorDialog"))
        SocStatusClassItemEditorDialog.resize(400, 302)
        SocStatusClassItemEditorDialog.setSizeGripEnabled(True)
        self.gridlayout = QtGui.QGridLayout(SocStatusClassItemEditorDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.edtCode = QtGui.QLineEdit(SocStatusClassItemEditorDialog)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridlayout.addWidget(self.edtCode, 0, 1, 1, 1)
        self.lblName = QtGui.QLabel(SocStatusClassItemEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridlayout.addWidget(self.lblName, 1, 0, 1, 1)
        self.tblTypes = CInDocTableView(SocStatusClassItemEditorDialog)
        self.tblTypes.setObjectName(_fromUtf8("tblTypes"))
        self.gridlayout.addWidget(self.tblTypes, 2, 1, 2, 1)
        self.lblTypes = QtGui.QLabel(SocStatusClassItemEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTypes.sizePolicy().hasHeightForWidth())
        self.lblTypes.setSizePolicy(sizePolicy)
        self.lblTypes.setObjectName(_fromUtf8("lblTypes"))
        self.gridlayout.addWidget(self.lblTypes, 2, 0, 1, 1)
        self.edtName = QtGui.QLineEdit(SocStatusClassItemEditorDialog)
        self.edtName.setMinimumSize(QtCore.QSize(200, 0))
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridlayout.addWidget(self.edtName, 1, 1, 1, 1)
        self.lblCode = QtGui.QLabel(SocStatusClassItemEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridlayout.addWidget(self.lblCode, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(73, 171, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 3, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(SocStatusClassItemEditorDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.lblName.setBuddy(self.edtName)
        self.lblTypes.setBuddy(self.tblTypes)
        self.lblCode.setBuddy(self.edtCode)

        self.retranslateUi(SocStatusClassItemEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SocStatusClassItemEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SocStatusClassItemEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SocStatusClassItemEditorDialog)
        SocStatusClassItemEditorDialog.setTabOrder(self.edtCode, self.edtName)
        SocStatusClassItemEditorDialog.setTabOrder(self.edtName, self.tblTypes)

    def retranslateUi(self, SocStatusClassItemEditorDialog):
        SocStatusClassItemEditorDialog.setWindowTitle(QtGui.QApplication.translate("SocStatusClassItemEditorDialog", "ChangeMe!", None, QtGui.QApplication.UnicodeUTF8))
        self.lblName.setText(QtGui.QApplication.translate("SocStatusClassItemEditorDialog", "На&именование", None, QtGui.QApplication.UnicodeUTF8))
        self.lblTypes.setText(QtGui.QApplication.translate("SocStatusClassItemEditorDialog", "Льготы", None, QtGui.QApplication.UnicodeUTF8))
        self.lblCode.setText(QtGui.QApplication.translate("SocStatusClassItemEditorDialog", "&Код", None, QtGui.QApplication.UnicodeUTF8))

from library.InDocTable import CInDocTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SocStatusClassItemEditorDialog = QtGui.QDialog()
    ui = Ui_SocStatusClassItemEditorDialog()
    ui.setupUi(SocStatusClassItemEditorDialog)
    SocStatusClassItemEditorDialog.show()
    sys.exit(app.exec_())

