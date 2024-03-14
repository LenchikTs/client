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
import re

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QFile, QString, QTextStream, pyqtSignature, SIGNAL

from library.AgeSelector import composeAgeSelector, parseAgeSelector
from library.database import CDatabaseException
from library.Utils import forceBool, forceDouble, forceInt, forceRef, forceString, forceStringEx, toVariant, trim

from Accounting.Tariff import CTariff

from Exchange.Ui_ImportTariffsCSV import Ui_ImportTariffsCSV

# wtf? действительно есть тонкая связь между групповым редактором типов действий и тарифами?
from RefBooks.ActionType.Ui_GroupActionTypeEditor import Ui_GroupActionTypeEditorDialog

tariffSimpleFields = ('tariffType', 'batch', 'begDate', 'endDate', 'sex', 'age', 'MKB',
                      'amount', 'uet', 'price',
                      'frag1Start', 'frag1Sum', 'frag1Price',
                      'frag2Start', 'frag2Sum', 'frag2Price',
                      'limitationExceedMode',  'limitation',
                      'priceEx',
                      'federalLimitation', 'federalPrice',
                      'regionalLimitation', 'regionalPrice',
                     )

tariffRefFields    =  ('eventType_id', 'service_id', 'unit_id', 'tariffCategory_id',  'result_id')

tariffKeyFields    = ('service_id')

def ImportTariffsCSV(widget, tariffRecordList):
    appPrefs = QtGui.qApp.preferences.appPrefs

    fileName = forceString(appPrefs.get('ImportTariffsCSVFileName', ''))
    fullLog = forceBool(appPrefs.get('ImportTariffsCSVFullLog', ''))
    updateTariff = forceBool(appPrefs.get('ImportTariffsCSVUpdatePrices', ''))
    onlyCodes = forceBool(appPrefs.get('ImportTariffsCSVOnlyCodes', ''))
    addMissing = forceBool(appPrefs.get('ImportTariffsCSVAddMissing', ''))
    dlg = CImportTariffsCSV(fileName, tariffRecordList,  widget)
    dlg.chkFullLog.setChecked(fullLog)
    dlg.chkUpdateTariff.setChecked(updateTariff)
    dlg.chkOnlyCodes.setChecked(onlyCodes)
    dlg.chkAddServicesAndAT.setChecked(addMissing)
    dlg.exec_()
    appPrefs['ImportTariffsCSVFileName'] = toVariant(dlg.fileName)
    appPrefs['ImportTariffsCSVFullLog'] = toVariant(dlg.chkFullLog.isChecked())
    appPrefs['ImportTariffsCSVUpdatePrices'] = toVariant(dlg.chkUpdateTariff.isChecked())
    appPrefs['ImportTariffsCSVOnlyCodes'] = toVariant(dlg.chkOnlyCodes.isChecked())
    appPrefs['ImportTariffsCSVAddMissing'] = toVariant(dlg.chkAddServicesAndAT.isChecked())
    return dlg.tariffRecordList if not dlg.aborted else []


class CGroupActionTypeEditor(QtGui.QDialog, Ui_GroupActionTypeEditorDialog):
    def __init__(self, parent = None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.confirmed = False

    def done(self, result):
        if result:
            self.confirmed = True
        QtGui.QDialog.done(self, result)

    def loadSettings(self, fields):
        sex = fields.get('sex', None)
        if sex:
            self.chkSex.setChecked(True)
            self.cmbSex.setCurrentIndex(sex)
        age = fields.get('age', None)
        if age:
            self.chkAge.setChecked(True)
            (begUnit, begCount, endUnit, endCount) = parseAgeSelector(age)
            self.cmbBegAgeUnit.setCurrentIndex(begUnit)
            self.edtBegAgeCount.setText(str(begCount))
            self.cmbEndAgeUnit.setCurrentIndex(endUnit)
            self.edtEndAgeCount.setText(str(endCount))
        if 'showTime' in fields:
            self.chkChkShowTime.setChecked(True)
            self.chkShowTime.setChecked(fields['showTime'])
        if 'isRequiredCoordination' in fields:
            self.chkChkRequiredCoordination.setChecked(True)
            self.chkRequiredCoordination.setChecked(fields['isRequiredCoordination'])
        if 'showInForm' in fields:
            self.chkChkShowInForm.setChecked(True)
            self.chkShowInForm.setChecked(fields['showInForm'])
        if 'hasAssistant' in fields:
            self.chkAssistant.setChecked(True)
            self.chkHasAssistant.setChecked(fields['hasAssistant'])
        if 'context' in fields:
            self.chkContext.setChecked(True)
            self.edtContext.text(fields['context'])
        if 'isPreferable' in fields:
            self.chkPreferable.setChecked(True)
            self.chkIsPreferable.setChecked(fields['isPreferable'])
        if 'maxOccursInEvent' in fields:
            self.chkMaxOccursInEvent.setChecked(True)
            self.edtMaxOccursInEvent.setValue(fields['maxOccursInEvent'])
        if 'serviceType' in fields:
            self.chkServiceType.setChecked(True)
            self.cmbServiceType.setValue(fields['serviceType'])
        if 'exposeDateSelector' in fields:
            self.chkExposeDateSelector.setChecked(True)
            self.cmbExposeDateSelector.setCurrentIndex(fields['exposeDateSelector'])
        if 'defaultStatus' in fields:
            self.chkDefaultStatus.setChecked(True)
            self.cmbDefaultStatus.setCurrentIndex(fields['defaultStatus'])
        if 'defaultPlannedEndDate' in fields:
            self.chkDefaultPlannedEndDate.setChecked(True)
            self.cmbDefaultPlannedEndDate.setCurrentIndex(fields['defaultPlannedEndDate'])
        if 'defaultEndDate' in fields:
            self.chkDefaultEndDate.setChecked(True)
            self.cmbDefaultEndDate.setCurrentIndex(fields['defaultEndDate'])
        if 'defaultDirectionDate' in fields:
            self.chkDefaultDirectionDate.setChecked(True)
            self.cmbDefaultDirectionDate.setCurrentIndex(fields['defaultDirectionDate'])
        if 'defaultExecPerson_id' in fields:
            self.chkDefaultExecPerson.setChecked(True)
            self.cmbDefaultExecPerson.setValue(fields['defaultExecPerson_id'])
        if 'defaultPersonInEvent' in fields:
            self.chkDefaultPersonInEvent.setChecked(True)
            self.cmbDefaultPersonInEvent.setCurrentIndex(fields['defaultPersonInEvent'])
        if 'defaultPersonInEditor' in fields:
            self.chkDefaultPersonInEditor.setChecked(True)
            self.cmbDefaultPersonInEditor.setCurrentIndex(fields['defaultPersonInEditor'])
        if 'defaultMKB' in fields:
            self.chkDefaultMKB.setChecked(True)
            self.cmbDefaultMKB.setCurrentIndex(fields['defaultMKB'])
        if 'isMorphologyRequired' in fields:
            self.chkIsMorphologyRequired.setChecked(True)
            self.cmbIsMorphologyRequired.setCurrentIndex(fields['isMorphologyRequired'])
        if 'defaultOrg_id' in fields:
            self.chkDefaultOrg.setChecked(True)
            self.cmbDefaultOrg.setValue(fields['defaultOrg_id'])
        if 'amount' in fields:
            self.chkAmount.setChecked(True)
            self.edtAmount.setValue(fields['amount'])
        if 'office' in fields:
            self.chkOffice.setChecked(True)
            self.edtOffice.setText(fields['office'])
        if 'propertyAssignedVisible' in fields:
            self.grpPropertiesFields.setChecked(True)
            self.chkPropertyAssignedVisible.setChecked(fields['propertyAssignedVisible'])
            self.chkPropertyUnitVisible.setChecked(fields['propertyUnitVisible'])
            self.chkPropertyNormVisible.setChecked(fields['propertyNormVisible'])
            self.chkPropertyEvaluationVisible.setChecked(fields['propertyEvaluationVisible'])


    def getSettings(self):
        if not self.confirmed:
            return {}
        fields = {'id':None}
        if self.chkSex.isChecked():
            fields['sex'] = self.cmbSex.currentIndex()
        if self.chkAge.isChecked():
            fields['age'] = composeAgeSelector(self.cmbBegAgeUnit.currentIndex(),  forceStringEx(self.edtBegAgeCount.text()),
                                               self.cmbEndAgeUnit.currentIndex(),  forceStringEx(self.edtEndAgeCount.text()))
        if self.chkChkShowTime.isChecked():
            fields['showTime'] = self.chkShowTime.isChecked()
        if self.chkChkRequiredCoordination.isChecked():
            fields['isRequiredCoordination'] = self.chkRequiredCoordination.isChecked()
        if self.chkChkShowInForm.isChecked():
            fields['showInForm'] = self.chkShowInForm.isChecked()
        if self.chkAssistant.isChecked():
            fields['hasAssistant'] = self.chkHasAssistant.isChecked()
        if self.chkContext.isChecked():
            fields['context'] = forceStringEx(self.edtContext.text())
        if self.chkPreferable.isChecked():
            fields['isPreferable'] = self.chkIsPreferable.isChecked()
        if self.chkMaxOccursInEvent.isChecked():
            fields['maxOccursInEvent'] = self.edtMaxOccursInEvent.value()
        if self.chkServiceType.isChecked():
            fields['serviceType'] = self.cmbServiceType.value()
        if self.chkExposeDateSelector.isChecked():
            fields['exposeDateSelector'] = self.cmbExposeDateSelector.currentIndex()
        if self.chkDefaultStatus.isChecked():
            fields['defaultStatus'] = self.cmbDefaultStatus.currentIndex()
        if self.chkDefaultPlannedEndDate.isChecked():
            fields['defaultPlannedEndDate'] = self.cmbDefaultPlannedEndDate.currentIndex()
        if self.chkDefaultEndDate.isChecked():
            fields['defaultEndDate'] = self.cmbDefaultEndDate.currentIndex()
        if self.chkDefaultDirectionDate.isChecked():
            fields['defaultDirectionDate'] = self.cmbDefaultDirectionDate.currentIndex()
        if self.chkDefaultExecPerson.isChecked():
            fields['defaultExecPerson_id'] = self.cmbDefaultExecPerson.value()
        if self.chkDefaultPersonInEvent.isChecked():
            fields['defaultPersonInEvent'] = self.cmbDefaultPersonInEvent.currentIndex()
        if self.chkDefaultPersonInEditor.isChecked():
            fields['defaultPersonInEditor'] = self.cmbDefaultPersonInEditor.currentIndex()
        if self.chkDefaultMKB.isChecked():
            fields['defaultMKB'] = self.cmbDefaultMKB.currentIndex()
        if self.chkIsMorphologyRequired.isChecked():
            fields['isMorphologyRequired'] = self.cmbIsMorphologyRequired.currentIndex()
        if self.chkDefaultOrg.isChecked():
            fields['defaultOrg_id'] = self.cmbDefaultOrg.value()
        if self.chkAmount.isChecked():
            fields['amount'] = self.edtAmount.value()
        if self.chkOffice.isChecked():
            fields['office'] = forceStringEx(self.edtOffice.text())
        if self.grpPropertiesFields.isChecked():
            fields['propertyAssignedVisible'] = self.chkPropertyAssignedVisible.isChecked()
            fields['propertyUnitVisible'] = self.chkPropertyUnitVisible.isChecked()
            fields['propertyNormVisible'] = self.chkPropertyNormVisible.isChecked()
            fields['propertyEvaluationVisible'] = self.chkPropertyEvaluationVisible.isChecked()
        return fields


class CCsvReader(object):
    def __init__(self, parent, mainGroupId, tariffRecordList, showLog, updateTariff,  onlyCodes, addMissing):
        self.table = QtGui.qApp.db.table('Contract_Tariff')
        self._parent = parent
        #self.contractId = contractId
        self.tariffRecordList = tariffRecordList
        self.showLog = showLog
        self.updateTariff = updateTariff
        self.onlyCodes = onlyCodes
        self.addMissing = addMissing

        self.mapTariffKeyToRecordList = {}
        for record in self.tariffRecordList:
            self.addTariffToMap(record)

        self.refValueCache = {}
        self.headers = {}
        self.currentGroupId = 0
        self.mainGroupId = mainGroupId
        self.resultTariffList = []

        self.reSpaces = re.compile(r'\s+')

        self.skip = False
        self.nadded = 0
        self.ncoincident = 0
        self.nprocessed = 0
        self.nupdated = 0
        self.nskipped = 0


    def getTariffKey(self, record):
        #return tuple([ forceStringEx(record.value(fieldName)) if not record.value(fieldName).isNull() else None for fieldName in tariffKeyFields ])
        return forceInt(record.value('service_id')) if not record.value('service_id').isNull() else 0


    def getTariffDescr(self, record):

        parts = []
        for fieldName in tariffKeyFields:
            if fieldName in self.refValueCache:
                value = forceRef(record.value(fieldName))
                if value:
                    value = forceString(self.refValueCache[fieldName].getNameById(value))
            elif fieldName == 'tariffType':
                index = forceInt(record.value(fieldName))
                value = CTariff.tariffTypeNames[index] if 0<=index<len(CTariff.tariffTypeNames) else ('{%d}'% index)
            else:
                value = forceString(record.value(fieldName))
            if value:
                parts.append(fieldName+' = '+value)
        return ', '.join([part for part in parts if part])


    def addTariffToMap(self, record):
        key = self.getTariffKey(record)
        type = forceInt(record.value('tariffType'))
        if type == 2:
            self.mapTariffKeyToRecordList.setdefault(key, []).append(record)


    def log(self, str, forceLog = False,  color = None):
        if self.showLog or forceLog:
            if color:
                oldColor = self._parent.logBrowser.textColor()
                self._parent.logBrowser.setTextColor( color )
                self._parent.logBrowser.append(str)
                self._parent.logBrowser.setTextColor( oldColor )
            else:
                self._parent.logBrowser.append(str)
            self._parent.logBrowser.update()

    def getResultList(self):
        return self.resultTariffList


    def formatField(self, text):
        text = trim(text)
        text = self.reSpaces.sub(' ', text)
        return text


    def readFile(self, stream):
        headerParent = None
        QtGui.qApp.db.transaction()
        try:
            while not stream.atEnd():
                self._parent.progressBar.setValue(stream.pos())
                QtGui.qApp.processEvents()
                if self._parent.aborted:
                    raise Exception()
                line = forceString(stream.readLine())
                fields = line.split('|')
                if len(fields) < 2:
                    self.log(u'Не могу разделить строку на элементы, неверная строка или неверный разделитель', True, Qt.red)
                    raise Exception()
                if len(fields) < 4:
                    self.log(u'Формат файла не верный, количество столбцов меньше 4', True, Qt.red)
                    self.log(line, True, Qt.red)
                    raise Exception()
                if fields[0] == u''\
                    and fields[1] != u''\
                    and fields[2] == u''\
                    and fields[3] == u'':
                    if headerParent:
                        headerParent = self.parseHeader(self.formatField(fields[1]), headerParent)
                    else:
                        headerParent = self.parseHeader(self.formatField(fields[1]))
                    continue
                if fields[0] != u''\
                    and fields[1] != u''\
                    and fields[2] != u''\
                    and fields[3] != u'':
                    headerParent = None
                    self.parseLine(fields)
                else:
                    self.log(u'Строка "%s" некорректна'%line)
        except Exception as e:
            QtGui.qApp.db.rollback()
            if type(e) == CDatabaseException:
                self.log(e._message, True)
            self.log(u'Изменения отменены', True, Qt.red)
            self._parent.abort()
            return False
        else:
            QtGui.qApp.db.commit()
            self.log(u'Загрузка завершена!', True, Qt.green)
        return True


    def parseHeader(self, header, parentId = None):
        self.currentGroupId = self.headers.get((header, parentId), 0)
        if not self.currentGroupId:
            db = QtGui.qApp.db
            tableAT = db.table('ActionType')
            record = db.getRecordEx(tableAT, 'id', 'name=\'%s\' and class=3 and group_id=%i'%(header, parentId if parentId else self.mainGroupId))
            if not record:
                record = tableAT.newRecord()
                record.setValue(u'name', toVariant(header))
                record.setValue(u'class', toVariant(3))
                record.setValue(u'code', toVariant(u'-'))
                record.setValue('showInForm', toVariant(1))
                record.setValue(u'group_id', toVariant(parentId if parentId else self.mainGroupId))
                id = db.insertRecord(tableAT, record)
            else:
                id = forceInt(record.value('id'))
            self.currentGroupId = id
            self.headers[(header, parentId)] = id
        return self.currentGroupId


    def parseLine(self, fields):
        db = QtGui.qApp.db
        tableService = db.table('rbService')
        tableUnit = db.table('rbMedicalAidUnit')
        tableAT = db.table('ActionType')
        tableATS = db.table('ActionType_Service')
        tableTariff = db.table('Contract_Tariff')
        code = trim(fields[0])
        name = trim(fields[1])
        unit = trim(fields[2])
        price = forceDouble(fields[3])
        if len(fields) > 4:
            try:
                vat = forceDouble(fields[4])
            except:
                vat = None

        unitId = forceInt(db.translate(tableUnit, 'name', unit, 'id'))
        if not unitId:
            self.log(u'Неизвестный тип медицинской помощи %s'%unit, True)
            return

        serviceId = self.getId(tableService, code, name)
        if not serviceId:
            if self.addMissing:
                service = tableService.newRecord()
                service.setValue('code', toVariant(code))
                service.setValue('name', toVariant(name))
                serviceId = db.insertRecord(tableService, service)
                self.log(u'Добавлен сервис с кодом %s'%code)
            else:
                self.log(u'Сервис с кодом %s не найден, пропускаю\n'%code, True)
                return

        actionTypeId = self.getId(tableAT, code, name)
        if not actionTypeId:
            if self.addMissing:
                aType = tableAT.newRecord()
                aType.setValue('code', toVariant(code))
                aType.setValue('name', toVariant(name))
                aType.setValue('title', toVariant(name))
                aType.setValue('class', toVariant(3))
                aType.setValue('showInForm', toVariant(1))
                aType.setValue('group_id', self.currentGroupId if self.currentGroupId else self.mainGroupId)
                if self._parent.actionTypeSettings:
                    for key in self._parent.actionTypeSettings.keys():
                        aType.setValue(key, toVariant(self._parent.actionTypeSettings[key]))
                actionTypeId = db.insertRecord(tableAT, aType)
                aTypeS = tableATS.newRecord()
                aTypeS.setValue('master_id', actionTypeId)
                aTypeS.setValue('service_id', serviceId)
                db.insertRecord(tableATS, aTypeS)
                self.log(u'Добавлен тип действия с кодом %s (%s)'%(code, name))
            else:
                self.log(u'Тип действия с кодом %s не найден, пропускаю\n'%code)

        tariffList = self.mapTariffKeyToRecordList.get(serviceId, [])
        if not tariffList:
            tariff = tableTariff.newRecord()
            tariff.setValue('service_id', toVariant(serviceId))
            tariff.setValue('price', toVariant(price))
            tariff.setValue('unit_id', toVariant(unitId))
            tariff.setValue('tariffType', toVariant(CTariff.ttActionAmount))
            if vat:
                if vat > 100:
                    self.log(u'У тарифа %s процент НДС больше 100!'%code, True, Qt.red)
                else:
                    tariff.setValue('VAT', toVariant(vat))
            self.tariffRecordList.append(tariff)
            self.addTariffToMap(tariff)
            self.log(u'Добавлен новый тариф "%s", стоимость %d\n'%(name, price))
        else:
            if self.updateTariff:
                for tariff in tariffList:
                    tariff.setValue('price', toVariant(price))
                    tariff.setValue('unit_id', toVariant(unitId))
                    if vat:
                        if vat > 100:
                            self.log(u'У тарифа %s процент НДС больше 100!'%code, True, Qt.red)
                        else:
                            tariff.setValue('VAT', toVariant(vat))
                    self.log(u'Обновлен тариф "%s", стоимость %d\n'%(name, price))
            else:
                self.log(u'Найден существующий тариф "%s", пропускаем\n'%name)

    def getId(self, table, code, name):
        id = None
        cond = [table['code'].eq(code)]
        if not self.onlyCodes:
            cond.append(table['name'].eq(name))
        record = QtGui.qApp.db.getRecordEx(table, 'id', cond)
        if record:
            id = forceInt(record.value('id'))
        return id


class CImportTariffsCSV(QtGui.QDialog, Ui_ImportTariffsCSV):
    def __init__(self, fileName, tariffRecordList, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.progressBar.reset()
        self.progressBar.setValue(0)
        #self.contractId = None
        self.fileName = fileName
        self.aborted = False
        self.tariffRecordList = list(tariffRecordList)
        self.actionTypeSettings = None
        self.connect(self, SIGNAL('import()'), self.import_, Qt.QueuedConnection)
        self.connect(self, SIGNAL('rejected()'), self.abort)
        if fileName:
            self.edtFileName.setText(fileName)
            self.btnImport.setEnabled(True)


    def abort(self):
        self.aborted = True


    def import_(self):
        self.aborted = False
        self.btnAbort.setEnabled(True)
        success, result = QtGui.qApp.call(self, self.doImport)
        if self.aborted or not success:
            self.progressBar.setText(u'Прервано')
        self.btnAbort.setEnabled(False)


    @pyqtSignature('')
    def on_btnSelectFile_clicked(self):
        self.fileName = QtGui.QFileDialog.getOpenFileName(
            self, u'Укажите файл с данными', self.edtFileName.text(), u'Файлы CSV (*.csv)')
        if self.fileName:
            self.edtFileName.setText(self.fileName)
            self.btnImport.setEnabled(True)


    @pyqtSignature('')
    def on_btnClose_clicked(self):
        self.accept()


    @pyqtSignature('')
    def on_btnAbort_clicked(self):
        self.abort()


    @pyqtSignature('')
    def on_btnImport_clicked(self):
        self.emit(SIGNAL('import()'))


    @pyqtSignature('')
    def on_btnSettings_clicked(self):
        dlg = CGroupActionTypeEditor()
        if self.actionTypeSettings:
            dlg.loadSettings(self.actionTypeSettings)
        if dlg.exec_():
            self.actionTypeSettings = dlg.getSettings()


    @pyqtSignature('QString')
    def on_edtFileName_textChanged(self):
        self.fileName = self.edtFileName.text()
        self.btnImport.setEnabled(self.fileName != '')


    def doImport(self):
        db = QtGui.qApp.db
        tableAT = db.table('ActionType')
        cond = [tableAT['name'].eq(u'Услуги'),
                    tableAT['class'].eq(3)]
        record = db.getRecordEx(tableAT, 'id', cond)
        if record:
            mainGroupId = forceInt(record.value(0))
        else:
            QtGui.QMessageBox.warning(self, u'Импорт тарифов для договора',
                                      u'не найдена группа "Услуги" в классе "Прочие мероприятия"')
            return
        fileName = self.edtFileName.text()
        if not fileName:
            return
        inFile = QFile(fileName)
        if not inFile.open(QFile.ReadOnly | QFile.Text):
            QtGui.QMessageBox.warning(self, u'Импорт тарифов для договора',
                                      QString(u'Не могу открыть файл для чтения %1:\n%2.')
                                      .arg(fileName)
                                      .arg(inFile.errorString()))
            return

        self.progressBar.reset()
        self.progressBar.setValue(0)
        self.progressBar.setFormat(u'%v байт')
        self.lblStatus.setText('')
        self.progressBar.setMaximum(max(inFile.size(), 1))
        myCsvReader = CCsvReader(self, mainGroupId, self.tariffRecordList,
                                               self.chkFullLog.isChecked(),
                                               self.chkUpdateTariff.isChecked(),  self.chkOnlyCodes.isChecked(), self.chkAddServicesAndAT.isChecked())

        self.btnImport.setEnabled(False)
        stream = QTextStream(inFile)
        if (myCsvReader.readFile(stream)):
            self.progressBar.setText(u'Готово')
        else:
            self.progressBar.setText(u'Прервано')
        self.edtFileName.setEnabled(False)
        self.btnSelectFile.setEnabled(False)


if __name__ == '__main__':
    from s11main import CS11mainApp
    QtGui.qApp = CS11mainApp(None, False, None, None, None)
    QtGui.qApp.openDatabase()
#    def ImportTariffsXML(widget, tariffRecordList, expenseRecordList):
#    appPrefs = QtGui.qApp.preferences.appPrefs
#
#    fileName = forceString(appPrefs.get('ImportTariffsXMLFileName', ''))
#    fullLog = forceBool(appPrefs.get('ImportTariffsXMLFullLog', ''))
#    updateTariff = forceBool(appPrefs.get('ImportTariffsXMLUpdatePrices', ''))
#    onlyCodes = forceBool(appPrefs.get('ImportTariffsXMLOnlyCodes', ''))
#    dlg = CImportTariffsCSV(fileName, tariffRecordList, expenseRecordList,  widget)
    dlg = CImportTariffsCSV('', 135, [], [],  None)
#    dlg.chkFullLog.setChecked(fullLog)
#    dlg.chkUpdateTariff.setChecked(updateTariff)
#    dlg.chkOnlyCodes.setChecked(onlyCodes)
    dlg.exec_()
    print 'qq'
#    appPrefs['ImportTariffsXMLFileName'] = toVariant(dlg.fileName)
#    appPrefs['ImportTariffsXMLFullLog'] = toVariant(dlg.chkFullLog.isChecked())
#    appPrefs['ImportTariffsXMLUpdatePrices'] = toVariant(dlg.chkUpdateTariff.isChecked())
#    appPrefs['ImportTariffsXMLOnlyCodes'] = toVariant(dlg.chkOnlyCodes.isChecked())
#    return dlg.tariffRecordList,  dlg.expenseRecordList
