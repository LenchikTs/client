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


from library.TableView    import CTableView


class CSortFilterProxyTableView(CTableView):
    def __init__(self, parent):
        CTableView.__init__(self, parent)


    def model(self):
        return  CTableView.model(self).sourceModel()
