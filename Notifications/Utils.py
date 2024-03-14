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
u"""Вспомогательные классы и функции"""

from library.DbComboBox import CDbComboBox


class CNotificationRuleComboBox(CDbComboBox):
    nameField = 'name'
    filter = ''
    def __init__(self, parent):
        CDbComboBox.__init__(self, parent)
        self.setNameField(CNotificationRuleComboBox.nameField)
        self.setAddNone(True)
        self.setFilter(CNotificationRuleComboBox.filter)
        self.setTable('Notification_Rule')
