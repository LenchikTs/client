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

u'''Статусы Action-a'''

from PyQt4.QtCore import QVariant

from library.ROComboBox         import CEnumComboBox
from library.ROComboBox         import CROComboBox
from library.MultivalueComboBox import CBaseMultivalue


class CActionStatus:
    names = (u'Начато',         # 0
             u'Ожидание',       # 1
             u'Закончено',      # 2
             u'Отменено',       # 3
             u'Без результата', # 4
             u'Назначено',      # 5
             u'Отказ',          # 6
            )

    started       = 0
    wait          = 1
    finished      = 2
    canceled      = 3
    withoutResult = 4
    appointed     = 5
    refused       = 6


    @staticmethod
    def text(status):
        if status is None:
            return u'не задано'
        if 0<=status<len(CActionStatus.names):
            return CActionStatus.names[status]
        else:
            return u'{%s}' % status


class CActionStatusComboBox(CEnumComboBox):
    def __init__(self, parent):
        CEnumComboBox.__init__(self, parent)
        for i, name in enumerate(CActionStatus.names):
            self.addItem(name, i)


class CActionStatusMultivalueComboBox(CBaseMultivalue, CROComboBox):
    def __init__(self, parent=None):
        CROComboBox.__init__(self, parent)
        CBaseMultivalue.__init__(self)
        self.addItems(CActionStatus.names)


    def insertSpecialValue(self, name, value, idx=0):
        self.insertItem(idx, name, QVariant(value))


    def setText(self, value):
        self.setValue(value)


    def setValue(self, value):
        self._popupView.setCheckedRows(value)
        self.setEditable(True)


    def value(self):
        return self._popupView.getCheckedRows()


    def text(self):
        return unicode(self.currentText())

