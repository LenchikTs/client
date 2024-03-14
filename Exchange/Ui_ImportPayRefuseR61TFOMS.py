# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\projects\samson\UP_s11\client_test\Exchange\ImportPayRefuseR61TFOMS.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(653, 399)
        self.gridLayout_2 = QtGui.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.btnImport = QtGui.QPushButton(Dialog)
        self.btnImport.setObjectName(_fromUtf8("btnImport"))
        self.hboxlayout.addWidget(self.btnImport)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.btnClose = QtGui.QPushButton(Dialog)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.hboxlayout.addWidget(self.btnClose)
        self.gridLayout_2.addLayout(self.hboxlayout, 4, 0, 1, 1)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.hboxlayout1.addWidget(self.label)
        self.edtFileName = QtGui.QLineEdit(Dialog)
        self.edtFileName.setObjectName(_fromUtf8("edtFileName"))
        self.hboxlayout1.addWidget(self.edtFileName)
        self.btnSelectFile = QtGui.QToolButton(Dialog)
        self.btnSelectFile.setObjectName(_fromUtf8("btnSelectFile"))
        self.hboxlayout1.addWidget(self.btnSelectFile)
        self.gridLayout_2.addLayout(self.hboxlayout1, 0, 0, 1, 1)
        self.progressBar = CProgressBar(Dialog)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout_2.addWidget(self.progressBar, 1, 0, 1, 1)
        self.tabRegime = QtGui.QTabWidget(Dialog)
        self.tabRegime.setObjectName(_fromUtf8("tabRegime"))
        self.tabFLC = QtGui.QWidget()
        self.tabFLC.setObjectName(_fromUtf8("tabFLC"))
        self.gridLayout = QtGui.QGridLayout(self.tabFLC)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.chkUpdateAccounts = QtGui.QCheckBox(self.tabFLC)
        self.chkUpdateAccounts.setObjectName(_fromUtf8("chkUpdateAccounts"))
        self.gridLayout.addWidget(self.chkUpdateAccounts, 1, 0, 1, 1)
        self._2 = QtGui.QHBoxLayout()
        self._2.setMargin(0)
        self._2.setSpacing(6)
        self._2.setObjectName(_fromUtf8("_2"))
        self.lblOutputDir = QtGui.QLabel(self.tabFLC)
        self.lblOutputDir.setObjectName(_fromUtf8("lblOutputDir"))
        self._2.addWidget(self.lblOutputDir)
        self.edtOutputDir = QtGui.QLineEdit(self.tabFLC)
        self.edtOutputDir.setObjectName(_fromUtf8("edtOutputDir"))
        self._2.addWidget(self.edtOutputDir)
        self.btnSelectDir = QtGui.QToolButton(self.tabFLC)
        self.btnSelectDir.setObjectName(_fromUtf8("btnSelectDir"))
        self._2.addWidget(self.btnSelectDir)
        self.gridLayout.addLayout(self._2, 2, 0, 1, 1)
        self.chkUpdatePolicy = QtGui.QCheckBox(self.tabFLC)
        self.chkUpdatePolicy.setObjectName(_fromUtf8("chkUpdatePolicy"))
        self.gridLayout.addWidget(self.chkUpdatePolicy, 0, 0, 1, 1)
        self.tabRegime.addTab(self.tabFLC, _fromUtf8(""))
        self.tabMEK = QtGui.QWidget()
        self.tabMEK.setObjectName(_fromUtf8("tabMEK"))
        self.tabRegime.addTab(self.tabMEK, _fromUtf8(""))
        self.tabReMEK = QtGui.QWidget()
        self.tabReMEK.setObjectName(_fromUtf8("tabReMEK"))
        self.tabRegime.addTab(self.tabReMEK, _fromUtf8(""))
        self.gridLayout_2.addWidget(self.tabRegime, 2, 0, 1, 1)
        self.log = QtGui.QTextBrowser(Dialog)
        self.log.setObjectName(_fromUtf8("log"))
        self.gridLayout_2.addWidget(self.log, 3, 0, 1, 1)
        self.gridLayout_2.setRowStretch(3, 2)

        self.retranslateUi(Dialog)
        self.tabRegime.setCurrentIndex(0)
        QtCore.QObject.connect(self.chkUpdateAccounts, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.lblOutputDir.setVisible)
        QtCore.QObject.connect(self.chkUpdateAccounts, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtOutputDir.setVisible)
        QtCore.QObject.connect(self.chkUpdateAccounts, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.btnSelectDir.setVisible)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Импорт реестров - Ростовская область", None))
        self.btnImport.setText(_translate("Dialog", "начать импортирование", None))
        self.btnClose.setText(_translate("Dialog", "закрыть", None))
        self.label.setText(_translate("Dialog", "импортировать из", None))
        self.btnSelectFile.setText(_translate("Dialog", "...", None))
        self.chkUpdateAccounts.setText(_translate("Dialog", "Разделить реестры по страховым компаниям", None))
        self.lblOutputDir.setText(_translate("Dialog", "Сохранить реестры в", None))
        self.btnSelectDir.setText(_translate("Dialog", "...", None))
        self.chkUpdatePolicy.setText(_translate("Dialog", "Обновить полисные данные", None))
        self.tabRegime.setTabText(self.tabRegime.indexOf(self.tabFLC), _translate("Dialog", "ФЛК", None))
        self.tabRegime.setTabText(self.tabRegime.indexOf(self.tabMEK), _translate("Dialog", "МЭК", None))
        self.tabRegime.setTabText(self.tabRegime.indexOf(self.tabReMEK), _translate("Dialog", "повторный МЭК", None))

from library.ProgressBar import CProgressBar
