# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2017-2020 SAMSON Group. All rights reserved.
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
from library.Utils             import forceRef, forceString, forceDate
from RefBooks.Speciality.Info  import CSpecialityInfo

from ActionPropertyValueType       import CActionPropertyValueType


class CSpecialityActionPropertyValueType(CActionPropertyValueType):
    name         = 'rbSpeciality'
    variantType  = QVariant.Int
    
    def __init__(self, domain = None):
        CActionPropertyValueType.__init__(self, domain)
        self.rawDomain = domain
        self.domain = self.parseDomain(domain)

    class CPropEditor(CRBComboBox):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            CRBComboBox.__init__(self, parent)
#            self.domain = domain
            setFilter = ''
            if action and action.actionType() and u'direction' in  action.actionType().flatCode.lower():
                if u'Целевая МО' in action._actionType._propertiesByName:
                    db = QtGui.qApp.db
                    propertyValue = action[u'Целевая МО']
                    tableRBSP = db.table('rbSpeciality')
                    tableOrganisation = db.table('Organisation')
                    tableOSP = db.table('Organisation_Speciality')
                    record = action.getRecord()
                    directionDate = forceDate(record.value('directionDate')) if record else None
                    cond = [tableOrganisation['deleted'].eq(0),
                            tableOSP['speciality_id'].isNotNull()
                            ]
                    if propertyValue:
                        cond.append(tableOSP['master_id'].eq(propertyValue))
                    else:
                        cond.append(tableOSP['master_id'].isNotNull())
                    if directionDate:
                        cond.append(db.joinOr([tableOSP['begDate'].isNull(), tableOSP['begDate'].dateLe(directionDate)]))
                        cond.append(db.joinOr([tableOSP['endDate'].isNull(), tableOSP['endDate'].dateGe(directionDate)]))
                    queryTable = tableOrganisation.innerJoin(tableOSP, tableOSP['master_id'].eq(tableOrganisation['id']))
                    idList = db.getDistinctIdList(queryTable, [tableOSP['speciality_id']], cond)
                    setFilter = db.joinAnd([tableRBSP['id'].inlist(idList)])
            self.setTable('rbSpeciality', addNone=True, filter=setFilter)
            

        def setValue(self, value):
            CRBComboBox.setValue(self, forceRef(value))
            
    def parseDomain(self, domain):
        
        fedCodes = []
        for word in domain.split(','):
            if word:
                parts = word.split(':')
                if len(parts) == 1:
                    key,  val = u'федкод',  parts[0].strip()
                elif len(parts) == 2:
                    key, val = parts[0].strip(), parts[1].strip()
                else:
                    raise ValueError, self.badDomain % locals()
                keylower = key.lower()
                vallower = val.lower()
                if keylower == u'федкод':
                    fedCodes.extend(vallower.split(';'))
                else:
                    raise ValueError, self.badKey % locals()

        
        db = QtGui.qApp.db
        table = db.table('rbSpeciality')
        cond = []
        if fedCodes:
            cond.append(table['federalCode'].inlist(fedCodes))
        return db.joinAnd(cond)   



    @staticmethod
    def convertDBValueToPyValue(value):
        return forceRef(value)


    convertQVariantToPyValue = convertDBValueToPyValue


    def toInfo(self, context, v):
        return CSpecialityInfo(context, v)


    def toText(self, v):
        return forceString(QtGui.qApp.db.translate('rbSpeciality', 'id', v, 'CONCAT(code,\' | \',name)'))


