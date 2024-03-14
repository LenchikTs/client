# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\F003\MenuDialog.ui'
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

class Ui_MenuDialog(object):
    def setupUi(self, MenuDialog):
        MenuDialog.setObjectName(_fromUtf8("MenuDialog"))
        MenuDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        MenuDialog.resize(844, 527)
        MenuDialog.setSizeGripEnabled(True)
        MenuDialog.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(MenuDialog)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lblPeriod = QtGui.QLabel(MenuDialog)
        self.lblPeriod.setObjectName(_fromUtf8("lblPeriod"))
        self.horizontalLayout.addWidget(self.lblPeriod)
        self.edtBegDate = CDateEdit(MenuDialog)
        self.edtBegDate.setObjectName(_fromUtf8("edtBegDate"))
        self.horizontalLayout.addWidget(self.edtBegDate)
        self.lblFor = QtGui.QLabel(MenuDialog)
        self.lblFor.setAlignment(QtCore.Qt.AlignCenter)
        self.lblFor.setObjectName(_fromUtf8("lblFor"))
        self.horizontalLayout.addWidget(self.lblFor)
        self.edtEndDate = CDateEdit(MenuDialog)
        self.edtEndDate.setObjectName(_fromUtf8("edtEndDate"))
        self.horizontalLayout.addWidget(self.edtEndDate)
        self.lblFeaturesToEat = QtGui.QLabel(MenuDialog)
        self.lblFeaturesToEat.setObjectName(_fromUtf8("lblFeaturesToEat"))
        self.horizontalLayout.addWidget(self.lblFeaturesToEat)
        self.edtFeaturesToEat = QtGui.QLineEdit(MenuDialog)
        self.edtFeaturesToEat.setObjectName(_fromUtf8("edtFeaturesToEat"))
        self.horizontalLayout.addWidget(self.edtFeaturesToEat)
        self.label_2 = QtGui.QLabel(MenuDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.cmbFinance = CRBComboBox(MenuDialog)
        self.cmbFinance.setMinimumSize(QtCore.QSize(140, 0))
        self.cmbFinance.setObjectName(_fromUtf8("cmbFinance"))
        self.horizontalLayout.addWidget(self.cmbFinance)
        self.chkRefusalToEat = QtGui.QCheckBox(MenuDialog)
        self.chkRefusalToEat.setObjectName(_fromUtf8("chkRefusalToEat"))
        self.horizontalLayout.addWidget(self.chkRefusalToEat)
        self.chkUpdate = QtGui.QCheckBox(MenuDialog)
        self.chkUpdate.setObjectName(_fromUtf8("chkUpdate"))
        self.horizontalLayout.addWidget(self.chkUpdate)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tblItems = CTableView(MenuDialog)
        self.tblItems.setTabKeyNavigation(False)
        self.tblItems.setAlternatingRowColors(True)
        self.tblItems.setObjectName(_fromUtf8("tblItems"))
        self.verticalLayout.addWidget(self.tblItems)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(4)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.label = QtGui.QLabel(MenuDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.hboxlayout.addWidget(self.label)
        self.statusBar = QtGui.QStatusBar(MenuDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusBar.sizePolicy().hasHeightForWidth())
        self.statusBar.setSizePolicy(sizePolicy)
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        self.hboxlayout.addWidget(self.statusBar)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.btnSelected = QtGui.QPushButton(MenuDialog)
        self.btnSelected.setObjectName(_fromUtf8("btnSelected"))
        self.hboxlayout.addWidget(self.btnSelected)
        self.btnEdit = QtGui.QPushButton(MenuDialog)
        self.btnEdit.setDefault(True)
        self.btnEdit.setObjectName(_fromUtf8("btnEdit"))
        self.hboxlayout.addWidget(self.btnEdit)
        self.btnPrint = QtGui.QPushButton(MenuDialog)
        self.btnPrint.setObjectName(_fromUtf8("btnPrint"))
        self.hboxlayout.addWidget(self.btnPrint)
        self.btnCancel = QtGui.QPushButton(MenuDialog)
        self.btnCancel.setObjectName(_fromUtf8("btnCancel"))
        self.hboxlayout.addWidget(self.btnCancel)
        self.verticalLayout.addLayout(self.hboxlayout)
        self.lblPeriod.setBuddy(self.edtBegDate)
        self.lblFor.setBuddy(self.edtEndDate)
        self.lblFeaturesToEat.setBuddy(self.edtFeaturesToEat)
        self.label_2.setBuddy(self.cmbFinance)

        self.retranslateUi(MenuDialog)
        QtCore.QObject.connect(self.btnCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), MenuDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(MenuDialog)
        MenuDialog.setTabOrder(self.edtBegDate, self.edtEndDate)
        MenuDialog.setTabOrder(self.edtEndDate, self.edtFeaturesToEat)
        MenuDialog.setTabOrder(self.edtFeaturesToEat, self.cmbFinance)
        MenuDialog.setTabOrder(self.cmbFinance, self.chkRefusalToEat)
        MenuDialog.setTabOrder(self.chkRefusalToEat, self.chkUpdate)
        MenuDialog.setTabOrder(self.chkUpdate, self.tblItems)
        MenuDialog.setTabOrder(self.tblItems, self.btnSelected)
        MenuDialog.setTabOrder(self.btnSelected, self.btnEdit)
        MenuDialog.setTabOrder(self.btnEdit, self.btnPrint)
        MenuDialog.setTabOrder(self.btnPrint, self.btnCancel)

    def retranslateUi(self, MenuDialog):
        MenuDialog.setWindowTitle(_translate("MenuDialog", "Список записей", None))
        self.lblPeriod.setText(_translate("MenuDialog", "Период с", None))
        self.edtBegDate.setDisplayFormat(_translate("MenuDialog", "dd.MM.yyyy", None))
        self.lblFor.setText(_translate("MenuDialog", "по", None))
        self.edtEndDate.setDisplayFormat(_translate("MenuDialog", "dd.MM.yyyy", None))
        self.lblFeaturesToEat.setText(_translate("MenuDialog", "Особенности", None))
        self.label_2.setText(_translate("MenuDialog", "Финансирование", None))
        self.chkRefusalToEat.setText(_translate("MenuDialog", "Отказ", None))
        self.chkUpdate.setText(_translate("MenuDialog", "Обновить", None))
        self.tblItems.setWhatsThis(_translate("MenuDialog", "список записей", "ура!"))
        self.label.setText(_translate("MenuDialog", "всего: ", None))
        self.statusBar.setToolTip(_translate("MenuDialog", "A status bar", None))
        self.statusBar.setWhatsThis(_translate("MenuDialog", "A status bar.", None))
        self.btnSelected.setText(_translate("MenuDialog", "Выбрать", None))
        self.btnEdit.setWhatsThis(_translate("MenuDialog", "изменить текущую запись", None))
        self.btnEdit.setText(_translate("MenuDialog", "Просмотр", None))
        self.btnEdit.setShortcut(_translate("MenuDialog", "F4", None))
        self.btnPrint.setText(_translate("MenuDialog", "Печать", None))
        self.btnCancel.setWhatsThis(_translate("MenuDialog", "выйти из списка без выбора", None))
        self.btnCancel.setText(_translate("MenuDialog", "Закрыть", None))

from library.DateEdit import CDateEdit
from library.TableView import CTableView
from library.crbcombobox import CRBComboBox
