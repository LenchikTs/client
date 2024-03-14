# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2022 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
u"""Импорт тарифов для Ростовской области"""

import os

from PyQt4              import QtGui
from PyQt4.QtCore       import QDate, pyqtSignature
from library.dbfpy.dbf  import Dbf
from library.Utils      import forceString, toVariant, forceRef, forceDouble
from xml.etree          import ElementTree

from Exchange.Ui_ImportTariffsR61 import Ui_Dialog


def importTariffsR61(widget, contractId, begDate, endDate, tariffList,
                     tariffExpenseItems, _):
    u"""Запускает мастер импорта тарифов для Ростова"""

    dlg = CImportTariffs(widget, contractId, begDate, endDate, tariffList, tariffExpenseItems)
    dlg.exec_()
    return not dlg.abort, [], [], []


class CImportTariffs(QtGui.QDialog, Ui_Dialog):
    u"""Мастер импорта тарифов для Ростова"""

    def __init__(self, parent, contractId, begDate, endDate, tariffList, tariffExpenseItems):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.contractId = contractId
        tariffTypes = [u'visit', u'event', u'action (кол-во)', u'визит-день', u'койко-день', u'action (УЕТ)', u'койка-профиль', u'визит по мероприятию', u'Визиты по МЭС', u'Событие по МЭС', u'Событие по МЭС (длит.)', u'визиты по профилю', u'Событие по МЭС (уровень)', u'КСГ']
        tariffTypesClose = [u'не задано'] + tariffTypes

        self.cmbFKSGEventType.setTable('EventType')
        self.cmbFKSGEventType.setValue(None)
        self.cmbFKSGUnit.setTable('rbMedicalAidUnit')
        self.cmbFKSGUnit.setValue(None)
        self.cmbFKSGTariffType.addItems(tariffTypes)
        self.cmbFKSGEventTypeClose.setTable('EventType')
        self.cmbFKSGEventTypeClose.setValue(None)
        self.cmbFKSGTariffTypeClose.addItems(tariffTypesClose)

        self.cmbVMPUnit.setTable('rbMedicalAidUnit')
        self.cmbVMPUnit.setValue(None)
        self.cmbVMPEventType.setTable('EventType')
        self.cmbVMPEventType.setValue(None)
        self.cmbVMPTariffType.addItems(tariffTypes)
        self.cmbVMPEventTypeClose.setTable('EventType')
        self.cmbVMPEventTypeClose.setValue(None)
        self.cmbVMPTariffTypeClose.addItems(tariffTypesClose)

        self.cmbAppUnit.setTable('rbMedicalAidUnit')
        self.cmbAppUnit.setValue(None)
        self.cmbAppEventType.setTable('EventType')
        self.cmbAppEventType.setValue(None)
        self.cmbAppTariffType.addItems(tariffTypes)
        self.cmbAppEventTypeClose.setTable('EventType')
        self.cmbAppEventTypeClose.setValue(None)
        self.cmbAppTariffTypeClose.addItems(tariffTypesClose)

        self.abort = False
        self.btnFKSGImport.setEnabled(False)
        self.btnVMPImport.setEnabled(False)
        self.btnAppImport.setEnabled(False)


    def startImportFKSG(self):
        self.nSkipped = 0
        self.nAdded = 0
        self.nUpdated = 0
        self.nProcessed = 0
        self.log.clear()
        if not self.contractId:
            return

        pathXml = forceString(self.edtFKSGXml.text())
        xmlData = None
        if pathXml:
            xmlData = self.loadFKSGXml(pathXml, self.edtFKSGDATE_IN.date())
            if not xmlData:
                self.log.append(u'На указанную дату не найдено КСГ в xml-файле')
                return

        db = QtGui.qApp.db
        tableContractTariff = db.table('Contract_Tariff')

        dbfTariff = Dbf(forceString(self.edtFKSGTARIF.text()), readOnly=True, encoding='cp866')
        if not self.checkFKSG_DBF(dbfTariff):
            dbfTariff.close()
            self.log.append(u'Структура DBF не соответствует шаблону')
            self.abort = True
            return

        eventTypeId = self.cmbFKSGEventType.value()
        tariffType = self.cmbFKSGTariffType.currentIndex()
        unitId = self.cmbFKSGUnit.value()
        cceTableKOEFZid = forceRef(db.translate('rbExpenseServiceItem', 'name', 'KOEF_Z', 'id'))
        cceTableKURVid = forceRef(db.translate('rbExpenseServiceItem', 'name', 'KURV', 'id'))
        cceTableKUPRid = forceRef(db.translate('rbExpenseServiceItem', 'name', 'KUPR', 'id'))
        cceTableMILBOLDNid = forceRef(db.translate('rbExpenseServiceItem', 'name', 'MILBOLDN', 'id'))
        cceTableRSTLid = forceRef(db.translate('rbExpenseServiceItem', 'name', 'KOEF_SHORT_RSTL', 'id'))
        cceTableZPid = forceRef(db.translate('rbExpenseServiceItem', 'name', 'ZP', 'id'))

        if not cceTableKOEFZid:
            self.log.append(u'Не найден rbExpenseServiceItem с именем KOEF_Z')
            self.abort = True
            return
        if not cceTableKURVid:
            self.log.append(u'Не найден rbExpenseServiceItem с именем KURV')
            self.abort = True
            return
        if not cceTableKUPRid:
            self.log.append(u'Не найден rbExpenseServiceItem с именем KUPR')
            self.abort = True
            return
        if bool(xmlData) and not cceTableMILBOLDNid:
            self.log.append(u'Не найден rbExpenseServiceItem с именем MILBOLDN')
            self.abort = True
            return
        if bool(xmlData) and not cceTableRSTLid:
            self.log.append(u'Не найден rbExpenseServiceItem с именем KOEF_SHORT_RSTL')
            self.abort = True
            return
        if bool(xmlData) and not cceTableZPid:
            self.log.append(u'Не найден rbExpenseServiceItem с именем ZP')
            self.abort = True
            return

        for record in dbfTariff:
            serviceCode = forceString(record[u'CODE_KSG'])
            stoim = forceDouble(record[u'STOIM'])
            begDate = record[u'DATAN']
            endDate = record[u'DATAK']
            tariffRecord = tableContractTariff.newRecord()
            tariffRecord.setValue('master_id', toVariant(self.contractId))
            tariffRecord.setValue('eventType_id', toVariant(eventTypeId))
            tariffRecord.setValue('tariffType', toVariant(tariffType))
            tariffRecord.setValue('service_id', toVariant(self.getServiceId(serviceCode)))
            tariffRecord.setValue('begDate', toVariant(QDate(begDate.year, begDate.month, begDate.day)))
            tariffRecord.setValue('endDate', toVariant(QDate(endDate.year, endDate.month, endDate.day)))
            tariffRecord.setValue('unit_id', toVariant(unitId))
            tariffRecord.setValue('price', toVariant(stoim))
            contractTariffId = db.insertRecord(tableContractTariff, tariffRecord)
            self.nAdded += 1
            self.nProcessed += 1

            KOEF_Z = record[u'KOEF_Z']
            KURV = record[u'KURV']
            KUPR = record[u'KUPR']
            self.addCompositionExpence(contractTariffId, cceTableKOEFZid, KOEF_Z)
            self.addCompositionExpence(contractTariffId, cceTableKUPRid, KUPR)
            self.addCompositionExpence(contractTariffId, cceTableKURVid, KURV)
            if xmlData:
                props = xmlData.get(serviceCode)
                if not props:
                    continue
                self.addCompositionExpence(contractTariffId, cceTableMILBOLDNid, props['SHORT_DAYS'])
                self.addCompositionExpence(contractTariffId, cceTableRSTLid, props['SHORT_RSTL'])
                self.addCompositionExpence(contractTariffId, cceTableZPid, props['ZP'])

        dbfTariff.close()
        self.log.append(u'добавлено: %d; изменено: %d' % (self.nAdded, self.nUpdated))
        self.log.append(u'пропущено: %d; обработано: %d' % (self.nSkipped, self.nProcessed))
        self.log.append(u'готово')


    def startCloseFKSG(self):
        date = self.edtFKSGEndDate.date()
        begDate = self.edtFKSGPeriodBeg.date()
        endDate = self.edtFKSGPeriodEnd.date()
        eventTypeId = self.cmbFKSGEventTypeClose.value()
        tariffType = self.cmbFKSGTariffTypeClose.currentIndex()
        self.closeTariffs(date, begDate, endDate, eventTypeId, tariffType)


    def checkFKSG_DBF(self, dbf):
        result = u'CODE_KSG' in dbf.fieldNames
        result = result and u'KOEF_Z' in dbf.fieldNames
        result = result and u'KURV' in dbf.fieldNames
        result = result and u'KUPR' in dbf.fieldNames
        result = result and u'STOIM' in dbf.fieldNames
        result = result and u'DATAN' in dbf.fieldNames
        result = result and u'DATAK' in dbf.fieldNames
        return result


    def checkVMP_DBF(self, dbf):
        result = u'KOIKA' in dbf.fieldNames
        result = result and u'STOIM' in dbf.fieldNames
        result = result and u'DATAN' in dbf.fieldNames
        result = result and u'DATAK' in dbf.fieldNames
        return result


    def checkAPP_DBF(self, dbf):
        result = u'KSPEC' in dbf.fieldNames
        result = result and u'STOIM' in dbf.fieldNames
        result = result and u'DATAN' in dbf.fieldNames
        result = result and u'DATAK' in dbf.fieldNames
        return result


    def loadFKSGXml(self, filepath, date):
        tagName = os.path.basename(os.path.splitext(filepath)[0]) + '_ITEM'
        root = ElementTree.parse(filepath).getroot()
        data = {}
        for item in root.findall(tagName):
            props = {}
            for p in item:
                props[p.tag] = p.text
                if p.tag == 'DATE_IN':
                    tagDate = QDate.fromString(p.text, 'dd.MM.yyyy')
                    if tagDate != date:
                        props = {}
                        break
            if props:
                ksg = props['KSG']
                data[ksg] = props
        return data


    def getServiceId(self, code):
        db = QtGui.qApp.db
        table = db.table('rbService')
        record = db.getRecordEx(table, table['id'], table['code'].eq(code))
        if record:
            return forceRef(record.value('id'))
        return None


    def addCompositionExpence(self, masterId, rbTableId, value):
        table = QtGui.qApp.db.table('Contract_CompositionExpence')
        record = table.newRecord()
        record.setValue('master_id', toVariant(masterId))
        record.setValue('rbTable_id', toVariant(rbTableId))
        record.setValue('sum', toVariant(float(value)))
        QtGui.qApp.db.insertRecord(table, record)


    def startImportVMP(self):
        self.nSkipped = 0
        self.nAdded = 0
        self.nUpdated = 0
        self.nProcessed = 0
        self.log.clear()
        if not self.contractId:
            return

        db = QtGui.qApp.db
        tableContractTariff = db.table('Contract_Tariff')

        dbfStactar = Dbf(forceString(self.edtVMPSTACTAR.text()), readOnly=True, encoding='cp866')
        if not self.checkVMP_DBF(dbfStactar):
            dbfStactar.close()
            self.log.append(u'Структура DBF не соответствует шаблону')
            self.abort = True
            return

        eventTypeId = self.cmbVMPEventType.value()
        tariffType = self.cmbVMPTariffType.currentIndex()
        unitId = self.cmbVMPUnit.value()
        for record in dbfStactar:
            serviceCode = forceString(record[u'KOIKA'])
            begDate = record[u'DATAN']
            endDate = record[u'DATAK']
            serviceId = self.getServiceId(serviceCode)
            if not serviceId:
                self.log.append(u'Код услуги "%s" не найден' % serviceCode)
                self.nSkipped += 1
                continue

            tariffRecord = tableContractTariff.newRecord()
            tariffRecord.setValue('master_id', toVariant(self.contractId))
            tariffRecord.setValue('eventType_id', toVariant(eventTypeId))
            tariffRecord.setValue('tariffType', toVariant(tariffType))
            tariffRecord.setValue('service_id', toVariant(serviceId))
            tariffRecord.setValue('begDate', toVariant(QDate(begDate.year, begDate.month, begDate.day)))
            tariffRecord.setValue('endDate', toVariant(QDate(endDate.year, endDate.month, endDate.day)))
            tariffRecord.setValue('unit_id', toVariant(unitId))
            db.insertRecord(tableContractTariff, tariffRecord)
            self.nAdded += 1
            self.nProcessed += 1

        dbfStactar.close()
        self.log.append(u'добавлено: %d; изменено: %d' % (self.nAdded, self.nUpdated))
        self.log.append(u'пропущено: %d; обработано: %d' % (self.nSkipped, self.nProcessed))
        self.log.append(u'готово')


    def startCloseVMP(self):
        date = self.edtVMPEndDate.date()
        begDate = self.edtVMPPerionBeg.date()
        endDate = self.edtVMPPerionEnd.date()
        eventTypeId = self.cmbVMPEventTypeClose.value()
        tariffType = self.cmbVMPTariffTypeClose.currentIndex()
        self.closeTariffs(date, begDate, endDate, eventTypeId, tariffType)


    def startImportApp(self):
        self.nSkipped = 0
        self.nAdded = 0
        self.nUpdated = 0
        self.nProcessed = 0
        self.log.clear()
        if not self.contractId:
            return

        db = QtGui.qApp.db
        tableContractTariff = db.table('Contract_Tariff')

        dbfPoliktar = Dbf(forceString(self.edtAPPPOLIKTAR.text()), readOnly=True, encoding='cp866')
        if not self.checkAPP_DBF(dbfPoliktar):
            dbfPoliktar.close()
            self.log.append(u'Структура DBF не соответствует шаблону')
            self.abort = True
            return

        eventTypeId = self.cmbAppEventType.value()
        tariffType = self.cmbAppTariffType.currentIndex()
        unitId = self.cmbAppUnit.value()
        for record in dbfPoliktar:
            serviceCode = forceString(record[u'KSPEC'])
            begDate = record[u'DATAN']
            endDate = record[u'DATAK']
            serviceId = self.getServiceId(serviceCode)
            if not serviceId:
                self.log.append(u'Код услуги "%s" не найден' % serviceCode)
                self.nSkipped += 1
                continue

            tariffRecord = tableContractTariff.newRecord()
            tariffRecord.setValue('master_id', toVariant(self.contractId))
            tariffRecord.setValue('eventType_id', toVariant(eventTypeId))
            tariffRecord.setValue('tariffType', toVariant(tariffType))
            tariffRecord.setValue('service_id', toVariant(serviceId))
            tariffRecord.setValue('begDate', toVariant(QDate(begDate.year, begDate.month, begDate.day)))
            tariffRecord.setValue('endDate', toVariant(QDate(endDate.year, endDate.month, endDate.day)))
            tariffRecord.setValue('unit_id', toVariant(unitId))
            db.insertRecord(tableContractTariff, tariffRecord)
            self.nAdded += 1
            self.nProcessed += 1

        dbfPoliktar.close()
        self.log.append(u'добавлено: %d; изменено: %d' % (self.nAdded, self.nUpdated))
        self.log.append(u'пропущено: %d; обработано: %d' % (self.nSkipped, self.nProcessed))
        self.log.append(u'готово')


    def startCloseApp(self):
        date = self.edtVMPEndDate.date()
        begDate = self.edtVMPPerionBeg.date()
        endDate = self.edtVMPPerionEnd.date()
        eventTypeId = self.cmbVMPEventTypeClose.value()
        tariffType = self.cmbVMPTariffTypeClose.currentIndex()
        self.closeTariffs(date, begDate, endDate, eventTypeId, tariffType)


    def closeTariffs(self, endDate, periodBeg, periodEnd, eventTypeId, tariffType):
        self.nSkipped = 0
        self.nAdded = 0
        self.nUpdated = 0
        self.nProcessed = 0
        self.log.clear()
        if not self.contractId:
            return

        db = QtGui.qApp.db
        table = db.table('Contract_Tariff')
        cond = [
            table['master_id'].eq(self.contractId),
        ]
        if periodBeg:
            cond.append(table['begDate'].dateGe(periodBeg))
        if periodEnd:
            cond.append(table['begDate'].dateLe(periodEnd))
        if eventTypeId:
            cond.append(table['eventType_id'].eq(eventTypeId))
        if tariffType:
            cond.append(table['tariffType'].eq(tariffType-1))

        idList = db.getIdList(table, 'id', cond)
        if idList:
            stmt = 'UPDATE Contract_Tariff SET %s WHERE %s'
            db.query(stmt % (table['endDate'].eq(endDate), table['id'].inlist(idList)))
            self.nUpdated += len(idList)
            self.nProcessed += len(idList)

        self.log.append(u'добавлено: %d; изменено: %d' % (self.nAdded, self.nUpdated))
        self.log.append(u'пропущено: %d; обработано: %d' % (self.nSkipped, self.nProcessed))
        self.log.append(u'готово')


    @pyqtSignature('bool')
    def on_btnFKSGSelectDBF_clicked(self, checked=False):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
            u'Укажите файл с данными', self.edtFKSGTARIF.text(),
            u'Файлы DBF (*.dbf)')
        self.edtFKSGTARIF.setText(fileName)


    @pyqtSignature('bool')
    def on_btnFKSGSelectXml_clicked(self, checked=False):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
            u'Укажите файл с данными', self.edtFKSGXml.text(),
            u'Файлы XML (*.xml)')
        self.edtFKSGXml.setText(fileName)


    @pyqtSignature('bool')
    def on_btnVMPSelectDBF_clicked(self, checked=False):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
            u'Укажите файл с данными', self.edtFKSGTARIF.text(),
            u'Файлы DBF (*.dbf)')
        self.edtFKSGTARIF.setText(fileName)


    @pyqtSignature('bool')
    def on_btnAppSelectPOLIKTAR_clicked(self, checked=False):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
            u'Укажите файл с данными', self.edtAPPPOLIKTAR.text(),
            u'Файлы DBF (*.dbf)')
        self.edtAPPPOLIKTAR.setText(fileName)
        self.btnAppImport.setEnabled(bool(fileName))


    @pyqtSignature('QString')
    def on_edtFKSGTARIF_textChanged(self, text):
        self.btnFKSGImport.setEnabled(bool(text) and bool(self.edtFKSGXml.text()))


    @pyqtSignature('QString')
    def on_edtFKSGXml_textChanged(self, text):
        self.btnFKSGImport.setEnabled(bool(text) and bool(self.edtFKSGTARIF.text()))


    @pyqtSignature('QString')
    def on_edtVMPSTACTAR_textChanged(self, text):
        self.btnVMPImport.setEnabled(bool(text))


    @pyqtSignature('QString')
    def on_edtAPPPOLIKTAR_textChanged(self, text):
        self.btnAppImport.setEnabled(bool(text))


    @pyqtSignature('bool')
    def on_btnFKSGImport_clicked(self, checked=False):
        self.startImportFKSG()


    @pyqtSignature('bool')
    def on_btnFKSGClose_clicked(self, checked=False):
        self.startCloseFKSG()


    @pyqtSignature('bool')
    def on_btnVMPImport_clicked(self, checked=False):
        self.startImportVMP()


    @pyqtSignature('bool')
    def on_btnVMPClose_clicked(self, checked=False):
        self.startCloseVMP()


    @pyqtSignature('bool')
    def on_btnAppImport_clicked(self, checked=False):
        self.startImportApp()


    @pyqtSignature('bool')
    def on_btnAppClose_clicked(self, checked=False):
        self.startCloseApp()
