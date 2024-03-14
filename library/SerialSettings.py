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

import json
from   library.Utils import forceBool, forceInt, forceString


class CSerialSettings:
    def __init__(self, preset=None):
        self.port   = ''
        self.baudrate = '9600'
        self.parity = 'N'
        self.stopbits = 1
        self.xonxoff = False
        self.rtscts = True
        self.dsrdtr = False
        if isinstance(preset, dict):
            self.__setDict(preset)
        if isinstance(preset, basestring):
            self.setString(preset)


    def __nonzero__(self):
        return bool(self.port and self.baudrate and self.parity and self.stopbits in (1, 2))


    def __setDict(self, data):
        self.port = forceString(data.get('port', ''))
        self.baudrate = forceString(data.get('baudrate', '9600'))
        self.parity = forceString(data.get('parity', 'N'))
        self.stopbits = forceInt(data.get('stopbits', 1))
        self.xonxoff = forceBool(data.get('xonxoff', False))
        self.rtscts = forceBool(data.get('rtscts', True))
        self.dsrdtr = forceBool(data.get('dsrdtr', False))


    def asDict(self):
        return { 'port'     : self.port,
                 'baudrate' : self.baudrate,
                 'parity'   : self.parity,
                 'stopbits' : self.stopbits,
                 'xonxoff'  : self.xonxoff,
                 'rtscts'   : self.rtscts,
                 'dsrdtr'   : self.dsrdtr,
               }


    def setDict(self, data):
        if isinstance(data, dict):
            self.__setDict(data)


    def setString(self, data):
        if data:
            try:
                self.setDict(json.loads(data))
            except:
                pass


    def asString(self):
        return json.dumps(self.asDict())

