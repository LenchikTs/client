# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/RefBooks/PlanningHealthResortActivity/RBPlanningHealthResortActivity.ui'
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

class Ui_RBPlanningHealthResortActivity(object):
    def setupUi(self, RBPlanningHealthResortActivity):
        RBPlanningHealthResortActivity.setObjectName(_fromUtf8("RBPlanningHealthResortActivity"))
        RBPlanningHealthResortActivity.resize(782, 502)
        self.gridLayout = QtGui.QGridLayout(RBPlanningHealthResortActivity)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(RBPlanningHealthResortActivity)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabDistrict = QtGui.QWidget()
        self.tabDistrict.setObjectName(_fromUtf8("tabDistrict"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tabDistrict)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lblYear = QtGui.QLabel(self.tabDistrict)
        self.lblYear.setObjectName(_fromUtf8("lblYear"))
        self.gridLayout_2.addWidget(self.lblYear, 0, 0, 1, 1)
        self.edtYear = QtGui.QDateEdit(self.tabDistrict)
        self.edtYear.setEnabled(True)
        self.edtYear.setObjectName(_fromUtf8("edtYear"))
        self.gridLayout_2.addWidget(self.edtYear, 0, 1, 1, 1)
        self.lblRegion = QtGui.QLabel(self.tabDistrict)
        self.lblRegion.setObjectName(_fromUtf8("lblRegion"))
        self.gridLayout_2.addWidget(self.lblRegion, 1, 0, 1, 1)
        self.btnFillDistricts = QtGui.QPushButton(self.tabDistrict)
        self.btnFillDistricts.setObjectName(_fromUtf8("btnFillDistricts"))
        self.gridLayout_2.addWidget(self.btnFillDistricts, 1, 3, 1, 1)
        self.cmbRegion = CMainRegionsKLADRComboBox(self.tabDistrict)
        self.cmbRegion.setObjectName(_fromUtf8("cmbRegion"))
        self.gridLayout_2.addWidget(self.cmbRegion, 1, 1, 1, 2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 4, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 2, 1, 3)
        self.tblPlan = CInDocTableViewTabMod(self.tabDistrict)
        self.tblPlan.setObjectName(_fromUtf8("tblPlan"))
        self.gridLayout_2.addWidget(self.tblPlan, 3, 0, 1, 5)
        self.tabWidget.addTab(self.tabDistrict, _fromUtf8(""))
        self.tabOrgStructure = QtGui.QWidget()
        self.tabOrgStructure.setObjectName(_fromUtf8("tabOrgStructure"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tabOrgStructure)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.tabWidget.addTab(self.tabOrgStructure, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 2)
        self.lblCount = QtGui.QLabel(RBPlanningHealthResortActivity)
        self.lblCount.setObjectName(_fromUtf8("lblCount"))
        self.gridLayout.addWidget(self.lblCount, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RBPlanningHealthResortActivity)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 1, 1, 1)

        self.retranslateUi(RBPlanningHealthResortActivity)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBPlanningHealthResortActivity.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBPlanningHealthResortActivity.reject)
        QtCore.QMetaObject.connectSlotsByName(RBPlanningHealthResortActivity)

    def retranslateUi(self, RBPlanningHealthResortActivity):
        RBPlanningHealthResortActivity.setWindowTitle(_translate("RBPlanningHealthResortActivity", "Планирование санаторной деятельности", None))
        self.lblYear.setText(_translate("RBPlanningHealthResortActivity", "Год", None))
        self.edtYear.setDisplayFormat(_translate("RBPlanningHealthResortActivity", "yyyy", None))
        self.lblRegion.setText(_translate("RBPlanningHealthResortActivity", "Регион", None))
        self.btnFillDistricts.setText(_translate("RBPlanningHealthResortActivity", "Сгенерировать", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabDistrict), _translate("RBPlanningHealthResortActivity", "Планирование по районам", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabOrgStructure), _translate("RBPlanningHealthResortActivity", "Планирование по отделениям", None))
        self.lblCount.setText(_translate("RBPlanningHealthResortActivity", "Список пуст", None))

from KLADR.kladrComboxes import CMainRegionsKLADRComboBox
from RefBooks.Utils import CInDocTableViewTabMod

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RBPlanningHealthResortActivity = QtGui.QDialog()
    ui = Ui_RBPlanningHealthResortActivity()
    ui.setupUi(RBPlanningHealthResortActivity)
    RBPlanningHealthResortActivity.show()
    sys.exit(app.exec_())

