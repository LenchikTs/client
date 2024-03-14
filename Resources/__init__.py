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

"""
resource planner classes library
"""
from PyQt4 import QtGui
from library.Utils import formatRecordAsDict, dict2json


def formatJobTicketRecordAsDict(jobTicketId):
    return formatRecordAsDict('Job_Ticket', jobTicketId, fieldNameList=['id', 
                                                                         'datetime', 
                                                                         'resTimestamp', 
                                                                         'resConnectionId', 
                                                                         'status', 
                                                                         'begDateTime', 
                                                                         'endDateTime', 
                                                                         'isExceedQuantity'])


def writeJobTicketAppLog(kw, jobTicketId):
    if jobTicketId and QtGui.qApp.isGlobalAppLog():
        kw.update({'recordInfo': formatJobTicketRecordAsDict(jobTicketId)})
        QtGui.qApp.writeAppLog(dict2json(kw), mark='jobTicket')
