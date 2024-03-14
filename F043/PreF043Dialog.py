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
F043 planer
"""


from F025.PreF025Dialog import CPreF025Dialog, CPreF025DagnosticAndActionPresets

CPreF043DagnosticAndActionPresets = CPreF025DagnosticAndActionPresets


class CPreF043Dialog(CPreF025Dialog):
    def __init__(self, parent, contractTariffCache):
        CPreF025Dialog.__init__(self, parent, contractTariffCache)
        self.setWindowTitleEx(u'Планирование осмотра Ф.043')