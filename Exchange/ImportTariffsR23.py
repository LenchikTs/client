# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2015 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
u"""
Импорт тарифа в R23
"""
from PyQt4 import QtGui
from PyQt4.QtCore import QDate, QDir, pyqtSignature

from library.dbfpy.dbf import Dbf
from library.Utils import forceDate, forceDouble, forceInt, forceRef, forceString, forceStringEx, toVariant

from Accounting.Tariff import CTariff
from Exchange.Cimport import CDBFimport, Cimport, CImportTariffsMixin

from Reports.ReportBase import CReportBase
from Reports.ReportView import CReportViewDialog

from Exchange.ImportTariffsXML import getTariffDifference, copyTariff

from Exchange.Ui_ImportTariffsR23 import Ui_Dialog


def ImportTariffsR23(widget, contractId, begDate, endDate, tariffList, tariffExpenseItems, tariffCoefficientItems):
    dlg=CImportTariffs(widget, contractId, begDate, endDate, tariffList, tariffExpenseItems, tariffCoefficientItems)
    dlg.edtSpr22.setText(forceString(QtGui.qApp.preferences.appPrefs.get('ImportTariffR23FileName22', '')))
    dlg.exec_()
    QtGui.qApp.preferences.appPrefs['ImportTariffR23FileName22'] = toVariant(dlg.edtSpr22.text())
    return (not dlg.abort), dlg.tariffList, dlg.tariffExpenseItems, dlg.tariffCoefficientItems


class CImportTariffs(QtGui.QDialog, Ui_Dialog, CDBFimport, CImportTariffsMixin):
    @pyqtSignature('')
    def on_btnImport_clicked(self): CDBFimport.on_btnImport_clicked(self)
    @pyqtSignature('')
    def on_btnClose_clicked(self): CDBFimport.on_btnClose_clicked(self)
    @pyqtSignature('')
    def on_btnView_clicked(self): CDBFimport.on_btnView_clicked(self)

    def __init__(self,  parent, contractId, begDate, endDate, tariffList, tariffExpenseItems, tariffCoefficientItems):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        Cimport.__init__(self, self.log)
        CImportTariffsMixin.__init__(self, self.log, tariffList, tariffExpenseItems)

        self.contractId = contractId
        self.tariffCoefficientItems = list(tariffCoefficientItems)

        self.tariffType = None
        self.loadMature = False
        self.loadChildren = False
        self.begDate = begDate
        self.endDate = endDate
        self.tfoms = False
        self.tfomsDup = []
        self.dupAskUser = False
        self.dupUpdate = False
        self.dupSkip = False
        self.serviceCache = {}

        self.nSkipped = 0
        self.nAdded = 0
        self.nUpdated = 0
        self.nProcessed = 0

        self.amount = 0


    def startImport(self):
        contractId = self.contractId
        if not contractId:
            return

        self.nSkipped = 0
        self.nAdded = 0
        self.nUpdated = 0
        self.nProcessed = 0
        self.serviceCache = {}

        self.tfoms = self.chkTFOMS.isChecked()
        self.tfomsDup = []
        self.dupAskUser = self.chkAskUser.isChecked()
        self.dupUpdate = self.chkUpdate.isChecked()
        self.dupSkip = self.chkSkip.isChecked()

        dbfFileName = forceStringEx(self.edtSpr22.text())
        dbfSpr22 = Dbf(dbfFileName, readOnly=True, encoding='cp866')
        self.progressBar.setValue(0)
        self.progressBar.setFormat('%v')
        rowCount = len(dbfSpr22)
        self.progressBar.setMaximum(rowCount)
        self.labelNum.setText(u'всего записей в источнике: %i' % (rowCount))

        self.process(dbfSpr22, self.processSpr22)
        dbfSpr22.close()

        self.log.append(u'добавлено: %d; изменено: %d' % (self.nAdded, self.nUpdated))
        self.log.append(u'пропущено: %d; обработано: %d' % (self.nSkipped, self.nProcessed))
        self.log.append(u'готово')
        if self.tfomsDup:
            self.showTFOMSDup()


    def process(self, dbf,  step):
        self.log.append(u'Обработка `%s`....' % dbf.name)

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
                
                
    def findServiceAndUetByInfisCode(self, code):
        result = self.serviceCache.get(code, (None, None))

        if not result[0]:
            rbService = QtGui.qApp.db.table('rbService')
            record = forceRef(QtGui.qApp.db.translate('rbService', 'infis', code, 'id'))
            record = QtGui.qApp.db.getRecordEx(rbService, 'id, adultUetDoctor', rbService['infis'].eq(code), 'id desc')
            if record:
                result = forceRef(record.value("id")), forceDouble(record.value("adultUetDoctor"))
                self.serviceCache[code] = result
        return result


    def processSpr22(self, row):
        tariffbegDate = QDate(row['DATN'])
        begDate = forceDate(row['DATN'])
        tariffendDate = QDate(row['DATO']) if row['DATO'] else None
        endDate = forceDate(row['DATO']) if row['DATO'] else None
        serviceCode = forceString(row['KUSL'].strip())
        (serviceId, uet) = self.findServiceAndUetByInfisCode(serviceCode)

        if not serviceId:
            self.log.append(u'<b><font color=orange>ОШИБКА:</b>'
                u' Услуга, код ИНФИС: "%s", не найдена' % serviceCode)
            self.nSkipped += 1
            return

        newRecord = self.tblContract_Tariff.newRecord()
        newRecord.setValue('price', toVariant(row['TARIF']))

        newRecord.setValue('amount', toVariant(0))
        newRecord.setValue('uet', toVariant(uet))
        newRecord.setValue('service_id', serviceId)
        newRecord.setValue('master_id', toVariant(self.contractId))
        newRecord.setValue('begDate', toVariant(tariffbegDate))
        newRecord.setValue('endDate', toVariant(tariffendDate))
        
        newRecord.setValue('batch', toVariant(''))
        newRecord.setValue('frag1Start', toVariant(0))
        newRecord.setValue('frag1Price', toVariant(0))
        newRecord.setValue('frag1Sum', toVariant(0))
        newRecord.setValue('frag2Start', toVariant(0))
        newRecord.setValue('frag2Sum', toVariant(0))
        newRecord.setValue('frag2Price', toVariant(0))
        newRecord.setValue('federalLimitation', toVariant(0))
        newRecord.setValue('federalPrice', toVariant(0))
        

        if serviceCode[:1] in ('A', 'B', 'K'):
            if uet:
                newRecord.setValue('tariffType',  toVariant(CTariff.ttActionUET))
            else:
                newRecord.setValue('tariffType',  toVariant(CTariff.ttActionAmount))
        # импорт тарифов КСГ
        elif serviceCode[:1] == 'G' and len(serviceCode) > 7:
            newRecord.setValue('tariffType',  toVariant(CTariff.ttKrasnodarA13))
            newRecord.setValue('frag1Sum', toVariant(row['TARIF']))
            newRecord.setValue('frag2Sum', toVariant(row['TARIF']))
            db = QtGui.qApp.db
            # проставляем длительности
            tableS71 = db.table('soc_spr71')
            tableS72 = db.table('soc_spr72')
            cond = [tableS71['ksgkusl'].eq(serviceCode), 
                u'soc_spr71.datn <={0:s}'.format(db.formatDate(begDate)), 
                u'soc_spr71.dato >={0:s}'.format(db.formatDate(begDate))
            ]
            cond2 = [tableS72['ksgkusl'].eq(serviceCode), 
                u'soc_spr72.datn <={0:s}'.format(db.formatDate(begDate)), 
                u'soc_spr72.dato >={0:s}'.format(db.formatDate(begDate))
            ]
            if endDate:
                cond.append(u'soc_spr71.dato <={0:s}'.format(db.formatDate(endDate)))
                cond2.append(u'soc_spr72.dato <={0:s}'.format(db.formatDate(endDate)))
                
            if QtGui.qApp.db.getRecordEx(tableS71, 'ksgkusl', cond, 'ksgkusl'):
                newRecord.setValue('frag1Start',  toVariant(1))
            else:
                newRecord.setValue('frag1Start',  toVariant(3))
            if QtGui.qApp.db.getRecordEx(tableS72, 'ksgkusl', cond2, 'ksgkusl'):
                newRecord.setValue('frag2Start',  toVariant(46))
            else:
                newRecord.setValue('frag2Start',  toVariant(31))
            
            # # Проставляем единицу учета
            # rbMedicalAidUnit = QtGui.qApp.db.table('rbMedicalAidUnit')
            # if serviceCode[1] == '1':
            #     regCode = '33'
            # else:
            #     regCode = '43'
            # unitRecord = QtGui.qApp.db.getRecordEx(rbMedicalAidUnit, 'id', rbMedicalAidUnit['regionalCode'].eq(regCode), 'id')
            # if unitRecord:
            #     newRecord.setValue('unit_id', toVariant(unitRecord.value("id")))
        else:
            newRecord.setValue('tariffType', toVariant(CTariff.ttActionAmount))
            # self.log.append(u'<b><font color=orange>ОШИБКА:</b>'
            #     u' Услуга, код ИНФИС: "%s", нет правила для добавления тарифа. Сообщите разработчику.' % serviceCode)
            # self.nSkipped += 1
            # return


        self.log.append(u'Тариф: `%s`, цена %.2f, количество %.2f, дата c %s%s'
                        % (serviceCode, forceDouble(newRecord.value('price')),
                                                    forceDouble(newRecord.value('amount')),
                                                    forceDate(newRecord.value('begDate')).toString('dd.MM.yyyy'),
                                                    u' по ' + forceDate(newRecord.value('endDate')).toString('dd.MM.yyyy') if newRecord.value('endDate') else ''))

        self.addOrUpdateTariff(serviceCode, newRecord)


    def addOrUpdateTariff(self, serviceCode, newTariff):
        tariffType = forceInt(newTariff.value('tariffType'))
        serviceId  = forceRef(newTariff.value('service_id'))
        sex = forceInt(newTariff.value('sex'))
        age = forceString(newTariff.value('age'))
        newBegDate = forceDate(newTariff.value('begDate'))
        newEndDate = forceDate(newTariff.value('endDate'))
        category = forceRef(newTariff.value('tariffCategory_id'))
        newUnitId = forceRef(newTariff.value('unit_id'))

        key = (tariffType, serviceId, sex, age, category)
        tariffIndexList = self.tariffDict.get(key, None)
        if tariffIndexList:
            self.log.append(u'Найден совпадающий тариф.')

            if self.dupSkip and not self.tfoms:
                self.log.append(u'Пропускаем.')
                self.nSkipped += 1
                return

            for i in tariffIndexList:
                tariff = self.tariffList[i]
                oldBegDate = forceDate(tariff.value('begDate'))
                oldEndDate = forceDate(tariff.value('endDate'))
                if (oldEndDate and self.tfoms) or (oldBegDate != newBegDate): #ТФОМС: Закрытые тарифы не трогаем, все что закрыто в договоре - должно остаться без изменения
                    continue
                    
                if not newUnitId:
                    newTariff.setValue('unit_id', toVariant(tariff.value('unit_id')))
                    
                diffStr = getTariffDifference(tariff, [], newTariff, [])
                
                # Если есть полное совпадение, выходим
                if not diffStr:
                    self.log.append(u'Количество, цены и ограничения совпадают, пропускаем.')
                    self.nSkipped += 1
                    return

                if self.dupUpdate and not self.tfoms:
                    self.log.append(u'Обновляем.')
                    copyTariff(tariff, newTariff)
                    self.nUpdated += 1
                elif not self.tfoms:
                    self.log.append(u'Запрос действий у пользователя.')
                    answer = QtGui.QMessageBox.question(self, u'Совпадающий тариф',
                                        u'Услуга "%s"\nРазличия: %s\n'
                                        u'Обновить?' %(serviceCode, diffStr),
                                        QtGui.QMessageBox.No|QtGui.QMessageBox.Yes,
                                        QtGui.QMessageBox.No)
                    self.log.append(u'Выбор пользователя %s' % \
                    (u'обновить' if answer == QtGui.QMessageBox.Yes else u'пропустить'))
                    if answer == QtGui.QMessageBox.Yes:
                        copyTariff(tariff, newTariff)
                        self.nUpdated += 1
                    else:
                        self.nSkipped += 1
                 # изменения в тариф внесены, выходим
                if self.tfoms:
                    self.tfomsDup.append(serviceCode)
                    continue
                return

            #  с новым тарифом не совпали даты. Добавляем
            if not (forceDate(tariff.value('endDate')) and self.tfoms): #ТФОМС: Закрытые тарифы не трогаем, все что закрыто в договоре - должно остаться без изменения
                self.log.append(u'Добавляем тариф с %s%s' % (newBegDate.toString('dd.MM.yyyy'), u' по ' + newEndDate.toString('dd.MM.yyyy') if newEndDate else ''))
                self.appendTariff(newTariff, tariffIndexList)
                if self.tfoms:
                    self.nUpdated += 1
            else:
                self.log.append(u'Пропускаем.')
                self.nSkipped += 1
        else:
            self.log.append(u'Добавляем тариф для услуги %s' % serviceCode)
            self.nAdded += 1
            self.addTariff(newTariff)


    def appendTariff(self, newTariff, tariffIndexList):
        newBegDate = forceDate(newTariff.value('begDate'))
        newEndDate = forceDate(newTariff.value('endDate'))
        closestBegDate = QDate()
        isModified = False

        for i in tariffIndexList:
            tariff = self.tariffList[i]

            begDate = forceDate(tariff.value('begDate'))
            endDate = forceDate(tariff.value('endDate'))

            # новый тариф попал внутрь ищеющегося
            if (begDate.isValid() and endDate.isValid()
                and (begDate <= newBegDate)
                and (endDate >= newBegDate)
                and (begDate <= newEndDate)
                and (endDate >= newEndDate)):
                tariff.setValue('endDate', toVariant(newBegDate.addDays(-1)))
                newTariff.setValue('endDate', toVariant(endDate))
                isModified = True
                break

            # тариф без окончания срока действия
            if (begDate.isValid() and not endDate.isValid()):
                if begDate <= newBegDate:
                    tariff.setValue('endDate', toVariant(newBegDate.addDays(-1)))
                if begDate > newBegDate:
                    newTariff.setValue('endDate', begDate.addDays(-1))

                isModified = True
                break

            if (begDate.isValid() and endDate.isValid()):
                if begDate > newBegDate:
                    if closestBegDate.isValid() and (closestBegDate.toJulianDay() - begDate.toJulianDay()) > 0:
                        closestBegDate = begDate

        if isModified and closestBegDate.isValid():
            newTariff.setValue('endDate', closestBegDate.addDays(-1))


        self.nAdded += 1
        self.addTariff(newTariff)


    def setContractCoefficient(self, typeId, date, value):
        isUpdated = False

        for record in self.tariffCoefficientItems:
            oldTypeId = forceRef(record.value('coefficientType_id'))

            if typeId == oldTypeId:
                oldBegDate = forceDate(record.value('begDate'))

                if oldBegDate == date:
                    record.setValue('value', toVariant(value))
                    isUpdated = True
                    break

        if not isUpdated:
            record = self.tblContract_Coefficient.newRecord()
            record.setValue('coefficientType_id', toVariant(typeId))
            record.setValue('begDate', toVariant(date))
            record.setValue('value', toVariant(value))
            self.tariffCoefficientItems.append(record)


    def checkFileName(self):
        flag = not self.edtSpr22.text().isEmpty()
        self.btnImport.setEnabled(flag)
        
        
    def showTFOMSDup(self):
        report = CReportBase()
        params = report.getDefaultParams()
        report.saveDefaultParams(params)
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Перечень дубликатов:')
        cursor.insertHtml('<br/><br/>')
        for tariff in self.tfomsDup:
            cursor.insertText(u'Услуга: {}'.format(tariff))
            cursor.insertHtml('<br/><br/>')
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertHtml('<br/><br/>')
        reportView = CReportViewDialog(self)
        reportView.setWindowTitle(u'Результаты импорта')
        reportView.setOrientation(QtGui.QPrinter.Portrait)
        reportView.setText(doc)
        reportView.exec_()


    @pyqtSignature('')
    def on_btnSelect22_clicked(self):
        fileName = QtGui.QFileDialog.getOpenFileName(
            self, u'Укажите файл с данными', self.edtSpr22.text(), u'Файлы DBF (*.dbf)')
        if fileName:
            self.edtSpr22.setText(QDir.toNativeSeparators(fileName))
            self.checkFileName()
