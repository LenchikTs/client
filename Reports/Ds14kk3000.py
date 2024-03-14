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
from Reports.Report     import CReport
from Reports.ReportBase import *
from Reports.Ds14kk1000 import CDs14kkHelpers
from Ui_Ds14kkSetupDialog import Ui_ds14kkSetupDialog
from library.Utils import forceString, forceInt, forceDouble
from Reports.Ds14kk1000 import CDs14kkSetupDialog


class CReportDs14kk3000(CReport):
    def __init__(self, parent = None):
        CReport.__init__(self, parent)
        self.setTitle(u'Движение пациентов в дневных стационарах, сроки и исходы лечения')

    def getSetupDialog(self, parent):
        result = CDs14kkSetupDialog(parent)
        #self.stationaryF14DCSetupDialog = result
        return result

    def selectData(self, params):
        stmt = u'''
 select cat.id as catId, reportlines.*,
        count(distinct case when Event.isClosed and Event.orgtype = 0 then Event.id else null end) as ambClosed,
        count(distinct case when Event.isClosed and Event.orgtype = 1 then Event.id else null end) as stacClosed,
        sum(case when Event.orgtype = 0 then Event.pd else 0 end) as ambpd,
        sum(case when Event.orgtype = 1 then Event.pd else 0 end) as stacpd,
        sum(case when Event.orgtype = 0 then Event.isDeath else 0 end) as ambdeath,
        sum(case when Event.orgtype = 1 then Event.isDeath else 0 end) as stacdeath
 from (
    select 1 as id, "взрослые" as ctitle union all select 2, "дети"
 ) cat
 cross join (
     select "Всего, в том числе" as title, 1 as number, "A00" as start, "T98" as end union all
     select "некоторые инфекционные и паразитарные болезни", 2, "A00", "B99" union all
     select "новообразования", 3, "C00", "D48" union all
     select "болезни крови и кроветворных органов и отдельные нарушения, вовлекающие иммунный механизм", 4, "D50", "D89" union all
     select "Болезни эндокринной системы, расстройства питания и нарушения обмена веществ", 5, "E00", "E90" union all
     select "Психические расстройства и расстройства поведения", 6, "F00", "F99" union all
     select "Болезни нервной системы", 7, "G00", "G99" union all
     select "Болезни глаза и его придаточного аппарата", 8, "H00", "H59" union all
     select "Болезни уха и сосцевидного отростка", 9, "H60", "H95" union all
     select "Болезни системы кровообращения", 10, "I00", "I99" union all
     select "Болезни органов дыхания", 11, "J00", "J99" union all
     select "Болезни органов пищеварения", 12, "K00", "K93" union all
     select "Болезни кожи и подкожной клетчатки", 13, "L00", "L98" union all
     select "Болезни костно-мышечной системы и соединительной ткани", 14, "M00", "M99" union all
     select "Болезни мочеполовой системы", 15, "N00", "N99" union all
     select "Беременность, роды и послеродовой период", 16, "O00", "O99" union all
     select "Врождённые аномалии, пороки развития, деформации и хромосомные нарушения", 17, "Q00", "Q99" union all
     select "Симптомы, признаки и отклонения от нормы, выявленные при клинических и лабораторных исследованиях, не классифицированные в других рубриках", 18, "R00", "R99" union all
     select "Травмы, отравления и некоторые другие последствия воздействия внешних причин", 19, "S00", "T98" union all
     select "Кроме того факторы, влияющие на состояние здоровья населения и обращения в учреждения здравоохранения", 20, "Z00", "Z99"
 ) reportlines
 left join (
   select Event.id,
          Event.isClosed, Diagnosis.MKB, OrgStructure.type as orgtype,
          max(isSexAndAgeSuitable(0, DATE_SUB(NOW(),INTERVAL 18 YEAR), 0, OrgStructure_HospitalBed.age, now())) as profileAdult,
          max(isSexAndAgeSuitable(0, DATE_SUB(NOW(),INTERVAL 17 YEAR), 0, OrgStructure_HospitalBed.age, now())) as profileChild,
          WorkDays(Event.setDate, Event.execDate, EventType.weekProfileCode, mt.regionalCode) as pd,
          (Event.isClosed and (rbResult.name LIKE 'умер' or rbResult.name like 'умер в приемном покое')) as isDeath
    from Diagnosis
    left join Diagnostic on Diagnostic.diagnosis_id = Diagnosis.id
    left join Event on Event.id = Diagnostic.event_id
    left join EventType on EventType.id = Event.eventType_id
    left join rbMedicalAidType mt ON mt.id = EventType.medicalAidType_id
    left join rbResult on rbResult.id = Event.result_id
    left join OrgStructure_HospitalBed on OrgStructure_HospitalBed.id = (
        select ActionProperty_HospitalBed.value
        from Action as HospitalAction
        left join ActionPropertyType on ActionPropertyType.name = 'койка'
        and ActionPropertyType.actionType_id = HospitalAction.actionType_id and ActionPropertyType.deleted = 0
        left join ActionProperty on ActionProperty.type_id = ActionPropertyType.id
            and ActionProperty.action_id = HospitalAction.id and ActionProperty.deleted = 0
        left join ActionProperty_HospitalBed on ActionProperty_HospitalBed.id = ActionProperty.id
        where HospitalAction.id = (SELECT MAX(A.id) FROM Action A
                    WHERE A.event_id = Event.id AND A.deleted = 0 AND A.actionType_id IN (
                                    SELECT AT.id
                                    FROM ActionType AT
                                    WHERE AT.flatCode ='moving'
                                        AND AT.deleted = 0)
                                    )

        )
    left join OrgStructure on OrgStructure_HospitalBed.master_id = OrgStructure.id
    left join rbHospitalBedShedule on rbHospitalBedShedule.id = OrgStructure_HospitalBed.schedule_id
    left join Contract on  Contract.id = Event.contract_id
   where
    OrgStructure.type in (0,1) and rbHospitalBedShedule.code = 2 and Event.deleted = 0
    and %(cond)s
   group by Event.id

 ) Event on (Event.MKB between reportlines.start and reportlines.end) and ((cat.id = 1 and Event.profileAdult) or (cat.id = 2 and Event.profileChild))
 group by cat.id, reportlines.number
 order by cat.id asc, reportlines.number asc

        '''
        db = QtGui.qApp.db
        st = stmt % {'cond': CDs14kkHelpers.getCond(params, 2)}
        return db.query(st)


    def build(self, params):

        reportAdult = [['', i+1, ''] + [0] * 9 for i in range(20)]
        reportChild = [['', i + 1, ''] + [0] * 9 for i in range(20)]

        def processQuery(query):
            while query.next():
                record = query.record()
                isAdult = forceInt(record.value("catId")) == 1
                isChild = forceInt(record.value("catId")) == 2
                if isAdult:
                    report = reportAdult
                else:
                    report = reportChild
                number = forceInt(record.value('number'))
                title = forceString(record.value('title'))
                range = u'%s-%s' % (forceString(record.value('start')), forceString(record.value('end')))
                reportline = report[number - 1]
                reportline[0] = title
                reportline[2] = range
                reportline[3] += forceInt(record.value('stacClosed'))
                reportline[4] += forceInt(record.value('stacpd'))
                reportline[5] += forceInt(record.value('stacdeath'))
                reportline[6] += forceInt(record.value('ambClosed'))
                reportline[7] += forceInt(record.value('ambpd'))
                reportline[8] += forceInt(record.value('ambdeath'))
                reportline[9] = u'-'
                reportline[10] = u'-'
                reportline[11] = u'-'
        processQuery(self.selectData(params))
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.setBlockFormat(CReportBase.AlignCenter)
        cursor.insertText(u'3. Движение пациентов в дневных стационарах, сроки и исходы лечения')
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportSubTitle)
        cursor.insertText(u'3.1 Дневные стационары для взрослых')
        CDs14kkHelpers.splitTitle(cursor,u'(3000)', u'Коды по ОКЕИ: человек - 792, еденица - 642')
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        tableColumns = [
            ('15%',[u'Наименование классов МКБ-10'], CReportBase.AlignLeft),
            ('5%', [u'№ строки'], CReportBase.AlignRight),
            ('8%', [u'Код по МКБ-10'], CReportBase.AlignCenter),
            ('8%', [u'Дневные стационары медицинских организаций, оказывающих медицинскую помощь', u'в стационарных условиях', u'выписано пациентов'], CReportBase.AlignRight),
            ('8%', [u'', u'', u'Проведено пациенто-дней'], CReportBase.AlignRight),
            ('8%', [u'', u'', u'умерло'], CReportBase.AlignRight),
            ('8%', [u'', u'в амбулаторных условиях', u'выписано пациентов'], CReportBase.AlignRight),
            ('8%', [u'', u'', u'Проведено пациенто-дней'], CReportBase.AlignRight),
            ('8%', [u'', u'', u'умерло'], CReportBase.AlignRight),
            ('8%', [u'', u'на дому', u'выписано пациентов'], CReportBase.AlignRight),
            ('8%', [u'', u'', u'Проведено пациенто-дней'], CReportBase.AlignRight),
            ('8%', [u'', u'', u'умерло'], CReportBase.AlignRight)
            ]

        table = createTable(cursor, tableColumns)
        autoMergeHeader(table, tableColumns)
        row = table.addRow()
        for i in range(12):
            table.setText(row, i, i+1, blockFormat=CReportBase.AlignCenter)
        for line in reportAdult:
            row = table.addRow()
            for i in range(12):
                table.setText(row, i, line[i])


        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportSubTitle)
        cursor.insertText(u'3.1 Дневные стационары для детей')
        CDs14kkHelpers.splitTitle(cursor, u'(3500)', u'Коды по ОКЕИ: человек - 792, еденица - 642')

        cursor.insertBlock()
        table = createTable(cursor, tableColumns)
        autoMergeHeader(table, tableColumns)
        row = table.addRow()
        for i in range(12):
            table.setText(row, i, i+1, blockFormat=CReportBase.AlignCenter)
        for line in reportChild:
            row = table.addRow()
            for i in range(12):
                table.setText(row, i, line[i])
        CDs14kkHelpers.writeFooter(cursor)
        return doc