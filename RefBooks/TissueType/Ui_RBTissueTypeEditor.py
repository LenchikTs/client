# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/RefBooks/RBTissueTypeEditor.ui'
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

class Ui_TissueTypeEditorDialog(object):
    def setupUi(self, TissueTypeEditorDialog):
        TissueTypeEditorDialog.setObjectName(_fromUtf8("TissueTypeEditorDialog"))
        TissueTypeEditorDialog.resize(400, 225)
        TissueTypeEditorDialog.setSizeGripEnabled(True)
        self.gridLayout_2 = QtGui.QGridLayout(TissueTypeEditorDialog)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.buttonBox = QtGui.QDialogButtonBox(TissueTypeEditorDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 3, 0, 1, 2)
        self.tabWidget = QtGui.QTabWidget(TissueTypeEditorDialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabMain = QtGui.QWidget()
        self.tabMain.setObjectName(_fromUtf8("tabMain"))
        self.gridLayout = QtGui.QGridLayout(self.tabMain)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.chkCounterManualInput = QtGui.QCheckBox(self.tabMain)
        self.chkCounterManualInput.setText(_fromUtf8(""))
        self.chkCounterManualInput.setObjectName(_fromUtf8("chkCounterManualInput"))
        self.gridLayout.addWidget(self.chkCounterManualInput, 4, 1, 1, 1)
        self.lblResetCounterType = QtGui.QLabel(self.tabMain)
        self.lblResetCounterType.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblResetCounterType.sizePolicy().hasHeightForWidth())
        self.lblResetCounterType.setSizePolicy(sizePolicy)
        self.lblResetCounterType.setObjectName(_fromUtf8("lblResetCounterType"))
        self.gridLayout.addWidget(self.lblResetCounterType, 5, 0, 1, 1)
        self.lblCounterManualInput = QtGui.QLabel(self.tabMain)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCounterManualInput.sizePolicy().hasHeightForWidth())
        self.lblCounterManualInput.setSizePolicy(sizePolicy)
        self.lblCounterManualInput.setObjectName(_fromUtf8("lblCounterManualInput"))
        self.gridLayout.addWidget(self.lblCounterManualInput, 4, 0, 1, 1)
        self.lblIsRealTimeProcessing = QtGui.QLabel(self.tabMain)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblIsRealTimeProcessing.sizePolicy().hasHeightForWidth())
        self.lblIsRealTimeProcessing.setSizePolicy(sizePolicy)
        self.lblIsRealTimeProcessing.setObjectName(_fromUtf8("lblIsRealTimeProcessing"))
        self.gridLayout.addWidget(self.lblIsRealTimeProcessing, 7, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 8, 0, 1, 1)
        self.lblSex = QtGui.QLabel(self.tabMain)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblSex.sizePolicy().hasHeightForWidth())
        self.lblSex.setSizePolicy(sizePolicy)
        self.lblSex.setObjectName(_fromUtf8("lblSex"))
        self.gridLayout.addWidget(self.lblSex, 3, 0, 1, 1)
        self.chkIsRealTimeProcessing = QtGui.QCheckBox(self.tabMain)
        self.chkIsRealTimeProcessing.setText(_fromUtf8(""))
        self.chkIsRealTimeProcessing.setObjectName(_fromUtf8("chkIsRealTimeProcessing"))
        self.gridLayout.addWidget(self.chkIsRealTimeProcessing, 7, 1, 1, 1)
        self.lblCounter = QtGui.QLabel(self.tabMain)
        self.lblCounter.setEnabled(True)
        self.lblCounter.setObjectName(_fromUtf8("lblCounter"))
        self.gridLayout.addWidget(self.lblCounter, 6, 0, 1, 1)
        self.cmbSex = QtGui.QComboBox(self.tabMain)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbSex.sizePolicy().hasHeightForWidth())
        self.cmbSex.setSizePolicy(sizePolicy)
        self.cmbSex.setObjectName(_fromUtf8("cmbSex"))
        self.cmbSex.addItem(_fromUtf8(""))
        self.cmbSex.setItemText(0, _fromUtf8(""))
        self.cmbSex.addItem(_fromUtf8(""))
        self.cmbSex.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbSex, 3, 1, 1, 1)
        self.cmbCounter = CRBComboBox(self.tabMain)
        self.cmbCounter.setEnabled(True)
        self.cmbCounter.setObjectName(_fromUtf8("cmbCounter"))
        self.gridLayout.addWidget(self.cmbCounter, 6, 1, 1, 2)
        self.cmbCounterResetType = QtGui.QComboBox(self.tabMain)
        self.cmbCounterResetType.setEnabled(True)
        self.cmbCounterResetType.setObjectName(_fromUtf8("cmbCounterResetType"))
        self.cmbCounterResetType.addItem(_fromUtf8(""))
        self.cmbCounterResetType.addItem(_fromUtf8(""))
        self.cmbCounterResetType.addItem(_fromUtf8(""))
        self.cmbCounterResetType.addItem(_fromUtf8(""))
        self.cmbCounterResetType.addItem(_fromUtf8(""))
        self.cmbCounterResetType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbCounterResetType, 5, 1, 1, 2)
        self.edtName = QtGui.QLineEdit(self.tabMain)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 2, 1, 1, 1)
        self.lblName = QtGui.QLabel(self.tabMain)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 2, 0, 1, 1)
        self.edtCode = QtGui.QLineEdit(self.tabMain)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout.addWidget(self.edtCode, 0, 1, 1, 1)
        self.lblCode = QtGui.QLabel(self.tabMain)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabMain, _fromUtf8(""))
        self.tabIdentification = QtGui.QWidget()
        self.tabIdentification.setObjectName(_fromUtf8("tabIdentification"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tabIdentification)
        self.gridLayout_3.setMargin(4)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.tblIdentification = CInDocTableView(self.tabIdentification)
        self.tblIdentification.setObjectName(_fromUtf8("tblIdentification"))
        self.gridLayout_3.addWidget(self.tblIdentification, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabIdentification, _fromUtf8(""))
        self.gridLayout_2.addWidget(self.tabWidget, 2, 0, 1, 2)
        self.lblResetCounterType.setBuddy(self.cmbCounterResetType)
        self.lblCounterManualInput.setBuddy(self.chkCounterManualInput)
        self.lblIsRealTimeProcessing.setBuddy(self.chkIsRealTimeProcessing)
        self.lblSex.setBuddy(self.cmbSex)
        self.lblCounter.setBuddy(self.cmbCounter)
        self.lblName.setBuddy(self.edtName)
        self.lblCode.setBuddy(self.edtCode)

        self.retranslateUi(TissueTypeEditorDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TissueTypeEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TissueTypeEditorDialog.reject)
        QtCore.QObject.connect(self.chkCounterManualInput, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbCounter.setDisabled)
        QtCore.QObject.connect(self.chkCounterManualInput, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.lblCounter.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(TissueTypeEditorDialog)
        TissueTypeEditorDialog.setTabOrder(self.tabWidget, self.edtCode)
        TissueTypeEditorDialog.setTabOrder(self.edtCode, self.edtName)
        TissueTypeEditorDialog.setTabOrder(self.edtName, self.cmbSex)
        TissueTypeEditorDialog.setTabOrder(self.cmbSex, self.cmbCounterResetType)
        TissueTypeEditorDialog.setTabOrder(self.cmbCounterResetType, self.chkCounterManualInput)
        TissueTypeEditorDialog.setTabOrder(self.chkCounterManualInput, self.cmbCounter)
        TissueTypeEditorDialog.setTabOrder(self.cmbCounter, self.chkIsRealTimeProcessing)
        TissueTypeEditorDialog.setTabOrder(self.chkIsRealTimeProcessing, self.tblIdentification)
        TissueTypeEditorDialog.setTabOrder(self.tblIdentification, self.buttonBox)

    def retranslateUi(self, TissueTypeEditorDialog):
        TissueTypeEditorDialog.setWindowTitle(_translate("TissueTypeEditorDialog", "Dialog", None))
        self.lblResetCounterType.setText(_translate("TissueTypeEditorDialog", "П&ериод уникальности идентификатора", None))
        self.lblCounterManualInput.setText(_translate("TissueTypeEditorDialog", "&Ручной ввод идентификатора", None))
        self.lblIsRealTimeProcessing.setText(_translate("TissueTypeEditorDialog", "&Обрабатывать в режиме реального времени", None))
        self.lblSex.setText(_translate("TissueTypeEditorDialog", "&Пол", None))
        self.lblCounter.setText(_translate("TissueTypeEditorDialog", "&Счетчик", None))
        self.cmbSex.setItemText(1, _translate("TissueTypeEditorDialog", "М", None))
        self.cmbSex.setItemText(2, _translate("TissueTypeEditorDialog", "Ж", None))
        self.cmbCounterResetType.setItemText(0, _translate("TissueTypeEditorDialog", "День", None))
        self.cmbCounterResetType.setItemText(1, _translate("TissueTypeEditorDialog", "Неделя", None))
        self.cmbCounterResetType.setItemText(2, _translate("TissueTypeEditorDialog", "Месяц", None))
        self.cmbCounterResetType.setItemText(3, _translate("TissueTypeEditorDialog", "Полгода", None))
        self.cmbCounterResetType.setItemText(4, _translate("TissueTypeEditorDialog", "Год", None))
        self.cmbCounterResetType.setItemText(5, _translate("TissueTypeEditorDialog", "Постоянно", None))
        self.lblName.setText(_translate("TissueTypeEditorDialog", "&Наименование", None))
        self.lblCode.setText(_translate("TissueTypeEditorDialog", "&Код", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMain), _translate("TissueTypeEditorDialog", "&Основная информация", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabIdentification), _translate("TissueTypeEditorDialog", "&Идентификация", None))

from library.InDocTable import CInDocTableView
from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TissueTypeEditorDialog = QtGui.QDialog()
    ui = Ui_TissueTypeEditorDialog()
    ui.setupUi(TissueTypeEditorDialog)
    TissueTypeEditorDialog.show()
    sys.exit(app.exec_())
