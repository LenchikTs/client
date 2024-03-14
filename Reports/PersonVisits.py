# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## Анализ/Посещаемость/Cводка на врача
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature, QDate

from library.database import addDateInRange
from library.Utils import forceDate, forceRef, forceString, formatDate, formatSNILS, formatNameInt, forceInt, formatSex, \
    calcAge
from Events.Utils import getWorkEventTypeFilter
from Orgs.Orgs import selectOrganisation
from Orgs.Utils import getOrgStructureDescendants
from Reports.Report import CReport
from Reports.ReportBase import CReportBase, createTable

from Ui_PersonVisitsSetup import Ui_PersonVisitsSetupDialog


def selectData(params):
    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())
    eventPurposeId = params.get('eventPurposeId', None)
    eventTypeId = params.get('eventTypeId', None)
    orgStructureId = params.get('orgStructureId', None)
    personId = params.get('personId', None)
    sceneId = params.get('sceneId', None)
    workOrgId = params.get('workOrgId', None)
    sex = params.get('sex', 0)
    ageFrom = params.get('ageFrom', 0)
    ageTo = params.get('ageTo', 150)
    preRecord = params.get('preRecord', 0)
    isPrimary = params.get('isPrimary', 0)
    financeId = params.get('financeId', None)
    isPreliminaryDiagnostics = params.get('isPreliminaryDiagnostics', False)
    accountingSystemId = params.get('accountingSystemId', None)
    if accountingSystemId:
        join = u"""LEFT JOIN rbAccountingSystem r ON r.id = %d
                   LEFT JOIN ClientIdentification ci on ci.accountingSystem_id = r.id 
                                                        and ci.deleted = 0 AND ci.client_id = Client.id
        """ % accountingSystemId
        identifier = 'ci.identifier'
    else:
        join = ''
        identifier = 'Client.id'
    additionalInfo = ''
    if params.get('hasSNILS', False):
        additionalInfo += ', Client.SNILS'
    if params.get('hasRegAddress', False):
        additionalInfo += ', getClientRegAddress(Client.id) as regAddress'
    if params.get('hasLocAddress', False):
        additionalInfo += ', getClientLocAddress(Client.id) as locAddress'
    if params.get('hasPolicy', False):
        additionalInfo += ', getClientPolicyForDate(Client.id, 1, Visit.date, Event.id) as compulsoryPolicy'
        additionalInfo += ', getClientPolicyForDate(Client.id, 0, Visit.date, Event.id) as voluntaryPolicy'
    if params.get('hasDocument', False):
        additionalInfo += ', getClientDocument(Client.id) as clientDocument'
    if params.get('hasWork', False):
        additionalInfo += ', getClientWork(Client.id) as work'
    if params.get('hasSocStatus', False):
        if QtGui.qApp.showingInInfoBlockSocStatus() == 0:
            statusFormat = 'sst.code'
        elif QtGui.qApp.showingInInfoBlockSocStatus() == 1:
            statusFormat = 'sst.name'
        else:
            statusFormat = "CONCAT(sst.code, '-', sst.name, ' ')"
        additionalInfo += """, (SELECT GROUP_CONCAT(%s)
FROM ClientSocStatus cs
LEFT JOIN rbSocStatusClass ssc ON ssc.id = cs.socStatusClass_id
left JOIN rbSocStatusType sst ON sst.id = cs.socStatusType_id
WHERE cs.deleted = 0 AND (cs.endDate is NULL OR cs.endDate >= CURDATE())
AND ssc.code <> '8' AND cs.client_id = Client.id) AS socStatuses """ % statusFormat

    stmt = """
SELECT
    Visit.id AS visit_id,
    Visit.date AS date,
    Event.client_id AS client_id,
    Client.lastName,
    Client.firstName,
    Client.patrName,
    Client.birthDate,
    Client.sex,
    EventType.name AS eventType,
    rbScene.name AS scene,
    Diagnosis.MKB,
    %s
    rbDispanser.name AS dispanser,
    rbFinance.name AS financeName,
    %s as identifier
    %s
FROM Visit
LEFT JOIN Event       ON Event.id = Visit.event_id
LEFT JOIN EventType   ON EventType.id = Event.eventType_id
LEFT JOIN Contract    ON Contract.id = Event.contract_id
LEFT JOIN rbFinance   ON rbFinance.id = Contract.finance_id
LEFT JOIN Person      ON Person.id = Visit.person_id
LEFT JOIN Client      ON Client.id = Event.client_id
LEFT JOIN rbScene     ON rbScene.id = Visit.scene_id
LEFT JOIN Diagnostic  ON Diagnostic.id = IFNULL(getEventPersonDiagnostic(Visit.event_id, Visit.person_id),
                                                getEventDiagnostic(Visit.event_id)
                                               )
LEFT JOIN Diagnosis   ON Diagnosis.id = Diagnostic.diagnosis_id
                         AND Diagnosis.deleted = 0
LEFT JOIN rbDispanser ON rbDispanser.id = Diagnostic.dispanser_id AND Diagnostic.person_id = Visit.person_id
%s
WHERE Visit.deleted = 0
AND Contract.deleted = 0
AND Event.deleted = 0
AND DATE(Event.setDate) <= DATE(Visit.date)
AND %s
ORDER BY Visit.date, Client.lastName, Client.firstName, Client.patrName, Client.birthDate, Client.sex, Visit.id
    """
    db = QtGui.qApp.db
    tableVisit = db.table('Visit')
    tableEvent = db.table('Event')
    tableContract = db.table('Contract')
    tableClient = db.table('Client')
    tablePerson = db.table('Person')
    cond = []

    addDateInRange(cond, tableVisit['date'], begDate, endDate)
    if financeId:
        cond.append(tableContract['finance_id'].eq(financeId))
    if isPrimary:
        cond.append(tableEvent['isPrimary'].eq(1 if isPrimary == 1 else 0))
    if personId:
        cond.append(tableVisit['person_id'].eq(personId))
    elif orgStructureId:
        cond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureDescendants(orgStructureId)))
    else:
        cond.append(tablePerson['org_id'].eq(QtGui.qApp.currentOrgId()))
    if eventTypeId:
        cond.append(tableEvent['eventType_id'].eq(eventTypeId))
    elif eventPurposeId:
        cond.append(db.table('EventType')['purpose_id'].eq(eventPurposeId))
    if sceneId:
        cond.append(tableVisit['scene_id'].eq(sceneId))
    if workOrgId:
        cond.append('EXISTS (SELECT * FROM ClientWork WHERE ClientWork.id = (SELECT MAX(id) FROM ClientWork AS CW WHERE CW.client_id = Client.id) and ClientWork.org_id=%d)' % workOrgId)
    if sex:
        cond.append(tableClient['sex'].eq(sex))
    if ageFrom <= ageTo:
        cond.append('Visit.date >= ADDDATE(Client.birthDate, INTERVAL %d YEAR)' % ageFrom)
        cond.append('Visit.date < SUBDATE(ADDDATE(Client.birthDate, INTERVAL %d YEAR),1)' % (ageTo+1))
#    if preRecord == 1:
#        cond.append(tableEvent['id'].inlist(eventIds))
#    if preRecord == 2:
#        cond.append(tableEvent['id'].notInlist(eventIds))
    preRecordCond = 'EXISTS (SELECT NULL FROM vScheduleItem '            \
                    '       WHERE vScheduleItem.person_id = Person.id'  \
                    '       AND vScheduleItem.client_id = Client.id'   \
                    '       AND vScheduleItem.date = DATE(Visit.date) '\
                    '       AND vScheduleItem.appointmentType = rbScene.appointmentType)'
    if preRecord == 1:
        cond.append(preRecordCond)
    elif preRecord == 2:
        cond.append('NOT '+preRecordCond)
    stmtPreliminaryDiagnostics = u'''(SELECT DS.MKB
                                      FROM Diagnosis AS DS
                                        INNER JOIN Diagnostic AS DC ON DC.diagnosis_id=DS.id
                                        INNER JOIN rbDiagnosisType AS DT ON DC.diagnosisType_id=DT.id
                                      WHERE DC.event_id = Event.id AND DS.deleted = 0 AND DC.deleted = 0
                                        AND DT.code = '7' AND DC.person_id = Event.execPerson_id
                                      ORDER BY DS.id
                                      LIMIT 1) AS MKBPreliminary, ''' if isPreliminaryDiagnostics else u''
    return db.query(stmt % (stmtPreliminaryDiagnostics, identifier, additionalInfo, join, db.joinAnd(cond)))


def produceTotalLine(table, date, cnt):
    if cnt != 0:
        i = table.addRow()
        table.setText(i, 0, u'всего за '+forceString(date), CReportBase.TableTotal)
        table.setText(i, 1, cnt, CReportBase.TableTotal)


def getAdditionalClientInfo(record, params):
    result = []
    if params.get('hasRegAddress', False):
        regAddress = forceString(record.value('regAddress'))
        result += [u'Адрес регистрации:<B>%s</B><BR>' % (regAddress if regAddress else u'нет'), ]
    if params.get('hasLocAddress', False):
        locAddress = forceString(record.value('locAddress'))
        result += [u'Адрес проживания:<B>%s</B><BR>' % (locAddress if locAddress else u'нет'), ]
    if params.get('hasPolicy', False):
        compulsoryPolicy = forceString(record.value('compulsoryPolicy'))
        voluntaryPolicy = forceString(record.value('voluntaryPolicy'))
        result += [u'полис <B>%s</B>%s<BR>' % (compulsoryPolicy if compulsoryPolicy else u'нет',
                                               u'полис ДМС <B>%s</B>' % voluntaryPolicy if voluntaryPolicy else u''), ]
    if params.get('hasDocument', False):
        clientDocument = forceString(record.value('clientDocument'))
        result += [u'Документ:<B>%s</B><BR>' % (clientDocument if clientDocument else u'нет'), ]
    if params.get('hasSNILS', False):
        snils = formatSNILS(forceString(record.value('SNILS')))
        result += [u'СНИЛС: <B>%s</B><BR>' % (snils if snils else u'нет'), ]
    if params.get('hasWork', False):
        work = forceString(record.value('work'))
        result += [u'Занятость:<B>%s</B><BR>' % (work if work else u'не указано'), ]
    if params.get('hasSocStatus', False):
        socStatuses = forceString(record.value('socStatuses'))
        result += [u'статус: <B>%s</B><BR>' % (socStatuses if socStatuses else u'не указан'), ]
    return " ".join(result)


def hasAdditionalClientInfo(params):
    return params.get('hasRegAddress', False) \
           or params.get('hasLocAddress', False) \
           or params.get('hasPolicy', False) \
           or params.get('hasDocument', False) \
           or params.get('hasSNILS', False) \
           or params.get('hasWork', False) \
           or params.get('hasSocStatus', False)


class CPersonVisits(CReport):
    tableColumns = [
            ('10%', [u'Дата'],                    CReportBase.AlignLeft),
            ('5%',  [u'№'],                       CReportBase.AlignRight),
            ('11%', [u'ФИО'],                     CReportBase.AlignLeft),
            ('3%',  [u'Пол'],                     CReportBase.AlignLeft),
            ('11%', [u'Дата рождения'],           CReportBase.AlignLeft),
            ('11%', [u'Идентификатор'],           CReportBase.AlignLeft),
            ('14%', [u'Дополнительные сведения'], CReportBase.AlignLeft),
            ('10%', [u'Тип обращения'],           CReportBase.AlignLeft),
            ('10%', [u'Место'],                   CReportBase.AlignLeft),
            ('5%',  [u'Диагноз'],                 CReportBase.AlignLeft),
            ('5%',  [u'ДН'],                      CReportBase.AlignLeft),
            ('5%',  [u'Тип финансирования'],      CReportBase.AlignLeft),
            ]

    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setPayPeriodVisible(False)
        self.setTitle(u'Сводка на врача', u'Сводка на врача')

    def getSetupDialog(self, parent):
        result = CPersonVisitsSetupDialog(parent)
        result.setTitle(self.title())
        return result

    def build(self, params):
        isPreliminaryDiagnostics = params.get('isPreliminaryDiagnostics', False)
        query = selectData(params)

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        if hasAdditionalClientInfo(params):
            table = createTable(cursor, self.tableColumns)
        else:
            tableColumns2 = [self.tableColumns[i] for i in xrange(len(self.tableColumns))]
            tableColumns2.remove(tableColumns2[6])
            table = createTable(cursor, tableColumns2)

        prevVisitId = None
        prevDate = None
        cnt = 0
        total = 0
        while query.next():
            record = query.record()
            visitId = forceRef(record.value('visit_id'))
            date = forceDate(record.value('date'))
            lastName = forceString(record.value('lastName'))
            firstName = forceString(record.value('firstName'))
            patrName = forceString(record.value('patrName'))
            sex = formatSex(forceInt(record.value('sex')))
            birthDate = forceDate(record.value('birthDate'))
            age = calcAge(birthDate, date)
            eventType = forceString(record.value('eventType'))
            scene = forceString(record.value('scene'))
            MKB = forceString(record.value('MKB'))
            dispanser = forceString(record.value('dispanser'))
            financeName = forceString(record.value('financeName'))
            clientIdentification = forceString(record.value('identifier'))
            if isPreliminaryDiagnostics:
                if not MKB:
                    MKB = forceString(record.value('MKBPreliminary'))

            if date != prevDate:
                produceTotalLine(table, prevDate, cnt)
                prevDate = date
                total += cnt
                cnt = 0
                prevVisitId = None

            if prevVisitId != visitId:
                cnt += 1
                i = table.addRow()
                table.setText(i, 0, forceString(date))
                table.setText(i, 1, cnt)
                table.setText(i, 2, formatNameInt(lastName, firstName, patrName))
                table.setText(i, 3, sex)
                table.setText(i, 4, "%s (%s)" % (formatDate(birthDate), age))
                table.setText(i, 5, clientIdentification)
                if hasAdditionalClientInfo(params):
                    table.setHtml(i, 6, getAdditionalClientInfo(record, params))
                    shift = 1
                else:
                    shift = 0
                table.setText(i, 6+shift, eventType)
                table.setText(i, 7+shift, scene)
                table.setText(i, 8+shift, MKB)
                table.setText(i, 9+shift, dispanser)
                table.setText(i, 10+shift, financeName)
            else:
                i = table.addRow()
                for j in xrange(7):
                    if j != 5:
                        table.mergeCells(i-1, j, 2, 1)
                table.setText(i, 5, MKB)
        produceTotalLine(table, prevDate, cnt)
        total += cnt
        i = table.addRow()
        table.setText(i, 0, u'ВСЕГО', CReportBase.TableTotal)
        table.setText(i, 1, total, CReportBase.TableTotal)
        return doc


class CPersonVisitsSetupDialog(QtGui.QDialog, Ui_PersonVisitsSetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.patientRequired = False
        self.setupUi(self)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())
        self.cmbEventPurpose.setTable('rbEventTypePurpose', True, filter='code != \'0\'')
        self.cmbEventType.setTable('EventType', True, filter=getWorkEventTypeFilter(isApplyActive=True))
        self.cmbScene.setTable('rbScene', True)
        self.cmbAccountingSystem.setTable('rbAccountingSystem', filter=u"code not in ('АдрРег', 'АдрПрож')")
        self.cmbPreRecord.insertItem(0, u'не учитывать')
        self.cmbPreRecord.insertItem(1, u'да')
        self.cmbPreRecord.insertItem(2, u'нет')
        self.cmbFinance.setTable('rbFinance', addNone=True)

    def setTitle(self, title):
        self.setWindowTitle(title)

    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate().currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate().currentDate()))
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.cmbPerson.setValue(params.get('personId', None))
        self.cmbEventPurpose.setValue(params.get('eventPurposeId', None))
        self.cmbEventType.setValue(params.get('eventTypeId', None))
        self.cmbScene.setValue(params.get('sceneId', None))
        self.cmbWorkOrganisation.setValue(params.get('workOrgId', None))
        self.cmbSex.setCurrentIndex(params.get('sex', 0))
        self.edtAgeFrom.setValue(params.get('ageFrom', 0))
        self.edtAgeTo.setValue(params.get('ageTo', 150))
        accountingSystem = params.get('accountingSystem', '')
        self.cmbAccountingSystem.setCurrentIndex(self.cmbAccountingSystem.findText(accountingSystem))
        self.cmbPreRecord.setCurrentIndex(params.get('preRecord', 0))
        self.chkRegAddress.setChecked(params.get('hasRegAddress', False))
        self.chkLocAddress.setChecked(params.get('hasRegAddress', False))
        self.chkPolicy.setChecked(params.get('hasPolicy', False))
        self.chkDocument.setChecked(params.get('hasDocument', False))
        self.chkSNILS.setChecked(params.get('hasSNILS', False))
        self.chkWork.setChecked(params.get('hasWork', False))
        self.chkSocStatus.setChecked(params.get('hasSocStatus', False))
        self.cmbIsPrimary.setCurrentIndex(params.get('isPrimary', 0))
        self.cmbFinance.setValue(params.get('financeId', None))
        self.chkPreliminaryDiagnostics.setChecked(params.get('isPreliminaryDiagnostics', False))

    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['eventPurposeId'] = self.cmbEventPurpose.value()
        result['eventTypeId'] = self.cmbEventType.value()
        result['orgStructureId'] = self.cmbOrgStructure.value()
        result['personId'] = self.cmbPerson.value()
        result['sceneId'] = self.cmbScene.value()
        result['workOrgId'] = self.cmbWorkOrganisation.value()
        result['sex'] = self.cmbSex.currentIndex()
        result['ageFrom'] = self.edtAgeFrom.value()
        result['ageTo'] = self.edtAgeTo.value()
        result['accountingSystem'] = self.cmbAccountingSystem.currentText()
        result['accountingSystemId'] = self.cmbAccountingSystem.value()
        result['preRecord'] = self.cmbPreRecord.currentIndex()
        result['hasRegAddress'] = self.chkRegAddress.isChecked()
        result['hasLocAddress'] = self.chkLocAddress.isChecked()
        result['hasPolicy'] = self.chkPolicy.isChecked()
        result['hasDocument'] = self.chkDocument.isChecked()
        result['hasSNILS'] = self.chkSNILS.isChecked()
        result['hasWork'] = self.chkWork.isChecked()
        result['hasSocStatus'] = self.chkSocStatus.isChecked()
        result['isPrimary'] = self.cmbIsPrimary.currentIndex()
        result['financeId'] = self.cmbFinance.value()
        result['isPreliminaryDiagnostics'] = self.chkPreliminaryDiagnostics.isChecked()
        return result

    @pyqtSignature('QDate')
    def on_edtBegDate_dateChanged(self, date):
        self.cmbPerson.setBegDate(date)

    @pyqtSignature('QDate')
    def on_edtEndDate_dateChanged(self, date):
        self.cmbPerson.setEndDate(date)

    @pyqtSignature('int')
    def on_cmbOrgStructure_currentIndexChanged(self, index):
        orgStructureId = self.cmbOrgStructure.value()
        self.cmbPerson.setOrgStructureId(orgStructureId)

    @pyqtSignature('int')
    def on_cmbEventPurpose_currentIndexChanged(self, index):
        eventPurposeId = self.cmbEventPurpose.value()
        if eventPurposeId:
            _filter = 'EventType.purpose_id =%d' % eventPurposeId
        else:
            _filter = getWorkEventTypeFilter()
        self.cmbEventType.setFilter(_filter)

    @pyqtSignature('')
    def on_btnSelectWorkOrganisation_clicked(self):
        orgId = selectOrganisation(self, self.cmbWorkOrganisation.value(), False)
        self.cmbWorkOrganisation.updateModel()
        if orgId:
            self.cmbWorkOrganisation.setValue(orgId)
