# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Samson\Exchange\ExportR67NativePage1.ui'
#
# Created: Wed Oct 19 21:18:56 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ExportPage1(object):
    def setupUi(self, ExportPage1):
        ExportPage1.setObjectName("ExportPage1")
        ExportPage1.resize(435, 300)
        self.gridlayout = QtGui.QGridLayout(ExportPage1)
        self.gridlayout.setObjectName("gridlayout")
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 0, 0, 1, 3)
        self.progressBar = CProgressBar(ExportPage1)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.gridlayout.addWidget(self.progressBar, 8, 0, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1, 9, 0, 1, 3)
        self.btnExport = QtGui.QPushButton(ExportPage1)
        self.btnExport.setObjectName("btnExport")
        self.gridlayout.addWidget(self.btnExport, 10, 1, 1, 1)
        self.btnCancel = QtGui.QPushButton(ExportPage1)
        self.btnCancel.setObjectName("btnCancel")
        self.gridlayout.addWidget(self.btnCancel, 10, 2, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem2, 10, 0, 1, 1)
        self.logBrowser = QtGui.QTextBrowser(ExportPage1)
        self.logBrowser.setObjectName("logBrowser")
        self.gridlayout.addWidget(self.logBrowser, 7, 0, 1, 3)
        self.chkVerboseLog = QtGui.QCheckBox(ExportPage1)
        self.chkVerboseLog.setObjectName("chkVerboseLog")
        self.gridlayout.addWidget(self.chkVerboseLog, 4, 0, 1, 1)
        self.chkIgnoreErrors = QtGui.QCheckBox(ExportPage1)
        self.chkIgnoreErrors.setEnabled(False)
        self.chkIgnoreErrors.setObjectName("chkIgnoreErrors")
        self.gridlayout.addWidget(self.chkIgnoreErrors, 6, 0, 1, 1)
        self.chkExportFormatAliens = QtGui.QCheckBox(ExportPage1)
        self.chkExportFormatAliens.setObjectName("chkExportFormatAliens")
        self.gridlayout.addWidget(self.chkExportFormatAliens, 1, 0, 1, 1)
        self.chkSkipZeroSum = QtGui.QCheckBox(ExportPage1)
        self.chkSkipZeroSum.setObjectName("chkSkipZeroSum")
        self.gridlayout.addWidget(self.chkSkipZeroSum, 2, 0, 1, 1)
        self.chkNumerateRecId = QtGui.QCheckBox(ExportPage1)
        self.chkNumerateRecId.setObjectName("chkNumerateRecId")
        self.gridlayout.addWidget(self.chkNumerateRecId, 3, 0, 1, 1)

        self.retranslateUi(ExportPage1)
        QtCore.QMetaObject.connectSlotsByName(ExportPage1)

    def retranslateUi(self, ExportPage1):
        ExportPage1.setWindowTitle(QtGui.QApplication.translate("ExportPage1", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.btnExport.setText(QtGui.QApplication.translate("ExportPage1", "экспорт", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setText(QtGui.QApplication.translate("ExportPage1", "прервать", None, QtGui.QApplication.UnicodeUTF8))
        self.chkVerboseLog.setText(QtGui.QApplication.translate("ExportPage1", "Подробный отчет", None, QtGui.QApplication.UnicodeUTF8))
        self.chkIgnoreErrors.setText(QtGui.QApplication.translate("ExportPage1", "Игнорировать ошибки", None, QtGui.QApplication.UnicodeUTF8))
        self.chkExportFormatAliens.setText(QtGui.QApplication.translate("ExportPage1", "Экспорт в формате иногородних", None, QtGui.QApplication.UnicodeUTF8))
        self.chkSkipZeroSum.setText(QtGui.QApplication.translate("ExportPage1", "Не выгружать записи с нулевой суммой", None, QtGui.QApplication.UnicodeUTF8))
        self.chkNumerateRecId.setToolTip(QtGui.QApplication.translate("ExportPage1", "Поле RECID в файле p*.dbf заполняется как счетчик от 1 до последней записи (1, 2, 3, 4 и т.д)", None, QtGui.QApplication.UnicodeUTF8))
        self.chkNumerateRecId.setText(QtGui.QApplication.translate("ExportPage1", "Порядковая нумерация записей", None, QtGui.QApplication.UnicodeUTF8))

from library.ProgressBar import CProgressBar

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ExportPage1 = QtGui.QWidget()
    ui = Ui_ExportPage1()
    ui.setupUi(ExportPage1)
    ExportPage1.show()
    sys.exit(app.exec_())

