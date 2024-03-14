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

from library.Utils      import forceDate, forceString
from Registry.Utils     import getClientBanner
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable


def selectData(clientId, begDate, endDate, eventPurposeId, specialityId, personId, sceneId, order):
    stmt="""
SELECT
    vrbPerson.name as personName,
    vrbPersonWithSpeciality.name,
    rbSpeciality.name as specialityName,
    rbScene.name as scene,
    DATE(Visit.date) as date,
    EventType.name as typeName,
    rbService.code as serviceName,
    rbFinance.name as financeName,
    (SELECT
        CONCAT_WS(': ', Diagnosis.MKB, tableMKB.DiagName)
    FROM
        Diagnosis
        LEFT JOIN Diagnostic ON Diagnostic.diagnosis_id = Diagnosis.id
        LEFT JOIN MKB AS tableMKB ON tableMKB.DiagID = Diagnosis.MKB
    WHERE
        Diagnostic.event_id = Event.id
            AND Diagnostic.diagnosisType_id IN (1 , 2)
    LIMIT 1
     ) as MKBCode
FROM
    Visit
        LEFT JOIN
    Event ON Event.id = Visit.event_id
        LEFT JOIN
    vrbPerson ON vrbPerson.id = Visit.person_id
        LEFT JOIN
    rbSpeciality ON rbSpeciality.id = vrbPerson.speciality_id
        LEFT JOIN
    vrbPersonWithSpeciality ON vrbPersonWithSpeciality.id = Visit.assistant_id
        LEFT JOIN
    rbScene ON rbScene.id = Visit.scene_id
        LEFT JOIN
    rbVisitType ON rbVisitType.id = Visit.visitType_id
        LEFT JOIN
    rbService ON rbService.id = Visit.service_id
        LEFT JOIN
    rbFinance ON rbFinance.id = Visit.finance_id
        LEFT JOIN
    EventType ON EventType.id = Event.eventType_id
WHERE
    %s
%s
    """
    db = QtGui.qApp.db
    tableVisit = db.table('Visit')
    tableEventType = db.table('EventType')
    tableEvent = db.table('Event')
    tablePerson = db.table('vrbPerson')
    tableScene = db.table('rbScene')
    cond = [ tableVisit['deleted'].eq(0)]
    if clientId:
        cond.append(tableEvent['client_id'].eq(clientId))
    if begDate:
        cond.append(tableVisit['date'].ge(begDate))
    if endDate:
        cond.append(tableVisit['date'].le(endDate))
    if eventPurposeId:
        cond.append(tableEventType['purpose_id'].le(eventPurposeId))
    if specialityId:
        cond.append(tablePerson['speciality_id'].eq(specialityId))
    if personId:
        cond.append(tablePerson['person_id'].eq(personId))
    if sceneId:
        cond.append(tableScene['id'].eq(sceneId))
    return db.query(stmt % (db.joinAnd(cond), (u'ORDER BY %s'%(order)) if order else u''))


class CClientVisits(CReport):
    name = u'Список визитов пациента'
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
        sceneId = params.get('sceneId', None)
        order = params.get('order', None)

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.name)
        cursor.setCharFormat(CReportBase.TableBody)
        cursor.insertBlock()
        cursor.insertHtml(getClientBanner(clientId))
        cursor.insertBlock()

        tableColumns = [
            ('10%', [u'Врач' ], CReportBase.AlignLeft),
            ('15%', [u'Специальность'], CReportBase.AlignLeft),
            ('10%', [u'Место' ], CReportBase.AlignLeft),
            ('15%', [u'Дата' ], CReportBase.AlignLeft),
            ('15%', [u'Тип обращения'], CReportBase.AlignLeft),
            ('10%', [u'Код услуги'], CReportBase.AlignLeft),
            ('10%', [u'Тип финансирования'], CReportBase.AlignLeft),
            ('15%', [u'Диагноз'], CReportBase.AlignLeft),
            ]
        table = createTable(cursor, tableColumns)

        query = selectData(clientId, begDate, endDate, eventPurposeId, specialityId, personId, sceneId, order)
        while query.next():
            record  = query.record()
            i = table.addRow()
            table.setText(i, 0, forceString(record.value('personName')))
            table.setText(i, 1, forceString(record.value('specialityName')))
            table.setText(i, 2, forceString(record.value('scene')))
            table.setText(i, 3, forceString(forceDate(record.value('date'))))
            table.setText(i, 4, forceString(record.value('typeName')))
            table.setText(i, 5, forceString(record.value('serviceName')))
            table.setText(i, 6, forceString(record.value('financeName')))
            table.setText(i, 7, forceString(record.value('MKBCode')))

        return doc
