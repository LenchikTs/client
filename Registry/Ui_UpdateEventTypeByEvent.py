# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Registry\UpdateEventTypeByEvent.ui'
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

class Ui_UpdateEventTypeByEvent(object):
    def setupUi(self, UpdateEventTypeByEvent):
        UpdateEventTypeByEvent.setObjectName(_fromUtf8("UpdateEventTypeByEvent"))
        UpdateEventTypeByEvent.resize(374, 70)
        UpdateEventTypeByEvent.setSizeGripEnabled(False)
        self.gridLayout = QtGui.QGridLayout(UpdateEventTypeByEvent)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbEventType = CRBComboBox(UpdateEventTypeByEvent)
        self.cmbEventType.setObjectName(_fromUtf8("cmbEventType"))
        self.gridLayout.addWidget(self.cmbEventType, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(103, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(UpdateEventTypeByEvent)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)
        self.label = QtGui.QLabel(UpdateEventTypeByEvent)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(UpdateEventTypeByEvent)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), UpdateEventTypeByEvent.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), UpdateEventTypeByEvent.reject)
        QtCore.QMetaObject.connectSlotsByName(UpdateEventTypeByEvent)
        UpdateEventTypeByEvent.setTabOrder(self.cmbEventType, self.buttonBox)

    def retranslateUi(self, UpdateEventTypeByEvent):
        UpdateEventTypeByEvent.setWindowTitle(_translate("UpdateEventTypeByEvent", "Типы события", None))
        self.label.setText(_translate("UpdateEventTypeByEvent", "Тип события", None))

from library.crbcombobox import CRBComboBox
