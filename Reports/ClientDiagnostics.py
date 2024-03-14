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

from library.ICDUtils   import getMKBName
from library.Utils      import forceDate, forceString
from Registry.Utils     import getClientBanner
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable


def selectData(clientId, begDate, endDate, eventPurposeId, specialityId, personId):
    stmt="""
SELECT 
    vrbPerson.name AS person,
    rbSpeciality.name AS speciality,
    Diagnostic.endDate AS date,
    rbDiagnosisType.name AS type,
    rbHealthGroup.name AS healthGroup,
    rbDiseaseCharacter.name AS diseaseCharacter,
    rbDiseasePhases.name AS diseasePhases,
    rbDiseaseStage.name AS diseaseStage,
    rbDispanser.name AS dispanser,
    rbTraumaType.name AS traumaType,
    rbDiagnosticResult.name AS result,
    EventType.purpose_id  AS purpose,
    Diagnosis.MKB AS MKB,
    Diagnosis.MKBEx AS MKBEx
FROM
    Diagnostic
        LEFT JOIN
    Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id
        LEFT JOIN
    rbDiagnosisType ON rbDiagnosisType.id = Diagnostic.diagnosisType_id
        LEFT JOIN
    vrbPerson ON vrbPerson.id = Diagnostic.person_id
        LEFT JOIN
    rbSpeciality ON rbSpeciality.id = Diagnostic.speciality_id
        LEFT JOIN
    rbHealthGroup ON rbHealthGroup.id = Diagnostic.healthGroup_id
        LEFT JOIN
    rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnostic.character_id
        LEFT JOIN
    rbDiseasePhases ON rbDiseasePhases.id = Diagnostic.phase_id
        LEFT JOIN
    rbDiseaseStage ON rbDiseaseStage.id = Diagnostic.stage_id
        LEFT JOIN
    rbDispanser ON rbDispanser.id = Diagnostic.dispanser_id
        LEFT JOIN
    rbTraumaType ON rbTraumaType.id = Diagnostic.traumaType_id
        LEFT JOIN
    rbDiagnosticResult ON rbDiagnosticResult.id = Diagnostic.result_id
        LEFT JOIN
    Event ON Event.id = Diagnostic.event_id
        LEFT JOIN
    EventType ON EventType.id = Event.eventType_id
WHERE
  rbDiagnosisType.code in ('1','2','3','4','98')
  AND %s
ORDER BY
  Diagnostic.endDate DESC , vrbPerson.name DESC
    """
    db = QtGui.qApp.db
    tableDiagnostic = db.table('Diagnostic')
    tableDiagnosis = db.table('Diagnosis')
    tableEventType = db.table('EventType')
    cond = [ tableDiagnostic['deleted'].eq(0)]
    if clientId:
        cond.append(tableDiagnosis['client_id'].eq(clientId))
    if begDate:
        cond.append(tableDiagnostic['endDate'].ge(begDate))
    if endDate:
        cond.append(tableDiagnostic['endDate'].le(endDate))
    if eventPurposeId:
        cond.append(tableEventType['purpose_id'].le(eventPurposeId))
    if specialityId:
        cond.append(tableDiagnostic['speciality_id'].eq(specialityId))
    if personId:
        cond.append(tableDiagnostic['person_id'].eq(personId))
    return db.query(stmt % (db.joinAnd(cond)))


class CClientDiagnostics(CReport):
    name = u'Список диагнозов пациента'
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(self.name)


    def getSetupDialog(self, parent):
        return None


    def build(self, params):
        clientId = params.get('clientId', None)
        begDate = params.get('begDate', None)
        endDate = params.get('endDate', None)
        eventPurposeId = params.get('eventPurposeId', None)
        specialityId = params.get('specialityId', None)
        personId = params.get('personId', None)

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.name)
        cursor.setCharFormat(CReportBase.TableBody)
        cursor.insertBlock()
        cursor.insertHtml(getClientBanner(clientId))
        cursor.insertBlock()

        tableColumns = [
            ('15%', [u'Врач' ], CReportBase.AlignLeft),
            ('15%', [u'Специальность'], CReportBase.AlignLeft),
            ('5%', [u'Установлен' ], CReportBase.AlignLeft),
            ('5%', [u'Тип'], CReportBase.AlignLeft),
            ('5%', [u'ГрЗд'], CReportBase.AlignLeft),
            ('15%', [u'Диагноз'], CReportBase.AlignLeft),
            ('10%', [u'Хар'], CReportBase.AlignLeft),
            ('5%', [u'Фаза'], CReportBase.AlignLeft),
            ('5%', [u'Ст'], CReportBase.AlignLeft),
            ('5%', [u'ДН'], CReportBase.AlignLeft),
            ('5%', [u'Тр'], CReportBase.AlignLeft),
            ('5%', [u'Результат'], CReportBase.AlignLeft),
            ('5%', [u'Назначение'], CReportBase.AlignLeft),
            ]
        table = createTable(cursor, tableColumns)

        query = selectData(clientId, begDate, endDate, eventPurposeId, specialityId, personId)
        while query.next():
            record  = query.record()
            i = table.addRow()
            table.setText(i, 0, forceString(record.value('person')))
            table.setText(i, 1, forceString(record.value('speciality')))
            table.setText(i, 2, forceString(forceDate(record.value('date'))))
            table.setText(i, 3, forceString(record.value('type')))
            table.setText(i, 4, forceString(record.value('healthGroup')))
            table.setText(i, 6, forceString(record.value('diseaseCharacter')))
            table.setText(i, 7, forceString(record.value('diseasePhases')))
            table.setText(i, 8, forceString(record.value('diseaseStage')))
            table.setText(i, 9, forceString(record.value('dispanser')))
            table.setText(i, 10, forceString(record.value('traumaType')))
            table.setText(i, 11, forceString(record.value('traumaType')))
            table.setText(i, 12, forceString(record.value('result')))
            diagnosis = []
            MKB = forceString(record.value('MKB'))
            MKBEx = forceString(record.value('MKBEx'))
            if MKB:
                diagnosis.append(MKB+': '+getMKBName(MKB))
            if MKBEx:
                diagnosis.append(MKBEx+': '+getMKBName(MKBEx))
            table.setText(i, 5, '\n'.join(diagnosis))
        return doc
