# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/preferences/CalendarExceptionListDialog.ui'
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

class Ui_CalendarExceptionListDialog(object):
    def setupUi(self, CalendarExceptionListDialog):
        CalendarExceptionListDialog.setObjectName(_fromUtf8("CalendarExceptionListDialog"))
        CalendarExceptionListDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        CalendarExceptionListDialog.resize(588, 328)
        CalendarExceptionListDialog.setSizeGripEnabled(True)
        CalendarExceptionListDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(CalendarExceptionListDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtYear = QtGui.QSpinBox(CalendarExceptionListDialog)
        self.edtYear.setEnabled(False)
        self.edtYear.setMinimum(1)
        self.edtYear.setMaximum(9999)
        self.edtYear.setObjectName(_fromUtf8("edtYear"))
        self.gridLayout.addWidget(self.edtYear, 1, 3, 1, 1)
        spacerItem = QtGui.QSpacerItem(308, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 4, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(CalendarExceptionListDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 5, 1, 1)
        self.chkYearFilter = QtGui.QCheckBox(CalendarExceptionListDialog)
        self.chkYearFilter.setObjectName(_fromUtf8("chkYearFilter"))
        self.gridLayout.addWidget(self.chkYearFilter, 1, 2, 1, 1)
        self.label = QtGui.QLabel(CalendarExceptionListDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.tblItems = CTableView(CalendarExceptionListDialog)
        self.tblItems.setTabKeyNavigation(False)
        self.tblItems.setAlternatingRowColors(True)
        self.tblItems.setObjectName(_fromUtf8("tblItems"))
        self.gridLayout.addWidget(self.tblItems, 0, 0, 1, 6)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 1, 1, 1)

        self.retranslateUi(CalendarExceptionListDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), CalendarExceptionListDialog.close)
        QtCore.QObject.connect(self.chkYearFilter, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.edtYear.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(CalendarExceptionListDialog)
        CalendarExceptionListDialog.setTabOrder(self.tblItems, self.chkYearFilter)
        CalendarExceptionListDialog.setTabOrder(self.chkYearFilter, self.edtYear)
        CalendarExceptionListDialog.setTabOrder(self.edtYear, self.buttonBox)

    def retranslateUi(self, CalendarExceptionListDialog):
        CalendarExceptionListDialog.setWindowTitle(_translate("CalendarExceptionListDialog", "Список записей", None))
        self.chkYearFilter.setText(_translate("CalendarExceptionListDialog", "Только год", None))
        self.label.setText(_translate("CalendarExceptionListDialog", "TextLabel", None))
        self.tblItems.setWhatsThis(_translate("CalendarExceptionListDialog", "список записей", "ура!"))

from library.TableView import CTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    CalendarExceptionListDialog = QtGui.QDialog()
    ui = Ui_CalendarExceptionListDialog()
    ui.setupUi(CalendarExceptionListDialog)
    CalendarExceptionListDialog.show()
    sys.exit(app.exec_())

