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
from library.Utils import forceInt, forceString


def parseModel(model):
    result = []
    # model as string -> list of tuples (title, value)
    db = QtGui.qApp.db
    modelCodes = model.split('.')
    modelItems = db.getRecordList('mes.ModelDescription', ['name', 'fieldIdx', 'tableName'], order='idx')
    for item in modelItems:
        name = forceString(item.value('name'))
        fieldIdx = forceInt(item.value('fieldIdx'))
        tableName = forceString(item.value('tableName'))
        if 0<=fieldIdx<len(modelCodes):
            code = modelCodes[fieldIdx]
            value = db.translate(tableName,'code',code,'name')
            if value:
                value = forceString(value)
            else:
                value = u'{%s}' % code
        else:
            value = ''
        result.append((name,value))
    return result