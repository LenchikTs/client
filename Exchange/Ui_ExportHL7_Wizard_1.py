# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ExportHL7_Wizard_1.ui'
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

class Ui_ExportHL7_Wizard_1(object):
    def setupUi(self, ExportHL7_Wizard_1):
        ExportHL7_Wizard_1.setObjectName(_fromUtf8("ExportHL7_Wizard_1"))
        ExportHL7_Wizard_1.setWindowModality(QtCore.Qt.NonModal)
        ExportHL7_Wizard_1.resize(593, 450)
        self.gridlayout = QtGui.QGridLayout(ExportHL7_Wizard_1)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.checkExportAll = QtGui.QCheckBox(ExportHL7_Wizard_1)
        self.checkExportAll.setObjectName(_fromUtf8("checkExportAll"))
        self.hboxlayout.addWidget(self.checkExportAll)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.gridlayout.addLayout(self.hboxlayout, 0, 0, 1, 1)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.checkOnlyOwn = QtGui.QCheckBox(ExportHL7_Wizard_1)
        self.checkOnlyOwn.setChecked(True)
        self.checkOnlyOwn.setObjectName(_fromUtf8("checkOnlyOwn"))
        self.hboxlayout1.addWidget(self.checkOnlyOwn)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem1)
        self.btnClearSelection = QtGui.QPushButton(ExportHL7_Wizard_1)
        self.btnClearSelection.setObjectName(_fromUtf8("btnClearSelection"))
        self.hboxlayout1.addWidget(self.btnClearSelection)
        self.gridlayout.addLayout(self.hboxlayout1, 4, 0, 1, 1)
        self.statusBar = QtGui.QStatusBar(ExportHL7_Wizard_1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusBar.sizePolicy().hasHeightForWidth())
        self.statusBar.setSizePolicy(sizePolicy)
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        self.gridlayout.addWidget(self.statusBar, 6, 0, 1, 1)
        self.splitterTree = QtGui.QSplitter(ExportHL7_Wizard_1)
        self.splitterTree.setOrientation(QtCore.Qt.Horizontal)
        self.splitterTree.setObjectName(_fromUtf8("splitterTree"))
        self.tblItems = CTableView(self.splitterTree)
        self.tblItems.setTabKeyNavigation(False)
        self.tblItems.setAlternatingRowColors(True)
        self.tblItems.setObjectName(_fromUtf8("tblItems"))
        self.gridlayout.addWidget(self.splitterTree, 2, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(ExportHL7_Wizard_1)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.rbAddPers = QtGui.QRadioButton(self.groupBox)
        self.rbAddPers.setObjectName(_fromUtf8("rbAddPers"))
        self.verticalLayout.addWidget(self.rbAddPers)
        self.rbUpdatePers = QtGui.QRadioButton(self.groupBox)
        self.rbUpdatePers.setChecked(True)
        self.rbUpdatePers.setObjectName(_fromUtf8("rbUpdatePers"))
        self.verticalLayout.addWidget(self.rbUpdatePers)
        self.rbDeletePers = QtGui.QRadioButton(self.groupBox)
        self.rbDeletePers.setObjectName(_fromUtf8("rbDeletePers"))
        self.verticalLayout.addWidget(self.rbDeletePers)
        self.rbTerminatePers = QtGui.QRadioButton(self.groupBox)
        self.rbTerminatePers.setObjectName(_fromUtf8("rbTerminatePers"))
        self.verticalLayout.addWidget(self.rbTerminatePers)
        self.gridlayout.addWidget(self.groupBox, 5, 0, 1, 1)
        self.statusBar.raise_()
        self.splitterTree.raise_()
        self.groupBox.raise_()

        self.retranslateUi(ExportHL7_Wizard_1)
        QtCore.QMetaObject.connectSlotsByName(ExportHL7_Wizard_1)

    def retranslateUi(self, ExportHL7_Wizard_1):
        ExportHL7_Wizard_1.setWindowTitle(_translate("ExportHL7_Wizard_1", "Список сотрудников", None))
        self.checkExportAll.setText(_translate("ExportHL7_Wizard_1", "Выгружать всё", None))
        self.checkOnlyOwn.setText(_translate("ExportHL7_Wizard_1", "Только свои", None))
        self.btnClearSelection.setText(_translate("ExportHL7_Wizard_1", "Очистить", None))
        self.statusBar.setToolTip(_translate("ExportHL7_Wizard_1", "A status bar", None))
        self.statusBar.setWhatsThis(_translate("ExportHL7_Wizard_1", "A status bar.", None))
        self.tblItems.setWhatsThis(_translate("ExportHL7_Wizard_1", "список записей", "ура!"))
        self.groupBox.setTitle(_translate("ExportHL7_Wizard_1", "Тип события для выгрузки", None))
        self.rbAddPers.setText(_translate("ExportHL7_Wizard_1", "B01 Добавить личное дело сотрудника", None))
        self.rbUpdatePers.setText(_translate("ExportHL7_Wizard_1", "B02 Обновить личное дело сотрудника", None))
        self.rbDeletePers.setText(_translate("ExportHL7_Wizard_1", "B03 Удалить личное дело сотрудника", None))
        self.rbTerminatePers.setText(_translate("ExportHL7_Wizard_1", "B06 Закрыть личное дело сотрудника", None))

from library.TableView import CTableView
