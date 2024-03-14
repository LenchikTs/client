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
u"""Журнал оповещений"""

from PyQt4 import QtGui
from PyQt4.QtCore import QDate, Qt, QVariant, pyqtSignature

from library.ItemsListDialog import CItemsListDialog, CItemEditorBaseDialog
from library.TableModel import CTextCol, CIntCol, CRefBookCol, CDateTimeCol, CCol
from library.Utils import (forceString, forceDateTime, forceStringEx, forceDate,
     forceRef, forceInt, forceBool)
from RefBooks.Tables import rbNotificationKind
from Notifications.NotificationManager import strSuccess
from Notifications.Ui_NotificationLogEditorDialog import Ui_NotificationLogEditorDialog
from Notifications.Ui_NotificationLogFilterDialog import Ui_ItemFilterDialog
from Notifications.ConfirmationTimeDialog import CConfirmationTimeDialog
from Ui_NotificationLogListDialog import Ui_NotificationLogListDialog

tblNotificationLog = 'Notification_Log'
strError = u'Ошибка'
statuses = (u'Ожидает отправки',
            u'Успешно отправлен опрос',
            u'Получен ответ',
            u'Отказ',
            u'Отмена',
            u'Удалось дозвониться',
            u'Удалось дозвониться и получить подтверждение',
            u'Удалось дозвониться, но подтверждение не получено',
            u'Не удалось дозвониться', 
            strSuccess,
            strError, 
            u'Подтверждено',
            u'Передано в мед. карту')

class CNotificationLogList(Ui_NotificationLogListDialog, CItemsListDialog):
    u"""Список видов оповещений"""
    def __init__(self, parent, clientId=None):
        fileds = [ CIntCol(u'Правило', ['rule_id'], 20),
                   CIntCol(u'Инициатор', ['createPerson_id'], 20),
                   CTextCol(u'Адресат', ['recipient'], 20),
                   CTextCol(u'Адрес', ['addr'], 20),
                   CRefBookCol(u'Вид', ['kind_id'], rbNotificationKind, 20),
                   CIntCol(u'Попытки', ['attempt'], 20),
                   CDateTimeCol(u'Дата создания', ['createDatetime'], 20),
                   CDateTimeCol(u'Дата отправки', ['sendDatetime'], 20),
                   CDateTimeCol(u'Дата подтверждения', ['confirmationDatetime'], 20),
                   CTextCol(u'Текст', ['text'], 40)
                 ]
        table = QtGui.qApp.db.table(tblNotificationLog)
        if table.hasField('status'):
            fileds.append(CEnumColNotificationStatus(u'Статус', ['status'], statuses, 40))
        fileds.append(CTextCol(u'Результат', ['result'], 40))
        CItemsListDialog.__init__(self, parent, fileds, tblNotificationLog, ['id'], filterClass=CNotificationLogFilterDialog, multiSelect=True)
        changeNotificationAction = QtGui.QAction(u'изменить статус', self)
        changeNotificationAction.triggered.connect(self.on_changeNotificationStatus_triggered)
        self.addObject('changeNotificationStatus', changeNotificationAction)
        self.tblItems.createPopupMenu([self.changeNotificationStatus])
        self.setWindowTitleEx(u'Журнал оповещений')
        self.recipient = clientId
        self.isAscending = True
        self.setSort(7)


    def on_changeNotificationStatus_triggered(self):
        selectedItemIdList = self.tblItems.selectedItemIdList()
        confirmationTimeDialog = CConfirmationTimeDialog(self, selectedItemIdList)
        confirmationTimeDialog.exec_()
        remainedIdList = [item for item in selectedItemIdList if item not in confirmationTimeDialog.updatedIdList]
        confirmationTimeDialog.updatedIdList = []
        idList = self.select(self.props)
        self.tblItems.setIdList(idList, None)
        self.tblItems.clearSelection()
        self.tblItems.setSelectedItemIdList(remainedIdList)
    
    
    @pyqtSignature('')
    def on_tblItems_popupMenuAboutToShow(self):
        db = QtGui.qApp.db
        selectedItemIdList = self.tblItems.selectedItemIdList()
        tableNotificationRule = db.table('Notification_Rule')
        tableNotificationLog = db.table('Notification_Log')
        table = tableNotificationLog.innerJoin(tableNotificationRule, tableNotificationRule['id'].eq(tableNotificationLog['rule_id']))
        cols = [tableNotificationRule['allowConfirmation']]
        cond = [tableNotificationLog['id'].inlist(selectedItemIdList)]
        recordList = db.getRecordList(table, cols, cond)
        for record in recordList:
            allowConfirmation = forceBool(record.value('allowConfirmation'))
            if allowConfirmation:
                self.changeNotificationStatus.setEnabled(True)
                return
        self.changeNotificationStatus.setEnabled(False)
    
    
    @pyqtSignature('QModelIndex')
    def on_tblItems_clicked(self):
        db = QtGui.qApp.db
        #notificationId = self.currentItemId()
        notificationId = None
        selectedItemIdList = self.tblItems.selectedItemIdList()
        if len(selectedItemIdList) != 1:
            self.lblAdditionalData.setText('')
        else:
            notificationId = selectedItemIdList[0] if len(selectedItemIdList) == 1 else None
        if notificationId:
            tableNotificationLog = db.table('Notification_Log')
            tableNotificationRule = db.table('Notification_Rule')
            tablePerson = db.table('Person')
            tableSpeciality = db.table('rbSpeciality')
            tablePost = db.table('rbPost')
            tableClient = db.table('Client')
            table = tableNotificationLog.innerJoin(tableNotificationRule, tableNotificationRule['id'].eq(tableNotificationLog['rule_id']))
            table = table.leftJoin(tablePerson, tablePerson['id'].eq(tableNotificationLog['createPerson_id']))
            table = table.leftJoin(tableClient, tableClient['id'].eq(tableNotificationLog['recipient']))
            table = table.leftJoin(tableSpeciality, tableSpeciality['id'].eq(tablePerson['speciality_id']))
            table = table.leftJoin(tablePost, tablePost['id'].eq(tablePerson['post_id']))
            cols = [tablePerson['lastName'].alias('personLastName'),
                    tablePerson['firstName'].alias('personFirstName'),
                    tablePerson['patrName'].alias('personPatrName'),
                    tablePost['name'].alias('postName'), 
                    tableSpeciality['name'].alias('specialityName'), 
                    tableClient['id'].alias('clientId'),
                    tableClient['lastName'].alias('clientLastName'),
                    tableClient['firstName'].alias('clientFirstName'),
                    tableClient['patrName'].alias('clientPatrName'),
                    tableClient['birthDate'].alias('clientBirthDate'),
                    tableClient['birthTime'].alias('clientBirthTime'),
                    tableClient['sex'].alias('ClientSex'),
                    tableNotificationRule['name'].alias('ruleName')
                   ]
            record = db.getRecord(table, cols, notificationId)
            personLastName = forceString(record.value('personLastName')) if record else ''
            personFirstName = forceString(record.value('personFirstName')) if record else ''
            personPatrName = forceString(record.value('personPatrName')) if record else ''
            postName = forceString(record.value('postName')) if record else ''
            specialityName = forceString(record.value('specialityName')) if record else ''
            clientId = forceString(record.value('clientId')) if record else ''
            clientLastName = forceString(record.value('clientLastName')) if record else ''
            clientFirstName = forceString(record.value('clientFirstName')) if record else ''
            clientPatrName = forceString(record.value('clientPatrName')) if record else ''
            birthDateTime = forceString(record.value('clientBirthDate')) + forceString(record.value('clientBirthTime')) if record else ''
            if record:
                sex = u'Муж' if forceInt(record.value('ClientSex')) == 1 else u'Жен'
            else:
                sex = ''
            ruleName = forceString(record.value('ruleName')) if record else ''
            text =  (u'Инициатор: ' + postName + ', ' + specialityName + ', ' + personLastName + ' ' + personFirstName + ' ' + personPatrName + u'\n' +
                     u'Адресат: ' + clientLastName + ' ' + clientFirstName + ' ' + clientPatrName + ', ' + u'Дата рождения: ' + birthDateTime[:-4] + ', ' + u'Пол: ' + sex + u' Код: ' + clientId + u'\n' +
                     u'Правило: ' + ruleName
                    )
            self.lblAdditionalData.setText(text)


    def select(self, props={}):
        db = QtGui.qApp.db
        table = self.model.table()
        cond = self.generateFilterByProps(props)

        if self.recipient:
            cond.append(table['recipient'].eq(self.recipient))

        withoutAddressTemp = props.get('withoutAddressTemp')
        if not withoutAddressTemp:
            addr = props.get('addrTemp')
            if addr:
                cond.append(table['addr'].like(addr))
        else:
            cond.append(table['addr'].isNull())

        withoutRecipientTemp = props.get('withoutRecipientTemp')
        if not withoutRecipientTemp:
            recipient = props.get('recipientTemp')
            if recipient:
                cond.append(table['recipient'].eq(recipient))
        else:
            cond.append(table['recipient'].isNull())

        withoutSendDate = props.get('withoutSendDate', False)
        if not withoutSendDate:
            sendBegDate = props.get('sendBegDate', QDate())
            if sendBegDate:
                cond.append(table['sendDatetime'].ge(
                    forceString(sendBegDate.toString(Qt.ISODate))))

            sendEndDate = props.get('sendEndDate', QDate())
            if sendEndDate:
                cond.append(table['sendDatetime'].le(
                    forceString(sendEndDate.toString(Qt.ISODate))))
        else:
            cond.append(table['sendDatetime'].isNull())

        withoutConfirmationDate = props.get('withoutConfirmationDate', False)
        if not withoutConfirmationDate:
            confirmBegDate = props.get('confirmBegDate', QDate())
            if confirmBegDate:
                cond.append(table['confirmationDatetime'].ge(
                    forceString(confirmBegDate.toString(Qt.ISODate))))

            confirmEndDate = props.get('confirmEndDate', QDate())
            if confirmEndDate:
                cond.append(table['confirmationDatetime'].le(
                    forceString(confirmEndDate.toString(Qt.ISODate))))
        else:
            cond.append(table['confirmationDatetime'].isNull())

        withoutCreatePerson = props.get('withoutCreatePerson')
        if not withoutCreatePerson:
            createPerson = props.get('createPerson')
            if createPerson:
                cond.append(table['createPerson_id'].eq(createPerson))
        else:
            cond.append(table['kind_id'].isNull())

        withoutKind = props.get('withoutKind')
        if not withoutKind:
            kind = props.get('kind')
            if kind:
                cond.append(table['kind_id'].eq(kind))
        else:
            cond.append(table['kind_id'].isNull())
        
        withoutRule = props.get('withoutRule')
        if not withoutRule:
            rule = props.get('rule')
            if rule:
                cond.append(table['rule_id'].eq(rule))
        else:
            cond.append(table['rule_id'].isNull())
        
        withoutType = props.get('withoutType')
        if not withoutType:
            type = props.get('type')
            if type == u'Расписание':
                idList = db.getIdList('Notification_Rule', 'id', 'type = %d' % 0)
                cond.append(table['rule_id'].inlist(idList))
            elif type == u'Картотека':
                idList = db.getIdList('Notification_Rule', 'id', 'type = %d' % 1)
                cond.append(table['rule_id'].inlist(idList))
            elif type == u'Действие':
                idList = db.getIdList('Notification_Rule', 'id', 'type = %d' % 2)
                cond.append(table['rule_id'].inlist(idList))
        else:
            cond.append(table['rule_id'].isNull())

        withoutStatus = props.get('withoutStatus', False)
        if not withoutStatus:
            status = props.get('status')
            if status == strError:
                cond.append(table['status'].eq(10))
            elif status == strSuccess:
                cond.append(table['status'].eq(9))
            elif status == u'Ожидает отправки':
                cond.append(table['status'].eq(0))
            elif status == u'Успешно отправлен опрос':
                cond.append(table['status'].eq(1))
            elif status == u'Получен ответ':
                cond.append(table['status'].eq(2))
            elif status == u'Отказ':
                cond.append(table['status'].eq(3))
            elif status == u'Отмена':
                cond.append(table['status'].eq(4))
            elif status == u'Удалось дозвониться':
                cond.append(table['status'].eq(5))
            elif status == u'Удалось дозвониться и получить подтверждение':
                cond.append(table['status'].eq(6))
            elif status == u'Удалось дозвониться, но подтверждение не получено':
                cond.append(table['status'].eq(7))
            elif status == u'Не удалось дозвониться':
                cond.append(table['status'].eq(8))
            elif status == u'Подтверждено':
                cond.append(table['status'].eq(11))
        else:
            cond.append(table['status'].isNull())
        return db.getIdList(table, self.idFieldName, cond, self.order)


    def getItemEditor(self):
        u"""Возвращает диалог редактировния вида оповещения"""
        return CNotificationLogEditor(self)
        
        
class CNotificationLogEditor(CItemEditorBaseDialog, Ui_NotificationLogEditorDialog):
    u"""Диалог редактирования события журнала оповещений"""
    def __init__(self, parent):
        CItemEditorBaseDialog.__init__(self, parent, tblNotificationLog)
        self.setupUi(self)
        self.buttonBox.setEnabled(False)


    def setRecord(self, record):
        CItemEditorBaseDialog.setRecord(self, record)
        self.edtNotificationRule.setText(forceString(record.value('rule_id')))
        self.edtCreateDatetime.setDateTime(forceDateTime(record.value('createDatetime')))
        self.edtRecipient.setText(forceString(record.value('recipient')))
        self.edtText.setText(forceString(record.value('text')))
        statusInt = forceInt(record.value('status'))
        self.edtStatus.setText(statuses[statusInt])
        self.edtAddress.setText(forceString(record.value('addr')))


class CNotificationLogFilterDialog(QtGui.QDialog, Ui_ItemFilterDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle(u'Фильтр журнала оповещений')
        self.edtSendBegDate.canBeEmpty(True)
        self.edtSendEndDate.canBeEmpty(True)
        self.edtConfirmBegDate.canBeEmpty(True)
        self.edtConfirmEndDate.canBeEmpty(True)
        self.cmbKind.setTable(rbNotificationKind)
        self.cmbRule.setTable('Notification_Rule')
        self.cmbStatus.addItem('')
        self.cmbStatus.addItem(u'Ожидает отправки')
        self.cmbStatus.addItem(u'Успешно отправлен опрос')
        self.cmbStatus.addItem(u'Получен ответ')
        self.cmbStatus.addItem(u'Отказ')
        self.cmbStatus.addItem(u'Отмена')
        self.cmbStatus.addItem(u'Удалось дозвониться')
        self.cmbStatus.addItem(u'Удалось дозвониться и получить подтверждение')
        self.cmbStatus.addItem(u'Удалось дозвониться, но подтверждение не получено')
        self.cmbStatus.addItem(u'Не удалось дозвониться')
        self.cmbStatus.addItem(strSuccess)
        self.cmbStatus.addItem(strError)
        self.cmbStatus.addItem(u'Подтверждено')
        self.cmbStatus.addItem(u'Передано в мед. карту')


    def setProps(self, props):
        self.edtAddressTemplate.setText(props.get('addrTemp', ''))
        self.edtRecipientTemplate.setText(props.get('recipientTemp', ''))
        self.edtSendBegDate.setDate(props.get('sendBegDate', QDate()))
        self.edtSendEndDate.setDate(props.get('sendEndDate', QDate()))
        self.edtConfirmBegDate.setDate(props.get('confirmBegDate', QDate()))
        self.edtConfirmEndDate.setDate(props.get('confirmEndDate', QDate()))
        self.cmbCreatePerson.setValue(props.get('createPerson', 0))
        self.cmbKind.setValue(props.get('kind', 0))
        self.cmbRule.setValue(props.get('rule', 0))
        self.cmbStatus.setCurrentIndex(self.cmbStatus.findData(props.get('status', ''), Qt.DisplayRole))
        self.cmbType.setCurrentIndex(self.cmbType.findData(props.get('type', ''), Qt.DisplayRole))
        self.chkWithoutConfirmDate.setChecked(forceBool(props.get('withoutConfirmationDate', '')))
        self.chkWithoutSendDate.setChecked(forceBool(props.get('withoutSendDate', '')))
        self.chkStatus.setChecked(forceBool(props.get('withoutStatus', '')))
        self.chkType.setChecked(forceBool(props.get('withoutType', '')))
        self.chkKind.setChecked(forceBool(props.get('withoutKind', '')))
        self.chkRule.setChecked(forceBool(props.get('withoutRule', '')))
        self.chkRecipientTemplate.setChecked(forceBool(props.get('withoutRecipientTemp', '')))
        self.chkAddressTemplate.setChecked(forceBool(props.get('withoutAddressTemp', '')))
        self.chkCreatePerson.setChecked(forceBool(props.get('withoutCreatePerson', '')))


    def props(self):
        result = {
         'addrTemp': forceStringEx(self.edtAddressTemplate.text()),
         'recipientTemp': forceStringEx(self.edtRecipientTemplate.text()),
         'sendBegDate': forceDate(self.edtSendBegDate.date()),
         'sendEndDate': forceDate(self.edtSendEndDate.date()),
         'confirmBegDate': forceDate(self.edtConfirmBegDate.date()),
         'confirmEndDate': forceDate(self.edtConfirmEndDate.date()),
         'createPerson': forceRef(self.cmbCreatePerson.value()),
         'kind': forceRef(self.cmbKind.value()),
         'rule': forceRef(self.cmbRule.value()),
         'type': forceRef(self.cmbType.currentText()), 
         'status': forceString(self.cmbStatus.currentText()),
         'withoutConfirmationDate': forceBool(self.chkWithoutConfirmDate.isChecked()),
         'withoutSendDate': forceBool(self.chkWithoutSendDate.isChecked()), 
         'withoutStatus': forceBool(self.chkStatus.isChecked()), 
         'withoutType': forceBool(self.chkType.isChecked()), 
         'withoutKind': forceBool(self.chkKind.isChecked()), 
         'withoutRule': forceBool(self.chkRule.isChecked()), 
         'withoutRecipientTemp': forceBool(self.chkRecipientTemplate.isChecked()), 
         'withoutAddressTemp': forceBool(self.chkAddressTemplate.isChecked()), 
         'withoutCreatePerson': forceBool(self.chkCreatePerson.isChecked())
        }
        return result


    @pyqtSignature('bool')
    def on_chkWithoutSendDate_toggled(self, checked):
        if checked:
            self.edtSendBegDate.setEnabled(False)
            self.edtSendEndDate.setEnabled(False)
            self.lblSendFrom.setEnabled(False)
            self.lblSendTo.setEnabled(False)
        else:
            self.edtSendBegDate.setEnabled(True)
            self.edtSendEndDate.setEnabled(True)
            self.lblSendFrom.setEnabled(True)
            self.lblSendTo.setEnabled(True)


    @pyqtSignature('bool')
    def on_chkWithoutConfirmDate_toggled(self, checked):
        if checked:
            self.edtConfirmBegDate.setEnabled(False)
            self.edtConfirmEndDate.setEnabled(False)
            self.lblConfirmFrom.setEnabled(False)
            self.lblConfirmTo.setEnabled(False)
        else:
            self.edtConfirmBegDate.setEnabled(True)
            self.edtConfirmEndDate.setEnabled(True)
            self.lblConfirmFrom.setEnabled(True)
            self.lblConfirmTo.setEnabled(True)


    @pyqtSignature('bool')
    def on_chkStatus_toggled(self, checked):
        if checked:
            self.cmbStatus.setEnabled(False)
            self.lblStatus.setEnabled(False)
        else:
            self.cmbStatus.setEnabled(True)
            self.lblStatus.setEnabled(True)


    @pyqtSignature('bool')
    def on_chkType_toggled(self, checked):
        if checked:
            self.cmbType.setEnabled(False)
            self.lblType.setEnabled(False)
        else:
            self.cmbType.setEnabled(True)
            self.lblType.setEnabled(True)


    @pyqtSignature('bool')
    def on_chkRule_toggled(self, checked):
        if checked:
            self.cmbRule.setEnabled(False)
            self.lblRule.setEnabled(False)
        else:
            self.cmbRule.setEnabled(True)
            self.lblRule.setEnabled(True)


    @pyqtSignature('bool')
    def on_chkKind_toggled(self, checked):
        if checked:
            self.cmbKind.setEnabled(False)
            self.lblKind.setEnabled(False)
        else:
            self.cmbKind.setEnabled(True)
            self.lblKind.setEnabled(True)


    @pyqtSignature('bool')
    def on_chkRecipientTemplate_toggled(self, checked):
        if checked:
            self.edtRecipientTemplate.setEnabled(False)
            self.lblRecipientTemplate.setEnabled(False)
        else:
            self.edtRecipientTemplate.setEnabled(True)
            self.lblRecipientTemplate.setEnabled(True)


    @pyqtSignature('bool')
    def on_chkAddressTemplate_toggled(self, checked):
        if checked:
            self.edtAddressTemplate.setEnabled(False)
            self.lblAddressTemplate.setEnabled(False)
        else:
            self.edtAddressTemplate.setEnabled(True)
            self.lblAddressTemplate.setEnabled(True)


    @pyqtSignature('bool')
    def on_chkCreatePerson_toggled(self, checked):
        if checked:
            self.cmbCreatePerson.setEnabled(False)
            self.lblCreatePerson.setEnabled(False)
        else:
            self.cmbCreatePerson.setEnabled(True)
            self.lblCreatePerson.setEnabled(True)


class CEnumColNotificationStatus(CCol):
#    """
#      Enum column (like sex etc)
#    """
    def __init__(self, title, fields, vallist, defaultWidth, alignment='l'):
        CCol.__init__(self, title, fields, defaultWidth, alignment)
        self._vallist = vallist

    def format(self, values):
        val = values[0]
        if val:
            if val.isNull():
                return val
            i = val.toInt()[0]
            if 0 <= i <len(self._vallist):
                return QVariant(self._vallist[i])
            else:
                return QVariant('{%s}' % val.toString())
