# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/Resources/TreatmentSchemeDialog.ui'
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

class Ui_TreatmentSchemeDialog(object):
    def setupUi(self, TreatmentSchemeDialog):
        TreatmentSchemeDialog.setObjectName(_fromUtf8("TreatmentSchemeDialog"))
        TreatmentSchemeDialog.resize(622, 300)
        self.gridLayout = QtGui.QGridLayout(TreatmentSchemeDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbTreatmentType = CRBComboBox(TreatmentSchemeDialog)
        self.cmbTreatmentType.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.cmbTreatmentType.setObjectName(_fromUtf8("cmbTreatmentType"))
        self.gridLayout.addWidget(self.cmbTreatmentType, 0, 5, 1, 1)
        self.btnGenerate = QtGui.QPushButton(TreatmentSchemeDialog)
        self.btnGenerate.setObjectName(_fromUtf8("btnGenerate"))
        self.gridLayout.addWidget(self.btnGenerate, 0, 6, 1, 1)
        self.edtBegDate = CDateEdit(TreatmentSchemeDialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 2, 1, 1)
        self.edtEndDate = CDateEdit(TreatmentSchemeDialog)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 0, 3, 1, 1)
        self.lblTreatmentType = QtGui.QLabel(TreatmentSchemeDialog)
        self.lblTreatmentType.setObjectName(_fromUtf8("lblTreatmentType"))
        self.gridLayout.addWidget(self.lblTreatmentType, 0, 4, 1, 1)
        self.lblPeriod = QtGui.QLabel(TreatmentSchemeDialog)
        self.lblPeriod.setObjectName(_fromUtf8("lblPeriod"))
        self.gridLayout.addWidget(self.lblPeriod, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 7, 1, 1)
        self.btnTreatmentHistory = QtGui.QPushButton(TreatmentSchemeDialog)
        self.btnTreatmentHistory.setObjectName(_fromUtf8("btnTreatmentHistory"))
        self.gridLayout.addWidget(self.btnTreatmentHistory, 0, 0, 1, 1)
        self.tblTreatmentScheme = CTreatmentSchemeInDocTableView(TreatmentSchemeDialog)
        self.tblTreatmentScheme.setObjectName(_fromUtf8("tblTreatmentScheme"))
        self.gridLayout.addWidget(self.tblTreatmentScheme, 1, 0, 1, 8)
        self.buttonBox = QtGui.QDialogButtonBox(TreatmentSchemeDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 8)

        self.retranslateUi(TreatmentSchemeDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TreatmentSchemeDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TreatmentSchemeDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TreatmentSchemeDialog)
        TreatmentSchemeDialog.setTabOrder(self.btnTreatmentHistory, self.cmbTreatmentType)
        TreatmentSchemeDialog.setTabOrder(self.cmbTreatmentType, self.btnGenerate)
        TreatmentSchemeDialog.setTabOrder(self.btnGenerate, self.edtBegDate)
        TreatmentSchemeDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        TreatmentSchemeDialog.setTabOrder(self.edtEndDate, self.tblTreatmentScheme)
        TreatmentSchemeDialog.setTabOrder(self.tblTreatmentScheme, self.buttonBox)

    def retranslateUi(self, TreatmentSchemeDialog):
        TreatmentSchemeDialog.setWindowTitle(_translate("TreatmentSchemeDialog", "Dialog", None))
        self.btnGenerate.setText(_translate("TreatmentSchemeDialog", "Сгенерировать", None))
        self.edtBegDate.setDisplayFormat(_translate("TreatmentSchemeDialog", "dd.MM.yyyy", None))
        self.edtEndDate.setDisplayFormat(_translate("TreatmentSchemeDialog", "dd.MM.yyyy", None))
        self.lblTreatmentType.setText(_translate("TreatmentSchemeDialog", "Цикл", None))
        self.lblPeriod.setText(_translate("TreatmentSchemeDialog", "Период", None))
        self.btnTreatmentHistory.setText(_translate("TreatmentSchemeDialog", "История", None))

from Resources.TreatmentSchemeInDocTableView import CTreatmentSchemeInDocTableView
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TreatmentSchemeDialog = QtGui.QDialog()
    ui = Ui_TreatmentSchemeDialog()
    ui.setupUi(TreatmentSchemeDialog)
    TreatmentSchemeDialog.show()
    sys.exit(app.exec_())

