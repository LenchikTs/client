# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\kmivc\Samson\client_test\Exchange\ReAttach.ui'
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
        Dialog.resize(978, 500)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.log = QtGui.QTextBrowser(Dialog)
        self.log.setObjectName(_fromUtf8("log"))
        self.gridLayout.addWidget(self.log, 0, 0, 1, 2)
        self.horizontalLayout2 = QtGui.QHBoxLayout()
        self.horizontalLayout2.setMargin(0)
        self.horizontalLayout2.setSpacing(4)
        self.horizontalLayout2.setObjectName(_fromUtf8("horizontalLayout2"))
        self.btnExport = QtGui.QPushButton(Dialog)
        self.btnExport.setObjectName(_fromUtf8("btnExport"))
        self.horizontalLayout2.addWidget(self.btnExport)
        self.chbFullLog = QtGui.QCheckBox(Dialog)
        self.chbFullLog.setObjectName(_fromUtf8("chbFullLog"))
        self.horizontalLayout2.addWidget(self.chbFullLog)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout2.addItem(spacerItem)
        self.labelCount = QtGui.QLabel(Dialog)
        self.labelCount.setObjectName(_fromUtf8("labelCount"))
        self.horizontalLayout2.addWidget(self.labelCount)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout2.addItem(spacerItem1)
        self.btnClose = QtGui.QPushButton(Dialog)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.horizontalLayout2.addWidget(self.btnClose)
        self.gridLayout.addLayout(self.horizontalLayout2, 3, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Экспорт данных в Web-сервис “Прикрепленное население”", None))
        self.btnExport.setText(_translate("Dialog", "Начать", None))
        self.chbFullLog.setText(_translate("Dialog", "Отображать лог", None))
        self.labelCount.setText(_translate("Dialog", "Выбрано человек:", None))
        self.btnClose.setText(_translate("Dialog", "Закрыть", None))

