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
from PyQt4.QtCore import QString

from library.Identification import getIdentificationInfo, getIdentification
from library.exception        import CException
from library.PrintInfo import (
    CInfo,
    CTemplatableInfoMixin,
    CInfoList,
    CInfoProxyList,
    CDateTimeInfo, CRBInfo, CDateInfo, _identification,
)
from library.Utils            import (
                                      forceBool,
                                      forceDate,
                                      forceDateTime,
                                      forceDouble,
                                      forceInt,
                                      forceRef,
                                      forceString,
                                      forceStringEx
                                     )
from library.ESKLP.SmnnInfo   import CSmnnInfo
from Events.Action import CActionTypeCache, CAction, CActionType
from ActionProperty           import CActionProperty, CActionPropertyType
from Events.ContractTariffCache import CContractTariffCache
from Events.MapActionTypeToServiceIdList import CMapActionTypeIdToServiceIdList
from Events.MKBInfo           import CMKBInfo, CMorphologyMKBInfo
from RefBooks.Service.Info    import CServiceInfo
from Events.Utils import CCSGInfo
from Orgs.PersonInfo          import CPersonInfo
from Orgs.Utils               import COrgInfo, COrgStructureInfo, getActionTypeOrgStructureIdList
from RefBooks.Test.Info       import CTestInfo
from RefBooks.Unit.Info       import CUnitInfo
from RefBooks.Finance.Info    import CFinanceInfo

from Stock.StockMotionInfo    import CStockMotionInfo, CStockMotionItemInfo, CNomenclatureInfo
from TissueJournal.TissueInfo import CTakenTissueJournalInfo, CTissueTypeInfo, CContainerTypeInfo
#from library.Pacs.RestToolbox  import getRequest
from Registry.Utils import CQuotaTypeInfo


class CActionTypeTissueTypeInfoList(CInfoList):
    def __init__(self, context, actionTypeId):
        CInfoList.__init__(self, context)
        self._actionTypeId = actionTypeId

    def _load(self):
        if self._actionTypeId:
            self.idList = QtGui.qApp.db.getIdList('ActionType_TissueType', 'id', 'master_id=%d'%self._actionTypeId)
            self._items = [ self.getInstance(CActionTypeTissueTypeInfo, id) for id in self.idList ]
        else:
            self.idList = []
            self._items = []
        return True

class CActionTypeTissueTypeInfo(CInfo):
    def __init__(self, context, id):
        CInfo.__init__(self, context)
        self.id = id


    def _load(self):
        db = QtGui.qApp.db
        table = db.table('ActionType_TissueType')
        record = db.getRecordEx(table, '*', [table['id'].eq(self.id)])
        if record:
            self.initByRecord(record)
            return True
        else:
            self.initByRecord(db.dummyRecord())
            return False


    def initByRecord(self, record):
        self._amount = forceInt(record.value('amount'))
        self._type = self.getInstance(CTissueTypeInfo, forceRef(record.value('tissueType_id')))
        self._container = self.getInstance(CContainerTypeInfo, forceRef(record.value('containerType_id')))

    amount       = property(lambda self: self.load()._amount)
    type        = property(lambda self: self.load()._type)
    container        = property(lambda self: self.load()._container)


#class CActionTypeInfo(CInfo, CIdentificationInfoMixin):
class CActionTypeInfo(CInfo):
    def __init__(self, context, actionType):
        self.tableName = 'ActionType'
        CInfo.__init__(self, context)
        self._mapUrnToIdentifier = {}
        self._mapUrnToIdentifierInfo = {}
        self._mapCodeToIdentifierInfo = {}
        self._actionType = actionType
        self._loaded = True
        self._ok = True
        self._tissueTypeList = self.getInstance(CActionTypeTissueTypeInfoList, actionType.id if actionType else None)
        self._quotaTypeList = self.getInstance(CActionTypeQuotaTypeInfoList, actionType.id if actionType else None)


    def isServiceTypeProcedure(self):
        return self._actionType.isServiceTypeProcedure() if self._actionType else None


    def isServiceTypeResearch(self):
        return self._actionType.isServiceTypeResearch() if self._actionType else None


    def hasJobTicketPropertyType(self):
        return self._actionType.hasJobTicketPropertyType() if self._actionType else None


    def _getGroup(self):
        groupId = self._actionType.groupId if self._actionType else None
        actionType = CActionTypeCache.getById(groupId) if groupId else None
        return self.getInstance(CActionTypeInfo, actionType)


    def __nonzero__(self):
        return bool(self._actionType)


    def __cmp__(self, other):
        selfKey = self._actionType.id if self._actionType else None
        otherKey = other._actionType.id if other._actionType else None if isinstance(other, CActionTypeInfo) else None
        return cmp(selfKey, otherKey)


    def getOrgStructures(self, includeInheritance=False):
        idList = getActionTypeOrgStructureIdList(self._actionType.id, includeInheritance) if self._actionType else []
        return [self.getInstance(COrgStructureInfo, id) for id in idList]

    def identify(self, urn):
        if self._actionType.id:
            if urn in self._mapUrnToIdentifier:
                return self._mapUrnToIdentifier[urn]
            else:
                result = getIdentification(self.tableName, self._actionType.id, urn, False)
                self._mapUrnToIdentifier[urn] = result
                return result
        else:
            return None

    def identifyInfoByUrn(self, urn):
        if self._actionType.id:
            if urn in self._mapUrnToIdentifierInfo:
                return self._mapUrnToIdentifierInfo[urn]
            else:
                code, name, urn, version, value, note, checkDate = getIdentificationInfo(self.tableName, self._actionType.id, urn)
                result = _identification(code, name, urn, version, value, note, CDateInfo(checkDate))
                self._mapUrnToIdentifierInfo[urn] = result
                return result
        else:
            return _identification(None, None, None, None, None, None, None)

    def identifyInfoByCode(self, code):
        if self._actionType.id:
            if code in self._mapCodeToIdentifierInfo:
                return self._mapCodeToIdentifierInfo[code]
            else:
                code, name, urn, version, value, note, checkDate = getIdentificationInfo(self.tableName, self._actionType.id, code, byCode=True)
                result = _identification(code, name, urn, version, value, note, CDateInfo(checkDate))
                self._mapCodeToIdentifierInfo[code] = result
                return result
        else:
            return _identification(None, None, None, None, None, None, None)

    group   = property(_getGroup)
    id      = property(lambda self: self._actionType.id if self._actionType else None)
    class_  = property(lambda self: self._actionType.class_ if self._actionType else None)
    code    = property(lambda self: self._actionType.code  if self._actionType else None)
    flatCode= property(lambda self: self._actionType.flatCode if self._actionType else None)
    name    = property(lambda self: self._actionType.name  if self._actionType else None)
    title   = property(lambda self: self._actionType.title if self._actionType else None)
    showTime= property(lambda self: self._actionType.showTime if self._actionType else None)
    isMes  = property(lambda self: self._actionType.isMes if self._actionType else None)
    nomenclativeService = property(lambda self: self.getInstance(CServiceInfo, self._actionType.nomenclativeServiceId if self._actionType else None))
    isHtml  = property(lambda self: self._actionType.isHtml() if self._actionType else None)
    isImage = property(lambda self: self._actionType.isImage() if self._actionType else None)
    hasAssistant = property(lambda self: self._actionType.hasAssistant if self._actionType else None)
    orgStructures = property(getOrgStructures)
    serviceType = property(lambda self: self._actionType.serviceType if self._actionType else None)
    tissueTypeList = property(lambda self: self._tissueTypeList)
    ticketDuration = property(lambda self: self._actionType.ticketDuration if self._actionType else None)
    quotaType = property(lambda self: self._quotaTypeList)


class CActionTypeQuotaTypeInfoList(CInfoList):
    def __init__(self, context, actionTypeId):
        CInfoList.__init__(self, context)
        self._actionTypeId = actionTypeId

    def _load(self):
        if self._actionTypeId:
            self.idList = QtGui.qApp.db.getIdList('ActionType_QuotaType', 'id', 'master_id=%d'%self._actionTypeId)
            self._items = [ self.getInstance(CActionTypeQuotaTypeInfo, id) for id in self.idList ]
        else:
            self.idList = []
            self._items = []
        return True

class CActionExport(CInfo):
    def __init__(self, context, action):
        CInfo.__init__(self, context)
        self.action = action
        self._externalId = ''
        self._note = ''
        self._alter_externalId = ''
        self._note_Person = ''


    def _load(self):
        db = QtGui.qApp.db
        record = db.getRecordEx('Action_Export', '*', 'master_id=%d'%self.action)
        if record:
            self._externalId = forceString(record.value('externalId'))
            self._note = forceString(record.value('note'))
            self._alter_externalId = forceString(record.value('alter_externalId'))
            self._note_Person = forceString(record.value('note_Person'))
            return True
        else:
            return False

    externalId = property(lambda self: self.load()._externalId)
    note = property(lambda self: self.load()._note)
    alter_externalId = property(lambda self: self.load()._alter_externalId)
    note_Person = property(lambda self: self.load()._note_Person)

class CActionTypeQuotaTypeInfo(CInfo):
    def __init__(self, context, id):
        CInfo.__init__(self, context)
        self.id = id
    

    def _load(self):
        db = QtGui.qApp.db
        table = db.table('ActionType_QuotaType')
        record = db.getRecordEx(table, '*', [table['id'].eq(self.id)])
        if record:
            self._initByRecord(record)
            return True
        else:
            self._initByRecord(db.dummyRecord())
            return False


    def _initByRecord(self, record):
        self._quotaClass = forceInt(record.value('quotaClass'))
        self._quotaType = forceInt(record.value('quotaType_id'))
        self._financeId = forceString(record.value('finance_id'))


    quotaClass = property(lambda self: self.load()._quotaClass)
    quotaType = property(lambda self: self.getInstance(CQuotaTypeInfo, self.load()._quotaType))
    financeId = property(lambda self: self.load()._financeId)


class CActionTypeInfoList(CInfoList):
    def __init__(self, context):
        CInfoList.__init__(self, context)
        self._idList = []
        self._loaded = True
        self._ok = True


    def _setIdList(self, idList):
        self._idList = idList[:]
        self._items = [ self.getInstance(CActionTypeInfo, CActionTypeCache.getById(id))
                        for id in self._idList
                      ]


    idList = property(lambda self: self._idList, _setIdList)


class CCookedActionInfo(CActionTypeInfo, CTemplatableInfoMixin):
    def __init__(self, context, record, action):
        CActionTypeInfo.__init__(self, context, action.getType())
        self._record = record
        self._action = action
        self._eventInfo = None
# получается, что CActionInfo загружается при инициализации (зачем?)
# надо ли тут сделать отдельный метод load()???
        self._ok = self._load()
        self._loaded = True
        self._isDirty = False

        self._price = None
        self._servicesIdList = None
        self.currentPropertyIndex = -1

    def _load(self):
        if self._record:
            self._id = forceRef(self._record.value('id'))
            self._typeId = self._actionType.id
            self._classId = self._actionType.class_
            self._ticketDuration = self._actionType.ticketDuration
            self._expirationDate = self._actionType.expirationDate
            self._directionDate = CDateTimeInfo(forceDateTime(self._record.value('directionDate')))
            self._begDate = CDateTimeInfo(forceDateTime(self._record.value('begDate')))
            self._plannedEndDate = CDateTimeInfo(forceDateTime(self._record.value('plannedEndDate')))
            self._endDate = CDateTimeInfo(forceDateTime(self._record.value('endDate')))
            self._isUrgent = forceBool(self._record.value('isUrgent'))
            self._coordDate = CDateTimeInfo(forceDate(self._record.value('coordDate')))
            self._coordAgent = forceString(self._record.value('coordAgent'))
            self._coordInspector = forceString(self._record.value('coordInspector'))
            self._coordText = forceString(self._record.value('coordText'))
            self._status = forceInt(self._record.value('status'))
            self._office = forceString(self._record.value('office'))
            self._note = forceString(self._record.value('note'))
            self._export = self.getInstance(CActionExport, self._id)
            self._amount = forceDouble(self._record.value('amount'))
            self._quantity = forceInt(self._record.value('quantity'))
            self._uet = forceDouble(self._record.value('uet'))
            self._financeId = forceRef(self._record.value('finance_id'))
            self._setPerson = self.getInstance(CPersonInfo, forceRef(self._record.value('setPerson_id')))
            self._person = self.getInstance(CPersonInfo, forceRef(self._record.value('person_id')))
            self._assistant = self.getInstance(CPersonInfo, forceRef(self._record.value('assistant_id')) if self.hasAssistant else None)
            self._expose = forceBool(self._record.value('expose'))
            self._account = forceBool(self._record.value('account'))
            self._MKB = self.getInstance(CMKBInfo, forceString(self._record.value('MKB')))
            self._exSubclassMKB = forceString(self._record.value('exSubclassMKB'))
            self._morphologyMKB = self.getInstance(CMorphologyMKBInfo, forceString(self._record.value('morphologyMKB')))
            self._takenTissueJournal = self.getInstance(CTakenTissueJournalInfo, forceRef(self._record.value('takenTissueJournal_id')))
            self._duration = forceInt(self._record.value('duration'))
            self._periodicity = forceInt(self._record.value('periodicity'))
            self._aliquoticity = forceInt(self._record.value('aliquoticity'))
            self._payStatus = forceInt(self._record.value('payStatus'))
            self._prescriptionId = forceInt(self._record.value('prescription_id'))
            self._csg = self.getInstance(CCSGInfo, forceInt(self._record.value('EventCSG_id')))
            self._prevAction = self.getInstance(CActionInfo, forceInt(self._record.value('prevAction_id')))
            self._createDatetime = CDateTimeInfo(forceDateTime(self._record.value('createDatetime')))
            self._createPerson = self.getInstance(CPersonInfo, forceRef(self._record.value('createPerson_id')))
            self._modifyDatetime = CDateTimeInfo(forceDateTime(self._record.value('modifyDatetime')))
            self._modifyPerson = self.getInstance(CPersonInfo, forceRef(self._record.value('modifyPerson_id')))
            self._orgStructure = self.getInstance(COrgStructureInfo, forceRef(self._record.value('OrgStructure_id')))
            self._specification = self.getInstance(CActionSpecificationInfo, forceRef(self._record.value('actionSpecification_id')))
            self._additional = forceBool(self._record.value('additional'))
            return True
        else:
            self._id = None
            self._typeId = None
            self._classId = None
            self._ticketDuration = None
            self._expirationDate = None
            self._directionDate = CDateTimeInfo(None)
            self._begDate = CDateTimeInfo(None)
            self._plannedEndDate = CDateTimeInfo(None)
            self._endDate = CDateTimeInfo(None)
            self._isUrgent = False
            self._coordDate = CDateTimeInfo(None)
            self._coordAgent = ''
            self._coordInspector = ''
            self._coordText = ''
            self._status = 0
            self._office = ''
            self._note = ''
            self._export = ''
            self._amount = 0.0
            self._quantity = 0
            self._uet = 0.0
            self._financeId = None
            self._setPerson = self.getInstance(CPersonInfo, None)
            self._person = self.getInstance(CPersonInfo, None)
            self._assistant = self.getInstance(CPersonInfo, None)
            self._expose = False
            self._account = False
            self._MKB = self.getInstance(CMKBInfo, None)
            self._exSubclassMKB = ''
            self._morphologyMKB = self.getInstance(CMorphologyMKBInfo, None)
            self._takenTissueJournal = self.getInstance(CTakenTissueJournalInfo, None)
            self._payStatus = 0
            self._prescriptionId = None
            self._csg = self.getInstance(CCSGInfo, None)
            self._prevAction = self.getInstance(CActionInfo, None)
            self._createDatetime = CDateTimeInfo(None)
            self._createPerson = self.getInstance(CPersonInfo, None)
            self._modifyDatetime = CDateTimeInfo(None)
            self._modifyPerson = self.getInstance(CPersonInfo, None)
            self._orgStructure = self.getInstance(COrgStructureInfo, None)
            self._specification = self.getInstance(CActionSpecificationInfo, None)
            self._additional = False
            return False


    def getPrintTemplateContext(self):
        return self._action.getType().context if self._action.getType() else None


    def getEventInfo(self):
        if not self._eventInfo:
            from Events.EventInfo import CEventInfo
            eventId = forceRef(self._record.value('event_id')) if self._record else None
            self._eventInfo = self.getInstance(CEventInfo, eventId)
        return self._eventInfo


    def getFinanceInfo(self):
        financeId = forceRef(self._record.value('finance_id')) if self._record else None
        if financeId:
            return self.getInstance(CFinanceInfo, financeId)
        else:
            return self.getEventInfo().finance


    def getContractInfo(self):
        from Events.EventInfo import CContractInfo
        contractId = forceRef(self._record.value('contract_id')) if self._record else None
        if contractId:
            return self.getInstance(CContractInfo, contractId)
        else:
            return self.getEventInfo().contract


    def _getTariffDescr(self):
        event = self.getEventInfo()
        return event.getTariffDescrEx(self.getContractInfo().id)


    def _getServicesIdList(self):
        if self._servicesIdList is None:
            if not hasattr(self.context, 'mapActionTypeIdToServiceIdList'):
                self.context.mapActionTypeIdToServiceIdList = CMapActionTypeIdToServiceIdList()
            actionTypeId = self._actionType.id
            financeId = self.getFinanceInfo().id
            self._servicesIdList = self.context.mapActionTypeIdToServiceIdList.getActionTypeServiceIdList(actionTypeId, financeId)
        return self._servicesIdList


    def getServices(self):
        return [ self.getInstance(CServiceInfo, serviceId)
                 for serviceId in self._getServicesIdList()
               ]


    def getService(self):
        servicesIdList = self._getServicesIdList()
        serviceId = servicesIdList[0] if servicesIdList else None
        return self.getInstance(CServiceInfo, serviceId)


    def getPrice(self):
        if self._price is None:
            tariffDescr = self._getTariffDescr()
            tariffMap = tariffDescr.actionTariffMap
            tariffCategoryId = self.person.tariffCategory.id
            self._price = CContractTariffCache.getPrice(tariffMap, self._getServicesIdList(), tariffCategoryId)
        return self._price


    def getServicePrice(self, serviceId): # алгоритм взят из self.getPrice()
        tariffDescr = self._getTariffDescr()
        tariffMap = tariffDescr.actionTariffMap
        tariffCategoryId = self.person.tariffCategory.id
        return CContractTariffCache.getPrice(tariffMap, [serviceId, ], tariffCategoryId)


    def getOrgInfo(self):
        orgId = forceRef(self._record.value('org_id')) if self._record else None
        if not orgId:
            orgId = self._actionType.defaultOrgId
        return self.getInstance(COrgInfo, orgId)


    def getStockMotionInfo(self):
        result = self.getInstance(CStockMotionInfo, None)
        stockMotionRecord = self._action.getStockMotionRecord()
        if stockMotionRecord:
            result.setRecord(stockMotionRecord)
            result._items = [self.getInstance(CStockMotionItemInfo, None).setRecord(itemRecord).setOkLoaded() for itemRecord in self._action.getStockMotionItemList()]
        return result


    def getNomenclaturePrice(self, propertyName):
        nomenclatureId = self[propertyName].value.id
        nomenclatureItem = self.getStockMotionInfo().getNomenclatureItem(nomenclatureId)
        if nomenclatureItem:
            return nomenclatureItem._sum
        return None


    def getData(self):
        itemId = forceRef(self._record.value('id')) if self._record else None
        eventInfo = self.getEventInfo()
        eventActions = eventInfo.actions
        eventActions._idList = [itemId]
        eventActions._items  = [self]
        eventActions._loaded = True

        return { 'event'  : eventInfo,
                 'action' : self,
                 'client' : eventInfo.client,
                 'actions': eventActions,
                 'currentActionIndex': 0,
                 'tempInvalid': None
               }


    def setCurrentPropertyIndex(self, currentPropertyIndex):
        self.currentPropertyIndex = currentPropertyIndex


    id = property(lambda self: self.load()._id)
    typeId = property(lambda self: self.load()._typeId)
    classId = property(lambda self: self.load()._classId)
    ticketDuration = property(lambda self: self.load()._ticketDuration)
    expirationDate = property(lambda self: self.load()._expirationDate)
    event = property(getEventInfo)
    directionDate = property(lambda self: self.load()._directionDate)
    begDate = property(lambda self: self.load()._begDate)
    plannedEndDate = property(lambda self: self.load()._plannedEndDate)
    endDate = property(lambda self: self.load()._endDate)
    isUrgent = property(lambda self: self.load()._isUrgent)
    coordDate = property(lambda self: self.load()._coordDate)
    coordAgent = property(lambda self: self.load()._coordAgent)
    coordInspector = property(lambda self: self.load()._coordInspector)
    coordText = property(lambda self: self.load()._coordText)
    status = property(lambda self: self.load()._status)
    office = property(lambda self: self.load()._office)
    note = property(lambda self: self.load()._note)
    export = property(lambda self: self.load()._export)
    amount = property(lambda self: self.load()._amount)
    quantity = property(lambda self: self.load()._quantity)
    uet = property(lambda self: self.load()._uet)
    setPerson = property(lambda self: self.load()._setPerson)
    person = property(lambda self: self.load()._person)
    assistant = property(lambda self: self.load()._assistant)
    expose = property(lambda self: self.load()._expose)
    account = property(lambda self: self.load()._account)
    MKB = property(lambda self: self.load()._MKB)
    exSubclassMKB = property(lambda self: self.load()._exSubclassMKB)
    morphologyMKB = property(lambda self: self.load()._morphologyMKB)
    duration = property(lambda self: self.load()._duration)
    periodicity = property(lambda self: self.load()._periodicity)
    aliquoticity = property(lambda self: self.load()._aliquoticity)
    services = property(getServices)
    service = property(getService) ### kill it!
    price = property(getPrice)
    contract = property(getContractInfo)
    finance = property(getFinanceInfo)
    takenTissueJournal = property(lambda self: self.load()._takenTissueJournal)
    stockMotion = property(getStockMotionInfo)
    organisation = property(getOrgInfo)
    payStatus = property(lambda self: self.load()._payStatus)
    prescriptionId = property(lambda self: self.load()._prescriptionId)
    csg = property(lambda self: self.load()._csg)
    pacs = property(lambda self: self.load()._pacs)
    isDirty = property(lambda self: self._isDirty)
    prevAction = property(lambda self: self._prevAction)
    createDatetime = property(lambda self: self._createDatetime)
    createPerson = property(lambda self: self._createPerson)
    modifyDatetime = property(lambda self: self._modifyDatetime)
    modifyPerson = property(lambda self: self._modifyPerson)
    orgStructure = property(lambda self: self.load()._orgStructure)
    specification = property(lambda self: self.load()._specification)
    additional = property(lambda self: self.load()._additional)


    def getPropertyByShortName(self, key):
        if isinstance(key, (basestring, QString)):
            try:
                return self.getInstance(CPropertyInfo, self._action.getPropertyByShortName(unicode(key)))
            except KeyError:
                actionType = self._action.getType()
                raise CException(u'Действие типа "%s" не имеет свойства с коротким наименованием"%s"' % (actionType.name, unicode(key)))


    def __len__(self):
        self.load()
        return len(self._action.getProperties())


    def __getitem__(self, key):
        if isinstance(key, (basestring, QString)):
            try:
                return self.getInstance(CPropertyInfo, self._action.getProperty(unicode(key)))
            except KeyError:
                actionType = self._action.getType()
                raise CException(u'Действие типа "%s" не имеет свойства "%s"' % (actionType.name, unicode(key)))
        if isinstance(key, (int, long)):
            try:
                return self.getInstance(CPropertyInfo, self._action.getPropertyByIndex(key))
            except IndexError:
                actionType = self._action.getType()
                raise CException(u'Действие типа "%s" не имеет свойства c индексом "%s"' % (actionType.name, unicode(key)))
        else:
            raise TypeError, u'Action property subscription must be string or integer'


    def __iter__(self):
        for property in self._action.getProperties():
            yield self.getInstance(CPropertyInfo, property)


    def __contains__(self, key):
        if isinstance(key, (basestring, QString)):
            return unicode(key) in self._action.getPropertiesByName()
        if isinstance(key, (int, long)):
            return 0<=key<len(self._action.getPropertiesById())
        else:
            raise TypeError, u'Action property subscription must be string or integer'


class CActionInfo(CCookedActionInfo):
    def __init__(self, context, actionId):
        action = CAction.getActionById(actionId)
        if action:
            CCookedActionInfo.__init__(self, context, action.getRecord() if action else None, action)


class CUnitInfo(CRBInfo):
    tableName = 'rbUnit'

    def _load(self):
        db = QtGui.qApp.db
        record = db.getRecord(self.tableName, '*', self.id) if self.id else None
        if record:
            self._code = forceString(record.value('code'))
            self._name = forceString(record.value('name'))
            self._latinName = forceString(record.value('latinName'))
            self._initByRecord(record)
            return True
        else:
            self._code = ''
            self._name = ''
            self._latinName = ''
            self._initByNull()
            return False

    code = property(lambda self: self.load()._code)
    name = property(lambda self: self.load()._name)
    latinName = property(lambda self: self.load()._latinName)


class CPropertyInfo(CInfo):
    def __init__(self, context, property):
        CInfo.__init__(self, context)
        self._property = property
        self._loaded = True
        self._ok = True

    value = property(lambda self: self._property.getInfo(self.context))
    name  = property(lambda self: self._property._type.name)
    age  = property(lambda self: self._property._type.age[1] if self._property._type.age else '')
    shortName  = property(lambda self: self._property._type.shortName)
    descr = property(lambda self: self._property._type.descr)
    sectionCDA = property(lambda self: self._property._type.sectionCDA)
    type = property(lambda self: self._property._type.typeName)
    id = property(lambda self: self._property.getId())
    unit  = property(lambda self: self.getInstance(CUnitInfo, self._property.getUnitId()))
    norm  = property(lambda self: self._property.getNorm())
    isAssigned = property(lambda self: self._property.isAssigned())
    evaluation = property(lambda self: self._property.getEvaluation())
    isHtml  = property(lambda self: self._property.isHtml())
    isImage = property(lambda self: self._property.isImage())
    test = property(lambda self: self.getInstance(CTestInfo, self._property._type.testId))
    sex = property(lambda self: self._property._type.sex)
    penalty = property(lambda self: self._property._type.penalty)
    visibleInJobTicket = property(lambda self: self._property._type.visibleInJobTicket)
    visibleInTableEditor = property(lambda self: self._property._type.visibleInTableEditor)
    inPlanOperatingDay = property(lambda self: self._property._type.inPlanOperatingDay)
    inMedicalDiagnosis = property(lambda self: self._property._type.inMedicalDiagnosis)


    def __str__(self):
#        v = self._property.getValue()
#        return forceString(v) if v else ''
        return forceString(self.value)


class CActionInfoList(CInfoList):
    def __init__(self, context, eventId):
        CInfoList.__init__(self, context)
        self.eventId = eventId
        self._idList = []

    def _load(self):
        db = QtGui.qApp.db
        table = db.table('Action')
        self._idList = db.getIdList(table, 'id', [table['event_id'].eq(self.eventId), table['deleted'].eq(0)], 'id')
        self._items = [ self.getInstance(CActionInfo, id) for id in self._idList ]
        return True


class CActionSelectedInfoProxyList(CInfoProxyList):
    def __init__(self, context, modelsItems, eventInfo):
        CInfoProxyList.__init__(self, context)
        self._rawItems = []
        for items in modelsItems:
            if items:
                self._rawItems.extend(items)
        self._items = [ None ]*len(self._rawItems)
        self._eventInfo = eventInfo

    def _getItemEx(self, key):
        record, action = self._rawItems[key]
        v = self.getInstance(CCookedActionInfo, record, action)
        v._eventInfo = self._eventInfo
        return v

    def __getitem__(self, key):
        if isinstance(key, slice):
            for i in range(key.start or 0, key.stop or len(self._items), key.step or 1):
                val = self._items[i]
                if val is None:
                    self._items[i] = self._getItemEx(i)
        v = self._items[key]
        if v is None:
            v = self._getItemEx(key)
            self._items[key] = v
        return v


class CActionInfoProxyList(CInfoProxyList):
    def __init__(self, context, models, eventInfo):
        CInfoProxyList.__init__(self, context)
        self._rawItems = []
        for model in models:
            self._rawItems.extend(model.items())
        self._items = [ None ]*len(self._rawItems)
        self._eventInfo = eventInfo

    def _getItemEx(self, key):
        record, action = self._rawItems[key]
        if not action:
            return None
        v = self.getInstance(CCookedActionInfo, record, action)
        v._eventInfo = self._eventInfo
        return v

    def __getitem__(self, key):
        if isinstance(key, slice):
            for i in range(key.start or 0, key.stop or len(self._items), key.step or 1):
                val = self._items[i]
                if val is None:
                    self._items[i] = self._getItemEx(i)
        v = self._items[key]
        if v is None:
            v = self._getItemEx(key)
            self._items[key] = v
        return v


class CLocActionInfoProxyList(CActionInfoProxyList):
    def __init__(self, context, models, eventInfo):
        CActionInfoProxyList.__init__(self, context)


# TODO: не должен ли этот класс наследоваться от CActionInfoProxyList???
class CLocActionInfoList(CInfoProxyList):
    def __init__(self, context, idList, clientSex=0, clientAge=0, type_ = CCookedActionInfo):
        CInfoProxyList.__init__(self, context)
        self.idList = idList
        self._items = [ None ]*len(self.idList)
        self.clientSex = clientSex
        self.clientAge = clientAge
        self._type = type_


    def __getitem__(self, key):
        v = self._items[key]
        if v is None:
            action = CAction.getActionById(self.idList[key])
            v = self.getInstance(self._type, action.getRecord(), action)
            self._items[key] = v
        return v


class CCookedNotActionInfo(CCookedActionInfo):
    def __init__(self, context, record, action):
        CCookedActionInfo.__init__(self, context, record, action)

    def getPrintTemplateContext(self):
        return None

    def getStockMotionInfo(self):
        return None

    def __len__(self):
        self.load()
        return len(self._items)


    def __getitem__(self, key):
        self.load()
        return self._items[key]


    def __iter__(self):
        self.load()
        return iter(self._items)


    def __contains__(self, key):
        return len(self._items)


class CPlanOperatingDayInfo(CCookedActionInfo):
    def __init__(self, context, record, action):
        if action:
            CCookedActionInfo.__init__(self, context, action.getRecord(), action)
        else:
            CCookedNotActionInfo.__init__(self, context, record, action)


class CPlanOperatingDayInfoList(CActionInfoProxyList):
    def __init__(self, context, models, eventInfo):
        CActionInfoProxyList.__init__(self, context, models, eventInfo)
        self._rawItems = []
        for model in models:
            self._rawItems.extend(model.items())
        self._items = [ None ]*len(self._rawItems)
        self._eventInfo = eventInfo

    def _getItemEx(self, key):
        record, action = self._rawItems[key]
        v = self.getInstance(CPlanOperatingDayInfo, record, action)
        v._eventInfo = self._eventInfo
        return v


class CMedicalDiagnosisInfo(CCookedActionInfo):
    def __init__(self, context, record, action):
        CCookedActionInfo.__init__(self, context, action.getRecord(), action)


class CMedicalDiagnosisInfoList(CActionInfoProxyList):
    def __init__(self, context, models, eventInfo):
        CActionInfoProxyList.__init__(self, context, models, eventInfo)
        self._rawItems = []
        for model in models:
            self._rawItems.extend(model.items())
        self._items = [ None ]*len(self._rawItems)
        self._eventInfo = eventInfo

    def _getItemEx(self, key):
        record, action = self._rawItems[key]
        v = self.getInstance(CMedicalDiagnosisInfo, record, action)
        v._eventInfo = self._eventInfo
        return v


class CActionInfoListEx(CInfoList):
    def __init__(self, context, actionIdList):
        CInfoList.__init__(self, context)
        self._idList = actionIdList

    def _load(self):
        self._items = [ self.getInstance(CActionInfo, id) for id in self._idList ]
        return True

class CActionSpecificationInfo(CRBInfo):
    tableName = 'rbActionSpecification'


class CLocActionPropertyMedicamentInfoList(CInfoList):
    def __init__(self, context, records):
        CInfoList.__init__(self, context)
        self._records = records
        self._items = []


    def _load(self):
        if self._records:
            self._items = [self.getInstance(CLocActionPropertyMedicamentInfo, record) for record in self._records]
        else:
            self._items = []
        return True


class CLocActionPropertyMedicamentInfo(CInfo):
    def __init__(self, context, record):
        CInfo.__init__(self, context)
        self._record = record
        self._ok = self._load()
        self._loaded = True
        self._isDirty = False


    def _load(self):
        if self._record:
            self._id = forceRef(self._record.value('id'))
            self._createDatetime = CDateTimeInfo(forceDateTime(self._record.value('createDatetime')))
            self._createPerson = self.getInstance(CPersonInfo, forceRef(self._record.value('createPerson_id')))
            self._modifyDatetime = CDateTimeInfo(forceDateTime(self._record.value('modifyDatetime')))
            self._modifyPerson = self.getInstance(CPersonInfo, forceRef(self._record.value('modifyPerson_id')))
            self._deleted = forceInt(self._record.value('deleted'))
            self._idx = forceInt(self._record.value('idx'))
            self._masterAction = self.getInstance(CActionInfo, forceRef(self._record.value('master_id')))
            self._action = self.getInstance(CActionInfo, forceRef(self._record.value('action_id')))
            self._nomenclature = self.getInstance(CNomenclatureInfo, forceRef(self._record.value('actionPropertyNomenclature_id')))
            self._smnnUUID = forceStringEx(self._record.value('smnnUUID'))
            self._smnn = self.getInstance(CSmnnInfo, self._smnnUUID)
            self._duration = forceString(self._record.value('duration'))
            self._periodicity = forceString(self._record.value('periodicity'))
            self._aliquoticity = forceString(self._record.value('aliquoticity'))
            return True
        else:
            self._id = None
            self._createDatetime = CDateTimeInfo(None)
            self._createPerson = self.getInstance(CPersonInfo, None)
            self._modifyDatetime = CDateTimeInfo(None)
            self._modifyPerson = self.getInstance(CPersonInfo, None)
            self._deleted = 0
            self._idx = 0
            self._masterAction = self.getInstance(CActionInfo, None)
            self._action = self.getInstance(CActionInfo, None)
            self._nomenclature = self.getInstance(CNomenclatureInfo, None)
            self._smnnUUID = None
            self._smnn = self.getInstance(CSmnnInfo, None)
            self._duration = ''
            self._periodicity = ''
            self._aliquoticity = ''
            return False


    id = property(lambda self: self.load()._id)
    createDatetime = property(lambda self: self._createDatetime)
    createPerson = property(lambda self: self._createPerson)
    modifyDatetime = property(lambda self: self._modifyDatetime)
    modifyPerson = property(lambda self: self._modifyPerson)
    deleted = property(lambda self: self.load()._deleted)
    idx = property(lambda self: self.load()._idx)
    masterAction = property(lambda self: self.load()._masterAction)
    action = property(lambda self: self.load()._action)
    nomenclature = property(lambda self: self.load()._nomenclature)
    smnnUUID = property(lambda self: self.load()._smnnUUID)
    smnn = property(lambda self: self.load()._smnn)
    duration = property(lambda self: self.load()._duration)
    periodicity = property(lambda self: self.load()._periodicity)
    aliquoticity = property(lambda self: self.load()._aliquoticity)


class CLocActionPropertyActionsInfoList(CInfoList):
    def __init__(self, context, records):
        CInfoList.__init__(self, context)
        self._records = records
        self._items = []


    def _load(self):
        if self._records:
            self._items = [self.getInstance(CLocActionPropertyActionsInfo, record) for record in self._records]
        else:
            self._items = []
        return True


class CLocActionPropertyActionsInfo(CInfo):
    def __init__(self, context, record):
        CInfo.__init__(self, context)
        self._record = record
        self._ok = self._load()
        self._loaded = True
        self._isDirty = False


    def _load(self):
        if self._record:
            db = QtGui.qApp.db
            tableA = db.table('Action')
            tableAT = db.table('ActionType')
            tableAP = db.table('ActionProperty')
            tableAPT = db.table('ActionPropertyType')
            actionId = forceRef(self._record.value('action_id'))
            if actionId:
                actionType = None
                propertyIdList = []
                propertyList = []
                propertyItems = self._record.aboutMERProperties.getItems()
                for propertyItem in propertyItems:
                    propertyId = forceRef(propertyItem.value('actionProperty_id'))
                    if propertyId and propertyId not in propertyIdList:
                        propertyIdList.append(propertyId)
                if propertyIdList:
                    actionRecord = db.getRecordEx(tableA, [tableA['actionType_id']], [tableA['id'].eq(actionId), tableA['deleted'].eq(0)])
                    actionTypeId = forceRef(actionRecord.value('actionType_id')) if actionRecord else None
                    if actionTypeId:
                        actionTypeRecord = db.getRecordEx(tableAT, '*', [tableAT['id'].eq(actionTypeId), tableAT['deleted'].eq(0)])
                        actionType = CActionType(record=actionTypeRecord)
                    propsCond = [
                        tableAP['id'].inlist(propertyIdList),
                        tableAP['action_id'].eq(actionId),
                        tableAP['deleted'].eq(0),
                    ]
                    recordProps = db.getRecordList(tableAP, [tableAP['id'], tableAP['type_id']], propsCond)
                    for recordProp in recordProps:
                        propId = forceRef(recordProp.value('id'))
                        propTypeId = forceRef(recordProp.value('type_id'))
                        if propId and propTypeId:
                            propRecord = db.getRecord(tableAP, '*', propId)
                            propTypeRecord = db.getRecord(tableAPT, '*', propTypeId)
                            propType = CActionPropertyType(propTypeRecord)
                            prop = CActionProperty(actionType=actionType, record=propRecord, type=propType)
                            propertyList.append(prop)
                self._id = forceRef(self._record.value('id'))
                self._idx = forceInt(self._record.value('idx'))
                self._action = self.getInstance(CActionInfo, actionId)
                self._masterAction = self.getInstance(CActionInfo, forceRef(self._record.value('master_id')))
                self._properties = [self.getInstance(CPropertyInfo, p) for p in propertyList]
                self._additional = forceBool(self._record.value('additional'))
                return True
            else:
                self._id = None
                self._idx = 0
                self._action = self.getInstance(CActionInfo, None)
                self._masterAction = self.getInstance(CActionInfo, None)
                self._properties = []
                self._additional = False
                return False
        else:
            self._id = None
            self._idx = 0
            self._action = self.getInstance(CActionInfo, None)
            self._masterAction = self.getInstance(CActionInfo, None)
            self._properties = []
            self._additional = False
            return False


    id = property(lambda self: self.load()._id)
    idx = property(lambda self: self.load()._idx)
    action = property(lambda self: self.load()._action)
    masterAction = property(lambda self: self.load()._masterAction)
    properties = property(lambda self: self.load()._properties)
    additional = property(lambda self: self.load()._additional)
