# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/Resources/TreatmentSchemeTypeDialog.ui'
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

class Ui_TreatmentSchemeTypeDialog(object):
    def setupUi(self, TreatmentSchemeTypeDialog):
        TreatmentSchemeTypeDialog.setObjectName(_fromUtf8("TreatmentSchemeTypeDialog"))
        TreatmentSchemeTypeDialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(TreatmentSchemeTypeDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblTreatmentSchemeType = CTableView(TreatmentSchemeTypeDialog)
        self.tblTreatmentSchemeType.setObjectName(_fromUtf8("tblTreatmentSchemeType"))
        self.gridLayout.addWidget(self.tblTreatmentSchemeType, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(TreatmentSchemeTypeDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(TreatmentSchemeTypeDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TreatmentSchemeTypeDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TreatmentSchemeTypeDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TreatmentSchemeTypeDialog)

    def retranslateUi(self, TreatmentSchemeTypeDialog):
        TreatmentSchemeTypeDialog.setWindowTitle(_translate("TreatmentSchemeTypeDialog", "Выберите План цикла", None))

from library.TableView import CTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TreatmentSchemeTypeDialog = QtGui.QDialog()
    ui = Ui_TreatmentSchemeTypeDialog()
    ui.setupUi(TreatmentSchemeTypeDialog)
    TreatmentSchemeTypeDialog.show()
    sys.exit(app.exec_())

