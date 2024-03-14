# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Rabota\s11\RefBooks\NomenclatureActiveSubstance\ActiveSubstanceComboBoxPopup.ui'
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

class Ui_ActiveSubstanceComboBoxPopup(object):
    def setupUi(self, ActiveSubstanceComboBoxPopup):
        ActiveSubstanceComboBoxPopup.setObjectName(_fromUtf8("ActiveSubstanceComboBoxPopup"))
        ActiveSubstanceComboBoxPopup.resize(687, 453)
        self.gridLayout = QtGui.QGridLayout(ActiveSubstanceComboBoxPopup)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtFindName = QtGui.QLineEdit(ActiveSubstanceComboBoxPopup)
        self.edtFindName.setObjectName(_fromUtf8("edtFindName"))
        self.gridLayout.addWidget(self.edtFindName, 0, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(479, 17, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ActiveSubstanceComboBoxPopup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Reset)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 1, 1, 1)
        self.tblActiveSubstance = CTableView(ActiveSubstanceComboBoxPopup)
        self.tblActiveSubstance.setObjectName(_fromUtf8("tblActiveSubstance"))
        self.gridLayout.addWidget(self.tblActiveSubstance, 2, 0, 1, 2)

        self.retranslateUi(ActiveSubstanceComboBoxPopup)
        QtCore.QMetaObject.connectSlotsByName(ActiveSubstanceComboBoxPopup)

    def retranslateUi(self, ActiveSubstanceComboBoxPopup):
        ActiveSubstanceComboBoxPopup.setWindowTitle(_translate("ActiveSubstanceComboBoxPopup", "Form", None))

from library.TableView import CTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ActiveSubstanceComboBoxPopup = QtGui.QWidget()
    ui = Ui_ActiveSubstanceComboBoxPopup()
    ui.setupUi(ActiveSubstanceComboBoxPopup)
    ActiveSubstanceComboBoxPopup.show()
    sys.exit(app.exec_())

