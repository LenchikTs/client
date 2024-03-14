# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\temp1\Exchange\ImportNSI_Wizard_2.ui'
#
# Created: Sun Nov 30 15:21:35 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ImportNSI_Wizard_2(object):
    def setupUi(self, ImportNSI_Wizard_2):
        ImportNSI_Wizard_2.setObjectName("ImportNSI_Wizard_2")
        ImportNSI_Wizard_2.setWindowModality(QtCore.Qt.NonModal)
        ImportNSI_Wizard_2.resize(593, 450)
        self.gridlayout = QtGui.QGridLayout(ImportNSI_Wizard_2)
        self.gridlayout.setMargin(4)
        self.gridlayout.setSpacing(4)
        self.gridlayout.setObjectName("gridlayout")
        self.splitterTree = QtGui.QSplitter(ImportNSI_Wizard_2)
        self.splitterTree.setOrientation(QtCore.Qt.Horizontal)
        self.splitterTree.setObjectName("splitterTree")
        self.tblEvents = QtGui.QTableWidget(self.splitterTree)
        self.tblEvents.setObjectName("tblEvents")
        self.tblEvents.setColumnCount(0)
        self.tblEvents.setRowCount(0)
        self.gridlayout.addWidget(self.splitterTree, 2, 0, 1, 1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.btnClearSelection = QtGui.QPushButton(ImportNSI_Wizard_2)
        self.btnClearSelection.setObjectName("btnClearSelection")
        self.hboxlayout.addWidget(self.btnClearSelection)
        self.gridlayout.addLayout(self.hboxlayout, 3, 0, 1, 1)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")
        self.chkImportAll = QtGui.QCheckBox(ImportNSI_Wizard_2)
        self.chkImportAll.setObjectName("chkImportAll")
        self.hboxlayout1.addWidget(self.chkImportAll)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem1)
        self.gridlayout.addLayout(self.hboxlayout1, 0, 0, 1, 1)
        self.statusLabel = QtGui.QLabel(ImportNSI_Wizard_2)
        self.statusLabel.setObjectName("statusLabel")
        self.gridlayout.addWidget(self.statusLabel, 4, 0, 1, 1)

        self.retranslateUi(ImportNSI_Wizard_2)
        QtCore.QMetaObject.connectSlotsByName(ImportNSI_Wizard_2)

    def retranslateUi(self, ImportNSI_Wizard_2):
        ImportNSI_Wizard_2.setWindowTitle(QtGui.QApplication.translate("ImportNSI_Wizard_2", "Список справочников", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClearSelection.setText(QtGui.QApplication.translate("ImportNSI_Wizard_2", "Очистить", None, QtGui.QApplication.UnicodeUTF8))
        self.chkImportAll.setText(QtGui.QApplication.translate("ImportNSI_Wizard_2", "Загружать всё", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ImportNSI_Wizard_2 = QtGui.QDialog()
    ui = Ui_ImportNSI_Wizard_2()
    ui.setupUi(ImportNSI_Wizard_2)
    ImportNSI_Wizard_2.show()
    sys.exit(app.exec_())

