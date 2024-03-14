# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\projects\samson\UP_s11\client\Registry\RegistryExpertPrintDialog.ui'
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

class Ui_RegistryExpertPrintDialog(object):
    def setupUi(self, RegistryExpertPrintDialog):
        RegistryExpertPrintDialog.setObjectName(_fromUtf8("RegistryExpertPrintDialog"))
        RegistryExpertPrintDialog.resize(281, 296)
        RegistryExpertPrintDialog.setWindowTitle(_fromUtf8("Список документов ВУТ"))
        self.verticalLayout = QtGui.QVBoxLayout(RegistryExpertPrintDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lblShowCols = QtGui.QLabel(RegistryExpertPrintDialog)
        self.lblShowCols.setText(_fromUtf8("Отображать столбцы:"))
        self.lblShowCols.setObjectName(_fromUtf8("lblShowCols"))
        self.verticalLayout.addWidget(self.lblShowCols)
        self.btnBegDateStationary = QtGui.QCheckBox(RegistryExpertPrintDialog)
        self.btnBegDateStationary.setText(_fromUtf8("В стационаре \"С\""))
        self.btnBegDateStationary.setChecked(True)
        self.btnBegDateStationary.setObjectName(_fromUtf8("btnBegDateStationary"))
        self.verticalLayout.addWidget(self.btnBegDateStationary)
        self.btnEndDateStationary = QtGui.QCheckBox(RegistryExpertPrintDialog)
        self.btnEndDateStationary.setText(_fromUtf8("В стационаре \"По\""))
        self.btnEndDateStationary.setChecked(True)
        self.btnEndDateStationary.setObjectName(_fromUtf8("btnEndDateStationary"))
        self.verticalLayout.addWidget(self.btnEndDateStationary)
        self.btnBreak = QtGui.QCheckBox(RegistryExpertPrintDialog)
        self.btnBreak.setText(_fromUtf8("Нарушение режима"))
        self.btnBreak.setChecked(True)
        self.btnBreak.setObjectName(_fromUtf8("btnBreak"))
        self.verticalLayout.addWidget(self.btnBreak)
        self.btnBreakDate = QtGui.QCheckBox(RegistryExpertPrintDialog)
        self.btnBreakDate.setText(_fromUtf8("Дата нарушения режима"))
        self.btnBreakDate.setChecked(True)
        self.btnBreakDate.setObjectName(_fromUtf8("btnBreakDate"))
        self.verticalLayout.addWidget(self.btnBreakDate)
        self.btnResult = QtGui.QCheckBox(RegistryExpertPrintDialog)
        self.btnResult.setText(_fromUtf8("Результат"))
        self.btnResult.setChecked(True)
        self.btnResult.setObjectName(_fromUtf8("btnResult"))
        self.verticalLayout.addWidget(self.btnResult)
        self.btnResultDate = QtGui.QCheckBox(RegistryExpertPrintDialog)
        self.btnResultDate.setText(_fromUtf8("Дата результата - Приступить к работе"))
        self.btnResultDate.setChecked(True)
        self.btnResultDate.setObjectName(_fromUtf8("btnResultDate"))
        self.verticalLayout.addWidget(self.btnResultDate)
        self.btnResultOtherwiseDate = QtGui.QCheckBox(RegistryExpertPrintDialog)
        self.btnResultOtherwiseDate.setText(_fromUtf8("Дата результата - Иное"))
        self.btnResultOtherwiseDate.setChecked(True)
        self.btnResultOtherwiseDate.setObjectName(_fromUtf8("btnResultOtherwiseDate"))
        self.verticalLayout.addWidget(self.btnResultOtherwiseDate)
        self.btnNumberPermit = QtGui.QCheckBox(RegistryExpertPrintDialog)
        self.btnNumberPermit.setText(_fromUtf8("Номер путевки"))
        self.btnNumberPermit.setChecked(True)
        self.btnNumberPermit.setObjectName(_fromUtf8("btnNumberPermit"))
        self.verticalLayout.addWidget(self.btnNumberPermit)
        self.btnBegDatePermit = QtGui.QCheckBox(RegistryExpertPrintDialog)
        self.btnBegDatePermit.setText(_fromUtf8("Дата начала путевки"))
        self.btnBegDatePermit.setChecked(True)
        self.btnBegDatePermit.setObjectName(_fromUtf8("btnBegDatePermit"))
        self.verticalLayout.addWidget(self.btnBegDatePermit)
        self.btnEndDatePermit = QtGui.QCheckBox(RegistryExpertPrintDialog)
        self.btnEndDatePermit.setText(_fromUtf8("Дата окончания путевки"))
        self.btnEndDatePermit.setChecked(True)
        self.btnEndDatePermit.setObjectName(_fromUtf8("btnEndDatePermit"))
        self.verticalLayout.addWidget(self.btnEndDatePermit)
        self.btnDisability = QtGui.QCheckBox(RegistryExpertPrintDialog)
        self.btnDisability.setText(_fromUtf8("Инвалидность"))
        self.btnDisability.setChecked(True)
        self.btnDisability.setObjectName(_fromUtf8("btnDisability"))
        self.verticalLayout.addWidget(self.btnDisability)
        self.btnIssueDate = QtGui.QCheckBox(RegistryExpertPrintDialog)
        self.btnIssueDate.setChecked(True)
        self.btnIssueDate.setObjectName(_fromUtf8("btnIssueDate"))
        self.verticalLayout.addWidget(self.btnIssueDate)
        spacerItem = QtGui.QSpacerItem(20, 14, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(RegistryExpertPrintDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(RegistryExpertPrintDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RegistryExpertPrintDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RegistryExpertPrintDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(RegistryExpertPrintDialog)

    def retranslateUi(self, RegistryExpertPrintDialog):
        self.btnIssueDate.setText(_translate("RegistryExpertPrintDialog", "Дата выдачи документа", None))

