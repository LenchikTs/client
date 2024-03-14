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

u'''Типы (в интерфейсе - виды) услуг в действиях '''

from PyQt4.QtCore import QVariant
#from PyQt4 import QtGui

from library.ROComboBox import CEnumComboBox


class CActionServiceType:

    names = (u'Прочее',                    # 0
             u'Первичный осмотр',          # 1
             u'Повторный осмотр',          # 2
             u'Процедура/манипуляция',     # 3
             u'Операция',                  # 4
             u'Исследование',              # 5
             u'Лечение',                   # 6
             u'Профилактика',              # 7
             u'Анестезия',                 # 8
             u'Реанимация',                # 9
             u'Лабораторное исследование', # 10
             u'Опрос',                     # 11
            )

    other             = 0
    initialInspection = 1
    reinspection      = 2
    procedure         = 3
    operation         = 4
    research          = 5
    healing           = 6
    prophylaxis       = 7
    anesthesia        = 8
    reanimation       = 9
    labResearch       = 10
    survey            = 11

    @staticmethod
    def text(serviceType):
        if serviceType is None:
            return u'не задано'
        if 0<=serviceType<len(CActionServiceType.names):
            return CActionServiceType.names[serviceType]
        else:
            return u'{%s}' % serviceType


class CActionServiceTypeComboBox(CEnumComboBox):
    def __init__(self, parent):
        CEnumComboBox.__init__(self, parent)
        for i, name in enumerate(CActionServiceType.names):
            self.addItem(name, QVariant(i))


    # insertSpecialValue предназначен для вызыва из конструктора формы,
    # при вызове комбо-бокс insertItem выпускает сигнал currentIndexChanged,
    # и это совершенно излишне...
    def insertSpecialValue(self, name, value, idx=0):
        bs = self.blockSignals(True)
        try:
            CEnumComboBox.insertItem(self, idx, name, value)
            self.setCurrentIndex(0)
        finally:
            self.blockSignals(bs)

