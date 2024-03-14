#! /usr/bin/env python
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
##
## 'P' запись протокола ASTM E-1394
##
#############################################################################


from PyQt4.QtCore import QDate


from Record import CRecord

class CPatientRecord(CRecord):
    structure = {
                    'recordType'             : ( 0,       str),
                    'seqNo'                  : ( 1,       int),
                    'patientId'              : ( 2,       unicode),
                    'laboratoryPatientId'    : ( 3,       unicode),
                    'reservedPatientId'      : ( 4,       unicode),
                    'lastName'               : ( (5,0,0), unicode),
                    'firstName'              : ( (5,0,1), unicode),
                    'patrName'               : ( (5,0,2), unicode),

                    'motherMaidenName'       : ( 6,       unicode),
                    'birthDate'              : ( 7,       QDate),
                    'sex'                    : ( 8,       str), # M/F
                    'race'                   : ( 9,       unicode),
                    'addressStreet'          : ((10,0,0), unicode),
                    'addressCity'            : ((10,0,1), unicode),
                    'addressState'           : ((10,0,2), unicode),
                    'addressPostalCode'      : ((10,0,3), unicode),
                    'addressCountryCode'     : ((10,0,4), unicode),
                    # !!! over the LIS2-A2 description
                    'documentType'           : ((10,0,5), unicode),
                    'documentSerial'         : ((10,0,6), unicode),
                    'documentNumber'         : ((10,0,7), unicode),
                    'policySerial'           : ((10,0,8), unicode),
                    'policyNumber'           : ((10,0,9), unicode),
                    #
                    'reserved'               : (11,       unicode),
                    'phone'                  : (12,       unicode),
                    'physician'              : (13,       unicode),
                    'age'                    : ((14,0,0), int),
                    'ageUnit'                : ((14,0,1), unicode), # days/months/years

                    'isExternal'             : (15,       int), # 1- external, 0 - internal
                    'height'                 : (16,       unicode),
                    'weight'                 : (17,       unicode),
                    'diagnosis'              : (18,       unicode),
                    'medication'             : (19,       unicode),
                    'diet'                   : (20,       unicode),
                    'practiceField1'         : (21,       unicode),
                    'practiceField2'         : (22,       unicode),
                    'admissionDate'          : (23,       unicode),
                    'admissionStatus'        : (24,       unicode),
                    'senderOrgStructureCode' : ((25,0,0), unicode),
                    'senderOrgStructureName' : ((25,0,1), unicode),
                    'senderPersonCode'       : ((25,0,2), unicode),
                    'senderPersonName'       : ((25,0,3), unicode),
                    'senderOrgStructureType' : ((25,0,4), unicode),
                    'senderOrgStructureExternalCode' : ((25,0,5), unicode),
                    'providerId'             : ((32,0,0), unicode),
                    'providerLastName'       : ((32,0,1), unicode),
                    'providerFirstName'      : ((32,0,2), unicode),
                    'providerPatrName'       : ((32,0,3), unicode),
                    'providerNameSuffix'     : ((32,0,4), unicode),
                    'providerTitle'          : ((32,0,5), unicode),
                    # !!! over the LIS2-A2 description
                    'eventTypeRegionalCode'  : ((32,0,6), unicode),
                    'eventTypeName'          : ((32,0,7), unicode),
                    'eventMesCode'           : ((32,0,8), unicode),
                    'eventExternalId'        : ((32,0,9), unicode),
                    #
                    'dosageCategory'         : (34,       unicode),
                }
    recordType = 'P'


if __name__ == '__main__':
    r = CPatientRecord()
    s = r'P|1|1212000|117118112||White^Nicky||19601218|M||||| Smith | 37^years^ssssss|0||||||||||CHIR'
    r.setString(s, '|\\^&')
    print r._storage
    s1 = r.asString('|\\^&')
    print s1==s
    print s
    print s1
