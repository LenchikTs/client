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

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QFile, QString, QXmlStreamReader, pyqtSignature, SIGNAL

from library.crbcombobox import CRBModelDataCache
from library.Utils      import anyToUnicode, exceptionToUnicode, forceBool, forceRef, forceString, toVariant, variantEq

from Exchange.Utils import tbl

from Exchange.ExportRbService import rbServiceFields, rbServiceRefFields, rbServiceProfileRefFields, rbServiceRefTables, rbServiceProfileRefTable
from Exchange.Ui_ImportRbService import Ui_ImportRbService


def ImportRbService(parent):
    fileName = forceString(QtGui.qApp.preferences.appPrefs.get('ImportRbServiceFileName', ''))
    fullLog = forceBool(QtGui.qApp.preferences.appPrefs.get('ImportRbServiceFullLog', ''))
    dlg = CImportRbService(fileName,  parent)
    dlg.chkFullLog.setChecked(fullLog)
    dlg.chkCompareOnlyByCode.setChecked(forceBool(QtGui.qApp.preferences.appPrefs.get('ImportRbServiceCompareOnlyByCode', False)))
    dlg.exec_()
    QtGui.qApp.preferences.appPrefs['ImportRbServiceFileName'] = toVariant(dlg.fileName)
    QtGui.qApp.preferences.appPrefs['ImportRbServiceFullLog'] = toVariant(dlg.chkFullLog.isChecked())
    QtGui.qApp.preferences.appPrefs['ImportRbServiceCompareOnlyByCode'] =\
        toVariant(dlg.chkCompareOnlyByCode.isChecked())


class CMyXmlStreamReader(QXmlStreamReader):
    def __init__(self,  parent,  compareOnlyByCode):
        QXmlStreamReader.__init__(self)
        self.parent = parent
        self.db=QtGui.qApp.db
        self.table = tbl('rbService')
        self.nadded = 0
        self.ncoincident = 0
        self.nprocessed = 0
        self.nupdated = 0
        self.mapServiceKeyToId = {}
        self.showLog = self.parent.chkFullLog.isChecked()
        self.recursionLevel = 0
        self.compareOnlyByCode = compareOnlyByCode
        self.skipAll = False
        self.addAll = False
        self.updateAll = False
        self.refValueCache = {}
        for field, tableName in zip(rbServiceRefFields+rbServiceProfileRefFields, rbServiceRefTables+rbServiceProfileRefTable):
            self.refValueCache[field] = CRBModelDataCache.getData(tableName, True)


    def raiseError(self,  str):
        QXmlStreamReader.raiseError(self, u'[%d:%d] %s' % (self.lineNumber(), self.columnNumber(), str))


    def readNext(self):
        QXmlStreamReader.readNext(self)
        self.parent.progressBar.setValue(self.device().pos())


    def log(self, str,  forceLog = False):
        if self.showLog or forceLog:
            self.parent.logBrowser.append(str)
            self.parent.logBrowser.update()


    def readFile(self, device):
        self.setDevice(device)
        xmlVersion = '1.00'

        try:
            while (not self.atEnd()):
                self.readNext()

                if self.isStartElement():
                    if self.name() == 'RbServiceExport':
                        if self.attributes().value('version') == xmlVersion:
                            self.readData()
                        else:
                            self.raiseError(u'Версия формата "%s" не поддерживается. Должна быть "%s"' \
                                % (self.attributes().value('version').toString(), xmlVersion))
                    else:
                        self.raiseError(u'Неверный формат экспорта данных.')

                if self.hasError() or self.parent.aborted:
                    return False

        except IOError, e:
            QtGui.qApp.logCurrentException()
            msg=''
            if hasattr(e, 'filename'):
                msg = u'%s:\n[Errno %s] %s' % (e.filename, e.errno, anyToUnicode(e.strerror))
            else:
                msg = u'[Errno %s] %s' % (e.errno, anyToUnicode(e.strerror))
            QtGui.QMessageBox.critical (self.parent,
                u'Произошла ошибка ввода-вывода', msg, QtGui.QMessageBox.Close)
            self.log(u'! Ошибка ввода-вывода: %s' % msg,  True)
            return False
        except Exception, e:
            QtGui.qApp.logCurrentException()
            QtGui.QMessageBox.critical (self.parent,
                u'Произошла ошибка', exceptionToUnicode(e), QtGui.QMessageBox.Close)
            self.log(u'! Ошибка: %s' % exceptionToUnicode(e),  True)
            return False


        return not (self.hasError() or self.parent.aborted)


    def readData(self):
        assert self.isStartElement() and self.name() == "RbServiceExport"

        while (not self.atEnd()):
            self.readNext()

            if self.isEndElement():
                break

            if self.isStartElement():
                if (self.name() == "ServiceElement"):
                    self.readThesaurusElement()
                else:
                    self.readUnknownElement()

            if self.hasError() or self.parent.aborted:
                break


    def getServiceDifference(self, oldRecordId, newRecordDict):
        parts = []
        oldRecord = self.db.getRecord(self.table, '*', oldRecordId)

        for fieldName in rbServiceFields:
                oldValue = oldRecord.value(fieldName)
                newValue = toVariant(newRecordDict.get(fieldName))
                if not variantEq(oldValue, newValue):
                    parts.append(u'%s было %s стало %s' % (fieldName, forceString(oldValue), forceString(newValue)))

        return ', '.join(parts)


    def addService(self, newRecordDict):
        record = self.table.newRecord()

        for x in rbServiceFields+rbServiceRefFields:
            value = newRecordDict.get(x)

            if value:
                record.setValue(x,  toVariant(value))

        id = self.db.insertRecord(self.table, record)
        self.mapServiceKeyToId[(newRecordDict.get('code'), newRecordDict.get('name'))] = id

        tableProfile = self.db.table('rbService_Profile')
        for profile in newRecordDict.get('Profiles', []):
            recordProfile = tableProfile.newRecord()
            recordProfile.setValue('master_id', toVariant(id))
            for fieldName in profile.keys():
                recordProfile.setValue(fieldName, toVariant(profile[fieldName]))
            self.db.insertRecord(tableProfile, recordProfile)

        self.nadded += 1


    def updateService(self, id,  newRecordDict):
        record = self.db.getRecord(self.table, '*', id)

        for x in rbServiceFields+rbServiceRefFields:
            value = newRecordDict.get(x)

            if value:
                record.setValue(x,  toVariant(value))

        id = self.db.updateRecord(self.table, record)

        #self.db.query('delete from rbService_Profile where master_id = %i'%id)
        tableProfile = self.db.table('rbService_Profile')
        for profile in newRecordDict.get('Profiles', []):
            recordProfile = tableProfile.newRecord()
            recordProfile.setValue('master_id', toVariant(id))
            for fieldName in profile.keys():
                recordProfile.setValue(fieldName, toVariant(profile[fieldName]))
            self.db.insertRecord(tableProfile, recordProfile)

        self.nupdated += 1


    def readThesaurusElement(self):
        assert self.isStartElement() and self.name() == "ServiceElement"

#        groupId = None
        element = {}

        for x in rbServiceFields:
            element[x] = forceString(self.attributes().value(x).toString())

        while not self.atEnd():
            self.readNext()

            QtGui.qApp.processEvents()
            if self.isEndElement():
                break
            if self.isStartElement():
                name = forceString(self.name().toString())
                if (name == 'medicalAidProfile'):
                    element[name+'_id'] = self.readAid('Profile')
                elif (name == 'medicalAidKind'):
                   element[name+'_id'] = self.readAid('Kind')
                elif (name == 'medicalAidType'):
                   element[name+'_id'] = self.readAid('Type')
                elif (name == 'Profile'):
                   element.setdefault('Profiles', []).append(self.readProfile())
                else:
                    self.readUnknownElement()



        name = element['name']
        code = element['code']
        self.log(u'Элемент: %s (%s)' %(name, code))
        id = self.lookupServiceElementByCode(code) if self.compareOnlyByCode \
            else self.lookupServiceElement(code, name)

        if self.hasError() or self.parent.aborted:
            return None

        if id and not (self.skipAll or self.updateAll or self.addAll):
            diff = self.getServiceDifference(id, element)

#            oldName = forceString(self.db.translate('rbService', 'id', id, 'name'))
            answer = QtGui.QMessageBox.question(self.parent,
                        u'Внимание!',
                        u'Услуга с кодом "%s" уже есть в БД.<br>Отличия:%s<br>'\
                        u'Да - добавить новую запись, Нет - обновить,<br>'\
                        u'Прервать - не обрабатывать текущую запись' % (code, diff),
                        QtGui.QMessageBox.Yes|QtGui.QMessageBox.YesToAll|QtGui.QMessageBox.No|
                        QtGui.QMessageBox.NoToAll|QtGui.QMessageBox.Abort,
                    QtGui.QMessageBox.Abort)
            if answer == QtGui.QMessageBox.YesToAll:
                self.addAll = True
            elif answer == QtGui.QMessageBox.NoToAll:
                self.updateAll = True
            elif answer == QtGui.QMessageBox.No:
                self.updateService(id,  element)
            elif answer == QtGui.QMessageBox.Yes:
                self.addService(element)

        if id and self.addAll:
            self.log(u'% Добавляем новую запись, хотя в БД похожая уже есть.')
            self.addService(element)
        elif id and self.updateAll:
            self.log(u'* Обновляем')
            self.updateService(id, element)
        elif id:
            self.log(u'%% Найдена совпадающая запись (id=%d), пропускаем' % id)
            self.ncoincident += 1
        else:
            self.log(u'% Сходные записи не обнаружены. Добавляем')
            # новая запись, добавляем само действие и все его свойства + ед.изм.
            self.addService(element)

        self.nprocessed += 1
        self.parent.statusLabel.setText(
                u'импорт типов действий: %d добавлено; %d обновлено; %d совпадений; %d обработано' % (self.nadded,
                                                                                                      self.nupdated,  self.ncoincident,  self.nprocessed))

        return id


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


    def readAid(self, colName):
        assert self.isStartElement() and self.name() == 'medicalAid'+colName
        code, name = self.readRefElement()
        return self.lookupAid(colName, code, name)


    def readProfile(self):
        assert self.isStartElement() and self.name() == 'Profile'
        result = {}
        result['sex'] = forceString(self.attributes().value('sex').toString())
        result['age'] = forceString(self.attributes().value('age').toString())
        result['mkbRegExp'] = forceString(self.attributes().value('mkbRegExp').toString())

        result['speciality_id'] = self.lookupIdByCodeName(forceString(self.attributes().value('specCode').toString()),
                            forceString(self.attributes().value('specName').toString()),
                            'speciality_id')

        result['medicalAidProfile_id'] = self.lookupIdByCodeName(forceString(self.attributes().value('profCode').toString()),
                            forceString(self.attributes().value('profName').toString()),
                            'medicalAidProfile_id')

        result['medicalAidType_id'] = self.lookupIdByCodeName(forceString(self.attributes().value('typeCode').toString()),
                            forceString(self.attributes().value('typeName').toString()),
                            'medicalAidType_id')

        result['medicalAidKind_id'] = self.lookupIdByCodeName(forceString(self.attributes().value('kindCode').toString()),
                            forceString(self.attributes().value('kindName').toString()),
                            'medicalAidKind_id')

        while not self.atEnd():
            self.readNext()
            QtGui.qApp.processEvents()
            if self.isEndElement():
                break
            if self.isStartElement():
                self.readUnknownElement()

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
            if self.hasError() or self.parent.aborted:
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


    def lookupAid(self, colName, code, name):
        if code and name:
            id = self.lookupIdByCodeName(code, name, 'medicalAid'+colName+'_id')
            if not id:
                self.log(u'Тип помощи (%s) "%s" в таблице %s не найден.' % (code, name, 'medicalAid'+colName),  True)
            return id
        return None


    def lookupServiceElement(self, code, name):
        key = (code, name)
        id = self.mapServiceKeyToId.get(key,  None)

        if id:
            return id

        cond = []
        cond.append(self.table['code'].eq(toVariant(code)))
        cond.append(self.table['name'].eq(toVariant(name)))

        record = self.db.getRecordEx(self.table, ['id'], where=cond)
        if record:
            id = forceRef(record.value('id'))
            self.mapServiceKeyToId[key] = id
            return id

        return None


    def lookupServiceElementByCode(self, code):
        key = (code)
        id = self.mapServiceKeyToId.get(key,  None)

        if not id:
            record = self.db.getRecordEx(self.table, ['id'],
                where=[self.table['code'].eq(toVariant(code))])

            if record:
                id = forceRef(record.value('id'))
                self.mapServiceKeyToId[key] = id

        return id


class CImportRbService(QtGui.QDialog, Ui_ImportRbService):
    def __init__(self, fileName,  parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.progressBar.reset()
        self.progressBar.setValue(0)
        self.fileName = ''
        self.aborted = False
        self.connect(self, SIGNAL('import()'), self.import_, Qt.QueuedConnection)
        self.connect(self, SIGNAL('rejected()'), self.abort)
        if fileName != '':
            self.edtFileName.setText(fileName)
            self.btnImport.setEnabled(True)
            self.fileName = fileName


    def abort(self):
        self.aborted = True


    def import_(self):
        self.aborted = False
        self.btnAbort.setEnabled(True)
        success,  result = QtGui.qApp.call(self, self.doImport)

        if self.aborted or not success:
            self.progressBar.setText(u'Прервано')

        self.btnAbort.setEnabled(False)


    @pyqtSignature('')
    def on_btnSelectFile_clicked(self):
        self.fileName = QtGui.QFileDialog.getOpenFileName(
            self, u'Укажите файл с данными', self.edtFileName.text(), u'Файлы XML (*.xml)')
        if self.fileName != '':
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

        if fileName.isEmpty():
            return

        inFile = QFile(fileName)
        if not inFile.open(QFile.ReadOnly | QFile.Text):
            QtGui.QMessageBox.warning(self, u'Импорт справочника "Услуги"',
                                      QString(u'Не могу открыть файл для чтения %1:\n%2.')
                                      .arg(fileName)
                                      .arg(inFile.errorString()))
        else:
            self.progressBar.reset()
            self.progressBar.setValue(0)
            self.progressBar.setFormat(u'%v байт')
            self.statusLabel.setText('')
            self.progressBar.setMaximum(max(inFile.size(), 1))
            myXmlStreamReader = CMyXmlStreamReader(self, self.chkCompareOnlyByCode.isChecked())
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
