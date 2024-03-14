# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2020-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4               import QtGui
from PyQt4.QtCore        import QDate

from library.Utils import forceString


def selectExpiredTempInvalidDocumentIds(filter):
    db = QtGui.qApp.db
    fssSystemId    = QtGui.qApp.getFssSystemId()
    orgId          = QtGui.qApp.getCurrentOrgId()
    orgStructureId = filter.get('orgStructureId', None)
    personId       = filter.get('personId', None)
    days           = filter.get('days', 0)
    fullName       = filter.get('fullName', None)
#    number         = filter.get('number', None)
#    begDate        = filter.get('begDate', None)
#    endDate        = filter.get('endDate', None)
    tempInvalidDocTypeId = QtGui.qApp.getTempInvalidDocTypeId()

    tableTempInvalidDocument          = db.table('TempInvalidDocument')
    tableTempInvalid                  = db.table('TempInvalid')
    tablePerson                       = db.table('Person')
    tableTempInvalidDocumentExport    = db.table('TempInvalidDocument_Export')

    table = tableTempInvalidDocument
    table = table.innerJoin( tableTempInvalid,
                             tableTempInvalid['id'].eq(tableTempInvalidDocument['master_id'])
                           )
    table = table.innerJoin(tablePerson,
                            tablePerson['id'].eq(tableTempInvalid['person_id'])
                           )
    table = table.leftJoin(tableTempInvalidDocumentExport,
                            [ tableTempInvalidDocumentExport['master_id'].eq(tableTempInvalidDocument['id']),
                              tableTempInvalidDocumentExport['masterDatetime'].eq(tableTempInvalidDocument['modifyDatetime']),
                              tableTempInvalidDocumentExport['system_id'].eq(fssSystemId)
                            ]
                          )
    cond = [ tableTempInvalidDocument['deleted'].eq(0),
             tableTempInvalidDocument['electronic'].eq(1),
             tableTempInvalidDocument['annulmentReason_id'].isNull(),
             tableTempInvalid['deleted'].eq(0),
             tableTempInvalid['doctype_id'].eq(tempInvalidDocTypeId),

             tableTempInvalid['endDate'].le(QDate.currentDate().addDays(-days)),
             tableTempInvalid['state'].eq(0),
             tableTempInvalidDocument['fssStatus'].notInlist(['M', 'R'])
           ]
    if personId:
        cond.append(tablePerson['id'].eq(personId))
    elif orgStructureId:
        orgStructureIdList = db.getDescendants('OrgStructure', 'parent_id', orgStructureId)
        cond.append(tablePerson['orgStructure_id'].inlist(orgStructureIdList))
    else:
        cond.append(tablePerson['org_id'].eq(orgId))
    if fullName:
      fullName = '%'+forceString(fullName)+'%'
      tableClient = db.table('Client')
      table = table.leftJoin(tableClient, tableTempInvalid['client_id'].eq(tableClient['id']))
      cond.append(u'CONCAT(Client.lastName,\' \', Client.firstName, \' \', Client.patrName) like \'{}\''.format(unicode(fullName)))

    idList = db.getIdList(table,
                          idCol=tableTempInvalidDocument['id'].name(),
                          where=cond,
                          order='TempInvalidDocument.id'
                         )
    return idList


