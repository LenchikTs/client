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
from PyQt4.QtCore import pyqtSignature, QDate

from library.Utils      import forceInt, forceString, formatName, formatSex, formatSNILS
from Orgs.Utils         import getOrgStructureDescendants, getOrgStructures
from Orgs.Orgs          import selectOrganisation
from Reports.ReportBase import CReportBase, createTable
from Reports.Report     import CReport, normalizeMKB


def dumpParamsEx(cursor, params):
    date = params['date']
    areaIdEnabled = params.get('areaIdEnabled', False)
    description = [u'на дату %s' % forceString(date)]
    if areaIdEnabled:
        filterAddressType = params.get('filterAddressType', 0)
        description.append(u'Адрес ' + forceString([u'регистрации', u'проживания'][filterAddressType]))
    columns = [ ('100%', [], CReportBase.AlignLeft) ]
    table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
    for i, row in enumerate(description):
        table.setText(i, 0, row)
    cursor.movePosition(QtGui.QTextCursor.End)


def selectData(date, workOrgId, sex, ageFrom, ageTo, areaIdEnabled, areaId, MKBFilter, MKBFrom, MKBTo, personId, isFilterAddressType, filterAddressType):
    stmt=u"""
SELECT DISTINCT
    Client.id, Client.lastName, Client.firstName, Client.patrName, Client.sex, Client.birthDate, Client.SNILS,
    %s
    ClientPolicy.serial    AS policySerial,
    ClientPolicy.number    AS policyNumber,
    formatInsurerName(ClientPolicy.insurer_id) as insurer,
    ClientDocument.serial  AS documentSerial,
    ClientDocument.number  AS documentNumber,
    rbDocumentType.code    AS documentType,
    IF(ClientWork.org_id IS NULL, ClientWork.freeInput, Organisation.shortName) AS workName,
    ClientWork.post AS workPost,
    Diagnosis.MKB,
    Diagnosis.MKBEx
FROM
    Diagnosis
    LEFT JOIN rbDispanser ON rbDispanser.id = Diagnosis.dispanser_id
    LEFT JOIN Diagnostic  ON Diagnostic.diagnosis_id = Diagnosis.id
    LEFT JOIN Client      ON Client.id = Diagnosis.client_id
    %s
    LEFT JOIN ClientPolicy  ON ClientPolicy.client_id = Client.id AND
              ClientPolicy.id = (SELECT MAX(CP.id)
                                 FROM   ClientPolicy AS CP
                                 LEFT JOIN rbPolicyType ON rbPolicyType.id = CP.policyType_id
                                 WHERE  CP.client_id = Client.id
                                 AND    rbPolicyType.name LIKE 'ОМС%%'
                                 AND CP.deleted = 0
                                )
    LEFT JOIN ClientDocument ON ClientDocument.client_id = Client.id AND
              ClientDocument.id = (SELECT MAX(CD.id)
                                 FROM   ClientDocument AS CD
                                 LEFT JOIN rbDocumentType AS rbDT ON rbDT.id = CD.documentType_id
                                 LEFT JOIN rbDocumentTypeGroup AS rbDTG ON rbDTG.id = rbDT.group_id
                                 WHERE  rbDTG.code = '1' AND CD.client_id = Client.id
                                 AND CD.deleted = 0)
    LEFT JOIN rbDocumentType ON rbDocumentType.id = ClientDocument.documentType_id
    LEFT JOIN ClientWork     ON ClientWork.client_id = Client.id
                                AND ClientWork.id = (SELECT MAX(CW.id) FROM ClientWork AS CW WHERE CW.deleted=0 AND CW.client_id=Client.id)
    LEFT JOIN Organisation   ON Organisation.id = ClientWork.org_id
WHERE
    %s
ORDER BY
    Client.lastName, Client.firstName, Client.patrName, Client.birthDate, Client.id
"""
    db = QtGui.qApp.db
    tableDiagnosis       = db.table('Diagnosis')
    tableDiagnostic = db.table('Diagnostic')
    tableClient          = db.table('Client')
    tableClientDispanser = db.table('rbDispanser')
    cond = []
    cond.append(tableDiagnosis['deleted'].eq(0))
    cond.append(tableDiagnostic['deleted'].eq(0))
    cond.append(tableClient['deleted'].eq(0))
    cond.append(tableDiagnosis['mod_id'].isNull())
    cond.append(tableClientDispanser['observed'].eq(1))
    cond.append(tableClient['deathDate'].isNull())
    cond.append(u'''NOT EXISTS(SELECT DC.id
                                          FROM Diagnostic AS DC
                                          INNER JOIN Diagnosis AS DS ON DS.id = DC.diagnosis_id
                                          INNER JOIN rbDispanser AS rbDP ON rbDP.id = DC.dispanser_id
                                          WHERE DC.diagnosis_id = Diagnosis.id AND DC.endDate <= %s AND DC.deleted = 0 AND rbDP.name LIKE '%s')
                                   OR EXISTS(SELECT DC.id
                                          FROM Diagnostic AS DC
                                          INNER JOIN Diagnosis AS DS ON DS.id = DC.diagnosis_id
                                          INNER JOIN rbDispanser AS rbDP ON rbDP.id = DC.dispanser_id
                                          WHERE DC.diagnosis_id = Diagnosis.id AND DC.endDate <= %s AND DC.deleted = 0 AND rbDP.name LIKE '%s')''' % (
    db.formatDate(date), u'%снят%', db.formatDate(date), u'%взят повторно%'))

    if personId:
        cond.append(tableDiagnosis['dispanserPerson_id'].eq(personId))
    if MKBFilter == 1:
        cond.append(tableDiagnosis['MKB'].ge(MKBFrom))
        cond.append(tableDiagnosis['MKB'].le(MKBTo))
    if workOrgId:
        tableClientWork = db.table('ClientWork')
        cond.append(tableClientWork['org_id'].eq(workOrgId))
    if sex:
        cond.append(tableClient['sex'].eq(sex))
    if ageFrom <= ageTo:
        if ageFrom != 0:
            cond.append('Diagnosis.endDate >= ADDDATE(Client.birthDate, INTERVAL %d YEAR)' % ageFrom)
        if ageTo != 150:
            cond.append('Diagnosis.endDate < SUBDATE(ADDDATE(Client.birthDate, INTERVAL %d YEAR),1)' % (ageTo + 1))
    cond.append('''Diagnostic.endDate = (SELECT MAX(DC.endDate)
               FROM Diagnostic AS DC LEFT JOIN rbDispanser AS rbDSP ON rbDSP.id = DC.dispanser_id
               WHERE DC.deleted = 0 AND DC.diagnosis_id = Diagnosis.id AND rbDSP.observed=1 AND Diagnosis.client_id = Client.id
               AND (DC.endDate < %s))''' % (db.formatDate(date.addDays(1))))
    if areaIdEnabled:
        if areaId:
            orgStructureIdList = getOrgStructureDescendants(areaId)
        else:
            orgStructureIdList = getOrgStructures(QtGui.qApp.currentOrgId())
        tableOrgStructureAddress = db.table('OrgStructure_Address')
        tableAddress = db.table('Address')
        subCond = [ tableOrgStructureAddress['master_id'].inlist(orgStructureIdList),
                    tableOrgStructureAddress['house_id'].eq(tableAddress['house_id']),
                  ]
        cond.append(db.existsStmt(tableOrgStructureAddress, subCond))
    if isFilterAddressType:
        if filterAddressType:
            colsAddressType = u'''formatClientAddress(ClientAddress1.id) AS regAddress,'''
            joinAddressType = u''' LEFT JOIN ClientAddress AS ClientAddress1 ON ClientAddress1.client_id = Diagnosis.client_id
                            AND ClientAddress1.id = (SELECT MAX(id) FROM ClientAddress AS CA1 WHERE CA1.Type=1 and CA1.client_id = Diagnosis.client_id AND CA1.deleted = 0)
                            LEFT JOIN Address ON Address.id = ClientAddress1.address_id'''
        else:
            colsAddressType = u'''formatClientAddress(ClientAddress0.id) AS locAddress,'''
            joinAddressType = u''' LEFT JOIN ClientAddress AS ClientAddress0 ON ClientAddress0.client_id = Diagnosis.client_id
                            AND ClientAddress0.id = (SELECT MAX(id) FROM ClientAddress AS CA0 WHERE CA0.Type=0 and CA0.client_id = Diagnosis.client_id AND CA0.deleted = 0)
                            LEFT JOIN Address ON Address.id = ClientAddress0.address_id'''
    else:
        colsAddressType = u'''formatClientAddress(ClientAddress0.id) AS regAddress,
                              formatClientAddress(ClientAddress1.id) AS locAddress,'''
        joinAddressType = u''' LEFT JOIN ClientAddress AS ClientAddress0 ON ClientAddress0.client_id = Diagnosis.client_id
                            AND ClientAddress0.id = (SELECT MAX(id) FROM ClientAddress AS CA0 WHERE CA0.Type=0 and CA0.client_id = Diagnosis.client_id AND CA0.deleted = 0)
                            LEFT JOIN Address ON Address.id = ClientAddress0.address_id
                            LEFT JOIN ClientAddress AS ClientAddress1 ON ClientAddress1.client_id = Diagnosis.client_id
                            AND ClientAddress1.id = (SELECT MAX(id) FROM ClientAddress AS CA1 WHERE CA1.Type=1 and CA1.client_id = Diagnosis.client_id AND CA1.deleted = 0)'''

    return db.query(stmt % (colsAddressType, joinAddressType, db.joinAnd(cond)))


class CDispObservationList(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setPayPeriodVisible(False)
        self.setTitle(u'Диспансерное наблюдение: список пациентов', u'Диспансерное наблюдение')


    def getSetupDialog(self, parent):
        result = CDispObservationListSetupDialog(parent)
        result.setTitle(self.title())
        return result


    def build(self, params):
        date = params.get('date', QDate())
        workOrgId = params.get('workOrgId', None)
        sex = params.get('sex', 0)
        ageFrom = params.get('ageFrom', 0)
        ageTo = params.get('ageTo', 150)
        areaIdEnabled = params.get('areaIdEnabled', False)
        areaId = params.get('areaId', None)
        MKBFilter = params.get('MKBFilter', 0)
        MKBFrom = params.get('MKBFrom', 'A00')
        MKBTo = params.get('MKBTo', 'Z99.9')
        personId = params.get('personId', None)
        isFilterAddressType = bool(params.get('isFilterAddressType', False))
        filterAddressType = params.get('filterAddressType', 0)

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        dumpParamsEx(cursor, params)
        self.dumpParams(cursor, params)
        cursor.insertBlock()

        tableColumns = [
            ('2%', [u'№' ],        CReportBase.AlignRight),
            ('15%',[u'ФИО'],       CReportBase.AlignLeft),
            ('2%', [u'пол'],       CReportBase.AlignCenter),
            ('5%', [u'д.р.'],      CReportBase.AlignLeft),
            ('5%', [u'СНИЛС'],     CReportBase.AlignLeft),
            ('16%',[u'Полис'],     CReportBase.AlignLeft),
            ('10%',[u'Документ'],  CReportBase.AlignLeft),
            ('20%',[u'Адрес'],     CReportBase.AlignLeft),
            ('10%',[u'Контакты'],  CReportBase.AlignLeft),
            ('10%',[u'Занятость'], CReportBase.AlignLeft),
            ('10%',[u'Диагноз'], CReportBase.AlignLeft)
            ]

        table = createTable(cursor, tableColumns)

        query = selectData(date, workOrgId, sex, ageFrom, ageTo, areaIdEnabled, areaId, MKBFilter, MKBFrom, MKBTo, personId, isFilterAddressType, filterAddressType)
        n = 0
        while query.next():
            n += 1
            record = query.record()
            name = formatName(record.value('lastName'),
                              record.value('firstName'),
                              record.value('patrName'))
            birthDate = forceString(record.value('birthDate'))
            sex = formatSex(forceInt(record.value('sex')))
            SNILS   = formatSNILS(record.value('SNILS'))
            policy  = ' '.join([forceString(record.value('policySerial')), forceString(record.value('policyNumber')), forceString(record.value('insurer'))])
            document= ' '.join([forceString(record.value('documentSerial')), forceString(record.value('documentNumber'))])
            regAddress = forceString(record.value('regAddress'))
            locAddress = forceString(record.value('locAddress'))
            MKB = normalizeMKB(forceString(record.value('MKB')))
            MKBEx = normalizeMKB(forceString(record.value('MKBEx')))
#            endDate = forceDate(record.value('endDate'))
            contacts = ''
            work= ' '.join([forceString(record.value('workName')), forceString(record.value('workPost'))])
            i = table.addRow()
            table.setText(i, 0, n)
            table.setText(i, 1, name)
            table.setText(i, 2, sex)
            table.setText(i, 3, birthDate)
            table.setText(i, 4, SNILS)
            table.setText(i, 5, policy)
            table.setText(i, 6, document)
            table.setText(i, 7, regAddress+'\n'+locAddress)
            table.setText(i, 8, contacts)
            table.setText(i, 9, work)
            table.setText(i, 10, MKB + ((u' + ' + MKBEx) if MKBEx else u''))
        return doc


from Ui_DispObservationListSetup import Ui_DispObservationSetupDialog


class CDispObservationListSetupDialog(QtGui.QDialog, Ui_DispObservationSetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.patientRequired = False
        self.setupUi(self)
        self.cmbArea.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbArea.setValue(QtGui.qApp.currentOrgStructureId())
        self.setChkPrintOnlyFilledRowsVisible(False)


    def setTitle(self, title):
        self.setWindowTitle(title)

    def setChkPrintOnlyFilledRowsVisible(self, value):
        self.chkPrintOnlyFilledRows.setVisible(value)


    def setParams(self, params):
        self.edtDate.setDate(params.get('date', QDate.currentDate()))
        self.cmbPerson.setValue(params.get('personId', None))
        self.cmbWorkOrganisation.setValue(params.get('workOrgId', None))
        self.cmbSex.setCurrentIndex(params.get('sex', 0))
        self.edtAgeFrom.setValue(params.get('ageFrom', 0))
        self.edtAgeTo.setValue(params.get('ageTo', 150))
        areaIdEnabled = bool(params.get('areaIdEnabled', False))
        self.chkArea.setChecked(areaIdEnabled)
        self.cmbArea.setEnabled(areaIdEnabled)
        self.cmbArea.setValue(params.get('areaId', None))
        isFilterAddressType = bool(params.get('isFilterAddressType', False))
        self.chkFilterAddressType.setChecked(isFilterAddressType)
        if isFilterAddressType:
            self.cmbFilterAddressType.setCurrentIndex(params.get('filterAddressType', 0))
        MKBFilter = params.get('MKBFilter', 0)
        self.cmbMKBFilter.setCurrentIndex(MKBFilter if MKBFilter else 0)
        self.edtMKBFrom.setText(params.get('MKBFrom', 'A00'))
        self.edtMKBTo.setText(params.get('MKBTo',   'Z99.9'))
        self.chkPrintOnlyFilledRows.setChecked(bool(params.get('isPrintOnlyFilledRows', False)))


    def params(self):
        result = {}
        result['date'] = self.edtDate.date()
        result['personId'] = self.cmbPerson.value()
        result['workOrgId'] = self.cmbWorkOrganisation.value()
        result['sex'] = self.cmbSex.currentIndex()
        result['ageFrom'] = self.edtAgeFrom.value()
        result['ageTo'] = self.edtAgeTo.value()
        result['areaIdEnabled'] = self.chkArea.isChecked()
        result['areaId'] = self.cmbArea.value()
        result['isFilterAddressType'] = self.chkFilterAddressType.isChecked()
        result['filterAddressType'] = self.cmbFilterAddressType.currentIndex()
        result['MKBFilter'] = self.cmbMKBFilter.currentIndex()
        result['MKBFrom']   = unicode(self.edtMKBFrom.text())
        result['MKBTo']     = unicode(self.edtMKBTo.text())
        result['isPrintOnlyFilledRows'] = self.chkPrintOnlyFilledRows.isChecked()
        return result


    @pyqtSignature('')
    def on_btnSelectWorkOrganisation_clicked(self):
        orgId = selectOrganisation(self, self.cmbWorkOrganisation.value(), False)
        self.cmbWorkOrganisation.updateModel()
        if orgId:
            self.cmbWorkOrganisation.setValue(orgId)


    @pyqtSignature('int')
    def on_cmbMKBFilter_currentIndexChanged(self, index):
        self.edtMKBFrom.setEnabled(index == 1)
        self.edtMKBTo.setEnabled(index == 1)
