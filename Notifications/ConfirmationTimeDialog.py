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
from PyQt4.QtCore  import QDateTime, QTime

from Notifications.Ui_ConfirmationTimeDialog import Ui_ConfirmationTimeDialog
from library.Utils  import exceptionToUnicode, forceDate, toVariant, forceTime, forceBool, forceRef
from library.ItemsListDialog import CItemEditorBaseDialog


class CConfirmationTimeDialog(Ui_ConfirmationTimeDialog, CItemEditorBaseDialog):
    def __init__(self, parent, selectedIdList):
        CItemEditorBaseDialog.__init__(self, parent, 'Notification_Log')
        self.setupUi(self)
        self.selectedIdList = selectedIdList
        currentTime = QTime.currentTime()
        self.edtNoteConfirmTime.setTime(currentTime)
        self.updatedIdList = []


    def accept(self):
        try:
            for notificationId in self.selectedIdList:
                confirmationDate = forceDate(self.edtNoteConfirmDate.date())
                confirmationTime = forceTime(self.edtNoteConfirmTime.time())
                db = QtGui.qApp.db
                tableNotificationLog = db.table('Notification_Log')
                tableNotificationRule = db.table('Notification_Rule')
                cols = [tableNotificationLog['id'],
                        tableNotificationLog['status'],
                        tableNotificationLog['confirmationDatetime'], 
                        tableNotificationLog['rule_id']
                       ]
                record = db.getRecord(tableNotificationLog, cols, notificationId)
                ruleId = forceRef(record.value('rule_id'))
                ruleRecord = db.getRecord(tableNotificationRule, '*', ruleId)
                allowConfirm = forceBool(ruleRecord.value('allowConfirmation'))
                if allowConfirm:
                    record.setValue('confirmationDatetime', toVariant(QDateTime(confirmationDate, confirmationTime)))
                    record.setValue('status', toVariant(11))
                    self.setRecord(record)
                    currentId = db.updateRecord(tableNotificationLog, record)
                    self.updatedIdList.append(currentId)
            CItemEditorBaseDialog.accept(self) if allowConfirm else CItemEditorBaseDialog.reject(self)
            return
        except Exception, e:
            QtGui.qApp.logCurrentException()
            QtGui.QMessageBox.critical( self,
                                        u'',
                                        exceptionToUnicode(e),
                                        QtGui.QMessageBox.Close)
