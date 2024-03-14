# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\Samson\UP_s11\client_merge\appendix\regional\r23\importReestr\ImportCovidDialog.ui'
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

class Ui_ImportCovidDialog(object):
    def setupUi(self, ImportCovidDialog):
        ImportCovidDialog.setObjectName(_fromUtf8("ImportCovidDialog"))
        ImportCovidDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ImportCovidDialog.resize(698, 515)
        self.verticalLayout = QtGui.QVBoxLayout(ImportCovidDialog)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(ImportCovidDialog)
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
        self.splitter = QtGui.QSplitter(ImportCovidDialog)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.grpAccountItems = QtGui.QGroupBox(self.splitter)
        self.grpAccountItems.setTitle(_fromUtf8(""))
        self.grpAccountItems.setObjectName(_fromUtf8("grpAccountItems"))
        self.gridLayout_2 = QtGui.QGridLayout(self.grpAccountItems)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tblAccountItems = CInDocTableView(self.grpAccountItems)
        self.tblAccountItems.setObjectName(_fromUtf8("tblAccountItems"))
        self.gridLayout_2.addWidget(self.tblAccountItems, 0, 0, 1, 2)
        self.verticalLayout.addWidget(self.splitter)
        self.labelCount = QtGui.QLabel(ImportCovidDialog)
        self.labelCount.setObjectName(_fromUtf8("labelCount"))
        self.verticalLayout.addWidget(self.labelCount)
        self.buttonBox = QtGui.QDialogButtonBox(ImportCovidDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ImportCovidDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ImportCovidDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ImportCovidDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ImportCovidDialog)
        ImportCovidDialog.setTabOrder(self.tblAccountItems, self.buttonBox)

    def retranslateUi(self, ImportCovidDialog):
        ImportCovidDialog.setWindowTitle(_translate("ImportCovidDialog", "Dialog", None))
        self.label.setText(_translate("ImportCovidDialog", "Список людей, по которым нет соответствия в БД по ФИО+ДР", None))
        self.labelCount.setText(_translate("ImportCovidDialog", "Всего человек: ", None))

from library.InDocTable import CInDocTableView
