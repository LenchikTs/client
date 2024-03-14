# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\appendix\regional\r23\importReestr\SimpleProgress.ui'
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

class Ui_SimpleProgress(object):
    def setupUi(self, SimpleProgress):
        SimpleProgress.setObjectName(_fromUtf8("SimpleProgress"))
        SimpleProgress.resize(780, 315)
        self.verticalLayout = QtGui.QVBoxLayout(SimpleProgress)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblProgress = QtGui.QLabel(SimpleProgress)
        self.lblProgress.setObjectName(_fromUtf8("lblProgress"))
        self.horizontalLayout.addWidget(self.lblProgress)
        self.prbProgress = QtGui.QProgressBar(SimpleProgress)
        self.prbProgress.setProperty("value", 0)
        self.prbProgress.setObjectName(_fromUtf8("prbProgress"))
        self.horizontalLayout.addWidget(self.prbProgress)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lblElapsed = QtGui.QLabel(SimpleProgress)
        self.lblElapsed.setObjectName(_fromUtf8("lblElapsed"))
        self.horizontalLayout_2.addWidget(self.lblElapsed)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.txtLog = QtGui.QTextBrowser(SimpleProgress)
        self.txtLog.setObjectName(_fromUtf8("txtLog"))
        self.verticalLayout.addWidget(self.txtLog)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        spacerItem1 = QtGui.QSpacerItem(331, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.btnCancel = QtGui.QPushButton(SimpleProgress)
        self.btnCancel.setDefault(True)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.hboxlayout.addWidget(self.btnCancel)
        self.verticalLayout.addLayout(self.hboxlayout)

        self.retranslateUi(SimpleProgress)
        QtCore.QMetaObject.connectSlotsByName(SimpleProgress)

    def retranslateUi(self, SimpleProgress):
        SimpleProgress.setWindowTitle(_translate("SimpleProgress", "Импорт", None))
        self.lblProgress.setText(_translate("SimpleProgress", "Процесс импорта", None))
        self.lblElapsed.setText(_translate("SimpleProgress", "Текущая операция: ??? зап/с, окончание в ??:??:??", None))
        self.btnCancel.setText(_translate("SimpleProgress", "Отмена", None))

