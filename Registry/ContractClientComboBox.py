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

from PyQt4 import QtCore
from PyQt4.QtCore import SIGNAL

from library.DbComboBox import CAbstractDbComboBox
from Orgs.OrgComboBox import CContractDbModel, CContractDbData


class CContractClientDbModel(CContractDbModel):

    def __init__(self, parent):
        CContractDbModel.__init__(self, parent)


    def initDbData(self):
        self.dbdata = CContractDbData()
        if self.orgId:
            self.dbdata.select(self)


class CContractClientComboBox(CAbstractDbComboBox):
    __pyqtSignals__ = ('valueChanged()',
                      )

    def __init__(self, parent):
        CAbstractDbComboBox.__init__(self, parent)
        self.__model = CContractClientDbModel(self)
        self.__prevValue = None
        self.setModel(self.__model)
        self.connect(self, QtCore.SIGNAL('currentIndexChanged(int)'), self.onCurrentIndexChanged)


    def showPopup(self):
        CAbstractDbComboBox.showPopup(self)
        view = self.view()
        viewFrame = view.parent()
        size = view.sizeHint()
        size.setWidth(size.width()*2)
        viewFrame.resize(size)



    def getWeakValue(self):
        if self.__model.dbdata:
            return self.value()
        else:
            return None


    def setCurrentIfOnlyOne(self):
        n = self.__model.rowCount()
        if n == 1:
            self.setCurrentIndex(0)
        elif n > 1 and self.__model.onlyOneWithSameFinance(0):
            self.setCurrentIndex(0)
        else:
            self.setCurrentIndex(-1)


    def setOrgId(self, orgId):
        self.__model.setOrgId(orgId)
#        self.setCurrentIfOnlyOne()


    def setClientInfo(self, clientId, sex, age, orgId, policyInfoList):
        self.__model.setClientInfo(clientId, sex, age, orgId, policyInfoList)


    def setFinanceId(self, financeId):
        self.__model.setFinanceId(financeId)


    def setEventTypeId(self, eventTypeId):
        self.__model.setEventTypeId(eventTypeId)


    def setActionTypeId(self, actionTypeId):
        self.__model.setActionTypeId(actionTypeId)


    def setBegDate(self, begDate):
        self.__model.setBegDate(begDate)
        self.setCurrentIfOnlyOne()
        self.conditionalEmitValueChanged()


    def setEndDate(self, endDate):
        self.__model.setEndDate(endDate)
        self.setCurrentIfOnlyOne()
        self.conditionalEmitValueChanged()


    def setDate(self, date):
        self.__model.setBegDate(date)
        self.__model.setEndDate(date)
        if self.__prevValue is not None:
            self.setValue(self.__prevValue)
        if self.getWeakValue() is None:
            self.setCurrentIfOnlyOne()



    def setCurrentIndex(self, index):
        CAbstractDbComboBox.setCurrentIndex(self, index)
        self.conditionalEmitValueChanged()


    def onCurrentIndexChanged(self, index):
        self.conditionalEmitValueChanged()


    def setValue(self, value):
        CAbstractDbComboBox.setValue(self, value)
        self.conditionalEmitValueChanged()


    def conditionalEmitValueChanged(self):
        value = self.getWeakValue()
        if self.__prevValue != value:
            self.__prevValue = value
            self.emit(SIGNAL('valueChanged()'))


    def getContractIdByFinance(self, financeCode):
        return self.__model.getContractIdByFinance(financeCode)

