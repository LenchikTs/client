# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/dmitrii/s11/Notifications/NotificationLogListDialog.ui'
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

class Ui_NotificationLogListDialog(object):
    def setupUi(self, NotificationLogListDialog):
        NotificationLogListDialog.setObjectName(_fromUtf8("NotificationLogListDialog"))
        NotificationLogListDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        NotificationLogListDialog.resize(688, 573)
        NotificationLogListDialog.setSizeGripEnabled(True)
        NotificationLogListDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(NotificationLogListDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lblAdditionalData = QtGui.QLabel(NotificationLogListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblAdditionalData.sizePolicy().hasHeightForWidth())
        self.lblAdditionalData.setSizePolicy(sizePolicy)
        self.lblAdditionalData.setText(_fromUtf8(""))
        self.lblAdditionalData.setObjectName(_fromUtf8("lblAdditionalData"))
        self.gridLayout.addWidget(self.lblAdditionalData, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(NotificationLogListDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 1, 1, 1)
        self.label = QtGui.QLabel(NotificationLogListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.statusBar = QtGui.QStatusBar(NotificationLogListDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusBar.sizePolicy().hasHeightForWidth())
        self.statusBar.setSizePolicy(sizePolicy)
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        self.gridLayout.addWidget(self.statusBar, 3, 0, 1, 1)
        self.tblItems = CTableView(NotificationLogListDialog)
        self.tblItems.setTabKeyNavigation(False)
        self.tblItems.setAlternatingRowColors(True)
        self.tblItems.setObjectName(_fromUtf8("tblItems"))
        self.gridLayout.addWidget(self.tblItems, 0, 0, 1, 2)

        self.retranslateUi(NotificationLogListDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NotificationLogListDialog.close)
        QtCore.QMetaObject.connectSlotsByName(NotificationLogListDialog)

    def retranslateUi(self, NotificationLogListDialog):
        NotificationLogListDialog.setWindowTitle(_translate("NotificationLogListDialog", "Список записей", None))
        self.label.setText(_translate("NotificationLogListDialog", "всего: ", None))
        self.statusBar.setToolTip(_translate("NotificationLogListDialog", "A status bar", None))
        self.statusBar.setWhatsThis(_translate("NotificationLogListDialog", "A status bar.", None))
        self.tblItems.setWhatsThis(_translate("NotificationLogListDialog", "список записей", "ура!"))

from library.TableView import CTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    NotificationLogListDialog = QtGui.QDialog()
    ui = Ui_NotificationLogListDialog()
    ui.setupUi(NotificationLogListDialog)
    NotificationLogListDialog.show()
    sys.exit(app.exec_())

