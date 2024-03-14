# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from library.DbComboBox import CDbComboBox


class CAccountComboBox(CDbComboBox):

    def __init__(self, parent):
        CDbComboBox.__init__(self, parent)
        self.setTable('Account', nameField=u"concat_ws(' ', number, 'от', DATE_FORMAT(date,'%d.%m.%Y'), "
                      u"(select OrgStructure.code from OrgStructure where OrgStructure.id = Account.orgStructure_id))",
                      order=['date', 'number'])
        self.setAddNone(True, u'не задано')
        self.updateFilter()

    def updateFilter(self, begDate=None, endDate=None, orgStruct=None, contract=None, finance=None):
        db = QtGui.qApp.db
        value = self.value()
        cond = ['Account.deleted = 0']
        if begDate and endDate:
            cond.append('Account.date between %s and %s' % (db.formatDate(begDate), db.formatDate(endDate)))
        elif begDate:
            cond.append('Account.date >= %s' % db.formatDate(begDate))
        elif endDate:
            cond.append('Account.date <= %s' % db.formatDate(endDate))
        if orgStruct:
            cond.append('Account.orgStructure_id = %s' % orgStruct)
        if contract:
            cond.append('Account.contract_id = %s' % contract)
        elif finance:
            cond.append('Account.contract_id in (SELECT id FROM Contract where finance_id = %s)' % finance)
        self.setFilter(db.joinAnd(cond))
        self.setValue(value)
