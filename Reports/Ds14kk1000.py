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
from Reports.Utils import _getChiefName
from Ui_Ds14kkSetupDialog import Ui_ds14kkSetupDialog
from library.Utils import forceString, forceInt, forceDouble
from Orgs.Utils import getOrgStructureDescendants


class CDs14kkSetupDialog(QtGui.QDialog, Ui_ds14kkSetupDialog):
    def __init__(self, parent=None, useCbPermanent = False):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.cbPermanent.setVisible(useCbPermanent)
        self.cmbFinance.setTable('rbFinance', addNone=True)

    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.cbPermanent.setChecked(params.get('notIsPermanent', True))
        self.cmbFinance.setValue(params.get('financeId', None))


    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['orgStructureId'] = self.cmbOrgStructure.value()
        result['notIsPermanent'] = self.cbPermanent.isChecked()
        result['financeId'] = self.cmbFinance.value()
        return result

class CDs14kkHelpers():
    @staticmethod
    def splitTitle(cursor, t1, t2):
        #type: (QtGui.QTextCursor, str, str) -> None
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        html = u'''
<table width="100%%">
    <tr>
        <td align="left"><h3>%s</h3></td>
        <td align="right"><h3>%s</h3></td>
    </tr>
</table>
        ''' % (t1,t2)
        cursor.insertHtml(html)
        cursor.insertBlock()
        cursor.insertBlock()

    @staticmethod
    def writeFooter(cursor):
        #type: (QtGui.QTextCursor) -> None
        orgPhone = forceString(QtGui.qApp.db.translate('Organisation',
                                                       'id', QtGui.qApp.currentOrgId(), 'phone'))
        orgChief = _getChiefName(QtGui.qApp.currentOrgId())
        if not orgChief:
            orgChief = u'_' * 30
        else:
            orgChief = u'<u>%s</u>' % orgChief
        if not orgPhone:
            orgPhone = u'_' * 30
        else:
            orgPhone = u'<u>%s</u>' % orgPhone
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.setBlockFormat(CReportBase.AlignRight)

        html = u'''
<table width="100%%">
    <tr>
        <td width="25%%">Руководитель организации</td>
        <td align="center">%(fio)s<br/><small>(Ф.И.О.)</small></td>
        <td align="center">_____________________________<br/><small>подпись</small></td>
        <td></td>
    </tr>
    <tr>
        <td>Должностное лицо, ответственное за предоставление статистической информации (лицо, уполномоченное
        предоставлять статистическую информацию от имени юридического лица)</td>
        <td align="center">_____________________________<br/><small>(Должность)</small></td>
        <td align="center">_____________________________<br/><small>(Ф.И.О.)</small></td>
        <td align="center">_____________________________<br/><small>подпись</small></td>
    </tr>
    <tr>
        <td></td>
        <td align="center">%(phone)s<br/><small>(номер контактного телефона)</small></td>
        <td align="center">%(data)s<br/><small>(дата составления документа)</small></td>
        <td></td>
    </tr>
</table>
        '''
        cursor.insertHtml(html % {u'fio': orgChief, u'phone': orgPhone, u'data': QDate.currentDate().toString('dd.MM.yyyy')})

    @staticmethod
    def getCond(params, dateType = 1, permanentBeds = False):
        #type: (dict, int) -> None
        cond = []
        if params.get('orgStructureId', None):
            orgStructList = ','.join(forceString(id) for id in getOrgStructureDescendants(params['orgStructureId']))
            cond.append('OrgStructure.id in ({0:s})'.format(orgStructList))

        if params.get('financeId', None):
            if dateType != 1:
                cond.append('Contract.finance_id = {0}'.format(params['financeId']))

        if params.get('begDate', None):
            if dateType == 1:
                cond.append(
                    '(OrgStructure_HospitalBed.endDate >= "%s" or OrgStructure_HospitalBed.endDate is null)' % params[
                        'begDate'].toString('yyyy-MM-dd hh:mm:ss')) #койка закончила работать после начала периода формы
            else:
                cond.append('Event.setDate >= "%s"' % params['begDate'].toString('yyyy-MM-dd hh:mm:ss'))

        if params.get('endDate', None):
            if dateType == 1:
                cond.append(
                    '(OrgStructure_HospitalBed.begDate <= "%s" or OrgStructure_HospitalBed.begDate is null)' % params[
                        'endDate'].toString('yyyy-MM-dd hh:mm:ss')) #койка начала работать до конечного периода формы


            else:
                cond.append('Event.setDate <= "%s"' % params['endDate'].toString('yyyy-MM-dd hh:mm:ss'))
        if permanentBeds and not params.get('notIsPermanent', True):
            cond.append('OrgStructure_HospitalBed.isPermanent = true')


        if len(cond) < 1:
            cond.append("1=1")
        return " and ".join(cond)


class CReportDs14kk1000(CReport):
    def __init__(self, parent = None):
        CReport.__init__(self, parent)
        self.setTitle(u'Таблица 1000 «Должности и физические лица дневных стационаров медицинской организации»')

    def getSetupDialog(self, parent):
        result = CDs14kkSetupDialog(parent)
        return result

    def selectData(self, params):
        stmt = u'''
        select dlgnsttype, orgtype, count(distinct fz) as fz, count(distinct dlgnst) as zan from (
            select
             concat_ws(' ', Person.lastName, Person.firstName, Person.patrName, DATE_FORMAT(Person.birthDate, '%%d.%%m.%%Y')) as fz,
             Person.id as dlgnst,
             stype.title as dlgnsttype,
             orgtype.title as orgtype
            from Person
            left join rbPost on rbPost.id = Person.post_id
            left join OrgStructure on OrgStructure.id = Person.orgStructure_id
            inner join (
              select  1 as id, /*'Руководители учреждений'*/ 'Врачи' as title
              union all select 2, /*'Руководители структурных подразделений''*/ 'Врачи'
              union all select 3, /*'Врачи-специалисты''*/ 'Врачи'
              union all select 4, 'Средние медицинские работники'
              union all select 5, 'Младший медицинский персонал') stype on stype.id = substr(rbPost.code, 1, 1)
            inner join (
              select 0 as id, 'Амбулатория' as title
                union all select 1, 'Стационар'
            ) orgtype on orgtype.id = OrgStructure.type
            left join OrgStructure_HospitalBed on OrgStructure_HospitalBed.master_id = OrgStructure.id
            left join rbHospitalBedShedule ON rbHospitalBedShedule.id = OrgStructure_HospitalBed.schedule_id

            where Person.deleted = false and rbHospitalBedShedule.code = 2 /*день*/
                and (Person.retireDate is null) or (Person.retireDate > '%(date)s')
                and %(cond)s
            ) report
            group by dlgnsttype, orgtype
        '''
        db = QtGui.qApp.db
        date = QDate.currentDate()
        if params.get("begDate", None):
            date = params["begDate"]
        elif params.get("endDate", None):
            date = params["endDate"]
        date = date.toString("yyyy-MM-dd")

        st = stmt % {'date': date, 'cond': CDs14kkHelpers.getCond(params)}
        return db.query(st)

    def selectData2(self, params):
        stmt = u'''
            select
                count(distinct case when isAdult then id else null end) as allAdult,
                count(distinct case when isChild then id else null end) as allChild,
                count(distinct case when isAdult and title = 'Стационар' then id else null end) as stacAdult,
                count(distinct case when isChild and title = 'Стационар' then id else null end) as stacChild,
                count(distinct case when isAdult and title = 'Амбулатория' then id else null end) as ambAdult,
                count(distinct case when isChild and title = 'Амбулатория' then id else null end) as ambChild from
            (
                select
                    OrgStructure.id,
                    orgtype.title,
                    isSexAndAgeSuitable(0, DATE_SUB(now(),INTERVAL 17 YEAR), 0, OrgStructure_HospitalBed.age, now()) as isChild,
                    isSexAndAgeSuitable(0, DATE_SUB(now(),INTERVAL 18 YEAR), 0, OrgStructure_HospitalBed.age, now()) as isAdult
                from OrgStructure

                inner join (
                  select 0 as id, 'Амбулатория' as title
                    union all select 1, 'Стационар'
                ) orgtype on orgtype.id = OrgStructure.type

                left join OrgStructure_HospitalBed on OrgStructure_HospitalBed.master_id = OrgStructure.id
                left join rbHospitalBedShedule ON rbHospitalBedShedule.id = OrgStructure_HospitalBed.schedule_id

                where rbHospitalBedShedule.code = 2 /*день*/  and %(cond)s
                group by OrgStructure.id, orgtype.title
            ) q
        '''
        db = QtGui.qApp.db
        st = stmt % {'cond': CDs14kkHelpers.getCond(params)}
        return db.query(st)


    def tbl_1010(self, cursor, data):
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        CDs14kkHelpers.splitTitle(cursor, u'(1010)', u'Коды по ОКЕИ: еденица - 642.')
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertText(u'Число дневных стационаров для взрослых: %d' % data.get('allAdult'))
        cursor.insertText(u'\r\n')
        cursor.insertText(u'Число дневных стационаров для детей: %d' % data.get('allChild'))

    def tbl_1020(self, cursor, data):
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        CDs14kkHelpers.splitTitle(cursor, u'(1020)', u'Коды по ОКЕИ: еденица - 642.')
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertText(u'Число дневных стационаров для взрослых при стационаре: %d' % data.get('stacAdult', 0))
        cursor.insertText(u'\r\n')
        cursor.insertText(u'число дневных стационаров для детей при стационаре: %d' % data.get('stacChild', 0))

    def tbl_1030(self, cursor, data):
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        CDs14kkHelpers.splitTitle(cursor, u'(1030)', u'Коды по ОКЕИ: еденица - 642.')
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertText(u'Число дневных стационаров для взрослых при поликлинике: %d' % data.get('ambAdult', 0))
        cursor.insertText(u'\r\n')
        cursor.insertText(u'Число дневных стационаров для детей при поликлинике: %d' % data.get('ambChild', 0))

    def tbl_1040(self, cursor, data):
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        CDs14kkHelpers.splitTitle(cursor, u'(1040)', u'Коды по ОКЕИ: еденица - 642.')
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertText(u'Число дневных стационаров для взрослых на дому: -')
        cursor.insertText(u'\r\n')
        cursor.insertText(u'Число дневных стационаров для детей на дому: -')

    def build(self, params):
        rowHeaders = [u'Врачи', u'Средние медицинские работники', u'Младший медицинский персонал', u'Всего']
        orgTypes = [u'Стационар', u'Амбулатория']
        report = [[0]*10 for x in range(4)]
        data2 = {'allAdult': 0, 'allChild': 0, 'stacAdult': 0, 'stacChild': 0, 'ambAdult': 0, 'ambChild': 0}
        def processQuery(query):
            while query.next():
                record = query.record()
                rowIdx = rowHeaders.index(forceString(record.value('dlgnsttype')))
                colIdx = orgTypes.index(forceString(record.value('orgtype'))) * 3

                report[rowIdx][0] = rowIdx + 1
                for _rowIdx in [rowIdx, 3]:
                    report[_rowIdx][1 + colIdx] += forceInt(record.value('zan'))
                    report[_rowIdx][2 + colIdx] += forceInt(record.value('zan'))
                    report[_rowIdx][3 + colIdx] += forceInt(record.value('fz'))
        def processQuery2(query):
            while query.next():
                record = query.record()
                for key in data2.keys():
                    data2[key] += forceInt(record.value(key))
        query = self.selectData(params)
        query2 = self.selectData2(params)

        processQuery(query)
        processQuery2(query2)
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.setBlockFormat(CReportBase.AlignCenter)
        cursor.insertText(u'1. ОБЩИЕ СВЕДЕНИЯ О ДНЕВНЫХ СТАЦИОНАРАХ')
        cursor.insertBlock()
        cursor.insertText(u'1.1 Должности и физические лица дневных стационаров медицинской организации')
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        CDs14kkHelpers.splitTitle(cursor, u'(1000)', u'Коды по ОКЕИ: человек - 792.')
        cursor.setCharFormat(CReportBase.ReportBody)

        cursor.insertBlock()
        tableColumns = [
            ('20%',[u'Наименование должностей'], CReportBase.AlignLeft),
            ('8%', [u'№ стр.'], CReportBase.AlignRight),
            ('8%', [u'Дневные стационары медицинских организаций, оказывающих медицинскую помощь', u'в стационарных условиях', u'число должностей', u'штатные'], CReportBase.AlignRight),
            ('8%', [u'', u'', u'', u'занятые'], CReportBase.AlignRight),
            ('8%', [u'', u'', u'физические лица'], CReportBase.AlignRight),
            ('8%', [u'', u'в амбулаторных условиях', u'число должностей', u'штатные'], CReportBase.AlignRight),
            ('8%', [u'', u'', u'', u'занятые'], CReportBase.AlignRight),
            ('8%', [u'', u'', u'физические лица'], CReportBase.AlignRight),
            ('8%', [u'', u'на дому',  u'число должностей', u'штатные'], CReportBase.AlignRight),
            ('8%', [u'', u'', u'', u'занятые'], CReportBase.AlignRight),
            ('8%', [u'', u'', u'физические лица'], CReportBase.AlignRight),
            ]

        table = createTable(cursor, tableColumns)
        autoMergeHeader(table, tableColumns)
        row = table.addRow()
        for i in range(11):
            table.setText(row, i, i+1, blockFormat=CReportBase.AlignCenter)
        for rowIdx, reportLine in enumerate(report):
            row = table.addRow()
            table.setText(row, 0, rowHeaders[rowIdx]) #заголовок
            for col, val in enumerate(reportLine):
                if col >= 7:
                    val = u'-'
                table.setText(row, col + 1, val)
            table.setText(row, 1, rowIdx + 1, blockFormat=CReportBase.AlignCenter) # номер страницы
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()

        self.tbl_1010(cursor, data2)
        self.tbl_1020(cursor, data2)
        self.tbl_1030(cursor, data2)
        self.tbl_1040(cursor, data2)
        CDs14kkHelpers.writeFooter(cursor)
        return doc