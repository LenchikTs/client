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

from PyQt4 import QtGui
from PyQt4.QtCore import QVariant

from library.crbcombobox import CRBComboBox
from Events.EventTypeComboBoxExPopup import CEventTypeComboBoxExPopup


class CEventTypeComboBoxEx(CRBComboBox):
    __pyqtSignals__ = ('textChanged(QString)',
                       'textEdited(QString)'
                      )


    def __init__(self, parent):
        CRBComboBox.__init__(self, parent)
        self._tableName = 'EventType'
        self._addNone = True
        self._popup=None
        self.eventTypeIdList =  []
        self.setOrderByName()
        CRBComboBox.setTable(self, self._tableName, self._addNone, '', self._order)


    def setAddNone(self, addNone=True):
        if self._addNone != addNone:
            self._addNone = addNone
            self.updateFilter()


    def setOrderByCode(self):
        self._order = 'code, name'


    def setOrderByName(self):
        self._order = 'name, code'


    def addNotSetValue(self):
        record = self.getActualEmptyRecord()
        record.setValue('code', QVariant(u'----'))
        record.setValue('name', QVariant(u'Значение не задано'))
        self.setSpecialValues(((-1, record), ))


    def _createPopup(self):
        if not self._popup:
            self._popup = CEventTypeComboBoxExPopup(self)


    def showPopup(self):
        self._createPopup()
        pos = self.rect().bottomLeft()
        pos = self.mapToGlobal(pos)
        size = self._popup.sizeHint()
        screen = QtGui.QApplication.desktop().availableGeometry(pos)
        size.setWidth(screen.width())
        pos.setX( max(min(pos.x(), screen.right()-size.width()), screen.left()) )
        pos.setY( max(min(pos.y(), screen.bottom()-size.height()), screen.top()) )
        self._popup.move(pos)
        self._popup.resize(size)
        self._popup.show()


    def setValue(self, eventTypeIdList):
        self.eventTypeIdList = eventTypeIdList
        rowIndex = self._model.searchId(self.eventTypeIdList[0] if self.eventTypeIdList else None)
        self.setCurrentIndex(rowIndex)
#        if self.eventTypeIdList:
#            self.setCurrentText(','.join(str(eventTypeId) for eventTypeId in self.eventTypeIdList if eventTypeId))
#        else:
#            self.setCurrentText( )


    def value(self):
        self.eventTypeIdList = self. _popup.eventTypeIdList
        return self.eventTypeIdList
