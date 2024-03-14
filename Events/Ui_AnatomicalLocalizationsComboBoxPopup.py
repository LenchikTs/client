# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\samson\Events\AnatomicalLocalizationsComboBoxPopup.ui'
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

class Ui_AnatomicalLocalizationsComboBoxPopup(object):
    def setupUi(self, AnatomicalLocalizationsComboBoxPopup):
        AnatomicalLocalizationsComboBoxPopup.setObjectName(_fromUtf8("AnatomicalLocalizationsComboBoxPopup"))
        AnatomicalLocalizationsComboBoxPopup.resize(680, 371)
        self.gridLayout = QtGui.QGridLayout(AnatomicalLocalizationsComboBoxPopup)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtFindWord = QtGui.QLineEdit(AnatomicalLocalizationsComboBoxPopup)
        self.edtFindWord.setObjectName(_fromUtf8("edtFindWord"))
        self.gridLayout.addWidget(self.edtFindWord, 0, 0, 1, 1)
        self.tblAnatomicalLocalizations = QtGui.QTreeView(AnatomicalLocalizationsComboBoxPopup)
        self.tblAnatomicalLocalizations.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.tblAnatomicalLocalizations.setObjectName(_fromUtf8("tblAnatomicalLocalizations"))
        self.tblAnatomicalLocalizations.header().setVisible(False)
        self.gridLayout.addWidget(self.tblAnatomicalLocalizations, 1, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(AnatomicalLocalizationsComboBoxPopup)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)

        self.retranslateUi(AnatomicalLocalizationsComboBoxPopup)
        QtCore.QMetaObject.connectSlotsByName(AnatomicalLocalizationsComboBoxPopup)

    def retranslateUi(self, AnatomicalLocalizationsComboBoxPopup):
        AnatomicalLocalizationsComboBoxPopup.setWindowTitle(_translate("AnatomicalLocalizationsComboBoxPopup", "Form", None))

