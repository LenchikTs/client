# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RBPrintTemplateListDialog.ui'
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

class Ui_RBPrintTemplateListDialog(object):
    def setupUi(self, RBPrintTemplateListDialog):
        RBPrintTemplateListDialog.setObjectName(_fromUtf8("RBPrintTemplateListDialog"))
        RBPrintTemplateListDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        RBPrintTemplateListDialog.resize(689, 450)
        RBPrintTemplateListDialog.setSizeGripEnabled(True)
        RBPrintTemplateListDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(RBPrintTemplateListDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.edtCodeFilter = QtGui.QLineEdit(RBPrintTemplateListDialog)
        self.edtCodeFilter.setObjectName(_fromUtf8("edtCodeFilter"))
        self.gridLayout.addWidget(self.edtCodeFilter, 0, 3, 1, 1)
        self.lblNameFilter = QtGui.QLabel(RBPrintTemplateListDialog)
        self.lblNameFilter.setObjectName(_fromUtf8("lblNameFilter"))
        self.gridLayout.addWidget(self.lblNameFilter, 0, 4, 1, 1)
        self.edtNameFilter = QtGui.QLineEdit(RBPrintTemplateListDialog)
        self.edtNameFilter.setObjectName(_fromUtf8("edtNameFilter"))
        self.gridLayout.addWidget(self.edtNameFilter, 0, 5, 1, 1)
        self.lblCodeFilter = QtGui.QLabel(RBPrintTemplateListDialog)
        self.lblCodeFilter.setObjectName(_fromUtf8("lblCodeFilter"))
        self.gridLayout.addWidget(self.lblCodeFilter, 0, 2, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(RBPrintTemplateListDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 4, 1, 3)
        self.edtContextFilter = QtGui.QLineEdit(RBPrintTemplateListDialog)
        self.edtContextFilter.setObjectName(_fromUtf8("edtContextFilter"))
        self.gridLayout.addWidget(self.edtContextFilter, 0, 1, 1, 1)
        self.tblItems = CSortFilterProxyTableView(RBPrintTemplateListDialog)
        self.tblItems.setTabKeyNavigation(False)
        self.tblItems.setAlternatingRowColors(True)
        self.tblItems.setObjectName(_fromUtf8("tblItems"))
        self.gridLayout.addWidget(self.tblItems, 1, 0, 1, 7)
        self.lblContextFilter = QtGui.QLabel(RBPrintTemplateListDialog)
        self.lblContextFilter.setObjectName(_fromUtf8("lblContextFilter"))
        self.gridLayout.addWidget(self.lblContextFilter, 0, 0, 1, 1)
        self.statusBar = QtGui.QStatusBar(RBPrintTemplateListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusBar.sizePolicy().hasHeightForWidth())
        self.statusBar.setSizePolicy(sizePolicy)
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        self.gridLayout.addWidget(self.statusBar, 3, 0, 1, 4)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.label = QtGui.QLabel(RBPrintTemplateListDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.hboxlayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.hboxlayout, 2, 0, 1, 4)

        self.retranslateUi(RBPrintTemplateListDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), RBPrintTemplateListDialog.close)
        QtCore.QMetaObject.connectSlotsByName(RBPrintTemplateListDialog)
        RBPrintTemplateListDialog.setTabOrder(self.tblItems, self.edtCodeFilter)
        RBPrintTemplateListDialog.setTabOrder(self.edtCodeFilter, self.edtNameFilter)
        RBPrintTemplateListDialog.setTabOrder(self.edtNameFilter, self.buttonBox)

    def retranslateUi(self, RBPrintTemplateListDialog):
        RBPrintTemplateListDialog.setWindowTitle(_translate("RBPrintTemplateListDialog", "Список записей", None))
        self.lblNameFilter.setText(_translate("RBPrintTemplateListDialog", "Наименование", None))
        self.lblCodeFilter.setText(_translate("RBPrintTemplateListDialog", "Код", None))
        self.tblItems.setWhatsThis(_translate("RBPrintTemplateListDialog", "список записей", "ура!"))
        self.lblContextFilter.setText(_translate("RBPrintTemplateListDialog", "Контекст", None))
        self.statusBar.setToolTip(_translate("RBPrintTemplateListDialog", "A status bar", None))
        self.statusBar.setWhatsThis(_translate("RBPrintTemplateListDialog", "A status bar.", None))
        self.label.setText(_translate("RBPrintTemplateListDialog", "всего: ", None))

from library.SortFilterProxyTableView import CSortFilterProxyTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RBPrintTemplateListDialog = QtGui.QDialog()
    ui = Ui_RBPrintTemplateListDialog()
    ui.setupUi(RBPrintTemplateListDialog)
    RBPrintTemplateListDialog.show()
    sys.exit(app.exec_())

