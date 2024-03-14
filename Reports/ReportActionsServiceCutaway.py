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
from PyQt4.QtCore import QDate

from library.database   import addDateInRange
from library.Utils      import forceDouble, forceInt, forceRef, forceString, formatName
from Events.Utils       import getActionTypeDescendants
from Orgs.Utils         import getOrgStructureFullName
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.ReportView import CPageFormat
from Reports.ReportSetupDialog import CReportSetupDialog
from Reports.StatReport1NPUtil import havePermanentAttach


def selectData(params):
    begDate             = params.get('begDate', QDate())
    endDate             = params.get('endDate', QDate())
    eventTypeId         = params.get('eventTypeId', None)
    sex                 = params.get('sex', 0)
    ageFrom             = params.get('ageFrom', 0)
    ageTo               = params.get('ageTo', 150)
    actionTypeClass     = params.get('actionTypeClass', None)
    actionTypeId        = params.get('actionTypeId', None)
    onlyPermanentAttach = params.get('onlyPermanentAttach', None)
    MKBFilter           = params.get('MKBFilter', 0)
    MKBFrom             = params.get('MKBFrom', '')
    MKBTo               = params.get('MKBTo', '')
    onlyPayedEvents     = params.get('onlyPayedEvents', False)
    begPayDate          = params.get('begPayDate', QDate())
    endPayDate          = params.get('endPayDate', QDate())
    detailPerson        = params.get('detailPerson', False)
    personId            = params.get('personId', None)
    specialityId        = params.get('specialityId', None)
    orgStructureId      = params.get('orgStructureId', None)
    insurerId           = params.get('insurerId', None)
    socStatusTypeId     = params.get('socStatusTypeId', None)
    isProfile           = params.get('isProfile', 0)
    eventStatus         = params.get('eventStatus', 0)
    noteUET             = params.get('noteUET', 0)

    db = QtGui.qApp.db
    tableEvent              = db.table('Event')
    tableClient             = db.table('Client')
    tableAction             = db.table('Action')
    tableActionType         = db.table('ActionType')
    tableActionTypeService  = db.table('ActionType_Service')
    tableService            = db.table('rbService')
    tablePerson             = db.table('Person')
    tablePost               = db.table('rbPost')
    tableContract           = db.table('Contract')
    tableOrgStructure       = db.table('OrgStructure')
    tableSpeciality         = db.table('rbSpeciality')
    tableAccountItem        = db.table('Account_Item')

    queryTable = tableEvent.leftJoin(tableAction, tableAction['event_id'].eq(tableEvent['id']))
    queryTable = queryTable.leftJoin(tableClient, tableClient['id'].eq(tableEvent['client_id']))
    queryTable = queryTable.leftJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
    queryTable = queryTable.leftJoin(tableContract, 'Contract.`id`=IF(Action.`contract_id`, Action.`contract_id`, Event.`contract_id`)')
    actionTypeServiceJoinCond = 'IF(ActionType_Service.`finance_id`, ActionType_Service.`finance_id`=Contract.`finance_id`, ActionType_Service.`finance_id` IS NULL)'
    queryTable = queryTable.leftJoin(tableActionTypeService,
                                     [tableActionType['id'].eq(tableActionTypeService['master_id']),
                                      actionTypeServiceJoinCond])
    queryTable = queryTable.leftJoin(tableService, tableService['id'].eq(tableActionTypeService['service_id']))
    queryTable = queryTable.leftJoin(tablePerson, tablePerson['id'].eq(tableAction['person_id']))
    queryTable = queryTable.leftJoin(tableSpeciality, tableSpeciality['id'].eq(tablePerson['speciality_id']))
    queryTable = queryTable.leftJoin(tableOrgStructure, tableOrgStructure['id'].eq(tablePerson['orgStructure_id']))

    cond = [tableAction['endDate'].isNotNull(),
            tableAction['deleted'].eq(0),
            tableEvent['deleted'].eq(0)]
    if begDate:
        cond.append(tableAction['endDate'].ge(begDate))
    if endDate:
        cond.append(tableAction['endDate'].lt(endDate.addDays(1)))
    if eventTypeId:
        cond.append(tableEvent['eventType_id'].eq(eventTypeId))
    if sex:
        cond.append(tableClient['sex'].eq(sex))
    if ageFrom <= ageTo and ageTo:
        if eventStatus == 2:
            cond.append(db.joinOr([tableEvent['execDate'].isNull(),
                                   db.joinAnd(['Event.execDate >= ADDDATE(Client.birthDate, INTERVAL %d YEAR)'%ageFrom,
                                               'Event.execDate < SUBDATE(ADDDATE(Client.birthDate, INTERVAL %d YEAR),1)'%(ageTo+1)
                                               ])
                                  ]))
        elif eventStatus == 1:
            cond.append(tableEvent['execDate'].isNull())
        else:
            cond.append('Event.execDate >= ADDDATE(Client.birthDate, INTERVAL %d YEAR)'%ageFrom)
            cond.append('Event.execDate < SUBDATE(ADDDATE(Client.birthDate, INTERVAL %d YEAR),1)'%(ageTo+1))
    if socStatusTypeId:
        tableClientSocStatus = db.table('ClientSocStatus')
        if begDate:
            cond.append(db.joinOr([db.joinAnd([tableClientSocStatus['endDate'].isNotNull(),
                                               tableClientSocStatus['endDate'].dateGe(begDate)
                                              ]),
                                   tableClientSocStatus['endDate'].isNull()
                                  ]))
        if endDate:
            cond.append(db.joinOr([db.joinAnd([tableClientSocStatus['begDate'].isNotNull(),
                                               tableClientSocStatus['begDate'].dateLt(endDate.addDays(1))
                                              ]),
                                   tableClientSocStatus['begDate'].isNull()
                                  ]))
        queryTable = queryTable.leftJoin(tableClientSocStatus, tableClientSocStatus['client_id'].eq(tableClient['id']))
        cond.append(tableClientSocStatus['socStatusType_id'].eq(socStatusTypeId))
        cond.append(tableClientSocStatus['deleted'].eq(0))
    if actionTypeId:
        cond.append(tableActionType['id'].inlist(getActionTypeDescendants(actionTypeId, actionTypeClass)))
    elif actionTypeClass is not None:
        cond.append(tableActionType['class'].eq(actionTypeClass))
    if onlyPermanentAttach:
        cond.append(havePermanentAttach(endDate))
    if MKBFilter:
        tableDiagnostic = db.table('Diagnostic')
        tableDiagnosis = db.table('Diagnosis')
        subQueryTable = tableDiagnosis.leftJoin(tableDiagnostic, tableDiagnosis['id'].eq(tableDiagnostic['diagnosis_id']))
        subCond = [ tableDiagnostic['event_id'].eq(tableEvent['id']),
                    tableDiagnosis['MKB'].between(MKBFrom, MKBTo)
                  ]
        cond.append(db.existsStmt(subQueryTable, subCond))
    if onlyPayedEvents:
#        cond.append('isEventPayed(Event.id)')
        accountItemJoinCond = '( Account_Item.id = (SELECT max(AI.id) FROM Account_Item AS AI WHERE AI.deleted=0 AND AI.date IS NOT NULL AND AI.refuseType_id IS NULL AND AI.reexposeItem_id IS NULL AND AI.visit_id IS NULL AND AI.action_id=Action.id))'
        queryTable = queryTable.leftJoin(tableAccountItem, accountItemJoinCond)
        cond.append(tableAction['id'].eq(tableAccountItem['action_id']))
        addDateInRange(cond, tableAccountItem['date'], begPayDate, endPayDate)
    if not detailPerson:
        if personId:
            cond.append(tableAction['person_id'].eq(personId))
    if specialityId:
        cond.append(tablePerson['speciality_id'].eq(specialityId))
    if orgStructureId:
        orgStructureIdList = db.getDescendants('OrgStructure', 'parent_id', orgStructureId)
        cond.append(tablePerson['orgStructure_id'].inlist(orgStructureIdList))
    if insurerId:
        cond.append('EXISTS (SELECT ClientPolicy.`client_id` FROM ClientPolicy WHERE ClientPolicy.`insurer_id`=%d AND ClientPolicy.`client_id`=Client.`id`)' % insurerId)

    if noteUET:
        queryTable = queryTable.leftJoin(tablePost, tablePost['id'].eq(tablePerson['post_id']))
        fieldUetDoctor = '''IF(rbPost.id IS NOT NULL AND (rbPost.code LIKE '1%%' OR rbPost.code LIKE '2%%' OR rbPost.code LIKE '3%%'), Action.uet, 0) AS uetDoctor'''
        fieldUetAverageMedWorker = '''IF(rbPost.id IS NOT NULL AND (rbPost.code NOT LIKE '1%%' AND rbPost.code NOT LIKE '2%%' AND rbPost.code NOT LIKE '3%%'), Action.uet, 0) AS uetAverageMedWorker'''
    else:
        fieldUetDoctor = 'IF(YEAR(FROM_DAYS(DATEDIFF(Action.`endDate`, Client.`birthDate`))) < 18, rbService.`childUetDoctor`, rbService.`adultUetDoctor`) AS uetDoctor'
        fieldUetAverageMedWorker = 'IF(YEAR(FROM_DAYS(DATEDIFF(Action.`endDate`, Client.`birthDate`))) < 18, rbService.`childUetAverageMedWorker`, rbService.`adultUetAverageMedWorker`) AS uetAverageMedWorker'

    fields = [tableAction['id'].alias('actionId'),
              tableAction['person_id'].name(),
              tableAction['finance_id'].name(),
              tableAction['payStatus'].alias('actionPayStatus'),
              tableAction['amount'].alias('actionAmount'),
              tableAction['uet'].alias('actionUet'),
              tableEvent['payStatus'].alias('eventPayStatus'),
              tablePerson['lastName'].alias('personLastName'),
              tablePerson['firstName'].alias('personFirstName'),
              tablePerson['patrName'].alias('personPatrName'),
              tableSpeciality['name'].alias('specialityName'),
              tableActionType['code'].alias('actionTypeCode'),
              tableActionType['name'].alias('actionTypeName'),
              tableOrgStructure['id'].alias('orgStructureId')
              ]
    if isProfile:
        cond.append('AIS.id = rbService.id OR AIS.id IS NULL')
        tableAIP = db.table('Account_Item').alias('AIP')
        tableAIS = db.table('rbService').alias('AIS')
        tableActionAI = db.table('Action').alias('ActionAI')
        fields.append(tableAIS['id'].alias('serviceIdAIP'))
        fields.append(tableAIP['amount'].alias('amountAIP'))
        fields.append(tableAIS['code'].alias('serviceCodeAIP'))
        fields.append(tableAIS['name'].alias('serviceNameAIP'))
        queryTable = queryTable.leftJoin(tableAIP, db.joinAnd([tableAIP['action_id'].eq(tableAction['id']),
                                                               tableAIP['deleted'].eq(0)]))
        queryTable = queryTable.leftJoin(tableAIS, tableAIP['service_id'].eq(tableAIS['id']))
        queryTable = queryTable.leftJoin(tableActionAI, tableActionAI['id'].eq(tableAIP['action_id']))
        if noteUET:
            tablePersonAI = db.table('Person').alias('PersonAI')
            tablePostAI = db.table('rbPost').alias('PostAI')
            queryTable = queryTable.leftJoin(tablePersonAI, tablePersonAI['id'].eq(tableActionAI['person_id']))
            queryTable = queryTable.leftJoin(tablePostAI, tablePostAI['id'].eq(tablePersonAI['post_id']))
            fieldUetDoctorAIP = '''IF(PostAI.id IS NOT NULL AND (PostAI.code LIKE '1%%' OR PostAI.code LIKE '2%%' OR PostAI.code LIKE '3%%'), ActionAI.uet, 0) AS uetDoctorAIP'''
            fieldUetAverageMedWorkerAIP = '''IF(PostAI.id IS NOT NULL AND (PostAI.code NOT LIKE '1%%' AND PostAI.code NOT LIKE '2%%' AND PostAI.code NOT LIKE '3%%'), ActionAI.uet, 0) AS uetAverageMedWorkerAIP'''
        else:
            fieldUetDoctorAIP = 'IF(YEAR(FROM_DAYS(DATEDIFF(ActionAI.`endDate`, Client.`birthDate`))) < 18, AIS.`childUetDoctor`, AIS.`adultUetDoctor`) AS uetDoctorAIP'
            fieldUetAverageMedWorkerAIP = 'IF(YEAR(FROM_DAYS(DATEDIFF(ActionAI.`endDate`, Client.`birthDate`))) < 18, AIS.`childUetAverageMedWorker`, AIS.`adultUetAverageMedWorker`) AS uetAverageMedWorkerAIP'
        fields.append(tableActionAI['uet'].alias('actionUetAI'))
        fields.append(fieldUetDoctorAIP)
        fields.append(fieldUetAverageMedWorkerAIP)
    order = ', '.join([tableAction['id'].name(),
             tableActionTypeService['finance_id'].name()])
    fields.append(tableService['id'].alias('serviceId'))
    fields.append(tableService['code'].alias('serviceCode'))
    fields.append(fieldUetDoctor)
    fields.append(fieldUetAverageMedWorker)
    stmt = db.selectStmt(queryTable, fields, cond, order+' DESC')
    return db.query(stmt)


def payStatusCheck(payStatus, condFinanceCode):
    if condFinanceCode:
        payCode = (payStatus >> (2*condFinanceCode)) & 3
        if payCode:
            return True
    return False


class CReportActionsServiceCutaway(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Отчет по УЕТ')
        self._mapOrgStructureIdOrder = {}
        self.orientation = CPageFormat.Landscape


    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setPayPeriodVisible(True)
        result.setWorkOrganisationVisible(True)
        result.setSexVisible(True)
        result.setAgeVisible(True)
        result.setActionTypeVisible(True)
        result.setMKBFilterVisible(True)
        result.setInsurerVisible(True)
        result.setOrgStructureVisible(True)
        result.setSpecialityVisible(True)
        result.setPersonVisible(True)
        result.setSocStatusTypeVisible(True)
        result.setFinanceVisible(True)
        result.setDetailActionVisible(True)
        result.setEventStatusVisible(True)
        result.setNoteUETVisible(True)
        result.setTitle(self.title())
        return result


    def dumpParams(self, cursor, params):
        description = self.getDescription(params)
        description.insert(len(description)-2, u'детализация %s'%([u'по Действиям', u'по Профилям'][params.get('isProfile', 0)]))
        description.insert(len(description)-2, u'события %s'%([u'только закрытые', u'только открытые', u'все'][params.get('eventStatus', 0)]))
        description.insert(len(description)-2, u'учитывать УЕТ: %s'%([u'по нормативу', u'по исполнителю'][params.get('noteUET', 0)]))
        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


    def build(self, params):
        detailPerson    = params.get('detailPerson', False)
        condFinanceId   = params.get('financeId', None)
        condFinanceCode = params.get('financeCode', '0')
        isProfile       = params.get('isProfile', 0)
        noteUET         = params.get('noteUET', 0)
        query = selectData(params)
        reportData = {}
        mapOrgStructureToFullName = {}
        origActionIdList = {}
        serviceIdList = []
        resultActionIdList = []
        def setProfileData(record, profileData = {}):
            serviceIdAI   = forceRef(record.value('serviceIdAIP'))
            if serviceIdAI:
                serviceCodeAI = forceString(record.value('serviceCodeAIP'))
                serviceNameAI = forceString(record.value('serviceNameAIP'))
                amountAI      = forceInt(record.value('amountAIP'))
                actionUetAI   = forceDouble(record.value('actionUetAI'))
                uetDoctorAIP  = forceDouble(record.value('uetDoctorAIP'))
                uetAverageMedWorkerAIP = forceDouble(record.value('uetAverageMedWorkerAIP'))
                profileLine = profileData.get(serviceIdAI, [])
                if not profileLine:
                    profileLine = [serviceNameAI, serviceCodeAI, amountAI, uetDoctorAIP, uetAverageMedWorkerAIP, actionUetAI]
                else:
                    profileLine[2] += amountAI
                profileData[serviceIdAI] = profileLine
            return profileData
        while query.next():
            record = query.record()
            actionId               = forceRef(record.value('actionId'))
            serviceCode            = forceString(record.value('serviceCode'))
            serviceId              = forceString(record.value('serviceId'))
            serviceIdList = origActionIdList.get(actionId, [])
            if serviceId in serviceIdList:
                continue
            serviceIdList.append(serviceId)
            origActionIdList[actionId] = serviceIdList
            orgStructureId         = forceString(record.value('orgStructureId'))
            financeId              = forceRef(record.value('finance_id'))
            actionPayStatus        = forceInt(record.value('actionPayStatus'))
            eventPayStatus         = forceInt(record.value('eventPayStatus'))
            actionTypeCode         = forceString(record.value('actionTypeCode'))
            actionTypeName         = forceString(record.value('actionTypeName'))
            amount                 = forceInt(record.value('actionAmount'))
            actionUet              = round(forceDouble(record.value('actionUet')), 2)
            uetDoctor              = round(forceDouble(record.value('uetDoctor')), 2)
            uetAverageMedWorker    = round(forceDouble(record.value('uetAverageMedWorker')), 2)
            personName             = formatName(record.value('personLastName'),
                                                record.value('personFirstName'),
                                                record.value('personPatrName'))
            specialityName         = forceString(record.value('specialityName'))

            if condFinanceId:
                if financeId:
                    if condFinanceId != financeId:
                        continue
                else:
                    payStatus = actionPayStatus if actionPayStatus else eventPayStatus
                    if not payStatusCheck(payStatus, forceInt(condFinanceCode)):
                        continue

            if specialityName:
                personName = personName + ' | ' + specialityName

            orgStructureName = mapOrgStructureToFullName.get(orgStructureId, None)
            if not orgStructureName:
                orgStructureName = getOrgStructureFullName(orgStructureId)
                mapOrgStructureToFullName[orgStructureId] = orgStructureName

            if not orgStructureName:
                continue

            if noteUET:
                uetDoctorAmount = uetDoctor
                uetAverageMedWorkerAmount = uetAverageMedWorker
            else:
                uetDoctorAmount = amount*uetDoctor
                uetAverageMedWorkerAmount = uetAverageMedWorker*amount

            existsData = reportData.get(orgStructureName, None)
            currentKey = (actionTypeName, actionTypeCode)
            if detailPerson:
                if not existsData:
                    existsData = {}
                    personData = {}
                    actionAmount = 1
                    resultActionIdList.append(actionId)
                    serviceCodeList = serviceCode
                    infoLine = [serviceCodeList, actionAmount, amount, uetDoctorAmount, uetAverageMedWorkerAmount]
                    if isProfile:
                        infoLine.append(setProfileData(record, {}))
                    infoLine.append(actionUet)
                    personData[currentKey] = infoLine
                    existsData[personName] = personData
                    reportData[orgStructureName] = existsData
                else:
                    personData = existsData.get(personName, None)
                    if not personData:
                        personData = {}
                        actionAmount = 1
                        resultActionIdList.append(actionId)
                        serviceCodeList = serviceCode
                        infoLine = [serviceCodeList, actionAmount, amount, uetDoctorAmount, uetAverageMedWorkerAmount]
                        if isProfile:
                            infoLine.append(setProfileData(record, {}))
                        infoLine.append(actionUet)
                        personData[currentKey] = infoLine
                        existsData[personName] = personData
                    else:
                        existsValue = personData.get(currentKey, None)
                        if not existsValue:
                            actionAmount = 1
                            resultActionIdList.append(actionId)
                            serviceCodeList = serviceCode
                            infoLine = [serviceCodeList, actionAmount, amount, uetDoctorAmount, uetAverageMedWorkerAmount]
                            if isProfile:
                                infoLine.append(setProfileData(record, {}))
                            infoLine.append(actionUet)
                            personData[currentKey] = infoLine
                            existsData[personName] = personData
                        else:
                            if serviceCode and serviceCode not in existsValue[0]:
                                existsValue[0] += u', ' + serviceCode
                            if actionId not in resultActionIdList:
                                existsValue[1] += 1
                                existsValue[2] += amount
                            existsValue[3] += uetDoctorAmount
                            existsValue[4] += uetAverageMedWorkerAmount
                            if isProfile:
                                profileData = setProfileData(record, existsValue[5])
                                existsValue[5] = profileData
                                existsValue[6] += actionUet
                            else:
                                existsValue[5] += actionUet
                            personData[currentKey] = existsValue
                            existsData[personName] = personData
                    reportData[orgStructureName] = existsData
            else:
                if not existsData:
                    existsData = {}
                    actionAmount = 1
                    resultActionIdList.append(actionId)
                    serviceCodeList = serviceCode
                    infoLine = [serviceCodeList, actionAmount, amount, uetDoctorAmount, uetAverageMedWorkerAmount]
                    if isProfile:
                        infoLine.append(setProfileData(record, {}))
                    infoLine.append(actionUet)
                    existsData[currentKey] = infoLine
                    reportData[orgStructureName] = existsData
                else:
                    existsValue = existsData.get(currentKey, None)
                    if not existsValue:
                        actionAmount = 1
                        resultActionIdList.append(actionId)
                        serviceCodeList = serviceCode
                        infoLine = [serviceCodeList, actionAmount, amount, uetDoctorAmount, uetAverageMedWorkerAmount]
                        if isProfile:
                            infoLine.append(setProfileData(record, {}))
                        infoLine.append(actionUet)
                        existsData[currentKey] = infoLine
                    else:
                        if serviceCode and serviceCode not in existsValue[0]:
                            existsValue[0] += u', ' + serviceCode
                        if actionId not in resultActionIdList:
                            existsValue[1] += 1
                            existsValue[2] += amount
                        existsValue[3] += uetDoctorAmount
                        existsValue[4] += uetAverageMedWorkerAmount
                        if isProfile:
                            profileData = setProfileData(record, existsValue[5])
                            existsValue[5] = profileData
                            existsValue[6] += actionUet
                        else:
                            existsValue[5] += actionUet
                        existsData[currentKey] = existsValue
                    reportData[orgStructureName] = existsData

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        tableColumns = [
            ( '5%', [u'№ п/п'], CReportBase.AlignRight),
            ( '20%', [u'Наименование типа действия'], CReportBase.AlignLeft),
            ( '12.5%', [u'Код типа действия'], CReportBase.AlignLeft),
            ( '12.5%', [u'Код профиля'], CReportBase.AlignLeft),
            ( '8%' if isProfile else '10%', [u'Количество действий'], CReportBase.AlignRight),
            ( '8%' if isProfile else '10%', [u'Количество'], CReportBase.AlignRight),
            ( '8%' if isProfile else '10%', [u'УЕТ врача'], CReportBase.AlignRight),
            ( '8%' if isProfile else '10%', [u'УЕТ ср.мед.персонала'], CReportBase.AlignRight),
            ( '8%' if isProfile else '10%', [u'УЕТ'], CReportBase.AlignRight)
        ]
        if isProfile:
            tableColumns.insert(6, ( '8%', [u'Количество услуг'], CReportBase.AlignRight))
        table = createTable(cursor, tableColumns)
        headerCount = 1
        headerList  = []
        colAISList = {0:1, 1:3, 2:6, 3:7, 4:8, 5:9}
        if detailPerson:
            orgStructureList = reportData.keys()
            orgStructureList.sort()
            resume = [0]*6 if isProfile else [0]*5
            for orgStructure in orgStructureList:
                orgStructureResult = [0]*6 if isProfile else [0]*5
                i = table.addRow()
                currentOrgStructureRow = i
                table.setText(i, 1, orgStructure)
                headerList.append(i)
                persons = reportData.get(orgStructure, {})
                personsKeys = persons.keys()
                personsKeys.sort()
                for personKey in personsKeys:
                    personResult = [0]*6 if isProfile else [0]*5
                    i = table.addRow()
                    currentPersonRow = i
                    table.setText(i, 1, personKey)
                    headerList.append(i)
                    existsData = persons.get(personKey, {})
                    existsDataKeys = existsData.keys()
                    existsDataKeys.sort()
                    for existsDataKey in existsDataKeys:
                        if isProfile:
                            actionTypeResult = [0]
                        i = table.addRow()
                        table.setText(i, 0, headerCount)
                        headerCount += 1
                        column = 1
                        for key in existsDataKey:
                            table.setText(i, column, key)
                            column += 1
                        existsValues = existsData.get(existsDataKey, [])
                        for col, existsValue in enumerate(existsValues):
                            if (isProfile and col not in [0, 5]) or (not isProfile and col not in [0,]):
                                colWriteRes = col if isProfile and col in [3, 4] else col-1
                                colWrite = col+4 if isProfile and col in [3, 4] else col + 3
                                orgStructureResult[colWriteRes] += existsValue
                                personResult[colWriteRes] += existsValue
                                resume[colWriteRes] += existsValue
                                table.setText(i, colWrite, existsValue)
                            elif col == 0:
                                table.setText(i, col + 3, existsValue)
                            elif col == 5 and isProfile:
                                for valAISs in existsValue.values():
                                    rowAIS = table.addRow()
                                    for colAIS, valAIS in enumerate(valAISs):
                                        table.setText(rowAIS, colAISList[colAIS], valAIS)
                                        if colAIS == 2:
                                            orgStructureResult[col] += valAIS
                                            personResult[colAIS] += valAIS
                                            actionTypeResult[0] += valAIS
                                            resume[colAIS] += valAIS
                        if isProfile:
                            table.setText(i, 6, actionTypeResult[0])
                    for column, val in enumerate(personResult):
                        table.setText(currentPersonRow, column+4, val)
                for column, val in enumerate(orgStructureResult):
                    table.setText(currentOrgStructureRow, column+4, val)
            for headerRow in headerList:
                table.mergeCells(headerRow, 0, 1, 3)
        else:
            orgStructureList = reportData.keys()
            orgStructureList.sort()
            resume = [0]*6 if isProfile else [0]*5
            for orgStructure in orgStructureList:
                orgStructureResult = [0]*6 if isProfile else [0]*5
                i = table.addRow()
                currentOrgStructureRow = i
                table.setText(i, 1, orgStructure)
                headerList.append(i)
                existsData = reportData.get(orgStructure, {})
                existsDataKeys = existsData.keys()
                existsDataKeys.sort()
                for existsDataKey in existsDataKeys:
                    if isProfile:
                        actionTypeResult = [0]
                    i = table.addRow()
                    table.setText(i, 0, headerCount)
                    headerCount += 1
                    column = 1
                    for key in existsDataKey:
                        table.setText(i, column, key)
                        column += 1
                    existsValues = existsData.get(existsDataKey, [])
                    for col, existsValue in enumerate(existsValues):
                        if (isProfile and col not in [0, 5]) or (not isProfile and col not in [0,]):
                            colWriteRes = col if isProfile and col in [3, 4] else col-1
                            colWrite = col+4 if isProfile and col in [3, 4] else col + 3
                            orgStructureResult[colWriteRes] += existsValue
                            resume[colWriteRes] += existsValue
                            table.setText(i, colWrite, existsValue)
                        elif col == 0:
                            table.setText(i, col + 3, existsValue)
                        elif col == 5 and isProfile:
                            for valAISs in existsValue.values():
                                rowAIS = table.addRow()
                                for colAIS, valAIS in enumerate(valAISs):
                                    table.setText(rowAIS, colAISList[colAIS], valAIS)
                                    if colAIS == 2:
                                        orgStructureResult[colAIS] += valAIS
                                        actionTypeResult[0] += valAIS
                                        resume[colAIS] += valAIS
                    if isProfile:
                        table.setText(i, 6, actionTypeResult[0])
                for column, val in enumerate(orgStructureResult):
                    table.setText(currentOrgStructureRow, column+4, val)
            for headerRow in headerList:
                table.mergeCells(headerRow, 0, 1, 3)
        i = table.addRow()
        table.setText(i, 1, u'Итого')
        for column, val in enumerate(resume):
            table.setText(i, column+4, val)
        return doc
