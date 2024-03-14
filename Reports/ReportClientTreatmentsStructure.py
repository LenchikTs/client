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

from library.SortedDict import CSortedDict
from library.Utils      import forceInt, forceString
from Reports.ReportBase import CReportBase, createTable
from Reports.Report     import CReport
from Reports.ReportUniversalEventList import CEventTypeTableModel
from Events.Utils       import getWorkEventTypeFilter

from Reports.Ui_ClientTreatmentsStructureReportSetupDialog import Ui_ClientTreatmentsStructureReportSetupDialog



class CClientTreatmentsStructureReport(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Структура обращений пациентов')
        self.setOrientation(QtGui.QPrinter.Landscape)

    def getSetupDialog(self, parent):
        result = CClientTreatmentsStructureReportSetup(parent)
        result.setTitle(self.title())
        return result

    def selectData(self, begDate, endDate, chkAge, edtAgeFrom, edtAgeTo, eventTypeIdList):
        data = CSortedDict()
        data[u'Местное население'] = {u'М':[0]*20, u'Ж':[0]*20}
        data[u'Иногородние'] = {u'М':[0]*20, u'Ж':[0]*20}
        data[u'Иностранцы'] = {u'М':[0]*20, u'Ж':[0]*20}

        clientsCount = {
            u'Иностранцы': {u'М':0, u'Ж':0},
            u'Местное население': {u'М':0, u'Ж':0},
            u'Иногородние': {u'М':0, u'Ж':0}
        }
        defaultKladrCode = QtGui.qApp.defaultKLADR()
        db = QtGui.qApp.db
        tableEvent = db.table('Event')

        ageCond = ''
        if chkAge:
            ageCond = 'AND age(Client.birthDate, \'%s\') >= %s AND age(Client.birthDate, \'%s\') <= %s' % (endDate.toString('yyyy-MM-dd'), edtAgeFrom, begDate.toString('yyyy-MM-dd'), edtAgeTo)

        stmtForeigners = '''
            SELECT Client.id as clientId, Client.sex as clientSex, rbSocStatusType.code as citizenship
                FROM Client
              INNER JOIN ClientSocStatus ON ClientSocStatus.client_id = Client.id
              INNER JOIN rbSocStatusClass ON rbSocStatusClass.id = ClientSocStatus.socStatusClass_id
              INNER JOIN rbSocStatusType  ON rbSocStatusType.id  = ClientSocStatus.socStatusType_id
              WHERE rbSocStatusClass.code = '8'
                AND (ClientSocStatus.begDate IS NULL OR ClientSocStatus.begDate<='%s')
                AND (ClientSocStatus.endDate IS NULL OR ClientSocStatus.endDate>='%s')
                AND ClientSocStatus.deleted = 0 %s
        '''%(endDate.toString('yyyy-MM-dd'), begDate.toString('yyyy-MM-dd'), ageCond)

        query = db.query(stmtForeigners)
        foreignersIdList = []
        while query.next():
            record = query.record()
            clientId = forceInt(record.value('clientId'))
            clientSex = u'М' if forceInt(record.value('clientSex')) == 1 else u'Ж'
            citizenship = forceString(record.value('citizenship'))
            if citizenship != u'м643':
                clientsCount[u'Иностранцы'][clientSex] += 1
                foreignersIdList.append(clientId)

        foreignersCond = ''
        if foreignersIdList:
            foreignersCond = ' AND Client.id not in (%s)' %(','.join(map(str, foreignersIdList)))

        stmtRusClients = '''
            SELECT
                COUNT(Client.id) as clientCount,
                Client.sex as clientSex,
                IF(AddressHouse.KLADRCode like '%s%%', 1, 0) as 'local'
            FROM
                Client
                    LEFT JOIN
                ClientAddress ON ClientAddress.id = (SELECT
                        MAX(id)
                    FROM
                        ClientAddress AS CA
                    WHERE
                        CA.type = 0 AND CA.deleted = 0
                            AND CA.client_id = Client.id)
                    LEFT JOIN
                Address ON Address.id = ClientAddress.address_id
                    LEFT JOIN
                AddressHouse ON AddressHouse.id = Address.house_id
            where
                Client.deleted = 0
                    %s %s
        group by clientSex, local
        '''%(defaultKladrCode[:2], foreignersCond, ageCond)

        query = db.query(stmtRusClients)
        while query.next():
            record = query.record()
            clientCount = forceInt(record.value('clientCount'))
            sex = u'М' if forceInt(record.value('clientSex')) == 1 else u'Ж'
            local = forceInt(record.value('local'))
            if local:
                clientsCount[u'Местное население'][sex] += clientCount
            else:
                clientsCount[u'Иногородние'][sex] += clientCount

        eventTypeCond = u''
        if eventTypeIdList:
            eventTypeCond = u' AND %s'%(db.joinAnd([tableEvent['eventType_id'].inlist(eventTypeIdList)]))

        stmt = '''
        select Client.id,
        getClientCitizenship(Client.id, Event.execDate) as 'citizenship',
        (select AddressHouse.KLADRCode from ClientAddress
                left join Address on Address.id = ClientAddress.address_id
                left join AddressHouse on AddressHouse.id = Address.house_id
                where ClientAddress.client_id = Client.id
                    and ClientAddress.type = 0
                    and ClientAddress.deleted = 0
                    and Address.deleted = 0
                    order by ClientAddress.modifyDateTime DESC
                    limit 1) as 'addressCode',
        Client.sex,
        count(Event.id) as eventCount,
        (select count(oldEvent.id)
            from Event as oldEvent
            where oldEvent.client_id = Client.id
                and oldEvent.execDate < '%s') as 'allEventsCount'

        from Event
        left join Client on Client.id = Event.client_id
        left join EventType on EventType.id = Event.eventType_id

        where %s
        and EventType.code != 'queue' %s
        %s

        group by Client.id
        ''' % (begDate.toString('yyyy-MM-dd'), tableEvent['execDate'].dateBetween(begDate, endDate), ageCond, eventTypeCond)
        query = db.query(stmt)
        while query.next():
            record = query.record()
            sex = u'М' if forceInt(record.value('sex')) == 1 else u'Ж'
            citizenship = forceString(record.value('citizenship'))
            if citizenship and citizenship != u'м643':
                eventCounter = data.setdefault(u'Иностранцы', {}).setdefault(sex, {})
            else:
                addressCode = forceString(record.value('addressCode'))
                if addressCode == defaultKladrCode:
                    eventCounter = data.setdefault(u'Местное население', {}).setdefault(sex, {})
                else:
                    eventCounter = data.setdefault(u'Иногородние', {}).setdefault(sex, {})
            eventCounter[0] += 1
            allEventsCount = forceInt(record.value('allEventsCount'))
            eventCount = forceInt(record.value('eventCount'))
            if allEventsCount == 0:
                eventCount -= 1
            if eventCount == 0:
                eventCounter[2] += 1
            elif eventCount == 1:
                eventCounter[4] += 1
            elif eventCount == 2:
                eventCounter[6] += 1
            elif eventCount == 3:
                eventCounter[8] += 1
            elif eventCount == 4:
                eventCounter[10] += 1
            elif eventCount == 5:
                eventCounter[12] += 1
            elif eventCount == 6:
                eventCounter[14] += 1
            elif eventCount == 7:
                eventCounter[16] += 1
            elif eventCount > 7:
                eventCounter[18] += 1

        for k in data.keys():
            for y in data[k].keys():
                data[k][y][1] = round((data[k][y][0]  *100.0/ clientsCount[k][y]) if clientsCount[k][y] else 0, 2)
                if data[k][y][0]:
                    data[k][y][3] = round(data[k][y][2]  *100.0/ data[k][y][0], 2)
                    data[k][y][5] = round(data[k][y][4]  *100.0/ data[k][y][0], 2)
                    data[k][y][7] = round(data[k][y][6]  *100.0/ data[k][y][0], 2)
                    data[k][y][9] = round(data[k][y][8]  *100.0/ data[k][y][0], 2)
                    data[k][y][11] = round(data[k][y][10]  *100.0/ data[k][y][0], 2)
                    data[k][y][13] = round(data[k][y][12]  *100.0/ data[k][y][0], 2)
                    data[k][y][15] = round(data[k][y][14]  *100.0/ data[k][y][0], 2)
                    data[k][y][17] = round(data[k][y][16]  *100.0/ data[k][y][0], 2)
                    data[k][y][19] = round(data[k][y][18]  *100.0/ data[k][y][0], 2)
        return data, clientsCount

    def build(self, params):
        begDate   = params.get('begDate', QDate())
        endDate   = params.get('endDate', QDate())
        chkAge     = params.get('chkAge', False)
        edtAgeFrom = params.get('ageFrom', 0)
        edtAgeTo      = params.get('ageTo', 150)
        eventTypeIdList = params.get('eventTypeIdList', None)

        tableColumns = [
            ('12%', [u'Название контингента',  '',  '1'],  CReportBase.AlignLeft),
            ('3%', [u'Пол',  '',  '2'],  CReportBase.AlignLeft),
            ('5%', [u'Всего человек', '',  '3'],     CReportBase.AlignRight),
            ('4%', [u'Всего обратилось',  u'кол-во',  '4'],      CReportBase.AlignRight),
            ('4%', [u'',  u'%',  '5'],      CReportBase.AlignRight),
            ('4%', [u'В т.ч. впервые', u'к-во', '6'], CReportBase.AlignRight),
            ('4%', [u'',  u'%',  '7'],      CReportBase.AlignRight),
            ('4%', [u'Повторно 1 раз', u'к-во', '8'],  CReportBase.AlignRight),
            ('4%', [u'',  u'%',  '9'],      CReportBase.AlignRight),
            ('4%', [u'Повторно 2 раза', u'к-во', '10'],  CReportBase.AlignRight),
            ('4%', [u'',  u'%',  '11'],      CReportBase.AlignRight),
            ('4%', [u'Повторно 3 раза', u'к-во', '12'],  CReportBase.AlignRight),
            ('4%', [u'',  u'%',  '13'],      CReportBase.AlignRight),
            ('4%', [u'Повторно 4 раза', u'к-во', '14'],  CReportBase.AlignRight),
            ('4%', [u'',  u'%',  '15'],      CReportBase.AlignRight),
            ('4%', [u'Повторно 5 раз',  u'к-во', '16'],  CReportBase.AlignRight),
            ('4%', [u'',  u'%',  '17'],      CReportBase.AlignRight),
            ('4%', [u'Повторно 6 раз',  u'к-во', '18'],  CReportBase.AlignRight),
            ('4%', [u'',  u'%',  '19'],      CReportBase.AlignRight),
            ('4%', [u'Повторно 7 раз',  u'к-во', '20'],  CReportBase.AlignRight),
            ('4%', [u'',  u'%',  '21'],      CReportBase.AlignRight),
            ('4%', [u'Повторно > 7 раз', u'к-во', '22'],  CReportBase.AlignRight),
            ('4%', [u'',  u'%',  '23'],      CReportBase.AlignRight),
            ]

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParamsEventTypeList(cursor, params)
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        table = createTable(cursor, tableColumns)

        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 2, 1)
        table.mergeCells(0, 3, 1, 2)
        table.mergeCells(0, 5, 1, 2)
        table.mergeCells(0, 7, 1, 2)
        table.mergeCells(0, 9, 1, 2)
        table.mergeCells(0, 11, 1, 2)
        table.mergeCells(0, 13, 1, 2)
        table.mergeCells(0, 15, 1, 2)
        table.mergeCells(0, 17, 1, 2)
        table.mergeCells(0, 19, 1, 2)
        table.mergeCells(0, 21, 1, 2)

        data, clientsCount = self.selectData(begDate, endDate, chkAge, edtAgeFrom, edtAgeTo, eventTypeIdList)

        sum = {u'М':[0]*21, u'Ж':[0]*21}

        for k in data.keys():
            localSum = [0]*21
            for y in data[k].keys():
                row = table.addRow()
                table.setText(row, 1, y)
                table.setText(row, 2, clientsCount[k][y])
                sum[y][0] += clientsCount[k][y]
                localSum[0] += clientsCount[k][y]
                for i, count in enumerate(data[k][y]):
                    table.setText(row, i+3, count)
                    sum[y][i+1] += count
                    localSum[i+1] += count
            localSum[2] = round((localSum[1] *100.0/ localSum[0]) if localSum[0] else 0, 2)
            if localSum[1]:
                for i in (4, 6, 8, 10, 12, 14, 16, 18, 20):
                    localSum[i] = round((localSum[i-1] *100.0/ localSum[1]), 2)
            else:
                for i in (4, 6, 8, 10, 12, 14, 16, 18, 20):
                    localSum[i] = 0
            row = table.addRow()
            table.setText(row, 1, u'М+Ж')
            for i, count in enumerate(localSum):
                table.setText(row, i+2, count)

            table.setText(row, 0, k)
            table.mergeCells(row-2, 0, 3, 1)

        for k in (u'М', u'Ж'):
            sum[k][2] = round((sum[k][1] *100.0/ sum[k][0]) if sum[k][0] else 0, 2)
            if sum[k][1]:
                for i in (4, 6, 8, 10, 12, 14, 16, 18, 20):
                    sum[k][i] = round((sum[k][i-1] *100.0/ sum[k][1]), 2)
            else:
                for i in (4, 6, 8, 10, 12, 14, 16, 18, 20):
                    sum[k][i] = 0

        localSum = [0]*21
        for k in (u'М', u'Ж'):
            row = table.addRow()
            table.setText(row, 1, k)
            for i, count in enumerate(sum[k]):
                table.setText(row, i+2, sum[k][i])
                localSum[i] += sum[k][i]

        localSum[2] = round((localSum[1] *100.0/ localSum[0]) if localSum[0] else 0, 2)
        if localSum[1]:
            for i in (4, 6, 8, 10, 12, 14, 16, 18, 20):
                localSum[i] = round((localSum[i-1] *100.0/ localSum[1]), 2)
        else:
            for i in (4, 6, 8, 10, 12, 14, 16, 18, 20):
                localSum[i] = 0

        row = table.addRow()
        table.setText(row, 1, u'М+Ж')
        for i, count in enumerate(localSum):
            table.setText(row, i+2, count)

        table.setText(row, 0, u'Всего')
        table.mergeCells(row-2, 0, 3, 1)

        return doc


class CClientTreatmentsStructureReportSetup(QtGui.QDialog, Ui_ClientTreatmentsStructureReportSetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.tableModel = CEventTypeTableModel(self)
        self.tableSelectionModel = QtGui.QItemSelectionModel(self.tableModel, self)
        self.tableSelectionModel.setObjectName('tableSelectionModel')
        self.setupUi(self)
        self.filter =  getWorkEventTypeFilter(isApplyActive=True)
        self.tblEventType.setModel(self.tableModel)
        self.tblEventType.setSelectionModel(self.tableSelectionModel)
        self.tblEventType.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.tblEventType.installEventFilter(self)
        self.tblEventType.model().setIdList(self.setEventTypeIdList())


    def getSelectEventTypeList(self):
        return self.tblEventType.selectedItemIdList()


    def setSelectEventTypeList(self, eventTypeList):
        self.tblEventType.clearSelection()
        if eventTypeList:
            self.tblEventType.setSelectedItemIdList(eventTypeList)


    def setEventTypeIdList(self):
        db = QtGui.qApp.db
        tableEventType = db.table('EventType')
        cond = [tableEventType['deleted'].eq(0)]
        if self.filter:
            cond.append(self.filter)
        return db.getDistinctIdList(tableEventType, tableEventType['id'].name(),
                              where=cond,
                              order=u'EventType.code ASC, EventType.name ASC')


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.chkAge.setChecked(params.get('chkAge', False))
        ageFrom = params.get('ageFrom', 0)
        ageTo = params.get('ageTo', 0)
        self.edtAgeFrom.setValue(ageFrom if ageFrom else 0)
        self.edtAgeTo.setValue(ageTo if ageTo else 150)
        self.setSelectEventTypeList(params.get('eventTypeIdList', None))


    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['chkAge'] = self.chkAge.isChecked()
        result['ageFrom'] = self.edtAgeFrom.value() if self.chkAge.isChecked() else None
        result['ageTo'] = self.edtAgeTo.value() if self.chkAge.isChecked() else None
        result['eventTypeIdList'] = self.getSelectEventTypeList()
        return result


    @pyqtSignature('int')
    def on_chkAge_stateChanged(self, state):
        self.edtAgeFrom.setEnabled(state)
        self.edtAgeTo.setEnabled(state)
        self.lblAgeTo.setEnabled(state)
        self.lblAgeFrom.setEnabled(state)

