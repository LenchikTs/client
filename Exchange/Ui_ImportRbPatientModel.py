# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ImportRbPatientModel.ui'
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

class Ui_ImportRbPatientModel(object):
    def setupUi(self, ImportRbPatientModel):
        ImportRbPatientModel.setObjectName(_fromUtf8("ImportRbPatientModel"))
        ImportRbPatientModel.resize(557, 420)
        self.gridLayout = QtGui.QGridLayout(ImportRbPatientModel)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(ImportRbPatientModel)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.edtFileName = QtGui.QLineEdit(ImportRbPatientModel)
        self.edtFileName.setObjectName(_fromUtf8("edtFileName"))
        self.gridLayout.addWidget(self.edtFileName, 0, 1, 1, 1)
        self.btnSelectFile = QtGui.QToolButton(ImportRbPatientModel)
        self.btnSelectFile.setObjectName(_fromUtf8("btnSelectFile"))
        self.gridLayout.addWidget(self.btnSelectFile, 0, 2, 1, 1)
        self.label_2 = QtGui.QLabel(ImportRbPatientModel)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.edtFileNameHelp = QtGui.QLineEdit(ImportRbPatientModel)
        self.edtFileNameHelp.setObjectName(_fromUtf8("edtFileNameHelp"))
        self.gridLayout.addWidget(self.edtFileNameHelp, 1, 1, 1, 1)
        self.btnSelectFileHelp = QtGui.QToolButton(ImportRbPatientModel)
        self.btnSelectFileHelp.setObjectName(_fromUtf8("btnSelectFileHelp"))
        self.gridLayout.addWidget(self.btnSelectFileHelp, 1, 2, 1, 1)
        self.progressBar = CProgressBar(ImportRbPatientModel)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 2, 0, 1, 3)
        self.chkFullLog = QtGui.QCheckBox(ImportRbPatientModel)
        self.chkFullLog.setObjectName(_fromUtf8("chkFullLog"))
        self.gridLayout.addWidget(self.chkFullLog, 3, 0, 1, 3)
        self.logBrowser = QtGui.QTextBrowser(ImportRbPatientModel)
        self.logBrowser.setObjectName(_fromUtf8("logBrowser"))
        self.gridLayout.addWidget(self.logBrowser, 4, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 0, 1, 3)
        self.statusLabel = QtGui.QLabel(ImportRbPatientModel)
        self.statusLabel.setText(_fromUtf8(""))
        self.statusLabel.setObjectName(_fromUtf8("statusLabel"))
        self.gridLayout.addWidget(self.statusLabel, 5, 0, 1, 3)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.btnImport = QtGui.QPushButton(ImportRbPatientModel)
        self.btnImport.setEnabled(False)
        self.btnImport.setObjectName(_fromUtf8("btnImport"))
        self.hboxlayout.addWidget(self.btnImport)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.btnAbort = QtGui.QPushButton(ImportRbPatientModel)
        self.btnAbort.setEnabled(False)
        self.btnAbort.setObjectName(_fromUtf8("btnAbort"))
        self.hboxlayout.addWidget(self.btnAbort)
        self.btnClose = QtGui.QPushButton(ImportRbPatientModel)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.hboxlayout.addWidget(self.btnClose)
        self.gridLayout.addLayout(self.hboxlayout, 7, 0, 1, 3)

        self.retranslateUi(ImportRbPatientModel)
        QtCore.QMetaObject.connectSlotsByName(ImportRbPatientModel)

    def retranslateUi(self, ImportRbPatientModel):
        ImportRbPatientModel.setWindowTitle(_translate("ImportRbPatientModel", "Импорт справочника `Модели пациента`", None))
        self.label.setText(_translate("ImportRbPatientModel", "Спарвочник «Модели пациента»", None))
        self.btnSelectFile.setText(_translate("ImportRbPatientModel", "...", None))
        self.label_2.setText(_translate("ImportRbPatientModel", "Справочник «Методы лечения»", None))
        self.btnSelectFileHelp.setText(_translate("ImportRbPatientModel", "...", None))
        self.chkFullLog.setText(_translate("ImportRbPatientModel", "Подробный отчет", None))
        self.btnImport.setText(_translate("ImportRbPatientModel", "Начать импорт", None))
        self.btnAbort.setText(_translate("ImportRbPatientModel", "Прервать", None))
        self.btnClose.setText(_translate("ImportRbPatientModel", "Закрыть", None))

from library.ProgressBar import CProgressBar

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ImportRbPatientModel = QtGui.QDialog()
    ui = Ui_ImportRbPatientModel()
    ui.setupUi(ImportRbPatientModel)
    ImportRbPatientModel.show()
    sys.exit(app.exec_())

