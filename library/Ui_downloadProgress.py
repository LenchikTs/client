# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_ELN\library\downloadProgress.ui'
#
# Created: Mon Jul 27 08:34:18 2020
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

class Ui_DownloadProgress(object):
    def setupUi(self, DownloadProgress):
        DownloadProgress.setObjectName(_fromUtf8("DownloadProgress"))
        DownloadProgress.resize(504, 87)
        DownloadProgress.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(DownloadProgress)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelFile = QtGui.QLabel(DownloadProgress)
        self.labelFile.setObjectName(_fromUtf8("labelFile"))
        self.horizontalLayout.addWidget(self.labelFile)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.labelFileSize = QtGui.QLabel(DownloadProgress)
        self.labelFileSize.setObjectName(_fromUtf8("labelFileSize"))
        self.horizontalLayout.addWidget(self.labelFileSize)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.progressBarFile = QtGui.QProgressBar(DownloadProgress)
        self.progressBarFile.setMinimumSize(QtCore.QSize(0, 32))
        self.progressBarFile.setProperty("value", 24)
        self.progressBarFile.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBarFile.setObjectName(_fromUtf8("progressBarFile"))
        self.verticalLayout.addWidget(self.progressBarFile)

        self.retranslateUi(DownloadProgress)
        QtCore.QMetaObject.connectSlotsByName(DownloadProgress)

    def retranslateUi(self, DownloadProgress):
        DownloadProgress.setWindowTitle(_translate("DownloadProgress", "Обновление программных модулей...", None))
        self.labelFile.setText(_translate("DownloadProgress", "labelFile", None))
        self.labelFileSize.setText(_translate("DownloadProgress", "labelFileSize", None))

