# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\TissueJournal\LabResultReaderDialog.ui'
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

class Ui_LabResultReader(object):
    def setupUi(self, LabResultReader):
        LabResultReader.setObjectName(_fromUtf8("LabResultReader"))
        LabResultReader.resize(528, 335)
        self.gridLayout = QtGui.QGridLayout(LabResultReader)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(LabResultReader)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.tblItems = CLabResultEquipmentTableView(self.splitter)
        self.tblItems.setObjectName(_fromUtf8("tblItems"))
        self.logWidget = CLabResultLogWidget(self.splitter)
        self.logWidget.setObjectName(_fromUtf8("logWidget"))
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.chkOnlyFromModel = QtGui.QCheckBox(LabResultReader)
        self.chkOnlyFromModel.setEnabled(False)
        self.chkOnlyFromModel.setObjectName(_fromUtf8("chkOnlyFromModel"))
        self.gridLayout.addWidget(self.chkOnlyFromModel, 3, 0, 1, 1)
        self.progressBar = CProgressBar(LabResultReader)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 4, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(LabResultReader)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 1)
        self.chkRewrite = QtGui.QCheckBox(LabResultReader)
        self.chkRewrite.setEnabled(False)
        self.chkRewrite.setObjectName(_fromUtf8("chkRewrite"))
        self.gridLayout.addWidget(self.chkRewrite, 1, 0, 2, 1)

        self.retranslateUi(LabResultReader)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), LabResultReader.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), LabResultReader.reject)
        QtCore.QMetaObject.connectSlotsByName(LabResultReader)
        LabResultReader.setTabOrder(self.tblItems, self.chkRewrite)
        LabResultReader.setTabOrder(self.chkRewrite, self.chkOnlyFromModel)
        LabResultReader.setTabOrder(self.chkOnlyFromModel, self.buttonBox)

    def retranslateUi(self, LabResultReader):
        LabResultReader.setWindowTitle(_translate("LabResultReader", "Dialog", None))
        self.chkOnlyFromModel.setText(_translate("LabResultReader", "Обрабатывать только отображенные пробы", None))
        self.chkRewrite.setText(_translate("LabResultReader", "Перезаписовать результат", None))

from TissueJournal.LabResultEquipmentTable import CLabResultEquipmentTableView
from TissueJournal.LabResultLogWidget import CLabResultLogWidget
from library.ProgressBar import CProgressBar
