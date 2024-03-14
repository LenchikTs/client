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
from library.Utils      import *
from library.database   import *
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable
from Orgs.Utils         import *
from Ui_CountByOms import Ui_CountByOmsSetupDialog

def selectData(org, attachType):
    stmt = '''
        select sum(q.cnt) as cnt,
          sum(case when age>=0 and age<=1 then q.male else 0 end) as mgrp1,
          sum(case when age>=2 and age<=3 then q.male else 0 end) as mgrp2,
          sum(case when age>=4 and age<=5 then q.male else 0 end) as mgrp3,
          sum(case when age>=6 and age<=8 then q.male else 0 end) as mgrp4,
          sum(case when age>=9 and age<=11 then q.male else 0 end) as mgrp5,
          sum(case when age>=12 and age<=14 then q.male else 0 end) as mgrp6,
          sum(case when age>=15 and age<=17 then q.male else 0 end) as mgrp7,
          sum(case when age>=18 and age<=39 then q.male else 0 end) as mgrp8,
          sum(case when age>=40 and age<=59 then q.male else 0 end) as mgrp9,
          sum(case when age>=60 then q.male else 0 end) as mgrp10,
          sum(case when age>=0 and age<=1 then q.female else 0 end) as fgrp1,
          sum(case when age>=2 and age<=3 then q.female else 0 end) as fgrp2,
          sum(case when age>=4 and age<=5 then q.female else 0 end) as fgrp3,
          sum(case when age>=6 and age<=8 then q.female else 0 end) as fgrp4,
          sum(case when age>=9 and age<=11 then q.female else 0 end) as fgrp5,
          sum(case when age>=12 and age<=14 then q.female else 0 end) as fgrp6,
          sum(case when age>=15 and age<=17 then q.female else 0 end) as fgrp7,
          sum(case when age>=18 and age<=39 then q.female else 0 end) as fgrp8,
          sum(case when age>=40 and age<=54 then q.female else 0 end) as fgrp9,
          sum(case when age>=55 then q.female else 0 end) as fgrp10,
          sum(q.male),
          sum(q.female)
         from (
            select count(distinct Client.id) as cnt,  age(Client.birthDate,CURRENT_DATE) as age, 
                count( distinct case when Client.sex = 1 then Client.id else null end) as male,
                count( distinct case when Client.sex = 2 then Client.id else null end) as female
            from ClientAttach
                left join Client on Client.id = ClientAttach.client_id
                left join ClientPolicy on ClientPolicy.client_id = Client.id
                left join Organisation on Organisation.id = ClientPolicy.insurer_id
            where 
                ClientPolicy.deleted = false and
                Client.deleted = false and
                Organisation.deleted = false and
                Client.deathDate is null and 
                ClientAttach.deleted = false and
                %s
                group by Client.id, Client.birthDate
                
            ) q
'''
    db = QtGui.qApp.db
    tableClientAttach = db.table('ClientAttach')
    tableOrganisation = db.table('Organisation')
    cond = []
    cond.append(tableOrganisation['id'].eq(org))
    if attachType:
        cond.append(tableClientAttach['attachType_id'].eq(attachType))
    return db.query(stmt % db.joinAnd(cond))

class CCountByOms(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setPayPeriodVisible(False)
        
        self.setTitle(u'''
Сведения о численности лиц, застрахованных в 
%s, 
выбравших Организацию для оказания амбулаторной медицинской помощи
        ''')
        
    def getSetupDialog(self, parent):
        result =  CCountByOmsSetupDialog(parent)
        result.setTitle(u'Параметры отчета')
        return result
    
    
    def dumpParams(self, cursor, params):
        description = []
        db = QtGui.qApp.db
        attachTypeId = params.get('attachType', None)
        if attachTypeId:
               description.append(u'Тип прикрепления: ' + forceString(db.translate('rbAttachType', 'id', attachTypeId, 'name')))
        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        
    def build(self, params):
        orgId = params.get('org',  None)
        if not orgId:
            return None
        db = QtGui.qApp.db
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.setBlockFormat(CReportBase.AlignCenter)
        updatedTitle = self.title() % forceString(db.translate('Organisation', 'id', orgId, 'fullName'))
        self.setTitle(updatedTitle)
        cursor.insertText(updatedTitle)
        
        cursor.insertText(u'на %s г.' % params.get('date', QDate.currentDate()).toString('dd.MM.yyyy'))
        cursor.insertBlock()
        cursor.setBlockFormat(QtGui.QTextBlockFormat())
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        query = selectData(params.get('org'), params.get('attachType'))
        reportdata = {}
        while query.next():
            record = query.record()
            reportData = { 'cnt'    :forceInt(record.value('cnt')), 
                                 'mgrp1' :forceInt(record.value('mgrp1')), 
                                 'mgrp2' :forceInt(record.value('mgrp2')), 
                                 'mgrp3' :forceInt(record.value('mgrp3')), 
                                 'mgrp4' :forceInt(record.value('mgrp4')), 
                                 'mgrp5' :forceInt(record.value('mgrp5')), 
                                 'mgrp6' :forceInt(record.value('mgrp6')), 
                                 'mgrp7' :forceInt(record.value('mgrp7')), 
                                 'mgrp8' :forceInt(record.value('mgrp8')), 
                                 'mgrp9' :forceInt(record.value('mgrp9')), 
                                 'mgrp10' :forceInt(record.value('mgrp10')), 
                                 'fgrp1' :forceInt(record.value('fgrp1')), 
                                 'fgrp2' :forceInt(record.value('fgrp2')), 
                                 'fgrp3' :forceInt(record.value('fgrp3')), 
                                 'fgrp4' :forceInt(record.value('fgrp4')), 
                                 'fgrp5' :forceInt(record.value('fgrp5')), 
                                 'fgrp6' :forceInt(record.value('fgrp6')), 
                                 'fgrp7' :forceInt(record.value('fgrp7')), 
                                 'fgrp8' :forceInt(record.value('fgrp8')), 
                                 'fgrp9' :forceInt(record.value('fgrp9')), 
                                 'fgrp10' :forceInt(record.value('fgrp10')), 
            }
        tableColumns = [
        ('10%',  [ u'№'], CReportBase.AlignLeft),
        ('40%',  [ u'Число застрахованных лиц'], CReportBase.AlignLeft),
        ('10%',  [ u'В том числе по группам застрахованных лиц', u'дети', u'0-1 лет', u'Муж.'], CReportBase.AlignCenter),
        ('10%',  [ u'', u'', u'', u'Жен.'], CReportBase.AlignCenter),
        ('10%',  [ u'', u'', u'2-3 лет', u'Муж.'], CReportBase.AlignCenter),
        ('10%',  [ u'', u'', u'', u'Жен.'], CReportBase.AlignCenter),
        ('10%',  [ u'', u'', u'4-5 лет', u'Муж.'], CReportBase.AlignCenter),
        ('10%',  [ u'', u'', u'', u'Жен.'], CReportBase.AlignCenter),
        ('10%',  [ u'', u'', u'6-8 лет', u'Муж.'], CReportBase.AlignCenter),
        ('10%',  [ u'', u'', u'', u'Жен.'], CReportBase.AlignCenter),
        ('10%',  [ u'', u'', u'9-11 лет', u'Муж.'], CReportBase.AlignCenter),
        ('10%',  [ u'', u'', u'', u'Жен.'], CReportBase.AlignCenter),
        ('10%',  [ u'', u'', u'12-14 лет', u'Муж.'], CReportBase.AlignCenter),
        ('10%',  [ u'', u'', u'', u'Жен.'], CReportBase.AlignCenter),
        ('10%',  [ u'', u'', u'15-17 лет', u'Муж.'], CReportBase.AlignCenter),
        ('10%',  [ u'', u'', u'', u'Жен.'], CReportBase.AlignCenter),
        #####
        ('10%',  [ u'', u'трудоспособный возраст', u'18-39 лет', u'Муж.'], CReportBase.AlignCenter),
        ('10%',  [ u'', u'', u'', u'Жен.'], CReportBase.AlignCenter),
        ('10%',  [ u'', u'', u'40-59 лет', u'Муж.'], CReportBase.AlignCenter),
        ('10%',  [ u'', u'', u'40-54 лет', u'Жен.'], CReportBase.AlignCenter),
        #####
        ('10%',  [ u'', u'пенсионеры', u'60 лет и старше', u'Муж.'], CReportBase.AlignCenter),
        ('10%',  [ u'', u'', u'55 лет и старше', u'Жен.'], CReportBase.AlignCenter),
        ]
        
        table = createTable(cursor, tableColumns)
        #row,col,mergeRow,mergeCol
        table.mergeCells(0, 0, 4, 1)
        table.mergeCells(0, 1, 4, 1)
        table.mergeCells(0, 2, 1, 20)
        table.mergeCells(1, 2, 1, 14)
        table.mergeCells(1, 16, 1, 4)
        table.mergeCells(1, 20, 1, 2)
        table.mergeCells(2, 2, 1, 2)
        table.mergeCells(2, 4, 1, 2)
        table.mergeCells(2, 6, 1, 2)
        table.mergeCells(2, 8, 1, 2)
        table.mergeCells(2, 10, 1, 2)
        table.mergeCells(2, 12, 1, 2)
        table.mergeCells(2, 14, 1, 2)
        table.mergeCells(2, 16, 1, 2)
        row = table.addRow()
        table.setText(row, 1, reportData['cnt'])
        col = 2
        for i in xrange(10):
            table.setText(row, col , reportData['mgrp%s' % (i+1)])
            table.setText(row, col+1, reportData['fgrp%s' % (i+1)])
            col+=2
        return doc
class CCountByOmsSetupDialog(QtGui.QDialog, Ui_CountByOmsSetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        #self.cmbOrganisation.setTable('Organisation', True, specialValues=((-1, u'ОМС', u'ОМС'), ))
        self.cmbAttachType.setTable('rbAttachType', True,  filter='finance_id = 2')

    def setPayPeriodVisible(self, value):
        pass


    def setWorkTypeVisible(self, value):
        pass


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setEventTypeVisible(self, visible=True):
        pass


    def setParams(self, params):
        self.cmbOrganisation.setValue(params.get('org', None))
        self.cmbAttachType.setValue(params.get('attachType', None))
        pass

    def params(self):
        result = {}
        result['org'] = self.cmbOrganisation.value()
        result['attachType'] = self.cmbAttachType.value()
        #result['policyType'] = self.cmbPolicyType.value()
        #result['policyKind'] = self.cmbPolicyKind.value()
        return result
        
    def accept(self):
        if not self.params().get('org', None):
            QtGui.QMessageBox.warning( self,
                                       u'Внимание!',
                                       u'Не выбрана организация',
                                       QtGui.QMessageBox.Close)
            QtGui.QDialog.ignore(self)
        else:
            QtGui.QDialog.accept(self)
               
