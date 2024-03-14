# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/Resources/TreatmentControlDialog.ui'
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

class Ui_TreatmentControlDialog(object):
    def setupUi(self, TreatmentControlDialog):
        TreatmentControlDialog.setObjectName(_fromUtf8("TreatmentControlDialog"))
        TreatmentControlDialog.resize(622, 300)
        self.gridLayout = QtGui.QGridLayout(TreatmentControlDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btnGenerate = QtGui.QPushButton(TreatmentControlDialog)
        self.btnGenerate.setObjectName(_fromUtf8("btnGenerate"))
        self.gridLayout.addWidget(self.btnGenerate, 0, 2, 1, 1)
        self.edtScheduleDate = CDateEdit(TreatmentControlDialog)
        self.edtScheduleDate.setCalendarPopup(True)
        self.edtScheduleDate.setObjectName(_fromUtf8("edtScheduleDate"))
        self.gridLayout.addWidget(self.edtScheduleDate, 0, 1, 1, 1)
        self.lblPeriod = QtGui.QLabel(TreatmentControlDialog)
        self.lblPeriod.setObjectName(_fromUtf8("lblPeriod"))
        self.gridLayout.addWidget(self.lblPeriod, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.tblTreatmentControl = CTreatmentSchemeInDocTableView(TreatmentControlDialog)
        self.tblTreatmentControl.setObjectName(_fromUtf8("tblTreatmentControl"))
        self.gridLayout.addWidget(self.tblTreatmentControl, 1, 0, 1, 4)
        self.buttonBox = QtGui.QDialogButtonBox(TreatmentControlDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 4)

        self.retranslateUi(TreatmentControlDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TreatmentControlDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TreatmentControlDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TreatmentControlDialog)

    def retranslateUi(self, TreatmentControlDialog):
        TreatmentControlDialog.setWindowTitle(_translate("TreatmentControlDialog", "Dialog", None))
        self.btnGenerate.setText(_translate("TreatmentControlDialog", "Сгенерировать", None))
        self.edtScheduleDate.setDisplayFormat(_translate("TreatmentControlDialog", "dd.MM.yyyy", None))
        self.lblPeriod.setText(_translate("TreatmentControlDialog", "Дата", None))

from Resources.TreatmentSchemeInDocTableView import CTreatmentSchemeInDocTableView
from library.DateEdit import CDateEdit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TreatmentControlDialog = QtGui.QDialog()
    ui = Ui_TreatmentControlDialog()
    ui.setupUi(TreatmentControlDialog)
    TreatmentControlDialog.show()
    sys.exit(app.exec_())

