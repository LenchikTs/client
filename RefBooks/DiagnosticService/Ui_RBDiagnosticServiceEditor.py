# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\Samson\UP_s11\client_merge\RefBooks\DiagnosticService\RBDiagnosticServiceEditor.ui'
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

class Ui_ItemEditorDialog(object):
    def setupUi(self, ItemEditorDialog):
        ItemEditorDialog.setObjectName(_fromUtf8("ItemEditorDialog"))
        ItemEditorDialog.resize(425, 246)
        ItemEditorDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(ItemEditorDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblCode = QtGui.QLabel(ItemEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ItemEditorDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 10, 0, 1, 2)
        self.lblFullName = QtGui.QLabel(ItemEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblFullName.sizePolicy().hasHeightForWidth())
        self.lblFullName.setSizePolicy(sizePolicy)
        self.lblFullName.setObjectName(_fromUtf8("lblFullName"))
        self.gridLayout.addWidget(self.lblFullName, 2, 0, 1, 1)
        self.edtComponents = QtGui.QLineEdit(ItemEditorDialog)
        self.edtComponents.setObjectName(_fromUtf8("edtComponents"))
        self.gridLayout.addWidget(self.edtComponents, 6, 1, 1, 1)
        self.chkApplicability = QtGui.QCheckBox(ItemEditorDialog)
        self.chkApplicability.setObjectName(_fromUtf8("chkApplicability"))
        self.gridLayout.addWidget(self.chkApplicability, 7, 1, 1, 1)
        self.lblMethod = QtGui.QLabel(ItemEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblMethod.sizePolicy().hasHeightForWidth())
        self.lblMethod.setSizePolicy(sizePolicy)
        self.lblMethod.setObjectName(_fromUtf8("lblMethod"))
        self.gridLayout.addWidget(self.lblMethod, 3, 0, 1, 1)
        self.edtMethod = QtGui.QLineEdit(ItemEditorDialog)
        self.edtMethod.setObjectName(_fromUtf8("edtMethod"))
        self.gridLayout.addWidget(self.edtMethod, 3, 1, 1, 1)
        self.edtLocalization = QtGui.QLineEdit(ItemEditorDialog)
        self.edtLocalization.setObjectName(_fromUtf8("edtLocalization"))
        self.gridLayout.addWidget(self.edtLocalization, 5, 1, 1, 1)
        self.edtArea = QtGui.QLineEdit(ItemEditorDialog)
        self.edtArea.setObjectName(_fromUtf8("edtArea"))
        self.gridLayout.addWidget(self.edtArea, 4, 1, 1, 1)
        self.lblArea = QtGui.QLabel(ItemEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblArea.sizePolicy().hasHeightForWidth())
        self.lblArea.setSizePolicy(sizePolicy)
        self.lblArea.setObjectName(_fromUtf8("lblArea"))
        self.gridLayout.addWidget(self.lblArea, 4, 0, 1, 1)
        self.lblLocalization = QtGui.QLabel(ItemEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblLocalization.sizePolicy().hasHeightForWidth())
        self.lblLocalization.setSizePolicy(sizePolicy)
        self.lblLocalization.setObjectName(_fromUtf8("lblLocalization"))
        self.gridLayout.addWidget(self.lblLocalization, 5, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(103, 21, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 9, 0, 1, 1)
        self.lblName = QtGui.QLabel(ItemEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 1, 0, 1, 1)
        self.edtCode = QtGui.QLineEdit(ItemEditorDialog)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout.addWidget(self.edtCode, 0, 1, 1, 1)
        self.lblComponents = QtGui.QLabel(ItemEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblComponents.sizePolicy().hasHeightForWidth())
        self.lblComponents.setSizePolicy(sizePolicy)
        self.lblComponents.setObjectName(_fromUtf8("lblComponents"))
        self.gridLayout.addWidget(self.lblComponents, 6, 0, 1, 1)
        self.edtFullName = QtGui.QLineEdit(ItemEditorDialog)
        self.edtFullName.setObjectName(_fromUtf8("edtFullName"))
        self.gridLayout.addWidget(self.edtFullName, 2, 1, 1, 1)
        self.edtName = QtGui.QLineEdit(ItemEditorDialog)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 1, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 2, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 2, 2, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 3, 2, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 4, 2, 1, 1)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem6, 5, 2, 1, 1)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem7, 6, 2, 1, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.lblCode.setBuddy(self.edtCode)
        self.lblFullName.setBuddy(self.edtFullName)
        self.lblMethod.setBuddy(self.edtMethod)
        self.lblArea.setBuddy(self.edtArea)
        self.lblLocalization.setBuddy(self.edtLocalization)
        self.lblName.setBuddy(self.edtName)
        self.lblComponents.setBuddy(self.edtComponents)

        self.retranslateUi(ItemEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ItemEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ItemEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ItemEditorDialog)
        ItemEditorDialog.setTabOrder(self.edtCode, self.edtName)

    def retranslateUi(self, ItemEditorDialog):
        ItemEditorDialog.setWindowTitle(_translate("ItemEditorDialog", "ChangeMe!", None))
        self.lblCode.setText(_translate("ItemEditorDialog", "&Код", None))
        self.lblFullName.setText(_translate("ItemEditorDialog", "&Полное наименование", None))
        self.chkApplicability.setText(_translate("ItemEditorDialog", "Применяемость в ЛПУ", None))
        self.lblMethod.setText(_translate("ItemEditorDialog", "Метод", None))
        self.lblArea.setText(_translate("ItemEditorDialog", "Область", None))
        self.lblLocalization.setText(_translate("ItemEditorDialog", "Локализация", None))
        self.lblName.setText(_translate("ItemEditorDialog", "&Наименование", None))
        self.lblComponents.setText(_translate("ItemEditorDialog", "Компоненты", None))
