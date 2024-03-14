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
from PyQt4.QtCore import *
from Reports.Report     import *
from Reports.ReportBase import *

from library.Utils      import *
from Reports.ReportSetupDialog import CReportSetupDialog
  
    
class CRep060Y(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Журнал учета инфекционных заболеваний')
        
    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setEventTypeVisible(False)
        result.setOnlyPermanentAttachVisible(False)
        result.setTitle(self.title())
        return result
        
    def selectData(self, params):    
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        if not endDate or endDate.isNull():
            return None
        db = QtGui.qApp.db
        stmt = u'''SELECT api.value AS num,convert(CONCAT('Прием ',apd.value,' ',apt.value,', отсылка ',apd_extr.value,', принял ',aps.value), char) AS two,o.fullName AS nam,
  CONCAT(c.lastName,' ',c.firstName,' ',c.patrName)  AS FIO,if (age(c.birthDate,a.begDate)<3,
  c.birthDate,age(c.birthDate,a.begDate)) AS age, getClientLocAddress(c.id) AS adres,if (cw.freeInput IS NULL OR cw.freeInput='','безработный',cw.freeInput) AS work,
  apd_zab.value AS zab,CONCAT(a.MKB,', ',apd_diag.value) AS mkb,convert(CONCAT(e.setDate,', ',o.fullName),char) AS post,apd_dobr.value AS gosp,' ' AS 'z12','' AS 'z13','' AS 'z14',
  apsli.value AS iss,'' AS 'z16'
  FROM Action a 
  LEFT JOIN ActionType at ON a.actionType_id = at.id
  LEFT JOIN Event e ON a.event_id = e.id
  LEFT JOIN Client c ON e.client_id = c.id
  LEFT JOIN ClientWork cw ON c.id = cw.client_id and cw.id = (SELECT MAX(cl.id) FROM ClientWork cl WHERE cl.deleted=0 AND cl.client_id=c.id)
  LEFT JOIN Organisation o ON e.org_id = o.id
  left join ActionProperty ap on ap.action_id = a.id and ap.type_id in (select id from ActionPropertyType where name = 'Номер извещения') AND ap.deleted = 0
  left join ActionProperty_Integer api on api.id = ap.id
  left join ActionProperty ap_teld on ap_teld.action_id = a.id and ap_teld.type_id in (select id from ActionPropertyType where name = 'Дата сообщения по телефону') AND ap_teld.deleted = 0
  left join ActionProperty_Date apd on apd.id = ap_teld.id
  left join ActionProperty ap_telt on ap_telt.action_id = a.id and ap_telt.type_id in (select id from ActionPropertyType where name = 'Время сообщения по телефону') AND ap_telt.deleted = 0
  left join ActionProperty_Time apt on apt.id = ap_telt.id
  left join ActionProperty ap_dobr on ap_dobr.action_id = a.id and ap_dobr.type_id in (select id from ActionPropertyType where name = 'Дата первичного обращения') AND ap_dobr.deleted = 0
  left join ActionProperty_Date apd_dobr on apd_dobr.id = ap_dobr.id
  left join ActionProperty ap_diag on ap_diag.action_id = a.id and ap_diag.type_id in (select id from ActionPropertyType where name = 'Дата установления предв. диагноза') AND ap_diag.deleted = 0
  left join ActionProperty_Date apd_diag on apd_diag.id = ap_diag.id
  left join ActionProperty ap_extr on ap_extr.action_id = a.id and ap_extr.type_id in (select id from ActionPropertyType where name = 'Дата отсылки экстренного извещения') AND ap_extr.deleted = 0
  left join ActionProperty_Date apd_extr on apd_extr.id = ap_extr.id
  left join ActionProperty ap_extrpri on ap_extrpri.action_id = a.id and ap_extrpri.type_id in (select id from ActionPropertyType where name = 'Экстренное извещение принял') AND ap_extrpri.deleted = 0
  left join ActionProperty_String aps on aps.id = ap_extrpri.id
  left join ActionProperty ap_dou on ap_dou.action_id = a.id and ap_dou.type_id in (select id from ActionPropertyType where name = 'Дата последнего посещения ДОУ или школы') AND ap_dou.deleted = 0
  left join ActionProperty_Date apd_dou on apd_dou.id = ap_dou.id
  left join ActionProperty ap_zab on ap_zab.action_id = a.id and ap_zab.type_id in (select id from ActionPropertyType where name = 'Дата заболевания') AND ap_zab.deleted = 0
  left join ActionProperty_Date apd_zab on apd_zab.id = ap_zab.id
  left join ActionProperty ap_li on ap_li.action_id = a.id and ap_li.type_id in (select id from ActionPropertyType where name = 'Л/И и результат') AND ap_li.deleted = 0
  left join ActionProperty_String apsli on apsli.id = ap_li.id
  WHERE at.context='f058' AND a.deleted=0 AND e.deleted=0 AND at.deleted=0 AND c.deleted=0 AND DATE(a.begDate) BETWEEN %(begDate)s AND %(endDate)s
  ORDER BY num
        ''' % {'begDate': db.formatDate(begDate),
               'endDate': db.formatDate(endDate),
               }
        db = QtGui.qApp.db
        return db.query(stmt)
        
       
    def build(self, params):
        query = self.selectData(params)
        query.first()
        
        
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        #рисуем первую табличку
        tableColumns = [
            ('6%',  [ u'N п/п', '1'], CReportBase.AlignLeft),
            ('6%',  [ u'Дата и часы сообщения (приема) по телефону и дата отсылки (получения) первичного экстренного извещения, кто передал, кто принял	', '2'], CReportBase.AlignRight),
            ('6%',  [ u'Наименование лечебного учреждения, сделавшего сообщение', '3'], CReportBase.AlignRight),
            ('6%',  [ u'Фамилия, имя, отчество больного', '4'], CReportBase.AlignRight), 
            ('6%',  [ u'Возраст (для детей до 3 лет указать месяц и год рождения)	', '5'], CReportBase.AlignRight),
            ('6%',  [ u'Домашний адрес (город, село, улица, дом N, кв. N)', '6'], CReportBase.AlignRight),
            ('6%',  [ u'Наименование места работы, учебы, дошкольного детского учреждения, группа, класс, дата последнего посещения', '7'], CReportBase.AlignRight),
            ('6%',  [ u'Дата заболевания', '8'], CReportBase.AlignRight),
            ('6%',  [ u'Диагноз и дата его установления', '9'], CReportBase.AlignRight),
            ('6%',  [ u'Дата, место госпитализации', '10'], CReportBase.AlignRight),
            ('6%',  [ u'Дата первичного обращения', '11'], CReportBase.AlignRight),
            ('6%',  [ u'Измененный (уточненный) диагноз и дата его установления', '12'], CReportBase.AlignRight),
            ('6%',  [ u'Дата эпид. обследования Фамилия обследовавшего', '13'], CReportBase.AlignRight),
            ('6%',  [ u'Сообщено о заболеваниях (в СЭС по месту постоянного жительства, в детское учреждение, по месту учебы, работы и др.)', '14'], CReportBase.AlignRight),
            ('6%',  [ u'Лабораторное обследование и его результат', '15'], CReportBase.AlignRight),
            ('6%',  [ u'Примечание', '16'], CReportBase.AlignRight),
            ]

        table = createTable(cursor, tableColumns)
        query = self.selectData(params)

        while query.next():
            record = query.record()
            num = forceInt(record.value('num'))
            two = forceString(record.value('two'))
            nam = forceString(record.value('nam'))
            FIO = forceString(record.value('FIO'))
            age = forceString(record.value('age'))
            adres = forceString(record.value('adres'))
            work = forceString(record.value('work'))
            zab = forceString(record.value('zab'))
            mkb = forceString(record.value('mkb'))
            post = forceString(record.value('post'))
            gosp = forceString(record.value('gosp'))
            z12 = forceString(record.value('z12'))
            z13 = forceString(record.value('z13'))
            z14 = forceString(record.value('z14'))
            iss = forceString(record.value('iss'))
            z16 = forceString(record.value('z16'))
            row = table.addRow()
            #table.mergeCells(0, 0, 1, 1)
            table.setText(row, 0, num)
            table.setText(row, 1, two)
            table.setText(row, 2, nam)  
            table.setText(row, 3, FIO)
            table.setText(row, 4, age)
            table.setText(row, 5, adres)  
            table.setText(row, 6, work) 
            table.setText(row, 7, zab)
            table.setText(row, 8, mkb)
            table.setText(row, 9, post)  
            table.setText(row, 10, gosp)
            table.setText(row, 11, z12)
            table.setText(row, 12, z13)  
            table.setText(row, 13, z14)
            table.setText(row, 14, iss)
            table.setText(row, 15, z16)
        

        return doc
