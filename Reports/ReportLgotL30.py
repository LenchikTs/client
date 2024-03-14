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

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from library.Utils      import *
from library.database   import *
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Orgs.Utils         import *
from Ui_ReportLgotL30 import Ui_ReportLgotL30SetupDialog

def selectData(dateN,  dateE):
    stmt = u'''
select 
	groups.id as id, groups.title,
	count(distinct client) as ClentTotal, 
	count(distinct recipe) as RecipeTotal,
   
    count(distinct case when age < 18 then client else null end) as Clent18, 
	count(distinct case when age < 18 then recipe else null end) as Recipe18,
    
    count(distinct case when age < 3 then client else null end) as Clent3, 
	count(distinct case when age < 3 then recipe else null end) as Recipe3,
    
    count(distinct case when (age > 60 and sex = 1) or (age > 55 and sex = 2) then client else null end) as ClentPension, 
	count(distinct case when (age > 60 and sex = 1) or (age > 55 and sex = 2) then recipe else null end) as RecipePension,
    
    count(distinct case when isInvalid then client else null end) as ClentInvalid, 
	count(distinct case when isInvalid then recipe else null end) as RecipeInvalid,
    
    count(distinct case when isDiabetis then client else null end) as ClentDiabetis, 
	count(distinct case when isDiabetis then recipe else null end) as RecipeDiabetis,
    
    count(distinct case when isAstma then client else null end) as ClentAstma, 
	count(distinct case when isAstma then recipe else null end) as RecipeAstma,
    
    count(distinct case when isOnko then client else null end) as ClentOnko, 
	count(distinct case when isOnko then recipe else null end) as RecipeOnko
    
from (
	select 1 as id,'ВЗН' as title
	union all
	select 2, 'Федеральное обеспечение'
	union all
	select 3, 'Региональное обеспечение'
		   
) groups 
left join
(
	select 
		c.id as client,
		a.id as recipe,
		age(c.birthDate,now()) as age,
		c.sex as sex,
		max(case when soctype.socCode in (8,9,10,11,12,20,81,82,83,84,85) then 1 else 0 end) as isInvalid,
		max(case when d.MKB between 'E10.0' and 'E14.9' then 1 else 0 end) as isDiabetis,
		max(case when d.MKB between 'J45.0' and 'J46.' then 1 else 0 end) as isAstma,
		max(case when d.MKB between 'C00' and 'C96.' or d.MKB = 'R52.9' then 1 else 0 end) as isOnko,
		(case when fin.value = 'Федеральный' then 1 else 0 end) as isFederal,
		max(case when d.MKB in (
			'C92.1',' C88.0',' C90.0',' C82',' C83.0',' C83.1',' C83.3',' C83.4',
			'C83.8',' C83.9',' C85',' C91.1',' E84',' D66',' D67',' D68.0',
			'G35',' E23.0',' E75.5',' Z94.0',' Z94.1',' Z94.4',' Z94.8') then 1 else 0 end) as isVZN
	from Client c
	left join Event e on e.client_id = c.id
	inner join ClientSocStatus soc on soc.id = (
						SELECT MAX(CSS.id)
						FROM ClientSocStatus CSS
						WHERE CSS.client_id = c.id AND
								  CSS.deleted = 0 AND
								  (CSS.begDate IS NULL OR CSS.begDate >= e.setDate) AND
								  (CSS.endDate IS NULL OR CSS.endDate <= e.execDate) AND
								  CSS.socStatusClass_id in (
										SELECT S.id
										FROM rbSocStatusClass S
										WHERE S.group_id= 1
								  )
						LIMIT 1
					)
	left join Action a on a.event_id = e.id 
	left join ActionType at on at.id = a.actionType_id and at.context = 'recipe'
	left join rbSocStatusType soctype on soctype.id = soc.socStatusType_id
	left join Diagnosis d on d.id = getEventDiagnosis(e.id) 
	left join ActionProperty ap_fin on ap_fin.action_id = a.id and ap_fin.type_id in (select id from ActionPropertyType where name = 'Источник финансирования')
	left join ActionProperty_String fin on fin.id = ap_fin.id
	where 
		a.deleted = false and
		c.deleted = false and
		d.deleted = false and
		ap_fin.deleted = false and
		soc.deleted = false and %s
        
    group by c.id, a.id
        )
q on (q.isVZN and groups.id = 1) or (q.isFederal and groups.id = 2) or (q.isFederal = 0 and groups.id = 3)
group by groups.id order by groups.id asc
'''
    db = QtGui.qApp.db
    cond = 'a.begDate between %s and %s' % (db.formatDate(dateN), db.formatDate(dateE))
    stmt = stmt % cond
    return db.query(stmt) 

class CReportLgotL30(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Информация о лекарственных средствах, отпущенных льготным категориям граждан')
        
    def getSetupDialog(self, parent):
        result =  CReportLgotL30SetupDialog(parent)
        result.setTitle(u'Параметры отчета')
        return result
    
    
    def dumpParams(self, cursor, params):
        description = []
        dateN =  params.get('dateN', QDate.currentDate()).toString('dd.MM.yyyy')
        dateE =  params.get('dateE', QDate.currentDate()).toString('dd.MM.yyyy')
        description.append(u'за период: %s - %s' % (dateN,  dateE))
        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        
    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.setBlockFormat(CReportBase.AlignCenter)
        cursor.insertText(self.title() )
        cursor.setBlockFormat(QtGui.QTextBlockFormat())
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        query = selectData(params.get('dateN'), params.get('dateE'))
        reportgroups = {}
        while query.next():
            record = query.record()
            groupId = forceInt(record.value('id'))
            reportData = { 
                'row1' : {
                              '0': str(groupId) + '.1',  
                              '1': u'Численность категории льготополучателей (человек)', 
                              '2': forceInt(record.value('ClentTotal')), 
                              '3': forceInt(record.value('Clent18')), 
                              '4': forceInt(record.value('Clent3')), 
                              '5': forceInt(record.value('ClentPension')), 
                              '6': forceInt(record.value('ClentInvalid')), 
                              '7':'', 
                              '8': forceInt(record.value('ClentDiabetis')), 
                              '9': forceInt(record.value('ClentAstma')), 
                              '10': forceInt(record.value('ClentOnko')), 
                }, 
                'row2' : {
                              '0': str(groupId) + '.2',  
                              '1': u'Выписано рецептов (шт.)', 
                              '2': forceInt(record.value('RecipeTotal')), 
                              '3': forceInt(record.value('Recipe18')), 
                              '4': forceInt(record.value('Recipe3')), 
                              '5': forceInt(record.value('RecipePension')), 
                              '6': forceInt(record.value('RecipeInvalid')), 
                              '7':'', 
                              '8': forceInt(record.value('RecipeDiabetis')), 
                              '9': forceInt(record.value('RecipeAstma')), 
                              '10': forceInt(record.value('RecipeOnko')), 
                }
            }
            reportgroups[groupId] =  reportData         
           
        tableColumns = [
        ('5%',  [ u'№ п/п'],CReportBase.AlignCenter),
        ('15%',  [ u'Наименование'],CReportBase.AlignCenter),
        ('8%',  [ u'ВСЕГО,\r\n в т.ч.:'],CReportBase.AlignCenter),
        ('9%',  [ u'детское население (0-18 лет)'],CReportBase.AlignCenter),
        ('9%',  [ u'дети до 3-х лет'],CReportBase.AlignCenter),
        ('9%',  [ u'граждане старше трудоспособного возраста (старше 55 лет - женщины, 60 - мужчины)'],CReportBase.AlignCenter),
        ('9%',  [ u'инвалиды и участники ВОВ'],CReportBase.AlignCenter),
        ('9%',  [ u'граждане (в т.ч. старше трудоспособного возраста и с ограниченной мобильностью), ' + 
                       u'лекарственное обеспечение которых осуществляется в рамках адресной доставки ЛП'],CReportBase.AlignCenter),
        ('9%',  [ u'Сахарный диабет (диагноз с E10.0 по E14.9)'],CReportBase.AlignCenter),
        ('9%',  [ u'Бронхиальная астма (диагноз с J45.0 по J46.)'],CReportBase.AlignCenter),
        ('9%',  [ u'Онкологические заболевания(диагноз с C00 по C96, и R52.9)'],CReportBase.AlignCenter),
        ]
        
        table = createTable(cursor, tableColumns)
        
        fmtc =QtGui.QTextBlockFormat()
        fmtc.setAlignment(QtCore.Qt.AlignCenter)
        fmtl=QtGui.QTextBlockFormat()
        fmtl.setAlignment(QtCore.Qt.AlignLeft)
        
        for grpId,  grpname in enumerate([u'ВЗН',  u'Федеральное обеспечение',  u'Региональное обеспечение'],  start = 1):
            row = table.addRow()
            table.setText(row, 0, grpId)
            table.setText(row, 1, grpname,  CReportBase.TableHeader)
            table.mergeCells(row, 1, 1, 10)
            row1 = table.addRow()
            row2 = table.addRow()
            for col in xrange(11):
                frmt = fmtl if col == 1 else fmtc
                table.setText(row1, col,reportgroups[grpId]['row1'][str(col)],  blockFormat = frmt)
                table.setText(row2, col,reportgroups[grpId]['row2'][str(col)],  blockFormat = frmt)
        return doc
        
class CReportLgotL30SetupDialog(QtGui.QDialog, Ui_ReportLgotL30SetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

    def setPayPeriodVisible(self, value):
        pass


    def setWorkTypeVisible(self, value):
        pass


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setEventTypeVisible(self, visible=True):
        pass


    def setParams(self, params):
        self.edtBegDate.setDate(params.get('dateN', QDate.currentDate()))
        self.edtEndDate.setDate(params.get('dateE', QDate.currentDate()))
        pass

    def params(self):
        result = {}
        result['dateN'] = self.edtBegDate.date()
        result['dateE'] = self.edtEndDate.date()
        return result
        
#    def accept(self):
#        if not self.params().get('org', None):
#            QtGui.QMessageBox.warning( self,
#                                       u'Внимание!',
#                                       u'Не выбрана организация',
#                                       QtGui.QMessageBox.Close)
#            QtGui.QDialog.ignore(self)
#        else:
#            QtGui.QDialog.accept(self)
               
