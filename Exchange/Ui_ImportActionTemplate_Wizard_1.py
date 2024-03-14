# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\py\s11-svn\Exchange\ImportActionTemplate_Wizard_1.ui'
#
# Created: Tue Apr 07 19:31:45 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ImportActionTemplate_Wizard_1(object):
    def setupUi(self, ImportActionTemplate_Wizard_1):
        ImportActionTemplate_Wizard_1.setObjectName("ImportActionTemplate_Wizard_1")
        ImportActionTemplate_Wizard_1.resize(475, 429)
        self.gridlayout = QtGui.QGridLayout(ImportActionTemplate_Wizard_1)
        self.gridlayout.setObjectName("gridlayout")
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName("hboxlayout")
        self.label = QtGui.QLabel(ImportActionTemplate_Wizard_1)
        self.label.setObjectName("label")
        self.hboxlayout.addWidget(self.label)
        self.edtFileName = QtGui.QLineEdit(ImportActionTemplate_Wizard_1)
        self.edtFileName.setObjectName("edtFileName")
        self.hboxlayout.addWidget(self.edtFileName)
        self.btnSelectFile = QtGui.QToolButton(ImportActionTemplate_Wizard_1)
        self.btnSelectFile.setObjectName("btnSelectFile")
        self.hboxlayout.addWidget(self.btnSelectFile)
        self.gridlayout.addLayout(self.hboxlayout, 0, 0, 1, 1)
        self.progressBar = CProgressBar(ImportActionTemplate_Wizard_1)
        self.progressBar.setProperty("value", QtCore.QVariant(24))
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName("progressBar")
        self.gridlayout.addWidget(self.progressBar, 2, 0, 1, 1)
        self.statusLabel = QtGui.QLabel(ImportActionTemplate_Wizard_1)
        self.statusLabel.setObjectName("statusLabel")
        self.gridlayout.addWidget(self.statusLabel, 5, 0, 1, 1)
        self.logBrowser = QtGui.QTextBrowser(ImportActionTemplate_Wizard_1)
        self.logBrowser.setObjectName("logBrowser")
        self.gridlayout.addWidget(self.logBrowser, 4, 0, 1, 1)
        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setObjectName("vboxlayout")
        self.groupBox = QtGui.QGroupBox(ImportActionTemplate_Wizard_1)
        self.groupBox.setObjectName("groupBox")
        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout1.setObjectName("vboxlayout1")
        self.rbAskUser = QtGui.QRadioButton(self.groupBox)
        self.rbAskUser.setEnabled(True)
        self.rbAskUser.setChecked(True)
        self.rbAskUser.setObjectName("rbAskUser")
        self.vboxlayout1.addWidget(self.rbAskUser)
        self.rbUpdate = QtGui.QRadioButton(self.groupBox)
        self.rbUpdate.setChecked(False)
        self.rbUpdate.setObjectName("rbUpdate")
        self.vboxlayout1.addWidget(self.rbUpdate)
        self.rbSkip = QtGui.QRadioButton(self.groupBox)
        self.rbSkip.setObjectName("rbSkip")
        self.vboxlayout1.addWidget(self.rbSkip)
        self.vboxlayout.addWidget(self.groupBox)
        self.gridlayout.addLayout(self.vboxlayout, 1, 0, 1, 1)
        self.chkFullLog = QtGui.QCheckBox(ImportActionTemplate_Wizard_1)
        self.chkFullLog.setObjectName("chkFullLog")
        self.gridlayout.addWidget(self.chkFullLog, 3, 0, 1, 1)

        self.retranslateUi(ImportActionTemplate_Wizard_1)
        QtCore.QMetaObject.connectSlotsByName(ImportActionTemplate_Wizard_1)

    def retranslateUi(self, ImportActionTemplate_Wizard_1):
        ImportActionTemplate_Wizard_1.setWindowTitle(QtGui.QApplication.translate("ImportActionTemplate_Wizard_1", "Импорт шаблонов ", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ImportActionTemplate_Wizard_1", "Загрузить из", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSelectFile.setText(QtGui.QApplication.translate("ImportActionTemplate_Wizard_1", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("ImportActionTemplate_Wizard_1", "Совпадающие записи", None, QtGui.QApplication.UnicodeUTF8))
        self.rbAskUser.setText(QtGui.QApplication.translate("ImportActionTemplate_Wizard_1", "Спрашивать действие у пользователя", None, QtGui.QApplication.UnicodeUTF8))
        self.rbUpdate.setText(QtGui.QApplication.translate("ImportActionTemplate_Wizard_1", "Обновлять", None, QtGui.QApplication.UnicodeUTF8))
        self.rbSkip.setText(QtGui.QApplication.translate("ImportActionTemplate_Wizard_1", "Пропускать", None, QtGui.QApplication.UnicodeUTF8))
        self.chkFullLog.setText(QtGui.QApplication.translate("ImportActionTemplate_Wizard_1", "Подробный отчет", None, QtGui.QApplication.UnicodeUTF8))

from library.ProgressBar import CProgressBar

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ImportActionTemplate_Wizard_1 = QtGui.QDialog()
    ui = Ui_ImportActionTemplate_Wizard_1()
    ui.setupUi(ImportActionTemplate_Wizard_1)
    ImportActionTemplate_Wizard_1.show()
    sys.exit(app.exec_())

