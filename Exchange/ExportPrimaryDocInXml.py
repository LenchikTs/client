# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2019 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDate, QDir, QFile, QIODevice, QVariant, QXmlStreamWriter, pyqtSignature

from library.SendMailDialog import sendMail
from library.Utils  import forceDate, forceRef, forceString, forceStringEx, toVariant

from Events.Utils   import getEventName, getWorkEventTypeFilter
from Exchange.Utils import tbl, checkEmail, compressFileInRar
from Registry.Utils import getClientInfoEx, getInfisForStreetKLADRCode, getInfisForKLADRCode

from Exchange.Ui_ExportPrimaryDocInXml import Ui_ExportPrimaryDocInXmlDialog


eventDateFields = ('setDate', 'execDate')
eventFields = ('isPrimary', 'order', 'externalId') + eventDateFields

actionDateFields = ('directionDate', 'begDate', 'endDate')
actionFields = ('status', 'uet', 'amount', 'note') + actionDateFields

clientDateFields = ('birthDate', )
clientCommonFields = ('sex', ) + clientDateFields
clientIdFields = ('lastName', 'firstName', 'patrName', 'SNILS')
clientFields = clientCommonFields + clientIdFields

diagnosticDateFields = ('setDate', 'endDate')
diagnosticFields = ('sanatorium', 'hospital', ) + diagnosticDateFields

diagnosisDateFields = ('setDate', 'endDate')
diagnosisFields = ('MKB', 'MKBEx', 'morphologyMKB', 'TNMS') + diagnosisDateFields

visitDateFields = ('date', )
visitFields = ('isPrimary', ) + visitDateFields

rbFields = ('code', 'name')
personFields = rbFields
specialityFields = rbFields
mesFields = rbFields
mesSpecificationFields = rbFields
eventTypeFields = rbFields
financeFields = rbFields
actionTypeFields = rbFields
resultFields = ('code', )
contractFields = ('number', )
identifierFields = ('code', 'name', 'identifier')
documentTypeFields = rbFields
visitTypeFields = rbFields
serviceFields = rbFields
sceneFields = rbFields
characterFields = rbFields
diagnosisTypeFields = rbFields

personGroup = {
    'speciality' : {'fields': specialityFields, 'prefix': 'person'}
}

execPersonGroup = {
    'speciality' : {'fields': specialityFields,  'prefix': 'execPerson'},
}

eventGroup = {
    'execPerson': {'fields': personFields, 'subGroup': execPersonGroup},
    'mes': {'fields': mesFields},
    'mesSpecification': {'fields': mesSpecificationFields},
    'eventType': {'fields': eventTypeFields},
    'finance': {'fields': financeFields}
#    'client': (clientFields, clientGroup),
#    'action': (actionFields, actionGroup),
#'visit': (personFields, {}),
#'diagnostic': (personFields, {}),
}

actionGroup = {
    'actionType': {'fields': actionTypeFields},
    'finance': {'fields': financeFields}
}

visitGroup = {
    'person': {'fields': personFields, 'subGroup': personGroup},
    'scene' : {'fields': sceneFields},
    'visitType': {'fields': visitTypeFields},
    'finance': {'fields': financeFields},
    'service' : {'fields': serviceFields},
}

diagnosticGroup = {
    'person': {'fields': personFields, 'subGroup': personGroup},
    'character': {'fields': characterFields},
    'diagnosisType': {'fields': diagnosisTypeFields},
    'diagnosis': {'fields': diagnosisFields, 'dateFields':diagnosisDateFields},
    'speciality' : {'fields': specialityFields},
}

exportVersion = '1.2'


def ExportPrimaryDocInXml(parent):
    QtGui.qApp.setWaitCursor()
    dlg = CExportPrimaryDocInXml(parent)
    dlg.edtFilePath.setText(forceString(QtGui.qApp.preferences.appPrefs.get('ExportPrimaryDocInXml', '')))
    dlg.edtDateFrom.setDate(forceDate(QtGui.qApp.preferences.appPrefs.get('ExportPrimaryDocInXmlBegDate', QDate.currentDate())))
    dlg.edtDateTo.setDate(forceDate(QtGui.qApp.preferences.appPrefs.get('ExportPrimaryDocInXmlEndDate', QDate.currentDate())))
    QtGui.qApp.restoreOverrideCursor()
    dlg.exec_()
    QtGui.qApp.preferences.appPrefs['ExportPrimaryDocInXml'] = toVariant(dlg.edtFilePath.text())
    QtGui.qApp.preferences.appPrefs['ExportPrimaryDocInXmlBegDate'] = toVariant(dlg.edtDateFrom.date())
    QtGui.qApp.preferences.appPrefs['ExportPrimaryDocInXmlEndDate'] = toVariant(dlg.edtDateTo.date())


class CXmlStreamWriter(QXmlStreamWriter):
    def __init__(self, parent=None):
        QXmlStreamWriter.__init__(self)
        self.parent = parent
        self.currentTypeNeedForceEnd = None #???
        self.setAutoFormatting(True)

    def writeElement(self, elementName, value=None):
        if value is not None:
            self.writeTextElement(elementName, value)
            self.currentTypeNeedForceEnd = False
        else:
            self.writeStartElement(elementName)
            self.currentTypeNeedForceEnd = True

    def writeNamespace(self, nameSpace, prefix):
        QXmlStreamWriter.writeNamespace(self, nameSpace, prefix)

    def endElement(self):
        self.writeEndElement()

    def stopWriting(self):
        self.device().close()


class CBaseExport(object):

    def badFile(self):
        QtGui.QMessageBox.critical(self,
                                   u'Внимание!',
                                   u'Не удалось открыть файл экспорта на запись!',
                                   QtGui.QMessageBox.Close)

    def getWriter(self):
        return self.writer

    def setWriter(self, writer):
        self.writer = writer

    def writeAttribute(self, attrName, value):
        self.writer.writeAttribute(attrName, value)

    def writeElement(self, elementName, value=None):
        self.writer.writeElement(elementName, value)

    def writeNamespace(self, nameSpace, prefix):
        self.writer.writeNamespace(nameSpace, prefix)

    def setDevice(self, device):
        self.writer.setDevice(device)

    def getDevice(self):
        return self.writer.device()

    def endElement(self):
        self.writer.endElement()

    def startWriting(self):
        self.writer.writeStartDocument()

    def stopWriting(self):
        self.endElement()
        self.writer.writeEndDocument()
        self.writer.stopWriting()

    def makeRar(self, filePath, rarFilePath=''):
        compressFileInRar(filePath, rarFilePath)

    def sendMail(self, email, subject, text='', attach=[]):
        sendMail(self, email, subject, text, attach)



class CExportPrimaryDocInXml(QtGui.QDialog, CBaseExport, Ui_ExportPrimaryDocInXmlDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.checkRun = False
        self.abort = False
        self.cmbSpeciality.setTable('rbSpeciality', True)
        self.progressBar.setFormat('%v')
        self.progressBar.setValue(0)
        self.tableEvent = tbl('Event')
        self.tableEventType = tbl('EventType')
        self.tableAction = tbl('Action')
        self.tableActionType = tbl('ActionType')
        self.tableClient = tbl('Client')
        self.tableVisit = tbl('Visit')
        self.tablePerson = tbl('vrbPersonWithSpeciality').alias('ExecPerson')
        self.tableTempInvalidPeriod = tbl('TempInvalid_Period')
        self.setWriter(CXmlStreamWriter())
        self.filePath = ''
        self.cmbEventPurpose.setTable('rbEventTypePurpose', False, filter='code != \'0\'')
        self.cmbEventType.setTable('EventType', False, filter=getWorkEventTypeFilter())
        self.cmbEventProfile.setTable('rbEventProfile', True)
        self.setWindowTitle(u'Экспорт первичных документов в XML')
        self.tempInvalidCond =  []
        self.xsdFile = None
        self.defaultSpecialityCodeFieldName = 'OKSOCode'
        self.cmbPersonSpecialityCode.addItem(u'ОКСО', QVariant('OKSOCode'))
        self.cmbPersonSpecialityCode.addItem(u'Региональный', QVariant('regionalCode'))
        self.cmbPersonSpecialityCode.addItem(u'МИС (внутрениий)', QVariant('code'))

        self.clientIdentificationCache = {}
        self.documentTypeCache = {}
        self.cacheHits = 0
        self.cacheMiss = 0
        self.db = QtGui.qApp.db

        self.getDocumentTypeRecord = lambda id: self.getRecord(id,
                    'rbDocumentType', self.documentTypeCache)


    def makeQuery(self, params):
        QtGui.qApp.setWaitCursor()
        def calcBirthDate(cnt):
            result = QDate.currentDate()
            return result.addYears(-cnt)
        self.btnClose.setText(u'Стоп')
        db = QtGui.qApp.db
        dateFrom = params.get('dateFrom', None)
        dateTo   = params.get('dateTo', None)
        specialityId = params.get('specialityId', None)
        doctorPersonId = params.get('doctorPersonId', None)
        ageBegin = params.get('ageBegin', None)
        ageEnd = params.get('ageEnd', None)
        sex = params.get('sex', None)
        onlyMes = params.get('onlyMes', None)

        cond = []
        cond.append(self.tableEvent['execDate'].le(dateTo))
        cond.append(self.tableEvent['execDate'].ge(dateFrom))
        cond.append(self.tableEvent['deleted'].eq(0))
        if specialityId:
            cond.append(self.tablePerson['speciality_id'].eq(specialityId))
        if doctorPersonId:
            cond.append(self.tablePerson['id'].eq(doctorPersonId))
        if sex:
            cond.append(self.tableClient['sex'].eq(sex))
        if ageBegin:
            cond.append(self.tableClient['birthDate'].le(calcBirthDate(ageBegin)))
            cond.append(self.tableClient['birthDate'].ge(calcBirthDate(ageEnd)))
        if onlyMes:
            cond.append(self.tableEvent['MES_id'].isNotNull())
            purposeId      = params.get('purposeId', None)
            eventTypeId    = params.get('eventTypeId', None)
            eventProfileId = params.get('eventProfileId', None)
            mesId          = params.get('mesId', None)
            if purposeId:
                cond.append(self.tableEventType['purpose_id'].eq(purposeId))
            if eventTypeId:
                cond.append(self.tableEventType['id'].eq(eventTypeId))
            if eventProfileId:
                cond.append(self.tableEventType['eventProfile_id'].eq(eventProfileId))
            if mesId:
                cond.append(self.tableEvent['MES_id'].eq(mesId))
        if params.get('isPolicy', None):
            insurerId = params.get('insurerId', None)
            policyType = params.get('policyType', None)
            if policyType:
                if policyType == u'ОМС':
                    if insurerId:
                        cond.append('ClientPolicyCompulsory.`insurer_id`=%d'%insurerId)
                    else:
                        cond.append('ClientPolicyCompulsory.`insurer_id` IS NULL')
                else:
                    if insurerId:
                        cond.append('ClientPolicyVoluntary.`insurer_id`=%d'%insurerId)
                    else:
                        cond.append('ClientPolicyVoluntary.`insurer_id` IS NULL')
            else:
                if insurerId:
                    cond.append(db.joinOr(['ClientPolicyCompulsory.`insurer_id`=%d'%insurerId, 'ClientPolicyVoluntary.`insurer_id`=%d'%insurerId]))
                else:
                    cond.append(db.joinAnd(['ClientPolicyCompulsory.`insurer_id` IS NULL', 'ClientPolicyVoluntary.`insurer_id` IS NULL']))

        specialityCodeFieldName = params.get('specialityCodeFieldName', '')
        if not specialityCodeFieldName:
            specialityCodeFieldName = self.defaultSpecialityCodeFieldName

        stmt = '''
SELECT
    Client.`id` AS clientId, %s,
    Event.`id` AS eventId, %s,
    Contract.`number` AS contract_number,
    EventType.`code` AS eventType_code,
    EventType.`name` AS eventType_name,
    rbFinance.`name` AS finance_name,
    rbFinance.`code` AS finance_code,
    rbResult.`code` AS result_code,
    ExecPerson.`id` AS eventExecPersonId,
    ExecPerson.`code` AS execPerson_code,
    ExecPerson.`name` AS execPerson_name,
    rbSpeciality.`%s` AS execPerson_speciality_code,
    rbSpeciality.`name` AS execPerson_speciality_name,
    mes.MES.`name` AS mes_name,
    mes.MES.`code` AS mes_code,
    rbMesSpecification.`name` AS mesSpecification_name,
    rbMesSpecification.`code` AS mesSpecification_code,
    ClientPolicyCompulsory.`insurer_id` AS ClientCompulsoryInsurerId,
    ClientPolicyVoluntary.`insurer_id` AS ClientVoluntaryInsurerId
FROM Event
    LEFT OUTER JOIN Contract ON Event.`contract_id`=Contract.`id`
    INNER JOIN Client ON Client.`id`=Event.`client_id`
    INNER JOIN EventType ON EventType.`id`=Event.`eventType_id`
    LEFT OUTER JOIN rbFinance ON EventType.`finance_id`=rbFinance.`id`
    INNER JOIN rbResult ON rbResult.`id`=Event.`result_id`
    INNER JOIN vrbPerson AS ExecPerson ON ExecPerson.`id`=Event.`execPerson_id`
    INNER JOIN rbSpeciality ON rbSpeciality.`id`= ExecPerson.`speciality_id`
    LEFT OUTER JOIN mes.MES ON Event.`MES_id`=mes.MES.`id`
    LEFT OUTER JOIN rbMesSpecification ON Event.`mesSpecification_id`=rbMesSpecification.`id`
    LEFT OUTER JOIN ClientPolicy AS ClientPolicyCompulsory ON ClientPolicyCompulsory.`id`=getClientPolicyId(Client.`id`, 1)
    LEFT OUTER JOIN ClientPolicy AS ClientPolicyVoluntary ON ClientPolicyVoluntary.`id`=getClientPolicyId(Client.`id`, 0)
WHERE %s
        ''' % (
               ','.join(['Client.`%s` AS client_%s' % (fieldName,  fieldName) for fieldName in clientFields]),
                ','.join(['Event.`%s` AS event_%s' % (fieldName,  fieldName) for fieldName in eventFields]),
               specialityCodeFieldName, db.joinAnd(cond))
        query = db.query(stmt)
        QtGui.qApp.restoreOverrideCursor()
        self.parseQuery(query, params)


    def writerFuncEx(self, prefix, rec, field, dateFields=tuple()):
        val = '%s_%s' % (prefix, field)

        if field in dateFields:
            self.writeElement(field, forceDate(rec.value(val)).toString(Qt.ISODate))
        else:
            self.writeElement(field, forceString(rec.value(val)))


    def writeGroup(self, groupName, fieldList, record,  subGroup={}, closeGroup=True, namePrefix=None, dateFields = tuple()):
        self.writeElement(groupName)

        if namePrefix:
            groupName = '%s_%s' % (namePrefix, groupName)

        map(lambda field: self.writerFuncEx(groupName, record, field, dateFields), fieldList)

        for (name,  val) in subGroup.iteritems():
            self.writeGroup(name, val.get('fields', tuple()),
                record, val.get('subGroup',{} ),
                True, val.get('prefix'),
                val.get('dateFields', tuple()))

        if closeGroup:
            self.endElement()


    def getRecord(self, id, tableName, cache):
        result = cache.get(id)

        if result:
            self.cacheHits += 1
        else:
            result = self.db.getRecord(tableName, '*', id)
            cache[id] = result
            self.cacheMiss += 1

        return result


    def parseQuery(self, query, params):
        self.cacheHits = 0
        self.checkRun = True
        count = query.size()
        self.progressBar.setMaximum(count)
        n = 0
        self.filePath = forceStringEx(self.edtFilePath.text())
        if self.filePath[-4:] != '.xml':
            self.filePath = self.filePath+'.xml'
        _file = QFile(self.filePath)
        if not _file.open(QIODevice.WriteOnly | QIODevice.Text):
            self.badFile()
            return
        else:
            self.setDevice(_file)

        self.startWriting()
        self.writeElement('Export')
        self.writeAttribute('exportVersion', exportVersion)
        self.writeAttribute('date', forceString(QDate.currentDate()))
        self.writeElement('MIS', 'SAMSON-VISTA')
        try:
            from buildInfo import lastChangedRev
            self.writeElement('revision', 'v2.0/'+lastChangedRev)
        except:
            self.writeElement('revision', 'v2.0/unknown')
        self.writeHeader(params)

        while query.next():
            QtGui.qApp.processEvents()

            if self.abort:
                self.checkRun = False
                break

            record = query.record()
            clientId = forceRef(record.value('clientId'))
            clientInfo = getClientInfoEx(clientId)
            eventId = forceRef(record.value('eventId'))
            eventExecPersonId = forceRef(record.value('eventExecPersonId'))

            self.writeGroup('event', eventFields, record, eventGroup, False, dateFields=eventDateFields)

            self.writeElement('Client')
            map(lambda field: self.writerFuncEx('client', record, field, clientDateFields), clientCommonFields)

            identificationRecords = self.getClientIdentification(clientId)
            map(lambda rec: self.writeGroup('identifier', identifierFields, rec), identificationRecords)

            if params.get('exportClientData'):
                map(lambda field: self.writerFuncEx('client', record, field, clientDateFields), clientIdFields)

                self.writeElement('document')
                self.writeElement('formated', clientInfo.get('document', ''))
                documentRecord = clientInfo.get('documentRecord')

                if documentRecord and params.get('detailDocument'):
                    documentTypeId = forceRef(documentRecord.value('documentType_id'))
                    if documentTypeId:
                        documentTypeRecord = self.getDocumentTypeRecord(documentTypeId)
                        if documentTypeRecord:
                            self.writeGroup('type', documentTypeFields, documentTypeRecord)

                        self.writeElement('serial', forceString(documentRecord.value('serial')))
                        self.writeElement('number', forceString(documentRecord.value('number')))

                self.endElement() #close document

                self.writeElement('policy')
                compulsoryPolicyRecord = clientInfo.get('compulsoryPolicyRecord', None)
                voluntaryPolicyRecord  = clientInfo.get('voluntaryPolicyRecord', None)
                if compulsoryPolicyRecord:
                    policyRecord = compulsoryPolicyRecord
                    self.writeElement('compulsoryPolicyFormated', clientInfo.get('compulsoryPolicy', ''))
                    if params.get('detailPolicy'):
#                        self.writeElement('compulsoryPolicyName', forceString(policyRecord.value('name')))
                        self.writeElement('compulsoryPolicyInsurer', forceString(QtGui.qApp.db.translate('Organisation', 'id', policyRecord.value('insurer_id'), 'shortName')))
                        policyTypeName = forceString(QtGui.qApp.db.translate('rbPolicyType', 'id', policyRecord.value('policyType_id'), 'name'))
                        self.writeElement('compulsoryPolicyType', policyTypeName)
                        self.writeElement('compulsoryPolicySerial', forceString(policyRecord.value('serial')))
                        self.writeElement('compulsoryPolicyNumber', forceString(policyRecord.value('number')))
                        self.writeElement('compulsoryPolicyBegDate', forceString(policyRecord.value('begDate')))
                        self.writeElement('compulsoryPolicyEndDate', forceString(policyRecord.value('endDate')))

                if voluntaryPolicyRecord:
                    policyRecord = voluntaryPolicyRecord
                    self.writeElement('voluntaryPolicyFormated', clientInfo.get('voluntaryPolicy', ''))
                    if params.get('detailPolicy'):
#                        self.writeElement('voluntaryPolicyName', forceString(policyRecord.value('name')))
                        self.writeElement('voluntaryPolicyInsurer', forceString(QtGui.qApp.db.translate('Organisation', 'id', policyRecord.value('insurer_id'), 'shortName')))
                        policyTypeName = forceString(QtGui.qApp.db.translate('rbPolicyType', 'id', policyRecord.value('policyType_id'), 'name'))
                        self.writeElement('voluntaryPolicyType', policyTypeName)
                        self.writeElement('voluntaryPolicySerial', forceString(policyRecord.value('serial')))
                        self.writeElement('voluntaryPolicyNumber', forceString(policyRecord.value('number')))
                        self.writeElement('voluntaryPolicyBegDate', forceString(policyRecord.value('begDate')))
                        self.writeElement('voluntaryPolicyEndDate', forceString(policyRecord.value('endDate')))
                self.endElement() #close policy
                self.writeElement('regAddress')
                self.writeElement('formated', clientInfo.get('regAddress', ''))
                regAdressInfo = clientInfo.get('regAddressInfo', None)
                if regAdressInfo and params.get('detailAddress'):
                    self.writeElement('KLADRCode', regAdressInfo.KLADRCode)
                    self.writeElement('KLADRStreetCode', regAdressInfo.KLADRStreetCode)
                    self.writeElement('KLADRCodeInfis', getInfisForKLADRCode(regAdressInfo.KLADRCode))
                    self.writeElement('KLADRStreetCodeInfis', getInfisForStreetKLADRCode(regAdressInfo.KLADRStreetCode))
                    self.writeElement('number', regAdressInfo.number)
                    self.writeElement('сorpus', regAdressInfo.corpus)
                    self.writeElement('аlat', regAdressInfo.flat)
                self.endElement() #close regAddress
                self.writeElement('locAddress')
                self.writeElement('formated', clientInfo.get('locAddress', ''))
                locAdressInfo = clientInfo.get('locAddressInfo', None)
                if locAdressInfo and params.get('detailAddress'):
                    self.writeElement('KLADRCode', locAdressInfo.KLADRCode)
                    self.writeElement('KLADRStreetCode', locAdressInfo.KLADRStreetCode)
                    self.writeElement('KLADRCodeInfis', getInfisForKLADRCode(locAdressInfo.KLADRCode))
                    self.writeElement('KLADRStreetCodeInfis', getInfisForStreetKLADRCode(locAdressInfo.KLADRStreetCode))
                    self.writeElement('number', locAdressInfo.number)
                    self.writeElement('corpus', locAdressInfo.corpus)
                    self.writeElement('flat', locAdressInfo.flat)
                self.endElement() #close locAddress
            self.endElement() #close client

            if params.get('exportTempInvalid'):
                tempInvalidRecords = self.getClientTempInvalid(clientId, params)
                for tempInvalidRecord in tempInvalidRecords:
                    self.writeElement('TempInvalid')
                    self.writeElement('begDate', forceString(tempInvalidRecord.value('begDate')))
                    self.writeElement('endDate', forceString(tempInvalidRecord.value('endDate')))
                    self.writeElement('state', forceString(tempInvalidRecord.value('state')))
                    self.writeElement('invalidReasonCode', forceString(tempInvalidRecord.value('invalidReasonCode')))
                    self.writeElement('invalidReasonName', forceString(tempInvalidRecord.value('invalidReasonName')))
                    self.endElement() #close tempInvalid

            if params.get('exportActions'):
               self.exportActions(eventId, eventExecPersonId, params)

            if params.get('exportVisits'):
                self.exportVisits(eventId, params)

            self.exportDiagnostics(eventId, params)
            self.endElement() #close event
            n += 1
            self.progressBar.setValue(n)

        self.endElement() #close export
        self.stopWriting()
        self.checkRun = False
        print('Cache hits: %d, miss %d, ratio %.2f%% ' % (self.cacheHits, self.cacheMiss,
                                                      (100*self.cacheHits/self.cacheMiss) if self.cacheMiss != 0 else 0))
        sendRar = False
        if params.get('makeRar', None):
            sendRar = self.makeRar(self.filePath)
        email = params.get('e-mail', None)
        if email:
            if sendRar:
                whatSend = self.filePath+'.rar'
            else:
                whatSend = self.filePath
            self.sendMail(email, u'Экспорт первичных документов', '', [whatSend])
        self.btnClose.setText(u'Закрыть')
        self.tempInvalidCond =  []


    def exportDiagnostics(self, eventId, params):
        diagnosticsRecords = self.getDiagnosticsInfo(eventId, params)

        for record in diagnosticsRecords:
            self.writeGroup('diagnostic', diagnosticFields, record, diagnosticGroup, dateFields=diagnosticDateFields)


    def exportActions(self, eventId, eventExecPersonId, params):
        actionRecords = self.getActionsInfo(eventId, params)

        for record in actionRecords:
            self.writeGroup('Action', actionFields, record, actionGroup, False, dateFields=actionDateFields)
            actionExecPersonId = forceRef(record.value('actionExecPersonId'))

            if actionExecPersonId:
                if actionExecPersonId == eventExecPersonId:
                    self.writeElement('healer', 'yes')
                else:
                    self.writeElement('healer', 'no')
                if forceRef(record.value('execPersonOrgId')) == QtGui.qApp.currentOrgId():
                    self.writeElement('externalHealer', 'no')
                else:
                    self.writeElement('externalHealer', 'yes')

            if params.get('exportActionExecPerson'):
                self.writeGroup('execPerson', personFields, record, execPersonGroup)

            self.endElement() #close action


    def exportVisits(self, eventId, params):
        visitRecords = self.getVisitsInfo(eventId, params)

        for record in visitRecords:
            self.writeGroup('visit', visitFields, record, visitGroup, dateFields=visitDateFields)


    def getVisitsInfo(self, eventId, params):
        specialityCodeFieldName = params.get('specialityCodeFieldName', '')

        if not specialityCodeFieldName:
            specialityCodeFieldName = self.defaultSpecialityCodeFieldName

        stmt = '''SELECT
    Visit.`date` AS visit_date,
    Visit.`isPrimary` AS visit_isPrimary,
    rbScene.`name` AS scene_name,
    rbScene.`code` AS scene_code,
    PersonTable.`code` AS person_code,
    PersonTable.`name` AS person_name,
    rbSpeciality.`%s` AS person_speciality_code,
    rbSpeciality.`name` AS person_speciality_name,
    rbVisitType.`name` AS visitType_name,
    rbVisitType.`code` AS visitType_code,
    rbFinance.`code` AS finance_code,
    rbFinance.`name` AS finance_name,
    rbService.`code` AS service_code,
    rbService.`name` AS service_name
FROM Visit
LEFT OUTER JOIN vrbPerson AS PersonTable ON PersonTable.`id`=Visit.`person_id`
LEFT OUTER JOIN rbSpeciality ON rbSpeciality.`id`= PersonTable.`speciality_id`
INNER JOIN rbScene ON rbScene.`id`=Visit.scene_id
INNER JOIN rbVisitType ON rbVisitType.`id`=Visit.`visitType_id`
LEFT OUTER JOIN rbFinance ON Visit.`finance_id`=rbFinance.`id`
LEFT OUTER JOIN rbService ON Visit.`service_id`=rbService.`id`
WHERE Visit.`event_id`=%d''' % (specialityCodeFieldName, eventId)
        return self.execStmt(stmt)


    def getActionsInfo(self, eventId, params):
        cond = [self.tableAction['event_id'].eq(eventId),
                self.tableAction['deleted'].eq(0)]
        if params.get('onlyNomenclativeActions', None):
            cond.append(self.tableActionType['nomenclativeService_id'].isNotNull())

        specialityCodeFieldName = params.get('specialityCodeFieldName', '')
        if not specialityCodeFieldName:
            specialityCodeFieldName = self.defaultSpecialityCodeFieldName

        stmt = '''SELECT
    Action.`id` AS actionId, Action.`uet`, Action.`amount`, Action.`directionDate` AS actionDirectionDate,
    Action.`begDate` AS actionBegDate, Action.`endDate` AS actionEndDate, Action.`status`, Action.`note`,
    ActionType.`class` AS actionTypeClass,ActionType.`nomenclativeService_id`,
    ActionType.`code` AS actionTypeCode, ActionType.`name` AS actionTypeName,
    rbFinance.`code` AS actionFinanceCode, rbFinance.`name` AS actionFinanceName,
    ExecPerson.`id` AS actionExecPersonId ,
    ExecPerson.`org_id` AS execPersonOrgId,
    ExecPerson.`name`AS execPerson_name,
    ExecPerson.`code` AS execPerson_code,
    rbSpeciality.`name` AS execPerson_speciality_name,
    rbSpeciality.`%s` AS execPerson_speciality_code
FROM Action
INNER JOIN ActionType ON ActionType.`id`=Action.`actionType_id`
LEFT OUTER JOIN rbFinance ON Action.`finance_id`=rbFinance.`id`
LEFT OUTER JOIN vrbPerson AS ExecPerson ON Action.`person_id`=ExecPerson.`id`
LEFT OUTER JOIN rbSpeciality ON rbSpeciality.`id`=ExecPerson.`speciality_id`
WHERE %s''' % (specialityCodeFieldName, QtGui.qApp.db.joinAnd(cond))
        return self.execStmt(stmt)


    def getClientIdentification(self, clientId):
        result = self.clientIdentificationCache.get(clientId)

        if not result:
            stmt = 'SELECT r.code, r.name, ci.identifier FROM ClientIdentification ci LEFT JOIN rbAccountingSystem r ON r.id = ci.accountingSystem_id WHERE ci.deleted = 0 AND ci.client_id = %d' % clientId
            result = self.execStmt(stmt)
            self.clientIdentificationCache[clientId] = result
            self.cacheMiss += 1
        else:
            self.cacheHits += 1

        return result


    def getClientTempInvalid(self, clientId, params):
        dateFrom = params.get('dateFrom', None)
        dateTo   = params.get('dateTo', None)
        if not self.tempInvalidCond:
            self.tempInvalidCond.append(self.tableTempInvalidPeriod['begDate'].le(dateTo))
            self.tempInvalidCond.append(self.tableTempInvalidPeriod['endDate'].ge(dateFrom))
            if params.get('exportOnlyClosedTempInvalid', None):
                self.tempInvalidCond.append('TempInvalid.`state`=1')
        stmt = '''
SELECT
    TempInvalid_Period.`begDate`, TempInvalid_Period.`endDate`, TempInvalid.`state`,
    rbTempInvalidReason.`code` AS invalidReasonCode, rbTempInvalidReason.`name` AS invalidReasonName
FROM TempInvalid
INNER JOIN rbTempInvalidReason ON rbTempInvalidReason.`id` = TempInvalid.`tempInvalidReason_id`
INNER JOIN TempInvalid_Period ON TempInvalid_Period.`master_id`=TempInvalid.`id`
WHERE TempInvalid.`client_id`=%d and %s''' % (clientId, QtGui.qApp.db.joinAnd(self.tempInvalidCond))
        return self.execStmt(stmt)


    def getDiagnosticsInfo(self, eventId, params):
        specialityCodeFieldName = params.get('specialityCodeFieldName',
                                             self.defaultSpecialityCodeFieldName)
        onlyEndDiagnostic = params.get('onlyEndDiagnostic')
        endDiagnosticCond = ' AND rbDiagnosisType.`code` in (\'1\',\'2\',\'7\')'\
            ' ORDER BY rbDiagnosisType.`code` ' if onlyEndDiagnostic else ''

        stmt = '''SELECT %s, %s,
                CreatePerson.`name` AS person_name,
                CreatePerson.`code` AS person_code,
                PersonSpeciality.`%s` AS person_speciality_code,
                PersonSpeciality.`name` AS person_speciality_name,
                rbDiagnosisType.`name` AS diagnosisType_name,
                rbDiagnosisType.`code` AS diagnosisType_code,
                rbDiseaseCharacter.`name` AS character_name,
                rbDiseaseCharacter.`code` AS character_code,
                rbSpeciality.`%s` AS speciality_code,
                rbSpeciality.name AS speciality_name
            FROM Diagnostic
            LEFT OUTER JOIN vrbPerson AS CreatePerson ON Diagnostic.`person_id`=CreatePerson.`id`
            LEFT OUTER JOIN rbSpeciality AS PersonSpeciality ON PersonSpeciality.`id`=CreatePerson.`speciality_id`
            LEFT JOIN rbSpeciality ON Diagnostic.speciality_id = rbSpeciality.id
            INNER JOIN Diagnosis ON Diagnosis.`id`=Diagnostic.`diagnosis_id`
            INNER JOIN rbDiagnosisType ON rbDiagnosisType.`id`=Diagnostic.`diagnosisType_id`
            LEFT OUTER JOIN rbDiseaseCharacter ON Diagnostic.`character_id`=rbDiseaseCharacter.`id`
            WHERE Diagnostic.`event_id`=%d
                AND Diagnostic.`deleted`=0
                AND Diagnosis.`deleted`=0 %s''' % (
                    ','.join(['Diagnostic.%s AS diagnostic_%s' % (f,  f) for f in diagnosticFields]),
                    ','.join(['Diagnosis.%s AS diagnosis_%s' % (f,  f) for f in diagnosisFields]),
                                                   specialityCodeFieldName, specialityCodeFieldName,
                                                   eventId, endDiagnosticCond)

        if onlyEndDiagnostic:
            return self.execStmt(stmt)[:1]

        return self.execStmt(stmt)


    def execStmt(self, stmt):
        query = QtGui.qApp.db.query(stmt)
        records = []
        while query.next():
            records.append(query.record())
        return records


    def writeHeader(self, params):
        orgId = QtGui.qApp.currentOrgId()
        record = QtGui.qApp.db.getRecord('Organisation', '*', orgId)
        if record:
            shortName = forceString(record.value('shortName'))
            infisCode = forceString(record.value('infisCode'))
            INN       = forceString(record.value('INN'))
            OGRN      = forceString(record.value('OGRN'))
            miacCode  = forceString(record.value('miacCode'))

            self.writeElement('Header')
            self.writeElement('Organisation')
            self.writeAttribute('id', str(orgId))
            self.writeElement('shortName', shortName)
            self.writeElement('infisCode', infisCode)
            self.writeElement('INN', INN)
            self.writeElement('OGRN', OGRN)
            self.writeElement('miacCode', miacCode)
            self.endElement()

            dateFrom = params.get('dateFrom', None)
            dateTo   = params.get('dateTo', None)
#            specialityId = params.get('specialityId', None)
#            doctorPersonId = params.get('doctorPersonId', None)
            ageBegin = params.get('ageBegin', None)
            ageEnd = params.get('ageEnd', None)
            sex = params.get('sex', None)
            if sex:
                sex = u'M' if sex == 1 else u'Ж'
#            onlyMes = params.get('onlyMes', None)
            purposeId      = params.get('purposeId', None)
            eventTypeId    = params.get('eventTypeId', None)
            eventProfileId = params.get('eventProfileId', None)
            mesId          = params.get('mesId', None)
            self.writeElement('QuerySettings')
            if dateFrom:
                self.writeElement('dateFrom', forceString(dateFrom))
            if dateTo:
                self.writeElement('dateTo', forceString(dateTo))
            self.writeElement('personSpecialityCodeType', self.cmbPersonSpecialityCode.currentText())
            if ageBegin is not None:
                self.writeElement('ageBegin', str(ageBegin))
            if ageEnd is not None:
                self.writeElement('ageEnd', str(ageEnd))
            if sex:
                self.writeElement('sex', sex)
            if purposeId:
                self.writeElement('purpose', forceString(QtGui.qApp.db.translate('rbEventTypePurpose', 'id', purposeId, 'name')))
            if eventTypeId:
                self.writeElement('eventType', getEventName(eventTypeId))
            if eventProfileId:
                self.writeElement('eventProfile', forceString(QtGui.qApp.db.translate('rbEventProfile', 'id', eventProfileId, 'name')))
            if mesId:
                self.writeElement('mes', forceString(QtGui.qApp.db.translate('mes.MES', 'id', mesId, 'name')))
            self.endElement()
            self.endElement()


    @pyqtSignature('')
    def on_btnOpenFilePath_clicked(self):
        filePath = QtGui.QFileDialog.getSaveFileName(
            self, u'Укажите каталог и название файла', self.edtFilePath.text(), u'Файлы XML (*.xml)')
        if filePath:
            self.edtFilePath.setText(QDir.toNativeSeparators(filePath))


    @pyqtSignature('')
    def on_btnStart_clicked(self):
        if not forceStringEx(self.edtFilePath.text()):
            QtGui.QMessageBox.critical(self,
                                   u'Внимание!',
                                   u'Укажите каталог и название файла!',
                                   QtGui.QMessageBox.Close)
            return

        params = {}
        params['dateFrom'] = self.edtDateFrom.date()
        params['dateTo']   = self.edtDateTo.date()
        params['specialityCodeFieldName'] = 'code' # forceString(self.cmbPersonSpecialityCode.itemData(self.cmbPersonSpecialityCode.currentIndex()))
        params['onlyMes'] = self.chkOnlyMes.isChecked()
        params['exportClientData'] = self.chkExportClientData.isChecked()
        params['exportActions'] = self.chkExportActions.isChecked()
        params['onlyNomenclativeActions'] = self.chkOnlyNomenclativeActions.isChecked()
        params['onlyEndDiagnostic'] = self.chkOnlyEndDiagnostic.isChecked()
        params['exportActionExecPerson'] = self.chkActionExecPerson.isChecked()
        params['exportVisits'] = self.chkExportVisits.isChecked()
        params['exportTempInvalid'] = self.chkExportTempInvalid.isChecked()
        params['detailAddress'] = self.chkAddressDetail.isChecked()
        params['detailPolicy'] = self.chkPolicyDetail.isChecked()
        params['detailDocument'] = self.chkDocumentDetail.isChecked()
        if self.chkExportTempInvalid.isChecked():
            params['exportOnlyClosedTempInvalid'] = self.chkExportOnlyExecutedTempInvalid.isChecked()
        if params['onlyMes']:
            params['purposeId'] = self.cmbEventPurpose.value()
            params['eventTypeId'] = self.cmbEventType.value()
            params['eventProfileId'] = self.cmbEventProfile.value()
            params['mesId'] = self.cmbMes.value()
        params['isPolicy'] = self.chkInsurer.isChecked()
        if params['isPolicy']:
            params['insurerId'] = self.cmbInsurer.value()
            policyType = self.cmbPolicyType.currentIndex()
            if policyType:
                params['policyType'] = self.cmbPolicyType.currentText()
            else:
                params['policyType'] = None
        if self.chkSpeciality.isChecked():
            params['specialityId'] = self.cmbSpeciality.value()
        if self.chkDoctor.isChecked():
            params['doctorPersonId'] = self.cmbDoctor.value()
        if self.chkAge.isChecked():
            params['ageBegin'] = self.edtAgeBegin.value()
            params['ageEnd'] = self.edtAgeEnd.value()
        if self.chkSex.isChecked():
            params['sex'] = self.cmbSex.currentIndex()
        params['makeRar'] = self.chkMakeRar.isChecked()
        if self.chkSendEmail.isChecked():
            email = self.edtSendEmail.text()
            if checkEmail(email):
                params['e-mail'] = self.edtSendEmail.text()
            else:
                QtGui.QMessageBox.critical(self,
                                   u'Внимание!',
                                   u'Указан не корректный адрес электронной почты!',
                                   QtGui.QMessageBox.Close)
                return
        self.makeQuery(params)


    @pyqtSignature('int')
    def on_cmbSpeciality_currentIndexChanged(self, index):
        specialityId = self.cmbSpeciality.value()
        self.cmbDoctor.setSpecialityId(specialityId)


    @pyqtSignature('')
    def on_btnClose_clicked(self):
        if self.checkRun:
            self.abort = True
            self.btnClose.setText(u'Закрыть')
        else:
            self.close()


    @pyqtSignature('int')
    def on_cmbEventProfile_currentIndexChanged(self, index):
        self.cmbMes.setEventProfile(self.cmbEventProfile.value())
