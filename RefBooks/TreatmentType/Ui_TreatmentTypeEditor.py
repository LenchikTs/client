# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/RefBooks/TreatmentTypeEditor.ui'
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

class Ui_TreatmentTypeEditor(object):
    def setupUi(self, TreatmentTypeEditor):
        TreatmentTypeEditor.setObjectName(_fromUtf8("TreatmentTypeEditor"))
        TreatmentTypeEditor.resize(484, 113)
        TreatmentTypeEditor.setSizeGripEnabled(True)
        self.gridLayout_2 = QtGui.QGridLayout(TreatmentTypeEditor)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lblCode = QtGui.QLabel(TreatmentTypeEditor)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout_2.addWidget(self.lblCode, 0, 0, 1, 1)
        self.lblName = QtGui.QLabel(TreatmentTypeEditor)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout_2.addWidget(self.lblName, 1, 0, 1, 1)
        self.cmbColor = CColorComboBox(TreatmentTypeEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbColor.sizePolicy().hasHeightForWidth())
        self.cmbColor.setSizePolicy(sizePolicy)
        self.cmbColor.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContentsOnFirstShow)
        self.cmbColor.setObjectName(_fromUtf8("cmbColor"))
        self.gridLayout_2.addWidget(self.cmbColor, 2, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 3, 1, 1, 1)
        self.lblColor = QtGui.QLabel(TreatmentTypeEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblColor.sizePolicy().hasHeightForWidth())
        self.lblColor.setSizePolicy(sizePolicy)
        self.lblColor.setObjectName(_fromUtf8("lblColor"))
        self.gridLayout_2.addWidget(self.lblColor, 2, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 2, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(TreatmentTypeEditor)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 5, 0, 1, 3)
        self.edtName = QtGui.QLineEdit(TreatmentTypeEditor)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout_2.addWidget(self.edtName, 1, 1, 1, 2)
        self.edtCode = QtGui.QLineEdit(TreatmentTypeEditor)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout_2.addWidget(self.edtCode, 0, 1, 1, 2)
        self.lblCode.setBuddy(self.edtCode)
        self.lblName.setBuddy(self.edtName)
        self.lblColor.setBuddy(self.cmbColor)

        self.retranslateUi(TreatmentTypeEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TreatmentTypeEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TreatmentTypeEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(TreatmentTypeEditor)
        TreatmentTypeEditor.setTabOrder(self.edtCode, self.edtName)
        TreatmentTypeEditor.setTabOrder(self.edtName, self.cmbColor)
        TreatmentTypeEditor.setTabOrder(self.cmbColor, self.buttonBox)

    def retranslateUi(self, TreatmentTypeEditor):
        TreatmentTypeEditor.setWindowTitle(_translate("TreatmentTypeEditor", "Dialog", None))
        self.lblCode.setText(_translate("TreatmentTypeEditor", "&Код", None))
        self.lblName.setText(_translate("TreatmentTypeEditor", "&Наименование", None))
        self.cmbColor.setToolTip(_translate("TreatmentTypeEditor", "Цветовая маркировка", None))
        self.lblColor.setText(_translate("TreatmentTypeEditor", "&Цветовая маркировка", None))

from library.ColorEdit import CColorComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TreatmentTypeEditor = QtGui.QDialog()
    ui = Ui_TreatmentTypeEditor()
    ui.setupUi(TreatmentTypeEditor)
    TreatmentTypeEditor.show()
    sys.exit(app.exec_())

