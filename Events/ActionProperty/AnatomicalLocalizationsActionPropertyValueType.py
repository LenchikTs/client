# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2023 SAMSON Group. All rights reserved.
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

from Registry.AnatomicalLocalizationsComboBox import CAnatomicalLocalizationsComboBox
from library.PrintInfo import CRBInfo, CInfo
from library.Utils import forceRef, forceString, trim
from ActionPropertyValueType   import CActionPropertyValueType
from library.crbcombobox import CRBModelDataCache


class CAnatomicalLocalizationsActionPropertyValueType(CActionPropertyValueType):
    name         = u'Анатомическая локализация'
    variantType  = QVariant.String
    isCopyable   = False
    badDomain   = u'Неверное описание области определения значения свойства действия типа Анатомическая локализация:\n%(domain)s'
    badKey      = u'Недопустимый ключ "%(key)s" в описание области определения значения свойства действия типа Анатомическая локализация:\n%(domain)s'


    class CPropEditor(CAnatomicalLocalizationsComboBox):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            CAnatomicalLocalizationsComboBox.__init__(self, parent, filter=u','.join(i for i in domain if i))


        def setValue(self, value):
            value = forceString(value)
            if value:
                idList = [trim(_id) for _id in value.split(u',')]
                if idList:
                    self.values = idList


    def __init__(self, domain = None):
        CActionPropertyValueType.__init__(self, domain)
        self.domain = self.parseDomain(domain)
        self._tableName = 'rbAnatomicalLocalizations'
        self._addNone = True
        self._needCache = True
        self._filter = ''
        self._order = ''
        self._specialValues = None
        self._data = None
        self._mapShown2Id = {}
        self._mapId2Shown = {}
        self._initRB()


    def _initRB(self):
        self._data = CRBModelDataCache.getData(self._tableName,
                                               self._addNone,
                                               self._filter,
                                               self._order,
                                               self._specialValues,
                                               self._needCache)
        for itemIndex in xrange(self._data.getCount()):
            _id = self._data.getId(itemIndex)
            shown = u' | '.join([unicode(self._data.getCode(itemIndex)), unicode(self._data.getName(itemIndex))])

            self._mapId2Shown[str(_id)] = shown
            self._mapShown2Id[shown] = unicode(_id)


    def parseDomain(self, domain):
        db = QtGui.qApp.db
        anatomicalLocalizationsCode = ''
        val = ''
        for word in domain.split(','):
            if word:
                parts = word.split(':')
                if len(parts) == 1:
                    key = parts[0].strip()
                elif len(parts) == 2:
                    key, val = parts[0].strip(), parts[1].strip()
                else:
                    raise ValueError, self.badDomain % locals()
                keylower = key.lower()
                vallower = val.lower()
                if keylower == u'код':
                    anatomicalLocalizationsCode = vallower
                else:
                    raise ValueError, self.badKey % locals()
        db = QtGui.qApp.db
        table = db.table('rbAnatomicalLocalizations')
        cond = []
        if anatomicalLocalizationsCode:
            record = db.getRecordEx(table, [table['id']], [table['code'].like(anatomicalLocalizationsCode)])
            if record:
                anatomicalLocalizationsId = forceRef(record.value('id'))
                if anatomicalLocalizationsId:
                    anatomicalLocalizationsIdList = db.getDescendants('rbAnatomicalLocalizations', 'group_id', anatomicalLocalizationsId)
                    if anatomicalLocalizationsIdList:
                        cond.append(table['id'].inlist(anatomicalLocalizationsIdList))
        idList = db.getDistinctIdList(table, 'rbAnatomicalLocalizations.id', cond)
        theseAndParentIdList = []
        if idList:
            theseAndParentIdList = db.getTheseAndParents('rbAnatomicalLocalizations', 'group_id', idList)
        if theseAndParentIdList:
            return [table['id'].inlist(theseAndParentIdList)]
        return None


    @staticmethod
    def convertDBValueToPyValue(value):
        return forceString(value)


    convertQVariantToPyValue = convertDBValueToPyValue


    def toText(self, v):
        value = forceString(v)
        if value:
            idList = [trim(_id) for _id in value.split(',')]
            if idList:
                value = [self._mapId2Shown[_id] for _id in idList]
                if value:
                    return u'‚ '.join(value)
        return u''


    def toInfo(self, context, v):
        value = forceString(v)
        infoList = []
        if value:
            infoList = [CAnatomicalLocalizationsActionPropertyValueType.CRBInfoEx(context, self._tableName, trim(_id)) for _id in
                        value.split(',')]
        return infoList


    @classmethod
    def getTableName(cls):
        return cls.tableNamePrefix+'String'


    class CRBInfoEx(CRBInfo):
        def __init__(self, context, tableName, _id):
            CInfo.__init__(self, context)
            self.id = _id
            self.tableName = tableName
