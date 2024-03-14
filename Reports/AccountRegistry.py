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
from PyQt4.QtCore import QLocale

from Reports.ReportBase import CReportBase, createTable
from Reports.ReportView import CPageFormat
from Reports.StationaryAccountSummary import getAccountItemsList

from library.Utils      import forceDate, forceDouble, forceInt, forceString, formatName, formatSex, formatSNILS



def selectData(accountItemIdList, orgInsurerId = None):
    db = QtGui.qApp.db
    tableAccountItem = db.table('Account_Item')
    accountingSystemId = QtGui.qApp.defaultAccountingSystemId()
    if accountingSystemId is None:
        accountingSystemId = 0
    stmt=u"""
        SELECT
            Client.id,
            ClientIdentification.identifier,
            Client.lastName,
            Client.firstName,
            Client.patrName,
            Client.birthDate,
            Client.sex,
            Client.SNILS,
            ClientPolicy.serial    AS policySerial,
            ClientPolicy.number    AS policyNumber,
            Insurer.infisCode      AS policyInsurer,

            ClientDocument.serial  AS documentSerial,
            ClientDocument.number  AS documentNumber,
            rbDocumentType.code    AS documentType,
            formatClientAddress(ClientAddress.id) AS address,
            Diagnosis.MKB AS MKB,
            IF(rbService.name IS NULL, EventType.name, rbService.name) AS service,
            IF(rbService.code IS NULL, '',             rbService.code) AS serviceCode,
            vrbPersonWithSpeciality.name AS person,
            Event.execDate         AS eventDate,
            Action.endDate         AS actionDate,
            Visit.date             AS visitDate,
            Account_Item.amount    AS amount,
            Account_Item.uet       AS uet,
            Account_Item.sum       AS sum,
            (SELECT      APOS.value    FROM ActionPropertyType AS APT      INNER JOIN ActionProperty AS AP        ON AP.type_id = APT.id      
          INNER JOIN ActionProperty_String AS APOS        ON APOS.id = AP.id      
          INNER JOIN Action        ON AP.action_id = Action.id    
          WHERE APT.actionType_id in (SELECT        id      FROM ActionType at      WHERE at.flatCode in ('ECO_Step')      AND at.deleted = 0)   
          AND Action.event_id = Event.id    AND APT.deleted = 0    AND APT.name = "Этап ЭКО" LIMIT 1) AS EKO
        FROM
            Account_Item
            LEFT JOIN Event         ON  Event.id  = Account_Item.event_id
            LEFT JOIN EventType     ON  EventType.id = Event.eventType_id
            LEFT JOIN Visit         ON  Visit.id  = Account_Item.visit_id
            LEFT JOIN Action        ON  Action.id  = Account_Item.action_id
            LEFT JOIN ActionType    ON  ActionType.id = Action.actionType_id
            LEFT JOIN Client        ON  Client.id = Event.client_id
            LEFT JOIN ClientPolicy  ON ClientPolicy.client_id = Client.id AND
                      ClientPolicy.id = (SELECT MAX(CP.id)
                                         FROM   ClientPolicy AS CP
                                         WHERE  CP.client_id = Client.id)
            LEFT JOIN Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
            LEFT JOIN ClientDocument ON ClientDocument.client_id = Client.id AND
                      ClientDocument.id = (SELECT MAX(CD.id)
                                         FROM   ClientDocument AS CD
                                         LEFT JOIN rbDocumentType AS rbDT ON rbDT.id = CD.documentType_id
                                         LEFT JOIN rbDocumentTypeGroup AS rbDTG ON rbDTG.id = rbDT.group_id
                                         WHERE  rbDTG.code = '1' AND CD.client_id = Client.id)
            LEFT JOIN rbDocumentType ON rbDocumentType.id = ClientDocument.documentType_id

            LEFT JOIN ClientAddress ON  ClientAddress.client_id = Client.id
                                    AND ClientAddress.id = (SELECT MAX(id) FROM ClientAddress AS CA WHERE CA.Type=0 and CA.client_id = Client.id)

            LEFT JOIN ClientIdentification ON ClientIdentification.client_id = Client.id
                                    AND ClientIdentification.accountingSystem_id = %d
                                    AND ClientIdentification.id = (SELECT MAX(CI.id)
                                         FROM ClientIdentification AS CI
                                         WHERE CI.client_id = Client.id
                                           AND CI.accountingSystem_id = %d)
            LEFT JOIN Diagnosis     ON Diagnosis.id = IF(Account_Item.visit_id IS NULL,
                                                         getEventDiagnosis(Account_Item.event_id),
                                                         getEventPersonDiagnosis(Account_Item.event_id, Visit.person_id))
            LEFT JOIN vrbPersonWithSpeciality ON vrbPersonWithSpeciality.id =
                IF(Account_Item.visit_id IS NULL,
                    IF(Account_Item.action_id IS NULL,
                        Event.execPerson_id,
                        Action.person_id),
                    Visit.person_id)
            LEFT JOIN rbService ON rbService.id =
                IF(Account_Item.service_id IS NOT NULL,
                   Account_Item.service_id,
                   IF(Account_Item.visit_id IS NOT NULL, Visit.service_id, EventType.service_id)
                  )
        WHERE
            %s """ % (accountingSystemId, accountingSystemId, tableAccountItem['id'].inlist(accountItemIdList))
    if orgInsurerId:
        tableOrganisation = db.table('Organisation').alias('Insurer')
        stmt += """ AND %s """ % (tableOrganisation['id'].eq(orgInsurerId))

    stmt += """ ORDER BY
            Client.lastName,
            Client.firstName,
            Client.patrName,
            Client.birthDate,
            Client.sex,
            Account_Item.id
    """
    query = db.query(stmt)
    return query


class CAccountRegistry(CReportBase):
    def __init__(self, parent):
        CReportBase.__init__(self, parent)
        self.setTitle(u'Реестр счёта')
        self.orientation = CPageFormat.Landscape


    def build(self, description, params):
        #accountId = params.get('accountId', None)
        accountIdList = params.get('selectedAccountIdList', None)
        accountItemIdList = params.get('accountItemIdList', None)
        orgInsurerId = params.get('orgInsurerId', None)

        if accountIdList:
            accountItemIdList = getAccountItemsList(accountIdList)


        if orgInsurerId:
            self.setTitle(u'Реестр счета на СМО')
            query = selectData(accountItemIdList, orgInsurerId)
        else:
            query = selectData(accountItemIdList)

        accountingSystemId = QtGui.qApp.defaultAccountingSystemId()
        accountingSystemName = QtGui.qApp.defaultAccountingSystemName() if accountingSystemId else u'код'
        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertText(description)
        cursor.insertBlock()
        lpuCode = forceString(QtGui.qApp.db.translate('Organisation', 'id', QtGui.qApp.currentOrgId(), 'infisCode'))

        if lpuCode == '07541':
            tableColumns = [
                ('2%', [u'№'], CReportBase.AlignRight),
                ('5%', [accountingSystemName], CReportBase.AlignLeft),
                ('8%', [u'СНИЛС'], CReportBase.AlignLeft),
                ('10%', [u'ФИО'], CReportBase.AlignLeft),
                ('5%', [u'Дата\nрождения'], CReportBase.AlignLeft),
                ('2%', [u'Пол'], CReportBase.AlignCenter),
                ('7%', [u'Полис'], CReportBase.AlignCenter),
                ('7%', [u'Документ'], CReportBase.AlignCenter),
                ('10%', [u'Адрес'], CReportBase.AlignLeft),
                ('3%', [u'Ди-\nаг-\nноз'], CReportBase.AlignLeft),
                ('5%', [u'Код\nпрофиля\n(услуги)'], CReportBase.AlignLeft),
                ('8%', [u'Профиль\n(услуга)'], CReportBase.AlignLeft),
                ('9%', [u'Врач'], CReportBase.AlignLeft),
                ('5%', [u'Выполнено'], CReportBase.AlignLeft),
                ('3%', [u'Кол-\nво'], CReportBase.AlignRight),
                ('3%', [u'УЕТ'], CReportBase.AlignRight),
                ('4%', [u'Тариф'], CReportBase.AlignRight),
                ('4%', [u'Сумма'], CReportBase.AlignRight),
                ('4%', [u'Этап ЭКО'], CReportBase.AlignRight),
            ]
        else:
            tableColumns = [
                              ('2%',  [ u'№'             ], CReportBase.AlignRight ),
                              ('5%',  [ accountingSystemName ], CReportBase.AlignLeft ),
                              ('8%',  [ u'СНИЛС'         ], CReportBase.AlignLeft ),
                              ('10%', [ u'ФИО'           ], CReportBase.AlignLeft ),
                              ('5%',  [ u'Дата\nрождения'], CReportBase.AlignLeft ),
                              ('2%',  [ u'Пол'           ], CReportBase.AlignCenter ),
                              ('7%',  [ u'Полис'         ], CReportBase.AlignCenter ),
                              ('7%',  [ u'Документ'      ], CReportBase.AlignCenter ),
                              ('10%', [ u'Адрес'         ], CReportBase.AlignLeft ),
                              ('3%',  [ u'Ди-\nаг-\nноз' ], CReportBase.AlignLeft ),
                              ('5%',  [ u'Код\nпрофиля\n(услуги)'], CReportBase.AlignLeft ),
                              ('8%',  [ u'Профиль\n(услуга)'], CReportBase.AlignLeft ),
                              ('9%',  [ u'Врач'          ], CReportBase.AlignLeft ),
                              ('5%',  [ u'Выполнено'     ], CReportBase.AlignLeft ),
                              ('3%',  [ u'Кол-\nво'      ], CReportBase.AlignRight ),
                              ('3%',  [ u'УЕТ'           ], CReportBase.AlignRight ),
                              ('4%',  [ u'Тариф'         ], CReportBase.AlignRight ),
                              ('4%',  [ u'Сумма'         ], CReportBase.AlignRight ),
                           ]
        table = createTable(cursor, tableColumns)
        totalAmount = 0
        totalUet    = 0.0
        totalSum    = 0.0
        n = 0
        locale = QLocale()
        while query.next():
            n += 1
            record = query.record()
            clientIdentifier = forceString(record.value('identifier'if accountingSystemId else 'id'))
            name = formatName(record.value('lastName'),
                              record.value('firstName'),
                              record.value('patrName'))
            birthDate = forceString(record.value('birthDate'))
            sex = formatSex(forceInt(record.value('sex')))
            SNILS   = formatSNILS(record.value('SNILS'))
            policy  = ' '.join([forceString(record.value('policySerial')), forceString(record.value('policyNumber')), forceString(record.value('policyInsurer'))])
            document= ' '.join([forceString(record.value('documentSerial')), forceString(record.value('documentNumber'))])
            address = forceString(record.value('address'))
            MKB = forceString(record.value('MKB'))
            service = forceString(record.value('service'))
            serviceCode = forceString(record.value('serviceCode'))
            person = forceString(record.value('person'))
            date = forceDate(record.value('actionDate'))
            if not date:
                date = forceDate(record.value('visitDate'))
            if not date:
                date = forceDate(record.value('eventDate'))
            amount = forceDouble(record.value('amount'))
            uet    = forceDouble(record.value('uet'))
            sum    = forceDouble(record.value('sum'))
            EKO    = forceString(record.value('EKO'))

            i = table.addRow()

            if lpuCode == '07541':
                table.setText(i, 0, n)
                table.setText(i, 1, clientIdentifier)
                table.setText(i, 2, SNILS)
                table.setText(i, 3, name)
                table.setText(i, 4, birthDate)
                table.setText(i, 5, sex)
                table.setText(i, 6, policy)
                table.setText(i, 7, document)
                table.setText(i, 8, address)
                table.setText(i, 9, MKB)
                table.setText(i,10, serviceCode)
                table.setText(i,11, service)
                table.setText(i,12, person)
                table.setText(i,13, forceString(date))
                table.setText(i,14, amount)
                table.setText(i,15, uet)
                table.setText(i,16, locale.toString(sum/amount if amount else sum, 'f', 2))
                table.setText(i,17, locale.toString(sum, 'f', 2))
                table.setText(i,18, EKO)
                totalAmount += amount
                totalUet += uet
                totalSum += sum
            else:
                table.setText(i, 0, n)
                table.setText(i, 1, clientIdentifier)
                table.setText(i, 2, SNILS)
                table.setText(i, 3, name)
                table.setText(i, 4, birthDate)
                table.setText(i, 5, sex)
                table.setText(i, 6, policy)
                table.setText(i, 7, document)
                table.setText(i, 8, address)
                table.setText(i, 9, MKB)
                table.setText(i, 10, serviceCode)
                table.setText(i, 11, service)
                table.setText(i, 12, person)
                table.setText(i, 13, forceString(date))
                table.setText(i, 14, amount)
                table.setText(i, 15, uet)
                table.setText(i, 16, locale.toString(sum / amount if amount else sum, 'f', 2))
                table.setText(i, 17, locale.toString(sum, 'f', 2))
                totalAmount += amount
                totalUet += uet
                totalSum += sum

        i = table.addRow()
        table.mergeCells(i, 0, 1, 14)
        table.setText(i,  0, u'Итого',    CReportBase.TableTotal, CReportBase.AlignLeft)
        table.setText(i, 14, totalAmount, CReportBase.TableTotal)
        table.setText(i, 15, totalUet,    CReportBase.TableTotal)
        table.setText(i, 17, locale.toString(totalSum, 'f', 2), CReportBase.TableTotal)

        return doc
