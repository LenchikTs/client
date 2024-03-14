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
from PyQt4.QtCore import QVariant


from Registry.Utils                import CClientQuotaInfo
from Quoting.ClientQuotingComboBox import CClientQuotingComboBox
from library.Utils                 import forceDate, forceRef, forceString

from ActionPropertyValueType  import CActionPropertyValueType

class CClientQuotingActionPropertyValueType(CActionPropertyValueType):
    mapIdToName = {} # wtf, кто будет чистить при присединении к другой базе данных?
    name        = u'Квота пациента'
    variantType = QVariant.Int

    class CPropEditor(CClientQuotingComboBox):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            actionRecord = action.getRecord()
            begDate = forceDate(actionRecord.value('begDate'))
            endDate = forceDate(actionRecord.value('endDate'))
            CClientQuotingComboBox.__init__(self, parent, clientId, begDate=begDate, endDate=endDate)

        def setValue(self, value):
            v = forceRef(value)
            CClientQuotingComboBox.setValue(self, v)


    def getEditorClass(self):
        return self.CPropEditor


    @classmethod
    def getTableName(cls):
        return cls.tableNamePrefix+'Client_Quoting'


    @staticmethod
    def convertDBValueToPyValue(value):
        return forceRef(value)


    convertQVariantToPyValue = convertDBValueToPyValue


    def toText(self, v):
        v = forceRef(v)
        name = ''
        if v:
            db = QtGui.qApp.db
            quotaTypeId = forceRef(db.translate('Client_Quoting', 'id', v, 'quotaType_id'))
            name = CClientQuotingActionPropertyValueType.mapIdToName.get(v, None)
            if not name:
                name = forceString(db.translate('QuotaType', 'id', quotaTypeId, 'CONCAT_WS(\' | \', code, name)'))
                CClientQuotingActionPropertyValueType.mapIdToName[quotaTypeId] = name
        return name

    def toInfo(self, context, v):
        return context.getInstance(CClientQuotaInfo, forceRef(v))
