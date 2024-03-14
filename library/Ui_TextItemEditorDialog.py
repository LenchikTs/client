# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\library\TextItemEditorDialog.ui'
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

class Ui_TextItemEditorDialog(object):
    def setupUi(self, TextItemEditorDialog):
        TextItemEditorDialog.setObjectName(_fromUtf8("TextItemEditorDialog"))
        TextItemEditorDialog.resize(248, 129)
        self.gridLayout = QtGui.QGridLayout(TextItemEditorDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblText = QtGui.QLabel(TextItemEditorDialog)
        self.lblText.setObjectName(_fromUtf8("lblText"))
        self.gridLayout.addWidget(self.lblText, 0, 0, 1, 1)
        self.edtText = QtGui.QLineEdit(TextItemEditorDialog)
        self.edtText.setObjectName(_fromUtf8("edtText"))
        self.gridLayout.addWidget(self.edtText, 0, 1, 1, 1)
        self.lblTextSize = QtGui.QLabel(TextItemEditorDialog)
        self.lblTextSize.setObjectName(_fromUtf8("lblTextSize"))
        self.gridLayout.addWidget(self.lblTextSize, 1, 0, 1, 1)
        self.edtTextSize = QtGui.QSpinBox(TextItemEditorDialog)
        self.edtTextSize.setMinimum(1)
        self.edtTextSize.setMaximum(10)
        self.edtTextSize.setObjectName(_fromUtf8("edtTextSize"))
        self.gridLayout.addWidget(self.edtTextSize, 1, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(TextItemEditorDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 2)
        self.lblRotation = QtGui.QLabel(TextItemEditorDialog)
        self.lblRotation.setObjectName(_fromUtf8("lblRotation"))
        self.gridLayout.addWidget(self.lblRotation, 2, 0, 1, 1)
        self.edtRotation = QtGui.QSpinBox(TextItemEditorDialog)
        self.edtRotation.setMinimum(-360)
        self.edtRotation.setMaximum(360)
        self.edtRotation.setObjectName(_fromUtf8("edtRotation"))
        self.gridLayout.addWidget(self.edtRotation, 2, 1, 1, 1)

        self.retranslateUi(TextItemEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TextItemEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TextItemEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TextItemEditorDialog)

    def retranslateUi(self, TextItemEditorDialog):
        TextItemEditorDialog.setWindowTitle(_translate("TextItemEditorDialog", "Редактор текстовых отметок", None))
        self.lblText.setText(_translate("TextItemEditorDialog", "Текст", None))
        self.lblTextSize.setText(_translate("TextItemEditorDialog", "Размер текста", None))
        self.lblRotation.setText(_translate("TextItemEditorDialog", "Поворот", None))

