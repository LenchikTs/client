# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\Import131XML.ui'
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
        Dialog.resize(651, 580)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.edtFileName = QtGui.QLineEdit(Dialog)
        self.edtFileName.setText(_fromUtf8(""))
        self.edtFileName.setObjectName(_fromUtf8("edtFileName"))
        self.horizontalLayout.addWidget(self.edtFileName)
        self.btnSelectFile = QtGui.QToolButton(Dialog)
        self.btnSelectFile.setObjectName(_fromUtf8("btnSelectFile"))
        self.horizontalLayout.addWidget(self.btnSelectFile)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 2)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.vboxlayout = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.checkFed = QtGui.QCheckBox(self.groupBox)
        self.checkFed.setObjectName(_fromUtf8("checkFed"))
        self.vboxlayout.addWidget(self.checkFed)
        self.checkShortLPU = QtGui.QCheckBox(self.groupBox)
        self.checkShortLPU.setObjectName(_fromUtf8("checkShortLPU"))
        self.vboxlayout.addWidget(self.checkShortLPU)
        self.checkShortWork = QtGui.QCheckBox(self.groupBox)
        self.checkShortWork.setObjectName(_fromUtf8("checkShortWork"))
        self.vboxlayout.addWidget(self.checkShortWork)
        self.checkAttachOGRN = QtGui.QCheckBox(self.groupBox)
        self.checkAttachOGRN.setObjectName(_fromUtf8("checkAttachOGRN"))
        self.vboxlayout.addWidget(self.checkAttachOGRN)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox_2)
        self.vboxlayout1.setObjectName(_fromUtf8("vboxlayout1"))
        self.checkDate = QtGui.QCheckBox(self.groupBox_2)
        self.checkDate.setObjectName(_fromUtf8("checkDate"))
        self.vboxlayout1.addWidget(self.checkDate)
        self.checkTIP_DD_R = QtGui.QCheckBox(self.groupBox_2)
        self.checkTIP_DD_R.setObjectName(_fromUtf8("checkTIP_DD_R"))
        self.vboxlayout1.addWidget(self.checkTIP_DD_R)
        self.checkTIP_DD_V = QtGui.QCheckBox(self.groupBox_2)
        self.checkTIP_DD_V.setObjectName(_fromUtf8("checkTIP_DD_V"))
        self.vboxlayout1.addWidget(self.checkTIP_DD_V)
        self.checkNoOwn = QtGui.QCheckBox(self.groupBox_2)
        self.checkNoOwn.setObjectName(_fromUtf8("checkNoOwn"))
        self.vboxlayout1.addWidget(self.checkNoOwn)
        self.gridLayout.addWidget(self.groupBox_2, 1, 1, 1, 1)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        self.statusLabel = QtGui.QLabel(Dialog)
        self.statusLabel.setText(_fromUtf8(""))
        self.statusLabel.setObjectName(_fromUtf8("statusLabel"))
        self.gridLayout.addWidget(self.statusLabel, 4, 0, 1, 2)
        self.logBrowser = QtGui.QTextBrowser(Dialog)
        self.logBrowser.setObjectName(_fromUtf8("logBrowser"))
        self.gridLayout.addWidget(self.logBrowser, 5, 0, 1, 2)
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
        self.gridLayout.addLayout(self.hboxlayout, 6, 0, 1, 2)
        self.checkOGRN2 = QtGui.QCheckBox(Dialog)
        self.checkOGRN2.setObjectName(_fromUtf8("checkOGRN2"))
        self.gridLayout.addWidget(self.checkOGRN2, 2, 0, 1, 1)
        self.edtOGRN2 = QtGui.QLineEdit(Dialog)
        self.edtOGRN2.setEnabled(False)
        self.edtOGRN2.setObjectName(_fromUtf8("edtOGRN2"))
        self.gridLayout.addWidget(self.edtOGRN2, 2, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.checkOGRN2, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtOGRN2.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Импорт реестра форм 131 XML", None))
        self.label.setText(_translate("Dialog", "импортировать из", None))
        self.btnSelectFile.setText(_translate("Dialog", "...", None))
        self.groupBox.setTitle(_translate("Dialog", "параметры полей", None))
        self.checkFed.setText(_translate("Dialog", "федеральный код врача", None))
        self.checkShortLPU.setText(_translate("Dialog", "короткое наименование ЛПУ", None))
        self.checkShortWork.setText(_translate("Dialog", "короткое наименование работодателя", None))
        self.checkAttachOGRN.setText(_translate("Dialog", "прикрепление только по ОГРН", None))
        self.groupBox_2.setTitle(_translate("Dialog", "выбор карточек", None))
        self.checkDate.setText(_translate("Dialog", "карточки только текущего года", None))
        self.checkTIP_DD_R.setText(_translate("Dialog", "карточки типа Р (876)", None))
        self.checkTIP_DD_V.setText(_translate("Dialog", "карточки типа В (869/859)", None))
        self.checkNoOwn.setText(_translate("Dialog", "не обрабатывать свои", None))
        self.btnImport.setText(_translate("Dialog", "начать импортирование", None))
        self.labelNum.setText(_translate("Dialog", "всего записей в источнике:", None))
        self.btnClose.setText(_translate("Dialog", "закрыть", None))
        self.checkOGRN2.setText(_translate("Dialog", "считать своим ОГРН", None))

