# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\DataCheck\LogicalControlDiagnosis.ui'
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
        Dialog.resize(672, 568)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblBegin = QtGui.QLabel(Dialog)
        self.lblBegin.setObjectName(_fromUtf8("lblBegin"))
        self.gridLayout.addWidget(self.lblBegin, 0, 0, 1, 1)
        self.dateBeginPeriod = CDateEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateBeginPeriod.sizePolicy().hasHeightForWidth())
        self.dateBeginPeriod.setSizePolicy(sizePolicy)
        self.dateBeginPeriod.setCalendarPopup(True)
        self.dateBeginPeriod.setObjectName(_fromUtf8("dateBeginPeriod"))
        self.gridLayout.addWidget(self.dateBeginPeriod, 0, 1, 1, 1)
        self.lblEnd = QtGui.QLabel(Dialog)
        self.lblEnd.setObjectName(_fromUtf8("lblEnd"))
        self.gridLayout.addWidget(self.lblEnd, 0, 2, 1, 1)
        self.dateEndPeriod = CDateEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateEndPeriod.sizePolicy().hasHeightForWidth())
        self.dateEndPeriod.setSizePolicy(sizePolicy)
        self.dateEndPeriod.setCalendarPopup(True)
        self.dateEndPeriod.setObjectName(_fromUtf8("dateEndPeriod"))
        self.gridLayout.addWidget(self.dateEndPeriod, 0, 3, 1, 2)
        spacerItem = QtGui.QSpacerItem(68, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 5, 1, 1)
        self.chkMKB = QtGui.QCheckBox(Dialog)
        self.chkMKB.setObjectName(_fromUtf8("chkMKB"))
        self.gridLayout.addWidget(self.chkMKB, 0, 6, 1, 1)
        self.edtMKBFrom = CICDCodeEdit(Dialog)
        self.edtMKBFrom.setEnabled(False)
        self.edtMKBFrom.setMaximumSize(QtCore.QSize(50, 16777215))
        self.edtMKBFrom.setObjectName(_fromUtf8("edtMKBFrom"))
        self.gridLayout.addWidget(self.edtMKBFrom, 0, 7, 1, 1)
        self.edtMKBTo = CICDCodeEdit(Dialog)
        self.edtMKBTo.setEnabled(False)
        self.edtMKBTo.setMaximumSize(QtCore.QSize(50, 16777215))
        self.edtMKBTo.setObjectName(_fromUtf8("edtMKBTo"))
        self.gridLayout.addWidget(self.edtMKBTo, 0, 8, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(14, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 9, 1, 1)
        self.chkAccountChronicDisease = QtGui.QCheckBox(Dialog)
        self.chkAccountChronicDisease.setChecked(True)
        self.chkAccountChronicDisease.setObjectName(_fromUtf8("chkAccountChronicDisease"))
        self.gridLayout.addWidget(self.chkAccountChronicDisease, 2, 0, 1, 3)
        spacerItem2 = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 2, 4, 1, 2)
        self.chkDiseaseDiagnostic = QtGui.QCheckBox(Dialog)
        self.chkDiseaseDiagnostic.setChecked(True)
        self.chkDiseaseDiagnostic.setObjectName(_fromUtf8("chkDiseaseDiagnostic"))
        self.gridLayout.addWidget(self.chkDiseaseDiagnostic, 2, 6, 1, 3)
        self.chkAccountAcuteDisease = QtGui.QCheckBox(Dialog)
        self.chkAccountAcuteDisease.setChecked(True)
        self.chkAccountAcuteDisease.setObjectName(_fromUtf8("chkAccountAcuteDisease"))
        self.gridLayout.addWidget(self.chkAccountAcuteDisease, 3, 0, 1, 3)
        spacerItem3 = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 3, 4, 1, 2)
        self.chkDataDiagnosis = QtGui.QCheckBox(Dialog)
        self.chkDataDiagnosis.setChecked(True)
        self.chkDataDiagnosis.setObjectName(_fromUtf8("chkDataDiagnosis"))
        self.gridLayout.addWidget(self.chkDataDiagnosis, 3, 6, 1, 2)
        self.chkControlIntegrity = QtGui.QCheckBox(Dialog)
        self.chkControlIntegrity.setChecked(True)
        self.chkControlIntegrity.setObjectName(_fromUtf8("chkControlIntegrity"))
        self.gridLayout.addWidget(self.chkControlIntegrity, 4, 0, 1, 3)
        spacerItem4 = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 4, 4, 1, 2)
        self.chkCharacterChronicFirstDisease = QtGui.QCheckBox(Dialog)
        self.chkCharacterChronicFirstDisease.setChecked(True)
        self.chkCharacterChronicFirstDisease.setObjectName(_fromUtf8("chkCharacterChronicFirstDisease"))
        self.gridLayout.addWidget(self.chkCharacterChronicFirstDisease, 4, 6, 1, 3)
        self.chkCodingMKBEx = QtGui.QCheckBox(Dialog)
        self.chkCodingMKBEx.setChecked(True)
        self.chkCodingMKBEx.setObjectName(_fromUtf8("chkCodingMKBEx"))
        self.gridLayout.addWidget(self.chkCodingMKBEx, 5, 0, 1, 4)
        spacerItem5 = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 5, 4, 1, 2)
        self.chkCharacterChronicKnowDisease = QtGui.QCheckBox(Dialog)
        self.chkCharacterChronicKnowDisease.setChecked(True)
        self.chkCharacterChronicKnowDisease.setObjectName(_fromUtf8("chkCharacterChronicKnowDisease"))
        self.gridLayout.addWidget(self.chkCharacterChronicKnowDisease, 5, 6, 1, 4)
        self.chkCodingMKB = QtGui.QCheckBox(Dialog)
        self.chkCodingMKB.setChecked(True)
        self.chkCodingMKB.setObjectName(_fromUtf8("chkCodingMKB"))
        self.gridLayout.addWidget(self.chkCodingMKB, 6, 0, 1, 3)
        spacerItem6 = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem6, 6, 4, 1, 2)
        self.chkChronicAcuteDisease = QtGui.QCheckBox(Dialog)
        self.chkChronicAcuteDisease.setChecked(True)
        self.chkChronicAcuteDisease.setObjectName(_fromUtf8("chkChronicAcuteDisease"))
        self.gridLayout.addWidget(self.chkChronicAcuteDisease, 6, 6, 1, 3)
        self.chkCodingTraumaType = QtGui.QCheckBox(Dialog)
        self.chkCodingTraumaType.setChecked(True)
        self.chkCodingTraumaType.setObjectName(_fromUtf8("chkCodingTraumaType"))
        self.gridLayout.addWidget(self.chkCodingTraumaType, 7, 0, 1, 4)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem7, 7, 4, 1, 2)
        self.chkIgnoreCorrectionUser = QtGui.QCheckBox(Dialog)
        self.chkIgnoreCorrectionUser.setEnabled(False)
        self.chkIgnoreCorrectionUser.setObjectName(_fromUtf8("chkIgnoreCorrectionUser"))
        self.gridLayout.addWidget(self.chkIgnoreCorrectionUser, 7, 6, 1, 3)
        self.listResultControlDiagnosis = CRemarkListWidget(Dialog)
        self.listResultControlDiagnosis.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed|QtGui.QAbstractItemView.SelectedClicked)
        self.listResultControlDiagnosis.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listResultControlDiagnosis.setFlow(QtGui.QListView.TopToBottom)
        self.listResultControlDiagnosis.setObjectName(_fromUtf8("listResultControlDiagnosis"))
        self.gridLayout.addWidget(self.listResultControlDiagnosis, 9, 0, 1, 10)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.btnStartControl = QtGui.QPushButton(Dialog)
        self.btnStartControl.setAutoDefault(True)
        self.btnStartControl.setObjectName(_fromUtf8("btnStartControl"))
        self.horizontalLayout_2.addWidget(self.btnStartControl)
        self.lblCountLine = QtGui.QLabel(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCountLine.sizePolicy().hasHeightForWidth())
        self.lblCountLine.setSizePolicy(sizePolicy)
        self.lblCountLine.setText(_fromUtf8(""))
        self.lblCountLine.setAlignment(QtCore.Qt.AlignCenter)
        self.lblCountLine.setObjectName(_fromUtf8("lblCountLine"))
        self.horizontalLayout_2.addWidget(self.lblCountLine)
        self.btnCorrectControl = QtGui.QPushButton(Dialog)
        self.btnCorrectControl.setEnabled(False)
        self.btnCorrectControl.setObjectName(_fromUtf8("btnCorrectControl"))
        self.horizontalLayout_2.addWidget(self.btnCorrectControl)
        self.btnEndControl = QtGui.QPushButton(Dialog)
        self.btnEndControl.setAutoDefault(True)
        self.btnEndControl.setObjectName(_fromUtf8("btnEndControl"))
        self.horizontalLayout_2.addWidget(self.btnEndControl)
        self.gridLayout.addLayout(self.horizontalLayout_2, 10, 0, 1, 10)
        self.prbControlDiagnosis = CProgressBar(Dialog)
        self.prbControlDiagnosis.setObjectName(_fromUtf8("prbControlDiagnosis"))
        self.gridLayout.addWidget(self.prbControlDiagnosis, 8, 0, 1, 10)
        self.lblAge = QtGui.QLabel(Dialog)
        self.lblAge.setObjectName(_fromUtf8("lblAge"))
        self.gridLayout.addWidget(self.lblAge, 1, 0, 1, 1)
        self.edtAgeFrom = QtGui.QSpinBox(Dialog)
        self.edtAgeFrom.setMaximum(150)
        self.edtAgeFrom.setObjectName(_fromUtf8("edtAgeFrom"))
        self.gridLayout.addWidget(self.edtAgeFrom, 1, 1, 1, 1)
        self.lblAgeTo = QtGui.QLabel(Dialog)
        self.lblAgeTo.setObjectName(_fromUtf8("lblAgeTo"))
        self.gridLayout.addWidget(self.lblAgeTo, 1, 2, 1, 1)
        self.edtAgeTo = QtGui.QSpinBox(Dialog)
        self.edtAgeTo.setMaximum(150)
        self.edtAgeTo.setObjectName(_fromUtf8("edtAgeTo"))
        self.gridLayout.addWidget(self.edtAgeTo, 1, 3, 1, 2)
        spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem8, 1, 5, 1, 5)
        self.lblBegin.setBuddy(self.dateBeginPeriod)
        self.lblEnd.setBuddy(self.dateEndPeriod)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.dateBeginPeriod, self.dateEndPeriod)
        Dialog.setTabOrder(self.dateEndPeriod, self.edtAgeFrom)
        Dialog.setTabOrder(self.edtAgeFrom, self.edtAgeTo)
        Dialog.setTabOrder(self.edtAgeTo, self.chkAccountChronicDisease)
        Dialog.setTabOrder(self.chkAccountChronicDisease, self.chkAccountAcuteDisease)
        Dialog.setTabOrder(self.chkAccountAcuteDisease, self.chkControlIntegrity)
        Dialog.setTabOrder(self.chkControlIntegrity, self.chkCodingMKBEx)
        Dialog.setTabOrder(self.chkCodingMKBEx, self.chkCodingMKB)
        Dialog.setTabOrder(self.chkCodingMKB, self.chkCodingTraumaType)
        Dialog.setTabOrder(self.chkCodingTraumaType, self.chkMKB)
        Dialog.setTabOrder(self.chkMKB, self.edtMKBFrom)
        Dialog.setTabOrder(self.edtMKBFrom, self.edtMKBTo)
        Dialog.setTabOrder(self.edtMKBTo, self.chkDiseaseDiagnostic)
        Dialog.setTabOrder(self.chkDiseaseDiagnostic, self.chkDataDiagnosis)
        Dialog.setTabOrder(self.chkDataDiagnosis, self.chkCharacterChronicFirstDisease)
        Dialog.setTabOrder(self.chkCharacterChronicFirstDisease, self.chkCharacterChronicKnowDisease)
        Dialog.setTabOrder(self.chkCharacterChronicKnowDisease, self.chkChronicAcuteDisease)
        Dialog.setTabOrder(self.chkChronicAcuteDisease, self.chkIgnoreCorrectionUser)
        Dialog.setTabOrder(self.chkIgnoreCorrectionUser, self.listResultControlDiagnosis)
        Dialog.setTabOrder(self.listResultControlDiagnosis, self.btnStartControl)
        Dialog.setTabOrder(self.btnStartControl, self.btnCorrectControl)
        Dialog.setTabOrder(self.btnCorrectControl, self.btnEndControl)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Логический контроль заболеваний в ЛУД", None))
        self.lblBegin.setText(_translate("Dialog", "Период с   ", None))
        self.dateBeginPeriod.setDisplayFormat(_translate("Dialog", "dd.MM.yyyy", None))
        self.lblEnd.setText(_translate("Dialog", "  по    ", None))
        self.dateEndPeriod.setDisplayFormat(_translate("Dialog", "dd.MM.yyyy", None))
        self.chkMKB.setText(_translate("Dialog", "Коды диагнозов по &МКБ", None))
        self.edtMKBFrom.setInputMask(_translate("Dialog", "a00.00; ", None))
        self.edtMKBFrom.setText(_translate("Dialog", "A.", None))
        self.edtMKBTo.setInputMask(_translate("Dialog", "a00.00; ", None))
        self.edtMKBTo.setText(_translate("Dialog", "T99.9", None))
        self.chkAccountChronicDisease.setText(_translate("Dialog", "Учитывать хронические", None))
        self.chkDiseaseDiagnostic.setText(_translate("Dialog", "Контроль длительности по случаям", None))
        self.chkAccountAcuteDisease.setText(_translate("Dialog", "Учитывать острые", None))
        self.chkDataDiagnosis.setText(_translate("Dialog", "Контроль длительности периода", None))
        self.chkControlIntegrity.setText(_translate("Dialog", "Контроль целостности", None))
        self.chkCharacterChronicFirstDisease.setText(_translate("Dialog", "Контроль начала хронического заболевания", None))
        self.chkCodingMKBEx.setText(_translate("Dialog", "Различие в шифрах доп.секции", None))
        self.chkCharacterChronicKnowDisease.setText(_translate("Dialog", "Контроль характера хронического заболевания", None))
        self.chkCodingMKB.setText(_translate("Dialog", "Одинаковые блоки МКБ", None))
        self.chkChronicAcuteDisease.setText(_translate("Dialog", "Контроль острое-хроническое-обострение", None))
        self.chkCodingTraumaType.setText(_translate("Dialog", "Несоответствие типа травмы", None))
        self.chkIgnoreCorrectionUser.setText(_translate("Dialog", "Игнорировать участие пользователя", None))
        self.btnStartControl.setText(_translate("Dialog", "начать выполнение", None))
        self.btnCorrectControl.setText(_translate("Dialog", "исправить", None))
        self.btnEndControl.setText(_translate("Dialog", "прервать", None))
        self.prbControlDiagnosis.setFormat(_translate("Dialog", "%p%", None))
        self.lblAge.setText(_translate("Dialog", "Возраст с", None))
        self.lblAgeTo.setText(_translate("Dialog", "  по", None))

from RemarkListWidget import CRemarkListWidget
from library.DateEdit import CDateEdit
from library.ICDCodeEdit import CICDCodeEdit
from library.ProgressBar import CProgressBar
