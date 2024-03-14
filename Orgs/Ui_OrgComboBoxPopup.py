# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/natkuch/s11/Orgs/OrgComboBoxPopup.ui'
#
# Created: Fri Sep 21 11:15:33 2018
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_OrgComboBoxPopup(object):
    def setupUi(self, OrgComboBoxPopup):
        OrgComboBoxPopup.setObjectName(_fromUtf8("OrgComboBoxPopup"))
        OrgComboBoxPopup.resize(389, 254)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(OrgComboBoxPopup)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.tabWidget = QtGui.QTabWidget(OrgComboBoxPopup)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.South)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabOrg = QtGui.QWidget()
        self.tabOrg.setObjectName(_fromUtf8("tabOrg"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tabOrg)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setMargin(4)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tblOrg = QtGui.QListView(self.tabOrg)
        self.tblOrg.setResizeMode(QtGui.QListView.Adjust)
        self.tblOrg.setObjectName(_fromUtf8("tblOrg"))
        self.verticalLayout.addWidget(self.tblOrg)
        self.tabWidget.addTab(self.tabOrg, _fromUtf8(""))
        self.tabSearch = QtGui.QWidget()
        self.tabSearch.setObjectName(_fromUtf8("tabSearch"))
        self.gridLayout = QtGui.QGridLayout(self.tabSearch)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(self.tabSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Reset)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 6, 2, 1, 1)
        self.lblName = QtGui.QLabel(self.tabSearch)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 3, 1, 1)
        self.lblOGRN = QtGui.QLabel(self.tabSearch)
        self.lblOGRN.setObjectName(_fromUtf8("lblOGRN"))
        self.gridLayout.addWidget(self.lblOGRN, 3, 0, 1, 1)
        self.edtINN = QtGui.QLineEdit(self.tabSearch)
        self.edtINN.setObjectName(_fromUtf8("edtINN"))
        self.gridLayout.addWidget(self.edtINN, 2, 1, 1, 2)
        self.lblINN = QtGui.QLabel(self.tabSearch)
        self.lblINN.setObjectName(_fromUtf8("lblINN"))
        self.gridLayout.addWidget(self.lblINN, 2, 0, 1, 1)
        self.edtOKATO = QtGui.QLineEdit(self.tabSearch)
        self.edtOKATO.setObjectName(_fromUtf8("edtOKATO"))
        self.gridLayout.addWidget(self.edtOKATO, 4, 1, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(172, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 6, 0, 1, 2)
        self.lblOKATO = QtGui.QLabel(self.tabSearch)
        self.lblOKATO.setObjectName(_fromUtf8("lblOKATO"))
        self.gridLayout.addWidget(self.lblOKATO, 4, 0, 1, 1)
        self.edtName = QtGui.QLineEdit(self.tabSearch)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 1, 1, 1, 2)
        self.edtOGRN = QtGui.QLineEdit(self.tabSearch)
        self.edtOGRN.setObjectName(_fromUtf8("edtOGRN"))
        self.gridLayout.addWidget(self.edtOGRN, 3, 1, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 5, 0, 1, 1)
        self.lblIsHospital = QtGui.QLabel(self.tabSearch)
        self.lblIsHospital.setObjectName(_fromUtf8("lblIsHospital"))
        self.gridLayout.addWidget(self.lblIsHospital, 0, 0, 1, 1)
        self.cmbIsMedical = QtGui.QComboBox(self.tabSearch)
        self.cmbIsMedical.setObjectName(_fromUtf8("cmbIsMedical"))
        self.cmbIsMedical.addItem(_fromUtf8(""))
        self.cmbIsMedical.addItem(_fromUtf8(""))
        self.cmbIsMedical.addItem(_fromUtf8(""))
        self.cmbIsMedical.addItem(_fromUtf8(""))
        self.cmbIsMedical.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cmbIsMedical, 0, 1, 1, 2)
        self.tabWidget.addTab(self.tabSearch, _fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.tabWidget)
        self.lblName.setBuddy(self.edtName)
        self.lblOGRN.setBuddy(self.edtOGRN)
        self.lblINN.setBuddy(self.edtINN)

        self.retranslateUi(OrgComboBoxPopup)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(OrgComboBoxPopup)
        OrgComboBoxPopup.setTabOrder(self.tblOrg, self.tabWidget)
        OrgComboBoxPopup.setTabOrder(self.tabWidget, self.cmbIsMedical)
        OrgComboBoxPopup.setTabOrder(self.cmbIsMedical, self.edtName)
        OrgComboBoxPopup.setTabOrder(self.edtName, self.edtINN)
        OrgComboBoxPopup.setTabOrder(self.edtINN, self.edtOGRN)
        OrgComboBoxPopup.setTabOrder(self.edtOGRN, self.edtOKATO)
        OrgComboBoxPopup.setTabOrder(self.edtOKATO, self.buttonBox)

    def retranslateUi(self, OrgComboBoxPopup):
        OrgComboBoxPopup.setWindowTitle(_translate("OrgComboBoxPopup", "Form", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabOrg), _translate("OrgComboBoxPopup", "&Организации", None))
        self.lblName.setText(_translate("OrgComboBoxPopup", "&Название содержит", None))
        self.lblOGRN.setText(_translate("OrgComboBoxPopup", "&ОГРН", None))
        self.lblINN.setText(_translate("OrgComboBoxPopup", "&ИНН", None))
        self.lblOKATO.setText(_translate("OrgComboBoxPopup", "ОКАТО", None))
        self.lblIsHospital.setText(_translate("OrgComboBoxPopup", "ЛПУ", None))
        self.cmbIsMedical.setItemText(0, _translate("OrgComboBoxPopup", "не определено", None))
        self.cmbIsMedical.setItemText(1, _translate("OrgComboBoxPopup", "поликлиника", None))
        self.cmbIsMedical.setItemText(2, _translate("OrgComboBoxPopup", "стационар", None))
        self.cmbIsMedical.setItemText(3, _translate("OrgComboBoxPopup", "прочая мед.организация", None))
        self.cmbIsMedical.setItemText(4, _translate("OrgComboBoxPopup", "СМП", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSearch), _translate("OrgComboBoxPopup", "&Поиск", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    OrgComboBoxPopup = QtGui.QWidget()
    ui = Ui_OrgComboBoxPopup()
    ui.setupUi(OrgComboBoxPopup)
    OrgComboBoxPopup.show()
    sys.exit(app.exec_())

