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

from library.Utils             import forceBool, forceInt, forceRef, forceString, lastYearDay
from library.MapCode           import createMapCodeToRowIdx
from Reports.Report            import CReport, normalizeMKB
from Reports.ReportBase        import CReportBase, createTable
from Reports.ReportSetupDialog import CReportSetupDialog
from Reports.Utils             import getAgeClass
from Orgs.Utils                import getOrgStructurePersonIdList



MainRows = [
    (u'Некоторые инфекционные и паразитарные болезни',u'1',u'A00-B99'),
    (u'в том числе: туберкулез',u'1.1',u'A15-A19'),
    (u'Новообразования',u'2',u'C00-D48'),
    (u'в том числе: злокачественные новообразования и новообразования in situ',u'2.1',u'C00-D09'),
    (u'в том числе: пищевода',u'2.2',u'C15, D00.1'),
    (u'из них в 1-2 стадии',u'2.2.1', u''),
    (u'желудка',u'2.3',u'C16, D00.2'),
    (u'из них в 1-2 стадии',u'2.3.1', u''),
    (u'ободочной кишки',u'2.4.',u'C18, D01.0'),
    (u'из них в 1-2 стадии',u'2.4.1', u''),
    (u'ректосигмоидного соединения, прямой кишки, заднего прохода (ануса) и анального канала',u'2.5',u'C19-C21, D01.1-D01.3'),
    (u'из них в 1-2 стадии',u'2.5.1', u''),
    (u'поджелудочной железы',u'2.6',u'C25'),
    (u'из них в 1-2 стадии',u'2.6.1', u''),
    (u'трахеи, бронхов и легкого',u'2.7',u'C33, C34, D02.1-D02.2'),
    (u'из них в 1-2 стадии',u'2.7.1', u''),
    (u'молочной железы',u'2.8',u'C50, D05'),
    (u'из них в 1-2 стадии',u'2.8.1', u''),
    (u'шейки матки',u'2.9.',u'C53, D06'),
    (u'из них в 1-2 стадии',u'2.9.1', u''),
    (u'тела матки',u'2.10',u'C54'),
    (u'из них в 1-2 стадии',u'2.10.1', u''),
    (u'яичника',u'2.11',u'C56'),
    (u'из них в 1-2 стадии',u'2.11.1', u''),
    (u'предстательной железы',u'2.12',u'C61, D07.5'),
    (u'из них в 1-2 стадии',u'2.12.1', u''),
    (u'почки, кроме почечной лоханки',u'2.13',u'C64'),
    (u'из них в 1-2 стадии',u'2.13.1', u''),
    (u'Болезни крови, кроветворных органов и отдельные нарушения, вовлекающие иммунный механизм',u'3',u'D50-D89'),
    (u'в том числе: анемии, связанные с питанием, гемолитические анемии, апластические и другие анемии',u'3.1',u'D50-D64'),
    (u'Болезни эндокринной системы, расстройства питания и нарушения обмена веществ',u'4',u'E00-E90'),
    (u'в том числе: сахарный диабет',u'4.1',u'E10-E14'),
    (u'ожирение',u'4.2',u'E66'),
    (u'нарушения обмена липопротеинов и другие липидемии',u'4.3',u'E78'),
    (u'Болезни нервной системы',u'5',u'G00-G99'),
    (u'в том числе: преходящие церебральные ишемические приступы [атаки] и родственные синдромы',u'5.1',u'G45'),
    (u'Болезни глаза и его придаточного аппарата',u'6',u'H00-H59'),
    (u'в том числе: старческая катаракта и другие катаракты',u'6.1',u'H25, H26'),
    (u'глаукома',u'6.2',u'H40'),
    (u'слепота и пониженное зрение',u'6.3',u'H54'),
    (u'Болезни системы кровообращения',u'7',u'I00-I99'),
    (u'в том числе: болезни, характеризующиеся повышенным кровяным давлением',u'7.1',u'I10-I15'),
    (u'ишемическая болезнь сердца',u'7.2',u'I20-I25'),
    (u'в том числе: стенокардия (грудная жаба)',u'7.2.1',u'I20'),
    (u'в том числе нестабильная стенокардия',u'7.2.2',u'I20.0'),
    (u'хроническая ишемическая болезнь сердца',u'7.2.3',u'I25'),
    (u'в том числе: перенесенный в прошлом инфаркт миокарда',u'7.2.4',u'I25.2'),
    (u'другие болезни сердца',u'7.3',u'I30-I52'),
    (u'цереброваскулярные болезни',u'7.4',u'I60-I69'),
    (u'в том числе: закупорка и стеноз прецеребральных артерий, не приводящие к инфаркту мозга и закупорка и стеноз церебральных артерий, не приводящие к инфаркту мозга',u'7.4.1',u'I65, I66'),
    (u'другие цереброваскулярные болезни',u'7.4.2',u'I67'),
    (u'последствия субарахноидального кровоизлияния, последствия внутричерепного кровоизлияния, последствия другого нетравматического внутричерепного кровоизлияния, последствия инфаркта мозга, последствия инсульта, не уточненные как кровоизлияние или инфаркт мозга',u'7.4.3',u'I69.0-I69.4'),
    (u'аневризма брюшной аорты',u'7.4.4',u'I71.3-I71.4'),
    (u'Болезни органов дыхания',u'8',u'J00-J98'),
    (u'в том числе: вирусная пневмония, пневмония, вызванная Streptococcus pneumonia, пневмония, вызванная Haemophilus influenza, бактериальная пневмония, пневмония, вызванная другими инфекционными возбудителями, пневмония при болезнях, классифицированных в других рубриках, пневмония без уточнения возбудителя',u'8.1',u'J12-J18'),
    (u'бронхит, не уточненный как острый и хронический, простой и слизисто-гнойный хронический бронхит, хронический бронхит неуточненный, эмфизема',u'8.2',u'J40-J43'),
    (u'другая хроническая обструктивная легочная болезнь, астма, астматический статус, бронхоэктатическая болезнь',u'8.3',u'J44-J47'),
    (u'Болезни органов пищеварения',u'9',u'K00-K93'),
    (u'в том числе: язва желудка, язва двенадцатиперстной кишки',u'9.1',u'K25, K26'),
    (u'гастрит и дуоденит',u'9.2',u'K29'),
    (u'неинфекционный энтерит и колит',u'9.3',u'K50-K52'),
    (u'другие болезни кишечника',u'9.4',u'K55-K63'),
    (u'Болезни мочеполовой системы',u'10',u'N00-N99'),
    (u'в том числе: гиперплазия предстательной железы, воспалительные болезни предстательной железы, другие болезни предстательной железы',u'10.1',u'N40-N42'),
    (u'доброкачественная дисплазия молочной железы',u'10.2',u'N60'),
    (u'воспалительные болезни женских тазовых органов',u'10.3',u'N70-N77'),
    (u'Прочие заболевания',u'11', u''),
    (u'ИТОГО заболеваний',u'12',u'A00-T98'),
]

def selectData(params, showSuspicion, onlyPrimary):
    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())
    orgStructureId = params.get('orgStructureId', None)
    db = QtGui.qApp.db
    mesDispansIdList = params.get('mesDispansIdList', [])
    if mesDispansIdList:
        mesDispans = u''' AND Event.MES_id IN (%s)'''%(u','.join(forceString(mesId) for mesId in mesDispansIdList if mesId))
    else:
        mesDispans = u''
    suspicionPhaseId = forceRef(db.translate('rbDiseasePhases', 'code', '10', 'id'))
    if showSuspicion:
        if suspicionPhaseId:
            suspicionCond = 'Diagnostic.phase_id=%d' % suspicionPhaseId
        else:
            suspicionCond = '0'
    else:
        if suspicionPhaseId:
            suspicionCond = '(Diagnostic.phase_id!=%d OR Diagnostic.phase_id IS NULL)' % suspicionPhaseId
        else:
            suspicionCond = '1'

    if onlyPrimary:
        primaryCond = 'rbDiseaseCharacter.code IN (\'1\',\'2\')' +\
                      ' AND Diagnosis.setDate BETWEEN %(begDate)s AND %(endDate)s ' % {
                        'begDate':     db.formatDate(begDate),
                        'endDate':     db.formatDate(endDate),
                      }

    else:
        primaryCond = '1'
    orgStructure = u''
    if orgStructureId:
        personIdList = getOrgStructurePersonIdList(orgStructureId)
        if personIdList:
            orgStructure = u''' AND Event.execPerson_id IN (%s)'''%(u','.join(str(personId) for personId in personIdList if personId))
    stmt = u'''
SELECT
    Client.sex AS clientSex,
    age(Client.birthDate, %(endYearDate)s) AS clientAge,
    Diagnosis.MKB,
    EXISTS(SELECT 1
           FROM
           Diagnostic AS D
           LEFT JOIN rbDispanser ON rbDispanser.id = D.dispanser_id
           WHERE D.diagnosis_id = Diagnosis.id
             AND D.deleted = 0
             AND rbDispanser.code IN ('1', '2', '6')
          ) AS isObserved

FROM Event
INNER JOIN mes.MES ON mes.MES.id=Event.MES_id
INNER JOIN mes.mrbMESGroup ON mes.mrbMESGroup.id=mes.MES.group_id
INNER JOIN Client ON Client.id=Event.client_id
INNER JOIN Diagnostic ON Diagnostic.event_id=Event.id
INNER JOIN Diagnosis ON Diagnosis.id=Diagnostic.diagnosis_id
INNER JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id=Diagnostic.character_id
WHERE Event.deleted=0
  %(orgStructure)s
  AND (DATE(Event.execDate) BETWEEN %(begDate)s AND %(endDate)s)
  %(mesDispans)s
  AND mes.mrbMESGroup.code='ДиспанС'
  AND (mes.MES.endDate IS NULL OR mes.MES.endDate >= %(begDate)s)
  AND Diagnostic.deleted = 0
  AND Diagnosis.deleted = 0
  AND %(suspicionCond)s
  AND %(primaryCond)s
GROUP BY Diagnosis.id''' % {
    'orgStructure':orgStructure,
    'begDate':     db.formatDate(begDate),
    'endDate':     db.formatDate(endDate),
    'endYearDate': db.formatDate(lastYearDay(endDate)),
    'suspicionCond':suspicionCond,
    'primaryCond': primaryCond,
    'mesDispans' : mesDispans,
                           }
    return db.query(stmt)


def selectData6000(params, showSuspicion=False, onlyPrimary=False):
    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())
    orgStructureId = params.get('orgStructureId', None)
    db = QtGui.qApp.db
    mesDispansIdList = params.get('mesDispansIdList', [])
    if mesDispansIdList:
        mesDispans = u''' AND Event.MES_id IN (%s)'''%(u','.join(forceString(mesId) for mesId in mesDispansIdList if mesId))
    else:
        mesDispans = u''
    suspicionPhaseId = forceRef(db.translate('rbDiseasePhases', 'code', '10', 'id'))
    if showSuspicion:
        if suspicionPhaseId:
            suspicionCond = 'Diagnostic.phase_id=%d' % suspicionPhaseId
        else:
            suspicionCond = '0'
    else:
        if suspicionPhaseId:
            suspicionCond = '(Diagnostic.phase_id!=%d OR Diagnostic.phase_id IS NULL)' % suspicionPhaseId
        else:
            suspicionCond = '1'

    if onlyPrimary:
        primaryCond = 'rbDiseaseCharacter.code IN (\'1\',\'2\')' +\
                      ' AND Diagnosis.setDate BETWEEN %(begDate)s AND %(endDate)s ' % {
                        'begDate':     db.formatDate(begDate),
                        'endDate':     db.formatDate(endDate),
                      }

    else:
        primaryCond = '1'
    orgStructure = u''
    if orgStructureId:
        personIdList = getOrgStructurePersonIdList(orgStructureId)
        if personIdList:
            orgStructure = u''' AND Event.execPerson_id IN (%s)'''%(u','.join(str(personId) for personId in personIdList if personId))
    stmt = u'''
SELECT
    Client.sex AS clientSex,
    age(Client.birthDate, %(endYearDate)s) AS clientAge,
    Diagnosis.MKB,
    EXISTS(SELECT DP.id
    FROM Diagnostic AS D
    INNER JOIN rbDiseasePhases AS DP ON DP.id = D.phase_id
    WHERE D.event_id = Event.id
    AND D.deleted = 0
    AND DP.code = '10') AS isPhasesAdditionDispans,
    EXISTS(SELECT rbDiagnosticResult.id
    FROM Diagnostic AS D
    INNER JOIN rbDiagnosticResult ON rbDiagnosticResult.id = D.result_id
    WHERE D.event_id = Event.id
    AND D.deleted = 0
    AND rbDiagnosticResult.code = '07') AS isResultAdditionDispans,
    EXISTS(SELECT 1
           FROM
           Diagnostic AS D
           LEFT JOIN rbDispanser ON rbDispanser.id = D.dispanser_id
           WHERE D.diagnosis_id = Diagnosis.id
             AND D.deleted = 0
             AND rbDispanser.code IN ('1', '2', '6')
          ) AS isObserved

FROM Event
INNER JOIN mes.MES ON mes.MES.id=Event.MES_id
INNER JOIN mes.mrbMESGroup ON mes.mrbMESGroup.id=mes.MES.group_id
INNER JOIN Client ON Client.id=Event.client_id
INNER JOIN Diagnostic ON Diagnostic.event_id=Event.id
INNER JOIN Diagnosis ON Diagnosis.id=Diagnostic.diagnosis_id
INNER JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id=Diagnostic.character_id
WHERE Event.deleted=0
  %(orgStructure)s
  AND (DATE(Event.execDate) BETWEEN %(begDate)s AND %(endDate)s)
  %(mesDispans)s
  AND mes.mrbMESGroup.code='ДиспанС'
  AND (mes.MES.endDate IS NULL OR mes.MES.endDate >= %(begDate)s)
  AND Diagnostic.deleted = 0
  AND Diagnosis.deleted = 0
  AND %(suspicionCond)s
  AND %(primaryCond)s
GROUP BY Diagnosis.id''' % {
    'orgStructure':orgStructure,
    'begDate':     db.formatDate(begDate),
    'endDate':     db.formatDate(endDate),
    'endYearDate': db.formatDate(lastYearDay(endDate)),
    'suspicionCond':suspicionCond,
    'primaryCond': primaryCond,
    'mesDispans' : mesDispans,
                           }
    return db.query(stmt)


class CReportForm131_o_5000_2016(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Сведения о выявленных заболеваниях (случаев) (2016)')


    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setEventTypeVisible(False)
        result.setMesDispansListVisible(True)
        result.setOnlyPermanentAttachVisible(False)
        result.setOrgStructureVisible(True)
        result.setTitle(self.title())
        return result


    def getReportData(self, query):
        mapRows = createMapCodeToRowIdx( [row[2] for row in MainRows] )
        reportData = [ [0]*13 for row in MainRows ]
        notClasifiedRows = [len(mapRows)-1]

        commonColumn = 8
        while query.next():
            record = query.record()
            clientAge = forceInt(record.value('clientAge'))
            clientSex = forceInt(record.value('clientSex'))
            mkb = normalizeMKB(forceString(record.value('MKB')))
            isObserved = forceInt(record.value('isObserved'))
            ageColumn = getAgeClass(clientAge)
            if ageColumn is None:
                continue
            rows = mapRows.get(mkb, [])
            if len(rows) == 1 and rows[0] == len(MainRows)-1:
                reportLine = reportData[len(MainRows)-2]
                baseColumn = 0 if clientSex == 1 else 4
                reportLine[baseColumn+ageColumn] += 1
                reportLine[baseColumn+3] += 1
                reportLine[commonColumn+ageColumn] += 1
                reportLine[commonColumn+3] += 1
                reportLine[12] += isObserved
            if rows == notClasifiedRows:
                rows.append[-2]
            for row in rows:
                reportLine = reportData[row]
                baseColumn = 0 if clientSex == 1 else 4
                reportLine[baseColumn+ageColumn] += 1
                reportLine[baseColumn+3] += 1
                reportLine[commonColumn+ageColumn] += 1
                reportLine[commonColumn+3] += 1
                reportLine[12] += isObserved
        return reportData


    def _selectData(self, params):
        return selectData(params, showSuspicion=False, onlyPrimary=False)


    def titleNumber(self):
        return u'(5000)'


    def build(self, params):
        query = self._selectData(params)
        reportData = self.getReportData(query)

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.insertText(self.titleNumber())
        cursor.insertBlock()
        tableColumns = [
            ( '18%', [u'Фактора риска (наименование по МКБ-10)', u'', u'1'], CReportBase.AlignLeft),
            ( '3%',  [u'№ строки', u'', u'2'], CReportBase.AlignLeft),
            ( '15%', [u'Код МКБ-10', u'', u'3'], CReportBase.AlignLeft),
            ( '5%',  [u'Мужчины', u'18 – 36 лет', u'4'], CReportBase.AlignRight),
            ( '5%',  [u'', u'39 – 60 лет', u'5'], CReportBase.AlignRight),
            ( '5%',  [u'', u'Старше 60 лет', u'6'], CReportBase.AlignRight),
            ( '5%',  [u'', u'Всего', u'7'], CReportBase.AlignRight),
            ( '5%',  [u'Женщины', u'18 – 36 лет', u'8'], CReportBase.AlignRight),
            ( '5%',  [u'', u'39 – 60 лет', u'9'], CReportBase.AlignRight),
            ( '5%',  [u'', u'Старше 60 лет', u'10'], CReportBase.AlignRight),
            ( '5%',  [u'', u'Всего', u'11'], CReportBase.AlignRight),
            ( '5%',  [u'Всего', u'18 – 36 лет', u'12'], CReportBase.AlignRight),
            ( '5%',  [u'', u'39 – 60 лет', u'13'], CReportBase.AlignRight),
            ( '5%',  [u'', u'Старше 60 лет', u'14'], CReportBase.AlignRight),
            ( '5%',  [u'', u'Всего', u'15'], CReportBase.AlignRight),
            ( '5%',  [u'Установлено диспансерное наблюдение', u'', u'16'], CReportBase.AlignRight)
                      ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 2, 1)
        table.mergeCells(0, 3, 1, 4)
        table.mergeCells(0, 7, 1, 4)
        table.mergeCells(0, 11, 1, 4)
        table.mergeCells(0, 15, 2, 1)

        for row, rowDescr in enumerate(MainRows):
            reportLine = reportData[row]
            i = table.addRow()
            table.setText(i, 0, rowDescr[0])
            table.setText(i, 1, rowDescr[1])
            table.setText(i, 2, rowDescr[2])
            for col, value in enumerate(reportLine):
                table.setText(i, 3+col, value)
        return doc


class CReportForm131_o_5001_2016(CReportForm131_o_5000_2016):
    def __init__(self, parent):
        CReportForm131_o_5000_2016.__init__(self, parent)
        self.setTitle(u'Сведения о впервые выявленных при проведении диспансеризации заболеваниях (случаев) (2016)')


    def _selectData(self, params):
        return selectData(params, showSuspicion=False, onlyPrimary=True)


    def titleNumber(self):
        return u'(5001)'


class CReportForm131_o_6000_2016(CReportForm131_o_5000_2016):
    def __init__(self, parent):
        CReportForm131_o_5000_2016.__init__(self, parent)
        self.setTitle(u'Сведения об установленных при проведении диспансеризации предварительных диагнозах (случаев) (2016)')


    def _selectData(self, params):
        return selectData(params, showSuspicion=True, onlyPrimary=False)


    def titleNumber(self):
        return u'(6000)'


    def getReportData(self, query):
        mapRows = createMapCodeToRowIdx( [row[2] for row in MainRows] )
        reportData = [ [0]*13 for row in MainRows ]
        notClasifiedRows = [len(mapRows)-1]

        commonColumn = 8
        while query.next():
            record = query.record()
            clientAge = forceInt(record.value('clientAge'))
            clientSex = forceInt(record.value('clientSex'))
            mkb = normalizeMKB(forceString(record.value('MKB')))
            ageColumn = getAgeClass(clientAge)
            isPhasesAdditionDispans = forceBool(record.value('isPhasesAdditionDispans'))
            isResultAdditionDispans = forceBool(record.value('isResultAdditionDispans'))
            mkb                     = normalizeMKB(forceString(record.value('MKB')))
            if ageColumn is None:
                continue
            rows = mapRows.get(mkb, [])
            if len(rows) == 1 and rows[0] == len(MainRows)-1:
                reportLine = reportData[len(MainRows)-2]
                baseColumn = 0 if clientSex == 1 else 4
                reportLine[baseColumn+ageColumn] += 1
                reportLine[baseColumn+3] += 1
                reportLine[commonColumn+ageColumn] += 1
                reportLine[commonColumn+3] += 1
                if isPhasesAdditionDispans and isResultAdditionDispans and mkb:
                    reportLine[12] += 1
            if rows == notClasifiedRows:
                rows.append[-2]
            for row in rows:
                reportLine = reportData[row]
                baseColumn = 0 if clientSex == 1 else 4
                reportLine[baseColumn+ageColumn] += 1
                reportLine[baseColumn+3] += 1
                reportLine[commonColumn+ageColumn] += 1
                reportLine[commonColumn+3] += 1
                if isPhasesAdditionDispans and isResultAdditionDispans and mkb:
                    reportLine[12] += 1
        return reportData


    def build(self, params):
        query = selectData6000(params, showSuspicion = True)
        reportData = self.getReportData(query)

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.insertText(self.titleNumber())
        cursor.insertBlock()
        tableColumns = [
            ( '18%', [u'Фактора риска (наименование по МКБ-10)', u'', u'1'], CReportBase.AlignLeft),
            ( '3%',  [u'№ строки', u'', u'2'], CReportBase.AlignLeft),
            ( '15%', [u'Код МКБ-10', u'', u'3'], CReportBase.AlignLeft),
            ( '5%',  [u'Мужчины', u'18 – 36 лет', u'4'], CReportBase.AlignRight),
            ( '5%',  [u'', u'39 – 60 лет', u'5'], CReportBase.AlignRight),
            ( '5%',  [u'', u'Старше 60 лет', u'6'], CReportBase.AlignRight),
            ( '5%',  [u'', u'Всего', u'7'], CReportBase.AlignRight),
            ( '5%',  [u'Женщины', u'18 – 36 лет', u'8'], CReportBase.AlignRight),
            ( '5%',  [u'', u'39 – 60 лет', u'9'], CReportBase.AlignRight),
            ( '5%',  [u'', u'Старше 60 лет', u'10'], CReportBase.AlignRight),
            ( '5%',  [u'', u'Всего', u'11'], CReportBase.AlignRight),
            ( '5%',  [u'Всего', u'18 – 36 лет', u'12'], CReportBase.AlignRight),
            ( '5%',  [u'', u'39 – 60 лет', u'13'], CReportBase.AlignRight),
            ( '5%',  [u'', u'Старше 60 лет', u'14'], CReportBase.AlignRight),
            ( '5%',  [u'', u'Всего', u'15'], CReportBase.AlignRight),
            ( '5%',  [u'Из них направлено на дополнительное обследование, не входящее в объем диспансеризации', u'', u'16'], CReportBase.AlignRight)
                      ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 2, 1)
        table.mergeCells(0, 3, 1, 4)
        table.mergeCells(0, 7, 1, 4)
        table.mergeCells(0, 11, 1, 4)
        table.mergeCells(0, 15, 2, 1)

        for row, rowDescr in enumerate(MainRows):
            reportLine = reportData[row]
            i = table.addRow()
            table.setText(i, 0, rowDescr[0])
            table.setText(i, 1, rowDescr[1])
            table.setText(i, 2, rowDescr[2])
            for col, value in enumerate(reportLine):
                table.setText(i, 3+col, value)
        return doc

