# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Rabota\s11\RefBooks\ReactionManifestation\RBReactionManifestationEditor.ui'
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

class Ui_RBReactionManifestationEditor(object):
    def setupUi(self, RBReactionManifestationEditor):
        RBReactionManifestationEditor.setObjectName(_fromUtf8("RBReactionManifestationEditor"))
        RBReactionManifestationEditor.resize(390, 234)
        RBReactionManifestationEditor.setSizeGripEnabled(True)
        self.gridLayout_2 = QtGui.QGridLayout(RBReactionManifestationEditor)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setSpacing(4)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tabWidget = QtGui.QTabWidget(RBReactionManifestationEditor)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabMain = QtGui.QWidget()
        self.tabMain.setObjectName(_fromUtf8("tabMain"))
        self.gridLayout = QtGui.QGridLayout(self.tabMain)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtName = QtGui.QLineEdit(self.tabMain)
        self.edtName.setObjectName(_fromUtf8("edtName"))
        self.gridLayout.addWidget(self.edtName, 1, 1, 1, 2)
        self.lblName = QtGui.QLabel(self.tabMain)
        self.lblName.setObjectName(_fromUtf8("lblName"))
        self.gridLayout.addWidget(self.lblName, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 120, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.lblCode = QtGui.QLabel(self.tabMain)
        self.lblCode.setObjectName(_fromUtf8("lblCode"))
        self.gridLayout.addWidget(self.lblCode, 0, 0, 1, 1)
        self.edtCode = QtGui.QLineEdit(self.tabMain)
        self.edtCode.setObjectName(_fromUtf8("edtCode"))
        self.gridLayout.addWidget(self.edtCode, 0, 1, 1, 2)
        self.tabWidget.addTab(self.tabMain, _fromUtf8(""))
        self.tabIdentification = QtGui.QWidget()
        self.tabIdentification.setObjectName(_fromUtf8("tabIdentification"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tabIdentification)
        self.gridLayout_3.setMargin(4)
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.tblIdentification = CInDocTableView(self.tabIdentification)
        self.tblIdentification.setObjectName(_fromUtf8("tblIdentification"))
        self.gridLayout_3.addWidget(self.tblIdentification, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabIdentification, _fromUtf8(""))
        self.gridLayout_2.addWidget(self.tabWidget, 2, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(RBReactionManifestationEditor)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_2.addWidget(self.buttonBox, 3, 0, 1, 2)
        self.lblName.setBuddy(self.edtName)
        self.lblCode.setBuddy(self.edtCode)

        self.retranslateUi(RBReactionManifestationEditor)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), RBReactionManifestationEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBReactionManifestationEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(RBReactionManifestationEditor)
        RBReactionManifestationEditor.setTabOrder(self.tabWidget, self.edtCode)
        RBReactionManifestationEditor.setTabOrder(self.edtCode, self.edtName)
        RBReactionManifestationEditor.setTabOrder(self.edtName, self.tblIdentification)
        RBReactionManifestationEditor.setTabOrder(self.tblIdentification, self.buttonBox)

    def retranslateUi(self, RBReactionManifestationEditor):
        RBReactionManifestationEditor.setWindowTitle(_translate("RBReactionManifestationEditor", "Dialog", None))
        self.lblName.setText(_translate("RBReactionManifestationEditor", "&Наименование", None))
        self.lblCode.setText(_translate("RBReactionManifestationEditor", "&Код", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMain), _translate("RBReactionManifestationEditor", "&Основная информация", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabIdentification), _translate("RBReactionManifestationEditor", "&Идентификация", None))

from library.InDocTable import CInDocTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RBReactionManifestationEditor = QtGui.QDialog()
    ui = Ui_RBReactionManifestationEditor()
    ui.setupUi(RBReactionManifestationEditor)
    RBReactionManifestationEditor.show()
    sys.exit(app.exec_())

