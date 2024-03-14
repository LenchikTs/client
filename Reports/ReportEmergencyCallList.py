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

#import datetime

from PyQt4 import QtGui
from PyQt4.QtCore import QDate

from library.Utils      import forceRef, forceString, formatDateTime, formatName

from Orgs.Utils         import getOrgStructureDescendants, getOrgStructureFullName
from Reports.Report     import CReport, normalizeMKB
from Reports.ReportBase import CReportBase, createTable


def selectData(params):
    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())
    attachTypeId = params.get('attachTypeId', None)
    if not begDate or not endDate:
        return None
    orgStructureId = params.get('orgStructureId', None)
    stmt="""
SELECT
   Event.id AS eventId,
   Client.id AS clientId,
   Client.lastName,
   Client.firstName,
   Client.patrName,
   Diagnosis.MKB,
   MKB.DiagName,
   CONCAT_WS(' / ', MKB.DiagName, rbMKBSubclass_Item.name) AS nameMKB,
   Event.setDate,
   Event.execDate,
   EmergencyCall.begDate,
   EmergencyCall.passDate,
   EmergencyCall.departureDate,
   EmergencyCall.arrivalDate,
   EmergencyCall.finishServiceDate,
   EmergencyCall.resultCall_id,
   EmergencyCall.causeCall_id,
   rbEmergencyCauseCall.code AS codeCauseCall,
   rbEmergencyCauseCall.name AS nameCauseCall,
   rbEmergencyResult.code AS codeResultCall,
   rbEmergencyResult.name AS nameResultCall

FROM Event
   INNER JOIN Client          ON Client.id = Event.client_id
   INNER JOIN EmergencyCall   ON EmergencyCall.event_id = Event.id
   INNER JOIN Diagnostic      ON Diagnostic.event_id = Event.id
   INNER JOIN Diagnosis       ON Diagnosis.id = Diagnostic.diagnosis_id
   INNER JOIN rbDiagnosisType ON Diagnostic.diagnosisType_id=rbDiagnosisType.id
   LEFT  JOIN MKB             ON MKB.DiagID = LEFT(Diagnosis.MKB, 5)
   LEFT  JOIN rbMKBSubclass_Item ON (rbMKBSubclass_Item.master_id = MKB.MKBSubclass_id
    AND (length(Diagnosis.MKB) = 6 AND rbMKBSubclass_Item.code = RIGHT(Diagnosis.MKB, 1)))
   LEFT JOIN rbEmergencyResult ON rbEmergencyResult.id = EmergencyCall.resultCall_id
   LEFT JOIN rbEmergencyCauseCall ON rbEmergencyCauseCall.id = EmergencyCall.causeCall_id
   %(joinAttach)s

WHERE Event.deleted = 0 AND EmergencyCall.deleted = 0
AND Diagnostic.deleted = 0 AND Diagnosis.deleted = 0
AND (rbDiagnosisType.code = '1'
OR (rbDiagnosisType.code = '2' AND Diagnostic.person_id = Event.execPerson_id
AND (NOT EXISTS (SELECT DC.id FROM Diagnostic AS DC
INNER JOIN rbDiagnosisType AS DT ON DT.id = DC.diagnosisType_id WHERE DT.code = '1'
AND DC.event_id = Event.id LIMIT 1))))
AND %(cond)s

ORDER BY    Client.lastName, Client.firstName, Client.patrName, Diagnosis.MKB
    """
    db = QtGui.qApp.db
    tableEvent  = db.table('Event')
    tableClientAttach = db.table('ClientAttach')
    tableEmergencyCall = db.table('EmergencyCall')
    cond = [tableEvent['setDate'].isNotNull(),
            tableEvent['execDate'].isNotNull(),
            tableEvent['setDate'].le(endDate),
            tableEvent['execDate'].ge(begDate),
            ]
    if orgStructureId:
        cond.append(tableEmergencyCall['orgStructure_id'].inlist(getOrgStructureDescendants(orgStructureId)))
    joinAttach = u''
    if attachTypeId:
        joinAttach = u'''INNER JOIN ClientAttach ON ClientAttach.id = (IF(getClientAttachIdForDate(Event.client_id, 0, Event.setDate),
        getClientAttachIdForDate(Event.client_id, 0, Event.setDate),
        getClientAttachIdForDate(Event.client_id, 1, Event.setDate)))'''
        cond.append(tableClientAttach['attachType_id'].eq(attachTypeId))
        cond.append(tableClientAttach['deleted'].eq(0))
    return db.query(stmt % dict(joinAttach = joinAttach,
                                cond = db.joinAnd(cond)))


class CReportEmergencyCallList(CReport):
    def __init__(self, parent, additionalFields = False):
        CReport.__init__(self, parent)
        self.setTitle(u'Список вызовов (СМП)', u'Список вызовов (СМП)')
        self.additionalFields = additionalFields


    def getSetupDialog(self, parent):
        result = CEmergencyCallListSetupDialog(parent)
        return result


    def dumpParams(self, cursor, params):
        orgStructureId = params.get('orgStructureId', None)
        params.pop('orgStructureId')
        description = self.getDescription(params)
        if orgStructureId:
            description.insert(-1, u'зона обслуживания: ' + getOrgStructureFullName(orgStructureId))
        attachTypeId = params.get('attachTypeId', None)
        if attachTypeId:
            description.append(u'Тип прикрепления: ' + forceString(QtGui.qApp.db.translate('rbAttachType', 'id', attachTypeId, 'name')))
        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        params['orgStructureId'] = orgStructureId


    def build(self, params):
        query = selectData(params)
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        tableColumns = [
            ('20%', [u'ФИО пациента',          u''              ], CReportBase.AlignLeft),
            ( '5%', [u'Время обслуживания',    u'принято'       ], CReportBase.AlignLeft),
            ( '5%', [u'',                      u'передано'      ], CReportBase.AlignLeft),
            ( '5%', [u'',                      u'выезд'         ], CReportBase.AlignLeft),
            ( '5%', [u'',                      u'прибытие'      ], CReportBase.AlignLeft),
            ( '5%', [u'',                      u'оконч. обслуж.'], CReportBase.AlignLeft),
            ( '10%', [u'Код МКБ',               u''              ], CReportBase.AlignRight),
            ( '15%', [u'Расшифровка МКБ',       u''              ], CReportBase.AlignLeft),
            ( '15%', [u'Повод вызова',          u''              ], CReportBase.AlignLeft),
            ( '15%', [u'Результат вызова ',     u''              ], CReportBase.AlignLeft)
            ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 1, 5)
        table.mergeCells(0, 6, 2, 1)
        table.mergeCells(0, 7, 2, 1)
        table.mergeCells(0, 8, 2, 1)
        table.mergeCells(0, 9, 2, 1)
        eventIdList = []
        while query.next():
            record    = query.record()
            eventId   = forceRef(record.value('eventId'))
            if eventId and eventId not in eventIdList:
                eventIdList.append(eventId)
                clientName = formatName(forceString(record.value('lastName')), forceString(record.value('firstName')), forceString(record.value('patrName')))
                MKB = normalizeMKB(forceString(record.value('MKB')))
                nameMKB = forceString(record.value('nameMKB'))
                begDate = formatDateTime(record.value('begDate'))
                passDate = formatDateTime(record.value('passDate'))
                departureDate = formatDateTime(record.value('departureDate'))
                arrivalDate = formatDateTime(record.value('arrivalDate'))
                finishServiceDate = formatDateTime(record.value('finishServiceDate'))
                codeCauseCall = forceString(record.value('codeCauseCall'))
                nameCauseCall = forceString(record.value('nameCauseCall'))
                codeResultCall = forceString(record.value('codeResultCall'))
                nameResultCall = forceString(record.value('nameResultCall'))
                i = table.addRow()
                table.setText(i, 0, clientName)
                table.setText(i, 1, begDate)
                table.setText(i, 2, passDate)
                table.setText(i, 3, departureDate)
                table.setText(i, 4, arrivalDate)
                table.setText(i, 5, finishServiceDate)
                table.setText(i, 6, MKB)
                table.setText(i, 7, nameMKB)
                table.setText(i, 8, codeCauseCall + u'-' + nameCauseCall)
                table.setText(i, 9, codeResultCall + u'-' + nameResultCall)
        return doc


from Ui_EmergencyCallListSetup import Ui_EmergencyCallListSetupDialog


class CEmergencyCallListSetupDialog(QtGui.QDialog, Ui_EmergencyCallListSetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())
        self.cmbAttachType.setTable('rbAttachType', True)


    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.cmbAttachType.setValue(params.get('attachTypeId', None))


    def params(self):
        params = {}
        params['begDate'] = self.edtBegDate.date()
        params['endDate'] = self.edtEndDate.date()
        params['orgStructureId'] = self.cmbOrgStructure.value()
        params['attachTypeId'] = self.cmbAttachType.value()
        return params
