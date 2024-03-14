# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/RefBooks/Equipment/SpecimenTypeChoiceDialog.ui'
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

class Ui_SpecimenTypeChoiceDialog(object):
    def setupUi(self, SpecimenTypeChoiceDialog):
        SpecimenTypeChoiceDialog.setObjectName(_fromUtf8("SpecimenTypeChoiceDialog"))
        SpecimenTypeChoiceDialog.resize(345, 113)
        self.gridLayout = QtGui.QGridLayout(SpecimenTypeChoiceDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblSpecimenType = QtGui.QLabel(SpecimenTypeChoiceDialog)
        self.lblSpecimenType.setObjectName(_fromUtf8("lblSpecimenType"))
        self.gridLayout.addWidget(self.lblSpecimenType, 0, 0, 1, 1)
        self.cmbSpecimenType = CRBComboBox(SpecimenTypeChoiceDialog)
        self.cmbSpecimenType.setObjectName(_fromUtf8("cmbSpecimenType"))
        self.gridLayout.addWidget(self.cmbSpecimenType, 0, 1, 1, 1)
        self.lblSpecimenCode = QtGui.QLabel(SpecimenTypeChoiceDialog)
        self.lblSpecimenCode.setObjectName(_fromUtf8("lblSpecimenCode"))
        self.gridLayout.addWidget(self.lblSpecimenCode, 1, 0, 1, 1)
        self.edtSpecimenCode = QtGui.QLineEdit(SpecimenTypeChoiceDialog)
        self.edtSpecimenCode.setObjectName(_fromUtf8("edtSpecimenCode"))
        self.gridLayout.addWidget(self.edtSpecimenCode, 1, 1, 1, 1)
        self.lblSpecimenName = QtGui.QLabel(SpecimenTypeChoiceDialog)
        self.lblSpecimenName.setObjectName(_fromUtf8("lblSpecimenName"))
        self.gridLayout.addWidget(self.lblSpecimenName, 2, 0, 1, 1)
        self.edtSpecimenName = QtGui.QLineEdit(SpecimenTypeChoiceDialog)
        self.edtSpecimenName.setObjectName(_fromUtf8("edtSpecimenName"))
        self.gridLayout.addWidget(self.edtSpecimenName, 2, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(SpecimenTypeChoiceDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 2)

        self.retranslateUi(SpecimenTypeChoiceDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SpecimenTypeChoiceDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SpecimenTypeChoiceDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SpecimenTypeChoiceDialog)

    def retranslateUi(self, SpecimenTypeChoiceDialog):
        SpecimenTypeChoiceDialog.setWindowTitle(_translate("SpecimenTypeChoiceDialog", "Dialog", None))
        self.lblSpecimenType.setText(_translate("SpecimenTypeChoiceDialog", "Тип образца", None))
        self.lblSpecimenCode.setText(_translate("SpecimenTypeChoiceDialog", "Код образца", None))
        self.lblSpecimenName.setText(_translate("SpecimenTypeChoiceDialog", "Наименование образца", None))

from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SpecimenTypeChoiceDialog = QtGui.QDialog()
    ui = Ui_SpecimenTypeChoiceDialog()
    ui.setupUi(SpecimenTypeChoiceDialog)
    SpecimenTypeChoiceDialog.show()
    sys.exit(app.exec_())

