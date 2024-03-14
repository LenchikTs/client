# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4                      import QtGui
from PyQt4.QtCore               import Qt, QDate, pyqtSignature, QModelIndex

from library.DialogBase         import CDialogBase
from library.database           import CTableRecordCache
from library.Utils              import (
                                         forceBool,
                                         forceDate,
                                         forceInt,
                                         forceRef,
                                         forceString,
                                         toVariant,
                                       )
from RefBooks.TempInvalidState  import CTempInvalidState
from Registry.RegistryTable     import CExpertTempInvalidTableModel
from Registry.Utils             import getRightEditTempInvalid


from DataCheck.Ui_CheckTempInvalidEditDialog   import Ui_CheckTempInvalidEditDialog


class CCheckTempInvalidEditDialog(CDialogBase, Ui_CheckTempInvalidEditDialog):
    def __init__(self,  parent):
        CDialogBase.__init__(self, parent)
        self.addModels('ExpertTempInvalid', CExpertTempInvalidTableModel(self, CTableRecordCache(QtGui.qApp.db, QtGui.qApp.db.forceTable('Client'), u'*', capacity=None)))
        self.addObject('actExpertTempInvalidUpdate', QtGui.QAction(u'Исправить эпизод', self))
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setWindowTitleEx(u'Контроль и исправление документов ВУТ')
        self.setModels(self.tblExpertTempInvalid, self.modelExpertTempInvalid, self.selectionModelExpertTempInvalid)
        self.tblExpertTempInvalid.createPopupMenu([self.actExpertTempInvalidUpdate])
        self.modelExpertTempInvalid.setIdList([])
        self.abortProcess = False
        self.checkRun = False
        self.edtBegDate.setDate(QDate.currentDate())
        self.edtEndDate.setDate(QDate.currentDate())


    def checkTempInvalidData(self):
        self.checkRun = True
        tempInvalidIdList = []
        doctype = self.cmbDoctype.currentIndex()
        begDate = self.edtBegDate.date()
        endDate = self.edtEndDate.date()
        db = QtGui.qApp.db
        table1 = db.table('TempInvalid').alias('T1')
        table2 = db.table('TempInvalid').alias('T2')
        queryTable = table1.innerJoin(table2, table2['client_id'].eq(table1['client_id']))
        cond = [table1['doctype'].eq(doctype),
                table2['doctype'].eq(doctype),
                table1['deleted'].eq(0),
                table2['deleted'].eq(0),
                table1['state'].ne(CTempInvalidState.extended),
                table2['state'].ne(CTempInvalidState.extended),
                table1['id'].ne(table2['id']),
                table1['endDate'].eq(table2['begDate']),
                ]
        if begDate:
            cond.append(table1['begDate'].dateGe(begDate))
        if endDate:
            cond.append(table1['begDate'].dateLe(endDate))
        tempInvalidIdList = db.getDistinctIdList(queryTable, [table1['id']], cond, [table1['begDate'].name(), table2['endDate'].name()], limit = 1000)
        self.checkRun = False
        self.abortProcess = False
        self.modelExpertTempInvalid.setIdList(tempInvalidIdList)
        self.lblCountRecords.setText(u'Всего записей: ' + forceString(len(tempInvalidIdList)))


    @pyqtSignature('')
    def on_tblExpertTempInvalid_popupMenuAboutToShow(self):
        tempInvalidId = self.tblExpertTempInvalid.currentItemId()
        self.actExpertTempInvalidUpdate.setEnabled(bool(tempInvalidId))


    @pyqtSignature('')
    def on_actExpertTempInvalidUpdate_triggered(self):
        tempInvalidId = self.tblExpertTempInvalid.currentItemId()
        if tempInvalidId and getRightEditTempInvalid(tempInvalidId):
            QtGui.qApp.callWithWaitCursor(self, self.updateTempInvalid, tempInvalidId)


    def updateTempInvalid(self, tempInvalidId):
        record = self.modelExpertTempInvalid.getRecordById(tempInvalidId)
        if not record:
            return
        db = QtGui.qApp.db
        begDate = forceDate(record.value('begDate'))
        endDate = forceDate(record.value('endDate'))
        caseBegDate = forceDate(record.value('caseBegDate'))
#        state = forceInt(record.value('state'))
        clientId = forceRef(record.value('client_id'))
        resultId = forceRef(record.value('result_id'))
        type = forceInt(record.value('type'))
        able = forceBool(db.translate('rbTempInvalidResult', 'id', resultId, 'able'))
        record.setValue('state', toVariant(CTempInvalidState.extended))
        table = db.table('TempInvalid')
        cond = [table['deleted'].eq(0),
                table['client_id'].eq(clientId),
                table['state'].notInlist([CTempInvalidState.closed, CTempInvalidState.transferred]),
                db.joinOr([table['endDate'].dateEq(begDate), table['endDate'].dateEq(begDate.addDays(-1))])
                ]
        recordPrev = db.getRecordEx(table, '*', cond, 'TempInvalid.endDate DESC')
        if recordPrev:
            caseBegDatePrev = forceDate(recordPrev.value('caseBegDate'))
            if caseBegDatePrev and caseBegDatePrev != caseBegDate:
                record.setValue('caseBegDate', toVariant(caseBegDatePrev))
        else:
            cond = [table['deleted'].eq(0),
                    table['client_id'].eq(clientId),
                    db.joinOr([table['begDate'].dateEq(endDate), table['begDate'].dateEq(endDate.addDays(1))])
                    ]
            recordNext = db.getRecordEx(table, '*', cond, 'TempInvalid.begDate')
            if recordNext:
                caseBegDateNext = forceDate(recordNext.value('caseBegDate'))
                if caseBegDateNext and caseBegDateNext < caseBegDate:
                    record.setValue('caseBegDate', toVariant(caseBegDateNext))
        if able or not resultId:
            tableResult = db.table('rbTempInvalidResult')
            cond = [tableResult['code'].eq(u'31'),
                    tableResult['name'].like(u'нетрудоспособен'),
                    tableResult['type'].eq(type),
                    tableResult['able'].eq(0)
                    ]
            recordAble = db.getRecordEx(tableResult, 'id', cond)
            if recordAble:
                resultIdAble = forceRef(recordAble.value('id'))
                if resultIdAble:
                   record.setValue('result_id', toVariant(resultIdAble))
        updateId = db.updateRecord(table, record)
        if updateId:
            row = self.tblExpertTempInvalid.currentRow()
            self.modelExpertTempInvalid.beginRemoveRows(QModelIndex(), row, row)
            del self.modelExpertTempInvalid.idList()[row]
            self.modelExpertTempInvalid.endRemoveRows()
            self.modelExpertTempInvalid.emitItemsCountChanged()


    @pyqtSignature('')
    def on_btnStart_clicked(self):
        self.prbCheckTempInvalid.setFormat('%v')
        self.prbCheckTempInvalid.setValue(0)
        self.btnClose.setText(u'Прервать')
        self.btnStart.setEnabled(False)
        self.lblCountRecords.setText(u'Всего записей: 0')
        try:
            QtGui.qApp.callWithWaitCursor(self, self.checkTempInvalidData)
        except Exception:
            self.abortProcess = True
        self.prbCheckTempInvalid.setText(u'Прервано' if self.abortProcess else u'Готово')
        self.btnClose.setText(u'Закрыть')
        self.btnStart.setEnabled(True)
        self.checkRun = False
        self.abortProcess = False


    @pyqtSignature('')
    def on_btnClose_clicked(self):
        if self.checkRun:
            self.abortProcess = True
        else:
            self.close()

