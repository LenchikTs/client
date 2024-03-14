# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/Resources/TreatmentAppointmentClientsEditor.ui'
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

class Ui_TreatmentAppointmentClientsEditor(object):
    def setupUi(self, TreatmentAppointmentClientsEditor):
        TreatmentAppointmentClientsEditor.setObjectName(_fromUtf8("TreatmentAppointmentClientsEditor"))
        TreatmentAppointmentClientsEditor.resize(558, 346)
        self.gridLayout = QtGui.QGridLayout(TreatmentAppointmentClientsEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblLastName = QtGui.QLabel(TreatmentAppointmentClientsEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblLastName.sizePolicy().hasHeightForWidth())
        self.lblLastName.setSizePolicy(sizePolicy)
        self.lblLastName.setObjectName(_fromUtf8("lblLastName"))
        self.gridLayout.addWidget(self.lblLastName, 0, 0, 1, 1)
        self.edtLastName = QtGui.QLineEdit(TreatmentAppointmentClientsEditor)
        self.edtLastName.setObjectName(_fromUtf8("edtLastName"))
        self.gridLayout.addWidget(self.edtLastName, 0, 1, 1, 6)
        self.lblFirstName = QtGui.QLabel(TreatmentAppointmentClientsEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblFirstName.sizePolicy().hasHeightForWidth())
        self.lblFirstName.setSizePolicy(sizePolicy)
        self.lblFirstName.setObjectName(_fromUtf8("lblFirstName"))
        self.gridLayout.addWidget(self.lblFirstName, 1, 0, 1, 1)
        self.edtFirstName = QtGui.QLineEdit(TreatmentAppointmentClientsEditor)
        self.edtFirstName.setObjectName(_fromUtf8("edtFirstName"))
        self.gridLayout.addWidget(self.edtFirstName, 1, 1, 1, 6)
        self.lblPatrName = QtGui.QLabel(TreatmentAppointmentClientsEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblPatrName.sizePolicy().hasHeightForWidth())
        self.lblPatrName.setSizePolicy(sizePolicy)
        self.lblPatrName.setObjectName(_fromUtf8("lblPatrName"))
        self.gridLayout.addWidget(self.lblPatrName, 2, 0, 1, 1)
        self.edtPatrName = QtGui.QLineEdit(TreatmentAppointmentClientsEditor)
        self.edtPatrName.setObjectName(_fromUtf8("edtPatrName"))
        self.gridLayout.addWidget(self.edtPatrName, 2, 1, 1, 6)
        self.lblBirthDate = QtGui.QLabel(TreatmentAppointmentClientsEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblBirthDate.sizePolicy().hasHeightForWidth())
        self.lblBirthDate.setSizePolicy(sizePolicy)
        self.lblBirthDate.setObjectName(_fromUtf8("lblBirthDate"))
        self.gridLayout.addWidget(self.lblBirthDate, 4, 0, 1, 1)
        self.edtBirthDate = CDateEdit(TreatmentAppointmentClientsEditor)
        self.edtBirthDate.setCalendarPopup(True)
        self.edtBirthDate.setObjectName(_fromUtf8("edtBirthDate"))
        self.gridLayout.addWidget(self.edtBirthDate, 4, 1, 1, 1)
        self.lblSex = QtGui.QLabel(TreatmentAppointmentClientsEditor)
        self.lblSex.setObjectName(_fromUtf8("lblSex"))
        self.gridLayout.addWidget(self.lblSex, 4, 2, 1, 1)
        self.cmbSex = QtGui.QComboBox(TreatmentAppointmentClientsEditor)
        self.cmbSex.setObjectName(_fromUtf8("cmbSex"))
        self.cmbSex.addItem(_fromUtf8(""))
        self.cmbSex.addItem(_fromUtf8(""))
        self.cmbSex.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbSex, 4, 3, 1, 1)
        self.tblTreatmentClientList = CTableView(TreatmentAppointmentClientsEditor)
        self.tblTreatmentClientList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblTreatmentClientList.setObjectName(_fromUtf8("tblTreatmentClientList"))
        self.gridLayout.addWidget(self.tblTreatmentClientList, 5, 0, 1, 7)
        self.buttonBox = QtGui.QDialogButtonBox(TreatmentAppointmentClientsEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 7)
        self.buttonBoxFilter = QtGui.QDialogButtonBox(TreatmentAppointmentClientsEditor)
        self.buttonBoxFilter.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Reset)
        self.buttonBoxFilter.setObjectName(_fromUtf8("buttonBoxFilter"))
        self.gridLayout.addWidget(self.buttonBoxFilter, 4, 5, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 4, 4, 1, 1)
        self.lblLastName.setBuddy(self.edtLastName)
        self.lblFirstName.setBuddy(self.edtFirstName)
        self.lblPatrName.setBuddy(self.edtPatrName)
        self.lblBirthDate.setBuddy(self.edtBirthDate)

        self.retranslateUi(TreatmentAppointmentClientsEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TreatmentAppointmentClientsEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TreatmentAppointmentClientsEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(TreatmentAppointmentClientsEditor)
        TreatmentAppointmentClientsEditor.setTabOrder(self.edtLastName, self.edtFirstName)
        TreatmentAppointmentClientsEditor.setTabOrder(self.edtFirstName, self.edtPatrName)
        TreatmentAppointmentClientsEditor.setTabOrder(self.edtPatrName, self.edtBirthDate)
        TreatmentAppointmentClientsEditor.setTabOrder(self.edtBirthDate, self.cmbSex)
        TreatmentAppointmentClientsEditor.setTabOrder(self.cmbSex, self.buttonBoxFilter)
        TreatmentAppointmentClientsEditor.setTabOrder(self.buttonBoxFilter, self.tblTreatmentClientList)
        TreatmentAppointmentClientsEditor.setTabOrder(self.tblTreatmentClientList, self.buttonBox)

    def retranslateUi(self, TreatmentAppointmentClientsEditor):
        TreatmentAppointmentClientsEditor.setWindowTitle(_translate("TreatmentAppointmentClientsEditor", "Dialog", None))
        self.lblLastName.setText(_translate("TreatmentAppointmentClientsEditor", "Фамилия", None))
        self.lblFirstName.setText(_translate("TreatmentAppointmentClientsEditor", "Имя", None))
        self.lblPatrName.setText(_translate("TreatmentAppointmentClientsEditor", "Отчество", None))
        self.lblBirthDate.setText(_translate("TreatmentAppointmentClientsEditor", "Дата рождения", None))
        self.edtBirthDate.setDisplayFormat(_translate("TreatmentAppointmentClientsEditor", "dd.MM.yyyy", None))
        self.lblSex.setText(_translate("TreatmentAppointmentClientsEditor", "Пол", None))
        self.cmbSex.setItemText(0, _translate("TreatmentAppointmentClientsEditor", "Не задано", None))
        self.cmbSex.setItemText(1, _translate("TreatmentAppointmentClientsEditor", "Мужской", None))
        self.cmbSex.setItemText(2, _translate("TreatmentAppointmentClientsEditor", "Женский", None))

from library.DateEdit import CDateEdit
from library.TableView import CTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TreatmentAppointmentClientsEditor = QtGui.QDialog()
    ui = Ui_TreatmentAppointmentClientsEditor()
    ui.setupUi(TreatmentAppointmentClientsEditor)
    TreatmentAppointmentClientsEditor.show()
    sys.exit(app.exec_())

