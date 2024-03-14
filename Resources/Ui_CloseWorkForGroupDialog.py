# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/Resources/CloseWorkForGroupDialog.ui'
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

class Ui_CloseWorkForGroupDialog(object):
    def setupUi(self, CloseWorkForGroupDialog):
        CloseWorkForGroupDialog.setObjectName(_fromUtf8("CloseWorkForGroupDialog"))
        CloseWorkForGroupDialog.resize(458, 300)
        self.gridLayout = QtGui.QGridLayout(CloseWorkForGroupDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblActionType = CTableView(CloseWorkForGroupDialog)
        self.tblActionType.setObjectName(_fromUtf8("tblActionType"))
        self.gridLayout.addWidget(self.tblActionType, 4, 0, 1, 4)
        self.buttonBox = QtGui.QDialogButtonBox(CloseWorkForGroupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 3, 1, 1)
        self.edtExecDate = CDateEdit(CloseWorkForGroupDialog)
        self.edtExecDate.setCalendarPopup(True)
        self.edtExecDate.setObjectName(_fromUtf8("edtExecDate"))
        self.gridLayout.addWidget(self.edtExecDate, 3, 1, 1, 1)
        self.cmbStatus = CJobTicketStatusComboBox(CloseWorkForGroupDialog)
        self.cmbStatus.setObjectName(_fromUtf8("cmbStatus"))
        self.gridLayout.addWidget(self.cmbStatus, 0, 1, 1, 3)
        self.lblStatus = QtGui.QLabel(CloseWorkForGroupDialog)
        self.lblStatus.setObjectName(_fromUtf8("lblStatus"))
        self.gridLayout.addWidget(self.lblStatus, 0, 0, 1, 1)
        self.lblPerson = QtGui.QLabel(CloseWorkForGroupDialog)
        self.lblPerson.setObjectName(_fromUtf8("lblPerson"))
        self.gridLayout.addWidget(self.lblPerson, 2, 0, 1, 1)
        self.lblExecDateTime = QtGui.QLabel(CloseWorkForGroupDialog)
        self.lblExecDateTime.setObjectName(_fromUtf8("lblExecDateTime"))
        self.gridLayout.addWidget(self.lblExecDateTime, 3, 0, 1, 1)
        self.edtExecTime = QtGui.QTimeEdit(CloseWorkForGroupDialog)
        self.edtExecTime.setObjectName(_fromUtf8("edtExecTime"))
        self.gridLayout.addWidget(self.edtExecTime, 3, 2, 1, 1)
        self.cmbPerson = CPersonComboBoxEx(CloseWorkForGroupDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 2, 1, 1, 3)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 3, 1, 1)
        self.lblOrgStructure = QtGui.QLabel(CloseWorkForGroupDialog)
        self.lblOrgStructure.setObjectName(_fromUtf8("lblOrgStructure"))
        self.gridLayout.addWidget(self.lblOrgStructure, 1, 0, 1, 1)
        self.cmbOrgStructure = COrgStructureComboBox(CloseWorkForGroupDialog)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 1, 1, 1, 3)

        self.retranslateUi(CloseWorkForGroupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), CloseWorkForGroupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), CloseWorkForGroupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CloseWorkForGroupDialog)
        CloseWorkForGroupDialog.setTabOrder(self.cmbStatus, self.cmbOrgStructure)
        CloseWorkForGroupDialog.setTabOrder(self.cmbOrgStructure, self.cmbPerson)
        CloseWorkForGroupDialog.setTabOrder(self.cmbPerson, self.edtExecDate)
        CloseWorkForGroupDialog.setTabOrder(self.edtExecDate, self.edtExecTime)
        CloseWorkForGroupDialog.setTabOrder(self.edtExecTime, self.tblActionType)
        CloseWorkForGroupDialog.setTabOrder(self.tblActionType, self.buttonBox)

    def retranslateUi(self, CloseWorkForGroupDialog):
        CloseWorkForGroupDialog.setWindowTitle(_translate("CloseWorkForGroupDialog", "Закрыть работу для группы", None))
        self.edtExecDate.setDisplayFormat(_translate("CloseWorkForGroupDialog", "dd.MM.yyyy", None))
        self.lblStatus.setText(_translate("CloseWorkForGroupDialog", "Состояние", None))
        self.lblPerson.setText(_translate("CloseWorkForGroupDialog", "Ответственный", None))
        self.lblExecDateTime.setText(_translate("CloseWorkForGroupDialog", "Дата и время", None))
        self.lblOrgStructure.setText(_translate("CloseWorkForGroupDialog", "Подразделение", None))

from Orgs.OrgStructComboBoxes import COrgStructureComboBox
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from Resources.JobTicketStatus import CJobTicketStatusComboBox
from library.DateEdit import CDateEdit
from library.TableView import CTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    CloseWorkForGroupDialog = QtGui.QDialog()
    ui = Ui_CloseWorkForGroupDialog()
    ui.setupUi(CloseWorkForGroupDialog)
    CloseWorkForGroupDialog.show()
    sys.exit(app.exec_())

