#!/usr/bin/env python
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

# Диалог импорта организаций СМО из ЕИС.ОМС

from PyQt4 import QtGui
from PyQt4.QtCore import QDateTime, QVariant

from library.database import connectDataBase
from library.Utils import forceInt, forceString, forceStringEx, toVariant

from Exchange.Cimport import Cimport

# WTF?!
import updateSMO_sql
from Exchange.Ui_ImportEISOMS_SMO import Ui_Dialog


def ImportEISOMS_SMO(widget):
    u"""Настройка соединения с ЕИС и запуск диалога"""
    try:
        EIS_db = QtGui.qApp.EIS_db
        if not EIS_db:
            pref=QtGui.qApp.preferences
            props = pref.appPrefs
            EIS_dbDriverName = forceStringEx(props.get('EIS_driverName', QVariant()))
            EIS_dbServerName = forceStringEx(props.get('EIS_serverName', QVariant()))
            EIS_dbServerPort = forceInt(props.get('EIS_serverPort', QVariant()))
            EIS_dbDatabaseName = forceStringEx(props.get('EIS_databaseName', QVariant()))
            EIS_dbUserName = forceStringEx(props.get('EIS_userName', QVariant()))
            EIS_dbPassword = forceStringEx(props.get('EIS_password', QVariant()))
            EIS_db = connectDataBase(
                EIS_dbDriverName, EIS_dbServerName, EIS_dbServerPort,
                EIS_dbDatabaseName, EIS_dbUserName, EIS_dbPassword, 'EIS')
            QtGui.qApp.EIS_db = EIS_db
        dlg = CImportEISOMS_SMO(widget, EIS_db)
        dlg.edtFileName.setText(EIS_dbDatabaseName)
        dlg.edtIP.setText(EIS_dbServerName)
        dlg.checkName()
        dlg.exec_()
        QtGui.qApp.EIS_db.close()
        QtGui.qApp.EIS_db = None
    except:
        if QtGui.qApp.EIS_db:
            QtGui.qApp.EIS_db.close()
            QtGui.qApp.EIS_db = None
        QtGui.QMessageBox.information(
            None, u'нет связи', u'не удалось установить соединение с базой ЕИС',
            QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)


class CImportEISOMS_SMO(QtGui.QDialog, Ui_Dialog, Cimport):
    # Диалог импорта организаций СМО из ЕИС.ОМС
    def __init__(self, parent, EIS_db):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        Cimport.__init__(self, self.log)
        self.progressBar.setFormat('%v')
        self.EIS_db=EIS_db


    def checkName(self):
        self.btnImport.setEnabled(self.edtFileName.text()!='' and self.edtIP.text()!='')


    def oldInfisList(self, record):
        # Список старых инфисов организации
        Id = forceInt(record.value('id'))
        code = forceString(record.value('CODE'))
        result = set()
        qresult = self.EIS_db.query('SELECT ID_SMO, ID_HISTORY, CODE '\
                                    'FROM SMO '\
                                    'WHERE ID_SMO != %d AND ID_HISTORY = %d'%(Id, Id))
        while qresult.next():
            record = qresult.record()
            oldcode = forceString(record.value('CODE'))
            if oldcode and oldcode != code:
                result.add(oldcode)
            Id = forceInt(record.value('ID_SMO'))
            qresult = self.EIS_db.query('SELECT ID_SMO, ID_HISTORY, CODE '\
                                        'FROM SMO '                       \
                                        'WHERE ID_SMO <> %d and ID_HISTORY = %d'%(Id, Id))
        result = list(result) # убираем повторы
        return result

    def getNumRecords(self):
        # Общее количество записей в источнике
        num_query = self.EIS_db.query('SELECT COUNT(*) FROM SMO where SMO.IS_ACTIVE = 1')
        num_query.next()
        return forceInt(num_query.record().value(0))


    def getNumRegRecords(self):
        # Общее количество записей в источнике
        num_query = self.EIS_db.query('SELECT COUNT(*) FROM VMU_SMO_REG where VMU_SMO_REG.IS_ACTIVE = 1')
        num_query.next()
        return forceInt(num_query.record().value(0))


    def startImport(self):
        self.startImportSMO()
        self.startImportSMOReg()


    def startImportSMO(self):
        db = QtGui.qApp.db
        EIS_db = self.EIS_db
        if not EIS_db:
            return
        self.n = 0
        org_found = 0
        org_add = 0
        num = self.getNumRecords()
        self.labelNum.setText(u'Организаций: '+str(num))
        self.progressBar.setMaximum(num)

        from_stmt = """
        SELECT a.ID_SMO AS id,
            a.ID_HISTORY,
            a.CHANGE_DATE,
            a.SMO_SHORT_NAME,
            a.SMO_LONG_NAME,
            a.BANK,
            a.FILIAL,
            a.INN,
            a.PC,
            a.PC2,
            a.BIK,
            a.OKPO,
            a.ADDRESS,
            a.JUR_ADDRESS,
            a.FIO,
            a.PHONE,
            a.FAX,
            a.EMAIL,
            a.REMARK,
            a.CODE,
            '' as OLD_CODES,
            a.KPP,
            a.FED_CODE
FROM SMO a
where a.IS_ACTIVE = 1
        """
        from_query = EIS_db.query(from_stmt)
        from_query.setForwardOnly(True)
        to_stmt = """
        CREATE TEMPORARY TABLE if not exists tmpSMO(
  id Integer NOT NULL,
  ID_HISTORY Integer NOT NULL,
  CHANGE_DATE Timestamp NOT NULL,
  SMO_SHORT_NAME Varchar(10) NOT NULL,
  SMO_LONG_NAME Varchar(255) NOT NULL,
  BANK Varchar(80) NOT NULL,
  FILIAL Varchar(80) NOT NULL,
  INN Varchar(10) NOT NULL,
  PC Varchar(20) NOT NULL,
  PC2 Varchar(20) NOT NULL,
  BIK Varchar(10) NOT NULL,
  OKPO Varchar(10) NOT NULL,
  ADDRESS Varchar(80) NOT NULL,
  JUR_ADDRESS Varchar(80) NOT NULL,
  FIO Varchar(80) NOT NULL,
  PHONE Varchar(30) NOT NULL,
  FAX Varchar(30) NOT NULL,
  EMAIL Varchar(30) NOT NULL,
  REMARK Varchar(80) NOT NULL,
  CODE Varchar(5) NOT NULL,
  OLD_CODES Varchar(30) NOT NULL,
  KPP Varchar(9) NOT NULL,
  FED_CODE Varchar(5) NOT NULL,
  CONSTRAINT PK_SMO PRIMARY KEY (id)
);
        """
        db.query(to_stmt)
        db.query('DELETE FROM tmpSMO WHERE 1') # на случай, если таблица до этого существовала

        while from_query.next():
            QtGui.qApp.processEvents()
            if self.abort:
                break
            self.n += 1
            record = from_query.record()
            record.setValue('OLD_CODES', toVariant(','.join(self.oldInfisList(record)))) # старые инфисы
            self.record = record
            org_found+=1
            org_add+=1  #?????????????????????????????????????????????
            db.insertRecord('tmpSMO',  self.record)
            self.progressBar.step()
            statusText = u'Найдено %d организаций' %org_found
            self.statusLabel.setText(statusText)

        self.log.append(u'Найдено %d организаций' %org_found)
        result = self.runScript(updateSMO_sql.COMMAND.split('\n'))
        if result:
            self.log.append(result.text())
        else:
            self.log.append(u'готово')
        self.progressBar.setValue(self.n-1)
        #db.query('DROP TABLE tmpSMO')

    def startImportSMOReg(self):
        db = QtGui.qApp.db
        EIS_db = self.EIS_db
        if not EIS_db:
            return
        tableOrganisation = db.table('Organisation')
        self.n = 0
        org_found = 0
        org_add = 0
        num = self.getNumRegRecords()
        text = forceString(self.labelNum.text())
        self.log.append(u'Импортируем региональные организации')
        self.labelNum.setText(text+u', региональных: '+str(num))
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(num)
        from_stmt = """
        SELECT
            a.ID_SMO_REG,
            a.IS_ACTIVE,
            a.OKATO,
            a.NAME_TER,
            a.OGRN_SMO,
            a.SMO_LONG_NAME,
            a.POST_CODE,
            a.ADDRESS,
            a.FAM_RUK,
            a.IM_RUK,
            a.OT_RUK,
            a.FAM_BUX,
            a.IM_BUX,
            a.OT_BUX,
            a.PHONE,
            a.FAX,
            a.EMAIL,
            a.DATE_IN,
            a.DATE_OUT,
            a.INN,
            a.OKVED,
            a.OKPO,
            a.REGION_CODE,
            a.SMO_SHORT_NAME,
            a.SMOCOD,
            RF_REGION.KLADR_CODE_C as kladrCode

        FROM VMU_SMO_REG a
            LEFT JOIN RF_REGION ON RF_REGION.REGION_CODE = a.REGION_CODE
        where a.IS_ACTIVE = 1
        """
        from_query = EIS_db.query(from_stmt)
        from_query.setForwardOnly(True)

        while from_query.next():
            QtGui.qApp.processEvents()
            if self.abort:
                break
            self.n += 1
            recordEIS = from_query.record()
            INN = forceString(recordEIS.value('INN'))
            SMOCOD = forceString(recordEIS.value('SMOCOD'))
            regionCode = forceString(recordEIS.value('kladrCode')).rjust(2, u'0')
            if regionCode == u'78':
                continue
            cond = [tableOrganisation['area'].like('%s%%'%regionCode)]
            if INN:
                cond.append(tableOrganisation['INN'].eq(INN))
            if SMOCOD:
                cond.append(tableOrganisation['smoCode'].eq(SMOCOD))
            existRecord = db.getRecordEx(tableOrganisation, '*', cond)
            if existRecord and regionCode:
                record = existRecord
                record.setValue('modifyPerson_id', QtGui.qApp.userId)
                record.setValue('modifyDatetime', QDateTime.currentDateTime())
                org_found+=1
            else:
                record = db.record('Organisation')
                record.setValue('createPerson_id', QtGui.qApp.userId)
                record.setValue('createDatetime', QDateTime.currentDateTime())
                org_add+=1
            record.setValue('tfomsExtCode',  recordEIS.value('ID_SMO_REG'))
            record.setValue('smoCode', recordEIS.value('SMOCOD'))
            record.setValue('infisCode', recordEIS.value('SMOCOD'))
            record.setValue('fullName', recordEIS.value('SMO_LONG_NAME'))
            record.setValue('shortName', recordEIS.value('SMO_SHORT_NAME'))
            record.setValue('title', recordEIS.value('SMO_SHORT_NAME'))
            record.setValue('OKVED', recordEIS.value('OKVED'))
            record.setValue('INN', recordEIS.value('INN'))
            record.setValue('OGRN', recordEIS.value('OGRN_SMO'))
            record.setValue('OKATO', recordEIS.value('OKATO'))
            record.setValue('OKPO', recordEIS.value('OKPO'))
            record.setValue('isMedical', 0)
            record.setValue('isHospital', 0)
            record.setValue('isInsurer', 1)
            record.setValue('Address', recordEIS.value('ADDRESS'))
            record.setValue('chiefFreeInput', u'%s %s %s'%(
                                                                forceString(recordEIS.value('FAM_RUK')),
                                                                forceString(recordEIS.value('IM_RUK')),
                                                                forceString(recordEIS.value('OT_RUK'))))
            record.setValue('phone', u'Телефон: %s; Факс: %s'%(
                                                                forceString(recordEIS.value('PHONE')),
                                                                forceString(recordEIS.value('FAX'))))
            record.setValue('accountant', u'%s %s %s'%(
                                                                forceString(recordEIS.value('FAM_BUX')),
                                                                forceString(recordEIS.value('IM_BUX')),
                                                                forceString(recordEIS.value('OT_BUX'))))
            record.setValue('area', forceString(recordEIS.value('kladrCode')).rjust(2, u'0').ljust(13, u'0'))
            record.setValue('notes', u'e-mail: %s'%forceString(recordEIS.value('EMAIL')))
            db.insertOrUpdate(tableOrganisation, record)

            self.progressBar.step()
            statusText = u'Добавлено %d организаций, обновлено %i организаций' %(org_add, org_found)
            self.statusLabel.setText(statusText)

        self.log.append(u'Добавлено %d организаций, обновлено %i организаций' %(org_add, org_found))
        self.log.append(u'готово')
        self.progressBar.setValue(self.n-1)

    def err2log(self, e):
        if self.log:
            self.log.append(u'запись '+str(self.n)+': '+e)

