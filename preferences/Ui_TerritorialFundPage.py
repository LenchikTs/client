# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Samson\UP_s11\client_merge\preferences\TerritorialFundPage.ui'
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

class Ui_territorialFundPage(object):
    def setupUi(self, territorialFundPage):
        territorialFundPage.setObjectName(_fromUtf8("territorialFundPage"))
        territorialFundPage.resize(471, 300)
        territorialFundPage.setToolTip(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(territorialFundPage)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.chkTFCheckPolicy = QtGui.QCheckBox(territorialFundPage)
        self.chkTFCheckPolicy.setObjectName(_fromUtf8("chkTFCheckPolicy"))
        self.gridLayout.addWidget(self.chkTFCheckPolicy, 0, 0, 1, 3)
        self.lblTFCPUrl = QtGui.QLabel(territorialFundPage)
        self.lblTFCPUrl.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTFCPUrl.sizePolicy().hasHeightForWidth())
        self.lblTFCPUrl.setSizePolicy(sizePolicy)
        self.lblTFCPUrl.setMinimumSize(QtCore.QSize(130, 0))
        self.lblTFCPUrl.setObjectName(_fromUtf8("lblTFCPUrl"))
        self.gridLayout.addWidget(self.lblTFCPUrl, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 185, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(160, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 2, 1, 1)
        self.btnTFCPTest = QtGui.QPushButton(territorialFundPage)
        self.btnTFCPTest.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnTFCPTest.sizePolicy().hasHeightForWidth())
        self.btnTFCPTest.setSizePolicy(sizePolicy)
        self.btnTFCPTest.setObjectName(_fromUtf8("btnTFCPTest"))
        self.gridLayout.addWidget(self.btnTFCPTest, 2, 1, 1, 1)
        self.edtTFCPUrl = QtGui.QLineEdit(territorialFundPage)
        self.edtTFCPUrl.setEnabled(False)
        self.edtTFCPUrl.setMinimumSize(QtCore.QSize(300, 0))
        self.edtTFCPUrl.setText(_fromUtf8(""))
        self.edtTFCPUrl.setObjectName(_fromUtf8("edtTFCPUrl"))
        self.gridLayout.addWidget(self.edtTFCPUrl, 1, 1, 1, 2)
        self.chkSyncAttachmentsAfterSave = QtGui.QCheckBox(territorialFundPage)
        self.chkSyncAttachmentsAfterSave.setObjectName(_fromUtf8("chkSyncAttachmentsAfterSave"))
        self.gridLayout.addWidget(self.chkSyncAttachmentsAfterSave, 3, 0, 1, 3)
        self.lblTFCPUrl.setBuddy(self.edtTFCPUrl)

        self.retranslateUi(territorialFundPage)
        QtCore.QObject.connect(self.chkTFCheckPolicy, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.lblTFCPUrl.setEnabled)
        QtCore.QObject.connect(self.chkTFCheckPolicy, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtTFCPUrl.setEnabled)
        QtCore.QObject.connect(self.chkTFCheckPolicy, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.btnTFCPTest.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(territorialFundPage)
        territorialFundPage.setTabOrder(self.chkTFCheckPolicy, self.edtTFCPUrl)
        territorialFundPage.setTabOrder(self.edtTFCPUrl, self.btnTFCPTest)

    def retranslateUi(self, territorialFundPage):
        territorialFundPage.setWindowTitle(_translate("territorialFundPage", "Страховая принадлежность", None))
        self.chkTFCheckPolicy.setText(_translate("territorialFundPage", "Разрешить использовать cервис поиска и проверки полиса ОМС", None))
        self.lblTFCPUrl.setText(_translate("territorialFundPage", "&Адрес сервиса", None))
        self.btnTFCPTest.setText(_translate("territorialFundPage", "Проверить соединение", None))
        self.edtTFCPUrl.setToolTip(_translate("territorialFundPage", "<html><head/><body><p>В случае унифицированного протокола можно вписать</p><p><br/><span style=\" font-weight:600;\">http://${dbServerName}/ident/handler.php<br/></span></p><p>При этом вместо <span style=\" font-weight:600;\">${dbServerName} </span>должно подставиться имя (или IP адрес) сервера базы данных.</p></body></html>", None))
        self.chkSyncAttachmentsAfterSave.setText(_translate("territorialFundPage", "Синхронизировать прикрепление после сохранения рег.карты", None))

