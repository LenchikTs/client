# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/RefBooks/RBMedicalExemptionTypeItemList.ui'
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

class Ui_RBMedicalExemptionTypeItemList(object):
    def setupUi(self, RBMedicalExemptionTypeItemList):
        RBMedicalExemptionTypeItemList.setObjectName(_fromUtf8("RBMedicalExemptionTypeItemList"))
        RBMedicalExemptionTypeItemList.resize(337, 249)
        self.gridLayout = QtGui.QGridLayout(RBMedicalExemptionTypeItemList)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(RBMedicalExemptionTypeItemList)
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
        self.widget_2 = QtGui.QWidget(self.splitter)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tblMedicalExemptionTypeInfections = CTableView(self.widget_2)
        self.tblMedicalExemptionTypeInfections.setObjectName(_fromUtf8("tblMedicalExemptionTypeInfections"))
        self.verticalLayout_2.addWidget(self.tblMedicalExemptionTypeInfections)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 2)
        self.label = QtGui.QLabel(RBMedicalExemptionTypeItemList)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RBMedicalExemptionTypeItemList)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 1, 1, 1)

        self.retranslateUi(RBMedicalExemptionTypeItemList)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBMedicalExemptionTypeItemList.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBMedicalExemptionTypeItemList.reject)
        QtCore.QMetaObject.connectSlotsByName(RBMedicalExemptionTypeItemList)

    def retranslateUi(self, RBMedicalExemptionTypeItemList):
        RBMedicalExemptionTypeItemList.setWindowTitle(_translate("RBMedicalExemptionTypeItemList", "Dialog", None))
        self.label.setText(_translate("RBMedicalExemptionTypeItemList", "Всего", None))

from library.TableView import CTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RBMedicalExemptionTypeItemList = QtGui.QDialog()
    ui = Ui_RBMedicalExemptionTypeItemList()
    ui.setupUi(RBMedicalExemptionTypeItemList)
    RBMedicalExemptionTypeItemList.show()
    sys.exit(app.exec_())

