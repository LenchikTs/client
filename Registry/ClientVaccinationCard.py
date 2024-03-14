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


from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDate, QLocale, QVariant, pyqtSignature, SIGNAL, QDateTime

from Orgs.OrgComboBox import CPolyclinicComboBox
from Orgs.Orgs import selectOrganisation
from Stock.getBatch import getBatch
from library.DialogBase              import CDialogBase
from library.Identification          import getIdentificationRecords
from library.InDocTable              import CInDocTableModel, CRBInDocTableCol
from library.interchange             import getDateEditValue, getDbComboBoxTextValue, getDoubleBoxValue, getLineEditValue, getRBComboBoxValue, setDateEditValue, setDbComboBoxTextValue, setDoubleBoxValue, setLineEditValue, setRBComboBoxValue
from library.ItemsListDialog         import CItemEditorBaseDialog
from library.RBCheckTable            import CRBCheckTableModel
from library.TableModel import CDateCol, CDesignationCol, CNumCol, CRefBookCol, CTableModel, CTextCol, CIntCol
from library.Utils                   import forceDouble, forceInt, forceRef, forceString, toVariant, trim, forceDateTime
from library.PrintTemplates          import applyTemplate, getPrintButton
from library.PrintInfo               import CInfoContext

from RefBooks.Vaccine.List           import CRBVaccineEditor
from Registry.Utils                  import getClientBanner, CClientInfo, CClientVaccinationProbeInfoList, CClientMedicalExemptionInfoList, CClientVaccinationInfoList
from Users.Rights                    import urCanEditClientVaccination

from Ui_ClientVaccinationCardDialog  import Ui_ClientVaccinationCardDialog
from Ui_ClientVaccinationEditor      import Ui_ClientVaccinationEditor
from Ui_ClientVaccinationProbeEditor import Ui_ClientVaccinationProbeEditor
from Ui_ClientMedicalExemptionEditor import Ui_ClientMedicalExemptionEditor


def openClientVaccinationCard(parent, clientId):
    result = None
    dialog = CClientVaccinationCard(parent, clientId)
    try:
        dialog.setReadOnly(not QtGui.qApp.userHasRight(urCanEditClientVaccination))
        result = dialog.exec_()
    finally:
        dialog.deleteLater()
    return result


# ###########################################################################


def openClientVaccination(parent, clientId, itemId):
    resultId = None
    dialog = CClientVaccinationEditor(parent, clientId)
    if itemId:
        try:
            dialog.load(itemId)
            dialog.setReadOnly(not QtGui.qApp.userHasRight(urCanEditClientVaccination))
            if dialog.exec_():
                resultId = dialog.itemId()
        finally:
            dialog.deleteLater()
    return resultId


def newClientVaccination(parent, clientId, params={}):
    resultId = None
    dialog = CClientVaccinationEditor(parent, clientId)
    try:
        dialog.setParams(params)
        if dialog.exec_():
            resultId = dialog.itemId()
    finally:
        dialog.deleteLater()
    return resultId


# ###########################################################################

def openClientProbe(parent, clientId, itemId):
    resultId = None
    dialog = CClientProbeEditor(parent, clientId)
    if itemId:
        try:
            dialog.load(itemId)
            dialog.setReadOnly(not QtGui.qApp.userHasRight(urCanEditClientVaccination))
            if dialog.exec_():
                resultId = dialog.itemId()
        finally:
            dialog.deleteLater()
    return resultId


def newClientProbe(parent, clientId, params={}):
    resultId = None
    dialog = CClientProbeEditor(parent, clientId)
    try:
        dialog.setParams(params)
        if dialog.exec_():
            resultId = dialog.itemId()
    finally:
        dialog.deleteLater()
    return resultId


# ###########################################################################


def openClientMedicalExemption(parent, clientId, itemId):
    resultId = None
    if itemId:
        dialog = CClientMedicalExemptionEditor(parent, clientId)
        try:
            dialog.load(itemId)
            dialog.setReadOnly(not QtGui.qApp.userHasRight(urCanEditClientVaccination))
            if dialog.exec_():
                resultId = dialog.itemId()
        finally:
            dialog.deleteLater()
    return resultId


def newClientMedicalExemption(parent, clientId, params={}):
    resultId = None
    dialog = CClientMedicalExemptionEditor(parent, clientId)
    try:
        dialog.setParams(params)
        if dialog.exec_():
            resultId = dialog.itemId()
    finally:
        dialog.deleteLater()
    return resultId


# ###########################################################################


def openVaccineSchema(parent, vaccineId):
    if vaccineId:
        dialog = CRBVaccineEditor(parent)
        try:
            dialog.load(vaccineId)
            dialog.setReadOnly(True)
            dialog.exec_()
        finally:
            dialog.deleteLater()


# ###########################################################################


def findVaccineIdAndVaccinationTypeByGtin(gtin):
    records = getIdentificationRecords('rbVaccine',
                                       'master_id, vaccinationType',
                                       'urn:gtin',
                                       gtin,
                                       1)
    if records:
        vaccineId = forceRef(records[0].value('master_id'))
        vaccinationType = forceString(records[0].value('vaccinationType'))
    else:
        vaccineId = None
        vaccinationType = ''
    return vaccineId, vaccinationType

# ###########################################################################


class CClientVaccinationCard(CDialogBase, Ui_ClientVaccinationCardDialog):
    def __init__(self, parent=None, clientId=None):
        CDialogBase.__init__(self, parent)

        # MODELS
        self.addModels('FilterInfection',            CRBCheckTableModel(self, 'rbInfection', u'Инфекции'))
        self.addModels('FilterVaccine',              CRBCheckTableModel(self, 'rbVaccine', u'Вакцины'))
        self.addModels('FilterProbe',                CRBCheckTableModel(self, 'rbVaccinationProbe', u'Пробы'))
        self.addModels('Vaccination',                CVaccinationTableModel(self))
        self.addModels('VaccineInfections',          CVaccineInfectionsTableModel(self))
        self.addModels('Probe',                      CProbeTableModel(self))
        self.addModels('ProbeLeftoverSchema',        CProbeLeftoverSchemaTableModel(self))
        self.addModels('MedicalExemption',           CMedicalExemptionModel(self))
        self.addModels('MedicalExemptionInfections', CMedicalExemptionInfectionsModel(self))

        # MENUS
        # vaccination table menu
        self.addObject('actAddVaccination',    QtGui.QAction(u'Добавить', self))
        self.addObject('actEditVaccination',   QtGui.QAction(u'Редактировать', self))
        self.addObject('actDeleteVaccination', QtGui.QAction(u'Удалить', self))
        self.addObject('actSchema',            QtGui.QAction(u'Схема', self))

        self.addObject('actAddProbe',    QtGui.QAction(u'Добавить', self))
        self.addObject('actEditProbe',   QtGui.QAction(u'Редактировать', self))
        self.addObject('actDeleteProbe', QtGui.QAction(u'Удалить', self))
        self.addAction(self.actAddProbe)
        self.addAction(self.actEditProbe)
        self.addAction(self.actDeleteProbe)

        self.actAddVaccination.setShortcut(Qt.Key_F9)
        self.addAction(self.actAddVaccination)

        self.actEditVaccination.setShortcut(Qt.Key_F4)
        self.addAction(self.actEditVaccination)

        # filter vaccine table menu
        self.addObject('actFilterVaccineSchema', QtGui.QAction(u'Схема', self))

        # medical exemption table menu
        self.addObject('actAddMedicalExemption',    QtGui.QAction(u'Добавить', self))
        self.addObject('actEditMedicalExemption',   QtGui.QAction(u'Редактировать', self))
        self.addObject('actDeleteMedicalExemption', QtGui.QAction(u'Удалить', self))

        self.setupUi(self)
        self.setWindowTitle(u'Прививочная карта пациента')
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setWindowState(Qt.WindowMaximized)

        # TABLES
        self.setModels(self.tblFilterInfection,           self.modelFilterInfection,   self.selectionModelFilterInfection)
        self.setModels(self.tblFilterVaccine,             self.modelFilterVaccine,     self.selectionModelFilterVaccine)
        self.setModels(self.tblFilterProbe,               self.modelFilterProbe,       self.selectionModelFilterProbe)
        self.setModels(self.tblVaccination,               self.modelVaccination,       self.selectionModelVaccination)
        self.setModels(self.tblVaccinationLeftOverSchema, self.modelVaccineInfections, self.selectionModelVaccineInfections) #временно
        self.setModels(self.tblProbe,                     self.modelProbe,             self.selectionModelProbe)
        self.setModels(self.tblProbeLeftoverSchema,       self.modelProbeLeftoverSchema, self.selectionModelProbeLeftoverSchema)
        self.setModels(self.tblMedicalExemption, self.modelMedicalExemption, self.selectionModelMedicalExemption)
        self.setModels(self.tblMedicalExemptionInfections,
                       self.modelMedicalExemptionInfections,
                       self.selectionModelMedicalExemptionInfections)



        # MENUS
        self.tblVaccination.createPopupMenu([self.actAddVaccination, self.actDeleteVaccination,
                                             self.actSchema, self.actEditVaccination])
        self.tblProbe.createPopupMenu([self.actAddProbe, self.actDeleteProbe, self.actEditProbe])

        self.tblFilterVaccine.addPopupAction(self.actFilterVaccineSchema)

        # medical exemption table menu
        self.tblMedicalExemption.createPopupMenu([self.actAddMedicalExemption, self.actEditMedicalExemption, self.actDeleteMedicalExemption])

        # view popup show
        self.connect(self.tblVaccination.popupMenu(), SIGNAL('aboutToShow()'), self.on_tblVaccinationPopup_aboutToShow)
        self.connect(self.tblProbe.popupMenu(), SIGNAL('aboutToShow()'), self.on_tblProbePopup_aboutToShow)
        # sort column
        self.connect(self.tblVaccination.horizontalHeader(), SIGNAL('sectionClicked(int)'), self._setVaccinationOrderByColumn)
        self.connect(self.tblVaccinationLeftOverSchema.horizontalHeader(), SIGNAL('sectionClicked(int)'), self._setVaccineInfectionsOrderByColumn)
        self.connect(self.tblMedicalExemption.horizontalHeader(), SIGNAL('sectionClicked(int)'), self._setMedicalExemptionOrderByColumn)
        self.connect(self.tblMedicalExemptionInfections.horizontalHeader(), SIGNAL('sectionClicked(int)'), self._setMedicalExemptionInfectionsOrderByColumn)

        if clientId:
            self.setClientId(clientId)
        self.__setVisibleProbeAndVaccine(False, True)
        self.cmbFilterVaccinationCalendar.setTable('rbVaccinationCalendar')

        self.updateMedicalExemptionList()
        self.updateVaccinationList()
        self.updateProbeList()
        self.addObject('btnPrint', getPrintButton(self, 'vaccinationCard'))
        self.buttonBox.addButton(self.btnPrint, QtGui.QDialogButtonBox.ActionRole)
        self.connect(self.btnPrint, SIGNAL('printByTemplate(int)'), self.on_btnPrint_printByTemplate)
        # QueuedConnection потребовалось потому, что в диалоге мы тоже хотим получать этот сигнал, а в случае DirectConnection
        # цикл прохождения сигнала блокируется до закрытия диалога, диалог при некоторых условиях не может получить сигнал.
        self.connect(QtGui.qApp, SIGNAL('sgtinReceived(QString)'), self.onSgtinReceived, Qt.QueuedConnection)


    def _setVaccinationOrderByColumn(self, column):
        self.tblVaccination.setOrder(column)
        self.updateVaccinationList(self.tblVaccination.currentItemId())


    def _setVaccineInfectionsOrderByColumn(self, column):
        self.tblVaccinationLeftOverSchema.setOrder(column)
        self.updateVaccinationInfectionList(self.tblVaccination.model().idList())


    def _setMedicalExemptionOrderByColumn(self, column):
        self.tblMedicalExemption.setOrder(column)
        self.updateMedicalExemptionList(self.tblMedicalExemption.currentItemId())


    def _setMedicalExemptionInfectionsOrderByColumn(self, column):
        self.tblMedicalExemptionInfections.setOrder(column)
        self.updateMedicalExemptionInfectionsList(self.tblMedicalExemption.currentItemId(), self.tblMedicalExemptionInfections.currentItemId())


    def setReadOnly(self, value=True):
        CDialogBase.setReadOnly(self, value)
        canEdit = not self.isReadOnly()
        self.actAddVaccination.setEnabled(canEdit)
        self.actAddProbe.setEnabled(canEdit)
        self.actAddMedicalExemption.setEnabled(canEdit)
        self.actEditMedicalExemption.setEnabled(canEdit)
        self.actDeleteMedicalExemption.setEnabled(canEdit)
        buttons = QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel if canEdit else QtGui.QDialogButtonBox.Close
        self.buttonBox.setStandardButtons(buttons)


    def __setVisibleProbeAndVaccine(self, probe=False, vaccine=True):
        self.tblFilterVaccine.setVisible(vaccine)
        self.tblFilterProbe.setVisible(probe)


    def setClientId(self, clientId):
        self._clientId = clientId
        if clientId:
            self.txtClientInfoBrowser.setHtml(getClientBanner(clientId))
        else:
            self.txtClientInfoBrowser.setText('')


    def updateVaccinationList(self, id=None):
        db = QtGui.qApp.db
        table = db.table('ClientVaccination')
        cond = [table['client_id'].eq(self._clientId),
                table['deleted'].eq(0)]
        vaccineIdList = self.modelFilterVaccine.getCheckedIdList()
        if vaccineIdList:
            cond.append(table['vaccine_id'].inlist(vaccineIdList))
        else:
            vaccineIdList = self.modelFilterVaccine.idList()
            if vaccineIdList:
                cond.append(table['vaccine_id'].inlist(vaccineIdList))
        queryTable = table
        order = self.tblVaccination.order() if self.tblVaccination.order() else 'ClientVaccination.datetime, ClientVaccination.id'
        if 'rbVaccine' in order:
            tableRBVaccine = db.table('rbVaccine')
            queryTable = queryTable.leftJoin(tableRBVaccine, tableRBVaccine['id'].eq(table['vaccine_id']))
        if 'vrbPersonWithSpeciality' in order:
            tablePerson = db.table('vrbPersonWithSpeciality')
            queryTable = queryTable.leftJoin(tablePerson, tablePerson['id'].eq(table['person_id']))
        if 'rbReaction' in order:
            tableRBReaction = db.table('rbReaction')
            queryTable = queryTable.leftJoin(tableRBReaction, tableRBReaction['id'].eq(table['reaction_id']))
        if 'rbVaccine_SchemaTransitionType' in order:
            tableRBVaccineST = db.table('rbVaccine_SchemaTransitionType')
            queryTable = queryTable.leftJoin(tableRBVaccineST, tableRBVaccineST['id'].eq(table['transitionType_id']))
        if 'Organisation' in order:
            tableOrganisation = db.table('Organisation')
            queryTable = queryTable.leftJoin(tableOrganisation, tableOrganisation['id'].eq(table['relegateOrg_id']))
        idList = db.getIdList(queryTable, table['id'], cond, order=order)
        self.tblVaccination.setIdList(idList, id)
        self.updateVaccinationInfectionList(idList)


    def updateVaccinationInfectionList(self, vaccinationIdList):
        db = QtGui.qApp.db
        tableClientVaccination = db.table('ClientVaccination')
        vaccineIdList = db.getDistinctIdList(tableClientVaccination, 'vaccine_id',
                                            [tableClientVaccination['id'].inlist(vaccinationIdList), tableClientVaccination['deleted'].eq(0)])
        tableInfectionVaccine = db.table('rbInfection_rbVaccine')
        order = self.tblVaccinationLeftOverSchema.order() if self.tblVaccinationLeftOverSchema.order() else ''
        queryTable = tableInfectionVaccine
        if 'rbInfection' in order:
            tableRBInfection = db.table('rbInfection')
            queryTable = queryTable.leftJoin(tableRBInfection, tableRBInfection['id'].eq(tableInfectionVaccine['infection_id']))
        idList = QtGui.qApp.db.getDistinctIdList(queryTable, tableInfectionVaccine['infection_id'],
                                                 tableInfectionVaccine['vaccine_id'].inlist(vaccineIdList), order=order)
        self.modelVaccineInfections.setIdList(idList)


    def updateProbeList(self, id=None):
        db = QtGui.qApp.db
        table = db.table('ClientVaccinationProbe')
        cond = [table['client_id'].eq(self._clientId),
                table['deleted'].eq(0)
               ]
        probeIdList = self.modelFilterProbe.getCheckedIdList()
        if probeIdList:
            cond.append(table['probe_id'].inlist(probeIdList))
        else:
            probeIdList = self.modelFilterProbe.idList()
            if probeIdList:
                cond.append(table['probe_id'].inlist(probeIdList))
        queryTable = table
        order = self.tblProbe.order() if self.tblProbe.order() else 'ClientVaccinationProbe.datetime, ClientVaccinationProbe.id'
        if 'rbVaccinationProbe' in order:
            tableRBProbe = db.table('rbVaccinationProbe')
            queryTable = queryTable.leftJoin(tableRBProbe, tableRBProbe['id'].eq(table['probe_id']))
        if 'vrbPersonWithSpeciality' in order:
            tablePerson = db.table('vrbPersonWithSpeciality')
            queryTable = queryTable.leftJoin(tablePerson, tablePerson['id'].eq(table['person_id']))
        if 'rbReaction' in order:
            tableRBReaction = db.table('rbReaction')
            queryTable = queryTable.leftJoin(tableRBReaction, tableRBReaction['id'].eq(table['reaction_id']))
        if 'rbVaccinationResult' in order:
            tableRBProbeST = db.table('rbVaccinationResult')
            queryTable = queryTable.leftJoin(tableRBProbeST, tableRBProbeST['id'].eq(table['result_id']))
        if 'Organisation' in order:
            tableOrganisation = db.table('Organisation')
            queryTable = queryTable.leftJoin(tableOrganisation, tableOrganisation['id'].eq(table['relegateOrg_id']))
        idList = db.getDistinctIdList(queryTable, table['id'], cond, order=order)
        self.tblProbe.setIdList(idList, id)
        self.updateProbeInfectionList(idList)


    def updateProbeInfectionList(self, probeIdList):
        infectionIdList = set([])
        idList = []
        db = QtGui.qApp.db
        tableClientProbe = db.table('ClientVaccinationProbe')
        probeIdList = db.getDistinctIdList(tableClientProbe, 'probe_id',
                                          [tableClientProbe['id'].inlist(probeIdList), tableClientProbe['deleted'].eq(0)])
        tableRBVaccinationProbe = db.table('rbVaccinationProbe')
        records = db.getRecordList(tableRBVaccinationProbe, [tableRBVaccinationProbe['infections']], [tableRBVaccinationProbe['id'].inlist(probeIdList)])
        for record in records:
            infections = forceString(record.value('infections'))
            infectionList = set(infections.split(u','))
            infectionIdList |= infectionList
        infectionIdList = list(infectionIdList)
        if infectionIdList:
            order = self.tblProbeLeftoverSchema.order() if self.tblProbeLeftoverSchema.order() else ''
            tableRBInfection = db.table('rbInfection')
            idList = QtGui.qApp.db.getDistinctIdList(tableRBInfection, tableRBInfection['id'], [tableRBInfection['id'].inlist(infectionIdList)], order=order)
        self.modelProbeLeftoverSchema.setIdList(idList)


    def updateMedicalExemptionList(self, id=None):
        db = QtGui.qApp.db
        table = db.table('ClientMedicalExemption')
        cond = [table['client_id'].eq(self._clientId),
                table['deleted'].eq(0)]
        queryTable = table
        order = self.tblMedicalExemption.order() if self.tblMedicalExemption.order() else 'ClientMedicalExemption.date'
        if 'vrbPersonWithSpeciality' in order:
            tablePerson = db.table('vrbPersonWithSpeciality')
            queryTable = queryTable.leftJoin(tablePerson, tablePerson['id'].eq(table['person_id']))
        if 'rbMedicalExemptionType' in order:
            tableMET = db.table('rbMedicalExemptionType')
            queryTable = queryTable.leftJoin(tableMET, tableMET['id'].eq(table['medicalExemptionType_id']))
        idList = db.getIdList(queryTable, table['id'], cond, order)
        self.tblMedicalExemption.setIdList(idList, id)


    def updateMedicalExemptionInfectionsList(self, medicalExemptionId, id=None):
        db = QtGui.qApp.db
        table = db.table('ClientMedicalExemption_Infection')
        cond = [table['master_id'].eq(medicalExemptionId)]
        queryTable = table
        order = self.tblMedicalExemptionInfections.order() if self.tblMedicalExemptionInfections.order() else ''
        if 'rbInfection' in order:
            tableRBInfection = db.table('rbInfection')
            queryTable = queryTable.leftJoin(tableRBInfection, tableRBInfection['id'].eq(table['infection_id']))
        idList = db.getIdList(queryTable, table['id'], cond, order)
        self.tblMedicalExemptionInfections.setIdList(idList, id)


    def _params(self):
        params = {}
        vaccinationCalendarId = self.cmbFilterVaccinationCalendar.value()
        if vaccinationCalendarId:
            params['vaccinationCalendarId'] = vaccinationCalendarId
        infectionIdList = self.modelFilterInfection.getCheckedIdList()
        if infectionIdList:
            params['infectionIdList'] = infectionIdList
        vaccineIdList = self.modelFilterVaccine.getCheckedIdList()
        if vaccineIdList:
            params['vaccineIdList'] = vaccineIdList
        else:
            params['vaccineIdList'] = self.modelFilterVaccine.idList()
        probeIdList = self.modelFilterProbe.getCheckedIdList()
        if probeIdList:
            params['probeIdList'] = probeIdList
        else:
            params['probeIdList'] = self.modelFilterProbe.idList()
        personId = QtGui.qApp.userId
        if personId:
            params['personId'] = personId
        return params


    def onSgtinReceived(self, sgtin):
        # мы обрабатываем сигнал только в том случае,
        # если нет открытых дочерних диалогов и выбрана вкладка с вакцинами
        if QtGui.qApp.activeWindow() == self and self.tabWidget.currentIndex() == 0:
            vaccineId, vaccinationType = findVaccineIdAndVaccinationTypeByGtin(sgtin[:14])
            params = self._params()
            params['sgtin'] = sgtin
#            params['seria'] = 'xxx'
            if vaccineId:
                if vaccineId in params['vaccineIdList']:
                    params['vaccineIdList'] = [vaccineId]
                    params['vaccinationType'] = vaccinationType
            vaccinationId = newClientVaccination(self, self._clientId, params)
            if vaccinationId:
                self.updateVaccinationList(vaccinationId)



    @pyqtSignature('int')
    def on_btnPrint_printByTemplate(self, templateId):
        context = CInfoContext()
        vaccineList = context.getInstance(CClientVaccinationInfoList, self._clientId)
        vaccineProbeList = context.getInstance(CClientVaccinationProbeInfoList, self._clientId)
        medicalExemptionList = context.getInstance(CClientMedicalExemptionInfoList, self._clientId)
        clientInfo = context.getInstance(CClientInfo, self._clientId)
        data = {'vaccineList' : vaccineList,
                'vaccineProbeList' : vaccineProbeList,
                'medicalExemptionList' : medicalExemptionList,
                'client' : clientInfo    # vaccination, vaccinationProbe
               }
        applyTemplate(self, templateId, data)


    @pyqtSignature('int')
    def on_tabWidget_currentChanged(self, index):
        if index == 0:
            self.__setVisibleProbeAndVaccine(False, True)
        elif index == 1:
            self.__setVisibleProbeAndVaccine(True, False)


    @pyqtSignature('int')
    def on_cmbFilterVaccinationCalendar_currentIndexChanged(self, index):
        vaccinationCalendarId = self.cmbFilterVaccinationCalendar.value()
        if vaccinationCalendarId:
            db = QtGui.qApp.db
            idList = db.getIdList('rbVaccinationCalendar_Infection', 'infection_id', 'master_id=%d'%vaccinationCalendarId)
            tableInfection = db.table('rbInfection')
            self.modelFilterInfection.setFilter(tableInfection['id'].inlist(idList))
        else:
            self.modelFilterInfection.setFilter('')


    @pyqtSignature('QModelIndex')
    def on_tblVaccination_doubleClicked(self, index):
        self.on_actEditVaccination_triggered()



    @pyqtSignature('')
    def on_modelFilterInfection_itemCheckingChanged(self):
        infectionIdList = self.modelFilterInfection.getCheckedIdList()
        if infectionIdList:
            db = QtGui.qApp.db
            tableInfectionVaccine = db.table('rbInfection_rbVaccine')
            tableVaccine = db.table('rbVaccine')
            cond = tableInfectionVaccine['infection_id'].inlist(infectionIdList)
            idList = db.getIdList(tableInfectionVaccine, 'vaccine_id', cond)
            self.modelFilterVaccine.setFilter(tableVaccine['id'].inlist(idList))
        else:
            self.modelFilterVaccine.setFilter('')

        self.updateVaccinationList()


    def on_modelFilterVaccine_itemCheckingChanged(self):
        self.updateVaccinationList()


    @pyqtSignature('')
    def on_tblVaccinationPopup_aboutToShow(self):
        isVaccinationIndexValid = self.tblVaccination.currentIndex().isValid()
        canEdit = not self.isReadOnly()
        self.actEditVaccination.setEnabled(isVaccinationIndexValid and canEdit)
        self.actDeleteVaccination.setEnabled(isVaccinationIndexValid and canEdit)
        self.actSchema.setEnabled(isVaccinationIndexValid)


    @pyqtSignature('')
    def on_tblProbePopup_aboutToShow(self):
        isProbeIndexValid = self.tblProbe.currentIndex().isValid()
        canEdit = not self.isReadOnly()
        self.actEditProbe.setEnabled(isProbeIndexValid and canEdit)
        self.actDeleteProbe.setEnabled(isProbeIndexValid and canEdit)


    @pyqtSignature('')
    def on_actAddVaccination_triggered(self):
        vaccinationId = newClientVaccination(self, self._clientId, self._params())
        if vaccinationId:
            self.updateVaccinationList(vaccinationId)


    @pyqtSignature('')
    def on_actEditVaccination_triggered(self):
        vaccinationId = self.tblVaccination.currentItemId()
        if vaccinationId:
            vaccinationId = openClientVaccination(self, self._clientId, vaccinationId)
            self.updateVaccinationList(vaccinationId)


    @pyqtSignature('')
    def on_actDeleteVaccination_triggered(self):
        index = self.tblVaccination.currentIndex()
        row = index.row()
        if index.isValid() and self.modelVaccination.confirmRemoveRow(self.tblVaccination, row):
            self.modelVaccination.removeRow(row)


    @pyqtSignature('')
    def on_actSchema_triggered(self):
        vaccinationItem = self.tblVaccination.currentItem()
        openVaccineSchema(self, forceRef(vaccinationItem.value('vaccine_id')))


    @pyqtSignature('')
    def on_actAddProbe_triggered(self):
        probeId = newClientProbe(self, self._clientId, self._params())
        if probeId:
            self.updateProbeList(probeId)


    @pyqtSignature('')
    def on_actEditProbe_triggered(self):
        probeId = self.tblProbe.currentItemId()
        if probeId:
            probeId = openClientProbe(self, self._clientId, probeId)
            self.updateProbeList(probeId)


    @pyqtSignature('')
    def on_actDeleteProbe_triggered(self):
        index = self.tblProbe.currentIndex()
        row = index.row()
        if index.isValid() and self.modelProbe.confirmRemoveRow(self.tblProbe, row):
            self.modelProbe.removeRow(row)
            self.updateProbeList()


    @pyqtSignature('')
    def on_actFilterVaccineSchema_triggered(self):
        vaccineId = self.tblFilterVaccine.currentItemId()
        openVaccineSchema(self, vaccineId)


    @pyqtSignature('')
    def on_actAddMedicalExemption_triggered(self):
        medicalExemptionId = newClientMedicalExemption(self, self._clientId)
        if medicalExemptionId:
            self.updateMedicalExemptionList(medicalExemptionId)


    @pyqtSignature('')
    def on_actEditMedicalExemption_triggered(self):
        itemId = self.tblMedicalExemption.currentItemId()
        medicalExemptionId = openClientMedicalExemption(self, self._clientId, itemId)
        if medicalExemptionId:
            self.updateMedicalExemptionList(medicalExemptionId)


    @pyqtSignature('')
    def on_actDeleteMedicalExemption_triggered(self):
        index = self.tblMedicalExemption.currentIndex()
        row = index.row()
        if index.isValid() and self.modelMedicalExemption.confirmRemoveRow(self.tblMedicalExemption, row):
            self.modelMedicalExemption.removeRow(row)


    @pyqtSignature('int, int')
    def on_tabVaccinationSplitter_splitterMoved(self, pos, index):
        self.tabProbeSplitter.blockSignals(True)
        self.tabMedicalExemptionSplitter.blockSignals(True)
        self.tabProbeSplitter.moveSplitter(pos, index)
        self.tabMedicalExemptionSplitter.moveSplitter(pos, index)
        self.tabProbeSplitter.blockSignals(False)
        self.tabMedicalExemptionSplitter.blockSignals(False)


    @pyqtSignature('int, int')
    def on_tabProbeSplitter_splitterMoved(self, pos, index):
        self.tabVaccinationSplitter.blockSignals(True)
        self.tabMedicalExemptionSplitter.blockSignals(True)
        self.tabVaccinationSplitter.moveSplitter(pos, index)
        self.tabMedicalExemptionSplitter.moveSplitter(pos, index)
        self.tabVaccinationSplitter.blockSignals(False)
        self.tabMedicalExemptionSplitter.blockSignals(False)


    @pyqtSignature('int, int')
    def on_tabMedicalExemptionSplitter_splitterMoved(self, pos, index):
        self.tabVaccinationSplitter.blockSignals(True)
        self.tabProbeSplitter.blockSignals(True)
        self.tabProbeSplitter.moveSplitter(pos, index)
        self.tabVaccinationSplitter.moveSplitter(pos, index)
        self.tabVaccinationSplitter.blockSignals(False)
        self.tabProbeSplitter.blockSignals(False)


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelVaccination_currentChanged(self, current, previous):
        item = self.tblVaccination.currentItem()
        if item:
            vaccineId = forceInt(item.value('vaccine_id'))
            idList = QtGui.qApp.db.getIdList('rbInfection_rbVaccine', 'infection_id', 'vaccine_id=%d'%vaccineId)
            self.modelVaccineInfections.setCurrntInfectionIdList(idList)
        else:
            self.modelVaccineInfections.setCurrntInfectionIdList([])


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelMedicalExemption_currentChanged(self, current, previous):
        itemId = self.tblMedicalExemption.currentItemId()
        self.updateMedicalExemptionInfectionsList(itemId)


# ###########################################################################


class CClientVaccinationEditor(CItemEditorBaseDialog, Ui_ClientVaccinationEditor):
    def __init__(self, parent, clientId):
        CItemEditorBaseDialog.__init__(self, parent, 'ClientVaccination')

        self.setupUi(self)

        self.cmbRelegateOrg.setValue(QtGui.qApp.currentOrgId())
        self.cmbVaccine.setTable('rbVaccine', needCache=False)
        self.cmbReaction.setTable('rbReaction')
        self.cmbTransitionType.setTable('rbVaccine_SchemaTransitionType')
        self._clientId = clientId
        self.vaccineIdList = []

        self.setWindowTitleEx(u'Прививка')
        self.edtReactionDate.setDate(None)
        self.connect(QtGui.qApp, SIGNAL('sgtinReceived(QString)'), self.onSgtinReceived)

    @pyqtSignature('')
    def on_btnSelectRelegateOrg_clicked(self):
        orgId = selectOrganisation(self, self.cmbRelegateOrg.value(), False, filter=CPolyclinicComboBox.filter)
        self.cmbRelegateOrg.updateModel()
        if orgId:
            self.cmbRelegateOrg.setValue(orgId)


    def setParams(self, params):
#        vaccinationCalendarId = params.get('vaccinationCalendarId', None)
#        infectionIdList       = params.get('infectionIdList', None)
        self.vaccineIdList     = params.get('vaccineIdList', [])
#        personId              = params.get('personId', None)
        vaccinationType = params.get('vaccinationType')
        sgtin = params.get('sgtin')

        if self.vaccineIdList:
            self.cmbVaccine.setFilter(QtGui.qApp.db.table('rbVaccine')['id'].inlist(self.vaccineIdList))
            self.cmbVaccine.setValue(self.vaccineIdList[0])

            if vaccinationType:
                self.cmbVaccinationType.setText(vaccinationType)

        if sgtin:
            self.edtSgtin.setText(sgtin)
            self.edtSeria.setText(self.getBatch(sgtin))


#        if personId:
#            self.cmbPerson.setValue(personId)

    def getBatch(self, sgtin):
        return getBatch(unicode(sgtin)) or ''


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        self._clientId = forceRef(record.value('client_id'))
        setRBComboBoxValue(    self.cmbVaccine,         record, 'vaccine_id')
        setRBComboBoxValue(    self.cmbVaccineIdentification, record, 'vaccineIdentificationIBP_id')
        setDbComboBoxTextValue(self.cmbVaccinationType, record, 'vaccinationType')
        setDateEditValue(      self.edtDate,            record, 'datetime')
        setDoubleBoxValue(     self.edtDose,            record, 'dose')
        setLineEditValue(      self.edtSeria,           record, 'seria')
        setLineEditValue(      self.edtSgtin,           record, 'sgtin')
        setRBComboBoxValue(    self.cmbPerson,          record, 'person_id')
        setRBComboBoxValue(    self.cmbReaction,        record, 'reaction_id')
        setDateEditValue(      self.edtReactionDate,    record, 'reactionDate')
        setRBComboBoxValue(    self.cmbTransitionType,  record, 'transitionType_id')
        setRBComboBoxValue(    self.cmbRelegateOrg,     record, 'relegateOrg_id')


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        record.setValue('client_id', QVariant(self._clientId))
        getRBComboBoxValue(    self.cmbVaccine,         record, 'vaccine_id')
        getRBComboBoxValue(    self.cmbVaccineIdentification, record, 'vaccineIdentificationIBP_id')
        getDbComboBoxTextValue(self.cmbVaccinationType, record, 'vaccinationType')
        getDateEditValue(      self.edtDate,            record, 'datetime')
        getDoubleBoxValue(     self.edtDose,            record, 'dose')
        getLineEditValue(      self.edtSeria,           record, 'seria')
        getLineEditValue(      self.edtSgtin,           record, 'sgtin')
        getRBComboBoxValue(    self.cmbPerson,          record, 'person_id')
        getRBComboBoxValue(    self.cmbReaction,        record, 'reaction_id')
        getDateEditValue(      self.edtReactionDate,    record, 'reactionDate')
        getRBComboBoxValue(    self.cmbTransitionType,  record, 'transitionType_id')
        getRBComboBoxValue(    self.cmbRelegateOrg,     record, 'relegateOrg_id')
        if not forceDateTime(record.value('createDatetime')).toString(Qt.ISODate):
            record.setValue('createDatetime', toVariant(QDateTime().currentDateTime()))
        record.setValue('modifyDatetime', toVariant(QDateTime().currentDateTime()))
        return record


    def checkDataEntered(self):
        result = True

        vaccineId = self.cmbVaccine.value()
        result = result and (vaccineId or self.checkInputMessage(u'вакцина', False, self.cmbVaccine))

        vaccinationType = trim(self.cmbVaccinationType.text())
        result = result and (vaccinationType or self.checkInputMessage(u'тип прививки', False, self.cmbVaccinationType))

        date = self.edtDate.date()
        result = result and (date or self.checkInputMessage(u'дата', False, self.edtDate))

        dose = self.edtDose.value()
        result = result and (dose or self.checkInputMessage(u'доза', True, self.edtDose))

        seria = trim(self.edtSeria.text())
        result = result and (seria or self.checkInputMessage(u'серия', False, self.edtSeria))

        personId = self.cmbPerson.value()
        result = result and (personId or self.checkInputMessage(u'врач', False, self.cmbPerson))

        reactionId = self.cmbReaction.value()
        result = result and (reactionId or self.checkInputMessage(u'реакция', True, self.cmbReaction))

        transitionTypeId = self.cmbTransitionType.value()
        result = result and (transitionTypeId or self.checkInputMessage(u'дополнительно', True, self.cmbTransitionType))

        relegateOrgId = self.cmbRelegateOrg.value()
        result = result and (relegateOrgId or self.checkInputMessage(u'направитель', True, self.cmbRelegateOrg))

        return result


    def setDependentsByVaccineId(self, vaccineId):
        db = QtGui.qApp.db

        tableClienVaccination = db.table('ClientVaccination')
        tableCV = db.table('ClientVaccination').alias('CV')

        subCond = [tableCV['vaccine_id'].eq(vaccineId), tableCV['deleted'].eq(0)]
        subStmt = db.selectStmt(tableCV, 'MAX('+tableCV['id'].name()+')', subCond)

        cond = [tableClienVaccination['id'].name()+'=('+subStmt+')', tableClienVaccination['deleted'].eq(0)]

        record = db.getRecordEx(tableClienVaccination,
                                [tableClienVaccination['seria'],
                                 tableClienVaccination['person_id']
                                ],
                                cond)

        if record:
            seria = forceString(record.value('seria'))
            personId = forceRef(record.value('person_id'))

            self.edtSeria.setText(seria)
            self.cmbPerson.setValue(QtGui.qApp.userId if QtGui.qApp.userSpecialityId else personId)

        else:
            self.edtSeria.clear()
            self.cmbPerson.setValue(QtGui.qApp.userId if QtGui.qApp.userSpecialityId else None)


    def onSgtinReceived(self, sgtin):
        db = QtGui.qApp.db
        vaccineId, vaccinationType = findVaccineIdAndVaccinationTypeByGtin(gtin = sgtin[:14])
        if vaccineId:
            if vaccineId in self.vaccineIdList:
                self.cmbVaccine.setValue(vaccineId)
                if vaccinationType:
                    self.cmbVaccinationType.setText(vaccinationType)
                self.edtSgtin.setText(sgtin)
                self.edtSeria.setText(self.getBatch(sgtin))
            else:
                vaccineName = forceString(db.translate('rbVaccine', 'id', vaccineId, 'name'))
                QtGui.QMessageBox.warning(self,
                                          u'Внимание!',
                                          u'Сканированный код соответствует вакцине «%s»' % vaccineName
                                          )
        else:
            QtGui.QMessageBox.warning(self,
                                      u'Внимание!',
                                      u'Сканированный код не соответствует никакой вакцине'
                                      )
            self.edtSgtin.setText(sgtin)


    @pyqtSignature('int')
    def on_cmbVaccine_currentIndexChanged(self, index):
        vaccineId = self.cmbVaccine.value()

        if vaccineId:
            self.cmbVaccinationType.setFilter('master_id = %d' % vaccineId)
        self.cmbVaccineIdentification.setVaccineId(vaccineId)
        self.cmbVaccinationType.setEnabled(bool(vaccineId))

        self.edtDose.setValue(forceDouble(QtGui.qApp.db.translate('rbVaccine',
                                                                  'id',
                                                                  vaccineId,
                                                                  'dose')) if vaccineId else 0)

        self.setDependentsByVaccineId(vaccineId)


# ###########################################################################


class CClientProbeEditor(CItemEditorBaseDialog, Ui_ClientVaccinationProbeEditor):
    def __init__(self, parent, clientId):
        CItemEditorBaseDialog.__init__(self, parent, 'ClientVaccinationProbe')
        self.setupUi(self)
        self.cmbProbe.setTable('rbVaccinationProbe', needCache=False)
        self.cmbReaction.setTable('rbReaction')
        self.cmbResult.setTable('rbVaccinationResult')
        self.probeIdList = []
        self._clientId = clientId
        self.setWindowTitleEx(u'Проба')
        self.edtReactionDate.setDate(None)
        self.edtResultDate.setDate(None)
        self.cmbRelegateOrg.setValue(QtGui.qApp.currentOrgId())


    def setParams(self, params):
        self.probeIdList = params.get('probeIdList', [])
        if self.probeIdList:
            self.cmbProbe.setFilter(QtGui.qApp.db.table('rbVaccinationProbe')['id'].inlist(self.probeIdList))
            self.cmbProbe.setValue(self.probeIdList[0])


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        self._clientId = forceRef(record.value('client_id'))
        setRBComboBoxValue(    self.cmbProbe,           record, 'probe_id')
        setRBComboBoxValue(    self.cmbProbeIdentification, record, 'probeIdentificationIBP_id')
        setDateEditValue(      self.edtDate,            record, 'datetime')
        setDoubleBoxValue(     self.edtDose,            record, 'dose')
        setLineEditValue(      self.edtSeria,           record, 'seria')
        setRBComboBoxValue(    self.cmbPerson,          record, 'person_id')
        setRBComboBoxValue(    self.cmbReaction,        record, 'reaction_id')
        setDateEditValue(      self.edtReactionDate,    record, 'reactionDate')
        setRBComboBoxValue(    self.cmbRelegateOrg,     record, 'relegateOrg_id')
        setRBComboBoxValue(    self.cmbResult,          record, 'result_id')
        setDateEditValue(      self.edtResultDate,      record, 'resultDate')
        self.cmbProbeType.setCurrentIndex(forceInt(record.value('type')))


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        record.setValue('client_id', QVariant(self._clientId))
        record.setValue('type', toVariant(forceInt(self.cmbProbeType.currentIndex())))
        getRBComboBoxValue(    self.cmbProbe,           record, 'probe_id')
        getRBComboBoxValue(    self.cmbProbeIdentification, record, 'probeIdentificationIBP_id')
        getDateEditValue(      self.edtDate,            record, 'datetime')
        getDoubleBoxValue(     self.edtDose,            record, 'dose')
        getLineEditValue(      self.edtSeria,           record, 'seria')
        getRBComboBoxValue(    self.cmbPerson,          record, 'person_id')
        getRBComboBoxValue(    self.cmbReaction,        record, 'reaction_id')
        getDateEditValue(      self.edtReactionDate,    record, 'reactionDate')
        getRBComboBoxValue(    self.cmbRelegateOrg,     record, 'relegateOrg_id')
        getRBComboBoxValue(    self.cmbResult,          record, 'result_id')
        getDateEditValue(      self.edtResultDate,      record, 'resultDate')
        if not forceDateTime(record.value('createDatetime')).toString(Qt.ISODate):
            record.setValue('createDatetime', toVariant(QDateTime().currentDateTime()))
        record.setValue('modifyDatetime', toVariant(QDateTime().currentDateTime()))
        return record


    @pyqtSignature('int')
    def on_cmbProbe_currentIndexChanged(self, index):
        probeId = self.cmbProbe.value()
        self.cmbProbeIdentification.setVaccinationProbeId(probeId)

    @pyqtSignature('')
    def on_btnSelectRelegateOrg_clicked(self):
        orgId = selectOrganisation(self, self.cmbRelegateOrg.value(), False, filter=CPolyclinicComboBox.filter)
        self.cmbRelegateOrg.updateModel()
        if orgId:
            self.cmbRelegateOrg.setValue(orgId)

    def checkDataEntered(self):
        result = True
        probeId = self.cmbProbe.value()
        result = result and (probeId or self.checkInputMessage(u'вакцина', False, self.cmbProbe))
        date = self.edtDate.date()
        result = result and (date or self.checkInputMessage(u'дата', False, self.edtDate))
        personId = self.cmbPerson.value()
        result = result and (personId or self.checkInputMessage(u'врач', False, self.cmbPerson))
        reactionId = self.cmbReaction.value()
        result = result and (reactionId or self.checkInputMessage(u'реакция', True, self.cmbReaction))
        relegateOrgId = self.cmbRelegateOrg.value()
        result = result and (relegateOrgId or self.checkInputMessage(u'направитель', True, self.cmbRelegateOrg))
        resultId = self.cmbResult.value()
        result = result and (resultId or self.checkInputMessage(u'результат', True, self.cmbResult))
        return result


# ###########################################################################


class CClientMedicalExemptionEditor(CItemEditorBaseDialog, Ui_ClientMedicalExemptionEditor):
    def __init__(self, parent, clientId):
        CItemEditorBaseDialog.__init__(self, parent, 'ClientMedicalExemption')
        self.addModels(u'MedicalExemptionInfections', CMedicalExemptionInfectionsInDocTableModel(self))
        self.setupUi(self)
        self._clientId = clientId
        self.cmbMedicalExemptionType.setTable('rbMedicalExemptionType', addNone=True)
        self.cmbMedicalExemptionReason.setTable('rbMedicalExemptionReason', addNone=True)
        self.edtEndDate.setDate(QDate())
        self.setModels(self.tblMedicalExemptionInfections,
                       self.modelMedicalExemptionInfections,
                       self.selectionModelMedicalExemptionInfections)
        self.setWindowTitleEx(u'Медотвод')


    def setParams(self, params):
        pass


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        self._clientId = forceRef(record.value('client_id'))
        setDateEditValue(  self.edtDate,                record, 'date')
        self.cmbMKB.setText(forceString(record.value('MKB')))
        setRBComboBoxValue(self.cmbPerson,                 record, 'person_id')
        setDateEditValue(  self.edtEndDate,                record, 'endDate')
        setRBComboBoxValue(self.cmbMedicalExemptionType,   record, 'medicalExemptionType_id')
        setRBComboBoxValue(self.cmbMedicalExemptionReason, record, 'medicalExemptionReason_id')
        self.modelMedicalExemptionInfections.loadItems(self.itemId())


    def getRecord(self):
        record = CItemEditorBaseDialog.getRecord(self)
        record.setValue('client_id', QVariant(self._clientId))
        getDateEditValue(  self.edtDate,                record, 'date')
        record.setValue('MKB', QVariant(self.cmbMKB.text()))
        getRBComboBoxValue(self.cmbPerson,                 record, 'person_id')
        getDateEditValue(  self.edtEndDate,                record, 'endDate')
        getRBComboBoxValue(self.cmbMedicalExemptionType,   record, 'medicalExemptionType_id')
        getRBComboBoxValue(self.cmbMedicalExemptionReason, record, 'medicalExemptionReason_id')
        return record


    def saveInternals(self, id):
        self.modelMedicalExemptionInfections.saveItems(id)


    def checkDataEntered(self):
        result = True
        date = self.edtDate.date()
        result = result and (date or self.checkInputMessage(u'дата', False, self.edtDate))
        result = result and (self.cmbPerson.value() or self.checkInputMessage(u'врач', True, self.cmbPerson))
        result = result and self.checkMedicalExemptionInfections()
        return result


    def checkMedicalExemptionInfections(self):
        for row, item in enumerate(self.modelMedicalExemptionInfections.items()):
            infectionId = forceRef(item.value('infection_id'))
            if not infectionId:
                return self.checkInputMessage(u'инфекцию', False, self.tblMedicalExemptionInfections, row, 0)
        return True


# ###########################################################################


class CVaccineInfectionsTableModel(CTableModel):
    def __init__(self, parent):
        cols = [CRefBookCol(u'Инфекция', ['id'], 'rbInfection', 12, showFields=2)]
        CTableModel.__init__(self, parent, cols=cols, tableName='rbInfection')
        self._currentInfectionIdList = []
        boldFont = QtGui.QFont()
        boldFont.setWeight(QtGui.QFont.Bold)
        self._qBoldFont = QVariant(boldFont)
        self._mapColumnToOrder ={'id' :'rbInfection.code'}


    def setCurrntInfectionIdList(self, currentInfectionIdList):
        if self._currentInfectionIdList != currentInfectionIdList:
            self._currentInfectionIdList = currentInfectionIdList
            self.emitDataChanged()


    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.FontRole:
            column = index.column()
            row = index.row()
            (col, values) = self.getRecordValues(column, row)
            if forceRef(values[0]) in self._currentInfectionIdList:
                return self._qBoldFont
        else:
            return CTableModel.data(self, index, role)


# ###########################################################################

class CVaccinationTableModel(CTableModel):
    class CLocDoseCol(CNumCol):

        locale = QLocale()

        def format(self, values):
            sum = forceDouble(values[0])
            return toVariant(self.locale.toString(sum, 'f', 3))


    def __init__(self, parent):
        cols = [CIntCol(u'Код', ['id'], 10),
                CRefBookCol(u'Вакцина', ['vaccine_id'], 'rbVaccine', 12, showFields=2),
                CTextCol(u'Тип прививки', ['vaccinationType'], 10),
                CDateCol(u'Дата', ['datetime'], 8),
                CVaccinationTableModel.CLocDoseCol(u'Доза', ['dose'], 8),
                CTextCol(u'Серия', ['seria'], 10),
                CRefBookCol(u'Врач', ['person_id'], 'vrbPersonWithSpeciality', 10),
                CRefBookCol(u'Реакция', ['reaction_id'], 'rbReaction', 10),
                CDateCol(u'Дата реакции', ['reactionDate'], 8),
                CRefBookCol(u'Дополнительно', ['transitionType_id'], 'rbVaccine_SchemaTransitionType', 10),
                CDesignationCol(u'Направитель', ['relegateOrg_id'], ('Organisation', 'shortName'), 10)]
        CTableModel.__init__(self, parent, cols=cols, tableName='ClientVaccination')
        self._mapColumnToOrder = {'id'                 : 'ClientVaccination.id',
                                  'vaccine_id'         : 'rbVaccine.code',
                                  'vaccinationType'    : 'ClientVaccination.vaccinationType',
                                  'datetime'           : 'ClientVaccination.datetime',
                                  'dose'               : 'ClientVaccination.dose',
                                  'seria'              : 'ClientVaccination.seria',
                                  'person_id'          : 'vrbPersonWithSpeciality.name',
                                  'reaction_id'        : 'rbReaction.name',
                                  'reactionDate'       : 'ClientVaccination.reactionDate',
                                  'transitionType_id'  : 'rbVaccine_SchemaTransitionType.name',
                                  'relegateOrg_id'     : 'Organisation.shortName'
                                  }


# ###########################################################################


class CProbeTableModel(CTableModel):

    class CLocDoseCol(CNumCol):
        locale = QLocale()

        def format(self, values):
            sum = forceDouble(values[0])
            return toVariant(self.locale.toString(sum, 'f', 3))


    def __init__(self, parent):
        cols = [CIntCol(u'Код', ['id'], 10),
                CRefBookCol(u'Проба', ['probe_id'], 'rbVaccinationProbe', 12, showFields=2),
                CDateCol(u'Дата', ['datetime'], 8),
                CProbeTableModel.CLocDoseCol(u'Доза', ['dose'], 8),
                CTextCol(u'Серия', ['seria'], 10),
                CRefBookCol(u'Врач', ['person_id'], 'vrbPersonWithSpeciality', 10),
                CRefBookCol(u'Реакция', ['reaction_id'], 'rbReaction', 10),
                CDateCol(u'Дата реакции', ['reactionDate'], 8),
                CDesignationCol(u'Направитель', ['relegateOrg_id'], ('Organisation', 'shortName'), 10),
                CRefBookCol(u'Результат', ['result_id'], 'rbVaccinationResult', 10),
                CDateCol(u'Дата результата', ['resultDate'], 8)]
        CTableModel.__init__(self, parent, cols=cols, tableName='ClientVaccinationProbe')
        self._mapColumnToOrder = {'id'                 : 'ClientVaccinationProbe.id',
                                  'probe_id'           : 'rbVaccinationProbe.code',
                                  'datetime'           : 'ClientVaccinationProbe.datetime',
                                  'dose'               : 'ClientVaccinationProbe.dose',
                                  'seria'              : 'ClientVaccinationProbe.seria',
                                  'person_id'          : 'vrbPersonWithSpeciality.name',
                                  'reaction_id'        : 'rbReaction.name',
                                  'reactionDate'       : 'ClientVaccinationProbe.reactionDate',
                                  'relegateOrg_id'     : 'Organisation.shortName',
                                  'result_id'          : 'rbVaccinationResult.name'
                                  }


class CProbeLeftoverSchemaTableModel(CTableModel):
    def __init__(self, parent):
        cols = [CRefBookCol(u'Инфекция', ['id'], 'rbInfection', 12, showFields=2)]
        CTableModel.__init__(self, parent, cols=cols, tableName='rbInfection')
        self._currentInfectionIdList = []
        boldFont = QtGui.QFont()
        boldFont.setWeight(QtGui.QFont.Bold)
        self._qBoldFont = QVariant(boldFont)
        self._mapColumnToOrder ={'id' :'rbInfection.code'}


    def setCurrntInfectionIdList(self, currentInfectionIdList):
        if self._currentInfectionIdList != currentInfectionIdList:
            self._currentInfectionIdList = currentInfectionIdList
            self.emitDataChanged()


    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.FontRole:
            column = index.column()
            row = index.row()
            (col, values) = self.getRecordValues(column, row)
            if forceRef(values[0]) in self._currentInfectionIdList:
                return self._qBoldFont
        else:
            return CTableModel.data(self, index, role)

# ###########################################################################


class CMedicalExemptionModel(CTableModel):
    def __init__(self, parent):
        cols = [CDateCol(u'Дата', ['date'], 8),
                CTextCol(u'МКБ', ['MKB'], 8),
                CRefBookCol(u'Врач', ['person_id'], 'vrbPersonWithSpeciality', 10),
                CDateCol(u'Дата окончания', ['endDate'], 8),
                CRefBookCol(u'Тип медотвода', ['medicalExemptionType_id'], 'rbMedicalExemptionType', 10)
               ]
        CTableModel.__init__(self, parent, cols=cols, tableName='ClientMedicalExemption')
        self._mapColumnToOrder ={ 'date'                    :'ClientMedicalExemption.date',
                                  'MKB'                     :'ClientMedicalExemption.MKB',
                                  'person_id'               :'vrbPersonWithSpeciality.name',
                                  'endDate'                 :'ClientMedicalExemption.endDate',
                                  'medicalExemptionType_id' :'rbMedicalExemptionType.name'
                                }


# ###########################################################################


class CMedicalExemptionInfectionsModel(CTableModel):
    def __init__(self, parent):
        cols = [CRefBookCol(u'Инфекция', ['infection_id'], 'rbInfection', 10, showFields=2)
               ]
        CTableModel.__init__(self, parent, cols=cols, tableName='ClientMedicalExemption_Infection')
        self._mapColumnToOrder ={'infection_id' :'rbInfection.code'}


# ###########################################################################


class CMedicalExemptionInfectionsInDocTableModel(CInDocTableModel):
    def __init__(self, parent):
        CInDocTableModel.__init__(self, 'ClientMedicalExemption_Infection', 'id', 'master_id',   parent)
        self.addCol(CRBInDocTableCol(  u'Инфекция', 'infection_id', 20, 'rbInfection'))
