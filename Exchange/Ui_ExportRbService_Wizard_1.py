# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ExportRbService_Wizard_1.ui'
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

class Ui_ExportRbService_Wizard_1(object):
    def setupUi(self, ExportRbService_Wizard_1):
        ExportRbService_Wizard_1.setObjectName(_fromUtf8("ExportRbService_Wizard_1"))
        ExportRbService_Wizard_1.setWindowModality(QtCore.Qt.NonModal)
        ExportRbService_Wizard_1.resize(453, 343)
        self.gridlayout = QtGui.QGridLayout(ExportRbService_Wizard_1)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.checkExportAll = QtGui.QCheckBox(ExportRbService_Wizard_1)
        self.checkExportAll.setObjectName(_fromUtf8("checkExportAll"))
        self.hboxlayout.addWidget(self.checkExportAll)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.gridlayout.addLayout(self.hboxlayout, 0, 0, 1, 1)
        self.splitterTree = QtGui.QSplitter(ExportRbService_Wizard_1)
        self.splitterTree.setOrientation(QtCore.Qt.Horizontal)
        self.splitterTree.setObjectName(_fromUtf8("splitterTree"))
        self.tblItems = CTableView(self.splitterTree)
        self.tblItems.setTabKeyNavigation(False)
        self.tblItems.setAlternatingRowColors(True)
        self.tblItems.setObjectName(_fromUtf8("tblItems"))
        self.gbFilter = QtGui.QGroupBox(self.splitterTree)
        self.gbFilter.setObjectName(_fromUtf8("gbFilter"))
        self.gridLayout = QtGui.QGridLayout(self.gbFilter)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.gbFilter)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.edtFilterBegDate = QtGui.QDateEdit(self.gbFilter)
        self.edtFilterBegDate.setEnabled(False)
        self.edtFilterBegDate.setObjectName(_fromUtf8("edtFilterBegDate"))
        self.horizontalLayout_2.addWidget(self.edtFilterBegDate)
        self.gridLayout.addLayout(self.horizontalLayout_2, 5, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(self.gbFilter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.edtFilterEndDate = QtGui.QDateEdit(self.gbFilter)
        self.edtFilterEndDate.setEnabled(False)
        self.edtFilterEndDate.setObjectName(_fromUtf8("edtFilterEndDate"))
        self.horizontalLayout.addWidget(self.edtFilterEndDate)
        self.gridLayout.addLayout(self.horizontalLayout, 6, 0, 1, 1)
        self.chkFilterCode = QtGui.QCheckBox(self.gbFilter)
        self.chkFilterCode.setObjectName(_fromUtf8("chkFilterCode"))
        self.gridLayout.addWidget(self.chkFilterCode, 0, 0, 1, 1)
        self.edtFilterCode = QtGui.QLineEdit(self.gbFilter)
        self.edtFilterCode.setEnabled(False)
        self.edtFilterCode.setObjectName(_fromUtf8("edtFilterCode"))
        self.gridLayout.addWidget(self.edtFilterCode, 1, 0, 1, 1)
        self.chkFilterEIS = QtGui.QCheckBox(self.gbFilter)
        self.chkFilterEIS.setTristate(True)
        self.chkFilterEIS.setObjectName(_fromUtf8("chkFilterEIS"))
        self.gridLayout.addWidget(self.chkFilterEIS, 2, 0, 1, 1)
        self.chkFilterNomenclature = QtGui.QCheckBox(self.gbFilter)
        self.chkFilterNomenclature.setTristate(True)
        self.chkFilterNomenclature.setObjectName(_fromUtf8("chkFilterNomenclature"))
        self.gridLayout.addWidget(self.chkFilterNomenclature, 3, 0, 1, 1)
        self.chkFilterPeriod = QtGui.QCheckBox(self.gbFilter)
        self.chkFilterPeriod.setObjectName(_fromUtf8("chkFilterPeriod"))
        self.gridLayout.addWidget(self.chkFilterPeriod, 4, 0, 1, 1)
        self.bbxFilter = QtGui.QDialogButtonBox(self.gbFilter)
        self.bbxFilter.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Reset)
        self.bbxFilter.setObjectName(_fromUtf8("bbxFilter"))
        self.gridLayout.addWidget(self.bbxFilter, 8, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 7, 0, 1, 1)
        self.chkFilterCode.raise_()
        self.edtFilterCode.raise_()
        self.chkFilterEIS.raise_()
        self.chkFilterNomenclature.raise_()
        self.chkFilterPeriod.raise_()
        self.bbxFilter.raise_()
        self.gridlayout.addWidget(self.splitterTree, 2, 0, 1, 1)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.btnSelectAll = QtGui.QPushButton(ExportRbService_Wizard_1)
        self.btnSelectAll.setObjectName(_fromUtf8("btnSelectAll"))
        self.hboxlayout1.addWidget(self.btnSelectAll)
        self.btnClearSelection = QtGui.QPushButton(ExportRbService_Wizard_1)
        self.btnClearSelection.setObjectName(_fromUtf8("btnClearSelection"))
        self.hboxlayout1.addWidget(self.btnClearSelection)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem2)
        self.gridlayout.addLayout(self.hboxlayout1, 3, 0, 1, 1)
        self.statusBar = QtGui.QStatusBar(ExportRbService_Wizard_1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusBar.sizePolicy().hasHeightForWidth())
        self.statusBar.setSizePolicy(sizePolicy)
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        self.gridlayout.addWidget(self.statusBar, 4, 0, 1, 1)

        self.retranslateUi(ExportRbService_Wizard_1)
        QtCore.QMetaObject.connectSlotsByName(ExportRbService_Wizard_1)
        ExportRbService_Wizard_1.setTabOrder(self.checkExportAll, self.tblItems)
        ExportRbService_Wizard_1.setTabOrder(self.tblItems, self.chkFilterCode)
        ExportRbService_Wizard_1.setTabOrder(self.chkFilterCode, self.edtFilterCode)
        ExportRbService_Wizard_1.setTabOrder(self.edtFilterCode, self.chkFilterEIS)
        ExportRbService_Wizard_1.setTabOrder(self.chkFilterEIS, self.chkFilterNomenclature)
        ExportRbService_Wizard_1.setTabOrder(self.chkFilterNomenclature, self.chkFilterPeriod)
        ExportRbService_Wizard_1.setTabOrder(self.chkFilterPeriod, self.edtFilterBegDate)
        ExportRbService_Wizard_1.setTabOrder(self.edtFilterBegDate, self.edtFilterEndDate)
        ExportRbService_Wizard_1.setTabOrder(self.edtFilterEndDate, self.bbxFilter)
        ExportRbService_Wizard_1.setTabOrder(self.bbxFilter, self.btnSelectAll)
        ExportRbService_Wizard_1.setTabOrder(self.btnSelectAll, self.btnClearSelection)

    def retranslateUi(self, ExportRbService_Wizard_1):
        ExportRbService_Wizard_1.setWindowTitle(_translate("ExportRbService_Wizard_1", "Список записей", None))
        self.checkExportAll.setText(_translate("ExportRbService_Wizard_1", "Выгружать всё", None))
        self.tblItems.setWhatsThis(_translate("ExportRbService_Wizard_1", "список записей", "ура!"))
        self.gbFilter.setTitle(_translate("ExportRbService_Wizard_1", "Фильтр", None))
        self.label.setText(_translate("ExportRbService_Wizard_1", "с", None))
        self.label_2.setText(_translate("ExportRbService_Wizard_1", "по", None))
        self.chkFilterCode.setText(_translate("ExportRbService_Wizard_1", "Код начинается с", None))
        self.chkFilterEIS.setText(_translate("ExportRbService_Wizard_1", "Унаследованно из ЕИС", None))
        self.chkFilterNomenclature.setText(_translate("ExportRbService_Wizard_1", "Номенклатура", None))
        self.chkFilterPeriod.setText(_translate("ExportRbService_Wizard_1", "Период", None))
        self.btnSelectAll.setText(_translate("ExportRbService_Wizard_1", "Выбрать все", None))
        self.btnClearSelection.setText(_translate("ExportRbService_Wizard_1", "Очистить", None))
        self.statusBar.setToolTip(_translate("ExportRbService_Wizard_1", "A status bar", None))
        self.statusBar.setWhatsThis(_translate("ExportRbService_Wizard_1", "A status bar.", None))

from library.TableView import CTableView
