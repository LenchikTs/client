# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\RefBooks\RBVaccinationCalendarItemList.ui'
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

class Ui_RBVaccinationCalendarItemList(object):
    def setupUi(self, RBVaccinationCalendarItemList):
        RBVaccinationCalendarItemList.setObjectName(_fromUtf8("RBVaccinationCalendarItemList"))
        RBVaccinationCalendarItemList.resize(329, 208)
        self.gridLayout = QtGui.QGridLayout(RBVaccinationCalendarItemList)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(RBVaccinationCalendarItemList)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.pnlItems = QtGui.QWidget(self.splitter)
        self.pnlItems.setObjectName(_fromUtf8("pnlItems"))
        self.verticalLayout = QtGui.QVBoxLayout(self.pnlItems)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tblItems = CTableView(self.pnlItems)
        self.tblItems.setObjectName(_fromUtf8("tblItems"))
        self.verticalLayout.addWidget(self.tblItems)
        self.widget_2 = QtGui.QWidget(self.splitter)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tblVaccinationCalendarInfections = CTableView(self.widget_2)
        self.tblVaccinationCalendarInfections.setObjectName(_fromUtf8("tblVaccinationCalendarInfections"))
        self.verticalLayout_2.addWidget(self.tblVaccinationCalendarInfections)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 2)
        self.label = QtGui.QLabel(RBVaccinationCalendarItemList)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RBVaccinationCalendarItemList)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 1, 1, 1)

        self.retranslateUi(RBVaccinationCalendarItemList)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBVaccinationCalendarItemList.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBVaccinationCalendarItemList.reject)
        QtCore.QMetaObject.connectSlotsByName(RBVaccinationCalendarItemList)

    def retranslateUi(self, RBVaccinationCalendarItemList):
        RBVaccinationCalendarItemList.setWindowTitle(_translate("RBVaccinationCalendarItemList", "Dialog", None))
        self.label.setText(_translate("RBVaccinationCalendarItemList", "Всего", None))

from library.TableView import CTableView
