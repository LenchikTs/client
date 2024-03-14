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

#from PyQt4 import QtGui
#from PyQt4.QtCore import *

from library.Utils import *
from library.DialogBase import CDialogBase

from Ui_TemplateDialog import Ui_ResourceTemplateDialog


class CTemplateDialog(CDialogBase, Ui_ResourceTemplateDialog):
    def __init__(self, parent):
        CDialogBase.__init__(self, parent)
        self.setupUi(self)
#        today = QDate.currentDate()
#        self.edtBegDate.setDateRange(today.addMonths(-1), today.addMonths(13))
#        self.edtEndDate.setDateRange(today.addMonths(-1), today.addMonths(13))
        self.edtBegDate.setFocus(Qt.OtherFocusReason)


    def setDateRange(self, begDate, endDate):
        self.edtBegDate.setDateRange(begDate, endDate)
        self.edtEndDate.setDateRange(begDate, endDate)
        self.edtBegDate.setDate(begDate)
        self.edtEndDate.setDate(endDate)


    def setDefaults(self, begTime, endTime, quantity):
            for widget in (self.edtTimeRange1, self.edtTimeRange2, self.edtTimeRange3,
                           self.edtTimeRange4, self.edtTimeRange5, self.edtTimeRange6, self.edtTimeRange7):
                widget.setTimeRange((begTime, endTime))
            for widget in (self.edtQuantity1, self.edtQuantity2, self.edtQuantity3,
                           self.edtQuantity4, self.edtQuantity5, self.edtQuantity6, self.edtQuantity7):
                widget.setValue(quantity)


    def getWorkPlan(self):
        dayPlans = [ self.getDayPlan(self.edtTimeRange1, self.edtQuantity1)
                    ]
        if self.rbDual.isChecked() or self.rbWeek.isChecked():
            dayPlans.append( self.getDayPlan(self.edtTimeRange2, self.edtQuantity2) )
        if self.rbWeek.isChecked():
            dayPlans.append( self.getDayPlan(self.edtTimeRange3, self.edtQuantity3) )
            dayPlans.append( self.getDayPlan(self.edtTimeRange4, self.edtQuantity4) )
            dayPlans.append( self.getDayPlan(self.edtTimeRange5, self.edtQuantity5) )
            dayPlans.append( self.getDayPlan(self.edtTimeRange6, self.edtQuantity6) )
            dayPlans.append( self.getDayPlan(self.edtTimeRange7, self.edtQuantity7) )
        return (dayPlans, self.chkFillRedDays.isChecked())


    def getDayPlan(self, edtTimeRange, edtQuantity):
        return ( edtTimeRange.timeRange(),
                 edtQuantity.value()
               )


    def getDateRange(self):
        return (self.edtBegDate.date(), self.edtEndDate.date())
