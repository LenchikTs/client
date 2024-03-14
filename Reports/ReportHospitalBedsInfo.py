# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2017 SAMSON Group. All rights reserved.
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

from Orgs.Utils import getOrgStructureListDescendants
from Reports.Report import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.ReportSetupDialog import CReportSetupDialog
from Reports.ReportView import CPageFormat
from library.Utils import forceInt, forceString, forceDate, calcAge


def selectData(params):
    # begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())
    orgStructureId = params.get('orgStructureId', None)
    descendantsIdList = []

    if orgStructureId:
        descendantsIdList = getOrgStructureListDescendants([orgStructureId])

    db = QtGui.qApp.db

    tableEvent = db.table('Event')
    tableAction = db.table('Action')
    tableOrgStructureHospitalBed = db.table('OrgStructure_HospitalBed')
    tableRbHospitalBedProfile = db.table('rbHospitalBedProfile')
    tableRbHospitalBedType = db.table('rbHospitalBedType')
    tableOrgStrucutre = db.table('OrgStructure')
    tableClient = db.table('Client')
    tableClientRelation = db.table('ClientRelation')
    tableRbRelationType = db.table('rbRelationType')
    tableDiagnostic = db.table('Diagnostic')
    tableAssociatedDiagnostic = db.table('Diagnostic').alias('AssociatedDiagnostic')
    tableDiagnosis = db.table('Diagnosis')
    tableAssociatedDiagnosis = db.table('Diagnosis').alias('AssociatedDiagnosis')
    queryTable = tableOrgStructureHospitalBed
    queryTable = queryTable.leftJoin(tableRbHospitalBedProfile, tableRbHospitalBedProfile['id'].eq(tableOrgStructureHospitalBed['profile_id']))
    queryTable = queryTable.leftJoin(tableRbHospitalBedType, tableRbHospitalBedType['id'].eq(tableOrgStructureHospitalBed['type_id']))
    queryTable = queryTable.leftJoin(tableOrgStrucutre, tableOrgStrucutre['id'].eq(tableOrgStructureHospitalBed['master_id']))
    queryTable = queryTable.leftJoin(tableAction, '''Action.id = (SELECT Action.id
  FROM ActionProperty_HospitalBed
  LEFT JOIN ActionProperty ON ActionProperty_HospitalBed.`id` = ActionProperty.`id` AND ActionProperty.deleted = 0
  LEFT JOIN Action ON ActionProperty.`action_id` = Action.`id` AND Action.deleted = 0
  LEFT JOIN ActionType at ON at.id = Action.actionType_id AND at.deleted = 0
  WHERE ActionProperty_HospitalBed.value = OrgStructure_HospitalBed.id
    AND at.flatCode = 'moving'
    AND (Action.`endDate` IS NULL OR Action.`endDate` < {0})
  ORDER BY Action.`begDate` DESC LIMIT 1
  )'''.format(db.formatDate(endDate)))
    queryTable = queryTable.leftJoin(tableEvent, tableAction['event_id'].eq(tableEvent['id']))
    queryTable = queryTable.leftJoin(tableClient, tableClient['id'].eq(tableEvent['client_id']))
    queryTable = queryTable.leftJoin(tableClientRelation, tableClientRelation['client_id'].eq(tableClient['id']))
    queryTable = queryTable.leftJoin(tableRbRelationType, tableRbRelationType['id'].eq(tableClientRelation['relativeType_id']))
    queryTable = queryTable.leftJoin(tableDiagnostic, [tableDiagnostic['event_id'].eq(tableEvent['id']), '''Diagnostic.id = (SELECT d.id
      FROM Diagnostic d
      INNER JOIN rbDiagnosisType ON rbDiagnosisType.id = d.diagnosisType_id
      WHERE d.event_id = Event.id
      AND rbDiagnosisType.CODE = '7'
      AND d.deleted = 0
      ORDER BY rbDiagnosisType.code
      LIMIT 1)'''])
    queryTable = queryTable.leftJoin(tableAssociatedDiagnostic, [tableAssociatedDiagnostic['event_id'].eq(tableEvent['id']), '''AssociatedDiagnostic.id = (SELECT d.id
      FROM Diagnostic d
      INNER JOIN rbDiagnosisType ON rbDiagnosisType.id = d.diagnosisType_id
      WHERE d.event_id = Event.id
      AND rbDiagnosisType.CODE = '11'
      AND d.deleted = 0
      ORDER BY rbDiagnosisType.code
      LIMIT 1)'''])
    queryTable = queryTable.leftJoin(tableDiagnosis, [tableDiagnosis['id'].eq(tableDiagnostic['diagnosis_id']), tableDiagnosis['deleted'].eq(0)])
    queryTable = queryTable.leftJoin(tableAssociatedDiagnosis, [tableAssociatedDiagnosis['id'].eq(tableAssociatedDiagnostic['diagnosis_id']), tableAssociatedDiagnosis['deleted'].eq(0)])

    cols = [tableOrgStructureHospitalBed['id'].alias('OSHBId'),
            tableOrgStructureHospitalBed['master_id'].alias('masterOrgStructure'),
            tableOrgStrucutre['name'].alias('orgStructureName'),
            tableOrgStructureHospitalBed['code'].alias('OSHBCode'),
            tableOrgStructureHospitalBed['name'].alias('OSHBName'),
            tableRbHospitalBedType['name'].alias('typeName'),
            tableClient['sex'].alias('clientSex'),
            tableClient['lastName'].alias('clientLastName'),
            tableClient['firstName'].alias('clientFirstName'),
            tableClient['patrName'].alias('clientPatrName'),
            tableClient['birthDate'].alias('clientBirthDate'),
            tableDiagnosis['MKB'].alias('clientMKB'),
            tableAssociatedDiagnosis['MKB'].alias('clientMKBEx'),
            tableAction['begDate'].alias('clientBegDate'),
            tableAction['endDate'].alias('clientEndDate'),
            tableEvent['id'].alias('eventId'),
            tableRbRelationType['leftName'].alias('relationTypeLeftName'),
            tableRbRelationType['rightName'].alias('relationTypeRightName')
            ]
    cond = []
    cond.append(tableOrgStructureHospitalBed['code'].inlist(['IVL', 'NIVL', 'General']))
    if descendantsIdList:
        cond.append(tableOrgStructureHospitalBed['master_id'].inlist(descendantsIdList))

    recordsList = db.getRecordList(queryTable, cols, cond, 'OrgStructure.name, OrgStructure_HospitalBed.master_id, OrgStructure_HospitalBed.name, OrgStructure_HospitalBed.code')

    return recordsList


class CReportHospitalBedsInfo(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Сводка. Коечный фонд')
        self.setOrientation(QtGui.QPrinter.Landscape)
        self.pageFormat = CPageFormat(pageSize=QtGui.QPrinter.A4, orientation=QtGui.QPrinter.Landscape, leftMargin=10, topMargin=10, rightMargin=10, bottomMargin=10)


    def getUslDispans(self,query):
        self.mapNumMesVisitCodeToRow = {}
        self.rowNames = []
        i = 0
        while query.next():
            record = query.record()
            num = forceInt(record.value('id'))
            tit = forceString(record.value('tit'))
            self.mapNumMesVisitCodeToRow[num] = i
            self.rowNames.append(unicode(tit))
            i += 1

    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setFixedHeight(150)
        result.setEventTypeVisible(False)
        result.setOnlyPermanentAttachVisible(False)
        result.lblEndDate.setText(u'Дата')
        result.lblBegDate.setVisible(False)
        result.edtBegDate.setVisible(False)
        result.setOrgStructureVisible(True)
        result.setTitle(self.title())
        return result

    def _getDefault(self):
        result = [ [0, 0, 0, 0, 0]
                   for row in self.rowNames
                 ]
        return result


    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()

        tableColumns = [
            ('5%', [u'Отделение', u'1'], CReportBase.AlignLeft),
            ('5%', [u'Палата', u'2'], CReportBase.AlignRight),
            ('5%', [u'Койка', u'3'], CReportBase.AlignRight),
            ('5%', [u'Свободно/Занято', u'4'], CReportBase.AlignRight),
            ('10%', [u'Тип койки', u'5'], CReportBase.AlignRight),
            ('10%', [u'Контагиозность', u'6'], CReportBase.AlignRight),
            ('5%', [u'Пол', u'7'], CReportBase.AlignRight),
            ('10%', [u'ФИО', u'8'], CReportBase.AlignRight),
            ('5%', [u'Возраст', u'9'], CReportBase.AlignRight),
            ('10%', [u'Дата поступления', u'10'], CReportBase.AlignRight),
            ('5%', [u'Предварительный диагноз (Доп.МКБ)', u'11'], CReportBase.AlignRight),
            ('5%', [u'Предварительный диагноз (МКБ)', u'12'], CReportBase.AlignRight),
            ('10%', [u'Контакт', u'13'], CReportBase.AlignRight)
        ]
        recordsList = selectData(params)
        params['begDate'] = None
        params['endDate'] = None
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        table = createTable(cursor, tableColumns)


        if recordsList:
            boldChars = QtGui.QTextCharFormat()
            boldChars.setFontWeight(QtGui.QFont.Bold)
            orgStructure = None
            hospitalWard = None
            for record in recordsList:
                eventId = forceInt(record.value('eventId'))
                masterId = forceString(record.value('masterOrgStructure'))
                orgStructureName = forceString(record.value('orgStructureName'))
                code = forceString(record.value('OSHBCode'))
                name = forceString(record.value('OSHBName'))
                typeName = forceString(record.value('typeName'))
                clientSex = forceInt(record.value('clientSex'))
                if clientSex == 1:
                    clientSex = u'М'
                elif clientSex == 2:
                    clientSex = u'Ж'
                else:
                    clientSex = u''
                lastName = forceString(record.value('clientLastName'))
                firstName = forceString(record.value('clientFirstName'))
                patrName = forceString(record.value('clientPatrName'))
                fullName = u'{0} {1} {2}'.format(lastName, firstName, patrName)
                birthDate = forceDate(record.value('clientBirthDate'))
                age = calcAge(birthDate)
                MKB = forceString(record.value('clientMKB'))
                MKBEx = forceString(record.value('clientMKBEx'))
                clientBegDate = forceString(record.value('clientBegDate'))
                clientEndDate = forceString(record.value('clientEndDate'))
                leftName = forceString(record.value('relationTypeLeftName'))
                rightName = forceString(record.value('relationTypeRightName'))
                if leftName or rightName:
                    relationName = u'{0} -> {1}'.format(leftName, rightName)
                else:
                    relationName = u''

                db = QtGui.qApp.db
                tableEvent = db.table('Event')
                tableAction = db.table('Action')
                tableAP = db.table('ActionProperty')
                tableAPT = db.table('ActionPropertyType')
                tableAPS = db.table('ActionProperty_String')

                queryTable = tableEvent
                queryTable = queryTable.leftJoin(tableAction, [tableAction['event_id'].eq(tableEvent['id']), u"Action.actionType_id = (SELECT at.id FROM ActionType at WHERE name = 'Поступление')"])
                queryTable = queryTable.leftJoin(tableAP, tableAP['action_id'].eq(tableAction['id']))
                queryTable = queryTable.leftJoin(tableAPT, [tableAPT['id'].eq(tableAP['type_id']), tableAPT['deleted'].eq(0), u'''(ActionPropertyType.name = 'Контагиозность' or ActionPropertyType.name LIKE '%COVID-19%')'''])
                queryTable = queryTable.leftJoin(tableAPS, tableAPS['id'].eq(tableAP['id']))

                cols = [tableAPT['name'],
                        tableAPS['value']]
                cond = [tableEvent['id'].eq(eventId)]
                recs = db.getRecordList(queryTable, cols, cond)
                contag = u''
                covid = u''
                for rec in recs:
                    nameAPT = forceString(rec.value('name'))
                    if nameAPT == u'Контагиозность':
                        contag = forceString(rec.value('value'))
                    else:
                        covid = forceString(rec.value('value'))

                if masterId != orgStructure:
                    # i = table.addRow()
                    orgStructure = masterId
                    # table.mergeCells(i, 0, 1, 13)
                    # table.setText(i, 0, orgStructureName, charFormat=boldChars)
                    if hospitalWard != name:
                        hospitalWard = name
                        # m = table.addRow()
                        # table.mergeCells(m, 0, 1, 13)
                        # table.setText(m, 0, hospitalWard, charFormat=boldChars)
                        n = table.addRow()
                        table.setText(n, 0, orgStructureName)
                        table.setText(n, 1, name)
                        table.setText(n, 2, code)
                        table.setText(n, 4, typeName)
                        if clientEndDate or not clientBegDate:
                            table.setText(n, 3, u'Свободно')
                        else:
                            table.setText(n, 3, u'Занято')
                            table.setText(n, 5, contag)
                            table.setText(n, 6, clientSex)
                            table.setText(n, 7, fullName)
                            table.setText(n, 8, age)
                            table.setText(n, 9, clientBegDate)
                            table.setText(n, 10, MKBEx)
                            table.setText(n, 11, MKB)
                            table.setText(n, 12, relationName)
                    else:
                        n = table.addRow()
                        table.setText(n, 0, orgStructureName)
                        table.setText(n, 1, name)
                        table.setText(n, 2, code)
                        table.setText(n, 4, typeName)
                        if clientEndDate or not clientBegDate:
                            table.setText(n, 3, u'Свободно')
                        else:
                            table.setText(n, 3, u'Занято')
                            table.setText(n, 5, contag)
                            table.setText(n, 6, clientSex)
                            table.setText(n, 7, fullName)
                            table.setText(n, 8, age)
                            table.setText(n, 9, clientBegDate)
                            table.setText(n, 10, MKBEx)
                            table.setText(n, 11, MKB)
                            table.setText(n, 12, relationName)
                else:
                    if hospitalWard != name:
                        hospitalWard = name
                        # m = table.addRow()
                        # table.mergeCells(m, 0, 1, 13)
                        # table.setText(m, 0, hospitalWard, charFormat=boldChars)
                        n = table.addRow()
                        table.setText(n, 0, orgStructureName)
                        table.setText(n, 1, name)
                        table.setText(n, 2, code)
                        table.setText(n, 4, typeName)
                        if clientEndDate or not clientBegDate:
                            table.setText(n, 3, u'Свободно')
                        else:
                            table.setText(n, 3, u'Занято')
                            table.setText(n, 5, contag)
                            table.setText(n, 6, clientSex)
                            table.setText(n, 7, fullName)
                            table.setText(n, 8, age)
                            table.setText(n, 9, clientBegDate)
                            table.setText(n, 10, MKBEx)
                            table.setText(n, 11, MKB)
                            table.setText(n, 12, relationName)
                    else:
                        n = table.addRow()
                        table.setText(n, 0, orgStructureName)
                        table.setText(n, 1, name)
                        table.setText(n, 2, code)
                        table.setText(n, 4, typeName)
                        if clientEndDate or not clientBegDate:
                            table.setText(n, 3, u'Свободно')
                        else:
                            table.setText(n, 3, u'Занято')
                            table.setText(n, 5, contag)
                            table.setText(n, 6, clientSex)
                            table.setText(n, 7, fullName)
                            table.setText(n, 8, age)
                            table.setText(n, 9, clientBegDate)
                            table.setText(n, 10, MKBEx)
                            table.setText(n, 11, MKB)
                            table.setText(n, 12, relationName)

        return doc