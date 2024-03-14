# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ExportR29NativePage1.ui'
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

class Ui_ExportPage1(object):
    def setupUi(self, ExportPage1):
        ExportPage1.setObjectName(_fromUtf8("ExportPage1"))
        ExportPage1.resize(530, 480)
        self.gridlayout = QtGui.QGridLayout(ExportPage1)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 11, 0, 1, 3)
        self.btnExport = QtGui.QPushButton(ExportPage1)
        self.btnExport.setObjectName(_fromUtf8("btnExport"))
        self.gridlayout.addWidget(self.btnExport, 12, 1, 1, 1)
        self.btnCancel = QtGui.QPushButton(ExportPage1)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.gridlayout.addWidget(self.btnCancel, 12, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1, 12, 0, 1, 1)
        self.logBrowser = QtGui.QTextBrowser(ExportPage1)
        self.logBrowser.setObjectName(_fromUtf8("logBrowser"))
        self.gridlayout.addWidget(self.logBrowser, 10, 0, 1, 3)
        self.chkVerboseLog = QtGui.QCheckBox(ExportPage1)
        self.chkVerboseLog.setObjectName(_fromUtf8("chkVerboseLog"))
        self.gridlayout.addWidget(self.chkVerboseLog, 8, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem2, 0, 0, 1, 3)
        self.chkExportDS = QtGui.QCheckBox(ExportPage1)
        self.chkExportDS.setObjectName(_fromUtf8("chkExportDS"))
        self.gridlayout.addWidget(self.chkExportDS, 5, 0, 1, 1)
        self.progressBar = CProgressBar(ExportPage1)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridlayout.addWidget(self.progressBar, 7, 0, 1, 3)
        self.chkExportDD = QtGui.QCheckBox(ExportPage1)
        self.chkExportDD.setObjectName(_fromUtf8("chkExportDD"))
        self.gridlayout.addWidget(self.chkExportDD, 3, 0, 1, 1)
        self.tblEventTypeDD = CRBListBox(ExportPage1)
        self.tblEventTypeDD.setEnabled(False)
        self.tblEventTypeDD.setObjectName(_fromUtf8("tblEventTypeDD"))
        self.gridlayout.addWidget(self.tblEventTypeDD, 4, 0, 1, 3)
        self.tblEventTypeDS = CRBListBox(ExportPage1)
        self.tblEventTypeDS.setEnabled(False)
        self.tblEventTypeDS.setObjectName(_fromUtf8("tblEventTypeDS"))
        self.gridlayout.addWidget(self.tblEventTypeDS, 6, 0, 1, 3)
        self.lblRegistryType = QtGui.QLabel(ExportPage1)
        self.lblRegistryType.setObjectName(_fromUtf8("lblRegistryType"))
        self.gridlayout.addWidget(self.lblRegistryType, 1, 0, 1, 1)
        self.cmbRegistryType = QtGui.QComboBox(ExportPage1)
        self.cmbRegistryType.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.cmbRegistryType.setObjectName(_fromUtf8("cmbRegistryType"))
        self.cmbRegistryType.addItem(_fromUtf8(""))
        self.cmbRegistryType.addItem(_fromUtf8(""))
        self.cmbRegistryType.addItem(_fromUtf8(""))
        self.cmbRegistryType.addItem(_fromUtf8(""))
        self.cmbRegistryType.addItem(_fromUtf8(""))
        self.cmbRegistryType.addItem(_fromUtf8(""))
        self.cmbRegistryType.addItem(_fromUtf8(""))
        self.cmbRegistryType.addItem(_fromUtf8(""))
        self.gridlayout.addWidget(self.cmbRegistryType, 2, 0, 1, 3)
        self.chkEventSplit = QtGui.QCheckBox(ExportPage1)
        self.chkEventSplit.setObjectName(_fromUtf8("chkEventSplit"))
        self.gridlayout.addWidget(self.chkEventSplit, 9, 0, 1, 1)

        self.retranslateUi(ExportPage1)
        QtCore.QObject.connect(self.chkExportDD, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.tblEventTypeDD.setEnabled)
        QtCore.QObject.connect(self.chkExportDS, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.tblEventTypeDS.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(ExportPage1)

    def retranslateUi(self, ExportPage1):
        ExportPage1.setWindowTitle(_translate("ExportPage1", "Form", None))
        self.btnExport.setText(_translate("ExportPage1", "экспорт", None))
        self.btnCancel.setText(_translate("ExportPage1", "прервать", None))
        self.chkVerboseLog.setText(_translate("ExportPage1", "подробный отчет", None))
        self.chkExportDS.setText(_translate("ExportPage1", "Выгружать информацию о ДС", None))
        self.chkExportDD.setText(_translate("ExportPage1", "Выгружать информацию о ДД", None))
        self.lblRegistryType.setText(_translate("ExportPage1", "Вид реестра оказанной медицинской помощи:", None))
        self.cmbRegistryType.setItemText(0, _translate("ExportPage1", "Граждане, застрахованные вне территории Архангельской области", None))
        self.cmbRegistryType.setItemText(1, _translate("ExportPage1", "Граждане, застрахованные на территории Архангельской области", None))
        self.cmbRegistryType.setItemText(2, _translate("ExportPage1", "Реестр работающих граждан по Постановлению Правительства РФ от 30.12.2006 г. №864", None))
        self.cmbRegistryType.setItemText(3, _translate("ExportPage1", "Реестр граждан, проходящих дополнительную диспансеризацию по Постановлению Правительства РФ от 30.12.2006 г. №860", None))
        self.cmbRegistryType.setItemText(4, _translate("ExportPage1", "Реестр детей-сирот и детей, оставшихся без попечения родителей, проходящих дополнительную диспансеризацию по Постановлению Правительства РФ от 10.04.2007 г. №22", None))
        self.cmbRegistryType.setItemText(5, _translate("ExportPage1", "Реестр граждан, проходящих дополнительную диспансеризацию по Постановлению Правительства РФ от 30.12.2006 г. №860", None))
        self.cmbRegistryType.setItemText(6, _translate("ExportPage1", "Реестр пребывающих в стационарных учреждениях детей-сирот и детей, находящихся в трудной жизненной ситуации, проходящих диспансеризацию по Постановлению Правительства РФ", None))
        self.cmbRegistryType.setItemText(7, _translate("ExportPage1", "Реестр граждан, проходящих дополнительную диспансеризацию по Постановлению Правительства РФ", None))
        self.chkEventSplit.setText(_translate("ExportPage1", "разбивать события на визиты", None))

from library.ProgressBar import CProgressBar
from library.RBListBox import CRBListBox
