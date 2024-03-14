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
from Events.ActionProperty.NomenclatureActionPropertyValueType import CNomenclatureActionPropertyValueType


def getNomenclatureActionTypesIds():
    db = QtGui.qApp.db

    tableActionType = db.table('ActionType')
    tableActionPropertyType = db.table('ActionPropertyType')

    queryTable = tableActionType.innerJoin(
        tableActionPropertyType, tableActionPropertyType['actionType_id'].eq(tableActionType['id'])
    )

    cond = [
        tableActionType['deleted'].eq(0),
        tableActionPropertyType['deleted'].eq(0),
        tableActionPropertyType['typeName'].eq(CNomenclatureActionPropertyValueType.name)
    ]

    return db.getIdList(queryTable, tableActionType['id'], cond)
