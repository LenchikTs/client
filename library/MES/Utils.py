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
from PyQt4.QtCore import QDate

from library.Utils import calcAgeTuple

__all__ = ( 'getServiceForSexAge',
            'getVisitForSexAge',
            'getServiceForAgeIdList',
            'getServiceNoAgeIdList',
            'getVisitsForAgeIdList',
            'getVisitsNoAgeIdList',
            'getServiceIdForAgeList',
            'getServiceIdList',
            'getActionTypeIdListByMesId',
            'getMesServiceInfo',
          )

#def getServiceIdList(mesId, necessity=None):
#    result = []
#    db = QtGui.qApp.db
#    stmt = u'''SELECT DISTINCT rbService.id FROM rbService
#LEFT JOIN mes.mrbService  ON rbService.code = mes.mrbService.code OR rbService.code = SUBSTRING(mes.mrbService.code,2)
#LEFT JOIN mes.MES_service ON mes.MES_service.service_id = mes.mrbService.id
#WHERE mes.MES_service.master_id = %d AND rbService.id IS NOT NULL''' % mesId
#    if necessity is not None:
#        stmt += ' AND mes.MES_service.necessity = %f ' % necessity
#    query = db.query(stmt)
#    while query.next():
#        record = query.record()
#        result.append(forceRef(record.value(0)))
#    return result


def getServiceForSexAge(cond, clientMesInfo):
    if clientMesInfo:
        ageStr = ''
        baseDate              = clientMesInfo[0]
        clientBirthDate      = clientMesInfo[1]
        curClientAge         = clientMesInfo[2]
        curClientAgePrevYearEnd = clientMesInfo[3]
        curClientAgeCurrYearEnd = clientMesInfo[4]
        clientSex            = clientMesInfo[5]
        if clientSex:
            cond.append('(mes.MES_service.sex = 0 OR mes.MES_service.sex = %s)'%(clientSex))
        if curClientAge:
            clientAge = curClientAge[3]
            clientAgeMonths = curClientAge[2]
            if clientAge == 0:
                clientAge = round(clientAgeMonths / 12.0, 2)
            if curClientAgePrevYearEnd is None:
                curClientAgePrevYearEnd = curClientAgeCurrYearEnd
                if baseDate and clientBirthDate:
                    curClientAgeCurrYearEnd = calcAgeTuple(clientBirthDate, QDate(baseDate.year(), 12, 31))
            clientAgeCurrYearEnd = curClientAgeCurrYearEnd[3]
            clientAgeMonthsCurrYear = curClientAgeCurrYearEnd[2]
            if clientAgeCurrYearEnd == 0:
                clientAgeCurrYearEnd = round(clientAgeMonthsCurrYear / 12.0, 2)
            clientAgePrevYearEnd = curClientAgePrevYearEnd[3]
            clientAgeMonthsPrevYear = curClientAgePrevYearEnd[2]
            if clientAgePrevYearEnd == 0:
                clientAgePrevYearEnd = round(clientAgeMonthsPrevYear / 12.0, 2)
            ageStr = u'''mes.MES_service.minimumAge <= (
            IF(mes.MES_service.begAgeUnit = 1,
            IF(mes.MES_service.controlPeriod = 1, %s, IF(mes.MES_service.controlPeriod = 2, %s, %s)),
            IF(mes.MES_service.begAgeUnit = 2,
            IF(mes.MES_service.controlPeriod = 1, %s, IF(mes.MES_service.controlPeriod = 2, %s, %s)),
            IF(mes.MES_service.begAgeUnit = 3,
            IF(mes.MES_service.controlPeriod = 1, %s, IF(mes.MES_service.controlPeriod = 2, %s, %s)),
            IF(mes.MES_service.begAgeUnit = 4,
            IF(mes.MES_service.controlPeriod = 1, %s, IF(mes.MES_service.controlPeriod = 2, %s, %s)),
            IF(mes.MES_service.controlPeriod = 1, %s, IF(mes.MES_service.controlPeriod = 2, %s, %s)))))))
            AND mes.MES_service.maximumAge >= (
            IF(mes.MES_service.endAgeUnit = 1,
            IF(mes.MES_service.controlPeriod = 1, %s, IF(mes.MES_service.controlPeriod = 2, %s, %s)),
            IF(mes.MES_service.endAgeUnit = 2,
            IF(mes.MES_service.controlPeriod = 1, %s, IF(mes.MES_service.controlPeriod = 2, %s, %s)),
            IF(mes.MES_service.endAgeUnit = 3,
            IF(mes.MES_service.controlPeriod = 1, %s, IF(mes.MES_service.controlPeriod = 2, %s, %s)),
            IF(mes.MES_service.endAgeUnit = 4,
            IF(mes.MES_service.controlPeriod = 1, %s, IF(mes.MES_service.controlPeriod = 2, %s, %s)),
            IF(mes.MES_service.controlPeriod = 1, %s, IF(mes.MES_service.controlPeriod = 2, %s, %s))
            )))))
            '''%(u'%.2f'%(curClientAgeCurrYearEnd[0]), u'%.2f'%(curClientAgePrevYearEnd[0]), u'%.2f'%(curClientAge[0]),
            u'%.2f'%(curClientAgeCurrYearEnd[1]), u'%.2f'%(curClientAgePrevYearEnd[1]), u'%.2f'%(curClientAge[1]),
            u'%.2f'%(curClientAgeCurrYearEnd[2]),u'%.2f'%(curClientAgePrevYearEnd[2]),u'%.2f'%(curClientAge[2]),
            u'%.2f'%(curClientAgeCurrYearEnd[3]), u'%.2f'%(curClientAgePrevYearEnd[3]), u'%.2f'%(curClientAge[3]),
            u'%.2f'%(clientAgeCurrYearEnd), u'%.2f'%(clientAgePrevYearEnd), u'%.2f'%(clientAge),
            u'%.2f'%(curClientAgeCurrYearEnd[0]), u'%.2f'%(curClientAgePrevYearEnd[0]), u'%.2f'%(curClientAge[0]),
            u'%.2f'%(curClientAgeCurrYearEnd[1]), u'%.2f'%(curClientAgePrevYearEnd[1]), u'%.2f'%(curClientAge[1]),
            u'%.2f'%(curClientAgeCurrYearEnd[2]),u'%.2f'%(curClientAgePrevYearEnd[2]),u'%.2f'%(curClientAge[2]),
            u'%.2f'%(curClientAgeCurrYearEnd[3]), u'%.2f'%(curClientAgePrevYearEnd[3]), u'%.2f'%(curClientAge[3]),
            u'%.2f'%(clientAgeCurrYearEnd), u'%.2f'%(clientAgePrevYearEnd), u'%.2f'%(clientAge)
            )
        cond.append(ageStr)
    return cond


def getVisitForSexAge(cond, clientMesInfo):
    if clientMesInfo:
        ageStr = ''
        baseDate              = clientMesInfo[0]
        clientBirthDate      = clientMesInfo[1]
        curClientAge         = clientMesInfo[2]
        curClientAgePrevYearEnd = clientMesInfo[3]
        curClientAgeCurrYearEnd = clientMesInfo[4]
        clientSex            = clientMesInfo[5]
        if clientSex:
            cond.append('(mes.MES_visit.sex = 0 OR mes.MES_visit.sex = %s)'%(clientSex))
        if curClientAge:
            clientAge = curClientAge[3]
            clientAgeMonths = curClientAge[2]
            if clientAge == 0:
                clientAge = round(clientAgeMonths / 12.0, 2)
            if curClientAgePrevYearEnd is None:
                curClientAgePrevYearEnd = curClientAgeCurrYearEnd
                if baseDate and clientBirthDate:
                    clientAgeCurrYearEnd = calcAgeTuple(clientBirthDate, QDate(baseDate.year(), 12, 31))
            clientAgeCurrYearEnd = curClientAgeCurrYearEnd[3]
            clientAgeMonthsCurrYear = curClientAgeCurrYearEnd[2]
            if clientAgeCurrYearEnd == 0:
                clientAgeCurrYearEnd = round(clientAgeMonthsCurrYear / 12.0, 2)
            clientAgePrevYearEnd = curClientAgePrevYearEnd[3]
            clientAgeMonthsPrevYear = curClientAgePrevYearEnd[2]
            if clientAgePrevYearEnd == 0:
                clientAgePrevYearEnd = round(clientAgeMonthsPrevYear / 12.0, 2)
            ageStr = u'''mes.MES_visit.minimumAge <= (
            IF(mes.MES_visit.begAgeUnit = 1,
            IF(mes.MES_visit.controlPeriod = 1, %s, IF(mes.MES_visit.controlPeriod = 2, %s, %s)),
            IF(mes.MES_visit.begAgeUnit = 2,
            IF(mes.MES_visit.controlPeriod = 1, %s, IF(mes.MES_visit.controlPeriod = 2, %s, %s)),
            IF(mes.MES_visit.begAgeUnit = 3,
            IF(mes.MES_visit.controlPeriod = 1, %s, IF(mes.MES_visit.controlPeriod = 2, %s, %s)),
            IF(mes.MES_visit.begAgeUnit = 4,
            IF(mes.MES_visit.controlPeriod = 1, %s, IF(mes.MES_visit.controlPeriod = 2, %s, %s)),
            IF(mes.MES_visit.controlPeriod = 1, %s, IF(mes.MES_visit.controlPeriod = 2, %s, %s)))))))
            AND mes.MES_visit.maximumAge >= (
            IF(mes.MES_visit.endAgeUnit = 1,
            IF(mes.MES_visit.controlPeriod = 1, %s, IF(mes.MES_visit.controlPeriod = 2, %s, %s)),
            IF(mes.MES_visit.endAgeUnit = 2,
            IF(mes.MES_visit.controlPeriod = 1, %s, IF(mes.MES_visit.controlPeriod = 2, %s, %s)),
            IF(mes.MES_visit.endAgeUnit = 3,
            IF(mes.MES_visit.controlPeriod = 1, %s, IF(mes.MES_visit.controlPeriod = 2, %s, %s)),
            IF(mes.MES_visit.endAgeUnit = 4,
            IF(mes.MES_visit.controlPeriod = 1, %s, IF(mes.MES_visit.controlPeriod = 2, %s, %s)),
            IF(mes.MES_visit.controlPeriod = 1, %s, IF(mes.MES_visit.controlPeriod = 2, %s, %s))
            )))))
            '''%(u'%.2f'%(curClientAgeCurrYearEnd[0]), u'%.2f'%(curClientAgePrevYearEnd[0]), u'%.2f'%(curClientAge[0]),
            u'%.2f'%(curClientAgeCurrYearEnd[1]), u'%.2f'%(curClientAgePrevYearEnd[1]), u'%.2f'%(curClientAge[1]),
            u'%.2f'%(curClientAgeCurrYearEnd[2]),u'%.2f'%(curClientAgePrevYearEnd[2]),u'%.2f'%(curClientAge[2]),
            u'%.2f'%(curClientAgeCurrYearEnd[3]), u'%.2f'%(curClientAgePrevYearEnd[3]), u'%.2f'%(curClientAge[3]),
            u'%.2f'%(clientAgeCurrYearEnd), u'%.2f'%(clientAgePrevYearEnd), u'%.2f'%(clientAge),
            u'%.2f'%(curClientAgeCurrYearEnd[0]), u'%.2f'%(curClientAgePrevYearEnd[0]), u'%.2f'%(curClientAge[0]),
            u'%.2f'%(curClientAgeCurrYearEnd[1]), u'%.2f'%(curClientAgePrevYearEnd[1]), u'%.2f'%(curClientAge[1]),
            u'%.2f'%(curClientAgeCurrYearEnd[2]),u'%.2f'%(curClientAgePrevYearEnd[2]),u'%.2f'%(curClientAge[2]),
            u'%.2f'%(curClientAgeCurrYearEnd[3]), u'%.2f'%(curClientAgePrevYearEnd[3]), u'%.2f'%(curClientAge[3]),
            u'%.2f'%(clientAgeCurrYearEnd), u'%.2f'%(clientAgePrevYearEnd), u'%.2f'%(clientAge)
            )
        cond.append(ageStr)
    return cond


def getServiceForAgeIdList(mesId, isNecessary=False, clientMesInfo=None, eventDate=None):
    db = QtGui.qApp.db
    tableRbService = db.table('rbService')
    tableMrbService = db.table('mes.mrbService')
    tableMesService = db.table('mes.MES_service')
    table = tableRbService.leftJoin(tableMrbService, tableRbService['code'].eq(tableMrbService['code']))
    table = table.leftJoin(tableMesService, tableMesService['service_id'].eq(tableMrbService['id']))
    cond = [ tableMesService['master_id'].eq(mesId),
             tableMesService['deleted'].eq(0)
           ]
    if eventDate:
        cond.append(db.joinOr([tableMesService['begDate'].isNull(), tableMesService['begDate'].le(eventDate)]))
        cond.append(db.joinOr([tableMesService['endDate'].isNull(), tableMesService['endDate'].ge(eventDate)]))
    cond = getServiceForSexAge(cond, clientMesInfo)
    if isNecessary:
        cond.append(tableMesService['necessity'].gt(0.999999))
    resultByServices = db.getDistinctIdList(table, tableRbService['id'], cond)
    return resultByServices


def getServiceNoAgeIdList(mesId, isNecessary=False, clientMesInfo=None, eventDate=None):
    db = QtGui.qApp.db
    tableRbService = db.table('rbService')
    tableMrbService = db.table('mes.mrbService')
    tableMesService = db.table('mes.MES_service')
    table = tableRbService.leftJoin(tableMrbService, tableRbService['code'].eq(tableMrbService['code']))
    table = table.leftJoin(tableMesService, tableMesService['service_id'].eq(tableMrbService['id']))
    cond = [ tableMesService['master_id'].eq(mesId),
             tableMesService['deleted'].eq(0),
             tableMesService['begAgeUnit'].eq(0),
             tableMesService['endAgeUnit'].eq(0)
           ]
    if eventDate:
        cond.append(db.joinOr([tableMesService['begDate'].isNull(), tableMesService['begDate'].le(eventDate)]))
        cond.append(db.joinOr([tableMesService['endDate'].isNull(), tableMesService['endDate'].ge(eventDate)]))
    clientSex = clientMesInfo[5]
    if clientSex:
        cond.append('(mes.MES_service.sex = 0 OR mes.MES_service.sex = %s)'%(clientSex))
    curClientAge = clientMesInfo[2]
    if curClientAge:
        cond.append(tableMesService['master_id'].isNotNull())
        cond.append(u'''((TRIM(mes.MES_service.minimumAge) = '' OR mes.MES_service.minimumAge = 0)
      AND (TRIM(mes.MES_service.maximumAge) = '' OR mes.MES_service.maximumAge = 0))''')
    if isNecessary:
        cond.append(tableMesService['necessity'].gt(0.999999))
    resultByServices = db.getDistinctIdList(table, tableRbService['id'], cond)
    return resultByServices


def getVisitsForAgeIdList(mesId, isNecessary=False, clientMesInfo=None):
    db = QtGui.qApp.db
    tableRbService = db.table('rbService')
    tableMesVisit = db.table('mes.MES_visit')
    table = tableRbService.innerJoin(tableMesVisit, 'rbService.code = mes.MES_visit.serviceCode AND mes.MES_visit.deleted=0')
    visitsCond =[tableMesVisit['master_id'].eq(mesId),
                 tableMesVisit['additionalServiceCode'].ne(''),
                 tableMesVisit['additionalServiceCode'].ne('0'),
                ]
    visitsCond = getVisitForSexAge(visitsCond, clientMesInfo)
    resultByVisits = db.getDistinctIdList(table,
                                          tableRbService['id'],
                                          visitsCond
                                         )
    return resultByVisits


def getVisitsNoAgeIdList(mesId, isNecessary=False, clientMesInfo=None):
    db = QtGui.qApp.db
    tableRbService = db.table('rbService')
    tableMesVisit = db.table('mes.MES_visit')
    table = tableRbService.innerJoin(tableMesVisit, 'rbService.code = mes.MES_visit.serviceCode AND mes.MES_visit.deleted=0')
    visitsCond =[tableMesVisit['master_id'].eq(mesId),
                 tableMesVisit['additionalServiceCode'].ne(''),
                 tableMesVisit['additionalServiceCode'].ne('0'),
                 tableMesVisit['begAgeUnit'].eq(0),
                 tableMesVisit['endAgeUnit'].eq(0)
                ]
    clientSex = clientMesInfo[5]
    if clientSex:
        visitsCond.append('(mes.MES_visit.sex = 0 OR mes.MES_visit.sex = %s)'%(clientSex))
    curClientAge = clientMesInfo[2]
    if curClientAge:
        visitsCond.append(tableMesVisit['master_id'].isNotNull())
        visitsCond.append(u'''((TRIM(mes.MES_visit.minimumAge) = '' OR mes.MES_visit.minimumAge = 0)
      AND (TRIM(mes.MES_visit.maximumAge) = '' OR mes.MES_visit.maximumAge = 0))''')
    resultByVisits = db.getDistinctIdList(table,
                                          tableRbService['id'],
                                          visitsCond
                                         )
    return resultByVisits


def getServiceIdForAgeList(mesId, isNecessary=False, clientMesInfo=None, eventDate=None):
    resultByServicesAge = getServiceForAgeIdList(mesId, isNecessary, clientMesInfo, eventDate)
    resultByServicesNoAge = getServiceNoAgeIdList(mesId, isNecessary, clientMesInfo, eventDate)
    resultByServices = list(set(resultByServicesAge)|set(resultByServicesNoAge))

    resultByVisitsAge = getVisitsForAgeIdList(mesId, isNecessary, clientMesInfo)
    resultByVisitsNoAge = getVisitsNoAgeIdList(mesId, isNecessary, clientMesInfo)
    resultByVisits = list(set(resultByVisitsAge)|set(resultByVisitsNoAge))

    return list(set(resultByServices)|set(resultByVisits))


def getServiceIdList(mesId, isNecessary=False, clientMesInfo=None, eventDate=None):
    db = QtGui.qApp.db
    tableRbService = db.table('rbService')
    tableMrbService = db.table('mes.mrbService')
    tableMesService = db.table('mes.MES_service')
    table = tableRbService.leftJoin(tableMrbService, tableRbService['code'].eq(tableMrbService['code']))
    table = table.leftJoin(tableMesService, tableMesService['service_id'].eq(tableMrbService['id']))
    cond = [ tableMesService['master_id'].eq(mesId),
             tableMesService['deleted'].eq(0)
           ]
    if eventDate:
        cond.append(db.joinOr([tableMesService['begDate'].isNull(), tableMesService['begDate'].le(eventDate)]))
        cond.append(db.joinOr([tableMesService['endDate'].isNull(), tableMesService['endDate'].ge(eventDate)]))
#    condNo = cond
    cond = getServiceForSexAge(cond, clientMesInfo)
    if isNecessary:
        cond.append(tableMesService['necessity'].gt(0.999999))
    resultByServices = db.getDistinctIdList(table, tableRbService['id'], cond)
    tableMesVisit = db.table('mes.MES_visit')
    table = tableRbService.innerJoin(tableMesVisit, 'rbService.code = mes.MES_visit.serviceCode AND mes.MES_visit.deleted=0')
    visitsCond =[tableMesVisit['master_id'].eq(mesId),
                 tableMesVisit['additionalServiceCode'].ne(''),
                 tableMesVisit['additionalServiceCode'].ne('0'),
                ]
    visitsCond = getVisitForSexAge(visitsCond, clientMesInfo)
    resultByVisits = db.getDistinctIdList(table,
                                          tableRbService['id'],
                                          visitsCond
                                         )
    return list(set(resultByServices)|set(resultByVisits))


def getActionTypeIdListByMesId(mesId, necessity=None):
    serviceIdList = getServiceIdList(mesId, necessity)
    db = QtGui.qApp.db
    tableActionTypeService = db.table('ActionType_Service')
    tableActionType = db.table('ActionType')
    cond = [tableActionType['deleted'].eq(0),
            tableActionTypeService['service_id'].inlist(serviceIdList)
           ]
    table = tableActionTypeService.leftJoin(tableActionType, tableActionType['id'].eq(tableActionTypeService['master_id']))
    result = db.getDistinctIdList(table, tableActionTypeService['master_id'].name(), cond)
    return result


def getMesServiceInfo(serviceCode, mesId):
    db = QtGui.qApp.db
    stmt = u'SELECT mes.mrbService.doctorWTU, mes.mrbService.paramedicalWTU, mes.MES_service.averageQnt, mes.MES_service.necessity FROM mes.MES_service  LEFT JOIN mes.mrbService ON mes.mrbService.id = mes.MES_service.service_id WHERE mes.MES_service.master_id = %d AND mes.mrbService.code = \'%s\'' % (mesId, serviceCode)
    query = db.query(stmt)
    if query.first():
        return query.record()
    return None


