# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\appendix\importNomenclature\Progress.ui'
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

class Ui_ProgressDialog(object):
    def setupUi(self, ProgressDialog):
        ProgressDialog.setObjectName(_fromUtf8("ProgressDialog"))
        ProgressDialog.resize(439, 274)
        self.gridLayout = QtGui.QGridLayout(ProgressDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        spacerItem = QtGui.QSpacerItem(331, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.btnCancel = QtGui.QPushButton(ProgressDialog)
        self.btnCancel.setDefault(True)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.hboxlayout.addWidget(self.btnCancel)
        self.gridLayout.addLayout(self.hboxlayout, 2, 0, 1, 2)
        self.prbNomenclature = QtGui.QProgressBar(ProgressDialog)
        self.prbNomenclature.setProperty("value", 24)
        self.prbNomenclature.setOrientation(QtCore.Qt.Horizontal)
        self.prbNomenclature.setObjectName(_fromUtf8("prbNomenclature"))
        self.gridLayout.addWidget(self.prbNomenclature, 0, 1, 1, 1)
        self.lblNomenclature = QtGui.QLabel(ProgressDialog)
        self.lblNomenclature.setObjectName(_fromUtf8("lblNomenclature"))
        self.gridLayout.addWidget(self.lblNomenclature, 0, 0, 1, 1)
        self.logBrowser = QtGui.QTextBrowser(ProgressDialog)
        self.logBrowser.setObjectName(_fromUtf8("logBrowser"))
        self.gridLayout.addWidget(self.logBrowser, 1, 0, 1, 2)
        self.actStartWork = QtGui.QAction(ProgressDialog)
        self.actStartWork.setObjectName(_fromUtf8("actStartWork"))

        self.retranslateUi(ProgressDialog)
        QtCore.QMetaObject.connectSlotsByName(ProgressDialog)

    def retranslateUi(self, ProgressDialog):
        ProgressDialog.setWindowTitle(_translate("ProgressDialog", "Процесс загрузки данных", None))
        self.btnCancel.setText(_translate("ProgressDialog", "Отмена", None))
        self.prbNomenclature.setFormat(_translate("ProgressDialog", "%v из %m", None))
        self.lblNomenclature.setText(_translate("ProgressDialog", "Номенклатура", None))
        self.actStartWork.setText(_translate("ProgressDialog", "startWork", None))

