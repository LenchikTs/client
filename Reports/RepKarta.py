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
from PyQt4.QtCore import *
from Reports.Report import *
from Reports.ReportBase import *
from Orgs.Utils import getOrgStructureDescendants

from library.Utils import *
from Reports.ReportForm131_1000_SetupDialog import CReportForm131_1000_SetupDialog


class CKarta_Expert(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Сводка карты экспертной оценки')

    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setEventTypeVisible(False)
        result.setOnlyPermanentAttachVisible(False)
        result.setTitle(self.title())
        result.setOrgStructureVisible(True)
        result.setSexVisible(True)
        result.lblSex.setText(u'В разрезе')
        result.cmbSex.addItem(u'Оценка врачебная комиссия')
        result.cmbSex.setItemText(1, u'Оценка зав. отделением')
        result.cmbSex.setItemText(2, u'Оценка зам. главного врача')
        result.cmbSex.setItemText(0, u'Карта экспертной оценки')
        for i in xrange(result.gridLayout.count()):
            spacer = result.gridLayout.itemAt(i)
            if isinstance(spacer, QtGui.QSpacerItem):
                itemposition = result.gridLayout.getItemPosition(i)
                if itemposition != (29, 0, 1, 1) and itemposition != (8, 1, 1, 3):
                    result.gridLayout.removeItem(spacer)
        result.resize(400, 10)
        return result

    def selectData(self, params, codeAT):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        org = params.get('orgStructureId', None)
        if org:
            orgStructureList = getOrgStructureDescendants(org)
            orgStructureSet = '('
            for orgStruct in orgStructureList:
                orgStructureSet = orgStructureSet + forceString(orgStruct) + ', '
            orgStructureSet = orgStructureSet[0:-2] + ')'
            orgStructureSetWhere = orgStructureSet
            orgStructureIdWhere = ' and os.id in %s' % orgStructureSetWhere
        else:
            orgStructureIdWhere = ''
        db = QtGui.qApp.db
        stmt = u'''SELECT e.id AS event_id,os.name,DATE(a.endDate) AS date FROM Event e
  LEFT JOIN Action a ON e.id = a.event_id
  LEFT JOIN ActionType at ON a.actionType_id = at.id

left join ActionPropertyType apt on apt.actionType_id = at.id and apt.name = 'Отделение' and apt.deleted = 0 
    left join ActionProperty ap on ap.action_id = a.id and ap.type_id = apt.id
    left join ActionProperty_OrgStructure sn on sn.id = ap.id
LEFT JOIN OrgStructure os ON sn.value = os.id

  WHERE at.code = 'karta_stc'
  AND a.deleted=0 AND at.deleted=0 AND e.deleted=0 and date(a.endDate) BETWEEN DATE(%(begDate)s) AND DATE(%(endDate)s) %(orgStructureId)s
  AND EXISTS(SELECT a1.id FROM Action a1 
  inner JOIN ActionType at1 ON a1.actionType_id = at1.id
  WHERE at1.code='%(codeAT)s' AND e.id=a1.event_id);
        ''' % {'begDate': db.formatDate(begDate),
               'endDate': db.formatDate(endDate),
               'orgStructureId': orgStructureIdWhere,
               'codeAT': codeAT
               }
        return db.query(stmt)

    def selectAsses(self, a, b):
        event = a
        if b == 'karta_stc':
            codeAT = 'at.code  in ("quality_zav", "quality_zamgl", "quality_vk")'
        else:
            codeAT = 'at.code  = "%s"' % b


        stmt = u'''SELECT e.id,
         
          count(a.id) AS cn,
  SUM(sn.value) AS a1, SUM(sn1.value) AS a2, SUM(sn2.value) AS a3, SUM(sn3.value) AS b1, SUM(sn4.value) AS b2, 
  SUM(sn5.value) AS v1, SUM(sn6.value) AS v2, SUM(sn7.value) AS v3, SUM(sn8.value) AS g, SUM(sn9.value) AS d,
  ((sn.value)+(sn1.value)+(sn2.value)+(sn3.value)+(sn4.value)+(sn5.value)+(sn6.value)+(sn7.value)+(sn8.value)+(sn9.value))/10 AS asses 
  
         
         FROM Event e
  LEFT JOIN Action a ON e.id = a.event_id
  LEFT JOIN ActionType at ON a.actionType_id = at.id

left join ActionPropertyType apt on apt.actionType_id = at.id and apt.name = '1. Объем и качество обсл. (сбор жалоб, анамнеза, физикальных данн. конс. спец-в, осмотр зав. отделением)' and apt.deleted = 0 
    left join ActionProperty ap on ap.action_id = a.id and ap.type_id = apt.id
    left join ActionProperty_Double sn on sn.id = ap.id

left join ActionPropertyType apt1 on apt1.actionType_id = at.id and apt1.name = '2. Объем лабораторных обследований в соответствии со стандартами' and apt1.deleted = 0 
    left join ActionProperty ap1 on ap1.action_id = a.id and ap1.type_id = apt1.id
    left join ActionProperty_Double sn1 on sn1.id = ap1.id

left join ActionPropertyType apt2 on apt2.actionType_id = at.id and apt2.name = '3. Объем инструментальных обследований в соответствии со стандартами' and apt2.deleted = 0 
    left join ActionProperty ap2 on ap2.action_id = a.id and ap2.type_id = apt2.id
    left join ActionProperty_Double sn2 on sn2.id = ap2.id

left join ActionPropertyType apt3 on apt3.actionType_id = at.id and apt3.name = '1. Диагноз поставлен в соответствии с правилами классификации (фаза, стадия процесса, локализация, нарушение функции, соп. заб. ' and apt3.deleted = 0 
    left join ActionProperty ap3 on ap3.action_id = a.id and ap3.type_id = apt3.id
    left join ActionProperty_Double sn3 on sn3.id = ap3.id

left join ActionPropertyType apt4 on apt4.actionType_id = at.id and apt4.name = '2. Обоснование диагноза' and apt4.deleted = 0 
    left join ActionProperty ap4 on ap4.action_id = a.id and ap4.type_id = apt4.id
    left join ActionProperty_Double sn4 on sn4.id = ap4.id

left join ActionPropertyType apt5 on apt5.actionType_id = at.id and apt5.name = '1. Адекватность лечения по диагнозу' and apt5.deleted = 0 
    left join ActionProperty ap5 on ap5.action_id = a.id and ap5.type_id = apt5.id
    left join ActionProperty_Double sn5 on sn5.id = ap5.id

left join ActionPropertyType apt6 on apt6.actionType_id = at.id and apt6.name = '2. Сроки лечения' and apt6.deleted = 0 
    left join ActionProperty ap6 on ap6.action_id = a.id and ap6.type_id = apt6.id
    left join ActionProperty_Double sn6 on sn6.id = ap6.id

left join ActionPropertyType apt7 on apt7.actionType_id = at.id and apt7.name = '3. Цель госпитализации, эффективность лечения' and apt7.deleted = 0 
    left join ActionProperty ap7 on ap7.action_id = a.id and ap7.type_id = apt7.id
    left join ActionProperty_Double sn7 on sn7.id = ap7.id

left join ActionPropertyType apt8 on apt8.actionType_id = at.id and apt8.name = 'Г. Преемственность этапов (ПЭ)' and apt8.deleted = 0 
    left join ActionProperty ap8 on ap8.action_id = a.id and ap8.type_id = apt8.id
    left join ActionProperty_Double sn8 on sn8.id = ap8.id

left join ActionPropertyType apt9 on apt9.actionType_id = at.id and apt9.name = 'Д. Оформление документации' and apt9.deleted = 0 
    left join ActionProperty ap9 on ap9.action_id = a.id and ap9.type_id = apt9.id
    left join ActionProperty_Double sn9 on sn9.id = ap9.id

  WHERE %(codeAT)s AND a.deleted=0 AND at.deleted=0 AND e.deleted=0 AND e.id= %(event)s
  group by e.id
        ''' % {'event': event,
               'codeAT': codeAT
               }
        db = QtGui.qApp.db
        return db.query(stmt)

    def getDescription(self, params):
        db = QtGui.qApp.db
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        paramCodeAT = params.get('sex', 0)
        orgStructureId = params.get('orgStructureId', None)

        rows = []
        rows.append(dateRangeAsStr(u'за период', begDate, endDate))

        if paramCodeAT == 2:
            rows.append(u'Оценка зам. главного врача')
        elif paramCodeAT == 3:
            rows.append(u'Оценка врачебной комиссии')
        elif paramCodeAT == 1:
            rows.append(u'Оценка зав. отделением')
        else:
            rows.append(u'Карта экспертной оценки')
        if orgStructureId:
            rows.append(u'подразделение: ' + getOrgStructureFullName(orgStructureId))

        rows.append(u'отчёт составлен: ' + forceString(QDateTime.currentDateTime()))
        return rows

    def build(self, params):
        reportRowSize = 15
        reportData = {}
        paramCodeAT = params.get('sex', 0)
        if paramCodeAT == 0:
            codeAT = 'karta_stc'
        elif paramCodeAT == 1:
            codeAT = 'quality_zav'
        elif paramCodeAT == 2:
            codeAT = 'quality_zamgl'
        else:
            codeAT = 'quality_vk'

        def processQuery(query):
            nameTemp = 0
            assesTemp = 0
            asses = 0

            while query.next():
                record = query.record()
                event_id = forceInt(record.value('event_id'))  # name
                name = forceString(record.value('name')) if forceString(
                    record.value('name')) else u'Отделение не заполнено'

                queryAsses = self.selectAsses(event_id, codeAT)
                while queryAsses.next():
                    tempEvent = False
                    recordAsses = queryAsses.record()
                    cn = forceInt(recordAsses.value('cn'))  # name
                    a1 = forceDouble(recordAsses.value('a1'))
                    a2 = forceDouble(recordAsses.value('a2'))
                    a3 = forceDouble(recordAsses.value('a3'))
                    b1 = forceDouble(recordAsses.value('b1'))
                    b2 = forceDouble(recordAsses.value('b2'))
                    v1 = forceDouble(recordAsses.value('v1'))
                    v2 = forceDouble(recordAsses.value('v2'))
                    v3 = forceDouble(recordAsses.value('v3'))
                    g = forceDouble(recordAsses.value('g'))
                    d = forceDouble(recordAsses.value('d'))
                    asses = forceDouble(recordAsses.value('asses'))  # name

                if (nameTemp == 0 or name == nameTemp):
                    nameTemp = name
                    assesTemp += asses
                else:
                    assesTemp = 0
                    nameTemp = name
                    assesTemp += asses

                key = (name,)
                reportLine = reportData.setdefault(key, [0] * reportRowSize)

                reportLine[0] += 1
                if a1+a2+a3 < 3 * cn:
                    reportLine[1] += 1
                    tempEvent = True
                if b1 + b2 < 2 * cn:
                    reportLine[3] += 1
                    tempEvent = True
                if v1 + v2 + v3 < 4 * cn:
                    reportLine[5] += 1
                    tempEvent = True
                if g < 0.5 * cn:
                    reportLine[7] += 1
                    tempEvent = True
                if d < 0.5 * cn:
                    reportLine[9] += 1
                    tempEvent = True


                if tempEvent:
                    reportLine[14] += 1
                reportLine[13] = round(assesTemp/reportLine[0], 2)


                reportLine[2] = round(float(reportLine[1]) / float(reportLine[0]) * 100, 2)
                reportLine[4] = round(float(reportLine[3]) / float(reportLine[0]) * 100, 2)
                reportLine[6] = round(float(reportLine[5]) / float(reportLine[0]) * 100, 2)
                reportLine[8] = round(float(reportLine[7]) / float(reportLine[0]) * 100, 2)
                reportLine[10] = round(float(reportLine[9]) / float(reportLine[0]) * 100, 2)
                reportLine[11] = reportLine[0]-reportLine[14]
                reportLine[12] = round(float(reportLine[0]-reportLine[11]) / float(reportLine[0]) * 100, 2)
                #    table.setText(row, 3, round(float(reportLine[1])/float(reportLine[0])*100, 2))
                #    table.setText(row, 5, round(float(reportLine[3])/float(reportLine[0])*100, 2))
                #    table.setText(row, 7, round(float(reportLine[5])/float(reportLine[0])*100, 2))
                #    table.setText(row, 9, round(float(reportLine[7])/float(reportLine[0])*100, 2))
                ##    table.setText(row, 11, round(float(reportLine[9])/float(reportLine[0])*100, 2))
                #   table.setText(row, 12, reportLine[0]-reportLine[11])
                #   table.setText(row, 13, round(float(reportLine[0]-reportLine[11]) / float(reportLine[0]) * 100, 2))
                #   table.setText(row, 14, reportLine[13])



            #   reportLine[0] += kd
            #   reportLine[1] += sum
            #  reportLine[2] += cnt

        query = self.selectData(params, codeAT)
        processQuery(query)

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        tableColumns = [
            ('20%', [u'Отделения (службы), или Ф.И.О. врачей', u'', u''], CReportBase.AlignLeft),
            ('10%', [u'Количество проведенных экспертиз', u'', u'абс.'], CReportBase.AlignCenter),
            ('5%',
             [u'Количество карт с выявленными дефектами медицинской помощи (абс. и %)', u'Диагностических мероприятий',
              u'абс.'], CReportBase.AlignCenter),
            ('5%', [u'', u'', u'%'], CReportBase.AlignCenter),
            ('5%', [u'', u'Полноты диагноза', u'абс.'], CReportBase.AlignCenter),
            ('5%', [u'', u'', u'%'], CReportBase.AlignCenter),
            ('5%', [u'', u'Лечебно-профилактических мероприятий', u'абс.'], CReportBase.AlignCenter),
            ('5%', [u'', u'', u'%'], CReportBase.AlignCenter),
            ('5%', [u'', u'Преемственности этапов', u'абс.'], CReportBase.AlignCenter),
            ('5%', [u'', u'', u'%'], CReportBase.AlignCenter),
            ('5%', [u'', u'Оформление медицинской документации', u'абс.'], CReportBase.AlignCenter),
            ('5%', [u'', u'', u'%'], CReportBase.AlignCenter),
            ('5%',
             [u'Количество медицинских карт без дефектов медицинской помощи от общего числа экспертиз', u'', u'абс.'],
             CReportBase.AlignCenter),
            ('5%', [u'', u'', u'%'], CReportBase.AlignCenter),
            ('10%', [u'Коэффициент Уровня качества лечения (УКЛ)', u'', u''], CReportBase.AlignCenter)
        ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 3, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 1, 10)
        table.mergeCells(1, 2, 1, 2)
        table.mergeCells(1, 4, 1, 2)
        table.mergeCells(1, 6, 1, 2)
        table.mergeCells(1, 8, 1, 2)
        table.mergeCells(1, 10, 1, 2)
        table.mergeCells(0, 12, 2, 2)
        table.mergeCells(0, 14, 3, 1)
        for col in xrange(reportRowSize):
            table.mergeCells(0, col, 1, 1)

        totalByReport = [0] * reportRowSize
        colsShift = 1

        keys = reportData.keys()
        keys.sort()

        def drawTotal(table, total, text, count):

            row = table.addRow()

            table.setText(row, 0, text, CReportBase.TableHeader)
            table.mergeCells(row, 0, 1, 1)
            for col in xrange(reportRowSize):

                if (col < 14 ):

                    if total[col] == 0 or col == 0:
                        table.setText(row, col + colsShift, total[col], fontBold=True)
                    else:
                        if col in (1,3,5,7,9,11):
                            table.setText(row, col + colsShift, round(float(total[col])/float(count), 3), fontBold=True)
                        else:
                            table.setText(row, col + colsShift, round(total[col]/count, 2), fontBold=True)


        count = 0
        for key in keys:

            name = key[0]

            reportLine = reportData[key]

            row = table.addRow()
            table.setText(row, 0, name)
        #    table.setText(row, 3, round(float(reportLine[1])/float(reportLine[0])*100, 2))
        #    table.setText(row, 5, round(float(reportLine[3])/float(reportLine[0])*100, 2))
        #    table.setText(row, 7, round(float(reportLine[5])/float(reportLine[0])*100, 2))
        #    table.setText(row, 9, round(float(reportLine[7])/float(reportLine[0])*100, 2))
        ##    table.setText(row, 11, round(float(reportLine[9])/float(reportLine[0])*100, 2))
         #   table.setText(row, 12, reportLine[0]-reportLine[11])
         #   table.setText(row, 13, round(float(reportLine[0]-reportLine[11]) / float(reportLine[0]) * 100, 2))
         #   table.setText(row, 14, reportLine[13])
            count += 1
            for col in xrange(reportRowSize):
                if (col < 14 ):
                    table.setText(row, col + colsShift, reportLine[col])
                totalByReport[col] = totalByReport[col] + reportLine[col]

        # total
        drawTotal(table, totalByReport, u'Итого', count);
        return doc

