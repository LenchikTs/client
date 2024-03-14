# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Timeline\CalcDialog.ui'
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

class Ui_CalcDialog(object):
    def setupUi(self, CalcDialog):
        CalcDialog.setObjectName(_fromUtf8("CalcDialog"))
        CalcDialog.resize(357, 203)
        self.gridLayout_2 = QtGui.QGridLayout(CalcDialog)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.groupBox = QtGui.QGroupBox(CalcDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setMargin(4)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.chkBudget = QtGui.QCheckBox(self.groupBox)
        self.chkBudget.setChecked(True)
        self.chkBudget.setObjectName(_fromUtf8("chkBudget"))
        self.verticalLayout_2.addWidget(self.chkBudget)
        self.chkCMI = QtGui.QCheckBox(self.groupBox)
        self.chkCMI.setChecked(True)
        self.chkCMI.setObjectName(_fromUtf8("chkCMI"))
        self.verticalLayout_2.addWidget(self.chkCMI)
        self.chkVMI = QtGui.QCheckBox(self.groupBox)
        self.chkVMI.setChecked(True)
        self.chkVMI.setObjectName(_fromUtf8("chkVMI"))
        self.verticalLayout_2.addWidget(self.chkVMI)
        self.chkCach = QtGui.QCheckBox(self.groupBox)
        self.chkCach.setChecked(True)
        self.chkCach.setObjectName(_fromUtf8("chkCach"))
        self.verticalLayout_2.addWidget(self.chkCach)
        self.chkTargeted = QtGui.QCheckBox(self.groupBox)
        self.chkTargeted.setChecked(True)
        self.chkTargeted.setObjectName(_fromUtf8("chkTargeted"))
        self.verticalLayout_2.addWidget(self.chkTargeted)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 2, 1)
        self.groupBox_2 = QtGui.QGroupBox(CalcDialog)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.chkAmbulance = QtGui.QCheckBox(self.groupBox_2)
        self.chkAmbulance.setChecked(True)
        self.chkAmbulance.setObjectName(_fromUtf8("chkAmbulance"))
        self.verticalLayout.addWidget(self.chkAmbulance)
        self.chkHome = QtGui.QCheckBox(self.groupBox_2)
        self.chkHome.setChecked(True)
        self.chkHome.setObjectName(_fromUtf8("chkHome"))
        self.verticalLayout.addWidget(self.chkHome)
        self.chkExp = QtGui.QCheckBox(self.groupBox_2)
        self.chkExp.setObjectName(_fromUtf8("chkExp"))
        self.verticalLayout.addWidget(self.chkExp)
        self.gridLayout_2.addWidget(self.groupBox_2, 0, 1, 1, 1)
        self.groupBox_3 = QtGui.QGroupBox(CalcDialog)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setMargin(4)
        self.verticalLayout_3.setSpacing(4)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.rbFillAll = QtGui.QRadioButton(self.groupBox_3)
        self.rbFillAll.setObjectName(_fromUtf8("rbFillAll"))
        self.verticalLayout_3.addWidget(self.rbFillAll)
        self.rbFillNew = QtGui.QRadioButton(self.groupBox_3)
        self.rbFillNew.setChecked(True)
        self.rbFillNew.setObjectName(_fromUtf8("rbFillNew"))
        self.verticalLayout_3.addWidget(self.rbFillNew)
        self.gridLayout_2.addWidget(self.groupBox_3, 1, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(CalcDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 3, 0, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 2, 0, 1, 1)

        self.retranslateUi(CalcDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), CalcDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), CalcDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CalcDialog)
        CalcDialog.setTabOrder(self.chkBudget, self.chkCMI)
        CalcDialog.setTabOrder(self.chkCMI, self.chkVMI)
        CalcDialog.setTabOrder(self.chkVMI, self.chkCach)
        CalcDialog.setTabOrder(self.chkCach, self.chkTargeted)
        CalcDialog.setTabOrder(self.chkTargeted, self.chkAmbulance)
        CalcDialog.setTabOrder(self.chkAmbulance, self.chkHome)
        CalcDialog.setTabOrder(self.chkHome, self.chkExp)
        CalcDialog.setTabOrder(self.chkExp, self.rbFillAll)
        CalcDialog.setTabOrder(self.rbFillAll, self.rbFillNew)
        CalcDialog.setTabOrder(self.rbFillNew, self.buttonBox)

    def retranslateUi(self, CalcDialog):
        CalcDialog.setWindowTitle(_translate("CalcDialog", "Заполнение фактического количества посещений", None))
        self.groupBox.setTitle(_translate("CalcDialog", "Тип финансирования", None))
        self.chkBudget.setText(_translate("CalcDialog", "Бюджет", None))
        self.chkCMI.setText(_translate("CalcDialog", "ОМС", None))
        self.chkVMI.setText(_translate("CalcDialog", "ДМС", None))
        self.chkCach.setText(_translate("CalcDialog", "Платные", None))
        self.chkTargeted.setText(_translate("CalcDialog", "Целевые", None))
        self.groupBox_2.setTitle(_translate("CalcDialog", "Место", None))
        self.chkAmbulance.setText(_translate("CalcDialog", "Амбулаторно", None))
        self.chkHome.setText(_translate("CalcDialog", "Дом.", None))
        self.chkExp.setText(_translate("CalcDialog", "КЭР", None))
        self.groupBox_3.setTitle(_translate("CalcDialog", "Заполнение", None))
        self.rbFillAll.setText(_translate("CalcDialog", "заполнять всё", None))
        self.rbFillNew.setText(_translate("CalcDialog", "только незаполненное", None))

