# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ExportFeedDataCsv_Wizard_1.ui'
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

class Ui_ExportFeedDataCsv_Wizard_1(object):
    def setupUi(self, ExportFeedDataCsv_Wizard_1):
        ExportFeedDataCsv_Wizard_1.setObjectName(_fromUtf8("ExportFeedDataCsv_Wizard_1"))
        ExportFeedDataCsv_Wizard_1.setWindowModality(QtCore.Qt.NonModal)
        ExportFeedDataCsv_Wizard_1.resize(412, 177)
        self.gridlayout = QtGui.QGridLayout(ExportFeedDataCsv_Wizard_1)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.statusBar = QtGui.QStatusBar(ExportFeedDataCsv_Wizard_1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusBar.sizePolicy().hasHeightForWidth())
        self.statusBar.setSizePolicy(sizePolicy)
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        self.gridlayout.addWidget(self.statusBar, 2, 0, 1, 1)
        self.splitterTree = QtGui.QSplitter(ExportFeedDataCsv_Wizard_1)
        self.splitterTree.setOrientation(QtCore.Qt.Horizontal)
        self.splitterTree.setObjectName(_fromUtf8("splitterTree"))
        self.gbFilter = QtGui.QGroupBox(self.splitterTree)
        self.gbFilter.setObjectName(_fromUtf8("gbFilter"))
        self.gridLayout = QtGui.QGridLayout(self.gbFilter)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.lblOrgStructure = QtGui.QLabel(self.gbFilter)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout_4.addWidget(self.lblOrgStructure, 3, 0, 1, 1)
        self.edtEndTime = QtGui.QTimeEdit(self.gbFilter)
        self.edtEndTime.setObjectName(_fromUtf8("edtEndTime"))
        self.gridLayout_4.addWidget(self.edtEndTime, 2, 3, 1, 1)
        self.edtEndDate = CDateEdit(self.gbFilter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setMinimumSize(QtCore.QSize(95, 0))
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout_4.addWidget(self.edtEndDate, 2, 2, 1, 1)
        self.lblBegDate = QtGui.QLabel(self.gbFilter)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout_4.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.lblEndDate = QtGui.QLabel(self.gbFilter)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout_4.addWidget(self.lblEndDate, 2, 0, 1, 1)
        self.edtBegDate = CDateEdit(self.gbFilter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setMinimumSize(QtCore.QSize(95, 0))
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout_4.addWidget(self.edtBegDate, 0, 2, 1, 1)
        self.edtBegTime = QtGui.QTimeEdit(self.gbFilter)
        self.edtBegTime.setObjectName(_fromUtf8("edtBegTime"))
        self.gridLayout_4.addWidget(self.edtBegTime, 0, 3, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 0, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem2, 2, 1, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(self.gbFilter)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout_4.addWidget(self.cmbOrgStructure, 3, 1, 1, 3)
        self.gridLayout.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        self.gridlayout.addWidget(self.splitterTree, 1, 0, 1, 1)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtBegDate)

        self.retranslateUi(ExportFeedDataCsv_Wizard_1)
        QtCore.QMetaObject.connectSlotsByName(ExportFeedDataCsv_Wizard_1)
        ExportFeedDataCsv_Wizard_1.setTabOrder(self.edtBegDate, self.edtBegTime)
        ExportFeedDataCsv_Wizard_1.setTabOrder(self.edtBegTime, self.edtEndDate)
        ExportFeedDataCsv_Wizard_1.setTabOrder(self.edtEndDate, self.edtEndTime)
        ExportFeedDataCsv_Wizard_1.setTabOrder(self.edtEndTime, self.cmbOrgStructure)

    def retranslateUi(self, ExportFeedDataCsv_Wizard_1):
        ExportFeedDataCsv_Wizard_1.setWindowTitle(_translate("ExportFeedDataCsv_Wizard_1", "Экспорт данных о питании", None))
        self.statusBar.setToolTip(_translate("ExportFeedDataCsv_Wizard_1", "A status bar", None))
        self.statusBar.setWhatsThis(_translate("ExportFeedDataCsv_Wizard_1", "A status bar.", None))
        self.gbFilter.setTitle(_translate("ExportFeedDataCsv_Wizard_1", "Фильтр", None))
        self.lblOrgStructure.setText(_translate("ExportFeedDataCsv_Wizard_1", "&Подразделение", None))
        self.edtEndDate.setDisplayFormat(_translate("ExportFeedDataCsv_Wizard_1", "dd.MM.yyyy", None))
        self.lblBegDate.setText(_translate("ExportFeedDataCsv_Wizard_1", "&Начало периода", None))
        self.lblEndDate.setText(_translate("ExportFeedDataCsv_Wizard_1", "&Окончание периода", None))
        self.edtBegDate.setDisplayFormat(_translate("ExportFeedDataCsv_Wizard_1", "dd.MM.yyyy", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.DateEdit import CDateEdit
