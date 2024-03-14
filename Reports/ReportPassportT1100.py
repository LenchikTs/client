# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2023 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4              import QtGui
from PyQt4.QtCore       import Qt, QDate
from library.Utils      import forceInt, forceString
from library.database   import decorateString
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable


def selectData(params):
    db = QtGui.qApp.db
    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())
    orgStructureId = params.get('orgStructureId')

    stmt = u'''
      SELECT Client.id,
        Client.sex,
        age(Client.birthDate, {endDate}) AS age,
rbDispanser.code
  FROM Client
  INNER JOIN Diagnosis ON Diagnosis.`client_id`=Client.`id`  
    INNER JOIN Diagnostic ON Diagnostic.`diagnosis_id`=Diagnosis.`id`  
      INNER JOIN rbDispanser ON rbDispanser.`id`=Diagnostic.`dispanser_id`  
        
        WHERE (Client.`deleted`=0) AND (Diagnosis.`deleted`=0) AND (Diagnostic.`deleted`=0) AND (Diagnostic.`dispanser_id` IS NOT NULL)
         AND (Diagnostic.`endDate`<={endDate}) 
      AND (rbDispanser.`observed`=1) AND (Client.`deathDate` IS NULL) 
            AND (((EXISTS (SELECT ClientAttach.id
                       FROM ClientAttach
                       LEFT JOIN rbAttachType ON rbAttachType.id = ClientAttach.attachType_id
                       WHERE ClientAttach.deleted=0
                       AND (ClientAttach.client_id = Client.id) AND (ClientAttach.orgStructure_id IN ({orgStructureId}))
                       AND ClientAttach.id in (SELECT MAX(CA2.id)
                                   FROM ClientAttach AS CA2
                                   LEFT JOIN rbAttachType AS rbAttachType2 ON rbAttachType2.id = CA2.attachType_id
                                   WHERE CA2.deleted=0 AND (CA2.client_id = Client.id) AND (rbAttachType2.temporary=0)))))) AND (NOT EXISTS(SELECT DC.id
                                   FROM Diagnostic AS DC
                                   INNER JOIN Diagnosis AS DS ON DS.id = DC.diagnosis_id
                                   INNER JOIN rbDispanser AS rbDP ON rbDP.id = DC.dispanser_id
                                   WHERE DS.client_id = Client.id
                                   AND DC.endDate <= {endDate} AND rbDP.name LIKE '%%снят%%' AND DC.deleted = 0 AND DS.deleted = 0
                                   AND (DC.diagnosis_id = Diagnosis.id OR DS.MKB = Diagnosis.MKB)))  
  
  GROUP BY Client.id   
    '''
    return db.query(stmt.format(
            begDate=decorateString(begDate.toString(Qt.ISODate)),
            endDate=decorateString(endDate.toString(Qt.ISODate)),
            orgStructureId=orgStructureId if orgStructureId else 'NULL',
        ))



class CReportPassportT1100(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Т.1100')


    def getSetupDialog(self, parent):
        dialog = CReport.getSetupDialog(self, parent)
        dialog.setEventTypeVisible(False)
        dialog.setOnlyPermanentAttachVisible(False)
        dialog.setOrgStructureVisible(True)
        dialog.adjustSize()
        return dialog


    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        tableColumns = [
            (u'21%', [u'Состав прикрепленного к врачебному (терапевтическому) участку населения по возрасту, полу', u''], CReportBase.AlignLeft),
            (u'6%', [u'№ строки', u''], CReportBase.AlignCenter),
            (u'6%', [u'Состоит под диспансерным наблюдением (человек)', u'всего'], CReportBase.AlignRight),
            (u'6%', [u'', u'в т.ч. взято на учет в отчетном году'], CReportBase.AlignRight),
            (u'6%', [u'Нуждались в лечении на начало отчетного года (человек)', u'амбулаторном'], CReportBase.AlignRight),
            (u'6%', [u'', u'стационарном'], CReportBase.AlignRight),
            (u'6%', [u'', u'высокотехнологической медицинской помощи (ВТМП)'], CReportBase.AlignRight),
            (u'6%', [u'', u'в дневном стационаре'], CReportBase.AlignRight),
            (u'6%', [u'', u'санаторно-курортном'], CReportBase.AlignRight),
            (u'6%', [u'Из числа нуждающихся получили лечение (человек)', u'амбулаторное'], CReportBase.AlignRight),
            (u'6%', [u'', u'стационарное'], CReportBase.AlignRight),
            (u'6%', [u'', u'высокотехнологическую медицинскую помощи (ВТМП)'], CReportBase.AlignRight),
            (u'6%', [u'', u'в дневном стационаре'], CReportBase.AlignRight),
            (u'6%', [u'', u'санаторно-курортное'], CReportBase.AlignRight),
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0,0, 2,1)
        table.mergeCells(0,1, 2,1)
        table.mergeCells(0,2, 1,2)
        table.mergeCells(1,2, 1,1)
        table.mergeCells(1,3, 1,1)
        table.mergeCells(0, 4, 1, 5)
        table.mergeCells(0, 9, 1, 5)

        reportDataKeys = (
            'all',
            'able',
            'noable',
        )
        reportDataRowText = (
            u'Всего',
            u'В том числе: трудоспособного возраста',
            u'нетрудоспособного возраста',
        )

        reportData = {}
        for key in reportDataKeys:
            reportData[key] = [set() for i in xrange(12)]
            reportData[key + 'Male'] = [set() for i in xrange(12)]
            reportData[key + 'Female'] = [set() for i in xrange(12)]

        query = selectData(params)
        while query.next():
            record = query.record()
            clientId = forceInt(record.value('id'))
            age = forceInt(record.value('age'))
            sex = forceInt(record.value('sex'))
            dispCode = forceString(record.value('code'))

            keys = []
            keys.append('all')
            if sex == 1:
                keys.append('allMale')
                if 16 <= age < 65:
                    if 'able' not in keys:
                        keys.append('able')
                    keys.append('ableMale')
                else:
                    if 'noable' not in keys:
                        keys.append('noable')
                    keys.append('noableMale')
            if sex == 2:
                keys.append('allFemale')
                if 16 <= age < 60:
                    if 'able' not in keys:
                        keys.append('able')
                    keys.append('ableFemale')
                else:
                    if 'noable' not in keys:
                        keys.append('noable')
                    keys.append('noableFemale')


            for key in keys:
                reportLine = reportData[key]
                reportLine[0].add(clientId)
                if dispCode == '2':
                    reportLine[1].add(clientId)

        rownum = 1
        for i in xrange(len(reportDataKeys)):
            rownum = self.addLine(table, reportData, reportDataKeys[i], reportDataRowText[i], rownum)
        return doc


    def addLine(self, table, reportData, key, text, rownum=0):
        reportLine = reportData[key]
        reportLineMale = reportData[key + 'Male']
        reportLineFemale = reportData[key + 'Female']

        row = table.addRow()
        rowMale = table.addRow()
        rowFemale = table.addRow()

        table.setText(row, 0, text)
        table.setText(row, 1, rownum)
        for i, clientSet in enumerate(reportLine):
            if i == 4:  # Инвалиды - Всего
                table.setText(row, 2+i,
                    len(reportLine[i+1]) + len(reportLine[i+2]) + len(reportLine[i+3]))
            else:
                table.setText(row, 2+i, len(clientSet))

        table.setText(rowMale, 0, u'Мужчины')
        table.setText(rowMale, 1, rownum+1)
        for i, clientSet in enumerate(reportLineMale):
            if i == 4:  # Инвалиды - Всего
                table.setText(rowMale, 2+i,
                    len(reportLineMale[i+1]) + len(reportLineMale[i+2]) + len(reportLineMale[i+3]))
            else:
                table.setText(rowMale, 2+i, len(clientSet))

        table.setText(rowFemale, 0, u'Женщины')
        table.setText(rowFemale, 1, rownum+2)
        for i, clientSet in enumerate(reportLineFemale):
            if i == 4:  # Инвалиды - Всего
                table.setText(rowFemale, 2+i,
                    len(reportLineFemale[i+1]) + len(reportLineFemale[i+2]) + len(reportLineFemale[i+3]))
            else:
                table.setText(rowFemale, 2+i, len(clientSet))

        return rownum + 3
