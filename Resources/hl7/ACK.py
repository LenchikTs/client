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


class ACK(THl7Message):
    _items = [ ('MSH', 'MSH', MSH),
               ('SFT', 'SFT', [SFT]),
               ('MSA', 'MSA', MSA), 
               ('ERR', 'ERR', [ERR]), 
             ]
    _name = 'ACK'

#    def __init__(self):
#        THl7Message.__init__(self)

ACK.register()