# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/dmitrii/s11/Events/LLO78MkbSearch.ui'
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

class Ui_LLO78MkbSearchDialog(object):
    def setupUi(self, LLO78MkbSearchDialog):
        LLO78MkbSearchDialog.setObjectName(_fromUtf8("LLO78MkbSearchDialog"))
        LLO78MkbSearchDialog.resize(660, 430)
        self.gridLayout = QtGui.QGridLayout(LLO78MkbSearchDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtDiagnosisSearch = QtGui.QLineEdit(LLO78MkbSearchDialog)
        self.edtDiagnosisSearch.setObjectName(_fromUtf8("edtDiagnosisSearch"))
        self.gridLayout.addWidget(self.edtDiagnosisSearch, 0, 0, 1, 1)
        self.btnGetMkb = QtGui.QPushButton(LLO78MkbSearchDialog)
        self.btnGetMkb.setObjectName(_fromUtf8("btnGetMkb"))
        self.gridLayout.addWidget(self.btnGetMkb, 0, 1, 1, 1)
        self.tblRecievedDiagnosises = QtGui.QTableWidget(LLO78MkbSearchDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblRecievedDiagnosises.sizePolicy().hasHeightForWidth())
        self.tblRecievedDiagnosises.setSizePolicy(sizePolicy)
        self.tblRecievedDiagnosises.setMinimumSize(QtCore.QSize(0, 0))
        self.tblRecievedDiagnosises.setRowCount(0)
        self.tblRecievedDiagnosises.setColumnCount(0)
        self.tblRecievedDiagnosises.setObjectName(_fromUtf8("tblRecievedDiagnosises"))
        self.tblRecievedDiagnosises.horizontalHeader().setCascadingSectionResizes(True)
        self.tblRecievedDiagnosises.horizontalHeader().setStretchLastSection(True)
        self.tblRecievedDiagnosises.verticalHeader().setCascadingSectionResizes(False)
        self.tblRecievedDiagnosises.verticalHeader().setStretchLastSection(False)
        self.gridLayout.addWidget(self.tblRecievedDiagnosises, 1, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(LLO78MkbSearchDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)

        self.retranslateUi(LLO78MkbSearchDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), LLO78MkbSearchDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), LLO78MkbSearchDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(LLO78MkbSearchDialog)

    def retranslateUi(self, LLO78MkbSearchDialog):
        LLO78MkbSearchDialog.setWindowTitle(_translate("LLO78MkbSearchDialog", "Поиск диагноза", None))
        self.btnGetMkb.setText(_translate("LLO78MkbSearchDialog", "Найти", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    LLO78MkbSearchDialog = QtGui.QDialog()
    ui = Ui_LLO78MkbSearchDialog()
    ui.setupUi(LLO78MkbSearchDialog)
    LLO78MkbSearchDialog.show()
    sys.exit(app.exec_())

