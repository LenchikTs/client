# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MultiplePersonEditor.ui'
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

class Ui_MultiplePersonEditorDialog(object):
    def setupUi(self, MultiplePersonEditorDialog):
        MultiplePersonEditorDialog.setObjectName(_fromUtf8("MultiplePersonEditorDialog"))
        MultiplePersonEditorDialog.setEnabled(True)
        MultiplePersonEditorDialog.resize(672, 449)
        self.gridLayout = QtGui.QGridLayout(MultiplePersonEditorDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.chkExternalQuota = QtGui.QCheckBox(MultiplePersonEditorDialog)
        self.chkExternalQuota.setObjectName(_fromUtf8("chkExternalQuota"))
        self.gridLayout.addWidget(self.chkExternalQuota, 9, 0, 1, 2)
        self.chkAvailableForSuspendedAppointment = QtGui.QCheckBox(MultiplePersonEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkAvailableForSuspendedAppointment.sizePolicy().hasHeightForWidth())
        self.chkAvailableForSuspendedAppointment.setSizePolicy(sizePolicy)
        self.chkAvailableForSuspendedAppointment.setObjectName(_fromUtf8("chkAvailableForSuspendedAppointment"))
        self.gridLayout.addWidget(self.chkAvailableForSuspendedAppointment, 2, 0, 1, 4)
        self.chkPrimaryQuota = QtGui.QCheckBox(MultiplePersonEditorDialog)
        self.chkPrimaryQuota.setObjectName(_fromUtf8("chkPrimaryQuota"))
        self.gridLayout.addWidget(self.chkPrimaryQuota, 6, 0, 1, 2)
        self.chkShowTypeTemplate = QtGui.QCheckBox(MultiplePersonEditorDialog)
        self.chkShowTypeTemplate.setObjectName(_fromUtf8("chkShowTypeTemplate"))
        self.gridLayout.addWidget(self.chkShowTypeTemplate, 10, 0, 1, 2)
        self.edtTimelineAccessibilityDays = QtGui.QSpinBox(MultiplePersonEditorDialog)
        self.edtTimelineAccessibilityDays.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtTimelineAccessibilityDays.sizePolicy().hasHeightForWidth())
        self.edtTimelineAccessibilityDays.setSizePolicy(sizePolicy)
        self.edtTimelineAccessibilityDays.setMaximumSize(QtCore.QSize(50, 16777215))
        self.edtTimelineAccessibilityDays.setSuffix(_fromUtf8(""))
        self.edtTimelineAccessibilityDays.setMaximum(999)
        self.edtTimelineAccessibilityDays.setObjectName(_fromUtf8("edtTimelineAccessibilityDays"))
        self.gridLayout.addWidget(self.edtTimelineAccessibilityDays, 5, 4, 1, 1)
        self.edtConsultancyQuota = QtGui.QSpinBox(MultiplePersonEditorDialog)
        self.edtConsultancyQuota.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtConsultancyQuota.sizePolicy().hasHeightForWidth())
        self.edtConsultancyQuota.setSizePolicy(sizePolicy)
        self.edtConsultancyQuota.setMaximum(100)
        self.edtConsultancyQuota.setObjectName(_fromUtf8("edtConsultancyQuota"))
        self.gridLayout.addWidget(self.edtConsultancyQuota, 8, 3, 1, 3)
        self.edtLastAccessibleTimelineDate = CDateEdit(MultiplePersonEditorDialog)
        self.edtLastAccessibleTimelineDate.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtLastAccessibleTimelineDate.sizePolicy().hasHeightForWidth())
        self.edtLastAccessibleTimelineDate.setSizePolicy(sizePolicy)
        self.edtLastAccessibleTimelineDate.setCalendarPopup(True)
        self.edtLastAccessibleTimelineDate.setObjectName(_fromUtf8("edtLastAccessibleTimelineDate"))
        self.gridLayout.addWidget(self.edtLastAccessibleTimelineDate, 4, 4, 1, 2)
        self.cmbUserRightsProfile = CDbComboBox(MultiplePersonEditorDialog)
        self.cmbUserRightsProfile.setEnabled(False)
        self.cmbUserRightsProfile.setObjectName(_fromUtf8("cmbUserRightsProfile"))
        self.gridLayout.addWidget(self.cmbUserRightsProfile, 0, 1, 1, 5)
        self.chkTimelineAccessibilityDays = QtGui.QCheckBox(MultiplePersonEditorDialog)
        self.chkTimelineAccessibilityDays.setObjectName(_fromUtf8("chkTimelineAccessibilityDays"))
        self.gridLayout.addWidget(self.chkTimelineAccessibilityDays, 5, 0, 1, 2)
        self.cmbShowTypeTemplate = QtGui.QComboBox(MultiplePersonEditorDialog)
        self.cmbShowTypeTemplate.setEnabled(False)
        self.cmbShowTypeTemplate.setObjectName(_fromUtf8("cmbShowTypeTemplate"))
        self.cmbShowTypeTemplate.addItem(_fromUtf8(""))
        self.cmbShowTypeTemplate.addItem(_fromUtf8(""))
        self.cmbShowTypeTemplate.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbShowTypeTemplate, 10, 2, 1, 4)
        self.edtOwnQuota = QtGui.QSpinBox(MultiplePersonEditorDialog)
        self.edtOwnQuota.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtOwnQuota.sizePolicy().hasHeightForWidth())
        self.edtOwnQuota.setSizePolicy(sizePolicy)
        self.edtOwnQuota.setMaximum(100)
        self.edtOwnQuota.setObjectName(_fromUtf8("edtOwnQuota"))
        self.gridLayout.addWidget(self.edtOwnQuota, 7, 3, 1, 3)
        self.edtPrimaryQuota = QtGui.QSpinBox(MultiplePersonEditorDialog)
        self.edtPrimaryQuota.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtPrimaryQuota.sizePolicy().hasHeightForWidth())
        self.edtPrimaryQuota.setSizePolicy(sizePolicy)
        self.edtPrimaryQuota.setMaximum(100)
        self.edtPrimaryQuota.setObjectName(_fromUtf8("edtPrimaryQuota"))
        self.gridLayout.addWidget(self.edtPrimaryQuota, 6, 3, 1, 3)
        self.chkAvailableForExternal = QtGui.QCheckBox(MultiplePersonEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkAvailableForExternal.sizePolicy().hasHeightForWidth())
        self.chkAvailableForExternal.setSizePolicy(sizePolicy)
        self.chkAvailableForExternal.setObjectName(_fromUtf8("chkAvailableForExternal"))
        self.gridLayout.addWidget(self.chkAvailableForExternal, 1, 0, 1, 3)
        self.cmbAvailableForSuspendedAppointment = QtGui.QComboBox(MultiplePersonEditorDialog)
        self.cmbAvailableForSuspendedAppointment.setEnabled(False)
        self.cmbAvailableForSuspendedAppointment.setObjectName(_fromUtf8("cmbAvailableForSuspendedAppointment"))
        self.cmbAvailableForSuspendedAppointment.addItem(_fromUtf8(""))
        self.cmbAvailableForSuspendedAppointment.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbAvailableForSuspendedAppointment, 2, 4, 1, 2)
        self.chkConsultancyQuota = QtGui.QCheckBox(MultiplePersonEditorDialog)
        self.chkConsultancyQuota.setObjectName(_fromUtf8("chkConsultancyQuota"))
        self.gridLayout.addWidget(self.chkConsultancyQuota, 8, 0, 1, 2)
        self.chkLastAccessibleTimelineDate = QtGui.QCheckBox(MultiplePersonEditorDialog)
        self.chkLastAccessibleTimelineDate.setObjectName(_fromUtf8("chkLastAccessibleTimelineDate"))
        self.gridLayout.addWidget(self.chkLastAccessibleTimelineDate, 4, 0, 1, 2)
        self.lblTimelineAccessibilityDaysSuffix = QtGui.QLabel(MultiplePersonEditorDialog)
        self.lblTimelineAccessibilityDaysSuffix.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTimelineAccessibilityDaysSuffix.sizePolicy().hasHeightForWidth())
        self.lblTimelineAccessibilityDaysSuffix.setSizePolicy(sizePolicy)
        self.lblTimelineAccessibilityDaysSuffix.setObjectName(_fromUtf8("lblTimelineAccessibilityDaysSuffix"))
        self.gridLayout.addWidget(self.lblTimelineAccessibilityDaysSuffix, 5, 5, 1, 1)
        self.chkUserRightsProfile = QtGui.QCheckBox(MultiplePersonEditorDialog)
        self.chkUserRightsProfile.setObjectName(_fromUtf8("chkUserRightsProfile"))
        self.gridLayout.addWidget(self.chkUserRightsProfile, 0, 0, 1, 1)
        self.chkAvailableForStand = QtGui.QCheckBox(MultiplePersonEditorDialog)
        self.chkAvailableForStand.setChecked(False)
        self.chkAvailableForStand.setObjectName(_fromUtf8("chkAvailableForStand"))
        self.gridLayout.addWidget(self.chkAvailableForStand, 3, 0, 1, 3)
        self.buttonBox = QtGui.QDialogButtonBox(MultiplePersonEditorDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 12, 0, 1, 6)
        self.edtExternalQuota = QtGui.QSpinBox(MultiplePersonEditorDialog)
        self.edtExternalQuota.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtExternalQuota.sizePolicy().hasHeightForWidth())
        self.edtExternalQuota.setSizePolicy(sizePolicy)
        self.edtExternalQuota.setMaximum(100)
        self.edtExternalQuota.setObjectName(_fromUtf8("edtExternalQuota"))
        self.gridLayout.addWidget(self.edtExternalQuota, 9, 3, 1, 3)
        self.cmbAvailableForStand = QtGui.QComboBox(MultiplePersonEditorDialog)
        self.cmbAvailableForStand.setEnabled(False)
        self.cmbAvailableForStand.setObjectName(_fromUtf8("cmbAvailableForStand"))
        self.cmbAvailableForStand.addItem(_fromUtf8(""))
        self.cmbAvailableForStand.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbAvailableForStand, 3, 4, 1, 2)
        self.cmbAvailableForExternal = QtGui.QComboBox(MultiplePersonEditorDialog)
        self.cmbAvailableForExternal.setEnabled(False)
        self.cmbAvailableForExternal.setObjectName(_fromUtf8("cmbAvailableForExternal"))
        self.cmbAvailableForExternal.addItem(_fromUtf8(""))
        self.cmbAvailableForExternal.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbAvailableForExternal, 1, 4, 1, 2)
        self.chkOwnQuota = QtGui.QCheckBox(MultiplePersonEditorDialog)
        self.chkOwnQuota.setObjectName(_fromUtf8("chkOwnQuota"))
        self.gridLayout.addWidget(self.chkOwnQuota, 7, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 11, 0, 1, 6)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 4, 2, 6, 1)

        self.retranslateUi(MultiplePersonEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), MultiplePersonEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), MultiplePersonEditorDialog.reject)
        QtCore.QObject.connect(self.chkUserRightsProfile, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbUserRightsProfile.setEnabled)
        QtCore.QObject.connect(self.chkAvailableForExternal, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbAvailableForExternal.setEnabled)
        QtCore.QObject.connect(self.chkAvailableForSuspendedAppointment, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbAvailableForSuspendedAppointment.setEnabled)
        QtCore.QObject.connect(self.chkAvailableForStand, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbAvailableForStand.setEnabled)
        QtCore.QObject.connect(self.chkLastAccessibleTimelineDate, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtLastAccessibleTimelineDate.setEnabled)
        QtCore.QObject.connect(self.chkTimelineAccessibilityDays, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtTimelineAccessibilityDays.setEnabled)
        QtCore.QObject.connect(self.chkPrimaryQuota, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtPrimaryQuota.setEnabled)
        QtCore.QObject.connect(self.chkOwnQuota, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtOwnQuota.setEnabled)
        QtCore.QObject.connect(self.chkConsultancyQuota, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtConsultancyQuota.setEnabled)
        QtCore.QObject.connect(self.chkExternalQuota, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtExternalQuota.setEnabled)
        QtCore.QObject.connect(self.chkShowTypeTemplate, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbShowTypeTemplate.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(MultiplePersonEditorDialog)

    def retranslateUi(self, MultiplePersonEditorDialog):
        MultiplePersonEditorDialog.setWindowTitle(_translate("MultiplePersonEditorDialog", "Сотрудники: групповой редактор", None))
        self.chkExternalQuota.setText(_translate("MultiplePersonEditorDialog", "Внешняя квота", None))
        self.chkAvailableForSuspendedAppointment.setText(_translate("MultiplePersonEditorDialog", "Сотрудник доступен для постановки в ЖОЗ внешними системами", None))
        self.chkPrimaryQuota.setText(_translate("MultiplePersonEditorDialog", "Первичная квота", None))
        self.chkShowTypeTemplate.setText(_translate("MultiplePersonEditorDialog", "Фильтрация шаблонов", None))
        self.edtTimelineAccessibilityDays.setToolTip(_translate("MultiplePersonEditorDialog", "Если это поле заполнено (не 0),\n"
"то указанная значение используется как количество дней начиная с текущего на которые видно расписание.", None))
        self.edtConsultancyQuota.setToolTip(_translate("MultiplePersonEditorDialog", "Доля (%) амбулаторного приёма, доступная для записи другим врачам", None))
        self.edtLastAccessibleTimelineDate.setToolTip(_translate("MultiplePersonEditorDialog", "Если это поле заполнено,\n"
"то указанная дата используется как предельная дата до которой видно расписание.", None))
        self.chkTimelineAccessibilityDays.setText(_translate("MultiplePersonEditorDialog", "Расписание видимо на", None))
        self.cmbShowTypeTemplate.setItemText(0, _translate("MultiplePersonEditorDialog", "показывать все доступные шаблоны", None))
        self.cmbShowTypeTemplate.setItemText(1, _translate("MultiplePersonEditorDialog", "показывать шаблоны текущего пользователя", None))
        self.cmbShowTypeTemplate.setItemText(2, _translate("MultiplePersonEditorDialog", "показывать шаблоны со СНИЛС текущего пользователя", None))
        self.edtOwnQuota.setToolTip(_translate("MultiplePersonEditorDialog", "Доля (%) амбулаторного приёма, доступная для записи самому врачу", None))
        self.edtPrimaryQuota.setToolTip(_translate("MultiplePersonEditorDialog", "Доля (%) амбулаторного приёма, доступная для записи из регистратуры", None))
        self.chkAvailableForExternal.setText(_translate("MultiplePersonEditorDialog", "Информация о сотруднике доступна для внешних систем", None))
        self.cmbAvailableForSuspendedAppointment.setItemText(0, _translate("MultiplePersonEditorDialog", "Нет", None))
        self.cmbAvailableForSuspendedAppointment.setItemText(1, _translate("MultiplePersonEditorDialog", "Да", None))
        self.chkConsultancyQuota.setText(_translate("MultiplePersonEditorDialog", "Консультативная квота", None))
        self.chkLastAccessibleTimelineDate.setText(_translate("MultiplePersonEditorDialog", "Расписание видимо до", None))
        self.lblTimelineAccessibilityDaysSuffix.setText(_translate("MultiplePersonEditorDialog", "дней", None))
        self.chkUserRightsProfile.setText(_translate("MultiplePersonEditorDialog", "Профиль прав", None))
        self.chkAvailableForStand.setToolTip(_translate("MultiplePersonEditorDialog", "Информация о сотруднике доступна для стендового расписания", None))
        self.chkAvailableForStand.setText(_translate("MultiplePersonEditorDialog", "Информация о сотруднике доступна для стендового расписания", None))
        self.edtExternalQuota.setToolTip(_translate("MultiplePersonEditorDialog", "Доля (%) амбулаторного приёма, доступная для записи из внешних систем", None))
        self.cmbAvailableForStand.setItemText(0, _translate("MultiplePersonEditorDialog", "Нет", None))
        self.cmbAvailableForStand.setItemText(1, _translate("MultiplePersonEditorDialog", "Да", None))
        self.cmbAvailableForExternal.setItemText(0, _translate("MultiplePersonEditorDialog", "Нет", None))
        self.cmbAvailableForExternal.setItemText(1, _translate("MultiplePersonEditorDialog", "Да", None))
        self.chkOwnQuota.setText(_translate("MultiplePersonEditorDialog", "Врачебная квота", None))

from library.DateEdit import CDateEdit
from library.DbComboBox import CDbComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MultiplePersonEditorDialog = QtGui.QDialog()
    ui = Ui_MultiplePersonEditorDialog()
    ui.setupUi(MultiplePersonEditorDialog)
    MultiplePersonEditorDialog.show()
    sys.exit(app.exec_())

