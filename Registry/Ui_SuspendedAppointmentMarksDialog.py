# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\SVN\Samson\UP_s11\client\Registry\SuspendedAppointmentMarksDialog.ui'
#
# Created: Mon Mar 22 10:46:49 2021
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

class Ui_SuspendedAppointmentMarksDialog(object):
    def setupUi(self, SuspendedAppointmentMarksDialog):
        SuspendedAppointmentMarksDialog.setObjectName(_fromUtf8("SuspendedAppointmentMarksDialog"))
        SuspendedAppointmentMarksDialog.resize(400, 381)
        self.gridLayout = QtGui.QGridLayout(SuspendedAppointmentMarksDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setHorizontalSpacing(5)
        self.gridLayout.setVerticalSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.chkProcessed = QtGui.QCheckBox(SuspendedAppointmentMarksDialog)
        self.chkProcessed.setText(_fromUtf8(""))
        self.chkProcessed.setObjectName(_fromUtf8("chkProcessed"))
        self.gridLayout.addWidget(self.chkProcessed, 0, 1, 1, 1)
        self.cmbNotified = QtGui.QComboBox(SuspendedAppointmentMarksDialog)
        self.cmbNotified.setObjectName(_fromUtf8("cmbNotified"))
        self.cmbNotified.addItem(_fromUtf8(""))
        self.cmbNotified.addItem(_fromUtf8(""))
        self.cmbNotified.addItem(_fromUtf8(""))
        self.cmbNotified.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbNotified, 1, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(SuspendedAppointmentMarksDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 3)
        self.edtNote = QtGui.QPlainTextEdit(SuspendedAppointmentMarksDialog)
        self.edtNote.setTabChangesFocus(True)
        self.edtNote.setObjectName(_fromUtf8("edtNote"))
        self.gridLayout.addWidget(self.edtNote, 5, 1, 3, 2)
        self.label = QtGui.QLabel(SuspendedAppointmentMarksDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.lblProcessed = QtGui.QLabel(SuspendedAppointmentMarksDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblProcessed.sizePolicy().hasHeightForWidth())
        self.lblProcessed.setSizePolicy(sizePolicy)
        self.lblProcessed.setObjectName(_fromUtf8("lblProcessed"))
        self.gridLayout.addWidget(self.lblProcessed, 0, 0, 1, 1)
        self.lblNote = QtGui.QLabel(SuspendedAppointmentMarksDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblNote.sizePolicy().hasHeightForWidth())
        self.lblNote.setSizePolicy(sizePolicy)
        self.lblNote.setMinimumSize(QtCore.QSize(0, 25))
        self.lblNote.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lblNote.setObjectName(_fromUtf8("lblNote"))
        self.gridLayout.addWidget(self.lblNote, 5, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 6, 0, 1, 1)
        self.cmbCancelVariant = CRBComboBox(SuspendedAppointmentMarksDialog)
        self.cmbCancelVariant.setObjectName(_fromUtf8("cmbCancelVariant"))
        self.gridLayout.addWidget(self.cmbCancelVariant, 2, 1, 1, 1)
        self.cmbOrgStructure = QtGui.QComboBox(SuspendedAppointmentMarksDialog)
        self.cmbOrgStructure.setEnabled(False)
        self.cmbOrgStructure.setEditable(False)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.cmbOrgStructure.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbOrgStructure, 3, 1, 1, 1)
        self.lblCancelVariant = QtGui.QLabel(SuspendedAppointmentMarksDialog)
        self.lblCancelVariant.setObjectName(_fromUtf8("lblCancelVariant"))
        self.gridLayout.addWidget(self.lblCancelVariant, 2, 0, 1, 1)
        self.lblOrgStructure = QtGui.QLabel(SuspendedAppointmentMarksDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 3, 0, 1, 1)
        self.label.setBuddy(self.cmbNotified)
        self.lblProcessed.setBuddy(self.chkProcessed)
        self.lblNote.setBuddy(self.edtNote)

        self.retranslateUi(SuspendedAppointmentMarksDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SuspendedAppointmentMarksDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SuspendedAppointmentMarksDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SuspendedAppointmentMarksDialog)
        SuspendedAppointmentMarksDialog.setTabOrder(self.chkProcessed, self.cmbNotified)
        SuspendedAppointmentMarksDialog.setTabOrder(self.cmbNotified, self.edtNote)
        SuspendedAppointmentMarksDialog.setTabOrder(self.edtNote, self.buttonBox)

    def retranslateUi(self, SuspendedAppointmentMarksDialog):
        SuspendedAppointmentMarksDialog.setWindowTitle(_translate("SuspendedAppointmentMarksDialog", "Dialog", None))
        self.cmbNotified.setItemText(0, _translate("SuspendedAppointmentMarksDialog", "Нет", None))
        self.cmbNotified.setItemText(1, _translate("SuspendedAppointmentMarksDialog", "По телефону", None))
        self.cmbNotified.setItemText(2, _translate("SuspendedAppointmentMarksDialog", "СМС", None))
        self.cmbNotified.setItemText(3, _translate("SuspendedAppointmentMarksDialog", "Эл.почтой", None))
        self.label.setText(_translate("SuspendedAppointmentMarksDialog", "&Извещён", None))
        self.lblProcessed.setText(_translate("SuspendedAppointmentMarksDialog", "&Отработан", None))
        self.lblNote.setText(_translate("SuspendedAppointmentMarksDialog", "&Примечание", None))
        self.cmbOrgStructure.setItemText(0, _translate("SuspendedAppointmentMarksDialog", "Регистратура", None))
        self.lblCancelVariant.setText(_translate("SuspendedAppointmentMarksDialog", "Поводы отмены", None))
        self.lblOrgStructure.setText(_translate("SuspendedAppointmentMarksDialog", "Источник заявки", None))

from library.crbcombobox import CRBComboBox
