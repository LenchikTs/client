# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2013 Chuk&Gek and Vista Software. All rights reserved.
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
from PyQt4.QtCore import *

from library.Utils      import *

from Orgs.Utils         import *
from Registry.Utils     import *

from Reports.Report     import CReportEx, CVoidSetupDialog
from Reports.ReportBase import CReportBase

from Ui_ReportPayersSetup import Ui_ReportPayersSetupDialog

def selectData(params):
    clientId               = params.get('clientId', None)
    eventIdList            = params.get('eventIdList', None)

    db = QtGui.qApp.db
    tableEvent = db.table('Event')
    stmt = """
SELECT Event.id AS eventId,
       Event.setDate AS eventBegDate,
       Event.execDate AS eventEndDate,
       CONCAT(EventType.name, ' ', EventType.mesCodeMask) AS eventTypeAndMES,
       CONCAT(EventPerson.lastName, ' ', EventPerson.firstName, ' ', EventPerson.patrName) AS eventPerson,

       Action.id AS actionId,
       Action.begDate AS actionBegDate,
       Action.endDate AS actionEndDate,
       CONCAT(ActionPerson.lastName, ' ', ActionPerson.firstName, ' ', ActionPerson.patrName) AS actionPerson,
       Action.amount AS actionAmount,
       IFNULL(NULLIF(Action.MKB, ''), Diagnosis.MKB) AS actionDiagnosis,

       Account_Item.number    AS eventAccountNumber,
       Account_Item.date      AS eventAccountDate,
       Account_Item.price AS actionPrice,
       Account_Item.sum   AS actionSum,
       Organisation.shortName AS clientSMO,
       rbService.infis AS serviceCode,
       rbService.name AS serviceName
FROM Action
INNER JOIN Event ON Event.id = Action.event_id
INNER JOIN EventType ON EventType.id = Event.eventType_id
INNER JOIN Client ON Client.id = Event.client_id
LEFT  JOIN Person AS EventPerson ON Event.execPerson_id = EventPerson.id
LEFT  JOIN Person AS ActionPerson ON Action.person_id = ActionPerson.id
LEFT  JOIN Account_Item ON Account_Item.action_id = Action.id
                           AND Account_Item.deleted = 0
                           AND Account_Item.reexposeItem_id IS NULL
                           AND EXISTS(SELECT 1
                                      FROM Account
                                      WHERE Account.id = Account_Item.master_id
                                        AND Account.deleted = 0)
LEFT  JOIN Diagnosis ON Diagnosis.id = getEventDiagnosis(Event.id)
LEFT  JOIN ClientPolicy ON ClientPolicy.id = getClientPolicyIdForDate(Event.client_id, IF(Action.finance_id = 3, 0, 1), Event.execDate, Event.id)
LEFT  JOIN Organisation  ON ClientPolicy.insurer_id = Organisation.id
LEFT  JOIN rbService ON rbService.id = IFNULL(Account_Item.service_id,
                                              IFNULL((SELECT ActionType_Service.service_id
                                                     FROM ActionType_Service
                                                     WHERE ActionType_Service.master_id = Action.actionType_id
                                                       AND ActionType_Service.finance_id = Action.finance_id
                                                     ORDER BY ActionType_Service.idx
                                                     LIMIT 1),
                                                     (SELECT ActionType_Service.service_id
                                                     FROM ActionType_Service
                                                     WHERE ActionType_Service.master_id = Action.actionType_id
                                                       AND ActionType_Service.finance_id IS NULL
                                                     ORDER BY ActionType_Service.idx
                                                     LIMIT 1)
                                                    )
                                             )
WHERE
    Client.id = %d
    AND Action.deleted = 0
    AND %s
    """%(clientId, tableEvent['id'].inlist(eventIdList))
    #print stmt
    return db.query(stmt)


class CReportClientServices(CReportEx):
    def __init__(self, parent, clientId, eventIds):
        CReportEx.__init__(self, parent, title=u'Сводка об услугах на пациента')
        self.table_columns = [
                        ('10%',
                        [u'Код случая / услуга'], CReportBase.AlignRight),
                        ('10%',
                        [u'Дата открытия случая / дата начала услуги'], CReportBase.AlignRight),
                        ('10%',
                        [u'Дата закрытия случая / дата окончания услуги'], CReportBase.AlignRight),
                        ('10%',
                        [u'Кол.-во усл. / кратн. усл.'], CReportBase.AlignRight),
                        ('10%',
                        [u'Плательщик / тариф услуги '], CReportBase.AlignRight),
                        ('10%',
                        [u'Тип случая / стоим. усл.'], CReportBase.AlignRight),
                        ('10%',
                        [u'Номер счета / профиль'], CReportBase.AlignRight),
                        ('10%',
                        [u'Номер счета / профиль'], CReportBase.AlignRight),
                        ('10%',
                        [u'Услуга'], CReportBase.AlignRight),
                        ('10%',
                        [u'Врач по случаю лечения / врач по услуге'], CReportBase.AlignRight)
                       ]
        self._clientId = clientId
        self._eventIds = eventIds


    def getSetupDialog(self, parent):
        result = CVoidSetupDialog(self) #CReportClientServicesSetup(parent, self)
        result.setParams({'clientId': self._clientId,
                          'eventIdList': self._eventIds})
#        result.setTitle(self.title())
#        print result.params()['clientId']
        return result


    def getDescription(self, params):
        clientInfo = getClientInfo2(self._clientId)
        rows = []
        rows.append(u'ФИО: %s' % clientInfo.fullName)
        rows.append(u'НАК: %d  пол: %s  дата рождения: %s' % (clientInfo.id, clientInfo.sex, clientInfo.birthDate))
        rows.append(u'Полис: %s' % clientInfo.policy)
        rows.append(u'Документ: %s' % clientInfo.document)
        rows.append(u'Адрес регистрации: %s' % clientInfo.regAddress)
        return rows


    def buildInt(self, params, cursor):
        #print params['clientId']
        query = selectData(params)
        result = self.getReportData(query, params)
        #print result

        table = self.createTable(cursor)

        boldChars = QtGui.QTextCharFormat()
        boldChars.setFontWeight(QtGui.QFont.Bold)

        numEvents = 0
        numActions = 0
        events = result.keys()
        events.sort()
        for eventId in events:
            event = result[eventId]
            row = table.addRow()
            table.setText(row, 0, eventId)
            table.setText(row, 1, event['begDate'])
            table.setText(row, 2, event['endDate'])
            table.setText(row, 3, sum([event['actions'][actionId][2] for actionId in event['actions']]))
            table.setText(row, 4, event['SMO'])
            table.setText(row, 5, event['typeAndMES'])
            table.setText(row, 6, event['accountNumber'])
            table.setText(row, 7, event['accountDate'])
            table.setText(row, 9, event['person'])
            actions = event['actions']
#            actions.sort(cmp = lambda i1, i2: (-1 if i1[1][1] < i2[1][1] else (0 if i1[1][1] == i2[1][1] else 1)))
            for actionId in actions:
                row = table.addRow()
                for i in xrange(8):
                    table.setText(row, i+1, unicode(actions[actionId][i]))
                numActions += 1
            numEvents += 1
        cursor.setCharFormat(CReportBase.TableTotal)
        row = table.addRow()
        table.mergeCells(row, 0, 1, 9)
        table.setText(row, 0, u'Итого случаев лечения: %d, услуг: %d'%(numEvents, numActions))
        return result


    def getReportData(self, query, params):
        result = {}
        while query.next():
            record = query.record()

            eventId = forceRef(record.value('eventId'))
            eventBegDate = forceDate(record.value('eventBegDate'))
            eventEndDate = forceDate(record.value('eventEndDate'))
            clientSMO = forceString(record.value('clientSMO'))
            eventTypeAndMES = forceString(record.value('eventTypeAndMES'))
            eventAccountNumber = forceString(record.value('eventAccountNumber'))
            eventAccountDate = forceDate(record.value('eventAccountDate'))
            eventPerson = forceString(record.value('eventPerson'))
            actionId = forceRef(record.value('actionId'))
            actionBegDate = forceDate(record.value('actionBegDate'))
            actionEndDate = forceDate(record.value('actionEndDate'))
            actionAmount = forceDouble(record.value('actionAmount'))
            actionPrice = forceDouble(record.value('actionPrice'))
            actionSum = forceDouble(record.value('actionSum'))
            serviceCode = forceString(record.value('serviceCode'))
            serviceName = forceString(record.value('serviceName'))
            actionDiagnosis = forceString(record.value('actionDiagnosis'))
            actionPerson = forceString(record.value('actionPerson'))

            result.setdefault(eventId, dict())
            result[eventId]['begDate'] = eventBegDate.toString("dd.MM.yyyy")
            result[eventId]['endDate'] = eventEndDate.toString("dd.MM.yyyy")
            result[eventId]['SMO'] = clientSMO
            result[eventId]['typeAndMES'] = eventTypeAndMES
            result[eventId]['accountNumber'] = eventAccountNumber
            result[eventId]['accountDate'] = eventAccountDate.toString("dd.MM.yyyy")
            result[eventId]['person'] = eventPerson
            result[eventId].setdefault('actions', dict())
            result[eventId]['actions'].setdefault(actionId, [0, ]*9)
            result[eventId]['actions'][actionId][0] = actionBegDate.toString("dd.MM.yyyy")
            result[eventId]['actions'][actionId][1] = actionEndDate.toString("dd.MM.yyyy")
            result[eventId]['actions'][actionId][2] = actionAmount
            result[eventId]['actions'][actionId][3] = actionPrice
            result[eventId]['actions'][actionId][4] = actionSum
            result[eventId]['actions'][actionId][5] = serviceCode
            result[eventId]['actions'][actionId][6] = actionDiagnosis
            result[eventId]['actions'][actionId][7] = serviceName
            result[eventId]['actions'][actionId][8] = actionPerson
        return result


class CReportClientServicesSetup(QtGui.QDialog, Ui_ReportPayersSetupDialog):
    def __init__(self, parent, report):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self._report = report


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.cmbContract.setValue(params.get('contractId', None))
        self.chkDetailContracts.setChecked(params.get('printContract', False))
        self.chkPrintPayerResult.setChecked(params.get('printAccount', False))
        self.cmbClientOrganisation.setValue(params.get('clientOrganisationId', None))
        self.cmbInsurer.setValue(params.get('insurerId'))
        self.chkFreeInputWork.setChecked(params.get('freeInputWork', False))
        self.edtFreeInputWork.setText(params.get('freeInputWorkValue', ''))


    def params(self):
        params = {}
        params['contractId'] = self.cmbContract.value()
        params['contractText'] = forceString(self.cmbContract.currentText())
        params['begDate'] = self.edtBegDate.date()
        params['endDate'] = self.edtEndDate.date()
        params['printContract']  = self.chkDetailContracts.isChecked()
        params['printAccount'] = self.chkPrintPayerResult.isChecked()
        params['clientOrganisationId'] = self.cmbClientOrganisation.value()
        params['insurerId'] = self.cmbInsurer.value()
        params['freeInputWork'] = self.chkFreeInputWork.isChecked()
        params['freeInputWorkValue'] = forceStringEx(self.edtFreeInputWork.text())
        return params
