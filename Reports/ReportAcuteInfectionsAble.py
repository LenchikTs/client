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

from library.Utils      import forceString
from library.DialogBase import CDialogBase
from Events.EventTypeListEditorDialog import CEventTypeListEditorDialog
from Events.Utils       import getWorkEventTypeFilter
#from Reports.Report     import CReport
from Reports.SelectOrgStructureListDialog      import CSelectOrgStructureListDialog
from Reports.Ui_ReportAcuteInfectionsAbleSetup import Ui_ReportAcuteInfectionsAbleSetupDialog


def getFilterAddress(params):
    condAddress = []
    db = QtGui.qApp.db
    tableClient = db.table('Client')
    tableClientAddress = db.table('ClientAddress').alias('CA')
    tableAddress = db.table('Address').alias('A')
    tableAddressHouse = db.table('AddressHouse').alias('AH')

    filterAddressType = params.get('filterAddressType', 0)
    filterAddressCity = params.get('filterAddressCity', None)
    filterAddressStreet = params.get('filterAddressStreet', None)
    filterAddressHouse = params.get('filterAddressHouse', u'')
    filterAddressCorpus = params.get('filterAddressCorpus', u'')
    filterAddressFlat = params.get('filterAddressFlat', u'')
    filterAddressOkato = params.get('filterAddressOkato')
    filterAddressStreetList = params.get('filterAddressStreetList')

    tableQuery = tableClientAddress.innerJoin(tableAddress, tableAddress['id'].eq(tableClientAddress['address_id']))
    tableQuery = tableQuery.innerJoin(tableAddressHouse, tableAddressHouse['id'].eq(tableAddress['house_id']))

    condAddress.append(tableClientAddress['client_id'].eq(tableClient['id']))
    condAddress.append(tableClientAddress['type'].eq(filterAddressType))
    condAddress.append(db.joinOr([tableClientAddress['id'].isNull(), tableClientAddress['deleted'].eq(0)]))
    if filterAddressCity or filterAddressStreet or filterAddressHouse or filterAddressCorpus or filterAddressFlat:
        condAddress.append(db.joinOr([tableAddress['id'].isNull(), tableAddress['deleted'].eq(0)]))
        condAddress.append(db.joinOr([tableAddressHouse['id'].isNull(), tableAddressHouse['deleted'].eq(0)]))
    if filterAddressCity:
        condAddress.append(tableAddressHouse['KLADRCode'].like('%s%%00'%filterAddressCity.rstrip('0')))
    if filterAddressStreet:
        condAddress.append(tableAddressHouse['KLADRStreetCode'].like(filterAddressStreet))
    if filterAddressHouse:
        condAddress.append(tableAddressHouse['number'].eq(filterAddressHouse))
    if filterAddressCorpus:
        condAddress.append(tableAddressHouse['corpus'].eq(filterAddressCorpus))
    if filterAddressFlat:
        condAddress.append(tableAddress['flat'].eq(filterAddressFlat))
    if filterAddressOkato:
        condAddress.append(tableAddressHouse['KLADRStreetCode'].inlist(filterAddressStreetList))
    return db.selectStmt(tableQuery, 'MAX(CA.id)', condAddress)


class CReportAcuteInfectionsAbleSetupDialog(CDialogBase, Ui_ReportAcuteInfectionsAbleSetupDialog):
    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.patientRequired = False
        self.setupUi(self)
        self.cmbEventPurpose.setTable('rbEventTypePurpose', True, filter='code != \'0\'')
        self.cmbEventTypeDD.setTable('EventType', True, filter ='form = 131', order='EventType.id DESC')
        self.cmbEventType.setTable('EventType', True, filter=getWorkEventTypeFilter(isApplyActive=True))
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())
        self.cmbSocStatusType.setTable('vrbSocStatusType', True)
        self.cmbSpeciality.setTable('rbSpeciality', True)
        self.setAreaEnabled(False)
        self.setFilterAddressOrgStructureVisible(False)
        self.setMKBFilterEnabled(False)
        self.setAccountAccompEnabled(False)
        self.setOnlyFirstTimeEnabled(False)
        self.setNotNullTraumaTypeEnabled(False)
        self.setEventTypeDDEnabled(False)
        self.setPersonPostEnabled(True)
        self.setEventTypeListListVisible(False)
        self.setOrgStructureListVisible(False)
        self.cmbArea.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbArea.setValue(QtGui.qApp.currentOrgStructureId())
        self.cmbFilterAddressCity.setCode(QtGui.qApp.defaultKLADR())
        self.eventTypeList = []
        self.orgStructureList = []
        self.setCMBEventTypeVisible(True)
        self.setCMBOrgStructureVisible(True)
        self._isAllAddressSelectable = False
        self.setSpecialityVisible(False)


    def setSpecialityVisible(self, value):
        self.cmbSpeciality.setVisible(value)
        self.lblSpeciality.setVisible(value)


    def setCMBEventTypeVisible(self, value):
        self.isEventTypeVisible = value
        self.cmbEventType.setVisible(value)
        self.lblEventType.setVisible(value)


    def setCMBOrgStructureVisible(self, value):
        self.isOrgStructureVisible = value
        self.cmbOrgStructure.setVisible(value)
        self.lblOrgStructure.setVisible(value)


    def setEventTypeListListVisible(self, value):
        self.btnEventTypeList.setVisible(value)
        self.lblEventTypeList.setVisible(value)


    def setOrgStructureListVisible(self, value):
        self.btnOrgStructureList.setVisible(value)
        self.lblOrgStructureList.setVisible(value)


    def setAreaEnabled(self, mode=True):
        for widget in (self.chkArea, self.lblArea, self.cmbArea):
            widget.setVisible(mode)
        self.areaEnabled = mode


    def setFilterAddressOrgStructureVisible(self, mode=False):
        self.chkFilterAddressOrgStructure.setVisible(mode)
        self.cmbFilterAddressOrgStructureType.setVisible(mode)
        self.cmbFilterAddressOrgStructure.setVisible(mode)


    def setPersonPostEnabled(self, mode=False):
        self.lblPersonPost.setVisible(mode)
        self.cmbPersonPost.setVisible(mode)
        self.personPostEnabled = mode


    def setMKBFilterEnabled(self, mode=True):
        for widget in (self.lblMKB, self.frmMKB, self.lblMKBEx, self.frmMKBEx):
            widget.setVisible(mode)
        self.MKBFilterEnabled = mode


    def setAccountAccompEnabled(self, mode=True):
        self.chkAccountAccomp.setVisible(mode)
        self.accountAccompEnabled = mode


    def setOnlyFirstTimeEnabled(self, mode=True):
        self.chkOnlyFirstTime.setVisible(mode)
        self.onlyFirstTimeEnabled = mode


    def setNotNullTraumaTypeEnabled(self, mode=True):
        self.chkNotNullTraumaType.setVisible(mode)
        self.notNullTraumaType = mode


    def setEventTypeDDEnabled(self, mode=True):
        self.lblEventTypeDD.setVisible(mode)
        self.cmbEventTypeDD.setVisible(mode)
        self.notEventTypeDD = mode


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setEventTypeVisible(self, visible=True):
        pass


    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.cmbSpeciality.setValue(params.get('specialityId', None))
        self.cmbEventPurpose.setValue(params.get('eventPurposeId', None))
        if self.isEventTypeVisible:
            self.cmbEventType.setValue(params.get('eventTypeId', None))
        else:
            self.eventTypeList = params.get('eventTypeList', [])
            if self.eventTypeList:
                db = QtGui.qApp.db
                tableET = db.table('EventType')
                records = db.getRecordList(tableET, [tableET['name']], [tableET['deleted'].eq(0), tableET['id'].inlist(self.eventTypeList)])
                nameList = []
                for record in records:
                    nameList.append(forceString(record.value('name')))
                self.lblEventTypeList.setText(u','.join(name for name in nameList if name))
            else:
                self.lblEventTypeList.setText(u'не задано')
        eventTypeDDId = None
        if self.notEventTypeDD:
            eventTypeDDId = params.get('eventTypeDDId', None)
            totalItems = self.cmbEventTypeDD._model.rowCount(None)
            if totalItems > 0:
                if not eventTypeDDId:
                    eventTypeDDId = self.cmbEventTypeDD._model.getId(0)
        self.cmbEventTypeDD.setValue(eventTypeDDId)
        if self.isOrgStructureVisible:
            self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        else:
            self.orgStructureList = params.get('orgStructureList', [])
            if self.orgStructureList:
                if len(self.orgStructureList) == 1 and not self.orgStructureList[0]:
                    self.lblOrgStructureList.setText(u'подразделение: ЛПУ')
                else:
                    db = QtGui.qApp.db
                    table = db.table('OrgStructure')
                    records = db.getRecordList(table, [table['name']], [table['deleted'].eq(0), table['id'].inlist(self.orgStructureList)])
                    self.lblOrgStructureList.setText(u', '.join(forceString(record.value('name')) for record in records if forceString(record.value('name'))))
            else:
                self.lblOrgStructureList.setText(u'подразделение: ЛПУ')
        self.cmbPerson.setValue(params.get('personId', None))
        self.cmbSex.setCurrentIndex(params.get('sex', 0))
        self.cmbSocStatusClass.setValue(params.get('socStatusClassId', None))
        self.cmbSocStatusType.setValue(params.get('socStatusTypeId', None))
        areaIdEnabled = bool(params.get('areaIdEnabled', False))
        self.chkArea.setChecked(areaIdEnabled)
        self.cmbArea.setEnabled(areaIdEnabled)
        self.cmbArea.setValue(params.get('areaId', None))
        MKBFilter = params.get('MKBFilter', 0)
        self.cmbMKBFilter.setCurrentIndex(MKBFilter if MKBFilter else 0)
        self.edtMKBFrom.setText(params.get('MKBFrom', 'A00'))
        self.edtMKBTo.setText(params.get('MKBTo',   'Z99.9'))
        MKBExFilter = params.get('MKBExFilter', 0)
        self.cmbMKBExFilter.setCurrentIndex(MKBExFilter if MKBExFilter else 0)
        self.edtMKBExFrom.setText(params.get('MKBExFrom', 'A00'))
        self.edtMKBExTo.setText(params.get('MKBExTo',   'Z99.9'))
        self.chkAccountAccomp.setChecked(bool(params.get('accountAccomp', False)))
        self.chkOnlyFirstTime.setChecked(bool(params.get('onlyFirstTime', False)))
        self.chkNotNullTraumaType.setChecked(bool(params.get('notNullTraumaType', False)))
        self.chkRegisteredInPeriod.setChecked(bool(params.get('registeredInPeriod', False)))
        self.cmbLocality.setCurrentIndex(params.get('locality', 0))
        self.chkFilterAddress.setChecked(bool(params.get('isFilterAddress', False)))
        self.cmbFilterAddressType.setCurrentIndex(params.get('filterAddressType', 0))
        self.cmbFilterAddressCity.setCode(params.get('filterAddressCity', QtGui.qApp.defaultKLADR()))
        addressStreet = params.get('filterAddressStreet', u'')
        if not addressStreet:
            addressStreet = QtGui.qApp.defaultKLADR()
            self.cmbFilterAddressStreet.setCity(addressStreet)
        else:
            self.cmbFilterAddressStreet.setCode(addressStreet)
        self.edtFilterAddressHouse.setText(params.get('filterAddressHouse', u''))
        self.edtFilterAddressCorpus.setText(params.get('filterAddressCorpus', u''))
        self.edtFilterAddressFlat.setText(params.get('filterAddressFlat', u''))
        if self.personPostEnabled:
            self.cmbPersonPost.setCurrentIndex(params.get('isPersonPost', 0))
        self.chkFilterAddressOrgStructure.setChecked(params.get('isFilterAddressOrgStructure', False))
        self.cmbFilterAddressOrgStructureType.setCurrentIndex(params.get('addressOrgStructureType', 0))
        self.cmbFilterAddressOrgStructure.setValue(params.get('addressOrgStructure', None))


    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['specialityId'] = self.cmbSpeciality.value()
        result['eventPurposeId'] = self.cmbEventPurpose.value()
        if self.isEventTypeVisible:
            result['eventTypeId'] = self.cmbEventType.value()
        else:
            result['eventTypeList'] = self.eventTypeList
        if self.notEventTypeDD:
            result['eventTypeDDId'] = self.cmbEventTypeDD.value()
        if self.isOrgStructureVisible:
            result['orgStructureId'] = self.cmbOrgStructure.value()
        else:
            if len(self.orgStructureList) == 1 and not self.orgStructureList[0]:
               result['orgStructureList'] = []
            else:
                result['orgStructureList'] = self.orgStructureList
        result['personId'] = self.cmbPerson.value()
        result['sex'] = self.cmbSex.currentIndex()
        result['socStatusClassId'] = self.cmbSocStatusClass.value()
        result['socStatusTypeId'] = self.cmbSocStatusType.value()
        if self.areaEnabled:
            result['areaIdEnabled'] = self.chkArea.isChecked()
            result['areaId'] = self.cmbArea.value()
        if self.MKBFilterEnabled:
            result['MKBFilter'] = self.cmbMKBFilter.currentIndex()
            result['MKBFrom']   = unicode(self.edtMKBFrom.text())
            result['MKBTo']     = unicode(self.edtMKBTo.text())
            result['MKBExFilter']= self.cmbMKBExFilter.currentIndex()
            result['MKBExFrom']  = unicode(self.edtMKBExFrom.text())
            result['MKBExTo']    = unicode(self.edtMKBExTo.text())
        if self.accountAccompEnabled:
            result['accountAccomp'] = self.chkAccountAccomp.isChecked()
        if self.onlyFirstTimeEnabled:
            result['onlyFirstTime'] = self.chkOnlyFirstTime.isChecked()
        if self.notNullTraumaType:
            result['notNullTraumaType'] = self.chkNotNullTraumaType.isChecked()
        result['registeredInPeriod'] = self.chkRegisteredInPeriod.isChecked()
        result['locality'] = self.cmbLocality.currentIndex()
        result['isFilterAddress'] = self.chkFilterAddress.isChecked()
        result['filterAddressType'] = self.cmbFilterAddressType.currentIndex()
        result['filterAddressCity'] = self.cmbFilterAddressCity.code()
        result['filterAddressStreet'] = self.cmbFilterAddressStreet.code()
        result['filterAddressHouse'] = self.edtFilterAddressHouse.text()
        result['filterAddressCorpus'] = self.edtFilterAddressCorpus.text()
        result['filterAddressFlat'] = self.edtFilterAddressFlat.text()
        if self.personPostEnabled:
            result['isPersonPost'] = self.cmbPersonPost.currentIndex()
        result['isFilterAddressOrgStructure'] = self.chkFilterAddressOrgStructure.isChecked()
        result['addressOrgStructureType'] = self.cmbFilterAddressOrgStructureType.currentIndex()
        result['addressOrgStructure'] = self.cmbFilterAddressOrgStructure.value()
        return result


    def exec_(self):
        result = CDialogBase.exec_(self)
        if self._isAllAddressSelectable:
            self.setAllAddressSelectable(False)
        return result


    def setAllAddressSelectable(self, value):
        self._isAllAddressSelectable = value
        self.cmbFilterAddressCity.model().setAllSelectable(value)


    @pyqtSignature('int')
    def on_cmbEventPurpose_currentIndexChanged(self, index):
        if self.isEventTypeVisible:
            eventPurposeId = self.cmbEventPurpose.value()
            if eventPurposeId:
                filter = 'EventType.purpose_id=%d' % eventPurposeId
            else:
                filter = getWorkEventTypeFilter(isApplyActive=True)
            self.cmbEventType.setFilter(filter)


    @pyqtSignature('int')
    def on_cmbFilterAddressCity_currentIndexChanged(self, index):
        code = self.cmbFilterAddressCity.code()
        self.cmbFilterAddressStreet.setCity(code)


    @pyqtSignature('QDate')
    def on_edtBegDate_dateChanged(self, date):
        self.cmbPerson.setBegDate(date)


    @pyqtSignature('QDate')
    def on_edtEndDate_dateChanged(self, date):
        self.cmbPerson.setEndDate(date)


    @pyqtSignature('int')
    def on_cmbSocStatusClass_currentIndexChanged(self, index):
        socStatusClassId = self.cmbSocStatusClass.value()
        filter = ('class_id=%d' % socStatusClassId) if socStatusClassId else ''
        self.cmbSocStatusType.setFilter(filter)


    @pyqtSignature('int')
    def on_cmbMKBFilter_currentIndexChanged(self, index):
        self.edtMKBFrom.setEnabled(index == 1)
        self.edtMKBTo.setEnabled(index == 1)


    @pyqtSignature('int')
    def on_cmbMKBExFilter_currentIndexChanged(self, index):
        self.edtMKBExFrom.setEnabled(index == 1)
        self.edtMKBExTo.setEnabled(index == 1)


    @pyqtSignature('')
    def on_btnEventTypeList_clicked(self):
        self.eventTypeList = []
        self.lblEventTypeList.setText(u'не задано')
        eventPurposeId = self.cmbEventPurpose.value()
        if eventPurposeId:
            filter = u'EventType.purpose_id =%d' % eventPurposeId
        else:
            filter = getWorkEventTypeFilter(isApplyActive=True)
        dialog = CEventTypeListEditorDialog(self, filter)
        if dialog.exec_():
            self.eventTypeList = dialog.values()
            if self.eventTypeList:
                db = QtGui.qApp.db
                tableET = db.table('EventType')
                records = db.getRecordList(tableET, [tableET['name']], [tableET['deleted'].eq(0), tableET['id'].inlist(self.eventTypeList)])
                nameList = []
                for record in records:
                    nameList.append(forceString(record.value('name')))
                self.lblEventTypeList.setText(u','.join(name for name in nameList if name))


    @pyqtSignature('')
    def on_btnOrgStructureList_clicked(self):
        db = QtGui.qApp.db
        self.orgStructureList = []
        self.lblOrgStructureList.setText(u'подразделение: ЛПУ')
        orgId = QtGui.qApp.currentOrgId()
        filter = []
        if orgId:
            filter.append(u'organisation_id = %s'%(orgId))
        dialog = CSelectOrgStructureListDialog(self, db.joinAnd(filter))
        if dialog.exec_():
            self.orgStructureList = dialog.values()
            if self.orgStructureList:
                if len(self.orgStructureList) == 1 and not self.orgStructureList[0]:
                    self.lblOrgStructureList.setText(u'подразделение: ЛПУ')
                else:
                    table = db.table('OrgStructure')
                    records = db.getRecordList(table, [table['name']], [table['id'].inlist(self.orgStructureList)])
                    nameList = []
                    for record in records:
                        nameList.append(forceString(record.value('name')))
                    self.lblOrgStructureList.setText(u', '.join(name for name in nameList if name))


    @pyqtSignature('int')
    def on_cmbSpeciality_currentIndexChanged(self, index):
        specialityId = self.cmbSpeciality.value()
        self.cmbPerson.setSpecialityId(specialityId)

