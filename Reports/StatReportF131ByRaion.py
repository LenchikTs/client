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

from library.Utils      import forceInt, forceRef, forceString, getInfisCodes

from library.database   import addDateInRange

from Orgs.Utils         import getOrgStructureDescendants

from Registry.Utils     import formatAddress, getAddress, getClientAddress, getClientInfo
from Reports.Report     import CReport, CReportSetupDialog
from Reports.ReportBase import CReportBase, createTable
from Reports.StatReport1NPUtil import havePermanentAttach


# WFT? почему это не члены класса?
groupTitles = []
reg_num=0
reg_ind={}


def selectData(params):
    begDate             = params.get('begDate', QDate())
    endDate             = params.get('endDate', QDate())
    eventTypeId         = params.get('eventTypeId', None)
    onlyPermanentAttach = params.get('onlyPermanentAttach', False)
    onlyPayedEvents     = params.get('onlyPayedEvents', False)
    begPayDate          = params.get('begPayDate', QDate())
    endPayDate          = params.get('endPayDate', QDate())
    orgStructureId      = params.get('orgStructureId', None)
    isOrderAddress      = params.get('isOrderAddress', False)
    stmt="""
        SELECT distinct
            lpu_OKATO.NAME as lpu_region, Event.client_id as clientId,
            lpu.infisCode,
            getClientRegAddress(Client.id) AS address,
            ClientAttach.LPU_id
        FROM Event
        JOIN Client            ON Client.id = Event.client_id
        LEFT JOIN ClientAttach ON ClientAttach.id=(
            select max(ca.id)
            from ClientAttach as ca join rbAttachType on ca.attachType_id=rbAttachType.id
            where ca.client_id=Event.client_id and rbAttachType.temporary=0 and rbAttachType.outcome=0)
        LEFT JOIN Organisation as lpu on lpu.id = ClientAttach.LPU_id
        LEFT JOIN kladr.OKATO as lpu_OKATO on lpu_OKATO.CODE=left(lpu.OKATO, 5)
        LEFT JOIN Account_Item ON (
            Account_Item.event_id = Event.id AND
            Account_Item.id = (
                SELECT max(AI.id)
                FROM Account_Item AS AI
                WHERE AI.event_id = Event.id AND AI.deleted=0 AND AI.date IS NOT NULL AND AI.refuseType_id IS NULL AND AI.reexposeItem_id IS NULL AND AI.visit_id IS NULL AND AI.action_id IS NULL))
        LEFT JOIN Person ON (Person.id = Event.execPerson_id AND Person.deleted = 0)
        WHERE
            Event.deleted = 0 AND %s
        ORDER BY
            %s
    """
    db = QtGui.qApp.db
    tableEvent = db.table('Event')
    tablePerson = db.table('Person')
    setDate  = tableEvent['setDate']
    execDate = tableEvent['execDate']
    cond = []
    dateCond = []
    #dateCond.append(db.joinAnd([setDate.le(endDate), execDate.isNull()]))
    dateCond.append(db.joinAnd([execDate.ge(begDate), execDate.le(endDate)]))
    dateCond.append(db.joinAnd([setDate.ge(begDate), execDate.le(endDate)]))
    cond.append(db.joinOr(dateCond))
    if eventTypeId:
        cond.append(tableEvent['eventType_id'].eq(eventTypeId))
    if orgStructureId:
        orgStructureIdList = getOrgStructureDescendants(orgStructureId)
        cond.append(tablePerson['orgStructure_id'].inlist(orgStructureIdList))
    if onlyPermanentAttach:
        cond.append(havePermanentAttach(endDate))
    if onlyPayedEvents:
        cond.append('isEventPayed(Event.id)')
        tableAccountItem = db.table('Account_Item')
        addDateInRange(cond, tableAccountItem['date'], begPayDate, endPayDate)
    if isOrderAddress:
        order = u'address'
    else:
        order = u'Client.lastName, Client.firstName, Client.patrName'
    my_org_id=forceInt(QtGui.qApp.preferences.appPrefs.get('orgId', None))
    cond.append(tableEvent['org_id'].eq(my_org_id))
    stmt=stmt % (db.joinAnd(cond), order)
    return db.query(stmt)


class CStatReportF131ByRaion(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setPayPeriodVisible(True)
        self.setTitle(u'Сводка по Ф.131 по районам', u'Сводка по Ф.131')


    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setPayPeriodVisible(True)
        result.setWorkTypeVisible(False)
        result.setOwnershipVisible(False)
        result.setOrgStructureVisible(True)
        result.setChkOrderAddressVisible(True)
        result.setTitle(self.title())
        result.resize(0,0)
        return result


    def build(self, params):
        global groupTitles
        global reg_num
        global reg_ind
        groupTitles = []
        reg_num=0
        reg_ind={}

        reportRowSize = 4
        reportDataByGroups = []
        reportData = []
        query = selectData(params)
        while query.next():
            record = query.record()
            region=''
            lpuInfisCode=forceString(record.value('infisCode'))
            if forceRef(record.value('LPU_id')):
                if lpuInfisCode.strip():
                    region = forceString(record.value('lpu_region')).strip()
                else:
                    lpuInfisCode=u'нет прикрепления'
            else: lpuInfisCode=u'нет прикрепления'
            clientId=forceRef(record.value('clientId'))
            clientInfo=getClientInfo(clientId)
            fio=clientInfo['lastName']+' '+clientInfo['firstName']+' '+clientInfo['patrName']
            if not region:
                region = getRegion(clientId)
            bd=forceString(clientInfo['birthDate'])
            adr = forceString(record.value('address'))
            ind=reg_ind.get(region, -1)
            if ind==-1:
                groupTitles.append(region)
                reg_ind[region]=reg_num
                ind=reg_num
                reg_num+=1
                reportDataByGroups.append([])
            reportData = reportDataByGroups[ind]
            reportData.append([lpuInfisCode, fio, bd, adr])

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(u'Сводка по Ф.131 по районам')
        cursor.insertBlock()
        self.dumpParams(cursor, params)

        tableColumns = [
              ('10%', [ u'Код ЛПУ' ], CReportBase.AlignLeft ),
              ('30%', [ u'ФИО' ], CReportBase.AlignLeft ),
              ('10%', [ u'Дата рождения' ], CReportBase.AlignLeft ),
              ('50%', [ u'Адрес' ], CReportBase.AlignLeft ),
                       ]

        table = createTable(cursor, tableColumns)

        rd=[]
        for i in range(len(groupTitles)):
            rd.append((groupTitles[i], reportDataByGroups[i]))
        rd.sort(key=(lambda x:x[0]))
        if rd and not rd[0][0]:
            rd=rd[1:]+[rd[0]]

        totalByReport = 0
        for Title, reportData in rd:
            if reportData:
                totalByGroup = len(reportData)
                totalByReport += totalByGroup
                self.addGroupHeader(table, Title)
                for i, reportLine in enumerate(reportData):
                    i = table.addRow()
                    for j in xrange(reportRowSize):
                        table.setText(i, j, reportLine[j])
                self.addTotal(table, u'всего по району', totalByGroup)
        self.addTotal(table, u'Всего', totalByReport)
        return doc


    def addGroupHeader(self, table, group):
        i = table.addRow()
        table.mergeCells(i, 0, 1, 4)
        if not group: group=u'прочие районы'
        table.setText(i, 0, group, CReportBase.TableHeader)


    def addTotal(self, table, title, reportLen):
        i = table.addRow()
        table.mergeCells(i, 1, 1, 3)
        table.setText(i, 0, title, CReportBase.TableTotal)
        table.setText(i, 1, reportLen)


def getRegion(clientId):
#    if clientId == 2930:
#        pass
    clientAddressRecord = getClientAddress(clientId, 0)
    if clientAddressRecord:
        address = getAddress(clientAddressRecord.value('address_id'))
#        if not addressInfo:
#            pass
        area, region, npunkt, street, streettype = getInfisCodes(
            address.KLADRCode, address.KLADRStreetCode,
            address.number, address.corpus)
#        if not area:
#            pass
        region = forceString(QtGui.qApp.db.translate('kladr.OKATO', 'infis', area, 'NAME'))
        if area == u'ЛО':
            region = u'Ленинградская обл.'
#        if not region:
#            pass
        return region
    else:
        return ''


def getClientAddressAsString(clientId):
    regAddressRecord = getClientAddress(clientId, 0)
    if regAddressRecord:
        return formatAddress(regAddressRecord.value('address_id'))
    return ''
