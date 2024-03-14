# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Resources\ActionJobTicketJobTypeChangerDialog.ui'
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

class Ui_ActionJobTicketJobTypeChangerDialog(object):
    def setupUi(self, ActionJobTicketJobTypeChangerDialog):
        ActionJobTicketJobTypeChangerDialog.setObjectName(_fromUtf8("ActionJobTicketJobTypeChangerDialog"))
        ActionJobTicketJobTypeChangerDialog.resize(782, 447)
        self.verticalLayout_3 = QtGui.QVBoxLayout(ActionJobTicketJobTypeChangerDialog)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.wgtCommon = QtGui.QWidget(ActionJobTicketJobTypeChangerDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wgtCommon.sizePolicy().hasHeightForWidth())
        self.wgtCommon.setSizePolicy(sizePolicy)
        self.wgtCommon.setObjectName(_fromUtf8("wgtCommon"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.wgtCommon)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblOrgStructure = QtGui.QLabel(self.wgtCommon)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblOrgStructure.sizePolicy().hasHeightForWidth())
        self.lblOrgStructure.setSizePolicy(sizePolicy)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.horizontalLayout.addWidget(self.lblOrgStructure)
        self.cmbOrgStructure = COrgStructureComboBox(self.wgtCommon)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.horizontalLayout.addWidget(self.cmbOrgStructure)
        self.verticalLayout_3.addWidget(self.wgtCommon)
        self.splitter = QtGui.QSplitter(ActionJobTicketJobTypeChangerDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.wgtActions = QtGui.QWidget(self.splitter)
        self.wgtActions.setObjectName(_fromUtf8("wgtActions"))
        self.verticalLayout = QtGui.QVBoxLayout(self.wgtActions)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tblActions = CTableView(self.wgtActions)
        self.tblActions.setObjectName(_fromUtf8("tblActions"))
        self.verticalLayout.addWidget(self.tblActions)
        self.wgtJobTypes = QtGui.QWidget(self.splitter)
        self.wgtJobTypes.setObjectName(_fromUtf8("wgtJobTypes"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.wgtJobTypes)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tblJobTypes = CTableView(self.wgtJobTypes)
        self.tblJobTypes.setObjectName(_fromUtf8("tblJobTypes"))
        self.verticalLayout_2.addWidget(self.tblJobTypes)
        self.verticalLayout_3.addWidget(self.splitter)
        self.buttonBox = QtGui.QDialogButtonBox(ActionJobTicketJobTypeChangerDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(ActionJobTicketJobTypeChangerDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ActionJobTicketJobTypeChangerDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ActionJobTicketJobTypeChangerDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ActionJobTicketJobTypeChangerDialog)

    def retranslateUi(self, ActionJobTicketJobTypeChangerDialog):
        ActionJobTicketJobTypeChangerDialog.setWindowTitle(_translate("ActionJobTicketJobTypeChangerDialog", "Dialog", None))
        self.lblOrgStructure.setText(_translate("ActionJobTicketJobTypeChangerDialog", "Подразделение: ", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.TableView import CTableView
