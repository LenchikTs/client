# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\HospitalBeds\ClientFeaturesEditDialog.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(916, 843)
        self.gridlayout = QtGui.QGridLayout(Dialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 2, 0, 1, 2)
        self.frmWidgets = QtGui.QWidget(Dialog)
        self.frmWidgets.setObjectName(_fromUtf8("frmWidgets"))
        self.gridLayout_4 = QtGui.QGridLayout(self.frmWidgets)
        self.gridLayout_4.setMargin(4)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.lblMenarhe = QtGui.QLabel(self.frmWidgets)
        self.lblMenarhe.setObjectName(_fromUtf8("lblMenarhe"))
        self.gridLayout_4.addWidget(self.lblMenarhe, 2, 7, 1, 1)
        self.lblMenoPausa = QtGui.QLabel(self.frmWidgets)
        self.lblMenoPausa.setObjectName(_fromUtf8("lblMenoPausa"))
        self.gridLayout_4.addWidget(self.lblMenoPausa, 2, 9, 1, 1)
        self.edtMenarhe = QtGui.QSpinBox(self.frmWidgets)
        self.edtMenarhe.setObjectName(_fromUtf8("edtMenarhe"))
        self.gridLayout_4.addWidget(self.edtMenarhe, 2, 8, 1, 1)
        self.lblBloodType = QtGui.QLabel(self.frmWidgets)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblBloodType.sizePolicy().hasHeightForWidth())
        self.lblBloodType.setSizePolicy(sizePolicy)
        self.lblBloodType.setObjectName(_fromUtf8("lblBloodType"))
        self.gridLayout_4.addWidget(self.lblBloodType, 1, 0, 1, 1)
        self.cmbBloodType = CRBComboBox(self.frmWidgets)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbBloodType.sizePolicy().hasHeightForWidth())
        self.cmbBloodType.setSizePolicy(sizePolicy)
        self.cmbBloodType.setObjectName(_fromUtf8("cmbBloodType"))
        self.gridLayout_4.addWidget(self.cmbBloodType, 1, 1, 1, 1)
        self.lblBloodTypeDate = QtGui.QLabel(self.frmWidgets)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblBloodTypeDate.sizePolicy().hasHeightForWidth())
        self.lblBloodTypeDate.setSizePolicy(sizePolicy)
        self.lblBloodTypeDate.setObjectName(_fromUtf8("lblBloodTypeDate"))
        self.gridLayout_4.addWidget(self.lblBloodTypeDate, 1, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 2, 11, 1, 1)
        self.edtBloodTypeDate = CDateEdit(self.frmWidgets)
        self.edtBloodTypeDate.setCalendarPopup(True)
        self.edtBloodTypeDate.setObjectName(_fromUtf8("edtBloodTypeDate"))
        self.gridLayout_4.addWidget(self.edtBloodTypeDate, 1, 3, 1, 1)
        self.lblBirthHeight = QtGui.QLabel(self.frmWidgets)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblBirthHeight.sizePolicy().hasHeightForWidth())
        self.lblBirthHeight.setSizePolicy(sizePolicy)
        self.lblBirthHeight.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblBirthHeight.setObjectName(_fromUtf8("lblBirthHeight"))
        self.gridLayout_4.addWidget(self.lblBirthHeight, 2, 0, 1, 1)
        self.edtBirthHeight = QtGui.QSpinBox(self.frmWidgets)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBirthHeight.sizePolicy().hasHeightForWidth())
        self.edtBirthHeight.setSizePolicy(sizePolicy)
        self.edtBirthHeight.setMaximum(200)
        self.edtBirthHeight.setObjectName(_fromUtf8("edtBirthHeight"))
        self.gridLayout_4.addWidget(self.edtBirthHeight, 2, 1, 1, 1)
        self.lblBirthWeight = QtGui.QLabel(self.frmWidgets)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblBirthWeight.sizePolicy().hasHeightForWidth())
        self.lblBirthWeight.setSizePolicy(sizePolicy)
        self.lblBirthWeight.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblBirthWeight.setObjectName(_fromUtf8("lblBirthWeight"))
        self.gridLayout_4.addWidget(self.lblBirthWeight, 2, 2, 1, 1)
        self.edtBirthWeight = QtGui.QSpinBox(self.frmWidgets)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBirthWeight.sizePolicy().hasHeightForWidth())
        self.edtBirthWeight.setSizePolicy(sizePolicy)
        self.edtBirthWeight.setMaximumSize(QtCore.QSize(70, 16777215))
        self.edtBirthWeight.setMaximum(9999)
        self.edtBirthWeight.setObjectName(_fromUtf8("edtBirthWeight"))
        self.gridLayout_4.addWidget(self.edtBirthWeight, 2, 3, 1, 1)
        self.edtBirthGestationalAge = QtGui.QSpinBox(self.frmWidgets)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBirthGestationalAge.sizePolicy().hasHeightForWidth())
        self.edtBirthGestationalAge.setSizePolicy(sizePolicy)
        self.edtBirthGestationalAge.setObjectName(_fromUtf8("edtBirthGestationalAge"))
        self.gridLayout_4.addWidget(self.edtBirthGestationalAge, 2, 6, 1, 1)
        self.grbAllergy_2 = QtGui.QGroupBox(self.frmWidgets)
        self.grbAllergy_2.setObjectName(_fromUtf8("grbAllergy_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.grbAllergy_2)
        self.gridLayout_3.setMargin(4)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.tblIntoleranceMedicament = CInDocTableView(self.grbAllergy_2)
        self.tblIntoleranceMedicament.setObjectName(_fromUtf8("tblIntoleranceMedicament"))
        self.gridLayout_3.addWidget(self.tblIntoleranceMedicament, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.grbAllergy_2, 4, 0, 1, 12)
        self.edtBloodTypeNotes = QtGui.QLineEdit(self.frmWidgets)
        self.edtBloodTypeNotes.setObjectName(_fromUtf8("edtBloodTypeNotes"))
        self.gridLayout_4.addWidget(self.edtBloodTypeNotes, 1, 6, 1, 6)
        self.lblBirthGestationalAge = QtGui.QLabel(self.frmWidgets)
        self.lblBirthGestationalAge.setObjectName(_fromUtf8("lblBirthGestationalAge"))
        self.gridLayout_4.addWidget(self.lblBirthGestationalAge, 2, 4, 1, 1)
        self.lblBloodTypeNotes = QtGui.QLabel(self.frmWidgets)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblBloodTypeNotes.sizePolicy().hasHeightForWidth())
        self.lblBloodTypeNotes.setSizePolicy(sizePolicy)
        self.lblBloodTypeNotes.setObjectName(_fromUtf8("lblBloodTypeNotes"))
        self.gridLayout_4.addWidget(self.lblBloodTypeNotes, 1, 4, 1, 2)
        self.edtMenoPausa = QtGui.QSpinBox(self.frmWidgets)
        self.edtMenoPausa.setObjectName(_fromUtf8("edtMenoPausa"))
        self.gridLayout_4.addWidget(self.edtMenoPausa, 2, 10, 1, 1)
        self.grbAllergy = QtGui.QGroupBox(self.frmWidgets)
        self.grbAllergy.setObjectName(_fromUtf8("grbAllergy"))
        self.gridLayout_2 = QtGui.QGridLayout(self.grbAllergy)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tblAllergy = CInDocTableView(self.grbAllergy)
        self.tblAllergy.setObjectName(_fromUtf8("tblAllergy"))
        self.gridLayout_2.addWidget(self.tblAllergy, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.grbAllergy, 3, 0, 1, 12)
        self.txtClientInfoBrowser = QtGui.QTextBrowser(self.frmWidgets)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtClientInfoBrowser.sizePolicy().hasHeightForWidth())
        self.txtClientInfoBrowser.setSizePolicy(sizePolicy)
        self.txtClientInfoBrowser.setMinimumSize(QtCore.QSize(0, 100))
        self.txtClientInfoBrowser.setObjectName(_fromUtf8("txtClientInfoBrowser"))
        self.gridLayout_4.addWidget(self.txtClientInfoBrowser, 0, 0, 1, 12)
        self.gridlayout.addWidget(self.frmWidgets, 1, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.frmWidgets, self.cmbBloodType)
        Dialog.setTabOrder(self.cmbBloodType, self.edtBloodTypeDate)
        Dialog.setTabOrder(self.edtBloodTypeDate, self.edtBloodTypeNotes)
        Dialog.setTabOrder(self.edtBloodTypeNotes, self.edtBirthHeight)
        Dialog.setTabOrder(self.edtBirthHeight, self.edtBirthWeight)
        Dialog.setTabOrder(self.edtBirthWeight, self.edtBirthGestationalAge)
        Dialog.setTabOrder(self.edtBirthGestationalAge, self.edtMenarhe)
        Dialog.setTabOrder(self.edtMenarhe, self.edtMenoPausa)
        Dialog.setTabOrder(self.edtMenoPausa, self.tblAllergy)
        Dialog.setTabOrder(self.tblAllergy, self.tblIntoleranceMedicament)
        Dialog.setTabOrder(self.tblIntoleranceMedicament, self.buttonBox)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Особенности пациента", None))
        self.lblMenarhe.setText(_translate("Dialog", "Менархе", None))
        self.lblMenoPausa.setText(_translate("Dialog", "Менопауза", None))
        self.lblBloodType.setText(_translate("Dialog", "Группа крови", None))
        self.lblBloodTypeDate.setText(_translate("Dialog", "Дата установления", None))
        self.lblBirthHeight.setText(_translate("Dialog", "Рост при рождении", None))
        self.edtBirthHeight.setToolTip(_translate("Dialog", "в сантиметрах", None))
        self.lblBirthWeight.setText(_translate("Dialog", "Вес при рождении", None))
        self.edtBirthWeight.setToolTip(_translate("Dialog", "в граммах", None))
        self.edtBirthGestationalAge.setToolTip(_translate("Dialog", "в неделях", None))
        self.grbAllergy_2.setTitle(_translate("Dialog", "Медикаментозная непереносимость", None))
        self.lblBirthGestationalAge.setText(_translate("Dialog", "Срок рождения", None))
        self.lblBloodTypeNotes.setText(_translate("Dialog", "Примечания", None))
        self.grbAllergy.setTitle(_translate("Dialog", "Аллергия", None))

from library.DateEdit import CDateEdit
from library.InDocTable import CInDocTableView
from library.crbcombobox import CRBComboBox
