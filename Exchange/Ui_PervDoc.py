# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\PervDoc.ui'
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

class Ui_PervDocDialog(object):
    def setupUi(self, PervDocDialog):
        PervDocDialog.setObjectName(_fromUtf8("PervDocDialog"))
        PervDocDialog.resize(662, 512)
        self.gridLayout = QtGui.QGridLayout(PervDocDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.treeContracts = QtGui.QTreeView(PervDocDialog)
        self.treeContracts.setObjectName(_fromUtf8("treeContracts"))
        self.gridLayout.addWidget(self.treeContracts, 0, 0, 5, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblAnalysisEndDate_2 = QtGui.QLabel(PervDocDialog)
        self.lblAnalysisEndDate_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblAnalysisEndDate_2.setObjectName(_fromUtf8("lblAnalysisEndDate_2"))
        self.horizontalLayout.addWidget(self.lblAnalysisEndDate_2)
        self.edtBegDate = CDateEdit(PervDocDialog)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.horizontalLayout.addWidget(self.edtBegDate)
        self.lblAnalysisEndDate = QtGui.QLabel(PervDocDialog)
        self.lblAnalysisEndDate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblAnalysisEndDate.setObjectName(_fromUtf8("lblAnalysisEndDate"))
        self.horizontalLayout.addWidget(self.lblAnalysisEndDate)
        self.edtEndDate = CDateEdit(PervDocDialog)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.horizontalLayout.addWidget(self.edtEndDate)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(PervDocDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.edtDate = CDateEdit(PervDocDialog)
        self.edtDate.setObjectName(_fromUtf8("edtDate"))
        self.horizontalLayout_2.addWidget(self.edtDate)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(PervDocDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.boxPeriod = QtGui.QSpinBox(PervDocDialog)
        self.boxPeriod.setObjectName(_fromUtf8("boxPeriod"))
        self.horizontalLayout_3.addWidget(self.boxPeriod)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 1, 1, 1)
        self.chkPerevystavl = QtGui.QCheckBox(PervDocDialog)
        self.chkPerevystavl.setChecked(True)
        self.chkPerevystavl.setObjectName(_fromUtf8("chkPerevystavl"))
        self.gridLayout.addWidget(self.chkPerevystavl, 3, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 329, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(PervDocDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 2)
        self.lblAnalysisEndDate_2.setBuddy(self.edtEndDate)
        self.lblAnalysisEndDate.setBuddy(self.edtEndDate)

        self.retranslateUi(PervDocDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PervDocDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PervDocDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PervDocDialog)

    def retranslateUi(self, PervDocDialog):
        PervDocDialog.setWindowTitle(_translate("PervDocDialog", "Экспорт первичных документов", None))
        self.lblAnalysisEndDate_2.setText(_translate("PervDocDialog", "Дата закрытия с", None))
        self.lblAnalysisEndDate.setText(_translate("PervDocDialog", "по", None))
        self.label.setText(_translate("PervDocDialog", "дата посылки", None))
        self.label_2.setText(_translate("PervDocDialog", "отчётный месяц", None))
        self.chkPerevystavl.setText(_translate("PervDocDialog", "включать подлежащие перевыставлению", None))

from library.DateEdit import CDateEdit
