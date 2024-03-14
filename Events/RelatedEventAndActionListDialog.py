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

from library.DialogBase import CDialogBase
from Registry.AmbCardMixin import CAmbCardMixin

from Ui_RelatedEventAndActionListDialog import Ui_RelatedEventAndActionListDialog


class CRelatedEventAndActionListDialog(CDialogBase, CAmbCardMixin, Ui_RelatedEventAndActionListDialog):
    def __init__(self, parent, eventId, prevEventId=None):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)

        self.tabEvents.eventEditor = parent
        self.tabActions.eventEditor = parent

        existsActionList = []

        for actionsTab in parent.getActionsTabsList():
            for item in actionsTab.tblAPActions.model().items():
                record, action = item
                actionId = action.getId()
                if actionId:
                    existsActionList.append(actionId)

        self.tabEvents.tblRelatedEventList.model().loadData(eventId, prevEventId)

        self.tabActions.tblRelatedActionList.model().setExistsActionList(existsActionList)
        self.tabActions.tblRelatedActionList.model().setCurrentEventId(eventId)
        self.tabActions.tblRelatedActionList.model().setClientId(parent.clientId)
        self.tabActions.tblRelatedActionList.model().loadData()
