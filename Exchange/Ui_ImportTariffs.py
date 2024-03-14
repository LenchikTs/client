# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ImportTariffs.ui'
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
        Dialog.resize(543, 468)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setContentsMargins(4, 4, 4, -1)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.log = QtGui.QTextBrowser(Dialog)
        self.log.setObjectName(_fromUtf8("log"))
        self.gridLayout.addWidget(self.log, 6, 0, 1, 2)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.btnImport = QtGui.QPushButton(Dialog)
        self.btnImport.setObjectName(_fromUtf8("btnImport"))
        self.hboxlayout.addWidget(self.btnImport)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.labelNum = QtGui.QLabel(Dialog)
        self.labelNum.setObjectName(_fromUtf8("labelNum"))
        self.hboxlayout.addWidget(self.labelNum)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.btnClose = QtGui.QPushButton(Dialog)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.hboxlayout.addWidget(self.btnClose)
        self.gridLayout.addLayout(self.hboxlayout, 7, 0, 1, 2)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.hboxlayout1.addWidget(self.label)
        self.splitter = QtGui.QSplitter(Dialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.edtFileName = QtGui.QLineEdit(self.splitter)
        self.edtFileName.setText(_fromUtf8(""))
        self.edtFileName.setReadOnly(True)
        self.edtFileName.setObjectName(_fromUtf8("edtFileName"))
        self.edtIP = QtGui.QLineEdit(self.splitter)
        self.edtIP.setReadOnly(True)
        self.edtIP.setObjectName(_fromUtf8("edtIP"))
        self.hboxlayout1.addWidget(self.splitter)
        self.gridLayout.addLayout(self.hboxlayout1, 0, 0, 1, 2)
        self.chkLoadChildren = QtGui.QCheckBox(Dialog)
        self.chkLoadChildren.setChecked(True)
        self.chkLoadChildren.setObjectName(_fromUtf8("chkLoadChildren"))
        self.gridLayout.addWidget(self.chkLoadChildren, 1, 0, 1, 1)
        self.chkAmb = QtGui.QCheckBox(Dialog)
        self.chkAmb.setChecked(True)
        self.chkAmb.setObjectName(_fromUtf8("chkAmb"))
        self.gridLayout.addWidget(self.chkAmb, 1, 1, 1, 1)
        self.chkLoadAdult = QtGui.QCheckBox(Dialog)
        self.chkLoadAdult.setChecked(True)
        self.chkLoadAdult.setObjectName(_fromUtf8("chkLoadAdult"))
        self.gridLayout.addWidget(self.chkLoadAdult, 2, 0, 1, 1)
        self.chkStom = QtGui.QCheckBox(Dialog)
        self.chkStom.setObjectName(_fromUtf8("chkStom"))
        self.gridLayout.addWidget(self.chkStom, 2, 1, 1, 1)
        self.chkCompleteCase = QtGui.QCheckBox(Dialog)
        self.chkCompleteCase.setObjectName(_fromUtf8("chkCompleteCase"))
        self.gridLayout.addWidget(self.chkCompleteCase, 3, 1, 1, 1)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 4, 0, 1, 2)
        self.statusLabel = QtGui.QLabel(Dialog)
        self.statusLabel.setText(_fromUtf8(""))
        self.statusLabel.setObjectName(_fromUtf8("statusLabel"))
        self.gridLayout.addWidget(self.statusLabel, 5, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.edtFileName, self.edtIP)
        Dialog.setTabOrder(self.edtIP, self.chkLoadChildren)
        Dialog.setTabOrder(self.chkLoadChildren, self.chkLoadAdult)
        Dialog.setTabOrder(self.chkLoadAdult, self.chkAmb)
        Dialog.setTabOrder(self.chkAmb, self.chkStom)
        Dialog.setTabOrder(self.chkStom, self.chkCompleteCase)
        Dialog.setTabOrder(self.chkCompleteCase, self.log)
        Dialog.setTabOrder(self.log, self.btnImport)
        Dialog.setTabOrder(self.btnImport, self.btnClose)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Загрузка тарифов из ЕИС", None))
        self.btnImport.setText(_translate("Dialog", "начать импортирование", None))
        self.labelNum.setText(_translate("Dialog", "всего записей в источнике:", None))
        self.btnClose.setText(_translate("Dialog", "закрыть", None))
        self.label.setText(_translate("Dialog", "импортировать из", None))
        self.chkLoadChildren.setText(_translate("Dialog", "загружать детские", None))
        self.chkAmb.setText(_translate("Dialog", "загружать амбулаторные тарифы", None))
        self.chkLoadAdult.setText(_translate("Dialog", "загружать взрослые", None))
        self.chkStom.setText(_translate("Dialog", "загружать стоматологические тарифы", None))
        self.chkCompleteCase.setText(_translate("Dialog", "загружать законченные случаи", None))

