# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Correct\CorrectWidget.ui'
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(723, 521)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.chkPropertyName = QtGui.QCheckBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkPropertyName.sizePolicy().hasHeightForWidth())
        self.chkPropertyName.setSizePolicy(sizePolicy)
        self.chkPropertyName.setObjectName(_fromUtf8("chkPropertyName"))
        self.gridLayout.addWidget(self.chkPropertyName, 1, 0, 1, 1)
        self.edtSourcePropertyName = QtGui.QLineEdit(Form)
        self.edtSourcePropertyName.setEnabled(False)
        self.edtSourcePropertyName.setObjectName(_fromUtf8("edtSourcePropertyName"))
        self.gridLayout.addWidget(self.edtSourcePropertyName, 1, 1, 1, 1)
        self.lblSourceTypeName = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblSourceTypeName.sizePolicy().hasHeightForWidth())
        self.lblSourceTypeName.setSizePolicy(sizePolicy)
        self.lblSourceTypeName.setObjectName(_fromUtf8("lblSourceTypeName"))
        self.gridLayout.addWidget(self.lblSourceTypeName, 2, 0, 1, 1)
        self.cmbSourceTypeName = QtGui.QComboBox(Form)
        self.cmbSourceTypeName.setObjectName(_fromUtf8("cmbSourceTypeName"))
        self.gridLayout.addWidget(self.cmbSourceTypeName, 2, 1, 1, 1)
        self.lblTargetTypeName = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTargetTypeName.sizePolicy().hasHeightForWidth())
        self.lblTargetTypeName.setSizePolicy(sizePolicy)
        self.lblTargetTypeName.setObjectName(_fromUtf8("lblTargetTypeName"))
        self.gridLayout.addWidget(self.lblTargetTypeName, 2, 2, 1, 1)
        self.cmbTargetTypeName = QtGui.QComboBox(Form)
        self.cmbTargetTypeName.setObjectName(_fromUtf8("cmbTargetTypeName"))
        self.gridLayout.addWidget(self.cmbTargetTypeName, 2, 3, 1, 1)
        self.edtLog = QtGui.QTextEdit(Form)
        self.edtLog.setReadOnly(True)
        self.edtLog.setObjectName(_fromUtf8("edtLog"))
        self.gridLayout.addWidget(self.edtLog, 5, 0, 1, 4)
        self.btnDataAnalysis = QtGui.QPushButton(Form)
        self.btnDataAnalysis.setObjectName(_fromUtf8("btnDataAnalysis"))
        self.gridLayout.addWidget(self.btnDataAnalysis, 6, 0, 1, 2)
        self.btnStart = QtGui.QPushButton(Form)
        self.btnStart.setEnabled(False)
        self.btnStart.setObjectName(_fromUtf8("btnStart"))
        self.gridLayout.addWidget(self.btnStart, 6, 2, 1, 1)
        self.btnReset = QtGui.QPushButton(Form)
        self.btnReset.setEnabled(True)
        self.btnReset.setObjectName(_fromUtf8("btnReset"))
        self.gridLayout.addWidget(self.btnReset, 6, 3, 1, 1)
        self.lblTargetPropertyName = QtGui.QLabel(Form)
        self.lblTargetPropertyName.setObjectName(_fromUtf8("lblTargetPropertyName"))
        self.gridLayout.addWidget(self.lblTargetPropertyName, 1, 2, 1, 1)
        self.edtTargetPropertyName = QtGui.QLineEdit(Form)
        self.edtTargetPropertyName.setEnabled(False)
        self.edtTargetPropertyName.setObjectName(_fromUtf8("edtTargetPropertyName"))
        self.gridLayout.addWidget(self.edtTargetPropertyName, 1, 3, 1, 1)
        self.chkActionType = QtGui.QCheckBox(Form)
        self.chkActionType.setObjectName(_fromUtf8("chkActionType"))
        self.gridLayout.addWidget(self.chkActionType, 0, 0, 1, 1)
        self.cmbActionType = CActionTypeComboBox(Form)
        self.cmbActionType.setEnabled(False)
        self.cmbActionType.setObjectName(_fromUtf8("cmbActionType"))
        self.gridLayout.addWidget(self.cmbActionType, 0, 1, 1, 1)
        self.chkDeleteSource = QtGui.QCheckBox(Form)
        self.chkDeleteSource.setChecked(True)
        self.chkDeleteSource.setObjectName(_fromUtf8("chkDeleteSource"))
        self.gridLayout.addWidget(self.chkDeleteSource, 3, 0, 1, 1)
        self.chkFullReport = QtGui.QCheckBox(Form)
        self.chkFullReport.setObjectName(_fromUtf8("chkFullReport"))
        self.gridLayout.addWidget(self.chkFullReport, 4, 0, 1, 1)
        self.chkDeletingAutoStart = QtGui.QCheckBox(Form)
        self.chkDeletingAutoStart.setEnabled(True)
        self.chkDeletingAutoStart.setObjectName(_fromUtf8("chkDeletingAutoStart"))
        self.gridLayout.addWidget(self.chkDeletingAutoStart, 3, 1, 1, 1)
        self._progressBar = CProgressBar(Form)
        self._progressBar.setProperty("value", 24)
        self._progressBar.setObjectName(_fromUtf8("_progressBar"))
        self.gridLayout.addWidget(self._progressBar, 7, 0, 1, 4)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.chkPropertyName, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtSourcePropertyName.setEnabled)
        QtCore.QObject.connect(self.chkPropertyName, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtTargetPropertyName.setEnabled)
        QtCore.QObject.connect(self.chkActionType, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbActionType.setEnabled)
        QtCore.QObject.connect(self.chkDeleteSource, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.chkDeletingAutoStart.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.chkActionType, self.cmbActionType)
        Form.setTabOrder(self.cmbActionType, self.chkPropertyName)
        Form.setTabOrder(self.chkPropertyName, self.edtSourcePropertyName)
        Form.setTabOrder(self.edtSourcePropertyName, self.edtTargetPropertyName)
        Form.setTabOrder(self.edtTargetPropertyName, self.cmbSourceTypeName)
        Form.setTabOrder(self.cmbSourceTypeName, self.cmbTargetTypeName)
        Form.setTabOrder(self.cmbTargetTypeName, self.chkDeleteSource)
        Form.setTabOrder(self.chkDeleteSource, self.chkDeletingAutoStart)
        Form.setTabOrder(self.chkDeletingAutoStart, self.chkFullReport)
        Form.setTabOrder(self.chkFullReport, self.edtLog)
        Form.setTabOrder(self.edtLog, self.btnDataAnalysis)
        Form.setTabOrder(self.btnDataAnalysis, self.btnStart)
        Form.setTabOrder(self.btnStart, self.btnReset)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.chkPropertyName.setText(_translate("Form", "Наименование. Исходное свойство", None))
        self.lblSourceTypeName.setText(_translate("Form", "Исходный тип свойства", None))
        self.lblTargetTypeName.setText(_translate("Form", "Итоговый тип свойства", None))
        self.btnDataAnalysis.setText(_translate("Form", "Анализ данных", None))
        self.btnStart.setText(_translate("Form", "Старт", None))
        self.btnReset.setText(_translate("Form", "Очистить", None))
        self.lblTargetPropertyName.setText(_translate("Form", "Итоговое свойство", None))
        self.chkActionType.setText(_translate("Form", "Тип действия", None))
        self.chkDeleteSource.setText(_translate("Form", "Удалять исходные свойства", None))
        self.chkFullReport.setText(_translate("Form", "Полная отчетность", None))
        self.chkDeletingAutoStart.setText(_translate("Form", "Автоматически начать удаление свойств", None))

from Events.ActionTypeComboBox import CActionTypeComboBox
from library.ProgressBar import CProgressBar
