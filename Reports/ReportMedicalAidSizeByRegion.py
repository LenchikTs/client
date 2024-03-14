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

from library.Utils      import forceDouble, forceInt, forceRef, forceString

from Events.Utils       import getWorkEventTypeFilter
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Orgs.Utils         import getOrgStructureDescendants


def calculateData(isDivideToRegions, stringBy, begDate, endDate, eventTypeId, orgStructureId, personId, sex, ageFrom, ageTo, specialityId, typeFinanceId, address):
    db = QtGui.qApp.db
    tableVisit  = db.table('Visit')
    tableEvent  = db.table('Event')
    tableAction = db.table('Action')
    tableEventType = db.table('EventType')
    tablePerson = db.table('vrbPersonWithSpeciality')
    tableClient = db.table('Client')
    cond = []
    if stringBy == 0:
        cond.append(tableEvent['execDate'].ge(begDate))
        cond.append(tableEvent['execDate'].lt(endDate.addDays(1)))
        string = 'Event'
        if personId:
            cond.append(tableEvent['execPerson_id'].eq(personId))
        if typeFinanceId:
            cond.append(tableEventType['finance_id'].eq(typeFinanceId))
    elif stringBy == 1:
        cond.append(tableVisit['date'].ge(begDate))
        cond.append(tableVisit['date'].lt(endDate.addDays(1)))
        string = 'Visit \n LEFT JOIN Event On Event.id = Visit.event_id'
        if personId:
            cond.append(tableVisit['person_id'].eq(personId))
        if typeFinanceId:
            cond.append(tableVisit['finance_id'].eq(typeFinanceId))
    else:
        cond.append(tableAction['endDate'].ge(begDate))
        cond.append(tableAction['endDate'].lt(endDate.addDays(1)))
        string = 'Action \n LEFT JOIN Event On Event.id = Action.event_id'
        if personId:
            cond.append(tableAction['person_id'].eq(personId))
        if typeFinanceId:
            cond.append(tableAction['finance_id'].eq(typeFinanceId))
#    cond.append(db.joinOr([tableEvent['execDate'].lt(endDate.addDays(1)), tableEvent['execDate'].isNull()]))
    if eventTypeId:
        cond.append(tableEvent['eventType_id'].eq(eventTypeId))
    if specialityId:
        cond.append(tablePerson['speciality_id'].eq(specialityId))

    if orgStructureId:
        cond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureDescendants(orgStructureId)))
    else:
        cond.append(tablePerson['org_id'].eq(QtGui.qApp.currentOrgId()))
    if sex:
        cond.append(tableClient['sex'].eq(sex))
    if ageFrom <= ageTo:
        cond.append('Event.setDate >= ADDDATE(Client.birthDate, INTERVAL %d YEAR)'%ageFrom)
        cond.append('Event.execDate < SUBDATE(ADDDATE(Client.birthDate, INTERVAL %d YEAR),1)'%(ageTo+1))

    data = selectData(db, cond, string, isDivideToRegions, address)
    return data

def selectData(db, condition, string, isDivideToRegions, address):
    stmt = """SELECT distinct(Event.id) as eventId,
                            Client.id as clientId,
                            EventType.regionalCode as eventRegionalCode,
                            EventType.finance_id as financeType,
                            Event.client_id AS clientId,
                            vrbPersonWithSpeciality.speciality_id as specialityId,
                            rbSpeciality.name as specialityName,
                        (SELECT SUM(A.amount)
                            FROM Action AS A
                            INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
                            WHERE A.event_id = Event.id
                            AND AT.flatCode LIKE 'moving%%' AND A.deleted = 0
                            GROUP BY A.event_id) as hospital,

                        (SELECT SUM(A.amount)
                            FROM Action AS A
                            INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
                            WHERE A.event_id = Event.id
                            AND AT.flatCode LIKE 'zub%%' AND A.deleted = 0
                            GROUP BY A.event_id) as stomat,

                        (SELECT SUM(A.uet)
                            FROM Action AS A
                            INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
                            WHERE A.event_id = Event.id
                            AND AT.flatCode LIKE 'zub%%' AND A.deleted = 0
                            GROUP BY A.event_id) as uet,

                        (SELECT SUM(A.amount)
                            FROM Action AS A
                            INNER JOIN ActionType AS AT ON AT.id = A.actionType_id
                            WHERE A.event_id = Event.id
                            AND AT.flatCode LIKE 'emergency%%' AND A.deleted = 0
                            GROUP BY A.event_id) as emergency,

                        (SELECT COUNT(*)
                             FROM Visit
                             LEFT JOIN rbVisitType ON rbVisitType.id = Visit.visitType_id
                             LEFT JOIN rbScene ON rbScene.id = Visit.scene_id
                             WHERE Visit.event_id = Event.id and (rbScene.code = 2 or rbScene.code = 3)
                            AND DATE(Event.setDate) <= DATE(Visit.date) AND Visit.deleted = 0)
                             AS visitHomeCount,

                        (SELECT COUNT(*)
                            FROM Visit
                            LEFT JOIN rbVisitType ON rbVisitType.id = Visit.visitType_id
                            LEFT JOIN rbScene ON rbScene.id = Visit.scene_id
                            WHERE Visit.event_id = Event.id
                            AND DATE(Event.setDate) <= DATE(Visit.date) AND Visit.deleted = 0)
                            AS visitCount,

                        (SELECT kladr.KLADR.CODE
                            FROM ClientAddress
                            INNER JOIN Address ON ClientAddress.address_id = Address.id
                            INNER JOIN AddressHouse ON Address.house_id = AddressHouse.id
                            INNER JOIN kladr.KLADR ON kladr.KLADR.CODE = AddressHouse.KLADRCode
                            WHERE Client.id IS NOT NULL AND ClientAddress.client_id = Client.id
                            AND Address.deleted = 0 AND AddressHouse.deleted = 0 AND ClientAddress.type = %s
                            AND DATE(ClientAddress.createDatetime) <= DATE(Event.setDate)
                             ORDER BY ClientAddress.id DESC
                            LIMIT 1)
                            AS kladrCode,

                        (SELECT kladr.KLADR.SOCR
                            FROM ClientAddress
                            INNER JOIN Address ON ClientAddress.address_id = Address.id
                            INNER JOIN AddressHouse ON Address.house_id = AddressHouse.id
                            INNER JOIN kladr.KLADR ON kladr.KLADR.CODE = AddressHouse.KLADRCode
                            WHERE Client.id IS NOT NULL AND ClientAddress.client_id = Client.id
                            AND Address.deleted = 0 AND AddressHouse.deleted = 0 AND ClientAddress.type = %s
                            AND DATE(ClientAddress.createDatetime) <= DATE(Event.setDate)
                             ORDER BY ClientAddress.id DESC
                             LIMIT 1
                            )
                            AS kladrSocrCode,
                            OrgStructure.type as OrgStructureType
                        FROM %s
                        INNER JOIN EventType              ON EventType.id = Event.eventType_id
                        INNER JOIN Client                 ON Client.id = Event.client_id
                        INNER JOIN vrbPersonWithSpeciality ON vrbPersonWithSpeciality.id = Event.execPerson_id
                        LEFT JOIN rbSpeciality ON rbSpeciality.id = vrbPersonWithSpeciality.speciality_id
                        LEFT JOIN OrgStructure ON OrgStructure.id = vrbPersonWithSpeciality.orgStructure_id
                        WHERE Event.deleted = 0 AND %s
                        GROUP BY Event.id
                        ORDER BY kladrCode, Event.id, Event.client_id""" #(db.joinAnd(condition))
    qqq = db.joinAnd(condition)
    query =  db.query(stmt%(address, address, string , str(qqq)))
    data = []
    while query.next():
        eventInfo = {}
        eventInfo["clientId"] = forceRef(query.record().value('clientId'))
        eventInfo["eventId"] = forceRef(query.record().value('eventId'))
        eventInfo["eventRegionalCode"] = forceInt(query.record().value('eventRegionalCode'))
        eventInfo["financeType"] = forceInt(query.record().value('financeType'))
        eventInfo["clientId"] = forceRef(query.record().value('clientId'))
        eventInfo["specialityId"] = forceRef(query.record().value('specialityId'))
        eventInfo["specialityName"] = forceString(query.record().value('specialityName'))
        eventInfo["hospital"] = forceInt(query.record().value('hospital'))
        eventInfo["uet"] = forceDouble(query.record().value('uet'))

        eventInfo["stomatAmount"] = forceInt(query.record().value('stomat'))
        eventInfo["emergency"] = forceInt(query.record().value('emergency'))
        eventInfo["visitHomeCount"] = forceInt(query.record().value('visitHomeCount'))
        eventInfo["visitCount"] = forceInt(query.record().value('visitCount'))
        eventInfo["OrgStructureType"] = forceInt(query.record().value('OrgStructureType'))

        if isDivideToRegions == True:
            eventInfo["kladrSocrCode"] = forceString(query.record().value('kladrSocrCode'))
            if forceString(query.record().value('kladrSocrCode')) != u'пгт' and forceString(query.record().value('kladrCode'))[:2] =='29':
                eventInfo["kladrCode"] = '%s00000'%(forceString(query.record().value('kladrCode'))[:8]) if forceString(query.record().value('kladrCode'))[:2] =='29' else '0000000000000'
            elif forceString(query.record().value('kladrCode'))[:2] !='29' and forceString(query.record().value('kladrCode'))[:2] !='83' and forceString(query.record().value('kladrCode'))[:2] != '':
                eventInfo["kladrCode"] = '0000000000000'
            elif forceString(query.record().value('kladrCode'))[:2] =='83':
                eventInfo["kladrCode"] = '8300000000000'
            elif forceString(query.record().value('kladrCode'))[:2] == '':
                eventInfo["kladrCode"] = '0000000000001'
            else:
                eventInfo["kladrCode"] = forceString(query.record().value('kladrCode'))
        else:
            if forceString(query.record().value('kladrCode')) =='2900000100000':
                eventInfo["kladrCode"] = forceString(query.record().value('kladrCode'))
            if forceString(query.record().value('kladrCode')) !='2900000100000' and forceString(query.record().value('kladrCode'))[:2] =='29':
                eventInfo["kladrCode"] = '2900000000000'
            if forceString(query.record().value('kladrCode'))[:2] =='83':
                eventInfo["kladrCode"] = '8300000000000'
            if forceString(query.record().value('kladrCode'))[:2] !='29' and forceString(query.record().value('kladrCode'))[:2] !='83' and forceString(query.record().value('kladrCode'))[:2] != '':
                eventInfo["kladrCode"] = '0000000000000'
            if forceString(query.record().value('kladrCode'))[:2] == '':
                eventInfo["kladrCode"] = '0000000000001'
        data.append(eventInfo)
    return data

def recievedDate(data, isSpecialityDetail, isDivideToRegions):
    massiv = []
    for dt in data:
            isMassive, element  = isInMassiv(massiv, "kladrCode", dt['kladrCode']) if isSpecialityDetail == False else isInMassiv(massiv, "kladrCode", dt['kladrCode'], "specialityId", dt['specialityId'])
            if isMassive == False:
                count= {'territory': '',
                        'speciality':'',
                        'stomatVisit':0,
                        'uet':0,
                        'stomatAmount':0,
                        'hospitalAmount':0,
                        'hospitalClients': [],
                        'hospitalEvents':[],
                        'dhospitalClients': [],
                        'dhospitalEvents':[],
                        'dhhospitalClients': [],
                        'dhhospitalEvents':[],
                        'dhospitalAmount':0,
                        'dhhospitalAmount':0,
                        'dHomeHospitalClients': [],
                        'dHomeHospitalEvents':[],
                        'dHomeHospitalAmount':0,
                        'emergencyClients': [],
                        'emergencyAmount':0,
                        'eventAmount':0,
                        'visitAmount':0,
                        'ambulancelClients':[]
                       }
                count['kladrCode'] = dt['kladrCode']
                if isDivideToRegions == True:
                    if dt['kladrCode'][:2] =='29':
                        count["territory"] = getAddress(dt['kladrCode'])
                    elif dt['kladrCode'][:2] =='83':
                         count["territory"] = u'НАО'
                    elif dt['kladrCode'] =='0000000000001':
                        count["territory"] = u'Без адреса'
                    else:
                         count["territory"] = u'Другие регионы'
                else:
                    if dt['kladrCode'] == '0000000000001':
                        count["territory"] = u'Без адреса'
                    if dt['kladrCode'][:2] =='29' and dt['kladrCode'] !='2900000100000':
                        count["territory"] = u'Архангельская область'
                    if dt['kladrCode'][:2] =='83':
                        count["territory"] = u'НАО'
                    if dt['kladrCode'][:2] !='29' and dt['kladrCode'][:2] !='83':
                        count["territory"] = u'Другие регионы'
                    if dt['kladrCode'] =='2900000100000':
                        count["territory"] = getAddress(dt['kladrCode'])
                count["specialityId"] = dt['specialityId']
                count["speciality"] = dt['specialityName']
                count = addToMassiveFromList(count, dt)
                massiv.append(count)
            else:
                massiv[element] = addToMassiveFromList(massiv[element], dt)
    return massiv

def addToMassiveFromList(massive, list):
    # стоматолгия
    if str(list["eventRegionalCode"])[:4] == '3019':
        massive["stomatAmount"] = massive["stomatAmount"] +list['stomatAmount']
        massive["uet"] = massive["uet"] +list['uet']
        massive["stomatVisit"] = massive["stomatVisit"] +list['visitCount']
    # амбулатория
    elif str(list["eventRegionalCode"])[:2] == '30':
        if str(list["eventRegionalCode"])[:3] == '301':
            massive["eventAmount"] = massive["eventAmount"] + 1
        massive["visitAmount"] = massive["visitAmount"] + list['visitCount']
        if list['clientId'] not in massive["ambulancelClients"]:
             massive["ambulancelClients"].append(list['clientId'])
    elif str(list["eventRegionalCode"])[:3] == '110':
        if list['clientId'] not in massive["hospitalClients"]:
            massive["hospitalClients"].append(list['clientId'])
        massive["hospitalEvents"].append(list["eventId"])
        massive["hospitalAmount"] = massive["hospitalAmount"] + list['hospital']
    elif str(list["eventRegionalCode"])[:3] == '250':
        if list["visitHomeCount"] >0:
            if list['clientId'] not in massive["dHomeHospitalClients"]:
                massive["dHomeHospitalClients"].append(list['clientId'])
            massive["dHomeHospitalEvents"].append(list["eventId"])
            massive["dHomeHospitalAmount"] = massive["dHomeHospitalAmount"] + list['visitHomeCount']
        if list["OrgStructureType"] == 0 and list['visitCount'] !=list['visitHomeCount']:
            if list['clientId'] not in massive["dhospitalClients"]:
                massive["dhospitalClients"].append(list['clientId'])
            massive["dhospitalEvents"].append(list["eventId"])
            massive["dhospitalAmount"] = massive["dhospitalAmount"] + list['visitCount'] - list['visitHomeCount']
        elif list["OrgStructureType"] == 1 and list['visitCount'] !=list['visitHomeCount']:
            if list['clientId'] not in massive["dhhospitalClients"]:
                massive["dhhospitalClients"].append(list['clientId'])
            massive["dhhospitalEvents"].append(list["eventId"])
            massive["dhhospitalAmount"] = massive["dhhospitalAmount"] + list['visitCount'] - list['visitHomeCount']
    if list["emergency"] >0:
        if list['clientId'] not in massive["emergencyClients"]:
                massive["emergencyClients"].append(list['clientId'])
        massive["emergencyAmount"] = massive["emergencyAmount"] + list['emergency']
    return massive

def isInMassiv(massiv, key, element, key2 = None, element2 = None):
    for s in massiv:
        if s[key] == element:
            if key2 and s[key2] == element2:
                return True, massiv.index(s)
            elif not key2:
                return True, massiv.index(s)
    return False, None

def getAddress(code):
        stmt = """SELECT  `NAME` as address
                    FROM  kladr.`KLADR`
                    WHERE  `CODE` =%s"""%(code)
        query =  QtGui.qApp.db.query(stmt)
        if query.next():
            return (forceString(query.record().value('address')))
        else:
            return None



class CReportMedicalAidSizeByRegion(CReport):
    def __init__(self, parent, type):
        CReport.__init__(self, parent)
        self.type = type
        self.setTitle(u'Форма')



    def getSetupDialog(self, parent):
        result = CReportMedicalAidSizeByRegionDialog(parent)
        result.setTitle(self.title())

        return result

    def build(self, params):

        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        eventTypeId = params.get('eventTypeId', None)
        orgStructureId = params.get('orgStructureId', None)
        personId = params.get('personId', None)
        sex = params.get('sex', 0)
        ageFrom = params.get('ageFrom', 0)
        ageTo = params.get('ageTo', 150)
        specialityId = params.get('specialityId', None)
        isSpecialityDetail = params.get('chkIsSpecialityDetail', None)
        stringBy = params.get('stringBy', None)
        address = params.get('address', None)
        isDivideToRegions =  params.get('chbIsDetail', None)
        typeFinanceId = params.get('financeId', None)

        boldChars = QtGui.QTextCharFormat()
        boldChars.setFontWeight(QtGui.QFont.Bold)
        normChars = QtGui.QTextCharFormat()
        normChars.setFontWeight(QtGui.QFont.Normal)

        data = calculateData(isDivideToRegions, stringBy, begDate, endDate, eventTypeId, orgStructureId, personId, sex, ageFrom, ageTo, specialityId, typeFinanceId, address)
        unsortedData = recievedDate(data, isSpecialityDetail, isDivideToRegions)

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        tableColumns = self.drawTable(isSpecialityDetail)
        table = createTable(cursor, tableColumns)
        self.mergeCells(table, isSpecialityDetail)
        i=4
        mf = i
     #   regionSummary = {'visitAmount':0, 'uet':0, 'stomatAmount':0, 'stomatVisit':0, 'hospitalAmount':0, 'hospitalClients':[]}
        summary = {
                    'stomatVisit':0,
                    'uet':0,
                    'stomatAmount':0,
                    'hospitalAmount':0,
                    'hospitalClients': [],
                    'hospitalEvents':[],
                    'dhospitalClients': [],
                    'dhospitalEvents':[],
                    'dhhospitalClients': [],
                    'dhhospitalEvents':[],
                    'dhospitalAmount':0,
                    'dhhospitalAmount':0,
                    'dHomeHospitalClients': [],
                    'dHomeHospitalEvents':[],
                    'dHomeHospitalAmount':0,
                    'emergencyClients': [],
                    'emergencyAmount':0,
                    'ambulancelClients':[],
                    "eventAmount":0,
                    "visitAmount":0
                  }
        shift = 1 if isSpecialityDetail == True else 0

        sortedData = self.processingMassive(unsortedData)
        for datum in sortedData.values():
            regionSummary = {
                              'stomatVisit':0,
                              'uet':0,
                              'stomatAmount':0,
                              'hospitalAmount':0,
                              'hospitalClients': [],
                              'hospitalEvents':[],
                              'dhospitalClients': [],
                              'dhospitalEvents':[],
                              'dhhospitalClients': [],
                              'dhhospitalEvents':[],
                              'dhospitalAmount':0,
                              'dhhospitalAmount':0,
                              'dHomeHospitalClients': [],
                              'dHomeHospitalEvents':[],
                              'dHomeHospitalAmount':0,
                              'emergencyClients': [],
                              'emergencyAmount':0,
                              'ambulancelClients':[],
                              "eventAmount":0,
                              "visitAmount":0

                             }
            table.addRow()
            table.setText(i, 0, datum[0]["territory"])
            if isSpecialityDetail:
                table.mergeCells(i, 1, 1, 19)
                i += 1
            for dt in datum:
                if isSpecialityDetail:
                    table.addRow()
                    table.setText(i ,shift, dt["speciality"])
                self.addData(table,i, shift, dt, normChars)
                regionSummary = self.addToSummary(dt, regionSummary)
                summary = self.addToSummary(dt, summary)
                i += 1
            if isSpecialityDetail:
                table.mergeCells(mf, 0, i-mf, 1)
                mf = i +1

            if isSpecialityDetail:
                table.addRow()
                table.setText(i, 1,  u"Итого по региону:", charFormat=boldChars)
                table.mergeCells(i, 0, 1, 1 +shift)
                self.addData(table, i, shift, regionSummary, boldChars)
                i += 1
        table.addRow()
        table.setText(i, 0,  u"Итого:", charFormat=boldChars)
        table.mergeCells(i, 0, 1, 1 +shift)
        self.addData(table, i, shift, summary, boldChars)
        return doc

    def processingMassive(self, massiv):
        data = []
        resultMassive = {}
        for el in massiv:
            if el["kladrCode"] in resultMassive.keys():
                data = []
                data = resultMassive[el["kladrCode"]]
                data.append(el)
                resultMassive[el["kladrCode"]] = data
            else:
                data = []
                data.append(el)
                resultMassive[el["kladrCode"]] = data
        return resultMassive


    def addData(self, table, i, shift, massiv, ch):
        # амбулатория
        table.setText(i , 1 + shift, len(massiv["ambulancelClients"]), charFormat=ch)
        table.setText(i , 2 + shift, massiv["eventAmount"], charFormat=ch)
        table.setText(i , 3 + shift, massiv["visitAmount"], charFormat=ch)
        # стоматология
        table.setText(i , 4 + shift, massiv["uet"], charFormat=ch)
        table.setText(i , 5 + shift, massiv["stomatAmount"], charFormat=ch)
        table.setText(i , 6 + shift, massiv["stomatVisit"], charFormat=ch)
        # стационар
        table.setText(i , 7 + shift, len(massiv["hospitalClients"]), charFormat=ch)
        table.setText(i , 8 + shift, len(massiv["hospitalEvents"]), charFormat=ch)
        table.setText(i , 9 + shift, massiv["hospitalAmount"], charFormat=ch)
        # дс
        # при поликлинике
        table.setText(i , 10 + shift, len(massiv["dhospitalClients"]), charFormat=ch)
        table.setText(i , 11 + shift, len(massiv["dhospitalEvents"]), charFormat=ch)
        table.setText(i , 12 + shift, massiv["dhospitalAmount"], charFormat=ch)
        # на дому
        table.setText(i , 13 + shift, len(massiv["dHomeHospitalClients"]), charFormat=ch)
        table.setText(i , 14 + shift, len(massiv["dHomeHospitalEvents"]), charFormat=ch)
        table.setText(i , 15 + shift, massiv["dHomeHospitalAmount"], charFormat=ch)
        # при стационвр
        table.setText(i , 16 + shift, len(massiv["dhhospitalClients"]), charFormat=ch)
        table.setText(i , 17 + shift, len(massiv["dhhospitalEvents"]), charFormat=ch)
        table.setText(i , 18 + shift, massiv["dhhospitalAmount"], charFormat=ch)
        # смп
        table.setText(i , 19 + shift, len(massiv["emergencyClients"]), charFormat=ch)
        table.setText(i , 20 + shift, massiv["emergencyAmount"], charFormat=ch)

    def addToSummary(self, massiv, summary = None):
        summary = {'eventAmount':0,'visitAmount':0, 'uet':0, 'stomatAmount':0, 'stomatVisit':0} if not summary else summary
        summary['ambulancelClients'] = (summary['ambulancelClients'] + massiv["ambulancelClients"])
        summary['eventAmount'] = (summary['eventAmount'] + massiv["eventAmount"])
        summary['visitAmount'] = (summary['visitAmount'] + massiv["visitAmount"])
        summary['uet'] = (summary['uet'] + massiv["uet"])
        summary['stomatAmount'] = (summary['stomatAmount'] + massiv["stomatAmount"])
        summary['stomatVisit'] = (summary['stomatVisit'] + massiv["stomatVisit"])

        summary['hospitalAmount'] = (summary['hospitalAmount'] + massiv["hospitalAmount"])
        summary['hospitalEvents'] = (summary['hospitalEvents'] + massiv["hospitalEvents"])
        summary['hospitalClients'] = (summary['hospitalClients'] + massiv["hospitalClients"])

        summary['dhospitalAmount'] = (summary['dhospitalAmount'] + massiv["dhospitalAmount"])
        summary['dhospitalEvents'] = (summary['dhospitalEvents'] + massiv["dhospitalEvents"])
        summary['dhospitalClients'] = (summary['dhospitalClients'] + massiv["dhospitalClients"])

        summary['dHomeHospitalClients'] = (summary['dHomeHospitalClients'] + massiv["dHomeHospitalClients"])
        summary['dHomeHospitalEvents'] = (summary['dHomeHospitalEvents'] + massiv["dHomeHospitalEvents"])
        summary['dHomeHospitalAmount'] = (summary['dHomeHospitalAmount'] + massiv["dHomeHospitalAmount"])

        summary['dhhospitalAmount'] = (summary['dhhospitalAmount'] + massiv["dhhospitalAmount"])
        summary['dhhospitalEvents'] = (summary['dhhospitalEvents'] + massiv["dhhospitalEvents"])
        summary['dhhospitalClients'] = (summary['dhhospitalClients'] + massiv["dhhospitalClients"])

        summary['emergencyAmount'] = (summary['emergencyAmount'] + massiv["emergencyAmount"])
        summary['emergencyClients'] = (summary['emergencyClients'] + massiv["emergencyClients"])
        return summary


    def mergeCells(self, table, isSpecialityDetail):
        shift = 0
        table.mergeCells(0, 0, 4, 1)
        if isSpecialityDetail == True:
            table.mergeCells(0, 1, 4, 1)
            shift = 1
        table.mergeCells(0, 1 + shift, 1, 20)
        table.mergeCells(1, 1 + shift, 2, 3)
        table.mergeCells(1, 4 + shift, 2, 3)
        table.mergeCells(1, 7 + shift, 2, 3)
        table.mergeCells(1, 10 + shift, 1, 9)
        table.mergeCells(2, 10 + shift, 1, 3)
        table.mergeCells(2, 13 + shift, 1, 3)
        table.mergeCells(2, 16 + shift, 1, 3)
        table.mergeCells(1, 19 + shift, 2, 2)


    def drawTable(self, isSpecialityDetail):
        tableColumns = [
                ( '10%', [u'Территория', u'', u'', u''], CReportBase.AlignCenter),
                ( '3%', [u'Объемы медицинской помощи', u'Амб.-поликл.помощь', u'',u'кол-во пациентов.'], CReportBase.AlignRight),
                ( '3%', [u'и', u'', u'',u'кол-во обращ.'], CReportBase.AlignRight),
                ( '3%', [u'и', u'', u'',u'кол-во посещ.'], CReportBase.AlignRight),
                ( '3%', [u'', u'Стоматологическая помощь', u'', u'кол-во УЕТ'], CReportBase.AlignLeft),
                ( '3%', [u'', u'', u'', u'кол-во услуг'], CReportBase.AlignLeft),
                ( '3%', [u'', u'', u'', u'кол-во посещ.'], CReportBase.AlignLeft),
                ( '3%', [u'', u'Круглосуточный стационар', u'', u'больные'], CReportBase.AlignLeft),
                ( '3%', [u'', u'', u'', u'случаи лечения'], CReportBase.AlignLeft),
                ( '3%', [u'', u'', u'', u'к/дни'], CReportBase.AlignLeft),
                ( '3%', [u'', u'Дневные стационары', u'в поликлинике', u'больные'], CReportBase.AlignLeft),
                ( '3%', [u'', u'', u'',u'случаи лечения'], CReportBase.AlignLeft),
                ( '3%', [u'', u'', u'',u'к/дни'], CReportBase.AlignLeft),
                ( '3%', [u'', u'', u'на дому',u'больные'], CReportBase.AlignLeft),
                ( '3%', [u'', u'', u'',u'случаи лечения'], CReportBase.AlignLeft),
                ( '3%', [u'', u'', u'',u'к/дни'], CReportBase.AlignLeft),
                ( '3%', [u'', u'', u'при стационаре',u'больные'], CReportBase.AlignLeft),
                ( '3%', [u'', u'', u'',u'случаи лечения'], CReportBase.AlignLeft),
                ( '3%', [u'', u'', u'',u'к/дни'], CReportBase.AlignLeft),
                ( '3%', [u'', u'СМП', u'',u'больные'], CReportBase.AlignLeft),
                ( '3%', [u'', u'', u'',u'вызов'], CReportBase.AlignLeft)
                ]
        if isSpecialityDetail == True:
            tableColumns.insert(1, ( '10%', [u'Специальность', u'',u'',u''], CReportBase.AlignRight))
        return tableColumns





from Ui_ReportMedicalAidSizeByRegion import Ui_ReportMedicalAidSizeByRegionDialog


class CReportMedicalAidSizeByRegionDialog(QtGui.QDialog, Ui_ReportMedicalAidSizeByRegionDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
      #  self.cmbEventPurpose.setTable('rbEventTypePurpose', True, filter='code != \'0\'')
        self.cmbEventType.setTable('EventType', True, filter=getWorkEventTypeFilter(isApplyActive=True))
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())


    def setTitle(self, title):
        self.setWindowTitle(title)

    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.cmbEventType.setValue(params.get('eventTypeId', None))
        self.cmbSpeciality.setTable('rbSpeciality', True)
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.cmbPerson.setValue(params.get('personId', None))
        self.cmbSex.setCurrentIndex(params.get('sex', 0))
        self.edtAgeFrom.setValue(params.get('ageFrom', 0))
        self.edtAgeTo.setValue(params.get('ageTo', 150))
        self.cmbFinance.setTable('rbFinance', True)
        self.cmbIsFineshedCase.addItems([u'по законченному случаю',u'по визитам',u'по мероприятиями'])
        self.cmbAddress.addItems([u'регистрации', u'проживания'])

    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['chkIsSpecialityDetail'] = self.chkIsSpecialityDetail.isChecked()
        result['chbIsDetail'] = self.chbIsDetail.isChecked()
        result['eventTypeId'] = self.cmbEventType.value()
        result['orgStructureId'] = self.cmbOrgStructure.value()
        result['personId'] = self.cmbPerson.value()
        result['sex'] = self.cmbSex.currentIndex()
        result['ageFrom'] = self.edtAgeFrom.value()
        result['ageTo'] = self.edtAgeTo.value()
        result['specialityId'] = self.cmbSpeciality.value()
        result['financeId'] = self.cmbFinance.value()
        result['stringBy'] = self.cmbIsFineshedCase.currentIndex()
        result['address'] = self.cmbAddress.currentIndex()
        return result

    @pyqtSignature('QDate')
    def on_edtBegDate_dateChanged(self, date):
        self.cmbPerson.setBegDate(date)

    @pyqtSignature('QDate')
    def on_edtEndDate_dateChanged(self, date):
        self.cmbPerson.setEndDate(date)

    @pyqtSignature('int')
    def on_cmbSpeciality_currentIndexChanged(self, index):
        specialityId = self.cmbSpeciality.value()
        self.cmbPerson.setSpecialityId(specialityId)

    @pyqtSignature('int')
    def on_cmbEventPurpose_currentIndexChanged(self, index):
        eventPurposeId = self.cmbEventPurpose.value()
        if eventPurposeId:
            filter = 'EventType.purpose_id =%d' % eventPurposeId
        else:
            filter = getWorkEventTypeFilter(isApplyActive=True)
        self.cmbEventType.setFilter(filter)

    @pyqtSignature('int')
    def on_cmbOrgStructure_currentIndexChanged(self, index):
        orgStructureId = self.cmbOrgStructure.value()
        self.cmbPerson.setOrgStructureId(orgStructureId)
