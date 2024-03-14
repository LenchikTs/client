# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/media/pvtr/0F0C-3E3A/py-dev/samson/appendix/importNomenclature/appPreferencesDialog.ui'
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

class Ui_appPreferencesDialog(object):
    def setupUi(self, appPreferencesDialog):
        appPreferencesDialog.setObjectName(_fromUtf8("appPreferencesDialog"))
        appPreferencesDialog.resize(400, 300)
        appPreferencesDialog.setSizeGripEnabled(True)
        self.verticalLayout = QtGui.QVBoxLayout(appPreferencesDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.chkCreateNomenclatureDuringImport = QtGui.QCheckBox(appPreferencesDialog)
        self.chkCreateNomenclatureDuringImport.setObjectName(_fromUtf8("chkCreateNomenclatureDuringImport"))
        self.verticalLayout.addWidget(self.chkCreateNomenclatureDuringImport)
        self.chkLogErrors = QtGui.QCheckBox(appPreferencesDialog)
        self.chkLogErrors.setObjectName(_fromUtf8("chkLogErrors"))
        self.verticalLayout.addWidget(self.chkLogErrors)
        self.chkLogSuccess = QtGui.QCheckBox(appPreferencesDialog)
        self.chkLogSuccess.setObjectName(_fromUtf8("chkLogSuccess"))
        self.verticalLayout.addWidget(self.chkLogSuccess)
        self.gbService = QtGui.QGroupBox(appPreferencesDialog)
        self.gbService.setObjectName(_fromUtf8("gbService"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.gbService)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.chkAutoImport = QtGui.QCheckBox(self.gbService)
        self.chkAutoImport.setObjectName(_fromUtf8("chkAutoImport"))
        self.verticalLayout_2.addWidget(self.chkAutoImport)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblScanDir = QtGui.QLabel(self.gbService)
        self.lblScanDir.setObjectName(_fromUtf8("lblScanDir"))
        self.horizontalLayout.addWidget(self.lblScanDir)
        self.edtScanDir = QtGui.QLineEdit(self.gbService)
        self.edtScanDir.setObjectName(_fromUtf8("edtScanDir"))
        self.horizontalLayout.addWidget(self.edtScanDir)
        self.btnSelectScanDir = QtGui.QToolButton(self.gbService)
        self.btnSelectScanDir.setObjectName(_fromUtf8("btnSelectScanDir"))
        self.horizontalLayout.addWidget(self.btnSelectScanDir)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lblScanPeriod = QtGui.QLabel(self.gbService)
        self.lblScanPeriod.setObjectName(_fromUtf8("lblScanPeriod"))
        self.horizontalLayout_2.addWidget(self.lblScanPeriod)
        self.edtScanPeriod = QtGui.QSpinBox(self.gbService)
        self.edtScanPeriod.setMinimum(10)
        self.edtScanPeriod.setMaximum(60000)
        self.edtScanPeriod.setObjectName(_fromUtf8("edtScanPeriod"))
        self.horizontalLayout_2.addWidget(self.edtScanPeriod)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.gbService)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.lblOrganisation = QtGui.QLabel(appPreferencesDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblOrganisation.sizePolicy().hasHeightForWidth())
        self.lblOrganisation.setSizePolicy(sizePolicy)
        self.lblOrganisation.setMinimumSize(QtCore.QSize(130, 0))
        self.lblOrganisation.setObjectName(_fromUtf8("lblOrganisation"))
        self.horizontalLayout_3.addWidget(self.lblOrganisation)
        self.cmbOrganisation = CPolyclinicComboBox(appPreferencesDialog)
        self.cmbOrganisation.setObjectName(_fromUtf8("cmbOrganisation"))
        self.horizontalLayout_3.addWidget(self.cmbOrganisation)
        self.btnSelectOrganisation = QtGui.QToolButton(appPreferencesDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSelectOrganisation.sizePolicy().hasHeightForWidth())
        self.btnSelectOrganisation.setSizePolicy(sizePolicy)
        self.btnSelectOrganisation.setObjectName(_fromUtf8("btnSelectOrganisation"))
        self.horizontalLayout_3.addWidget(self.btnSelectOrganisation)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(appPreferencesDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.lblOrganisation.setBuddy(self.cmbOrganisation)

        self.retranslateUi(appPreferencesDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), appPreferencesDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), appPreferencesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(appPreferencesDialog)

    def retranslateUi(self, appPreferencesDialog):
        appPreferencesDialog.setWindowTitle(_translate("appPreferencesDialog", "Умолчания", None))
        self.chkCreateNomenclatureDuringImport.setText(_translate("appPreferencesDialog", "Создавать номенклатуру при импорте", None))
        self.chkLogErrors.setText(_translate("appPreferencesDialog", "Формировать файл ошибок загрузки", None))
        self.chkLogSuccess.setText(_translate("appPreferencesDialog", "Формировать файл успешной загрузки", None))
        self.gbService.setTitle(_translate("appPreferencesDialog", "Сервис", None))
        self.chkAutoImport.setText(_translate("appPreferencesDialog", "Автозапуск импорта", None))
        self.lblScanDir.setText(_translate("appPreferencesDialog", "Директория обмена", None))
        self.btnSelectScanDir.setText(_translate("appPreferencesDialog", "...", None))
        self.lblScanPeriod.setText(_translate("appPreferencesDialog", "Интервал проверки", None))
        self.edtScanPeriod.setSuffix(_translate("appPreferencesDialog", "сек", None))
        self.lblOrganisation.setText(_translate("appPreferencesDialog", "&ЛПУ", None))
        self.btnSelectOrganisation.setText(_translate("appPreferencesDialog", "...", None))

from Orgs.OrgComboBox import CPolyclinicComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    appPreferencesDialog = QtGui.QDialog()
    ui = Ui_appPreferencesDialog()
    ui.setupUi(appPreferencesDialog)
    appPreferencesDialog.show()
    sys.exit(app.exec_())

