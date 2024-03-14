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

import os.path
import shutil

from PyQt4 import QtGui
from PyQt4.QtCore import QDate

from library.dbfpy.dbf import Dbf
from library.Utils     import forceDate, forceDouble, forceInt, forceString, forceStringEx, pyDate, toVariant


from Exchange.Export import (CExportHelperMixin, CAbstractExportWizard,
     CAbstractExportPage1, CAbstractExportPage2)

from Exchange.Ui_ExportAccountRegisterPage1 import Ui_ExportPage1
from Exchange.Ui_ExportAccountRegisterPage2 import Ui_ExportPage2


def exportRegister(widget, accountId, accountItemIdList):
    wizard = CExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.exec_()

# *****************************************************************************************

class CExportWizard(CAbstractExportWizard):
    def __init__(self, parent=None):
        title = u'Мастер экспорта реестра счетов'
        CAbstractExportWizard.__init__(self, parent, title)

        self.page1 = CExportPage1(self)
        self.page2 = CExportPage2(self)
        self.addPage(self.page1)
        self.addPage(self.page2)


    def getTmpDir(self):
        return CAbstractExportWizard.getTmpDirEx(self, 'Accounts')

# *****************************************************************************************

class CExportPage1(CAbstractExportPage1, Ui_ExportPage1, CExportHelperMixin):
    def __init__(self, parent):
        CAbstractExportPage1.__init__(self, parent)
        CExportHelperMixin.__init__(self)

    def setExportMode(self, flag):
        """Выключаем элементы управления, если flag == True,
        иначе -- включаем. Абстрактный метод."""
        pass

    def createDbf(self):
        dbfName = os.path.join(self.getTmpDir(), 'REGISTER.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('NAME', 'C', 20), # Фамилия
            ('SURNAME', 'C', 20), # Имя
            ('PATRNAME', 'C', 20), # Отчество
            ('BIRTHDATE', 'D'), # Дата рождения
            ('SEX', 'C', 1), # Пол
            ('POLIS_S','C',10),     # Серия полиса
            ('POLIS_N','C',45),     # Номер полиса
            ('POLIS_W','C',30),      # Код СМО, выдавшей полис
            ('DOC_T', 'C', 15), # Тип документа
            ('DOC_S', 'C', 10), # Серия документа
            ('DOC_N', 'C', 20), # Номер документа
            ('ADDR', 'C', 60), # Адрес регистрации
            ('ADDR_KLADR', 'C', 20), # КЛАДР код улицы регистрации
            ('PROFILE', 'C', 10), # Код профиля оплаты
            ('BEGDATE', 'D'), # Дата начала оказания услуги
            ('ENDDATE', 'D'), # Дата окончания оказания услуги
            ('EVENT', 'C', 10),  # External ID
            ('ACCOUNT', 'C', 20), # Номер счета
            ('FINANCETYPE', 'C', 15), # Тип финансирования
            ('AMOUNT', 'N', 2), # Количество
            ('UET', 'N', 11, 2), # УЕТ
            ('PRICE', 'N', 11, 2), # Цена услуги
            ('SUM', 'N', 11, 2), # Сумма
            ('CLIENTID', 'N', 10, 0), # Идентификатор клиента
            ('ACCOUNTID', 'N', 10, 0), # Идентификатор счета
            ('ITEMID', 'N', 10, 0), # Идентификатор позиции в счете
            ('PERSON', 'C', 50), # ФИО оказавшего услугу
            ('SPECIALITY', 'C', 20), # Код специальности оказавшего услугу
            ('ORGSTR', 'C', 45), # Код подразделения, оказавшего услугу
            ('SEND', 'L'), # Флаг обработки записи
            ('ERROR', 'C', 20), # Текст ошибки
            ('PAYTYPE', 'C', 40), # Тип оплаты
        )
        return dbf

# *****************************************************************************************

    def createQuery(self):
        tableAccount = self.db.table('Account')

        stmt = u"""select
            Client.lastName,
            Client.firstName,
            Client.patrName,
            Client.birthDate,
            IF(Client.sex = 1, 'M', 'Ж') as 'sex',
            OMSPolicy.serial    AS omsPolicySerial,
            OMSPolicy.number    AS omsPolicyNumber,
            OMSOrganisation.infisCode AS omsPolicyInsurer,
            DMSPolicy.serial    AS dmsPolicySerial,
            DMSPolicy.number    AS dmsPolicyNumber,
            DMSOrganisation.infisCode AS dmsPolicyInsurer,
            rbDocumentType.name    AS documentType,
            rbDocumentType.regionalCode AS documentRegionalCode,
            ClientDocument.serial  AS documentSerial,
            ClientDocument.number  AS documentNumber,
            AddressHouse.KLADRCode AS KLADRCode,
            AddressHouse.KLADRStreetCode AS KLADRStreetCode,
            AddressHouse.number    AS number,
            AddressHouse.corpus    AS corpus,
            Address.flat           AS flat,
            formatAddress(Address.id) as freeInput,
            Event.externalId as externalId,
            rbService.code,
            Action.begDate,
            Action.endDate,
            rbFinance.code as financeCode,
            rbFinance.name as finance,
            Account.number as account,
            Account_Item.amount,
            Account_Item.uet,
            Account_Item.price,
            Account_Item.sum,
            Client.id as clientid,
            Account.id as accountid,
            Account_Item.id as itemid,
            CONCAT(`Person`.`lastName`,
                _UTF8' ',
                IF((`Person`.`firstName` = _UTF8''),
                    _UTF8'',
                    CONCAT(LEFT(`Person`.`firstName`, 1), _UTF8'.')),
                IF((`Person`.`patrName` = _UTF8''),
                    _UTF8'',
                    CONCAT(LEFT(`Person`.`patrName`, 1), _UTF8'.'))) AS `personName`,

            rbSpeciality.federalCode as specialityCode,
            OrgStructure.code as orgStructureName,
            Contract.payType


            from Account_Item
                LEFT JOIN Account ON Account.id = Account_Item.master_id
                LEFT JOIN Contract ON Contract.id = Account.contract_id
                LEFT JOIN rbFinance on rbFinance.id = Contract.finance_id
                LEFT JOIN Event ON Event.id = Account_Item.event_id
                LEFT JOIN Client ON Client.id = Event.client_id
                LEFT JOIN Action ON Action.id = Account_Item.action_id
                LEFT JOIN ClientPolicy AS OMSPolicy on OMSPolicy.id =
                    (select MAX(CP.id) from ClientPolicy as CP
                        left join rbPolicyType on rbPolicyType.id = CP.policyType_id
                        where CP.deleted=0 and CP.client_id = Client.id and rbPolicyType.isCompulsory = 1)
                LEFT JOIN Organisation as OMSOrganisation on OMSOrganisation.id = OMSPolicy.insurer_id
                LEFT JOIN ClientPolicy AS DMSPolicy on DMSPolicy.id =
                    (select MAX(CP.id) from ClientPolicy as CP
                        left join rbPolicyType on rbPolicyType.id = CP.policyType_id
                        where CP.deleted=0 and CP.client_id = Client.id and rbPolicyType.isCompulsory = 0)
                LEFT JOIN Organisation as DMSOrganisation on DMSOrganisation.id = DMSPolicy.insurer_id
                LEFT JOIN ClientAddress on ClientAddress.id =
                    (select MAX(CA.id) from ClientAddress as CA
                        where CA.client_id = Client.id and CA.type=0)
                LEFT JOIN Address on Address.id = ClientAddress.address_id
                LEFT JOIN AddressHouse on AddressHouse.id = Address.house_id
                LEFT JOIN ClientDocument on ClientDocument.id =
                    (select MAX(CD.id) from ClientDocument as CD
                        where CD.client_id = Client.id)
                LEFT JOIN rbDocumentType on rbDocumentType.id = ClientDocument.documentType_id
                LEFT JOIN rbService on rbService.id = Account_Item.service_id
                LEFT JOIN Person on Person.id = Action.person_id
                LEFT JOIN OrgStructure on OrgStructure.id = Person.orgStructure_id
                LEFT JOIN rbSpeciality ON rbSpeciality.id = Person.speciality_id


            where %s
        """ % tableAccount['id'].inlist(self.idList)
        query = self.db.query(stmt)
        return query

# *****************************************************************************************

    def process(self, dbf, record,  params):
        row = dbf.newRecord()

        row['NAME'] = forceString(record.value('firstName'))
        row['SURNAME'] = forceString(record.value('lastName'))
        row['PATRNAME'] = forceString(record.value('patrName'))
        row['BIRTHDATE'] = pyDate(forceDate(record.value('birthDate')))
        row['SEX'] = forceString(record.value('sex'))
        financeCode = forceString(record.value('financeCode'))
        if financeCode == '2':
            row['POLIS_S'] = forceString(record.value('omsPolicySerial'))
            row['POLIS_N'] = forceString(record.value('omsPolicyNumber'))
            row['POLIS_W'] = forceString(record.value('omsPolicyInsurer'))
        elif financeCode == '3':
            row['POLIS_S'] = forceString(record.value('dmsPolicySerial'))
            row['POLIS_N'] = forceString(record.value('dmsPolicyNumber'))
            row['POLIS_W'] = forceString(record.value('dmsPolicyInsurer'))
        row['DOC_T'] = forceString(record.value('documentType'))
        row['DOC_S'] = forceString(record.value('documentSerial'))
        row['DOC_N'] = forceString(record.value('documentNumber'))
        row['ADDR'] = forceString(record.value('freeInput'))
        row['ADDR_KLADR'] = forceString(record.value('KLADRStreetCode'))
        row['EVENT'] = forceString(record.value('externalId'))
        row['PROFILE'] = forceString(record.value('code'))
        row['BEGDATE'] = pyDate(forceDate(record.value('begDate')))
        row['ENDDATE'] = pyDate(forceDate(record.value('endDate')))
        row['ACCOUNT'] = forceString(record.value('account'))
        row['FINANCETYPE'] = forceString(record.value('finance'))
        row['AMOUNT'] = forceInt(record.value('amount'))
        row['UET'] = forceDouble(record.value('uet'))
        row['PRICE'] = forceDouble(record.value('price'))
        row['SUM'] = forceDouble(record.value('sum'))
        row['CLIENTID'] = forceInt(record.value('clientid'))
        row['ACCOUNTID'] = forceInt(record.value('accountid'))
        row['ITEMID'] = forceInt(record.value('itemid'))
        row['PERSON'] = forceString(record.value('personName'))
        row['SPECIALITY'] = forceString(record.value('specialityCode'))
        row['ORGSTR'] = forceString(record.value('orgStructureName'))
        row['SEND'] = False
        row['ERROR'] = ''
        payTypeId = forceInt(record.value('payType'))
        payTypeDict = { 0:u'не задано',
                        1: u'наличный',
                        2 : u'безналичный',
                        3 : u'комбинированный',
                     }
        payType = payTypeDict.get(payTypeId, payTypeDict)
        row['PAYTYPE'] = payType

        row.store()

# *****************************************************************************************

class CExportPage2(CAbstractExportPage2, Ui_ExportPage2):
    def __init__(self, parent):
        CAbstractExportPage2.__init__(self, parent,  'ExportREGISTER')


    def saveExportResults(self):
        src = 'REGISTER.DBF'
        srcFullName = os.path.join(forceStringEx(self.getTmpDir()),
                                                os.path.basename(src))
        dst = os.path.join(forceStringEx(self.edtDir.text()),
                                                os.path.basename(src))
        success, result = QtGui.qApp.call(self, shutil.move, (srcFullName, dst))
        return success

    def validatePage(self):
        success = self.saveExportResults()

        if success:
            QtGui.qApp.preferences.appPrefs['%sExportDir' % self.prefix] = toVariant(self.edtDir.text())
            for accountId in self.wizard().page1.idList:
                accountRecord = QtGui.qApp.db.table('Account').newRecord(['id', 'exposeDate'])
                accountRecord.setValue('id', toVariant(accountId))
                accountRecord.setValue('exposeDate', toVariant(QDate.currentDate()))
                QtGui.qApp.db.updateRecord('Account', accountRecord)
        return success
