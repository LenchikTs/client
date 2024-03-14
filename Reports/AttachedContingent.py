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
from PyQt4.QtCore import QDate

from library.Utils      import forceBool, forceInt

from Orgs.Utils         import getOrgStructureDescendants, getOrgStructures,  getOrgStructureFullName
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable


def selectData(date, areaId, addressType):
    stmt="""
SELECT
    COUNT(*) AS cnt,
    age(Client.birthDate, %(attachCheckDate)s) AS clientAge,
    orgStructure_id,
    Client.sex AS clientSex,
    IF(((ClientWork.org_id IS NOT NULL OR TRIM(ClientWork.freeInput) != '') AND
    EXISTS(SELECT ClientSocStatus.id
           FROM ClientSocStatus
           INNER JOIN rbSocStatusClass ON rbSocStatusClass.id = ClientSocStatus.socStatusClass_id
           INNER JOIN rbSocStatusType ON rbSocStatusType.id = ClientSocStatus.socStatusType_id
           WHERE ClientSocStatus.deleted=0 AND ClientSocStatus.client_id = Client.id
           AND rbSocStatusClass.code = 9 AND rbSocStatusType.name LIKE '%(dat)s')), 1, 0
    ) AS busy
FROM Client
LEFT JOIN ClientAddress AS CAReg ON CAReg.client_id = Client.id
                        AND CAReg.id = (SELECT MAX(CARegInt.id) FROM ClientAddress AS CARegInt WHERE CARegInt.type=0 AND CARegInt.client_id=Client.id)
LEFT JOIN Address       AS AReg ON AReg.id = CAReg.address_id
LEFT JOIN ClientAddress AS CALoc ON CALoc.client_id = Client.id
                        AND CALoc.id = (SELECT MAX(CALocInt.id) FROM ClientAddress AS CALocInt WHERE CALocInt.type=1 AND CALocInt.client_id=Client.id)
LEFT JOIN Address       AS ALoc ON ALoc.id = CALoc.address_id
LEFT JOIN ClientAttach  ON ClientAttach.client_id = Client.id
                        AND ClientAttach.id = (SELECT MAX(CAT.id) FROM ClientAttach AS CAT
                                               LEFT JOIN rbAttachType ON rbAttachType.id=CAT.attachType_id
                                               WHERE CAT.deleted=0
                                               AND   CAT.client_id=Client.id
                                               AND   rbAttachType.temporary=0
                                               AND   CAT.begDate<=%(attachCheckDate)s
                                               AND   (CAT.endDate IS NULL or CAT.endDate>=%(attachCheckDate)s)
                                              )
LEFT JOIN ClientWork    ON ClientWork.client_id = Client.id
                        AND ClientWork.id = (SELECT MAX(CW.id) FROM ClientWork AS CW WHERE CW.deleted=0 AND CW.client_id=Client.id)
LEFT JOIN rbAttachType ON rbAttachType.id=ClientAttach.attachType_id
WHERE
  %(cond)s
GROUP BY orgStructure_id, clientAge, clientSex, busy
    """
    db = QtGui.qApp.db
    tableClient = db.table('Client')
    tableAttachType = db.table('rbAttachType')

    cond = [ tableClient['deleted'].eq(0),db.joinOr([ tableClient['deathDate'].ge(date),
                             tableClient['deathDate'].isNull()]), 
#             tableAttachType['outcome'].eq(0)
             db.joinOr( [tableAttachType['outcome'].eq(0), tableAttachType['id'].isNull()] )
           ]
    if areaId:
        areaIdList = getOrgStructureDescendants(areaId)
    else:
        areaIdList = getOrgStructures(QtGui.qApp.currentOrgId())
    reg = (addressType+1) & 1
    loc = (addressType+1) & 2
    attach = (addressType+1) & 4
    condAddr = []
    if reg:
        tableOrgStructureAddress = db.table('OrgStructure_Address')
        tableAddress = db.table('Address').alias('AReg')
        subCond = [ tableOrgStructureAddress['master_id'].inlist(areaIdList),
                    tableOrgStructureAddress['house_id'].eq(tableAddress['house_id']),
                  ]
        condAddr.append(db.existsStmt(tableOrgStructureAddress, subCond))
    if loc:
        tableOrgStructureAddress = db.table('OrgStructure_Address')
        tableAddress = db.table('Address').alias('ALoc')
        subCond = [ tableOrgStructureAddress['master_id'].inlist(areaIdList),
                    tableOrgStructureAddress['house_id'].eq(tableAddress['house_id']),
                  ]
        condAddr.append(db.existsStmt(tableOrgStructureAddress, subCond))
    if attach:
        tableClientAttach = db.table('ClientAttach')
        condAddr.append(db.joinAnd([db.joinOr([tableClientAttach['orgStructure_id'].inlist(areaIdList),
                                               # tableClientAttach['orgStructure_id'].isNull()
                                              ]),
                                      tableClientAttach['deleted'].eq(0)
                                    ]))
    if condAddr:
        cond.append(db.joinOr(condAddr))
    st=stmt % {'attachCheckDate':tableClient['birthDate'].formatValue(date), 'dat':u'работающий%%', 'cond':db.joinAnd(cond)}
    return db.query(st)


class CAttachedContingent(CReport):
    
    
    
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setPayPeriodVisible(False)
        self.setTitle(u'Прикреплённый контингент')


    def getSetupDialog(self, parent):
        result = CAttachedContingentSetupDialog(parent)
        result.setTitle(self.title())
        return result


    def build(self, params):
        endDate = params.get('endDate', QDate())
        areaId = params.get('areaId', None)
        addressType = params.get('addressType', 0)
        check_all = params.get('checkbox_all')
        reportRowSize = 15
        query = selectData(endDate, areaId, addressType)

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        tableColumns = [
            ('15%', [u'Категории населения',   u''], CReportBase.AlignLeft),
            ( '5%', [u'№ стр.',                u''], CReportBase.AlignRight),
            ( '5%', [u'Численность прикреплённого населения по возрастному составу', u'дети', u'до 1 года', u'М'], CReportBase.AlignRight),
            ( '5%', [u'', u'', u'', u'Ж'], CReportBase.AlignRight),
            ( '5%', [u'', u'', u'1 год', u'М'], CReportBase.AlignRight),
            ( '5%', [u'', u'', u'', u'Ж'], CReportBase.AlignRight),
            ( '5%', [u'', u'', u'2-6 лет', u'М'], CReportBase.AlignRight),
            ( '5%', [u'', u'', u'', u'Ж'], CReportBase.AlignRight),
            ( '5%', [u'', u'', u'7-14 лет', u'М'], CReportBase.AlignRight),
            ( '5%', [u'', u'', u'', u'Ж'], CReportBase.AlignRight),
            ( '5%', [u'', u'', u'15-17 лет', u'М'], CReportBase.AlignRight),
            ( '5%', [u'', u'', u'', u'Ж'], CReportBase.AlignRight),
            ( '5%', [u'', u'взрослые', u'трудосп. возраста', u'М, 18-59 лет'], CReportBase.AlignRight),
            ( '5%', [u'', u'', u'', u'Ж, 18-54 лет'], CReportBase.AlignRight),
            ( '5%', [u'', u'', u'нетрудосп. возраста', u'М, 60 и ст.'], CReportBase.AlignRight),
            ( '5%', [u'', u'', u'', u'Ж, 55 и ст.'], CReportBase.AlignRight),
            ( '5%', [u'Всего', ], CReportBase.AlignRight),
            ]


        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 4, 1) # Категории населения
        table.mergeCells(0, 1, 4, 1) # № стр.
        table.mergeCells(0, 2, 1,14) # Численность...
        table.mergeCells(1, 2, 1,10) # дети
        table.mergeCells(2, 2, 1, 2) # <1
        table.mergeCells(2, 4, 1, 2) # 1
        table.mergeCells(2, 6, 1, 2) # 2-6
        table.mergeCells(2, 8, 1, 2) # 7-14
        table.mergeCells(2,10, 1, 2) # 15-17
        table.mergeCells(1,12, 1, 4) # взрослые
        table.mergeCells(2,12, 1, 2) # тр.
        table.mergeCells(2,14, 1, 2) # нетр.
        table.mergeCells(0,16, 4, 1) # всего
        
        if check_all is False:
            reportData = [[0]*reportRowSize for row in range(3)]
            while query.next():

                record = query.record()
                cnt = forceInt(record.value('cnt'))
                age = forceInt(record.value('clientAge'))
                sex = forceInt(record.value('clientSex'))
                busy = forceBool(record.value('busy'))

                if age < 1:
                    colBase = 0
                elif age == 1:
                    colBase = 2
                elif age <= 6:
                    colBase = 4
                elif age <= 14:
                    colBase = 6
                elif age <= 17:
                    colBase = 8
                elif (sex==1 and age < 60) or (sex != 1 and age < 55):
                    colBase = 10
                else:
                    colBase = 12
                cols = [colBase+(0 if sex == 1 else 1), 14]
                rows = [0, 1 if busy else 2]
                for row in rows:
                    for col in cols:
                        reportData[row][col] += cnt

            # now text

            for rowIndex, rowName in enumerate([u'ИТОГО', u'работающие', u'неработающие']):
                i = table.addRow()
                table.setText(i, 0, rowName)
                table.setText(i, 1, rowIndex+1)
                rowData = reportData[rowIndex]
                for j in xrange(len(rowData)):
                    table.setText(i, 2+j, rowData[j])

            return doc

        elif check_all is True:
            reportRowSize = 17
            colsShift = 1
            reportData = {}
            prevOrgStructure = None
            self.reportData = [[0]*(reportRowSize - 2) for row in range(3)]
            self.index = 1

            def processQuery(query):
                while query.next():
                    record = query.record()
                    orgStrId = forceInt(record.value('orgStructure_Id'))
                    cnt = forceInt(record.value('cnt'))
                    age = forceInt(record.value('clientAge'))
                    sex = forceInt(record.value('clientSex'))
                    busy = forceBool(record.value('busy'))

                    if age < 1:
                        colBase = 0
                    elif age == 1:
                        colBase = 2
                    elif age <= 6:
                        colBase = 4
                    elif age <= 14:
                        colBase = 6
                    elif age <= 17:
                        colBase = 8
                    elif (sex == 1 and age < 60) or (sex != 1 and age < 55):
                        colBase = 10
                    else:
                        colBase = 12
                    cols = [colBase + (0 if sex == 1 else 1), 14]
                    rows = [0, 1 if busy else 2]
                    for row in rows:
                        for col in cols:
                            self.reportData[row][col] += cnt

                    reportLine = reportData.setdefault((orgStrId, 0), [0]*reportRowSize)
                    reportLine2 = reportData.setdefault((orgStrId, 1), [0] * reportRowSize)
                    reportLine3 = reportData.setdefault((orgStrId, 2), [0] * reportRowSize)
                    rows = [reportLine, reportLine2 if busy else reportLine3]
                    for row in rows:
                        row[15] += cnt
                        if sex == 1:
                            if age < 1:
                                row[1] += cnt
                            elif age == 1:
                                row[3] += cnt
                            elif age <= 6:
                                row[5] += cnt
                            elif age <= 14:
                                row[7] += cnt
                            elif age <= 17:
                                row[9] += cnt
                            elif sex == 1 and age < 60:
                                row[11] += cnt
                            else:
                                row[13] += cnt
                        elif sex != 1:
                            if age < 1:
                                row[2] += cnt
                            elif age == 1:
                                row[4] += cnt
                            elif age <= 6:
                                row[6] += cnt
                            elif age <= 14:
                                row[8] += cnt
                            elif age <= 17:
                                row[10] += cnt
                            elif sex != 1 and age < 55:
                                row[12] += cnt
                            else:
                                row[14] += cnt

            processQuery(query)

            keys = reportData.keys()
            keys.sort()

            for key in keys:
                orgStructure = key[0]
                if key[0] != 0:
                    orgName = getOrgStructureFullName(key[0])
                    if prevOrgStructure != orgStructure and orgStructure is not None:
                        row = table.addRow()
                        table.mergeCells(row, 0, 1, reportRowSize + 5)
                        table.setText(row, 0, orgName, CReportBase.TableHeader)
                        prevOrgStructure = orgStructure

                    row = table.addRow()
                    reportLine = reportData[key]
                    table.setText(row, 0, [u'ИТОГО', u'работающие', u'неработающие'][key[1]])

                    for col in xrange(reportRowSize - colsShift):
                        table.setText(row, col + colsShift, reportLine[col])

                    table.setText(row, 1, self.index)
                    self.index += 1
            row = table.addRow()
            table.mergeCells(row, 0, 1, reportRowSize + 5)
            table.setText(row, 0, u'Итого по ЛПУ ', CReportBase.TableHeader)
            rowAll = table.addRow()
            table.setText(rowAll, 0, u'ИТОГО')
            table.setText(rowAll, 1, self.index)
            self.index += 1
            column = 1
            for col in self.reportData[0]:

                table.setText(rowAll, column + 1, col)
                column += 1
            rowWorker = table.addRow()
            table.setText(rowWorker, 0, u'работающие')
            table.setText(rowWorker, 1, self.index)
            self.index += 1
            column = 1
            for col in self.reportData[1]:
                table.setText(rowWorker, column + 1, col)
                column += 1
            rowNotworker = table.addRow()
            table.setText(rowNotworker, 0, u'неработающие')
            table.setText(rowNotworker, 1, self.index)
            self.index += 1
            column = 1
            for col in self.reportData[2]:
                table.setText(rowNotworker, column + 1, col)
                column += 1

            return doc

from Ui_AttachedContingentSetup import Ui_AttachedContingentSetupDialog


class CAttachedContingentSetupDialog(QtGui.QDialog, Ui_AttachedContingentSetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.patientRequired = False
        self.setupUi(self)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())
        self.checkBox_all.setVisible(True)

    def setPayPeriodVisible(self, value):
        pass

    def setWorkTypeVisible(self, value):
        pass

    def setTitle(self, title):
        self.setWindowTitle(title)

    def setEventTypeVisible(self, visible=True):
        pass

    def setParams(self, params):
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.cmbOrgStructure.setValue(params.get('areaId', None))
        self.cmbAddressOrgStructureType.setCurrentIndex(params.get('addressType', 4))

    def params(self):
        result = {}
        result['endDate'] = self.edtEndDate.date()
        result['areaId'] = self.cmbOrgStructure.value()
        result['addressType'] = self.cmbAddressOrgStructureType.currentIndex()
        result['checkbox_all'] = self.checkBox_all.isChecked()
        return result
