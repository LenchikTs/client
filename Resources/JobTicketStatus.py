# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

u'''Статусы Job-ticket-a'''


from library.ROComboBox import CEnumComboBox

class CJobTicketStatus:
    names = (u'Ожидание',       # 0
             u'Выполнение',     # 1
             u'Закончено',      # 2
             u'В очереди',      # 3
            )

    wait          = 0
    doing         = 1
    done          = 2
    enqueued      = 3 # ready?


    @staticmethod
    def text(status):
        if status is None:
            return u'не задано'
        if 0<=status<len(CJobTicketStatus.names):
            return CJobTicketStatus.names[status]
        else:
            return u'{%s}' % status


class CJobTicketStatusComboBox(CEnumComboBox):
    def __init__(self, parent):
        CEnumComboBox.__init__(self, parent)
        for i, name in enumerate(CJobTicketStatus.names):
            self.addItem(name, i)
