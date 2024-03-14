#!/usr/bin/env python
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
from PyQt4.QtCore import Qt, QDir, QFile, QXmlStreamWriter, pyqtSignature, SIGNAL

from library.DialogBase import CConstructHelperMixin
from library.TableModel import CTableModel, CTextCol
from library.Utils import anyToUnicode, exceptionToUnicode, forceBool, forceDate, forceInt, forceString, toVariant

from Exchange.Utils import compressFileInRar

from Exchange.Ui_ExportEvents_Wizard_1 import Ui_ExportEvents_Wizard_1
from Exchange.Ui_ExportEvents_Wizard_2 import Ui_ExportEvents_Wizard_2

# список экспортируемых полей, без ссылок (*_id)
eventTypeFields = ('code',  'regionalCode', 'name', 'weekProfileCode',
        'visitServiceModifier', 'visitServiceFilter',  'visitFinance',
        'actionFinance', 'actionContract', 'period', 'singleInPeriod',  'isLong',
        'dateInput', 'context',  'form', 'minDuration',  'maxDuration',
        'showStatusActionsInPlanner', 'showDiagnosticActionsInPlanner',
        'showCureActionsInPlanner', 'showMiscActionsInPlanner',
        'limitStatusActionsInput', 'limitDiagnosticActionsInput',
        'limitCureActionsInput', 'limitMiscActionsInput', 'showTime',
        'mesRequired', 'mesCodeMask', 'mesNameMask' ,
        'isExternal',  'hasAssistant',  'hasCurator',  'hasVisitAssistant',
        'canHavePayableActions',  'isRequiredCoordination',
        'isOrgStructurePriority', 'isTakenIssue',  'sex',  'age',
        'contractCondition')

eventTypePurposeFields = ('code',  'name')

financeFields = ('code',  'name')

sceneFields = ('code',  'name')

serviceFields = ('code', 'name', 'eisLegacy', 'nomenclatureLegacy', \
                        'license', 'infis', 'begDate', 'endDate')

serviceDateFileds = ('begDate', 'endDate')

medicalAidTypeFields = ('code',  'name')

medicalAidKindFields = ('code',  'name')

eventProfileFields = ('code',  'regionalCode',  'name')

counterFields = ('code', 'name')

dispanserFields = ('code',  'name')

exportFormatVersion = '1.2'


def ExportEventType():
    fileName = forceString(QtGui.qApp.preferences.appPrefs.get('ExportEventTypeFileName', ''))
    exportAll = forceBool(QtGui.qApp.preferences.appPrefs.get('ExportEventTypeExportAll', 'False'))
    compressRAR = forceBool(QtGui.qApp.preferences.appPrefs.get('ExportEventTypeCompressRAR', 'False'))
    dlg = CExportEventType(fileName, exportAll, compressRAR)
    dlg.exec_()
    QtGui.qApp.preferences.appPrefs['ExportEventTypeFileName'] = toVariant(dlg.fileName)
    QtGui.qApp.preferences.appPrefs['ExportEventTypeExportAll'] = toVariant(dlg.exportAll)
    QtGui.qApp.preferences.appPrefs['ExportEventTypeCompressRAR'] = toVariant(dlg.compressRAR)


def checkPropertyList(tableName, propsList):
    u'''Проверяет, есть ли в указанной таблицы поля из списка propsList
        Возвращает список найденных полей.'''
    db = QtGui.qApp.db
    table = db.table(tableName)
    return [prop for prop in propsList if prop in table.fieldsDict]


class CMyXmlStreamWriter(QXmlStreamWriter):
    def __init__(self,  parent, idList):
        QXmlStreamWriter.__init__(self)
        self.parent = parent
        self.setAutoFormatting(True)
        self._idList = idList


    def createQuery(self,  idList,  propsList):
        u''' Запрос информации о типах событий. Если idList пуст,
            запрашиваются все типы событий'''

        db = QtGui.qApp.db
        stmt = '''
        SELECT  e.id, rbEventTypePurpose.code AS `purpose_code`,
                    rbEventTypePurpose.name AS `purpose_name`,
                    rbFinance.code AS `finance_code`,
                    rbFinance.name AS `finance_name`,
                    rbScene.code AS `scene_code`,
                    rbScene.name AS `scene_name`,
                    rbService.code AS `service_code`,
                    rbService.name AS `service_name`,
                    rbService.eisLegacy AS `service_eisLegacy`,
                    rbService.license AS `service_license`,
                    rbService.infis AS `service_infis`,
                    rbService.begDate AS `service_begDate`,
                    rbService.endDate AS `service_endDate`,
                    rbMedicalAidType.code AS `medicalAidType_code`,
                    rbMedicalAidType.name AS `medicalAidType_name`,
                    rbMedicalAidKind.code AS `medicalAidKind_code`,
                    rbMedicalAidKind.name AS `medicalAidKind_name`,
                    rbEventProfile.code AS `eventProfile_code`,
                    rbEventProfile.regionalCode AS `eventProfile_regionalCode`,
                    rbEventProfile.name AS `eventProfile_name`,
                    rbCounter.code AS `counter_code`,
                    rbCounter.name AS `counter_name`'''

        if propsList != []:
            stmt+= ','+ ', '.join(['e.%s' % et for et in propsList])

        stmt +=    ''' FROM EventType e
        LEFT JOIN rbEventTypePurpose ON e.purpose_id = rbEventTypePurpose.id
        LEFT JOIN rbScene ON e.scene_id = rbScene.id
        LEFT JOIN rbFinance ON e.finance_id = rbFinance.id
        LEFT JOIN rbService ON e.service_id = rbService.id
        LEFT JOIN rbMedicalAidType ON e.medicalAidType_id = rbMedicalAidType.id
        LEFT JOIN rbMedicalAidKind ON e.medicalAidKind_id = rbMedicalAidKind.id
        LEFT JOIN rbEventProfile ON e.eventProfile_id = rbEventProfile.id
        LEFT JOIN rbCounter ON e.counter_id = rbCounter.id
        WHERE
        '''
        if idList:
            stmt+= ' e.id in ('+', '.join([str(et) for et in idList])+ ') AND '

        stmt += ' e.deleted = 0'

        query = db.query(stmt)
        return query

    def createEventTypeActionQuery(self, eventTypeId,  propsList):
        u'''Запрос действий для указанного типа события.  Для типа
            действия и специальности выгружается их код и имя. '''

        db = QtGui.qApp.db
        stmt = '''
        SELECT  ActionType.code AS `ActionType_code`,
                    ActionType.name AS `ActionType_name`,
                    rbSpeciality.code AS `speciality_code`,
                    rbSpeciality.name AS `speciality_name`'''
        if propsList != []:
            stmt+= ','+ ', '.join(['e.%s' % et for et in propsList])
        stmt +=    '''
        FROM EventType_Action e
        LEFT JOIN ActionType ON e.actionType_id = ActionType.id
        LEFT JOIN rbSpeciality ON e.speciality_id = rbSpeciality.id
        WHERE e.eventType_id = %d
        ''' % eventTypeId
        query = db.query(stmt)
        return query


    def createEventTypeDiagnosticQuery(self, eventTypeId,  propsList):
        u''' Запрос диагностик для указанного типа события.  Для
            всех справочников выгружается их код и имя. '''

        db = QtGui.qApp.db
        stmt = '''
        SELECT  rbSpeciality.code AS `speciality_code`,
                    rbSpeciality.name AS `speciality_name`,
                    rbHealthGroup.code AS `defaultHealthGroup_code`,
                    rbHealthGroup.name AS `defaultHealthGroup_name`,
                    rbVisitType.code AS `visitType_code`,
                    rbVisitType.name AS `visitType_name`,
                    rbDispanser.code AS `defaultDispanser_code`,
                    rbDispanser.name AS `defaultDispanser_name`,
                    rbDispanser.observed AS `defaultDispanser_observed`'''
        if propsList != []:
            stmt+= ','+ ', '.join(['e.%s' % et  for et in propsList])
        stmt +=    '''
        FROM EventType_Diagnostic e
        LEFT JOIN rbSpeciality ON e.speciality_id = rbSpeciality.id
        LEFT JOIN rbHealthGroup ON e.defaultHealthGroup_id = rbHealthGroup.id
        LEFT JOIN rbVisitType ON e.visitType_id = rbVisitType.id
        LEFT JOIN rbDispanser ON e.defaultDispanser_id = rbDispanser.id
        WHERE e.eventType_id = %d
        ''' % eventTypeId
        query = db.query(stmt)
        return query


    def createEventTypeFormQuery(self,  eventTypeId,  propsList):
        u''' Запрос форм для указанного типа события. '''

        db = QtGui.qApp.db
        stmt = '''
        SELECT
        ''' +', '.join(['e.%s' % et for et in propsList])+ '''
        FROM EventTypeForm e
        WHERE e.eventType_id = %d AND e.deleted = 0
        ''' % eventTypeId
        query = db.query(stmt)
        return query


    def writeEventTypeParams(self,  record,  elementName,  propertiesList,  rbList):
        self.writeStartElement(elementName)

        for x in propertiesList:
            self.writeAttribute(x,  forceString(record.value(x)))

        if rbList:
            for (x,  fields) in rbList:
                if forceString(record.value(x+'_name')) != '':
                    self.writeStartElement(x)
                    for f in fields:
                        self.writeAttribute(f, forceString(record.value(x+'_'+f)))
                    self.writeEndElement()

        self.writeEndElement()


    def processEventProperties(self, eventId):
        actionProperties = ('idx',  'sex',  'age',  'selectionGroup',  \
                                    'actuality',  'expose')
        actionRb = (
                ('ActionType',  ('code',  'name')),
                ('speciality',  ('code',  'name')),
            )

        diagnosticProperties = ('idx',  'sex',  'age',  'defaultMKB',  \
                                'selectionGroup', 'actuality')
        diagnosticRb = (
                ('speciality',  ('code',  'name')),
                ('defaultDispancer',  dispanserFields),
                ('defaultHealthGroup',  ('code',  'name')),
                ('visitType',  ('code',  'name')),
            )

        formProperties = ('code',  'name',  'descr',  'pass')
        formRb = None

        propsList = checkPropertyList('EventType_Action', actionProperties)
        query = self.createEventTypeActionQuery(eventId,  propsList)
        while (query.next()):
            self.writeEventTypeParams(query.record(),  'Action', \
                                      propsList,  actionRb)

        propsList = checkPropertyList('EventType_Diagnostic', diagnosticProperties)
        query = self.createEventTypeDiagnosticQuery(eventId,  propsList)
        while (query.next()):
            self.writeEventTypeParams(query.record(),  'Diagnostic', \
                                      propsList,  diagnosticRb)

        propsList = checkPropertyList('EventTypeForm', formProperties)
        query = self.createEventTypeFormQuery(eventId,  propsList)
        while (query.next()):
            self.writeEventTypeParams(query.record(),  'Form', \
                                      propsList,  formRb)


    def writeRecord(self, record,  propsList):
        self.writeStartElement('EventType')

        # все свойства действия экспортируем как атрибуты
        for x in propsList:
            self.writeAttribute(x, forceString(record.value(x)))

        # все, что определяется ссылками на другие таблицы - как элементы

        # префикс таблицы, поля для выгрузки, поля с датами
        subTables = (
            ('service',  serviceFields,  serviceDateFileds),
            ('scene',  sceneFields,  None),
            ('purpose', eventTypePurposeFields,  None),
            ('finance',  financeFields,  None),
            ('medicalAidType', medicalAidTypeFields,  None),
            ('medicalAidKind', medicalAidKindFields,  None),
            ('eventProfile', eventProfileFields ,  None),
            ('counter',  counterFields,  None)
        )

        for (tableName, fields,  dateFields) in subTables:
            # поле name должно быть у всех выгружаемых таблиц!
            if (forceString(record.value('%s_name' % tableName))!= ''):
                self.writeStartElement(tableName)
                for x in fields:
                    if dateFields and (x in dateFields):
                        self.writeAttribute(x, forceDate(record.value('%s_%s' %\
                            (tableName,  x))).toString(Qt.ISODate))
                    else:
                        self.writeAttribute(x, forceString(record.value('%s_%s' %\
                            (tableName, x))))
                self.writeEndElement()

        # Выгружаем свойства события (осмотры, действия, формы)
        self.processEventProperties(forceInt(record.value('id')))
        self.writeEndElement()

    def writeFile(self,  device,  progressBar):
        global lastChangedRev
        global lastChangedDate
        try:
            from buildInfo import lastChangedRev, lastChangedDate
        except:
            lastChangedRev  = 'unknown'
            lastChangedDate = 'unknown'

        try:
            progressBar.setText(u'Запрос данных')
            propsList = checkPropertyList('EventType',  eventTypeFields)
            query = self.createQuery(self._idList,  propsList)
            self.setDevice(device)
            progressBar.setMaximum(max(query.size(), 1))
            progressBar.reset()
            progressBar.setValue(0)

            self.writeStartDocument()
            self.writeDTD('<!DOCTYPE xEventType>')
            self.writeStartElement('EventTypeExport')
            self.writeAttribute('SAMSON',
                                '2.0 revision(%s, %s)' %(lastChangedRev, lastChangedDate))
            self.writeAttribute('version', exportFormatVersion)
            while (query.next()):
                self.writeRecord(query.record(),  propsList)
                progressBar.step()

            self.writeEndDocument()

        except IOError, e:
            QtGui.qApp.logCurrentException()
            msg=''
            if hasattr(e, 'filename'):
                msg = u'%s:\n[Errno %s] %s' % (e.filename, e.errno, anyToUnicode(e.strerror))
            else:
                msg = u'[Errno %s] %s' % (e.errno, anyToUnicode(e.strerror))
            QtGui.QMessageBox.critical (self.parent,
                u'Произошла ошибка ввода-вывода', msg, QtGui.QMessageBox.Close)
            return False
        except Exception, e:
            QtGui.qApp.logCurrentException()
            QtGui.QMessageBox.critical (self.parent,
                u'Произошла ошибка', exceptionToUnicode(e), QtGui.QMessageBox.Close)
            return False

        return True


class CExportEventTypeWizardPage1(QtGui.QWizardPage, Ui_ExportEvents_Wizard_1, CConstructHelperMixin):
    def __init__(self, parent):
        QtGui.QWizardPage.__init__(self, parent)
        self.cols = [
            CTextCol(   u'Код',          ['code'], 20),
            CTextCol(   u'Наименование', ['name'],   40)
            ]
        self.tableName = 'EventType'
        self.order = ['code', 'name', 'id']
        self.parent = parent #wtf? скрывать Qt-шный parent - это плохая затея
        self.preSetupUi()
        self.setupUi(self)
        self.postSetupUi()
        self.setTitle(u'Параметры экспорта')
        self.setSubTitle(u'Выбор записей для экспорта')


    def isComplete(self):
        # проверим пустой ли у нас список выбранных элементов
        return self.parent.exportAll or self.parent.selectedItems != []


    def preSetupUi(self):
        self.addModels('Table',CTableModel(self, self.cols, self.tableName))


    def postSetupUi(self):
        self.setModels(self.tblItems,   self.modelTable, self.selectionModelTable)
        self.tblItems.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        idList = self.select()
        self.modelTable.setIdList(idList)
        self.selectionModelTable.clearSelection()
        self.tblItems.setFocus(Qt.OtherFocusReason)
        self.tblItems.setEnabled(not self.parent.exportAll)
        self.btnClearSelection.setEnabled(not self.parent.exportAll)
        self.checkExportAll.setChecked(self.parent.exportAll)


    def select(self):
        table = self.modelTable.table()
        return QtGui.qApp.db.getIdList(table.name(), order=self.order)


    @pyqtSignature('QModelIndex')
    def on_tblItems_clicked(self, index):
        self.parent.selectedItems =self.tblItems.selectedItemIdList()
        self.emit(SIGNAL('completeChanged()'))


    @pyqtSignature('')
    def on_btnClearSelection_clicked(self):
        self.parent.selectedItems = []
        self.selectionModelTable.clearSelection()
        self.emit(SIGNAL('completeChanged()'))


    @pyqtSignature('')
    def on_checkExportAll_clicked(self):
        self.parent.exportAll = self.checkExportAll.isChecked()
        self.tblItems.setEnabled(not self.parent.exportAll)
        self.btnClearSelection.setEnabled(not self.parent.exportAll)
        self.emit(SIGNAL('completeChanged()'))



class CExportEventTypeWizardPage2(QtGui.QWizardPage, Ui_ExportEvents_Wizard_2):
    def __init__(self,  parent):
        QtGui.QWizardPage.__init__(self, parent)
        self.setupUi(self)
        self.parent=parent #wtf? скрывать Qt-шный parent - это плохая затея
        self.setTitle(u'Параметры сохранения')
        self.setSubTitle(u'Выбор места для сохранения')
        self.progressBar.setFormat('%p%')
        self.progressBar.setValue(0)
        self.edtFileName.setText(self.parent.fileName)
        self.btnExport.setEnabled(self.parent.fileName != '')
        self.checkRAR.setChecked(self.parent.compressRAR)
        self.done = False


    def isComplete(self):
        return self.done


    @pyqtSignature('')
    def on_btnSelectFile_clicked(self):
        fileName = QtGui.QFileDialog.getSaveFileName(
            self, u'Укажите файл с данными', self.edtFileName.text(), u'Файлы XML (*.xml)')
        if fileName != '':
            fileName = QDir.toNativeSeparators(fileName)
            self.edtFileName.setText(fileName)
            self.parent.fileName = fileName
            self.btnExport.setEnabled(True)


    @pyqtSignature('')
    def on_btnExport_clicked(self):
        assert self.parent.exportAll or self.parent.selectedItems != []
        fileName = self.edtFileName.text()

        if fileName.isEmpty():
            return

        outFile = QFile(fileName)
        if not outFile.open(QFile.WriteOnly | QFile.Text):
            QtGui.QMessageBox.warning(self, u'Экспорт типов событий',
                                      u'Не могу открыть файл для записи %s:\n%s.'
                                      % (fileName,  outFile.errorString()))
            return

        myXmlStreamWriter = CMyXmlStreamWriter(self, self.parent.selectedItems)
        if (myXmlStreamWriter.writeFile(outFile,  self.progressBar)):
            self.progressBar.setText(u'Готово')
        else:
            self.progressBar.setText(u'Прервано')
        outFile.close()

        if self.checkRAR.isChecked():
            self.progressBar.setText(u'Сжатие')
            compressFileInRar(fileName, fileName+'.rar')
            self.progressBar.setText(u'Сжато в "%s"' % (fileName+'.rar'))

        self.done = True
        self.btnExport.setEnabled(False)
        self.emit(SIGNAL('completeChanged()'))

    @pyqtSignature('')
    def on_checkRAR_clicked(self):
        self.parent.compressRAR = self.checkRAR.isChecked()


class CExportEventType(QtGui.QWizard):
    def __init__(self, fileName,  exportAll, compressRAR,  parent=None):
        QtGui.QWizard.__init__(self, parent, Qt.Dialog)
        self.setWizardStyle(QtGui.QWizard.ModernStyle)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle(u'Экспорт типов событий')
        self.selectedItems = []
        self.fileName = fileName
        self.exportAll = exportAll
        self.compressRAR = compressRAR
        self.addPage(CExportEventTypeWizardPage1(self))
        self.addPage(CExportEventTypeWizardPage2(self))
