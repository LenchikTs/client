# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ImportRD1.ui'
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
        Dialog.resize(581, 496)
        self.gridlayout = QtGui.QGridLayout(Dialog)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
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
        self.gridlayout.addLayout(self.hboxlayout, 0, 0, 1, 1)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.hboxlayout1.addWidget(self.label_2)
        self.edtPodtv = QtGui.QLineEdit(Dialog)
        self.edtPodtv.setObjectName(_fromUtf8("edtPodtv"))
        self.hboxlayout1.addWidget(self.edtPodtv)
        self.gridlayout.addLayout(self.hboxlayout1, 1, 0, 1, 1)
        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setObjectName(_fromUtf8("hboxlayout2"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.hboxlayout2.addWidget(self.label_3)
        self.edtAttach = QtGui.QLineEdit(Dialog)
        self.edtAttach.setObjectName(_fromUtf8("edtAttach"))
        self.hboxlayout2.addWidget(self.edtAttach)
        self.gridlayout.addLayout(self.hboxlayout2, 2, 0, 1, 1)
        self.AccCheck = QtGui.QCheckBox(Dialog)
        self.AccCheck.setChecked(True)
        self.AccCheck.setObjectName(_fromUtf8("AccCheck"))
        self.gridlayout.addWidget(self.AccCheck, 3, 0, 1, 1)
        self.OplataCheck = QtGui.QCheckBox(Dialog)
        self.OplataCheck.setChecked(True)
        self.OplataCheck.setObjectName(_fromUtf8("OplataCheck"))
        self.gridlayout.addWidget(self.OplataCheck, 4, 0, 1, 1)
        self.OtkazCheck = QtGui.QCheckBox(Dialog)
        self.OtkazCheck.setChecked(True)
        self.OtkazCheck.setObjectName(_fromUtf8("OtkazCheck"))
        self.gridlayout.addWidget(self.OtkazCheck, 5, 0, 1, 1)
        self.chkAttach = QtGui.QCheckBox(Dialog)
        self.chkAttach.setObjectName(_fromUtf8("chkAttach"))
        self.gridlayout.addWidget(self.chkAttach, 6, 0, 1, 1)
        self.chkOnlyAttach = QtGui.QCheckBox(Dialog)
        self.chkOnlyAttach.setObjectName(_fromUtf8("chkOnlyAttach"))
        self.gridlayout.addWidget(self.chkOnlyAttach, 7, 0, 1, 1)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridlayout.addWidget(self.progressBar, 8, 0, 1, 1)
        self.stat = QtGui.QLabel(Dialog)
        self.stat.setText(_fromUtf8(""))
        self.stat.setObjectName(_fromUtf8("stat"))
        self.gridlayout.addWidget(self.stat, 9, 0, 1, 1)
        self.log = QtGui.QTextBrowser(Dialog)
        self.log.setObjectName(_fromUtf8("log"))
        self.gridlayout.addWidget(self.log, 10, 0, 1, 1)
        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setMargin(0)
        self.hboxlayout3.setSpacing(6)
        self.hboxlayout3.setObjectName(_fromUtf8("hboxlayout3"))
        self.btnImport = QtGui.QPushButton(Dialog)
        self.btnImport.setObjectName(_fromUtf8("btnImport"))
        self.hboxlayout3.addWidget(self.btnImport)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout3.addItem(spacerItem)
        self.labelNum = QtGui.QLabel(Dialog)
        self.labelNum.setObjectName(_fromUtf8("labelNum"))
        self.hboxlayout3.addWidget(self.labelNum)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout3.addItem(spacerItem1)
        self.btnClose = QtGui.QPushButton(Dialog)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.hboxlayout3.addWidget(self.btnClose)
        self.gridlayout.addLayout(self.hboxlayout3, 11, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Загрузка РД1", None))
        self.label.setText(_translate("Dialog", "импортировать из", None))
        self.btnSelectFile.setText(_translate("Dialog", "...", None))
        self.btnView.setText(_translate("Dialog", "Просмотреть", None))
        self.label_2.setText(_translate("Dialog", "подтверждение", None))
        self.edtPodtv.setText(_translate("Dialog", "б/н", None))
        self.label_3.setText(_translate("Dialog", "Название поля прикрепления", None))
        self.edtAttach.setText(_translate("Dialog", "TMO2", None))
        self.AccCheck.setText(_translate("Dialog", "только текущий счёт", None))
        self.OplataCheck.setText(_translate("Dialog", "загружать оплаченные", None))
        self.OtkazCheck.setText(_translate("Dialog", "загружать отказы", None))
        self.chkAttach.setText(_translate("Dialog", "загружать данные о прикреплении", None))
        self.chkOnlyAttach.setText(_translate("Dialog", "загружать только данные о прикреплении", None))
        self.btnImport.setText(_translate("Dialog", "начать импортирование", None))
        self.labelNum.setText(_translate("Dialog", "всего записей в источнике:", None))
        self.btnClose.setText(_translate("Dialog", "закрыть", None))

