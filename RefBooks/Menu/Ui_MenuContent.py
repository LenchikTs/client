# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\F003\MenuContent.ui'
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

class Ui_MenuContent(object):
    def setupUi(self, MenuContent):
        MenuContent.setObjectName(_fromUtf8("MenuContent"))
        MenuContent.resize(540, 307)
        MenuContent.setSizeGripEnabled(False)
        self.gridLayout = QtGui.QGridLayout(MenuContent)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtCode = QtGui.QLabel(MenuContent)
        self.edtCode.setText(_fromUtf8(""))
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout.addWidget(self.edtCode, 0, 1, 1, 1)
        self.tblMenuContent = CInDocTableView(MenuContent)
        self.tblMenuContent.setObjectName(_fromUtf8("tblMenuContent"))
        self.gridLayout.addWidget(self.tblMenuContent, 2, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(422, 13, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(103, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 2)
        self.lblName = QtGui.QLabel(MenuContent)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 1, 0, 1, 1)
        self.lblCode = QtGui.QLabel(MenuContent)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout.addWidget(self.lblCode, 0, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(422, 17, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 2, 1, 1)
        self.edtName = QtGui.QLabel(MenuContent)
        self.edtName.setText(_fromUtf8(""))
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 1, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(MenuContent)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 3)

        self.retranslateUi(MenuContent)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), MenuContent.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), MenuContent.reject)
        QtCore.QMetaObject.connectSlotsByName(MenuContent)

    def retranslateUi(self, MenuContent):
        MenuContent.setWindowTitle(_translate("MenuContent", "Шаблон питания", None))
        self.lblName.setText(_translate("MenuContent", "Наименование: ", None))
        self.lblCode.setText(_translate("MenuContent", "Код: ", None))

from library.InDocTable import CInDocTableView
