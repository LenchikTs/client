# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/Resources/TreatmentAppointmentEditor.ui'
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

class Ui_TreatmentAppointmentEditor(object):
    def setupUi(self, TreatmentAppointmentEditor):
        TreatmentAppointmentEditor.setObjectName(_fromUtf8("TreatmentAppointmentEditor"))
        TreatmentAppointmentEditor.resize(795, 470)
        self.gridLayout = QtGui.QGridLayout(TreatmentAppointmentEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblTreatmentAppointmentList = CTreatmentAppointmentTableView(TreatmentAppointmentEditor)
        self.tblTreatmentAppointmentList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblTreatmentAppointmentList.setObjectName(_fromUtf8("tblTreatmentAppointmentList"))
        self.gridLayout.addWidget(self.tblTreatmentAppointmentList, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(TreatmentAppointmentEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(TreatmentAppointmentEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TreatmentAppointmentEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TreatmentAppointmentEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(TreatmentAppointmentEditor)

    def retranslateUi(self, TreatmentAppointmentEditor):
        TreatmentAppointmentEditor.setWindowTitle(_translate("TreatmentAppointmentEditor", "Dialog", None))

from Resources.TreatmentAppointmentTableView import CTreatmentAppointmentTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TreatmentAppointmentEditor = QtGui.QDialog()
    ui = Ui_TreatmentAppointmentEditor()
    ui.setupUi(TreatmentAppointmentEditor)
    TreatmentAppointmentEditor.show()
    sys.exit(app.exec_())

