# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2022 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui

from library.Utils import (
    forceRef,
    forceString,
    forceStringEx,
    forceDouble
)

# DIREACTION_DATE_INDEX = 0
# BEG_DATE_INDEX = 1
# NOMENCLATURE_INDEX = 2
# PLAN_END_DATE = 3
# DOSES_INDEX = 4
# SIGNA_INDEX = 5
# DURATION_INDEX = 6
# ALIQUOTICITY_INDEX = 7
# PERIODICITY_INDEX = 8
# ACTIVESUBSTANCE_INDEX = 9

(DIREACTION_DATE_INDEX,
BEG_DATE_INDEX,
NOMENCLATURE_INDEX,
PLAN_END_DATE,
DOSES_INDEX,
SIGNA_INDEX,
DURATION_INDEX,
ALIQUOTICITY_INDEX,
PERIODICITY_INDEX,
ACTIVESUBSTANCE_INDEX) = range(10)


nomenclatureInTableIndex = 1
dosageInTableIndex = 2
signaInTableIndex = 3
activeSubstanceInTableIndex = 4


_mapInActionsSelectionTable2Index = {
    nomenclatureInTableIndex: NOMENCLATURE_INDEX,
    dosageInTableIndex: DOSES_INDEX,
    signaInTableIndex: SIGNA_INDEX,
    activeSubstanceInTableIndex: ACTIVESUBSTANCE_INDEX
}

_mapColumnIndex2InActionsSelectionTable = {}
for k, v in _mapInActionsSelectionTable2Index.items():
    _mapColumnIndex2InActionsSelectionTable[v] = k


class CCellsSettings(object):
    __usingTypes__ = 'usingTypes'
    __dosageValue__ = 'dosageValue'
    __dosageUnitName__ = 'dosageUnitName'
    __dosageUnitId__ = 'dosageUnitId'

    def __init__(self, model):
        self._model = model
        self._actionTypeData = {}
        self._nomenclatureData = {}

    def getNomenclatureUsingTypes(self, nomenclatureId):
        data = self._getNomenclatureValues(nomenclatureId)
        return data.get(self.__usingTypes__)

    def setNomenclatureUsingTypes(self, nomenclatureId, value):
        val = forceStringEx(value)
        if val:
            usingTypes = self.getNomenclatureUsingTypes(nomenclatureId)
            if val not in usingTypes:
                usingTypes.append(val)
                result = self._nomenclatureData[nomenclatureId]
                result[self.__usingTypes__] = usingTypes
                self._nomenclatureData[nomenclatureId] = result
        return self.getNomenclatureUsingTypes(nomenclatureId)

    def getNomenclatureDoses(self, nomenclatureId):
        values = self._getNomenclatureValues(nomenclatureId)
        return values.get(self.__dosageValue__, 0)

    def getNomenclatureDosageText(self, nomenclatureId):
        values = self._getNomenclatureValues(nomenclatureId)
        if not values:
            return ''

        return '%s %s' % (
            values.get(self.__dosageValue__, 0),
            values.get(self.__dosageUnitName__)
        )

    def getNomenclatureDosageUnitName(self, nomenclatureId):
        values = self._getNomenclatureValues(nomenclatureId)
        if not values:
            return ''
        return values[self.__dosageUnitName__]

    def _getNomenclatureValues(self, nomenclatureId):
        if not nomenclatureId:
            return {
                self.__dosageUnitName__: u'',
                self.__usingTypes__: [],
                self.__dosageValue__: 0.0,
                self.__dosageUnitId__: None
            }
        if nomenclatureId not in self._nomenclatureData:
            db = QtGui.qApp.db
            nomenclatureRecord = db.getRecord(
                'rbNomenclature',
                'unit_id, '
                'dosageValue',
                nomenclatureId
            )

            if not nomenclatureRecord:
                self._nomenclatureData[nomenclatureId] = {
                    self.__dosageUnitName__: u'',
                    self.__usingTypes__: [],
                    self.__dosageValue__: 0.0,
                    self.__dosageUnitId__: None
                }
                return self._nomenclatureData[nomenclatureId]

            dosageUnitId = forceRef(nomenclatureRecord.value('unit_id'))

            result = {
                self.__dosageValue__: forceDouble(nomenclatureRecord.value('dosageValue')),
                self.__dosageUnitId__: dosageUnitId
            }

            if dosageUnitId:
                unitRecord = db.getRecord('rbUnit', 'code, name', dosageUnitId)
                name = forceString(unitRecord.value('code')) if unitRecord else u''
            else:
                name = ''
            result[self. __dosageUnitName__] = name

            unitTypesTable = db.table('rbNomenclature_UsingType')
            tableUsingType = db.table('rbNomenclatureUsingType')
            queryUsingType = unitTypesTable.innerJoin(tableUsingType, tableUsingType['id'].eq(unitTypesTable['usingType_id']))
            unitTypesRecordList = db.getRecordList(
                queryUsingType,
                [tableUsingType['name'].alias('usingType')],
                where=unitTypesTable['master_id'].eq(nomenclatureId),
                order=unitTypesTable['idx'].name()
            )

            result[self.__usingTypes__] = [forceStringEx(r.value('usingType')) for r in unitTypesRecordList]
            self._nomenclatureData[nomenclatureId] = result

        return self._nomenclatureData[nomenclatureId]

    def get(self, group):
        return self._get(group)

    def clear(self):
        self._actionTypeData.clear()

    def _get(self, group):
        actionTypeId = group.actionTypeId
        if not actionTypeId in self._actionTypeData:
            self._createSettings(group)
        return self._actionTypeData[actionTypeId]

    def getByRowColumn(self, row, column):
        group = self._model.items()[row]
        return self._get(group).get(column)

    def checkNomenclature(self, group, nomenclatureId):
        if not nomenclatureId:
            return True

        propertyType = self.getGroupNomenclaturePT(group)
        if not propertyType:
            return False

        return self.getGroupNomenclature(group) == nomenclatureId

    def hasGroupSigna(self, group):
        return bool(self.getGroupSignaPT(group))

    def hasGroupDoses(self, group):
        return bool(self.getGroupDosesPT(group))

    def _getPropertyValue(self, group, pt):
        if not pt:
            return None
        action = group.headItem[1]
        return action.getPropertyById(pt.id).getValue()

    def _setPropertyValue(self, group, pt, value):
        if not pt:
            return
        #action = group.headItem[1]
        for actionRecordItem in group._mapRow2Item.values():
            action = actionRecordItem[1]
            property = action.getPropertyById(pt.id)
            property.preApplyDependents(action)
            property.setValue(value)
            property.applyDependents(action)

    def _getPropertyText(self, group, pt):
        if not pt:
            return None
        action = group.headItem[1]
        return action.getPropertyById(pt.id).getText()

    def getGroupNomenclature(self, group):
        pt = self.getGroupNomenclaturePT(group)
        return self._getPropertyValue(group, pt)

    def setGroupNomenclature(self, group, value):
        pt = self.getGroupNomenclaturePT(group)
        self._setPropertyValue(group, pt, value)

    def getGroupNomenclatureText(self, group):
        pt = self.getGroupNomenclaturePT(group)
        return self._getPropertyText(group, pt)

    def getGroupSigna(self, group):
        pt = self.getGroupSignaPT(group)
        return self._getPropertyValue(group, pt)

    def getGroupSignaText(self, group):
        pt = self.getGroupSignaPT(group)
        return self._getPropertyText(group, pt)

    def setGroupSigna(self, group, value):
        pt = self.getGroupSignaPT(group)
        return self._setPropertyValue(group, pt, value)

    def getGroupDoses(self, group):
        pt = self.getGroupDosesPT(group)
        return self._getPropertyValue(group, pt)

    def setGroupDoses(self, group, value):
        pt = self.getGroupDosesPT(group)
        return self._setPropertyValue(group, pt, value)

    def getGroupDosesText(self, group):
        doses = self.getGroupDoses(group)
        name = self.getNomenclatureDosageUnitName(self.getGroupNomenclature(group))
        if name:
            return ' '.join([str(doses), name])
        return str(doses)

    def getGroupNomenclaturePT(self, group):
        return self._get(group).get(NOMENCLATURE_INDEX)

    def getGroupDosesPT(self, group):
        return self._get(group).get(DOSES_INDEX)

    def getGroupSignaPT(self, group):
        return self._get(group).get(SIGNA_INDEX)

    def _createSettings(self, group):
        action = group.headItem[1]
        actionType = action.getType()

        self._actionTypeData[actionType.id] = {}

        for propertyType in actionType.getPropertiesById().values():
            if propertyType.inActionsSelectionTable:
                column = _mapInActionsSelectionTable2Index[propertyType.inActionsSelectionTable]
                self._actionTypeData[actionType.id][column] = propertyType
