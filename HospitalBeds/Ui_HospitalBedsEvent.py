# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\py\s11-svn\HospitalBeds\HospitalBedsEvent.ui'
#
# Created: Thu Jul 08 15:47:13 2010
#      by: PyQt4 UI code generator snapshot-4.7.1-106919e3444b
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_dialogHospitalBedsEvent(object):
    def setupUi(self, dialogHospitalBedsEvent):
        dialogHospitalBedsEvent.setObjectName("dialogHospitalBedsEvent")
        dialogHospitalBedsEvent.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(dialogHospitalBedsEvent)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.tblHospitalBedEvent = CTableView(dialogHospitalBedsEvent)
        self.tblHospitalBedEvent.setObjectName("tblHospitalBedEvent")
        self.gridLayout.addWidget(self.tblHospitalBedEvent, 0, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(294, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.btnClose = QtGui.QPushButton(dialogHospitalBedsEvent)
        self.btnClose.setObjectName("btnClose")
        self.gridLayout.addWidget(self.btnClose, 1, 1, 1, 1)

        self.retranslateUi(dialogHospitalBedsEvent)
        QtCore.QMetaObject.connectSlotsByName(dialogHospitalBedsEvent)

    def retranslateUi(self, dialogHospitalBedsEvent):
        dialogHospitalBedsEvent.setWindowTitle(QtGui.QApplication.translate("dialogHospitalBedsEvent", "События для коек", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClose.setText(QtGui.QApplication.translate("dialogHospitalBedsEvent", "Закрыть", None, QtGui.QApplication.UnicodeUTF8))

from library.TableView import CTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    dialogHospitalBedsEvent = QtGui.QDialog()
    ui = Ui_dialogHospitalBedsEvent()
    ui.setupUi(dialogHospitalBedsEvent)
    dialogHospitalBedsEvent.show()
    sys.exit(app.exec_())

