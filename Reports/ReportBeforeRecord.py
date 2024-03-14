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

from library.DialogBase import CDialogBase
from library.Utils      import calcAge, forceBool, forceDate, forceInt, forceString, formatNameInt, formatShortNameInt

from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Registry.Utils     import getClientIdentifier, getAttachRecord
from Orgs.Utils         import getPersonInfo

from Reports.Ui_ReportBeforeRecordSetup import Ui_ReportBeforeRecordSetup


class CReportBeforeRecord(CReport):
    def __init__(self, schedule, scheduleList, parent = None):
        CReport.__init__(self, parent)
        self.setTitle(u'Список предварительной записи')
        self.schedule = schedule
        self.scheduleList = scheduleList
        self.table_columns = [
            ('5%',[u'№'], CReportBase.AlignRight),
            ('10%', [u'Время'], CReportBase.AlignLeft),
            ('35%', [u'ФИО'], CReportBase.AlignLeft),
            ('20%', [u'Идентификатор'], CReportBase.AlignLeft),
            ('30%', [u'Примечание'], CReportBase.AlignLeft),
               ]

    def getSetupDialog(self, parent):
        result = CReportBeforeRecordSetup(parent)
        result.setEnabledAllPeroids(len(self.scheduleList)>1)
        return result


    def build(self, params):
        numberType         = params.get('numberType', 0) # 0 - по порядку, 1 - по записи
        showTime           = params.get('showTime', True) # выводить время
        showBirthDate      = params.get('showBirthDate', False) # выводить дату рождения
        showAge            =  params.get('showAge', False) # выводить возраст
        showAttachment     =  params.get('showAttachment', False) # выводить прикрепление
        accountingSystemId = params.get('accountingSystemId', -1) # -1 - не выводить
        encodeName         = params.get('encodeName', True) # кодировать имя
        fillNote           = params.get('fillNote', False)  # заполнять примечания
        listOnlyQueued     = params.get('listOnlyQueued', False) # показывать только записанных
        allPeriodsEnabled  = params.get('allPeriodsEnabled', False) # есть ли другие периоды
        allPeriodsChecked  = params.get('allPeriodsChecked', False) # показывать другие периоды
        allPeriodsCombine  = params.get('allPeriodsCombine', False) # объединять периоды
        if numberType == 0:
            idx = lambda row, item: row+1
        else:
            idx = lambda row, item: item.idx+1
        if accountingSystemId == -1:
            identifier = lambda item: ''
        elif accountingSystemId is None:
            identifier = lambda item: str(item.clientId) if item.clientId else ''
        else:
            identifier = lambda item: getClientIdentifier(accountingSystemId, item.clientId) if item.clientId else ''
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.setCharFormat(CReportBase.ReportBody)
        scheduleList = self.scheduleList if allPeriodsEnabled and allPeriodsChecked else [self.schedule]
        firstStep = True
        boldChars = QtGui.QTextCharFormat()
        boldChars.setFontPointSize(12)
        for schedule in scheduleList:
            if listOnlyQueued:
                items = [item for item in schedule.items if item.clientId]
            else:
                items = schedule.items
            pi = getPersonInfo(schedule.personId)
            if firstStep or not allPeriodsCombine:
                table = createTable (cursor, [ ('30%', [], CReportBase.AlignLeft),
                                           ('70%', [], CReportBase.AlignLeft)
                                         ], headerRowCount=0, border=0, cellPadding=2, cellSpacing=0)

            if firstStep:
                i = table.addRow()
                table.setText(i, 0, u'Врач', charFormat=boldChars)
                table.setText(i, 1, pi.get('fullName', ''), charFormat=boldChars)
                i = table.addRow()
                table.setText(i, 0, u'Специальность', charFormat=boldChars)
                table.setText(i, 1, pi.get('specialityName', ''), charFormat=boldChars)
                i = table.addRow()
                table.setText(i, 0, u'Дата', charFormat=boldChars)
                table.setText(i, 1, forceString(schedule.date), charFormat=boldChars)
            
            if not allPeriodsCombine:
                i = table.addRow()
                table.setText(i, 0, u'Период', charFormat=boldChars)
                table.setText(i, 1, u'c %s по %s'% (schedule.begTime.toString('hh:mm'),
                                                    schedule.endTime.toString('hh:mm'),
                                                   ), charFormat=boldChars
                              )
                i = table.addRow()
                table.setText(i, 0, u'Кабинет', charFormat=boldChars)
                table.setText(i, 1, schedule.office, charFormat=boldChars)
            
            if not allPeriodsCombine or firstStep:
                cursor.movePosition(QtGui.QTextCursor.End)
                cursor.insertBlock()
                cursor.setCharFormat(CReportBase.ReportBody)
                cursor.insertBlock()
                tableColumns = []
                ciNumber = 0
                tableColumns.append(     ('10%',   [ u'№' ],             CReportBase.AlignCenter))
                if showTime:
                    ciTime = len(tableColumns)
                    tableColumns.append( ('10%',   [ u'ВРЕМЯ' ],         CReportBase.AlignCenter))
                ciName = len(tableColumns)
                tableColumns.append(     ('30%',   [ u'ФИО' ],           CReportBase.AlignLeft))
                if showBirthDate:
                    ciBirthDate = len(tableColumns)
                    tableColumns.append( ('15%',   [ u'ДАТА РОЖД.' ], CReportBase.AlignLeft))
                if showAge:
                    ciAge = len(tableColumns)
                    tableColumns.append( ('15%',   [ u'ВОЗРАСТ' ], CReportBase.AlignLeft))
                if showAttachment:
                    ciAttachment = len(tableColumns)
                    tableColumns.append( ('15%',   [ u'ПРИКРЕПЛЕНИЕ' ], CReportBase.AlignLeft))
                if accountingSystemId != -1:
                    ciIdentifier = len(tableColumns)
                    tableColumns.append( ('20%',   [ u'ИДЕНТИФИКАТОР' ], CReportBase.AlignLeft))
                ciNote = len(tableColumns)
                tableColumns.append(     ('30%',   [ u'ПРИМЕЧАНИЕ' ],    CReportBase.AlignLeft))
                table = createTable(cursor, tableColumns)
                
            for row, item in enumerate(items):
                i = table.addRow()
                table.setText(i, ciNumber, idx(row, item), charFormat=boldChars)
                if showTime:
                    table.setText(i, ciTime, item.time.toString('hh:mm'), charFormat=boldChars)
                table.setText(i, ciName, self.getClientName(item.clientId, encodeName), charFormat=boldChars)
                if showBirthDate or showAge:
                    birthDate = self.getClientBirthDate(item.clientId)
                if showBirthDate:
                    table.setText(i, ciBirthDate, birthDate.toString("dd.MM.yyyy") if birthDate else "", charFormat=boldChars)
                if showAge:
                    clientAge = calcAge(birthDate, schedule.date) if item.clientId else None
                    table.setText(i, ciAge, forceString(clientAge) if clientAge else "", charFormat=boldChars)
                if showAttachment:
                    orgStrCode = None
                    if item.clientId:
                        attachment = getAttachRecord(item.clientId, 0)
                        if attachment:
                            orgStrCode = forceString(QtGui.qApp.db.translate('OrgStructure', 'id', attachment['orgStructure_id'], 'code'))
                        else:
                            attachment = getAttachRecord(item.clientId, 1)
                            if attachment:
                                orgStrCode = forceString(QtGui.qApp.db.translate('OrgStructure', 'id', attachment['orgStructure_id'], 'code'))
                    table.setText(i, ciAttachment, forceString(orgStrCode) if orgStrCode else u'', charFormat=boldChars)
                if accountingSystemId != -1:
                    table.setText(i, ciIdentifier, identifier(item), charFormat=boldChars)
                if fillNote:
                    table.setText(i, ciNote, item.complaint, charFormat=boldChars)
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.insertBlock()
            firstStep = False
        return doc


    def getClientName(self, clientId, encoded):
        db = QtGui.qApp.db
        table  = db.table('Client')
        record = db.getRecord(table, 'lastName, firstName, patrName', clientId)
        if record:
            lastName  = forceString(record.value('lastName'))
            firstName = forceString(record.value('firstName'))
            patrName  = forceString(record.value('patrName'))
            if encoded:
                return formatShortNameInt(lastName[:3]+ '*'*(len(lastName)-3), firstName, patrName)
            else:
                return formatNameInt(lastName, firstName, patrName)
        else:
            return ''


    def getClientBirthDate(self, clientId):
        db = QtGui.qApp.db
        table  = db.table('Client')
        record = db.getRecord(table, 'birthDate', clientId)
        if record:
            return forceDate(record.value('birthDate'))
        else:
            return None


class CReportBeforeRecordSetup(CDialogBase, Ui_ReportBeforeRecordSetup):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.cmbAccountingSystem.setTable('rbAccountingSystem', addNone=False, filter='showInClientInfo = 1')
        self.cmbAccountingSystem.setSpecialValues(((-1,   '',  u'не выводить'),
                                                   (None, '',  u'не задано'),
                                                  )
                                                 )

        self.setEnabledAllPeroids(False)

    def setEnabledAllPeroids(self, value):
        self.chkAllPeriods.setEnabled(value)
        self.lblAllPeriods.setEnabled(value)


    def setParams(self, params):
        reportPrefs        = QtGui.qApp.preferences.reportPrefs.get(u'список предварительной записи', {})
        numberType         = forceInt(reportPrefs.get('numbertype', 0))
        showTime           = forceBool(reportPrefs.get('showtime', True))
        showBirthDate      = forceBool(reportPrefs.get('showbirthdate', False))
        showAge      = forceBool(reportPrefs.get('showAge', False))
        showAttachment      = forceBool(reportPrefs.get('showAttachment', False))
        accountingSystemId = forceInt(reportPrefs.get('accountingsystemid', -1))
        encodeName         = forceBool(reportPrefs.get('encodename', True))
        fillNote           = forceBool(reportPrefs.get('fillnote', False))
        listOnlyQueued     = forceBool(reportPrefs.get('listonlyqueued', False))
        allPeriodsChecked  = forceBool(reportPrefs.get('allperiodschecked', False))
        allPeriodsCombine  = forceBool(reportPrefs.get('allPeriodsCombine', False))

        self.cmbNumberType.setCurrentIndex(params.get('numberType',             numberType))
        self.cmbShowTime.setCurrentIndex(int(params.get('showTime',             showTime)))
        self.cmbAccountingSystem.setValue(params.get('accountingSystemId',      accountingSystemId))
        self.cmbEncodeName.setCurrentIndex(int(params.get('encodeName',         encodeName)))
        self.cmbFillNote.setCurrentIndex(int(params.get('fillNote',             fillNote)))
        self.cmbListOnlyQueued.setCurrentIndex(int(params.get('listOnlyQueued', listOnlyQueued)))
        self.chkAllPeriods.setChecked(params.get('allPeriodsChecked',           allPeriodsChecked))
        self.chkAllPeriodsCombine.setChecked(params.get('allPeriodsCombine',           allPeriodsCombine))
        self.chkBirthDate.setChecked(params.get('showBirthDate',                showBirthDate))
        self.chkAge.setChecked(params.get('showAge',                showAge))
        self.chkAttachment.setChecked(params.get('showAttachment',                showAttachment))


    def params(self):
        return dict(
                    numberType         = self.cmbNumberType.currentIndex(),
                    showTime           = bool(self.cmbShowTime.currentIndex()),
                    accountingSystemId = self.cmbAccountingSystem.value(),
                    encodeName         = bool(self.cmbEncodeName.currentIndex()),
                    fillNote           = bool(self.cmbFillNote.currentIndex()),
                    listOnlyQueued     = bool(self.cmbListOnlyQueued.currentIndex()),
                    allPeriodsEnabled  = self.chkAllPeriods.isEnabled(),
                    allPeriodsChecked  = self.chkAllPeriods.isChecked(),
                    allPeriodsCombine  = self.chkAllPeriodsCombine.isChecked(),
                    showBirthDate      = self.chkBirthDate.isChecked(),
                    showAge            = self.chkAge.isChecked(), 
                    showAttachment     = self.chkAttachment.isChecked()
                   )
