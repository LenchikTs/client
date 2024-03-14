# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4.QtCore import QDate

from Reports.Utils import _getChiefName
from library.Utils import forceString, forceDate, forceInt, forceRef
from Reports.Report import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.EconomicAnalisysSetupDialog import CEconomicAnalisysSetupDialog


class CAttachmentBySmoSetupDialog(CEconomicAnalisysSetupDialog):
    def __init__(self, parent=None):
        CEconomicAnalisysSetupDialog.__init__(self, parent)
        self.lblBegDate.setText(u'Дата')
        self.lblPayer.setText(u'СМО')
        self.lblOrgStructure.setText(u'Медицинская организация')
        self.setOrgStructureVisible(True)
        self.setEventTypeVisible(False)
        self.setEndDateVisible(False)
        self.setNoschetaVisible(False)
        self.setDateTypeVisible(False)
        self.setSpecialityVisible(False)
        self.setPersonVisible(False)
        self.setFinanceVisible(False)
        self.setVidPomVisible(False)
        self.setRazrNasVisible(False)
        self.setSchetaVisible(False)
        self.setSexVisible(False)
        self.setAgeVisible(False)
        self.setProfileBedVisible(False)
        self.setPriceVisible(False)
        self.cmbPayer.setWithoutKTFOMS(True)
        self.resize(400, 10)


class CAttachmentBySmoReport(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setOrientation(QtGui.QPrinter.Landscape)

    def getQuery(self, oms, smo, date):
        where = ['1 = 1']
        if oms:
            where.append('sa.attach_mo = %s' % oms)
        if smo:
            where.append('sa.smo = %s' % smo)

        stmt = u'''
                select mocode, org,
                       sum(cnt) as allcnt,
                       sum(case when sex = 'м' and age < 1 then cnt else 0 end) as grp1m,
                       sum(case when sex = 'ж' and age < 1 then cnt else 0 end) as grp1f,
                       sum(case when sex = 'м' and age >= 1 and age <= 4 then cnt else 0 end) as grp2m,
                       sum(case when sex = 'ж' and age >= 1 and age <= 4 then cnt else 0 end) as grp2f,
                       sum(case when sex = 'м' and age >= 5 and age <= 17 then cnt else 0 end) as grp3m,
                       sum(case when sex = 'ж' and age >= 5 and age <= 17 then cnt else 0 end) as grp3f,
                       sum(case when sex = 'м' and age >= 18 and age <= 59 then cnt else 0 end) as grp4m,
                       sum(case when sex = 'ж' and age >= 18 and age <= 54 then cnt else 0 end) as grp4f,
                       sum(case when sex = 'м' and age >= 60 then cnt else 0 end) as grp5m,
                       sum(case when sex = 'ж' and age >= 55 then cnt else 0 end) as grp5f
                from
                (
                    select
                        sa.attach_mo as mocode,
                        (select shortName from Organisation where infisCode = sa.attach_mo order by id asc limit 1) as org,
                        count(sa.id) as cnt,
                        lower(sa.sex) as sex,
                        age(sa.birthDate, %(date)s) as age
                    from soc_attachments sa
                    where sa.attach_date = %(date)s and sa.serviceMethod = 2 and %(where)s
                    group by
                        sa.attach_mo, sa.sex, age(sa.birthDate, %(date)s)
                ) q
                group by mocode
                order by mocode asc
            ''' % {'date': QtGui.qApp.db.formatDate(date), 'where': ' and '.join(where)}
        return QtGui.qApp.db.query(stmt)

    def getSetupDialog(self, parent):
        result = CAttachmentBySmoSetupDialog(parent)
        result.setTitle(u'Акт сверки прикрепленного населения по СМО')
        return result

    def exec_(self):
        query = QtGui.qApp.db.query(u'select count(*) from soc_attachments where serviceMethod = 2')
        if query.first() and query.value(0).toInt()[0] > 0:
            CReport.exec_(self)
        else:
            QtGui.QMessageBox.warning(None,
                                      u'Внимание!',
                                      u'Проведите синхронизацию с Регистром прикрепленного населения согласно Актам сверок',
                                      QtGui.QMessageBox.Ok)

    def build(self, params):
        db = QtGui.qApp.db
        smo_id = params.get('payer', None)
        smo = forceString(db.translate('Organisation', 'id', smo_id, 'usishCode')) if smo_id else None
        date = forceDate(params.get('begDate', QDate.currentDate()))
        orgStructureId = params.get('orgStructureId', None)
        orgId = forceString(QtGui.qApp.db.translate('OrgStructure', 'id', orgStructureId, 'organisation_id')
                            ) if orgStructureId else QtGui.qApp.currentOrgId()
        if orgStructureId:
            bookkeeperCode = forceString(db.translate('OrgStructure', 'id', orgStructureId, 'bookkeeperCode'))
            # ищем омс код подразделения к которому прикреплен человек
            while not bookkeeperCode and orgStructureId:
                orgStructureId = forceRef(db.translate('OrgStructure', 'id', orgStructureId, 'parent_id'))
                bookkeeperCode = forceString(db.translate('OrgStructure', 'id', orgStructureId, 'bookkeeperCode'))
            oms = bookkeeperCode
        else:
            oms = None
        query = self.getQuery(oms, smo, date)

        doc = QtGui.QTextDocument()
        doc.setDefaultStyleSheet("body{font-size: 10pt}")
        cursor = QtGui.QTextCursor(doc)
        rt = CReportBase.ReportTitle
        rt.setFontWeight(QtGui.QFont.Normal)
        cursor.setCharFormat(rt)
        cursor.setBlockFormat(CReportBase.AlignCenter)
        cursor.insertHtml(u'<br/>')
        cursor.insertText(u'''Акт
сверки численности застрахованного населения
(прикрепленного к медицинской организации/прикрепленного к фельдшерско-акушерскому пункту/обслуживаемого СМП)
в разрезе половозрастных групп
на %s г.
                          ''' % date.toString('dd.MM.yyyy') if params.get('begDate') else '___')

        cursor.insertBlock()
        smoname = omsname = omscode = smochief = orgchief = u' '
        if smo_id:
            smoname = forceString(QtGui.qApp.db.translate('Organisation', 'id', smo_id, 'fullName'))
            smochief = _getChiefName(smo_id)

        if orgId:
            omsname = forceString(QtGui.qApp.db.translate('Organisation', 'id', orgId, 'fullName'))
            orgchief = _getChiefName(orgId)
            omscode = forceString(QtGui.qApp.db.translate('Organisation', 'id', orgId, 'infisCode'))
        cursor.insertHtml(u'''
        <table width="100%%" cellspacing="0" cellpadding="0">
            <tr>
                <td align="center"><div style="font-size: 10pt"> </div><hr/><div style="font-size: 8pt"> </div></td>
                <td colspan="3" align="center"><div style="font-size: 10pt">%s</div><hr/><div style="font-size: 8pt">(наименование CМО)</div></td>
                <td align="center"><div style="font-size: 10pt"> </div><hr/><div style="font-size: 8pt"> </div></td>
            </tr>
        </table>
        ''' % smoname)
        cursor.insertBlock()
        cursor.insertHtml(u'''
        <br/>
        <table width="100%%" cellspacing="0" cellpadding="0">
            <tr>
                <td align="center"><div style="font-size: 10pt">%s</div><hr/><div style="font-size: 8pt">(код МО)</div></td>
                <td colspan="3" align="center"><div style="font-size: 10pt">%s</div><hr/><div style="font-size: 8pt">(наименование МО)</div></td>
                <td align="center"><div style="font-size: 10pt"> </div><hr/><div style="font-size: 8pt"> </div></td>
            </tr>
        </table>
        <br/>
        <br/>
        ''' % (omscode, omsname))
        cursor.insertBlock()
        tableColumns = [
            ('5%',  [u'№ п/п'], CReportBase.AlignCenter),
            ('5%', [u'Код структурного подразделения'], CReportBase.AlignCenter),
            ('10%',  [u'Наименование структурного подразделения'], CReportBase.AlignCenter),
            ('5%', [u'Численность застрахованного населения (прикрепленного к медицинской организации/прикрепленного '
                    u'к фельдшерско-акушерскому пункту/обслуживаемого СМП), чел.'], CReportBase.AlignCenter),
            ('10%', [u'в том числе по группам застрахованных лиц',
                     u'моложе трудоспособного возраста',
                     u'0-1 год',
                     u'Муж'], CReportBase.AlignCenter),
            ('5%', [u'', u'', u'', u'Жен'], CReportBase.AlignCenter),
            ('5%', [u'', u'', u'1-4 года', u'Муж'], CReportBase.AlignCenter),
            ('5%', [u'', u'', u'', u'Жен'], CReportBase.AlignCenter),
            ('5%', [u'', u'', u'5-17 лет', u'Муж'], CReportBase.AlignCenter),
            ('5%', [u'', u'', u'', u'Жен'], CReportBase.AlignCenter),
            ('5%', [u'', u'трудоспособный возраст', u'18-59 лет', u'Муж'], CReportBase.AlignCenter),
            ('5%', [u'', u'', u'18-54 лет', u'Жен'], CReportBase.AlignCenter),
            ('5%', [u'', u'старше трудоспособного возраста', u'60 лет и ст', u'Муж'], CReportBase.AlignCenter),
            ('5%', [u'', u'', u'55 лет и ст', u'Жен'], CReportBase.AlignCenter),
        ]
        table = createTable(cursor, tableColumns)
        # row, column, numRows, numCols
        # 1я строка
        table.mergeCells(0, 0, 4, 1)
        table.mergeCells(0, 1, 4, 1)
        table.mergeCells(0, 2, 4, 1)
        table.mergeCells(0, 3, 4, 1)
        table.mergeCells(0, 4, 1, 10)
        # 2я строка
        table.mergeCells(1, 4, 1, 6)
        table.mergeCells(1, 10, 1, 2)
        table.mergeCells(1, 12, 1, 2)
        # 3я строка
        table.mergeCells(2, 4, 1, 2)
        table.mergeCells(2, 6, 1, 2)
        table.mergeCells(2, 8, 1, 2)
        rowNumber = 0
        allkeys = ['mocode', 'org', 'allcnt',
                   'grp1m', 'grp1f',
                   'grp2m', 'grp2f',
                   'grp3m', 'grp3f',
                   'grp4m', 'grp4f',
                   'grp5m', 'grp5f']
        total = {}
        while query.next():
            record = query.record()
            row = table.addRow()
            rowNumber += 1
            table.setText(row, 0, rowNumber)

            for i, key in enumerate(allkeys):
                table.setText(row, i+1, forceString(record.value(key)))
                if i > 1:
                    total[key] = total.get(key, 0) + forceInt(record.value(key))

        row = table.addRow()
        table.setText(row, 0, u'ИТОГО по медицинской организации')
        table.mergeCells(row, 0, 1, 3)
        for i, key in enumerate(allkeys):
            if i > 1:
                table.setText(row, i + 1, forceString(total.get(key, 0)))
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        if not orgchief:
            orgchief = u' '
        if not smochief:
            smochief = u' '
        cursor.insertHtml(u'''
        <br/>
        <table width="100%%" cellspacing="0" cellpadding="0">
            <tr>
                <td colspan="2" align="center"><div style="font-size: 10pt"> </div><hr/><div><div style="font-size: 8pt">(подпись)</div></td>
                <td align="center"><div><div style="font-size: 10pt"> </div><hr/><div><div style="font-size: 8pt"> </div></td>
                <td align="center"><div><div style="font-size: 10pt">%s</div><hr/><div><div style="font-size: 8pt">(Ф.И.О. руководителя МО)</div></td>
                <td align="center"><div><div style="font-size: 10pt"> </div><hr/><div><div style="font-size: 8pt"> </div></td>
            </tr>
            <tr>
                <td colspan="2">МП</td>
            </tr>
        </table>
        <br/>
        ''' % orgchief)
        cursor.insertHtml(u'''
        <table width="100%%" cellspacing="0" cellpadding="0">
            <tr>
                <td colspan="2" align="center"><div style="font-size: 10pt"> </div><hr/><div><div style="font-size: 8pt">(подпись)</div></td>
                <td align="center"><div><div style="font-size: 10pt"> </div><hr/><div><div style="font-size: 8pt"> </div></td>
                <td align="center"><div><div style="font-size: 10pt">%s</div><hr/><div><div style="font-size: 8pt">(Ф.И.О. руководителя СМО)</div></td>
                <td align="center"><div><div style="font-size: 10pt"> </div><hr/><div><div style="font-size: 8pt"> </div></td>
            </tr>
            <tr>
                <td colspan="2">МП</td>
            </tr>
        </table>
        <br/>
        ''' % smochief)
        return doc
