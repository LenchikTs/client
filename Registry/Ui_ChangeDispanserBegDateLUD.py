# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/Registry/ChangeDispanserBegDateLUD.ui'
#
# Created: Tue Jan 15 16:42:38 2019
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_ChangeDispanserBegDateLUD(object):
    def setupUi(self, ChangeDispanserBegDateLUD):
        ChangeDispanserBegDateLUD.setObjectName(_fromUtf8("ChangeDispanserBegDateLUD"))
        ChangeDispanserBegDateLUD.resize(352, 71)
        self.gridLayout = QtGui.QGridLayout(ChangeDispanserBegDateLUD)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblBegDate = QtGui.QLabel(ChangeDispanserBegDateLUD)
        self.lblBegDate.setObjectName(_fromUtf8("lblBegDate"))
        self.gridLayout.addWidget(self.lblBegDate, 0, 0, 1, 1)
        self.edtBegDate = CDateEdit(ChangeDispanserBegDateLUD)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtBegDate.sizePolicy().hasHeightForWidth())
        self.edtBegDate.setSizePolicy(sizePolicy)
        self.edtBegDate.setCalendarPopup(True)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.gridLayout.addWidget(self.edtBegDate, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ChangeDispanserBegDateLUD)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 3)

        self.retranslateUi(ChangeDispanserBegDateLUD)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ChangeDispanserBegDateLUD.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ChangeDispanserBegDateLUD.reject)
        QtCore.QMetaObject.connectSlotsByName(ChangeDispanserBegDateLUD)

    def retranslateUi(self, ChangeDispanserBegDateLUD):
        ChangeDispanserBegDateLUD.setWindowTitle(_translate("ChangeDispanserBegDateLUD", "Изменение пероида заболевания", None))
        self.lblBegDate.setText(_translate("ChangeDispanserBegDateLUD", "Дата постановки на диспансерный учет", None))
        self.edtBegDate.setDisplayFormat(_translate("ChangeDispanserBegDateLUD", "dd.MM.yyyy", None))

from library.DateEdit import CDateEdit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ChangeDispanserBegDateLUD = QtGui.QDialog()
    ui = Ui_ChangeDispanserBegDateLUD()
    ui.setupUi(ChangeDispanserBegDateLUD)
    ChangeDispanserBegDateLUD.show()
    sys.exit(app.exec_())

