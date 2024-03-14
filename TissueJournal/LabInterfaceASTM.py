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

import json
import os.path

from collections import namedtuple

from PyQt4 import QtGui
from PyQt4.QtCore import QDateTime

from Events.Utils  import getEventDiagnosis

from Exchange.Lab.AstmE1394.Message          import CMessage
from Exchange.Lab.AstmE1381.AbstractLoop     import CBaseMessage
#from Exchange.Lab.AstmE1381.FileExchangeLoop import CFileExchangeLoop

from Exchange.Lab.AstmE1381.FileInterface import CFileInterface

from Orgs.Utils import getPersonInfo

from library.crbcombobox import CRBModelDataCache
from library.Utils       import calcAgeInYears, forceBool, forceDateTime, forceInt, forceRef, forceString, smartDict
from library.Identification import getIdentification


__all__ = ( 'sendOrdersOverASTM',
          )


class SPECIMEN_IDENTIFIER_MODE:
    sampleIdMode=0
    positionMode=1


# обнаружено, что разные протоколы могут предусматривать разные
# способы группировки проб по заданиям.
# поэтому мы должны самостоятельно группировать пробы в задания

def sendOrdersOverASTM(widget, equipmentInterface, clientInfo, probeIdList, probeSaver=None):
    def boolOpt(value):
        return value in (1, '1')

    opts = json.loads(equipmentInterface.address)
    opts['encoding'] = opts.get('exportEncoding', opts.get('encoding', 'utf-8'))
    opts['processingId'] = opts.get('processingId', 'P')
    opts['extendedValues'] = boolOpt(opts.get('extendedValues', 0))
    opts['appendIbmIntoFileName'] = boolOpt(opts.get('appendIbmIntoFileName', 0))
    opts['uniTestId'] = boolOpt(opts.get('uniTestId', 1))
    opts['uniTestName'] = boolOpt(opts.get('uniTestName', 1))
    opts['testCode'] = boolOpt(opts.get('testCode', 1))
    equipmentInterface.opts = smartDict(**opts)

    orderList = selectASTMOrders(equipmentInterface, clientInfo, probeIdList)
    for order in orderList:
        if equipmentInterface.eachTestDetached:
            for test in order.tests:
                if probeSaver:
                    probeSaver.clear()
                identifier = sendOrderOverASTM(equipmentInterface, order, [test])
                if probeSaver:
                    probeSaver.append(test.probeId)
                    probeSaver.save(identifier)
        else:
            if probeSaver:
                probeSaver.clear()
            identifier = sendOrderOverASTM(equipmentInterface, order, order.tests)
            if probeSaver:
                for test in order.tests:
                    probeSaver.append(test.probeId)
                probeSaver.save(identifier)
    return bool(orderList)


CASTMTestOrder = namedtuple('CASTMTestOrder',
                                (  'probeId',
                                   'isUrgent',
                                   'testId',
                                   'testCode',
                                   'testName',
                                   'specimenCode',
                                   'specimenName',
                                   'tripodNumber',
                                   'placeInTripod',
                                   'exportName'
                                )
                           )

class CASTMOrder:
    u'Заказ исследования по пртоколу ASTM'
    def __init__(self, clientInfo, dateTime, label, takenTissueJournalId):
        self.clientInfo = clientInfo
        self.dateTime = dateTime
        self.label = label
        self.takenTissueJournalId = takenTissueJournalId

        self.orgStructureCode = ''
        self.orgStructureExternalCode = ''
        self.orgStructureName = ''
        self.orgStructureType = ''
        self.setPersonCode = ''
        self.setPersonName = ''
        self.MKB = ''

        self.eventTypeRegionalCode = ''
        self.eventTypeName = ''
        self.eventMesCode = ''
        self.financeCode = ''
        self.eventExternalId = ''
        self.actionFinanceCode = ''
        self.contractNumber = ''

        self.tests = []


    def fillExtendedValues(self):
        orgStructureCode = orgStructureExternalCode = orgStructureName = orgStructureType = setPersonCode = setPersonName = MKB = ''
        orgStructureId = None
        db = QtGui.qApp.db

        masterTakenTissueJournalId = forceRef(
            db.translate('TakenTissueJournal', 'id', self.takenTissueJournalId, 'parent_id')
        ) or self.takenTissueJournalId

        tableAction = db.table('Action')
        actionRecord = db.getRecordEx(tableAction,
                                      '*',
                                      [ tableAction['takenTissueJournal_id'].eq(masterTakenTissueJournalId),
                                        tableAction['deleted'].eq(0)
                                      ],
                                      'directionDate DESC'
                                     )
        if actionRecord:
            actionId = forceRef(actionRecord.value('id'))
            eventId  = forceRef(actionRecord.value('event_id'))
            MKB      = forceString(actionRecord.value('MKB'))
            if not MKB:
                MKB = getEventDiagnosis(eventId)
            directionDate = forceDateTime(actionRecord.value('directionDate'))
            setPersonId   = forceRef(actionRecord.value('setPerson_id'))
            personInfo    = getPersonInfo(setPersonId)
            tableActionMoving = db.table('vActionMoving')
            relegateOrgId = forceRef(db.translate('Event', 'id', eventId, 'relegateOrg_id'))
            moveActionRecord = db.getRecordEx(tableActionMoving,
                                              tableActionMoving['propOrgStructure_id'].name(),
                                              [ tableActionMoving['event_id'].eq(eventId),
                                                tableActionMoving['begDate'].le(directionDate),
                                              ],
                                              'begDate DESC'
                                             )
            if relegateOrgId and QtGui.qApp.preferences.appPrefs.get('astm_exportRelegateOrg', False):
                orgRecord = db.getRecord('Organisation', 'id, shortName, infisCode, head_id', relegateOrgId)
                if orgRecord and forceRef(orgRecord.value('head_id')):
                    orgRecord = db.getRecord('Organisation', 'id, shortName, infisCode', forceRef(orgRecord.value('head_id')))
                if orgRecord:
                    orgStructureName = forceString(orgRecord.value('shortName'))
                    orgStructureExternalCode = forceString(orgRecord.value('infisCode'))
            else:
                if moveActionRecord:
                    orgStructureId = forceRef(moveActionRecord.value('propOrgStructure_id'))

                if orgStructureId is None:
                    orgStructureId = personInfo['orgStructureId']

                if orgStructureId:
                    data = CRBModelDataCache.getData('OrgStructure')
                    orgStructureCode = unicode(data.getCodeById(orgStructureId))
                    orgStructureName = unicode(data.getNameById(orgStructureId))
                    orgStructureType = forceString(db.translate('OrgStructure', 'id', orgStructureId, 'type'))
                    orgStructureExternalCode = getIdentification('OrgStructure', orgStructureId, 'lis.OrgStructure', False)
            setPersonCode = personInfo['code']
            setPersonName = personInfo['fullName']

            self.orgStructureCode = orgStructureCode
            self.orgStructureName = orgStructureName
            self.orgStructureType = orgStructureType
            self.orgStructureExternalCode = orgStructureExternalCode if orgStructureExternalCode else ''
            self.setPersonCode = setPersonCode
            self.setPersonName = setPersonName
            self.MKB = MKB

            (self.eventTypeRegionalCode,
             self.eventTypeName,
             self.eventMesCode,
             self.financeCode,
             self.eventExternalId,
             self.actionFinanceCode,
             self.contractNumber) = self._getAccountValues(actionId)


    def _getAccountValues(self, actionId):
        db = QtGui.qApp.db
        tableAction = db.table('Action')
        tableEvent = db.table('Event')
        tableEventType = db.table('EventType')
        tableMES = db.table('mes.MES')
        tableContract = db.table('Contract')
        tableFinance = db.table('rbFinance')
        tableActionFinance = db.table('rbFinance').alias('ActionFinance')
        tableActionContract = db.table('Contract').alias('ActionContract')

        queryTable = tableAction
        queryTable = queryTable.leftJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))
        queryTable = queryTable.leftJoin(tableEventType, tableEventType['id'].eq(tableEvent['eventType_id']))
        queryTable = queryTable.leftJoin(tableMES, tableMES['id'].eq(tableEvent['MES_id']))
        queryTable = queryTable.leftJoin(tableContract, tableContract['id'].eq(tableEvent['contract_id']))
        queryTable = queryTable.leftJoin(tableFinance, tableFinance['id'].eq(tableContract['finance_id']))
        queryTable = queryTable.leftJoin(tableActionFinance, tableActionFinance['id'].eq(tableAction['finance_id']))
        queryTable = queryTable.leftJoin(tableActionContract, tableActionContract['id'].eq(tableAction['contract_id']))

        cols = [tableEventType['regionalCode'].alias('eventTypeRegionalCode'),
                tableEventType['name'].alias('eventTypeName'),
                tableMES['code'].alias('eventMesCode'),
                tableFinance['code'].alias('financeCode'),
                tableEvent['externalId'].alias('eventExternalId'),
                tableActionFinance['code'].alias('actionFinanceCode'),
                tableContract['number'].alias('eventContractNumber'),
                tableActionContract['number'].alias('actionContractNumber')]

        cond = [tableAction['id'].eq(actionId),
                tableEvent['deleted'].eq(0),
                tableEventType['deleted'].eq(0),
#                tableActionPropertyType['test_id'].eq(testId),
               ]

        record = db.getRecordEx(queryTable, cols, cond)
        if record:
            return (forceString(record.value('eventTypeRegionalCode')),
                    forceString(record.value('eventTypeName')),
                    forceString(record.value('eventMesCode')),
                    forceString(record.value('financeCode')),
                    forceString(record.value('eventExternalId')),
                    forceString(record.value('actionFinanceCode')),
                    forceString(record.value('actionContractNumber'))
                    or forceString(record.value('eventContractNumber')))
        return '', '', '', '', '', '', ''


def selectASTMOrders(equipmentInterface, clientInfo, probeIdList):
    u'Сформировать заказы из списка id проб'
    db = QtGui.qApp.db
    tableProbe = db.table('Probe')
    tableTissue = db.table('TakenTissueJournal')
    tableEquipmentTest = db.table('rbEquipment_Test')

    table = tableProbe.leftJoin(tableEquipmentTest, db.joinAnd([tableEquipmentTest['equipment_id'].eq(tableProbe['equipment_id']),
                                                                tableEquipmentTest['test_id'].eq(tableProbe['workTest_id']),
                                                                tableEquipmentTest['specimenType_id'].eq(tableProbe['specimenType_id'])
                                                               ]
                                                              )
                               )
    table = table.leftJoin(     tableTissue, tableTissue['id'].eq(tableProbe['takenTissueJournal_id']))
    stmt = db.selectStmt(table,
                         [tableProbe['takenTissueJournal_id'],
                          tableTissue['datetimeTaken'],
                          tableProbe['externalId'],
                          tableProbe['id'].alias('probe_id'),
                          tableProbe['isUrgent'],
                          tableEquipmentTest['test_id'],
                          tableEquipmentTest['hardwareTestCode'],
                          tableEquipmentTest['hardwareTestName'],
                          tableEquipmentTest['hardwareSpecimenCode'],
                          tableEquipmentTest['hardwareSpecimenName'],
                          tableProbe['tripodNumber'],
                          tableProbe['placeInTripod'],
                          tableProbe['exportName']
                         ],
                         db.joinAnd([ tableProbe['id'].inlist(probeIdList),
                                      tableEquipmentTest['type'].eq(2)
                                    ]
                                   )
                        )
    query = db.query(stmt)
    mapKeyToOrders = {}
    while query.next():
       record = query.record()
       dateTime             = forceDateTime(record.value('datetimeTaken'))
#       takenTissueJournalId = forceRef(record.value('takenTissueJournal_id'))
       externalId  = forceString(record.value('externalId'))

       probeId     = forceRef(record.value('probe_id'))
       isUrgent    = forceBool(record.value('isUrgent'))
       testId = forceRef(record.value('test_id'))
       hardwareTestCode = forceString(record.value('hardwareTestCode'))
       hardwareTestName = forceString(record.value('hardwareTestName'))
       hardwareSpecimenCode = forceString(record.value('hardwareSpecimenCode'))
       hardwareSpecimenName = forceString(record.value('hardwareSpecimenName'))
       takenTissueJournalId = forceRef(record.value('takenTissueJournal_id'))
       tripodNumber = forceString(record.value('tripodNumber'))
       placeInTripod = forceInt(record.value('placeInTripod'))
       exportName = forceString(record.value('exportName'))
       key = ( dateTime.toPyDateTime(), externalId, takenTissueJournalId, exportName )

       order = mapKeyToOrders.get(key)
       if order is None:
           mapKeyToOrders[key] = order = CASTMOrder(clientInfo, dateTime, externalId, takenTissueJournalId)
           if equipmentInterface.opts.extendedValues:
               order.fillExtendedValues()
       order.tests.append( CASTMTestOrder(probeId,
                                          isUrgent,
                                          testId,
                                          hardwareTestCode,
                                          hardwareTestName,
                                          hardwareSpecimenCode,
                                          hardwareSpecimenName,
                                          tripodNumber,
                                          placeInTripod,
                                          exportName
                                         )
                         )
    return [ mapKeyToOrders[key]
             for key in sorted(mapKeyToOrders.iterkeys())
           ]


def sendOrderOverASTM(equipmentInterface, order, testList):
    u'Послать заказ (частичный заказ - см. testList) по протоколу ASTM'
    interface = CFileInterface(equipmentInterface.opts)
    clientInfo = order.clientInfo
    now = QDateTime.currentDateTime()
    message = CMessage()
    patient = message.newPatient()
    patient.patientId = clientInfo['id']
    patient.laboratoryPatientId = clientInfo['id']
    patient.lastName  = clientInfo['lastName']
    patient.firstName = clientInfo['firstName']
    patient.patrName  = clientInfo['patrName']
    patient.birthDate = clientInfo['birthDate']
    patient.sex = ['U', 'M', 'F'][clientInfo['sexCode']]
    patient.age = calcAgeInYears(clientInfo['birthDate'], order.dateTime.date())
    for contact in clientInfo.contacts:
        if contact[0] == u'электронная почта' or contact[0] == u'адрес электронной почты':
            patient.reserved = contact[1]
        if contact[0] == u'мобильный телефон' and not patient.phone:
            patient.phone = contact[1]
        if contact[0] == u'домашний телефон' and not patient.phone:
            patient.phone = contact[1]
    patient.dosageCategory = None
    if equipmentInterface.opts.extendedValues:
        patient.senderOrgStructureCode = order.orgStructureCode
        patient.senderOrgStructureName = order.orgStructureName
        patient.senderOrgStructureType = order.orgStructureType
        patient.senderPersonCode = order.setPersonCode
        patient.senderPersonName = order.setPersonName
        patient.senderOrgStructureExternalCode = order.orgStructureExternalCode
        patient.diagnosis = order.MKB
        patient.eventTypeRegionalCode = order.eventTypeRegionalCode
        patient.eventTypeName = order.eventTypeName
        patient.eventMesCode = order.eventMesCode
        patient.eventExternalId = order.eventExternalId

        patient.addressStreet = clientInfo.get('locAddress', '') or clientInfo.get('regAddress', '')
        documentRecord = clientInfo.get('documentRecord')
        if documentRecord:
            patient.documentType = forceString(QtGui.qApp.db.translate(
                                                        'rbDocumentType',
                                                        'id',
                                                        documentRecord.value('documentType_id'),
                                                        'regionalCode')
                                                        )
            patient.documentSerial = forceString(documentRecord.value('serial'))
            patient.documentNumber = forceString(documentRecord.value('number'))
        policyType = 'voluntaryPolicyRecord' if order.financeCode == '3' else 'compulsoryPolicyRecord'
        if clientInfo.get(policyType):
            patient.policySerial = forceString(clientInfo[policyType].value('serial'))
            patient.policyNumber = forceString(clientInfo[policyType].value('number'))

    exportName = None

    for test in testList:
        if exportName is None:
            exportName = test.exportName
        elif test.exportName and exportName != test.exportName:
            exportName = ''
        orderItem = patient.newOrder()
        orderItem.specimenId      = order.label
#        orderItem.instrumentSpecimenId = order.label
        if equipmentInterface.specimenIdentifierMode  == SPECIMEN_IDENTIFIER_MODE.positionMode:
            if test.tripodNumber and test.placeInTripod:
                if equipmentInterface.opts.get('useSpecimenForTripod', False):
                    orderItem.specimenIndex = test.tripodNumber
                    orderItem.specimenCount = test.placeInTripod
                else:
                    orderItem.instrumentSpecimenId = test.tripodNumber
                    orderItem.instrumentSpecimenIndex = test.placeInTripod
            else:
                orderItem.instrumentSpecimenIndex = order.tests.index(test)+1
                orderItem.instrumentSpecimenCount = len(order.tests)
        if equipmentInterface.opts.uniTestId:
            orderItem.testId = test.testCode
        if equipmentInterface.opts.testCode:
            orderItem.assayCode = test.testCode
        if equipmentInterface.opts.uniTestName:
            orderItem.assayName = test.testName
        orderItem.requestDateTime =  now
        orderItem.specimenCollectionDateTime = order.dateTime
        orderItem.priority        = 'A' if test.isUrgent else 'R'
        orderItem.actionCode      = 'A'
        orderItem.specimenDescr   = test.specimenCode
        orderItem.userField1      = test.probeId
#        orderItem.userField2      = test.probeId
        orderItem.reportTypes     = 'O'
        #orderItem.specimenInstitution='LAB2'
        if equipmentInterface.opts.extendedValues:
            orderItem.laboratoryField1Finance = order.actionFinanceCode
            orderItem.laboratoryField1EventTypeRegionalCode = order.eventTypeRegionalCode
            orderItem.laboratoryField1ContractNumber = order.contractNumber

    headerValues = {'receiverName' : equipmentInterface.labName,
                    'receiverCode' : equipmentInterface.labCode,
                    'version'      : equipmentInterface.protocolVersion,
                    'processingId' : equipmentInterface.opts.processingId
                   }
    records = message.getRecords(encoding=equipmentInterface.opts.encoding, headerValues=headerValues)
    filePath = interface.write(CBaseMessage(records),
                               forceFileName=exportName if exportName else '',
                               appendIntoFileName=order.label if equipmentInterface.opts.appendIbmIntoFileName else u'')

    return os.path.basename(filePath)
