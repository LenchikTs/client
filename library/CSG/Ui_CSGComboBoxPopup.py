# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\library\CSG\CSGComboBoxPopup.ui'
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

class Ui_CSGComboBoxPopup(object):
    def setupUi(self, CSGComboBoxPopup):
        CSGComboBoxPopup.setObjectName(_fromUtf8("CSGComboBoxPopup"))
        CSGComboBoxPopup.resize(545, 214)
        self.gridlayout = QtGui.QGridLayout(CSGComboBoxPopup)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(0)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.tabWidget = QtGui.QTabWidget(CSGComboBoxPopup)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.South)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabCSG = QtGui.QWidget()
        self.tabCSG.setObjectName(_fromUtf8("tabCSG"))
        self.vboxlayout = QtGui.QVBoxLayout(self.tabCSG)
        self.vboxlayout.setMargin(4)
        self.vboxlayout.setSpacing(4)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.tblCSG = CTableView(self.tabCSG)
        self.tblCSG.setObjectName(_fromUtf8("tblCSG"))
        self.vboxlayout.addWidget(self.tblCSG)
        self.tabWidget.addTab(self.tabCSG, _fromUtf8(""))
        self.tabSearch = QtGui.QWidget()
        self.tabSearch.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabSearch.setObjectName(_fromUtf8("tabSearch"))
        self.gridlayout1 = QtGui.QGridLayout(self.tabSearch)
        self.gridlayout1.setMargin(4)
        self.gridlayout1.setSpacing(4)
        self.gridlayout1.setObjectName(_fromUtf8("gridlayout1"))
        self.lblMKB = QtGui.QLabel(self.tabSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblMKB.sizePolicy().hasHeightForWidth())
        self.lblMKB.setSizePolicy(sizePolicy)
        self.lblMKB.setObjectName(_fromUtf8("lblMKB"))
        self.gridlayout1.addWidget(self.lblMKB, 3, 0, 1, 1)
        self.chkSex = QtGui.QCheckBox(self.tabSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkSex.sizePolicy().hasHeightForWidth())
        self.chkSex.setSizePolicy(sizePolicy)
        self.chkSex.setChecked(True)
        self.chkSex.setObjectName(_fromUtf8("chkSex"))
        self.gridlayout1.addWidget(self.chkSex, 0, 0, 1, 2)
        self.chkAge = QtGui.QCheckBox(self.tabSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkAge.sizePolicy().hasHeightForWidth())
        self.chkAge.setSizePolicy(sizePolicy)
        self.chkAge.setChecked(True)
        self.chkAge.setObjectName(_fromUtf8("chkAge"))
        self.gridlayout1.addWidget(self.chkAge, 1, 0, 1, 2)
        self.chkCsgServices = QtGui.QCheckBox(self.tabSearch)
        self.chkCsgServices.setChecked(True)
        self.chkCsgServices.setObjectName(_fromUtf8("chkCsgServices"))
        self.gridlayout1.addWidget(self.chkCsgServices, 2, 0, 1, 2)
        self.cmbMKB = QtGui.QComboBox(self.tabSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbMKB.sizePolicy().hasHeightForWidth())
        self.cmbMKB.setSizePolicy(sizePolicy)
        self.cmbMKB.setObjectName(_fromUtf8("cmbMKB"))
        self.cmbMKB.addItem(_fromUtf8(""))
        self.cmbMKB.addItem(_fromUtf8(""))
        self.cmbMKB.addItem(_fromUtf8(""))
        self.gridlayout1.addWidget(self.cmbMKB, 3, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem, 6, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(self.tabSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Reset)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout1.addWidget(self.buttonBox, 6, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem1, 5, 0, 1, 3)
        self.lblEventProfile = QtGui.QLabel(self.tabSearch)
        self.lblEventProfile.setObjectName(_fromUtf8("lblEventProfile"))
        self.gridlayout1.addWidget(self.lblEventProfile, 4, 0, 1, 1)
        self.cmbEventProfile = QtGui.QComboBox(self.tabSearch)
        self.cmbEventProfile.setObjectName(_fromUtf8("cmbEventProfile"))
        self.cmbEventProfile.addItem(_fromUtf8(""))
        self.cmbEventProfile.addItem(_fromUtf8(""))
        self.gridlayout1.addWidget(self.cmbEventProfile, 4, 1, 1, 1)
        self.tabWidget.addTab(self.tabSearch, _fromUtf8(""))
        self.gridlayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(CSGComboBoxPopup)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(CSGComboBoxPopup)
        CSGComboBoxPopup.setTabOrder(self.buttonBox, self.tblCSG)

    def retranslateUi(self, CSGComboBoxPopup):
        CSGComboBoxPopup.setWindowTitle(_translate("CSGComboBoxPopup", "Form", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabCSG), _translate("CSGComboBoxPopup", "&Номенклатура", None))
        self.lblMKB.setText(_translate("CSGComboBoxPopup", "Диагноз", None))
        self.chkSex.setText(_translate("CSGComboBoxPopup", "Учитывать пол пациента", None))
        self.chkAge.setText(_translate("CSGComboBoxPopup", "Учитывать возраст пациента", None))
        self.chkCsgServices.setText(_translate("CSGComboBoxPopup", "Учитывать номенклатурные услуги", None))
        self.cmbMKB.setItemText(0, _translate("CSGComboBoxPopup", "не учитывать", None))
        self.cmbMKB.setItemText(1, _translate("CSGComboBoxPopup", "соответствие по рубрике", None))
        self.cmbMKB.setItemText(2, _translate("CSGComboBoxPopup", "строгое соответствие", None))
        self.lblEventProfile.setText(_translate("CSGComboBoxPopup", "Профили событий", None))
        self.cmbEventProfile.setItemText(0, _translate("CSGComboBoxPopup", "не учитывать", None))
        self.cmbEventProfile.setItemText(1, _translate("CSGComboBoxPopup", "строгое соответствие", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSearch), _translate("CSGComboBoxPopup", "&Поиск", None))

from library.TableView import CTableView
