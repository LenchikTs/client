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
from Events.EventInfo import CDiagnosticInfo
from Reports.Report import *
from Reports.ReportBase import *
from Orgs.Utils import getOrgStructureDescendants
from library.PrintInfo import CInfoContext

from library.Utils import *


class CForm035(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'035')

    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setEventTypeVisible(False)
        result.setOnlyPermanentAttachVisible(False)
        result.setNoteUETVisible(True)
        result.setTitle(self.title())
        result.setOrgStructureVisible(True)
        result.setEventStatusVisible(False)
        result.cmbNoteUET.setVisible(True)
        result.lblNoteUET.setVisible(True)
        result.lblNoteUET.setText(u'Вид и предмет экспертизы')
        result.lblEventStatus.setText(u'Характеристика случая')
        db = QtGui.qApp.db
        stmt = u'''SELECT apt.valueDomain FROM ActionPropertyType apt
          WHERE apt.actionType_id IN (SELECT id from ActionType at
          WHERE at.flatCode  = 'form035' AND at.deleted=0) AND apt.typeName='string' AND apt.name="Характеристика случая экспертизы"'''
        query = db.query(stmt)
        if query.next():
            rec = forceString(query.record().value(0))
            rec = rec.replace("u'", '')
            rec = rec.replace("'", '')
            rec = rec.replace(",*", '')
            self.rec = rec.split(",")
        if query.record().value(0) != '':

            for i in xrange(len(self.rec) - 2):
                result.cmbEventStatus.addItem(u'')
            result.cmbEventStatus.setItemText(0, u'Не задано')
            for i, item in enumerate(self.rec):
                if i == 0:
                    result.cmbEventStatus.setItemText(0, u'Не задано')
                    result.cmbEventStatus.setItemText(1, item)
                else:
                    result.cmbEventStatus.setItemText(i + 1, item)

        stmt = u'''SELECT apt.valueDomain FROM ActionPropertyType apt
          WHERE apt.actionType_id IN (SELECT id from ActionType at
          WHERE at.flatCode  = 'form035' AND at.deleted=0) AND apt.typeName='string' AND apt.name="Вид и предмет экспертизы"'''
        query = db.query(stmt)
        if query.next():
            recExpert = forceString(query.record().value(0))
            recExpert = recExpert.replace("u'", '')
            recExpert = recExpert.replace("'", '')
            recExpert = recExpert.replace(",*", '')
            self.recExpert = recExpert.split(",")
        if query.record().value(0) != '':

            for i in xrange(len(self.recExpert) - 1):
                result.cmbNoteUET.addItem(u'')
            result.cmbNoteUET.setItemText(0, u'Не задано')
            for i, item in enumerate(self.recExpert):
                if i == 0:
                    result.cmbNoteUET.setItemText(0, u'Не задано')
                    result.cmbNoteUET.setItemText(1, item)
                else:
                    result.cmbNoteUET.setItemText(i + 1, item)

            result.setSexVisible(True)
            result.lblSex.setText(u'Тип журнала')
            result.cmbSex.addItem(u'')
            result.cmbSex.addItem(u'')
            result.cmbSex.addItem(u'')
            result.cmbSex.setItemText(0, u'Не задано')
            result.cmbSex.setItemText(1, u'Общий')
            result.cmbSex.setItemText(2, u'Лекарственное обеспечение')
            result.cmbSex.setItemText(3, u'Принудительное лечение')
            result.cmbSex.setItemText(4, u'Недобровольная госпитализация')
            result.cmbSex.setItemText(5, u'Детство')
        for i in xrange(result.gridLayout.count()):
            spacer = result.gridLayout.itemAt(i)
            if isinstance(spacer, QtGui.QSpacerItem):
                itemposition = result.gridLayout.getItemPosition(i)
                if itemposition != (29, 0, 1, 1) and itemposition != (8, 1, 1, 3):
                    result.gridLayout.removeItem(spacer)
        result.resize(400, 10)
        return result

    def selectData(self, params):
        db = QtGui.qApp.db

        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        JournalType = params.get('sex', 0)
        characterCases = params.get('eventStatus', None)
        vidExperts = params.get('noteUET', None)
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

        if JournalType == 1:
            jornType = u' sn7 = "Общий"'
        elif JournalType == 2:
            jornType = u' sn7 = "Лекарственное обеспечение"'
        elif JournalType == 3:
            jornType = u' sn7 = "Принудительное лечение"'
        elif JournalType == 4:
            jornType = u' sn7 = "Недобровольная госпитализация"'
        elif JournalType == 5:
            jornType = u' sn7 = "Детство"'
        else:
            jornType = u'1'

        if characterCases:
            characterCase = u'sn3 = "' + self.rec[characterCases-1] + u'"'
        else:
            characterCase = u'1'

        if vidExperts:
            vidExpert = u'sn4 = "' + self.recExpert[vidExperts-1] + u'"'
        else:
            vidExpert = u'1'

        stmt = u'''SELECT e.id,sn.value,a.begDate,formatPersonName(e.execPerson_id) AS pers,os.code,CONCAT(c.lastName,' ',c.firstName,' ', c.patrName) AS fio,e.externalId,c.birthDate,c.sex
  ,sn2.value AS sn2,sn3.value as sn3,sn4.value as sn4,sn5.value as sn5,sn6.value as sn6,sn7.value as sn7
  ,sn8.value as sn8,sn9.value as sn9,sn10.value as sn10,sn11.value as sn11,sn12.value as sn12,sn13.value as sn13,sn14.value as sn14, sn15.value AS sn15,
  (SELECT   Diagnostic.id  FROM Diagnosis  
  INNER JOIN Diagnostic    ON Diagnostic.diagnosis_id = Diagnosis.id   
  INNER JOIN rbDiagnosisType    ON Diagnostic.diagnosisType_id = rbDiagnosisType.id  
  WHERE Diagnostic.event_id = e.id  AND Diagnosis.deleted = 0  AND Diagnostic.deleted = 0  
  AND (rbDiagnosisType.code = '1'  OR (rbDiagnosisType.code = '2'  AND Diagnostic.person_id = e.execPerson_id  
  AND (NOT EXISTS (SELECT    DC.id   FROM Diagnostic AS DC    INNER JOIN rbDiagnosisType AS DT     ON DT.id = DC.diagnosisType_id   
  WHERE DT.code = '1'   AND DC.event_id = e.id   AND DC.deleted = 0 LIMIT 1)))  
  OR (rbDiagnosisType.code = '7'  AND Diagnostic.person_id = e.execPerson_id  
  AND (NOT EXISTS (SELECT    DC.id   FROM Diagnostic AS DC    INNER JOIN rbDiagnosisType AS DT     ON DT.id = DC.diagnosisType_id   WHERE DT.code = '1'   AND DC.event_id = e.id   AND DC.deleted = 0 LIMIT 1))
  AND (NOT EXISTS (SELECT    DC.id   FROM Diagnostic AS DC    INNER JOIN rbDiagnosisType AS DT     ON DT.id = DC.diagnosisType_id   WHERE DT.code = '2'   AND DC.event_id = e.id   AND DC.deleted = 0 LIMIT 1))))
  ORDER BY Diagnosis.id LIMIT 1) AS MKB

FROM Event e
  LEFT JOIN Action a ON e.id = a.event_id
  LEFT JOIN ActionType at ON a.actionType_id = at.id
  LEFT JOIN Client c ON e.client_id = c.id

left join ActionPropertyType apt on apt.actionType_id = at.id and apt.name = '№ ВК' and apt.deleted = 0 
    left join ActionProperty ap on ap.action_id = a.id and ap.type_id = apt.id
    left join ActionProperty_Integer sn on sn.id = ap.id

left join ActionPropertyType apt1 on apt1.actionType_id = at.id and apt1.name = 'Отделение' and apt1.deleted = 0 
    left join ActionProperty ap1 on ap1.action_id = a.id and ap1.type_id = apt1.id
    left join ActionProperty_OrgStructure sn1 on sn1.id = ap1.id
    LEFT JOIN OrgStructure os ON sn1.value = os.id

left join ActionPropertyType apt2 on apt2.actionType_id = at.id and apt2.name = 'Социальный статус' and apt2.deleted = 0 
    left join ActionProperty ap2 on ap2.action_id = a.id and ap2.type_id = apt2.id
    left join ActionProperty_String sn2 on sn2.id = ap2.id

left join ActionPropertyType apt3 on apt3.actionType_id = at.id and apt3.name = 'Характеристика случая экспертизы' and apt3.deleted = 0 
    left join ActionProperty ap3 on ap3.action_id = a.id and ap3.type_id = apt3.id
    left join ActionProperty_String sn3 on sn3.id = ap3.id

left join ActionPropertyType apt4 on apt4.actionType_id = at.id and apt4.name = 'Вид и предмет экспертизы' and apt4.deleted = 0 
    left join ActionProperty ap4 on ap4.action_id = a.id and ap4.type_id = apt4.id
    left join ActionProperty_String sn4 on sn4.id = ap4.id

left join ActionPropertyType apt5 on apt5.actionType_id = at.id and apt5.name = 'Отклонение от стандартов' and apt5.deleted = 0 
    left join ActionProperty ap5 on ap5.action_id = a.id and ap5.type_id = apt5.id
    left join ActionProperty_String sn5 on sn5.id = ap5.id

left join ActionPropertyType apt6 on apt6.actionType_id = at.id and apt6.name = 'Дефекты нарушения, ошибки и др.' and apt6.deleted = 0 
    left join ActionProperty ap6 on ap6.action_id = a.id and ap6.type_id = apt6.id
    left join ActionProperty_String sn6 on sn6.id = ap6.id

left join ActionPropertyType apt7 on apt7.actionType_id = at.id and apt7.name = 'Категория ВК' and apt7.deleted = 0 
    left join ActionProperty ap7 on ap7.action_id = a.id and ap7.type_id = apt7.id
    left join ActionProperty_String sn7 on sn7.id = ap7.id

left join ActionPropertyType apt8 on apt8.actionType_id = at.id and apt8.name = 'Обоснование заключения' and apt8.deleted = 0 
    left join ActionProperty ap8 on ap8.action_id = a.id and ap8.type_id = apt8.id
    left join ActionProperty_String sn8 on sn8.id = ap8.id

left join ActionPropertyType apt9 on apt9.actionType_id = at.id and apt9.name = 'Дата направления на МСЭ или др.леч.уч.' and apt9.deleted = 0 
    left join ActionProperty ap9 on ap9.action_id = a.id and ap9.type_id = apt9.id
    left join ActionProperty_String sn9 on sn9.id = ap9.id

left join ActionPropertyType apt10 on apt10.actionType_id = at.id and apt10.name = 'Заключение МСЭ или др.спец.учрежд.' and apt10.deleted = 0 
    left join ActionProperty ap10 on ap10.action_id = a.id and ap10.type_id = apt10.id
    left join ActionProperty_String sn10 on sn10.id = ap10.id

left join ActionPropertyType apt11 on apt11.actionType_id = at.id and apt11.name = 'Дата получения заключения МСЭ или др.учржд.' and apt11.deleted = 0 
    left join ActionProperty ap11 on ap11.action_id = a.id and ap11.type_id = apt11.id
    left join ActionProperty_String sn11 on sn11.id = ap11.id

left join ActionPropertyType apt12 on apt12.actionType_id = at.id and apt12.name = 'Доп. информация по заключению др.учрежд.' and apt12.deleted = 0 
    left join ActionProperty ap12 on ap12.action_id = a.id and ap12.type_id = apt12.id
    left join ActionProperty_String sn12 on sn12.id = ap12.id

left join ActionPropertyType apt13 on apt13.actionType_id = at.id and apt13.name = 'Эксперт 1' and apt13.deleted = 0 
    left join ActionProperty ap13 on ap13.action_id = a.id and ap13.type_id = apt13.id
    left join ActionProperty_String sn13 on sn13.id = ap13.id

left join ActionPropertyType apt14 on apt14.actionType_id = at.id and apt14.name = 'Эксперт 2' and apt14.deleted = 0 
    left join ActionProperty ap14 on ap14.action_id = a.id and ap14.type_id = apt14.id
    left join ActionProperty_String sn14 on sn14.id = ap14.id
left join ActionPropertyType apt15 on apt15.actionType_id = at.id and apt15.name = 'Председатель ВК' and apt15.deleted = 0 
    left join ActionProperty ap15 on ap15.action_id = a.id and ap15.type_id = apt15.id
    left join ActionProperty_String sn15 on sn15.id = ap15.id
/* общее кол-во ВК */ 
  WHERE at.flatCode  = 'form035' AND a.deleted=0 AND at.deleted=0 AND e.deleted=0 and date(a.endDate) BETWEEN DATE(%(begDate)s) AND DATE(%(endDate)s) %(orgStructureIdWhere)s 
    GROUP BY a.id
    Having %(jornType)s and %(characterCase)s and %(vidExpert)s
    ORDER BY sn.value
        ''' % {'begDate': db.formatDate(begDate),
               'endDate': db.formatDate(endDate),
               'orgStructureIdWhere': orgStructureIdWhere,
               'jornType': jornType,
               'vidExpert': vidExpert,
               'characterCase': characterCase
               }
        return db.query(stmt)

    def getDescription(self, params):

        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        JournalType = params.get('sex', 0)
        orgStructureId = params.get('orgStructureId', None)
        characterCases = params.get('eventStatus', 0)
        vidExperts = params.get('noteUET', 0)

        rows = []
        rows.append(dateRangeAsStr(u'за период', begDate, endDate))

        if JournalType == 1:
            rows.append(u'Тип журнала: Общий')
        elif JournalType == 2:
            rows.append(u'Тип журнала: Лекарственное обеспечение')
        elif JournalType == 3:
            rows.append(u'Тип журнала: Принудительное лечение')
        elif JournalType == 4:
            rows.append(u'Тип журнала: Недобровольная госпитализация')
        elif JournalType == 5:
            rows.append(u'Тип журнала: Детство')
        if characterCases:
            rows.append(u'Характеристика случая: ' + self.rec[characterCases-1])
        if vidExperts:
            rows.append(u'Вид и предмет экспертизы: ' + self.recExpert[vidExperts-1])
        if orgStructureId:
            rows.append(u'подразделение: ' + getOrgStructureFullName(orgStructureId))

        rows.append(u'отчёт составлен: ' + forceString(QDateTime.currentDateTime()))
        return rows

    def build(self, params):
        reportRowSize = 22

        query = self.selectData(params)

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.insertHtml(u'<div align="right">Приложение N 1<br>к Приказу<br>Министерства здравоохранения<br>Российской Федерации<br>от 21 мая 2002 г. N 154</div>')
        cursor.insertHtml(u'<table width=70% align="center"><tr><td>Министерство здравоохранения</td><td>&nbsp;</td><td align="right">Медицинская документация</td></tr><tr><td>Российской Федерации</td><td>&nbsp;</td><td align="right">Форма N 035/у-02</td></tr><tr><td>__________________________________</td><td>&nbsp;</td><td align="right">Утверждена</td></tr><tr><td>(наименование учреждения)</td><td>&nbsp;</td><td align="right">Приказом Минздрава</td></tr><tr><td></td>&nbsp;<td></td><td align="right">Российской Федерации</td></tr></table>')
        cursor.insertHtml(u'<table width=100%><tr><td width=100% align = center><h4>ЖУРНАЛ<br>УЧЕТА КЛИНИКО - ЭКСПЕРТНОЙ РАБОТЫ<br>ЛЕЧЕБНО - ПРОФИЛАКТИЧЕСКОГО УЧРЕЖДЕНИЯ</h4></td></tr></table>')
        self.dumpParams(cursor, params, CReportBase.AlignCenter)
        cursor.setBlockFormat(CReportBase.AlignCenter)
        cursor.insertHtml(u'общее кол-во ВК %s' % query.size())
        cursor.insertBlock()
        # cursor.insertText(firstTitle)
        cursor.insertBlock()
        cursor.insertBlock()
        # рисуем первую табличку
        tableColumns = [
            ('30', [u'№ п/п', u'', u'1'], CReportBase.AlignCenter),
            ('50', [u'Номер вк', u'', u'2'], CReportBase.AlignLeft),
            ('80', [u'Дата экспертизы', u'', u'3'], CReportBase.AlignLeft),
            ('150', [u'Наименование ЛПУ, фамилия врача, направившего пациента на экспертизу', u'', u'4'], CReportBase.AlignLeft),
            ('100', [u'Фамилия, имя, отчество пациента', u'', u'5'], CReportBase.AlignLeft),
            ('100', [u'Адрес (либо N страхового полиса или медицинского документа) пациента', u'', u'6'], CReportBase.AlignLeft),
            ('70', [u'Дата рождения', u'', u'7'], CReportBase.AlignLeft),
            ('30', [u'Пол', u'', u'8'], CReportBase.AlignCenter),
            ('150', [u'Социальный статус\n----------\nпрофессия', u'', u'9'], CReportBase.AlignLeft),
            ('100', [u'Причина обращения. Диагноз (основной, сопутствующий) в соответствии с МКБ-10', u'', u'10'], CReportBase.AlignLeft),
            ('100', [u'Характеристика случая экспертизы', u'', u'11'], CReportBase.AlignLeft),
            ('100', [u'Вид и предмет экспертизы', u'', u'12'], CReportBase.AlignLeft),
            ('100', [u'Выявлено при экспертизе', u'отклонение от стандартов', u'13'], CReportBase.AlignLeft),
            ('100', [u'', u'дефекты, нарушения, ошибки и др.', u'14'], CReportBase.AlignLeft),
            ('100', [u'', u'достижение результата этапа или исхода лечебно - профилактического мероприятия', u'15'], CReportBase.AlignLeft),
            ('100', [u'Обоснование заключения. Заключение экспертов, рекомендации', u'', u'16'], CReportBase.AlignLeft),
            ('100', [u'Дата направления в бюро МСЭ или другие (специализированные) учреждения', u'', u'17'], CReportBase.AlignLeft),
            ('100', [u'Заключение МСЭ или других (специализированных) учреждений', u'', u'18'], CReportBase.AlignLeft),
            ('100', [u'Дата получения заключения МСЭ или других учреждений, срок его действия', u'', u'19'], CReportBase.AlignLeft),
            ('100', [u'Дополнительная информация по заключению других (специализированных) учреждений. Примечания', u'', u'20'], CReportBase.AlignLeft),
            ('100', [u'Основной состав экспертов', u'', u'21'], CReportBase.AlignLeft),
            ('100', [u'Подписи экспертов', u'', u'22'], CReportBase.AlignLeft),
        ]

        table = createTable(cursor, tableColumns)
        for col in xrange(reportRowSize):
            if col in (12, 13, 14):
                table.mergeCells(0, col, 1, 1)
            else:
                table.mergeCells(0, col, 2, 1)
        table.mergeCells(0, 12, 1, 3)


        ind = 0
        while query.next():
            record = query.record()
            value = forceString(record.value('value'))
            begDate = forceDateTime(record.value('begDate'))
            pers = forceString(record.value('pers'))
            code = forceString(record.value('code'))
            fio = forceString(record.value('fio'))
            externalId = forceString(record.value('externalId'))
            birthDate = forceDate(record.value('birthDate'))
            sex = forceString(record.value('sex'))
            sn2 = forceString(record.value('sn2'))
            sn3 = forceString(record.value('sn3'))
            sn4 = forceString(record.value('sn4'))
            sn5 = forceString(record.value('sn5'))
            sn6 = forceString(record.value('sn6'))
            sn7 = forceString(record.value('sn7'))
            sn8 = forceString(record.value('sn8'))
            sn9 = forceString(record.value('sn9'))
            sn10 = forceString(record.value('sn10'))
            sn11 = forceString(record.value('sn11'))
            sn12 = forceString(record.value('sn12'))
            sn13 = forceString(record.value('sn13'))
            sn14 = forceString(record.value('sn14'))
            sn15 = forceString(record.value('sn15'))
            MKB = forceString(record.value('MKB'))
            context = CInfoContext()
            diag = context.getInstance(CDiagnosticInfo, MKB)
            ind += 1
            row = table.addRow()

            table.setText(row, 0, ind)
            table.setText(row, 1, value)
            table.setText(row, 2, begDate.toString('dd.MM.yyyy'))
            table.setText(row, 3, pers + ' \n' + code)
            table.setText(row, 4, fio)
            table.setText(row, 5, externalId)
            table.setText(row, 6, birthDate.toString('dd.MM.yyyy'))
            table.setText(row, 7, u'М' if sex == '1' else u'Ж')
            table.setText(row, 8, sn2)
            table.setText(row, 9, diag.MKB + ' ' + diag.MKB.descr)
            table.setText(row, 10, sn3)
            table.setText(row, 11, sn4)
            table.setText(row, 12, sn5)
            table.setText(row, 13, sn6)
            table.setText(row, 14, '')
            table.setText(row, 15, sn8)
            table.setText(row, 16, sn9)
            table.setText(row, 17, sn10)
            table.setText(row, 18, sn11)
            table.setText(row, 19, sn12)
            table.setText(row, 20, sn15 + ' \n' + sn13 + ' \n' + sn14)



        return doc

