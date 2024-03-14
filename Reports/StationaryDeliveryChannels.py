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
from PyQt4.QtCore import QDate, QDateTime, QTime

from library.Utils      import forceInt, forceString

from Orgs.Utils         import getOrgStructureDescendants
from Reports.ReportBase import CReportBase, createTable
from Reports.Report     import CReport
from Reports.Ui_DateAndOrgStructureSetupDialog import Ui_DateAndOrgStructureSetupDialog


class CDeliveryChannelsReport(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Справка о каналах поступления выбывших больных в стационар')
        self.setOrientation(QtGui.QPrinter.Landscape)
        self.mapOrgStructureIdToName = {}

    def getSetupDialog(self, parent):
        result = CDateAndOrgStructureSetup(parent)
        result.setTitle(self.title())
        return result

    def selectData(self, begDate, endDate, orgStructureId):
        data = {}
        unCounted = []
        db = QtGui.qApp.db
        tableAction = db.table('Action')
        cond = [
            tableAction['endDate'].between(begDate, endDate if endDate else QDateTime.currentDateTime())
        ]
        orgStructureCond = 'is not NULL'
        if orgStructureId:
            orgIds = getOrgStructureDescendants(orgStructureId)
            orgStructureCond = ' in (%s)'% ','.join(map(str, orgIds))

        eventIdList = []
        stmt = u'''
            select IF(Event.prevEvent_id IS NOT NULL, getFirstEventId(Event.prevEvent_id), Event.id) as id
            from Event
            left join Action on Action.event_id = Event.id
            left join ActionType on ActionType.id = Action.actionType_id
            left join ActionProperty AS AP on AP.action_id = Action.id
            left join ActionPropertyType on ActionPropertyType.id = AP.type_id
            left join ActionProperty_OrgStructure as APOS on APOS.id = AP.id

            where %s
            and ActionType.flatCode = 'leaved' 
            and ActionType.deleted=0 
            and Action.deleted=0 
            and ActionPropertyType.deleted=0
            and AP.deleted=0
            and Event.deleted=0
            and ActionPropertyType.name = 'Отделение'
            and APOS.value %s
        ''' % (db.joinAnd(cond), orgStructureCond)

        query = db.query(stmt)
        while query.next():
            record = query.record()
            eventIdList.append(forceInt(record.value(0)))

        if eventIdList:
            stmt = u'''
                select
                ActionProperty_String.value as deliveredBy,
                Event.id as eventId,
                isClientVillager(Client.id) as 'isVillager',
                (
                    select OrgStructure.id from Action as Act
                        left join ActionType as AT on AT.id = Act.actionType_id
                        left join ActionProperty as AP on AP.action_id = Act.id
                        left join ActionPropertyType on ActionPropertyType.id = AP.type_id
                        left join ActionProperty_OrgStructure as APOS on APOS.id = AP.id
                        left join OrgStructure on OrgStructure.id = APOS.value
                    where
                        AT.flatCode = 'leaved'
                        and Act.deleted=0
                        and AT.deleted=0
                        and ActionPropertyType.deleted=0
                        and AP.deleted=0
                        and Act.event_id = getLastEventId(Event.id)
                        and ActionPropertyType.name = 'Отделение'

                ) as 'OrgStructureId',
                Event.`order` as 'EventOrder'

            from Action

                left join ActionType on ActionType.id = Action.actionType_id
                left join ActionProperty on ActionProperty.action_id = Action.id
                left join ActionPropertyType on ActionPropertyType.actionType_id = ActionType.id
                left join ActionProperty_String on ActionProperty_String.id = ActionProperty.id
                left join Event on Event.id = Action.event_id
                left join Client on Client.id = Event.client_id

            where ActionType.flatCode = 'received'
                and ActionPropertyType.typeName = 'String'
                and ActionPropertyType.name = 'Кем доставлен'
                and ActionProperty.type_id = ActionPropertyType.id
                and Action.deleted=0
                and ActionProperty.deleted=0
                and ActionPropertyType.deleted=0
                and Event.deleted=0
                and Client.deleted=0
                and Event.`order` IN (1, 2)
                and Event.id in (%s)

            ''' % (','.join(map(str, eventIdList)))

            query = db.query(stmt)
            while query.next():
                record = query.record()
                orgId = forceInt(record.value('OrgStructureId'))
                if not self.mapOrgStructureIdToName.get(orgId, ''):
                    self.mapOrgStructureIdToName[orgId] = forceString(db.translate('OrgStructure', 'id', orgId, 'name'))
                order = forceInt(record.value('EventOrder'))
                if int(order) == 2:
                    order = 1
                elif int(order) == 1:
                    order = 0
                # senderType = forceInt(record.value('senderType'))
                deliveredBy = forceString(record.value('deliveredBy')) # Переведи в нижний регистр и проверяй в нем
                deliveredBy = deliveredBy.lower()
                isVillager = forceInt(record.value('isVillager'))
                eventId = forceString(record.value('eventId'))
                stmt = """SELECT relegateOrg_id FROM Event WHERE id = %s""" % (eventId)
                query2 = db.query(stmt)
                while query2.next():
                    record2 = query2.record()
                    relegateOrg_id = forceString(record2.value('relegateOrg_id'))  # relegateOrg_id if not null

#                row = sqldata.setDefault((orgId, order), {'count': 0, 'isVillager':0, 'Pol':0, 'Stac':0, 'SMP':0, 'self':0, 'other':0})
                orderRow = data.setdefault(orgId, {0: [0]*7, 1: [0]*7})
                row = orderRow.setdefault(order, [])
                if isVillager:
                    row[1] += isVillager
                else:
                    row[0] += 1

                if deliveredBy in (u'смп', u'самостоятельно') and relegateOrg_id != u"0":
                    row[2] += 1
                elif deliveredBy in (u'перевод из другой мо') and relegateOrg_id != u"0":
                    row[3] += 1
                elif deliveredBy in (u'смп'):
                    row[4] += 1
                elif deliveredBy in (u'самостоятельно'):
                    row[5] += 1
                else:
                    row[6] += 1

            #Достаем тех, у кого не отмечено "Кем доставлен"
            stmt = u'''
                select
                isClientVillager(Client.id) as 'isVillager',
                Organisation.isMedical as senderType,
                Event.id as eventId,
                (
                    select OrgStructure.id from Action as Act
                        left join ActionType as AT on AT.id = Act.actionType_id
                        left join ActionProperty as AP on AP.action_id = Act.id
                        left join ActionPropertyType on ActionPropertyType.id = AP.type_id
                        left join ActionProperty_OrgStructure as APOS on APOS.id = AP.id
                        left join OrgStructure on OrgStructure.id = APOS.value
                    where
                        AT.flatCode = 'leaved'
                        and Act.deleted=0
                        and AT.deleted=0
                        and AP.deleted=0
                        and ActionPropertyType.deleted=0
                        and Act.event_id = getLastEventId(Event.id)
                        and ActionPropertyType.name = 'Отделение'

                ) as 'OrgStructureId',
                Event.`order` as 'EventOrder'

            from Action

                left join ActionType on ActionType.id = Action.actionType_id
                left join Event on Event.id = Action.event_id
                left join Organisation on Organisation.id = Event.relegateOrg_id
                left join Client on Client.id = Event.client_id

            where ActionType.flatCode = 'received'
                and ActionType.deleted=0
                and Action.deleted=0
                and Event.deleted=0
                and Client.deleted=0
                and Organisation.deleted=0
                and Event.`order` = (1 or 2)
                and Event.id in (%s)
                and not exists (
                    select * from ActionProperty
                        left join ActionPropertyType on ActionPropertyType.id = ActionProperty.type_id
                    where
                        ActionPropertyType.id = ActionProperty.type_id
                        and ActionProperty.action_id = Action.id
                        and ActionPropertyType.name = 'Кем доставлен')

            '''% (','.join(map(str, eventIdList)))
            query = db.query(stmt)
            while query.next():
                record = query.record()
                orgId = forceInt(record.value('OrgStructureId'))
                if not self.mapOrgStructureIdToName.get(orgId, ''):
                    self.mapOrgStructureIdToName[orgId] = forceString(db.translate('OrgStructure', 'id', orgId, 'name'))
                order = forceInt(record.value('EventOrder'))
                if int(order) == 2:
                    order = 1
                elif int(order) == 1:
                    order = 0
                senderType = forceInt(record.value('senderType'))
                isVillager = forceInt(record.value('isVillager'))
                #row = sqldata.setDefault((orgId, order), {'count': 0, 'isVillager':0, 'Pol':0, 'Stac':0, 'SMP':0, 'self':0, 'other':0})
                orderRow = data.setdefault(orgId, {0: [0]*7, 1: [0]*7})
                row = orderRow.setdefault(order, [])

                if isVillager:
                    row[1] += isVillager
                else:
                    row[0] += 1

                if deliveredBy in (u'смп', u'самостоятельно') and relegateOrg_id != u"0":
                    row[2] += 1
                elif deliveredBy in (u'перевод из другой мо') and relegateOrg_id != u"0":
                    row[3] += 1
                elif deliveredBy in (u'смп'):
                    row[4] += 1
                elif deliveredBy in (u'самостоятельно'):
                    row[5] += 1
                else:
                    row[6] += 1

        return data, unCounted

    def build(self, params):
        begDate   = QDateTime(params.get('begDate', QDate()), params.get('begTime', QTime()))
        endDate   = QDateTime(params.get('endDate', QDate()), params.get('endTime', QTime()))
        orgStructure = params.get('orgStructureId', None)

        tableColumns = [
            ('3%', [u'№', '',  '1'],       CReportBase.AlignRight),
            ('25%', [u'Подразделение',  '',  '2'],  CReportBase.AlignLeft),
            ('9%', [u'Порядок госпитализации', '',  '3'],     CReportBase.AlignLeft),
            ('6%', [u'Всего',  u'Всего',  '4'],      CReportBase.AlignRight),
            ('6%', ['', u'Городских', '5'], CReportBase.AlignRight),
            ('6%', ['', u'Сельских', '6'], CReportBase.AlignRight),
            ('9%', [u'Источники поступления', u'Поликлиники', '7'],  CReportBase.AlignRight),
            ('9%', ['', u'Стационары', '8'],  CReportBase.AlignRight),
            ('9%', ['', u'Скорая помощь', '9'],  CReportBase.AlignRight),
            ('9%', ['', u'Самостоятельно', '10'],  CReportBase.AlignRight),
            ('9%', ['', u'Прочие', '11'],  CReportBase.AlignRight),
            ]

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        table = createTable(cursor, tableColumns)

        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 2, 1)
        table.mergeCells(0, 3, 1, 3)
        table.mergeCells(0, 6, 1, 5)

        data, unCounted = self.selectData(begDate, endDate, orgStructure)
        orgNames = data.keys()
        orgNames.sort()
        allSumPlan = [0]*7
        allSumUrg = [0]*7
        orgNum = 1
        for orgStructureId in orgNames:
            orgStructureName = self.mapOrgStructureIdToName.get(orgStructureId, u'')
            #orgStructureName = forceString(QtGui.qApp.db.translate('OrgStructure', 'id', orgId, 'name'))
            orderRow = data[orgStructureId]
            sum = [0]*7
            for order in orderRow:
                i = table.addRow()
                table.setText(i, 2, u'Планово' if order == 0 else u'Экстренно')
                row = orderRow[order]
                for j, item in enumerate(row):
                    table.setText(i, j+4, item)
                    sum[j] += item
                    if order:
                        allSumUrg[j] += item
                    else:
                        allSumPlan[j] += item
                table.setText(i, 3, row[0]+row[1])
            i = table.addRow()
            table.setText(i, 2, u'Итого', CReportBase.TableTotal)
            for j, item in enumerate(sum):
                table.setText(i, j+4, item, CReportBase.TableTotal)
            table.setText(i, 3, sum[0]+sum[1], CReportBase.TableTotal)
            table.setText(i-2, 1, orgStructureName)
            table.setText(i-2, 0, orgNum)
            orgNum += 1
            table.mergeCells(i-2, 1, 3, 1)
            table.mergeCells(i-2, 0, 3, 1)

        sum = [0]*7
        i = table.addRow()
        table.setText(i, 2, u'Планово')
        for j, item in enumerate(allSumPlan):
            table.setText(i, j+4, item, CReportBase.TableTotal)
            sum[j] += item
        table.setText(i, 3, allSumPlan[0]+allSumPlan[1], CReportBase.TableTotal)
        i = table.addRow()
        table.setText(i, 2, u'Экстренно')
        for j, item in enumerate(allSumUrg):
            table.setText(i, j+4, item, CReportBase.TableTotal)
            sum[j] += item
        table.setText(i, 3, allSumUrg[0]+allSumUrg[1], CReportBase.TableTotal)
        i = table.addRow()
        table.setText(i, 2, u'Итого', CReportBase.TableTotal)
        for j, item in enumerate(sum):
            table.setText(i, j+4, item, CReportBase.TableTotal)
        table.setText(i, 3, sum[0]+sum[1], CReportBase.TableTotal)
        table.setText(i-2, 1, u'Итого по стационару', CReportBase.TableTotal)
        table.mergeCells(i-2, 1, 3, 1)
        table.mergeCells(i-2, 0, 3, 1)

        #lostActionsCount = allActionsCount - (sum[0]+sum[1])
        lostActionsCount = len(unCounted)
        if lostActionsCount:
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.insertBlock()
            cursor.insertBlock()
            cursor.insertText(u'Всего неучтенных событий: %i (указанные поля "Кем доставлен" и направитель не соответствуют правилам заполнения)'%lostActionsCount)
            cursor.insertBlock()
            cursor.insertText(u'Код карточки: %s'%', '.join(unCounted))

        return doc



class CDateAndOrgStructureSetup(QtGui.QDialog, Ui_DateAndOrgStructureSetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())

    def setTitle(self, title):
        self.setWindowTitle(title)

    def setParams(self, params):
        begDate = params.get('begDate', QDate.currentDate())
        endDate = params.get('endDate', QDate.currentDate())
        begTime = params.get('begTime', QTime.currentTime())
        endTime = params.get('endTime', QTime.currentTime())
        self.edtBegDate.setDate(begDate)
        self.edtEndDate.setDate(endDate)
        self.edtBegTime.setTime(begTime)
        self.edtEndTime.setTime(endTime)
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))

    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['begTime'] = self.edtBegTime.time()
        result['endTime'] = self.edtEndTime.time()
        result['orgStructureId'] = self.cmbOrgStructure.value()
        return result
