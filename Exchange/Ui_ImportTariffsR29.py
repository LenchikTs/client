# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/Exchange/ImportTariffsR29.ui'
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

class Ui_ImportTariffsR29(object):
    def setupUi(self, ImportTariffsR29):
        ImportTariffsR29.setObjectName(_fromUtf8("ImportTariffsR29"))
        ImportTariffsR29.resize(544, 320)
        self.lblStatus = QtGui.QLabel(ImportTariffsR29)
        self.lblStatus.setGeometry(QtCore.QRect(0, 398, 16, 16))
        self.lblStatus.setText(_fromUtf8(""))
        self.lblStatus.setObjectName(_fromUtf8("lblStatus"))
        self.splitter = QtGui.QSplitter(ImportTariffsR29)
        self.splitter.setGeometry(QtCore.QRect(20, 5, 511, 302))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.widget = QtGui.QWidget(self.splitter)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.edtFileName = QtGui.QLineEdit(self.widget)
        self.edtFileName.setObjectName(_fromUtf8("edtFileName"))
        self.horizontalLayout.addWidget(self.edtFileName)
        self.btnSelectFile = QtGui.QToolButton(self.widget)
        self.btnSelectFile.setObjectName(_fromUtf8("btnSelectFile"))
        self.horizontalLayout.addWidget(self.btnSelectFile)
        self.widget1 = QtGui.QWidget(self.splitter)
        self.widget1.setObjectName(_fromUtf8("widget1"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget1)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.chkFullLog = QtGui.QCheckBox(self.widget1)
        self.chkFullLog.setObjectName(_fromUtf8("chkFullLog"))
        self.verticalLayout.addWidget(self.chkFullLog)
        self.chkUpdateTariff = QtGui.QCheckBox(self.widget1)
        self.chkUpdateTariff.setObjectName(_fromUtf8("chkUpdateTariff"))
        self.verticalLayout.addWidget(self.chkUpdateTariff)
        self.progressBar = CProgressBar(self.splitter)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.log = QtGui.QTextBrowser(self.splitter)
        self.log.setObjectName(_fromUtf8("log"))
        self.widget2 = QtGui.QWidget(self.splitter)
        self.widget2.setObjectName(_fromUtf8("widget2"))
        self.hboxlayout = QtGui.QHBoxLayout(self.widget2)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.btnImport = QtGui.QPushButton(self.widget2)
        self.btnImport.setEnabled(False)
        self.btnImport.setObjectName(_fromUtf8("btnImport"))
        self.hboxlayout.addWidget(self.btnImport)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.btnClose = QtGui.QPushButton(self.widget2)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.hboxlayout.addWidget(self.btnClose)
        self.label.setBuddy(self.edtFileName)

        self.retranslateUi(ImportTariffsR29)
        QtCore.QMetaObject.connectSlotsByName(ImportTariffsR29)
        ImportTariffsR29.setTabOrder(self.edtFileName, self.btnSelectFile)
        ImportTariffsR29.setTabOrder(self.btnSelectFile, self.chkFullLog)
        ImportTariffsR29.setTabOrder(self.chkFullLog, self.chkUpdateTariff)
        ImportTariffsR29.setTabOrder(self.chkUpdateTariff, self.log)
        ImportTariffsR29.setTabOrder(self.log, self.btnImport)
        ImportTariffsR29.setTabOrder(self.btnImport, self.btnClose)

    def retranslateUi(self, ImportTariffsR29):
        ImportTariffsR29.setWindowTitle(_translate("ImportTariffsR29", "Импорт тарифов для Архангельской области", None))
        self.label.setText(_translate("ImportTariffsR29", "Загрузить из", None))
        self.btnSelectFile.setText(_translate("ImportTariffsR29", "...", None))
        self.chkFullLog.setText(_translate("ImportTariffsR29", "Подробный отчет", None))
        self.chkUpdateTariff.setText(_translate("ImportTariffsR29", "Обновлять совпадающие тарифы", None))
        self.btnImport.setText(_translate("ImportTariffsR29", "Начать импорт", None))
        self.btnClose.setText(_translate("ImportTariffsR29", "Закрыть", None))

from library.ProgressBar import CProgressBar

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ImportTariffsR29 = QtGui.QDialog()
    ui = Ui_ImportTariffsR29()
    ui.setupUi(ImportTariffsR29)
    ImportTariffsR29.show()
    sys.exit(app.exec_())

