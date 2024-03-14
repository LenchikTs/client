# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\soc-inform\TissueJournal\ActionTableRedactor.ui'
#
# Created: Fri Sep 21 09:19:47 2018
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_ActionTableRedactorDialog(object):
    def setupUi(self, ActionTableRedactorDialog):
        ActionTableRedactorDialog.setObjectName(_fromUtf8("ActionTableRedactorDialog"))
        ActionTableRedactorDialog.resize(702, 596)
        self.gridLayout_2 = QtGui.QGridLayout(ActionTableRedactorDialog)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.splitter = QtGui.QSplitter(ActionTableRedactorDialog)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.pnlInfo = QtGui.QWidget(self.splitter)
        self.pnlInfo.setObjectName(_fromUtf8("pnlInfo"))
        self.gridLayout = QtGui.QGridLayout(self.pnlInfo)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.txtClientInfoBrowser = CTextBrowser(self.pnlInfo)
        self.txtClientInfoBrowser.setObjectName(_fromUtf8("txtClientInfoBrowser"))
        self.gridLayout.addWidget(self.txtClientInfoBrowser, 0, 0, 1, 1)
        self.lblTissueJournalRecordInfo = QtGui.QLabel(self.pnlInfo)
        self.lblTissueJournalRecordInfo.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lblTissueJournalRecordInfo.setFrameShadow(QtGui.QFrame.Sunken)
        self.lblTissueJournalRecordInfo.setWordWrap(True)
        self.lblTissueJournalRecordInfo.setMargin(0)
        self.lblTissueJournalRecordInfo.setObjectName(_fromUtf8("lblTissueJournalRecordInfo"))
        self.gridLayout.addWidget(self.lblTissueJournalRecordInfo, 1, 0, 1, 1)
        self.tblActions = CActionRedactorTableView(self.splitter)
        self.tblActions.setObjectName(_fromUtf8("tblActions"))
        self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ActionTableRedactorDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(ActionTableRedactorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ActionTableRedactorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ActionTableRedactorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ActionTableRedactorDialog)

    def retranslateUi(self, ActionTableRedactorDialog):
        ActionTableRedactorDialog.setWindowTitle(_translate("ActionTableRedactorDialog", "Dialog", None))
        self.lblTissueJournalRecordInfo.setText(_translate("ActionTableRedactorDialog", "Информация о записи в журнале забора ткани", None))

from TissueJournal.TissueJournalModels import CActionRedactorTableView
from library.TextBrowser import CTextBrowser
