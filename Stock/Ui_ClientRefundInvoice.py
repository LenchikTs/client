# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/green/s11_trunk/Stock/ClientRefundInvoice.ui'
#
# Created: Wed May  7 18:16:39 2014
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_ClientRefundInvoiceDialog(object):
    def setupUi(self, ClientRefundInvoiceDialog):
        ClientRefundInvoiceDialog.setObjectName(_fromUtf8("ClientRefundInvoiceDialog"))
        ClientRefundInvoiceDialog.resize(600, 500)
        self.gridLayout = QtGui.QGridLayout(ClientRefundInvoiceDialog)
        self.gridLayout.setMargin(4)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.txtClientInfoBrowser = CTextBrowser(ClientRefundInvoiceDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtClientInfoBrowser.sizePolicy().hasHeightForWidth())
        self.txtClientInfoBrowser.setSizePolicy(sizePolicy)
        self.txtClientInfoBrowser.setMinimumSize(QtCore.QSize(0, 100))
        self.txtClientInfoBrowser.setMaximumSize(QtCore.QSize(16777215, 130))
        self.txtClientInfoBrowser.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.txtClientInfoBrowser.setObjectName(_fromUtf8("txtClientInfoBrowser"))
        self.gridLayout.addWidget(self.txtClientInfoBrowser, 0, 0, 1, 5)
        self.lblNumber = QtGui.QLabel(ClientRefundInvoiceDialog)
        self.lblNumber.setObjectName(_fromUtf8("lblNumber"))
        self.gridLayout.addWidget(self.lblNumber, 1, 0, 1, 1)
        self.edtNumber = QtGui.QLineEdit(ClientRefundInvoiceDialog)
        self.edtNumber.setObjectName(_fromUtf8("edtNumber"))
        self.gridLayout.addWidget(self.edtNumber, 1, 1, 1, 1)
        self.lblDate = QtGui.QLabel(ClientRefundInvoiceDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDate.sizePolicy().hasHeightForWidth())
        self.lblDate.setSizePolicy(sizePolicy)
        self.lblDate.setObjectName(_fromUtf8("lblDate"))
        self.gridLayout.addWidget(self.lblDate, 1, 2, 1, 1)
        self.edtDate = CDateEdit(ClientRefundInvoiceDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtDate.sizePolicy().hasHeightForWidth())
        self.edtDate.setSizePolicy(sizePolicy)
        self.edtDate.setObjectName(_fromUtf8("edtDate"))
        self.gridLayout.addWidget(self.edtDate, 1, 3, 1, 1)
        self.edtTime = QtGui.QTimeEdit(ClientRefundInvoiceDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtTime.sizePolicy().hasHeightForWidth())
        self.edtTime.setSizePolicy(sizePolicy)
        self.edtTime.setObjectName(_fromUtf8("edtTime"))
        self.gridLayout.addWidget(self.edtTime, 1, 4, 1, 1)
        self.lblReason = QtGui.QLabel(ClientRefundInvoiceDialog)
        self.lblReason.setObjectName(_fromUtf8("lblReason"))
        self.gridLayout.addWidget(self.lblReason, 2, 0, 1, 1)
        self.edtReason = QtGui.QLineEdit(ClientRefundInvoiceDialog)
        self.edtReason.setObjectName(_fromUtf8("edtReason"))
        self.gridLayout.addWidget(self.edtReason, 2, 1, 1, 1)
        self.lblReasonDate = QtGui.QLabel(ClientRefundInvoiceDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblReasonDate.sizePolicy().hasHeightForWidth())
        self.lblReasonDate.setSizePolicy(sizePolicy)
        self.lblReasonDate.setObjectName(_fromUtf8("lblReasonDate"))
        self.gridLayout.addWidget(self.lblReasonDate, 2, 2, 1, 1)
        self.edtReasonDate = CDateEdit(ClientRefundInvoiceDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edtReasonDate.sizePolicy().hasHeightForWidth())
        self.edtReasonDate.setSizePolicy(sizePolicy)
        self.edtReasonDate.setObjectName(_fromUtf8("edtReasonDate"))
        self.gridLayout.addWidget(self.edtReasonDate, 2, 3, 1, 1)
        self.lblReceiver = QtGui.QLabel(ClientRefundInvoiceDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblReceiver.sizePolicy().hasHeightForWidth())
        self.lblReceiver.setSizePolicy(sizePolicy)
        self.lblReceiver.setObjectName(_fromUtf8("lblReceiver"))
        self.gridLayout.addWidget(self.lblReceiver, 3, 0, 1, 1)
        self.lblReceiverPerson = QtGui.QLabel(ClientRefundInvoiceDialog)
        self.lblReceiverPerson.setObjectName(_fromUtf8("lblReceiverPerson"))
        self.gridLayout.addWidget(self.lblReceiverPerson, 4, 0, 1, 1)
        self.lblNote = QtGui.QLabel(ClientRefundInvoiceDialog)
        self.lblNote.setObjectName(_fromUtf8("lblNote"))
        self.gridLayout.addWidget(self.lblNote, 5, 0, 1, 1)
        self.tblItems = CInDocTableView(ClientRefundInvoiceDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblItems.sizePolicy().hasHeightForWidth())
        self.tblItems.setSizePolicy(sizePolicy)
        self.tblItems.setObjectName(_fromUtf8("tblItems"))
        self.gridLayout.addWidget(self.tblItems, 6, 0, 1, 5)
        self.edtNote = QtGui.QLineEdit(ClientRefundInvoiceDialog)
        self.edtNote.setObjectName(_fromUtf8("edtNote"))
        self.gridLayout.addWidget(self.edtNote, 5, 1, 1, 4)
        self.cmbReceiverPerson = CPersonComboBoxEx(ClientRefundInvoiceDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbReceiverPerson.sizePolicy().hasHeightForWidth())
        self.cmbReceiverPerson.setSizePolicy(sizePolicy)
        self.cmbReceiverPerson.setObjectName(_fromUtf8("cmbReceiverPerson"))
        self.gridLayout.addWidget(self.cmbReceiverPerson, 4, 1, 1, 4)
        self.cmbReceiver = CStorageComboBox(ClientRefundInvoiceDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbReceiver.sizePolicy().hasHeightForWidth())
        self.cmbReceiver.setSizePolicy(sizePolicy)
        self.cmbReceiver.setObjectName(_fromUtf8("cmbReceiver"))
        self.gridLayout.addWidget(self.cmbReceiver, 3, 1, 1, 4)
        self.lblSummaryInfo = QtGui.QLabel(ClientRefundInvoiceDialog)
        self.lblSummaryInfo.setText(_fromUtf8(""))
        self.lblSummaryInfo.setObjectName(_fromUtf8("lblSummaryInfo"))
        self.gridLayout.addWidget(self.lblSummaryInfo, 7, 0, 1, 5)
        self.buttonBox = QtGui.QDialogButtonBox(ClientRefundInvoiceDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 8, 0, 1, 5)
        self.lblNumber.setBuddy(self.edtNumber)
        self.lblDate.setBuddy(self.edtDate)
        self.lblReason.setBuddy(self.edtReason)
        self.lblReasonDate.setBuddy(self.edtReasonDate)
        self.lblReceiver.setBuddy(self.cmbReceiver)
        self.lblReceiverPerson.setBuddy(self.cmbReceiverPerson)
        self.lblNote.setBuddy(self.edtNote)

        self.retranslateUi(ClientRefundInvoiceDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ClientRefundInvoiceDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ClientRefundInvoiceDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ClientRefundInvoiceDialog)
        ClientRefundInvoiceDialog.setTabOrder(self.edtNumber, self.edtDate)
        ClientRefundInvoiceDialog.setTabOrder(self.edtDate, self.edtTime)
        ClientRefundInvoiceDialog.setTabOrder(self.edtTime, self.edtReason)
        ClientRefundInvoiceDialog.setTabOrder(self.edtReason, self.edtReasonDate)
        ClientRefundInvoiceDialog.setTabOrder(self.edtReasonDate, self.cmbReceiver)
        ClientRefundInvoiceDialog.setTabOrder(self.cmbReceiver, self.cmbReceiverPerson)
        ClientRefundInvoiceDialog.setTabOrder(self.cmbReceiverPerson, self.edtNote)
        ClientRefundInvoiceDialog.setTabOrder(self.edtNote, self.tblItems)
        ClientRefundInvoiceDialog.setTabOrder(self.tblItems, self.buttonBox)

    def retranslateUi(self, ClientRefundInvoiceDialog):
        ClientRefundInvoiceDialog.setWindowTitle(_translate("ClientRefundInvoiceDialog", "Накладная на возврат ЛСиИМН от пациента", None))
        self.txtClientInfoBrowser.setWhatsThis(_translate("ClientRefundInvoiceDialog", "Описание пациента", None))
        self.txtClientInfoBrowser.setHtml(_translate("ClientRefundInvoiceDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Liberation Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p></body></html>", None))
        self.lblNumber.setText(_translate("ClientRefundInvoiceDialog", "Номер", None))
        self.lblDate.setText(_translate("ClientRefundInvoiceDialog", "Дата", None))
        self.edtTime.setDisplayFormat(_translate("ClientRefundInvoiceDialog", "HH:mm", None))
        self.lblReason.setText(_translate("ClientRefundInvoiceDialog", "Основание", None))
        self.lblReasonDate.setText(_translate("ClientRefundInvoiceDialog", "Дата основания", None))
        self.lblReceiver.setText(_translate("ClientRefundInvoiceDialog", "Получатель", None))
        self.lblReceiverPerson.setText(_translate("ClientRefundInvoiceDialog", "Ответственный", None))
        self.lblNote.setText(_translate("ClientRefundInvoiceDialog", "Примечания", None))

from library.InDocTable import CInDocTableView
from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from library.TextBrowser import CTextBrowser
from library.DateEdit import CDateEdit
from Orgs.OrgStructComboBoxes import CStorageComboBox

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ClientRefundInvoiceDialog = QtGui.QDialog()
    ui = Ui_ClientRefundInvoiceDialog()
    ui.setupUi(ClientRefundInvoiceDialog)
    ClientRefundInvoiceDialog.show()
    sys.exit(app.exec_())

