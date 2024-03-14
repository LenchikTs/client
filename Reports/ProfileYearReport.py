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

from PyQt4                import QtGui
from PyQt4.QtCore         import QDate
from Reports.Report       import CReport
from Reports.ReportBase   import CReportBase, createTable
from Reports.ReportView   import CPageFormat
from library.Utils        import forceInt, forceString
from library.DialogBase   import CDialogBase

from Ui_ProfileYearReportSetupDialog import Ui_ProfileYearReportSetupDialog


RECEIVED_STATE_NOT_SET = 0
RECEIVED_STATE_LIGHT = 1
RECEIVED_STATE_MIDDLE = 2
RECEIVED_STATE_HEAVY = 3

RECEIVED_ORDER_NOT_SET = 0
RECEIVED_ORDER_PLANNED = 1
RECEIVED_ORDER_URGENT = 2


def getStmt(params, bedSheduleCode):

    if params['received'] == RECEIVED_STATE_LIGHT:
        receivedStateCond = u"AND ActionProperty_String.value LIKE 'л:%'"
    elif params['received'] == RECEIVED_STATE_MIDDLE:
        receivedStateCond = u"AND ActionProperty_String.value LIKE 'с:%'"
    elif params['received'] == RECEIVED_STATE_HEAVY:
        receivedStateCond = u"AND ActionProperty_String.value LIKE 'т:%'"
    else:
        receivedStateCond = ''


    if params['order'] == RECEIVED_ORDER_PLANNED:
        eventOrderCond = 'AND Event.order IN (1,4,5)'
    elif params['order'] == RECEIVED_ORDER_URGENT:
        eventOrderCond = 'AND Event.order IN (2,3,6)'
    else:
        eventOrderCond = ''


    return u"""
SELECT
    BedProfile.profile,
    BedProfile.orgName,
    BedProfile.planApplied,
    BedProfile.planBedDays,
    SUM(Actions.factApplied) AS `factApplied`,
    SUM(Actions.factBedDays) AS `factBedDays`,
    YEAR(Event.execDate) AS `execYear`
FROM
    (
    SELECT DISTINCT
        OrgStructure.organisation_id AS `org_id`,
        rbHospitalBedProfile.id AS `profile_id`,
        rbHospitalBedProfile.name AS `profile`,
        (   OrgStructure_Planning.plan1 + OrgStructure_Planning.plan2 +
            OrgStructure_Planning.plan3 + OrgStructure_Planning.plan4 +
            OrgStructure_Planning.plan5 + OrgStructure_Planning.plan6 +
            OrgStructure_Planning.plan7 + OrgStructure_Planning.plan8 +
            OrgStructure_Planning.plan9 + OrgStructure_Planning.plan10 +
            OrgStructure_Planning.plan11 + OrgStructure_Planning.plan12
        ) AS `planApplied`,
        (   OrgStructure_Planning.bedDays1 + OrgStructure_Planning.bedDays2 +
            OrgStructure_Planning.bedDays3 + OrgStructure_Planning.bedDays4 +
            OrgStructure_Planning.bedDays5 + OrgStructure_Planning.bedDays6 +
            OrgStructure_Planning.bedDays7 + OrgStructure_Planning.bedDays8 +
            OrgStructure_Planning.bedDays9 + OrgStructure_Planning.bedDays10 +
            OrgStructure_Planning.bedDays11 + OrgStructure_Planning.bedDays12
        ) AS `planBedDays`,
        OrgStructure.name AS `orgName`
    FROM
        OrgStructure
        JOIN OrgStructure_Planning ON OrgStructure.id = OrgStructure_Planning.orgStructure_id
        JOIN rbHospitalBedProfile ON OrgStructure_Planning.profile_id = rbHospitalBedProfile.id
        JOIN OrgStructure_HospitalBed ON OrgStructure_Planning.orgStructure_id = OrgStructure_HospitalBed.master_id
        JOIN rbHospitalBedShedule ON OrgStructure_HospitalBed.schedule_id = rbHospitalBedShedule.id
    WHERE
        OrgStructure_Planning.year BETWEEN {begYear} AND {endYear}
        AND rbHospitalBedShedule.code = {bedSheduleCode}
    ) AS `BedProfile`

    JOIN Event ON BedProfile.org_id = Event.org_id

    JOIN
    (
        SELECT
            Action.event_id,
            SUM(IF(ActionType.flatCode = 'leaved',1,0)) AS `factApplied`,
            SUM(IF(ActionType.flatCode = 'moving', Action.amount, 0)) AS `factBedDays`
        FROM
       (
            SELECT
                DISTINCT Action.event_id AS `id`
            FROM
                Action
                JOIN ActionType ON Action.actionType_id = ActionType.id
                JOIN ActionProperty ON ActionProperty.action_id = Action.id
                JOIN ActionPropertyType ON ActionProperty.type_id = ActionPropertyType.id
                JOIN ActionProperty_String ON ActionProperty.id = ActionProperty_String.id
                JOIN Diagnostic ON Action.event_id = Diagnostic.event_id
                JOIN Diagnosis ON Diagnostic.diagnosis_id = Diagnosis.id
                JOIN Person ON Action.person_id = Person.id
            WHERE
                Action.deleted = 0
                AND ActionType.deleted = 0
                AND ActionProperty.deleted = 0
                AND ActionPropertyType.deleted = 0
                AND Diagnostic.deleted = 0
                AND Diagnosis.deleted = 0
                AND ActionType.flatCode = 'received'
                AND ActionPropertyType.name = 'Состояние при поступлении'
                {receivedStateCond}
                AND Diagnosis.MKB >= '{MKBFrom}'
                AND Diagnosis.MKB <= '{MKBTo}'
                AND Person.org_id = {orgId}
        ) AS `ReceivedEvents`
        JOIN Action ON Action.event_id = ReceivedEvents.id
        JOIN ActionType ON Action.actionType_id = ActionType.id
        GROUP BY Action.event_id
        ORDER BY NULL
    ) AS `Actions` ON Event.id = Actions.event_id

    JOIN Client ON Event.client_id = Client.id
WHERE
    Event.deleted = 0
    AND Client.deleted = 0
    {eventOrderCond}
    AND Event.execDate >= '{begYear}-01-01T00:00:00'
    AND Event.execDate <= '{endYear}-12-31T23:59:59'
    AND (YEAR(Event.setDate) - YEAR(Client.birthDate)) BETWEEN {ageFrom} AND {ageTo}
GROUP BY
    BedProfile.profile_id,
    YEAR(Event.execDate)
ORDER BY NULL;
        """.format(
            begYear=params['reportYear']-2,
            endYear=params['reportYear'],
            eventOrderCond=eventOrderCond,
            receivedStateCond=receivedStateCond,
            bedSheduleCode=bedSheduleCode,
            MKBFrom=params['MKBFrom'] if params['MKBFilter'] else 'A00.00',
            MKBTo=params['MKBTo'] if params['MKBFilter'] else 'Z99.99',
            orgId=QtGui.qApp.currentOrgId(),
            ageFrom=params['ageFrom'],
            ageTo=params['ageTo'])



def selectData(params):
    db = QtGui.qApp.db
    reportDataRoundClock = dict()  # { orgName: {profile: { planBedDays:[year1, year2, year3], ...} } }
    reportDataDaily = dict()       # { orgName: {profile: { planBedDays:[year1, year2, year3], ...} } }
    reportDataDiagnostic = dict()  # { speciality: int }

    roundClockQuery = db.query(getStmt(params, 1))
    dailyQuery = db.query(getStmt(params, 2))

    for query,reportData in ((roundClockQuery,reportDataRoundClock), (dailyQuery,reportDataDaily)):
        while query.next():
            record = query.record()
            profile = forceString(record.value('profile'))
            orgName = forceString(record.value('orgName'))
            planApplied = forceInt(record.value('planApplied'))
            planBedDays = forceInt(record.value('planBedDays'))
            factApplied = forceInt(record.value('factApplied'))
            factBedDays = forceInt(record.value('factBedDays'))
            execYear = abs(forceInt(record.value('execYear')) - params['reportYear'])

            if not reportData.has_key(orgName):
                reportData[orgName] = {}

            if not reportData[orgName].has_key(profile):
                reportData[orgName][profile] = {
                    'planBedDays': [0]*3,
                    'planApplied': [0]*3,
                    'factBedDays': [0]*3,
                    'factApplied': [0]*3
                }

            reportData[orgName][profile]['planBedDays'][execYear] = planBedDays
            reportData[orgName][profile]['planApplied'][execYear] = planApplied
            reportData[orgName][profile]['factBedDays'][execYear] = factBedDays
            reportData[orgName][profile]['factApplied'][execYear] = factApplied


    # Консультативно-диагностический центр
    tableEvent        = db.table('Event')
    tablePerson       = db.table('Person')
    tableSpeciality   = db.table('rbSpeciality')
    tableOrgStructure = db.table('OrgStructure')
    tableAction       = db.table('Action')

    queryTable = tableEvent
    queryTable = queryTable.innerJoin(tableAction, tableEvent['id'].eq(tableAction['event_id']))
    queryTable = queryTable.innerJoin(tablePerson, tableAction['person_id'].eq(tablePerson['id']))
    queryTable = queryTable.innerJoin(tableSpeciality, tablePerson['speciality_id'].eq(tableSpeciality['id']))
    queryTable = queryTable.innerJoin(tableOrgStructure, tablePerson['orgStructure_id'].eq(tableOrgStructure['id']))

    cols = [ 'YEAR(Event.execDate) AS `execYear`',
             'COUNT(DISTINCT Action.id) AS `factApplied`',
             tableSpeciality['name']
           ]
    cond = [ tableEvent['deleted'].eq(0),
             tablePerson['deleted'].eq(0),
             tableAction['deleted'].eq(0),
             tableOrgStructure['hasHospitalBeds'].eq(0),
             "Event.execDate >= '%d-01-01T00:00:00'" % (params['reportYear']-2),
             "Event.execDate <= '%d-12-31T23:59:59'" % params['reportYear']
           ]
    groupBy = [ tableSpeciality['id'].name(),
                'YEAR(Event.execDate)'
              ]

    diagnosticStmt = db.selectStmtGroupBy(queryTable, cols, cond, groupBy, order='NULL')
    query = db.query(diagnosticStmt)
    while query.next():
        record = query.record()
        speciality = forceString(record.value('name'))
        count = forceInt(record.value('factApplied'))
        year = abs(forceInt(record.value('execYear')) - params['reportYear'])

        if not reportDataDiagnostic.has_key(speciality):
            reportDataDiagnostic[speciality] = [0]*3

        reportDataDiagnostic[speciality][year] = count


    return reportDataRoundClock, reportDataDaily, reportDataDiagnostic



def getProfilesTotal(orgs):
    total = {
        'planBedDays': [0, 0, 0],
        'planApplied': [0, 0, 0],
        'factBedDays': [0, 0, 0],
        'factApplied': [0, 0, 0]
    }
    for dicProfiles in orgs.values():
        for profile in dicProfiles.values():
            for i in xrange(3):
                total['planBedDays'][i] += profile['planBedDays'][i]
                total['planApplied'][i] += profile['planApplied'][i]
                total['factBedDays'][i] += profile['factBedDays'][i]
                total['factApplied'][i] += profile['factApplied'][i]
    return total



class CProfileYearReport(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.profileYearReportSetupDialog = None
        self.setTitle(u'Годовой отчет за ЛПУ по профилям')

    def getSetupDialog(self, parent):
        result = CProfileYearReportSetupDialog(parent)
        self.profileYearReportSetupDialog = result
        return result

    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        reportYear = params['reportYear']
        reportDataRoundClock, reportDataDaily, reportDataDiagnostic = selectData(params)

        alignCenter, alignRight = CReportBase.AlignCenter, CReportBase.AlignRight

        cursor.mergeBlockFormat(alignCenter)
        cursor.insertBlock()
        cursor.insertText(u'Годовой отчет за ЛПУ по профилям с учетом плановых и фактических показателей в сравнении с прошедшими периодами')
        cursor.insertBlock()

        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        cols = [('10%', [u'Подразделение', u'', u''], CReportBase.AlignLeft),
                ('5%', [u'%d год' % (reportYear), u'План', u'Койко-дней'], CReportBase.AlignLeft),
                ('5%', [u'', u'', u'Обращений'], CReportBase.AlignLeft),
                ('5%', [u'', u'Факт', u'Койко-дней'], CReportBase.AlignLeft),
                ('5%', [u'', u'', u'Обращений'], CReportBase.AlignLeft),
                ('5%', [u'', u'% выполнения плана', u'Койко-дней'], CReportBase.AlignLeft),
                ('5%', [u'', u'', u'Обращений'], CReportBase.AlignLeft),

                ('5%', [u'%d год' % (reportYear-1), u'План', u'Койко-дней'], CReportBase.AlignLeft),
                ('5%', [u'', u'', u'Обращений'], CReportBase.AlignLeft),
                ('5%', [u'', u'Факт', u'Койко-дней'], CReportBase.AlignLeft),
                ('5%', [u'', u'', u'Обращений'], CReportBase.AlignLeft),
                ('5%', [u'', u'% выполнения плана', u'Койко-дней'], CReportBase.AlignLeft),
                ('5%', [u'', u'', u'Обращений'], CReportBase.AlignLeft),

                ('5%', [u'%d год' % (reportYear-2), u'План', u'Койко-дней'], CReportBase.AlignLeft),
                ('5%', [u'', u'', u'Обращений'], CReportBase.AlignLeft),
                ('5%', [u'', u'Факт', u'Койко-дней'], CReportBase.AlignLeft),
                ('5%', [u'', u'', u'Обращений'], CReportBase.AlignLeft),
                ('5%', [u'', u'% выполнения плана', u'Койко-дней'], CReportBase.AlignLeft),
                ('5%', [u'', u'', u'Обращений'], CReportBase.AlignLeft)]
        table = createTable(cursor, cols)
        table.mergeCells(0, 0, 3, 1)

        table.mergeCells(0, 1, 1, 6)
        table.mergeCells(0, 7, 1, 6)
        table.mergeCells(0, 13, 1, 6)

        table.mergeCells(1, 1, 1, 2)
        table.mergeCells(1, 3, 1, 2)
        table.mergeCells(1, 5, 1, 2)
        table.mergeCells(1, 7, 1, 2)
        table.mergeCells(1, 9, 1, 2)
        table.mergeCells(1, 11, 1, 2)
        table.mergeCells(1, 13, 1, 2)
        table.mergeCells(1, 15, 1, 2)
        table.mergeCells(1, 17, 1, 2)


        # Процентное соотношение 'piece' от 'value'
        def percentRaito(value, piece):
            if value == 0: return '100%'
            if piece == 0: return '0%'
            return "%g%%" % round((float(piece) / value) * 100.0, 1)


        # Круглосуточный и дневной стационар
        for data, orgTitle, orgTotalTitle in (
                (reportDataRoundClock, u'Стационар круглосуточный', u'Итого за круглосуточный стационар'),
                (reportDataDaily, u'Дневной стационар', u'Итого за дневной стационар')):

            row = table.addRow()
            table.setText(row, 0, orgTitle, blockFormat=alignCenter)
            table.mergeCells(row, 0, 1, 19)

            for orgName, profiles in data.items():
                row = table.addRow()
                table.setText(row, 0, orgName)
                for name, values in profiles.items():
                    row = table.addRow()
                    table.setText(row, 0, '    ' + name)  # Имя профиля с отступом
                    for i in xrange(3):
                        table.setText(row, 1 + 6*i, values['planBedDays'][i], blockFormat=alignRight)
                        table.setText(row, 2 + 6*i, values['planApplied'][i], blockFormat=alignRight)
                        table.setText(row, 3 + 6*i, values['factBedDays'][i], blockFormat=alignRight)
                        table.setText(row, 4 + 6*i, values['factApplied'][i], blockFormat=alignRight)
                        table.setText(row, 5 + 6*i, percentRaito(values['planBedDays'][i], values['factBedDays'][i]), blockFormat=alignRight)
                        table.setText(row, 6 + 6*i, percentRaito(values['planApplied'][i], values['factApplied'][i]), blockFormat=alignRight)

            # Итоговые значения
            total = getProfilesTotal(data)
            row = table.addRow()
            table.setText(row, 0, orgTotalTitle)
            for i in xrange(3):
                table.setText(row, 1 + 6*i, total['planBedDays'][i], blockFormat=alignRight)
                table.setText(row, 2 + 6*i, total['planApplied'][i], blockFormat=alignRight)
                table.setText(row, 3 + 6*i, total['factBedDays'][i], blockFormat=alignRight)
                table.setText(row, 4 + 6*i, total['factApplied'][i], blockFormat=alignRight)


        # Консультативно-диагностический центр
        row = table.addRow()
        table.setText(row, 0, u'Консультативно-диагностический центр', blockFormat=alignCenter)
        table.mergeCells(row, 0, 1, 19)

        for name, values in reportDataDiagnostic.items():
            row = table.addRow()
            table.setText(row, 0, name)
            for i in xrange(3):
                table.setText(row, 1 + 6*i, u'—', blockFormat=alignRight)
                table.setText(row, 3 + 6*i, u'—', blockFormat=alignRight)
                table.setText(row, 4 + 6*i, values[i], blockFormat=alignRight)

        row = table.addRow()
        table.setText(row, 0,  u'Итого за КДЦ')
        for i in xrange(3):
            table.setText(row, 1 + 6*i, u'—', blockFormat=alignRight)
            table.setText(row, 3 + 6*i, u'—', blockFormat=alignRight)
            table.setText(row, 4 + 6*i, sum(lst[i] for lst in reportDataDiagnostic.values()), blockFormat=alignRight)

        return doc



class CProfileYearReportSetupDialog(CDialogBase, Ui_ProfileYearReportSetupDialog):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle(u'Годовой отчет за ЛПУ по профилям')
        self.setObjectName(u'Годовой отчет за ЛПУ по профилям')

    def setParams(self, params):
        self.edtReportYear.setValue(params.get('reportYear', QDate.currentDate().year()))
        self.cmbReceivedCnd.setCurrentIndex(params.get('received', RECEIVED_STATE_NOT_SET))
        self.cmbOrder.setCurrentIndex(params.get('order', RECEIVED_ORDER_NOT_SET))
        self.edtAgeFrom.setValue(params.get('ageFrom', 0))
        self.edtAgeTo.setValue(params.get('ageTo', 150))
        self.chkEnableMKB.setChecked(params.get('MKBFilter', False))
        self.edtMKBFrom.setText(params.get('MKBFrom', 'A00.00'))
        self.edtMKBTo.setText(params.get('MKBTo', 'Z99.99'))

    def params(self):
        result = {}
        result['reportYear'] = self.edtReportYear.value()
        result['received'] = self.cmbReceivedCnd.currentIndex()
        result['order'] = self.cmbOrder.currentIndex()
        result['ageFrom'] = self.edtAgeFrom.value()
        result['ageTo'] = self.edtAgeTo.value()
        result['MKBFilter'] = self.chkEnableMKB.isChecked()
        result['MKBFrom'] = self.edtMKBFrom.text()
        result['MKBTo'] = self.edtMKBTo.text()
        return result
