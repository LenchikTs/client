# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/library/MKBExSubclassPopup.ui'
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

class Ui_MKBExSubclassPopup(object):
    def setupUi(self, MKBExSubclassPopup):
        MKBExSubclassPopup.setObjectName(_fromUtf8("MKBExSubclassPopup"))
        MKBExSubclassPopup.resize(295, 27)
        self.gridLayout = QtGui.QGridLayout(MKBExSubclassPopup)
        self.gridLayout.setMargin(2)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.cmbC9 = CRBMKBExSubclassComboBox(MKBExSubclassPopup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbC9.sizePolicy().hasHeightForWidth())
        self.cmbC9.setSizePolicy(sizePolicy)
        self.cmbC9.setObjectName(_fromUtf8("cmbC9"))
        self.cmbC9.addItem(_fromUtf8(""))
        self.cmbC9.addItem(_fromUtf8(""))
        self.cmbC9.addItem(_fromUtf8(""))
        self.cmbC9.addItem(_fromUtf8(""))
        self.cmbC9.addItem(_fromUtf8(""))
        self.cmbC9.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbC9, 0, 3, 1, 1)
        self.cmbC6 = CRBMKBExSubclassComboBox(MKBExSubclassPopup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbC6.sizePolicy().hasHeightForWidth())
        self.cmbC6.setSizePolicy(sizePolicy)
        self.cmbC6.setObjectName(_fromUtf8("cmbC6"))
        self.cmbC6.addItem(_fromUtf8(""))
        self.cmbC6.addItem(_fromUtf8(""))
        self.cmbC6.addItem(_fromUtf8(""))
        self.cmbC6.addItem(_fromUtf8(""))
        self.cmbC6.addItem(_fromUtf8(""))
        self.cmbC6.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbC6, 0, 0, 1, 1)
        self.cmbC7 = CRBMKBExSubclassComboBox(MKBExSubclassPopup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbC7.sizePolicy().hasHeightForWidth())
        self.cmbC7.setSizePolicy(sizePolicy)
        self.cmbC7.setObjectName(_fromUtf8("cmbC7"))
        self.cmbC7.addItem(_fromUtf8(""))
        self.cmbC7.addItem(_fromUtf8(""))
        self.cmbC7.addItem(_fromUtf8(""))
        self.cmbC7.addItem(_fromUtf8(""))
        self.cmbC7.addItem(_fromUtf8(""))
        self.cmbC7.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbC7, 0, 1, 1, 1)
        self.cmbC8 = CRBMKBExSubclassComboBox(MKBExSubclassPopup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbC8.sizePolicy().hasHeightForWidth())
        self.cmbC8.setSizePolicy(sizePolicy)
        self.cmbC8.setObjectName(_fromUtf8("cmbC8"))
        self.cmbC8.addItem(_fromUtf8(""))
        self.cmbC8.addItem(_fromUtf8(""))
        self.cmbC8.addItem(_fromUtf8(""))
        self.cmbC8.addItem(_fromUtf8(""))
        self.cmbC8.addItem(_fromUtf8(""))
        self.cmbC8.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbC8, 0, 2, 1, 1)
        self.cmbC10 = CRBMKBExSubclassComboBox(MKBExSubclassPopup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbC10.sizePolicy().hasHeightForWidth())
        self.cmbC10.setSizePolicy(sizePolicy)
        self.cmbC10.setObjectName(_fromUtf8("cmbC10"))
        self.cmbC10.addItem(_fromUtf8(""))
        self.cmbC10.addItem(_fromUtf8(""))
        self.cmbC10.addItem(_fromUtf8(""))
        self.cmbC10.addItem(_fromUtf8(""))
        self.cmbC10.addItem(_fromUtf8(""))
        self.cmbC10.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbC10, 0, 4, 1, 1)

        self.retranslateUi(MKBExSubclassPopup)
        QtCore.QMetaObject.connectSlotsByName(MKBExSubclassPopup)

    def retranslateUi(self, MKBExSubclassPopup):
        MKBExSubclassPopup.setWindowTitle(_translate("MKBExSubclassPopup", "Form", None))
        self.cmbC9.setItemText(0, _translate("MKBExSubclassPopup", "x", None))
        self.cmbC9.setItemText(1, _translate("MKBExSubclassPopup", "6", None))
        self.cmbC9.setItemText(2, _translate("MKBExSubclassPopup", "7", None))
        self.cmbC9.setItemText(3, _translate("MKBExSubclassPopup", "8", None))
        self.cmbC9.setItemText(4, _translate("MKBExSubclassPopup", "9", None))
        self.cmbC9.setItemText(5, _translate("MKBExSubclassPopup", "10", None))
        self.cmbC6.setItemText(0, _translate("MKBExSubclassPopup", "x", None))
        self.cmbC6.setItemText(1, _translate("MKBExSubclassPopup", "6", None))
        self.cmbC6.setItemText(2, _translate("MKBExSubclassPopup", "7", None))
        self.cmbC6.setItemText(3, _translate("MKBExSubclassPopup", "8", None))
        self.cmbC6.setItemText(4, _translate("MKBExSubclassPopup", "9", None))
        self.cmbC6.setItemText(5, _translate("MKBExSubclassPopup", "10", None))
        self.cmbC7.setItemText(0, _translate("MKBExSubclassPopup", "x", None))
        self.cmbC7.setItemText(1, _translate("MKBExSubclassPopup", "6", None))
        self.cmbC7.setItemText(2, _translate("MKBExSubclassPopup", "7", None))
        self.cmbC7.setItemText(3, _translate("MKBExSubclassPopup", "8", None))
        self.cmbC7.setItemText(4, _translate("MKBExSubclassPopup", "9", None))
        self.cmbC7.setItemText(5, _translate("MKBExSubclassPopup", "10", None))
        self.cmbC8.setItemText(0, _translate("MKBExSubclassPopup", "x", None))
        self.cmbC8.setItemText(1, _translate("MKBExSubclassPopup", "6", None))
        self.cmbC8.setItemText(2, _translate("MKBExSubclassPopup", "7", None))
        self.cmbC8.setItemText(3, _translate("MKBExSubclassPopup", "8", None))
        self.cmbC8.setItemText(4, _translate("MKBExSubclassPopup", "9", None))
        self.cmbC8.setItemText(5, _translate("MKBExSubclassPopup", "10", None))
        self.cmbC10.setItemText(0, _translate("MKBExSubclassPopup", "x", None))
        self.cmbC10.setItemText(1, _translate("MKBExSubclassPopup", "6", None))
        self.cmbC10.setItemText(2, _translate("MKBExSubclassPopup", "7", None))
        self.cmbC10.setItemText(3, _translate("MKBExSubclassPopup", "8", None))
        self.cmbC10.setItemText(4, _translate("MKBExSubclassPopup", "9", None))
        self.cmbC10.setItemText(5, _translate("MKBExSubclassPopup", "10", None))

from library.RBMKBExSubclassComboBox import CRBMKBExSubclassComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MKBExSubclassPopup = QtGui.QWidget()
    ui = Ui_MKBExSubclassPopup()
    ui.setupUi(MKBExSubclassPopup)
    MKBExSubclassPopup.show()
    sys.exit(app.exec_())

