# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PreF106.ui'
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

class Ui_PreF106Dialog(object):
    def setupUi(self, PreF106Dialog):
        PreF106Dialog.setObjectName(_fromUtf8("PreF106Dialog"))
        PreF106Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        PreF106Dialog.resize(456, 515)
        self.verticalLayout = QtGui.QVBoxLayout(PreF106Dialog)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.grpContract = QtGui.QWidget(PreF106Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grpContract.sizePolicy().hasHeightForWidth())
        self.grpContract.setSizePolicy(sizePolicy)
        self.grpContract.setObjectName(_fromUtf8("grpContract"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.grpContract)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblContract = QtGui.QLabel(self.grpContract)
        self.lblContract.setObjectName(_fromUtf8("lblContract"))
        self.horizontalLayout.addWidget(self.lblContract)
        self.cmbContract = CContractComboBox(self.grpContract)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbContract.sizePolicy().hasHeightForWidth())
        self.cmbContract.setSizePolicy(sizePolicy)
        self.cmbContract.setObjectName(_fromUtf8("cmbContract"))
        self.cmbContract.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.cmbContract)
        spacerItem = QtGui.QSpacerItem(613, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.lblSum = QtGui.QLabel(self.grpContract)
        self.lblSum.setObjectName(_fromUtf8("lblSum"))
        self.horizontalLayout.addWidget(self.lblSum)
        self.lblSumValue = QtGui.QLabel(self.grpContract)
        self.lblSumValue.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lblSumValue.setFrameShadow(QtGui.QFrame.Sunken)
        self.lblSumValue.setTextFormat(QtCore.Qt.PlainText)
        self.lblSumValue.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblSumValue.setObjectName(_fromUtf8("lblSumValue"))
        self.horizontalLayout.addWidget(self.lblSumValue)
        self.verticalLayout.addWidget(self.grpContract)
        self.splitter = QtGui.QSplitter(PreF106Dialog)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.grpActions = QtGui.QGroupBox(self.splitter)
        self.grpActions.setObjectName(_fromUtf8("grpActions"))
        self.gridLayout_2 = QtGui.QGridLayout(self.grpActions)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tblActions = CInDocTableView(self.grpActions)
        self.tblActions.setObjectName(_fromUtf8("tblActions"))
        self.gridLayout_2.addWidget(self.tblActions, 0, 0, 1, 4)
        self.btnSelectActions = QtGui.QPushButton(self.grpActions)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSelectActions.sizePolicy().hasHeightForWidth())
        self.btnSelectActions.setSizePolicy(sizePolicy)
        self.btnSelectActions.setMinimumSize(QtCore.QSize(100, 0))
        self.btnSelectActions.setAutoDefault(False)
        self.btnSelectActions.setObjectName(_fromUtf8("btnSelectActions"))
        self.gridLayout_2.addWidget(self.btnSelectActions, 1, 0, 1, 1)
        self.btnDeselectActions = QtGui.QPushButton(self.grpActions)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnDeselectActions.sizePolicy().hasHeightForWidth())
        self.btnDeselectActions.setSizePolicy(sizePolicy)
        self.btnDeselectActions.setMinimumSize(QtCore.QSize(100, 0))
        self.btnDeselectActions.setAutoDefault(False)
        self.btnDeselectActions.setObjectName(_fromUtf8("btnDeselectActions"))
        self.gridLayout_2.addWidget(self.btnDeselectActions, 1, 1, 1, 1)
        self.btnAddActionTypes = QtGui.QPushButton(self.grpActions)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAddActionTypes.sizePolicy().hasHeightForWidth())
        self.btnAddActionTypes.setSizePolicy(sizePolicy)
        self.btnAddActionTypes.setMinimumSize(QtCore.QSize(100, 0))
        self.btnAddActionTypes.setObjectName(_fromUtf8("btnAddActionTypes"))
        self.gridLayout_2.addWidget(self.btnAddActionTypes, 1, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(343, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 1, 3, 1, 1)
        self.verticalLayout.addWidget(self.splitter)
        self.buttonBox = QtGui.QDialogButtonBox(PreF106Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(PreF106Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PreF106Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PreF106Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PreF106Dialog)
        PreF106Dialog.setTabOrder(self.cmbContract, self.tblActions)
        PreF106Dialog.setTabOrder(self.tblActions, self.btnSelectActions)
        PreF106Dialog.setTabOrder(self.btnSelectActions, self.btnDeselectActions)
        PreF106Dialog.setTabOrder(self.btnDeselectActions, self.btnAddActionTypes)
        PreF106Dialog.setTabOrder(self.btnAddActionTypes, self.buttonBox)

    def retranslateUi(self, PreF106Dialog):
        PreF106Dialog.setWindowTitle(_translate("PreF106Dialog", "Dialog", None))
        self.lblContract.setText(_translate("PreF106Dialog", "Договор", None))
        self.cmbContract.setWhatsThis(_translate("PreF106Dialog", "номер, дата и основание договора в рамках которого производится осмотр", None))
        self.cmbContract.setItemText(0, _translate("PreF106Dialog", "Договор", None))
        self.lblSum.setText(_translate("PreF106Dialog", "Сумма:", None))
        self.lblSumValue.setText(_translate("PreF106Dialog", "0.00", None))
        self.grpActions.setTitle(_translate("PreF106Dialog", "Мероприятия", None))
        self.btnSelectActions.setText(_translate("PreF106Dialog", "Выбрать всё", None))
        self.btnDeselectActions.setText(_translate("PreF106Dialog", "Очистить выбор", None))
        self.btnAddActionTypes.setText(_translate("PreF106Dialog", "Добавить", None))

from Orgs.OrgComboBox import CContractComboBox
from library.InDocTable import CInDocTableView
