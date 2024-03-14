# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ReportMedicalServiceExportSetup.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
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

class Ui_ReportMedicalServiceExportSetup(object):
    def setupUi(self, ReportMedicalServiceExportSetup):
        ReportMedicalServiceExportSetup.setObjectName(_fromUtf8("ReportMedicalServiceExportSetup"))
        ReportMedicalServiceExportSetup.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(ReportMedicalServiceExportSetup)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbEventType = CRBComboBox(ReportMedicalServiceExportSetup)
        self.cmbEventType.setObjectName(_fromUtf8("cmbEventType"))
        self.gridLayout.addWidget(self.cmbEventType, 3, 1, 1, 1)
        self.lblEventPurpose = QtGui.QLabel(ReportMedicalServiceExportSetup)
        self.lblEventPurpose.setObjectName(_fromUtf8("lblEventPurpose"))
        self.gridLayout.addWidget(self.lblEventPurpose, 2, 0, 1, 1)
        self.lblBegDate = QtGui.QLabel(ReportMedicalServiceExportSetup)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.lblEventType = QtGui.QLabel(ReportMedicalServiceExportSetup)
        self.lblEventType.setObjectName(_fromUtf8("lblEventType"))
        self.gridLayout.addWidget(self.lblEventType, 3, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 0, 1, 2)
        self.cmbEventPurpose = CRBComboBox(ReportMedicalServiceExportSetup)
        self.cmbEventPurpose.setObjectName(_fromUtf8("cmbEventPurpose"))
        self.gridLayout.addWidget(self.cmbEventPurpose, 2, 1, 1, 1)
        self.edtEndDate = CDateEdit(ReportMedicalServiceExportSetup)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        self.lblEndDate = QtGui.QLabel(ReportMedicalServiceExportSetup)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.edtBegDate = CDateEdit(ReportMedicalServiceExportSetup)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ReportMedicalServiceExportSetup)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 7, 0, 1, 2)
        self.lblFinance = QtGui.QLabel(ReportMedicalServiceExportSetup)
        self.lblFinance.setObjectName(_fromUtf8("lblFinance"))
        self.gridLayout.addWidget(self.lblFinance, 4, 0, 1, 1)
        self.cmbFinance = CRBComboBox(ReportMedicalServiceExportSetup)
        self.cmbFinance.setObjectName(_fromUtf8("cmbFinance"))
        self.gridLayout.addWidget(self.cmbFinance, 4, 1, 1, 1)
        self.lblConsider = QtGui.QLabel(ReportMedicalServiceExportSetup)
        self.lblConsider.setObjectName(_fromUtf8("lblConsider"))
        self.gridLayout.addWidget(self.lblConsider, 5, 0, 1, 1)
        self.cmbConsider = QtGui.QComboBox(ReportMedicalServiceExportSetup)
        self.cmbConsider.setObjectName(_fromUtf8("cmbConsider"))
        self.cmbConsider.addItem(_fromUtf8(""))
        self.cmbConsider.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbConsider, 5, 1, 1, 1)

        self.retranslateUi(ReportMedicalServiceExportSetup)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportMedicalServiceExportSetup.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportMedicalServiceExportSetup.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportMedicalServiceExportSetup)

    def retranslateUi(self, ReportMedicalServiceExportSetup):
        self.lblEventPurpose.setText(_translate("ReportMedicalServiceExportSetup", "Назначение события", None))
        self.lblBegDate.setText(_translate("ReportMedicalServiceExportSetup", "Дата начала открытия события", None))
        self.lblEventType.setText(_translate("ReportMedicalServiceExportSetup", "Тип события", None))
        self.lblEndDate.setText(_translate("ReportMedicalServiceExportSetup", "Дата окончания закрытия события", None))
        self.lblFinance.setText(_translate("ReportMedicalServiceExportSetup", "Тип финансирования", None))
        self.lblConsider.setText(_translate("ReportMedicalServiceExportSetup", "Считать", None))
        self.cmbConsider.setItemText(0, _translate("ReportMedicalServiceExportSetup", "визиты", None))
        self.cmbConsider.setItemText(1, _translate("ReportMedicalServiceExportSetup", "услуги", None))

from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ReportMedicalServiceExportSetup = QtGui.QDialog()
    ui = Ui_ReportMedicalServiceExportSetup()
    ui.setupUi(ReportMedicalServiceExportSetup)
    ReportMedicalServiceExportSetup.show()
    sys.exit(app.exec_())

