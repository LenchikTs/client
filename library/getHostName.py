# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2021 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################
##
## getHostName: отдаётся в загадочной кодировке, а нам нужно в юникоде
##
#############################################################################

import os
import socket

from library.Utils import anyToUnicode


def getHostName():
    if os.name == 'nt':
        remoteClientName = os.getenv('CLIENTNAME')
        if remoteClientName:
            return anyToUnicode(remoteClientName)

    return anyToUnicode(socket.gethostname())
