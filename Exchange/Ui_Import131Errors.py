# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\Import131Errors.ui'
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

class Ui_Import131ErrorsDialog(object):
    def setupUi(self, Import131ErrorsDialog):
        Import131ErrorsDialog.setObjectName(_fromUtf8("Import131ErrorsDialog"))
        Import131ErrorsDialog.resize(717, 517)
        self.gridLayout = QtGui.QGridLayout(Import131ErrorsDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblImportFrom = QtGui.QLabel(Import131ErrorsDialog)
        self.lblImportFrom.setObjectName(_fromUtf8("lblImportFrom"))
        self.horizontalLayout.addWidget(self.lblImportFrom)
        self.edtImportFrom = QtGui.QLineEdit(Import131ErrorsDialog)
        self.edtImportFrom.setObjectName(_fromUtf8("edtImportFrom"))
        self.horizontalLayout.addWidget(self.edtImportFrom)
        self.btnImportFrom = QtGui.QPushButton(Import131ErrorsDialog)
        self.btnImportFrom.setObjectName(_fromUtf8("btnImportFrom"))
        self.horizontalLayout.addWidget(self.btnImportFrom)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 2)
        self.progressBar = CProgressBar(Import131ErrorsDialog)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 1, 0, 1, 2)
        self.logList = QtGui.QListWidget(Import131ErrorsDialog)
        self.logList.setObjectName(_fromUtf8("logList"))
        self.gridLayout.addWidget(self.logList, 2, 0, 1, 2)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.lblCount = QtGui.QLabel(Import131ErrorsDialog)
        self.lblCount.setObjectName(_fromUtf8("lblCount"))
        self.hboxlayout.addWidget(self.lblCount)
        self.btnImport = QtGui.QPushButton(Import131ErrorsDialog)
        self.btnImport.setObjectName(_fromUtf8("btnImport"))
        self.hboxlayout.addWidget(self.btnImport)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.lblDone = QtGui.QLabel(Import131ErrorsDialog)
        self.lblDone.setObjectName(_fromUtf8("lblDone"))
        self.hboxlayout.addWidget(self.lblDone)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.btnClose = QtGui.QPushButton(Import131ErrorsDialog)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.hboxlayout.addWidget(self.btnClose)
        self.gridLayout.addLayout(self.hboxlayout, 3, 0, 1, 2)

        self.retranslateUi(Import131ErrorsDialog)
        QtCore.QMetaObject.connectSlotsByName(Import131ErrorsDialog)

    def retranslateUi(self, Import131ErrorsDialog):
        Import131ErrorsDialog.setWindowTitle(_translate("Import131ErrorsDialog", "Импорт протокола ошибок", None))
        self.lblImportFrom.setText(_translate("Import131ErrorsDialog", "Импортировать из", None))
        self.btnImportFrom.setText(_translate("Import131ErrorsDialog", "...", None))
        self.lblCount.setText(_translate("Import131ErrorsDialog", "всего записей в источнике:", None))
        self.btnImport.setText(_translate("Import131ErrorsDialog", "начать импортирование", None))
        self.lblDone.setText(_translate("Import131ErrorsDialog", "Импортировано: ", None))
        self.btnClose.setText(_translate("Import131ErrorsDialog", "закрыть", None))

from library.ProgressBar import CProgressBar
