# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\samson\HospitalBeds\ReportF001Setup.ui'
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

class Ui_ReportF001SetupDialog(object):
    def setupUi(self, ReportF001SetupDialog):
        ReportF001SetupDialog.setObjectName(_fromUtf8("ReportF001SetupDialog"))
        ReportF001SetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ReportF001SetupDialog.resize(595, 87)
        ReportF001SetupDialog.setSizeGripEnabled(True)
        self.gridlayout = QtGui.QGridLayout(ReportF001SetupDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        spacerItem = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 4, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ReportF001SetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 5, 0, 1, 2)
        self.cmbCondSort = QtGui.QComboBox(ReportF001SetupDialog)
        self.cmbCondSort.setObjectName(_fromUtf8("cmbCondSort"))
        self.cmbCondSort.addItem(_fromUtf8(""))
        self.cmbCondSort.addItem(_fromUtf8(""))
        self.cmbCondSort.addItem(_fromUtf8(""))
        self.gridlayout.addWidget(self.cmbCondSort, 0, 1, 1, 1)
        self.lblCondOrgStructure = QtGui.QLabel(ReportF001SetupDialog)
        self.lblCondOrgStructure.setObjectName(_fromUtf8("lblCondOrgStructure"))
        self.gridlayout.addWidget(self.lblCondOrgStructure, 1, 0, 1, 1)
        self.lblCondSort = QtGui.QLabel(ReportF001SetupDialog)
        self.lblCondSort.setObjectName(_fromUtf8("lblCondSort"))
        self.gridlayout.addWidget(self.lblCondSort, 0, 0, 1, 1)
        self.cmbCondOrgStructure = QtGui.QComboBox(ReportF001SetupDialog)
        self.cmbCondOrgStructure.setObjectName(_fromUtf8("cmbCondOrgStructure"))
        self.cmbCondOrgStructure.addItem(_fromUtf8(""))
        self.cmbCondOrgStructure.addItem(_fromUtf8(""))
        self.gridlayout.addWidget(self.cmbCondOrgStructure, 1, 1, 1, 1)

        self.retranslateUi(ReportF001SetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportF001SetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportF001SetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportF001SetupDialog)
        ReportF001SetupDialog.setTabOrder(self.buttonBox, self.cmbCondSort)
        ReportF001SetupDialog.setTabOrder(self.cmbCondSort, self.cmbCondOrgStructure)

    def retranslateUi(self, ReportF001SetupDialog):
        ReportF001SetupDialog.setWindowTitle(_translate("ReportF001SetupDialog", "параметры отчёта", None))
        self.cmbCondSort.setItemText(0, _translate("ReportF001SetupDialog", "по ФИО", None))
        self.cmbCondSort.setItemText(1, _translate("ReportF001SetupDialog", "по дате и времени поступления", None))
        self.cmbCondSort.setItemText(2, _translate("ReportF001SetupDialog", "по номеру документа", None))
        self.lblCondOrgStructure.setText(_translate("ReportF001SetupDialog", "Графа \"Отделение\"", None))
        self.lblCondSort.setText(_translate("ReportF001SetupDialog", "Сортировка отчета", None))
        self.cmbCondOrgStructure.setItemText(0, _translate("ReportF001SetupDialog", "название подразделения", None))
        self.cmbCondOrgStructure.setItemText(1, _translate("ReportF001SetupDialog", "код подразделения", None))

