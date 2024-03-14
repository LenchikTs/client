# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RBNotificationKind.ui'
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

class Ui_NotificationKindEditorDialog(object):
    def setupUi(self, NotificationKindEditorDialog):
        NotificationKindEditorDialog.setObjectName(_fromUtf8("NotificationKindEditorDialog"))
        NotificationKindEditorDialog.resize(290, 132)
        NotificationKindEditorDialog.setSizeGripEnabled(False)
        self.gridlayout = QtGui.QGridLayout(NotificationKindEditorDialog)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.edtName = QtGui.QLineEdit(NotificationKindEditorDialog)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridlayout.addWidget(self.edtName, 1, 1, 1, 1)
        self.lblName = QtGui.QLabel(NotificationKindEditorDialog)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridlayout.addWidget(self.lblName, 1, 0, 1, 1)
        self.edtCode = QtGui.QLineEdit(NotificationKindEditorDialog)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridlayout.addWidget(self.edtCode, 0, 1, 1, 1)
        self.lblCode = QtGui.QLabel(NotificationKindEditorDialog)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridlayout.addWidget(self.lblCode, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(103, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 3, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(NotificationKindEditorDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.lblContactType = QtGui.QLabel(NotificationKindEditorDialog)
        self.lblContactType.setObjectName(_fromUtf8("lblContactType"))
        self.gridlayout.addWidget(self.lblContactType, 2, 0, 1, 1)
        self.cmbContactType = CRBComboBox(NotificationKindEditorDialog)
        self.cmbContactType.setObjectName(_fromUtf8("cmbContactType"))
        self.gridlayout.addWidget(self.cmbContactType, 2, 1, 1, 1)
        self.lblName.setBuddy(self.edtName)
        self.lblCode.setBuddy(self.edtCode)

        self.retranslateUi(NotificationKindEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NotificationKindEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NotificationKindEditorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NotificationKindEditorDialog)
        NotificationKindEditorDialog.setTabOrder(self.edtCode, self.edtName)
        NotificationKindEditorDialog.setTabOrder(self.edtName, self.cmbContactType)
        NotificationKindEditorDialog.setTabOrder(self.cmbContactType, self.buttonBox)

    def retranslateUi(self, NotificationKindEditorDialog):
        NotificationKindEditorDialog.setWindowTitle(_translate("NotificationKindEditorDialog", "Вид оповещения", None))
        self.lblName.setText(_translate("NotificationKindEditorDialog", "&Наименование", None))
        self.lblCode.setText(_translate("NotificationKindEditorDialog", "&Код", None))
        self.lblContactType.setText(_translate("NotificationKindEditorDialog", "Тип контакта", None))

from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    NotificationKindEditorDialog = QtGui.QDialog()
    ui = Ui_NotificationKindEditorDialog()
    ui.setupUi(NotificationKindEditorDialog)
    NotificationKindEditorDialog.show()
    sys.exit(app.exec_())

