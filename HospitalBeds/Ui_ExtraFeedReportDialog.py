# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\HospitalBeds\ExtraFeedReportDialog.ui'
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

class Ui_ExtraFeedReportDialog(object):
    def setupUi(self, ExtraFeedReportDialog):
        ExtraFeedReportDialog.setObjectName(_fromUtf8("ExtraFeedReportDialog"))
        ExtraFeedReportDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ExtraFeedReportDialog.resize(502, 91)
        ExtraFeedReportDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(ExtraFeedReportDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblBegDate = QtGui.QLabel(ExtraFeedReportDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblBegDate.sizePolicy().hasHeightForWidth())
        self.lblBegDate.setSizePolicy(sizePolicy)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.edtBegDate = CDateEdit(ExtraFeedReportDialog)
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
        self.buttonBox = QtGui.QDialogButtonBox(ExtraFeedReportDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 3)
        self.lblTypePrint = QtGui.QLabel(ExtraFeedReportDialog)
        self.lblTypePrint.setObjectName(_fromUtf8("lblTypePrint"))
        self.gridLayout.addWidget(self.lblTypePrint, 1, 0, 1, 1)
        self.cmbTypePrint = QtGui.QComboBox(ExtraFeedReportDialog)
        self.cmbTypePrint.setObjectName(_fromUtf8("cmbTypePrint"))
        self.cmbTypePrint.addItem(_fromUtf8(""))
        self.cmbTypePrint.addItem(_fromUtf8(""))
        self.cmbTypePrint.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbTypePrint, 1, 1, 1, 2)
        self.lblBegDate.setBuddy(self.edtBegDate)

        self.retranslateUi(ExtraFeedReportDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ExtraFeedReportDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ExtraFeedReportDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ExtraFeedReportDialog)
        ExtraFeedReportDialog.setTabOrder(self.edtBegDate, self.buttonBox)

    def retranslateUi(self, ExtraFeedReportDialog):
        ExtraFeedReportDialog.setWindowTitle(_translate("ExtraFeedReportDialog", "параметры отчёта", None))
        self.lblBegDate.setText(_translate("ExtraFeedReportDialog", "Порционник на дату", None))
        self.edtBegDate.setDisplayFormat(_translate("ExtraFeedReportDialog", "dd.MM.yyyy", None))
        self.lblTypePrint.setText(_translate("ExtraFeedReportDialog", "Тип порционника", None))
        self.cmbTypePrint.setItemText(0, _translate("ExtraFeedReportDialog", "Порционник с финансированием", None))
        self.cmbTypePrint.setItemText(1, _translate("ExtraFeedReportDialog", "Порционник с финансированием для пациентов", None))
        self.cmbTypePrint.setItemText(2, _translate("ExtraFeedReportDialog", "Порционник с финансированием для лиц по уходу", None))

from library.DateEdit import CDateEdit
