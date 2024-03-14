# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2015-2017 SAMSON Group. All rights reserved.
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

from library.Calendar    import monthName, dowName
from library.interchange import getLineEditValue, getSpinBoxValue, setLineEditValue, setSpinBoxValue
from library.Utils       import forceInt

from library.TableModel  import CEnumCol, CIntCol, CTextCol
from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog

from preferences.Ui_CalendarExceptionListDialog import Ui_CalendarExceptionListDialog
from preferences.Ui_CalendarExceptionDialog     import Ui_CalendarExceptionDialog


class CCalendarExceptionList(Ui_CalendarExceptionListDialog, CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [
            CTextCol(u'Наименование', ('name', ), 20),

            CIntCol( u'НГод',  ('begYear', ), 6),
            CIntCol( u'КГод',  ('endYear', ), 6),
            CEnumCol(u'Месяц', ('month', ), monthName, 12, 'l'),
            CIntCol( u'День',  ('day', ),   6),
            CEnumCol(u'Числить как', ('dow', ), dowName, 12, 'l'),
            CTextCol(u'Примечание', ('note', ), 20),
            ], 'CalendarException',
            ('month', 'day', 'begYear', 'endYear'))
        self.setWindowTitleEx(u'Календарные исключения')

        self.tblItems.addPopupDelRow()

        self.chkYearFilter.blockSignals(True)
        self.edtYear.blockSignals(True)

        self.chkYearFilter.setChecked(True)
        self.edtYear.setValue( QDate.currentDate().addMonths(1).year())
        self.edtYear.setEnabled(True)

        self.chkYearFilter.blockSignals(False)
        self.edtYear.blockSignals(False)


    def getItemEditor(self):
        return CCalendarExceptionEditor(self)


    def select(self, props):
        table = self.model.table()
        cond  = [table['deleted'].eq(0)]
        if self.chkYearFilter.isChecked():
            year = self.edtYear.value()
            cond.append(table['begYear'].le(year))
            cond.append(table['endYear'].ge(year))
        return QtGui.qApp.db.getIdList(table, 'id', where=cond, order=self.order)


    @pyqtSignature('bool')
    def on_chkYearFilter_toggled(self, val):
        self.renewListAndSetTo(self.currentItemId())


    @pyqtSignature('int')
    def on_edtYear_valueChanged(self, val):
        self.renewListAndSetTo(self.currentItemId())


    @pyqtSignature('')
    def on_btnPrint_clicked(self):
        tbl=self.tblItems
        tbl.setReportHeader(u'Календарные исключения')
        if self.chkYearFilter.isChecked():
            tbl.setReportDescription(u'Только %d год\n' % self.edtYear.value())
        else:
            tbl.setReportDescription('')
        tbl.printContent()


class CCalendarExceptionEditor(CItemEditorBaseDialog, Ui_CalendarExceptionDialog):
    def __init__(self,  parent):
        CItemEditorBaseDialog.__init__(self, parent, 'CalendarException')

        self.setupUi(self)

        year = QDate.currentDate().addMonths(1).year()
        self.edtBegYear.setValue(year)
        self.edtEndYear.setValue(year)
        self.chkEndYearDiffer.setChecked(False)


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setLineEditValue(self.edtName,        record, 'name')
        setSpinBoxValue( self.edtDay,         record, 'day')
        self.cmbMonth.setCurrentIndex(forceInt(record.value('month'))-1)
        setSpinBoxValue(self.edtBegYear,      record, 'begYear')
        setSpinBoxValue(self.edtEndYear,      record, 'endYear')
        self.cmbDow.setCurrentIndex(forceInt(record.value('dow'))-1)
        self.chkEndYearDiffer.setChecked(self.edtBegYear.value() != self.edtEndYear.value())
        self.setIsDirty(False)


    def checkDataEntered(self):
        result = True
        return result


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getLineEditValue(self.edtName,         record, 'name')
        getSpinBoxValue( self.edtDay,          record, 'day')
        record.setValue('month', self.cmbMonth.currentIndex()+1 )
        getSpinBoxValue(self.edtBegYear,       record, 'begYear')
        if self.chkEndYearDiffer.isChecked():
            getSpinBoxValue(self.edtEndYear,   record, 'endYear')
        else:
            getSpinBoxValue(self.edtBegYear,   record, 'endYear')
        record.setValue('dow', self.cmbDow.currentIndex()+1 )
        return record


    def setupMaxDay(self):
        month = self.cmbMonth.currentIndex()+1
        if month != 2:
            maxDay = QDate(2000, month, 1).daysInMonth()
        else:
            begYear = self.edtBegYear.value()
            endYear = self.edtEndYear.value() if self.chkEndYearDiffer.isChecked() else begYear
            if endYear-begYear>=8 or any(QDate.isLeapYear(year) for year in xrange(begYear, endYear+1)):
                maxDay = 29
            else:
                maxDay = 28
        self.edtDay.setMaximum(maxDay)


    @pyqtSignature('int')
    def on_edtBegYear_valueChanged(self, val):
        if self.chkEndYearDiffer.isChecked():
            if self.edtEndYear.value()<val:
                self.edtEndYear.setValue(val)
        else:
            self.edtEndYear.setValue(val)
        self.setupMaxDay()


    @pyqtSignature('')
    def on_chkEndYearDiffer_toggled(self, val):
        if val:
            pass
        else:
            self.edtEndYear.setValue(self.edtBegYear.value())
        self.setupMaxDay()


    @pyqtSignature('int')
    def on_edtEndYear_valueChanged(self, val):
        if self.edtBegYear.value()>val:
                self.edtBegYear.setValue(val)
        self.setupMaxDay()


    @pyqtSignature('int')
    def on_cmbMonth_currentIndexChanged(self, index):
        self.setupMaxDay()
