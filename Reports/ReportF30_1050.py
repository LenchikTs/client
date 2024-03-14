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
from PyQt4.QtCore import *
from library.Utils import forceInt
from Reports.Report import CReport
from Reports.ReportBase import CReportBase, createTable
from Orgs.Utils         import getOrgStructureDescendants, getOrgStructures


class CReportF30_1050(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Численность обслуживаемого прикрепленного населения (ф.30 табл.1050)')
        
    def selectData(self,  edate,  areaId,  addressType):
    
        db = QtGui.qApp.db
            
        stmt = u"""SELECT 
  COUNT(CASE WHEN Client.birthDate + INTERVAL 18 year > '{date}' AND Client.sex = 1 THEN Client.id ELSE NULL end) AS m_not_18,
  COUNT(CASE WHEN Client.birthDate + INTERVAL 18 year <= '{date}' AND  Client.birthDate + INTERVAL 60 year > '{date}' AND Client.sex = 1 THEN Client.id ELSE NULL end) AS m_18_59,
  COUNT(CASE WHEN Client.birthDate + INTERVAL 60 year <= '{date}' AND Client.sex = 1 THEN Client.id ELSE NULL end) AS m_60,
  COUNT(CASE WHEN Client.birthDate + INTERVAL 18 year > '{date}' AND Client.sex = 2 THEN Client.id ELSE NULL end) AS f_not_18,
  COUNT(CASE WHEN Client.birthDate + INTERVAL 18 year <= '{date}' AND  Client.birthDate + INTERVAL 55 year > '{date}' AND Client.sex = 2 THEN Client.id ELSE NULL end) AS f_18_54,
  COUNT(CASE WHEN Client.birthDate + INTERVAL 55 year <= '{date}'  AND Client.sex = 2 THEN Client.id ELSE NULL end) AS f_55,
  COUNT(CASE WHEN Client.birthDate + INTERVAL 1 month > '{date}' THEN Client.id ELSE NULL end) AS ch_1m,
  COUNT(CASE WHEN Client.birthDate + INTERVAL 1 year > '{date}' THEN Client.id ELSE NULL end) AS ch_1,
  COUNT(CASE WHEN Client.birthDate + INTERVAL 5 year > '{date}' THEN Client.id ELSE NULL end) AS ch_0_4,
  COUNT(CASE WHEN Client.birthDate + INTERVAL 5 year <= '{date}' AND  Client.birthDate + INTERVAL 10 year > '{date}' THEN Client.id ELSE NULL end) AS ch_5_9,
  COUNT(CASE WHEN Client.birthDate + INTERVAL 10 year <= '{date}' AND  Client.birthDate + INTERVAL 14 year > '{date}' THEN Client.id ELSE NULL end) AS ch_10_14,
  COUNT(IF(Address.house_id IS NOT NULL AND isOkatoVillager(kladr.getOKATO(AddressHouse.KLADRCode, AddressHouse.KLADRStreetCode, AddressHouse.number)), Client.id, NULL)) AS village,
  COUNT(*) AS allClients
  FROM Client 
  LEFT JOIN ClientAddress ON ClientAddress.client_id = Client.id 
  AND ClientAddress.id = (SELECT MAX(CA.id) FROM ClientAddress AS CA WHERE CA.type=0 AND CA.client_id = Client.id  AND CA.deleted = 0)
  
  LEFT JOIN ClientAttach ca ON ca.id = (
      SELECT MAX(ClientAttach.id)
            FROM ClientAttach
            INNER JOIN rbAttachType ON rbAttachType.id = ClientAttach.attachType_id
            WHERE client_id = Client.id
              
              AND ClientAttach.deleted = 0 AND (ClientAttach.endDate is NULL OR ClientAttach.endDate>= '{date}')
              AND NOT rbAttachType.TEMPORARY)
  
  LEFT JOIN Address ON Address.id = ClientAddress.address_id
  LEFT JOIN AddressHouse ON AddressHouse.id = Address.house_id
  LEFT JOIN rbAttachType ON rbAttachType.id=ca.attachType_id
  WHERE Client.deleted = 0 AND ((Client.deathDate >= '{date}') OR (Client.deathDate IS NULL)) AND (((rbAttachType.`outcome`=0) OR (rbAttachType.`id` IS NULL))) AND ({cond})"""
  
        cond = []
        if areaId:
            areaIdList = getOrgStructureDescendants(areaId)
        else:
            areaIdList = getOrgStructures(QtGui.qApp.currentOrgId())
        reg = (addressType+1) & 1
        loc = (addressType+1) & 2
        attach = (addressType+1) & 4
        condAddr = []
        if reg:
            tableOrgStructureAddress = db.table('OrgStructure_Address')
            tableAddress = db.table('Address')
            subCond = [ tableOrgStructureAddress['master_id'].inlist(areaIdList),
                        tableOrgStructureAddress['house_id'].eq(tableAddress['house_id']),
                    ]
            condAddr.append(db.existsStmt(tableOrgStructureAddress, subCond))
        if loc:
            tableOrgStructureAddress = db.table('OrgStructure_Address')
            tableAddress = db.table('Address')
            subCond = [ tableOrgStructureAddress['master_id'].inlist(areaIdList),
                        tableOrgStructureAddress['house_id'].eq(tableAddress['house_id']),
                    ]
            condAddr.append(db.existsStmt(tableOrgStructureAddress, subCond))
        if attach:
            tableClientAttach = db.table('ClientAttach').alias('ca')
            condAddr.append(db.joinAnd([db.joinOr([tableClientAttach['orgStructure_id'].inlist(areaIdList),
                                                tableClientAttach['orgStructure_id'].isNull()
                                                ]),
                                        tableClientAttach['deleted'].eq(0)
                                        ]))
        if condAddr:
            cond.append(db.joinOr(condAddr))
        st = stmt.format(date=db.formatDate(edate)[1:11], cond = db.joinAnd(cond))
        return db.query(st)

    def getSetupDialog(self, parent):
        result = CAttachedContingentSetupDialog(parent)
        result.setTitle(self.title())
        return result

    def build(self, params):
        areaId = params.get('areaId', None)
        addressType = params.get('addressType', 0)
        eDate = params.get('endDate',  QDate())
        
        query = self.selectData(eDate,  areaId,  addressType)
        while query.next():
            
            record = query.record()
            male_not_18 = forceInt(record.value('m_not_18'))
            male_18_59 = forceInt(record.value('m_18_59'))
            male_60 = forceInt(record.value('m_60'))
            female_not_18 = forceInt(record.value('f_not_18'))
            female_18_54 = forceInt(record.value('f_18_54'))
            female_55 = forceInt(record.value('f_55'))
            child_1m = forceInt(record.value('ch_1m'))
            child_1 = forceInt(record.value('ch_1'))
            child_0_4 = forceInt(record.value('ch_0_4'))
            child_5_9 = forceInt(record.value('ch_5_9'))
            child_10_14 = forceInt(record.value('ch_10_14'))
            village = forceInt(record.value('village'))
            allClients = forceInt(record.value('allClients'))
            children = male_not_18 + female_not_18
            worker = male_18_59 + female_18_54
            old = male_60 + female_55
            
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()

        tableColumns = [
            ('50%', [u'Наименование'], CReportBase.AlignCenter),
            ('15%', [u'№ строки'], CReportBase.AlignCenter),
            ('35%', [u'Численность прикрепленного населения'], CReportBase.AlignCenter)
            
        ]
                
        table = createTable(cursor, tableColumns,  12)
        table.setText(1, 0, u'1')
        table.setText(1, 1, u'2')
        table.setText(1, 2, u'3')
        table.setText(2, 0, u'  Всего (чел)',  blockFormat = CReportBase.AlignLeft)
        table.setText(2, 1, u'1')
        table.setText(2, 2, allClients)
        table.setText(3, 0, u'  в том числе: детей 0-17 лет включительно',  blockFormat = CReportBase.AlignLeft)
        table.setText(3, 1, u'2')
        table.setText(3, 2, children)
        table.setText(4, 0, u'из них: до 1 года\t')
        table.setText(4, 1, u'3')
        table.setText(4, 2, child_1)
        table.setText(5, 0, u'\tиз них: до 1 мес.')
        table.setText(5, 1, u'3.1')
        table.setText(5, 2, child_1m)
        table.setText(6, 0, u'детей 0-4 лет')
        table.setText(6, 1, u'4')
        table.setText(6, 2, child_0_4)
        table.setText(7, 0, u'детей 5-9 лет')
        table.setText(7, 1, u'5')
        table.setText(7, 2, child_5_9)
        table.setText(8, 0, u'детей 10-14 лет')
        table.setText(8, 1, u'6')
        table.setText(8, 2, child_10_14)
        table.setText(9, 0, u'  население трудоспособного возраста',  blockFormat = CReportBase.AlignLeft)
        table.setText(9, 1, u'7')
        table.setText(9, 2, worker)
        table.setText(10, 0, u' население старше трудоспособного возраста',  blockFormat = CReportBase.AlignLeft)
        table.setText(10,  1, u'8')
        table.setText(10, 2, old)
        table.setText(11, 0, u' Сельское население',  blockFormat = CReportBase.AlignLeft)
        table.setText(11, 1, u'9')
        table.setText(11, 2, (village))
        
        return doc

from Ui_AttachedContingentSetup import Ui_AttachedContingentSetupDialog

class CAttachedContingentSetupDialog(QtGui.QDialog, Ui_AttachedContingentSetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.patientRequired = False
        self.setupUi(self)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())

    def setPayPeriodVisible(self, value):
        pass

    def setWorkTypeVisible(self, value):
        pass

    def setTitle(self, title):
        self.setWindowTitle(title)

    def setEventTypeVisible(self, visible=True):
        pass

    def setParams(self, params):
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.cmbOrgStructure.setValue(params.get('areaId', None))
        self.cmbAddressOrgStructureType.setCurrentIndex(params.get('addressType', 4))

    def params(self):
        result = {}
        result['endDate'] = self.edtEndDate.date()
        result['areaId'] = self.cmbOrgStructure.value()
        result['addressType'] = self.cmbAddressOrgStructureType.currentIndex()
        return result
