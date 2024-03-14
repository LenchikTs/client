# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/dark/work/s11/Reports/RegistryStructure/SetupDialog.ui'
#
# Created by: PyQt4 UI code generator 4.12.3
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

class Ui_SetupDialog(object):
    def setupUi(self, SetupDialog):
        SetupDialog.setObjectName(_fromUtf8("SetupDialog"))
        SetupDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        SetupDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtGui.QVBoxLayout(SetupDialog)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widgetLayout = QtGui.QVBoxLayout()
        self.widgetLayout.setContentsMargins(10, -1, 10, -1)
        self.widgetLayout.setObjectName(_fromUtf8("widgetLayout"))
        self.verticalLayout.addLayout(self.widgetLayout)
        spacerItem = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(SetupDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SetupDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SetupDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SetupDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SetupDialog)

    def retranslateUi(self, SetupDialog):
        SetupDialog.setWindowTitle(_translate("SetupDialog", "параметры отчёта", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SetupDialog = QtGui.QDialog()
    ui = Ui_SetupDialog()
    ui.setupUi(SetupDialog)
    SetupDialog.show()
    sys.exit(app.exec_())

