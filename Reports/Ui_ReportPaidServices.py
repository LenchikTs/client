# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\projects\samson\UP_s11\client_test\Reports\ReportPaidServices.ui'
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

class Ui_ReportPaidServicesDialog(object):
    def setupUi(self, ReportPaidServicesDialog):
        ReportPaidServicesDialog.setObjectName(_fromUtf8("ReportPaidServicesDialog"))
        ReportPaidServicesDialog.resize(522, 493)
        self.gridLayout = QtGui.QGridLayout(ReportPaidServicesDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.widget = QtGui.QWidget(ReportPaidServicesDialog)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.edtBegDate = CDateEdit(self.widget)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.horizontalLayout.addWidget(self.edtBegDate)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.edtEndDate = CDateEdit(self.widget)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.horizontalLayout.addWidget(self.edtEndDate)
        self.gridLayout.addWidget(self.widget, 0, 2, 1, 1)
        self.widget_2 = QtGui.QWidget(ReportPaidServicesDialog)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget_2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.rbPayment = QtGui.QRadioButton(self.widget_2)
        self.rbPayment.setChecked(True)
        self.rbPayment.setObjectName(_fromUtf8("rbPayment"))
        self.verticalLayout.addWidget(self.rbPayment)
        self.rbPatient = QtGui.QRadioButton(self.widget_2)
        self.rbPatient.setObjectName(_fromUtf8("rbPatient"))
        self.verticalLayout.addWidget(self.rbPatient)
        self.rbPerson = QtGui.QRadioButton(self.widget_2)
        self.rbPerson.setObjectName(_fromUtf8("rbPerson"))
        self.verticalLayout.addWidget(self.rbPerson)
        self.rbService = QtGui.QRadioButton(self.widget_2)
        self.rbService.setObjectName(_fromUtf8("rbService"))
        self.verticalLayout.addWidget(self.rbService)
        self.gridLayout.addWidget(self.widget_2, 6, 2, 1, 1)
        self.cmbService = CRBServiceComboBox(ReportPaidServicesDialog)
        self.cmbService.setObjectName(_fromUtf8("cmbService"))
        self.gridLayout.addWidget(self.cmbService, 5, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ReportPaidServicesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 9, 0, 1, 3)
        self.cmbTypePayment = QtGui.QComboBox(ReportPaidServicesDialog)
        self.cmbTypePayment.setObjectName(_fromUtf8("cmbTypePayment"))
        self.cmbTypePayment.addItem(_fromUtf8(""))
        self.cmbTypePayment.addItem(_fromUtf8(""))
        self.cmbTypePayment.addItem(_fromUtf8(""))
        self.cmbTypePayment.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbTypePayment, 2, 2, 1, 1)
        self.lblDate = QtGui.QLabel(ReportPaidServicesDialog)
        self.lblDate.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lblDate.setObjectName(_fromUtf8("lblDate"))
        self.gridLayout.addWidget(self.lblDate, 0, 0, 1, 1)
        self.cmbPatient = CClientComboBox(ReportPaidServicesDialog)
        self.cmbPatient.setObjectName(_fromUtf8("cmbPatient"))
        self.gridLayout.addWidget(self.cmbPatient, 4, 2, 1, 1)
        self.lblTypePayment = QtGui.QLabel(ReportPaidServicesDialog)
        self.lblTypePayment.setObjectName(_fromUtf8("lblTypePayment"))
        self.gridLayout.addWidget(self.lblTypePayment, 2, 0, 1, 1)
        self.lblService = QtGui.QLabel(ReportPaidServicesDialog)
        self.lblService.setObjectName(_fromUtf8("lblService"))
        self.gridLayout.addWidget(self.lblService, 5, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 8, 0, 1, 1)
        self.lblPatient = QtGui.QLabel(ReportPaidServicesDialog)
        self.lblPatient.setObjectName(_fromUtf8("lblPatient"))
        self.gridLayout.addWidget(self.lblPatient, 4, 0, 1, 1)
        self.lblEventType = QtGui.QLabel(ReportPaidServicesDialog)
        self.lblEventType.setObjectName(_fromUtf8("lblEventType"))
        self.gridLayout.addWidget(self.lblEventType, 1, 0, 1, 1)
        self.cmbEventType = CRBMultivalueComboBox(ReportPaidServicesDialog)
        self.cmbEventType.setObjectName(_fromUtf8("cmbEventType"))
        self.gridLayout.addWidget(self.cmbEventType, 1, 2, 1, 1)
        self.lblLab = QtGui.QLabel(ReportPaidServicesDialog)
        self.lblLab.setObjectName(_fromUtf8("lblLab"))
        self.gridLayout.addWidget(self.lblLab, 3, 0, 1, 1)
        self.lblGroupBy = QtGui.QLabel(ReportPaidServicesDialog)
        self.lblGroupBy.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lblGroupBy.setObjectName(_fromUtf8("lblGroupBy"))
        self.gridLayout.addWidget(self.lblGroupBy, 6, 0, 1, 1)
        self.lblCustomDateTime = QtGui.QLabel(ReportPaidServicesDialog)
        self.lblCustomDateTime.setObjectName(_fromUtf8("lblCustomDateTime"))
        self.gridLayout.addWidget(self.lblCustomDateTime, 7, 0, 1, 1)
        self.edtCustomDate = QtGui.QDateEdit(ReportPaidServicesDialog)
        self.edtCustomDate.setObjectName(_fromUtf8("edtCustomDate"))
        self.gridLayout.addWidget(self.edtCustomDate, 7, 1, 1, 1)
        self.edtCustomTime = QtGui.QTimeEdit(ReportPaidServicesDialog)
        self.edtCustomTime.setObjectName(_fromUtf8("edtCustomTime"))
        self.gridLayout.addWidget(self.edtCustomTime, 7, 2, 1, 1)
        self.cmbPerson = CPersonComboBoxEx(ReportPaidServicesDialog)
        self.cmbPerson.setEnabled(True)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 3, 2, 1, 1)
        self.lblDate.setBuddy(self.edtBegDate)

        self.retranslateUi(ReportPaidServicesDialog)
        self.cmbTypePayment.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportPaidServicesDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportPaidServicesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportPaidServicesDialog)

    def retranslateUi(self, ReportPaidServicesDialog):
        ReportPaidServicesDialog.setWindowTitle(_translate("ReportPaidServicesDialog", "параметры отчёта", None))
        self.label.setText(_translate("ReportPaidServicesDialog", "с:", None))
        self.label_2.setText(_translate("ReportPaidServicesDialog", "по:", None))
        self.rbPayment.setText(_translate("ReportPaidServicesDialog", "Тип оплаты", None))
        self.rbPatient.setText(_translate("ReportPaidServicesDialog", "Пациентам", None))
        self.rbPerson.setText(_translate("ReportPaidServicesDialog", "Исполнителю", None))
        self.rbService.setText(_translate("ReportPaidServicesDialog", "Услугам", None))
        self.cmbTypePayment.setItemText(0, _translate("ReportPaidServicesDialog", "все", None))
        self.cmbTypePayment.setItemText(1, _translate("ReportPaidServicesDialog", "наличный", None))
        self.cmbTypePayment.setItemText(2, _translate("ReportPaidServicesDialog", "безналичный", None))
        self.cmbTypePayment.setItemText(3, _translate("ReportPaidServicesDialog", "по реквизитам", None))
        self.lblDate.setText(_translate("ReportPaidServicesDialog", "Дата:", None))
        self.lblTypePayment.setText(_translate("ReportPaidServicesDialog", "Тип оплаты:", None))
        self.lblService.setText(_translate("ReportPaidServicesDialog", "В разрезе услуг:", None))
        self.lblPatient.setText(_translate("ReportPaidServicesDialog", "В разрезе пациентов:", None))
        self.lblEventType.setText(_translate("ReportPaidServicesDialog", "Тип события:", None))
        self.lblLab.setText(_translate("ReportPaidServicesDialog", "По исполнителю:", None))
        self.lblGroupBy.setText(_translate("ReportPaidServicesDialog", "Группировать по:", None))
        self.lblCustomDateTime.setText(_translate("ReportPaidServicesDialog", "Отчёт составлен", None))

from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from RefBooks.Service.RBServiceComboBox import CRBServiceComboBox
from library.ClientComboBox import CClientComboBox
from library.DateEdit import CDateEdit
from library.MultivalueComboBox import CRBMultivalueComboBox
