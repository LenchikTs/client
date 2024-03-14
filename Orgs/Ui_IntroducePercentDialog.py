# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Orgs\IntroducePercentDialog.ui'
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

class Ui_IntroducePercentDialog(object):
    def setupUi(self, IntroducePercentDialog):
        IntroducePercentDialog.setObjectName(_fromUtf8("IntroducePercentDialog"))
        IntroducePercentDialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(IntroducePercentDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblIntroducePercent = CTableView(IntroducePercentDialog)
        self.tblIntroducePercent.setObjectName(_fromUtf8("tblIntroducePercent"))
        self.gridLayout.addWidget(self.tblIntroducePercent, 0, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(IntroducePercentDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 1, 1, 1)
        self.lblSelectionRows = QtGui.QLabel(IntroducePercentDialog)
        self.lblSelectionRows.setText(_fromUtf8(""))
        self.lblSelectionRows.setObjectName(_fromUtf8("lblSelectionRows"))
        self.gridLayout.addWidget(self.lblSelectionRows, 1, 0, 1, 1)

        self.retranslateUi(IntroducePercentDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), IntroducePercentDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), IntroducePercentDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(IntroducePercentDialog)

    def retranslateUi(self, IntroducePercentDialog):
        IntroducePercentDialog.setWindowTitle(_translate("IntroducePercentDialog", "Dialog", None))

from library.TableView import CTableView
