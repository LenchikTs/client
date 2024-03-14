# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ImportDD.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 439)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.hboxlayout.addWidget(self.label)
        self.edtFileName = QtGui.QLineEdit(Dialog)
        self.edtFileName.setObjectName(_fromUtf8("edtFileName"))
        self.hboxlayout.addWidget(self.edtFileName)
        self.btnSelectFile = QtGui.QToolButton(Dialog)
        self.btnSelectFile.setObjectName(_fromUtf8("btnSelectFile"))
        self.hboxlayout.addWidget(self.btnSelectFile)
        self.btnView = QtGui.QPushButton(Dialog)
        self.btnView.setObjectName(_fromUtf8("btnView"))
        self.hboxlayout.addWidget(self.btnView)
        self.gridLayout.addLayout(self.hboxlayout, 0, 0, 1, 1)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.hboxlayout1.addWidget(self.label_2)
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.hboxlayout1.addWidget(self.comboBox)
        self.gridLayout.addLayout(self.hboxlayout1, 1, 0, 1, 1)
        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setObjectName(_fromUtf8("hboxlayout2"))
        self.checkINN = QtGui.QCheckBox(Dialog)
        self.checkINN.setObjectName(_fromUtf8("checkINN"))
        self.hboxlayout2.addWidget(self.checkINN)
        self.edtINN = QtGui.QLineEdit(Dialog)
        self.edtINN.setObjectName(_fromUtf8("edtINN"))
        self.hboxlayout2.addWidget(self.edtINN)
        self.gridLayout.addLayout(self.hboxlayout2, 2, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.cmbPolis = QtGui.QComboBox(Dialog)
        self.cmbPolis.setObjectName(_fromUtf8("cmbPolis"))
        self.horizontalLayout.addWidget(self.cmbPolis)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 6, 0, 1, 1)
        self.stat = QtGui.QLabel(Dialog)
        self.stat.setText(_fromUtf8(""))
        self.stat.setObjectName(_fromUtf8("stat"))
        self.gridLayout.addWidget(self.stat, 7, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 8, 0, 1, 1)
        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setMargin(0)
        self.hboxlayout3.setSpacing(6)
        self.hboxlayout3.setObjectName(_fromUtf8("hboxlayout3"))
        self.btnImport = QtGui.QPushButton(Dialog)
        self.btnImport.setObjectName(_fromUtf8("btnImport"))
        self.hboxlayout3.addWidget(self.btnImport)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout3.addItem(spacerItem1)
        self.btnClose = QtGui.QPushButton(Dialog)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.hboxlayout3.addWidget(self.btnClose)
        self.gridLayout.addLayout(self.hboxlayout3, 9, 0, 1, 1)
        self.chkAddNewPatients = QtGui.QCheckBox(Dialog)
        self.chkAddNewPatients.setEnabled(True)
        self.chkAddNewPatients.setChecked(True)
        self.chkAddNewPatients.setObjectName(_fromUtf8("chkAddNewPatients"))
        self.gridLayout.addWidget(self.chkAddNewPatients, 4, 0, 1, 1)
        self.chkUpdatePatients = QtGui.QCheckBox(Dialog)
        self.chkUpdatePatients.setChecked(True)
        self.chkUpdatePatients.setObjectName(_fromUtf8("chkUpdatePatients"))
        self.gridLayout.addWidget(self.chkUpdatePatients, 5, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Загрузка населения (ДД) из ТФОМС", None))
        self.label.setText(_translate("Dialog", "импортировать из", None))
        self.btnSelectFile.setText(_translate("Dialog", "...", None))
        self.btnView.setText(_translate("Dialog", "Просмотреть", None))
        self.label_2.setText(_translate("Dialog", "тип прикрепления", None))
        self.checkINN.setText(_translate("Dialog", "ИНН работы", None))
        self.label_3.setText(_translate("Dialog", "тип полиса", None))
        self.btnImport.setText(_translate("Dialog", "начать импортирование", None))
        self.btnClose.setText(_translate("Dialog", "закрыть", None))
        self.chkAddNewPatients.setText(_translate("Dialog", "Добавлять данные о новых пациентах", None))
        self.chkUpdatePatients.setText(_translate("Dialog", "Обновлять данные на имеющихся пациентов", None))

