# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature, QDate

from library.Counter         import formatDocumentNumber2Int, delCachedValues
from library.DialogBase      import CDialogBase
from library.interchange     import getCheckBoxValue, getComboBoxValue, getLineEditValue, setCheckBoxValue, setComboBoxValue, setLineEditValue
from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog
from library.TableModel      import CBoolCol, CEnumCol, CNumCol, CTextCol
from library.Utils           import exceptionToUnicode, forceInt, forceRef

from .Ui_RBCounterEditor         import Ui_RBCounterEditor
from .Ui_CounterFormatTestDialog import Ui_CounterFormatTestDialog


class CCounterValueCol(CNumCol):
    def __init__(self, title, fields, defaultWidth, alignment='r'):
        CNumCol.__init__(self, title, fields, defaultWidth, alignment)
        self.counterValueIdCache = {}


    def extractValuesFromRecord(self, record):
        counterId = forceInt(record.value('id'))
        (counterValueId, value) = self.counterValueIdCache.get(counterId, (None, 0))
        if counterValueId is None:
            db = QtGui.qApp.db
            query = db.query('SELECT findOrCreateCounterValueRecord(%d, CURRENT_DATE()) AS id'%counterId)
            if query.next():
                counterValueId = forceRef(query.record().value(0))
            if counterValueId:
                value = forceInt(db.translate('rbCounter_Value', 'id', counterValueId, 'value'))
            self.counterValueIdCache[counterId] = (counterValueId, value)
        return [value]


    def invalidateRecordsCache(self):
        self.counterValueIdCache.clear()


class CRBCounterList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Код',                     ['code'],         10),
            CTextCol(u'Наименование',            ['name'],         30),
            CCounterValueCol(u'Текущее значение',['value'],        16),
            CTextCol(u'Префикс',                 ['prefix'],       10),
            CTextCol(u'Постфикс',                ['postfix'],      10),
            CTextCol(u'Разделитель',             ['separator'],    10),
            CTextCol(u'Формат',                  ['format'],       20),

            CEnumCol(u'Сброс',                   ['reset'],  [u'Не сбрасывается',
                                                              u'Каждые сутки',
                                                              u'Каждую неделю',
                                                              u'Каждый месяц',
                                                              u'Каждый квартал',
                                                              u'Каждое полугодие',
                                                              u'Каждый год'],
                                                                   16),
#            CDateCol(u'Дата начала работы',      ['startDate'],    10),
#            CDateCol(u'Дата следующего сброса',  ['nextDate'],    10),
            CBoolCol(u'Флаг последовательности', ['sequenceFlag'], 10)
            ], 'rbCounter', ['code', 'name'])
        self.setWindowTitleEx(u'Счетчики')


    def getItemEditor(self):
        return CRBCounterListEditor(self)


class CRBCounterListEditor(CItemEditorBaseDialog, Ui_RBCounterEditor):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, 'rbCounter')
        self.setupUi(self)
        self.setWindowTitleEx(u'Счетчик')
        self.counterValueIdCache = {}
        self.setupDirtyCather()


    def getValue(self, record):
        counterId = forceInt(record.value('id'))
        (counterValueId, value) = self.counterValueIdCache.get(counterId, (None, 0))
        if counterValueId is None:
            db = QtGui.qApp.db
            query = db.query('SELECT findOrCreateCounterValueRecord(%d, CURRENT_DATE()) AS id'%counterId)
            if query.next():
                counterValueId = forceRef(query.record().value(0))
            if counterValueId:
                value = forceInt(db.translate('rbCounter_Value', 'id', counterValueId, 'value'))
            self.counterValueIdCache[counterId] = (counterValueId, value)
        return value


    def setValue(self, record):
        counterId = forceInt(record.value('id'))
        (counterValueId, value) = self.counterValueIdCache.get(counterId, (None, None))
        newValue = self.edtValue.value()
        if value != newValue:
            db = QtGui.qApp.db
            table = db.table('rbCounter_Value')
            record = db.getRecord(table, 'id, value', counterValueId)
            if record:
                record.setValue('value', newValue)
                db.updateRecord(table, record)


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(   self.edtCode,          record, 'code')
        setLineEditValue(   self.edtName,          record, 'name')
        setCheckBoxValue(   self.chkSequenceFlag,  record, 'sequenceFlag')
        setComboBoxValue(   self.cmbReset,         record, 'reset')
#        setDateEditValue(   self.edtStartDate,     record, 'startDate')
        setLineEditValue(   self.edtPrefix,        record, 'prefix')
        setLineEditValue(   self.edtPostfix,       record, 'postfix')
        setLineEditValue(   self.edtSeparator,     record, 'separator')
        setLineEditValue(   self.edtFormat,        record, 'format')
        self.edtValue.setValue(self.getValue(record))


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(   self.edtCode,          record, 'code')
        getLineEditValue(   self.edtName,          record, 'name')
        getCheckBoxValue(   self.chkSequenceFlag,  record, 'sequenceFlag')
        getComboBoxValue(   self.cmbReset,         record, 'reset')
#        getDateEditValue(   self.edtStartDate,     record, 'startDate')
        getLineEditValue(   self.edtPrefix,        record, 'prefix')
        getLineEditValue(   self.edtPostfix,       record, 'postfix')
        getLineEditValue(   self.edtSeparator,     record, 'separator')
        getLineEditValue(   self.edtFormat,        record, 'format')
        self.setValue(record)
        return record

#    @pyqtSignature('QString')
#    def on_edtFormat_textChanged(self, val):
#        self.btnFormatTest.setEnabled(bool(val))

    @pyqtSignature('')
    def on_btnFormatTest_clicked(self):
        dlg = CCounterFormatTestDialog(self)
        dlg.setFormat(self.edtFormat.text())
        dlg.setValue(self.edtValue.value())
        if dlg.exec_():
            self.edtFormat.setText(dlg.getFormat())

    @pyqtSignature('int')
    def on_edtValue_valueChanged(self, val):
        if self.chkSequenceFlag.isChecked():
            delCachedValues(self._id, val)


class CCounterFormatTestDialog(Ui_CounterFormatTestDialog, CDialogBase):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.addObject('btnEval', QtGui.QPushButton(u'В&ычислить', self))
        self.setupUi(self)
        self.buttonBox.addButton(self.btnEval, self.buttonBox.ActionRole)
        self.edtDate.setDate(QDate.currentDate())


    def setFormat(self, format):
        self.edtFormat.setText(format)
        self.edtFormat.end(False)


    def setValue(self, value):
        self.edtValue.setValue(value)


    def getFormat(self):
        return unicode(self.edtFormat.text())


    def addFormat(self, part):
        self.edtFormat.insert(part)


    @pyqtSignature('')
    def on_btnEval_clicked(self):
        format = self.getFormat()
        value = self.edtValue.value()
        clientId = self.edtClientId.value()
        date = self.edtDate.date()

        try:
            result = formatDocumentNumber2Int(format,
                                              value,
                                              clientId,
                                              date
                                             )
        except Exception, e:
            result = u'Ошибка: '+ exceptionToUnicode(e)
        self.lblResult.setText(result)


    @pyqtSignature('')
    def on_btnAddValue_clicked(self):
        self.addFormat('{value}')


    @pyqtSignature('')
    def on_btnAddValue06_clicked(self):
        self.addFormat('{value:06}')


    @pyqtSignature('')
    def on_btnAddClientId_clicked(self):
        self.addFormat('{clientId}')


    @pyqtSignature('')
    def on_btnAddClientId2_clicked(self):
        self.addFormat('{clientId.2}')


    @pyqtSignature('')
    def on_btnAddYear_clicked(self):
        self.addFormat('{year}')


    @pyqtSignature('')
    def on_btnAddMonth_clicked(self):
        self.addFormat('{month:02}')


    @pyqtSignature('')
    def on_btnAddDay_clicked(self):
        self.addFormat('{day:02}')
