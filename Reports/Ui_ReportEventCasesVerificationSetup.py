# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ReportEventCasesVerificationSetup.ui'
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

class Ui_ReportEventCasesVerificationSetup(object):
    def setupUi(self, ReportEventCasesVerificationSetup):
        ReportEventCasesVerificationSetup.setObjectName(_fromUtf8("ReportEventCasesVerificationSetup"))
        ReportEventCasesVerificationSetup.resize(465, 278)
        self.gridLayout = QtGui.QGridLayout(ReportEventCasesVerificationSetup)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 0, 1, 2)
        self.chkSendIEMK = QtGui.QCheckBox(ReportEventCasesVerificationSetup)
        self.chkSendIEMK.setObjectName(_fromUtf8("chkSendIEMK"))
        self.gridLayout.addWidget(self.chkSendIEMK, 3, 0, 1, 2)
        self.lblEndDate = QtGui.QLabel(ReportEventCasesVerificationSetup)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridLayout.addWidget(self.lblEndDate, 1, 0, 1, 1)
        self.cmbAidType = QtGui.QComboBox(ReportEventCasesVerificationSetup)
        self.cmbAidType.setObjectName(_fromUtf8("cmbAidType"))
        self.cmbAidType.addItem(_fromUtf8(""))
        self.cmbAidType.addItem(_fromUtf8(""))
        self.cmbAidType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbAidType, 2, 1, 1, 1)
        self.edtBegDate = CDateEdit(ReportEventCasesVerificationSetup)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        self.lblBegDate = QtGui.QLabel(ReportEventCasesVerificationSetup)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.edtEndDate = CDateEdit(ReportEventCasesVerificationSetup)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridLayout.addWidget(self.edtEndDate, 1, 1, 1, 1)
        self.lblAidType = QtGui.QLabel(ReportEventCasesVerificationSetup)
        self.lblAidType.setObjectName(_fromUtf8("lblAidType"))
        self.gridLayout.addWidget(self.lblAidType, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ReportEventCasesVerificationSetup)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 2)
        self.chkHideHeader = QtGui.QCheckBox(ReportEventCasesVerificationSetup)
        self.chkHideHeader.setObjectName(_fromUtf8("chkHideHeader"))
        self.gridLayout.addWidget(self.chkHideHeader, 4, 0, 1, 2)
        self.chkCompareUsishCode = QtGui.QCheckBox(ReportEventCasesVerificationSetup)
        self.chkCompareUsishCode.setChecked(True)
        self.chkCompareUsishCode.setObjectName(_fromUtf8("chkCompareUsishCode"))
        self.gridLayout.addWidget(self.chkCompareUsishCode, 5, 0, 1, 2)
        self.chkOnlyOMC = QtGui.QCheckBox(ReportEventCasesVerificationSetup)
        self.chkOnlyOMC.setObjectName(_fromUtf8("chkOnlyOMC"))
        self.gridLayout.addWidget(self.chkOnlyOMC, 6, 0, 1, 2)

        self.retranslateUi(ReportEventCasesVerificationSetup)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReportEventCasesVerificationSetup.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReportEventCasesVerificationSetup.reject)
        QtCore.QMetaObject.connectSlotsByName(ReportEventCasesVerificationSetup)
        ReportEventCasesVerificationSetup.setTabOrder(self.edtBegDate, self.edtEndDate)
        ReportEventCasesVerificationSetup.setTabOrder(self.edtEndDate, self.cmbAidType)
        ReportEventCasesVerificationSetup.setTabOrder(self.cmbAidType, self.chkSendIEMK)
        ReportEventCasesVerificationSetup.setTabOrder(self.chkSendIEMK, self.chkHideHeader)
        ReportEventCasesVerificationSetup.setTabOrder(self.chkHideHeader, self.chkCompareUsishCode)
        ReportEventCasesVerificationSetup.setTabOrder(self.chkCompareUsishCode, self.chkOnlyOMC)
        ReportEventCasesVerificationSetup.setTabOrder(self.chkOnlyOMC, self.buttonBox)

    def retranslateUi(self, ReportEventCasesVerificationSetup):
        ReportEventCasesVerificationSetup.setWindowTitle(_translate("ReportEventCasesVerificationSetup", "Dialog", None))
        self.chkSendIEMK.setText(_translate("ReportEventCasesVerificationSetup", "Передано в ИЭМК", None))
        self.lblEndDate.setText(_translate("ReportEventCasesVerificationSetup", "Дата окончания периода", None))
        self.cmbAidType.setItemText(0, _translate("ReportEventCasesVerificationSetup", "не задано", None))
        self.cmbAidType.setItemText(1, _translate("ReportEventCasesVerificationSetup", "амбулаторный", None))
        self.cmbAidType.setItemText(2, _translate("ReportEventCasesVerificationSetup", "стационарный", None))
        self.lblBegDate.setText(_translate("ReportEventCasesVerificationSetup", "Дата начала периода", None))
        self.lblAidType.setText(_translate("ReportEventCasesVerificationSetup", "Тип медицинской помощи", None))
        self.chkHideHeader.setText(_translate("ReportEventCasesVerificationSetup", "Скрывать шапку", None))
        self.chkCompareUsishCode.setText(_translate("ReportEventCasesVerificationSetup", "Учитывать код ЕГИСЗ Типа События", None))
        self.chkOnlyOMC.setText(_translate("ReportEventCasesVerificationSetup", "Только ОМС", None))

from library.DateEdit import CDateEdit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ReportEventCasesVerificationSetup = QtGui.QDialog()
    ui = Ui_ReportEventCasesVerificationSetup()
    ui.setupUi(ReportEventCasesVerificationSetup)
    ReportEventCasesVerificationSetup.show()
    sys.exit(app.exec_())

