# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2017 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from os import path

from PyQt4 import QtGui, QtSql
from PyQt4.QtCore import Qt, pyqtSignature, SIGNAL, QDate, QDateTime, QString, QVariant

from library.DialogBase      import CConstructHelperMixin, CDialogBase
from library.InDocTable      import CInDocTableCol, CInDocTableView, CRecordListModel
from library.Utils           import forceBool, forceDate, forceInt, forceRef, forceString, forceStringEx, nameCase, trim, withWaitCursor

#from library.DialogButtonBox import CApplyResetDialogButtonBox
from library.crbcombobox     import CRBModelDataCache
from library.PrintTemplates  import customizePrintButton, applyTemplate
from library.PrintInfo       import CInfoContext


from RefBooks.Equipment.Protocol           import CEquipmentProtocol
from RefBooks.Equipment.RoleInIntegration  import CEquipmentRoleInIntegration

from TissueJournal.LabInterface            import sendTests, readResultOverASTM
try:
    from TissueJournal.LabInterfaceFHIR    import pickupResultsOverFHIR as pickupResultsOverFHIR050
    from TissueJournal.LabInterfaceFHIR102 import pickupResultsOverFHIR as pickupResultsOverFHIR102
    FHIRisOk = True
except:
    FHIRisOk = False

from TissueJournal.TissueJournalModels import CSamplePreparationModel, CSamplingOnlyProbesModel, CSamplingOnlyTestsModel
from TissueJournal.TissueInfo          import CWorkListInfo
from TissueJournal.Utils               import getEquipmentInterface, getEquipmentFilterByOrgStructureId

from Ui_ProbeWorkListPage    import Ui_ProbeWorkListWidget

probeInWaiting = 1
probeSent2LIS = 6

class CProbeWorkListPage(QtGui.QWidget, CConstructHelperMixin, Ui_ProbeWorkListWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self._isInitialized = False


    def isInitialized(self):
        return self._isInitialized


    def initializedProbeWorkList(self):
        if not self.isInitialized():
            self._filter = {}
            self._mapEquipmentId2TripodCount = {}

            validator  = QtGui.QIntValidator(0, 1000, self.edtPWLTripodNumber)
            self.edtPWLTripodNumber.setValidator(validator)

            # setup comboboxes
            orgStructureId = QtGui.qApp.currentOrgStructureId()
            cmbEquipmentFilter = 'status=1 AND roleInIntegration in %s' % ((CEquipmentRoleInIntegration.external, CEquipmentRoleInIntegration.internal),)
            if orgStructureId:
                cmbEquipmentFilter = '(%s) AND (%s)' % ( cmbEquipmentFilter, getEquipmentFilterByOrgStructureId(orgStructureId))

            self.cmbPWLEquipment.setTable(       'rbEquipment',         addNone=True, filter=cmbEquipmentFilter)
            self.cmbPWLTestGroup.setTable(       'rbTestGroup',         addNone=True)
            self.cmbPWLTest.setTable(            'rbTest',              addNone=True)
            self.cmbPWLTissueType.setTable(      'rbTissueType',        addNone=True)
            self.cmbPWLContainerType.setTable(   'rbContainerType',     addNone=True)
            self.cmbPWLAccountingSystem.setTable('rbAccountingSystem',  addNone=True)
            self.cmbPWLPerson.addNotSetValue()

            #setup models
            self.addModels('SamplingPreparation', CSamplePreparationModel(self))
            self.addModels('SamplingOnlyProbes',  CSamplingOnlyProbesModel(self, self.modelSamplingPreparation))
            self.addModels('SamplingOnlyTests',   CSamplingOnlyTestsModel(self,  self.modelSamplingPreparation))

            self.setModels(self.tblPWLProbe,      self.modelSamplingPreparation, self.selectionModelSamplingPreparation)
            self.setModels(self.tblPWLOnlyProbes, self.modelSamplingOnlyProbes,  self.selectionModelSamplingOnlyProbes)
            self.setModels(self.tblPWLOnlyTests,  self.modelSamplingOnlyTests,   self.selectionModelSamplingOnlyTests)

            self.tblPWLOnlyProbes.addPopupDelRow()

            self.resetFilter()
            self.setProbes()

            customizePrintButton(self.btnPWLPrint, 'tissueJournalWorkList')
            self.connect(self.btnPWLPrint, SIGNAL('printByTemplate(int)'), self.printWorkList)

            self.addBarcodeScanAction('actPWLScanBarcode')
            self.addAction(self.actPWLScanBarcode)
            self.connect(self.actPWLScanBarcode, SIGNAL('triggered()'), self.on_actPWLScanBarcode_triggered)
            self.connect(self.selectionModelSamplingOnlyProbes,
                         SIGNAL('currentRowChanged(QModelIndex, QModelIndex)'),
                         self.on_selectionModelSamplingOnlyProbes_currentRowChanged)

            self._isInitialized = True


    def on_actPWLScanBarcode_triggered(self):
        self.edtPWLProbeIdentifier.setFocus(Qt.OtherFocusReason)
        self.edtPWLProbeIdentifier.selectAll()


    def setProbes(self, force=False):
        QtGui.qApp.setWaitCursor()

        db = QtGui.qApp.db
        tableProbe                = db.table('Probe')
        tableTest                 = db.table('rbTest')
        tableTissueJournal        = db.table('TakenTissueJournal')
        tableAction               = db.table('Action')
        tableEvent                = db.table('Event')
        tableClient               = db.table('Client')
        tableIdentification       = db.table('ClientIdentification')
#        tableActionTypeTissueType = db.table('ActionType_TissueType')

        begDate            = self._filter.get('dateFrom', QDate())
        endDate            = self._filter.get('dateTo', QDate())
        equipmentId        = self._filter.get('equipmentId', None)
        tripodNumber       = self._filter.get('tripodNumber', None)
        testGroupId        = self._filter.get('testGroupId', None)
        testId             = self._filter.get('testId', None)
        status             = self._filter.get('status', 0) # не забыть учитывать съезд на 1
        tissueTypeId       = self._filter.get('tissueTypeId', None)
        chkRelegateOrg     = self._filter.get('chkPWLRelegateOrg', False)
        relegateOrgId      = self._filter.get('PWLRelegateOrgId', None)
        ibm                = self._filter.get('ibm', '')
        probeIdentifier    = self._filter.get('probeIdentifier', '')
        isUrgent           = self._filter.get('isUrgent', False)
        containerTypeId    = self._filter.get('containerTypeId', None)
        personId           = self._filter.get('personId', None)

        clientFilter       = self._filter.get('clientFilter', False)
        chkClientId        = self._filter.get('chkClientId', False)
        accountingSystemId = self._filter.get('accountingSystemId', None)
        clientId           = self._filter.get('clientId', None)
        chkPWLLastName     = self._filter.get('chkPWLLastName', False)
        lastName           = self._filter.get('lastName', None)
        chkPWLFirstName    = self._filter.get('chkPWLFirstName', False)
        firstName          = self._filter.get('firstName', None)
        chkPWLPatrName     = self._filter.get('chkPWLPatrName', False)
        patrName           = self._filter.get('patrName', None)
        chkPWLBirthDay     = self._filter.get('chkPWLBirthDay', False)
        birthDay           = self._filter.get('birthDay', None)

        queryTable = tableProbe.leftJoin(tableTissueJournal,
                                         tableTissueJournal['id'].eq(tableProbe['takenTissueJournal_id']))

        if clientFilter:
            queryTable = queryTable.leftJoin(tableClient, tableClient['id'].eq(tableTissueJournal['client_id']))

        cond = []
        if begDate:
            cond.append(tableTissueJournal['datetimeTaken'].dateGe(begDate))
        if endDate:
            cond.append(tableTissueJournal['datetimeTaken'].dateLe(endDate))
        if tissueTypeId:
            cond.append(tableTissueJournal['tissueType_id'].eq(tissueTypeId))
        if equipmentId:
            cond.append(tableProbe['equipment_id'].eq(equipmentId))
        if tripodNumber:
            cond.append(tableProbe['tripodNumber'].eq(tripodNumber))
        if testGroupId:
            queryTable = queryTable.leftJoin(tableTest, tableTest['id'].eq(tableProbe['test_id']))
            cond.append(tableTest['testGroup_id'].eq(testGroupId))
        if testId:
            cond.append(tableProbe['test_id'].eq(testId))
        if status:
            cond.append(tableProbe['status'].eq(status-1))
        if chkRelegateOrg:
            queryTable = queryTable.leftJoin(
                tableAction, tableTissueJournal['parent_id'].eq(tableAction['takenTissueJournal_id'])
            )

            queryTable = queryTable.leftJoin(tableEvent,
                                             tableEvent['id'].eq(tableAction['event_id']))
            if not relegateOrgId or relegateOrgId == QtGui.qApp.currentOrgId():
                cond.append(
                            db.joinOr([tableEvent['relegateOrg_id'].eq(QtGui.qApp.currentOrgId()),
                                       tableEvent['relegateOrg_id'].isNull()])
                           )
            else:
                cond.append(tableEvent['relegateOrg_id'].eq(relegateOrgId))
        if ibm:
            cond.append(tableTissueJournal['externalId'].eq(ibm))
        if probeIdentifier:
            cond.append(tableProbe['externalId'].eq(probeIdentifier))
        if isUrgent:
            cond.append(tableProbe['isUrgent'].eq(isUrgent))
        if clientFilter:
            if chkClientId:
                if accountingSystemId:
                    queryTable = queryTable.innerJoin(tableIdentification,
                                                      tableIdentification['client_id'].eq(tableClient['id']))
                    cond.append(tableIdentification['accountingSystem_id'].eq(accountingSystemId))
                    cond.append(tableIdentification['identifier'].eq(clientId))
                else:
                    cond.append(tableClient['id'].eq(clientId))
            else:
                if chkPWLFirstName:
                    cond.append(tableClient['firstName'].eq(firstName))
                if chkPWLLastName:
                    cond.append(tableClient['lastName'].eq(lastName))
                if chkPWLPatrName:
                    cond.append(tableClient['patrName'].eq(patrName))
                if chkPWLBirthDay and birthDay:
                    cond.append(tableClient['birthDate'].dateEq(birthDay))

        if containerTypeId:
            cond.append(tableProbe['containerType_id'].eq(containerTypeId))
        if personId:
            if personId == -1:
                cond.append(tableProbe['person_id'].isNull())
            else:
                cond.append(tableProbe['person_id'].eq(personId))
        cond = cond if cond else '1'

        if equipmentId:
            order = [tableProbe['tripodNumber'].name(),
                     tableProbe['placeInTripod'].name(),
                     tableTissueJournal['number'].name()]
        else:
            order = ''

        idList = db.getDistinctIdList(queryTable, tableProbe['id'].name(), cond, order=order)

        if self.modelSamplingPreparation.setIdList(idList, force):
            cti = self.tabWidgetPWL.currentIndex()
            if cti == 0:
                tbl = self.tblPWLOnlyProbes
            else:
                tbl = self.tblPWLProbe
            tbl.setFocus(Qt.OtherFocusReason)
            if idList:
                tbl.setCurrentIndex(tbl.model().index(0, 0))
                if cti == 0:
                    index = tbl.currentIndex()
                    self.on_selectionModelSamplingOnlyProbes_currentRowChanged(index, index)

        self.updateProbeCountLabel()
        QtGui.qApp.restoreOverrideCursor()


    def updateProbeCountLabel(self):
        self.lblProbeCount.setText(u'Количество проб: %d'%len(self.modelSamplingPreparation.idList()))
        self.lblOnlyProbesCount.setText(u'Количество: %d'%self.modelSamplingOnlyProbes.rowCount())


    def updateOnlyTestsCountLabel(self):
        self.lblOnlyTestsCount.setText(u'Количество: %d'%self.modelSamplingOnlyTests.rowCount())


    def isExistEquipmentTripod(self, equipmentId):
        return bool(QtGui.qApp.db.translate('rbEquipment', 'id', equipmentId, 'tripod'))


    def updateFilter(self):
        self._filter.clear()
        equipmentId = self.cmbPWLEquipment.value()
        self.btnPWLTripod.setEnabled(self.isExistEquipmentTripod(equipmentId))
        self._filter['equipmentId'] = equipmentId
        if equipmentId:
            sTripodNumber = trim(self.edtPWLTripodNumber.text())
            self._filter['tripodNumber'] = int(sTripodNumber) if sTripodNumber else None
        self._filter['testGroupId'] = self.cmbPWLTestGroup.value()
        self._filter['testId'] = self.cmbPWLTest.value()
        self._filter['status'] = self.cmbPWLStatus.currentIndex()
        self._filter['dateFrom'] = self.edtPWLDateFrom.date()
        self._filter['dateTo'] = self.edtPWLDateTo.date()
        self._filter['tissueTypeId'] = self.cmbPWLTissueType.value()
        self._filter['chkPWLRelegateOrg'] = self.chkPWLRelegateOrg.isChecked()
        self._filter['PWLRelegateOrgId'] = self.cmbPWLRelegateOrg.value()
        self._filter['ibm'] = forceStringEx(self.edtPWLIbm.text())
        self._filter['probeIdentifier'] = forceStringEx(self.edtPWLProbeIdentifier.text())
        self._filter['isUrgent'] = self.chkPWLIsUrgent.isChecked()
        self._filter['containerTypeId'] = self.cmbPWLContainerType.value()
        self._filter['personId'] = self.cmbPWLPerson.value()
        self._filter['clientFilter'] = self.grpClient.isChecked()
        if self._filter['clientFilter']:
            self._filter['chkClientId']        = self.chkPWLId.isChecked()
            self._filter['accountingSystemId'] = self.cmbPWLAccountingSystem.value()
            self._filter['clientId']           = forceStringEx(self.edtPWLId.text())
            self._filter['chkPWLLastName']     = self.chkPWLLastName.isChecked()
            self._filter['lastName']           = nameCase(forceStringEx(self.edtPWLLastName.text()))
            self._filter['chkPWLFirstName']    = self.chkPWLFirstName.isChecked()
            self._filter['firstName']          = nameCase(forceStringEx(self.edtPWLFirstName.text()))
            self._filter['chkPWLPatrName']     = self.chkPWLPatrName.isChecked()
            self._filter['patrName']           = nameCase(forceStringEx(self.edtPWLPatrName.text()))
            self._filter['chkPWLBirthDay']     = self.chkPWLBirthDay.isChecked()
            self._filter['birthDay']           = self.edtPWLBirthDay.date()


    def resetFilter(self):
        self.cmbPWLEquipment.setValue(None)
        self.edtPWLTripodNumber.clear()
        self.cmbPWLTestGroup.setValue(None)
        self.cmbPWLTest.setValue(None)
        self.cmbPWLTissueType.setValue(None)
        self.cmbPWLStatus.setCurrentIndex(0)
        self.edtPWLDateFrom.setDate(QDate.currentDate())
        self.edtPWLDateTo.setDate(QDate.currentDate())
        self.cmbPWLRelegateOrg.setValue(None)
        self.chkPWLRelegateOrg.setChecked(False)
        self.edtPWLIbm.clear()
        self.edtPWLProbeIdentifier.clear()
        self.chkPWLIsUrgent.setChecked(False)
        self.cmbPWLContainerType.setValue(None)
        self.cmbPWLPerson.setValue(None)
        self.grpClient.setChecked(False)
        self.chkPWLId.setChecked(False)
        self.cmbPWLAccountingSystem.setValue(None)
        self.edtPWLId.setText('')
        self.chkPWLLastName.setChecked(False)
        self.edtPWLLastName.setText('')
        self.chkPWLFirstName.setChecked(False)
        self.edtPWLFirstName.setText('')
        self.chkPWLPatrName.setChecked(False)
        self.edtPWLPatrName.setText('')
        self.chkPWLBirthDay.setChecked(False)
        self.edtPWLBirthDay.setDate(None)
        self.updateFilter()


    def getEquipmentTripodCount(self, equipmentId):
        result = self._mapEquipmentId2TripodCount.get(equipmentId, None)
        if result is None:
            tripod = QtGui.qApp.db.translate('rbEquipment', 'id', equipmentId, 'tripod')
            result = (len(tripod.toString().split(';', QString.SkipEmptyParts))) if tripod else 0
            self._mapEquipmentId2TripodCount[equipmentId] = result
        return result


    def getAbsProbeCount(self, probeId):
        return self.modelSamplingPreparation.originalProbeTestsCount(probeId)


    def originalProbeTestsIdList(self, probeId):
        return self.modelSamplingPreparation.originalProbeTestsIdList(probeId)


    def getOriginalProbeItemsList(self, probeId):
        return self.modelSamplingPreparation.getOriginalProbeItemsList(probeId)


    # tuple (Exchange.Lab.AstmE1381.FileExchangeLoop.CFileMessage, Exchange.Lab.AstmE1394.CMessage)
#    def applyEquipmentMessage(self, progressBar, message, dataFileName, rewrite, onlyFromModel, equipmentId):

    def applyEquipmentMessage(self, labInterface):
        def _list2Tuple(val):
            if isinstance(val, (list,  tuple)):
                return tuple(_list2Tuple(x) for x in val)
            else:
                return val

        def _messageSize(message):
            return sum( sum(len(o.results)
                            for o in p.orders
                           )
                        for p in message.patients
                      )

        def _setupProgressBar(progressBar, messageList):
            maxVal = sum( _messageSize(message)
                          for message, messageHandler, equipmentId in messageList
                        )
#            progressBar.setFormat(u'%s [%%d/%%m]' % title)
            progressBar.setMinimum(0)
            progressBar.setMaximum(maxVal)
#            progressBar.setValue(0)
        db = QtGui.qApp.db
        rewrite = labInterface.chkRewrite.isChecked()
        onlyFromModel = labInterface.chkOnlyFromModel.isChecked()

        try:
            QtGui.qApp.setWaitCursor()
            _setupProgressBar(labInterface.progressBar, labInterface.messageList())
            progressPassed = 0
            progressMinimumValue = labInterface.progressBar.minimum()
            progressMaximumValue = labInterface.progressBar.maximum()
            for messageValues in labInterface.messageList():
                db.transaction()
                try:
                    message, messageHandler, equipmentId = messageValues
                    dataFileName = path.split(messageHandler.dataFilePatch)[1]
                    labInterface.progressBar.setFormat(u'%s [%%v из %d]' % (dataFileName, _messageSize(message)))
                    labInterface.progressBar.setMinimum(progressMinimumValue - progressPassed)
                    labInterface.progressBar.setMaximum(progressMaximumValue - progressPassed)
                    labInterface.progressBar.setValue(0)

                    self.modelSamplingPreparation.resetItemWithoutImportValueHelper()
                    resultMap = {}
                    resultOnFact = forceBool(QtGui.qApp.db.translate('rbEquipment', 'id', equipmentId, 'resultOnFact'))
                    for p in message.patients:
                        for o in p.orders:
                            for r in o.results:
                                arg = {'clientId'           : p.patientId,
                                       'laboratoryPatientId': p.laboratoryPatientId,
                                       'clientId3'          : p.reservedPatientId,
                                       'externalId'         : o.specimenId,
                                       'testId_like_code'   : r.testId,
                                       'testCode'           : r.assayCode,
                                       'testName'           : r.assayName,
                                       'value'              : r.value,
                                       'referenceRange'     : r.referenceRange,
                                       'abnormalFlags'      : r.abnormalFlags,
                                       'unit'               : r.unit,
                                       'resultStatus'       : r.status,
                                       'assistantCode'      : r.operator1,
                                       'personCode'         : r.operator2,
                                       'rewrite'            : rewrite,
                                       'onlyFromModel'      : onlyFromModel,
                                       'filterEquipmentId'  : self._filter.get('equipmentId', None),
                                       'equipmentId'        : equipmentId,
                                       'dataFileName'       : dataFileName,
                                       'resultOnFact'       : resultOnFact,
                                       'resultType'         : r.resultType,
                                       'instrumentSpecimenId' : o.instrumentSpecimenId,
                                       'instrumentSpecimenIndex' : o.instrumentSpecimenIndex}
                                labInterface.progressBar.step()
                                progressPassed += 1
                                QtGui.qApp.processEvents()
                                result = self.modelSamplingPreparation.setResult(arg)
                                resultKey = _list2Tuple([p.patientId, o.specimenId, r.testId, r.assayCode, r.assayName, r.value, r.referenceRange, r.unit])
                                resultMap[resultKey] = result
                    labInterface.logOnImport(message, resultMap)
                    resultList = resultMap.values()
                    if all(result == labInterface.importResultOk for result in resultList):
                        messageHandler.dismiss()
                    self.modelSamplingPreparation.applayItemWithoutImportValue()
                    db.commit()
                except:
                    db.rollback()
                    raise
            self.setProbes(force=True)
        except Exception, e:
            QtGui.qApp.logCurrentException()
            labInterface.logException()
            QtGui.QMessageBox.critical(self, u'Внимание!', u'При импорте данных произошла ошибка!\n"%s"'%unicode(e))
        finally:
            QtGui.qApp.restoreOverrideCursor()



    @pyqtSignature('')
    def on_btnPWLTripod_clicked(self):
        dlg = CTripodProbeLoaderDialog(self, self.cmbPWLEquipment.value())
        probeIdList = []
        for row in range(self.modelSamplingOnlyProbes.rowCount()):
            probeId = self.modelSamplingOnlyProbes.getId(row)
            probeItem = self.modelSamplingPreparation.getItemById(probeId)
            if forceInt(probeItem.value('status')) not in (CSamplePreparationModel.probeIsFinished,
                                                           CSamplePreparationModel.probeWithoutResult):
                probeIdList.append(probeId)
        dlg.setProbeIdList(probeIdList)
        dlg.exec_()
        self.setProbes(force=True)


    @pyqtSignature('int')
    def on_cmbPWLEquipment_currentIndexChanged(self, index):
        equipmentId = self.cmbPWLEquipment.value()
        self.edtPWLTripodNumber.setEnabled(bool(self.getEquipmentTripodCount(equipmentId)))


    @pyqtSignature('')
    def on_btnPWLImport_clicked(self):
        @withWaitCursor
        def pickupResultsOverFHIR050Int(equipmentInterface, probeIdList):
            QtGui.qApp.call(self, pickupResultsOverFHIR050, (self, equipmentInterface, probeIdList))
        @withWaitCursor
        def pickupResultsOverFHIR102Int(equipmentInterface, probeIdList):
            QtGui.qApp.call(self, pickupResultsOverFHIR102, (self, equipmentInterface, probeIdList))
        # Это, по факту, ошибка.
        # как мне кажется этот диалог и его устройство нехороши.
        # Не случайно Антон не нашёл способа подружить анализаторы мочи с этим диалогом.
        equipmentId = self._filter.get('equipmentId')
        if equipmentId: # and False:
            equipmentInterface = getEquipmentInterface(equipmentId)
            if equipmentInterface.protocol == CEquipmentProtocol.fhir050:
                if FHIRisOk:
                    pickupResultsOverFHIR050Int(equipmentInterface, None)
#                    QtGui.qApp.call(self, pickupResultsOverFHIR, (self, equipmentInterface, None))
                else:
                    raise Exception('FHIR support is disabled')
                return
            elif equipmentInterface.protocol == CEquipmentProtocol.fhir102:
                if FHIRisOk:
                    pickupResultsOverFHIR102Int(equipmentInterface, None)
#                    QtGui.qApp.call(self, pickupResultsOverFHIR, (self, equipmentInterface, None))
                else:
                    raise Exception('FHIR support is disabled')
                return

        allItems = self.modelSamplingPreparation.items()
#        selectedRows = self.tblPWLProbe.getSelectedRows()
#        items = [allItems[row] for row in selectedRows]
        items, idList = getActual(allItems, (probeSent2LIS, ))
        readResultOverASTM(self, items)


    @pyqtSignature('')
    def on_btnPWLExport_clicked(self):
        if getActual(self.modelSamplingPreparation.items(), (probeSent2LIS, ))[0]:
            if QtGui.QMessageBox.question(self, u'Внимание!', u'Экспортировать пробы ранее уже отправленные на экспорт?', QtGui.QMessageBox.Yes|QtGui.QMessageBox.No, QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes:
                checkStatus = (probeInWaiting, probeSent2LIS)
            else:
                checkStatus = (probeInWaiting, )
        else:
            checkStatus = (probeInWaiting, )
        items, idList = getActual(self.modelSamplingPreparation.items(), checkStatus)
        probeSaver = CProbeSaver({'status':probeSent2LIS},
                                 items,
                                 self.modelSamplingPreparation.setStatusItem)
        sendTests(self, idList, probeSaver=probeSaver)
#        self.modelSamplingPreparation.setStatus(probeSent2LIS)


    @pyqtSignature('')
    def on_btnRegistration_clicked(self):
        if self.modelSamplingPreparation.existsCheckedRows():
            if QtGui.QMessageBox.Ok == QtGui.QMessageBox.question(self,
                                                                  u'Внимание',
                                                                  u'Вы уверены что хотите зарегистрировать пробы?',
                                                                  QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel,
                                                                  QtGui.QMessageBox.Cancel):
                closeAction = QtGui.QMessageBox.question(self, u'Вопрос', u'Закрывать соответствующие действия?', QtGui.QMessageBox.Yes|QtGui.QMessageBox.No, QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes
                self.modelSamplingPreparation.registrateProbe(closeAction)


    @pyqtSignature('QAbstractButton*')
    def on_buttonBoxPWL_clicked(self, button):
        buttonCode = self.buttonBoxPWL.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Apply:
            self.updateFilter()
            self.setProbes(force=True)
        elif buttonCode == QtGui.QDialogButtonBox.Reset:
            self.resetFilter()
            self.setProbes()


#    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelSamplingOnlyProbes_currentRowChanged(self, currentIndex, previousIndex):
        if currentIndex.isValid():
            row = currentIndex.row()
            self.modelSamplingOnlyTests.setMainProbeId(self.modelSamplingOnlyProbes.getId(row))
            self.updateOnlyTestsCountLabel()


    def printWorkList(self, templateId):
        context = CInfoContext()
        data = {'testList': CWorkListInfo(context, self.modelSamplingPreparation._items, self.modelSamplingPreparation._originalProbeItems)}
        applyTemplate(self, templateId, data)


# ######################################################################################

class CTripodProbeLoaderDialog(CDialogBase):
    def __init__(self, parent, equipmentId):
        CDialogBase.__init__(self, parent)
        self._equipmentId = equipmentId
        #self._tripod = forceInt(QtGui.qApp.db.translate('rbEquipment', 'id', equipmentId, 'tripod'))
        tripod = QtGui.qApp.db.translate('rbEquipment', 'id', equipmentId, 'tripod')
        self._tripodItems = tripod.toString().split(';', QString.SkipEmptyParts) if tripod else []
        self._parent = parent
        self._probeData = CRBModelDataCache.getData('rbTest', addNone=False)
        self.setupUi()

        self.addModels('LoadingProbe', CLoadingProbeModel(self, equipmentId, self._tripodItems))
        self.setModels(self.tblLoadingProbe, self.modelLoadingProbe, self.selectionModelLoadingProbe)

        equipmentName = forceString(QtGui.qApp.db.translate('rbEquipment', 'id', equipmentId, 'name'))
        self.setWindowTitle(u'Загрузка проб в штатив оборудования \'%s\''%equipmentName)


    def getTestInfo(self, testId):
        code = unicode(self._probeData.getCodeById(testId))
        name = unicode(self._probeData.getNameById(testId))
        return u' | '.join([code, name])


    def getAbsProbeCount(self, probeId):
        return self._parent.getAbsProbeCount(probeId)


    def originalProbeTestsIdList(self, probeId):
        return self._parent.originalProbeTestsIdList(probeId)


    def getOriginalProbeItemsList(self, probeId):
        return self._parent.getOriginalProbeItemsList(probeId)


    def setCmbTripodNumberValues(self):
        #for value in xrange(self._tripod):
        #    self.cmbTripodNumber.addItem(unicode(value+1))
        for item in self._tripodItems:
            self.cmbTripodNumber.addItem(item)


    def setupUi(self):
        self.vLayout = QtGui.QVBoxLayout(self)
        self.lblTripodNumber = QtGui.QLabel(u'Номер штатива', self)
        self.cmbTripodNumber = QtGui.QComboBox(self)
        self.cmbTripodNumber.setEditable(True)
        self.edtTripodNumberLineEdit = QtGui.QLineEdit(self)
        #validator = QtGui.QIntValidator(1, 1000, self)
        #self.edtTripodNumberLineEdit.setValidator(validator)
        self.cmbTripodNumber.setLineEdit(self.edtTripodNumberLineEdit)
        self.setCmbTripodNumberValues()
        self.tblLoadingProbe = CInDocTableView(self)
        self.tblLoadingProbe.verticalHeader().show()
        self.tblLoadingProbe.addPopupSelectAllRow()
        self.tblLoadingProbe.addPopupClearSelectionRow()
        self._actShowProbeInfo = QtGui.QAction(u'Список тестов', self)
        self.tblLoadingProbe.popupMenu().addAction(self._actShowProbeInfo)
        self.connect(self._actShowProbeInfo, SIGNAL('triggered()'), self.on_actShowProbeInfo)

        self.btnLoadProbes   = QtGui.QPushButton(u'Загрузить', self)
        self.btnPickUpProbes = QtGui.QPushButton(u'Подобрать', self)
        self.btnExport       = QtGui.QPushButton(u'Экспорт', self)
        self.btnClose        = QtGui.QPushButton(u'Закрыть', self)

        self.hLayout = QtGui.QHBoxLayout()
        self.hLayout.addWidget(self.btnLoadProbes)
        self.hLayout.addWidget(self.btnPickUpProbes)
        self.hLayout.addWidget(self.btnExport)
        self.hLayout.addWidget(self.btnClose)

        self.vLayout.addWidget(self.lblTripodNumber)
        self.vLayout.addWidget(self.cmbTripodNumber)
        self.vLayout.addWidget(self.tblLoadingProbe)

        self.vLayout.addLayout(self.hLayout)

        self.connect(self.btnLoadProbes,   SIGNAL('clicked()'), self.loadProbes)
        self.connect(self.btnPickUpProbes, SIGNAL('clicked()'), self.pickUpProbes)
        self.connect(self.btnExport,       SIGNAL('clicked()'), self.export)
        self.connect(self.btnClose,        SIGNAL('clicked()'), self.close)
        self.connect(self.cmbTripodNumber, SIGNAL('currentIndexChanged(int)'),  self.tripodNumberChanged)
        self.connect(self.cmbTripodNumber, SIGNAL('editTextChanged(QString)'),  self.tripodNumberChanged)


    def on_actShowProbeInfo(self):
        index = self.tblLoadingProbe.currentIndex()
        if index.isValid():
            row = index.row()
            record = self.modelLoadingProbe._items[row]
            probeId = forceRef(record.value('id'))
            groupRecordList = self.getOriginalProbeItemsList(probeId)
            result = []
            for record in groupRecordList:
                testId = forceRef(record.value('workTest_id'))
                test = self.getTestInfo(testId)
                externalId = forceString(record.value('externalId'))
                result.append(u' | '.join([test, externalId]))

            QtGui.QMessageBox.information(self, u'Список тестов', u'\n'.join(result))


    def tripodNumberChanged(self, value):
        if isinstance(value, int):
            self.modelLoadingProbe.setTripodNumber(value)
        elif isinstance(value, basestring):
            value = '1' if not value else value
            self.modelLoadingProbe.setTripodNumber(int(value)-1)


    def setProbeIdList(self, probeIdList):
        self.modelLoadingProbe.setProbeIdList(probeIdList)
        self.modelLoadingProbe.setTripodNumber(0)


    def loadProbes(self):
        for record in self.modelLoadingProbe.recordList():
            if not record.isEmpty():
                self.saveProbeGroup(record)


    def saveProbeGroup(self, record, **kw):
        groupRecordList = self.getOriginalProbeItemsList(forceRef(record.value('id')))
        tmpRecord       = self.modelLoadingProbe.getTmpRecord()
        tripodNumber    = record.value('tripodNumber')
        placeInTripod   = record.value('placeInTripod')
        nullValue = QVariant()
        status = kw.get('status', None)
        for groupRecord in groupRecordList:
            placeInTripod = nullValue if forceInt(placeInTripod) == 0 else placeInTripod
            tripodNumber  = nullValue if forceString(tripodNumber) == '' else tripodNumber
            tmpRecord.setValue('id',            groupRecord.value('id'))
            tmpRecord.setValue('placeInTripod', placeInTripod)
            tmpRecord.setValue('tripodNumber',  tripodNumber)
            if status is not None:
                tmpRecord.setValue('status', QVariant(status))
            else:
                tmpRecord.setValue('status', groupRecord.value('status'))
            QtGui.qApp.db.updateRecord('Probe', tmpRecord)


    def export(self):
        rowList = set([index.row() for index in self.tblLoadingProbe.selectedIndexes()])
        idList = self.modelLoadingProbe.getProbeIdList(list(rowList))
        result = []
        for probeId in idList:
            result.extend(self.originalProbeTestsIdList(probeId))

        recordList = [self.modelLoadingProbe.getRecordById(probeId) for probeId in idList]
        probeSaver = CProbeSaver({'status':probeSent2LIS},
                                 recordList,
                                 self.saveProbeGroup)
        sendTests(self, idList, probeSaver=probeSaver)
#        for probeId in idList:
#            record = self.modelLoadingProbe.getRecordById(probeId)
#            self.saveProbeGroup(record, status=probeSent2LIS)

    def pickUpProbes(self):
        currentTripodNumber = self.cmbTripodNumber.currentIndex()
        self.modelLoadingProbe.setTripodNumber(0)
        self.modelLoadingProbe.pickUpProbes()
        self.modelLoadingProbe.setTripodNumber(currentTripodNumber)



class CLoadingProbeModel(CRecordListModel):

    class CLocInDocProbeCol(CInDocTableCol):
        invalidValue = QVariant()
        def __init__(self, model):
            CInDocTableCol.__init__(self, u'Проба', 'id', 10)
            self._cache = {}
            self._model = model
            self._currValue = None
            self._mapTakenTissueJournalId2date = {}

        def getDatetimeTaken(self, takenTissueJournalId):
            result = self._mapTakenTissueJournalId2date.get(takenTissueJournalId, None)
            if result is None:
                result = forceDate(QtGui.qApp.db.translate('TakenTissueJournal', 'id', takenTissueJournalId, 'datetimeTaken'))
                self._mapTakenTissueJournalId2date[takenTissueJournalId] = result
            return result


        def getTestInfo(self, testId):
            return self._model.getTestInfo(testId)


        def toString(self, val, record):
            if not record or record.isEmpty():
                return CLoadingProbeModel.CLocInDocProbeCol.invalidValue
            id = forceRef(val)
            result = self._cache.get(id, None)
            if result is None:
                testId = forceRef(record.value('workTest_id'))
                test = '['+self.getTestInfo(testId)+']'
                datetimeTaken = forceString(self.getDatetimeTaken(forceRef(record.value('takenTissueJournal_id'))))
                externalId = forceString(record.value('externalId'))
                result = QVariant(' | '.join([unicode(self.getAbsProbeCount(id)), externalId, datetimeTaken, test]))
                self._cache[id] = result
            return result

        def getAbsProbeCount(self, probeId):
            return self._model.getAbsProbeCount(probeId)

        def createEditor(self, parent):
            editor = CProbeComboBox(parent, self)
            editor.setIdList(self._model.actualProbeIdList())
            return editor


        def setEditorData(self, editor, value, record):
            id = forceRef(value)
            if id:
                editor._addItem(id)
            self._currValue = id
            editor.setCurrentIndex(editor.findData(value))


        def getEditorData(self, editor):
            vId = editor.itemData(editor.currentIndex())
            id = forceRef(vId)
            if id != self._currValue:
                self._model.removeExistsProbeId(self._currValue)
                self._model.addExistsProbeId(id)
            self._currValue = None
            return vId


    def __init__(self, parent, equipmentId, tripodItems):
        CRecordListModel.__init__(self, parent)
        self.addCol(CLoadingProbeModel.CLocInDocProbeCol(self))
        self.addHiddenCol('exportName')
        self.addHiddenCol('exportDatetime')
        self.addHiddenCol('exportPerson_id')

        self._parent = parent
        self._equipmentId = equipmentId
        self._tripodCapacity = forceInt(QtGui.qApp.db.translate('rbEquipment', 'id', equipmentId, 'tripodCapacity'))
        self._tripodItems = tripodItems
        self._tripodCount = len(tripodItems)
        self._tripodNumber = 0

        self._probeIdList = []
        self._existsProbeIdList = []
        self._mapProbeId2Record = {None: QtSql.QSqlRecord()}
        self._mapCurrentProbeId2Record = {None: QtSql.QSqlRecord()}
        self._mapTripodNumberToItems = {}

        self.buildItemsCache()


    def getProbeIdList(self, rowList=[]):
        result = []
        items = self._mapTripodNumberToItems[self._tripodNumber]
        if not rowList:
            rowList = range(len(items))
        for row in rowList:
            item = items[row]
            if not item.isEmpty():
                result.append(forceRef(item.value('id')))
        return result


    def getTestInfo(self, testId):
        return self._parent.getTestInfo(testId)


    def recordList(self):
        return self._mapProbeId2Record.values()


    def getAbsProbeCount(self, probeId):
#        if probeId in self._probeIdList:
        return self._parent.getAbsProbeCount(probeId)
#        return u'---'


    def originalProbeTestsIdList(self, probeId):
        return self._parent.originalProbeTestsIdList(probeId)


    def pickUpProbes(self, emitChanged=True):
        startRow    = 0
        rowCount    = self.rowCount()
        fullRowList = range(rowCount)
        for idx, (probeId, record) in enumerate(self._mapCurrentProbeId2Record.items()):
            if probeId and probeId not in self._existsProbeIdList:
                actualRowList = fullRowList[startRow:]
                for row in actualRowList:
                    if self._items[row].isEmpty():
                        record.setValue('placeInTripod', QVariant(row+1))
                        record.setValue('tripodNumber',  QVariant(self._tripodItems[self._tripodNumber]))
                        self._items[row] = record
                        self._mapTripodNumberToItems[self._tripodNumber][row] = record
                        self._existsProbeIdList.append(probeId)
                        startRow = row+1
                        break
                if startRow == rowCount:
                    if self._tripodNumber < self._tripodCount-1:
                        self.setTripodNumber(self._tripodNumber+1)
                        self.pickUpProbes(emitChanged=False)
                    break
        if emitChanged:
            self.emitAllChanged()


    def removeExistsProbeId(self, id):
        if id and id in self._mapProbeId2Record.keys():
            record = self._mapProbeId2Record[id]
            record.setValue('placeInTripod', QVariant())
            record.setValue('tripodNumber',  QVariant())
            if id in self._existsProbeIdList:
                self._existsProbeIdList.remove(id)


    def addExistsProbeId(self, id):
        if id and id not in self._existsProbeIdList:
            self._existsProbeIdList.append(id)


    def actualProbeIdList(self):
        return list(set(self._probeIdList)-set(self._existsProbeIdList))


    def rowCount(self, index=None):
        return self._tripodCapacity


    def columnCount(self, index=None):
        return 1


    def getTmpRecord(self):
        db = QtGui.qApp.db
        fields = ['id', 'placeInTripod', 'tripodNumber', 'status']
        table = db.table('Probe')
        return table.newRecord(fields)


    def buildItemsCache(self):
        emptyValue = QtSql.QSqlRecord()
        rowCount   = self.rowCount()
        for tripodNumber in xrange(self._tripodCount):
            self._mapTripodNumberToItems[tripodNumber] = [emptyValue]*rowCount


    def getRecordById(self, probeId):
        return self._mapProbeId2Record.get(probeId, None)


    def _checkFilled(self):
        db = QtGui.qApp.db
        table = db.table('Probe')
        #tripodNumberList = range(self._tripodCount)
        tripodNumberList = self._tripodItems
        placeInTripodList = range(self._tripodCapacity)
        probeIdList = []
        for probeId in self._probeIdList:
            probeIdList.extend(self.originalProbeTestsIdList(probeId))
        cond = [table['status'].notInlist([CSamplePreparationModel.probeIsFinished,
                                           CSamplePreparationModel.probeWithoutResult]
                                         ),
                table['id'].notInlist(probeIdList),
                table['equipment_id'].eq(self._equipmentId),
                table['tripodNumber'].inlist(tripodNumberList),
                table['placeInTripod'].inlist(placeInTripodList)
               ]
        fields = 'id, externalId, workTest_id, placeInTripod, tripodNumber, takenTissueJournal_id, status'
        recordList = db.getRecordList(table, fields, cond)
        for record in recordList:
            placeInTripod = forceInt(record.value('placeInTripod')) - 1
            tripodNumber  = forceString(record.value('tripodNumber'))
            notOverTop = placeInTripod <= self.rowCount()# and tripodNumber <= self._tripodCount
            notUnderBottom = placeInTripod >= 0# and tripodNumber >= 0
            if notOverTop and notUnderBottom and tripodNumber in self._tripodItems:
                tripodIndex = self._tripodItems.indexOf(tripodNumber)
                if self._mapTripodNumberToItems[tripodIndex][placeInTripod].isEmpty():
                    self._mapTripodNumberToItems[tripodIndex][placeInTripod] = record
                    probeId = forceRef(record.value('id'))
                    self._mapProbeId2Record[probeId] = record


    def setTripodNumber(self, tripodNumber):
        self._tripodNumber = tripodNumber
        self._items = self._mapTripodNumberToItems[tripodNumber]
        self.emitAllChanged()


    def setProbeIdList(self, probeIdList):
        db = QtGui.qApp.db
        self._probeIdList = probeIdList
        self._checkFilled()
        fields = 'id, externalId, workTest_id, placeInTripod, tripodNumber, takenTissueJournal_id, status'
        table = db.table('Probe')
        recordList = db.getRecordList(table, fields, table['id'].inlist(probeIdList))
        for record in recordList:
            probeId = forceRef(record.value('id'))
            self._mapProbeId2Record[probeId] = record
            self._mapCurrentProbeId2Record[probeId] = record
            placeInTripod = record.value('placeInTripod')
            tripodNumber  = record.value('tripodNumber')
            if not (placeInTripod.isNull() or tripodNumber.isNull()):
                placeInTripod = forceInt(placeInTripod) - 1
                tripodNumber  = forceString(tripodNumber)
                notOverTop = placeInTripod <= self.rowCount()# and tripodNumber <= self._tripodCount
                notUnderBottom = placeInTripod >= 0# and tripodNumber >= 0
                if notOverTop and notUnderBottom and tripodNumber in self._tripodItems:
                    tripodIndex = self._tripodItems.indexOf(tripodNumber)
                    if self._mapTripodNumberToItems[tripodIndex][placeInTripod].isEmpty():
                        self._mapTripodNumberToItems[tripodIndex][placeInTripod] = record
                        self._existsProbeIdList.append(probeId)
        self.reset()


    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            column = index.column()
            if column == self.getColIndex('id'):
                id  = forceRef(value)
                row = index.row()
                record = self._mapProbeId2Record[id]
                if id:
                    record.setValue('placeInTripod', QVariant(row+1))
                    record.setValue('tripodNumber',  QVariant(self._tripodItems[self._tripodNumber]))
                self._items[row] = record
                self._mapTripodNumberToItems[self._tripodNumber][row] = record
                self.emitCellChanged(row, column)
                return True
        CRecordListModel.setData(self, index, value, role)


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Vertical:
            if role == Qt.DisplayRole:
                return QVariant(section+1)
        return CRecordListModel.headerData(self, section, orientation, role)


# ########################################################


class CProbeComboBox(QtGui.QComboBox):
    def __init__(self, parent, column):
        QtGui.QComboBox.__init__(self, parent)
        self._column = column


    def columnCache(self):
        return self._column._cache


    def getDatetimeTaken(self, takenTissueJournalId):
        self._column.getDatetimeTaken(takenTissueJournalId)


    def setIdList(self, idList):
        self.addItem(forceString(u'Не задано'), QVariant())
        for id in idList:
            self._addItem(id)


    def _addItem(self, id):
        result = self.columnCache().get(id, None)
        if result is None:
            probeRecord = QtGui.qApp.db.getRecord('Probe', 'workTest_id, externalId, takenTissueJournal_id', id)
            if probeRecord:
                testId = forceRef(probeRecord.value('workTest_id'))
                test = '['+self._column.getTestInfo(testId)+']'
                datetimeTaken = forceString(self.getDatetimeTaken(forceRef(probeRecord.value('takenTissueJournal_id'))))
                externalId = forceString(probeRecord.value('externalId'))
                result = QVariant(' | '.join([unicode(self.getAbsProbeCount(id)), externalId, datetimeTaken, test]))
            else:
                result = QVariant()
            self.columnCache()[id] = result
        self.addItem(forceString(result), QVariant(id))


    def getAbsProbeCount(self, probeId):
        return self._column.getAbsProbeCount(probeId)



# #######################################################


class CProbeSaver(object):
    def __init__(self, values, records, saveFunc):
        self._probeIdList = []
        self._mapProbeId2Record = {}
        self._values = values
        self.parseRecords(records)
        self._saveFunc = saveFunc


    def clear(self):
        self._probeIdList = []


    def append(self, probeId):
        self._probeIdList.append(probeId)


    def parseRecords(self, records):
        for record in records:
            self._mapProbeId2Record[forceRef(record.value('id'))] = record


    def save(self, fileName=''):
        for probeId in self._probeIdList:
            record = self._mapProbeId2Record.get(probeId, None)
            if record:
                record.setValue('exportName', QVariant(fileName))
                record.setValue('exportDatetime', QVariant(QDateTime.currentDateTime()))
                record.setValue('exportPerson_id', QVariant(QtGui.qApp.userId))
                self._saveFunc(record, **self._values)


# ############################################################


def getActual(items, status):
    resultItems = []
    resultIdList = []
    for item in items:
        if forceInt(item.value('status')) in status and forceRef(item.value('equipment_id')):
            resultIdList.append(forceRef(item.value('id')))
            resultItems.append(item)
    return resultItems, resultIdList
