# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/RefBooks/ExtraDataDefEditor.ui'
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

class Ui_ItemEditorDialog(object):
    def setupUi(self, ItemEditorDialog):
        ItemEditorDialog.setObjectName(_fromUtf8("ItemEditorDialog"))
        ItemEditorDialog.resize(587, 383)
        self.gridLayout_2 = QtGui.QGridLayout(ItemEditorDialog)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lblName = QtGui.QLabel(ItemEditorDialog)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout_2.addWidget(self.lblName, 0, 0, 1, 1)
        self.edtName = QtGui.QLineEdit(ItemEditorDialog)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout_2.addWidget(self.edtName, 0, 1, 1, 1)
        self.tabMain = QtGui.QTabWidget(ItemEditorDialog)
        self.tabMain.setEnabled(True)
        self.tabMain.setObjectName(_fromUtf8("tabMain"))
        self.tabUploadCase = QtGui.QWidget()
        self.tabUploadCase.setObjectName(_fromUtf8("tabUploadCase"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tabUploadCase)
        self.gridLayout_3.setMargin(4)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.tblUploadCases = CInDocTableView(self.tabUploadCase)
        self.tblUploadCases.setObjectName(_fromUtf8("tblUploadCases"))
        self.tblUploadCases.horizontalHeader().setHighlightSections(True)
        self.tblUploadCases.verticalHeader().setVisible(False)
        self.tblUploadCases.verticalHeader().setHighlightSections(True)
        self.gridLayout_3.addWidget(self.tblUploadCases, 1, 0, 1, 1)
        self.chkUploadEnabled = QtGui.QCheckBox(self.tabUploadCase)
        self.chkUploadEnabled.setChecked(True)
        self.chkUploadEnabled.setObjectName(_fromUtf8("chkUploadEnabled"))
        self.gridLayout_3.addWidget(self.chkUploadEnabled, 0, 0, 1, 1)
        self.tabMain.addTab(self.tabUploadCase, _fromUtf8(""))
        self.tabUploadSource = QtGui.QWidget()
        self.tabUploadSource.setObjectName(_fromUtf8("tabUploadSource"))
        self.gridLayout_4 = QtGui.QGridLayout(self.tabUploadSource)
        self.gridLayout_4.setMargin(4)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.rbSourceIsActionFromSameEvent = QtGui.QRadioButton(self.tabUploadSource)
        self.rbSourceIsActionFromSameEvent.setObjectName(_fromUtf8("rbSourceIsActionFromSameEvent"))
        self.gridLayout_4.addWidget(self.rbSourceIsActionFromSameEvent, 1, 0, 1, 2)
        self.rbSourceIsAnyAction = QtGui.QRadioButton(self.tabUploadSource)
        self.rbSourceIsAnyAction.setObjectName(_fromUtf8("rbSourceIsAnyAction"))
        self.gridLayout_4.addWidget(self.rbSourceIsAnyAction, 2, 0, 1, 2)
        self.rbSourceIsDirection = QtGui.QRadioButton(self.tabUploadSource)
        self.rbSourceIsDirection.setChecked(True)
        self.rbSourceIsDirection.setObjectName(_fromUtf8("rbSourceIsDirection"))
        self.gridLayout_4.addWidget(self.rbSourceIsDirection, 0, 0, 1, 2)
        self.tblUploadActionTypes = CInDocTableView(self.tabUploadSource)
        self.tblUploadActionTypes.setEnabled(False)
        self.tblUploadActionTypes.setObjectName(_fromUtf8("tblUploadActionTypes"))
        self.tblUploadActionTypes.verticalHeader().setVisible(False)
        self.gridLayout_4.addWidget(self.tblUploadActionTypes, 4, 0, 1, 2)
        self.lblSourceActionType = QtGui.QLabel(self.tabUploadSource)
        self.lblSourceActionType.setEnabled(False)
        self.lblSourceActionType.setObjectName(_fromUtf8("lblSourceActionType"))
        self.gridLayout_4.addWidget(self.lblSourceActionType, 3, 0, 1, 2)
        self.tabMain.addTab(self.tabUploadSource, _fromUtf8(""))
        self.tabElements = QtGui.QWidget()
        self.tabElements.setObjectName(_fromUtf8("tabElements"))
        self.gridLayout_5 = QtGui.QGridLayout(self.tabElements)
        self.gridLayout_5.setMargin(4)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.tblElements = CInDocTableView(self.tabElements)
        self.tblElements.setProperty("showDropIndicator", False)
        self.tblElements.setDragDropOverwriteMode(False)
        self.tblElements.setObjectName(_fromUtf8("tblElements"))
        self.tblElements.horizontalHeader().setHighlightSections(True)
        self.tblElements.verticalHeader().setVisible(False)
        self.gridLayout_5.addWidget(self.tblElements, 0, 0, 1, 1)
        self.tabMain.addTab(self.tabElements, _fromUtf8(""))
        self.tabDownload = QtGui.QWidget()
        self.tabDownload.setObjectName(_fromUtf8("tabDownload"))
        self.gridLayout = QtGui.QGridLayout(self.tabDownload)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.rbDestIsSeparateAction = QtGui.QRadioButton(self.tabDownload)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rbDestIsSeparateAction.sizePolicy().hasHeightForWidth())
        self.rbDestIsSeparateAction.setSizePolicy(sizePolicy)
        self.rbDestIsSeparateAction.setObjectName(_fromUtf8("rbDestIsSeparateAction"))
        self.gridLayout.addWidget(self.rbDestIsSeparateAction, 1, 0, 1, 1)
        self.cmbDestActionType = CActionTypeComboBox(self.tabDownload)
        self.cmbDestActionType.setEnabled(False)
        self.cmbDestActionType.setObjectName(_fromUtf8("cmbDestActionType"))
        self.cmbDestActionType.addItem(_fromUtf8(""))
        self.cmbDestActionType.addItem(_fromUtf8(""))
        self.cmbDestActionType.addItem(_fromUtf8(""))
        self.cmbDestActionType.addItem(_fromUtf8(""))
        self.cmbDestActionType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbDestActionType, 1, 1, 1, 1)
        self.rbDestIsDirection = QtGui.QRadioButton(self.tabDownload)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rbDestIsDirection.sizePolicy().hasHeightForWidth())
        self.rbDestIsDirection.setSizePolicy(sizePolicy)
        self.rbDestIsDirection.setChecked(True)
        self.rbDestIsDirection.setObjectName(_fromUtf8("rbDestIsDirection"))
        self.gridLayout.addWidget(self.rbDestIsDirection, 0, 0, 1, 2)
        self.tblDownloadElements = CInDocTableView(self.tabDownload)
        self.tblDownloadElements.setObjectName(_fromUtf8("tblDownloadElements"))
        self.tblDownloadElements.horizontalHeader().setHighlightSections(True)
        self.tblDownloadElements.verticalHeader().setVisible(False)
        self.tblDownloadElements.verticalHeader().setCascadingSectionResizes(False)
        self.gridLayout.addWidget(self.tblDownloadElements, 2, 0, 1, 2)
        self.tabMain.addTab(self.tabDownload, _fromUtf8(""))
        self.gridLayout_2.addWidget(self.tabMain, 1, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(ItemEditorDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 2, 0, 1, 2)
        self.lblSourceActionType.setBuddy(self.tblUploadActionTypes)

        self.retranslateUi(ItemEditorDialog)
        self.tabMain.setCurrentIndex(0)
        QtCore.QObject.connect(self.chkUploadEnabled, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.tblUploadCases.setEnabled)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ItemEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ItemEditorDialog.reject)
        QtCore.QObject.connect(self.rbSourceIsDirection, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.tblUploadActionTypes.setDisabled)
        QtCore.QObject.connect(self.rbSourceIsDirection, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.lblSourceActionType.setDisabled)
        QtCore.QObject.connect(self.rbDestIsSeparateAction, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbDestActionType.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(ItemEditorDialog)
        ItemEditorDialog.setTabOrder(self.edtName, self.tabMain)
        ItemEditorDialog.setTabOrder(self.tabMain, self.chkUploadEnabled)
        ItemEditorDialog.setTabOrder(self.chkUploadEnabled, self.tblUploadCases)
        ItemEditorDialog.setTabOrder(self.tblUploadCases, self.rbSourceIsDirection)
        ItemEditorDialog.setTabOrder(self.rbSourceIsDirection, self.rbSourceIsActionFromSameEvent)
        ItemEditorDialog.setTabOrder(self.rbSourceIsActionFromSameEvent, self.rbSourceIsAnyAction)
        ItemEditorDialog.setTabOrder(self.rbSourceIsAnyAction, self.tblUploadActionTypes)
        ItemEditorDialog.setTabOrder(self.tblUploadActionTypes, self.tblElements)
        ItemEditorDialog.setTabOrder(self.tblElements, self.rbDestIsDirection)
        ItemEditorDialog.setTabOrder(self.rbDestIsDirection, self.rbDestIsSeparateAction)
        ItemEditorDialog.setTabOrder(self.rbDestIsSeparateAction, self.cmbDestActionType)
        ItemEditorDialog.setTabOrder(self.cmbDestActionType, self.tblDownloadElements)
        ItemEditorDialog.setTabOrder(self.tblDownloadElements, self.buttonBox)

    def retranslateUi(self, ItemEditorDialog):
        ItemEditorDialog.setWindowTitle(_translate("ItemEditorDialog", "Dialog", None))
        self.lblName.setText(_translate("ItemEditorDialog", "Наименование", None))
        self.chkUploadEnabled.setText(_translate("ItemEditorDialog", "Выгрузка разрешена", None))
        self.tabMain.setTabText(self.tabMain.indexOf(self.tabUploadCase), _translate("ItemEditorDialog", "Выгружать в случае", None))
        self.rbSourceIsActionFromSameEvent.setText(_translate("ItemEditorDialog", "Выгружать из действия того же события что и направление", None))
        self.rbSourceIsAnyAction.setText(_translate("ItemEditorDialog", "Выгружать из любого действия", None))
        self.rbSourceIsDirection.setText(_translate("ItemEditorDialog", "Выгружать из направления", None))
        self.lblSourceActionType.setText(_translate("ItemEditorDialog", "Тип действия", None))
        self.tabMain.setTabText(self.tabMain.indexOf(self.tabUploadSource), _translate("ItemEditorDialog", "Выгружать из действия", None))
        self.tabMain.setTabText(self.tabMain.indexOf(self.tabElements), _translate("ItemEditorDialog", "Элементы", None))
        self.rbDestIsSeparateAction.setText(_translate("ItemEditorDialog", "Загружать в отдельное действие", None))
        self.cmbDestActionType.setItemText(0, _translate("ItemEditorDialog", "Тип действия 1", None))
        self.cmbDestActionType.setItemText(1, _translate("ItemEditorDialog", "Тип действия 2", None))
        self.cmbDestActionType.setItemText(2, _translate("ItemEditorDialog", "Тип действия 3", None))
        self.cmbDestActionType.setItemText(3, _translate("ItemEditorDialog", "Тип действия 4", None))
        self.cmbDestActionType.setItemText(4, _translate("ItemEditorDialog", "Тип действия 5", None))
        self.rbDestIsDirection.setText(_translate("ItemEditorDialog", "Загружать в действие-направление", None))
        self.tabMain.setTabText(self.tabMain.indexOf(self.tabDownload), _translate("ItemEditorDialog", "Загрузка", None))

from Events.ActionTypeComboBox import CActionTypeComboBox
from library.InDocTable import CInDocTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ItemEditorDialog = QtGui.QDialog()
    ui = Ui_ItemEditorDialog()
    ui.setupUi(ItemEditorDialog)
    ItemEditorDialog.show()
    sys.exit(app.exec_())
