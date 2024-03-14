# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2020 SAMSON Group. All rights reserved.
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

from library.PrintInfo import CRBInfoWithIdentification
from library.crbcombobox     import CRBComboBox
from library.Utils           import forceRef, forceString

from ActionPropertyValueType import CActionPropertyValueType


class CTissueTypeActionPropertyValueType(CActionPropertyValueType):
    badDomain = u'Неверное описание области определения значения свойства действия типа "Тип биоматериала":\n%(domain)s'
    badKey = u'Недопустимый ключ "%(key)s" в описание области определения значения свойства действия типа "Тип биоматериала":\n%(domain)s'
    badValue = u'Недопустимое значение "%(val)s" ключа "%(key)s" в описание области определения значения свойства действия типа "Тип биоматериала":\n%(domain)s'

    name         = u'Тип биоматериала'
    variantType  = QVariant.Int


    class CTissueTypeInfo(CRBInfoWithIdentification):
        tableName = 'rbTissueType'


    class CPropEditor(CRBComboBox):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            CRBComboBox.__init__(self, parent)
            self.setShowFields(CRBComboBox.showCodeAndName)
            self.setTable('rbTissueType')
            self.setFilter(domain)

        def setValue(self, value):
            CRBComboBox.setValue(self, forceRef(value))


    def __init__(self, domain = None):
        CActionPropertyValueType.__init__(self, domain)
        self.rawDomain = domain
        self.domain = self.parseDomain(domain)


    def parseDomain(self, domain):
        codeList = []
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
                else:
                    raise ValueError, self.badKey % locals()
                    
        db = QtGui.qApp.db
        table = db.table('rbTissueType')
        cond = []
        if codeList:
            cond.append(table['code'].inlist(codeList))
        return db.joinAnd(cond)


    @staticmethod
    def convertDBValueToPyValue(value):
        values = forceString(value).split(':')
        if len(values) == 2:
            return forceRef(QtGui.qApp.db.translate('rbTissueType', 'code', values[1], 'id'))
        return forceRef(value)


    convertQVariantToPyValue = convertDBValueToPyValue


    def toText(self, v):
        return forceString(QtGui.qApp.db.translate('rbTissueType', 'id', v, 'CONCAT(code,\' | \',name)'))


    def toInfo(self, context, v):
        return CTissueTypeActionPropertyValueType.CTissueTypeInfo(context, v)


    def getTableName(self):
        return self.tableNamePrefix+'Integer'
