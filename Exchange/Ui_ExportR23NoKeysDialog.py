# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ExportR23NoKeysDialog.ui'
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

class Ui_ExportR23NoKeysDialog(object):
    def setupUi(self, ExportR23NoKeysDialog):
        ExportR23NoKeysDialog.setObjectName(_fromUtf8("ExportR23NoKeysDialog"))
        ExportR23NoKeysDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ExportR23NoKeysDialog.resize(698, 515)
        self.verticalLayout = QtGui.QVBoxLayout(ExportR23NoKeysDialog)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(ExportR23NoKeysDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.splitter = QtGui.QSplitter(ExportR23NoKeysDialog)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.grpAccountItems = QtGui.QGroupBox(self.splitter)
        self.grpAccountItems.setObjectName(_fromUtf8("grpAccountItems"))
        self.gridLayout_2 = QtGui.QGridLayout(self.grpAccountItems)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tblAccountItems = CInDocTableView(self.grpAccountItems)
        self.tblAccountItems.setObjectName(_fromUtf8("tblAccountItems"))
        self.gridLayout_2.addWidget(self.tblAccountItems, 0, 0, 1, 2)
        self.verticalLayout.addWidget(self.splitter)
        self.labelCount = QtGui.QLabel(ExportR23NoKeysDialog)
        self.labelCount.setObjectName(_fromUtf8("labelCount"))
        self.verticalLayout.addWidget(self.labelCount)
        self.buttonBox = QtGui.QDialogButtonBox(ExportR23NoKeysDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ExportR23NoKeysDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ExportR23NoKeysDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ExportR23NoKeysDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ExportR23NoKeysDialog)
        ExportR23NoKeysDialog.setTabOrder(self.tblAccountItems, self.buttonBox)

    def retranslateUi(self, ExportR23NoKeysDialog):
        ExportR23NoKeysDialog.setWindowTitle(_translate("ExportR23NoKeysDialog", "Dialog", None))
        self.label.setText(_translate("ExportR23NoKeysDialog", "При экспорте реестров обнаружены персональные счета, не прошедшие предварительный контроль (отсутствует RKEY).\n"
"Удалите персональные счета из реестра и повторите экспорт", None))
        self.grpAccountItems.setTitle(_translate("ExportR23NoKeysDialog", "Персональные счета", None))
        self.labelCount.setText(_translate("ExportR23NoKeysDialog", "Всего персональных счетов: ", None))

from library.InDocTable import CInDocTableView
