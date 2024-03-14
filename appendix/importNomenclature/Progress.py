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
u"""Импорт номенклатуры из XML"""

import os

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt, pyqtSignature, SIGNAL, QDate, QDateTime

from library.Utils import (forceRef, toVariant, forceInt, forceString,
                           forceDouble)

from Exchange.Export import LoggerMixin
from Exchange.Utils import tbl
from Stock.Utils import (getExistsNomenclatureAmount,
                         getExistsNomenclatureAmountSum)

from appendix.importNomenclature.Log import CSuccessLogger, CErrorLogger
from appendix.importNomenclature.XmlReader import CXmlStreamReader
from appendix.importNomenclature.Ui_Progress import Ui_ProgressDialog

def _setCount(progressBar, cnt):
    u'Настройка индикатора прогресса'
    if cnt:
        progressBar.setValue(0)
        progressBar.setMaximum(cnt)
        progressBar.setEnabled(True)
        progressBar.setTextVisible(True)
    else:
        progressBar.setValue(0)
        progressBar.setMaximum(1)
        progressBar.setEnabled(False)
        progressBar.setTextVisible(False)


class CProgressDialog(QtGui.QDialog, Ui_ProgressDialog, LoggerMixin):
    u'Диалог импорта данных'
    __pyqtSignals__ = ('startWork()', )


    docTypeBalance = 0
    docTypeArrival = 1
    docTypeMovement = 2
    docTypeChargeOff = 3
    lastKnownDocType = 3

    rbTags = ('CODE', 'NAME')
    personTags = ('ID', 'LASTN', 'FIRSTN', 'PATRN')

    commonRequiredTags = {
        'SUPPLIER_ORG': ('NAME', 'INN'),
        'SUP_PERSON': personTags,
        'RECEIVER': ('CODE', ),
        'SUPPLIER': ('CODE', ),
        'REC_PERSON': personTags,
        'ITEM': ('ID', 'NOMENCLATURE', 'QNT', 'UNIT'),
        'NOMENCLATURE': ('ID', 'TN_R', ),
        'KIND': rbTags,
        'UNIT': rbTags,
        'TYPE': rbTags,
        'CLASS': rbTags,
        'DOSAGE_UNIT': rbTags,
        'FORM': rbTags,
        'STOCK_UNIT': rbTags,
        'CLIENT_UNIT': rbTags,
    }

    requiredTags = {
        docTypeBalance: {
            'DOC': ('ID', 'TYPE', 'DATE', 'RECEIVER', 'ITEM'),
        },
        docTypeArrival: {
            'DOC': ('ID', 'TYPE', 'DATE', 'RECEIVER', 'ITEM'),
        },
        docTypeMovement: {
            'DOC': ('ID', 'TYPE', 'DATE', 'SUPPLIER', 'RECEIVER', 'ITEM'),
        },
        docTypeChargeOff: {
            'DOC': ('ID', 'TYPE', 'DATE', 'SUPPLIER', 'ITEM'),
        },
    }

    startElementName = 'LIST'
    groupNames = {
        'LIST' : ('DOC', ),
        'DOC' : ('SUPPLIER_ORG', 'SUPPLIER', 'SUP_PERSON', 'RECEIVER',
                 'REC_PERSON', 'ITEM'),
        'ITEM': ('TYPE', 'NOMENCLATURE', 'UNIT'),
        'NOMENCLATURE' : ('KIND', 'TYPE', 'CLASS', 'DOSAGE_UNIT',
                          'FORM', 'STOCK_UNIT', 'CLIENT_UNIT'),
    }

    modeNormal = 0
    modeHealthExamination = 1

    def __init__(self, parent, fileName, auto=False):
        QtGui.QDialog.__init__(self, parent)
        LoggerMixin.__init__(self)
        self._parent = parent
        self.setupUi(self)

        self.start()
        self.connect(self, SIGNAL('startWork()'), self.startWork,
                     Qt.QueuedConnection)

        self.nAdded = 0
        self.nProcessed = 0
        self.nUpdated = 0

        _setCount(self.prbNomenclature, 0)
        self._fileName = fileName
        self._db = QtGui.qApp.db

        self._tblStockMotion = tbl('StockMotion')
        self._tblOrganisation = tbl('Organisation')
        self._tblOrgStructIdentification = tbl('OrgStructure_Identification')
        self._tblPersonIdentification = tbl('Person_Identification')
        self._tblRbNomenclature = tbl('rbNomenclature')
        self._tblRbFinance = tbl('rbFinance')
        self._tblRbUnit = tbl('rbUnit')
        self._tblRbUnitIdentification = tbl('rbUnit_Identification')
        self._tblRbNomenclatureType = tbl('rbNomenclatureType')
        self._tblRbNomenclatureKind = tbl('rbNomenclatureKind')
        self._tblRbNomenclatureClass = tbl('rbNomenclatureClass')
        self._tblRbNomenclatureUnitRatio = tbl('rbNomenclature_UnitRatio')
        self._tblStockMotionItem = tbl('StockMotion_Item')
        self._tblRbStockMotionItemReason = tbl('rbStockMotionItemReason')
        self._tblRbMedicalAidKind = tbl('rbMedicalAidKind')
        self._tblStockRequisition = tbl('StockRequisition')
        self._tblStockRequisitionItem = tbl('StockRequisition_Item')

        self._cacheOrganisation = {}
        self._cacheOrgStuct = {}
        self._cachePerson = {}
        self._cacheNomenclature = {}
        self._cacheRbFinance = {}
        self._cacheRbUnit = {}
        self._cacheRbUnitName = {}
        self._cacheNomenclatureType = {}
        self._cacheNomenclatureKind = {}
        self._cacheNomenclatureClass = {}
        self._cacheRbStockMotionItemReason = {}
        self._cacheRbMedicalAidKind = {}

        self._warehouseAccSystemId = forceRef(self._db.translate(
            'rbAccountingSystem', 'code', 'WMS_warehouse', 'id'))
        self._personAccSystemId = forceRef(self._db.translate(
            'rbAccountingSystem', 'code', 'WMS_Person', 'id'))
        self._unitAccSystemId = forceRef(self._db.translate(
            'rbAccountingSystem', 'code', 'WMS_unit', 'id'))

        for val in self.requiredTags.values():
            val.update(self.commonRequiredTags)

        self._logErrors = False
        self._logSuccess = False
        self._createNomenclature = False
        self._lastMsg = None
        self._logFieldName = None
        self._logBaseFieldName = None
        self._logItemId = None
        self._errorLog = None
        self._successLog = None

        self.auto = auto
        self.aborted = False
        self.processDone = False


    def start(self):
        u'Готовит диалог к началу работы'
        self.processDone = False
        self.aborted = False
        self.btnCancel.setText(u'Отмена')


    def stop(self):
        u'Готовит диалог к окончанию работы'
        self.processDone = True
        self.btnCancel.setText(u'Закрыть')


    def done(self, result):
        u'Завершает работу диалога'
        self.stop()
        QtGui.QDialog.done(self, result)


    def exec_(self):
        u'Запускает диалог'
        self.emit(SIGNAL('startWork()'))

        return QtGui.QDialog.exec_(self)


    @pyqtSignature('')
    def on_btnCancel_clicked(self):
        u'Обработчик нажатия кнопки `Отмена`'
        if self.processDone:
            self.accept()
        else:
            self.aborted = True


    def startWork(self):
        u'Слот, запускает работу'
        self.start()
        QtGui.qApp.call(self, self.work)
        self.stop()


    def work(self):
        u"""Запускает рабочую функцию диалога"""

        if self._logErrors:
            self._errorLog = CErrorLogger()
            self._errorLog.open(u'{0}.err'.format(self._fileName[:-4]))

        if self._logSuccess:
            self._successLog = CSuccessLogger()
            self._successLog.open(u'{0}.scc'.format(self._fileName[:-4]))

        result = self.processXml(self.prbNomenclature)

        if self._logErrors:
            self._errorLog.close()

            if result:
                os.remove(self._errorLog.fileName)

        if self._logSuccess:
            self._successLog.close()

            if not result:
                os.remove(self._successLog.fileName)

        if self.auto:
            self.close()


    def setLogError(self, val):
        self._logErrors = val


    def setLogSuccess(self, val):
        self._logSuccess = val


    def setCreateNomenclature(self, val):
        self._createNomenclature = val


    def logError(self, msg):
        self._lastMsg = msg
        LoggerMixin.logError(self, msg)


    def logInfo(self, msg):
        LoggerMixin.logInfo(self, msg, True)

# ******************************************************************************

    def processXml(self, progressBar):
        u"""Разбирает указанный XML файл, отправляет данные в БД"""
        fileName = self._fileName

        if not fileName:
            self.logError(u'Не указано имя файла для импорта данных.')
            return False

        if not self._warehouseAccSystemId:
            self.logError(u'Не найдена внешняя учётная система с кодом'
                          u' `WMS_warehouse`.')
            return False

        if not self._personAccSystemId:
            self.logError(u'Не найдена внешняя учётная система с кодом'
                          u' `WMS_Person`.')
            return False

        progressBar.setFormat(u'%v байт')
        inFile = QtCore.QFile(fileName)

        if not inFile.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            msg = u'Не могу открыть файл для чтения {0}:\n{1}.'.format(
                fileName, forceString(inFile.errorString()))
            if self.auto:
                self.logError(msg)
                self.registerError({'ID': None})
            else:
                QtGui.QMessageBox.warning(self, u'Импорт номенклатуры', msg)
            return False

        progressBar.setMaximum(max(inFile.size(), 1))
        reader = CXmlStreamReader(self, self.groupNames, self.startElementName,
                                  self.logBrowser, True)
        reader.setDevice(inFile)
        params = {}
        success = False
        errorCount = 0

        self._db.transaction()

        if reader.readHeader():
            for name, row in reader.readData():
                progressBar.setValue(inFile.pos())
                QtGui.qApp.processEvents()

                if row:
                    success = self.processXmlRow(row, name, params)

                if not success or self.aborted:
                    self.registerError(row)
                    errorCount += 1

                    if self.aborted:
                        break
                else:
                    self.registerSuccess(row)

        self.log(u'импорт: %d обработано' % self.nProcessed)

        if not errorCount and not (
                reader.hasError() or self.aborted or not success):
            self._db.commit()
            self.log(u'Готово, удаляем `{0}`'.format(fileName))
            inFile.close()
            os.remove(fileName)
            return True
        else:
            self._db.rollback()
            self.log(u'Прервано')

            if self.aborted:
                self.log(u'! Прервано пользователем.')
            elif reader.hasError():
                self.log(u'! Ошибка: файл %s, %s' % (fileName,
                                                     reader.errorString()))
            elif errorCount:
                self.log(u'! Количество ошибок импорта: {0}'.format(errorCount))

            return False

# ******************************************************************************

    def processXmlRow(self, row, name, params):
        docType = forceInt(row.get('TYPE', -1))

        if docType == -1 or docType > self.lastKnownDocType:
            self.logError(u'Неизвестный тип документа')
            return False

        errList = self.processRequiredTags(row, name,
                                           self.requiredTags[docType])
        result = False

        if not errList:
            docId = row['ID']

            if docType == 0:
                result = self.processBalance(docId, row, name, params)
            elif docType == 1:
                result = self.proccessArrival(docId, row, name, params)
            elif docType == 2:
                result = self.processMovement(docId, row, name, params)
            elif docType == 3:
                result = self.processChargeOff(docId, row, name, params)
            else:
                self.setFieldName('ID')
                self.setBaseFieldName('DOC')
                self.logError(u'Документ {dId}: неизвестный тип документа '
                              u'{dType}.'.format(dId=docId, dType=docType))

            if result:
                self.nProcessed += 1
        else:
            for err, tags in errList:
                self.logError(u'{err} пропущен(ы) тэг(и): {tags} '.
                              format(err=err, tags=', '.join(tags)))

        return result

# ******************************************************************************

    def proccessArrival(self, docId, row, name, params):
        u'Импорт прихода на склад'

        stockMotion = {
            'type': 10,
            'number': row.get('NUMBER'),
            'date': QDateTime.fromString(row['DATE'], Qt.ISODate),
            'reason': row.get('REASON'),
            'reasonDate': QDate.fromString(row.get('REASON_DATE', ''),
                                           Qt.ISODate),
            'note': row.get('NOTE'),
        }

        if row.has_key('SUPPLIER_ORG'):
            supplierId = self.findOrgByInn(row['SUPPLIER_ORG']['INN'])

            if not supplierId:
                org = row['SUPPLIER_ORG']
                supplier = {
                    'fullName': org['NAME'],
                    'shortName': org.get('SHORT_NAME'),
                    'OGRN' : org.get('OGRN'),
                    'INN': org['INN'],
                    'KPP': org.get('KPP'),
                    'address' : org.get('ADDRESS'),
                }
                supplierId = self.addSupplierOrg(supplier)
                self.log(u'Добавлен новый поставщик: ИНН {inn}, `{name}`'
                         .format(inn=org['INN'], name=org['NAME']))

            stockMotion['supplierOrg_id'] = supplierId

        if row.has_key('SUP_ORG_PERSON'):
            stockMotion['supplierOrgPerson'] = row['SUP_ORG_PERSON']

        receiverCode = row['RECEIVER']['CODE']
        stockMotion['receiver_id'] = self.findOrgStructByCode(receiverCode)

        if not stockMotion['receiver_id']:
            self.setFieldName('CODE')
            self.setBaseFieldName('RECEIVER')
            self.logError(u'Документ {docId}: получатель с кодом `{code}` '
                          u'не найден'.format(docId=docId,
                                              code=receiverCode))
            return False

        if row.has_key('REC_PERSON'):
            receiverPersonCode = row['REC_PERSON']['ID']
            receiverPersonId = self.findPerson(receiverPersonCode)

            if not receiverPersonId:
                self.setFieldName('ID')
                self.setBaseFieldName('REC_PERSON')
                self.logError(u'Документ {docId}: ответственный за получени'
                              u'е (код `{code}`) не найден'.format(
                                  docId=docId, code=receiverPersonCode))
                return False

            stockMotion['receiverPerson_id'] = receiverPersonId

        stockMotionId = self.addStockMotion(stockMotion)
        items = (row['ITEM'] if isinstance(row['ITEM'], list)
                 else [row['ITEM']])

        for i in items:
            if not self.processStockMotionItem(
                    stockMotionId, i, docId, self._createNomenclature):
                return False

        return True

# ******************************************************************************

    def processMovement(self, docId, row, name, params):
        stockMotion = {
            'type': 0,
            'number': row.get('NUMBER'),
            'date': QDateTime.fromString(row['DATE'], Qt.ISODate),
            'reason': row.get('REASON'),
            'reasonDate': QDate.fromString(row.get('REASON_DATE', ''),
                                           Qt.ISODate),
            'note': row.get('NOTE'),
        }

        supplierCode = row['SUPPLIER']['CODE']
        supplierId = self.findOrgStructByCode(supplierCode)

        if not supplierId:
            self.setFieldName('CODE')
            self.setBaseFieldName('SUPPLIER')
            self.logError(u'Документ {docId}: склад с кодом {code} не '
                          u'найден.'.format(docId=docId, code=supplierCode))
            return False

        stockMotion['supplier_id'] = supplierId
        supPersonCode = row['SUP_PERSON']['ID']
        supPersonId = self.findPerson(supPersonCode)

        if not supPersonId:
            self.setFieldName('ID')
            self.setBaseFieldName('SUP_PERSON')
            self.logError(u'Документ {docId}: сотрудник с кодом {code} не '
                          u'найден'.format(docId=docId, code=supPersonCode))
            return False

        stockMotion['supplierPerson_id'] = supPersonId
        receiverCode = row['RECEIVER']['CODE']
        stockMotion['receiver_id'] = self.findOrgStructByCode(receiverCode)

        if not stockMotion['receiver_id']:
            self.setFieldName('CODE')
            self.setBaseFieldName('RECEIVER')
            self.logError(u'Документ {docId}: получатель с кодом `{code}` '
                          u'не найден'.format(docId=docId,
                                              code=receiverCode))
            return False

        if row.has_key('REC_PERSON'):
            receiverPersonCode = row['REC_PERSON']['ID']
            receiverPersonId = self.findPerson(receiverPersonCode)

            if not receiverPersonId:
                self.setFieldName('ID')
                self.setBaseFieldName('REC_PERSON')
                self.logError(u'Документ {docId}: ответственный за получени'
                              u'е (код `{code}`) не найден'.format(
                                  docId=docId, code=receiverPersonCode))
                return False

            stockMotion['receiverPerson_id'] = receiverPersonId

        requisitionId = forceRef(row.get('REC'))
        if requisitionId and not self.updateRequisition(row['REC']):
            self.logError(u'Документ {docId}: требование с идентификатором'
                          u'`{id}` не найдено'.format(
                              docId=docId, id=row['REC']))

        stockMotionId = self.addStockMotion(stockMotion)
        items = row['ITEM'] if isinstance(row['ITEM'], list) else [row['ITEM']]
        for i in items:
            if not self.processStockMotionItem(
                    stockMotionId, i, docId, self._createNomenclature,
                    requisitionId):
                return False

        return True


# ******************************************************************************

    def processBalance(self, docId, row, name, params):
        u'Обработка остатков'

        stockMotion = {
            'type': 1,
            'number': row.get('NUMBER'),
            'date': QDateTime.fromString(row['DATE'], Qt.ISODate),
            'reason': row.get('REASON'),
            'reasonDate': QDate.fromString(row.get('REASON_DATE', ''),
                                           Qt.ISODate),
            'note': row.get('NOTE'),
        }

        receiverCode = row['RECEIVER']['CODE']
        stockMotion['receiver_id'] = self.findOrgStructByCode(receiverCode)

        if not stockMotion['receiver_id']:
            self.setFieldName('CODE')
            self.setBaseFieldName('RECEIVER')
            self.logError(u'Документ {docId}: получатель с кодом `{code}` '
                          u'не найден'.format(docId=docId,
                                              code=receiverCode))
            return False

        stockMotion['supplier_id'] = stockMotion['receiver_id']

        if row.has_key('REC_PERSON'):
            receiverPersonCode = row['REC_PERSON']['ID']
            receiverPersonId = self.findPerson(receiverPersonCode)

            if not receiverPersonId:
                self.setFieldName('ID')
                self.setBaseFieldName('REC_PERSON')
                self.logError(u'Документ {docId}: ответственный за получени'
                              u'е (код `{code}`) не найден'.format(
                                  docId=docId, code=receiverPersonCode))
                return False

            stockMotion['receiverPerson_id'] = receiverPersonId
            stockMotion['supplierPerson_id'] = receiverPersonId

        stockMotionId = self.addStockMotion(stockMotion)
        items = row['ITEM'] if isinstance(row['ITEM'], list) else [row['ITEM']]
        for i in items:
            itemId = self.processStockMotionItem(
                stockMotionId, i, docId, self._createNomenclature)
            if not itemId:
                return False
            self.fillOldQntAndSum(itemId, stockMotion['supplier_id'])
        return True

# ******************************************************************************

    def processChargeOff(self, docId, row, name, params):
        u'Обработка списаний со склада'

        stockMotion = {
            'type': 7,
            'number': row.get('NUMBER'),
            'date': QDateTime.fromString(row['DATE'], Qt.ISODate),
            'reason': row.get('REASON'),
            'reasonDate': QDate.fromString(row.get('REASON_DATE', ''),
                                           Qt.ISODate),
            'note': row.get('NOTE'),
        }

        supplierCode = row['SUPPLIER']['CODE']
        supplierId = self.findOrgStructByCode(supplierCode)

        if not supplierId:
            self.setFieldName('CODE')
            self.setBaseFieldName('SUPPLIER')
            self.logError(u'Документ {docId}: склад с кодом {code} не '
                          u'найден.'.format(docId=docId, code=supplierCode))
            return False

        stockMotion['supplier_id'] = supplierId
        supPersonCode = row['SUP_PERSON']['ID']
        supPersonId = self.findPerson(supPersonCode)

        if not supPersonId:
            self.setFieldName('ID')
            self.setBaseFieldName('SUP_PERSON')
            self.logError(u'Документ {docId}: сотрудник с кодом {code} не '
                          u'найден'.format(docId=docId, code=supPersonCode))
            return False

        stockMotion['supplierPerson_id'] = supPersonId
        reasonId = self.findStockMotionItemReason(row['CANCEL_REASON'])

        stockMotionId = self.addStockMotion(stockMotion)
        items = row['ITEM'] if isinstance(row['ITEM'], list) else [row['ITEM']]

        for i in items:
            i['reason_id'] = reasonId
            if not self.processStockMotionItem(
                    stockMotionId, i, docId, self._createNomenclature):
                return False

        return True

# ******************************************************************************

    def processStockMotionItem(self, master_id, data, docId, addMissing,
                               requisitionId=None):
        u'Обрабатывает элемент движения'
        item = {
            'idx' : data['ID'],
            'batch' : data.get('BATCH'),
            'shelfTime': data.get('SHELF_TIME'),
            'qnt': data['QNT'],
            'sum': data.get('SUM'),
            'master_id': master_id,
            'reason_id': data.get('reason_id'),
        }

        QtGui.qApp.processEvents()
        nomenclature = data['NOMENCLATURE']
        nomenclatureId = self.findNomenclature(nomenclature['ID'])
        item['unit_id'] = self.ensureUnit(data['UNIT'])

        if not nomenclatureId:
            if addMissing:
                nomenclatureId = self.processNomenclature(nomenclature,
                                                          item['unit_id'])
                if not nomenclatureId:
                    return False

                self.logInfo(u'Добавлена новая позиция номенклатуры с кодом '
                             u'{0}'.format(nomenclature['ID']))
            else:
                self.setItemId(data['ID'])
                self.setFieldName('ID')
                self.setBaseFieldName('NOMENCLATURE')
                self.logError(u'Номенклатура с идентификатором {nId} '
                              u'не найдена.'.format(nId=nomenclature['ID']))
                return False

        if not self.checkNomenclatureUnit(nomenclatureId, item['unit_id']):
            self.setItemId(data['ID'])
            self.setFieldName('ID')
            self.setBaseFieldName('UNIT')
            self.logError(u'DOC_ID={docId}, ITEM={itemId}: единица учета не'
                          u' соответствует упаковочной и расходной единицам '
                          u'учета.'.format(docId=docId, itemId=data['ID']))
            return False

        item['medicalAidKind_id'] = self.findMedicalAidKind(data.get('MAK'))
        item['nomenclature_id'] = nomenclatureId

        if data.has_key('FINANCE'):
            item['finance_id'] = self.findFinanceByCode(data['FINANCE'])

        if data.has_key('SUM') and data.get('QNT', 0):
            item['price'] = forceDouble(data['SUM']) / forceDouble(data['QNT'])

        if requisitionId and not self.updateRequisitionItem(
                requisitionId, nomenclatureId, data['QNT']):
            self.logError(u'DOC_ID={docId}, ITEM={itemId}: отсутствует элемент'
                          u' требования `{rId}`'.format(
                            docId=docId, itemId=data['ID'], rId=requisitionId))

        return self.addStockMotionItem(item)

# ******************************************************************************

    def processNomenclature(self, data, unitId):
        u'Добавляет новый элемент в справочник номенклатуры'
        item = {
            'code': data['ID'],
            'name': data['TN_R'],
            'originName': data.get('TN_L'),
            'internationalNonproprietaryName' : data.get('MNN_R'),
            'mnnLatin': data.get('MNN_L'),
            'regionalCode' : data.get('REG_CODE'),
            'mnnCode': data.get('MNN_CODE'),
            'trnCode': data.get('TRN_CODE'),
            'ATC': data.get('ATC'),
            'producer': data.get('PRODUCER'),
            'dosageValue': data.get('DOSAGE'),
            'inDate': QDate.fromString(data.get('INDATE', ''), Qt.ISODate),
            'exDate': QDate.fromString(data.get('EXDATE', ''), Qt.ISODate),
            'packSize': data.get('PACK_SIZE'),
            'completeness': data.get('COMPL'),
        }

        if data.has_key('TYPE'):
            nType = data['TYPE']
            typeId = self.findNomenclatureType(nType['CODE'])

            if not typeId:
                kindId = None

                if data.has_key('KIND'):
                    nKind = data['KIND']
                    kindId = self.findNomenclatureKind(nKind['CODE'])

                    if not kindId:
                        classId = None

                        if data.has_key('CLASS'):
                            nClass = data['CLASS']
                            classId = self.findNomenclatureClass(nClass['CODE'])

                            if not classId:
                                classId = self.addNomenclatureClass(
                                    nClass['CODE'], nClass['NAME'])

                        kindId = self.addNomenclatureKind(nKind['CODE'],
                                                          nKind['NAME'],
                                                          classId)
                typeId = self.addNomenclatureType(nType['CODE'], nType['NAME'],
                                                  kindId)

            item['type_id'] = typeId

        for (field, key) in (('defaultStockUnit_id', 'STOCK_UNIT'),
                             ('defaultClientUnit_id', 'CLIENT_UNIT'),
                             ('unit_id', 'DOSAGE_UNIT')):
            item[field] = (self.ensureUnit(data[key]) if data.has_key(key)
                           else unitId)

        _id = self.addNomenclature(item)
        self.addNomenclatureUnitRatio(_id, data.get('UNIT_RATIO', 1),
                                      item['defaultStockUnit_id'],
                                      item['defaultClientUnit_id'])
        return _id

# ******************************************************************************

    def processRequiredTags(self, row, name, tagList, errPrefix=''):
        u"""Возвращает множество найденных обязательных тэгов в записи"""

        def describeError():
            err = name

            if name == 'DOC':
                err = u'Документ {docId}'.format(docId=row.get('ID', '?'))
            elif name == 'ITEM':
                err = u'позиция {itemId}'.format(itemId=row.get('ID', '?'))
            else:
                err = u'поле {tag}'.format(tag=name)

            return (u'{prefix} {err}'.format(prefix=errPrefix, err=err)).strip()

        presentTags = set()
        subresult = []
        requiredTags = set(tagList.get(name, tuple()))

        for key, val in row.iteritems():
            if key in requiredTags:
                presentTags.add(key)

            if isinstance(val, dict):
                subresult.extend(self.processRequiredTags(val, key, tagList,
                                                          describeError()))
            elif isinstance(val, list):
                for item in val:
                    subresult.extend(self.processRequiredTags(item, key,
                                                              tagList,
                                                              describeError()))

        absentTags = requiredTags.difference(presentTags)
        result = [(describeError(), absentTags), ] if absentTags else []
        result.extend(subresult)
        return result


    def checkNomenclatureUnit(self, nomenclatureId, unitId):
        record = self._db.getRecord(self._tblRbNomenclature,
                                    'defaultStockUnit_id, defaultClientUnit_id',
                                    nomenclatureId)
        defaultStockUnitId = forceRef(record.value(0)) if record else None
        defaultClientUnitId = forceRef(record.value(1)) if record else None
        return unitId in (defaultStockUnitId, defaultClientUnitId)


    def fillOldQntAndSum(self, itemId, supplierId):
        u"""Подбор значений для полей oldQnt и oldSum осуществляется по
            ITEM.NOMENCLATURE.ID, ITEM.BATCH, ITEM.SHELF_TIME и ITEM.UNIT."""
        record = self._db.getRecord(self._tblStockMotionItem, '*', itemId)

        if not record:
            return False

        params = {
            'nomenclatureId': forceRef(record.value('nomenclature_id')),
            'batch': forceString(record.value('batch')),
            'shelfTime': forceString(record.value('shelfTime')),
            'unitId': forceRef(record.value('unit_id')),
            'filter': self._tblStockMotion['supplier_id'].eq(supplierId),
        }

        qnt = getExistsNomenclatureAmount(*params)
        sum = getExistsNomenclatureAmountSum(*params)

        record.setValue('oldQnt', qnt)
        record.setValue('oldSum', sum)
        return self._db.updateRecord(self._tblStockMotionItem, record)


    def updateRequisition(self, requisitionId):
        u"""Обновляет требование по идентификатору"""
        record = self._db.getRecord(self._tblStockRequisition, '*', requisitionId)
        result = None
        if record:
            count = forceInt(record.value('stockMotionsCount'))
            record.setValue('stockMotionsCount', toVariant(count + 1))
            result = self._db.updateRecord(self._tblStockRequisition, record)
        return result


    def updateRequisitionItem(self, requisitionId, nomenclatureId, qnt):
        _tbl = self._tblStockRequisitionItem
        cond = [_tbl['nomenclature_id'].eq(nomenclatureId),
                _tbl['master_id'].eq(requisitionId)]
        record = self._db.getRecordEx(_tbl, '*', where=cond)
        result = None
        if record:
            count = forceDouble(record.value('satisfiedQnt'))
            record.setValue('satisfiedQnt', toVariant(count + forceDouble(qnt)))
            result = self._db.updateRecord(_tbl, record)
        return result

# ******************************************************************************

    def insertRecordByDict(self, table, data, cache=None, key=None):
        u'Добавляет новую запись в таблицу по словарю'
        record = table.newRecord()

        for _key, _val in data.iteritems():
            if _val:
                record.setValue(_key, toVariant(_val))

        result = self._db.insertRecord(table, record)

        if cache and key:
            cache[key] = result

        return result


    def addStockMotion(self, data):
        u'Добавляет новое движение ЛСиИМН'
        return self.insertRecordByDict(self._tblStockMotion, data)


    def addSupplierOrg(self, data):
        u'Добавляет нового поставщика в таблицу организаций'
        data['isSupplier'] = 1
        data['isActive'] = 1
        result = self.insertRecordByDict(self._tblOrganisation, data)
        self._cacheOrganisation[data['INN']] = result
        return result


    def addStockMotionItem(self, data):
        u'Добавляет новый элемент движения ЛСиИМН'
        return self.insertRecordByDict(self._tblStockMotionItem, data)


    def addNomenclature(self, data):
        u'Добавляет новый элемент в справочник номенклатуры'
        return self.insertRecordByDict(self._tblRbNomenclature, data,
                                       self._cacheNomenclature, data['code'])


    def addNomenclatureType(self, code, name, kindId):
        u'Добавляет новый элемент в справочник номенклатуры'
        data = {
            'code' : code,
            'name' : name,
            'kind_id': kindId,
        }
        return self.insertRecordByDict(self._tblRbNomenclatureType, data,
                                       self._cacheNomenclatureType, code)


    def addNomenclatureKind(self, code, name, classId):
        u'Добавляет новый элемент в справочник номенклатуры'
        data = {
            'code' : code,
            'name' : name,
            'class_id': classId,
        }
        return self.insertRecordByDict(self._tblRbNomenclatureKind, data,
                                       self._cacheNomenclatureKind, code)


    def addNomenclatureClass(self, code, name):
        u'Добавляет новый элемент в справочник номенклатуры'
        data = {
            'code' : code,
            'name' : name,
        }
        return self.insertRecordByDict(self._tblRbNomenclatureClass, data,
                                       self._cacheNomenclatureClass, code)


    def addUnit(self, code, name):
        u'Добавляет новую единицу измерения'
        data = {
            'code': code,
            'name': name,
        }
        masterId = self.insertRecordByDict(self._tblRbUnit, data)
        data = {
            'value': code,
            'master_id': masterId,
            'system_id': self._unitAccSystemId
        }
        self.insertRecordByDict(self._tblRbUnitIdentification, data)
        self._cacheRbUnit[code] = masterId
        return masterId


    def addNomenclatureUnitRatio(self, masterId, val, sourceId, targetId):
        u'Добавляет относительный коэффициент пересчета'
        data = {
            'master_id': masterId,
            'ratio': val,
            'sourceUnit_id': sourceId,
            'targetUnit_id': targetId,
        }
        return self.insertRecordByDict(self._tblRbNomenclatureUnitRatio, data)

# ******************************************************************************

    def findStockMotion(self, date, number):
        u'Ищет движение ЛСиИМН по дате и номеру'
        table = self._tblStockMotion
        cond = [table['date'].eq(date), table['number'].eq(number)]
        record = self._db.getRecordEx(table, 'id', where=cond)
        return forceRef(record.value(0)) if record else None


    def _findIdByKey(self, table, cond, key, cache, idField='id'):
        u'Кэшированный поиск идентификатора по ключу и условию'
        result = cache.get(key, -1)

        if result == -1:
            record = self._db.getRecordEx(table, idField, where=cond)
            result = forceRef(record.value(0)) if record else None
            cache[key] = result

        return result


    def _findRbItemByCode(self, table, code, cache, fieldName='code'):
        u'Кэшированный поиск по справочникам'
        cond = [table[fieldName].eq(code)]
        return self._findIdByKey(table, cond, code, cache)


    def _findRbItemByIdentificationCode(self, table, code, systemId, cache):
        u"""Поиск элемента справочника по коду через таблицу _Identification"""
        cond = [table['value'].eq(code),
                table['deleted'].eq(0),
                table['system_id'].eq(systemId)]
        return self._findIdByKey(table, cond, code, cache, 'master_id')


    def findOrgByInn(self, inn):
        u'Поиск организации по ИНН'
        table = self._tblOrganisation
        cond = table['INN'].eq(inn)
        return self._findIdByKey(table, cond, inn, self._cacheOrganisation)


    def findOrgStructByCode(self, code):
        u'Поиск подразделения по коду'
        return self._findRbItemByIdentificationCode(
            self._tblOrgStructIdentification, code, self._warehouseAccSystemId,
            self._cacheOrgStuct)


    def findPerson(self, code):
        u'Поиск сотрудника по коду'
        return self._findRbItemByIdentificationCode(
            self._tblPersonIdentification, code, self._personAccSystemId,
            self._cachePerson)


    def findNomenclature(self, code):
        u'Поиск номенклатуры по коду'
        return self._findRbItemByCode(self._tblRbNomenclature, code,
                                      self._cacheNomenclature)


    def findFinanceByCode(self, code):
        u'Поиск источника финансирования по коду'
        return self._findRbItemByCode(self._tblRbFinance, code,
                                      self._cacheRbFinance)


    def findUnitByCode(self, code):
        u'Поиск единицы измерения по коду'
        return self._findRbItemByIdentificationCode(
            self._tblRbUnitIdentification, code, self._unitAccSystemId,
            self._cacheRbUnit)


    def findUnitByName(self, name):
        u'Поиск единицы измерения по коду'
        return self._findRbItemByCode(self._tblRbUnit, name,
                                      self._cacheRbUnitName, 'name')


    def findNomenclatureType(self, code):
        u'Поиск типа номенклатуры'
        return self._findRbItemByCode(self._tblRbNomenclatureType, code,
                                      self._cacheNomenclatureType)


    def findNomenclatureKind(self, code):
        u'Поиск типа номенклатуры'
        return self._findRbItemByCode(self._tblRbNomenclatureKind, code,
                                      self._cacheNomenclatureKind)


    def findNomenclatureClass(self, code):
        u'Поиск класса номенклатуры'
        return self._findRbItemByCode(self._tblRbNomenclatureClass, code,
                                      self._cacheNomenclatureClass)


    def findStockMotionItemReason(self, code):
        u'Поиск причины списания'
        return self._findRbItemByCode(self._tblRbStockMotionItemReason, code,
                                      self._cacheRbStockMotionItemReason)


    def findMedicalAidKind(self, code):
        u'Поиск вида медпомощи'
        return self._findRbItemByCode(self._tblRbMedicalAidKind, code,
                                      self._cacheRbMedicalAidKind)

# ******************************************************************************

    def ensureUnit(self, data):
        u'Ищет ед.измерения по коду и имени. При отсутствии оной добавляет её'
        unitId = self.findUnitByCode(data['CODE'])

        if not unitId:
            unitId = self.findUnitByName(data['NAME'])
        if not unitId:
            unitId = self.addUnit(data['CODE'], data['NAME'])
        return unitId

# ******************************************************************************

    def registerSuccess(self, row):
        if self._logSuccess:
            self._successLog.writeRecord(row['ID'])


    def registerError(self, row):
        if self._logErrors:
            self._errorLog.writeRecord(row['ID'], comment=self._lastMsg,
                                       fieldName=self._logFieldName,
                                       baseFieldName=self._logBaseFieldName,
                                       itemId=self._logItemId)


    def setFieldName(self, val):
        self._logFieldName = val


    def setBaseFieldName(self, val):
        self._logBaseFieldName = val


    def setItemId(self, val):
        self._logItemId = val
