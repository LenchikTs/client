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


from Events.ActionStatus import CActionStatus


from library.blmodel.Model import CModel, CDocumentModel
from library.blmodel.ModelAttribute import (
    CIntAttribute, CStringAttribute, CDateTimeAttribute, CDateAttribute, CRefAttribute,
    CTimeAttribute, CBooleanAttribute
)
from library.blmodel.ModelRelationship import CRelationship

from library.blmodel.Query import CQuery


class CJob(CDocumentModel):
    tableName = 'Job'

    jobType_id = CRefAttribute()
    jobPurpose_id = CRefAttribute()
    orgStructure_id = CRefAttribute()
    date = CDateAttribute()
    begTime = CTimeAttribute()
    endTime = CTimeAttribute()
    quantity = CIntAttribute()
    capacity = CIntAttribute()



class CJobTicket(CModel):
    tableName = 'Job_Ticket'

    deleted = CBooleanAttribute()
    master_id = CRefAttribute()
    idx = CIntAttribute()
    pass_ = CIntAttribute(name='pass')
    datetime = CDateTimeAttribute()
    resTimestamp = CDateTimeAttribute()
    resConnectionId = CIntAttribute()
    status = CIntAttribute()
    begDateTime = CDateTimeAttribute()
    endDateTime = CDateTimeAttribute()
    orgStructure_id = CRefAttribute()
    note = CStringAttribute(length=128)
    isExceedQuantity = CBooleanAttribute()
    masterJobTicket_id = CRefAttribute()

    job = CRelationship(CJob, 'master_id')

    @staticmethod
    def _getActionsQuery(jobTickerId, hideDoneActions=False):
        db = QtGui.qApp.db

        table = db.table('Job_Ticket')
        tableAPJT = db.table('ActionProperty_Job_Ticket')
        tableAP = db.table('ActionProperty')
        tableAction = db.table('Action')
        tableActionType = db.table('ActionType')
        tableEvent = db.table('Event')
        tableClient = db.table('Client')
        queryTable = table
        queryTable = queryTable.leftJoin(tableAPJT, tableAPJT['value'].eq(table['id']))
        queryTable = queryTable.leftJoin(tableAP, tableAP['id'].eq(tableAPJT['id']))
        queryTable = queryTable.leftJoin(tableAction, tableAction['id'].eq(tableAP['action_id']))
        queryTable = queryTable.leftJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
        queryTable = queryTable.leftJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))
        queryTable = queryTable.leftJoin(tableClient, tableClient['id'].eq(tableEvent['client_id']))

        cond = [table['id'].eq(jobTickerId),
                tableAction['deleted'].eq(0),
                tableEvent['deleted'].eq(0),
                tableClient['deleted'].eq(0),
                ]

        if hideDoneActions:
            cond.append(tableAction['status'].inlist([CActionStatus.started,
                                                      CActionStatus.appointed,
                                                      CActionStatus.withoutResult]))

        return CQuery(None, queryTable, where=cond)

    def getActionIdList(self, hideDoneActions=False):
        query = self._getActionsQuery(self.id, hideDoneActions)
        return query.orderBy('Action.id').getDistinctIdList('Action.id')

    def getEventExternalIdList(self):
        query = self._getActionsQuery(self.id)
        result = query.orderBy('Event.id').getDistinctStringValues('Event.externalId')
        return [v for v in result if v]
