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

from PyQt4                import QtGui
from PyQt4.QtCore         import QDate, QTime, QDateTime

from library.Utils        import forceString, forceInt
from Reports.Report       import CReport
from Reports.ReportBase   import CReportBase, createTable
from Reports.ReportView   import CPageFormat
from Reports.Utils        import dateRangeAsStr
from Orgs.Utils           import getOrganisationInfo, getOrgStructureName

from Reports.Ui_ReportTreatedPatientsForComorbiditiesSetupDialog import Ui_ReportTreatedPatientsForComorbiditiesSetupDialog
from Reports.ReportTreatedPatientsForMajorDiseases import getMKBClassBlockName

BUILD_BY_DISEASES_CLASSES = 0
BUILD_BY_DISEASES_GROUPS = 1
BUILD_BY_DISEASES = 2

def selectData(params, orgStructureList):
    reportData = dict()  # { MKB:{name:'', with1Disease:0, with2Disease:0, with3Disease:0}, ... }
    totalCount = dict(all=0, with1Disease=0, with2Disease=0, with3Disease=0)
    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())

    db = QtGui.qApp.db
    tableEvent            = db.table('Event')
    tableEventType        = db.table('EventType')
    tableRbMedicalAidType = db.table('rbMedicalAidType')
    tableMKB              = db.table('MKB')
    tableDiagnostic       = db.table('Diagnostic')
    tableDiagnosis        = db.table('Diagnosis')
    tableDiagnosisType    = db.table('rbDiagnosisType')
    tablePerson           = db.table('Person')
    tableAction           = db.table('Action')
    tableActionType       = db.table('ActionType')

    cond = [ tableEvent['deleted'].eq(0),
             tableEvent['isClosed'].eq(1),
             tableEventType['deleted'].eq(0),
             tablePerson['org_id'].eq(QtGui.qApp.currentOrgId()),
             tableRbMedicalAidType['code'].eq(8),
             tableDiagnosis['deleted'].eq(0),
             tableDiagnostic['deleted'].eq(0),
             tableActionType['flatCode'].eq('leaved'),
             tableEventType['form'].eq('072')
            ]
    if begDate:
        begDate = QDateTime(begDate)
        begDate.setTime(QTime(9,0,0))
        cond.append(tableAction['endDate'].ge(begDate))
    if endDate:
        endDate = QDateTime(endDate)
        endDate.setTime(QTime(9,0,0))
        cond.append(tableAction['endDate'].le(endDate))
    if orgStructureList != []:
        cond.append(tablePerson['orgStructure_id'].inlist(orgStructureList))

    queryTable = tableEvent
    queryTable = queryTable.innerJoin(tablePerson, tablePerson['id'].eq(tableEvent['execPerson_id']))
    queryTable = queryTable.innerJoin(tableEventType, tableEventType['id'].eq(tableEvent['eventType_id']))
    queryTable = queryTable.innerJoin(tableAction, tableAction['event_id'].eq(tableEvent['id']))
    queryTable = queryTable.innerJoin(tableActionType, tableAction['actionType_id'].eq(tableActionType['id']))
    queryTable = queryTable.innerJoin(tableRbMedicalAidType, tableRbMedicalAidType['id'].eq(tableEventType['medicalAidType_id']))
    queryTable = queryTable.innerJoin(tableDiagnostic, tableDiagnostic['event_id'].eq(tableEvent['id']))
    queryTable = queryTable.innerJoin(tableDiagnosis, tableDiagnostic['diagnosis_id'].eq(tableDiagnosis['id']))
    queryTable = queryTable.innerJoin(tableDiagnosisType, tableDiagnosis['diagnosisType_id'].eq(tableDiagnosisType['id']))
    if params['buildCond'] == BUILD_BY_DISEASES_GROUPS:
        queryTable = queryTable.innerJoin(tableMKB, 'LEFT(Diagnosis.MKB, 3) = MKB.DiagID')
    else:
        queryTable = queryTable.innerJoin(tableMKB, 'LEFT(Diagnosis.MKB, 5) = MKB.DiagID') # После точки учитываем только 1 знак

    eventList = list()
    stmt = db.selectStmt(queryTable, 'DISTINCT Event.id', where=cond, order=tableDiagnosis['MKB'].name())
    query = db.query(stmt)
    while query.next():
        eventList.append( forceInt(query.value(0)) )
    totalCount['all'] = len(eventList)


    cols = None
    if params['buildCond'] == BUILD_BY_DISEASES or params['buildCond'] == BUILD_BY_DISEASES_GROUPS:
        cols = [ tableMKB['DiagID'].alias('diagnosisCode'), tableMKB['DiagName'].alias('diagnosisName') ]
    else:  # BUILD_BY_DISEASES_CLASSES
        cols = [ tableMKB['ClassID'].alias('diagnosisCode'), tableMKB['ClassName'].alias('diagnosisName') ]

    cond.append(tableDiagnosisType['code'].eq(9))

    for eventID in eventList:
        stmt = db.selectStmt(queryTable, cols, where=cond + [tableEvent['id'].eq(eventID)])
        diagnosisList = list()
        query = db.query(stmt)
        while query.next():
            record = query.record()
            diagnosisCode = forceString(record.value('diagnosisCode'))
            if params['buildCond'] == BUILD_BY_DISEASES_CLASSES:
                diagnosisCode = getMKBClassBlockName(diagnosisCode)
            diagnosisName = forceString(record.value('diagnosisName'))
            diagnosisList.append(dict(code=diagnosisCode, name=diagnosisName))

        diagnosisCount = len(diagnosisList)
        totalCount['with1Disease'] += int(diagnosisCount == 1)
        totalCount['with2Disease'] += int(diagnosisCount == 2)
        totalCount['with3Disease'] += int(diagnosisCount >= 3)

        for diag in diagnosisList:
            diagnosisCode = diag['code']
            diagnosisName = diag['name']
            if not reportData.has_key(diagnosisCode):
                reportData[diagnosisCode] = dict(with1Disease=0, with2Disease=0, with3Disease=0, name=diagnosisName)
            reportData[diagnosisCode]['with1Disease'] += int(diagnosisCount == 1)
            reportData[diagnosisCode]['with2Disease'] += int(diagnosisCount == 2)
            reportData[diagnosisCode]['with3Disease'] += int(diagnosisCount >= 3)

    return reportData, totalCount



class CReportTreatedPatientsForComorbidities(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Отчет о пролеченных больных по сопутствующим заболеваниям')


    def getSetupDialog(self, parent):
        result = CReportTreatedPatientsForComorbiditiesSetupDialog(parent)
        result.setTitle(self.title())
        self.reportTreatedPatientsForComorbiditiesSetupDialog = result
        return result


    def getCurrentOrgStructureIdList(self):
        cmbOrgStruct = self.reportTreatedPatientsForComorbiditiesSetupDialog.cmbOrgStructure
        treeIndex = cmbOrgStruct._model.index(cmbOrgStruct.currentIndex(), 0, cmbOrgStruct.rootModelIndex())
        treeItem = treeIndex.internalPointer() if treeIndex.isValid() else None
        return treeItem.getItemIdList() if treeItem else []


    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setBlockFormat(CReportBase.AlignCenter)
        cursor.setCharFormat(CReportBase.ReportBody)

        orgId = QtGui.qApp.currentOrgId()
        orgInfo = getOrganisationInfo(orgId)
        orgName = orgInfo.get('fullName', u'ЛПУ в настройках не указано!')
        cursor.insertText(orgName)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'\nОтчет о пролеченных больных по сопутствующим заболеваниям\n')
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertText(dateRangeAsStr(u'за период', params['begDate'], params['endDate']))
        if not params['orgStructure']:
            cursor.insertText(u'\n(по сопуствующему заболеванию) все отделения')
        else:
            cursor.insertText(u'\n(по сопуствующему заболеванию) ' + getOrgStructureName(params['orgStructure']))
        cursor.insertBlock()

        alignLeft = CReportBase.AlignLeft
        alignRight = CReportBase.AlignRight
        alignCenter = CReportBase.AlignCenter
        charBold = QtGui.QTextCharFormat()
        charBold.setFontWeight(QtGui.QFont.Bold)


        # Вычисление процента 'piece' от 'value' с точностью до 0,01 и запятой в качестве разделителя
        def percentRaito(value, piece):
            if value == 0: return '100%'
            elif piece == 0: return '0%'
            else: return ("%g%%" % round(piece / float(value) * 100, 2)).replace('.', ',', 1)


        colTitle = u'% больных' if params['showPercentages'] else ''
        tableColumns = [ ('10%', [u'Код', ''], alignLeft),
                         ('5%',  [u'Класс, диагноз', ''], alignLeft),
                         ('15%', ['', ''], alignLeft),
                         ('5%',  ['', ''], alignLeft),
                         ('5%',  ['', ''], alignLeft),
                         ('10%', [u'Одно сопутствующее заболевание', u'больных'], alignLeft),
                         ('10%', ['', colTitle], alignLeft),
                         ('10%', [u'Два сопутствующих заболевания', u'больных'], alignLeft),
                         ('10%', ['', colTitle], alignLeft),
                         ('10%', [u'Три и более сопутствующих заболеваний', u'больных'], alignLeft),
                         ('10%', ['', colTitle], alignLeft)
                       ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 4)
        table.mergeCells(0, 5, 1, 2)
        table.mergeCells(0, 7, 1, 2)
        table.mergeCells(0, 9, 1, 2)

        if not params['showPercentages']:
            table.mergeCells(1, 5, 1, 2)
            table.mergeCells(1, 7, 1, 2)
            table.mergeCells(1, 9, 1, 2)

        reportData, totalCount = selectData(params, orgStructureList=self.getCurrentOrgStructureIdList())
        for diagnosisCode, diagnosisInfo in sorted(reportData.items()):
            row = table.addRow()
            table.setText(row, 0, diagnosisCode)
            table.setText(row, 1, diagnosisInfo['name'])
            table.setText(row, 5, diagnosisInfo['with1Disease'], blockFormat=alignRight)
            table.setText(row, 7, diagnosisInfo['with2Disease'], blockFormat=alignRight)
            table.setText(row, 9, diagnosisInfo['with3Disease'], blockFormat=alignRight)
            if params['showPercentages']:
                table.setText(row, 6, percentRaito(totalCount['all'], diagnosisInfo['with1Disease']), blockFormat=alignRight)
                table.setText(row, 8, percentRaito(totalCount['all'], diagnosisInfo['with2Disease']), blockFormat=alignRight)
                table.setText(row,10, percentRaito(totalCount['all'], diagnosisInfo['with3Disease']), blockFormat=alignRight)
            else:
                table.mergeCells(row, 5, 1, 2)
                table.mergeCells(row, 7, 1, 2)
                table.mergeCells(row, 9, 1, 2)
            table.mergeCells(row, 1, 2, 4)

        # Вывод итого
        withoutDisease = totalCount['all'] - (totalCount['with1Disease'] + totalCount['with2Disease'] + totalCount['with3Disease'])
        row = table.addRow()
        table.setText(row, 0, u'Итого', blockFormat=alignCenter, charFormat=charBold)
        table.setText(row, 1, totalCount['all'], blockFormat=alignRight)
        table.setText(row, 2, u'Без сопутствующих заболеваний', blockFormat=alignCenter, charFormat=charBold)
        table.setText(row, 3, withoutDisease, blockFormat=alignRight)
        if params['showPercentages']:
            table.setText(row, 4, percentRaito(totalCount['all'], withoutDisease), blockFormat=alignRight)
        else:
            table.mergeCells(row, 3, 1, 2)

        table.setText(row, 5, totalCount['with1Disease'], blockFormat=alignRight)
        table.setText(row, 7, totalCount['with2Disease'], blockFormat=alignRight)
        table.setText(row, 9, totalCount['with3Disease'], blockFormat=alignRight)
        if params['showPercentages']:
            table.setText(row, 6, percentRaito(totalCount['all'], totalCount['with1Disease']), blockFormat=alignRight)
            table.setText(row, 8, percentRaito(totalCount['all'], totalCount['with2Disease']), blockFormat=alignRight)
            table.setText(row,10, percentRaito(totalCount['all'], totalCount['with3Disease']), blockFormat=alignRight)
        else:
            table.mergeCells(row, 5, 1, 2)
            table.mergeCells(row, 7, 1, 2)
            table.mergeCells(row, 9, 1, 2)

        return doc


class CReportTreatedPatientsForComorbiditiesSetupDialog(QtGui.QDialog, Ui_ReportTreatedPatientsForComorbiditiesSetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

    def setTitle(self, title):
        self.setWindowTitle(title)

    def setParams(self, params):
        currentDate = QDate.currentDate()
        self.edtBegDate.setDate(params.get('begDate', QDate(currentDate.year(), 1, 1)))
        self.edtEndDate.setDate(params.get('endDate', currentDate))
        self.cmbOrgStructure.setValue(params.get('orgStructure', None))
        self.chkShowPercentages.setChecked(params.get('showPercentages', True))
        self.cmbBuildCond.setCurrentIndex(int(params.get('buildCond', 0)))

    def params(self):
        return {
            'begDate':         self.edtBegDate.date(),
            'endDate':         self.edtEndDate.date(),
            'orgStructure':    self.cmbOrgStructure.value(),
            'buildCond':       self.cmbBuildCond.currentIndex(),
            'showPercentages': self.chkShowPercentages.isChecked()
        }

