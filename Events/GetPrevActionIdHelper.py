#!/usr/bin/env python
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

from library.Utils import forceDate, forceRef


class CGetPrevActionIdHelper(object):
    ownPrevAction            = 0
    sameSpecialityPrevAction = 1
    anyPrevAction            = 2

    def __init__(self, eventEditor=None):
        self.prevActionIdCache = {}
        self._eventEditor = eventEditor
        self._clientId = None


    def setClientId(self, clientId):
        self._clientId = clientId

    def getPersonIdAndDate(self, action):
        actionPersonId = forceRef(action.getRecord().value('person_id'))
        if actionPersonId:
            personId = actionPersonId
        elif QtGui.qApp.userSpecialityId:
            personId = QtGui.qApp.userId
        else:
            personId = forceRef(action.getRecord().value('setPerson_id'))

        actionEndDate = forceDate(action.getRecord().value('endDate'))
        if actionEndDate:
            date = actionEndDate
        else:
            date = forceDate(action.getRecord().value('directionDate'))

        return personId, date


    def getClientId(self):
        if self._eventEditor:
            return self._eventEditor.clientId
        else:
            return self._clientId



    def getPrevActionId(self, action, type):
        actionTypeId = action.getType().id
        actionId = forceRef(action.getRecord().value('id')) if action.getRecord() else None
        personId, date = self.getPersonIdAndDate(action)
        key = (actionTypeId, actionId, personId, type, date.toPyDate())
        if key in self.prevActionIdCache:
            return self.prevActionIdCache[key]
        else:
            result = self.findPrevActionId(actionTypeId, actionId, personId, type, date)
            self.prevActionIdCache[key] = result
            return result


    def findPrevActionId(self, actionTypeId, actionId, personId, type, date):
        db = QtGui.qApp.db
        tableEvent  = db.table('Event')
        tableAction = db.table('Action')
        tableActionTypeTestator = db.table('ActionType_Testator')
        table = tableAction.leftJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))
        table = table.leftJoin(tableActionTypeTestator,
                               tableActionTypeTestator['testator_id'].eq(tableAction['actionType_id']))

        cond = [tableAction['deleted'].eq(0),
                tableEvent['deleted'].eq(0),
                db.joinOr([tableAction['actionType_id'].eq(actionTypeId),
                           tableActionTypeTestator['master_id'].eq(actionTypeId)
                          ]
                         ),
                tableEvent['client_id'].eq(self.getClientId())
               ]

        if type == CGetPrevActionIdHelper.ownPrevAction:
            cond.append(tableAction['endDate'].lt(date.addDays(1)))
            cond.append(tableAction['person_id'].eq(personId))
            field = tableAction['id'].name()
        elif type == CGetPrevActionIdHelper.sameSpecialityPrevAction:
            tablePerson = db.table('Person')
            tablePerson2 = db.table('Person').alias('Person2')
            table = table.leftJoin(tablePerson, tablePerson['id'].eq(tableAction['person_id']))
            table = table.leftJoin(tablePerson2, tablePerson2['speciality_id'].eq(tablePerson['speciality_id']))
            cond.append(tablePerson2['id'].eq(personId))
            cond.append(tableAction['endDate'].lt(date.addDays(1)))
            field = tableAction['id'].name()
        elif type == CGetPrevActionIdHelper.anyPrevAction:
            cond.append(tableAction['endDate'].lt(date.addDays(1)))
            field = tableAction['id'].name()
        else:
            return None

        if actionId:
            cond.append(tableAction['id'].ne(actionId))

        idList = db.getIdList(table,
                              field,
                              cond,
                              '%s DESC, %s DESC' % (tableAction['endDate'].name(),
                                                    tableAction['id'].name()
                                                   ),
                              1)
        if idList:
            return idList[0]
        else:
            return None
