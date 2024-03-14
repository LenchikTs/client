# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2022 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from library.TableView    import CTableView
from library.InDocTable   import CInDocTableView


class CSurveillanceClientsTableView(CTableView):
    def __init__(self, parent):
        CTableView.__init__(self, parent)


class CSurveillanceClientDiagnosisTableView(CTableView):
    def __init__(self, parent):
        CTableView.__init__(self, parent)


class CSurveillanceMonitoringTableView(CTableView):
    def __init__(self, parent):
        CTableView.__init__(self, parent)


class CSurveillancePlanningTableView(CInDocTableView):
    def __init__(self, parent):
        CInDocTableView.__init__(self, parent)
