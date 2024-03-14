# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RBVaccineEditor.ui'
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

class Ui_RBVaccineEditor(object):
    def setupUi(self, RBVaccineEditor):
        RBVaccineEditor.setObjectName(_fromUtf8("RBVaccineEditor"))
        RBVaccineEditor.resize(457, 389)
        self.gridLayout_4 = QtGui.QGridLayout(RBVaccineEditor)
        self.gridLayout_4.setMargin(4)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.lblCode = QtGui.QLabel(RBVaccineEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCode.sizePolicy().hasHeightForWidth())
        self.lblCode.setSizePolicy(sizePolicy)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout_4.addWidget(self.lblCode, 0, 0, 1, 1)
        self.edtCode = QtGui.QLineEdit(RBVaccineEditor)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout_4.addWidget(self.edtCode, 0, 1, 1, 1)
        self.lblName = QtGui.QLabel(RBVaccineEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblName.sizePolicy().hasHeightForWidth())
        self.lblName.setSizePolicy(sizePolicy)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout_4.addWidget(self.lblName, 1, 0, 1, 1)
        self.edtName = QtGui.QLineEdit(RBVaccineEditor)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout_4.addWidget(self.edtName, 1, 1, 1, 1)
        self.lblRegionalCode = QtGui.QLabel(RBVaccineEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblRegionalCode.sizePolicy().hasHeightForWidth())
        self.lblRegionalCode.setSizePolicy(sizePolicy)
        self.lblRegionalCode.setObjectName(_fromUtf8("lblRegionalCode"))
        self.gridLayout_4.addWidget(self.lblRegionalCode, 2, 0, 1, 1)
        self.edtRegionalCode = QtGui.QLineEdit(RBVaccineEditor)
        self.edtRegionalCode.setObjectName(_fromUtf8("edtRegionalCode"))
        self.gridLayout_4.addWidget(self.edtRegionalCode, 2, 1, 1, 1)
        self.lblDose = QtGui.QLabel(RBVaccineEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDose.sizePolicy().hasHeightForWidth())
        self.lblDose.setSizePolicy(sizePolicy)
        self.lblDose.setObjectName(_fromUtf8("lblDose"))
        self.gridLayout_4.addWidget(self.lblDose, 3, 0, 1, 1)
        self.edtDose = QtGui.QDoubleSpinBox(RBVaccineEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtDose.sizePolicy().hasHeightForWidth())
        self.edtDose.setSizePolicy(sizePolicy)
        self.edtDose.setDecimals(3)
        self.edtDose.setMaximum(100.0)
        self.edtDose.setObjectName(_fromUtf8("edtDose"))
        self.gridLayout_4.addWidget(self.edtDose, 3, 1, 1, 1)
        self.tabWidget = QtGui.QTabWidget(RBVaccineEditor)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabInfections = QtGui.QWidget()
        self.tabInfections.setObjectName(_fromUtf8("tabInfections"))
        self.gridLayout = QtGui.QGridLayout(self.tabInfections)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblVaccineInfections = CInDocTableView(self.tabInfections)
        self.tblVaccineInfections.setObjectName(_fromUtf8("tblVaccineInfections"))
        self.gridLayout.addWidget(self.tblVaccineInfections, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabInfections, _fromUtf8(""))
        self.tabSchemes = QtGui.QWidget()
        self.tabSchemes.setObjectName(_fromUtf8("tabSchemes"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tabSchemes)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.splitter = QtGui.QSplitter(self.tabSchemes)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.tblVaccineSchemes = CInDocTableView(self.splitter)
        self.tblVaccineSchemes.setObjectName(_fromUtf8("tblVaccineSchemes"))
        self.tblVaccineSchemaTransitions = CInDocTableView(self.splitter)
        self.tblVaccineSchemaTransitions.setObjectName(_fromUtf8("tblVaccineSchemaTransitions"))
        self.gridLayout_2.addWidget(self.splitter, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tabSchemes, _fromUtf8(""))
        self.tabIdentification = QtGui.QWidget()
        self.tabIdentification.setObjectName(_fromUtf8("tabIdentification"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tabIdentification)
        self.gridLayout_3.setMargin(4)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.tblVaccineIdentification = CInDocTableView(self.tabIdentification)
        self.tblVaccineIdentification.setObjectName(_fromUtf8("tblVaccineIdentification"))
        self.gridLayout_3.addWidget(self.tblVaccineIdentification, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabIdentification, _fromUtf8(""))
        self.gridLayout_4.addWidget(self.tabWidget, 4, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(RBVaccineEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_4.addWidget(self.buttonBox, 5, 0, 1, 2)
        self.lblCode.setBuddy(self.edtCode)
        self.lblName.setBuddy(self.edtName)
        self.lblRegionalCode.setBuddy(self.edtRegionalCode)
        self.lblDose.setBuddy(self.edtDose)

        self.retranslateUi(RBVaccineEditor)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBVaccineEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBVaccineEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(RBVaccineEditor)
        RBVaccineEditor.setTabOrder(self.edtCode, self.edtName)
        RBVaccineEditor.setTabOrder(self.edtName, self.edtRegionalCode)
        RBVaccineEditor.setTabOrder(self.edtRegionalCode, self.edtDose)
        RBVaccineEditor.setTabOrder(self.edtDose, self.tabWidget)
        RBVaccineEditor.setTabOrder(self.tabWidget, self.tblVaccineInfections)
        RBVaccineEditor.setTabOrder(self.tblVaccineInfections, self.tblVaccineSchemes)
        RBVaccineEditor.setTabOrder(self.tblVaccineSchemes, self.tblVaccineSchemaTransitions)
        RBVaccineEditor.setTabOrder(self.tblVaccineSchemaTransitions, self.tblVaccineIdentification)
        RBVaccineEditor.setTabOrder(self.tblVaccineIdentification, self.buttonBox)

    def retranslateUi(self, RBVaccineEditor):
        RBVaccineEditor.setWindowTitle(_translate("RBVaccineEditor", "Dialog", None))
        self.lblCode.setText(_translate("RBVaccineEditor", "&Код", None))
        self.lblName.setText(_translate("RBVaccineEditor", "&Наименование", None))
        self.lblRegionalCode.setText(_translate("RBVaccineEditor", "&Региональный код", None))
        self.lblDose.setText(_translate("RBVaccineEditor", "&Доза", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabInfections), _translate("RBVaccineEditor", "&Инфекции", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSchemes), _translate("RBVaccineEditor", "&Схемы и переходы", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabIdentification), _translate("RBVaccineEditor", "Идентификация", None))

from library.InDocTable import CInDocTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RBVaccineEditor = QtGui.QDialog()
    ui = Ui_RBVaccineEditor()
    ui.setupUi(RBVaccineEditor)
    RBVaccineEditor.show()
    sys.exit(app.exec_())

