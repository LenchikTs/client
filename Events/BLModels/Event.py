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


from library.blmodel.Model import CDocumentModel
from library.blmodel.ModelAttribute import (
                                             CBooleanAttribute,
                                             CDateAttribute,
                                             CDateTimeAttribute,
                                             CIntAttribute,
                                             CRefAttribute,
                                             CStringAttribute,
                                             CDoubleAttribute,
                                           )


class CEvent(CDocumentModel):
    tableName = 'Event'

    externalId = CStringAttribute(length=30)
    eventType_id = CRefAttribute()
    org_id = CRefAttribute()
    client_id = CRefAttribute()
    relative_id = CRefAttribute()
    contract_id = CRefAttribute()
    prevEventDate = CDateTimeAttribute()
    setDate = CDateTimeAttribute()
    setPerson_id = CRefAttribute()
    execDate = CDateTimeAttribute()
    execPerson_id = CRefAttribute()
    isPrimary = CIntAttribute()
    order = CIntAttribute()
    result_id = CRefAttribute()
    nextEventDate = CDateTimeAttribute()
    payStatus = CIntAttribute()
    typeAsset_id = CRefAttribute()
    note = CStringAttribute()
    curator_id = CRefAttribute()
    assistant_id = CRefAttribute()
    MES_id = CRefAttribute()
    mesSpecification_id = CRefAttribute()
    pregnancyWeek = CIntAttribute()
    relegateOrg_id = CRefAttribute()
    relegatePerson_id = CRefAttribute()
    totalCost = CDoubleAttribute()
    patientModel_id = CRefAttribute()
    cureType_id = CRefAttribute()
    cureMethod_id = CRefAttribute()
    prevEvent_id = CRefAttribute()
    isClosed = CBooleanAttribute()
    expertiseDate = CDateAttribute()
    expert_id = CRefAttribute()
    srcDate = CDateAttribute()
    srcNumber = CStringAttribute(length=64)
