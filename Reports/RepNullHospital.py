# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2015 SAMSON Group. All rights reserved.
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
from Reports.Report import CReport
from Reports.Utils import dateRangeAsStr
from Reports.ReportBase import CReportBase, createTable
from ReportSetupDialog import CReportSetupDialog
from Orgs.Utils import getOrgStructurePersonIdList, getOrgStructureFullName
from library.Utils import forceString, forceDate, forceInt
from PyQt4.QtCore import *
    
class CNullHospital(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Список аннулированых направлений')

    def getSetupDialog(self, parent):
        result = CFinReestrSetupDialog(parent)
        result.setTitle(self.title())
        for i in xrange(result.gridLayout.count()):
            spacer=result.gridLayout.itemAt(i)
            if isinstance(spacer, QtGui.QSpacerItem):
                itemposition=result.gridLayout.getItemPosition(i)
                if itemposition!=(29, 0, 1, 1)and itemposition!=(8, 1, 1, 3):
                    result.gridLayout.removeItem(spacer)
        result.resize(400, 10)
        return result


    def selectData(self, params): 
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        db = QtGui.qApp.db
        stmt = u'''SELECT c.lastName,c.firstName,c.patrName,c.birthDate,fin.value,doza.value as note,o.infisCode,CASE WHEN a.status = 0 
                  THEN 'Начато'
                WHEN a.status = 1 
                  THEN 'Ожидание'
                WHEN a.status = 2 
                  THEN 'Закончено'
                WHEN a.status = 3 
                  THEN 'Отменено'
                WHEN a.status = 4 
                  THEN 'Без результата'
                WHEN a.status = 5 
                  THEN 'Назначено'
                WHEN a.status = 6 
                  THEN 'Отказ'
                END AS status, doza5.value as ist 
    FROM Action a
LEFT JOIN ActionType at ON a.actionType_id = at.id
LEFT JOIN Event e ON a.event_id = e.id
LEFT JOIN EventType et ON e.eventType_id = et.id
LEFT JOIN Client c ON e.client_id = c.id
left join ActionPropertyType apt2 on apt2.actionType_id = at.id and apt2.name = 'Дата аннулирования' and apt2.deleted = 0
left join ActionProperty ap_fin on ap_fin.action_id = a.id and ap_fin.type_id = apt2.id
left join ActionProperty_Date fin on fin.id = ap_fin.id
LEFT JOIN Organisation o ON a.org_id = o.id
left join ActionPropertyType apt4 on apt4.actionType_id = at.id and apt4.name = 'Причина аннулирования' and apt4.deleted = 0
left join ActionProperty ap_doza on ap_doza.action_id = a.id and ap_doza.type_id = apt4.id
left join ActionProperty_String doza on doza.id = ap_doza.id
left join ActionPropertyType apt5 on apt5.actionType_id = at.id and apt5.name = 'Источник аннулирования' and apt5.deleted = 0
left join ActionProperty ap_doza5 on ap_doza5.action_id = a.id and ap_doza5.type_id = apt5.id
left join ActionProperty_String doza5 on doza5.id = ap_doza5.id
WHERE fin.value
AND a.begDate BETWEEN %(begDate)s AND %(endDate)s
and (at.flatCode in ("hospitalDirection", "received","planning") or at.flatCode = "leaved" and e.execDate is not NULL) 
AND a.deleted=0 AND ap_doza.deleted=0 AND ap_fin.deleted=0 AND apt2.deleted=0   and apt4.deleted=0 and at.deleted=0 and c.deleted =0 and e.deleted=0  AND et.deleted=0 
        '''% dict(begDate=db.formatDate(begDate),
                    endDate=db.formatDate(endDate))
        db = QtGui.qApp.db
        return db.query(stmt) 
        
    def getDescription(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())

        rows = []
        rows.append(dateRangeAsStr(u'за период', begDate, endDate))
        rows.append(u'отчёт составлен: ' + forceString(QDateTime.currentDateTime()))
        return rows


    def build(self, params):
        reportRowSize = 7
        reportData = {}
        chkDetailPerson   = params.get('detailPerson', False)
        secondTitle = u'Список аннулированых направлений'

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()

        tableColumns = [
            ('20%',  [ u'ФИО'], CReportBase.AlignLeft),
            ('10%',  [ u'Дата рождения'], CReportBase.AlignCenter),
            ('15%',  [ u'Дата аннулирования'], CReportBase.AlignCenter),
            ('20%',  [ u'Причина аннулирования'], CReportBase.AlignLeft),
            ('20%',  [ u'Источник аннулирования'], CReportBase.AlignLeft),
            ('15%',  [ u'Статус действия'], CReportBase.AlignLeft),
            ]

        table = createTable(cursor, tableColumns)
        query = self.selectData(params)
        while query.next():
            record = query.record()
            lastName = forceString(record.value('lastName'))
            firstName = forceString(record.value('firstName'))
            patrName = forceString(record.value('patrName'))
            birthDate = forceString(record.value('birthDate'))
            value = forceString(record.value('value'))
            note = forceString(record.value('note'))
            ist = forceString(record.value('ist'))
            status = forceString(record.value('status'))
            row = table.addRow()
            
            
            table.setText(row, 0, lastName + u' ' + firstName + u' ' + patrName)
            table.setText(row, 1, birthDate)
            table.setText(row, 2, value)
            table.setText(row, 3, note)
            table.setText(row, 4, ist)
            table.setText(row, 5, status)

        return doc

class CFinReestrSetupDialog(CReportSetupDialog):
    def __init__(self, parent=None):
        CReportSetupDialog.__init__(self, parent)
        self.setEventTypeVisible(False)
        self.setOnlyPermanentAttachVisible(False)
        self.chkDetailPerson.setVisible(False)
        self.setOrgStructureVisible(False)
        


        #страховая организация
        # self.cmbInsurer = CInsurerComboBox(self)
        # self.cmbInsurer.setObjectName("cmbInsurer")
        # self.gridLayout.addWidget(self.cmbInsurer, 11, 2, 1, 2)
        # self.lblInsurer = QtGui.QLabel(self)
        # self.lblInsurer.setText(u'Страховая организация')
        # self.lblInsurer.setObjectName("lblInsurer")
        # self.gridLayout.addWidget(self.lblInsurer, 11, 0, 1, 2)
        # self.lblInsurer.setBuddy(self.cmbInsurer)
        #Типы реестров
        

        #self.lblDetail.enterEvent = lambda self, event: self.chkDetail.enterEvent(self.chkDetail, event)
    def setTitle(self, title):
        self.setWindowTitle(title)

    def setParams(self, params):
        #self.cmbInsurer.setValue(params.get('insurerId', None))
        CReportSetupDialog.setParams(self, params)

    def params(self):
        result = CReportSetupDialog.params(self)
        return result

