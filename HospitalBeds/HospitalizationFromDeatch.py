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

from Events.CreateEvent         import requestNewEvent
from HospitalizationFromQueue   import CHospitalizationFromQueue


class CHospitalizationFromDeatch(CHospitalizationFromQueue):
    def requestNewEvent(self):
        self.close()
        self.newEventId = None
        if self.clientId and self.eventId:
            params = {}
            params['widget'] = self
            params['clientId'] = self.clientId
            params['flagHospitalization'] = False
            params['actionTypeId'] = None
            params['valueProperties'] = [None, None]
            params['eventTypeFilterHospitalization'] = 3
            params['diagnos'] = self.getDiagnosString(self.eventId)
            self.newEventId = requestNewEvent(params)
            return self.newEventId
        return None

