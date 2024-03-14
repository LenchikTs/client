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

from library.DialogBase import CDialogBase
from library.Utils      import firstMonthDay, forceBool, forceInt, forceRef, forceString, lastMonthDay
from Orgs.Utils         import getOrgStructureDescendants, getOrgStructureFullName, getPersonInfo, getPersonShortName, getSpecialityName
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.Utils      import dateRangeAsStr
from Timeline.Schedule  import CSchedule

from Reports.Ui_PreRecordSpecialityDialog import Ui_PreRecordSpecialityDialog


def sumLists(*lists):
    from itertools import izip
    return map(sum, izip(*lists))


def selectData(params):
    useRecordPeriod   = params.get('useRecordPeriod', True)
    begRecordDate     = params.get('begRecordDate', None)
    endRecordDate     = params.get('endRecordDate', None)
    useSchedulePeriod = params.get('useSchedulePeriod', False)
    begScheduleDate   = params.get('begScheduleDate', None)
    endScheduleDate   = params.get('endScheduleDate', None)
    orgStructureId    = params.get('orgStructureId', None)
    specialityId      = params.get('specialityId', None)
    personId          = params.get('personId', None)
    showDeleted          = params.get('showDeleted', None)

    db = QtGui.qApp.db
    tablePerson = db.table('Person')
    tableSchedule = db.table('Schedule')
    tableScheduleItem = db.table('Schedule_Item')

    cond = [ tableScheduleItem['client_id'].isNotNull(), 
           ]

    if not showDeleted:
        cond.append(tableSchedule['deleted'].eq(0))
        cond.append(tableScheduleItem['deleted'].eq(0))
    if useRecordPeriod:
        if begRecordDate:
            cond.append(tableScheduleItem['recordDatetime'].ge(begRecordDate))
        if endRecordDate:
            cond.append(tableScheduleItem['recordDatetime'].lt(endRecordDate.addDays(1)))
    if useSchedulePeriod:
        if begScheduleDate:
            cond.append(tableSchedule['date'].ge(begScheduleDate))
        if endScheduleDate:
            cond.append(tableSchedule['date'].le(endScheduleDate))
    if personId:
        cond.append(tableSchedule['person_id'].eq(personId))
    if specialityId:
        cond.append(tablePerson['speciality_id'].eq(specialityId))
    if orgStructureId:
        cond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureDescendants(orgStructureId)))
    else:
        if not personId:
            cond.append(tablePerson['org_id'].eq(QtGui.qApp.currentOrgId()))

    stmt =  'SELECT'                                                                        \
            ' COUNT(1) AS cnt,'                                                             \
            ' Schedule.person_id,'                                                          \
            ' Person.speciality_id,'                                                        \
            ' Person.orgStructure_id,'                                                      \
            ' Schedule.appointmentType,'                                                    \
            ' (Schedule_Item.client_id IS NOT NULL) AS isBusy,'                             \
            ' (RecordPerson.speciality_id IS NULL) AS isPrimary,'                           \
            ' ((Schedule_Item.client_id IS NOT NULL)'                                       \
            '  AND EXISTS(SELECT 1 FROM vVisitExt'                                          \
                                  ' WHERE vVisitExt.client_id = Schedule_Item.client_id'    \
                                    ' AND Person.speciality_id=vVisitExt.speciality_id'     \
                                    ' AND DATE(vVisitExt.date) = Schedule.date'             \
                   ')) AS isVisited '                                                       \
            'FROM'                                                                          \
            ' Schedule_Item'                                                                \
            ' LEFT JOIN Schedule               ON Schedule.id = Schedule_Item.master_id'    \
            ' LEFT JOIN Person                 ON Person.id = Schedule.person_id'           \
            ' LEFT JOIN Person AS RecordPerson ON RecordPerson.id = Schedule_Item.recordPerson_id'\
            ' WHERE %s'                                                                     \
            ' GROUP BY person_id, appointmentType, isBusy, isPrimary, isVisited'
    return db.query(stmt % db.joinAnd(cond))


class CPreRecordSpeciality(CReport):

    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Предварительная запись по специальности')
        self.rowSize = 10


    def dumpParams(self, cursor, params):
        description = []
        useRecordPeriod      = params.get('useRecordPeriod', True)
        begRecordDate        = params.get('begRecordDate', None)
        endRecordDate        = params.get('endRecordDate', None)
        useSchedulePeriod    = params.get('useSchedulePeriod', False)
        begScheduleDate      = params.get('begScheduleDate', None)
        endScheduleDate      = params.get('endScheduleDate', None)
        orgStructureId       = params.get('orgStructureId', None)
        specialityId         = params.get('specialityId', None)
        personId             = params.get('personId', None)
        detailOnOrgStructure = params.get('detailOnOrgStructure', False)
        detailOnPerson       = params.get('detailOnPerson', False)
        showDeleted = params.get('showDeleted', None)

        if useRecordPeriod:
            if begRecordDate or endRecordDate:
                description.append(dateRangeAsStr(u'период постановки в очередь', begRecordDate, endRecordDate))
        if useSchedulePeriod:
            if begScheduleDate or endScheduleDate:
                description.append(dateRangeAsStr(u'период планируемого приёма', begScheduleDate, endScheduleDate))
        if orgStructureId:
            description.append(u'подразделение: ' + getOrgStructureFullName(orgStructureId))
        else:
            description.append(u'подразделение: ЛПУ')
        if specialityId:
            description.append(u'специальность: ' + getSpecialityName(specialityId))
        if personId:
            personInfo = getPersonInfo(personId)
            description.append(u'врач: ' + personInfo['shortName']+', '+personInfo['specialityName'])
        if detailOnOrgStructure:
            description.append(u'с детализацией по подразделениям')
        if detailOnPerson:
            description.append(u'с детализацией по врачам')
        if showDeleted:
            description.append(u'учитывать удаленные записи')
        description.append(u'отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


    def build(self, description, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        detailOnOrgStructure = params.get('detailOnOrgStructure', False)
        detailOnPerson = params.get('detailOnPerson', False)
        self.makeTable(cursor, doc, self.analyzeData(selectData(params), detailOnOrgStructure, detailOnPerson))
        return doc


    def analyzeData(self, query, detailOnOrgStructure, detailOnPerson):
        mapATtoCol = { CSchedule.atAmbulance:0, CSchedule.atHome:5 }
        reportData = {}
        orgStructureDict = {}
        specialityDict = {}
        personDict = {}

        while query.next():
            record = query.record()
            cnt             = forceInt(record.value('cnt'))
            orgStructureId  = forceRef(record.value('orgStructure_id')) if detailOnOrgStructure else None
            specialityId    = forceRef(record.value('speciality_id'))
            personId        = forceRef(record.value('person_id')) if detailOnPerson else None
            appointmentType = forceInt(record.value('appointmentType'))
            isBusy          = forceBool(record.value('isBusy'))
            isPrimary       = forceBool(record.value('isPrimary'))
            isVisited       = forceBool(record.value('isVisited'))

            column = mapATtoCol.get(appointmentType, -1)
            if column>=0:
                orgStructureData = reportData.setdefault(orgStructureId, {})
                specialityData   = orgStructureData.setdefault(specialityId, {})
                rowData          = specialityData.get(personId)
                if not rowData:
                    specialityData[personId] = rowData = [0]*self.rowSize
                rowData[column] += cnt # всего
                if isBusy:
                    if isPrimary:
                        rowData[column+1] += cnt # первичные
                    else:
                        rowData[column+2] += cnt # повторные, консультации и пр.
                else:
                    rowData[column+3] += cnt # не использованы
                if isVisited:
                    rowData[column+4] += cnt # выполнено

                if detailOnOrgStructure:
                    if orgStructureId not in orgStructureDict:
                        orgStructureDict[orgStructureId] = getOrgStructureFullName(orgStructureId)
                if specialityId not in specialityDict:
                    specialityDict[specialityId] = getSpecialityName(specialityId)
                if detailOnPerson:
                    if personId not in personDict:
                        personDict[personId] = getPersonShortName(personId)

        return detailOnOrgStructure, detailOnPerson, reportData, orgStructureDict, specialityDict, personDict


    def makeTable(self, cursor, doc, (detailOnOrgStructure, detailOnPerson, reportData, orgStructureDict, specialityDict, personDict)):
        tableColumns = [('3%', [u'№',            '',                ''], CReportBase.AlignRight),
                        ('25%',[u'Врачи',        '',                ''], CReportBase.AlignLeft),
                        ('7%', [u'Амбулаторно', u'Всего номерков',  ''], CReportBase.AlignRight),
                        ('7%', [ '',            u'В том числе',    u'Первичный приём'], CReportBase.AlignRight),
                        ('7%', [ '',             '',               u'Вторичный прием'], CReportBase.AlignRight),
                        ('7%', [ '',             '',               u'Не использовано'], CReportBase.AlignRight),
                        ('7%', [ '',            u'Выполнено',      u''], CReportBase.AlignRight),
                        ('7%', [u'На дому',     u'Всего номерков', u''], CReportBase.AlignRight),
                        ('7%', [ '',            u'В том числе',    u'Первичный приём'], CReportBase.AlignRight),
                        ('7%', [ '',             '',               u'Вторичный прием'], CReportBase.AlignRight),
                        ('7%', [ '',             '',               u'Не использовано'], CReportBase.AlignRight),
                        ('7%', [ '',            u'Выполнено',       ''], CReportBase.AlignRight)
                       ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 3, 1) # №
        table.mergeCells(0, 1, 3, 1) # Врачи
        table.mergeCells(0, 2, 1, 5) # Амбулаторно
        table.mergeCells(1, 2, 2, 1) # Всего
        table.mergeCells(1, 3, 1, 3) # В т.ч.
        table.mergeCells(1, 6, 2, 1) # Выполнено

        table.mergeCells(0, 7, 1, 5) # На дому
        table.mergeCells(1, 7, 2, 1) # Всего
        table.mergeCells(1, 8, 1, 3) # В т.ч.
        table.mergeCells(1,11, 2, 1) # Выполнено

        n = 0
        total = [0]*self.rowSize
        if detailOnOrgStructure:
            orgStructureList = zip(orgStructureDict.itervalues(),orgStructureDict.iterkeys())
            orgStructureList.sort()
            for name, id in orgStructureList:
                n, total = self.writeOrgStructureSubTable(table, name, detailOnPerson, reportData[id], specialityDict, personDict, n, total)
        else:
            if None in reportData:
                n, total = self.writeSpecialitiesRows(table, detailOnPerson, reportData[None], specialityDict, personDict, n, total)
        i = table.addRow()
        table.setText(i, 1, u'Всего', charFormat=CReportBase.TableTotal)
        for column in xrange(self.rowSize):
            table.setText(i, column+2, total[column], charFormat=CReportBase.TableTotal)


    def writeOrgStructureSubTable(self, table, name, detailOnPerson, orgStructureData, specialityDict, personDict, n, total):
        i = table.addRow()
        table.setText(i, 1, name, charFormat=CReportBase.TableTotal)
        subTotal = [0]*self.rowSize
        n, subTotal = self.writeSpecialitiesRows(table, detailOnPerson, orgStructureData, specialityDict, personDict, n, subTotal)
        for column in xrange(self.rowSize):
            table.setText(i, column+2, subTotal[column], charFormat=CReportBase.TableTotal)
        return n, sumLists(total, subTotal)


    def writeSpecialitiesRows(self, table, detailOnPerson, data, specialityDict, personDict, n, total):
        specialityList = [ (specialityDict[specialityId], specialityId)
                           for specialityId in data.iterkeys()
                         ]
        specialityList.sort()

        if detailOnPerson:
            for name, id in specialityList:
                i = table.addRow()
                table.setText(i, 1, name, charFormat=CReportBase.TableTotal)
                subTotal = [0]*self.rowSize
                n, subTotal = self.writePersonsRows(table, data[id], personDict, n, subTotal)
                for column in xrange(self.rowSize):
                    table.setText(i, column+2, subTotal[column], charFormat=CReportBase.TableTotal)
                total = sumLists(total, subTotal)
        else:
            for name, id in specialityList:
                i = table.addRow()
                n += 1
                table.setText(i, 0, n)
                table.setText(i, 1, name)
                row = data[id][None]
                for column in xrange(self.rowSize):
                    table.setText(i, column+2, row[column])
                total = sumLists(total, row)
        return n, total


    def writePersonsRows(self, table, data, personDict, n, total):
        personList = [ (personDict[personId], personId)
                       for personId in data.iterkeys()
                     ]
        personList.sort()
        for name, id in personList:
            i = table.addRow()
            n += 1
            table.setText(i, 0, n)
            table.setText(i, 1, name)
            row = data[id]
            for column in xrange(self.rowSize):
                table.setText(i, column+2, row[column])
            total = sumLists(total, row)
        return n, total


class CPreRecordSpecialityEx(CPreRecordSpeciality):
    def exec_(self):
        CPreRecordSpeciality.exec_(self)

    def getSetupDialog(self, parent):
        result = CPreRecordSpecialityDialog(parent)
        result.setTitle(self.title())
        return result

    def build(self, params):
        return CPreRecordSpeciality.build(self, '\n'.join(self.getDescription(params)), params)


class CPreRecordSpecialityDialog(CDialogBase, Ui_PreRecordSpecialityDialog):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.cmbSpeciality.setTable('rbSpeciality', True)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        date = QDate.currentDate().addDays(-3)
        self.chkRecordPeriod.setChecked(params.get('useRecordPeriod', False))
        self.edtBegRecordDate.setDate(params.get('begRecordDate', firstMonthDay(date)))
        self.edtEndRecordDate.setDate(params.get('endRecordDate', lastMonthDay(date)))
        self.chkSchedulePeriod.setChecked(params.get('useSchedulePeriod', True))
        self.edtBegScheduleDate.setDate(params.get('begScheduleDate', firstMonthDay(date)))
        self.edtEndScheduleDate.setDate(params.get('endScheduleDate', lastMonthDay(date)))
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.cmbSpeciality.setValue(params.get('specialityId', None))
        self.cmbPerson.setValue(params.get('personId', None))
        self.chkDetailOnOrgStructure.setChecked(params.get('detailOnOrgStructure', False))
        self.chkDetailOnPerson.setChecked(params.get('detailOnPerson', False))
        self.chkShowDeleted.setChecked(params.get('showDeleted', False))


    def params(self):
        return dict(useRecordPeriod      = self.chkRecordPeriod.isChecked(),
                    begRecordDate        = self.edtBegRecordDate.date(),
                    endRecordDate        = self.edtEndRecordDate.date(),
                    useSchedulePeriod    = self.chkSchedulePeriod.isChecked(),
                    begScheduleDate      = self.edtBegScheduleDate.date(),
                    endScheduleDate      = self.edtEndScheduleDate.date(),
                    orgStructureId       = self.cmbOrgStructure.value(),
                    specialityId         = self.cmbSpeciality.value(),
                    personId             = self.cmbPerson.value(),
                    detailOnOrgStructure = self.chkDetailOnOrgStructure.isChecked(),
                    detailOnPerson       = self.chkDetailOnPerson.isChecked(), 
                    showDeleted  = self.chkShowDeleted.isChecked()
                   )


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
