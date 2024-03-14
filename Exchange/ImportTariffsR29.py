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

u"""Импорт тарифа из XML для Архангельска"""
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt, QDate, QString
#from library.InDocTable import *
#from library.crbcombobox import CRBComboBox

#from library.TableModel import *
from Export29XMLCommon import Export29XMLCommon

from Exchange.ImportTariffsXML import copyTariff, getTariffDifference

#from Utils import *
from library.Utils     import forceBool, forceDouble, forceInt, forceRef, forceString, toVariant

from Exchange.Cimport import CXMLimport, CImportTariffsMixin
from Accounting.Tariff import CTariff

from Ui_ImportTariffsR29 import Ui_ImportTariffsR29
from Ui_ImportTariffsR29Filter import Ui_FilterDialog

#resultList = []
 
def ImportTariffsR29(widget, contractId, begDate, endDate, tariffList, tariffExpenseItems, tariffCoefficientItems):
    appPrefs = QtGui.qApp.preferences.appPrefs
    
    fileName = forceString(appPrefs.get('ImportTariffsR29FileName', ''))
    fullLog = forceBool(appPrefs.get('ImportTariffsR29FullLog', ''))
    updateTariff = forceBool(appPrefs.get('ImportTariffsR29UpdatePrices', ''))
  #  allowCoef = forceBool(appPrefs.get('ImportTariffsR29AllowCoef', ''))

    dlg = CImportTariffs(widget, fileName, contractId, begDate, endDate,
                         tariffList, tariffExpenseItems, tariffCoefficientItems)

    dlg.chkFullLog.setChecked(fullLog)
    dlg.chkUpdateTariff.setChecked(updateTariff)
 #   dlg.chkOnlyCodes.setChecked(onlyCodes)

    dlg.exec_()

    appPrefs['ImportTariffsR29FileName'] = toVariant(dlg.fileName)
    appPrefs['ImportTariffsR29FullLog'] = toVariant(dlg.chkFullLog.isChecked())
    appPrefs['ImportTariffsR29UpdatePrices'] = toVariant(dlg.chkUpdateTariff.isChecked())
 #   appPrefs['ImportTariffsR29AllowCoef'] = toVariant(dlg.chkAllowCoef.isChecked())

    return (not dlg.abort), dlg.tariffList,  dlg.tariffExpenseItems, dlg.tariffCoefficientItems #, dlg.chkAllowCoef



class CFilterDialog(QtGui.QDialog, Ui_FilterDialog):
    def __init__(self, resultList):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.resultList = resultList

        self.edtInfis.setText(forceString(QtGui.qApp.db.translate('Organisation',
            'id', QtGui.qApp.currentOrgId(), 'infisCode')))
        self.cmbTariffType.addItems(CTariff.tariffTypeNames)
        self.cmbEventType.setTable('EventType')
        self.cmbDepartment.setTable('rbServiceGroup')

    @QtCore.pyqtSignature('')
    def on_btnDelete_clicked(self):
        row = self.lstService.currentRow()
        self.lstService.takeItem(row)
        self.resultList.pop(row)


    @QtCore.pyqtSignature('')
    def on_btnAdd_clicked(self):
        result = {}
        result['infisCode'] = forceString(self.edtInfis.text())
        result['tariffType'] = self.cmbTariffType.currentIndex()
        result['eventType'] = self.cmbEventType.value()
        result['department'] = self.cmbDepartment.value()
        result['MES'] = self.cmbMES.currentIndex()
        result['amount'] = self.spbAmount.value()
        result['group'] = forceString(self.edtGroup.text())
        result['isSpecOrgStructure'] = self.chkSpecOrgStructure.isChecked()
        result['isIncompleteCaseStomotology'] = self.chkIncompleteCaseStomotology.isChecked()
        result['isAllowCoef'] = self.chkAllowCoef.isChecked()
        result['isStac'] = self.chkIsStac.isChecked()
        result['period'] = self.cmbPeriod.currentIndex()
        self.lstService.addItem(u'Тарификация: %s, тип события: %s, группа услуг: %s'%(self.translate(result)))
        self.resultList.append(result)

    def translate(self, dict):
        serviceGroup = forceString(QtGui.qApp.db.translate('rbServiceGroup',
            'id', dict['department'], 'code'))
        tariffType = CTariff.tariffTypeNames[dict['tariffType']]
        eventType = forceString(QtGui.qApp.db.translate('EventType',
            'id', dict['eventType'], 'name'))
        return tariffType, eventType, serviceGroup
    

class CImportTariffs(QtGui.QDialog, Ui_ImportTariffsR29, CXMLimport, CImportTariffsMixin):
    headerFields = ('ZGLV', 'VERSION', 'DATE')
    departmentFields = ('TARIF_LIST', 'USL_LIST', 'RUBRIKATOR', 'PG_LIST', 'RAZDEL_PG_LIST', 'DOP_LIST')
    tariffFields = ('MCOD', 'CODE', 'P_CODE', 'LPU_1', 'CODE_USL', 'NAME',  'VALUE', 'DATEBEG', 'DATEEND')
    tariffGroup = {'TARIF':{'fields': tariffFields}}
    tariffListGroup = {'TARIF_LIST': {'subGroup': tariffGroup}}
    tariffsGroup = {
        'ZGLV':  {'fields': headerFields},
        'TARIF_LIST': {'subGroup': tariffFields}
    }
    tariffsGroupName = 'RKU'


    def __init__(self, parent, fileName, contractId, begDate, endDate, tariffList, tariffExpenseItems, tariffCoefficientItems):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        CXMLimport.__init__(self)
        CImportTariffsMixin.__init__(self,  self.log, tariffList, tariffExpenseItems)

        self.fileName = fileName
        self.tariffCoefficientItems = list(tariffCoefficientItems)
        self.contractId = contractId
        self.begDate = begDate
        self.endDate = endDate

        if fileName:
            self.edtFileName.setText(fileName)
            self.btnImport.setEnabled(True)

        self._unitIdCache = {}
        self.findUnitId = lambda code: self.findIdByCode(code, 'rbMedicalAidUnit', self._unitIdCache)

        self._serviceCache = {}
        self.findService = lambda code, name: self.lookupIdByCodeName(code, name, self.tblService, self._serviceCache)


    def setImportMode(self, flag):
        self.chkFullLog.setEnabled(not flag)
   #     self.cmbServiceGroup.setEnabled(not flag)
        self.chkUpdateTariff.setEnabled(True)
        self.btnSelectFile.setEnabled(not flag)
        self.edtFileName.setEnabled(not flag)


    def startImport(self):
        resultList = []
        self.showFilterDialog(resultList)        
        fileName = self.edtFileName.text()
        self.setImportMode(True)

        if not fileName:
            return

        inFile = QtCore.QFile(fileName)
        if not inFile.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, u'Импорт тарифов для договора',
                                      QString(u'Не могу открыть файл для чтения %1:\n%2.')
                                      .arg(fileName)
                                      .arg(inFile.errorString()))
            return

        self.progressBar.setFormat(u'%v байт')
        self.progressBar.setMaximum(max(inFile.size(), 1))
        self.lblStatus.setText('')

        self.setDevice(inFile)

        while (not self.atEnd()):
            self.readNext()

            if self.isStartElement():
                if self.name() == self.tariffsGroupName:
                    xmlData = self.readTariffGroup()
                else:
                    self.raiseError(u'Неверный формат данных.')

            if self.hasError():
                break

        if not self.hasError():
            if resultList != []:
                for filter in resultList:
                    self.processData(xmlData, filter)
                    self.progressBar.setText(u'Готово')
            else:
                self.abort = True
                self.err2log(u'! Прервано пользователем.')
        else:
            self.progressBar.setText(u'Прервано')
            if self.abort:
                self.err2log(u'! Прервано пользователем.')
            else:
                self.err2log(u'! Ошибка: файл %s, %s' % (fileName,self.errorString()))

        inFile.close()
        self.setImportMode(False)
        
    def readTariffGroup(self):
        xmlData = []
        while (not self.atEnd()):
            self.readNext()

            if self.isStartElement():
                if self.name() == 'TARIF_LIST':
                        xmlData = self.readTariffs()
            if self.hasError():
                break
        return xmlData
    
    def readTariffs(self):
        xmlData = []
        while (not self.atEnd()):
            self.readNext()
            if self.isStartElement():
                if self.name() == 'TARIF':
                    xmlData.append(self.readGroup('TARIF', self.tariffFields))
            if self.hasError():
                break
        return xmlData
    
    def readGroup(self, groupName, fieldsList):
        if self.atEnd():
            return None
        result = {}
        while not (self.isEndElement() and self.name() == groupName):
            if self.name() in fieldsList:
                result[forceString(self.name())] = forceString(self.readElementText())
            self.readNext()
            if len(result) == len(fieldsList):
                break
        return result
    
    def showFilterDialog(self, resultList):
        dlg = CFilterDialog(resultList)
        dlg.exec_()


    def processData(self, data, filterDict):
        def getStacTariff(data, filterDict):
            if 'T' in dt['CODE_USL'] and filterDict['MES'] == 1:
                return forceRef(QtGui.qApp.db.getRecordEx('rbService',
                                                                         'id', 
                                                                         'code = "%s" AND group_id = "%s"'%
                                                                         ( dt['CODE_USL'], filterDict['department'])))
            elif 'T' not in dt['CODE_USL'] and filterDict['MES'] == 2:
                return forceRef(QtGui.qApp.db.getRecordEx('rbService',
                                                                         'id', 
                                                                         'code = "%s" AND group_id = "%s"'%
                                                                         ( dt['CODE_USL'], filterDict['department'])))
        self.progressBar.setText(u'Обработка данных...')
        self.progressBar.setMaximum(0)

        infisCode = filterDict.get('infisCode') #'290004'
        idsp = forceString(QtGui.qApp.db.translate('rbServiceGroup',
            'id', filterDict['department'], 'regionalCode'))
        unitId = forceString(QtGui.qApp.db.translate('rbMedicalAidUnit',
            'code', idsp, 'id'))
        groupCode = forceString(QtGui.qApp.db.translate('rbServiceGroup',
            'id', filterDict['department'], 'code'))

        lpu1Str = Export29XMLCommon.getMobileModule(QtGui.qApp.db, forceDouble(infisCode))
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(100)        
        for dt in data:
            
        #    QtGui.qApp.processEvents()
            if infisCode == dt['MCOD'] : #and groupCode in dt['CODE_USL']:
                service = None
                if filterDict['MES'] in (1,2) and filterDict['isStac'] == True:
                    if filterDict['isSpecOrgStructure'] == True and lpu1Str and  'LPU_1' in dt.keys():
                        service = getStacTariff(data, filterDict)
                    elif filterDict['isSpecOrgStructure'] == False and 'LPU_1' not in dt.keys():
                        service = getStacTariff(data, filterDict)
                elif filterDict['isIncompleteCaseStomotology'] == True:
                    if  'T' in dt['CODE_USL']:
                        service = forceRef(QtGui.qApp.db.getRecordEx('rbService',
                                                                     'id', 
                                                                     'code = "%s" AND group_id = "%s"'%
                                                                     ( dt['CODE_USL'], filterDict['department'])))
                else:
                    if  'T' not in dt['CODE_USL']:
                        service = forceRef(QtGui.qApp.db.getRecordEx('rbService',
                                                                         'id', 
                                                                         'code = "%s" AND group_id = "%s"'%
                                                                         ( dt['CODE_USL'], filterDict['department'])))
                if not service and filterDict['isStac'] == False:
                    service = forceRef(QtGui.qApp.db.getRecordEx('rbService',
                                                                         'id', 
                                                                         'code = "%s" AND group_id = "%s"'%
                                                                         ( dt['CODE'], filterDict['department'])))
                
  
                PG = {}
                if service:
    
                    serviceId = service.value('id')
                    if 'P_CODE' in dt.keys():
                        pgs = QtGui.qApp.db.getRecordList('rbPacientGroup_r29',
                                                              '*', 'code = "%s"'%dt['P_CODE'])
                        if not pgs:
                            break
                        
                        for pg in pgs:
                            PG[forceString(pg.value('age'))] = [forceString(pg.value('sex')), forceString(pg.value('code'))]
                    else:
                        PG[None] = None
                    begDate = QDate.fromString(dt['DATEBEG'], Qt.ISODate)
                    if 'DATEEND' in dt.keys():
                        endDate = QDate.fromString(dt['DATEEND'], Qt.ISODate)
                    else:
                        endDate = None
                
                    price = forceDouble(dt['VALUE'])
                    tariffType = filterDict.get('tariffType', CTariff.ttVisit)
                    eventType = filterDict.get('eventType', 0)
                    amount = filterDict.get('amount', 0)
                    MES = filterDict.get('MES', 0)
                    period = filterDict.get('period', 0)
                    group = filterDict.get('group')
                    for key, value in  PG.items(): 
                        if self.endDate > begDate and (endDate > self.begDate or endDate== None):
                            tariff = self.tblContract_Tariff.newRecord()
                            tariff.setValue('price', price)
                            tariff.setValue('eventType_id',  toVariant(eventType))
                            tariff.setValue('service_id',  toVariant(serviceId))
                            tariff.setValue('master_id',  toVariant(self.contractId))
                            tariff.setValue('begDate', toVariant(begDate))
                            tariff.setValue('endDate', toVariant(endDate))
                            tariff.setValue('tariffType',  toVariant(tariffType))
                            tariff.setValue('amount',  toVariant(amount))
                            if unitId:
                                tariff.setValue('unit_id', toVariant(unitId))
                            tariff.setValue('age', toVariant(key))
                            if key:
                                tariff.setValue('sex', toVariant(value[0]))
                                tariff.setValue('pg', toVariant(value[1]))
                            tariff.setValue('batch', toVariant(group))
                            tariff.setValue('mesStatus', toVariant(MES))
                            tariff.setValue('controlPeriod', toVariant(period))
                            if filterDict['isAllowCoef'] == True:
                                tariff.setValue('enableCoefficients', toVariant(1))
                            self.addOrUpdateTariffs(dt['CODE'], tariff, [])
            
                QtGui.qApp.processEvents()
                self.progressBar.step()    
                
    def addOrUpdateTariffs(self, serviceCode, newTariff, newExpenses):
        def _addTariffs():
            self.log.append(u'Добавляем тариф для услуги %s' % serviceCode)
            self.nAdded += 1
            self.addTariff(newTariff)
            self.tariffExpenseItems.append(newExpenses)
        
        eventType = forceInt(newTariff.value('eventType'))    
        tariffType = forceInt(newTariff.value('tariffType'))
        serviceId  = forceRef(newTariff.value('service_id'))
        sex = forceInt(newTariff.value('sex'))
        age = forceString(newTariff.value('age'))
        tariffCategoryId = forceRef(newTariff.value('tariffCategory_id'))

        key = (eventType, tariffType, serviceId, sex, age, tariffCategoryId)
        tariffIndexList = self.tariffDict.get(key, None)

        if tariffIndexList:
            self.log.append(u'Найден совпадающий тариф.')

            # проверяем интервалы действия тарифов на пересечение
            for i in tariffIndexList:
                tariff = self.tariffList[i]

                if self.tariffPeriodIntersect(tariff, newTariff):
                    break
            # если не пересекаются - добавляем новый
            else:
                self.log.append(u'Интервал действия тарифа не пересекается с имеющимися.')
                _addTariffs()
                return

            if self.dupSkip:
                self.log.append(u'Пропускаем.')
                self.nSkipped += len(tariffIndexList)
                return

            for i in tariffIndexList:
                tariff = self.tariffList[i]
                diffStr = getTariffDifference(tariff, self.tariffExpenseItems[self.tariffList.index(tariff)],
                                                                                                    newTariff,  newExpenses)

                if not diffStr or not self.tariffPeriodIntersect(tariff, newTariff):
                    self.nSkipped += 1
                    break

                if self.dupUpdate:
                    self.log.append(u'Обновляем.')
                    self.tariffExpenseItems[self.tariffList.index(tariff)] = newExpenses
                    copyTariff(tariff, newTariff)
                    self.nUpdated += 1
                else:
                    self.log.append(u'Запрос действий у пользователя.')
                    answer = QtGui.QMessageBox.question(self, u'Совпадающий тариф',
                                        u'Услуга "%s"\nРазличия: %s\n'
                                        u'Обновить?' %(serviceCode, diffStr),
                                        QtGui.QMessageBox.No|QtGui.QMessageBox.Yes,
                                        QtGui.QMessageBox.No)
                    self.log.append(u'Выбор пользователя %s' % \
                    (u'обновить' if answer == QtGui.QMessageBox.Yes else u'пропустить'))
                    if answer == QtGui.QMessageBox.Yes:
                        self.tariffExpenseItems[self.tariffList.index(tariff)] = newExpenses
                        copyTariff(tariff, newTariff)
                        self.nUpdated += 1
                    else:
                        self.nSkipped += 1
        else:
            _addTariffs()           
    
    def addTariffs(self, newTariff):
        tariffType = forceInt(newTariff.value('tariffType'))
        serviceId  = forceRef(newTariff.value('service_id'))
        sex = forceInt(newTariff.value('sex'))
        age = forceString(newTariff.value('age'))
        category = forceRef(newTariff.value('tariffCategory_id'))

        i = len(self.tariffList)
        self.tariffList.append(newTariff)
        key = (tariffType, serviceId, sex, age, category)
        tariffIndexList = self.tariffDict.setdefault(key, [])
        tariffIndexList.append(i)

    def processStomatology(self, tariff, data):
        serviceCode = forceString(tariff.get('CODE'))
        serviceName = forceString(tariff.get('USL_NAME'))
        serviceId = self.findService(serviceCode, serviceName)

        if not serviceId:
            self.err2log(u'Услуга `%s` `%s` не найдена, пропускаем' % (serviceCode, serviceName))
            return
        
        begDate = QDate.fromString(tariff.get('DATE_BEG', ''), Qt.ISODate)
        endDate = QDate.fromString(tariff.get('DATE_END', ''), Qt.ISODate)
        maturePrice = forceDouble(tariff.get('USL_UET_V', 0.0))
        childPrice = forceDouble(tariff.get('USL_UET_D', 0.0))
        tariffType = data.get('tariffType', CTariff.ttVisit)
        
        for (uet, age) in ((maturePrice, u'18г-'), (childPrice, u'-17г')):
            if uet > 0.0:
                tariff = self.tblContract_Tariff.newRecord()
                tariff.setValue('uet', uet)
                tariff.setValue('service_id',  toVariant(serviceId))
                tariff.setValue('master_id',  toVariant(self.contractId))
                tariff.setValue('begDate', toVariant(begDate))
                tariff.setValue('endDate', toVariant(endDate))
                tariff.setValue('tariffType',  toVariant(tariffType))
                tariff.setValue('age', toVariant(age))
                self.addOrUpdateTariffs(serviceCode, tariff, [])

        QtGui.qApp.processEvents()
        self.progressBar.step()
