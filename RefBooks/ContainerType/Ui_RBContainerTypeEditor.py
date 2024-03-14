# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/RefBooks/RBContainerTypeEditor.ui'
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

class Ui_RBContainerTypeEditor(object):
    def setupUi(self, RBContainerTypeEditor):
        RBContainerTypeEditor.setObjectName(_fromUtf8("RBContainerTypeEditor"))
        RBContainerTypeEditor.resize(390, 234)
        RBContainerTypeEditor.setSizeGripEnabled(True)
        self.gridLayout_2 = QtGui.QGridLayout(RBContainerTypeEditor)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tabWidget = QtGui.QTabWidget(RBContainerTypeEditor)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabMain = QtGui.QWidget()
        self.tabMain.setObjectName(_fromUtf8("tabMain"))
        self.gridLayout = QtGui.QGridLayout(self.tabMain)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblUnit = QtGui.QLabel(self.tabMain)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblUnit.sizePolicy().hasHeightForWidth())
        self.lblUnit.setSizePolicy(sizePolicy)
        self.lblUnit.setObjectName(_fromUtf8("lblUnit"))
        self.gridLayout.addWidget(self.lblUnit, 4, 0, 1, 1)
        self.cmbUnit = CRBComboBox(self.tabMain)
        self.cmbUnit.setObjectName(_fromUtf8("cmbUnit"))
        self.gridLayout.addWidget(self.cmbUnit, 4, 1, 1, 1)
        self.lblColor = QtGui.QLabel(self.tabMain)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblColor.sizePolicy().hasHeightForWidth())
        self.lblColor.setSizePolicy(sizePolicy)
        self.lblColor.setObjectName(_fromUtf8("lblColor"))
        self.gridLayout.addWidget(self.lblColor, 2, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 120, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)
        self.cmbColor = CColorComboBox(self.tabMain)
        self.cmbColor.setObjectName(_fromUtf8("cmbColor"))
        self.gridLayout.addWidget(self.cmbColor, 2, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 2, 1, 1)
        self.lblAmount = QtGui.QLabel(self.tabMain)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblAmount.sizePolicy().hasHeightForWidth())
        self.lblAmount.setSizePolicy(sizePolicy)
        self.lblAmount.setObjectName(_fromUtf8("lblAmount"))
        self.gridLayout.addWidget(self.lblAmount, 3, 0, 1, 1)
        self.edtName = QtGui.QLineEdit(self.tabMain)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 1, 1, 1, 2)
        self.lblName = QtGui.QLabel(self.tabMain)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 1, 0, 1, 1)
        self.edtCode = QtGui.QLineEdit(self.tabMain)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout.addWidget(self.edtCode, 0, 1, 1, 2)
        self.lblCode = QtGui.QLabel(self.tabMain)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.edtAmount = QtGui.QDoubleSpinBox(self.tabMain)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtAmount.sizePolicy().hasHeightForWidth())
        self.edtAmount.setSizePolicy(sizePolicy)
        self.edtAmount.setDecimals(1)
        self.edtAmount.setMaximum(1000.0)
        self.edtAmount.setObjectName(_fromUtf8("edtAmount"))
        self.gridLayout.addWidget(self.edtAmount, 3, 1, 1, 2)
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
        self.buttonBox = QtGui.QDialogButtonBox(RBContainerTypeEditor)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 3, 0, 1, 2)
        self.lblUnit.setBuddy(self.cmbUnit)
        self.lblColor.setBuddy(self.cmbColor)
        self.lblAmount.setBuddy(self.edtAmount)
        self.lblName.setBuddy(self.edtName)
        self.lblCode.setBuddy(self.edtCode)

        self.retranslateUi(RBContainerTypeEditor)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBContainerTypeEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBContainerTypeEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(RBContainerTypeEditor)
        RBContainerTypeEditor.setTabOrder(self.tabWidget, self.edtCode)
        RBContainerTypeEditor.setTabOrder(self.edtCode, self.edtName)
        RBContainerTypeEditor.setTabOrder(self.edtName, self.cmbColor)
        RBContainerTypeEditor.setTabOrder(self.cmbColor, self.edtAmount)
        RBContainerTypeEditor.setTabOrder(self.edtAmount, self.cmbUnit)
        RBContainerTypeEditor.setTabOrder(self.cmbUnit, self.tblIdentification)
        RBContainerTypeEditor.setTabOrder(self.tblIdentification, self.buttonBox)

    def retranslateUi(self, RBContainerTypeEditor):
        RBContainerTypeEditor.setWindowTitle(_translate("RBContainerTypeEditor", "Dialog", None))
        self.lblUnit.setText(_translate("RBContainerTypeEditor", "&Единица измерения", None))
        self.lblColor.setText(_translate("RBContainerTypeEditor", "&Цветовая маркировка", None))
        self.lblAmount.setText(_translate("RBContainerTypeEditor", "О&бъем", None))
        self.lblName.setText(_translate("RBContainerTypeEditor", "&Наименование", None))
        self.lblCode.setText(_translate("RBContainerTypeEditor", "&Код", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMain), _translate("RBContainerTypeEditor", "&Основная информация", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabIdentification), _translate("RBContainerTypeEditor", "&Идентификация", None))

from library.ColorEdit import CColorComboBox
from library.InDocTable import CInDocTableView
from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RBContainerTypeEditor = QtGui.QDialog()
    ui = Ui_RBContainerTypeEditor()
    ui.setupUi(RBContainerTypeEditor)
    RBContainerTypeEditor.show()
    sys.exit(app.exec_())

