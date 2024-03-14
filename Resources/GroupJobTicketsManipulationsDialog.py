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

from PyQt4 import QtGui, QtCore

from Events.Action import CAction

from Users.Rights import urAccessJobsPlanning, urAdmin

from JobTicketChooserHelper import CJobTicketChooserHelper
from JobPlanner import CJobPlanner

from library.TableModel import CTableModel, CRefBookCol, CBoolCol, CTextCol
from library.crbcombobox import CRBComboBox
from library.Utils import exceptionToUnicode, forceRef, formatName, forceString, forceInt, formatNameByRecord
from library.RecordLock import CRecordLockMixin
from library.DialogBase import CDialogBase

from Resources.JobSchedule import COrgStructureJobTemplate

from Ui_GroupJobTicketsManipulationsDialog import Ui_GroupJobTicketsManipulationsDialog
from Ui_ActionJobTicketJobTypeChangerDialog import Ui_ActionJobTicketJobTypeChangerDialog


class CBaseJobTicketChanger(CDialogBase, CRecordLockMixin):
    def __init__(self, jobTicketIdList, jobTypeId, parent):
        CDialogBase.__init__(self, parent)
        CRecordLockMixin.__init__(self)
        self._parent = parent
        self._jobTicketIdList = jobTicketIdList if isinstance(jobTicketIdList, (list, tuple)) else [jobTicketIdList]
        self._jobTypeId = jobTypeId
        self._execOnce = True

    def _confirmLock(self, message):
        self._notLockedActionsInfo[self._currentActionId] = message
        return False

    def apply(self):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

    def _checkNotApplied(self):
        raise NotImplementedError

    def exec_(self):
        QtGui.qApp.setJTR(self)
        try:
            result = None
            while True:
                if not self._execOnce or result is None:
                    result = CDialogBase.exec_(self)
                if result == QtGui.QDialog.Accepted:
                    QtGui.qApp.callWithWaitCursor(self, self.apply)
                    if self._checkNotApplied():
                        break
                    self.reset()
                else:
                    break
            return result
        finally:
            QtGui.qApp.unsetJTR(self)


    def _getMainQueryAndCond(self):
        db = QtGui.qApp.db
        tableJT = db.table('Job_Ticket')
        tableJob = db.table('Job')
        tableAPJT = db.table('ActionProperty_Job_Ticket')
        tableAP = db.table('ActionProperty')
        tableAction = db.table('Action')
        tableEvent = db.table('Event')
        tableClient = db.table('Client')
        tableOrgStructure = db.table('OrgStructure')
        queryTable = tableJT
        queryTable = queryTable.innerJoin(tableJob, tableJob['id'].eq(tableJT['master_id']))
        queryTable = queryTable.leftJoin(tableOrgStructure, tableOrgStructure['id'].eq(tableJob['orgStructure_id']))
        queryTable = queryTable.leftJoin(tableAPJT, tableAPJT['value'].eq(tableJT['id']))
        queryTable = queryTable.leftJoin(tableAP, tableAP['id'].eq(tableAPJT['id']))
        queryTable = queryTable.leftJoin(tableAction, tableAction['id'].eq(tableAP['action_id']))
        queryTable = queryTable.leftJoin(tableEvent, tableEvent['id'].eq(tableAction['event_id']))
        queryTable = queryTable.leftJoin(tableClient, tableClient['id'].eq(tableEvent['client_id']))

        cond = [tableJT['id'].inlist(self._jobTicketIdList),
                tableAction['deleted'].eq(0),
                tableEvent['deleted'].eq(0),
                tableClient['deleted'].eq(0),
                ]

        return queryTable, cond


class CGroupJobTicketsManipulationsDialog(CBaseJobTicketChanger, Ui_GroupJobTicketsManipulationsDialog):

    def __init__(self, jobTicketIdList, jobTypeId, parent):
        CBaseJobTicketChanger.__init__(self, jobTicketIdList, jobTypeId, parent)
        self.setupUi(self)
        self._jobTicketId2Data = {}
        self._actionId2JobTicketId = {}
        self._notLockedActionsInfo = {}
        self._jobTicketIdListWithoutPlan = []
        self.calendar.setMinimumDate(QtCore.QDate.currentDate())
        self.setWindowTitle(u'Групповое изменение номерка')
        self._presetOrgStrustureValues()

    def reset(self):
        self._jobTicketId2Data = {}
        self._actionId2JobTicketId = {}
        self._notLockedActionsInfo = {}
        self._jobTicketIdListWithoutPlan = []

    def apply(self):
        self.__loadData()
        self.__applyChanges()

    def _checkNotApplied(self):
        if self._jobTicketIdListWithoutPlan or self._notLockedActionsInfo:
            targetOrgStructureId = self.cmbOrgStructure.value()
            if targetOrgStructureId:
                targetOrgStructureData = {'orgStructureName': self.cmbOrgStructure.currentText(),
                                          'orgStructureId': targetOrgStructureId}
            else:
                targetOrgStructureData = None
            result = CNotAppliedInfoDialog(self._jobTicketIdListWithoutPlan,
                                           self._notLockedActionsInfo,
                                           self._jobTicketId2Data,
                                           self._actionId2JobTicketId,
                                           targetOrgStructureData,
                                           self.calendar.selectedDate(),
                                           self._parent).exec_()
            return result != QtGui.QDialog.Accepted
        return True

    def _presetOrgStrustureValues(self):
        self.cmbOrgStructure.setFilter(self.__getFilterByJobType())
        self.cmbOrgStructure.setValue(self.__getValueForCmbOrgStructure())

    def __getFilterByJobType(self):
        db = QtGui.qApp.db
        tableOrgStructure = db.table('OrgStructure')
        tableOrgStructuerJobTemplate = db.table('OrgStructure_JobTemplate')
        idList = db.getDistinctIdList(tableOrgStructuerJobTemplate,
                                      tableOrgStructuerJobTemplate['master_id'],
                                      tableOrgStructuerJobTemplate['jobType_id'].eq(self._jobTypeId))
        return tableOrgStructure['id'].inlist(db.getTheseAndParents(tableOrgStructure, 'parent_id', idList))

    def __getValueForCmbOrgStructure(self):
        db = QtGui.qApp.db
        tableJob = db.table('Job')
        tableJobTicket = db.table('Job_Ticket')

        queryTable = tableJob.leftJoin(tableJobTicket,
                                       tableJobTicket['master_id'].eq(tableJob['id']))

        orgStrucrureIdList = db.getDistinctIdList(queryTable, tableJob['orgStructure_id'],
                                                        tableJobTicket['id'].inlist(self._jobTicketIdList))

        return orgStrucrureIdList[0] if len(orgStrucrureIdList) == 1 else None

    def __applyChanges(self):
        db = QtGui.qApp.db

        for jobTicketId, data in self._jobTicketId2Data.items():
            newJobId = data['newJobId']
            if not newJobId:
                continue

            for actionId, eventTypeId in data['actionsData']:
                self._currentActionId = actionId
                if not self.lock('Action', actionId):
                    self.releaseLock()
                    break

            clientId = data['clientId']
            # eventTypeId в запросе не участвует, так как мы передаем newJobId. Так что подсовываем None
            chooserHelper = CJobTicketChooserHelper(self._jobTypeId, clientId, None, 1, None)
            reservedTicketId = chooserHelper.selectFreeJobTicket(newJobId)

            db.transaction()
            try:
                newTicketId = reservedTicketId or chooserHelper.createExceedJobTicket(newJobId)
                for actionId, _ in data['actionsData']:
                    action = CAction.getActionById(actionId)
                    actionType = action.getType()
                    propertyTypeList = actionType.getPropertiesById().values() if actionType else []
                    for propertyType in propertyTypeList:
                        if propertyType.isJobTicketValueType():
                            property = action.getPropertyById(propertyType.id)
                            actionJobTicketId = property.getValue()
                            if actionJobTicketId != jobTicketId:
                                continue
                            property.setValue(newTicketId)
                            action.save()
                            break

                self._jobTicketIdList.remove(jobTicketId)
                db.commit()
                self._endStep(reservedTicketId)

            except Exception as e:
                db.rollback()
                self._endStep(reservedTicketId)
                QtGui.qApp.logCurrentException()
                QtGui.QMessageBox.critical(self,
                                           u'Произошла ошибка',
                                           exceptionToUnicode(e),
                                           QtGui.QMessageBox.Close)

    def _endStep(self, reservedTicketId):
        self.releaseLock()

    def __loadData(self):
        db = QtGui.qApp.db
        tableJT = db.table('Job_Ticket')
        tableJob = db.table('Job')
        tableAPJT = db.table('ActionProperty_Job_Ticket')
        tableAction = db.table('Action')
        tableEvent = db.table('Event')
        tableClient = db.table('Client')
        tableOrgStructure = db.table('OrgStructure')

        queryTable, cond = self._getMainQueryAndCond()

        tableNewJob = db.table('Job').alias('NewJob')

        targetOrgStructure = self.cmbOrgStructure.value()
        if targetOrgStructure:
            newOrgStructureCond = tableNewJob['orgStructure_id'].eq(targetOrgStructure)
        else:
            newOrgStructureCond = tableNewJob['orgStructure_id'].eq(tableJob['orgStructure_id'])
        newJobIdStmt = db.selectStmt(tableNewJob, tableNewJob['id'],
                                     [tableNewJob['deleted'].eq(0),
                                      tableNewJob['jobType_id'].eq(tableJob['jobType_id']),
                                      tableNewJob['date'].eq(self.calendar.selectedDate()),
                                      newOrgStructureCond],
                                     order='NewJob.jobPurpose_id <=> Job.jobPurpose_id',
                                     limit=1)

        fields = [tableJT['id'].alias('jobTicketId'),
                  tableAction['id'].alias('actionId'),
                  tableEvent['eventType_id'],
                  tableClient['firstName'],
                  tableClient['lastName'],
                  tableClient['patrName'],
                  tableClient['id'].alias('clientId'),
                  tableAPJT['id'].alias('APJTId'),
                  tableOrgStructure['name'].alias('orgStructureName'),
                  tableOrgStructure['id'].alias('orgStructureId'),
                  '(%s) AS newJobId' % newJobIdStmt
                  ]

        stmt = db.selectStmt(queryTable, fields, cond)
        query = db.query(stmt)

        while query.next():
            record = query.record()
            jobTicketId = forceRef(record.value('jobTicketId'))
            newJobId = forceRef(record.value('newJobId'))
            if not newJobId:
                self._jobTicketIdListWithoutPlan.append(jobTicketId)

            actionId = forceRef(record.value('actionId'))
            eventTypeId = forceRef(record.value('eventType_id'))
            clientId = forceRef(record.value('clientId'))
            APJTId = forceRef(record.value('APJTId'))

            if jobTicketId in self._jobTicketId2Data:
                self._jobTicketId2Data[jobTicketId]['actionsData'].append((actionId, eventTypeId))
            else:
                data = {'actionsData': [(actionId, eventTypeId)],
                        'clientId': clientId,
                        'APJTId': APJTId,
                        'newJobId': newJobId,
                        'orgStructureName': forceString(record.value('orgStructureName')),
                        'orgStructureId': forceRef(record.value('orgStructureId')),
                        'clientName': formatName(record.value('lastName'),
                                                 record.value('firstName'),
                                                 record.value('patrName'))}

                self._jobTicketId2Data[jobTicketId] = data

            self._actionId2JobTicketId[actionId] = jobTicketId

# #######################################################

class CJobTicketJobTypeChangerDialog(CBaseJobTicketChanger, Ui_ActionJobTicketJobTypeChangerDialog):
    def __init__(self, jobTicketId, jobTypeId, jtDatetime, clientId, parent):
        CBaseJobTicketChanger.__init__(self, jobTicketId, jobTypeId, parent)
        self._execOnce = False
        self._actionId2Selected = {}
        self._jobTypeId2Selected = {}
        self._jobTypeId2ActionIdList = {}
        self._jobType2EventTypeData = {}
        self._actionId2JobTypeId = {}
        self._actionId2AvailableJobTypeIdList = {}
        self._actionId2Data = {}
        self._eventTypeId2Actions = {}
        self._notLockedActionsInfo = {}
        self._actionIdList = []
        self._jobTypeIdList = []
        self._orgStrucureIdList = []
        self._jobType2OrgSTructureIdList = {}
        self._jobTypeIdWithoutPlan = None
        self.addModels('Actions', CLocActionsModel(self))
        self.addModels('JobTypes', CLocJobTypesModel(self))
        self.setupUi(self)
        db = QtGui.qApp.db
        clientName = formatNameByRecord(db.getRecord('Client', 'firstName, lastName, patrName', clientId))
        jobTypeName = forceString(db.translate('rbJobType', 'id', jobTypeId, 'name'))
        self.setWindowTitle(u'Изменение типа работы `%s` %s' % (jobTypeName, clientName))
        self.setModels(self.tblActions, self.modelActions, self.selectionModelActions)
        self.setModels(self.tblJobTypes, self.modelJobTypes, self.selectionModelJobTypes)

        self.connect(self.modelActions, QtCore.SIGNAL('reloadDependents()'), self.modelJobTypes.emitDataChanged)
        self.connect(self.modelJobTypes, QtCore.SIGNAL('reloadDependents()'), self.modelActions.emitDataChanged)
        self.connect(self.selectionModelJobTypes,
                     QtCore.SIGNAL('currentChanged(QModelIndex, QModelIndex)'),
                     self.on_jobTypesSelectedItemChanged)

        self._jtDatetime = jtDatetime
        self._clientId = clientId

        self.setupData()

    def on_jobTypesSelectedItemChanged(self, index1, index2):
        self.modelActions.emitDataChanged()

    def reset(self):
        # Тут данные почти не нужно сбрасывать, только при новом открытии окна,
        # а новая попытка должна использоваться с уже загруженными днными,
        # так как в этом случае или все или ничего.
        self._notLockedActionsInfo = {}

    def apply(self):
        self._jobTypeIdWithoutPlan = self.__applyChanges()

    def isActionSelected(self, actionId):
        return self._actionId2Selected.get(actionId, False)

    def setActionSelected(self, actionId, value):
        jobTypeId = self.tblJobTypes.currentItemId()
        eventTypeId = self._actionId2Data[actionId]['eventTypeId']
        actionIdList = self._jobTypeId2ActionIdList.setdefault(jobTypeId, [])

        if value:
            self._actionId2JobTypeId[actionId] = jobTypeId
            actionId not in actionIdList and actionIdList.append(actionId)
            self._jobType2EventTypeData.setdefault(jobTypeId, {}).setdefault(eventTypeId, []).append(actionId)

        else:
            # Учитывая, что у нас стоят ограничения на возможность добавлять action к разным jobType-ам,
            # данные для удаления должны быть. Будут ошибки - сразу пойму что что-то не так.
            del self._actionId2JobTypeId[actionId]
            actionIdList.remove(actionId)
            self._jobType2EventTypeData[jobTypeId][eventTypeId].remove(actionId)
        self._actionId2Selected[actionId] = value


    def isJobTypeSelected(self, jobTypeId):
        return self._jobTypeId2Selected.get(jobTypeId, False)

    def setJobTypeSelected(self, jobTypeId, value):
        self._jobTypeId2Selected[jobTypeId] = value

    def getActionsCountByJobTypeId(self, jobTypeId):
        return len(self._jobTypeId2ActionIdList.get(jobTypeId, []))

    def setupData(self):
        db = QtGui.qApp.db
        tableAction = db.table('Action')
        tableEvent = db.table('Event')
        tableActionProperty = db.table('ActionProperty')
        tableActionTypeTissueType = db.table('ActionType_TissueType')
        tableOrgStructure = db.table('OrgStructure')
        tableOrgStructureJobTemplate = db.table(COrgStructureJobTemplate.tableName)


        queryTable, cond = self._getMainQueryAndCond()

        queryTable = queryTable.leftJoin(tableActionTypeTissueType,
                                         tableActionTypeTissueType['master_id'].eq(tableAction['actionType_id']))

        jtOrgStructures = '(SELECT GROUP_CONCAT({id_name}) FROM {table_name} WHERE  {cond}) AS orgStructures'.format(
            id_name=tableOrgStructureJobTemplate['master_id'].name(),
            table_name=tableOrgStructureJobTemplate.name(),
            cond=db.joinAnd([tableOrgStructureJobTemplate['jobType_id'].eq(tableActionTypeTissueType['jobType_id']),
                             tableActionTypeTissueType['master_id'].eq(tableAction['actionType_id'])])
        )

        fields = [tableActionTypeTissueType['jobType_id'].alias('jobTypeId'),
                  tableAction['id'].alias('actionId'),
                  tableActionProperty['type_id'].alias('propertyTypeId'),
                  tableEvent['eventType_id'].alias('eventTypeId'),
                  jtOrgStructures]

        cond.append(tableActionTypeTissueType['jobType_id'].ne(self._jobTypeId))

        stmt = db.selectStmt(queryTable, fields, cond)
        query = db.query(stmt)
        orgStrucureIdList = []
        while query.next():
            record = query.record()
            actionId = forceRef(record.value('actionId'))
            eventTypeId = forceRef(record.value('eventTypeId'))
            jobTypeOrgStructures = [int(v) for v in forceString(record.value('orgStructures')).split(',') if v]
            actionId not in self._actionIdList and self._actionIdList.append(actionId)

            orgStrucureIdList.extend(jobTypeOrgStructures)

            jobTypeId = forceRef(record.value('jobTypeId'))
            if (jobTypeId and jobTypeId != self._jobTypeId and jobTypeId not in self._jobTypeIdList):
                self._jobTypeIdList.append(jobTypeId)

            self._jobType2OrgSTructureIdList.setdefault(jobTypeId, []).extend(jobTypeOrgStructures)
            self._actionId2AvailableJobTypeIdList.setdefault(actionId, set()).add(jobTypeId)

            self._actionId2Data[actionId] = {'propertyTypeId': forceRef(record.value('propertyTypeId')),
                                             'eventTypeId': eventTypeId}

            self._eventTypeId2Actions.setdefault(eventTypeId, set()).add(actionId)

        self._orgStrucureIdList = db.getTheseAndParents(tableOrgStructure, 'parent_id', orgStrucureIdList)
        cmbOrgStructureFilter = tableOrgStructure['id'].inlist(self._orgStrucureIdList)
        self.cmbOrgStructure.setFilter(cmbOrgStructureFilter)
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())

        if self._jobTypeIdList:
            self.tblActions.setIdList(self._actionIdList)
            self.tblJobTypes.setIdList(self._jobTypeIdList)
            if len(self._jobTypeIdList) == 1:
                self.setJobTypeSelected(self._jobTypeIdList[0], True)

    def exec_(self):
        if not self._jobTypeIdList:
            QtGui.QMessageBox.information(self, u'Внимание',
                                          u'В справочнике типов действий не настроены альтернативные типы работ',
                                          QtGui.QMessageBox.Ok)
            return QtGui.QDialog.Rejected
        return CBaseJobTicketChanger.exec_(self)

    def isActionEnabled(self, actionId):
        jobTypeId = self.tblJobTypes.currentItemId()
        return (jobTypeId in self._actionId2AvailableJobTypeIdList[actionId]
                and (actionId not in self._actionId2JobTypeId
                     or self._actionId2JobTypeId[actionId] == jobTypeId))

    def isJobTypeEnabled(self, jobTypeId):
        return True

    def _lockActions(self):
        for actionId, selected in self._actionId2Selected.items():
            if not selected:
                continue
            if not self.lock('Action', actionId):
                self.releaseLock()
                return False
        return True

    def __applyChanges(self):
        if not self._lockActions():
            return None

        try:
            begDate, endDate = self._jtDatetime, self._jtDatetime.addSecs(60 * 5)
            targetDate = (begDate, endDate)

            db = QtGui.qApp.db
            db.transaction()

            for jobTypeId, selected in self._jobTypeId2Selected.items():
                if not selected:
                    continue

                jobTypeData = self._jobType2EventTypeData.get(jobTypeId, None)
                if not jobTypeData:
                    continue

                for eventTypeId, actionIdList in jobTypeData.items():
                    chooserHelper = CJobTicketChooserHelper(jobTypeId, self._clientId, eventTypeId, 1, targetDate)
                    chooserHelper.jobOrgStructureIdList = self._getCmbOrgStructureIdList()
                    reservedTicketId = chooserHelper.get()

                    if reservedTicketId:
                        newTicketId = reservedTicketId
                    else:
                        newJobId = chooserHelper.getJobIdForSelect(date=self._jtDatetime)
                        if newJobId:
                            newTicketId = chooserHelper.createExceedJobTicket(newJobId)
                        else:
                            db.rollback()
                            self.releaseLock()
                            return jobTypeId

                    for actionId in actionIdList:
                        if not self._actionId2Selected.get(actionId, False):
                            continue
                        actionData = self._actionId2Data[actionId]
                        propertyTypeId = actionData['propertyTypeId']

                        action = CAction.getActionById(actionId)
                        property = action.getPropertyById(propertyTypeId)
                        property.setValue(newTicketId)
                        action.save()

            db.commit()
            self.releaseLock()

        except Exception as e:
            db.rollback()
            self.releaseLock()
            QtGui.qApp.logCurrentException()
            QtGui.QMessageBox.critical(self,
                                       u'Произошла ошибка',
                                       exceptionToUnicode(e),
                                       QtGui.QMessageBox.Close)

    def _getCmbOrgStructureIdList(self):
        item = self.cmbOrgStructure.currentModelIndex().internalPointer()
        return item.getItemIdList() if item else self._orgStrucureIdList

    def _checkNotApplied(self):
        if self._jobTypeIdWithoutPlan or self._notLockedActionsInfo:
            if self._jobTypeIdWithoutPlan:
                jtname = forceString(QtGui.qApp.db.translate('rbJobType', 'id', self._jobTypeIdWithoutPlan, 'name'))
                message = u'На тип работы "%s" отсутствует расписание. ' % jtname
                v = (QtGui.qApp.currentOrgId() and (QtGui.qApp.userHasAnyRight([urAccessJobsPlanning, urAdmin])))
                if v:
                    message += u'Составить расписание?'
                    buttons = QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel
                else:
                    buttons = QtGui.QMessageBox.Close
            else:
                lockInfo = self._notLockedActionsInfo.values()[0]
                message = u'Связанное действие заблокировано другим пользователем "%s". Попробовать снова?' % lockInfo
                buttons = QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel

            if QtGui.QMessageBox.question(
                    self, u'Тип работы не был сменен!', message,
                    buttons) == QtGui.QMessageBox.Ok:

                if self._jobTypeIdWithoutPlan:
                    targetOrgStructure = self._getTargetOrgStructure()
                    planner = CJobPlanner(self, targetOrgStructure)
                    planner.exec_()

                return False
        return True

    def _getTargetOrgStructure(self):
        orgStructureId = self.cmbOrgStructure.value()
        db = QtGui.qApp.db

        tableOrgStructureJobTemplate = db.table(COrgStructureJobTemplate.tableName)
        cond = [tableOrgStructureJobTemplate['master_id'].eq(orgStructureId),
                tableOrgStructureJobTemplate['jobType_id'].eq(self._jobTypeIdWithoutPlan)]
        stmt = 'SELECT %s' % db.existsStmt(tableOrgStructureJobTemplate, cond)
        query = db.query(stmt)
        if query.first():
            if query.value(0).toBool():
                return orgStructureId

        tableOrgStructure = db.table('OrgStructure')
        descendants = db.getDescendants(tableOrgStructure, 'parent_id', orgStructureId)
        stmt = db.selectStmt(tableOrgStructureJobTemplate,
                             tableOrgStructureJobTemplate['master_id'],
                             [tableOrgStructureJobTemplate['master_id'].inlist(descendants),
                              tableOrgStructureJobTemplate['jobType_id'].eq(self._jobTypeIdWithoutPlan)],
                             order='%s DESC' % db.notExistsStmt(
                                 tableOrgStructure,
                                 tableOrgStructure['parent_id'].ne(tableOrgStructureJobTemplate['master_id'])),
                             limit=1)

        query = db.query(stmt)
        if query.first():
            result = forceRef(query.value(0))
            if result:
                return result

        parents = db.getTheseAndParents(tableOrgStructure, 'parent_id', [orgStructureId])
        queryTable = tableOrgStructureJobTemplate.innerJoin(tableOrgStructure,
                                                       tableOrgStructure['id'].eq(
                                                           tableOrgStructureJobTemplate['master_id']))
        stmt = db.selectStmt(queryTable,
                             tableOrgStructureJobTemplate['master_id'],
                             [tableOrgStructureJobTemplate['master_id'].inlist(parents),
                              tableOrgStructureJobTemplate['jobType_id'].eq(self._jobTypeIdWithoutPlan)],
                             order='%s DESC' % tableOrgStructure['parent_id'].isNull(),
                             limit=1)

        query = db.query(stmt)
        if query.first():
            result = forceRef(query.value(0))
            if result:
                return result


        return forceRef(db.translate(tableOrgStructureJobTemplate,
                                     tableOrgStructureJobTemplate['jobType_id'],
                                     self._jobTypeIdWithoutPlan,
                                     tableOrgStructureJobTemplate['master_id']))


class CLocEnableCol(CBoolCol):
    def __init__(self, title, fields, defaultWidth, selector, isSelectedGetterMethodName):
        self.isSelectedGetterMethodName = isSelectedGetterMethodName
        CBoolCol.__init__(self, title, fields, defaultWidth)
        self.selector = selector

    def checked(self, values):
        actionId = forceRef(values[0])
        if getattr(self.selector, self.isSelectedGetterMethodName)(actionId):
            return CBoolCol.valChecked
        else:
            return CBoolCol.valUnchecked



class CLocBaseCheckingModel(CTableModel):
        def __init__(self, parent, cols, tableName, setCheckedMethodName, isEnabledMethodName):
            self._parent = parent
            self.setCheckedMethodName = setCheckedMethodName
            self.isEnabledMethodName = isEnabledMethodName
            CTableModel.__init__(self, parent, cols, tableName)

        def flags(self, index):
            result = CTableModel.flags(self, index)
            if index.column() == 0:
                result |= QtCore.Qt.ItemIsUserCheckable
            if not getattr(self._parent, self.isEnabledMethodName)(self._idList[index.row()]):
                result ^= QtCore.Qt.ItemIsEnabled
            return result

        def data(self, index, role=QtCore.Qt.DisplayRole):
            if not index.isValid():
                return QtCore.QVariant()
            else:
                return CTableModel.data(self, index, role)

        def setData(self, index, value, role=QtCore.Qt.EditRole):
            if role == QtCore.Qt.CheckStateRole:
                row = index.row()
                getattr(self._parent, self.setCheckedMethodName)(self._idList[row],
                                                                 forceInt(value) == QtCore.Qt.Checked)
                self.emitDataChanged()
                self.emitReloadDependents()
                return True
            return False

        def emitReloadDependents(self):
            self.emit(QtCore.SIGNAL('reloadDependents()'))


class CLocActionsModel(CLocBaseCheckingModel):
    def __init__(self, parent):
        CLocBaseCheckingModel.__init__(self, parent,
                                       [CLocEnableCol(u'Включить', ['id'], 20, parent, 'isActionSelected'),
                                        CRefBookCol(u'Действие', ['actionType_id'], 'ActionType', 20,
                                                    showFields=CRBComboBox.showCodeAndName)],
                                       'Action',
                                       'setActionSelected',
                                       'isActionEnabled')

class CLocJobTypesModel(CLocBaseCheckingModel):
    ACTIONS_COUNT_COLUMN = 2

    def __init__(self, parent):
        CLocBaseCheckingModel.__init__(self, parent,
                                       [CLocEnableCol(u'Включить', ['id'], 20, parent, 'isJobTypeSelected'),
                                        CTextCol(u'Тип работы', ['name'], 20)],
                                      'rbJobType',
                                      'setJobTypeSelected',
                                      'isJobTypeEnabled')

    def columnCount(self, index=None):
        return 3

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if section == 2 and orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                return QtCore.QVariant(u'Кол-во')
            return QtCore.QVariant()
        return CTableModel.headerData(self, section, orientation, role)

    def flags(self, index):
        if index.column() == self.ACTIONS_COUNT_COLUMN:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        return CLocBaseCheckingModel.flags(self, index)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return QtCore.QVariant()
        else:
            if index.column() == self.ACTIONS_COUNT_COLUMN:
                if role == QtCore.Qt.DisplayRole:
                    return QtCore.QVariant(self._parent.getActionsCountByJobTypeId(self._idList[index.row()]))
                return QtCore.QVariant()
            return CTableModel.data(self, index, role)

# #######################################################


class CNotAppliedInfoDialog(CDialogBase):
    def __init__(self, planNotExistsJTIdList, notLockedActionInfo, jobTicketsData, action2JT,
                 targetStructureData, date, parent):
        CDialogBase.__init__(self, parent)
        self.setWindowTitle(u'Информация о номерках')
        self._date = date
        self._targetStructureData = targetStructureData
        self._orgStructureIdListForPlan = set([])
        self.edtText = QtGui.QTextEdit(self)
        self.edtText.setReadOnly(True)
        self.vLayout = QtGui.QVBoxLayout()
        self.vLayout.addWidget(self.edtText)
        self.btnOpenPlan = QtGui.QPushButton(u'Добавить расписание', self)
        self.vLayout.addWidget(self.btnOpenPlan)
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel)
        self.vLayout.addWidget(self.buttonBox)
        self.setLayout(self.vLayout)
        self.connect(self.buttonBox, QtCore.SIGNAL('accepted()'), self.accept)
        self.connect(self.buttonBox, QtCore.SIGNAL('rejected()'), self.reject)
        self.connect(self.btnOpenPlan, QtCore.SIGNAL('clicked()'), self.openPlan)
        self.setInfo(planNotExistsJTIdList, notLockedActionInfo, jobTicketsData, action2JT)
        self.setOpenPlanVisible(planNotExistsJTIdList)

    def setOpenPlanVisible(self, planNotExistsJTIdList):
        v = (QtGui.qApp.currentOrgId() and bool(planNotExistsJTIdList)
             and (QtGui.qApp.userHasAnyRight([urAccessJobsPlanning, urAdmin])))
        self.btnOpenPlan.setVisible(v)

    def setInfo(self, planNotExistsJTIdList, notLockedActionInfo, jobTicketsData, action2JT):
        settedClientId = {}
        orgStructures = {}

        if planNotExistsJTIdList:
            for jobTicketId in planNotExistsJTIdList:
                data = jobTicketsData[jobTicketId]
                orgStructureData = self._targetStructureData if self._targetStructureData else data
                orgStructureName = orgStructureData['orgStructureName']
                orgStructureId = orgStructureData['orgStructureId']
                clientId = data['clientId']
                if not orgStructureId in orgStructures:
                    self._orgStructureIdListForPlan.add(orgStructureId)
                    orgStructures[orgStructureId] = orgStructureName
                if not clientId in settedClientId:
                    settedClientId[clientId] = data['clientName']

        if notLockedActionInfo:
            for actionId, info in notLockedActionInfo.items():
                jobTicketId = action2JT[actionId]
                data = jobTicketsData[jobTicketId]
                clientId = data['clientId']
                if not clientId in settedClientId:
                    settedClientId[clientId] = data['clientName']

        self.edtText.append(u'Номерки не могут быть изменены для:\n')
        for clientName in sorted(settedClientId.values()):
            self.edtText.append('    %s' % clientName)

        self.edtText.append('')
        for orgStructureName in sorted(orgStructures.values()):
            self.edtText.append(u'Не добавлено расписание для "%s" на выбранный день "%s"\n' % (orgStructureName,
                                                                                              forceString(self._date)))

        for actionId, info in notLockedActionInfo.items():
            self.edtText.append(u'Действие с идентификатором "%s": %s\n' % (actionId, info))

    def openPlan(self):
        orgStructureId = (self._orgStructureIdListForPlan and self._orgStructureIdListForPlan.pop()) or None
        CJobPlanner(self, orgStructureId).exec_()
