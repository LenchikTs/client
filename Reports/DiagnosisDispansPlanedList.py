# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2023 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import QDate, pyqtSignature

from Reports.Utils import dateRangeAsStr
from library.Utils import forceString, getPref, getPrefInt, forceDate, formatDate, getPrefDate, formatSex, getPrefString
from Reports.Report import CReport
from Reports.ReportBase import CReportBase, createTable

from Ui_DiagnosisDispansPlanedList import Ui_DiagnosisDispansPlanedListDialog


def getQuery(params):
    db = QtGui.qApp.db
    table = db.table('ProphylaxisPlanning').alias('pp')
    tableDiagnosis = db.table('Diagnosis')
    tableClient = db.table('Client')
    begDate = params['begDate']
    endDate = params['endDate']
    personId = params['personId']
    MKBFilter = params.get('MKBFilter', 0)
    MKBFrom = params.get('MKBFrom', 'A00')
    MKBTo = params.get('MKBTo', 'Z99.9')
    noVisit = params.get('noVisit')

    cond = ["rbDispanser.observed = 1",
            tableDiagnosis['deleted'].eq(0),
            u"ppt.code = 'ДН'",
            'pp.parent_id IS NOT NULL',
            tableClient['deathDate'].isNull(),
            tableDiagnosis['mod_id'].isNull()]

    cond.append(u'''NOT EXISTS(SELECT DC.id
                                          FROM Diagnostic AS DC
                                          INNER JOIN Diagnosis AS DS ON DS.id = DC.diagnosis_id
                                          INNER JOIN rbDispanser AS rbDP ON rbDP.id = DC.dispanser_id
                                          WHERE DC.diagnosis_id = Diagnosis.id AND DC.endDate <= %s AND DC.deleted = 0 AND rbDP.name LIKE '%s')
                                   OR EXISTS(SELECT DC.id
                                          FROM Diagnostic AS DC
                                          INNER JOIN Diagnosis AS DS ON DS.id = DC.diagnosis_id
                                          INNER JOIN rbDispanser AS rbDP ON rbDP.id = DC.dispanser_id
                                          WHERE DC.diagnosis_id = Diagnosis.id AND DC.endDate <= %s AND DC.deleted = 0 AND rbDP.name LIKE '%s')''' % (db.formatDate(endDate), u'%снят%', db.formatDate(endDate), u'%взят повторно%'))

    if begDate and endDate:
        cond.append(db.joinOr([table['begDate'].between(begDate, endDate),
                               table['endDate'].between(begDate, endDate)]))

    if personId:
        cond.append(tableDiagnosis['dispanserPerson_id'].eq(personId))

    if noVisit:
        cond.append(table['visit_id'].isNull())

    if MKBFilter == 1:
        cond.append(tableDiagnosis['MKB'].ge(MKBFrom))
        cond.append(tableDiagnosis['MKB'].le(MKBTo))

    stmt = u"""
SELECT CONCAT_WS(' ', Client.lastName, Client.firstName, Client.patrName) AS clientName,
       Client.birthDate AS clientBirthDate,
       Client.sex AS clientSex,
       getClientContacts(Client.id) as contacts,
       coalesce(getClientLocAddress(Client.id), getClientRegAddress(Client.id)) as address,
       formatPersonName(Diagnosis.dispanserPerson_id) as personName,
       pp.MKB,
       Diagnosis.dispanserBegDate,
       (SELECT v.date
        FROM ProphylaxisPlanning pp2
        LEFT JOIN Visit v ON v.id = pp2.visit_id
        WHERE pp2.parent_id = pp.parent_id AND pp2.deleted = 0 AND pp2.visit_id IS NOT NULL
        AND pp2.begDate < pp.begDate
        ORDER BY v.date DESC LIMIT 1) AS lastVisitDate,
       CONCAT_WS(' - ', DATE_FORMAT(pp.begDate, '%d.%m.%Y'), DATE_FORMAT(pp.endDate, '%d.%m.%Y')) as curPeriod,
       Visit.date AS visitDate,
       (SELECT CONCAT_WS(' - ', DATE_FORMAT(pp3.begDate, '%d.%m.%Y'), DATE_FORMAT(pp3.endDate, '%d.%m.%Y'))
        FROM ProphylaxisPlanning pp3
        WHERE pp3.parent_id = pp.parent_id AND pp3.deleted = 0 AND pp3.begDate >= CURDATE()
        ORDER BY pp3.begDate ASC LIMIT 1) AS nextVisitDate
FROM Diagnosis
LEFT JOIN Client on Client.id = Diagnosis.client_id
LEFT JOIN rbDispanser ON rbDispanser.ID = Diagnosis.dispanser_id
LEFT JOIN ProphylaxisPlanning pp ON Diagnosis.MKB = pp.MKB AND pp.deleted = 0 AND pp.client_id = Diagnosis.client_id
LEFT JOIN rbProphylaxisPlanningType ppt ON ppt.id = pp.prophylaxisPlanningType_id
LEFT JOIN Visit ON Visit.id = pp.visit_id
WHERE {cond}
ORDER BY clientName""".format(cond=db.joinAnd(cond))
    return db.query(stmt)


class CDiagnosisDispansPlanedListDialog(QtGui.QDialog, Ui_DiagnosisDispansPlanedListDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Ok:
            if not all([self.edtEndDate.date(), self.edtBegDate.date()]) or self.edtEndDate.date() < self.edtBegDate.date():
                QtGui.QMessageBox.information(self, u'Внимание', u'Необходимо указать корректный период!')
                return
            QtGui.QDialog.accept(self)
        elif buttonCode == QtGui.QDialogButtonBox.Cancel:
            self.close()

    def setTitle(self, title):
        self.setWindowTitle(title)

    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate().currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate().currentDate()))
        self.cmbPerson.setValue(params.get('personId', None))
        MKBFilter = params.get('MKBFilter', 0)
        self.cmbMKBFilter.setCurrentIndex(MKBFilter if MKBFilter else 0)
        self.edtMKBFrom.setText(params.get('MKBFrom', 'A00'))
        self.edtMKBTo.setText(params.get('MKBTo', 'Z99.9'))

    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['personId'] = self.cmbPerson.value()
        result['MKBFilter'] = self.cmbMKBFilter.currentIndex()
        result['MKBFrom']   = unicode(self.edtMKBFrom.text())
        result['MKBTo']     = unicode(self.edtMKBTo.text())
        return result

    @pyqtSignature('int')
    def on_cmbMKBFilter_currentIndexChanged(self, index):
        self.edtMKBFrom.setEnabled(index == 1)
        self.edtMKBTo.setEnabled(index == 1)


class CDiagnosisDispansPlanedListReport(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)                         
        self.setTitle(u'Отчет по запланированным на диспансерное наблюдение')

    def getSetupDialog(self, parent):
        result = CDiagnosisDispansPlanedListDialog(parent)
        result.edtBegDate.canBeEmpty(False)
        result.edtEndDate.canBeEmpty(False)
        result.setTitle(self.title())
        return result
    
    def getDefaultParams(self):
        result = {}
        prefs = getPref(QtGui.qApp.preferences.reportPrefs, self.title(), {})
        result['begDate'] = getPrefDate(prefs, 'begDate', QDate().currentDate())
        result['endDate'] = getPrefDate(prefs, 'endDate', QDate().currentDate())
        result['personId'] = getPrefInt(prefs, 'personId', None)
        result['MKBFilter'] = getPrefInt(prefs, 'MKBFilter', 0)  # 0-нет фильтра, 1-интервал, 2-нет кода
        result['MKBFrom'] = getPrefString(prefs, 'MKBFrom', 'A00')
        result['MKBTo'] = getPrefString(prefs, 'MKBTo', 'Z99.9')

        return result

    def dumpParams(self, cursor, params, align=CReportBase.AlignLeft):
        db = QtGui.qApp.db
        begDate = params['begDate']
        endDate = params['endDate']
        personId = params['personId']
        MKBFilter = params.get('MKBFilter', 0)
        MKBFrom = params.get('MKBFrom', '')
        MKBTo = params.get('MKBTo', '')
        description = [dateRangeAsStr(u'за период', begDate, endDate)]
        if personId:
            personName = forceString(db.translate('vrbPersonWithSpeciality', 'id', personId, 'name'))
            description.append(u'врач: %s' % personName)
        if MKBFilter == 1:
            description.append(u'код МКБ с "%s" по "%s"' % (MKBFrom, MKBTo))
        elif MKBFilter == 2:
            description.append(u'код МКБ пуст')
        columns = [('100%', [], CReportBase.AlignLeft)]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()

    def build(self, params):
        query = getQuery(params)

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        tableColumns = [
            ('3%',  [u'№ п/п'], CReportBase.AlignLeft),
            ('12%', [u'ФИО пациента'], CReportBase.AlignLeft),
            ('5%', [u'Дата рождения'], CReportBase.AlignLeft),
            ('2%', [u'Пол'], CReportBase.AlignLeft),
            ('15%', [u'Телефон'], CReportBase.AlignLeft),
            ('15%', [u'Адрес'], CReportBase.AlignLeft),
            ('10%', [u'Врач'], CReportBase.AlignLeft),
            ('3%', [u'МКБ'], CReportBase.AlignLeft),
            ('5%', [u'Дата взятия на Д-учет'], CReportBase.AlignLeft),
            ('5%', [u'Дата предыдущей явки'], CReportBase.AlignLeft),
            ('10%',  [u'Запланированный период'], CReportBase.AlignLeft),
            ('5%', [u'Дата явки'], CReportBase.AlignLeft),
            ('10%',  [u'Период следующей явки'], CReportBase.AlignLeft)
        ]

        table = createTable(cursor, tableColumns)
        rowNumber = 0
        while query.next():
            record = query.record()
            row = table.addRow()
            rowNumber += 1
            table.setText(row, 0, rowNumber)
            table.setText(row, 1, forceString(record.value('clientName')))
            table.setText(row, 2, formatDate(record.value('clientBirthDate')))
            table.setText(row, 3, formatSex(record.value('clientSex')))
            table.setText(row, 4, forceString(record.value('contacts')))
            table.setText(row, 5, forceString(record.value('address')))
            table.setText(row, 6, forceString(record.value('personName')))
            table.setText(row, 7, forceString(record.value('MKB')))
            table.setText(row, 8, formatDate(forceDate(record.value('dispanserBegDate'))))
            table.setText(row, 9, formatDate(forceDate(record.value('lastVisitDate'))))
            table.setText(row, 10, forceString(record.value('curPeriod')))
            table.setText(row, 11, formatDate(forceDate(record.value('visitDate'))))
            table.setText(row, 12, forceString(record.value('nextVisitDate')))

        return doc


class CDiagnosisDispansNoVisitReport(CDiagnosisDispansPlanedListReport):
    def __init__(self, parent):
        CDiagnosisDispansPlanedListReport.__init__(self, parent)
        self.setTitle(u'Отчет по неявившимся на диспансерный осмотр')


    def build(self, params):
        params['noVisit'] = True
        query = getQuery(params)

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        tableColumns = [
            ('3%', [u'№ п/п'], CReportBase.AlignLeft),
            ('12%', [u'ФИО пациента'], CReportBase.AlignLeft),
            ('5%', [u'Дата рождения'], CReportBase.AlignLeft),
            ('2%', [u'Пол'], CReportBase.AlignLeft),
            ('15%', [u'Телефон'], CReportBase.AlignLeft),
            ('15%', [u'Адрес'], CReportBase.AlignLeft),
            ('10%', [u'Врач'], CReportBase.AlignLeft),
            ('3%', [u'МКБ'], CReportBase.AlignLeft),
            ('5%', [u'Дата взятия на Д-учет'], CReportBase.AlignLeft),
            ('5%', [u'Дата предыдущей явки'], CReportBase.AlignLeft),
            ('10%', [u'Запланированный период'], CReportBase.AlignLeft),
            ('10%', [u'Период следующей явки'], CReportBase.AlignLeft)
        ]

        table = createTable(cursor, tableColumns)
        rowNumber = 0
        while query.next():
            record = query.record()
            row = table.addRow()
            rowNumber += 1
            table.setText(row, 0, rowNumber)
            table.setText(row, 1, forceString(record.value('clientName')))
            table.setText(row, 2, formatDate(record.value('clientBirthDate')))
            table.setText(row, 3, formatSex(record.value('clientSex')))
            table.setText(row, 4, forceString(record.value('contacts')))
            table.setText(row, 5, forceString(record.value('address')))
            table.setText(row, 6, forceString(record.value('personName')))
            table.setText(row, 7, forceString(record.value('MKB')))
            table.setText(row, 8, formatDate(forceDate(record.value('dispanserBegDate'))))
            table.setText(row, 9, formatDate(forceDate(record.value('lastVisitDate'))))
            table.setText(row, 10, forceString(record.value('curPeriod')))
            table.setText(row, 11, forceString(record.value('nextVisitDate')))

        return doc
