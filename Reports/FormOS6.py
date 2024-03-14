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

from PyQt4.QtCore import pyqtSignature, QDate, QDateTime
from PyQt4 import QtGui

from Orgs.Utils import getOrgStructureFullName
from Reports.EconomicAnalisysSetupDialog import CEconomicAnalisysSetupDialog, getCond
from Reports.Report import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.ReportView import CPageFormat
from Reports.Utils import dateRangeAsStr
from library.Utils import forceDate, forceString, forceDouble, forceInt


class CFormOS6SetupDialog(CEconomicAnalisysSetupDialog):
    def __init__(self, parent=None):
        CEconomicAnalisysSetupDialog.__init__(self, parent)

    def setVisibilityForDateType(self, datetype):
        pass

    def setParams(self, params):
        CEconomicAnalisysSetupDialog.setParams(self, params)

    def updateNoScheta(self):
        self.cmbNoscheta.updateFilter(
            forceDate(self.edtBegDate.date()),
            forceDate(self.edtEndDate.date()),
            self.cmbOrgStructure.value(),
            self.cmbContract.value(),
            self.cmbFinance.value())


    @pyqtSignature('QDate')
    def on_edtBegDate_dateChanged(self, date):
        self.cmbPerson.setBegDate(date)
        self.updateNoScheta()
        self.updateContractFilter()

    @pyqtSignature('QDate')
    def on_edtEndDate_dateChanged(self, date):
        self.cmbPerson.setEndDate(date)
        self.updateNoScheta()
        self.updateContractFilter()

    @pyqtSignature('int')
    def on_cmbOrgStructure_currentIndexChanged(self, index):
        orgStructureId = self.cmbOrgStructure.value()
        self.cmbPerson.setOrgStructureId(orgStructureId)
        self.updateNoScheta()

    @pyqtSignature('int')
    def on_cmbContract_currentIndexChanged(self, index):
        self.updateNoScheta()

    @pyqtSignature('int')
    def on_cmbFinance_currentIndexChanged(self, index):
        self.updateContractFilter()
        self.updateNoScheta()


class CFormOS6(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Отчет о представленных счетах в разрезе видов медицинской помощи')
        self.setOrientation(QtGui.QPrinter.Landscape)
        self.pageFormat = CPageFormat(pageSize=CPageFormat.A4, orientation=CPageFormat.Landscape, leftMargin=1,
                                      topMargin=1, rightMargin=1, bottomMargin=1)
        self.isDetailed = False;


    def getSetupDialog(self, parent):
        result = CFormOS6SetupDialog(parent)
        result.setVisibilityProfileBed(False)
        result.setFinanceVisible(True)
        result.setSpecialityVisible(False)
        result.setPersonVisible(False)
        result.setVidPomVisible(False)
        result.setSchetaVisible(False)
        result.setPayerVisible(False)
        result.setEventTypeVisible(False)
        result.setSexVisible(False)
        result.setDetailToVisible(False)
        result.setRazrNasVisible(False)
        result.setAgeVisible(False)
        result.setNoschetaVisible(True)
        result.setNoschetaEnabled(True)
        result.setDateTypeVisible(False)
        result.edtBegTime.setVisible(False)
        result.edtEndTime.setVisible(False)
        result.setPriceVisible(False)
        result.setDetailVisible(True)
        result.setPrintAccNumberVisible(True)
        result.setTitle(self.title())

        #for i in xrange(result.gridLayout.count()):                                        #ymd
        #    spacer = result.gridLayout.itemAt(i)                                           #ymd
        #    if isinstance(spacer, QtGui.QSpacerItem):                                      #ymd
        #        itemposition = result.gridLayout.getItemPosition(i)                        #ymd
        #        if itemposition != (29, 0, 1, 1) and itemposition != (8, 1, 1, 3):         #ymd
        #            result.gridLayout.removeItem(spacer)                                   #ymd
        result.resize(400, 10)
        return result

    def selectData(self, params):
        stmt = u'''
SELECT
       number,
	   smotitle,
	   smoid,
       orgcode,
       orgname,
       mtcode,
       mtname,
       count(distinct if(exposed, event_id, null)) as ex_count,
       Sum(IF(exposed, is_mes, 0))          AS ex_mes,
       Sum(IF(exposed, kd, 0))              AS ex_kd,
       Sum(IF(exposed, ispos, 0))           AS ex_pos,
       Sum(IF(exposed, uet, 0))             AS ex_uet,
       Sum(IF(exposed, pd, 0))              AS ex_pd,
       Sum(IF(exposed, iscallambulance, 0)) AS ex_smp,
       Sum(IF(exposed, isobr, 0))           AS ex_obr,
       Round(Sum(IF(exposed, sum, 0)), 2)   AS ex_sum,
       count(distinct if(refused, event_id, null)) as ref_count,
       Sum(IF(refused, is_mes, 0))          AS ref_mes,
       Sum(IF(refused, kd, 0))              AS ref_kd,
       Sum(IF(refused, ispos, 0))           AS ref_pos,
       Sum(IF(refused, uet, 0))             AS ref_uet,
       Sum(IF(refused, pd, 0))              AS ref_pd,
       Sum(IF(refused, iscallambulance, 0)) AS ref_smp,
       Sum(IF(refused, isobr, 0))           AS ref_obr,
       Round(Sum(IF(refused, sum, 0)), 2)   AS ref_sum,
       count(distinct if(payed, event_id, null)) as pay_count,
       Sum(IF(payed, is_mes, 0))            AS pay_mes,
       Sum(IF(payed, kd, 0))                AS pay_kd,
       Sum(IF(payed, ispos, 0))             AS pay_pos,
       Sum(IF(payed, uet, 0))               AS pay_uet,
       Sum(IF(payed, pd, 0))                AS pay_pd,
       Sum(IF(payed, iscallambulance, 0))   AS pay_smp,
       Sum(IF(payed, isobr, 0))             AS pay_obr,
       Round(Sum(IF(payed, sum, 0)), 2)   AS pay_sum
FROM   (SELECT concat_ws(' | ', if(Payer.infisCode = "", null, Payer.infisCode), Payer.title) as smotitle,
			   Payer.id as smoid,
               OrgStructure.bookkeeperCode AS orgcode,
               OrgStructure.name AS orgname,
               mt.regionalCode AS mtcode,
               Account.number AS number,
               mt.name AS mtname,
               Account_Item.event_id as event_id,
               ( Account_Item.id IS NOT NULL ) AS exposed,
               ( Account_Item.id IS NOT NULL AND Account_Item.date IS NOT NULL AND Account_Item.refusetype_id IS NULL ) AS payed,
               ( Account_Item.id IS NOT NULL AND Account_Item.refusetype_id IS NOT NULL )  AS refused,
               IF(substr(rbService.infis, 1, 1) in ('V', 'G') and mt.regionalcode in ('11', '12', '301', '302', '41', '42', '43', '51', '52', '71', '72', '90', '411', '422', '511', '522'), 1, 0) AS is_mes,
               IF(substr(rbService.infis, 1, 1) in ('V', 'G') AND mt.regionalcode IN ( '11', '12', '301', '302', '401', '402'), Workdays(Event.setdate, Event.execdate, EventType.weekprofilecode, mt.regionalcode), 0) AS kd,
               IF(substr(rbService.infis, 1, 1) in ('V', 'G') AND mt.regionalcode IN ( '41', '42', '43', '51', '52', '71', '72', '90', '411', '422', '511', '522' ), Workdays(Event.setdate, Event.execdate, EventType.weekprofilecode, mt.regionalcode), 0) AS PD,
               IF(rbService.id in (select vVisitServices.id from vVisitServices), 1, 0) AS isPos,
               Account_Item.uet AS uet,
               IF(substr(rbService.infis, 1, 7) = 'B01.044', 1, 0) AS isCallAmbulance,
               IF(rbService.name like 'Обращен%%', 1, 0)  AS isObr,
               Account_Item.sum AS SUM
        FROM   Account_Item
               left join Account
                      on Account.id = Account_Item.master_id
               left join rbAccountType
                      on rbAccountType.id = Account.type_id
               LEFT JOIN Event
                      ON Event.id = Account_Item.event_id
               LEFT JOIN Action
                      ON Action.id = Account_Item.action_id
               LEFT JOIN EventType
                      ON EventType.id = Event.eventType_id
               LEFT JOIN rbMedicalAidType ON EventType.medicalAidType_id = rbMedicalAidType.id
               LEFT JOIN ActionType
                      ON ActionType.id = Action.actionType_id
               LEFT JOIN OrgStructure
                      ON OrgStructure.id = Account.orgstructure_id
               LEFT JOIN Organisation AS Payer
                      ON Payer.id = Account.payer_id
               LEFT JOIN rbService
                      ON rbService.id = Ifnull(Account_Item.service_id,
                                        ActionType.nomenclativeservice_id)
               LEFT JOIN Diagnosis d on d.id = (SELECT diagnosis_id
  FROM Diagnostic
  INNER JOIN rbDiagnosisType ON rbDiagnosisType.id = diagnosisType_id
  WHERE Diagnostic.event_id = Event.id
  AND Diagnostic.deleted = 0
  AND rbDiagnosisType.code IN ('1', '2', '4')
  ORDER BY rbDiagnosisType.code
  LIMIT 1
  )
               left join Contract
                      on Contract.id = Account.contract_id
               LEFT JOIN rbFinance on rbFinance.id = Contract.finance_id
               LEFT JOIN Organisation currentOrg on currentOrg.id = Event.org_id
               LEFT JOIN Person ActionPerson ON ActionPerson.id = Action.person_id
               LEFT JOIN rbSpeciality PersonSpeciality ON PersonSpeciality.id = ActionPerson.speciality_id
               LEFT JOIN rbMedicalAidType mt ON mt.id = case when rbMedicalAidType.regionalCode in ('271', '272') and Event.execDate >= '2020-05-01' then (select mat.id from rbMedicalAidType mat where mat.regionalCode = IF(rbMedicalAidType.regionalCode = '271', '21', '22') limit 1) else rbMedicalAidType.id end

        where %(cond)s ) q
GROUP  BY %(groupby)s
order by %(orderby)s
        '''
        db = QtGui.qApp.db
        self.isDetailed = params.get("paydetail", False)
        self.isPrice=params.get('printAccNumber', False)
        if params['accountId']:
            params['dataType'] = 3
        else:
            params['dataType'] = 2
        cond = getCond(params)
        if self.isPrice:
            groupby = "q.smoid, q.orgcode, q.mtcode, q.number"
        else:
            groupby = "q.smoid, q.orgcode, q.mtcode"
        
        orderby = "q.orgcode, q.mtcode"
        if self.isDetailed:
            orderby = "q.smoid, q.orgcode, q.mtcode"

        st = stmt % {"cond": cond, "groupby": groupby, "orderby": orderby}
        return db.query(st)

    # def getCond(self, params):
    #     db = QtGui.qApp.db
    #     cond = []
    #     begDate = params.get('begDate', None)
    #     endDate = params.get('endDate', None)
    #     financeId = params.get('financeId', None)
    #     orgStructureId = params.get('orgStructureId', None)
    #     contractId = params.get('contractId', None)
    #     accountId = params.get('accountId')
    #     if begDate:
    #         cond.append("Date(Account.date) >= {0}".format(db.formatDate(begDate)))
    #     if endDate:
    #         cond.append("Date(Account.date) <= {0}".format(db.formatDate(endDate)))
    #
    #     if orgStructureId:
    #         cond.append("Account.orgStructure_id = %s" % orgStructureId)
    #
    #     if financeId:
    #         cond.append('Contract.finance_id = {0:d}'.format(financeId))
    #     if contractId:
    #         cond.append('Account.contract_id = {0:d}'.format(contractId))
    #     if accountId:
    #         cond.append("Account.id = {0:d}".format(accountId))
    #     return db.joinAnd(cond)

    def getDescription(self, params):
        db = QtGui.qApp.db
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        orgStructureId = params.get('orgStructureId', None)
        typeFinanceId = params.get('financeId', None)
        contractId = params.get('contractId', None)
        rows = []
        rows.append(u'по дате счет-фактуры')
        rows.append(dateRangeAsStr(u'за период', begDate, endDate))
        rows.append(u'подразделение: ' + getOrgStructureFullName(orgStructureId))
        if typeFinanceId is not None:
            rows.append(u'тип финансирования: ' + forceString(db.translate('rbFinance', 'id', typeFinanceId, 'name')))
        if contractId:
            rows.append(u'по договору № ' + forceString(db.translate('Contract', 'id', contractId, "concat_ws(' | ', (select rbFinance.name from rbFinance where rbFinance.id = Contract.finance_id), Contract.resolution, Contract.number)")))

        rows.insert(10, u'типы реестров: %s' %
                      [u"не задано", u"Только Основные", u"Основные + Дополнительные", u"Только Повторные"][
                          params.get("accountType", 0)])
        if params.get("paydetail", False):
            rows.insert(10, u'в разрезе плательщиков')
        rows.append(u'отчёт составлен: ' + forceString(QDateTime.currentDateTime()))
        return rows


    def build(self, params):
        reportData = {}
        self.isPrice=params.get('printAccNumber', False)
        
        if self.isPrice:
            reportRowSize = 32
            def processQuery(query):
                while query.next():
                    record = query.record()

                    reportLine = [0] * reportRowSize
                    for i, key in enumerate(['orgcode', 'orgname', 'mtcode', 'mtname', 'number', 'ex_count',
                                             'ex_mes', 'ex_kd', 'ex_pos', 'ex_uet', 'ex_pd',
                                             'ex_smp', 'ex_obr', 'ex_sum', 'ref_count', 'ref_mes',
                                             'ref_kd', 'ref_pos', 'ref_uet', 'ref_pd', 'ref_smp',
                                             'ref_obr', 'ref_sum', 'pay_count', 'pay_mes', 'pay_kd',
                                             'pay_pos', 'pay_uet', 'pay_pd', 'pay_smp', 'pay_obr',
                                             'pay_sum' ]):
                        if key in ['orgcode', 'orgname', 'mtcode', 'mtname', 'number']:
                            reportLine[i] = forceString(record.value(key))
                        elif key in ['ex_sum', 'ex_uet', 'ref_sum', 'ref_uet', 'pay_sum', 'pay_uet']:
                            reportLine[i] = forceDouble(record.value(key))
                        else:
                            reportLine[i] = forceInt(record.value(key))
                    smoid = forceString(record.value("smoid")) if self.isDetailed else 'Default'
                    smotitle = forceString(record.value("smotitle")) if self.isDetailed else 'Default'

                    linesPerSmo = reportData.setdefault(forceString(smoid), {"title": smotitle,
                                                "items": {}
                                                })["items"]
                    linesPerOrg = linesPerSmo.setdefault("{%s,%s,%s}" % (reportLine[0], reportLine[2], reportLine[4]), [0] * reportRowSize)
                    for i, k in enumerate(linesPerOrg):
                        if isinstance(reportLine[i], str) or isinstance(reportLine[i], unicode):
                            linesPerOrg[i] = reportLine[i]
                        else:
                            linesPerOrg[i] += reportLine[i]

            query = self.selectData(params)
            processQuery(query)
            # now text
            doc = QtGui.QTextDocument()
            cursor = QtGui.QTextCursor(doc)

            cursor.setCharFormat(CReportBase.ReportTitle)
            cursor.insertText(u'Отчет о представленных счетах в разрезе видов медицинской помощи')
            self.dumpParams(cursor, params)
            tableHeader = (
                [u'Структурное подразделение',
                                          [u'Код',               '1'],
                                          [u'Наименование',      '2']
                ],
                [u'Вид помощи',
                                          [u'Код',               '3'],
                                          [u'Наименование',      '4']
                ],
                [u'Представлено к оплате',
                                          [u'Номер счета',       '5'],
                                          [u'Перс.счетов',       '6'],
                                          [u'Стандартов ОМП',    '7'],
                                          [u'Койко-дней',        '8'],
                                          [u'Посещений',         '9'],
                                          [u'УЕТ',               '10'],
                                          [u'Пациенто-дни',      '11'],
                                          [u'Вызов бригады СМП', '12'],
                                          [u'Обращение',         '13'],
                                          [u'Сумма, р.',         '14']
                ],
                [u'Отклонено счетов по результатам медико-экономического контроля',
                                          [u'Перс.счетов',       '15'],
                                          [u'Стандартов ОМП',    '16'],
                                          [u'Койко-дней',        '17'],
                                          [u'Посещений',         '18'],
                                          [u'УЕТ',               '19'],
                                          [u'Пациенто-дни',      '20'],
                                          [u'Вызов бригады СМП', '21'],
                                          [u'Обращение',         '22'],
                                          [u'Сумма, р.',         '23']
                ],
                [u'Принято к оплате по результатам медико-экономического контроля',
                                          [u'Перс.счетов',       '24'],
                                          [u'Стандартов ОМП',    '25'],
                                          [u'Койко-дней',        '26'],
                                          [u'Посещений',         '27'],
                                          [u'УЕТ',               '28'],
                                          [u'Пациенто-дни',      '29'],
                                          [u'Вызов бригады СМП', '30'],
                                          [u'Обращение',         '31'],
                                          [u'Сумма, р.',         '32']
                ]

            )
            tableColumns = []

            #перегон заголовка в формат ['строка1', 'строка2', 'строка 3']
            for fullheader in sum([[[row1[0] if i == 0 else u'', row2[0], row2[1]] for i, row2 in enumerate(row1[1:])] for row1 in tableHeader], []):
                width = '60'
                if fullheader[1] == u'Наименование':
                    width = '100'
                if fullheader[1] == u'Сумма, р.':
                    width = '100'
                tableColumns.append((width, fullheader, CReportBase.AlignCenter))

            def mergeTableHeader(table):
                #объединение колонок в заголовке
                for numCols, column in [(len(row[1:]), len(sum([x[1:] for x in tableHeader[0:i]], []))) for i,row in enumerate(tableHeader)]:
                    table.mergeCells(0, column, 1, numCols)

            cursor.insertBlock()
            for k, v in reportData.iteritems():
                total_by_orgcode = [0] * reportRowSize
                total_by_smo = [0] * reportRowSize
                total_lines = 0
                if self.isDetailed or reportData.keys().index(k) == 0:



                    if self.isDetailed:
                        cursor.insertBlock()
                        cursor.setCharFormat(CReportBase.ReportSubTitle)
                        cursor.insertText(v["title"])
                        cursor.insertBlock()

                    table = createTable(cursor, tableColumns)
                    mergeTableHeader(table)

                items = sorted(v["items"].items(), key=lambda i: (i[1][0], forceInt(i[1][2]) if i[1][2] else 0))
                for idx, reportLine in enumerate(items):
                    reportLine = reportLine[1]
                    total_lines += 1
                    row = table.addRow()
                    orgcode = reportLine[0]
                    for col, val in enumerate(reportLine):
                        table.setText(row, col, val)
                    for i in range(5, reportRowSize):
                        total_by_orgcode[i] += reportLine[i]
                        total_by_smo[i] += reportLine[i]

                    if idx+1 == len(items) or orgcode != items[idx+1][1][0]:
                        total_by_orgcode[0] = orgcode
                        total_by_orgcode[1] = reportLine[1]
                        total_by_orgcode[2] = ''
                        total_by_orgcode[3] = u'Итого'
                        total_by_orgcode[4] = u''
                        row = table.addRow()
                        for i, k in enumerate(total_by_orgcode):
                            table.setText(row, i, k, fontBold=True)
                        table.mergeCells(row, 1, 1, 2)
                        total_by_orgcode = [0] * reportRowSize
                        table.mergeCells(row, 3, 1, 2)

                total_by_smo[0] = ''
                total_by_smo[1] = u'Всего'
                total_by_smo[2] = ''
                total_by_smo[3] = ''
                total_by_smo[4] = ''
                row = table.addRow()
                for i, k in enumerate(total_by_smo):
                    table.setText(row, i, k, fontBold=True)
                table.mergeCells(row, 0, 1, 5)
                cursor.movePosition(QtGui.QTextCursor.End)
                cursor.insertBlock()
        else:
            reportRowSize = 31
            def processQuery(query):
                while query.next():
                    record = query.record()

                    reportLine = [0] * reportRowSize
                    for i, key in enumerate(['orgcode', 'orgname', 'mtcode', 'mtname', 'ex_count',
                                             'ex_mes', 'ex_kd', 'ex_pos', 'ex_uet', 'ex_pd',
                                             'ex_smp', 'ex_obr', 'ex_sum', 'ref_count', 'ref_mes',
                                             'ref_kd', 'ref_pos', 'ref_uet', 'ref_pd', 'ref_smp',
                                             'ref_obr', 'ref_sum', 'pay_count', 'pay_mes', 'pay_kd',
                                             'pay_pos', 'pay_uet', 'pay_pd', 'pay_smp', 'pay_obr',
                                             'pay_sum' ]):
                        if key in ['orgcode', 'orgname', 'mtcode', 'mtname']:
                            reportLine[i] = forceString(record.value(key))
                        elif key in ['ex_sum', 'ex_uet', 'ref_sum', 'ref_uet', 'pay_sum', 'pay_uet']:
                            reportLine[i] = forceDouble(record.value(key))
                        else:
                            reportLine[i] = forceInt(record.value(key))
                    smoid = forceString(record.value("smoid")) if self.isDetailed else 'Default'
                    smotitle = forceString(record.value("smotitle")) if self.isDetailed else 'Default'

                    linesPerSmo = reportData.setdefault(forceString(smoid), {"title": smotitle,
                                                "items": {}
                                                })["items"]
                    linesPerOrg = linesPerSmo.setdefault("{%s,%s}" % (reportLine[0], reportLine[2]), [0] * reportRowSize)
                    for i, k in enumerate(linesPerOrg):
                        if isinstance(reportLine[i], str) or isinstance(reportLine[i], unicode):
                            linesPerOrg[i] = reportLine[i]
                        else:
                            linesPerOrg[i] += reportLine[i]

            query = self.selectData(params)
            processQuery(query)
            # now text
            doc = QtGui.QTextDocument()
            cursor = QtGui.QTextCursor(doc)

            cursor.setCharFormat(CReportBase.ReportTitle)
            cursor.insertText(u'Отчет о представленных счетах в разрезе видов медицинской помощи')
            self.dumpParams(cursor, params)
            tableHeader = (
                [u'Структурное подразделение',
                                          [u'Код',               '1'],
                                          [u'Наименование',      '2']
                ],
                [u'Вид помощи',
                                          [u'Код',               '3'],
                                          [u'Наименование',      '4']
                ],
                [u'Представлено к оплате',
                                          [u'Перс.счетов',       '5'],
                                          [u'Стандартов ОМП',    '6'],
                                          [u'Койко-дней',        '7'],
                                          [u'Посещений',         '8'],
                                          [u'УЕТ',               '9'],
                                          [u'Пациенто-дни',      '10'],
                                          [u'Вызов бригады СМП', '11'],
                                          [u'Обращение',         '12'],
                                          [u'Сумма, р.',         '13']
                ],
                [u'Отклонено счетов по результатам медико-экономического контроля',
                                          [u'Перс.счетов',       '14'],
                                          [u'Стандартов ОМП',    '15'],
                                          [u'Койко-дней',        '16'],
                                          [u'Посещений',         '17'],
                                          [u'УЕТ',               '18'],
                                          [u'Пациенто-дни',      '19'],
                                          [u'Вызов бригады СМП', '20'],
                                          [u'Обращение',         '21'],
                                          [u'Сумма, р.',         '22']
                ],
                [u'Принято к оплате по результатам медико-экономического контроля',
                                          [u'Перс.счетов',       '23'],
                                          [u'Стандартов ОМП',    '24'],
                                          [u'Койко-дней',        '25'],
                                          [u'Посещений',         '26'],
                                          [u'УЕТ',               '27'],
                                          [u'Пациенто-дни',      '28'],
                                          [u'Вызов бригады СМП', '29'],
                                          [u'Обращение',         '30'],
                                          [u'Сумма, р.',         '31']
                ]

            )
            tableColumns = []

            #перегон заголовка в формат ['строка1', 'строка2', 'строка 3']
            for fullheader in sum([[[row1[0] if i == 0 else u'', row2[0], row2[1]] for i, row2 in enumerate(row1[1:])] for row1 in tableHeader], []):
                width = '60'
                if fullheader[1] == u'Наименование':
                    width = '100'
                if fullheader[1] == u'Сумма, р.':
                    width = '100'
                tableColumns.append((width, fullheader, CReportBase.AlignCenter))

            def mergeTableHeader(table):
                #объединение колонок в заголовке
                for numCols, column in [(len(row[1:]), len(sum([x[1:] for x in tableHeader[0:i]], []))) for i,row in enumerate(tableHeader)]:
                    table.mergeCells(0, column, 1, numCols)

            cursor.insertBlock()
            for k, v in reportData.iteritems():
                total_by_orgcode = [0] * reportRowSize
                total_by_smo = [0] * reportRowSize
                total_lines = 0
                if self.isDetailed or reportData.keys().index(k) == 0:



                    if self.isDetailed:
                        cursor.insertBlock()
                        cursor.setCharFormat(CReportBase.ReportSubTitle)
                        cursor.insertText(v["title"])
                        cursor.insertBlock()

                    table = createTable(cursor, tableColumns)
                    mergeTableHeader(table)

                items = sorted(v["items"].items(), key=lambda i: (i[1][0], forceInt(i[1][2]) if i[1][2] else 0))
                for idx, reportLine in enumerate(items):
                    reportLine = reportLine[1]
                    total_lines += 1
                    row = table.addRow()
                    orgcode = reportLine[0]
                    for col, val in enumerate(reportLine):
                        table.setText(row, col, val)
                    for i in range(4, reportRowSize):
                        total_by_orgcode[i] += reportLine[i]
                        total_by_smo[i] += reportLine[i]

                    if idx+1 == len(items) or orgcode != items[idx+1][1][0]:
                        total_by_orgcode[0] = orgcode
                        total_by_orgcode[1] = reportLine[1]
                        total_by_orgcode[2] = ''
                        total_by_orgcode[3] = u'Итого'
                        row = table.addRow()
                        for i, k in enumerate(total_by_orgcode):
                            table.setText(row, i, k, fontBold=True)
                        table.mergeCells(row, 1, 1, 2)
                        total_by_orgcode = [0] * reportRowSize
                        table.mergeCells(row, 3, 1, 1)

                total_by_smo[0] = ''
                total_by_smo[1] = u'Всего'
                total_by_smo[2] = ''
                total_by_smo[3] = ''
                row = table.addRow()
                for i, k in enumerate(total_by_smo):
                    table.setText(row, i, k, fontBold=True)
                table.mergeCells(row, 0, 1, 4)
                cursor.movePosition(QtGui.QTextCursor.End)
                cursor.insertBlock()
        


        return doc
