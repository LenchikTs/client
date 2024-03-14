# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2016 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui

from library.Utils import forceRef, forceString, forceDate
from library.exception import CException


class CIdentificationException(CException):
    pass


def getIdentification(tableName, id, urn, raiseIfNonFound=True):
    u'получить идентификатор записи таблицы tableName c заданным id в справочнике с заданным urn'
    value, version = getIdentificationEx(tableName, id, urn, raiseIfNonFound)
    return value


def getIdentificationByCode(tableName, id, code, raiseIfNonFound=True):
    u"""Получить идентификатор записи таблицы tableName c заданным id в справочнике с заданным urn"""
    value, version = getIdentificationByCodeEx(tableName, id, code, raiseIfNonFound)
    return value


def getIdentificationByCodeEx(tableName, id, code, raiseIfNonFound=True):
    u"""Получить идентификатор и версию записи таблицы tableName c заданным id в справочнике с заданным urn"""
    db = QtGui.qApp.db
    identificationTableName = tableName + '_Identification'
    tableIdentification = db.table(identificationTableName)
    tableAccountingSystem = db.table('rbAccountingSystem')
    table = tableIdentification.innerJoin(tableAccountingSystem,
                                          tableAccountingSystem['id'].eq(tableIdentification['system_id'])
                                          )
    recordList = db.getRecordList(table,
                                  [tableIdentification['value'],
                                   tableAccountingSystem['version']
                                   ],
                                  [tableIdentification['deleted'].eq(0),
                                   tableIdentification['master_id'].eq(id),
                                   tableAccountingSystem['code'].eq(code)
                                   ],
                                  [tableIdentification['id'].name() + ' DESC'],
                                  1
                                  )
    if recordList:
        record = recordList[0]
        value   = forceString(record.value('value'))
        version = forceString(record.value('version'))
        return value, version
    QtGui.qApp.log(u'Поиск идентификатора', u'Для %s.id=%s не задан код в системе %s' % (tableName, id, code))
    if raiseIfNonFound:
        raise Exception(u'Для %s.id=%s не задан код в системе %s' % (tableName, id, code))
    return None, None


def getIdentificationEx(tableName, id, urn, raiseIfNonFound=True):
    u'получить идентификатор и версию записи таблицы tableName c заданным id в справочнике с заданным urn'
    db = QtGui.qApp.db
    identificationTableName = tableName + '_Identification'
    tableIdentification = db.table(identificationTableName)
    tableAccountingSystem = db.table('rbAccountingSystem')
    table = tableIdentification.innerJoin(tableAccountingSystem,
                                          tableAccountingSystem['id'].eq(tableIdentification['system_id'])
                                         )
    recordList = db.getRecordList(table,
                                  [ tableIdentification['value'],
                                    tableAccountingSystem['version']
                                  ],
                                  [ tableIdentification['deleted'].eq(0),
                                    tableIdentification['master_id'].eq(id),
                                    tableAccountingSystem['urn'].eq(urn)
                                  ],
                                  [ tableIdentification['id'].name() + ' DESC' ],
                                  1
                                 )
    if recordList:
        record = recordList[0]
        value   = forceString(record.value('value'))
        version = forceString(record.value('version'))
        return value, version
    # QtGui.qApp.log(u'Поиск идентификатора', u'Для %s.id=%s не задан код в системе %s' % (tableName, id, urn))
    if raiseIfNonFound:
        raise CIdentificationException(u'Для %s.id=%s не задан код в системе %s' % (tableName, id, urn))
    return None, None

def getIdentificationInfo(tableName, id, urn, byCode=False):
    u'Получить идентификатор и версию записи таблицы tableName c заданным id в справочнике с заданным urn'
    db = QtGui.qApp.db
    identificationTableName = tableName + '_Identification'
    tableIdentification = db.table(identificationTableName)
    tableAccountingSystem = db.table('rbAccountingSystem')
    table = tableIdentification.innerJoin(tableAccountingSystem,
                                          tableAccountingSystem['id'].eq(tableIdentification['system_id'])
                                          )
    cols = [tableAccountingSystem['code'],
            tableAccountingSystem['name'],
            tableAccountingSystem['urn'],
            tableAccountingSystem['version'],
            tableIdentification['value'],
            tableIdentification['note'],
            tableIdentification['checkDate']
            ]
    cond = [tableIdentification['deleted'].eq(0),
            tableIdentification['master_id'].eq(id)
            ]
    if byCode:
        cond.append(tableAccountingSystem['code'].eq(urn))
    else:
        cond.append(tableAccountingSystem['urn'].eq(urn))

    record = db.getRecordEx(table, cols, cond, [tableIdentification['id'].name() + ' DESC'])
    if record:
        code = forceString(record.value('code'))
        name = forceString(record.value('name'))
        urn = forceString(record.value('urn'))
        version = forceString(record.value('version'))
        value = forceString(record.value('value'))
        note = forceString(record.value('note'))
        checkDate = forceDate(record.value('checkDate'))
        return code, name, urn, version, value, note, checkDate
    return None, None, None, None, None, None, None

def getIdentificationInfoList(tableName, id, urn, byCode=False):
    u'Получить идентификатор и версию записи таблицы tableName c заданным id в справочнике с заданным urn'
    db = QtGui.qApp.db
    identificationTableName = tableName + '_Identification'
    tableIdentification = db.table(identificationTableName)
    tableAccountingSystem = db.table('rbAccountingSystem')
    table = tableIdentification.innerJoin(tableAccountingSystem,
                                          tableAccountingSystem['id'].eq(tableIdentification['system_id'])
                                          )
    cols = [tableAccountingSystem['code'],
            tableAccountingSystem['name'],
            tableAccountingSystem['urn'],
            tableAccountingSystem['version'],
            tableIdentification['value'],
            tableIdentification['note'],
            tableIdentification['checkDate']
            ]
    cond = [tableIdentification['deleted'].eq(0),
            tableIdentification['master_id'].eq(id)
            ]
    if byCode:
        cond.append(tableAccountingSystem['code'].eq(urn))
    else:
        cond.append(tableAccountingSystem['urn'].eq(urn))

    record = db.getRecordList(table, cols, cond, [tableIdentification['id'].name() + ' DESC'])

    return record

def getIdentificationInfoById(tableName, _id):
    u'Получить идентификатор c заданным id'
    db = QtGui.qApp.db
    identificationTableName = tableName + '_Identification'
    tableIdentification = db.table(identificationTableName)
    tableAccountingSystem = db.table('rbAccountingSystem')
    table = tableIdentification.innerJoin(tableAccountingSystem,
                                          tableAccountingSystem['id'].eq(tableIdentification['system_id'])
                                          )
    cols = [tableAccountingSystem['code'],
            tableAccountingSystem['name'],
            tableAccountingSystem['urn'],
            tableAccountingSystem['version'],
            tableIdentification['value'],
            tableIdentification['note'],
            tableIdentification['checkDate']
            ]
    cond = [tableIdentification['deleted'].eq(0),
            tableIdentification['id'].eq(_id)
            ]

    record = db.getRecordEx(table, cols, cond, [tableIdentification['id'].name() + ' DESC'])
    if record:
        code = forceString(record.value('code'))
        name = forceString(record.value('name'))
        urn = forceString(record.value('urn'))
        version = forceString(record.value('version'))
        value = forceString(record.value('value'))
        note = forceString(record.value('note'))
        checkDate = forceDate(record.value('checkDate'))
        return code, name, urn, version, value, note, checkDate
    return None, None, None, None, None, None, None


def getIdentificationRecords(tableName, cols, urn, value, limit=None):
    u'получить записи идентификации с заданным кодом в справочнике с заданным urn'
    db = QtGui.qApp.db
    tableIdentification = db.table(tableName + '_Identification')
    tableAccountingSystem = db.table('rbAccountingSystem')
    table = tableIdentification.innerJoin(tableAccountingSystem,
                                          tableAccountingSystem['id'].eq(tableIdentification['system_id'])
                                         )
    recordList = db.getRecordList(table,
                                  cols,
                                  [ tableIdentification['deleted'].eq(0),
                                    tableAccountingSystem['urn'].eq(urn),
                                    tableIdentification['value'].eq(value)
                                  ],
                                  tableIdentification['id'].name() + ' DESC',
                                  limit
                                 )
    return recordList



def findByIdentification(tableName, urn, value, raiseIfNonFound=True):
    u'получить id записи таблицы tableName c заданным кодом в справочнике с заданным urn'
    records = getIdentificationRecords(tableName, 'master_id', urn, value, 1)
    if records:
        return forceRef(records[0].value('master_id'))

    if raiseIfNonFound:
        raise CIdentificationException(u'Для %s в системе %s не найден код %s' % (tableName, urn, value))

    return None


def addIdentification(tableName, id, urn, value):
    db = QtGui.qApp.db
    tableIdentification = db.table(tableName + '_Identification')
    systemId = db.translate('rbAccountingSystem', 'urn', urn, 'id')
    if not systemId:
        raise Exception('rbAccountingSystem with urn=%r not found' % urn)

    record = tableIdentification.newRecord()
    record.setValue('master_id', id)
    record.setValue('system_id', systemId)
    record.setValue('value', value)
    db.insertRecord(tableIdentification, record)
