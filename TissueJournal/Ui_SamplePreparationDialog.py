# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\TissueJournal\SamplePreparationDialog.ui'
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

class Ui_SamplePreparationDialog(object):
    def setupUi(self, SamplePreparationDialog):
        SamplePreparationDialog.setObjectName(_fromUtf8("SamplePreparationDialog"))
        SamplePreparationDialog.resize(850, 716)
        SamplePreparationDialog.setSizeGripEnabled(True)
        self.gridLayout_2 = QtGui.QGridLayout(SamplePreparationDialog)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.splitter = QtGui.QSplitter(SamplePreparationDialog)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.pnlInfo = QtGui.QWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pnlInfo.sizePolicy().hasHeightForWidth())
        self.pnlInfo.setSizePolicy(sizePolicy)
        self.pnlInfo.setObjectName(_fromUtf8("pnlInfo"))
        self.verticalLayout = QtGui.QVBoxLayout(self.pnlInfo)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.textBrowser = CTextBrowser(self.pnlInfo)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.verticalLayout.addWidget(self.textBrowser)
        self.lblTissueRecordInfo = QtGui.QLabel(self.pnlInfo)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTissueRecordInfo.sizePolicy().hasHeightForWidth())
        self.lblTissueRecordInfo.setSizePolicy(sizePolicy)
        self.lblTissueRecordInfo.setObjectName(_fromUtf8("lblTissueRecordInfo"))
        self.verticalLayout.addWidget(self.lblTissueRecordInfo)
        self.pnlItems = QtGui.QWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pnlItems.sizePolicy().hasHeightForWidth())
        self.pnlItems.setSizePolicy(sizePolicy)
        self.pnlItems.setObjectName(_fromUtf8("pnlItems"))
        self.gridLayout = QtGui.QGridLayout(self.pnlItems)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblEquipment = QtGui.QLabel(self.pnlItems)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblEquipment.sizePolicy().hasHeightForWidth())
        self.lblEquipment.setSizePolicy(sizePolicy)
        self.lblEquipment.setObjectName(_fromUtf8("lblEquipment"))
        self.gridLayout.addWidget(self.lblEquipment, 0, 0, 1, 1)
        self.cmbEquipment = CRBComboBox(self.pnlItems)
        self.cmbEquipment.setObjectName(_fromUtf8("cmbEquipment"))
        self.gridLayout.addWidget(self.cmbEquipment, 0, 1, 1, 1)
        self.lblTestGroup = QtGui.QLabel(self.pnlItems)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblTestGroup.sizePolicy().hasHeightForWidth())
        self.lblTestGroup.setSizePolicy(sizePolicy)
        self.lblTestGroup.setObjectName(_fromUtf8("lblTestGroup"))
        self.gridLayout.addWidget(self.lblTestGroup, 0, 2, 1, 1)
        self.cmbTestGroup = CRBComboBox(self.pnlItems)
        self.cmbTestGroup.setObjectName(_fromUtf8("cmbTestGroup"))
        self.gridLayout.addWidget(self.cmbTestGroup, 0, 3, 1, 1)
        self.tblSamplePreparation = CSamplePreparationInDocTableView(self.pnlItems)
        self.tblSamplePreparation.setObjectName(_fromUtf8("tblSamplePreparation"))
        self.gridLayout.addWidget(self.tblSamplePreparation, 1, 0, 1, 5)
        self.btnSelectItems = QtGui.QPushButton(self.pnlItems)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSelectItems.sizePolicy().hasHeightForWidth())
        self.btnSelectItems.setSizePolicy(sizePolicy)
        self.btnSelectItems.setObjectName(_fromUtf8("btnSelectItems"))
        self.gridLayout.addWidget(self.btnSelectItems, 0, 4, 1, 1)
        self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 5)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.btnApply = QtGui.QPushButton(SamplePreparationDialog)
        self.btnApply.setObjectName(_fromUtf8("btnApply"))
        self.gridLayout_2.addWidget(self.btnApply, 1, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(SamplePreparationDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 1, 4, 1, 1)
        self.btnSetEquipment = QtGui.QPushButton(SamplePreparationDialog)
        self.btnSetEquipment.setObjectName(_fromUtf8("btnSetEquipment"))
        self.gridLayout_2.addWidget(self.btnSetEquipment, 1, 3, 1, 1)

        self.retranslateUi(SamplePreparationDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SamplePreparationDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SamplePreparationDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SamplePreparationDialog)

    def retranslateUi(self, SamplePreparationDialog):
        SamplePreparationDialog.setWindowTitle(_translate("SamplePreparationDialog", "Dialog", None))
        self.lblTissueRecordInfo.setText(_translate("SamplePreparationDialog", "Информация о биоматериале", None))
        self.lblEquipment.setText(_translate("SamplePreparationDialog", "Оборудование", None))
        self.lblTestGroup.setText(_translate("SamplePreparationDialog", "Группа тестов", None))
        self.btnSelectItems.setText(_translate("SamplePreparationDialog", "Выбрать", None))
        self.btnApply.setText(_translate("SamplePreparationDialog", "Регистрация проб", None))
        self.btnSetEquipment.setText(_translate("SamplePreparationDialog", "Назначить оборудование", None))

from TissueJournal.TissueJournalModels import CSamplePreparationInDocTableView
from library.TextBrowser import CTextBrowser
from library.crbcombobox import CRBComboBox
