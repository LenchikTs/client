# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_test\Registry\DemogrCertificates.ui'
#
# Created: Tue Nov  6 15:48:27 2018
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_DemogrCertificatesDialog(object):
    def setupUi(self, DemogrCertificatesDialog):
        DemogrCertificatesDialog.setObjectName(_fromUtf8("DemogrCertificatesDialog"))
        DemogrCertificatesDialog.resize(1000, 700)
        self.gridLayout_2 = QtGui.QGridLayout(DemogrCertificatesDialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnSyncSelected = QtGui.QPushButton(DemogrCertificatesDialog)
        self.btnSyncSelected.setObjectName(_fromUtf8("btnSyncSelected"))
        self.horizontalLayout.addWidget(self.btnSyncSelected)
        self.btnFindClient = QtGui.QPushButton(DemogrCertificatesDialog)
        self.btnFindClient.setObjectName(_fromUtf8("btnFindClient"))
        self.horizontalLayout.addWidget(self.btnFindClient)
        self.btnShowReport = QtGui.QPushButton(DemogrCertificatesDialog)
        self.btnShowReport.setObjectName(_fromUtf8("btnShowReport"))
        self.horizontalLayout.addWidget(self.btnShowReport)
        self.btnSelectAll = QtGui.QPushButton(DemogrCertificatesDialog)
        self.btnSelectAll.setObjectName(_fromUtf8("btnSelectAll"))
        self.horizontalLayout.addWidget(self.btnSelectAll)
        self.btnClearSelection = QtGui.QPushButton(DemogrCertificatesDialog)
        self.btnClearSelection.setObjectName(_fromUtf8("btnClearSelection"))
        self.horizontalLayout.addWidget(self.btnClearSelection)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.tblCertificates = CTableView(DemogrCertificatesDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblCertificates.sizePolicy().hasHeightForWidth())
        self.tblCertificates.setSizePolicy(sizePolicy)
        self.tblCertificates.setObjectName(_fromUtf8("tblCertificates"))
        self.gridLayout_2.addWidget(self.tblCertificates, 1, 0, 1, 1)
        self.txtCertificateInfo = QtGui.QTextBrowser(DemogrCertificatesDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtCertificateInfo.sizePolicy().hasHeightForWidth())
        self.txtCertificateInfo.setSizePolicy(sizePolicy)
        self.txtCertificateInfo.setObjectName(_fromUtf8("txtCertificateInfo"))
        self.gridLayout_2.addWidget(self.txtCertificateInfo, 2, 0, 1, 1)
        self.lblCertificatesCount = QtGui.QLabel(DemogrCertificatesDialog)
        self.lblCertificatesCount.setObjectName(_fromUtf8("lblCertificatesCount"))
        self.gridLayout_2.addWidget(self.lblCertificatesCount, 3, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(DemogrCertificatesDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.chkFilterSurname = QtGui.QCheckBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkFilterSurname.sizePolicy().hasHeightForWidth())
        self.chkFilterSurname.setSizePolicy(sizePolicy)
        self.chkFilterSurname.setMaximumSize(QtCore.QSize(16777215, 14))
        self.chkFilterSurname.setObjectName(_fromUtf8("chkFilterSurname"))
        self.verticalLayout.addWidget(self.chkFilterSurname)
        self.edtFilterSurname = QtGui.QLineEdit(self.groupBox)
        self.edtFilterSurname.setEnabled(False)
        self.edtFilterSurname.setObjectName(_fromUtf8("edtFilterSurname"))
        self.verticalLayout.addWidget(self.edtFilterSurname)
        self.chkFilterName = QtGui.QCheckBox(self.groupBox)
        self.chkFilterName.setMaximumSize(QtCore.QSize(16777215, 14))
        self.chkFilterName.setObjectName(_fromUtf8("chkFilterName"))
        self.verticalLayout.addWidget(self.chkFilterName)
        self.edtFilterName = QtGui.QLineEdit(self.groupBox)
        self.edtFilterName.setEnabled(False)
        self.edtFilterName.setObjectName(_fromUtf8("edtFilterName"))
        self.verticalLayout.addWidget(self.edtFilterName)
        self.chkFilterPatronymic = QtGui.QCheckBox(self.groupBox)
        self.chkFilterPatronymic.setMaximumSize(QtCore.QSize(16777215, 14))
        self.chkFilterPatronymic.setObjectName(_fromUtf8("chkFilterPatronymic"))
        self.verticalLayout.addWidget(self.chkFilterPatronymic)
        self.edtFilterPatronymic = QtGui.QLineEdit(self.groupBox)
        self.edtFilterPatronymic.setEnabled(False)
        self.edtFilterPatronymic.setObjectName(_fromUtf8("edtFilterPatronymic"))
        self.verticalLayout.addWidget(self.edtFilterPatronymic)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.edtDeathDateFrom = QtGui.QDateEdit(self.groupBox)
        self.edtDeathDateFrom.setObjectName(_fromUtf8("edtDeathDateFrom"))
        self.gridLayout_3.addWidget(self.edtDeathDateFrom, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)
        self.edtDeathDateTo = QtGui.QDateEdit(self.groupBox)
        self.edtDeathDateTo.setObjectName(_fromUtf8("edtDeathDateTo"))
        self.gridLayout_3.addWidget(self.edtDeathDateTo, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_3)
        self.filterButtonBox = QtGui.QDialogButtonBox(self.groupBox)
        self.filterButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Reset)
        self.filterButtonBox.setObjectName(_fromUtf8("filterButtonBox"))
        self.verticalLayout.addWidget(self.filterButtonBox)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 1, 4, 1)

        self.retranslateUi(DemogrCertificatesDialog)
        QtCore.QMetaObject.connectSlotsByName(DemogrCertificatesDialog)

    def retranslateUi(self, DemogrCertificatesDialog):
        DemogrCertificatesDialog.setWindowTitle(_translate("DemogrCertificatesDialog", "Сервис Демография (умершие)", None))
        self.btnSyncSelected.setText(_translate("DemogrCertificatesDialog", "Синхронизировать список", None))
        self.btnFindClient.setText(_translate("DemogrCertificatesDialog", "Найти соответствие", None))
        self.btnShowReport.setText(_translate("DemogrCertificatesDialog", "Печать", None))
        self.btnSelectAll.setText(_translate("DemogrCertificatesDialog", "Выделить все", None))
        self.btnClearSelection.setText(_translate("DemogrCertificatesDialog", "Отменить все", None))
        self.lblCertificatesCount.setText(_translate("DemogrCertificatesDialog", "Список пуст", None))
        self.groupBox.setTitle(_translate("DemogrCertificatesDialog", "Фильтр", None))
        self.chkFilterSurname.setText(_translate("DemogrCertificatesDialog", "Фамилия", None))
        self.chkFilterName.setText(_translate("DemogrCertificatesDialog", "Имя", None))
        self.chkFilterPatronymic.setText(_translate("DemogrCertificatesDialog", "Отчество", None))
        self.label.setText(_translate("DemogrCertificatesDialog", "Дата смерти с", None))
        self.label_2.setText(_translate("DemogrCertificatesDialog", "по", None))

from library.TableView import CTableView
