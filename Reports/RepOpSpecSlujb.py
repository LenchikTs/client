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
from Reports.ReportView import CPageFormat
from Reports.ReportBase import *

from library.Utils      import *
from Reports.StationaryF007 import CStationaryF007SetupDialog 
  
    
class CSpec_Journal(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Журнал контроля оповещения спецслужб')
        self.pageFormat = CPageFormat(pageSize=CPageFormat.A4, orientation=CPageFormat.Landscape, leftMargin=10, topMargin=20, rightMargin=10,  bottomMargin=15)

    def getSetupDialog(self, parent):
        result = CStationaryF007SetupDialog(parent)
        result.setBegDateVisible(True)
        self.stationaryF007SetupDialog = result
        self.stationaryF007SetupDialog.chkIsEventInfo.setVisible(False)
        self.stationaryF007SetupDialog.chkCompactInfo.setVisible(False)
        self.stationaryF007SetupDialog.cmbSchedule.setVisible(False)
        self.stationaryF007SetupDialog.cmbHospitalBedProfile.setVisible(False)
        self.stationaryF007SetupDialog.chkNoProfileBed.setVisible(False)
        self.stationaryF007SetupDialog.chkIsPermanentBed.setVisible(False)
        self.stationaryF007SetupDialog.chkIsGroupingOS.setVisible(False)
        self.stationaryF007SetupDialog.chkNoPrintCaption.setVisible(False)
        self.stationaryF007SetupDialog.chkIsEventInfo.setVisible(False)
        self.stationaryF007SetupDialog.chkCompactInfo.setVisible(False)
        self.stationaryF007SetupDialog.chkNoPrintFilterParameters.setVisible(False)
        self.stationaryF007SetupDialog.cmbOrgStructure.setVisible(False)
        self.stationaryF007SetupDialog.lblOrgStructure.setVisible(False)
        self.stationaryF007SetupDialog.lblHospitalBedProfile.setVisible(False)
        self.stationaryF007SetupDialog.lblSchedule.setVisible(False)
        for i in xrange(result.gridLayout.count()):
            spacer=result.gridLayout.itemAt(i)
            if isinstance(spacer, QtGui.QSpacerItem):
                itemposition=result.gridLayout.getItemPosition(i)
                if itemposition!=(29, 0, 1, 1)and itemposition!=(8, 1, 1, 3):
                    result.gridLayout.removeItem(spacer)
        result.resize(400, 10)
        return result


    def selectData(self, params): 
        endDate = params.get('endDate', QDate())
        begDate = params.get('begDate', QDate())
        if not endDate:
            endDate = QDate.currentDate()
        if endDate:
            endTime = params.get('endTime', QTime(9, 0, 0, 0))
            begTime = params.get('begTime', None)
            endDateTime = QDateTime(endDate, endTime)
            if not begDate:
                begTime = begTime if begTime else endTime
                begDateTime = QDateTime(endDate.addDays(-1), begTime)
            else:
                begTime = begTime if begTime else endTime
                begDateTime = QDateTime(begDate, begTime)
        db = QtGui.qApp.db
        stmt = u'''SELECT e.id AS _id,e.client_id AS cli_id,sn.value AS number,a.directionDate as dat,os.name AS gosp,proc.value AS nom,IFNULL(e.externalId,e.id)AS sob,
  CONCAT(c.lastName,' ',c.firstName,' ',c.patrName)as fio, IFNULL(getClientRegAddress(c.id),getClientLocAddress(c.id))AS addres,
  getClientWork(c.id) AS work,doza.value AS dost,period.value AS diag,nomen.value AS prich,formatPersonName(a.setPerson_id)AS nazn,formatPersonName(a.Person_id)AS isp,
  quant.value AS slu,vk.value AS prin,a.endDate AS opo,c.birthDate as birth,a.begDate as date
FROM Event e
  LEFT JOIN Action a ON e.id = a.event_id
  LEFT JOIN ActionType at ON a.actionType_id=at.id
  left join ActionPropertyType apt on apt.actionType_id = at.id and apt.name = 'Номер телефонограммы' and apt.deleted = 0
  left join ActionProperty ap on ap.action_id = a.id and ap.type_id = apt.id
  left join ActionProperty_Integer sn on sn.id = ap.id
  left join ActionPropertyType apt2 on apt2.actionType_id = at.id and apt2.name = 'Госпитализирован' and apt2.deleted = 0
  left join ActionProperty ap_fin on ap_fin.action_id = a.id and ap_fin.type_id = apt2.id
  left join ActionProperty_OrgStructure fin on fin.id = ap_fin.id
  left join OrgStructure os ON fin.value = os.id
  left join ActionPropertyType apt3 on apt3.actionType_id = at.id and apt3.name = 'Номер извещения' and apt3.deleted = 0
  left join ActionProperty ap_proc on ap_proc.action_id = a.id and ap_proc.type_id = apt3.id
  left join ActionProperty_Integer proc on proc.id = ap_proc.id
  left join ActionPropertyType apt4 on apt4.actionType_id = at.id and apt4.name = 'Кем доставлен' and apt4.deleted = 0
  left join ActionProperty ap_doza on ap_doza.action_id = a.id and ap_doza.type_id = apt4.id
  left join ActionProperty_String doza on doza.id = ap_doza.id
  left join ActionPropertyType apt5 on apt5.actionType_id = at.id and apt5.name = 'Диагноз при обращении' and apt5.deleted = 0
  left join ActionProperty ap_period on ap_period.action_id = a.id and ap_period.type_id = apt5.id
  left join ActionProperty_String period on period.id = ap_period.id
  left join ActionPropertyType apt8 on apt8.actionType_id = at.id and apt8.name = 'Причина извещения' and apt8.deleted = 0
  left join ActionProperty ap_nomen on ap_nomen.action_id = a.id and ap_nomen.type_id = apt8.id
  left join ActionProperty_String nomen on nomen.id = ap_nomen.id
  left join ActionPropertyType apt6 on apt6.actionType_id = at.id and apt6.name = 'Наименование службы' and apt6.deleted = 0
  left join ActionProperty ap_quant on ap_quant.action_id = a.id and ap_quant.type_id = apt6.id
  left join ActionProperty_String quant on quant.id = ap_quant.id
  left join ActionPropertyType apt7 on apt7.actionType_id = at.id and apt7.name = 'Извещение принял' and apt7.deleted = 0
  left join ActionProperty ap_vk on ap_vk.action_id = a.id and ap_vk.type_id = apt7.id
  left join ActionProperty_String vk on vk.id = ap_vk.id
  left join Client c ON e.client_id = c.id
WHERE at.flatCode='j_specsl' AND a.deleted=0 AND at.deleted=0 AND e.deleted=0 AND a.endDate BETWEEN %(begDate)s AND %(endDate)s
ORDER BY fio
        '''% dict(begDate=db.formatDate(begDateTime),
                    endDate=db.formatDate(endDateTime)
                    )
        db = QtGui.qApp.db
        return db.query(stmt) 

    def build(self, params):
        reportRowSize = 16
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
            while query.next():
                record = query.record()
                _id= forceString(record.value('_id'))#name
                cli_id= forceString(record.value('cli_id'))#name
                number = forceString(record.value('number'))#+
                dat = forceString(record.value('dat'))#+
                gosp = forceString(record.value('gosp'))#+
                nom = forceString(record.value('nom'))#+
                sob = forceString(record.value('sob'))#+
                fio = forceString(record.value('fio'))#+
                bibi = forceDate(record.value('birth'))#+
                bebe = forceDate(record.value('date'))#+
                ag = calcAge(bibi, bebe)
                addres = forceString(record.value('addres'))#+
                work = forceString(record.value('work'))#+
                dost = forceString(record.value('dost'))#+
                diag = forceString(record.value('diag'))#+
                prich = forceString(record.value('prich'))#+
                nazn = forceString(record.value('nazn'))#+
                isp = forceString(record.value('isp'))#+
                slu = forceString(record.value('slu'))#+
                prin = forceString(record.value('prin'))#+
                opo = forceString(record.value('opo'))#+

                key = (number, gosp, nom, sob, fio, ag, addres, work, dost, diag, prich, nazn, isp, slu, prin, opo, _id, cli_id, bibi, dat)
                reportLine = reportData.setdefault(key)
                
             #   reportLine[0] += kd
             #   reportLine[1] += sum
              #  reportLine[2] += cnt
        query = self.selectData(params)
        processQuery(query)
        lpuCode = forceString(QtGui.qApp.db.translate('Organisation', 'id', QtGui.qApp.currentOrgId(), 'infisCode'))
        org = forceString(QtGui.qApp.db.translate('Organisation', 'id', QtGui.qApp.currentOrgId(), 'shortName'))
        vse= lpuCode +' '+ org
        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        cursor.insertHtml(u'''<table STYLE="font-size: 10pt;"><tr><td>медицинское учреждение: %s</td></tr></table>'''% vse)
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        tableColumns = [
            ('5%',  [ u'№ телефонограммы', ], CReportBase.AlignLeft),
            ('10%',  [ u'Дата и время поступления | Отделение госпитализации'], CReportBase.AlignLeft),
            ('2%',  [ u'Рег. №'], CReportBase.AlignLeft),
            ('3%',  [ u'№ мед. карты'], CReportBase.AlignLeft),
            ('10%',  [ u'Фамилия, имя, отчество пострадавшего'], CReportBase.AlignLeft),
            ('5%',  [ u'Возраст / Дата рождения'], CReportBase.AlignLeft),
            ('10%',  [ u'Адрес'], CReportBase.AlignLeft),
            ('10%',  [ u'Место учебы/работы'], CReportBase.AlignLeft),
            ('5%',  [ u'Направлен/ доставлен'], CReportBase.AlignLeft),
            ('10%',  [ u'Диагноз приемного отделения'], CReportBase.AlignLeft),
            ('10%',  [ u'Виды травм, отравлений и несчастных случаев'], CReportBase.AlignLeft),
            ('5%',  [ u'Фамилия И.О. врача'], CReportBase.AlignLeft),
            ('5%',  [ u'Фамилия И.О. передавшего информацию'], CReportBase.AlignLeft),
            ('5%',  [ u'Кому передано',u'Название службы'], CReportBase.AlignLeft),
            ('5%',  [ u'',u'Фамилия И.О. принявшего, должность'], CReportBase.AlignLeft),
            ('5%',  [ u'',u'Дата и время оповещения'], CReportBase.AlignLeft),
            ]
    
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 13, 1, 3)
        for col in xrange(reportRowSize):
            table.mergeCells(0, col, 2, 1)


        totalBynum = [0]*reportRowSize
        totalByReport = [0]*reportRowSize
        cnt_cli=0
        cl=None
        cnt_eve=0
        ev=None
        
        keys = reportData.keys()
        keys.sort()
        def drawTotal(table,  total,  text): 
    
            row = table.addRow()

            table.setText(row, 1, text, CReportBase.TableHeader, CReportBase.AlignLeft)
            table.mergeCells(row, 0, 1, 16)
        for key in keys:
            #key = (osname, fin,   infis,  name)key = (fioP, fio, happy, pol, snil, lgot, serial, number,nazn, mkb, name, vk)
            
            number = key[0]
            gosp = key[1]
            nom = key[2]
            sob = key[3]
            fio = key[4]
            ag = key[5]
            addres = key[6]
            work = key[7]
            dost = key[8]
            diag = key[9]
            prich = key[10]
            nazn = key[11]
            isp = key[12]
            slu = key[13]
            prin = key[14]
            opo = key[15]
            cli_id = key[16]
            _id = key[17]
            bibi = key[18]
            dat = key[19]
            #mergeCells(int row, int column, int numRows, int numCols)_id, cli_id
                
            if cl!=cli_id:
                cl=cli_id
                cnt_cli+=1
            if ev!=_id:
                ev=_id
                cnt_eve+=1
            
            row = table.addRow()          
            table.setText(row, 0, number)
            table.setText(row, 1, dat + ' / '+gosp)
            table.setText(row, 2, nom)
            table.setText(row, 3, sob)
            table.setText(row, 4, fio)
            table.setText(row, 5, ag + ' / '+ bibi.toString("dd.MM.yyyy"))
            table.setText(row, 6, addres)
            table.setText(row, 7, work)
            table.setText(row, 8, dost)
            table.setText(row, 9, diag)
            table.setText(row, 10, prich)
            table.setText(row, 11, nazn)
            table.setText(row, 12, isp)
            table.setText(row, 13, slu)
            table.setText(row, 14, prin)
            table.setText(row, 15, opo)
            
        #total
        drawTotal(table,  totalBynum, u'Количество пациентов %s ' %  cnt_cli);
        drawTotal(table,  totalBynum, u'Количество случаев %s ' %  cnt_eve);
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertHtml(u'''<table STYLE="font-size: 10pt;"><tr><td>Ответственный: _______________________________</td></tr></table>''')
        return doc

