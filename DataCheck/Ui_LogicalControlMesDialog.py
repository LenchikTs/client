# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\DataCheck\LogicalControlMesDialog.ui'
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

class Ui_LogicalControlMesDialog(object):
    def setupUi(self, LogicalControlMesDialog):
        LogicalControlMesDialog.setObjectName(_fromUtf8("LogicalControlMesDialog"))
        LogicalControlMesDialog.resize(1113, 804)
        self.gridLayout = QtGui.QGridLayout(LogicalControlMesDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblBegin = QtGui.QLabel(LogicalControlMesDialog)
        self.lblBegin.setObjectName(_fromUtf8("lblBegin"))
        self.gridLayout.addWidget(self.lblBegin, 0, 0, 1, 1)
        self.dateBeginPeriod = CDateEdit(LogicalControlMesDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateBeginPeriod.sizePolicy().hasHeightForWidth())
        self.dateBeginPeriod.setSizePolicy(sizePolicy)
        self.dateBeginPeriod.setCalendarPopup(True)
        self.dateBeginPeriod.setObjectName(_fromUtf8("dateBeginPeriod"))
        self.gridLayout.addWidget(self.dateBeginPeriod, 0, 1, 1, 1)
        self.lblEnd = QtGui.QLabel(LogicalControlMesDialog)
        self.lblEnd.setObjectName(_fromUtf8("lblEnd"))
        self.gridLayout.addWidget(self.lblEnd, 0, 2, 1, 1)
        self.dateEndPeriod = CDateEdit(LogicalControlMesDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateEndPeriod.sizePolicy().hasHeightForWidth())
        self.dateEndPeriod.setSizePolicy(sizePolicy)
        self.dateEndPeriod.setCalendarPopup(True)
        self.dateEndPeriod.setObjectName(_fromUtf8("dateEndPeriod"))
        self.gridLayout.addWidget(self.dateEndPeriod, 0, 3, 1, 1)
        self.lblEventFeature = QtGui.QLabel(LogicalControlMesDialog)
        self.lblEventFeature.setObjectName(_fromUtf8("lblEventFeature"))
        self.gridLayout.addWidget(self.lblEventFeature, 0, 6, 1, 1)
        self.cmbEventFeature = QtGui.QComboBox(LogicalControlMesDialog)
        self.cmbEventFeature.setObjectName(_fromUtf8("cmbEventFeature"))
        self.cmbEventFeature.addItem(_fromUtf8(""))
        self.cmbEventFeature.addItem(_fromUtf8(""))
        self.cmbEventFeature.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbEventFeature, 0, 7, 1, 1)
        spacerItem = QtGui.QSpacerItem(42, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 8, 1, 1)
        self.lblOrgStructure = QtGui.QLabel(LogicalControlMesDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 3, 6, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(LogicalControlMesDialog)
        self.cmbOrgStructure.setEnabled(True)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 3, 7, 1, 2)
        self.lblSpeciality = QtGui.QLabel(LogicalControlMesDialog)
        self.lblSpeciality.setObjectName(_fromUtf8("lblSpeciality"))
        self.gridLayout.addWidget(self.lblSpeciality, 4, 6, 1, 1)
        self.cmbSpeciality = CRBComboBox(LogicalControlMesDialog)
        self.cmbSpeciality.setEnabled(True)
        self.cmbSpeciality.setObjectName(_fromUtf8("cmbSpeciality"))
        self.gridLayout.addWidget(self.cmbSpeciality, 4, 7, 1, 2)
        self.lblPersonal = QtGui.QLabel(LogicalControlMesDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblPersonal.sizePolicy().hasHeightForWidth())
        self.lblPersonal.setSizePolicy(sizePolicy)
        self.lblPersonal.setObjectName(_fromUtf8("lblPersonal"))
        self.gridLayout.addWidget(self.lblPersonal, 5, 6, 1, 1)
        self.cmbPerson = CPersonComboBoxEx(LogicalControlMesDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 5, 7, 1, 2)
        self.prbControlMes = CProgressBar(LogicalControlMesDialog)
        self.prbControlMes.setObjectName(_fromUtf8("prbControlMes"))
        self.gridLayout.addWidget(self.prbControlMes, 9, 0, 1, 9)
        self.listResultControlMes = CRemarkListWidget(LogicalControlMesDialog)
        self.listResultControlMes.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed|QtGui.QAbstractItemView.SelectedClicked)
        self.listResultControlMes.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listResultControlMes.setFlow(QtGui.QListView.TopToBottom)
        self.listResultControlMes.setObjectName(_fromUtf8("listResultControlMes"))
        self.gridLayout.addWidget(self.listResultControlMes, 10, 0, 1, 9)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.btnStartControl = QtGui.QPushButton(LogicalControlMesDialog)
        self.btnStartControl.setAutoDefault(True)
        self.btnStartControl.setObjectName(_fromUtf8("btnStartControl"))
        self.horizontalLayout_2.addWidget(self.btnStartControl)
        self.lblCountLine = QtGui.QLabel(LogicalControlMesDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCountLine.sizePolicy().hasHeightForWidth())
        self.lblCountLine.setSizePolicy(sizePolicy)
        self.lblCountLine.setText(_fromUtf8(""))
        self.lblCountLine.setAlignment(QtCore.Qt.AlignCenter)
        self.lblCountLine.setObjectName(_fromUtf8("lblCountLine"))
        self.horizontalLayout_2.addWidget(self.lblCountLine)
        self.btnEndControl = QtGui.QPushButton(LogicalControlMesDialog)
        self.btnEndControl.setAutoDefault(True)
        self.btnEndControl.setObjectName(_fromUtf8("btnEndControl"))
        self.horizontalLayout_2.addWidget(self.btnEndControl)
        self.gridLayout.addLayout(self.horizontalLayout_2, 11, 0, 1, 9)
        self.chkMes = QtGui.QCheckBox(LogicalControlMesDialog)
        self.chkMes.setObjectName(_fromUtf8("chkMes"))
        self.gridLayout.addWidget(self.chkMes, 8, 0, 1, 2)
        self.chkDuration = QtGui.QCheckBox(LogicalControlMesDialog)
        self.chkDuration.setObjectName(_fromUtf8("chkDuration"))
        self.gridLayout.addWidget(self.chkDuration, 8, 2, 1, 2)
        self.chkMKB = QtGui.QCheckBox(LogicalControlMesDialog)
        self.chkMKB.setObjectName(_fromUtf8("chkMKB"))
        self.gridLayout.addWidget(self.chkMKB, 8, 4, 1, 1)
        self.chkExecActions = QtGui.QCheckBox(LogicalControlMesDialog)
        self.chkExecActions.setObjectName(_fromUtf8("chkExecActions"))
        self.gridLayout.addWidget(self.chkExecActions, 8, 8, 1, 1)
        self.chkCountVisits = QtGui.QCheckBox(LogicalControlMesDialog)
        self.chkCountVisits.setObjectName(_fromUtf8("chkCountVisits"))
        self.gridLayout.addWidget(self.chkCountVisits, 8, 7, 1, 1)
        self.cmbMes = CMESComboBoxEx(LogicalControlMesDialog)
        self.cmbMes.setObjectName(_fromUtf8("cmbMes"))
        self.gridLayout.addWidget(self.cmbMes, 6, 2, 1, 7)
        self.lblMes = QtGui.QLabel(LogicalControlMesDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblMes.sizePolicy().hasHeightForWidth())
        self.lblMes.setSizePolicy(sizePolicy)
        self.lblMes.setObjectName(_fromUtf8("lblMes"))
        self.gridLayout.addWidget(self.lblMes, 6, 0, 1, 2)
        self.cmbEventPurpose = CRBComboBox(LogicalControlMesDialog)
        self.cmbEventPurpose.setObjectName(_fromUtf8("cmbEventPurpose"))
        self.gridLayout.addWidget(self.cmbEventPurpose, 3, 2, 1, 4)
        self.lblEventPurpose = QtGui.QLabel(LogicalControlMesDialog)
        self.lblEventPurpose.setObjectName(_fromUtf8("lblEventPurpose"))
        self.gridLayout.addWidget(self.lblEventPurpose, 3, 0, 1, 2)
        self.lblEventType = QtGui.QLabel(LogicalControlMesDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblEventType.sizePolicy().hasHeightForWidth())
        self.lblEventType.setSizePolicy(sizePolicy)
        self.lblEventType.setObjectName(_fromUtf8("lblEventType"))
        self.gridLayout.addWidget(self.lblEventType, 4, 0, 1, 2)
        self.cmbEventType = CRBComboBox(LogicalControlMesDialog)
        self.cmbEventType.setObjectName(_fromUtf8("cmbEventType"))
        self.gridLayout.addWidget(self.cmbEventType, 4, 2, 1, 4)
        self.cmbEventProfile = CRBComboBox(LogicalControlMesDialog)
        self.cmbEventProfile.setObjectName(_fromUtf8("cmbEventProfile"))
        self.gridLayout.addWidget(self.cmbEventProfile, 5, 2, 1, 4)
        self.lblEventProfile = QtGui.QLabel(LogicalControlMesDialog)
        self.lblEventProfile.setObjectName(_fromUtf8("lblEventProfile"))
        self.gridLayout.addWidget(self.lblEventProfile, 5, 0, 1, 2)
        self.cmbEventExec = QtGui.QComboBox(LogicalControlMesDialog)
        self.cmbEventExec.setObjectName(_fromUtf8("cmbEventExec"))
        self.cmbEventExec.addItem(_fromUtf8(""))
        self.cmbEventExec.addItem(_fromUtf8(""))
        self.cmbEventExec.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbEventExec, 0, 5, 1, 1)
        self.lblEventExec = QtGui.QLabel(LogicalControlMesDialog)
        self.lblEventExec.setObjectName(_fromUtf8("lblEventExec"))
        self.gridLayout.addWidget(self.lblEventExec, 0, 4, 1, 1)
        self.chkNotAlternative = QtGui.QCheckBox(LogicalControlMesDialog)
        self.chkNotAlternative.setObjectName(_fromUtf8("chkNotAlternative"))
        self.gridLayout.addWidget(self.chkNotAlternative, 8, 5, 1, 2)
        self.lblBegin.setBuddy(self.dateBeginPeriod)
        self.lblEnd.setBuddy(self.dateEndPeriod)
        self.lblSpeciality.setBuddy(self.cmbSpeciality)
        self.lblPersonal.setBuddy(self.cmbPerson)
        self.lblMes.setBuddy(self.cmbMes)
        self.lblEventType.setBuddy(self.cmbEventType)

        self.retranslateUi(LogicalControlMesDialog)
        QtCore.QMetaObject.connectSlotsByName(LogicalControlMesDialog)
        LogicalControlMesDialog.setTabOrder(self.dateBeginPeriod, self.dateEndPeriod)
        LogicalControlMesDialog.setTabOrder(self.dateEndPeriod, self.cmbEventFeature)
        LogicalControlMesDialog.setTabOrder(self.cmbEventFeature, self.cmbEventPurpose)
        LogicalControlMesDialog.setTabOrder(self.cmbEventPurpose, self.cmbEventType)
        LogicalControlMesDialog.setTabOrder(self.cmbEventType, self.cmbEventProfile)
        LogicalControlMesDialog.setTabOrder(self.cmbEventProfile, self.cmbMes)
        LogicalControlMesDialog.setTabOrder(self.cmbMes, self.cmbOrgStructure)
        LogicalControlMesDialog.setTabOrder(self.cmbOrgStructure, self.cmbSpeciality)
        LogicalControlMesDialog.setTabOrder(self.cmbSpeciality, self.cmbPerson)
        LogicalControlMesDialog.setTabOrder(self.cmbPerson, self.chkMes)
        LogicalControlMesDialog.setTabOrder(self.chkMes, self.chkDuration)
        LogicalControlMesDialog.setTabOrder(self.chkDuration, self.chkMKB)
        LogicalControlMesDialog.setTabOrder(self.chkMKB, self.chkCountVisits)
        LogicalControlMesDialog.setTabOrder(self.chkCountVisits, self.chkExecActions)
        LogicalControlMesDialog.setTabOrder(self.chkExecActions, self.listResultControlMes)
        LogicalControlMesDialog.setTabOrder(self.listResultControlMes, self.btnStartControl)
        LogicalControlMesDialog.setTabOrder(self.btnStartControl, self.btnEndControl)

    def retranslateUi(self, LogicalControlMesDialog):
        LogicalControlMesDialog.setWindowTitle(_translate("LogicalControlMesDialog", "Логический контроль событий с МЭС ", None))
        self.lblBegin.setText(_translate("LogicalControlMesDialog", "с   ", None))
        self.dateBeginPeriod.setDisplayFormat(_translate("LogicalControlMesDialog", "dd.MM.yyyy", None))
        self.lblEnd.setText(_translate("LogicalControlMesDialog", "  по    ", None))
        self.dateEndPeriod.setDisplayFormat(_translate("LogicalControlMesDialog", "dd.MM.yyyy", None))
        self.lblEventFeature.setText(_translate("LogicalControlMesDialog", "Особенности", None))
        self.cmbEventFeature.setItemText(0, _translate("LogicalControlMesDialog", "Не учитывать", None))
        self.cmbEventFeature.setItemText(1, _translate("LogicalControlMesDialog", "Только выполненные", None))
        self.cmbEventFeature.setItemText(2, _translate("LogicalControlMesDialog", "Только невыполненные", None))
        self.lblOrgStructure.setText(_translate("LogicalControlMesDialog", "Подразделение", None))
        self.lblSpeciality.setText(_translate("LogicalControlMesDialog", "&Специальность", None))
        self.cmbSpeciality.setWhatsThis(_translate("LogicalControlMesDialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None))
        self.lblPersonal.setText(_translate("LogicalControlMesDialog", "&Врач", None))
        self.prbControlMes.setFormat(_translate("LogicalControlMesDialog", "%p%", None))
        self.btnStartControl.setText(_translate("LogicalControlMesDialog", "начать выполнение", None))
        self.btnEndControl.setText(_translate("LogicalControlMesDialog", "прервать", None))
        self.chkMes.setText(_translate("LogicalControlMesDialog", "Наличие МЭС", None))
        self.chkDuration.setText(_translate("LogicalControlMesDialog", "Длительность события", None))
        self.chkMKB.setText(_translate("LogicalControlMesDialog", "Заключительный диагноз", None))
        self.chkExecActions.setText(_translate("LogicalControlMesDialog", "Наличие выполненных действий", None))
        self.chkCountVisits.setText(_translate("LogicalControlMesDialog", "Кол-во визитов", None))
        self.lblMes.setText(_translate("LogicalControlMesDialog", "МЭС", None))
        self.lblEventPurpose.setText(_translate("LogicalControlMesDialog", "Назначение события", None))
        self.lblEventType.setText(_translate("LogicalControlMesDialog", "Тип события", None))
        self.lblEventProfile.setText(_translate("LogicalControlMesDialog", "Профиль МЭС", None))
        self.cmbEventExec.setItemText(0, _translate("LogicalControlMesDialog", "Все", None))
        self.cmbEventExec.setItemText(1, _translate("LogicalControlMesDialog", "Законченные", None))
        self.cmbEventExec.setItemText(2, _translate("LogicalControlMesDialog", "Незаконченные", None))
        self.lblEventExec.setText(_translate("LogicalControlMesDialog", "Учитывать события", None))
        self.chkNotAlternative.setText(_translate("LogicalControlMesDialog", "Не выполнена альтернативность", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from RemarkListWidget import CRemarkListWidget
from library.DateEdit import CDateEdit
from library.MES.MESComboBoxEx import CMESComboBoxEx
from library.ProgressBar import CProgressBar
from library.crbcombobox import CRBComboBox
