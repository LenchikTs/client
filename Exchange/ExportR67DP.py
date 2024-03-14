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
from PyQt4.QtCore import QDate, QDir, QFile, QIODevice, QTextStream, pyqtSignature, SIGNAL

from library.dbfpy.dbf import Dbf
from library.Utils     import forceBool, forceDate, forceDouble, forceInt, forceRef, forceString, forceStringEx, formatSex, pyDate, toVariant, trim

from Registry.Utils import formatAddress

from Exchange.Ui_ExportR67DPPage1 import Ui_ExportPage1
from Exchange.Ui_ExportPage2 import Ui_ExportPage2


def getAccountInfo(accountId):
    db = QtGui.qApp.db
    accountRecord = db.getRecord('Account', 'settleDate, number, exposeDate,'\
        'contract_id, payer_id', accountId)
    if accountRecord:
        date = forceDate(accountRecord.value('settleDate'))
        exposeDate = forceDate(accountRecord.value('exposeDate'))
        number = forceString(accountRecord.value('number'))
        payerId = forceRef(accountRecord.value('payer_id'))
    else:
        date = exposeDate = payerId = None
        number = ''
    return date, number, exposeDate, payerId


def exportR67DP(widget, accountId, accountItemIdList):
    wizard = CExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.exec_()


class CExportWizard(QtGui.QWizard):
    def __init__(self, parent=None):
        QtGui.QWizard.__init__(self, parent)
        self.setWizardStyle(QtGui.QWizard.ModernStyle)
        self.page1 = CExportPage1(self)
        self.page2 = CExportPage2(self)
        self.addPage(self.page1)
        self.addPage(self.page2)
        self.setWindowTitle(u'Мастер экспорта Смоленской области диспансеризация подростков')
        self.dbfFileName = ''
        self.tmpDir = ''


    def setAccountId(self, accountId):
        self.accountId = accountId
        date, number, exposeDate, payerId = getAccountInfo(accountId)
        strNumber = number if trim(number) else u'б/н'
        strDate = forceString(date) if date else u'б/д'
        self.page1.setTitle(u'Экспорт данных реестра по счёту №%s от %s' %(strNumber, strDate))
        self.page2.setTitle(u'Укажите директорий для сохранения обменных файлов "*.dbf"')


    def setAccountExposeDate(self):
        db = QtGui.qApp.db
        accountRecord = db.table('Account').newRecord(['id', 'exposeDate'])
        accountRecord.setValue('id', toVariant(self.accountId))
        accountRecord.setValue('exposeDate', toVariant(QDate.currentDate()))
        db.updateRecord('Account', accountRecord)


    def getTmpDir(self):
        if not self.tmpDir:
            self.tmpDir = QtGui.qApp.getTmpDir('R67DP')
        return self.tmpDir


    def getFullDbfFileName(self):
        return os.path.join(self.getTmpDir(), self.dbfFileName + '.dbf')


    def getFullTxtFileName(self):
        return os.path.join(self.getTmpDir(), self.dbfFileName + '.txt')


    def setAccountItemsIdList(self, accountItemIdList):
        self.page1.setAccountItemsIdList(accountItemIdList)


    def cleanup(self):
        if self.tmpDir:
            QtGui.qApp.removeTmpDir(self.tmpDir)
            self.tmpDir = ''


    def exec_(self):
        QtGui.QWizard.exec_(self)
        self.cleanup()


# *****************************************************************************************


class CExportPage1(QtGui.QWizardPage, Ui_ExportPage1):
    dpSpecialityMap = {
        '52': 'PEDIATR',
        '48': 'OTOLAR',
        '89': 'HIRURG',
        '49': 'OFTAL',
        '40': 'NEVROL',
        '02': 'GINEKOL',
        '70': 'STOMAT',
        '20': 'ENDOKR',
        '18': 'ANDROL',
        '81': 'ORTOPED'
    }

    def __init__(self, parent):
        QtGui.QWizardPage.__init__(self, parent)
        self.setupUi(self)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(1)
        self.progressBar.setText('')

        self.setTitle(u'Экспорт данных реестра по счёту')
        self.setSubTitle(u'для выполнения шага нажмите кнопку "экспорт"')

        self.setExportMode(False)
        self.aborted = False
        self.done = False
        self.idList = []
        self.parent = parent #wtf? скрывать Qt-шный parent - это плохая затея
        self.ignoreErrors = forceBool(QtGui.qApp.preferences.appPrefs.get(
            'ExportR67DPIgnoreErrors', False))
        self.connect(parent, SIGNAL('rejected()'), self.abort)
        self.chkVerboseLog.setChecked(forceBool(QtGui.qApp.preferences.appPrefs.get(
            'ExportR67DPVerboseLog', 'False')))
        self.chkIgnoreErrors.setChecked(self.ignoreErrors)
        self.accDate = QDate()
        self.dpAnalysisMap = None
        self.actionTypeGroup1 = None
        self.actionTypeGroup2 = None
        self.db = QtGui.qApp.db
        self.tableActionType = self.db.table('ActionType')
        self.tableDiagnostic = self.db.table('Diagnostic')
        self.tableSpeciality = self.db.table('rbSpeciality')
        self.tableAction = self.db.table('Action')
        self.tableNum = 1
        self.exportedClients = set()


    def validatePage(self):
        QtGui.qApp.preferences.appPrefs['ExportR67DPIgnoreErrors'] = toVariant(self.chkIgnoreErrors.isChecked())
        QtGui.qApp.preferences.appPrefs['ExportR67DPVerboseLog'] = toVariant(self.chkVerboseLog.isChecked())
        return self.done


    def setExportMode(self, flag):
        self.btnCancel.setEnabled(flag)
        self.btnExport.setEnabled(not flag)
        self.chkIgnoreErrors.setEnabled(not flag)
        self.chkVerboseLog.setEnabled(not flag)
        self.btnExport.setEnabled(not flag)


    def log(self, str, forceLog = False):
        if self.chkVerboseLog.isChecked() or forceLog:
            self.logBrowser.append(str)
            self.logBrowser.update()


    def setAccountItemsIdList(self, accountItemIdList):
        self.idList = accountItemIdList


    def prepareActionTypeGroups(self):
        if not self.actionTypeGroup1:
            record = self.db.getRecordEx('ActionType', 'id', 'code=\'1-1\' and class=1')

            if record:
                self.actionTypeGroup1 = forceInt(record.value(0)) # id лабораторных исследований

        if not self.actionTypeGroup2:
            record = self.db.getRecordEx('ActionType', 'id', 'code=\'1-2\' and class=1')

            if record:
                self.actionTypeGroup2 = forceInt(record.value(0)) # id лучевой диагностики

        dpAnalysisTypes = [
            # name, code, group_id
            ('AN_KROV', '03', self.actionTypeGroup1), # Дата анализа крови
            ('AN_MOCH', '04', self.actionTypeGroup1), # Дата анализа мочи
            ('AN_KAL', '16', self.actionTypeGroup1), # Дата анализа кала
            ('USI_SHC', '15', self.actionTypeGroup2), # Дата УЗИ щитовидной железы
            ('USI_MJ', '08', self.actionTypeGroup2), # Дата УЗИ молочных желез
            ('USI_MT', '50', self.actionTypeGroup2), # Дата УЗИ органов малого таза
            ('USI_YI', '14', self.actionTypeGroup2), # Дата УЗИ яичек
            ('GLAZ_DNO', '53', self.actionTypeGroup2) # Дата осмотра глазного дна
        ]

        self.dpAnalysisMap = self.makeAnalysisMap(dpAnalysisTypes)


    def makeAnalysisMap(self, types):
        result = {}

        for (key, code,  groupId) in types:
            record = self.db.getRecordEx(self.tableActionType, 'id',
                self.db.joinAnd([self.tableActionType['code'].eq(code),
                                 self.tableActionType['group_id'].eq(groupId)]))
            if record:
                id = forceRef(record.value(0))
                result[id] = key
            else:
                self.log(u'<b><font color=red>ОШИБКА</font></b>:'\
                u' Не найден тип действия с кодом `%s`,'
                u' находящийся в группе id=`%d`,'
                u' необходимый для заполнения поля `%s` файла экспорта.' %\
                (code, groupId, key))

        return result


    def getDiagDates(self,  eventId,  specList):
        u""" Получаем словарь {имя_поля:дата_диагностика} по событию и списку специальностей"""

        stmt='''SELECT Diagnostic.endDate, rbSpeciality.code
            FROM Diagnostic
            LEFT JOIN Person on Diagnostic.person_id=Person.id
            LEFT JOIN rbSpeciality on rbSpeciality.id=Person.speciality_id
            WHERE %s
            ORDER BY rbSpeciality.code
        ''' % self.db.joinAnd([self.tableDiagnostic['event_id'].eq(eventId),
            self.tableSpeciality['code'].inlist(specList.keys())])

        query = self.db.query(stmt)
        result = {}

        while query.next():
            record = query.record()
            if record:
                fieldName = specList.get(forceString(record.value('code')))
                endDate = forceDate(record.value('endDate'))

                if fieldName and endDate:
                    result[fieldName] = endDate

        return result


    def getAnalysisDates(self, eventId, actionTypeMap):
        u""" Получаем словарь {код_типа_действия:дата_окончания} по событию и списку типов действий"""

        result = {}

        if actionTypeMap and eventId:
            recordList = self.db.getRecordList(self.tableAction, 'actionType_id, endDate', [
                self.tableAction['event_id'].eq(eventId),
                self.tableAction['actionType_id'].inlist(actionTypeMap.keys())])


            for record in recordList:
                if record:
                    code = actionTypeMap.get(forceRef(record.value(0)))
                    endDate = forceDate(record.value(1))

                    if code and endDate:
                        result[code] = endDate

        return result


    def prepareToExport(self):
        self.done = False
        self.aborted = False
        self.emit(SIGNAL('completeChanged()'))
        self.setExportMode(True)
        dbf = self.createDbf()
        self.progressBar.reset()
        self.progressBar.setMaximum(1)
        self.progressBar.setValue(0)
        self.progressBar.setText(u'Запрос в БД...')
        QtGui.qApp.processEvents()
        query = self.createQuery()
        self.progressBar.setMaximum(max(query.size(), 1))
        self.progressBar.reset()
        self.progressBar.setValue(0)
        self.prepareActionTypeGroups()
        txt,  txtStream = self.createTxt()
        return dbf, query, txt, txtStream


    def export(self):
        (result, rc) = QtGui.qApp.call(self, self.exportInt)
        self.setExportMode(False)
        if self.aborted or not result:
            self.progressBar.setText(u'прервано')
        else:
            self.progressBar.setText(u'готово')
            self.done = True
            self.emit(SIGNAL('completeChanged()'))


    def getDbfBaseName(self):
        lpuCode = forceString(QtGui.qApp.db.translate(
            'Organisation', 'id', QtGui.qApp.currentOrgId() , 'infisCode'))
        return forceString(lpuCode + u'DP.DBF')


    def getTxtFileName(self):
        lpuCode = forceString(QtGui.qApp.db.translate(
            'Organisation', 'id', QtGui.qApp.currentOrgId() , 'infisCode'))
        return forceString(lpuCode + u'DP.TXT')


    def createTxt(self):
        txt = QFile(os.path.join(self.parent.getTmpDir(), self.getTxtFileName()))
        txt.open(QIODevice.WriteOnly | QIODevice.Text)
        txtStream =  QTextStream(txt)
        txtStream.setCodec('CP866')
        return txt,  txtStream

# *****************************************************************************************

    def exportInt(self):
        self.ignoreErrors = self.chkIgnoreErrors.isChecked()
        lpuId = QtGui.qApp.currentOrgId()
        lpuCode = forceString(QtGui.qApp.db.translate(
            'Organisation', 'id', lpuId , 'infisCode'))
        self.log(u'ЛПУ: код инфис: "%s".' % lpuCode)

        if not lpuCode:
            self.log(u'<b><font color=red>ОШИБКА<\font><\b>:'
                     u'Для текущего ЛПУ не задан код инфис', True)
            if not self.ignoreErrors:
                return

        dbf, query, txt, txtStream = self.prepareToExport()
        self.accDate, accNumber, exposeDate, payerId = getAccountInfo(self.parent.accountId)
        payerStr = forceString(QtGui.qApp.db.translate(
            'Organisation', 'id', payerId , 'title'))
        senderStr = forceString(QtGui.qApp.db.translate(
            'Organisation', 'id', lpuId , 'title'))

        self.writeTextHeader(txtStream, forceString(exposeDate.toString('MM.yyyy')), payerStr, senderStr)
        totalSum = 0.0
        totalFederalSum = 0.0

        if self.idList:
            while query.next():
                QtGui.qApp.processEvents()
                if self.aborted:
                    break
                self.progressBar.step()
                self.process(dbf, query.record(), lpuCode, txtStream)
                totalSum += forceDouble(query.record().value('sum'))
                totalFederalSum += forceDouble(query.record().value('federalSum'))
        else:
            self.log(u'Нечего выгружать.')
            self.progressBar.step()

        self.writeTextFooter(txtStream, totalSum-totalFederalSum, totalFederalSum)
        txt.close()
        dbf.close()


    def createDbf(self):
        u"""Создает структуру dbf файла"""

        dbfName = os.path.join(self.parent.getTmpDir(), self.getDbfBaseName())
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('FAM', 'C', 40),  #    Фамилия
            ('IM', 'C', 40),  # Имя
            ('OT', 'C', 40),  # Отчество
            ('W', 'N', 1), # Пол(1-муж,2-жен)
            ('DR', 'D'), # Дата рождения
            ('SPOL', 'C', 20),  # Серия полиса
            ('NPOL', 'C', 20),  # Номер полиса
            ('Q', 'C', 5),  # СМО
            ('ADRES', 'C', 100),  # Адрес проживания
            ('DS', 'C', 5), # Диагноз
            ('MCOD', 'C', 7),  #Код МО
            ('PEDIATR', 'D'), # Дата приема педиатра
            ('OTOLAR', 'D'), # Дата приема отоларинголога
            ('HIRURG', 'D'), # Дата приема хирурга-ортопеда
            ('OFTAL', 'D'), # Дата приема офтальмолога
            ('NEVROL', 'D'), # Дата приема невролога
            ('GINEKOL', 'D'), # Дата приема гинеколога
            ('ORTOPED', 'D'),  # Дата приема травмотолога-оротопеда
            ('STOMAT', 'D'), # Дата приема стоматолога
            ('ENDOKR', 'D'), # Дата приема эндокринолога
            ('ANDROL', 'D'), # Дата приема уролога-андролога
            ('AN_KROV', 'D'), # Дата анализа крови
            ('AN_MOCH', 'D'), # Дата анализа мочи
            ('AN_KAL', 'D'), # Дата анализа кала
            ('USI_SHC', 'D'), # Дата УЗИ щитовидной железы
            ('USI_MJ', 'D'), # Дата УЗИ молочных желез
            ('USI_MT', 'D'), # Дата УЗИ органов малого таза
            ('USI_YI', 'D'), # Дата УЗИ яичек
            ('GLAZ_DNO', 'D'), # Дата осмотра глазного дна
            ('S_ALL', 'N', 11, 2) #Сумма по диспансеризации
            )

        return dbf

# *****************************************************************************************

    def createQuery(self):
        db = QtGui.qApp.db
        tableAccountItem = db.table('Account_Item')

        stmt = """SELECT Client.id AS clientId,
            Client.lastName,
            Client.firstName,
            Client.patrName,
            Client.birthDate,
            Client.sex,
            Insurer.infisCode AS policyInsurer,
            ClientPolicy.serial AS policySerial,
            ClientPolicy.number AS policyNumber,
            Event.execDate AS endDate,
            ClientRegAddress.address_id AS addressId,
            ClientRegAddress.freeInput AS freeInput,
            Account_Item.`sum`,
            Diagnosis.MKB,
            Account_Item.event_id,
            LEAST(
            IF(Contract_Tariff.federalLimitation = 0,
                Account_Item.amount,
                LEAST(Contract_Tariff.federalLimitation, Account_Item.amount)
               ) * Contract_Tariff.federalPrice, Account_Item.sum)
                AS federalSum
        FROM Account_Item
        LEFT JOIN Event  ON Event.id  = Account_Item.event_id
        LEFT JOIN Client ON Client.id = Event.client_id
        LEFT JOIN ClientPolicy ON ClientPolicy.client_id = Client.id AND
        ClientPolicy.id = (SELECT MAX(CP.id)
            FROM ClientPolicy AS CP
            LEFT JOIN rbPolicyType AS CPT ON CPT.id = CP.policyType_id
            WHERE CP.client_id = Client.id
                AND CP.deleted=0
                AND CPT.code IN ('1','2'))
        LEFT JOIN Contract_Tariff ON Contract_Tariff.id = Account_Item.tariff_id
        LEFT JOIN Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
        LEFT JOIN ClientAddress ClientRegAddress ON ClientRegAddress.client_id = Client.id AND
                  ClientRegAddress.id = (SELECT MAX(CRA.id)
                                     FROM   ClientAddress AS CRA
                                     WHERE  CRA.type = 0 AND CRA.client_id = Client.id AND CRA.deleted=0)
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        LEFT JOIN Diagnostic ON ( Diagnostic.event_id = Account_Item.event_id
            AND Diagnostic.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code IN ('1', '2'))
            AND Diagnostic.person_id = Event.execPerson_id AND Diagnostic.deleted = 0)
        LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
        LEFT JOIN MKB       ON MKB.DiagID = Diagnosis.MKB
        WHERE
            Account_Item.reexposeItem_id IS NULL
        AND (Account_Item.date IS NULL
             OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
            ) AND %s""" % tableAccountItem['id'].inlist(self.idList)

        return db.query(stmt)

# *****************************************************************************************

    def process(self, dbf, record, codeLPU, txtStream):
        eventId = forceString(record.value('event_id'))

        row = dbf.newRecord()
        row['FAM'] = forceString(record.value('lastName')) # Фамилия
        row['IM'] = forceString(record.value('firstName')) # Имя
        row['OT'] = forceString(record.value('patrName')) # Отчество
        row['W'] = forceInt(record.value('sex')) # Пол(1-муж,2-жен)
        row['DR'] = pyDate(forceDate(record.value('birthDate'))) # Дата рождения
        row['SPOL'] = forceString(record.value('policySerial')) # Серия полиса
        row['NPOL'] = forceString(record.value('policyNumber')) # Номер полиса
        row['Q'] = forceString(record.value('policyInsurer')) # СМО
        clientAddress = formatAddress(forceRef(record.value('addressId')))
        row['ADRES'] = clientAddress if clientAddress else forceString(record.value('freeInput')) # Адрес проживания
        row['DS'] = forceString(record.value('MKB')) # Диагноз
        row['MCOD'] = codeLPU #Код МО
        row['S_ALL'] = forceDouble(record.value('sum')) # Сумма по диспансеризации

        diagDates = self.getDiagDates(eventId, self.dpSpecialityMap)
        analysisDates = self.getAnalysisDates(eventId, self.dpAnalysisMap)

        for dicts in (diagDates,  analysisDates):
            for (key, val) in dicts.iteritems():
                row[key] = pyDate(val)

        # пишем строчку в отчет
        self.processTxt(txtStream, record, diagDates,  analysisDates, row['ADRES'])
        row.store()

# *****************************************************************************************
# Отчет

    def writeTextHeader(self, txtStream, period, payer, sender):
        self.tableNum = 1
        self.exportedClients = set()
        txtStream << u'РЕЕСТР счетов за %s на оплату расходов по проведенной диспансеризации подростков.\n\n' % period
        txtStream << u'Учреждение-отправитель %s\n' % sender
        txtStream << u'Учреждение-получатель %s\n\n' % payer
        txtStream << u"""──────┬────────────────────┬────────────────────┬────────────────────┬───┬──────────┬────────────────────────────────────────────────────────────────────────────────────────────────────┬────────────────────────────────────────┬─────┬───────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┬───────────────────────────────────────────┬──────────
№ п/п │      Фамилия       │         Имя        │        Отчество    │Пол│   Дата   │                                       Адрес по месту регистрации                                   │            Серия и номер полиса        │ СМО │ Диагноз по│ Даты осмотров врачами-специалистами, проведения лабораторных и функциональных исследований                                                               │                   УЗИ                     │Норматив
      │                    │                    │                    │   │          │                                                                                                    │                                        │     │   МКБ 10  ├──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬───────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┼──────────┬──────────┬──────────┬──────────┤затрат на
      │                    │                    │                    │   │ рождения │                                                                                                    │                                        │     │ (основной)│  педиатр │ невролог │ офталь-  │ Детский  │ оторино- │ акушер-  │Травматолог│детский   │ Детский  │ Детский  │   Клин.  │   Клин.  │  Анализ  │  Осмотр  │Щитовидной│ молочных │  органов │          │проведение
      │                    │                    │                    │   │          │                                                                                                    │                                        │     │           │          │          │  молог   │  хирург  │ларинголог│гинеколог │ -ортопед  │стоматолог│ уролог-  │ эндокри- │  Анализ  │  Анализ  │   кала   │ глазного │  железы  │  желез   │  малого  │  яичек   │диспансе-
      │                    │                    │                    │   │          │                                                                                                    │                                        │     │           │          │          │          │          │          │          │           │          │ андролог │  нолог   │   крови  │   мочи   │          │    дна   │          │          │   таза   │          │ризации
──────┼────────────────────┼────────────────────┼────────────────────┼───┼──────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────┼─────┼───────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼───────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────
   1  │         2          │          3         │           4        │ 5 │     6    │                                                    7                                               │                     8                  │  9  │     10    │    11    │    12    │    13    │    14    │    15    │    16    │     17    │    18    │    19    │    20    │    21    │    22    │    23    │    24    │    25    │    26    │    27    │    28    │    29
──────┼────────────────────┼────────────────────┼────────────────────┼───┼──────────┼────────────────────────────────────────────────────────────────────────────────────────────────────┼────────────────────────────────────────┼─────┼───────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼───────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────┼──────────\n"""

    def writeTextFooter(self, txtStream, totalSum, totalFederalSum):
        txtStream << u"""──────┴────────────────────┴────────────────────┴────────────────────┴───┴──────────┴────────────────────────────────────────────────────────────────────────────────────────────────────┴────────────────────────────────────────┴─────┴───────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴───────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────\n\nВСЕГО ПРЕДСТАВЛЕНО К ОПЛАТЕ:
По территориальному тарифу на сумму %.2f\n
По дополнительному тарифу на сумму %.2f\n
Руководитель мед.учреждения ____________________
Гл.бухгалтер мед.учреждения ____________________""" % (totalSum, totalFederalSum)

    format = u'%6d│%20.20s│%20.20s│%20.20s│ %1s │%10s│%100.100s│%40.40s│%5.5s│%11.11s│%10s│%10s│%10s│%10s│%10s│%10s│%11s│%10s│%10s│%10s│%10s│%10s│%10s│%10s│%10s│%10s│%10s│%10s│%8.2f\n'

    def processTxt(self, txtStream, record, diagDates,  analysisDates, address):
        clientId = forceRef(record.value('clientId'))

        if clientId in self.exportedClients:
            return

        txtStream << self.format % (
            self.tableNum,
            forceString(record.value('lastName')),
            forceString(record.value('firstName')),
            forceString(record.value('patrName')),
            formatSex(record.value('sex')),
            forceDate(record.value('birthDate')).toString('dd.MM.yyyy'),
            address, '%s %s' % (forceString(record.value('policySerial')), forceString(record.value('policyNumber'))),
            forceString(record.value('policyInsurer')),
            forceString(record.value('MKB')),
            diagDates.get('PEDIATR', QDate()).toString('dd.MM.yyyy'),
            diagDates.get('NEVROL', QDate()).toString('dd.MM.yyyy'),
            diagDates.get('OFTAL', QDate()).toString('dd.MM.yyyy'),
            diagDates.get('HIRURG', QDate()).toString('dd.MM.yyyy'),
            diagDates.get('OTOLAR', QDate()).toString('dd.MM.yyyy'),
            diagDates.get('GINEKOL', QDate()).toString('dd.MM.yyyy'),
            diagDates.get('ORTOPED', QDate()).toString('dd.MM.yyyy'),
            diagDates.get('STOMAT', QDate()).toString('dd.MM.yyyy'),
            diagDates.get('ANDROL', QDate()).toString('dd.MM.yyyy'),
            diagDates.get('ENDOKR', QDate()).toString('dd.MM.yyyy'),
            analysisDates.get('AN_KROV', QDate()).toString('dd.MM.yyyy'),
            analysisDates.get('AN_MOCH', QDate()).toString('dd.MM.yyyy'),
            analysisDates.get('AN_KAL', QDate()).toString('dd.MM.yyyy'),
            analysisDates.get('GLAZ_DNO', QDate()).toString('dd.MM.yyyy'),
            analysisDates.get('USI_SHC', QDate()).toString('dd.MM.yyyy'),
            analysisDates.get('USI_MJ', QDate()).toString('dd.MM.yyyy'),
            analysisDates.get('USI_MT', QDate()).toString('dd.MM.yyyy'),
            analysisDates.get('USI_YI', QDate()).toString('dd.MM.yyyy'),
            forceDouble(record.value('sum'))
        )

        self.exportedClients.add(clientId)
        self.tableNum += 1

# *****************************************************************************************

    def isComplete(self):
        return self.done


    def abort(self):
        self.aborted = True


    @pyqtSignature('')
    def on_btnExport_clicked(self):
        self.export()


    @pyqtSignature('')
    def on_btnCancel_clicked(self):
        self.abort()


class CExportPage2(QtGui.QWizardPage, Ui_ExportPage2):
    def __init__(self, parent):
        QtGui.QWizardPage.__init__(self, parent)
        self.parent = parent #wtf? скрывать Qt-шный parent - это плохая затея
        self.setupUi(self)
        self.setTitle(u'Экспорт данных реестра по счёту')
        self.setSubTitle(u'для выполнения шага нажмите кнопку "финиш"')

        self.pathIsValid = True
        homePath = QDir.toNativeSeparators(QDir.homePath())
        exportDir = forceString(QtGui.qApp.preferences.appPrefs.get('R67DPExportDir', homePath))
        self.edtDir.setText(exportDir)


    def isComplete(self):
        return self.pathIsValid


    def validatePage(self):

        for fileName in (self.parent.page1.getDbfBaseName(),
                            self.parent.page1.getTxtFileName()):
            srcFullName = os.path.join(forceStringEx(self.parent.getTmpDir()),
                                                fileName)
            dst = os.path.join(forceStringEx(self.edtDir.text()),
                                                fileName)
            success, result = QtGui.qApp.call(self, shutil.move, (srcFullName, dst))

        if success:
            QtGui.qApp.preferences.appPrefs['R67DPExportDir'] = toVariant(self.edtDir.text())
            self.wizard().setAccountExposeDate()

        return success


    @pyqtSignature('QString')
    def on_edtDir_textChanged(self):
        dir = forceStringEx(self.edtDir.text())
        pathIsValid = os.path.isdir(dir)
        if self.pathIsValid != pathIsValid:
            self.pathIsValid = pathIsValid
            self.emit(SIGNAL('completeChanged()'))


    @pyqtSignature('')
    def on_btnSelectDir_clicked(self):
        dir = QtGui.QFileDialog.getExistingDirectory(self,
                u'Выберите директорий для сохранения файла выгрузки в ОМС Смоленской области',
                 forceStringEx(self.edtDir.text()),
                 QtGui.QFileDialog.ShowDirsOnly)
        if forceString(dir):
            self.edtDir.setText(QDir.toNativeSeparators(dir))
