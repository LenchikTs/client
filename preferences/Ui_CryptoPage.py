# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CryptoPage.ui'
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

class Ui_cryptoPage(object):
    def setupUi(self, cryptoPage):
        cryptoPage.setObjectName(_fromUtf8("cryptoPage"))
        cryptoPage.resize(498, 202)
        self.gridLayout = QtGui.QGridLayout(cryptoPage)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblCsp = QtGui.QLabel(cryptoPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCsp.sizePolicy().hasHeightForWidth())
        self.lblCsp.setSizePolicy(sizePolicy)
        self.lblCsp.setMinimumSize(QtCore.QSize(130, 0))
        self.lblCsp.setObjectName(_fromUtf8("lblCsp"))
        self.gridLayout.addWidget(self.lblCsp, 0, 0, 1, 1)
        self.cmbCsp = QtGui.QComboBox(cryptoPage)
        self.cmbCsp.setObjectName(_fromUtf8("cmbCsp"))
        self.gridLayout.addWidget(self.cmbCsp, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.rbnOwnPK = QtGui.QRadioButton(cryptoPage)
        self.rbnOwnPK.setChecked(True)
        self.rbnOwnPK.setObjectName(_fromUtf8("rbnOwnPK"))
        self.gridLayout.addWidget(self.rbnOwnPK, 1, 0, 1, 1)
        self.rbnCustomPK = QtGui.QRadioButton(cryptoPage)
        self.rbnCustomPK.setObjectName(_fromUtf8("rbnCustomPK"))
        self.gridLayout.addWidget(self.rbnCustomPK, 2, 0, 1, 1)
        self.cmbUserCert = CCertComboBox(cryptoPage)
        self.cmbUserCert.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbUserCert.sizePolicy().hasHeightForWidth())
        self.cmbUserCert.setSizePolicy(sizePolicy)
        self.cmbUserCert.setObjectName(_fromUtf8("cmbUserCert"))
        self.gridLayout.addWidget(self.cmbUserCert, 2, 1, 1, 2)
        self.lblOrgCert = QtGui.QLabel(cryptoPage)
        self.lblOrgCert.setObjectName(_fromUtf8("lblOrgCert"))
        self.gridLayout.addWidget(self.lblOrgCert, 3, 0, 1, 1)
        self.cmbOrgCert = CCertComboBox(cryptoPage)
        self.cmbOrgCert.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbOrgCert.sizePolicy().hasHeightForWidth())
        self.cmbOrgCert.setSizePolicy(sizePolicy)
        self.cmbOrgCert.setObjectName(_fromUtf8("cmbOrgCert"))
        self.gridLayout.addWidget(self.cmbOrgCert, 3, 1, 1, 2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.chkWarnAboutCertExpiration = QtGui.QCheckBox(cryptoPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkWarnAboutCertExpiration.sizePolicy().hasHeightForWidth())
        self.chkWarnAboutCertExpiration.setSizePolicy(sizePolicy)
        self.chkWarnAboutCertExpiration.setObjectName(_fromUtf8("chkWarnAboutCertExpiration"))
        self.horizontalLayout.addWidget(self.chkWarnAboutCertExpiration)
        self.edtCertExpirationWarnPeriod = QtGui.QSpinBox(cryptoPage)
        self.edtCertExpirationWarnPeriod.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtCertExpirationWarnPeriod.sizePolicy().hasHeightForWidth())
        self.edtCertExpirationWarnPeriod.setSizePolicy(sizePolicy)
        self.edtCertExpirationWarnPeriod.setObjectName(_fromUtf8("edtCertExpirationWarnPeriod"))
        self.horizontalLayout.addWidget(self.edtCertExpirationWarnPeriod)
        self.lblCertExpirationWarnPeriod = QtGui.QLabel(cryptoPage)
        self.lblCertExpirationWarnPeriod.setEnabled(False)
        self.lblCertExpirationWarnPeriod.setObjectName(_fromUtf8("lblCertExpirationWarnPeriod"))
        self.horizontalLayout.addWidget(self.lblCertExpirationWarnPeriod)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 4, 0, 1, 3)
        spacerItem2 = QtGui.QSpacerItem(129, 218, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 5, 0, 1, 1)
        self.lblCsp.setBuddy(self.cmbCsp)
        self.lblOrgCert.setBuddy(self.cmbOrgCert)
        self.lblCertExpirationWarnPeriod.setBuddy(self.edtCertExpirationWarnPeriod)

        self.retranslateUi(cryptoPage)
        QtCore.QObject.connect(self.rbnCustomPK, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbUserCert.setEnabled)
        QtCore.QObject.connect(self.chkWarnAboutCertExpiration, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtCertExpirationWarnPeriod.setEnabled)
        QtCore.QObject.connect(self.chkWarnAboutCertExpiration, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.lblCertExpirationWarnPeriod.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(cryptoPage)
        cryptoPage.setTabOrder(self.cmbCsp, self.rbnOwnPK)
        cryptoPage.setTabOrder(self.rbnOwnPK, self.rbnCustomPK)
        cryptoPage.setTabOrder(self.rbnCustomPK, self.cmbUserCert)
        cryptoPage.setTabOrder(self.cmbUserCert, self.cmbOrgCert)
        cryptoPage.setTabOrder(self.cmbOrgCert, self.chkWarnAboutCertExpiration)
        cryptoPage.setTabOrder(self.chkWarnAboutCertExpiration, self.edtCertExpirationWarnPeriod)

    def retranslateUi(self, cryptoPage):
        cryptoPage.setWindowTitle(_translate("cryptoPage", "Криптография", None))
        self.lblCsp.setText(_translate("cryptoPage", "&Криптопровайдер", None))
        self.rbnOwnPK.setText(_translate("cryptoPage", "Ключ пользователя по &СНИЛС", None))
        self.rbnCustomPK.setText(_translate("cryptoPage", "&Произвольный ключ пользователя", None))
        self.lblOrgCert.setText(_translate("cryptoPage", "Ключ медицинской &организации", None))
        self.chkWarnAboutCertExpiration.setText(_translate("cryptoPage", "П&редупреждать об истечении срока действия сертификата за ", None))
        self.lblCertExpirationWarnPeriod.setText(_translate("cryptoPage", "&дней", None))

from library.CertComboBox import CCertComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    cryptoPage = QtGui.QWidget()
    ui = Ui_cryptoPage()
    ui.setupUi(cryptoPage)
    cryptoPage.show()
    sys.exit(app.exec_())

