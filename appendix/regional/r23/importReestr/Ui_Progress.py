# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\appendix\regional\r23\importReestr\Progress.ui'
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
        ProgressDialog.resize(440, 407)
        self.gridLayout = QtGui.QGridLayout(ProgressDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblServices = QtGui.QLabel(ProgressDialog)
        self.lblServices.setObjectName(_fromUtf8("lblServices"))
        self.gridLayout.addWidget(self.lblServices, 3, 0, 1, 1)
        self.prbServices = QtGui.QProgressBar(ProgressDialog)
        self.prbServices.setProperty("value", 24)
        self.prbServices.setObjectName(_fromUtf8("prbServices"))
        self.gridLayout.addWidget(self.prbServices, 3, 1, 1, 1)
        self.lblElapsed = QtGui.QLabel(ProgressDialog)
        self.lblElapsed.setObjectName(_fromUtf8("lblElapsed"))
        self.gridLayout.addWidget(self.lblElapsed, 4, 0, 1, 2)
        self.prbClients = QtGui.QProgressBar(ProgressDialog)
        self.prbClients.setProperty("value", 24)
        self.prbClients.setOrientation(QtCore.Qt.Horizontal)
        self.prbClients.setObjectName(_fromUtf8("prbClients"))
        self.gridLayout.addWidget(self.prbClients, 2, 1, 1, 1)
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
        self.gridLayout.addLayout(self.hboxlayout, 6, 0, 1, 2)
        self.lblClients = QtGui.QLabel(ProgressDialog)
        self.lblClients.setObjectName(_fromUtf8("lblClients"))
        self.gridLayout.addWidget(self.lblClients, 2, 0, 1, 1)
        self.prbPlaces = QtGui.QProgressBar(ProgressDialog)
        self.prbPlaces.setProperty("value", 24)
        self.prbPlaces.setOrientation(QtCore.Qt.Horizontal)
        self.prbPlaces.setObjectName(_fromUtf8("prbPlaces"))
        self.gridLayout.addWidget(self.prbPlaces, 0, 1, 1, 1)
        self.lblPlaces = QtGui.QLabel(ProgressDialog)
        self.lblPlaces.setObjectName(_fromUtf8("lblPlaces"))
        self.gridLayout.addWidget(self.lblPlaces, 0, 0, 1, 1)
        self.logBrowser = QtGui.QTextBrowser(ProgressDialog)
        self.logBrowser.setObjectName(_fromUtf8("logBrowser"))
        self.gridLayout.addWidget(self.logBrowser, 5, 0, 1, 2)
        self.lblOrgs = QtGui.QLabel(ProgressDialog)
        self.lblOrgs.setObjectName(_fromUtf8("lblOrgs"))
        self.gridLayout.addWidget(self.lblOrgs, 1, 0, 1, 1)
        self.prbOrgs = QtGui.QProgressBar(ProgressDialog)
        self.prbOrgs.setProperty("value", 24)
        self.prbOrgs.setObjectName(_fromUtf8("prbOrgs"))
        self.gridLayout.addWidget(self.prbOrgs, 1, 1, 1, 1)
        self.actStartWork = QtGui.QAction(ProgressDialog)
        self.actStartWork.setObjectName(_fromUtf8("actStartWork"))

        self.retranslateUi(ProgressDialog)
        QtCore.QMetaObject.connectSlotsByName(ProgressDialog)

    def retranslateUi(self, ProgressDialog):
        ProgressDialog.setWindowTitle(_translate("ProgressDialog", "Процесс загрузки данных", None))
        self.lblServices.setText(_translate("ProgressDialog", "Услуги", None))
        self.prbServices.setFormat(_translate("ProgressDialog", "%v из %m", None))
        self.lblElapsed.setText(_translate("ProgressDialog", "Текущая операция: ??? зап/с, окончание в ??:??:??", None))
        self.prbClients.setFormat(_translate("ProgressDialog", "%v из %m", None))
        self.btnCancel.setText(_translate("ProgressDialog", "Отмена", None))
        self.lblClients.setText(_translate("ProgressDialog", "Население", None))
        self.prbPlaces.setFormat(_translate("ProgressDialog", "%v из %m", None))
        self.lblPlaces.setText(_translate("ProgressDialog", "Населённые пункты", None))
        self.lblOrgs.setText(_translate("ProgressDialog", "Организации", None))
        self.prbOrgs.setFormat(_translate("ProgressDialog", "%v из %m", None))
        self.actStartWork.setText(_translate("ProgressDialog", "startWork", None))

