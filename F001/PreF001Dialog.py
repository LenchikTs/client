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
F001 planer
"""


from F025.PreF025Dialog import CPreF025Dialog, CPreF025DagnosticAndActionPresets

CPreF001DagnosticAndActionPresets = CPreF025DagnosticAndActionPresets


class CPreF001Dialog(CPreF025Dialog):
    def __init__(self, parent, contractTariffCache=None):
        CPreF025Dialog.__init__(self, parent, contractTariffCache)
        self.setWindowTitleEx(u'Планирование осмотра Ф.001')