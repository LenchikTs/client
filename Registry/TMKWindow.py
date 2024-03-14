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
##
## Работа с отложенной записью
##
#############################################################################


import requests
from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDate, QDateTime, QMetaObject, QVariant, pyqtSignature, SIGNAL, QObject, pyqtSlot

from Events.ActionInfo import CActionInfo
from Events.CreateEvent import createEvent, editEvent
from Events.PreCreateEventDialog import CPreCreateEventDialog
from Events.Utils import getEventTypeForm
from Exchange.TMK.TMK_Method import moveToStage
from Timeline.Schedule import freeScheduleItem
from library.database                  import CTableRecordCache
from library.DialogBase                import CDialogBase, CConstructHelperMixin
from library.PreferencesMixin          import CDialogPreferencesMixin
from library.PrintInfo                 import CInfoContext
from library.PrintTemplates            import applyTemplate, CPrintAction, getPrintTemplates
from library.RecordLock                import CRecordLockMixin
from library.TableModel                import CBoolCol, CEnumCol, CDateCol, CDesignationCol, CTextCol, CDateTimeCol, CCol, CRefBookCol, CTableModel
from library.Utils import formatName, toVariant, forceString, withWaitCursor, forceRef, forceTime, forceBool, \
    formatRecordsCount, forceDate, forceStringEx, formatSex, forceInt, exceptionToUnicode
from Registry.RegistryWindow           import CSchedulesModel, CVisitsBySchedulesModel, convertFilterToTextItem, requestNewEvent
from Registry.Utils import getClientBanner, CCheckNetMixin
from Timeline.Schedule                 import CSchedule


from Ui_TMKWindow import Ui_TMKWindow
from Ui_HomeCallRequestUpdateStatusDialog import Ui_HomeCallRequestUpdateStatusDialog

StatusDict = {
    '85dad08c-1eb7-479f-8bf5-66b3ea5e4a02': u"Передано врачу",
    'f2eead71-c257-4f12-827c-cfe86776f1b4': u"Черновик",
    'f6917177-a702-4c7f-981a-84552c91addf': u"Направлено в МО",
    'd56f26ed-3947-4c4b-b1c2-414eb11cd576': u"Подготовка заключения консилиумом",
    '26e048e2-6c52-4e2f-9545-35e37b3cf013': u"Подпись заключения участниками консилиума",
    '1e658872-795b-445b-8632-cb70798f4dd5': u"Организация консилиума",
    'f0093882-61f3-4684-aa0e-52094991cbf8': u"Запрашивается дополнительная информация",
    'fff74636-1c39-448a-bbae-0f14f8c1f6a5': u"Подготовка заключения",
    '764f55f2-2c0e-43e3-81ce-3e5626682322': u"Отклонено",
    '425a04fc-b21e-4009-bf45-67625abddff6': u"В листе ожидания",
    'f869ab89-c111-4e65-a896-661f14d1d2db': u"На подписи у председателя консилиума",
    'ba65d940-8ebd-4583-a6cb-9a0f683ed331': u"Заключение готово",
    'ea0e8711-7b6e-4ad3-8bc2-904006eb569d': u"Заключение консилиума готово",
    '0': u"Все",
}

urgencyDict = {
    '1': u"Экстренная",
    '2': u"Неотложная",
    '3': u"Плановая",
    '4': u"Все",
}

primaryAppealList = {
        '1': u'первично',
        '2': u'повторно',
}


reasonCodeDict = {
    '1': u"Определение (подтверждение) диагноза",
    '2': u"Определение (подтверждение) тактики лечения и методов диагностики",
    '3': u"Согласование направления пациента в медицинскую организацию",
    '4': u"Согласование перевода пациента в медицинскую организацию",
    '5': u"Интерпретация результатов диагностического исследования",
    '6': u"Получение экспертного мнения по результату диагностического исследования",
    '7': u"Разбор клинического случая",
    '8': u"Дистанционное наблюдение за пациентом",
    '9': u"Другое",
}

AllowedStatuses = ['85dad08c-1eb7-479f-8bf5-66b3ea5e4a02',
    'f2eead71-c257-4f12-827c-cfe86776f1b4',
    'f6917177-a702-4c7f-981a-84552c91addf',
    'd56f26ed-3947-4c4b-b1c2-414eb11cd576',
    '26e048e2-6c52-4e2f-9545-35e37b3cf013',
    '1e658872-795b-445b-8632-cb70798f4dd5',
    'f0093882-61f3-4684-aa0e-52094991cbf8',
    'fff74636-1c39-448a-bbae-0f14f8c1f6a5',
    '764f55f2-2c0e-43e3-81ce-3e5626682322',
    '425a04fc-b21e-4009-bf45-67625abddff6',
    'f869ab89-c111-4e65-a896-661f14d1d2db',
    'ba65d940-8ebd-4583-a6cb-9a0f683ed331',
    'ea0e8711-7b6e-4ad3-8bc2-904006eb569d',
                   '0']

AllowedUrgency = ['1', '2', '3', '4']


def organisation(org):
    db = QtGui.qApp.db
    orgVal = ''
    if org:
        orgValue = db.getRecordEx(
            'Organisation',
            'title',
            'usishCode="%s" and deleted = 0 and isActive = 1' % org)
        if orgValue:
            orgVal = forceString(orgValue.value(0))
        else:
            orgValue = db.getRecordEx(
                'Organisation o LEFT JOIN Organisation_Identification oi ON o.id = oi.master_id ',
                'o.title',
                'oi.value="%s" and o.deleted = 0 and o.isActive = 1' % org)
            if orgValue:
                orgVal = forceString(orgValue.value(0))
        return orgVal
    else:
        return orgVal

class CTMKWindow(QtGui.QScrollArea, Ui_TMKWindow, CDialogPreferencesMixin, CConstructHelperMixin, CRecordLockMixin, CCheckNetMixin):
    def __init__(self, parent=None):
        QtGui.QScrollArea.__init__(self, parent)
        CCheckNetMixin.__init__(self)
        CRecordLockMixin.__init__(self)
        self.addModels('TMK', CTMKModel(self))
        # self.addModels('Schedules', CSchedulesModel(self))
        # self.addModels('VisitsBySchedules', CVisitsBySchedulesModel(self))
        self.addObject('actSetScheduleItem', QtGui.QAction(u'Подобрать номерок и назначить врача', self))
        self.addObject('actCancelTMK', QtGui.QAction(u'Отказать в принятии заявки', self))
        self.addObject('actCreateEvent', QtGui.QAction(u'Новое обращение', self))
        self.actCreateEvent.setShortcut(Qt.Key_Space)

        self.setObjectName('TMKWindow')
        self.internal = QtGui.QWidget(self)
        self.setWidget(self.internal)
        self.setupUi(self.internal)
        self.cmbFilterStatus.view().setMinimumWidth(280)
        self.setWindowTitle(self.internal.windowTitle())
        self.setWidgetResizable(True)
        QMetaObject.connectSlotsByName(self) # т.к. в setupUi параметр не self
        printTemplates = getPrintTemplates(['TMKList'])
        if not printTemplates:
            self.btnPrint.setId(-1)
        else:
            for template in printTemplates:
                action = CPrintAction(template.name, template.id, self.btnPrint, self.btnPrint)
                self.btnPrint.addAction(action)
            self.btnPrint.menu().addSeparator()
            self.btnPrint.addAction(CPrintAction(u'Напечатать список заявок', -1, self.btnPrint, self.btnPrint))
        self.setModels(self.tblTMKRequests, self.modelTMK, self.selectionModelTMK)

        #self.setModels(self.tblSchedules, self.modelSchedules, self.selectionModelSchedules)
        #self.setModels(self.tblVisitsBySchedules, self.modelVisitsBySchedules, self.selectionModelVisitsBySchedules)

        self.tblTMKRequests.createPopupMenu([
            self.actSetScheduleItem,
            self.actCancelTMK,
            self.actCreateEvent
        ])

        self.edtFilterBegBirthDay.canBeEmpty(True)
        self.edtFilterEndBirthDay.canBeEmpty(True)
        self.cmbFilterCategory.setTable('rbMedicalAidProfile', True)
        self.cmbFilterCategory.setVisible(False)
        self.chkFilterCategory.setVisible(False)
        for status in AllowedStatuses:
            self.cmbFilterStatus.addItem(StatusDict[status], status)
        for urgency in AllowedUrgency:
            if urgency == 4:
                self.cmbFilterUrgency.addItem(u'Все', 4)
            else:
                self.cmbFilterUrgency.addItem(urgencyDict[str(urgency)], urgency)
        # self.connect(QtGui.qApp, SIGNAL('currentClientInfoSAChanged(int)'), self.updateScheduleItemId)
        self.connect(QtGui.qApp, SIGNAL('currentClientInfoTMKChanged(int)'), self.updateScheduleItemId)

        self.filter = {}
        self.filter['personId'] = QtGui.qApp.userId
        self.on_buttonBoxFilterOne_reset()
        self.focusTMKList()
        self.tblTMKRequests.enableColsHide()
        self.tblTMKRequests.enableColsMove()
        self.tblTMKRequests.addAction(self.actCreateEvent)

        self.loadDialogPreferences()
        self.setSortable(self.tblTMKRequests, self.updateTMKList)

        self.textEdit.setOpenLinks(False)
        handler = self.handler
        QObject.connect(self.textEdit, SIGNAL("anchorClicked(const QUrl&)"), handler)

    @pyqtSlot("QUrl")
    def handler(self, url):
        if u'http' not in url.toString():
            print u'При попытке скачать прикрепленный документ возникла ошибка'
        else:
            documentsDir = unicode(QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.DocumentsLocation))
            import os
            listDoc = [u'Документы(*.pdf *.odt *.ods *.doc *.xls *.docx *.xlsx)',
                       u'Изображения(*.png *.tiff *.jpg *.jpeg *.gif *.bmp *.xpm)',
                       u'Текстовые файлы(*.txt)',
                       u'Архивы(*.zip *.7z *.Z *.gz *.bz *.xz *.arj *.rar)',
                       u'Любые файлы(*)']
            file = requests.get(url.toString(), verify=False)
            tempDoc = None
            if file.status_code == 200 and file.headers.get('Content-Disposition'):
                fileName = file.headers.get('Content-Disposition').split('"')[1]
                for doc in listDoc:
                    if '.' in fileName:
                        if fileName.split('.')[1] in doc:
                            tempDoc = doc
                    else:
                        tempDoc = doc
                localFile = QtGui.QFileDialog.getSaveFileName(None,
                                                              u'Сохранить файл',
                                                              os.path.join(documentsDir, fileName.decode('utf-8')),
                                                              tempDoc if tempDoc else u'Любые файлы(*)')
                if localFile:
                    with open(unicode(localFile), 'wb') as stream:  # в случае отказа файл останется?
                        stream.write(file.content)
                        stream.close()

    def setSortingIndicator(self, tbl, col, asc):
        tbl.setSortingEnabled(True)
        tbl.horizontalHeader().setSortIndicator(col, Qt.AscendingOrder if asc else Qt.DescendingOrder)


    def setSortable(self, tbl, update_function=None):
        def on_click(col):
            hs = tbl.horizontalScrollBar().value()
            model = tbl.model()
            sortingCol = model.headerSortingCol.get(col, False)
            model.headerSortingCol = {}
            model.headerSortingCol[col] = not sortingCol
            if update_function:
                update_function()
            else:
                model.loadData()
            self.setSortingIndicator(tbl, col, not sortingCol)
            tbl.horizontalScrollBar().setValue(hs)
        header = tbl.horizontalHeader()
        header.setClickable(True)
        QObject.connect(header, SIGNAL('sectionClicked(int)'), on_click)

    def updateScheduleItemId(self, scheduleItemId):
        if scheduleItemId and self.getCurrentClientId() == QtGui.qApp.currentClientId():
            db = QtGui.qApp.db
            scheduleId = forceRef(db.translate('Schedule_Item', 'id', scheduleItemId, 'master_id'))
            scheduleDate = forceString(db.translate('Schedule', 'id', scheduleId, 'date'))
            personId = forceRef(db.translate('Schedule', 'id', scheduleId, 'person_id'))

            smt = u"""            
SELECT s.value AS spec, pi.value AS post, oo.value AS org, pc_phone.contact AS phone, pc_mail.contact AS mail, SNILS, CONCAT(p.lastName,' ',p.firstName,' ',p.patrName)
  FROM Person p
  LEFT JOIN rbSpeciality_Identification s ON s.master_id=p.speciality_id AND s.system_id = (SELECT id FROM rbAccountingSystem WHERE urn = "urn:oid:1.2.643.5.1.13.13.11.1066")
  LEFT JOIN rbPost_Identification pi ON pi.master_id=p.post_id AND pi.system_id = (SELECT id FROM rbAccountingSystem WHERE urn = "urn:oid:1.2.643.5.1.13.13.99.2.181")
  LEFT JOIN Organisation_Identification oo ON p.org_id = oo.master_id AND oo.deleted=0 AND oo.system_id in (SELECT id FROM rbAccountingSystem `as` WHERE `as`.urn="urn:oid:1.2.643.2.69.1.1.1.64" )
  LEFT JOIN Person_Contact pc_phone ON p.id = pc_phone.master_id AND pc_phone.deleted=0 and pc_phone.contactType_id in (SELECT id FROM rbContactType WHERE (name LIKE "%%рабоч%%") OR (name LIKE "%%мобил%%"))
  LEFT JOIN Person_Contact pc_mail ON p.id = pc_mail.master_id AND pc_mail.deleted=0 and pc_mail.contactType_id in (SELECT id FROM rbContactType WHERE (name LIKE "%%mail%%") OR (name LIKE "%%почт%%"))
  WHERE p.id = %(personId)s;
            """ % {"personId": personId}

            records = db.query(smt)
            if records.first():
                record = records.record()

            if (record and forceString(record.value(0)) and forceString(record.value(1)) and forceString(record.value(2)) and forceString(record.value(3))
                    and forceString(record.value(4)) and forceString(record.value(5)) and forceString(record.value(6))):

                comment = u"Вызов записан на " + scheduleDate
                # dialog = CTMKUpdateStatusDialog(self, True, comment, 3)
                try:
                    # if dialog.exec_():
                    if 1 == 1:
                        db = QtGui.qApp.db
                        table = db.table('TMK_Service')
                        record_ = self.tblTMKRequests.currentItem()
                        status = forceString(record_.value('status'))
                        # comment = dialog.comment
                        self.updateStatus('85dad08c-1eb7-479f-8bf5-66b3ea5e4a02', comment, scheduleItemId, personId)
                        if status == '425a04fc-b21e-4009-bf45-67625abddff6':
                            moveToStage(self, 'e3440aee-7599-47e5-8838-b01cacb487be', False, record)
                        else:
                            moveToStage(self, '8968e933-1ee9-45ff-885e-5e48146384ed', False, record)
                finally:
                    pass
            else:
                textError = ''
                if record:
                    if not forceString(record.value(1)):
                        textError += u'Не указана идентификация для должности исполнителя по справочнику 1.2.643.5.1.13.13.99.2.181 \n'
                    if not forceString(record.value(0)):
                        textError += u'Не указана идентификация для специальности исполнителя по справочнику 1.2.643.5.1.13.13.11.1066 \n'
                    if not forceString(record.value(3)):
                        textError += u'Не указан телефон для исполнителя (находится в карточке врача, тип - "рабочий" или "мобильный") \n'
                    if not forceString(record.value(4)):
                        textError += u'Не указана электронная почта (находится в карточке организации, поле "E-mail") \n'
                    if not forceString(record.value(2)):
                        textError += u'Не указана идентификация для МО - направителя по справочнику 1.2.643.2.69.1.1.1.64 \n'
                    if not forceString(record.value(5)):
                        textError += u'Для врача-консультанта не указан снилс \n'

                    QtGui.QMessageBox.warning(self,
                                              u'Внимание!',
                                              u'"%s"!' % textError,
                                              QtGui.QMessageBox.Ok,
                                              QtGui.QMessageBox.Ok
                                              )
                    return
                else:
                    QtGui.QMessageBox.warning(self,
                                              u'Внимание!',
                                              u'"Не удалось определить врача-консультанта"!' % textError,
                                              QtGui.QMessageBox.Ok,
                                              QtGui.QMessageBox.Ok
                                              )

    @pyqtSignature('int')
    def on_btnPrint_printByTemplate(self, templateId):
        if templateId == -1:
            self.tblTMKRequests.setReportHeader(u'Сервис телемедицины')
            self.tblTMKRequests.setReportDescription(self.getTMKFilterAsText())
            self.tblTMKRequests.printContent()
            self.tblTMKRequests.setFocus(Qt.TabFocusReason)
        else:
            idList = self.tblTMKRequests.model().idList()
            context = CInfoContext()
            TMKInfo = context.getInstance(CTMKInfo, self.tblTMKRequests.currentItemId())
            TMKInfoList = context.getInstance(CTMKInfoList, tuple(idList))
            data = { 'TMKList': TMKInfoList,
                     'TMK'    : TMKInfo }
            QtGui.qApp.call(self, applyTemplate, (self, templateId, data))


    def getTMKFilterAsText(self):
        db = QtGui.qApp.db
        filter  = self.filter
        resList = []
        tmpList = [
            ('lastName',  u'Фамилия', forceString),
            ('firstName', u'Имя', forceString),
            ('patrName',  u'Отчество', forceString),
            ('birthDate', u'Дата рождения', forceString),
            ('begBirthDay', u'Дата рождения с', forceString),
            ('endBirthDay', u'Дата рождения по', forceString),
            ('sex',       u'Пол',           formatSex),
            ('conract',   u'Контакт', forceString),
            ('orgStructureId', u'Подразделение',
                lambda id: forceString(db.translate('OrgStructure', 'id', id, 'name'))),
            ('personId', u'Врач',
                lambda id: forceString(db.translate('vrbPersonWithSpeciality', 'id', id, 'name'))),
            ('statusName', u'Статус', forceString),
            ('note', u'Примечание', forceString),
            ('begCreateDate', u'Дата создания с', forceString),
            ('endCreateDate', u'Дата создания по', forceString),
            ]

        for (x, y, z) in tmpList:
            convertFilterToTextItem(resList, filter, x, y, z)
        return '\n'.join([ ': '.join(item) for item in resList])


    @withWaitCursor
    def updateTMKList(self, posToId=None):
        db = QtGui.qApp.db

        tableTMK = db.table('TMK_Service')
        tableClient = db.table('Client')
        queryTable = tableTMK.innerJoin(tableClient, tableClient['id'].eq(tableTMK['client_id']))

        cond = [
                tableClient['deleted'].eq(0)
               ]

        chkDirection = self.filter.get('chkDirection')
        if chkDirection:
            cond.append(tableTMK['requesterOrganization'].isNotNull())
            cond.append(tableTMK['status'].ne('f2eead71-c257-4f12-827c-cfe86776f1b4'))
        else:
            cond.append(tableTMK['requesterOrganization'].isNull())


        lastName = self.filter.get('lastName')
        if lastName is not None:
            cond.append(tableClient['lastName'].like(lastName))

        firstName = self.filter.get('firstName')
        if firstName is not None:
            cond.append(tableClient['firstName'].like(firstName))

        patrName = self.filter.get('patrName')
        if patrName is not None:
            cond.append(tableClient['patrName'].like(patrName))

        begBirthDay = self.filter.get('begBirthDay', None)
        endBirthDay = self.filter.get('endBirthDay', None)
        if begBirthDay != endBirthDay:
            if begBirthDay:
                cond.append(tableClient['birthDate'].ge(begBirthDay))
            if endBirthDay:
                cond.append(tableClient['birthDate'].le(endBirthDay))
        elif begBirthDay:
            cond.append(tableClient['birthDate'].eq(begBirthDay))

        sex = self.filter.get('sex', None)
        if sex is not None:
            cond.append(tableClient['sex'].eq(sex))

        contact = self.filter.get('contact')
        if contact is not None:
            cond.append(tableTMK['contact'].like(contact))

        orgStructureId = self.filter.get('orgStructureId')

        personId = self.filter.get('personId')
        if personId:
            cond.append(tableTMK['person_id'].eq(personId))

        status = self.filter.get('status')
        if status is not None and status != '0':
            cond.append(tableTMK['status'].eq(status))
        urgency = self.filter.get('urgency')
        if urgency is not None and urgency != '4':
            cond.append(tableTMK['urgency'].eq(urgency))
        
        applicantPhone = self.filter.get('applicantPhone')
        if applicantPhone is not None:
            cond.append(tableTMK['applicantMobilePhone'].like(applicantPhone))

        createDateRange = self.filter.get('createDateRange')
        if createDateRange:
            begDate, endDate = createDateRange
            if begDate:
                cond.append(tableTMK['createDatetime'].ge(begDate))
            if endDate:
                cond.append(tableTMK['createDatetime'].lt(endDate.addDays(1)))

        order = self.getOrderBy()
        idList = db.getDistinctIdList(queryTable,
                                      tableTMK['id'].name(),
                                      cond,
                                      order
                                     )
        self.tblTMKRequests.setIdList(idList, posToId)
        self.lblRecordCount.setText(formatRecordsCount(len(idList)))

    @pyqtSignature('')
    def on_actCreateEvent_triggered(self):
        clientId = self.getCurrentClientId()
        record = self.tblTMKRequests.currentItem()
        if clientId:
            if record:
                personId = forceRef(record.value('person_id'))
            event = QtGui.qApp.db.getRecordEx('TMK_Service', ['event_id','scheduleItem_id','status'],
                                              'id = %s ' % str(self.tblTMKRequests.currentItemId()))
            eventId = forceRef(event.value('event_id')) if event else None
            scheduleItem_id = forceRef(event.value('scheduleItem_id')) if event else None
            status = forceString(event.value('status')) if event else None

            if (not eventId and status != '85dad08c-1eb7-479f-8bf5-66b3ea5e4a02' and not scheduleItem_id):
                return

            actionType = QtGui.qApp.db.getRecordEx('ActionType', 'id', 'flatCode = "tmkDirection" and deleted=0')
            if not actionType:
                QtGui.QMessageBox.critical(self,
                   u'Ошибка',
                   u'Не удалось найти тип действия телемедицины с кодом для отчетов "tmkDirection"',
                   QtGui.QMessageBox.Ok,
                   QtGui.QMessageBox.Ok)
                return
            actionTypeId = forceRef(actionType.value('id')) if event else None
            if clientId and actionType:
                if eventId:
                    try:
                        editEvent(self, eventId)
                    except RuntimeError, e:
                        print 2
                        editEvent(self, eventId)
                else:
                    eventDatetime = None
                    dlg = CPreCreateEventDialog({'widget': self, 'clientId': clientId, 'personId': personId if personId else '', 'eventType_Form': "025"})
                    if dlg.exec_():
                        orgId = dlg.orgId()
                        externalId = dlg.externalId()
                        eventTypeId = dlg.eventTypeId()
                        personId = dlg.personId()
                        eventSetDatetime = dlg.eventSetDate()
                        if not eventDatetime:
                            eventDatetime = dlg.eventDate()
                        weekProfile = dlg.weekProfile()
                        days = dlg.days()
                        assistantId = dlg.assistantId()
                        curatorId = dlg.curatorId()
                        eventSetDate = eventSetDatetime.date() if eventSetDatetime else None
                        eventDate = eventDatetime.date() if eventDatetime else None
                        form = getEventTypeForm(eventTypeId)
                        event = createEvent(self, form, clientId, eventTypeId, orgId, personId, eventDate, eventSetDate, weekProfile, days, externalId, assistantId, curatorId, flagHospitalization = True, actionTypeId = actionTypeId,
                    valueProperties = None, tissueTypeId=None, selectPreviousActions=False, relegateOrgId = None, relegatePersonId = None, planningEventId = None, diagnos = None, financeId = None, protocolQuoteId = None,
                    actionByNewEvent = [], order = 1, actionListToNewEvent = [], result = None, prevEventId = None, typeQueue = -1, docNum=None, relegateInfo = [], plannedEndDate = None, mapJournalInfoTransfer=[],
                    planningActionId = None, emergencyInfo = self.tblTMKRequests.currentItemId())
                        if event:
                            table = QtGui.qApp.db.table('TMK_Service')
                            id = forceRef(self.tblTMKRequests.currentItemId())
                            updates = table.newRecord(['id', 'event_id'])
                            updates.setValue('id', id)
                            # updates.setValue('statusForUpdate', newStatus)
                            # updates.setNull('updateError')
                            updates.setValue('event_id', event)
                            QtGui.qApp.db.updateRecord(table, updates)




    def getOrderBy(self):
        orderBY = u'Client.lastName ASC'
        for key, value in self.modelTMK.headerSortingCol.items():
            if value:
                ASC = u'ASC'
            else:
                ASC = u'DESC'
            if key == 0:
                orderBY = u'Client.lastName %s' % ASC
            elif key == 1:
                orderBY = u'Client.sex %s' % ASC
            elif key == 3:
                orderBY = u'fullName_Requster %s' % ASC
            elif key == 4:
                orderBY = u'status %s' % ASC
            elif key == 7:
                orderBY = u'urgency %s' % ASC
        return orderBY

    def focusTMKList(self):
        self.tblTMKRequests.setFocus(Qt.TabFocusReason)


    def updateClientInfo(self):
        clientId = self.getCurrentClientId()
        if clientId:
            self.txtClientInfoBrowser.setHtml(getClientBanner(clientId))
        else:
            self.txtClientInfoBrowser.setText('')
        QtGui.qApp.setCurrentClientId(clientId)
        # self.loadSchedules(clientId)


    def loadSchedules(self, clientId):
        self.modelSchedules.loadData(clientId)
        self.modelVisitsBySchedules.loadData(clientId)


    def getCurrentClientId(self):
        record = self.tblTMKRequests.currentItem()
        if record:
            return forceRef(record.value('client_id'))
        return None

    def updateStatus(self, newStatus, comment, newScheduleItemId=None, personId = None):
        db = QtGui.qApp.db
        table = db.table('TMK_Service')
        record = self.tblTMKRequests.currentItem()
        if record:
            id = forceRef(record.value('id'))
            currentScheduleItemId = forceRef(record.value('scheduleItem_id'))
            if self.lock('TMK_Service', id):
                try:
                    updates = table.newRecord(['id', 'scheduleItem_id', 'person_id', 'status'])
                    updates.setValue('id', id)
                    # updates.setValue('statusForUpdate', newStatus)
                    # updates.setNull('updateError')
                    updates.setValue('status', newStatus)
                    if newStatus == '85dad08c-1eb7-479f-8bf5-66b3ea5e4a02':
                        updates.setValue('scheduleItem_id', newScheduleItemId)
                        updates.setValue('person_id', personId)
                        updates.setValue('status', newStatus)
                    else:
                        if currentScheduleItemId:
                            freeScheduleItem(self, currentScheduleItemId, forceRef(record.value('client_id')))
                        updates.setNull('scheduleItem_id')
                        updates.setNull('person_id')
                        # updates.setValue('communication', comment)
                    db.updateRecord(table, updates)
                    self.updateTMKList(id)
                finally:
                    self.releaseLock()


    def on_buttonBoxFilter_apply(self):
        def cmbToTristate(val):
            return val-1 if val>0 else None

        self.filter = {}
        if self.chkDirection.isChecked():
            self.filter['chkDirection'] = True
        else:
            self.filter['chkDirection'] = False
        if self.chkFilterLastName.isChecked():
            self.filter['lastName'] = forceStringEx(self.edtFilterLastName.text())
        if self.chkFilterFirstName.isChecked():
            self.filter['firstName'] = forceStringEx(self.edtFilterFirstName.text())
        if self.chkFilterPatrName.isChecked():
            self.filter['patrName'] = forceStringEx(self.edtFilterPatrName.text())
        if self.chkFilterBirthDay.isChecked():
            if self.chkFilterEndBirthDay.isChecked():
                self.filter['begBirthDay'] = self.edtFilterBegBirthDay.date()
                self.filter['endBirthDay'] = self.edtFilterEndBirthDay.date()
            else:
                self.filter['begBirthDay'] = self.filter['endBirthDay'] = self.edtFilterBegBirthDay.date()
        if self.chkFilterSex.isChecked():
            self.filter['sex'] = self.cmbFilterSex.currentIndex()
        if self.chkFilterPerson.isChecked():
            self.filter['personId'] = self.cmbFilterPerson.value()
        self.filter['status'] = AllowedStatuses[self.cmbFilterStatus.currentIndex()]
        self.filter['statusName'] = self.cmbFilterStatus.currentText()
        self.filter['urgency'] = AllowedUrgency[self.cmbFilterUrgency.currentIndex()]
        self.filter['urgencyName'] = self.cmbFilterUrgency.currentText()
        if self.chkFilterExCreateDate.isChecked():
            self.filter['createDateRange'] = self.edtFilterExBegCreateDate.date(), self.edtFilterExEndCreateDate.date()
            self.filter['begCreateDate'] = self.edtFilterExBegCreateDate.date()
            self.filter['endCreateDate'] = self.edtFilterExEndCreateDate.date()
        self.updateTMKList()


    def on_buttonBoxFilter_reset(self):
        self.chkFilterLastName.setChecked(False)
        self.edtFilterLastName.setText('')
        self.chkFilterFirstName.setChecked(False)
        self.edtFilterFirstName.setText('')
        self.chkFilterPatrName.setChecked(False)
        self.edtFilterPatrName.setText('')
        self.chkFilterBirthDay.setChecked(False)
        self.edtFilterBegBirthDay.setDate(QDate())
        self.chkFilterEndBirthDay.setChecked(False)
        self.edtFilterEndBirthDay.setDate(QDate())
        self.chkFilterSex.setChecked(False)
        self.cmbFilterSex.setCurrentIndex(0)
        self.chkFilterPerson.setChecked(False)
        self.cmbFilterPerson.setValue(None)
        self.cmbFilterStatus.setCurrentIndex(0)
        self.cmbFilterUrgency.setCurrentIndex(3)
        self.chkFilterExCreateDate.setChecked(False)
        self.edtFilterExBegCreateDate.setDate(QDate())
        self.edtFilterExEndCreateDate.setDate(QDate())

        self.on_buttonBoxFilter_apply()

    def on_buttonBoxFilterOne_reset(self):
        self.chkFilterLastName.setChecked(False)
        self.edtFilterLastName.setText('')
        self.chkFilterFirstName.setChecked(False)
        self.edtFilterFirstName.setText('')
        self.chkFilterPatrName.setChecked(False)
        self.edtFilterPatrName.setText('')
        self.chkFilterBirthDay.setChecked(False)
        self.edtFilterBegBirthDay.setDate(QDate())
        self.chkFilterEndBirthDay.setChecked(False)
        self.edtFilterEndBirthDay.setDate(QDate())
        self.chkFilterSex.setChecked(False)
        self.cmbFilterSex.setCurrentIndex(0)
        self.chkFilterPerson.setChecked(True)
        self.cmbFilterPerson.setValue(QtGui.qApp.userId)
        self.cmbFilterStatus.setCurrentIndex(0)
        self.cmbFilterUrgency.setCurrentIndex(3)
        self.chkFilterExCreateDate.setChecked(False)
        self.edtFilterExBegCreateDate.setDate(QDate())
        self.edtFilterExEndCreateDate.setDate(QDate())

        self.on_buttonBoxFilter_apply()

    def getInfoText(self, row):
        def formatField(name, value):
            if value is None or len(forceString(value).strip()) == 0:
                return u''
            else:
                return u'<div><b>%s:</b> %s</div>' % (name, forceString(value))

        # def format(clientCache):
        #     clientId  = self.getCurrentClientId()
        #     clientRecord = clientCache.get(clientId)
        #     if clientRecord:
        #         name  = formatName(clientRecord.value('lastName'),
        #                            clientRecord.value('firstName'),
        #                            clientRecord.value('patrName'))
        #         return toVariant(name)
        #     return CCol.invalid

        db = QtGui.qApp.db
        record = db.getRecord('TMK_Service', '*', self.tblTMKRequests.currentItemId())

        # self.clientCache = CTableRecordCache(QtGui.qApp.db, 'Client', ('id', 'lastName', 'firstName', 'patrName', 'birthDate', 'sex'), 300)


        text = ''
        if record:
            text = u'''<style> 
                .header {
                    font: bold large; 
                    margin-bottom: 5px; 
                    margin-left: 20px;
                }
                </style>'''
            text += u'<div class="header"> Цель консультации: '+reasonCodeDict.get(forceString(record.value('reasonCode')))+u'</div><br>'
            if forceInt(record.value('urgency')) in (1, 2):
                text += u'<div class="header"> Срочность: <font color=red>' + urgencyDict.get(forceString(record.value('urgency'))) + u'</font></div><br>'
            else:
                text += u'<div class="header"> Срочность: ' + urgencyDict.get(forceString(record.value('urgency'))) + u'</div><br>'
            text += u'<div style="margin-bottom: 5px; margin-left: 20px;"><b>Номер заявки в ТМК</b><br>   '+forceString(record.value('numberTMK'))+u'</div>'
            text += u'<div style="margin-bottom: 5px; margin-left: 20px;"><b>Наименование заявки</b><br>   '+forceString(record.value('processName'))+u'</div>'
            text += u'<hr>'
            text += u'<div class="header">Данные по направителю</div>'
            if len(forceString(record.value('requesterOrganization'))) > 3:
                text += u'<br>'
                text += formatField(u'Направляющая организация', organisation(forceString(record.value('requesterOrganization'))) if organisation(forceString(record.value('requesterOrganization'))) else forceString(record.value('requesterOrganization')) )
            if forceString(record.value('fullName_Requster')):
                text += u'<br>'
                text += formatField(u'Врач - направитель', forceString(record.value('fullName_Requster')))
            if forceString(record.value('telecom_phone')):
                text += u'<br>'
                text += formatField(u'Телефон врача - направителя', forceString(record.value('telecom_phone')))
            if forceString(record.value('telecom_mail')):
                text += u'<br>'
                text += formatField(u'Почта врача - направителя', forceString(record.value('telecom_mail')))
            text += u'<hr>'


            if len(forceString(record.value('fullName_Performer'))) > 3:
                text += u'<div class="header">Данные по врачу-консультанту</div>'
                text += u'<br>'
                if forceString(record.value('fullName_Performer')):
                    text += formatField(u'Врач - направитель (контактная информация, дата приема)', forceString(record.value('fullName_Performer')))
                    text += u'<br>'
                text += u'<hr>'

            text += u'<div class="header">Данные по заявке</div>'
            text += formatField(u'Первичность', primaryAppealList.get(forceString(record.value('primaryAppeal'))))
            text += formatField(u'Диагноз', forceString(record.value('codeMKB')))
            text += formatField(u'Анамнез', forceString(record.value('anamnesis')))
            if forceString(record.value('files')):
                text += u'<br>'
                text += u'<div class="header">Прикрепленные файлы</div><br><br>'
                files = forceString(record.value('files')).split(',')
                html = ''
                if files > 1:
                    for file in files:
                        if len(file)>5:
                            fileNames = requests.get(file, verify=False)
                            if fileNames.status_code == 200 and fileNames.headers.get('Content-Disposition'):
                                fileName = fileNames.headers.get('Content-Disposition').split('"')[1]
                                if file and fileName:
                                    html += u'<a href="%s" title="всплывающая подсказка">скачать %s</a><br><br>' % (file, fileName.decode('utf-8'))
                            else:
                                html += u'<a href="%s" title="всплывающая подсказка">скачать файл (не удалось определить наименование документа)</a><br><br>' % file
                    text += html
                else:
                    text += u'<a href="%s">файл</a>' % files

            text += u'<hr>'

            if len(forceString(record.value('complaints'))) > 2 :
                text += u'<div class="header">Дополнительная информация</div>'
                text += u'<br><br>' + forceString(record.value('complaints'))
                text += u'<hr>'
            if len(forceString(record.value('communication'))) > 2:
                text += u'<div class="header">Комментарий при отказе обработки заявки</div>'
                text += u'<br><br>' + forceString(record.value('communication'))
                text += u'<hr>'
            return text
##############################################
## SLOTS #####################################

    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelTMK_currentRowChanged(self, current, previous):
        self.updateClientInfo()
        if current.isValid():
            row = current.row()
            self.textEdit.setHtml(self.getInfoText(row))
        else:
            self.textEdit.setText('')



    @pyqtSignature('')
    def on_tblTMKRequests_popupMenuAboutToShow(self):
        record = self.tblTMKRequests.currentItem()
        scheduleItemId = forceRef(record.value('scheduleItem_id')) if record else None
        personId = forceRef(record.value('person_id')) if record else None
        status = forceString(record.value('status')) if record else None
        event = QtGui.qApp.db.getRecordEx('TMK_Service', 'event_id',
                                            'id = %s ' % str(self.tblTMKRequests.currentItemId()))
        eventId = forceRef(event.value('event_id')) if event else None
        # enableUpdateStatus = record is not None and scheduleItemId is None and status in ('1', '3')
        self.status = status
        self.actSetScheduleItem.setEnabled(False)
        self.actCreateEvent.setEnabled(False)
        self.actCancelTMK.setEnabled(False)
        if status == '425a04fc-b21e-4009-bf45-67625abddff6' or status == 'f6917177-a702-4c7f-981a-84552c91addf':
            self.actSetScheduleItem.setEnabled(True)
        self.actCancelTMK.setEnabled(status in ('85dad08c-1eb7-479f-8bf5-66b3ea5e4a02', 'f6917177-a702-4c7f-981a-84552c91addf', '425a04fc-b21e-4009-bf45-67625abddff6'))
        if status == '85dad08c-1eb7-479f-8bf5-66b3ea5e4a02' and personId and scheduleItemId and not eventId:
            self.actCreateEvent.setText(u'Новое обращение')
            self.actCreateEvent.setEnabled(True)
        elif eventId is not None:
            self.actCreateEvent.setText(u'Открыть обращение')
            self.actCreateEvent.setEnabled(True)


    @pyqtSignature('')
    def on_actSetScheduleItem_triggered(self):
        record = self.tblTMKRequests.currentItem()
        if record:
            db = QtGui.qApp.db
            personId       = forceRef(record.value('person_id'))
            orgStructureId = forceRef(db.translate('Person', 'id', personId, 'orgStructure_id'))
            specialityId   = forceRef(db.translate('Person', 'id', personId, 'speciality_id'))
            begDate        = forceDate(record.value('date'))
            QtGui.qApp.setupResourcesDock(orgStructureId, specialityId, personId, begDate, CSchedule.atAmbulance)
        #     QtGui.qApp.setupDocFreeQueue(orgStructureId, specialityId, personId, begDate)


    @pyqtSignature('')
    def on_actCancelTMK_triggered(self):
        text = u'Заявка отменена МО'

        if self.status == '85dad08c-1eb7-479f-8bf5-66b3ea5e4a02': # отклоняет врач
            text = u'Заявка отменена врачем-консультантом'
            newStatus = 'f6917177-a702-4c7f-981a-84552c91addf'
        elif self.status == '425a04fc-b21e-4009-bf45-67625abddff6': # отклоняем из листа ожидания
            newStatus = '764f55f2-2c0e-43e3-81ce-3e5626682322'
        else:
            newStatus = '764f55f2-2c0e-43e3-81ce-3e5626682322'
        dialog = CTMKUpdateStatusDialog(self, False, text, self.status)
        try:
            if dialog.exec_():
                text = dialog.comment
                if newStatus == 'f6917177-a702-4c7f-981a-84552c91addf':
                    result = moveToStage(self, '239e8005-462b-437d-ac33-2a1134187852', text)
                elif newStatus == '764f55f2-2c0e-43e3-81ce-3e5626682322' and self.status == '425a04fc-b21e-4009-bf45-67625abddff6':
                    result = moveToStage(self, 'b9becd83-1b5b-4c23-95c7-d545466b2dbb', text)
                else:
                    result = moveToStage(self, '0c1912f0-947b-4c84-8e5d-35094847c3b7', text)
                if result == 1:
                    self.updateStatus(newStatus, dialog.comment)
        finally:
            dialog.deleteLater()



    @pyqtSignature('bool')
    def on_chkFilterBirthDay_toggled(self, value):
        self.edtFilterEndBirthDay.setEnabled(value and self.chkFilterEndBirthDay.isChecked())


    @pyqtSignature('QAbstractButton*')
    def on_buttonBoxFilter_clicked(self, button):
        buttonCode = self.buttonBoxFilter.standardButton(button)
        if buttonCode == QtGui.QDialogButtonBox.Apply:
            self.on_buttonBoxFilter_apply()
        elif buttonCode == QtGui.QDialogButtonBox.Reset:
            self.on_buttonBoxFilter_reset()
        self.focusTMKList()
        self.updateClientInfo()


    def closeEvent(self, event):
        self.saveDialogPreferences()
        QtGui.QScrollArea.closeEvent(self, event)


class CTMKModel(CTableModel):

    class CLocClientColumn(CCol):
        def __init__(self, title, fields, defaultWidth, clientCache):
            CCol.__init__(self, title, fields, defaultWidth, 'l')
            self.clientCache = clientCache

        def format(self, values):
            val = values[0]
            clientId  = forceRef(val)
            clientRecord = self.clientCache.get(clientId)
            if clientRecord:
                name  = formatName(clientRecord.value('lastName'),
                                   clientRecord.value('firstName'),
                                   clientRecord.value('patrName'))
                return toVariant(name)
            return CCol.invalid


    class CLocClientBirthDateColumn(CCol):
        def __init__(self, title, fields, defaultWidth, clientCache):
            CCol.__init__(self, title, fields, defaultWidth, 'l')
            self.clientCache = clientCache

        def format(self, values):
            val = values[0]
            clientId  = forceRef(val)
            clientRecord = self.clientCache.get(clientId)
            if clientRecord:
                return toVariant(forceString(clientRecord.value('birthDate')))
            return CCol.invalid


    class CLocClientSexColumn(CCol):
        def __init__(self, title, fields, defaultWidth, clientCache):
            CCol.__init__(self, title, fields, defaultWidth, 'l')
            self.clientCache = clientCache

        def format(self, values):
            val = values[0]
            clientId  = forceRef(val)
            clientRecord = self.clientCache.get(clientId)
            if clientRecord:
                return toVariant(formatSex(clientRecord.value('sex')))
            return CCol.invalid


    class CStatusCol(CCol):
        def __init__(self, title, fields, defaultWidth):
            CCol.__init__(self, title, fields, defaultWidth, 'l')

        def format(self, values):
            status  = forceString(values[0])
            statusText = StatusDict.get(status)
            if statusText:
                return toVariant(statusText)
            return CCol.invalid

    class CReasonCol(CCol):
        def __init__(self, title, fields, defaultWidth):
            CCol.__init__(self, title, fields, defaultWidth, 'l')

        def format(self, values):
            status  = forceString(values[0])
            statusText = reasonCodeDict.get(status)
            if statusText:
                return toVariant(statusText)
            return CCol.invalid

    class CUrgencyCol(CCol):
        def __init__(self, title, fields, defaultWidth):
            CCol.__init__(self, title, fields, defaultWidth, 'l')

        def format(self, values):
            urgency  = forceString(values[0])
            statusText = urgencyDict.get(urgency)
            if statusText:
                return toVariant(statusText)
            return CCol.invalid

    class CReqOrgCol(CCol):
        def __init__(self, title, fields, defaultWidth):
            CCol.__init__(self, title, fields, defaultWidth, 'l')

        def format(self, values):
            status  = forceString(values[0])
            statusText = organisation(forceString(status))
            if statusText:
                return toVariant(statusText)
            else:
                return toVariant(forceString(status))
            return CCol.invalid

    class CApplicantCol(CCol):
        def __init__(self, title, fields, defaultWidth):
            CCol.__init__(self, title, fields, defaultWidth, 'l')

        def format(self, values):
            lastName = forceString(values[0])
            firstName = forceString(values[1])
            patrName = forceString(values[2])
            return toVariant(formatName(lastName, firstName, patrName))

    class CPrimaryCol(CCol):
        def __init__(self, title, fields, defaultWidth):
            CCol.__init__(self, title, fields, defaultWidth, 'l')

        def format(self, values):
            id = forceString(values[0])
            return toVariant(u'первично' if id == '1' else u'повторно')

    class CProfileCol(CCol):
        def __init__(self, title, fields, defaultWidth):
            CCol.__init__(self, title, fields, defaultWidth, 'l')

        def format(self, values):
            fedProf  = forceRef(values[0])
            clientRecord = QtGui.qApp.db.getRecordEx('rbMedicalAidProfile', 'name', 'federalCode = %s ' % fedProf)
            if clientRecord:
                return toVariant(forceString(clientRecord.value('name')))
            return CCol.invalid

    class CScheduleItemCol(CCol):
        def __init__(self, title, fields, defaultWidth):
            CCol.__init__(self, title, fields, defaultWidth, 'l')

            db = QtGui.qApp.db
            tableScheduleItem = db.table('Schedule_Item')
            tableSchedule = db.table('Schedule')
            tablePerson = db.table('vrbPersonWithSpeciality')
            tableOrgStructure = db.table('OrgStructure')
            cols = ['Schedule_Item.client_id',
                    'Schedule_Item.time',
                    'Schedule.date',
                    'OrgStructure.name AS osName',
                    'vrbPersonWithSpeciality.name AS personName',
                    '(Schedule_Item.deleted OR Schedule.deleted) AS deleted'
                   ]
            table = tableScheduleItem.innerJoin(tableSchedule, tableSchedule['id'].eq(tableScheduleItem['master_id']))
            table = table.innerJoin(tablePerson, tablePerson['id'].eq(tableSchedule['person_id']))
            table = table.innerJoin(tableOrgStructure, tableOrgStructure['id'].eq(tablePerson['orgStructure_id']))

            self.recordCache = CTableRecordCache(db, table, cols)


        def invalidateRecordsCache(self):
            self.recordCache.invalidate()


        def format(self, values):
            clientId = forceRef(values[0])
            scheduleItemId = forceRef(values[1])
            record = self.recordCache.get(scheduleItemId)
            if record and not forceBool(record.value('deleted')) and clientId == forceRef(record.value('client_id')):
                date = forceDate(record.value('date'))
                time = forceTime(record.value('time'))
                personName = forceString(record.value('personName'))
#                osName = forceString(record.value('osName'))
                return toVariant(forceString(QDateTime(date, time))+' '+personName)
            return QVariant()


    def __init__(self, parent):
        self.clientCache = CTableRecordCache(QtGui.qApp.db, 'Client', ('id', 'lastName', 'firstName', 'patrName', 'birthDate', 'sex'), 300)
        CTableModel.__init__(self, parent)
        self.addColumn(self.CLocClientColumn( u'Ф.И.О.', ('client_id',), 60, self.clientCache))
        # self.addColumn(self.CLocClientBirthDateColumn(u'Дата рожд.', ('client_id',), 20, self.clientCache))
        self.addColumn(self.CLocClientSexColumn(u'Пол', ('client_id',), 5, self.clientCache))
        self.addColumn(self.CReqOrgCol(u'Направляющее МО', ('requesterOrganization',), 20))
        self.addColumn(CTextCol(u'Направитель', ('fullName_Requster',), 20))
        self.addColumn(self.CStatusCol(u'Статус', ('status',), 30))
        self.addColumn(self.CScheduleItemCol(u'Талон на приём к врачу', ('client_id', 'scheduleItem_id',), 50))
        self.addColumn(CRefBookCol(u'Врач', ('person_id',), 'vrbPerson', 30))
        self.addColumn(self.CUrgencyCol(u'Срочность', ('urgency',), 20))
        self.addColumn(CTextCol(u'Диагноз', ('codeMKB',), 20))
        self.addColumn(self.CReasonCol(u'Цель обращения', ('reasonCode',), 20))
        self.addColumn(self.CPrimaryCol(u'Первичность', ('primaryAppeal',), 20))
        self.addColumn(self.CProfileCol(u'Профиль МП', ('category',), 20))
        self.setTable('TMK_Service')
        self.headerSortingCol = {}

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        column = index.column()
        row = index.row()
        record = self.getRecordByRow(row)
        if role == Qt.BackgroundColorRole and column == 4:
            if StatusDict.get(forceString(record.value('status'))) == u'Отклонено':
                return toVariant(QtGui.QColor(255, 36, 0))
            elif u'готово' in StatusDict.get(forceString(record.value('status'))):
                return toVariant(QtGui.QColor(28, 211, 162))
            else:
                return toVariant(QtGui.QColor(0, 255, 255))
        return CTableModel.data(self, index, role)
        #
        # (col_, values_) = self.getRecordValues(column, row)
        # if role == Qt.DisplayRole: ### or role == Qt.EditRole:
        #     (col, values) = self.getRecordValues(column, row)
        #     return col.format(values)
        # elif role == Qt.TextAlignmentRole:
        #    col = self._cols[column]
        #    return col.alignment()
        # elif role == Qt.FontRole and 'CStatusCol' in str(col_):
        #     return QVariant(QtGui.QBrush(QtGui.QColor(255, 94, 94)))
        # elif role == Qt.CheckStateRole:
        #     (col, values) = self.getRecordValues(column, row)
        #     return col.checked(values)
        # elif role == Qt.ForegroundRole:
        #     (col, values) = self.getRecordValues(column, row)
        #     return col.getForegroundColor(values)
        # elif role == Qt.BackgroundRole:
        #     (col, values) = self.getRecordValues(column, row)
        #     return col.getBackgroundColor(values)
        # return QVariant()

    def invalidateRecordsCache(self):
        self.clientCache.invalidate()
        CTableModel.invalidateRecordsCache(self)


class CTMKUpdateStatusDialog(CDialogBase, Ui_HomeCallRequestUpdateStatusDialog):
    def __init__(self, parent, confirm, defaultComment, status):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        if confirm:
            # self.allowedStatuses = [u'85dad08c-1eb7-479f-8bf5-66b3ea5e4a02']
            self.cmbStatus.setVisible(False)
            self.label.setVisible(False)
            self.setWindowTitle(u"Подтверждение заявки")
            self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        else:
            # a = self.cmbStatus.currentIndex()
            self.cmbStatus.setVisible(False)
            self.label.setVisible(False)
            self.setWindowTitle(u"Отмена заявки")
        self.cmbStatus.addItem('123', status)
        self.edtComment.setPlainText(defaultComment)

    def accept(self):
        self.status = forceString(self.cmbStatus.itemData(self.cmbStatus.currentIndex()))
        self.comment = forceString(self.edtComment.toPlainText())
        QtGui.QDialog.accept(self)
