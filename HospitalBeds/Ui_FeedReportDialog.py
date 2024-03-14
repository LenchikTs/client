# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\HospitalBeds\FeedReportDialog.ui'
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

class Ui_FeedReportDialog(object):
    def setupUi(self, FeedReportDialog):
        FeedReportDialog.setObjectName(_fromUtf8("FeedReportDialog"))
        FeedReportDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        FeedReportDialog.resize(365, 91)
        FeedReportDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(FeedReportDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblBegDate = QtGui.QLabel(FeedReportDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblBegDate.sizePolicy().hasHeightForWidth())
        self.lblBegDate.setSizePolicy(sizePolicy)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.edtBegDate = CDateEdit(FeedReportDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(FeedReportDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 3)
        self.lblTypePrint = QtGui.QLabel(FeedReportDialog)
        self.lblTypePrint.setObjectName(_fromUtf8("lblTypePrint"))
        self.gridLayout.addWidget(self.lblTypePrint, 1, 0, 1, 1)
        self.cmbTypePrint = QtGui.QComboBox(FeedReportDialog)
        self.cmbTypePrint.setObjectName(_fromUtf8("cmbTypePrint"))
        self.cmbTypePrint.addItem(_fromUtf8(""))
        self.cmbTypePrint.addItem(_fromUtf8(""))
        self.cmbTypePrint.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbTypePrint, 1, 1, 1, 2)
        self.lblBegDate.setBuddy(self.edtBegDate)

        self.retranslateUi(FeedReportDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), FeedReportDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), FeedReportDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(FeedReportDialog)
        FeedReportDialog.setTabOrder(self.edtBegDate, self.buttonBox)

    def retranslateUi(self, FeedReportDialog):
        FeedReportDialog.setWindowTitle(_translate("FeedReportDialog", "параметры отчёта", None))
        self.lblBegDate.setText(_translate("FeedReportDialog", "Порционник на дату", None))
        self.edtBegDate.setDisplayFormat(_translate("FeedReportDialog", "dd.MM.yyyy", None))
        self.lblTypePrint.setText(_translate("FeedReportDialog", "Тип порционника", None))
        self.cmbTypePrint.setItemText(0, _translate("FeedReportDialog", "Порционник", None))
        self.cmbTypePrint.setItemText(1, _translate("FeedReportDialog", "Порционник для пациентов", None))
        self.cmbTypePrint.setItemText(2, _translate("FeedReportDialog", "Порционник для лиц по уходу", None))

from library.DateEdit import CDateEdit
