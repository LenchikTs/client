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
u"""Импорт тарифа в Мурманске"""

import os

from PyQt4 import QtGui
from PyQt4.QtCore import QDir, pyqtSignature

from library.dbfpy.dbf import Dbf
from library.Utils import (forceString, toVariant, forceRef,
                           forceStringEx, forceDouble, forceBool, forceDate)

from Accounting.Tariff import CTariff
from Exchange.Cimport import CDBFimport, CImportTariffsMixin

from Exchange.Ui_ImportTariffsR51 import Ui_Dialog


def importTariffsR51(widget, contractId, begDate, endDate, tariffList,
                     tariffExpenseItems, _):
    u"""Запускает мастер импорта тарифов для Мурманска"""

    dlg = CImportTariffs(widget, contractId, begDate, endDate, tariffList,
                       tariffExpenseItems)
    dlg.edtFileName.setText(forceString(QtGui.qApp.preferences.appPrefs.get('ImportTariffR51FileName', '')))
    dlg.edtToothRbDir.setText(forceString(QtGui.qApp.preferences.appPrefs.get('ImportTariffR51ToothRbDir', '')))
    dlg.edtLpuCode.setText(forceString(QtGui.qApp.preferences.appPrefs.get('ImportTariffR51LpuCode', '')))
    dlg.exec_()
    QtGui.qApp.preferences.appPrefs['ImportTariffR51FileName'] = \
        toVariant(dlg.edtFileName.text())
    QtGui.qApp.preferences.appPrefs['ImportTariffR51ToothRbDir'] = \
        toVariant(dlg.edtToothRbDir.text())
    QtGui.qApp.preferences.appPrefs['ImportTariffR51LpuCode'] = \
        toVariant(dlg.edtLpuCode.text())
    return not dlg.abort, dlg.tariffList, dlg.tariffExpenseItems, []


class CImportTariffs(QtGui.QDialog, Ui_Dialog, CDBFimport, CImportTariffsMixin):
    u"""Мастер импорта тарифов для Мурманска"""

    # название поля, код затраты
    expenseServiceMatureFields2014 = (('TARIF_1', '1'), ('TARIF_2', '2'),
                        ('TARIF_3', '3'), ('TARIF_4', '4'), ('TARIF_41', '5'))
    expenseServiceChildFields2014 = (('TARIF_5', '1'), ('TARIF_6', '2'),
                        ('TARIF_7', '3'), ('TARIF_8', '4'), ('TARIF_81', '5'))
    expenseVisitChildFields2014 = (('TARIF_A1', '1'), ('TARIF_A2', '2'),
                        ('TARIF_A3', '3'), ('TARIF_A4', '4'), ('TARIF_A6', '5'))
    expenseToothMatureFields2014 = expenseServiceMatureFields2014
    expenseToothChildFields2014 = expenseServiceChildFields2014
    expenseToothMatureFields2015 = (('TARIF_1', '6'), ('TARIF_2', '7'),
                                    ('TARIF_3', '8'), ('TARIF_4', '5'))
    expenseToothChildFields2015 = (('TARIF_5', '6'), ('TARIF_6', '7'),
                                   ('TARIF_7', '8'), ('TARIF_8', '5'))

    def __init__(self, parent, contractId, begDate, endDate, tariffList,
                 tariffExpenseItems):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        CDBFimport.__init__(self, self.log)
        CImportTariffsMixin.__init__(self, self.log, tariffList,
                                     tariffExpenseItems)
        self.progressBar.setFormat('%v')
        self.contractId = contractId

        self.tariffType = None
        self.begDate = begDate
        self.endDate = endDate
        self.dupAskUser = False
        self.dupUpdate = False
        self.dupSkip = False

        self.nSkipped = 0
        self.nAdded = 0
        self.nUpdated = 0
        self.nProcessed = 0

        self.tariffCategory = {}

        self.unitId = None

        self.edtBegDate.canBeEmpty()
        self.edtEndDate.canBeEmpty()
        self.edtBegDate.setDate(begDate)
        self.edtEndDate.setDate(endDate)

        self.ageStr = None
        self.matureTariff = False
        self.expenseFields = None
        self.amount = 0
        self.infisCode = None
        self.priceFieldName = None


    def startImport(self):
        contractId = self.contractId
        if not contractId:
            return

        toothImport = self.tabWidget.currentIndex() != 0
        matureTariff = self.chkLoadMature.isChecked()
        self.progressBar.setFormat('%v')

        if toothImport:
            # импорт стоматологии
            self.tariffType = CTariff.ttActionUET
            self.unitId = forceRef(QtGui.qApp.db.translate('rbMedicalAidUnit',
                'regionalCode', '28', 'id'))
        else:
            dbfFileName = forceStringEx(self.edtFileName.text())
            self.tariffType = (CTariff.ttVisit
                if self.chkTariffVisit.isChecked() else CTariff.ttActionAmount)
            self.unitId = forceRef(QtGui.qApp.db.translate('rbMedicalAidUnit',
                'regionalCode',
                ('1' if self.tariffType == CTariff.ttVisit else '6'), 'id'))

        self.nSkipped = 0
        self.nAdded = 0
        self.nUpdated = 0
        self.nProcessed = 0

        self.infisCode = forceString(self.edtLpuCode.text())

        if not self.unitId:
            if self.tariffType == CTariff.ttActionUET:
                unitStr = u'"9" (УЕТ)'
            elif self.tariffType == CTariff.ttVisit:
                unitStr = u'"1" (Посещение)'
            else:
                unitStr = u'"6" (Медицинская услуга)'

            self.log.append(u'<b><font color=red>ОШИБКА:</b>'
             u' Не найдена единица учета медицинской помощи'
             u' (rbMedicalAidUnit) с региональным кодом %s' % unitStr)
            #return

        self.ageStr = u'18г-' if matureTariff else u'-17г'
        self.dupAskUser = self.chkAskUser.isChecked()
        self.dupUpdate = self.chkUpdate.isChecked()
        self.dupSkip = self.chkSkip.isChecked()
        self.begDate = (self.edtBegDate.date()
                        if self.edtBegDate.date().isValid() else None)
        self.endDate = (self.edtEndDate.date()
                        if self.edtEndDate.date().isValid() else None)
        self.amount = 1 if self.tariffType == CTariff.ttVisit else 0

        if self.tariffType == CTariff.ttVisit: #visit
            self.priceFieldName = 'TARIF_A'
        else:
            self.priceFieldName = ('PROF_TARIF'  if matureTariff
                                   else 'CHLD_TARIF')

        if self.begDate and self.endDate and (self.begDate > self.endDate):
            self.log.append(u'<b><font color=red>ОШИБКА:</b>'
                u' Неверно задан период.')
            return

        self.matureTariff = matureTariff

        if toothImport:
            dbfSpec = Dbf(os.path.join(
                forceString(self.edtToothRbDir.text()), u'STOMAT_TAR.DBF'),
                readOnly=True, encoding='cp866')
            dbfTariff = Dbf(os.path.join(
                forceString(self.edtToothRbDir.text()), u'R_SERV.DBF'),
                readOnly=True, encoding='cp866')

            self.expenseFields = self.setupExpenses(True, matureTariff, dbfSpec)
            if not  self.expenseFields:
                dbfTariff.close()
                dbfSpec.close()
                return

            self.progressBar.setMaximum(len(dbfTariff)+len(dbfSpec)-1)
            self.process(dbfSpec, self.processSpec)
            self.process(dbfTariff, self.processToothTariff)
            dbfTariff.close()
            dbfSpec.close()
        else:
            self.expenseFields = self.setupExpenses(False, matureTariff, None)
            if not self.expenseFields:
                return

            dbfTariff = Dbf(dbfFileName, readOnly=True, encoding='cp866')
            self.progressBar.setMaximum(len(dbfTariff)-1)
            self.process(dbfTariff, self.processTariff)
            dbfTariff.close()

        self.log.append(u'добавлено: %d; изменено: %d' % (
                                                  self.nAdded, self.nUpdated))
        self.log.append(u'пропущено: %d; обработано: %d' % (
                                                self.nSkipped, self.nProcessed))
        self.log.append(u'готово')


    def setupExpenses(self, isToothImport, isMatureTariff, dbf):
        result = {}

        if isToothImport:
            isType2015 = dbf.header.fields.count('TARIF_41') == 0

            if isType2015:
                childFields = self.expenseToothChildFields2015
                matureFields = self.expenseToothMatureFields2015
            else:
                childFields = self.expenseToothChildFields2014
                matureFields = self.expenseToothMatureFields2014

            fields = matureFields if isMatureTariff else childFields
        else:
            if self.tariffType == CTariff.ttVisit: #visit
                fields = self.expenseVisitChildFields2014
            else: # service
                fields = self.expenseServiceMatureFields2014 if isMatureTariff \
                    else self.expenseServiceChildFields2014

        for (fieldName, code) in fields:
            result[(fieldName, code)] = forceRef(QtGui.qApp.db.translate(
                'rbExpenseServiceItem', 'code', code, 'id'))

        for ((fieldName, code), _id) in result.items():
            if not _id:
                self.log.append(u'<b><font color=red>ОШИБКА:</b>'
                 u' Не найдена статья затрат'
                 u' (rbExpenseServiceItem) с кодом %s' % code)
                return None

        return result


    def process(self, dbf, step):
        for row in dbf:
            QtGui.qApp.processEvents()
            if self.abort:
                self.reject()
                return
            self.progressBar.setValue(self.progressBar.value()+1)
            QtGui.qApp.db.transaction()
            try:
                step(row)
                QtGui.qApp.db.commit()
            except:
                QtGui.qApp.db.rollback()
                QtGui.qApp.logCurrentException()
                raise


    def processTariff(self, row):
        infisCode = forceString(row['CODE_HOSP'])
        tariffBegDate = forceDate(row['TARIF_DATE'])
        tariffEndDate = forceDate(row['D_TO'])
        serviceCode = row['PROF'].strip()
        strTariffDate = forceString(tariffBegDate.toString('dd.MM.yyyy'))

        if self.infisCode != '' and infisCode != self.infisCode:
            self.nSkipped += 1
            self.log.append(u'Услуга: "%s" дата "%s", чужой инфис код "%s". '
                u'Пропущена.' % (serviceCode, strTariffDate, infisCode))
            return

        if (((not self.begDate) or (tariffBegDate >= self.begDate)) and
                ((not self.endDate) or (tariffEndDate <= self.endDate))):

            serviceId = self.findServiceByInfisCode(serviceCode)

            if not serviceId:
                self.log.append(u'<b><font color=orange>ОШИБКА:</b>'
                    u' Услуга, код ИНФИС: "%s", не найдена' % serviceCode)
                self.nSkipped += 1
                return

            federalPrice = row['TARIF_F'] if row.asDict().get('TARIF_F') else 0
            price = row[self.priceFieldName] + federalPrice

            tariff = self.tblContract_Tariff.newRecord()
            tariff.setValue('price', price)
            tariff.setValue('federalPrice', federalPrice)
            tariff.setValue('amount', toVariant(self.amount))
            tariff.setValue('service_id', toVariant(serviceId))
            tariff.setValue('master_id', toVariant(self.contractId))
            tariff.setValue('begDate', toVariant(tariffBegDate))
            tariff.setValue('endDate', toVariant(tariffEndDate))
            tariff.setValue('tariffType', toVariant(self.tariffType))
            tariff.setValue('unit_id', toVariant(self.unitId))
            tariff.setValue('age', toVariant(self.ageStr))

            expenseList = []

            for ((fieldName, _), expenseTypeId) in self.expenseFields:
                expense = self.tblContract_CompositionExpense.newRecord()
                expense.setValue('percent', toVariant(
                    100*row[fieldName]/price if price != 0 else row[fieldName]))
                expense.setValue('rbTable_id', toVariant(expenseTypeId))
                expenseList.append(expense)

            self.log.append(u'Услуга: "%s". Дата "%s". Возраст "%s": <b>'
                u'<font color=green>"%.2f"</b>' % (serviceCode, strTariffDate,
                                                   self.ageStr, price))
            self.addOrUpdateTariff(serviceCode, tariff, expenseList)
            self.nProcessed += 1
        else:
            self.nSkipped += 1
            self.log.append(u'Услуга: "%s". Дата "%s" вне периода загрузки.' % (
                                    serviceCode, strTariffDate))


    def processToothTariff(self, row):
        serviceCode = forceString(row['CODE'])
        tariffBegDate = forceDate(row['D_FROM'])
        tariffEndDate = forceDate(row['D_TO'])
        uet = forceDouble(row['UNIT'])
        isMatureTariff = (forceBool(row['DET']) == False)
        strTariffDate = forceString(tariffEndDate.toString('dd.MM.yyyy'))

        if (not self.begDate) or (not self.endDate):
            self.log.append(u'Услуга: "%s". '
                u'Не задан период загрузки.' % serviceCode)
            self.nSkipped += 1
            return

        if tariffEndDate >= self.begDate:
            serviceId = self.findServiceByInfisCode(serviceCode)

            if not serviceId:
                self.log.append(u'<b><font color=orange>ОШИБКА:</b>'
                    u' Услуга, код ИНФИС: "%s", не найдена' % serviceCode)
                self.nSkipped += 1
                return

            if self.matureTariff != isMatureTariff:
                fmt = (u'взрослый' if isMatureTariff else u'детский')
                self.log.append(u'Услуга: "%s" - %s тариф. Пропущена.' % (serviceCode, fmt))
                self.nSkipped += 1
                return

            for (categoryId, val) in self.tariffCategory.iteritems():
                (code, maturePrice, childPrice, expenseCode) = val

                price = uet * (maturePrice if self.matureTariff else childPrice)
                tariff = self.tblContract_Tariff.newRecord()
                tariff.setValue('amount', toVariant(0))
                tariff.setValue('service_id', toVariant(serviceId))
                tariff.setValue('master_id', toVariant(self.contractId))
                tariff.setValue('begDate', toVariant(self.begDate))
                tariff.setValue('endDate', toVariant(self.endDate))
                tariff.setValue('tariffType', toVariant(self.tariffType))
                tariff.setValue('unit_id', toVariant(self.unitId))
                tariff.setValue('uet', toVariant(uet))
                tariff.setValue('tariffCategory_id', toVariant(categoryId))
                tariff.setValue('age', toVariant(self.ageStr))

                newPrice = 0.0

                for (expenseTypeId, expenseVal) in expenseCode.items():
                    newPrice += round(expenseVal*uet+0.000001, 2)

                if newPrice > 0.0:
                    self.log.append(u'Корректировка цены: %.2f -> %.2f' % (
                                                               price, newPrice))
                    price = newPrice

                expenseList = []

                for (expenseTypeId, expenseVal) in expenseCode.items():
                    expense = self.tblContract_CompositionExpense.newRecord()
                    expense.setValue('percent', toVariant(
                        100.0*round(expenseVal*uet+0.000001, 2)/price
                        if price != 0 else 0))
                    expense.setValue('rbTable_id', toVariant(expenseTypeId))
                    expenseList.append(expense)

                tariff.setValue('price', price)

                self.log.append(u'Услуга: "%s". Дата "%s". Возраст "%s".'
                    u' Тарифная катеогория "%s": <b>'
                    u'<font color=green>"%.2f"</b>' % (serviceCode,
                            strTariffDate, self.ageStr, code, price))
                self.addOrUpdateTariff(serviceCode, tariff, expenseList)
                self.nProcessed += 1
        else:
            self.nSkipped += 1
            self.log.append(u'Услуга: "%s". '
                u'Дата "%s" вне периода загрузки.' % (serviceCode, strTariffDate))


    def processSpec(self, row):
        maturePrice = forceDouble(row['PROF_TARIF'])
        childPrice = forceDouble(row['CHLD_TARIF'])

        if maturePrice == 0 and childPrice == 0:
            return

        code = forceString(row['SPEC'])
        categoryId = self.ensureTariffCategory(code)

        expenseCode = {}

        for ((fieldName, code), _id) in self.expenseFields.items():
            expenseCode[_id] = forceDouble(row[fieldName])

        self.tariffCategory[categoryId] = (code,
            maturePrice, childPrice, expenseCode)


    @pyqtSignature('')
    def on_btnSelectFile_clicked(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
            u'Укажите файл с данными', self.edtFileName.text(),
            u'Файлы DBF (*.dbf)')
        if fileName != '':
            self.edtFileName.setText(QDir.toNativeSeparators(fileName))
            self.btnImport.setEnabled(True)
            dbfFileName = forceStringEx(self.edtFileName.text())
            dbfTariff = Dbf(dbfFileName, readOnly=True, encoding='cp866')
            self.labelNum.setText(
                u'всего записей в источнике: '+str(len(dbfTariff)))


    @pyqtSignature('')
    def on_btnSelectToothRbDir_clicked(self):
        dirName = QtGui.QFileDialog.getExistingDirectory(self,
            u'Укажите директорий со справочниками', self.edtToothRbDir.text())

        if dirName:
            self.edtToothRbDir.setText(QDir.toNativeSeparators(dirName))
