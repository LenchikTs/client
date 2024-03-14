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
from PyQt4.QtCore import pyqtSignature, QDate

from library.Utils                import forceBool, forceDouble, forceInt, forceString
from RefBooks.ContingentType.List import CContingentTypeTranslator
from Reports.Report               import CReport
from Reports.ReportBase           import CReportBase, createTable
from Reports.ReportView           import CPageFormat

from Reports.Ui_ReportDispansMO_1_1_Setup import Ui_ReportDispansMO_1_1_SetupDialog


def getContingentTypeCond(contingentTypeId):
    db = QtGui.qApp.db
    cond = []
    table = ''
    contingentOperation = forceInt(db.translate(CContingentTypeTranslator.CTTName, 'id',
                                                contingentTypeId, 'contingentOperation'))
    if CContingentTypeTranslator.isSexAgeSocStatusEnabled(contingentOperation):
        tmp = []
        table = 'LEFT JOIN ClientSocStatus ON ClientSocStatus.client_id = Client.id'
        sexAgeCond    = CContingentTypeTranslator.getSexAgeCond(contingentTypeId)
        socStatusCond = CContingentTypeTranslator.getSocStatusCond(contingentTypeId)
        if CContingentTypeTranslator.isSexAgeSocStatusOperationType_OR(contingentOperation):
            if sexAgeCond is not None:
                tmp.extend(sexAgeCond)
            if socStatusCond is not None:
                tmp.extend(socStatusCond)
            cond.append(db.joinOr(tmp))
        else:
            if sexAgeCond is not None:
                tmp.append(db.joinOr(sexAgeCond))
            if socStatusCond is not None:
                tmp.append(db.joinOr(socStatusCond))
            cond.append(db.joinAnd(tmp))
    return table, cond


def selectData(params):
    db = QtGui.qApp.db
    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())
    contingentTypeId = params.get('contingentTypeId', None)
    if not endDate:
        return None
    if contingentTypeId:
        table, cond = getContingentTypeCond(contingentTypeId)
    stmt = u'''
SELECT
    count(DISTINCT Client.id) AS cnt,
    count(DISTINCT Client.id) AS clientCount,
    count(DISTINCT Event.id) AS  eventCount,
    sum(Account_Item.`sum`) as `sum`,
    (Account_Item.date IS NOT NULL AND Account_Item.refuseType_id IS NULL) AS isPayed,
    rbEventProfile.regionalCode IN (8017,8014,8008) as isFirstPhase,
    rbHealthGroup.code AS healthGroupCode,
    Client.sex AS clientSex,
    2015-YEAR(Client.birthDate) as clientAge,
    IFNULL(ClientWork.post LIKE '%%СТУДЕНТ%%', 0) AS isStudent,
    (ClientWork.id is NULL OR (TRIM(ClientWork.freeInput) = '' AND ClientWork.org_id IS NULL AND  (ClientWork.post LIKE '%%БЕЗРАБ%%'
    OR TRIM(ClientWork.post) = ''))) AS isWorkless,
    IF((rbResult.code = '01' AND rbResult.regionalCode = '49'
    AND rbResult.eventPurpose_id = (SELECT MAX(rbEventTypePurpose.id)
    FROM rbEventTypePurpose WHERE rbEventTypePurpose.code = '11')), 1, 0) AS isResultEvent

FROM Event
INNER JOIN Account_Item ON Account_Item.event_id=Event.id
INNER JOIN Account      ON Account.id=Account_Item.master_id
LEFT JOIN mes.MES         AS MES          ON MES.id=Event.MES_id
LEFT JOIN mes.mrbMESGroup AS mrbMESGroup  ON mrbMESGroup.id=MES.group_id
LEFT JOIN Event           AS PrevEvent    ON PrevEvent.id=Event.prevEvent_id
LEFT JOIN mes.MES         AS PrevMES      ON PrevMES.id=PrevEvent.MES_id
LEFT JOIN mes.mrbMESGroup AS PrevMESGroup ON PrevMESGroup.id=PrevMES.group_id
LEFT JOIN Client        ON Client.id=Event.client_id
LEFT JOIN ClientWork    ON ClientWork.client_id=Client.id
LEFT JOIN Diagnostic    ON Diagnostic.id=getEventDiagnostic(Event.id)
LEFT JOIN rbHealthGroup ON rbHealthGroup.id=Diagnostic.healthGroup_id
LEFT JOIN rbResult      ON rbResult.id = Event.result_id
%(table)s
left JOIN EventType ON EventType.id = Event.eventType_id
  LEFT JOIN rbMedicalAidType ON EventType.medicalAidType_id = rbMedicalAidType.id
  LEFT JOIN rbEventProfile ON rbEventProfile.id=EventType.eventProfile_id
WHERE Event.deleted=0
  AND Event.execDate IS NOT NULL
  AND Account.deleted=0
  AND Account_Item.deleted=0
  AND Account.settleDate>=%(begDate)s
  AND Account.settleDate<=%(endDate)s
--  AND mes.mrbMESGroup.code='ДиспанС'
--  AND ((PrevMESGroup.code='ДиспанС') OR (PrevEvent.id IS NULL))
  AND %(year)d-YEAR(Client.birthDate)>=18
  AND Client.deleted = 0
  AND (ClientWork.id=(SELECT MAX(CW.id)
                      FROM ClientWork AS CW
                      WHERE CW.client_id=ClientWork.client_id AND CW.deleted=0)
       OR ClientWork.id IS NULL)
  AND Account_Item.reexposeItem_id IS NULL
  %(cond)s
     AND rbMedicalAidType.regionalCode=211
GROUP BY isPayed, isResultEvent, isFirstPhase, healthGroupCode, clientSex, clientAge, isStudent, isWorkless;''' % {
        'table'   : table,
        'begDate' : db.formatDate(begDate),
        'endDate' : db.formatDate(endDate),
        'year'    : endDate.year(),
        'cond'    : 'AND %s'%(db.joinAnd(cond)) if cond else ''
    }
    return db.query(stmt)


def selectAttachedClientCountData(params):
    db = QtGui.qApp.db
    endDate = params.get('endDate', QDate())
    contingentTypeId = params.get('contingentTypeId', None)
    if contingentTypeId:
        table, cond = getContingentTypeCond(contingentTypeId)
    stmt=u'''
SELECT
    COUNT(1) AS cnt,
    Client.sex AS clientSex,
    %(year)d-YEAR(Client.birthDate) as clientAge,
    IFNULL(ClientWork.post LIKE '%%СТУДЕНТ%%', 0) AS isStudent,
    (ClientWork.id is NULL OR ClientWork.post LIKE '%%БЕЗРАБ%%' OR TRIM(ClientWork.post) = '') AS isWorkless
FROM Client
LEFT JOIN ClientWork ON ClientWork.client_id=Client.id
%(table)s
WHERE Client.deleted=0
  AND %(year)d-YEAR(Client.birthDate)>=18
  AND (ClientWork.id=(SELECT MAX(CW.id)
                      FROM ClientWork AS CW
                      WHERE CW.client_id=ClientWork.client_id AND CW.deleted=0)
       OR ClientWork.id IS NULL)
  AND (EXISTS (SELECT ClientAttach.id FROM ClientAttach WHERE (ClientAttach.deleted=0)
  AND (ClientAttach.client_id=Client.id) AND (DATE(ClientAttach.begDate)<=DATE('2015-09-01'))
  AND (((DATE(ClientAttach.endDate)>=DATE(%(endDate)s)) OR (ClientAttach.endDate IS NULL)))))
  AND (EXISTS (SELECT ClientPolicy.id FROM ClientPolicy WHERE (ClientPolicy.deleted=0)
  AND (ClientPolicy.client_id=Client.id) AND (DATE(ClientPolicy.begDate)<=DATE('2015-09-01'))
  AND (((DATE(ClientPolicy.endDate)>=DATE(%(endDate)s)) OR (ClientPolicy.endDate IS NULL)))))
  %(cond)s
GROUP BY clientSex, clientAge, isStudent, isWorkless;''' % {'year' : endDate.year(),
                                                            'endDate' : db.formatDate(endDate),
                                                            'table': table,
                                                            'cond' : 'AND %s'%(db.joinAnd(cond)) if cond else ''
                                                           }
    return db.query(stmt)


def selectDispansClientCountDataFromYear(params):
    db = QtGui.qApp.db
    endDate = params.get('endDate', QDate())
    contingentTypeId = params.get('contingentTypeId', None)
    if contingentTypeId:
        table, cond = getContingentTypeCond(contingentTypeId)
    stmt=u'''
SELECT
    COUNT(1) AS cnt,
    Client.sex AS clientSex,
    2015-YEAR(Client.birthDate) as clientAge,
    IFNULL(ClientWork.post LIKE '%%СТУДЕНТ%%', 0) AS isStudent,
    (ClientWork.id is NULL OR ClientWork.post LIKE '%%БЕЗРАБ%%' OR TRIM(ClientWork.post) = '') AS isWorkless
FROM Event
LEFT JOIN mes.MES ON mes.MES.id=Event.MES_id
LEFT JOIN mes.mrbMESGroup ON mes.mrbMESGroup.id=mes.MES.group_id
LEFT JOIN Client ON Client.id=Event.client_id
LEFT JOIN ClientWork ON ClientWork.client_id=Client.id
%(table)s
WHERE (Event.deleted=0)
  AND (Event.execDate IS NOT NULL)
  AND (mes.mrbMESGroup.code='ДиспанС')
  AND %(year)d-YEAR(Client.birthDate)>=18
  AND (ClientWork.id=(SELECT MAX(CW.id)
                      FROM ClientWork AS CW
                      WHERE CW.client_id=ClientWork.client_id AND CW.deleted=0)
       OR ClientWork.id IS NULL)
  %(cond)s
GROUP BY clientSex, clientAge, isStudent, isWorkless;''' % {'year' : endDate.year(),
                                                            'table': table,
                                                            'cond' : 'AND %s'%(db.joinAnd(cond)) if cond else ''
                                                           }
    return db.query(stmt)


class CReportDispansMO_1_1_SetupDialog(QtGui.QDialog, Ui_ReportDispansMO_1_1_SetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.cmbFilterContingentType.setTable('rbContingentType', addNone=True)


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.cmbFilterContingentType.setValue(params.get('contingentTypeId', None))


    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['contingentTypeId'] = self.cmbFilterContingentType.value()
        return result


    @pyqtSignature('int')
    def on_cmbFilterContingentType_currentIndexChanged(self, index):
        contingentTypeId = self.cmbFilterContingentType.value()
        stringInfo = u'Введите тип контингента' if not contingentTypeId else u''
        self.cmbFilterContingentType.setToolTip(stringInfo)
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(bool(contingentTypeId))


class CReportDispansMO_1_1(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Сведения о предъявленных к оплате реестрах счетов за проведенную диспансеризацию взрослого населения. Приложение 1.1')
        self.orientation = CPageFormat.Landscape
        self.rows = {
                    1  : [u'Всего взрослых (в возрасте 18 лет и старше) \n    из них:'],
                    2  : [u'        мужчины'],
                    3  : [u'        женщины'],
                    4  : [u'Работающих граждан \n    из них:'],
                    5  : [u'        мужчины'],
                    6  : [u'        женщины'],
                    7  : [u'Неработающих граждан \n    из них:'],
                    8  : [u'        мужчины'],
                    9  : [u'        женщины'],
                    10 : [u'Справочно: из строки 1 обучающиеся в образовательных организациях по очной форме'],
                    11 : [u'        из строки 2 мужчины'],
                    12 : [u'        из строки 3 женщины']
                    }


    def getSetupDialog(self, parent):
        result = CReportDispansMO_1_1_SetupDialog(parent)
        result.setTitle(self.title())
        return result


    def clearData(self):
        defaultDataValues = ['', 0, 0, 0, 0.0, 0, 0.0, 0, 0.0, 0.0, 0, 0.0, 0, 0.0, 0, 0, 0, 0]
        for data in self.rows.values():
            for defaultValue in defaultDataValues:
                data.append(defaultValue)


    def _setExposeValues(self, cnt, sum, isFirstPhase, clientSex, isStudent, isWorkless, asPayed):
        column = 5 if not asPayed else 10

        self.rows[1][column] += sum
        if isFirstPhase:
            pcolumn = column + 1
        else:
            pcolumn = column + 3

        self.rows[1][pcolumn] += cnt
        self.rows[1][pcolumn+1] += sum

        if clientSex == 1: # мужчины
            self.rows[2][column] += sum
            self.rows[2][pcolumn] += cnt
            self.rows[2][pcolumn+1] += sum
        else: # женщины
            self.rows[3][column] += sum
            self.rows[3][pcolumn] += cnt
            self.rows[3][pcolumn+1] += sum

        if isStudent: # студенты
            self.rows[10][column] += sum
            self.rows[10][pcolumn] += cnt
            self.rows[10][pcolumn+1] += sum
            if clientSex == 1: # мужчины
                self.rows[11][column] += sum
                self.rows[11][pcolumn] += cnt
                self.rows[11][pcolumn+1] += sum
            else: # женщины
                self.rows[12][column] += sum
                self.rows[12][pcolumn] += cnt
                self.rows[12][pcolumn+1] += sum
        elif isWorkless: # не работающие
            self.rows[7][column] = 5
            self.rows[7][pcolumn] += cnt
            self.rows[7][pcolumn+1] += 6
            if clientSex == 1: # мужчины
                self.rows[8][column] += sum
                self.rows[8][pcolumn] += cnt
                self.rows[8][pcolumn+1] += sum
            else: # женщины
                self.rows[9][column] += sum
                self.rows[9][pcolumn] += cnt
                self.rows[9][pcolumn+1] += sum

        else: # работающие
            self.rows[4][column] += sum
            self.rows[4][pcolumn] += cnt
            self.rows[4][pcolumn+1] += sum
            if clientSex == 1: # мужчины
                self.rows[5][column] += sum
                self.rows[5][pcolumn] += cnt
                self.rows[5][pcolumn+1] += sum
            else: # женщины
                self.rows[6][column] += sum
                self.rows[6][pcolumn] += cnt
                self.rows[6][pcolumn+1] += sum


    def _setSecondPhaseDispansValues(self, cnt, clientSex, isStudent, isWorkless):
        self.rows[1][15] += cnt
        if clientSex == 1: # мужчины
            self.rows[2][15] += cnt
        else: # женщины
            self.rows[3][15] += cnt

        if isStudent: # студенты
            self.rows[10][15] += cnt
            if clientSex == 1: # мужчины
                self.rows[11][15] += cnt
            else: # женщины
                self.rows[12][15] += cnt
        elif isWorkless: # не работающие
            self.rows[7][15] += cnt
            if clientSex == 1: # мужчины
                self.rows[8][15] += cnt
            else: # женщины
                self.rows[9][15] += cnt
        else: # работающие
            self.rows[4][15] += cnt
            if clientSex == 1: # мужчины
                self.rows[5][15] += cnt
            else: # женщины
                self.rows[6][15] += cnt


    def _setHealthGroupValues(self, cnt, healthGroupCode, clientSex, isStudent, isWorkless):
        healthGroupCodeIndex = '123'.find(healthGroupCode[:1])
        if healthGroupCodeIndex<0:
            return

        column = 16 + healthGroupCodeIndex

        self.rows[1][column] += cnt
        if clientSex == 1: # мужчины
            self.rows[2][column] += cnt
        else: # женщины
            self.rows[3][column] += cnt

        if isStudent: # студенты
            self.rows[10][column] += cnt
            if clientSex == 1: # мужчины
                self.rows[11][column] += cnt
            else: # женщины
                self.rows[12][column] += cnt
        elif isWorkless: # не работающие
            self.rows[7][column] += cnt
            if clientSex == 1: # мужчины
                self.rows[8][column] += cnt
            else: # женщины
                self.rows[9][column] += cnt
        else: # работающие
            self.rows[4][column] += cnt
            if clientSex == 1: # мужчины
                self.rows[5][column] += cnt
            else: # женщины
                self.rows[6][column] += cnt


    def _setCurrentPeriodClientCount(self, cnt, clientSex, isStudent, isWorkless):
        column = 4

        self.rows[1][column] += cnt
        if clientSex == 1: # мужчины
            self.rows[2][column] += cnt
        else: # женщины
            self.rows[3][column] += cnt

        if isStudent: # студенты
            self.rows[10][column] += cnt
            if clientSex == 1: # мужчины
                self.rows[11][column] += cnt
            else: # женщины
                self.rows[12][column] += cnt
        elif isWorkless: # не работающие
            self.rows[7][column] += cnt
            if clientSex == 1: # мужчины
                self.rows[8][column] += cnt
            else: # женщины
                self.rows[9][column] += cnt
        else: # работающие
            self.rows[4][column] += cnt
            if clientSex == 1: # мужчины
                self.rows[5][column] += cnt
            else: # женщины
                self.rows[6][column] += cnt


    def _setAttachedCurrentPeriodClientCount(self, cnt, clientSex, isStudent, isWorkless):
        column = 2

        self.rows[1][column] += cnt
        if clientSex == 1: # мужчины
            self.rows[2][column] += cnt
        else: # женщины
            self.rows[3][column] += cnt

        if isStudent:
            self.rows[10][column] += cnt
            if clientSex == 1: # мужчины
                self.rows[11][column] += cnt
            else: # женщины
                self.rows[12][column] += cnt
        elif isWorkless:
            self.rows[7][column] += cnt
            if clientSex == 1: # мужчины
                self.rows[8][column] += cnt
            else: # женщины
                self.rows[9][column] += cnt
        else: # работающие
            self.rows[4][column] += cnt
            if clientSex == 1: # мужчины
                self.rows[5][column] += cnt
            else: # женщины
                self.rows[6][column] += cnt


    def _setDispansClientCountDataFromYear(self, cnt, clientSex, isStudent, isWorkless):
        column = 3

        self.rows[1][column] += cnt
        if clientSex == 1: # мужчины
            self.rows[2][column] += cnt
        else: # женщины
            self.rows[3][column] += cnt

        if isStudent: # студенты
            self.rows[10][column] += cnt
            if clientSex == 1: # мужчины
                self.rows[11][column] += cnt
            else: # женщины
                self.rows[12][column] += cnt
        elif isWorkless:
            self.rows[7][column] += cnt
            if clientSex == 1: # мужчины
                self.rows[8][column] += cnt
            else: # женщины
                self.rows[9][column] += cnt
        else: # работающие
            self.rows[4][column] += cnt
            if clientSex == 1: # мужчины
                self.rows[5][column] += cnt
            else: # женщины
                self.rows[6][column] += cnt


    def getReportData(self, query):
        self.clearData()

        while query.next():
            record = query.record()
            clientCount = forceInt(record.value('clientCount'))
            eventCount = forceInt(record.value('eventCount'))
            sum = forceDouble(record.value('sum'))/1000.
            isPayed = forceBool(record.value('isPayed'))
            isFirstPhase = forceBool(record.value('isFirstPhase'))
            healthGroupCode = forceString(record.value('healthGroupCode'))
            clientSex = forceInt(record.value('clientSex'))
            isStudent = forceBool(record.value('isStudent'))
            isWorkless = forceBool(record.value('isWorkless'))
            isResultEvent = forceBool(record.value('isResultEvent'))

            self._setExposeValues(eventCount, sum, isFirstPhase, clientSex, isStudent, isWorkless, False)
            if isPayed:
                self._setExposeValues(eventCount, sum, isFirstPhase, clientSex, isStudent, isWorkless, True)
            if isResultEvent:
                self._setSecondPhaseDispansValues(clientCount, clientSex, isStudent, isWorkless)
            self._setHealthGroupValues(eventCount, healthGroupCode, clientSex, isStudent, isWorkless)
            self._setCurrentPeriodClientCount(clientCount, clientSex, isStudent, isWorkless)


    def getAttachedClientCountReportData(self, query):
        while query.next():
            record = query.record()
            cnt        = forceInt(record.value('cnt'))
            clientSex  = forceInt(record.value('clientSex'))
            isStudent  = forceBool(record.value('isStudent'))
            isWorkless = forceBool(record.value('isWorkless'))
            self._setAttachedCurrentPeriodClientCount(cnt, clientSex, isStudent, isWorkless)


    def getDispansClientCountDataFromYear(self, query):
        while query.next():
            record = query.record()
            cnt        = forceInt(record.value('cnt'))
            clientSex  = forceInt(record.value('clientSex'))
            isStudent  = forceBool(record.value('isStudent'))
            isWorkless = forceBool(record.value('isWorkless'))
            self._setDispansClientCountDataFromYear(cnt, clientSex, isStudent, isWorkless)


    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        self.rows = {
                    1  : [u'Всего взрослых (в возрасте 18 лет и старше) \n    из них:'],
                    2  : [u'        мужчины'],
                    3  : [u'        женщины'],
                    4  : [u'Работающих граждан \n    из них:'],
                    5  : [u'        мужчины'],
                    6  : [u'        женщины'],
                    7  : [u'Неработающих граждан \n    из них:'],
                    8  : [u'        мужчины'],
                    9  : [u'        женщины'],
                    10 : [u'Справочно: из строки 1 обучающиеся в образовательных организациях по очной форме'],
                    11 : [u'        из строки 2 мужчины'],
                    12 : [u'        из строки 3 женщины']
                    }

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        tableColumns = [
            ( '5%', [u'Группы', u'', u'', u'1'], CReportBase.AlignLeft),
            ( '2%', [u'№', u'', u'', u'2'], CReportBase.AlignRight),
            ( '5%', [u'Количество медицинских организаций, проводящих диспансе-ризацию в отчетном периоде', u'', u'', u'3'], CReportBase.AlignRight),
            ( '6%', [u'Численность застрахованных лиц, прикрепленных к медицинским организациям, оказывающим первичную медико-санитарную помощь, на отчетную дату, человек', u'', u'', u'4'], CReportBase.AlignRight),
            ( '5%', [u'В том числе', u'', u'', u'5'], CReportBase.AlignRight),
            ( '5%', [u'подлежащие диспансе-ризации в отчетном году, согласно утвержденному плану-графику, всего, человек', u'из них:', u'на отчетный период, человек', u'6'], CReportBase.AlignRight),
            ( '5%', [u'Всего предъявлен-ных к оплате реестров счетов в рамках диспансе-ризации на отчетную дату, тыс. рублей', u'', u'', u'7'], CReportBase.AlignRight),
            ( '5%', [u'В том числе', u'В рамках I этапа диспансеризации', u'Кол-во случаев', u'8'], CReportBase.AlignRight),
            ( '5%', [u'', u'', u'Тысяч руб.', u'9'], CReportBase.AlignRight),
            ( '5%', [u'', u'В рамках II этапа диспансеризации', u'Кол-во случаев', u'10'], CReportBase.AlignRight),
            ( '5%', [u'', u'', u'Тысяч руб.', u'11'], CReportBase.AlignRight),
            ( '5%', [u'Всего оплачено реестров счетов в рамках диспансеризации за отчетный период, тыс. рублей', u'', u'', u'12'], CReportBase.AlignRight),
            ( '5%', [u'В том числе', u'В рамках I этапа диспансеризации', u'Кол-во случаев', u'13'], CReportBase.AlignRight),
            ( '5%', [u'', u'', u'Тысяч руб.', u'14'], CReportBase.AlignRight),
            ( '5%', [u'', u'В рамках II этапа диспансеризации', u'Кол-во случаев', u'15'], CReportBase.AlignRight),
            ( '5%', [u'', u'', u'Тысяч руб.', u'16'], CReportBase.AlignRight),
            ( '7%', [u'Количество граждан, направленных на II этап диспансе-ризации по результатам I этапа диспансе-ризации, человек', u'', u'', u'17'], CReportBase.AlignRight),
            ( '7%', [u'Группы состояния здоровья застрахованных лиц, прошедших диспансеризацию', u'I группа состояния здоровья, человек', u'', u'18'], CReportBase.AlignRight),
            ( '4%', [u'', u'II группа состояния здоровья, человек', u'', u'19'], CReportBase.AlignRight),
            ( '4%', [u'', u'III группа состояния здоровья, человек', u'', u'20'], CReportBase.AlignRight),
        ]

        table = createTable(cursor, tableColumns)

        table.mergeCells(0, 0, 3, 1)
        table.mergeCells(0, 1, 3, 1)
        table.mergeCells(0, 2, 3, 1)
        table.mergeCells(0, 3, 3, 1)
        table.mergeCells(0, 4, 1, 2)
        table.mergeCells(1, 4, 2, 1)
        table.mergeCells(0, 6, 3, 1)
        table.mergeCells(0, 7, 1, 4)
        table.mergeCells(1, 7, 1, 2)
        table.mergeCells(1, 9, 1, 2)
        table.mergeCells(0, 11, 3, 1)
        table.mergeCells(0, 12, 1, 4)
        table.mergeCells(1, 12, 1, 2)
        table.mergeCells(1, 14, 1, 2)
        table.mergeCells(0, 16, 3, 1)
        table.mergeCells(0, 17, 1, 3)
        table.mergeCells(1, 17, 2, 1)
        table.mergeCells(1, 18, 2, 1)
        table.mergeCells(1, 19, 2, 1)

        query = selectData(params)

        if query is None:
            return doc

        self.getReportData(query)
        self.getAttachedClientCountReportData(selectAttachedClientCountData(params))
        self.getDispansClientCountDataFromYear(selectDispansClientCountDataFromYear(params))

        keyList = self.rows.keys()
        keyList.sort()


        for key in keyList:
            data = self.rows[key]

            i = table.addRow()
            table.setText(i, 0, data[0])
            table.setText(i, 1, key)

            for idx, value in enumerate(data[1:]):
                table.setText(i, idx+2, value)


        cursor.movePosition(QtGui.QTextCursor.End)

        cursor.insertText(u'\n\n\n\n\n')
        cursor.insertText(u'Руководитель \nмедицинской организации            ')
        cursor.insertText(u'________________________________                  ________________________________\n')
        cursor.insertText(u' '*77 + u'подпись' + u' ' * 62 + u'ФИО\n\n\n\n\n')

        cursor.insertText(u'Исполнитель  \nТел                                                     ')
        cursor.insertText(u'________________________________                  ________________________________\n')
        cursor.insertText(u' '*77 + u'подпись' + u' ' * 62 + u'ФИО')

        return doc
