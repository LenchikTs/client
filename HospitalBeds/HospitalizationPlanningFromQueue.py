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

from PyQt4.QtCore import pyqtSignature

from Events.ActionEditDialog    import CActionEditDialog
from Events.CreateEvent         import requestNewEvent
from HospitalizationEventDialog import CHospitalizationEventDialog

class CHospitalizationPlanningFromQueue(CHospitalizationEventDialog):
    def __init__(self, parent):
        CHospitalizationEventDialog.__init__(self, parent)


    @pyqtSignature('')
    def on_actCreateEvent_triggered(self):
        self.requestNewEvent()


    def requestNewEvent(self):
        self.newEventId = None
        clientId = self.getCurrentClientId()
        if clientId:
            btnAction, actionId = self.checkPlanningOpenEvents(clientId)
            if btnAction == 1 and actionId:
                self.close()
                dialog = CActionEditDialog(self)
                try:
                    dialog.load(actionId)
                    if dialog.exec_():
                        pass
                finally:
                    dialog.deleteLater()
                return None
            elif btnAction == 0:
                return None
        self.close()
        if clientId:
            self.selectHospitalizationEventCode(clientId)
            params = {}
            params['widget'] = self
            params['clientId'] = clientId
            params['flagHospitalization'] = True
            params['actionTypeId'] = None
            params['valueProperties'] = [None, None]
            params['eventTypeFilterHospitalization'] = 4
            self.newEventId = requestNewEvent(params)
            return self.newEventId
        return None

