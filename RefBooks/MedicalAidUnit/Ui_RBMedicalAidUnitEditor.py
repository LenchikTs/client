# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/RefBooks/RBMedicalAidUnitEditor.ui'
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

class Ui_ItemEditorDialog(object):
    def setupUi(self, ItemEditorDialog):
        ItemEditorDialog.setObjectName(_fromUtf8("ItemEditorDialog"))
        ItemEditorDialog.resize(320, 245)
        ItemEditorDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(ItemEditorDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(ItemEditorDialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabMain = QtGui.QWidget()
        self.tabMain.setObjectName(_fromUtf8("tabMain"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tabMain)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lblCode = QtGui.QLabel(self.tabMain)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout_2.addWidget(self.lblCode, 0, 0, 1, 1)
        self.lblRegionalCode = QtGui.QLabel(self.tabMain)
        self.lblRegionalCode.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblRegionalCode.sizePolicy().hasHeightForWidth())
        self.lblRegionalCode.setSizePolicy(sizePolicy)
        self.lblRegionalCode.setObjectName(_fromUtf8("lblRegionalCode"))
        self.gridLayout_2.addWidget(self.lblRegionalCode, 3, 0, 1, 1)
        self.edtRegionalCode = QtGui.QLineEdit(self.tabMain)
        self.edtRegionalCode.setEnabled(False)
        self.edtRegionalCode.setObjectName(_fromUtf8("edtRegionalCode"))
        self.gridLayout_2.addWidget(self.edtRegionalCode, 3, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(73, 36, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 5, 0, 1, 1)
        self.lblFederalCode = QtGui.QLabel(self.tabMain)
        self.lblFederalCode.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblFederalCode.sizePolicy().hasHeightForWidth())
        self.lblFederalCode.setSizePolicy(sizePolicy)
        self.lblFederalCode.setObjectName(_fromUtf8("lblFederalCode"))
        self.gridLayout_2.addWidget(self.lblFederalCode, 2, 0, 1, 1)
        self.edtName = QtGui.QLineEdit(self.tabMain)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout_2.addWidget(self.edtName, 1, 1, 1, 1)
        self.lblName = QtGui.QLabel(self.tabMain)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout_2.addWidget(self.lblName, 1, 0, 1, 1)
        self.edtCode = QtGui.QLineEdit(self.tabMain)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout_2.addWidget(self.edtCode, 0, 1, 1, 1)
        self.edtFederalCode = QtGui.QLineEdit(self.tabMain)
        self.edtFederalCode.setEnabled(False)
        self.edtFederalCode.setObjectName(_fromUtf8("edtFederalCode"))
        self.gridLayout_2.addWidget(self.edtFederalCode, 2, 1, 1, 1)
        self.lblDescr = QtGui.QLabel(self.tabMain)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDescr.sizePolicy().hasHeightForWidth())
        self.lblDescr.setSizePolicy(sizePolicy)
        self.lblDescr.setObjectName(_fromUtf8("lblDescr"))
        self.gridLayout_2.addWidget(self.lblDescr, 4, 0, 1, 1)
        self.edtDescr = QtGui.QLineEdit(self.tabMain)
        self.edtDescr.setMaxLength(64)
        self.edtDescr.setObjectName(_fromUtf8("edtDescr"))
        self.gridLayout_2.addWidget(self.edtDescr, 4, 1, 1, 1)
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
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ItemEditorDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.lblCode.setBuddy(self.edtCode)
        self.lblRegionalCode.setBuddy(self.edtRegionalCode)
        self.lblFederalCode.setBuddy(self.edtFederalCode)
        self.lblName.setBuddy(self.edtName)
        self.lblDescr.setBuddy(self.edtDescr)

        self.retranslateUi(ItemEditorDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ItemEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ItemEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ItemEditorDialog)
        ItemEditorDialog.setTabOrder(self.tabWidget, self.edtCode)
        ItemEditorDialog.setTabOrder(self.edtCode, self.edtName)
        ItemEditorDialog.setTabOrder(self.edtName, self.edtFederalCode)
        ItemEditorDialog.setTabOrder(self.edtFederalCode, self.edtRegionalCode)
        ItemEditorDialog.setTabOrder(self.edtRegionalCode, self.edtDescr)
        ItemEditorDialog.setTabOrder(self.edtDescr, self.tblIdentification)
        ItemEditorDialog.setTabOrder(self.tblIdentification, self.buttonBox)

    def retranslateUi(self, ItemEditorDialog):
        ItemEditorDialog.setWindowTitle(_translate("ItemEditorDialog", "ChangeMe!", None))
        self.lblCode.setText(_translate("ItemEditorDialog", "&Код", None))
        self.lblRegionalCode.setText(_translate("ItemEditorDialog", "&Региональный код", None))
        self.lblFederalCode.setText(_translate("ItemEditorDialog", "&Федеральный код", None))
        self.lblName.setText(_translate("ItemEditorDialog", "&Наименование", None))
        self.lblDescr.setText(_translate("ItemEditorDialog", "О&писание", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMain), _translate("ItemEditorDialog", "&Основная информация", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabIdentification), _translate("ItemEditorDialog", "&Идентификация", None))

from library.InDocTable import CInDocTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ItemEditorDialog = QtGui.QDialog()
    ui = Ui_ItemEditorDialog()
    ui.setupUi(ItemEditorDialog)
    ItemEditorDialog.show()
    sys.exit(app.exec_())

