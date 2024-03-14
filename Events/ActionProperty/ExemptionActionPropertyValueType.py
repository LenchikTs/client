# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2015 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################


from PyQt4.QtCore import QVariant, QDateTime
from PyQt4 import QtGui
from library.PrintInfo       import CRBInfo
from library.crbcombobox     import CRBComboBox
from library.Utils           import forceRef, forceString, forceDateTime

from ActionPropertyValueType import CActionPropertyValueType


class CExemptionActionPropertyValueType(CActionPropertyValueType):
    name         = u'Льгота'
    variantType  = QVariant.Int
    
    class CRBSocStatusInfo(CRBInfo):
        tableName = 'rbSocStatusType'

    class CPropEditor(CRBComboBox):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            CRBComboBox.__init__(self, parent)
            CRBComboBox.showFields = CRBComboBox.showCodeAndName            
            date = forceDateTime(action._record.value('directionDate'))
            if not date.isValid():
                date = QDateTime.currentDateTime()
            date = QtGui.qApp.db.formatDate(date)
            # выбираемтолько действующие льготы
            filter = u"""rbSocStatusType.id in (select cs.socStatusType_id 
                from Client c 
                left join ClientSocStatus cs on cs.client_id = c.id and cs.deleted = 0
                left join ClientDocument cd on cd.id = cs.document_id and cd.deleted = 0
                left join rbSocStatusClass ssc on ssc.id = cs.socStatusClass_id
                where c.id = %s and ssc.group_id = 1 and cd.documentType_id is not null and length(trim(cd.number))>0
                and cs.begDate <= %s and (cs.endDate is null or cs.endDate >= %s))""" % (clientId, date, date)
            self.setTable('rbSocStatusType', filter=filter, needCache=False)

        def setValue(self, value):
            CRBComboBox.setValue(self, forceRef(value))


    @staticmethod
    def convertDBValueToPyValue(value):
        return forceRef(value)


    convertQVariantToPyValue = convertDBValueToPyValue


    def toInfo(self, context, v):
        return CExemptionActionPropertyValueType.CRBSocStatusInfo(context, v)
        
    def toText(self, v):
        return forceString(QtGui.qApp.db.translate('rbSocStatusType', 'id', v, 'CONCAT(code,\' | \',name)'))


    def getTableName(self):
        return self.tableNamePrefix+'rbSocStatus'
