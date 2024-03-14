# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################


from PyQt4 import QtGui
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import SIGNAL, Qt, pyqtSignature, QDate, QDateTime

from library.crbcombobox         import CRBComboBox
from library.Identification      import getIdentification, findByIdentification

from library.InDocTable          import (
                                          CBoolInDocTableCol,
                                          CDateInDocTableCol,
                                          CFloatInDocTableCol,
                                          CInDocTableCol,
                                          CRBInDocTableCol,
                                        )
from library.interchange         import (
                                          getDateEditValue,
                                          setDateEditValue,
                                          getLineEditValue,
                                          setLineEditValue,
                                          getRBComboBoxValue,
                                          setRBComboBoxValue,
                                        )
from library.PrintInfo           import CInfoContext
from library.PrintTemplates      import (
                                          applyTemplate,
                                          CPrintAction,
                                          CPrintButton,
                                          getPrintTemplates,
                                        )
from library.Utils               import (
                                          forceBool,
                                          forceDouble,
                                          forceRef,
                                          forceString,
                                          toVariant,
                                          forceInt,
#                                          forceDate,
#                                          trim,
                                        )
#from Orgs.Utils                  import getOrgStructureIdentification

from Reports.ReportBase          import CReportBase, createTable
from Reports.ReportView          import CReportViewDialog
from Stock.NomenclatureComboBox  import CNomenclatureInDocTableCol
from Stock.StockMotionBaseDialog import (
                                          CStockMotionBaseDialog,
                                          CStockMotionItemsCopyPasteMixin,
                                          CNomenclatureItemsBaseModel,
                                        )
#from Stock.StockBatchEditor      import CStockBatchEditor
from Stock.Utils                 import (
                                          getStockMotionItemQuantityColumn,
#                                          CPriceItemDelegate,
                                          CSummaryInfoModelMixin,
                                        )

from Stock.Mdlp.Logger                 import CLogger
from Stock.Mdlp.Stage                  import CMdlpStage
from Stock.Mdlp.connection             import CMdlpConnection
from Stock.Mdlp.selectIncomingInvoice  import selectIncomingInvoiceFromMdlp
from Stock.Mdlp.iidoProcess            import iidoProcess
from Stock.Mdlp.iiroProcess            import iiroProcess
from Stock.Mdlp.iinmProcess            import iinmProcess

from Ui_IncomingInvoice import Ui_IncomingInvoiceDialog


class CIncomingInvoiceEditDialog(Ui_IncomingInvoiceDialog,
                                 CStockMotionBaseDialog,
                                 CStockMotionItemsCopyPasteMixin,
                                ):
    stockDocumentType = 10 # Накладная от поставщика

    def __init__(self,  parent):
        CStockMotionBaseDialog.__init__(self, parent)
        CStockMotionItemsCopyPasteMixin.__init__(self, parent)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)

        self.addObject('btnPrint', CPrintButton(self, u'Печать'))
        self.btnPrint.setShortcut('F6')
        self.addObject('btnFill', QtGui.QPushButton(u'Заполнить', self))
        self.btnFill.setShortcut('F9')
        self.addObject('btnSelectDocumentFromMdlp', QtGui.QPushButton(u'Запросить в МДЛП', self))
        self.addObject('actOpenStockBatchEditor', QtGui.QAction(u'Подобрать параметры', self))

        self.addObject('actConfirmAll',   QtGui.QAction(u'Подтвердить все', self))
        self.addObject('actUnconfirmAll', QtGui.QAction(u'Снять подтверждение со всех', self))
        self.addObject('actPropagatePriceEtc',QtGui.QAction(u'Распространить цену и т.п.', self))

        self.addModels('Items', CItemsModel(self))
        self.setupUi(self)
        self.btnSelectDocumentFromMdlp.setEnabled(False)
        self.actConfirmAll.setEnabled(False)
        self.actUnconfirmAll.setEnabled(False)
        self.actPropagatePriceEtc.setEnabled(False)

        self.cmbReceiverPerson.setSpecialityIndependents() # Что это?
        self.cmbSupplierOrg.setFilter('isSupplier = 1')
#        self.edtSupplierOrgPerson.setEnabled(False)
        self.cmbFinance.setTable('rbFinance')

        self.tblItems.setModel(self.modelItems)
        self.prepareItemsPopupMenu(self.tblItems)
        self.tblItems.popupMenu().addSeparator()
        self.tblItems.popupMenu().addAction(self.actOpenStockBatchEditor)
        self.tblItems.popupMenu().addAction(self.actConfirmAll)
        self.tblItems.popupMenu().addAction(self.actUnconfirmAll)
        self.tblItems.popupMenu().addAction(self.actPropagatePriceEtc)


        self.tblItems.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.tblItems.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        self.buttonBox.addButton(self.btnPrint, QtGui.QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.btnFill, QtGui.QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.btnSelectDocumentFromMdlp, QtGui.QDialogButtonBox.ActionRole)
        self.btnFill.setEnabled(False)

        templates = getPrintTemplates(self.getStockContext())
        if not templates:
            self.btnPrint.setId(-1)
        else:
            for template in templates:
                action = CPrintAction(template.name, template.id, self.btnPrint, self.btnPrint)
                self.btnPrint.addAction(action)
            self.btnPrint.menu().addSeparator()
            self.btnPrint.addAction(CPrintAction(u'Напечатать список', -1, self.btnPrint, self.btnPrint))

#        self.tblItems.setItemDelegateForColumn(CItemsModel.priceColumnIndex, CPriceItemDelegate(self.tblItems))
        self._initView()
        self.setupDirtyCather()

        if QtGui.qApp.isMdlpEnabled():
            self.connect(QtGui.qApp, SIGNAL('ssccReceived(QString)'),  self.onSsccReceived)
            self.connect(QtGui.qApp, SIGNAL('sgtinReceived(QString)'), self.onSgtinReceived)
        self.connect(QtGui.qApp, SIGNAL('gtinReceived(QString)'),  self.onGtinReceived)

        self.mdlpBaseDocumentUuid = None
        self.mdlpStage  = None
        self.connection = None


    def save(self):
        id = CStockMotionBaseDialog.save(self)
        if not QtGui.qApp.isMdlpEnabled():
           return id
        if (    id
            and self.mdlpBaseDocumentUuid
            and self.useDirectConfirmationOrder()
            and self.mdlpStage in (None, CMdlpStage.ready, CMdlpStage.inProgress)
           ):
            confirmedSsccs, confirmedSgtins = self.modelItems.getConfirmedCiszs()
            refusedSsccs,   refusedSgtins   = self.modelItems.getRefusedCiszs()
            with CLogger(self, u'Обмен с МДЛП') as logger:
                QtGui.qApp.call(self,
                                iidoProcess,
                                (logger,
                                 id,
                                 self.getConnection(),
                                 self.mdlpBaseDocumentUuid,
                                 confirmedSsccs,
                                 confirmedSgtins,
                                 refusedSsccs,
                                 refusedSgtins
                                )
                               )
            # после этого self.mdlpStage нужно бы перечитать?
        elif ( id
               and self.useReverseConfirmationOrder()
               and self.mdlpStage in (None, CMdlpStage.ready, CMdlpStage.inProgress)
             ):
            supplierOrgId = self.cmbSupplierOrg.value()
            supplierMdlpId = getIdentification('Organisation', supplierOrgId, 'urn:mdlp:anyId', raiseIfNonFound=True)
            receiverId = self.cmbReceiver.value()
            receiverMdlpId = getIdentification('OrgStructure', receiverId, 'urn:mdlp:anyId', raiseIfNonFound=True)
            docNum = unicode(self.edtNumber.text())
            docDate = self.edtDocDate.date()
            confirmedSsccsWithSumAndVat, confirmedSgtinsWithSumAndVat = self.modelItems.getConfirmedCiszsWithSumAndVat()
            with CLogger(self, u'Обмен с МДЛП') as logger:
                QtGui.qApp.call(self,
                                iiroProcess,
                                (logger,
                                 id,
                                 self.getConnection(),
                                 supplierMdlpId,
                                 receiverMdlpId,
                                 docNum,
                                 docDate,
                                 confirmedSsccsWithSumAndVat,
                                 confirmedSgtinsWithSumAndVat,
                                )
                               )
            # после этого self.mdlpStage нужно бы перечитать?
        elif ( id
               and self.useNotificationMode()
               and self.mdlpStage in (None, CMdlpStage.ready, CMdlpStage.inProgress)
             ):
            supplierOrgId = self.cmbSupplierOrg.value()
            supplierMdlpId = getIdentification('Organisation', supplierOrgId, 'urn:mdlp:anyId', raiseIfNonFound=True)
            supplierInn = forceString(QtGui.qApp.db.translate('Organisation', 'id', supplierOrgId, 'INN'))
            supplierKpp = forceString(QtGui.qApp.db.translate('Organisation', 'id', supplierOrgId, 'KPP'))
            receiverId = self.cmbReceiver.value()
            receiverMdlpId = getIdentification('OrgStructure', receiverId, 'urn:mdlp:anyId', raiseIfNonFound=True)
            docNum = unicode(self.edtNumber.text())
            docDate = self.edtDocDate.date()
            confirmedSsccsWithSumAndVat, confirmedSgtinsWithSumAndVat = self.modelItems.getConfirmedCiszsWithSumAndVat()
            with CLogger(self, u'Обмен с МДЛП') as logger:
                QtGui.qApp.call(self,
                                iinmProcess,
                                (logger,
                                 id,
                                 self.getConnection(),
                                 supplierMdlpId,
                                 supplierInn,
                                 supplierKpp,
                                 receiverMdlpId,
                                 docNum,
                                 docDate,
                                 confirmedSsccsWithSumAndVat,
                                 confirmedSgtinsWithSumAndVat,
                                )
                               )
            # после этого self.mdlpStage нужно бы перечитать?
        return id


#    def getOrgStructureIdList(self):
#        orgStructureIdList = []
#        orgId = QtGui.qApp.currentOrgId()
#        if orgId:
#            orgId = QtGui.qApp.currentOrgId()
#            receiverId = self.cmbReceiver.value()
#            if orgId and receiverId:
#                db = QtGui.qApp.db
#                tableOS = db.table('OrgStructure')
#                orgStructureIdList = db.getDistinctIdList(tableOS, [tableOS['id']], [tableOS['organisation_id'].eq(orgId), tableOS['deleted'].eq(0)])
#        return orgStructureIdList


    def getStockContext(self):
        return ['InvoiceCreate']


    def actPrintMotions(self, templateId):
        from Stock.StockMotionInfo import CStockMotionInfoList
        if templateId == -1:
            self.getNomenclaturePrint()
        else:
            idList = self.tblItems.model().itemIdList()
            context = CInfoContext()
            data = { 'invoicesList': CStockMotionInfoList(context, idList)}
            QtGui.qApp.call(self, applyTemplate, (self, templateId, data))


    def dumpParams(self, cursor):
        db = QtGui.qApp.db
        description = []
        number = unicode(self.edtNumber.text())
        if number:
            description.append(u'Номер %s'%number)
        docDate = self.edtDocDate.date()
        if docDate:
           description.append(u'Дата документа %s'%forceString(docDate))

        reason = unicode(self.cmbReason.currentText())
        if reason:
           description.append(u'Основание %s'%unicode)


        date = self.edtDate.date()
        if date:
            dateTime = QDateTime(date, self.edtTime.time())
            description.append(u'Дата приходования %s'%forceString(dateTime))

        receiver = self.cmbReceiver.value()
        if receiver:
            description.append(u'Получатель %s'%forceString(db.translate('OrgStructure', 'id', receiver, 'name')))

        receiverPerson = self.cmbReceiverPerson.value()
        if receiverPerson:
            description.append(u'Ответственный %s'%forceString(db.translate('vrbPersonWithSpeciality', 'id', receiverPerson, 'name')))

        note = self.edtNote.text()
        if note:
            description.append(u'Примечания %s'%forceString(note))
        description.append(u'отчёт составлен: ' + forceString(QDateTime.currentDateTime()))
        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


    def getNomenclaturePrint(self):
        model = self.tblItems.model()
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.windowTitle())
        self.dumpParams(cursor)
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        colWidths  = [ self.tblItems.columnWidth(i) for i in xrange(model.columnCount()-1) ]
        colWidths.insert(0,10)
        totalWidth = sum(colWidths)
        tableColumns = []
        iColNumber = False
        for iCol, colWidth in enumerate(colWidths):
            widthInPercents = str(max(1, colWidth*90/totalWidth))+'%'
            if iColNumber == False:
                tableColumns.append((widthInPercents, [u'№'], CReportBase.AlignRight))
                iColNumber = True
            tableColumns.append((widthInPercents, [forceString(model._cols[iCol].title())], CReportBase.AlignLeft))
        table = createTable(cursor, tableColumns)
        for iModelRow in xrange(model.rowCount()-1):
            iTableRow = table.addRow()
            table.setText(iTableRow, 0, iModelRow+1)
            for iModelCol in xrange(model.columnCount()):
                index = model.createIndex(iModelRow, iModelCol)
                text = forceString(model.data(index))
                table.setText(iTableRow, iModelCol+1, text)
        html = doc.toHtml('utf-8')
        view = CReportViewDialog(self)
        view.setText(html)
        view.exec_()


    def setDefaults(self):
        now = QDateTime.currentDateTime()
        self.edtDate.setDate(now.date())
        self.cmbReceiver.setValue(QtGui.qApp.currentOrgStructureId())


    def setMdlpBaseDocumentUuid(self, documentUuid):
        self.mdlpBaseDocumentUuid = documentUuid


    def setRecord(self, record):
        CStockMotionBaseDialog.setRecord(self, record)
        setRBComboBoxValue(self.cmbSupplierOrg,       record, 'supplierOrg_id')
        setDateEditValue(  self.edtDocDate,           record, 'docDate')
        setRBComboBoxValue(self.cmbReason,            record, 'reason_id')
        setLineEditValue(  self.edtSupplierOrgPerson, record, 'supplierOrgPerson')
        setRBComboBoxValue(self.cmbReceiver,          record, 'receiver_id')
        setRBComboBoxValue(self.cmbReceiverPerson,    record, 'receiverPerson_id')
        self.setMdlpBaseDocumentUuid(forceString(record.value('mdplBaseDocumentUuid')))
        self.mdlpStage = forceInt(record.value('mdlpStage'))
#        self.mdplDone = forceBool(record.value('mdplDone'))
        self.modelItems.loadItems(self.itemId())
        self.lblSummaryInfo.setText(self.modelItems.getSummaryInfo())
        self.btnFill.setEnabled(self.cmbReason.value() is not None)
        self.setIsDirty(False)
#        if self.mdlpStage != CMdlpStage.unnecessary:
#            self.setReadOnly()


    def getRecord(self):
        record = CStockMotionBaseDialog.getRecord(self)
        getRBComboBoxValue(self.cmbSupplierOrg,       record, 'supplierOrg_id')
        getDateEditValue(  self.edtDocDate,           record, 'docDate')
        getRBComboBoxValue(self.cmbReason,            record, 'reason_id')
        getLineEditValue(  self.edtSupplierOrgPerson, record, 'supplierOrgPerson')
        getRBComboBoxValue(self.cmbReceiver,          record, 'receiver_id')
        getRBComboBoxValue(self.cmbReceiverPerson,    record, 'receiverPerson_id')
        record.setValue('mdplBaseDocumentUuid', self.mdlpBaseDocumentUuid)
        if self.mdlpStage is None:
            storedMdlpStage = CMdlpStage.unnecessary # нужно не storedMdlpStage а что-то другое...
            if self.modelItems.hasMdlpRelatedCiszs():
                if self.useDirectConfirmationOrder():
                    confirmedSsccs, confirmedSgtins = self.modelItems.getConfirmedCiszs()
                    refusedSsccs,   refusedSgtins   = self.modelItems.getRefusedCiszs()
                    if confirmedSsccs or confirmedSgtins or refusedSsccs or refusedSgtins:
                        storedMdlpStage = CMdlpStage.ready
                elif self.useReverseConfirmationOrder() or self.useNotificationMode():
                    confirmedSsccsWithSumAndVat, confirmedSgtinsWithSumAndVat = self.modelItems.getConfirmedCiszsWithSumAndVat()
                    if confirmedSsccsWithSumAndVat or confirmedSgtinsWithSumAndVat:
                        storedMdlpStage = CMdlpStage.ready
            record.setValue('mdlpStage', storedMdlpStage)
        record.setValue('type', self.stockDocumentType)
        return record


    def saveInternals(self, id):
        financeId = self.cmbFinance.value()
        for item in self.modelItems.items():
            item.setValue('finance_id', financeId)
        self.modelItems.saveItems(id)


    def checkDataEntered(self):
        result = self._checkStockMotionItemsData(self.tblItems)
        result = result and (self.cmbReason.value() or self.checkInputMessage(u'основание', False, self.cmbReason))
        result = result and (self.cmbSupplierOrg.value() or self.checkInputMessage(u'поставщика', False, self.cmbSupplierOrg))
        result = result and self.checkItemsDataEntered()
        return result


    def checkItemsDataEntered(self):
        return True


    def useDirectConfirmationOrder(self):
        return QtGui.qApp.isMdlpEnabled() and self.cmbConfirmationOrder.currentIndex() == 1 and not self.useNotificationMode()


    def useReverseConfirmationOrder(self):
        return QtGui.qApp.isMdlpEnabled() and self.cmbConfirmationOrder.currentIndex() == 2 and not self.useNotificationMode()


    def useNotificationMode(self):
        return QtGui.qApp.isMdlpEnabled() and self.getConnection().notificationMode


    def getConnection(self):
        if self.connection is None:
            self.connection = CMdlpConnection()
        return self.connection


    def onSsccReceived(self, sscc):
        if self.useDirectConfirmationOrder():
            rows = self.modelItems.confirmRowsWithSscc(sscc)
            if rows:
                self.tblItems.setCurrentIndex(self.modelItems.index(rows[0], self.modelItems.ssccColumnIndex))
            else:
                QMessageBox.information(self,
                                        u'Поставка не соответствует документу',
                                        u'В документе нет строк с кодом транспортной упаковки «%s»' % sscc,
                                        QMessageBox.Close,
                                        QMessageBox.Close
                                       )
        elif self.useReverseConfirmationOrder() or self.useNotificationMode():
            row = self.modelItems.findRowWithSscc(sscc)
            if row is not None:
                self.tblItems.setCurrentIndex(self.modelItems.index(row, self.modelItems.ssccColumnIndex))
            else:
                supplierOrgId = self.cmbSupplierOrg.value()
                supplierMdlpId = getIdentification('Organisation', supplierOrgId, 'urn:mdlp:anyId', raiseIfNonFound=True)

                connection = self.getConnection()
                fhs = connection.getSsccFullHierarchyByList([sscc])
                if not isinstance(fhs, list) or len(fhs) != 1:
                    QMessageBox.information(self,
                                            u'Ошибка',
                                            u'В МДЛП не удалось найти транспортную упаковку с кодом «%s»' % sscc,
                                            QMessageBox.Close,
                                            QMessageBox.Close
                                           )
                    return
                ownerId = fhs[0].up.ownerId
                if ownerId != supplierMdlpId:
                    QMessageBox.information(self,
                                            u'Ошибка',
                                            u'По данным МДЛП транспортная упаковка с кодом «%s» принадлежит организации «%s», а отправитель «%s»' % (sscc, ownerId, supplierMdlpId),
                                            QMessageBox.Close,
                                            QMessageBox.Close
                                           )
                    return
                rows = self.modelItems.addSgtins(sscc, fhs[0].sgtins)
                if rows:
                    self.tblItems.setCurrentIndex(self.modelItems.index(rows[0], self.modelItems.ssccColumnIndex))


    def onSgtinReceived(self, sgtin):
        if self.useDirectConfirmationOrder():
            rows = self.modelItems.confirmRowsWithSgtin(sgtin)
            if rows:
                self.tblItems.setCurrentIndex(self.modelItems.index(rows[0], self.modelItems.sgtinColumnIndex))
            else:
                QMessageBox.information(self,
                                        u'Поставка не соответствует документу',
                                        u'В документе нет строк с кодом вторичной упаковки «%s»' % sgtin,
                                        QMessageBox.Close,
                                        QMessageBox.Close
                                       )
        elif self.useReverseConfirmationOrder() or self.useNotificationMode():
            rows = self.modelItems.confirmRowsWithSgtin(sgtin)
            if rows:
                self.tblItems.setCurrentIndex(self.modelItems.index(rows[0], self.modelItems.sgtinColumnIndex))
                return
            supplierOrgId = self.cmbSupplierOrg.value()
            supplierMdlpId = getIdentification('Organisation', supplierOrgId, 'urn:mdlp:anyId', raiseIfNonFound=True)
            connection = self.getConnection()
            sgtinObjects = connection.getSgtins(sgtin=unicode(sgtin), ownerId=supplierMdlpId)
            if sgtinObjects:
                row = self.modelItems.addSgtin('', sgtinObjects[0])
                self.tblItems.setCurrentIndex(self.modelItems.index(row, self.modelItems.sgtinColumnIndex))
            else:
                QMessageBox.information(self,
                                        u'Ошибка',
                                        u'В МДЛП у поставщика «%s» не найден sgtin «%s»' % (supplierMdlpId, sgtin),
                                        QMessageBox.Close,
                                        QMessageBox.Close
                                       )


    def onGtinReceived(self, gtin):
        modelItems = self.modelItems
        if not modelItems.isMdlpRelatedGtinPresent(gtin):
            nomenclatureId = findByIdentification('rbNomenclature', 'urn:gtin', gtin, raiseIfNonFound=False)
            if nomenclatureId:
                row = modelItems.findMdlpIndependedNomemclature(nomenclatureId)
                if row is not None:
                    qnt = forceInt(modelItems.value(row, 'qnt'))
                    modelItems.setValue(row, 'qnt', qnt+1)
                else:
                    row = len(modelItems.items())
                    item = modelItems.getEmptyRecord()
                    item.setValue('nomenclature_id', nomenclatureId)
                    item.setValue('qnt', 1)
                    modelItems.addRecord(item)
                self.tblItems.setCurrentIndex(self.modelItems.index(row, self.modelItems.nomenclatureColumnIndex))
                self.lblSummaryInfo.setText(modelItems.getSummaryInfo())
            else:
                QMessageBox.information(self,
                                        u'ЛСиИМН не найдено',
                                        u'Не удаётся найти ЛСиИМН с кодом GTIN «%s»' % gtin,
                                        QMessageBox.Close,
                                        QMessageBox.Close
                                       )

    # slots

    @pyqtSignature('int')
    def on_cmbSupplierOrg_currentIndexChanged(self, val):
        supplierOrgId = self.cmbSupplierOrg.value()
        supplierOrgAssigned = bool(supplierOrgId)
        for widget in ( self.lblSupplierOrgPerson, self.edtSupplierOrgPerson,
                        self.lblReason,            self.cmbReason,
                        self.lblFinance,           self.cmbFinance,
                      ):
            widget.setEnabled(supplierOrgAssigned)

        for widget in ( self.lblConfirmationOrder, self.cmbConfirmationOrder
                      ):
            widget.setEnabled(QtGui.qApp.isMdlpEnabled() and supplierOrgAssigned)
        self.cmbReason.setSupplierOrgId(supplierOrgId)
        self.modelItems.setSupplierOrgId(supplierOrgId)


    @pyqtSignature('QDate')
    def on_edtDate_dateChanged(self, date):
        self.cmbReason.setDate(date)


    @pyqtSignature('int')
    def on_cmbReason_currentIndexChanged(self, index):
        purchaseContractId = self.cmbReason.value()
        self.btnFill.setEnabled(bool(purchaseContractId))
        if purchaseContractId:
            db = QtGui.qApp.db
            record = db.getRecord('StockPurchaseContract',
                                   ('finance_id',
                                    'confirmationOrder'
                                   ),
                                   purchaseContractId
                                 )
            self.cmbFinance.setValue(forceRef(record.value('finance_id')))
            self.cmbConfirmationOrder.setCurrentIndex(forceInt(record.value('confirmationOrder')))
        else:
            self.cmbFinance.setValue(None)
            self.cmbConfirmationOrder.setCurrentIndex(0)


    @pyqtSignature('int')
    def on_cmbConfirmationOrder_currentIndexChanged(self, index):
        directConfirmationOrder = self.useDirectConfirmationOrder()
        self.btnSelectDocumentFromMdlp.setEnabled(directConfirmationOrder)
        self.actConfirmAll.setEnabled(directConfirmationOrder)
        self.actUnconfirmAll.setEnabled(directConfirmationOrder)
        self.actPropagatePriceEtc.setEnabled(self.useReverseConfirmationOrder() or self.useNotificationMode())


    @pyqtSignature('int')
    def on_cmbReceiver_currentIndexChanged(self, index):
        receiverId = self.cmbReceiver.value()
        self.cmbReceiverPerson.setOrgStructureId(receiverId)
        self.modelItems.setReceiverId(receiverId)


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_modelItems_dataChanged(self, topLeftIndex, bottomRightIndex):
        self.lblSummaryInfo.setText(self.modelItems.getSummaryInfo())


    @pyqtSignature('')
    def on_actOpenStockBatchEditor_triggered(self):
        self.on_tblItems_doubleClicked(self.tblItems.currentIndex())


    @pyqtSignature('')
    def on_actConfirmAll_triggered(self):
        if self.useDirectConfirmationOrder():
            self.modelItems.setConfirmAll(True)


    @pyqtSignature('')
    def on_actUnconfirmAll_triggered(self):
        if self.useDirectConfirmationOrder():
            self.modelItems.setConfirmAll(False)


    @pyqtSignature('')
    def on_actPropagatePriceEtc_triggered(self):
        if self.useReverseConfirmationOrder() or self.useNotificationMode():
            self.modelItems.propagatePriceEtc()


    @pyqtSignature('int')
    def on_btnPrint_printByTemplate(self, templateId):
        self.actPrintMotions(templateId)


    @pyqtSignature('')
    def on_btnFill_clicked(self):
        purchaseContractId = self.cmbReason.value()
        if purchaseContractId:
            self.modelItems.fill(purchaseContractId)


    @pyqtSignature('')
    def on_btnSelectDocumentFromMdlp_clicked(self):
        if not QtGui.qApp.isMdlpEnabled():
            return
        date = self.edtDocDate.date() or QDate.currentDate()
        supplierOrgId = self.cmbSupplierOrg.value()
        supplierMdlpId = getIdentification('Organisation', supplierOrgId, 'urn:mdlp:anyId', raiseIfNonFound=True)
        receiverId = self.cmbReceiver.value()
        receiverMdlpId = getIdentification('OrgStructure', receiverId, 'urn:mdlp:anyId', raiseIfNonFound=True)
        mdlpDocumentId, itemsFromDocument = selectIncomingInvoiceFromMdlp(self,
                                                                          self.getConnection(),
                                                                          date,
                                                                          supplierMdlpId,
                                                                          receiverMdlpId)
        if mdlpDocumentId:
            items = []
            for itemFromDocument in itemsFromDocument:
                item = self.modelItems.getEmptyRecord()
                item.setValue('isMdlpRelated',   True)
                item.setValue('isConfirmed',     False)
                item.setValue('sscc',            itemFromDocument.sscc)
                item.setValue('sgtin',           itemFromDocument.sgtin)
                item.setValue('nomenclature_id', findByIdentification('rbNomenclature', 'urn:gtin', itemFromDocument.sgtin[:14], raiseIfNonFound=False))
                item.setValue('batch',           itemFromDocument.batch)
                item.setValue('shelfTime',       itemFromDocument.expirationDate)
                item.setValue('qnt',             1)
                item.setValue('price',           itemFromDocument.sum)
                item.setValue('sum',             itemFromDocument.sum)
                item.setValue('vat',             itemFromDocument.vat)
                items.append(item)
            self.setMdlpBaseDocumentUuid(mdlpDocumentId)
            self.modelItems.setItems(items)
            self.lblSummaryInfo.setText(self.modelItems.getSummaryInfo())


# ############################################


class CItemsModel(CNomenclatureItemsBaseModel, CSummaryInfoModelMixin):
    isMdlpRelatedColumnIndex  = 0
    isConfirmedColumnIndex    = 1
    ssccColumnIndex           = 2
    sgtinColumnIndex          = 3
    nomenclatureColumnIndex   = 4
    batchColumnIndex          = 5
    shelfTimeColumnIndex      = 6
    medicalAidKindColumnIndex = 7
    qntColumnIndex            = 8
    unitColumnIndex           = 9
    priceColumnIndex          = 10
    sumColumnIndex            = 11
    vatColumnIndex            = 12
    noteColumnIndex           = 13

    class CSumCol(CFloatInDocTableCol):
        def _toString(self, value):
            if value.isNull():
                return None
            return format(forceDouble(value), '.2f')


    def __init__(self, parent, showExists=False):
        CNomenclatureItemsBaseModel.__init__(self, parent)
        #CNomenclatureItemsBaseModel.__init__(self, 'StockMotion_Item', 'id', 'master_id', parent)

        isMdlpEnabled = QtGui.qApp.isMdlpEnabled()

        self.addCol(CBoolInDocTableCol(u'МДЛП',   'isMdlpRelated', 5, readOnly=not isMdlpEnabled))
        self.addCol(CBoolInDocTableCol(u'Подтв.', 'isConfirmed',   5, readOnly=not isMdlpEnabled))

        self.addCol(CInDocTableCol(u'Код третичной упаковки', 'sscc', 18, readOnly=not isMdlpEnabled))
        self.addCol(CInDocTableCol(u'Код вторичной упаковки', 'sgtin', 50, readOnly=not isMdlpEnabled))

        self._nomenclatureColumn = CNomenclatureInDocTableCol(u'ЛСиИМН', 'nomenclature_id', 50, showFields = CRBComboBox.showName)
        self.addCol(self._nomenclatureColumn)
        self.addCol(CInDocTableCol( u'Серия', 'batch', 16))
        self.addCol(CDateInDocTableCol( u'Годен до', 'shelfTime', 12, canBeEmpty=True))
        self.addCol(CRBInDocTableCol(    u'Вид медицинской помощи', 'medicalAidKind_id', 15, 'rbMedicalAidKind'))
        self.addCol(getStockMotionItemQuantityColumn(u'Кол-во', 'qnt', 12))
        self.addCol(CRBInDocTableCol(u'Ед.Учета', 'unit_id', 12, 'rbUnit', addNone=False))
        self.addCol(CFloatInDocTableCol(u'Цена', 'price', 12, precision=2))
        self.addCol(CItemsModel.CSumCol( u'Сумма', 'sum', 12)).setReadOnly(True)
        self.addCol(CItemsModel.CSumCol( u'НДС', 'vat', 12))
        self.addCol(CInDocTableCol( u'Примечание', 'note', 15))
        self.addHiddenCol('finance_id')

#        self.addCol(CItemsModel.CPriceCol(u'Цена', 'id', 12, precision=2))


#    def cellReadOnly(self, index):
#        column = index.column()
#        if column == CItemsModel.sumColumnIndex:
#            return (not self._supplierOrgId)
#        return False


    def getNomenclatureNameById(self, nomenclatureId):
        return forceString(self._nomenclatureColumn.toString(nomenclatureId, None))


#    def getEmptyRecord(self):
#        record = CNomenclatureItemsBaseModel.getEmptyRecord(self)
#        return record

    def setData(self, index, value, role=Qt.EditRole):
        col = index.column()
        row = index.row()
        result = CNomenclatureItemsBaseModel.setData(self, index, value, role)
        if role == Qt.EditRole:
            if result:
                if col == self.nomenclatureColumnIndex:
                    nomenclatureId = forceRef(value)
                    unitId = self._getNomenclatureDefaultUnits(nomenclatureId)['defaultStockUnitId']
                    self.setValue(row, 'unit_id', unitId)
                if col in (self.qntColumnIndex,  self.priceColumnIndex):
                    qnt   = forceDouble(self.value(row, 'qnt'))
                    price = forceDouble(self.value(row, 'price'))
                    self.setValue(row, 'sum', round(qnt*price, 2))
        return result




#    def setData(self, index, value, role=Qt.EditRole):
#        if not index.isValid():
#            return False
#        col = index.column()
#        row = index.row()
#        if col in (self.qntColumnIndex, self.priceColumnIndex):
#            if col == self.qntColumnIndex:
#                if not (0 <= row < len(self._items)):
#                    return False
#                item = self._items[row]
#                prevQnt = forceDouble(item.value('qnt'))
#                existsColumn = forceDouble(self._cols[self.existsColumnIndex].toString(value, item))
#                if self.setPriceLineEditable(item):
#                    #existsColumn = existsColumn + prevQnt
#                    existsColumn = existsColumn + forceDouble(value)
#                if not self.isPriceLineEditable and forceDouble(item.value('price')) and (not existsColumn or existsColumn < 0):
#                   return False
#                if not self.isPriceLineEditable and forceDouble(item.value('price')) and existsColumn < forceDouble(value):
#                    value = toVariant(existsColumn)
#            result = CNomenclatureItemsBaseModel.setData(self, index, value, role)
#            if result:
#                self.setIsUpdateValue(True)
#                item = self._items[row]
#                if col == self.qntColumnIndex:
#                    item.setValue('prevQnt', prevQnt)
#                item.setValue('sum', toVariant(forceDouble(item.value('qnt')) * forceDouble(item.value('price'))))
#                self.emitRowChanged(row)
#            return result
#        elif col == self.nomenclatureColumnIndex:
#            if 0 <= row < len(self._items):
#                oldNomenclatureId = forceRef(self._items[row].value('nomenclature_id'))
#            else:
#                oldNomenclatureId = None
#            result = CNomenclatureItemsBaseModel.setData(self, index, value, role)
#            if result:
#                item = self._items[row]
#                nomenclatureId = forceRef(item.value('nomenclature_id'))
#                if oldNomenclatureId != nomenclatureId:
#                    unitId = self.getDefaultStockUnitId(nomenclatureId)
#                    item.setValue('unit_id', toVariant(unitId))
#                    if self.updateBatchShelfTimeFinance:
#                        batch, shelfTime, financeId, medicalAidKind, price = getBatchShelfTimeFinance(forceRef(value))
#                        result = CNomenclatureItemsBaseModel.setData(self, index, value, role)
#                        item.setValue('batch', toVariant(batch))
#                        unitId = forceRef(item.value('unit_id'))
#                        nomenclatureId = forceRef(item.value('nomenclature_id'))
#                        if price and unitId and nomenclatureId:
#                            ratio = self.getRatio(nomenclatureId, unitId, None)
#                            if ratio is not None:
#                                price = price*ratio
#                        item.setValue('price', toVariant(price))
#                        if financeId:
#                            item.setValue('finance_id', toVariant(financeId))
#                        else:
#                            item.setNull('finance_id')
#                        item.setValue('shelfTime', toVariant(shelfTime))
#                        if medicalAidKind:
#                            item.setValue('medicalAidKind_id', toVariant(medicalAidKind))
#                        else:
#                            item.setNull('medicalAidKind_id')
#                    self.emitRowChanged(row)
#            return result
#        elif col == self.unitColumnIndex:
#            if not (0 <= row < len(self._items)):
#                return False
#            item = self._items[row]
#            oldUnitId = forceRef(item.value('unit_id'))
#            result = CNomenclatureItemsBaseModel.setData(self, index, value, role)
#            if result:
#                self.setIsUpdateValue(True)
#                newUnitId = forceRef(item.value('unit_id'))
##                self._applySumRatio(item, oldUnitId, newUnitId)
#                self._applyQntRatio(item, oldUnitId, newUnitId)
#                newPrice = self.updatePriceByRatio(item, oldUnitId)
#                item.setValue('price', toVariant(newPrice))
#                item.setValue('sum', toVariant(forceDouble(item.value('qnt')) * forceDouble(item.value('price'))))
#                self.emitRowChanged(row)
#        elif col == self.sumColumnIndex and self._supplierOrgId:
#            result = CNomenclatureItemsBaseModel.setData(self, index, value, role)
#            if result:
#                item = self._items[row]
#                qnt = forceDouble(item.value('qnt'))
#                item.setValue('price', toVariant(forceDouble(item.value('sum'))/qnt) if qnt else 0.0)
#        else:
#            return CNomenclatureItemsBaseModel.setData(self, index, value, role)



    def fill(self, purchaseContractId):
        if purchaseContractId:
            db = QtGui.qApp.db
            tablePurchaseContract = db.table('StockPurchaseContract')
            tablePurchaseContractItem = db.table('StockPurchaseContract_Item')
            cols = [tablePurchaseContract['finance_id'],
                    tablePurchaseContractItem['idx'],
                    tablePurchaseContractItem['nomenclature_id'],
                    tablePurchaseContractItem['batch'],
                    tablePurchaseContractItem['shelfTime'],
                    tablePurchaseContractItem['qnt'],
                    tablePurchaseContractItem['unit_id'],
                    tablePurchaseContractItem['sum']
                    ]
            cond = [tablePurchaseContract['id'].eq(purchaseContractId),
                    tablePurchaseContract['deleted'].eq(0),
                    tablePurchaseContractItem['master_id'].eq(purchaseContractId),
                    tablePurchaseContractItem['deleted'].eq(0)
                    ]
            queryTable = tablePurchaseContract.innerJoin(tablePurchaseContractItem, tablePurchaseContractItem['master_id'].eq(tablePurchaseContract['id']))
            records = db.getRecordList(queryTable, cols, cond, order = [tablePurchaseContractItem['idx'].name()])
            for record in records:
                nomenclatureId = forceRef(record.value('nomenclature_id'))
#                unitId = self.getDefaultStockUnitId(nomenclatureId)
                myItem = self.getEmptyRecord()
                myItem.setValue('nomenclature_id', toVariant(nomenclatureId))
                myItem.setValue('unit_id',         record.value('unit_id'))
                myItem.setValue('finance_id',      record.value('finance_id'))
                myItem.setValue('medicalAidKind_id', toVariant(None))
                myItem.setValue('batch',           record.value('batch'))
                myItem.setValue('shelfTime',       record.value('shelfTime'))
                myItem.setValue('qnt',             record.value('qnt'))
                myItem.setValue('sum',             record.value('sum'))
                myItem.setValue('price',           toVariant(forceDouble(record.value('sum'))/forceDouble(record.value('qnt'))))
                myItem.setValue('oldQnt',          record.value('qnt'))
                myItem.setValue('oldSum',          record.value('sum'))
                self.items().append(myItem)
        self.reset()


    def setConfirmAll(self, value):
        for row, item in enumerate(self.items()):
            if forceBool(item.value('isMdlpRelated')):
                self.setValue(row, 'isConfirmed', value)


    def confirmRowsWithSscc(self, sscc):
        # подтвердить строки с заданным sscc
        # вернуть номера подходящих строк
        # применяется для прямого порядка
        result = []
        for row, item in enumerate(self.items()):
            if forceBool(item.value('isMdlpRelated')) and forceString(item.value('sscc')) == sscc:
                self.setValue(row, 'isConfirmed', True)
                result.append(row)
        return result


    def findRowWithSscc(self, sscc):
        # найти строку с заданным sscc
        # вернуть номер подходящей строки
        # применяется для обратного порядка
        for row, item in enumerate(self.items()):
            if forceBool(item.value('isMdlpRelated')) and forceString(item.value('sscc')) == sscc:
                return row
        return None


    def addSgtin(self, sscc, sgtinObject):
        result = len(self.items())
        gtin = sgtinObject.sgtin[:14]
        nomenclatureId = findByIdentification('rbNomenclature', 'urn:gtin', gtin, raiseIfNonFound=False)
        prevItem = None
        if nomenclatureId is not None:
            for prevItem in reversed(self.items()):
                if forceRef(prevItem.value('nomenclature_id')) == nomenclatureId:
                    break
        item = self.getEmptyRecord()
        item.setValue('isMdlpRelated',   True)
        item.setValue('isConfirmed',     not sscc)
        item.setValue('sscc',            sscc)
        item.setValue('sgtin',           sgtinObject.sgtin)
        item.setValue('nomenclature_id', nomenclatureId)
        item.setValue('batch',           sgtinObject.batch)
        item.setValue('shelfTime',       sgtinObject.expirationDate)
        item.setValue('qnt',             1)
        if prevItem:
            item.setValue('price', prevItem.value('price'))
            item.setValue('sum', prevItem.value('sum'))
            item.setValue('vat', prevItem.value('vat'))

        self.addRecord(item)
        return result


    def addSgtins(self, sscc, sgtinObjects):
        # добавить sgtins
        # применяется при обратном порядке
        result = []
        for sgtinObject in sgtinObjects:
            result.append(self.addSgtin(sscc, sgtinObject))
        return result


    def confirmRowsWithSgtin(self, sgtin):
        # подтвердить строки с заданным sgtin
        # вернуть номера подходящих строк
        result = []
        for row, item in enumerate(self.items()):
            if forceBool(item.value('isMdlpRelated')) and forceString(item.value('sgtin')) == sgtin:
                self.setValue(row, 'isConfirmed', True)
                result.append(row)
        return result


    def propagatePriceEtc(self):
        # проставить цены и т.п. в строки, где цена не указана
        samples = {}
        for row, item in enumerate(self.items()):
            if forceBool(item.value('isMdlpRelated')):
                nomenclatureId = forceRef(item.value('nomenclature_id'))
                qnt   = forceDouble(item.value('qnt'))
                price = forceDouble(item.value('price'))
                vat   = forceDouble(item.value('vat'))
                if price > 0.005:
                    samples[nomenclatureId] = (price, vat/qnt if qnt>0 else 0.0)
                elif nomenclatureId in samples:
                    (price, vatPerUnit) = samples[nomenclatureId]
                    self.setValue(row, 'price', price)
                    self.setValue(row, 'sum',   price*qnt)
                    self.setValue(row, 'vat',   vatPerUnit*qnt)



    def isMdlpRelatedGtinPresent(self, gtin):
        for row, item in enumerate(self.items()):
            if forceBool(item.value('isMdlpRelated')) and forceString(item.value('sgtin'))[:14] == gtin:
                return True
        return False


    def findMdlpIndependedNomemclature(self, nomenclatureId):
        for row, item in enumerate(self.items()):
            if not forceBool(item.value('isMdlpRelated')) and forceRef(item.value('nomenclature_id')) == nomenclatureId:
                return row
        return None


    def hasMdlpRelatedCiszs(self):
        for item in self.items():
            if forceBool(item.value('isMdlpRelated')):
                return True
        return False


    def getConfirmedCiszs(self):
        ssccs  = set()
        refusedSsccs = set()
        sgtins = set()
        for item in self.items():
            if forceBool(item.value('isMdlpRelated')):
                if forceBool(item.value('isConfirmed')):
                    sscc  = forceString(item.value('sscc'))
                    sgtin = forceString(item.value('sgtin'))
                    if sscc:
                        ssccs.add(sscc)
                    else:
                        sgtins.add(sgtin)
                else:
                    sscc  = forceString(item.value('sscc'))
                    if sscc:
                        refusedSsccs.add(sscc)

        return list(ssccs-refusedSsccs), list(sgtins)


    def getConfirmedCiszsWithSumAndVat(self):
        mapSsccsToData  = {}
        refusedSsccs = set()
        sgtins = set()
        for item in self.items():
            if forceBool(item.value('isMdlpRelated')):
                if forceBool(item.value('isConfirmed')):
                    sscc  = forceString(item.value('sscc'))
                    sgtin = forceString(item.value('sgtin'))
                    sum   = forceDouble(item.value('sum'))
                    vat   = forceDouble(item.value('vat'))
                    if sscc:
                        ssccData = mapSsccsToData.get(sscc)
                        if sscc not in mapSsccsToData:
                            mapSsccsToData[sscc] = [sum, vat]
                    else:
                        sgtins.add((sgtin, sum, vat))
                else:
                    sscc  = forceString(item.value('sscc'))
                    if sscc:
                        refusedSsccs.add(sscc)
        return ([(sscc, ssccData[0], ssccData[1])
                 for sscc, ssccData in mapSsccsToData.iteritems()
                 if sscc not in refusedSsccs
                ],
                list(sgtins)
               )


    def getRefusedCiszs(self):
        ssccs  = set()
        sgtins = set()
        for item in self.items():
            if forceBool(item.value('isMdlpRelated')) and not forceBool(item.value('isConfirmed')):
                sscc  = forceString(item.value('sscc'))
                sgtin = forceString(item.value('sgtin'))
                if sscc:
                    ssccs.add(sscc)
                else:
                    sgtins.add(sgtin)
        return list(ssccs), list(sgtins)
