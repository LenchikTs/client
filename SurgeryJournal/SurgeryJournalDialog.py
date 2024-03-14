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

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QVariant, pyqtSignature, QDate, QDateTime
from library.TableModel import CTableModel, CDateTimeCol, CRefBookCol, CTextCol
from library.DialogBase import CDialogBase
from library.Utils      import (
                                forceDate,
                                forceInt,
                                forceRef,
                                forceString,
                                formatShortNameInt,
                                formatRecordsCount,
                                formatSex,
                                trim,
                               )
from Events.Action         import CAction
from Events.ActionInfo     import CActionInfoListEx
from Events.EditDispatcher import getEventFormClass
from Events.ActionStatus   import CActionStatus
from Events.ActionEditDialog  import CActionEditDialog
from Events.ActionServiceType import CActionServiceType
from Orgs.Utils               import getPersonInfo
from Registry.Utils           import canChangePayStatusAdditional, canEditOtherpeopleAction
from Registry.ClientEditDialog  import CClientEditDialog
from Reports.ReportBase         import CReportBase, createTable
from Reports.ReportView         import CReportViewDialog
from Reports.Utils              import dateRangeAsStr
from library.PrintInfo          import CInfoContext
from library.PrintTemplates     import (
                                        getPrintButton,
                                        applyTemplate,
                                        CPrintAction,
                                        getPrintTemplates,
                                       )
from library.crbcombobox        import CRBComboBox, CRBModelDataCache
from library.database           import CTableRecordCache
from Resources.JobTicketChooser import getJobTicketAsText
from Users.Rights        import (urSurgeryJournalReadEvent,
                                 urSurgeryJournalEditEvent,
                                 urSurgeryJournalReadClientInfo,
                                 urSurgeryJournalEditClientInfo,
                                 urSurgeryJournalReadAction,
                                 urSurgeryJournalEditAction,
                                )

from Ui_SurgeryJournalDialog import Ui_SurgeryJournalDialog


ActionPropertyTableList = {u'Contract'              : u'Contract',
                           u'rbFinance'             : u'rbFinance',
                           u'HospitalBed'           : u'HospitalBed',
                           u'rbHospitalBedProfile'  : u'rbHospitalBedProfile',
                           u'Organisation'          : u'Organisation',
                           u'OrgStructure'          : u'OrgStructure',
                           u'OrgStructurePlacements': u'OrgStructure_Placement',
                           u'Person'                : u'vrbPersonWithSpeciality',
                           u'rbSpeciality'          : u'rbSpeciality'
                           }


class CSurgeryJournalDialog(CDialogBase, Ui_SurgeryJournalDialog):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.addModels('Journal',  CJournalModel(self))
        self.addModels('Canceled', CCanceledModel(self))
        self.addModels('Plan',     CPlanModel(self))
        self.addObject('btnPrint', getPrintButton(self, ''))
        self.addObject('btnApplyFilter', QtGui.QPushButton(u'Применить фильтр', self))
        self.addObject('btnResetFilter', QtGui.QPushButton(u'Сбросить фильтр', self))
        self.setupJournalMenu()
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setWindowState(Qt.WindowMaximized)
        self.setModels(self.tblJournal,  self.modelJournal, self.selectionModelJournal)
        self.setModels(self.tblCanceled,  self.modelCanceled, self.selectionModelCanceled)
        self.setModels(self.tblPlan,  self.modelPlan, self.selectionModelPlan)
        self.buttonBox.addButton(self.btnApplyFilter, QtGui.QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.btnResetFilter, QtGui.QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.btnPrint, QtGui.QDialogButtonBox.ActionRole)
        self.tblJournal.setPopupMenu(self.mnuJournal)
        self.tblCanceled.setPopupMenu(self.mnuJournal)
        self.tblPlan.setPopupMenu(self.mnuJournal)
        self.tblJournal.setWordWrap(True)
        self.tblCanceled.setWordWrap(True)
        self.tblPlan.setWordWrap(True)
        self.tblJournal.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.tblCanceled.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.tblPlan.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.tblJournal.enableColsHide()
        self.tblJournal.enableColsMove()
        self.tblPlan.enableColsHide()
        self.tblPlan.enableColsMove()
        self.tblCanceled.enableColsHide()
        self.tblCanceled.enableColsMove()
        self.filter = {}
        self.resetFilter()
        self.updatePersonOrgStructureCanceledFilter()
        self.on_tabSurgeryJournal_currentChanged(0)
        templates = getPrintTemplates(getSurgeryJournalContext())
        if not templates:
            self.btnPrint.setId(-1)
        else:
            for template in templates:
                action = CPrintAction(template.name, template.id, self.btnPrint, self.btnPrint)
                self.btnPrint.addAction(action)
            self.btnPrint.menu().addSeparator()
            self.btnPrint.addAction(CPrintAction(u'Список', -1, self.btnPrint, self.btnPrint))
        self.btnPrint.setEnabled(True)
        self.cmbActionTypeJournal.setServiceType(CActionServiceType.operation)
        self.cmbActionTypeCanceled.setServiceType(CActionServiceType.operation)


    def exec_(self):
        self.loadDialogPreferences()
        self.showMaximized()
        result = QtGui.QDialog.exec_(self)
        return result


    def setupJournalMenu(self):
        self.addObject('mnuJournal', QtGui.QMenu(self))
        self.addObject('actEditAction',QtGui.QAction(u'Протокол', self))
        self.addObject('actOpenEvent', QtGui.QAction(u'Случай обслуживание', self))
        self.addObject('actEditClient', QtGui.QAction(u'Рег.карта пациента', self))
        self.mnuJournal.addAction(self.actEditAction)
        self.mnuJournal.addAction(self.actOpenEvent)
        self.mnuJournal.addAction(self.actEditClient)


    @pyqtSignature('int')
    def on_tabSurgeryJournal_currentChanged(self, index):
        self.getFillingTable()


    def getFillingTable(self):
        QtGui.qApp.setWaitCursor()
        try:
            self.setFilter()
            table = self.getCurrentTable()
            currentRow = table.currentRow()
            model = table.model()
            model.loadData(self.filter)
            if model.rowCount() >= 0:
                if currentRow is None:
                    currentRow = 0
                table.setCurrentRow(currentRow)
        finally:
            QtGui.qApp.restoreOverrideCursor()
        self.lblCountRecordList.setText(formatRecordsCount(self.getCurrentTable().model().rowCount()))


    def dumpParams(self, cursor, params):
        description = self.getDescription(params)
        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


    def getDescription(self, params):
        db = QtGui.qApp.db
        rows = []
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        if begDate or endDate:
            rows.append(dateRangeAsStr(u'За период', begDate, endDate))
        widgetIndex = self.tabSurgeryJournal.currentIndex()
        if widgetIndex in [0, 1]:
            personId = params.get('personId', None)
            if personId:
                personInfo = getPersonInfo(personId)
                rows.append(u'Врач: ' + personInfo['shortName']+', '+personInfo['specialityName'])
            actionTypeId = params.get('actionTypeId', None)
            if actionTypeId:
                actionTypeName = forceString(db.translate('ActionType', 'id', actionTypeId, 'name'))
                rows.append(u'Мероприятие: ' + actionTypeName)
            MKBFilter = params.get('MKBFilter', 0)
            MKBFrom = params.get('MKBFrom', '')
            MKBTo = params.get('MKBTo', '')
            if MKBFilter == 1:
                rows.append(u'Код МКБ: с "%s" по "%s"' % (MKBFrom, MKBTo))
            if widgetIndex == 0:
                actionStatus = params.get('status', None)
                if actionStatus is not None:
                    rows.append(u'Статус действия: '+ CActionStatus.text(actionStatus))
            elif widgetIndex == 1:
                statusCanceled = CActionStatus.canceled if params.get('statusCanceled', None) else None
                statusRefused = CActionStatus.refused if params.get('statusRefused', None) else None
                statusList = []
                if statusCanceled:
                   statusList.append(CActionStatus.text(statusCanceled))
                if statusRefused:
                    statusList.append(CActionStatus.text(statusRefused))
                if statusList:
                    rows.append(u'Статус действия: '+ u', '.join(status for status in statusList if status))
        elif widgetIndex == 2:
            actionStatus = params.get('status', None)
            if actionStatus is not None:
                rows.append(u'Статус действия: '+ CActionStatus.text(actionStatus))
        rows.append(u'отчёт составлен: ' + forceString(QDateTime.currentDateTime()))
        return rows


    @pyqtSignature('int')
    def on_btnPrint_printByTemplate(self, templateId):
        widgetIndex = self.tabSurgeryJournal.currentIndex()
        if widgetIndex == 0:
            model = self.modelJournal
            tableJournal = self.tblJournal
            messag = u'Журнал'
        elif widgetIndex == 1:
            model = self.modelCanceled
            tableJournal = self.tblCanceled
            messag = u'Отмена'
        elif widgetIndex == 2:
            model = self.modelPlan
            tableJournal = self.tblPlan
            messag = u'План'
        if templateId == -1:
            doc = QtGui.QTextDocument()
            cursor = QtGui.QTextCursor(doc)
            cursor.setCharFormat(CReportBase.ReportTitle)
            cursor.insertText(u'Операции: %s'%(messag))
            cursor.setCharFormat(CReportBase.ReportBody)
            cursor.insertBlock()
            self.dumpParams(cursor, self.filter)
            cursor.insertBlock()
            colWidths  = [ tableJournal.columnWidth(i) for i in xrange(model.columnCount()) ]
            totalWidth = sum(colWidths)
            tableColumns = []
            for iCol, colWidth in enumerate(colWidths):
                widthInPercents = str(max(1, colWidth*90/totalWidth))+'%'
                tableColumns.append((widthInPercents, [forceString(model._cols[iCol].title())], CReportBase.AlignLeft))
            table = createTable(cursor, tableColumns)
            for iModelRow in xrange(model.rowCount()):
                iTableRow = table.addRow()
                for iModelCol in xrange(model.columnCount()):
                    index = model.createIndex(iModelRow, iModelCol)
                    text = forceString(model.data(index))
                    table.setText(iTableRow, iModelCol, text)
            html = doc.toHtml('utf-8')
            view = CReportViewDialog(self)
            view.setText(html)
            view.exec_()
        else:
            context = CInfoContext()
            surgeryInfoList = context.getInstance(CActionInfoListEx, tuple(model.idList()))
            data = { 'surgeryInfo': surgeryInfoList }
            QtGui.qApp.call(self, applyTemplate, (self, templateId, data))


    @pyqtSignature('')
    def on_btnApplyFilter_clicked(self):
        self.on_tabSurgeryJournal_currentChanged(self.tabSurgeryJournal.currentIndex())


    @pyqtSignature('')
    def on_btnResetFilter_clicked(self):
        self.resetFilter()


    def setFilter(self):
        self.filter = {}
        widgetIndex = self.tabSurgeryJournal.currentIndex()
        if widgetIndex == 0:
            self.filter['personId']     = self.cmbPersonJournal.value()
            self.filter['orgStructureId'] = self.cmbOrgStructureJournal.value()
            self.filter['begDate']      = self.edtBegDateJournal.date()
            self.filter['endDate']      = self.edtEndDateJournal.date()
            self.filter['MKBFilter']    = self.cmbMKBFilterJournal.currentIndex()
            self.filter['MKBFrom']      = unicode(self.edtMKBFromJournal.text())
            self.filter['MKBTo']        = unicode(self.edtMKBToJournal.text())
            self.filter['status']       = self.cmbActionStatusJournal.value()
            self.filter['actionTypeId'] = self.cmbActionTypeJournal.value()
            self.filter['actionTypeIdList'] = self.getActionTypeIdList(self.cmbActionTypeJournal.value())
        elif widgetIndex == 1:
            self.filter['personId']     = self.cmbPersonCanceled.value()
            self.filter['orgStructureId'] = self.cmbOrgStructureCanceled.value()
            self.filter['begDate']      = self.edtBegDateCanceled.date()
            self.filter['endDate']      = self.edtEndDateCanceled.date()
            self.filter['MKBFilter']    = self.cmbMKBFilterCanceled.currentIndex()
            self.filter['MKBFrom']      = unicode(self.edtMKBFromCanceled.text())
            self.filter['MKBTo']        = unicode(self.edtMKBToCanceled.text())
            self.filter['statusCanceled']= self.chkActionStatusCanceled.isChecked()
            self.filter['statusRefused'] = self.chkActionStatusRefused.isChecked()
            self.filter['actionTypeId']  = self.cmbActionTypeCanceled.value()
            self.filter['actionTypeIdList'] = self.getActionTypeIdList(self.cmbActionTypeJournal.value())
        elif widgetIndex == 2:
            self.filter['begDate']      = self.edtBegDatePlan.date()
            self.filter['endDate']      = self.edtEndDatePlan.date()
            self.filter['status']       = self.cmbActionStatusPlan.value()


    def getActionTypeIdList(self, actionTypeId):
        db = QtGui.qApp.db
        tableActionType = db.table('ActionType')
        return db.getDescendants(tableActionType, 'group_id', actionTypeId, 'deleted=0') if actionTypeId else []


    def updatePersonOrgStructureCanceledFilter(self):
        orgStructureId = None
        personId = None
        if QtGui.qApp.surgeryPageRestrictFormation() == 1:
            personId = QtGui.qApp.userId if QtGui.qApp.userSpecialityId else None
        elif QtGui.qApp.surgeryPageRestrictFormation() == 2:
            orgStructureId = QtGui.qApp.userOrgStructureId if QtGui.qApp.userSpecialityId else None
        elif QtGui.qApp.surgeryPageRestrictFormation() == 3:
            orgStructureId = forceRef(QtGui.qApp.preferences.appPrefs.get('orgStructureId', QVariant()))
        elif QtGui.qApp.surgeryPageRestrictFormation() == 4:
            orgStructureId = QtGui.qApp.surgeryPageOrgStructureId()
        self.cmbPersonCanceled.setValue(personId)
        self.cmbOrgStructureCanceled.setValue(orgStructureId)


    def resetFilter(self):
        widgetIndex = self.tabSurgeryJournal.currentIndex()
        orgStructureId = None
        personId = None
        if QtGui.qApp.surgeryPageRestrictFormation() == 1:
            personId = QtGui.qApp.userId if QtGui.qApp.userSpecialityId else None
        elif QtGui.qApp.surgeryPageRestrictFormation() == 2:
            orgStructureId = QtGui.qApp.userOrgStructureId if QtGui.qApp.userSpecialityId else None
        elif QtGui.qApp.surgeryPageRestrictFormation() == 3:
            orgStructureId = forceRef(QtGui.qApp.preferences.appPrefs.get('orgStructureId', QVariant()))
        elif QtGui.qApp.surgeryPageRestrictFormation() == 4:
            orgStructureId = QtGui.qApp.surgeryPageOrgStructureId()
        if widgetIndex == 0:
            self.cmbPersonJournal.setValue(personId)
            self.cmbOrgStructureJournal.setValue(orgStructureId)
            self.edtBegDateJournal.setDate(QDate.currentDate())
            self.edtEndDateJournal.setDate(QDate.currentDate())
            self.cmbMKBFilterJournal.setCurrentIndex(0)
            self.edtMKBFromJournal.setText('A__. _')
            self.edtMKBToJournal.setText('Z99.9_')
            self.on_cmbMKBFilterJournal_currentIndexChanged(0)
            self.cmbActionStatusJournal.setValue(CActionStatus.finished)
            self.cmbActionTypeJournal.setValue(None)
        elif widgetIndex == 1:
            self.cmbPersonCanceled.setValue(personId)
            self.cmbOrgStructureCanceled.setValue(orgStructureId)
            self.edtBegDateCanceled.setDate(QDate.currentDate())
            self.edtEndDateCanceled.setDate(QDate.currentDate())
            self.cmbMKBFilterCanceled.setCurrentIndex(0)
            self.edtMKBFromCanceled.setText('A__. _')
            self.edtMKBToCanceled.setText('Z99.9_')
            self.on_cmbMKBFilterCanceled_currentIndexChanged(0)
            self.chkActionStatusCanceled.setChecked(True)
            self.chkActionStatusRefused.setChecked(True)
            self.cmbActionTypeCanceled.setValue(None)
        elif widgetIndex == 2:
            self.edtBegDatePlan.setDate(QDate.currentDate())
            self.edtEndDatePlan.setDate(QDate.currentDate())
            self.cmbActionStatusPlan.setValue(0)
        self.setFilter()


    @pyqtSignature('int')
    def on_cmbMKBFilterJournal_currentIndexChanged(self, index):
        mode = bool(index)
        for widget in (self.edtMKBFromJournal, self.edtMKBToJournal):
            widget.setEnabled(mode)


    @pyqtSignature('int')
    def on_cmbMKBFilterCanceled_currentIndexChanged(self, index):
        mode = bool(index)
        for widget in (self.edtMKBFromCanceled, self.edtMKBToCanceled):
            widget.setEnabled(mode)


    @pyqtSignature('')
    def on_mnuJournal_aboutToShow(self):
        isEnabled = False
        widgetIndex = self.tabSurgeryJournal.currentIndex()
        if widgetIndex == 0:
            self.tblJournal.setFocus(Qt.OtherFocusReason)
            currentIndex = self.tblJournal.currentIndex()
            isEnabled = currentIndex.row() >= 0
        elif widgetIndex == 1:
            self.tblCanceled.setFocus(Qt.TabFocusReason)
            currentIndex = self.tblCanceled.currentIndex()
            isEnabled = currentIndex.row() >= 0
        elif widgetIndex == 2:
            self.tblPlan.setFocus(Qt.OtherFocusReason)
            currentIndex = self.tblPlan.currentIndex()
            isEnabled = currentIndex.row() >= 0
        self.actEditAction.setEnabled(isEnabled)
        self.actOpenEvent.setEnabled(isEnabled)
        self.actEditClient.setEnabled(isEnabled)


    @pyqtSignature('')
    def on_actEditAction_triggered(self):
        isRightAdmin =  QtGui.qApp.isAdmin()
        isSJReadAction = QtGui.qApp.userHasRight(urSurgeryJournalReadAction) or isRightAdmin
        isSJEditAction = QtGui.qApp.userHasRight(urSurgeryJournalEditAction) or isRightAdmin
        if isSJReadAction or isSJEditAction:
            table = self.getCurrentTable()
            actionId = table.currentItemId()
            if actionId and canChangePayStatusAdditional(self, 'Action', actionId) and canEditOtherpeopleAction(self, actionId):
                currentRow = table.currentRow()
                dialog = CActionEditDialog(self)
                try:
                    dialog.load(actionId)
                    if dialog.exec_():
                        table.setCurrentRow(currentRow)
                        self.on_tabSurgeryJournal_currentChanged(self.tabSurgeryJournal.currentIndex())
                finally:
                    dialog.deleteLater()
        else:
            QtGui.QMessageBox.warning( self,
                         u'Внимание!',
                         u'Нет права на чтение и редактирование действия!',
                         QtGui.QMessageBox.Ok,
                         QtGui.QMessageBox.Ok)


    @pyqtSignature('')
    def on_actEditClient_triggered(self):
        self.editClient()


    def editClient(self):
        isRightAdmin =  QtGui.qApp.isAdmin()
        isSJReadClientInfo = QtGui.qApp.userHasRight(urSurgeryJournalReadClientInfo) or isRightAdmin
        isSJEditClientInfo = QtGui.qApp.userHasRight(urSurgeryJournalEditClientInfo) or isRightAdmin
        if isSJReadClientInfo or isSJEditClientInfo:
            table = self.getCurrentTable()
            if table:
                tableIndex = table.currentIndex()
                row = tableIndex.row()
                if row >= 0:
                    currentRow = table.currentRow()
                    model = table.model()
                    record = model.getRecordByRow(currentRow)
                    eventId = forceRef(record.value('event_id')) if record else None
                    if eventId and model.clientCache and model.eventCache:
                        eventRecord = model.eventCache.get(eventId)
                        if eventRecord:
                            clientId = forceRef(eventRecord.value('client_id'))
                            if clientId:
                                dialog = CSurgeryJournalClientEditDialog(self)
                                try:
                                    if clientId:
                                        dialog.load(clientId)
                                    if dialog.exec_():
                                        table.setCurrentRow(currentRow)
                                        self.on_tabSurgeryJournal_currentChanged(self.tabSurgeryJournal.currentIndex())
                                finally:
                                    dialog.deleteLater()
        else:
            QtGui.QMessageBox.warning( self,
                         u'Внимание!',
                         u'Нет права на чтение и редактирование карты пациента!',
                         QtGui.QMessageBox.Ok,
                         QtGui.QMessageBox.Ok)


    @pyqtSignature('')
    def on_actOpenEvent_triggered(self):
        QtGui.qApp.callWithWaitCursor(self, self.openEvent)


    def openEvent(self):
        isRightAdmin =  QtGui.qApp.isAdmin()
        isSurgeryJournalReadEvent = QtGui.qApp.userHasRight(urSurgeryJournalReadEvent) or isRightAdmin
        isSurgeryJournalEditEvent = QtGui.qApp.userHasRight(urSurgeryJournalEditEvent) or isRightAdmin
        if isSurgeryJournalReadEvent or isSurgeryJournalEditEvent:
            currentTable = self.getCurrentTable()
            currentRow = currentTable.currentRow()
            record = currentTable.model().getRecordByRow(currentRow)
            eventId = forceRef(record.value('event_id')) if record else None
            if eventId:
                try:
                    formClass = getEventFormClass(eventId)
                    dialog = formClass(self)
                    dialog.load(eventId)
                    QtGui.qApp.restoreOverrideCursor()
                    dialog.setReadOnly(isSurgeryJournalReadEvent and not isSurgeryJournalEditEvent)
                    if dialog.exec_():
                        currentTable.setCurrentRow(currentRow)
                        self.getFillingTable()
                finally:
                    dialog.deleteLater()
        else:
            QtGui.QMessageBox.warning( self,
                                     u'Внимание!',
                                     u'Нет права на чтение и редактирование события!',
                                     QtGui.QMessageBox.Ok,
                                     QtGui.QMessageBox.Ok)


    def getCurrentTable(self):
        index = self.tabSurgeryJournal.currentIndex()
        return [self.tblJournal, self.tblCanceled, self.tblPlan][index]


class CSurgeryJournalModel(CTableModel):
    class CLocClientColumn(CTextCol):
        def __init__(self, title, fields, defaultWidth, alignment='l'):
            CTextCol.__init__(self, title, fields, defaultWidth, alignment)
            self.clientCache = {}
            self.eventCache = {}

        def setClientCache(self, clientCache):
            self.clientCache = clientCache

        def setEventCache(self, eventCache):
            self.eventCache = eventCache

        def format(self, values):
            name = u''
            eventId = forceRef(values[0])
            if eventId and self.clientCache and self.eventCache:
                eventRecord = self.eventCache.get(eventId)
                if eventRecord:
                    clientId = forceRef(eventRecord.value('client_id'))
                    clientRecord = self.clientCache.get(clientId) if clientId else None
                    if clientRecord:
                        birthDate = forceDate(clientRecord.value('birthDate'))
                        name = formatShortNameInt(forceString(clientRecord.value('lastName')),
                               forceString(clientRecord.value('firstName')),
                               forceString(clientRecord.value('patrName'))) + u', ' + birthDate.toString('dd.MM.yyyy') + u', ' + formatSex(forceInt(clientRecord.value('sex')))
            return QVariant(name)

    class CLocProtocolCol(CTextCol):
        def __init__(self, title, fields, defaultWidth, alignment='l'):
            CTextCol.__init__(self, title, fields, defaultWidth, alignment)

        def format(self, values):
            db = QtGui.qApp.db
            propertyResult = u''
            actionId = forceRef(values[0])
            if actionId:
                action = CAction.getActionById(actionId)
                if action:
                    propertiesByName = action.getPropertiesByName()
                    properties = propertiesByName.values()
                    properties.sort(key=lambda prop:prop._type.idx)
                    for property in properties:
                        name = property._type.name
                        tableName = None
                        propertyType = property.type()
                        typeName = propertyType.typeName
                        if typeName == 'Reference':
                            domain = propertyType.valueDomain
                            if domain:
                                domainList = domain.split(u';') # engl
                                if len(domainList) != 3:
                                    domainList = domain.split(u';') # rus
                                if len(domainList) == 3:
                                    tableName = trim(domainList[0])
                                    if tableName.lower() == u'person':
                                        tableName = u'vrbPersonWithSpeciality'
                        elif typeName == u'JobTicket':
                            propertyValue = forceRef(action[name])
                            if propertyValue:
                                propertyResult += name + u': ' + getJobTicketAsText(propertyValue) + u'\n'
                        elif typeName and typeName in ActionPropertyTableList:
                            tableName = ActionPropertyTableList.get(typeName, None)
                        if tableName:
                            propertyValue = forceRef(action[name])
                            if propertyValue:
                                if typeName == u'Contract':
                                    record = db.getRecord('Contract', ['number', 'date', 'resolution'], propertyValue)
                                    propertyResult += name + u': ' + ' '.join([forceString(record.value(n)) for n in ['number', 'date', 'resolution']]) + u'\n'
                                else:
                                    propertyResult += name + u': ' + forceString(db.translate(tableName, 'id', propertyValue, 'name' if typeName != 'Organisation' else 'shortName')) + u'\n'
                        else:
                            propertyValue = forceString(action[name])
                            if propertyValue:
                                propertyResult += name + u': ' + propertyValue + u'\n'
            return QVariant(propertyResult)


    class CLocActionTypeCol(CRefBookCol):
        def __init__(self, title, fields, tableName, defaultWidth, showFields=CRBComboBox.showName, alignment='l', filter = ''):
            CRefBookCol.__init__(self, title, fields, tableName, defaultWidth, showFields, alignment)
            self.tableName = tableName
            self.filter = filter
            self.data = CRBModelDataCache.getData(tableName, True, self.filter)
            self.showFields = showFields

        def invalidateRecordsCache(self):
            self.data = CRBModelDataCache.getData(self.tableName, True, self.filter)

    Col_Client      = 1
    Col_ProtocolCol = 5

    def __init__(self, parent):
        CTableModel.__init__(self, parent)
        self.eventCache = {}
        self.clientCache = {}
        self.filter = {}


    def setEventCache(self, eventCache):
        self.eventCache = eventCache
        self._cols[CSurgeryJournalModel.Col_Client].setEventCache(self.eventCache)


    def setClientCache(self, clientCache):
        self.clientCache = clientCache
        self._cols[CSurgeryJournalModel.Col_Client].setClientCache(self.clientCache)


class CJournalModel(CSurgeryJournalModel):
    def __init__(self, parent):
        CSurgeryJournalModel.__init__(self, parent)
        self.addColumn(CDateTimeCol(                          u'Дата',         ['endDate'],                                  12, highlightRedDate=False))
        self.addColumn(CSurgeryJournalModel.CLocClientColumn( u'Пациент',      ['event_id'],                                 20, 'l'))
        self.addColumn(CRefBookCol(                           u'Исполнитель',  ['person_id'],     'vrbPersonWithSpeciality', 12))
        self.addColumn(CSurgeryJournalModel.CLocActionTypeCol(u'Тип операции', ['actionType_id'], 'ActionType',              25, showFields=CRBComboBox.showCodeAndName, filter = 'serviceType = %d'%(CActionServiceType.operation)))
        self.addColumn(CTextCol(                              u'МКБ',          ['MKB'],                                      6))
        self.addColumn(CSurgeryJournalModel.CLocProtocolCol(  u'Протокол',     ['id'],                                       25))
        self.setTable('Action')


    def loadData(self, filter):
        actionIdList = []
        eventIdList = []
        clientIdList = []
        self.filter = filter
        db = QtGui.qApp.db
        tableEvent = db.table('Event')
        tableClient = db.table('Client')
        tableAction = db.table('Action')
        tableActionType = db.table('ActionType')
        cols = [tableAction['id'].alias('actionId'),
                tableAction['event_id'].alias('eventId'),
                tableEvent['client_id'].alias('clientId')
                ]
        cond = [tableActionType['serviceType'].eq(CActionServiceType.operation),
                tableAction['deleted'].eq(0),
                tableAction['endDate'].isNotNull(),
                tableActionType['deleted'].eq(0)
                ]
        queryTable = tableAction.innerJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
        queryTable = queryTable.leftJoin(tableEvent, db.joinAnd([tableEvent['id'].eq(tableAction['event_id']), tableEvent['deleted'].eq(0)]))
        personId = self.filter.get('personId', None)
        if personId:
            cond.append(tableAction['person_id'].eq(personId))
        orgStructureId = self.filter.get('orgStructureId', None)
        if orgStructureId:
            cond.append(tableAction['orgStructure_id'].eq(orgStructureId))
        begDate = self.filter.get('begDate', None)
        endDate = self.filter.get('endDate', None)
        if begDate:
           cond.append(tableAction['endDate'].dateGe(begDate))
        if endDate:
           cond.append(tableAction['endDate'].dateLe(endDate))
        MKBFilter = self.filter.get('MKBFilter', None)
        if MKBFilter:
            MKBFrom = self.filter.get('MKBFrom', None)
            MKBTo = self.filter.get('MKBTo', None)
            if MKBFrom:
               cond.append(u'''Action.MKB >= '%s'''%(MKBFrom))
            if MKBTo:
                cond.append(u'''Action.MKB <= '%s'''%(MKBTo))
        status = self.filter.get('status', None)
        if status:
            cond.append(tableAction['status'].eq(status))
        actionTypeIdList = self.filter.get('actionTypeIdList', None)
        if actionTypeIdList:
            cond.append(tableAction['actionType_id'].inlist(actionTypeIdList))
        records = db.getRecordList(queryTable, cols, cond, tableAction['endDate'].name())
        for record in records:
            actionId = forceRef(record.value('actionId'))
            if actionId and actionId not in actionIdList:
                actionIdList.append(actionId)
                eventId = forceRef(record.value('eventId'))
                if eventId and eventId not in eventIdList:
                    eventIdList.append(eventId)
                clientId = forceRef(record.value('clientId'))
                if clientId and clientId not in clientIdList:
                    clientIdList.append(clientId)
        eventCache = CTableRecordCache(db, db.forceTable(tableEvent), u'*', capacity=None)
        eventCache.fetch(eventIdList)
        self.setEventCache(eventCache)
        clientCache = CTableRecordCache(db, db.forceTable(tableClient), u'*', capacity=None)
        clientCache.fetch(clientIdList)
        self.setClientCache(clientCache)
        self.setIdList(actionIdList)


class CCanceledModel(CSurgeryJournalModel):
    def __init__(self, parent):
        CSurgeryJournalModel.__init__(self, parent)
        self.addColumn(CDateTimeCol(                          u'Дата',         ['begDate'],                                  12, highlightRedDate=False))
        self.addColumn(CSurgeryJournalModel.CLocClientColumn( u'Пациент',      ['event_id'],                                 20, 'l'))
        self.addColumn(CRefBookCol(                           u'Исполнитель',  ['person_id'],     'vrbPersonWithSpeciality', 12))
        self.addColumn(CSurgeryJournalModel.CLocActionTypeCol(u'Тип операции', ['actionType_id'], 'ActionType',              25, showFields=CRBComboBox.showCodeAndName, filter = 'serviceType = %d'%(CActionServiceType.operation)))
        self.addColumn(CTextCol(                              u'МКБ',          ['MKB'],                                      6))
        self.addColumn(CSurgeryJournalModel.CLocProtocolCol(  u'Протокол',     ['id'],                                       25))
        self.setTable('Action')


    def loadData(self, filter):
        actionIdList = []
        eventIdList = []
        clientIdList = []
        self.filter = filter
        db = QtGui.qApp.db
        tableEvent = db.table('Event')
        tableClient = db.table('Client')
        statusCanceled = CActionStatus.canceled if self.filter.get('statusCanceled', None) else None
        statusRefused = CActionStatus.refused if self.filter.get('statusRefused', None) else None
        if statusCanceled or statusRefused:
            tableAction = db.table('Action')
            tableActionType = db.table('ActionType')
            cols = [tableAction['id'].alias('actionId'),
                    tableAction['event_id'].alias('eventId'),
                    tableEvent['client_id'].alias('clientId')
                    ]
            cond = [tableActionType['serviceType'].eq(CActionServiceType.operation),
                    tableAction['deleted'].eq(0),
                    tableAction['endDate'].isNull(),
                    tableActionType['deleted'].eq(0)
                    ]
            queryTable = tableAction.innerJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
            queryTable = queryTable.leftJoin(tableEvent, db.joinAnd([tableEvent['id'].eq(tableAction['event_id']), tableEvent['deleted'].eq(0)]))
            personId = self.filter.get('personId', None)
            if personId:
                cond.append(tableAction['person_id'].eq(personId))
            orgStructureId = self.filter.get('orgStructureId', None)
            if orgStructureId:
                cond.append(tableAction['orgStructure_id'].eq(orgStructureId))
            begDate = self.filter.get('begDate', None)
            endDate = self.filter.get('endDate', None)
            if begDate:
               cond.append(tableAction['begDate'].dateGe(begDate))
            if endDate:
               cond.append(tableAction['begDate'].dateLe(endDate))
            MKBFilter = self.filter.get('MKBFilter', None)
            if MKBFilter:
                MKBFrom = self.filter.get('MKBFrom', None)
                MKBTo = self.filter.get('MKBTo', None)
                if MKBFrom:
                   cond.append(u'''Action.MKB >= '%s'''%(MKBFrom))
                if MKBTo:
                    cond.append(u'''Action.MKB <= '%s'''%(MKBTo))
            status = []
            if statusCanceled:
                status.append(statusCanceled)
            if statusRefused:
                status.append(statusRefused)
            if status:
                cond.append(tableAction['status'].inlist(status))
            actionTypeIdList = self.filter.get('actionTypeIdList', None)
            if actionTypeIdList:
                cond.append(tableAction['actionType_id'].inlist(actionTypeIdList))
            records = db.getRecordList(queryTable, cols, cond, tableAction['endDate'].name())
            for record in records:
                actionId = forceRef(record.value('actionId'))
                if actionId and actionId not in actionIdList:
                    actionIdList.append(actionId)
                    eventId = forceRef(record.value('eventId'))
                    if eventId and eventId not in eventIdList:
                        eventIdList.append(eventId)
                    clientId = forceRef(record.value('clientId'))
                    if clientId and clientId not in clientIdList:
                        clientIdList.append(clientId)
        eventCache = CTableRecordCache(db, db.forceTable(tableEvent), u'*', capacity=None)
        eventCache.fetch(eventIdList)
        self.setEventCache(eventCache)
        clientCache = CTableRecordCache(db, db.forceTable(tableClient), u'*', capacity=None)
        clientCache.fetch(clientIdList)
        self.setClientCache(clientCache)
        self.setIdList(actionIdList)


class CPlanModel(CSurgeryJournalModel):
    def __init__(self, parent):
        CSurgeryJournalModel.__init__(self, parent)
        self.addColumn(CDateTimeCol(                          u'Дата',         ['plannedEndDate'],                           12, highlightRedDate=False))
        self.addColumn(CSurgeryJournalModel.CLocClientColumn( u'Пациент',      ['event_id'],                                 20, 'l'))
        self.addColumn(CRefBookCol(                           u'Исполнитель',  ['person_id'],     'vrbPersonWithSpeciality', 12))
        self.addColumn(CSurgeryJournalModel.CLocActionTypeCol(u'Тип операции', ['actionType_id'], 'ActionType',              25, showFields=CRBComboBox.showCodeAndName, filter = 'serviceType = %d'%(CActionServiceType.operation)))
        self.addColumn(CTextCol(                              u'МКБ',          ['MKB'],                                      6))
        self.addColumn(CSurgeryJournalModel.CLocProtocolCol(  u'Протокол',     ['id'],                                       25))
        self.setTable('Action')


    def loadData(self, filter):
        actionIdList = []
        eventIdList = []
        clientIdList = []
        self.filter = filter
        db = QtGui.qApp.db
        tableEvent = db.table('Event')
        tableClient = db.table('Client')
        tableAction = db.table('Action')
        tableActionType = db.table('ActionType')
        cols = [tableAction['id'].alias('actionId'),
                tableAction['event_id'].alias('eventId'),
                tableEvent['client_id'].alias('clientId')
                ]
        cond = [tableActionType['serviceType'].eq(CActionServiceType.operation),
                tableAction['deleted'].eq(0),
                tableAction['plannedEndDate'].isNotNull(),
                tableActionType['deleted'].eq(0)
                ]
        queryTable = tableAction.innerJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
        queryTable = queryTable.leftJoin(tableEvent, db.joinAnd([tableEvent['id'].eq(tableAction['event_id']), tableEvent['deleted'].eq(0)]))

        begDate = self.filter.get('begDate', None)
        endDate = self.filter.get('endDate', None)
        if begDate:
           cond.append(tableAction['plannedEndDate'].dateGe(begDate))
        if endDate:
           cond.append(tableAction['plannedEndDate'].dateLe(endDate))
        status = self.filter.get('status', None)
        if status:
            cond.append(tableAction['status'].eq(status))
        records = db.getRecordList(queryTable, cols, cond, tableAction['endDate'].name())
        for record in records:
            actionId = forceRef(record.value('actionId'))
            if actionId and actionId not in actionIdList:
                actionIdList.append(actionId)
                eventId = forceRef(record.value('eventId'))
                if eventId and eventId not in eventIdList:
                    eventIdList.append(eventId)
                clientId = forceRef(record.value('clientId'))
                if clientId and clientId not in clientIdList:
                    clientIdList.append(clientId)
        eventCache = CTableRecordCache(db, db.forceTable(tableEvent), u'*', capacity=None)
        eventCache.fetch(eventIdList)
        self.setEventCache(eventCache)
        clientCache = CTableRecordCache(db, db.forceTable(tableClient), u'*', capacity=None)
        clientCache.fetch(clientIdList)
        self.setClientCache(clientCache)
        self.setIdList(actionIdList)


class CSurgeryJournalClientEditDialog(CClientEditDialog):
    def __init__(self, parent):
        CClientEditDialog.__init__(self, parent)


    def saveData(self):
        isRightAdmin =  QtGui.qApp.isAdmin()
        isSJReadClientInfo = QtGui.qApp.userHasRight(urSurgeryJournalReadClientInfo) or isRightAdmin
        isSJEditClientInfo = QtGui.qApp.userHasRight(urSurgeryJournalEditClientInfo) or isRightAdmin
        if isSJReadClientInfo and not isSJEditClientInfo:
            QtGui.QMessageBox.warning(self,
                            u'Внимание',
                            u'Право только на чтение!',
                            QtGui.QMessageBox.Ok,
                            QtGui.QMessageBox.Ok)
            return False
        if isSJEditClientInfo:
            return self.checkDataEntered() and self.save()
        return False


def getSurgeryJournalContext():
    return ['surgeryJournal']

