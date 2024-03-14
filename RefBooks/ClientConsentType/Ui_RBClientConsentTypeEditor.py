# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/RefBooks/RBClientConsentTypeEditor.ui'
#
# Created: Wed Feb 19 22:56:10 2014
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RBClientConsentTypeEditor(object):
    def setupUi(self, RBClientConsentTypeEditor):
        RBClientConsentTypeEditor.setObjectName(_fromUtf8("RBClientConsentTypeEditor"))
        RBClientConsentTypeEditor.resize(320, 166)
        self.gridLayout = QtGui.QGridLayout(RBClientConsentTypeEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblName = QtGui.QLabel(RBClientConsentTypeEditor)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 1, 0, 1, 1)
        self.edtName = QtGui.QLineEdit(RBClientConsentTypeEditor)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 1, 1, 1, 1)
        self.lblPeriodFlag = QtGui.QLabel(RBClientConsentTypeEditor)
        self.lblPeriodFlag.setObjectName(_fromUtf8("lblPeriodFlag"))
        self.gridLayout.addWidget(self.lblPeriodFlag, 2, 0, 1, 1)
        self.chkInClientInfoBrowser = QtGui.QCheckBox(RBClientConsentTypeEditor)
        self.chkInClientInfoBrowser.setText(_fromUtf8(""))
        self.chkInClientInfoBrowser.setObjectName(_fromUtf8("chkInClientInfoBrowser"))
        self.gridLayout.addWidget(self.chkInClientInfoBrowser, 4, 1, 1, 1)
        self.lblCode = QtGui.QLabel(RBClientConsentTypeEditor)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.edtCode = QtGui.QLineEdit(RBClientConsentTypeEditor)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout.addWidget(self.edtCode, 0, 1, 1, 1)
        self.cmbPeriodFlag = QtGui.QComboBox(RBClientConsentTypeEditor)
        self.cmbPeriodFlag.setObjectName(_fromUtf8("cmbPeriodFlag"))
        self.cmbPeriodFlag.addItem(_fromUtf8(""))
        self.cmbPeriodFlag.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbPeriodFlag, 2, 1, 1, 1)
        self.lblDefaultPeriod = QtGui.QLabel(RBClientConsentTypeEditor)
        self.lblDefaultPeriod.setObjectName(_fromUtf8("lblDefaultPeriod"))
        self.gridLayout.addWidget(self.lblDefaultPeriod, 3, 0, 1, 1)
        self.edtDefaultPeriod = QtGui.QSpinBox(RBClientConsentTypeEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtDefaultPeriod.sizePolicy().hasHeightForWidth())
        self.edtDefaultPeriod.setSizePolicy(sizePolicy)
        self.edtDefaultPeriod.setObjectName(_fromUtf8("edtDefaultPeriod"))
        self.gridLayout.addWidget(self.edtDefaultPeriod, 3, 1, 1, 1)
        self.lblInClientInfoBrowser = QtGui.QLabel(RBClientConsentTypeEditor)
        self.lblInClientInfoBrowser.setObjectName(_fromUtf8("lblInClientInfoBrowser"))
        self.gridLayout.addWidget(self.lblInClientInfoBrowser, 4, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RBClientConsentTypeEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)
        self.lblName.setBuddy(self.edtName)
        self.lblCode.setBuddy(self.edtCode)

        self.retranslateUi(RBClientConsentTypeEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBClientConsentTypeEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBClientConsentTypeEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(RBClientConsentTypeEditor)
        RBClientConsentTypeEditor.setTabOrder(self.edtCode, self.edtName)
        RBClientConsentTypeEditor.setTabOrder(self.edtName, self.cmbPeriodFlag)
        RBClientConsentTypeEditor.setTabOrder(self.cmbPeriodFlag, self.edtDefaultPeriod)
        RBClientConsentTypeEditor.setTabOrder(self.edtDefaultPeriod, self.chkInClientInfoBrowser)
        RBClientConsentTypeEditor.setTabOrder(self.chkInClientInfoBrowser, self.buttonBox)

    def retranslateUi(self, RBClientConsentTypeEditor):
        RBClientConsentTypeEditor.setWindowTitle(QtGui.QApplication.translate("RBClientConsentTypeEditor", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.lblName.setText(QtGui.QApplication.translate("RBClientConsentTypeEditor", "&Наименование", None, QtGui.QApplication.UnicodeUTF8))
        self.lblPeriodFlag.setText(QtGui.QApplication.translate("RBClientConsentTypeEditor", "Срочность", None, QtGui.QApplication.UnicodeUTF8))
        self.lblCode.setText(QtGui.QApplication.translate("RBClientConsentTypeEditor", "&Код", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbPeriodFlag.setItemText(0, QtGui.QApplication.translate("RBClientConsentTypeEditor", "Бессрочный", None, QtGui.QApplication.UnicodeUTF8))
        self.cmbPeriodFlag.setItemText(1, QtGui.QApplication.translate("RBClientConsentTypeEditor", "Срочный", None, QtGui.QApplication.UnicodeUTF8))
        self.lblDefaultPeriod.setText(QtGui.QApplication.translate("RBClientConsentTypeEditor", "Срок действия (месяцев)", None, QtGui.QApplication.UnicodeUTF8))
        self.lblInClientInfoBrowser.setText(QtGui.QApplication.translate("RBClientConsentTypeEditor", "Визуализация в шильдике пациента", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RBClientConsentTypeEditor = QtGui.QDialog()
    ui = Ui_RBClientConsentTypeEditor()
    ui.setupUi(RBClientConsentTypeEditor)
    RBClientConsentTypeEditor.show()
    sys.exit(app.exec_())

