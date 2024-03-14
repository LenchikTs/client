# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LLOPage.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
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

class Ui_LLOPage(object):
    def setupUi(self, LLOPage):
        LLOPage.setObjectName(_fromUtf8("LLOPage"))
        LLOPage.setEnabled(True)
        LLOPage.resize(553, 189)
        LLOPage.setMouseTracking(False)
        self.gridLayout = QtGui.QGridLayout(LLOPage)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lbllloUrl = QtGui.QLabel(LLOPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbllloUrl.sizePolicy().hasHeightForWidth())
        self.lbllloUrl.setSizePolicy(sizePolicy)
        self.lbllloUrl.setObjectName(_fromUtf8("lbllloUrl"))
        self.gridLayout.addWidget(self.lbllloUrl, 0, 0, 1, 1)
        self.edtlloUrl = QtGui.QLineEdit(LLOPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtlloUrl.sizePolicy().hasHeightForWidth())
        self.edtlloUrl.setSizePolicy(sizePolicy)
        self.edtlloUrl.setObjectName(_fromUtf8("edtlloUrl"))
        self.gridLayout.addWidget(self.edtlloUrl, 0, 1, 1, 1)
        self.lblRecipientCode = QtGui.QLabel(LLOPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblRecipientCode.sizePolicy().hasHeightForWidth())
        self.lblRecipientCode.setSizePolicy(sizePolicy)
        self.lblRecipientCode.setObjectName(_fromUtf8("lblRecipientCode"))
        self.gridLayout.addWidget(self.lblRecipientCode, 1, 0, 1, 1)
        self.edtRecipientCode = QtGui.QLineEdit(LLOPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtRecipientCode.sizePolicy().hasHeightForWidth())
        self.edtRecipientCode.setSizePolicy(sizePolicy)
        self.edtRecipientCode.setObjectName(_fromUtf8("edtRecipientCode"))
        self.gridLayout.addWidget(self.edtRecipientCode, 1, 1, 1, 1)
        self.lblRecipientName = QtGui.QLabel(LLOPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblRecipientName.sizePolicy().hasHeightForWidth())
        self.lblRecipientName.setSizePolicy(sizePolicy)
        self.lblRecipientName.setObjectName(_fromUtf8("lblRecipientName"))
        self.gridLayout.addWidget(self.lblRecipientName, 2, 0, 1, 1)
        self.edtRecipientName = QtGui.QLineEdit(LLOPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtRecipientName.sizePolicy().hasHeightForWidth())
        self.edtRecipientName.setSizePolicy(sizePolicy)
        self.edtRecipientName.setObjectName(_fromUtf8("edtRecipientName"))
        self.gridLayout.addWidget(self.edtRecipientName, 2, 1, 1, 1)
        self.lbllloLogin = QtGui.QLabel(LLOPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbllloLogin.sizePolicy().hasHeightForWidth())
        self.lbllloLogin.setSizePolicy(sizePolicy)
        self.lbllloLogin.setObjectName(_fromUtf8("lbllloLogin"))
        self.gridLayout.addWidget(self.lbllloLogin, 3, 0, 1, 1)
        self.edtlloLogin = QtGui.QLineEdit(LLOPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtlloLogin.sizePolicy().hasHeightForWidth())
        self.edtlloLogin.setSizePolicy(sizePolicy)
        self.edtlloLogin.setObjectName(_fromUtf8("edtlloLogin"))
        self.gridLayout.addWidget(self.edtlloLogin, 3, 1, 1, 1)
        self.lbllloPassword = QtGui.QLabel(LLOPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbllloPassword.sizePolicy().hasHeightForWidth())
        self.lbllloPassword.setSizePolicy(sizePolicy)
        self.lbllloPassword.setObjectName(_fromUtf8("lbllloPassword"))
        self.gridLayout.addWidget(self.lbllloPassword, 4, 0, 1, 1)
        self.edtlloPassword = QtGui.QLineEdit(LLOPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtlloPassword.sizePolicy().hasHeightForWidth())
        self.edtlloPassword.setSizePolicy(sizePolicy)
        self.edtlloPassword.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText)
        self.edtlloPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.edtlloPassword.setObjectName(_fromUtf8("edtlloPassword"))
        self.gridLayout.addWidget(self.edtlloPassword, 4, 1, 1, 1)
        self.chkRecipeTestIsOn = QtGui.QCheckBox(LLOPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkRecipeTestIsOn.sizePolicy().hasHeightForWidth())
        self.chkRecipeTestIsOn.setSizePolicy(sizePolicy)
        self.chkRecipeTestIsOn.setObjectName(_fromUtf8("chkRecipeTestIsOn"))
        self.gridLayout.addWidget(self.chkRecipeTestIsOn, 5, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 292, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 0, 1, 2)
        self.lbllloUrl.setBuddy(self.edtlloUrl)
        self.lblRecipientCode.setBuddy(self.edtRecipientCode)
        self.lblRecipientName.setBuddy(self.edtRecipientName)
        self.lbllloLogin.setBuddy(self.edtlloLogin)
        self.lbllloPassword.setBuddy(self.edtlloPassword)

        self.retranslateUi(LLOPage)
        QtCore.QMetaObject.connectSlotsByName(LLOPage)
        LLOPage.setTabOrder(self.edtlloUrl, self.edtRecipientCode)
        LLOPage.setTabOrder(self.edtRecipientCode, self.edtRecipientName)
        LLOPage.setTabOrder(self.edtRecipientName, self.edtlloLogin)
        LLOPage.setTabOrder(self.edtlloLogin, self.edtlloPassword)
        LLOPage.setTabOrder(self.edtlloPassword, self.chkRecipeTestIsOn)

    def retranslateUi(self, LLOPage):
        LLOPage.setWindowTitle(_translate("LLOPage", "Льготно-лекарственное обеспечение", None))
        self.lbllloUrl.setText(_translate("LLOPage", "&Адрес(url) сервиса льготно-лекарственного обеспечения", None))
        self.lblRecipientCode.setText(_translate("LLOPage", "&Код получателя", None))
        self.lblRecipientName.setText(_translate("LLOPage", "&Наименование получателя", None))
        self.lbllloLogin.setText(_translate("LLOPage", "&Логин сервиса льготно-лекарственного обеспечения", None))
        self.lbllloPassword.setText(_translate("LLOPage", "&Пароль сервиса льготно-лекарственного обеспечения", None))
        self.chkRecipeTestIsOn.setText(_translate("LLOPage", "Тестовый режим включен", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    LLOPage = QtGui.QWidget()
    ui = Ui_LLOPage()
    ui.setupUi(LLOPage)
    LLOPage.show()
    sys.exit(app.exec_())

