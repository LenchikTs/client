# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
from PyQt4 import QtGui
from PyQt4.QtCore import QDate

from Reports.Report import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.ReportSetupDialog import CReportSetupDialog
from library.Utils import forceInt

# наименование / №  п/п / ед.изм / fieldName
MainRows = [(
    u'Численность взрослого населения (18 лет и старше), находящегося под наблюдением медицинской организации, всего (на отчетный период)',
    '1', u'чел.', ''), (u'в том числе: взрослых инвалидов', '1.1', u'чел.', 'cntAdult'),
    (u'из них: впервые признанных инвалидами', '1.1.1', u'чел.', 'cntAdultFirstInv'), (
        u'Численность детского населения (0-17 лет), находящегося под наблюдением медицинской организации, всего (на отчетный период)',
        '2', u'чел.', ''), (u'в том числе: детей-инвалидов', '2.1', u'чел.', 'cntChild'),
    (u'из них: впервые признанных инвалидами', '2.1.1', u'чел.', 'cntChildFirstInv'),
    (u'Число посещений врачей инвалидами, всего', '17', u'ед.', 'cntPosAll'),
    (u'в том числе: взрослыми', '17.1', u'ед.', 'cntPosAdult'), (u'детьми', '17.2', u'ед.', 'cntPosChild'), (
        u'Число обращений взрослых инвалидов к врачам для оказания медицинской помощи с использованием реабилитационных процедур (Z50)',
        '18', u'ед.', 'cntHospAll'), (u'в том числе: взрослыми', '18.1', u'ед.', 'cntHospAdult'),
    (u'детьми', '18.2', u'ед.', 'cntHospChild'),
    (u'Число инвалидов, нуждающихся в медицинской реабилитации, в рамках ИПРА', '23', u'чел.', 'cntAll'),
    (u'в том числе: взрослых', '23.1', u'чел.', 'cntAdult'), (u'детей', '23.2', u'чел.', 'cntChild')]


class CReportMonitoringReabilityInvalid(CReport):

    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Мониторинг реабилитации инвалидов')

    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setEventTypeVisible(False)
        result.setMKBFilterVisible(False)
        result.setPersonVisible(False)
        result.cmbPerson.setVisible(False)
        result.lblPerson.setVisible(False)
        result.setOnlyPermanentAttachVisible(False)
        result.setTitle(self.title())
        result.setOrgStructureVisible(False)
        result.setActionStatusVisible(False)
        for i in xrange(result.gridLayout.count()):
            spacer = result.gridLayout.itemAt(i)
            if isinstance(spacer, QtGui.QSpacerItem):
                itemposition = result.gridLayout.getItemPosition(i)
                if itemposition != (29, 0, 1, 1) and itemposition != (8, 1, 1, 3):
                    result.gridLayout.removeItem(spacer)
        result.resize(400, 10)
        return result

    def build(self, params):
        reportMainData = dict(cntAll=0, cntAdult=0, cntAdultFirstInv=0, cntChild=0, cntChildFirstInv=0, cntPosAdult=0,
                              cntPosChild=0, cntPosAll=0, cntHospAdult=0, cntHospChild=0, cntHospAll=0)
        query = selectData(params)
        while query.next():
            record = query.record()
            cnt = forceInt(record.value('cnt'))
            ageOut = forceInt(record.value('ageOut'))
            firstInv = forceInt(record.value('firstInv'))
            cntPosAdult = forceInt(record.value('cntPosAdult'))
            cntPosChild = forceInt(record.value('cntPosChild'))
            cntHospAdult = forceInt(record.value('cntHospAdult'))
            cntHospChild = forceInt(record.value('cntHospChild'))

            reportMainData['cntAll'] += cnt
            reportMainData['cntPosAdult'] += cntPosAdult
            reportMainData['cntPosChild'] += cntPosChild
            reportMainData['cntPosAll'] += cntPosAdult + cntPosChild
            reportMainData['cntHospAdult'] += cntHospAdult
            reportMainData['cntHospChild'] += cntHospChild
            reportMainData['cntHospAll'] += cntHospAdult + cntHospChild
            if ageOut >= 18:
                reportMainData['cntAdult'] += cnt
                if firstInv:
                    reportMainData['cntAdultFirstInv'] += cnt
            else:
                reportMainData['cntChild'] += cnt
                if firstInv:
                    reportMainData['cntChildFirstInv'] += cnt

        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(
            u'Форма мониторинга организации медицинской реабилитации инвалидов и детей-инвалидов в медицинских организациях, имеющих лицензию на осуществление медицинской деятельности, включая работы (услуги), по медицинской реабилитации, и в санаторно-курортных организациях, в условиях которых осуществляется медицинская реабилитация на основании соответствующей лицензии')
        tableColumns = [('10%', [u'№ п/п'], CReportBase.AlignCenter),
                        ('60%', [u'Показатель'], CReportBase.AlignLeft),
                        ('10%', [u'Единица измерения'], CReportBase.AlignCenter),
                        ('20%', [u'Всего'], CReportBase.AlignCenter)]
        table = createTable(cursor, tableColumns)

        for row, rowDescr in enumerate(MainRows):
            i = table.addRow()
            table.setText(i, 0, rowDescr[1])
            table.setText(i, 1, rowDescr[0])
            table.setText(i, 2, rowDescr[2])
            table.setText(i, 3, reportMainData.get(rowDescr[3], ''))
        return doc


def selectData(params):
    db = QtGui.qApp.db
    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())

    stmt = u'''SELECT COUNT(c.id) AS cnt, age(c.birthDate, {endDate}) AS ageOut,
  NOT EXISTS(SELECT NULL FROM ClientSocStatus cssold
              left JOIN rbSocStatusClass sscold ON sscold.id = cssold.socStatusClass_id
              left JOIN rbSocStatusClass sscold2 ON sscold2.id = sscold.group_id
              left JOIN rbSocStatusType sstold ON sstold.id = cssold.socStatusType_id
              WHERE cssold.client_id = css.client_id AND cssold.deleted = 0 AND cssold.begDate < css.begDate
                    AND sstold.code in ('081', '082', '083', '084')
                    AND cssold.note IN ('1с', '2с', '3с', '4с') 
                    AND sscold2.code = '1' AND sscold.code = '1') AND css.begDate BETWEEN {begDate} AND {endDate} AS firstInv
  , SUM((SELECT count(e.id) 
    FROM Event e
    left JOIN EventType et ON et.id = e.eventType_id
    LEFT JOIN rbMedicalAidType mat ON mat.id = et.medicalAidType_id
    WHERE mat.regionalCode IN ('21', '211', '261') AND et.deleted = 0 AND IFNULL(et.finance_id, 1) != 4
      AND e.client_id = c.id AND e.deleted = 0 AND e.setDate BETWEEN {begDate} AND {endDate})) AS cntPosAdult
  , SUM((SELECT count(e.id) 
    FROM Event e
    left JOIN EventType et ON et.id = e.eventType_id
    LEFT JOIN rbMedicalAidType mat ON mat.id = et.medicalAidType_id
    WHERE mat.regionalCode IN ('22', '262') AND et.deleted = 0 AND IFNULL(et.finance_id, 1) != 4
      AND e.client_id = c.id AND e.deleted = 0 AND e.setDate BETWEEN {begDate} AND {endDate})) AS cntPosChild
  , SUM((SELECT count(e.id) 
    FROM Event e
    left JOIN EventType et ON et.id = e.eventType_id
    LEFT JOIN rbMedicalAidType mat ON mat.id = et.medicalAidType_id
    WHERE mat.regionalCode IN ('11', '41') AND et.deleted = 0 AND IFNULL(et.finance_id, 1) != 4
      AND e.client_id = c.id AND e.deleted = 0 AND e.setDate BETWEEN {begDate} AND {endDate})) AS cntHospAdult
  , SUM((SELECT count(e.id) 
    FROM Event e
    left JOIN EventType et ON et.id = e.eventType_id
    LEFT JOIN rbMedicalAidType mat ON mat.id = et.medicalAidType_id
    WHERE mat.regionalCode IN ('12', '42') AND et.deleted = 0 AND IFNULL(et.finance_id, 1) != 4
      AND e.client_id = c.id AND e.deleted = 0 AND e.setDate BETWEEN {begDate} AND {endDate})) AS cntHospChild
FROM Client c
LEFT JOIN ClientSocStatus css ON css.id = (SELECT ClientSocStatus.id 
          FROM ClientSocStatus
          left JOIN rbSocStatusClass ssc ON ssc.id = ClientSocStatus.socStatusClass_id
          left JOIN rbSocStatusClass ssc2 ON ssc2.id = ssc.group_id
          left JOIN rbSocStatusType sst ON sst.id = ClientSocStatus.socStatusType_id
          WHERE ClientSocStatus.deleted = 0 
            AND ClientSocStatus.client_id = c.id
            AND sst.code in ('081', '082', '083', '084')
            AND ClientSocStatus.note IN ('1с', '2с', '3с', '4с')
            AND ssc2.code = '1' AND ssc.code = '1'
            AND ClientSocStatus.begDate <= {endDate} 
                AND IFNULL(ClientSocStatus.endDate, {begDate}) >= {begDate}
            ORDER BY ClientSocStatus.begDate DESC LIMIT 1) 
WHERE css.deleted = 0 AND c.deleted = 0
AND NOT EXISTS(select NULL FROM ClientContingentKind cck
  left JOIN rbContingentKind ck ON ck.id = cck.contingentKind_id
WHERE cck.client_id = c.id and cck.deleted = 0 and ck.code = 'А' AND cck.endDate is null)    
GROUP BY ageOut, firstInv;'''.format(begDate=db.formatDate(begDate), endDate=db.formatDate(endDate))
    return db.query(stmt)
