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
from Orgs.Utils                 import getOrgStructurePersonIdList
from Reports.Utils import _getChiefName

from library.Utils      import *
from Reports.ReportView    import CPageFormat
  
    
class CLgot030(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.pageFormat = CPageFormat(pageSize=CPageFormat.A4, orientation=CPageFormat.Landscape, leftMargin=1, topMargin=1, rightMargin=1,  bottomMargin=1)
        self.setTitle(u'Форма N 030-Р/у')

    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setEventTypeVisible(False)
        result.setMKBFilterVisible(True)
        result.setOnlyPermanentAttachVisible(False)
        result.setTitle(self.title())
        result.setOrgStructureVisible(True)
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
        orgStructureId = params.get('orgStructureId', None)
        start=params.get('MKBFilter', 0)
        db = QtGui.qApp.db
        if start==1:
            MKBFrom   = params.get('MKBFrom', '')
            MKBTo     = params.get('MKBTo', '')
            cond0=u'''and d1.MKB BETWEEN "%s"''' % (MKBFrom)
            cond1=u''' and "%s"''' % (MKBTo)
            cond=cond0+cond1
        else:
            cond=u''
        condOrgStructure = u''
        if orgStructureId:
            personIdList = getOrgStructurePersonIdList(orgStructureId)
            if personIdList:
                condOrgStructure = u''' AND e.execPerson_id IN (%s)''' % (u','.join(str(personId) for personId in personIdList if personId))
        db = QtGui.qApp.db
        stmt = u'''SELECT DISTINCT c.id AS num,count(c.id) as cnt,CONCAT(p.lastName,' ',p.firstName,' ',p.patrName) AS fioP,CONCAT(c.lastName,' ',c.firstName,' ',c.patrName) AS fio,
    c.birthDate happy,CONCAT(cp.serial,' ',cp.number) AS pol,c.SNILS AS snil,rb.code AS lgot,SUBSTRING_INDEX (apbsn.value, ' ', 1) as serial,
  SUBSTRING_INDEX (apbsn.value, ' ', -1) as number,date(a.directionDate) AS nazn,IF(IFNULL(a.MKB, '') = '', d1.MKB, a.MKB) AS mkb,rbN.name AS name,vv.value as vk
FROM Action a
    left join ActionType at on at.id = a.actionType_id
    left join ActionProperty ap_nomen on ap_nomen.action_id = a.id and ap_nomen.type_id in (select id from ActionPropertyType where typeName in ('Номенклатура ЛСиИМН'))
    left join ActionProperty_rbNomenclature nomen on nomen.id = ap_nomen.id
    left join ActionProperty ap_ser on ap_ser.action_id = a.id and ap_ser.type_id in (select id from ActionPropertyType where typeName in ('BlankSerialNumber'))
    left join ActionProperty_BlankSerialNumber apbsn  on apbsn.id = ap_ser.id
    left join ActionProperty ap_lg on ap_lg.action_id = a.id and ap_lg.type_id in (select id from ActionPropertyType where typeName in ('Льгота'))
    left join ActionProperty_rbSocStatus lg  on lg.id = ap_lg.id
    left join rbSocStatusType rb  on rb.id = lg.value
    left join ActionProperty ap_vk on ap_vk.action_id = a.id and ap_vk.type_id in (select id from ActionPropertyType where name in ('Протокол ВК'))
    left join ActionProperty_String vv  on vv.id = ap_vk.id
    left join rbNomenclature rbN on rbN.id = nomen.value
    LEFT JOIN Event e ON a.event_id = e.id %(condOrgStructure)s
    LEFT JOIN Client c ON e.client_id = c.id
    LEFT JOIN ClientPolicy cp ON c.id = cp.client_id
    LEFT JOIN Diagnostic d ON e.id = d.event_id
    LEFT JOIN Diagnosis d1 ON d.diagnosis_id = d1.id
    LEFT JOIN MKB m ON m.DiagID=d1.MKB
    LEFT JOIN rbResult r ON e.result_id = r.id
    LEFT JOIN Person p ON p.id=a.setPerson_id
    where at.context = 'recipe' AND rbN.id IS NOT NULL AND d1.MKB IS NOT NULL AND a.deleted=0 AND 
  c.deleted=0 AND e.deleted=0 AND d.deleted=0 AND cp.deleted=0 AND (DATE(cp.endDate)>DATE(NOW()) OR cp.endDate IS NULL ) and DATE(a.begDate) BETWEEN %(begDate)s AND %(endDate)s %(cond)s
    GROUP BY fioP,fio,apbsn.value
    ORDER BY fioP
        '''% dict(begDate=db.formatDate(begDate),
                    endDate=db.formatDate(endDate),
                    condOrgStructure=condOrgStructure, 
                    cond=cond
                    )
        db = QtGui.qApp.db
        return db.query(stmt) 

    def build(self, params):
        reportRowSize = 12
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
            prevnum=0
            num=0
            while query.next():
                record = query.record()
                fioP= forceString(record.value('fioP'))#name
                fio= forceString(record.value('fio'))#name
                happy = forceString(record.value('happy'))#+
                pol = forceString(record.value('pol'))#+
                snil = forceString(record.value('snil'))#+
                lgot = forceString(record.value('lgot'))#+
                serial = forceString(record.value('serial'))#+
                number = forceString(record.value('number'))#+
                nazn = forceString(record.value('nazn'))#+
                mkb = forceString(record.value('mkb'))#+
                name = forceString(record.value('name'))#+
                vk = forceString(record.value('vk'))#+
                if prevnum!=fioP:
                    num = 1
                    prevnum = fioP
                else:
                    num += 1

                key = (fioP, num, nazn, fio, happy, pol, snil, lgot, serial, number, mkb, name)
                reportLine = reportData.setdefault(key)
                
             #   reportLine[0] += kd
             #   reportLine[1] += sum
              #  reportLine[2] += cnt
        query = self.selectData(params)
        processQuery(query)
        lpuName = forceString(QtGui.qApp.db.translate('Organisation', 'id', QtGui.qApp.currentOrgId(), 'fullName'))
        lpuAddress = forceString(QtGui.qApp.db.translate('Organisation', 'id', QtGui.qApp.currentOrgId(), 'address'))
        lpuOGRN = forceString(QtGui.qApp.db.translate('Organisation', 'id', QtGui.qApp.currentOrgId(), 'OGRN'))
        lpuChief = _getChiefName(QtGui.qApp.currentOrgId())
        lpu=u'<table width=100%><tr><td width=50% align=center>Министерство здравоохранения и социального <br>развития Российской Федерации <br>' + lpuName +'<br>'+ lpuAddress + u'<br></td><td width=50% align=right>Медицинская документация<br>Форма N 030-Р/у ________<br>утверждена приказом Минздравсоцразвития<br>России<br>от 22.11.2004 г. N 255<br></td></tr></table></tr>'
        chief=u'<table width=100%><tr>        <td width=50% align=center>         <br>Код ОГРН ' + lpuOGRN + u'<br></td><td width=50% align=right>Утверждаю: '+ lpuChief + u'<br>Руководитель медицинской организации<br>"___" __________ 200___ г.</td></tr></table></tr>'
        centr=u'<table width=100%><tr><td align=center>СВЕДЕНИЯ О ЛЕКАРСТВЕННЫХ СРЕДСТВАХ, ВЫПИСАННЫХ И ОТПУЩЕННЫХ ГРАЖДАНАМ,<br>                         ИМЕЮЩИМ ПРАВО НА ПОЛУЧЕНИЕ НАБОРА СОЦИАЛЬНЫХ УСЛУГ<br>                     (в соответствии с Федеральным законом от 22.08.2004 N 122)<br></td></tr></table>'
        
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
<td width="25%" align=left>
Приложение 7<br>
&nbsp;&nbsp;&nbsp;к приказу Министерства здравоохранения<br>
&nbsp;&nbsp;&nbsp;и социального развития Российской Федерации<br>
&nbsp;&nbsp;&nbsp;от 22 ноября 2004 г.<br>
&nbsp;&nbsp;&nbsp;N 255
</td>
<td width="25%">
<br>
</td>
<td width="25%">

</td>
<td width="25%">
</td>
</tr>
</table>''')
        cursor.insertHtml(u'''%s '''% lpu)
        cursor.insertHtml(u'''%s '''% chief)
        cursor.insertHtml(u'''%s '''% centr)
        cursor.insertBlock()
        cursor.setBlockFormat(CReportBase.AlignRight)
        self.dumpParams(cursor, params, CReportBase.AlignRight)
        cursor.insertBlock()       
        cursor.setBlockFormat(CReportBase.AlignCenter)
        
        
        cursor.insertBlock()
        cursor.insertBlock()

        tableColumns = [
            ('3%',  [ u'Заполняется специалистом ОМК', u'N п/п', u'1'], CReportBase.AlignLeft),            
            ('5%',  [u'', u'Дата выписки', u'2'], CReportBase.AlignLeft),
            ('15%',  [ u'',u'Фамилия Имя Отчество пациента', u'3'], CReportBase.AlignLeft),
            ('5%',  [ u'',u'Дата рождения', u'4'], CReportBase.AlignLeft),
            ('7%',  [u'', u'Серия, номер полиса(паспорта)', u'5'], CReportBase.AlignLeft),
            ('7%',  [u'', u'Снилс', u'6'], CReportBase.AlignLeft),
            ('5%',  [ u'',u'Код льготы', u'7'], CReportBase.AlignLeft),
            ('5%',  [u'', u'Серия', u'8'], CReportBase.AlignLeft),
            ('7%',  [u'', u'Номер', u'9'], CReportBase.AlignLeft),
            ('7%',  [u'', u'Код МКБ-Х', u'10'], CReportBase.AlignLeft),
            ('24%',  [u'', u'Лекарственное средство', u'11'], CReportBase.AlignLeft),
            ('2%',  [ u'Заполняется на основании сведений аптечного учреждения* ', u'Дата отпуска', u'12'], CReportBase.AlignLeft),
            ('2%',  [u'', u'Наименование отпущенного ЛС (код)', u'13'], CReportBase.AlignLeft),
            ('2%',  [ u'',u'Стоимость упаковки', u'14'], CReportBase.AlignLeft),
            ('2%',  [ u'',u'Отпущено упаковок', u'15'], CReportBase.AlignLeft),
            ('2%',  [u'', u'Общая стоимость 1 отпуска', u'16'], CReportBase.AlignLeft),
            ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 1, 11)# Заполняется специалистом ОМК
        table.mergeCells(0, 11, 1, 5)#Заполняется на основании сведений аптечного учреждения* 
        for col in xrange(reportRowSize):
            table.mergeCells(0, col, 2, 1)


        totalBynum = [0]*reportRowSize
        totalByReport = [0]*reportRowSize
        prevnum = None
        coun=None
        cnt=None
        ttt=None
        tt=None
        allcnt=0
        allcoun=0
        
        keys = reportData.keys()
        keys.sort()
        def drawTotal(table,  total,  text): 
    
            row = table.addRow()

            table.setText(row, 1, text, CReportBase.TableHeader)
            table.mergeCells(row, 0, 1, 11)
        for key in keys:
            #key = (fioP, num, nazn, fio, happy, pol, snil, lgot, serial, number, mkb, name)
            
            fioP= key[0]
            num = key[1]
            name = key[11]
            mkb = key[10]
            nazn = key[2]
            number = key[9]
            serial = key[8]
            lgot = key[7]
            snil = key[6]
            pol = key[5]
            happy = key[4]
            fio = key[3]
            #mergeCells(int row, int column, int numRows, int numCols)
            
        
            
            if prevnum!=None and prevnum!=fioP:
                drawTotal(table,  totalBynum, u'Количество пациентов %s ' %  cnt);
                drawTotal(table,  totalBynum, u'Количество рецептов %s ' %  coun);
                totalBynum = [0]*reportRowSize
                
            if ttt==(fioP) :
                if tt!=(fio):
                    cnt=cnt+1
                    allcnt+=1
                coun=coun+1
                allcoun+=1
            else:
                cnt=0
                coun=0
                cnt=cnt+1
                coun=coun+1
                allcnt+=1
                allcoun+=1
                
            
            if prevnum!=fioP:
                row = table.addRow()
                table.setText(row, 0, fioP, CReportBase.TableHeader)
                table.mergeCells(row, 0, 1, 11)
                
            row = table.addRow()          
            table.setText(row, 0, num)
            table.setText(row, 1, nazn)
            table.setText(row, 2, fio)
            table.setText(row, 3, happy)
            table.setText(row, 4, pol)
            table.setText(row, 5, snil)
            table.setText(row, 6, lgot)
            table.setText(row, 7, serial)
            table.setText(row, 8, number)
            table.setText(row, 9, mkb)
            table.setText(row, 10, name)
            
            prevnum = fioP
            ttt =   (fioP)
            tt =   (fio)
        #total
        drawTotal(table,  totalBynum, u'Количество пациентов %s ' %  cnt);
        drawTotal(table,  totalBynum, u'Количество рецептов %s ' %  coun);
        drawTotal(table,  totalBynum, u'ИТОГО пациентов %s ' %  allcnt);
        drawTotal(table,  totalBynum, u'ИТОГО рецептов %s ' %  allcoun);
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock() 
        cursor.insertHtml(u'''<br><table><tr><td>Итого на общую сумму ____________________________________________</td></tr></table>''')
        cursor.insertHtml(u'''<br><table><tr><td>Специалист ОМК _________________________________________________</td></tr></table>''')
        cursor.insertHtml(u'''<br><table><tr><td>Работник аптечного учреждения ___________________________________</td></tr></table>''')
        cursor.insertHtml(u'''<table><tr><td><br>*представляется в ЛПУ 2 раза в месяц</td></tr></table>''')
        return doc
