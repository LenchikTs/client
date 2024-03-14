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

# В базе данных хранится json-представление списка пар [ имя-особенности, значение особенности ]

import json
from PyQt4 import QtGui
from PyQt4.QtCore import QVariant

from Stock.NomenclatureComboBox    import CFeatureItemDelegate, CFeaturesModel
from library.InDocTable            import CInDocTableView
from library.Utils                 import forceRef, forceString
from ActionPropertyValueType       import CActionPropertyValueType
from StringActionPropertyValueType import CStringActionPropertyValueType


class CFeatureActionPropertyValueType(CActionPropertyValueType):
    variantType  = QVariant.String
    name         = u'Особенности ЛСиИМН'
    preferredHeight     = 5
    preferredHeightUnit = 1


    class CPropEditor(CInDocTableView):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            CInDocTableView.__init__(self, parent)

            self.modelFeatures = CFeaturesModel(self)

            self.setItemDelegate(CFeatureItemDelegate(self))
            self.setModel(self.modelFeatures)

            actionTypeId = action.getType().id

            cols = ['nomenclatureClass_id', 'nomenclatureKind_id', 'nomenclatureType_id'] # wtf
            record = QtGui.qApp.db.getRecord('ActionType', cols, actionTypeId)

            nomenclatureClassId = forceRef(record.value('nomenclatureClass_id'))
            nomenclatureKindId  = forceRef(record.value('nomenclatureKind_id'))
            nomenclatureTypeId  = forceRef(record.value('nomenclatureType_id'))

            self.modelFeatures.prepareList(nomenclatureClassId, nomenclatureKindId, nomenclatureTypeId)
            self.addMoveRow()
            self.addPopupSeparator()
            self.addPopupSelectAllRow()
            self.addPopupClearSelectionRow()
            self.addPopupSeparator()
            self.addPopupDelRow()


        def setValue(self, value):
            try:
                listKeyValueMaps = CFeatureActionPropertyValueType.parseValue(forceString(value))
            except:
                # logCurrentException()
                listKeyValueMaps = []
            if listKeyValueMaps:
                self.modelFeatures.setValuableFeatures(listKeyValueMaps)
            else:
                self.modelFeatures.setEmptyFeatures()


        def value(self):
            return CFeatureActionPropertyValueType.combineValue(self.modelFeatures.getValuableFeatures())


    @staticmethod
    def convertDBValueToPyValue(value):
        return forceString(value)

    convertQVariantToPyValue = convertDBValueToPyValue


    def toText(self, v):
        result = []
        try:
            listKeyValueMaps = self.parseValue(forceString(v))
            for name, value in listKeyValueMaps:
                result.append(u'%s:%s' % (name, value))
            return '\n'.join(result)
        except:
            # logCurrentException()
            return u'<ошибка формата данных>'


    def toInfo(self, context, v):
        return self.parseValue(forceString(v))


    @classmethod
    def getTableName(cls):
        return cls.tableNamePrefix+CStringActionPropertyValueType.name


    @staticmethod
    def parseValue(strValue):
        if not strValue:
            return []
        result = json.loads(strValue)
        if not isinstance(result, list):
            raise ValueError('CFeatureActionPropertyValueType data format error')
        for item in result:
            if not ( isinstance(item, list)
                     and len(item) == 2
                     and isinstance(item[0], basestring)
                     and isinstance(item[1], basestring)):
                raise ValueError('CFeatureActionPropertyValueType data format error')
        return result


    @staticmethod
    def combineValue(listValue):
        if not listValue:
            return ''
        return json.dumps(listValue)
