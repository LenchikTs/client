# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

u'''Статусы закрытия элементов Курса'''


from library.ROComboBox import CEnumComboBox

class CCourseStatus:
    names = (u'Продолжить',                 # 0
             u'Пропустить (отказ пациента)',# 1
             u'Пропустить (отмена МО)',     # 2
             u'Завершить (отказ пациента)', # 3
             u'Завершить (отмена МО)',      # 4
            )

    proceed             = 0
    skipRefusalClient   = 1
    skipRefusalMO       = 2
    finishRefusalClient = 3
    finishRefusalMO     = 4


    @staticmethod
    def text(status):
        if status is None:
            return u'не задано'
        if 0 <= status < len(CCourseStatus.names):
            return CCourseStatus.names[status]
        else:
            return u'{%s}' % status


class CCourseStatusComboBox(CEnumComboBox):
    def __init__(self, parent):
        CEnumComboBox.__init__(self, parent)
        for i, name in enumerate(CCourseStatus.names):
            self.addItem(name, i)

