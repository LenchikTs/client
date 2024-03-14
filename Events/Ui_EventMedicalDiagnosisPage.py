# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Events\EventMedicalDiagnosisPage.ui'
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

class Ui_EventMedicalDiagnosisPageWidget(object):
    def setupUi(self, EventMedicalDiagnosisPageWidget):
        EventMedicalDiagnosisPageWidget.setObjectName(_fromUtf8("EventMedicalDiagnosisPageWidget"))
        EventMedicalDiagnosisPageWidget.resize(613, 580)
        self.verticalLayout = QtGui.QVBoxLayout(EventMedicalDiagnosisPageWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.scrEventMedicalDiagnosisPage = QtGui.QScrollArea(EventMedicalDiagnosisPageWidget)
        self.scrEventMedicalDiagnosisPage.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrEventMedicalDiagnosisPage.setLineWidth(0)
        self.scrEventMedicalDiagnosisPage.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrEventMedicalDiagnosisPage.setWidgetResizable(True)
        self.scrEventMedicalDiagnosisPage.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.scrEventMedicalDiagnosisPage.setObjectName(_fromUtf8("scrEventMedicalDiagnosisPage"))
        self.scrEventMedicalDiagnosisPageInterior = QtGui.QWidget()
        self.scrEventMedicalDiagnosisPageInterior.setGeometry(QtCore.QRect(0, 0, 613, 580))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrEventMedicalDiagnosisPageInterior.sizePolicy().hasHeightForWidth())
        self.scrEventMedicalDiagnosisPageInterior.setSizePolicy(sizePolicy)
        self.scrEventMedicalDiagnosisPageInterior.setObjectName(_fromUtf8("scrEventMedicalDiagnosisPageInterior"))
        self.gridLayout = QtGui.QGridLayout(self.scrEventMedicalDiagnosisPageInterior)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblEventMedicalDiagnosis = CEventMedicalDiagnosisInDocTableView(self.scrEventMedicalDiagnosisPageInterior)
        self.tblEventMedicalDiagnosis.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tblEventMedicalDiagnosis.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblEventMedicalDiagnosis.setObjectName(_fromUtf8("tblEventMedicalDiagnosis"))
        self.gridLayout.addWidget(self.tblEventMedicalDiagnosis, 0, 0, 1, 1)
        self.scrEventMedicalDiagnosisPage.setWidget(self.scrEventMedicalDiagnosisPageInterior)
        self.verticalLayout.addWidget(self.scrEventMedicalDiagnosisPage)

        self.retranslateUi(EventMedicalDiagnosisPageWidget)
        QtCore.QMetaObject.connectSlotsByName(EventMedicalDiagnosisPageWidget)

    def retranslateUi(self, EventMedicalDiagnosisPageWidget):
        EventMedicalDiagnosisPageWidget.setWindowTitle(_translate("EventMedicalDiagnosisPageWidget", "Диагноз", None))

from Events.EventMedicalDiagnosisInDocTableView import CEventMedicalDiagnosisInDocTableView
