# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_test\Exchange\ImportTariffsR47.ui'
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

class Ui_ImportTariffs(object):
    def setupUi(self, ImportTariffs):
        ImportTariffs.setObjectName(_fromUtf8("ImportTariffs"))
        ImportTariffs.resize(475, 429)
        ImportTariffs.setWindowTitle(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(ImportTariffs)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(ImportTariffs)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.edtFileName = QtGui.QLineEdit(ImportTariffs)
        self.edtFileName.setObjectName(_fromUtf8("edtFileName"))
        self.gridLayout.addWidget(self.edtFileName, 0, 2, 1, 1)
        self.btnSelectFile = QtGui.QToolButton(ImportTariffs)
        self.btnSelectFile.setObjectName(_fromUtf8("btnSelectFile"))
        self.gridLayout.addWidget(self.btnSelectFile, 0, 3, 1, 1)
        self.progressBar = CProgressBar(ImportTariffs)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 1, 0, 1, 4)
        self.log = QtGui.QTextBrowser(ImportTariffs)
        self.log.setObjectName(_fromUtf8("log"))
        self.gridLayout.addWidget(self.log, 10, 0, 1, 4)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.btnImport = QtGui.QPushButton(ImportTariffs)
        self.btnImport.setEnabled(False)
        self.btnImport.setObjectName(_fromUtf8("btnImport"))
        self.hboxlayout.addWidget(self.btnImport)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.btnClose = QtGui.QPushButton(ImportTariffs)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.hboxlayout.addWidget(self.btnClose)
        self.gridLayout.addLayout(self.hboxlayout, 12, 0, 1, 4)
        self.lblStatus = QtGui.QLabel(ImportTariffs)
        self.lblStatus.setText(_fromUtf8(""))
        self.lblStatus.setObjectName(_fromUtf8("lblStatus"))
        self.gridLayout.addWidget(self.lblStatus, 11, 0, 1, 4)
        self.chkFullLog = QtGui.QCheckBox(ImportTariffs)
        self.chkFullLog.setObjectName(_fromUtf8("chkFullLog"))
        self.gridLayout.addWidget(self.chkFullLog, 9, 0, 1, 4)
        self.edtOrgInfis = QtGui.QSpinBox(ImportTariffs)
        self.edtOrgInfis.setMinimum(1)
        self.edtOrgInfis.setMaximum(999)
        self.edtOrgInfis.setObjectName(_fromUtf8("edtOrgInfis"))
        self.gridLayout.addWidget(self.edtOrgInfis, 5, 1, 1, 3)
        self.lblTariffType = QtGui.QLabel(ImportTariffs)
        self.lblTariffType.setObjectName(_fromUtf8("lblTariffType"))
        self.gridLayout.addWidget(self.lblTariffType, 8, 0, 1, 1)
        self.lblOrgInfis = QtGui.QLabel(ImportTariffs)
        self.lblOrgInfis.setObjectName(_fromUtf8("lblOrgInfis"))
        self.gridLayout.addWidget(self.lblOrgInfis, 5, 0, 1, 1)
        self.lblOrgLevel = QtGui.QLabel(ImportTariffs)
        self.lblOrgLevel.setObjectName(_fromUtf8("lblOrgLevel"))
        self.gridLayout.addWidget(self.lblOrgLevel, 4, 0, 1, 1)
        self.cmbOrgLevel = QtGui.QComboBox(ImportTariffs)
        self.cmbOrgLevel.setObjectName(_fromUtf8("cmbOrgLevel"))
        self.cmbOrgLevel.addItem(_fromUtf8(""))
        self.cmbOrgLevel.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbOrgLevel, 4, 1, 1, 3)
        self.cmbEventType = CRBComboBox(ImportTariffs)
        self.cmbEventType.setObjectName(_fromUtf8("cmbEventType"))
        self.gridLayout.addWidget(self.cmbEventType, 7, 1, 1, 3)
        self.cmbTariffType = QtGui.QComboBox(ImportTariffs)
        self.cmbTariffType.setObjectName(_fromUtf8("cmbTariffType"))
        self.gridLayout.addWidget(self.cmbTariffType, 8, 1, 1, 3)
        self.lblEventType = QtGui.QLabel(ImportTariffs)
        self.lblEventType.setObjectName(_fromUtf8("lblEventType"))
        self.gridLayout.addWidget(self.lblEventType, 7, 0, 1, 1)
        self.label.setBuddy(self.edtFileName)

        self.retranslateUi(ImportTariffs)
        QtCore.QMetaObject.connectSlotsByName(ImportTariffs)
        ImportTariffs.setTabOrder(self.edtFileName, self.btnSelectFile)
        ImportTariffs.setTabOrder(self.btnSelectFile, self.chkFullLog)
        ImportTariffs.setTabOrder(self.chkFullLog, self.log)
        ImportTariffs.setTabOrder(self.log, self.btnImport)
        ImportTariffs.setTabOrder(self.btnImport, self.btnClose)

    def retranslateUi(self, ImportTariffs):
        self.label.setText(_translate("ImportTariffs", "Загрузить из", None))
        self.btnSelectFile.setText(_translate("ImportTariffs", "...", None))
        self.btnImport.setText(_translate("ImportTariffs", "Начать импорт", None))
        self.btnClose.setText(_translate("ImportTariffs", "Закрыть", None))
        self.chkFullLog.setText(_translate("ImportTariffs", "Подробный отчет", None))
        self.lblTariffType.setText(_translate("ImportTariffs", "Тип тарифа", None))
        self.lblOrgInfis.setText(_translate("ImportTariffs", "Код ЛПУ", None))
        self.lblOrgLevel.setText(_translate("ImportTariffs", "Уровень ЛПУ", None))
        self.cmbOrgLevel.setItemText(0, _translate("ImportTariffs", "1", None))
        self.cmbOrgLevel.setItemText(1, _translate("ImportTariffs", "2", None))
        self.lblEventType.setText(_translate("ImportTariffs", "Тип события", None))

from library.ProgressBar import CProgressBar
from library.crbcombobox import CRBComboBox
