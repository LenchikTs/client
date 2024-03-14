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
from PyQt4.QtCore import Qt, QChar, QString, QVariant

from Orgs.PersonComboBoxEx import CPersonComboBoxEx
from Orgs.PersonInfo       import CPersonInfo
from library.Utils         import forceRef, forceString, formatNameByRecord

from ActionPropertyValueType       import CActionPropertyValueType


class CPersonActionPropertyValueType(CActionPropertyValueType):
    name         = 'Person'
    variantType  = QVariant.Int

    class CPropEditor(CPersonComboBoxEx):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            self.domain = domain
            self.action = action
            CPersonComboBoxEx.__init__(self, parent)
            self.propertyOrgStructure = False

        def setValue(self, value):
            value = forceRef(value)
            if value:
                CPersonComboBoxEx.setValue(self, value)
            else:
                recordDomainList, defaultPropertyList = self.getByDefault(self.domain)
                db = QtGui.qApp.db
                tableEvent = db.table('Event')
                eventId = forceRef(self.action._record.value('event_id'))
                for key, domain in recordDomainList.items():
                    value = None
                    if key.lower() == u'лпу':
                        value = forceRef(domain)
                        # CPersonComboBoxEx.setOrganisationId(self, value)
                        CPersonComboBoxEx.setOrgStructureId(self, None, True)
                    elif key.lower() == u'подразделение':
                        tableOrgStructure = db.table('OrgStructure')
                        code = forceString(domain)
                        if code:
                            record = db.getRecordEx(tableOrgStructure, [tableOrgStructure['id']], [tableOrgStructure['deleted'].eq(0), tableOrgStructure['code'].eq(code)])
                            if record:
                                value = forceRef(record.value('id'))
                                CPersonComboBoxEx.setOrgStructureId(self, value, True)
                    elif key.lower() == u'должность':
                        value = forceString(domain)
                        CPersonComboBoxEx.setPostCode(self, value)
                    elif key.lower() == u'специальность':
                        value = forceString(domain)
                        CPersonComboBoxEx.setSpecialityCode(self, value)
                    elif key.lower() == u'деятельность':
                        value = forceString(domain)
                        CPersonComboBoxEx.setActivityCode(self, value)
                for key, domain in defaultPropertyList.items():
                    value = None
                    if key.lower() == u'подразделение':
                        if domain.contains(u'ответственного за событие', Qt.CaseInsensitive):
                            if eventId:
                                record = db.getRecordEx(tableEvent, [tableEvent['execPerson_id']], [tableEvent['deleted'].eq(0), tableEvent['id'].eq(eventId)])
                                if record:
                                    personId = forceRef(record.value('execPerson_id')) if record else None
                                    value = self.getOrgStructureId(personId)
                        elif domain.contains(u'назначившего действие', Qt.CaseInsensitive):
                            personId = forceRef(self.action._record.value('setPerson_id'))
                            value = self.getOrgStructureId(personId)
                        elif domain.contains(u'выполнившего действие', Qt.CaseInsensitive):
                            personId = forceRef(self.action._record.value('person_id'))
                            value = self.getOrgStructureId(personId)
                        elif domain.contains(u'пользователя', Qt.CaseInsensitive):
                            userId = QtGui.qApp.userId
                            if userId:
                                value = self.getOrgStructureId(userId)
                        elif key.lower() == u'подразделение' and domain.contains(u'пребывания', Qt.CaseInsensitive):
                            value = self.action[u'Отделение пребывания'] if (u'moving' in self.action._actionType.flatCode.lower()) else None
                        CPersonComboBoxEx.setOrgStructureId(self, value, True)
                    if key.lower() == u'специальность':
                        if domain.contains(u'ответственного за событие', Qt.CaseInsensitive):
                            if eventId:
                                record = db.getRecordEx(tableEvent, [tableEvent['execPerson_id']], [tableEvent['deleted'].eq(0), tableEvent['id'].eq(eventId)])
                                if record:
                                    personId = forceRef(record.value('execPerson_id')) if record else None
                                    value = self.getSpecialityId(personId)
                        elif domain.contains(u'назначившего действие', Qt.CaseInsensitive):
                            personId = forceRef(self.action._record.value('setPerson_id'))
                            value = self.getSpecialityId(personId)
                        elif domain.contains(u'выполнившего действие', Qt.CaseInsensitive):
                            personId = forceRef(self.action._record.value('person_id'))
                            value = self.getSpecialityId(personId)
                        elif domain.contains(u'пользователя', Qt.CaseInsensitive):
                            userId = QtGui.qApp.userId
                            if userId:
                                value = self.getSpecialityId(userId)
                        CPersonComboBoxEx.setSpecialityId(self, value)


        def getOrgStructureId(self, personId):
            orgStructureId = None
            if personId:
                db = QtGui.qApp.db
                tablePerson = db.table('Person')
                recOrgStructure = db.getRecordEx(tablePerson, [tablePerson['orgStructure_id']], [tablePerson['deleted'].eq(0), tablePerson['id'].eq(personId)])
                orgStructureId = forceRef(recOrgStructure.value('orgStructure_id')) if recOrgStructure else None
            return orgStructureId


        def getSpecialityId(self, personId):
            specialityId = None
            if personId:
                db = QtGui.qApp.db
                tablePerson = db.table('Person')
                record = db.getRecordEx(tablePerson, [tablePerson['speciality_id']], [tablePerson['deleted'].eq(0), tablePerson['id'].eq(personId)])
                specialityId = forceRef(record.value('speciality_id')) if record else None
            return specialityId


        def getByDefault(self, domain):
            defaultProperty = [u'ответственного за событие', u'назначившего действие', u'выполнившего действие', u'пользователя', u'пребывания']
            defaultPropertyKey = {u'ЛПУ':u'', u'подразделение':u'', u'должность':u'', u'специальность':u'', u'деятельность':u''}
            recordDomainList = {}
            defaultPropertyList = {}
            if domain:
                domainR = QString(forceString(domain))
                domainList = domainR.split(",")
                for domainI in domainList:
                    if u'\'' in domainI:
                        domainI.remove(QChar('\''), Qt.CaseInsensitive)
                    domainProperty = domainI.split(":")
                    if len(domainProperty) == 2:
                        for key in defaultPropertyKey.keys():
                            if domainProperty[0].contains(key, Qt.CaseInsensitive) and forceString(domainProperty[1]).lower() not in defaultProperty:
                                recordDomainList[key] = domainProperty[1]
                                break
                            elif domainProperty[0].contains(key, Qt.CaseInsensitive) and forceString(domainProperty[1]).lower() in defaultProperty:
                                defaultPropertyList[key] = domainProperty[1]
                                break
                    elif len(domainProperty) == 1 and forceString(domainProperty[0]).lower() == u'лпу':
                        recordDomainList[u'лпу'] = ''

            return recordDomainList, defaultPropertyList


    @staticmethod
    def convertDBValueToPyValue(value):
        v = forceString(value)
        if v == 'currentPerson':
            return QtGui.qApp.userId
        return forceRef(value)


    convertQVariantToPyValue = convertDBValueToPyValue


    def toText(self, v):
        name = u''
        db = QtGui.qApp.db
        tablePerson = db.table('Person')
        tablePost = db.table('rbPost')
        tableSpeciality = db.table('rbSpeciality')
        table = tablePerson.leftJoin(tableSpeciality, tableSpeciality['id'].eq(tablePerson['speciality_id']))
        table = table.leftJoin(tablePost, tablePost['id'].eq(tablePerson['post_id']))
        cols = [tablePerson['lastName'],
                tablePerson['firstName'],
                tablePerson['patrName'],
                tableSpeciality['name'].alias('specialityName'),
                tablePost['name'].alias('postName'),
                ]
        cond = [tablePerson['id'].eq(v),
                tablePerson['deleted'].eq(0)]
        record = db.getRecordEx(table, cols, cond)
        if record:
            name =  formatNameByRecord(record)
            specialityName = forceString(record.value('specialityName'))
            if specialityName:
                name += u', '+ specialityName
            postName = forceString(record.value('postName'))
            if postName:
                name += u', '+ postName
        return name


    def toInfo(self, context, v):
        return context.getInstance(CPersonInfo, forceRef(v))

