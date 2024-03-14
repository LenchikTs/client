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
from PyQt4.QtCore import pyqtSignature

from library.crbcombobox      import CRBComboBox
from library.DialogBase       import CConstructHelperMixin
from library.TableModel       import CTableModel, CDateCol, CEnumCol, CRefBookCol, CTextCol

from Events.CreateEvent       import editEvent
from Events.Utils             import orderTexts
from Registry.RegistryTable   import codeIsPrimary

from Quoting.Ui_EventsListDialog import Ui_EventsListDialog


class CEventsList(QtGui.QDialog, CConstructHelperMixin, Ui_EventsListDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.addModels('Events', CEventsTableModel(self))
        self.setModels(self.tblEvents, self.modelEvents, self.selectionModelEvents)


    def setClientId(self, clientId):
        db = QtGui.qApp.db
        cond = [u'Event.`deleted`=0',
                u'Event.`client_id` IN (%d)'%clientId,
                u"Event.`eventType_id` IN (SELECT id FROM EventType WHERE(EventType.purpose_id NOT IN (SELECT rbEventTypePurpose.id from rbEventTypePurpose where rbEventTypePurpose.code = '0')))"]
        table = db.table('Event')
        idList = db.getIdList(table,
                           'id',
                           cond,
                           ['setDate DESC', 'id'])
        self.tblEvents.setIdList(idList, None)


    @pyqtSignature('QModelIndex')
    def on_tblEvents_doubleClicked(self, index):
        eventId = self.tblEvents.currentItemId()
        editEvent(self, eventId)


class CEventsTableModel(CTableModel):
    def __init__(self, parent):
        CTableModel.__init__(self, parent)
        self.addColumn(CDateCol(u'Назначен', ['setDate'],  10))
        self.addColumn(CDateCol(u'Выполнен', ['execDate'], 10))
        self.addColumn(CRefBookCol(u'Тип',  ['eventType_id'], 'EventType', 15))
        self.addColumn(CRefBookCol(u'МЭС',  ['MES_id'], 'mes.MES', 15, CRBComboBox.showCode))
        self.addColumn(CRefBookCol(u'Врач', ['execPerson_id'], 'vrbPersonWithSpeciality', 15))
        self.addColumn(CEnumCol(u'Первичный', ['isPrimary'], codeIsPrimary, 8))
        self.addColumn(CEnumCol(u'Порядок', ['order'], orderTexts, 8))
        self.addColumn(CRefBookCol(u'Результат', ['result_id'], 'rbResult', 40))
        self.addColumn(CTextCol(u'Номер документа', ['externalId'], 30))
        self.setTable('Event')
        self.diagnosisIdList = None
