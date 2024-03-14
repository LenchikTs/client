# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Orgs\SuiteReagentComboBoxPopup.ui'
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

class Ui_SuiteReagentPopupForm(object):
    def setupUi(self, SuiteReagentPopupForm):
        SuiteReagentPopupForm.setObjectName(_fromUtf8("SuiteReagentPopupForm"))
        SuiteReagentPopupForm.resize(497, 315)
        self.verticalLayout = QtGui.QVBoxLayout(SuiteReagentPopupForm)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(SuiteReagentPopupForm)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabSuiteReagent = QtGui.QWidget()
        self.tabSuiteReagent.setObjectName(_fromUtf8("tabSuiteReagent"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tabSuiteReagent)
        self.verticalLayout_2.setMargin(4)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tblSuiteReagent = CTableView(self.tabSuiteReagent)
        self.tblSuiteReagent.setObjectName(_fromUtf8("tblSuiteReagent"))
        self.verticalLayout_2.addWidget(self.tblSuiteReagent)
        self.tabWidget.addTab(self.tabSuiteReagent, _fromUtf8(""))
        self.tabFind = QtGui.QWidget()
        self.tabFind.setObjectName(_fromUtf8("tabFind"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tabFind)
        self.verticalLayout_3.setMargin(4)
        self.verticalLayout_3.setSpacing(4)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.chkOnlyByTest = QtGui.QCheckBox(self.tabFind)
        self.chkOnlyByTest.setChecked(True)
        self.chkOnlyByTest.setObjectName(_fromUtf8("chkOnlyByTest"))
        self.verticalLayout_3.addWidget(self.chkOnlyByTest)
        self.chkNotOverdue = QtGui.QCheckBox(self.tabFind)
        self.chkNotOverdue.setChecked(True)
        self.chkNotOverdue.setObjectName(_fromUtf8("chkNotOverdue"))
        self.verticalLayout_3.addWidget(self.chkNotOverdue)
        self.chkStartOperation = QtGui.QCheckBox(self.tabFind)
        self.chkStartOperation.setChecked(True)
        self.chkStartOperation.setObjectName(_fromUtf8("chkStartOperation"))
        self.verticalLayout_3.addWidget(self.chkStartOperation)
        self.chkNotOverLimit = QtGui.QCheckBox(self.tabFind)
        self.chkNotOverLimit.setChecked(True)
        self.chkNotOverLimit.setObjectName(_fromUtf8("chkNotOverLimit"))
        self.verticalLayout_3.addWidget(self.chkNotOverLimit)
        spacerItem = QtGui.QSpacerItem(20, 123, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.buttonBox = CApplyResetDialogButtonBox(self.tabFind)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Reset)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_3.addWidget(self.buttonBox)
        self.tabWidget.addTab(self.tabFind, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(SuiteReagentPopupForm)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(SuiteReagentPopupForm)

    def retranslateUi(self, SuiteReagentPopupForm):
        SuiteReagentPopupForm.setWindowTitle(_translate("SuiteReagentPopupForm", "Form", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSuiteReagent), _translate("SuiteReagentPopupForm", "&Наборы", None))
        self.chkOnlyByTest.setText(_translate("SuiteReagentPopupForm", "Только наборы относяшиеся к тесту", None))
        self.chkNotOverdue.setText(_translate("SuiteReagentPopupForm", "Не просрочены", None))
        self.chkStartOperation.setText(_translate("SuiteReagentPopupForm", "Введены в работу", None))
        self.chkNotOverLimit.setText(_translate("SuiteReagentPopupForm", "Не превышен плановое количество", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFind), _translate("SuiteReagentPopupForm", "&Поиск", None))

from library.DialogButtonBox import CApplyResetDialogButtonBox
from library.TableView import CTableView
