# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ExportHL7v2_5_Wizard_1.ui'
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

class Ui_ExportHL7v2_5_Wizard_1(object):
    def setupUi(self, ExportHL7v2_5_Wizard_1):
        ExportHL7v2_5_Wizard_1.setObjectName(_fromUtf8("ExportHL7v2_5_Wizard_1"))
        ExportHL7v2_5_Wizard_1.resize(436, 252)
        self.gridLayout = QtGui.QGridLayout(ExportHL7v2_5_Wizard_1)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblBegDate = QtGui.QLabel(ExportHL7v2_5_Wizard_1)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.edtBegDate = CDateEdit(ExportHL7v2_5_Wizard_1)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 2)
        spacerItem = QtGui.QSpacerItem(61, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 2)
        self.lblEndDate = QtGui.QLabel(ExportHL7v2_5_Wizard_1)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.edtEndDate = CDateEdit(ExportHL7v2_5_Wizard_1)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(61, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 2)
        self.lblEventType = QtGui.QLabel(ExportHL7v2_5_Wizard_1)
        self.lblEventType.setObjectName(_fromUtf8("lblEventType"))
        self.gridLayout.addWidget(self.lblEventType, 2, 0, 1, 1)
        self.cmbEventType = CRBComboBox(ExportHL7v2_5_Wizard_1)
        self.cmbEventType.setObjectName(_fromUtf8("cmbEventType"))
        self.gridLayout.addWidget(self.cmbEventType, 2, 1, 1, 4)
        self.chkOnlyPermanentAttach = QtGui.QCheckBox(ExportHL7v2_5_Wizard_1)
        self.chkOnlyPermanentAttach.setObjectName(_fromUtf8("chkOnlyPermanentAttach"))
        self.gridLayout.addWidget(self.chkOnlyPermanentAttach, 3, 1, 1, 4)
        self.chkOnlyPayedEvents = QtGui.QCheckBox(ExportHL7v2_5_Wizard_1)
        self.chkOnlyPayedEvents.setObjectName(_fromUtf8("chkOnlyPayedEvents"))
        self.gridLayout.addWidget(self.chkOnlyPayedEvents, 4, 1, 1, 4)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 8, 1, 1, 1)
        self.chkXML = QtGui.QCheckBox(ExportHL7v2_5_Wizard_1)
        self.chkXML.setEnabled(False)
        self.chkXML.setObjectName(_fromUtf8("chkXML"))
        self.gridLayout.addWidget(self.chkXML, 5, 1, 1, 4)
        self.cmbEncoding = QtGui.QComboBox(ExportHL7v2_5_Wizard_1)
        self.cmbEncoding.setObjectName(_fromUtf8("cmbEncoding"))
        self.cmbEncoding.addItem(_fromUtf8(""))
        self.cmbEncoding.addItem(_fromUtf8(""))
        self.cmbEncoding.addItem(_fromUtf8(""))
        self.cmbEncoding.addItem(_fromUtf8(""))
        self.cmbEncoding.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbEncoding, 6, 1, 1, 4)
        self.label = QtGui.QLabel(ExportHL7v2_5_Wizard_1)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 6, 0, 1, 1)
        self.label_2 = QtGui.QLabel(ExportHL7v2_5_Wizard_1)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 7, 0, 1, 1)
        self.cmbPersonCode = QtGui.QComboBox(ExportHL7v2_5_Wizard_1)
        self.cmbPersonCode.setObjectName(_fromUtf8("cmbPersonCode"))
        self.cmbPersonCode.addItem(_fromUtf8(""))
        self.cmbPersonCode.addItem(_fromUtf8(""))
        self.cmbPersonCode.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbPersonCode, 7, 1, 1, 4)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblEventType.setBuddy(self.cmbEventType)

        self.retranslateUi(ExportHL7v2_5_Wizard_1)
        self.cmbEncoding.setCurrentIndex(0)
        self.cmbPersonCode.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(ExportHL7v2_5_Wizard_1)
        ExportHL7v2_5_Wizard_1.setTabOrder(self.edtBegDate, self.edtEndDate)
        ExportHL7v2_5_Wizard_1.setTabOrder(self.edtEndDate, self.cmbEventType)
        ExportHL7v2_5_Wizard_1.setTabOrder(self.cmbEventType, self.chkOnlyPermanentAttach)
        ExportHL7v2_5_Wizard_1.setTabOrder(self.chkOnlyPermanentAttach, self.chkOnlyPayedEvents)

    def retranslateUi(self, ExportHL7v2_5_Wizard_1):
        ExportHL7v2_5_Wizard_1.setWindowTitle(_translate("ExportHL7v2_5_Wizard_1", "параметры отчёта", None))
        self.lblBegDate.setText(_translate("ExportHL7v2_5_Wizard_1", "Дата &начала периода", None))
        self.lblEndDate.setText(_translate("ExportHL7v2_5_Wizard_1", "Дата &окончания периода", None))
        self.lblEventType.setText(_translate("ExportHL7v2_5_Wizard_1", "&Тип обращения", None))
        self.chkOnlyPermanentAttach.setText(_translate("ExportHL7v2_5_Wizard_1", "&Прикреплённые к базовому ЛПУ", None))
        self.chkOnlyPayedEvents.setText(_translate("ExportHL7v2_5_Wizard_1", "Только опла&ченные", None))
        self.chkXML.setText(_translate("ExportHL7v2_5_Wizard_1", "Выгрузка в формате XML", None))
        self.cmbEncoding.setItemText(0, _translate("ExportHL7v2_5_Wizard_1", "utf-8", None))
        self.cmbEncoding.setItemText(1, _translate("ExportHL7v2_5_Wizard_1", "cp1251", None))
        self.cmbEncoding.setItemText(2, _translate("ExportHL7v2_5_Wizard_1", "koi8-r", None))
        self.cmbEncoding.setItemText(3, _translate("ExportHL7v2_5_Wizard_1", "cp866", None))
        self.cmbEncoding.setItemText(4, _translate("ExportHL7v2_5_Wizard_1", "koi8-u", None))
        self.label.setText(_translate("ExportHL7v2_5_Wizard_1", "Кодировка HL7 v2.5", None))
        self.label_2.setText(_translate("ExportHL7v2_5_Wizard_1", "Код врача", None))
        self.cmbPersonCode.setItemText(0, _translate("ExportHL7v2_5_Wizard_1", "локальный", None))
        self.cmbPersonCode.setItemText(1, _translate("ExportHL7v2_5_Wizard_1", "федеральный", None))
        self.cmbPersonCode.setItemText(2, _translate("ExportHL7v2_5_Wizard_1", "региональный", None))

from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox
