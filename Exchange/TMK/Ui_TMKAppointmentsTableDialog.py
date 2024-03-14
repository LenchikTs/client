# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\SVN\Samson\UP_s11\client\Exchange\TMK\TMKAppointmentsTableDialog.ui'
#
# Created: Fri Mar 26 16:27:22 2021
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

class Ui_TMKAppointmentsTableDialog(object):
    def setupUi(self, TMKAppointmentsTableDialog):
        TMKAppointmentsTableDialog.setObjectName(_fromUtf8("TMKAppointmentsTableDialog"))
        TMKAppointmentsTableDialog.resize(716, 538)
        self.verticalLayout = QtGui.QVBoxLayout(TMKAppointmentsTableDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(TMKAppointmentsTableDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.lvDoctors = QtGui.QListView(TMKAppointmentsTableDialog)
        self.lvDoctors.setObjectName(_fromUtf8("lvDoctors"))
        self.verticalLayout.addWidget(self.lvDoctors)
        self.label_2 = QtGui.QLabel(TMKAppointmentsTableDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.tblAppointments = QtGui.QTableView(TMKAppointmentsTableDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.tblAppointments.sizePolicy().hasHeightForWidth())
        self.tblAppointments.setSizePolicy(sizePolicy)
        self.tblAppointments.setObjectName(_fromUtf8("tblAppointments"))
        self.verticalLayout.addWidget(self.tblAppointments)
        self.lblStatus = QtGui.QLabel(TMKAppointmentsTableDialog)
        self.lblStatus.setObjectName(_fromUtf8("lblStatus"))
        self.verticalLayout.addWidget(self.lblStatus)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btnUpdateList = QtGui.QPushButton(TMKAppointmentsTableDialog)
        self.btnUpdateList.setObjectName(_fromUtf8("btnUpdateList"))
        self.horizontalLayout_2.addWidget(self.btnUpdateList)
        self.btnSetWaitingList = QtGui.QPushButton(TMKAppointmentsTableDialog)
        self.btnSetWaitingList.setObjectName(_fromUtf8("btnSetWaitingList"))
        self.horizontalLayout_2.addWidget(self.btnSetWaitingList)
        self.btnSetAppointment = QtGui.QPushButton(TMKAppointmentsTableDialog)
        self.btnSetAppointment.setObjectName(_fromUtf8("btnSetAppointment"))
        self.horizontalLayout_2.addWidget(self.btnSetAppointment)
        self.btnClose = QtGui.QPushButton(TMKAppointmentsTableDialog)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.horizontalLayout_2.addWidget(self.btnClose)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(TMKAppointmentsTableDialog)
        QtCore.QMetaObject.connectSlotsByName(TMKAppointmentsTableDialog)

    def retranslateUi(self, TMKAppointmentsTableDialog):
        TMKAppointmentsTableDialog.setWindowTitle(_translate("TMKAppointmentsTableDialog", "Сервис Телемедицины", None))
        self.label.setText(_translate("TMKAppointmentsTableDialog", "Врач:", None))
        self.label_2.setText(_translate("TMKAppointmentsTableDialog", "Доступные талоны:", None))
        self.lblStatus.setText(_translate("TMKAppointmentsTableDialog", "Загрузка списка талонов...", None))
        self.btnUpdateList.setText(_translate("TMKAppointmentsTableDialog", "Обновить", None))
        self.btnSetWaitingList.setText(_translate("TMKAppointmentsTableDialog", "Отправить в лист ожидания", None))
        self.btnSetAppointment.setText(_translate("TMKAppointmentsTableDialog", "Записать", None))
        self.btnClose.setText(_translate("TMKAppointmentsTableDialog", "Закрыть", None))

