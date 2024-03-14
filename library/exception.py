# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

import locale


class CException(Exception):

    def __init__(self, message):
        m = unicode(message)
        Exception.__init__(self, m.encode(locale.getpreferredencoding()))
        self._message = m

    def __unicode__(self):
        return self._message
