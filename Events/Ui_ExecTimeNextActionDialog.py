# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Rabota\s11\Events\ExecTimeNextActionDialog.ui'
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

class Ui_ExecTimeNextActionDialog(object):
    def setupUi(self, ExecTimeNextActionDialog):
        ExecTimeNextActionDialog.setObjectName(_fromUtf8("ExecTimeNextActionDialog"))
        ExecTimeNextActionDialog.resize(380, 125)
        self.gridLayout = QtGui.QGridLayout(ExecTimeNextActionDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(ExecTimeNextActionDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.btnExecTimeOld = QtGui.QPushButton(ExecTimeNextActionDialog)
        self.btnExecTimeOld.setText(_fromUtf8(""))
        self.btnExecTimeOld.setObjectName(_fromUtf8("btnExecTimeOld"))
        self.gridLayout.addWidget(self.btnExecTimeOld, 4, 0, 1, 2)
        self.lblExecTimeNew = QtGui.QLabel(ExecTimeNextActionDialog)
        self.lblExecTimeNew.setObjectName(_fromUtf8("lblExecTimeNew"))
        self.gridLayout.addWidget(self.lblExecTimeNew, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ExecTimeNextActionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 4, 2, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 2, 1, 1)
        self.edtExecTimeNew = QtGui.QTimeEdit(ExecTimeNextActionDialog)
        self.edtExecTimeNew.setObjectName(_fromUtf8("edtExecTimeNew"))
        self.gridLayout.addWidget(self.edtExecTimeNew, 0, 1, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(129, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 3, 1, 1)
        self.cmbPerson = CPersonComboBoxEx(ExecTimeNextActionDialog)
        self.cmbPerson.setObjectName(_fromUtf8("cmbPerson"))
        self.gridLayout.addWidget(self.cmbPerson, 2, 1, 1, 3)
        self.lblCourse = QtGui.QLabel(ExecTimeNextActionDialog)
        self.lblCourse.setObjectName(_fromUtf8("lblCourse"))
        self.gridLayout.addWidget(self.lblCourse, 1, 0, 1, 1)
        self.cmbCourse = CCourseStatusComboBox(ExecTimeNextActionDialog)
        self.cmbCourse.setObjectName(_fromUtf8("cmbCourse"))
        self.gridLayout.addWidget(self.cmbCourse, 1, 1, 1, 3)

        self.retranslateUi(ExecTimeNextActionDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ExecTimeNextActionDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ExecTimeNextActionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ExecTimeNextActionDialog)
        ExecTimeNextActionDialog.setTabOrder(self.edtExecTimeNew, self.cmbCourse)
        ExecTimeNextActionDialog.setTabOrder(self.cmbCourse, self.btnExecTimeOld)
        ExecTimeNextActionDialog.setTabOrder(self.btnExecTimeOld, self.buttonBox)
        ExecTimeNextActionDialog.setTabOrder(self.buttonBox, self.cmbPerson)

    def retranslateUi(self, ExecTimeNextActionDialog):
        ExecTimeNextActionDialog.setWindowTitle(_translate("ExecTimeNextActionDialog", "Время выполнения", None))
        self.label.setText(_translate("ExecTimeNextActionDialog", "Исполнитель", None))
        self.lblExecTimeNew.setText(_translate("ExecTimeNextActionDialog", "Время выполнения", None))
        self.lblCourse.setText(_translate("ExecTimeNextActionDialog", "Курс", None))

from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from Resources.CourseStatus import CCourseStatusComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ExecTimeNextActionDialog = QtGui.QDialog()
    ui = Ui_ExecTimeNextActionDialog()
    ui.setupUi(ExecTimeNextActionDialog)
    ExecTimeNextActionDialog.show()
    sys.exit(app.exec_())

