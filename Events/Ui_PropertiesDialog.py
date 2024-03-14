# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Events\PropertiesDialog.ui'
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

class Ui_PropertiesDialog(object):
    def setupUi(self, PropertiesDialog):
        PropertiesDialog.setObjectName(_fromUtf8("PropertiesDialog"))
        PropertiesDialog.resize(393, 261)
        self.gridLayout = QtGui.QGridLayout(PropertiesDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblAPProps = CActionPropertiesTableView(PropertiesDialog)
        self.tblAPProps.setObjectName(_fromUtf8("tblAPProps"))
        self.gridLayout.addWidget(self.tblAPProps, 0, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(PropertiesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 2)

        self.retranslateUi(PropertiesDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PropertiesDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PropertiesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PropertiesDialog)
        PropertiesDialog.setTabOrder(self.tblAPProps, self.buttonBox)

    def retranslateUi(self, PropertiesDialog):
        PropertiesDialog.setWindowTitle(_translate("PropertiesDialog", "Свойства", None))

from Events.ActionPropertiesTable import CActionPropertiesTableView
