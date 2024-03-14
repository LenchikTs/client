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
from PyQt4.QtCore import Qt, pyqtSignature, QDate

from library.Utils      import firstYearDay, forceDouble, forceInt, forceString

from Events.Utils       import getWorkEventTypeFilter
from Orgs.Utils         import getOrgStructureDescendants
from Reports.ReportBase import CReportBase, createTable
from Reports.Report     import CReport


def calculateData(begDate, endDate, eventPurposeId, eventTypeId, orgStructureId, personId, sex, ageFrom, ageTo, type, detailBed, specialityId, includeHoliday):
    db = QtGui.qApp.db
    tableVisit  = db.table('Visit')
    tableEvent  = db.table('Event')
#    tableAction = db.table('Action')
    tableEventType = db.table('EventType')
    tablePerson = db.table('Person')
    tableClient = db.table('Client')
#    tableSpeciality = db.table('rbSpeciality')
    cond = []

#    addDateInRange(cond, tableVisit['date'], begDate, endDate)
#    cond.append(tableEvent['setDate'].ge(begDate))
#    cond.append(tableEvent['execDate'].lt(endDate))
    if eventTypeId:
        cond.append(tableEvent['eventType_id'].eq(eventTypeId))
    if specialityId:
        cond.append(tablePerson['speciality_id'].eq(specialityId))
    elif eventPurposeId:
        tableEvent = db.table('Event')
        cond.append(tableEventType['purpose_id'].eq(eventPurposeId))
    if personId:
        cond.append(tableVisit['person_id'].eq(personId))
    elif orgStructureId:
        cond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureDescendants(orgStructureId)))
    else:
        cond.append(tablePerson['org_id'].eq(QtGui.qApp.currentOrgId()))
    if sex:
        cond.append(tableClient['sex'].eq(sex))
    if ageFrom <= ageTo:
        cond.append('Event.setDate >= ADDDATE(Client.birthDate, INTERVAL %d YEAR)'%ageFrom)
        cond.append('Event.execDate < SUBDATE(ADDDATE(Client.birthDate, INTERVAL %d YEAR),1)'%(ageTo+1))
    data =[]
    dataBedProfile = []
    bedIds = []
    if detailBed:
        dataBedProfile, bedIds  = createQueryForAmbulance(db, u'Action', cond,
                                                 createCondition( 5, 1, 1, 3, 2, begDate, endDate, False, None, None, None, 1, None, detailBed),
                                                 'rbHospitalBedProfile.id as id, rbHospitalBedProfile.name',
                                                 u"""LEFT JOIN `ActionType` ON Action.actionType_id=`ActionType`.id
                                                     LEFT JOIN ActionProperty ON ActionProperty.action_id = Action.id
                                                    LEFT JOIN `ActionPropertyType` ON `ActionPropertyType`.id = ActionProperty.type_id
                                                    LEFT JOIN ActionProperty_HospitalBed ON ActionProperty_HospitalBed.id = ActionProperty.id
                                                    LEFT JOIN OrgStructure_HospitalBed ON OrgStructure_HospitalBed.id = ActionProperty_HospitalBed .value
                                                    LEFT JOIN rbHospitalBedProfile ON rbHospitalBedProfile.id = OrgStructure_HospitalBed.profile_id
                                                 """, detailBed)

    data = selectData(db, cond, type ,orgStructureId,begDate,endDate, detailBed, bedIds, includeHoliday)
    return data, dataBedProfile


def selectData(db, cond, type, orgStructureId,begDate,endDate, detailBed, bedIds, includeHoliday):
    if type == 1: data =selectAmbulanceData(db, cond, begDate, endDate)
    elif type ==2: data =selectStomotologyData(db, cond, begDate, endDate)
    elif type ==3: data =selectDHospitalData(db, cond, begDate, endDate, orgStructureId, includeHoliday)
    elif type ==4: data = selectHospitalData(db, cond, begDate, endDate, orgStructureId, detailBed, bedIds)
    elif type ==5: data = selectEmergencyData(db, cond, begDate, endDate)
    else:
        data = None
    return data


def selectAmbulanceData(db, cond, begDate, endDate):
    data = []
    emergencyVisitNumberToDoctors = createQueryForAmbulance(db, 'Visit',
                                            cond, createCondition( 1, 2, 6, 12, 2, begDate, endDate, False, 1),
                                            'COUNT(`Visit`.`id`)')

    emergencyVisitNumberToStaff =createQueryForAmbulance(db, 'Visit',
                                           cond, createCondition( 1, 2, 6, 12, 2, begDate, endDate, False, 2),
                                        'COUNT(`Visit`.`id`)')
#    emergencyVisitNumber = forceInt(createQueryForAmbulance(db, 'Visit',
#                                            cond, createCondition(1,2,6,12,2,begDate,endDate,False,0),
#                                            'COUNT(`Visit`.`id`)'))

    preventiveVisitNumberToDoctors = createQueryForAmbulance(db, 'Visit',
                                           cond, createCondition( 2, 2, 6, 1, 2, begDate, endDate, False, 1, 3),
                                           'COUNT(`Visit`.`id`)')
    preventiveVisitNumberToStaff = createQueryForAmbulance(db, 'Visit',
                                           cond, createCondition( 2, 2, 6, 1, 2, begDate, endDate, False, 2, 3),
                                           'COUNT(`Visit`.`id`)')
    consultVisitNumberToDoctors = createQueryForAmbulance(db, 'Visit',
                                           cond, createCondition( 1, 2, 6, 1, 2, begDate, endDate, False, 1, 8),
                                           'COUNT(`Visit`.`id`)')
    consultVisitNumberToStaff =  createQueryForAmbulance(db, 'Visit',
                                           cond, createCondition( 1, 2, 6, 1, 2, begDate, endDate, False, 2, 8),
                                           'COUNT(`Visit`.`id`)')

    #количество визитов
#    data.append(emergencyVisitNumber+
#                forceInt(createQueryForAmbulance(db, 'Visit',
#                                            cond, createCondition(1,2,6,1,2,begDate,endDate,False, 0, 3, 8),
#                                            'COUNT(`Visit`.`id`)')))
    data.append(emergencyVisitNumberToDoctors +
                emergencyVisitNumberToStaff +
                preventiveVisitNumberToDoctors +
                preventiveVisitNumberToStaff +
                consultVisitNumberToDoctors +
                consultVisitNumberToStaff)
    #количество обращений
    data.append(createQueryForAmbulance(db, 'Visit',
                                            cond, createCondition( 1, 2, 6, 1, 2, begDate, endDate, False, 0, 1),
                                            'COUNT(DISTINCT(`Event`.`id`))'))

    # к врачам
    #   количество посещений
    data.append(emergencyVisitNumberToDoctors+
                preventiveVisitNumberToDoctors+
                consultVisitNumberToDoctors)
    #    количество посещений c профилактической целью
    data.append(preventiveVisitNumberToDoctors)
    #    количество посещений по неотложной помощи
    data.append(emergencyVisitNumberToDoctors)
    #    количество посещений для консультации
    data.append(consultVisitNumberToDoctors)
    #    количество обращений
    data.append(createQueryForAmbulance(db, 'Visit',
                                           cond, createCondition( 1, 2, 6, 1, 2, begDate, endDate, False, 1, 1),
                                           'COUNT(DISTINCT(`Event`.`id`))'))
    #к среднему мед. персоналу
        #количество посещений
    data.append(emergencyVisitNumberToStaff+
                preventiveVisitNumberToStaff+
                consultVisitNumberToStaff)
        #количество посещений c профилактической целью
    data.append(preventiveVisitNumberToStaff)
        #количество посещений по неотложной помощи
    data.append(emergencyVisitNumberToStaff)
        #количество посещений для консультации
    data.append(consultVisitNumberToStaff)
        #количество обращений
    data.append(createQueryForAmbulance(db, 'Visit', cond,
                                           createCondition( 1, 2, 6, 1, 2, begDate, endDate, False, 2, 1),
                                           'COUNT(DISTINCT(`Event`.`id`))'))
    #платные посещения
    data.append(createQueryForAmbulance(db, 'Visit', cond,
                                           createCondition( 0, 2, 6, 1, 4, begDate, endDate, False, 0),
                                           'COUNT(`Visit`.`id`)'))
    #по 911
    data.append(createQueryForAmbulance(db, 'Visit', cond,
                                           createCondition( 0, 2, 6, 1, 0, begDate, endDate, True, 0),
                                           'COUNT(`Visit`.`id`)'))
    return data


def selectStomotologyData(db, cond,begDate,endDate):
    data = []
    emergencyVisitNumberToDoctors = createQueryForAmbulance(db, 'Visit',
                                            cond, createCondition( 1, 5, 6, 12, 2, begDate, endDate, False, 1),
                                            'COUNT(`Visit`.`id`)')
    emergencyVisitNumberToStaff = createQueryForAmbulance(db, 'Visit',
                                            cond, createCondition( 1, 5, 6, 12, 2, begDate, endDate, False, 2),
                                            'COUNT(`Visit`.`id`)')
    preventiveNumberToDoctors =createQueryForAmbulance(db, 'Visit',
                                            cond, createCondition( 1, 5, 6, 1, 2, begDate, endDate, False, 1, 3),
                                            'COUNT(`Visit`.`id`)')
    preventiveNumberToStaff =createQueryForAmbulance(db, 'Visit',
                                            cond, createCondition( 1, 5, 6, 1, 2, begDate, endDate, False, 2, 3),
                                            'COUNT(`Visit`.`id`)')
    treatmentNumberToDoctors =createQueryForAmbulance(db, 'Visit',
                                            cond, createCondition( 1, 5, 6, 1, 2, begDate, endDate, False, 1, 1),
                                            'COUNT(DISTINCT(`Event`.`id`))')
    treatmentNumberToStaff =createQueryForAmbulance(db, 'Visit',
                                            cond, createCondition( 1, 5, 6, 1, 2, begDate, endDate, False, 2, 1),
                                            'COUNT(DISTINCT(`Event`.`id`))')
    visitForTreatmentNumberToDoctors = createQueryForAmbulance(db, 'Visit',
                                            cond, createCondition( 1, 5, 6, 1, 2, begDate, endDate, False, 1, 1),
                                            'COUNT(`Visit`.`id`)')
    visitForTreatmentNumberToStaff = createQueryForAmbulance(db, 'Visit',
                                            cond, createCondition( 1, 5, 6, 1, 2, begDate, endDate, False, 2, 1),
                                            'COUNT(`Visit`.`id`)')
    uetNumberToDoctors = createQueryForStomotology(db, 'Action',cond,
                                            createCondition( 0, 5, 6, 0, 2, begDate, endDate, False, 1),
                                            """if(((YEAR(Event.setDate)-YEAR(Client.birthDate)) -
                                            (DATE_FORMAT(Event.setDate, '%m-%d')<RIGHT(Client.birthDate,5))) >17,
                                            rbService.adultUetDoctor*Action.amount, rbService.childUetDoctor*Action.amount)""")
    uetNumberToStaff =   createQueryForStomotology(db, 'Action',cond,
                                            createCondition( 0, 5, 6, 0, 2, begDate, endDate, False, 2),
                                            """if(((YEAR(Event.setDate)-YEAR(Client.birthDate)) -
                                            (DATE_FORMAT(Event.setDate, '%m-%d')<RIGHT(Client.birthDate,5))) >17,
                                            rbService.adultUetDoctor*Action.amount, rbService.childUetDoctor*Action.amount)""")
    visitNumberToDoctors = visitForTreatmentNumberToDoctors + preventiveNumberToDoctors + emergencyVisitNumberToDoctors
    visitNumberToStaff = visitForTreatmentNumberToStaff + preventiveNumberToStaff + emergencyVisitNumberToStaff

    # число посещений с профилактической целью
    data.append(preventiveNumberToDoctors + preventiveNumberToStaff)
    #число посещений в неотложной форме
    data.append(emergencyVisitNumberToStaff + emergencyVisitNumberToDoctors)
    #количество обращений
    data.append(treatmentNumberToDoctors + treatmentNumberToStaff)
    #количество посещений в обращении
    data.append(visitForTreatmentNumberToDoctors + visitForTreatmentNumberToStaff)
    #количество посещений
    data.append(visitNumberToStaff + visitNumberToDoctors)
    #УЕТ
    data.append(uetNumberToDoctors + uetNumberToStaff)

    #к врачам
        # число посещений с профилактической целью
    data.append(preventiveNumberToDoctors)
        #число посещений в неотложной форме
    data.append(emergencyVisitNumberToDoctors)
        #количество обращений
    data.append(treatmentNumberToDoctors)
        #количество посещений в обращении
    data.append(visitForTreatmentNumberToDoctors)
        #количество посещений
    data.append(visitNumberToDoctors)
        #УЕТ
    data.append(uetNumberToDoctors)

    #к мед.персоналу
        # число посещений с профилактической целью
    data.append(preventiveNumberToStaff)
        #число посещений в неотложной форме
    data.append(emergencyVisitNumberToStaff)
        #количество обращений
    data.append(treatmentNumberToStaff)
        #количество посещений в обращении
    data.append(visitForTreatmentNumberToStaff)
        #количество посещений
    data.append(visitNumberToStaff)
        #УЕТ
    data.append(uetNumberToStaff)
    #платные посещения
    data.append(createQueryForAmbulance(db, 'Visit', cond,
                                            createCondition( 0, 5, 6, 1, 4, begDate, endDate, False, 0),
                                            'COUNT(`Visit`.`id`)'))
    #по 911
    data.append(createQueryForAmbulance(db, 'Visit', cond,
                                            createCondition( 0, 5, 6, 1, 0, begDate, endDate, True, 0),
                                            'COUNT(`Visit`.`id`)'))
    return data


def selectDHospitalData(db, cond,begDate,endDate,orgStructureId, includeHoliday):
    data =[]
    #количество коек
    data.append(forceInt(createQueryForHospitalStructure(db, cond,
                                                         createConditionForHospitalStructure( 0, orgStructureId),
                                                         'COUNT(`OrgStructure_HospitalBed`.`id`)')))
    #количество мест
    data.append(forceInt(createQueryForHospitalStructure(db, cond,
                                                         createConditionForHospitalStructure( 0, orgStructureId),
                                                         'SUM(`OrgStructure_HospitalBed`.relief)')))
    #количество больных

    data.append(createQueryForAmbulance( db, 'Visit', cond,
                                                 createCondition( 6, 8, 7, 0, 2, begDate, endDate, False, None, 10),
                                                 'COUNT(DISTINCT `event_id`)'))
    #
    data.append(createQueryForAmbulance(db,'Visit', cond,
                                                 createCondition( 6, 8, 7, 0, 4, begDate, endDate, False, None, 10),
                                                 'COUNT(DISTINCT `event_id`)'))
        #количество пациетно-дней
    if includeHoliday is True:
        data.append(createQueryForAmbulance(db,'Visit',cond,
                                                 createCondition( 6, 8, 7, 0, 2, begDate, endDate, False, None, 10),
                                                 'COUNT(Visit.id)'))
    #
        data.append(createQueryForAmbulance(db,'Visit', cond,
                                                 createCondition( 6, 8, 7, 0, 4, begDate, endDate, False, None, 10),
                                                 'COUNT(`Visit`.`id`)'))
    else:
        data.append(createQueryForAmbulance(db,'Visit',cond,
                                                 createCondition( 6, 8, 7, 0, 2, begDate, endDate, False, None, 10),
                                                 'SUM(if(DAYOFWEEK(Visit.date) != 7 and DAYOFWEEK(Visit.date) != 1, 1, 0))'))
    #
        data.append(createQueryForAmbulance(db,'Visit', cond,
                                                 createCondition( 6, 8, 7, 0, 4, begDate, endDate, False, None, 10),
                                                 'SUM(if(DAYOFWEEK(Visit.date) != 7 and DAYOFWEEK(Visit.date) != 1, 1, 0))'))
    return data


def selectHospitalData(db, cond,begDate,endDate, orgStructureId, detailBed, bedIds = None):
    data =[]
#    dataBedProfile = []
    #количество коек
    data.append(forceInt(createQueryForHospitalStructure(db, cond,
                                                         createConditionForHospitalStructure( 1, orgStructureId),
                                                         'COUNT(`OrgStructure_HospitalBed`.`id` )')))
    #число пролеченных больных
    data.append(createQueryForAmbulance( db, 'Action', cond,
                                                 createCondition( 5, 1, 1 , 3, 2, begDate, endDate, False),
                                                 'COUNT(DISTINCT `event_id`)'))
        #платно
    data.append(createQueryForAmbulance( db, 'Action', cond,
                                                 createCondition( 5, 1, 1, 3, 4, begDate, endDate, False),
                                                 'COUNT(DISTINCT `event_id`)'))
 #   if detailBed:
 #   #количество коек


 #       data.append(createQueryForAmbulance(db, u'Action', cond,
 #                                                createCondition( 5, 1, 1, 3, 2, begDate, endDate, False, None, None, None, 1, None, detailBed),
 #                                                'Sum(`Action`.`amount`)',
 #                                                u"""LEFT JOIN `ActionType` ON Action.actionType_id=`ActionType`.id
 #                                                    LEFT JOIN ActionProperty ON ActionProperty.action_id = Action.id
 #                                                   LEFT JOIN `ActionPropertyType` ON `ActionPropertyType`.id = ActionProperty.type_id
 #                                                   LEFT JOIN ActionProperty_HospitalBed ON ActionProperty_HospitalBed.id = ActionProperty.id
 #                                                   LEFT JOIN OrgStructure_HospitalBed ON OrgStructure_HospitalBed.id = ActionProperty_HospitalBed .value
 #                                                   LEFT JOIN rbHospitalBedProfile ON rbHospitalBedProfile.id = OrgStructure_HospitalBed.profile_id
 #                                                """, detailBed))
 #   else:
        #количество коекк
    data.append(createQueryForAmbulance(db, u'Action', cond,
                                                 createCondition( 5, 1, 1, 3, 2, begDate, endDate, False, None, None, None, 1),
                                                 'Sum(`Action`.`amount`)',
                                                 u'LEFT JOIN `ActionType` ON Action.actionType_id=`ActionType`.id '))
        #платно
    data.append(createQueryForAmbulance(db, u'Action', cond,
                                                 createCondition( 5, 1, 1, 3, 4, begDate, endDate, False),
                                                 'Sum(`Action`.`amount`)',
                                                 u'LEFT JOIN `ActionType` ON Action.actionType_id=`ActionType`.id '))
    newYearBegDate = firstYearDay(begDate)
    numberDead = createQueryForAmbulance(db, u'Action', cond,
                                                  createCondition( 5, 1, 1, 3, 2, newYearBegDate, endDate, False, None, None, None, None, 1),
                                                  'COUNT(DISTINCT `event_id`)',
                                                  u'LEFT JOIN rbResult ON Event.result_id = rbResult.id')
    numberCame = createQueryForAmbulance(db, u'Action', cond,
                                                  createCondition( 5, 1, 1, 3, 2, newYearBegDate),
                                                  'COUNT(DISTINCT `event_id`)')
    numberOut = createQueryForAmbulance(db, u'Action',cond,
                                                  createCondition( 5, 1, 1, 3, 2, newYearBegDate, endDate),
                                                  'COUNT(DISTINCT `event_id`)')
    data.append((numberDead + numberCame + numberOut)/2)
    return data


def selectEmergencyData(db, cond, begDate, endDate):
    data = []
    data.append(createQueryForAmbulance( db, u'Action', cond,
                                                 createCondition( 7, 2, 4, 0, 0, begDate, endDate),
                                                 'COUNT(Action.id)'
                                                 ))
    data.append(createQueryForAmbulance(db,u'Action', cond,
                                                 createCondition( 7, 2, 4, 0, 2, begDate, endDate),
                                                 'COUNT(Action.id)'
                                                 ))

    return data


def createCondition(eventPurposeCode, eventProfileCode, medicalAidType, medicalAidKind, financeCode,
                    begDate=None, endDate=None,
                    isArmy=None, isDoctor =None,
                    visitType1=None, visitType2=None,
                    isHospital=None, isDead=None, detailBed=None):
    condition = []
    if eventPurposeCode != 0:
        condition.append(u'rbEventTypePurpose.code=%s'%eventPurposeCode)
    condition.append(u"rbEventProfile.code =%s"%eventProfileCode)
    condition.append(u"rbMedicalAidType.code =%s"%medicalAidType)
    if medicalAidKind !=0:
        condition.append(u'rbMedicalAidKind.code =%s'%medicalAidKind)
    if financeCode !=0:
        condition.append(u'rbFinance.code =%s'%financeCode)
    if isArmy == True:
        condition.append(u'Event.Client_id IN ( SELECT  `client_id`  FROM  `ClientSocStatus` LEFT JOIN rbSocStatusType ON ClientSocStatus.socStatusType_id = rbSocStatusType.id WHERE  `rbSocStatusType`.`code` =  "с09" OR rbSocStatusType.`code`=  "008")')
    if isDoctor:
        if isDoctor ==1:
            condition.append(u'rbPost.code RLIKE "^1|^2|^3"')
        else: condition.append(u'rbPost.code NOT RLIKE "^1|^2|^3"')
    if visitType1: condition.append(u'(Visit.visitType_id = %s or Visit.visitType_id = %s)'%(visitType1,visitType2) if visitType2 else 'Visit.visitType_id =%s'%visitType1)
    if isHospital: condition.append(u"`ActionType` .`flatCode` =  'moving'")
    if isDead:
        condition.append(u"Event.`client_id` IN(SELECT DISTINCT Event.`client_id` FROM Event LEFT JOIN EventType ON Event.`eventType_id` = EventType.id WHERE EventType.code ='15')")
        condition.append(u"rbResult.code = 106 or rbResult.code = 105")
#    if begDate and visitType1 and visitType1 != 10:
#        condition.append(u"Visit.`date`>='%s'"%begDate.toString(Qt.ISODate))
    elif begDate:
            condition.append(u"Event.`execDate`>='%s'"%begDate.toString(Qt.ISODate))
    if endDate:
            condition.append(u"Event.`execDate`<'%s'"%endDate.toString(Qt.ISODate))
        #       condition.append(u"Event.`execDate`<='%s'"%(endDate.addDays(1)).toString(Qt.ISODate))
    if detailBed:
        condition.append(u"ActionPropertyType.typeName = 'HospitalBed'")
    return condition


def createConditionForHospitalStructure(structureType,orgStructureId=None):
    condition =[]
    condition.append(u'OrgStructure.type =%s'%structureType)
    #===========================================================================
    # if not orgStructureId:orgStructureId = QtGui.qApp.currentOrgId()
    # condition.append(u'OrgStructure.id=%s'%orgStructureId)
    #===========================================================================
    return condition


def createQueryForAmbulance(db, table,  cond, condition, selection, additional='', detailBed = None):
    s = 'GROUP BY rbHospitalBedProfile.name ORDER BY rbHospitalBedProfile.name' if detailBed else ''
    stmt = """SELECT %s as Number
                FROM %s
                LEFT JOIN Event ON %s.Event_id=Event.id
                LEFT JOIN Person ON `Event`.`setPerson_id` = Person.id
                LEFT JOIN rbPost ON Person.post_id=rbPost.id
                LEFT JOIN EventType ON Event.`eventType_id` = EventType.id
                LEFT JOIN rbMedicalAidKind ON EventType.medicalAidKind_id = rbMedicalAidKind.id
                LEFT JOIN rbMedicalAidType ON EventType.medicalAidType_id = rbMedicalAidType.id
                LEFT JOIN rbFinance ON %s.finance_id = rbFinance.id
                LEFT JOIN rbEventProfile ON EventType.eventProfile_id = rbEventProfile.id
                LEFT JOIN rbEventTypePurpose ON EventType.purpose_id = rbEventTypePurpose.id
                LEFT JOIN Client ON Event.client_id = Client.id
                %s
                WHERE %s AND %s
                AND %s.deleted=0
                AND Event.deleted=0 %s
                """%(selection,
                     table,
                     table,
                     table,
                     additional,
                     db.joinAnd(condition),
                     db.joinAnd(cond),
                     table,
                     s)
    query = db.query(stmt)
#    print(stmt)
    if detailBed:
        result = []
        resultId = []
        while query.next():
                result.append(forceString(query.record().value('Number'))),
                resultId.append(forceInt(query.record().value('id')))
        return result, resultId
    else:
        if query.next():
            return forceInt(query.record().value('Number'))
        else:
            return None


def createQueryForStomotology(db,table, cond, condition, selection):
    stmt = """ SELECT SUM(%s) as Number
                FROM %s
                LEFT JOIN Event ON Action.Event_id=Event.id
                LEFT JOIN Person ON `Event`.`setPerson_id` = Person.id
             --   LEFT JOIN Person ON Visit.person_id = Person.id
                LEFT JOIN rbPost ON Person.post_id=rbPost.id
                LEFT JOIN rbVisitType ON Event.`eventType_id` = rbVisitType.id
                LEFT JOIN EventType ON Event.`eventType_id` = EventType.id
                LEFT JOIN rbMedicalAidKind ON EventType.medicalAidKind_id = rbMedicalAidKind.id
                LEFT JOIN rbMedicalAidType ON EventType.medicalAidType_id = rbMedicalAidType.id
                LEFT JOIN rbEventProfile ON EventType.eventProfile_id = rbEventProfile.id
             --   LEFT JOIN Visit ON  Visit.Event_id=Event.id
                LEFT JOIN rbFinance ON Action.finance_id = rbFinance.id
                LEFT JOIN Client ON Event.client_id = Client.id
                LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
                LEFT JOIN rbService ON ActionType.nomenclativeService_id = rbService.id
                WHERE %s AND %s
                AND Action.deleted=0
                AND Event.deleted=0
                """ % (selection, table, db.joinAnd(condition), db.joinAnd(cond))
    query = db.query(stmt)
    if query.next():
        return forceDouble(query.record().value('Number'))
    else:
        return 0


def createQueryForHospitalStructure(db,cond,condition,selection):
    stmt ="""
    SELECT %s as Number
    FROM  `OrgStructure_HospitalBed`
    LEFT JOIN  `OrgStructure` ON  `OrgStructure_HospitalBed`.`master_id` =  `OrgStructure`.id
    WHERE  `isPermanent` =1
    AND  %s AND `OrgStructure`.hasHospitalBeds =1
    """%(selection,db.joinAnd(condition))
    query = db.query(stmt)
    if query.next():
        return query.record().value('Number')
    else:
        return None


def createQueryForHospital(db,cond,condition,selection):
    stmt ="""SELECT %s as Number
    LEFT JOIN Event ON Action.Event_id=Event.id
    LEFT JOIN Person ON `Event`.`setPerson_id` = Person.id
    LEFT JOIN rbPost ON Person.post_id=rbPost.id
    LEFT JOIN EventType ON Event.`eventType_id` = EventType.id
    LEFT JOIN rbMedicalAidKind ON EventType.medicalAidKind_id = rbMedicalAidKind.id
    LEFT JOIN rbMedicalAidType ON EventType.medicalAidType_id = rbMedicalAidType.id
    LEFT JOIN rbFinance ON EventType.finance_id = rbFinance.id
    LEFT JOIN rbEventProfile ON EventType.eventProfile_id = rbEventProfile.id
    WHERE %s
            AND %s
            AND Action.deleted=0
            AND Event.deleted=0
    """%(selection,db.joinAnd(cond),db.joinAnd(condition))
    query = db.query(stmt)
    print(stmt)
    if query.next():
        return query.record().value('Number')
    else:
        return None


class CReportPGG(CReport):
    def __init__(self, parent, type):
        CReport.__init__(self, parent)
        self.type = type
        self.setTitle(u'Форма ПГГ')



    def getSetupDialog(self, parent):
        result = CReportPGGSetupDialog(parent)
        result.setTitle(self.title())
        return result


    def build(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        detailBed= params.get('detailBed', False)
        eventPurposeId = params.get('eventPurposeId', None)
        eventTypeId = params.get('eventTypeId', None)
        orgStructureId = params.get('orgStructureId', None)
        personId = params.get('personId', None)
        sex = params.get('sex', 0)
        ageFrom = params.get('ageFrom', 0)
        ageTo = params.get('ageTo', 150)
        specialityId = params.get('specialityId', None)
        includeHoliday = params.get('includeHoliday', None)

        data, dataBedprofile = calculateData(begDate, endDate.addDays(1), eventPurposeId, eventTypeId, orgStructureId, personId, sex, ageFrom, ageTo, self.type, detailBed, specialityId, includeHoliday)

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        tableColumns = self.drawTable(dataBedprofile)
        table = createTable(cursor, tableColumns)

        self.mergeCells(table)
        i=3
#        if type
        for datum in data:
            table.setText(i, 5, datum)
            i=i+1
        return doc


    def mergeCells(self, table):
        #заголовок
        table.mergeCells(0, 0, 1, 7)
        table.mergeCells(1, 2, 1, 2)
        table.mergeCells(2, 2, 1, 2)
        if self.type ==1: self.mergeCellsForAmbulance(table)
        elif self.type ==2: self.mergeCellsForStomotology(table)
        elif self.type ==3: self.mergeCellsForDHospital(table),
        elif self.type ==4: self.mergeCellsForHospital(table),
        elif self.type ==5: self.mergeCellsForEmergency(table)


    def mergeCellsForAmbulance(self, table):
        table.mergeCells(3, 0, 2, 1)
        table.mergeCells(5, 0, 4, 1)
        table.mergeCells(10, 0, 4, 1)

        table.mergeCells(3, 2, 2, 1)
        table.mergeCells(5, 2, 4, 1)

        table.mergeCells(10, 2, 4, 1)
        table.mergeCells(9, 2, 1, 2)
        table.mergeCells(14, 2, 1, 2)
        table.mergeCells(15, 2, 1, 2)
        table.mergeCells(16, 2, 1, 2)

    def mergeCellsForStomotology(self, table):
        table.mergeCells(3, 0, 6, 1)
        table.mergeCells(9, 0, 6, 1)
        table.mergeCells(15, 0, 6, 1)

        table.mergeCells(3, 2, 5, 1)
        table.mergeCells(9, 2, 5, 1)
        table.mergeCells(15, 2, 5, 1)

        table.mergeCells(8, 2, 1, 2)
        table.mergeCells(14, 2, 1, 2)
        table.mergeCells(20, 2, 1, 2)
        table.mergeCells(21, 2, 1, 2)
        table.mergeCells(22, 2, 1, 2)


    def mergeCellsForDHospital(self, table):
        table.mergeCells(3, 0, 2, 1)
        table.mergeCells(5, 0, 2, 1)
        table.mergeCells(7, 0, 2, 1)
        table.mergeCells(3, 2, 1, 2)
        table.mergeCells(4, 2, 1, 2)
        table.mergeCells(5, 2, 2, 1)
        table.mergeCells(7, 2, 2, 1)


    def mergeCellsForHospital(self, table):
        table.mergeCells(4, 0, 2, 1)
        table.mergeCells(8, 0, 2, 1)
        table.mergeCells(3, 2, 1, 2)
        table.mergeCells(6, 0, 2, 1)
        table.mergeCells(4, 2, 2, 1)
        table.mergeCells(6, 2, 2, 1)
        table.mergeCells(8, 2, 1, 2)


    def mergeCellsForEmergency(self, table):
        table.mergeCells(3, 0, 2, 1)
        table.mergeCells(3, 2, 2, 1)


    def drawTable(self, dataBedprofile):
        tokens = [
                 self.drawTableForAmbulance(),
                 self.drawTableForStomotology(),
                 self.drawTableForDHospital(),
                 self.drawTableForHospital(dataBedprofile),
                 self.drawTableForEmergency()
                 ]
#        if dataBedprofile:
#            tableColumns =self.drawTableForBHospital(dataBedprofile)
#        else:
        tableColumns = tokens[self.type-1]
        return tableColumns


    def drawTableForAmbulance(self):
        tableColumns = [
                ( '5%', [u'1. Амбулаторно-поликлиническая помощь',u'',u'1',
                         u'1',u'',
                         u'2',u'',u'',u'',
                         u'3',
                         u'4',u'',u'',u'',u'5',u'6',u'7'], CReportBase.AlignLeft),
                ( '5%', [u'', u'№',u'2',
                         u'1.1',u'1.2',
                         u'2.1',u'2.2',u'2.3',u'2.5',
                         u'3',
                         u'4.1',u'4.2',u'4.3',u'4.4',
                         u'5',u'6',u'7'], CReportBase.AlignLeft),
                ( '20%', [u'', u'Наименование показателя',u'',
                          u'Всего к врачам и среднему медперсоналу',u'',
                          u'Число посещений к врачам',u'',u'',u'',
                          u'Число обращений к врачам в связи с заболеваниями',
                          u'Число посещений к среднему медперсоналу', u'',u'',u'',
                          u'Число обращений к среднему медперсоналу в связи с заболеваниями',
                          u'Платные посещения(кроме того)',
                          u'Число посещений по постановлению 911',], CReportBase.AlignLeft),
                ( '30%', [u'', u'',u'3',
                          u'Посещений',u'Обращений',
                          u'всего',u'с профилактической целью',u'по медицинской помощи в неотложной форме', u'с иными целями', u'',
                          u'всего',u'с профилактической целью',u'по медицинской помощи в неотложной форме', u'с иными целями',], CReportBase.AlignLeft),
                ( '10%', [u'',u'План',u'4'], CReportBase.AlignRight),
                ( '10%', [u'',u'Факт',u'5'], CReportBase.AlignRight),
                ( '10%', [u'',u'% от плана',u'6'], CReportBase.AlignRight),
                ]
        return tableColumns


    def drawTableForStomotology(self):
        tableColumns = [
            ( '5%', [u'2. Стоматологическая помощь', u'', u'1',
                     u'1', u'', u'', u'', u'', u'',
                     u'2', u'', u'', u'', u'', u'',
                     u'3', u'', u'', u'', u'', u'',
                     u'4',
                     u'5'], CReportBase.AlignLeft),
            ( '5%', [u'', u'№',u'2',
                     u'1.1', u'1.2', u'1.3', u'1.4', u'1.5', u'1.6',
                     u'2.1', u'2.2', u'2.3', u'2.4', u'2.5', u'2.6',
                     u'3.1', u'3.2', u'3.3', u'3.4', u'3.5', u'3.6',
                     u'4',
                     u'5'], CReportBase.AlignLeft),
            ( '20%', [u'', u'Наименование показателя',u'',
                      u'Всего число посещений и обращений к врачам и среднему медперсоналу, ведущему самостоятельный прием',
                            u'', u'', u'', u'', u'Всего УЕТ',
                      u'Число посещений и обращений к врачам', u'', u'', u'', u'',u'Количество УЕТ к врачам',
                      u'Число посещений и обращений к среднему медперсоналу, ведущему самостоятельный прием',
                            u'', u'', u'', u'',
                            u'Количество УЕТ к среднему медперсоналу, ведущему самостоятельный прием',
                      u'Платные посещения(кроме того)',
                      u'Число посещений по постановлению 911',], CReportBase.AlignLeft),
            ( '30%', [u'', u'', u'3',
                      u'Число посещений с профилактической целью',u'Число посещений по медицинской помощи в неотложной форме',
                            u'число обращений с диагностической и/или лечебной целью в связи с заболеваниями \nих них:',
                            u'число посещений с диагностической и/или лечебной целью в связи с заболеваниями',
                            u'Всего число посещений', u'',
                      u'посещений с профилактической целью',u'посещений по медицинской помощи в неотложной форме',
                            u'обращений с диагностической и/или лечебной целью в связи с заболеваниями \nих них:',
                            u'посещений с диагностической и/или лечебной целью в связи с заболеваниями', u'всего посещений', u'',
                      u'посещений с профилактической целью',u'посещений по медицинской помощи в неотложной форме',
                            u'обращений с диагностической и/или лечебной целью в связи с заболеваниями \nих них:',
                            u'посещений с диагностической и/или лечебной целью в связи с заболеваниями', u'всего посещений', u''], CReportBase.AlignLeft),
            ( '10%', [u'',u'План',u'4'], CReportBase.AlignRight),
            ( '10%', [u'',u'Факт',u'5'], CReportBase.AlignRight),
            ( '10%', [u'',u'% от плана',u'6'], CReportBase.AlignRight),
                   ]
        return tableColumns


    def drawTableForDHospital(self):
        tableColumns = [
            ( '5%', [u'3. Деятельность дневного стационара',u'',u'1',
                     u'1',u'',
                     u'2',u'',
                     u'3',u''
                     ], CReportBase.AlignLeft),
            ( '5%', [u'', u'№',u'2',
                     u'1.1',u'1.2',
                     u'2.1',u'2.2',
                     u'3.1',u'3.2'
                     ], CReportBase.AlignLeft),
            ( '20%', [u'', u'Наименование показателя',u'',
                      u'Количество коек',u'Количество мест(с учетом сменности)',
                      u'Число пролеченных больных(чел.)',u'',
                      u'Проведено больными дней лечения', u''
                      ], CReportBase.AlignLeft),
            ( '30%', [u'', u'',u'3',
                      u'',u'',
                      u'всего',u'платно(кроме того)',
                      u'всего',u'платно(кроме того)'
                      ], CReportBase.AlignLeft),
            ( '10%', [u'',u'План',u'4'], CReportBase.AlignRight),
            ( '10%', [u'',u'Факт',u'5'], CReportBase.AlignRight),
            ( '10%', [u'',u'% от плана',u'6'], CReportBase.AlignRight),
                   ]
        return tableColumns


    def drawTableForHospital(self, dataBedProfile):
        tableColumns = [
            ( '5%', [u'4. Деятельность стационара',u'',u'1',
                     u'1',
                     u'2',u'',
                     u'3',u'',
                     u'4'
                     ], CReportBase.AlignLeft),
            ( '5%', [u'', u'№',u'2',
                     u'1',
                     u'2.1',u'2.2',
                     u'3.1',u'3.2',
                     u'4'
                     ], CReportBase.AlignLeft),
            ( '20%', [u'', u'Наименование показателя',u'',
                      u'Количество коек',
                      u'Число пролеченных больных(чел.)',u'',
                      u'Проведено больными койко-дней', u'',
                      u'Число пользованных больных',
                      ], CReportBase.AlignLeft),
            ( '30%', [u'', u'',u'3',
                      u'',
                      u'всего',u'платно(кроме того)',
                      u'всего',u'платно(кроме того)'
                      ], CReportBase.AlignLeft),
            ( '10%', [u'',u'План',u'4'], CReportBase.AlignRight),
            ( '10%', [u'',u'Факт',u'5'], CReportBase.AlignRight),
            ( '10%', [u'',u'% от плана',u'6'], CReportBase.AlignRight),
                   ]
        i =6
        for beds in dataBedProfile:
            tableColumns.insert(i,  ( '20%', [u'', u'', beds], CReportBase.AlignRight))
            i=i+1
        return tableColumns


    def drawTableForEmergency(self):
        tableColumns = [
            ( '5%', [u'5. Работа скорой медицинской помощи',u'',u'1',
                     u'1',u'',
                     ], CReportBase.AlignLeft),
            ( '5%', [u'', u'№',u'2',
                     u'1.1',u'1.2',
                     ], CReportBase.AlignLeft),
            ( '20%', [u'', u'Наименование показателя',u'',
                      u'Число вызовов',
                      u''
                      ], CReportBase.AlignLeft),
            ( '30%', [u'', u'',u'3',
                      u'всего',u'в т.ч. к застрахованным(ОМС)',
                      ], CReportBase.AlignLeft),
            ( '10%', [u'',u'План',u'4'], CReportBase.AlignRight),
            ( '10%', [u'',u'Факт',u'5'], CReportBase.AlignRight),
            ( '10%', [u'',u'% от плана',u'6'], CReportBase.AlignRight),
                   ]
        return tableColumns


from Ui_ReportPGGSetup import Ui_ReportPGGSetupDialog


class CReportPGGSetupDialog(QtGui.QDialog, Ui_ReportPGGSetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.cmbEventPurpose.setTable('rbEventTypePurpose', True, filter='code != \'0\'')
        self.cmbEventType.setTable('EventType', True, filter=getWorkEventTypeFilter(isApplyActive=True))
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())
        self.chbIncludeHoliday.setEnabled(True)


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.cmbEventPurpose.setValue(params.get('eventPurposeId', None))
        self.cmbEventType.setValue(params.get('eventTypeId', None))
        self.cmbSpeciality.setTable('rbSpeciality', True)
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.cmbPerson.setValue(params.get('personId', None))
        self.cmbSex.setCurrentIndex(params.get('sex', 0))
        self.edtAgeFrom.setValue(params.get('ageFrom', 0))
        self.edtAgeTo.setValue(params.get('ageTo', 150))
        self.chbIncludeHoliday.setChecked(bool(params.get('onlyFirstTime', False)))


    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['eventPurposeId'] = self.cmbEventPurpose.value()
        result['eventTypeId'] = self.cmbEventType.value()
        result['orgStructureId'] = self.cmbOrgStructure.value()
        result['personId'] = self.cmbPerson.value()
        result['sex'] = self.cmbSex.currentIndex()
        result['ageFrom'] = self.edtAgeFrom.value()
        result['ageTo'] = self.edtAgeTo.value()
        result['specialityId'] = self.cmbSpeciality.value()
        result['includeHoliday'] = self.chbIncludeHoliday.isChecked()
        return result


    @pyqtSignature('QDate')
    def on_edtBegDate_dateChanged(self, date):
        self.cmbPerson.setBegDate(date)


    @pyqtSignature('QDate')
    def on_edtEndDate_dateChanged(self, date):
        self.cmbPerson.setEndDate(date)


    @pyqtSignature('int')
    def on_cmbSpeciality_currentIndexChanged(self, index):
        specialityId = self.cmbSpeciality.value()
        self.cmbPerson.setSpecialityId(specialityId)


    @pyqtSignature('int')
    def on_cmbEventPurpose_currentIndexChanged(self, index):
        eventPurposeId = self.cmbEventPurpose.value()
        if eventPurposeId:
            filter = 'EventType.purpose_id =%d' % eventPurposeId
        else:
            filter = getWorkEventTypeFilter(isApplyActive=True)
        self.cmbEventType.setFilter(filter)


    @pyqtSignature('int')
    def on_cmbOrgStructure_currentIndexChanged(self, index):
        orgStructureId = self.cmbOrgStructure.value()
        self.cmbPerson.setOrgStructureId(orgStructureId)
