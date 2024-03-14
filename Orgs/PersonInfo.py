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

from PyQt4 import QtGui

from library.PrintInfo          import (
                                         CInfo,
                                         CInfoList,
                                         CDateInfo,
                                         CDateTimeInfo,
                                         CRBInfo,
                                         CDictInfoMixin,
                                       )
from Utils import COrgInfo, COrgStructureInfo, CActivityInfo

from RefBooks.DocumentType.Info import CDocumentTypeInfo
from RefBooks.Post.Info         import CPostInfo
from RefBooks.Speciality.Info   import CSpecialityInfo

from library.Utils              import (
                                         forceDate,
                                         forceInt,
                                         forceRef,
                                         forceString,
                                         formatNameInt,
                                         formatShortNameInt,
                                         formatSNILS,
                                         formatSex,
                                       )


class CPersonInfo(CInfo):
    def __init__(self, context, personId):
        CInfo.__init__(self, context)
        self.personId = personId
        self._code = ''
        self._federalCode = ''
        self._regionalCode = ''
        self._lastName = ''
        self._firstName = ''
        self._patrName = ''
        self._sex = 0
        self._office = ''
        self._office2 = ''
        self._contacts = ''
        self._organisation = self.getInstance(COrgInfo, None)
        self._orgStructure = self.getInstance(COrgStructureInfo, None)
        self._speciality     = self.getInstance(CSpecialityInfo, None)
        self._post           = self.getInstance(CPostInfo, None)
        self._tariffCategory = self.getInstance(CTariffCategoryInfo, None)
        self._academicDegree = ''
        self._login = ''
        self._sex = ''
        self._orders = None
        self._educations = None
        self._SNILS = ''
        self._birthDate = CDateInfo(None)
        self._primaryQuota = 0
        self._ownQuota = 0
        self._consultancyQuota = 0
        self._externalQuota = 0
        self._identification = self.getInstance(CPersonIdentificationInfo, None)


    def _load(self):
        db = QtGui.qApp.db
        record = db.getRecord('Person', '*', self.personId)
        if record:
            self._code = forceString(record.value('code'))
            self._federalCode = forceString(record.value('federalCode'))
            self._regionalCode = forceString(record.value('regionalCode'))
            self._lastName = forceString(record.value('lastName'))
            self._firstName = forceString(record.value('firstName'))
            self._patrName = forceString(record.value('patrName'))
            self._sex = formatSex(forceInt(record.value('sex')))
            self._sexCode = forceInt(record.value('sex'))
            self._office = forceString(record.value('office'))
            self._office2 = forceString(record.value('office2'))
            self._contacts = getPersonPhones(self.personId)

            self._organisation = self.getInstance(COrgInfo, forceRef(record.value('org_id')))
            self._orgStructure = self.getInstance(COrgStructureInfo, forceRef(record.value('orgStructure_id')))
            self._speciality = self.getInstance(CSpecialityInfo, forceRef(record.value('speciality_id')))
            self._post = self.getInstance(CPostInfo, forceRef(record.value('post_id')))
            self._tariffCategory = self.getInstance(CTariffCategoryInfo, forceRef(record.value('tariffCategory_id')))
            self._academicDegree = forceString(record.value('academicDegree'))
            self._login = forceString(record.value('login'))
            self._educations = self.getInstance(CEducationInfoList, forceRef(record.value('id')))
            self._activities = self.getInstance(CPersonActivitiesInfoList, forceRef(record.value('id')))
            self._SNILS     = formatSNILS(forceString(record.value('SNILS')))
            self._birthDate = CDateInfo(record.value('birthDate'))
            self._primaryQuota = forceInt(record.value('primaryQuota'))
            self._ownQuota = forceInt(record.value('ownQuota'))
            self._consultancyQuota = forceInt(record.value('consultancyQuota'))
            self._externalQuota = forceInt(record.value('externalQuota'))
            self._identification = self.getInstance(CPersonIdentificationInfo, self.personId)
            return True
        else:
            return False

    def getPostIdentifyNote(self, url=None, postId=None):
        if url is None:
            return u'не указан справочник'
        if postId is None:
            return u'не указан идентификатор должности'
        record = QtGui.qApp.db.getRecordEx('rbPost_Identification', 'note',
                                           'system_id = (SELECT id FROM rbAccountingSystem `as` WHERE `as`.urn = "%s") and deleted = 0 AND master_id = %s' % (url, postId))
        if record:
            return forceString(record.value('note'))
        else:
            return None

    def getShortName(self, byDate=None, code='OldSurname'):
        self.load()
        lastName = self._lastName
        if byDate:  # Старая фамилия из идентификации на указанную дату
            if isinstance(byDate, (CDateInfo, CDateTimeInfo)):
                date = byDate.date
            else:
                date = forceDate(byDate)
            oldSurname = self._identification.byCode.get(code)
            checkDate = self._identification.checkDateDict.get(code)
            if oldSurname and checkDate and checkDate.date > date:
                lastName = oldSurname
        return formatShortNameInt(lastName, self._firstName, self._patrName)


    def getFullName(self, byDate=None, code='OldSurname'):
        self.load()
        lastName = self._lastName
        if byDate:  # Старая фамилия из идентификации на указанную дату
            if isinstance(byDate, (CDateInfo, CDateTimeInfo)):
                date = byDate.date
            else:
                date = forceDate(byDate)
            oldSurname = self._identification.byCode.get(code)
            checkDate = self._identification.checkDateDict.get(code)
            if oldSurname and checkDate and checkDate.date > date:
                lastName = oldSurname
        return formatNameInt(lastName, self._firstName, self._patrName)



    def getOrders(self):
        self.load()
        if self._orders is None:
            self._orders = self.getInstance(CPersonOrderInfoList, self.personId)
        return self._orders


#    def __unicode__(self):
    def __str__(self):
        self.load()
        result = formatShortNameInt(self._lastName, self._firstName, self._patrName)
        if self._speciality:
            result += ', '+self._speciality.name
        if self._academicDegree:
            result += ', '+self._academicDegree
        return unicode(result)

    id             = property(lambda self: self.personId)
    code           = property(lambda self: self.load()._code)
    federalCode    = property(lambda self: self.load()._federalCode)
    regionalCode   = property(lambda self: self.load()._regionalCode)
    lastName       = property(lambda self: self.load()._lastName)
    firstName      = property(lambda self: self.load()._firstName)
    patrName       = property(lambda self: self.load()._patrName)
    fullName       = property(getFullName)
    longName       = property(getFullName)
    shortName      = property(getShortName)
    name           = property(getShortName)
    sexCode            = property(lambda self: self.load()._sexCode)
    sex            = property(lambda self: self.load()._sex)
    office         = property(lambda self: self.load()._office)
    office2        = property(lambda self: self.load()._office2)
    contacts        = property(lambda self: self.load()._contacts)

    organisation   = property(lambda self: self.load()._organisation)
    orgStructure   = property(lambda self: self.load()._orgStructure)
    speciality     = property(lambda self: self.load()._speciality)
    post           = property(lambda self: self.load()._post)
    tariffCategory = property(lambda self: self.load()._tariffCategory)
    academicDegree = property(lambda self: self.load()._academicDegree)
    login          = property(lambda self: self.load()._login)
    orders         = property(getOrders)
    educations = property(lambda self: self.load()._educations)
    activities = property(lambda self: self.load()._activities)
    SNILS            = property(lambda self: self.load()._SNILS)
    birthDate        = property(lambda self: self.load()._birthDate)
    primaryQuota     = property(lambda self: self.load()._primaryQuota)
    ownQuota         = property(lambda self: self.load()._ownQuota)
    consultancyQuota = property(lambda self: self.load()._consultancyQuota)
    externalQuota    = property(lambda self: self.load()._externalQuota)
    identification   = property(lambda self: self.load()._identification)

def getPersonPhones(personId):
    db = QtGui.qApp.db
    table = db.table('Person_Contact')
    cond  = []
    cond.append(table['master_id'].eq(personId))
    cond.append(table['deleted'].eq(0))
    tableContactTypes = db.table('rbContactType')
    queryTable = table.leftJoin(tableContactTypes, tableContactTypes['id'].eq(table['contactType_id']))
    records = db.getRecordList(queryTable,
                               [tableContactTypes['name'], table['contact'], table['notes'], tableContactTypes['code']],
                               cond,
                               [u'Person_Contact.id DESC', tableContactTypes['code'].name()])
    result = []
    for record in records:
        typeName = forceString(record.value(0))
        contact  = forceString(record.value(1))
        notes    = forceString(record.value(2))
        contactTypeCode = forceString(record.value(3))
        result.append((typeName, contact, notes, contactTypeCode))
    return result

class CPersonInfoList(CInfoList):
    def __init__(self, context, tableName, masterId):
        CInfoList.__init__(self, context)
        self.tableName = tableName
        self.masterId = masterId

    def _load(self):
        db = QtGui.qApp.db
        table = db.table(self.tableName)
        if table.hasField('deleted'):
            cond = db.joinAnd([table['master_id'].eq(self.masterId), table['deleted'].eq(0) ])
        else:
            cond = db.joinAnd([table['master_id'].eq(self.masterId),])
        idList = db.getIdList(table, 'person_id', cond, 'person_id')
        self._items = [ self.getInstance(CPersonInfo, id) for id in idList ]


class CPersonInfoListEx(CInfoList):
    def __init__(self, context, personIdList):
        CInfoList.__init__(self, context)
        self.idList = personIdList


    def _load(self):
        self._items = [ self.getInstance(CPersonInfo, id) for id in self.idList ]
        return True


class CPersonActivitiesInfoList(CInfoList):
    def __init__(self, context, personId):
        CInfoList.__init__(self, context)
        self.personId = personId

    def _load(self):
        db = QtGui.qApp.db
        table = db.table('Person_Activity')
        idList = db.getIdList(table, 'activity_id',
                              db.joinAnd([table['master_id'].eq(self.personId),
                                          table['deleted'].eq(0)
                                         ]),
                              'id')
        self._items = [ self.getInstance(CActivityInfo, id) for id in idList ]



class CPersonIdentificationInfo(CInfo, CDictInfoMixin):
    def __init__(self, context, personId):
        CInfo.__init__(self, context)
        CDictInfoMixin.__init__(self, '_byCode')
        self._personId = personId
        self._nameDict = {}
        self._checkDateDict = {}
        self._byUrn = {}


    def _load(self):
        db = QtGui.qApp.db
        tablePI = db.table('Person_Identification')
        tableAS = db.table('rbAccountingSystem')
        queryTable = tablePI.leftJoin(tableAS, tablePI['system_id'].eq(tableAS['id']))
        cols = [ tableAS['code'],
                 tableAS['name'],
                 tableAS['urn'],
                 tablePI['value'],
                 tablePI['checkDate'],
                ]
        cond = [ tablePI['deleted'].eq(0),
                 tablePI['master_id'].eq(self._personId),
               ]
        query = db.query(db.selectStmt(queryTable, cols, cond))
        while query.next():
            record = query.record()
            code = forceString(record.value('code'))
            self._byCode[code] = forceString(record.value('value'))
            self._nameDict[code] = forceString(record.value('name'))
            self._checkDateDict[code] = CDateInfo(record.value('checkDate'))
            self._byUrn[code] = forceString(record.value('urn'))
        return True


    def __str__(self):
        self.load()
        l = [ u'%s (%s): %s' % (self._nameDict[code], code, identifier)
              for code, identifier in self._byCode.iteritems()
            ]
        l.sort()
        return ', '.join(l)


    byCode = property(lambda self: self.load()._byCode)
    byUrn = property(lambda self: self.load()._byUrn)
    nameDict = property(lambda self: self.load()._nameDict)
    checkDateDict = property(lambda self: self.load()._checkDateDict)



class CPersonOrderInfoList(CInfoList):
    def __init__(self, context, personId):
        CInfoList.__init__(self, context)
        self.personId = personId

    def _load(self):
        db = QtGui.qApp.db
        table = db.table('Person_Order')
        idList = db.getIdList(table, 'id',
                              db.joinAnd([table['master_id'].eq(self.personId),
                                          table['deleted'].eq(0)
                                         ]),
                              'id')
        self._items = [ self.getInstance(CPersonOrderInfo, id) for id in idList ]


class CPersonOrderInfo(CInfo):
    def __init__(self, context, orderId):
        CInfo.__init__(self, context)
        self.orderId = orderId
        self._date = CDateInfo()
        self._documentDate = CDateInfo()
        self._documentNumber = ''
        self._documentType = None
        self._validFromDate = CDateInfo()
        self._validToDate = CDateInfo()
        self._orgStructure = None
        self._post = None

    def _load(self):
        db = QtGui.qApp.db
        table = db.table('Person_Order')
        record = db.getRecord(table, '*', self.orderId)
        if record:
            self._date = CDateInfo(forceDate(record.value('date')))
            self._type = forceInt(record.value('type'))
            self._documentDate = CDateInfo(forceDate(record.value('documentDate')))
            self._documentNumber = forceString(record.value('documentNumber'))
            self._documentType = self.getInstance(CDocumentTypeInfo, forceRef(record.value('documentType_id')))
            self._validFromDate = CDateInfo(forceDate(record.value('validFromDate')))
            self._validToDate = CDateInfo(forceDate(record.value('validToDate')))
            self._orgStructure = self.getInstance(COrgStructureInfo, forceRef(record.value('orgStructure_id')))
            self._post = self.getInstance(CPostInfo, forceRef(record.value('post_id')))
            return True
        return False


    def getTypeAsString(self):
        self.load()
        return (u'Приём на работу', u'Увольнение', u'Назначение на должность', u'Отпуск', u'Учёба', u'Командировка', u'Прикрепление к участку')[self._type]

#    def __unicode__(self):
    def __str__(self):
        self.load()
        return u'%s %s' % (self._date, self.getTypeAsString())


    date = property(lambda self: self.load()._date)
    type = property(lambda self: self.load()._type)
    typeAsString = property(getTypeAsString)
    documentDate = property(lambda self: self.load()._documentDate)
    documentNumber = property(lambda self: self.load()._documentNumber)
    documentType = property(lambda self: self.load()._documentType)
    validFromDate = property(lambda self: self.load()._validFromDate)
    validToDate = property(lambda self: self.load()._validToDate)
    orgStructure = property(lambda self: self.load()._orgStructure)
    post = property(lambda self: self.load()._post)


class CEducationInfoList(CInfoList):
    def __init__(self, context, personId):
        CInfoList.__init__(self, context)
        self.personId = personId

    def _load(self):
        db = QtGui.qApp.db
        table = db.table('Person_Education')
        idList = db.getIdList(table, 'id',
                              db.joinAnd([table['master_id'].eq(self.personId),
                                          table['deleted'].eq(0)
                                         ]),
                              'id')
        self._items = [ self.getInstance(CEducationInfo, id) for id in idList ]


class CEducationInfo(CInfo):
    def __init__(self, context, id):
        CInfo.__init__(self, context)
        self._id = id
        self._documentType = self.getInstance(CDocumentTypeInfo, None)
        self._serial = ''
        self._number = ''
        self._date = CDateInfo()
        self._origin = ''
        self._status = ''
        self._validFromDate = CDateInfo()
        self._validToDate = CDateInfo()
        self._speciality = self.getInstance(CSpecialityInfo, None)

    def _load(self):
        db = QtGui.qApp.db
        table = db.table('Person_Education')
        record = db.getRecord(table, '*', self._id)
        if record:
            self._documentType = self.getInstance(CDocumentTypeInfo, forceRef(record.value('documentType_id')))
            self._serial = forceString(record.value('serial'))
            self._number = forceString(record.value('number'))
            self._date = CDateInfo(forceDate(record.value('date')))
            self._origin =  forceString(record.value('origin'))
            self._status = forceString(record.value('status'))
            self._validFromDate = CDateInfo(forceDate(record.value('validFromDate')))
            self._validToDate = CDateInfo(forceDate(record.value('validToDate')))
            self._speciality = self.getInstance(CSpecialityInfo, forceRef(record.value('speciality_id')))
            return True
        return False

    documentType  = property(lambda self: self.load()._documentType)
    serial  = property(lambda self: self.load()._serial)
    number  = property(lambda self: self.load()._number)
    date  = property(lambda self: self.load()._date)
    origin  = property(lambda self: self.load()._origin)
    status  = property(lambda self: self.load()._status)
    validFromDate  = property(lambda self: self.load()._validFromDate)
    validToDate  = property(lambda self: self.load()._validToDate)
    speciality  = property(lambda self: self.load()._speciality)


class CTariffCategoryInfo(CRBInfo):
    tableName = 'rbTariffCategory'
