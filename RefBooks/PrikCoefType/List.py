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
from PyQt4.QtCore import QVariant, pyqtSignature, QDate

from Exchange.Utils import dbfCheckNames

from library.InDocTable import CTextInDocTableCol, CRecordListModel
from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog
from library.TableModel import CEnumCol, CDesignationCol, CDateCol
from library.Utils import forceInt, forceString, forceRef, forceDouble, toVariant, forceDate
from library.dbfpy.dbf import Dbf
from library.interchange import setDateEditValue, getDateEditValue, setRBComboBoxValue, getRBComboBoxValue

from RefBooks.PrikCoefType.Ui_PrikCoefTypeEditorDialog import Ui_PrikCoefTypeEditorDialog

class CRBPrikCoefTypeList(CItemsListDialog):
    def __init__(self, parent):
        CItemsListDialog.__init__(self, parent, [CEnumCol(u'Тип коэффициента', ['coefficientType'],
                                                          ['', u'К1 | Поправочный коэффициент подушевого финансирования',
                                                           u'К2 | Поправочный коэффициент стоимости пролеченных больных'],
                                                          1), CDesignationCol(u'Плательщик', ['organisation_id'], (
        'Organisation', 'CONCAT(infisCode, \' | \', shortName)'), 8),
                                                 CDateCol(u'Дата начала', ['begDate'], 10),
                                                 CDateCol(u'Дата окончания', ['endDate'], 10)],
                                  'soc_prikCoefType', 'begDate')
        self.setWindowTitleEx(u'Поправочные коэффициенты')
        self.tblItems.addPopupRecordProperies()
        self.tblItems.addPopupDelRow()
        self.mapOgrnToOrgId = {}
        self.mapBookkeeperCodeToName = {}
        self.mapK2 = {}

    def preSetupUi(self):
        CItemsListDialog.preSetupUi(self)
        self.addObject('btnImport', QtGui.QPushButton(u'Импорт', self))

    def postSetupUi(self):
        CItemsListDialog.postSetupUi(self)
        self.buttonBox.addButton(self.btnImport, QtGui.QDialogButtonBox.ActionRole)
        self.btnEdit.setText(u'Открыть')
        self.btnNew.setVisible(False)
        self.btnPrint.setVisible(False)

    def getItemEditor(self):
        return CRBPrikCoefTypeEditor(self)

    @pyqtSignature('')
    def on_btnImport_clicked(self):
        def importK2(row):
            ogrn = forceString(row['PL_OGRN'])
            yaer = forceInt(row['YEARS'])
            month = forceInt(row['MONTHS'])

            bookkeeperCode = forceString(row['CODE_MO'])
            coeff = forceDouble(row['COEFF'])

            record = self.mapK2.get((ogrn, yaer, month), None)
            if not record:
                orgId = self.getOrganisationId(ogrn)
                begDate = QDate(yaer, month, 1)
                endDate = begDate.addMonths(1).addDays(-1)
                cond = [table['coefficientType'].eq(2), table['organisation_id'].eq(orgId),
                        table['begDate'].eq(begDate), table['endDate'].eq(endDate)]
                record = db.getRecordEx(table, '*', cond)
                if not record:
                    record = table.newRecord()
                    record.setValue('coefficientType', 2)
                    record.setValue('organisation_id', orgId)
                    record.setValue('begDate', toVariant(begDate))
                    record.setValue('endDate', toVariant(endDate))
                    db.insertRecord(table, record)
                    self.mapK2[(ogrn, yaer, month)] = record
            # -------------------------
            masterId = forceRef(record.value('id'))
            recordItem = db.getRecordEx(tableItem, '*', [tableItem['master_id'].eq(masterId),
                                                         tableItem['bookkeeperCode'].eq(bookkeeperCode)])
            if not recordItem:
                recordItem = tableItem.newRecord()
                recordItem.setValue('master_id', masterId)
                recordItem.setValue('bookkeeperCode', bookkeeperCode)
                name = self.mapBookkeeperCodeToName.get(bookkeeperCode, None)
                if not name:
                    name = forceString(db.translate('OrgStructure', 'bookkeeperCode', bookkeeperCode, 'name'))
                    self.mapBookkeeperCodeToName[bookkeeperCode] = name
                recordItem.setValue('orgStructure_name', name)

            recordItem.setValue('value', toVariant(coeff))
            db.insertOrUpdate(tableItem, recordItem)
            db.insertOrUpdate(table, record)

        def importK3(row):
            ogrn = forceString(row['PL_OGRN'])
            ns = forceInt(row['NS'])
            sn = forceInt(row['SN'])
            uid = forceInt(row['UID'])
            dats = forceDate(row['DATS'])
            coef = forceDouble(row['SUMM'])
            stmt = u"""UPDATE Account_Item ai
  left JOIN Account a ON ai.master_id = a.id
  left JOIN Organisation o ON o.id = a.payer_id
  set ai.note = 'K3={coef}'
WHERE o.OGRN = '{ogrn}' 
    AND ai.event_id = {sn} 
    AND a.number = '{ns}' 
    AND a.date = {dats} 
    AND {uid} IN (ai.event_id, ai.visit_id, ai.action_id) 
    AND ai.deleted = 0 
    AND a.deleted = 0;""".format(coef=coef, ogrn=ogrn, ns=ns, sn=sn, dats=db.formatDate(dats), uid=uid)
            db.query(stmt)

        def importK0(row):
            ogrn = forceString(row['PL_OGRN'])
            uid = forceInt(row['UID'])
            month = forceInt(row['MONTHS'])
            year = forceInt(row['YEARS'])
            coef = forceDouble(row['SUMM'])
            dats = QDate(year, month, 1)
            dats = dats.addMonths(1).addDays(-1)

            stmt = u"""UPDATE Account_Item ai
      left JOIN Account a ON ai.master_id = a.id
      left JOIN Organisation o ON o.id = a.payer_id
      set ai.note = 'K0={coef}'
    WHERE o.OGRN = '{ogrn}' 
        AND a.date = {dats} 
        AND {uid} IN (ai.event_id, ai.visit_id, ai.action_id) 
        AND ai.deleted = 0 
        AND a.deleted = 0;""".format(coef=coef, ogrn=ogrn, dats=db.formatDate(dats), uid=uid)
            db.query(stmt)

        db = QtGui.qApp.db
        self.mapK2 = {}
        requiredFieldsK2 = ['CODE_MO', 'PL_OGRN', 'YEARS', 'MONTHS', 'COEFF']
        requiredFieldsK3 = ['CODE_MO', 'NS', 'SN', 'DATS', 'PL_OGRN', 'VP', 'KUSL', 'UID', 'YEARS', 'MONTHS', 'SUMM']
        requiredFieldsK0 = ['CODE_MO', 'CODE_UR', 'UID', 'TARU', 'SUMM', 'PL_OGRN', 'MONTHS', 'YEARS']
        table = db.table('soc_prikCoefType')
        tableItem = db.table('soc_prikCoefItem')
        filter = u'DBF (*.dbf)'
        fileName = QtGui.QFileDialog.getOpenFileName(self, u'Укажите файл с данными', '', filter)
        fileName = forceString(fileName)
        if not fileName:
            return

        dbf = Dbf(fileName, readOnly=True, encoding='cp866')
        if dbfCheckNames(dbf, requiredFieldsK3):
            importMessage = u'Импорт поправочных коэффициентов K3 завершен успешно'
            importFunc = importK3
        elif dbfCheckNames(dbf, requiredFieldsK2):
            importMessage = u'Импорт поправочных коэффициентов K2 завершен успешно'
            importFunc = importK2
        elif dbfCheckNames(dbf, requiredFieldsK0):
            importMessage = u'Импорт поправочных коэффициентов K0 завершен успешно'
            importFunc = importK0
        else:
            QtGui.QMessageBox.critical(self, u'Внимание!', u'В импортируемом файле отсуствуют необходимые поля. Импорт невозможен!', QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            return
        try:
            QtGui.qApp.setWaitCursor()
            for row in dbf:
                importFunc(row)
                QtGui.qApp.processEvents()
        finally:
            QtGui.qApp.restoreOverrideCursor()
        QtGui.QMessageBox.information(self, u'Импорт', importMessage, QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
        self.renewListAndSetTo()


    def getOrganisationId(self, ogrn):
        orgId = self.mapOgrnToOrgId.get(ogrn, None)
        if not orgId:
            table = QtGui.qApp.db.table('Organisation')
            cond = [table['OGRN'].eq(ogrn),
                    table['deleted'].eq(0),
                    table['infisCode'].ne(''),
                    table['isInsurer'].eq(1),
                    table['compulsoryServiceStop'].eq(0),
                    table['head_id'].isNull()]
            record = QtGui.qApp.db.getRecordEx(table, 'id', cond)
            if record:
                orgId = forceRef(record.value('id'))
                self.mapOgrnToOrgId[ogrn] = orgId
        return orgId



class CRBPrikCoefTypeEditor(CItemEditorBaseDialog, Ui_PrikCoefTypeEditorDialog):
    def __init__(self, parent):
        CItemEditorBaseDialog.__init__(self, parent, 'soc_prikCoefType')
        self.setReadOnly()
        self.addModels('PrikCoefItem', CPrikCoefItemModel(self))
        self.setupUi(self)
        self.tblPrikCoefItem.setModel(self.modelPrikCoefItem)
        self.setupDirtyCather()
        self.setWindowTitleEx(u'Поправочные коэффициенты')

    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        setRBComboBoxValue(self.cmbInsurer, record, 'organisation_id')

        # setComboBoxValue(self.cmbCoefType, record, 'coefficientType')
        self.cmbCoefType.setCurrentIndex(0 if forceInt(record.value('coefficientType')) == 2 else None)

        setDateEditValue(self.edtBegDate, record, 'begDate')
        setDateEditValue(self.edtEndDate, record, 'endDate')

        self.modelPrikCoefItem.loadData(self.itemId())
        self.setIsDirty(False)

    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        getRBComboBoxValue(self.cmbInsurer, record, 'organisation_id')

        # getComboBoxValue(self.cmbCoefType, record, 'coefficientType')
        record.setValue('coefficientType', QVariant(2 if self.cmbCoefType.currentIndex() == 0 else 0))

        getDateEditValue(self.edtBegDate, record, 'begDate')
        getDateEditValue(self.edtEndDate, record, 'endDate')
        return record

    def checkDataEntered(self):
        return True

    def saveInternals(self, id):
        self.modelPrikCoefItem.saveItems(id)


class CPrikCoefItemModel(CRecordListModel):
    def __init__(self, parent):
        CRecordListModel.__init__(self, parent)
        self.addCol(CTextInDocTableCol(u'Код ОМС', 'bookkeeperCode', 20)).setReadOnly()
        self.addCol(CTextInDocTableCol(u'Наименование подразделения', 'orgStructure_name', 60)).setReadOnly()
        self.addCol(CTextInDocTableCol(u'Значение', 'value', 40)).setReadOnly()

    def loadData(self, masterId):
        if masterId:
            db = QtGui.qApp.db
            stmt = """select bookkeeperCode,
            orgStructure_name,
            CONVERT(value, char) AS value
            FROM soc_prikCoefItem
            WHERE master_id = {0};""".format(masterId)
            query = db.query(stmt)
            items = []
            while query.next():
                items.append(query.record())
            self.setItems(items)
        else:
            self.clearItems()
