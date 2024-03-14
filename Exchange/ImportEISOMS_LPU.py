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

from library.Utils import forceInt, forceString, forceStringEx, toVariant
from library.database import connectDataBase

from Exchange.Cimport import Cimport

from Exchange.Ui_ImportEISOMS_LPU import Ui_Dialog


# Диалог импорта организаций ЛПУ из ЕИС.ОМС

def ImportEISOMS_LPU(widget):
    # Настройка соединения с ЕИС и запуск диалога
    try:
        EIS_db=QtGui.qApp.EIS_db
        if not EIS_db:
            pref=QtGui.qApp.preferences
            props=pref.appPrefs
            EIS_dbDriverName=forceStringEx(props.get('EIS_driverName', QVariant()))
            EIS_dbServerName=forceStringEx(props.get('EIS_serverName', QVariant()))
            EIS_dbServerPort=forceInt(props.get('EIS_serverPort', QVariant()))
            EIS_dbDatabaseName=forceStringEx(props.get('EIS_databaseName', QVariant()))
            EIS_dbUserName=forceStringEx(props.get('EIS_userName', QVariant()))
            EIS_dbPassword=forceStringEx(props.get('EIS_password', QVariant()))
            EIS_db = connectDataBase(
                EIS_dbDriverName, EIS_dbServerName, EIS_dbServerPort,
                EIS_dbDatabaseName, EIS_dbUserName, EIS_dbPassword, 'EIS')
            QtGui.qApp.EIS_db=EIS_db
        dlg=CImportEISOMS_LPU(widget, EIS_db)
        dlg.edtFileName.setText(EIS_dbDatabaseName)
        dlg.edtIP.setText(EIS_dbServerName)
        dlg.checkName()
        dlg.exec_()
        QtGui.qApp.EIS_db.close()
        QtGui.qApp.EIS_db=None
    except:
        if QtGui.qApp.EIS_db:
            QtGui.qApp.EIS_db.close()
            QtGui.qApp.EIS_db=None
        QtGui.QMessageBox.information(
            None, u'нет связи', u'не удалось установить соединение с базой ЕИС',
            QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)


class CImportEISOMS_LPU(QtGui.QDialog, Ui_Dialog, Cimport):
    # Диалог импорта организаций ЛПУ из ЕИС.ОМС
    def __init__(self, parent, EIS_db):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        Cimport.__init__(self, self.log)
        self.progressBar.setFormat('%v')
        self.EIS_db=EIS_db


    def checkName(self):
        self.btnImport.setEnabled(self.edtFileName.text()!='' and self.edtIP.text()!='')


#    def oldInfisList(self, record):
#        u"""Список старых инфисов организации"""
#        Id = record.value("id").toInt()[0]
#        code = unicode(record.value("CODE").toString())
#        result = []
#        qresult = self.EIS_db.query("""select ID_LPU, ID_HISTORY, CODE
#                        from LPU
#                        where ID_LPU <> %d
#                        and ID_HISTORY = %d
#                        """%(Id, Id))
#        while qresult.next():
#            record = qresult.record()
#            oldcode = unicode(record.value("CODE").toString())
#            if len(oldcode) and oldcode != code:
#                result = result + [oldcode, ]
#            Id = record.value("ID_LPU").toInt()[0]
#            qresult = self.EIS_db.query("""select ID_LPU, ID_HISTORY, CODE
#                        from LPU
#                        where ID_LPU <> %d
#                        and ID_HISTORY = %d
#                        """%(Id, Id))
#        result = list(set(result)) # убираем повторы
#        return result


#    def orgStructureInfisList(self, record):
#        u"""Список инфисов всех подчиненных организаций"""
#        Id = record.value("id").toInt()[0]
#        code = unicode(record.value("CODE").toString())
#        result = []
#        qresult = self.EIS_db.query("""select ID_LPU as id, ID_PARENT, CODE
#                        from LPU
#                        where ID_LPU <> %d
#                        and ID_PARENT = %d
#                        """%(Id, Id))
#        while qresult.next():
#            record = qresult.record()
#            subcode = unicode(record.value("CODE").toString())
#            if len(subcode) and subcode != code:
#                result += [subcode,]
#            result += self.orgStructureInfisList(record)
#        result = list(set(result)) # убираем повторы
#        return result


    def getNumRecords(self):
        # u"""Общее количество записей в источнике"""
        return self.EIS_db.getCount('LPU','1','IS_ACTIVE=1 AND ID_LPU=ID_PARENT AND (CODE != \'\' OR CODE IS NOT NULL)')


    def startImport(self):
        self.prepareNetIds()

        EIS_db = self.EIS_db
        if not EIS_db:
            return
        self.n = 0
        num = self.getNumRecords()
        self.labelNum.setText(u'всего записей в источнике: %d' % num)
        self.progressBar.setMaximum(num)

        stmt='SELECT * FROM LPU WHERE IS_ACTIVE=1 AND ID_LPU=ID_PARENT AND (CODE != \'\' OR CODE IS NOT NULL)'
        query = EIS_db.query(stmt)

        while query.next():
            QtGui.qApp.processEvents()
            if self.abort:
                break
            self.processRecord(query.record())
            self.n += 1
            self.progressBar.step()

        self.log.append(u'готово')
#        self.progressBar.setValue(self.n-1)


    def err2log(self, e):
        if self.log:
            self.log.append(u'запись '+str(self.n)+': '+e)


    def prepareNetIds(self):
        db = QtGui.qApp.db
        table = db.table('rbNet')
        idList = db.getIdList(table, order='id', limit=1)
        fallback = idList[0] if idList else None

        idList = db.getIdList(table, where=u'name like \'в%\'', order='id', limit=1)
        self.adultNetId = idList[0] if idList else fallback
        idList = db.getIdList(table, where=u'name like \'д%\'', order='id', limit=1)
        self.childrenNetId = idList[0] if idList else fallback
        idList = db.getIdList(table, where=u'name like \'ст%\'', order='id', limit=1)
        self.stomatologyNetId = idList[0] if idList else fallback
        idList = db.getIdList(table, where=u'name like \'ж%\'', order='id', limit=1)
        self.womanNetId = idList[0] if idList else fallback



    def processRecord(self, sourceRecord):
        eisLpuId  = forceInt(sourceRecord.value('ID_LPU'))
        tfomsCode = forceString(sourceRecord.value('CODE'))

        shortName = forceStringEx(sourceRecord.value('LPU_SHORT_NAME'))
        bankName  = forceStringEx(sourceRecord.value('LPU_LONG_NAME'))
        printName = forceStringEx(sourceRecord.value('LPU_PRINT_NAME'))

        bik       = forceStringEx(sourceRecord.value('BIK'))
        bankName  = forceStringEx(sourceRecord.value('BANK'))
        branchName= forceStringEx(sourceRecord.value('FILIAL'))
        account   = forceStringEx(sourceRecord.value('PC'))
        #account2  = forceStringEx(sourceRecord.value('PC2'))

        inn       = forceString(sourceRecord.value('INN'))
        #okonh     = forceString(sourceRecord.value('OKONH'))
        okpo      = forceString(sourceRecord.value('OKPO'))
        kpp       = forceString(sourceRecord.value('KPP'))
        ogrn      = forceString(sourceRecord.value('OGRN'))
        #okato     = forceString(sourceRecord.value('OKATO'))
        #kvk       = forceString(sourceRecord.value('KVK'))

        address   = forceStringEx(sourceRecord.value('JUR_ADDRESS'))
        chief     = forceStringEx(sourceRecord.value('FIO'))

        remark    = forceStringEx(sourceRecord.value('REMARK'))
        phone     = forceStringEx(sourceRecord.value('PHONE'))
        fax       = forceStringEx(sourceRecord.value('FAX'))
        email     = forceStringEx(sourceRecord.value('EMAIL'))

        helpType  = forceInt(sourceRecord.value('ID_HELP_TYPE')) # undocumented
        eisLpuType= forceInt(sourceRecord.value('ID_LPU_TYPE')) # undocumented

        anyName   = printName or bankName or shortName
        parts = [ remark,
                  (u'факс: '+fax) if fax else '',
                  (u'e-mail: '+email) if email else ''
                ]
        notes = '; '.join(filter(None, parts))
        orgType   = helpType if helpType in (1, 2) else 3
        if eisLpuType in (14, 18, 21, 22):
            netId = self.childrenNetId
        elif eisLpuType in (5, 6):
            netId = self.womanNetId
        elif eisLpuType in (38, ):
            netId = self.stomatologyNetId
        else:
            netId = self.adultNetId

        orgId = self.findOrg(inn, tfomsCode)
        if orgId:
            if orgId == QtGui.qApp.currentOrgId():
                self.updateOrganisationCode(orgId, eisLpuId)
                self.log.append(u'Обновляем код своего ЛПУ (%s)' % tfomsCode)
            else:
                self.updateOrganisation(orgId, tfomsCode, eisLpuId, anyName, address, chief, phone, notes, orgType)
                self.log.append(u'Обновляем "%s" (%s)' % (anyName, tfomsCode))
        else:
            orgId = self.createOrganisation(tfomsCode, eisLpuId, anyName, address,
                                            inn, okpo, kpp, ogrn,
                                            chief, phone, notes, orgType, netId)
            self.log.append(u'Добавляем "%s" (%s)' % (anyName, tfomsCode))

        if bik and bankName and branchName:
            bankId = self.getBankId(bik, bankName, branchName)
            if orgId != QtGui.qApp.currentOrgId():
                self.updateOrgAccount(orgId, bankId, account, bankName)


    def findOrg(self, inn, tfomsCode):
        db = QtGui.qApp.db
        table = db.table('Organisation')
        idList = []
        if inn:
            idList = db.getIdList(table, where=[table['deleted'].eq(0), table['INN'].eq(inn)], limit=1)
        elif tfomsCode:
            idList = db.getIdList(table, where=[table['deleted'].eq(0), table['infisCode'].eq(tfomsCode)], limit=1)
        return idList[0] if idList else None


    def updateOrganisationCode(self, orgId, eisLpuId):
        db = QtGui.qApp.db
        table = db.table('Organisation')
        record = table.newRecord(('id', 'tfomsExtCode'))
        record.setValue('id', orgId)
        record.setValue('tfomsExtCode', eisLpuId)
        db.updateRecord(table, record)


    def updateOrganisation(self, orgId, tfomsCode, eisLpuId, printName, address, chief, phone, notes, orgType):
        db = QtGui.qApp.db
        table = db.table('Organisation')
        record = db.getRecord(table, '*', orgId)
        record.setValue('infisCode', tfomsCode)
        record.setValue('tfomsExtCode', eisLpuId)
        record.setValue('fullName', printName)
        record.setValue('title', printName)
        record.setValue('address', address)
        record.setValue('chiefFreeInput', chief)
        record.setValue('phone', phone)
        record.setValue('notes', notes)
        record.setValue('isMedical', orgType)
        db.updateRecord(table, record)


    def createOrganisation(self, tfomsCode, eisLpuId, printName, address,
                                 inn, okpo, kpp, ogrn,
                                 chief, phone, notes, orgType, netId):
        db = QtGui.qApp.db
        table = db.table('Organisation')
        record = table.newRecord()
        record.setValue('infisCode', tfomsCode)
        record.setValue('tfomsExtCode', eisLpuId)
        record.setValue('fullName', printName)
        record.setValue('shortName', printName)
        record.setValue('title', printName)
        record.setValue('address', address)
        record.setValue('INN', inn)
        record.setValue('KPP', kpp)
        record.setValue('OGRN', ogrn)
        record.setValue('OKPO', okpo)
        record.setValue('chiefFreeInput', chief)
        record.setValue('phone', phone)
        record.setValue('notes', notes)
        record.setValue('isMedical', orgType)
        record.setValue('net_id', netId)
        return db.insertRecord(table, record)


    def getBankId(self, bik, bankName, branchName):
        db = QtGui.qApp.db
        table = db.table('Bank')
        cond = [ table['deleted'].eq(0),
                 table['BIK'].eq(bik),
                 table['name'].eq(bankName),
                 table['branchName'].eq(branchName),
               ]
        idList = db.getIdList(table, where=db.joinAnd(cond), limit=1)
        if idList:
            return idList[0]
        record = table.newRecord()
        record.setValue('BIK', toVariant(bik))
        record.setValue('name', toVariant(bankName))
        record.setValue('branchName', toVariant(branchName))
        return db.insertRecord(table, record)


    def updateOrgAccount(self, orgId, bankId, account, bankName):
        db = QtGui.qApp.db
        table = db.table('Organisation_Account')
        cond = [ table['organisation_id'].eq(orgId),
                 table['bank_id'].eq(bankId),
                 table['name'].eq('account')
               ]
        idList = db.getIdList(table, where=cond)
        if idList:
            record = table.newRecord(['id', 'bankName'])
            record.setValue('bankName', bankName)
            for id in idList:
                record.setValue('id', id)
                db.updateRecord(table, record)
        else:
            record = table.newRecord()
            record.setValue('organisation_id', orgId)
            record.setValue('bank_id', bankId)
            record.setValue('name', 'account')
            record.setValue('bankName', 'bankName')
