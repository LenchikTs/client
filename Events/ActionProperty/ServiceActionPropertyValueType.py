# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2017-2023 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

import json
from PyQt4 import QtGui
from PyQt4.QtCore import QVariant


from RefBooks.Service.Info   import CServiceInfo
from library.CRBSearchComboBox import CRBSearchComboBox
from library.Utils           import forceRef, forceString, forceDate

from ActionPropertyValueType import CActionPropertyValueType


class CServiceActionPropertyValueType(CActionPropertyValueType):
    name         = 'rbService'
    variantType  = QVariant.Int

    class CPropEditor(CRBSearchComboBox):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            CRBSearchComboBox.__init__(self, parent)
            db = QtGui.qApp.db
            tableService = db.table('rbService')
            domainObj = json.loads(domain) if domain else {}
            groupObj = domainObj.get('group', None)
            codeObj = domainObj.get('code', None)
            nameObj = domainObj.get('name', None)
            cond = []
            if action and action.actionType() and u'direction' in  action.actionType().flatCode.lower():
                if action.hasProperty(u'Целевая МО'):
                    propertyValue = action[u'Целевая МО']
                    tableOrganisation = db.table('Organisation')
                    tableOrganisationService = db.table('Organisation_Service')
                    record = action.getRecord()
                    directionDate = forceDate(record.value('directionDate')) if record else None
                    tmpCond = [tableOrganisation['deleted'].eq(0),
                               tableOrganisationService['service_id'].isNotNull()
                              ]
                    if propertyValue:
                        tmpCond.append(tableOrganisationService['master_id'].eq(propertyValue))
                    else:
                        tmpCond.append(tableOrganisationService['master_id'].isNotNull())
                    if directionDate:
                        tmpCond.append(db.joinOr([tableOrganisationService['begDate'].isNull(), tableOrganisationService['begDate'].dateLe(directionDate)]))
                        tmpCond.append(db.joinOr([tableOrganisationService['endDate'].isNull(), tableOrganisationService['endDate'].dateGe(directionDate)]))
                    queryTable = tableOrganisationService.innerJoin(tableOrganisation, tableOrganisation['id'].eq(tableOrganisationService['master_id']))
                    idList = db.getDistinctIdList(queryTable, [tableOrganisationService['service_id']], tmpCond)
                    cond.append(tableService['id'].inlist(idList))

            if groupObj is not None:
                ok, groupCodes = self._checkAndNormalizeCodeObj(groupObj)
                if ok:
                    tableServiceGroup = db.table('rbServiceGroup')
                    groupIds = db.getIdList(tableServiceGroup,
                                            'id',
                                            tableServiceGroup['code'].inlist(groupCodes)
                                           )
                    cond.append(tableService['group_id'].inlist(groupIds))
                else:
                    raise Exception(u'Неправильное описание group в «%s»' % domain)

            if codeObj is not None:
                ok, codes = self._checkAndNormalizeCodeObj(codeObj)
                if ok:
                    cond.append(db.joinOr([tableService['code'].like(code) for code in codes]))
                else:
                    raise Exception(u'Неправильное описание code в «%s»' % domain)

            if nameObj is not None:
                ok, names = self._checkAndNormalizeCodeObj(nameObj)
                if ok:
                    cond.append(db.joinOr([tableService['name'].like(name) for name in names]))
                else:
                    raise Exception(u'Неправильное описание name в «%s»' % domain)

            self.setTable('rbService', addNone=True, filter=db.joinAnd(cond) if cond else '')


        def setValue(self, value):
            CRBSearchComboBox.setValue(self, forceRef(value))


        @staticmethod
        def _checkAndNormalizeCodeObj(codeObj):
            if isinstance(codeObj, (basestring, int)):
                return True, [unicode(codeObj)]
            if (     isinstance(codeObj, list)
                 and all(isinstance(code, (basestring, int)) for code in codeObj)
               ):
                return True, [unicode(code) for code in codeObj]
            return False, None


    @staticmethod
    def convertDBValueToPyValue(value):
        return forceRef(value)


    convertQVariantToPyValue = convertDBValueToPyValue


    def toInfo(self, context, v):
        return CServiceInfo(context, v)


    def toText(self, v):
        return forceString(QtGui.qApp.db.translate('rbService', 'id', v, 'CONCAT(code,\' | \',name)'))
