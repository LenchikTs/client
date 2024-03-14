# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\client\Exchange\ImportTariffsR23.ui'
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
        Dialog.resize(500, 491)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout2 = QtGui.QHBoxLayout()
        self.horizontalLayout2.setMargin(0)
        self.horizontalLayout2.setSpacing(4)
        self.horizontalLayout2.setObjectName(_fromUtf8("horizontalLayout2"))
        self.btnImport = QtGui.QPushButton(Dialog)
        self.btnImport.setObjectName(_fromUtf8("btnImport"))
        self.horizontalLayout2.addWidget(self.btnImport)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout2.addItem(spacerItem)
        self.labelNum = QtGui.QLabel(Dialog)
        self.labelNum.setObjectName(_fromUtf8("labelNum"))
        self.horizontalLayout2.addWidget(self.labelNum)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout2.addItem(spacerItem1)
        self.btnClose = QtGui.QPushButton(Dialog)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.horizontalLayout2.addWidget(self.btnClose)
        self.gridLayout.addLayout(self.horizontalLayout2, 6, 0, 1, 4)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 3, 0, 1, 4)
        self.statusLabel = QtGui.QLabel(Dialog)
        self.statusLabel.setText(_fromUtf8(""))
        self.statusLabel.setObjectName(_fromUtf8("statusLabel"))
        self.gridLayout.addWidget(self.statusLabel, 4, 0, 1, 4)
        self.lblSpr22 = QtGui.QLabel(Dialog)
        self.lblSpr22.setObjectName(_fromUtf8("lblSpr22"))
        self.gridLayout.addWidget(self.lblSpr22, 0, 0, 1, 1)
        self.edtSpr22 = QtGui.QLineEdit(Dialog)
        self.edtSpr22.setObjectName(_fromUtf8("edtSpr22"))
        self.gridLayout.addWidget(self.edtSpr22, 0, 1, 1, 1)
        self.log = QtGui.QTextBrowser(Dialog)
        self.log.setObjectName(_fromUtf8("log"))
        self.gridLayout.addWidget(self.log, 5, 0, 1, 4)
        self.btnSelect22 = QtGui.QToolButton(Dialog)
        self.btnSelect22.setObjectName(_fromUtf8("btnSelect22"))
        self.gridLayout.addWidget(self.btnSelect22, 0, 2, 1, 1)
        self.gbDublicates = QtGui.QGroupBox(Dialog)
        self.gbDublicates.setObjectName(_fromUtf8("gbDublicates"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.gbDublicates)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.chkUpdate = QtGui.QRadioButton(self.gbDublicates)
        self.chkUpdate.setChecked(True)
        self.chkUpdate.setObjectName(_fromUtf8("chkUpdate"))
        self.verticalLayout_4.addWidget(self.chkUpdate)
        self.chkSkip = QtGui.QRadioButton(self.gbDublicates)
        self.chkSkip.setObjectName(_fromUtf8("chkSkip"))
        self.verticalLayout_4.addWidget(self.chkSkip)
        self.chkAskUser = QtGui.QRadioButton(self.gbDublicates)
        self.chkAskUser.setObjectName(_fromUtf8("chkAskUser"))
        self.verticalLayout_4.addWidget(self.chkAskUser)
        self.gridLayout.addWidget(self.gbDublicates, 2, 0, 1, 4)
        self.chkTFOMS = QtGui.QCheckBox(Dialog)
        self.chkTFOMS.setObjectName(_fromUtf8("chkTFOMS"))
        self.gridLayout.addWidget(self.chkTFOMS, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.chkTFOMS, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.chkAskUser.setDisabled)
        QtCore.QObject.connect(self.chkTFOMS, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.chkSkip.setDisabled)
        QtCore.QObject.connect(self.chkTFOMS, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.chkUpdate.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Загрузка тарифов для Краснодарского края", None))
        self.btnImport.setText(_translate("Dialog", "Начать импортирование", None))
        self.labelNum.setText(_translate("Dialog", "всего записей в источнике:", None))
        self.btnClose.setText(_translate("Dialog", "Закрыть", None))
        self.lblSpr22.setText(_translate("Dialog", "Путь к Spr22", None))
        self.btnSelect22.setText(_translate("Dialog", "...", None))
        self.gbDublicates.setTitle(_translate("Dialog", "Совпадающие записи", None))
        self.chkUpdate.setText(_translate("Dialog", "Обновить", None))
        self.chkSkip.setText(_translate("Dialog", "Пропустить", None))
        self.chkAskUser.setText(_translate("Dialog", "Спросить у пользователя", None))
        self.chkTFOMS.setText(_translate("Dialog", "Spr22 ТФОМС", None))

