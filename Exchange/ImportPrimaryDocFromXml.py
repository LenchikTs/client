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

import os
from zipfile import ZipFile

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QFile

from library.Utils import forceBool, forceDate, forceRef, forceString, forceStringEx, toVariant

from Exchange.Cimport import CXMLimport
from ExportPrimaryDocInXml import ( eventFields,
                                    clientFields,
#                                    mesSpecificationFields,
                                    eventTypeFields,
#                                    mesFields,
                                    specialityFields,
                                    financeFields,
                                    personFields,
                                    identifierFields,
                                    visitFields,
                                    sceneFields,
                                    visitTypeFields,
                                    serviceFields,
                                    characterFields,
                                    diagnosisTypeFields,
                                    diagnosticFields,
                                    eventDateFields,
                                    actionTypeFields,
                                    actionFields,
                                    diagnosticDateFields,
                                    actionDateFields,
                                    visitDateFields,
                                    eventGroup,
                                    actionGroup,
                                    diagnosticGroup,
                                    visitGroup,
                                  )

from Exchange.Utils import tbl

from Exchange.Ui_ImportPrimaryDocFromXml import Ui_Dialog


organisationFields = ('shortName', 'infisCode', 'INN', 'OGRN', 'miacCode')
querySettingsFields = ('dateFrom', 'dateTo', 'personSpecialityCodeType',
    'ageBegin', 'ageEnd', 'sex', 'purpose', 'eventType', 'eventProfile', 'mes')
exportFields = ('MIS', 'revision')

actionRefFields = ('finance_id', 'actionType_id')
diagnosticRefFields = ('person_id', 'character_id', 'diagnosisType_id', 'speciality_id')
visitRefFields = ('person_id', 'scene_id', 'finance_id', 'service_id', 'visitType_id')

documentFields = ('formated', )
policyFields = ('formated', )
regAddressFields = ('formated', )
locAddressFields = ('formated', )

eventRefFields = ('client_id', 'org_id')
actionRefFields = ()

clientGroup = {
    'document': {'fields':documentFields},
    'policy': {'fields':policyFields},
    'regAddress': {'fields':regAddressFields},
    'locAddress': {'fields':locAddressFields},
    'identifier': {'fields':identifierFields}
}

eventExGroup = {
    'Client': {'fields':clientFields, 'subGroup': clientGroup},
    'Action': {'fields':actionFields, 'subGroup': actionGroup},
    'visit': {'fields':visitFields, 'subGroup': visitGroup},
    'diagnostic': {'fields':diagnosticFields, 'subGroup': diagnosticGroup},
}

headerGroup = {
    'Organisation': {'fields': organisationFields},
    'QuerySettings': {'fields': querySettingsFields},
}

exportGroup = {
    'Header' : {'subGroup': headerGroup},
    'event' : {'fields': eventFields,  'subGroup': eventGroup}
}

eventKeyFields = ('org_id', 'client_id', 'setDate', 'execDate', 'eventType_id')

def ImportPrimaryDocFromXml(parent):
    isFullLog = forceBool(QtGui.qApp.preferences.appPrefs.get(
            'ImportPrimaryDocFromXmlFullLog', 'False'))
    fileName = forceString(QtGui.qApp.preferences.appPrefs.get(
            'ImportPrimaryDocFromXmlFileName', ''))
    checkLastDiagnosticOnly = forceString(QtGui.qApp.preferences.appPrefs.get(
            'ImportPrimaryDocFromXmlCheckLastDiagnosticOnly', True))

    dlg = CImportDialog(fileName, isFullLog, checkLastDiagnosticOnly, parent)
    dlg.exec_()

    QtGui.qApp.preferences.appPrefs['ImportPrimaryDocFromXmlFileName'] \
        = toVariant(dlg.edtFileName.text())
    QtGui.qApp.preferences.appPrefs['ImportPrimaryDocFromXmlFullLog'] \
        = toVariant(dlg.isFullLog)
    QtGui.qApp.preferences.appPrefs['ImportPrimaryDocFromXmlCheckLastDiagnosticOnly'] \
        =toVariant(dlg.checkLastDiagnosticOnly)


class CImportDialog(QtGui.QDialog, Ui_Dialog, CXMLimport):
    def __init__(self,  fileName, isFullLog, checkLastDiagnosticOnly,  parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        CXMLimport.__init__(self, self.log, self.edtFileName)
        self._parent = parent
        self.edtFileName.setText(fileName)
        self.isFullLog = isFullLog
        self.tmpDir = ''
        self.checkLastDiagnosticOnly = checkLastDiagnosticOnly

        self.nProcessed = 0
        self.nAdded = 0
        self.nUpdated = 0
        self.nSkipped = 0

        self.db = QtGui.qApp.db
        self.tableEvent = tbl('Event')
        self.tableOrganisation = tbl('Organisation')
        self.tableEventType = tbl('EventType')
        self.tableFinance = tbl('rbFinance')
        self.tableAction = tbl('Action')
        self.tableVisit = tbl('Visit')
        self.tableDiagnostic = tbl('Diagnostic')
        self.tableActionType = tbl('ActionType')
        self.tableDiagnosisType = tbl('rbDiagnosisType')
        self.tablePerson = tbl('vrbPerson')
        self.tableCharacter = tbl('rbDiseaseCharacter')
        self.tableScene = tbl('rbScene')
        self.tableService = tbl('rbService')
        self.tableResult = tbl('rbResult')
        self.tableVisitType = tbl('rbVisitType')
        self.tableSpeciality = tbl('rbSpeciality')

        self.finalDiagnosisTypeIdList = self.db.getIdList(self.tableDiagnosisType,
                                                   where=self.tableDiagnosisType['code'].inlist(['1', '2', '7']))

        self.findFinanceId = lambda finance: self.findId(finance,
                                                         self.tableFinance, financeFields)
        self.findEventTypeId = lambda eventType: self.findId(eventType,
                                                             self.tableEventType, eventTypeFields)
        self.findEvent = lambda event: self.findRecord(event, self.tableEvent,
                                                       eventKeyFields)
        self.findClientId = lambda client: self.findId(client, self.tableClient,
                                                       clientFields)
        self.findOrgId = lambda org: self.findId(org, self.tableOrganisation,
                                                 organisationFields)
        self.findActionTypeId = lambda actionType: self.findId(actionType,
                                                        self.tableActionType, actionTypeFields)
        self.findDiagnosisTypeId = lambda diagnosisType: self.findId(diagnosisType,
                                                        self.tableDiagnosisType, diagnosisTypeFields)
        self.findPersonId = lambda person: self.findId(person, self.tablePerson,
                                                       personFields)
        self.findCharacterId = lambda character: self.findId(character,
                                                             self.tableCharacter, characterFields)
        self.findSceneId = lambda scene: self.findId(scene, self.tableScene, sceneFields)
        self.findServiceId = lambda service: self.findId(service, self.tableService, serviceFields)
        self.findVisitTypeId = lambda visitType: self.findId(visitType, self.tableVisitType, visitTypeFields)
        self.findSpecialityId = lambda spec: self.findId(spec, self.tableSpeciality, specialityFields)

        self.isCoinsidentAction = lambda item, record: self.isCoinsidentRecord(
                                                                               item, record, actionFields, actionRefFields,
                                                                               actionDateFields)
        self.isCoinsidentDiagnostic = lambda item, record: self.isCoinsidentRecord(
                                                                                   item, record, diagnosticFields, diagnosticRefFields,
                                                                                   diagnosticDateFields)
        self.isCoinsidentVisit = lambda item, record: self.isCoinsidentRecord(
                                                                              item, record, visitFields, visitRefFields,
                                                                              visitDateFields)

        self.refFuncMap = {
            'finance_id': self.findFinanceId,
            'actionType_id': self.findActionTypeId,
            'character_id': self.findCharacterId,
            'person_id': self.findPersonId,
            'diagnosisType_id' : self.findDiagnosisTypeId,
            'scene_id': self.findSceneId,
            'service_id': self.findServiceId,
            'visitType_id' : self.findVisitTypeId,
            'speciality_id': self.findSpecialityId
        }



    def cleanup(self):
        if self.tmpDir:
            QtGui.qApp.removeTmpDir(self.tmpDir)
            self.tmpDir = ''


    def getTmpDir(self):
        if not self.tmpDir:
            self.tmpDir = QtGui.qApp.getTmpDir('ImportPrimaryDocFromXml')
        return self.tmpDir


    def startImport(self):
        fileName = forceStringEx(self.edtFileName.text())
        (name,  fileExt) = os.path.splitext(fileName)

        if  fileExt.lower() == '.zip':
            zf = ZipFile(fileName, 'r', allowZip64=True)
            zf.extract(zf.namelist()[0], self.getTmpDir())
            fileName = os.path.join(self.getTmpDir(), zf.namelist()[0])
            (name,  fileExt) = os.path.splitext(fileName)

        if fileExt.lower() != '.xml':
            self.log.append(u'распакованный файл `%s` должен быть в формате XML' % fileName)
            self.cleanup()
            return

        inFile = QFile(fileName)

        if not inFile.open(QFile.ReadOnly | QFile.Text):
            QtGui.QMessageBox.warning(self, u'Импорт данных из XML',
                                  u'Не могу открыть файл для чтения %s:\n%s.' \
                                  % (fileName, inFile.errorString()))
            self.cleanup()
            return

        self.progressBar.reset()
        self.progressBar.setValue(0)
        self.progressBar.setFormat(u'%v байт')
        self.stat.setText("")
        size = max(inFile.size(), 1)
        self.progressBar.setMaximum(size)
        self.labelNum.setText(u'размер источника: %d' % (size))
        self.btnImport.setEnabled(False)

        if (not self.readFile(inFile)):
            if self.abort:
                self.err2log(u'! Прервано пользователем.')
            else:
                self.err2log(u'! Ошибка: файл %s, %s' % (fileName,
                                            self.errorString()))

        self.cleanup()
        self.stat.setText(u'обработано: %d' % self.nProcessed)


    def readFile(self, device):
        self.setDevice(device)
        data = {}

        while (not self.atEnd()):
            self.readNext()

            if self.isStartElement():
                if self.name() == 'Export':
                    exportGroup['event']['subGroup'].update(eventExGroup)
                    data = self.readGroupEx('Export', exportFields, subGroupDict=exportGroup)
                else:
                    self.raiseError(u'Неверный формат экспорта данных.')

            if self.hasError() or self.abort:
                return False

        orgId = self.findOrgId(data.get('Header', {}).get('Organisation'))

        if not orgId:
            self.log.append(u'Организация не найдена %s. Импорт остановлен.' % self.dumpFields(data.get('Organisation'), organisationFields))
            return

        eventList = data.get('event', [])
        eventCount = len(eventList)

        self.log.append(u'Прочитано событий: %d' % eventCount)
        self.progressBar.reset()
        self.progressBar.setValue(0)
        self.progressBar.setFormat(u'%v событий')
        self.progressBar.setMaximum(eventCount)

        map(lambda event: self.processEvent(event, orgId), eventList)
        return True


    def processEvent(self, event, orgId):
        self.log.append(u'Event: execDate %s' % event.get('execDate', '-'))

        self.processEventRefs(event, orgId)

        if not event['client_id']:
            self.log.append(u'Пациент не найден %s' % self.dumpFields(event.get('Client'), clientFields))
            self.nSkipped += 1
            return

        if not event['org_id']:
            self.log.append(u'Организация не найдена %s' % self.dumpFields(event.get('Organisation'), organisationFields))
            self.nSkipped += 1
            return

        oldEventRecord = self.findEvent(event)

        if oldEventRecord :
            if self.isCoinsidentEvent(event, oldEventRecord):
                self.log.append(u'Найдено совпадающее событие, пропускаем')
                self.nSkipped += 1
            else:
                self.log.append(u'События различаются, обновляем')
                self.updateEvent(event, oldEventRecord)
                self.nUpdated += 1
        else:
            self.log.append(u'Добавляем новое событие')
            self.addEvent(event)
            self.nAdded += 1

        self.progressBar.step()
        QtGui.qApp.processEvents()


    def processEventRefs(self, event, orgId):
        u"""Обработка ссылочных полей события, поиск идентификаторов"""

        event['org_id'] = orgId
        event['client_id']= self.findClientId(event.get('Client'))
        event['eventType_id'] = self.findEventTypeId(event.get('eventType'))
        event['finance_id'] = self.findFinanceId(event.get('finance'))

        for (groupName,  refFields) in (
                    ('Action', actionRefFields),
                    ('diagnostic', diagnosticRefFields),
                    ('visit', visitRefFields),
                ):
            items = event.get(groupName, [])

            # если элемент только один, преобразуем его в список
            if not isinstance(items, list):
                items = [items, ]
                event[groupName] = items

            for item in items:
                for field in refFields:
                    if item.has_key(field[:-3]):
                        findRef = self.refFuncMap.get(field, self.unknowRefField)
                        item[field] = findRef(item[field[:-3]])
                    else:
                        item[field] = None


    def unknowRefField(self, items):
        self.log.append(u'Неизвестный элемент')


    def findId(self, data, table, fieldList, cache=None):
        record = self.findRecord(data, table, fieldList, cache)
        id = forceRef(record.value('id')) if record else None
        return id


    def findRecord(self, data, table, fieldList, cache=None):
        if not data or data == {}:
            return None

        result =cache.get(data) if cache else None

        if not result:
            cond = []

            for field in fieldList:
                val = data.get(field)
                if val:
                    cond.append(table[field].eq(val))

            result = self.db.getRecordEx(table, '*', cond)

            if cache:
                cache[data] = result

        return result


    def isCoinsidentEvent(self, event, oldEventRecord):
        if not oldEventRecord:
            return False

        # проверяем поля, не являющиеся ссылками
        for field in eventFields:
            if field in eventDateFields:
               if event.get(field) != forceString(forceDate(
                            oldEventRecord.value(field)).toString(Qt.ISODate)):
                    return False
            else:
                if event.get(field) != forceString(oldEventRecord.value(field)):
                    return False

        # проверяем поля, являющиеся ссылками
        for ref in eventRefFields:
            if event.get(ref) != forceRef(oldEventRecord.value(ref)):
                return False


        oldEventId = forceRef(oldEventRecord.value('id'))
        #проверяем действия, визиты, диагностики
        for (table, groupName, comparator) in (
                (self.tableAction, 'Action', self.isCoinsidentAction),
                (self.tableDiagnostic,  'diagnostic', self.isCoinsidentDiagnostic),
                (self.tableVisit, 'visit', self.isCoinsidentVisit)):

            cond = [table['event_id'].eq(oldEventId), table['deleted'].eq(0)]

            if groupName == 'diagnostic' and self.checkLastDiagnosticOnly:
                cond.append(table['diagnosisType_id'].inlist(self.finalDiagnosisTypeIdList))

            oldRecords =  self.db.getRecordList(table, where=cond)
            items = event.get(groupName, [])

            if len(oldRecords) != len(items):
                return False

            for item in items:
                for record in oldRecords:
                    if comparator(item, record):
                        break
                else: # for - else!
                    return False

        return True


    def isCoinsidentRecord(self, itemDict, record, fields, refFields, dateFields=tuple()):
        for field in fields:
            if field in dateFields:
                if itemDict.get(field, '') != forceString(forceDate(record.value(field)).toString(Qt.ISODate)):
                    return False
            else:
                if itemDict.get(field, '') != forceString(record.value(field)):
                    return False

        for field in refFields:
            if itemDict.get(field) != forceRef(record.value(field)):
                return False

        return True


    def updateRecord(self, table, itemDict, record, fields, refFields, dateFields=tuple()):
        isDirty = False
        result = None

        for field in fields:
            if field in dateFields:
                if itemDict.get(field, '') != forceString(forceDate(record.value(field)).toString(Qt.ISODate)):
                    record.setValue(field, toVariant(itemDict.get(field, '')))
                    isDirty = True
            else:
                if itemDict.get(field, '') != forceString(record.value(field)):
                    record.setValue(field, toVariant(itemDict.get(field, '')))
                    isDirty = True

        for field in refFields:
            if itemDict.get(field) != forceRef(record.value(field)):
                record.setValue(field, toVariant(itemDict.get(field, '')))
                isDirty = True

        if isDirty:
            result = self.db.updateRecord(table, record)

        return result


    def addRecord(self, table, itemDict, fields):
        record = table.newRecord()

        for x in fields:
            if itemDict.has_key(x):
                record.setValue(x, toVariant(itemDict[x]))

        return self.db.insertRecord(table, record)


    def updateEvent(self, event, oldEventRecord):
        self.updateRecord(self.tableEvent, event, oldEventRecord,
                          eventFields, eventRefFields, eventDateFields)

        eventId = forceRef(oldEventRecord.value('id'))

        for (table, groupName, fields, refFields, dateFields, comparator) in (
                (self.tableAction, 'Action', actionFields, actionRefFields, actionDateFields, self.isCoinsidentAction),
                (self.tableDiagnostic,  'diagnostic', diagnosticFields, diagnosticRefFields, diagnosticDateFields, self.isCoinsidentDiagnostic),
                (self.tableVisit, 'visit', visitFields, visitRefFields, visitDateFields, self.isCoinsidentEvent)):

            items = event.get(groupName, [])
            cond = [table['event_id'].eq(eventId), table['deleted'].eq(0)]

            if groupName == 'diagnostic' and self.checkLastDiagnosticOnly:
                cond.append(table['diagnosisType_id'].inlist(self.finalDiagnosisTypeIdList))

            oldRecords =  self.db.getRecordList(table, where=cond)

            for item in items:
                for record in oldRecords:
                    if comparator(item, record):
                        break
                else: # нет совпадений - добавляем
                    item['event_id']= eventId
                    self.addRecord(table, item, fields + refFields+('event_id',  ))

            # получаем новый список записей
            oldRecords =  self.db.getRecordList(table, where=cond)

            # удаляем отсутствующие записи
            for record in oldRecords:
                for item in items:
                    if comparator(item, record):
                        break
                else: # нет совпадений - удаляем
                    record.setValue('deleted', toVariant(5))
                    self.db.updateRecord(table, record)



    def addEvent(self, event):
        eventId = self.addRecord(self.tableEvent, event, eventFields + eventRefFields)

        if not eventId:
            return False

        for (table, groupName, fields) in (
                (self.tableAction, 'Action', actionFields+actionRefFields),
                (self.tableDiagnostic,  'diagnostic', diagnosticFields+diagnosticRefFields),
                (self.tableVisit, 'visit', visitFields+visitRefFields)):

            items = event.get(groupName, [])

            for item in items:
                item['event_id'] = eventId

                if not self.addRecord(table, item, fields+('event_id',  )):
                    return False

        return True


    def dumpFields(self, fDict, fields):
        return ' '.join(u'%s=`%s`' % (f,  fDict.get(f, '-')) for f in fields) if fDict else '-'
