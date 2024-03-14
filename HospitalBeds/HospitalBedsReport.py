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
from PyQt4.QtCore import QDate, QDateTime, QTime

from library.Utils            import forceInt, forceRef, forceString
from library.PrintInfo        import CInfoList
from Events.EventInfo         import CEventInfo, CMealTimeInfo, CDietInfo
from RefBooks.Finance.Info    import CFinanceInfo

from Reports.Report           import CReport
from Reports.ReportBase       import CReportBase, createTable
from Orgs.OrgStructComboBoxes import COrgStructureModel

from Ui_FeedReportDialog import Ui_FeedReportDialog
#from Ui_ExtraFeedReportDialog import Ui_ExtraFeedReportDialog


class CMealTimeList(CInfoList):
    def __init__(self,  context, id):
        CInfoList.__init__(self, context)
        self._tableName = 'rbMealTime'
        self._class = CMealTimeInfo

    def _load(self):
        db = QtGui.qApp.db
        table = db.table(self._tableName)
        self._idList = db.getIdList(table, 'id')
        self._items = [ self.getInstance(self._class, id) for id in self._idList ]
        return True

    def index(self, key):
        return self._items.index(key)


class CDietList(CMealTimeList):
    def __init__(self,  context, id):
        CMealTimeList.__init__(self, context, id)
        self._tableName = 'rbDiet'
        self._class = CDietInfo


class CFinanceList(CMealTimeList):
    def __init__(self,  context, id):
        CMealTimeList.__init__(self, context, id)
        self._tableName = 'rbFinance'
        self._class = CFinanceInfo


def getFeedData(context,  clientIdList, feedDate, typePrint, time = None):
    feedData = []
    clientIdFeedList = []
    patronIdFeedList = []
    if clientIdList:
        #feedDate = params.get('feedDate', QDate())
        #typePrint = params.get('typePrint', 0)
        if typePrint == 1:
            typeFeed = 1
        #    self.parentTitle = u'для пациентов'
        elif typePrint == 2:
            typeFeed = 2
        #    self.parentTitle = u'для патронов'
        else:
            typeFeed = 0
        #    self.parentTitle = u''
        #if not self.feedDate:
        #feedDate = QDate.currentDate()
        db = QtGui.qApp.db
        tableEvent = db.table('Event')
        tableClient = db.table('Client')
        tableEF = db.table('Event_Feed')
        tableRBMealTime = db.table('rbMealTime')
        tableRBDiet = db.table('rbDiet')
        tableRBFinance = db.table('rbFinance')
        tableSocStatus = db.table('ClientSocStatus')
        cols = [tableEvent['id'].alias('eventId'),
                tableEvent['client_id'],
                tableEF['mealTime_id'],
                tableEF['diet_id'],
                tableEF['date'],
                tableEF['finance_id'],
                tableEF['featuresToEat'],
                tableRBFinance['name'].alias('financeName'),
                tableEF['typeFeed'],
                tableRBMealTime['name'].alias('mealTimeName'),
                tableRBMealTime['code'].alias('mealTimeCode'),
                tableRBDiet['name'].alias('dietName'),
                tableRBDiet['code'].alias('dietCode'),
                tableSocStatus['id'].alias('foreigner')
                ]
        queryTable = tableEvent.innerJoin(tableEF, tableEF['event_id'].eq(tableEvent['id']))
        queryTable = queryTable.innerJoin(tableClient, tableEvent['client_id'].eq(tableClient['id']))
        queryTable = queryTable.innerJoin(tableRBMealTime, tableEF['mealTime_id'].eq(tableRBMealTime['id']))
        queryTable = queryTable.innerJoin(tableRBDiet, tableEF['diet_id'].eq(tableRBDiet['id']))
        queryTable = queryTable.leftJoin(tableRBFinance, tableEF['finance_id'].eq(tableRBFinance['id']))
        queryTable = queryTable.leftJoin(tableSocStatus, [tableSocStatus['client_id'].eq(tableClient['id']), tableSocStatus['socStatusClass_id'].eq('8'), tableSocStatus['socStatusType_id'].ne('249'), tableSocStatus['deleted'].eq('0')])
        cond = [ tableEF['date'].dateEq(feedDate),
                 tableEF['deleted'].eq(0),
                 tableEF['mealTime_id'].isNotNull(),
                 tableEF['diet_id'].isNotNull(),
                 tableEF['refusalToEat'].eq(0),
                 tableEvent['deleted'].eq(0),
                 tableEvent['client_id'].inlist(clientIdList),
                 tableClient['deleted'].eq(0)
               ]
        if typeFeed == 1:
            cond.append(tableEF['typeFeed'].eq(0))
        elif typeFeed == 2:
            cond.append(tableEF['typeFeed'].eq(1))
        if time:
            dateTime = QDateTime(feedDate, time)
        else:
            dateTime = QDateTime(feedDate, QTime(9, 0))
        if dateTime:
            cond.append(db.joinOr([tableEvent['setDate'].isNull(), tableEvent['setDate'].le(dateTime)]))
            cond.append(db.joinOr([tableEvent['execDate'].isNull(), tableEvent['execDate'].ge(dateTime)]))
        stmt = db.selectDistinctStmt(queryTable, cols, cond, u'rbMealTime.code, rbDiet.code')
        query = db.query(stmt)

        while query.next():
            record    = query.record()
            clientId = forceRef(record.value('client_id'))
            eventId = forceRef(record.value('eventId'))
            financeId = forceRef(record.value('finance_id'))
            mealTimeId = forceInt(record.value('mealTime_id'))
            typeFeed = forceInt(record.value('typeFeed'))
            dietId = forceInt(record.value('diet_id'))
            foreigner = 1 if forceRef(record.value('foreigner')) else 0
            featuresToEat = forceString(record.value('featuresToEat'))

            if typeFeed:
                if clientId and clientId not in patronIdFeedList:
                    patronIdFeedList.append(clientId)
            else:
                if clientId and clientId not in clientIdFeedList:
                    clientIdFeedList.append(clientId)

            feedData.append({
                                'finance': context.getInstance(CFinanceInfo, financeId),
                                'mealTime': context.getInstance(CMealTimeInfo, mealTimeId),
                                'diet': context.getInstance(CDietInfo, dietId),
                                'isPatron': typeFeed,
                                'eventId': eventId,
                                'foreigner': foreigner,
                                'featuresToEat':featuresToEat,
                                'event': context.getInstance(CEventInfo, eventId),
                        })
    return feedData,  clientIdFeedList, patronIdFeedList

class CEventListWithDopInfo(CInfoList):
    def __init__(self,  context, idList, bedList):
        CInfoList.__init__(self, context)
        self._idList = idList
        self._bedList = bedList

    def _load(self):
        self._items = [ (self.getInstance(CEventInfo, id), self._bedList[id]) for id in self._idList ]
        return True

class CHospitalBedsReport(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Коечный фонд')


    def build(self, descr, idList):
        db = QtGui.qApp.db
        table = db.table('vHospitalBed')
        tableInvolution = db.table('OrgStructure_HospitalBed_Involution')
        tableEx = table
        tableProfile = db.table('rbHospitalBedProfile')
        tableEx = tableEx.leftJoin(tableProfile, tableProfile['id'].eq(table['profile_id']))
        tableEx = tableEx.leftJoin(tableInvolution, db.joinAnd([tableInvolution['master_id'].eq(table['id']),
                                                                tableInvolution['involutionType'].ne(0),
                                                                u"""(NOW() BETWEEN OrgStructure_HospitalBed_Involution.begDate AND OrgStructure_HospitalBed_Involution.endDate)
                                                                OR (OrgStructure_HospitalBed_Involution.begDate IS NULL AND OrgStructure_HospitalBed_Involution.endDate IS NULL) 
                                                                OR (OrgStructure_HospitalBed_Involution.begDate <= NOW() AND OrgStructure_HospitalBed_Involution.endDate IS NULL)"""]))
        currentDatetime = QDateTime.currentDateTime()
        cond = [table['id'].inlist(idList)]
        stmt = db.selectStmt(tableEx,
                             fields="""vHospitalBed.*, OrgStructure_HospitalBed_Involution.involutionType, rbHospitalBedProfile.name as profileName,
                             IF(vHospitalBed.`endDate` < CURDATE(), 1, 0) as isClosed,
                             (SELECT COUNT(ActionBed.value)
                              FROM ActionProperty_HospitalBed as ActionBed
                              left join ActionProperty on ActionProperty.id = ActionBed.id
                              left join Action on Action.actionType_id = (select id from ActionType where deleted = 0 and flatCode = 'moving') and Action.id = ActionProperty.action_id AND Action.deleted = 0
                              WHERE ActionBed.value = vHospitalBed.id AND Action.begDate < NOW() AND Action.endDate IS NULL AND Action.status = 0) AS cntBusy,
                              (SELECT COUNT(ActionBed.value)
                              FROM ActionProperty_HospitalBed as ActionBed
                              left join ActionProperty on ActionProperty.id = ActionBed.id
                              left join Action on Action.actionType_id = (select id from ActionType where deleted = 0 and flatCode = 'moving') and Action.id = ActionProperty.action_id AND Action.deleted = 0
                              WHERE ActionBed.value = vHospitalBed.id AND Action.begDate < NOW() AND Action.endDate IS NULL AND Action.status = 1) AS cntReserved""",
                             where=cond)
        query = db.query(stmt)

        reportData = {}
        while query.next():
            record = query.record()
            orgStructureId = forceInt(record.value('master_id'))
            profileName = forceString(record.value('profileName'))
            involution = forceInt(record.value('involutionType'))
            relief = forceInt(record.value('relief'))
            isClosed = forceInt(record.value('isClosed'))
            relief = 1 if relief == 0 else relief
            cntBusy = forceInt(record.value('cntBusy'))
            cntReserved = forceInt(record.value('cntReserved'))
            reportSubTable = reportData.setdefault(orgStructureId, {})
            row = reportSubTable.setdefault(profileName, [0, 0, 0, 0, 0, 0])
            row[0] += relief
            if isClosed:
                row[5] += relief
            elif involution > 0:
                row[4] += relief
            else:
                row[1] += relief - cntReserved - cntBusy
                row[2] += cntReserved
                row[3] += cntBusy

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertText(descr)
        cursor.insertBlock()

        tableColumns = [
            ('40%', [u'Профиль'], CReportBase.AlignLeft),
            ('10%', [u'Всего'], CReportBase.AlignRight),
            ('10%', [u'Свободно'], CReportBase.AlignRight),
            ('10%', [u'Резерв'], CReportBase.AlignRight),
            ('10%', [u'Занято'], CReportBase.AlignRight),
            ('10%', [u'Свернуто (временно)'], CReportBase.AlignRight),
            ('10%', [u'Закрыто'], CReportBase.AlignRight)
            ]

        table = createTable(cursor, tableColumns)
        self.genOrgStructureReport(table, reportData, len(tableColumns))
        return doc


    def genOrgStructureReport(self, table, reportData, rowSize):
        model = COrgStructureModel(None, QtGui.qApp.currentOrgId())
        item = model.getRootItem()
        total = self.genOrgStructureReportForItem(table, reportData, item, rowSize)
        self.genTotalEx(table, u'ИТОГО', rowSize, total)


    def dataPresent(self, reportData, item):
        reportSubTable = reportData.get(item.id(), None)
        return bool(reportSubTable)


    def dataPresentInChildren(self, reportData, item):
        for subitem in item.items():
            if self.dataPresent(reportData, subitem) or self.dataPresentInChildren(reportData, subitem):
                return True
        return False


    def genTitle(self, table, item, rowSize):
        i = table.addRow()
        table.mergeCells(i, 0, 1, rowSize)
        table.setText(i, 0, item.name(), CReportBase.TableHeader)


    def genTotalEx(self, table, title, rowSize, total):
        i = table.addRow()
        table.setText(i, 0, title)
        for j, v in enumerate(total):
            table.setText(i, j + 1, v)


    def genTotal(self, table, item, rowSize, total):
        self.genTotalEx(table, u'Итого по ' + item.name(), rowSize, total)


    def genTable(self, table, reportData, item, rowSize):
        self.genTitle(table, item, rowSize)
        total = [0, 0, 0, 0, 0, 0]
        reportSubTable = reportData.get(item.id(), None)
        if reportSubTable:
            profiles = reportSubTable.keys()
            profiles.sort()
            for profile in profiles:
                i = table.addRow()
                row = reportSubTable[profile]
                table.setText(i, 0, profile)
                for j, v in enumerate(row):
                    table.setText(i, j+1, v)
                    total[j] += v
        return total


    def genOrgStructureReportForItem(self, table, reportData, item, rowSize):
        total = [0, 0, 0, 0, 0, 0]
        if item.childCount() == 0:
            if self.dataPresent(reportData, item):
                total = self.genTable(table, reportData, item, rowSize)
                self.genTotal(table, item, rowSize, total)
        else:
            if self.dataPresent(reportData, item):
                total = self.genTable(table, reportData, item, rowSize)
                if self.dataPresentInChildren(reportData, item):
                    for subitem in item.items():
                        subtotal = self.genOrgStructureReportForItem(table, reportData, subitem, rowSize)
                        total = [x+y for x, y in zip(total,subtotal)]
                self.genTotal(table, item, rowSize, total)
            elif self.dataPresentInChildren(reportData, item):
                self.genTitle(table, item, rowSize)
                for subitem in item.items():
                    subtotal = self.genOrgStructureReportForItem(table, reportData, subitem, rowSize)
                    total = [x+y for x, y in zip(total,subtotal)]
                self.genTotal(table, item, rowSize, total)
        return total


class CFeedReportDialog(QtGui.QDialog, Ui_FeedReportDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.edtBegDate.setDate(QDate.currentDate().addDays(1))


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.edtBegDate.setDate(params.get('feedDate', QDate.currentDate()))
        self.cmbTypePrint.setCurrentIndex(params.get('typePrint', 0))


    def params(self):
        result = {}
        result['feedDate'] = self.edtBegDate.date()
        result['typePrint'] = self.cmbTypePrint.currentIndex()
        return result
