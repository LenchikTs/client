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
from Ui_s11main import _fromUtf8

from library.Utils import *
from Reports.ReportSetupDialog import CReportSetupDialog


class CAnalitic_referralMSE(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Контроль выгрузки подписанных мсэ в региональную РЭМД')
        self.stattmp1 = ''

    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setEventTypeVisible(False)
        result.setOnlyPermanentAttachVisible(False)
        result.setOrgStructureVisible(True)
        result.chkActionClass.setText(u'Группировать по подразделениям')
        result.setActionTypeVisible(False)
        result.setPersonVisible(False)
        result.setClientIdVisible(False)
        result.lblClientId.setVisible(False)
        result.lblOrgStructure.setText(u'Подразделение (по исполнителю)')
        result.lblPerson.setVisible(False)
        result.lblEventStatus.setText(u'Детализировать по')
        result.setEventStatusVisible(True)

        result.cmbEventStatus.setItemText(0, u'требуют подписи МО')
        result.cmbEventStatus.setItemText(1, u'готовы к отправке')
        result.cmbEventStatus.setItemText(2, u'без подписания ЧК')
        result.cmbEventStatus.addItem(_fromUtf8(""))
        result.cmbEventStatus.setItemText(3, u'отправленные')
        result.cmbEventStatus.addItem(_fromUtf8(""))
        result.cmbEventStatus.setItemText(4, u'все')

        result.lblActionTypeClass.setVisible(False)
        result.chkDiagnosisType.setVisible(True)
        result.chkDiagnosisType.setText(u'Расширить информацию по подписям')
        result.lblActionType.setVisible(False)
        result.cmbActionTypeClass.setVisible(False)
        result.cmbActionType.setVisible(False)
        result.setGroupOrganisation(True)
        result.setTitle(self.title())
        for i in xrange(result.gridLayout.count()):
            spacer = result.gridLayout.itemAt(i)
            if isinstance(spacer, QtGui.QSpacerItem):
                itemposition = result.gridLayout.getItemPosition(i)
                if itemposition != (43, 0, 1, 10):
                    result.gridLayout.removeItem(spacer)
        result.resize(400, 10)
        return result

    def selectData(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        details = params.get('eventStatus', None)
        detalSign = params.get('diagnosisType', False)
        orgStructureId = params.get('orgStructureId', None)
        groupOrganisation = params.get('groupOrganisation', False)

        if details == 0:
            detail = u' AND (afa.orgSigner_id IS  NULL and afa.respSigner_id IS NOT NULL ) AND IF(p.id  IS NOT NULL,IF(afas.id  IS NOT NULL,1,0),1) AND IF(p2.id IS NOT NULL,IF(afas2.id IS NOT NULL,1,0),1) AND IF(p3.id IS NOT NULL,IF(afas3.id IS NOT NULL,1,0),1) AND IF(p4.id IS NOT NULL,IF(afas4.id IS NOT NULL,1,0),1) AND IF(p5.id IS NOT NULL,IF(afas5.id IS NOT NULL,1,0),1) AND IF(p6.id IS NOT NULL,IF(afas6.id IS NOT NULL,1,0),1) AND IF(p7.id IS NOT NULL,IF(afas7.id IS NOT NULL,1,0),1) AND IF(p8.id IS NOT NULL,IF(afas8.id IS NOT NULL,1,0),1) AND IF(p9.id IS NOT NULL,IF(afas9.id IS NOT NULL,1,0),1) AND IF(p10.id IS NOT NULL,IF(afas10.id IS NOT NULL,1,0),1) '
        elif details == 1:
            detail = u' AND (afa.orgSigner_id IS NOT NULL and afa.respSigner_id IS NOT NULL ) AND IF(p.id  IS NOT NULL,IF(afas.id  IS NOT NULL,1,0),1) AND IF(p2.id IS NOT NULL,IF(afas2.id IS NOT NULL,1,0),1) AND IF(p3.id IS NOT NULL,IF(afas3.id IS NOT NULL,1,0),1) AND IF(p4.id IS NOT NULL,IF(afas4.id IS NOT NULL,1,0),1) AND IF(p5.id IS NOT NULL,IF(afas5.id IS NOT NULL,1,0),1) AND IF(p6.id IS NOT NULL,IF(afas6.id IS NOT NULL,1,0),1) AND IF(p7.id IS NOT NULL,IF(afas7.id IS NOT NULL,1,0),1) AND IF(p8.id IS NOT NULL,IF(afas8.id IS NOT NULL,1,0),1) AND IF(p9.id IS NOT NULL,IF(afas9.id IS NOT NULL,1,0),1) AND IF(p10.id IS NOT NULL,IF(afas10.id IS NOT NULL,1,0),1) AND (afae.id IS NULL OR afae.dateTime < afa.respSigningDatetime OR afae.dateTime < afa.orgSigningDatetime OR afae.dateTime < afas.signingDatetime OR afae.dateTime < afas2.signingDatetime  OR afae.dateTime < afas3.signingDatetime OR afae.dateTime < afas4.signingDatetime OR afae.dateTime < afas5.signingDatetime OR afae.dateTime < afas6.signingDatetime OR afae.dateTime < afas7.signingDatetime OR afae.dateTime < afas8.signingDatetime OR afae.dateTime < afas9.signingDatetime OR afae.dateTime < afas10.signingDatetime) '
        elif details == 2:
            detail = u' AND afa.orgSigner_id IS NOT NULL AND (afa.respSigner_id IS  NULL OR IF(p.id  IS NOT NULL,IF(afas.id  IS NULL,1,0),0) OR IF(p2.id IS NOT NULL,IF(afas2.id IS NULL,1,0),0) OR IF(p3.id IS NOT NULL,IF(afas3.id IS NULL,1,0),0) OR IF(p4.id IS NOT NULL,IF(afas4.id IS NULL,1,0),0) OR IF(p5.id IS NOT NULL,IF(afas5.id IS NULL,1,0),0) OR IF(p6.id IS NOT NULL,IF(afas6.id IS NULL,1,0),0) OR IF(p7.id IS NOT NULL,IF(afas7.id IS NULL,1,0),0) OR IF(p8.id IS NOT NULL,IF(afas8.id IS NULL,1,0),0) OR IF(p9.id IS NOT NULL,IF(afas9.id IS NULL,1,0),0) OR IF(p10.id IS NOT NULL,IF(afas10.id IS NULL,1,0),0) ) '
        elif details == 3:
            detail = u' and afae.success = 1 '
        else:
            detail = u''

        if detalSign:
            group = ''
        else:
            group = 'GROUP BY a.id'

        if groupOrganisation:
            order = 'ORDER BY os.name'
        else:
            order = ''

        if orgStructureId:
            orgStructureIdList = getOrgStructureDescendants(orgStructureId)
            orgStructureList = u' and p_action.orgStructure_id in (%s)' % (','.join(map(str, orgStructureIdList)))
        else:
            orgStructureList = u''
        if not endDate or endDate.isNull():
            return None
        db = QtGui.qApp.db
        stmt = u'''  
                SELECT e.client_id ,formatClientName(e.client_id) AS fio,e.id,date(a.endDate) AS endDate,
                os.name,concat(p_action.lastName,' ',p_action.firstName,' ',p_action.patrName) AS person,afa.respSigningDatetime,
                afa.respSigner_name, afa.orgSigningDatetime, afae.dateTime, IF(afae.success=1,'успех',IF(afae.success=0,'ошибка','отсутствует')) AS success, 
                  formatPersonName(p.id) AS person_id1 , afas.signingDatetime AS afas1, afas.signerTitle AS signerTitle1,
                  formatPersonName(p2.id) AS person_id2, afas2.signingDatetime AS afas2, afas2.signerTitle AS signerTitle2,
                  formatPersonName(p3.id) AS person_id3, afas3.signingDatetime AS afas3, afas3.signerTitle AS signerTitle3,
                  formatPersonName(p4.id) AS person_id4, afas4.signingDatetime AS afas4, afas4.signerTitle AS signerTitle4,
                  formatPersonName(p5.id) AS person_id5, afas5.signingDatetime AS afas5, afas5.signerTitle AS signerTitle5,
                  formatPersonName(p6.id) AS person_id6, afas6.signingDatetime AS afas6, afas6.signerTitle AS signerTitle6,
                  formatPersonName(p7.id) AS person_id7, afas7.signingDatetime AS afas7, afas7.signerTitle AS signerTitle7,
                  formatPersonName(p8.id) AS person_id8, afas8.signingDatetime AS afas8, afas8.signerTitle AS signerTitle8,
                  formatPersonName(p9.id) AS person_id9, afas9.signingDatetime AS afas9, afas9.signerTitle AS signerTitle9,
                  formatPersonName(p10.id) AS person_id10, afas10.signingDatetime AS afas10, afas10.signerTitle AS signerTitle10
FROM Action a

  LEFT JOIN Event e ON a.event_id = e.id

  INNER JOIN ActionType at ON at.id = a.actionType_id

  inner  JOIN Action_FileAttach afa ON afa.master_id = a.id AND afa.deleted = 0 AND afa.path LIKE '%%.xml' AND afa.id = (SELECT MAX(id) FROM Action_FileAttach WHERE deleted=0 AND master_id = a.id)

  LEFT JOIN ActionPropertyType apt ON at.id = apt.actionType_id AND apt.typeName="Person" AND apt.valueDomain like '%%signer%%' AND apt.name='Член врачебной комиссии 1'
  LEFT JOIN ActionProperty ap ON a.id = ap.action_id AND apt.id = ap.type_id AND ap.deleted=0
  LEFT JOIN ActionProperty_Person app ON ap.id = app.id
                   LEFT JOIN Person p ON app.value=p.id
                   LEFT JOIN Action_FileAttach_Signature afas ON p.id = afas.signer_id AND afa.id = afas.master_id

LEFT JOIN ActionPropertyType apt2 ON at.id = apt2.actionType_id AND apt2.typeName="Person" AND apt2.valueDomain like '%%signer%%' AND apt2.name='Член врачебной комиссии 2'
  LEFT JOIN ActionProperty ap2 ON a.id = ap2.action_id AND apt2.id = ap2.type_id AND ap2.deleted=0
  LEFT JOIN ActionProperty_Person app2 ON ap2.id = app2.id
                   LEFT JOIN Person p2 ON app2.value=p2.id
                   LEFT JOIN Action_FileAttach_Signature afas2 ON p2.id = afas2.signer_id AND afa.id = afas2.master_id

LEFT JOIN ActionPropertyType apt3 ON at.id = apt3.actionType_id AND apt3.typeName="Person" AND apt3.valueDomain like '%%signer%%' AND apt3.name='Член врачебной комиссии 3'
  LEFT JOIN ActionProperty ap3 ON a.id = ap3.action_id AND apt3.id = ap3.type_id AND ap3.deleted=0
  LEFT JOIN ActionProperty_Person app3 ON ap3.id = app3.id
                  LEFT JOIN Person p3 ON app3.value=p3.id
                  LEFT JOIN Action_FileAttach_Signature afas3 ON p3.id = afas3.signer_id AND afa.id = afas3.master_id

LEFT JOIN ActionPropertyType apt4 ON at.id = apt4.actionType_id AND apt4.typeName="Person" AND apt4.valueDomain like '%%signer%%' AND apt4.name='Член врачебной комиссии 4'
  LEFT JOIN ActionProperty ap4 ON a.id = ap4.action_id AND apt4.id = ap4.type_id AND ap4.deleted=0
  LEFT JOIN ActionProperty_Person app4 ON ap4.id = app4.id
                  LEFT JOIN Person p4 ON app4.value=p4.id
                  LEFT JOIN Action_FileAttach_Signature afas4 ON p4.id = afas4.signer_id AND afa.id = afas4.master_id

LEFT JOIN ActionPropertyType apt5 ON at.id = apt5.actionType_id AND apt5.typeName="Person" AND apt5.valueDomain like '%%signer%%' AND apt5.name='Член врачебной комиссии 5'
  LEFT JOIN ActionProperty ap5 ON a.id = ap5.action_id AND apt5.id = ap5.type_id AND ap5.deleted=0
  LEFT JOIN ActionProperty_Person app5 ON ap5.id = app5.id
                  LEFT JOIN Person p5 ON app5.value=p5.id
                  LEFT JOIN Action_FileAttach_Signature afas5 ON p5.id = afas5.signer_id AND afa.id = afas5.master_id

LEFT JOIN ActionPropertyType apt6 ON at.id = apt6.actionType_id AND apt6.typeName="Person" AND apt6.valueDomain like '%%signer%%' AND apt6.name='Член врачебной комиссии 6'
  LEFT JOIN ActionProperty ap6 ON a.id = ap6.action_id AND apt6.id = ap6.type_id AND ap6.deleted=0
  LEFT JOIN ActionProperty_Person app6 ON ap6.id = app6.id
                  LEFT JOIN Person p6 ON app6.value=p6.id
                  LEFT JOIN Action_FileAttach_Signature afas6 ON p6.id = afas6.signer_id AND afa.id = afas6.master_id

LEFT JOIN ActionPropertyType apt7 ON at.id = apt7.actionType_id AND apt7.typeName="Person" AND apt7.valueDomain like '%%signer%%' AND apt7.name='Член врачебной комиссии 7'
  LEFT JOIN ActionProperty ap7 ON a.id = ap7.action_id AND apt7.id = ap7.type_id AND ap7.deleted=0
  LEFT JOIN ActionProperty_Person app7 ON ap7.id = app7.id
                  LEFT JOIN Person p7 ON app7.value=p7.id
                  LEFT JOIN Action_FileAttach_Signature afas7 ON p7.id = afas7.signer_id AND afa.id = afas7.master_id

LEFT JOIN ActionPropertyType apt8 ON at.id = apt8.actionType_id AND apt8.typeName="Person" AND apt8.valueDomain like '%%signer%%' AND apt8.name='Член врачебной комиссии 8'
  LEFT JOIN ActionProperty ap8 ON a.id = ap8.action_id AND apt8.id = ap8.type_id AND ap8.deleted=0
  LEFT JOIN ActionProperty_Person app8 ON ap8.id = app8.id
                  LEFT JOIN Person p8 ON app8.value=p8.id
                  LEFT JOIN Action_FileAttach_Signature afas8 ON p8.id = afas8.signer_id AND afa.id = afas8.master_id

LEFT JOIN ActionPropertyType apt9 ON at.id = apt9.actionType_id AND apt9.typeName="Person" AND apt9.valueDomain like '%%signer%%' AND apt9.name='Член врачебной комиссии 9'
  LEFT JOIN ActionProperty ap9 ON a.id = ap9.action_id AND apt9.id = ap9.type_id AND ap9.deleted=0
  LEFT JOIN ActionProperty_Person app9 ON ap9.id = app9.id
                  LEFT JOIN Person p9 ON app9.value=p9.id
                  LEFT JOIN Action_FileAttach_Signature afas9 ON p9.id = afas9.signer_id AND afa.id = afas9.master_id

LEFT JOIN ActionPropertyType apt10 ON at.id = apt10.actionType_id AND apt10.typeName="Person" AND apt10.valueDomain like '%%signer%%' AND apt10.name='Член врачебной комиссии 10'
  LEFT JOIN ActionProperty ap10 ON a.id = ap10.action_id AND apt10.id = ap10.type_id AND ap10.deleted=0
  LEFT JOIN ActionProperty_Person app10 ON ap10.id = app10.id
                  LEFT JOIN Person p10 ON app10.value=p10.id
                  LEFT JOIN Action_FileAttach_Signature afas10 ON p10.id = afas10.signer_id AND afa.id = afas10.master_id


  LEFT JOIN Person p_action ON a.person_id = p_action.id

  LEFT JOIN OrgStructure os ON p_action.orgStructure_id = os.id
  
  LEFT JOIN Action_FileAttach_Export afae ON afae.id = (SELECT id FROM Action_FileAttach_Export afae WHERE afa.id=afae.master_id ORDER BY afae.dateTime DESC LIMIT 1)

WHERE at.flatCode = 'inspection_mse'  
-- AND apt.deleted=0 
  AND at.deleted=0 AND a.deleted=0
  AND a.endDate BETWEEN DATE(%(begDate)s) AND DATE(%(endDate)s) 
-- AND app.id IS NOT NULL
/*
AND afa.createDatetime IN ( SELECT MAX(Action_FileAttach.createDatetime) 
                                            FROM Action 
                                            INNER JOIN Action_FileAttach ON Action_FileAttach.master_id=Action.id and Action_FileAttach.path LIKE '%%.xml'
                                            WHERE Action.event_id=a.event_id 
                                            GROUP BY master_id )
*/
%(orgStructureList)s

%(detail)s
%(order)s

 -- AND a.event_id=1949328
;
               ''' % {'begDate': db.formatDate(begDate),
                      'endDate': db.formatDate(endDate),
                      'orgStructureList': orgStructureList,
                      'detail': detail,
                      'order': order
                      }
        return db.query(stmt)

    def getDescription(self, params):
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        detalSign = params.get('diagnosisType', False)
        details = params.get('eventStatus', 0)
        orgStructureId = params.get('orgStructureId', None)
        rows = []
        rows.append(dateRangeAsStr(u'за период', begDate, endDate))

        if details == 0:
            rows.append(u'детализировать по: требуют подписи МО')
        elif details == 1:
            rows.append(u'детализировать по: готовы к отправке')
        elif details == 2:
            rows.append(u'детализировать по: без подписания ЧК')
        elif details == 3:
            rows.append(u'детализировать по: отправленные')
        else:
            rows.append(u'детализировать по: всем')

        if detalSign:
            rows.append(u'расширить информацию по подписям')

        if orgStructureId:
            rows.append(u'по отделению: %s ' % (getOrgStructureName(orgStructureId)))

        rows.append(u'отчёт составлен: ' + forceString(QDateTime.currentDateTime()))
        return rows

    def build(self, params):
        detalSign = params.get('diagnosisType', False)
        groupOrganisation = params.get('groupOrganisation', False)
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.setBlockFormat(CReportBase.AlignCenter)
        # cursor.insertText(u'Успешно принятые документы на федеральном уровне')
        cursor.insertBlock()
        cursor.insertBlock()

        tableColumns = [
            ('3%', [u'№'], CReportBase.AlignCenter),
            ('5%', [u'код пациента'], CReportBase.AlignCenter),
            ('10%', [u'фио пациента'], CReportBase.AlignRight),
            ('4%', [u'код карточки'], CReportBase.AlignCenter),
            ('10%', [u'дата направления (окончание действия)'], CReportBase.AlignRight),
            ('10%', [u'подразделение (по исполнителю)'], CReportBase.AlignRight),
            ('10%', [u'исполнитель'], CReportBase.AlignRight),
            ('10%', [u'дата подписания исполнитетем'], CReportBase.AlignRight),
            ('15%', [u'данные ЭЦП, подписавшего за исполнителя'], CReportBase.AlignRight),
            ('10%', [u'дата подписания МО'], CReportBase.AlignRight),
            ('10%', [u'дата последнего экспорта'], CReportBase.AlignRight),
            ('5%', [u'успешность экспорта'], CReportBase.AlignRight)
        ]

        table = createTable(cursor, tableColumns)

        query = self.selectData(params)
        old_Structure = ''

        tempIndex = 0
        while query.next():
            record = query.record()
            client = forceInt(record.value('client_id'))
            if client:
                fio = forceString(record.value('fio'))
                event_id = forceInt(record.value('id'))
                endDate = forceString(record.value('endDate'))
                name = forceString(record.value('name'))
                person = forceString(record.value('person'))
                respSigningDatetime = forceString(record.value('respSigningDatetime'))
                respSigner_name = forceString(record.value('respSigner_name'))
                orgSigningDatetime = forceString(record.value('orgSigningDatetime'))
                dateTime = forceString(record.value('dateTime'))
                success = forceString(record.value('success'))
                signs_array = []
                person_id1 = forceString(record.value('person_id1'))
                if len(person_id1) > 1:
                    signs_array.append([forceString(record.value('person_id1')), forceString(record.value('afas1')), forceString(record.value('signerTitle1'))])
                person_id2 = forceString(record.value('person_id2'))
                if len(person_id2) > 1:
                    signs_array.append([forceString(record.value('person_id2')), forceString(record.value('afas2')), forceString(record.value('signerTitle2'))])
                person_id3 = forceString(record.value('person_id3'))
                if len(person_id3) > 1:
                    signs_array.append([forceString(record.value('person_id3')), forceString(record.value('afas3')), forceString(record.value('signerTitle3'))])
                person_id4 = forceString(record.value('person_id4'))
                if len(person_id4) > 1:
                    signs_array.append([forceString(record.value('person_id4')), forceString(record.value('afas4')), forceString(record.value('signerTitle4'))])
                person_id5 = forceString(record.value('person_id5'))
                if len(person_id5) > 1:
                    signs_array.append([forceString(record.value('person_id5')), forceString(record.value('afas5')), forceString(record.value('signerTitle5'))])
                person_id6 = forceString(record.value('person_id6'))
                if len(person_id6) > 1:
                    signs_array.append([forceString(record.value('person_id6')), forceString(record.value('afas6')), forceString(record.value('signerTitle6'))])
                person_id7 = forceString(record.value('person_id7'))
                if len(person_id7) > 1:
                    signs_array.append([forceString(record.value('person_id7')), forceString(record.value('afas7')), forceString(record.value('signerTitle7'))])
                person_id8 = forceString(record.value('person_id8'))
                if len(person_id8) > 1:
                    signs_array.append([forceString(record.value('person_id8')), forceString(record.value('afas8')), forceString(record.value('signerTitle8'))])
                person_id9 = forceString(record.value('person_id9'))
                if len(person_id9) > 1:
                    signs_array.append([forceString(record.value('person_id9')), forceString(record.value('afas9')), forceString(record.value('signerTitle9'))])
                person_id10 = forceString(record.value('person_id10'))
                if len(person_id10) > 1:
                    signs_array.append([forceString(record.value('person_id10')), forceString(record.value('afas10')), forceString(record.value('signerTitle10'))])

                tempIndex += 1

                if old_Structure != name and groupOrganisation:
                    old_Structure = name

                    row = table.addRow()
                    table.mergeCells(row, 0, row, 11)
                    table.setText(row, 0, name)

                row = table.addRow()
                table.setText(row, 0, tempIndex)
                table.setText(row, 1, client)
                table.setText(row, 2, fio)
                table.setHtml(row, 3, u"<a href='event_" + str(event_id) + u"'><span style='color: rgb(FF, FF, FF);'>" + str(event_id) + "</span></a>")
                table.setText(row, 4, endDate)
                table.setText(row, 5, name)
                table.setText(row, 6, person)
                table.setText(row, 7, respSigningDatetime)
                table.setText(row, 8, respSigner_name)
                table.setText(row, 9, orgSigningDatetime)
                table.setText(row, 10, dateTime)
                table.setText(row, 11, success)

                temp_row = row
                check = False

                if detalSign:
                    for i, sign in enumerate((person_id1, person_id2, person_id3, person_id4, person_id5, person_id6, person_id7, person_id8, person_id9, person_id10)):
                        if sign and sign != 0:
                            row = table.addRow()
                            table.mergeCells(row, 0, row, 6)
                            table.setText(row, 6, sign)
                            table.setText(row, 7, signs_array[i][1])
                            table.setText(row, 8, signs_array[i][2])
                            table.mergeCells(row, 9, row, 3)
                            check = True
                    if check:
                        table.mergeCells(temp_row + 1, 0, row, 6)

        return doc
