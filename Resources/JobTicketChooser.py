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
from PyQt4.QtCore import Qt, QDate, QVariant, pyqtSignature, SIGNAL

from library.crbcombobox      import ( CRBComboBox, CRBModelDataCache )
from library.DialogBase       import CDialogBase
from library.TableModel       import ( CTableModel,
                                       CDesignationCol,
                                       CDateTimeCol,
                                       CCol,
                                     )
from library.TreeModel        import CDBTreeModel, CDBTreeItem
from library.Utils import (forceString,
                           forceRef,
                           forceBool,
                           forceDate,
                           forceDateTime,
                                       forceInt,
                                     )

from Orgs.Utils import getOrgStructureName, getOrgStructureDescendants, getSolitaryOrgStructureId
from Resources.JobTicketStatus import CJobTicketStatus
from Resources.JobTicketChooserHelper import createExceedJobTicket, getJobId, CJobTicketChooserHelper
from Users.Rights import urCanAddExceedJobTicket, urUsePreviouslyAppointedJobTicket

from Resources.Ui_JobTicketChooserDialog import Ui_JobTicketChooserDialog


# ##############################################################################

def getJobTicketRecord(ticketId):
    db = QtGui.qApp.db
    stmt = '''SELECT Job.jobType_id, Job.jobPurpose_id, Job.orgStructure_id, Job.date, Job_Ticket.orgStructure_id as jobTicketOrgStructure_id, Job.begTime, Job.endTime, Job_Ticket.*
              FROM Job_Ticket LEFT JOIN Job ON Job.id=Job_Ticket.master_id
              WHERE Job_Ticket.id=%d''' % ticketId
    query = db.query(stmt)
    if query.next():
        return query.record()
    else:
        return None


def getJobTicketAsText(ticketId):
    record = getJobTicketRecord(ticketId) if ticketId else None
    if record:
        jobTypeId = forceRef(record.value('jobType_id'))
        isExceed  = forceBool(record.value('isExceedQuantity'))
        if isExceed:
            datetimeStr = u'%s, сверх плана' % forceDate(record.value('date')).toString(Qt.LocaleDate)
        else:
            datetimeStr = forceDateTime(record.value('datetime')).toString(Qt.LocaleDate)
        orgStructureId = forceRef(record.value('orgStructure_id'))
        cache = CRBModelDataCache.getData('rbJobType', True)
        return u'%s, %s, %s' % ( cache.getStringById(jobTypeId, CRBComboBox.showName),
                                 forceString(datetimeStr),
                                 getOrgStructureName(orgStructureId) )
    else:
        return ''


def getJobTicketsQueryParts(ticketId, jobTypeId, date, showNextDays, execOrgStructureId, eventTypeId, clientId, actionTypeId=None, excludedTickets=[]):
    db = QtGui.qApp.db

    tableJobTicket = db.table('Job_Ticket')
    tableJob = db.table('Job')
    tableAPJT = db.table('ActionProperty_Job_Ticket')
    tableOrgStructure = db.table('OrgStructure')

    queryTable = tableJobTicket
    queryTable = queryTable.leftJoin(tableJob, tableJob['id'].eq(tableJobTicket['master_id']))
    queryTable = queryTable.leftJoin(tableAPJT, tableAPJT['value'].eq(tableJobTicket['id']))
    queryTable = queryTable.leftJoin(tableOrgStructure, tableOrgStructure['id'].eq(tableJob['orgStructure_id']))

    jobPurposeIdList = CJobTicketChooserHelper.selectJobPurposeIdList(clientId, eventTypeId,
                                                                      QtGui.qApp.currentOrgStructureId(), False, actionTypeId)
    cond = [tableJob['deleted'].eq(0),
            tableJobTicket['deleted'].eq(0),
            'Job_Ticket.`datetime` >= NOW()',
            tableJob['date'].ge(date) if showNextDays else tableJob['date'].eq(date),
            tableJob['jobType_id'].eq(jobTypeId),
            db.joinOr([db.joinAnd([tableJobTicket['status'].eq(CJobTicketStatus.wait),
                                   tableAPJT['id'].isNull()
                                  ]
                                 ),
                       tableJobTicket['id'].eq(ticketId)
                      ]
                     ),
            db.joinOr([tableJob['jobPurpose_id'].isNull(),
                       tableJob['jobPurpose_id'].inlist(jobPurposeIdList)
                      ]
                     ),
             tableJobTicket['id'].notInlist(excludedTickets),
            'NOT isReservedJobTicket(Job_Ticket.id)'
            ]

    if execOrgStructureId:
        cond.append(tableOrgStructure['id'].inlist(db.getDescendants(tableOrgStructure, 'parent_id', execOrgStructureId)))

    return queryTable, cond


def getJobTicketIdList(ticketId, jobTypeId, date, showNextDays, orgStructureId, eventTypeId, clientId, actionTypeId=None, excludedTickets=[]):
    if jobTypeId and date:
        db = QtGui.qApp.db
        tableEx, cond = getJobTicketsQueryParts(ticketId, jobTypeId, date, showNextDays, orgStructureId, eventTypeId, clientId, actionTypeId, excludedTickets)
        cond.append(db.table('Job_Ticket')['isExceedQuantity'].eq(0))
        idList = db.getDistinctIdList(tableEx, idCol='Job_Ticket.id', where=cond, order='OrgStructure.code, datetime')
    else:
        idList = []
    return idList


# ##############################################################################


class CJobTicketChooserComboBox(QtGui.QComboBox):
    def __init__(self, parent = None):
        QtGui.QComboBox.__init__(self, parent)
        self.setMinimumContentsLength(10)
        self._popup=None
        self._ticketId = None
        self._defaultDate = QDate.currentDate()
        self._defaultJobTypeCode = ''
        self.eventTypeId = None
        self.actionTypeId = None
        self.clientId = None
        self.reservedJobTickets = {}
        self.addItem('')


    def setReservedJobTickets(self, reservedJobTickets):
        self.reservedJobTickets = reservedJobTickets


    def setEventTypeId(self, eventTypeId):
        self.eventTypeId = eventTypeId


    def setClientId(self, clientId):
        self.clientId = clientId


    def setDefaultDate(self, date):
        self._defaultDate = date


    def setActionTypeId(self, actionTypeId):
        self.actionTypeId = actionTypeId


    def setDefaultJobTypeCode(self, code):
        self._defaultJobTypeCode = code


    def defaultJobTypeCode(self):
        return self._defaultJobTypeCode


    def setValue(self, ticketId):
        if ticketId:
            db = QtGui.qApp.db
            tableJob = db.table('Job')
            tableJobTicket = db.table('Job_Ticket')
            queryTable = tableJob.leftJoin(tableJobTicket, tableJobTicket['master_id'].eq(tableJob['id']))
            record = db.getRecordEx(queryTable, [tableJobTicket['id'].alias('jobTicketId'), tableJob['deleted'].alias('deletedJob'), tableJobTicket['deleted'].alias('deletedJobTicket')], [tableJobTicket['id'].eq(ticketId)])
            checkTicketId = forceRef(record.value('jobTicketId')) if record else None
            message = u''
            if not checkTicketId:
                message = u'Данный номерок недоступен!'
            deletedJob = forceBool(record.value('deletedJob')) if record else False
            if deletedJob:
                message = u'Расписание удалено!\nДанный номерок недоступен!'
            deletedJobTicket = forceBool(record.value('deletedJobTicket')) if record else False
            if deletedJobTicket:
                message = u'Данный номерок удалён!'
            if message:
                QtGui.QMessageBox.warning(None,
                                u'Внимание!',
                                message,
                                QtGui.QMessageBox.Cancel,
                                QtGui.QMessageBox.Cancel)
                return
        if self._ticketId != ticketId:
            self._ticketId = ticketId
            text = getJobTicketAsText(self._ticketId) if self._ticketId else u'не выбрано'
            self.setItemText(0, text)
            self.emit(SIGNAL('textChanged(QString)'), text)


    def value(self):
        return self._ticketId


    def text(self):
        return self.lineEdit.text()


    def showPopup(self):
        dlg = CJobTicketChooserDialog(self, self.eventTypeId, self.clientId, self.actionTypeId)
        if self.reservedJobTickets:
            dlg.setReservedJobTickets(self.reservedJobTickets)
        if self._ticketId:
            dlg.setTicketId(self._defaultJobTypeCode, self._ticketId)
        else:
            dlg.setDefaults(self._defaultJobTypeCode, self._defaultDate)
        if dlg.exec_():
            self.setValue(dlg.getTicketId())


    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Delete:
            self.setValue(None)
        QtGui.QComboBox.keyPressEvent(self, event)


# ##############################################################################


class CJobTicketChooserDialog(CDialogBase, Ui_JobTicketChooserDialog):
    def __init__(self, parent, eventTypeId, clientId, actionTypeId):
        CDialogBase.__init__(self, parent)

        self._parent = parent

        self._userJobTypeIdList = None
        self._keyForExistent = None
        self._keyForNew = None
        self._createdExceedJobTicketId = None
        self._filterOrgStructureId = None

        self.addModels('JobTypes', CDBTreeModel(self, 'rbJobType', 'id', 'group_id', 'name',
                                                order='code', filter=self.getJobTypeFilter()))
        self.addModels('ExistensTickets', CTicketsModel(self))
        self.addModels('Tickets', CTicketsModel(self))
        self.addObject('btnAddExceed', QtGui.QPushButton(u'Добавить сверх плана', self))

        self.setupUi(self)
        self.buttonBox.addButton(self.btnAddExceed, QtGui.QDialogButtonBox.ActionRole)
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)

        self.modelJobTypes.setRootItemVisible(False)
        self.modelJobTypes.setLeavesVisible(True)

        self.setModels(self.treeJobTypes, self.modelJobTypes, self.selectionModelJobTypes)
        self.treeJobTypes.header().setVisible(False)
        self.setModels(self.tblOldTickets,  self.modelExistensTickets, self.selectionModelExistensTickets)
        self.setModels(self.tblTickets,  self.modelTickets, self.selectionModelTickets)

        self.eventTypeId = eventTypeId
        self.clientId = clientId
        self.ticketId = None
        self.actionTypeId = actionTypeId
        self.reservedJobTickets = {}

        self.cmbFilterOrgStructure.setExpandAll(True)
        self.setFilterOrgStructureVisible(False)
        today = QDate.currentDate()
        self.clnCalendar.setMinimumDate(today)
        self.updateAddExceedButton()


    def exec_(self):
        self.loadDialogPreferences()
        if not QtGui.qApp.userHasRight(urUsePreviouslyAppointedJobTicket):
            self.tabWidget.setCurrentIndex(1)
            self.tabOld.setEnabled(False)
        result = QtGui.QDialog.exec_(self)
        return result


    def setReservedJobTickets(self, reservedJobTickets):
        self.reservedJobTickets = reservedJobTickets


    def getJobTypeFilter(self):
        db = QtGui.qApp.db
        jobTypeIdList = QtGui.qApp.userAvailableJobTypeIdList()
        if jobTypeIdList:
            return db.table('rbJobType')['id'].inlist(db.getTheseAndParents('rbJobType', 'group_id', jobTypeIdList))
        return None


    def setDefaultJobType(self, jobTypeCode):
        db = QtGui.qApp.db
        jobTypeId = forceRef(db.translate('rbJobType', 'code', jobTypeCode, 'id'))
        if jobTypeId:
            self.setDefaultJobTypeId(jobTypeId)
        return jobTypeId


    def setDefaultJobTypeId(self, jobTypeId):
        db = QtGui.qApp.db
        jobTypeName = forceString(db.translate('rbJobType', 'id', jobTypeId, 'name'))
        self.modelJobTypes.setRootItem(CDBTreeItem(None, jobTypeName, jobTypeId, self.modelJobTypes))
        self.modelJobTypes.setRootItemVisible(True)
        jobTypesVisible = not self.modelJobTypes.getRootItem().isLeaf()
        self.pnlTreeJobTypes.setVisible(jobTypesVisible)
        orgStructuresVisible = False
        orgStructureIdList = self._getOrgStructureByJobTypeId(jobTypeId)
        if orgStructureIdList:
            orgStructuresVisible = len(orgStructureIdList)>1
            self.setFilterOrgStructureVisible(orgStructuresVisible)
            if orgStructuresVisible:
                extOrgStructureIdList = db.getTheseAndParents('OrgStructure', 'parent_id', orgStructureIdList)
                filter = QtGui.qApp.db.table('OrgStructure')['id'].inlist(extOrgStructureIdList)
                self.cmbFilterOrgStructure.setFilter(filter)
            else:
                self._filterOrgStructureId = orgStructureIdList[0]
        else:
            self.setFilterOrgStructureVisible(False)

        if orgStructuresVisible:
            if jobTypesVisible:
                tilte = u'Выберите работу, место и дату'
            else:
                tilte = u'%s: выберите место и дату' % jobTypeName
        else:
            tilte = u''
            if self._filterOrgStructureId:
                tableOS = db.table('OrgStructure')
                record = db.getRecordEx(tableOS, [tableOS['name']], [tableOS['id'].eq(self._filterOrgStructureId), tableOS['deleted'].eq(0)])
                tilte += ('%s. '%(forceString(record.value('name')))) if record else u''
            if jobTypesVisible:
                tilte += u'Выберите работу и дату'
            else:
                tilte += u'%s: выберите дату' % jobTypeName
        self.setWindowTitle(tilte)


    def setFilterOrgStructureVisible(self, value):
        self.cmbFilterOrgStructure.setVisible(value)
        self.lblFilterOrgStructure.setVisible(value)


    def _getOrgStructureByJobTypeId(self, jobTypeId):
        db = QtGui.qApp.db
        table = db.table('Job')
        cond = [table['jobType_id'].eq(jobTypeId),
                table['deleted'].eq(0),
                table['date'].ge(QDate.currentDate()),
                table['date'].le(QDate.currentDate().addYears(1))
               ]
        queryTable = table
        if self.clientId:
            clientRecord = db.getRecord('Client', ('sex', 'birthDate'), self.clientId)
            clientSex = forceInt(clientRecord.value('sex'))
            clientBirthDate = forceDate(clientRecord.value('birthDate'))
            tableRBJobPurpose = db.table('rbJobPurpose')
            cond.append(u'isSexAndAgeSuitable(%d, %s, rbJobPurpose.sex, rbJobPurpose.age, CURRENT_DATE())' % (clientSex, db.formatDate(clientBirthDate)))
            queryTable = queryTable.leftJoin(tableRBJobPurpose, tableRBJobPurpose['id'].eq(table['jobPurpose_id']))
        idList = db.getDistinctIdList(queryTable, table['orgStructure_id'].name(), cond)
        return idList


    def _blockSignals(self, block):
        self.clnCalendar.blockSignals(block)
        self.cmbFilterOrgStructure.blockSignals(block)
        self.selectionModelJobTypes.blockSignals(block)
        self.chkShowForNextDays.blockSignals(block)


    def setDefaults(self, jobTypeCode, date):
        self._blockSignals(True)
        try:
            self.setDate(date)
            self.setJobTypeId(self.setDefaultJobType(jobTypeCode))
        finally:
            self._blockSignals(False)
        self.updateTickets()
        self.updateAddExceedButton()
        # self.tabWidget.setCurrentIndex(0 if self.modelExistensTickets.idList() else 1)


    def setTicketId(self, jobTypeCode, ticketId):
        self._blockSignals(True)
        try:
            self.ticketId = ticketId
            defaultJobTypeId = self.setDefaultJobType(jobTypeCode)
            if ticketId:
                record = getJobTicketRecord(ticketId)
                jobTypeId = forceRef(record.value('jobType_id'))
                orgStructureId = forceRef(record.value('orgStructure_id'))
                date = forceDate(record.value('date'))
                self.setJobTypeId(jobTypeId)
                self.setOrgStructureId(orgStructureId)
                self.setDate(date)
            else:
                self.setJobTypeId(defaultJobTypeId)
                self.setDate(QDate.currentDate())
        finally:
            self._blockSignals(False)
        self.updateTickets()
        self.updateAddExceedButton()
        self.tblOldTickets.setCurrentItemId(ticketId)
        self.tblTickets.setCurrentItemId(ticketId)
        self.tabWidget.setCurrentIndex(1 if self.modelExistensTickets.idList() in [[], [ticketId]] else 0)


    def getTicketId(self):
        return self.ticketId


    def setJobTypeId(self, jobTypeId):
        index = self.modelJobTypes.findItemId(jobTypeId)
        if index:
            self.treeJobTypes.setCurrentIndex(index)


    def getJobTypeId(self):
        jobTypesCurrentIndex = self.selectionModelJobTypes.currentIndex()
        return self.modelJobTypes.itemId(jobTypesCurrentIndex) if jobTypesCurrentIndex.isValid() else None


    def setDate(self, date):
        if date:
            self.clnCalendar.setSelectedDate(date)


    def getDate(self):
        return self.clnCalendar.selectedDate()


    def setOrgStructureId(self, orgStructureId):
        self.cmbFilterOrgStructure.setValue(orgStructureId)


    def getOrgStructureId(self):
        if self._filterOrgStructureId is None:
            return self.cmbFilterOrgStructure.value()
        else:
            return self._filterOrgStructureId


    def getExistentJobTicketIdList(self, jobTypeId, date):
        if jobTypeId and date:
            db = QtGui.qApp.db
            table = db.table('Job_Ticket')
            tableJob = db.table('Job')
            tableOrgStructure = db.table('OrgStructure')
            tableEx = table.leftJoin(tableJob, tableJob['id'].eq(table['master_id']))
            tableEx = tableEx.leftJoin(tableOrgStructure, tableOrgStructure['id'].eq(tableJob['orgStructure_id']))
            cond = [ tableJob['deleted'].eq(0),
                     tableJob['jobType_id'].eq(jobTypeId),
                     tableJob['date'].ge(date),
                     table['status'].eq(CJobTicketStatus.wait),
#                     table['isExceedQuantity'].eq(0),
                     db.joinOr([table['id'].inlist(QtGui.qApp.getReservedJobTickets()),
                                'EXISTS( SELECT `ActionProperty_Job_Ticket`.`id`'
                                             ' FROM `ActionProperty_Job_Ticket` '
                                             ' INNER JOIN `ActionProperty` ON `ActionProperty`.`id` = `ActionProperty_Job_Ticket`.`id`'
                                             ' INNER JOIN `Action` ON (`Action`.`id` = `ActionProperty`.`action_id` AND `Action`.`deleted` = 0)'
                                             ' INNER JOIN `Event` ON (`Event`.`id` = `Action`.`event_id` AND `Event`.`deleted` = 0 )'
                                             ' WHERE `ActionProperty_Job_Ticket`.`value` = `Job_Ticket`.`id`'
                                                   ' AND `Event`.`client_id` =%d)' % self.clientId
                               ])
                   ]
            idList = db.getIdList(tableEx, idCol='Job_Ticket.id', where=cond, order='OrgStructure.code, datetime')
        else:
            idList = []
        return idList


    def getJobTicketIdList(self, jobTypeId, date, showNextDays, orgStructureId):
        excludedList = QtGui.qApp.getReservedJobTickets() if QtGui.qApp.checkGlobalPreference(u'23:uniqJobTickets', u'да') else []
        if self.ticketId in excludedList:
            excludedList.remove(self.ticketId)
        return getJobTicketIdList(self.ticketId, jobTypeId, date, showNextDays, orgStructureId, self.eventTypeId, self.clientId, self.actionTypeId,  excludedTickets=excludedList)


    def saveData(self):
        if self._createdExceedJobTicketId is None:
            tableWidget = self.tblTickets if self.tabWidget.currentIndex() == 1 else self.tblOldTickets
            ticketId = tableWidget.currentItemId()
        else:
            ticketId = self._createdExceedJobTicketId
        if ticketId and QtGui.qApp.addJobTicketReservation(ticketId):
            self.ticketId = ticketId
        return True


    def updateTickets(self):
        jobTypeId            = self.getJobTypeId()
        orgStructureId       = self.getOrgStructureId()
        date                 = self.getDate()
        showNextDays         = self.chkShowForNextDays.isChecked()

        # date getDate() используется как хеш-функция.
        keyForExistent = jobTypeId, date.getDate()
        if  self._keyForExistent != keyForExistent:
            existentJobTicketIdListAll = self.getExistentJobTicketIdList(jobTypeId, date)
            if self.reservedJobTickets:
                existentJobTicketIdList = self.reservedJobTickets.get(self.clientId, [])
            else:
                existentJobTicketIdList = existentJobTicketIdListAll
            self.tblOldTickets.setIdList(existentJobTicketIdList)
            self.tabWidget.setTabEnabled(0, bool(existentJobTicketIdList))
            self._keyForExistent = keyForExistent

        keyForNew = jobTypeId, orgStructureId, date.getDate(), showNextDays
        if self._keyForNew != keyForNew:
            jobTicketIdList = self.getJobTicketIdList(jobTypeId, date, showNextDays, orgStructureId)
            if not self.reservedJobTickets:
                existentJobTicketIdListAll = self.tblOldTickets.model().idList()
                for existentJobTicketId in existentJobTicketIdListAll:
                    if existentJobTicketId in jobTicketIdList:
                        jobTicketIdList.remove(existentJobTicketId)
            self.tblTickets.setIdList(jobTicketIdList)
            self._keyForNew = keyForNew


    def updateAddExceedButton(self):
        enabled = (    QtGui.qApp.userHasRight(urCanAddExceedJobTicket)
                   and self.tabWidget.currentIndex() == 1
                   and getJobId( self.getJobTypeId(),
                                 self.getDate(),
                                 self.getOrgStructureId()) is not None)
        self.btnAddExceed.setEnabled(enabled)


    @pyqtSignature('QModelIndex, QModelIndex')
    def on_selectionModelJobTypes_currentChanged(self, current, previous):
        self.updateTickets()
        self.updateAddExceedButton()


    @pyqtSignature('int')
    def on_cmbFilterOrgStructure_currentIndexChanged(self, index):
        self.updateTickets()
        self.updateAddExceedButton()


    @pyqtSignature('int')
    def on_tabWidget_currentChanged(self, index):
        self.updateAddExceedButton()


    @pyqtSignature('')
    def on_clnCalendar_selectionChanged(self):
        self.updateTickets()
        self.updateAddExceedButton()


    @pyqtSignature('bool')
    def on_chkShowForNextDays_toggled(self, val):
        self.updateTickets()


    @pyqtSignature('QModelIndex')
    def on_tblOldTickets_doubleClicked(self, index):
        self.accept()


    @pyqtSignature('QModelIndex')
    def on_tblTickets_doubleClicked(self, index):
        self.accept()


    @pyqtSignature('')
    def on_btnAddExceed_clicked(self):
        orgStructureId = self.getOrgStructureId()
        jobId = getJobId(self.getJobTypeId(), self.getDate(), orgStructureId, additionalCond=self.getJobPurposeConditions(), clientId=self.clientId)
        if jobId:
            jobTicketId = createExceedJobTicket(jobId)
            if jobTicketId:
                self._createdExceedJobTicketId = jobTicketId
                self.accept()
        # else:
        #     self.checkValueMessage(u'Необходимо указать подразделение', False, self.cmbFilterOrgStructure)

    def getJobPurposeConditions(self):
        cond = []
        db = QtGui.qApp.db
        tableJob = db.table('Job')
        orgStructureId = QtGui.qApp.currentOrgStructureId()
        jobPurposeIdList = CJobTicketChooserHelper.selectJobPurposeIdList(self.clientId, self.eventTypeId, orgStructureId, True, self.actionTypeId, isFreeJobTicket=True)
        cond.append(db.joinOr(
            [tableJob['jobPurpose_id'].isNull(), tableJob['jobPurpose_id'].inlist(jobPurposeIdList)]))
        # if orgStructureId:
        #     orgStructureIdList = getOrgStructureDescendants(orgStructureId)
        #     cond.append(db.joinOr([tableJob['orgStructure_id'].inlist(orgStructureIdList),
        #                            tableJob['jobPurpose_id'].isNotNull(), ]))
        return cond

class CDateTimeOrExceedCol(CDateTimeCol):
    def __init__(self, *args, **kwargs):
        CDateTimeCol.__init__(self, *args, **kwargs)


    def format(self, values):
        datetime = values[0]
        isExceed = values[1]
        if datetime.type() == QVariant.DateTime:
            if forceBool(isExceed):
                result = u'%s, сверх плана' % datetime.toDate().toString(Qt.LocaleDate)
            else:
                result = datetime.toDateTime().toString(Qt.LocaleDate)
            return QVariant(result)
        return CCol.invalid


class CTicketsModel(CTableModel):
    def __init__(self, parent):
        CTableModel.__init__(self, parent,  [
            CDesignationCol(u'Подразделение',['master_id'], [('Job', 'orgStructure_id'),
                                                             ('OrgStructure', 'code')], 25),

            CDesignationCol(u'Назначение',   ['master_id'], [('Job', 'jobPurpose_id'),
                                                             ('rbJobPurpose', 'name')], 25),

            CDateTimeOrExceedCol(u'Дата и время', ['datetime', 'isExceedQuantity'],  25),
            ], 'Job_Ticket' )

