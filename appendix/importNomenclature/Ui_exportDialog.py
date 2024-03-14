# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/pvtr/py-dev/samson/appendix/importNomenclature/exportDialog.ui'
#
# Created by: PyQt4 UI code generator 4.12.3
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

class Ui_ExportDialog(object):
    def setupUi(self, ExportDialog):
        ExportDialog.setObjectName(_fromUtf8("ExportDialog"))
        ExportDialog.resize(792, 669)
        self.verticalLayout = QtGui.QVBoxLayout(ExportDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gbStockMotion = QtGui.QGroupBox(ExportDialog)
        self.gbStockMotion.setObjectName(_fromUtf8("gbStockMotion"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.gbStockMotion)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gbFilter = QtGui.QGroupBox(self.gbStockMotion)
        self.gbFilter.setObjectName(_fromUtf8("gbFilter"))
        self.gridLayout = QtGui.QGridLayout(self.gbFilter)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cmbMotionsFilterSupplier = CStorageComboBox(self.gbFilter)
        self.cmbMotionsFilterSupplier.setObjectName(_fromUtf8("cmbMotionsFilterSupplier"))
        self.gridLayout.addWidget(self.cmbMotionsFilterSupplier, 4, 1, 1, 2)
        self.lblDocType = QtGui.QLabel(self.gbFilter)
        self.lblDocType.setObjectName(_fromUtf8("lblDocType"))
        self.gridLayout.addWidget(self.lblDocType, 0, 0, 1, 1)
        self.lblSource = QtGui.QLabel(self.gbFilter)
        self.lblSource.setObjectName(_fromUtf8("lblSource"))
        self.gridLayout.addWidget(self.lblSource, 4, 0, 1, 1)
        self.cmbMotionsFilterReceiver = CStorageComboBox(self.gbFilter)
        self.cmbMotionsFilterReceiver.setObjectName(_fromUtf8("cmbMotionsFilterReceiver"))
        self.gridLayout.addWidget(self.cmbMotionsFilterReceiver, 6, 1, 1, 2)
        self.cmbMotionsFilterType = CStockMotionTypeComboBox(self.gbFilter)
        self.cmbMotionsFilterType.setObjectName(_fromUtf8("cmbMotionsFilterType"))
        self.gridLayout.addWidget(self.cmbMotionsFilterType, 0, 1, 1, 2)
        self.lblDest = QtGui.QLabel(self.gbFilter)
        self.lblDest.setObjectName(_fromUtf8("lblDest"))
        self.gridLayout.addWidget(self.lblDest, 6, 0, 1, 1)
        self.edtMotionsFilterBegDate = CDateEdit(self.gbFilter)
        self.edtMotionsFilterBegDate.setObjectName(_fromUtf8("edtMotionsFilterBegDate"))
        self.gridLayout.addWidget(self.edtMotionsFilterBegDate, 1, 1, 1, 1)
        self.lblPeriod = QtGui.QLabel(self.gbFilter)
        self.lblPeriod.setObjectName(_fromUtf8("lblPeriod"))
        self.gridLayout.addWidget(self.lblPeriod, 1, 0, 1, 1)
        self.edtMotionsFilterEndDate = CDateEdit(self.gbFilter)
        self.edtMotionsFilterEndDate.setObjectName(_fromUtf8("edtMotionsFilterEndDate"))
        self.gridLayout.addWidget(self.edtMotionsFilterEndDate, 1, 2, 1, 1)
        self.btnMotionsFilterReset = QtGui.QPushButton(self.gbFilter)
        self.btnMotionsFilterReset.setObjectName(_fromUtf8("btnMotionsFilterReset"))
        self.gridLayout.addWidget(self.btnMotionsFilterReset, 7, 2, 1, 1)
        self.btnMotionsFilterApply = QtGui.QPushButton(self.gbFilter)
        self.btnMotionsFilterApply.setObjectName(_fromUtf8("btnMotionsFilterApply"))
        self.gridLayout.addWidget(self.btnMotionsFilterApply, 7, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 8, 1, 1, 1)
        self.horizontalLayout.addWidget(self.gbFilter)
        self.tblMotions = CTableView(self.gbStockMotion)
        self.tblMotions.setObjectName(_fromUtf8("tblMotions"))
        self.horizontalLayout.addWidget(self.tblMotions)
        self.verticalLayout.addWidget(self.gbStockMotion)
        self.gbStockRequisition = QtGui.QGroupBox(ExportDialog)
        self.gbStockRequisition.setObjectName(_fromUtf8("gbStockRequisition"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.gbStockRequisition)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.gbRequisitionFilter = QtGui.QGroupBox(self.gbStockRequisition)
        self.gbRequisitionFilter.setObjectName(_fromUtf8("gbRequisitionFilter"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gbRequisitionFilter)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lblRequisitionsPeriod = QtGui.QLabel(self.gbRequisitionFilter)
        self.lblRequisitionsPeriod.setObjectName(_fromUtf8("lblRequisitionsPeriod"))
        self.gridLayout_2.addWidget(self.lblRequisitionsPeriod, 0, 0, 1, 1)
        self.cmbRequisitionsFilterSupplier = CStorageComboBox(self.gbRequisitionFilter)
        self.cmbRequisitionsFilterSupplier.setObjectName(_fromUtf8("cmbRequisitionsFilterSupplier"))
        self.gridLayout_2.addWidget(self.cmbRequisitionsFilterSupplier, 3, 1, 1, 2)
        self.lblRequisitionsSource = QtGui.QLabel(self.gbRequisitionFilter)
        self.lblRequisitionsSource.setObjectName(_fromUtf8("lblRequisitionsSource"))
        self.gridLayout_2.addWidget(self.lblRequisitionsSource, 3, 0, 1, 1)
        self.edtRequisitionsFilterBegDate = CDateEdit(self.gbRequisitionFilter)
        self.edtRequisitionsFilterBegDate.setObjectName(_fromUtf8("edtRequisitionsFilterBegDate"))
        self.gridLayout_2.addWidget(self.edtRequisitionsFilterBegDate, 0, 1, 1, 1)
        self.btnRequisitionsFilterApply = QtGui.QPushButton(self.gbRequisitionFilter)
        self.btnRequisitionsFilterApply.setObjectName(_fromUtf8("btnRequisitionsFilterApply"))
        self.gridLayout_2.addWidget(self.btnRequisitionsFilterApply, 6, 1, 1, 1)
        self.lblRequisitionsDest = QtGui.QLabel(self.gbRequisitionFilter)
        self.lblRequisitionsDest.setObjectName(_fromUtf8("lblRequisitionsDest"))
        self.gridLayout_2.addWidget(self.lblRequisitionsDest, 5, 0, 1, 1)
        self.cmbRequisitionsFilterRecipient = CStorageComboBox(self.gbRequisitionFilter)
        self.cmbRequisitionsFilterRecipient.setObjectName(_fromUtf8("cmbRequisitionsFilterRecipient"))
        self.gridLayout_2.addWidget(self.cmbRequisitionsFilterRecipient, 5, 1, 1, 2)
        self.btnRequisitionsFilterReset = QtGui.QPushButton(self.gbRequisitionFilter)
        self.btnRequisitionsFilterReset.setObjectName(_fromUtf8("btnRequisitionsFilterReset"))
        self.gridLayout_2.addWidget(self.btnRequisitionsFilterReset, 6, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 7, 1, 1, 1)
        self.edtRequisitionsFilterEndDate = CDateEdit(self.gbRequisitionFilter)
        self.edtRequisitionsFilterEndDate.setObjectName(_fromUtf8("edtRequisitionsFilterEndDate"))
        self.gridLayout_2.addWidget(self.edtRequisitionsFilterEndDate, 0, 2, 1, 1)
        self.horizontalLayout_2.addWidget(self.gbRequisitionFilter)
        self.tblRequisitions = CTableView(self.gbStockRequisition)
        self.tblRequisitions.setObjectName(_fromUtf8("tblRequisitions"))
        self.horizontalLayout_2.addWidget(self.tblRequisitions)
        self.verticalLayout.addWidget(self.gbStockRequisition)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.btnExport = QtGui.QPushButton(ExportDialog)
        self.btnExport.setObjectName(_fromUtf8("btnExport"))
        self.horizontalLayout_3.addWidget(self.btnExport)
        self.btnClose = QtGui.QPushButton(ExportDialog)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.horizontalLayout_3.addWidget(self.btnClose)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(ExportDialog)
        QtCore.QObject.connect(self.btnClose, QtCore.SIGNAL(_fromUtf8("clicked()")), ExportDialog.close)
        QtCore.QMetaObject.connectSlotsByName(ExportDialog)

    def retranslateUi(self, ExportDialog):
        ExportDialog.setWindowTitle(_translate("ExportDialog", "Dialog", None))
        self.gbStockMotion.setTitle(_translate("ExportDialog", "Движения", None))
        self.gbFilter.setTitle(_translate("ExportDialog", "Фильтр", None))
        self.lblDocType.setText(_translate("ExportDialog", "Тип документа", None))
        self.lblSource.setText(_translate("ExportDialog", "Источник", None))
        self.lblDest.setText(_translate("ExportDialog", "Получатель", None))
        self.lblPeriod.setText(_translate("ExportDialog", "Период", None))
        self.btnMotionsFilterReset.setText(_translate("ExportDialog", "Сбросить", None))
        self.btnMotionsFilterApply.setText(_translate("ExportDialog", "Применить", None))
        self.gbStockRequisition.setTitle(_translate("ExportDialog", "Требования", None))
        self.gbRequisitionFilter.setTitle(_translate("ExportDialog", "Фильтр", None))
        self.lblRequisitionsPeriod.setText(_translate("ExportDialog", "Период", None))
        self.lblRequisitionsSource.setText(_translate("ExportDialog", "Источник", None))
        self.btnRequisitionsFilterApply.setText(_translate("ExportDialog", "Применить", None))
        self.lblRequisitionsDest.setText(_translate("ExportDialog", "Получатель", None))
        self.btnRequisitionsFilterReset.setText(_translate("ExportDialog", "Сбросить", None))
        self.btnExport.setText(_translate("ExportDialog", "Экспорт", None))
        self.btnClose.setText(_translate("ExportDialog", "Закрыть", None))

from Orgs.OrgStructComboBoxes import CStorageComboBox
from appendix.importNomenclature.StockMotionTypeComboBox import CStockMotionTypeComboBox
from library.DateEdit import CDateEdit
from library.TableView import CTableView

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ExportDialog = QtGui.QDialog()
    ui = Ui_ExportDialog()
    ui.setupUi(ExportDialog)
    ExportDialog.show()
    sys.exit(app.exec_())

