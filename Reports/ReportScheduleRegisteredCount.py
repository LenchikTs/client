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

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature, QDate, Qt

from library.DialogBase import CDialogBase
from library.Utils      import forceDate, forceInt, formatDate, forceString, formatName
from library.TableModel import CTableModel, CTextCol
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Orgs.Utils         import getOrgStructureDescendants

from Reports.Ui_ReportScheduleRegisteredCountSetup import Ui_ReportScheduleRegisteredCountSetup


def formatAppointmentPurposeNames(idList):
    if not idList:
        return ''
    db = QtGui.qApp.db
    tableAP = db.table('rbAppointmentPurpose')
    records = db.getRecordList(tableAP, 'name', [tableAP['id'].inlist(idList)])
    nameList = []
    for record in records:
        nameList.append(forceString(record.value('name')))
    return u', '.join(name for name in nameList if name)


def selectData(params):
    db = QtGui.qApp.db

    tablePerson    = db.table('Person')
    tableSchedule  = db.table('Schedule')

    begDate        = params.get('begDate')
    endDate        = params.get('endDate')
    orgStructureId = params.get('orgStructureId')
    specialityId   = params.get('specialityId')
    personId       = params.get('personId')
    detailPerson   = params.get('detailPerson', False)
    appointmentType = params.get('appointmentType')
    appointmentPurposeIdList = params.get('appointmentPurposeIdList')

    stmt = '''SELECT
                Schedule.date,
                Schedule.capacity,
                Person.firstName,
                Person.lastName,
                Person.patrName,
                rbSpeciality.name AS specialityName,
                rbAppointmentPurpose.name AS purposeName,
                ( SELECT COUNT(id)
                  FROM Schedule_Item
                  WHERE master_id = Schedule.id
                    AND client_id IS NOT NULL
                    AND deleted = 0
                ) AS countBusy
              FROM Schedule
                JOIN Person ON Schedule.person_id = Person.id
                JOIN rbAppointmentPurpose ON Schedule.appointmentPurpose_id = rbAppointmentPurpose.id
                LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
              WHERE %s '''

    cond = [ tableSchedule['deleted'].eq(0),
             tablePerson['deleted'].eq(0),
           ]
    if begDate:
        cond.append(tableSchedule['date'].ge(begDate))
    if endDate:
        cond.append(tableSchedule['date'].le(endDate))
    if personId and not detailPerson:
        cond.append(tableSchedule['person_id'].eq(personId))
    if specialityId:
        cond.append(tablePerson['speciality_id'].eq(specialityId))
    if orgStructureId:
        cond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureDescendants(orgStructureId)))
    if appointmentType:
        cond.append(tableSchedule['appointmentType'].eq(appointmentType))
    if appointmentPurposeIdList:
        cond.append(tableSchedule['appointmentPurpose_id'].inlist(appointmentPurposeIdList))

    query = db.query(stmt % db.joinAnd(cond))
    while query.next():
        record = query.record()
        yield record



class CReportScheduleRegisteredCount(CReport):
    def __init__(self, parent=None):
        CReport.__init__(self, parent)
        self.setTitle(u'Отчет о количестве записанных пациентов на прием')


    def getSetupDialog(self, parent):
        result = CReportScheduleRegisteredCountSetup(parent)
        result.setWindowTitle(self.title())
        return result


    def getDescription(self, params):
        rows = CReport.getDescription(self, params)
        appointmentPurposeIdList = params.get('appointmentPurposeIdList')
        appointmentType = params.get('appointmentType', 0)
        if appointmentPurposeIdList:
            rows.append(u'Назначение приема: ' + formatAppointmentPurposeNames(appointmentPurposeIdList))
        if appointmentType:
            rows.append(u'Тип приема: ' + (u'амбулаторно' if appointmentType == 1 else u'на дому'))
        return rows


    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()

        detailPerson = params.get('detailPerson', False)

        reportData = {}  # ([person] если детализировать)[date][purpose]['busy'/'free']
        purposes = set()
        for record in selectData(params):
            date = forceDate(record.value('date')).toJulianDay()
            firstName = forceString(record.value('firstName'))
            lastName = forceString(record.value('lastName'))
            patrName = forceString(record.value('patrName'))
            specialityName = forceString(record.value('specialityName'))
            purposeName = forceString(record.value('purposeName'))
            capacity = forceInt(record.value('capacity'))
            busy = forceInt(record.value('countBusy'))
            personString = formatName(lastName, firstName, patrName) + ', ' + specialityName

            purposes.add(purposeName)
            if busy > capacity:
                busy = capacity

            if detailPerson:
                if not personString in reportData:
                    reportData[personString] = {}
                dict = reportData[personString]
            else:
                dict = reportData

            if not date in dict:
                dict[date] = {}
                dict[date][purposeName] = {}
                dict[date][purposeName]['busy'] = 0
                dict[date][purposeName]['free'] = 0
            if not purposeName in dict[date]:
                dict[date][purposeName] = {}
                dict[date][purposeName]['busy'] = 0
                dict[date][purposeName]['free'] = 0

            dict = dict[date][purposeName]
            dict['busy'] += busy
            dict['free'] += capacity - busy


        tableColumns = [ ('', ['', u'Дата'], CReportBase.AlignLeft),
                         ('', ['', u'Всего'], CReportBase.AlignLeft),
                         ('', ['', u'Занято'], CReportBase.AlignLeft),
                         ('', ['', u'Свободно'], CReportBase.AlignLeft),
                       ]
        for name in purposes:
            tableColumns.append(('', [name, u'Всего'], CReportBase.AlignLeft))
            tableColumns.append(('', ['', u'Занято'], CReportBase.AlignLeft))
            tableColumns.append(('', ['', u'Свободно'], CReportBase.AlignLeft))
        table = createTable(cursor, tableColumns)
        for i in xrange(4):
            table.mergeCells(0,i, 2,1)
        for i in xrange(len(purposes)):
            table.mergeCells(0,4+i*3, 1, 3)

        fmt = table.table.format()
        fmt.setWidth(QtGui.QTextLength(QtGui.QTextLength.PercentageLength, 100))
        table.table.setFormat(fmt)

        boldChars = QtGui.QTextCharFormat()
        boldChars.setFontWeight(QtGui.QFont.Bold)

        def writeDates(datesDict):
            for date in sorted(datesDict.keys()):
                purposesDict = datesDict[date]
                totalForDate = {'busy': 0, 'free': 0}
                row = table.addRow()
                col = 4
                for purposeName in purposes:
                    counts = purposesDict.get(purposeName, {'busy':0, 'free':0})
                    table.setText(row, col+0, counts['busy'] + counts['free'])
                    table.setText(row, col+1, counts['busy'])
                    table.setText(row, col+2, counts['free'])
                    col += 3
                    totalForDate['busy'] += counts['busy']
                    totalForDate['free'] += counts['free']

                table.setText(row, 0, formatDate(QDate.fromJulianDay(date)))
                table.setText(row, 1, totalForDate['busy'] + totalForDate['free'])
                table.setText(row, 2, totalForDate['busy'])
                table.setText(row, 3, totalForDate['free'])

        if detailPerson:
            for personString in sorted(reportData.keys()):
                personRow = table.addRow()
                table.setText(personRow, 0, personString, charFormat=boldChars)
                table.mergeCells(personRow,0, 1,len(tableColumns))
                writeDates(reportData[personString])
        else:
            writeDates(reportData)

        return doc




class CReportScheduleRegisteredCountSetup(CDialogBase, Ui_ReportScheduleRegisteredCountSetup):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())
        self.cmbSpeciality.setTable('rbSpeciality')


    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.cmbSpeciality.setValue(params.get('specialityId', None))
        self.chkDetailPerson.setChecked(params.get('detailPerson', False))
        self.cmbPerson.setValue(params.get('personId', None))
        self.cmbAppointmentType.setCurrentIndex(params.get('appointmentType', 0))
        self.setAppointmentPurposeList(params.get('appointmentPurposeIdList', []))


    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['orgStructureId'] = self.cmbOrgStructure.value()
        result['specialityId'] = self.cmbSpeciality.value()
        result['detailPerson'] = self.chkDetailPerson.isChecked()
        result['personId'] = self.cmbPerson.value()
        result['appointmentType'] = self.cmbAppointmentType.currentIndex()
        result['appointmentPurposeIdList'] = self.appointmentPurposeIdList
        return result


    def setAppointmentPurposeList(self, items):
        self.appointmentPurposeIdList = items
        if self.appointmentPurposeIdList:
            self.lblAppointmentPurpose.setText(formatAppointmentPurposeNames(items))
        else:
            self.lblAppointmentPurpose.setText(u'не задано')


    @pyqtSignature('bool')
    def on_btnAppointmentPurpose_clicked(self, checked=False):
        dialog = CAppointmentPurposeListEditorDialog(self)
        if dialog.exec_():
            self.setAppointmentPurposeList(dialog.values())


    @pyqtSignature('int')
    def on_cmbOrgStructure_currentIndexChanged(self, index):
        orgStructureId = self.cmbOrgStructure.value()
        self.cmbPerson.setOrgStructureId(orgStructureId)


    @pyqtSignature('int')
    def on_cmbSpeciality_currentIndexChanged(self, index):
        specialityId = self.cmbSpeciality.value()
        self.cmbPerson.setSpecialityId(specialityId)




class CAppointmentPurposeTableModel(CTableModel):
    def __init__(self, parent):
        CTableModel.__init__(self, parent)
        self.addColumn(CTextCol(u'Код',          ['code'], 30))
        self.addColumn(CTextCol(u'Наименование', ['name'], 70))
        self.setTable('rbAppointmentPurpose')


    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable



from Events.Ui_EventTypeListEditor import Ui_EventTypeListEditor

class CAppointmentPurposeListEditorDialog(QtGui.QDialog, Ui_EventTypeListEditor):
    def __init__(self, parent, filter=None):
        QtGui.QDialog.__init__(self, parent)
        self.tableModel = CAppointmentPurposeTableModel(self)
        self.tableSelectionModel = QtGui.QItemSelectionModel(self.tableModel, self)
        self.tableSelectionModel.setObjectName('tableSelectionModel')

        self.setupUi(self)
        self.tblAppointmentTypeList = self.tblEventTypeList
        del self.tblEventTypeList

        self.tblAppointmentTypeList.setModel(self.tableModel)
        self.tblAppointmentTypeList.setSelectionModel(self.tableSelectionModel)
        self.tblAppointmentTypeList.installEventFilter(self)
        self.appointmentPurposeIdList = []
        self.filter = filter
        self.tableModel.setIdList(QtGui.qApp.db.getIdList('rbAppointmentPurpose', 'id'))
        self.setWindowTitle(u'Назначение приема')


    @pyqtSignature('QAbstractButton*')
    def on_buttonBox_clicked(self, button):
        buttonCode = self.buttonBox.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Ok:
            self.appointmentPurposeIdList = self.tblAppointmentTypeList.selectedItemIdList()
        self.close()


    def values(self):
        return self.appointmentPurposeIdList


    def setValue(self, appointmentPurposeIdList):
        self.appointmentPurposeIdList = appointmentPurposeIdList

