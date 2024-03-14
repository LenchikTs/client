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
  
    
class CRepLgotRecipe(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Сведения о количестве льготных рецептов, в разрезе льгот')
        
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
        stmt = u'''SELECT sst.code AS cod, COUNT(a.id) AS kol,COUNT( DISTINCT c.id) AS lud  FROM Action a
  left join ActionType at on at.id = a.actionType_id
  LEFT JOIN Person p ON a.person_id = p.id
left join ActionProperty ap_nomen on ap_nomen.action_id = a.id and ap_nomen.type_id in (select id from ActionPropertyType where typeName in ('Номенклатура ЛСиИМН'))
    left join ActionProperty_rbNomenclature nomen on nomen.id = ap_nomen.id
    left join rbNomenclature rbN on rbN.id = nomen.value
  LEFT JOIN Event e ON a.event_id = e.id
  LEFT JOIN Client c ON e.client_id = c.id
  LEFT JOIN ClientSocStatus css ON e.client_id = css.client_id
  LEFT JOIN rbSocStatusType sst ON css.socStatusType_id = sst.id
  LEFT JOIN rbSocStatusClass ssc ON css.socStatusClass_id = ssc.id
where at.context = 'recipe' AND rbN.id IS NOT NULL AND sst.id IS NOT NULL AND css.id IS NOT NULL AND ssc.group_id = 1  and DATE(a.begDate) BETWEEN %(begDate)s AND %(endDate)s
  GROUP BY sst.code
  ORDER BY cod
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
            ('30%',  [ u'Код льготы'], CReportBase.AlignLeft),
            ('35%',  [ u'Количество человек'], CReportBase.AlignRight),
            ('35%',  [ u'Количество выписанных рецептов'], CReportBase.AlignRight),
            ]

        table = createTable(cursor, tableColumns)
        query = self.selectData(params)
        while query.next():
            record = query.record()
            cod = forceString(record.value('cod'))
            kol = forceString(record.value('kol'))
            lud = forceString(record.value('lud'))
            row = table.addRow()
            table.setText(row, 0, cod)
            table.setText(row, 1, lud)
            table.setText(row, 2, kol)
        
        return doc
