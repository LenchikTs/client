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
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtCore import QDate

from library.Utils       import forceString
from library.DialogBase  import CDialogBase
from Reports.Report      import CReport
from Reports.ReportBase  import CReportBase, createTable
from Orgs.Utils import getOrgStructureDescendants
from Reports.Ui_ReportVaccineTuberculin import Ui_ReportVaccineJournalSetup


def selectDataVaccination(params):
    db = QtGui.qApp.db

    begDate = params.get('begDate').toString('yyyy-MM-dd')
    endDate = params.get('endDate').toString('yyyy-MM-dd')

    ageFrom = params.get('ageFrom', 0)
    ageTo   = params.get('ageTo', 150)

    personId = params.get('personId')

    socStatusClassId = params.get('socStatusClassId', None)
    socStatusTypeId = params.get('socStatusTypeId', None)

    orgStructureId = params.get('orgStructureId') # Подразделения
    orgStructureRegion = params.get('cmbOrgStructureRegion') # Участок прикрепления

    chkgroupfordivision = params.get('chkgroupfordivision') # группировать по подразделениям
    chkgroupforperson = params.get('chkgroupforperson') # группировать по врачам


    condorgStructureId = u''
    condorgStructureRegion = u''
    condpersonId = u''
    condsocStatusClassId = u''
    condsocStatusTypeId = u''
    condGroupOrder = u''

    if orgStructureId:
        condorgStructureId = "\nAND (OrgStructure.`id` IN ({0}))".format(", ".join(map(str, getOrgStructureDescendants(orgStructureId))))

    if orgStructureRegion:
        condorgStructureRegion = "\nAND (attach.`id` IN ({0}))".format(", ".join(map(str, getOrgStructureDescendants(orgStructureRegion))))

    if personId:
        condpersonId = "\nAND (Person.`id` = {0})".format(personId)

    if socStatusClassId:
        condsocStatusClassId = """
    AND (EXISTS (SELECT
    ClientSocStatus.id
    FROM ClientSocStatus
    WHERE ClientSocStatus.deleted = 0
    AND ClientSocStatus.client_id = Client.id
    AND ClientSocStatus.socStatusClass_id = %s))""" % (socStatusClassId)

    if socStatusTypeId:
        condsocStatusTypeId = """
    AND (EXISTS (SELECT
    ClientSocStatus.id
    FROM ClientSocStatus
    WHERE ClientSocStatus.deleted = 0
    AND ClientSocStatus.client_id = Client.id
    AND ClientSocStatus.socStatusType_id = %s))""" % (socStatusTypeId)


    # Без группировок
    if chkgroupfordivision == False and chkgroupforperson == False:
        condGroupOrder = "\nGROUP BY q.VaccineName \nORDER BY q.VaccineName"
    # Группируем по врачам
    elif chkgroupfordivision == False and chkgroupforperson == True:
        condGroupOrder = "\nGROUP BY q.fio, q.VaccineName \nORDER BY q.fio, q.VaccineName"
    # Группируем по подразделениям
    elif chkgroupfordivision == True and chkgroupforperson == False:
        condGroupOrder = "\nGROUP BY q.orgName, q.VaccineName \nORDER BY q.orgName, q.VaccineName"
    # Группируем по подразделениям и врачам
    elif chkgroupfordivision == True and chkgroupforperson == True:
        condGroupOrder = "\nGROUP BY q.orgName, q.fio, q.VaccineName \nORDER BY q.orgName, q.fio, q.VaccineName"


    stmt = """
SELECT COUNT(q.client_id) as ccount,q.VaccineName,q.fio, q.orgName   FROM(

SELECT
DISTINCT ClientVaccination.id AS vacc,
  ClientVaccination.client_id,
  Person.id ,
  CONCAT(Person.lastName,' ',Person.firstName,' ',Person.patrName) AS fio,
  rbVaccine.`name` AS VaccineName,
  OrgStructure.`name` AS `orgName`
FROM Person
  LEFT JOIN ClientVaccination
    ON ClientVaccination.`person_id` = Person.`id`
  LEFT JOIN Client
    ON Client.`id` = ClientVaccination.`client_id`
  LEFT JOIN ClientSocStatus
    ON ClientSocStatus.`client_id` = ClientVaccination.`client_id` AND ClientSocStatus.`deleted` = 0
  LEFT JOIN rbSocStatusClass
    ON rbSocStatusClass.`id` = ClientSocStatus.`socStatusClass_id`
  LEFT JOIN rbSocStatusType
    ON rbSocStatusType.`id` = ClientSocStatus.`socStatusType_id`
  LEFT JOIN OrgStructure
    ON Person.`orgStructure_id` = OrgStructure.`id`
  LEFT JOIN rbVaccine
    ON rbVaccine.`id` = ClientVaccination.`vaccine_id`
  LEFT join ClientAttach ca on ca.id = (
                          SELECT MAX(ClientAttach.id)
                                FROM ClientAttach
                                INNER JOIN rbAttachType ON rbAttachType.id = ClientAttach.attachType_id
                                WHERE client_id = Client.id
                                  AND ClientAttach.deleted = 0
                                  AND NOT rbAttachType.TEMPORARY)
   LEFT JOIN OrgStructure as attach  ON ca.orgStructure_id = attach.id                               
WHERE (Person.`deleted` = 0)
AND (ClientVaccination.`deleted` = 0)
AND (Client.`deleted` = 0)

AND (OrgStructure.`deleted` = 0)
%(orgStructureId)s
%(orgStructureRegion)s
%(personId)s
%(socStatusClassId)s
%(socStatusTypeId)s

AND (age(Client.birthDate, ClientVaccination.dateTime) BETWEEN %(ageFrom)s AND %(ageTo)s)
AND (DATE(ClientVaccination.`dateTime`) >= DATE('%(begDate)sT00:00:00'))
AND (DATE(ClientVaccination.`dateTime`) <= DATE('%(endDate)sT00:00:00'))

UNION ALL

  SELECT
  DISTINCT ClientVaccinationProbe.id as vaccp,
  ClientVaccinationProbe.client_id,
  Person.`id`,
  CONCAT(Person.lastName,' ',Person.firstName,' ',Person.patrName) AS fio,
  rbVaccinationProbe.`name` AS `VaccineProbeName`,
  OrgStructure.`name` AS `orgName`
FROM Person
  LEFT JOIN ClientVaccinationProbe
    ON ClientVaccinationProbe.`person_id` = Person.`id`
  LEFT JOIN Client
    ON Client.`id` = ClientVaccinationProbe.`client_id`
  LEFT JOIN ClientSocStatus
    ON ClientSocStatus.`client_id` = ClientVaccinationProbe.`client_id` AND ClientSocStatus.`deleted` = 0
  LEFT JOIN rbSocStatusClass
    ON rbSocStatusClass.`id` = ClientSocStatus.`socStatusClass_id`
  LEFT JOIN rbSocStatusType
    ON rbSocStatusType.`id` = ClientSocStatus.`socStatusType_id`
  LEFT JOIN OrgStructure
    ON Person.`orgStructure_id` = OrgStructure.`id`
  LEFT JOIN rbVaccinationProbe
    ON rbVaccinationProbe.`id` = ClientVaccinationProbe.`probe_id`
  LEFT join ClientAttach ca on ca.id = (
                          SELECT MAX(ClientAttach.id)
                                FROM ClientAttach
                                INNER JOIN rbAttachType ON rbAttachType.id = ClientAttach.attachType_id
                                WHERE client_id = Client.id
                                  AND ClientAttach.deleted = 0
                                  AND NOT rbAttachType.TEMPORARY)
  LEFT JOIN OrgStructure as attach  ON ca.orgStructure_id = attach.id
WHERE (Person.`deleted` = 0)
AND (ClientVaccinationProbe.`deleted` = 0)
AND (Client.`deleted` = 0)

AND (OrgStructure.`deleted` = 0) 
%(orgStructureId)s
%(orgStructureRegion)s
%(personId)s
%(socStatusClassId)s
%(socStatusTypeId)s

AND (age(Client.birthDate, ClientVaccinationProbe.dateTime) BETWEEN %(ageFrom)s AND %(ageTo)s)
AND (DATE(ClientVaccinationProbe.`dateTime`) >= DATE('%(begDate)sT00:00:00'))
AND (DATE(ClientVaccinationProbe.`dateTime`) <= DATE('%(endDate)sT00:00:00'))
)q

%(GroupOrder)s

    """ % {
        'orgStructureId': condorgStructureId,
        'orgStructureRegion': condorgStructureRegion,
        'personId': condpersonId,
        'socStatusClassId': condsocStatusClassId,
        'socStatusTypeId': condsocStatusTypeId,
        'ageFrom': ageFrom,
        'ageTo': ageTo,
        'begDate': begDate,
        'endDate': endDate,
        'GroupOrder': condGroupOrder
    }


    return_table = []
    list_fio = []
    list_orgName = []

    num_all_vaccine = 0 # Количество всех вакцин
    num_person = 0 # Количество прививок у врача
    num_org = 0 # Количество прививок у организации
    old_fio = '' # ФИО Врача
    old_orgName = '' # название организации


    query = db.query(stmt)
    while query.next():
        record = query.record()

        ccount = forceString(record.value('ccount'))
        VaccineName = forceString(record.value('VaccineName'))
        fio = forceString(record.value('fio'))
        orgName = forceString(record.value('orgName'))

        tab = [] # Столбик 1|Столбак 2|Шрифт жирный/Нет

        # Без группировок
        if chkgroupfordivision == False and chkgroupforperson == False:
            tab.append(VaccineName)
            tab.append(ccount)
            tab.append(False)

            num_all_vaccine += int(ccount)

        # Группируем по врачам
        elif chkgroupfordivision == False and chkgroupforperson == True:
            if fio not in list_fio:
                if list_fio != []:
                    tab = []
                    tab.append(u'Всего у ' +  unicode(old_fio))
                    tab.append(num_person)
                    tab.append(False)
                    return_table.append(tab)

                    num_person = 0

                    tab = []
                    tab.append(u'   ')
                    tab.append(u'   ')
                    tab.append(False)
                    return_table.append(tab)

                list_fio.append(fio)

                tab = []
                tab.append(fio)
                tab.append(u"   ")
                tab.append(True)
                return_table.append(tab)

                tab = []
                tab.append(VaccineName)
                tab.append(ccount)
                tab.append(False)

                num_person += int(ccount)
                num_all_vaccine += int(ccount)
                old_fio = fio
            else:
                tab.append(VaccineName)
                tab.append(ccount)
                tab.append(False)

                num_person += int(ccount)
                num_all_vaccine += int(ccount)
                old_fio = fio

        # Группируем по подразделениям
        elif chkgroupfordivision == True and chkgroupforperson == False:
            if orgName not in list_orgName:
                if list_orgName != []:
                    tab = []
                    tab.append(u'Всего по ' + unicode(old_orgName))
                    tab.append(num_org)
                    tab.append(False)
                    return_table.append(tab)

                    num_org = 0

                    tab = []
                    tab.append(u'   ')
                    tab.append(u'   ')
                    tab.append(False)
                    return_table.append(tab)

                list_orgName.append(orgName)

                tab = []
                tab.append(orgName)
                tab.append(u'    ')
                tab.append(True)
                return_table.append(tab)

                tab = []
                tab.append(VaccineName)
                tab.append(ccount)
                tab.append(False)

                num_org += int(ccount)
                num_all_vaccine += int(ccount)

                old_orgName = orgName
            else:
                tab.append(VaccineName)
                tab.append(ccount)
                tab.append(False)

                num_org += int(ccount)
                num_all_vaccine += int(ccount)

        # Группируем по подразделениям и врачам
        elif chkgroupfordivision == True and chkgroupforperson == True:
            if orgName not in list_orgName:
                if list_orgName != []:
                    tab = []
                    tab.append(u'Всего у ' + unicode(old_fio))
                    tab.append(num_person)
                    tab.append(False)
                    return_table.append(tab)

                    num_person = 0

                    tab = []
                    tab.append(u'Всего по ' + unicode(old_orgName))
                    tab.append(num_org)
                    tab.append(False)
                    return_table.append(tab)

                    num_org = 0

                    tab = []
                    tab.append(u'   ')
                    tab.append(u'   ')
                    tab.append(False)
                    return_table.append(tab)

                list_orgName.append(orgName)

                tab = []
                tab.append(orgName)
                tab.append(u'    ')
                tab.append(True)
                return_table.append(tab)

                tab = []
                tab.append(u'   ')
                tab.append(u'   ')
                tab.append(False)
                return_table.append(tab)

                old_orgName = orgName


                if fio not in list_fio:
                    list_fio.append(fio)

                    tab = []
                    tab.append(u'   ')
                    tab.append(u'   ')
                    tab.append(False)
                    return_table.append(tab)

                    tab = []
                    tab.append(fio)
                    tab.append(u'    ')
                    tab.append(True)
                    return_table.append(tab)

                    tab = []
                    tab.append(VaccineName)
                    tab.append(ccount)
                    tab.append(False)
                    num_person += int(ccount)
                    num_org += int(ccount)
                    num_all_vaccine += int(ccount)

                    old_fio = fio
                else:
                    tab.append(VaccineName)
                    tab.append(ccount)
                    tab.append(False)
                    num_person += int(ccount)
                    num_org += int(ccount)
                    num_all_vaccine += int(ccount)

            else:
                if fio not in list_fio:
                    if list_fio != []:
                        tab = []
                        tab.append(u'Всего у ' + unicode(old_fio))
                        tab.append(num_person)
                        tab.append(False)
                        return_table.append(tab)

                        num_person = 0

                    list_fio.append(fio)

                    tab = []
                    tab.append(u'   ')
                    tab.append(u'   ')
                    tab.append(False)
                    return_table.append(tab)

                    tab = []
                    tab.append(fio)
                    tab.append(u'    ')
                    tab.append(True)
                    return_table.append(tab)

                    tab = []
                    tab.append(VaccineName)
                    tab.append(ccount)
                    tab.append(False)

                    num_person += int(ccount)
                    num_org += int(ccount)
                    num_all_vaccine += int(ccount)

                    old_fio = fio
                else:
                    tab.append(VaccineName)
                    tab.append(ccount)
                    tab.append(False)

                    num_person += int(ccount)
                    num_org += int(ccount)
                    num_all_vaccine += int(ccount)

        if tab != []:
            return_table.append(tab)


    # Без группировок
    if chkgroupfordivision == False and chkgroupforperson == False:
        pass

    # Группируем по врачам
    elif chkgroupfordivision == False and chkgroupforperson == True:
        tab = []
        tab.append(u'Всего у ' + unicode(old_fio) + ':')
        tab.append(num_person)
        tab.append(False)
        return_table.append(tab)

        num_person = 0

    # Группируем по подразделениям
    elif chkgroupfordivision == True and chkgroupforperson == False:
        tab = []
        tab.append(u'Всего по ' + unicode(old_orgName) + ':')
        tab.append(num_org)
        tab.append(False)
        return_table.append(tab)

        num_org = 0

    # Группируем по подразделениям и врачам
    elif chkgroupfordivision == True and chkgroupforperson == True:
        tab = []
        tab.append(u'Всего у ' + unicode(old_fio) + ':')
        tab.append(num_person)
        tab.append(False)
        return_table.append(tab)

        num_person = 0

        tab = []
        tab.append(u'Всего по ' + unicode(old_orgName) + ':')
        tab.append(num_org)
        tab.append(False)
        return_table.append(tab)

        num_org = 0


    tab = []
    tab.append(u'   ')
    tab.append(u'   ')
    tab.append(False)
    return_table.append(tab)


    tab = []
    tab.append(u"Всего вакицн:")
    tab.append(num_all_vaccine)
    tab.append(False)
    return_table.append(tab)

    return return_table



class CReportVaccineAndTuberculinTestJournal(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Отчет о профилактических прививках и туберкулиновых пробах')


    def getSetupDialog(self, parent):
        result = CReportVaccineJournalSetup(parent)
        result.setWindowTitle(self.title())
        return result


    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        chkgroupfordivision = params.get('chkgroupfordivision')  # группировать по подразделениям
        chkgroupforperson = params.get('chkgroupforperson')  # группировать по врачам

        # Без группировок
        if chkgroupfordivision == False and chkgroupforperson == False:
            title = u'Группировка по прививкам'
        # Группируем по врачам # Готово
        elif chkgroupfordivision == False and chkgroupforperson == True:
            title = u'Группировка по врачам'
        # Группируем по подразделениям # Готово
        elif chkgroupfordivision == True and chkgroupforperson == False:
            title = u'Группировка по подразделениям'
        # Группируем по подразделениям и врачам
        elif chkgroupfordivision == True and chkgroupforperson == True:
            title = u'Группировка по подразделениям и врачам'

        # title
        tableColumns = [
            ('90%',  [title], CReportBase.AlignLeft),
            ('10%', [u'Кол-во привитых пациентов'], CReportBase.AlignLeft)
        ]
        table = createTable(cursor, tableColumns)

        list_table = selectDataVaccination(params)

        for tab in list_table:
            row = table.addRow()
            table.setText(row, 0, forceString(tab[0]), fontBold=tab[2])
            table.setText(row, 1, forceString(tab[1]), fontBold=tab[2])

        return doc



class CReportVaccineJournalSetup(CDialogBase, Ui_ReportVaccineJournalSetup):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())

        self.cmbSocStatusType.setTable('vrbSocStatusType', True)


    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['orgStructureId'] = self.cmbOrgStructure.value()
        result['personId'] = self.cmbPerson.value()
        result['ageFrom'] = self.edtAgeFrom.value()
        result['ageTo'] = self.edtAgeTo.value()
        result['socStatusClassId'] = self.cmbSocStatusClass.value()
        result['socStatusTypeId'] = self.cmbSocStatusType.value()
        result['cmbOrgStructureRegion'] = self.cmbOrgStructureRegion.value()
        if self.chkgroupfordivision:
            result['chkgroupfordivision'] = self.chkgroupfordivision.isChecked()
        if self.chkgroupforperson:
            result['chkgroupforperson'] = self.chkgroupforperson.isChecked()
        return result


    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.cmbOrgStructure.setValue(params.get('orgStructureId'))
        self.cmbPerson.setValue(params.get('personId', None))
        self.edtAgeFrom.setValue(params.get('ageFrom', 0))
        self.edtAgeTo.setValue(params.get('ageTo', 150))
        self.cmbSocStatusClass.setValue(params.get('socStatusClassId', None))
        self.cmbSocStatusType.setValue(params.get('socStatusTypeId', None))
        self.cmbOrgStructureRegion.setValue(params.get('cmbOrgStructureRegion'))
        self.chkgroupfordivision.setChecked(bool(params.get('chkgroupfordivision', None)))
        self.chkgroupforperson.setChecked(bool(params.get('chkgroupforperson', None)))


    @pyqtSignature('int')
    def on_cmbSocStatusClass_currentIndexChanged(self, index):
        socStatusClassId = self.cmbSocStatusClass.value()
        filter = ('class_id=%d' % socStatusClassId) if socStatusClassId else ''
        self.cmbSocStatusType.setFilter(filter)

