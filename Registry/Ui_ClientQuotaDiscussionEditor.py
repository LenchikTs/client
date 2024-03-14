# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Registry\ClientQuotaDiscussionEditor.ui'
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

class Ui_ClientQuotaDiscussionEditor(object):
    def setupUi(self, ClientQuotaDiscussionEditor):
        ClientQuotaDiscussionEditor.setObjectName(_fromUtf8("ClientQuotaDiscussionEditor"))
        ClientQuotaDiscussionEditor.resize(400, 304)
        self.gridLayout = QtGui.QGridLayout(ClientQuotaDiscussionEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblDateMessage = QtGui.QLabel(ClientQuotaDiscussionEditor)
        self.lblDateMessage.setObjectName(_fromUtf8("lblDateMessage"))
        self.gridLayout.addWidget(self.lblDateMessage, 0, 0, 1, 1)
        self.edtDateMessage = QtGui.QDateTimeEdit(ClientQuotaDiscussionEditor)
        self.edtDateMessage.setCalendarPopup(True)
        self.edtDateMessage.setObjectName(_fromUtf8("edtDateMessage"))
        self.gridLayout.addWidget(self.edtDateMessage, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(115, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.lblAgreementType = QtGui.QLabel(ClientQuotaDiscussionEditor)
        self.lblAgreementType.setObjectName(_fromUtf8("lblAgreementType"))
        self.gridLayout.addWidget(self.lblAgreementType, 1, 0, 1, 1)
        self.cmbAgreementType = CRBComboBox(ClientQuotaDiscussionEditor)
        self.cmbAgreementType.setObjectName(_fromUtf8("cmbAgreementType"))
        self.gridLayout.addWidget(self.cmbAgreementType, 1, 1, 1, 2)
        self.lblResponsiblePerson = QtGui.QLabel(ClientQuotaDiscussionEditor)
        self.lblResponsiblePerson.setObjectName(_fromUtf8("lblResponsiblePerson"))
        self.gridLayout.addWidget(self.lblResponsiblePerson, 2, 0, 1, 1)
        self.cmbResponsiblePerson = CRBComboBox(ClientQuotaDiscussionEditor)
        self.cmbResponsiblePerson.setObjectName(_fromUtf8("cmbResponsiblePerson"))
        self.gridLayout.addWidget(self.cmbResponsiblePerson, 2, 1, 1, 2)
        self.lblCosignatory = QtGui.QLabel(ClientQuotaDiscussionEditor)
        self.lblCosignatory.setObjectName(_fromUtf8("lblCosignatory"))
        self.gridLayout.addWidget(self.lblCosignatory, 3, 0, 1, 1)
        self.edtCosignatory = QtGui.QLineEdit(ClientQuotaDiscussionEditor)
        self.edtCosignatory.setObjectName(_fromUtf8("edtCosignatory"))
        self.gridLayout.addWidget(self.edtCosignatory, 3, 1, 1, 2)
        self.lblCosignatoryPost = QtGui.QLabel(ClientQuotaDiscussionEditor)
        self.lblCosignatoryPost.setObjectName(_fromUtf8("lblCosignatoryPost"))
        self.gridLayout.addWidget(self.lblCosignatoryPost, 4, 0, 1, 1)
        self.edtCosignatoryPost = QtGui.QLineEdit(ClientQuotaDiscussionEditor)
        self.edtCosignatoryPost.setObjectName(_fromUtf8("edtCosignatoryPost"))
        self.gridLayout.addWidget(self.edtCosignatoryPost, 4, 1, 1, 2)
        self.lblCosignatoryName = QtGui.QLabel(ClientQuotaDiscussionEditor)
        self.lblCosignatoryName.setObjectName(_fromUtf8("lblCosignatoryName"))
        self.gridLayout.addWidget(self.lblCosignatoryName, 5, 0, 1, 1)
        self.edtCosignatoryName = QtGui.QLineEdit(ClientQuotaDiscussionEditor)
        self.edtCosignatoryName.setObjectName(_fromUtf8("edtCosignatoryName"))
        self.gridLayout.addWidget(self.edtCosignatoryName, 5, 1, 1, 2)
        self.lblRemark = QtGui.QLabel(ClientQuotaDiscussionEditor)
        self.lblRemark.setObjectName(_fromUtf8("lblRemark"))
        self.gridLayout.addWidget(self.lblRemark, 6, 0, 1, 1)
        self.edtRemark = QtGui.QTextEdit(ClientQuotaDiscussionEditor)
        self.edtRemark.setObjectName(_fromUtf8("edtRemark"))
        self.gridLayout.addWidget(self.edtRemark, 6, 1, 2, 2)
        spacerItem1 = QtGui.QSpacerItem(20, 79, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 7, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ClientQuotaDiscussionEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 1, 1, 2)
        self.lblDateMessage.setBuddy(self.edtDateMessage)
        self.lblAgreementType.setBuddy(self.cmbAgreementType)
        self.lblResponsiblePerson.setBuddy(self.cmbResponsiblePerson)
        self.lblCosignatory.setBuddy(self.edtCosignatory)
        self.lblCosignatoryPost.setBuddy(self.edtCosignatoryPost)
        self.lblCosignatoryName.setBuddy(self.edtCosignatoryName)
        self.lblRemark.setBuddy(self.edtRemark)

        self.retranslateUi(ClientQuotaDiscussionEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ClientQuotaDiscussionEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ClientQuotaDiscussionEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(ClientQuotaDiscussionEditor)
        ClientQuotaDiscussionEditor.setTabOrder(self.edtDateMessage, self.cmbAgreementType)
        ClientQuotaDiscussionEditor.setTabOrder(self.cmbAgreementType, self.cmbResponsiblePerson)
        ClientQuotaDiscussionEditor.setTabOrder(self.cmbResponsiblePerson, self.edtCosignatory)
        ClientQuotaDiscussionEditor.setTabOrder(self.edtCosignatory, self.edtCosignatoryPost)
        ClientQuotaDiscussionEditor.setTabOrder(self.edtCosignatoryPost, self.edtCosignatoryName)
        ClientQuotaDiscussionEditor.setTabOrder(self.edtCosignatoryName, self.edtRemark)
        ClientQuotaDiscussionEditor.setTabOrder(self.edtRemark, self.buttonBox)

    def retranslateUi(self, ClientQuotaDiscussionEditor):
        ClientQuotaDiscussionEditor.setWindowTitle(_translate("ClientQuotaDiscussionEditor", "Dialog", None))
        self.lblDateMessage.setText(_translate("ClientQuotaDiscussionEditor", "Дата и время сообщения", None))
        self.lblAgreementType.setText(_translate("ClientQuotaDiscussionEditor", "Тип согласования", None))
        self.lblResponsiblePerson.setText(_translate("ClientQuotaDiscussionEditor", "Ответственный ЛПУ", None))
        self.lblCosignatory.setText(_translate("ClientQuotaDiscussionEditor", "Контрагент", None))
        self.lblCosignatoryPost.setText(_translate("ClientQuotaDiscussionEditor", "Должность", None))
        self.lblCosignatoryName.setText(_translate("ClientQuotaDiscussionEditor", "ФИО", None))
        self.lblRemark.setText(_translate("ClientQuotaDiscussionEditor", "Примечания", None))

from library.crbcombobox import CRBComboBox
