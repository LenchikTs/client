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
u"""Диалог оповещения пациента"""

from PyQt4 import QtGui

from PyQt4.QtCore import pyqtSignature
from PyQt4.QtGui import QDialogButtonBox

from library.DialogBase import CDialogBase
from library.Utils      import forceString

from Notifications.NotificationManager import CNotificationManager,  parseNotificationTemplate
from Notifications.NotificationRule    import CNotificationRule, tblNotificationRule

from Notifications.Ui_NotifyDialog     import Ui_NotifyDialog

# Коллеги,
# конструктор в одном случае получает список id пациентов
# в другом случае получает спписок троек (id пациентов, scheduleItem, schedule)
# и потом в двух разных местах пытается разобраться - а что собственно получено.

class CNotifyDialog(CDialogBase, Ui_NotifyDialog):
    u"""Диалог редактирования оповещения"""
    def __init__(self, clientInfoList, actionInfoList = None, type=None, cl=None):
        CDialogBase.__init__(self, None)
        self.clientInfoList = clientInfoList
        self.actionInfoList = actionInfoList
        self.setupUi(self)
        filter = 'class=%d' % CNotificationRule.ncInternal if cl is None else 'class=%d' % cl
        filter += ' AND deleted=0'
        if type is not None:
            filter += ' AND type=%d' % type
        if actionInfoList and cl == CNotificationRule.ncExternal:
            filter += ' AND Notification_Rule.condition=%d' % CNotificationRule.ncdResearch
            actionTypeIdString = ''
            for actionTypeInfo in actionInfoList:
                actionTypeIdString += '%d,' % actionTypeInfo[2]
            filter += ' AND actionType_id IN (%s)' % actionTypeIdString[:-1]

        self.cmbNotificationRule.setFilter(filter)
        self.updateButtonBox()


    @pyqtSignature('QAbstractButton*')
    def on_bbxNotify_clicked(self, button):
        u"""Обработчик нажатия кнопок диалога"""
        buttonCode = self.bbxNotify.standardButton(button)
        manager = CNotificationManager()

        if self.clientInfoList and not isinstance(self.clientInfoList[0], tuple):
            self.clientInfoList = [ (clientId, None, None)
                                    for clientId in self.clientInfoList
                                  ]
        if buttonCode == QDialogButtonBox.Ok:
            msg = forceString(self.edtMessage.toPlainText())
            ruleId = self.cmbNotificationRule.value()
            record = QtGui.qApp.db.getRecord('Notification_Rule', '*', ruleId)
            rule = CNotificationRule(record)
            if self.actionInfoList and rule.condition == CNotificationRule.ncdResearch:
                noAddrClientList = manager.notifyClientWithResearchInfo( self.cmbNotificationRule.value(),
                                                                         self.actionInfoList,
                                                                         msg)
            else:
                noAddrClientList = manager.notifyClient( self.clientInfoList,
                                                         self.cmbNotificationRule.value(),
                                                         msg)
            if noAddrClientList:
                names = ''
                for i, val in enumerate(noAddrClientList):
                    if i > 99:
                        names = names + '...'
                        break
                    if (i + 1) % 5 == 0:
                        names = names + val + "\n"
                        continue
                    names = names + val + ', '
                msg = u'Список пациентов для которых не были созданы оповещения по причине отсутствия подходящих контактов:: %s' % names
                QtGui.QMessageBox.critical( self,
                                            u'Отсутствуют подходящие контакты',
                                            msg,
                                            QtGui.QMessageBox.Close)


    def updateExample(self):
        ruleId = self.cmbNotificationRule.value()
        info = self.clientInfoList[0] if len(self.clientInfoList) > 0 else None
        clientId, scheduleItem, schedule = (info
                                            if info and isinstance(info, tuple)
                                            else (info, None, None)
                                           )

        if ruleId and clientId:
            record = QtGui.qApp.db.getRecord(tblNotificationRule, '*', ruleId)
            rule = CNotificationRule(record)
            if (
                  (rule.type == CNotificationRule.ntAction and rule.condition == CNotificationRule.ncdQuiz)
               or (rule.condition == CNotificationRule.ncdResearch)
               ):
                text = rule.template
            else:
                text = parseNotificationTemplate(rule.template, clientId,
                                    (scheduleItem, schedule) if scheduleItem else None,
                                    msg=self.edtMessage.toPlainText())
            if not text:
                text = u'Синтаксическая ошибка в шаблоне'
        else:
            text = u'Выберите правило из списка'

        self.edtMsgExample.setPlainText(text)


    def updateButtonBox(self):
        self.bbxNotify.button(QDialogButtonBox.Ok).setEnabled(
                              self.cmbNotificationRule.value() is not None)


    @pyqtSignature('int')
    def on_cmbNotificationRule_currentIndexChanged(self):
        self.updateExample()
        self.updateButtonBox()


    @pyqtSignature('')
    def on_edtMessage_textChanged(self):
        self.updateExample()

