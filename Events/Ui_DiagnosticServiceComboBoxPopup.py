# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\Samson\UP_s11\client_merge\Events\DiagnosticServiceComboBoxPopup.ui'
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

class Ui_DiagnosticServiceComboBoxPopup(object):
    def setupUi(self, DiagnosticServiceComboBoxPopup):
        DiagnosticServiceComboBoxPopup.setObjectName(_fromUtf8("DiagnosticServiceComboBoxPopup"))
        DiagnosticServiceComboBoxPopup.resize(469, 204)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(DiagnosticServiceComboBoxPopup)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.tabWidget = QtGui.QTabWidget(DiagnosticServiceComboBoxPopup)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.South)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabServices = QtGui.QWidget()
        self.tabServices.setObjectName(_fromUtf8("tabServices"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tabServices)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tblServices = CTableView(self.tabServices)
        self.tblServices.setObjectName(_fromUtf8("tblServices"))
        self.verticalLayout.addWidget(self.tblServices)
        self.tabWidget.addTab(self.tabServices, _fromUtf8(""))
        self.tabSearch = QtGui.QWidget()
        self.tabSearch.setObjectName(_fromUtf8("tabSearch"))
        self.gridLayout = QtGui.QGridLayout(self.tabSearch)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtName = QtGui.QLineEdit(self.tabSearch)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 0, 1, 1, 2)
        self.lblName = QtGui.QLabel(self.tabSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(172, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(self.tabSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Reset)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 3, 0, 1, 1)
        self.gridLayout.setColumnMinimumWidth(2, 2)
        self.gridLayout.setColumnStretch(2, 2)
        self.tabWidget.addTab(self.tabSearch, _fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.tabWidget)
        self.lblName.setBuddy(self.edtName)

        self.retranslateUi(DiagnosticServiceComboBoxPopup)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(DiagnosticServiceComboBoxPopup)
        DiagnosticServiceComboBoxPopup.setTabOrder(self.tabWidget, self.edtName)
        DiagnosticServiceComboBoxPopup.setTabOrder(self.edtName, self.buttonBox)

    def retranslateUi(self, DiagnosticServiceComboBoxPopup):
        DiagnosticServiceComboBoxPopup.setWindowTitle(_translate("DiagnosticServiceComboBoxPopup", "Form", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabServices), _translate("DiagnosticServiceComboBoxPopup", "&Услуги", None))
        self.lblName.setText(_translate("DiagnosticServiceComboBoxPopup", "&Название содержит", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSearch), _translate("DiagnosticServiceComboBoxPopup", "&Поиск", None))

from library.TableView import CTableView
