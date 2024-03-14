# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Timeline\ScheduleItemsDialog.ui'
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

class Ui_ScheduleItemsDialog(object):
    def setupUi(self, ScheduleItemsDialog):
        ScheduleItemsDialog.setObjectName(_fromUtf8("ScheduleItemsDialog"))
        ScheduleItemsDialog.resize(532, 456)
        self.verticalLayout_5 = QtGui.QVBoxLayout(ScheduleItemsDialog)
        self.verticalLayout_5.setMargin(4)
        self.verticalLayout_5.setSpacing(4)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.splitter_2 = QtGui.QSplitter(ScheduleItemsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter_2.sizePolicy().hasHeightForWidth())
        self.splitter_2.setSizePolicy(sizePolicy)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setChildrenCollapsible(False)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.grpScheduleItems = QtGui.QGroupBox(self.splitter_2)
        self.grpScheduleItems.setObjectName(_fromUtf8("grpScheduleItems"))
        self.verticalLayout = QtGui.QVBoxLayout(self.grpScheduleItems)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tblScheduleItems = CTableView(self.grpScheduleItems)
        self.tblScheduleItems.setObjectName(_fromUtf8("tblScheduleItems"))
        self.verticalLayout.addWidget(self.tblScheduleItems)
        self.splitter = QtGui.QSplitter(self.splitter_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.grpOrgStructureGaps = QtGui.QGroupBox(self.splitter)
        self.grpOrgStructureGaps.setObjectName(_fromUtf8("grpOrgStructureGaps"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.grpOrgStructureGaps)
        self.verticalLayout_3.setMargin(4)
        self.verticalLayout_3.setSpacing(4)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.tblOrgStructureGaps = CTableView(self.grpOrgStructureGaps)
        self.tblOrgStructureGaps.setObjectName(_fromUtf8("tblOrgStructureGaps"))
        self.verticalLayout_3.addWidget(self.tblOrgStructureGaps)
        self.grpPersonGaps = QtGui.QGroupBox(self.splitter)
        self.grpPersonGaps.setObjectName(_fromUtf8("grpPersonGaps"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.grpPersonGaps)
        self.verticalLayout_4.setMargin(4)
        self.verticalLayout_4.setSpacing(4)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.tblPersonGaps = CTableView(self.grpPersonGaps)
        self.tblPersonGaps.setObjectName(_fromUtf8("tblPersonGaps"))
        self.verticalLayout_4.addWidget(self.tblPersonGaps)
        self.verticalLayout_5.addWidget(self.splitter_2)
        self.buttonBox = QtGui.QDialogButtonBox(ScheduleItemsDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_5.addWidget(self.buttonBox)

        self.retranslateUi(ScheduleItemsDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ScheduleItemsDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ScheduleItemsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ScheduleItemsDialog)
        ScheduleItemsDialog.setTabOrder(self.tblScheduleItems, self.tblOrgStructureGaps)
        ScheduleItemsDialog.setTabOrder(self.tblOrgStructureGaps, self.tblPersonGaps)
        ScheduleItemsDialog.setTabOrder(self.tblPersonGaps, self.buttonBox)

    def retranslateUi(self, ScheduleItemsDialog):
        ScheduleItemsDialog.setWindowTitle(_translate("ScheduleItemsDialog", "Номерки", None))
        self.grpScheduleItems.setTitle(_translate("ScheduleItemsDialog", "Амбулаторный прием", None))
        self.grpOrgStructureGaps.setTitle(_translate("ScheduleItemsDialog", "Перерывы подразделения", None))
        self.grpPersonGaps.setTitle(_translate("ScheduleItemsDialog", "Перерывы сотрудника", None))

from library.TableView import CTableView
