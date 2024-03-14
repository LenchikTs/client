# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\user\Documents\svn\HospitalBeds\UpdateDateSurgeryDialog.ui'
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

class Ui_UpdateDateSurgeryDialog(object):
    def setupUi(self, UpdateDateSurgeryDialog):
        UpdateDateSurgeryDialog.setObjectName(_fromUtf8("UpdateDateSurgeryDialog"))
        UpdateDateSurgeryDialog.resize(347, 72)
        UpdateDateSurgeryDialog.setSizeGripEnabled(False)
        self.gridLayout = QtGui.QGridLayout(UpdateDateSurgeryDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(103, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.lblSurgeryDate = QtGui.QLabel(UpdateDateSurgeryDialog)
        self.lblSurgeryDate.setObjectName(_fromUtf8("lblSurgeryDate"))
        self.gridLayout.addWidget(self.lblSurgeryDate, 0, 0, 1, 1)
        self.edtSurgeryDate = CDateEdit(UpdateDateSurgeryDialog)
        self.edtSurgeryDate.setCalendarPopup(True)
        self.edtSurgeryDate.setObjectName(_fromUtf8("edtSurgeryDate"))
        self.gridLayout.addWidget(self.edtSurgeryDate, 0, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(UpdateDateSurgeryDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 3)

        self.retranslateUi(UpdateDateSurgeryDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), UpdateDateSurgeryDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), UpdateDateSurgeryDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(UpdateDateSurgeryDialog)

    def retranslateUi(self, UpdateDateSurgeryDialog):
        UpdateDateSurgeryDialog.setWindowTitle(_translate("UpdateDateSurgeryDialog", "Изменение даты операции", None))
        self.lblSurgeryDate.setText(_translate("UpdateDateSurgeryDialog", "Дата операции", None))
        self.edtSurgeryDate.setDisplayFormat(_translate("UpdateDateSurgeryDialog", "dd.MM.yyyy", None))

from library.DateEdit import CDateEdit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    UpdateDateSurgeryDialog = QtGui.QDialog()
    ui = Ui_UpdateDateSurgeryDialog()
    ui.setupUi(UpdateDateSurgeryDialog)
    UpdateDateSurgeryDialog.show()
    sys.exit(app.exec_())

