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

from Reports.ReportSetupDialog import CReportSetupDialog
from Reports.Report import CReport
from Reports.ReportBase import CReportBase, createTable
from library.Utils import forceRef, forceString, forceDate

# наименование / текущая группа / предыдущая группа
MainRows = [
    (u'I гр усилено из II группы', '083', '082'),
    (u'I гр усилено из III группы', '083', '081'),
    (u'I гр понижено до II группы', '082', '083'),
    (u'I гр понижено до III группы', '081', '083'),
    (u'Снято  с I группы', '', '083'),
    (u'II гр усилено из  III группы', '082', '081'),
    (u'II гр усилено в I группу', '083', '082'),
    (u'II гр понижено до III группы', '082', '083'),
    (u'Снято со II группы', '', '082'),
    (u'III  гр усилено в I группу', '083', '081'),
    (u'III  гр усилено во II группу', '082', '081'),
    (u'Снято с III группы ', '', '081')
]

class CReportInvalidGroupMovement(CReport):

    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Движение инвалидов из группы в группу')


    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setEventTypeVisible(False)
        result.setMKBFilterVisible(False)
        result.setPersonVisible(False)
        result.cmbPerson.setVisible(False)
        result.lblPerson.setVisible(False)
        result.setOnlyPermanentAttachVisible(False)
        result.setTitle(self.title())
        result.setOrgStructureVisible(False)
        result.setActionStatusVisible(False)
        for i in xrange(result.gridLayout.count()):
            spacer = result.gridLayout.itemAt(i)
            if isinstance(spacer, QtGui.QSpacerItem):
                itemposition = result.gridLayout.getItemPosition(i)
                if itemposition != (29, 0, 1, 1) and itemposition != (8, 1, 1, 3):
                    result.gridLayout.removeItem(spacer)
        result.resize(400, 10)
        return result


    def build(self, params):
        mapMainRows = createMapGroupsToRowIdx([(row[1], row[2]) for row in MainRows])
        rowSize = 1
        reportMainData = [[0] * rowSize for row in xrange(len(MainRows))]
        query = selectData(params)
        dictTakenInvalidGroup = dict()
        dictRemovedInvalidGroup = dict()
        while query.next():
            record = query.record()
            clientId = forceRef(record.value('client_id'))
            code = forceString(record.value('code'))
            begDate = forceDate(record.value('begDate'))
            endDate = forceDate(record.value('endDate'))
            if endDate.isNull():
                dictTakenInvalidGroup[clientId] = (code, begDate, None)
            else:
                dictRemovedInvalidGroup[clientId] = (code, begDate, endDate)

        for clientId in dictRemovedInvalidGroup:
            removedGroup = dictRemovedInvalidGroup[clientId]
            takenGroup = dictTakenInvalidGroup.get(clientId, None)
            removedCode = removedGroup[0]
            takenCode = takenGroup[0] if takenGroup else ''
            rows = mapMainRows.get((takenCode, removedCode), [])
            for row in rows:
                reportLine = reportMainData[row]
                reportLine[0] += 1

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Движение инвалидов из группы в группу')
        tableColumns = [('20%', [u'Движение'], CReportBase.AlignLeft),
                        ('10%', [u'Количество пациентов'], CReportBase.AlignCenter)]
        table = createTable(cursor, tableColumns)

        for row, rowDescr in enumerate(MainRows):
            reportLine = reportMainData[row]
            i = table.addRow()
            table.setText(i, 0, rowDescr[0])
            table.setText(i, 1, reportLine[0])

        return doc


def selectData(params):
    db = QtGui.qApp.db
    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())

    stmt = u'''
SELECT css.client_id, sst.code, css.begDate, css.endDate
FROM ClientSocStatus css
left JOIN rbSocStatusClass ssc ON ssc.id = css.socStatusClass_id
left JOIN rbSocStatusClass ssc2 ON ssc2.id = ssc.group_id
left JOIN rbSocStatusType sst ON sst.id = css.socStatusType_id
left JOIN Client c on c.id = css.client_id
WHERE css.deleted = 0 AND c.deleted = 0 
    AND sst.code in ('081', '082', '083')
    AND note IN ('1с', '2с', '3с') 
    AND ssc2.code = '1' AND ssc.code = '1'
    AND (css.begDate BETWEEN {begDate} AND {endDate} 
        OR css.endDate BETWEEN {begDate} AND {endDate});
    '''.format(begDate=db.formatDate(begDate), endDate=db.formatDate(endDate))

    return db.query(stmt)

def createMapGroupsToRowIdx(codesList):
    mapCodeToRowIdx = {}
    for rowIdx, (group1, group2) in enumerate(codesList):
        mapCodeToRowIdx.setdefault((group1, group2), []).append(rowIdx)
    return mapCodeToRowIdx
