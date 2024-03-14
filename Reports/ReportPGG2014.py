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

import datetime
import string

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, pyqtSignature, QDate
from library.Utils      import forceDate, forceInt, forceRef, forceString, formatShortName
#from library.database   import *
from Events.Utils       import getWorkEventTypeFilter
from Orgs.Utils         import getOrgStructureDescendants
from Reports.Report     import CReport
from Reports.ReportBase import createTable, CReportBase

from Ui_ReportPGGSetup import Ui_ReportPGGSetupDialog


def calculateData(begDate, endDate, eventPurposeId, eventTypeId, orgStructureId, personId, sex, ageFrom, ageTo, type, detailBed, specialityId, financeId, columnGrouping, includeHoliday):
    db = QtGui.qApp.db
    tableEvent = db.table('Event')
    tableEventType = db.table('EventType')
    tablePerson = db.table('Person')
    tableClient = db.table('Client')
    rbFinance = db.table('rbFinance')
    cond = []
    groupField = '1'
#    addDateInRange(cond, tableVisit['date'], begDate, endDate)
#    cond.append(tableEvent['setDate'].ge(begDate))
#    cond.append(tableEvent['execDate'].lt(endDate))
    if eventTypeId:
        cond.append(tableEvent['eventType_id'].eq(eventTypeId))
    if specialityId:
        cond.append(tablePerson['speciality_id'].eq(specialityId))
    elif eventPurposeId:
        cond.append(tableEventType['purpose_id'].eq(eventPurposeId))
    if personId:
        cond.append(tablePerson['id'].eq(personId))

    if orgStructureId:
        cond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureDescendants(orgStructureId)))
    else:
        cond.append(tablePerson['org_id'].eq(QtGui.qApp.currentOrgId()))
    if sex:
        cond.append(tableClient['sex'].eq(sex))
    if ageFrom <= ageTo:
        cond.append('DATE(Event.setDate) >= ADDDATE(Client.birthDate, INTERVAL %d YEAR)'%ageFrom)
        cond.append('DATE(Event.setDate) <= SUBDATE(ADDDATE(Client.birthDate, INTERVAL %d YEAR),1)'%(ageTo+1))
    if financeId:
        cond.append(rbFinance['code'].eq(financeId))

    if columnGrouping == 3:
        groupField = 'Person.speciality_id'
    elif columnGrouping == 2:
        groupField = 'Person.id'
    elif columnGrouping == 1:
        groupField = 'Insurer.id'
    elif columnGrouping == 4:
        groupField = 'rbServiceGroup.id'
    elif columnGrouping == 5:
        groupField = 'rbService.id'
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

    data = selectData(db, cond, type ,orgStructureId,begDate,endDate, groupField,  detailBed, bedIds, includeHoliday)
    if detailBed:
        return data, dataBedProfile
    else:
        return data

def selectData(db, cond, type, orgStructureId,begDate,endDate, groupField, detailBed,  bedIds, includeHoliday):
    if type == 1: data =selectAmbulanceData(db, cond, begDate, endDate, groupField )
    elif type ==2: data =selectF62Data(db, cond, begDate, endDate, groupField )
    elif type ==3: data =selectTomographyData(db, cond, begDate, endDate, groupField )
    elif type ==4: data =selectDHospitalData(db, cond, begDate, endDate, groupField , orgStructureId, includeHoliday)
    elif type ==5: data =selectDialisData(db, cond, begDate, endDate, groupField )
    elif type ==6: data = selectHospitalData(db, cond, begDate, endDate, groupField , orgStructureId, detailBed, bedIds)
    elif type ==7: data = selectEmergencyData(db, cond, begDate, endDate, groupField )
    elif type ==8: data =selectPaidData(db, cond, begDate, endDate, groupField )
    elif type == 9: data =selectAmbulanceData(db, cond, begDate, endDate, groupField , '5')
    elif type == 10: data =selectAmbulanceData(db, cond, begDate, endDate, groupField , '', '5')
    elif type == 11: data =selectDHospital2016Data(db, cond, begDate, endDate, groupField , orgStructureId, includeHoliday)
    elif type == 12:
        data = selectDialisData(db, cond, begDate, endDate, groupField )
        data = selectActionData(data, db, cond, begDate, endDate, groupField , "'scintigraphy'")
        data = selectEcoData(data, db, cond, begDate, endDate, groupField )
        data = selectActionData(data, db, cond, begDate, endDate, groupField , "'tele_concult'")
        data = selectActionData(data, db, cond, begDate, endDate, groupField , "'tele_medecine'")
        data = selectActionData(data, db, cond, begDate, endDate, groupField , "'telemetry'")
    else:
        data = None
    return data

def sumDatum(mass):
    massLength = len(mass)
    result = {}
    for n in mass:
        for l in n:
            if l in result.keys():
                result[l] = result[l]+ n[l]
            else:
                result[l] = n[l]
    return result

def delDatum(mass, dete):
    massLength = len(mass)
    result = {}
    for l, n in mass.items():
        mass[l] = n/2
    return mass

def selectAmbulanceData(db, cond, begDate, endDate, groupField , excludeProfileCode='', includeProfileCode = ''):
    data = []
    condition = dict({'eventType': u"'3%'",
              #   'financeId': 2,
                 'begDate': begDate,
                 'endDate':endDate,
                 'isDoctor': True})
    if excludeProfileCode != '':
        condition['excludeProfileCode'] = excludeProfileCode
    if includeProfileCode != '':
        condition['includeProfileCode'] = includeProfileCode
    cond = changeTable(cond, 'Visit', 'Action')
    if excludeProfileCode == '':
        uetNumberToDoctors = createQueryForStomotology(db, 'Action',cond,
                                            createCondition(condition),  groupField,
                                            """if(((YEAR(Event.setDate)-YEAR(Client.birthDate)) -
                                            (DATE_FORMAT(Event.setDate, '%m-%d')<RIGHT(Client.birthDate,5))) >17,
                                            rbService.adultUetDoctor*Action.amount, rbService.childUetDoctor*Action.amount)""")

    cond = changeTable(cond, 'Action', 'Event_CSG')
    if excludeProfileCode == '':
        csgNumberToDoctors = createQueryForAmbulance(db, 'Event_CSG', cond, createCondition(condition),  groupField,  'COUNT(Event_CSG.id)', '', None, 'Event')
    cond = changeTable(cond, 'Event_CSG', 'Visit')
    condition['eventType'] = "'3%'"
    condition['visitType'] = 8
    preventiveVisitNumberToDoctors = createQueryForAmbulance(db, 'Visit',
                                            cond, createCondition(condition),  groupField,
                                            'COUNT(DISTINCT(Visit.id))')

    condition['visitType'] = 3
    consultVisitNumberToDoctors = createQueryForAmbulance(db, 'Visit',
                                            cond, createCondition(condition),  groupField,
                                            'COUNT(DISTINCT(Visit.id))')
    condition['isExecPerson'] = True
    condition['eventType'] = "'3%'"
    condition['excludeEventType'] = '305'
    condition['excludeEventType2'] = '301%'
    condition['visitType'] = 1
    dispanserisationVisitNumberToDoctors = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Event.id))', '', None, 'Event')

    del condition['excludeEventType2']
    condition['eventType'] = "'32%'"
    condition['visitType'] = 1
    complexVisitNumberToDoctors = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Event.id))', '', None, 'Event')

    condition['isExecPerson'] = False
    del condition['excludeEventType']
    condition['eventType'] = '305'
    condition['visitType'] = 1
    emergencyVisitNumberToDoctors = createQueryForAmbulance(db, 'Visit',
                                            cond, createCondition(condition),  groupField,
                                            'COUNT(DISTINCT(Visit.id))')
    condition['eventType'] = "'301%'"
    condition['excludeEventType'] = '305'
    condition['visitType'] = 1
    treatmentEventNumberToDoctors = createQueryForAmbulance(db, 'Visit',
                                            cond, createCondition(condition),  groupField,
                                            'COUNT(DISTINCT(`Event`.`id`))', '', None, 'Event')
    treatmentVisitNumberToDoctors = createQueryForAmbulance(db, 'Visit',
                                            cond, createCondition(condition),  groupField,
                                            'COUNT(DISTINCT(Visit.id))')
    condition['eventType'] = "'30%'"
    condition['isExecPerson'] = False
    del condition['visitType']
    del condition['excludeEventType']
    condition['isDoctor'] = False
    cond = changeTable(cond, 'Visit', 'Action')
    if excludeProfileCode == '':
        uetNumberToStaff = createQueryForStomotology(db, 'Action',cond,
                                                createCondition(condition),  groupField,
                                                """if(((YEAR(Event.setDate)-YEAR(Client.birthDate)) -
                                                (DATE_FORMAT(Event.setDate, '%m-%d')<RIGHT(Client.birthDate,5))) >17,
                                                rbService.adultUetDoctor*Action.amount, rbService.childUetDoctor*Action.amount)""")
    cond = changeTable(cond, 'Action', 'Event_CSG')
    if excludeProfileCode == '':
        csgNumberToStaff = createQueryForAmbulance(db, 'Event_CSG', cond, createCondition(condition),  groupField,  'COUNT(Event_CSG.id)', '', None, 'Event')
    cond = changeTable(cond, 'Event_CSG', 'Visit')
    condition['eventType'] = "'3%'"
    condition['visitType'] = 8
    preventiveVisitNumberToStaff = createQueryForAmbulance(db, 'Visit',
                                            cond, createCondition(condition),  groupField,
                                            'COUNT(DISTINCT(Visit.id))')
    condition['visitType'] = 3
    consultVisitNumberToStaff = createQueryForAmbulance(db, 'Visit',
                                            cond, createCondition(condition),  groupField,
                                            'COUNT(DISTINCT(Visit.id))')
    condition['isExecPerson'] = True
    condition['eventType'] = "'3%'"
    condition['visitType'] = 1
    condition['excludeEventType'] = '301%'
    condition['excludeEventType2'] = '305'
    dispanserisationVisitNumberToStaff = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Event.id))', '', None, 'Event')
    del condition['excludeEventType']
    del condition['excludeEventType2']
    condition['eventType'] = "'32%'"
    condition['visitType'] = 1
    complexVisitNumberToStaff = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Event.id))', '', None, 'Event')
    condition['isExecPerson'] = False

    condition['eventType'] = '305'
    condition['visitType'] = 1
    emergencyVisitNumberToStaff = createQueryForAmbulance(db, 'Visit',
                                            cond, createCondition(condition),  groupField,
                                            'COUNT(DISTINCT(Visit.id))')
    condition['eventType'] = "'301%'"
    condition['visitType'] = 1
    treatmentEventNumberToStaff = createQueryForAmbulance(db, 'Visit',
                                            cond, createCondition(condition),  groupField,
                                            'COUNT(DISTINCT(`Event`.`id`))','', None, 'Event')
    treatmentVisitNumberToStaff = createQueryForAmbulance(db, 'Visit',
                                            cond, createCondition(condition),  groupField,
                                            'COUNT(DISTINCT(Visit.id))')
    # --- общее
    if excludeProfileCode == '':
        data.append(sumDatum([uetNumberToStaff, uetNumberToDoctors]))
        data.append(sumDatum([csgNumberToStaff, csgNumberToDoctors]))

  #  sumDatum([consultVisitNumberToStaff, preventiveVisitNumberToStaff, consultVisitNumberToDoctors, preventiveVisitNumberToDoctors,
  #              dispanserisationVisitNumberToStaff, dispanserisationVisitNumberToDoctors, complexVisitNumberToDoctors,complexVisitNumberToStaff])
    data.append(sumDatum([consultVisitNumberToStaff, preventiveVisitNumberToStaff, consultVisitNumberToDoctors, preventiveVisitNumberToDoctors,
                dispanserisationVisitNumberToStaff, dispanserisationVisitNumberToDoctors #, #complexVisitNumberToDoctors,complexVisitNumberToStaff
                ]))
    data.append(sumDatum([emergencyVisitNumberToDoctors, emergencyVisitNumberToStaff]))
    data.append(sumDatum([treatmentEventNumberToStaff , treatmentEventNumberToDoctors]))
    data.append(sumDatum([treatmentVisitNumberToStaff , treatmentVisitNumberToDoctors]))
    data.append(sumDatum([consultVisitNumberToStaff , preventiveVisitNumberToStaff ,
                consultVisitNumberToDoctors , preventiveVisitNumberToDoctors ,
                treatmentVisitNumberToStaff , treatmentVisitNumberToDoctors ,
                emergencyVisitNumberToStaff , emergencyVisitNumberToDoctors ,
                dispanserisationVisitNumberToStaff , dispanserisationVisitNumberToDoctors #, complexVisitNumberToDoctors , complexVisitNumberToStaff
                ]))
    # ---  к врачам
    if excludeProfileCode == '':
        data.append(sumDatum([uetNumberToDoctors]))
        data.append(sumDatum([csgNumberToDoctors]))
    data.append(sumDatum([consultVisitNumberToDoctors , preventiveVisitNumberToDoctors , dispanserisationVisitNumberToDoctors # , complexVisitNumberToDoctors
                          ]))
    data.append(sumDatum([emergencyVisitNumberToDoctors]))
    data.append(sumDatum([treatmentEventNumberToDoctors]))
    data.append(sumDatum([treatmentVisitNumberToDoctors]))
    data.append(sumDatum([consultVisitNumberToDoctors , preventiveVisitNumberToDoctors ,
                treatmentVisitNumberToDoctors , emergencyVisitNumberToDoctors , dispanserisationVisitNumberToDoctors #, complexVisitNumberToDoctors
                ]))
    # --- к ср. мед персоналу
    if excludeProfileCode == '':
        data.append(sumDatum([uetNumberToStaff]))
        data.append(sumDatum([csgNumberToStaff]))
    data.append(sumDatum([consultVisitNumberToStaff , preventiveVisitNumberToStaff , dispanserisationVisitNumberToStaff #, complexVisitNumberToStaff
                          ]))
    data.append(sumDatum([emergencyVisitNumberToStaff]))
    data.append(sumDatum([treatmentEventNumberToStaff]))
    data.append(sumDatum([treatmentVisitNumberToStaff]))
    data.append(sumDatum([consultVisitNumberToStaff , preventiveVisitNumberToStaff ,
                treatmentVisitNumberToStaff,emergencyVisitNumberToStaff , dispanserisationVisitNumberToStaff #, complexVisitNumberToStaff
                ]))
    return data



def selectF62Data(db, cond, begDate, endDate, groupField ):
    data = []

    condition = dict({'eventType': u"'30%'",
                # 'financeId': 2,
                 'begDate': begDate,
                 'endDate':endDate,
                 'visitType':8})
 #   numberUETToDoctors

    preventiveVisitNumber = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))')

    condition['visitType']  = 1
    condition['eventType'] = "'35%'"
    preventiveEventNumber = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Event.id))')
    condition['isExecPerson'] = True
    condition['eventType'] = "'32%'"
    complexVisitNumber = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Event.id))', '', None, 'Event')
    condition['eventType'] = "'34%'"
    otherConditionVisitNumber = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))')
    del condition['isExecPerson']
    condition['eventType'] = "'3%'"
    condition['scene'] = '3'
    condition['visitType'] = 8
    patronageVisitNumber = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))', u'LEFT JOIN rbScene ON rbScene.id = Visit.scene_id')
    condition['eventType'] = "'3019%'"
    del condition['scene']
    stomatologyPreventiveVisitNumber = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))')
    condition['isExecPerson'] = False
    condition['eventType'] = "'31%'"
    condition['visitType'] = 1

   # del condition['visitType']
    dispanserisationVisitNumber = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Event.id))', '', None, 'Event')
    del condition['isExecPerson']
    sumPreventiveVisitNumber = sumDatum([preventiveVisitNumber,complexVisitNumber,otherConditionVisitNumber, #patronageVisitNumber,
                                         dispanserisationVisitNumber, preventiveEventNumber])
    condition['eventType'] = "'3%'"
    condition['visitType'] = 3
    consultVisitNumber = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))')
    condition['scene'] = '2'
    consultHomeVisitNumber = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))', u'LEFT JOIN rbScene ON rbScene.id = Visit.scene_id')
    condition['eventType'] = "'305'"
    condition['visitType'] = 1
    emergencyHomeVisitNumber = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))',u'LEFT JOIN rbScene ON rbScene.id = Visit.scene_id')
    del condition['scene']
    emergencyVisitNumber = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))')
    condition['eventType'] = "'301%'"

    treatmentVisitNumber = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))')
    treatmentEventNumber = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(`Event`.`id`))','', None, 'Event')
    visitNumber = sumDatum([treatmentVisitNumber, emergencyVisitNumber, consultVisitNumber, sumPreventiveVisitNumber]) # тут должно быть вычитание патронажей
    condition['eventType'] = "'30%'"
    condition['isDoctor'] = False
    condition['visitType'] = 8
    preventiveVisitNumberToStaff  = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))')
    del condition['visitType']
    condition['isExecPerson'] = True
    condition['eventType'] = "'32%'"
    complexVisitNumberToStaff  = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Event.id))')
    condition['eventType'] = "'34%'"
    otherConditionVisitNumberToStaff  = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))')
    condition['isExecPerson'] = False
    condition['eventType'] = "'3%'"
    condition['scene'] = '3'
#    del condition['visitType']
    patronageVisitNumberToStaff  = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))', u'LEFT JOIN rbScene ON rbScene.id = Visit.scene_id')
    del condition['scene']
    condition['isExecPerson'] = True
    condition['eventType'] = "'31%'"
    condition['visitType'] = 1
    dispanserisationVisitNumberToStaff  = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))')
    condition['isExecPerson'] = False
    condition['eventType'] = "'30%'"
    condition['excludeEventType'] = '305'
    treatmentVisitNumberToStaff = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))')
    condition['eventType'] = "'305'"
    del condition['excludeEventType']
    emergencyVisitNumberToStaff = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))')
    condition['eventType'] = "'3%'"
    condition['visitType'] = 3
    consultVisitNumberToStaff = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))')
    visitToStaff = (sumDatum([consultVisitNumberToStaff , treatmentVisitNumberToStaff ,
                    dispanserisationVisitNumberToStaff , #patronageVisitNumberToStaff,
                    otherConditionVisitNumberToStaff , emergencyVisitNumberToStaff,
                    complexVisitNumberToStaff, preventiveVisitNumberToStaff]))
    data.append(sumDatum([visitNumber]))
    # тут должно быть вычитание
    data.append(sumDatum([sumPreventiveVisitNumber]))
    # тут должно быть вычитание
    data.append(sumDatum([preventiveVisitNumber, preventiveEventNumber]))
    data.append(sumDatum([dispanserisationVisitNumber]))
    data.append(sumDatum([complexVisitNumber]))
    data.append(sumDatum([patronageVisitNumber]))
    data.append(sumDatum([otherConditionVisitNumber]))
    data.append(sumDatum([stomatologyPreventiveVisitNumber]))
    data.append(sumDatum([consultVisitNumber,emergencyVisitNumber]))
    data.append(sumDatum([consultHomeVisitNumber,emergencyHomeVisitNumber]))
    data.append(sumDatum([emergencyVisitNumber]))
    data.append(sumDatum([emergencyHomeVisitNumber]))
    data.append(sumDatum([treatmentVisitNumber]))
    data.append(sumDatum([treatmentEventNumber]))
    # тут должно быть вычитание
    data.append(sumDatum([visitToStaff]))
    return data


def selectTomographyData(db, cond, begDate, endDate, groupField ):
    data = []
    cond = changeTable(cond, 'Visit', 'Action')
    condition = dict({ 'begDate': begDate,
                      'endDate':endDate,
                      'actionType': "'ComputerTomographyContrasting%'" #,
                     # 'financeId': 2
                     }
                     )

    computerTomographyContrastingNumber = createQueryForAmbulance(db, 'Action', cond, createCondition(condition),  groupField,
                                                                  'SUM(Action.amount)')
    # del condition['eventType']
    condition['actionType'] = "'ComputerTomography%'"
    condition['attachType'] = 2
    computerTomographyForAttachedNumber = createQueryForAmbulance(db, 'Action', cond, createCondition(condition),  groupField,
                                                                  'SUM(Action.amount)',
                                                                  u''' -- LEFT JOIN `ActionType` ON Action.actionType_id=`ActionType`.id
                                                                  LEFT JOIN ClientAttach ON (ClientAttach.client_id = Client.id AND
                                                                  (ClientAttach.endDate IS NULL or ClientAttach.endDate>Event.execDate
                                                                  or ClientAttach.endDate='0000-00-00')
                                                                  AND ClientAttach.deleted =0)
                                                                    LEFT JOIN rbAttachType ON rbAttachType.id = ClientAttach.attachType_id''')
    condition['attachType'] = 1
    computerTomographyForNonAttachedNumber = createQueryForAmbulance(db, 'Action', cond, createCondition(condition),  groupField,  'SUM(Action.amount)', u''' -- LEFT JOIN `ActionType` ON Action.actionType_id=`ActionType`.id
                                                                  LEFT JOIN ClientAttach ON (ClientAttach.client_id = Client.id AND
                                                                  (ClientAttach.endDate IS NULL or ClientAttach.endDate>Event.execDate
                                                                  or ClientAttach.endDate='0000-00-00')
                                                                  AND ClientAttach.deleted =0)
                                                                    LEFT JOIN rbAttachType ON rbAttachType.id = ClientAttach.attachType_id''')

    condition['actionType'] = "'MRIContrasting%'"
    del condition['attachType']
    MRIContrastingNumber = createQueryForAmbulance(db, 'Action', cond, createCondition(condition),  groupField,  'SUM(Action.amount)')
    condition['actionType'] = "'MRI%'"
    condition['attachType'] = 2
    MRIForAttachedNumber = createQueryForAmbulance(db, 'Action', cond, createCondition(condition),  groupField,  'SUM(Action.amount)', u'''-- LEFT JOIN `ActionType` ON Action.actionType_id=`ActionType`.id
                                                                  LEFT JOIN ClientAttach ON (ClientAttach.client_id = Client.id AND
                                                                  (ClientAttach.endDate IS NULL or ClientAttach.endDate>Event.execDate
                                                                  or ClientAttach.endDate='0000-00-00')
                                                                  AND ClientAttach.deleted =0)
                                                                    LEFT JOIN rbAttachType ON rbAttachType.id = ClientAttach.attachType_id''')
    condition['attachType'] = 1
    MRIForNonAttachedNumber = createQueryForAmbulance(db, 'Action', cond, createCondition(condition),  groupField,  'SUM(Action.amount)', u'''-- LEFT JOIN `ActionType` ON Action.actionType_id=`ActionType`.id
                                                                  LEFT JOIN ClientAttach ON (ClientAttach.client_id = Client.id AND
                                                                  (ClientAttach.endDate IS NULL or ClientAttach.endDate>Event.execDate
                                                                  or ClientAttach.endDate='0000-00-00')
                                                                  AND ClientAttach.deleted =0)
                                                                    LEFT JOIN rbAttachType ON rbAttachType.id = ClientAttach.attachType_id''')

    data.append(sumDatum([computerTomographyForAttachedNumber, computerTomographyForNonAttachedNumber]))
    data.append(sumDatum([computerTomographyContrastingNumber]))
    data.append(sumDatum([computerTomographyForAttachedNumber]))
    data.append(sumDatum([computerTomographyForNonAttachedNumber]))

    data.append(sumDatum([MRIForAttachedNumber, MRIForNonAttachedNumber]))
    data.append(sumDatum([MRIContrastingNumber]))
    data.append(sumDatum([MRIForAttachedNumber]))
    data.append(sumDatum([MRIForNonAttachedNumber]))

    return data

def selectDHospitalData(db, cond,begDate,endDate, groupField, orgStructureId, includeHoliday):
    data =[]
    #количество коек
    cond = changeTable(cond, 'Visit', 'Action')
    condition = dict({'eventType': "'250%'",
                 'begDate': begDate,
                 'endDate':endDate,
                 'visitType':10 #,
                # 'financeId': 2
                }
                     )
    data.append(sumDatum([(createQueryForHospitalStructure(db, cond,
                                                         createConditionForHospitalStructure( 0, orgStructureId),
                                                         'COUNT(`OrgStructure_HospitalBed`.`id` )'))]))
    data.append(sumDatum([(createQueryForHospitalStructure(db, cond,
                                                         createConditionForHospitalStructure( 0, orgStructureId),
                                                         'SUM(`OrgStructure_HospitalBed`.relief)'))]))
    cond = changeTable(cond, 'Action', 'Visit')
    eventNumber = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Event.id))')
    if includeHoliday is True:
        visitNumber = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))')
    else:
        visitNumber = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'SUM(if(DAYOFWEEK(Visit.date) != 7 and DAYOFWEEK(Visit.date) != 1, 1, 0))')
    data.append(sumDatum([eventNumber]))
    data.append(sumDatum([visitNumber]))
    return data

def selectDHospital2016Data(db, cond, begDate, endDate, groupField, orgStructureId, includeHoliday):
    data =[]
    #количество коек
    cond = changeTable(cond, 'Visit', 'Action')
    condition = dict({'eventType': "'250%'",
                 'begDate': begDate,
                 'endDate':endDate,
                # 'visitType':10 #,
                # 'financeId': 2
                }
                     )
    data.append(sumDatum([(createQueryForHospitalStructure(db, cond,
                                                         createConditionForHospitalStructure( 0, orgStructureId),
                                                         'COUNT(`OrgStructure_HospitalBed`.`id` )'))]))
    data.append(sumDatum([(createQueryForHospitalStructure(db, cond,
                                                         createConditionForHospitalStructure( 0, orgStructureId),
                                                         'SUM(`OrgStructure_HospitalBed`.relief)'))]))
    condition['isHospital'] = True
    daysAmount=createQueryForAmbulance(db, u'Action', cond,
                                                 createCondition(condition), groupField,
                                                 'Sum(`Action`.`amount`)', '',
                                                  None, 'Event')
    eventAmount=createQueryForAmbulance( db, 'Action', cond,
                                                 createCondition(condition), groupField,
                                                 'COUNT(DISTINCT `event_id`)', '',
                                                   None, 'Event')

    data.append(sumDatum([eventAmount]))
    data.append(sumDatum([daysAmount]))
    return data

def selectDialisData(db, cond, begDate, endDate, groupField ):
    data =[]
    condition = dict({'eventType': '281',
                 'begDate': begDate,
                 'endDate': endDate
                 #,
                 #'financeId': 2
                 }
                     )
    hemodialysisNumber = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))')
    condition['eventType'] = "'282'"
    peritoneoclysisNumber = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))')
    condition['eventType'] = "'283'"
    hemofiltrationNumber = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))')

    data.append(sumDatum([hemodialysisNumber]))
    data.append(sumDatum([peritoneoclysisNumber]))
    data.append(sumDatum([hemofiltrationNumber]))
    return data

def selectEcoData(data, db, cond, begDate, endDate, groupField ):
    condition = dict({'eventType': "'29%'",
                 'begDate': begDate,
                 'endDate': endDate

                 }
                     )
    number = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Event.id))')

    data.append(sumDatum([number]))

    return data


def selectActionData(data, db, cond, begDate, endDate, groupField , name):
  #  data = []
    cond = changeTable(cond, 'Visit', 'Action')
    condition = dict({ 'begDate': begDate,
                      'endDate':endDate,
                      'actionType': name #,
                     # 'financeId': 2
                     }
                     )

    number = createQueryForAmbulance(db, 'Action', cond, createCondition(condition),  groupField,
                                     'SUM(Action.amount)')
    data.append(sumDatum([number]))

    return data

def selectHospitalData(db, cond,begDate,endDate, groupField, orgStructureId, detailBed, bedIds = None):
    data =[]
#    dataBedProfile = []
    #количество коек
    cond = changeTable(cond, 'Visit', 'Action')
    data.append(sumDatum([(createQueryForHospitalStructure(db, cond,
                                                         createConditionForHospitalStructure( 1, orgStructureId),
                                                         'COUNT(`OrgStructure_HospitalBed`.`id` )'))]))
    condition = dict({'eventType': '110',
                 'begDate': begDate,
                 'endDate':endDate
                 #,
                 #'financeId': 2
                 }
                     )
    #число пролеченных больных
    patientNumber = createQueryForAmbulance( db, 'Action', cond,
                                                 createCondition(condition), groupField,
                                                 "COUNT(DISTINCT IF(Event.prevEvent_id IS NULL or (prevEvent.code = '9208' or prevEvent.code =  '%s'), `event_id`, Event.prevEvent_id))" % u'УО',
                                                 '', None, 'Event')
    condition['isHospital'] = True
    daysAmount=createQueryForAmbulance(db, u'Action', cond,
                                                 createCondition(condition), groupField,
                                                 'Sum(`Action`.`amount`)','', None, 'Event', 1)
    daysAmount1=createQueryForAmbulance(db, u'Action', cond,
                                                 createCondition(condition), groupField,
                                                 'Sum(`Action`.`amount`)','', None, 'Event', 2)
  #  daysAmount = Counter(daysAmount1) + Counter(daysAmount)
    for key in daysAmount.keys():
        daysAmount[key] = daysAmount[key] + daysAmount1[key]

    data.append(sumDatum([patientNumber]))
    data.append(sumDatum([{1:0}]))
    data.append(sumDatum([{1:0}]))
    data.append(sumDatum([daysAmount]))
    data.append(sumDatum([{1:0}]))
    data.append(sumDatum([{1:0}]))
    newYearBegDate = forceDate(datetime.datetime.strptime(str(begDate.year())+'0101',"%Y%m%d"))
    condition['begDate'] = newYearBegDate
    del  condition['isHospital']
    condition['isDead'] = True
    numberDead = createQueryForAmbulance(db, u'Action', cond,
                                                  createCondition(condition), groupField,
                                                  "COUNT(DISTINCT IF(Event.prevEvent_id IS NULL or (prevEvent.code = '9208' or prevEvent.code =  '%s'), `event_id`, Event.prevEvent_id))" % u'УО',
                                                  u'LEFT JOIN rbResult ON Event.result_id = rbResult.id',  None, 'Event')
    del condition['isDead']
    numberOut = createQueryForAmbulance(db, u'Action', cond,
                                                  createCondition( condition), groupField,
                                                  "COUNT(DISTINCT IF(Event.prevEvent_id IS NULL or (prevEvent.code = '9208' or prevEvent.code =  '%s'), `event_id`, Event.prevEvent_id))" % u'УО',
                                                  '', None, 'Event')
    del condition['endDate']
    numberCame= createQueryForAmbulance(db, u'Action',cond,
                                                  createCondition(condition), groupField,
                                                  "COUNT(DISTINCT IF(Event.prevEvent_id IS NULL or (prevEvent.code = '9208' or prevEvent.code =  '%s'), `event_id`, Event.prevEvent_id))" % u'УО',
                                                  '', None, 'Event')

    data.append(delDatum(sumDatum([numberDead, numberCame, numberOut]), 2))

    return data

def selectEmergencyData(db, cond, begDate, endDate, groupField ):
    data = []
    cond = changeTable(cond, 'Visit', 'Action')
    condition = dict({'actionType': "'emergency'",
                 'begDate': begDate,
                 'endDate': endDate})

    data.append(sumDatum([createQueryForAmbulance( db, u'Action', cond,
                                                 createCondition(condition), groupField, 'COUNT(DISTINCT Action.id)',
                                                  u'LEFT JOIN rbResult ON Event.result_id = rbResult.id')]))
    condition['eventType'] = "'404%'"
    data.append(sumDatum([createQueryForAmbulance( db, u'Action', cond,
                                                 createCondition(condition), groupField, 'COUNT(DISTINCT Action.id)',
                                                 u'LEFT JOIN rbResult ON Event.result_id = rbResult.id')]))
    del condition['eventType']

    condition['isFalseEmergencyCall'] = True
    data.append(sumDatum([createQueryForAmbulance( db, u'Action', cond,
                                                 createCondition(condition), groupField, 'COUNT(DISTINCT Action.id)',
                                                 u'LEFT JOIN rbResult ON Event.result_id = rbResult.id')]))

    del condition['isFalseEmergencyCall']
    condition['isTrueEmergencyCall'] = True
    condition['financeId'] = 2
    data.append(sumDatum([createQueryForAmbulance(db,u'Action', cond,
                                                 createCondition(condition), groupField,
                                                 'COUNT(DISTINCT(Action.id))', u'LEFT JOIN rbResult ON Event.result_id = rbResult.id')]))
    return data

def selectPaidData(db, cond, begDate, endDate, groupField ):
    data = []
    condition = dict({'eventType': "'3%'",
                 'begDate': begDate,
                 'endDate':endDate,
                 'financeId': 3})
    visitsOFDMSInAmbulatory = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))')
    condition['financeId'] = 4
    visitsOFPayInAmbulatory = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))')
  #  condition['isArmy'] = True
    condition['financeId'] = 5
    visitsOF911InAmbulatory = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))')
  #  del condition['isArmy']

    data.append(sumDatum([visitsOFDMSInAmbulatory , visitsOFPayInAmbulatory , visitsOF911InAmbulatory]))
    data.append(sumDatum([visitsOFDMSInAmbulatory]))
    data.append(sumDatum([visitsOFPayInAmbulatory]))
    data.append(sumDatum([visitsOF911InAmbulatory]))

    condition['eventType'] = "'3019%'"
    condition['financeId'] = 3
    visitsOFDMSInStomatAmbulatory = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))')
    condition['financeId'] = 4
    visitsOFPayInStomatAmbulatory = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))')
  #  condition['isArmy'] = True
    condition['financeId'] = 5
    visitsOF911InStomatAmbulatory = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))')
  #  del condition['isArmy']

    data.append(sumDatum([visitsOFDMSInStomatAmbulatory, visitsOFPayInStomatAmbulatory, visitsOF911InStomatAmbulatory]))
    data.append(sumDatum([visitsOFDMSInStomatAmbulatory]))
    data.append(sumDatum([visitsOFPayInStomatAmbulatory]))
    data.append(sumDatum([visitsOF911InStomatAmbulatory]))

    condition['eventType'] = "'3%'"
    condition['financeId'] = 3
    condition['flatCode'] = 'diagnost'
    eventsOFDMSInAmbulatory = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Event.id))', u'LEFT JOIN `Action` ON Action.event_id = Event.id LEFT JOIN `ActionType` ON Action.actionType_id=`ActionType`.id')
    condition['financeId'] = 4
    eventsOFPayInAmbulatory = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Event.id))', u'LEFT JOIN `Action` ON Action.event_id = Event.id LEFT JOIN `ActionType` ON Action.actionType_id=`ActionType`.id')
 #   condition['isArmy'] = True
    condition['financeId'] = 5
    eventsOF911InAmbulatory = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Event.id))', u'LEFT JOIN `Action` ON Action.event_id = Event.id LEFT JOIN `ActionType` ON Action.actionType_id=`ActionType`.id')
  #  del condition['isArmy']
    del condition['flatCode']
    data.append(sumDatum([eventsOFDMSInAmbulatory, eventsOFPayInAmbulatory, eventsOF911InAmbulatory]))
    data.append(sumDatum([eventsOFDMSInAmbulatory]))
    data.append(sumDatum([eventsOFPayInAmbulatory]))
    data.append(sumDatum([eventsOF911InAmbulatory]))

    condition['eventType'] = "'2%'"
    condition['financeId'] = 3
    condition['visitType'] = 10

    eventsOFDMSInDS = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Event.id))')
    condition['financeId'] = 4
    eventsOFPayInDS = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Event.id))')
 #   condition['isArmy'] = True
    condition['financeId'] = 5
    eventsOF911InDS = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Event.id))')
  #  del condition['isArmy']

    data.append(sumDatum([eventsOFDMSInDS, eventsOFPayInDS, eventsOF911InDS]))
    data.append(sumDatum([eventsOFDMSInDS]))
    data.append(sumDatum([eventsOFPayInDS]))
    data.append(sumDatum([eventsOF911InDS]))

    condition['financeId'] = 3
    visitsOFDMSInDS = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))')
    condition['financeId'] = 4
    visitsOFPayInDS = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))')
  #  condition['isArmy'] = True
    condition['financeId'] = 5
    visitsOF911InDS = createQueryForAmbulance(db, 'Visit', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Visit.id))')
 #   del condition['isArmy']

    data.append(sumDatum([visitsOFDMSInDS, visitsOFPayInDS, visitsOF911InDS]))
    data.append(sumDatum([visitsOFDMSInDS]))
    data.append(sumDatum([visitsOFPayInDS]))
    data.append(sumDatum([visitsOF911InDS]))

    condition['eventType'] = "'1%'"
    condition['financeId'] = 3

    del condition['visitType']
    cond = changeTable(cond, 'Visit', 'Action')
    eventsOFDMSInHospital = createQueryForAmbulance(db, 'Action', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Event.id))')
    condition['financeId'] = 4
    eventsOFPayInHospital = createQueryForAmbulance(db, 'Action', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Event.id))')
 #   condition['isArmy'] = True
    condition['financeId'] = 5
    eventsOF911InHospital = createQueryForAmbulance(db, 'Action', cond, createCondition(condition),  groupField,  'COUNT(DISTINCT(Event.id))')

    data.append(sumDatum([eventsOFDMSInHospital, eventsOFPayInHospital, eventsOF911InHospital]))
    data.append(sumDatum([eventsOFDMSInHospital]))
    data.append(sumDatum([eventsOFPayInHospital]))
    data.append(sumDatum([eventsOF911InHospital]))

 #   del condition['isArmy']
    condition['financeId'] = 3
    condition['isHospital'] = True
    actionsAmountOFDMSInHospital = createQueryForAmbulance(db, 'Action', cond, createCondition(condition),  groupField,  'Sum(`Action`.`amount`)')
    condition['financeId'] = 4
    actionsAmountOFPayInHospital = createQueryForAmbulance(db, 'Action', cond, createCondition(condition),  groupField,  'Sum(`Action`.`amount`)')
 #   condition['isArmy'] = True
    condition['financeId'] = 5
    actionsAmountOF911InHospital = createQueryForAmbulance(db, 'Action', cond, createCondition(condition),  groupField,  'Sum(`Action`.`amount`)')

    data.append(sumDatum([actionsAmountOFDMSInHospital, actionsAmountOFPayInHospital, actionsAmountOF911InHospital]))
    data.append(sumDatum([actionsAmountOFDMSInHospital]))
    data.append(sumDatum([actionsAmountOFPayInHospital]))
    data.append(sumDatum([actionsAmountOF911InHospital]))

 #   del condition['isArmy']

    return data


def createCondition(cond):
    condition = []
    if cond.has_key('excludeProfileCode'):
# ругаюсь - №1
        condition.append(u"rbEventProfile.code NOT LIKE %s"%cond['excludeProfileCode'])
    if cond.has_key('eventType'):
        condition.append(u"EventType.regionalCode LIKE %s"%cond['eventType'])
    if cond.has_key('includeProfileCode'):
        condition.append(u'rbEventProfile.code  LIKE "%s"'%cond['includeProfileCode'])
    if cond.has_key('excludeEventType2'):
        condition.append(u'EventType.regionalCode NOT LIKE "%s"'%cond['excludeEventType2'])
    if cond.has_key('excludeEventType'):
        condition.append(u'EventType.regionalCode NOT LIKE "%s"'%cond['excludeEventType'])
    if cond.has_key('financeId'):
        condition.append(u"rbFinance.code =%s"%cond['financeId'])
    if cond.has_key('isArmy'):
# ругаюсь - №2
        if cond['isArmy'] == True:
            condition.append(u'''Event.Client_id IN ( SELECT  `client_id`  FROM  `ClientSocStatus`
                                LEFT JOIN rbSocStatusType ON ClientSocStatus.socStatusType_id = rbSocStatusType.id
                                WHERE  `rbSocStatusType`.`code` =  "с09" OR rbSocStatusType.`code`=  "008")''')
    if cond.has_key('isDoctor'):
# ругаюсь - №3 :(
        condition.append(u'rbPost.code RLIKE "^1|^2|^3"') if cond['isDoctor'] == True else condition.append(u'rbPost.code NOT RLIKE "^1|^2|^3"')
    if cond.has_key('visitType'):
        condition.append(u'(rbVisitType.regionalCode =%s)'%(cond['visitType']))
    if cond.has_key('isHospital'):
        condition.append('`ActionType`.`flatCode` = \'moving\'')
    if cond.has_key('isDead'):
        condition.append(u"Event.`client_id` IN(SELECT DISTINCT Event.`client_id` FROM Event LEFT JOIN EventType ON Event.`eventType_id` = EventType.id WHERE EventType.code ='15')")
        condition.append(u"rbResult.code = 106 or rbResult.code = 105")
#    if cond.has_key('begDate') and cond.has_key('visitType') and  cond['visitType'] != 10:
#        condition.append(u"Visit.`date`>='%s'"%(cond['begDate']).toString(Qt.ISODate))
    if cond.has_key('begDate'):
        condition.append(u"Event.`execDate`>='%s'"%(cond['begDate']).toString(Qt.ISODate))
    if cond.has_key('endDate'):
        condition.append(u"Event.`execDate`<'%s'"%(cond['endDate']).toString(Qt.ISODate))
    if cond.has_key('detailBed'):
        condition.append(u"ActionPropertyType.typeName = 'HospitalBed'")
    if cond.has_key('scene'):
        condition.append(u'(rbScene.code =%s)'%(cond['scene']))
    if cond.has_key('attachType'):
        if cond['attachType'] == 1:
            condition.append(u'(rbAttachType.code !=2)' + 'or ClientAttach.id is NULL')
        else:
            condition.append(u'(rbAttachType.code =%s)'%(cond['attachType']))
    if cond.has_key('actionType'):
        condition.append(u'(ActionType.flatCode LIKE %s)'%(cond['actionType']))
    if cond.has_key('isFalseEmergencyCall'):
        condition.append(u"rbResult.code = '11'")
    if cond.has_key('isTrueEmergencyCall'):
        condition.append(u"rbResult.code != '11'")
    if cond.has_key('isExecPerson'):
          if  cond['isExecPerson'] == True:
                condition.append(u"Visit.person_id = Event.execPerson_id")

    return condition

def createConditionForHospitalStructure(structureType,orgStructureId=None):
    condition =[]
    condition.append(u'OrgStructure.type =%s'%structureType)
    #===========================================================================
    # if not orgStructureId:orgStructureId = QtGui.qApp.currentOrgId()
    # condition.append(u'OrgStructure.id=%s'%orgStructureId)
    #===========================================================================
    return condition

def createQueryForAmbulance(db, table,  cond, condition, groupField, selection, additional='',  detailBed = None, tableEvent = None, isHospital = None):
    if groupField == 'Insurer.id':
        additional += ' LEFT JOIN ClientPolicy ON Client.id = ClientPolicy.client_id AND (ClientPolicy.endDate IS NULL OR ClientPolicy.endDate >= Event.setDate) ANd ClientPolicy.deleted = 0 LEFT JOIN Organisation as Insurer ON Insurer.id = ClientPolicy.insurer_id'
    if table == 'Action':
        additional += ' LEFT JOIN ActionType ON Action.actionType_id = ActionType.id'
        additional += ' LEFT JOIN Event as e2 ON e2.prevEvent_id=Event.id '
        additional += ' LEFT JOIN EventType prevEvent ON e2.`eventType_id` = prevEvent.id'
        if groupField == 'rbServiceGroup.id':
            additional += ' LEFT JOIN rbService ON rbService.id = ActionType.nomenclativeService_id'
            additional += ' LEFT JOIN rbServiceGroup ON rbServiceGroup.id = rbService.group_id'
    if table == 'Event':
        additional += ' LEFT JOIN mes.MES ON mes.MES.id = Event.MES_id'
        additional += ' LEFT JOIN rbService ON rbService.code = mes.MES.code'
        additional += ' LEFT JOIN Event as e2 ON e2.prevEvent_id=Event.id '
        additional += ' LEFT JOIN EventType prevEvent ON e2.`eventType_id` = prevEvent.id'
        if groupField == 'rbServiceGroup.id':
            additional += ' LEFT JOIN rbServiceGroup ON rbServiceGroup.id = rbService.group_id'
    if table == 'Visit':
        additional += ' LEFT JOIN rbVisitType ON rbVisitType.id = Visit.visitType_id'
        additional += ' LEFT JOIN rbService ON rbService.id = Visit.service_id'
        if groupField == 'rbServiceGroup.id':
            additional += ' LEFT JOIN rbServiceGroup ON rbServiceGroup.id = rbService.group_id'
    if table == 'Event_CSG':
        join = 'LEFT JOIN Event ON %s.master_id=Event.id'%table
        additional += ' LEFT JOIN rbService ON rbService.code = Event_CSG.CSGCode'
        if groupField == 'rbServiceGroup.id':
            additional += ' LEFT JOIN rbServiceGroup ON rbServiceGroup.id = rbService.group_id'
    elif isHospital == 1:
        join = 'LEFT JOIN Event ON Action.Event_id= Event.id'
    elif isHospital == 2:
        join = 'LEFT JOIN Event ON  Action.Event_id = Event.prevEvent_id'
    else:
        join = 'LEFT JOIN Event ON %s.Event_id=Event.id '%table


    s = 'GROUP BY rbHospitalBedProfile.name ORDER BY rbHospitalBedProfile.name' if detailBed else ''
    stmt = """SELECT %s AS rowKey,
                    %s as Number
                FROM %s
                %s %s

                -- LEFT JOIN Person ON `Event`.`execPerson_id` = Person.id
                LEFT JOIN Person ON %s = Person.id
                LEFT JOIN rbPost ON Person.post_id=rbPost.id
                LEFT JOIN EventType ON Event.`eventType_id` = EventType.id
                LEFT JOIN rbMedicalAidKind ON EventType.medicalAidKind_id = rbMedicalAidKind.id
                LEFT JOIN rbMedicalAidType ON EventType.medicalAidType_id = rbMedicalAidType.id
                %s
                LEFT JOIN rbEventProfile ON EventType.eventProfile_id = rbEventProfile.id
                LEFT JOIN rbEventTypePurpose ON EventType.purpose_id = rbEventTypePurpose.id
                LEFT JOIN Client ON Event.client_id = Client.id
                %s
                WHERE %s AND %s %s

                AND Event.deleted=0 %s
                GROUP BY rowKey
                """%(groupField,
                     selection,
                     table,
                     table,
                     join,
                     "`Event`.`execPerson_id`" if tableEvent else '%s.person_id'%table,
                    # 'LEFT JOIN rbFinance ON %s.finance_id = rbFinance.id'%table if table != 'Event_CSG' else 'LEFT JOIN rbFinance ON %s.finance_id = rbFinance.id'%'EventType' ,
                    'LEFT JOIN rbFinance ON %s.finance_id = rbFinance.id'%'EventType',
                     additional,
                     db.joinAnd(condition),
                     db.joinAnd(cond),
                     "AND %s.deleted=0"%table if table != 'Event_CSG' else '',
                     s)
    query = db.query(stmt)
 #   print(stmt)
    if detailBed:
        result = []
        resultId = []
        while query.next():
                result.append(forceString(query.record().value('Number'))),
                resultId.append(forceInt(query.record().value('id')))
        return result, resultId
    else:
        data = {1: 0}
        while query.next():
            if forceInt(query.record().value('Number')) != None:
                data[forceRef(query.record().value('rowKey'))] = forceInt(query.record().value('Number'))
            else:
                data[forceRef(query.record().value('rowKey'))] = 0
        return data


def changeTable(mass, tableBefore, tableAfter):
    for x in mass:
        if string.find(x, tableBefore) >=0:
            mass.append(string.replace(x, tableBefore, tableAfter))
            mass.remove(x)
    return mass


def createQueryForStomotology(db,table, cond, condition, groupField, selection):
    additional = ''
    if groupField == 'Insurer.id':
        additional += ' LEFT JOIN ClientPolicy ON Client.id = ClientPolicy.client_id AND (ClientPolicy.endDate IS NULL OR ClientPolicy.endDate >= Event.setDate) ANd ClientPolicy.deleted = 0 LEFT JOIN Organisation as Insurer ON Insurer.id = ClientPolicy.insurer_id'
    if table == 'Action' and groupField == 'rbServiceGroup.id':

        additional += ' LEFT JOIN rbServiceGroup ON rbServiceGroup.id = rbService.group_id'
    stmt = """ SELECT %s AS rowKey,
                SUM(%s) as Number
                FROM %s
                LEFT JOIN Event ON Action.Event_id=Event.id
                LEFT JOIN Person ON `Event`.`setPerson_id` = Person.id
                LEFT JOIN rbPost ON Person.post_id=rbPost.id
                LEFT JOIN rbVisitType ON Event.`eventType_id` = rbVisitType.id
                LEFT JOIN EventType ON Event.`eventType_id` = EventType.id
                LEFT JOIN rbMedicalAidKind ON EventType.medicalAidKind_id = rbMedicalAidKind.id
                LEFT JOIN rbMedicalAidType ON EventType.medicalAidType_id = rbMedicalAidType.id
                LEFT JOIN rbEventProfile ON EventType.eventProfile_id = rbEventProfile.id
         --       LEFT JOIN Visit ON  Visit.Event_id=Event.id
                LEFT JOIN rbFinance ON Action.finance_id = rbFinance.id
                LEFT JOIN Client ON Event.client_id = Client.id
                LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
                LEFT JOIN rbService ON ActionType.nomenclativeService_id = rbService.id
                %s
                WHERE %s AND %s
                AND Action.deleted=0
                AND Event.deleted=0
                GROUP BY rowKey
                """ % (groupField, selection, table, additional, db.joinAnd(condition), db.joinAnd(cond))
    query = db.query(stmt)
    data = {}
    while query.next():
            if forceInt(query.record().value('Number')) != None:
                data[forceRef(query.record().value('rowKey'))] = forceInt(query.record().value('Number'))
            else:
                data[forceRef(query.record().value('rowKey'))] = 0
    return data

def createQueryForHospitalStructure(db, cond, condition, selection):
    stmt ="""
    SELECT %s as Number
    FROM  `OrgStructure_HospitalBed`
    LEFT JOIN  `OrgStructure` ON  `OrgStructure_HospitalBed`.`master_id` =  `OrgStructure`.id
    WHERE  `isPermanent` =1
    AND  %s AND `OrgStructure`.hasHospitalBeds =1
    """%(selection,db.joinAnd(condition))
    query = db.query(stmt)
    data = {}
    if query.next():
        data[0] = forceInt(query.record().value('Number'))
    return data

def createQueryForHospital(db,cond,condition, groupField, selection):
    additional = ''
    if groupField == 'Insurer.id':
        additional += ' LEFT JOIN ClientPolicy ON Client.id = ClientPolicy.client_id AND (ClientPolicy.endDate IS NULL OR ClientPolicy.endDate >= Event.setDate) ANd ClientPolicy.deleted = 0 LEFT JOIN Organisation as Insurer ON Insurer.id = ClientPolicy.insurer_id'
    if groupField == 'rbServiceGroup.id' or groupField == 'rbService.id':
        additional += ' LEFT JOIN mes.MES ON mes.MES.id = Event.MES_id'
        additional += ' LEFT JOIN rbService ON rbService.code = mes.MES.code'
        additional += ' LEFT JOIN rbServiceGroup ON rbServiceGroup.id = rbService.group_id'
    stmt ="""SELECT
    SELECT %s AS rowKey,
    %s as Number
    LEFT JOIN Event ON Action.Event_id=Event.id
    LEFT JOIN Person ON `Event`.`setPerson_id` = Person.id
    LEFT JOIN rbPost ON Person.post_id=rbPost.id
    LEFT JOIN EventType ON Event.`eventType_id` = EventType.id
    LEFT JOIN rbMedicalAidKind ON EventType.medicalAidKind_id = rbMedicalAidKind.id
    LEFT JOIN rbMedicalAidType ON EventType.medicalAidType_id = rbMedicalAidType.id
    LEFT JOIN rbFinance ON EventType.finance_id = rbFinance.id
    LEFT JOIN rbEventProfile ON EventType.eventProfile_id = rbEventProfile.id
    %s
    WHERE %s
            AND %s
            AND Action.deleted=0
            AND Event.deleted=0
    GROUP BY rowKey
    """%(groupField, selection, additional, db.joinAnd(cond),db.joinAnd(condition))
    query = db.query(stmt)
 #   print(stmt)
    data = {}
    while query.next():
            if forceInt(query.record().value('Number')) != None:
                data[forceRef(query.record().value('rowKey'))] = forceInt(query.record().value('Number'))
            else:
                data[forceRef(query.record().value('rowKey'))] = 0
    return data


class CReportPGG2014(CReport):
    def __init__(self, parent, type):
        CReport.__init__(self, parent)
        self.type = type
        self.setTitle(u'Форма ПГГ')




    def getSetupDialog(self, parent):
        result = CReportPGGSetupDialog(parent)
     #   result.setTitle(self.title())
        if self.type == 8 or self.type == 7:
            result.lblFinanceType.setVisible(False)
            result.cmbFinanceId.setVisible(False)
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
        columnGrouping = params.get('columnGrouping', 0)
        ageFrom = params.get('ageFrom', 0)
        ageTo = params.get('ageTo', 150)
        specialityId = params.get('specialityId', None)
        includeHoliday = params.get('includeHoliday', None)
        financeId = params.get('financeId', None)

        if detailBed:
            data, dataBedprofile= calculateData(begDate, endDate.addDays(1), eventPurposeId, eventTypeId, orgStructureId, personId, sex, ageFrom, ageTo, self.type, detailBed, specialityId, financeId, columnGrouping)
        else:
            data = calculateData(begDate, endDate.addDays(1), eventPurposeId, eventTypeId, orgStructureId, personId, sex, ageFrom, ageTo, self.type, detailBed, specialityId, financeId, columnGrouping, includeHoliday)
            dataBedprofile =[]
        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
      #  cursor.setCharFormat(CReportBase.ReportTitle)
      #  cursor.insertText(self.title())
        self.setOrientation(QtGui.QPrinter.Landscape)
        cursor.insertBlock()
        self.dumpParams(cursor, params)

        number, mass = self.getAdditionalColumnNumber(data)
        if columnGrouping != 0:
            tableColumns = self.drawTable(dataBedprofile, 1, len)
            tableColumns = self.transportTable(tableColumns)
#             l = 100/(len(tableColumns) + number)
#             k=h = len(tableColumns)
#             while k < (number+h):
#                tableColumns.insert(k, ('%s'%l + '%', [u'',u'',u'%s'%(k-2)], CReportBase.AlignLeft))
#                k=k+1
        else:
            tableColumns = self.drawTable(dataBedprofile, 0)
         #   tableColumns.insert(1, ( '10%', [u'Специальность', u'',u'',u''], CReportBase.AlignRight))

        table = createTable(cursor, tableColumns, 0)

        self.mergeCells(table, number, columnGrouping)
        i=3

        #s =len(tableColumns) - number
        j =1
        db = QtGui.qApp.db
        if columnGrouping != 0:

            for el in mass:
                if columnGrouping == 3:
                    groupField = forceString(db.translate('rbSpeciality', 'id',  forceString(el), 'CONCAT(code, " ", name)'))
                elif columnGrouping == 2:
                    lastName = forceString(db.translate('Person', 'id',  forceString(el), 'lastName'))
                    firstName = forceString(db.translate('Person', 'id',  forceString(el), 'firstName') )
                    patrName = forceString(db.translate('Person', 'id',  forceString(el), 'patrName'))
                    code = forceString(db.translate('Person', 'id',  forceString(el), 'code'))
                    groupField = code + ' ' + formatShortName(lastName, firstName, patrName)
                elif columnGrouping == 1:
                    groupField = forceString(db.translate('Organisation', 'id',  forceString(el), 'shortName'))
                elif columnGrouping == 4:
                    groupField = forceString(db.translate('rbServiceGroup', 'id',  forceString(el), 'CONCAT(code, " ", name)'))
                elif columnGrouping == 5:
                    groupField = forceString(db.translate('rbService', 'id',  forceString(el), 'CONCAT(code, " ", name)'))
                else:
                    groupField = ''
                table.addRow()

                table.setText(3 + j, 1, groupField)
                table.setText(3 + j, 0, j)
                table.mergeCells(3 + j, 1, 1, 2)
                j=j+1
            for datum in data:
                for key, value in datum.items():
                    table.setText(4+mass.index(key), i, value)
                i=i+1
        else:
            if self.type !=12 and columnGrouping != 0:
                for datum in data:
                    for key, value in datum.items():
                        pass  # что за s? table.setText(i, s+mass.index(key), value)
                    i=i+1
            elif self.type !=12 and columnGrouping == 0:
                 for datum in data:
                    for key, value in datum.items():
                        table.setText(i, 5, value)
                    i=i+1
            else:
                c = [3,4,5,7,11,13,14,16]
                i =0
                for datum in data:
                    for key, value in datum.items():
                        table.setText(c[i], mass.index(key), value)
                    i=i+1
#
        return doc

    def transportTable(self, tableColumns):
        mass = []
        self.obmTable(tableColumns)
        for row in tableColumns:
            for i in row[1]:
                if tableColumns.index(row) == 0:
                    mass.append((row[0], [i], row[2]))
                else:
                    mass[row[1].index(i)][1].append(i)
        self.obmTable(mass)
        return mass

    def obmTable(self, tableColumns):
        s = 200
        for row in tableColumns:
            for i in row[1]:
                if i == '':
                    tableColumns[tableColumns.index(row)][1][row[1].index(i)] = str(s)
                    s = s +1
                elif i[:2] in ['20', '22', '21', '23', '24', '25', '26', '27', '28', '29']:
                    tableColumns[tableColumns.index(row)][1][row[1].index(i)] = ''
        return tableColumns

    def getAdditionalColumnNumber(self, massive):
#        number = 0
        result_mas = []
        for i in massive:
            for j in i:
                if j not in result_mas:
                    result_mas.append(j)
        return len(result_mas), result_mas

    def mergeCells(self, table, number, columnGrouping):

        highCell = [[0, 0, 1, 6+number], [1, 2, 1, 2], [2, 2, 1, 2]]  #заголовок
        cells = [[[3, 0, 6, 1] ,[9, 0, 6, 1] ,[15, 0, 6, 1] ,[3, 2, 6, 1] ,[9, 2, 6, 1] ,[15, 2, 6, 1]],
                 [[3, 0, 15, 1] ,[5, 2, 5, 1] ,[3, 2, 1, 2] ,[4, 2, 1, 2] ,[10, 2, 1, 2] ,[11, 2, 1, 2] ,[12, 2, 1, 2] ,[13, 2, 1, 2] ,[14, 2, 1, 2] ,[15, 2, 1, 2] ,[16, 2, 1, 2] ,[17, 2, 1, 2]],
                 [[3, 0, 4, 1] ,[7, 0, 4, 1] ,[3, 2, 4, 1] ,[7, 2, 4, 1] ,[3, 3, 4, 1] ,[7, 3, 4, 1]  ,[2, 2, 1, 3] ,[1, 2, 1, 3]],
                 [[3, 0, 2, 1]  ,[3, 2, 1, 2] ,[4, 2, 1, 2]],
                 [[3, 0, 3, 1] ,[3, 2, 1, 2] ,[4, 2, 1, 2] ,[5, 2, 1, 2]],
                 [[4, 0, 3, 1] ,[7, 0, 3, 1] ,[4, 2, 3, 1] ,[7, 2, 3, 1] ,[10, 2, 1, 2]],
                 [[3, 0, 4, 1] ,[3, 2, 4, 1] ],
                 [[3, 0, 12, 1] ,[15, 0, 8, 1] ,[23, 0, 8, 1] ,[3, 2, 12, 1],[15, 2, 8, 1] ,[23, 2, 8, 1] ,[27, 3, 8, 1] ,[3, 3, 4, 1] ,[11, 3, 4, 1] ,[19, 3, 4, 1] ,[23, 3, 4, 1] ,[7, 3, 4, 1] ,[15, 3, 4, 1] ,[23, 3, 4, 1] ,[3, 2, 4, 1] ,[2, 2, 1, 3],[1, 2, 1, 3]],
                 [[3, 0, 5, 1] ,[8, 0, 5, 1] ,[13, 0, 5, 1]  ,[3, 2, 5, 1] ,[8, 2, 5, 1] ,[13, 2, 5, 1] ] ,  # амбулатория 2016
                 [[3, 0, 7, 1] ,[10, 0, 7, 1] ,[17, 0, 7, 1] ,[3, 2, 7, 1] ,[10, 2, 7, 1] ,[17, 2, 7, 1]],    # стоматология 2016
                 [[3, 0, 2, 1]  ,[3, 2, 1, 2] ,[4, 2, 1, 2]],
                 [[2, 0, 1, 5], [6, 0, 1, 5],[10, 0, 1, 5],[12, 0, 1, 5],[15, 0, 1, 5],[0, 1, 1, 2],[1, 1, 1, 2],[3, 1, 1, 2],[4, 1, 1, 2],[5, 1, 1, 2],[11, 1, 1, 2],[13, 1, 1, 2],[14, 1, 1, 2],[16, 1, 1, 2],[7, 1, 3, 1]]]

        if self.type !=12:
            for cell in highCell:
                if columnGrouping == 0:
                    table.mergeCells(cell[0], cell[1], cell[2], cell[3])
                else:
                    table.mergeCells(cell[1], cell[0], cell[3], cell[2])
        for cell in cells[self.type-1]:
            if columnGrouping == 0:
                table.mergeCells(cell[0], cell[1], cell[2], cell[3])
            else:
                table.mergeCells(cell[1], cell[0], cell[3], cell[2])


    def drawTable(self, dataBedprofile, flag, len = None):
        tokens = [
                 self.drawTableForAmbulance(flag, len),
                 self.drawTableFor62(flag, len),
                 self.drawTableForTomography(flag, len),
                 self.drawTableForDHospital(flag, len),
                 self.drawTableForDialysis(flag, len),
                 self.drawTableForHospital(dataBedprofile, flag, len),
                 self.drawTableForEmergency(flag, len),
                 self.drawTableForPayers(flag, len),
                 self.drawTableForAmbulanc2016(flag, len),
                 self.drawTableForStomolotogy2016(flag, len),
                 self.drawTableForDHospital2016(flag, len),
                 self.drawTableForOthers(flag, len)
                 ]
        tableColumns = tokens[self.type-1]
        return tableColumns


    def drawTableForAmbulance(self, flag, len):
        tableColumns = [
                ( '5%', [u'1. Амбулаторно-поликлиническая помощь',u'',u'1.',
                         u'1',u'',u'',u'',u'',u'',
                         u'2',u'',u'',u'',u'',u'',
                         u'3',u'',u'',u'',u'',u'',], CReportBase.AlignLeft),
                ( '5%', [u'',u'№',u'2.',
                         u'1.1',u'1.2',u'1.3',u'1.4',u'1.5',u'1.6',
                         u'2.1',u'2.2',u'2.3',u'2.4',u'2.5',u'2.6',
                         u'3.1',u'3.2',u'3.3',u'3.4',u'3.5',u'3.6'], CReportBase.AlignLeft),
                ( '5%', [u'', u'Наименование показателя',u'',
                          u'Всего число посещений и обращений к врачам и ср. мед.перс.(вкл. стоматол. помощь)',u'',u'',u'',u'',u'',
                          u'Всего число посещений и обращений к врачам(включая стоматологическую помощь)',u'',u'',u'',u'',u'',
                          u'Всего число посещений и обращений к ср. мед.перс.(вкл. стоматол. помощь)',u'',u'',u'',u'',u''], CReportBase.AlignLeft),
                ( '5%', [u'', u'',u'3.',
                          u'количество УЕТ', u'число посещений с проф. и иными целями', u'число посещений по МП в неотложной форме',
                          u'обращений  в связи с заболеваниями из них',
                          u'Посещений в обращениях по заболеванию ',u'всего посещений',
                          u'Количество УЕТ ', u'число посещений с проф. и иными целями ', u'число посещений по МП в неотложной форме ',
                          u'обращений  в связи с заболеваниями из них ',
                          u'посещений  в обращениях по заболеванию ',u'всего посещений ',
                          u'количество УЕТ  ',
                          u'число посещений с проф. и иными целями  ',
                          u'число посещений по МП в неотложной форме  ',
                          u'обращений  в связи с заболеваниями из них  ',
                          u'посещений в обращениях по заболеванию  ',u'всего посещений  '
                          ], CReportBase.AlignLeft),]
        if flag == 0:
                tableColumns.insert(6, ('10%', [u'',u'План',u'4.'], CReportBase.AlignRight))
                tableColumns.insert(6, ('10%', [u'',u'Факт',u'5.'], CReportBase.AlignRight))
        return tableColumns


    def drawTableForAmbulanc2016(self, flag, len):
        tableColumns = [
                ( '5%', [u'1. Амбулаторно-поликлиническая помощь',u'',u'1.',
                         u'1',u'',u'',u'',u'',
                         u'2',u'',u'',u'',u'',
                         u'3',u'',u'',u'',u'',], CReportBase.AlignLeft),
                ( '5%', [u'',u'№',u'2.',
                         u'1.1',u'1.2',u'1.3',u'1.4',u'1.5',
                         u'2.1',u'2.2',u'2.3',u'2.4',u'2.5',
                         u'3.1',u'3.2',u'3.3',u'3.4',u'3.5',], CReportBase.AlignLeft),
                ( '30%', [u'', u'Наименование показателя',u'',
                          u'Всего число посещений и обращений к врачам и ср. мед.перс.(без стоматол. помощи)',u'',u'',u'',u'',
                          u'Число посещений и обращений к врачам (без стоматол. помощи)',u'',u'',u'',u'',
                          u'Число посещений и обращений к ср. мед.перс.(без стоматол. помощи)',u'',u'',u'',u''], CReportBase.AlignLeft),
                ( '30%', [u'', u'',u'3.',
                          u'число посещений с проф. и иными целью (сумма стр. 2.1+3.1)',
                          u'число посещений по МП в неотложной форме (сумма стр. 2.2+3.2)',
                          u'число обращений (сумма стр. 2.3+3.3)',
                          u'число посещений по обращению по заболеванию (сумма стр. 2.4+3.4)',
                          u'всего: число посещений (сумма стр. 2.5+3.5)',
                          u'число посещений с проф. и иными целью',
                          u'число посещений по МП в неотложной форме',
                          u'число обращений (стр. 2.3 ≤2.4)',
                          u'число посещений в обращениях по заболеванию',
                          u'всего: число посещений (сумма стр. 1.1+2.2+2.4)',
                          u'число посещений с проф. и иными целью ',
                          u'число посещений по МП в неотложной форме ',
                          u'число обращений (стр. 3.3 ≤3.4) ',
                          u'число посещений в обращениях по заболеванию ',
                          u'всего: число посещений (сумма стр. 3.1+2.3+2.4)',
                          ], CReportBase.AlignLeft),

                ]
        if flag == 0:
                tableColumns.insert(6, ('10%', [u'',u'План',u'4.'], CReportBase.AlignRight))
                tableColumns.insert(6, ('10%', [u'',u'Факт',u'5.'], CReportBase.AlignRight))
        return tableColumns


    def drawTableForStomolotogy2016(self, flag, len):
        tableColumns = [
                ( '5%' if not len else '%s'%len + '%', [u' 2.Стоматологическая помощь ',u'',u'1',
                         u'1',u'',u'',u'',u'',u'', u'',
                         u'2',u'',u'',u'',u'',u'', u'',
                         u'3',u'',u'',u'',u'',u'', u'',], CReportBase.AlignLeft),
                ( '5%' if not len else '%s'%len + '%', [u'',u'№',u'2',
                         u'1.1',u'1.2',u'1.3',u'1.4',u'1.5',u'1.6',u'1.7',
                         u'2.1',u'2.2',u'2.3',u'2.4',u'2.5',u'2.6', u'2.7',
                         u'3.1',u'3.2',u'3.3',u'3.4',u'3.5',u'3.6',u'3.7'], CReportBase.AlignLeft),
                ( '5%' if not len else '%s'%len + '%', [u'', u'Наименование показателя',u'',
                          u'Всего число посещений и обращений к врачам и среднему медперсоналу, ведущему самостоятельный прием  ',u'',u'',u'',u'',u'',u'',
                          u'Число посещений и обращений к врачам ',u'',u'',u'',u'',u'',u'',
                          u'Число посещений и обращений к среднему медперсоналу, ведущему самостоятельный прием ',u'',u'',u'',u'',u'',u'',], CReportBase.AlignLeft),
                ( '5%' if not len else '%s'%len + '%', [u'', u'',u'3',
                          u'количество УЕТ (сумма стр. 2.1+3.1)',
                          u'количество СТГ',
                          u'число посещений с профилактической и иными целью (сумма стр. 2.3+3.3)',
                          u'число посещений по медицинской помощи в неотложной форме (сумма стр. 2.4+3.4)',
                          u'число обращений, в т.ч. незаконченные в связи с заболеваниями (сумма стр. 2.5+3.5) ',
                          u'число посещений, включенных в обращения, в т.ч. незаконченные в связи с заболеваниями (сумма стр. 2.6+3.6)',
                          u'всего: число посещений (сумма стр. 2.7+3.7)',
                          u'Количество УЕТ к врачам ',
                          u'Количество СТГ к врачам ',
                          u'число посещений с профилактической и иными целью',
                          u'число посещений по медицинской помощи в неотложной форме',
                          u'обращений с диагностической и/или лечебной целью в связи с заболеваниями из них к врачам ',
                          u'число обращений, в т.ч. незаконченные в связи с заболеваниями (стр. 2.5 ≤2.6)  ',
                          u'всего: число посещений (сумма стр. 2.3+2.4+2.6)',
                          u'количество УЕТ, к среднему медперсоналу, ведущему самостоятельный прием',
                          u'количество СТГ, к среднему медперсоналу, ведущему самостоятельный прием',
                          u'число посещений с профилактической и иными целью ',
                          u'число посещений по медицинской помощи в неотложной форме ',
                          u'число обращений, в т.ч. незаконченные в связи с заболеваниями (стр. 3.5 ≤3.6) ',
                          u'число посещений, включенных в обращения, в т.ч. незаконченные в связи с заболеваниями',
                          u'всего: число посещений (сумма стр. 3.3+3.4+3.6)'
                          ], CReportBase.AlignLeft), ]
        if flag == 0:
                tableColumns.insert(5, ('10%', [u'',u'Факт',u'5.'], CReportBase.AlignRight))
                tableColumns.insert(5, ('10%', [u'',u'План',u'4.'], CReportBase.AlignRight))
        return tableColumns


    def drawTableFor62(self, flag, len):
        tableColumns = [
            ( '5%', [u'2. Форма №62', u'', u'1.',
                     u'1 ', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'', u''
                     ], CReportBase.AlignLeft),
            ( '5%', [u'', u'№',u'2.',
                     u'01', u'02', u'03', u'04', u'05', u'06',u'07',u'08',u'09',u'10',u'11',u'12',u'13',u'14',u'15'
                     ], CReportBase.AlignLeft),
            ( '20%', [u'', u'Наименование показателя',u'',
                      u'Посещений  - всего, в том числе',
                      u'Посещений с профилактической целью всего', u'в том числе', u'', u'', u'',u'',
                      u'Из стр.02: посещения с профилактической целью к стоматологам',
                      u'Разовые посещения по поводу заболеваний - всего', u'из них: на дому',
                      u'Из стр.  09 - при оказании медицинской помощи в неотложной форме', u'из них: на дому ',
                      u'Посещений, включенных  в обращения в связи с заболеваниями',
                      u'Обращений по заболеванию',
                      u'Из стр. 01 - посещений медицинских работников, имеющих среднее медициснкое образование, ведущих самостоятельный прием'
                      ], CReportBase.AlignLeft),
            ( '30%', [u'', u'', u'3.',
                      u'',u'',
                      u'медицинские осмотры',
                      u'диспансеризация',
                      u'комплексный медицинский осмотр',
                      u'патронаж',
                      u'другие обстоятельства',
                      u'',u'',u'',u'',u'',u'',u'',''], CReportBase.AlignLeft),
                   ]
        if flag == 0:
                tableColumns.insert(5, ('10%', [u'',u'Факт',u'5.'], CReportBase.AlignRight))
                tableColumns.insert(5, ('10%', [u'',u'План',u'4.'], CReportBase.AlignRight))
        return tableColumns


    def drawTableFor622016(self, flag, len):
        tableColumns = [
            ( '5%', [u'2. Форма №62', u'', u'1',
                     u'1', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'', u''
                     ], CReportBase.AlignLeft),
            ( '5%', [u'', u'№',u'2',
                     u'01', u'02', u'03', u'04', u'05', u'06',u'07',u'08',u'09',u'10',u'11',u'12',u'13',u'14',u'15'
                     ], CReportBase.AlignLeft),
            ( '20%', [u'', u'Наименование показателя',u'',
                      u'Посещений - всего (сумма строк 02+09+13) в том числе',
                      u' посещений с профилактической целью всего (сумма строк с 03 по 07),',
                      u'в том числе', u'', u'', u'',u'',
                      u'Из стр.02:  - посещения с профилактической целью к стоматологам',
                      u'Разовые посещения по поводу заболеваний - всего',
                      u'из них: на дому',
                      u'Из стр.  09 - при оказании медицинской помощи в неотложной форме', u'из них: на дому',
                      u'Посещений, включенных  в обращения в связи с заболеваниями',
                      u'Обращений по заболеванию',
                      u'Из стр. 01 - посещений медицинских работников, имеющих среднее медициснкое образование, ведущих самостоятельный прием'
                      ], CReportBase.AlignLeft),
            ( '30%', [u'', u'', u'3',
                      u'',u'',
                      u'медицинские осмотры (могут быть посещения и случаи)',
                      u'диспансеризация (приказы  №216н, №72н, до 27.02.2015г №1006н, после - №36ан) случаи',
                      u'комплексный медицинский осмотр (центры здоровья)',
                      u'патронаж (дети + беременные)',
                      u'другие обстоятельства',
                      u'',u'',u'',u'',u'',u'',u'',''], CReportBase.AlignLeft),
                   ]
        k = len(tableColumns)
        if flag == 0:
                tableColumns.insert(k, ('10%', [u'',u'Факт',u'5.'], CReportBase.AlignRight))
                tableColumns.insert(k, ('10%', [u'',u'План',u'4.'], CReportBase.AlignRight))
        return tableColumns


    def drawTableForTomography(self, flag, len = None):
        tableColumns = [
            ( '5%', [u'3. Проведение КТ, МРТ амбулаторным пациентам',u'',u'1',
                     u'1',u'',u'',u'',
                     u'2',u'',u'', u''
                     ], CReportBase.AlignLeft),
            ( '5%', [u'', u'№',u'2',
                     u'1.1',u'1.1.1',u'1.2',u'1.3',
                     u'2.1',u'2.1.1',u'2.2',u'2.3'
                     ], CReportBase.AlignLeft),
            ( '5%', [u'', u'Наименование показателя',u'',
                      u'КТ',u'',u'',u'',
                      u'МРТ',u'',u'',u''
                      ], CReportBase.AlignLeft),
            ( '15%', [u'', u'',u'3',
                      u'Количество исследований',u'',u'',u'',
                      u'Количество исследований ',u'',u'',u''
                      ], CReportBase.AlignLeft),
            ( '30%', [u'', u'',u'',
                    u'ВСЕГО из них:', u'из них: с констрастированием',u'прикрепленному населению',u'неприкрепленному населению',
                     u'ВСЕГО из них: ',u'из них: с констрастированием ',u'прикрепленному населению ',u'неприкрепленному населению '
                      ], CReportBase.AlignLeft),
                   ]
        if flag == 0:
                tableColumns.insert(5, ('10%', [u'',u'Факт',u'5.'], CReportBase.AlignRight))
                tableColumns.insert(5, ('10%', [u'',u'План',u'4.'], CReportBase.AlignRight))
        return tableColumns


    def drawTableForDHospital(self, flag, len):
        tableColumns = [
            ( '5%', [u'4. Деятельность дневного стационара',u'',u'1',
                     u'1',u'',
                     u'2',
                     u'3'
                     ], CReportBase.AlignLeft),
            ( '5%', [u'', u'№',u'2',
                     u'1.1',u'1.2',
                     u'2.1',
                     u'3.1'
                     ], CReportBase.AlignLeft),
            ( '20%', [u'', u'Наименование показателя',u'',
                      u'Количество коек',u'Количество мест(с учетом сменности)',
                      u'Число пролеченных больных(чел.)',
                      u'Проведено больными дней лечения'
                      ], CReportBase.AlignLeft),
            ( '30%', [u'', u'',u'3',
                      u'',u'',
                      u'всего (чел.)',
                      u'всего (к/д)'
                      ], CReportBase.AlignLeft),
                   ]
        if flag == 0:
                tableColumns.insert(5, ('10%', [u'',u'План',u'4.'], CReportBase.AlignRight))
                tableColumns.insert(5, ('10%', [u'',u'Факт',u'5.'], CReportBase.AlignRight))
        return tableColumns


    def drawTableForDHospital2016(self, flag, len):
        tableColumns = [
            ( '5%', [u'Деятельность дневных стационаров',u'',u'1',
                     u'1',u'',
                     u'2',
                     u'3'
                     ], CReportBase.AlignLeft),
            ( '5%', [u'', u'№',u'2',
                     u'1.1',u'1.2',
                     u'2.1',
                     u'3.1'
                     ], CReportBase.AlignLeft),
            ( '20%', [u'', u'Наименование показателя',u'',
                      u'Количество коек',u'Количество мест(с учетом сменности)',
                      u'Число случаев лечения (законченные)',
                      u'Проведено больными дней  лечения'
                      ], CReportBase.AlignLeft),
            ( '30%', [u'', u'',u'3',
                      u'',u'',
                      u'всего  (чел.)',
                      u'всего  (к/д)'
                      ], CReportBase.AlignLeft),
                   ]
        if flag == 0:
                tableColumns.insert(5, ('10%', [u'',u'Факт',u'5.'], CReportBase.AlignRight))
                tableColumns.insert(5, ('10%', [u'',u'План',u'4.'], CReportBase.AlignRight))
        return tableColumns


    def drawTableForDialysis(self, flag, len):
        tableColumns = [
            ( '5%', [u'5. Диализная помощь',u'',u'1',
                     u'1',u'', u'',
                     ], CReportBase.AlignLeft),
            ( '5%', [u'', u'№',u'2',
                     u'1.1',u'1.2',u'1.3',
                     ], CReportBase.AlignLeft),
            ( '20%', [u'', u'Наименование показателя',u'',
                      u'Гемодиализ (сеансы)',
                      u'Перитонеальный диализ(сеансы)',
                      u'Продленная гемофильтрация(сеансы)'
                      ], CReportBase.AlignLeft),
            ( '30%', [u'', u'',u'3',
                      u'',
                      u'',
                      u''
                      ], CReportBase.AlignLeft),
                   ]
        if flag == 0:
                tableColumns.insert(5, ('10%', [u'',u'Факт',u'5.'], CReportBase.AlignRight))
                tableColumns.insert(5, ('10%', [u'',u'План',u'4.'], CReportBase.AlignRight))
        return tableColumns


    def drawTableForHospital(self, dataBedProfile, flag, len):
        tableColumns = [
            ( '5%', [u'6. Деятельность стационара',u'',u'1',
                     u'1',
                     u'2',u'',u'',
                     u'3',u'',u'',
                     u'4'
                     ], CReportBase.AlignLeft),
            ( '5%', [u'', u'№',u'2',
                     u'1',
                     u'2.1',u'2.2',u'2.3',
                     u'3.1',u'3.2',u'3.3',
                     u'4'
                     ], CReportBase.AlignLeft),
            ( '20%', [u'', u'Наименование показателя',u'',
                      u'Количество коек',
                      u'Число законченных случаев госпитализации(чел.)',u'',u'',
                      u'Проведено больными койко-дней', u'', u'',
                      u'Число пользованных больных',
                      ], CReportBase.AlignLeft),
            ( '30%', [u'', u'',u'3',
                      u'',
                      u'всего, в том числе (чел.) ',u'с использованием ВМП, финансируемой за счет средств ОМС (чел.)',
                      u'по медицинской реабилитации(только ГБУЗ АО "1ГКБ им Е.Е. Волосевич") (чел.)',
                      u'всего, в том числе',u'с использованием ВМП, финансируемой за счет средств ОМС',
                      u'по медицинской реабилитации(только ГБУЗ АО "1ГКБ им Е.Е. Волосевич")',
                      u''], CReportBase.AlignLeft),]
        i =6
        if flag == 0:
                tableColumns.insert(5, ('10%', [u'',u'Факт',u'5.'], CReportBase.AlignRight))
                tableColumns.insert(5, ('10%', [u'',u'План',u'4.'], CReportBase.AlignRight))
                i = i +2
        for beds in dataBedProfile:
            tableColumns.insert(i,  ( '20%', [u'', u'', beds], CReportBase.AlignRight))
            i=i+1
        return tableColumns


    def drawTableForEmergency(self, flag, len):
        tableColumns = [
            ( '5%', [u'7. Работа скорой медицинской помощи',u'',u'1',
                     u'1',u'',u'',u'',
                     ], CReportBase.AlignLeft),
            ( '5%', [u'', u'№',u'2',
                     u'1.1',u'1.2',u'1.3', u'1.4'
                     ], CReportBase.AlignLeft),
            ( '20%', [u'', u'Наименование показателя',u'',
                      u'Вызовов',
                      u'', u'', u'',
                      ], CReportBase.AlignLeft),
            ( '30%', [u'', u'',u'3',
                      u'всего ',
                      u'Сверхбазовой ОМС',
                      u'безрезультатные',
                      u'ОМС',
                      ], CReportBase.AlignLeft),
                   ]
        if flag == 0:
                tableColumns.insert(5, ('10%', [u'',u'Факт',u'5.'], CReportBase.AlignRight))
                tableColumns.insert(5, ('10%', [u'',u'План',u'4.'], CReportBase.AlignRight))
        return tableColumns


    def drawTableForPayers(self, flag, len):
        tableColumns = [
                ( '5%', [u'8. Платная медицинская помощь',u'',u'1',
                         u'1',u'',u'',u'',u'',u'',u'',u'',u'',u'',u'',u'',
                         u'2',u'',u'',u'',u'',u'',u'',u'',
                         u'3',u'',u'',u'',u'',u'',u'',u'',], CReportBase.AlignLeft),
                ( '5%', [u'',u'№',u'2',
                         u'1.1',u'1.2',u'1.3',u'1.4',u'1.5',u'1.6',u'1.7',u'1.8',u'1.9',u'1.10',u'1.11',u'1.12',
                         u'2.1',u'2.2',u'2.3',u'2.4',u'2.5',u'2.6',u'2.7',u'2.8',
                         u'3.1',u'3.2',u'3.3',u'3.4',u'3.5',u'3.6',u'3.7',u'3.8'], CReportBase.AlignLeft),
                ( '5%', [u'', u'Наименование показателя',u'',
                          u'Амбулаторно-поликническая помощь(в том числе стоматологическая помощь с учетом ортодонтии)',u'',u'',u'',u'',u'',u'',u'',u'',u'',u'',u'',
                          u'Дневные стационары',u'',u'',u'',u'',u'',u'',u'',
                          u'Круглосуточный стационар',u'',u'',u'',u'',u'',u'',u''], CReportBase.AlignLeft),
                ( '5%', [u'', u'',u'3',
                          u'посещения', u'', u'', u'',
                          u'из них стоматологические посещения(ортодонтов)', u'', u'', u'',
                          u'количество человек, получивших медицинскую услугу', u'', u'', u'',
                          u'число пролеченных пациентов', u'', u'', u'',
                          u'число пациенто-дней', u'', u'', u'',
                          u'число пролеченных пациентов ', u'', u'', u'',
                          u'число койко-дней', u'', u'', u''
                          ], CReportBase.AlignLeft),
                ( '5%', [u'', u'',u'',
                          u'ВСЕГО, из них', u'за счет средств ДМС', u'за счет личного хозяйства(личных средств граждан)',
                          u'прочие источники, в том числе по 911 постановлению',
                          u'ВСЕГО, из них ', u'за счет средств ДМС ', u'за счет личного хозяйства(личных средств граждан) ',
                          u'прочие источники, в том числе по 911 постановлению ',
                          u'ВСЕГО, из них  ', u'за счет средств ДМС  ', u'за счет личного хозяйства(личных средств граждан)  ',
                          u'прочие источники, в том числе по 911 постановлению  ',
                          u'ВСЕГО, из них(чел)', u'за счет средств ДМС(чел)', u'за счет личного хозяйства(личных средств граждан)(чел)',
                          u'прочие источники, в том числе по 911 постановлению(чел)',
                          u'ВСЕГО, из них(п/д)', u'за счет средств ДМС(п/д)', u'за счет личного хозяйства(личных средств граждан)(п/д)',
                          u'прочие источники, в том числе по 911 постановлению(п/д)',
                          u'ВСЕГО, из них(чел.)', u'за счет средств ДМС(чел.)', u'за счет личного хозяйства(личных средств граждан)(чел.)',
                          u'прочие источники, в том числе по 911 постановлению(чел.)',
                          u'ВСЕГО, из них(к/д)', u'за счет средств ДМС(к/д)', u'за счет личного хозяйства(личных средств граждан)(к/д)',
                          u'прочие источники, в том числе по 911 постановлению(к/д)'
                          ], CReportBase.AlignLeft),
                ]
        if flag == 0:
                tableColumns.insert(6, ('10%', [u'',u'Факт',u'5.'], CReportBase.AlignRight))
                tableColumns.insert(6, ('10%', [u'',u'План',u'4.'], CReportBase.AlignRight))
        return tableColumns


    def drawTableForOthers(self, flag, len):
        tableColumns = [
            ( '5%' if not len else '%s'%len + '%', [u' №',u'1',u'Диализная помощь',
                     u'1.1',u'1.2',u'1.3',
                     u'Проведение радионуклидных (сцинтиграфических) исследований в амбулаторных условиях медицинскими организациями, которым утверждены объемы по территориальной программы ОМС',
                     u'1.1',u'1.2',u'1.3',
                      u'Оказание медицинской помощи по проведению вспомогательных репродуктивных технологий (экстракорпоральное оплодотворение) по территориальной программе ОМС',
                      u'1.1',
                      u'Медицинская помощь, оказанная в условиях круглосуточного стационара с использованием телекоммуникационных технологий,  в рамках территориальной программы ОМС.',
                      u'1.1', u'1.2',
                      u' Медицинская помощь, оказанная в амбулаторных условиях с использованием передачи телеметрических данных с многоканальных кардиографов,  в рамках территориальной программы ОМС',
                      u'1.1',
                     ], CReportBase.AlignLeft),
            ( '20%' if not len else '%s'%len + '%', [u'Наименование показателя',
                      u'2',
                      u'',
                      u'Гемодиализ (сеансы)',
                      u'Перитонеальный диализ (сеансы)',
                      u'Продленная гемофильтрация (сеансы)',
                      u'',
                      u'Количество исследований',
                      u'',
                      u'',
                      u'',
                      u'Количество сеансов',
                      u'',
                      u'Оказание телемедицинской консультации',
                      u'Обращение за телемедицинской консультацией',
                      u'',
                      u'Количество диагностических исследований (только ГБУЗ АО "Вельская ЦРБ")',
                      ], CReportBase.AlignLeft),
            ( '30%' if not len else '%s'%len + '%', [u'', u'',u'',u'',u'',u'',u'',
                      u'Всего  (∑ стр. 1.2+1.3 )',
                      u'Пациентам, неприкрепленным к ФГБУЗ "СМКЦ им. Н.А. Семашко ФМБА"',
                      u'Пациентам не профильным для ГБУЗ АО "АКОД"',

                      ], CReportBase.AlignLeft),
                   ]
        if flag == 0:
                tableColumns.insert(4, ('10%' if not len else '%s'%len + '%', [u'',u'Факт',u'5.'], CReportBase.AlignRight))
                tableColumns.insert(4, ('10%' if not len else '%s'%len + '%', [u'',u'План',u'4.'], CReportBase.AlignRight))
        return tableColumns



class CReportPGGSetupDialog(QtGui.QDialog, Ui_ReportPGGSetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.cmbEventPurpose.setTable('rbEventTypePurpose', True, filter='code != \'0\'')
        self.cmbEventType.setTable('EventType', True, filter=getWorkEventTypeFilter(isApplyActive=True))
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())
        self.chbIncludeHoliday.setEnabled(True)
#        if self.type == 8:
#            self.cmbFinanceId.setEnabled(False)


    def setTitle(self, title):
        self.setWindowTitle(title)

    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.cmbEventPurpose.setValue(params.get('eventPurposeId', None))
        self.cmbEventType.setValue(params.get('eventTypeId', None))
        self.cmbSpeciality.setTable('rbSpeciality', True)
        self.cmbFinanceId.setTable('rbFinance', True)
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.cmbPerson.setValue(params.get('personId', None))
        self.cmbSex.setCurrentIndex(params.get('sex', 0))
        self.cmbColumnBy.setCurrentIndex(params.get('columnGrouping', 0))
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
        result['columnGrouping'] = self.cmbColumnBy.currentIndex()
        result['ageFrom'] = self.edtAgeFrom.value()
        result['ageTo'] = self.edtAgeTo.value()
        result['specialityId'] = self.cmbSpeciality.value()
        result['includeHoliday'] = self.chbIncludeHoliday.isChecked()
        result['financeId'] = self.cmbFinanceId.value()
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
