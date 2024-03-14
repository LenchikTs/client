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

from library.Utils      import forceInt, forceString, formatName, formatSex, formatSNILS, forceDateTime, formatDateTime
from Reports.ReportBase import CReportBase, createTable


def selectData(accountItemIdList, detailPerson):
    db = QtGui.qApp.db
    stmt="""
        SELECT DISTINCT
            Client.id,
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
            %s
            formatClientAddress(ClientAddress.id) AS address
        FROM
            Account_Item
            LEFT JOIN Event         ON  Event.id  = Account_Item.event_id
            LEFT JOIN Client        ON  Client.id = Event.client_id
            LEFT JOIN ClientPolicy  ON ClientPolicy.id = getClientPolicyId(Event.client_id, 1)
            LEFT JOIN Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
            LEFT JOIN ClientDocument ON ClientDocument.client_id = Client.id AND
                      ClientDocument.id = (SELECT MAX(CD.id)
                                         FROM   ClientDocument AS CD
                                         LEFT JOIN rbDocumentType AS rbDT ON rbDT.id = CD.documentType_id
                                         LEFT JOIN rbDocumentTypeGroup AS rbDTG ON rbDTG.id = rbDT.group_id
                                         WHERE  rbDTG.code = '1' AND CD.client_id = Client.id)
            LEFT JOIN rbDocumentType ON rbDocumentType.id = ClientDocument.documentType_id
            %s
            LEFT JOIN ClientAddress ON  ClientAddress.client_id = Client.id
                                    AND ClientAddress.id = (SELECT MAX(id) FROM ClientAddress AS CA WHERE CA.Type=0 and CA.client_id = Client.id)
            WHERE
                %s
            ORDER BY
                Client.lastName,
                Client.firstName,
                Client.patrName,
                Client.birthDate,
                Client.sex
    """ % ('''Person.lastName    AS personLastName,
              Person.firstName     AS personFirstName,
              Person.patrName      AS personPatrName,
              Event.createDatetime AS createDatetime,
              rbPayRefuseType.name AS refuseName,''' if detailPerson else '',

          '''LEFT JOIN rbPayRefuseType ON Account_Item.refuseType_id = rbPayRefuseType.id
             LEFT JOIN Person ON Event.createPerson_id = Person.id''' if detailPerson else '',

            db.table('Account_Item')['id'].inlist(accountItemIdList),
          )
    return db.query(stmt)


class CClientsListByRegistry(CReportBase):
    def __init__(self, parent):
        CReportBase.__init__(self, parent)
        self.setTitle(u'Список пациентов по реестру')


    def build(self, description, params):
        result = QtGui.QMessageBox.question(None,
                                            u'Параметры отчета',
                                            u'Детализировать по врачам?',
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        detailPerson = (result == QtGui.QMessageBox.Yes)
        accountItemIdList = params.get('accountItemIdList', None)
        query = selectData(accountItemIdList, detailPerson)

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertText(description)
        cursor.insertBlock()

        if detailPerson:
            tableColumns = [
                              ('2%',  [ u'№'             ], CReportBase.AlignRight ),
                              ('10%', [ u'СНИЛС'         ], CReportBase.AlignLeft ),
                              ('10%', [ u'ФИО'           ], CReportBase.AlignLeft ),
                              ('10%', [ u'Дата рождения' ], CReportBase.AlignLeft ),
                              ('3%',  [ u'Пол'           ], CReportBase.AlignCenter ),
                              ('15%', [ u'Полис'         ], CReportBase.AlignCenter ),
                              ('10%', [ u'Документ'      ], CReportBase.AlignCenter ),
                              ('10%', [ u'Адрес'         ], CReportBase.AlignLeft ),
                              ('10%', [ u'ФИО врача'     ], CReportBase.AlignLeft ),
                              ('10%', [ u'Дата обращения'], CReportBase.AlignLeft ),
                              ('10%', [ u'Причина отказа'], CReportBase.AlignLeft ),
                           ]
        else:
            tableColumns = [
                              ('5%',  [ u'№'             ], CReportBase.AlignRight ),
                              ('10%', [ u'СНИЛС'         ], CReportBase.AlignLeft ),
                              ('20%', [ u'ФИО'           ], CReportBase.AlignLeft ),
                              ('10%', [ u'Дата рождения' ], CReportBase.AlignLeft ),
                              ('5%',  [ u'Пол'           ], CReportBase.AlignCenter ),
                              ('15%', [ u'Полис'         ], CReportBase.AlignCenter ),
                              ('15%', [ u'Документ'      ], CReportBase.AlignCenter ),
                              ('20%', [ u'Адрес'         ], CReportBase.AlignLeft ),
                           ]
        table = createTable(cursor, tableColumns)
        n = 0
        while query.next():
            n += 1
            record = query.record()
            name = formatName(record.value('lastName'),
                              record.value('firstName'),
                              record.value('patrName'))
            birthDate  = forceString(record.value('birthDate'))
            sex        = formatSex(forceInt(record.value('sex')))
            SNILS      = formatSNILS(record.value('SNILS'))
            policy     = ' '.join([forceString(record.value('policySerial')), forceString(record.value('policyNumber')), forceString(record.value('policyInsurer'))])
            document   = ' '.join([forceString(record.value('documentSerial')), forceString(record.value('documentNumber'))])
            address    = forceString(record.value('address'))
            if detailPerson:
                personName = formatName(record.value('personLastName'),
                                        record.value('personFirstName'),
                                        record.value('personPatrName'))
                createDatetime = formatDateTime(forceDateTime(record.value('createDatetime')))
                refuseName     = forceString(record.value('refuseName'))
            i = table.addRow()
            table.setText(i, 0, n)
            table.setText(i, 1, SNILS)
            table.setText(i, 2, name)
            table.setText(i, 3, birthDate)
            table.setText(i, 4, sex)
            table.setText(i, 5, policy)
            table.setText(i, 6, document)
            table.setText(i, 7, address)
            if detailPerson:
                table.setText(i,  8, personName)
                table.setText(i,  9, createDatetime)
                table.setText(i, 10, refuseName)
        return doc
