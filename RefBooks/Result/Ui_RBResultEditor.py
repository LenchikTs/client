# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/RefBooks/RBResultEditor.ui'
#
# Created: Tue Apr 12 16:08:49 2016
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_ItemEditorDialog(object):
    def setupUi(self, ItemEditorDialog):
        ItemEditorDialog.setObjectName(_fromUtf8("ItemEditorDialog"))
        ItemEditorDialog.resize(320, 293)
        ItemEditorDialog.setSizeGripEnabled(True)
        self.gridlayout = QtGui.QGridLayout(ItemEditorDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.edtEndDate = CDateEdit(ItemEditorDialog)
        self.edtEndDate.setCalendarPopup(True)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.gridlayout.addWidget(self.edtEndDate, 10, 1, 1, 1)
        self.edtBegDate = CDateEdit(ItemEditorDialog)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridlayout.addWidget(self.edtBegDate, 9, 1, 1, 1)
        self.lblBegDate = QtGui.QLabel(ItemEditorDialog)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridlayout.addWidget(self.lblBegDate, 9, 0, 1, 1)
        self.label = QtGui.QLabel(ItemEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridlayout.addWidget(self.label, 0, 0, 1, 1)
        self.lblUsishCode = QtGui.QLabel(ItemEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblUsishCode.sizePolicy().hasHeightForWidth())
        self.lblUsishCode.setSizePolicy(sizePolicy)
        self.lblUsishCode.setObjectName(_fromUtf8("lblUsishCode"))
        self.gridlayout.addWidget(self.lblUsishCode, 5, 0, 1, 1)
        self.lblCode = QtGui.QLabel(ItemEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridlayout.addWidget(self.lblCode, 1, 0, 1, 1)
        self.lblFederalCode = QtGui.QLabel(ItemEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblFederalCode.sizePolicy().hasHeightForWidth())
        self.lblFederalCode.setSizePolicy(sizePolicy)
        self.lblFederalCode.setObjectName(_fromUtf8("lblFederalCode"))
        self.gridlayout.addWidget(self.lblFederalCode, 4, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(103, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 11, 0, 1, 1)
        self.lblName = QtGui.QLabel(ItemEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridlayout.addWidget(self.lblName, 2, 0, 1, 1)
        self.lblRegionalCode = QtGui.QLabel(ItemEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblRegionalCode.sizePolicy().hasHeightForWidth())
        self.lblRegionalCode.setSizePolicy(sizePolicy)
        self.lblRegionalCode.setObjectName(_fromUtf8("lblRegionalCode"))
        self.gridlayout.addWidget(self.lblRegionalCode, 6, 0, 1, 1)
        self.lblEndDate = QtGui.QLabel(ItemEditorDialog)
        self.lblEndDate.setObjectName(_fromUtf8("lblEndDate"))
        self.gridlayout.addWidget(self.lblEndDate, 10, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1, 9, 2, 1, 1)
        self.edtRegionalCode = QtGui.QLineEdit(ItemEditorDialog)
        self.edtRegionalCode.setMaxLength(8)
        self.edtRegionalCode.setObjectName(_fromUtf8("edtRegionalCode"))
        self.gridlayout.addWidget(self.edtRegionalCode, 6, 1, 1, 2)
        self.edtUsishCode = QtGui.QLineEdit(ItemEditorDialog)
        self.edtUsishCode.setObjectName(_fromUtf8("edtUsishCode"))
        self.gridlayout.addWidget(self.edtUsishCode, 5, 1, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(ItemEditorDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 12, 0, 1, 3)
        self.edtFederalCode = QtGui.QLineEdit(ItemEditorDialog)
        self.edtFederalCode.setObjectName(_fromUtf8("edtFederalCode"))
        self.gridlayout.addWidget(self.edtFederalCode, 4, 1, 1, 2)
        self.edtName = QtGui.QLineEdit(ItemEditorDialog)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridlayout.addWidget(self.edtName, 2, 1, 1, 2)
        self.edtCode = QtGui.QLineEdit(ItemEditorDialog)
        self.edtCode.setMaxLength(8)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridlayout.addWidget(self.edtCode, 1, 1, 1, 2)
        self.cmbEventPurpose = CRBComboBox(ItemEditorDialog)
        self.cmbEventPurpose.setObjectName(_fromUtf8("cmbEventPurpose"))
        self.gridlayout.addWidget(self.cmbEventPurpose, 0, 1, 1, 2)
        self.chkContinued = QtGui.QCheckBox(ItemEditorDialog)
        self.chkContinued.setObjectName(_fromUtf8("chkContinued"))
        self.gridlayout.addWidget(self.chkContinued, 8, 1, 1, 2)
        self.label.setBuddy(self.cmbEventPurpose)
        self.lblUsishCode.setBuddy(self.edtUsishCode)
        self.lblCode.setBuddy(self.edtCode)
        self.lblFederalCode.setBuddy(self.edtFederalCode)
        self.lblName.setBuddy(self.edtName)
        self.lblRegionalCode.setBuddy(self.edtRegionalCode)

        self.retranslateUi(ItemEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ItemEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ItemEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ItemEditorDialog)
        ItemEditorDialog.setTabOrder(self.cmbEventPurpose, self.edtCode)
        ItemEditorDialog.setTabOrder(self.edtCode, self.edtName)
        ItemEditorDialog.setTabOrder(self.edtName, self.edtFederalCode)
        ItemEditorDialog.setTabOrder(self.edtFederalCode, self.edtUsishCode)
        ItemEditorDialog.setTabOrder(self.edtUsishCode, self.edtRegionalCode)
        ItemEditorDialog.setTabOrder(self.edtRegionalCode, self.chkContinued)
        ItemEditorDialog.setTabOrder(self.chkContinued, self.edtBegDate)
        ItemEditorDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        ItemEditorDialog.setTabOrder(self.edtEndDate, self.buttonBox)

    def retranslateUi(self, ItemEditorDialog):
        ItemEditorDialog.setWindowTitle(_translate("ItemEditorDialog", "ChangeMe!", None))
        self.edtEndDate.setDisplayFormat(_translate("ItemEditorDialog", "dd.MM.yyyy", None))
        self.edtBegDate.setDisplayFormat(_translate("ItemEditorDialog", "dd.MM.yyyy", None))
        self.lblBegDate.setText(_translate("ItemEditorDialog", "Дата начала", None))
        self.label.setText(_translate("ItemEditorDialog", "Назначение", None))
        self.lblUsishCode.setText(_translate("ItemEditorDialog", "Код &ЕГИСЗ", None))
        self.lblCode.setText(_translate("ItemEditorDialog", "&Код", None))
        self.lblFederalCode.setText(_translate("ItemEditorDialog", "&Федеральный код", None))
        self.lblName.setText(_translate("ItemEditorDialog", "&Наименование", None))
        self.lblRegionalCode.setText(_translate("ItemEditorDialog", "&Региональный код", None))
        self.lblEndDate.setText(_translate("ItemEditorDialog", "Дата окончания", None))
        self.chkContinued.setText(_translate("ItemEditorDialog", "&Не закончен", None))

from library.crbcombobox import CRBComboBox
from library.DateEdit import CDateEdit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ItemEditorDialog = QtGui.QDialog()
    ui = Ui_ItemEditorDialog()
    ui.setupUi(ItemEditorDialog)
    ItemEditorDialog.show()
    sys.exit(app.exec_())

