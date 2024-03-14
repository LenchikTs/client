# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2022 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4              import QtGui
from PyQt4.QtCore       import QDate, Qt
from library.Utils      import forceInt, forceDouble
from library.database   import decorateString
from Reports.Report     import CReport
from Reports.ReportBase import CReportBase, createTable


def selectData(params):
    stmt = u'''
SELECT Client.id,
       Client.sex,
       age(Client.birthDate, CURDATE()) AS age,

  (SELECT COUNT(CV.id)
   FROM ClientVaccination CV
   WHERE CV.client_id = Client.id
     AND CV.deleted = 0
     AND CV.vaccine_id IS NOT NULL
     AND DATE(CV.datetime) BETWEEN {begDate} AND {endDate}) AS countVaccine,

  (SELECT SUM(A.amount)
   FROM Action A
   JOIN Event E ON A.event_id = E.id
   JOIN ActionType `AT` ON A.actionType_id = `AT`.id
   WHERE A.deleted = 0
     AND E.deleted = 0
     AND `AT`.deleted = 0
     AND E.client_id = Client.id
     AND DATE(E.setDate) BETWEEN {begDate} AND {endDate}
     AND `AT`.serviceType = 10
     AND A.status = 2) AS countAnalysis,

  (SELECT SUM(A.amount)
   FROM Action A
   JOIN Event E ON A.event_id = E.id
   JOIN ActionType `AT` ON A.actionType_id = `AT`.id
   WHERE A.deleted = 0
     AND E.deleted = 0
     AND `AT`.deleted = 0
     AND E.client_id = Client.id
     AND DATE(E.setDate) BETWEEN {begDate} AND {endDate}
     AND `AT`.serviceType = 5
     AND A.status = 2) AS countResearch,

  (SELECT SUM(A.amount)
   FROM Action A
   JOIN Event E ON A.event_id = E.id
   JOIN ActionType `AT` ON A.actionType_id = `AT`.id
   WHERE A.deleted = 0
     AND E.deleted = 0
     AND `AT`.deleted = 0
     AND E.client_id = Client.id
     AND DATE(E.setDate) BETWEEN {begDate} AND {endDate}
     AND `AT`.serviceType = 3
     AND A.status = 2) AS countProcedures,

  (SELECT SUM(A.amount)
   FROM Action A
   JOIN Event E ON A.event_id = E.id
   JOIN ActionType `AT` ON A.actionType_id = `AT`.id
   WHERE A.deleted = 0
     AND E.deleted = 0
     AND `AT`.deleted = 0
     AND E.client_id = Client.id
     AND DATE(E.setDate) BETWEEN {begDate} AND {endDate}
     AND `AT`.serviceType IN (1, 2)
     AND A.status = 2) AS countConsultations,

  EXISTS(SELECT NULL
   FROM Event E
   JOIN EventType ET ON E.eventType_id = ET.id
   JOIN rbEventTypePurpose ON ET.purpose_id = rbEventTypePurpose.id
   JOIN rbMedicalAidKind ON ET.medicalAidKind_id = rbMedicalAidKind.id
   JOIN rbMedicalAidType ON ET.medicalAidType_id = rbMedicalAidType.id
   WHERE E.client_id = Client.id
     AND E.deleted = 0
     AND ET.deleted = 0
     AND rbEventTypePurpose.name = 'СМП'
     AND rbMedicalAidKind.name = 'Скорая, в том числе специализированная, медицинская помощь'
     AND rbMedicalAidType.name = 'Скорая помощь'
     AND DATE(E.execDate) BETWEEN {begDate} AND {endDate}) AS isSMP,

  EXISTS(SELECT NULL
   FROM Event E
   JOIN EventType ET ON E.eventType_id = ET.id
   JOIN EmergencyCall EC ON EC.event_id = E.id
   JOIN rbEventTypePurpose ON ET.purpose_id = rbEventTypePurpose.id
   JOIN rbMedicalAidKind ON ET.medicalAidKind_id = rbMedicalAidKind.id
   JOIN rbMedicalAidType ON ET.medicalAidType_id = rbMedicalAidType.id
   JOIN rbEmergencyResult ON EC.resultCall_id = rbEmergencyResult.id
   WHERE E.client_id = Client.id
     AND E.deleted = 0
     AND ET.deleted = 0
     AND EC.deleted = 0
     AND rbEventTypePurpose.name = 'СМП'
     AND rbMedicalAidKind.name = 'Скорая, в том числе специализированная, медицинская помощь'
     AND rbMedicalAidType.name = 'Скорая помощь'
     AND rbEmergencyResult.code = '4'
     AND DATE(E.execDate) BETWEEN {begDate} AND {endDate}) AS isSMPHospitalized,

  EXISTS(SELECT NULL
   FROM ClientSocStatus CSS
   JOIN rbSocStatusClass ON CSS.socStatusClass_id = rbSocStatusClass.id
   JOIN rbSocStatusType ON CSS.socStatusType_id = rbSocStatusType.id
   WHERE CSS.client_id = Client.id
     AND CSS.deleted = 0
     AND rbSocStatusType.code IN ('081', '082', '083')
     AND (CSS.endDate IS NULL OR DATE(CSS.endDate) > {begDate})) AS gotDisability,

  EXISTS(SELECT NULL
   FROM ClientSocStatus CSS
   JOIN rbSocStatusClass ON CSS.socStatusClass_id = rbSocStatusClass.id
   JOIN rbSocStatusType ON CSS.socStatusType_id = rbSocStatusType.id
   WHERE CSS.client_id = Client.id
     AND CSS.deleted = 0
     AND rbSocStatusType.code IN ('081', '082', '083')
     AND DATE(CSS.begDate) BETWEEN {begDate} AND {endDate}) AS gotDisabilityInPeriod,

  EXISTS(SELECT C.deathDate
   FROM Client C
   WHERE C.id = Client.id
     AND C.deleted = 0
     AND DATE(C.deathDate) BETWEEN {begDate} AND {endDate}) AS isDead,

  EXISTS(SELECT C.deathPlaceType_id
   FROM Client C
   JOIN rbDeathPlaceType DPT ON DPT.id = C.deathPlaceType_id
   WHERE C.id = Client.id
     AND C.deleted = 0
     AND DPT.name like '%дома%') AS isDeadAtHome

FROM Client
WHERE Client.deleted = 0
  AND Client.sex != 0
  AND EXISTS
    (SELECT NULL
     FROM ClientAttach CA
     LEFT JOIN rbAttachType AT ON AT.id = CA.attachType_id
     LEFT JOIN rbFinance F ON F.id = AT.finance_id
     WHERE CA.client_id = Client.id
       AND CA.deleted = 0
       AND CA.orgStructure_id = {orgStructureId}
       AND (DATE(CA.endDate) > {endDate}
       OR CA.endDate is NULL)
       AND F.name like '%ОМС%')
    '''

    db = QtGui.qApp.db
    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())
    orgStructureId = forceInt(params.get('orgStructureId', 0))
    return db.query(stmt.format(
        begDate=decorateString(begDate.toString(Qt.ISODate)),
        endDate=decorateString(endDate.toString(Qt.ISODate)),
        orgStructureId=orgStructureId))



class CReportPassportT1200(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Т.1200')


    def getSetupDialog(self, parent):
        dialog = CReport.getSetupDialog(self, parent)
        dialog.setEventTypeVisible(False)
        dialog.setOnlyPermanentAttachVisible(False)
        dialog.setOrgStructureVisible(True)
        dialog.adjustSize()
        return dialog


    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        tableColumns = [
            ('10%',  [u'Возрастной состав прикрепленного к врачебному (терапевтическому) участку населения', u'', u'1'], CReportBase.AlignLeft),
            ('7.5%', [u'№ строки', u'', u'2'], CReportBase.AlignRight),
            ('7.5%', [u'Число проведенных мероприятий (ед.)', u'прививок', u'15'], CReportBase.AlignRight),
            ('7.5%', [u'', u'анализов', u'16'], CReportBase.AlignRight),
            ('7.5%', [u'', u'исследований', u'17'], CReportBase.AlignRight),
            ('7.5%', [u'', u'процедур', u'18'], CReportBase.AlignRight),
            ('7.5%', [u'', u'консультаций', u'19'], CReportBase.AlignRight),
            ('7.5%', [u'Число лиц, которым оказана скорая медицинская помощь при выездах (человек)', u'', u'20'], CReportBase.AlignRight),
            ('7.5%', [u'в т.ч. направлено в стационар', u'', u'21'], CReportBase.AlignRight),
            ('7.5%', [u'Выход на инвалидность (человек)', u'всего', u'22'], CReportBase.AlignRight),
            ('7.5%', [u'', u'в т.ч. в отчетном году', u'23'], CReportBase.AlignRight),
            ('7.5%', [u'Число умерших (человек)', u'всего', u'24'], CReportBase.AlignRight),
            ('7.5%', [u'', u'в т.ч. на дому', u'25'], CReportBase.AlignRight),
        ]
        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 1, 5)
        table.mergeCells(0, 7, 2, 1)
        table.mergeCells(0, 8, 2, 1)
        table.mergeCells(0, 9, 1, 2)
        table.mergeCells(0, 11, 1, 2)

        ableMale = [0] * 11
        ableFemale = [0] * 11
        seniorMale = [0] * 11
        seniorFemale = [0] * 11

        query = selectData(params)
        while query.next():
            record = query.record()
            sex = forceInt(record.value('sex'))
            age = forceInt(record.value('age'))

            reportLine = None
            if sex == 1:
                if 16 <= age < 65:
                    reportLine = ableMale
                elif age >= 65:
                    reportLine = seniorMale
                else:
                    continue
            elif sex == 2:
                if 16 <= age < 60:
                    reportLine = ableFemale
                elif age >= 60:
                    reportLine = seniorFemale
                else:
                    continue
            else:
                continue

            reportLine[0] += forceInt(record.value('countVaccine'))
            reportLine[1] += forceInt(record.value('countAnalysis'))
            reportLine[2] += forceInt(record.value('countResearch'))
            reportLine[3] += forceInt(record.value('countProcedures'))
            reportLine[4] += forceInt(record.value('countConsultations'))
            reportLine[5] += forceInt(record.value('isSMP'))
            reportLine[6] += forceInt(record.value('isSMPHospitalized'))
            reportLine[7] += forceInt(record.value('gotDisability'))
            reportLine[8] += forceInt(record.value('gotDisabilityInPeriod'))
            reportLine[9] += forceInt(record.value('isDead'))
            reportLine[10] += forceInt(record.value('isDeadAtHome'))

        totalAble = [sum(x) for x in zip(ableMale, ableFemale)]
        totalSeniors = [sum(x) for x in zip(seniorMale, seniorFemale)]
        total = [sum(x) for x in zip(totalAble, totalSeniors)]

        row = table.addRow()
        table.setText(row, 0, u'ВСЕГО')
        table.setText(row, 1, u'1.')
        for col, value in enumerate(total):
            table.setText(row, 2+col, value)

        row = table.addRow()
        table.setText(row, 0, u'в том числе:\nтрудоспособного возраста')
        table.setText(row, 1, u'2.')
        for col, value in enumerate(totalAble):
            table.setText(row, 2+col, value)

        row = table.addRow()
        table.setText(row, 0, u'мужчины')
        table.setText(row, 1, u'3.')
        for col, value in enumerate(ableMale):
            table.setText(row, 2+col, value)

        row = table.addRow()
        table.setText(row, 0, u'женщины')
        table.setText(row, 1, u'4.')
        for col, value in enumerate(ableFemale):
            table.setText(row, 2+col, value)

        row = table.addRow()
        table.setText(row, 0, u'нетрудоспособного возраста')
        table.setText(row, 1, u'5.')
        for col, value in enumerate(totalSeniors):
            table.setText(row, 2+col, value)

        row = table.addRow()
        table.setText(row, 0, u'мужчины')
        table.setText(row, 1, u'6.')
        for col, value in enumerate(seniorMale):
            table.setText(row, 2+col, value)

        row = table.addRow()
        table.setText(row, 0, u'женщины')
        table.setText(row, 1, u'7.')
        for col, value in enumerate(seniorFemale):
            table.setText(row, 2+col, value)

        return doc
