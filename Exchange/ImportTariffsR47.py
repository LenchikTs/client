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
u"""Импорт тарифа из XML для Ленобласти"""

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDate, QFile, QString

from library.Utils import forceBool, forceDouble, forceString, toVariant

from Accounting.Tariff import CTariff
from Exchange.Cimport import CXMLimport, CImportTariffsMixin

from Exchange.Ui_ImportTariffsR47 import Ui_ImportTariffs


def ImportTariffsR47(widget, contractId, begDate, endDate, tariffList,
        tariffExpenseItems, tariffCoefficientItems):
    u'Создает диалог импорта тарифов для 47 региона'
    appPrefs = QtGui.qApp.preferences.appPrefs

    fileName = forceString(appPrefs.get('ImportTariffsR47FileName', ''))
    fullLog = forceBool(appPrefs.get('ImportTariffsR47FullLog', ''))

    dlg = CImportTariffs(widget, fileName, contractId,
                         tariffList, tariffExpenseItems, tariffCoefficientItems)

    dlg.chkFullLog.setChecked(fullLog)

    dlg.exec_()

    appPrefs['ImportTariffsR47FileName'] = toVariant(dlg.fileName)
    appPrefs['ImportTariffsR47FullLog'] = toVariant(dlg.chkFullLog.isChecked())
    return ((not dlg.abort), dlg.tariffList, dlg.tariffExpenseItems,
        dlg.tariffCoefficientItems)


class CImportTariffs(QtGui.QDialog, Ui_ImportTariffs, CXMLimport,
        CImportTariffsMixin):
    u'Класс диалога импорта тарифов'

    rowFields = ('STARTDATE', 'ENDDATE')
    valueFields = ('VALUE', )
    rowGroup = {
        'TITLE': {'fields': valueFields},
        'TARIF_CODE': {'fields': valueFields},
        'SUMM': {'fields': valueFields},
        'AVG_CASE_PERIOD': {'fields': valueFields},
        'MIN_CASE_PERIOD': {'fields': valueFields},
        'PRVS_CODE': {'fields': valueFields},
        'IDSP_CODE': {'fields': valueFields},
        'USL_MP': {'fields': valueFields},
        'AMB_CODE': {'fields': valueFields},
        'LPU_LEVEL': {'fields': valueFields},
        'UCH_SL' : {'fields': valueFields},
    }

    tariffsGroupName = 'DATA'
    tariffsGroup = {
        'ROW':  {'fields': rowFields, 'subGroup': rowGroup},
    }

    mapTariffCodeToEventTypeCode = {u'ЗН': u'16', u'ЗП': u'17', u'ЗЛ': u'18',
        u'СМП': u'19'}


    def __init__(self, parent, fileName, contractId,
            tariffList, tariffExpenseItems, tariffCoefficientItems):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        CXMLimport.__init__(self)
        CImportTariffsMixin.__init__(self, self.log, tariffList,
            tariffExpenseItems)

        self.fileName = fileName
        self.tariffCoefficientItems = list(tariffCoefficientItems)
        self.contractId = contractId

        if fileName:
            self.edtFileName.setText(fileName)
            self.btnImport.setEnabled(True)

        self._unitIdCache = {}
        self.findUnitId = lambda code: self.findIdByCode(code,
            'rbMedicalAidUnit', self._unitIdCache)

        self._serviceCache = {}
        self.findService = lambda code, name: self.lookupIdByCodeName(code,
            name, self.tblService, self._serviceCache)

        self.cmbTariffType.addItems(CTariff.tariffTypeNames)
        _filter = u'EventType.code IN (\'ЗН\', \'ЗП\', \'ЗЛ\', \'СМП\')'
        self.cmbEventType.setTable('EventType', False, _filter)
        self.cmbEventType.setCurrentIndex(0)


    def setImportMode(self, flag):
        u'Выключает поля ввода во время импорта'

        self.chkFullLog.setEnabled(not flag)
        self.btnSelectFile.setEnabled(not flag)
        self.edtFileName.setEnabled(not flag)
        self.cmbOrgLevel.setEnabled(not flag)
        self.cmbTariffType.setEnabled(not flag)
        self.edtOrgInfis.setEnabled(not flag)
        self.cmbEventType.setEnabled(not flag)


    def startImport(self):
        u'Реализация импорта тарифов'
        fileName = self.edtFileName.text()

        if not fileName:
            return

        self.setImportMode(True)
        params = {
            'orgInfis': forceString(self.edtOrgInfis.value()),
            'orgLevel': forceString(self.cmbOrgLevel.currentText()),
            'tariffType': self.cmbTariffType.currentIndex(),
            'tariffCode': self.mapTariffCodeToEventTypeCode[
                    forceString(self.cmbEventType.code())],
            'eventTypeId': self.cmbEventType.value()
        }


        inFile = QFile(fileName)
        if not inFile.open(QFile.ReadOnly | QFile.Text):
            QtGui.QMessageBox.warning(self, u'Импорт тарифов для договора',
                      QString(u'Не могу открыть файл для чтения %1:\n%2.')
                      .arg(fileName)
                        .arg(inFile.errorString()))
            return

        self.progressBar.setFormat(u'%v байт')
        self.progressBar.setMaximum(max(inFile.size(), 1))
        self.lblStatus.setText('')

        self.setDevice(inFile)

        while not self.atEnd():
            self.readNext()

            if self.isStartElement():
                if self.name() == self.tariffsGroupName:
                    xmlData = self.readGroupEx(self.tariffsGroupName, tuple(),
                        False, self.tariffsGroup)
                else:
                    self.raiseError(u'Неверный формат данных.')

            if self.hasError():
                break

        if not self.hasError():
            self.processData(xmlData, params)
            self.progressBar.setText(u'Готово')
        else:
            self.progressBar.setText(u'Прервано')
            if self.abort:
                self.err2log(u'! Прервано пользователем.')
            else:
                self.err2log(u'! Ошибка: файл %s, %s' % (fileName,
                    self.errorString()))

        inFile.close()
        self.setImportMode(False)
        self.fileName = fileName


    def processData(self, data, params):
        u'Фукнция обработки данных'
        self.progressBar.setFormat(u'Обработка данных...')
        self.progressBar.setMaximum(0)

        for row in data.get('ROW', []):
            price = forceDouble(row['SUMM']['VALUE']) / 100
            tariffCode = row['TARIF_CODE']['VALUE'].strip()

            if price <= 0.0:
                continue

            if (params['orgInfis'] != row['AMB_CODE']['VALUE'].strip()
                or params['orgLevel'] != row['LPU_LEVEL']['VALUE'].strip()
                or params['tariffCode'] != tariffCode[2:4]):
                continue

            begDate = QDate.fromString(row['STARTDATE'], Qt.ISODate)
            endDate = QDate.fromString(row['ENDDATE'], Qt.ISODate)
            serviceCode = forceString(row['TARIF_CODE']['VALUE'].strip())
            serviceName = forceString(row['TITLE']['VALUE'].strip())
            serviceId = self.findService(serviceCode, serviceName)

            if not serviceId:
                self.err2log(u'Услуга не найдена: код `%s`  наименование `%s`' %
                    (serviceCode, serviceName))
                continue

            unitCode = forceString(row['IDSP_CODE']['VALUE'])
            unitId = self.findUnitId(unitCode)

            if not unitId:
                self.err2log(u'Модуль не найден: `%s`' % unitCode)

            tariff = self.tblContract_Tariff.newRecord()
            tariff.setValue('price', toVariant(price))
            tariff.setValue('service_id', toVariant(serviceId))
            tariff.setValue('master_id', toVariant(self.contractId))
            tariff.setValue('begDate', toVariant(begDate))
            tariff.setValue('endDate', toVariant(endDate))
            tariff.setValue('tariffType', toVariant(params['tariffType']))
            tariff.setValue('unit_id', toVariant(unitId))
            tariff.setValue('eventType_id', toVariant(params['eventTypeId']))
            self.addOrUpdateTariff(serviceCode, tariff, [])

            QtGui.qApp.processEvents()
            self.progressBar.step()

        self.progressBar.setMaximum(100)
        self.progressBar.setValue(100)
