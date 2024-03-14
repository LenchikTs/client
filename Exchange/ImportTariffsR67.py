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
u"""Импорт тарифа для Смоленской области"""

import math

from PyQt4 import QtGui
from PyQt4.QtCore import QDate, QDir, pyqtSignature


from library.dbfpy.dbf import Dbf
from library.Utils import copyFields, firstMonthDay, forceBool, forceDate, forceDouble, forceInt, forceRef, forceString, forceStringEx, toVariant

from Accounting.Tariff import CTariff
from Exchange.Cimport import CDBFimport, Cimport

from Exchange.Utils import tbl

from Exchange.Ui_ImportTariffsR67 import Ui_Dialog


def ImportTariffsR67(widget, contractId, begDate, endDate, tariffList, tariffExpenseItems, tariffCoefficientItems):
    dlg=CImportTariffs(widget, contractId, begDate, endDate, tariffList)
    dlg.edtFileName.setText(forceString(QtGui.qApp.preferences.appPrefs.get('ImportTariffR67FileName',  '')))
    dlg.chkOnlyForCurrentOrg.setChecked(forceBool(QtGui.qApp.preferences.appPrefs.get('ImportTariffR67CurrentOrgOnly',  False)))
    dlg.edtUetValue.setValue(forceDouble(QtGui.qApp.preferences.appPrefs.get('ImportTariffR67UetValue',  0.01)))
    dlg.exec_()
    QtGui.qApp.preferences.appPrefs['ImportTariffR67FileName'] = toVariant(dlg.edtFileName.text())
    QtGui.qApp.preferences.appPrefs['ImportTariffR67CurrentOrgOnly'] = \
        toVariant(dlg.chkOnlyForCurrentOrg.isChecked())
    QtGui.qApp.preferences.appPrefs['ImportTariffR67UetValue'] = \
        toVariant(dlg.edtUetValue.value())
    return dlg.ok, dlg.tariffList, tariffExpenseItems, []


class CImportTariffs(QtGui.QDialog, Ui_Dialog, CDBFimport):
    def __init__(self,  parent, contractId, begDate, endDate, tariffList):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        Cimport.__init__(self, self.log)
        self.progressBar.setFormat('%v')
        self.contractId = contractId
        self.tblContract_Tariff = tbl('Contract_Tariff')
        self.ok = False

        self.tariffList = map(None, tariffList)
        self.tariffDict = {}
        for i, tariff in enumerate(self.tariffList):
            key = ( forceInt(tariff.value('tariffType')),
                    forceRef(tariff.value('service_id')),
                    forceInt(tariff.value('sex')),
                    forceString(tariff.value('age')),
                  )
            tariffIndexList = self.tariffDict.setdefault(key, [])
            tariffIndexList.append(i)

        self.dupAskUser = False
        self.dupUpdate = False
        self.dupSkip = False
        self.dupAppend = False
        self.currentOrgOnly = False
        self.yesToAll = False
        self.noToAll = False
        self.saveAll = False
        self.currentOrgInfisCode = None

        self.nSkipped = 0
        self.nAdded = 0
        self.nUpdated = 0
        self.nProcessed = 0
        self.nAppended = 0

        self.unitVisitId = None
        self.unitServiceId = None


    def exec_(self):
        self.updateLabel()
        QtGui.QDialog.exec_(self)


    def startImport(self):
        self.ok = False
        contractId = self.contractId
        if not contractId:
            return

        dbfFileName = forceStringEx(self.edtFileName.text())
        dbfTariff = Dbf(dbfFileName, readOnly=True, encoding='cp866')
        self.progressBar.setMaximum(len(dbfTariff)-1)

        self.nSkipped = 0
        self.nAdded = 0
        self.nUpdated = 0
        self.nProcessed = 0
        self.nAppended = 0

        self.unitVisitId = forceRef(QtGui.qApp.db.translate('rbMedicalAidUnit', 'code',
            '1', 'id'))
        self.unitServiceId = forceRef(QtGui.qApp.db.translate('rbMedicalAidUnit', 'code',
            '6', 'id'))

        if not self.unitVisitId:
            self.log.append(u'<b><font color=red>ОШИБКА:</b>'
             u' Не найдена единица учета медицинской помощи'
             u' (rbMedicalAidUnit) с кодом "1" (Посещение)')
            return

        if not self.unitServiceId:
            self.log.append(u'<b><font color=red>ОШИБКА:</b>'
             u' Не найдена единица учета медицинской помощи'
             u' (rbMedicalAidUnit) с кодом "6" (Медицинская услуга)')
            return

        self.dupAskUser = self.chkAskUser.isChecked()
        self.dupUpdate = self.chkUpdate.isChecked()
        self.dupSkip = self.chkSkip.isChecked()
        self.dupAppend = self.chkAppend.isChecked()
        self.currentOrgOnly = self.chkOnlyForCurrentOrg.isChecked()
        self.yesToAll = False
        self.noToAll = False
        self.saveAll = False

        if self.currentOrgOnly:
            self.currentOrgInfisCode = forceString(
                QtGui.qApp.db.translate('Organisation', 'id', QtGui.qApp.currentOrgId(), 'infisCode'))
            self.log.append(u'загрузка тарифов только с кодом `%s`' % self.currentOrgInfisCode)

        self.chkOnlyForCurrentOrg.setEnabled(False)
        self.process(dbfTariff, self.processTariff)
        self.ok = not self.abort

        dbfTariff.close()
        self.chkOnlyForCurrentOrg.setEnabled(True)
        self.log.append(u'добавлено: %d; изменено: %d' % (self.nAdded, self.nUpdated))
        self.log.append(u'дополнено: %d' % self.nAppended)
        self.log.append(u'пропущено: %d; обработано: %d' % (self.nSkipped, self.nProcessed))
        self.log.append(u'готово')


    def process(self, dbf, step):
        for row in dbf:
            QtGui.qApp.processEvents()
            if self.abort:
                self.reject()
                return
            self.progressBar.setValue(self.progressBar.value()+1)
            try:
                step(row)
            except:
                QtGui.qApp.logCurrentException()
                raise


    def processTariff(self,  row):
        orgCode = forceString(row['MCOD'].strip())
        serviceCode = forceString(row['KMU'].strip())

        if self.currentOrgOnly and (self.currentOrgInfisCode != orgCode):
            self.log.append(u' Услуга, код ИНФИС: "%s", не соответствует текущему ЛПУ.' \
                                    u' Пропускаем.' % serviceCode)
            self.nSkipped += 1
            return

        price = forceDouble(row['S']) # float
        federalPrice = forceDouble(row['PSZP'])

        if row.deleted:
            self.log.append(u'<b><font color=blue>ВНИМАНИЕ:</b>'
                u'Услуга, код ИНФИС: "%s", помечена на удаление. Пропускаем.' % serviceCode)
            self.nSkipped += 1
            return

        serviceId = self.findServiceByInfisCode(serviceCode)

        if not serviceId:
            self.log.append(u'<b><font color=orange>ОШИБКА:</b>'
                u' Услуга, код ИНФИС: "%s", не найдена' % serviceCode)
            self.nSkipped += 1
            return

        tariffType = CTariff.ttActionAmount # тарифицируем услуги
        uet = 0

        if serviceCode[:3] in ('097', '099', '197', '199'):
            #Мероприятие по количеству и тарифу койки
            tariffType = CTariff.ttHospitalBedService
        elif serviceCode[:3] in ('009', '109'):
            #Мероприятие по количеству
            tariffType = CTariff.ttActionUET
            uet = math.floor(price/self.edtUetValue.value()*100)/100
        elif serviceCode[:3] in ('001', '101'):
            #Посещение
            tariffType = CTariff.ttVisit

        amount = 1 if tariffType == CTariff.ttVisit else 0

        self.log.append(u'Услуга: "%s". Тариф: <b>'
                u'<font color=green>"%.2f"</b>,'
                u' ует <b><font color=green>"%.2f"</b>,'
                u' федеральная часть <b><font color=green>"%.2f"</b>' % (serviceCode, price, uet,  federalPrice))
        self.addOrUpdateTariff(tariffType, serviceCode, serviceId,  0,  '',  amount, price,  0, uet, federalPrice)
        self.nProcessed += 1


    def addOrUpdateTariff(self, tariffType, serviceCode, serviceId, sex, age, amount, price, limit, uet, federalPrice):
        key = (tariffType, serviceId, sex, age)
        tariffIndexList = self.tariffDict.get(key, None)

        if tariffIndexList:
            self.log.append(u'Найден совпадающий тариф.')
            if self.dupSkip:
                self.log.append(u'Пропускаем.')
                self.nSkipped += len(tariffIndexList)
                return
            for i in tariffIndexList:
                tariff = self.tariffList[i]
                oldAmount = forceDouble(tariff.value('amount'))
                oldPrice  = forceDouble(tariff.value('price'))
                oldLimit  = forceDouble(tariff.value('limit'))
                oldUet = forceDouble(tariff.value('uet'))
                oldFederalPrice = forceDouble(tariff.value('federalPrice'))

                if abs(oldPrice-price)<0.001 and abs(oldLimit-limit)<0.001 \
                        and abs(oldAmount-amount)<0.001 and abs(oldUet-uet)<0.001 \
                        and abs(oldFederalPrice-federalPrice)<0.001:
                    self.log.append(u'Количество, цены и ограничения совпадают, пропускаем.')
                    self.nSkipped += 1
                    break

                if self.dupUpdate:
                    self.log.append(u'Обновляем. (%.2f на %.2f,  фед. %.2f на %.2f)' % \
                                    (oldPrice, price, oldFederalPrice,  federalPrice))
                    self.updateTariff(tariff, amount, price, limit, uet, federalPrice)
                    self.nUpdated += 1
                elif self.dupAppend:
                    self.log.append(u'Дополняем с текущей даты по новой цене.')
                    self.appendTariff(tariff, amount, price, limit, uet,  federalPrice)
                    self.nAppended += 1
                    break
                else:
                    self.log.append(u'Запрос действий у пользователя.')
                    if not (self.yesToAll or self.noToAll or self.saveAll):
                        answer = QtGui.QMessageBox.question(self, u'Совпадающий тариф',
                                        u'Услуга "%s", пол "%s", возраст "%s"\n'
                                        u'Количество: %.2f, новое количество %.2f\n'
                                        u'Тариф: %.2f, новый %.2f\n'
                                        u'Фед. тариф: %.2f, новый %.2f\n'
                                        u'Предел: %d, новый предел %d\n'
                                        u'Да - Обновить, Нет - Пропустить, Сохранить - Дополнить' % \
                                            (serviceCode, sex, age if age else '-',
                                                oldAmount, amount, oldPrice, price, oldFederalPrice,  federalPrice,  oldLimit, limit),
                                        QtGui.QMessageBox.No|QtGui.QMessageBox.Yes|QtGui.QMessageBox.Save|
                                        QtGui.QMessageBox.NoToAll|QtGui.QMessageBox.YesToAll|
                                        QtGui.QMessageBox.SaveAll|QtGui.QMessageBox.Abort,
                                        QtGui.QMessageBox.No)

                        if answer == QtGui.QMessageBox.Abort:
                            self.log.append(u'Прервано пользователем.')
                            self.abort = True
                            return

                        strChoise = u'пропустить'

                        if (answer == QtGui.QMessageBox.Yes or
                            answer == QtGui.QMessageBox.YesToAll):
                            strChoise = u'обновить'
                            self.updateTariff(tariff, amount, price, limit, uet, federalPrice)
                            self.nUpdated += 1
                            self.yesToAll = (answer == QtGui.QMessageBox.YesToAll)
                        elif (answer == QtGui.QMessageBox.Save or
                                answer == QtGui.QMessageBox.SaveAll or self.saveAll):
                            strChoise = u'дополнить'
                            self.appendTariff(tariff, amount, price, limit,  uet, federalPrice)
                            self.nAppended += 1
                            self.saveAll = (answer == QtGui.QMessageBox.SaveAll)
                        else:
                            self.nSkipped += 1
                            self.noToAll = (answer == QtGui.QMessageBox.NoToAll)

                        self.log.append(u'Выбор пользователя %s' % strChoise)
                    else:
                        if self.yesToAll:
                            self.updateTariff(tariff, amount, price, limit, uet, federalPrice)
                            self.nUpdated += 1
                        elif self.saveAll:
                            self.appendTariff(tariff, amount, price, limit, uet, federalPrice)
                            self.nAppended += 1
                        else:
                            self.nSkipped += 1
        else:
            self.log.append(u'Добавляем тариф.')
            self.nAdded += 1
            self.addTariff(tariffType, serviceId, sex, age, amount, price, limit, uet, federalPrice)


    def addTariff(self, tariffType, serviceId, sex, age, amount, price, limit, uet, federalPrice):
        record = self.tblContract_Tariff.newRecord()
        record.setValue('master_id',  toVariant(self.contractId))
        record.setValue('tariffType', toVariant(tariffType))
        record.setValue('service_id', toVariant(serviceId))
        record.setValue('sex', toVariant(sex))
        record.setValue('age', toVariant(age))
        record.setValue('unit_id',
            toVariant(self.unitVisitId if tariffType == CTariff.ttVisit else self.unitServiceId))
        record.setValue('amount',  toVariant(amount))
        record.setValue('price', toVariant(price))
        record.setValue('limit',  toVariant(limit))
        record.setValue('uet',  toVariant(uet))
        record.setValue('federalPrice', toVariant(federalPrice))
        i = len(self.tariffList)
        self.tariffList.append(record)
        key = (tariffType, serviceId, sex, age)
        tariffIndexList = self.tariffDict.setdefault(key, [])
        tariffIndexList.append(i)


    def updateTariff(self, tariff, amount, price, limit, uet, federalPrice):
        tariff.setValue('amount',  toVariant(amount))
        tariff.setValue('price', toVariant(price))
        tariff.setValue('limit', toVariant(limit))
        tariff.setValue('uet', toVariant(uet))
        tariff.setValue('federalPrice', toVariant(federalPrice))


    def appendTariff(self, tariff, amount, price, limit, uet, federalPrice):
        endDate = forceDate(tariff.value('endDate'))
        record = self.tblContract_Tariff.newRecord()
        copyFields(record, tariff)
        date = firstMonthDay(QDate.currentDate())
        record.setValue('begDate', date)

        if endDate and endDate < date:
            record.setNull('endDate')
        else:
            tariff.setValue('endDate', date.addDays(-1))

        record.setValue('amount',  toVariant(amount))
        record.setValue('price', toVariant(price))
        record.setValue('federalPrice', toVariant(federalPrice))
        record.setValue('limit', toVariant(limit))
        record.setValue('uet',  toVariant(uet))

        i = len(self.tariffList)
        self.tariffList.append(record)
        key = (forceInt(record.value('tariffType')), forceRef(record.value('service_id')),
                    forceInt(record.value('sex')), forceString(record.value('age')))
        tariffIndexList = self.tariffDict.setdefault(key, [])
        tariffIndexList.append(i)


    serviceCache = {}

    def findServiceByInfisCode(self, code):
        result = self.serviceCache.get(code)

        if not result:
            result = forceRef(QtGui.qApp.db.translate('rbService', 'infis', code, 'id'))

            if result:
                self.serviceCache[code] = result

        return result


    def updateLabel(self):
        try:
            dbfFileName = forceStringEx(self.edtFileName.text())
            dbfTariff = Dbf(dbfFileName, readOnly=True, encoding='cp866')
            self.labelNum.setText(u'всего записей в источнике: '+str(len(dbfTariff)))
        except:
            pass


    @pyqtSignature('')
    def on_btnSelectFile_clicked(self):
        fileName = QtGui.QFileDialog.getOpenFileName(
            self, u'Укажите файл с данными', self.edtFileName.text(), u'Файлы DBF (*.dbf)')
        if fileName != '':
            self.edtFileName.setText(QDir.toNativeSeparators(fileName))
            self.btnImport.setEnabled(True)
            self.updateLabel()
