# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\projects\samson\UP_s11\client\Events\ActionRelations\AddRelatedAction.ui'
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

class Ui_AddRelatedAction(object):
    def setupUi(self, AddRelatedAction):
        AddRelatedAction.setObjectName(_fromUtf8("AddRelatedAction"))
        AddRelatedAction.resize(971, 399)
        AddRelatedAction.setSizeGripEnabled(False)
        self.gridLayout_2 = QtGui.QGridLayout(AddRelatedAction)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.buttonBox = QtGui.QDialogButtonBox(AddRelatedAction)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 1, 1, 1, 1)
        self.splitter_2 = QtGui.QSplitter(AddRelatedAction)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.pnlActionTypes = QtGui.QWidget(self.splitter_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pnlActionTypes.sizePolicy().hasHeightForWidth())
        self.pnlActionTypes.setSizePolicy(sizePolicy)
        self.pnlActionTypes.setObjectName(_fromUtf8("pnlActionTypes"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.pnlActionTypes)
        self.verticalLayout_5.setMargin(0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.splitter = QtGui.QSplitter(self.pnlActionTypes)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.tblActionTypes = CTableView(self.splitter)
        self.tblActionTypes.setObjectName(_fromUtf8("tblActionTypes"))
        self.verticalLayout_5.addWidget(self.splitter)
        self.gridLayout_2.addWidget(self.splitter_2, 0, 0, 1, 2)

        self.retranslateUi(AddRelatedAction)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AddRelatedAction.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AddRelatedAction.reject)
        QtCore.QMetaObject.connectSlotsByName(AddRelatedAction)
        AddRelatedAction.setTabOrder(self.tblActionTypes, self.buttonBox)

    def retranslateUi(self, AddRelatedAction):
        AddRelatedAction.setWindowTitle(_translate("AddRelatedAction", "Выберите действия", None))

from library.TableView import CTableView
