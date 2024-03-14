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

from library.SortedDict import CSortedDict
from library.Utils      import forceInt, forceString, formatSex

from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.Ui_ReportF1SetupDialog import Ui_ReportF1SetupDialog


class CReportF1chSetup(QtGui.QDialog, Ui_ReportF1SetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        year = QDate.currentDate().year()
        begDate = params.get('begDate', QDate(year, 1, 1))
        endDate = params.get('endDate', QDate(year+1, 1, 1))
        self.edtBegDate.setDate(begDate)
        self.edtEndDate.setDate(endDate)


    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        return result


class CReportF1_1000(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Возрастно-половой состав беспризорных и безнадзорных несовершеннолетних. (1000)')


    def getSetupDialog(self, parent):
        result = CReportF1chSetup(parent)
        result.setTitle(self.title())
        return result


    def selectData(self, begDate, endDate):
        data = {}
        if not begDate or not endDate:
            return data
        for i in xrange(18): data.update({i:{u'М':0, u'Ж':0}})
        db = QtGui.qApp.db
        tableClient = db.table('Client')
        tableAction = db.table('Action').alias('A')
        tableAT = db.table('ActionType')
        tableEvent = db.table('Event')
        tableCSS = db.table('ClientSocStatus')
        tableRBSS = db.table('rbSocStatusType')

        table = tableClient.innerJoin(tableEvent, tableEvent['client_id'].eq(tableClient['id']))
        table = table.leftJoin(tableCSS, tableCSS['client_id'].eq(tableClient['id']))
        table = table.leftJoin(tableRBSS, tableRBSS['id'].eq(tableCSS['socStatusType_id']))

        movTable = tableAction.leftJoin(tableAT, tableAT['id'].eq(tableAction['actionType_id']))
        movCond = [tableAction['event_id'].eq(tableEvent['id']),
                        tableAT['flatCode'].eq('moving')]

        cols = [ #'count(DISTINCT Client.id) as count',  # Это если считать по головам
                    'count(Client.id) as count',
                    'age(Client.birthDate, \'%s\') as agef'%endDate.toString('yyyy-MM-dd'),
                    'Client.sex']

        cond = [tableRBSS['code'].eq(u'с00'),
                    tableEvent['setDate'].dateBetween(begDate, endDate),
                    db.existsStmt(movTable, movCond),
                    tableEvent['prevEvent_id'].isNull(),
                    tableCSS['deleted'].eq(0)]

        recordList = db.getRecordListGroupBy(table, cols, cond, 'agef,sex')
        for record in recordList:
            count = forceInt(record.value(0))
            age = forceInt(record.value(1))
            sex = formatSex(record.value(2))
            sexData = data.setdefault(age, {})
            sexData[sex] = count
        return data


    def build(self, params):
        begDate = params.get('begDate',  None)
        endDate = params.get('endDate',  None)

        tableColumns = [
            ('20%', [u'Наименование показателей', '', '1'], CReportBase.AlignLeft),
            ('20%', [u'N строки', '', '2'], CReportBase.AlignLeft),
            ('20%', [u'Всего', '', '3'], CReportBase.AlignLeft),
            ('20%', [u'В том числе:', u'девочки', '4'], CReportBase.AlignLeft),
            ('20%', ['', u'мальчики', '5'], CReportBase.AlignLeft)
            ]

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        html = u"""
        <b align="center"><h3>Раздел 1.<br>Возрастно-половой состав беспризорных и безнадзорных несовершеннолетних, находившихся в лечебно-профилактическом учреждении</h3>
за период с %s по %s</b>
<table width="100%%", border=0, margin=0>
<tr><td><b>(1000)</b></td><td align="right">Код по ОКЕИ: человек – 792</td></tr></table>
        """%(begDate.toString('dd.MM.yyyy'), endDate.toString('dd.MM.yyyy'))
        cursor.insertHtml(html)

#        cursor.setCharFormat(CReportBase.ReportTitle)
#        cursor.insertText(self.title())
#        cursor.insertBlock()
        #self.dumpParams(cursor, params)
        cursor.insertBlock()
        table = createTable(cursor, tableColumns)

        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 2, 1)
        table.mergeCells(0, 3, 1, 3)

        data = self.selectData(begDate, endDate)
        sumRow = table.addRow()
        sumB = 0
        sumG = 0
        for age in xrange(18):
            i = table.addRow()
            table.setText(i, 0, self.getAgeString(age))
            table.setText(i, 1, '%02d'%(age+2))
            table.setText(i, 2, data[age][u'М'] + data[age][u'Ж'])
            table.setText(i, 3, data[age][u'Ж'])
            table.setText(i, 4, data[age][u'М'])
            sumB += data[age][u'М']
            sumG += data[age][u'Ж']
        table.setText(sumRow, 0, u'Численность беспризорных и безнадзорных несовершеннолетних, находившихся в лечебно-профилактическом учреждении - всего (сумма строк 02-19)')
        table.setText(sumRow, 1, '01')
        table.setText(sumRow, 2, sumB+sumG)
        table.setText(sumRow, 3, sumG)
        table.setText(sumRow, 4, sumB)
        return doc


    def getAgeString(self, age):
        if age == 0:
            return u'в том числе в возрасте (число исполнившихся лет на отчетную дату) до 1 года'
        elif age == 1:
            return u'1 год'
        elif age < 5:
            return u'%i года'%age
        else:
            return u'%i лет'%age


class CReportF1_2000(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Возрастно-половой состав беспризорных и безнадзорных несовершеннолетних')


    def getSetupDialog(self, parent):
        result = CReportF1chSetup(parent)
        result.setTitle(self.title())
        return result


    def selectData(self, begDate, endDate):
        visitData = dict((k,0) for k in xrange(4))
        leavedData = dict((k,0) for k in xrange(8))
        inspectData = CSortedDict()
        if not begDate or not endDate:
            return visitData, inspectData
        inspectData[u'Педиатр'] = 0
        inspectData[u'Психиатр'] = 0
        inspectData[u'Дерматолог'] = 0
        inspectData[u'Психонарколог'] = 0
        inspectData[u'Гинеколог']  = 0
        inspectData[u'госп']  = 0
        inspectData[u'отказ']  = 0

        specQueryActions = """
                (select GROUP_CONCAT(DISTINCT P.speciality_id) from Action as A
                LEFT JOIN
                Person AS P ON P.id = A.person_id
                where A.event_id = Event.id
                GROUP BY A.event_id
                ) as ActionsSpecialities
            """

        specQueryVisits = """
                (select GROUP_CONCAT(DISTINCT P.speciality_id) from Visit as V
                LEFT JOIN
                Person AS P ON P.id = V.person_id
                where V.event_id = Event.id
                GROUP BY V.event_id
                ) as VisitsSpecialities
            """

        db = QtGui.qApp.db
        tableClient = db.table('Client')
        tableAction = db.table('Action')
        tableAT = db.table('ActionType')
        tableEvent = db.table('Event')
        tableCSS = db.table('ClientSocStatus')
        tableRBSS = db.table('rbSocStatusType')
        tableAP = db.table('ActionProperty')
        tableAPT = db.table('ActionPropertyType')
        tableAPS = db.table('ActionProperty_String')
        tableAPOS = db.table('ActionProperty_OrgStructure')
        tableEventPerson = db.table('Person')
        tableSpeciality = db.table('rbSpeciality')

        deliveredTable = tableAP.leftJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
        deliveredTable = deliveredTable.leftJoin(tableAPS, tableAPS['id'].eq(tableAP['id']))

        table = tableClient.innerJoin(tableEvent, tableEvent['client_id'].eq(tableClient['id']))
        table = table.leftJoin(tableCSS, tableCSS['client_id'].eq(tableClient['id']))
        table = table.leftJoin(tableRBSS, tableRBSS['id'].eq(tableCSS['socStatusType_id']))
        table = table.leftJoin(tableEventPerson, tableEventPerson['id'].eq(tableEvent['execPerson_id']))

        cols = [ tableEventPerson['speciality_id'].name(),
                    specQueryActions,
                    specQueryVisits
                    ]

        cond = [tableRBSS['code'].eq(u'с00'),
                    tableEvent['setDate'].dateBetween(begDate, endDate),
                    tableCSS['deleted'].eq(0),
                    'age(Client.birthDate, \'%s\') < 18'%endDate.toString('yyyy-MM-dd')]

        specialityList = {}
        for record in db.getRecordList(tableSpeciality, [tableSpeciality['id'], tableSpeciality['name']], [tableSpeciality['name'].inlist(inspectData.keys())]):
            id = forceInt(record.value(0))
            name = forceString(record.value(1))
            specialityList[id] = name

        for record in db.getRecordList(table, cols, cond):
            idList = set(map(int, filter(None, ','.join([forceString(record.value(i)) for i in range(3)]).split(','))))
            for id in idList:
                name = specialityList.get(id, None)
                if name in inspectData:
                    inspectData[name] += 1

        table = tableEvent.leftJoin(tableClient, tableClient['id'].eq(tableEvent['client_id']))
        table = table.leftJoin(tableCSS, tableCSS['client_id'].eq(tableClient['id']))
        table = table.leftJoin(tableRBSS, tableRBSS['id'].eq(tableCSS['socStatusType_id']))

        tableHasHosp = tableAction.leftJoin(tableAT, tableAT['id'].eq(tableAction['actionType_id']))
        tableHasHosp = tableHasHosp.leftJoin(tableAP, tableAP['action_id'].eq(tableAction['id']))
        tableHasHosp = tableHasHosp.leftJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
        tableHasHosp = tableHasHosp.leftJoin(tableAPOS, tableAPOS['id'].eq(tableAP['id']))

        hasHospCond = [tableAction['event_id'].eq(tableEvent['id']),
                        tableAT['flatCode'].eq('received'),
                        tableAPT['name'].eq(u'Направлен в отделение')]

        tableHasRefuse = tableAction.leftJoin(tableAT, tableAT['id'].eq(tableAction['actionType_id']))
        tableHasRefuse = tableHasRefuse.leftJoin(tableAP, tableAP['action_id'].eq(tableAction['id']))
        tableHasRefuse = tableHasRefuse.leftJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
        tableHasRefuse = tableHasRefuse.leftJoin(tableAPS, tableAPS['id'].eq(tableAP['id']))

        hasRefuseCond = [tableAction['event_id'].eq(tableEvent['id']),
                        tableAT['flatCode'].eq('received'),
                        tableAPT['name'].eq(u'Причина отказа от госпитализации')]

        tableDelivered = tableAction.leftJoin(tableAT, tableAT['id'].eq(tableAction['actionType_id']))
        tableDelivered = tableDelivered.leftJoin(tableAP, tableAP['action_id'].eq(tableAction['id']))
        tableDelivered = tableDelivered.leftJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
        tableDelivered = tableDelivered.leftJoin(tableAPS, tableAPS['id'].eq(tableAP['id']))

        hasDeliveredCond = [tableAction['event_id'].eq(tableEvent['id']),
                        tableAT['flatCode'].eq('received'),
                        tableAPT['name'].eq(u'Кем доставлен')]

        cols = ['(%s) as hasHosp'%db.selectStmt(tableHasHosp, tableAPOS['value'].name(), hasHospCond),
                    '(%s) as hasRefuse'%db.selectStmt(tableHasRefuse, tableAPS['value'].name(), hasRefuseCond),
                    '(%s) as delivered'%db.selectStmt(tableDelivered, tableAPS['value'].name(), hasDeliveredCond)]

        for record in db.getRecordList(table, cols, cond):
            visitData[0] += 1
            if forceInt(record.value(0)):
                inspectData[u'госп'] += 1
            if forceInt(record.value(1)):
                inspectData[u'отказ'] += 1
            if forceString(record.value(2)) == u'Самостоятельно':
                visitData[3] += 1
            else:
                visitData[2] += 1

        table = tableEvent.leftJoin(tableClient, tableClient['id'].eq(tableEvent['client_id']))
        table = table.leftJoin(tableCSS, tableCSS['client_id'].eq(tableClient['id']))
        table = table.leftJoin(tableRBSS, tableRBSS['id'].eq(tableCSS['socStatusType_id']))
        table = table.leftJoin(tableAction, tableAction['event_id'].eq(tableEvent['id']))
        table = table.leftJoin(tableAT, tableAT['id'].eq(tableAction['actionType_id']))

        tableResult = tableAP.leftJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
        tableResult = tableResult.leftJoin(tableAPS, tableAPS['id'].eq(tableAP['id']))
        condResult = [tableAP['action_id'].eq(tableAction['id']),
                                tableAPT['name'].eq(u'Исход госпитализации')]


        cols = ['(%s) as result'%db.selectStmt(tableResult, tableAPS['value'].name(), condResult)]


        tableMoving = tableAP.leftJoin(tableAPT, tableAPT['id'].eq(tableAP['type_id']))
        tableMoving = tableMoving.leftJoin(tableAPOS, tableAPOS['id'].eq(tableAP['id']))
        movingCond = [tableAP['action_id'].eq(tableAction['id']),
                                tableAPT['name'].eq(u'Отделение')]

        cond.append(db.existsStmt(tableMoving, movingCond))

        for record in db.getRecordList(table, cols, cond):
            if forceString(record.value(0)) == u'Умер':
                leavedData[6] += 1
            else:
                leavedData[7] += 1

        return visitData, inspectData, leavedData

    def build(self, params):
        begDate = params.get('begDate',  None)
        endDate = params.get('endDate',  None)

        tableColumns = [
            ('60%', [u'Наименование показателей', '1'], CReportBase.AlignLeft),
            ('20%', [u'N строки', '2'], CReportBase.AlignLeft),
            ('20%', [u'', '3'], CReportBase.AlignLeft)
            ]

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        #cursor.insertBlock()
        html = u"""
        <b align="center"><h3>Раздел 2.<br>Сведения о беспризорных и безнадзорных несовершеннолетних, доставленных в
лечебно-профилактическое учреждение</h3>
за период с %s по %s</b>
<table width="100%%", border=0, margin=0>
<tr><td><b>(2000)</b></td><td align="right">Код по ОКЕИ: человек – 792</td></tr></table>
        """%(begDate.toString('dd.MM.yyyy'), endDate.toString('dd.MM.yyyy'))
        cursor.insertHtml(html)

        #cursor.setCharFormat(CReportBase.ReportTitle)
        #cursor.insertText(self.title())
#        cursor.insertBlock()
#        cursor.insertBlock()
        table = createTable(cursor, tableColumns)

        strNum = 20

        visitData, inspectData, leavedData = self.selectData(begDate, endDate)

        visitMap = {0: u'Численность беспризорных и безнадзорных несовершеннолетних, \
доставленных в лечебное учреждение, всего (сумма строк 21-23)',
                        1: u'сотрудниками органов внутренних дел',
                        2: u'гражданами',
                        3: u'самостоятельно обратились'}

        for key in sorted(visitData.keys()):
            i = table.addRow()
            table.setText(i, 0, visitMap[key])
            table.setText(i, 1, strNum)
            table.setText(i, 2, visitData[key])
            strNum += 1


        inspectMap = {u'Педиатр': u'Из общего числа доставленных (обратившихся) (из стр. 20):\nосмотрено врачами:\nпедиатром',
                            u'Психиатр':u'психиатром',
                            u'Дерматолог': u'дерматологом',
                            u'Психонарколог': u'психонаркологом',
                            u'Гинеколог': u'гинекологом',
                            u'госп': u'госпитализировано',
                            u'отказ': u'отказано в госпитализации'}
        for key in inspectData:
            i = table.addRow()
            table.setText(i, 0, inspectMap[key])
            table.setText(i, 1, strNum)
            table.setText(i, 2, inspectData[key])
            strNum += 1

        leavedMap = {
                0: u'Из числа госпитализированных (сумма строк 31-38) выбыло:\nпередано родителям или законным представителям',
                1: u'в учреждения социальной защиты населения',
                2: u'в учреждения системы образования',
                3: u'в учреждения системы здравоохранения  (дома ребенка)',
                4: u'в  учреждения временного содержания несовершеннолетних МВД России',
                5: u'самовольно покинули учреждение',
                6: u'умерло',
                7: u'прочее'
                }

        for key in sorted(leavedData.keys()):
            i = table.addRow()
            table.setText(i, 0, leavedMap[key])
            table.setText(i, 1, strNum)
            table.setText(i, 2, leavedData[key])
            strNum += 1

        return doc

if __name__ == '__main__':
    from s11main import CS11mainApp
    QtGui.qApp = CS11mainApp(None, False, None, None, None)
    QtGui.qApp.openDatabase()
    CReportF1_2000(None).exec_()
