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
u"""Экспорт номенклатуры в XML"""

from PyQt4 import QtGui
from PyQt4.QtCore import QDate, pyqtSignature, SIGNAL, QFile

from Exchange.AbstractExportXmlStreamWriter import CAbstractExportXmlStreamWriter
from Exchange.Utils import tbl
from Stock.StockDialog import CMyMotionsModel, CMyRequisitionsModel
from Stock.StockMotion import stockMotionType

from library.DialogBase import CDialogBase
from library.Utils import (smartDict, forceInt, toVariant, forceRef,
                           forceString, anyToUnicode, exceptionToUnicode)

from StockMotionTypeComboBox import getStockMotionTypeIds
from Ui_exportDialog import Ui_ExportDialog


class CExportDialog(CDialogBase, Ui_ExportDialog):
    _indexes = [] + getStockMotionTypeIds()

    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.motionsFilter = smartDict()
        self.requisitionsFilter = smartDict()
        self.fileName = None

        self.addModels('Requisitions', CMyRequisitionsModel(self))
        self.addModels('Motions', CMyMotionsModel(self))
        self.addObject('actSelectAllRow',
                       QtGui.QAction(u'Выделить все строки', self))
        self.addObject('actClearSelectionRow',
                       QtGui.QAction(u'Снять выделение', self))
        self.addObject('actSelectAllRequisitions',
                       QtGui.QAction(u'Выделить все строки', self))
        self.addObject('actClearRequisitionsSelectionRow',
                       QtGui.QAction(u'Снять выделение', self))
        self.setupUi(self)

        self.tblMotions.setModel(self.modelMotions)
        self.tblMotions.setSelectionModel(self.selectionModelMotions)
        self.tblMotions.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.tblMotions.addPopupAction(self.actSelectAllRow)
        self.connect(self.actSelectAllRow, SIGNAL('triggered()'),
                     self.selectAllRowTblItem)
        self.tblMotions.addPopupAction(self.actClearSelectionRow)
        self.connect(self.actClearSelectionRow, SIGNAL('triggered()'),
                     self.clearSelectionRow)

        self.tblRequisitions.setModel(self.modelRequisitions)
        self.tblRequisitions.setSelectionModel(self.selectionModelRequisitions)
        self.tblRequisitions.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.tblRequisitions.addPopupAction(self.actSelectAllRequisitions)
        self.connect(self.actSelectAllRequisitions, SIGNAL('triggered()'),
        self.selectAllRequisitions)
        self.tblRequisitions.addPopupAction(self.actClearRequisitionsSelectionRow)
        self.connect(self.actClearRequisitionsSelectionRow,
                     SIGNAL('triggered()'), self.clearRequisitionsSelectionRow)


    def updateMotionsList(self, currentId=None):
        filter = self.motionsFilter
        db = QtGui.qApp.db
        table = db.table('StockMotion')
        cond = [
            table['deleted'].eq(0),
        ]

        if filter.begDate:
            cond.append(table['date'].ge(filter.begDate))
        if filter.endDate:
            cond.append(table['date'].lt(filter.endDate.addDays(1)))
        if filter.supplierId:
            cond.append(table['supplier_id'].eq(filter.supplierId))
        if filter.receiverId:
            cond.append(table['receiver_id'].eq(filter.receiverId))
        if filter.type >=0:
            cond.append(table['type'].eq(filter.type))
        else:
            cond.append(table['type'].inlist(self._indexes))

        cols = [u'IF(StockMotion.`client_id`, StockMotion.`client_id`, StockMotion.`id`) as ident',
                    table['id'],
                    table['type'],
                    table['number'],
                    table['date'],
                    table['reason'],
                    table['supplierOrg_id'],
                    table['supplier_id'],
                    table['receiver_id'],
                    table['client_id'],
                    table['note'],
                    ]

        cols.append(u'StockMotion.`id` as idList')
        records = db.getRecordList(table, cols, where=cond)

        idList = []

        if records:
            for record in records:
                id = forceInt(record.value('id'))
                idList.append(id)
        self.modelMotions.setRecords(records)
        self.tblMotions.setIdList(idList)


    def updateRequisitionsList(self):
        db = QtGui.qApp.db
        table = db.table('StockRequisition')

        cond = [
            table['deleted'].eq(0),
        ]
        filter = self.requisitionsFilter

        if filter.begDate:
            cond.append(table['date'].ge(filter.begDate))
        if filter.endDate:
            cond.append(table['date'].lt(filter.endDate.addDays(1)))
        if filter.supplierId:
            cond.append(table['supplier_id'].eq(filter.supplierId))
        if filter.recipientId:
            cond.append(table['recipient_id'].eq(filter.recipientId))

        idList = db.getIdList(table, where=cond)
        self.tblRequisitions.setIdList(idList)


    def resetMotionsFilter(self):
        self.edtMotionsFilterBegDate.setDate(QDate.currentDate().addDays(-7))
        self.edtMotionsFilterEndDate.setDate(QDate())
        self.cmbMotionsFilterSupplier.setValue(None)
        self.cmbMotionsFilterReceiver.setValue(None)
        self.cmbMotionsFilterType.setCurrentIndex(0)


    def applyMotionsFilter(self):
        filter = self.motionsFilter
        filter.begDate = self.edtMotionsFilterBegDate.date()
        filter.endDate = self.edtMotionsFilterEndDate.date()
        filter.supplierId = self.cmbMotionsFilterSupplier.value()
        filter.receiverId = self.cmbMotionsFilterReceiver.value()
        idx = self.cmbMotionsFilterType.currentIndex()
        name = forceString(self.cmbMotionsFilterType.itemText(idx))
        filter.type = [key for key, val in stockMotionType.items() if val[0] == name][0] if idx else None
        self.updateMotionsList()


    def resetRequisitionsFilter(self):
        self.edtRequisitionsFilterBegDate.setDate(QDate.currentDate().addDays(-7))
        self.edtRequisitionsFilterEndDate.setDate(QDate())
        self.cmbRequisitionsFilterSupplier.setValue(None)
        self.cmbRequisitionsFilterRecipient.setValue(None)


    def applyRequisitionsFilter(self):
        filter = self.requisitionsFilter
        filter.begDate = self.edtRequisitionsFilterBegDate.date()
        filter.endDate = self.edtRequisitionsFilterEndDate.date()
        filter.supplierId = self.cmbRequisitionsFilterSupplier.value()
        filter.recipientId = self.cmbRequisitionsFilterRecipient.value()
        self.updateRequisitionsList()


    def exec_(self):
        self.resetMotionsFilter()
        self.applyMotionsFilter()
        self.resetRequisitionsFilter()
        self.applyRequisitionsFilter()
        CDialogBase.exec_(self)


    def selectAllRowTblItem(self):
        self.tblMotions.selectAll()


    def clearSelectionRow(self):
        self.tblMotions.clearSelection()


    def selectAllRequisitions(self):
        self.tblRequisitions.selectAll()


    def clearRequisitionsSelectionRow(self):
        self.tblRequisitions.clearSelection()


    @pyqtSignature('')
    def on_btnMotionsFilterApply_clicked(self):
        self.applyMotionsFilter()


    @pyqtSignature('')
    def on_btnMotionsFilterReset_clicked(self):
        self.resetMotionsFilter()


    @pyqtSignature('')
    def on_btnRequisitionsFilterApply_clicked(self):
        self.applyRequisitionsFilter()


    @pyqtSignature('')
    def on_btnRequisitionsFilterReset_clicked(self):
        self.resetRequisitionsFilter()


    @pyqtSignature('')
    def on_btnExport_clicked(self):
        xmlWriter = CXmlWriter(self)
        xmlWriter.fileName = self.fileName
        xmlWriter.idList = self.tblMotions.selectedItemIdList()
        xmlWriter.requisitionsIdList = self.tblRequisitions.selectedItemIdList()

        if xmlWriter.work():
            QtGui.QMessageBox.information(self,
                u'Экспорт документов',
                u'Файл {0} успешно сохранен'.format(self.fileName),
                QtGui.QMessageBox.Ok)
        else:
            QtGui.QMessageBox.critical(self,
                u'Произошла ошибка ввода-вывода', xmlWriter.errorString(),
                QtGui.QMessageBox.Close)


class CXmlWriter(CAbstractExportXmlStreamWriter):
    rbFields = ('CODE', 'NAME')
    nomenclatureSubGroup = {
        'STOCK_UNIT': {'fields': rbFields},
        'CLIENT_UNIT': {'fields': rbFields},
    }
    itemSubGroup = {
        'NOMENCLATURE' : {'fields': ('ID', 'CODE', 'TN_R', 'STOCK_UNIT',
                                     'CLIENT_UNIT', 'UNIT_RATIO'),
                          'subGroup': nomenclatureSubGroup},
        'UNIT': {'fields': rbFields},
    }
    itemFields = ('ID', 'NOMENCLATURE', 'BATCH', 'SHELF_TIME', 'FINANCE', 'MAK',
                  'QNT', 'UNIT', 'SUM')
    itemDateFields = ('SHELF_TIME', )
    docFields = ('ID', 'TYPE', 'NUMBER', 'DATE', 'REASON', 'REASON_DATE',
                 'SUPPLIER_ORG', 'SUP_ORG_PERSON', 'SUPPLIER', 'SUP_PERSON',
                 'RECEIVER', 'REC_PERSON', 'CANCEL_REASON', 'NOTE')
    docDateFields = ('DATE', 'REASON_DATE')
    docSubGroup = {
        'SUPPLIER_ORG': {'fields': ('NAME', 'SHORT_NAME', 'OGRN', 'INN', 'KPP',
                                    'ADDRESS')},
        'SUPPLIER': {'fields': rbFields},
        'SUP_PERSON': {'fields': ('ID', 'LASTN', 'FIRSTN', 'PATRN',
                                  'BIRTH_DATE', 'SNILS'),
                        'dateFields': ('BIRTH_DATE')},
        'RECEIVER': {'fields': rbFields},
        'REC_PERSON': {'fields': ('ID', 'LASTN', 'FIRSTN', 'PATRN',
                                  'BIRTH_DATE', 'SNILS'),
                        'dateFields': ('BIRTH_DATE')},
    }

    def __init__(self, parent):
        CAbstractExportXmlStreamWriter.__init__(self, parent)
        self.fileName = None
        self.idList = []
        self.requisitionsIdList = []
        self.tblStockMotion = tbl('StockMotion')
        self._currentDocId = None
        self._tblStockRequisition = tbl('StockRequisition')
        self._db = QtGui.qApp.db


    def query(self):
        stmt = u"""SELECT StockMotion.id AS DOC_ID,
            StockMotion.type AS DOC_TYPE,
            StockMotion.number AS DOC_NUMBER,
            StockMotion.date AS DOC_DATE,
            StockMotion.reason AS DOC_REASON,
            StockMotion.reasonDate AS DOC_REASON_DATE,
            StockMotion.supplierOrgPerson AS DOC_SUP_ORG_PERSON,
            (CASE StockMotion.type
                WHEN 4 THEN '0'
                WHEN 7 THEN rbStockMotionItemReason.code
                ELSE '' END) AS DOC_CANCEL_REASON,
            StockMotion.note AS DOC_NOTE,
            SupplierOrg.fullName AS SUPPLIER_ORG_NAME,
            SupplierOrg.shortName AS SUPPLIER_ORG_SHORT_NAME,
            SupplierOrg.OGRN AS SUPPLIER_ORG_OGRN,
            SupplierOrg.INN AS SUPPLIER_ORG_INN,
            SupplierOrg.KPP AS SUPPLIER_ORG_KPP,
            SupplierOrg.Address AS SUPPLIER_ORG_ADDRESS,
            Supplier.name AS SUPPLIER_NAME,
            SupplierIdentification.value AS SUPPLIER_CODE,
            SupPersonIdentification.value AS SUP_PERSON_ID,
            SupPerson.lastName AS SUP_PERSON_LASTN,
            SupPerson.firstName AS SUP_PERSON_FIRSTN,
            SupPerson.patrName AS SUP_PERSON_PATRN,
            SupPerson.birthDate AS SUP_PERSON_BIRTH_DATE,
            SupPerson.SNILS AS SUP_PERSON_SNILS,
            ReceiverIdentification.value AS RECEIVER_CODE,
            Receiver.name AS RECEIVER_NAME,
            RecPersonIdentification.value AS REC_PERSON_ID,
            RecPerson.lastName AS REC_PERSON_LASTN,
            RecPerson.firstName AS REC_PERSON_FIRSTN,
            RecPerson.patrName AS REC_PERSON_PATRN,
            RecPerson.birthDate AS REC_PERSON_BIRTH_DATE,
            RecPerson.SNILS AS REC_PERSON_SNILS,
            0 AS ITEM_ID,
            StockMotion_Item.batch AS ITEM_BATCH,
            StockMotion_Item.shelfTime AS ITEM_SHELF_TIME,
            rbFinance.code AS ITEM_FINANCE,
            StockMotion_Item.qnt AS ITEM_QNT,
            StockMotion_Item.sum AS ITEM_SUM,
            (SELECT rbMedicalAidKind.code
             FROM rbMedicalAidKind
             WHERE rbMedicalAidKind.id = StockMotion_Item.medicalAidKind_id
            ) AS ITEM_MAK,
            rbNomenclature.code AS NOMENCLATURE_ID,
            rbNomenclature.code AS NOMENCLATURE_CODE,
            rbNomenclature.name AS NOMENCLATURE_TN_R,
            rbNomenclature_UnitRatio.ratio AS NOMENCLATURE_UNIT_RATIO,
            IFNULL((SELECT value FROM rbUnit_Identification
             WHERE deleted = 0
               AND system_id IN (SELECT id FROM rbAccountingSystem
                                 WHERE code = 'WMS_unit')
               AND master_id = rbUnit.id
             LIMIT 1), rbUnit.code) AS UNIT_CODE,
            rbUnit.name AS UNIT_NAME,
            IFNULL((SELECT value FROM rbUnit_Identification
             WHERE deleted = 0
               AND system_id IN (SELECT id FROM rbAccountingSystem
                                 WHERE code = 'WMS_unit')
               AND master_id = StockUnit.id
             LIMIT 1), StockUnit.code) AS STOCK_UNIT_CODE,
            StockUnit.name AS STOCK_UNIT_NAME,
            IFNULL((SELECT value FROM rbUnit_Identification
             WHERE deleted = 0
               AND system_id IN (SELECT id FROM rbAccountingSystem
                                 WHERE code = 'WMS_unit')
               AND master_id = ClientUnit.id
             LIMIT 1), ClientUnit.code) AS CLIENT_UNIT_CODE,
            ClientUnit.name AS CLIENT_UNIT_NAME,
            SupplierOrg.id AS supplierOrgId,
            Supplier.id AS supplierId,
            Receiver.id AS receiverId
        FROM StockMotion
        LEFT JOIN Organisation AS SupplierOrg
            ON SupplierOrg.id = StockMotion.supplierOrg_id
        LEFT JOIN OrgStructure AS Supplier
            ON Supplier.id = StockMotion.supplier_id
        LEFT JOIN OrgStructure_Identification AS SupplierIdentification
            ON SupplierIdentification.id = (
                SELECT MAX(id) FROM OrgStructure_Identification OI
                WHERE OI.master_id = Supplier.id
                  AND OI.deleted = 0
                  AND OI.system_id = (
                    SELECT MAX(id) FROM rbAccountingSystem
                    WHERE code = 'WMS_warehouse'))
        LEFT JOIN Person AS SupPerson
            ON SupPerson.id = StockMotion.supplierPerson_id
        LEFT JOIN Person_Identification AS SupPersonIdentification
            ON SupPersonIdentification.id = (
                SELECT MAX(id) FROM Person_Identification PI
                WHERE PI.master_id = SupPerson.id
                  AND PI.deleted = 0
                  AND PI.system_id = (
                    SELECT MAX(id) FROM rbAccountingSystem
                    WHERE code = 'WMS_Person'))
        LEFT JOIN OrgStructure AS Receiver
            ON Receiver.id = StockMotion.receiver_id
        LEFT JOIN OrgStructure_Identification AS ReceiverIdentification
            ON ReceiverIdentification.id = (
                SELECT MAX(id) FROM OrgStructure_Identification OI
                WHERE OI.master_id = Receiver.id
                  AND OI.deleted = 0
                  AND OI.system_id = (
                    SELECT MAX(id) FROM rbAccountingSystem
                    WHERE code = 'WMS_warehouse'))
        LEFT JOIN Person AS RecPerson
            ON RecPerson.id = StockMotion.receiverPerson_id
        LEFT JOIN Person_Identification AS RecPersonIdentification
            ON RecPersonIdentification.id = (
                SELECT MAX(id) FROM Person_Identification PI
                WHERE PI.master_id = RecPerson.id
                  AND PI.deleted = 0
                  AND PI.system_id = (
                    SELECT MAX(id) FROM rbAccountingSystem
                    WHERE code = 'WMS_Person'))
        LEFT JOIN StockMotion_Item
            ON StockMotion_Item.master_id = StockMotion.id
        LEFT JOIN rbNomenclature
            ON rbNomenclature.id = StockMotion_Item.nomenclature_id
        LEFT JOIN rbFinance ON rbFinance.id = StockMotion_Item.finance_id
        LEFT JOIN rbUnit ON rbUnit.id = StockMotion_Item.unit_id
        LEFT JOIN rbNomenclature_UnitRatio ON rbNomenclature_UnitRatio.id = (
            SELECT MAX(id) FROM rbNomenclature_UnitRatio NUR
            WHERE NUR.deleted = 0 AND NUR.master_id = rbNomenclature.id)
        LEFT JOIN rbUnit AS ClientUnit ON
            ClientUnit.id = rbNomenclature.defaultClientUnit_id
        LEFT JOIN rbUnit AS StockUnit ON
            StockUnit.id = rbNomenclature.defaultStockUnit_id
        LEFT JOIN rbStockMotionItemReason ON
            StockMotion_Item.reason_id = rbStockMotionItemReason.id
        WHERE {idList} AND StockMotion_Item.deleted = 0""".format(
            idList=self.tblStockMotion['id'].inlist(self.idList))
        return self._db.query(stmt)


    def requisitionsQuery(self):
        stmt = """SELECT StockRequisition.id AS DOC_ID,
            5 AS DOC_TYPE,
            StockRequisition.number AS DOC_NUMBER,
            StockRequisition.date AS DOC_DATE,
            StockRequisition.note AS DOC_NOTE,
            Supplier.name AS SUPPLIER_NAME,
            SupplierIdentification.value AS SUPPLIER_CODE,
            ReceiverIdentification.value AS RECEIVER_CODE,
            Receiver.name AS RECEIVER_NAME,
            0 AS ITEM_ID,
            rbFinance.code AS ITEM_FINANCE,
            StockRequisition_Item.qnt AS ITEM_QNT,
            (SELECT rbMedicalAidKind.code
             FROM rbMedicalAidKind
             WHERE rbMedicalAidKind.id = StockRequisition_Item.medicalAidKind_id
            ) AS ITEM_MAK,
            rbNomenclature.code AS NOMENCLATURE_ID,
            rbNomenclature.code AS NOMENCLATURE_CODE,
            rbNomenclature.name AS NOMENCLATURE_TN_R,
            rbNomenclature_UnitRatio.ratio AS NOMENCLATURE_UNIT_RATIO,
            IFNULL((SELECT value FROM rbUnit_Identification
             WHERE deleted = 0
               AND system_id IN (SELECT id FROM rbAccountingSystem
                                 WHERE code = 'WMS_unit')
               AND master_id = rbUnit.id
             LIMIT 1), rbUnit.code) AS UNIT_CODE,
            rbUnit.name AS UNIT_NAME,
            IFNULL((SELECT value FROM rbUnit_Identification
             WHERE deleted = 0
               AND system_id IN (SELECT id FROM rbAccountingSystem
                                 WHERE code = 'WMS_unit')
               AND master_id = StockUnit.id
             LIMIT 1), StockUnit.code) AS STOCK_UNIT_CODE,
            StockUnit.name AS STOCK_UNIT_NAME,
            IFNULL((SELECT value FROM rbUnit_Identification
             WHERE deleted = 0
               AND system_id IN (SELECT id FROM rbAccountingSystem
                                 WHERE code = 'WMS_unit')
               AND master_id = ClientUnit.id
             LIMIT 1), ClientUnit.code) AS CLIENT_UNIT_CODE,
            ClientUnit.name AS CLIENT_UNIT_NAME,
            Supplier.id AS supplierId,
            Receiver.id AS receiverId
        FROM StockRequisition
        LEFT JOIN OrgStructure AS Supplier
            ON Supplier.id = StockRequisition.supplier_id
        LEFT JOIN OrgStructure AS Receiver
            ON Receiver.id = StockRequisition.recipient_id
        LEFT JOIN StockRequisition_Item
            ON StockRequisition_Item.master_id = StockRequisition.id
        LEFT JOIN OrgStructure_Identification AS SupplierIdentification
            ON SupplierIdentification.id = (
                SELECT MAX(id) FROM OrgStructure_Identification OI
                WHERE OI.master_id = Supplier.id
                  AND OI.deleted = 0
                  AND OI.system_id = (
                    SELECT MAX(id) FROM rbAccountingSystem
                    WHERE code = 'WMS_warehouse'))
        LEFT JOIN OrgStructure_Identification AS ReceiverIdentification
            ON ReceiverIdentification.id = (
                SELECT MAX(id) FROM OrgStructure_Identification OI
                WHERE OI.master_id = Receiver.id
                  AND OI.deleted = 0
                  AND OI.system_id = (
                    SELECT MAX(id) FROM rbAccountingSystem
                    WHERE code = 'WMS_warehouse'))
        LEFT JOIN rbFinance ON rbFinance.id = StockRequisition_Item.finance_id
        LEFT JOIN rbUnit ON rbUnit.id = StockRequisition_Item.unit_id
        LEFT JOIN rbNomenclature
            ON rbNomenclature.id = StockRequisition_Item.nomenclature_id
        LEFT JOIN rbNomenclature_UnitRatio ON rbNomenclature_UnitRatio.id = (
            SELECT MAX(id) FROM rbNomenclature_UnitRatio NUR
            WHERE NUR.deleted = 0 AND NUR.master_id = rbNomenclature.id)
        LEFT JOIN rbUnit AS ClientUnit ON
            ClientUnit.id = rbNomenclature.defaultClientUnit_id
        LEFT JOIN rbUnit AS StockUnit ON
            StockUnit.id = rbNomenclature.defaultStockUnit_id
        WHERE {idList}""".format(
            idList=self._tblStockRequisition['id'].inlist(
                self.requisitionsIdList))
        return self._db.query(stmt)


    def work(self):
        file = QFile(self.fileName)

        if not file.open(QFile.Text|QFile.WriteOnly):
            return False

        self.writeFile(file, (self.query(), self.requisitionsQuery()))

        file.close()
        return True


    def writeFile(self, device, queryList, progressBar=None, params=None):
        try:
            self.setDevice(device)

            if progressBar:
                progressBar.setMaximum(max(sum(q.size() for q in queryList), 1))
                progressBar.reset()
                progressBar.setValue(0)

            self.writeStartDocument()
            self.writeHeader(params)
            self.aborted = False

            for query in queryList:
                self._currentDocId = None

                while query.next():
                    self.writeRecord(query.record(), params)

                    if progressBar:
                        progressBar.step()

                    if self.aborted:
                        return False

                    QtGui.qApp.processEvents()

                if self._currentDocId:
                    self.writeEndElement() # DOC


            self.writeFooter(params)
            self.writeEndDocument()

        except IOError, e:
            QtGui.qApp.logCurrentException()
            msg = ''

            if hasattr(e, 'filename'):
                msg = u'%s:\n[Errno %s] %s' % (
                   e.filename, e.errno,
                   anyToUnicode(e.strerror))
            else:
                msg = u'[Errno %s] %s' % (e.errno,
                                          anyToUnicode(e.strerror))

            QtGui.QMessageBox.critical(self._parent,
                u'Произошла ошибка ввода-вывода', msg,
                QtGui.QMessageBox.Close)
            return False

        except Exception, e:
            QtGui.qApp.logCurrentException()
            QtGui.QMessageBox.critical(self._parent,
                u'Произошла ошибка', exceptionToUnicode(e),
                QtGui.QMessageBox.Close)
            return False

        return True

    def writeHeader(self, _):
        self.writeStartElement('LIST')


    def writeFooter(self, _):
        if self._currentDocId:
            self.writeEndElement() # DOC

        self.writeEndElement() # LIST


    def writeRecord(self, record, params):
        docId = forceInt(record.value('DOC_ID'))

        if self._currentDocId != docId:
            if self._currentDocId:
                self.writeEndElement() # DOC

            self._currentDocId = docId
            self._currentItemId = 0

            docType = forceInt(record.value('DOC_TYPE'))
            if docType == 0 and forceRef(record.value('supplierOrgId')):
                docType = 1
            elif (docType == 0 and forceRef(record.value('supplierId'))
                    and forceRef(record.value('receiverId'))):
                docType = 2
            elif docType in (4, 7, 8):
                docType = 3

            record.setValue('DOC_TYPE', toVariant(docType))

            self.writeGroup('DOC', self.docFields, record,
                            subGroup=self.docSubGroup, closeGroup=False,
                            dateFields=self.docDateFields)

        self.writeItem(record, params)


    def writeItem(self, record, params):
        self._currentItemId += 1
        record.setValue('ITEM_ID', toVariant(self._currentItemId))
        self.writeGroup('ITEM', self.itemFields, record,
                        subGroup=self.itemSubGroup,
                        dateFields=self.itemDateFields)


    def writeElement(self, elementName, value=None):
        if value:
            self.writeTextElement(elementName, value)


    def errorString(self):
        return (self.device().errorString() if self.device()
                else u'Не могу создать файл экспорта')

# ******************************************************************************
