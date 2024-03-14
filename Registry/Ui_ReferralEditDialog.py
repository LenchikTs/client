# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/Registry/ReferralEditDialog.ui'
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

class Ui_ReferralEditDialog(object):
    def setupUi(self, ReferralEditDialog):
        ReferralEditDialog.setObjectName(_fromUtf8("ReferralEditDialog"))
        ReferralEditDialog.resize(342, 185)
        self.gridLayout = QtGui.QGridLayout(ReferralEditDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblSrcNumber = QtGui.QLabel(ReferralEditDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblSrcNumber.sizePolicy().hasHeightForWidth())
        self.lblSrcNumber.setSizePolicy(sizePolicy)
        self.lblSrcNumber.setObjectName(_fromUtf8("lblSrcNumber"))
        self.gridLayout.addWidget(self.lblSrcNumber, 3, 0, 1, 1)
        self.lblSrcOrg = QtGui.QLabel(ReferralEditDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblSrcOrg.sizePolicy().hasHeightForWidth())
        self.lblSrcOrg.setSizePolicy(sizePolicy)
        self.lblSrcOrg.setObjectName(_fromUtf8("lblSrcOrg"))
        self.gridLayout.addWidget(self.lblSrcOrg, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)
        self.edtSrcDate = CDateEdit(ReferralEditDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtSrcDate.sizePolicy().hasHeightForWidth())
        self.edtSrcDate.setSizePolicy(sizePolicy)
        self.edtSrcDate.setCalendarPopup(True)
        self.edtSrcDate.setObjectName(_fromUtf8("edtSrcDate"))
        self.gridLayout.addWidget(self.edtSrcDate, 4, 1, 1, 1)
        self.lblSrcDate = QtGui.QLabel(ReferralEditDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblSrcDate.sizePolicy().hasHeightForWidth())
        self.lblSrcDate.setSizePolicy(sizePolicy)
        self.lblSrcDate.setObjectName(_fromUtf8("lblSrcDate"))
        self.gridLayout.addWidget(self.lblSrcDate, 4, 0, 1, 1)
        self.cmbSrcOrg = CPolyclinicComboBox(ReferralEditDialog)
        self.cmbSrcOrg.setObjectName(_fromUtf8("cmbSrcOrg"))
        self.gridLayout.addWidget(self.cmbSrcOrg, 0, 1, 1, 2)
        self.btnSelectSrcOrg = QtGui.QToolButton(ReferralEditDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSelectSrcOrg.sizePolicy().hasHeightForWidth())
        self.btnSelectSrcOrg.setSizePolicy(sizePolicy)
        self.btnSelectSrcOrg.setObjectName(_fromUtf8("btnSelectSrcOrg"))
        self.gridLayout.addWidget(self.btnSelectSrcOrg, 0, 3, 1, 1)
        self.edtSrcNumber = QtGui.QLineEdit(ReferralEditDialog)
        self.edtSrcNumber.setMaxLength(16)
        self.edtSrcNumber.setObjectName(_fromUtf8("edtSrcNumber"))
        self.gridLayout.addWidget(self.edtSrcNumber, 3, 1, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 4, 2, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(ReferralEditDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 4)
        self.lblSrcSpeciality = QtGui.QLabel(ReferralEditDialog)
        self.lblSrcSpeciality.setObjectName(_fromUtf8("lblSrcSpeciality"))
        self.gridLayout.addWidget(self.lblSrcSpeciality, 2, 0, 1, 1)
        self.cmbSrcSpeciality = CRBComboBox(ReferralEditDialog)
        self.cmbSrcSpeciality.setObjectName(_fromUtf8("cmbSrcSpeciality"))
        self.gridLayout.addWidget(self.cmbSrcSpeciality, 2, 1, 1, 3)
        self.lblSrcPerson = QtGui.QLabel(ReferralEditDialog)
        self.lblSrcPerson.setObjectName(_fromUtf8("lblSrcPerson"))
        self.gridLayout.addWidget(self.lblSrcPerson, 1, 0, 1, 1)
        self.edtSrcPerson = QtGui.QLineEdit(ReferralEditDialog)
        self.edtSrcPerson.setMaxLength(64)
        self.edtSrcPerson.setObjectName(_fromUtf8("edtSrcPerson"))
        self.gridLayout.addWidget(self.edtSrcPerson, 1, 1, 1, 3)
        self.lblSrcNumber.setBuddy(self.edtSrcNumber)
        self.lblSrcOrg.setBuddy(self.cmbSrcOrg)
        self.lblSrcDate.setBuddy(self.edtSrcDate)
        self.lblSrcSpeciality.setBuddy(self.cmbSrcSpeciality)
        self.lblSrcPerson.setBuddy(self.edtSrcPerson)

        self.retranslateUi(ReferralEditDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ReferralEditDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ReferralEditDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ReferralEditDialog)
        ReferralEditDialog.setTabOrder(self.cmbSrcOrg, self.btnSelectSrcOrg)
        ReferralEditDialog.setTabOrder(self.btnSelectSrcOrg, self.edtSrcPerson)
        ReferralEditDialog.setTabOrder(self.edtSrcPerson, self.cmbSrcSpeciality)
        ReferralEditDialog.setTabOrder(self.cmbSrcSpeciality, self.edtSrcNumber)
        ReferralEditDialog.setTabOrder(self.edtSrcNumber, self.edtSrcDate)
        ReferralEditDialog.setTabOrder(self.edtSrcDate, self.buttonBox)

    def retranslateUi(self, ReferralEditDialog):
        ReferralEditDialog.setWindowTitle(_translate("ReferralEditDialog", "Направление", None))
        self.lblSrcNumber.setText(_translate("ReferralEditDialog", "&Номер", None))
        self.lblSrcOrg.setText(_translate("ReferralEditDialog", "&Направитель", None))
        self.edtSrcDate.setDisplayFormat(_translate("ReferralEditDialog", "dd.MM.yyyy", None))
        self.lblSrcDate.setText(_translate("ReferralEditDialog", "&Дата", None))
        self.btnSelectSrcOrg.setText(_translate("ReferralEditDialog", "...", None))
        self.lblSrcSpeciality.setText(_translate("ReferralEditDialog", "&Специальность", None))
        self.lblSrcPerson.setText(_translate("ReferralEditDialog", "&Врач", None))

from Orgs.OrgComboBox import CPolyclinicComboBox
from library.DateEdit import CDateEdit
from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ReferralEditDialog = QtGui.QDialog()
    ui = Ui_ReferralEditDialog()
    ui.setupUi(ReferralEditDialog)
    ReferralEditDialog.show()
    sys.exit(app.exec_())

