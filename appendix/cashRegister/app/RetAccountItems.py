# -*- coding: utf-8 -*-

#############################################################################
##
## Copyright (C) 2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, pyqtSignature, QVariant
from PyQt4.QtSql  import QSqlField

from library.DialogBase import CDialogBase
from library.InDocTable import CInDocTableCol, CRecordListModel
from library.Utils      import forceDouble, toVariant

from AmountCol          import CAmountCol
from SumCol             import CSumCol

from Ui_RetAccountItems import Ui_CRetAccountItems


class CRetAccountItemsDialog(Ui_CRetAccountItems, CDialogBase):
    u"""
    """
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.addModels('AccountItems', CAccountItemsTableModel(self))
        self.setupUi(self)
        self.setModels(self.tblAccountItems, self.modelAccountItems, self.selectionModelAccountItems)


    def setAccountNumber(self, val):
        self.lblAccountNumberText.setText(val)


    def setAccountDate(self, val):
        self.lblAccountDateText.setText(val)


    def setClientName(self, val):
        self.lblClientNameText.setText(val)


    def setPayerName(self, val):
        self.lblPayerNameText.setText(val)


    def setAccountItems(self, items):
        self.modelAccountItems.setItems(items)
        self.updateCounters()


    def updateCounters(self):
        retAmount = 0.0
        retSum    = 0.0
        for item in self.modelAccountItems.items():
            retAmount += round(forceDouble(item.value('retAmount')), 3)
            retSum    += round(forceDouble(item.value('retSum')), 2)
        self.lblRetAmountText.setText( format(round(retAmount, 3), '.3f'))
        self.lblRetSumText.setText(    format(round(retSum, 2),    '.2f'))


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_modelAccountItems_dataChanged(self, leftTop, rightBottom):
        self.updateCounters()



class CRetAmountCol(CAmountCol):
    def createEditor(self, parent):
        editor = QtGui.QLineEdit(parent)
        validator = QtGui.QDoubleValidator(editor)
        validator.setRange(self.low, self.high, self.precision)
        editor.setValidator(validator)
        return editor


    def setEditorData(self, editor, value, record):
        payedAmount = forceDouble(record.value('payedAmount'))
#        validator = QtGui.QDoubleValidator(editor)
#        validator.setRange(0, payedAmount, self.precision)
#        editor.setValidator(validator)
        editor.validator().setRange(0, payedAmount, self.precision)
        CAmountCol.setEditorData(self, editor, value, record)


    def getEditorData(self, editor):
        validator = editor.validator()
        return toVariant(max(validator.bottom(), min(validator.top(), editor.text().toDouble()[0])))



class CAccountItemsTableModel( CRecordListModel ):
    def __init__(self, parent, showPayedItems=False):

        CRecordListModel.__init__(self, parent)
#        self.addCol(CDateInDocTableCol( u'Дата',         'serviceDate', 12).setSortable())
        self.addCol(CInDocTableCol( u'Код',              'serviceCode', 12).setSortable())
        self.addCol(CInDocTableCol( u'Наименование',     'serviceName', 12).setSortable())
        self.addCol(CSumCol(        u'Цена',             'price',       12, precision=2).setSortable())
        self.addCol(CAmountCol(     u'Опл.количество',   'payedAmount', 12, precision=3).setSortable())
        self.addCol(CSumCol(        u'Опл.сумма',        'payedSum',    12, precision=2).setSortable())
        self.addCol(CRetAmountCol(  u'Возвр.количество', 'retAmount',   12, precision=3).setSortable())
        self.addCol(CSumCol(        u'Возвр.сумма',      'retSum',      12, precision=2).setSortable())

#    def flags(self, index):
#        return Qt.ItemIsSelectable|Qt.ItemIsEnabled

    def cellReadOnly(self, index):
        col = index.column()
        return col != 5


    def setItems(self, items):
        fieldPayedAmount = QSqlField('payedAmount', QVariant.Double)
        fieldRetAmount   = QSqlField('retAmount',   QVariant.Double)
        fieldRetSum      = QSqlField('retSum',      QVariant.Double)
        for item in items:
            item.append(fieldPayedAmount)
            item.append(fieldRetAmount)
            item.append(fieldRetSum)

            price    = forceDouble( item.value('price')  )
            payedSum = forceDouble( item.value('payedSum')  )
            payedAmount = payedSum/price if price != 0 else 0

            item.setValue( 'payedAmount',  payedAmount )
            item.setValue( 'retAmount',    payedAmount )
            item.setValue( 'retSum',       payedSum )
        CRecordListModel.setItems(self, items)


    def setData(self, index, value, role=Qt.EditRole):
        result = CRecordListModel.setData(self, index, value, role)
        if result and role==Qt.EditRole and index.column() == 5:
            row = index.row()
            price = forceDouble(self.value(row, 'price'))
            retSum = round( price*forceDouble(value), 2)
            self.setValue(row, 'retSum', retSum)
        return result

