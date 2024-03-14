# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ReportPage.ui'
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

class Ui_reportPage(object):
    def setupUi(self, reportPage):
        reportPage.setObjectName(_fromUtf8("reportPage"))
        reportPage.resize(651, 592)
        self.gridLayout = QtGui.QGridLayout(reportPage)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(20, 1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.lblExaroPath = QtGui.QLabel(reportPage)
        self.lblExaroPath.setObjectName(_fromUtf8("lblExaroPath"))
        self.gridLayout.addWidget(self.lblExaroPath, 2, 0, 1, 1)
        self.edtExaroEditor = QtGui.QLineEdit(reportPage)
        self.edtExaroEditor.setObjectName(_fromUtf8("edtExaroEditor"))
        self.gridLayout.addWidget(self.edtExaroEditor, 2, 1, 1, 2)
        self.btnSelectDocumentEditor = QtGui.QToolButton(reportPage)
        self.btnSelectDocumentEditor.setObjectName(_fromUtf8("btnSelectDocumentEditor"))
        self.gridLayout.addWidget(self.btnSelectDocumentEditor, 0, 3, 1, 1)
        self.edtExtGenRep = QtGui.QLineEdit(reportPage)
        self.edtExtGenRep.setObjectName(_fromUtf8("edtExtGenRep"))
        self.gridLayout.addWidget(self.edtExtGenRep, 1, 1, 1, 2)
        self.btnSelectExaroEditor = QtGui.QToolButton(reportPage)
        self.btnSelectExaroEditor.setObjectName(_fromUtf8("btnSelectExaroEditor"))
        self.gridLayout.addWidget(self.btnSelectExaroEditor, 2, 3, 1, 1)
        self.lblDocumentEditor = QtGui.QLabel(reportPage)
        self.lblDocumentEditor.setObjectName(_fromUtf8("lblDocumentEditor"))
        self.gridLayout.addWidget(self.lblDocumentEditor, 0, 0, 1, 1)
        self.edtDocumentEditor = QtGui.QLineEdit(reportPage)
        self.edtDocumentEditor.setObjectName(_fromUtf8("edtDocumentEditor"))
        self.gridLayout.addWidget(self.edtDocumentEditor, 0, 1, 1, 2)
        self.btnSelectExtGenRep = QtGui.QToolButton(reportPage)
        self.btnSelectExtGenRep.setObjectName(_fromUtf8("btnSelectExtGenRep"))
        self.gridLayout.addWidget(self.btnSelectExtGenRep, 1, 3, 1, 1)
        self.lblExtGenRep = QtGui.QLabel(reportPage)
        self.lblExtGenRep.setObjectName(_fromUtf8("lblExtGenRep"))
        self.gridLayout.addWidget(self.lblExtGenRep, 1, 0, 1, 1)
        self.lblExaroPath.setBuddy(self.edtExaroEditor)
        self.lblDocumentEditor.setBuddy(self.edtDocumentEditor)
        self.lblExtGenRep.setBuddy(self.edtExtGenRep)

        self.retranslateUi(reportPage)
        QtCore.QMetaObject.connectSlotsByName(reportPage)
        reportPage.setTabOrder(self.edtDocumentEditor, self.btnSelectDocumentEditor)
        reportPage.setTabOrder(self.btnSelectDocumentEditor, self.edtExtGenRep)
        reportPage.setTabOrder(self.edtExtGenRep, self.btnSelectExtGenRep)
        reportPage.setTabOrder(self.btnSelectExtGenRep, self.edtExaroEditor)
        reportPage.setTabOrder(self.edtExaroEditor, self.btnSelectExaroEditor)

    def retranslateUi(self, reportPage):
        reportPage.setWindowTitle(_translate("reportPage", "Отчёты", None))
        self.lblExaroPath.setText(_translate("reportPage", "Внешний редактор отчетов Exaro", None))
        self.btnSelectDocumentEditor.setText(_translate("reportPage", "...", None))
        self.btnSelectExaroEditor.setText(_translate("reportPage", "...", None))
        self.lblDocumentEditor.setText(_translate("reportPage", "Внешний редактор &документов", None))
        self.btnSelectExtGenRep.setText(_translate("reportPage", "...", None))
        self.lblExtGenRep.setText(_translate("reportPage", "Внешний генератор &отчетов", None))

