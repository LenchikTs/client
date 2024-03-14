# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ExportR23NativePage2.ui'
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

class Ui_ExportR23NativePage2(object):
    def setupUi(self, ExportR23NativePage2):
        ExportR23NativePage2.setObjectName(_fromUtf8("ExportR23NativePage2"))
        ExportR23NativePage2.resize(400, 300)
        self.gridlayout = QtGui.QGridLayout(ExportR23NativePage2)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.lblDir = QtGui.QLabel(ExportR23NativePage2)
        self.lblDir.setObjectName(_fromUtf8("lblDir"))
        self.gridlayout.addWidget(self.lblDir, 0, 0, 1, 1)
        self.edtDir = QtGui.QLineEdit(ExportR23NativePage2)
        self.edtDir.setObjectName(_fromUtf8("edtDir"))
        self.gridlayout.addWidget(self.edtDir, 0, 1, 1, 1)
        self.btnSelectDir = QtGui.QToolButton(ExportR23NativePage2)
        self.btnSelectDir.setObjectName(_fromUtf8("btnSelectDir"))
        self.gridlayout.addWidget(self.btnSelectDir, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(128, 241, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 1, 0, 1, 1)

        self.retranslateUi(ExportR23NativePage2)
        QtCore.QMetaObject.connectSlotsByName(ExportR23NativePage2)

    def retranslateUi(self, ExportR23NativePage2):
        ExportR23NativePage2.setWindowTitle(_translate("ExportR23NativePage2", "Form", None))
        self.lblDir.setText(_translate("ExportR23NativePage2", "Сохранить в директории", None))
        self.btnSelectDir.setText(_translate("ExportR23NativePage2", "...", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ExportR23NativePage2 = QtGui.QWidget()
    ui = Ui_ExportR23NativePage2()
    ui.setupUi(ExportR23NativePage2)
    ExportR23NativePage2.show()
    sys.exit(app.exec_())

