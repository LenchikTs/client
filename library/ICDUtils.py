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
u'Разные функции для работы с кодами МКБ'

from PyQt4 import QtGui

from library.Utils import forceRef, forceString, forceInt


def MKBwithoutSubclassification(code):
    code = code[:5].strip()
    if code.endswith('.'):
        code = code[:-1]
    return code


def getMKBName(code):
    mainCode = MKBwithoutSubclassification(code)
    subclass = code[5:]
    db = QtGui.qApp.db
    table = db.table('MKB')
    record = db.getRecordEx(table, 'DiagName, MKBSubclass_id', table['DiagID'].eq(mainCode))
    if record:
        result = forceString(record.value(0))
        if subclass:
            subclassId = forceRef(record.value(1))
            tableSubclass = db.table('rbMKBSubclass_Item')
            cond = [tableSubclass['master_id'].eq(subclassId), tableSubclass['code'].eq(subclass)]
            recordSubclass = db.getRecordEx(tableSubclass, 'name', cond)
            if recordSubclass:
                result = result + ', ' + forceString(recordSubclass.value(0))
            else:
                result = result + ' {%s}'%subclass
    else:
        result = '{%s}' % code
    return result


def getMKBBlockName(code):
    mainCode = MKBwithoutSubclassification(code)
    db = QtGui.qApp.db
    table = db.table('MKB')
    record = db.getRecordEx(table, 'DiagName, BlockName', table['DiagID'].eq(mainCode))
    if record:
        result = forceString(record.value(1))
    else:
        result = ''
    return result


def getMKBClassName(code):
    mainCode = MKBwithoutSubclassification(code)
    db = QtGui.qApp.db
    table = db.table('MKB')
    record = db.getRecordEx(table, 'DiagName, ClassName', table['DiagID'].eq(mainCode))
    if record:
        result = forceString(record.value(1))
    else:
        result = ''
    return result

def getMKBC_Id(code):
    mainCode = MKBwithoutSubclassification(code)
    db = QtGui.qApp.db
    table = db.table('MKB')
    record = db.getRecordEx(table, 'id', table['DiagID'].eq(mainCode))
    if record:
        result = forceInt(record.value(0))
    else:
        result = ''
    return result

