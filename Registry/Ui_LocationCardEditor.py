# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Registry\LocationCardEditor.ui'
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

class Ui_LocationCardEditor(object):
    def setupUi(self, LocationCardEditor):
        LocationCardEditor.setObjectName(_fromUtf8("LocationCardEditor"))
        LocationCardEditor.resize(500, 291)
        LocationCardEditor.setSizeGripEnabled(False)
        self.gridLayout = QtGui.QGridLayout(LocationCardEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(LocationCardEditor)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.cmbLocationCardType = CRBComboBox(LocationCardEditor)
        self.cmbLocationCardType.setObjectName(_fromUtf8("cmbLocationCardType"))
        self.gridLayout.addWidget(self.cmbLocationCardType, 0, 1, 1, 1)
        self.lblPerson = QtGui.QLabel(LocationCardEditor)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 1, 0, 1, 1)
        self.cmbPerson = CPersonComboBoxEx(LocationCardEditor)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 1, 1, 1, 1)
        self.lblNotesPage = QtGui.QLabel(LocationCardEditor)
        self.lblNotesPage.setObjectName(_fromUtf8("lblNotesPage"))
        self.gridLayout.addWidget(self.lblNotesPage, 2, 0, 1, 1)
        self.edtNotesPage = QtGui.QTextEdit(LocationCardEditor)
        self.edtNotesPage.setObjectName(_fromUtf8("edtNotesPage"))
        self.gridLayout.addWidget(self.edtNotesPage, 2, 1, 2, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(LocationCardEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.label.setBuddy(self.cmbLocationCardType)
        self.lblPerson.setBuddy(self.cmbPerson)
        self.lblNotesPage.setBuddy(self.edtNotesPage)

        self.retranslateUi(LocationCardEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), LocationCardEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), LocationCardEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(LocationCardEditor)
        LocationCardEditor.setTabOrder(self.cmbLocationCardType, self.cmbPerson)
        LocationCardEditor.setTabOrder(self.cmbPerson, self.edtNotesPage)
        LocationCardEditor.setTabOrder(self.edtNotesPage, self.buttonBox)

    def retranslateUi(self, LocationCardEditor):
        LocationCardEditor.setWindowTitle(_translate("LocationCardEditor", "Место нахождения амбулаторной карты", None))
        self.label.setText(_translate("LocationCardEditor", "Место нахождения амбулаторной карты", None))
        self.lblPerson.setText(_translate("LocationCardEditor", "Ответственный за хранение", None))
        self.lblNotesPage.setText(_translate("LocationCardEditor", "Примечание", None))

from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.crbcombobox import CRBComboBox
