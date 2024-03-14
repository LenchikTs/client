# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Registry\EventPrintSetupDialog.ui'
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

class Ui_EventPrintSetupDialog(object):
    def setupUi(self, EventPrintSetupDialog):
        EventPrintSetupDialog.setObjectName(_fromUtf8("EventPrintSetupDialog"))
        EventPrintSetupDialog.resize(364, 162)
        EventPrintSetupDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(EventPrintSetupDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.widget = QtGui.QWidget(EventPrintSetupDialog)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.widget)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.begDate = QtGui.QDateEdit(self.widget)
        self.begDate.setMaximumSize(QtCore.QSize(16777215, 20))
        self.begDate.setObjectName(_fromUtf8("begDate"))
        self.gridLayout_2.addWidget(self.begDate, 1, 2, 1, 1)
        self.endDate = QtGui.QDateEdit(self.widget)
        self.endDate.setObjectName(_fromUtf8("endDate"))
        self.gridLayout_2.addWidget(self.endDate, 1, 4, 1, 1)
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 1, 3, 1, 1)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 1, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.widget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 0, 1, 1, 4)
        self.gridLayout.addWidget(self.widget, 3, 0, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(EventPrintSetupDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 3)
        self.cmbOrgStructure = COrgStructureComboBox(EventPrintSetupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 1, 1, 1, 2)
        self.label = QtGui.QLabel(EventPrintSetupDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.label_3.setBuddy(self.endDate)
        self.label_2.setBuddy(self.begDate)
        self.label.setBuddy(self.cmbOrgStructure)

        self.retranslateUi(EventPrintSetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), EventPrintSetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), EventPrintSetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EventPrintSetupDialog)
        EventPrintSetupDialog.setTabOrder(self.cmbOrgStructure, self.begDate)
        EventPrintSetupDialog.setTabOrder(self.begDate, self.endDate)
        EventPrintSetupDialog.setTabOrder(self.endDate, self.buttonBox)

    def retranslateUi(self, EventPrintSetupDialog):
        EventPrintSetupDialog.setWindowTitle(_translate("EventPrintSetupDialog", "Выбор параметров отчета", None))
        self.label_3.setText(_translate("EventPrintSetupDialog", "по", None))
        self.label_2.setText(_translate("EventPrintSetupDialog", "За период с", None))
        self.label_4.setText(_translate("EventPrintSetupDialog", "Дата окончания лечения:", None))
        self.label.setText(_translate("EventPrintSetupDialog", "Подразделение:", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
