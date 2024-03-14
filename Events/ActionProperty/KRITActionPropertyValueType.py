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


from PyQt4.QtCore import QVariant
from PyQt4 import QtGui

from library.PrintInfo import CRBInfo
from library.crbcombobox import CRBComboBox
from library.Utils import forceRef, forceString, forceDate
from Events.Utils import getEventAidTypeRegionalCode

from ActionPropertyValueType import CActionPropertyValueType


class CKRITActionPropertyValueType(CActionPropertyValueType):
    name         = u'Доп. классиф. критерий'
    variantType  = QVariant.Int
    badDomain = u'Неверное описание области определения значения свойства действия типа "Доп. классиф. критерий":\n%(domain)s'
    badKey = u'Недопустимый ключ "%(key)s" в описание области определения значения свойства действия типа "Доп. классиф. критерий":\n%(domain)s'
    badValue = u'Недопустимое значение "%(val)s" ключа "%(key)s" в описание области определения значения свойства действия типа "Доп. классиф. критерий":\n%(domain)s'


    class CKRITInfo(CRBInfo):
        tableName = 'soc_spr80'


    class CPropEditor(CRBComboBox):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            CRBComboBox.__init__(self, parent)
            self.setShowFields(CRBComboBox.showCodeAndName)
            self.setTable('soc_spr80')
            db = QtGui.qApp.db
            tableSpr80 = db.table('soc_spr80')
            begDateAction = forceDate(action._record.value('begDate'))
            endDateAction = forceDate(action._record.value('endDate'))
            finalDomain = domain[:]
            regionalCode = getEventAidTypeRegionalCode(eventTypeId)
            if regionalCode in ['301', '302', '511', '522']:
                finalDomain.append('type = 0')
            else:
                finalDomain.append('type <> 0')

            if not endDateAction.isNull():
                finalDomain.append(tableSpr80['begDate'].le(endDateAction))
                finalDomain.append(db.joinOr([tableSpr80['endDate'].isNull(), tableSpr80['endDate'].ge(endDateAction)]))
            else:
                finalDomain.append(tableSpr80['begDate'].le(begDateAction))
                finalDomain.append(db.joinOr([tableSpr80['endDate'].isNull(), tableSpr80['endDate'].ge(begDateAction)]))
            self.setFilter(db.joinAnd(finalDomain))

        def setValue(self, value):
            CRBComboBox.setValue(self, forceRef(value))

    def __init__(self, domain=None):
        CActionPropertyValueType.__init__(self, domain)
        self.rawDomain = domain
        self.domain = self.parseDomain(domain)


    def filterByMKB(self, mkb):
        self.domain = self.parseDomain(self.rawDomain)
        if mkb is None or mkb and (mkb[0] != u'C' and mkb[:2] != 'D0'):
            self.domain.append('type <> 1')


    def parseDomain(self, domain):
        codeList = []
        type = None
        for word in domain.split(','):
            if word:
                parts = word.split(':')
                if len(parts) == 1:
                    key, val = u'код', parts[0].strip()
                elif len(parts) == 2:
                    key, val = parts[0].strip(), parts[1].strip()
                else:
                    raise ValueError, self.badDomain % locals()
                keylower = key.lower()
                vallower = val.lower()
                if keylower == u'код':
                    codeList.extend(vallower.split(';'))
                elif keylower == u'тип':
                    if vallower == u'шрм':
                        type = 0
                    elif vallower == u'лечение зно':
                        type = 1
                    elif vallower == u'ивл':
                        type = 2
                    elif vallower == u'лечение гепс':
                        type = 3
                    elif vallower == u'мрт':
                        type = 4
                    elif vallower == u'гиписи':
                        type = 5
                    elif vallower == u'биопсиязно':
                        type = 6
                    elif vallower == u'эко':
                        type = 7
                    elif vallower == u'грыжи':
                        type = 8
                    elif vallower == u'ковид':
                        type = 9
                    elif vallower == u'инфаркт':
                        type = 10
                    elif vallower == u'реабковид':
                        type = 11
                    elif vallower == u'лимфа':
                        type = 12
                    elif vallower == u'препараты':
                        type = 13
                    elif vallower == u'дистонии':
                        type = 14
                    elif vallower == u'лучтер':
                        type = 15
                    elif vallower == u'травма':
                        type = 16
                    elif vallower == u'антимикр':
                        type = 17
                    elif vallower == u'дерматозы':
                        type = 18
                    elif vallower == u'генинж':
                        type = 19
                    elif vallower == u'иммунизация':
                        type = 20
                    elif vallower == u'уркур':
                        type = 21
                    elif vallower == u'колфракц':
                        type = 22
                    elif vallower == u'заменгенинж':
                        type = 23
                    elif vallower == u'сопровтер':
                        type = 24
                    elif vallower == u'мочсист':
                        type = 25
                    elif vallower == u'лечение гепb':
                        type = 26
                else:
                    raise ValueError, self.badKey % locals()
                    
        db = QtGui.qApp.db
        table = db.table('soc_spr80')
        cond = []

        if codeList:
            cond.append(table['code'].inlist(codeList))
        if type is not None:
            cond.append(table['type'].eq(type))
        return cond
        
        
    @staticmethod
    def convertDBValueToPyValue(value):
        return forceRef(value)


    convertQVariantToPyValue = convertDBValueToPyValue
    
    
    def toText(self, v):
        return forceString(QtGui.qApp.db.translate('soc_spr80', 'id', v, 'CONCAT(code,\' | \',name)'))
        

    def toInfo(self, context, v):
        return CKRITActionPropertyValueType.CKRITInfo(context, v)


    def getTableName(self):
        return self.tableNamePrefix + 'Integer'
