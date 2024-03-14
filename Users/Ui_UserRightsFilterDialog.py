# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\soc-inform\Users\UserRightsFilterDialog.ui'
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

class Ui_UserRightsFilterDialog(object):
    def setupUi(self, UserRightsFilterDialog):
        UserRightsFilterDialog.setObjectName(_fromUtf8("UserRightsFilterDialog"))
        UserRightsFilterDialog.resize(554, 369)
        UserRightsFilterDialog.setSizeGripEnabled(False)
        self.gridLayout = QtGui.QGridLayout(UserRightsFilterDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.grpFilter = QtGui.QGroupBox(UserRightsFilterDialog)
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
        self.gridLayout.addWidget(self.grpFilter, 0, 0, 1, 2)
        self.tblRights = CRBCheckTableView(UserRightsFilterDialog)
        self.tblRights.setObjectName(_fromUtf8("tblRights"))
        self.gridLayout.addWidget(self.tblRights, 2, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(UserRightsFilterDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 2)
        self.lblRights = QtGui.QLabel(UserRightsFilterDialog)
        self.lblRights.setObjectName(_fromUtf8("lblRights"))
        self.gridLayout.addWidget(self.lblRights, 1, 0, 1, 2)
        self.lblRightFilter.setBuddy(self.cmbActivenessFilter)

        self.retranslateUi(UserRightsFilterDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), UserRightsFilterDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), UserRightsFilterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(UserRightsFilterDialog)
        UserRightsFilterDialog.setTabOrder(self.cmbActivenessFilter, self.edtCodeFilter)
        UserRightsFilterDialog.setTabOrder(self.edtCodeFilter, self.edtNameFilter)
        UserRightsFilterDialog.setTabOrder(self.edtNameFilter, self.tblRights)
        UserRightsFilterDialog.setTabOrder(self.tblRights, self.buttonBox)

    def retranslateUi(self, UserRightsFilterDialog):
        UserRightsFilterDialog.setWindowTitle(_translate("UserRightsFilterDialog", "Профиль прав", None))
        self.grpFilter.setTitle(_translate("UserRightsFilterDialog", "Фильтр прав", None))
        self.lblRightFilter.setText(_translate("UserRightsFilterDialog", "&Показывать", None))
        self.cmbActivenessFilter.setItemText(0, _translate("UserRightsFilterDialog", "Все", None))
        self.cmbActivenessFilter.setItemText(1, _translate("UserRightsFilterDialog", "Выбранные", None))
        self.cmbActivenessFilter.setItemText(2, _translate("UserRightsFilterDialog", "Не выбранные", None))
        self.lblCodeFilter.setText(_translate("UserRightsFilterDialog", "Код", None))
        self.lblNameFilter.setText(_translate("UserRightsFilterDialog", "Наименование", None))
        self.lblRights.setText(_translate("UserRightsFilterDialog", "Права", None))

from library.RBCheckTable import CRBCheckTableView
