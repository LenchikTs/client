# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\library\DbfViewDialog.ui'
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

class Ui_DbfViewDialog(object):
    def setupUi(self, DbfViewDialog):
        DbfViewDialog.setObjectName(_fromUtf8("DbfViewDialog"))
        DbfViewDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        DbfViewDialog.resize(593, 450)
        DbfViewDialog.setSizeGripEnabled(True)
        DbfViewDialog.setModal(True)
        self.gridlayout = QtGui.QGridLayout(DbfViewDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.tblDbf = CTableView(DbfViewDialog)
        self.tblDbf.setWhatsThis(_fromUtf8(""))
        self.tblDbf.setTabKeyNavigation(False)
        self.tblDbf.setAlternatingRowColors(True)
        self.tblDbf.setObjectName(_fromUtf8("tblDbf"))
        self.gridlayout.addWidget(self.tblDbf, 0, 0, 1, 1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.statusBar = QtGui.QStatusBar(DbfViewDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusBar.sizePolicy().hasHeightForWidth())
        self.statusBar.setSizePolicy(sizePolicy)
        self.statusBar.setToolTip(_fromUtf8(""))
        self.statusBar.setWhatsThis(_fromUtf8(""))
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        self.hboxlayout.addWidget(self.statusBar)
        self.btnCancel = QtGui.QPushButton(DbfViewDialog)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.hboxlayout.addWidget(self.btnCancel)
        self.gridlayout.addLayout(self.hboxlayout, 1, 0, 1, 1)

        self.retranslateUi(DbfViewDialog)
        QtCore.QObject.connect(self.btnCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), DbfViewDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DbfViewDialog)
        DbfViewDialog.setTabOrder(self.tblDbf, self.btnCancel)

    def retranslateUi(self, DbfViewDialog):
        DbfViewDialog.setWindowTitle(_translate("DbfViewDialog", "Просмотр DBF файла", None))
        self.btnCancel.setWhatsThis(_translate("DbfViewDialog", "выйти из списка без выбора", None))
        self.btnCancel.setText(_translate("DbfViewDialog", "Закрыть", None))

from TableView import CTableView
