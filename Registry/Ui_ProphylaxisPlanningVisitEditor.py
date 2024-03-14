# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\projects\samson\UP_s11\client_DN\Registry\ProphylaxisPlanningVisitEditor.ui'
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

class Ui_ProphylaxisPlanningVisitEditor(object):
    def setupUi(self, ProphylaxisPlanningVisitEditor):
        ProphylaxisPlanningVisitEditor.setObjectName(_fromUtf8("ProphylaxisPlanningVisitEditor"))
        ProphylaxisPlanningVisitEditor.resize(400, 66)
        self.gridLayout = QtGui.QGridLayout(ProphylaxisPlanningVisitEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setHorizontalSpacing(5)
        self.gridLayout.setVerticalSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ProphylaxisPlanningVisitEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 3)
        self.cmbVisit = CVisitComboBox(ProphylaxisPlanningVisitEditor)
        self.cmbVisit.setObjectName(_fromUtf8("cmbVisit"))
        self.gridLayout.addWidget(self.cmbVisit, 0, 1, 1, 2)
        self.lblVisit = QtGui.QLabel(ProphylaxisPlanningVisitEditor)
        self.lblVisit.setObjectName(_fromUtf8("lblVisit"))
        self.gridLayout.addWidget(self.lblVisit, 0, 0, 1, 1)

        self.retranslateUi(ProphylaxisPlanningVisitEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ProphylaxisPlanningVisitEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ProphylaxisPlanningVisitEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(ProphylaxisPlanningVisitEditor)

    def retranslateUi(self, ProphylaxisPlanningVisitEditor):
        ProphylaxisPlanningVisitEditor.setWindowTitle(_translate("ProphylaxisPlanningVisitEditor", "Явка", None))
        self.lblVisit.setText(_translate("ProphylaxisPlanningVisitEditor", "Визит", None))

from Registry.VisitComboBox import CVisitComboBox
