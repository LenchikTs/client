# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/Exchange/ImportRbServiceR29.ui'
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

class Ui_ImportRbService(object):
    def setupUi(self, ImportRbService):
        ImportRbService.setObjectName(_fromUtf8("ImportRbService"))
        ImportRbService.resize(608, 788)
        self.gridlayout = QtGui.QGridLayout(ImportRbService)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.statusLabel = QtGui.QLabel(ImportRbService)
        self.statusLabel.setText(_fromUtf8(""))
        self.statusLabel.setObjectName(_fromUtf8("statusLabel"))
        self.gridlayout.addWidget(self.statusLabel, 5, 0, 1, 1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.label = QtGui.QLabel(ImportRbService)
        self.label.setObjectName(_fromUtf8("label"))
        self.hboxlayout.addWidget(self.label)
        self.edtFileName = QtGui.QLineEdit(ImportRbService)
        self.edtFileName.setObjectName(_fromUtf8("edtFileName"))
        self.hboxlayout.addWidget(self.edtFileName)
        self.btnSelectFile = QtGui.QToolButton(ImportRbService)
        self.btnSelectFile.setObjectName(_fromUtf8("btnSelectFile"))
        self.hboxlayout.addWidget(self.btnSelectFile)
        self.gridlayout.addLayout(self.hboxlayout, 0, 0, 1, 1)
        self.progressBar = CProgressBar(ImportRbService)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridlayout.addWidget(self.progressBar, 1, 0, 1, 1)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.btnImport = QtGui.QPushButton(ImportRbService)
        self.btnImport.setEnabled(False)
        self.btnImport.setObjectName(_fromUtf8("btnImport"))
        self.hboxlayout1.addWidget(self.btnImport)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem)
        self.btnAbort = QtGui.QPushButton(ImportRbService)
        self.btnAbort.setEnabled(False)
        self.btnAbort.setObjectName(_fromUtf8("btnAbort"))
        self.hboxlayout1.addWidget(self.btnAbort)
        self.btnClose = QtGui.QPushButton(ImportRbService)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.hboxlayout1.addWidget(self.btnClose)
        self.gridlayout.addLayout(self.hboxlayout1, 17, 0, 1, 1)
        self.logBrowser = QtGui.QTextBrowser(ImportRbService)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logBrowser.sizePolicy().hasHeightForWidth())
        self.logBrowser.setSizePolicy(sizePolicy)
        self.logBrowser.setMaximumSize(QtCore.QSize(16777215, 13000000))
        self.logBrowser.setObjectName(_fromUtf8("logBrowser"))
        self.gridlayout.addWidget(self.logBrowser, 6, 0, 3, 1)
        self.gbKinaProfilMedicalAid = QtGui.QGroupBox(ImportRbService)
        self.gbKinaProfilMedicalAid.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbKinaProfilMedicalAid.sizePolicy().hasHeightForWidth())
        self.gbKinaProfilMedicalAid.setSizePolicy(sizePolicy)
        self.gbKinaProfilMedicalAid.setObjectName(_fromUtf8("gbKinaProfilMedicalAid"))
        self.cmbMedicalAidKind = CRBComboBox(self.gbKinaProfilMedicalAid)
        self.cmbMedicalAidKind.setGeometry(QtCore.QRect(140, 20, 441, 20))
        self.cmbMedicalAidKind.setObjectName(_fromUtf8("cmbMedicalAidKind"))
        self.cmbSpeciality = CRBComboBox(self.gbKinaProfilMedicalAid)
        self.cmbSpeciality.setGeometry(QtCore.QRect(140, 50, 441, 20))
        self.cmbSpeciality.setObjectName(_fromUtf8("cmbSpeciality"))
        self.cmbMedicalAidProfile = CRBComboBox(self.gbKinaProfilMedicalAid)
        self.cmbMedicalAidProfile.setGeometry(QtCore.QRect(139, 80, 441, 20))
        self.cmbMedicalAidProfile.setObjectName(_fromUtf8("cmbMedicalAidProfile"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.gbKinaProfilMedicalAid)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 110, 571, 22))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btnAdd = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.btnAdd.setMaximumSize(QtCore.QSize(60, 20))
        self.btnAdd.setObjectName(_fromUtf8("btnAdd"))
        self.horizontalLayout.addWidget(self.btnAdd)
        self.tableView = QtGui.QTableView(self.gbKinaProfilMedicalAid)
        self.tableView.setGeometry(QtCore.QRect(10, 190, 571, 211))
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.lblMedicalAidKind = QtGui.QLabel(self.gbKinaProfilMedicalAid)
        self.lblMedicalAidKind.setGeometry(QtCore.QRect(10, 20, 91, 16))
        self.lblMedicalAidKind.setObjectName(_fromUtf8("lblMedicalAidKind"))
        self.lblSpeciality = QtGui.QLabel(self.gbKinaProfilMedicalAid)
        self.lblSpeciality.setGeometry(QtCore.QRect(10, 50, 91, 16))
        self.lblSpeciality.setObjectName(_fromUtf8("lblSpeciality"))
        self.lblProfile = QtGui.QLabel(self.gbKinaProfilMedicalAid)
        self.lblProfile.setGeometry(QtCore.QRect(10, 80, 46, 13))
        self.lblProfile.setObjectName(_fromUtf8("lblProfile"))
        self.lblInfo = QtGui.QLabel(self.gbKinaProfilMedicalAid)
        self.lblInfo.setGeometry(QtCore.QRect(20, 130, 561, 41))
        self.lblInfo.setObjectName(_fromUtf8("lblInfo"))
        self.btnContinue = QtGui.QPushButton(self.gbKinaProfilMedicalAid)
        self.btnContinue.setGeometry(QtCore.QRect(510, 410, 75, 23))
        self.btnContinue.setObjectName(_fromUtf8("btnContinue"))
        self.cmbMedicalAidKind.raise_()
        self.cmbSpeciality.raise_()
        self.cmbMedicalAidProfile.raise_()
        self.horizontalLayoutWidget.raise_()
        self.tableView.raise_()
        self.lblMedicalAidKind.raise_()
        self.lblSpeciality.raise_()
        self.lblProfile.raise_()
        self.lblInfo.raise_()
        self.btnContinue.raise_()
        self.logBrowser.raise_()
        self.gridlayout.addWidget(self.gbKinaProfilMedicalAid, 15, 0, 1, 1)
        self.chkFullLog = QtGui.QCheckBox(ImportRbService)
        self.chkFullLog.setObjectName(_fromUtf8("chkFullLog"))
        self.gridlayout.addWidget(self.chkFullLog, 4, 0, 1, 1)

        self.retranslateUi(ImportRbService)
        QtCore.QMetaObject.connectSlotsByName(ImportRbService)

    def retranslateUi(self, ImportRbService):
        ImportRbService.setWindowTitle(_translate("ImportRbService", "Импорт справочника \"Услуги\"", None))
        self.label.setText(_translate("ImportRbService", "Загрузить из", None))
        self.btnSelectFile.setText(_translate("ImportRbService", "...", None))
        self.btnImport.setText(_translate("ImportRbService", "Начать импорт", None))
        self.btnAbort.setText(_translate("ImportRbService", "Прервать", None))
        self.btnClose.setText(_translate("ImportRbService", "Закрыть", None))
        self.gbKinaProfilMedicalAid.setTitle(_translate("ImportRbService", "Выберите вид и профиль мед. помощи", None))
        self.btnAdd.setText(_translate("ImportRbService", "Добавить", None))
        self.lblMedicalAidKind.setText(_translate("ImportRbService", "Вид мед. помощи", None))
        self.lblSpeciality.setText(_translate("ImportRbService", "Специальность", None))
        self.lblProfile.setText(_translate("ImportRbService", "Профиль", None))
        self.lblInfo.setText(_translate("ImportRbService", "Информация", None))
        self.btnContinue.setText(_translate("ImportRbService", "Продолжить", None))
        self.chkFullLog.setText(_translate("ImportRbService", "Подробный отчет", None))

from library.ProgressBar import CProgressBar
from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ImportRbService = QtGui.QDialog()
    ui = Ui_ImportRbService()
    ui.setupUi(ImportRbService)
    ImportRbService.show()
    sys.exit(app.exec_())

