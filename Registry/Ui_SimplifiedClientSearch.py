# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Registry\SimplifiedClientSearch.ui'
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

class Ui_SimplifiedClientSearchDialog(object):
    def setupUi(self, SimplifiedClientSearchDialog):
        SimplifiedClientSearchDialog.setObjectName(_fromUtf8("SimplifiedClientSearchDialog"))
        SimplifiedClientSearchDialog.resize(374, 67)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SimplifiedClientSearchDialog.sizePolicy().hasHeightForWidth())
        SimplifiedClientSearchDialog.setSizePolicy(sizePolicy)
        SimplifiedClientSearchDialog.setSizeGripEnabled(False)
        self.gridLayout = QtGui.QGridLayout(SimplifiedClientSearchDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblKey = QtGui.QLabel(SimplifiedClientSearchDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblKey.sizePolicy().hasHeightForWidth())
        self.lblKey.setSizePolicy(sizePolicy)
        self.lblKey.setObjectName(_fromUtf8("lblKey"))
        self.gridLayout.addWidget(self.lblKey, 0, 0, 1, 1)
        self.edtKey = QtGui.QLineEdit(SimplifiedClientSearchDialog)
        self.edtKey.setObjectName(_fromUtf8("edtKey"))
        self.gridLayout.addWidget(self.edtKey, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(103, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(SimplifiedClientSearchDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)

        self.retranslateUi(SimplifiedClientSearchDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SimplifiedClientSearchDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SimplifiedClientSearchDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SimplifiedClientSearchDialog)
        SimplifiedClientSearchDialog.setTabOrder(self.edtKey, self.buttonBox)

    def retranslateUi(self, SimplifiedClientSearchDialog):
        SimplifiedClientSearchDialog.setWindowTitle(_translate("SimplifiedClientSearchDialog", "Упрощенный поиск пациента", None))
        self.lblKey.setText(_translate("SimplifiedClientSearchDialog", "Ключ поиска", None))
        self.edtKey.setToolTip(_translate("SimplifiedClientSearchDialog", "<html><head/><body><p>инициалы: ФИО<br/>инициалы и дата рождения: ФИОДДММГГ[ГГ]<br/>сокращение: Фам Им Отч<br/>сокращение и дата рождения: Фам Им Отч ДДММГГ[ГГ]</p></body></html>", None))

