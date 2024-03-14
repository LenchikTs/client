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

from List import CRBServiceList, CServiceFilterDialog

def selectService(parent, cmd):
    serviceId = cmd.value()
    filterDialog = CServiceFilterDialog(parent)
    filterDialog.setProps({})
    try:
        if filterDialog.exec_():
            dialog = CRBServiceList(parent, True)
            try:
                dialog.props = filterDialog.props()
                dialog.renewListAndSetTo(serviceId)
                if dialog.model.rowCount() == 1:
                    return dialog.currentItemId()
                else:
                    if dialog.exec_():
                        return dialog.currentItemId()
            finally:
                dialog.deleteLater()
    finally:
        filterDialog.deleteLater()
    return None

