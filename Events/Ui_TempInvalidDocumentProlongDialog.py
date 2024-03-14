# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/Events/TempInvalidDocumentProlongDialog.ui'
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

class Ui_TempInvalidDocumentProlongDialog(object):
    def setupUi(self, TempInvalidDocumentProlongDialog):
        TempInvalidDocumentProlongDialog.setObjectName(_fromUtf8("TempInvalidDocumentProlongDialog"))
        TempInvalidDocumentProlongDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        TempInvalidDocumentProlongDialog.resize(766, 367)
        self.gridLayout = QtGui.QGridLayout(TempInvalidDocumentProlongDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblDocuments = CTempInvalidDocumentsInDocTableView(TempInvalidDocumentProlongDialog)
        self.tblDocuments.setObjectName(_fromUtf8("tblDocuments"))
        self.gridLayout.addWidget(self.tblDocuments, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(TempInvalidDocumentProlongDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(TempInvalidDocumentProlongDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TempInvalidDocumentProlongDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TempInvalidDocumentProlongDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TempInvalidDocumentProlongDialog)
        TempInvalidDocumentProlongDialog.setTabOrder(self.tblDocuments, self.buttonBox)

    def retranslateUi(self, TempInvalidDocumentProlongDialog):
        TempInvalidDocumentProlongDialog.setWindowTitle(_translate("TempInvalidDocumentProlongDialog", "Продлить документы временной нетрудоспособности", None))

from Events.TempInvalidDocumentsInDocTableView import CTempInvalidDocumentsInDocTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TempInvalidDocumentProlongDialog = QtGui.QDialog()
    ui = Ui_TempInvalidDocumentProlongDialog()
    ui.setupUi(TempInvalidDocumentProlongDialog)
    TempInvalidDocumentProlongDialog.show()
    sys.exit(app.exec_())

