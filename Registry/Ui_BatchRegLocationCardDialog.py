# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Registry\BatchRegLocationCardDialog.ui'
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

class Ui_BatchRegLocationCardDialog(object):
    def setupUi(self, BatchRegLocationCardDialog):
        BatchRegLocationCardDialog.setObjectName(_fromUtf8("BatchRegLocationCardDialog"))
        BatchRegLocationCardDialog.resize(526, 244)
        BatchRegLocationCardDialog.setSizeGripEnabled(False)
        self.gridLayout = QtGui.QGridLayout(BatchRegLocationCardDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbDocumentNumber = QtGui.QComboBox(BatchRegLocationCardDialog)
        self.cmbDocumentNumber.setObjectName(_fromUtf8("cmbDocumentNumber"))
        self.cmbDocumentNumber.addItem(_fromUtf8(""))
        self.cmbDocumentNumber.addItem(_fromUtf8(""))
        self.cmbDocumentNumber.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbDocumentNumber, 1, 1, 1, 4)
        self.cmbDocumentTypeForTracking = CRBComboBox(BatchRegLocationCardDialog)
        self.cmbDocumentTypeForTracking.setObjectName(_fromUtf8("cmbDocumentTypeForTracking"))
        self.gridLayout.addWidget(self.cmbDocumentTypeForTracking, 0, 1, 1, 4)
        self.lblDocumentTypeForTracking = QtGui.QLabel(BatchRegLocationCardDialog)
        self.lblDocumentTypeForTracking.setObjectName(_fromUtf8("lblDocumentTypeForTracking"))
        self.gridLayout.addWidget(self.lblDocumentTypeForTracking, 0, 0, 1, 1)
        self.edtNotesPage = QtGui.QTextEdit(BatchRegLocationCardDialog)
        self.edtNotesPage.setObjectName(_fromUtf8("edtNotesPage"))
        self.gridLayout.addWidget(self.edtNotesPage, 4, 1, 2, 4)
        self.lblDocumentNumber = QtGui.QLabel(BatchRegLocationCardDialog)
        self.lblDocumentNumber.setObjectName(_fromUtf8("lblDocumentNumber"))
        self.gridLayout.addWidget(self.lblDocumentNumber, 1, 0, 1, 1)
        self.lblNote = QtGui.QLabel(BatchRegLocationCardDialog)
        self.lblNote.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lblNote.setObjectName(_fromUtf8("lblNote"))
        self.gridLayout.addWidget(self.lblNote, 4, 0, 1, 1)
        self.btnStart = QtGui.QPushButton(BatchRegLocationCardDialog)
        self.btnStart.setObjectName(_fromUtf8("btnStart"))
        self.gridLayout.addWidget(self.btnStart, 6, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(326, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 6, 0, 1, 2)
        self.btnRetry = QtGui.QPushButton(BatchRegLocationCardDialog)
        self.btnRetry.setObjectName(_fromUtf8("btnRetry"))
        self.gridLayout.addWidget(self.btnRetry, 6, 3, 1, 1)
        self.cmbPerson = CPersonComboBoxEx(BatchRegLocationCardDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 3, 1, 1, 4)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 5, 0, 1, 1)
        self.lblDocumentLocation = QtGui.QLabel(BatchRegLocationCardDialog)
        self.lblDocumentLocation.setObjectName(_fromUtf8("lblDocumentLocation"))
        self.gridLayout.addWidget(self.lblDocumentLocation, 2, 0, 1, 1)
        self.btnClose = QtGui.QPushButton(BatchRegLocationCardDialog)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.gridLayout.addWidget(self.btnClose, 6, 4, 1, 1)
        self.lblPerson = QtGui.QLabel(BatchRegLocationCardDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 3, 0, 1, 1)
        self.cmbDocumentLocation = CRBComboBox(BatchRegLocationCardDialog)
        self.cmbDocumentLocation.setObjectName(_fromUtf8("cmbDocumentLocation"))
        self.gridLayout.addWidget(self.cmbDocumentLocation, 2, 1, 1, 4)
        self.lblDocumentTypeForTracking.setBuddy(self.cmbDocumentLocation)
        self.lblDocumentNumber.setBuddy(self.cmbDocumentLocation)
        self.lblNote.setBuddy(self.edtNotesPage)
        self.lblDocumentLocation.setBuddy(self.cmbDocumentLocation)
        self.lblPerson.setBuddy(self.cmbPerson)

        self.retranslateUi(BatchRegLocationCardDialog)
        QtCore.QMetaObject.connectSlotsByName(BatchRegLocationCardDialog)
        BatchRegLocationCardDialog.setTabOrder(self.cmbDocumentLocation, self.cmbPerson)
        BatchRegLocationCardDialog.setTabOrder(self.cmbPerson, self.edtNotesPage)
        BatchRegLocationCardDialog.setTabOrder(self.edtNotesPage, self.btnStart)
        BatchRegLocationCardDialog.setTabOrder(self.btnStart, self.btnRetry)
        BatchRegLocationCardDialog.setTabOrder(self.btnRetry, self.btnClose)

    def retranslateUi(self, BatchRegLocationCardDialog):
        BatchRegLocationCardDialog.setWindowTitle(_translate("BatchRegLocationCardDialog", "Место нахождения учетного документа", None))
        self.cmbDocumentNumber.setItemText(0, _translate("BatchRegLocationCardDialog", "Не заполнять", None))
        self.cmbDocumentNumber.setItemText(1, _translate("BatchRegLocationCardDialog", "Заполнять кодом пациента", None))
        self.cmbDocumentNumber.setItemText(2, _translate("BatchRegLocationCardDialog", "Заполнять номером документа события", None))
        self.lblDocumentTypeForTracking.setText(_translate("BatchRegLocationCardDialog", "Вид учетного документа", None))
        self.lblDocumentNumber.setText(_translate("BatchRegLocationCardDialog", "Номер учетного документа", None))
        self.lblNote.setText(_translate("BatchRegLocationCardDialog", "Примечание", None))
        self.btnStart.setText(_translate("BatchRegLocationCardDialog", "Начать", None))
        self.btnRetry.setText(_translate("BatchRegLocationCardDialog", "Отмена", None))
        self.lblDocumentLocation.setText(_translate("BatchRegLocationCardDialog", "Место нахождения", None))
        self.btnClose.setText(_translate("BatchRegLocationCardDialog", "Выход", None))
        self.lblPerson.setText(_translate("BatchRegLocationCardDialog", "Ответственный", None))

from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.crbcombobox import CRBComboBox
