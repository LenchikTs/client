# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Rabota\s11\RefBooks\NomenclatureActiveSubstance\RBNomenclatureActiveSubstanceEditor.ui'
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

class Ui_RBNomenclatureActiveSubstanceEditor(object):
    def setupUi(self, RBNomenclatureActiveSubstanceEditor):
        RBNomenclatureActiveSubstanceEditor.setObjectName(_fromUtf8("RBNomenclatureActiveSubstanceEditor"))
        RBNomenclatureActiveSubstanceEditor.resize(632, 423)
        RBNomenclatureActiveSubstanceEditor.setSizeGripEnabled(True)
        self.gridLayout_2 = QtGui.QGridLayout(RBNomenclatureActiveSubstanceEditor)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tabWidget = QtGui.QTabWidget(RBNomenclatureActiveSubstanceEditor)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabMain = QtGui.QWidget()
        self.tabMain.setObjectName(_fromUtf8("tabMain"))
        self.gridLayout = QtGui.QGridLayout(self.tabMain)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtCode = QtGui.QLineEdit(self.tabMain)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout.addWidget(self.edtCode, 0, 1, 1, 1)
        self.lblATC = QtGui.QLabel(self.tabMain)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblATC.sizePolicy().hasHeightForWidth())
        self.lblATC.setSizePolicy(sizePolicy)
        self.lblATC.setObjectName(_fromUtf8("lblATC"))
        self.gridLayout.addWidget(self.lblATC, 3, 0, 1, 1)
        self.edtNameLatin = QtGui.QLineEdit(self.tabMain)
        self.edtNameLatin.setObjectName(_fromUtf8("edtNameLatin"))
        self.gridLayout.addWidget(self.edtNameLatin, 2, 1, 1, 1)
        self.edtATC = QtGui.QLineEdit(self.tabMain)
        self.edtATC.setObjectName(_fromUtf8("edtATC"))
        self.gridLayout.addWidget(self.edtATC, 3, 1, 1, 1)
        self.lblNameLatin = QtGui.QLabel(self.tabMain)
        self.lblNameLatin.setObjectName(_fromUtf8("lblNameLatin"))
        self.gridLayout.addWidget(self.lblNameLatin, 2, 0, 1, 1)
        self.lbDosageUnit = QtGui.QLabel(self.tabMain)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbDosageUnit.sizePolicy().hasHeightForWidth())
        self.lbDosageUnit.setSizePolicy(sizePolicy)
        self.lbDosageUnit.setObjectName(_fromUtf8("lbDosageUnit"))
        self.gridLayout.addWidget(self.lbDosageUnit, 4, 0, 1, 1)
        self.lblNameRussian = QtGui.QLabel(self.tabMain)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblNameRussian.sizePolicy().hasHeightForWidth())
        self.lblNameRussian.setSizePolicy(sizePolicy)
        self.lblNameRussian.setObjectName(_fromUtf8("lblNameRussian"))
        self.gridLayout.addWidget(self.lblNameRussian, 1, 0, 1, 1)
        self.lblCode = QtGui.QLabel(self.tabMain)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.edtNameRussian = QtGui.QLineEdit(self.tabMain)
        self.edtNameRussian.setObjectName(_fromUtf8("edtNameRussian"))
        self.gridLayout.addWidget(self.edtNameRussian, 1, 1, 1, 1)
        self.cmbUnit = CRBComboBox(self.tabMain)
        self.cmbUnit.setObjectName(_fromUtf8("cmbUnit"))
        self.gridLayout.addWidget(self.cmbUnit, 4, 1, 1, 1)
        self.tblActiveSubstanceGroups = CInDocTableView(self.tabMain)
        self.tblActiveSubstanceGroups.setObjectName(_fromUtf8("tblActiveSubstanceGroups"))
        self.gridLayout.addWidget(self.tblActiveSubstanceGroups, 5, 0, 1, 2)
        self.tabWidget.addTab(self.tabMain, _fromUtf8(""))
        self.tabIdentification = QtGui.QWidget()
        self.tabIdentification.setObjectName(_fromUtf8("tabIdentification"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tabIdentification)
        self.gridLayout_3.setMargin(4)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.tblIdentification = CInDocTableView(self.tabIdentification)
        self.tblIdentification.setObjectName(_fromUtf8("tblIdentification"))
        self.gridLayout_3.addWidget(self.tblIdentification, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabIdentification, _fromUtf8(""))
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RBNomenclatureActiveSubstanceEditor)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.lblATC.setBuddy(self.edtATC)
        self.lblNameRussian.setBuddy(self.edtNameRussian)
        self.lblCode.setBuddy(self.edtCode)

        self.retranslateUi(RBNomenclatureActiveSubstanceEditor)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBNomenclatureActiveSubstanceEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBNomenclatureActiveSubstanceEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(RBNomenclatureActiveSubstanceEditor)
        RBNomenclatureActiveSubstanceEditor.setTabOrder(self.edtCode, self.edtNameRussian)
        RBNomenclatureActiveSubstanceEditor.setTabOrder(self.edtNameRussian, self.edtNameLatin)
        RBNomenclatureActiveSubstanceEditor.setTabOrder(self.edtNameLatin, self.edtATC)
        RBNomenclatureActiveSubstanceEditor.setTabOrder(self.edtATC, self.cmbUnit)
        RBNomenclatureActiveSubstanceEditor.setTabOrder(self.cmbUnit, self.tblActiveSubstanceGroups)
        RBNomenclatureActiveSubstanceEditor.setTabOrder(self.tblActiveSubstanceGroups, self.buttonBox)
        RBNomenclatureActiveSubstanceEditor.setTabOrder(self.buttonBox, self.tabWidget)
        RBNomenclatureActiveSubstanceEditor.setTabOrder(self.tabWidget, self.tblIdentification)

    def retranslateUi(self, RBNomenclatureActiveSubstanceEditor):
        RBNomenclatureActiveSubstanceEditor.setWindowTitle(_translate("RBNomenclatureActiveSubstanceEditor", "ChangeMe!", None))
        self.lblATC.setText(_translate("RBNomenclatureActiveSubstanceEditor", "Код &АТХ", None))
        self.lblNameLatin.setText(_translate("RBNomenclatureActiveSubstanceEditor", "Наименование на латыни", None))
        self.lbDosageUnit.setText(_translate("RBNomenclatureActiveSubstanceEditor", "Ед. Дозировки", None))
        self.lblNameRussian.setText(_translate("RBNomenclatureActiveSubstanceEditor", "Наименование на русском", None))
        self.lblCode.setText(_translate("RBNomenclatureActiveSubstanceEditor", "&Код", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMain), _translate("RBNomenclatureActiveSubstanceEditor", "Описание", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabIdentification), _translate("RBNomenclatureActiveSubstanceEditor", "Идентификация", None))

from library.InDocTable import CInDocTableView
from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RBNomenclatureActiveSubstanceEditor = QtGui.QDialog()
    ui = Ui_RBNomenclatureActiveSubstanceEditor()
    ui.setupUi(RBNomenclatureActiveSubstanceEditor)
    RBNomenclatureActiveSubstanceEditor.show()
    sys.exit(app.exec_())

