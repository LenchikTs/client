# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ExportTariffR23_Wizard_2.ui'
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

class Ui_ExportTariff_Wizard_2(object):
    def setupUi(self, ExportTariff_Wizard_2):
        ExportTariff_Wizard_2.setObjectName(_fromUtf8("ExportTariff_Wizard_2"))
        ExportTariff_Wizard_2.resize(415, 153)
        self.gridLayout = QtGui.QGridLayout(ExportTariff_Wizard_2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.checkRAR = QtGui.QCheckBox(ExportTariff_Wizard_2)
        self.checkRAR.setCheckable(True)
        self.checkRAR.setObjectName(_fromUtf8("checkRAR"))
        self.gridLayout.addWidget(self.checkRAR, 1, 0, 1, 2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblFileName = QtGui.QLabel(ExportTariff_Wizard_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblFileName.sizePolicy().hasHeightForWidth())
        self.lblFileName.setSizePolicy(sizePolicy)
        self.lblFileName.setMinimumSize(QtCore.QSize(125, 0))
        self.lblFileName.setObjectName(_fromUtf8("lblFileName"))
        self.horizontalLayout.addWidget(self.lblFileName)
        self.edtFileName = QtGui.QLineEdit(ExportTariff_Wizard_2)
        self.edtFileName.setObjectName(_fromUtf8("edtFileName"))
        self.horizontalLayout.addWidget(self.edtFileName)
        self.btnSelectFile = QtGui.QToolButton(ExportTariff_Wizard_2)
        self.btnSelectFile.setObjectName(_fromUtf8("btnSelectFile"))
        self.horizontalLayout.addWidget(self.btnSelectFile)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(278, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 8, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lblOms = QtGui.QLabel(ExportTariff_Wizard_2)
        self.lblOms.setMinimumSize(QtCore.QSize(125, 0))
        self.lblOms.setObjectName(_fromUtf8("lblOms"))
        self.horizontalLayout_2.addWidget(self.lblOms)
        self.edtOms = QtGui.QLineEdit(ExportTariff_Wizard_2)
        self.edtOms.setEchoMode(QtGui.QLineEdit.Normal)
        self.edtOms.setObjectName(_fromUtf8("edtOms"))
        self.horizontalLayout_2.addWidget(self.edtOms)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 2)
        self.btnExport = QtGui.QPushButton(ExportTariff_Wizard_2)
        self.btnExport.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnExport.sizePolicy().hasHeightForWidth())
        self.btnExport.setSizePolicy(sizePolicy)
        self.btnExport.setObjectName(_fromUtf8("btnExport"))
        self.gridLayout.addWidget(self.btnExport, 8, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(397, 79, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 5, 0, 1, 2)
        self.progressBar = CProgressBar(ExportTariff_Wizard_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        self.lblFileName.setBuddy(self.edtFileName)
        self.lblOms.setBuddy(self.edtOms)

        self.retranslateUi(ExportTariff_Wizard_2)
        QtCore.QMetaObject.connectSlotsByName(ExportTariff_Wizard_2)
        ExportTariff_Wizard_2.setTabOrder(self.edtFileName, self.btnSelectFile)
        ExportTariff_Wizard_2.setTabOrder(self.btnSelectFile, self.checkRAR)
        ExportTariff_Wizard_2.setTabOrder(self.checkRAR, self.edtOms)

    def retranslateUi(self, ExportTariff_Wizard_2):
        ExportTariff_Wizard_2.setWindowTitle(_translate("ExportTariff_Wizard_2", "Выбор файла и процесс", None))
        self.checkRAR.setText(_translate("ExportTariff_Wizard_2", "Архивировать zip", None))
        self.lblFileName.setText(_translate("ExportTariff_Wizard_2", "Экспортировать в", None))
        self.btnSelectFile.setText(_translate("ExportTariff_Wizard_2", "...", None))
        self.lblOms.setText(_translate("ExportTariff_Wizard_2", "Код ЛПУ в системе ОМС", None))
        self.edtOms.setInputMask(_translate("ExportTariff_Wizard_2", "99999; ", None))
        self.btnExport.setText(_translate("ExportTariff_Wizard_2", "Начать экспорт", None))

from library.ProgressBar import CProgressBar
