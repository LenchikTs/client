# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/lampa/Docs/svn/trunk/TissueJournal/TissueJournalTotalEditor.ui'
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

class Ui_TissueJournalTotalEditorDialog(object):
    def setupUi(self, TissueJournalTotalEditorDialog):
        TissueJournalTotalEditorDialog.setObjectName(_fromUtf8("TissueJournalTotalEditorDialog"))
        TissueJournalTotalEditorDialog.resize(498, 287)
        TissueJournalTotalEditorDialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(TissueJournalTotalEditorDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbMorphologyMKB = CICDMorphologyCodeEditEx(TissueJournalTotalEditorDialog)
        self.cmbMorphologyMKB.setEnabled(False)
        self.cmbMorphologyMKB.setObjectName(_fromUtf8("cmbMorphologyMKB"))
        self.gridLayout.addWidget(self.cmbMorphologyMKB, 9, 1, 1, 1)
        self.chkMorphologyMKB = QtGui.QCheckBox(TissueJournalTotalEditorDialog)
        self.chkMorphologyMKB.setObjectName(_fromUtf8("chkMorphologyMKB"))
        self.gridLayout.addWidget(self.chkMorphologyMKB, 9, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(TissueJournalTotalEditorDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 11, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 0, 1, 1)
        self.cmbStatus = CActionStatusComboBox(TissueJournalTotalEditorDialog)
        self.cmbStatus.setEnabled(False)
        self.cmbStatus.setObjectName(_fromUtf8("cmbStatus"))
        self.gridLayout.addWidget(self.cmbStatus, 0, 1, 1, 2)
        self.cmbMKB = CICDCodeEditEx(TissueJournalTotalEditorDialog)
        self.cmbMKB.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbMKB.sizePolicy().hasHeightForWidth())
        self.cmbMKB.setSizePolicy(sizePolicy)
        self.cmbMKB.setObjectName(_fromUtf8("cmbMKB"))
        self.gridLayout.addWidget(self.cmbMKB, 8, 1, 1, 1)
        self.lblMorphologyMKBText = QtGui.QLabel(TissueJournalTotalEditorDialog)
        self.lblMorphologyMKBText.setText(_fromUtf8(""))
        self.lblMorphologyMKBText.setObjectName(_fromUtf8("lblMorphologyMKBText"))
        self.gridLayout.addWidget(self.lblMorphologyMKBText, 9, 2, 1, 1)
        self.chkPersonInAction = QtGui.QCheckBox(TissueJournalTotalEditorDialog)
        self.chkPersonInAction.setObjectName(_fromUtf8("chkPersonInAction"))
        self.gridLayout.addWidget(self.chkPersonInAction, 2, 0, 1, 1)
        self.chkPersonInJournal = QtGui.QCheckBox(TissueJournalTotalEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkPersonInJournal.sizePolicy().hasHeightForWidth())
        self.chkPersonInJournal.setSizePolicy(sizePolicy)
        self.chkPersonInJournal.setObjectName(_fromUtf8("chkPersonInJournal"))
        self.gridLayout.addWidget(self.chkPersonInJournal, 1, 0, 1, 1)
        self.cmbPersonInAction = CPersonComboBoxEx(TissueJournalTotalEditorDialog)
        self.cmbPersonInAction.setEnabled(False)
        self.cmbPersonInAction.setObjectName(_fromUtf8("cmbPersonInAction"))
        self.gridLayout.addWidget(self.cmbPersonInAction, 2, 1, 1, 2)
        self.cmbPersonInJournal = CPersonComboBoxEx(TissueJournalTotalEditorDialog)
        self.cmbPersonInJournal.setEnabled(False)
        self.cmbPersonInJournal.setObjectName(_fromUtf8("cmbPersonInJournal"))
        self.gridLayout.addWidget(self.cmbPersonInJournal, 1, 1, 1, 2)
        self.cmbAssistantInAction = CPersonComboBoxEx(TissueJournalTotalEditorDialog)
        self.cmbAssistantInAction.setEnabled(False)
        self.cmbAssistantInAction.setObjectName(_fromUtf8("cmbAssistantInAction"))
        self.gridLayout.addWidget(self.cmbAssistantInAction, 3, 1, 1, 2)
        self.chkStatus = QtGui.QCheckBox(TissueJournalTotalEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkStatus.sizePolicy().hasHeightForWidth())
        self.chkStatus.setSizePolicy(sizePolicy)
        self.chkStatus.setObjectName(_fromUtf8("chkStatus"))
        self.gridLayout.addWidget(self.chkStatus, 0, 0, 1, 1)
        self.chkMKB = QtGui.QCheckBox(TissueJournalTotalEditorDialog)
        self.chkMKB.setObjectName(_fromUtf8("chkMKB"))
        self.gridLayout.addWidget(self.chkMKB, 8, 0, 1, 1)
        self.lblMKBText = QtGui.QLabel(TissueJournalTotalEditorDialog)
        self.lblMKBText.setText(_fromUtf8(""))
        self.lblMKBText.setObjectName(_fromUtf8("lblMKBText"))
        self.gridLayout.addWidget(self.lblMKBText, 8, 2, 1, 1)
        self.chkAssistantInAction = QtGui.QCheckBox(TissueJournalTotalEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkAssistantInAction.sizePolicy().hasHeightForWidth())
        self.chkAssistantInAction.setSizePolicy(sizePolicy)
        self.chkAssistantInAction.setObjectName(_fromUtf8("chkAssistantInAction"))
        self.gridLayout.addWidget(self.chkAssistantInAction, 3, 0, 1, 1)
        self.chkAmount = QtGui.QCheckBox(TissueJournalTotalEditorDialog)
        self.chkAmount.setObjectName(_fromUtf8("chkAmount"))
        self.gridLayout.addWidget(self.chkAmount, 4, 0, 1, 1)
        self.edtAmount = QtGui.QDoubleSpinBox(TissueJournalTotalEditorDialog)
        self.edtAmount.setEnabled(False)
        self.edtAmount.setObjectName(_fromUtf8("edtAmount"))
        self.gridLayout.addWidget(self.edtAmount, 4, 1, 1, 1)
        self.chkActionSpecification = QtGui.QCheckBox(TissueJournalTotalEditorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkActionSpecification.sizePolicy().hasHeightForWidth())
        self.chkActionSpecification.setSizePolicy(sizePolicy)
        self.chkActionSpecification.setObjectName(_fromUtf8("chkActionSpecification"))
        self.gridLayout.addWidget(self.chkActionSpecification, 6, 0, 1, 1)
        self.cmbActionSpecification = CRBComboBox(TissueJournalTotalEditorDialog)
        self.cmbActionSpecification.setEnabled(False)
        self.cmbActionSpecification.setObjectName(_fromUtf8("cmbActionSpecification"))
        self.gridLayout.addWidget(self.cmbActionSpecification, 6, 1, 1, 2)

        self.retranslateUi(TissueJournalTotalEditorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TissueJournalTotalEditorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TissueJournalTotalEditorDialog.reject)
        QtCore.QObject.connect(self.chkStatus, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbStatus.setEnabled)
        QtCore.QObject.connect(self.chkPersonInJournal, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbPersonInJournal.setEnabled)
        QtCore.QObject.connect(self.chkPersonInAction, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbPersonInAction.setEnabled)
        QtCore.QObject.connect(self.chkAssistantInAction, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbAssistantInAction.setEnabled)
        QtCore.QObject.connect(self.chkMKB, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbMKB.setEnabled)
        QtCore.QObject.connect(self.chkMorphologyMKB, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbMorphologyMKB.setEnabled)
        QtCore.QObject.connect(self.chkAmount, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtAmount.setEnabled)
        QtCore.QObject.connect(self.chkActionSpecification, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.cmbActionSpecification.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(TissueJournalTotalEditorDialog)
        TissueJournalTotalEditorDialog.setTabOrder(self.chkStatus, self.cmbStatus)
        TissueJournalTotalEditorDialog.setTabOrder(self.cmbStatus, self.chkPersonInJournal)
        TissueJournalTotalEditorDialog.setTabOrder(self.chkPersonInJournal, self.cmbPersonInJournal)
        TissueJournalTotalEditorDialog.setTabOrder(self.cmbPersonInJournal, self.chkPersonInAction)
        TissueJournalTotalEditorDialog.setTabOrder(self.chkPersonInAction, self.cmbPersonInAction)
        TissueJournalTotalEditorDialog.setTabOrder(self.cmbPersonInAction, self.chkAssistantInAction)
        TissueJournalTotalEditorDialog.setTabOrder(self.chkAssistantInAction, self.cmbAssistantInAction)
        TissueJournalTotalEditorDialog.setTabOrder(self.cmbAssistantInAction, self.chkAmount)
        TissueJournalTotalEditorDialog.setTabOrder(self.chkAmount, self.edtAmount)
        TissueJournalTotalEditorDialog.setTabOrder(self.edtAmount, self.chkMKB)
        TissueJournalTotalEditorDialog.setTabOrder(self.chkMKB, self.cmbMKB)
        TissueJournalTotalEditorDialog.setTabOrder(self.cmbMKB, self.chkMorphologyMKB)
        TissueJournalTotalEditorDialog.setTabOrder(self.chkMorphologyMKB, self.cmbMorphologyMKB)
        TissueJournalTotalEditorDialog.setTabOrder(self.cmbMorphologyMKB, self.buttonBox)

    def retranslateUi(self, TissueJournalTotalEditorDialog):
        TissueJournalTotalEditorDialog.setWindowTitle(_translate("TissueJournalTotalEditorDialog", "Изменить атрибуты выбранных Действий", None))
        self.chkMorphologyMKB.setText(_translate("TissueJournalTotalEditorDialog", "Морфология МКБ", None))
        self.chkPersonInAction.setText(_translate("TissueJournalTotalEditorDialog", "Ответственный в действии", None))
        self.chkPersonInJournal.setText(_translate("TissueJournalTotalEditorDialog", "Ответственный в журнале", None))
        self.chkStatus.setText(_translate("TissueJournalTotalEditorDialog", "Статус", None))
        self.chkMKB.setText(_translate("TissueJournalTotalEditorDialog", "МКБ", None))
        self.chkAssistantInAction.setText(_translate("TissueJournalTotalEditorDialog", "Ассистент в действии", None))
        self.chkAmount.setText(_translate("TissueJournalTotalEditorDialog", "Количество", None))
        self.chkActionSpecification.setText(_translate("TissueJournalTotalEditorDialog", "Особенности выполенения", None))

from Events.ActionStatus import CActionStatusComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.ICDCodeEdit import CICDCodeEditEx
from library.ICDMorphologyCodeEdit import CICDMorphologyCodeEditEx
from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TissueJournalTotalEditorDialog = QtGui.QDialog()
    ui = Ui_TissueJournalTotalEditorDialog()
    ui.setupUi(TissueJournalTotalEditorDialog)
    TissueJournalTotalEditorDialog.show()
    sys.exit(app.exec_())

