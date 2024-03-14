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
from PyQt4.QtCore import pyqtSignature, QDate

from library.MapCode    import createMapCodeToRowIdx
from library.Utils      import forceInt, forceString

from Orgs.Utils         import getOrgStructureDescendants
from Events.Utils       import getWorkEventTypeFilter
from Reports.Report     import CReport, normalizeMKB
from Reports.ReportBase import CReportBase, createTable

from Reports.Ui_ReportDiseaseInPermilleSetup import Ui_DiseaseInPermilleDialog


MainRows = [
    ( u'Некоторые инфекционные и паразитарные болезни', u'A00-B99'),
    ( u'в т.ч. туберкулез',u'A15-A19'),
    ( u'Болезни эндокринной системы', u'E00-E90'),
    ( u'В т.ч. сахарный диабет', u'E10-E14'),
    ( u'Болезни нервной системы', u'G00-G99'),
    ( u'Болезни глаз и его придаточного аппарата', u'H00-H59'),
    ( u'Болезни уха и сосцевидного отростка', u'H60-H95'),
    ( u'Болезни системы кровообращения', u'I00-I99'),
    ( u'В т.ч. ИБС', u'I20-I25'),
    ( u'В т.ч. острый инфаркт миокарда', u'I21'),
    ( u'В т.ч. болезни, характеризующиеся. повышенным кровяным давлением (ГБ)', u'I10-I13'),
    ( u'В т.ч. цереброваскулярные болезни', u'I60-I69'),
    ( u'В т.ч. Болезни артерий, вен', u'I70-I89'),
    ( u'В т.ч. ишемический неуточненный инсульт', u'S63- S66'),
    ( u'Новообразования', u'C00-D89'),
    ( u'Болезни крови, кроветворных органов', u'D50-D89'),
    ( u'Болезни органов дыхания', u'J00-J99'),
    ( u'В т.ч. острая пневмония', u'J12-J18'),
    ( u'В т.ч. бронхиальная астма', u'J45'),
    ( u'Болезни органов пищеварения', u'K00-K93'),
    ( u'Болезни кожи и подкожной клетчатки', u'L00-L99'),
    ( u'В т.ч. абсцессы кожи, фурункулы, карбункулы, лимфадениты, кисты и др.', u'L02-L05'),
    ( u'Болезни ногтей', u'L60.0'),
    ( u'Болезни костно-мышечной системы', u'M00-M99'),
    ( u'Болезни мочеполовой системы', u'N00-N99'),
    ( u'В т.ч. болезни почек', u'N00-N20'),
    ( u'В т.ч. МКБ и др.болезни почек и мочеточников', u'N20-N37'),
    ( u'В т.ч. заболевания мужских половых органов', u'N40-N51'),
    #( u'В т.ч. заболевания женских половых органов', u'NN'), ????????????????????????????????????????
    ( u'Беременность, роды, послеродовой период', u'O00-O99'),
    ( u'Травмы, отравления и некоторые другие последствия воздействий внешних причин', u'S00-T98'),
    ( u'Z00-Z99 - профилактика', u'Z00-Z99'),
]


def selectData(begDate, endDate, eventPurposeId, eventTypeId, orgStructureId, personId, sex, ageFrom, ageTo, isPersonPost):
    stmt="""
SELECT
   Diagnosis.MKB AS MKB,
   COUNT(Visit.id) AS sickCount

FROM Diagnosis
INNER JOIN Client ON Client.id = Diagnosis.client_id
INNER JOIN Diagnostic ON Diagnostic.diagnosis_id = Diagnosis.id
INNER JOIN Event ON Event.id = Diagnostic.event_id
INNER JOIN Visit ON Visit.event_id = Event.id
LEFT JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnosis.character_id
WHERE %s
GROUP BY MKB
    """
    db = QtGui.qApp.db
    tableDiagnosis  = db.table('Diagnosis')
    tableDiseaseCharacter = db.table('rbDiseaseCharacter')
    tableClient = db.table('Client')
    tableDiagnostic = db.table('Diagnostic')
    tablePerson = db.table('Person')
    tableEvent = db.table('Event')
    tableVisit = db.table('Visit')

    cond = []
    cond.append(tableDiagnosis['deleted'].eq(0))
    cond.append(tableVisit['deleted'].eq(0))
    cond.append(tableDiagnostic['deleted'].eq(0))
    cond.append(tableDiagnosis['mod_id'].isNull())
    cond.append(db.joinOr([tableDiagnosis['setDate'].isNull(), tableDiagnosis['setDate'].lt(endDate.addDays(1))]))
    cond.append(db.joinOr([tableDiagnosis['endDate'].ge(begDate), tableDiseaseCharacter['code'].eq('3')]))

    diagnosticQuery = tableDiagnostic
    diagnosticCond = [ tableDiagnostic['diagnosis_id'].eq(tableDiagnosis['id']),
                       tableDiagnostic['deleted'].eq(0)
                     ]
    if isPersonPost:
        tableRBPost = db.table('rbPost')
        diagnosticQuery = diagnosticQuery.innerJoin(tablePerson, tablePerson['id'].eq(tableDiagnostic['person_id']))
        diagnosticQuery = diagnosticQuery.innerJoin(tableRBPost, tableRBPost['id'].eq(tablePerson['post_id']))
        diagnosticCond.append(tablePerson['deleted'].eq(0))
        if isPersonPost == 1:
            diagnosticCond.append('''LEFT(rbPost.code, 1) IN ('1','2','3') ''')
        elif isPersonPost == 2:
            diagnosticCond.append('''LEFT(rbPost.code, 1) IN ('4','5','6','7','8','9')''')
    if personId:
        diagnosticCond.append(tableDiagnostic['person_id'].eq(personId))
    elif orgStructureId:
        if not isPersonPost:
            diagnosticQuery = diagnosticQuery.leftJoin(tablePerson, tablePerson['id'].eq(tableDiagnostic['person_id']))
        diagnosticCond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureDescendants(orgStructureId)))
    else:
        if not isPersonPost:
            diagnosticQuery = diagnosticQuery.leftJoin(tablePerson, tablePerson['id'].eq(tableDiagnostic['person_id']))
        diagnosticCond.append(tablePerson['org_id'].eq(QtGui.qApp.currentOrgId()))
    if eventTypeId:
        diagnosticQuery = diagnosticQuery.leftJoin(tableEvent, tableEvent['id'].eq(tableDiagnostic['event_id']))
        diagnosticCond.append(tableEvent['eventType_id'].eq(eventTypeId))
    elif eventPurposeId:
        tableEventType = db.table('EventType')
        diagnosticQuery = diagnosticQuery.leftJoin(tableEvent, tableEvent['id'].eq(tableDiagnostic['event_id']))
        diagnosticQuery = diagnosticQuery.leftJoin(tableEventType, tableEventType['id'].eq(tableEvent['eventType_id']))
        diagnosticCond.append(tableEventType['purpose_id'].eq(eventPurposeId))
    cond.append(db.existsStmt(diagnosticQuery, diagnosticCond))
    if sex:
        cond.append(tableClient['sex'].eq(sex))
    if ageFrom <= ageTo:
        cond.append('Diagnosis.endDate >= ADDDATE(Client.birthDate, INTERVAL %d YEAR)'%ageFrom)
        cond.append('Diagnosis.endDate < SUBDATE(ADDDATE(Client.birthDate, INTERVAL %d YEAR),1)'%(ageTo+1))

    return db.query(stmt % (db.joinAnd(cond)))


class CStatReportDiseaseInPermilleSetupDialog(QtGui.QDialog, Ui_DiseaseInPermilleDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.patientRequired = False
        self.setupUi(self)
        self.cmbEventPurpose.setTable('rbEventTypePurpose', True, filter='code != \'0\'')
        self.cmbEventType.setTable('EventType', True, filter=getWorkEventTypeFilter(isApplyActive=True))
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.cmbEventPurpose.setValue(params.get('eventPurposeId', None))
        self.cmbEventType.setValue(params.get('eventTypeId', None))
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.cmbPerson.setValue(params.get('personId', None))
        self.cmbSex.setCurrentIndex(params.get('sex', 0))
        self.edtAgeFrom.setValue(params.get('ageFrom', 0))
        self.edtAgeTo.setValue(params.get('ageTo', 150))
        self.edtCountPermille.setValue(params.get('countPermille', 1000))


    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['eventPurposeId'] = self.cmbEventPurpose.value()
        result['eventTypeId'] = self.cmbEventType.value()
        result['orgStructureId'] = self.cmbOrgStructure.value()
        result['personId'] = self.cmbPerson.value()
        result['sex'] = self.cmbSex.currentIndex()
        result['ageFrom'] = self.edtAgeFrom.value()
        result['ageTo'] = self.edtAgeTo.value()
        result['countPermille'] = self.edtCountPermille.value()
        return result


    @pyqtSignature('QDate')
    def on_edtBegDate_dateChanged(self, date):
        self.cmbPerson.setBegDate(date)


    @pyqtSignature('QDate')
    def on_edtEndDate_dateChanged(self, date):
        self.cmbPerson.setEndDate(date)


    @pyqtSignature('int')
    def on_cmbEventPurpose_currentIndexChanged(self, index):
        eventPurposeId = self.cmbEventPurpose.value()
        if eventPurposeId:
            filter = 'EventType.purpose_id =%d' % eventPurposeId
        else:
            filter = getWorkEventTypeFilter(isApplyActive=True)
        self.cmbEventType.setFilter(filter)


    @pyqtSignature('int')
    def on_cmbOrgStructure_currentIndexChanged(self, index):
        orgStructureId = self.cmbOrgStructure.value()
        self.cmbPerson.setOrgStructureId(orgStructureId)


class CStatReportDiseaseInPermille(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        title = u'Отчет по заболеваниям в промилях'
        self.setTitle(title, u'Отчет по заболеваниям в промилях')


    def getDefaultParams(self):
        result = CReport.getDefaultParams(self)
        result['ageFrom']     = 18
        result['ageTo']       = 150
        return result


    def getSetupDialog(self, parent):
        result = CStatReportDiseaseInPermilleSetupDialog(parent)
        result.setTitle(self.title())
        return result


    def build(self, params):
        mapMainRows = createMapCodeToRowIdx( [row[1] for row in MainRows] )
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        eventPurposeId = params.get('eventPurposeId', None)
        eventTypeId = params.get('eventTypeId', None)
        orgStructureId = params.get('orgStructureId', None)
        personId = params.get('personId', None)
        sex = params.get('sex', 0)
        ageFrom = params.get('ageFrom', 18)
        ageTo = params.get('ageTo', 150)
        countPermille = params.get('countPermille', 1000)
        isPersonPost = params.get('isPersonPost', 0)
#        reportData = []
        reportLine = None

        rowSize = 1
#        getObservedSum = 0
#        eventTypeDDSum = 0
#        eventIdList = []
        reportMainData = [ [0]*rowSize for row in xrange(len(MainRows)) ]
        query = selectData(begDate, endDate, eventPurposeId, eventTypeId, orgStructureId, personId, sex, ageFrom, ageTo, isPersonPost)
        while query.next():
            record    = query.record()
            MKB       = normalizeMKB(forceString(record.value('MKB')))
            sickCount = forceInt(record.value('sickCount'))
            for row in mapMainRows.get(MKB, []):
                reportLine = reportMainData[row]
                reportLine[0] += sickCount

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        strCountPermille = u'На ' + str(countPermille) + u' чел. насел.'
        tableColumns = [
            ('40%', [u'Классы болезней, в т.ч. некоторые виды заболеваний', u''], CReportBase.AlignLeft),
            ('20%',  [u'Код по МКБ-10 пересмотра', u''], CReportBase.AlignLeft),
            ('20%',  [u'Количество посещений', u'Абс.'], CReportBase.AlignRight),
            ('20%',  [u'', strCountPermille], CReportBase.AlignRight),
            ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1) # Наименование
        table.mergeCells(0, 1, 2, 1) # Код МКБ
        table.mergeCells(0, 2, 1, 2)

        for row, rowDescr in enumerate(MainRows):
            reportLine = reportMainData[row]
            i = table.addRow()
            table.setText(i, 0, rowDescr[0])
            table.setText(i, 1, rowDescr[1])
            for col in xrange(rowSize):
                absVisits = reportLine[col]
                procentVisits = round(absVisits/(countPermille * 1.0), 2) if countPermille else 0.0
                table.setText(i, 2+col, absVisits)
                table.setText(i, 3+col, procentVisits)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        return doc
