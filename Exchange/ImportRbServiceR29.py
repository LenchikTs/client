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
# Для загрузки необходима таблица
# CREATE TABLE IF NOT EXISTS `rbPacientGroup_r29` (
#   `id` int(11) NOT NULL,
#   `code` varchar(20) NOT NULL,
#   `name` varchar(255) NOT NULL,
#   `sex` tinyint(4) NOT NULL,
#   `age` varchar(9) NOT NULL,
#   `comment` varchar(256) NOT NULL,
#   PRIMARY KEY (`id`)
# ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='Пациенто-группы для Арх.обл';

import re
from PyQt4 import QtGui
from PyQt4.QtCore import Qt, pyqtSignature, SIGNAL, QDate, QFile, QString, QXmlStreamReader

from library.ItemsListDialog import CItemEditorBaseDialog
from library.Utils      import anyToUnicode, forceBool, forceDouble, forceInt, forceRef, forceString, toVariant, variantEq

from library.crbcombobox import CRBComboBox
from library.crbcombobox import CRBModelDataCache
from library.InDocTable  import CInDocTableModel, CBoolInDocTableCol, CCodeNameInDocTableCol, CRBInDocTableCol

from ExportRbService import  rbServiceRefFields, rbServiceProfileRefFields, rbServiceRefTables, rbServiceProfileRefTable

from Ui_ImportRbServiceR29_1 import Ui_ImportRbServiceR29_1
from Ui_ImportRbServiceR29_2 import Ui_ImportRbServiceR29_2

def ImportRbServiceR29(parent):
    fileName = forceString(
        QtGui.qApp.preferences.appPrefs.get('ImportRbServiceFileName', ''))
    fullLog = forceBool(QtGui.qApp.preferences.appPrefs.get('ImportRbServiceFullLog', ''))
    dlg = CImportRbService1(fileName,  parent)
    dlg.chkFullLog.setChecked(fullLog)
#    dlg.chkCompareOnlyByCode.setChecked(forceBool(getVal(
 #       QtGui.qApp.preferences.appPrefs, 'ImportRbServiceCompareOnlyByCode', False)))
    dlg.exec_()
    QtGui.qApp.preferences.appPrefs['ImportRbServiceFileName'] = toVariant(dlg.fileName)
    QtGui.qApp.preferences.appPrefs['ImportRbServiceFullLog'] = toVariant(dlg.chkFullLog.isChecked())
#    QtGui.qApp.preferences.appPrefs['ImportRbServiceCompareOnlyByCode'] =\
 #       toVariant(dlg.chkCompareOnlyByCode.isChecked())
    dlg2 = CImportRbService2(fileName,  parent)
    dlg2.exec_()

class CMyXmlStreamReader(QXmlStreamReader):

    fieldsHeader = ('VERSION', 'DATE')
    fieldsUslGroup = ('CODE', 'NAME', 'USL_KAT', 'DATEBEG', 'DATEEND', 'IDSP')
    fieldsUsl = ('USL_OK', 'RAZDEL', 'CODE',  'NAME', 'DATEBEG', 'DATEEND', 'EXTNUM')
    fieldsDop = ('RAZDEL', 'DOP_CODE', 'DOP_NAME',  'DET', 'KOL_USL', 'DATEBEG', 'DATEEND')
    fieldsPacientGroup = ('P_CODE', 'P_NAME' , 'COMMENT', 'sex', 'age')
    sexDict = {u'М':u'1', u'Ж':u'2'}
    dictPG = [          u'-х',
                        u'-',
                        u'Взрослый',
                        u'Взр',
                        u'Детский',
                        u'Дет',
                        u'года',
                        u'год',
                        u'г',
                        u'лет',
                        u'месяцев',
                        u'мес',
                        u'м',
                        u'старше',
                        u'и',
                        u'от',
                        u'до',
                        ]
    dictPacientGroup = {
                     #   u'2г':u'2г',
                      #  u'6м':u'6м',
                        u'Взрослый':u'18г-',
                        u'Взр':u'18г-',
                        u'Детский':u'-17г',
                        u'Дет':u'-17г',
                        u'года':u'г',
                        u'год':u'г',
                        u'г': u'г',
                        u'лет':u'г',
                        u'месяцев':u'м',
                        u'мес':u'м',
                        u'м':u'м',
                        u'старше':u'-',
                        u'до':u'г-!',
                        u'и':u'',
                        u'от':u'',
                        u'-х':u'',
                        u'-':u'г-'

}
    coordUsl = {'code':'CODE', 'name':'NAME', 'begDate':'DATEBEG', 'endDate':'DATEEND', 'medicalAidType_id':'USL_OK', 'group_id': 'RAZDEL'}#, 'notes': 'EXTNUM'}
    coordDop = {'code':'DOP_CODE', 'name':'DOP_NAME', 'begDate':'DATEBEG', 'endDate':'DATEEND', 'adultUetDoctor': 'KOL_USL', 'infis':'DOP_CODE'}
    coordPG = {'code':'P_CODE', 'sex':'sex', 'age':'age'}
    coordSG = {'code':'CODE', 'name':'NAME', 'regionalCode':'IDSP'}
    trans = {'code':u'код услуги',
             'name':u'наименование услуги',
             'begDate':u'Дата начала услуги',
             'endDate':u'Дата окончания услуги',
             'adultUetDoctor':u'УЕТ для врача взр',
             'childUetDoctor':u'УЕТ для врача дет',
             'medicalAidType_id':u'Тип МП',
             'group_id': u'Группа услуг',
             'sex': u'Пол',
             'age': u'Возраст',
             'infis': u'код Инфис',
             'regionalCode':'региональый код'}
    def __init__(self,  parent):
        QXmlStreamReader.__init__(self)
        self.parent = parent
        self.db=QtGui.qApp.db
        self.table = self.db.table('rbService')
        self.nadded = 0
        self.ncoincident = 0
        self.nprocessed = 0
        self.nupdated = 0
        self.mapServiceKeyToId = {}
        self.showLog = self.parent.chkFullLog.isChecked()
        self.recursionLevel = 0
        self.skipAll = False
        self.addAll = False
        self.updateAll = False
        self.refValueCache = {}
        self.paragraf = ''
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

        try:
            while (not self.atEnd()):#(self.name() == 'RKU' and self.isEndElement()):
               # print self.name()
                self.readNext()
                if self.name() == 'RKU':
                    self.readNext()
                if self.isStartElement():
                    if self.name() == 'RUBRIKATOR':
                        self.readData()
                    if (self.name() == "USL_LIST"):
                            self.readUSL()
                    if (self.name() == "PG_LIST"):
                            self.readPacientGroup()
                    if (self.name() == "DOP_LIST"):
                        self.readDop()
                if self.name() == 'RKU' and self.isEndElement():
                    break
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
                u'Произошла ошибка', unicode(e), QtGui.QMessageBox.Close)
            self.log(u'! Ошибка: %s' % unicode(e),  True)
            return False
        return not (self.hasError() or self.parent.aborted)




    def readData(self):
        assert self.isStartElement() and self.name() == "RUBRIKATOR"

        while (not self.atEnd()):
            self.readNext()

            if self.isEndElement():
                break

            if self.isStartElement():
                if (self.name() == "USL_OK"):
                    self.readGroupElement()
                else:
                    self.readUnknownElement()

            if self.hasError() or self.parent.aborted:
                break

    def transformPG(self, name, old, new):
        name = name.replace(old, new)
        return name

    def retransformPG(self, name, regexpress):
        c = re.compile(regexpress)
        if c.search(name):
            name=str(int(name[0])*12+int(name[2])) + name[3]
        return name

    def retranslateNamePacientGroup(self, name):
        sex = age = u''
     #   name = unicode(name)
     #   print name.isalpha()
        if name.isalpha() == False:

            name = self.transformPG(name, u' ', u'')
            firstFields = name.split(u'.')
            if name in self.sexDict.keys():
                sex = self.sexDict[name]
                age = u''

            elif len(firstFields) == 2 and forceString(firstFields[0]) in self.sexDict.keys():
                sex = self.sexDict[firstFields[0]]
                age = firstFields[1]

            elif len(firstFields) == 2:
                age = firstFields[1]
            else:
                age = name
            for x in self.dictPG:
                age = self.transformPG(age, x, self.dictPacientGroup[x])
            if age != u'':
                age = self.retransformPG(age, u'[0-9][^a-z][0-9][^a-z]')
                age = self.prepareAge(age)
        return sex, age



    def prepareAge(self, age):
        if age[-1].isalpha() == False:
            age = age + u'г'
        if len(age) <4:
            age = age + '-' + age
        s =  age.find('!')
        if s >0:
            age = age[:s] + str(int(age[s+1:-1]) -1)+age[-1:]
        return age

    def readPacientGroup(self):
        assert self.isStartElement() and self.name() == "PG_LIST"
        table = self.db.table('rbPacientGroup_r29')
        while (not self.atEnd()):
            self.readNext()
            if self.name() == "PG_LIST" and self.isEndElement():
                break
            if self.isStartElement():
                if (self.name() == "PG"):
                    result = self.readGroup('PG', self.fieldsPacientGroup)
                    idx = self.lookupServiceElementByCode(table, result['P_CODE'])
                    result['name'] = forceString(result['P_NAME'])
                    first = ''
                    if ',' in result['P_NAME']:
                        if '.' in result['P_NAME']:
                            first = result['P_NAME'].split('.')[0]
                        second = result['P_NAME'].replace(first+'.', '')
                        second =second.split(',')
                        if isinstance(second, list):
                            for el in second:
                                result['sex'], result['age'] = self.retranslateNamePacientGroup(first + '.' + el)
                                idx = self.db.getRecordList('rbPacientGroup_r29', 'id', 'code = "%s" AND sex = "%s" AND age = "%s"'%(result['P_CODE'], result['sex'], result['age']))
                                if idx == []:
                                    self.addPacientGroup(result)
                             #   for id in idx:
                             #       if id:
                             #           change, diff = self.getServiceDifference(table, id, result, self.coordPG)
                             #           if diff:
                             #               self.addPacientGroup(result)
                             #       else:
                             #              self.addPacientGroup(result)
                    else:
                        result['sex'], result['age'] = self.retranslateNamePacientGroup(result['P_NAME'])
#                    for id in idx:
#                        if id:
#                            change, diff = self.getServiceDifference(table, id, result, self.coordPG)
#                            if diff:
#                                self.updatePacientGroup(id,  result, change)
                    if idx == []:
                        self.addPacientGroup(result)

    def readDop(self):
        self.skipAll = self.updateAll = self.addAll = None
        assert self.isStartElement() and self.name() == "DOP_LIST"

        while (not self.atEnd()):
            self.readNext()

            if self.name() == "DOP_LIST" and self.isEndElement():
                break

            if self.isStartElement():
                if (self.name() == "DOP"):
                    result = self.readGroup('DOP', self.fieldsDop)

                #    stmt = 'Select FROM rbService LEFT JOIN rbServiceGroup ON rbServiceGroup.id = rbService.group id WHERE'
                    groupId = forceRef(self.db.translate('rbServiceGroup', 'code', forceString(result['RAZDEL']),'id'))
                    if groupId:
                        dopCode = self.db.getRecordList(self.table, '*', 'group_id = %s'%groupId)
                        for dop in dopCode:
                            result['DOP_NAME'] =  result['DOP_NAME'][:500]
                            result['RAZDEL'] =  '9'
                            name = result['DOP_NAME'][:500]
                            if 'KOL_USL' in result.keys():
                                result['KOL_USL'] = forceString(forceDouble(result['KOL_USL']))
                            code =  forceString(dop.value('code')) + '-' + result['DOP_CODE']

                        #    print code
                            if 'DATEEND' not in result.keys():
                                result['DATEEND'] = '2075-01-01'
                            self.log(u'Элемент: %s (%s)' %(name, code))
                            id = None
                            idx = self.lookupServiceElementByCode(self.table, code)
                            for id in idx:
                                if id:
                                   change, diff = self.getServiceDifference(self.table, id, result, self.coordDop, 1, code, name)
                                if self.hasError() or self.parent.aborted:
                                    return None
                                if id and not (self.skipAll or self.updateAll or self.addAll):
                                   if diff:
                                       answer = QtGui.QMessageBox.question(self.parent,
                                                                           u'Внимание!',
                                                                           u'Услуга  "%s" "%s"  уже есть в БД.<br>Отличия:%s<br>'\
                                                                           u'Да - добавить новую запись, Нет - обновить,<br>'\
                                                                           u'Прервать - не обрабатывать текущую запись' % (code, name, diff),
                                                                           QtGui.QMessageBox.Yes|QtGui.QMessageBox.YesToAll|QtGui.QMessageBox.No|
                                                                           QtGui.QMessageBox.NoToAll|QtGui.QMessageBox.Abort,
                                                                           QtGui.QMessageBox.Abort)
                                       if answer == QtGui.QMessageBox.YesToAll:
                                            self.addAll = True
                                       elif answer == QtGui.QMessageBox.NoToAll:
                                            self.updateAll = True
                                       elif answer == QtGui.QMessageBox.No:
                                            self.updateService(id,  result, change)
                                       elif answer == QtGui.QMessageBox.Yes:
                                            self.addDopService(result, code, name)

                            if id and self.addAll:
                                self.log(u'% Добавляем новую запись, хотя в БД похожая уже есть.')
                                self.addDopService(result, code, name)
                            elif id and self.updateAll:
                             #   self.log(u'* Обновляем')
                                self.updateService(id, result,  change)
                            elif id:
                                self.log(u'%% Найдена совпадающая запись (id=%d), пропускаем' % id)
                                self.ncoincident += 1
                            else:
                                self.log(u'% Сходные записи не обнаружены. Добавляем')
                                # новая запись, добавляем само действие и все его свойства + ед.изм.
                                self.addDopService(result, code, name)

                                self.nprocessed += 1
                                self.parent.statusLabel.setText(
                                                u'импорт услуг: %d добавлено; %d обновлено; %d совпадений; %d обработано' % (self.nadded,
                                                                    self.nupdated,  self.ncoincident,  self.nprocessed))
                else:
                    self.readUnknownElement()

            if self.hasError() or self.parent.aborted:
                break

    def readUSL(self):
        assert self.isStartElement() and self.name() == "USL_LIST"

        while (not self.atEnd()):
            self.readNext()

            if self.name() == "USL_LIST" and self.isEndElement():
                break

            if self.isStartElement():
                if (self.name() == "USL"):
                    result = self.readGroup('USL', self.fieldsUsl)

                    groupId =  forceString(self.db.translate('rbServiceGroup', 'code', forceString(result.get('RAZDEL')), 'name'))
                    self.log(u'Добавляем услуги из раздела:' + forceString(result.get('RAZDEL')))
                    if 'DATEEND' in result.keys():
                        if QDate.fromString(result['DATEEND'], Qt.ISODate) < QDate(2016, 1, 2):
                            result['NAME'] = result['NAME'][:500]
                        else:
                            result['NAME'] = (result['NAME']+ '(%s)'%groupId)[:500]
                    else:
                        result['NAME'] = (result['NAME']+ '(%s)'%groupId)[:500]
                    name = result['NAME'][:500]
                    code = result['CODE']


                    if 'DATEEND' not in result.keys():
                        result['DATEEND'] = '2075-01-01'
                    self.log(u'Элемент: %s (%s)' %(name, code))
                    id = None
                    idx = self.lookupServiceElementByCode(self.table, code)
                    for id in idx:
                        if id:
                           change, diff = self.getServiceDifference(self.table, id, result, self.coordUsl)
                        if self.hasError() or self.parent.aborted:
                            return None
                        if id and not (self.skipAll or self.updateAll or self.addAll):
                           if diff:
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
                                    self.updateService(id,  result, change)
                               elif answer == QtGui.QMessageBox.Yes:
                                    self.addService(result)
                    if id and self.addAll:
                        self.log(u'% Добавляем новую запись, хотя в БД похожая уже есть.')
                        self.addService(result)
                    elif id and self.updateAll:
                        self.log(u'* Обновляем')
                        self.updateService(id, result, change)
                    elif id:
                        self.log(u'%% Найдена совпадающая запись (id=%d), пропускаем' % id)
                        self.ncoincident += 1
                    else:
                        self.log(u'% Сходные записи не обнаружены. Добавляем')
                        # новая запись, добавляем само действие и все его свойства + ед.изм.
                        self.addService(result)

                        self.nprocessed += 1
                        self.parent.statusLabel.setText(
                                        u'импорт типов действий: %d добавлено; %d обновлено; %d совпадений; %d обработано' % (self.nadded,
                                                                                                                              self.nupdated,  self.ncoincident,  self.nprocessed))

                else:
                    self.readUnknownElement()

            if self.hasError() or self.parent.aborted:
                break

    def getServiceDifference(self, table, oldRecordId, newRecordDict, dict, flag = None, code = None, name = None):
        parts = []
        changes = {}
        oldRecord = self.db.getRecord(table, '*', oldRecordId)
        for fieldName in dict.keys():
                oldValue = oldRecord.value(fieldName)

                if fieldName=='group_id':
                        oldValue = toVariant(self.db.translate('`rbServiceGroup`', 'id', oldValue, 'code'))
                if flag:
                    if 'DET' in newRecordDict.keys():
                        if (newRecordDict['DET'] == '1') and fieldName == u'adultUetDoctor':
                            fieldName=u'childUetDoctor'
                            oldValue = oldRecord.value(fieldName)
                            newValue = toVariant(newRecordDict.get(u'KOL_USL'))
                        else:
                            newValue = toVariant(newRecordDict.get(dict[fieldName]))
                    elif code and fieldName in (u'code', u'infis'):
                            newValue =code
                    elif name and fieldName == u'name':
                            newValue =name
                    else:
                        newValue = toVariant(newRecordDict.get(dict[fieldName]))
                else:
                    if fieldName=='medicalAidType_id':
                        oldValue = toVariant(self.db.translate('rbMedicalAidType', 'id', oldValue, 'regionalCode'))

                    newValue = toVariant(newRecordDict.get(dict[fieldName]))
                if not variantEq(oldValue, newValue): # or  not variantEq(toVariant(fieldName), oldFieldName):
                    changes[fieldName] =forceString(newValue)
                    if table.tableName != 'rbServiceGroup':
                        parts.append(u'<b>%s</b> <br> было: <b>%s</b><br> стало: <b>%s</b><br>,' % (self.trans[fieldName], forceString(oldValue), forceString(newValue)))
        return changes, ', '.join(parts)

    def updatePacientGroup(self, id, newRecordDict, change):
        table = self.db.table('rbPacientGroup_r29')
        record = self.db.getRecord(table, '*', id)
        for x in change:
            value = change.get(x)
            if value:
                record.setValue(x,  forceString(value))
        id = self.db.updateRecord(table, record)
        self.nupdated += 1


    def addPacientGroup(self, newRecordDict):
        table = self.db.table('rbPacientGroup_r29')
        record = table.newRecord()
        record.setValue('code', forceString(newRecordDict.get('P_CODE')))
        record.setValue('name', forceString(newRecordDict.get('P_NAME')))
        record.setValue('sex', forceString(newRecordDict.get('sex')))
        record.setValue('age', forceString(newRecordDict.get('age')))
        self.db.insertRecord(table, record)
        self.nadded += 1

    def updateSGroup(self, id, newRecordDict, change):
        table = self.db.table('rbServiceGroup')
        record = self.db.getRecord(table, '*', id)
        for x in change:
            value = change.get(x)
            if value:
                record.setValue(x,  forceString(value))
        id = self.db.updateRecord(table, record)
        self.nupdated += 1


    def addServiceGroup(self, newRecordDict):
        table = self.db.table('rbServiceGroup')
        record = table.newRecord()
        record.setValue('code', forceString(newRecordDict.get('CODE')))
        record.setValue('regionalCode', forceString(newRecordDict.get('IDSP')))
        record.setValue('name', forceString(newRecordDict.get('NAME'))[:64])
        self.db.insertRecord(table, record)
        self.nadded += 1

    def addDopService(self, newRecordDict, code, name):
        record = self.table.newRecord()
        groupId =  forceRef(self.db.translate('rbServiceGroup', 'code', 9, 'id'))
        record.setValue('code', code)
        record.setValue('begDate', forceString(newRecordDict.get('DATEBEG')))
        record.setValue('endDate', forceString(newRecordDict.get('DATEEND')))
        record.setValue('name', name[:500])
        record.setValue('infis', code)
        if forceInt(newRecordDict.get('DET')) == 0:
            record.setValue('adultUetDoctor', forceString(newRecordDict.get('KOL_USL')))
        else:
            record.setValue('childUetDoctor', forceString(newRecordDict.get('KOL_USL')))
        record.setValue('group_id', groupId)
        self.db.insertRecord(self.table, record)
        self.nadded += 1


    def addService(self, newRecordDict):
        record = self.table.newRecord()
        groupId =  forceRef(self.db.translate('rbServiceGroup', 'code', forceString(newRecordDict.get('RAZDEL')), 'id'))
        record.setValue('code', forceString(newRecordDict.get('CODE')))
        record.setValue('begDate', forceString(newRecordDict.get('DATEBEG')))
        record.setValue('endDate', forceString(newRecordDict.get('DATEEND')))
        record.setValue('name', forceString(newRecordDict.get('NAME'))[:500])
        medicalAidTypeCode = forceRef(self.db.translate('rbMedicalAidType', 'regionalCode', forceString(newRecordDict.get('USL_OK')), 'id'))
#        self.lookupAid('Type', forceString(newRecordDict.get('USL_OK')))
        record.setValue('medicalAidType_id', medicalAidTypeCode)
        record.setValue('infis', forceString(newRecordDict.get('CODE')))
        record.setValue('group_id', groupId)
        self.db.insertRecord(self.table, record)
        self.nadded += 1


    def updateService(self, id,  newRecordDict, change):
        record = self.db.getRecord(self.table, '*', id)

        for x in change:
            if x == 'medicalAidType_id':
               value = forceRef(self.db.translate('rbMedicalAidType', 'regionalCode', change.get(x), 'id'))
            elif x == 'group_id':
               value = forceRef(self.db.translate('rbServiceGroup', 'code', change.get(x), 'id'))
            else:
                value = change.get(x)

            if value:
                record.setValue(x,  toVariant(value))

        id = self.db.updateRecord(self.table, record)

        self.nupdated += 1

    def readGroup(self, groupName, fieldsList):
        if self.atEnd():
            return None
        result = {}
        while not (self.isEndElement() and self.name() == groupName):
            if self.name() in fieldsList:
             #   result[forceString(self.name())] = forceString(self.readElementText()).decode('utf8')
                result[forceString(self.name())] = forceString(self.readElementText())
            self.readNext()
            if self.isEndDocument() or len(result) == len(fieldsList):
                break
        return result


    def readGroupElement(self):
    #    assert self.isStartElement() and self.name() == "USL_OK"
        while not self.atEnd():
            self.readNext()
            result = []
            QtGui.qApp.processEvents()
            if self.atEnd():
                return None
            if self.name() == 'USL_OK' and self.isEndElement():
                return None
            if self.isStartElement():
                if self.name() == 'RAZDEL':
                    result.append(self.readGroup('RAZDEL', self.fieldsUslGroup))
                if result != [{}]:
                    for element in  result:
                        code = element['CODE']

                        id = forceRef(self.db.translate('rbServiceGroup', 'code', code ,'id'))
#                         stmt = "SELECT `id` FROM `rbServiceGroup` WHERE `code` = '%s'"
#                         query = self.db.query(stmt%(code))
#                         id = forceInt(query.record().value('id'))
                        if id:
                            change, diff = self.getServiceDifference(QtGui.qApp.db.table('rbServiceGroup'), id, element, self.coordSG)
                            if change != []:
                                self.updateSGroup(id,  result, change)
                        else:
                            self.addServiceGroup(element)






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



    def lookupIdByCode(self, code, fieldName,  searchByName = False):
        cache = self.refValueCache[fieldName]
        index = cache.getIndexByCode(code)
        if index>=0 and cache.getCode(index) == code:
            return cache.getId(index)
        return None


    def lookupAid(self, colName, code):
        if code:
            id = self.lookupIdByCode(code, 'medicalAid'+colName+'_id')
            if not id:
                self.log(u'Тип помощи (%s) в таблице %s не найден.' % (code, 'medicalAid'+colName),  True)
            return id
        return None


    def lookupServiceElement(self, table, code, name):
        key = (code, name)
        id = self.mapServiceKeyToId.get(key,  None)
        idx = []
        if id:
            return id

        cond = []

        cond.append(table['code'].eq(toVariant(code)))
        cond.append(table['name'].eq(toVariant(name[:500])))

        stmt = self.db.selectStmt(table, ['id'], where=cond)
        query = self.db.query(stmt)
        while query.next():
            id = forceRef(query.record().value('id'))
         #   self.mapServiceKeyToId[key] = id
            idx.append(id)

        return idx


    def lookupServiceElementByCode(self, table, code):
        key = (code)
        id = self.mapServiceKeyToId.get(key,  None)
        idx = []
        if id:
            return id

        cond = []

        cond.append(table['code'].eq(toVariant(code)))
     #   cond.append(table['name'].eq(toVariant(name[:500])))

        stmt = self.db.selectStmt(table, ['id'], where=cond)
        query = self.db.query(stmt)
        while query.next():
            id = forceRef(query.record().value('id'))
         #   self.mapServiceKeyToId[key] = id
            idx.append(id)

        return idx


class CImportRbService1(QtGui.QDialog, Ui_ImportRbServiceR29_1):
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


    @pyqtSignature('')
    def on_btnContinue_clicked(self):
        CMyXmlStreamReader.readUSL()


    @pyqtSignature('')
    def on_btnSelectFile_clicked(self):
        self.fileName = QtGui.QFileDialog.getOpenFileName(
            self, u'Укажите файл с данными', self.edtFileName.text(), u'Файлы XML (*.xml)')
        if self.fileName != '':
            self.edtFileName.setText(self.fileName)
            self.btnImport.setEnabled(True)



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
            myXmlStreamReader = CMyXmlStreamReader(self)
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

class CImportRbService2(CItemEditorBaseDialog, Ui_ImportRbServiceR29_2):
    def __init__(self, fileName,  parent=None):
        CItemEditorBaseDialog.__init__(self, parent, Ui_ImportRbServiceR29_2)
        self.db=QtGui.qApp.db
       # self.tableModel = CMedicalAidProfilesModel(self)
        self.addModels('MedicalAidProfiles', CMedicalAidProfilesModel(self))
        self.setupUi(self)
        self.cmbServiceGroup.setTable('rbServiceGroup')
        self.cmbMedicalAidKind.setTable('rbMedicalAidKind')
        self.cmbMedicalAidType.setTable('rbMedicalAidType')
        self.cmbMedicalAidProfile.setTable('rbMedicalAidProfile')
        self.setModels(self.tblCoord, self.modelMedicalAidProfiles, self.selectionModelMedicalAidProfiles)
        self.tblCoord.addMoveRow()
        self.tblCoord.addPopupDelRow()


    @pyqtSignature('int')
    def on_cmbServiceGroup_currentIndexChanged(self, index):
        self.serviceGroupId = self.cmbServiceGroup.value()
      #  groupId = forceRef(self.db.translate('rbServiceGroup', 'code', forceString(result['RAZDEL']),'id'))
        serviceId = forceRef(self.db.translate('rbService', 'group_id', self.serviceGroupId, 'id'))
        self.serviceRecord = self.db.getRecord('rbService', '*', serviceId)
        self.serviceProfileRecord = self.db.getRecordList('rbService_Profile', '*', 'master_id=%s'%serviceId)
       # self.tblCoord.setSpecialityId(specialityId)
        self.cmbMedicalAidKind.setValue(forceRef(self.serviceRecord.value('medicalAidKind_id')))
        self.cmbMedicalAidType.setValue(forceRef(self.serviceRecord.value('medicalAidType_id')))
        self.cmbMedicalAidProfile.setValue(forceRef(self.serviceRecord.value('medicalAidProfile_id')))
        self.modelMedicalAidProfiles.loadItems(serviceId)



    @pyqtSignature('')
    def on_btnContinue_clicked(self):

        serviceRecords = self.db.getRecordList('rbService', '*', 'group_id = %s'% self.serviceGroupId)

        tableSP = self.db.table('rbService_Profile')
        tableService = self.db.table('rbService')
        for sv in serviceRecords:
            id = forceRef(sv.value('id'))

            sv.setValue('medicalAidKind_id',  self.cmbMedicalAidKind.value()) #.setValue(forceRef(self.serviceRecord.value('medicalAidKind_id')))
            sv.setValue('medicalAidType_id', self.cmbMedicalAidType.value())
            sv.setValue('medicalAidProfile_id', self.cmbMedicalAidProfile.value())
            self.db.updateRecord(tableService, sv)
            for i in self.modelMedicalAidProfiles.items():
                cond = []
                cond.append('master_id =%s'%id)
             #   print id
#                 mak = forceRef(i.value('medicalAidKind_id'))
#                 if mak:
#                     cond.append('medicalAidKind_id =%s'%mak)
#                 mat = forceRef(i.value('medicalAidKind_id'))
#                 if mat:
#                     cond.append('medicalAidType_id =%s'%mat)
#                 mad = forceRef(i.value('medicalAidProfile_id'))
#                 if mad:
#                     cond.append('medicalAidProfile_id =%s'%mad)
                spec = forceRef(i.value('speciality_id'))
                if spec:
                    cond.append('speciality_id =%s'%spec)
                records = self.db.getRecordList('rbService_Profile', '*',
                                                ' %s'%
                                                (self.db.joinAnd(cond)))
            #    records = []
                if not records:
                    record = tableSP.newRecord()
                    record.setValue('master_id', forceString(id))
                #    self.db.insertRecord(table, record)
                    records.append(record)
                for rec in records:
#                    rec = i
                     rec.setValue('master_id', forceString(id))
                     rec.setValue('medicalAidKind_id', forceRef(i.value('medicalAidKind_id')))
                     rec.setValue('medicalAidType_id', forceRef(i.value('medicalAidType_id')))
                     rec.setValue('medicalAidProfile_id', forceRef(i.value('medicalAidProfile_id')))
                     rec.setValue('speciality_id', forceRef(i.value('speciality_id')))
                     self.db.insertOrUpdate(tableSP, rec)
                #    self.modelMedicalAidProfiles.saveItems(id)
        #   self.modelMedicalAidProfiles._items = record
       #    self.modelMedicalAidProfiles.saveItems(id)


    @pyqtSignature('')
    def on_btnClose_clicked(self):
        self.close()

  #  def saveInternals(self, id):
    #    self.modelServices.saveItems(id)
   #     self.modelMedicalAidProfiles.saveItems(id)

class CServiceContentsModel(CInDocTableModel):
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'rbService_Contents', 'id', 'master_id', parent)
        self.addCol(CCodeNameInDocTableCol(u'Услуга', 'service_id', 40, 'rbService', preferredWidth = 100))
        self.addCol(CBoolInDocTableCol(u'Обязательно', 'required', 10))


class CMedicalAidProfilesModel(CInDocTableModel):
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'rbService_Profile', 'id', 'master_id', parent)
        self.addCol(CRBInDocTableCol(   u'Специальность',  'speciality_id', 20, 'rbSpeciality', showFields = CRBComboBox.showName))
        self.addCol(CRBInDocTableCol(   u'Профиль',        'medicalAidProfile_id', 20, 'rbMedicalAidProfile', showFields = CRBComboBox.showName))
        self.addCol(CRBInDocTableCol(   u'Вид',            'medicalAidKind_id',    20, 'rbMedicalAidKind', showFields = CRBComboBox.showName))
        self.addCol(CRBInDocTableCol(   u'Тип',            'medicalAidType_id',    20, 'rbMedicalAidType', showFields = CRBComboBox.showName))

