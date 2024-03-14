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

u'''Статусы TakenTissueJournal-a'''


from Events.ActionStatus import CActionStatus

class CTissueStatus:
    names = (u'В работе',       # 0
            ) + CActionStatus.names

    inProcess     = 0
    started       = CActionStatus.started+1
    wait          = CActionStatus.wait+1
    finished      = CActionStatus.finished+1
    canceled      = CActionStatus.canceled+1
    withoutResult = CActionStatus.canceled+1
    refused       = CActionStatus.refused+1

    @staticmethod
    def text(status):
        if status is None:
            return u'Не задано'
        if 0<=status<len(CTissueStatus.names):
            return CTissueStatus.names[status]
        else:
            return u'{%s}' % status


    @staticmethod
    def fromActionStatus(status):
        if 0<=status<len(CActionStatus.names):
            return status+1
        else:
            return CTissueStatus.inProcess



#class CTissueComboBox(CEnumComboBox):
#    def __init__(self, parent):
#        CEnumComboBox.__init__(self, parent)
#        for i, name in enumerate(CTissueStatus.names):
#            self.addItem(name, i)

