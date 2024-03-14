# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rights reserved.
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

from Orgs.Utils import getOrgStructurePersonIdList

from Reports.Report import CReport
from Reports.ReportBase import CReportBase, createTable
from Reports.ReportSetupDialog import CReportSetupDialog
from library.Utils import forceInt, forceString


def selectData(params):
    begDate = params.get('begDate', QDate())
    endDate = params.get('endDate', QDate())
    OrgId = params.get('OrgId', None)
    if OrgId:
        condworkOrgId = ' and o.id = %d' % OrgId
    else:
        condworkOrgId = ''
    rbMedicalAidProfileId = params.get('rbMedicalAidProfileId', None)
    if rbMedicalAidProfileId:
        condrbMedicalAidProfileId = ' and map.id = %d' % rbMedicalAidProfileId
    else:
        condrbMedicalAidProfileId = ''
    specialityid = params.get('specialityId', None)
    if specialityid:
        condspecialityid = ' and s.id = %d' % specialityid
    else:
        condspecialityid = ''
    personId = params.get('personId', None)
    if personId:
        condpersonId = ' and p.id = %d' % personId
    else:
        condpersonId = ''
    orgStructureId = params.get('orgStructureId', None)
    condOrgStructure = u''
    if orgStructureId:
        personIdList = getOrgStructurePersonIdList(orgStructureId)
        if personIdList:
            condOrgStructure = u''' AND p.id IN (%s)''' % (u','.join(str(personId) for personId in personIdList if personId))
    db = QtGui.qApp.db
    stmt = u'''SELECT c.id AS ii,concat(c.lastName,' ',c.firstName,' ',c.patrName) AS fio,c.birthDate AS birth,
CONCAT(o.infisCode,' | ',o.shortName) AS organ,CONCAT(map.code,' | ',map.name) AS otdel,DATE(a.begDate) AS napr,
CONCAT(formatPersonName(p.id),' ',s.name) AS pers, IF(ae.externalId, 'да', 'нет') AS reg,
proc.value as stat,a.plannedEndDate AS plan
FROM Action a 
left JOIN ActionType at ON a.actionType_id = at.id
left join ActionPropertyType apt1 on apt1.actionType_id = at.id and apt1.name = 'Куда направляется' and apt1.deleted = 0
left join ActionProperty ap on ap.action_id = a.id and ap.type_id = apt1.id
left join ActionProperty_Organisation sn on sn.id = ap.id
left JOIN Organisation o ON sn.value = o.id
left join ActionPropertyType apt2 on apt2.actionType_id = at.id and apt2.name = 'Профиль' and apt2.deleted = 0
left join ActionProperty ap_fin on ap_fin.action_id = a.id and ap_fin.type_id = apt2.id
left join ActionProperty_Integer fin on fin.id = ap_fin.id
left JOIN rbMedicalAidProfile map ON fin.value = map.id 
left join ActionPropertyType apt3 on apt3.actionType_id = at.id and apt3.name = 'Статус' and apt3.deleted = 0
left join ActionProperty ap_proc on ap_proc.action_id = a.id and ap_proc.type_id = apt3.id
left join ActionProperty_String proc on proc.id = ap_proc.id
left JOIN Event e ON a.event_id = e.id
left JOIN Client c ON e.client_id = c.id
left JOIN Person p ON a.person_id=p.id 
left JOIN rbSpeciality s ON p.speciality_id = s.id
left JOIN rbExternalSystem es ON es.code = 'РЕГИЗ.УО'
LEFT JOIN Action_Export ae on ae.master_id = a.id AND ae.system_id = es.id AND ae.success = 1
WHERE at.flatCode in ('consultationDirection','researchDirection') AND a.deleted=0 AND ap.deleted=0 
AND at.deleted=0 AND c.deleted=0 AND e.deleted=0 AND o.deleted=0 AND p.deleted=0 and DATE(a.begDate) 
BETWEEN DATE(%(begDate)s) AND DATE(%(endDate)s)
%(condOrgStructure)s %(condpersonId)s  %(condworkOrgId)s %(condrbMedicalAidProfileId)s %(condspecialityid)s
    ''' % dict(begDate=db.formatDate(begDate),
               endDate=db.formatDate(endDate),
               condOrgStructure=condOrgStructure,
               condpersonId=condpersonId,
               condrbMedicalAidProfileId=condrbMedicalAidProfileId,
               condspecialityid=condspecialityid,
               condworkOrgId=condworkOrgId
               )
    db = QtGui.qApp.db
    return db.query(stmt)


class CRepJournalNapr(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Сводка об исходящих направлениях (сервис УО)')

    def getSetupDialog(self, parent):
        result = CReportSetupDialog(parent)
        result.setEventTypeVisible(False)
        result.setOnlyPermanentAttachVisible(False)
        result.setTitle(self.title())
        result.setOrgStructureVisible(True)
        result.setWorkOrganisationVisible(True)
        result.setSpecialityVisible(True)
        result.setMedicalAidProfileVisible(True)
        result.setPersonVisible(True)
        result.chkDetailPerson.setVisible(False)
        result.lblWorkOrganisation.setText(u'Направление в')
        for i in xrange(result.gridLayout.count()):
            spacer = result.gridLayout.itemAt(i)
            if isinstance(spacer, QtGui.QSpacerItem):
                itemposition = result.gridLayout.getItemPosition(i)
                if itemposition != (29, 0, 1, 1) and itemposition != (8, 1, 1, 3):
                    result.gridLayout.removeItem(spacer)
        result.resize(400, 10)
        return result

    def build(self, params):
        query = selectData(params)
        query.first()

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertBlock()
        workOrgId = params.get('workOrgId', None)
        if workOrgId:
            params['OrgId'] = workOrgId
            params['workOrgId'] = None
        self.dumpParams(cursor, params)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertBlock()
        cursor.insertBlock()
        tableColumns = [
            ('3%',  [u'№ п/п'], CReportBase.AlignLeft),
            ('5%',  [u'Код пациента'], CReportBase.AlignLeft),
            ('23%', [u'ФИО пациента'], CReportBase.AlignLeft),
            ('6%',  [u'Дата рождения'], CReportBase.AlignLeft),
            ('15%', [u'Направлен в МО'], CReportBase.AlignLeft),
            ('10%', [u'Профиль'], CReportBase.AlignLeft),
            ('6%',  [u'Дата направления'], CReportBase.AlignLeft),
            ('10%', [u'Врач'], CReportBase.AlignLeft),
            ('10%', [u'Регистрация направления в Сервисе УО'], CReportBase.AlignLeft),
            ('10%', [u'Статус направления'], CReportBase.AlignLeft),
            ('8%',  [u'Плановая дата консультации'], CReportBase.AlignLeft),
            ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 1, 1)
        i = 0
        query = selectData(params)
        while query.next():
            record = query.record()
            ii = forceInt(record.value('ii'))
            fio = forceString(record.value('fio'))
            birth = forceString(record.value('birth'))
            organ = forceString(record.value('organ'))
            otdel = forceString(record.value('otdel'))
            napr = forceString(record.value('napr'))
            pers = forceString(record.value('pers'))
            reg = forceString(record.value('reg'))
            stat = forceString(record.value('stat'))
            plan = forceString(record.value('plan'))
            row = table.addRow()
            i += 1
            table.setText(row, 0, i)
            table.setText(row, 1, ii)
            table.setText(row, 2, fio)
            table.setText(row, 3, birth)
            table.setText(row, 4, organ)
            table.setText(row, 5, otdel)
            table.setText(row, 6, napr)
            table.setText(row, 7, pers)
            table.setText(row, 8, reg)
            table.setText(row, 9, stat)
            table.setText(row, 10, plan)
        return doc
