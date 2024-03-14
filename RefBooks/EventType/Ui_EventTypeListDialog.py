# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Rabota\s11\RefBooks\EventType\EventTypeListDialog.ui'
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

class Ui_EventTypeListDialog(object):
    def setupUi(self, EventTypeListDialog):
        EventTypeListDialog.setObjectName(_fromUtf8("EventTypeListDialog"))
        EventTypeListDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        EventTypeListDialog.resize(689, 450)
        EventTypeListDialog.setSizeGripEnabled(True)
        EventTypeListDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(EventTypeListDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tblItems = CTableView(EventTypeListDialog)
        self.tblItems.setTabKeyNavigation(False)
        self.tblItems.setAlternatingRowColors(True)
        self.tblItems.setObjectName(_fromUtf8("tblItems"))
        self.gridLayout.addWidget(self.tblItems, 0, 0, 1, 2)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.label = QtGui.QLabel(EventTypeListDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.hboxlayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.hboxlayout, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(EventTypeListDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)
        self.statusBar = QtGui.QStatusBar(EventTypeListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusBar.sizePolicy().hasHeightForWidth())
        self.statusBar.setSizePolicy(sizePolicy)
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        self.gridLayout.addWidget(self.statusBar, 3, 0, 1, 2)
        self.chkFilterActive = QtGui.QCheckBox(EventTypeListDialog)
        self.chkFilterActive.setObjectName(_fromUtf8("chkFilterActive"))
        self.gridLayout.addWidget(self.chkFilterActive, 1, 0, 1, 2)

        self.retranslateUi(EventTypeListDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), EventTypeListDialog.close)
        QtCore.QMetaObject.connectSlotsByName(EventTypeListDialog)
        EventTypeListDialog.setTabOrder(self.tblItems, self.chkFilterActive)
        EventTypeListDialog.setTabOrder(self.chkFilterActive, self.buttonBox)

    def retranslateUi(self, EventTypeListDialog):
        EventTypeListDialog.setWindowTitle(_translate("EventTypeListDialog", "Список записей", None))
        self.tblItems.setWhatsThis(_translate("EventTypeListDialog", "список записей", "ура!"))
        self.label.setText(_translate("EventTypeListDialog", "всего: ", None))
        self.statusBar.setToolTip(_translate("EventTypeListDialog", "A status bar", None))
        self.statusBar.setWhatsThis(_translate("EventTypeListDialog", "A status bar.", None))
        self.chkFilterActive.setText(_translate("EventTypeListDialog", "Отображать не активные типы событий", None))

from library.TableView import CTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    EventTypeListDialog = QtGui.QDialog()
    ui = Ui_EventTypeListDialog()
    ui.setupUi(EventTypeListDialog)
    EventTypeListDialog.show()
    sys.exit(app.exec_())

