# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/Exchange/ImportRbServiceR29_2.ui'
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

class Ui_ImportRbServiceR29_2(object):
    def setupUi(self, ImportRbServiceR29_2):
        ImportRbServiceR29_2.setObjectName(_fromUtf8("ImportRbServiceR29_2"))
        ImportRbServiceR29_2.resize(623, 508)
        self.gbKinaProfilMedicalAid = QtGui.QGroupBox(ImportRbServiceR29_2)
        self.gbKinaProfilMedicalAid.setEnabled(True)
        self.gbKinaProfilMedicalAid.setGeometry(QtCore.QRect(20, 10, 590, 461))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbKinaProfilMedicalAid.sizePolicy().hasHeightForWidth())
        self.gbKinaProfilMedicalAid.setSizePolicy(sizePolicy)
        self.gbKinaProfilMedicalAid.setObjectName(_fromUtf8("gbKinaProfilMedicalAid"))
        self.layoutWidget = QtGui.QWidget(self.gbKinaProfilMedicalAid)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 561, 145))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.layoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.txtGroup = QtGui.QLabel(self.layoutWidget)
        self.txtGroup.setObjectName(_fromUtf8("txtGroup"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.txtGroup)
        self.cmbServiceGroup = CRBComboBox(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbServiceGroup.sizePolicy().hasHeightForWidth())
        self.cmbServiceGroup.setSizePolicy(sizePolicy)
        self.cmbServiceGroup.setMinimumSize(QtCore.QSize(150, 0))
        self.cmbServiceGroup.setObjectName(_fromUtf8("cmbServiceGroup"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.cmbServiceGroup)
        self.lblMedicalAidKind = QtGui.QLabel(self.layoutWidget)
        self.lblMedicalAidKind.setObjectName(_fromUtf8("lblMedicalAidKind"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.lblMedicalAidKind)
        self.cmbMedicalAidKind = CRBComboBox(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbMedicalAidKind.sizePolicy().hasHeightForWidth())
        self.cmbMedicalAidKind.setSizePolicy(sizePolicy)
        self.cmbMedicalAidKind.setObjectName(_fromUtf8("cmbMedicalAidKind"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.cmbMedicalAidKind)
        self.lblMedicalAidType = QtGui.QLabel(self.layoutWidget)
        self.lblMedicalAidType.setObjectName(_fromUtf8("lblMedicalAidType"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.lblMedicalAidType)
        self.lblProfile = QtGui.QLabel(self.layoutWidget)
        self.lblProfile.setObjectName(_fromUtf8("lblProfile"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.lblProfile)
        self.cmbMedicalAidType = CRBComboBox(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbMedicalAidType.sizePolicy().hasHeightForWidth())
        self.cmbMedicalAidType.setSizePolicy(sizePolicy)
        self.cmbMedicalAidType.setObjectName(_fromUtf8("cmbMedicalAidType"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.cmbMedicalAidType)
        self.cmbMedicalAidProfile = CRBComboBox(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbMedicalAidProfile.sizePolicy().hasHeightForWidth())
        self.cmbMedicalAidProfile.setSizePolicy(sizePolicy)
        self.cmbMedicalAidProfile.setObjectName(_fromUtf8("cmbMedicalAidProfile"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.cmbMedicalAidProfile)
        self.layoutWidget1 = QtGui.QWidget(self.gbKinaProfilMedicalAid)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 200, 571, 213))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tblCoord = CInDocTableView(self.layoutWidget1)
        self.tblCoord.setObjectName(_fromUtf8("tblCoord"))
        self.verticalLayout.addWidget(self.tblCoord)
        self.layoutWidget2 = QtGui.QWidget(self.gbKinaProfilMedicalAid)
        self.layoutWidget2.setGeometry(QtCore.QRect(310, 420, 262, 25))
        self.layoutWidget2.setObjectName(_fromUtf8("layoutWidget2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(150, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btnContinue = QtGui.QPushButton(self.layoutWidget2)
        self.btnContinue.setObjectName(_fromUtf8("btnContinue"))
        self.horizontalLayout_2.addWidget(self.btnContinue)
        self.btnClose = QtGui.QPushButton(ImportRbServiceR29_2)
        self.btnClose.setGeometry(QtCore.QRect(520, 470, 75, 23))
        self.btnClose.setObjectName(_fromUtf8("btnClose"))

        self.retranslateUi(ImportRbServiceR29_2)
        QtCore.QMetaObject.connectSlotsByName(ImportRbServiceR29_2)

    def retranslateUi(self, ImportRbServiceR29_2):
        ImportRbServiceR29_2.setWindowTitle(_translate("ImportRbServiceR29_2", "Импорт справочника \"Услуги\"", None))
        self.gbKinaProfilMedicalAid.setTitle(_translate("ImportRbServiceR29_2", "Выберите вид и профиль мед. помощи", None))
        self.txtGroup.setText(_translate("ImportRbServiceR29_2", "Группа услуг", None))
        self.lblMedicalAidKind.setText(_translate("ImportRbServiceR29_2", "Вид мед. помощи", None))
        self.lblMedicalAidType.setText(_translate("ImportRbServiceR29_2", "Тип мед. помощи", None))
        self.lblProfile.setText(_translate("ImportRbServiceR29_2", "Профиль", None))
        self.btnContinue.setText(_translate("ImportRbServiceR29_2", "Добавить в услугу", None))
        self.btnClose.setText(_translate("ImportRbServiceR29_2", "Закрыть", None))

from library.InDocTable import CInDocTableView
from library.crbcombobox import CRBComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ImportRbServiceR29_2 = QtGui.QDialog()
    ui = Ui_ImportRbServiceR29_2()
    ui.setupUi(ImportRbServiceR29_2)
    ImportRbServiceR29_2.show()
    sys.exit(app.exec_())

