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

u"""
Импорт тарифа из ИНФИС
"""
import re

from PyQt4 import QtGui
from PyQt4.QtCore import QDate, QDir, pyqtSignature

from library.dbfpy.dbf import Dbf
from library.DbfViewDialog import CDbfViewDialog
from library.exception import CException
from library.Utils import forceDouble, forceInt, forceRef, forceString, forceStringEx, formatSex, toVariant

from Accounting.Tariff import CTariff
from Exchange.Cimport import CDBFimport, Cimport

from Exchange.Utils import tbl

from Exchange.Ui_ImportTariffsINFIS import Ui_Dialog


def ImportTariffsINFIS(widget, contractId, begDate, endDate, tariffList, tariffExpenseItems, tariffCoefficientItems):
    dlg=CImportTariffs(widget, contractId, begDate, endDate, tariffList)
    dlg.edtFileName.setText(forceString(QtGui.qApp.preferences.appPrefs.get('ImportTariffINFISFileName',  '')))
    dlg.edtRbProfileFileName.setText(forceString(QtGui.qApp.preferences.appPrefs.get('ImportProfilesINFISFileName',  '')))
    dlg.exec_()
    QtGui.qApp.preferences.appPrefs['ImportTariffINFISFileName'] = toVariant(dlg.edtFileName.text())
    QtGui.qApp.preferences.appPrefs['ImportProfilesINFISFileName'] = toVariant(dlg.edtRbProfileFileName.text())
    return dlg.ok, dlg.tariffList, tariffExpenseItems, []


class CImportTariffs(QtGui.QDialog, Ui_Dialog, CDBFimport):

    tariffTypeDependOnProfileType = {
                                     u'п':2,
                                     u'у':2,
                                     u'а':2,
                                     u'с':2,
                                     u'г':6,
                                     u'д':2,
                                     u'0':0,
                                     }

    def __init__(self, parent, contractId, begDate, endDate, tariffList):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        Cimport.__init__(self, self.log)
        self.rbProfileLoaded = False
        self.rbProfileTypeLoaded = False
        self.dbfProfileFileName = None
        self.dbfProfileTypeFileName = None
        self.profileCache = {}
        self.tariffDictGroupByProfile = {}
        self.progressBar.setFormat('%v')
        self.parent = parent #wtf? скрывать Qt-шный parent - это плохая затея
        self.contractId = contractId
        self.begDate = begDate
        self.endDate = endDate
        self.tariffList = map(None, tariffList)
        self.tariffDict = {}
        self.profileThatMoreThanOneInDbf = []
        for i, tariff in enumerate(self.tariffList):
            key = ( forceInt(tariff.value('tariffType')),
                    forceRef(tariff.value('service_id')),
                    forceInt(tariff.value('sex')),
                    forceString(tariff.value('age')),
                  )
            tariffIndexList = self.tariffDict.setdefault(key, [])
            tariffIndexList.append(i)

        self.tblContract_Tariff = tbl('Contract_Tariff')

        self.ok = False
        self.abort = False
        self.loadMature = False
        self.loadChildren = False
        self.dupAskUser = False
        self.dupUpdate = False
        self.dupSkip = False

        self.nSkipped = 0
        self.nAdded = 0
        self.nUpdated = 0
        self.nProcessed = 0

        self.unitId = None
        self.amount = 0
        self.tariffType = CTariff.ttActionAmount

        self.edtBegDate.canBeEmpty()
        self.edtEndDate.canBeEmpty()
        self.edtBegDate.setDate(self.begDate)
        self.edtEndDate.setDate(self.endDate)


    def exec_(self):
        if self.edtRbProfileFileName.text() != '':
            self.dbfProfileFileName = forceStringEx(self.edtRbProfileFileName.text())
            self.loadRbProfiles()
            self.btnLoadRbProfile.setEnabled(True)
        return QtGui.QDialog.exec_(self)

    def startImport(self):
        if not self.rbProfileLoaded:# and self.rbProfileTypeLoaded):
            if QtGui.QMessageBox.No == QtGui.QMessageBox.question(self, u'Вы уверены?',
                                        u'Справочник для определения типа тарификации не загружен, возможны проблемы с импортом.\nВсе равно продолжить?',
                                        QtGui.QMessageBox.No|QtGui.QMessageBox.Yes,
                                        QtGui.QMessageBox.No):
                return
        self.ok = False
#        db = QtGui.qApp.db

        dbfFileName = forceStringEx(self.edtFileName.text())
        dbfTariff = Dbf(dbfFileName, readOnly=True, encoding='cp866')
        self.progressBar.setMaximum(len(dbfTariff)-1)

        self.nSkipped = 0
        self.nAdded = 0
        self.nUpdated = 0
        self.nProcessed = 0

        self.amount =  0
        self.unitId = forceRef(QtGui.qApp.db.translate('rbMedicalAidUnit', 'code',
            '6', 'id'))

        if not self.unitId:
            self.log.append(u'<b><font color=red>ОШИБКА:</b>'
             u' Не найдена единица учета медицинской помощи'
             u' (rbMedicalAidUnit) с кодом "6"(Медицинская услуга)')
            return

        self.loadChildren = self.chkLoadChildren.isChecked()
        self.loadMature = self.chkLoadMature.isChecked()
        self.dupAskUser = self.chkAskUser.isChecked()
        self.dupUpdate = self.chkUpdate.isChecked()
        self.dupSkip = self.chkSkip.isChecked()
        self.importBegDate = self.edtBegDate.date()
        self.importEndDate = self.edtEndDate.date()
        self.loadMes = self.chkLoadMes.isChecked()
        self.loadService = self.chkLoadService.isChecked()
        self.loadVisit = self.chkLoadVisit.isChecked()

        if self.importBegDate and self.importEndDate and (self.importBegDate> self.importEndDate):
            self.log.append(u'<b><font color=red>ОШИБКА:</b> Неверно задан период.')
            return

        if (self.importBegDate and self.importBegDate>self.endDate) or \
            (self.importEndDate and self.importEndDate<self.begDate):
            self.log.append(u'<b><font color=red>ОШИБКА:</b> Период вне времени действия договора.')
            return

        self.importBegDate = max(self.importBegDate, self.begDate) if self.importBegDate else self.begDate
        self.importEndDate = min(self.importEndDate, self.endDate) if self.importEndDate else self.endDate

        self.log.append(u'фильтр по дате: с %s по %s' % (forceString(self.importBegDate), forceString(self.importEndDate)))
        self.importRun = True
        self.process(dbfTariff, self.processTariff)
        self.ok = not self.abort

        dbfTariff.close()
        self.log.append(u'добавлено: %d; изменено: %d' % (self.nAdded, self.nUpdated))
        self.log.append(u'пропущено: %d; обработано: %d' % (self.nSkipped, self.nProcessed))
        self.log.append(u'готово')


    def process(self, dbf, step):
#        self.parseDbfToDict(dbf)
        try:
            for row in dbf:
                if self.abort:
                    self.importRun = False
#                    self.reject()
                    return
                self.progressBar.setValue(self.progressBar.value()+1)
                step(row)

        except ValueError:
            self.log.append(u'<b><font color=red>ОШИБКА:</b>'
                    u' неверное значение строки "%d" в dbf.' % \
                    (self.progressBar.value()+1))
            self.nSkipped += 1
            self.abort = True


    def parseDbfToDict(self, dbf):
        QtGui.qApp.setWaitCursor()
        self.profileThatMoreThanOneInDbf = []
        for row in dbf:
            profile = row['PROFILE']
            tGroup = row['TGROUP']
            outcome = row['OUTCOME']
            tariffDate = QDate(row['DATEBREAK']) if row['DATEBREAK'] else QDate()
            alreadyExists = self.tariffDictGroupByProfile.get((profile, tariffDate, tGroup, outcome), None)
            if alreadyExists:
                if profile not in self.profileThatMoreThanOneInDbf:
                    self.profileThatMoreThanOneInDbf.append(profile)
                alreadyExists.append(row)
            else:
                self.tariffDictGroupByProfile[(profile, tariffDate, tGroup, outcome)] = [row]
        QtGui.qApp.restoreOverrideCursor()


    def checkTGroupAndOutcome(self, row):
        if row['TGROUP'] != '':
            return False
        if row['OUTCOME'] != '':
            return False
        return True


    def processTariff(self,  row):
        QtGui.qApp.processEvents()
        serviceCode = forceString(row['PROFILE']).strip()
        tariffDate = QDate(row['DATEBREAK']) if row['DATEBREAK'] else QDate()

        if tariffDate and (tariffDate<self.importBegDate or tariffDate>self.importEndDate):
            self.log.append(u'пропускаем тариф "%s", так как дата %s вне интервала' % \
                            (serviceCode, forceString(tariffDate)))
            return

        tariffType = None
        if serviceCode[:1] in (u'а', u'к', u'л', u'ф'): # посещения
            tariffType = CTariff.ttVisit
        elif serviceCode[:1] in (u'з', u'и', u'у'): # услуги
            tariffType = CTariff.ttActionAmount
        elif serviceCode.startswith(u'нК'):
            tariffType = CTariff.ttActionAmount
        elif re.match('^\d+$', serviceCode):
            if not self.checkTGroupAndOutcome(row):
                return
            mesId = forceRef(QtGui.qApp.db.translate('mes.MES', 'code', serviceCode, 'id'))
            if mesId:
                tariffType = CTariff.ttEventByMESLen
        if tariffType is None:
            tariffType = self.profileCache.get(serviceCode, None)
            if tariffType is None:
                self.log.append(u'<b><font color=red>ОШИБКА:</b>'\
                    u' Обработка тарифов с профилем "%s" не поддерживается.' %  serviceCode)
                return

        if (   (tariffType == CTariff.ttVisit         and not self.loadVisit)
            or (tariffType == CTariff.ttActionAmount  and not self.loadService)
            or (tariffType == CTariff.ttEventByMESLen and not self.loadMes)):
            self.log.append(u'<b><font color=red>НЕСООТВЕТСТВИЕ:</b>'\
                u'Обработка тарифов с типом "%s" не включена в импортирование' % CTariff.tariffTypeNames[tariffType])
            return
        amount = 1.0
        fullPrice = price = row['TARIFF'] # float
        inflectionPrice = 0.0
        exceedMode = 0
        inflectionPoint = row['DAYBORDER']
        inflectionPoint2 = row['AM120']
        coeff = float(row['COEFF'])
        evalType = forceStringEx(row['EVALTYPE'])

        if evalType[0] == '=':
            pass
        elif evalType[0] == '*':
            amount = float(row['AMOUNT'])
            price = price / amount
        elif evalType[0] == u'ф':
            amount = float(row['AMOUNT'])
            price = price / amount
            if coeff != 0.0:
                price = price * coeff
                fullPrice = fullPrice * coeff
        elif evalType[0] == '<':
            amount = float(row['AMOUNT'])
            price = price / amount
            if coeff != 0.0:
                price = price * coeff
                fullPrice = fullPrice * coeff
            exceedMode = 1
        elif evalType[0] == '5':
            amount = float(row['AMOUNT'])
            price = price / amount
            if coeff != 0.0:
                price = price * coeff
                fullPrice = fullPrice * coeff
            exceedMode = 1
            inflectionPoint = 5
        else:
            self.log.append(u'<b><font color=red>ОШИБКА:</b>'\
                u' Обработка тарифов с полем EVALTYPE="%s" не поддерживается.' %  evalType)
            return


        profileNet = unicode(row['PROFILENET'])
        sex = 0
        age = ''
        if profileNet == u'в':
            age = u'18г-'
        elif profileNet == u'д':
            age = u'-17г'
        elif profileNet == u'ж':
            sex = 2
        elif not profileNet:
            pass
        else:
            self.log.append(u'<b><font color=red>ОШИБКА:</b>'\
                u' Обработка тарифов с полем PROFILENET="%s" не поддерживается.' % profileNet)
            return

        serviceId = self.findServiceByInfisCode(serviceCode)

        if not serviceId:
            self.log.append(u'<b><font color=orange>ОШИБКА:</b>'\
                u' Услуга, код ИНФИС: "%s", не найдена' % serviceCode)
            self.nSkipped += 1
            return

        self.log.append(u'Профиль: "%s". Тариф: <b>'\
                u'<font color=green>%.2f</b>, количество <b>%.2f</b>,'\
                u' пол "%s", возраст "%s", дата окончания - %s, тип %d' %\
                (serviceCode, price, amount, formatSex(sex),  age if age else '-',
                 forceString(tariffDate) if tariffDate else u'бессрочный',
                 tariffType))

        result = self.formatValues(price,  fullPrice, inflectionPoint, inflectionPoint2, inflectionPrice, exceedMode)
        if result:
            f1Start, f1Sum, f1Price, f2Start, f2Sum, f2Price = result
            self.addOrUpdateTariff(tariffType, serviceCode, serviceId, sex, age, amount, tariffDate,
                                   price, f1Start, f1Sum, f1Price, f2Start, f2Sum, f2Price)
            self.nProcessed += 1

    def formatValues(self, price, fullPrice,  inflectionPoint, inflectionPoint2, inflectionPrice, exceedMode):
        f1Start = f1Sum = f1Price = f2Start = f2Sum = f2Price = 0
        if exceedMode == 0:
            pass
        elif exceedMode == 1:
            f1Start = inflectionPoint
            f1Sum   = fullPrice
            f1Price = 0
            f2Start = inflectionPoint2
            f2Sum   = fullPrice
            f2Price = price
        else:
            return None

        return f1Start, f1Sum, f1Price, f2Start, f2Sum, f2Price

    def addOrUpdateTariff(self, tariffType, serviceCode, serviceId, sex, age, amount, tariffDate,
                          price, f1Start, f1Sum, f1Price, f2Start, f2Sum, f2Price):

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
                oldF1Start = forceDouble(tariff.value('frag1Start'))
                oldF1Sum   = forceDouble(tariff.value('frag1Sum'))
                oldF1Price = forceDouble(tariff.value('frag1Price'))
                oldF2Start = forceDouble(tariff.value('frag2Start'))
                oldF2Sum   = forceDouble(tariff.value('frag2Sum'))
                oldF2Price = forceDouble(tariff.value('frag2Price'))

                equalF1Start = abs(oldF1Start-f1Start)<0.001
                equalF1Sum = abs(oldF1Sum-f1Sum)<0.001
                equalF1Price = abs(oldF1Price-f1Price)<0.001
                equalF2Start = abs(oldF2Start-f2Start)<0.001
                equalF2Sum = abs(oldF2Sum-f2Sum)<0.001
                equalF2Price = abs(oldF2Price-f2Price)<0.001
                equalPrice = abs(oldPrice-price)<0.001
                equalAmount = abs(oldAmount-amount)<0.001

                allAreEqual = equalF1Start and equalF1Sum and equalF1Price and equalF2Start and equalF2Sum and equalF2Price and equalPrice and equalAmount

                if allAreEqual:
                    self.log.append(u'Количество, цены и ограничения совпадают, пропускаем.')
                    self.nSkipped += 1
                if self.dupUpdate:
                    self.log.append(u'Обновляем. (%.2f на %.2f)' % (oldPrice, price))
                    self.updateTariff(tariff, amount, price, f1Start, f1Sum, f1Price, f2Start, f2Sum, f2Price)
                    self.nUpdated += 1
                else:
                    self.log.append(u'Запрос действий у пользователя.')
                    msgTuple = (serviceCode, sex, age if age else '-', oldAmount, amount,
                                oldPrice, price, oldF1Start, f1Start, oldF1Sum, f1Sum, oldF1Price, f1Price, oldF2Start, f2Start, oldF2Sum, f2Sum, oldF2Price, f2Price)
                    answer = QtGui.QMessageBox.question(self, u'Совпадающий тариф',
                                        u'Услуга "%s", пол "%s", возраст "%s"\n'
                                        u'Количество: %.2f, новое количество %.2f\n'
                                        u'Тариф: %.2f, новый %.2f\n'
                                        u'Начало Ф1: %.2f, новое начало Ф1 %.2f\n'
                                        u'Начальная сумма Ф1: %.2f, новая начальная сумма Ф1 %.2f\n'
                                        u'Цена Ф1: %.2f, новая цена Ф1 %.2f\n'
                                        u'Начало Ф2: %.2f, новое начало Ф2 %.2f\n'
                                        u'Начальная сумма Ф2: %.2f, новая начальная сумма Ф2 %.2f\n'
                                        u'Цена Ф2: %.2f, новая цена Ф2 %.2f\n'
                                        u'Обновить?' % msgTuple,
                                        QtGui.QMessageBox.No|QtGui.QMessageBox.Yes,
                                        QtGui.QMessageBox.No)
                    self.log.append(u'Выбор пользователя %s' % \
                    (u'обновить' if answer == QtGui.QMessageBox.Yes else u'пропустить'))
                    if answer == QtGui.QMessageBox.Yes:
                        self.updateTariff(tariff, amount, price, f1Start, f1Sum, f1Price, f2Start, f2Sum, f2Price)
                        self.nUpdated += 1
                    else:
                        self.nSkipped += 1
        else:
            self.log.append(u'Добавляем тариф.')
            self.nAdded += 1
            self.addTariff(tariffType, serviceId, sex, age, QDate(), tariffDate, amount, price, f1Start, f1Sum, f1Price, f2Start, f2Sum, f2Price)


    def addTariff(self, tariffType, serviceId, sex, age, begDate, endDate, amount, price, f1Start, f1Sum, f1Price, f2Start, f2Sum, f2Price):
        record = self.tblContract_Tariff.newRecord()
        record.setValue('master_id',  toVariant(self.contractId))
        record.setValue('tariffType', toVariant(tariffType))
        record.setValue('service_id', toVariant(serviceId))
        record.setValue('sex', toVariant(sex))
        record.setValue('age', toVariant(age))
        record.setValue('unit_id',  toVariant(self.unitId))
        record.setValue('amount',  toVariant(amount))
        record.setValue('price', toVariant(price))
        record.setValue('frag1Start', toVariant(f1Start))
        record.setValue('frag1Sum', toVariant(f1Sum))
        record.setValue('frag1Price', toVariant(f1Price))
        record.setValue('frag2Start', toVariant(f2Start))
        record.setValue('frag2Sum', toVariant(f2Sum))
        record.setValue('frag2Price', toVariant(f2Price))
        i = len(self.tariffList)
        self.tariffList.append(record)
        key = (tariffType, serviceId, sex, age)
        tariffIndexList = self.tariffDict.setdefault(key, [])
        tariffIndexList.append(i)


    def updateTariff(self, tariff, amount, price, f1Start, f1Sum, f1Price, f2Start, f2Sum, f2Price):
        tariff.setValue('amount',  toVariant(amount))
        tariff.setValue('price', toVariant(price))
        tariff.setValue('frag1Start', toVariant(f1Start))
        tariff.setValue('frag1Sum', toVariant(f1Sum))
        tariff.setValue('frag1Price', toVariant(f1Price))
        tariff.setValue('frag2Start', toVariant(f2Start))
        tariff.setValue('frag2Sum', toVariant(f2Sum))
        tariff.setValue('frag2Price', toVariant(f2Price))


    def findServiceByInfisCode(self, code):
        return forceRef(QtGui.qApp.db.translate('rbService', 'infis', code, 'id'))

    def checkProfileFields(self, dbfProfile):
        chkFields = ['CODE', 'NAME', 'HSNET', 'TYPE', 'EVALTYPE', 'PAYER', 'GTS']
        self.checkDbfFields(chkFields, dbfProfile, u' профилей')

    def checkDbfFields(self, fieldsList, dbfFile, dbfName=''):
        for field in fieldsList:
            if field not in dbfFile.header.fields:
               raise CException(u'Не правильная структура dbf файла%s!'% dbfName)

    def loadRbProfiles(self):
        try:
            self.profileCache.clear()
            dbfProfile = Dbf(self.dbfProfileFileName, readOnly=True, encoding='cp866')
            self.checkProfileFields(dbfProfile)
            for row in dbfProfile:
                type = row['TYPE']
                code = row['CODE']
                exists = self.profileCache.get(code, None)
                if exists:
                    pass
                else:
                    self.profileCache[code] = self.tariffTypeDependOnProfileType.get(type, None)
            self.btnViewRbProfile.setEnabled(True)
            self.lblRbLoadedInfo.setText(u'Загружено: %d профилей'%len(dbfProfile))
            self.rbProfileLoaded = True

        except Exception, e:
            self.btnViewRbProfile.setEnabled(False)
            self.lblRbLoadedInfo.clear()
            self.rbProfileLoaded = False
            QtGui.QMessageBox.critical( self,
                                        u'Произошла ошибка',
                                        unicode(e),
                                        QtGui.QMessageBox.Close)


    @pyqtSignature('')
    def on_btnSelectFile_clicked(self):
        fileName = QtGui.QFileDialog.getOpenFileName(
            self, u'Укажите файл с данными', self.edtFileName.text(), u'Файлы DBF (*.dbf)')
        if fileName != '':
            self.edtFileName.setText(QDir.toNativeSeparators(fileName))
            self.btnImport.setEnabled(True)
            dbfFileName = forceStringEx(self.edtFileName.text())
            dbfTariff = Dbf(dbfFileName, readOnly=True, encoding='cp866')
            self.labelNum.setText(u'всего записей в источнике: '+str(len(dbfTariff)))


    @pyqtSignature('')
    def on_btnSelectFileRbProfile_clicked(self):
        fileName = QtGui.QFileDialog.getOpenFileName(
            self, u'Укажите файл с данными', self.edtRbProfileFileName.text(), u'Файлы DBF (*.dbf)')
        if fileName != '':
            self.edtRbProfileFileName.setText(QDir.toNativeSeparators(fileName))
            self.dbfProfileFileName = forceStringEx(self.edtRbProfileFileName.text())
        else:
            self.dbfProfileFileName = None
        self.btnLoadRbProfile.setEnabled(bool(self.dbfProfileFileName))



    @pyqtSignature('')
    def on_btnLoadRbProfile_clicked(self):
        self.loadRbProfiles()

    @pyqtSignature('')
    def on_btnViewRbProfile_clicked(self):
        fname=unicode(forceStringEx(self.edtRbProfileFileName.text()))
        if fname:
            CDbfViewDialog(self, fileName=fname).exec_()
