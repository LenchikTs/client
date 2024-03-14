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

from PyQt4 import QtGui
from library.Utils import forceRef, forceString, forceStringEx

from Ui_ClientRecordProperties import Ui_ClientRecordProperties


class CRecordProperties(QtGui.QDialog, Ui_ClientRecordProperties):
    def __init__(self, parent, table, recordId=None, showRecordId=False):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.table = table
        self.recordId = recordId
        self.showRecordId = showRecordId
        self.setWindowTitle(u'Свойства записи')


    def exec_(self):
        text = self.loadInfo()
        self.edtInfo.setText(text)
        return QtGui.QDialog.exec_(self)


    def loadInfo(self):
        if self.recordId is None:
            return u''
        text = u''
        db = QtGui.qApp.db
        fields = '*'
        record = db.getRecord(self.table, fields, self.recordId)
        createPersonId = forceRef(record.value('createPerson_id'))
        createPersonName = u''
        if createPersonId:
            createPersonRecord = db.getRecord('vrbPersonWithSpeciality', 'name', createPersonId)
            if createPersonRecord:
                createPersonName = forceString(createPersonRecord.value('name'))
        if self.showRecordId:
            text += u'Идентификатор записи: %s\n' % self.recordId
        text += u'Создатель записи: %s\n' % createPersonName
        createDatetime = forceString(record.value('createDatetime'))
        createDatetime = createDatetime if createDatetime else u''
        text += u'Дата создания записи: %s\n' % createDatetime
        modifyPersonId = forceRef(record.value('modifyPerson_id'))
        modifyPersonName = u''
        if modifyPersonId:
            modifyPersonRecord = db.getRecord('vrbPersonWithSpeciality', 'name', modifyPersonId)
            if modifyPersonRecord:
                modifyPersonName = forceString(modifyPersonRecord.value('name'))
        text += u'Редактор записи: %s\n' % modifyPersonName
        modifyDatetime = forceString(record.value('modifyDatetime'))
        modifyDatetime = modifyDatetime if modifyDatetime else u''
        text += u'Дата редактирования записи: %s\n' % modifyDatetime
        actionTypeGroupId = forceRef(record.value('actionTypeGroup_id'))
        if actionTypeGroupId:
            tableATG = db.table('ActionTypeGroup')
            actionTypeGroupRecord = db.getRecordEx(tableATG, [tableATG['code']], [tableATG['id'].eq(actionTypeGroupId), tableATG['deleted'].eq(0)])
            if actionTypeGroupRecord:
                actionTypeGroupCode = forceStringEx(actionTypeGroupRecord.value('code'))
                text += u'Схема: %s\n' % actionTypeGroupCode
        return text
