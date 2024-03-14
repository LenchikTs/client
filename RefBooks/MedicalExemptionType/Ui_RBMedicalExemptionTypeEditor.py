# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/RefBooks/RBMedicalExemptionTypeEditor.ui'
#
# Created: Wed Feb 19 22:56:09 2014
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RBMedicalExemptionTypeEditor(object):
    def setupUi(self, RBMedicalExemptionTypeEditor):
        RBMedicalExemptionTypeEditor.setObjectName(_fromUtf8("RBMedicalExemptionTypeEditor"))
        RBMedicalExemptionTypeEditor.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(RBMedicalExemptionTypeEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblCode = QtGui.QLabel(RBMedicalExemptionTypeEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.edtCode = QtGui.QLineEdit(RBMedicalExemptionTypeEditor)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout.addWidget(self.edtCode, 0, 1, 1, 1)
        self.lblName = QtGui.QLabel(RBMedicalExemptionTypeEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 1, 0, 1, 1)
        self.edtName = QtGui.QLineEdit(RBMedicalExemptionTypeEditor)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 1, 1, 1, 1)
        self.tblMedicalExemptionTypeInfections = CInDocTableView(RBMedicalExemptionTypeEditor)
        self.tblMedicalExemptionTypeInfections.setObjectName(_fromUtf8("tblMedicalExemptionTypeInfections"))
        self.gridLayout.addWidget(self.tblMedicalExemptionTypeInfections, 2, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(RBMedicalExemptionTypeEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)
        self.lblCode.setBuddy(self.edtCode)
        self.lblName.setBuddy(self.edtName)

        self.retranslateUi(RBMedicalExemptionTypeEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBMedicalExemptionTypeEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBMedicalExemptionTypeEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(RBMedicalExemptionTypeEditor)

    def retranslateUi(self, RBMedicalExemptionTypeEditor):
        RBMedicalExemptionTypeEditor.setWindowTitle(QtGui.QApplication.translate("RBMedicalExemptionTypeEditor", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.lblCode.setText(QtGui.QApplication.translate("RBMedicalExemptionTypeEditor", "&Код", None, QtGui.QApplication.UnicodeUTF8))
        self.lblName.setText(QtGui.QApplication.translate("RBMedicalExemptionTypeEditor", "&Наименование", None, QtGui.QApplication.UnicodeUTF8))

from library.InDocTable import CInDocTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RBMedicalExemptionTypeEditor = QtGui.QDialog()
    ui = Ui_RBMedicalExemptionTypeEditor()
    ui.setupUi(RBMedicalExemptionTypeEditor)
    RBMedicalExemptionTypeEditor.show()
    sys.exit(app.exec_())

