# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Registry\VisitsBySchedules.ui'
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

class Ui_VisitsBySchedules(object):
    def setupUi(self, VisitsBySchedules):
        VisitsBySchedules.setObjectName(_fromUtf8("VisitsBySchedules"))
        VisitsBySchedules.resize(489, 553)
        self.gridLayout = QtGui.QGridLayout(VisitsBySchedules)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblBegDate = QtGui.QLabel(VisitsBySchedules)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblBegDate.sizePolicy().hasHeightForWidth())
        self.lblBegDate.setSizePolicy(sizePolicy)
        self.lblBegDate.setAlignment(QtCore.Qt.AlignCenter)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.edtBegDate = CDateEdit(VisitsBySchedules)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.lblEndDate = QtGui.QLabel(VisitsBySchedules)
        self.lblEndDate.setAlignment(QtCore.Qt.AlignCenter)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 0, 2, 1, 1)
        self.edtEndDate = CDateEdit(VisitsBySchedules)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtEndDate.sizePolicy().hasHeightForWidth())
        self.edtEndDate.setSizePolicy(sizePolicy)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 0, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(159, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 4, 1, 1)
        self.lblOrgStructure = QtGui.QLabel(VisitsBySchedules)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblOrgStructure.sizePolicy().hasHeightForWidth())
        self.lblOrgStructure.setSizePolicy(sizePolicy)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 1, 0, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(VisitsBySchedules)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 1, 1, 1, 4)
        self.lblSpeciality = QtGui.QLabel(VisitsBySchedules)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblSpeciality.sizePolicy().hasHeightForWidth())
        self.lblSpeciality.setSizePolicy(sizePolicy)
        self.lblSpeciality.setObjectName(_fromUtf8("lblSpeciality"))
        self.gridLayout.addWidget(self.lblSpeciality, 2, 0, 1, 1)
        self.cmbSpeciality = CRBComboBox(VisitsBySchedules)
        self.cmbSpeciality.setObjectName(_fromUtf8("cmbSpeciality"))
        self.gridLayout.addWidget(self.cmbSpeciality, 2, 1, 1, 4)
        self.lblPerson = QtGui.QLabel(VisitsBySchedules)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblPerson.sizePolicy().hasHeightForWidth())
        self.lblPerson.setSizePolicy(sizePolicy)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 3, 0, 1, 1)
        self.cmbPerson = CPersonComboBoxEx(VisitsBySchedules)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 3, 1, 1, 4)
        self.chkShowQueueWithoutVisit = QtGui.QCheckBox(VisitsBySchedules)
        self.chkShowQueueWithoutVisit.setObjectName(_fromUtf8("chkShowQueueWithoutVisit"))
        self.gridLayout.addWidget(self.chkShowQueueWithoutVisit, 4, 1, 1, 3)
        self.splitter = QtGui.QSplitter(VisitsBySchedules)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.txtClient = QtGui.QTextBrowser(self.splitter)
        self.txtClient.setObjectName(_fromUtf8("txtClient"))
        self.tblSchedules = CTableView(self.splitter)
        self.tblSchedules.setObjectName(_fromUtf8("tblSchedules"))
        self.gridLayout.addWidget(self.splitter, 5, 0, 1, 5)
        self.buttonBox = QtGui.QDialogButtonBox(VisitsBySchedules)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 5)
        self.lblBegDate.setBuddy(self.edtBegDate)
        self.lblEndDate.setBuddy(self.edtEndDate)
        self.lblOrgStructure.setBuddy(self.cmbOrgStructure)
        self.lblSpeciality.setBuddy(self.cmbSpeciality)
        self.lblPerson.setBuddy(self.cmbPerson)

        self.retranslateUi(VisitsBySchedules)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), VisitsBySchedules.close)
        QtCore.QMetaObject.connectSlotsByName(VisitsBySchedules)
        VisitsBySchedules.setTabOrder(self.edtBegDate, self.edtEndDate)
        VisitsBySchedules.setTabOrder(self.edtEndDate, self.cmbOrgStructure)
        VisitsBySchedules.setTabOrder(self.cmbOrgStructure, self.cmbSpeciality)
        VisitsBySchedules.setTabOrder(self.cmbSpeciality, self.cmbPerson)
        VisitsBySchedules.setTabOrder(self.cmbPerson, self.chkShowQueueWithoutVisit)
        VisitsBySchedules.setTabOrder(self.chkShowQueueWithoutVisit, self.txtClient)
        VisitsBySchedules.setTabOrder(self.txtClient, self.tblSchedules)

    def retranslateUi(self, VisitsBySchedules):
        VisitsBySchedules.setWindowTitle(_translate("VisitsBySchedules", "Протокол обращений пациента по предварительной записи", None))
        self.lblBegDate.setText(_translate("VisitsBySchedules", "С", None))
        self.edtBegDate.setDisplayFormat(_translate("VisitsBySchedules", "dd.MM.yyyy", None))
        self.lblEndDate.setText(_translate("VisitsBySchedules", "по", None))
        self.edtEndDate.setDisplayFormat(_translate("VisitsBySchedules", "dd.MM.yyyy", None))
        self.lblOrgStructure.setText(_translate("VisitsBySchedules", "&Подразделение", None))
        self.lblSpeciality.setText(_translate("VisitsBySchedules", "&Специальность", None))
        self.lblPerson.setText(_translate("VisitsBySchedules", "&Врач", None))
        self.chkShowQueueWithoutVisit.setText(_translate("VisitsBySchedules", "Показывать записи без о&бращения", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.DateEdit import CDateEdit
from library.TableView import CTableView
from library.crbcombobox import CRBComboBox
