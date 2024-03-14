# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Timeline\TemplateDialog.ui'
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

class Ui_TemplateDialog(object):
    def setupUi(self, TemplateDialog):
        TemplateDialog.setObjectName(_fromUtf8("TemplateDialog"))
        TemplateDialog.resize(1112, 690)
        self.gridLayout = QtGui.QGridLayout(TemplateDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblTimeTable = CPersonTimeTableView(TemplateDialog)
        self.tblTimeTable.setObjectName(_fromUtf8("tblTimeTable"))
        self.gridLayout.addWidget(self.tblTimeTable, 2, 0, 1, 8)
        self.cmbTimelinePeriod = QtGui.QComboBox(TemplateDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbTimelinePeriod.sizePolicy().hasHeightForWidth())
        self.cmbTimelinePeriod.setSizePolicy(sizePolicy)
        self.cmbTimelinePeriod.setObjectName(_fromUtf8("cmbTimelinePeriod"))
        self.cmbTimelinePeriod.addItem(_fromUtf8(""))
        self.cmbTimelinePeriod.addItem(_fromUtf8(""))
        self.cmbTimelinePeriod.addItem(_fromUtf8(""))
        self.cmbTimelinePeriod.addItem(_fromUtf8(""))
        self.cmbTimelinePeriod.addItem(_fromUtf8(""))
        self.cmbTimelinePeriod.addItem(_fromUtf8(""))
        self.cmbTimelinePeriod.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbTimelinePeriod, 1, 0, 1, 4)
        self.edtBegDate = CDateEdit(TemplateDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.lblEndDate = QtGui.QLabel(TemplateDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblEndDate.sizePolicy().hasHeightForWidth())
        self.lblEndDate.setSizePolicy(sizePolicy)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 0, 2, 1, 1)
        self.edtEndDate = CDateEdit(TemplateDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 0, 3, 1, 1)
        self.lblBegDate = QtGui.QLabel(TemplateDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblBegDate.sizePolicy().hasHeightForWidth())
        self.lblBegDate.setSizePolicy(sizePolicy)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(TemplateDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 8)
        self.chkRemoveExistingSchedules = QtGui.QCheckBox(TemplateDialog)
        self.chkRemoveExistingSchedules.setObjectName(_fromUtf8("chkRemoveExistingSchedules"))
        self.gridLayout.addWidget(self.chkRemoveExistingSchedules, 3, 0, 1, 8)
        self.edtTimelineCustomLength = QtGui.QSpinBox(TemplateDialog)
        self.edtTimelineCustomLength.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtTimelineCustomLength.sizePolicy().hasHeightForWidth())
        self.edtTimelineCustomLength.setSizePolicy(sizePolicy)
        self.edtTimelineCustomLength.setMinimum(3)
        self.edtTimelineCustomLength.setMaximum(31)
        self.edtTimelineCustomLength.setProperty("value", 3)
        self.edtTimelineCustomLength.setObjectName(_fromUtf8("edtTimelineCustomLength"))
        self.gridLayout.addWidget(self.edtTimelineCustomLength, 1, 5, 1, 1)
        self.lblTimelineCustomLength = QtGui.QLabel(TemplateDialog)
        self.lblTimelineCustomLength.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTimelineCustomLength.sizePolicy().hasHeightForWidth())
        self.lblTimelineCustomLength.setSizePolicy(sizePolicy)
        self.lblTimelineCustomLength.setObjectName(_fromUtf8("lblTimelineCustomLength"))
        self.gridLayout.addWidget(self.lblTimelineCustomLength, 1, 4, 1, 1)
        spacerItem = QtGui.QSpacerItem(449, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 4, 1, 4)
        self.chkFillRedDays = QtGui.QCheckBox(TemplateDialog)
        self.chkFillRedDays.setObjectName(_fromUtf8("chkFillRedDays"))
        self.gridLayout.addWidget(self.chkFillRedDays, 1, 6, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 7, 1, 1)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblTimelineCustomLength.setBuddy(self.edtTimelineCustomLength)

        self.retranslateUi(TemplateDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TemplateDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TemplateDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TemplateDialog)
        TemplateDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        TemplateDialog.setTabOrder(self.edtEndDate, self.cmbTimelinePeriod)
        TemplateDialog.setTabOrder(self.cmbTimelinePeriod, self.edtTimelineCustomLength)
        TemplateDialog.setTabOrder(self.edtTimelineCustomLength, self.chkFillRedDays)
        TemplateDialog.setTabOrder(self.chkFillRedDays, self.tblTimeTable)
        TemplateDialog.setTabOrder(self.tblTimeTable, self.chkRemoveExistingSchedules)
        TemplateDialog.setTabOrder(self.chkRemoveExistingSchedules, self.buttonBox)

    def retranslateUi(self, TemplateDialog):
        TemplateDialog.setWindowTitle(_translate("TemplateDialog", "Шаблон планировщика", None))
        self.cmbTimelinePeriod.setItemText(0, _translate("TemplateDialog", "Один план", None))
        self.cmbTimelinePeriod.setItemText(1, _translate("TemplateDialog", "Нечет/чет", None))
        self.cmbTimelinePeriod.setItemText(2, _translate("TemplateDialog", "Произвольный график", None))
        self.cmbTimelinePeriod.setItemText(3, _translate("TemplateDialog", "Одна неделя", None))
        self.cmbTimelinePeriod.setItemText(4, _translate("TemplateDialog", "Две недели", None))
        self.cmbTimelinePeriod.setItemText(5, _translate("TemplateDialog", "Три недели", None))
        self.cmbTimelinePeriod.setItemText(6, _translate("TemplateDialog", "Четыре недели", None))
        self.lblEndDate.setText(_translate("TemplateDialog", "&По", None))
        self.lblBegDate.setText(_translate("TemplateDialog", "В период &с", None))
        self.chkRemoveExistingSchedules.setText(_translate("TemplateDialog", "Удалить предыдущее расписание", None))
        self.lblTimelineCustomLength.setText(_translate("TemplateDialog", "длительность", None))
        self.chkFillRedDays.setText(_translate("TemplateDialog", "Заполнять выходные и праздничные дни", None))

from Timeline.PersonTimeTable import CPersonTimeTableView
from library.DateEdit import CDateEdit
