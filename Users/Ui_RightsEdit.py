# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Users\RightsEdit.ui'
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

class Ui_UserRightsEditDialog(object):
    def setupUi(self, UserRightsEditDialog):
        UserRightsEditDialog.setObjectName(_fromUtf8("UserRightsEditDialog"))
        UserRightsEditDialog.resize(451, 330)
        UserRightsEditDialog.setSizeGripEnabled(False)
        self.gridLayout = QtGui.QGridLayout(UserRightsEditDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtName = QtGui.QLineEdit(UserRightsEditDialog)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 0, 1, 1, 2)
        self.lblName = QtGui.QLabel(UserRightsEditDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 0, 0, 1, 1)
        self.grpFilter = QtGui.QGroupBox(UserRightsEditDialog)
        self.grpFilter.setObjectName(_fromUtf8("grpFilter"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.grpFilter)
        self.horizontalLayout.setMargin(4)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblRightFilter = QtGui.QLabel(self.grpFilter)
        self.lblRightFilter.setObjectName(_fromUtf8("lblRightFilter"))
        self.horizontalLayout.addWidget(self.lblRightFilter)
        self.cmbActivenessFilter = QtGui.QComboBox(self.grpFilter)
        self.cmbActivenessFilter.setObjectName(_fromUtf8("cmbActivenessFilter"))
        self.cmbActivenessFilter.addItem(_fromUtf8(""))
        self.cmbActivenessFilter.addItem(_fromUtf8(""))
        self.cmbActivenessFilter.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.cmbActivenessFilter)
        self.lblCodeFilter = QtGui.QLabel(self.grpFilter)
        self.lblCodeFilter.setObjectName(_fromUtf8("lblCodeFilter"))
        self.horizontalLayout.addWidget(self.lblCodeFilter)
        self.edtCodeFilter = QtGui.QLineEdit(self.grpFilter)
        self.edtCodeFilter.setObjectName(_fromUtf8("edtCodeFilter"))
        self.horizontalLayout.addWidget(self.edtCodeFilter)
        self.lblNameFilter = QtGui.QLabel(self.grpFilter)
        self.lblNameFilter.setObjectName(_fromUtf8("lblNameFilter"))
        self.horizontalLayout.addWidget(self.lblNameFilter)
        self.edtNameFilter = QtGui.QLineEdit(self.grpFilter)
        self.edtNameFilter.setObjectName(_fromUtf8("edtNameFilter"))
        self.horizontalLayout.addWidget(self.edtNameFilter)
        self.gridLayout.addWidget(self.grpFilter, 1, 0, 1, 3)
        self.tblRights = CRBCheckTableView(UserRightsEditDialog)
        self.tblRights.setObjectName(_fromUtf8("tblRights"))
        self.gridLayout.addWidget(self.tblRights, 3, 0, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(UserRightsEditDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 3)
        self.label = QtGui.QLabel(UserRightsEditDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 3)
        self.lblName.setBuddy(self.edtName)
        self.lblRightFilter.setBuddy(self.cmbActivenessFilter)

        self.retranslateUi(UserRightsEditDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), UserRightsEditDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), UserRightsEditDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(UserRightsEditDialog)
        UserRightsEditDialog.setTabOrder(self.edtName, self.cmbActivenessFilter)
        UserRightsEditDialog.setTabOrder(self.cmbActivenessFilter, self.edtCodeFilter)
        UserRightsEditDialog.setTabOrder(self.edtCodeFilter, self.edtNameFilter)
        UserRightsEditDialog.setTabOrder(self.edtNameFilter, self.tblRights)
        UserRightsEditDialog.setTabOrder(self.tblRights, self.buttonBox)

    def retranslateUi(self, UserRightsEditDialog):
        UserRightsEditDialog.setWindowTitle(_translate("UserRightsEditDialog", "Профиль прав", None))
        self.lblName.setText(_translate("UserRightsEditDialog", "&Наименование", None))
        self.grpFilter.setTitle(_translate("UserRightsEditDialog", "Фильтр прав", None))
        self.lblRightFilter.setText(_translate("UserRightsEditDialog", "&Показывать", None))
        self.cmbActivenessFilter.setItemText(0, _translate("UserRightsEditDialog", "Все", None))
        self.cmbActivenessFilter.setItemText(1, _translate("UserRightsEditDialog", "Выбранные", None))
        self.cmbActivenessFilter.setItemText(2, _translate("UserRightsEditDialog", "Не выбранные", None))
        self.lblCodeFilter.setText(_translate("UserRightsEditDialog", "Код", None))
        self.lblNameFilter.setText(_translate("UserRightsEditDialog", "Наименование", None))
        self.label.setText(_translate("UserRightsEditDialog", "Права", None))

from library.RBCheckTable import CRBCheckTableView
