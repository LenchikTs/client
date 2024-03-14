# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROJECTS\samson\UP_s11\client_test\Exchange\ImportDispExportedPlanSyncDialog.ui'
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

class Ui_ImportDispExportedPlanSyncDialog(object):
    def setupUi(self, ImportDispExportedPlanSyncDialog):
        ImportDispExportedPlanSyncDialog.setObjectName(_fromUtf8("ImportDispExportedPlanSyncDialog"))
        ImportDispExportedPlanSyncDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        ImportDispExportedPlanSyncDialog.resize(572, 254)
        self.verticalLayout = QtGui.QVBoxLayout(ImportDispExportedPlanSyncDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(ImportDispExportedPlanSyncDialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.lblMonthYearTotalCount = QtGui.QLabel(ImportDispExportedPlanSyncDialog)
        self.lblMonthYearTotalCount.setObjectName(_fromUtf8("lblMonthYearTotalCount"))
        self.verticalLayout.addWidget(self.lblMonthYearTotalCount)
        self.lblDeleteCSS = QtGui.QLabel(ImportDispExportedPlanSyncDialog)
        self.lblDeleteCSS.setObjectName(_fromUtf8("lblDeleteCSS"))
        self.verticalLayout.addWidget(self.lblDeleteCSS)
        self.lblInsertCSS = QtGui.QLabel(ImportDispExportedPlanSyncDialog)
        self.lblInsertCSS.setObjectName(_fromUtf8("lblInsertCSS"))
        self.verticalLayout.addWidget(self.lblInsertCSS)
        self.lblUpdatePlanExport = QtGui.QLabel(ImportDispExportedPlanSyncDialog)
        self.lblUpdatePlanExport.setObjectName(_fromUtf8("lblUpdatePlanExport"))
        self.verticalLayout.addWidget(self.lblUpdatePlanExport)
        self.lblDeletePlanExport = QtGui.QLabel(ImportDispExportedPlanSyncDialog)
        self.lblDeletePlanExport.setObjectName(_fromUtf8("lblDeletePlanExport"))
        self.verticalLayout.addWidget(self.lblDeletePlanExport)
        self.chkDeleteNotFoundCSS = QtGui.QCheckBox(ImportDispExportedPlanSyncDialog)
        self.chkDeleteNotFoundCSS.setObjectName(_fromUtf8("chkDeleteNotFoundCSS"))
        self.verticalLayout.addWidget(self.chkDeleteNotFoundCSS)
        self.label_2 = QtGui.QLabel(ImportDispExportedPlanSyncDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.buttonBox = QtGui.QDialogButtonBox(ImportDispExportedPlanSyncDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.No|QtGui.QDialogButtonBox.Yes)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(ImportDispExportedPlanSyncDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ImportDispExportedPlanSyncDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ImportDispExportedPlanSyncDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ImportDispExportedPlanSyncDialog)

    def retranslateUi(self, ImportDispExportedPlanSyncDialog):
        ImportDispExportedPlanSyncDialog.setWindowTitle(_translate("ImportDispExportedPlanSyncDialog", "Внимание!", None))
        self.label.setText(_translate("ImportDispExportedPlanSyncDialog", "Данные о планировании профилактических мероприятий будут обновлены в МИС\n"
"в соответствии с данными, импортированными из ТФОМС:", None))
        self.lblMonthYearTotalCount.setText(_translate("ImportDispExportedPlanSyncDialog", "Импортировано из ТФОМС за месяц 0000 г.: 0", None))
        self.lblDeleteCSS.setText(_translate("ImportDispExportedPlanSyncDialog", "Удалить планирование: 0", None))
        self.lblInsertCSS.setText(_translate("ImportDispExportedPlanSyncDialog", "Добавить планирование: 0", None))
        self.lblUpdatePlanExport.setText(_translate("ImportDispExportedPlanSyncDialog", "Обновить признак экспорта: 0", None))
        self.lblDeletePlanExport.setText(_translate("ImportDispExportedPlanSyncDialog", "Удалить признак экспорта: 0", None))
        self.chkDeleteNotFoundCSS.setText(_translate("ImportDispExportedPlanSyncDialog", "Удалить соц. статусы из карт, не найденных на сервисе: 0", None))
        self.label_2.setText(_translate("ImportDispExportedPlanSyncDialog", "Продолжить?", None))

