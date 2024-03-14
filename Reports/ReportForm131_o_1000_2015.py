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
from PyQt4.QtCore import QDate, QDateTime

from library.Utils      import firstYearDay, forceInt, forceString, lastYearDay

from Orgs.Utils         import getOrgStructureFullName, getOrgStructurePersonIdList
from RefBooks.ContingentType.List import CContingentTypeTranslator
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.Utils      import dateRangeAsStr, getAgeClass

from Reports.ReportForm131_1000_SetupDialog import CReportForm131_1000_SetupDialog


def selectData(params):
    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())
    contingentTypeId = params.get('contingentTypeId', None)
    isAttache = params.get('isAttache', False)
    orgStructureId = params.get('orgStructureId', None)
    orgId = params.get('orgId', None)
    if not endDate or not contingentTypeId:
        return None
    begYearDate = firstYearDay(begDate)
    endYearDate = lastYearDay(endDate)
    db = QtGui.qApp.db
    if contingentTypeId:
        joinAttach = u''
        condAttach = u''
        if isAttache:
            joinAttach = u'''INNER JOIN ClientAttach ON ClientAttach.client_id = clientCT.id
                             INNER JOIN rbAttachType ON rbAttachType.id = ClientAttach.attachType_id'''
            condAttach = u'''%s
    AND (ClientAttach.deleted = 0) AND (rbAttachType.temporary = 0)
    AND (((ClientAttach.begDate IS NULL)
    OR (DATE(ClientAttach.begDate) <= DATE(%s))))
    AND (((ClientAttach.endDate IS NULL)
                OR (DATE(ClientAttach.endDate) >= DATE(%s))))''' % ((U'AND (ClientAttach.LPU_id = %s)' % (orgId)) if orgId else u'',
                                                                    db.formatDate(endDate), db.formatDate(begDate))
        condOrgStructure = u''
        if orgStructureId:
            personIdList = getOrgStructurePersonIdList(orgStructureId)
            if personIdList:
                condOrgStructure = u''' AND Event.execPerson_id IN (%s)''' % (u','.join(str(personId) for personId in personIdList if personId))
        condOrgStructure = u''
        if orgStructureId:
            personIdList = getOrgStructurePersonIdList(orgStructureId)
            if personIdList:
                condOrgStructure = u''' AND Event.execPerson_id IN (%s)''' % (u','.join(str(personId) for personId in personIdList if personId))
        stmt = u'''
    SELECT clientSex,
           clientAge,
           SUM(executedI) AS executedCntI,
           SUM(executedII) AS executedCntII
    FROM (SELECT IF(rbEventProfile.regionalCode = '8008', 1, 0) AS executedI,
                 IF(rbEventProfile.regionalCode = '8009', 1, 0) AS executedII,
                 clientCT.sex AS clientSex,
                 age(clientCT.birthDate, %(endYearDate)s) AS clientAge
          FROM Event
            left join EventType on EventType.id = Event.eventType_id
            left join rbEventProfile on rbEventProfile.id = EventType.eventProfile_id
            left join Action on Action.event_id = Event.id
          INNER JOIN Client AS clientCT ON clientCT.id = Event.client_id
          %(joinAttach)s
          WHERE Event.deleted = 0
            AND DATE(Event.execDate) BETWEEN DATE(%(begDate)s) AND DATE(%(endDate)s)
            AND rbEventProfile.regionalCode in ('8008', '8009')
            %(condAttach)s
            %(condOrgStructure)s
          GROUP BY clientCT.sex, clientCT.birthDate, rbEventProfile.regionalCode) AS T
            GROUP BY clientSex, clientAge''' % dict(begDate=db.formatDate(begDate),
                                                    endDate=db.formatDate(endDate),
                                                    begYearDate=db.formatDate(begYearDate),
                                                    endYearDate=db.formatDate(endYearDate),
                                                    joinAttach=joinAttach,
                                                    begPrevYearDate=db.formatDate(begYearDate.addYears(-1)),
                                                    condAttach=condAttach,
                                                    condOrgStructure=condOrgStructure
                                                    )
    return db.query(stmt)


class CReportForm131_o_1000_2015(CReport):

    ages = (u'18-36 лет', u'39-60 лет', u'Старше 60 лет')

    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.parent = parent
        self.setTitle(u'Сведения о проведении диспансеризации определенных групп взрослого населения')

    def getSetupDialog(self, parent):
        result = CReportForm131_1000_SetupDialog(parent)
        result.setTitle(self.title())
        return result

    def dumpParams(self, cursor, params):
        db = QtGui.qApp.db
        description = []
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        if begDate or endDate:
            description.append(dateRangeAsStr(u'за период', begDate, endDate))
        contingentTypeId = params.get('contingentTypeId', None)
        orgStructureId = params.get('orgStructureId', None)
        isAttache = params.get('isAttache', False)
        orgId = params.get('orgId', None)
        if orgStructureId:
            description.append(u'подразделение: ' + getOrgStructureFullName(orgStructureId))
        if contingentTypeId:
            description.append(u'тип контингента: ' + forceString(db.translate('rbContingentType', 'id', contingentTypeId, 'name')))
        if isAttache:
            description.append(u'прикрепление к ЛПУ: ' + forceString(db.translate('Organisation', 'id', orgId, 'shortName')))
        description.append(u'отчёт составлен: ' + forceString(QDateTime.currentDateTime()))
        columns = [('100%', [], CReportBase.AlignLeft)]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()

    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.insertText(u'(1000)')
        cursor.insertBlock()
        tableColumns = [
            ('7%',   [u'Возрастная группа', u'', u'', u'1'], CReportBase.AlignLeft),
            ('3%',   [u'№ строки', u'', u'', u'2'], CReportBase.AlignRight),
            ('7.5%', [u'Все население', u'Численность населения на 01.01 текущего года', u'', u'3'], CReportBase.AlignRight),
            ('7.5%', [u'', u'Подлежит диспансе-ризации по плану текущего года', u'', u'4'], CReportBase.AlignRight),
            ('7.5%', [u'', u'Прошли диспансеризацию (чел.)', u'I этап', u'5'], CReportBase.AlignRight),
            ('7.5%', [u'', u'', u'II этап', u'6'], CReportBase.AlignRight),
            ('7.5%', [u'Мужчины', u'Численность населения на 01.01 текущего года', u'', u'7'], CReportBase.AlignRight),
            ('7.5%', [u'', u'Подлежит диспансе-ризации по плану текущего года', u'', u'8'], CReportBase.AlignRight),
            ('7.5%', [u'', u'Прошли диспансеризацию (чел.)', u'I этап', u'9'], CReportBase.AlignRight),
            ('7.5%', [u'', u'', u'II этап', u'10'], CReportBase.AlignRight),
            ('7.5%', [u'Женщины', u'Численность населения на 01.01 текущего года', u'', u'11'], CReportBase.AlignRight),
            ('7.5%', [u'', u'Подлежит диспансе-ризации по плану текущего года', u'', u'12'], CReportBase.AlignRight),
            ('7.5%', [u'', u'Прошли диспансеризацию (чел.)', u'I этап', u'13'], CReportBase.AlignRight),
            ('7.5%', [u'', u'', u'II этап', u'14'], CReportBase.AlignRight),
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 3, 1)
        table.mergeCells(0, 1, 3, 1)
        table.mergeCells(1, 2, 2, 1)
        table.mergeCells(1, 3, 2, 1)
        table.mergeCells(0, 2, 1, 4)
        table.mergeCells(1, 4, 1, 2)
        table.mergeCells(0, 6, 1, 4)
        table.mergeCells(1, 6, 2, 1)
        table.mergeCells(1, 7, 2, 1)
        table.mergeCells(1, 8, 1, 2)
        table.mergeCells(0, 10, 1, 4)
        table.mergeCells(1, 10, 2, 1)
        table.mergeCells(1, 11, 2, 1)
        table.mergeCells(1, 12, 1, 2)
        query = selectData(params)
        if query is None:
            return doc
        endDate = params['endDate']
        isAttache = params.get('isAttache', False)
        orgId = params.get('orgId', None)
        reportData = [[0]*12 for age in self.ages]
        self.getDataByEvents(reportData, query)
        self.getDataByContingent(reportData, params)
        commonAgeStats = self.getCommonAgeStats(endDate, isAttache, orgId)
        self.addCommonAgeData(reportData, commonAgeStats)
        result = [0]*12
        cnt = 1
        for reportRow, age in enumerate(self.ages):
            i = table.addRow()
            table.setText(i, 0, age)
            table.setText(i, 1, cnt)
            cnt += 1
            reportLine = reportData[reportRow]
            for idx, value in enumerate(reportLine):
                column = 2+idx
                table.setText(i, column, value)
                result[idx] += value
        i = table.addRow()
        table.mergeCells(i, 0, 1, 2)
        table.setText(i, 1, u'Всего')
        for idx, value in enumerate(result):
            column = 2+idx
            table.setText(i, column, value)
        return doc

    def getDataByEvents(self, reportData, query):
        while query.next():
            record = query.record()
            clientSex = forceInt(record.value('clientSex'))
            clientAge = forceInt(record.value('clientAge'))
            executedCntI = forceInt(record.value('executedCntI'))
            executedCntII = forceInt(record.value('executedCntII'))
            if executedCntI or executedCntII:
                reportRow = getAgeClass(clientAge)
                if reportRow is not None:
                    reportLine = reportData[reportRow]
                    column = 5 if clientSex == 1 else 9
                    reportLine[column+1] += executedCntI
                    reportLine[column+2] += executedCntII
                    reportLine[2] += executedCntI
                    reportLine[3] += executedCntII
        return reportData

    def addCommonAgeData(self, reportData, commonAgeStats):
        for (clientAge, sex), val in commonAgeStats.iteritems():
            reportRow = getAgeClass(clientAge)
            if reportRow is not None:
                reportLine = reportData[reportRow]
                if sex == 1:
                    reportLine[4] += val
                elif sex == 2:
                    reportLine[8] += val
                reportLine[0] += val

    def getCommonAgeStats(self, endDate, isAttache, orgId):
        db = QtGui.qApp.db
        date = lastYearDay(endDate)
        strDate = db.formatDate(date)
        tableClient = db.table('Client')
        if isAttache:
            tableClientAddress = db.table('ClientAddress')
            tableAddress = db.table('Address')
            tableClientAttach = db.table('ClientAttach')
            tableAttachType = db.table('rbAttachType')
            tableAddressHouse = db.table('AddressHouse')
            clientAddressJoinCond = [tableClientAddress['client_id'].eq(tableClient['id']),
                                     'ClientAddress.`id`=(SELECT MAX(CA.`id`) FROM ClientAddress AS CA WHERE CA.`client_id`=ClientAddress.`client_id`)']
            queryTable = tableClient
            queryTable = queryTable.innerJoin(tableClientAddress, clientAddressJoinCond)
            queryTable = queryTable.innerJoin(tableAddress, tableAddress['id'].eq(tableClientAddress['address_id']))
            queryTable = queryTable.innerJoin(tableAddressHouse, tableAddressHouse['id'].eq(tableAddress['house_id']))
            cond = ['SUBSTR(AddressHouse.`KLADRCode`, 1, 2)=\'%s\'' % QtGui.qApp.defaultKLADR()[0:2],
                    tableClient['deleted'].eq(0),
                    tableClientAttach['deleted'].eq(0)
                    ]
            if orgId:
                cond.append(tableClientAttach['LPU_id'].eq(orgId))
            cond.append(tableAttachType['temporary'].eq(0))
            begDateAttach = db.formatDate(QDate(endDate.year(), 1, 1))
            cond.append('''IF((((ClientAttach.begDate IS NULL)
                 OR (DATE(ClientAttach.begDate)<=DATE(%s))))
                 AND (((ClientAttach.endDate IS NULL)
                 OR (DATE(ClientAttach.endDate)>=DATE(%s)))), 1, 0)''' % (begDateAttach, begDateAttach))
            queryTable = queryTable.innerJoin(tableClientAttach, tableClientAttach['client_id'].eq(tableClient['id']))
            queryTable = queryTable.innerJoin(tableAttachType, tableAttachType['id'].eq(tableClientAttach['attachType_id']))
        else:
            cond = [tableClient['deleted'].eq(0)]
            queryTable = tableClient
        fields = 'age(birthDate, %s) AS clientAge, sex AS clientSex , COUNT(Client.`id`) AS cnt' % strDate
        stmt = db.selectStmtGroupBy(queryTable, fields, cond, 'clientSex, clientAge')
        query = db.query(stmt)
        result = {}
        while query.next():
            record = query.record()
            clientAge = forceInt(record.value('clientAge'))
            clientSex = forceInt(record.value('clientSex'))
            cnt = forceInt(record.value('cnt'))
            key = clientAge, clientSex
            result[key] = result.get(key, 0) + cnt
        return result

    def getDataByContingent(self, reportData, params):
        contingentTypeId = params.get('contingentTypeId', None)
        isAttache = params.get('isAttache', False)
        if not contingentTypeId:
            return {}
        endDate = params.get('endDate', QDate())
        orgId = params.get('orgId', None)
        date = lastYearDay(endDate)
        db = QtGui.qApp.db
        tableClient = db.table('Client')
        tableClientSocStatus = db.table('ClientSocStatus')
        queryTable = tableClient.leftJoin(tableClientSocStatus, tableClientSocStatus['client_id'].eq(tableClient['id']))
        cols = 'age(Client.birthDate, %s) AS clientAge, Client.sex AS clientSex , COUNT(Client.`id`) AS cnt' % db.formatDate(date)
        cond = self.appendClientToContingentTypeCond(contingentTypeId)
        cond.append(tableClient['deleted'].eq(0))
        if isAttache:
            cond.append('SUBSTR(AddressHouse.`KLADRCode`, 1, 2) = \'%s\''%QtGui.qApp.defaultKLADR()[0:2])
            tableClientAddress = db.table('ClientAddress')
            tableAddress = db.table('Address')
            tableClientAttach = db.table('ClientAttach')
            tableAttachType = db.table('rbAttachType')
            tableAddressHouse = db.table('AddressHouse')
            clientAddressJoinCond = [tableClientAddress['client_id'].eq(tableClient['id']),
                                     'ClientAddress.`id` = (SELECT MAX(CA.`id`) FROM ClientAddress AS CA WHERE CA.`client_id` = ClientAddress.`client_id`)']
            queryTable = queryTable.innerJoin(tableClientAddress, clientAddressJoinCond)
            queryTable = queryTable.innerJoin(tableAddress, tableAddress['id'].eq(tableClientAddress['address_id']))
            queryTable = queryTable.innerJoin(tableAddressHouse, tableAddressHouse['id'].eq(tableAddress['house_id']))
            queryTable = queryTable.innerJoin(tableClientAttach, tableClientAttach['client_id'].eq(tableClient['id']))
            queryTable = queryTable.innerJoin(tableAttachType, tableAttachType['id'].eq(tableClientAttach['attachType_id']))
            cond.append(tableClientAttach['deleted'].eq(0))
            if orgId:
                cond.append(tableClientAttach['LPU_id'].eq(orgId))
            cond.append(tableAttachType['temporary'].eq(0))
            begDateAttach = db.formatDate(QDate(endDate.year(), 1, 1))
            cond.append('''IF((((ClientAttach.begDate IS NULL)
                OR (DATE(ClientAttach.begDate) <= DATE(%s))))
                AND (((ClientAttach.endDate IS NULL)
                OR (DATE(ClientAttach.endDate) >= DATE(%s)))), 1, 0)''' % (begDateAttach, begDateAttach))
        stmt = db.selectStmtGroupBy(queryTable, cols, cond, 'clientSex, clientAge')
        query = db.query(stmt)
        while query.next():
            record = query.record()
            clientAge = forceInt(record.value('clientAge'))
            clientSex = forceInt(record.value('clientSex'))
            cnt = forceInt(record.value('cnt'))
            reportRow = getAgeClass(clientAge)
            if reportRow is not None:
                reportLine = reportData[reportRow]
                if clientSex == 1:
                    reportLine[5] += cnt
                elif clientSex == 2:
                    reportLine[9] += cnt
                reportLine[1] += cnt

    def appendClientToContingentTypeCond(self, contingentTypeId):
        if not contingentTypeId:
            return []
        db = QtGui.qApp.db
        contingentOperation = forceInt(db.translate(CContingentTypeTranslator.CTTName, 'id',
                                                    contingentTypeId, 'contingentOperation'))
        contingentTypeCond = []
        if CContingentTypeTranslator.isSexAgeSocStatusEnabled(contingentOperation):
            tmp = []
            contingentTypeCond.append('Client.deleted = 0')
            sexAgeCond = CContingentTypeTranslator.getSexAgeCond(contingentTypeId)
            socStatusCond = CContingentTypeTranslator.getSocStatusCond(contingentTypeId)
            if CContingentTypeTranslator.isSexAgeSocStatusOperationType_OR(contingentOperation):
                if sexAgeCond is not None:
                    tmp.extend(sexAgeCond)
                if socStatusCond is not None:
                    tmp.extend(socStatusCond)
                contingentTypeCond.append(db.joinOr(tmp))
            else:
                if sexAgeCond is not None:
                    tmp.append(db.joinOr(sexAgeCond))
                if socStatusCond is not None:
                    tmp.append(db.joinOr(socStatusCond))
                contingentTypeCond.append(db.joinAnd(tmp))
        return contingentTypeCond
