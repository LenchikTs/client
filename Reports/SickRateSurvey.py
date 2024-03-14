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
from PyQt4.QtCore import pyqtSignature, QDate

from library.database   import addDateInRange
from library.ICDUtils   import MKBwithoutSubclassification
from library.Utils      import forceBool, forceInt, forceString

from Reports.Report     import CReport
from Reports.ReportView import CPageFormat
from Reports.ReportBase import CReportBase, createTable
from Reports.ReportPersonSickList import addAddressCond, addAttachCond
from Orgs.Utils         import getOrgStructureDescendants, getOrgStructureAddressIdList
from Reports.ReportAcuteInfections import CReportAcuteInfectionsSetupDialog
from Reports.SpecialityListDialog import CSpecialityListDialog, formatSpecialityIdList


def selectData(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeId, orgStructureId, personId, specialityList, sex, ageFrom, ageTo, socStatusClassId, socStatusTypeId, accountAccomp, locality, isFilterAddressOrgStructure, addrType, addressOrgStructureId, params, countClientId = False):
# затея подсчитывать clientCount таким образом неверна.
# т.к. противоречит группировкам отличным от главной.
# но пока забъём
#    stmt="""
#SELECT
#   Diagnosis.MKB AS MKB,
#   COUNT(*) AS sickCount,
#   COUNT(DISTINCT Diagnosis.client_id) AS clientCount,
#   rbDiseaseCharacter.code AS diseaseCharacter,
#   (%s) AS firstInPeriod
#FROM Diagnosis
#LEFT JOIN Client ON Client.id = Diagnosis.client_id
#LEFT JOIN rbDiagnosisType    ON rbDiagnosisType.id = Diagnosis.diagnosisType_id
#LEFT JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnosis.character_id%s
#WHERE Diagnosis.deleted=0 AND Diagnosis.mod_id IS NULL AND %s
#GROUP BY MKB, diseaseCharacter, firstInPeriod
#    """
    db = QtGui.qApp.db
    tableDiagnosis  = db.table('Diagnosis')
    tableDiseaseCharacter = db.table('rbDiseaseCharacter')
    tableDiagnosisType = db.table('rbDiagnosisType')
    tableClient = db.table('Client')
    tableDiagnostic = db.table('Diagnostic')
    tablePerson = db.table('Person')
    tableClientAddress = db.table('ClientAddress')
    tableAddress = db.table('Address')
    tableAddressHouse = db.table('AddressHouse')

    MKBFilter = params.get('MKBFilter', 0)
    MKBFrom   = params.get('MKBFrom', '')
    MKBTo     = params.get('MKBTo', '')
    phaseId   = params.get('phaseId', None)
    MKBExFilter = params.get('MKBExFilter', 0)
    MKBExFrom   = params.get('MKBExFrom', '')
    MKBExTo     = params.get('MKBExTo', '')
    phaseIdEx   = params.get('phaseIdEx', None)

    queryTable = tableDiagnosis.leftJoin(tableClient, tableDiagnosis['client_id'].eq(tableClient['id']))
    queryTable = queryTable.leftJoin(tableDiagnosisType, tableDiagnosis['diagnosisType_id'].eq(tableDiagnosisType['id']))
    queryTable = queryTable.leftJoin(tableDiseaseCharacter, tableDiagnosis['character_id'].eq(tableDiseaseCharacter['id']))
    cond = []
#    cond.append(tableDiagnosis['MKB'].lt('Z'))
    #cond.append(db.joinOr([tableDiagnosis['setDate'].isNull(), db.joinAnd([tableDiagnosis['setDate'].le(endDate), tableDiagnosis['setDate'].ge(begDate)])]))
    #cond.append(db.joinOr([tableDiagnosis['endDate'].ge(begDate), tableDiseaseCharacter['code'].eq('3')]))

    diagnosticQuery = tableDiagnostic
    diagnosticCond = [ tableDiagnostic['diagnosis_id'].eq(tableDiagnosis['id']),
                       tableDiagnostic['deleted'].eq(0)
                     ]
    if registeredInPeriod:
        addDateInRange(diagnosticCond, tableDiagnostic['setDate'], begDate, endDate)
    isPersonPost = params.get('isPersonPost', 0)
    if isPersonPost:
        tableRBPost = db.table('rbPost')
        diagnosticQuery = diagnosticQuery.innerJoin(tablePerson, tablePerson['id'].eq(tableDiagnostic['person_id']))
        diagnosticQuery = diagnosticQuery.innerJoin(tableRBPost, tableRBPost['id'].eq(tablePerson['post_id']))
        diagnosticCond.append(tablePerson['deleted'].eq(0))
        if isPersonPost == 1:
            diagnosticCond.append('''LEFT(rbPost.code, 1) IN ('1','2','3') ''')
        elif isPersonPost == 2:
            diagnosticCond.append('''LEFT(rbPost.code, 1) IN ('4','5','6','7','8','9')''')
    if personId:
        diagnosticCond.append(tableDiagnostic['person_id'].eq(personId))
    elif orgStructureId:
        if not isPersonPost:
            diagnosticQuery = diagnosticQuery.leftJoin(tablePerson, tablePerson['id'].eq(tableDiagnostic['person_id']))
        diagnosticCond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureDescendants(orgStructureId)))
    else:
        if not isPersonPost:
            diagnosticQuery = diagnosticQuery.leftJoin(tablePerson, tablePerson['id'].eq(tableDiagnostic['person_id']))
        diagnosticCond.append(tablePerson['org_id'].eq(QtGui.qApp.currentOrgId()))
    if specialityList:
        diagnosticCond.append(tablePerson['speciality_id'].inlist(specialityList))
    if eventTypeId:
        tableEvent = db.table('Event')
        diagnosticQuery = diagnosticQuery.leftJoin(tableEvent, tableEvent['id'].eq(tableDiagnostic['event_id']))
        diagnosticCond.append(tableEvent['eventType_id'].eq(eventTypeId))
    elif eventPurposeId:
        tableEvent = db.table('Event')
        tableEventType = db.table('EventType')
        diagnosticQuery = diagnosticQuery.leftJoin(tableEvent, tableEvent['id'].eq(tableDiagnostic['event_id']))
        diagnosticQuery = diagnosticQuery.leftJoin(tableEventType, tableEventType['id'].eq(tableEvent['eventType_id']))
        diagnosticCond.append(tableEventType['purpose_id'].eq(eventPurposeId))
    cond.append(db.existsStmt(diagnosticQuery, diagnosticCond))
    if sex:
        cond.append(tableClient['sex'].eq(sex))
    if ageFrom <= ageTo:
        cond.append('Diagnosis.endDate >= ADDDATE(Client.birthDate, INTERVAL %d YEAR)'%ageFrom)
        cond.append('Diagnosis.endDate < SUBDATE(ADDDATE(Client.birthDate, INTERVAL %d YEAR),1)'%(ageTo+1))
    if socStatusTypeId:
        subStmt = ('SELECT ClientSocStatus.id FROM ClientSocStatus WHERE '
                  +'ClientSocStatus.deleted=0 AND ClientSocStatus.client_id=Client.id AND '
                  +'ClientSocStatus.socStatusType_id=%d' % socStatusTypeId)
        cond.append('EXISTS('+subStmt+')')
    elif socStatusClassId:
        subStmt = ('SELECT ClientSocStatus.id FROM ClientSocStatus WHERE '
                  +'ClientSocStatus.deleted=0 AND ClientSocStatus.client_id=Client.id AND '
                  +'ClientSocStatus.socStatusClass_id=%d' % socStatusClassId)
        cond.append('EXISTS('+subStmt+')')
    if MKBFilter == 1:
        cond.append(tableDiagnosis['MKB'].ge(MKBFrom))
        cond.append(tableDiagnosis['MKB'].le(MKBTo))
        if phaseId:
            phaseCond = [tableDiagnostic['diagnosis_id'].eq(tableDiagnosis['id']),
                         tableDiagnostic['deleted'].eq(0),
                         tableDiagnostic['phase_id'].eq(phaseId)]
            cond.append(db.existsStmt(tableDiagnostic, phaseCond))
    else:
        cond.append(tableDiagnosis['MKB'].lt('Z'))
    if MKBExFilter == 1:
        cond.append(tableDiagnosis['MKBEx'].ge(MKBExFrom))
        cond.append(tableDiagnosis['MKBEx'].le(MKBExTo))
        if phaseIdEx:
            phaseCondEx = [tableDiagnostic['diagnosis_id'].eq(tableDiagnosis['id']),
                           tableDiagnostic['deleted'].eq(0),
                           tableDiagnostic['phase_id'].eq(phaseIdEx)]
            cond.append(db.existsStmt(tableDiagnostic, phaseCondEx))
    if not accountAccomp:
        cond.append(tableDiagnosisType['code'].inlist(['1', '2', '4']))
    if locality:
        # 1: горожане, isClientVillager == 0 или NULL
        # 2: сельские жители, isClientVillager == 1
        cond.append('IFNULL(isClientVillager(Client.id), 0) = %d' % (locality-1))
    filterAddress = params.get('isFilterAddress', False)
    if filterAddress:
        filterAddressType = params.get('filterAddressType', 0)
        filterAddressCity = params.get('filterAddressCity', None)
        filterAddressStreet = params.get('filterAddressStreet', None)
        filterAddressHouse = params.get('filterAddressHouse', u'')
        filterAddressCorpus = params.get('filterAddressCorpus', u'')
        filterAddressFlat = params.get('filterAddressFlat', u'')
        queryTable = queryTable.leftJoin(tableClientAddress, tableClientAddress['id'].eqEx(u'getClientLocAddressId(Client.id)' if filterAddressType else u'getClientRegAddressId(Client.id)'))
        cond.append(tableClientAddress['type'].eq(filterAddressType))
        cond.append(db.joinOr([tableClientAddress['id'].isNull(), tableClientAddress['deleted'].eq(0)]))
        if filterAddressCity or filterAddressStreet or filterAddressHouse or filterAddressCorpus or filterAddressFlat:
            queryTable = queryTable.leftJoin(tableAddress, tableClientAddress['address_id'].eq(tableAddress['id']))
            queryTable = queryTable.leftJoin(tableAddressHouse, tableAddress['house_id'].eq(tableAddressHouse['id']))
            cond.append(db.joinOr([tableAddress['id'].isNull(), tableAddress['deleted'].eq(0)]))
            cond.append(db.joinOr([tableAddressHouse['id'].isNull(), tableAddressHouse['deleted'].eq(0)]))
        if filterAddressCity:
            cond.append(tableAddressHouse['KLADRCode'].like(filterAddressCity))
        if filterAddressStreet:
            cond.append(tableAddressHouse['KLADRStreetCode'].like(filterAddressStreet))
        if filterAddressHouse:
            cond.append(tableAddressHouse['number'].eq(filterAddressHouse))
        if filterAddressCorpus:
            cond.append(tableAddressHouse['corpus'].eq(filterAddressCorpus))
        if filterAddressFlat:
            cond.append(tableAddress['flat'].eq(filterAddressFlat))
    if isFilterAddressOrgStructure:
        addrIdList = None
        cond2 = []
        if (addrType+1) & 1:
            addrIdList = getOrgStructureAddressIdList(addressOrgStructureId)
            addAddressCond(db, cond2, 0, addrIdList)
        if (addrType+1) & 2:
            if addrIdList is None:
                addrIdList = getOrgStructureAddressIdList(addressOrgStructureId)
            addAddressCond(db, cond2, 1, addrIdList)
        if ((addrType+1) & 4):
            if addressOrgStructureId:
                addAttachCond(db, cond2, 'orgStructure_id = %d'%addressOrgStructureId, 1, None)
            else:
                addAttachCond(db, cond2, 'LPU_id=%d'%QtGui.qApp.currentOrgId(), 1, None)
        if cond2:
            cond.append(db.joinOr(cond2))
    if countClientId:
        stmt="""
    SELECT
       COUNT(DISTINCT Diagnosis.client_id) AS clientCount
    FROM %s
    WHERE Diagnosis.deleted=0 AND Diagnosis.mod_id IS NULL AND %s
        """ % (db.getTableName(queryTable),
               db.joinAnd(cond))
    else:
        stmt="""
    SELECT
       Diagnosis.MKB AS MKB,
       COUNT(DISTINCT Diagnosis.id) AS sickCount,
       COUNT(DISTINCT Diagnosis.client_id) AS clientCount,
       rbDiseaseCharacter.code AS diseaseCharacter,
       (%s) AS firstInPeriod
    FROM %s
    WHERE Diagnosis.deleted=0 AND Diagnosis.mod_id IS NULL AND %s
    GROUP BY MKB, diseaseCharacter, firstInPeriod
        """ % (db.joinAnd([tableDiagnosis['setDate'].le(endDate),
                                        tableDiagnosis['setDate'].ge(begDate)]),
                            db.getTableName(queryTable),
                            db.joinAnd(cond))
    return db.query(stmt)



class CSickRateSurveySetupDialog(CReportAcuteInfectionsSetupDialog):
    def __init__(self, parent=None):
        CReportAcuteInfectionsSetupDialog.__init__(self, parent)
        self.setMKBFilterEnabled(True)
        self.setFilterAddressOrgStructureVisible(True)
        self.setAccountAccompEnabled(True)
        self.setSpecialityVisible(True)
        self.cmbSpeciality.setVisible(False)
        self.lblSpeciality.setVisible(False)
        self.specialityList = []
        self.lblSpecialityList = QtGui.QLabel(u'не задано')
        self.btnSpecialityList = QtGui.QPushButton(u'Специальность')
        self.btnSpecialityList.clicked.connect(self.on_btnSpecialityList_clicked)

        index = self.gridLayout.indexOf(self.lblSpeciality)
        row, col, rowspan, colspan = self.gridLayout.getItemPosition(index)
        self.gridLayout.addWidget(self.btnSpecialityList, row, col, rowspan, colspan)

        index = self.gridLayout.indexOf(self.cmbSpeciality)
        row, col, rowspan, colspan = self.gridLayout.getItemPosition(index)
        self.gridLayout.addWidget(self.lblSpecialityList, row, col, rowspan, colspan)
        self.edtBegDate.setEnabled(self.chkRegisteredInPeriod.isChecked())
        self.edtEndDate.setEnabled(self.chkRegisteredInPeriod.isChecked())


    def on_btnSpecialityList_clicked(self):
        self.specialityList = []
        self.lblSpecialityList.setText(u'не задано')
        dialog = CSpecialityListDialog(self)
        if dialog.exec_():
            self.specialityList = dialog.values()
            if self.specialityList:
                self.lblSpecialityList.setText(formatSpecialityIdList(self.specialityList))


    @pyqtSignature('bool')
    def on_chkRegisteredInPeriod_toggled(self, checked):
        self.edtBegDate.setEnabled(checked)
        self.edtEndDate.setEnabled(checked)
    

    def params(self):
        result = CReportAcuteInfectionsSetupDialog.params(self)
        del result['specialityId']
        result['specialityList'] = self.specialityList
        return result


    def setParams(self, params):
        CReportAcuteInfectionsSetupDialog.setParams(self, params)
        self.specialityList = params.get('specialityList', [])
        if self.specialityList:
            self.lblSpecialityList.setText(formatSpecialityIdList(self.specialityList))
        else:
            self.lblSpecialityList.setText(u'не задано')




class CSickRateSurvey(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
#        self.setPayPeriodVisible(False)
        self.setTitle(u'Общая сводка по заболеваемости')
        self.pageFormat = CPageFormat(pageSize=CPageFormat.A4, leftMargin=1,
                                        topMargin=1, rightMargin=1, bottomMargin=1)


    def getSetupDialog(self, parent):
        result = CSickRateSurveySetupDialog(parent)
        result.setTitle(self.title())
        return result


    def build(self, params):
        registeredInPeriod = params.get('registeredInPeriod', False)
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        eventPurposeId = params.get('eventPurposeId', None)
        eventTypeId = params.get('eventTypeId', None)
        orgStructureId = params.get('orgStructureId', None)
        specialityList = params.get('specialityList', None)
        personId = params.get('personId', None)
        sex = params.get('sex', 0)
        ageFrom = params.get('ageFrom', 0)
        ageTo = params.get('ageTo', 150)
        socStatusClassId = params.get('socStatusClassId', None)
        socStatusTypeId = params.get('socStatusTypeId', None)
        accountAccomp = params.get('accountAccomp', False)
        locality = params.get('locality', 0)
        isFilterAddressOrgStructure = params.get('isFilterAddressOrgStructure', False)
        addrType = params.get('addressOrgStructureType', 0)
        addressOrgStructureId = params.get('addressOrgStructure', None)

        db = QtGui.qApp.db
        reportRowSize = 6
        reportData = {}
        query = selectData(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeId, orgStructureId, personId, specialityList, sex, ageFrom, ageTo, socStatusClassId, socStatusTypeId, accountAccomp, locality, isFilterAddressOrgStructure, addrType, addressOrgStructureId, params)
#        records = selectData(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeId, orgStructureId, personId, sex, ageFrom, ageTo, socStatusClassId, socStatusTypeId, MKBFilter, MKBFrom, MKBTo, MKBExFilter, MKBExFrom, MKBExTo, accountAccomp, locality, params, True)
#        countClientId = 0
#        while records.next():
#            record = records.record()
#            countClientId = forceInt(record.value('clientCount'))
        while query.next():
            record    = query.record()
            MKB       = forceString(record.value('MKB'))
            sickCount = forceInt(record.value('sickCount'))
            clientCount = forceInt(record.value('clientCount'))
            diseaseCharacter = forceString(record.value('diseaseCharacter'))
            firstInPeriod = forceBool(record.value('firstInPeriod'))

            reportRow = reportData.get(MKB, None)
            if not reportRow:
                reportRow = [0]*reportRowSize
                reportData[MKB] = reportRow
            reportRow[0] += sickCount
            if diseaseCharacter == '1': # острое
                reportRow[1] += sickCount
                reportRow[2] += sickCount
            else:
                if firstInPeriod:
                    reportRow[1] += sickCount
                    reportRow[3] += sickCount
                else:
                    reportRow[4] += sickCount
            reportRow[5] += clientCount

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        if params.get('isFilterAddress', False):
            self.dumpParamsAdress(cursor, params)
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        tableColumns = [
            ('35%', [u'Наименование',   u''], CReportBase.AlignLeft),
            ('5%',  [u'Код МКБ',        u''], CReportBase.AlignLeft),
            ('10%', [u'Всего',          u''], CReportBase.AlignRight),
            ('10%', [u'Впервые',        u'всего'], CReportBase.AlignRight),
            ('10%', [u'',               u'острые'], CReportBase.AlignRight),
            ('10%', [u'',               u'хрон.'], CReportBase.AlignRight),
            ('10%', [u'Хрон. ранее изв.',          u''], CReportBase.AlignRight),
            ('10%', [u'Чел',            u''], CReportBase.AlignRight),
            ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1) # Наименование
        table.mergeCells(0, 1, 2, 1) # Код МКБ
        table.mergeCells(0, 2, 2, 1) # Всего
        table.mergeCells(0, 3, 1, 3) # Впервые
        table.mergeCells(0, 6, 2, 1) # Хрон.
        table.mergeCells(0, 7, 2, 1) # Чел

        total = [0]*reportRowSize
        blockTotal = [0]*reportRowSize
        classTotal = [0]*reportRowSize
        MKBList = reportData.keys()
        MKBList.sort()
        tableMKB = db.table('MKB')
        prevBlockId = ''
        prevClassId = ''
        for MKB in MKBList:
            MKBRecord = db.getRecordEx(tableMKB, 'ClassID, ClassName, BlockID, BlockName, DiagName', tableMKB['DiagID'].eq(MKBwithoutSubclassification(MKB)))
            if MKBRecord:
                classId   = forceString(MKBRecord.value('ClassID'))
                className = forceString(MKBRecord.value('ClassName'))
                blockId   = forceString(MKBRecord.value('BlockID'))
                blockName = forceString(MKBRecord.value('BlockName'))
                MKBName   = forceString(MKBRecord.value('DiagName'))
            else:
                classId   = '-'
                className = '-'
                blockId   = '-'
                blockName = '-'
                MKBName   = '-'

            if prevBlockId and prevBlockId != blockId:
                self.produceTotalLine(table, u'Итого по блоку '+prevBlockId, blockTotal)
                blockTotal = [0]*reportRowSize
            if prevClassId and prevClassId != classId:
                self.produceTotalLine(table, u'Всего по классу '+ prevClassId, classTotal)
                classTotal = [0]*reportRowSize
            if  prevClassId != classId:
                i = table.addRow()
                table.setText(i, 0, classId + '. ' +className)
                table.mergeCells(i, 0, 1, 8)
                prevClassId = classId
            if  prevBlockId != blockId:
                i = table.addRow()
                table.setText(i, 0, blockId+ ' '+blockName)
                table.mergeCells(i, 0, 1, 8)
                prevBlockId = blockId
            row = reportData[MKB]
            i = table.addRow()
            table.setText(i, 0, MKBName)
            table.setText(i, 1, MKB)
            for j in xrange(reportRowSize):
                table.setText(i, j+2, row[j])
                total[j] += row[j]
                blockTotal[j] += row[j]
                classTotal[j] += row[j]
        if prevBlockId:
            self.produceTotalLine(table, u'Итого по блоку '+prevBlockId, blockTotal)
        if prevClassId:
            self.produceTotalLine(table, u'Всего по классу '+prevClassId, classTotal)
        self.produceTotalLine(table, u'ВСЕГО', total)
        return doc


    def produceTotalLine(self, table, title, total):
        i = table.addRow()
        table.setText(i, 0, title, CReportBase.TableTotal)
        for j in xrange(len(total)):
            table.setText(i, j+2, total[j], CReportBase.TableTotal)
