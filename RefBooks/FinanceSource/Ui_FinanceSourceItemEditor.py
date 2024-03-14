# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FinanceSourceItemEditor.ui'
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

class Ui_FinanceSourceItemEditor(object):
    def setupUi(self, FinanceSourceItemEditor):
        FinanceSourceItemEditor.setObjectName(_fromUtf8("FinanceSourceItemEditor"))
        FinanceSourceItemEditor.resize(363, 160)
        FinanceSourceItemEditor.setSizeGripEnabled(False)
        self.gridlayout = QtGui.QGridLayout(FinanceSourceItemEditor)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.lblCode = QtGui.QLabel(FinanceSourceItemEditor)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridlayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.edtName = QtGui.QLineEdit(FinanceSourceItemEditor)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridlayout.addWidget(self.edtName, 1, 1, 1, 1)
        self.lblName = QtGui.QLabel(FinanceSourceItemEditor)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridlayout.addWidget(self.lblName, 1, 0, 1, 1)
        self.edtCode = QtGui.QLineEdit(FinanceSourceItemEditor)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridlayout.addWidget(self.edtCode, 0, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(FinanceSourceItemEditor)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(103, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 3, 0, 1, 2)
        self.cmbFinance = CRBComboBox(FinanceSourceItemEditor)
        self.cmbFinance.setObjectName(_fromUtf8("cmbFinance"))
        self.gridlayout.addWidget(self.cmbFinance, 2, 1, 1, 1)
        self.lblFinance = QtGui.QLabel(FinanceSourceItemEditor)
        self.lblFinance.setObjectName(_fromUtf8("lblFinance"))
        self.gridlayout.addWidget(self.lblFinance, 2, 0, 1, 1)
        self.lblCode.setBuddy(self.edtCode)
        self.lblName.setBuddy(self.edtName)

        self.retranslateUi(FinanceSourceItemEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), FinanceSourceItemEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), FinanceSourceItemEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(FinanceSourceItemEditor)
        FinanceSourceItemEditor.setTabOrder(self.edtCode, self.edtName)

    def retranslateUi(self, FinanceSourceItemEditor):
        FinanceSourceItemEditor.setWindowTitle(_translate("FinanceSourceItemEditor", "ChangeMe!", None))
        self.lblCode.setText(_translate("FinanceSourceItemEditor", "&Код", None))
        self.lblName.setText(_translate("FinanceSourceItemEditor", "&Наименование", None))
        self.lblFinance.setText(_translate("FinanceSourceItemEditor", "Тип финансирования", None))

from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    FinanceSourceItemEditor = QtGui.QDialog()
    ui = Ui_FinanceSourceItemEditor()
    ui.setupUi(FinanceSourceItemEditor)
    FinanceSourceItemEditor.show()
    sys.exit(app.exec_())

