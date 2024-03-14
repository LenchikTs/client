# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Rabota\s11\RefBooks\NomenclatureActiveSubstanceGroups\RBNomenclatureActiveSubstanceGroupsEditor.ui'
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

class Ui_RBNomenclatureActiveSubstanceGroupsEditor(object):
    def setupUi(self, RBNomenclatureActiveSubstanceGroupsEditor):
        RBNomenclatureActiveSubstanceGroupsEditor.setObjectName(_fromUtf8("RBNomenclatureActiveSubstanceGroupsEditor"))
        RBNomenclatureActiveSubstanceGroupsEditor.resize(692, 115)
        RBNomenclatureActiveSubstanceGroupsEditor.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(RBNomenclatureActiveSubstanceGroupsEditor)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblCode = QtGui.QLabel(RBNomenclatureActiveSubstanceGroupsEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.edtCode = QtGui.QLineEdit(RBNomenclatureActiveSubstanceGroupsEditor)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout.addWidget(self.edtCode, 0, 1, 1, 2)
        self.lblName = QtGui.QLabel(RBNomenclatureActiveSubstanceGroupsEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 1, 0, 1, 1)
        self.edtName = QtGui.QLineEdit(RBNomenclatureActiveSubstanceGroupsEditor)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 1, 1, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 13, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RBNomenclatureActiveSubstanceGroupsEditor)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 2, 1, 1)
        self.lblCode.setBuddy(self.edtCode)
        self.lblName.setBuddy(self.edtName)

        self.retranslateUi(RBNomenclatureActiveSubstanceGroupsEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBNomenclatureActiveSubstanceGroupsEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBNomenclatureActiveSubstanceGroupsEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(RBNomenclatureActiveSubstanceGroupsEditor)
        RBNomenclatureActiveSubstanceGroupsEditor.setTabOrder(self.edtCode, self.edtName)
        RBNomenclatureActiveSubstanceGroupsEditor.setTabOrder(self.edtName, self.buttonBox)

    def retranslateUi(self, RBNomenclatureActiveSubstanceGroupsEditor):
        RBNomenclatureActiveSubstanceGroupsEditor.setWindowTitle(_translate("RBNomenclatureActiveSubstanceGroupsEditor", "ChangeMe!", None))
        self.lblCode.setText(_translate("RBNomenclatureActiveSubstanceGroupsEditor", "&Код", None))
        self.lblName.setText(_translate("RBNomenclatureActiveSubstanceGroupsEditor", "Наименование", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RBNomenclatureActiveSubstanceGroupsEditor = QtGui.QDialog()
    ui = Ui_RBNomenclatureActiveSubstanceGroupsEditor()
    ui.setupUi(RBNomenclatureActiveSubstanceGroupsEditor)
    RBNomenclatureActiveSubstanceGroupsEditor.show()
    sys.exit(app.exec_())

