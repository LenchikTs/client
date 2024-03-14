# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\kmivc\Samson\UP_s11\client\Exchange\ImportDispPlanQtysDialog.ui'
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

class Ui_ImportDispPlanQtysDialog(object):
    def setupUi(self, ImportDispPlanQtysDialog):
        ImportDispPlanQtysDialog.setObjectName(_fromUtf8("ImportDispPlanQtysDialog"))
        ImportDispPlanQtysDialog.resize(522, 392)
        self.verticalLayout = QtGui.QVBoxLayout(ImportDispPlanQtysDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(ImportDispPlanQtysDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.label_2 = QtGui.QLabel(ImportDispPlanQtysDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.sbYear = QtGui.QSpinBox(ImportDispPlanQtysDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sbYear.sizePolicy().hasHeightForWidth())
        self.sbYear.setSizePolicy(sizePolicy)
        self.sbYear.setMinimum(2017)
        self.sbYear.setMaximum(9999)
        self.sbYear.setObjectName(_fromUtf8("sbYear"))
        self.gridLayout.addWidget(self.sbYear, 2, 1, 1, 1)
        self.label_3 = QtGui.QLabel(ImportDispPlanQtysDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 2, 1, 1)
        self.btnGetFromService = QtGui.QPushButton(ImportDispPlanQtysDialog)
        self.btnGetFromService.setObjectName(_fromUtf8("btnGetFromService"))
        self.gridLayout.addWidget(self.btnGetFromService, 0, 5, 1, 1)
        self.cmbOrgStructure = CDbComboBox(ImportDispPlanQtysDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbOrgStructure.sizePolicy().hasHeightForWidth())
        self.cmbOrgStructure.setSizePolicy(sizePolicy)
        self.cmbOrgStructure.setObjectName(_fromUtf8("cmbOrgStructure"))
        self.gridLayout.addWidget(self.cmbOrgStructure, 0, 1, 1, 4)
        self.cmbKind = QtGui.QComboBox(ImportDispPlanQtysDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbKind.sizePolicy().hasHeightForWidth())
        self.cmbKind.setSizePolicy(sizePolicy)
        self.cmbKind.setObjectName(_fromUtf8("cmbKind"))
        self.gridLayout.addWidget(self.cmbKind, 2, 3, 1, 3)
        self.verticalLayout.addLayout(self.gridLayout)
        self.tblPlanQtys = CInDocTableView(ImportDispPlanQtysDialog)
        self.tblPlanQtys.setObjectName(_fromUtf8("tblPlanQtys"))
        self.verticalLayout.addWidget(self.tblPlanQtys)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btnClose = QtGui.QPushButton(ImportDispPlanQtysDialog)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.horizontalLayout_2.addWidget(self.btnClose)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(ImportDispPlanQtysDialog)
        QtCore.QMetaObject.connectSlotsByName(ImportDispPlanQtysDialog)

    def retranslateUi(self, ImportDispPlanQtysDialog):
        ImportDispPlanQtysDialog.setWindowTitle(_translate("ImportDispPlanQtysDialog", "Плановые объемы профилактических мероприятий", None))
        self.label.setText(_translate("ImportDispPlanQtysDialog", "Год:", None))
        self.label_2.setText(_translate("ImportDispPlanQtysDialog", "Подразделение:", None))
        self.label_3.setText(_translate("ImportDispPlanQtysDialog", "Вид осмотра:", None))
        self.btnGetFromService.setText(_translate("ImportDispPlanQtysDialog", "Получить из ТФОМС", None))
        self.btnClose.setText(_translate("ImportDispPlanQtysDialog", "Закрыть", None))

from library.DbComboBox import CDbComboBox
from library.InDocTable import CInDocTableView
