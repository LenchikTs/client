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

from Orgs.Utils import getOrgStructureDescendants, getOrgStructureName
from Reports.Report import *
from Reports.ReportBase import *

from library.Utils import *
from Reports.ReportSetupDialog import CReportSetupDialog


class CRepServiceAttach(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Результаты экспорта вложений в ИЭМК')
        self.stattmp1 = ''

    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setEventTypeVisible(False)
        result.setOnlyPermanentAttachVisible(False)
        result.setOrgStructureVisible(True)
        result.chkActionClass.setText(u'Группировать по подразделениям')
        result.setPersonVisible(True)
        result.setActionTypeVisible(True)
        result.lblActionTypeClass.setVisible(False)
        result.lblActionType.setVisible(False)
        result.cmbActionTypeClass.setVisible(False)
        result.cmbActionType.setVisible(False)
        result.setTitle(self.title())
        for i in xrange(result.gridLayout.count()):
            spacer = result.gridLayout.itemAt(i)
            if isinstance(spacer, QtGui.QSpacerItem):
                itemposition = result.gridLayout.getItemPosition(i)
                if itemposition != (43, 0, 1, 10):
                    result.gridLayout.removeItem(spacer)
        result.resize(400, 10)
        return result


    def selectFileAttachData(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        chkActionTypeClass = params.get('chkActionTypeClass', False)
        chkDetailPerson = params.get('detailPerson', False)
        orgStructureId = params.get('orgStructureId', None)
        if orgStructureId:
            orgStructureIdList = getOrgStructureDescendants(orgStructureId)
            orgStructureList = u' and p_e.orgStructure_id in (%s)' %(','.join(map(str, orgStructureIdList)))
        else:
            orgStructureList = u''
        if chkDetailPerson:
            if chkActionTypeClass:
                order = 'GROUP BY fName,Vr ORDER BY fName,Vr'
            else:
                order = 'GROUP BY Vr ORDER BY Vr'
        else:
            if chkActionTypeClass:
                order = 'GROUP BY fName ORDER BY fName'
            else:
                order = ''
        personId = params.get('personId', None)
        if personId:
            condpersonId = ' and p.id = %d' % personId
        else:
            condpersonId = ''
        if not endDate or endDate.isNull():
            return None
        db = QtGui.qApp.db
        stmt = u'''  
            SELECT 
                COUNT(*) as cn,
                COUNT(ae.id) as cnExport,
                SUM(IF(at.class = 0 AND at.serviceType in (1, 2),1,0)) AS Dne,
                SUM(IF(at.serviceType = 0 AND at.flatCode like '%%epikriz%%' ,1,0)) AS Epi,
              SUM(IF(at.serviceType = 0 AND at.flatCode = 'inspection_mse' ,1,0)) AS mse,
                SUM(IF(((at.class = 0 AND at.serviceType in (1, 2)) OR (at.serviceType = 0 AND at.flatCode like '%%epikriz%%') OR (at.serviceType = 0 AND at.flatCode = 'inspection_mse')) AND afa.respSignatureBytes IS NOT NULL,1,0)) AS Pers,
                SUM(IF(((at.class = 0 AND at.serviceType in (1, 2)) OR (at.serviceType = 0 AND at.flatCode like '%%epikriz%%') OR (at.serviceType = 0 AND at.flatCode = 'inspection_mse')) AND afa.orgSignatureBytes IS NOT NULL,1,0)) AS MO,
                
                
                SUM(IF(at.class = 0 AND at.serviceType in (1, 2) AND ae.success=1,1,0)) AS dneYes,
                SUM(IF(at.class = 0 AND at.serviceType in (1, 2) AND ae.success=1 AND afa.respSignatureBytes IS NOT NULL,1,0)) AS dneYesPers,
                SUM(IF(at.class = 0 AND at.serviceType in (1, 2) AND ae.success=1 AND afa.orgSignatureBytes IS NOT NULL,1,0)) AS dneYesMO,
                SUM(IF(at.serviceType = 0 AND at.flatCode like '%%epikriz%%' AND ae.success=1 AND afa.respSignatureBytes IS NOT NULL,1,0)) AS epiYesPers,
                SUM(IF(at.serviceType = 0 AND at.flatCode like '%%epikriz%%' AND ae.success=1 AND afa.orgSignatureBytes IS NOT NULL,1,0)) AS epiYesMO,
                SUM(IF(at.serviceType = 0 AND at.flatCode like '%%epikriz%%' AND ae.success=1,1,0)) AS epiYes,
              SUM(IF(at.serviceType = 0 AND at.flatCode = 'inspection_mse' AND ae.success=1 AND afa.respSignatureBytes IS NOT NULL,1,0)) AS mseYesPers,
              SUM(IF(at.serviceType = 0 AND at.flatCode = 'inspection_mse' AND ae.success=1 AND afa.orgSignatureBytes IS NOT NULL,1,0)) AS mseYesMO,
              SUM(IF(at.serviceType = 0 AND at.flatCode = 'inspection_mse' AND ae.success=1,1,0)) AS mseYes,
                SUM(IF(at.class = 0 AND at.serviceType in (1, 2) AND ae.success=0,1,0)) AS dneNo,
                SUM(IF(at.serviceType = 0 AND at.flatCode like '%%epikriz%%' AND ae.success=0,1,0)) AS epiNo,
              SUM(IF(at.serviceType = 0 AND at.flatCode = 'inspection_mse' AND ae.success=0,1,0)) AS mseNo,
                IF(p.id IS NOT NULL, concat(p.lastName,' ',p.firstName,' ',p.patrName),'Не выбран исполнитель') as Vr,os.name AS fName
                
            FROM Action_FileAttach afa
                INNER JOIN (SELECT MAX(Action_FileAttach.id)AS iid FROM Action_FileAttach 
                      GROUP BY master_id)q 
                    on q.iid=afa.id
                  LEFT JOIN Action_FileAttach_Export ae ON ae.master_id = afa.id AND ae.id IN (SELECT MAX(id) FROM Action_FileAttach_Export WHERE afa.id=Action_FileAttach_Export.master_id)
                  inner JOIN Action a ON afa.master_id = a.id
                  inner JOIN ActionType at ON a.actionType_id = at.id
                  LEFT JOIN Person p ON p.id=IF(a.person_id, a.person_id, afa.respSigner_id)
                  LEFT JOIN OrgStructure os ON os.id=p.orgStructure_id
                  inner join Event e on e.id = a.event_id AND DATE(e.execDate) BETWEEN DATE(%(begDate)s) AND DATE(%(endDate)s) AND e.deleted=0
                  left join Person p_e on p_e.id = e.execPerson_id
            WHERE 
                a.deleted=0 AND afa.deleted=0 
                AND ((at.class = 0 AND at.serviceType in (1, 2)) OR (at.serviceType = 0 AND at.flatCode like '%%epikriz%%' and at.class = 3) OR (at.flatCode='inspection_mse' AND at.class=3))
                %(condpersonId)s %(orgStructureList)s

            %(order)s
           ''' % {'begDate': db.formatDate(begDate),
                  'endDate': db.formatDate(endDate),
                  'condpersonId': condpersonId,
                  'orgStructureList': orgStructureList,
                  'order': order
                  }
        db = QtGui.qApp.db
        return db.query(stmt)

    def selectFileAttachDataNotExport(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        orgStructureId = params.get('orgStructureId', None)
        if orgStructureId:
            orgStructureIdList = getOrgStructureDescendants(orgStructureId)
            orgStructureList = u' and p_e.orgStructure_id in (%s)' % (','.join(map(str, orgStructureIdList)))
        else:
            orgStructureList = u''
        if not endDate or endDate.isNull():
            return None
        db = QtGui.qApp.db
        stmt = u'''  
            SELECT 
                COUNT(*) as cn,
                e.id as eId,
                e.setDate,
                e.execDate,
                et.name,
                at.name as atname,
                e.client_id,
                CASE when at.class=0
                  THEN 'Статус'
                WHEN at.class=1
                  THEN 'Диагностика'
                WHEN at.class=2
                  THEN 'Лечение'
                WHEN at.class=3
                  THEN 'Мероприятия'
                END AS vkladka,
                CASE when at.serviceType=0
                THEN 'Прочие'
                when at.serviceType=1
                  THEN 'перв.осмотр'
                when at.serviceType=2
                  THEN 'повт.осмотр'
                when at.serviceType=3
                  THEN 'процедура/манип.'
                when at.serviceType=4
                  THEN 'операция'
                when at.serviceType=5
                  THEN 'исследование'
                when at.serviceType=6
                  THEN 'лечение'
                when at.serviceType=7
                  THEN 'профилактика'
                when at.serviceType=8
                  THEN 'анестезия'
                when at.serviceType=9
                  THEN 'реанимация'
                when at.serviceType=10
                  THEN 'лаб.исследование'
                END AS usl,
                at.flatCode,
                CASE WHEN a.status = 0 
                  THEN 'Начато'
                WHEN a.status = 1 
                  THEN 'Ожидание'
                WHEN a.status = 2 
                  THEN 'Закончено'
                WHEN a.status = 3 
                  THEN 'Отменено'
                WHEN a.status = 4 
                  THEN 'Без результата'
                WHEN a.status = 5 
                  THEN 'Назначено'
                WHEN a.status = 6 
                  THEN 'Отказ'
                END AS statu,
                a.endDate AS dat,
                IF(p.id IS NOT NULL, concat(p.lastName,' ',p.firstName,' ',p.patrName),'Не выбран исполнитель') as Vr,os.name AS fName

            FROM Action_FileAttach afa
        INNER JOIN (SELECT MAX(Action_FileAttach.id)AS iid FROM Action_FileAttach GROUP BY master_id)q on q.iid=afa.id
          LEFT JOIN Action_FileAttach_Export ae ON ae.master_id = afa.id AND ae.id IN (SELECT MAX(id) FROM Action_FileAttach_Export WHERE afa.id=Action_FileAttach_Export.master_id)
          inner JOIN Action a ON afa.master_id = a.id
          inner JOIN ActionType at ON a.actionType_id = at.id and at.deleted=0
          LEFT JOIN Person p ON p.id=IF(a.person_id, a.person_id, afa.respSigner_id)
          LEFT JOIN OrgStructure os ON os.id=p.orgStructure_id
          INNER JOIN Event e ON e.id=a.event_id AND DATE(e.execDate) BETWEEN DATE(%(begDate)s) AND DATE(%(endDate)s) and e.deleted = 0
          left join Person p_e on p_e.id = e.execPerson_id
          LEFT JOIN EventType et ON e.eventType_id=et.id
      
      WHERE  ae.id IS NULL AND a.deleted=0 AND afa.deleted=0 
          
                %(orgStructureList)s
            GROUP BY Vr,a.id ORDER BY setDate,execDate
            limit 1000
           ''' % {'begDate': db.formatDate(begDate),
                  'endDate': db.formatDate(endDate),
                  'orgStructureList': orgStructureList,
                  }
        db = QtGui.qApp.db
        return db.query(stmt)

    def getDescription(self, params):
        db = QtGui.qApp.db
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        chkActionTypeClass = params.get('chkActionTypeClass', False)
        chkDetailPerson = params.get('detailPerson', False)
        personId = params.get('personId', None)
        orgStructureId = params.get('orgStructureId', None)
        rows = []
        rows.append(dateRangeAsStr(u'за период', begDate, endDate))
        if orgStructureId:
            rows.append(u'по отделению: %s ' % (getOrgStructureName(orgStructureId)))
        if personId:
            rows.append(u'по врачу: %s ' % forceString(db.translate('vrbPerson', 'id', personId, 'name')))

        if chkDetailPerson:
            rows.append(u'детализировать по врачам %s ' % forceString(db.translate('vrbPerson', 'id', personId, 'name')))

        if chkActionTypeClass:
            rows.append(u'детализировать по отделениям %s ' % forceString(db.translate('vrbPerson', 'id', personId, 'name')))

        rows.append(u'отчёт составлен: ' + forceString(QDateTime.currentDateTime()))
        return rows

    def build(self, params):
        chkDetailPerson = params.get('detailPerson', False)
        chkActionTypeClass = params.get('chkActionTypeClass', False)

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertBlock()
        cursor.insertBlock()
        # рисуем первую табличку
        if chkActionTypeClass and chkDetailPerson:
            tableColumns = [
                ('20%', [u'Интегрированная электронная медицинская карта (ИЭМК)', u'Прикрепленные документы', u'врач', u''], CReportBase.AlignRight),
                ('5%', [u'', u'', u'всего', u''], CReportBase.AlignRight),
                ('10%', [u'', u'', u'из них', u'экспортировано'], CReportBase.AlignRight),
                ('10%', [u'', u'', u'', u'консультативных\nзаключений'], CReportBase.AlignRight),
                ('10%', [u'', u'', u'', u'эпикризов'], CReportBase.AlignRight),
                ('10%', [u'', u'', u'', u'направлений\nна МСЭ'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'', u'с подписью врача'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'', u'с подписью МО'], CReportBase.AlignRight),
                ('5%', [u'', u'Экспорт', u'консультативных заключений ', u'успешно экспортировано'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'', u'с подписью врача'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'', u'с подписью МО'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'', u'ошибка экспорта'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'эпикризов', u'успешно экспортировано'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'', u'с подписью врача'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'', u'с подписью МО'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'', u'ошибка экспорта'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'направлений на МСЭ', u'успешно экспортировано'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'', u'с подписью врача'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'', u'с подписью МО'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'', u'ошибка экспорта'], CReportBase.AlignRight),
            ]
        else:
            tableColumns = [
                ('4%', [u'Интегрированная электронная медицинская карта (ИЭМК) ', u'Прикрепленные документы', u'всего', u''], CReportBase.AlignRight),
                ('7%', [u'', u'', u'из них', u'экспортировано'], CReportBase.AlignRight),
                ('7%', [u'', u'', u'', u'консультативных\nзаключений'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'', u'эпикризов'], CReportBase.AlignRight),
                ('7%', [u'', u'', u'', u'направлений\nна МСЭ'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'', u'с подписью врача'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'', u'с подписью МО'], CReportBase.AlignRight),
                ('5%', [u'', u'Экспорт', u'консультативных заключений ', u'успешно экспортировано'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'', u'с подписью врача'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'', u'с подписью МО'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'', u'ошибка экспорта'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'эпикризов', u'успешно экспортировано'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'', u'с подписью врача'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'', u'с подписью МО'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'', u'ошибка экспорта'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'направлений на МСЭ', u'успешно экспортировано'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'', u'с подписью врача'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'', u'с подписью МО'], CReportBase.AlignRight),
                ('5%', [u'', u'', u'', u'ошибка экспорта'], CReportBase.AlignRight),
            ]

        table = createTable(cursor, tableColumns)
        if chkActionTypeClass and chkDetailPerson:
            table.mergeCells(0, 0, 1, 20)
            table.mergeCells(1, 0, 1, 8)
            table.mergeCells(2, 0, 2, 1)
            table.mergeCells(2, 1, 2, 1)
            table.mergeCells(2, 2, 1, 6)
            table.mergeCells(1, 8, 1, 12)
            table.mergeCells(2, 8, 1, 4)
            table.mergeCells(2, 12, 1, 4)
            table.mergeCells(2, 16, 1, 4)
        else:
            table.mergeCells(0, 0, 1, 19)
            table.mergeCells(1, 0, 1, 7)
            table.mergeCells(2, 0, 2, 1)
            table.mergeCells(2, 1, 1, 6)
            table.mergeCells(1, 7, 1, 12)
            table.mergeCells(2, 7, 1, 4)
            table.mergeCells(2, 11, 1, 4)
            table.mergeCells(2, 15, 1, 4)
        query = self.selectFileAttachData(params)
        person = None
        OrgStr = None

        sumPers = 0
        sumMO = 0
        sumdneYes = 0
        sumMseYes = 0
        sumepiYes = 0
        sumdneNo = 0
        sumMseNo = 0
        sumepiNo = 0
        sumDne = 0
        sumEpi = 0
        sumMse = 0
        sumCn = 0
        sumcnExport = 0
        sumcndneYesPers = 0
        sumcndneYesMO = 0
        sumcnepiYesPers = 0
        sumcnepiYesMO = 0
        sumcnMseYesPers = 0
        sumcnMseYesMO = 0

        while query.next():
            record = query.record()
            cn = forceInt(record.value('cn'))
            cnExport = forceInt(record.value('cnExport'))
            Pers = forceInt(record.value('Pers'))
            MO = forceInt(record.value('MO'))
            dneYes = forceInt(record.value('dneYes'))
            dneYesPers = forceInt(record.value('dneYesPers'))
            dneYesMO = forceInt(record.value('dneYesMO'))
            epiYes = forceInt(record.value('epiYes'))
            epiYesPers = forceInt(record.value('epiYesPers'))
            epiYesMO = forceInt(record.value('epiYesMO'))
            mseYes = forceInt(record.value('mseYes'))
            mseYesPers = forceInt(record.value('mseYesPers'))
            mseYesMO = forceInt(record.value('mseYesMO'))
            dneNo = forceInt(record.value('dneNo'))
            epiNo = forceInt(record.value('epiNo'))
            mseNo = forceInt(record.value('mseNo'))
            pers = forceString(record.value('Vr'))
            fName = forceString(record.value('fName'))
            Dne = forceInt(record.value('Dne'))
            Epi = forceInt(record.value('Epi'))
            mse = forceInt(record.value('mse'))

            def totalSum(sumCn, sumPers, sumMO, sumdneYes, sumepiYes, sumdneNo, sumepiNo, sumDne, sumEpi, sumcnExport, sumcndneYesPers, sumcndneYesMO, sumcnepiYesPers, sumcnepiYesMO, sumMse, sumMseYes, sumcnMseYesPers, sumcnMseYesMO, sumMseNo):
                row = table.addRow()
                table.setText(row, 0, u'ИТОГО по ' + OrgStr, CReportBase.TableHeader, CReportBase.AlignLeft)
                table.setText(row, 1, u'  ' + str(sumCn), CReportBase.TableHeader, CReportBase.AlignLeft)
                table.setText(row, 2, u'  ' + str(sumcnExport), CReportBase.TableHeader, CReportBase.AlignLeft)
                table.setText(row, 3, u'  ' + str(sumDne), CReportBase.TableHeader, CReportBase.AlignLeft)
                table.setText(row, 4, u'  ' + str(sumEpi), CReportBase.TableHeader, CReportBase.AlignLeft)
                table.setText(row, 5, u'  ' + str(sumMse), CReportBase.TableHeader, CReportBase.AlignLeft)
                table.setText(row, 6, u'  ' + str(sumPers), CReportBase.TableHeader, CReportBase.AlignLeft)
                table.setText(row, 7, u'  ' + str(sumMO), CReportBase.TableHeader, CReportBase.AlignLeft)
                table.setText(row, 8, u'  ' + str(sumdneYes), CReportBase.TableHeader, CReportBase.AlignLeft)
                table.setText(row, 9, u'  ' + str(sumcndneYesPers), CReportBase.TableHeader, CReportBase.AlignLeft)
                table.setText(row, 10, u'  ' + str(sumcndneYesMO), CReportBase.TableHeader, CReportBase.AlignLeft)
                table.setText(row, 11, u'  ' + str(sumdneNo), CReportBase.TableHeader, CReportBase.AlignLeft)
                table.setText(row, 12, u'  ' + str(sumepiYes), CReportBase.TableHeader, CReportBase.AlignLeft)
                table.setText(row, 13, u'  ' + str(sumcnepiYesPers), CReportBase.TableHeader, CReportBase.AlignLeft)
                table.setText(row, 14, u'  ' + str(sumcnepiYesMO), CReportBase.TableHeader, CReportBase.AlignLeft)
                table.setText(row, 15, u'  ' + str(sumepiNo), CReportBase.TableHeader, CReportBase.AlignLeft)
                table.setText(row, 16, u'  ' + str(sumMseYes), CReportBase.TableHeader, CReportBase.AlignLeft)
                table.setText(row, 17, u'  ' + str(sumcnMseYesPers), CReportBase.TableHeader, CReportBase.AlignLeft)
                table.setText(row, 18, u'  ' + str(sumcnMseYesMO), CReportBase.TableHeader, CReportBase.AlignLeft)
                table.setText(row, 19, u'  ' + str(sumMseNo), CReportBase.TableHeader, CReportBase.AlignLeft)


            if chkActionTypeClass:
                if chkDetailPerson:
                    if OrgStr == fName or OrgStr is None:
                        sumCn = sumCn + cn
                        sumcnExport = sumcnExport + cnExport
                        sumPers = sumPers + Pers
                        sumMO = sumMO + MO
                        sumdneYes = sumdneYes + dneYes
                        sumcndneYesPers = sumcndneYesPers + dneYesPers
                        sumcndneYesMO = sumcndneYesMO + dneYesMO
                        sumepiYes = sumepiYes + epiYes
                        sumcnepiYesPers = sumcnepiYesPers + epiYesPers
                        sumcnepiYesMO = sumcnepiYesMO + epiYesMO
                        sumdneNo = sumdneNo + dneNo
                        sumepiNo = sumepiNo + epiNo
                        sumMseYes = sumMseYes + mseYes
                        sumcnMseYesPers = sumcnMseYesPers + mseYesPers
                        sumcnMseYesMO = sumcnMseYesMO + mseYesMO
                        sumMseNo = sumMseNo + mseNo
                        sumDne = sumDne + Dne
                        sumEpi = sumEpi + Epi
                        sumMse = sumMse + mse
                    else:
                        totalSum(sumCn, sumPers, sumMO, sumdneYes, sumepiYes, sumdneNo, sumepiNo, sumDne, sumEpi, sumcnExport, sumcndneYesPers, sumcndneYesMO, sumcnepiYesPers, sumcnepiYesMO, sumMse, sumMseYes, sumcnMseYesPers, sumcnMseYesMO, sumMseNo)
                        sumPers = 0
                        sumMO = 0
                        sumdneYes = 0
                        sumepiYes = 0
                        sumMseYes = 0
                        sumdneNo = 0
                        sumepiNo = 0
                        sumMseNo = 0
                        sumDne = 0
                        sumEpi = 0
                        sumMse = 0
                        sumCn = 0
                        sumcnExport = 0
                        sumcndneYesPers = 0
                        sumcndneYesMO = 0
                        sumcnepiYesPers = 0
                        sumcnepiYesMO = 0
                        sumcnMseYesPers = 0
                        sumcnMseYesMO = 0

                        sumCn = sumCn + cn
                        sumcnExport = sumcnExport + cnExport
                        sumPers = sumPers + Pers
                        sumMO = sumMO + MO
                        sumdneYes = sumdneYes + dneYes
                        sumcndneYesPers = sumcndneYesPers + dneYesPers
                        sumcndneYesMO = sumcndneYesMO + dneYesMO
                        sumepiYes = sumepiYes + epiYes
                        sumcnepiYesPers = sumcnepiYesPers + epiYesPers
                        sumcnepiYesMO = sumcnepiYesMO + epiYesMO
                        sumdneNo = sumdneNo + dneNo
                        sumepiNo = sumepiNo + epiNo
                        sumMseYes = sumMseYes + mseYes
                        sumcnMseYesPers = sumcnMseYesPers + mseYesPers
                        sumcnMseYesMO = sumcnMseYesMO + mseYesMO
                        sumMseNo = sumMseNo + mseNo
                        sumDne = sumDne + Dne
                        sumEpi = sumEpi + Epi
                        sumMse = sumMse + mse

                if OrgStr != fName:
                    row = table.addRow()
                    table.setText(row, 1, u' ' + fName, CReportBase.TableHeader, CReportBase.AlignLeft)
                    if chkDetailPerson:
                        table.mergeCells(row, 0, 1, 10)
                    else:
                        table.mergeCells(row, 0, 1, 9)
            else:
                if chkDetailPerson:
                    if person != pers:
                        row = table.addRow()
                        table.setText(row, 1, u'Врач - ' + pers, CReportBase.TableHeader, CReportBase.AlignLeft)
                        table.mergeCells(row, 0, 1, 14)

            row = table.addRow()

            if chkActionTypeClass and chkDetailPerson:
                table.setText(row, 0, pers)
                table.setText(row, 1, cn)
                table.setText(row, 2, cnExport)
                table.setText(row, 3, Dne)
                table.setText(row, 4, Epi)
                table.setText(row, 5, mse)
                table.setText(row, 6, Pers)
                table.setText(row, 7, MO)
                table.setText(row, 8, dneYes)
                table.setText(row, 9, dneYesPers)
                table.setText(row, 10, dneYesMO)
                table.setText(row, 11, dneNo)
                table.setText(row, 12, epiYes)
                table.setText(row, 13, epiYesPers)
                table.setText(row, 14, epiYesMO)
                table.setText(row, 15, epiNo)
                table.setText(row, 16, mseYes)
                table.setText(row, 17, mseYesPers)
                table.setText(row, 18, mseYesMO)
                table.setText(row, 19, mseNo)
            else:
                table.setText(row, 0, cn)
                table.setText(row, 1, cnExport)
                table.setText(row, 2, Dne)
                table.setText(row, 3, Epi)
                table.setText(row, 4, mse)
                table.setText(row, 5, Pers)
                table.setText(row, 6, MO)
                table.setText(row, 7, dneYes)
                table.setText(row, 8, dneYesPers)
                table.setText(row, 9, dneYesMO)
                table.setText(row, 10, dneNo)
                table.setText(row, 11, epiYes)
                table.setText(row, 12, epiYesPers)
                table.setText(row, 13, epiYesMO)
                table.setText(row, 14, epiNo)
                table.setText(row, 15, mseYes)
                table.setText(row, 16, mseYesPers)
                table.setText(row, 17, mseYesMO)
                table.setText(row, 18, mseNo)

            if chkDetailPerson:
                person = pers

            if chkActionTypeClass:
                OrgStr = fName


        if chkActionTypeClass and chkDetailPerson:
            totalSum(sumCn, sumPers, sumMO, sumdneYes, sumepiYes, sumdneNo, sumepiNo, sumDne, sumEpi, sumcnExport, sumcndneYesPers, sumcndneYesMO, sumcnepiYesPers, sumcnepiYesMO, sumMse, sumMseYes, sumcnMseYesPers, sumcnMseYesMO, sumMseNo)

        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.setBlockFormat(CReportBase.AlignCenter)
        cursor.insertText(u'Список прикрепленных документов не подлежащих или еще не выгруженных в ИЭМК')
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.setBlockFormat(CReportBase.AlignCenter)
        cursor.insertText(u'В выгрузку попадают выписные эпикризы - статус "закончено", вид услуги в типе действия "прочее", вкладка "мероприятия", код для отчетов "epikriz"')
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.setBlockFormat(CReportBase.AlignCenter)
        cursor.insertText(u'В выгрузку попадают консультативные заключения - статус "закончено", вкладка "статус", вид услуги в типе действия "первичный или повторный осмотр"')
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.setBlockFormat(CReportBase.AlignCenter)
        cursor.insertText(u'В выгрузку попадают направления на МСЭ - статус "закончено", код для отчетов "inspection_mse", прикреплено и подписано 2 документа (они создаются при нажатии кнопки "прикрепить и подписать" в шаблоне печати)')
        cursor.insertBlock()
        cursor.insertBlock()

        tableColumns = [
            ('5%', [u'Прикрепленные но не подлежащие или еще не выгруженные документы', u'код пациента'], CReportBase.AlignRight),
            ('5%', [u'', u'код карточки события'], CReportBase.AlignRight),
            ('10%', [u'', u'дата начала события'], CReportBase.AlignRight),
            ('10%', [u'', u'дата окончания события'], CReportBase.AlignRight),
            ('10%', [u'', u'тип события'], CReportBase.AlignRight),
            ('10%', [u'', u'тип действия'], CReportBase.AlignRight),
            ('10%', [u'', u'вкладка нахождения типа действия'], CReportBase.AlignRight),
            ('10%', [u'', u'вид услуги в типе действия'], CReportBase.AlignRight),
            ('10%', [u'', u'код для отчетов в типе действия'], CReportBase.AlignRight),
            ('10%', [u'', u'статус действия'], CReportBase.AlignRight),
            ('10%', [u'', u'дата окончания действия'], CReportBase.AlignRight),
        ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 1, 11)

        query = self.selectFileAttachDataNotExport(params)
        while query.next():
            record = query.record()
            eId = forceInt(record.value('eId'))
            client = forceInt(record.value('client_id'))
            setDate = forceDate(record.value('setDate')).toString("dd.MM.yyyy")
            execDate = forceDate(record.value('execDate')).toString("dd.MM.yyyy")
            name = forceString(record.value('name'))
            atname = forceString(record.value('atname'))
            vkladka = forceString(record.value('vkladka'))
            usl = forceString(record.value('usl'))
            flatCode = forceString(record.value('flatCode'))
            statu = forceString(record.value('statu'))
            dat = forceDate(record.value('dat')).toString("dd.MM.yyyy")

            row = table.addRow()

            table.setText(row, 0, client)
            table.setText(row, 1, eId)
            table.setText(row, 2, setDate)
            table.setText(row, 3, execDate)
            table.setText(row, 4, name)
            table.setText(row, 5, atname)
            table.setText(row, 6, vkladka)
            table.setText(row, 7, usl)
            table.setText(row, 8, flatCode)
            table.setText(row, 9, statu)
            table.setText(row, 10, dat)



        return doc
