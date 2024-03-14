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
from PyQt4.QtCore import QDate, QDateTime

from library.Utils      import forceInt, forceString, formatSex, forceRef, agreeNumberAndWord
from Reports.ReportBase import CReportBase, createTable
from Reports.Report     import CReport
from Reports.Utils      import dateRangeAsStr

from Ui_ReportNumberResidentsAddressSetup import Ui_ReportNumberResidentsAddressSetup


def selectData(params):
    sex            = params.get('sex', 0)
    ageFrom        = params.get('ageFrom', 0)
    ageTo          = params.get('ageTo', 150)
    addressType    = params.get('addressType', 0)
    permanentAttach= params.get('permanentAttach', None)
    attachCategory = params.get('attachCategory', 0)
    attachTypeId   = params.get('attachTypeId', None)
    attachBegDate  = params.get('attachBegDate', None)
    attachEndDate  = params.get('attachEndDate', None)
    stmt=u"""
SELECT COUNT(DISTINCT Client.id) AS clientCount,
kladr.KLADR.SOCR,
kladr.KLADR.NAME AS settlement,
kladr.KLADR.parent AS settlementParent,
kladr.STREET.NAME AS street,
kladr.STREET.SOCR AS streetType,
AddressHouse.number AS numberHouse,
AddressHouse.corpus AS corpusHouse,
ClientAddress.address_id
FROM
    Client
    LEFT JOIN ClientAddress ON (ClientAddress.type = %d AND ClientAddress.id = IF(ClientAddress.type = 0, getClientRegAddressId(Client.id), getClientLocAddressId(Client.id))
    AND ClientAddress.deleted = 0)
    LEFT JOIN Address       ON (Address.id = ClientAddress.address_id AND Address.deleted = 0)
    LEFT JOIN AddressHouse  ON (AddressHouse.id = Address.house_id AND AddressHouse.deleted = 0)
    LEFT JOIN kladr.STREET  ON kladr.STREET.CODE = AddressHouse.KLADRStreetCode
    LEFT JOIN kladr.KLADR   ON kladr.KLADR.CODE = AddressHouse.KLADRCode
WHERE
    %s
GROUP BY settlementParent, settlement, kladr.KLADR.SOCR, street, streetType, numberHouse, corpusHouse, ClientAddress.address_id
ORDER BY settlementParent, settlement, kladr.KLADR.SOCR, street, numberHouse, corpusHouse
"""
    db = QtGui.qApp.db
    tableClient       = db.table('Client')
    tableClientAttach = db.table('ClientAttach')
    cond = [tableClient['deleted'].eq(0)]
    if sex:
        cond.append(tableClient['sex'].eq(sex))
    if ageFrom <= ageTo:
        cond.append('DATE(%s) >= ADDDATE(Client.birthDate, INTERVAL %d YEAR)'%(db.formatDate(attachBegDate), ageFrom))
        cond.append('DATE(%s) < SUBDATE(ADDDATE(Client.birthDate, INTERVAL %d YEAR),1)'%(db.formatDate(attachEndDate), ageTo+1))
    outerCond = ['ClientAttach.client_id = Client.id']
    innerCond = ['CA2.client_id = ClientAttach.client_id']
    if attachBegDate and attachEndDate:
        outerCond.append(db.joinOr([db.joinAnd(['DATE(ClientAttach.begDate) IS NULL',
                                                'DATE(ClientAttach.endDate) IS NULL'
                                                ]),

                                    db.joinAnd(['DATE(ClientAttach.begDate) IS NULL',
                                                'DATE(ClientAttach.endDate) >= DATE(%s)'%(db.formatDate(attachBegDate))
                                                ]),

                                    db.joinAnd(['DATE(ClientAttach.endDate) IS NULL',
                                                'DATE(ClientAttach.begDate) < DATE(%s)'%(db.formatDate(attachEndDate))
                                                ]),

                                    db.joinAnd(['DATE(ClientAttach.begDate) IS NOT NULL',
                                                'DATE(ClientAttach.begDate) < DATE(%s)'%(db.formatDate(attachEndDate)),
                                    db.joinAnd(['DATE(ClientAttach.endDate) IS NOT NULL',
                                                'DATE(ClientAttach.endDate) >= DATE(%s)'%(db.formatDate(attachBegDate))
                                                ])
                                                ])
                                    ])
                        )
    elif attachBegDate:
        outerCond.append(db.joinOr([db.joinAnd(['DATE(ClientAttach.begDate) IS NULL',
                                                'DATE(ClientAttach.endDate) IS NULL'
                                                ]),
                                    db.joinAnd(['DATE(ClientAttach.endDate) IS NOT NULL',
                                                'DATE(ClientAttach.endDate) >= DATE(%s)'%(db.formatDate(attachBegDate))
                                                ])
                                    ])
                        )
    elif attachEndDate:
        outerCond.append(db.joinOr([db.joinAnd(['DATE(ClientAttach.begDate) IS NULL',
                                                'DATE(ClientAttach.endDate) IS NULL'
                                                ]),
                                    db.joinAnd(['DATE(ClientAttach.begDate) IS NOT NULL',
                                                'DATE(ClientAttach.begDate) < DATE(%s)'%(db.formatDate(attachEndDate))
                                                ])
                                    ])
                        )
        outerCond.append('DATE(ClientAttach.begDate) >= DATE(%s)'%(db.formatDate(attachBegDate)))
        outerCond.append('DATE(ClientAttach.begDate) < DATE(%s)'%(db.formatDate(attachEndDate)))
    if permanentAttach:
        outerCond.append(tableClientAttach['LPU_id'].eq(permanentAttach))
        innerCond.append('CA2.LPU_id=%d' % permanentAttach)
    if attachTypeId:
        outerCond.append('attachType_id=%d' % attachTypeId)
        innerCond.append('CA2.attachType_id=%d' % attachTypeId)
    else:
        if attachCategory == 1:
            innerCond.append('rbAttachType2.temporary=0')
        elif attachCategory == 2:
            innerCond.append('rbAttachType2.temporary')
        elif attachCategory == 3:
            innerCond.append('rbAttachType2.outcome')
        elif attachCategory == 0:
            outerCond.append('rbAttachType.outcome=0')
            innerCond.append('rbAttachType2.temporary=0')
    attachStmt = '''EXISTS (SELECT ClientAttach.id
       FROM ClientAttach
       LEFT JOIN rbAttachType ON rbAttachType.id = ClientAttach.attachType_id
       WHERE ClientAttach.deleted=0
       AND %s
       AND ClientAttach.id = (SELECT MAX(CA2.id)
                   FROM ClientAttach AS CA2
                   LEFT JOIN rbAttachType AS rbAttachType2 ON rbAttachType2.id = CA2.attachType_id
                   WHERE CA2.deleted=0 AND %s))'''
    cond.append(attachStmt % (db.joinAnd(outerCond), db.joinAnd(innerCond)))
    return db.query(stmt % (addressType, db.joinAnd(cond)))


class CReportNumberResidentsAddress(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setPayPeriodVisible(False)
        self.setTitle(u'Население по адресам')


    def getSetupDialog(self, parent):
        result = CReportNumberResidentsAddressSetup(parent)
        result.setTitle(self.title())
        return result


    def getDescription(self, params):
        db = QtGui.qApp.db
        sex            = params.get('sex', 0)
        ageFrom        = params.get('ageFrom', 0)
        ageTo          = params.get('ageTo', 150)
        addressType    = params.get('addressType', 0)
        permanentAttach= params.get('permanentAttach', None)
        attachCategory = params.get('attachCategory', 0)
        attachTypeId   = params.get('attachTypeId', None)
        attachBegDate  = params.get('attachBegDate', None)
        attachEndDate  = params.get('attachEndDate', None)
        rows = []
        if sex:
            rows.append(u'пол: ' + formatSex(sex))
        if ageFrom is not None and ageTo is not None and ageFrom <= ageTo:
            rows.append(u'возраст: c %d по %d %s' % (ageFrom, ageTo, agreeNumberAndWord(ageTo, (u'год', u'года', u'лет'))))
        if addressType is not None:
            rows.append(u'адрес ' + [u'регистрации', u'проживания'][addressType])
        if permanentAttach:
            rows.append(u'ЛПУ прикрепления: ' + forceString(db.translate('Organisation', 'id', permanentAttach, 'shortName')))
        if attachCategory:
            rows.append(u'прикрепление ' + [u'не задано', u'-', u'Постоянное', u'Временное', u'Выбыл'][attachCategory])
        if attachBegDate or attachEndDate:
            rows.append(dateRangeAsStr(u'прикрепление за период', attachBegDate, attachEndDate))
        if attachTypeId:
            rows.append(u'тип прикрепления: ' + forceString(db.translate('rbAttachType', 'id', attachTypeId, 'name')))
        rows.append(u'отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        return rows


    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        tableColumns = [
                        ('25%', [u'Населённый пункт'],  CReportBase.AlignLeft),
                        ('25%', [u'Улица'],             CReportBase.AlignLeft),
                        ('20%', [u'Тип улицы'],         CReportBase.AlignCenter),
                        ('10%', [u'Номер дома'],        CReportBase.AlignLeft),
                        ('10%', [u'Корпус'],            CReportBase.AlignLeft),
                        ('10%', [u'Количество людей' ], CReportBase.AlignRight)
                        ]
        reportData = {}
        reportDataTotal = 0
        clientCountNoAddress = 0
        table = createTable(cursor, tableColumns)
        db = QtGui.qApp.db
        tableKladr = db.table('kladr.KLADR')
        query = selectData(params)
        while query.next():
            record = query.record()
            clientCount      = forceInt(record.value('clientCount'))
            addressId        = forceRef(record.value('address_id'))
            street           = forceString(record.value('street'))
            streetType       = forceString(record.value('streetType'))
            numberHouse      = forceString(record.value('numberHouse'))
            corpusHouse      = forceString(record.value('corpusHouse'))
            SOCR             = forceString(record.value('SOCR'))
            settlement       = forceString(record.value('settlement')) + ((u' ' + SOCR) if SOCR else u'')
            settlementParent = forceString(record.value('settlementParent'))
            while settlementParent:
                record = db.getRecordEx(tableKladr, [tableKladr['parent'], tableKladr['NAME'], tableKladr['SOCR']], [u'''RPAD('%s', LENGTH(kladr.KLADR.CODE), '0') = kladr.KLADR.CODE'''%(settlementParent)])
                if record:
                    SOCR = forceString(record.value('SOCR'))
                    NAME = forceString(record.value('NAME'))
                    if NAME:
                        settlement = NAME + u' ' + SOCR + u', ' + settlement
                    settlementParent = forceString(record.value('parent'))
                else:
                    settlementParent = ''
            if not addressId:
                clientCountNoAddress += clientCount
            else:
                reportLine = reportData.get((settlement, street, streetType, numberHouse, corpusHouse), 0)
                reportLine += clientCount
                reportData[(settlement, street, streetType, numberHouse, corpusHouse)] = reportLine
            reportDataTotal += clientCount
        boldChars = QtGui.QTextCharFormat()
        boldChars.setFontWeight(QtGui.QFont.Bold)
        if reportDataTotal:
            i = table.addRow()
            table.setText(i, 0, u'Итого', charFormat=boldChars)
            table.setText(i, 5, reportDataTotal, charFormat=boldChars)
            table.mergeCells(i, 0, 1, 5)
        reportKeys = reportData.keys()
        reportKeys.sort(key=lambda item: (item[0], item[1]))
        for reportLine in reportKeys:
            clientCount = reportData.get(reportLine, 0)
            i = table.addRow()
            table.setText(i, 0, reportLine[0])
            table.setText(i, 1, reportLine[1])
            table.setText(i, 2, reportLine[2])
            table.setText(i, 3, reportLine[3])
            table.setText(i, 4, reportLine[4])
            table.setText(i, 5, clientCount)
        if clientCountNoAddress:
            i = table.addRow()
            table.setText(i, 0, u'Без адреса', charFormat=boldChars)
            table.setText(i, 5, clientCountNoAddress, charFormat=boldChars)
            table.mergeCells(i, 0, 1, 5)
        return doc


class CReportNumberResidentsAddressSetup(QtGui.QDialog, Ui_ReportNumberResidentsAddressSetup):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.edtAttachEndDate.canBeEmpty()
        self.cmbAttachType.setTable('rbAttachType', True)


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        currentDate = QDate.currentDate()
        self.cmbSex.setCurrentIndex(params.get('sex', 0))
        self.edtAgeFrom.setValue(params.get('ageFrom', 0))
        self.edtAgeTo.setValue(params.get('ageTo', 150))
        self.cmbAddressType.setCurrentIndex(params.get('addressType', 0))
        self.cmbArea.setValue(params.get('permanentAttach', None))
        self.cmbAttachCategory.setCurrentIndex(params.get('attachCategory', 0))
        self.cmbAttachType.setValue(params.get('attachTypeId', None))
        self.edtAttachBegDate.setDate(params.get('attachBegDate', currentDate))
        self.edtAttachEndDate.setDate(params.get('attachEndDate', currentDate))


    def params(self):
        result = {}
        result['sex']            = self.cmbSex.currentIndex()
        result['ageFrom']        = self.edtAgeFrom.value()
        result['ageTo']          = self.edtAgeTo.value()
        result['addressType']    = self.cmbAddressType.currentIndex()
        result['permanentAttach']= self.cmbArea.value()
        result['attachCategory'] = self.cmbAttachCategory.currentIndex()
        result['attachTypeId']   = self.cmbAttachType.value()
        result['attachBegDate']  = self.edtAttachBegDate.date()
        result['attachEndDate']  = self.edtAttachEndDate.date()
        return result

