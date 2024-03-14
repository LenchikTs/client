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
from PyQt4.QtCore import QDate, QDateTime

from library.Utils      import forceInt, forceRef, forceString, formatDays
from Orgs.Utils         import getOrgStructureDescendants, getOrgStructureFullName
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable

from Ui_ReportBreachSASetup import Ui_ReportBreachSASetupDialog


def selectData(params):
    begDate        = params.get('begDate', QDate())
    endDate        = params.get('endDate', QDate())
    orgStructureId = params.get('orgStructureId', None)
    breachDays     = params.get('breachDays', 1)
    db = QtGui.qApp.db
#    tableScheduleItem  = db.table('Schedule_Item')
    tablePerson        = db.table('vrbPersonWithSpeciality')
    tableSA            = db.table('SuspendedAppointment')
    cond = []
    orgStructureIdList = []
    if begDate:
        cond.append(tableSA['endDate'].dateGe(begDate))
    if endDate:
        cond.append(tableSA['begDate'].dateLt(endDate.addDays(1)))
    if orgStructureId:
        orgStructureIdList = getOrgStructureDescendants(orgStructureId)
        cond.append(tablePerson['orgStructure_id'].inlist(orgStructureIdList))
    if breachDays:
        cond.append('''DATE_ADD(SuspendedAppointment.endDate, INTERVAL %s Day) <= DATE(Schedule_Item.time)'''%(breachDays))
    stmtSA = ''' SELECT SA.id
        FROM SuspendedAppointment AS SA
        INNER JOIN Schedule_Item AS SI ON SI.client_id = SA.client_id
        INNER JOIN Schedule AS S ON S.id = SI.master_id
        INNER JOIN Person ON Person.id = S.person_id
        WHERE SA.client_id = Client.id
        AND DATE(SI.time) >= DATE(SA.begDate)
        AND DATE(SI.time) <= DATE(SA.endDate)
        AND SA.deleted = 0 AND S.deleted = 0 AND SI.deleted = 0 AND Person.deleted = 0 %s
        AND (SA.orgStructure_id = Person.orgStructure_id OR SA.orgStructure_id IS NULL)
        AND (SA.speciality_id = Person.speciality_id OR SA.speciality_id IS NULL)
        AND (SA.person_id = S.person_id OR SA.person_id IS NULL)'''%((u'AND Person.orgStructure_id IN (%s)'%(','.join(str(orgStructureId) for orgStructureId in orgStructureIdList if orgStructureId))) if orgStructureIdList else '')
    cond.append(''' Schedule_Item.time = (SELECT MIN(SI.time)
    FROM Schedule_Item AS SI
    INNER JOIN Schedule AS S ON S.id = SI.master_id
    INNER JOIN Person ON Person.id = S.person_id
    WHERE SI.client_id = SuspendedAppointment.client_id
    AND DATE_ADD(SuspendedAppointment.endDate, INTERVAL %s Day) <= DATE(SI.time)
    AND S.deleted = 0 AND SI.deleted = 0 AND Person.deleted = 0 %s
    AND (Person.orgStructure_id = SuspendedAppointment.orgStructure_id OR SuspendedAppointment.orgStructure_id IS NULL)
    AND (Person.speciality_id = SuspendedAppointment.speciality_id OR SuspendedAppointment.speciality_id IS NULL)
    AND (S.person_id = SuspendedAppointment.person_id OR SuspendedAppointment.person_id IS NULL))'''%(breachDays, (u'AND Person.orgStructure_id IN (%s)'%(','.join(str(orgStructureId) for orgStructureId in orgStructureIdList if orgStructureId))) if orgStructureIdList else ''))
    stmt="""
    SELECT
    COUNT(Schedule_Item.id) AS countSI,
    vrbPersonWithSpeciality.id AS personId,
    vrbPersonWithSpeciality.name AS personName
    FROM Client
    INNER JOIN SuspendedAppointment ON SuspendedAppointment.client_id = Client.id
    INNER JOIN Schedule_Item ON Schedule_Item.client_id = SuspendedAppointment.client_id
    INNER JOIN Schedule ON Schedule.id = Schedule_Item.master_id
    INNER JOIN vrbPersonWithSpeciality ON vrbPersonWithSpeciality.id = Schedule.person_id
    WHERE
    SuspendedAppointment.id NOT IN (%s)
    AND Client.deleted = 0 AND SuspendedAppointment.deleted = 0
    AND Schedule.deleted = 0 AND Schedule_Item.deleted = 0
    AND (SuspendedAppointment.orgStructure_id = vrbPersonWithSpeciality.orgStructure_id OR SuspendedAppointment.orgStructure_id IS NULL)
    AND (SuspendedAppointment.speciality_id = vrbPersonWithSpeciality.speciality_id OR SuspendedAppointment.speciality_id IS NULL)
    AND (SuspendedAppointment.person_id = Schedule.person_id OR SuspendedAppointment.person_id IS NULL)
    %s
    GROUP BY personId
    ORDER BY personName
    """ % (stmtSA, (u' AND %s'%db.joinAnd(cond)) if cond else '')
    records = db.query(stmt)
    reportData = {}
    while records.next():
        record = records.record()
        countSI = forceInt(record.value('countSI'))
        personId = forceRef(record.value('personId'))
        personName = forceString(record.value('personName'))
        reportCount = reportData.get((personName, personId), 0)
        reportData[(personName, personId)] = reportCount + countSI
    return reportData


class CReportBreachSASetupDialog(QtGui.QDialog, Ui_ReportBreachSASetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.edtBreachDays.setValue(params.get('breachDays', 1))


    def params(self):
        result = {}
        result['begDate']        = self.edtBegDate.date()
        result['endDate']        = self.edtEndDate.date()
        result['orgStructureId'] = self.cmbOrgStructure.value()
        result['breachDays']     = self.edtBreachDays.value()
        return result


class CReportBreachSA(CReport):
    def __init__(self, parent = None):
        CReport.__init__(self, parent)
        self.setTitle(u'Отчёт по записи с нарушением сроков ожидания по заявкам из Журнала отложенной записи.')


    def getSetupDialog(self, parent):
        result = CReportBreachSASetupDialog(parent)
        return result


    def getDescription(self, params):
        def dateRangeAsStr(begDate, endDate):
            result = ''
            if begDate:
                result += u' с '+forceString(begDate)
            if endDate:
                result += u' по '+forceString(endDate)
            return result
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        orgStructureId = params.get('orgStructureId', None)
        rows = []
        if begDate or endDate:
            rows.append(u'за период' + dateRangeAsStr(begDate, endDate))
        if orgStructureId:
            rows.append(u'подразделение: ' + getOrgStructureFullName(orgStructureId))
        rows.append(u'нарушение сроков ожидания на %s и более'%(formatDays(params.get('breachDays', 1))))
        rows.append(u'отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        return rows


    def build(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        doc = QtGui.QTextDocument()
        if (not begDate) or (not endDate):
            currentDate = QDate.currentDate()
            begDate = QDate(currentDate.year(), 1, 1)
            endDate = currentDate
            params['begDate'] = begDate
            params['endDate'] = endDate
        if begDate and endDate:
            doc = QtGui.QTextDocument()
            cursor = QtGui.QTextCursor(doc)
            cursor.setCharFormat(CReportBase.ReportTitle)
            cursor.setBlockFormat(CReportBase.AlignCenter)
            cursor.insertText(u'Отчёт по записи с нарушением сроков ожидания по заявкам из Журнала отложенной записи.')
            cursor.insertBlock()
            self.dumpParams(cursor, params)
            cursor.insertBlock()
            cursor.setCharFormat(CReportBase.ReportBody)
            cols = [('10%',[u'№ строки'],           CReportBase.AlignLeft),
                    ('50%',[u'Врач'],               CReportBase.AlignLeft),
                    ('40%',[u'Количество записей'], CReportBase.AlignLeft)
                   ]
            table = createTable(cursor, cols)
            reportData = selectData(params)
            keysData = reportData.keys()
            keysData.sort()
            cnt = 1
            for keyData in keysData:
                reportCount = reportData.get(keyData)
                i = table.addRow()
                table.setText(i, 0, cnt)
                table.setText(i, 1, keyData[0])
                table.setText(i, 2, reportCount)
                cnt += 1
        return doc

