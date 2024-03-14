# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2019 SAMSON Group. All rights reserved.
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

import re

from Orgs.Utils import getOrgStructureFullName
from Reports.StatReportEED import selectDataFromTypes
from Reports.StationaryF30_KK import splitTitle
from Reports.Ui_Form11Setup import Ui_Form11SetupDialog
from Reports.Utils import dateRangeAsStr
from library.Utils import forceInt, forceString, forceBool

from Reports.Report import CReport
from Reports.ReportBase import CReportBase, createTable

startChar = re.compile('^[A-Z]')
threeChar = re.compile('^[A-Z][0-9][0-9]$')
fourChar = re.compile('^[A-Z][0-9][0-9]\.[0-9]$')
threeOrFourChar = re.compile('^[A-Z][0-9][0-9](\.[0-9])?$')
sixChar = re.compile('^[A-Z][0-9][0-9](\.[0-9][0-9])?$')
sevenChar = re.compile('^[A-Z][0-9][0-9](\.[0-9][0-9][0-9])?$')
eightChar = re.compile('^[A-Z][0-9][0-9](\.[0-9][0-9][0-9][0-9])?$')
nineChar = re.compile('^[A-Z][0-9][0-9](\.[0-9][0-9][0-9][0-9][0-9])?$')

ord0 = ord('0')
ordA = ord('A')
# отступ | наименование | диагнозы титул | диагнозы | № строки
MainRows = [
    (0, u'Психические и поведенческие расстройства,\nсвязанные с употреблением психоактивных\nвеществ, - всего', u'F10 - F19', u'F10-F19', u'01'),
    (1, u'в том числе:\nпсихотические расстройства, связанные\nс употреблением алкоголя (алкогольные психозы)', u'F10.03, F10.07, F10.4 - F10.6, F10.73, 75, 81, 91', u'F10.03; F10.07; F10.4 - F10.6; F10.73, 75, 81, 91', u'02'),
    (2, u'из них амнестический синдром и\nрезидуальные психотические расстройства', u'F10.6, F10.73, 75', u'F10.6; F10.73, 75', u'03'),
    (1, u'синдром зависимости от алкоголя\n(алкоголизм)', u'F10.2, 3, F10.70 - 72, 74, 82, 92', u'F10.2, 3; F10.70 - 72, 74, 82, 92', u'04'),
    (2, u'из них со стадиями:\nначальная (I)', u'F10.2x1', u'F10.2x1', u'05'),
    (2, u'средняя (II)', u'F10.2x2', u'F10.2x2', u'06'),
    (2, u'конечная (III)', u'F10.2x3', u'F10.2x3', u'07'),
    (1, u'синдром зависимости от наркотических\nвеществ (наркомания)', u'F11.2-9 - F19.2-9H', u'F11.2-F11.9;F12.2-F12.9;F13.2H-F13.9H;F14.2-F14.9;F15.2H-F15.9H;F16.2H-F16.9H;F18.2H-F18.9H;F19.2H-F19.9H', u'08'),
    (2, u'в том числе вследствие употребления:\nопиоидов', u'F11.2 - F11.9', u'F11.2-F11.9', u'09'),
    (2, u'каннабиноидов', u'F12.2 - F12.9', u'F12.2-F12.9', u'10'),
    (2, u'кокаина', u'F14.2 - F14.9', u'F14.2-F14.9', u'11'),
    (2, u'других психостимуляторов', u'F15.2 - F15.9H', u'F15.2H-F15.9H', u'12'),
    (2, u'других наркотиков и их сочетаний', u'F13.2-9H; F16-9H; F18.2-9H; F19.2-9H', u'F13.2H-F13.9H;F16.2H-F16.9H;F18.2H-F18.9H;F19.2H-F19.9H', u'13'),
    (1, u'синдром зависимости от ненаркотических\nпсихоактивных веществ (токсикомания)', u'F13.2-9T - F16.2-9T; F18.2-9T - F19.2-9T', u'F13.2T-F13.9T;F16.2T-F16.9T;F18.2T-F18.9T;F19.2T-F19.9T', u'14'),
    (0, u'Пагубное (с вредными последствиями)\nупотребление:\n    алкоголя', u'F10.1', u'F10.1', u'15'),
    (2, u'наркотиков', u'F11.1 - F19.1H', u'F11.1;F12.1;F13.1H;F14.1;F15.1H;F16.1H;F18.1H;F19.1H;', u'16'),
    (2, u'ненаркотических ПАВ', u'F13.1T - F16.1T; F18.1T - F19.1T', u'F13.1T;F15.1T;F16.1T;F18.1T;F19.1T', u'17'),
    (0, u'Из общего числа потребителей наркотиков\n(из стр. 08 и 16) - употребляют наркотики\nинъекционным способом', u'', u'', u'18'),
]

# наименование | диагнозы | № строки
CompRows = [
    (u'Синдром зависимости от наркотических веществ - наркомания (из стр. 08 табл. 1000)', u'F11.2-F11.9;F12.2-F12.9;F13.2H-F13.9H;F14.2-F14.9;F15.2H-F15.9H;F16.2H-F16.9H;F18.2H-F18.9H;F19.2H-F19.9H', u'01'),
    (u'Употребление наркотиков с вредными последствиями (из стр. 16 табл. 1000)', u'F11.1;F12.1;F13.1H;F14.1;F15.1H;F16.1H;F18.1H;F19.1H;', u'02'),
    (u'Потребители инъекционных наркотиков (из стр. 01, 02 табл. 4000)', u'', u'03'),
]

def selectData(params):
    db = QtGui.qApp.db
    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())
    if not endDate:
        endDate = QDate.currentDate()
    if endDate:
        endTime = params.get('endTime', QTime(9, 0, 0, 0))
        begTime = params.get('begTime', QTime(0, 0, 0, 0))
        endDateTime = QDateTime(endDate, endTime)
        if not begDate:
            begTime = begTime if begTime else endTime
            begDateTime = QDateTime(endDate.addDays(-1), begTime)
        else:
            begTime = begTime if begTime else endTime
            begDateTime = QDateTime(begDate, begTime)

    addressType = params.get('addressType', 0)
    addressFunc = 'getClientLocAddressId' if addressType == 1 else 'getClientRegAddressId'
    orgStructureIdList = params.get('orgStructureIdList', None)
    if orgStructureIdList:
        condOrgstruct = 'AND ' + db.table('Person').alias('p')['orgStructure_id'].inlist(orgStructureIdList)
    else:
        condOrgstruct = ''
    forResult = params.get('forResult', -1)
    if forResult == 0:
        addCols = u""", CASE WHEN (SELECT aps.value FROM Action a
            LEFT JOIN ActionType at on at.id = a.actionType_id AND at.deleted = 0
            left JOIN Event e2 ON e2.id = a.event_id AND e2.deleted = 0
            left JOIN ActionPropertyType apt ON apt.actionType_id = at.id AND apt.shortName = 'analizResult' and apt.deleted = 0
            left JOIN ActionProperty ap on ap.action_id = a.id AND ap.type_id = apt.id AND ap.deleted = 0
            left JOIN ActionProperty_String aps on aps.id = ap.id
            WHERE e2.client_id = c.id AND a.deleted = 0 AND at.code = 'B-23y'
            ORDER BY a.endDate DESC LIMIT 1) = 'положительно' THEN 1 else 0 end AS HIV,
        CASE WHEN (SELECT aps.value FROM Action a
            LEFT JOIN ActionType at on at.id = a.actionType_id AND at.deleted = 0
            left JOIN Event e2 ON e2.id = a.event_id AND e2.deleted = 0
            left JOIN ActionPropertyType apt ON apt.actionType_id = at.id AND apt.shortName = 'analizResult' and apt.deleted = 0
            left JOIN ActionProperty ap on ap.action_id = a.id AND ap.type_id = apt.id AND ap.deleted = 0
            left JOIN ActionProperty_String aps on aps.id = ap.id
            WHERE e2.client_id = c.id AND a.deleted = 0 AND at.code = 'Hepatic-B'
            ORDER BY a.endDate DESC LIMIT 1) = 'положительно' THEN 1 else 0 end AS HepaticB,
        CASE WHEN (SELECT aps.value FROM Action a
            LEFT JOIN ActionType at on at.id = a.actionType_id AND at.deleted = 0
            left JOIN Event e2 ON e2.id = a.event_id AND e2.deleted = 0
            left JOIN ActionPropertyType apt ON apt.actionType_id = at.id AND apt.shortName = 'analizResult' and apt.deleted = 0
            left JOIN ActionProperty ap on ap.action_id = a.id AND ap.type_id = apt.id AND ap.deleted = 0
            left JOIN ActionProperty_String aps on aps.id = ap.id
            WHERE e2.client_id = c.id AND a.deleted = 0 AND at.code = 'Hepatic-C'
            ORDER BY a.endDate DESC LIMIT 1) = 'положительно' THEN 1 else 0 end AS HepaticC"""
    elif forResult == 1:
        addCols = u""", CASE WHEN (SELECT cr.researchResult FROM ClientResearch cr
        left JOIN rbClientResearchKind crk ON cr.researchKind_id = crk.id
        WHERE cr.client_id = c.id AND crk.code = 'В-23' AND cr.deleted = 0
        ORDER BY cr.begDate DESC LIMIT 1) = '+' THEN 1 else 0 end AS HIV,
    CASE WHEN (SELECT cr.researchResult FROM ClientResearch cr
        left JOIN rbClientResearchKind crk ON cr.researchKind_id = crk.id
        WHERE cr.client_id = c.id AND crk.code = 'Гепатит "В"' AND cr.deleted = 0
        ORDER BY cr.begDate DESC LIMIT 1) = '+' THEN 1 else 0 end AS HepaticB,
    CASE WHEN (SELECT cr.researchResult FROM ClientResearch cr
        left JOIN rbClientResearchKind crk ON cr.researchKind_id = crk.id
        WHERE cr.client_id = c.id AND crk.code = 'Гепатит "С"' AND cr.deleted = 0
        ORDER BY cr.begDate DESC LIMIT 1) = '+' THEN 1 else 0 end AS HepaticC"""
    else:
        addCols = ''

    stmt = u"""
SELECT t.* 
  FROM (SELECT e.id, 
    IF(d.exSubclassMKB IS NOT NULL, CONCAT(d.MKB, d.exSubclassMKB), d.MKB) AS MKB,
    e.client_id, 
    e.setDate,
    c.sex,
    age(c.birthDate, e.setDate) AS age,
    IFNULL(isAddressVillager((SELECT address_id   FROM ClientAddress  WHERE id = {addressFunc}(c.id))), 0) as isVillager,
    IF(d.setDate BETWEEN {begDate} AND {endDate}, 1, 0) isFirstInLife
    {addCols}
  FROM Event e
  LEFT JOIN Person p ON p.id = e.execPerson_id
  left JOIN Client c on c.id = e.client_id
  left JOIN EventType et ON e.eventType_id = et.id
  left JOIN rbEventTypePurpose etp ON et.purpose_id = etp.id
  LEFT JOIN Diagnosis d on d.id = (SELECT diagnosis_id
  FROM Diagnostic
  INNER JOIN rbDiagnosisType ON rbDiagnosisType.id = diagnosisType_id
  WHERE Diagnostic.event_id = e.id
  AND Diagnostic.deleted = 0
  AND rbDiagnosisType.code = '1'
  )
  WHERE e.deleted = 0
  AND c.deleted = 0
  AND d.deleted = 0
  AND et.code NOT IN ('hospDir','egpuDisp','plng', 'anonim')
  AND et.context NOT LIKE '%relatedAction%' AND et.context NOT LIKE '%inspection%'
  AND et.form NOT IN ('000', '027', '106', '110')
  AND etp.code <> 0
  AND e.setDate BETWEEN {begDate} AND {endDate}
  AND (c.deathDate IS NULL OR c.deathDate BETWEEN {begDate} AND {endDate})
  AND d.MKB >= 'F10' and d.MKB < 'F20' and d.MKB not like 'F17%' AND mod_id is NULL
  {condOrgstruct}) t
GROUP BY t.client_id
ORDER BY t.setDate desc
    """.format(begDate=db.formatDate(begDateTime),
            endDate=db.formatDate(endDateTime),
            addressFunc=addressFunc,
            condOrgstruct=condOrgstruct,
            addCols=addCols)

    return db.query(stmt)


class CForm11SetupDialog(QtGui.QDialog, Ui_Form11SetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())
        self.setOrgStructureVisible()
        self.setAddressTypeVisible()
        self.setForResultVisible(False)
        self.setTypeDNVisible(False)
        self.setChkOnliContingentVisible(False)


    def setOrgStructureVisible(self, value=True):
        self.cmbOrgStructure.setVisible(value)
        self.lblOrgStructure.setVisible(value)
        self.orgStructureVisible = value


    def setForResultVisible(self, value=True):
        self.cmbForResult.setVisible(value)
        self.lblForResult.setVisible(value)
        self.forResultVisible = value


    def setAddressTypeVisible(self, value=True):
        self.cmbAddressType.setVisible(value)
        self.lblAddressType.setVisible(value)
        self.addressTypeVisible = value


    def setTypeDNVisible(self, value=True):
        self.cmbTypeDN.setVisible(value)
        self.lblTypeDN.setVisible(value)
        self.typeDNVisible = value


    def setChkOnliContingentVisible(self, value=True):
        self.chkOnlyContingent.setVisible(value)
        self.chkOnlyContingentVisible = value


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtBegTime.setTime(params.get('begTime', QTime(9, 0, 0, 0)))
        self.edtTimeEdit.setTime(params.get('endTime', QTime(9, 0, 0, 0)))
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.cmbAddressType.setCurrentIndex(params.get('addressType', 0))
        self.cmbForResult.setCurrentIndex(params.get('forResult', 0))
        self.cmbTypeDN.setCurrentIndex(params.get('typeDN', 0))
        self.chkOnlyContingent.setChecked(params.get('isOnlyContingent', 0))


    def params(self):
        def getPureHMTime(time):
            return QTime(time.hour(), time.minute())

        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['begTime'] = getPureHMTime(self.edtBegTime.time())
        result['endDate'] = self.edtEndDate.date()
        result['endTime'] = getPureHMTime(self.edtTimeEdit.time())
        result['orgStructureId'] = self.cmbOrgStructure.value()

        if self.orgStructureVisible:
            orgStructureIdList = []
            if self.cmbOrgStructure.value():
                orgStructureIndex = self.cmbOrgStructure._model.index(
                    self.cmbOrgStructure.currentIndex(), 0,
                    self.cmbOrgStructure.rootModelIndex())
                treeItem = orgStructureIndex.internalPointer() if orgStructureIndex.isValid() else None
                orgStructureIdList = treeItem.getItemIdList() if treeItem else []
            result['orgStructureIdList'] = orgStructureIdList

        if self.addressTypeVisible:
            result['addressType'] = self.cmbAddressType.currentIndex()
        if self.forResultVisible:
            result['forResult'] = self.cmbForResult.currentIndex()
        if self.typeDNVisible:
            result['typeDN'] = self.cmbTypeDN.currentIndex()
        if self.chkOnlyContingentVisible:
            result['isOnlyContingent'] = self.chkOnlyContingent.isChecked()
        return result


class CForm11(CReport):

    def __init__(self, parent):
        CReport.__init__(self, parent)


    def getSetupDialog(self, parent):
        result = CForm11SetupDialog(parent)
        return result


    def dumpParams(self, cursor, params):
        description = []
        endDate = params.get('endDate', QDate())
        begDate = params.get('begDate', QDate())
        if not endDate:
            endDate = QDate.currentDate()
        if endDate:
            endTime = params.get('endTime', QTime(9, 0, 0, 0))
            begTime = params.get('begTime', None)
            endDateTime = QDateTime(endDate, endTime)
            if not begDate:
                begTime = begTime if begTime else endTime
                description.append(u'Текущий день: ' + forceString(QDateTime(endDate, endTime)))
            else:
                begTime = begTime if begTime else endTime
                begDateTime = QDateTime(begDate, begTime)
                if begDateTime.date() or endDateTime.date():
                    description.append(dateRangeAsStr(u'за период', begDateTime, endDateTime))

        orgStructureId = params.get('orgStructureId', None)
        addressType = params.get('addressType', -1)
        forResult = params.get('forResult', -1)

        if orgStructureId:
            description.append(u'подразделение: ' + getOrgStructureFullName(orgStructureId))
        else:
            description.append(u'подразделение: ЛПУ')

        if addressType >= 0:
            description.append(u'адрес: ' + (u'по проживанию' if addressType else u'по регистрации'))
        if forResult >= 0:
            description.append(u'по результату: ' + (u'лабораторного анализа' if not forResult else u'обследования в карте'))

        description.append(u'отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        columns = [('100%', [], CReportBase.AlignLeft)]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


class CForm11_1000(CForm11):
    def __init__(self, parent):
        CForm11.__init__(self, parent)
        self.setTitle(u'Форма N 11 1000')


    def build(self, params):
        mapMainRows = createMapCodeToRowIdx([row[3] for row in MainRows])
        rowSize = 8
        reportMainData = [[0] * rowSize for row in xrange(len(MainRows))]

        query = selectData(params)
        while query.next():
            record = query.record()
            clientAge = forceInt(record.value('age'))
            clientSex = forceInt(record.value('sex'))
            MKB, postfixs = normalizeMKB(forceString(record.value('MKB')))

            cols = [0]
            if clientSex == 2:
                cols.append(1)
            if clientAge >= 0 and clientAge < 15:
                cols.append(2)
            elif clientAge >= 15 and clientAge < 18:
                cols.append(3)
            elif clientAge >= 18 and clientAge < 20:
                cols.append(4)
            elif clientAge >= 20 and clientAge < 40:
                cols.append(5)
            elif clientAge >= 40 and clientAge < 60:
                cols.append(6)
            elif clientAge >= 60:
                cols.append(7)

            rows = []
            for postfix in postfixs:
                rows.extend(mapMainRows.get((MKB, postfix), []))
                while len(MKB[:-1]) > 4:
                    MKB = MKB[:-1]
                    rows.extend(mapMainRows.get((MKB, postfix), []))

            for row in rows:
                reportLine = reportMainData[row]
                for col in cols:
                    reportLine[col] += 1

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Число заболеваний наркологическими расстройствами, зарегистрированных организацией')
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        splitTitle(cursor, u'(1000)', u'Код по ОКЕИ: человек - 792')
        tableColumns = [
            ('32%', [u'Наименование', u'', u'', u'1'], CReportBase.AlignLeft),
            ('2%', [u'№ строки', u'', u'', u'2'], CReportBase.AlignCenter),
            ('10%', [u'Код по МКБ-10', u'', u'', u'3'], CReportBase.AlignCenter),
            ('7%', [u'Зарегистрировано заболеваний в течение года:', u'всего', u'', u'4'], CReportBase.AlignRight),
            ('7%', [u'', u'из них - женщин', u'', u'5'], CReportBase.AlignRight),
            ('7%', [u'', u'в том числе в возрасте (из гр. 4):', u'0 - 14 лет', u'6'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'15 - 17 лет', u'7'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'18 - 19 лет', u'8'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'20 - 39 лет', u'9'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'40 - 59 лет', u'10'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'60 лет и старше', u'11'], CReportBase.AlignRight)
        ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 3, 1)  # Наименование
        table.mergeCells(0, 1, 3, 1)  # № стр.
        table.mergeCells(0, 2, 3, 1)  # Код МКБ
        table.mergeCells(0, 3, 1, 8)  # зарег
        table.mergeCells(1, 3, 2, 1)  # Всего
        table.mergeCells(1, 4, 2, 1)  # Всего
        table.mergeCells(1, 5, 1, 6)  # Всего
        table.mergeCells(0, 11, 2, 2)  # Всего

        t = QtGui.QTextBlockFormat()
        for row, rowDescr in enumerate(MainRows):
            reportLine = reportMainData[row]
            i = table.addRow()
            t.setLeftMargin(rowDescr[0] * 10)
            table.setText(i, 0, rowDescr[1], blockFormat=t)
            table.setText(i, 1, rowDescr[4])
            table.setText(i, 2, rowDescr[2])
            for col in xrange(rowSize):
                table.setText(i, 3 + col, reportLine[col])

        # продолжение
        reportMainData = [[0] * rowSize for row in xrange(len(MainRows))]

        query.setForwardOnly(False)
        query.first()
        while query.next():
            record = query.record()
            clientAge = forceInt(record.value('age'))
            clientSex = forceInt(record.value('sex'))
            MKB, postfixs = normalizeMKB(forceString(record.value('MKB')))
            isVillager = forceBool(record.value('isVillager'))
            cols = []
            if isVillager:
                cols.append(0)
                if clientSex == 2:
                    cols.append(1)
                if clientAge >= 0 and clientAge < 15:
                    cols.append(2)
                elif clientAge >= 15 and clientAge < 18:
                    cols.append(3)
                elif clientAge >= 18 and clientAge < 20:
                    cols.append(4)
                elif clientAge >= 20 and clientAge < 40:
                    cols.append(5)
                elif clientAge >= 40 and clientAge < 60:
                    cols.append(6)
                elif clientAge >= 60:
                    cols.append(7)

                rows = []
                for postfix in postfixs:
                    rows.extend(mapMainRows.get((MKB, postfix), []))
                    while len(MKB[:-1]) > 4:
                        MKB = MKB[:-1]
                        rows.extend(mapMainRows.get((MKB, postfix), []))
                for row in rows:
                    reportLine = reportMainData[row]
                    for col in cols:
                        reportLine[col] += 1

        splitTitle(cursor, u'', u'Продолжение')
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Число заболеваний наркологическими расстройствами, зарегистрированных организацией')
        cursor.insertBlock()
        splitTitle(cursor, u'(1000)', u'Код по ОКЕИ: человек - 792')
        tableColumns = [
            ('32%', [u'Наименование', u'', u'', u'1'], CReportBase.AlignLeft),
            ('2%', [u'№ строки', u'', u'', u'2'], CReportBase.AlignCenter),
            ('10%', [u'Код по МКБ-10', u'', u'', u'3'], CReportBase.AlignCenter),
            ('7%', [u'Из общего числа пациентов (гр. 4) - сельских жителей:', u'всего', u'', u'12'], CReportBase.AlignRight),
            ('7%', [u'', u'из них - женщин', u'', u'13'], CReportBase.AlignRight),
            ('7%', [u'', u'в том числе в возрасте (из гр. 12):', u'0 - 14 лет', u'14'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'15 - 17 лет', u'15'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'18 - 19 лет', u'16'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'20 - 39 лет', u'17'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'40 - 59 лет', u'18'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'60 лет и старше', u'19'], CReportBase.AlignRight)
        ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 3, 1)  # Наименование
        table.mergeCells(0, 1, 3, 1)  # № стр.
        table.mergeCells(0, 2, 3, 1)  # Код МКБ
        table.mergeCells(0, 3, 1, 8)  # зарег
        table.mergeCells(1, 3, 2, 1)  # Всего
        table.mergeCells(1, 4, 2, 1)  # Всего
        table.mergeCells(1, 5, 1, 6)  # Всего
        table.mergeCells(0, 11, 2, 2)  # Всего

        t = QtGui.QTextBlockFormat()
        for row, rowDescr in enumerate(MainRows):
            reportLine = reportMainData[row]
            i = table.addRow()
            t.setLeftMargin(rowDescr[0] * 10)
            table.setText(i, 0, rowDescr[1], blockFormat=t)
            table.setText(i, 1, rowDescr[4])
            table.setText(i, 2, rowDescr[2])
            for col in xrange(rowSize):
                table.setText(i, 3 + col, reportLine[col])

        return doc


class CForm11_2000(CForm11):
    def __init__(self, parent):
        CForm11.__init__(self, parent)
        self.setTitle(u'Форма N 11 2000')


    def build(self, params):
        mapMainRows = createMapCodeToRowIdx([row[3] for row in MainRows])
        rowSize = 8
        reportMainData = [[0] * rowSize for row in xrange(len(MainRows))]

        query = selectData(params)
        while query.next():
            record = query.record()
            clientAge = forceInt(record.value('age'))
            clientSex = forceInt(record.value('sex'))
            MKB, postfixs = normalizeMKB(forceString(record.value('MKB')))
            isFirstInLife = forceBool(record.value('isFirstInLife'))

            if isFirstInLife:
                cols = [0]
                if clientSex == 2:
                    cols.append(1)
                if clientAge >= 0 and clientAge < 15:
                    cols.append(2)
                elif clientAge >= 15 and clientAge < 18:
                    cols.append(3)
                elif clientAge >= 18 and clientAge < 20:
                    cols.append(4)
                elif clientAge >= 20 and clientAge < 40:
                    cols.append(5)
                elif clientAge >= 40 and clientAge < 60:
                    cols.append(6)
                elif clientAge >= 60:
                    cols.append(7)

                rows = []
                for postfix in postfixs:
                    rows.extend(mapMainRows.get((MKB, postfix), []))
                    while len(MKB[:-1]) > 4:
                        MKB = MKB[:-1]
                        rows.extend(mapMainRows.get((MKB, postfix), []))

                for row in rows:
                    reportLine = reportMainData[row]
                    for col in cols:
                        reportLine[col] += 1

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Число заболеваний наркологическими расстройствами, зарегистрированных организацией впервые в жизни')
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        splitTitle(cursor, u'(2000)', u'Код по ОКЕИ: человек - 792')
        tableColumns = [
            ('32%', [u'Наименование', u'', u'', u'1'], CReportBase.AlignLeft),
            ('2%', [u'№ строки', u'', u'', u'2'], CReportBase.AlignCenter),
            ('10%', [u'Код по МКБ-10', u'', u'', u'3'], CReportBase.AlignCenter),
            ('7%', [u'Из общего числа пациентов (гр. 4 т. 1000) - с диагнозом, установленным впервые в жизни:', u'всего', u'', u'4'], CReportBase.AlignRight),
            ('7%', [u'', u'из них - женщин', u'', u'5'], CReportBase.AlignRight),
            ('7%', [u'', u'в том числе в возрасте (из гр. 4):', u'0 - 14 лет', u'6'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'15 - 17 лет', u'7'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'18 - 19 лет', u'8'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'20 - 39 лет', u'9'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'40 - 59 лет', u'10'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'60 лет и старше', u'11'], CReportBase.AlignRight)
        ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 3, 1)  # Наименование
        table.mergeCells(0, 1, 3, 1)  # № стр.
        table.mergeCells(0, 2, 3, 1)  # Код МКБ
        table.mergeCells(0, 3, 1, 8)  # зарег
        table.mergeCells(1, 3, 2, 1)  # Всего
        table.mergeCells(1, 4, 2, 1)  # Всего
        table.mergeCells(1, 5, 1, 6)  # Всего
        table.mergeCells(0, 11, 2, 2)  # Всего

        t = QtGui.QTextBlockFormat()
        for row, rowDescr in enumerate(MainRows):
            reportLine = reportMainData[row]
            i = table.addRow()
            t.setLeftMargin(rowDescr[0] * 10)
            table.setText(i, 0, rowDescr[1], blockFormat=t)
            table.setText(i, 1, rowDescr[4])
            table.setText(i, 2, rowDescr[2])
            for col in xrange(rowSize):
                table.setText(i, 3 + col, reportLine[col])

        # продолжение
        reportMainData = [[0] * rowSize for row in xrange(len(MainRows))]

        query.setForwardOnly(False)
        query.first()
        while query.next():
            record = query.record()
            clientAge = forceInt(record.value('age'))
            clientSex = forceInt(record.value('sex'))
            MKB, postfixs = normalizeMKB(forceString(record.value('MKB')))
            isVillager = forceBool(record.value('isVillager'))
            isFirstInLife = forceBool(record.value('isFirstInLife'))

            if isVillager and isFirstInLife:
                cols = [0]
                if clientSex == 2:
                    cols.append(1)
                if clientAge >= 0 and clientAge < 15:
                    cols.append(2)
                elif clientAge >= 15 and clientAge < 18:
                    cols.append(3)
                elif clientAge >= 18 and clientAge < 20:
                    cols.append(4)
                elif clientAge >= 20 and clientAge < 40:
                    cols.append(5)
                elif clientAge >= 40 and clientAge < 60:
                    cols.append(6)
                elif clientAge >= 60:
                    cols.append(7)

                rows = []
                for postfix in postfixs:
                    rows.extend(mapMainRows.get((MKB, postfix), []))
                    while len(MKB[:-1]) > 4:
                        MKB = MKB[:-1]
                        rows.extend(mapMainRows.get((MKB, postfix), []))
                for row in rows:
                    reportLine = reportMainData[row]
                    for col in cols:
                        reportLine[col] += 1

        splitTitle(cursor, u'', u'Продолжение')
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Число заболеваний наркологическими расстройствами, зарегистрированных организацией впервые в жизни')
        cursor.insertBlock()
        splitTitle(cursor, u'(2000)', u'Код по ОКЕИ: человек - 792')
        tableColumns = [
            ('32%', [u'Наименование', u'', u'', u'1'], CReportBase.AlignLeft),
            ('2%', [u'№ строки', u'', u'', u'2'], CReportBase.AlignCenter),
            ('10%', [u'Код по МКБ-10', u'', u'', u'3'], CReportBase.AlignCenter),
            ('7%', [u'Из числа пациентов с впервые в жизни установленным диагнозом (гр. 4) - сельских жителей:', u'всего', u'', u'12'], CReportBase.AlignRight),
            ('7%', [u'', u'из них - женщин', u'', u'13'], CReportBase.AlignRight),
            ('7%', [u'', u'в том числе в возрасте (из гр. 12):', u'0 - 14 лет', u'14'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'15 - 17 лет', u'15'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'18 - 19 лет', u'16'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'20 - 39 лет', u'17'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'40 - 59 лет', u'18'], CReportBase.AlignRight),
            ('7%', [u'', u'', u'60 лет и старше', u'19'], CReportBase.AlignRight)
        ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 3, 1)  # Наименование
        table.mergeCells(0, 1, 3, 1)  # № стр.
        table.mergeCells(0, 2, 3, 1)  # Код МКБ
        table.mergeCells(0, 3, 1, 8)  # зарег
        table.mergeCells(1, 3, 2, 1)  # Всего
        table.mergeCells(1, 4, 2, 1)  # Всего
        table.mergeCells(1, 5, 1, 6)  # Всего
        table.mergeCells(0, 11, 2, 2)  # Всего

        t = QtGui.QTextBlockFormat()
        for row, rowDescr in enumerate(MainRows):
            reportLine = reportMainData[row]
            i = table.addRow()
            t.setLeftMargin(rowDescr[0] * 10)
            table.setText(i, 0, rowDescr[1], blockFormat=t)
            table.setText(i, 1, rowDescr[4])
            table.setText(i, 2, rowDescr[2])
            for col in xrange(rowSize):
                table.setText(i, 3 + col, reportLine[col])

        return doc


class CForm11_4000(CForm11):
    def __init__(self, parent):
        CForm11.__init__(self, parent)
        self.setTitle(u'Форма N 11 4000')


    def getSetupDialog(self, parent):
        result = CForm11.getSetupDialog(self, parent)
        result.setAddressTypeVisible(False)
        result.setForResultVisible(True)
        return result


    def build(self, params):
        mapMainRows = createMapCodeToRowIdx([row[1] for row in CompRows])
        rowSize = 6
        reportMainData = [[0] * rowSize for row in xrange(len(CompRows))]

        query = selectData(params)
        while query.next():
            record = query.record()
            clientAge = forceInt(record.value('age'))
            MKB, postfixs = normalizeMKB(forceString(record.value('MKB')))
            HIV = forceBool(record.value('HIV'))
            HepaticB = forceBool(record.value('HepaticB'))
            HepaticC = forceBool(record.value('HepaticC'))
            cols = []
            if HIV:
                cols.append(0)
                if clientAge >= 15 and clientAge < 18:
                    cols.append(1)
            if HepaticB:
                cols.append(2)
                if clientAge >= 15 and clientAge < 18:
                    cols.append(3)
            if HepaticC:
                cols.append(4)
                if clientAge >= 15 and clientAge < 18:
                    cols.append(5)

            rows = []
            for postfix in postfixs:
                rows.extend(mapMainRows.get((MKB, postfix), []))
                while len(MKB[:-1]) > 4:
                    MKB = MKB[:-1]
                    rows.extend(mapMainRows.get((MKB, postfix), []))

            for row in rows:
                reportLine = reportMainData[row]
                for col in cols:
                    reportLine[col] += 1

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Обследование зарегистрированных пациентов на наличие гемоконтактных инфекций')
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        splitTitle(cursor, u'(4000)', u'Код по ОКЕИ: человек - 792')
        tableColumns = [
            ('38%', [u'Наименование', u'', u'', u'1'], CReportBase.AlignLeft),
            ('2%', [u'№ стр.', u'', u'', u'2'], CReportBase.AlignCenter),
            ('10%', [u'Из общего числа зарегистрированных пациентов (табл. 1000) имеют позитивный статус:', u'по ВИЧ-инфекции', u'всего\n(из гр. 4)', u'3'], CReportBase.AlignRight),
            ('10%', [u'', u'', u'детей 15 - 17 лет\n(из гр. 7)', u'4'], CReportBase.AlignRight),
            ('10%', [u'', u'по гепатиту C', u'всего\n(из гр. 4)', u'5'], CReportBase.AlignRight),
            ('10%', [u'', u'', u'детей 15 - 17 лет\n(из гр. 7)', u'6'], CReportBase.AlignRight),
            ('10%', [u'', u'по гепатиту B', u'всего\n(из гр. 4)', u'7'], CReportBase.AlignRight),
            ('10%', [u'', u'', u'детей 15 - 17 лет\n(из гр. 7)', u'8'], CReportBase.AlignRight)
        ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 3, 1)  # Наименование
        table.mergeCells(0, 1, 3, 1)  # № стр.
        table.mergeCells(0, 2, 1, 6)  # из общего числа
        table.mergeCells(1, 2, 1, 2)  # по вич
        table.mergeCells(1, 4, 1, 2)  # по геп С
        table.mergeCells(1, 6, 1, 2)  # по геп В

        for row, rowDescr in enumerate(CompRows):
            reportLine = reportMainData[row]
            i = table.addRow()
            table.setText(i, 0, rowDescr[0])
            table.setText(i, 1, rowDescr[2])
            for col in xrange(rowSize):
                table.setText(i, 2 + col, reportLine[col])
        return doc


def normalizeMKB(mkb):
    postfixs = ['']
    if mkb[-1] in [u'Н', u'Т']:
        postfixs.append(mkb[-1].replace(u'Н', 'H').replace(u'Т', 'T'))
        mkb = mkb[:-1]
    if len(mkb) == 3:
        mkb = mkb + '.0'

    return mkb, postfixs


def addCodesRange(rowIdx, lowCode, highCode, postfix, mapCodesToRowIdx):
    def convCodeToNumberSub(code):
        r = (ord(code[0]) - ordA)
        r = r * 10 + (ord(code[1]) - ord0)
        r = r * 10 + (ord(code[2]) - ord0)
        r = r * 10 + (ord(code[4]) - ord0)
        r = r * 10 + (ord(code[5]) - ord0)
        return r

    def convNumberToCodeSub(num):
        return '%c%c%c.%c%c' % (num / 10000 + ordA,
                                (num / 1000) % 10 + ord0,
                                (num / 100) % 10 + ord0,
                                (num / 10) % 10 + ord0,
                                (num) % 10 + ord0)

    def convCodeToNumberSub7(code):
        r = (ord(code[0]) - ordA)
        r = r * 10 + (ord(code[1]) - ord0)
        r = r * 10 + (ord(code[2]) - ord0)
        r = r * 10 + (ord(code[4]) - ord0)
        r = r * 10 + (ord(code[5]) - ord0)
        r = r * 10 + (ord(code[6]) - ord0)
        return r

    def convNumberToCodeSub7(num):
        return '%c%c%c.%c%c%c' % (num / 100000 + ordA,
                                (num / 10000) % 10 + ord0,
                                (num / 1000) % 10 + ord0,
                                (num / 100) % 10 + ord0,
                                (num / 10) % 10 + ord0,
                                (num) % 10 + ord0)

    def convCodeToNumber(code):
        r = (ord(code[0]) - ordA)
        r = r * 10 + (ord(code[1]) - ord0)
        r = r * 10 + (ord(code[2]) - ord0)
        r = r * 10 + (ord(code[4]) - ord0)
        return r

    def convNumberToCode(num):
        return '%c%c%c.%c' % (num / 1000 + ordA,
                              (num / 100) % 10 + ord0,
                              (num / 10) % 10 + ord0,
                              (num) % 10 + ord0)

    #        return chr(num/2600+ordA)+chr((num/100)%10+ord0)+chr((num/10)%10+ord0)+'.'+chr((num)%10+ord0)

    assert lowCode <= highCode

    #    if re.match('^[A-Z][0-9][0-9]$', lowCode) is not None:
    if threeChar.match(lowCode):
        lowCode = lowCode + '.0'
    #    if re.match('^[A-Z][0-9][0-9]$', highCode) is not None:
    if threeChar.match(highCode):
        highCode = highCode + '.9'

    if len(lowCode) == 6:
        low = convCodeToNumberSub(lowCode)
        high = convCodeToNumberSub(highCode)
    elif len(lowCode) == 7:
        low = convCodeToNumberSub7(lowCode)
        high = convCodeToNumberSub7(highCode)
    else:
        low = convCodeToNumber(lowCode)
        high = convCodeToNumber(highCode)
    for i in xrange(low, high + 1):
        if len(lowCode) == 6:
            code = convNumberToCodeSub(i)
        elif len(lowCode) == 7:
            code = convNumberToCodeSub7(i)
        else:
            code = convNumberToCode(i)
        mapCodesToRowIdx.setdefault((code, postfix), []).append(rowIdx)


def parseRowCodes(rowIdx, codes, mapCodesToRowIdx):
    diagRanges = codes.split(';')
    for tempDiagRange in diagRanges:
        tempDiagLimits = tempDiagRange.split('-')
        n = len(tempDiagLimits)
        if n == 1 and tempDiagLimits[0] and 'x' in tempDiagLimits[0]:
            pos = tempDiagLimits[0].find('x')
            xRanges = tempDiagLimits[:]
            while pos > -1:
                for item in xRanges:
                    pos = item.find('x')
                    if pos > -1:
                        for i in range(10):
                            xRanges.append(item.replace('x', str(i), 1))
                        xRanges.remove(item)
                pos = xRanges[0].find('x')
            diagRanges.remove(tempDiagLimits[0])
            diagRanges.extend(xRanges)

    prefix = ''
    for diagRange in diagRanges:
        diagSets = diagRange.split(',')
        if len(diagSets) > 1:
            for i, d in enumerate(diagSets):
                diagLimits = d.split('-')
                n = len(diagLimits)
                if i == 0:
                    tmp = diagLimits[0].split('.')[0]
                if n == 1 and diagLimits[0]:
                    tmpCode = diagLimits[0] if i==0 else '.'.join([tmp.strip(), diagLimits[0].strip()])
                    prefix, code, postfix = normalizeCode(prefix, tmpCode)
                    addCode(rowIdx, code, postfix, mapCodesToRowIdx)
                elif n == 2:
                    tmpCode = diagLimits[0] if i == 0 else '.'.join([tmp.strip(), diagLimits[0].strip()])
                    tmpCode2 = diagLimits[1] if i == 0 else '.'.join([tmp.strip(), diagLimits[1].strip()])
                    prefix, lowCode, lowPostfix = normalizeCode(prefix, tmpCode)
                    prefix, highCode, highPostfix = normalizeCode(prefix, tmpCode2)
                    addCodesRange(rowIdx, lowCode, highCode, postfix, mapCodesToRowIdx)
                else:
                    assert False, 'Wrong codes range "' + diagRange + '"'
        else:
            diagLimits = diagRange.split('-')
            n = len(diagLimits)
            if n == 1 and diagLimits[0]:
                prefix, code, postfix = normalizeCode(prefix, diagLimits[0])
                addCode(rowIdx, code, postfix, mapCodesToRowIdx)
            elif n == 2:
                prefix, lowCode, postfix = normalizeCode(prefix, diagLimits[0])
                prefix, highCode, highPostfix = normalizeCode(prefix, diagLimits[1])
                addCodesRange(rowIdx, lowCode, highCode, postfix, mapCodesToRowIdx)
            else:
                # assert False, 'Wrong codes range "' + diagRange + '"'
                pass


def normalizeCode(prefix, code):
    code = code.strip().upper()
    postfix = ''
    if code[-1] in ['H', 'T']:
        postfix = code[-1]
        code = code[:-1]

    #    if re.match('^[A-Z]', code) is not None:
    if startChar.match(code):
        codeParts = code.split('.')
        prefix = codeParts[0]
    else:
        assert prefix
        code = prefix + '.' + code
    #    assert  re.match('^[A-Z][0-9][0-9](\.[0-9])?$', code) is not None

    if len(code) == 6:
        assert sixChar.match(code) is not None
    elif len(code) == 7:
        assert sevenChar.match(code) is not None
    elif len(code) == 8:
        assert eightChar.match(code) is not None
    elif len(code) == 9:
        assert nineChar.match(code) is not None
    else:
        assert threeOrFourChar.match(code) is not None
    return prefix, code, postfix


def addCode(rowIdx, code, postfix, mapCodesToRowIdx):
    #    if re.match('^[A-Z][0-9][0-9]\.[0-9]', code) is not None:
    if fourChar.match(code):
        mapCodesToRowIdx.setdefault((code, postfix), []).append(rowIdx)
    #    elif re.match('^[A-Z][0-9][0-9]$', code) is not None:
    elif threeChar.match(code):
        addCodesRange(rowIdx, code, code, postfix, mapCodesToRowIdx)
    else:
        mapCodesToRowIdx.setdefault((code, postfix), []).append(rowIdx)


def createMapCodeToRowIdx(codesList):
    mapCodeToRowIdx = {}
    for rowIdx, code in enumerate(codesList):
        if code:
            parseRowCodes(rowIdx, str(code), mapCodeToRowIdx)
    return mapCodeToRowIdx