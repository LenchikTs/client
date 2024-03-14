# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Users\UserRightListDialog.ui'
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

class Ui_UserRightListDialog(object):
    def setupUi(self, UserRightListDialog):
        UserRightListDialog.setObjectName(_fromUtf8("UserRightListDialog"))
        UserRightListDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        UserRightListDialog.resize(689, 450)
        UserRightListDialog.setSizeGripEnabled(True)
        UserRightListDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(UserRightListDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblCodeFilter = QtGui.QLabel(UserRightListDialog)
        self.lblCodeFilter.setObjectName(_fromUtf8("lblCodeFilter"))
        self.gridLayout.addWidget(self.lblCodeFilter, 0, 0, 1, 1)
        self.statusBar = QtGui.QStatusBar(UserRightListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusBar.sizePolicy().hasHeightForWidth())
        self.statusBar.setSizePolicy(sizePolicy)
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        self.gridLayout.addWidget(self.statusBar, 3, 0, 1, 2)
        self.edtCodeFilter = QtGui.QLineEdit(UserRightListDialog)
        self.edtCodeFilter.setObjectName(_fromUtf8("edtCodeFilter"))
        self.gridLayout.addWidget(self.edtCodeFilter, 0, 1, 1, 1)
        self.lblNameFilter = QtGui.QLabel(UserRightListDialog)
        self.lblNameFilter.setObjectName(_fromUtf8("lblNameFilter"))
        self.gridLayout.addWidget(self.lblNameFilter, 0, 2, 1, 1)
        self.edtNameFilter = QtGui.QLineEdit(UserRightListDialog)
        self.edtNameFilter.setObjectName(_fromUtf8("edtNameFilter"))
        self.gridLayout.addWidget(self.edtNameFilter, 0, 3, 1, 1)
        self.tblItems = CUserRightListSortView(UserRightListDialog)
        self.tblItems.setTabKeyNavigation(False)
        self.tblItems.setAlternatingRowColors(True)
        self.tblItems.setObjectName(_fromUtf8("tblItems"))
        self.gridLayout.addWidget(self.tblItems, 1, 0, 1, 5)
        self.buttonBox = QtGui.QDialogButtonBox(UserRightListDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 2, 1, 3)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.label = QtGui.QLabel(UserRightListDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.hboxlayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.hboxlayout, 2, 0, 1, 2)

        self.retranslateUi(UserRightListDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), UserRightListDialog.close)
        QtCore.QMetaObject.connectSlotsByName(UserRightListDialog)
        UserRightListDialog.setTabOrder(self.tblItems, self.edtCodeFilter)
        UserRightListDialog.setTabOrder(self.edtCodeFilter, self.edtNameFilter)
        UserRightListDialog.setTabOrder(self.edtNameFilter, self.buttonBox)

    def retranslateUi(self, UserRightListDialog):
        UserRightListDialog.setWindowTitle(_translate("UserRightListDialog", "Список записей", None))
        self.lblCodeFilter.setText(_translate("UserRightListDialog", "Код", None))
        self.statusBar.setToolTip(_translate("UserRightListDialog", "A status bar", None))
        self.statusBar.setWhatsThis(_translate("UserRightListDialog", "A status bar.", None))
        self.lblNameFilter.setText(_translate("UserRightListDialog", "Наименование", None))
        self.tblItems.setWhatsThis(_translate("UserRightListDialog", "список записей", "ура!"))
        self.label.setText(_translate("UserRightListDialog", "всего: ", None))

from UserRightListSortView import CUserRightListSortView
