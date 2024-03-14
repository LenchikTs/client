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
##
## Работа с отложенной записью
##
#############################################################################


from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDate, QDateTime, QMetaObject, QVariant, pyqtSignature, SIGNAL, QObject

from Timeline.Schedule import freeScheduleItem
from library.database                  import CTableRecordCache
from library.DialogBase                import CDialogBase, CConstructHelperMixin
from library.PreferencesMixin          import CDialogPreferencesMixin
from library.PrintInfo                 import CInfoContext
from library.PrintTemplates            import applyTemplate, CPrintAction, getPrintTemplates
from library.RecordLock                import CRecordLockMixin
from library.TableModel                import CDateCol, CDesignationCol, CTextCol, CDateTimeCol, CCol, CRefBookCol, CTableModel
from library.Utils                     import formatName, toVariant, forceString, withWaitCursor, forceRef, forceTime, forceBool, formatRecordsCount, forceDate, forceStringEx, formatSex
from Orgs.Utils                        import getOrgStructureDescendants
from Registry.RegistryWindow           import CSchedulesModel, CVisitsBySchedulesModel, convertFilterToTextItem
from Registry.Utils                    import getClientBanner
from Timeline.Schedule                 import CSchedule

from Ui_HomeCallRequestsWindow import Ui_HomeCallRequestsWindow
from Ui_HomeCallRequestUpdateStatusDialog import Ui_HomeCallRequestUpdateStatusDialog

StatusDict = {
    '1': u"Заявка зарегистрирована",
    '2': u"Заявка не подтверждена",
    '3': u"Заявка подтверждена",
    '4': u"Заявка отменена пациентом",
    '5': u"Заявка отменена МО",
    '6': u"Услуга оказана",
    '7': u"Услуга не оказана по другим причинам",
}

AllowedStatuses = ['1', '2', '3', '4', '5', '6', '7']

class CHomeCallRequestsWindow(QtGui.QScrollArea, Ui_HomeCallRequestsWindow, CDialogPreferencesMixin, CConstructHelperMixin, CRecordLockMixin):
    def __init__(self, parent):
        QtGui.QScrollArea.__init__(self, parent)
        CRecordLockMixin.__init__(self)
        self.addModels('HomeCallRequests', CHomeCallRequestModel(self))
        self.addModels('Schedules', CSchedulesModel(self))
        self.addModels('VisitsBySchedules', CVisitsBySchedulesModel(self))
        self.addObject('actSetScheduleItem', QtGui.QAction(u'Подобрать номерок', self))
        self.addObject('actCancelHomeCall', QtGui.QAction(u'Отменить', self))

        self.setObjectName('HomeCallRequestWindow')
        self.internal = QtGui.QWidget(self)
        self.setWidget(self.internal)
        self.setupUi(self.internal)

        self.setWindowTitle(self.internal.windowTitle())
        self.setWidgetResizable(True)
        QMetaObject.connectSlotsByName(self) # т.к. в setupUi параметр не self
        printTemplates = getPrintTemplates(['homeCallRequestList'])
        if not printTemplates:
            self.btnPrint.setId(-1)
        else:
            for template in printTemplates:
                action = CPrintAction(template.name, template.id, self.btnPrint, self.btnPrint)
                self.btnPrint.addAction(action)
            self.btnPrint.menu().addSeparator()
            self.btnPrint.addAction(CPrintAction(u'Напечатать список заявок', -1, self.btnPrint, self.btnPrint))
        self.setModels(self.tblHomeCallRequests, self.modelHomeCallRequests, self.selectionModelHomeCallRequests)

        #self.setModels(self.tblSchedules, self.modelSchedules, self.selectionModelSchedules)
        #self.setModels(self.tblVisitsBySchedules, self.modelVisitsBySchedules, self.selectionModelVisitsBySchedules)
        self.tabBeforeRecord.setVisible(False)
        self.tblHomeCallRequests.createPopupMenu([
            self.actSetScheduleItem,
            self.actCancelHomeCall
        ])

        self.edtFilterBegBirthDay.canBeEmpty(True)
        self.edtFilterEndBirthDay.canBeEmpty(True)
        self.cmbFilterSpeciality.setTable('rbSpeciality', True)
        for status in AllowedStatuses:
            self.cmbFilterStatus.addItem(StatusDict[status], status)

        self.connect(QtGui.qApp, SIGNAL('currentClientInfoSAChanged(int)'), self.updateScheduleItemId)
        self.connect(QtGui.qApp, SIGNAL('currentClientInfoJLWChanged(int)'), self.updateScheduleItemId)

        self.filter = {}
        self.on_buttonBoxFilter_reset()
        # Мешает активации/деактивации окна в CMdiArea (s11main.CS11MainWindow.centralWidget)
        # self.focusHomeCallRequestsList()
        self.tblHomeCallRequests.enableColsHide()
        self.tblHomeCallRequests.enableColsMove()
        self.tblSchedules.enableColsHide()
        self.tblSchedules.enableColsMove()
        self.tblVisitsBySchedules.enableColsHide()
        self.tblVisitsBySchedules.enableColsMove()
        self.loadDialogPreferences()
        self.setSortable(self.tblHomeCallRequests, self.updateHomeCallRequestsList)


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
        if scheduleItemId:
            db = QtGui.qApp.db
            scheduleId = forceRef(db.translate('Schedule_Item', 'id', scheduleItemId, 'master_id'))
            scheduleDate = forceString(db.translate('Schedule', 'id', scheduleId, 'date'))
            comment = u"Вызов записан на " + scheduleDate
            dialog = CHomeCallRequestUpdateStatusDialog(self, True, comment)
            try:
                if dialog.exec_():
                    comment = dialog.comment
            finally:
                dialog.deleteLater()
            self.updateStatus('3', comment, scheduleItemId)

    @pyqtSignature('int')
    def on_btnPrint_printByTemplate(self, templateId):
        if templateId == -1:
            self.tblHomeCallRequests.setReportHeader(u'Журнал вызова врача на дом')
            self.tblHomeCallRequests.setReportDescription(self.getHomeCallRequestFilterAsText())
            self.tblHomeCallRequests.printContent()
            self.tblHomeCallRequests.setFocus(Qt.TabFocusReason)
        else:
            idList = self.tblHomeCallRequests.model().idList()
            context = CInfoContext()
            homeCallRequestInfo = context.getInstance(CHomeCallRequestInfo, self.tblHomeCallRequests.currentItemId())
            homeCallRequestInfoList = context.getInstance(CHomeCallRequestInfoList, tuple(idList))
            data = { 'homeCallRequestList': homeCallRequestInfoList,
                     'homeCallRequest'    : homeCallRequestInfo }
            QtGui.qApp.call(self, applyTemplate, (self, templateId, data))


    def getHomeCallRequestFilterAsText(self):
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
    def updateHomeCallRequestsList(self, posToId=None):
        db = QtGui.qApp.db

        tableHomeCallRequest = db.table('HomeCallRequest')
        tableClient = db.table('Client')
        tableOrgStructure = db.table('OrgStructure')
        tableSpeciality = db.table('rbSpeciality')
        tablePerson = db.table('vrbPerson')
        tableScheduleItem = db.table('Schedule_Item')
        tableSchedule = db.table('Schedule')
        queryTable = tableHomeCallRequest.innerJoin(tableClient, tableClient['id'].eq(tableHomeCallRequest['client_id']))
        queryTable = queryTable.leftJoin(tablePerson, tablePerson['id'].eq(tableHomeCallRequest['person_id']))
        queryTable = queryTable.leftJoin(tableOrgStructure, tableOrgStructure['id'].eq(tablePerson['orgStructure_id']))
        queryTable = queryTable.leftJoin(tableSpeciality, tableSpeciality['id'].eq(tablePerson['speciality_id']))
        queryTable = queryTable.leftJoin(tableScheduleItem, tableScheduleItem['id'].eq(tableHomeCallRequest['scheduleItem_id']))
        queryTable = queryTable.leftJoin(tableSchedule, tableSchedule['id'].eq(tableScheduleItem['master_id']))

        cond = [tableHomeCallRequest['deleted'].eq(0),
                tableClient['deleted'].eq(0),
                db.joinOr([tableHomeCallRequest['statusForUpdate'].isNull(), tableHomeCallRequest['updateError'].isNotNull()])
               ]

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
            cond.append(tableHomeCallRequest['contact'].like(contact))

        orgStructureId = self.filter.get('orgStructureId')
        if orgStructureId:
            cond.append(tablePerson['orgStructure_id'].inlist(getOrgStructureDescendants(orgStructureId)))

        specialityId = self.filter.get('specialityId')
        if specialityId:
            cond.append(tablePerson['speciality_id'].eq(specialityId))

        personId = self.filter.get('personId')
        if personId:
            cond.append(tableHomeCallRequest['person_id'].eq(personId))

        status = self.filter.get('status')
        if status is not None:
            cond.append(tableHomeCallRequest['status'].eq(status))

        applicantPhone = self.filter.get('applicantPhone')
        if applicantPhone is not None:
            cond.append(tableHomeCallRequest['applicantMobilePhone'].like(applicantPhone))

        createDateRange = self.filter.get('createDateRange')
        if createDateRange:
            begDate, endDate = createDateRange
            if begDate:
                cond.append(tableHomeCallRequest['createDatetime'].ge(begDate))
            if endDate:
                cond.append(tableHomeCallRequest['createDatetime'].lt(endDate.addDays(1)))

        order = self.getOrderBy()
        idList = db.getDistinctIdList(queryTable,
                                      tableHomeCallRequest['id'].name(),
                                      cond,
                                      order
                                     )
        self.tblHomeCallRequests.setIdList(idList, posToId)
        self.lblRecordCount.setText(formatRecordsCount(len(idList)))


    def getOrderBy(self):
        orderBY = u'Client.lastName ASC'
        for key, value in self.modelHomeCallRequests.headerSortingCol.items():
            if value:
                ASC = u'ASC'
            else:
                ASC = u'DESC'
            if key == 0:
                orderBY = u'Client.lastName %s' % ASC
            elif key == 1:
                orderBY = u'Client.birthDate %s' % ASC
            elif key == 2:
                orderBY = u'Client.sex %s' % ASC
            elif key == 3:
                orderBY = u'HomeCallRequest.applicantLastName %s' % ASC
            elif key == 4:
                orderBY = u'HomeCallRequest.applicantMobilePhone %s' % ASC
            elif key == 5:
                orderBY = u'HomeCallRequest.DATE %s' % ASC
            elif key == 6:
                orderBY = u'OrgStructure.name %s' % ASC
            elif key == 7:
                orderBY = u'vrbPerson.name %s' % ASC
            elif key == 8:
                orderBY = u'HomeCallRequest.status %s' % ASC
            elif key == 9:
                orderBY = u'Schedule.date %s, Schedule_Item.time %s' % (ASC, ASC)
            elif key == 10:
                orderBY = u'HomeCallRequest.reason %s' % ASC
            elif key == 11:
                orderBY = u'HomeCallRequest.comment %s' % ASC
            elif key == 12:
                orderBY = u'HomeCallRequest.createDatetime %s' % ASC
        return orderBY


    def focusHomeCallRequestsList(self):
        self.tblHomeCallRequests.setFocus(Qt.TabFocusReason)


    def update(self):
        self.updateHomeCallRequestsList(self.tblHomeCallRequests.currentItemId())
        # super(CHomeCallRequestsWindow, self).update()


    def updateClientInfo(self):
        clientId = self.getCurrentClientId()
        if clientId:
            self.txtClientInfoBrowser.setHtml(getClientBanner(clientId))
        else:
            self.txtClientInfoBrowser.setText('')
        QtGui.qApp.setCurrentClientId(clientId)
        self.loadSchedules(clientId)


    def loadSchedules(self, clientId):
        self.modelSchedules.loadData(clientId)
        self.modelVisitsBySchedules.loadData(clientId)


    def getCurrentClientId(self):
        record = self.tblHomeCallRequests.currentItem()
        if record:
            return forceRef(record.value('client_id'))
        return None


    def updateStatus(self, newStatus, comment, newScheduleItemId=None):
        db = QtGui.qApp.db
        table = db.table('HomeCallRequest')
        record = self.tblHomeCallRequests.currentItem()
        if record:
            id = forceRef(record.value('id'))
            currentScheduleItemId = forceRef(record.value('scheduleItem_id'))
            if self.lock('HomeCallRequest', id):
                try:
                    updates = table.newRecord(['id', 'scheduleItem_id', 'statusForUpdate', 'statusChangeNote', 'updateError'])
                    updates.setValue('id', id)
                    updates.setValue('statusForUpdate', newStatus)
                    updates.setValue('statusChangeNote', comment)
                    updates.setNull('updateError')
                    if newStatus == '3':
                        updates.setValue('scheduleItem_id', newScheduleItemId)
                    else:
                        if currentScheduleItemId:
                            freeScheduleItem(self, currentScheduleItemId, forceRef(record.value('client_id')))
                        updates.setNull('scheduleItem_id')
                    db.updateRecord(table, updates)
                    self.updateHomeCallRequestsList(id)
                finally:
                    self.releaseLock()


    def on_buttonBoxFilter_apply(self):
        def cmbToTristate(val):
            return val-1 if val>0 else None

        self.filter = {}
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
        if self.chkFilterOrgStructure.isChecked():
            self.filter['orgStructureId'] = self.cmbFilterOrgStructure.value()
        if self.chkFilterPerson.isChecked():
            self.filter['personId'] = self.cmbFilterPerson.value()
        if self.chkFilterApplicantPhone.isChecked():
            self.filter['applicantPhone'] = forceStringEx(self.edtFilterApplicantPhone.text())
        self.filter['status'] = AllowedStatuses[self.cmbFilterStatus.currentIndex()]
        self.filter['statusName'] = self.cmbFilterStatus.currentText()
        if self.chkFilterExCreateDate.isChecked():
            self.filter['createDateRange'] = self.edtFilterExBegCreateDate.date(), self.edtFilterExEndCreateDate.date()
            self.filter['begCreateDate'] = self.edtFilterExBegCreateDate.date()
            self.filter['endCreateDate'] = self.edtFilterExEndCreateDate.date()
        self.updateHomeCallRequestsList()


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
        self.chkFilterApplicantPhone.setChecked(False)
        self.edtFilterApplicantPhone.setText('')
        self.chkFilterOrgStructure.setChecked(False)
        self.cmbFilterOrgStructure.setValue(None)
        self.chkFilterSpeciality.setChecked(False)
        self.cmbFilterSpeciality.setValue(None)
        self.chkFilterPerson.setChecked(False)
        self.cmbFilterPerson.setValue(None)
        self.cmbFilterStatus.setCurrentIndex(0)
        self.chkFilterExCreateDate.setChecked(False)
        self.edtFilterExBegCreateDate.setDate(QDate())
        self.edtFilterExEndCreateDate.setDate(QDate())

        self.on_buttonBoxFilter_apply()


##############################################
## SLOTS #####################################

    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelHomeCallRequests_currentRowChanged(self, current, previous):
        self.updateClientInfo()


    @pyqtSignature('')
    def on_tblHomeCallRequests_popupMenuAboutToShow(self):
        record = self.tblHomeCallRequests.currentItem()
        scheduleItemId = forceRef(record.value('scheduleItem_id')) if record else None
        status = forceString(record.value('status')) if record else None
        enableUpdateStatus = record is not None and scheduleItemId is None and status == '1'
        enableCancel = record is not None and status in ('1', '3')
        self.actSetScheduleItem.setEnabled(enableUpdateStatus)
        self.actCancelHomeCall.setEnabled(enableCancel)


    @pyqtSignature('')
    def on_actSetScheduleItem_triggered(self):
        record = self.tblHomeCallRequests.currentItem()
        if record:
            db = QtGui.qApp.db
            personId       = forceRef(record.value('person_id'))
            orgStructureId = forceRef(db.translate('Person', 'id', personId, 'orgStructure_id'))
            specialityId   = forceRef(db.translate('Person', 'id', personId, 'speciality_id'))
            begDate        = forceDate(record.value('date'))
            QtGui.qApp.setupResourcesDock(orgStructureId, specialityId, personId, begDate, CSchedule.atHome)
            QtGui.qApp.setupDocFreeQueue(CSchedule.atHome, orgStructureId, specialityId, personId, begDate)


    @pyqtSignature('')
    def on_actCancelHomeCall_triggered(self):
        dialog = CHomeCallRequestUpdateStatusDialog(self, False, u"Заявка отменена МО")
        try:
            if dialog.exec_():
                self.updateStatus(dialog.status, dialog.comment)
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
        self.focusHomeCallRequestsList()
        self.updateClientInfo()


    def closeEvent(self, event):
        self.saveDialogPreferences()
        QtGui.QScrollArea.closeEvent(self, event)



class CHomeCallRequestModel(CTableModel):

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


    class CApplicantCol(CCol):
        def __init__(self, title, fields, defaultWidth):
            CCol.__init__(self, title, fields, defaultWidth, 'l')

        def format(self, values):
            lastName = forceString(values[0])
            firstName = forceString(values[1])
            patrName = forceString(values[2])
            return toVariant(formatName(lastName, firstName, patrName))


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
        self.addColumn(self.CLocClientBirthDateColumn(u'Дата рожд.', ('client_id',), 20, self.clientCache))
        self.addColumn(self.CLocClientSexColumn(u'Пол', ('client_id',), 5, self.clientCache))
        self.addColumn(self.CApplicantCol(u'Заявитель', ('applicantLastName', 'applicantFirstName', 'applicantMiddleName'), 20))
        self.addColumn(CTextCol(u'Телефон', ('applicantMobilePhone',), 20))
        self.addColumn(CDateCol(u'Дата', ('date',), 10))
        self.addColumn(CDesignationCol(u'Участок', ('orgStructure_id',), ('OrgStructure', 'name'), 10))
        self.addColumn(CRefBookCol(u'Врач', ('person_id',), 'vrbPerson', 30))
        self.addColumn(self.CStatusCol(u'Статус', ('status',), 30))
        self.addColumn(self.CScheduleItemCol(u'Талон на приём к врачу', ('client_id', 'scheduleItem_id', ), 50))
        self.addColumn(CTextCol(u'Причина вызова', ('reason', ), 10))
        self.addColumn(CTextCol(u'Комментарий', ('comment', ), 10))
        self.addColumn(CDateTimeCol(u'Создано', ('createDatetime',), 20))
        self.setTable('HomeCallRequest')
        self.headerSortingCol = {}


    def invalidateRecordsCache(self):
        self.clientCache.invalidate()
        CTableModel.invalidateRecordsCache(self)


class CHomeCallRequestUpdateStatusDialog(CDialogBase, Ui_HomeCallRequestUpdateStatusDialog):
    def __init__(self, parent, confirm, defaultComment):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
        record = parent.tblHomeCallRequests.currentItem()
        status = forceString(record.value('status')) if record else None
        if confirm:
            self.allowedStatuses = ['3']
            self.cmbStatus.setEnabled(False)
            self.setWindowTitle(u"Подтверждение заявки")
            self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        else:
            if status != '1':
                self.allowedStatuses = ['5', '7']
            else:
                self.allowedStatuses = ['2']
            self.setWindowTitle(u"Отмена заявки")
        for status in self.allowedStatuses:
            self.cmbStatus.addItem(StatusDict[status], status)
        self.cmbStatus.setCurrentIndex(0)
        self.edtComment.setPlainText(defaultComment)

    def accept(self):
        self.status = forceString(self.cmbStatus.itemData(self.cmbStatus.currentIndex()))
        self.comment = forceString(self.edtComment.toPlainText())
        QtGui.QDialog.accept(self)
