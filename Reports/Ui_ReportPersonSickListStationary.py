# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client\Reports\ReportPersonSickListStationary.ui'
#
# Created: Fri Apr 26 11:12:17 2019
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_ReportPersonSickListStationary(object):
    def setupUi(self, ReportPersonSickListStationary):
        ReportPersonSickListStationary.setObjectName(_fromUtf8("ReportPersonSickListStationary"))
        ReportPersonSickListStationary.setWindowModality(QtCore.Qt.ApplicationModal)
        ReportPersonSickListStationary.resize(360, 179)
        ReportPersonSickListStationary.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(ReportPersonSickListStationary)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.frmAge = QtGui.QFrame(ReportPersonSickListStationary)
        self.frmAge.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmAge.setFrameShadow(QtGui.QFrame.Raised)
        self.frmAge.setObjectName(_fromUtf8("frmAge"))
        self.hboxlayout = QtGui.QHBoxLayout(self.frmAge)
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.gridLayout.addWidget(self.frmAge, 3, 1, 1, 5)
        self.frmMKB = QtGui.QFrame(ReportPersonSickListStationary)
        self.frmMKB.setFrameShape(QtGui.QFrame.NoFrame)
        self.frmMKB.setFrameShadow(QtGui.QFrame.Raised)
        self.frmMKB.setObjectName(_fromUtf8("frmMKB"))
        self.gridlayout = QtGui.QGridLayout(self.frmMKB)
        self.gridlayout.setMargin(0)
        self.gridlayout.setHorizontalSpacing(4)
        self.gridlayout.setVerticalSpacing(0)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.edtMKBFrom = CICDCodeEdit(self.frmMKB)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtMKBFrom.sizePolicy().hasHeightForWidth())
        self.edtMKBFrom.setSizePolicy(sizePolicy)
        self.edtMKBFrom.setMaximumSize(QtCore.QSize(40, 16777215))
        self.edtMKBFrom.setMaxLength(6)
        self.edtMKBFrom.setObjectName(_fromUtf8("edtMKBFrom"))
        self.gridlayout.addWidget(self.edtMKBFrom, 0, 0, 1, 1)
        self.edtMKBTo = CICDCodeEdit(self.frmMKB)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtMKBTo.sizePolicy().hasHeightForWidth())
        self.edtMKBTo.setSizePolicy(sizePolicy)
        self.edtMKBTo.setMaximumSize(QtCore.QSize(40, 16777215))
        self.edtMKBTo.setMaxLength(6)
        self.edtMKBTo.setObjectName(_fromUtf8("edtMKBTo"))
        self.gridlayout.addWidget(self.edtMKBTo, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.frmMKB, 4, 1, 1, 5)
        self.cmbOrgStructure = COrgStructureComboBox(ReportPersonSickListStationary)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 2, 1, 1, 5)
        self.lblBegDate = QtGui.QLabel(ReportPersonSickListStationary)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.edtEndDate = CDateEdit(ReportPersonSickListStationary)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 4, 1, 2)
        self.lblMKB = QtGui.QLabel(ReportPersonSickListStationary)
        self.lblMKB.setObjectName(_fromUtf8("lblMKB"))
        self.gridLayout.addWidget(self.lblMKB, 4, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ReportPersonSickListStationary)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 7, 0, 1, 6)
        spacerItem2 = QtGui.QSpacerItem(91, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 4, 1, 2)
        spacerItem3 = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 6, 0, 1, 1)
        self.lblTypeHospytal = QtGui.QLabel(ReportPersonSickListStationary)
        self.lblTypeHospytal.setObjectName(_fromUtf8("lblTypeHospytal"))
        self.gridLayout.addWidget(self.lblTypeHospytal, 5, 0, 1, 1)
        self.cmbTypeHospytal = QtGui.QComboBox(ReportPersonSickListStationary)
        self.cmbTypeHospytal.setObjectName(_fromUtf8("cmbTypeHospytal"))
        self.cmbTypeHospytal.addItem(_fromUtf8(""))
        self.cmbTypeHospytal.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbTypeHospytal, 5, 1, 1, 5)
        self.lblEndDate = QtGui.QLabel(ReportPersonSickListStationary)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.edtBegDate = CDateEdit(ReportPersonSickListStationary)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 2)
        self.lblOrgStructure = QtGui.QLabel(ReportPersonSickListStationary)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 2, 0, 1, 1)
        self.edtBegTime = QtGui.QTimeEdit(ReportPersonSickListStationary)
        self.edtBegTime.setObjectName(_fromUtf8("edtBegTime"))
        self.gridLayout.addWidget(self.edtBegTime, 0, 3, 1, 1)
        self.edtEndTime = QtGui.QTimeEdit(ReportPersonSickListStationary)
        self.edtEndTime.setObjectName(_fromUtf8("edtEndTime"))
        self.gridLayout.addWidget(self.edtEndTime, 1, 3, 1, 1)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblMKB.setBuddy(self.edtMKBFrom)
        self.lblTypeHospytal.setBuddy(self.cmbTypeHospytal)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)

        self.retranslateUi(ReportPersonSickListStationary)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportPersonSickListStationary.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportPersonSickListStationary.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportPersonSickListStationary)
        ReportPersonSickListStationary.setTabOrder(self.edtBegDate, self.edtEndDate)
        ReportPersonSickListStationary.setTabOrder(self.edtEndDate, self.cmbOrgStructure)
        ReportPersonSickListStationary.setTabOrder(self.cmbOrgStructure, self.edtMKBFrom)
        ReportPersonSickListStationary.setTabOrder(self.edtMKBFrom, self.edtMKBTo)
        ReportPersonSickListStationary.setTabOrder(self.edtMKBTo, self.cmbTypeHospytal)
        ReportPersonSickListStationary.setTabOrder(self.cmbTypeHospytal, self.buttonBox)

    def retranslateUi(self, ReportPersonSickListStationary):
        ReportPersonSickListStationary.setWindowTitle(_translate("ReportPersonSickListStationary", "параметры отчёта", None))
        self.edtMKBFrom.setInputMask(_translate("ReportPersonSickListStationary", "a00.00; ", None))
        self.edtMKBFrom.setText(_translate("ReportPersonSickListStationary", "A.", None))
        self.edtMKBTo.setInputMask(_translate("ReportPersonSickListStationary", "a00.00; ", None))
        self.edtMKBTo.setText(_translate("ReportPersonSickListStationary", "Z99.9", None))
        self.lblBegDate.setText(_translate("ReportPersonSickListStationary", "Дата &начала периода", None))
        self.edtEndDate.setDisplayFormat(_translate("ReportPersonSickListStationary", "dd.MM.yyyy", None))
        self.lblMKB.setText(_translate("ReportPersonSickListStationary", "Коды диагнозов по МКБ", None))
        self.lblTypeHospytal.setText(_translate("ReportPersonSickListStationary", "Тип помощи", None))
        self.cmbTypeHospytal.setItemText(0, _translate("ReportPersonSickListStationary", "Стационарно", None))
        self.cmbTypeHospytal.setItemText(1, _translate("ReportPersonSickListStationary", "Амбулаторно", None))
        self.lblEndDate.setText(_translate("ReportPersonSickListStationary", "Дата &окончания периода", None))
        self.edtBegDate.setDisplayFormat(_translate("ReportPersonSickListStationary", "dd.MM.yyyy", None))
        self.lblOrgStructure.setText(_translate("ReportPersonSickListStationary", "&Подразделение", None))

from library.ICDCodeEdit import CICDCodeEdit
from library.DateEdit import CDateEdit
from Orgs.OrgStructComboBoxes import COrgStructureComboBox