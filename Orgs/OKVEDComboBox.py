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

from PyQt4 import QtGui

from library.DbComboBox import CDbComboBox
from Utils import parseOKVEDList


class COKVEDComboBox(CDbComboBox):
    def __init__(self, parent):
        CDbComboBox.__init__(self, parent)
        self.setAddNone(False)
        self.setNameField('code')
        self.setTable('rbOKVED')
        self.__orgCode = ''


    def setOrgCode(self, orgCode):
        if self.__orgCode != orgCode:
            db = QtGui.qApp.db
            table = db.table('rbOKVED')
            filter = []
            for code in parseOKVEDList(orgCode):
                code = code[:-1] ### последний символ отрезаем т.к. он вредит в случае указания основной деятельности :(
                if code:
                    filter.append(table['code'].like(code+'...'))
            currText = self.text()
            self.setFilter(db.joinOr(filter))
            self.setText(currText)
            self.__orgCode = orgCode


    def orgCode(self):
        return self.__orgCode
