# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\HospitalBeds\CardLocationEditDialog.ui'
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

class Ui_CardLocation(object):
    def setupUi(self, CardLocation):
        CardLocation.setObjectName(_fromUtf8("CardLocation"))
        CardLocation.resize(387, 155)
        self.gridLayout = QtGui.QGridLayout(CardLocation)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblCardLocation = QtGui.QLabel(CardLocation)
        self.lblCardLocation.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lblCardLocation.setObjectName(_fromUtf8("lblCardLocation"))
        self.gridLayout.addWidget(self.lblCardLocation, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(CardLocation)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 7, 1, 1, 3)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 1, 1, 1)
        self.lblCardLocationNotes = QtGui.QLabel(CardLocation)
        self.lblCardLocationNotes.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lblCardLocationNotes.setObjectName(_fromUtf8("lblCardLocationNotes"))
        self.gridLayout.addWidget(self.lblCardLocationNotes, 5, 0, 1, 1)
        self.lblCardLocationDate = QtGui.QLabel(CardLocation)
        self.lblCardLocationDate.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lblCardLocationDate.setObjectName(_fromUtf8("lblCardLocationDate"))
        self.gridLayout.addWidget(self.lblCardLocationDate, 4, 0, 1, 1)
        self.edtCardLocationDate = CCreateEventDateEdit(CardLocation)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtCardLocationDate.sizePolicy().hasHeightForWidth())
        self.edtCardLocationDate.setSizePolicy(sizePolicy)
        self.edtCardLocationDate.setCalendarPopup(True)
        self.edtCardLocationDate.setObjectName(_fromUtf8("edtCardLocationDate"))
        self.gridLayout.addWidget(self.edtCardLocationDate, 4, 1, 1, 3)
        self.edtCardLocationNotes = QtGui.QLineEdit(CardLocation)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtCardLocationNotes.sizePolicy().hasHeightForWidth())
        self.edtCardLocationNotes.setSizePolicy(sizePolicy)
        self.edtCardLocationNotes.setObjectName(_fromUtf8("edtCardLocationNotes"))
        self.gridLayout.addWidget(self.edtCardLocationNotes, 5, 1, 1, 3)
        self.cmbCardLocation = CRBComboBox(CardLocation)
        self.cmbCardLocation.setEditable(True)
        self.cmbCardLocation.setObjectName(_fromUtf8("cmbCardLocation"))
        self.gridLayout.addWidget(self.cmbCardLocation, 1, 1, 1, 3)

        self.retranslateUi(CardLocation)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), CardLocation.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), CardLocation.reject)
        QtCore.QMetaObject.connectSlotsByName(CardLocation)

    def retranslateUi(self, CardLocation):
        CardLocation.setWindowTitle(_translate("CardLocation", "Редактор места нахождения карты", None))
        self.lblCardLocation.setText(_translate("CardLocation", "Место нахождения карты", None))
        self.lblCardLocationNotes.setText(_translate("CardLocation", "Обстоятельства передачи", None))
        self.lblCardLocationDate.setText(_translate("CardLocation", "Дата передачи", None))

from Events.CreateEventDateEdit import CCreateEventDateEdit
from library.crbcombobox import CRBComboBox
