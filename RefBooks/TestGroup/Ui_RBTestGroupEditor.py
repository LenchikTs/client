# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RBTestGroupEditor.ui'
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

class Ui_RBTestGroupEditor(object):
    def setupUi(self, RBTestGroupEditor):
        RBTestGroupEditor.setObjectName(_fromUtf8("RBTestGroupEditor"))
        RBTestGroupEditor.resize(320, 86)
        RBTestGroupEditor.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(RBTestGroupEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.lblName = QtGui.QLabel(RBTestGroupEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 1, 0, 1, 1)
        self.edtName = QtGui.QLineEdit(RBTestGroupEditor)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 1, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RBTestGroupEditor)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.lblCode = QtGui.QLabel(RBTestGroupEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.edtCode = QtGui.QLineEdit(RBTestGroupEditor)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout.addWidget(self.edtCode, 0, 1, 1, 1)
        self.lblName.setBuddy(self.edtName)
        self.lblCode.setBuddy(self.edtCode)

        self.retranslateUi(RBTestGroupEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBTestGroupEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBTestGroupEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(RBTestGroupEditor)
        RBTestGroupEditor.setTabOrder(self.edtCode, self.edtName)
        RBTestGroupEditor.setTabOrder(self.edtName, self.buttonBox)

    def retranslateUi(self, RBTestGroupEditor):
        RBTestGroupEditor.setWindowTitle(_translate("RBTestGroupEditor", "Dialog", None))
        self.lblName.setText(_translate("RBTestGroupEditor", "&Наименование", None))
        self.lblCode.setText(_translate("RBTestGroupEditor", "&Код", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RBTestGroupEditor = QtGui.QDialog()
    ui = Ui_RBTestGroupEditor()
    ui.setupUi(RBTestGroupEditor)
    RBTestGroupEditor.show()
    sys.exit(app.exec_())

