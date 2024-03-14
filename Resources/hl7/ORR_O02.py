# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2015 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from bases import *
from segments import *


class ORR_O02_PATIENT(THl7Compound):
    _items = [ ('PID', 'PID', [PID]),
               ('NTE', 'NTE', NTE),
             ]


class ORR_O02_CHOICE(THl7Compound):
    _items = [ ('OBR', 'OBR', OBR),
               ('RQD', 'RQD', RQD),
               ('RQ1', 'RQ1', RQ1),
               ('RXO', 'RXO', RXO),
               ('ODT', 'ODT', ODT),
             ]
             
             
class ORR_O02_ORDER(THl7Compound):
    _items = [ ('ORC', 'ORC', ORC),
               ('ORR_O02_CHOICE',   'ORR_O02.CHOICE',   [ORR_O02_CHOICE]),
               ('NTE', 'NTE',   [NTE]),
               ('CTI', 'CTI',   [CTI]),
             ]

             
class ORR_O02_RESPONSE(THl7Compound):
    _items = [ ('ORR_O02_PATIENT', 'ORR_O02.PATIENT', ORR_O02_PATIENT),
               ('ORR_O02_ORDER',   'ORR_O02.ORDER',   [ORR_O02_ORDER]),
             ]

             
class ORR_O02(THl7Message):
    _items = [ ('MSH', 'MSH', MSH),
               ('MSA', 'MSA', MSA),
               ('ERR', 'ERR', ERR),
               ('NTE', 'NTE', NTE),
               ('ORR_O02_RESPONSE', 'ORR_O02.RESPONSE', ORR_O02_RESPONSE),
             ]
    _name = 'ORR_O02'

    
ORR_O02.register()
