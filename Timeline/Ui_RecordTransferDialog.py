# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Timeline\RecordTransferDialog.ui'
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

class Ui_RecordTransferDialog(object):
    def setupUi(self, RecordTransferDialog):
        RecordTransferDialog.setObjectName(_fromUtf8("RecordTransferDialog"))
        RecordTransferDialog.resize(571, 426)
        self.verticalLayout = QtGui.QVBoxLayout(RecordTransferDialog)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.txtClientInfoBrowser = CTextBrowser(RecordTransferDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtClientInfoBrowser.sizePolicy().hasHeightForWidth())
        self.txtClientInfoBrowser.setSizePolicy(sizePolicy)
        self.txtClientInfoBrowser.setMinimumSize(QtCore.QSize(0, 100))
        self.txtClientInfoBrowser.setMaximumSize(QtCore.QSize(16777215, 130))
        self.txtClientInfoBrowser.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.txtClientInfoBrowser.setObjectName(_fromUtf8("txtClientInfoBrowser"))
        self.verticalLayout.addWidget(self.txtClientInfoBrowser)
        self.splitter = QtGui.QSplitter(RecordTransferDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.frmFilter = QtGui.QWidget(self.splitter)
        self.frmFilter.setObjectName(_fromUtf8("frmFilter"))
        self.gridLayout = QtGui.QGridLayout(self.frmFilter)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.calendar = CCalendarWidget(self.frmFilter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calendar.sizePolicy().hasHeightForWidth())
        self.calendar.setSizePolicy(sizePolicy)
        self.calendar.setFirstDayOfWeek(QtCore.Qt.Monday)
        self.calendar.setGridVisible(False)
        self.calendar.setObjectName(_fromUtf8("calendar"))
        self.gridLayout.addWidget(self.calendar, 0, 0, 1, 2)
        self.label = QtGui.QLabel(self.frmFilter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 2)
        self.label_2 = QtGui.QLabel(self.frmFilter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 2)
        self.cmbAppointmentPurpose = CRBComboBox(self.frmFilter)
        self.cmbAppointmentPurpose.setObjectName(_fromUtf8("cmbAppointmentPurpose"))
        self.gridLayout.addWidget(self.cmbAppointmentPurpose, 4, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 24, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)
        self.cmbSpeciality = CRBComboBox(self.frmFilter)
        self.cmbSpeciality.setObjectName(_fromUtf8("cmbSpeciality"))
        self.gridLayout.addWidget(self.cmbSpeciality, 2, 0, 1, 2)
        self.tblPersonnel = CTableView(self.splitter)
        self.tblPersonnel.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblPersonnel.setObjectName(_fromUtf8("tblPersonnel"))
        self.tblScheduleItems = CTableView(self.splitter)
        self.tblScheduleItems.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblScheduleItems.setObjectName(_fromUtf8("tblScheduleItems"))
        self.verticalLayout.addWidget(self.splitter)
        self.buttonBox = QtGui.QDialogButtonBox(RecordTransferDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.label.setBuddy(self.cmbSpeciality)
        self.label_2.setBuddy(self.cmbAppointmentPurpose)

        self.retranslateUi(RecordTransferDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RecordTransferDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RecordTransferDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RecordTransferDialog)
        RecordTransferDialog.setTabOrder(self.calendar, self.tblPersonnel)
        RecordTransferDialog.setTabOrder(self.tblPersonnel, self.tblScheduleItems)
        RecordTransferDialog.setTabOrder(self.tblScheduleItems, self.buttonBox)
        RecordTransferDialog.setTabOrder(self.buttonBox, self.cmbSpeciality)
        RecordTransferDialog.setTabOrder(self.cmbSpeciality, self.cmbAppointmentPurpose)

    def retranslateUi(self, RecordTransferDialog):
        RecordTransferDialog.setWindowTitle(_translate("RecordTransferDialog", "Перенести запись", None))
        self.txtClientInfoBrowser.setWhatsThis(_translate("RecordTransferDialog", "Описание пациента", None))
        self.txtClientInfoBrowser.setHtml(_translate("RecordTransferDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Tahoma\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\';\"><br /></p></body></html>", None))
        self.calendar.setWhatsThis(_translate("RecordTransferDialog", "Дата, на которую переносится запись", None))
        self.label.setText(_translate("RecordTransferDialog", "&Специальность", None))
        self.label_2.setText(_translate("RecordTransferDialog", "&Назначение приёма", None))

from library.CalendarWidget import CCalendarWidget
from library.TableView import CTableView
from library.TextBrowser import CTextBrowser
from library.crbcombobox import CRBComboBox
