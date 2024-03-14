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


from PyQt4.QtCore import QVariant
from PyQt4 import QtGui

from library.PrintInfo import CRBInfo, CRBInfoWithIdentification
from library.crbcombobox     import CRBComboBox
from library.database import CTableRecordCache
from library.Utils           import forceRef, forceString

from ActionPropertyValueType import CActionPropertyValueType


class CSocStatusActionPropertyValueType(CActionPropertyValueType):
    name         = u'Соц статус'
    variantType  = QVariant.Int
    recordCache = None


    class CRBSocStatusInfo(CRBInfoWithIdentification):
        tableName = 'rbSocStatusType'


    class CPropEditor(CRBComboBox):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            CRBComboBox.__init__(self, parent)
            domain = domain.replace('\'', '').replace('"', '').split(',')
            filter = u'''exists(select rbSocStatusClass.id from
                rbSocStatusClass
                LEFT JOIN
                    rbSocStatusClassTypeAssoc ON rbSocStatusClass.id = rbSocStatusClassTypeAssoc.class_id
                where rbSocStatusClass.name in (%s) and rbSocStatusClassTypeAssoc.type_id = rbSocStatusType.id
                )'''%','.join(u'\'%s\''%d.strip() for d in domain ) if domain[0] else ''
            self.setTable('rbSocStatusType', filter=filter)

        def setValue(self, value):
            CRBComboBox.setValue(self, forceRef(value))


    @staticmethod
    def convertDBValueToPyValue(value):
        return forceRef(value)


    convertQVariantToPyValue = convertDBValueToPyValue


    def toInfo(self, context, v):
        return CSocStatusActionPropertyValueType.CRBSocStatusInfo(context, v)


    @classmethod
    def getTableName(cls):
        return cls.tableNamePrefix+'rbSocStatus'



    def toText(self, v):
        if self.recordCache is None:
            self.recordCache = CTableRecordCache(QtGui.qApp.db, 'rbSocStatusType')
        record = self.recordCache.get(v)
        if record:
            return forceString(record.value('name'))
        return forceString(v)

