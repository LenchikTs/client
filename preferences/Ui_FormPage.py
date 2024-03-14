# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/preferences/FormPage.ui'
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

class Ui_FormPage(object):
    def setupUi(self, FormPage):
        FormPage.setObjectName(_fromUtf8("FormPage"))
        FormPage.resize(543, 274)
        self.gridLayout = QtGui.QGridLayout(FormPage)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.grpTabWidgets = QtGui.QGroupBox(FormPage)
        self.grpTabWidgets.setAlignment(QtCore.Qt.AlignCenter)
        self.grpTabWidgets.setObjectName(_fromUtf8("grpTabWidgets"))
        self.gridLayout_3 = QtGui.QGridLayout(self.grpTabWidgets)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.chkTempInvalid = QtGui.QCheckBox(self.grpTabWidgets)
        self.chkTempInvalid.setChecked(True)
        self.chkTempInvalid.setObjectName(_fromUtf8("chkTempInvalid"))
        self.gridLayout_3.addWidget(self.chkTempInvalid, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.grpTabWidgets, 12, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 13, 0, 1, 1)

        self.retranslateUi(FormPage)
        QtCore.QMetaObject.connectSlotsByName(FormPage)

    def retranslateUi(self, FormPage):
        FormPage.setWindowTitle(_translate("FormPage", "Формы ввода", None))
        self.grpTabWidgets.setTitle(_translate("FormPage", "Визуализация: Вкладки", None))
        self.chkTempInvalid.setText(_translate("FormPage", "Вкладка Трудоспособность", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    FormPage = QtGui.QWidget()
    ui = Ui_FormPage()
    ui.setupUi(FormPage)
    FormPage.show()
    sys.exit(app.exec_())

