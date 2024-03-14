# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/Resources/TreatmentScheduleDialog.ui'
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

class Ui_TreatmentScheduleDialog(object):
    def setupUi(self, TreatmentScheduleDialog):
        TreatmentScheduleDialog.setObjectName(_fromUtf8("TreatmentScheduleDialog"))
        TreatmentScheduleDialog.resize(461, 288)
        self.gridLayout = QtGui.QGridLayout(TreatmentScheduleDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblPeriod = QtGui.QLabel(TreatmentScheduleDialog)
        self.lblPeriod.setObjectName(_fromUtf8("lblPeriod"))
        self.gridLayout.addWidget(self.lblPeriod, 0, 0, 1, 1)
        self.edtBegDate = CDateEdit(TreatmentScheduleDialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.edtEndDate = CDateEdit(TreatmentScheduleDialog)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 0, 2, 1, 1)
        self.btnGenerate = QtGui.QPushButton(TreatmentScheduleDialog)
        self.btnGenerate.setObjectName(_fromUtf8("btnGenerate"))
        self.gridLayout.addWidget(self.btnGenerate, 0, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 4, 1, 1)
        self.splitter = QtGui.QSplitter(TreatmentScheduleDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.tblTreatmentSchedule = CTreatmentScheduleInDocTableView(self.splitter)
        self.tblTreatmentSchedule.setObjectName(_fromUtf8("tblTreatmentSchedule"))
        self.tblTreatmentColorType = QtGui.QTableView(self.splitter)
        self.tblTreatmentColorType.setObjectName(_fromUtf8("tblTreatmentColorType"))
        self.gridLayout.addWidget(self.splitter, 1, 0, 1, 6)
        self.buttonBox = QtGui.QDialogButtonBox(TreatmentScheduleDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 5)

        self.retranslateUi(TreatmentScheduleDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TreatmentScheduleDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TreatmentScheduleDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TreatmentScheduleDialog)
        TreatmentScheduleDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        TreatmentScheduleDialog.setTabOrder(self.edtEndDate, self.btnGenerate)

    def retranslateUi(self, TreatmentScheduleDialog):
        TreatmentScheduleDialog.setWindowTitle(_translate("TreatmentScheduleDialog", "Dialog", None))
        self.lblPeriod.setText(_translate("TreatmentScheduleDialog", "Период", None))
        self.edtBegDate.setDisplayFormat(_translate("TreatmentScheduleDialog", "dd.MM.yyyy", None))
        self.edtEndDate.setDisplayFormat(_translate("TreatmentScheduleDialog", "dd.MM.yyyy", None))
        self.btnGenerate.setText(_translate("TreatmentScheduleDialog", "Сформировать", None))

from Resources.TreatmentScheduleInDocTableView import CTreatmentScheduleInDocTableView
from library.DateEdit import CDateEdit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TreatmentScheduleDialog = QtGui.QDialog()
    ui = Ui_TreatmentScheduleDialog()
    ui.setupUi(TreatmentScheduleDialog)
    TreatmentScheduleDialog.show()
    sys.exit(app.exec_())

