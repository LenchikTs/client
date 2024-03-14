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

from library.Utils        import forceString, forceInt, forceDate
from Reports.Report       import CReport
from Reports.ReportBase   import CReportBase, createTable
from Reports.ReportView   import CPageFormat
from Reports.Utils        import dateRangeAsStr
from Orgs.Utils           import getOrganisationInfo, getOrgStructureName

from Reports.Ui_ReportTreatedPatientsForComorbiditiesSetupDialog import Ui_ReportTreatedPatientsForComorbiditiesSetupDialog

# Получить название блока для класса МКБ
def getMKBClassBlockName(MKBClassName):
    if MKBClassName == 'I':     return '(A00-B99)'
    if MKBClassName == 'II':    return '(C00-D48)'
    if MKBClassName == 'III':   return '(D50-D89)'
    if MKBClassName == 'IV':    return '(E00-E90)'
    if MKBClassName == 'V':     return '(F00-F99)'
    if MKBClassName == 'VI':    return '(G00-G99)'
    if MKBClassName == 'VII':   return '(H00-H59)'
    if MKBClassName == 'VIII':  return '(H60-H95)'
    if MKBClassName == 'IX':    return '(I00-I99)'
    if MKBClassName == 'X':     return '(J00-J99)'
    if MKBClassName == 'XI':    return '(K00-K93)'
    if MKBClassName == 'XII':   return '(L00-L99)'
    if MKBClassName == 'XIII':  return '(M00-M99)'
    if MKBClassName == 'XIV':   return '(N00-N99)'
    if MKBClassName == 'XV':    return '(O00-O99)'
    if MKBClassName == 'XVI':   return '(P00-P96)'
    if MKBClassName == 'XVII':  return '(Q00-Q99)'
    if MKBClassName == 'XVIII': return '(R00-R99)'
    if MKBClassName == 'XIX':   return '(S00-T98)'
    if MKBClassName == 'XX':    return '(V01-Y98)'
    if MKBClassName == 'XXI':   return '(Z00-Z99)'

BUILD_BY_DISEASES_CLASSES = 0
BUILD_BY_DISEASES_GROUPS = 1
BUILD_BY_DISEASES = 2

def selectData(params, orgStructureList):
    reportData = list()    # [ {code:str, name:str, ...} ]
    totalRelative = 0

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
    tableClient           = db.table('Client')
    tableAction           = db.table('Action')
    tableActionType       = db.table('ActionType')
    tableActionProperty   = db.table('ActionProperty')
    tableActionOrgStruct  = db.table('ActionProperty_OrgStructure')

    cols = None
    if params['buildCond'] == BUILD_BY_DISEASES:
        cols = [ tableMKB['DiagID'].alias('diagnosisCode'), tableMKB['DiagName'].alias('diagnosisName') ]

    elif params['buildCond'] == BUILD_BY_DISEASES_GROUPS:
        cols = [ 'LEFT(MKB.`DiagID`, 3) AS `diagnosisCode`', '(SELECT `DiagName` FROM MKB WHERE `DiagID` = `diagnosisCode`) AS `diagnosisName`' ]

    else:  # BUILD_BY_DISEASES_CLASSES
        cols = [ tableMKB['ClassID'].alias('diagnosisCode'), tableMKB['ClassName'].alias('diagnosisName') ]

    cols.append(tableEvent['setDate'].alias('eventSetDate'))
    cols.append(tableEvent['client_id'].alias('clientId'))
    cols.append('(DATEDIFF(Event.`execDate`, Event.`setDate`)+1) AS `bedDays`')

    cond = [ tableEvent['deleted'].eq(0),
             tableEvent['isClosed'].eq(1),
             tableEventType['deleted'].eq(0),
             tablePerson['org_id'].eq(QtGui.qApp.currentOrgId()),
             tableRbMedicalAidType['code'].eq(8),
             tableDiagnosisType['code'].eq(1),
             tableDiagnostic['deleted'].eq(0),
             tableDiagnosis['deleted'].eq(0),
             tableEventType['form'].eq('072'),
             tableActionType['flatCode'].eq('leaved'),
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
    queryTable = queryTable.innerJoin(tableDiagnostic, tableDiagnostic['event_id'].eq(tableEvent['id']))
    queryTable = queryTable.innerJoin(tableDiagnosis, tableDiagnostic['diagnosis_id'].eq(tableDiagnosis['id']))
    queryTable = queryTable.innerJoin(tableDiagnosisType, tableDiagnostic['diagnosisType_id'].eq(tableDiagnosisType['id']))
    queryTable = queryTable.innerJoin(tableMKB, tableMKB['DiagID'].eq(tableDiagnosis['MKB']))
    queryTable = queryTable.innerJoin(tableAction, tableAction['event_id'].eq(tableEvent['id']))
    queryTable = queryTable.innerJoin(tableActionType, tableAction['actionType_id'].eq(tableActionType['id']))
    queryTable = queryTable.innerJoin(tableActionProperty, tableActionProperty['action_id'].eq(tableAction['id']))
    queryTable = queryTable.innerJoin(tableActionOrgStruct, tableActionProperty['id'].eq(tableActionOrgStruct['id']))


    stmt = db.selectStmtGroupBy(queryTable, cols, cond, group=tableEvent['id'].name())
    ageCall = 'age(Client.`birthDate`, nested.`eventSetDate`)'
    stmt = '''
        SELECT
            nested.`diagnosisName`,
            nested.`diagnosisCode`,
            SUM(IF({0} <= 3, 1, 0)) AS `patientsBefore3`,
            SUM(IF({0} BETWEEN 4 AND 6, 1, 0)) AS `patientsFrom4To6`,
            SUM(IF({0} BETWEEN 7 AND 10, 1, 0)) AS `patientsFrom7To10`,
            SUM(IF({0} >= 11, 1, 0)) AS `patientsFrom11To17`,
            SUM(IF({0} >= 15, 1, 0)) AS `patientsFrom15To17`,
            SUM(IF({0} <= 3, nested.`bedDays`, 0)) AS `bedDaysBefore3`,
            SUM(IF({0} BETWEEN 4 AND 6, nested.`bedDays`, 0)) AS `bedDaysFrom4To6`,
            SUM(IF({0} BETWEEN 7 AND 10, nested.`bedDays`, 0)) AS `bedDaysFrom7To10`,
            SUM(IF({0} >= 11, nested.`bedDays`, 0)) AS `bedDaysFrom11To17`,
            SUM(IF({0} >= 15, nested.`bedDays`, 0)) AS `bedDaysFrom15To17`
        FROM
            ({1}) AS `nested` JOIN Client ON Client.`id` = nested.`clientId`
        GROUP BY
            nested.`diagnosisCode`, nested.`diagnosisName`
    '''.format(ageCall, stmt)

    query = db.query(stmt)
    while query.next():
        record = query.record()
        diagnosisCode     = forceString(record.value('diagnosisCode'))
        diagnosisName     = forceString(record.value('diagnosisName'))

        patientsBefore3        = forceInt(record.value('patientsBefore3'))
        patientsFrom4To6       = forceInt(record.value('patientsFrom4To6'))
        patientsFrom7To10      = forceInt(record.value('patientsFrom7To10'))
        patientsFrom11To17     = forceInt(record.value('patientsFrom11To17'))
        patientsFrom15To17     = forceInt(record.value('patientsFrom15To17'))

        bedDaysBefore3    = forceInt(record.value('bedDaysBefore3'))
        bedDaysFrom4To6   = forceInt(record.value('bedDaysFrom4To6'))
        bedDaysFrom7To10  = forceInt(record.value('bedDaysFrom7To10'))
        bedDaysFrom11To17 = forceInt(record.value('bedDaysFrom11To17'))
        bedDaysFrom15To17 = forceInt(record.value('bedDaysFrom15To17'))

        if params['buildCond'] == BUILD_BY_DISEASES_CLASSES:
            diagnosisCode = getMKBClassBlockName(diagnosisCode)
        reportData.append({
                'code':          diagnosisCode,
                'name':          diagnosisName,
                'patients0-3':   patientsBefore3,
                'patients4-6':   patientsFrom4To6,
                'patients7-10':  patientsFrom7To10,
                'patients11-17': patientsFrom11To17,
                'patients15-17': patientsFrom15To17,
                'bedDays0-3':    bedDaysBefore3,
                'bedDays4-6':    bedDaysFrom4To6,
                'bedDays7-10':   bedDaysFrom7To10,
                'bedDays11-17':  bedDaysFrom11To17,
                'bedDays15-17':  bedDaysFrom15To17
            })

    queryTable = queryTable.innerJoin(tableClient, tableEvent['relative_id'].eq(tableClient['id']))
    cols = [ tableClient['id'].name(),
             tableEvent['setDate'].name(),
             tableEvent['execDate'].name(),
           ]
    stmt = db.selectStmt(queryTable, cols, cond, order=cols)
    query = db.query(stmt)
    lastSetDate, lastExecDate, lastRelativeId = None, None, None
    while query.next():
        record = query.record()
        relativeId = forceInt(record.value('id'))
        setDate = forceDate(record.value('setDate'))
        execDate = forceDate(record.value('execDate'))

        # Сопровождающий для нескольких пациентов может быть назначен либо в один день с разными датами выписки,
        # либо назначен в разные дни и выписан в один день.
        if lastExecDate is None and lastSetDate is None:
            totalRelative += 1
        else:
            if lastExecDate == execDate and lastRelativeId == relativeId:
                pass
            elif lastSetDate == setDate and lastRelativeId == relativeId:
                pass
            else:
                totalRelative += 1
        lastExecDate, lastSetDate, lastRelativeId = execDate, setDate, relativeId

    return reportData, totalRelative



class CReportTreatedPatientsForMajorDiseases(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Отчет о пролеченных больных по основным заболеваниям')
        self.orientation = CPageFormat.Landscape


    def getSetupDialog(self, parent):
        result = CReportTreatedPatientsForMajorDiseasesSetupDialog(parent)
        result.setTitle(self.title())
        self.reportTreatedPatientsForMajorDiseasesSetupDialog = result
        return result

    def getCurrentOrgStructureIdList(self):
        cmbOrgStruct = self.reportTreatedPatientsForMajorDiseasesSetupDialog.cmbOrgStructure
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
        cursor.insertText(u'\nОтчет о пролеченных больных\n')
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertText(dateRangeAsStr(u'за период', params['begDate'], params['endDate']))
        if not params['orgStructure']:
            cursor.insertText(u'\n(по основному заболеванию) все отделения\n')
        else:
            cursor.insertText(u'\n(по основному заболеванию) %s\n' % getOrgStructureName(params['orgStructure']))
        cursor.insertBlock()

        alignLeft = CReportBase.AlignLeft
        alignRight = CReportBase.AlignRight
        charBold = QtGui.QTextCharFormat()
        charBold.setFontWeight(QtGui.QFont.Bold)


        # Вычисление процента 'piece' от 'value' с точностью до 0,1 и запятой в качестве разделителя
        def percentRaito(value, piece):
            if params['showPercentages'] == True:
                if value == 0:
                    return '100%'
                elif piece == 0:
                    return '0%'
                else:
                    return ("%g%%" % round(piece / float(value) * 100, 1)).replace('.', ',', 1)
            else:
                return str()


        colTitle = u'% больных' if params['showPercentages'] else ''
        tableColumns = [ ('4%',  [u'Дети', u'Код', '', '', ''], alignLeft),
                         ('12%', ['', u'Класс, диагноз', '', '', ''], alignLeft),
                         ('4%',  ['', u'Всего', '', '', u'больных'], alignLeft),
                         ('4%',  ['', '', '', '', u'койко-дней'], alignLeft),
                         ('4%',  ['', '', '', '', colTitle], alignLeft),
                         ('4%',  ['', u'В том числе', u'до 3 лет', '', u'больных'], alignLeft),
                         ('4%',  ['', '', '', '', u'койко-дней'], alignLeft),
                         ('4%',  ['', '', '', '', colTitle], alignLeft),
                         ('4%',  ['', '', u'4-17 лет', '', u'больных'], alignLeft),
                         ('4%',  ['', '', '', '', u'койко-дней'], alignLeft),
                         ('4%',  ['', '', '', '', colTitle], alignLeft),
                         ('4%',  ['', '', u'В том числе', u'4-6 лет', u'больных'], alignLeft),
                         ('4%',  ['', '', '', '', u'койко-дней'], alignLeft),
                         ('4%',  ['', '', '', '', colTitle], alignLeft),
                         ('4%',  ['', '', '', u'7-10 лет', u'больных'], alignLeft),
                         ('4%',  ['', '', '', '', u'койко-дней'], alignLeft),
                         ('4%',  ['', '', '', '', colTitle], alignLeft),
                         ('4%',  ['', '', '', u'11-17 лет', u'больных'], alignLeft),
                         ('4%',  ['', '', '', '', u'койко-дней'], alignLeft),
                         ('4%',  ['', '', '', '', colTitle], alignLeft),
                         ('4%',  ['', '', u'Подростки', '', u'больных'], alignLeft),
                         ('4%',  ['', '', '', '', u'койко-дней'], alignLeft),
                         ('4%',  ['', '', '', '', colTitle], alignLeft)
                       ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 1, 23)
        table.mergeCells(1, 0, 4, 1)
        table.mergeCells(1, 1, 4, 1)
        table.mergeCells(1, 2, 3, 3)
        table.mergeCells(1, 5, 1, 18)
        table.mergeCells(2, 5, 2, 3)
        table.mergeCells(2, 8, 2, 3)
        table.mergeCells(2, 11, 1, 9)
        table.mergeCells(3, 11, 1, 3)
        table.mergeCells(3, 14, 1, 3)
        table.mergeCells(3, 17, 1, 3)
        table.mergeCells(2, 20, 2, 3)

        if not params['showPercentages']:
            for i in xrange(1, 8):
                table.mergeCells(4, 3*i, 1, 2)

        reportData, totalRelative = selectData(params, orgStructureList=self.getCurrentOrgStructureIdList())
        totalPatients = sum(item['patients0-3'] + item['patients4-6'] + item['patients7-10'] + item['patients11-17'] for item in reportData)

        # Заполение таблицы и горизонтальная сумма
        for item in reportData:
            patientsWithConcreteDisease = item['patients0-3'] + item['patients4-6'] + item['patients7-10'] + item['patients11-17']

            row = table.addRow()
            table.setText(row, 0, item['code'])
            table.setText(row, 1, item['name'])
            table.setText(row, 2, patientsWithConcreteDisease, blockFormat=alignRight)
            table.setText(row, 3, item ['bedDays0-3'] + item['bedDays4-6'] + item['bedDays7-10'] + item['bedDays11-17'], blockFormat=alignRight)
            table.setText(row, 4, percentRaito(totalPatients, patientsWithConcreteDisease), blockFormat=alignRight)

            table.setText(row, 5, item['patients0-3'], blockFormat=alignRight)
            table.setText(row, 6, item['bedDays0-3'], blockFormat=alignRight)
            table.setText(row, 7, percentRaito(patientsWithConcreteDisease, item['patients0-3']), blockFormat=alignRight)

            patientsFrom4To17 = patientsWithConcreteDisease - item['patients0-3']
            table.setText(row, 8, patientsFrom4To17, blockFormat=alignRight)
            table.setText(row, 9, item['bedDays4-6'] + item['bedDays7-10'] + item['bedDays11-17'], blockFormat=alignRight)
            table.setText(row, 10, percentRaito(patientsWithConcreteDisease, patientsFrom4To17), blockFormat=alignRight)

            table.setText(row, 11, item['patients4-6'], blockFormat=alignRight)
            table.setText(row, 12, item['bedDays4-6'], blockFormat=alignRight)
            table.setText(row, 13, percentRaito(patientsFrom4To17, item['patients4-6']), blockFormat=alignRight)

            table.setText(row, 14, item['patients7-10'], blockFormat=alignRight)
            table.setText(row, 15, item['bedDays7-10'], blockFormat=alignRight)
            table.setText(row, 16, percentRaito(patientsFrom4To17, item['patients7-10']), blockFormat=alignRight)

            table.setText(row, 17, item['patients11-17'], blockFormat=alignRight)
            table.setText(row, 18, item['bedDays11-17'], blockFormat=alignRight)
            table.setText(row, 19, percentRaito(patientsFrom4To17, item['patients11-17']), blockFormat=alignRight)

            table.setText(row, 20, item['patients15-17'], blockFormat=alignRight)
            table.setText(row, 21, item['bedDays15-17'], blockFormat=alignRight)
            table.setText(row, 22, percentRaito(patientsFrom4To17, item['patients15-17']), blockFormat=alignRight)

            if not params['showPercentages']:
                for i in xrange(1, 8):
                    table.mergeCells(row, 3*i, 1, 2)


        # Подсчет и вывод итого (вертикальная сумма)
        totalPatientsWithAge = {'0-3':0, '4-6':0, '7-10':0, '11-17':0, '15-17':0}
        totalBedDaysWithAge  = {'0-3':0, '4-6':0, '7-10':0, '11-17':0, '15-17':0}
        for item in reportData:
            totalPatientsWithAge['0-3']   += item['patients0-3']
            totalPatientsWithAge['4-6']   += item['patients4-6']
            totalPatientsWithAge['7-10']  += item['patients7-10']
            totalPatientsWithAge['11-17'] += item['patients11-17']
            totalPatientsWithAge['15-17'] += item['patients15-17']
            totalBedDaysWithAge['0-3']    += item['bedDays0-3']
            totalBedDaysWithAge['4-6']    += item['bedDays4-6']
            totalBedDaysWithAge['7-10']   += item['bedDays7-10']
            totalBedDaysWithAge['11-17']  += item['bedDays11-17']
            totalBedDaysWithAge['15-17']  += item['bedDays15-17']
        totalBedDays = totalBedDaysWithAge['0-3'] + totalBedDaysWithAge['4-6'] + totalBedDaysWithAge['7-10'] + totalBedDaysWithAge['11-17']
        totalPatientsWithAge['4-17'] = totalPatientsWithAge['4-6'] + totalPatientsWithAge['7-10'] + totalPatientsWithAge['11-17']
        totalBedDaysWithAge['4-17'] = totalBedDaysWithAge['4-6'] + totalBedDaysWithAge['7-10'] + totalBedDaysWithAge['11-17']

        row = table.addRow()
        table.setText(row, 1, u'Итого', charFormat=charBold)

        table.setText(row, 2, totalPatients, blockFormat=alignRight, charFormat=charBold)
        table.setText(row, 3, totalBedDays, blockFormat=alignRight, charFormat=charBold)
        table.setText(row, 4, '100%' if params['showPercentages'] else str(), blockFormat=alignRight, charFormat=charBold)

        table.setText(row, 5, totalPatientsWithAge['0-3'], blockFormat=alignRight, charFormat=charBold)
        table.setText(row, 6, totalBedDaysWithAge['0-3'], blockFormat=alignRight, charFormat=charBold)
        table.setText(row, 7, percentRaito(totalPatients, totalPatientsWithAge['0-3']), blockFormat=alignRight, charFormat=charBold)

        table.setText(row, 8, totalPatientsWithAge['4-17'], blockFormat=alignRight, charFormat=charBold)
        table.setText(row, 9, totalBedDaysWithAge['4-17'], blockFormat=alignRight, charFormat=charBold)
        table.setText(row, 10, percentRaito(totalPatients, totalPatientsWithAge['4-17']), blockFormat=alignRight, charFormat=charBold)

        table.setText(row, 11, totalPatientsWithAge['4-6'], blockFormat=alignRight, charFormat=charBold)
        table.setText(row, 12, totalBedDaysWithAge['4-6'], blockFormat=alignRight, charFormat=charBold)
        table.setText(row, 13, percentRaito(totalPatients, totalPatientsWithAge['4-6']), blockFormat=alignRight, charFormat=charBold)

        table.setText(row, 14, totalPatientsWithAge['7-10'], blockFormat=alignRight, charFormat=charBold)
        table.setText(row, 15, totalBedDaysWithAge['7-10'], blockFormat=alignRight, charFormat=charBold)
        table.setText(row, 16, percentRaito(totalPatients, totalPatientsWithAge['7-10']), blockFormat=alignRight, charFormat=charBold)

        table.setText(row, 17, totalPatientsWithAge['11-17'], blockFormat=alignRight, charFormat=charBold)
        table.setText(row, 18, totalBedDaysWithAge['11-17'], blockFormat=alignRight, charFormat=charBold)
        table.setText(row, 19, percentRaito(totalPatients, totalPatientsWithAge['11-17']), blockFormat=alignRight, charFormat=charBold)

        table.setText(row, 20, totalPatientsWithAge['15-17'], blockFormat=alignRight, charFormat=charBold)
        table.setText(row, 21, totalBedDaysWithAge['15-17'], blockFormat=alignRight, charFormat=charBold)
        table.setText(row, 22, percentRaito(totalPatients, totalPatientsWithAge['15-17']), blockFormat=alignRight, charFormat=charBold)

        if not params['showPercentages']:
            for i in xrange(1, 8):
                table.mergeCells(row, 3*i, 1, 2)



        row = table.addRow()
        table.mergeCells(row, 0, 1, 2)
        table.setText(row, 0, u'Выписано сопровождающих', charFormat=charBold)
        table.setText(row, 2, totalRelative, blockFormat=alignLeft, charFormat=charBold)
        table.mergeCells(row, 2, 1, 21)

        return doc


class CReportTreatedPatientsForMajorDiseasesSetupDialog(QtGui.QDialog, Ui_ReportTreatedPatientsForComorbiditiesSetupDialog):
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

