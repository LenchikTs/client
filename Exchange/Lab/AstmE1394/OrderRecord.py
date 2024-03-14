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
## 'O' запись протокола ASTM E-1394
##
#############################################################################


from PyQt4.QtCore import QDateTime


from Record import CRecord

class COrderRecord(CRecord):
    structure = {
                    'recordType'              : ( 0,       str),
                    'seqNo'                   : ( 1,       int),
                    'specimenId'              : ( (2,0,0), unicode), # sample id
                    'specimenIndex'              : ( (2,0,1), unicode), # sample id
                    'specimenCount'              : ( (2,0,2), unicode), # place in tripod in ABX Pentra ML
                    'instrumentSpecimenId'    : ( (3,0,0), unicode),
                    'instrumentSpecimenIndex' : ( (3,0,1), unicode),
                    'instrumentSpecimenCount' : ( (3,0,2), unicode),
                    'testId'                  : ( (4,0,0), unicode), # as vector
                    'assayName'               : ( (4,0,1), unicode),
                    'assayCode'               : ( (4,0,3), unicode),
                    'dilutionFactor '         : ( (4,0,4), unicode),
                    'priority'                : ( 5,       unicode), # S=Stat, R=Routine
                    'requestDateTime'         : ( 6,       QDateTime),
                    'specimenCollectionDateTime' : ( 7,       QDateTime),
                    'actionCode'              : (11,       str),  # (C)ancel – Used to cancel a previously downloaded test order.
                                                                # (A)dd – Used to add a test to a known specimen.
                                                                # (N)ew – Used to identify New Test Order for an unknown specimen. If the specimen is known, this message is ignored.
                                                                # (R)erun – Used to request a Rerun for a test.
                    'specimenDescr'           : (15,       unicode), # S (Serum), U (Urine) etc, etc
                    'userField1'              : (18,       unicode),
                    'userField2'              : (19,       unicode),
                    'laboratoryField1Finance'               : ((20,0,0), unicode),
                    'laboratoryField1EventTypeRegionalCode' : ((20,0,1), unicode),
                    'laboratoryField1ContractNumber'        : ((20,0,2), unicode),
                    'laboratoryField2'        : (21,       unicode),

                    'reportTypes'             : (25,       unicode), # (O)rder – Normal request from Host.
                                                                   # (F)inal - Final Result
                    'specimenInstitution'     : (30,       unicode), # Production Lab: when using multi-laboratory configuration
                                                                   # this field can indicate laboratory expected to process the sample
                }
    recordType = 'O'



if __name__ == '__main__':
    r = COrderRecord()
    s = r'O|1|12120001||^^^NA^Sodium\^^^Cl^Clorum|R|20011023105715|20011023105715||||N||||S|||CHIM|AXM|Lab1|12120||||O|||||LAB2'
    r.setString(s, '|\\^&')
    print r._storage
    for n in ('specimenId', 'instrumentSpecimenId', 'testId', 'assayCode', 'assayName',
              'requestDateTime', 'specimenCollectionDateTime', 'actionCode', 'specimenDescr',
              'userField1', 'userField2', 'laboratoryField1', 'laboratoryField2','reportTypes', 'specimenInstitution'):
        print n,'\t= ', getattr(r, n)
    s1 = r.asString('|\\^&')
    print s1==s
    print s
    print s1

    print '**********************'
    r1 = COrderRecord()

    now = QDateTime.currentDateTime()

    r1.specimenId      = 'label'
#    r1.instrumentSpecimenId = 'instrumentSpecimenId'
    r1.instrumentSpecimenIndex = 1
    r1.instrumentSpecimenCount = 6
    r1.assayCode       = 'testCode'
    r1.assayName       = 'testName'
    r1.requestDateTime =  now
    r1.specimenCollectionDateTime = now
    r1.priority        = 'R'
    r1.actionCode      = 'A'
    r1.specimenDescr   = 'specimenCode'
    r1.userField1      = 123
    r1.reportTypes     = 'O'

    print r1.asString('|\\^&')
    print r1._storage
