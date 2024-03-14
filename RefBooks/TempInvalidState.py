# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

u'''Состояние эпизода временной нетрудоспособности'''

from library.ROComboBox import CEnumComboBox

class CTempInvalidState:
    names = (u'Открыт',         # 0
             u'Закрыт',         # 1
             u'Продлён',        # 2
             u'Передан',        # 3
             u'Аннулирован',    # 4
            )

    opened        = 0
    closed        = 1
    extended      = 2
    prolonged     = 2
    transferred   = 3
    annulled      = 4

    @staticmethod
    def text(state):
        if state is None:
            return u'не задано'
        if 0<=state<len(CTempInvalidState.names):
            return CTempInvalidState.names[state]
        else:
            return u'{%s}' % state


class CTempInvalidStateComboBox(CEnumComboBox):
    def __init__(self, parent):
        CEnumComboBox.__init__(self, parent)
        for i, name in enumerate(CTempInvalidState.names):
            self.addItem(name, i)
