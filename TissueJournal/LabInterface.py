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

from collections import namedtuple
#from os          import path

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, SIGNAL, QObject, QString

from RefBooks.Equipment.Protocol             import CEquipmentProtocol
from Registry.Utils                          import getClientInfo
from Exchange.Lab.AstmE1394.Message          import CMessage
from Exchange.Lab.AstmE1381.FileExchangeLoop import CFileExchangeLoop

from library.SimpleProgressDialog            import CSimpleProgressDialog
from library.DialogBase                      import CDialogBase
from library.Utils                           import forceRef, forceString, formatName

from TissueJournal.LabInterfaceASTM          import sendOrdersOverASTM

try:
    from TissueJournal.LabInterfaceFHIR    import sendOrdersOverFHIR as sendOrdersOverFHIR050
    from TissueJournal.LabInterfaceFHIR102 import sendOrdersOverFHIR as sendOrdersOverFHIR102
    FHIRisOk = True
except:
    FHIRisOk = False

from LabResultEquipmentTable import CLabResultEquipmentModel
from Utils                   import getEquipmentInterface

from Ui_LabResultReaderDialog import Ui_LabResultReader


CBundleKey = namedtuple('CBundleKey',
                        ('takenTissueJournalId',
                         'equipmentId',
                         'clientId'
                        )
                       )


class CProcessHelper(object):
    def __init__(self, bundles):
        self.bundles = bundles
        self.mapEquipmentIdToInterface = {}
        self.mapClientIdToInfo = {}
        self.probeSaver = None


    def setProbeSaver(self, probeSaver):
        self.probeSaver = probeSaver


    def getEquipmentInterface(self, equipmentId):
        result = self.mapEquipmentIdToInterface.get(equipmentId)
        if result is None:
            result = getEquipmentInterface(equipmentId)
            self.mapEquipmentIdToInterface[equipmentId] = result
        return result


    def getClientInfo(self, clientId):
        result = self.mapClientIdToInfo.get(clientId)
        if result is None:
            self.mapClientIdToInfo[clientId] = result = getClientInfo(clientId)
        return result


    def stepIterator(self, progressDialog):
        for bundleKey, probeIdList in self.bundles.iteritems():
            equipmentId = bundleKey.equipmentId
            equipmentInterface = self.getEquipmentInterface(equipmentId)
            if equipmentInterface.protocol == CEquipmentProtocol.astm:
                sendOrdersOverASTM(progressDialog,
                                   equipmentInterface,
                                   self.getClientInfo(bundleKey.clientId),
                                   probeIdList,
                                   self.probeSaver)
            elif equipmentInterface.protocol == CEquipmentProtocol.fhir050:
                if FHIRisOk:
                    sendOrdersOverFHIR050(progressDialog,
                                          equipmentInterface,
                                          self.getClientInfo(bundleKey.clientId),
                                          probeIdList,
                                          self.probeSaver)
                else:
                    raise Exception('FHIR support is disabled')
            elif equipmentInterface.protocol == CEquipmentProtocol.fhir102:
                if FHIRisOk:
                    sendOrdersOverFHIR102(progressDialog,
                                          equipmentInterface,
                                          self.getClientInfo(bundleKey.clientId),
                                          probeIdList,
                                         self.probeSaver)
                else:
                    raise Exception('FHIR support is disabled')
            yield len(probeIdList)




def sendTests(widget, probeIdList, probeSaver=None):
    pd = CSimpleProgressDialog(widget)
    pd.setWindowTitle(u'Экспорт заданий')
    try:
        bundles = bundleProbes(probeIdList)
        helper = CProcessHelper(bundles)
        helper.setProbeSaver(probeSaver)
        count = sum(len(bundle) for bundle in bundles.itervalues())
        pd.setStepCount(count)
        pd.setAutoStart(True)
        pd.setAutoClose(False)
        pd.setStepIterator(helper.stepIterator)
        pd.exec_()
    finally:
        pass


def bundleProbes(probeIdList):
    # возвращает словарь (takenTissueJournal_id, equipment_id, client_id) -> список probeId
    result = {}
    db = QtGui.qApp.db
    tableProbe = db.table('Probe')
    tableTissue = db.table('TakenTissueJournal')
    table = tableProbe.innerJoin(tableTissue, tableTissue['id'].eq(tableProbe['takenTissueJournal_id']))
    stmt = db.selectStmt(table,
                         [tableProbe['equipment_id'],
                          tableProbe['takenTissueJournal_id'],
                          tableProbe['id'],
                          tableTissue['client_id'],
                         ],
                         tableProbe['id'].inlist(probeIdList),
                         [tableProbe['equipment_id'].name(),
                          tableProbe['takenTissueJournal_id'].name(),
                          tableProbe['id'].name(),
                         ]
                        )
    query = db.query(stmt)
    while query.next():
        record = query.record()
        equipmentId = forceRef(record.value('equipment_id'))
        takenTissueJournalId = forceRef(record.value('takenTissueJournal_id'))
        clientId = forceRef(record.value('client_id'))
        probeId = forceRef(record.value('id'))
        key = CBundleKey(takenTissueJournalId, equipmentId, clientId)
        result.setdefault(key, []).append(probeId)
    return result


# ##################################################################################

class CLabResultReaderDialog(CDialogBase, Ui_LabResultReader):
    importResultFullResultField = 0 # Все поля результат заняты, некуда импортировать.
    importResultCannotFindProbe = 1 # Не удалось идентифицировать пробу
    importResultOk = 2
    importResultValueIsEmpty = 3
    importResultCannotFindTest = 4

    def __init__(self, parent=None):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)

        self._parent = parent

        self._probeItems = []
        self._messageList = []
        self._fileLoop = None

        self.modelItems = CLabResultEquipmentModel(self)
        self.tblItems.setModel(self.modelItems)
        self._isStarted = False

        #buttons
        self.btnStartStop = QtGui.QPushButton(u'Загрузка данных', self)
        self.buttonBox.addButton(self.btnStartStop, QtGui.QDialogButtonBox.ActionRole)
        self.connect(self.btnStartStop, SIGNAL('clicked()'), self.on_btnStartStop)

        self.btnImport = QtGui.QPushButton(u'Импорт', self)
        self.buttonBox.addButton(self.btnImport, QtGui.QDialogButtonBox.ActionRole)
        self.connect(self.btnImport, SIGNAL('clicked()'), self.on_btnImport)
        self.btnImport.setEnabled(False)

        self.chkRewrite.setEnabled(False)
        self.chkOnlyFromModel.setEnabled(False)

        self.setWindowTitle(u'Импорт')

        self.progressBar.setVisible(False)


    def on_btnStartStop(self):
        if self._isStarted:
            self.btnStartStop.setText(u'Загрузка данных')
            self.stop()
            self.btnImport.setEnabled(True)
            self.chkOnlyFromModel.setEnabled(True)
            self.chkRewrite.setEnabled(True)
            self._isStarted = False
        else:
            self.btnStartStop.setText(u'Стоп')
            self._isStarted = True
            self.btnImport.setEnabled(False)
            self.chkRewrite.setEnabled(False)
            self.chkOnlyFromModel.setEnabled(False)
            self.start()


    def setProbeItems(self, probeItems):
        self._probeItems = probeItems
        self.load()


    def load(self):
        self.modelItems.setIdList(QtGui.qApp.db.getIdList('rbEquipment'), self._parent._filter.get('equipmentId', None))


    def start(self):
        QtGui.qApp.setOverrideCursor(QtGui.QCursor(Qt.BusyCursor))

        self.logWidget.clear()
        self._messageList = []
        self._fileLoop = None

        checkedEquipmentIdList = self.modelItems.checkedEquipmentIdList()

        if checkedEquipmentIdList:
            import json

            equipmentId = checkedEquipmentIdList[0]
            equipmentInterface = getEquipmentInterface(equipmentId)
            opts = json.loads(equipmentInterface.address)

            self._fileLoop = CLocFileExchangeLoop(opts)
            self._fileLoop._externalInfo = {'equipmentId':equipmentId}
            self._fileLoop.setConnector(self.onMessageAccepted)
            self._fileLoop.start()
            for equipmentId in checkedEquipmentIdList[1:]:
                equipmentInterface = getEquipmentInterface(equipmentId)
                opts = json.loads(equipmentInterface.address)
                self._fileLoop.appendOpts(opts, {'equipmentId':equipmentId})

        else:
            self.on_btnStartStop()
            QtGui.QMessageBox.information(self, u'Внимание!',
                                          u'Оборудование не выбрано!',
                                          QtGui.QMessageBox.Ok,
                                          QtGui.QMessageBox.Ok)


    def stop(self):
        if self._isStarted:
            if self._fileLoop:
                self._fileLoop.stop()
            QtGui.qApp.restoreOverrideCursor()


    def onMessageAccepted(self, message):
        if not self._isStarted:
            return

        self.logWidget.append(message)


    def logPatients(self, m):
        for p in m.patients:
            pName = formatName(p.lastName, p.firstName, p.patrName)
            self.logWidget.append(pName+u': id '+p.patientId)
            for o in p.orders:
                self.logWidget.append(u'ИБМ: '+o.specimenId)
                for r in o.results:
                    self.logWidget.append(_concatenateResultValues(r))


    def logOnImport(self, m, resultList):
        def _list2Tuple(val):
            if isinstance(val, list):
                result = tuple()
                for v in val:
                    result += (_list2Tuple(v), )
                return result
            else:
                return val

        mapResult2Text = {self.importResultFullResultField:u'! ОШИБКА: Все поля результат заняты, некуда импортировать',
                         self.importResultCannotFindProbe:u'! ОШИБКА: Не удалось идентифицировать пробу',
                         self.importResultOk:u'Импорт прошел успешно!',
                         self.importResultValueIsEmpty:u'Импортируемое значение не задано',
                         self.importResultCannotFindTest: u'ОШИБКА: Тест не найден'}

        for p in m.patients:
            pName = formatName(p.lastName, p.firstName, p.patrName)
            for o in p.orders:
                for r in o.results:
                    key = _list2Tuple([p.patientId, o.specimenId, r.testId, r.assayCode, r.assayName, r.value, r.referenceRange, r.unit])
                    if key in resultList:
                        resultKey = resultList[key]
                        self.logWidget.append(pName+u': id '+(p.patientId if p.patientId else p.reservedPatientId))
                        self.logWidget.append(u'ИБМ: '+o.specimenId)
                        self.logWidget.append(_concatenateResultValues(r))
                        self.logWidget.append(mapResult2Text[resultKey])
                        self.logWidget.append('\n\n')


    def logException(self):
        self.logWidget.append(u'! Произошла критическая ошибка. Импорт прекращен.')


    def accept(self):
        if self.on_accept():
            CDialogBase.accept(self)


    def reject(self):
        if self._isStarted:
            self.on_btnStartStop()
        CDialogBase.reject(self)


    def on_btnImport(self):
        self.logWidget.clear()
        if self._fileLoop:
            self._messageList = list(self._fileLoop.messageList())
        self.applyMessageList()


    def messageList(self):
        return self._messageList


    def applyMessageList(self):
        if self._messageList:
            self.progressBar.setVisible(True)
            self.progressBar.reset()

            self._parent.applyEquipmentMessage(self)

            self.progressBar.setVisible(False)


    def on_accept(self):
        if self._fileLoop:
            if self._isStarted:
                self.on_btnStartStop()

            return QtGui.QMessageBox.question(self, u'',
                                              u'Закрыть диалог?',
                                              QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel,
                                              QtGui.QMessageBox.Cancel) == QtGui.QMessageBox.Ok
        return True

# #######################################################
# Следующий механизм придуман всвязи с тем что Qt ругается
# во время логирования загружаемых данных из файла
# 'make sure QTextCursor is registered using qRegisterMetaType()'.
# Это происходит из-за того что CFileExchangeLoop для считывания данных
# создает новый поток используя threading.Thread a QTextCursor
# находится в основном потоке.

class CConnector(QObject):
    def __init__(self, slot):
        QObject.__init__(self)
        self.setConnect(slot)

    def setConnect(self, slot):
        self._slot = slot
        self.connect(self, SIGNAL('connectorSignal(QString)'), self._slot, Qt.QueuedConnection)

    def removeConnect(self):
        self.disconnect(self, SIGNAL('connectorSignal(QString)'), self._slot)

    def execEmit(self, message):
        self.emit(SIGNAL('connectorSignal(QString)'), QString(message))


class CLocFileExchangeLoop(CFileExchangeLoop):
    def __init__(self, opts):
        CFileExchangeLoop.__init__(self, opts)
        self.connector = None
        self._messageList = []
        self.onMessageAccepted = self.__onMessageAccepted
        self._allLoaded = False
        self._logLevel = 1
        self.onLog = self.__onLog
        self.setName('exchange thread')


    def start(self):
        self._messageList = []
        CFileExchangeLoop.start(self)


    def setConnector(self, slot):
        if self.connector:
            self.connector.removeConnect()
            self.connector = None
        if slot:
            self.connector = CConnector(slot)


    def stop(self, timeout=None):
        self.setConnector(None)
        CFileExchangeLoop.stop(self, timeout)


    def __onLog(self, logText):
        self.connector.execEmit(logText)


    def __onMessageAccepted(self, message):
        def _getClientByTripodNumber(tripodNumber, placeInTripod):
            result = {}
            db = QtGui.qApp.db
            tableClient = db.table('Client')
            tableProbe = db.table('Probe')
            tableAction = db.table('Action')
            tableEvent = db.table('Event')
            table = tableProbe.leftJoin(tableAction, tableAction['takenTissueJournal_id'].eq(tableProbe['takenTissueJournal_id']))
            table = table.leftJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))
            table = table.leftJoin(tableClient, tableClient['id'].eq(tableEvent['client_id']))
            cols = [
                tableProbe['id'].alias('probeId'),
                tableProbe['externalId'].alias('externalId'),
                tableClient['id'].alias('clientId'),
                tableClient['lastName'].alias('clientLastName'),
                tableClient['firstName'].alias('clientFirstName'),
                tableClient['patrName'].alias('clientPatrName')]
            cond = [tableProbe['tripodNumber'].eq(tripodNumber),
                tableProbe['placeInTripod'].eq(placeInTripod),
                tableProbe['status'].inlist([1, 2, 6])]
            recordList = db.getRecordList(table, cols, cond)
            if len(recordList) == 1:
                record = recordList[0]
            elif len(recordList) > 1:
                self.connector.execEmit(u'Обнаружено несколько ожидающих проб на позиции %i %i, берем первую'%(tripodNumber, placeInTripod))
                record = recordList[0]
            elif len(recordList) == 0:
                self.connector.execEmit(u'Ожидающих проб на позиции %i %i не обнаружено'%(tripodNumber, placeInTripod))
                record = None
            if record:
                clientId = forceRef(recordList[0].value('clientId'))
                probeId = forceRef(recordList[0].value('probeId'))
                externalId = forceString(recordList[0].value('externalId'))
                clientLastName = forceString(recordList[0].value('clientLastName'))
                clientFirstName = forceString(recordList[0].value('clientFirstName'))
                clientPatrName = forceString(recordList[0].value('clientPatrName'))
                result['clientId'] = clientId
                result['probeId'] = probeId
                result['externalId'] = externalId
                result['clientLastName'] = clientLastName
                result['clientFirstName'] = clientFirstName
                result['clientPatrName'] = clientPatrName
            return result
        m = CMessage()
        m.setRecords(message.body, encoding=message.encoding)
        
        try:
            for p in m.patients:
                if not p.patientId and not p.laboratoryPatientId and not p.reservedPatientId:
                    for o in p.orders:
                        try:
                            tripodNumber = int(o.specimenIndex)
                            placeInTripod = int(o.specimenCount)
                        except:
                            try:
                                tripodNumber = int(o.instrumentSpecimenId)
                                placeInTripod = int(o.instrumentSpecimenIndex)
                            except:
                                continue
                        data = _getClientByTripodNumber(tripodNumber, placeInTripod)
                        if data.keys():
                            p.patientId = data.get('clientId', None)
                            p.lastName = data.get('clientLastName', None)
                            p.firstName = data.get('clientFirstName', None)
                            p.patrName = data.get('clientPatrName', None)
                            o.specimenId = data.get('externalId', None)
        except:
            pass

        try:
            for p in m.patients:
                if not p.patientId and not p.laboratoryPatientId and not p.reservedPatientId:
                    for o in p.orders:
                        try:
                            tripodNumber = int(o.specimenIndex)
                            placeInTripod = int(o.specimenCount)
                        except:
                            try:
                                tripodNumber = int(o.instrumentSpecimenId)
                                placeInTripod = int(o.instrumentSpecimenIndex)
                            except:
                                continue
                        data = _getClientByTripodNumber(tripodNumber, placeInTripod)
                        if data.keys():
                            p.patientId = data.get('clientId', None)
                            p.lastName = data.get('clientLastName', None)
                            p.firstName = data.get('clientFirstName', None)
                            p.patrName = data.get('clientPatrName', None)
                            o.specimenId = data.get('externalId', None)
        except:
            pass

        self._messageList.append((m, message, message.source._externalInfo['equipmentId']))

        logText = u'\n'.join([u'Сообщение от: '+(m.header.senderName or u'анонимного устройства'),
                              self._getPatientsLog(m), '\n\n'])
        self.connector.execEmit(logText)
#?        message.dismiss()


    def _getPatientsLog(self, m):
        result = []
        for p in m.patients:
            pName = formatName(p.lastName, p.firstName, p.patrName)
            pId = p.patientId or p.reservedPatientId or p.laboratoryPatientId
            if type(pId) == list:
                pId = pId[0][0]
            result.append(pName+u': id '+pId)
            for o in p.orders:
                result.append(u'ИБМ: '+o.specimenId)
                for r in o.results:
                    result.append(_concatenateResultValues(r))
        return u'\n'.join(result)


    def messageList(self):
        return self._messageList


    def _cannotChangeOpts(self):
        if not self._allLoaded:
            self.connector.execEmit(u'Загрузка данных закончена.')
            self._allLoaded = True


def _concatenateResultValues(r):
    return u' '.join([u'Тест', forceString(r.assayCode), u'|', forceString(r.assayName), u':', forceString(r.value), forceString(r.unit)])


def readResultOverASTM(widget, probeItems):
    dlg = CLabResultReaderDialog(widget)
    dlg.setProbeItems(probeItems)
    dlg.exec_()
    dlg.stop()
