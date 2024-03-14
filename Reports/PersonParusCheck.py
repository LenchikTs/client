# -*- coding: utf-8 -*-

from PyQt4 import QtGui

from library.Utils import forceString, forceDate
from Reports.Report import CReport, CVoidSetupDialog
from Reports.ReportBase import CReportBase, createTable


def getQuery():
    stmt = u"""
        SELECT
          Organisation.infisCode,
          Person.SNILS,
          Person.lastName,
          Person.firstName,
          Person.patrName,
          case Person.sex when 1 then 'М' when 2 then 'Ж' end as sex,
          Person.birthDate,
          Parus.MoCodeOms as p_MoCodeOms,
          replace(replace(Parus.Snils,'-',''),' ','') as p_Snils,
          Parus.Surname as p_Surname,
          Parus.Name as p_Name,
          Parus.MiddleName as p_MiddleName,
          case Parus.sex when 1 then 'М' when 2 then 'Ж' end as p_Sex,
          Parus.DateBirth as p_DateBirth

        from Person
          left join Organisation on Organisation.id = Person.org_id
          inner join soc_PersonParus as Parus on (Parus.Surname = Person.lastName
                                                  and Parus.Name = Person.firstName
                                                  and coalesce(Parus.MiddleName, '') = coalesce(Person.patrName, ''))
                                              or replace(replace(Parus.Snils,'-',''),' ','') = Person.SNILS
        where Person.deleted = 0
          and (((Parus.Surname != Person.lastName
            or Parus.Name != Person.firstName
            or coalesce(Parus.MiddleName, '') != coalesce(Person.patrName, '')) and replace(replace(Parus.Snils,'-',''),' ','') = Person.SNILS)
			or 
            (Parus.Surname = Person.lastName
				and Parus.Name = Person.firstName
				and coalesce(Parus.MiddleName, '') = coalesce(Person.patrName, '') 
				and replace(replace(Parus.Snils,'-',''),' ','') != Person.SNILS))
        """
    return QtGui.qApp.db.query(stmt)


class CPersonParusCheckReport(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setOrientation(QtGui.QPrinter.Landscape)
        self.setTitle(u'Сверка данных медицинских работников')

    def getSetupDialog(self, parent):
        return CVoidSetupDialog(self)

    def exec_(self):
        query = QtGui.qApp.db.query(u'select count(*) from soc_PersonParus')
        if query.first() and query.value(0).toInt()[0] > 0:
            CReport.exec_(self)
        else:
            QtGui.QMessageBox.warning(None,
                                      u'Внимание!',
                                      u'Проведите синхронизацию с Регистром медицинских работников',
                                      QtGui.QMessageBox.Ok)

    def build(self, params):
        query = getQuery()

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()

        tableColumns = [
            ('7%', [u'Данные МИС', u'ЛПУ'], CReportBase.AlignLeft),
            ('7%', ['', u'СНИЛС'], CReportBase.AlignLeft),
            ('8%', ['', u'Фамилия'], CReportBase.AlignLeft),
            ('7%', ['', u'Имя'], CReportBase.AlignLeft),
            ('7%', ['', u'Отчество'], CReportBase.AlignLeft),
            ('7%', ['', u'Пол'], CReportBase.AlignLeft),
            ('7%', ['', u'Дата рождения'], CReportBase.AlignLeft),
            ('7%', [u'Данные Регистра медицинских работников', u'ЛПУ'], CReportBase.AlignLeft),
            ('7%', ['', u'СНИЛС'], CReportBase.AlignLeft),
            ('8%', ['', u'Фамилия'], CReportBase.AlignLeft),
            ('7%', ['', u'Имя'], CReportBase.AlignLeft),
            ('7%', ['', u'Отчество'], CReportBase.AlignLeft),
            ('7%', ['', u'Пол'], CReportBase.AlignLeft),
            ('7%', ['', u'Дата рождения'], CReportBase.AlignLeft)
        ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 1, 7)
        table.mergeCells(0, 7, 1, 7)

        rowNumber = 0
        while query.next():
            record = query.record()
            row = table.addRow()
            rowNumber += 1

            table.setText(row, 0, forceString(record.value('infisCode')))
            table.setText(row, 1, forceString(record.value('SNILS')))
            table.setText(row, 2, forceString(record.value('lastName')))
            table.setText(row, 3, forceString(record.value('firstName')))
            table.setText(row, 4, forceString(record.value('patrName')))
            table.setText(row, 5, forceString(record.value('sex')))
            table.setText(row, 6, '' if record.isNull('birthDate') else forceDate(record.value('birthDate')).toString('dd.MM.yyyy'))
            table.setText(row, 7, forceString(record.value('p_MoCodeOms')))
            table.setText(row, 8, forceString(record.value('p_Snils')))
            table.setText(row, 9, forceString(record.value('p_Surname')))
            table.setText(row, 10, forceString(record.value('p_Name')))
            table.setText(row, 11, forceString(record.value('p_MiddleName')))
            table.setText(row, 12, forceString(record.value('p_Sex')))
            table.setText(row, 13, '' if record.isNull('p_DateBirth') else forceDate(record.value('p_DateBirth')).toString('dd.MM.yyyy'))
        return doc
