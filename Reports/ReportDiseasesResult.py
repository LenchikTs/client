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
from PyQt4.QtCore import QDate, QTime, QDateTime

from library.Utils        import forceString, forceInt
from Reports.Report       import CReport
from Reports.ReportBase   import CReportBase, createTable
from Reports.ReportView   import CPageFormat
from Reports.Utils        import dateRangeAsStr
from Orgs.Utils           import getOrganisationInfo, getOrgStructureName

from ReportTreatedPatientsForMajorDiseases import getMKBClassBlockName
from Reports.Ui_ReportDiseasesResultSetupDialog import Ui_ReportDiseasesResultSetupDialog


def selectData(params, orgStructureList):
    reportData = list()    # [ {code:str, name:str, ...} ]
    totalPatients = {'better':0, 'nochange':0, 'worse':0}

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
    tableDiagnosticResult = db.table('rbDiagnosticResult')
    tablePerson           = db.table('Person')
    tableAction           = db.table('Action')
    tableActionType       = db.table('ActionType')
    tableActionProperty   = db.table('ActionProperty')
    tableActionOrgStruct  = db.table('ActionProperty_OrgStructure')


    cols = [ tableMKB['ClassID'].alias('diagnosisCode'),
             tableMKB['ClassName'].alias('diagnosisName'),
             u"SUM(IF(rbDiagnosticResult.`name` LIKE '%лучш%', 1, 0)) AS `better`",
             u"SUM(IF(rbDiagnosticResult.`name` LIKE '%перем%', 1, 0)) AS `nochange`",
             u"SUM(IF(rbDiagnosticResult.`name` LIKE '%худш%', 1, 0)) AS `worse`",
           ]

    cond = [ tableEvent['deleted'].eq(0),
             tableEvent['isClosed'].eq(1),
             tableAction['deleted'].eq(0),
             tableEventType['deleted'].eq(0),
             tableEvent['execDate'].isNotNull(),
             tablePerson['org_id'].eq(QtGui.qApp.currentOrgId()),
             tableRbMedicalAidType['code'].eq(8),
             tableDiagnosisType['code'].eq(1),
             tableDiagnostic['deleted'].eq(0),
             tableDiagnosis['deleted'].eq(0),
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
        cond.append(tableActionOrgStruct['value'].inlist(orgStructureList))

    queryTable = tableEvent
    queryTable = queryTable.innerJoin(tablePerson, tablePerson['id'].eq(tableEvent['execPerson_id']))
    queryTable = queryTable.innerJoin(tableEventType, tableEventType['id'].eq(tableEvent['eventType_id']))
    queryTable = queryTable.innerJoin(tableRbMedicalAidType, tableRbMedicalAidType['id'].eq(tableEventType['medicalAidType_id']))
    queryTable = queryTable.innerJoin(tableAction, tableAction['event_id'].eq(tableEvent['id']))
    queryTable = queryTable.innerJoin(tableActionType, tableAction['actionType_id'].eq(tableActionType['id']))
    queryTable = queryTable.innerJoin(tableActionProperty, tableAction['id'].eq(tableActionProperty['action_id']))
    queryTable = queryTable.innerJoin(tableActionOrgStruct, tableActionProperty['id'].eq(tableActionOrgStruct['id']))
    queryTable = queryTable.innerJoin(tableDiagnostic, tableDiagnostic['event_id'].eq(tableEvent['id']))
    queryTable = queryTable.innerJoin(tableDiagnosisType, tableDiagnostic['diagnosisType_id'].eq(tableDiagnosisType['id']))
    queryTable = queryTable.innerJoin(tableDiagnosticResult, tableDiagnostic['result_id'].eq(tableDiagnosticResult['id']))
    queryTable = queryTable.innerJoin(tableDiagnosis, tableDiagnostic['diagnosis_id'].eq(tableDiagnosis['id']))
    queryTable = queryTable.innerJoin(tableMKB, tableMKB['DiagID'].eq(tableDiagnosis['MKB']))

    stmt = db.selectStmtGroupBy(queryTable, cols, where=cond, group=tableMKB['ClassID'].name())
    query = db.query(stmt)
    while query.next():
        record = query.record()
        better = forceInt(record.value('better'))
        nochange = forceInt(record.value('nochange'))
        worse = forceInt(record.value('worse'))

        totalPatients['better'] += better
        totalPatients['nochange'] += nochange
        totalPatients['worse'] += worse
        reportData.append({
                'code':     getMKBClassBlockName(forceString(record.value('diagnosisCode'))),
                'name':     forceString(record.value('diagnosisName')),
                'better':   better,
                'nochange': nochange,
                'worse':    worse
            })


    return reportData, totalPatients



class CReportDiseasesResult(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Отчет об исходе заболеваний')


    def getSetupDialog(self, parent):
        result = CReportDiseasesResultSetupDialog(parent)
        result.setTitle(self.title())
        self.reportDiseasesResultSetupDialog = result
        return result

    def getCurrentOrgStructureIdList(self):
        cmbOrgStruct = self.reportDiseasesResultSetupDialog.cmbOrgStructure
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
        cursor.insertText(u'\nОтчет об исходе заболеваний в разрезе групп диагнозов у пролеченных больных\n')
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertText(dateRangeAsStr(u'за период', params['begDate'], params['endDate']) + '\n')
        if not params['orgStructure']:
            cursor.insertText(u'все отделения')
        else:
            cursor.insertText(getOrgStructureName(params['orgStructure']))
        cursor.insertBlock()

        alignLeft = CReportBase.AlignLeft
        alignRight = CReportBase.AlignRight
        alignCenter = CReportBase.AlignCenter
        charBold = QtGui.QTextCharFormat()
        charBold.setFontWeight(QtGui.QFont.Bold)


        # Вычисление процента 'piece' от 'value' с точностью до 0,01 и запятой в качестве разделителя
        def percentRaito(value, piece):
            if params['showPercentages'] == True:
                if value == 0:
                    return '100%'
                elif piece == 0:
                    return '0%'
                else:
                    return ("%g%%" % round(piece / float(value) * 100, 2)).replace('.', ',', 1)
            else:
                return str()


        colTitle = u'% больных' if params['showPercentages'] else str()
        tableColumns = [ ('12%', [u'Код', '',], alignLeft),
                         ('16%', [u'Класс, диагноз', ''], alignLeft),
                         ('12%', [u'Улучшение', u'больных'], alignLeft),
                         ('12%', ['', colTitle], alignLeft),
                         ('12%', [u'Без изменений', u'больных'], alignLeft),
                         ('12%', ['', colTitle], alignLeft),
                         ('12%', [u'Ухудшение', u'больных'], alignLeft),
                         ('12%', ['', colTitle], alignLeft)
                       ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 1, 2)
        table.mergeCells(0, 4, 1, 2)
        table.mergeCells(0, 6, 1, 2)

        if not params['showPercentages']:
            table.mergeCells(1, 2, 1, 2)
            table.mergeCells(1, 4, 1, 2)
            table.mergeCells(1, 6, 1, 2)

        reportData, totalPatients = selectData(params, orgStructureList=self.getCurrentOrgStructureIdList())
        allPatients = totalPatients['better'] + totalPatients['nochange'] + totalPatients['worse']

        for item in reportData:
            row = table.addRow();
            table.setText(row, 0, item['code'])
            table.setText(row, 1, item['name'])
            table.setText(row, 2, item['better'], blockFormat=alignRight)
            table.setText(row, 3, percentRaito(allPatients, item['better']), blockFormat=alignRight)
            table.setText(row, 4, item['nochange'], blockFormat=alignRight)
            table.setText(row, 5, percentRaito(allPatients, item['nochange']), blockFormat=alignRight)
            table.setText(row, 6, item['worse'], blockFormat=alignRight)
            table.setText(row, 7, percentRaito(allPatients, item['worse']), blockFormat=alignRight)
            if not params['showPercentages']:
                table.mergeCells(row, 2, 1, 2)
                table.mergeCells(row, 4, 1, 2)
                table.mergeCells(row, 6, 1, 2)

        row = table.addRow()
        table.setText(row, 0, u'Итого', charFormat=charBold)
        table.setText(row, 1, allPatients, blockFormat=alignCenter, charFormat=charBold)
        table.setText(row, 2, totalPatients['better'], blockFormat=alignRight, charFormat=charBold)
        table.setText(row, 3, percentRaito(allPatients, totalPatients['better']), blockFormat=alignRight, charFormat=charBold)
        table.setText(row, 4, totalPatients['nochange'], blockFormat=alignRight, charFormat=charBold)
        table.setText(row, 5, percentRaito(allPatients, totalPatients['nochange']), blockFormat=alignRight, charFormat=charBold)
        table.setText(row, 6, totalPatients['worse'], blockFormat=alignRight, charFormat=charBold)
        table.setText(row, 7, percentRaito(allPatients, totalPatients['worse']), blockFormat=alignRight, charFormat=charBold)
        if not params['showPercentages']:
            table.mergeCells(row, 2, 1, 2)
            table.mergeCells(row, 4, 1, 2)
            table.mergeCells(row, 6, 1, 2)


        return doc


class CReportDiseasesResultSetupDialog(QtGui.QDialog, Ui_ReportDiseasesResultSetupDialog):
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

    def params(self):
        return {
            'begDate':              self.edtBegDate.date(),
            'endDate':              self.edtEndDate.date(),
            'orgStructure':         self.cmbOrgStructure.value(),
            'showPercentages':      self.chkShowPercentages.isChecked()
        }

