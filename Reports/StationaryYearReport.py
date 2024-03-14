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

from PyQt4               import QtGui
from PyQt4.QtCore        import QDate, QTime, QDateTime
from Reports.Report      import CReport
from Reports.ReportBase  import CReportBase, createTable
from Reports.ReportView  import CPageFormat
from library.Utils       import forceInt, forceString
from library.DialogBase  import CDialogBase
from copy                import deepcopy

from Ui_StationaryYearReportSetupDialog import Ui_StationaryYearReportSetupDialog


RECEIVED_STATE_NOT_SET = 0
RECEIVED_STATE_LIGHT = 1
RECEIVED_STATE_MIDDLE = 2
RECEIVED_STATE_HEAVY = 3

RECEIVED_ORDER_NOT_SET = 0
RECEIVED_ORDER_PLANNED = 1
RECEIVED_ORDER_URGENT = 2

COMPILCATIONS_NOT_SET = 0
COMPILCATIONS_YES = 1
COMPILCATIONS_NO = 2


def selectData(params, orgStructureId):
    basedict = {'eventCount' : 0,      # Кол-во всех событий, из них:
                'plannedHospital' : 0, # Плановая госпитализация
                'urgentHospital' : 0,  # Экстренная госпитализация
                'liveInSPB' : 0,       # Проживают в СПб
                'liveVillage' : 0,     # Сельские
                'notLiveInSPB': 0,     # Не проживают в СПб (иногородние)
                'age-1' : 0,           # Возраст до года
                'age1-3' : 0,          # Возраст от 1 до 3
                'age4-6' : 0,          # Возраст от 4 до 6
                'age7-14' : 0,         # Возраст от 7 до 14
                'age14+' : 0,          # Старше 14
                'recovery' : 0,        # Выздоровление
                'better': 0,           # Улучшение
                'nochange' : 0,        # Без изменений
                'worse' : 0,           # Ухудшение
                'death' : 0,           # Смерть
                'finOMC' : 0,          # Финансирование ОМС
                'finDMC' : 0,          # Финансирование ДМС
                'finPay' : 0,          # Платно
                'finTarget' : 0,       # Целевые
                'finBudget' : 0,       # Бюджет
                'finOther' : 0,        # Прочие источники финансирования
                'state' : {},          # Состояние при поступлении {'name' : count}
                'nosology' : {},       # Диагнозы по нозологии  {'name' : count}
                'performedOper' : {}   # Проведенные операции  {'name' : count}
                }

    reportData = {}  # {orgName: [year1, year2, year3]}

    db = QtGui.qApp.db
    begyear = QDateTime(QDate(params['reportYear']-2, 1, 1), QTime(0,0,0))
    endyear = QDateTime(QDate(params['reportYear'], 12, 31), QTime(23,59,59))
    orgId = QtGui.qApp.currentOrgId()

    tableEvent              = db.table('Event')
    tableAction             = db.table('Action')
    tableClient             = db.table('Client')
    tablePerson             = db.table('Person')
    tableAddress            = db.table('Address')
    tableClientAddress      = db.table('ClientAddress')
    tableAddressHouse       = db.table('AddressHouse')
    tableDiagnosis          = db.table('Diagnosis')
    tableDiagnostic         = db.table('Diagnostic')
    tableDiagnosisType      = db.table('rbDiagnosisType')
    tableDiagnosticResult   = db.table('rbDiagnosticResult')
    tableActionType         = db.table('ActionType')
    tableFinance            = db.table('rbFinance')
    tableContract           = db.table('Contract')
    tableActionProperty     = db.table('ActionProperty')
    tablePropertyString     = db.table('ActionProperty_String')
    tableActionPropertyType = db.table('ActionPropertyType')
    tableOrgStructure       = db.table('OrgStructure')


    defaultQueryTable = tableEvent
    defaultQueryTable = defaultQueryTable.innerJoin(tableClient, tableEvent['client_id'].eq(tableClient['id']))
    defaultQueryTable = defaultQueryTable.innerJoin(tablePerson, tableEvent['execPerson_id'].eq(tablePerson['id']))
    defaultQueryTable = defaultQueryTable.innerJoin(tableOrgStructure, tablePerson['orgStructure_id'].eq(tableOrgStructure['id']))
    if params['MKBFilter']:
        defaultQueryTable = defaultQueryTable.innerJoin(tableDiagnostic, tableDiagnostic['event_id'].eq(tableEvent['id']))
        defaultQueryTable = defaultQueryTable.innerJoin(tableDiagnosis, tableDiagnostic['diagnosis_id'].eq(tableDiagnosis['id']))
        defaultQueryTable = defaultQueryTable.innerJoin(tableDiagnosisType, tableDiagnosis['diagnosisType_id'].eq(tableDiagnosisType['id']))
    if not params['operationId'] is None:
        defaultQueryTable = defaultQueryTable.innerJoin(tableAction, tableAction['event_id'].eq(tableEvent['id']))
        defaultQueryTable = defaultQueryTable.innerJoin(tableActionType, tableAction['actionType_id'].eq(tableActionType['id']))
    if params['complications'] != COMPILCATIONS_NOT_SET:
        defaultQueryTable = defaultQueryTable.innerJoin(tableAction, tableAction['event_id'].eq(tableEvent['id']))
        defaultQueryTable = defaultQueryTable.innerJoin(tableActionType, tableAction['actionType_id'].eq(tableActionType['id']))
        defaultQueryTable = defaultQueryTable.innerJoin(tableActionProperty, tableActionProperty['action_id'].eq(tableAction['id']))
        defaultQueryTable = defaultQueryTable.innerJoin(tableActionPropertyType, tableActionProperty['type_id'].eq(tableActionPropertyType['id']))
        defaultQueryTable = defaultQueryTable.innerJoin(tablePropertyString, tableActionProperty['id'].eq(tablePropertyString['id']))

    defaultCond = [ tableEvent['deleted'].eq(0),
                    tableClient['deleted'].eq(0),
                    tableEvent['execDate'].ge(begyear),
                    tableEvent['execDate'].le(endyear),
                    tablePerson['org_id'].eq(orgId),
                   ]
    if params['MKBFilter']:
        defaultCond.append(tableDiagnosis['MKB'].ge(params['MKBFrom']))
        defaultCond.append(tableDiagnosis['MKB'].le(params['MKBTo']))
        defaultCond.append(tableDiagnosisType['code'].eq(1))

    if not params['orgStructureId'] is None:
        defaultCond.append(tableOrgStructure['id'].inlist(orgStructureId))

    if not params['operationId'] is None:
        defaultCond.append(tableActionType['id'].eq(params['operationId']))
        defaultCond.append(tableAction['deleted'].eq(0))
        defaultCond.append(tableActionType['deleted'].eq(0))

    if params['complications'] != COMPILCATIONS_NOT_SET:
        defaultCond.append(tableAction['deleted'].eq(0))
        defaultCond.append(tableActionType['deleted'].eq(0))
        defaultCond.append(tableActionPropertyType['name'].eq(u'осложнения'))
        defaultCond.append(tableActionType['serviceType'].eq(4))
        if params['complications'] == COMPILCATIONS_YES:
            defaultCond.append(tablePropertyString['value'].ne(''))
            defaultCond.append(tablePropertyString['value'].notlike(u'нет%'))

    # Должно быть последней строкой
    defaultCond.append('age(Client.birthDate, Event.setDate) BETWEEN %d AND %d' % (params['ageFrom'], params['ageTo']))

    defaultCols = [ 'COUNT(DISTINCT Event.id) AS `eventCount`',
                    'YEAR(Event.execDate) AS `execYear`',
                    'OrgStructure.name AS `orgStructureName`'
                  ]

    defaultGroup = ['YEAR(Event.execDate)', tableOrgStructure['id'].name()]
    defaultOrder = 'NULL'


    # Всего обслуживаний
    query = db.query(db.selectStmtGroupBy(defaultQueryTable, defaultCols, defaultCond, defaultGroup, defaultOrder))
    while query.next():
        record = query.record()
        orgName = forceString(record.value('orgStructureName'))
        year = abs(forceInt(record.value('execYear')) - params['reportYear'])
        if not reportData.has_key(orgName):
            reportData[orgName] = [deepcopy(basedict) for _ in xrange(3)]
        reportData[orgName][year]['eventCount'] = forceInt(record.value('eventCount'))


    # Порядок поступления
    for hospitalKey, hospitalOrder in (('plannedHospital', [1,4,5]),
                                       ('urgentHospital', [2,3,6])):
        cond = defaultCond + [ tableEvent['order'].inlist(hospitalOrder) ]
        query = db.query(db.selectStmtGroupBy(defaultQueryTable, defaultCols, cond, defaultGroup, defaultOrder))
        while query.next():
            record = query.record()
            orgName = forceString(record.value('orgStructureName'))
            year = abs(forceInt(record.value('execYear')) - params['reportYear'])
            if not reportData.has_key(orgName):
                reportData[orgName] = [deepcopy(basedict) for _ in xrange(3)]
            reportData[orgName][year][hospitalKey] = forceInt(record.value('eventCount'))


    # Источники финансирования
    financeQueryTable = db.innerJoin(defaultQueryTable, tableContract, tableEvent['contract_id'].eq(tableContract['id']))
    financeQueryTable = financeQueryTable.innerJoin(tableFinance, tableContract['finance_id'].eq(tableFinance['id']))
    for financeKey, financeCode in (('finBudget', 1),
                                    ('finOMC', 2),
                                    ('finDMC', 3),
                                    ('finPay', 4),
                                    ('finTarget', 5)):
        cond = defaultCond + [ tableFinance['code'].eq(financeCode) ]
        query = db.query(db.selectStmtGroupBy(financeQueryTable, defaultCols, cond, defaultGroup, defaultOrder))
        while query.next():
            record = query.record()
            orgName = forceString(record.value('orgStructureName'))
            year = abs(forceInt(record.value('execYear')) - params['reportYear'])
            if not reportData.has_key(orgName):
                reportData[orgName] = [deepcopy(basedict) for _ in xrange(3)]
            reportData[orgName][year][financeKey] = forceInt(record.value('eventCount'))
    for orgName in reportData.keys():
        for year in xrange(3):
            data = reportData[orgName][year]
            data['finOther'] = data['eventCount'] - (data['finBudget'] + data['finOMC'] + data['finDMC'] + data['finPay'] + data['finTarget'])
            if data['finOther'] < 0:
                data['finOther'] = 0


    # Возрастные группы
    for ageKey, ageFrom, ageTo in (('age-1', 0,0),
                                   ('age1-3', 1,3),
                                   ('age4-6', 4,6),
                                   ('age7-14', 7,14),
                                   ('age14+', 14,150)):
        cond = defaultCond[:-1]
        cond.append('age(Client.birthDate, Event.setDate) BETWEEN %d AND %d' % (ageFrom, ageTo))
        query = db.query(db.selectStmtGroupBy(defaultQueryTable, defaultCols, cond, defaultGroup, defaultOrder))
        while query.next():
            record = query.record()
            orgName = forceString(record.value('orgStructureName'))
            year = abs(forceInt(record.value('execYear')) - params['reportYear'])
            if not reportData.has_key(orgName):
                reportData[orgName] = [deepcopy(basedict) for _ in xrange(3)]
            reportData[orgName][year][ageKey] = forceInt(record.value('eventCount'))

    # Исходы лечения
    if not params['MKBFilter']:
        resultQueryTable = db.innerJoin(defaultQueryTable, tableDiagnostic, tableEvent['id'].eq(tableDiagnostic['event_id']))
        resultQueryTable = resultQueryTable.innerJoin(tableDiagnosticResult, tableDiagnostic['result_id'].eq(tableDiagnosticResult['id']))
    else:
        resultQueryTable = db.innerJoin(defaultQueryTable, tableDiagnostic, tableEvent['id'].eq(tableDiagnostic['event_id']))
    for resultKey, resultParam in (('better', u'%улучшение%'),
                                   ('worse', u'%ухудшение%'),
                                   ('recovery', u'%выздоровление%'),
                                   ('death', u'%смерть%')):
        cond = defaultCond + [ tableDiagnosticResult['name'].like(resultParam) ]
        query = db.query(db.selectStmtGroupBy(resultQueryTable, defaultCols, cond, defaultGroup, defaultOrder))
        while query.next():
            record = query.record()
            orgName = forceString(record.value('orgStructureName'))
            year = abs(forceInt(record.value('execYear')) - params['reportYear'])
            if not reportData.has_key(orgName):
                reportData[orgName] = [deepcopy(basedict) for _ in xrange(3)]
            reportData[orgName][year][resultKey] = forceInt(record.value('eventCount'))


    # Места проживания
    liveQueryTable = db.innerJoin(defaultQueryTable, tableClientAddress, tableClientAddress['client_id'].eq(tableClient['id']))
    liveQueryTable = liveQueryTable.innerJoin(tableAddress, tableClientAddress['address_id'].eq(tableAddress['id']))
    liveQueryTable = liveQueryTable.innerJoin(tableAddressHouse, tableAddress['house_id'].eq(tableAddressHouse['id']))

    for liveKey, liveCond in (('liveInSPB', "AddressHouse.KLADRCode = '7800000000000'"),
                              ('liveVillage', "isAddressVillager(Address.id) = 1")):
        cond = defaultCond + [ liveCond ]
        query = db.query(db.selectStmtGroupBy(liveQueryTable, defaultCols, cond, defaultGroup, defaultOrder))
        while query.next():
            record = query.record()
            orgName = forceString(record.value('orgStructureName'))
            year = abs(forceInt(record.value('execYear')) - params['reportYear'])
            if not reportData.has_key(orgName):
                reportData[orgName] = [deepcopy(basedict) for _ in xrange(3)]
            reportData[orgName][year][liveKey] = forceInt(record.value('eventCount'))
    for orgName in reportData.keys():
        for year in xrange(3):
            data = reportData[orgName][year]
            data['notLiveInSPB'] = data['eventCount'] - (data['liveInSPB'] + data['liveVillage'])
            if data['notLiveInSPB'] < 0:
                data['notLiveInSPB'] = 0


    # Состояние при поступлении
    if (params['operationId'] is None) and (params['complications'] == COMPILCATIONS_NOT_SET):
        receivedQueryTable = db.innerJoin(defaultQueryTable, tableAction, tableAction['event_id'].eq(tableEvent['id']))
        receivedQueryTable = receivedQueryTable.innerJoin(tableActionType, tableAction['actionType_id'].eq(tableActionType['id']))
        receivedQueryTable = receivedQueryTable.innerJoin(tableActionProperty, tableActionProperty['action_id'].eq(tableAction['id']))
        receivedQueryTable = receivedQueryTable.innerJoin(tableActionPropertyType, tableActionProperty['type_id'].eq(tableActionPropertyType['id']))
        receivedQueryTable = receivedQueryTable.innerJoin(tablePropertyString, tableActionProperty['id'].eq(tablePropertyString['id']))
    elif (not params['operationId'] is None) and (params['complications'] == COMPILCATIONS_NOT_SET):
        receivedQueryTable = db.innerJoin(defaultQueryTable, tableActionProperty, tableActionProperty['action_id'].eq(tableAction['id']))
        receivedQueryTable = receivedQueryTable.innerJoin(tableActionPropertyType, tableActionProperty['type_id'].eq(tableActionPropertyType['id']))
        receivedQueryTable = receivedQueryTable.innerJoin(tablePropertyString, tableActionProperty['id'].eq(tablePropertyString['id']))
    else:
        receivedQueryTable = defaultQueryTable

    receivedCols = defaultCols + [ tablePropertyString['value'].alias('state') ]
    receivedCond = defaultCond + [ tableActionPropertyType['name'].eq(u'Состояние при поступлении'), tableActionProperty['deleted'].eq(0) ]
    receivedGroup = defaultGroup + [ tablePropertyString['value'].name() ]
    if params['received'] == RECEIVED_STATE_LIGHT:
        receivedCond.append(tablePropertyString['value'].like(u'л:%'))
    if params['received'] == RECEIVED_STATE_MIDDLE:
        receivedCond.append(tablePropertyString['value'].like(u'с:%'))
    if params['received'] == RECEIVED_STATE_HEAVY:
        receivedCond.append(tablePropertyString['value'].like(u'т:%'))

    query = db.query(db.selectStmtGroupBy(receivedQueryTable, receivedCols, receivedCond, receivedGroup, defaultOrder))
    while query.next():
        record = query.record()
        orgName = forceString(record.value('orgStructureName'))
        year = abs(forceInt(record.value('execYear')) - params['reportYear'])
        stateName = forceString(record.value('state'))
        if not reportData.has_key(orgName):
            reportData[orgName] = [deepcopy(basedict) for _ in xrange(3)]
        reportData[orgName][year]['state'][stateName] = forceInt(record.value('eventCount'))


    # По нозологии
    if not params['MKBFilter']:
        nosologyQueryTable = db.innerJoin(defaultQueryTable, tableDiagnostic, tableDiagnostic['event_id'].eq(tableEvent['id']))
        nosologyQueryTable = nosologyQueryTable.innerJoin(tableDiagnosis, tableDiagnostic['diagnosis_id'].eq(tableDiagnosis['id']))
        nosologyQueryTable = nosologyQueryTable.innerJoin(tableDiagnosisType, tableDiagnosis['diagnosisType_id'].eq(tableDiagnosisType['id']))
    else:
        nosologyQueryTable = defaultQueryTable

    nosologyCols = defaultCols + [ tableDiagnosis['MKB'] ]
    nosologyGroup = defaultGroup + [ tableDiagnosis['MKB'].name() ]
    query = db.query(db.selectStmtGroupBy(nosologyQueryTable, nosologyCols, defaultCond, nosologyGroup, defaultOrder))
    while query.next():
        record = query.record()
        orgName = forceString(record.value('orgStructureName'))
        year = abs(forceInt(record.value('execYear')) - params['reportYear'])
        if not reportData.has_key(orgName):
            reportData[orgName] = [deepcopy(basedict) for _ in xrange(3)]
        mkb = forceString(record.value('MKB'))
        reportData[orgName][year]['nosology'][mkb] = forceInt(record.value('eventCount'))


    # Проведенные опрерации
    if (params['operationId'] is None) and (params['complications'] == COMPILCATIONS_NOT_SET):
        operationsQueryTable = db.innerJoin(defaultQueryTable, tableAction, tableAction['event_id'].eq(tableEvent['id']))
        operationsQueryTable = operationsQueryTable.innerJoin(tableActionType, tableAction['actionType_id'].eq(tableActionType['id']))
    else:
        operationsQueryTable = defaultQueryTable

    operationsCols = [ tableActionType['name'],
                       tableActionType['code'],
                       tableOrgStructure['name'].alias('orgStructureName'),
                       'YEAR(Event.execDate) AS `execYear`',
                       'COUNT(DISTINCT Action.id) AS `operationsCount`'
                     ]
    operationsCond = defaultCond + [ tableActionType['serviceType'].eq(4) ]
    operationsGroup = defaultGroup + [ tableActionType['code'].name() ]
    query = db.query(db.selectStmtGroupBy(operationsQueryTable, operationsCols, operationsCond, operationsGroup, defaultOrder))
    while query.next():
        record = query.record()
        orgName = forceString(record.value('orgStructureName'))
        year = abs(forceInt(record.value('execYear')) - params['reportYear'])
        if not reportData.has_key(orgName):
            reportData[orgName] = [deepcopy(basedict) for _ in xrange(3)]
        operationName = u'%s - %s' % (forceString(record.value('code')), forceString(record.value('name')))
        reportData[orgName][year]['performedOper'][operationName] = forceInt(record.value('operationsCount'))

    return reportData




class CStationaryYearReport(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.stationaryYearReportSetupDialog = None
        self.setTitle(u'Годовой отчет заведующего отделения')

    def getCurrentOrgStructureIdList(self):
        cmbOrgStruct = self.stationaryYearReportSetupDialog.cmbOrgStructure
        treeIndex = cmbOrgStruct._model.index(cmbOrgStruct.currentIndex(), 0, cmbOrgStruct.rootModelIndex())
        treeItem = treeIndex.internalPointer() if treeIndex.isValid() else None
        return treeItem.getItemIdList() if treeItem else []

    def getSetupDialog(self, parent):
        result = CStationaryYearReportSetupDialog(parent)
        self.stationaryYearReportSetupDialog = result
        result.setWindowTitle(self.title())
        result.setObjectName(self.title())
        return result

    def build(self, params):
        reportYear = params['reportYear']
        yearValues = None

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)

        alignRight = CReportBase.AlignRight
        alignLeft = CReportBase.AlignLeft
        alignCenter = CReportBase.AlignCenter

        cursor.mergeBlockFormat(alignCenter)
        cursor.insertBlock()
        cursor.insertText(u'Годовой отчет заведующего отделения')
        cursor.insertBlock()
        cursor.insertText(u'Характеристика стационарных больных, исходы лечения и нозологии заболеваний')

        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        cols = [('15%', [u'Подразделение', u''], alignLeft),
                ('25%', [u'Характеристика', u''], alignLeft),
                ('10%', [u'%d год' % (reportYear), u'Кол-во'], alignLeft),
                ('10%', [u'', u'% от общего кол-ва'], alignLeft),
                ('10%', [u'%d год' % (reportYear-1), u'Кол-во'], alignLeft),
                ('10%', [u'', u'% от общего кол-ва'], alignLeft),
                ('10%', [u'%d год' % (reportYear-2), u'Кол-во'], alignLeft),
                ('10%', [u'', u'% от общего кол-ва'], alignLeft)]
        table = createTable(cursor, cols)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 1, 2)
        table.mergeCells(0, 4, 1, 2)
        table.mergeCells(0, 6, 1, 2)

        row = table.addRow()
        table.setText(row, 0, u'Стационар круглосуточный', blockFormat=alignCenter)
        table.mergeCells(row, 0, 1, 8)


        # Объединить словари в один, перенеся значения в список
        # {name : value1} + {name: value2} + ... == {name: [value1, value2, ...]}
        def collectValues(dictA, dictB, dictC):
            for i in dictA.keys():
                dictA[i] = [dictA[i], dictB.get(i, 0), dictC.get(i, 0)]
            for i in dictB.keys():
                if not dictA.has_key(i):
                    dictA[i] = [0, dictB[i], dictC.get(i, 0)]
            for i in dictC.keys():
                if not dictA.has_key(i):
                    dictA[i] = [0, 0, dictC[i]]


        # Высчитать процентное соотношение yearValues[i][name] от yearValues[i]['eventCount']
        def percentRaito(name, i):
            value = float(yearValues[i]['eventCount'])
            piece = yearValues[i][name]
            return '100%' if value == 0 else '%g%%' % round((piece / value) * 100.0, 1)


        # Объединяет ячейки "Кол-во" и "% от общего числа"
        def mergeCountAndPercentCells(tab, row):
            tab.mergeCells(row, 2, 1, 2)
            tab.mergeCells(row, 4, 1, 2)
            tab.mergeCells(row, 6, 1, 2)


        # Добавляет строку в таблицу и заполняет параметрами из словаря (за 3 года)
        def addRowWithParams(table, rowName, yearValueKey=None):
            row = table.addRow()
            if not yearValueKey is None:
                table.setText(row, 1, '    ' + rowName)
                for i in xrange(3):
                    table.setText(row, (i+1)*2,   yearValues[i][yearValueKey],   blockFormat=alignRight)
                    table.setText(row, (i+1)*2+1, percentRaito(yearValueKey, i), blockFormat=alignRight)
            else:
                table.setText(row, 1, rowName)
                mergeCountAndPercentCells(table, row)
            return row

        reportData = selectData(params, self.getCurrentOrgStructureIdList())

        for orgStructureName,yearValues in reportData.items():
            begRow = addRowWithParams(table, u'Характер госпитализаци:')
            table.setText(begRow, 0, orgStructureName)
            addRowWithParams(table, u'Плановые', 'plannedHospital')
            addRowWithParams(table, u'Экстренные', 'urgentHospital')

            addRowWithParams(table, u'Место проживания:')
            addRowWithParams(table, u'СПб', 'liveInSPB')
            addRowWithParams(table, u'сельские', 'liveVillage')
            addRowWithParams(table, u'иногородние', 'notLiveInSPB')

            addRowWithParams(table, u'Возрастные группы:')
            addRowWithParams(table, u'до 1 года', 'age-1')
            addRowWithParams(table, u'1-3 лет', 'age1-3')
            addRowWithParams(table, u'4-6 лет', 'age4-6')
            addRowWithParams(table, u'7-14 лет', 'age7-14')
            addRowWithParams(table, u'старше 14 лет', 'age14+')

            row = addRowWithParams(table, u'Состояние при поступлении:')
            collectValues(yearValues[0]['state'], yearValues[1]['state'], yearValues[2]['state'])
            for name in sorted(yearValues[0]['state'].keys()):
                if name == '':  # Не вставлять пустую строку
                    continue
                counts = yearValues[0]['state'][name]
                row = table.addRow()
                table.setText(row, 1, '    ' + name)
                table.setText(row, 2, counts[0], blockFormat=alignRight)
                table.setText(row, 4, counts[1], blockFormat=alignRight)
                table.setText(row, 6, counts[2], blockFormat=alignRight)
                mergeCountAndPercentCells(table, row)

            addRowWithParams(table, u'Исход лечения:')
            addRowWithParams(table, u'выздоровление', 'recovery')
            addRowWithParams(table, u'улучшение', 'better')
            addRowWithParams(table, u'без перемен', 'nochange')
            addRowWithParams(table, u'ухудшение', 'worse')
            addRowWithParams(table, u'Из них умерло', 'death')

            addRowWithParams(table, u'Источники финансирования:')
            addRowWithParams(table, u'ОМС', 'finOMC')
            addRowWithParams(table, u'ДМС', 'finDMC')
            addRowWithParams(table, u'Платно', 'finPay')
            addRowWithParams(table, u'Целевые', 'finTarget')
            addRowWithParams(table, u'Бюджет', 'finBudget')
            addRowWithParams(table, u'Прочие', 'finOther')

            row = addRowWithParams(table, u'По нозологии:')
            collectValues(yearValues[0]['nosology'], yearValues[1]['nosology'], yearValues[2]['nosology'])
            for name in sorted(yearValues[0]['nosology'].keys()):
                if name == '':  # Не вставлять пустую строку
                    continue
                counts = yearValues[0]['nosology'][name]
                row = table.addRow()
                table.setText(row, 1, '    ' + name)
                table.setText(row, 2, counts[0], blockFormat=alignRight)
                table.setText(row, 4, counts[1], blockFormat=alignRight)
                table.setText(row, 6, counts[2], blockFormat=alignRight)
                mergeCountAndPercentCells(table, row)

            row = addRowWithParams(table, u'Проведенные операции:')
            collectValues(yearValues[0]['performedOper'], yearValues[1]['performedOper'], yearValues[2]['performedOper'])
            for name in sorted(yearValues[0]['performedOper'].keys()):
                if name == ' - ':  # Не вставлять пустую строку
                    continue
                counts = yearValues[0]['performedOper'][name]
                row = table.addRow()
                table.setText(row, 1, '    ' + name)
                table.setText(row, 2, counts[0], blockFormat=alignRight)
                table.setText(row, 4, counts[1], blockFormat=alignRight)
                table.setText(row, 6, counts[2], blockFormat=alignRight)
                mergeCountAndPercentCells(table, row)

            row = addRowWithParams(table, u'Итого за отделение: ')
            for i in xrange(3):
                table.setText(row, (i+1)*2, yearValues[i]['eventCount'], blockFormat=alignRight)
                table.mergeCells(row, (i+1)*2, 1, 2)

            table.mergeCells(begRow, 0, row - begRow + 1, 1)

        return doc



class CStationaryYearReportSetupDialog(CDialogBase, Ui_StationaryYearReportSetupDialog):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())
        self.cmbOperations.setTable('ActionType', filter='serviceType=4')

    def setParams(self, params):
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.edtReportYear.setValue(params.get('reportYear', QDate.currentDate().year()))
        self.cmbReceivedCnd.setCurrentIndex(params.get('received', RECEIVED_STATE_NOT_SET))
        self.cmbOrder.setCurrentIndex(params.get('order', RECEIVED_ORDER_NOT_SET))
        self.edtAgeFrom.setValue(params.get('ageFrom', 0))
        self.edtAgeTo.setValue(params.get('ageTo', 150))
        self.chkEnableMKB.setChecked(params.get('MKBFilter', False))
        self.edtMKBFrom.setText(params.get('MKBFrom', 'A00.00'))
        self.edtMKBTo.setText(params.get('MKBTo', 'Z99.99'))
        self.cmbOperations.setValue(params.get('operationId', None))
        self.cmbComplications.setCurrentIndex(params.get('complications', COMPILCATIONS_NOT_SET))

    def params(self):
        result = {}
        result['reportYear'] = self.edtReportYear.value()
        result['orgStructureId'] = self.cmbOrgStructure.value()
        result['received'] = self.cmbReceivedCnd.currentIndex()
        result['order'] = self.cmbOrder.currentIndex()
        result['ageFrom'] = self.edtAgeFrom.value()
        result['ageTo'] = self.edtAgeTo.value()
        result['MKBFilter'] = self.chkEnableMKB.isChecked()
        result['MKBFrom'] = self.edtMKBFrom.text()
        result['MKBTo'] = self.edtMKBTo.text()
        result['operationId'] = self.cmbOperations.value()
        result['complications'] = self.cmbComplications.currentIndex()
        return result

