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

from library.Utils      import *
from Reports.ReportForm131_1000_SetupDialog import CReportForm131_1000_SetupDialog
  
    
class CLgotRecip(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Список выписанных льготных рецептов')

    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setEventTypeVisible(False)
        result.setMKBFilterVisible(True)
        result.setPersonVisible(True)
        result.cmbPerson.setVisible(False)
        result.lblPerson.setVisible(False)
        result.chkDetailPerson.setText(u'Выводить подробную информацию')
        result.setOnlyPermanentAttachVisible(False)
        result.setTitle(self.title())
        result.setOrgStructureVisible(True)
        result.setActionStatusVisible(True)
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
        chkDetailPerson   = params.get('detailPerson', False)
        if chkDetailPerson:
            dop1 = u''' ,pri.value AS pri,prin.value AS prin,dlit.value AS dlit,signa.value AS signa'''
            dop2 = u''' left join ActionPropertyType apt7 on apt7.actionType_id = at.id and apt7.name = 'На один прием' and apt7.deleted = 0
    left join ActionProperty ap_pri on ap_pri.action_id = a.id and ap_pri.type_id = apt7.id
    left join ActionProperty_String pri on pri.id = ap_pri.id

    left join ActionPropertyType apt8 on apt8.actionType_id = at.id and apt8.name = 'Принимать' and apt8.deleted = 0
    left join ActionProperty ap_prin on ap_prin.action_id = a.id and ap_prin.type_id = apt8.id
    left join ActionProperty_Double prin on prin.id = ap_prin.id
  
    left join ActionPropertyType apt9 on apt9.actionType_id = at.id and apt9.name = 'длительность' and apt9.deleted = 0
    left join ActionProperty ap_dlit on ap_dlit.action_id = a.id and ap_dlit.type_id = apt9.id
    left join ActionProperty_String dlit on dlit.id = ap_dlit.id

    left join ActionPropertyType apt0 on apt0.actionType_id = at.id and apt0.name = 'Signa' and apt0.deleted = 0
    left join ActionProperty ap_sign on ap_sign.action_id = a.id and ap_sign.type_id = apt0.id
    left join ActionProperty_String signa on signa.id = ap_sign.id'''
        else:
            dop1 = u''' '''
            dop2 = u''' '''
        orgStructureId = params.get('orgStructureId', None)
        actStatus=params.get('ActionStatus', None)
        if actStatus or actStatus==0:
            condactStatus = u''' AND a.status = (%s)''' % (actStatus)
        else:
            condactStatus =u''
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
    c.birthDate happy,CONCAT(cp.serial,' ',cp.number) AS pol,cd.serial as pasSerial,cd.number as pasNumber,c.SNILS AS snil,rb.code AS lgot,SUBSTRING_INDEX (apbsn.value, ' ', 1) as serial,
  SUBSTRING_INDEX (apbsn.value, ' ', -1) as number,date(a.directionDate) AS nazn,IF(IFNULL(a.MKB, '') = '', d1.MKB, a.MKB) AS mkb,rbN.name AS name,vv.value as vk,pr.value as prim,vv1.value as ddt
  %(dop1)s
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
    left join ActionProperty ap_vk1 on ap_vk1.action_id = a.id and ap_vk1.type_id in (select id from ActionPropertyType where name in ('D.t.d.'))
    left join ActionProperty_String vv1  on vv1.id = ap_vk1.id
    left join ActionProperty ap_pr on ap_pr.action_id = a.id and ap_pr.type_id in (select id from ActionPropertyType where name in ('Примечание'))
    left join ActionProperty_String pr  on pr.id = ap_pr.id
    LEFT JOIN Event e ON a.event_id = e.id %(condOrgStructure)s
    LEFT JOIN Client c ON e.client_id = c.id
    LEFT JOIN ClientPolicy cp ON c.id = cp.client_id
    LEFT JOIN Diagnostic d ON e.id = d.event_id
    LEFT JOIN Diagnosis d1 ON d.diagnosis_id = d1.id
    LEFT JOIN MKB m ON m.DiagID=d1.MKB
    LEFT JOIN rbResult r ON e.result_id = r.id
    LEFT JOIN Person p ON p.id=a.setPerson_id
    LEFT JOIN ClientDocument cd ON cd.id=getClientDocumentId(c.id)
    %(dop2)s
    where at.context = 'recipe' AND rbN.id IS NOT NULL AND d1.MKB IS NOT NULL AND a.deleted=0 AND 
  c.deleted=0 AND e.deleted=0 AND d.deleted=0 AND cp.deleted=0 AND (DATE(cp.endDate)>DATE(NOW()) OR cp.endDate IS NULL ) and DATE(a.begDate) BETWEEN %(begDate)s AND %(endDate)s %(cond)s %(condactStatus)s
    GROUP BY fioP,fio,apbsn.value
    ORDER BY fioP
        '''% dict(begDate=db.formatDate(begDate),
                    endDate=db.formatDate(endDate),
                    condOrgStructure=condOrgStructure, 
                    cond=cond, 
                    condactStatus=condactStatus, 
                    dop1=dop1, 
                    dop2=dop2
                    )
        db = QtGui.qApp.db
        return db.query(stmt) 

    def build(self, params):
        chkDetailPerson   = params.get('detailPerson', False)
        a=params.get('ActionStatus', None)
        if a==4:
            reportRowSize = 21
        else:
            reportRowSize = 19
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
        if chkDetailPerson:

			def processQuery(query):
				while query.next():
					record = query.record()
					fioP= forceString(record.value('fioP'))#name
					fio= forceString(record.value('fio'))#name
					happy = forceString(record.value('happy'))#+
					pol = forceString(record.value('pol'))#+
					pasSerial = forceString(record.value('pasSerial'))#+
					pasNumber = forceString(record.value('pasNumber'))#+
					snil = forceString(record.value('snil'))#+
					lgot = forceString(record.value('lgot'))#+
					ddt = forceString(record.value('ddt'))#+
					serial = forceString(record.value('serial'))#+
					number = forceString(record.value('number'))#+
					nazn = forceString(record.value('nazn'))#+
					mkb = forceString(record.value('mkb'))#+
					name = forceString(record.value('name'))#+
					vk = forceString(record.value('vk'))#+
					prim = forceString(record.value('prim'))#+
					pri = forceString(record.value('pri'))#+
					prin = forceString(record.value('prin'))#+
					dlit = forceString(record.value('dlit'))#+
					signa = forceString(record.value('signa'))#+
					
					key = (fioP, fio, happy, pol, pasSerial, pasNumber, snil, lgot, serial, number,nazn, ddt, mkb, name, vk, prim, pri, prin, dlit, signa)
					reportLine = reportData.setdefault(key)
					
				 #   reportLine[0] += kd
				 #   reportLine[1] += sum
				  #  reportLine[2] += cnt
			query = self.selectData(params)
			processQuery(query)
			
			# now text
			doc = QtGui.QTextDocument()
			cursor = QtGui.QTextCursor(doc)

			cursor.setCharFormat(CReportBase.ReportTitle)
			cursor.insertText(self.title())
			cursor.insertBlock()
			self.dumpParams(cursor, params)
			cursor.setCharFormat(CReportBase.ReportBody)
			cursor.insertBlock()
			if a==4:
				tableColumns = [
				('250',  [ u'Фамилия Имя Отчество'], CReportBase.AlignLeft),
				('150',  [ u'Дата рождения'], CReportBase.AlignLeft),
				('150',  [ u'Серия, номер полиса'], CReportBase.AlignLeft),
				('100',  [ u'УДЛ',u'серия'], CReportBase.AlignLeft),
				('100',  [ u'',u'номер'], CReportBase.AlignLeft),
				('100',  [ u'Снилс'], CReportBase.AlignRight),
				('100',  [ u'Код льготы'], CReportBase.AlignRight),
				('100',  [ u'Рецепт', u'Серия'], CReportBase.AlignRight),
				('100',  [ u'', u'Номер'], CReportBase.AlignRight),
				('100',  [ u'', u'Дата выписки'], CReportBase.AlignRight),
				('100',  [ u'D.t.d'], CReportBase.AlignRight),
				('100',  [ u'Код МКБ-Х'], CReportBase.AlignRight),
				('250',  [ u'Лекарственное средство'], CReportBase.AlignRight),
				('50',  [ u'Сумма'], CReportBase.AlignRight),
				('100',  [ u'По решению врачебной комиссии'], CReportBase.AlignRight),
				('100',  [ u'На один прием'], CReportBase.AlignRight),
				('100',  [ u'Принимать'], CReportBase.AlignRight),
				('100',  [ u'Длительность'], CReportBase.AlignRight),
				('100',  [ u'Signa'], CReportBase.AlignRight),
				('100',  [ u'Примечание'], CReportBase.AlignRight),
				]
			else:
				tableColumns = [
				('250',  [ u'Фамилия Имя Отчество'], CReportBase.AlignLeft),
				('150',  [ u'Дата рождения'], CReportBase.AlignLeft),
				('150',  [ u'Серия, номер полиса'], CReportBase.AlignLeft),
				('100',  [ u'УДЛ',u'серия'], CReportBase.AlignLeft),
				('100',  [ u'',u'номер'], CReportBase.AlignLeft),
				('100',  [ u'Снилс'], CReportBase.AlignRight),
				('100',  [ u'Код льготы'], CReportBase.AlignRight),
				('100',  [ u'Рецепт', u'Серия'], CReportBase.AlignRight),
				('100',  [ u'', u'Номер'], CReportBase.AlignRight),
				('100',  [ u'', u'Дата выписки'], CReportBase.AlignRight),
				('100',  [ u'D.t.d'], CReportBase.AlignRight),
				('100',  [ u'Код МКБ-Х'], CReportBase.AlignRight),
				('250',  [ u'Лекарственное средство'], CReportBase.AlignRight),
				('50',  [ u'Сумма'], CReportBase.AlignRight),
				('100',  [ u'По решению врачебной комиссии'], CReportBase.AlignRight),
				('100',  [ u'На один прием'], CReportBase.AlignRight),
				('100',  [ u'Принимать'], CReportBase.AlignRight),
				('100',  [ u'Длительность'], CReportBase.AlignRight),
				('100',  [ u'Signa'], CReportBase.AlignRight),
				]
			

			table = createTable(cursor, tableColumns)
			table.mergeCells(0, 3, 1, 2)
			table.mergeCells(0, 7, 1, 3)
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
				table.mergeCells(row, 0, 1, reportRowSize)
			for key in keys:
				#key = (fioP, fio, happy, pol, pasSerial, pasNumber, snil, lgot, serial, number,nazn, ddt, mkb, name, vk, prim, pri, prin, dlit, signa)
				
				fioP= key[0]
				ddt = key[11]
				signa = key[19]
				dlit = key[18]
				prin = key[17]
				pri = key[16]
				prim = key[15]
				vk = key[14]
				name = key[13]
				mkb = key[12]
				nazn = key[10]
				number = key[9]
				serial = key[8]
				lgot = key[7]
				snil = key[6]
				pasNumber = key[5]
				pasSerial = key[4]
				pol = key[3]
				happy = key[2]
				fio = key[1]
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
					table.mergeCells(row, 0, 1, reportRowSize)
				# key = (fioP, fio, happy, pol, pasSerial, pasNumber, snil, lgot, serial, number,nazn, ddt, mkb, name, vk, prim, pri, prin, dlit, signa)
				row = table.addRow()          
				if a==4:
					table.setText(row, 0, fio)
					table.setText(row, 1, happy)
					table.setText(row, 2, pol)
					table.setText(row, 3, pasSerial)
					table.setText(row, 4, pasNumber)
					table.setText(row, 5, snil)
					table.setText(row, 6, lgot)
					table.setText(row, 7, serial)
					table.setText(row, 8, number)
					table.setText(row, 9, nazn)
					table.setText(row, 11, mkb)
					table.setText(row, 12, name)
					table.setText(row, 14, vk)
					table.setText(row, 10, ddt)
					table.setText(row, 19, prim)#
					table.setText(row, 15, pri)
					table.setText(row, 16, prin)
					table.setText(row, 17, dlit)
					table.setText(row, 18, signa)
					table.mergeCells(0, col, 2, 1)
				else:
					table.setText(row, 0, fio)
					table.setText(row, 1, happy)
					table.setText(row, 2, pol)
					table.setText(row, 3, pasSerial)
					table.setText(row, 4, pasNumber)
					table.setText(row, 5, snil)
					table.setText(row, 6, lgot)
					table.setText(row, 7, serial)
					table.setText(row, 8, number)
					table.setText(row, 9, nazn)
					table.setText(row, 11, mkb)
					table.setText(row, 12, name)
					table.setText(row, 14, vk)
					table.setText(row, 10, ddt)
					table.setText(row, 15, pri)
					table.setText(row, 16, prin)
					table.setText(row, 17, dlit)
					table.setText(row, 18, signa)

				prevnum = fioP
				ttt =   (fioP)
				tt =   (fio)
			#totalpri, prin, dlit, signa
			drawTotal(table,  totalBynum, u'Количество пациентов %s ' %  cnt);
			drawTotal(table,  totalBynum, u'Количество рецептов %s ' %  coun);
			drawTotal(table,  totalBynum, u'ИТОГО пациентов %s ' %  allcnt);
			drawTotal(table,  totalBynum, u'ИТОГО рецептов %s ' %  allcoun);
			return doc
        else:
			def processQuery(query):
				while query.next():
					record = query.record()
					fioP= forceString(record.value('fioP'))#name
					fio= forceString(record.value('fio'))#name
					happy = forceString(record.value('happy'))#+
					pol = forceString(record.value('pol'))#+
					pasSerial = forceString(record.value('pasSerial'))#+
					pasNumber = forceString(record.value('pasNumber'))#+
					snil = forceString(record.value('snil'))#+
					lgot = forceString(record.value('lgot'))#+
					ddt = forceString(record.value('ddt'))#+
					serial = forceString(record.value('serial'))#+
					number = forceString(record.value('number'))#+
					nazn = forceString(record.value('nazn'))#+
					mkb = forceString(record.value('mkb'))#+
					name = forceString(record.value('name'))#+
					vk = forceString(record.value('vk'))#+
					prim = forceString(record.value('prim'))#+
					
					key = (fioP, fio, happy, pol, pasSerial, pasNumber, snil, lgot, serial, number,nazn, ddt, mkb, name, vk, prim)
					reportLine = reportData.setdefault(key)
					
				 #   reportLine[0] += kd
				 #   reportLine[1] += sum
				  #  reportLine[2] += cnt
			query = self.selectData(params)
			processQuery(query)
			
			# now text
			doc = QtGui.QTextDocument()
			cursor = QtGui.QTextCursor(doc)

			cursor.setCharFormat(CReportBase.ReportTitle)
			cursor.insertText(self.title())
			cursor.insertBlock()
			self.dumpParams(cursor, params)
			cursor.setCharFormat(CReportBase.ReportBody)
			cursor.insertBlock()
			if a==4:
				tableColumns = [
				('10%',  [ u'Фамилия Имя Отчество'], CReportBase.AlignLeft),
				('5%',  [ u'Дата рождения'], CReportBase.AlignLeft),
				('10%',  [ u'Серия, номер полиса'], CReportBase.AlignLeft),
				('5%',  [ u'УДЛ',u'серия'], CReportBase.AlignLeft),
				('5%',  [ u'',u'номер'], CReportBase.AlignLeft),
				('5%',  [ u'Снилс'], CReportBase.AlignRight),
				('5%',  [ u'Код льготы'], CReportBase.AlignRight),
				('5%',  [ u'Рецепт', u'Серия'], CReportBase.AlignRight),
				('9%',  [ u'', u'Номер'], CReportBase.AlignRight),
				('9%',  [ u'', u'Дата выписки'], CReportBase.AlignRight),
				('5%',  [ u'D.t.d'], CReportBase.AlignRight),
				('5%',  [ u'Код МКБ-Х'], CReportBase.AlignRight),
				('20%',  [ u'Лекарственное средство'], CReportBase.AlignRight),
				('5%',  [ u'Сумма'], CReportBase.AlignRight),
				('5%',  [ u'По решению врачебной комиссии'], CReportBase.AlignRight),
				('5%',  [ u'Примечание'], CReportBase.AlignRight),
				]
			else:
				tableColumns = [
				('12%',  [ u'Фамилия Имя Отчество'], CReportBase.AlignLeft),
				('5%',  [ u'Дата рождения'], CReportBase.AlignLeft),
				('10%',  [ u'Серия, номер полиса'], CReportBase.AlignLeft),
				('5%',  [ u'УДЛ',u'серия'], CReportBase.AlignLeft),
				('5%',  [ u'',u'номер'], CReportBase.AlignLeft),
				('5%',  [ u'Снилс'], CReportBase.AlignRight),
				('5%',  [ u'Код льготы'], CReportBase.AlignRight),
				('5%',  [ u'Рецепт', u'Серия'], CReportBase.AlignRight),
				('9%',  [ u'', u'Номер'], CReportBase.AlignRight),
				('9%',  [ u'', u'Дата выписки'], CReportBase.AlignRight),
				('5%',  [ u'D.t.d'], CReportBase.AlignRight),
				('5%',  [ u'Код МКБ-Х'], CReportBase.AlignRight),
				('20%',  [ u'Лекарственное средство'], CReportBase.AlignRight),
				('5%',  [ u'Сумма'], CReportBase.AlignRight),
				('5%',  [ u'По решению врачебной комиссии'], CReportBase.AlignRight),
				]
			

			table = createTable(cursor, tableColumns)
			table.mergeCells(0, 3, 1, 2)
			table.mergeCells(0, 7, 1, 3)
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
				table.mergeCells(row, 0, 1, reportRowSize)
			for key in keys:
				#key = (fioP, fio, happy, pol, pasSerial, pasNumber, snil, lgot, serial, number,nazn, ddt, mkb, name, vk, prim)
				
				fioP= key[0]
				ddt = key[11]
				prim = key[15]
				vk = key[14]
				name = key[13]
				mkb = key[12]
				nazn = key[10]
				number = key[9]
				serial = key[8]
				lgot = key[7]
				snil = key[6]
				pasNumber = key[5]
				pasSerial = key[4]
				pol = key[3]
				happy = key[2]
				fio = key[1]
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
					table.mergeCells(row, 0, 1, reportRowSize)
					
				row = table.addRow()          
				table.setText(row, 0, fio)
				table.setText(row, 1, happy)
				table.setText(row, 2, pol)
				table.setText(row, 3, pasSerial)
				table.setText(row, 4, pasNumber)
				table.setText(row, 5, snil)
				table.setText(row, 6, lgot)
				table.setText(row, 7, serial)
				table.setText(row, 8, number)
				table.setText(row, 9, nazn)
				table.setText(row, 11, mkb)
				table.setText(row, 12, name)
				table.setText(row, 14, vk)
				table.setText(row, 10, ddt)
				if a==4:
					table.setText(row, 15, prim)
					table.mergeCells(0, col, 2, 1)
					
				
				prevnum = fioP
				ttt =   (fioP)
				tt =   (fio)
			#total
			drawTotal(table,  totalBynum, u'Количество пациентов %s ' %  cnt);
			drawTotal(table,  totalBynum, u'Количество рецептов %s ' %  coun);
			drawTotal(table,  totalBynum, u'ИТОГО пациентов %s ' %  allcnt);
			drawTotal(table,  totalBynum, u'ИТОГО рецептов %s ' %  allcoun);
			return doc
