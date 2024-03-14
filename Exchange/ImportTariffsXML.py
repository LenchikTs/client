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
u"""Импорт тарифа из XML"""
from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QFile, QString, QXmlStreamReader, pyqtSignature, SIGNAL

from library.crbcombobox import CRBModelDataCache
from library.Utils       import anyToUnicode, forceBool, forceDouble, forceInt, forceRef, forceString, forceStringEx, toVariant, variantEq

from Exchange.ExportTariffsXML import tariffSimpleFields, tariffRefFields, tariffRefTableNames, tariffKeyFields, exportVersion


from Exchange.Ui_ImportTariffsXML import Ui_ImportTariffsXML


def ImportTariffsXML(widget, tariffRecordList, expenseRecordList):
    appPrefs = QtGui.qApp.preferences.appPrefs

    fileName = forceString(appPrefs.get('ImportTariffsXMLFileName', ''))
    fullLog = forceBool(appPrefs.get('ImportTariffsXMLFullLog', ''))
    updateTariff = forceBool(appPrefs.get('ImportTariffsXMLUpdatePrices', ''))
    onlyCodes = forceBool(appPrefs.get('ImportTariffsXMLOnlyCodes', ''))
    dlg = CImportTariffsXML(fileName, tariffRecordList, expenseRecordList,  widget)
    dlg.chkFullLog.setChecked(fullLog)
    dlg.chkUpdateTariff.setChecked(updateTariff)
    dlg.chkOnlyCodes.setChecked(onlyCodes)
    dlg.exec_()
    appPrefs['ImportTariffsXMLFileName'] = toVariant(dlg.fileName)
    appPrefs['ImportTariffsXMLFullLog'] = toVariant(dlg.chkFullLog.isChecked())
    appPrefs['ImportTariffsXMLUpdatePrices'] = toVariant(dlg.chkUpdateTariff.isChecked())
    appPrefs['ImportTariffsXMLOnlyCodes'] = toVariant(dlg.chkOnlyCodes.isChecked())
    return dlg.tariffRecordList,  dlg.expenseRecordList


def getTariffDifference(oldRecord, oldExpenses, newRecord, newExpenses):
    parts = []

    for fieldName in tariffSimpleFields+tariffRefFields:
        if fieldName not in tariffKeyFields:
            oldValue = oldRecord.value(fieldName)
            newValue = newRecord.value(fieldName)
            if not variantEq(oldValue, newValue):
                parts.append(u'%s было %s стало %s' % (fieldName, forceString(oldValue), forceString(newValue)))

    # проверяем изменения в затратах
    for oldX in  oldExpenses:
        for newX in newExpenses:
            if (forceRef(newX.value('rbTable_id')) == forceRef(oldX.value('rbTable_id'))) and\
                    (not variantEq(newX.value('percent'), oldX.value('percent'))):
                parts.append(u'затрата id=%d было %.2f%% стало %.2f%%' % (
                    forceInt(newX.value('rbTable_id')),
                    forceDouble(oldX.value('percent')),
                    forceDouble(newX.value('percent'))))

    # проверяем появление удалённых затрат
    for oldX in  oldExpenses:
        flag = False

        for newX in newExpenses:
            if (forceRef(newX.value('rbTable_id')) == forceRef(oldX.value('rbTable_id'))):
                flag = True
                break

        if not flag:
                parts.append(u'удалена затрата id=%d %.2f%%' % (
                    forceInt(oldX.value('rbTable_id')),
                    forceDouble(oldX.value('percent'))))

    # проверяем появление новых затрат
    for newX in newExpenses:
        flag = False

        for oldX in  oldExpenses:
            if (forceRef(newX.value('rbTable_id')) == forceRef(oldX.value('rbTable_id'))):
                flag = True
                break

        if not flag:
                parts.append(u'новая затрата id=%d %.2f%%' % (
                    forceInt(newX.value('rbTable_id')),
                    forceDouble(newX.value('percent'))))

    return ', '.join(parts)


def copyTariff(oldRecord, newRecord):
    for fieldName in tariffSimpleFields+tariffRefFields:
        if fieldName not in tariffKeyFields:
            oldRecord.setValue(fieldName, newRecord.value(fieldName))


class CMyXmlStreamReader(QXmlStreamReader):
    def __init__(self, parent, tariffRecordList, expenseRecordList, showLog, updateTariff,  onlyCodes):
        QXmlStreamReader.__init__(self)
        self._parent = parent
        self.table = QtGui.qApp.db.table('Contract_Tariff')
        self.tableExpenses = QtGui.qApp.db.table('Contract_CompositionExpense')

        self.tariffRecordList = tariffRecordList
        self.expenseRecordList = expenseRecordList
        self.showLog = showLog
        self.updateTariff = updateTariff
        self.onlyCodes = onlyCodes

        self.mapTariffKeyToRecordList = {}
        for record in self.tariffRecordList:
            self.addTariffToMap(record)

        self.refValueCache = {}
        for field, tableName in zip(tariffRefFields, tariffRefTableNames):
            self.refValueCache[field] = CRBModelDataCache.getData(tableName, True)

        self.expenseTypeCache = CRBModelDataCache.getData('rbExpenseServiceItem', True)

        self.skip = False
        self.nadded = 0
        self.ncoincident = 0
        self.nprocessed = 0
        self.nupdated = 0
        self.nskipped = 0


    def getTariffKey(self, record):
        return tuple([ forceStringEx(record.value(fieldName)) if not record.value(fieldName).isNull() else None for fieldName in tariffKeyFields ])


    def getTariffDescr(self, record):
        from Accounting.Tariff import CTariff

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
        self.mapTariffKeyToRecordList.setdefault(key, []).append(record)


    def getTariffDifference(self, oldRecord, newRecord, newExpenses):
        return getTariffDifference(oldRecord,
                                   self.expenseRecordList[self.tariffRecordList.index(oldRecord)],
                                   newRecord, newExpenses)


    def raiseError(self, str):
        QXmlStreamReader.raiseError(self, u'[%d:%d] %s' % (self.lineNumber(), self.columnNumber(), str))


    def readNext(self):
        QXmlStreamReader.readNext(self)
        self._parent.progressBar.setValue(self.device().pos())


    def log(self, str, forceLog = False,  red = None):
        if self.showLog or forceLog:
            if red:
                color = self._parent.logBrowser.textColor()
                self._parent.logBrowser.setTextColor( Qt.red )
                self._parent.logBrowser.append(str)
                self._parent.logBrowser.setTextColor( color )
            else:
                self._parent.logBrowser.append(str)
            self._parent.logBrowser.update()

    def readFile(self, device):
        self.setDevice(device)
        try:
            while (not self.atEnd()):
                self.readNext()

                if self.isStartElement():
                    if self.name() == 'TariffExport':
                        if self.attributes().value('version') == exportVersion:
                            self.readData()
                        else:
                            self.raiseError(u'Версия формата "%s" не поддерживается. Должна быть "%s"' \
                                % (self.attributes().value('version').toString(), exportVersion))
                    else:
                        self.raiseError(u'Неверный формат экспорта данных.')

                if self.hasError() or self._parent.aborted:
                    return False

        except IOError, e:
            QtGui.qApp.logCurrentException()
            msg=''
            if hasattr(e, 'filename'):
                msg = u'%s:\n[Errno %s] %s' % (e.filename, e.errno, anyToUnicode(e.strerror))
            else:
                msg = u'[Errno %s] %s' % (e.errno, anyToUnicode(e.strerror))
            QtGui.QMessageBox.critical (self._parent,
                u'Произошла ошибка ввода-вывода', msg, QtGui.QMessageBox.Close)
            self.log(u'! Ошибка ввода-вывода: %s' % msg, True)
            return False
        except Exception, e:
            QtGui.qApp.logCurrentException()
            QtGui.QMessageBox.critical (self._parent,
                u'Произошла ошибка', unicode(e), QtGui.QMessageBox.Close)
            self.log(u'! Ошибка: %s' % unicode(e), True)
            return False
        return not (self.hasError() or self._parent.aborted)


    def readData(self):
        assert self.isStartElement() and self.name() == 'TariffExport'
        while (not self.atEnd()):
            self.readNext()
            if self.isEndElement():
                break
            if self.isStartElement():
                if (self.name() == 'TariffElement'):
                    self.readTariffElement()
                else:
                    self.readUnknownElement()
            if self.hasError() or self._parent.aborted:
                break


    def readTariffElement(self):
        assert self.isStartElement() and self.name() == 'TariffElement'
        newTariffRecord = self.table.newRecord()
        newExpenses = []

        for fieldName in tariffSimpleFields:
            value = toVariant(self.attributes().value(fieldName).toString())
            value.convert(newTariffRecord.field(fieldName).type())
            newTariffRecord.setValue(fieldName, value)

        while not self.atEnd():
            self.readNext()
            QtGui.qApp.processEvents()
            if self.isEndElement():
                break
            if self.isStartElement():
                name = self.name().toString()
                if (name == 'eventType'):
                    newTariffRecord.setValue(name+'_id', toVariant(self.readEventType()))
                elif (name == 'service'):
                    newTariffRecord.setValue(name+'_id', toVariant(self.readService()))
                elif (name == 'unit'):
                    newTariffRecord.setValue(name+'_id', toVariant(self.readUnit()))
                elif (name == 'tariffCategory'):
                    newTariffRecord.setValue(name+'_id', toVariant(self.readTariffCategory()))
                elif (name == 'expense'):
                    expenseRec = self.readTariffExpense()

                    if expenseRec:
                        newExpenses.append(expenseRec)
                elif name == 'result':
                    newTariffRecord.setValue(name+'_id', toVariant(self.readResult()))
                else:
                    self.readUnknownElement()

        self.log(u'Тариф: %s' % self.getTariffDescr(newTariffRecord))

        if self.skip:
            self.log(u'Информация по тарифу не полная. Пропускаем.',  True,  True)
            self.nskipped += 1
            self.skip = False
        else:

            if self.hasError() or self._parent.aborted:
                return None

            key = self.getTariffKey(newTariffRecord)
            recordList = self.mapTariffKeyToRecordList.get(key, None)
            if recordList:
                if self.updateTariff:
                    for record in recordList:
                        diff = self.getTariffDifference(record, newTariffRecord, newExpenses)
                        if diff:
                            self.log(u'* Существующий тариф %s отличается и будет обновлён' % self.getTariffDescr(record),  True)
                            self.log(u': Различия: %s' % diff)
                            copyTariff(record, newTariffRecord)
                            self.expenseRecordList[self.tariffRecordList.index(record)] = newExpenses
                            self.nupdated += 1
                        else:
                            self.log(u'* Изменений не обнаружено')
                else:
                    self.log(u'%% Найдена совпадающая запись, пропускаем')
                    self.ncoincident += 1
            else:
                self.log(u'% Сходные записи не обнаружены, добавляем')
                self.tariffRecordList.append(newTariffRecord)
                self.addTariffToMap(newTariffRecord)
                self.expenseRecordList.append(newExpenses)
                self.nadded += 1

        self.nprocessed += 1
        self._parent.lblStatus.setText(
                u'импорт тарифов: %d добавлено; %d обновлено; %d совпадений; %d неполных; %d обработано;' % (self.nadded,
                self.nupdated, self.ncoincident, self.nskipped, self.nprocessed))


    def readRefElement(self):
        code = forceString(self.attributes().value('code').toString())
        name = forceString(self.attributes().value('name').toString())
        while not self.atEnd():
            self.readNext()
            QtGui.qApp.processEvents()
            if self.isEndElement():
                break
            if self.isStartElement():
                self.readUnknownElement()
        return code, name


    def readEventType(self):
        assert self.isStartElement() and self.name() == 'eventType'
        code, name = self.readRefElement()
        if code or name:
            self.log(u'Тип события (%s) "%s"'%(code, name))
        return self.lookupEventType(code, name)


    def readUnit(self):
        assert self.isStartElement() and self.name() == 'unit'
        code, name = self.readRefElement()
        if code or name:
            self.log(u'Единица измерения (%s) "%s"'%(code, name))
        return self.lookupUnit(code, name)



    def readService(self):
        assert self.isStartElement() and self.name() == 'service'
        code, name = self.readRefElement()
        if code or name:
            self.log(u'Услуга (%s) "%s"'%(code, name))
        return self.lookupService(code, name)


    def readTariffCategory(self):
        assert self.isStartElement() and self.name() == 'tariffCategory'
        code, name = self.readRefElement()
        if code or name:
            self.log(u'Тарифная категория (%s) "%s"'%(code, name))
        return self.lookupTariffCategory(code, name)


    def readResult(self):
        assert self.isStartElement() and self.name() == 'result'
        code, name = self.readRefElement()
        if code or name:
            self.log(u'Результат (%s) "%s"'%(code, name))
        return self.lookupResult(code, name)


    def readTariffExpense(self):
        assert self.isStartElement() and self.name() == 'expense'
        result = None
        code = forceString(self.attributes().value('code').toString())
        string = self.attributes().value('percent').toString()
        sum = self.attributes().value('sum').toString()
        percent = forceDouble(string) if string else 0.0
        id = self.expenseTypeCache.getId(self.expenseTypeCache.getIndexByCode(code))

        while not self.atEnd():
            self.readNext()
            QtGui.qApp.processEvents()
            if self.isEndElement():
                break
            if self.isStartElement():
                self.readUnknownElement()

        if id:
            self.log(u'Затрата (%s) "%.2f"'%(code, percent))
            result = self.tableExpenses.newRecord()
            result.setValue('rbTable_id',  toVariant(id))
            result.setValue('percent', toVariant(percent))
            result.setValue('sum', toVariant(sum))

        return result


    def readUnknownElement(self):
        assert self.isStartElement()
        self.log(u'Неизвестный элемент: '+self.name().toString())
        while (not self.atEnd()):
            self.readNext()
            if (self.isEndElement()):
                break
            if (self.isStartElement()):
                self.readUnknownElement()
            if self.hasError() or self._parent.aborted:
                break


    def lookupIdByCodeName(self, code, name, fieldName,  searchByName = False):
        cache = self.refValueCache[fieldName]
        index = cache.getIndexByCode(code)
        if index>=0 and ( searchByName or cache.getName(index) == name ):
            return cache.getId(index)
        index = cache.getIndexByName(name)
        if index>=0 and cache.getCode(index) == code:
            return cache.getId(index)
        return None


    def lookupUnit(self, code, name):
        if code and name:
            return self.lookupIdByCodeName(code, name, 'unit_id') or self.addUnit(code, name)
        return None


    def addUnit(self, code, name):
        db = QtGui.qApp.db
        table = db.table('rbMedicalAidUnit')
        record = table.newRecord()
        record.setValue('code', toVariant(code))
        record.setValue('name', toVariant(name))
        id = db.insertRecord(table, record)
        cache = self.refValueCache['unit_id']
        cache.addItem(id, code, name)
        self.log(u'Ед.изм. (%s) "%s" не найдена, добавлена. (id=%d)' % (code, name, id),  True)
        return id


    def lookupTariffCategory(self, code, name):
        if code and name:
            return self.lookupIdByCodeName(code, name, 'tariffCategory_id') or self.addTariffCatergory(code, name)
        return None


    def addTariffCatergory(self, code, name):
        db = QtGui.qApp.db
        table = db.table('rbTariffCategory')
        record = self.table.newRecord()
        record.setValue('code', toVariant(code))
        record.setValue('name', toVariant(name))
        id = db.insertRecord(table, record)
        cache = self.refValueCache['tariffCategory_id']
        cache.addItem(id, code, name)
        self.log(u'Тарифная категория (%s) "%s" не найдена, добавлена. (id=%d)' % (code, name, id),  True)
        return id


    def lookupService(self, code, name):
        if code and name:
            id = self.lookupIdByCodeName(code, name, 'service_id', self.onlyCodes)
            if not id:
                self.log(u'Услуга (%s) "%s" не найдена.' % (code, name),  True)
                self.skip = True
            return id
        return None


    def lookupEventType(self, code, name):
        if code and name:
            id = self.lookupIdByCodeName(code, name, 'eventType_id')
            if not id:
                self.log(u'Тип события (%s) "%s" не найден.' % (code, name),  True)
                self.skip = True
            return id
        return None


    def lookupResult(self, code, name):
        if code and name:
            id = self.lookupIdByCodeName(code, name, 'result_id')

            if not id:
                self.log(u'Результат события (%s) "%s" не найден.' % (code, name),  True)
                self.skip = True
            return id
        return None


class CImportTariffsXML(QtGui.QDialog, Ui_ImportTariffsXML):
    def __init__(self, fileName, tariffRecordList, expenseRecordList, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.progressBar.reset()
        self.progressBar.setValue(0)
        self.fileName = fileName
        self.aborted = False
        self.tariffRecordList = list(tariffRecordList)
        self.expenseRecordList = list(expenseRecordList)
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
            self, u'Укажите файл с данными', self.edtFileName.text(), u'Файлы XML (*.xml)')
        if self.fileName:
            self.edtFileName.setText(self.fileName)
            self.btnImport.setEnabled(True)


    @pyqtSignature('')
    def on_btnClose_clicked(self):
        self.close()


    @pyqtSignature('')
    def on_btnAbort_clicked(self):
        self.abort()


    @pyqtSignature('')
    def on_btnImport_clicked(self):
        self.emit(SIGNAL('import()'))


    @pyqtSignature('QString')
    def on_edtFileName_textChanged(self):
        self.fileName = self.edtFileName.text()
        self.btnImport.setEnabled(self.fileName != '')


    def doImport(self):
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
        myXmlStreamReader = CMyXmlStreamReader(self, self.tariffRecordList,
                                               self.expenseRecordList, self.chkFullLog.isChecked(),
                                               self.chkUpdateTariff.isChecked(),  self.chkOnlyCodes.isChecked())

        self.btnImport.setEnabled(False)
        if (myXmlStreamReader.readFile(inFile)):
            self.progressBar.setText(u'Готово')
        else:
            self.progressBar.setText(u'Прервано')
            if self.aborted:
                self.logBrowser.append(u'! Прервано пользователем.')
            else:
                self.logBrowser.append(u'! Ошибка: файл %s, %s' % (fileName, myXmlStreamReader.errorString()))
        self.edtFileName.setEnabled(False)
        self.btnSelectFile.setEnabled(False)
