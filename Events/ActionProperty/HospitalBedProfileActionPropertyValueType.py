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


from library.crbcombobox import CRBComboBox
from library.Utils       import forceRef, forceString, forceDate
from ActionPropertyValueType       import CActionPropertyValueType


class CHospitalBedProfileActionPropertyValueType(CActionPropertyValueType):
    name         = 'rbHospitalBedProfile'
    variantType  = QVariant.Int

    class CPropEditor(CRBComboBox):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            CRBComboBox.__init__(self, parent)
            self.domain = domain
            orgStructureId = None
            setFilter=''
            setFilterAnd = u''
            db = QtGui.qApp.db
            if action and action.actionType() and u'direction' in  action.actionType().flatCode.lower():
                if u'Целевая МО' in action._actionType._propertiesByName:
                    propertyValue = action[u'Целевая МО']
                    tableRBHBP = db.table('rbHospitalBedProfile')
                    tableOrganisation = db.table('Organisation')
                    tableOHBP = db.table('Organisation_HospitalBedProfile')
                    record = action.getRecord()
                    directionDate = forceDate(record.value('directionDate')) if record else None
                    cond = [tableOrganisation['deleted'].eq(0),
                            tableOHBP['hospitalBedProfile_id'].isNotNull()
                            ]
                    if propertyValue:
                        cond.append(tableOHBP['master_id'].eq(propertyValue))
                    else:
                        cond.append(tableOHBP['master_id'].isNotNull())
                    if directionDate:
                        cond.append(db.joinOr([tableOHBP['begDate'].isNull(), tableOHBP['begDate'].dateLe(directionDate)]))
                        cond.append(db.joinOr([tableOHBP['endDate'].isNull(), tableOHBP['endDate'].dateGe(directionDate)]))
                    queryTable = tableOrganisation.innerJoin(tableOHBP, tableOHBP['master_id'].eq(tableOrganisation['id']))
                    idList = db.getDistinctIdList(queryTable, [tableOHBP['hospitalBedProfile_id']], cond)
                    setFilter = db.joinAnd([tableRBHBP['id'].inlist(idList)])
            elif action:
                record = action.getRecord()
                if record:
                    begDate = forceDate(record.value('begDate'))
                    if begDate:
                        setFilter = u'''(endDate IS NULL OR endDate >= %s)'''%(db.formatDate(begDate))
                        setFilterAnd = u' AND '
            if u'received' in action._actionType.flatCode.lower():
                orgStructureId = action[u'Направлен в отделение'] if u'Направлен в отделение' in action._actionType._propertiesByName else None
            elif u'leaved' in action._actionType.flatCode.lower():
                orgStructureId = action[u'Отделение'] if u'Отделение' in action._actionType._propertiesByName else None
            elif u'planning' in action._actionType.flatCode.lower():
                orgStructureId = action[u'Подразделение'] if u'Подразделение' in action._actionType._propertiesByName else None
            if action._actionType.flatCode.lower() in [u'received', u'leaved', u'planning']:
                if orgStructureId:
                    table = db.table('vHospitalBed')
                    hospitalBedProfileIdList = db.getDistinctIdList(table, [table['profile_id']], [table['master_id'].eq(orgStructureId)])
                    if hospitalBedProfileIdList:
                        setFilter += setFilterAnd + u'id IN (%s)'%(u', '.join(str(profileId) for profileId in hospitalBedProfileIdList))
                    else:
                        setFilter += setFilterAnd + "id is null"
                else:
                    setFilter = "id is null"
            if self.domain:
                codeList = ','.join(str(item) for item in self.domain)
                setFilter += setFilterAnd + u'rbHospitalBedProfile.code in (%s)'%codeList
            self.setTable('rbHospitalBedProfile', addNone=True, filter=setFilter, order='code')


        def setValue(self, value):
            CRBComboBox.setValue(self, forceRef(value))


    def __init__(self, domain = None):
        CActionPropertyValueType.__init__(self, domain)
        self.domain = self.parseDomain(domain)


    def parseDomain(self, domain):
        codeList = []
        for param in domain.split(';'):
            if param.startswith('range'):
                rangeStart = ''
                rangeEnd = ''
                param = param.split(',')
                for part in param:
                    if not rangeStart:
                        for i in ''.join(i for i in part):
                                if i.isdigit():
                                    rangeStart += i
                    else:
                        for i in ''.join(i for i in part):
                                if i.isdigit():
                                    rangeEnd += i
                if rangeStart and rangeEnd:
                    codeList.extend(range(int(rangeStart), int(rangeEnd)+1))
            elif param.isdigit():
                codeList.append(int(param) if param else 0)
            else:
                pass
        return codeList


    @staticmethod
    def convertDBValueToPyValue(value):
        return forceRef(value)


    convertQVariantToPyValue = convertDBValueToPyValue


    def toInfo(self, context, v):
        from HospitalBeds.HospitalBedInfo import CHospitalBedProfileInfo
        return CHospitalBedProfileInfo(context, v)


    def toText(self, v):
        return forceString(QtGui.qApp.db.translate('rbHospitalBedProfile', 'id', v, 'CONCAT(code,\' | \',name)'))

