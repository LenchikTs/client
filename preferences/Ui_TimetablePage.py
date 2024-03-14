# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_merge\preferences\TimetablePage.ui'
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

class Ui_timetablePage(object):
    def setupUi(self, timetablePage):
        timetablePage.setObjectName(_fromUtf8("timetablePage"))
        timetablePage.resize(716, 171)
        timetablePage.setToolTip(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(timetablePage)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblCombineTimetable = QtGui.QLabel(timetablePage)
        self.lblCombineTimetable.setObjectName(_fromUtf8("lblCombineTimetable"))
        self.gridLayout.addWidget(self.lblCombineTimetable, 3, 0, 1, 1)
        self.lblSyncCheckableAndInvitiation = QtGui.QLabel(timetablePage)
        self.lblSyncCheckableAndInvitiation.setObjectName(_fromUtf8("lblSyncCheckableAndInvitiation"))
        self.gridLayout.addWidget(self.lblSyncCheckableAndInvitiation, 2, 0, 1, 1)
        self.chkSyncCheckableAndInvitiation = QtGui.QCheckBox(timetablePage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkSyncCheckableAndInvitiation.sizePolicy().hasHeightForWidth())
        self.chkSyncCheckableAndInvitiation.setSizePolicy(sizePolicy)
        self.chkSyncCheckableAndInvitiation.setText(_fromUtf8(""))
        self.chkSyncCheckableAndInvitiation.setObjectName(_fromUtf8("chkSyncCheckableAndInvitiation"))
        self.gridLayout.addWidget(self.chkSyncCheckableAndInvitiation, 2, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(153, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 2, 1, 1)
        self.lblAmbulanceUserCheckable = QtGui.QLabel(timetablePage)
        self.lblAmbulanceUserCheckable.setObjectName(_fromUtf8("lblAmbulanceUserCheckable"))
        self.gridLayout.addWidget(self.lblAmbulanceUserCheckable, 1, 0, 1, 1)
        self.chkAmbulanceUserCheckable = QtGui.QCheckBox(timetablePage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkAmbulanceUserCheckable.sizePolicy().hasHeightForWidth())
        self.chkAmbulanceUserCheckable.setSizePolicy(sizePolicy)
        self.chkAmbulanceUserCheckable.setText(_fromUtf8(""))
        self.chkAmbulanceUserCheckable.setObjectName(_fromUtf8("chkAmbulanceUserCheckable"))
        self.gridLayout.addWidget(self.chkAmbulanceUserCheckable, 1, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(153, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 1)
        self.lblDoubleClickQueuePerson = QtGui.QLabel(timetablePage)
        self.lblDoubleClickQueuePerson.setObjectName(_fromUtf8("lblDoubleClickQueuePerson"))
        self.gridLayout.addWidget(self.lblDoubleClickQueuePerson, 0, 0, 1, 1)
        self.cmbDoubleClickQueuePerson = QtGui.QComboBox(timetablePage)
        self.cmbDoubleClickQueuePerson.setObjectName(_fromUtf8("cmbDoubleClickQueuePerson"))
        self.cmbDoubleClickQueuePerson.addItem(_fromUtf8(""))
        self.cmbDoubleClickQueuePerson.addItem(_fromUtf8(""))
        self.cmbDoubleClickQueuePerson.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbDoubleClickQueuePerson, 0, 1, 1, 2)
        self.cmbCombineTimetable = QtGui.QComboBox(timetablePage)
        self.cmbCombineTimetable.setObjectName(_fromUtf8("cmbCombineTimetable"))
        self.cmbCombineTimetable.addItem(_fromUtf8(""))
        self.cmbCombineTimetable.addItem(_fromUtf8(""))
        self.cmbCombineTimetable.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbCombineTimetable, 3, 1, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(20, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 4, 0, 1, 1)
        self.lblSyncCheckableAndInvitiation.setBuddy(self.chkSyncCheckableAndInvitiation)
        self.lblAmbulanceUserCheckable.setBuddy(self.chkAmbulanceUserCheckable)
        self.lblDoubleClickQueuePerson.setBuddy(self.cmbDoubleClickQueuePerson)

        self.retranslateUi(timetablePage)
        self.cmbCombineTimetable.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(timetablePage)
        timetablePage.setTabOrder(self.cmbDoubleClickQueuePerson, self.chkAmbulanceUserCheckable)
        timetablePage.setTabOrder(self.chkAmbulanceUserCheckable, self.chkSyncCheckableAndInvitiation)

    def retranslateUi(self, timetablePage):
        timetablePage.setWindowTitle(_translate("timetablePage", "Панель «График»", None))
        self.lblCombineTimetable.setText(_translate("timetablePage", "Объединять листы предварительной записи для выбранных суток", None))
        self.lblSyncCheckableAndInvitiation.setText(_translate("timetablePage", "Синхронизировать подтверждение с приглашением", None))
        self.lblAmbulanceUserCheckable.setText(_translate("timetablePage", "Показывать подтверждение записей амбулаторного приема", None))
        self.lblDoubleClickQueuePerson.setText(_translate("timetablePage", "Двойной щелчок в листе предварительной записи врача", None))
        self.cmbDoubleClickQueuePerson.setItemText(0, _translate("timetablePage", "Изменить жалобы/примечания", None))
        self.cmbDoubleClickQueuePerson.setItemText(1, _translate("timetablePage", "Перейти в картотеку", None))
        self.cmbDoubleClickQueuePerson.setItemText(2, _translate("timetablePage", "Новое обращение", None))
        self.cmbCombineTimetable.setItemText(0, _translate("timetablePage", "Нет", None))
        self.cmbCombineTimetable.setItemText(1, _translate("timetablePage", "По назначению приёма", None))
        self.cmbCombineTimetable.setItemText(2, _translate("timetablePage", "Все", None))

