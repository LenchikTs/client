# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RBInfectionItemList.ui'
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

class Ui_RBInfectionItemList(object):
    def setupUi(self, RBInfectionItemList):
        RBInfectionItemList.setObjectName(_fromUtf8("RBInfectionItemList"))
        RBInfectionItemList.resize(569, 488)
        self.gridLayout = QtGui.QGridLayout(RBInfectionItemList)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(RBInfectionItemList)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.pnlItems = QtGui.QWidget(self.splitter)
        self.pnlItems.setObjectName(_fromUtf8("pnlItems"))
        self.verticalLayout = QtGui.QVBoxLayout(self.pnlItems)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tblItems = CTableView(self.pnlItems)
        self.tblItems.setObjectName(_fromUtf8("tblItems"))
        self.verticalLayout.addWidget(self.tblItems)
        self.pnlVaccines = QtGui.QWidget(self.splitter)
        self.pnlVaccines.setObjectName(_fromUtf8("pnlVaccines"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.pnlVaccines)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tblInfectionVaccines = CTableView(self.pnlVaccines)
        self.tblInfectionVaccines.setObjectName(_fromUtf8("tblInfectionVaccines"))
        self.verticalLayout_2.addWidget(self.tblInfectionVaccines)
        self.pnlMinimumTerms = QtGui.QWidget(self.splitter)
        self.pnlMinimumTerms.setObjectName(_fromUtf8("pnlMinimumTerms"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.pnlMinimumTerms)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.tblInfectionMinimumTerms = CTableView(self.pnlMinimumTerms)
        self.tblInfectionMinimumTerms.setObjectName(_fromUtf8("tblInfectionMinimumTerms"))
        self.verticalLayout_3.addWidget(self.tblInfectionMinimumTerms)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 2)
        self.label = QtGui.QLabel(RBInfectionItemList)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RBInfectionItemList)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 1, 1, 1)

        self.retranslateUi(RBInfectionItemList)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBInfectionItemList.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBInfectionItemList.reject)
        QtCore.QMetaObject.connectSlotsByName(RBInfectionItemList)
        RBInfectionItemList.setTabOrder(self.tblItems, self.tblInfectionVaccines)
        RBInfectionItemList.setTabOrder(self.tblInfectionVaccines, self.tblInfectionMinimumTerms)
        RBInfectionItemList.setTabOrder(self.tblInfectionMinimumTerms, self.buttonBox)

    def retranslateUi(self, RBInfectionItemList):
        RBInfectionItemList.setWindowTitle(_translate("RBInfectionItemList", "Dialog", None))
        self.label.setText(_translate("RBInfectionItemList", "Всего", None))

from library.TableView import CTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RBInfectionItemList = QtGui.QDialog()
    ui = Ui_RBInfectionItemList()
    ui.setupUi(RBInfectionItemList)
    RBInfectionItemList.show()
    sys.exit(app.exec_())

