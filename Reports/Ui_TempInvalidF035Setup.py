# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_vipisnoy\Reports\TempInvalidF035Setup.ui'
#
# Created: Thu Sep 24 15:27:24 2020
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_TempInvalidF035Dialog(object):
    def setupUi(self, TempInvalidF035Dialog):
        TempInvalidF035Dialog.setObjectName(_fromUtf8("TempInvalidF035Dialog"))
        TempInvalidF035Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        TempInvalidF035Dialog.resize(412, 496)
        TempInvalidF035Dialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(TempInvalidF035Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.chkFilterExpertExpertiseTypeMC = QtGui.QCheckBox(TempInvalidF035Dialog)
        self.chkFilterExpertExpertiseTypeMC.setObjectName(_fromUtf8("chkFilterExpertExpertiseTypeMC"))
        self.gridLayout.addWidget(self.chkFilterExpertExpertiseTypeMC, 0, 0, 1, 2)
        self.chkFilterExecDateMC = QtGui.QCheckBox(TempInvalidF035Dialog)
        self.chkFilterExecDateMC.setObjectName(_fromUtf8("chkFilterExecDateMC"))
        self.gridLayout.addWidget(self.chkFilterExecDateMC, 1, 0, 1, 2)
        self.horizontalLayout_17 = QtGui.QHBoxLayout()
        self.horizontalLayout_17.setObjectName(_fromUtf8("horizontalLayout_17"))
        self.edtFilterBegExecDateMC = CDateEdit(TempInvalidF035Dialog)
        self.edtFilterBegExecDateMC.setEnabled(False)
        self.edtFilterBegExecDateMC.setDisplayFormat(_fromUtf8("dd.MM.yyyy"))
        self.edtFilterBegExecDateMC.setCalendarPopup(True)
        self.edtFilterBegExecDateMC.setObjectName(_fromUtf8("edtFilterBegExecDateMC"))
        self.horizontalLayout_17.addWidget(self.edtFilterBegExecDateMC)
        self.edtFilterEndExecDateMC = CDateEdit(TempInvalidF035Dialog)
        self.edtFilterEndExecDateMC.setEnabled(False)
        self.edtFilterEndExecDateMC.setCalendarPopup(True)
        self.edtFilterEndExecDateMC.setObjectName(_fromUtf8("edtFilterEndExecDateMC"))
        self.horizontalLayout_17.addWidget(self.edtFilterEndExecDateMC)
        spacerItem = QtGui.QSpacerItem(33, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout_17, 1, 2, 1, 2)
        self.chkFilterExpertSetPersonMC = QtGui.QCheckBox(TempInvalidF035Dialog)
        self.chkFilterExpertSetPersonMC.setObjectName(_fromUtf8("chkFilterExpertSetPersonMC"))
        self.gridLayout.addWidget(self.chkFilterExpertSetPersonMC, 3, 0, 1, 2)
        self.chkFilterExpertOrgStructMC = QtGui.QCheckBox(TempInvalidF035Dialog)
        self.chkFilterExpertOrgStructMC.setObjectName(_fromUtf8("chkFilterExpertOrgStructMC"))
        self.gridLayout.addWidget(self.chkFilterExpertOrgStructMC, 4, 0, 1, 2)
        self.chkFilterExpertSpecialityMC = QtGui.QCheckBox(TempInvalidF035Dialog)
        self.chkFilterExpertSpecialityMC.setObjectName(_fromUtf8("chkFilterExpertSpecialityMC"))
        self.gridLayout.addWidget(self.chkFilterExpertSpecialityMC, 5, 0, 1, 2)
        self.chkFilterExpertClosedMC = QtGui.QCheckBox(TempInvalidF035Dialog)
        self.chkFilterExpertClosedMC.setObjectName(_fromUtf8("chkFilterExpertClosedMC"))
        self.gridLayout.addWidget(self.chkFilterExpertClosedMC, 7, 0, 1, 2)
        self.chkFilterExpertExpertiseCharacterMC = QtGui.QCheckBox(TempInvalidF035Dialog)
        self.chkFilterExpertExpertiseCharacterMC.setObjectName(_fromUtf8("chkFilterExpertExpertiseCharacterMC"))
        self.gridLayout.addWidget(self.chkFilterExpertExpertiseCharacterMC, 8, 0, 1, 2)
        self.chkFilterExpertExpertiseKindMC = QtGui.QCheckBox(TempInvalidF035Dialog)
        self.chkFilterExpertExpertiseKindMC.setObjectName(_fromUtf8("chkFilterExpertExpertiseKindMC"))
        self.gridLayout.addWidget(self.chkFilterExpertExpertiseKindMC, 9, 0, 1, 2)
        self.ghkFilterExpertExpertiseObjectMC = QtGui.QCheckBox(TempInvalidF035Dialog)
        self.ghkFilterExpertExpertiseObjectMC.setObjectName(_fromUtf8("ghkFilterExpertExpertiseObjectMC"))
        self.gridLayout.addWidget(self.ghkFilterExpertExpertiseObjectMC, 10, 0, 1, 2)
        self.chkFilterExpertExpertiseArgumentMC = QtGui.QCheckBox(TempInvalidF035Dialog)
        self.chkFilterExpertExpertiseArgumentMC.setObjectName(_fromUtf8("chkFilterExpertExpertiseArgumentMC"))
        self.gridLayout.addWidget(self.chkFilterExpertExpertiseArgumentMC, 11, 0, 1, 2)
        self.lblCntUser = QtGui.QLabel(TempInvalidF035Dialog)
        self.lblCntUser.setObjectName(_fromUtf8("lblCntUser"))
        self.gridLayout.addWidget(self.lblCntUser, 12, 0, 1, 2)
        self.edtCntUser = QtGui.QSpinBox(TempInvalidF035Dialog)
        self.edtCntUser.setMinimum(1)
        self.edtCntUser.setMaximum(999999999)
        self.edtCntUser.setObjectName(_fromUtf8("edtCntUser"))
        self.gridLayout.addWidget(self.edtCntUser, 12, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 12, 3, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 8, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 16, 1, 1, 1)
        self.cmbFilterExpertExpertiseTypeMC = CRBMultivalueComboBox(TempInvalidF035Dialog)
        self.cmbFilterExpertExpertiseTypeMC.setEnabled(False)
        self.cmbFilterExpertExpertiseTypeMC.setObjectName(_fromUtf8("cmbFilterExpertExpertiseTypeMC"))
        self.gridLayout.addWidget(self.cmbFilterExpertExpertiseTypeMC, 0, 2, 1, 2)
        self.cmbExpertIdMC = CPersonComboBoxEx(TempInvalidF035Dialog)
        self.cmbExpertIdMC.setEnabled(False)
        self.cmbExpertIdMC.setObjectName(_fromUtf8("cmbExpertIdMC"))
        self.gridLayout.addWidget(self.cmbExpertIdMC, 2, 2, 1, 2)
        self.cmbFilterExpertSetPersonMC = CPersonComboBoxEx(TempInvalidF035Dialog)
        self.cmbFilterExpertSetPersonMC.setEnabled(False)
        self.cmbFilterExpertSetPersonMC.setObjectName(_fromUtf8("cmbFilterExpertSetPersonMC"))
        self.gridLayout.addWidget(self.cmbFilterExpertSetPersonMC, 3, 2, 1, 2)
        self.cmbFilterExpertOrgStructMC = COrgStructureComboBox(TempInvalidF035Dialog)
        self.cmbFilterExpertOrgStructMC.setEnabled(False)
        self.cmbFilterExpertOrgStructMC.setObjectName(_fromUtf8("cmbFilterExpertOrgStructMC"))
        self.gridLayout.addWidget(self.cmbFilterExpertOrgStructMC, 4, 2, 1, 2)
        self.cmbFilterExpertSpecialityMC = CRBComboBox(TempInvalidF035Dialog)
        self.cmbFilterExpertSpecialityMC.setEnabled(False)
        self.cmbFilterExpertSpecialityMC.setObjectName(_fromUtf8("cmbFilterExpertSpecialityMC"))
        self.gridLayout.addWidget(self.cmbFilterExpertSpecialityMC, 5, 2, 1, 2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.edtFilterExpertBegMKBMC = CICDCodeEdit(TempInvalidF035Dialog)
        self.edtFilterExpertBegMKBMC.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtFilterExpertBegMKBMC.sizePolicy().hasHeightForWidth())
        self.edtFilterExpertBegMKBMC.setSizePolicy(sizePolicy)
        self.edtFilterExpertBegMKBMC.setMaximumSize(QtCore.QSize(40, 16777215))
        self.edtFilterExpertBegMKBMC.setMaxLength(6)
        self.edtFilterExpertBegMKBMC.setObjectName(_fromUtf8("edtFilterExpertBegMKBMC"))
        self.horizontalLayout.addWidget(self.edtFilterExpertBegMKBMC)
        self.edtFilterExpertEndMKBMC = CICDCodeEdit(TempInvalidF035Dialog)
        self.edtFilterExpertEndMKBMC.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtFilterExpertEndMKBMC.sizePolicy().hasHeightForWidth())
        self.edtFilterExpertEndMKBMC.setSizePolicy(sizePolicy)
        self.edtFilterExpertEndMKBMC.setMaximumSize(QtCore.QSize(40, 16777215))
        self.edtFilterExpertEndMKBMC.setMaxLength(6)
        self.edtFilterExpertEndMKBMC.setObjectName(_fromUtf8("edtFilterExpertEndMKBMC"))
        self.horizontalLayout.addWidget(self.edtFilterExpertEndMKBMC)
        spacerItem3 = QtGui.QSpacerItem(41, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.gridLayout.addLayout(self.horizontalLayout, 6, 2, 1, 2)
        self.cmbFilterExpertClosedMC = CActionStatusComboBox(TempInvalidF035Dialog)
        self.cmbFilterExpertClosedMC.setEnabled(False)
        self.cmbFilterExpertClosedMC.setObjectName(_fromUtf8("cmbFilterExpertClosedMC"))
        self.gridLayout.addWidget(self.cmbFilterExpertClosedMC, 7, 2, 1, 2)
        self.cmbFilterExpertExpertiseCharacterMC = CRBComboBox(TempInvalidF035Dialog)
        self.cmbFilterExpertExpertiseCharacterMC.setEnabled(False)
        self.cmbFilterExpertExpertiseCharacterMC.setObjectName(_fromUtf8("cmbFilterExpertExpertiseCharacterMC"))
        self.gridLayout.addWidget(self.cmbFilterExpertExpertiseCharacterMC, 8, 2, 1, 2)
        self.cmbFilterExpertExpertiseKindMC = CRBComboBox(TempInvalidF035Dialog)
        self.cmbFilterExpertExpertiseKindMC.setEnabled(False)
        self.cmbFilterExpertExpertiseKindMC.setObjectName(_fromUtf8("cmbFilterExpertExpertiseKindMC"))
        self.gridLayout.addWidget(self.cmbFilterExpertExpertiseKindMC, 9, 2, 1, 2)
        self.cmbFilterExpertExpertiseObjectMC = CRBComboBox(TempInvalidF035Dialog)
        self.cmbFilterExpertExpertiseObjectMC.setEnabled(False)
        self.cmbFilterExpertExpertiseObjectMC.setObjectName(_fromUtf8("cmbFilterExpertExpertiseObjectMC"))
        self.gridLayout.addWidget(self.cmbFilterExpertExpertiseObjectMC, 10, 2, 1, 2)
        self.cmbFilterExpertExpertiseArgumentMC = CRBComboBox(TempInvalidF035Dialog)
        self.cmbFilterExpertExpertiseArgumentMC.setEnabled(False)
        self.cmbFilterExpertExpertiseArgumentMC.setObjectName(_fromUtf8("cmbFilterExpertExpertiseArgumentMC"))
        self.gridLayout.addWidget(self.cmbFilterExpertExpertiseArgumentMC, 11, 2, 1, 2)
        self.chkRegAddress = QtGui.QCheckBox(TempInvalidF035Dialog)
        self.chkRegAddress.setObjectName(_fromUtf8("chkRegAddress"))
        self.gridLayout.addWidget(self.chkRegAddress, 13, 2, 1, 2)
        self.chkNumberPolicy = QtGui.QCheckBox(TempInvalidF035Dialog)
        self.chkNumberPolicy.setObjectName(_fromUtf8("chkNumberPolicy"))
        self.gridLayout.addWidget(self.chkNumberPolicy, 14, 2, 1, 2)
        self.chkClientId = QtGui.QCheckBox(TempInvalidF035Dialog)
        self.chkClientId.setObjectName(_fromUtf8("chkClientId"))
        self.gridLayout.addWidget(self.chkClientId, 15, 2, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(TempInvalidF035Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 17, 0, 1, 4)
        self.chkFilterExpertMKBMC = QtGui.QCheckBox(TempInvalidF035Dialog)
        self.chkFilterExpertMKBMC.setObjectName(_fromUtf8("chkFilterExpertMKBMC"))
        self.gridLayout.addWidget(self.chkFilterExpertMKBMC, 6, 0, 1, 2)
        self.chkExpertIdMC = QtGui.QCheckBox(TempInvalidF035Dialog)
        self.chkExpertIdMC.setObjectName(_fromUtf8("chkExpertIdMC"))
        self.gridLayout.addWidget(self.chkExpertIdMC, 2, 0, 1, 2)

        self.retranslateUi(TempInvalidF035Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TempInvalidF035Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TempInvalidF035Dialog.reject)
        QtCore.QObject.connect(self.chkFilterExpertExpertiseTypeMC, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbFilterExpertExpertiseTypeMC.setEnabled)
        QtCore.QObject.connect(self.chkFilterExecDateMC, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtFilterBegExecDateMC.setEnabled)
        QtCore.QObject.connect(self.chkFilterExecDateMC, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtFilterEndExecDateMC.setEnabled)
        QtCore.QObject.connect(self.chkExpertIdMC, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbExpertIdMC.setEnabled)
        QtCore.QObject.connect(self.chkFilterExpertSetPersonMC, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbFilterExpertSetPersonMC.setEnabled)
        QtCore.QObject.connect(self.chkFilterExpertOrgStructMC, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbFilterExpertOrgStructMC.setEnabled)
        QtCore.QObject.connect(self.chkFilterExpertSpecialityMC, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbFilterExpertSpecialityMC.setEnabled)
        QtCore.QObject.connect(self.chkFilterExpertMKBMC, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtFilterExpertBegMKBMC.setEnabled)
        QtCore.QObject.connect(self.chkFilterExpertMKBMC, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtFilterExpertEndMKBMC.setEnabled)
        QtCore.QObject.connect(self.chkFilterExpertClosedMC, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbFilterExpertClosedMC.setEnabled)
        QtCore.QObject.connect(self.chkFilterExpertExpertiseCharacterMC, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbFilterExpertExpertiseCharacterMC.setEnabled)
        QtCore.QObject.connect(self.chkFilterExpertExpertiseKindMC, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbFilterExpertExpertiseKindMC.setEnabled)
        QtCore.QObject.connect(self.ghkFilterExpertExpertiseObjectMC, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbFilterExpertExpertiseObjectMC.setEnabled)
        QtCore.QObject.connect(self.chkFilterExpertExpertiseArgumentMC, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbFilterExpertExpertiseArgumentMC.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(TempInvalidF035Dialog)
        TempInvalidF035Dialog.setTabOrder(self.chkFilterExpertExpertiseTypeMC, self.cmbFilterExpertExpertiseTypeMC)
        TempInvalidF035Dialog.setTabOrder(self.cmbFilterExpertExpertiseTypeMC, self.chkFilterExecDateMC)
        TempInvalidF035Dialog.setTabOrder(self.chkFilterExecDateMC, self.edtFilterBegExecDateMC)
        TempInvalidF035Dialog.setTabOrder(self.edtFilterBegExecDateMC, self.edtFilterEndExecDateMC)
        TempInvalidF035Dialog.setTabOrder(self.edtFilterEndExecDateMC, self.chkExpertIdMC)
        TempInvalidF035Dialog.setTabOrder(self.chkExpertIdMC, self.cmbExpertIdMC)
        TempInvalidF035Dialog.setTabOrder(self.cmbExpertIdMC, self.chkFilterExpertSetPersonMC)
        TempInvalidF035Dialog.setTabOrder(self.chkFilterExpertSetPersonMC, self.cmbFilterExpertSetPersonMC)
        TempInvalidF035Dialog.setTabOrder(self.cmbFilterExpertSetPersonMC, self.chkFilterExpertOrgStructMC)
        TempInvalidF035Dialog.setTabOrder(self.chkFilterExpertOrgStructMC, self.cmbFilterExpertOrgStructMC)
        TempInvalidF035Dialog.setTabOrder(self.cmbFilterExpertOrgStructMC, self.chkFilterExpertSpecialityMC)
        TempInvalidF035Dialog.setTabOrder(self.chkFilterExpertSpecialityMC, self.cmbFilterExpertSpecialityMC)
        TempInvalidF035Dialog.setTabOrder(self.cmbFilterExpertSpecialityMC, self.chkFilterExpertMKBMC)
        TempInvalidF035Dialog.setTabOrder(self.chkFilterExpertMKBMC, self.edtFilterExpertBegMKBMC)
        TempInvalidF035Dialog.setTabOrder(self.edtFilterExpertBegMKBMC, self.edtFilterExpertEndMKBMC)
        TempInvalidF035Dialog.setTabOrder(self.edtFilterExpertEndMKBMC, self.chkFilterExpertClosedMC)
        TempInvalidF035Dialog.setTabOrder(self.chkFilterExpertClosedMC, self.cmbFilterExpertClosedMC)
        TempInvalidF035Dialog.setTabOrder(self.cmbFilterExpertClosedMC, self.chkFilterExpertExpertiseCharacterMC)
        TempInvalidF035Dialog.setTabOrder(self.chkFilterExpertExpertiseCharacterMC, self.cmbFilterExpertExpertiseCharacterMC)
        TempInvalidF035Dialog.setTabOrder(self.cmbFilterExpertExpertiseCharacterMC, self.chkFilterExpertExpertiseKindMC)
        TempInvalidF035Dialog.setTabOrder(self.chkFilterExpertExpertiseKindMC, self.cmbFilterExpertExpertiseKindMC)
        TempInvalidF035Dialog.setTabOrder(self.cmbFilterExpertExpertiseKindMC, self.ghkFilterExpertExpertiseObjectMC)
        TempInvalidF035Dialog.setTabOrder(self.ghkFilterExpertExpertiseObjectMC, self.cmbFilterExpertExpertiseObjectMC)
        TempInvalidF035Dialog.setTabOrder(self.cmbFilterExpertExpertiseObjectMC, self.chkFilterExpertExpertiseArgumentMC)
        TempInvalidF035Dialog.setTabOrder(self.chkFilterExpertExpertiseArgumentMC, self.cmbFilterExpertExpertiseArgumentMC)
        TempInvalidF035Dialog.setTabOrder(self.cmbFilterExpertExpertiseArgumentMC, self.edtCntUser)
        TempInvalidF035Dialog.setTabOrder(self.edtCntUser, self.chkRegAddress)
        TempInvalidF035Dialog.setTabOrder(self.chkRegAddress, self.chkNumberPolicy)
        TempInvalidF035Dialog.setTabOrder(self.chkNumberPolicy, self.chkClientId)
        TempInvalidF035Dialog.setTabOrder(self.chkClientId, self.buttonBox)

    def retranslateUi(self, TempInvalidF035Dialog):
        TempInvalidF035Dialog.setWindowTitle(_translate("TempInvalidF035Dialog", "параметры отчёта", None))
        self.chkFilterExpertExpertiseTypeMC.setText(_translate("TempInvalidF035Dialog", "Тип экспертизы", None))
        self.chkFilterExecDateMC.setText(_translate("TempInvalidF035Dialog", "Период Экпертизы", None))
        self.edtFilterEndExecDateMC.setDisplayFormat(_translate("TempInvalidF035Dialog", "dd.MM.yyyy", None))
        self.chkFilterExpertSetPersonMC.setText(_translate("TempInvalidF035Dialog", "Назначивший", None))
        self.chkFilterExpertOrgStructMC.setText(_translate("TempInvalidF035Dialog", "Подразделение", None))
        self.chkFilterExpertSpecialityMC.setText(_translate("TempInvalidF035Dialog", "Специальность", None))
        self.chkFilterExpertClosedMC.setText(_translate("TempInvalidF035Dialog", "Состояние", None))
        self.chkFilterExpertExpertiseCharacterMC.setText(_translate("TempInvalidF035Dialog", "Характеристика экспертизы", None))
        self.chkFilterExpertExpertiseKindMC.setText(_translate("TempInvalidF035Dialog", "Вид экспертизы", None))
        self.ghkFilterExpertExpertiseObjectMC.setText(_translate("TempInvalidF035Dialog", "Предмет экспертизы", None))
        self.chkFilterExpertExpertiseArgumentMC.setText(_translate("TempInvalidF035Dialog", "Обоснование", None))
        self.lblCntUser.setText(_translate("TempInvalidF035Dialog", "Номер строки с", None))
        self.edtFilterExpertBegMKBMC.setInputMask(_translate("TempInvalidF035Dialog", "a00.00; ", None))
        self.edtFilterExpertBegMKBMC.setText(_translate("TempInvalidF035Dialog", "A.", None))
        self.edtFilterExpertEndMKBMC.setInputMask(_translate("TempInvalidF035Dialog", "a00.00; ", None))
        self.edtFilterExpertEndMKBMC.setText(_translate("TempInvalidF035Dialog", "Z99.9", None))
        self.chkRegAddress.setText(_translate("TempInvalidF035Dialog", "Адрес пациента", None))
        self.chkNumberPolicy.setText(_translate("TempInvalidF035Dialog", "Номер полиса", None))
        self.chkClientId.setText(_translate("TempInvalidF035Dialog", "Номер амбулаторной карты", None))
        self.chkFilterExpertMKBMC.setText(_translate("TempInvalidF035Dialog", "Диагноз", None))
        self.chkExpertIdMC.setText(_translate("TempInvalidF035Dialog", "Эксперт", None))

from library.crbcombobox import CRBComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.ICDCodeEdit import CICDCodeEdit
from Events.ActionStatus import CActionStatusComboBox
from library.MultivalueComboBox import CRBMultivalueComboBox
from library.DateEdit import CDateEdit