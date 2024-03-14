# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2015 SAMSON Group. All rights reserved.
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
from Reports.Report import CReport
from Reports.ReportSetupDialog import CReportSetupDialog
from Orgs.Utils import getOrgStructurePersonIdList
from Reports.ReportBase import CReportBase, createTable

from library.Utils import forceInt, forceString


class CSvedVipis(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Сведения о выбывших')

    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setTitle(self.title())
        result.setOrgStructureVisible(True)
        result.setFinanceVisible(True)
        result.setEventTypeVisible(False)
        result.setOnlyPermanentAttachVisible(False)
        for i in xrange(result.gridLayout.count()):
            spacer = result.gridLayout.itemAt(i)
            if isinstance(spacer, QtGui.QSpacerItem):
                result.gridLayout.removeItem(spacer)
        result.resize(400, 10)
        return result

    def selectData(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        orgStructureId = params.get('orgStructureId', None)
        financeId = params.get('financeId', None)
        db = QtGui.qApp.db
        condOrgStructure = u''
        if orgStructureId:
            personIdList = getOrgStructurePersonIdList(orgStructureId)
            if personIdList:
                condOrgStructure = u''' AND e.execPerson_id IN (%s)''' % (u','.join(str(personId) for personId in personIdList if personId))
        if financeId:
            condFinanceId = ' and Contract.id IS NOT NULL AND Contract.deleted=0 AND Contract.finance_id = %d' % financeId
        else:
            condFinanceId = ''
        db = QtGui.qApp.db
        stmt = u'''SELECT t.org AS org, t.prof AS prof, SUM(t.cont) AS cont, SUM(t.den) AS den,
SUM(t.gor) AS gor,
SUM(CASE WHEN t.gor = 1 THEN t.den else 0 END) AS gor_day,
SUM(CASE WHEN t.gor = 0 THEN 1 ELSE 0 END) AS sel,
SUM(CASE WHEN t.gor = 0 THEN t.den else 0 END) AS sel_day,
SUM(CASE WHEN t.kray = 1 AND t.gor=1 THEN 1 else 0 END) AS kraygor,
SUM(CASE WHEN t.kray = 1 AND t.gor=1 THEN t.den else 0 END) AS kraygor_day,
SUM(CASE WHEN t.kray = 1 AND t.gor=0 THEN 1 else 0 END) AS kraysel,
SUM(CASE WHEN t.kray = 1 AND t.gor=0 THEN t.den else 0 END) AS kraysel_day,
SUM(CASE WHEN t.kray = 0 AND t.gos=1 THEN 1 else 0 END) AS inkray,
SUM(CASE WHEN t.kray = 0 AND t.gos=1 THEN t.den else 0 END) AS inkray_day,
SUM(CASE WHEN t.gos = 0 THEN 1 else 0 END) AS inostr,
SUM(CASE WHEN t.gos = 0 THEN t.den else 0 END) AS inostr_day,
SUM(CASE WHEN t.countDeath = 1 THEN 1 else 0 END) AS countDeath,
SUM(CASE WHEN t.countTransfer = 1 THEN 1 else 0 END) AS countTransfer
from (
SELECT OrgStructure.name as org,hbp.name AS prof,
(EXISTS(SELECT APS.id
FROM ActionProperty AS AP
INNER JOIN ActionPropertyType AS APT ON AP.type_id=APT.id
INNER JOIN ActionProperty_String AS APS ON APS.id=AP.id
WHERE APT.deleted=0 AND AP.deleted=0 AND APT.name LIKE 'Исход госпитализации'
AND (APS.value LIKE '%%переведен%%' OR APS.value LIKE '%%выписан%%')
)) AS cont,
g.day as den,
case when isClientVillager(e.client_id)=1 OR isClientVillager(e.client_id) IS null then 1 else 0 END  AS gor,
case when Insurer.area like "23%%" then 1 else 0 END AS kray,
case when cd.documentType_id in (SELECT dt1.id FROM rbDocumentType dt1 WHERE dt1.regionalCode in ('14','3')) OR cd.id IS null
then 1 else 0 END AS gos,
(EXISTS(SELECT APS.id
FROM ActionProperty AS AP
INNER JOIN ActionPropertyType AS APT ON AP.type_id=APT.id
LEFT JOIN Action a ON AP.action_id = a.id  AND a.deleted=0
INNER JOIN ActionProperty_String AS APS ON APS.id=AP.id
WHERE AP.action_id=a.id AND a.event_id=e.id and APT.deleted=0 AND AP.deleted=0 AND APT.name LIKE 'Исход госпитализации'
AND (APS.value LIKE '%%умер%%' OR APS.value LIKE '%%смерть%%')
)) AS countDeath,
(EXISTS(SELECT APS.id
FROM ActionProperty AS AP
INNER JOIN ActionPropertyType AS APT ON AP.type_id=APT.id
LEFT JOIN Action a ON AP.action_id = a.id  AND a.deleted=0
INNER JOIN ActionProperty_String AS APS ON APS.id=AP.id
WHERE AP.action_id=a.id AND a.event_id=e.id and APT.deleted=0 AND AP.deleted=0 AND APT.name LIKE 'Исход госпитализации'
AND (APS.value LIKE '%%переведен%%')
)) AS countTransfer
FROM Action a
LEFT JOIN Event e ON e.id = a.event_id  AND e.deleted=0 %(condOrgStructure)s
LEFT JOIN EventType et ON et.id = e.eventType_id AND et.deleted=0
LEFT JOIN ActionProperty ap ON a.id = ap.action_id AND ap.deleted=0
LEFT JOIN ActionProperty_HospitalBed aphb ON ap.id = aphb.id
LEFT JOIN OrgStructure_HospitalBed oshb ON aphb.value = oshb.id
LEFT JOIN OrgStructure ON oshb.master_id = OrgStructure.id AND OrgStructure.name IS NOT NULL AND OrgStructure.name!=''
left join OrgStructure as Parent1 on Parent1.id = OrgStructure.parent_id
                left join OrgStructure as Parent2 on Parent2.id = Parent1.parent_id
                left join OrgStructure as Parent3 on Parent3.id = Parent2.parent_id
                left join OrgStructure as Parent4 on Parent4.id = Parent3.parent_id
                left join OrgStructure as Parent5 on Parent5.id = Parent4.parent_id
left join ClientPolicy on ClientPolicy.id = getClientPolicyIdForDate(e.client_id, 1, e.execDate, e.id)
left join Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
LEFT JOIN ClientDocument cd ON e.client_id=cd.client_id AND cd.deleted=0 AND 
  cd.id=(SELECT MAX(cli.id) FROM ClientDocument cli 
  LEFT JOIN rbDocumentType dt ON cli.documentType_id = dt.id
  LEFT JOIN rbDocumentTypeGroup dtg ON dt.group_id = dtg.id
  WHERE dtg.code='1')
LEFT JOIN Contract ON e.contract_id = Contract.id
LEFT JOIN rbHospitalBedProfile hbp ON oshb.profile_id = hbp.id
LEFT JOIN (SELECT WorkDays(e.setDate, e.execDate, et.weekProfileCode, mat.regionalCode) AS day,
          isClientVillager(e.client_id) AS telo,e.id AS ev FROM Event e
          LEFT JOIN EventType et ON e.eventType_id = et.id
          LEFT JOIN rbMedicalAidType mat ON et.medicalAidType_id = mat.id
          WHERE DATE(e.execDate) BETWEEN %(begDate)s AND %(endDate)s) g ON g.ev=e.id
WHERE OrgStructure.name IS NOT NULL AND a.id = (
            SELECT MAX(A.id)
            FROM Action A
            WHERE A.event_id = e.id AND
                      A.deleted = 0 AND
                      A.actionType_id IN (
                            SELECT AT.id
                            FROM ActionType AT
                            WHERE AT.flatCode ='moving'
                                AND AT.deleted = 0
                      )
        ) %(condFinanceId)s and DATE(e.execDate) BETWEEN %(begDate)s AND %(endDate)s ) t
GROUP BY t.org, t.prof
            ''' % dict(begDate=db.formatDate(begDate),
                       endDate=db.formatDate(endDate),
                       condOrgStructure=condOrgStructure,
                       condFinanceId=condFinanceId
                       )
        db = QtGui.qApp.db
        return db.query(stmt)

    def build(self, params):
        reportRowSize = 16
        reportData = {}

        def processQuery(query):
            while query.next():
                record = query.record()
                org = forceString(record.value('org'))
                prof = forceString(record.value('prof'))
                cont = forceInt(record.value('cont'))
                den = forceInt(record.value('den'))
                gor = forceInt(record.value('gor'))
                gor_day = forceInt(record.value('gor_day'))
                sel = forceInt(record.value('sel'))
                sel_day = forceInt(record.value('sel_day'))
                kraygor = forceInt(record.value('kraygor'))
                kraygor_day = forceInt(record.value('kraygor_day'))
                kraysel = forceInt(record.value('kraysel'))
                kraysel_day = forceInt(record.value('kraysel_day'))
                inkray = forceInt(record.value('inkray'))
                inkray_day = forceInt(record.value('inkray_day'))
                inostr = forceInt(record.value('inostr'))
                inostr_day = forceInt(record.value('inostr_day'))
                countTransfer = forceInt(record.value('countTransfer'))
                countDeath = forceInt(record.value('countDeath'))

                key = (org, prof)
                reportLine = reportData.setdefault(key, [0]*reportRowSize)
                reportLine[0] += cont
                reportLine[1] += den
                reportLine[2] += gor
                reportLine[3] += gor_day
                reportLine[4] += sel
                reportLine[5] += sel_day
                reportLine[6] += kraygor
                reportLine[7] += kraygor_day
                reportLine[8] += kraysel
                reportLine[9] += kraysel_day
                reportLine[10] += inkray
                reportLine[11] += inkray_day
                reportLine[12] += inostr
                reportLine[13] += inostr_day
                reportLine[14] += countTransfer
                reportLine[15] += countDeath
        query = self.selectData(params)
        processQuery(query)

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        tableColumns = [
            ('10%', [u'Отделение/профиль койки'], CReportBase.AlignLeft),
            ('5%', [u'Всего выбыло'], CReportBase.AlignLeft),
            ('5%', [u'Всего койко-дней(пациенто-дней)'], CReportBase.AlignLeft),
            ('5%', [u'Муниципальное образование', u'Городские'], CReportBase.AlignLeft),
            ('5%', [u'', u'к/дни'], CReportBase.AlignLeft),
            ('5%', [u'', u'Сельские'], CReportBase.AlignLeft),
            ('5%', [u'', u'к/дни'], CReportBase.AlignLeft),
            ('5%', [u'Краевые', u'Городские'], CReportBase.AlignLeft),
            ('5%', [u'', u'к/дни'], CReportBase.AlignLeft),
            ('5%', [u'', u'Сельские'], CReportBase.AlignLeft),
            ('5%', [u'', u'к/дни'], CReportBase.AlignLeft),
            ('5%', [u'Инокраевые', u'выбыло'], CReportBase.AlignLeft),
            ('5%', [u'', u'к/дни'], CReportBase.AlignLeft),
            ('5%', [u'Иностранные граждане', u'выбыло'], CReportBase.AlignLeft),
            ('5%', [u'', u'к/дни'], CReportBase.AlignLeft),
            ('10%', [u'в т.ч. переведено в др. стационары'], CReportBase.AlignLeft),
            ('10%', [u'в т.ч. умерло'], CReportBase.AlignLeft),
            ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 2, 1)
        table.mergeCells(0, 3, 1, 4)
        table.mergeCells(0, 7, 1, 4)
        table.mergeCells(0, 11, 1, 2)
        table.mergeCells(0, 13, 1, 2)
        table.mergeCells(0, 15, 2, 1)
        table.mergeCells(0, 16, 2, 1)
        for col in xrange(reportRowSize):
            table.mergeCells(0, col, 1, 1)

        totalBynum = [0]*reportRowSize
        totalByReport = [0]*reportRowSize
        prevnum = None
        prevnu = None
        colsShift = 1
        keys = reportData.keys()
        keys.sort()

        def drawTotal(table,  total,  text):

            row = table.addRow()

            table.setText(row, 0, text, CReportBase.TableHeader, CReportBase.AlignRight)
            table.mergeCells(row, 0, 1, 1)
            for col in xrange(reportRowSize):
                if (col < 16):
                    table.setText(row, col + colsShift, total[col], fontBold=True)
        for key in keys:
            org = key[0]
            prof = key[1]

            reportLine = reportData[key]
            if prevnum and prevnum != org:
                drawTotal(table,  totalBynum, u'Итого по отделению')
                totalBynum = [0]*reportRowSize

            if prevnum != org:
                row = table.addRow()
                table.setText(row, 0, org, CReportBase.TableHeader)
                table.mergeCells(row, 0, 1, 17)

            if prevnu == prof and prevnum != org:
                row = table.addRow()
                table.setText(row, 0, prof)

            if prevnu != prof:
                row = table.addRow()
                table.setText(row, 0, prof)

            for col in xrange(reportRowSize):
                if (col < 16):
                    table.setText(row, col + colsShift, reportLine[col])
                totalByReport[col] = totalByReport[col] + reportLine[col]
                totalBynum[col] = totalBynum[col] + reportLine[col]
            prevnum = org
            prevnu = prof

        drawTotal(table,  totalBynum, u'Итого по отделению')
        drawTotal(table,  totalByReport, u'ИТОГО:')
        return doc
