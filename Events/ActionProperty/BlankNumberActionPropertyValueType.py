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
from PyQt4.QtCore import QVariant

from library.Utils       import forceDate, forceRef, forceString
from Blank.BlankComboBox import CBlankNumberComboBoxActions

from ActionPropertyValueType  import CActionPropertyValueType


class CBlankNumberActionPropertyValueType(CActionPropertyValueType):
    name         = 'BlankNumber'
    variantType  = QVariant.String
    isCopyable   = False

    class CPropEditor(CBlankNumberComboBoxActions):
        def __init__(self, action, domain, parent, clientId, eventTypeId):
            blankIdList = self.getBlankIdList(action)
            CBlankNumberComboBoxActions.__init__(self, parent, blankIdList, True)


        def getBlankIdList(self, action):
            blankIdList = []
            docTypeId = action._actionType.id
            if docTypeId:
                db = QtGui.qApp.db
                tableEvent = db.table('Event')
                tableRBBlankActions = db.table('rbBlankActions')
                tableBlankActionsParty = db.table('BlankActions_Party')
                tableBlankActionsMoving = db.table('BlankActions_Moving')
#                tablePerson = db.table('Person')
                eventId = forceRef(action._record.value('event_id'))
                personId = None
                orgStructureId = None
                if eventId:
                    record = db.getRecordEx(tableEvent, [tableEvent['execPerson_id'], tableEvent['setDate']], [tableEvent['deleted'].eq(0), tableEvent['id'].eq(eventId)])
                    if record:
                        personId = forceRef(record.value('execPerson_id')) if record else None
                        setDate = forceDate(record.value('setDate')) if record else None
                else:
                    personId = forceRef(action._record.value('person_id'))
                if not personId:
                    personId = forceRef(action._record.value('setPerson_id'))
                if not personId:
                    personId = QtGui.qApp.userId
                if personId:
                    orgStructureId = self.getOrgStructureId(personId)
                if not orgStructureId:
                   orgStructureId = QtGui.qApp.currentOrgStructureId()

                date = forceDate(action._record.value('begDate'))
                if not date and setDate:
                    date = setDate
                cond = [tableRBBlankActions['doctype_id'].eq(docTypeId),
                        tableBlankActionsParty['deleted'].eq(0),
                        tableBlankActionsMoving['deleted'].eq(0)
                        ]
                if date:
                    cond.append(tableBlankActionsMoving['date'].le(date))
                if personId and orgStructureId:
                    cond.append(db.joinOr([tableBlankActionsMoving['person_id'].eq(personId), tableBlankActionsMoving['orgStructure_id'].eq(orgStructureId)]))
                elif personId:
                    cond.append(tableBlankActionsMoving['person_id'].eq(personId))
                elif orgStructureId:
                    cond.append(tableBlankActionsMoving['orgStructure_id'].eq(orgStructureId))
                queryTable = tableRBBlankActions.innerJoin(tableBlankActionsParty, tableBlankActionsParty['doctype_id'].eq(tableRBBlankActions['id']))
                queryTable = queryTable.innerJoin(tableBlankActionsMoving, tableBlankActionsMoving['blankParty_id'].eq(tableBlankActionsParty['id']))
                blankIdList = db.getIdList(queryTable, u'BlankActions_Moving.id', cond, u'rbBlankActions.checkingSerial, rbBlankActions.checkingNumber, rbBlankActions.checkingAmount DESC')
            return blankIdList


        def setValue(self, value):
            CBlankNumberComboBoxActions.setValue(self, forceString(value) if forceString(value) else forceString(CBlankNumberComboBoxActions.text(self)))


        def getOrgStructureId(self, personId):
            orgStructureId = None
            if personId:
                db = QtGui.qApp.db
                tablePerson = db.table('Person')
                recOrgStructure = db.getRecordEx(tablePerson, [tablePerson['orgStructure_id']], [tablePerson['deleted'].eq(0), tablePerson['id'].eq(personId)])
                orgStructureId = forceRef(recOrgStructure.value('orgStructure_id')) if recOrgStructure else None
            return orgStructureId


    @staticmethod
    def convertDBValueToPyValue(value):
        return forceString(value)

    convertQVariantToPyValue = convertDBValueToPyValue


    def toText(self, v):
        return forceString(v)


