# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\appendix\regional\r23\importReestr\importPrik.ui'
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

class Ui_PrikImportDialog(object):
    def setupUi(self, PrikImportDialog):
        PrikImportDialog.setObjectName(_fromUtf8("PrikImportDialog"))
        PrikImportDialog.resize(1103, 740)
        PrikImportDialog.setMinimumSize(QtCore.QSize(913, 646))
        self.verticalLayout = QtGui.QVBoxLayout(PrikImportDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter = QtGui.QSplitter(PrikImportDialog)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.chbSelectAll = QtGui.QCheckBox(self.layoutWidget)
        self.chbSelectAll.setEnabled(False)
        self.chbSelectAll.setCheckable(True)
        self.chbSelectAll.setChecked(True)
        self.chbSelectAll.setTristate(True)
        self.chbSelectAll.setObjectName(_fromUtf8("chbSelectAll"))
        self.verticalLayout_3.addWidget(self.chbSelectAll)
        self.tblDbfView = QtGui.QTableView(self.layoutWidget)
        self.tblDbfView.setObjectName(_fromUtf8("tblDbfView"))
        self.verticalLayout_3.addWidget(self.tblDbfView)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lblProgress = QtGui.QLabel(self.layoutWidget)
        self.lblProgress.setObjectName(_fromUtf8("lblProgress"))
        self.horizontalLayout_2.addWidget(self.lblProgress)
        self.prbProgress = QtGui.QProgressBar(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.prbProgress.sizePolicy().hasHeightForWidth())
        self.prbProgress.setSizePolicy(sizePolicy)
        self.prbProgress.setMaximum(0)
        self.prbProgress.setProperty("value", 0)
        self.prbProgress.setTextVisible(True)
        self.prbProgress.setOrientation(QtCore.Qt.Horizontal)
        self.prbProgress.setObjectName(_fromUtf8("prbProgress"))
        self.horizontalLayout_2.addWidget(self.prbProgress)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblElapsed = QtGui.QLabel(self.layoutWidget)
        self.lblElapsed.setObjectName(_fromUtf8("lblElapsed"))
        self.horizontalLayout.addWidget(self.lblElapsed)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnShowLog = QtGui.QToolButton(self.layoutWidget)
        self.btnShowLog.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.btnShowLog.setAutoRaise(True)
        self.btnShowLog.setArrowType(QtCore.Qt.UpArrow)
        self.btnShowLog.setObjectName(_fromUtf8("btnShowLog"))
        self.horizontalLayout.addWidget(self.btnShowLog)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.txtLog = QtGui.QTextBrowser(self.splitter)
        self.txtLog.setObjectName(_fromUtf8("txtLog"))
        self.verticalLayout.addWidget(self.splitter)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        spacerItem1 = QtGui.QSpacerItem(331, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.btnStart = QtGui.QPushButton(PrikImportDialog)
        self.btnStart.setObjectName(_fromUtf8("btnStart"))
        self.hboxlayout.addWidget(self.btnStart)
        self.btnCancel = QtGui.QPushButton(PrikImportDialog)
        self.btnCancel.setDefault(True)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.hboxlayout.addWidget(self.btnCancel)
        self.verticalLayout.addLayout(self.hboxlayout)
        self.actStartWork = QtGui.QAction(PrikImportDialog)
        self.actStartWork.setObjectName(_fromUtf8("actStartWork"))

        self.retranslateUi(PrikImportDialog)
        QtCore.QMetaObject.connectSlotsByName(PrikImportDialog)

    def retranslateUi(self, PrikImportDialog):
        PrikImportDialog.setWindowTitle(_translate("PrikImportDialog", "Импорт прикрепленного населения", None))
        self.chbSelectAll.setText(_translate("PrikImportDialog", "Выбрать все", None))
        self.lblProgress.setText(_translate("PrikImportDialog", "Процесс импорта", None))
        self.prbProgress.setFormat(_translate("PrikImportDialog", "%v из %m", None))
        self.lblElapsed.setText(_translate("PrikImportDialog", "Текущая операция: ??? зап/с, окончание в ??:??:??", None))
        self.btnShowLog.setText(_translate("PrikImportDialog", "Журнал импорта", None))
        self.btnStart.setText(_translate("PrikImportDialog", "Начать импорт", None))
        self.btnCancel.setText(_translate("PrikImportDialog", "Отмена", None))
        self.actStartWork.setText(_translate("PrikImportDialog", "startWork", None))

