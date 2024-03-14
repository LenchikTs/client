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
from Reports.ReportForm131_1000_SetupDialog import CReportForm131_1000_SetupDialog
  
    
class CRepForm30(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Паспорт врачебного участка. Форма 30')

    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setEventTypeVisible(False)
        result.setOnlyPermanentAttachVisible(False)
        result.setTitle(self.title())
        result.setOrgStructureVisible(False)
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
        stmt = u'''SELECT DISTINCT c.id AS num,count(c.id) as cnt,CONCAT(c.lastName,' ',c.firstName,' ',c.patrName) AS fio, CONCAT(cp.serial,' ',cp.number) as polis, c.SNILS as snils,  
    c.birthDate happy,getClientLocAddress(c.id) AS adress,lg.value AS lgot,m.DiagName mkbname,d.MKB AS mkb,rbN.name AS name,apbsn.value as serial,r.name AS result,'0' AS nul FROM Action a
    left join ActionType at on at.id = a.actionType_id
    left join ActionProperty ap_nomen on ap_nomen.action_id = a.id and ap_nomen.type_id in (select id from ActionPropertyType where typeName in ('Номенклатура ЛСиИМН'))
    left join ActionProperty_rbNomenclature nomen on nomen.id = ap_nomen.id
    left join ActionProperty ap_ser on ap_ser.action_id = a.id and ap_ser.type_id in (select id from ActionPropertyType where typeName in ('BlankSerialNumber'))
    left join ActionProperty_BlankSerialNumber apbsn  on apbsn.id = ap_ser.id
    left join ActionProperty ap_lg on ap_lg.action_id = a.id and ap_lg.type_id in (select id from ActionPropertyType where typeName in ('Льгота'))
    left join ActionProperty_rbSocStatus lg  on lg.id = ap_lg.id
    left join rbNomenclature rbN on rbN.id = nomen.value
    LEFT JOIN Event e ON a.event_id = e.id
    LEFT JOIN Client c ON e.client_id = c.id
    LEFT JOIN ClientPolicy cp ON c.id = cp.client_id
    LEFT JOIN Diagnosis d ON c.id = d.client_id
    LEFT JOIN MKB m ON m.DiagID=d.MKB
    LEFT JOIN rbResult r ON e.result_id = r.id
    where at.context = 'recipe' AND rbN.id IS NOT NULL AND d.MKB IS NOT NULL AND a.deleted=0 AND c.deleted=0 AND e.deleted=0 AND d.deleted=0 AND cp.deleted=0 and DATE(a.begDate) BETWEEN %(begDate)s AND %(endDate)s
    GROUP BY name
    ORDER BY fio
        '''% dict(begDate=db.formatDate(begDate),
                    endDate=db.formatDate(endDate)
                    )
        db = QtGui.qApp.db
        return db.query(stmt) 

    def build(self, params):
        reportData = {}
# osname = forceString(record.value('osname'))
  #              fin = forceString(record.value('fin'))
#                infis = forceString(record.value('infis'))
               # name = forceString(record.value('name'))
             #   amount = forceInt(record.value('amount'))
           #     kd = forceInt(record.value('kd'))
         #       pd = forceInt(record.value('pd'))
       #         uet = forceDouble(record.value('uet'))
     #           sum = forceDouble(record.value('sum'))
   #             cnt = forceInt(record.value('cnt'))
 #               pos = forceInt(record.value('pos'))

                #key = (osname, fin,   infis,  name)
              #  reportLine = reportData.setdefault(key, [0]*reportRowSize)
            #    reportLine[0] += amount
          #      reportLine[1] += kd
        #        reportLine[2] += pd
      #          reportLine[3] += uet
    #            reportLine[4] += sum
  #              reportLine[5] += cnt
#                 reportLine[6] += pos


        def processQuery(query):
            num=0
            tt = None
            while query.next():
                record = query.record()
                fio = forceString(record.value('fio'))
                polis = forceString(record.value('polis'))
                snils = forceString(record.value('snils'))
                happy = forceString(record.value('happy'))
                adress = forceString(record.value('adress'))
                lgot = forceString(record.value('lgot'))
                mkbname = forceString(record.value('mkbname'))
                mkb = forceString(record.value('mkb'))#
                name = forceString(record.value('name'))
                serial = forceString(record.value('serial'))
                result = forceString(record.value('result'))
                if tt!=(fio, mkb):
                    tt=(fio, mkb)
                    num +=1
                
                key = (num, fio,   happy , adress, lgot, mkbname, mkb, name, serial, result, polis, snils)
                reportLine = reportData.setdefault(key)
                
             #   reportLine[0] += kd
             #   reportLine[1] += sum
              #  reportLine[2] += cnt
        query = self.selectData(params)
        processQuery(query)
        
        # now text
        doc = QtGui.QTextDocument()
        doc.setDefaultStyleSheet("body{font-size: 10pt}")
        #doc.set
        cursor = QtGui.QTextCursor(doc)
        rt = CReportBase.ReportTitle
        rt.setFontWeight(QtGui.QFont.Normal)
        cursor.setCharFormat(rt)
        cursor.setBlockFormat(CReportBase.AlignCenter)
        cursor.insertHtml(u'''<table width="100%">
<tr>
<td width="25%" align=right>
ПАСПОРТ ВРАЧЕБНОГО УЧАСТКА ГРАЖДАН, ИМЕЮЩИХ ПРАВО НА<br>
ПОЛУЧЕНИЕ НАБОРА СОЦИАЛЬНЫХ УСЛУГ<br>
за ___ квартал 200__ г.
</td>
<td width="25%">
<br>
</td>
<td width="25%">

</td>
<td width="25%">
</td>
</tr>
<tr>
<td width="25%">
</td>

<td width="45%" align=center>
<br>
<br>
<br>
Ежеквартальная<br>
                                                  (по состоянию на 1 число следующего за<br>
                                                        отчетным кварталом месяца)
</td>
<td width="30%">
</td>
</tr>
<tr>
<td width="25%" align="left">
<br>
Ф. И. О. врача _________________________<br>
Должность ____________________________<br>
N участка _____________________________

</td>
</tr>
</table>''')
        cursor.setBlockFormat(CReportBase.AlignRight)
        cursor.setBlockFormat(CReportBase.AlignCenter)
        
        
        cursor.insertBlock()
        cursor.insertBlock()

        tableColumns = [
            ('4%',  [ u'Сведение участкового врача (ВОП)',u'N п/п',u'',u'',u'1'], CReportBase.AlignLeft),
            ('5%',  [ u'',u'Ф.И.О. пациента',u'',u'',u'2'], CReportBase.AlignRight),
            ('5%',  [ u'',u'номер страхового полиса ОМС',u'',u'',u'3'], CReportBase.AlignRight),
            ('5%',  [ u'',u'Снилс',u'',u'',u'4'], CReportBase.AlignRight),
            ('5%',  [ u'',u'Дата рождения',u'',u'',u'5'], CReportBase.AlignRight),
            ('5%',  [ u'',u'Адрес',u'',u'',u'6'], CReportBase.AlignRight), 
            ('3%',  [ u'',u'Код категории льготы',u'',u'',u'7'], CReportBase.AlignRight),
            ('5%',  [ u'',u'Наименование заболевания',u'',u'',u'8'], CReportBase.AlignRight),
            ('3%',  [ u'',u'код по МКБ-10',u'',u'',u'9'], CReportBase.AlignRight),
            ('5%',  [ u'',u'Дата постановки на учет',u'',u'',u'10'], CReportBase.AlignRight),
            ('5%',  [ u'',u'Дата снятия, причина',u'',u'',u'11'], CReportBase.AlignRight),
            ('5%',  [ u'',u'Число посещений',u'',u'',u'12'], CReportBase.AlignRight),
            ('5%',  [ u'Сведение ОМК',u'Лекарственное обеспечение',u'выписано',u'Наименование ЛС, дозировка',u'13'], CReportBase.AlignRight),
            ('5%',  [ u'',u'',u'выписано',u'Серия и номер рецепта',u'14'], CReportBase.AlignRight),
            ('5%',  [ u'',u'',u'Фактически получено (наименование ЛС, дозировка)',u'',u'15'], CReportBase.AlignRight),
            ('5%',  [ u'',u'',u'Стоимость лекарственного обеспечения',u'',u'16'], CReportBase.AlignLeft),
            ('5%',  [ u'',u'Санаторно-курортное и восстановительное лечение',u'Выдано:',u'справок на сан-кур лечение',u'17'], CReportBase.AlignLeft),
            ('5%',  [ u'',u'',u'',u'из них на амб-кур лечение',u'18'], CReportBase.AlignLeft),
            ('5%',  [ u'',u'',u'',u'сан-кур карт',u'19'], CReportBase.AlignLeft),
            ('5%',  [ u'',u'',u'Возвращено',u'',u'20'], CReportBase.AlignLeft),
            ('5%',  [ u'Направленно на госпитализацию, медицинскую реабилитацию,обследование, консультацию',u'',u'',u'',u'21'], CReportBase.AlignLeft),
            ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 1, 12)#верхние
        table.mergeCells(0, 12, 1, 8)#верхние
        table.mergeCells(0, 21, 4, 1)#верхние
        table.mergeCells(1, 0, 3, 1)#1
        table.mergeCells(1, 1, 3, 1)#2-3
        table.mergeCells(1, 2, 3, 1)#4
        table.mergeCells(1, 3, 3, 1)#5
        table.mergeCells(1, 4, 3, 1)#6
        table.mergeCells(1, 5, 3, 1)#7
        table.mergeCells(1, 6, 3, 1)#8
        table.mergeCells(1, 7, 3, 1)#9
        table.mergeCells(1, 8, 3, 1)#10
        table.mergeCells(1, 9, 3, 1)#11
        table.mergeCells(1, 10, 3, 1)#12
        table.mergeCells(1, 11, 3, 1)#13
        table.mergeCells(1, 12, 1, 4)#обеспеч
        table.mergeCells(2, 12,  1, 2)#выписано
        table.mergeCells(3, 12, 1, 1)#12
        table.mergeCells(3, 13, 1, 1)#13
        table.mergeCells(2, 14, 2, 1)#14
        table.mergeCells(1, 15, 3, 1)#15
        table.mergeCells(1, 16, 1, 4)#сан
        table.mergeCells(2, 16, 1, 3)#выдано
        table.mergeCells(3, 16, 1, 1)#16
        table.mergeCells(3, 17, 1, 1)#17
        table.mergeCells(3, 18, 1, 1)#18
        table.mergeCells(2, 19, 2, 1)#19
        table.mergeCells(0, 20, 4, 1)#20
        
        keys = reportData.keys()
        keys.sort()
        def drawTotal(table,  total,  text): 
    
            row = table.addRow()

            table.setText(row, 1, text, CReportBase.TableHeader)
            table.mergeCells(row, 0, 1, 2)
            
        ttt = None
        for key in keys:
            #key = (osname, fin,   infis,  name)
            
            
            snils = key[11]
            polis = key[10]
            result = key[9]
            serial = key[8]
            name = key[7]
            mkb = key[6]
            mkbname = key[5]
            lgot = key[4]
            adress = key[3]
            happy = key[2]
            fio = key[1]
            num= key[0]
           
            #mergeCells(int row, int column, int numRows, int numCols)
            row = table.addRow()     
            if ttt!=(fio, mkb):
                ttt=(fio, mkb)
                table.setText(row, 0, num)
                table.setText(row, 1, fio)
                table.setText(row, 2, polis)
                table.setText(row, 3, snils)
                table.setText(row, 4, happy)
                table.setText(row, 5, adress)
                table.setText(row, 6, lgot)
                table.setText(row, 7, mkbname)
                table.setText(row, 8, mkb)
                table.setText(row, 12, name)
                table.setText(row, 13, serial)
                table.setText(row, 20, result)
            else:
                table.setText(row, 12, name)
                table.setText(row, 13, serial)
                table.setText(row, 20, result)
            
        #total
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock() 
        cursor.insertHtml(u'''<br><br><table><tr><td>Участковый врач (ВОП) ________________________ </td><td>Заведующий ОМК ________________________</td></tr></table>''')
        cursor.insertHtml(u'''<br><table><tr><td>Дата "____" ______________ 200_ года</td></tr></table>''')
        return doc
