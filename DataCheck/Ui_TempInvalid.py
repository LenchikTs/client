# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\projects\samson\UP_s11\client\DataCheck\TempInvalid.ui'
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

class Ui_TempInvalidCheckDialog(object):
    def setupUi(self, TempInvalidCheckDialog):
        TempInvalidCheckDialog.setObjectName(_fromUtf8("TempInvalidCheckDialog"))
        TempInvalidCheckDialog.resize(589, 538)
        self.gridLayout = QtGui.QGridLayout(TempInvalidCheckDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.frmDateRange = QtGui.QWidget(TempInvalidCheckDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frmDateRange.sizePolicy().hasHeightForWidth())
        self.frmDateRange.setSizePolicy(sizePolicy)
        self.frmDateRange.setObjectName(_fromUtf8("frmDateRange"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frmDateRange)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.frmDateRange)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.dateEdit_1 = CDateEdit(self.frmDateRange)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateEdit_1.sizePolicy().hasHeightForWidth())
        self.dateEdit_1.setSizePolicy(sizePolicy)
        self.dateEdit_1.setDate(QtCore.QDate(2000, 1, 1))
        self.dateEdit_1.setCalendarPopup(True)
        self.dateEdit_1.setObjectName(_fromUtf8("dateEdit_1"))
        self.horizontalLayout.addWidget(self.dateEdit_1)
        self.label_2 = QtGui.QLabel(self.frmDateRange)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.dateEdit_2 = CDateEdit(self.frmDateRange)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateEdit_2.sizePolicy().hasHeightForWidth())
        self.dateEdit_2.setSizePolicy(sizePolicy)
        self.dateEdit_2.setDate(QtCore.QDate(2000, 1, 1))
        self.dateEdit_2.setCalendarPopup(True)
        self.dateEdit_2.setObjectName(_fromUtf8("dateEdit_2"))
        self.horizontalLayout.addWidget(self.dateEdit_2)
        self.gridLayout.addWidget(self.frmDateRange, 0, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(349, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 4)
        self.boxDocTypes = QtGui.QComboBox(TempInvalidCheckDialog)
        self.boxDocTypes.setObjectName(_fromUtf8("boxDocTypes"))
        self.boxDocTypes.addItem(_fromUtf8(""))
        self.boxDocTypes.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.boxDocTypes, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(TempInvalidCheckDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(349, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 4)
        self.checkExpert = QtGui.QCheckBox(TempInvalidCheckDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkExpert.sizePolicy().hasHeightForWidth())
        self.checkExpert.setSizePolicy(sizePolicy)
        self.checkExpert.setObjectName(_fromUtf8("checkExpert"))
        self.gridLayout.addWidget(self.checkExpert, 3, 0, 1, 6)
        self.checkDur = QtGui.QCheckBox(TempInvalidCheckDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkDur.sizePolicy().hasHeightForWidth())
        self.checkDur.setSizePolicy(sizePolicy)
        self.checkDur.setObjectName(_fromUtf8("checkDur"))
        self.gridLayout.addWidget(self.checkDur, 5, 0, 1, 6)
        self.checkDocum = QtGui.QCheckBox(TempInvalidCheckDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkDocum.sizePolicy().hasHeightForWidth())
        self.checkDocum.setSizePolicy(sizePolicy)
        self.checkDocum.setObjectName(_fromUtf8("checkDocum"))
        self.gridLayout.addWidget(self.checkDocum, 4, 0, 1, 6)
        self.progressBar = CProgressBar(TempInvalidCheckDialog)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 6, 0, 1, 6)
        self.log = QtGui.QListWidget(TempInvalidCheckDialog)
        self.log.setObjectName(_fromUtf8("log"))
        self.gridLayout.addWidget(self.log, 7, 0, 1, 6)
        self.btnStart = QtGui.QPushButton(TempInvalidCheckDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnStart.sizePolicy().hasHeightForWidth())
        self.btnStart.setSizePolicy(sizePolicy)
        self.btnStart.setMinimumSize(QtCore.QSize(100, 0))
        self.btnStart.setObjectName(_fromUtf8("btnStart"))
        self.gridLayout.addWidget(self.btnStart, 8, 4, 1, 1)
        self.labelInfo = QtGui.QLabel(TempInvalidCheckDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelInfo.sizePolicy().hasHeightForWidth())
        self.labelInfo.setSizePolicy(sizePolicy)
        self.labelInfo.setText(_fromUtf8(""))
        self.labelInfo.setObjectName(_fromUtf8("labelInfo"))
        self.gridLayout.addWidget(self.labelInfo, 8, 0, 1, 3)
        self.btnClose = QtGui.QPushButton(TempInvalidCheckDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnClose.sizePolicy().hasHeightForWidth())
        self.btnClose.setSizePolicy(sizePolicy)
        self.btnClose.setMinimumSize(QtCore.QSize(100, 0))
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.gridLayout.addWidget(self.btnClose, 8, 5, 1, 1)
        self.btnPrint = QtGui.QPushButton(TempInvalidCheckDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnPrint.sizePolicy().hasHeightForWidth())
        self.btnPrint.setSizePolicy(sizePolicy)
        self.btnPrint.setMinimumSize(QtCore.QSize(100, 0))
        self.btnPrint.setObjectName(_fromUtf8("btnPrint"))
        self.gridLayout.addWidget(self.btnPrint, 8, 3, 1, 1)

        self.retranslateUi(TempInvalidCheckDialog)
        QtCore.QMetaObject.connectSlotsByName(TempInvalidCheckDialog)
        TempInvalidCheckDialog.setTabOrder(self.dateEdit_1, self.dateEdit_2)
        TempInvalidCheckDialog.setTabOrder(self.dateEdit_2, self.boxDocTypes)
        TempInvalidCheckDialog.setTabOrder(self.boxDocTypes, self.checkExpert)
        TempInvalidCheckDialog.setTabOrder(self.checkExpert, self.checkDocum)
        TempInvalidCheckDialog.setTabOrder(self.checkDocum, self.checkDur)
        TempInvalidCheckDialog.setTabOrder(self.checkDur, self.log)
        TempInvalidCheckDialog.setTabOrder(self.log, self.btnStart)
        TempInvalidCheckDialog.setTabOrder(self.btnStart, self.btnClose)

    def retranslateUi(self, TempInvalidCheckDialog):
        TempInvalidCheckDialog.setWindowTitle(_translate("TempInvalidCheckDialog", "логический контроль ВУТ", None))
        self.label.setText(_translate("TempInvalidCheckDialog", "с", None))
        self.dateEdit_1.setDisplayFormat(_translate("TempInvalidCheckDialog", "dd.MM.yyyy", None))
        self.label_2.setText(_translate("TempInvalidCheckDialog", "по", None))
        self.dateEdit_2.setDisplayFormat(_translate("TempInvalidCheckDialog", "dd.MM.yyyy", None))
        self.boxDocTypes.setItemText(0, _translate("TempInvalidCheckDialog", "больничный лист", None))
        self.boxDocTypes.setItemText(1, _translate("TempInvalidCheckDialog", "справка", None))
        self.label_3.setText(_translate("TempInvalidCheckDialog", "тип документа", None))
        self.checkExpert.setText(_translate("TempInvalidCheckDialog", "выполнять экспертизу", None))
        self.checkDur.setText(_translate("TempInvalidCheckDialog", "проверять длительность", None))
        self.checkDocum.setText(_translate("TempInvalidCheckDialog", "проверять документ", None))
        self.btnStart.setText(_translate("TempInvalidCheckDialog", "начать проверку", None))
        self.btnClose.setText(_translate("TempInvalidCheckDialog", "прервать", None))
        self.btnPrint.setText(_translate("TempInvalidCheckDialog", "печать", None))

from library.DateEdit import CDateEdit
from library.ProgressBar import CProgressBar
