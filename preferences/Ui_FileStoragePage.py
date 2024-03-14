# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_DN\preferences\FileStoragePage.ui'
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

class Ui_fileStoragePage(object):
    def setupUi(self, fileStoragePage):
        fileStoragePage.setObjectName(_fromUtf8("fileStoragePage"))
        fileStoragePage.resize(411, 124)
        self.gridLayout = QtGui.QGridLayout(fileStoragePage)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblWebDAVUrl = QtGui.QLabel(fileStoragePage)
        self.lblWebDAVUrl.setObjectName(_fromUtf8("lblWebDAVUrl"))
        self.gridLayout.addWidget(self.lblWebDAVUrl, 0, 0, 1, 1)
        self.edtWebDAVUrl = QtGui.QLineEdit(fileStoragePage)
        self.edtWebDAVUrl.setObjectName(_fromUtf8("edtWebDAVUrl"))
        self.gridLayout.addWidget(self.edtWebDAVUrl, 0, 1, 1, 1)
        self.chkSaveWithSignatures = QtGui.QCheckBox(fileStoragePage)
        self.chkSaveWithSignatures.setObjectName(_fromUtf8("chkSaveWithSignatures"))
        self.gridLayout.addWidget(self.chkSaveWithSignatures, 1, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 2)
        self.lblWebDAVUrl.setBuddy(self.edtWebDAVUrl)

        self.retranslateUi(fileStoragePage)
        QtCore.QMetaObject.connectSlotsByName(fileStoragePage)

    def retranslateUi(self, fileStoragePage):
        fileStoragePage.setWindowTitle(_translate("fileStoragePage", "Файловое хранилище", None))
        fileStoragePage.setToolTip(_translate("fileStoragePage", "Хранение прикреплённых файлов", None))
        self.lblWebDAVUrl.setText(_translate("fileStoragePage", "&URL сервиса WebDAV", None))
        self.edtWebDAVUrl.setToolTip(_translate("fileStoragePage", "<html><head/><body><p>Если это поле пусто, то используется глобальная настройка WebDAV.</p><p>Возможно указание имени сервера в символическом виде, типа <span style=\" font-weight:600;\">http://${dbServerName}/sabre</span></p><p>При этом вместо <span style=\" font-weight:600;\">${dbServerName}</span> должно подставиться имя (или IP адрес) сервера базы данных.</p></body></html>", None))
        self.chkSaveWithSignatures.setText(_translate("fileStoragePage", "Сохранять файл подписи при сохранении файла", None))

