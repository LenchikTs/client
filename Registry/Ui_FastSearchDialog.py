# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_merge\Registry\FastSearchDialog.ui'
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

class Ui_fsDialog(object):
    def setupUi(self, fsDialog):
        fsDialog.setObjectName(_fromUtf8("fsDialog"))
        fsDialog.resize(606, 375)
        fsDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtGui.QVBoxLayout(fsDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = QtGui.QWidget(fsDialog)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblQuery = QtGui.QLabel(self.widget)
        self.lblQuery.setMaximumSize(QtCore.QSize(151, 31))
        self.lblQuery.setObjectName(_fromUtf8("lblQuery"))
        self.gridLayout.addWidget(self.lblQuery, 0, 0, 1, 1)
        self.edtQuery = QtGui.QLineEdit(self.widget)
        self.edtQuery.setObjectName(_fromUtf8("edtQuery"))
        self.gridLayout.addWidget(self.edtQuery, 0, 1, 1, 1)
        self.btnQuery = QtGui.QPushButton(self.widget)
        self.btnQuery.setObjectName(_fromUtf8("btnQuery"))
        self.gridLayout.addWidget(self.btnQuery, 0, 2, 1, 1)
        self.lblShabl = QtGui.QLabel(self.widget)
        self.lblShabl.setWordWrap(False)
        self.lblShabl.setIndent(-1)
        self.lblShabl.setObjectName(_fromUtf8("lblShabl"))
        self.gridLayout.addWidget(self.lblShabl, 2, 0, 1, 2)
        self.chkWithMask = QtGui.QCheckBox(self.widget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Times"))
        font.setPointSize(11)
        self.chkWithMask.setFont(font)
        self.chkWithMask.setObjectName(_fromUtf8("chkWithMask"))
        self.gridLayout.addWidget(self.chkWithMask, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.widget)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(fsDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.lblQuery.setBuddy(self.edtQuery)

        self.retranslateUi(fsDialog)
        QtCore.QMetaObject.connectSlotsByName(fsDialog)
        fsDialog.setTabOrder(self.edtQuery, self.btnQuery)
        fsDialog.setTabOrder(self.btnQuery, self.buttonBox)

    def retranslateUi(self, fsDialog):
        fsDialog.setWindowTitle(_translate("fsDialog", "Быстрый поиск пациента", None))
        self.lblQuery.setText(_translate("fsDialog", "<html>\n"
"<head/>\n"
"<body style=\'font-family:Times; font-size:10pt; font-style:normal\'>\n"
"Шаблон быстрого поиска\n"
"</body>\n"
"</html>", None))
        self.btnQuery.setText(_translate("fsDialog", "Искать", None))
        self.lblShabl.setText(_translate("fsDialog", "<html>\n"
"<head/>\n"
"<body style=\'font-family:Times; font-size:11pt; font-style:normal\'>\n"
"Допустимые шаблоны поиска:<br/>\n"
"ФИОДДММГГГГ (РЕЕ09021995)<br/>\n"
"ФИОДДММГГ (РЕЕ090295)<br/>\n"
"ФИДДММГГГГ (РЕ09021995)<br/>\n"
"ФИДДММГГ (РЕ090295)<br/>\n"
"Ф* И* (Руд Его)<br/>\n"
"Ф* И* О* (Руден Ег Евген)<br/>\n"
"Ф* И* О* ДДММГГГГ (Руденк Егор Евг 09021995)<br/>\n"
"Ф* И* О* ДДММГГ (Руд Ег Евг 090295)<br/>\n"
"Ф* И* ДДММГГГГ (Руд Егор 09021995)<br/>\n"
"Ф* И* ДДММГГ (Руд Его 090295)<br/>\n"
"Ф* ДДММГГГГ (Руден 09021995)<br/>\n"
"Ф* ДДММГГ (Руден 090295)<br/>\n"
"</body>\n"
"</html>", None))
        self.chkWithMask.setText(_translate("fsDialog", "По маске", None))

