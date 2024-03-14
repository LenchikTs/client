# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/Resources/GroupJobAppointmentDialog.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
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

class Ui_GroupJobAppointmentDialog(object):
    def setupUi(self, GroupJobAppointmentDialog):
        GroupJobAppointmentDialog.setObjectName(_fromUtf8("GroupJobAppointmentDialog"))
        GroupJobAppointmentDialog.resize(871, 796)
        self.gridLayout_5 = QtGui.QGridLayout(GroupJobAppointmentDialog)
        self.gridLayout_5.setMargin(4)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_3 = QtGui.QLabel(GroupJobAppointmentDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.cmbJobType = CRBComboBox(GroupJobAppointmentDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbJobType.sizePolicy().hasHeightForWidth())
        self.cmbJobType.setSizePolicy(sizePolicy)
        self.cmbJobType.setObjectName(_fromUtf8("cmbJobType"))
        self.cmbJobType.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.cmbJobType)
        self.label_6 = QtGui.QLabel(GroupJobAppointmentDialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_2.addWidget(self.label_6)
        self.cmbActionType = CActionTypeComboBoxEx(GroupJobAppointmentDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbActionType.sizePolicy().hasHeightForWidth())
        self.cmbActionType.setSizePolicy(sizePolicy)
        self.cmbActionType.setObjectName(_fromUtf8("cmbActionType"))
        self.cmbActionType.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.cmbActionType)
        self.label_7 = QtGui.QLabel(GroupJobAppointmentDialog)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout_2.addWidget(self.label_7)
        self.cmbOrgStructure = COrgStructureComboBox(GroupJobAppointmentDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbOrgStructure.sizePolicy().hasHeightForWidth())
        self.cmbOrgStructure.setSizePolicy(sizePolicy)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.cmbOrgStructure.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.cmbOrgStructure)
        self.gridLayout_5.addLayout(self.horizontalLayout_2, 0, 0, 1, 2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(GroupJobAppointmentDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.edtBegDate = CDateEdit(GroupJobAppointmentDialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.horizontalLayout.addWidget(self.edtBegDate)
        self.label_2 = QtGui.QLabel(GroupJobAppointmentDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.edtEndDate = CDateEdit(GroupJobAppointmentDialog)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.horizontalLayout.addWidget(self.edtEndDate)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout_5.addLayout(self.horizontalLayout, 1, 0, 1, 2)
        self.splitter_2 = QtGui.QSplitter(GroupJobAppointmentDialog)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.widget = QtGui.QWidget(self.splitter)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_4 = QtGui.QLabel(self.widget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.tblEvents = CTableView(self.widget)
        self.tblEvents.setObjectName(_fromUtf8("tblEvents"))
        self.gridLayout.addWidget(self.tblEvents, 1, 0, 1, 1)
        self.widget_2 = QtGui.QWidget(self.splitter)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.widget_2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_5 = QtGui.QLabel(self.widget_2)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.tblSchedule = CTableView(self.widget_2)
        self.tblSchedule.setObjectName(_fromUtf8("tblSchedule"))
        self.gridLayout_2.addWidget(self.tblSchedule, 1, 0, 1, 1)
        self.widget_3 = QtGui.QWidget(self.splitter_2)
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.gridLayout_3 = QtGui.QGridLayout(self.widget_3)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_8 = QtGui.QLabel(self.widget_3)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_3.addWidget(self.label_8, 0, 0, 1, 1)
        self.tblGroup = CInDocTableView(self.widget_3)
        self.tblGroup.setObjectName(_fromUtf8("tblGroup"))
        self.gridLayout_3.addWidget(self.tblGroup, 1, 0, 1, 1)
        self.widget_4 = QtGui.QWidget(self.splitter_2)
        self.widget_4.setObjectName(_fromUtf8("widget_4"))
        self.gridLayout_4 = QtGui.QGridLayout(self.widget_4)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_9 = QtGui.QLabel(self.widget_4)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_4.addWidget(self.label_9, 0, 0, 1, 1)
        self.tblActions = CTableView(self.widget_4)
        self.tblActions.setObjectName(_fromUtf8("tblActions"))
        self.gridLayout_4.addWidget(self.tblActions, 1, 0, 1, 1)
        self.gridLayout_5.addWidget(self.splitter_2, 2, 0, 1, 2)
        self.lblCountEvents = QtGui.QLabel(GroupJobAppointmentDialog)
        self.lblCountEvents.setObjectName(_fromUtf8("lblCountEvents"))
        self.gridLayout_5.addWidget(self.lblCountEvents, 3, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(GroupJobAppointmentDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_5.addWidget(self.buttonBox, 3, 1, 1, 1)

        self.retranslateUi(GroupJobAppointmentDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), GroupJobAppointmentDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), GroupJobAppointmentDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GroupJobAppointmentDialog)

    def retranslateUi(self, GroupJobAppointmentDialog):
        GroupJobAppointmentDialog.setWindowTitle(_translate("GroupJobAppointmentDialog", "Групповое назначение", None))
        self.label_3.setText(_translate("GroupJobAppointmentDialog", "Направление", None))
        self.cmbJobType.setItemText(0, _translate("GroupJobAppointmentDialog", "Тип работы", None))
        self.label_6.setText(_translate("GroupJobAppointmentDialog", "Назначение", None))
        self.cmbActionType.setItemText(0, _translate("GroupJobAppointmentDialog", "Тип действия", None))
        self.label_7.setText(_translate("GroupJobAppointmentDialog", "Подразделение", None))
        self.cmbOrgStructure.setItemText(0, _translate("GroupJobAppointmentDialog", "Подразделение", None))
        self.label.setText(_translate("GroupJobAppointmentDialog", "Период с", None))
        self.edtBegDate.setDisplayFormat(_translate("GroupJobAppointmentDialog", "dd.MM.yyyy", None))
        self.label_2.setText(_translate("GroupJobAppointmentDialog", "по", None))
        self.edtEndDate.setDisplayFormat(_translate("GroupJobAppointmentDialog", "dd.MM.yyyy", None))
        self.label_4.setText(_translate("GroupJobAppointmentDialog", "Контингент", None))
        self.label_5.setText(_translate("GroupJobAppointmentDialog", "Расписание", None))
        self.label_8.setText(_translate("GroupJobAppointmentDialog", "Группа", None))
        self.label_9.setText(_translate("GroupJobAppointmentDialog", "Назначение", None))
        self.lblCountEvents.setText(_translate("GroupJobAppointmentDialog", "Контингент всего: 0.  Контингент в группе: 0", None))

from Events.ActionTypeComboBoxEx import CActionTypeComboBoxEx
from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from library.DateEdit import CDateEdit
from library.InDocTable import CInDocTableView
from library.TableView import CTableView
from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    GroupJobAppointmentDialog = QtGui.QDialog()
    ui = Ui_GroupJobAppointmentDialog()
    ui.setupUi(GroupJobAppointmentDialog)
    GroupJobAppointmentDialog.show()
    sys.exit(app.exec_())

