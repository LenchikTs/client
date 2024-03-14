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
from PyQt4.QtCore import pyqtSignature, QDate

from library.Utils      import forceString, formatName
from Events.Utils       import getActionTypeDescendants
from Reports.ReportBase import CReportBase, createTable
from Reports.Report     import CReport
from Reports.Utils      import getStringPropertyValue
from Ui_ReportSurgeryPlanDay import Ui_ReportSurgeryPlanDay


def selectData(params):
    begDate  = params.get('begDate', None)
    actionTypeClass = params.get('actionTypeClass', None)
    actionTypeId = params.get('actionTypeId', None)
    stmt=u"""
SELECT Client.lastName, Client.firstName, Client.patrName,
       Client.birthDate, Client.sex, Client.id AS clientId,
       rbJobType.name AS jobTypeName,
       Job_Ticket.datetime,
       %s AS diagnos,
       %s AS plan,
       vrbPersonWithSpeciality.name AS personName,
       OrgStructure.name AS orgStrName
FROM
    Action
    INNER JOIN ActionType on ActionType.id=Action.actionType_id
    INNER JOIN ActionProperty on ActionProperty.action_id = Action.id
    INNER JOIN ActionProperty_Job_Ticket ON ActionProperty_Job_Ticket.id = ActionProperty.id
    INNER JOIN Job_Ticket ON Job_Ticket.id = ActionProperty_Job_Ticket.value
    INNER JOIN Job ON Job.id = Job_Ticket.master_id
    INNER JOIN rbJobType ON rbJobType.id = Job.jobType_id
    INNER JOIN Event ON Action.event_id = Event.id
    INNER JOIN Client ON Client.id = Event.client_id
    LEFT JOIN vrbPersonWithSpeciality ON vrbPersonWithSpeciality.id = Action.person_id
    LEFT JOIN OrgStructure ON vrbPersonWithSpeciality.orgStructure_id = OrgStructure.id
WHERE
    %s
ORDER BY jobTypeName, datetime
"""
    db = QtGui.qApp.db
    tableEvent      = db.table('Event')
    tableClient     = db.table('Client')
    tableAction     = db.table('Action')
    tableActionType = db.table('ActionType')
    tableAP         = db.table('ActionProperty')
    tableAPJT       = db.table('ActionProperty_Job_Ticket')
    tableJT         = db.table('Job_Ticket')
    tableJ          = db.table('Job')
    cond = [tableAction['deleted'].eq(0),
            tableJT['deleted'].eq(0),
            tableJ['deleted'].eq(0),
            tableAP['deleted'].eq(0),
            tableActionType['deleted'].eq(0),
            tableEvent['deleted'].eq(0),
            tableClient['deleted'].eq(0),
            tableAPJT['value'].isNotNull()
            ]
    if begDate:
        cond.append(tableJT['datetime'].dateEq(begDate))
    if actionTypeId:
        cond.append(tableActionType['id'].inlist(getActionTypeDescendants(actionTypeId, actionTypeClass)))
    elif actionTypeClass is not None:
        cond.append(tableActionType['class'].eq(actionTypeClass))
    return db.query(stmt % (getStringPropertyValue(u'Диагноз при направлении'), getStringPropertyValue(u'Планируется'), db.joinAnd(cond)))


class CReportSurgeryPlanDay(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setPayPeriodVisible(False)
        self.setTitle(u'План операционного дня')


    def getSetupDialog(self, parent):
        result = CReportSurgeryPlanDaySetup(parent)
        result.setTitle(self.title())
        return result


    def build(self, params):
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        tableColumns = [
                        ('20%', [u'Операционная'], CReportBase.AlignLeft),
                        ('10%', [u'Дата операции'],CReportBase.AlignLeft),
                        ('20%', [u'ФИО пациентов'],CReportBase.AlignLeft),
                        ('20%', [u'Диагноз'],      CReportBase.AlignLeft),
                        ('10%', [u'Планируется'],  CReportBase.AlignLeft),
                        ('10%', [u'Кто записал' ], CReportBase.AlignLeft),
                        ('10%', [u'Подразделение направителя' ], CReportBase.AlignLeft)
                        ]
        table = createTable(cursor, tableColumns)
        query = selectData(params)
        while query.next():
            record = query.record()
            lastName = forceString(record.value('lastName'))
            firstName = forceString(record.value('firstName'))
            patrName = forceString(record.value('patrName'))
            #birthDate = forceString(record.value('birthDate'))
            #sex = forceString(record.value('sex'))
            clientId = forceString(record.value('clientId'))
            clientName = formatName(lastName, firstName, patrName) + u', ' + clientId
            jobTypeName = forceString(record.value('jobTypeName'))
            datetime = forceString(record.value('datetime'))
            diagnos = forceString(record.value('diagnos'))
            plan = forceString(record.value('plan'))
            personName = forceString(record.value('personName'))
            orgStrName = forceString(record.value('orgStrName'))
            i = table.addRow()
            table.setText(i, 0, jobTypeName)
            table.setText(i, 1, datetime)
            table.setText(i, 2, clientName)
            table.setText(i, 3, diagnos)
            table.setText(i, 4, plan)
            table.setText(i, 5, personName)
            table.setText(i, 6, orgStrName)
        return doc


class CReportSurgeryPlanDaySetup(QtGui.QDialog, Ui_ReportSurgeryPlanDay):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)


    def setTitle(self, title):
        self.setWindowTitle(title)


    def setParams(self, params):
        self.edtDate.setDate(QDate.currentDate()) # в соответствии с задачей №8817
        classCode = params.get('actionTypeClass', 0)
        self.cmbActionTypeClass.setCurrentIndex(classCode)
        self.cmbActionType.setClassesPopup([classCode])
        self.cmbActionType.setClass(classCode)
        self.cmbActionType.setValue(params.get('actionTypeId', None))


    def params(self):
        result = {}
        result['begDate']  = self.edtDate.date()
        result['actionTypeClass']  = self.cmbActionTypeClass.currentIndex()
        result['actionTypeId']  = self.cmbActionType.value()
        return result


    @pyqtSignature('int')
    def on_cmbActionTypeClass_currentIndexChanged(self, classCode):
        self.cmbActionType.setClassesPopup([classCode])
        self.cmbActionType.setClass(classCode)

