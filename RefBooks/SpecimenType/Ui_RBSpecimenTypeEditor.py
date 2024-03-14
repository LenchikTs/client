# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/RefBooks/RBSpecimenTypeEditor.ui'
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

class Ui_SpecimenTypeEditorDialog(object):
    def setupUi(self, SpecimenTypeEditorDialog):
        SpecimenTypeEditorDialog.setObjectName(_fromUtf8("SpecimenTypeEditorDialog"))
        SpecimenTypeEditorDialog.resize(345, 165)
        self.gridLayout_2 = QtGui.QGridLayout(SpecimenTypeEditorDialog)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tabWidget = QtGui.QTabWidget(SpecimenTypeEditorDialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabMain = QtGui.QWidget()
        self.tabMain.setObjectName(_fromUtf8("tabMain"))
        self.gridLayout = QtGui.QGridLayout(self.tabMain)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblLatinName = QtGui.QLabel(self.tabMain)
        self.lblLatinName.setObjectName(_fromUtf8("lblLatinName"))
        self.gridLayout.addWidget(self.lblLatinName, 2, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.edtLatinName = QtGui.QLineEdit(self.tabMain)
        self.edtLatinName.setObjectName(_fromUtf8("edtLatinName"))
        self.gridLayout.addWidget(self.edtLatinName, 2, 1, 1, 1)
        self.lblName = QtGui.QLabel(self.tabMain)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 1, 0, 1, 1)
        self.edtName = QtGui.QLineEdit(self.tabMain)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 1, 1, 1, 1)
        self.edtCode = QtGui.QLineEdit(self.tabMain)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout.addWidget(self.edtCode, 0, 1, 1, 1)
        self.lblCode = QtGui.QLabel(self.tabMain)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout.addWidget(self.lblCode, 0, 0, 1, 1)
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
        self.gridLayout_2.addWidget(self.tabWidget, 2, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(SpecimenTypeEditorDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 3, 0, 1, 2)
        self.lblLatinName.setBuddy(self.edtLatinName)
        self.lblName.setBuddy(self.edtName)
        self.lblCode.setBuddy(self.edtCode)

        self.retranslateUi(SpecimenTypeEditorDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SpecimenTypeEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SpecimenTypeEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SpecimenTypeEditorDialog)
        SpecimenTypeEditorDialog.setTabOrder(self.tabWidget, self.edtLatinName)
        SpecimenTypeEditorDialog.setTabOrder(self.edtLatinName, self.tblIdentification)
        SpecimenTypeEditorDialog.setTabOrder(self.tblIdentification, self.buttonBox)

    def retranslateUi(self, SpecimenTypeEditorDialog):
        SpecimenTypeEditorDialog.setWindowTitle(_translate("SpecimenTypeEditorDialog", "Dialog", None))
        self.lblLatinName.setText(_translate("SpecimenTypeEditorDialog", "&Латинское наименование", None))
        self.lblName.setText(_translate("SpecimenTypeEditorDialog", "&Наименование", None))
        self.lblCode.setText(_translate("SpecimenTypeEditorDialog", "&Код", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMain), _translate("SpecimenTypeEditorDialog", "&Основная информация", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabIdentification), _translate("SpecimenTypeEditorDialog", "&Идентификация", None))

from library.InDocTable import CInDocTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SpecimenTypeEditorDialog = QtGui.QDialog()
    ui = Ui_SpecimenTypeEditorDialog()
    ui.setupUi(SpecimenTypeEditorDialog)
    SpecimenTypeEditorDialog.show()
    sys.exit(app.exec_())

