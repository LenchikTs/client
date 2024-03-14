# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/Resources/JobTypeActionsSelector.ui'
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

class Ui_JobTypeActionsSelectorDialog(object):
    def setupUi(self, JobTypeActionsSelectorDialog):
        JobTypeActionsSelectorDialog.setObjectName(_fromUtf8("JobTypeActionsSelectorDialog"))
        JobTypeActionsSelectorDialog.resize(879, 364)
        self.gridLayout = QtGui.QGridLayout(JobTypeActionsSelectorDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblActionTypes = CInDocTableView(JobTypeActionsSelectorDialog)
        self.tblActionTypes.setObjectName(_fromUtf8("tblActionTypes"))
        self.gridLayout.addWidget(self.tblActionTypes, 0, 0, 1, 4)
        self.lblFindByCode = QtGui.QLabel(JobTypeActionsSelectorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblFindByCode.sizePolicy().hasHeightForWidth())
        self.lblFindByCode.setSizePolicy(sizePolicy)
        self.lblFindByCode.setObjectName(_fromUtf8("lblFindByCode"))
        self.gridLayout.addWidget(self.lblFindByCode, 1, 0, 1, 1)
        self.edtFindByCode = QtGui.QLineEdit(JobTypeActionsSelectorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtFindByCode.sizePolicy().hasHeightForWidth())
        self.edtFindByCode.setSizePolicy(sizePolicy)
        self.edtFindByCode.setObjectName(_fromUtf8("edtFindByCode"))
        self.gridLayout.addWidget(self.edtFindByCode, 1, 1, 1, 1)
        self.chkFindFilter = QtGui.QCheckBox(JobTypeActionsSelectorDialog)
        self.chkFindFilter.setObjectName(_fromUtf8("chkFindFilter"))
        self.gridLayout.addWidget(self.chkFindFilter, 1, 2, 1, 1)
        self.edtFindFilter = QtGui.QLineEdit(JobTypeActionsSelectorDialog)
        self.edtFindFilter.setEnabled(False)
        self.edtFindFilter.setObjectName(_fromUtf8("edtFindFilter"))
        self.gridLayout.addWidget(self.edtFindFilter, 1, 3, 1, 1)
        self.chkOnlyNotExists = QtGui.QCheckBox(JobTypeActionsSelectorDialog)
        self.chkOnlyNotExists.setChecked(True)
        self.chkOnlyNotExists.setObjectName(_fromUtf8("chkOnlyNotExists"))
        self.gridLayout.addWidget(self.chkOnlyNotExists, 2, 0, 1, 1)
        self.buttonBox = CApplyResetDialogButtonBox(JobTypeActionsSelectorDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 3)

        self.retranslateUi(JobTypeActionsSelectorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), JobTypeActionsSelectorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), JobTypeActionsSelectorDialog.reject)
        QtCore.QObject.connect(self.chkFindFilter, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtFindFilter.setEnabled)
        QtCore.QObject.connect(self.chkFindFilter, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtFindByCode.setDisabled)
        QtCore.QObject.connect(self.chkFindFilter, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtFindFilter.setEnabled)
        QtCore.QObject.connect(self.chkFindFilter, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtFindByCode.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(JobTypeActionsSelectorDialog)
        JobTypeActionsSelectorDialog.setTabOrder(self.tblActionTypes, self.edtFindByCode)
        JobTypeActionsSelectorDialog.setTabOrder(self.edtFindByCode, self.chkFindFilter)
        JobTypeActionsSelectorDialog.setTabOrder(self.chkFindFilter, self.edtFindFilter)

    def retranslateUi(self, JobTypeActionsSelectorDialog):
        JobTypeActionsSelectorDialog.setWindowTitle(_translate("JobTypeActionsSelectorDialog", "Dialog", None))
        self.lblFindByCode.setText(_translate("JobTypeActionsSelectorDialog", " Поиск по коду или наименованию", None))
        self.chkFindFilter.setText(_translate("JobTypeActionsSelectorDialog", "Фильтр", None))
        self.chkOnlyNotExists.setText(_translate("JobTypeActionsSelectorDialog", "Отсутствующие", None))

from library.DialogButtonBox import CApplyResetDialogButtonBox
from library.InDocTable import CInDocTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    JobTypeActionsSelectorDialog = QtGui.QDialog()
    ui = Ui_JobTypeActionsSelectorDialog()
    ui.setupUi(JobTypeActionsSelectorDialog)
    JobTypeActionsSelectorDialog.show()
    sys.exit(app.exec_())

