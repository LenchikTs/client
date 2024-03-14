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
from PyQt4.QtCore import pyqtSignature, QDate

from library.Utils       import firstYearDay, forceDate, forceInt, forceRef, forceString, lastYearDay

from Events.ActionStatus import CActionStatus
from Reports.ReportBase  import CReportBase, createTable
from Reports.Report      import CReport
from Reports.ReportView  import CPageFormat
from Reports.Utils       import dateRangeAsStr


from Reports.Ui_SetupReportYearActions import Ui_SetupReportYearActionsDialog


def selectData(params, patBegDate, partEndDate):
    db = QtGui.qApp.db

    begDate = patBegDate
    endDate = partEndDate
    financeId = params.get('financeId', None)
    class_ = params.get('class', None)
    actionTypeGroupId = params.get('actionTypeGroupId', None)
    if actionTypeGroupId:
        actionTypeGroupIdList = db.getDescendants('ActionType', 'group_id', actionTypeGroupId)
    else:
        actionTypeGroupIdList = None
    status = params.get('status', None)
    orgStructureId = params.get('orgStructureId', None)
    personId = params.get('personId', None)
    assistantId = params.get('assistantId', None)
    tissueTypeId = params.get('tissueTypeId', None)

    tableAction        = db.table('Action')
    tableActionType    = db.table('ActionType')
    tablePerson        = db.table('Person')
    tableTissueJournal = db.table('TakenTissueJournal')
    cond = [tableAction['deleted'].eq(0),
            tableAction['endDate'].ge(begDate),
            tableAction['endDate'].lt(endDate.addDays(1)),
           ]
    if financeId:
        cond.append(tableAction['finance_id'].eq(financeId))
    if class_ is not None:
        cond.append(tableActionType['class'].eq(class_))
    if actionTypeGroupIdList:
        cond.append(tableActionType['group_id'].inlist(actionTypeGroupIdList))
    if status is not None:
        cond.append(tableAction['status'].eq(status))
    if orgStructureId:
        cond.append(tablePerson['orgStructure_id'].eq(orgStructureId))
    if personId:
        cond.append(tableAction['person_id'].eq(personId))
    if assistantId:
        cond.append(tableAction['assistant_id'].eq(assistantId))
    if tissueTypeId:
        if tissueTypeId == -1:
            cond.append(tableTissueJournal['tissueType_id'].isNotNull())
        else:
            cond.append(tableTissueJournal['tissueType_id'].eq(tissueTypeId))

    stmt = '''
SELECT
sum(`Action`.`amount`) AS amount,
`Action`.`endDate`,
`ActionType`.`id` AS actionTypeId,
`ActionType`.`class`,
`ActionType`.`code`,
`ActionType`.`name`,
`ParentActionType`.`id`    AS parentActionTypeId,
`ParentActionType`.`class` AS parentActionTypeClass,
`ParentActionType`.`code`  AS parentActionTypeCode,
`ParentActionType`.`name`  AS parentActionTypeName
FROM Action
INNER JOIN ActionType ON ActionType.`id` = `Action`.`actionType_id`
LEFT JOIN `Person` ON `Person`.`id` = `Action`.`setPerson_id`
LEFT JOIN `ActionType` AS `ParentActionType` ON `ParentActionType`.`id`=ActionType.`group_id`
LEFT JOIN `TakenTissueJournal` ON `TakenTissueJournal`.`id` = `Action`.`takenTissueJournal_id`
WHERE
Action.`deleted`=0 AND %s
GROUP BY `Action`.`actionType_id`, `Action`.`endDate`
''' % db.joinAnd(cond)
    return db.query(stmt)


class CReportYearActions(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Сводка об услугах за год')
        self.orientation = CPageFormat.Landscape


    def getSetupDialog(self, parent):
        result = CSetupReportYearActions(parent)
        result.setSexVisible(False)
        result.setAgeVisible(False)
        result.setTitle(self.title())
        return result


    def build(self, params):
        params['begDate'] = begDate = params.get('begDate', None) or firstYearDay(QDate.currentDate())
        params['endDate'] = endDate = params.get('endDate', None) or lastYearDay(begDate)

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)

        outDate = lastYearDay(endDate)
        partBegDate = begDate
        while partBegDate < outDate:
            partEndDate = min(lastYearDay(partBegDate), endDate)
            if partEndDate > endDate:
                partEndDate = endDate
            query = selectData(params, partBegDate, partEndDate)
            reportData, mapActionTypeIdToInfo = self.makeStructAction(query, partBegDate, partEndDate)
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.insertBlock()
            if partBegDate!=begDate:
                cursor.insertBlock()
            self.outputMonthTable(cursor, partBegDate, partEndDate, reportData, mapActionTypeIdToInfo)
            partBegDate = firstYearDay(partBegDate).addYears(1)
        return doc


    def makeStructAction(self, query, partBegDate, partEndDate):
        daysInPart = partEndDate.month()
        reportData = {}
        mapActionTypeIdToInfo   = { None: (100, None, '-') }

        while query.next():
            record = query.record()
            amount               = forceInt(record.value('amount'))
            date                 = forceDate(record.value('endDate'))
            parentActionTypeId   = forceRef(record.value('parentActionTypeId'))
            parentActionTypeClass= forceString(record.value('parentActionTypeClass'))
            parentActionTypeCode = forceString(record.value('parentActionTypeCode'))
            parentActionTypeName = forceString(record.value('parentActionTypeName'))
            actionTypeId         = forceRef(record.value('actionTypeId'))
            actionTypeClass      = forceString(record.value('class'))
            actionTypeCode       = forceString(record.value('code'))
            actionTypeName       = forceString(record.value('name'))

            parentData = reportData.setdefault(parentActionTypeId, {})
            values     = parentData.get(actionTypeId)
            if values is None:
                parentData[actionTypeId] = values = [0]*daysInPart
            values[date.month()-1] += amount

            if parentActionTypeId not in mapActionTypeIdToInfo:
                mapActionTypeIdToInfo[parentActionTypeId] = parentActionTypeClass, parentActionTypeCode, parentActionTypeName
            if actionTypeId not in mapActionTypeIdToInfo:
                mapActionTypeIdToInfo[actionTypeId] = actionTypeClass, actionTypeCode, actionTypeName
        return reportData, mapActionTypeIdToInfo


    def outputMonthTable(self, cursor, partBegDate, partEndDate, reportData, mapActionTypeIdToInfo):
        def formatInfo(info):
            return u' | '.join(filter(None, info[1:]))

        daysInPart = partEndDate.month()
#        partBegDateDay = partBegDate.day()

        cursor.setCharFormat(CReportBase.ReportSubTitle)
        cursor.insertText('%s' % (partBegDate.year()))
        cursor.insertBlock()

        tableColumns = [('2%', [u'№'], CReportBase.AlignRight),
                        ('20%', [u'Наименование\nгруппы/действия'], CReportBase.AlignLeft)]
        monthList = [u'Январь', u'Февраль', u'Март', u'Апрель', u'Май', u'Июнь', u'Июль', u'Август', u'Сентябрь', u'Октябрь', u'Ноябрь', u'Декабрь']
        colSize = '%.2f'%(78.0/daysInPart)
        daysColumns =  [(colSize, ['%s' % (monthList[i])], CReportBase.AlignRight)
                        for i in range(daysInPart)
                       ]
        tableColumns.extend(daysColumns)
        tableColumns.extend([('3%', [u'Итого'], CReportBase.AlignRight)])

        table = createTable(cursor, tableColumns)

        boldChars = QtGui.QTextCharFormat()
        boldChars.setFontWeight(QtGui.QFont.Bold)

        iActionTypes = 1
        resultValues = [0]*(daysInPart+1) # +1 - это колонка «итого»

        spaceShift = ' '*6

        orderedActionTypeIdList = map( lambda item: item[0],
                                       sorted(mapActionTypeIdToInfo.iteritems(),
                                              key = lambda item: (item[0] is None, item[1], item[0])
                                             )
                                     )

        for parentActionTypeId in filter(lambda actionTypeId: actionTypeId in reportData,
                                         orderedActionTypeIdList):
            intermediateValues = [0]*(daysInPart+1) # +1 - это колонка «итого»
            i = table.addRow()
            ationTypeBlockName = formatInfo(mapActionTypeIdToInfo[parentActionTypeId])
            table.setText(i, 1, spaceShift+ationTypeBlockName, charFormat=boldChars)
            table.mergeCells(i, 0, 1, daysInPart+3)
            parentData = reportData[parentActionTypeId]
            for actionTypeId in filter(lambda actionTypeId: actionTypeId in parentData,
                                       orderedActionTypeIdList):
                i = table.addRow()
                table.setText(i, 0, iActionTypes)
                table.setText(i, 1, formatInfo(mapActionTypeIdToInfo[actionTypeId]))
                rowValue = 0
                for iDay, val in enumerate(parentData[actionTypeId]):
                    val = val if val else u''
                    table.setText(i, iDay+2, val)
                    if bool(val):
                        intermediateValues[iDay] += val
                        resultValues[iDay] += val
                        rowValue += val
                intermediateValues[-1] += rowValue
                table.setText(i, daysInPart+2, rowValue)
                iActionTypes += 1
            resultValues[-1] += intermediateValues[-1]

            i = table.addRow()
            table.mergeCells(i, 0, 1, 2)
            table.setText(i, 1, u'Итого', charFormat=boldChars)
            for iDay, val in enumerate(intermediateValues):
                val = val if val else u''
                table.setText(i, iDay+2, val, charFormat=boldChars)

            cursor.setCharFormat(CReportBase.TableBody)

        i = table.addRow()
        table.mergeCells(i, 0, 1, 2)
        table.setText(i, 1, u'Всего', charFormat=boldChars)
        for iDay, val in enumerate(resultValues):
            val = val if val else u''
            table.setText(i, iDay+2, val, charFormat=boldChars)


    def getDescription(self, params):
        begDate = params.get('begDate', None)
        endDate = params.get('endDate', None)
        financeId = params.get('financeId', None)
        class_ = params.get('class', None)
        actionTypeGroupId = params.get('actionTypeGroupId', None)
        status = params.get('status', None)
        orgStructureId = params.get('orgStructureId', None)
        personId = params.get('personId', None)
        assistantId = params.get('assistantId', None)
        tissueTypeId = params.get('tissueTypeId', None)

        rows = []
        if begDate or endDate:
            rows.append(dateRangeAsStr(u'за период', begDate, endDate))
        db = QtGui.qApp.db
        if financeId:
            rows.append(u'Тип финансирования: %s'%forceString(db.translate('rbFinance', 'id', financeId, 'name')))
        if class_ is not None:
            rows.append(u'Класс типов действия: %s'%[u'статус', u'диагностика', u'лечение', u'прочие мероприятия'][class_])
        if actionTypeGroupId:
            rows.append(u'Группа типов действий: %s'%forceString(db.translate('ActionType', 'id', actionTypeGroupId, 'CONCAT(code, \' | \', name)')))
        if status is not None:
            rows.append(u'Статус: %s'%CActionStatus.text(status))
        if orgStructureId:
            rows.append(u'Подразделение: %s'%forceString(db.translate('OrgStructure', 'id', orgStructureId, 'name')))
        if personId:
            rows.append(u'Назначивший: %s'%forceString(db.translate('vrbPersonWithSpeciality', 'id', personId, 'name')))
        if assistantId:
            rows.append(u'Ассистент: %s'%forceString(db.translate('vrbPersonWithSpeciality', 'id', assistantId, 'name')))
        if tissueTypeId:
            rows.append(u'Тип биоматериала: %s'%forceString(db.translate('rbTissueType', 'id', tissueTypeId, 'CONCAT(code, \' | \', name)')))
        return rows


class CSetupReportYearActions(QtGui.QDialog, Ui_SetupReportYearActionsDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.patientRequired = False
        self.setupUi(self)
        self.cmbFinance.setTable('rbFinance', addNone=True)
        self.cmbTissueType.setTable('rbTissueType', addNone=True, specialValues=[(-1, u'-', u'Любой')])

        self.getPeriodDates()
        self.cmbActionTypeGroup.setClass(None)
        self.cmbActionTypeGroup.model().setLeavesVisible(False)

        self._classVisible = True
        self._actionTypeGroupVisible = True
        self._financeVisible = True
        self._statusVisible = True
        self._assistantVisible = True
        self._tissueTypeVisible = True
        self._sexVisible = True
        self._ageVisible = True
        self._personDetailVisible = False
        self._localityVisible = False
        self.setPersonDetailVisible(self._personDetailVisible)


    def getPeriodDates(self):
        currentDate = QDate.currentDate()
        currentYear = currentDate.year()
        currentMonth = currentDate.month()
        currentDay = currentDate.day()
        self.edtBegDate.setDate(QDate(currentYear, currentMonth, 1))
        self.edtEndDate.setDate(QDate(currentYear, currentMonth, currentDay))


    def setPersonDetailVisible(self, value):
        self._personDetailVisible = value
        self.chkPersonDetail.setVisible(value)
        self.chkPersonOverall.setVisible(value)
        self.chkPersonDateDetail.setVisible(value)


    def setActionTypeClassVisible(self, value):
        self._classVisible = value
        self.chkClass.setVisible(value)
        self.cmbClass.setVisible(value)


    def setActionTypeGroupVisible(self, value):
        self._actionTypeGroupVisible = value
        self.chkActionTypeGroup.setVisible(value)
        self.cmbActionTypeGroup.setVisible(value)


    def setFinanceVisible(self, value):
        self._financeVisible = value
        self.chkFinance.setVisible(value)
        self.cmbFinance.setVisible(value)


    def setStatusVisible(self, value):
        self._statusVisible = value
        self.chkStatus.setVisible(value)
        self.cmbStatus.setVisible(value)


    def setAssistantVisible(self, value):
        self._assistantVisible = value
        self.chkAssistant.setVisible(value)
        self.cmbAssistant.setVisible(value)


    def setTissueTypeVisible(self, value):
        self._tissueTypeVisible = value
        self.chkTissueType.setVisible(value)
        self.cmbTissueType.setVisible(value)


    def setLocalityVisible(self, value):
        self._localityVisible = value
        self.chkLocality.setVisible(value)
        self.cmbLocality.setVisible(value)


    def setSexVisible(self, value):
        self._sexVisible = value
        self.chkSex.setVisible(value)
        self.cmbSex.setVisible(value)


    def setAgeVisible(self, value):
        self._ageVisible = value
        self.chkAge.setVisible(value)
        self.frmAge.setVisible(value)


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        if begDate and endDate:
            self.edtBegDate.setDate(begDate)
            self.edtEndDate.setDate(endDate)
        else:
            self.getPeriodDates()

        if self._financeVisible:
            chkFinance = params.get('chkFinance', False)
            self.chkFinance.setChecked(chkFinance)
            self.cmbFinance.setValue(params.get('financeId', None))

        if self._classVisible:
            chkClass = params.get('chkClass', False)
            self.chkClass.setChecked(chkClass)
            self.cmbClass.setCurrentIndex(params.get('class', 0))

        if self._actionTypeGroupVisible:
            chkActionTypeGroup = params.get('chkActionTypeGroup', False)
            self.chkActionTypeGroup.setChecked(chkActionTypeGroup)
            self.cmbActionTypeGroup.setValue(params.get('actionTypeGroupId', None))

        if self._statusVisible:
            chkStatus = params.get('chkStatus', False)
            self.chkStatus.setChecked(chkStatus)
            self.cmbStatus.setValue(params.get('status', CActionStatus.started))

        if self._localityVisible:
            locality = params.get('chkLocality', False)
            self.chkLocality.setChecked(locality)
            self.cmbLocality.setCurrentIndex(params.get('locality', 0))

        chkOrgStructure = params.get('chkOrgStructure', False)
        self.chkOrgStructure.setChecked(chkOrgStructure)
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))

        chkPerson = params.get('chkPerson', False)
        self.chkPerson.setChecked(chkPerson)
        self.cmbPerson.setValue(params.get('personId', None))

        if self._assistantVisible:
            chkAssistant = params.get('chkAssistant', False)
            self.chkAssistant.setChecked(chkAssistant)
            self.cmbAssistant.setValue(params.get('assistantId', None))

        if self._tissueTypeVisible:
            chkTissueType = params.get('chkTissueType', False)
            self.chkTissueType.setChecked(chkTissueType)
            self.cmbTissueType.setValue(params.get('tissueTypeId', None))

        if self._sexVisible:
            chkSex = params.get('chkSex', False)
            self.chkSex.setChecked(chkSex)
            self.cmbSex.setCurrentIndex(params.get('sex', 0))

        if self._ageVisible:
            chkAge = params.get('chkAge', False)
            self.chkAge.setChecked(chkAge)
            self.edtAgeFrom.setValue(params.get('ageFrom', 0))
            self.edtAgeTo.setValue(params.get('ageTo', 150))

        if self._personDetailVisible:
            self.chkPersonOSDetail.setChecked(params.get('chkPersonOSDetail', False))
            chkPersonDetail = params.get('chkPersonDetail', False)
            chkPersonOverall = params.get('chkPersonOverall', False)
            self.chkPersonOverall.setEnabled(not chkPersonDetail)
            self.chkPersonOverall.setChecked(chkPersonOverall)
            self.chkPersonDetail.setEnabled(not chkPersonOverall)
            self.chkPersonDetail.setChecked(chkPersonDetail and not chkPersonOverall)
            self.chkPersonDateDetail.setEnabled(chkPersonDetail or chkPersonOverall)
            self.chkPersonDateDetail.setChecked(params.get('chkPersonDateDetail', False))


    def params(self):
        params = {}
        params['begDate'] = self.edtBegDate.date()
        params['endDate'] = self.edtEndDate.date()

        if self._financeVisible:
            params['chkFinance']    = self.chkFinance.isChecked()
            if params['chkFinance']:
                params['financeId'] = params['financeId'] = self.cmbFinance.value() #typeFinanceId for report header

        if self._classVisible:
            params['chkClass']  = self.chkClass.isChecked()
            if params['chkClass']:
                params['class'] = self.cmbClass.currentIndex()

        if self._actionTypeGroupVisible:
            params['chkActionTypeGroup']    = self.chkActionTypeGroup.isChecked()
            if params['chkActionTypeGroup']:
                params['actionTypeGroupId'] = self.cmbActionTypeGroup.value()

        if self._statusVisible:
            params['chkStatus']  = self.chkStatus.isChecked()
            if params['chkStatus']:
                params['status'] = self.cmbStatus.value()

        params['chkOrgStructure']    = self.chkOrgStructure.isChecked()
        if params['chkOrgStructure']:
            params['orgStructureId'] = self.cmbOrgStructure.value()

        params['chkPerson']    = self.chkPerson.isChecked()
        if params['chkPerson']:
            params['personId'] = self.cmbPerson.value()

        if self._assistantVisible:
            params['chkAssistant']    = self.chkAssistant.isChecked()
            if params['chkAssistant']:
                params['assistantId'] = self.cmbAssistant.value()

        if self._tissueTypeVisible:
            params['chkTissueType']    = self.chkTissueType.isChecked()
            if params['chkTissueType']:
                params['tissueTypeId'] = self.cmbTissueType.value()

        if self._sexVisible:
            params['chkSex']    = self.chkSex.isChecked()
            if params['chkSex']:
                params['sex'] = self.cmbSex.currentIndex()

        if self._ageVisible:
            params['chkAge']    = self.chkAge.isChecked()
            if params['chkAge']:
                params['ageFrom'] = self.edtAgeFrom.value()
                params['ageTo'] = self.edtAgeTo.value()

        if self._localityVisible:
            params['chkLocality']     = self.chkLocality.isChecked()
            if params.get('chkLocality', False):
                params['locality']    = self.cmbLocality.currentIndex()

        if self._personDetailVisible:
            params['chkPersonOSDetail'] = self.chkPersonOSDetail.isChecked()
            params['chkPersonOverall'] = self.chkPersonOverall.isChecked()
            params['chkPersonDetail'] = self.chkPersonDetail.isChecked()
            params['chkPersonDateDetail'] = self.chkPersonDateDetail.isChecked()

        return params


    @pyqtSignature('bool')
    def on_chkPersonOSDetail_clicked(self, bValue):
        if bValue:
            self.chkPersonDetail.setChecked(False)
        self.chkPersonDetail.setEnabled(not bValue and not self.chkPersonOverall.isChecked())
        self.chkPersonDateDetail.setEnabled(bValue)


    @pyqtSignature('bool')
    def on_chkPersonOverall_clicked(self, bValue):
        if bValue:
            self.chkPersonDetail.setChecked(False)
        self.chkPersonDetail.setEnabled(not bValue and not self.chkPersonOSDetail.isChecked())
        self.chkPersonDateDetail.setEnabled(bValue)


    @pyqtSignature('bool')
    def on_chkPersonDetail_clicked(self, bValue):
        if bValue:
            self.chkPersonOverall.setChecked(False)
        self.chkPersonOverall.setEnabled(not bValue)


    @pyqtSignature('bool')
    def on_chkClass_clicked(self, bValue):
        if bValue:
            class_ = self.cmbClass.currentIndex()
        else:
            class_ = None
        self.cmbActionTypeGroup.setClass(class_)


    @pyqtSignature('int')
    def on_cmbClass_currentIndexChanged(self, index):
        self.cmbActionTypeGroup.setClass(index)
