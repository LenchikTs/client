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

class CEventSelect:
    createDatetime, createPerson_id, setDate, execDate, execPerson_id = range(5)

class CMainSelect:
    clientId, eventId, code, neededCount, isUpdate = range(5)
    value = u"""
select
  events.clientId,
  events.eventId,
  mes.mrbService.code,
  mes.MES_service.averageQnt as neededCount,
  (select
    case
       when count(*) = 0 then 0
       when count(*) = 1 then 1
     end
   from Event e
     left join Action on Action.event_id = e.id
     left join ActionType on ActionType.id = Action.actionType_id
   where e.id = events.eventId and
         ActionType.code = mes.mrbService.code) as isUpdate
from (select
        Event.id as eventId,
        Event.client_id as clientId,
        Event.mes_id as mesId
      from Account
        left join Account_Item on Account_Item.master_id = Account.id
        left join Event on Event.id = Account_Item.event_id
      where trim(Account.number) = trim('%s') and
            Event.mesSpecification_id = 1 -- 1-МЭС выполнен полностью
      group by Event.id, Event.client_id) as events
  left join mes.MES on mes.MES.id = events.mesId
  left join mes.MES_service on mes.MES_service.master_id = mes.MES.id
  left join mes.mrbService on mes.mrbService.id = mes.MES_service.service_id
where abs(mes.MES_service.necessity - 1.0) < 0.0001
      and not exists(select *
                     from Event e
                       left join Action on Action.event_id = e.id
                       left join ActionType on ActionType.id = Action.actionType_id
                     where e.id = events.eventId
                           and ActionType.code = mes.mrbService.code
                           and Action.amount >= mes.MES_service.averageQnt)
order by events.clientId, events.eventId, mes.mrbService.code;
"""