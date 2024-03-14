# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Rabota\s11\F088\TempInvalidF088.ui'
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

class Ui_grpTempInvalid(object):
    def setupUi(self, grpTempInvalid):
        grpTempInvalid.setObjectName(_fromUtf8("grpTempInvalid"))
        grpTempInvalid.resize(884, 516)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(grpTempInvalid.sizePolicy().hasHeightForWidth())
        grpTempInvalid.setSizePolicy(sizePolicy)
        grpTempInvalid.setChecked(False)
        self.gridLayout_3 = QtGui.QGridLayout(grpTempInvalid)
        self.gridLayout_3.setMargin(4)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.grpTempInvalidPrivate = QtGui.QGroupBox(grpTempInvalid)
        self.grpTempInvalidPrivate.setAlignment(QtCore.Qt.AlignCenter)
        self.grpTempInvalidPrivate.setObjectName(_fromUtf8("grpTempInvalidPrivate"))
        self.gridLayout = QtGui.QGridLayout(self.grpTempInvalidPrivate)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(self.grpTempInvalidPrivate)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.tblTempInvalidPrivate = CInDocTableView(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblTempInvalidPrivate.sizePolicy().hasHeightForWidth())
        self.tblTempInvalidPrivate.setSizePolicy(sizePolicy)
        self.tblTempInvalidPrivate.setObjectName(_fromUtf8("tblTempInvalidPrivate"))
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.grpTempInvalidPrivate, 0, 0, 1, 1)

        self.retranslateUi(grpTempInvalid)
        QtCore.QMetaObject.connectSlotsByName(grpTempInvalid)

    def retranslateUi(self, grpTempInvalid):
        self.grpTempInvalidPrivate.setTitle(_translate("grpTempInvalid", "Собственные", None))

from library.InDocTable import CInDocTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    grpTempInvalid = QtGui.QGroupBox()
    ui = Ui_grpTempInvalid()
    ui.setupUi(grpTempInvalid)
    grpTempInvalid.show()
    sys.exit(app.exec_())

