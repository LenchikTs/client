# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/RefBooks/RBVaccinationCalendarEditor.ui'
#
# Created: Wed Feb 19 22:56:08 2014
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RBVaccinationCalendarEditor(object):
    def setupUi(self, RBVaccinationCalendarEditor):
        RBVaccinationCalendarEditor.setObjectName(_fromUtf8("RBVaccinationCalendarEditor"))
        RBVaccinationCalendarEditor.resize(400, 259)
        self.gridLayout = QtGui.QGridLayout(RBVaccinationCalendarEditor)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblCode = QtGui.QLabel(RBVaccinationCalendarEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.edtCode = QtGui.QLineEdit(RBVaccinationCalendarEditor)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout.addWidget(self.edtCode, 0, 1, 1, 1)
        self.lblName = QtGui.QLabel(RBVaccinationCalendarEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 1, 0, 1, 1)
        self.edtName = QtGui.QLineEdit(RBVaccinationCalendarEditor)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 1, 1, 1, 1)
        self.lblDate = QtGui.QLabel(RBVaccinationCalendarEditor)
        self.lblDate.setObjectName(_fromUtf8("lblDate"))
        self.gridLayout.addWidget(self.lblDate, 2, 0, 1, 1)
        self.edtDate = CDateEdit(RBVaccinationCalendarEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtDate.sizePolicy().hasHeightForWidth())
        self.edtDate.setSizePolicy(sizePolicy)
        self.edtDate.setObjectName(_fromUtf8("edtDate"))
        self.gridLayout.addWidget(self.edtDate, 2, 1, 1, 1)
        self.grpInfection = QtGui.QGroupBox(RBVaccinationCalendarEditor)
        self.grpInfection.setObjectName(_fromUtf8("grpInfection"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.grpInfection)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setMargin(4)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblFilterInfection = QtGui.QLabel(self.grpInfection)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblFilterInfection.sizePolicy().hasHeightForWidth())
        self.lblFilterInfection.setSizePolicy(sizePolicy)
        self.lblFilterInfection.setObjectName(_fromUtf8("lblFilterInfection"))
        self.horizontalLayout.addWidget(self.lblFilterInfection)
        self.cmbFilterInfection = CRBComboBox(self.grpInfection)
        self.cmbFilterInfection.setObjectName(_fromUtf8("cmbFilterInfection"))
        self.horizontalLayout.addWidget(self.cmbFilterInfection)
        self.gridLayout.addWidget(self.grpInfection, 3, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(RBVaccinationCalendarEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 2)
        self.tblVaccinationCalendarInfections = CInDocTableView(RBVaccinationCalendarEditor)
        self.tblVaccinationCalendarInfections.setObjectName(_fromUtf8("tblVaccinationCalendarInfections"))
        self.gridLayout.addWidget(self.tblVaccinationCalendarInfections, 4, 0, 1, 2)
        self.lblCode.setBuddy(self.edtCode)
        self.lblName.setBuddy(self.edtName)

        self.retranslateUi(RBVaccinationCalendarEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBVaccinationCalendarEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBVaccinationCalendarEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(RBVaccinationCalendarEditor)

    def retranslateUi(self, RBVaccinationCalendarEditor):
        RBVaccinationCalendarEditor.setWindowTitle(QtGui.QApplication.translate("RBVaccinationCalendarEditor", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.lblCode.setText(QtGui.QApplication.translate("RBVaccinationCalendarEditor", "&Код", None, QtGui.QApplication.UnicodeUTF8))
        self.lblName.setText(QtGui.QApplication.translate("RBVaccinationCalendarEditor", "&Наименование", None, QtGui.QApplication.UnicodeUTF8))
        self.lblDate.setText(QtGui.QApplication.translate("RBVaccinationCalendarEditor", "Дата", None, QtGui.QApplication.UnicodeUTF8))
        self.grpInfection.setTitle(QtGui.QApplication.translate("RBVaccinationCalendarEditor", "Фильтр", None, QtGui.QApplication.UnicodeUTF8))
        self.lblFilterInfection.setText(QtGui.QApplication.translate("RBVaccinationCalendarEditor", "Инфекция", None, QtGui.QApplication.UnicodeUTF8))

from library.InDocTable import CInDocTableView
from library.crbcombobox import CRBComboBox
from library.DateEdit import CDateEdit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RBVaccinationCalendarEditor = QtGui.QDialog()
    ui = Ui_RBVaccinationCalendarEditor()
    ui.setupUi(RBVaccinationCalendarEditor)
    RBVaccinationCalendarEditor.show()
    sys.exit(app.exec_())

