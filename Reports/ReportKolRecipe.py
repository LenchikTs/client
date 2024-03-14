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
  
    
class CRepKolRecipe(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Сведение о колличестве льготных рецептов, выписанных врачами')
        
    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setEventTypeVisible(False)
        result.setOnlyPermanentAttachVisible(False)
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
        if not endDate or endDate.isNull():
            return None  
        db = QtGui.qApp.db
        stmt = u'''SELECT p.regionalCode AS cod, CONCAT(p.lastName,' ',p.firstName,' ',p.patrName) AS nam,COUNT(at.context) as kol,
  SUM(case when aps.value='Муниципальный' then 1 else 0 end) AS mun,SUM(case when aps.value='Муниципальный' AND aps_vk.value='да' then 1 else 0 end) AS mun_vk,
  SUM(case when aps.value='Субъект РФ' then 1 else 0 end) AS sub,SUM(case when aps.value='Субъект РФ' AND aps_vk.value='да' then 1 else 0 end) AS sub_vk,
  SUM(case when aps.value='Федеральный' then 1 else 0 end) AS fed, SUM(case when aps.value='Федеральный' AND aps_vk.value='да' then 1 else 0 end) AS fed_vk,
  SUM(case when aps.value='Гуманитарная помощь' then 1 else 0 end) AS gum,SUM(case when aps.value='Гуманитарная помощь' AND aps_vk.value='да' then 1 else 0 end) AS gum_vk 
  FROM Action a
  left join ActionType at on at.id = a.actionType_id
  LEFT JOIN Person p ON a.person_id = p.id
left join ActionProperty ap_nomen on ap_nomen.action_id = a.id and ap_nomen.type_id in (select id from ActionPropertyType where typeName in ('Номенклатура ЛСиИМН'))
left join ActionProperty ap_n on ap_n.action_id = a.id and ap_n.type_id in (select id from ActionPropertyType where Name=('Источник финансирования') AND typeName='String')
  left join ActionProperty ap_vk on ap_vk.action_id = a.id and ap_vk.type_id in (select id from ActionPropertyType where Name=('Протокол ВК') AND typeName='String')
  LEFT JOIN ActionProperty_String aps ON ap_n.id = aps.id
  LEFT JOIN ActionProperty_String aps_vk ON ap_vk.id = aps_vk.id
    left join ActionProperty_rbNomenclature nomen on nomen.id = ap_nomen.id
    left join rbNomenclature rbN on rbN.id = nomen.value
where at.context = 'recipe' AND rbN.id IS NOT NULL and DATE(a.begDate) BETWEEN %(begDate)s AND %(endDate)s
  GROUP BY cod,nam
ORDER BY nam
        '''% {'begDate': db.formatDate(begDate),
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
            ('7%',  [ u'Таб. N'], CReportBase.AlignLeft),
            ('30%',  [ u'Фамилия И. О.'], CReportBase.AlignRight),
            ('7%',  [ u'Колличество выписанных рецептов',u'Всего'], CReportBase.AlignRight),
            ('7%',  [ u'',u'Из них в разрезе источников финнсирования',u'Федеральный',u'Всего'], CReportBase.AlignRight), 
            ('7%',  [ u'',u'',u'',u'По решению врачебной комиссии'], CReportBase.AlignRight),
            ('7%',  [ u'',u'',u'Субъект РФ',u'Всего'], CReportBase.AlignRight),
            ('7%',  [ u'',u'',u'',u'По решению врачебной комиссии'], CReportBase.AlignRight),
            ('7%',  [ u'',u'',u'Муниципальный',u'Всего'], CReportBase.AlignRight),
            ('7%',  [ u'',u'',u'',u'По решению врачебной комиссии'], CReportBase.AlignRight),
            ('7%',  [ u'',u'',u'Гумманитарная помощь',u'Всего'], CReportBase.AlignRight),
            ('7%',  [ u'',u'',u'',u'По решению врачебной комиссии'], CReportBase.AlignRight),
            ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 4, 1)
        table.mergeCells(0, 1, 4, 1)
        table.mergeCells(0, 2, 1, 9)
        table.mergeCells(1, 2, 3, 1)
        table.mergeCells(1, 3, 1, 8)
        table.mergeCells(2, 3, 1, 2)
        table.mergeCells(2, 5, 1, 2)
        table.mergeCells(2, 7, 1, 2)
        table.mergeCells(2, 9, 1, 2)
        query = self.selectData(params)
        while query.next():
            record = query.record()
            cod = forceInt(record.value('cod'))
            nam = forceString(record.value('nam'))
            nam = forceString(record.value('nam'))
            kol = forceString(record.value('kol'))
            kol = forceString(record.value('kol'))
            fed = forceString(record.value('fed'))
            fed_vk = forceString(record.value('fed_vk'))
            sub = forceString(record.value('sub'))
            sub_vk = forceString(record.value('sub_vk'))
            mun = forceString(record.value('mun'))
            mun_vk = forceString(record.value('mun_vk'))
            gum = forceString(record.value('gum'))
            gum_vk = forceString(record.value('gum_vk'))
            row = table.addRow()
            
            table.setText(row, 0, cod)
            table.setText(row, 1, nam)
            table.setText(row, 2, kol)  
            table.setText(row, 3, fed)
            table.setText(row, 4, fed_vk)
            table.setText(row, 5, sub)  
            table.setText(row, 6, sub_vk) 
            table.setText(row, 7, mun)
            table.setText(row, 8, mun_vk)
            table.setText(row, 9, gum)  
            table.setText(row, 10, gum_vk)
        
        
        return doc
