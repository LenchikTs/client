# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/Exchange/ImportRbServiceR29_1.ui'
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

class Ui_ImportRbServiceR29_1(object):
    def setupUi(self, ImportRbServiceR29_1):
        ImportRbServiceR29_1.setObjectName(_fromUtf8("ImportRbServiceR29_1"))
        ImportRbServiceR29_1.resize(608, 465)
        self.gridlayout = QtGui.QGridLayout(ImportRbServiceR29_1)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.statusLabel = QtGui.QLabel(ImportRbServiceR29_1)
        self.statusLabel.setText(_fromUtf8(""))
        self.statusLabel.setObjectName(_fromUtf8("statusLabel"))
        self.gridlayout.addWidget(self.statusLabel, 5, 0, 1, 1)
        self.chkFullLog = QtGui.QCheckBox(ImportRbServiceR29_1)
        self.chkFullLog.setObjectName(_fromUtf8("chkFullLog"))
        self.gridlayout.addWidget(self.chkFullLog, 4, 0, 1, 1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.label = QtGui.QLabel(ImportRbServiceR29_1)
        self.label.setObjectName(_fromUtf8("label"))
        self.hboxlayout.addWidget(self.label)
        self.edtFileName = QtGui.QLineEdit(ImportRbServiceR29_1)
        self.edtFileName.setObjectName(_fromUtf8("edtFileName"))
        self.hboxlayout.addWidget(self.edtFileName)
        self.btnSelectFile = QtGui.QToolButton(ImportRbServiceR29_1)
        self.btnSelectFile.setObjectName(_fromUtf8("btnSelectFile"))
        self.hboxlayout.addWidget(self.btnSelectFile)
        self.gridlayout.addLayout(self.hboxlayout, 0, 0, 1, 1)
        self.progressBar = CProgressBar(ImportRbServiceR29_1)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridlayout.addWidget(self.progressBar, 1, 0, 1, 1)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.btnImport = QtGui.QPushButton(ImportRbServiceR29_1)
        self.btnImport.setEnabled(False)
        self.btnImport.setObjectName(_fromUtf8("btnImport"))
        self.hboxlayout1.addWidget(self.btnImport)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem)
        self.btnAbort = QtGui.QPushButton(ImportRbServiceR29_1)
        self.btnAbort.setEnabled(False)
        self.btnAbort.setObjectName(_fromUtf8("btnAbort"))
        self.hboxlayout1.addWidget(self.btnAbort)
        self.btnClose = QtGui.QPushButton(ImportRbServiceR29_1)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.hboxlayout1.addWidget(self.btnClose)
        self.gridlayout.addLayout(self.hboxlayout1, 16, 0, 1, 1)
        self.logBrowser = QtGui.QTextBrowser(ImportRbServiceR29_1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logBrowser.sizePolicy().hasHeightForWidth())
        self.logBrowser.setSizePolicy(sizePolicy)
        self.logBrowser.setMaximumSize(QtCore.QSize(16777215, 13000000))
        self.logBrowser.setObjectName(_fromUtf8("logBrowser"))
        self.gridlayout.addWidget(self.logBrowser, 6, 0, 3, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1, 9, 0, 1, 1)

        self.retranslateUi(ImportRbServiceR29_1)
        QtCore.QMetaObject.connectSlotsByName(ImportRbServiceR29_1)

    def retranslateUi(self, ImportRbServiceR29_1):
        ImportRbServiceR29_1.setWindowTitle(_translate("ImportRbServiceR29_1", "Импорт справочника \"Услуги\"", None))
        self.chkFullLog.setText(_translate("ImportRbServiceR29_1", "Подробный отчет", None))
        self.label.setText(_translate("ImportRbServiceR29_1", "Загрузить из", None))
        self.btnSelectFile.setText(_translate("ImportRbServiceR29_1", "...", None))
        self.btnImport.setText(_translate("ImportRbServiceR29_1", "Начать импорт", None))
        self.btnAbort.setText(_translate("ImportRbServiceR29_1", "Прервать", None))
        self.btnClose.setText(_translate("ImportRbServiceR29_1", "Закрыть", None))

from library.ProgressBar import CProgressBar

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ImportRbServiceR29_1 = QtGui.QDialog()
    ui = Ui_ImportRbServiceR29_1()
    ui.setupUi(ImportRbServiceR29_1)
    ImportRbServiceR29_1.show()
    sys.exit(app.exec_())

