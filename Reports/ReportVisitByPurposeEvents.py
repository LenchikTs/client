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
from PyQt4.QtCore import pyqtSignature, QDate, QDateTime

from library.Utils      import firstMonthDay, forceInt, forceRef, forceString, lastMonthDay

from Orgs.Utils         import getOrgStructureDescendants
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable

from Reports.Ui_VisitByPurposeEventsDialog import Ui_VisitByPurposeEventsSetupDialog


def selectData(params):
    db = QtGui.qApp.db
    tableAccount = db.table('Account')
    tableContract = db.table('Contract')
    tableAccountItem = db.table('Account_Item')
    tablePerson = db.table('Person')
    tableEvent = db.table('Event')
    tableClient = db.table('Client')

    cond = []
    begDate = params.get('begDate', None)
    endDate = params.get('endDate', None)
    if begDate:
        cond.append(tableEvent['execDate'].ge(begDate))
    if endDate:
        cond.append(tableEvent['execDate'].lt(endDate.addDays(1)))
    if params.get('personId', None):
        cond.append(tablePerson['id'].eq(params['personId']))
        cond.append(tablePerson['deleted'].eq(0))
    else:
        if params.get('orgStructureId', None):
            cond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureDescendants(params['orgStructureId'])))
        else:
            cond.append(db.joinOr([tablePerson['org_id'].eq(QtGui.qApp.currentOrgId()),
                                   tablePerson['org_id'].isNull()]))
        if params.get('specialityId', None):
            cond.append(tablePerson['speciality_id'].eq(params['specialityId']))
    queryTable = u''
    if params.get('confirmation', None):
        queryTable = u'''INNER JOIN Contract        ON Contract.id = Event.contract_id
                         INNER JOIN Account         ON Account.contract_id = Contract.id
                         INNER JOIN Account_Item    ON Account_Item.master_id = Account.id'''
        cond.append(tableEvent['id'].eq(tableAccountItem['event_id']))
        cond.append(tableAccountItem['deleted'].eq(0))
        cond.append(tableAccount['deleted'].eq(0))
        cond.append(tableContract['deleted'].eq(0))
        if params.get('confirmationType', 0) == 1:
            cond.append(tableAccountItem['date'].isNotNull())
            cond.append(tableAccountItem['number'].ne(''))
            cond.append(tableAccountItem['refuseType_id'].isNull())
        elif params.get('confirmationType', 0) == 2:
            cond.append(tableAccountItem['date'].isNotNull())
            cond.append(tableAccountItem['number'].ne(''))
            cond.append(tableAccountItem['refuseType_id'].isNotNull())
        else:
            cond.append(tableAccountItem['number'].eq(''))
        condAIDate = []
        if params.get('confirmationBegDate', None):
            condAIDate.append(tableAccountItem['date'].ge(params['confirmationBegDate']))
        if params.get('confirmationEndDate', None):
            condAIDate.append(tableAccountItem['date'].lt(params['confirmationEndDate'].addDays(1)))
        if params.get('confirmationType', 0) in [1, 2]:
            if condAIDate:
                cond.append(db.joinAnd(condAIDate))
        else:
            if condAIDate:
                cond.append(db.joinOr([tableAccountItem['date'].isNull(), db.joinAnd(condAIDate)]))
        if params.get('refuseType', None):
            cond.append(tableAccountItem['refuseType_id'].eq(params['refuseType']))
    filterBegAge = params.get('filterBegAge', 0)
    filterEndAge = params.get('filterEndAge', 150)
    if (((filterBegAge!=0) or (filterEndAge!=150)) and filterBegAge <=filterEndAge):
        cond.append(tableClient['id'].eq(tableEvent['client_id']))
        cond.append('''age(Client.birthDate, IF(Event.execDate IS NOT NULL, DATE(Event.execDate), DATE(%s))) >= %d
                           AND age(Client.birthDate, IF(Event.execDate IS NOT NULL, DATE(Event.execDate), DATE(%s))) < %d''' % (db.formatDate(QDate.currentDate()), filterBegAge, db.formatDate(QDate.currentDate()), filterEndAge+1))
    stmt="""
SELECT
    COUNT(DISTINCT Event.id) AS countEvent,
    rbEventTypePurpose.id AS eventTypePurposeId,
    rbEventTypePurpose.code AS eventTypePurposeCode,
    rbEventTypePurpose.name AS eventTypePurposeName,
    SUM((SELECT COUNT(DISTINCT Visit.id) FROM Visit WHERE Visit.event_id = Event.id AND Visit.deleted = 0)) AS countVisit

FROM Event
LEFT JOIN EventType       ON EventType.id = Event.eventType_id
LEFT JOIN Person          ON Person.id = Event.execPerson_id
LEFT JOIN rbSpeciality    ON rbSpeciality.id = Person.speciality_id
LEFT JOIN Client          ON Client.id = Event.client_id
LEFT JOIN rbEventTypePurpose ON rbEventTypePurpose.id = EventType.purpose_id
%s
WHERE
    Event.deleted = 0
    AND EventType.deleted = 0
    AND Client.deleted = 0
    AND %s
GROUP BY eventTypePurposeId
    """
    db = QtGui.qApp.db
    return db.query(stmt % (queryTable, db.joinAnd(cond)))


class CReportVisitByPurposeEvents(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Посещения по назначениям событий')


    def build(self, params):
        reportData = {}
        reportRowSize = 2
        query = selectData(params)
        while query.next():
            record = query.record()
            countEvent = forceInt(record.value('countEvent'))
            countVisit = forceInt(record.value('countVisit'))
            eventTypePurposeId = forceRef(record.value('eventTypePurposeId'))
            eventTypePurposeName = forceString(record.value('eventTypePurposeName'))
            reportLine = reportData.get((eventTypePurposeName, eventTypePurposeId), [0]*reportRowSize)
            reportLine[0] += countEvent
            reportLine[1] += countVisit
            reportData[(eventTypePurposeName, eventTypePurposeId)] = reportLine

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertText('\n'.join(self.getDescription(params)))
        cursor.insertBlock()

        tableColumns = [
                          ('40%',  [ u'Типы назначений'], CReportBase.AlignLeft),
                          ('30%',  [ u'Количество событий'], CReportBase.AlignRight),
                          ('30%',  [ u'Количество посещений'], CReportBase.AlignRight)
                       ]
        table = createTable(cursor, tableColumns)
        keysLine = reportData.keys()
        keysLine.sort(key=lambda item: item[0])
        totalLine = [0]*reportRowSize
        for key in keysLine:
            reportLine = reportData[key]
            i = table.addRow()
            table.setText(i, 0, key[0])
            table.setText(i, 1, reportLine[0])
            table.setText(i, 2, reportLine[1])
            totalLine[0] += reportLine[0]
            totalLine[1] += reportLine[1]
        i = table.addRow()
        table.setText(i, 0, u'ИТОГО')
        table.setText(i, 1, totalLine[0])
        table.setText(i, 2, totalLine[1])
        return doc


    def getSetupDialog(self, parent):
        result = CVisitByPurposeEventsSetupDialog(parent)
        result.setTitle(self.title())
        return result


    def getDescription(self, params):
        db = QtGui.qApp.db
        begDate              = params.get('begDate', None)
        endDate              = params.get('endDate', None)
        orgStructureId       = params.get('orgStructureId', None)
        personId             = params.get('personId', None)
        specialityId         = params.get('specialityId', None)
        confirmation         = params.get('confirmation', False)
        confirmationBegDate  = params.get('confirmationBegDate', None)
        confirmationEndDate  = params.get('confirmationEndDate', None)
        confirmationType     = params.get('confirmationType', 0)
        refuseType           = params.get('refuseType', None)
        filterBegAge         = params.get('filterBegAge', 0)
        filterEndAge         = params.get('filterEndAge', 150)
        rows = []

        if begDate:
            rows.append(u'Дата начала периода: %s'%forceString(begDate))
        if endDate:
            rows.append(u'Дата окончания периода: %s'%forceString(endDate))
        if orgStructureId:
            rows.append(u'Подразделение исполнителя: %s'%forceString(db.translate('OrgStructure', 'id', orgStructureId, 'CONCAT_WS(\' | \', code,name)')))
        if personId:
            rows.append(u'Врач: %s'%forceString(db.translate('vrbPerson', 'id', personId, 'name')))
        if specialityId:
            rows.append(u'Специальность: %s'%forceString(db.translate('rbSpeciality', 'id', specialityId, 'CONCAT_WS(\' | \', code,name)')))
        if confirmation:
            rows.append(u'Тип подтверждения: %s'%{0: u'без подтверждения',
                                                  1: u'оплаченные',
                                                  2: u'отказанные'}.get(confirmationType, u''))
            if confirmationBegDate:
                rows.append(u'Начало периода подтверждения: %s'%forceString(confirmationBegDate))
            if confirmationEndDate:
                rows.append(u'Окончание периода подтверждения: %s'%forceString(confirmationEndDate))
            if refuseType:
                rows.append(u'Причина отказа: %s'%forceString(db.translate('rbPayRefuseType', 'id', refuseType, 'CONCAT_WS(\' | \', code,name)')))
        if filterEndAge != 150:
            rows.append(u'Возраст с %s по %s'%(forceString(filterBegAge), forceString(filterEndAge)))
        rows.append(u'Отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        return rows


class CVisitByPurposeEventsSetupDialog(QtGui.QDialog, Ui_VisitByPurposeEventsSetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.cmbSpeciality.setTable('rbSpeciality', True)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())
        self.cmbRefuseType.setTable('rbPayRefuseType', True)
        self.cmbConfirmationType.addItem(u'без подтверждения')
        self.cmbConfirmationType.addItem(u'оплаченные')
        self.cmbConfirmationType.addItem(u'отказанные')


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        date = QDate.currentDate().addDays(-3)
        self.edtBegDate.setDate(params.get('begDate', firstMonthDay(date)))
        self.edtEndDate.setDate(params.get('endDate', lastMonthDay(date)))
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.cmbSpeciality.setValue(params.get('specialityId', None))
        self.cmbPerson.setValue(params.get('personId', None))
        self.chkConfirmation.setChecked(params.get('confirmation', False))
        self.edtConfirmationBegDate.setDate(params.get('confirmationBegDate', firstMonthDay(date)))
        self.edtConfirmationEndDate.setDate(params.get('confirmationEndDate', lastMonthDay(date)))
        self.cmbConfirmationType.setCurrentIndex(params.get('confirmationType', 0))
        self.cmbRefuseType.setValue(params.get('refuseType', None))
        self.edtFilterBegAge.setValue(params.get('filterBegAge', 0))
        self.edtFilterEndAge.setValue(params.get('filterEndAge', 150))


    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['orgStructureId'] = self.cmbOrgStructure.value()
        result['specialityId'] = self.cmbSpeciality.value()
        result['personId'] = self.cmbPerson.value()
        result['confirmation'] = self.chkConfirmation.isChecked()
        result['confirmationType'] = self.cmbConfirmationType.currentIndex()
        result['confirmationBegDate'] = self.edtConfirmationBegDate.date()
        result['confirmationEndDate'] = self.edtConfirmationEndDate.date()
        result['refuseType'] = self.cmbRefuseType.value()
        result['filterBegAge'] = self.edtFilterBegAge.value()
        result['filterEndAge'] = self.edtFilterEndAge.value()
        return result


    def onStateChanged(self, state):
        self.lblConfirmationType.setEnabled(state)
        self.lblBegDateConfirmation.setEnabled(state)
        self.lblEndDateConfirmation.setEnabled(state)
        self.lblRefuseType.setEnabled(state)
        self.cmbConfirmationType.setEnabled(state)
        self.edtConfirmationBegDate.setEnabled(state)
        self.edtConfirmationEndDate.setEnabled(state)
        self.cmbRefuseType.setEnabled(state)


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
    def on_cmbSpeciality_currentIndexChanged(self, index):
        specialityId = self.cmbSpeciality.value()
        self.cmbPerson.setSpecialityId(specialityId)

