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
## 'R' запись протокола ASTM E-1394
##
#############################################################################


from Record import CRecord

class CCommentRecord(CRecord):
    structure = {
                    'recordType'            : ( 0,       str),
                    'seqNo'                 : ( 1,       int),
                    'source'                : ( 2,       unicode), # comment source:
                                                                   #   P practice
                                                                   #   L information system
                                                                   #   I clinical instrument system
                    'textEx'                : ( 3,       unicode), # текст целиком
                    'code'                  : ( (3,0,0), unicode), # PC = Patient Comment, RC = Request Comment, SC = Sample Comment, TC = Test Comment
                    'text'                  : ( (3,0,1), unicode), # up to 255 chars?
                    'type'                  : ( 4,       unicode), # comment type:
                                                                   #   G generic/free result comment
                                                                   #   T result name comment
                                                                   #   P positive result comment
                                                                   #   N negative result comment
                                                                   #   I instrument flag(s) comment

                }
    recordType = 'C'


if __name__ == '__main__':
    r = CCommentRecord()
    s = r'C|1|L|SC^fully assured|G'
    r.setString(s, '|\\^&')
    print r._storage
    s1 = r.asString('|\\^&')
    print s1==s
    print s
    print s1
