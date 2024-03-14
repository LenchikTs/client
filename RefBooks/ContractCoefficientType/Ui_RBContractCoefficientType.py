# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/RefBooks/RBContractCoefficientType.ui'
#
# Created: Fri Oct 28 14:52:37 2016
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

class Ui_RBContractCoefficientType(object):
    def setupUi(self, RBContractCoefficientType):
        RBContractCoefficientType.setObjectName(_fromUtf8("RBContractCoefficientType"))
        RBContractCoefficientType.resize(524, 435)
        RBContractCoefficientType.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(RBContractCoefficientType)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblCode = QtGui.QLabel(RBContractCoefficientType)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.edtCode = QtGui.QLineEdit(RBContractCoefficientType)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout.addWidget(self.edtCode, 0, 1, 1, 1)
        self.lblRegionalCode = QtGui.QLabel(RBContractCoefficientType)
        self.lblRegionalCode.setObjectName(_fromUtf8("lblRegionalCode"))
        self.gridLayout.addWidget(self.lblRegionalCode, 1, 0, 1, 1)
        self.edtRegionalCode = QtGui.QLineEdit(RBContractCoefficientType)
        self.edtRegionalCode.setObjectName(_fromUtf8("edtRegionalCode"))
        self.gridLayout.addWidget(self.edtRegionalCode, 1, 1, 1, 1)
        self.lblFederalCode = QtGui.QLabel(RBContractCoefficientType)
        self.lblFederalCode.setObjectName(_fromUtf8("lblFederalCode"))
        self.gridLayout.addWidget(self.lblFederalCode, 2, 0, 1, 1)
        self.edtFederalCode = QtGui.QLineEdit(RBContractCoefficientType)
        self.edtFederalCode.setObjectName(_fromUtf8("edtFederalCode"))
        self.gridLayout.addWidget(self.edtFederalCode, 2, 1, 1, 1)
        self.lblName = QtGui.QLabel(RBContractCoefficientType)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 3, 0, 1, 1)
        self.edtName = QtGui.QLineEdit(RBContractCoefficientType)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 3, 1, 1, 1)
        self.tabWidget = QtGui.QTabWidget(RBContractCoefficientType)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabSigns = QtGui.QWidget()
        self.tabSigns.setObjectName(_fromUtf8("tabSigns"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tabSigns)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tblSigns = CInDocTableView(self.tabSigns)
        self.tblSigns.setObjectName(_fromUtf8("tblSigns"))
        self.verticalLayout.addWidget(self.tblSigns)
        self.tabWidget.addTab(self.tabSigns, _fromUtf8(""))
        self.tabAlgorithm = QtGui.QWidget()
        self.tabAlgorithm.setObjectName(_fromUtf8("tabAlgorithm"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tabAlgorithm)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lblAlgorithm = QtGui.QLabel(self.tabAlgorithm)
        self.lblAlgorithm.setTextFormat(QtCore.Qt.RichText)
        self.lblAlgorithm.setObjectName(_fromUtf8("lblAlgorithm"))
        self.gridLayout_2.addWidget(self.lblAlgorithm, 0, 0, 1, 1)
        self.edtAlgorithm = QtGui.QPlainTextEdit(self.tabAlgorithm)
        self.edtAlgorithm.setObjectName(_fromUtf8("edtAlgorithm"))
        self.gridLayout_2.addWidget(self.edtAlgorithm, 1, 0, 1, 1)
        self.btnTestAlgorithm = QtGui.QPushButton(self.tabAlgorithm)
        self.btnTestAlgorithm.setObjectName(_fromUtf8("btnTestAlgorithm"))
        self.gridLayout_2.addWidget(self.btnTestAlgorithm, 2, 0, 1, 1)
        self.tabWidget.addTab(self.tabAlgorithm, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 4, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(RBContractCoefficientType)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 2)
        self.lblCode.setBuddy(self.edtCode)
        self.lblRegionalCode.setBuddy(self.edtRegionalCode)
        self.lblFederalCode.setBuddy(self.edtFederalCode)
        self.lblName.setBuddy(self.edtName)

        self.retranslateUi(RBContractCoefficientType)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBContractCoefficientType.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBContractCoefficientType.reject)
        QtCore.QMetaObject.connectSlotsByName(RBContractCoefficientType)
        RBContractCoefficientType.setTabOrder(self.edtCode, self.edtRegionalCode)
        RBContractCoefficientType.setTabOrder(self.edtRegionalCode, self.edtFederalCode)
        RBContractCoefficientType.setTabOrder(self.edtFederalCode, self.edtName)
        RBContractCoefficientType.setTabOrder(self.edtName, self.tabWidget)
        RBContractCoefficientType.setTabOrder(self.tabWidget, self.tblSigns)
        RBContractCoefficientType.setTabOrder(self.tblSigns, self.edtAlgorithm)
        RBContractCoefficientType.setTabOrder(self.edtAlgorithm, self.btnTestAlgorithm)
        RBContractCoefficientType.setTabOrder(self.btnTestAlgorithm, self.buttonBox)

    def retranslateUi(self, RBContractCoefficientType):
        RBContractCoefficientType.setWindowTitle(_translate("RBContractCoefficientType", "ChangeMe!", None))
        self.lblCode.setText(_translate("RBContractCoefficientType", "&Код", None))
        self.lblRegionalCode.setText(_translate("RBContractCoefficientType", "&Региональный код", None))
        self.lblFederalCode.setText(_translate("RBContractCoefficientType", "&Федеральный код", None))
        self.lblName.setText(_translate("RBContractCoefficientType", "&Наименование", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSigns), _translate("RBContractCoefficientType", "Условия применения", None))
        self.lblAlgorithm.setText(_translate("RBContractCoefficientType", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Tahoma\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Алгоритм расчёта значения коэффициента основываясь на свойствах события и МЭСа.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Переменнные:</p>\n"
"<table border=\"0\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;\" cellspacing=\"2\" cellpadding=\"0\">\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">k</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">значение коэффициента из договора</p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">duration</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">длительность события</p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">minDuration</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">минимальная длительность согласно МЭС</p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">maxDuration</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">максимальная длительность согласно МЭС</p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">avgDuration</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">средняя длительность согласно МЭС</p></td></tr></table>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Пустое значение из соображений совместимости соответствует <span style=\" font-weight:600;\">k</span></p></body></html>", None))
        self.btnTestAlgorithm.setText(_translate("RBContractCoefficientType", "Проверить алгоритм", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAlgorithm), _translate("RBContractCoefficientType", "Алгоритм расчёта", None))

from library.InDocTable import CInDocTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RBContractCoefficientType = QtGui.QDialog()
    ui = Ui_RBContractCoefficientType()
    ui.setupUi(RBContractCoefficientType)
    RBContractCoefficientType.show()
    sys.exit(app.exec_())

