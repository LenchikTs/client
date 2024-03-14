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

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from library.Utils      import *
from library.database   import *
from Orgs.Utils         import *
from Registry.Utils     import *
from Reports.Report     import CReport
from Reports.ReportBase import *
from ReportView import CReportViewDialog
from Events.ContractTariffCache import CContractTariffCache
from Events.MapActionTypeToServiceIdList import CMapActionTypeIdToServiceIdList

from Ui_ReportCostSetup import Ui_ReportCostSetupDialog


def selectData2(params):
    db = QtGui.qApp.db
    stmt="""
select
t.lpuname,
t.isMain,
t.code,
t.spec,
t.person,
count(t.event_id) as kol_all,
sum(case when t.regionalCode in ('21','22','31','32','60','80','01','02','111','112','222','201','202','232','211','241','242','252','261','262') then 1 else 0 end) as pol_kol,
sum(case when t.regionalCode in ('11','12', '401', '402') then 1 else 0 end) as stac_kol,
sum(case when t.regionalCode in ('41','42','43','51','52','71','72','90') then 1 else 0 end) as staczam_kol
 from ( select 
OrgStructure.name as lpuname,
OrgStructure.parent_id is null as isMain,
OrgStructure.infisCode as code,
s.OKSOName as spec,
concat(p.lastName, ' ', p.firstName, ' ', p.patrName, ' (', p.code, ')') as person,
l.event_id
, mt.regionalCode
from OrgStructure
left join OrgStructure o1 on o1.parent_id = OrgStructure.id
left join OrgStructure o2 on o2.parent_id = o1.id
left join OrgStructure o3 on o3.parent_id = o2.id
left join Person p on p.orgStructure_id in (OrgStructure.id, o1.id, o2.id, o3.id)
left join rbSpeciality s on s.id = p.speciality_id
left join soc_logRepCost l on l.person_id = p.id
left join Event e on e.id = l.event_id
left join EventType et on et.id = e.eventType_id
left join rbMedicalAidType mt on mt.id = et.medicalAidType_id
where exists (select id from Organisation org where org.infisCode = OrgStructure.infisCode) and l.person_id is not null and %s
group by OrgStructure.infisCode, OrgStructure.name, p.id, l.event_id) as t
group by t.code, t.lpuname, t.person
order by t.code, t.lpuname, t.person
""" % (getCond(params))
    return db.query(stmt)

def getCond(params):
    db = QtGui.qApp.db   
    cond = [] 
    cond.append("1=1")
    if params.get('vidPom',  None):
        regionalCode = forceRef(db .translate('rbMedicalAidType', 'id', params['vidPom'],'regionalCode'))
        cond.append("mt.regionalCode = '%s'" % regionalCode)
    if params.get('begDate', None):
        cond.append("l.date >= '%s'" % params['begDate'].toString('yyyy-MM-dd'))
    if params.get('endDate', None):
        cond.append("l.date < '%s'" % params['endDate'].addDays(1).toString('yyyy-MM-dd'))
    if params.get('personId', None):
        cond.append("p.id = %s" % params['personId'])

    if params.get('orgStructureId', None):
        OrgStructure = db.table("OrgStructure")
        cond.append(OrgStructure['id'].inlist(getOrgStructureDescendants(params['orgStructureId'])))
    else:
        cond.append("p.org_id = %s or p.org_id is null" % QtGui.qApp.currentOrgId())
    if params.get('specialityId', None):
        cond.append('s.id = %s' % params['specialityId'])
    return db.joinAnd(cond)
class CReportCost(CReport, CMapActionTypeIdToServiceIdList):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        CMapActionTypeIdToServiceIdList.__init__(self)
        self.parent = parent
        self.setTitle(u'Информация о количестве справок о стоимости оказанной медицинской помощи, выданных пациентам в медицинских организациях на отчетную дату %s'
            % forceString(QtCore.QDate.currentDate()))
        self.contractTariffCache = CContractTariffCache()

    def reportLoop(self):
        params = self.getDefaultParams()
        while True:
            setupDialog = self.getSetupDialog(self.parent)
            setupDialog.setParams(params)
            if not setupDialog.exec_():
                break
            params = setupDialog.params()
            self.saveDefaultParams(params)
            try:
                QtGui.qApp.setOverrideCursor(QtGui.QCursor(Qt.WaitCursor))
                reportResult = self.build(params)
            finally:
                QtGui.qApp.restoreOverrideCursor()
            viewDialog = CReportViewDialog(self.parent)
            if self.viewerGeometry:
                viewDialog.restoreGeometry(self.viewerGeometry)
            viewDialog.setWindowTitle(self.title())
            viewDialog.setRepeatButtonVisible()
            viewDialog.setText(reportResult)
            done = not viewDialog.exec_()
            self.viewerGeometry = viewDialog.saveGeometry()
            if done:
                break


    def getSetupDialog(self, parent):
        result = CReportCostDialog(parent, self)
        result.setTitle(self.title())
        return result

    def build(self, params):
        query = selectData2(params)
        reportLines = self.getStructInfo(query)

        doc = QtGui.QTextDocument()
        boldChars = QtGui.QTextCharFormat()
        boldChars.setFontWeight(QtGui.QFont.Bold)
        if query is None:
            return doc
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock(CReportBase.AlignCenter)
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        tableColumns = [
                        ('30%', [u'Наименование учреждения'], CReportBase.AlignCenter),
                        ('10%', [u'Код ЛПУ в системе ОМС'], CReportBase.AlignCenter), 
                        ('12%', [u'Всего'], CReportBase.AlignCenter), 
                        ('8%', [u'Количество выданных справок в амбулаторно-поликлиническом звене'], CReportBase.AlignCenter), 
                        ('8%', [u''], CReportBase.AlignCenter), 
                        ('8%', [u'Количество выданных справок в стационарном звене'], CReportBase.AlignCenter), 
                        ('8%', [u''], CReportBase.AlignCenter), 
                        ('8%', [u'Количество выданных справок в стационаро-замещающем звене'], CReportBase.AlignCenter), 
                        ('8%', [u''], CReportBase.AlignCenter)
                       ]
        #mergeCells ( int row, int column, int numRows, int numCols )
        table = createTable(cursor, tableColumns)
        row = table.addRow();
        table.setText(row, 3 , u'через АРМ', charFormat=boldChars)
        table.setText(row, 4 , u'вручную', charFormat=boldChars)
        table.setText(row, 5 , u'через АРМ', charFormat=boldChars)
        table.setText(row, 6 , u'вручную', charFormat=boldChars)
        table.setText(row, 7 , u'через АРМ', charFormat=boldChars)
        table.setText(row, 8 , u'вручную', charFormat=boldChars)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 2, 1)
        table.mergeCells(0, 3, 1, 2)
        table.mergeCells(0, 5, 1, 2)
        table.mergeCells(0, 7, 1, 2)
        #[0] = lastlpu, [1] - lastlpurow, [2] - total by lpu
        lpu_data=[0, 0, [0, 0, 0, 0]]
        #[0] = lastspec, [1] - lastspecrow, [2] - total by spec
        spec_data=[0, 0, [0, 0, 0, 0]]
        total = [0, 0, 0, 0]
        
        for rl in reportLines:
           lpuname,  infisCode,  specName,  person,  cnt,  stacCnt,  zamCnt,  polCnt, isMain = rl
           if lpu_data[0]!=lpuname:
               if lpu_data[1]!=0:
                   for i in range(0, 4):
                    cols = [2, 3, 5, 7]
                    table.setText(lpu_data[1], cols[i] , lpu_data[2][i],  charFormat=boldChars)
               lpu_data[2] = [0, 0, 0, 0]
               row = table.addRow();
               lpu_data[1] = row
               table.setText(row, 0 , lpuname,  charFormat=boldChars, blockFormat=CReportBase.AlignLeft)
               table.setText(row, 1 , infisCode)
               table.setText(row, 4 , '-')
               table.setText(row, 6 , '-')
               table.setText(row, 8 , '-')
           if spec_data[0]!=specName or lpu_data[0]!=lpuname:
               if spec_data[1]!=0:
                   for i in range(0, 4):
                    cols = [2, 3, 5, 7]
                    table.setText(spec_data[1], cols[i] , spec_data[2][i],  charFormat=boldChars)
               spec_data[2] = [0, 0, 0, 0]
               row = table.addRow();
               spec_data[1] = row
               table.setText(row, 0 , specName,  charFormat=boldChars, blockFormat=CReportBase.AlignRight)
               table.setText(row, 4 , '-')
               table.setText(row, 6 , '-')
               table.setText(row, 8 , '-')
           row = table.addRow();
           table.setText(row, 0 , person,  blockFormat=CReportBase.AlignRight)

           table.setText(row, 2 , cnt)
           table.setText(row, 3 , polCnt)
           table.setText(row, 4 , '-')
           table.setText(row, 5 , stacCnt)
           table.setText(row, 6 , '-')
           table.setText(row, 7 , zamCnt)
           table.setText(row, 8 , '-')
           lpu_data[0] =lpuname
           lpu_data[2][0]+=cnt
           lpu_data[2][1]+=polCnt
           lpu_data[2][2]+=stacCnt
           lpu_data[2][3]+=zamCnt
           spec_data[0] = specName
           spec_data[2][0]+=cnt
           spec_data[2][1]+=polCnt
           spec_data[2][2]+=stacCnt
           spec_data[2][3]+=zamCnt
           if not isMain:
               total[0]+=cnt
               total[1]+=polCnt
               total[2]+=stacCnt
               total[3]+=zamCnt
        
        for i in range(0, 4):
            cols = [2, 3, 5, 7]
            table.setText(lpu_data[1], cols[i] , lpu_data[2][i],  charFormat=boldChars)
            table.setText(spec_data[1], cols[i] , spec_data[2][i],  charFormat=boldChars)
        row = table.addRow();
        table.setText(row, 0 , u'Итого',  charFormat=boldChars,  blockFormat=CReportBase.AlignRight)
        table.setText(row, 2 , total[0],  charFormat=boldChars)
        table.setText(row, 3 , total[1],  charFormat=boldChars)
        table.setText(row, 4 , '-',  charFormat=boldChars)
        table.setText(row, 5 , total[2],  charFormat=boldChars)
        table.setText(row, 6 , '-',  charFormat=boldChars)
        table.setText(row, 7 , total[3],  charFormat=boldChars)
        table.setText(row, 8 , '-',  charFormat=boldChars)
        
        return doc


    def getStructInfo(self,  query):
        rows = []
        while query.next():
            record = query.record()
            lpuname = forceString(record.value('lpuname'))
            infisCode = forceString(record.value('code'))
            specName = forceString(record.value('spec'))
            person = forceString(record.value('person'))
            cnt = forceInt(record.value('kol_all'))
            stacCnt = forceInt(record.value('stac_kol'))
            zamCnt = forceInt(record.value('staczam_kol'))
            polCnt = forceInt(record.value('pol_kol'))
            isMain = forceBool(record.value('isMain'))
            row = [lpuname,  infisCode,  specName,  person,  cnt,  stacCnt,  zamCnt,  polCnt,  isMain]
            rows.append(row)
        return rows;




class CReportCostDialog(QtGui.QDialog, Ui_ReportCostSetupDialog):
    def __init__(self, parent, report):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self._report = report
        self.connect(self.buttonBox, SIGNAL('accepted()'), self.accept)
        self.cmbSpeciality.setTable('rbSpeciality', True)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())
        self.cmbVidPom.setTable('rbMedicalAidType',  True,  '',  'id');



    def accept(self):
        QtGui.QDialog.accept(self)


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.begDate.setDate(params.get('begDate', QDate.currentDate()))
        self.endDate.setDate(params.get('endDate', QDate.currentDate()))
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.cmbSpeciality.setValue(params.get('specialityId', None))
        self.cmbPerson.setValue(params.get('personId', None))
        self.cmbVidPom.setValue(params.get('vidPom', None))


    def params(self):
        params = {}
        params['begDate'] = self.begDate.date()
        params['endDate'] = self.endDate.date()
        params['orgStructureId'] = self.cmbOrgStructure.value()
        params['specialityId'] = self.cmbSpeciality.value()
        params['personId'] = self.cmbPerson.value()
        params['vidPom'] = self.cmbVidPom.value()
        return params
