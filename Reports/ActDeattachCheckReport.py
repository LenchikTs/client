# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4.QtGui import QDialog
from PyQt4 import QtCore
from library.Utils import forceString, forceDate, forceInt, formatSex, forceDateTime, getPrefDate, getPref
from Reports.Utils import dateRangeAsStr
from Reports.Report import CReport
from Reports.ReportBase import CReportBase, createTable
from Ui_ActDeattachCheckSetupDialog import Ui_ActDeattachCheckSetupDialog

def getQuery(begDate, endDate, actType):
    if actType == 1:
        stmt = u"""
            select
                ce.master_id as clientid,
                concat_ws(' ', Client.lastName, Client.firstName, Client.patrName) as fio,
                Client.sex as sex,
                Client.birthDate as birthDate,
                coalesce(
                    (select concat_ws(' ',Organisation.infisCode, Organisation.shortName) from Organisation where Organisation.infisCode = ce.note order by id desc limit 1),
                    ce.note) as org,
                ce.dateTime as date
            from Client_Export ce
            left join Client on Client.id = ce.master_id
            where date(ce.dateTime) between '%s' and '%s' and ce.system_id = 10 and ce.success = 1
            and ce.note not in (select bookkeeperCode from OrgStructure where deleted = 0)
            order by ce.dateTime desc
        """
    else:
        stmt = u"""
            select
                concat_ws(' ', sa.lastName, sa.firstName, sa.patrName) as fio,
                case
                    when sa.sex like 'Ж' then 2
                    when sa.sex like 'М' then 1
                    else null end as sex,
                date(sa.birthDate) as birthDate,
                coalesce(
                    (select concat_ws(' ',Organisation.infisCode, Organisation.shortName) from Organisation where Organisation.infisCode = sa.attach_mo order by id desc limit 1),
                     sa.attach_mo) as org,
                sa.createDate as date
             from soc_attachments sa

            where date(sa.createDate) between '%s' and '%s' and  sa.serviceMethod = 3
            order by sa.lastName asc, sa.firstName asc, sa.patrName asc
        """
    stmt = stmt % (
        forceString(begDate.toString("yyyy-MM-dd")),
        forceString(endDate.toString("yyyy-MM-dd"))
    )
    return QtGui.qApp.db.query(stmt)


class CActDeattachCheckSetupDialog(QDialog, Ui_ActDeattachCheckSetupDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['actType'] = 1 if self.rbActType1.isChecked() else 2
        return result


    def setParams(self, params):
        today = QtCore.QDate.currentDate()
        self.edtBegDate.setDate(params.get('begDate', today))
        self.edtEndDate.setDate(params.get('endDate', today))
        if params.get('actType', 1) == 1:
            self.rbActType1.setChecked(True)
        else:
            self.rbActType2.setChecked(True)

    def setTitle(self, title):
        self.setWindowTitle(title)


class CActDeattachCheckReport(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Журнал обмена уведомлениями с другими медицинским организациями о прикреплении граждан')

    def getDefaultParams(self):
        result = {}
        today = QtCore.QDate.currentDate()
        prefs = getPref(QtGui.qApp.preferences.reportPrefs, self.title(), {})
        result['begDate'] = getPrefDate(prefs, 'begDate', today)
        result['endDate'] = getPrefDate(prefs, 'endDate', today)
        result['actType'] = 1
        return result

    def getSetupDialog(self, parent):
        result = CActDeattachCheckSetupDialog(parent)
        result.setTitle(self.title())
        return result

    def getDescription(self, params):
        begDate = params.get('begDate', QtCore.QDate())
        endDate = params.get('endDate', QtCore.QDate())
        actType = params.get('actType', 1)
        rows = []
        rows.append(dateRangeAsStr(u'за период', begDate, endDate))
        if actType == 1:
            rows.append(u'по отправленным уведомлениями')
        else:
            rows.append(u'по полученным уведомлениями')
        rows.append(u'отчёт составлен: ' + forceString(QtCore.QDateTime.currentDateTime()))
        return rows

    def dumpParams(self, cursor, params):
        description = self.getDescription(params)
        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)

        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertHtml('<br/><br/>')

    def build(self, params):
        actType = params.get("actType", 1)
        query = getQuery(
            params.get("begDate",QtCore.QDate.currentDate()),
            params.get("endDate",QtCore.QDate.currentDate()),
            actType
        )
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Журнал обмена уведомлениями с другими медицинским организациями о прикреплении граждан')
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertHtml('<br/><br/>')
        self.dumpParams(cursor, params)
        if actType == 1:
            tableColumns = [
                ('10%',  [u'№ п/п'], CReportBase.AlignLeft),
                ('10%', [u'Код'], CReportBase.AlignLeft),
                ('20%', [u'ФИО пациента'], CReportBase.AlignLeft),
                ('5%',  [u'Пол'], CReportBase.AlignLeft),
                ('10%', [u'Дата рождения'], CReportBase.AlignLeft),
                ('30%', [u'Сведения отправлены в'], CReportBase.AlignLeft),
                ('15%', [u'Запрос отправлен'], CReportBase.AlignLeft),
            ]
        else:
            tableColumns = [
                ('10%',  [u'№ п/п'], CReportBase.AlignLeft),
                ('30%', [u'ФИО пациента'], CReportBase.AlignLeft),
                ('10%', [u'Дата рождения'], CReportBase.AlignLeft),
                ('35%', [u'МО-отправитель уведомления'], CReportBase.AlignLeft),
                ('15%', [u'Запрос получен'], CReportBase.AlignLeft),
            ]

        table = createTable(cursor, tableColumns)

        rowNumber = 0
        while query.next():
            record = query.record()
            row = table.addRow()
            rowNumber += 1
            columns = [rowNumber,
                       forceString(record.value('fio')),
                       '' if record.isNull('birthDate') else forceDate(record.value('birthDate')).toString(
                           'dd.MM.yyyy'),
                       forceString(record.value('org')),
                       '' if record.isNull('date') else forceDateTime(record.value('date')).toString(
                           'dd.MM.yyyy hh:mm:ss')
                       ]
            if actType == 1:
                columns.insert(1, forceInt(record.value('clientid'))) #поле код для первого акта
                columns.insert(3, formatSex(forceInt(record.value('sex'))))  # поле пол для первого акта
            for idx, val in enumerate(columns):
                table.setText(row, idx, val)

        return doc
