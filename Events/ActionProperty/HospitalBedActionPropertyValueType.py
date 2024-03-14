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

from HospitalBeds.HospitalBedFindComboBox import CHospitalBedFindComboBox
from library.Utils         import forceDate, forceInt, forceRef, forceString

from ActionPropertyValueType       import CActionPropertyValueType


class CHospitalBedActionPropertyValueType(CActionPropertyValueType):
    name         = 'HospitalBed'
    variantType  = QVariant.Int
    isCopyable   = False

    class CPropEditor(CHospitalBedFindComboBox):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            plannedEndDate = forceDate(action._record.value('plannedEndDate'))
            orgStructureId = action[u'Отделение пребывания'] if (u'moving' in action._actionType.flatCode.lower()) else None
            bedId = action[u'койка']
            begDateAction = forceDate(action._record.value('begDate'))
            if bedId:
                orgStructureId = forceRef(QtGui.qApp.db.translate('OrgStructure_HospitalBed', 'id', bedId, 'master_id'))
            if not orgStructureId and action:
                propertyCount = 0
                actionType = action.getType()
                propertyTypeList = actionType.getPropertiesById().values()
                propertyTypeList.sort(key=lambda x: (x.idx))
                for row, propertyType in enumerate(propertyTypeList):
                    if propertyType.typeName.lower() == (u'OrgStructure').lower():
                        propertyCount += 1
                        if propertyCount > 1:
                            orgStructureId = None
                            break
                        property = action.getPropertyById(propertyType.id)
                        orgStructureId = property._value
            sex = 0
            age = None
            if clientId:
                db = QtGui.qApp.db
                table = db.table('Client')
                cond = [table['id'].eq(clientId), 
                        table['deleted'].eq(0)]
                cols = [table['sex'], 
                        '''age(Client.birthDate, DATE(%s)) AS clientAge'''%(db.formatDate(begDateAction)) if begDateAction else '0 AS clientAge']
                record = db.getRecordEx(table, cols, cond)
                if record:
                    sex = forceInt(record.value('sex'))
                    age = forceInt(record.value('clientAge')) 
            CHospitalBedFindComboBox.__init__(self, parent, domain, plannedEndDate, orgStructureId, sex, age, bedId, eventTypeId, begDateAction)


        def setValue(self, value):
            CHospitalBedFindComboBox.setValue(self, forceRef(value))


    @staticmethod
    def convertDBValueToPyValue(value):
        return forceRef(value)


    convertQVariantToPyValue = convertDBValueToPyValue


    def getTableName(self):
        return self.tableNamePrefix + self.name


    def toText(self, v):
        return forceString(QtGui.qApp.db.translate('OrgStructure_HospitalBed', 'id', v, 'CONCAT(code,\' | \',name)'))


    def toInfo(self, context, v):
        from HospitalBeds.HospitalBedInfo import CHospitalBedInfo
        return context.getInstance(CHospitalBedInfo, forceRef(v))

