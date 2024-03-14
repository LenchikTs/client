# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\client\RefBooks\JobPurpose\RBJobPurposeListDialog.ui'
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

class Ui_RBJobPurposeListDialog(object):
    def setupUi(self, RBJobPurposeListDialog):
        RBJobPurposeListDialog.setObjectName(_fromUtf8("RBJobPurposeListDialog"))
        RBJobPurposeListDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        RBJobPurposeListDialog.resize(689, 450)
        RBJobPurposeListDialog.setSizeGripEnabled(True)
        RBJobPurposeListDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(RBJobPurposeListDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.label = QtGui.QLabel(RBJobPurposeListDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.hboxlayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.chkOnlyActive = QtGui.QCheckBox(RBJobPurposeListDialog)
        self.chkOnlyActive.setVisible(False)
        self.chkOnlyActive.setObjectName(_fromUtf8("chkOnlyActive"))
        self.hboxlayout.addWidget(self.chkOnlyActive)
        self.gridLayout.addLayout(self.hboxlayout, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RBJobPurposeListDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)
        self.statusBar = QtGui.QStatusBar(RBJobPurposeListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusBar.sizePolicy().hasHeightForWidth())
        self.statusBar.setSizePolicy(sizePolicy)
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        self.gridLayout.addWidget(self.statusBar, 3, 0, 1, 2)
        self.tblItems = CSortFilterProxyTableView(RBJobPurposeListDialog)
        self.tblItems.setTabKeyNavigation(False)
        self.tblItems.setAlternatingRowColors(True)
        self.tblItems.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.tblItems.setObjectName(_fromUtf8("tblItems"))
        self.gridLayout.addWidget(self.tblItems, 1, 0, 1, 2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 2)

        self.retranslateUi(RBJobPurposeListDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBJobPurposeListDialog.close)
        QtCore.QMetaObject.connectSlotsByName(RBJobPurposeListDialog)

    def retranslateUi(self, RBJobPurposeListDialog):
        RBJobPurposeListDialog.setWindowTitle(_translate("RBJobPurposeListDialog", "Назначения работы", None))
        self.label.setText(_translate("RBJobPurposeListDialog", "всего: ", None))
        self.chkOnlyActive.setText(_translate("RBJobPurposeListDialog", "Только активные", None))
        self.statusBar.setToolTip(_translate("RBJobPurposeListDialog", "A status bar", None))
        self.statusBar.setWhatsThis(_translate("RBJobPurposeListDialog", "A status bar.", None))
        self.tblItems.setWhatsThis(_translate("RBJobPurposeListDialog", "список записей", "ура!"))

from library.SortFilterProxyTableView import CSortFilterProxyTableView
