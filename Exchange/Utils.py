# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2023 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

import os
import re
import datetime
from binascii import hexlify
from zipfile import ZIP_DEFLATED, ZipFile
from PyQt4 import QtGui, QtSql
from PyQt4.QtCore import Qt, QDate, QRegExp, QVariant, QDateTime

from library.database import connectDataBase
from library.dbfpy.dbf import Dbf
from library.exception import CException
from library.Utils import forceDate, forceInt, forceRef, forceString, forceStringEx, nameCase, toVariant, variantEq

# это скверная затея - Utils это что-то не спеифичное, общепотребительное.
# получается, что getTariffDifference и copyTariff ещё более общие?
# тогда почему они не в Utils ?
#from Exchange.ImportTariffsXML import getTariffDifference, copyTariff
from Registry.Utils import getClientAddress


def getId(table, fields, fields2=[]):
    db = QtGui.qApp.db
#    cond=[table[name].eq(toVariant(val)) for (name, val) in fields]
    cond=[]
    for (name, val) in fields:
        if val==None:
            cond.append(table[name].isNull())
        else:
            cond.append(table[name].eq(toVariant(val)))
    record=db.getRecordEx(table, '*', where=cond)
    if record:
        updateRecord = False
        for (name, val) in fields2:
            recVal=record.value(name)
            if (recVal.isNull() or forceString(recVal)=='') and isNotNull(val):
                record.setValue(name, toVariant(val))
                updateRecord = True
        if updateRecord:
            db.updateRecord(table, record)
        return forceInt(record.value('id'))
    else:
        record = table.newRecord()
        for (name, val) in fields+fields2:
            record.setValue(name, toVariant(val))
        return db.insertRecord(table, record)


def findAndUpdateOrCreateRecord(table, filterFields, updateFields=[], id=None):
    # вариант getId, обновляющий запись не только если поля пусты
    db = QtGui.qApp.db
    cond=[ table[name].isNull() if val is None else table[name].eq(toVariant(val))
           for (name, val) in filterFields
         ]
    if id:
        cond.append(table['id'].eq(id))
    record=db.getRecordEx(table, '*', where=cond)
    if record:
        updateRecord = False
        for (name, val) in updateFields:
            recVal=record.value(name)
            newVal=toVariant(val)
            if not variantEq(recVal, newVal):
                record.setValue(name, newVal)
                updateRecord = True
        if updateRecord:
            db.updateRecord(table, record)
        return forceInt(record.value('id'))
    else:
        record = table.newRecord()
        for (name, val) in filterFields:
            record.setValue(name, toVariant(val))
        for (name, val) in updateFields:
            record.setValue(name, toVariant(val))
        return db.insertRecord(table, record)


def checkPatientData(self, lastNameField, firstNameField, patrNameField, sexField, birthDateField):
    bad=False
    lastName=nameCase(self.row[lastNameField])
    firstName=nameCase(self.row[firstNameField])
    patrName=nameCase(self.row[patrNameField])
    if not (lastName and firstName and patrName):
        bad=True
        self.err2log(u'нет полного ФИО')
    fio=lastName+firstName+patrName
    if not check_rus_lat(fio):
        bad=True
        self.err2log(u'недопустимое ФИО')
    sex=self.row[sexField].upper()
    if sex == u'М':
        sex = 1
    elif sex == u'Ж':
        sex = 2
    else:
        self.err2log(u'не указан пол')

    birthDate=self.row[birthDateField]
    if not birthDate:
        bad=True
        self.err2log(u'не указан день рождения')
    if bad:
        return None
    else:
        clientFields=[
            ('lastName', lastName), ('firstName', firstName), ('patrName', patrName),
            ('sex', sex), ('birthDate', birthDate)]
        return checkData(clientFields, self.tableClient)

def checkData(fields, table):
    db = QtGui.qApp.db
    cond=[]
    for (name, val) in fields:
        if val==None:
            cond.append(table[name].isNull())
        else:
            cond.append(table[name].eq(toVariant(val)))
    record=db.getRecordEx(table, '*', where=cond)
    if record:
        return True
    return False


def isNull(s):
    return s in (None, '', 'Null', 'null', 'NULL')


def isNotNull(s):
    return s not in (None, '', 'Null', 'null', 'NULL')


def dbfCheckNames(d, names):
    for name in names:
        if name not in d.header.fields:
            return False
    return True


def xmlCheckNames(d, names):
    for name in names:
        if not d.get(name, None):
            return False
    return True


def getOKVED(okved):
    OKVED=''
    for c in okved:
        if c==' ': pass
        elif c=='-': break
        else: OKVED=OKVED+c
    if len(OKVED) and OKVED[0:1].isdigit():
        OKVED=QtGui.qApp.db.translate('rbOKVED', 'OKVED', OKVED, 'code')
    return OKVED

currentYear=QDate.currentDate().year()
currentYearBeg=datetime.date(currentYear, 1, 1)
currentYearEnd=datetime.date(currentYear, 12, 31)

def tbl(tn):
    t=QtGui.qApp.db.table(tn)
    assert t.fields
    return t

rus_re=re.compile(u'[абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ]')
lat_re=re.compile('[a-zA-Z]')

def check_rus_lat(s):
    rus=rus_re.search(s)!=None
    lat=lat_re.search(s)!=None
    return rus!=lat

def check_rus(s):
    return rus_re.search(s)

#WFT? это, товарищи, говнище: эта функция очень специфична, что она делает в Utils?
def get_specs(POL):
    if POL in (1, u'м', u'М'):
        POL_spec1, POL_spec2 = [], [('U', '84', 3)]
    else:
        POL_spec1, POL_spec2 = [('A', '02', 3)], []
    return [('T', '78', 5)]+POL_spec1+[('N', '40', 3), ('H', '89', 3)]+POL_spec2+[('O', '49', 3), ('E', '91', 3)]


def getWorkHurt(clientWorkId):
    hurt   = ''
    stage  = 0
    factors = ''
    if clientWorkId:
        db = QtGui.qApp.db
        stmt = u'''
SELECT
    rbHurtType.code AS hurt,
    ClientWork_Hurt.stage AS stage,
    GROUP_CONCAT(DISTINCT rbHurtFactorType.code ORDER BY rbHurtFactorType.code) AS factors
FROM
    ClientWork_Hurt
    LEFT JOIN rbHurtType ON rbHurtType.id = ClientWork_Hurt.hurtType_id
    LEFT JOIN ClientWork_Hurt_Factor ON ClientWork_Hurt_Factor.master_id = ClientWork_Hurt.id
    LEFT JOIN rbHurtFactorType ON rbHurtFactorType.id = ClientWork_Hurt_Factor.factorType_id
WHERE
    ClientWork_Hurt.master_id = %d AND
    ClientWork_Hurt.stage = (
        SELECT MAX(CWH.stage) FROM ClientWork_Hurt AS CWH WHERE CWH.master_id=%d)
GROUP BY ClientWork_Hurt.id
            ''' % (clientWorkId, clientWorkId)
        query = db.query(stmt)
        if query.next():
            record = query.record()
            hurt    = forceString(record.value(0))
            stage   = forceInt(record.value(1))
            factors = forceString(record.value(2))
    return hurt, stage, factors

def get_Account_Item(eventId):
    if not eventId: return None
    stmt='''
select
Account_Item.date, rbPayRefuseType.code, rbPayRefuseType.name
from
Account_Item
left join rbPayRefuseType on rbPayRefuseType.id=Account_Item.refuseType_id
where
Account_Item.event_id='''+str(eventId)+''' and Account_Item.date=(
    select max(a.date) from Account_Item as a where a.master_id=Account_Item.master_id)
        '''
    query=QtGui.qApp.db.query(stmt)
    if query.next():
        return query.record()
    return None

def getClientAddressEx(clientId):
    freeInput = ''
    KLADRCode = ''
    KLADRStreetCode = ''
    house = ''
    corpus = ''
    flat = ''

    db = QtGui.qApp.db
    regAddressRecord=getClientAddress(clientId, 0)
    if regAddressRecord:
        addressId=forceRef(regAddressRecord.value('address_id'))
        freeInput=forceString(regAddressRecord.value('freeInput'))
        if addressId:
            recAddress = db.getRecord('Address', 'house_id, flat', addressId)
            if recAddress:
                flat = forceString(recAddress.value('flat'))
                houseId = forceRef(recAddress.value('house_id'))
                if houseId:
                    recHouse = db.getRecord(
                        'AddressHouse', 'KLADRCode, KLADRStreetCode, number, corpus',  houseId)
                    KLADRCode=forceString(recHouse.value('KLADRCode'))
                    KLADRStreetCode=forceString(recHouse.value('KLADRStreetCode'))
                    house = forceString(recHouse.value('number'))
                    corpus = forceString(recHouse.value('corpus'))
    return freeInput, KLADRCode, KLADRStreetCode, house, corpus, flat



def getDiags(event_id, speciality):
    stmt='''
select
    Person.lastName, Person.firstName, Person.patrName, Person.code,
    Diagnostic.sanatorium, Diagnostic.endDate, Diagnostic.diagnosisType_id,
    Diagnosis.MKB, Diagnostic.character_id, Diagnostic.stage_id, Diagnostic.healthGroup_id,
    rbDispanser.code AS dispanser_code
from
    Diagnostic
    join Person on Diagnostic.person_id=Person.id
    join Diagnosis on Diagnosis.id=Diagnostic.diagnosis_id
    join rbSpeciality on rbSpeciality.id=Person.speciality_id
    left join rbDispanser on rbDispanser.id = Diagnostic.dispanser_id
where
    Diagnostic.event_id='''+str(event_id)+''' and rbSpeciality.code=\''''+str(speciality)+'''\'
    AND Diagnostic.deleted = 0 AND Diagnosis.deleted = 0
order
    by Diagnostic.diagnosisType_id
        '''
    query=QtGui.qApp.db.query(stmt)
    Diags=[]
    while query.next():
        Diags.append(query.record())
    return Diags

def getOtherDiags(event_id, specs):
    sp=' and rbSpeciality.code not in ('+', '.join([s[1] for s in specs])+')'
    stmt='''
select
    Person.lastName, Person.firstName, Person.patrName, Person.code,
    Diagnostic.sanatorium, Diagnostic.endDate, Diagnostic.diagnosisType_id,
    Diagnosis.MKB, Diagnostic.character_id, Diagnostic.stage_id, Diagnostic.healthGroup_id,
    rbSpeciality.code as spec_code, rbSpeciality.OKSOCode, rbSpeciality.name as spec_name
from
    Diagnostic
    join Person on Diagnostic.person_id=Person.id
    join Diagnosis on Diagnosis.id=Diagnostic.diagnosis_id
    join rbSpeciality on rbSpeciality.id=Person.speciality_id
where
    Diagnostic.event_id='''+str(event_id)+sp+'''
    AND Diagnostic.deleted = 0 AND Diagnosis.deleted = 0
order
    by Diagnostic.diagnosisType_id
        '''
    query=QtGui.qApp.db.query(stmt)
    Diags=[]
    while query.next():
        Diags.append(query.record())
    return Diags

def get_dom_korp_kv(freeInput):
    DOM, KOR, KV = None, None, None
    dom_pos=freeInput.rfind(u' д.')
    if dom_pos==-1:
        dom_pos=freeInput.rfind(u',д.')
    if dom_pos==-1:
        dom_pos=freeInput.rfind(u' Д ')
    if dom_pos==-1:
        dom_pos=freeInput.rfind(u' Д.')
    if dom_pos==-1:
        dom_pos=freeInput.rfind(u',Д.')
    if dom_pos>=0:
        f=freeInput[dom_pos+3:]
        d2=f.find(',')
        if d2>=0:
            f=f[:d2]
        DOM=f.strip()
    k_pos=freeInput.find(u' к.')
    if k_pos==-1:
        k_pos=freeInput.find(u',к.')
    if k_pos==-1:
        k_pos=freeInput.find(u',КОРП.')
    if k_pos==-1:
        k_pos=freeInput.find(u',КОР.')
    if k_pos==-1:
        k_pos=freeInput.find(u',К.')
    if k_pos>=0:
        f=freeInput[k_pos+3:]
        k2=f.find(',')
        if k2>=0:
            f=f[:k2]
        KOR=f.strip()
    kv_pos=freeInput.find(u' кв.')
    if kv_pos==-1:
        kv_pos=freeInput.find(u',кв.')
    if kv_pos==-1:
        kv_pos=freeInput.find(u' КВ ')
    if kv_pos==-1:
        kv_pos=freeInput.find(u' КВ.')
    if kv_pos==-1:
        kv_pos=freeInput.find(u',КВ.')
    if kv_pos>=0:
        f=freeInput[kv_pos+4:]
        kv2=f.find(',')
        if kv2>=0:
            f=f[:kv2]
        KV=f.strip()
    return DOM, KOR, KV

def get_dop(dop0):
    dop=[]
    for (dop_name, dop_code, dop_group_id) in dop0:
        r=QtGui.qApp.db.getRecordEx(
            'ActionType', 'id', 'code=\'%s\' and group_id=%d' % (dop_code, dop_group_id))
        if r:
            dop_id=forceInt(r.value(0))
            if dop_id:
                dop.append((dop_name, dop_id))
    return dop

def setEIS_db():
    EIS_db=QtGui.qApp.EIS_db
    if not EIS_db:
        pref=QtGui.qApp.preferences
        props=pref.appPrefs
        EIS_dbDriverName=forceStringEx(props.get('EIS_driverName', QVariant()))
        EIS_dbServerName=forceStringEx(props.get('EIS_serverName', QVariant()))
        EIS_dbServerPort=forceInt(props.get('EIS_serverPort', QVariant()))
        EIS_dbDatabaseName=forceStringEx(props.get('EIS_databaseName', QVariant()))
        EIS_dbUserName=forceStringEx(props.get('EIS_userName', QVariant()))
        EIS_dbPassword=forceStringEx(props.get('EIS_password', QVariant()))
        EIS_db = connectDataBase(
            EIS_dbDriverName, EIS_dbServerName, EIS_dbServerPort,
            EIS_dbDatabaseName, EIS_dbUserName, EIS_dbPassword, 'EIS')
        QtGui.qApp.EIS_db=EIS_db

def EIS_close():
    if QtGui.qApp.EIS_db:
        QtGui.qApp.EIS_db.close()
        QtGui.qApp.EIS_db=None
    QtGui.QMessageBox.information(
        None, u'нет связи', u'не удалось установить соединение с базой ЕИС',
        QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)


def binaryToInt(str):
    str = str.encode('cp866')
    return int('0' + hexlify(str), 16)


def insertRecordFromDbf(db, tablename, record, fields=None, mode=0):
    u"""
    Конвертирует запись DBF в запись в любой БД
    db - БД
    tablename - имя таблицы БД, куда вставлять запись
    record - запись DBF
    fields - номера полей, которые надо конвертировать (None - все поля). Если номер равен -1, нужно вставить значение по умолчанию.
    mode: 0 - IGNORE,
      1 - REPLACE
    """
    db_record = db.record(tablename)
    values = record.asList()
    valuesLen = len(values)
    strvalues = []
    strfieldNames = []
    if fields is None:
        fields = xrange(len(values))
    for i in xrange(len(fields)):
        field = db_record.field(i)
        if fields[i] != -1:
            if fields[i] < valuesLen:
                # для корректной загрузки дат
                if isinstance(values[fields[i]], datetime.date):
                    field.setValue(QVariant(QDateTime().fromString(values[fields[i]].isoformat(), 'yyyy-MM-dd')))
                else:
                    field.setValue(QVariant(values[fields[i]]))
            strvalues.append(unicode(db.db.driver().formatValue(field)))
            strfieldNames.append('`%s`'%forceString(field.name()))
    stmt = '%s INTO %s ( %s ) VALUES ( %s )'%(('INSERT IGNORE', 'REPLACE')[mode], tablename, ', '.join(strfieldNames), ', '.join(strvalues))
    querier =  QtSql.QSqlQuery(db.db)
    if not querier.exec_(stmt):
        return querier.lastError()
    return None


def insertTableDataFromDbf(db, tablename, filename, encoding, binaries=[], fields=None, mode=0, errors=0, batch=0):
    u"""
    Выкачивает данные из DBF и добавляет в таблицу БД
    tablename - имя таблицы БД
    filename - имя файла DBF
    encoding - кодировка, в которой хранится DBF
    binaries - список номеров полей, которые нужно перекодировать из бинарных в целые
    fields - номера полей, которые надо конвертировать (None - все поля). Если номер равен -1, нужно вставить значение по умолчанию.
    mode: 0 - IGNORE,
          1 - REPLACE
    errors: 0 - игнорировать
            1 - завершать работу и возвращать ошибку
    batch: количество записей вставляемых за раз (0 - вставка по одной записи)
    """
    dbftable = Dbf(filename, readOnly=True, encoding=encoding, enableFieldNameDups=True)
#    for i in binaries:
#        dbf.fieldDefs[i].encoding = 'latin-1'
    if batch:
        recordList = []
        strfieldNames = []
        db_record = db.record(tablename)

        for record in dbftable:
            for i in binaries:
                record[i] = binaryToInt(record[i])
            values = record.asList()
            valuesLen = len(values)

            # список полей
            if not strfieldNames:
                if fields is None:
                    fields = xrange(len(values))
                for i in xrange(len(fields)):
                    field = db_record.field(i)
                    if fields[i] != -1:
                        strfieldNames.append('`%s`' % forceString(field.name()))
            # список значений
            strvalues = []
            for i in xrange(len(fields)):
                field = db_record.field(i)
                if fields[i] != -1:
                    if fields[i] < valuesLen:
                        # для корректной загрузки дат
                        if isinstance(values[fields[i]], datetime.date):
                            field.setValue(
                                QVariant(QDateTime().fromString(values[fields[i]].isoformat(), 'yyyy-MM-dd')))
                        else:
                            field.setValue(QVariant(values[fields[i]]))
                    strvalues.append(unicode(db.db.driver().formatValue(field)))
            recordList.append('( %s )' % (', '.join(strvalues)))

            if len(recordList) == batch:
                stmt = '%s INTO %s ( %s ) VALUES %s' % (('INSERT IGNORE', 'REPLACE')[mode], tablename, ', '.join(strfieldNames), ', '.join(recordList))
                querier = QtSql.QSqlQuery(db.db)
                if not querier.exec_(stmt):
                    return querier.lastError()
                recordList = []
            QtGui.qApp.processEvents()

        if recordList:
            stmt = '%s INTO %s ( %s ) VALUES %s' % (('INSERT IGNORE', 'REPLACE')[mode], tablename, ', '.join(strfieldNames), ', '.join(recordList))
            querier = QtSql.QSqlQuery(db.db)
            if not querier.exec_(stmt):
                return querier.lastError()
            QtGui.qApp.processEvents()
    else:
        for record in dbftable:
            for i in binaries:
                record[i] = binaryToInt(record[i])
            error = insertRecordFromDbf(db, tablename, record, fields,  mode=mode)
            if errors == 1 and error:
                return error
            QtGui.qApp.processEvents()
    dbftable.close()
    return None


def logMessage(log, str):
    strings = str.split('\n')
    for s in strings:
        log.append(s)


def logQueryResult(log, query):
    u"""Записывает результат выполнения запроса query в лог по строкам"""
    while query.next():
        rec = query.record()
        str = query.value(0).toString()
        for i in xrange(1,  rec.count()):
            str = str + '\t' + query.value(i).toString()
        log.append(str)

def setSqlVariable(db, name, value):
    u"""Устанавливает значение переменной в запросе на SQL"""
    if value:
        if str(type(value)) == "<type 'string'>" or str(type(value)) == "<type 'unicode'>":
            strvalue = '\'' + value + '\''
        else:
            strvalue = str(value)
    else:
        strvalue = 'NULL'
    querier =  QtSql.QSqlQuery(db.db)
    if not querier.exec_('SELECT @' + name + ' := ' + strvalue):
        return querier.lastError()
    return None


def execQuery(db, s, log):
    if QRegExp('[ \n\r\t]*').exactMatch(s): # пустой запрос
        return None
    #print "QUERY: " + s
    querier =  QtSql.QSqlQuery(db.db)
    if not querier.exec_(s):
        return querier.lastError()
    if log:
        logQueryResult(log, querier) # записываем результат выполнения
    return None

def runScript(db, log, instream, dict = {}):
    u"""Выполняет последовательность запросов к базе данных db, считанную из входного потока instream.
    instream - это произвольный контейнер со строками
    Записывает результаты в окно log
    dict - набор пар (имя, значение) для установки переменных в SQL
    """
    # устанавливаем значения переменных:
    for (key,  value) in dict.items():
        setSqlVariable(db, key,  value)

    # анализируем запросы:
    fullstr = '' # текущий запрос
    delimiter = ';' # разделитель запросов
    for str in instream:
        delimexp = QRegExp('delimiter', Qt.CaseInsensitive)
        if delimexp.indexIn(str.strip()) == 0: # в этой строке меняется разделитель
            delimiter = str[delimexp.matchedLength():].strip()
        else:
            pos = QRegExp('--|\'|\"|%s'%QRegExp.escape(delimiter)).indexIn(str, 0) # позиция, с которой начинается комментарий или открывается строка
            while pos != -1:
                if str[pos] == '\'':
                    pos = str.find('\'', pos+1)
                    pos += (1 if pos != -1 else 0)
                elif str[pos] == '\"':
                    pos = str.find('\"', pos+1)
                    pos += (1 if pos != -1 else 0)
                elif str[pos:pos+len(delimiter)] == delimiter: # здесь запрос закончился
                    fullstr = fullstr + ' ' + str[:pos]
                    result = execQuery(db, fullstr, log) # выполняем его
                    if result:
                        return result
                    fullstr = '' # и ждем нового
                    str = str[pos+len(delimiter):]
                    pos = 0
                else: # найден комментарий
                    str = str[:pos]
                    break
                pos = QRegExp('--|\'|\"|%s'%QRegExp.escape(delimiter)).indexIn(str, pos)
            fullstr = fullstr + ' ' + str
    result = execQuery(db, fullstr, log) # выполняем всё, что осталось в конце
    return result

def checkEmail(email):
    reg = '^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$'
    if len(email) > 7:
        if re.match(reg, email):
            return True
    return False

def compressFileInRar(filePath='', rarFilePath=''):
        if not filePath:
            raise CException(u'При сжатии получен пустой адрес сохранения файла')
        if not rarFilePath:
            rarFilePath = filePath+'.rar'
        prg=QtGui.qApp.execProgram(u'rar mf -ep -m5 -o+ -y -- "%s" "%s"'% (rarFilePath, filePath))
        if not prg[0]:
            raise CException(u'не удалось запустить rar')
        if prg[2]:
            raise CException(u'ошибка при выполнении rar')
        return True


def compressFileInArj(filePath, arjFilePath=''):
    if filePath:
        if not arjFilePath:
            arjFilePath = filePath+'.arj'
        prg=QtGui.qApp.execProgram(u'arj m -m4 -y -e "%s" "%s"'% (arjFilePath, filePath))
        if not prg[0]:
            raise CException(u'не удалось запустить arj')
        if prg[2]:
            raise CException(u'ошибка при выполнении arj')
        return True

    return False


def compressFileInZip(filePath, zipFilePath=''):
    if not zipFilePath:
        zipFilePath = filePath+'.zip'

    zf = ZipFile(zipFilePath, 'w', allowZip64=True)
    if (isinstance(filePath, list) or isinstance(filePath, tuple) or
                isinstance(filePath, set)):
        for file in filePath:
            zf.write(file, os.path.basename(file), ZIP_DEFLATED)
    else:
        zf.write(filePath, os.path.basename(filePath), ZIP_DEFLATED)
    zf.close()

    return True


def compressFileIn7Zip(filePath, zipFilePath=''):
    if filePath:
        if not zipFilePath:
            zipFilePath = filePath+'.7z'
        prg=QtGui.qApp.execProgram(u'7za a -y "%s" "%s"'% (zipFilePath, filePath))
        if not prg[0]:
            raise CException(u'не удалось запустить 7za')
        if prg[2]:
            raise CException(u'ошибка при выполнении 7za')
        return True

    return False


def getClientRepresentativeInfo(clientId):
    db = QtGui.qApp.db
    stmt = """
SELECT
    Client.id,
    Client.firstName,
    Client.lastName,
    Client.patrName,
    Client.sex,
    Client.birthDate,
    Client.birthPlace,
    ClientDocument.serial,
    ClientDocument.number,
    ClientDocument.date,
    ClientDocument.origin,
    Client.SNILS,
    rbDocumentType.code AS documentTypeCode,
    rbDocumentType.regionalCode AS documentTypeRegionalCode,
    rbDocumentType.federalCode AS documentTypeFederalCode,
    T.regionalRelationTypeCode AS regionalRelationTypeCode
FROM
    (SELECT rbRelationType.code, ClientRelation.client_id, rbRelationType.regionalReverseCode AS regionalRelationTypeCode
    FROM ClientRelation
    LEFT JOIN rbRelationType ON ClientRelation.relativeType_id = rbRelationType.id
    WHERE ClientRelation.deleted=0
      AND ClientRelation.relative_id = %d
      AND rbRelationType.isDirectRepresentative
    UNION
    SELECT rbRelationType.code, ClientRelation.relative_id AS client_id, rbRelationType.regionalCode AS regionalRelationTypeCode
    FROM ClientRelation
    LEFT JOIN rbRelationType ON ClientRelation.relativeType_id=rbRelationType.id
    WHERE ClientRelation.deleted=0
      AND ClientRelation.client_id = %d
      AND rbRelationType.isBackwardRepresentative
    ) AS T
    LEFT JOIN Client ON T.client_id = Client.id
    LEFT JOIN ClientDocument ON ClientDocument.client_id = Client.id AND
        ClientDocument.id = (SELECT MAX(CD.id)
                        FROM   ClientDocument AS CD
                        LEFT JOIN rbDocumentType AS rbDT ON rbDT.id = CD.documentType_id
                        LEFT JOIN rbDocumentTypeGroup AS rbDTG ON rbDTG.id = rbDT.group_id
                        WHERE  rbDTG.code = '1' AND CD.client_id = Client.id AND CD.deleted=0)
    LEFT JOIN rbDocumentType ON rbDocumentType.id = ClientDocument.documentType_id
WHERE
    Client.deleted = 0
ORDER BY T.code
LIMIT 1
    """ % (clientId, clientId)
    query = db.query(stmt)
    result = {}

    if query.first():
        record=query.record()
        if record:
            result['firstName'] = forceString(record.value('firstName'))
            result['lastName'] = forceString(record.value('lastName'))
            result['patrName'] = forceString(record.value('patrName'))
            result['serial'] = forceString(record.value('serial'))
            result['number'] = forceString(record.value('number'))
            result['date']   = forceDate(record.value('date'))
            result['origin'] = forceString(record.value('origin'))
            result['sex'] = forceInt(record.value('sex'))
            result['birthDate'] = forceDate(record.value('birthDate'))
            result['birthPlace'] = forceString(record.value('birthPlace'))
            result['documentTypeCode'] = forceString(record.value('documentTypeCode'))
            result['documentTypeRegionalCode'] = forceInt(record.value('documentTypeRegionalCode'))
            result['documentTypeFederalCode'] = forceString(record.value('documentTypeFederalCode'))
            result['regionalRelationTypeCode'] = forceString(record.value('regionalRelationTypeCode'))
            result['SNILS'] = forceString(record.value('SNILS'))
            result['id'] = forceRef(record.value('id'))
    return result


def testAccountExchange(func, accNum=None, configFileName='S11App.ini',
                      accountItemIdList=None, isImport=False, eventIdList=None,
                      limit=None):
    u'Запускает приложение в демо режиме, вызывает exportFunc для accountId'

    import sys
    from PyQt4 import QtGui
    from s11main import CS11mainApp, CS11MainWindow

    result = False

    try:
        app = CS11mainApp(sys.argv, True, configFileName, True, True, 'mark')
        QtGui.qApp = app
        app.applyDecorPreferences()
        mainWindow = CS11MainWindow()
        app.mainWindow = mainWindow
        mainWindow.show()
        mainWindow.actLogin.activate(QtGui.QAction.Trigger)

        if app.db:
            mainWindow.statusBar.showMessage(app.db.connectionId)
            mainWindow.menuBar.setVisible(False)
            tblAcccount = app.db.table('Account')
            tblAccountItem = app.db.table('Account_Item')
            if isinstance(accNum, (str, unicode)):
                record = app.db.getRecordEx(tblAcccount, 'id',
                                        tblAcccount['number'].eq(accNum))
                accId = forceRef(record.value(0)) if record else None
            elif isinstance(accNum, int):
                accId = accNum
            else:
                accId = None

            if not accountItemIdList:
                accountItemIdList = []

            if not accountItemIdList and not eventIdList:
                accountItemIdList = app.db.getIdList(
                    tblAccountItem,
                    where=[tblAccountItem['master_id'].eq(accId),
                           tblAccountItem['deleted'].eq(0)], limit=limit)

            if eventIdList:
                accountItemIdList.extend(app.db.getIdList(
                    tblAccountItem,
                    where=[tblAccountItem['event_id'].inlist(eventIdList),
                           tblAccountItem['deleted'].eq(0)], limit=limit))

            if accountItemIdList:
                if not accId:
                    accId = forceRef(app.db.translate(
                        'Account_Item', 'id', accountItemIdList[0],
                        'master_id'))
                if isImport:
                    func(mainWindow, accId, accountItemIdList)
                else:
                    func(mainWindow, accId, accountItemIdList, None)
                result = True
            else:
                print('Account items not found.')

            app.clearUserId(False)
            app.closeDatabase()

        app.doneTrace()

    except Exception as e:
        print e

    QtGui.qApp = None
    print('Test {0}.'.format('ok' if result else 'failed'))
    return result


def testAccountExport(exportFunc, accNum=None, configFileName='S11App.ini',
                      accountItemIdList=None, eventIdList=None, limit=None):
    return testAccountExchange(exportFunc, accNum, configFileName,
                               accountItemIdList, eventIdList=eventIdList,
                               limit=limit)


def testAccountImport(exportFunc, accNum=None, configFileName='S11App.ini',
                      accountItemIdList=None, limit=None):
    return testAccountExchange(exportFunc, accNum, configFileName,
                               accountItemIdList, isImport=True,
                               limit=limit)


def getChecksum(s):

    crc32_table = [
            0x00000000, 0x77073096, 0xee0e612c, 0x990951ba, 0x076dc419, 0x706af48f, 0xe963a535, 0x9e6495a3,
            0x0edb8832, 0x79dcb8a4, 0xe0d5e91e, 0x97d2d988, 0x09b64c2b, 0x7eb17cbd, 0xe7b82d07, 0x90bf1d91,
            0x1db71064, 0x6ab020f2, 0xf3b97148, 0x84be41de, 0x1adad47d, 0x6ddde4eb, 0xf4d4b551, 0x83d385c7,
            0x136c9856, 0x646ba8c0, 0xfd62f97a, 0x8a65c9ec, 0x14015c4f, 0x63066cd9, 0xfa0f3d63, 0x8d080df5,
            0x3b6e20c8, 0x4c69105e, 0xd56041e4, 0xa2677172, 0x3c03e4d1, 0x4b04d447, 0xd20d85fd, 0xa50ab56b,
            0x35b5a8fa, 0x42b2986c, 0xdbbbc9d6, 0xacbcf940, 0x32d86ce3, 0x45df5c75, 0xdcd60dcf, 0xabd13d59,
            0x26d930ac, 0x51de003a, 0xc8d75180, 0xbfd06116, 0x21b4f4b5, 0x56b3c423, 0xcfba9599, 0xb8bda50f,
            0x2802b89e, 0x5f058808, 0xc60cd9b2, 0xb10be924, 0x2f6f7c87, 0x58684c11, 0xc1611dab, 0xb6662d3d,
            0x76dc4190, 0x01db7106, 0x98d220bc, 0xefd5102a, 0x71b18589, 0x06b6b51f, 0x9fbfe4a5, 0xe8b8d433,
            0x7807c9a2, 0x0f00f934, 0x9609a88e, 0xe10e9818, 0x7f6a0dbb, 0x086d3d2d, 0x91646c97, 0xe6635c01,
            0x6b6b51f4, 0x1c6c6162, 0x856530d8, 0xf262004e, 0x6c0695ed, 0x1b01a57b, 0x8208f4c1, 0xf50fc457,
            0x65b0d9c6, 0x12b7e950, 0x8bbeb8ea, 0xfcb9887c, 0x62dd1ddf, 0x15da2d49, 0x8cd37cf3, 0xfbd44c65,
            0x4db26158, 0x3ab551ce, 0xa3bc0074, 0xd4bb30e2, 0x4adfa541, 0x3dd895d7, 0xa4d1c46d, 0xd3d6f4fb,
            0x4369e96a, 0x346ed9fc, 0xad678846, 0xda60b8d0, 0x44042d73, 0x33031de5, 0xaa0a4c5f, 0xdd0d7cc9,
            0x5005713c, 0x270241aa, 0xbe0b1010, 0xc90c2086, 0x5768b525, 0x206f85b3, 0xb966d409, 0xce61e49f,
            0x5edef90e, 0x29d9c998, 0xb0d09822, 0xc7d7a8b4, 0x59b33d17, 0x2eb40d81, 0xb7bd5c3b, 0xc0ba6cad,
            0xedb88320, 0x9abfb3b6, 0x03b6e20c, 0x74b1d29a, 0xead54739, 0x9dd277af, 0x04db2615, 0x73dc1683,
            0xe3630b12, 0x94643b84, 0x0d6d6a3e, 0x7a6a5aa8, 0xe40ecf0b, 0x9309ff9d, 0x0a00ae27, 0x7d079eb1,
            0xf00f9344, 0x8708a3d2, 0x1e01f268, 0x6906c2fe, 0xf762575d, 0x806567cb, 0x196c3671, 0x6e6b06e7,
            0xfed41b76, 0x89d32be0, 0x10da7a5a, 0x67dd4acc, 0xf9b9df6f, 0x8ebeeff9, 0x17b7be43, 0x60b08ed5,
            0xd6d6a3e8, 0xa1d1937e, 0x38d8c2c4, 0x4fdff252, 0xd1bb67f1, 0xa6bc5767, 0x3fb506dd, 0x48b2364b,
            0xd80d2bda, 0xaf0a1b4c, 0x36034af6, 0x41047a60, 0xdf60efc3, 0xa867df55, 0x316e8eef, 0x4669be79,
            0xcb61b38c, 0xbc66831a, 0x256fd2a0, 0x5268e236, 0xcc0c7795, 0xbb0b4703, 0x220216b9, 0x5505262f,
            0xc5ba3bbe, 0xb2bd0b28, 0x2bb45a92, 0x5cb36a04, 0xc2d7ffa7, 0xb5d0cf31, 0x2cd99e8b, 0x5bdeae1d,
            0x9b64c2b0, 0xec63f226, 0x756aa39c, 0x026d930a, 0x9c0906a9, 0xeb0e363f, 0x72076785, 0x05005713,
            0x95bf4a82, 0xe2b87a14, 0x7bb12bae, 0x0cb61b38, 0x92d28e9b, 0xe5d5be0d, 0x7cdcefb7, 0x0bdbdf21,
            0x86d3d2d4, 0xf1d4e242, 0x68ddb3f8, 0x1fda836e, 0x81be16cd, 0xf6b9265b, 0x6fb077e1, 0x18b74777,
            0x88085ae6, 0xff0f6a70, 0x66063bca, 0x11010b5c, 0x8f659eff, 0xf862ae69, 0x616bffd3, 0x166ccf45,
            0xa00ae278, 0xd70dd2ee, 0x4e048354, 0x3903b3c2, 0xa7672661, 0xd06016f7, 0x4969474d, 0x3e6e77db,
            0xaed16a4a, 0xd9d65adc, 0x40df0b66, 0x37d83bf0, 0xa9bcae53, 0xdebb9ec5, 0x47b2cf7f, 0x30b5ffe9,
            0xbdbdf21c, 0xcabac28a, 0x53b39330, 0x24b4a3a6, 0xbad03605, 0xcdd70693, 0x54de5729, 0x23d967bf,
            0xb3667a2e, 0xc4614ab8, 0x5d681b02, 0x2a6f2b94, 0xb40bbe37, 0xc30c8ea1, 0x5a05df1b, 0x2d02ef8d
        ]

    def get_crc(text, j):
        
        result = 0xFFFFFFFF
        for i in range(j):
            result = ((result >> 8) & 0x00FFFFFF) ^ crc32_table[(result ^ text[i]) & 0xFF]
        result ^= 0xFFFFFFFF
        return result

    with open(s, 'rb') as f:
        buf = bytearray(f.read())
        checksum = get_crc(buf, len(buf))
        
    return hex(checksum).upper()[2:-1].zfill(8)