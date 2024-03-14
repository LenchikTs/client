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
from PyQt4.QtCore import QDate, QTime, QDateTime

from library.Utils      import forceString, forceInt
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.ReportView import CPageFormat
from Orgs.Utils         import getOrganisationInfo

from Reports.Ui_ReportHealthResortSetupDialog import Ui_ReportHealthResortSetupDialog
from library.DialogBase         import CDialogBase


def selectData(params):
    reportData = {}    # { district : { profile : { planned:0, count:0 } } }
    otherVouchers = 0  # Прочие путевки (регион не указан)

    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())

    db = QtGui.qApp.db
    tableAction = db.table('Action')
    tableActionType = db.table('ActionType')
    tableEvent = db.table('Event')
    tableEventType = db.table('EventType')
    tableEventVoucher = db.table('Event_Voucher')
    tableMedicalAidType = db.table('rbMedicalAidType')
    tablePerson = db.table('Person')
    tableActionProperty = db.table('ActionProperty')
    tableAPHospitalBedProfile = db.table('ActionProperty_rbHospitalBedProfile')
    tableHospitalBedProfile = db.table('rbHospitalBedProfile')
    tableOKATO = db.table('kladr.OKATO')
    tableHRAP = db.table('HealthResortActivityPlanning')

    sumPlans = None
    if begDate > endDate:
        begDate = endDate
    if begDate.year() == endDate.year() and begDate.month() == endDate.month():
        sumPlans = 'HealthResortActivityPlanning.`plan%d`' % endDate.month()
    else:
        sumPlans = '+'.join(['HealthResortActivityPlanning.`plan%d`' % i for i in xrange(begDate.month(), endDate.month()+1)])

    if begDate:
        begDate = QDateTime(begDate)
        begDate.setTime(QTime(9,0,0))
    if endDate:
        endDate = QDateTime(endDate)
        endDate.setTime(QTime(9,0,0))

    # Кол-во путевок
    queryTable = tableEvent
    queryTable = queryTable.innerJoin(tableEventType, tableEvent['eventType_id'].eq(tableEventType['id']))
    queryTable = queryTable.innerJoin(tableEventVoucher, tableEventVoucher['event_id'].eq(tableEvent['id']))
    queryTable = queryTable.innerJoin(tableMedicalAidType, tableEventType['medicalAidType_id'].eq(tableMedicalAidType['id']))
    queryTable = queryTable.innerJoin(tablePerson, tableEvent['execPerson_id'].eq(tablePerson['id']))
    queryTable = queryTable.innerJoin(tableAction, tableAction['event_id'].eq(tableEvent['id']))
    queryTable = queryTable.innerJoin(tableActionType, tableAction['actionType_id'].eq(tableActionType['id']))
    queryTable = queryTable.innerJoin(tableActionProperty, tableActionProperty['action_id'].eq(tableAction['id']))
    queryTable = queryTable.innerJoin(tableAPHospitalBedProfile, tableActionProperty['id'].eq(tableAPHospitalBedProfile['id']))
    queryTable = queryTable.innerJoin(tableHospitalBedProfile, tableAPHospitalBedProfile['value'].eq(tableHospitalBedProfile['id']))
    queryTable = queryTable.leftJoin(tableOKATO, tableOKATO['CODE'].eq(tableEvent['directionRegion']))

    cols = [ 'COUNT(DISTINCT Event_Voucher.id) AS voucherCount',
             tableOKATO['NAME'].alias('regionName'),
             tableHospitalBedProfile['name'].alias('profileName')
           ]
    cond = [ tableEvent['deleted'].eq(0),
             tableAction['deleted'].eq(0),
             tableEvent['isClosed'].eq(1),
             tablePerson['org_id'].eq(QtGui.qApp.currentOrgId()),
             tableEventType['deleted'].eq(0),
             tableEventVoucher['deleted'].eq(0),
             tableActionType['flatCode'].eq('leaved'),
             tableActionProperty['deleted'].eq(0),
             tableMedicalAidType['code'].eq(8),
             tableAction['endDate'].ge(begDate),
             tableAction['endDate'].le(endDate)
           ]
    group =[ tableEvent['directionRegion'].name(),
             tableHospitalBedProfile['code'].name()
           ]
    stmt = db.selectStmtGroupBy(queryTable, cols, where=cond, group=group)
    query = db.query(stmt)
    while query.next():
        record = query.record()
        voucherCount = forceInt(record.value('voucherCount'))
        regionName = forceString(record.value('regionName'))
        profileName = forceString(record.value('profileName'))

        if regionName != '':
            if not reportData.has_key(regionName):
                reportData[regionName] = dict()
            if not reportData[regionName].has_key(profileName):
                reportData[regionName][profileName] = dict(count=0, planned=0)
            reportData[regionName][profileName]['count'] += voucherCount
        else:
            otherVouchers += voucherCount

    # План
    queryTable = tableHRAP
    queryTable = queryTable.innerJoin(tableOKATO, tableOKATO['CODE'].eq(tableHRAP['districtCode']))
    queryTable = queryTable.innerJoin(tableHospitalBedProfile, tableHospitalBedProfile['id'].eq(tableHRAP['profile_id']))

    cols = [ 'SUM(%s) AS voucherPlanned' % sumPlans,
             tableHospitalBedProfile['name'].alias('profileName'),
             tableOKATO['NAME'].alias('regionName')
           ]
    cond = [ tableHRAP['planYear'].eq(begDate.date().year())
           ]
    group =[ tableHRAP['profile_id'].name(),
             tableHRAP['districtCode'].name()
           ]
    stmt = db.selectStmtGroupBy(queryTable, cols, where=cond, group=group)
    query = db.query(stmt)
    while query.next():
        record = query.record()
        regionName = forceString(record.value('regionName'))
        profileName = forceString(record.value('profileName'))
        voucherPlanned = forceInt(record.value('voucherPlanned'))

        if regionName != '':
            if not reportData.has_key(regionName):
                reportData[regionName] = dict()
            if not reportData[regionName].has_key(profileName):
                reportData[regionName][profileName] = dict(count=0, planned=0)
            reportData[regionName][profileName]['planned'] += voucherPlanned
        else:
            otherVouchers += voucherCount


    return reportData, otherVouchers


class CReportHealthResortAnalysisUsePlacesRegions(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Анализ использования мест регионами')
        self.orientation = CPageFormat.Landscape


    def getSetupDialog(self, parent):
        result = CReportHealthResortSetupDialog(parent)
        result.setTitle(self.title())
        return result


    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.setBlockFormat(CReportBase.AlignCenter)

        orgId = QtGui.qApp.currentOrgId()
        orgInfo = getOrganisationInfo(orgId)
        shortName = orgInfo.get('shortName', u'ЛПУ в настройках не указано!')
        cursor.insertText(self.title() + u'\n' + shortName)
        cursor.insertBlock()

        self.dumpParams(cursor, params)
        reportData, otherVouchers = selectData(params)

        alignLeft = CReportBase.AlignLeft
        alignRight = CReportBase.AlignRight
        alignCenter = CReportBase.AlignCenter
        charBold = QtGui.QTextCharFormat()
        charBold.setFontWeight(QtGui.QFont.Bold)


        # Вычисление процента 'piece' от 'value'
        def percentRaito(value, piece):
            if value == 0: return '100%'
            elif piece == 0: return '0%'
            else: return "%g%%" % round(piece / float(value) * 100, 1)


        # Собрать все названия профилей для всех регионов
        profileNames = set()
        for profiles in reportData.values():
            profileNames.update(profiles.keys())
        count = len(profileNames) * 3    # Каждый профиль делится на три графы

        if count > 0:
            tableColumns = [('%d%%' % int(50.0 / count), ['', '', ''], alignLeft)] * count  # Резервирование столбцов под название профилей
        else:
            tableColumns = []
        tableColumns.insert(0, ('5%',  [u'№ п/п', '', ''],         alignLeft))
        tableColumns.insert(1, ('25%', [u'Районы СПб', '' ,''],    alignLeft))
        tableColumns.append((('7%',    ['', u'Всего', u'план'],    alignLeft)))
        tableColumns.append((('7%',    ['', '', u'пролеч.'],       alignLeft)))
        tableColumns.append((('6%',    ['', '', '%'],              alignLeft)))

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 3, 1)
        table.mergeCells(0, 1, 3, 1)
        table.mergeCells(0, count+2, 1, 3)
        table.mergeCells(1, count+2, 1, 3)

        table.setText(0, 2, u'Реализовано путевок по профилю коек / Пролечено детей по профилю основного заболевания',  blockFormat=alignCenter, charFormat=charBold)
        table.mergeCells(0, 2, 1, count+3)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.setBlockFormat(CReportBase.AlignCenter)
        totalDistrict = dict()

        # Вывод профилей коек
        for i, profile in enumerate(sorted(profileNames)):
            table.setText(1, 3*i+2, profile, charFormat=charBold, blockFormat=alignCenter)
            table.mergeCells(1, 3*i+2, 1, 3)
            table.setText(2, 3*i+2, u'план', blockFormat=alignCenter)
            table.setText(2, 3*i+3, u'пролеч.', blockFormat=alignCenter)
            table.setText(2, 3*i+4, '%', blockFormat=alignCenter)

        # Вывод названий регионов со значениями по профилям
        for district in sorted(reportData.keys()):
            row = table.addRow()
            table.setText(row, 0, str(row - 2))
            table.setText(row, 1, district)
            for i, profile in enumerate(sorted(profileNames)):
                value = reportData[district].get(profile, {'planned':0, 'count':0})
                table.setText(row, 3*i+2, value['planned'], blockFormat=alignRight)
                table.setText(row, 3*i+3, value['count'], blockFormat=alignRight)
                table.setText(row, 3*i+4, percentRaito(value['planned'], value['count']), blockFormat=alignRight)

                total = totalDistrict.get(district, {'planned':0, 'count':0})
                total['planned'] += value['planned']
                total['count'] += value['count']
                totalDistrict[district] = total

            # Сумма по регионам
            total = totalDistrict[district]
            table.setText(row, count+2, total['planned'], blockFormat=alignRight, charFormat=charBold)
            table.setText(row, count+3, total['count'], blockFormat=alignRight, charFormat=charBold)
            table.setText(row, count+4, percentRaito(total['planned'], total['count']), blockFormat=alignRight, charFormat=charBold)

        # Сумма по профилям
        row = table.addRow()
        table.setText(row, 1, u'Всего по СПб', charFormat=charBold)
        totalProfile = dict()

        for district in sorted(reportData.keys()):
            for i, profile in enumerate(sorted(profileNames)):
                value = reportData[district].get(profile, {'planned':0, 'count':0})
                total = totalProfile.get(profile, {'planned':0, 'count':0})
                total['planned'] += value['planned']
                total['count'] += value['count']
                totalProfile[profile] = total
        for i, profile in enumerate(sorted(profileNames)):
            value = totalProfile[profile]
            table.setText(row, 3*i+2, value['planned'], blockFormat=alignRight, charFormat=charBold)
            table.setText(row, 3*i+3, value['count'], blockFormat=alignRight, charFormat=charBold)
            table.setText(row, 3*i+4, percentRaito(value['planned'], value['count']), blockFormat=alignRight, charFormat=charBold)

        # Сумма по итогу профилей
        total = {'planned': 0, 'count': 0}
        for profile in sorted(profileNames):
            total['planned'] += totalProfile[profile]['planned']
            total['count'] += totalProfile[profile]['count']
        table.setText(row, count+2, total['planned'], blockFormat=alignRight, charFormat=charBold)
        table.setText(row, count+3, total['count'], blockFormat=alignRight, charFormat=charBold)
        table.setText(row, count+4, percentRaito(total['planned'], total['count']), blockFormat=alignRight, charFormat=charBold)

        # Прочие путевки
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertText(u'Прочие путевки: ' + str(otherVouchers))

        return doc


class CReportHealthResortSetupDialog(CDialogBase, Ui_ReportHealthResortSetupDialog):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)

    def setTitle(self, title):
        self.setWindowTitleEx(title)

    def setParams(self, params):
        currentDate = QDate.currentDate()
        self.edtBegDate.setDate(params.get('begDate', QDate(currentDate.year(), 1, 1)))
        self.edtEndDate.setDate(params.get('endDate', currentDate))

    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        return result

