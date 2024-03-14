# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\HospitalBeds\HospitalizationExecDialog.ui'
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

class Ui_HospitalizationExecDialog(object):
    def setupUi(self, HospitalizationExecDialog):
        HospitalizationExecDialog.setObjectName(_fromUtf8("HospitalizationExecDialog"))
        HospitalizationExecDialog.resize(478, 201)
        self.gridLayout = QtGui.QGridLayout(HospitalizationExecDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbPerson = CPersonComboBoxEx(HospitalizationExecDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 1, 1, 1, 4)
        self.cmbMes = CMESComboBox(HospitalizationExecDialog)
        self.cmbMes.setObjectName(_fromUtf8("cmbMes"))
        self.gridLayout.addWidget(self.cmbMes, 4, 1, 1, 4)
        self.edtExecTime = QtGui.QTimeEdit(HospitalizationExecDialog)
        self.edtExecTime.setObjectName(_fromUtf8("edtExecTime"))
        self.gridLayout.addWidget(self.edtExecTime, 0, 2, 1, 2)
        self.lblExecTimeNew = QtGui.QLabel(HospitalizationExecDialog)
        self.lblExecTimeNew.setObjectName(_fromUtf8("lblExecTimeNew"))
        self.gridLayout.addWidget(self.lblExecTimeNew, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 3, 1, 1)
        self.lblExec = QtGui.QLabel(HospitalizationExecDialog)
        self.lblExec.setObjectName(_fromUtf8("lblExec"))
        self.gridLayout.addWidget(self.lblExec, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(HospitalizationExecDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 3, 1, 2)
        self.lblMes = QtGui.QLabel(HospitalizationExecDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblMes.sizePolicy().hasHeightForWidth())
        self.lblMes.setSizePolicy(sizePolicy)
        self.lblMes.setObjectName(_fromUtf8("lblMes"))
        self.gridLayout.addWidget(self.lblMes, 4, 0, 1, 1)
        self.lblMesSpecification = QtGui.QLabel(HospitalizationExecDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblMesSpecification.sizePolicy().hasHeightForWidth())
        self.lblMesSpecification.setSizePolicy(sizePolicy)
        self.lblMesSpecification.setObjectName(_fromUtf8("lblMesSpecification"))
        self.gridLayout.addWidget(self.lblMesSpecification, 5, 0, 1, 1)
        self.cmbMesSpecification = CRBComboBox(HospitalizationExecDialog)
        self.cmbMesSpecification.setObjectName(_fromUtf8("cmbMesSpecification"))
        self.gridLayout.addWidget(self.cmbMesSpecification, 5, 1, 1, 4)
        self.cmbExec = QtGui.QComboBox(HospitalizationExecDialog)
        self.cmbExec.setObjectName(_fromUtf8("cmbExec"))
        self.gridLayout.addWidget(self.cmbExec, 2, 1, 1, 4)
        self.label = QtGui.QLabel(HospitalizationExecDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 4, 1, 1)
        self.edtExecDate = CDateEdit(HospitalizationExecDialog)
        self.edtExecDate.setCalendarPopup(True)
        self.edtExecDate.setObjectName(_fromUtf8("edtExecDate"))
        self.gridLayout.addWidget(self.edtExecDate, 0, 1, 1, 1)
        self.lblTransferTo = QtGui.QLabel(HospitalizationExecDialog)
        self.lblTransferTo.setEnabled(False)
        self.lblTransferTo.setObjectName(_fromUtf8("lblTransferTo"))
        self.gridLayout.addWidget(self.lblTransferTo, 3, 0, 1, 1)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.edtTransferTo = QtGui.QLineEdit(HospitalizationExecDialog)
        self.edtTransferTo.setEnabled(False)
        self.edtTransferTo.setObjectName(_fromUtf8("edtTransferTo"))
        self.gridLayout_3.addWidget(self.edtTransferTo, 0, 0, 1, 1)
        self.btnSelectTransferToOrganisation = QtGui.QToolButton(HospitalizationExecDialog)
        self.btnSelectTransferToOrganisation.setEnabled(False)
        self.btnSelectTransferToOrganisation.setObjectName(_fromUtf8("btnSelectTransferToOrganisation"))
        self.gridLayout_3.addWidget(self.btnSelectTransferToOrganisation, 0, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 3, 1, 1, 4)
        self.lblMes.setBuddy(self.cmbMes)
        self.lblMesSpecification.setBuddy(self.cmbMesSpecification)

        self.retranslateUi(HospitalizationExecDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), HospitalizationExecDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), HospitalizationExecDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(HospitalizationExecDialog)
        HospitalizationExecDialog.setTabOrder(self.edtExecDate, self.edtExecTime)
        HospitalizationExecDialog.setTabOrder(self.edtExecTime, self.cmbPerson)
        HospitalizationExecDialog.setTabOrder(self.cmbPerson, self.cmbExec)
        HospitalizationExecDialog.setTabOrder(self.cmbExec, self.cmbMes)
        HospitalizationExecDialog.setTabOrder(self.cmbMes, self.cmbMesSpecification)
        HospitalizationExecDialog.setTabOrder(self.cmbMesSpecification, self.buttonBox)

    def retranslateUi(self, HospitalizationExecDialog):
        HospitalizationExecDialog.setWindowTitle(_translate("HospitalizationExecDialog", "Выписка", None))
        self.lblExecTimeNew.setText(_translate("HospitalizationExecDialog", "Дата и время", None))
        self.lblExec.setText(_translate("HospitalizationExecDialog", "Исход госпитализации", None))
        self.lblMes.setText(_translate("HospitalizationExecDialog", "МЭС", None))
        self.lblMesSpecification.setText(_translate("HospitalizationExecDialog", "Результат МЭС", None))
        self.label.setText(_translate("HospitalizationExecDialog", "Исполнитель", None))
        self.lblTransferTo.setText(_translate("HospitalizationExecDialog", "Переведен в стационар", None))
        self.btnSelectTransferToOrganisation.setText(_translate("HospitalizationExecDialog", "...", None))

from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
from library.MES.MESComboBox import CMESComboBox
from library.crbcombobox import CRBComboBox
