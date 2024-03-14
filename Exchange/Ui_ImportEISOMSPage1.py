# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ImportEISOMSPage1.ui'
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

class Ui_ImportEISOMSPage1(object):
    def setupUi(self, ImportEISOMSPage1):
        ImportEISOMSPage1.setObjectName(_fromUtf8("ImportEISOMSPage1"))
        ImportEISOMSPage1.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(ImportEISOMSPage1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblFileName = QtGui.QLabel(ImportEISOMSPage1)
        self.lblFileName.setObjectName(_fromUtf8("lblFileName"))
        self.horizontalLayout.addWidget(self.lblFileName)
        self.edtFileName = QtGui.QLineEdit(ImportEISOMSPage1)
        self.edtFileName.setObjectName(_fromUtf8("edtFileName"))
        self.horizontalLayout.addWidget(self.edtFileName)
        self.btnSelectFile = QtGui.QToolButton(ImportEISOMSPage1)
        self.btnSelectFile.setObjectName(_fromUtf8("btnSelectFile"))
        self.horizontalLayout.addWidget(self.btnSelectFile)
        self.btnView = QtGui.QPushButton(ImportEISOMSPage1)
        self.btnView.setObjectName(_fromUtf8("btnView"))
        self.horizontalLayout.addWidget(self.btnView)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 2)
        self.chkImportAfterSMOCheck = QtGui.QCheckBox(ImportEISOMSPage1)
        self.chkImportAfterSMOCheck.setObjectName(_fromUtf8("chkImportAfterSMOCheck"))
        self.gridLayout.addWidget(self.chkImportAfterSMOCheck, 1, 1, 1, 1)
        self.chkRemoveFileAfterImport = QtGui.QCheckBox(ImportEISOMSPage1)
        self.chkRemoveFileAfterImport.setObjectName(_fromUtf8("chkRemoveFileAfterImport"))
        self.gridLayout.addWidget(self.chkRemoveFileAfterImport, 2, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 251, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)

        self.retranslateUi(ImportEISOMSPage1)
        QtCore.QMetaObject.connectSlotsByName(ImportEISOMSPage1)

    def retranslateUi(self, ImportEISOMSPage1):
        ImportEISOMSPage1.setWindowTitle(_translate("ImportEISOMSPage1", "Form", None))
        self.lblFileName.setText(_translate("ImportEISOMSPage1", "Выберите файл", None))
        self.btnSelectFile.setText(_translate("ImportEISOMSPage1", "...", None))
        self.btnView.setText(_translate("ImportEISOMSPage1", "Просмотреть", None))
        self.chkImportAfterSMOCheck.setText(_translate("ImportEISOMSPage1", "Импорт данных контроля СМО", None))
        self.chkRemoveFileAfterImport.setText(_translate("ImportEISOMSPage1", "Удалить файл после успешного импорта", None))

