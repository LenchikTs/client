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
from PyQt4.QtCore import QDate

from library.database          import addDateInRange
from library.Utils             import forceBool, forceDouble, forceRef, forceString

from Orgs.Utils                import getOrgStructurePersonIdList
from Reports.Report            import CReport, CReportEx
from Reports.ReportSetupDialog import CReportSetupDialog
from Reports.ReportBase        import CReportBase
from Reports.Utils             import dateRangeAsStr


def selectData(params):
    begDate = params.get('begDate', QDate.currentDate())
    endDate = params.get('endDate', QDate.currentDate())
    orgStructureId = params.get('orgStructureId', None)
    personId = params.get('personId', None)
    stmt= u"""
        SELECT
            Person.id AS personId,
            Action.assistant_id AS assistantId,
            vrbPersonWithSpeciality.code AS personCode,
            vrbPersonWithSpeciality.name AS personName,
            rbPost.id AS postId,
            rbPost.code AS postCode,
            PWSA.code AS personCodeA,
            PWSA.name AS personNameA,
            rbPostA.id AS postIdA,
            rbPostA.code AS postCodeA,
            IF(LEFT(rbPost.code, 1) IN ('1','2','3'), 1, 0) AS postDoctor,
            IF(LEFT(rbPost.code, 1) IN ('4','5','6','7','8','9'), 1, 0) AS postMediatePersonal,
            IF(rbPost.code = '3097', 1, 0) AS postGigienist,
            IF(rbPost.code = '4041', 1, 0) AS postRentgen,
            SUM(Account_Item.price * IF(Account_Item.amount, Account_Item.amount, Action.amount)) AS sumTariff
        FROM
            Event
            INNER JOIN Action ON Action.event_id = Event.id
            INNER JOIN ActionType ON ActionType.id = Action.actionType_id
            INNER JOIN Account_Item ON Account_Item.action_id = Action.id
            INNER JOIN EventType ON EventType.id = Event.eventType_id
            INNER JOIN rbMedicalAidType ON rbMedicalAidType.id = EventType.medicalAidType_id
            INNER JOIN vrbPersonWithSpeciality ON vrbPersonWithSpeciality.id = Action.person_id
            INNER JOIN Person ON Person.id = Action.person_id
            INNER JOIN rbPost ON rbPost.id = Person.post_id
            LEFT JOIN vrbPersonWithSpeciality AS PWSA ON PWSA.id = Action.assistant_id
            LEFT JOIN Person AS PersonA ON (PersonA.id = Action.assistant_id AND PersonA.deleted = 0)
            LEFT JOIN rbPost AS rbPostA ON rbPostA.id = PersonA.post_id
        WHERE
            Event.deleted = 0
            AND Person.deleted = 0
            AND rbMedicalAidType.code = '9'
            AND Action.deleted = 0
            AND ActionType.deleted = 0
            AND Account_Item.deleted = 0
            AND %s
        GROUP BY rbPost.code, Person.id, rbPostA.code, Action.assistant_id, postDoctor, postMediatePersonal, postGigienist, postRentgen
        ORDER BY rbPost.code, vrbPersonWithSpeciality.code, vrbPersonWithSpeciality.name, rbPostA.code, PWSA.code, PWSA.name
    """
    db = QtGui.qApp.db
#    tableEvent = db.table('Event')
    tableAction = db.table('Action')

    cond = []
    addDateInRange(cond, tableAction['endDate'], begDate, endDate)
    if orgStructureId:
        persons = getOrgStructurePersonIdList(orgStructureId)
        cond.append(tableAction['person_id'].inlist(persons))
    if personId:
        cond.append(tableAction['person_id'].eq(personId))

    return db.query(stmt % (db.joinAnd(cond)))


class CStomatReportCompositeList(CReportEx): #actStomatReportCompositeList
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self._mapActionTypeId2ServiceIdList = {}
        self.setTitle(u'СВОДНАЯ ВЕДОМОСТЬ', u'СВОДНАЯ ВЕДОМОСТЬ')
        self.table_columns = [
            ('50%',  [u'CПЕЦИАЛИСТЫ'], CReportBase.AlignLeft),
            ('25%', [u'СУММА ОКАЗАННЫХ УСЛУГ'], CReportBase.AlignRight),
            ('25%', [u'ФОНД ОПЛАТЫ ТРУДА'], CReportBase.AlignRight)
            ]

    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setTitle(self.title())
        result.setOrgStructureVisible(True)
        result.setPersonVisible(True)
        result.setFinanceVisible(False)
        result.setSpecialityVisible(False)
        result.setInsurerVisible(False)
        result.setStageVisible(False)
        result.setPayPeriodVisible(False)
        result.setOwnershipVisible(False)
        result.setWorkOrganisationVisible(False)
        result.setSexVisible(False)
        result.setAgeVisible(False)
        result.setActionTypeVisible(False)
        result.setMKBFilterVisible(False)
        result.setEventTypeVisible(False)
        result.lblEventType.hide()
        result.cmbEventType.hide()
        result.chkOnlyPermanentAttach.hide()
        result.chkDetailPerson.hide()
        return result


    def getPeriodName(self, params):
        begDate = params.get('begDate', QDate.currentDate())
        endDate = params.get('endDate', QDate.currentDate())
        return dateRangeAsStr(u' период', begDate, endDate)


    def getReportData(self, query):
        reportData = []
#        context = CInfoContext()
#        i = 0
#        colCount = 13
        reportDataType = {}
        while query.next():
            record = query.record()
            personId = forceRef(record.value('personId'))
            personCode = forceString(record.value('personCode'))
            personName = forceString(record.value('personName'))
#            postId = forceRef(record.value('postId'))
#            postCode = forceString(record.value('postCode'))
            sumTariff = forceDouble(record.value('sumTariff'))
            assistantId = forceRef(record.value('assistantId'))
            personCodeA = forceString(record.value('personCodeA'))
            personNameA = forceString(record.value('personNameA'))
#            postIdA = forceRef(record.value('postIdA'))
#            postCodeA = forceString(record.value('postCodeA'))
            postDoctor = forceBool(record.value('postDoctor'))
            postMediatePersonal = forceBool(record.value('postMediatePersonal'))
            postGigienist = forceBool(record.value('postGigienist'))
            postRentgen = forceBool(record.value('postRentgen'))
            postRow = 0
            if postDoctor:
                postRow = 1
            elif postMediatePersonal:
                postRow = 2
            elif postGigienist:
                postRow = 4
            elif postRentgen:
                postRow = 5
            if postRow:
                reportData = reportDataType.get(postRow, {})
                reportLine = reportData.get(personId, ['', 0, 0])
                reportLine[0] = personCode + u' ' + personName
                reportLine[1] += sumTariff
                fondTariff = 0
                if postDoctor:
                    fondTariff = (sumTariff * 22.0)/100.0
                if postMediatePersonal:
                    fondTariff = (sumTariff * 7.5)/100.0
                if postGigienist:
                    fondTariff = (sumTariff * 15.0)/100.0
                if postRentgen:
                    fondTariff = (sumTariff * 15.0)/100.0
                reportLine[2] += fondTariff
                reportData[personId] = reportLine
                reportDataType[postRow] = reportData
            if assistantId:
                postRow = 3
                reportData = reportDataType.get(postRow, {})
                reportLine = reportData.get(personId, ['', 0, 0])
                reportLine[0] = personCodeA + u' ' + personNameA
                reportLine[1] += sumTariff
                reportLine[2] = '?'
                reportData[personId] = reportLine
                reportDataType[postRow] = reportData
        return reportDataType


    def buildInt(self, params, cursor):
        query = selectData(params)
        reportDataType = self.getReportData(query)
        reportDataTotal = [u'Итого', 0, 0]
        reportLineTotal = [u'Итого', 0, 0]
        table = self.createTable(cursor)
        repTypeKeys = reportDataType.keys()
        repTypeKeys.sort()
        totalName = [u'Итого, по неопределённым:', u'Итого, по врачам:', u'Итого, по мед. сестрам:', u'Итого, по ассистентам:', u'Итого, по гигиенистам:', u'Итого, по рентгенлаборантам:']
        for repTypeKey in repTypeKeys:
            reportData = reportDataType.get(repTypeKey, {})
            for reportLine in reportData.values():
                row = table.addRow()
                for j, val in enumerate(reportLine):
                    table.setText(row, j, unicode(val))
                    if j > 0:
                        reportLineTotal[j] += val
                        reportDataTotal[j] += val
            row = table.addRow()
            table.setText(row, 0, totalName[repTypeKey])
            for i in [1, 2]:
                table.setText(row, i, unicode(reportLineTotal[i]))

        if len(reportDataType) > 0:
            row = table.addRow()
            table.setText(row, 0, u'Итого:')
            for i in [1, 2]:
                table.setText(row, i, unicode(reportDataTotal[i]))
        return reportDataType


class CStomatReportToSpecialityList(CReportEx): #actStomatReportToSpecialityList
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self._mapActionTypeId2ServiceIdList = {}
        self.setTitle(u'РАСШИФРОВКА ПОЛУЧЕННЫХ СУММ ПО СПЕЦИАЛИСТАМ', u'РАСШИФРОВКА ПОЛУЧЕННЫХ СУММ ПО СПЕЦИАЛИСТАМ')
        self.table_columns = [
            ('40%', [u'ВРАЧ'],               CReportBase.AlignLeft),
            ('20%', [u'ПРОЧИЕ ИСПОЛНИТЕЛИ'], CReportBase.AlignLeft),
            ('20%', [u'СУММА'],              CReportBase.AlignRight),
            ('20%', [u'НОМЕРА НАРЯДОВ'],     CReportBase.AlignRight)
            ]

    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setTitle(self.title())
        result.setOrgStructureVisible(True)
        result.setPersonVisible(True)
        result.setFinanceVisible(False)
        result.setSpecialityVisible(False)
        result.setInsurerVisible(False)
        result.setStageVisible(False)
        result.setPayPeriodVisible(False)
        result.setOwnershipVisible(False)
        result.setWorkOrganisationVisible(False)
        result.setSexVisible(False)
        result.setAgeVisible(False)
        result.setActionTypeVisible(False)
        result.setMKBFilterVisible(False)
        result.setEventTypeVisible(False)
        result.lblEventType.hide()
        result.cmbEventType.hide()
        result.chkOnlyPermanentAttach.hide()
        result.chkDetailPerson.hide()
        return result


    def getPeriodName(self, params):
        begDate = params.get('begDate', QDate.currentDate())
        endDate = params.get('endDate', QDate.currentDate())
        return dateRangeAsStr(u' период', begDate, endDate)


    def getReportData(self, query):
        reportData = []
#        context = CInfoContext()
#        i = 0
#        colCount = 13
        reportDataType = {}
        while query.next():
            record = query.record()
            personId = forceRef(record.value('personId'))
#            personCode = forceString(record.value('personCode'))
            personName = forceString(record.value('personName'))
#            postId = forceRef(record.value('postId'))
#            postCode = forceString(record.value('postCode'))
            sumTariff = forceDouble(record.value('sumTariff'))
            assistantId = forceRef(record.value('assistantId'))
#            personCodeA = forceString(record.value('personCodeA'))
            personNameA = forceString(record.value('personNameA'))
#            postIdA = forceRef(record.value('postIdA'))
#            postCodeA = forceString(record.value('postCodeA'))
            postDoctor = forceBool(record.value('postDoctor'))
            if postDoctor:
                reportData = reportDataType.get((personId, personName), {})
                reportLine = reportData.get(assistantId, ['', 0, '?'])
                reportLine[0] = personNameA
                reportLine[1] += sumTariff
                reportLine[2] = '?'
                reportData[assistantId] = reportLine
                reportDataType[(personId, personName)] = reportData
        return reportDataType


    def buildInt(self, params, cursor):
        query = selectData(params)
        reportDataType = self.getReportData(query)
        table = self.createTable(cursor)
        repTypeKeys = reportDataType.keys()
        repTypeKeys.sort()
        for repTypeKey in repTypeKeys:
            row = table.addRow()
            newRow = row
            table.setText(row, 0, unicode(repTypeKey[1]))
            reportData = reportDataType.get(repTypeKey, {})
            for reportLine in reportData.values():
                for j, val in enumerate(reportLine):
                    table.setText(row, j+1, unicode(val))
                if (len(reportData)-1) > (newRow - row):
                    newRow = table.addRow()
        return reportDataType

