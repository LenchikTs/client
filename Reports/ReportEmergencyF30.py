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
from PyQt4.QtCore import QDate, QDateTime, QTime, pyqtSignature

from library.Utils      import forceDateTime, forceInt, forceRef
from Orgs.Utils         import getOrgStructureFullName
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.Utils      import getKladrClientRural

from Reports.Ui_EmergencyF30Setup    import Ui_EmergencyF30SetupDialog


Rows2350 = [
            (u'Число больных с острым и повторным инфарктом миокарда (I21, I22)', u'1'),
            (u'с острыми цереброваскулярными болезнями, которым оказана скорая медицинская помощь (I60-I69)', u'2'),
            (u'Из числа больных с острым и повторным инфарктом миокарда и с острыми цереброваскулярными болезнями в автомобиле СМП проведено тромболизисов всего (I21, I22, I60-I69, Y44.5)', u'3'),
            (u'из них при остром и повторном инфаркте миокарда (I21, I22, Y44.5)', u'4'),
            (u'при острых цереброваскулярных болезнях (I60-I69, Y44.5)', u'5'),
            (u'Из числа больных с острым и повторным инфарктом миокарда и с острыми цереброваскулярнымиболезнями, число больных смерть которых наступила в автомобиле СМП (I21, I22, I60-I69)', u'6'),
            (u'Число безрезультатных выездов', u'7'),
            (u'Отказано за необоснованностью вызова', u'8'),
            (u'Число дорожно-транспортных происшествий(ДТП), на которые выезжали автомобили СМП', u'9'),
            (u'Число пострадавших в ДТП, которым оказана медицинская помощь', u'10'),
            (u'из них со смертельным исходом', u'11'),
            (u'из них смерть наступила в автомобиле СМП', u'12'),
            (u'Число выездов для медицинского обслуживания спортивных и культурно-массовых мероприятий(или общественных мероприятий)всего', u'13')
           ]


class CEmergencyF30SetupDialog(QtGui.QDialog, Ui_EmergencyF30SetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbAttachType.setTable('rbAttachType', True)
        self.setAttachTypeVisible(False)
        self.setMKBFilterVisible(False)
        self.setAgeVisible(False)


    def setAgeVisible(self, value):
        self.ageVisible = value
        self.lblAge.setVisible(value)
        self.edtAgeFrom.setVisible(value)
        self.lblAgeTo.setVisible(value)
        self.edtAgeTo.setVisible(value)
        self.lblAgeYears.setVisible(value)


    def setMKBFilterVisible(self, value):
        self.MKBFilterVisible = value
        self.lblMKB.setVisible(value)
        self.cmbMKBFilter.setVisible(value)
        self.edtMKBFrom.setVisible(value)
        self.edtMKBTo.setVisible(value)


    def setAttachTypeVisible(self, value):
        self.lblAttachType.setVisible(value)
        self.cmbAttachType.setVisible(value)
        if not value:
            self.cmbAttachType.setValue(None)


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.cmbAttachType.setValue(params.get('attachTypeId', None))
        if self.MKBFilterVisible:
            MKBFilter = params.get('MKBFilter', 0)
            self.cmbMKBFilter.setCurrentIndex(MKBFilter if MKBFilter else 0)
            self.edtMKBFrom.setText(params.get('MKBFrom', 'A00'))
            self.edtMKBTo.setText(params.get('MKBTo',   'Z99.9'))
        if self.ageVisible:
            self.edtAgeFrom.setValue(params.get('ageFrom', 0))
            self.edtAgeTo.setValue(params.get('ageTo', 150))


    def params(self):
        result = {}
        result['begDate']        = self.edtBegDate.date()
        result['endDate']        = self.edtEndDate.date()
        result['orgStructureId'] = self.cmbOrgStructure.value()
        result['attachTypeId']   = self.cmbAttachType.value()
        if self.MKBFilterVisible:
            result['MKBFilter']      = self.cmbMKBFilter.currentIndex()
            result['MKBFrom']        = unicode(self.edtMKBFrom.text())
            result['MKBTo']          = unicode(self.edtMKBTo.text())
        if self.ageVisible:
            result['ageFrom'] = self.edtAgeFrom.value()
            result['ageTo'] = self.edtAgeTo.value()
        return result


    @pyqtSignature('int')
    def on_cmbMKBFilter_currentIndexChanged(self, index):
        self.edtMKBFrom.setEnabled(index == 1)
        self.edtMKBTo.setEnabled(index == 1)



class CReportEmergencyF30(CReport):
    def __init__(self, parent = None):
        CReport.__init__(self, parent)
        self.clientDeath = 8


    def getSetupDialog(self, parent):
        result = CEmergencyF30SetupDialog(parent)
        self.emergencyF30SetupDialog = result
        return result


    def dumpParams(self, cursor, params):
        orgStructureId = params.get('orgStructureId', None)
        params.pop('orgStructureId')
        description = self.getDescription(params)
        if orgStructureId:
            description.insert(-1, u'зона обслуживания: ' + getOrgStructureFullName(orgStructureId))
        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


class CReportEmergencyF302350(CReportEmergencyF30):
    def __init__(self, parent = None):
        CReportEmergencyF30.__init__(self, parent)
        self.emergencyF30SetupDialog = None
        self.setTitle(u'Таблица 2350. Медицинская помощь при выездах')


    def build(self, params):
        db = QtGui.qApp.db
        begDate = forceDateTime(params.get('begDate', QDateTime()))
        endDate = forceDateTime(params.get('endDate', QDateTime()))
        orgStructureId = params.get('orgStructureId', None)
        begDate.setTime(QTime(0, 0))
        endDate.setTime(QTime(23, 59))
        if begDate and endDate:
            db = QtGui.qApp.db
            tableEvent = db.table('Event')
            tableEmergencyCall = db.table('EmergencyCall')
            tableRBEventTypePurpose = db.table('rbEventTypePurpose')
            tableEventType = db.table('EventType')
            tableRBEmergencyAccident = db.table('rbEmergencyAccident')
            tableRBEmergencyCauseCall = db.table('rbEmergencyCauseCall')
            tableRBResult = db.table('rbResult')
            tableDiagnosis = db.table('Diagnosis')
            tableRBDiagnosisType = db.table('rbDiagnosisType')
            tableRBEmergencyDeath = db.table('rbEmergencyDeath')
            tableRBDiseaseCharacter = db.table('rbDiseaseCharacter')
            tableOrgStructure = db.table('OrgStructure')
            stmt = u''' SELECT Event.client_id AS clientId, Event.id AS eventId,
                        IF(rbResult.code = '11', 1, 0) AS A,
                        IF(rbResult.code = '4', 1, 0) AS B,
                        %s AS clientRural
                        FROM Event
                        INNER JOIN EventType ON Event.eventType_id =  EventType.id
                        INNER JOIN rbEventTypePurpose ON EventType.purpose_id = rbEventTypePurpose.id
                        INNER JOIN EmergencyCall ON EmergencyCall.event_id = Event.id
                        INNER JOIN rbResult ON rbResult.id = Event.result_id
                        LEFT JOIN OrgStructure ON OrgStructure.id = EmergencyCall.orgStructure_id
                        INNER JOIN Client ON Client.id = Event.client_id
                        WHERE %s
                        GROUP BY Event.id'''
            cond = [tableRBEventTypePurpose['code'].eq(7),
                    tableEvent['deleted'].eq(0),
                    tableEmergencyCall['deleted'].eq(0),
                    tableEventType['deleted'].eq(0),
                    tableEvent['setDate'].isNotNull(),
                    tableEvent['execDate'].isNotNull(),
                    tableEvent['setDate'].ge(begDate),
                    tableEvent['setDate'].lt(endDate)
                   ]
            if orgStructureId:
                orgStructureIdList = db.getDescendants('OrgStructure', 'parent_id', orgStructureId)
                if orgStructureIdList:
                    cond.append(tableOrgStructure['deleted'].eq(0))
                    cond.append(tableOrgStructure['id'].inlist(orgStructureIdList))
            query = db.query(stmt % (getKladrClientRural(), db.joinAnd(cond)))
            eventIdList = []
            A = 0
            AR = 0
            B = 0
            BR = 0
            C = 0
            CR = 0
            D = 0
            DR = 0
            E = 0
            ER = 0
            F = 0
            FR = 0
            while query.next():
                record = query.record()
                eventId = forceRef(record.value('eventId'))
                if eventId not in eventIdList:
                    eventIdList.append(eventId)
                    clientRural = forceInt(record.value('clientRural'))
                    if forceInt(record.value('A')):
                        A += 1
                        AR += clientRural
                    if forceInt(record.value('B')):
                        B += 1
                        BR += clientRural
            stmt2 = u'''SELECT Event.client_id AS clientId, Event.id AS eventId,
                        IF(Event.id IS NOT NULL, 1, 0) AS C,
                        IF(rbResult.code = '1', 1, 0) AS D,
                        IF(rbResult.code = '1' AND EmergencyCall.death_id IN (SELECT DISTINCT rbEmergencyDeath.id
                        FROM rbEmergencyDeath WHERE (rbEmergencyDeath.code = '2' OR rbEmergencyDeath.code = '3')), 1, 0) AS E,
                        IF(rbResult.code = '1' AND EmergencyCall.death_id IN (SELECT DISTINCT rbEmergencyDeath.id
                        FROM rbEmergencyDeath WHERE (rbEmergencyDeath.code = '3')), 1, 0) AS F,
                        %s AS clientRural
                        FROM Event
                        LEFT JOIN EventType ON Event.eventType_id =  EventType.id
                        LEFT JOIN rbEventTypePurpose ON EventType.purpose_id = rbEventTypePurpose.id
                        LEFT JOIN EmergencyCall ON EmergencyCall.event_id = Event.id
                        LEFT JOIN rbResult ON rbResult.id = Event.result_id
                        LEFT JOIN rbEmergencyAccident ON rbEmergencyAccident.id = EmergencyCall.accident_id
                        LEFT JOIN OrgStructure ON OrgStructure.id = EmergencyCall.orgStructure_id
                        INNER JOIN Client ON Client.id = Event.client_id
                        WHERE %s
                        GROUP BY Event.id'''
            cond.append(tableRBEmergencyAccident['code'].eq(3))
            if orgStructureId:
                orgStructureIdList = db.getDescendants('OrgStructure', 'parent_id', orgStructureId)
                if orgStructureIdList:
                    cond.append(tableOrgStructure['deleted'].eq(0))
                    cond.append(tableOrgStructure['id'].inlist(orgStructureIdList))
            query2 = db.query(stmt2 % (getKladrClientRural(), db.joinAnd(cond)))
            eventIdList2 = []
            while query2.next():
                record = query2.record()
                eventId = forceRef(record.value('eventId'))
                if eventId not in eventIdList2:
                    eventIdList2.append(eventId)
                    clientRural = forceInt(record.value('clientRural'))
                    if forceInt(record.value('C')):
                        C += 1
                        CR += clientRural
                    if forceInt(record.value('D')):
                        D += 1
                        DR += clientRural
                    if forceInt(record.value('E')):
                        E += 1
                        ER += clientRural
                    if forceInt(record.value('F')):
                        F += 1
                        FR += clientRural
            stmt3 = u'''SELECT Event.client_id AS clientId, Event.id AS eventId,
                        IF(Event.id IS NOT NULL, 1, 0) AS G,
                        %s AS clientRural
                        FROM Event
                        INNER JOIN EventType ON Event.eventType_id =  EventType.id
                        INNER JOIN rbEventTypePurpose ON EventType.purpose_id = rbEventTypePurpose.id
                        INNER JOIN EmergencyCall ON EmergencyCall.event_id = Event.id
                        INNER JOIN rbEmergencyCauseCall ON rbEmergencyCauseCall.id = EmergencyCall.causeCall_id
                        LEFT JOIN OrgStructure ON OrgStructure.id = EmergencyCall.orgStructure_id
                        INNER JOIN Client ON Client.id = Event.client_id
                        WHERE %s
                        GROUP BY Event.id'''
            cond = [tableRBEventTypePurpose['code'].eq(7),
                    tableEvent['deleted'].eq(0),
                    tableEmergencyCall['deleted'].eq(0),
                    tableEventType['deleted'].eq(0),
                    tableEvent['setDate'].isNotNull(),
                    tableEvent['execDate'].isNotNull(),
                    tableEvent['setDate'].ge(begDate),
                    tableEvent['setDate'].lt(endDate),
                    tableRBEmergencyCauseCall['typeCause'].eq(1)
                   ]
            if orgStructureId:
                orgStructureIdList = db.getDescendants('OrgStructure', 'parent_id', orgStructureId)
                if orgStructureIdList:
                    cond.append(tableOrgStructure['deleted'].eq(0))
                    cond.append(tableOrgStructure['id'].inlist(orgStructureIdList))
            query3 = db.query(stmt3 % (getKladrClientRural(), db.joinAnd(cond)))
            eventIdList3 = []
            G = 0
            GR = 0
            while query3.next():
                record = query3.record()
                eventId = forceRef(record.value('eventId'))
                if eventId not in eventIdList3:
                    eventIdList3.append(eventId)
                    clientRural = forceInt(record.value('clientRural'))
                    if forceInt(record.value('G')):
                        G += 1
                        GR += clientRural
            H = 0
            HR = 0
            stmtIM = u'''SELECT COUNT(Event.id), SUM(%s) AS clientRural
                        FROM Event
                        LEFT JOIN EventType ON Event.eventType_id =  EventType.id
                        LEFT JOIN rbEventTypePurpose ON EventType.purpose_id = rbEventTypePurpose.id
                        LEFT JOIN EmergencyCall ON EmergencyCall.event_id = Event.id
                        LEFT JOIN rbResult ON rbResult.id = Event.result_id
                        RIGHT JOIN Diagnostic ON Diagnostic.event_id = Event.id
                        LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id
                        LEFT JOIN rbDiagnosisType ON rbDiagnosisType.id = Diagnosis.diagnosisType_id
                        LEFT JOIN OrgStructure ON OrgStructure.id = EmergencyCall.orgStructure_id
                        INNER JOIN Client ON Client.id = Event.client_id
                        WHERE %s'''
            cond = [tableRBEventTypePurpose['code'].eq(7),
                    tableEvent['deleted'].eq(0),
                    tableEmergencyCall['deleted'].eq(0),
                    tableEventType['deleted'].eq(0),
                    tableDiagnosis['deleted'].eq(0),
                    tableEvent['setDate'].isNotNull(),
                    tableEvent['execDate'].isNotNull(),
                    tableEvent['setDate'].ge(begDate),
                    tableEvent['setDate'].lt(endDate),
                    tableRBResult['code'].eq(1),
                    tableRBDiagnosisType['code'].eq(2)
                   ]
            if orgStructureId:
                orgStructureIdList = db.getDescendants('OrgStructure', 'parent_id', orgStructureId)
                if orgStructureIdList:
                    cond.append(tableOrgStructure['deleted'].eq(0))
                    cond.append(tableOrgStructure['id'].inlist(orgStructureIdList))
            cond.append(db.joinOr([tableDiagnosis['MKB'].like(u'I21%'), tableDiagnosis['MKB'].like(u'I22%')]))
            queryIM = db.query(stmtIM % (getKladrClientRural(), db.joinAnd(cond)))
            if queryIM.first():
                H = queryIM.value(0).toInt()[0]
                HR = queryIM.value(1).toInt()[0]
            I = 0
            IR = 0
            stmtZB = u'''SELECT COUNT(Event.id), SUM(%s) AS clientRural
                        FROM Event
                        LEFT JOIN EventType ON Event.eventType_id =  EventType.id
                        LEFT JOIN rbEventTypePurpose ON EventType.purpose_id = rbEventTypePurpose.id
                        LEFT JOIN EmergencyCall ON EmergencyCall.event_id = Event.id
                        LEFT JOIN rbResult ON rbResult.id = Event.result_id
                        INNER JOIN Diagnostic ON Diagnostic.event_id = Event.id
                        LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id
                        LEFT JOIN rbDiagnosisType ON rbDiagnosisType.id = Diagnosis.diagnosisType_id
                        LEFT JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnostic.character_id
                        LEFT JOIN OrgStructure ON OrgStructure.id = EmergencyCall.orgStructure_id
                        INNER JOIN Client ON Client.id = Event.client_id
                        WHERE %s'''
            cond = [tableRBEventTypePurpose['code'].eq(7),
                    tableEvent['deleted'].eq(0),
                    tableEmergencyCall['deleted'].eq(0),
                    tableEventType['deleted'].eq(0),
                    tableDiagnosis['deleted'].eq(0),
                    tableEvent['setDate'].isNotNull(),
                    tableEvent['execDate'].isNotNull(),
                    tableEvent['setDate'].ge(begDate),
                    tableEvent['setDate'].lt(endDate),
                    tableRBResult['code'].eq(1),
                    tableRBDiagnosisType['code'].eq(2),
                    tableDiagnosis['MKB'].like(u'I6%')
                   ]
            if orgStructureId:
                orgStructureIdList = db.getDescendants('OrgStructure', 'parent_id', orgStructureId)
                if orgStructureIdList:
                    cond.append(tableOrgStructure['deleted'].eq(0))
                    cond.append(tableOrgStructure['id'].inlist(orgStructureIdList))
            cond.append(db.joinOr([tableRBDiseaseCharacter['code'].eq(1), tableRBDiseaseCharacter['code'].eq(4)]))
            queryZB = db.query(stmtZB % (getKladrClientRural(), db.joinAnd(cond)))
            if queryZB.first():
                I = queryZB.value(0).toInt()[0]
                IR = queryZB.value(1).toInt()[0]
            J = 0
            JR = 0
            stmtIMDeath = u'''SELECT COUNT(Event.id), SUM(%s) AS clientRural
                                FROM Event
                                INNER JOIN EventType ON Event.eventType_id =  EventType.id
                                INNER JOIN rbEventTypePurpose ON EventType.purpose_id = rbEventTypePurpose.id
                                INNER JOIN EmergencyCall ON EmergencyCall.event_id = Event.id
                                INNER JOIN Diagnostic ON Diagnostic.event_id = Event.id
                                INNER JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id
                                INNER JOIN rbEmergencyDeath ON rbEmergencyDeath.id = EmergencyCall.death_id
                                INNER JOIN rbDiagnosisType ON rbDiagnosisType.id = Diagnosis.diagnosisType_id
                                INNER JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnostic.character_id
                                LEFT JOIN OrgStructure ON OrgStructure.id = EmergencyCall.orgStructure_id
                                INNER JOIN Client ON Client.id = Event.client_id
                                WHERE %s'''
            cond = [tableRBEventTypePurpose['code'].eq(7),
                    tableEvent['deleted'].eq(0),
                    tableEmergencyCall['deleted'].eq(0),
                    tableEventType['deleted'].eq(0),
                    tableDiagnosis['deleted'].eq(0),
                    tableEvent['setDate'].isNotNull(),
                    tableEvent['execDate'].isNotNull(),
                    tableEvent['setDate'].ge(begDate),
                    tableEvent['setDate'].lt(endDate),
                    tableRBDiagnosisType['code'].eq(2),
                    tableRBEmergencyDeath['code'].eq(3)
                   ]
            if orgStructureId:
                orgStructureIdList = db.getDescendants('OrgStructure', 'parent_id', orgStructureId)
                if orgStructureIdList:
                    cond.append(tableOrgStructure['deleted'].eq(0))
                    cond.append(tableOrgStructure['id'].inlist(orgStructureIdList))
            cond.append(db.joinOr([tableDiagnosis['MKB'].like(u'I21%'), tableDiagnosis['MKB'].like(u'I22%'), db.joinAnd([tableDiagnosis['MKB'].like(u'I6%'), db.joinOr([tableRBDiseaseCharacter['code'].eq(1), tableRBDiseaseCharacter['code'].eq(4)])])]))
            queryIMDeath  = db.query(stmtIMDeath % (getKladrClientRural(), db.joinAnd(cond)))
            if queryIMDeath.first():
                J = queryIMDeath.value(0).toInt()[0]
                JR = queryIMDeath.value(1).toInt()[0]
            K = 0
            KR = 0
            stmtTL = u'''SELECT COUNT(Event.id), SUM(%s) AS clientRural
                            FROM Event
                            LEFT JOIN EventType ON Event.eventType_id =  EventType.id
                            LEFT JOIN rbEventTypePurpose ON EventType.purpose_id = rbEventTypePurpose.id
                            LEFT JOIN EmergencyCall ON EmergencyCall.event_id = Event.id
                            LEFT JOIN rbResult ON rbResult.id = Event.result_id
                            INNER JOIN Diagnostic ON Diagnostic.event_id = Event.id
                            LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id
                            LEFT JOIN rbDiagnosisType ON rbDiagnosisType.id = Diagnosis.diagnosisType_id
                            LEFT JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnostic.character_id
                            LEFT JOIN OrgStructure ON OrgStructure.id = EmergencyCall.orgStructure_id
                            INNER JOIN Client ON Client.id = Event.client_id
                            WHERE %s'''
            cond = [tableRBEventTypePurpose['code'].eq(7),
                    tableEvent['deleted'].eq(0),
                    tableEmergencyCall['deleted'].eq(0),
                    tableEventType['deleted'].eq(0),
                    tableDiagnosis['deleted'].eq(0),
                    tableEvent['setDate'].isNotNull(),
                    tableEvent['execDate'].isNotNull(),
                    tableEvent['setDate'].ge(begDate),
                    tableEvent['setDate'].lt(endDate),
                    tableRBResult['code'].eq(1),
                    tableRBDiagnosisType['code'].eq(2),
                    tableDiagnosis['MKBEx'].like(u'Y44.5')
                   ]
            if orgStructureId:
                orgStructureIdList = db.getDescendants('OrgStructure', 'parent_id', orgStructureId)
                if orgStructureIdList:
                    cond.append(tableOrgStructure['deleted'].eq(0))
                    cond.append(tableOrgStructure['id'].inlist(orgStructureIdList))
            cond.append(db.joinOr([tableDiagnosis['MKB'].like(u'I21%'), tableDiagnosis['MKB'].like(u'I22%'), db.joinAnd([tableDiagnosis['MKB'].like(u'I6%'), db.joinOr([tableRBDiseaseCharacter['code'].eq(1), tableRBDiseaseCharacter['code'].eq(4)])])]))
            queryTL = db.query(stmtTL % (getKladrClientRural(), db.joinAnd(cond)))
            if queryTL.first():
                K = queryTL.value(0).toInt()[0]
                KR = queryTL.value(1).toInt()[0]
            K1 = 0
            K1R = 0
            stmtTL1 = u'''SELECT COUNT(Event.id), SUM(%s) AS clientRural
                            FROM Event
                            LEFT JOIN EventType ON Event.eventType_id =  EventType.id
                            LEFT JOIN rbEventTypePurpose ON EventType.purpose_id = rbEventTypePurpose.id
                            LEFT JOIN EmergencyCall ON EmergencyCall.event_id = Event.id
                            LEFT JOIN rbResult ON rbResult.id = Event.result_id
                            INNER JOIN Diagnostic ON Diagnostic.event_id = Event.id
                            LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id
                            LEFT JOIN rbDiagnosisType ON rbDiagnosisType.id = Diagnosis.diagnosisType_id
                            LEFT JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnostic.character_id
                            LEFT JOIN OrgStructure ON OrgStructure.id = EmergencyCall.orgStructure_id
                            INNER JOIN Client ON Client.id = Event.client_id
                            WHERE %s'''
            cond = [tableRBEventTypePurpose['code'].eq(7),
                    tableEvent['deleted'].eq(0),
                    tableEmergencyCall['deleted'].eq(0),
                    tableEventType['deleted'].eq(0),
                    tableDiagnosis['deleted'].eq(0),
                    tableEvent['setDate'].isNotNull(),
                    tableEvent['execDate'].isNotNull(),
                    tableEvent['setDate'].ge(begDate),
                    tableEvent['setDate'].lt(endDate),
                    tableRBResult['code'].eq(1),
                    tableRBDiagnosisType['code'].eq(2),
                    tableDiagnosis['MKBEx'].like(u'Y44.5')
                   ]
            if orgStructureId:
                orgStructureIdList = db.getDescendants('OrgStructure', 'parent_id', orgStructureId)
                if orgStructureIdList:
                    cond.append(tableOrgStructure['deleted'].eq(0))
                    cond.append(tableOrgStructure['id'].inlist(orgStructureIdList))
            cond.append(db.joinOr([tableDiagnosis['MKB'].like(u'I21%'), tableDiagnosis['MKB'].like(u'I22%')]))
            queryTL1 = db.query(stmtTL1 % (getKladrClientRural(), db.joinAnd(cond)))
            if queryTL1.first():
                K1 = queryTL1.value(0).toInt()[0]
                K1R = queryTL1.value(1).toInt()[0]
            K2 = 0
            K2R = 0
            stmtTL2 = u'''SELECT COUNT(Event.id), SUM(%s) AS clientRural
                            FROM Event
                            LEFT JOIN EventType ON Event.eventType_id =  EventType.id
                            LEFT JOIN rbEventTypePurpose ON EventType.purpose_id = rbEventTypePurpose.id
                            LEFT JOIN EmergencyCall ON EmergencyCall.event_id = Event.id
                            LEFT JOIN rbResult ON rbResult.id = Event.result_id
                            INNER JOIN Diagnostic ON Diagnostic.event_id = Event.id
                            LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id
                            LEFT JOIN rbDiagnosisType ON rbDiagnosisType.id = Diagnosis.diagnosisType_id
                            LEFT JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnostic.character_id
                            LEFT JOIN OrgStructure ON OrgStructure.id = EmergencyCall.orgStructure_id
                            INNER JOIN Client ON Client.id = Event.client_id
                            WHERE %s'''
            cond = [tableRBEventTypePurpose['code'].eq(7),
                    tableEvent['deleted'].eq(0),
                    tableEmergencyCall['deleted'].eq(0),
                    tableEventType['deleted'].eq(0),
                    tableDiagnosis['deleted'].eq(0),
                    tableEvent['setDate'].isNotNull(),
                    tableEvent['execDate'].isNotNull(),
                    tableEvent['setDate'].ge(begDate),
                    tableEvent['setDate'].lt(endDate),
                    tableRBResult['code'].eq(1),
                    tableRBDiagnosisType['code'].eq(2),
                    tableDiagnosis['MKBEx'].like(u'Y44.5')
                   ]
            if orgStructureId:
                orgStructureIdList = db.getDescendants('OrgStructure', 'parent_id', orgStructureId)
                if orgStructureIdList:
                    cond.append(tableOrgStructure['deleted'].eq(0))
                    cond.append(tableOrgStructure['id'].inlist(orgStructureIdList))
            cond.append(db.joinAnd([tableDiagnosis['MKB'].like(u'I6%'), db.joinOr([tableRBDiseaseCharacter['code'].eq(1), tableRBDiseaseCharacter['code'].eq(4)])]))
            queryTL2 = db.query(stmtTL2 % (getKladrClientRural(), db.joinAnd(cond)))
            if queryTL2.first():
                K2 = queryTL2.value(0).toInt()[0]
                K2R = queryTL2.value(1).toInt()[0]
            callList = [H, I, K, K1, K2, J, A, B, C, D, E, F, G]
            callListR = [HR, IR, KR, K1R, K2R, JR, AR, BR, CR, DR, ER, FR, GR]
            doc = QtGui.QTextDocument()
            cursor = QtGui.QTextCursor(doc)
            cursor.setCharFormat(CReportBase.ReportTitle)
            cursor.insertText(u'Медицинская помощь при выездах\n(2350)')
            cursor.insertBlock()
            self.dumpParams(cursor, params)
            cursor.setCharFormat(CReportBase.ReportBody)
            cursor.insertBlock()
            self.Rows = [] + Rows2350
            cols = [('50%',[u'Показатели', u'1'], CReportBase.AlignLeft),
                    ('10%',[u'№ строки', u'2'], CReportBase.AlignLeft),
                    ('20%',[u'Число', u'3'], CReportBase.AlignLeft),
                    ('20%',[u'Из них: сельских жителей', u'4'], CReportBase.AlignLeft)]
            table = createTable(cursor, cols)
            for iRow, row in enumerate(self.Rows):
                i = table.addRow()
                for j in xrange(2):
                    table.setText(i, j, row[j])
                table.setText(i, 2, callList[i - 2])
                table.setText(i, 3, callListR[i - 2])
        return doc
