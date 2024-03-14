# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2018 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDir, QFile, QXmlStreamReader, pyqtSignature, SIGNAL

from library.Utils import anyToUnicode, exceptionToUnicode, forceBool, forceInt, forceRef, forceString, toVariant

from Exchange.ExportEvents import  checkPropertyList,  eventTypeFields, exportFormatVersion,  medicalAidTypeFields, eventProfileFields,  serviceFields,  sceneFields,  medicalAidKindFields,  counterFields, eventTypePurposeFields
from Exchange.Utils import tbl

from Exchange.Ui_ImportEvents_Wizard_1 import Ui_ImportEvents_Wizard_1
from Exchange.Ui_ImportEvents_Wizard_2 import Ui_ImportEvents_Wizard_2
from Exchange.Ui_ImportEvents_Wizard_3 import Ui_ImportEvents_Wizard_3


eventTypeRefFields = ('id',  'finance_id', 'scene_id', 'service_id',
    'purpose_id',  'medicalAidType_id', 'medicalAidKind_id',
    'eventProfile_id',  'counter_id')

# имена известных полей в таблицы (без внешних ключей)
eventTypeActionFieldNames = ('idx',  'sex',  'age',  'selectionGroup',  \
    'actuality',  'expose')
# имена известных внешних ключей
eventTypeActionRefFieldNames = ('eventType_id',  'actionType_id',  \
    'speciality_id')


eventTypeDiagnosticFieldNames = ('idx',  'sex',  'age',  'defaultMKB',  \
    'selectionGroup', 'actuality')
eventTypeDiagnosticRefFieldNames = ('eventType_id', 'speciality_id',  \
    'defaultHealthGroup_id', 'defaultDispanser_id', 'visitType_id')


eventTypeFormFieldNames = ('code',  'name',  'descr',  'pass')
eventTypeFormRefFieldNames = ('eventType_id', )

def ImportEventType():
    dlg = CImportEventType(forceString(QtGui.qApp.preferences.appPrefs.get('ImportEventTypeFileName', '')),
        fullLog = forceBool(QtGui.qApp.preferences.appPrefs.get('ImportEventFullLog', 'False')),
        importAll = forceBool(QtGui.qApp.preferences.appPrefs.get('ImportEventImportAll', 'False')))
    dlg.exec_()
    QtGui.qApp.preferences.appPrefs['ImportEventTypeFileName'] = toVariant(dlg.fileName)
    QtGui.qApp.preferences.appPrefs['ImportEventFullLog'] = toVariant(dlg.fullLog)
    QtGui.qApp.preferences.appPrefs['ImportEventImportAll'] = toVariant(dlg.importAll)


class CMyXmlStreamReader(QXmlStreamReader):
    def __init__(self,  parent,  showLog = False):
        QXmlStreamReader.__init__(self)
        self.parent = parent
        self.db=QtGui.qApp.db

        self.tableEventType = tbl('EventType')
        self.tableEventTypeAction = tbl('EventType_Action')
        self.tableEventTypeDiagnostic = tbl('EventType_Diagnostic')
        self.tableEventTypeForm  = tbl('EventTypeForm')
        self.tableService = tbl('rbService')
        self.tablePurpose = tbl('rbEventTypePurpose')
        self.tableFinance = tbl('rbFinance')
        self.tableVisitType = tbl('rbVisitType')
        self.tableHealthGroup = tbl('rbHealthGroup')
        self.tableActionType = tbl('ActionType')
        self.tableSpeciality = tbl('rbSpeciality')
        self.tableMedicalAidType = tbl('rbMedicalAidType')
        self.tableEventProfile = tbl('rbEventProfile')
        self.tableDispanser = tbl('rbDispanser')
        self.tableScene = tbl('rbScene')
        self.tableCounter = tbl('rbCounter')
        self.tableMedicalAidKind = tbl('rbMedicalAidKind')

        self.nadded = 0
        self.ncoincident = 0
        self.nprocessed = 0
        self.nupdated = 0

        self.mapServiceKeyToId = {}
        self.mapEventTypeKeyToId = {}
        self.mapFinanceKeyToId = {}
        self.mapPurposeKeyToId = {}
        self.mapVisitTypeKeyToId = {}
        self.mapHealthGroupKeyToId = {}
        self.mapActionTypeKeyToId = {}
        self.mapSpecialityKeyToId = {}
        self.mapMedicalAidTypeKeyToId = {}
        self.mapEventProfileKeyToId = {}
        self.mapDispanserKeyToId = {}
        self.mapMedicalAidKindKeyToId = {}
        self.mapSceneKeyToId = {}
        self.mapCounterKeyToId = {}

        self.showLog = showLog
        self.eventsList = []
        # список полей , которые есть в бд для таблиц
        self.eventTypeFieldNamesExist =  checkPropertyList('EventType', \
                                                        eventTypeFields + eventTypeRefFields)
        self.eventTypeFieldNamesNoRefsExist =  checkPropertyList('EventType', \
                                                        eventTypeFields)
        self.eventTypeActionFieldNamesExist = checkPropertyList('EventType_Action', \
                                                        eventTypeActionFieldNames)
        self.eventTypeActionRefFieldNamesExist = checkPropertyList('EventType_Action',  \
                                                        eventTypeActionRefFieldNames)
        self.eventTypeDiagnosticFieldNamesExist = checkPropertyList('EventType_Diagnostic', \
                                                        eventTypeDiagnosticFieldNames)
        self.eventTypeDiagnosticRefFieldNamesExist = checkPropertyList('EventType_Diagnostic', \
                                                        eventTypeDiagnosticRefFieldNames)
        self.eventTypeFormFieldNamesExist = checkPropertyList('EventTypeForm', \
                                                        eventTypeFormFieldNames)
        self.eventTypeFormRefFieldNamesExist = checkPropertyList('EventTypeForm', \
                                                        eventTypeFormRefFieldNames)

    def raiseError(self,  str):
        QXmlStreamReader.raiseError(self, u'[%d:%d] %s' % (self.lineNumber(), self.columnNumber(), str))


    def readNext(self):
        QXmlStreamReader.readNext(self)
        self.parent.progressBar.setValue(self.device().pos())

    def getEventPropertyParams(self, eventProperty):
        if eventProperty['type'] == 'action':
            fieldList = self.eventTypeActionFieldNamesExist
            refFields = self.eventTypeActionRefFieldNamesExist
            table = self.tableEventTypeAction
        elif eventProperty['type'] == 'diagnostic':
            fieldList = self.eventTypeDiagnosticFieldNamesExist
            refFields = self.eventTypeDiagnosticRefFieldNamesExist
            table = self.tableEventTypeDiagnostic
        elif eventProperty['type'] == 'form':
            fieldList = self.eventTypeFormFieldNamesExist
            refFields = self.eventTypeFormRefFieldNamesExist
            table = self.tableEventTypeForm
        else:
            self.raiseError(u'! Неизвестный тип свойства события: "%s"'\
                      % eventProperty['type'])
            return None

        return (table,  fieldList,  refFields)


    def log(self, str,  forceLog = False):
        if self.showLog or forceLog:
            self.parent.logBrowser.append(str)
            self.parent.logBrowser.update()


    def readFile(self, device,  selectedItems=None,  makeEventsList=False):
        u""" Разбирает и загружает xml из указанного устройства device
            если makeEventsList == True - составляет список найденных
            в событий для загрузки"""
        self.setDevice(device)
        xmlVersion = '1.00'

        try:
            while (not self.atEnd()):
                self.readNext()

                if self.isStartElement():
                    if self.name() == 'EventTypeExport':
                        if self.attributes().value('version') == exportFormatVersion:
                            self.readData(selectedItems, makeEventsList)
                        else:
                            self.raiseError(u'Версия формата "%s" не поддерживается. Должна быть "%s"' \
                                % (self.attributes().value('version').toString(), xmlVersion))
                    else:
                        self.raiseError(u'Неверный формат экспорта данных.')

                if self.hasError() or self.parent.aborted:
                    return False

        except IOError, e:
            QtGui.qApp.logCurrentException()
            msg=''
            if hasattr(e, 'filename'):
                msg = u'%s:\n[Errno %s] %s' % (e.filename, e.errno, anyToUnicode(e.strerror))
            else:
                msg = u'[Errno %s] %s' % (e.errno, anyToUnicode(e.strerror))
            QtGui.QMessageBox.critical (self.parent,
                u'Произошла ошибка ввода-вывода', msg, QtGui.QMessageBox.Close)
            self.log(u'! Ошибка ввода-вывода: %s' % msg,  True)
            return False
        except Exception, e:
            QtGui.qApp.logCurrentException()
            QtGui.QMessageBox.critical (self.parent,
                u'Произошла ошибка', exceptionToUnicode(e), QtGui.QMessageBox.Close)
            self.log(u'! Ошибка: %s' % exceptionToUnicode(e),  True)
            return False


        return not self.hasError()


    def readData(self,  selectedItems,  makeEventsList):
        assert self.isStartElement() and self.name() == 'EventTypeExport'

        # очищаем список событий перед заполнением
        if makeEventsList:
            self.eventsList = []

        while (not self.atEnd()):
            self.readNext()

            if self.isEndElement():
                break

            if self.isStartElement():
                if (self.name() == 'EventType'):
                    self.readEventType(selectedItems,  makeEventsList)
                else:
                    self.readUnknownElement()

            if self.hasError() or self.parent.aborted:
                break


    def readEventType(self,  selectedItems,  makeEventsList):
        assert self.isStartElement() and self.name() == 'EventType'

        eventProperties = []
        eventType = {}
        service = None
        finance = None
        purpose = None
        eventProfile = None
        medicalAidType = None
        medicalAidKind = None
        scene = None
        counter = None
        skipItem = False

        if self.parent.aborted:
            return None

        if makeEventsList:
            self.eventsList.append((forceString(self.attributes().value('code').toString()), \
                                            forceString(self.attributes().value('name').toString())))
            self.log(u' Найден тип события: (%s) "%s"' % self.eventsList[-1])
        else:
            for x in self.eventTypeFieldNamesNoRefsExist:
                eventType[x] = forceString(self.attributes().value(x).toString())

            name = eventType['name']
            code = eventType['code']
            if selectedItems:
                skipItem = (code,  name) not in selectedItems

            if not skipItem:
                self.log(u'Тип события: %s (%s)' %(name, code))

        while not self.atEnd():
            QtGui.qApp.processEvents()
            self.readNext()

            if self.isEndElement():
                break

            if self.isStartElement():
                if not (makeEventsList or skipItem):
                    if (self.name() == 'Action'):
                        eventProperties.append(self.readEventTypeAction())
                    elif (self.name() == 'Diagnostic'):
                        eventProperties.append(self.readEventTypeDiagnostic())
                    elif (self.name() == 'Form'):
                        eventProperties.append(self.readEventTypeForm())
                    elif (self.name() == 'service'):
                        service = self.readService()
                        eventType['service_id'] = service['id']
                    elif (self.name() == 'purpose'):
                        purpose = self.readPurpose()
                        eventType['purpose_id'] = purpose['id']
                    elif (self.name() == 'finance'):
                        finance = self.readFinance()
                        eventType['finance_id'] = finance['id']
                    elif (self.name() == 'medicalAidType'):
                        medicalAidType = self.readMedicalAidType()
                        eventType['medicalAidType_id'] = medicalAidType['id']
                    elif (self.name() == 'eventProfile'):
                        eventProfile = self.readEventProfile()
                        eventType['eventProfile_id'] = eventProfile['id']
                    elif self.name() == 'scene':
                        scene = self.readScene()
                        eventType['scene_id'] = scene['id']
                    elif self.name() == 'medicalAidKind':
                        medicalAidKind = self.readMedicalAidKind()
                        eventType['medicalAidKind_id'] = medicalAidKind['id']
                    elif self.name() == 'counter':
                        counter = self.readCounter()
                        eventType['counter_id'] = counter['id']
                    else:
                        self.readUnknownElement()
                else:
                    # молча пропускаем все элементы, т.к мы только
                    # создаем список событий
                    self.readUnknownElement(False)

        if makeEventsList or skipItem:
            return None

        id = self.lookupEventType(eventType)

        if self.hasError() or self.parent.aborted:
            return None

        if id:
            self.log(u'%% Найдена похожая запись (id=%d)' % id)
            # такое действие уже есть. надо проверить все его свойства
            if not self.parent.parent.page(0).rbSkip.isChecked():
                if not self.isCoincidentEventType(eventType,  id):
                    # есть разхождения в полях. спрашиваем у пользователя что делать
                    self.log(u' поля различаются')
                    if self.parent.parent.page(0).rbAskUser.isChecked():
                        self.log(u' Запрос действия пользователя: ')
                        if QtGui.QMessageBox.question(self.parent, u'Записи различаются',
                                                    self.prepareMessageBoxText(eventType, id) ,
                                                    QtGui.QMessageBox.No|QtGui.QMessageBox.Yes,
                                                    QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes:
                            self.log(u' - обновляем')
                            self.updateEventType(eventType, id, service, finance,
                                                 scene, purpose, medicalAidType,
                                                 medicalAidKind, eventProfile,
                                                 counter)
                        else:
                            self.log(u' - пропускаем')
                    elif self.parent.parent.page(0).rbUpdate.isChecked():
                        self.log(u' - обновляем')
                        self.updateEventType(eventType, id, service, finance,
                                                 scene, purpose, medicalAidType,
                                                 medicalAidKind, eventProfile,
                                                 counter)
                #  проверим свойства действия
                for x in eventProperties:
                    self.log(u'  Свойство: %s' %(x['type']))

                    if self.parent.aborted:
                        return

                    # если нет 100% совпадения, ищем похожие свойства
                    if not self.isCoincidentEventTypeProperty(x, id):
                        if self.parent.parent.page(0).rbAskUser.isChecked():
                            self.log(u' Запрос действия пользователя: ')
                            if QtGui.QMessageBox.question(self.parent, u'Записи различаются',
                                                        self.prepareEventPropertyMessageBoxText(x) ,
                                                        QtGui.QMessageBox.No|QtGui.QMessageBox.Yes,
                                                        QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes:
                                self.log(u'  + выбор пользователя: добавляем')
                                self.addEventProperty(x,  id)
                            else:
                                self.log(u'  + выбор пользователя: пропускаем')
                        if self.parent.parent.page(0).rbUpdate.isChecked():
                            self.log(u'  + выбор пользователя: добавляем')
                            self.addEventProperty(x,  id)
                        else:
                            self.log(u'  + выбор пользователя: пропускаем')
                    else: # похожих нет, добавляем
                        self.log(u'  : есть в базе данных, пропускаем ')

            else:
                self.log(u' - пропускаем')


            self.ncoincident += 1
        else:
            self.log(u'% Сходные записи не обнаружены. Добавляем')
            # новая запись, добавляем само действие и все его свойства
            record = self.tableEventType.newRecord()

            for x in self.eventTypeFieldNamesExist:
                if eventType.has_key(x) and eventType[x]:
                    record.setValue(x,  toVariant(eventType[x]))

            if service: # если есть услуга по еис, запишем ее
                sId = self.processService(service)
                record.setValue('service_id', toVariant(sId))

            if finance:
                fId = self.processFinance(finance)
                record.setValue('finance_id',  toVariant(fId))

            if purpose:
                pId = self.processPurpose(purpose)
                record.setValue('purpose_id',  toVariant(pId))

            if medicalAidType:
                mId = self.processMedicalAidType(medicalAidType)
                record.setValue('medicalAidType_id',  toVariant(mId))

            if eventProfile:
                epId = self.processEventProfile(eventProfile)
                record.setValue('eventProfile_id',  toVariant(epId))

            if medicalAidKind:
                mKindId = self.processMedicalAidKind(medicalAidKind)
                record.setValue('medicalAidKind_id', toVariant(mKindId))

            if counter:
                counterId = self.processCounter(counter)
                record.setValue('counter_id', toVariant(counterId))

            if scene:
                sceneId = self.processScene(scene)
                record.setValue('scene_id',  toVariant(sceneId))

            id = self.db.insertRecord(self.tableEventType, record)

            # поскольку тип события - новый, то просто добавим все его свойства
            if eventProperties != []:
                for p in eventProperties:
                    self.addEventProperty(p,  id)

            self.nadded += 1

        self.nprocessed += 1
        self.parent.statusLabel.setText(
                u'импорт типов событий: %d добавлено; %d обновлено; %d совпадений; %d обработано' % (self.nadded,
                                                                                                      self.nupdated,  self.ncoincident,  self.nprocessed))

        return id


    def readElement(self, name, fieldNameList,  lookupProc, logMessage = None):
        '''Чтение произвольного элемента
                name - имя элемента
                fieldNameList -  список имен полей для чтения
                lookupProc - функция поиска элемента в БД, возвращающая идентификатор
                logMessage - сообщение в журнал загрузки'''

        assert self.isStartElement() and self.name() == name
        result = {}

        for fieldName in fieldNameList:
            result[fieldName] = forceString(self.attributes().value(fieldName).toString())

        if lookupProc:
            result['id'] = lookupProc(result)

        if logMessage and result.has_key('name') and result.has_key('code'):
            self.log(logMessage %(result['name'],  result['code']))

        while not self.atEnd():
            self.readNext()

            if self.isEndElement():
                break

            if self.isStartElement():
                self.readUnknownElement()

            if self.hasError() or self.parent.aborted:
               break

        return result


    def readScene(self):
        return self.readElement('scene', sceneFields, self.lookupScene,
                                                    u'Место: %s, код %s')


    def readMedicalAidKind(self):
        return self.readElement('medicalAidKind', medicalAidKindFields,
                                self.lookupMedicalAidKind,
                                u'Вид мед.помощи: %s, код %s')


    def readCounter(self):
        return self.readElement('counter',  counterFields,
                                self.lookupCounter,
                                u'Счетчик: %s, код %s')


    def readActionType(self):
        return self.readElement('ActionType',  ('code',  'name'),
                                self.lookupActionType)


    def readService(self):
        return self.readElement('service', serviceFields,
                                self.lookupService,
                                u'Услуга ЕИС: %s, код %s')


    def readPurpose(self):
        return self.readElement('purpose', eventTypePurposeFields,
                                self.lookupPurpose,
                                u'Назначение: %s, код %s')


    def readSpeciality(self):
        return self.readElement('speciality', ('code',  'name'),
                                self.lookupSpeciality)


    def readFinance(self):
        return self.readElement('finance', ('code',  'name'),
                                self.lookupFinance,
                                u'Финансирование: %s, код %s')


    def readHealthGroup(self):
        return self.readElement('defaultHealthGroup', ('code',  'name'),
                                self.lookupHealthGroup)


    def readDispanser(self):
        return self.readElement('defaultDispanser', ('code',  'name'),
                                self.lookupDispanser)


    def readVisitType(self):
        return self.readElement('visitType', ('code',  'name'),
                                self.lookupVisitType)


    def readMedicalAidType(self):
        return self.readElement('medicalAidType', medicalAidTypeFields,
                                self.lookupMedicalAidType,
                                u'Тип мед. помощи: %s, код %s')


    def readEventProfile(self):
        return self.readElement('eventProfile', eventProfileFields,
                                self.lookupEventProfile,
                                u'Профиль события: %s, код %s')


    def readEventTypeAction(self):
        assert self.isStartElement() and self.name() == 'Action'
        action = {}
        action['type'] = 'action'

        for fieldName in self.eventTypeActionFieldNamesExist:
            action[fieldName] = forceString(self.attributes().value(fieldName).toString())

        while not self.atEnd():
            self.readNext()

            if self.isEndElement():
                break

            if self.isStartElement():
                if (self.name() == 'ActionType'):
                    action['action_type'] = self.readActionType()
                    action['actionType_id'] = action['action_type']['id']
                elif (self.name() == 'speciality'):
                    action['speciality'] = self.readSpeciality()
                    action['speciality_id'] = action['speciality']['id']
                else:
                    self.readUnknownElement()

            if self.hasError() or self.parent.aborted:
               break

        return action


    def readEventTypeDiagnostic(self):
        assert self.isStartElement() and self.name() == 'Diagnostic'
        diagnostic = {}
        diagnostic['type'] = 'diagnostic'

        for fieldName in self.eventTypeDiagnosticFieldNamesExist:
            diagnostic[fieldName] = forceString(self.attributes().value(fieldName).toString())

        while not self.atEnd():
            self.readNext()

            if self.isEndElement():
                break

            if self.isStartElement():
                if (self.name() == 'defaultHealthGroup'):
                    diagnostic['defaultHealthGroup'] = self.readHealthGroup()
                    diagnostic['defaultHealthGroup_id'] = \
                        diagnostic['defaultHealthGroup']['id']
                elif (self.name() == 'defaultDispanser'):
                    diagnostic['defaultDispanser'] = self.readDispanser()
                    diagnostic['defaultDispanser_id'] = \
                        diagnostic['defaultDispanser']['id']
                elif (self.name() == 'visitType'):
                    diagnostic['visitType'] = self.readVisitType()
                    diagnostic['visitType_id'] = diagnostic['visitType']['id']
                elif (self.name() == 'speciality'):
                    diagnostic['speciality'] = self.readSpeciality()
                    diagnostic['speciality_id'] = diagnostic['speciality']['id']
                else:
                    self.readUnknownElement()

            if self.hasError() or self.parent.aborted:
               break

        return diagnostic


    def readEventTypeForm(self):
        assert self.isStartElement() and self.name() == 'Form'
        form = {}
        form['type'] = 'form'

        for fieldName in self.eventTypeFormFieldNamesExist:
            form[fieldName] = forceString(self.attributes().value(fieldName).toString())

        while not self.atEnd():
            self.readNext()

            if self.isEndElement():
                break

            if self.isStartElement():
                self.readUnknownElement()

            if self.hasError() or self.parent.aborted:
               break

        return form


    def readUnknownElement(self, report = True):
        ''' Читает неизвестный элемент, и сообщает об этом,
            если report ==True '''

        assert self.isStartElement()

        if report:
            self.log(u'Неизвестный элемент: '+self.name().toString())

        while (not self.atEnd()):
            self.readNext()

            if (self.isEndElement()):
                break

            if (self.isStartElement()):
                self.readUnknownElement(report)

            if self.hasError() or self.parent.aborted:
                break


    def lookupAnythingByNameAndCode(self, name,  code,  cache,  table):
        key = (code, name)
        id = cache.get(key,  None)

        if not id:
            cond = []
            cond.append(table['code'].eq(toVariant(code)))
            cond.append(table['name'].eq(toVariant(name)))

            if table.hasField('deleted'):
                cond.append(table['deleted'].eq(0))

            record = self.db.getRecordEx(table, ['id'], where=cond)

            if record:
                id = forceRef(record.value('id'))
                cache[key] = id

        return id


    def lookupActionType(self, fields):
        return self.lookupAnythingByNameAndCode(fields.get('name', ''),
                                fields.get('code',  ''),
                                self.mapActionTypeKeyToId,
                                self.tableActionType)


    def lookupEventType(self, fields):
        ''' Поиск похожего типа события по имени и коду'''
        return self.lookupAnythingByNameAndCode(fields.get('name', ''),
                                fields.get('code',  ''),
                                self.mapEventTypeKeyToId,
                                self.tableEventType)


    def lookupService(self, fields):
        '''Для идентификации услуг (профиль ЕИС) используем имя и код'''
        return self.lookupAnythingByNameAndCode(fields.get('name', ''),
                                fields.get('code',  ''),
                                self.mapServiceKeyToId,
                                self.tableService)


    def lookupMedicalAidType(self, fields):
        '''Для идентификации типа мед. помощи используем имя и код'''
        return self.lookupAnythingByNameAndCode(fields.get('name', ''),
                                fields.get('code',  ''),
                                self.mapMedicalAidTypeKeyToId,
                                self.tableMedicalAidType)


    def lookupEventProfile(self, fields):
        '''Для идентификации типа мед. помощи используем имя и код'''
        return self.lookupAnythingByNameAndCode(fields.get('name', ''),
                                fields.get('code',  ''),
                                self.mapEventProfileKeyToId,
                                self.tableEventProfile)


    def lookupVisitType(self, fields):
        '''Для идентификации типа визита используем имя и код'''
        return self.lookupAnythingByNameAndCode(fields.get('name', ''),
                                fields.get('code',  ''),
                                self.mapVisitTypeKeyToId, self.tableVisitType)


    def lookupHealthGroup(self, fields):
        '''Для идентификации типа визита используем имя и код'''
        return self.lookupAnythingByNameAndCode(fields.get('name', ''),
                                fields.get('code',  ''),
                                self.mapHealthGroupKeyToId,
                                self.tableHealthGroup)


    def lookupPurpose(self, fields):
        ''' Для идентификации назначения типа события
            используем имя и код'''
        return self.lookupAnythingByNameAndCode(fields.get('name', ''),
                                fields.get('code',  ''),
                                self.mapPurposeKeyToId, self.tablePurpose)


    def lookupSpeciality(self, fields):
        ''' Для идентификации специальности используем имя и код'''
        return self.lookupAnythingByNameAndCode(fields.get('name', ''),
                                fields.get('code',  ''),
                                self.mapSpecialityKeyToId, self.tableSpeciality)


    def lookupFinance(self, fields):
        ''' Для идентификации типа финансирования используем имя и код'''
        return self.lookupAnythingByNameAndCode(fields.get('name', ''),
                                fields.get('code',  ''),
                                self.mapFinanceKeyToId,  self.tableFinance)


    def lookupDispanser(self, fields):
        return self.lookupAnythingByNameAndCode(fields.get('name', ''),
                                fields.get('code',  ''),
                                self.mapDispanserKeyToId,  self.tableDispanser)


    def lookupScene(self, fields):
        return self.lookupAnythingByNameAndCode(fields.get('name', ''),
                                fields.get('code',  ''),  self.mapSceneKeyToId,
                                self.tableScene)


    def lookupMedicalAidKind(self, fields):
        return self.lookupAnythingByNameAndCode(fields.get('name', ''),
                                fields.get('code', ''),  self.mapMedicalAidKindKeyToId,
                                self.tableMedicalAidKind)


    def lookupCounter(self, fields):
        return self.lookupAnythingByNameAndCode(fields.get('name', ''),
                                fields.get('code', ''), self.mapCounterKeyToId,
                                self.tableCounter)


    def isCoincidentEventType(self,  eventType,  id):
        record = self.db.getRecord(self.tableEventType, \
                                self.eventTypeFieldNamesExist, id)

        if record:
            for x in self.eventTypeFieldNamesNoRefsExist:
                if forceString(record.value(x)) != forceString(eventType[x]):
                    return False

            for x in eventTypeRefFields[1:]:
                a = eventType.get(x)
                b = forceRef(record.value(x))

                if (a != b) or ((not b) and eventType.has_key(x)):
                    return False

            return True

        return False


    def prepareMessageBoxText(self, eventType, id):
        record = self.db.getRecord(self.tableEventType, \
                                self.eventTypeFieldNamesExist, id)
        str = u'''<h3>Обнаружены следующие различия в записях:</h3>\n\n\n
                        <table>
                        <tr>
                            <td><b>Название поля</b></td>
                            <td align=center><b>Новое</b></td>
                            <td align=center><b>Исходное</b></td>
                        </tr>'''

        if record:
            for x in self.eventTypeFieldNamesNoRefsExist:
                str += '<tr><td><b> '+x+': </b></td>'

                if forceString(record.value(x)) != forceString(eventType[x]):
                    str += '<td align=center bgcolor=''red''> '
                else:
                    str += '<td align=center>'

                str += forceString(eventType[x])+' </td><td align=center>' \
                        + forceString(record.value(x)) + '</td></tr>\n'

            for x in ('service_id', 'finance_id', 'purpose_id',  'medicalAidType_id',  'eventProfile_id'):
                a = eventType.get(x)
                b = forceRef(record.value(x))

                if (a != b) or (eventType.has_key(x) and (not b)):
                    str += '<tr><td><b> '+x+': </b></td><td align=center bgcolor=red>' \
                            + forceString(eventType.get(x, '0'))
                    str += ' </td><td align=center>' + forceString(record.value(x)) \
                            + '</td></tr>\n'

            str += u'</table>\n\n<p align=center>Обновить?</p>'
        return str


    def prepareEventPropertyMessageBoxText(self, eventProperty):
        str = u'Обнаружено новое свойство типа события: добавить?'
        return str

    def processElement(self, fields, table, fieldNameList, cache, message=None):
        id = fields['id']

        if not id: # нету в базе. добавим
            record = table.newRecord()

            for x in fieldNameList:
                if fields.get(x):
                    record.setValue(x, toVariant(fields[x]))

            id = self.db.insertRecord(table, record)
            # добавим в кэш
            cache[(fields['code'], fields['name'])] = id

            if message:
                self.log(message)

        return id

    def processService(self,  service):
        return self.processElement(service, self.tableService, serviceFields,
                                    self.mapServiceKeyToId,
                                    u'Добавлена услуга: (%s) "%s"' % (
                                        service['code'], service['name']))


    def processFinance(self,  finance):
        return self.processElement(finance, self.tableFinance, ('code', 'name'),
                                   self.mapFinanceKeyToId,
                                    u'Добавлен тип финансировния: (%s) "%s"' % \
                                        (finance['code'], finance['name']))


    def processPurpose(self,  purpose):
        return self.processElement(purpose, self.tablePurpose, ('code', 'name'),
                                   self.mapPurposeKeyToId,
                                   u'Добавлено назначение типа события: (%s) "%s"' % \
                                        (purpose['code'], purpose['name']))


    def processMedicalAidType(self,  element):
        return self.processElement(element, self.tableMedicalAidType,
                                   medicalAidTypeFields,
                                   self.mapMedicalAidTypeKeyToId,
                                   u'Добавлен тип мед. помощи: (%s) "%s"' % \
                                        (element['code'], element['name']))


    def processEventProfile(self,  element):
        return self.processElement(element, self.tableEventProfile,
                                   eventProfileFields,
                                   self.mapEventProfileKeyToId,
                                   u'Добавлен профиль события: (%s) "%s"' % \
                                        (element['code'], element['name']))


    def processMedicalAidKind(self, element):
        return self.processElement(element, self.tableMedicalAidKind,
                                   medicalAidKindFields,
                                   self.mapMedicalAidKindKeyToId,
                                   u'Добавлен вид мед. помощи: (%s) "%s"' % \
                                        (element['code'], element['name']))


    def processCounter(self, element):
        return self.processElement(element, self.tableCounter,
                                   counterFields, self.mapCounterKeyToId,
                                   u'Добавлен счетчик: (%s) "%s"' % \
                                    (element['code'], element['name']))


    def processScene(self, element):
        return self.processElement(element, self.tableScene,
                                   sceneFields, self.mapSceneKeyToId,
                                   u'Добавлено место: (%s) "%s"' % \
                                   (element['code'], element['name']))


    def isCoincidentEventTypeProperty(self,  eventProperty,  eventTypeId):
        ''' Сравнивает все поля, выдает True в случае совпадения'''
        table = None
        fieldList = []
        refFields = []

        l = self.getEventPropertyParams(eventProperty)
        if not l:
            return False

        (table,  fieldList,  refFields) = l

        allFields = fieldList + refFields
        eventProperty['eventType_id'] = eventTypeId
        cond = []

        for x in allFields:
            if eventProperty.has_key(x) and eventProperty[x]:
                cond.append(table[x].eq(toVariant(eventProperty[x])))

        record = self.db.getRecordEx(table, allFields, cond)

        if record:
            # если свойство не относится к текущему действию
            if forceInt(eventTypeId) != forceInt(record.value('eventType_id')):
                return False

            # проверяем все поля, кроме внешних ключей
            for x in fieldList: # сверяется все, кроме id, unit_id
                if forceString(record.value(x)) != forceString(eventProperty[x]):
                    return False

            # проверяем все внешние ключи
            for x in refFields:
                if eventProperty.has_key(x): # проверяем id
                    if forceInt(eventProperty[x]) != forceInt(record.value(x)):
                        return False
                else:
                    # В приёмнике есть ссылка, а в у нас её нету
                    if forceInt(record.value(x)) != 0:
                        return False

            return True

        return False


    def addEventProperty(self,  p,  id):
        '''Добавляет свойство события в бд
                p - словарь с параметрами свойства
                id - идентификатор события в бд '''
        fieldsList = []
        refFields = []
        table = None

        (table,  fieldsList,  refFields) = self.getEventPropertyParams(p)

        record = table.newRecord()

        if p.has_key('action_type'):
            actionTypeId = p['action_type']['id']

            if not actionTypeId or actionTypeId == 0:
                self.log(u'! Отсутствует тип действия: (%s) "%s"' % \
                    (p['action_type']['code'],  p['action_type']['name']))
                self.log(u'! Мероприятие не добавлено')
                return False

            record.setValue('actionType_id',  toVariant(actionTypeId))


        for fieldName in fieldsList:
            if p[fieldName]:
                record.setValue(fieldName, toVariant(p[fieldName]))

        if p.has_key('speciality'):
            if forceInt(p['speciality_id']) == 0:
                p['speciality_id'] = self.addSpeciality(p['speciality'])

            record.setValue('speciality_id', toVariant(p['speciality_id']))

        if p.has_key('defaultHealthGroup'):
            if forceInt(p['defaultHealthGroup_id']) == 0:
                p['defaultHealthGroup_id'] = \
                    self.addHealthGroup(p['defaultHealthGroup'])

            record.setValue('defaultHealthGroup_id',  \
                toVariant(p['defaultHealthGroup_id']))

        if p.has_key('defaultDispanser'):
            if not p.get('defaultDispanser_id'):
                p['defaultDispanser_id'] = \
                    self.addDispanser(p['defaultDispanser'])
            record.setValue('defaultDispanser_id',  \
                toVariant(p['defaultDispanser_id']))

        if p.has_key('visitType'):
            if forceInt(p['visitType_id']) == 0:
                p['visitType_id'] = self.addVisitType(p['visitType'])

            record.setValue('visitType_id',  toVariant(p['visitType_id']))

        record.setValue('eventType_id',  toVariant(id))
        self.db.insertRecord(table,  record)
        return True


    def addElement(self, element, table, cache, fields, key, message=None):
        id = cache.get(key)

        if not id:
            record = table.newRecord()

            for x in fields:
                if element.get(x):
                    record.setValue(x, toVariant(element[x]))

            id = self.db.insertRecord(table, record)
            cache[key] = id

            if message:
                self.log(message)

        return id


    def addSpeciality(self,  speciality):
        key = (speciality['code'], speciality['name'])
        return self.addElement(speciality, self.tableSpeciality,
                               self.mapSpecialityKeyToId, ('code', 'name'),
                               key, u'Добавлена специальность: (%s) "%s"' % key)


    def addHealthGroup(self,  element):
        key = (element['code'], element['name'])
        return self.addElement(element, self.tableHealthGroup,
                               self.mapHealthGroupKeyToId, ('code', 'name'),
                               key, u'Добавлена группа здоровья: (%s) "%s"' % key)


    def addVisitType(self,  element):
        key = (element['code'], element['name'])
        return self.addElement(element, self.tableVisitType,
                               self.mapVisitTypeKeyToId, ('code', 'name'),
                               key, u'Добавлен тип визита: (%s) "%s"' % key)


    def addDispanser(self,  element):
        key = (element['code'], element['name'])
        return self.addElement(element, self.tableDispanser,
                               self.mapDispanserKeyToId, ('code', 'name'),
                               key, u'Добавлена отметка диспансерного наблюдения: (%s) "%s"' % key)


    def updateEventType(self, eventType, id, service, finance, scene,
                        purpose, medicalAidType, medicalAidKind, eventProfile,
                        counter):
        eventType['id'] = id

        if service:
            eventType['service_id'] =  self.processService(service)

        if finance:
            eventType['finance_id'] =  self.processFinance(finance)

        if purpose:
            eventType['purpose_id'] =  self.processPurpose(purpose)

        if medicalAidType:
            eventType['medicalAidType_id'] = self.processMedicalAidType(medicalAidType)

        if eventProfile:
            eventType['eventProfile_id'] = self.processEventProfile(eventProfile)

        if scene:
            eventType['scene_id'] = self.processScene(scene)

        if medicalAidKind:
            eventType['medicalAidKind_id'] = self.processMedicalAidKind(medicalAidKind)

        if counter:
            eventType['counter_id'] = self.processCounter(counter)

        record = self.db.getRecord(self.tableEventType, self.eventTypeFieldNamesExist, id)

        for x in self.eventTypeFieldNamesExist:
            val = eventType.get(x, None)
            if val:
                record.setValue(x, toVariant(val))
            else:
                record.setNull(x)

        self.db.updateRecord(self.tableEventType, record)
        self.nupdated += 1


class CImportEventTypeWizardPage1(QtGui.QWizardPage, Ui_ImportEvents_Wizard_1):
    def __init__(self,  parent):
        QtGui.QWizardPage.__init__(self, parent)
        self.parent = parent #wtf? скрывать Qt-шный parent - это плохая затея
        self.setTitle(u'Параметры загрузки')
        self.setSubTitle(u'Выбор источника импорта')
        self.isPreImportDone = False
        self.aborted = False
        self.setupUi(self)
        self.progressBar.reset()
        self.progressBar.setValue(0)
        self.edtFileName.setText(parent.fileName)
        self.chkFullLog.setChecked(parent.fullLog)
        self.connect(parent, SIGNAL('rejected()'), self.abort)


    def isComplete(self):
        return self.edtFileName.text()!= ''


    def validatePage(self):
        self.import_()
        return self.isPreImportDone


    def abort(self):
        self.aborted = True


    def import_(self):
        self.isPreImportDone = False
        self.aborted = False
        success,  result = QtGui.qApp.call(self, self.doPreImport)

        if self.aborted or not success:
            self.progressBar.setText(u'Прервано')
        else:
            self.isPreImportDone = result


    def doPreImport(self):
        inFile = QFile(self.parent.fileName)
        if not inFile.open(QFile.ReadOnly | QFile.Text):
            QtGui.QMessageBox.warning(self, u'Импорт типов событий',
                                      u'Не могу открыть файл для чтения %s:\n%s.' % \
                                      (self.parent.fileName, inFile.errorString()))
            return False
        else:
            self.progressBar.reset()
            self.progressBar.setValue(0)
            self.progressBar.setFormat(u'%v байт')
            self.statusLabel.setText(u'Составления списка событий для загрузки')
            self.progressBar.setMaximum(max(inFile.size(), 1))
            myXmlStreamReader = CMyXmlStreamReader(self)
            if (myXmlStreamReader.readFile(inFile,  None,  True)):
                self.progressBar.setText(u'Готово')
                # сохраняем список найденных типов событий в предке
                self.parent.eventsList = myXmlStreamReader.eventsList
                self.statusLabel.setText(u'Найдено %d событий для импорта' % len(self.parent.eventsList))
            else:
                self.progressBar.setText(u'Прервано')
                if self.aborted:
                    self.logBrowser.append(u'! Прервано пользователем.')
                else:
                    self.logBrowser.append(u'! Ошибка: файл %s, %s' % (self.parent.fileName, myXmlStreamReader.errorString()))
                return False

        return True

    @pyqtSignature('')
    def on_btnSelectFile_clicked(self):
        self.parent.fileName = QtGui.QFileDialog.getOpenFileName(
            self, u'Укажите файл с данными', self.edtFileName.text(), u'Файлы XML (*.xml)')
        if self.parent.fileName != '':
            self.edtFileName.setText(QDir.toNativeSeparators(self.parent.fileName))
            self.emit(SIGNAL('completeChanged()'))


    @pyqtSignature('QString')
    def on_edtFileName_textChanged(self,  text):
        self.emit(SIGNAL('completeChanged()'))
        self.parent.fileName = unicode(text)


    @pyqtSignature('bool')
    def on_chkFullLog_toggled(self,  checked):
        self.parent.fullLog = checked


class CImportEventTypeWizardPage2(QtGui.QWizardPage, Ui_ImportEvents_Wizard_2):
    def __init__(self,  parent):
        QtGui.QWizardPage.__init__(self, parent)
        self.parent = parent #wtf? скрывать Qt-шный parent - это плохая затея
        self.setTitle(u'Параметры загрузки')
        self.setSubTitle(u'Выбор событий для импорта')
        self.setupUi(self)
        self.chkImportAll.setChecked(parent.importAll)
        #self.postSetupUi()


    def isComplete(self):
        return self.parent.importAll or self.parent.selectedItems != []


    def initializePage(self):
        self.tblEvents.setRowCount(len(self.parent.eventsList))
        self.tblEvents.setColumnCount(2) # code, name
        self.tblEvents.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.tblEvents.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblEvents.setHorizontalHeaderLabels((u'Код',  u'Наименование'))
        self.tblEvents.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.tblEvents.horizontalHeader().setStretchLastSection(True)
        self.tblEvents.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.tblEvents.verticalHeader().hide()

        i = 0

        for x in self.parent.eventsList:
            eventNameItem = QtGui.QTableWidgetItem(x[1])
            eventCodeItem = QtGui.QTableWidgetItem(x[0])
            eventNameItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            eventCodeItem.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tblEvents.setItem(i, 0,  eventCodeItem)
            self.tblEvents.setItem(i, 1,  eventNameItem)
            i += 1

    @pyqtSignature('bool')
    def on_chkImportAll_toggled(self,  checked):
        self.parent.importAll = checked
        self.tblEvents.setEnabled(not checked)
        self.btnClearSelection.setEnabled(not checked)

        if checked:
            self.statusLabel.setText(u'Выбраны все события для импорта')
        else:
            self.statusLabel.setText(u'Выбрано событий для импорта: %d' % \
                                        len(self.parent.selectedItems))

        self.emit(SIGNAL('completeChanged()'))


    @pyqtSignature('')
    def on_tblEvents_itemSelectionChanged(self):
        self.parent.selectedItems = []
        for r in self.tblEvents.selectedRanges():
            for row in range(r.topRow(),  r.bottomRow()+1):
                code = forceString(self.tblEvents.item(row, 0).data(Qt.DisplayRole))
                name = forceString(self.tblEvents.item(row, 1).data(Qt.DisplayRole))
                self.parent.selectedItems.append((code, name))

        self.statusLabel.setText(u'Выбрано событий для импорта: %d' % \
                                        len(self.parent.selectedItems))
        self.emit(SIGNAL('completeChanged()'))


class CImportEventTypeWizardPage3(QtGui.QWizardPage, Ui_ImportEvents_Wizard_3):
    def __init__(self,  parent):
        QtGui.QWizardPage.__init__(self, parent)
        self.parent = parent #wtf? скрывать Qt-шный parent - это плохая затея
        self.setTitle(u'Загрузка')
        self.setSubTitle(u'Импорт типов событий')
        self.setupUi(self)
        self.isImportDone = False
        self.aborted = False
        self.connect(self, SIGNAL('import()'), self.import_, Qt.QueuedConnection)
        self.connect(parent, SIGNAL('rejected()'), self.abort)


    def isComplete(self):
        return self.isImportDone


    def initializePage(self):
        self.emit(SIGNAL('import()'))


    def abort(self):
        self.aborted = True


    def import_(self):
        self.isImportDone = False
        self.aborted = False
        success,  result = QtGui.qApp.call(self, self.doImport)

        if self.aborted or not success:
            self.progressBar.setText(u'Прервано')


    def doImport(self):
        inFile = QFile(self.parent.fileName)
        if not inFile.open(QFile.ReadOnly | QFile.Text):
            QtGui.QMessageBox.warning(self, u'Импорт типов событий',
                                      u'Не могу открыть файл для чтения %s:\n%s.' % \
                                      (self.parent.fileName, inFile.errorString()))
            return
        else:
            self.progressBar.reset()
            self.progressBar.setValue(0)
            self.progressBar.setFormat(u'%v байт')
            self.progressBar.setMaximum(max(inFile.size(), 1))
            myXmlStreamReader = CMyXmlStreamReader(self,  self.parent.fullLog)
            itemsList = None if self.parent.importAll else self.parent.selectedItems

            if (myXmlStreamReader.readFile(inFile,  itemsList)):
                self.progressBar.setText(u'Готово')
                self.isImportDone = True
                self.emit(SIGNAL('completeChanged()'))
                # сохраняем список найденных типов событий в предке
                #self.statusLabel.setText(u'Найдено %d событий для импорта' % len(self.parent.eventsList))
            else:
                self.progressBar.setText(u'Прервано')
                if self.aborted:
                    self.logBrowser.append(u'! Прервано пользователем.')
                else:
                    self.logBrowser.append(u'! Ошибка: файл %s, %s' % (self.parent.fileName, myXmlStreamReader.errorString()))


    @pyqtSignature('')
    def on_btnAbort_clicked(self):
        self.abort()



class CImportEventType(QtGui.QWizard):
    def __init__(self, fileName = '',  importAll = False,  fullLog = False,  parent=None):
        QtGui.QWizard.__init__(self, parent, Qt.Dialog)
        self.setWizardStyle(QtGui.QWizard.ModernStyle)
        self.setWindowTitle(u'Импорт типов событий')
        self.fullLog = fullLog
        self.importAll = importAll
        self.selectedItems = []
        self.eventsList =[]
        self.fileName= fileName
        self.addPage(CImportEventTypeWizardPage1(self))
        self.addPage(CImportEventTypeWizardPage2(self))
        self.addPage(CImportEventTypeWizardPage3(self))
