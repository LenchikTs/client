# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2023 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

import os
import os.path
import re
import shutil
from collections import namedtuple

from PyQt4 import QtGui
from PyQt4.QtCore import QDate, QDir, QVariant, pyqtSignature, SIGNAL

from library.dbfpy.dbf  import Dbf
from library.ICDUtils   import MKBwithoutSubclassification
from library.Identification import getIdentification

from library.Utils      import ( calcAgeInMonths,
                                 calcAgeInYears,
                                 calcAgeTuple,
                                 exceptionToUnicode,
                                 forceBool,
                                 forceDate,
                                 forceDateTime,
                                 forceDouble,
                                 forceInt,
                                 forceRef,
                                 forceString,
                                 forceStringEx,
                                 formatSex,
                                 formatSNILS,
                                 formatName,
                                 getInfisCodes,
                                 nameCase,
                                 pyDate,
                                 toVariant,
                                 trim,
                               )
from Registry.Utils     import ( clientIsStudent,
                                 clientIsWorking,
                                 formatAddress,
                                 getAddress,
                                 getClientAddress,
                                 getClientInfo,
                                 getClientWork,
                               )
from Accounting.AccountBuilder import ( CCircumstance,
                                        filterUniqueCircumstances,
                                        getEventActionsCircumstances,
                                        getEventVisitsCircumstances,
                                        getInappropriateCircumstances,
                                        getVisitsFromEventWithSameSevrice,
                                      )

from Accounting.ServiceDetailCache import CServiceDetailCache
from Accounting.Tariff  import CTariff
from Events.Action      import CAction #, CActionType
from Events.ActionServiceType import CActionServiceType

from Exchange.Utils     import getClientRepresentativeInfo

from Exchange.Ui_ExportEISOMSPage1 import Ui_ExportEISOMSPage1
from Exchange.Ui_ExportEISOMSPage2 import Ui_ExportEISOMSPage2


def getAccountInfo(accountId):
    db = QtGui.qApp.db
    accountRecord = db.getRecord('Account', 'date, number', accountId)
#            settleDate = forceDate(accountRecord.value('settleDate'))
    if accountRecord:
        date = forceDate(accountRecord.value('date'))
        number = forceString(accountRecord.value('number'))
    else:
        date = None
        number = ''
    return date, number, adviseDBFFileName(date, number)


def adviseDBFFileName(date, number):
    tmp = trim(''.join([c if c.isalnum() or '-_'.find(c)>=0 else ' ' for c in number]))
    return tmp.replace(' ','_')


def exportEISOMS(widget, accountId, accountItemIdList):
    wizard = CExportEISOMSWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.exec_()
    return wizard.accountItemIdWithException


class CExportEISOMSWizard(QtGui.QWizard):
    def __init__(self, parent=None):
        QtGui.QWizard.__init__(self, parent)
        self.setWizardStyle(QtGui.QWizard.ModernStyle)
        self.page1 = CExportEISOMSPage1(self)
        self.page2 = CExportEISOMSPage2(self)
        self.addPage(self.page1)
        self.addPage(self.page2)
        self.setWindowTitle(u'Мастер экспорта в ЕИС.ОМС.ВМУ.АПУ')
        self.tmpDir = ''
        self.dbfFileName = ''
        self.accountItemIdWithException = None


    def setAccountId(self, accountId):
        self.accountId = accountId
        date, number, fileName = getAccountInfo(accountId)
        self.dbfFileName = fileName
        strNumber = number if trim(number) else u'б/н'
        strDate = forceString(date) if date else u'б/д'
        self.page1.setTitle(u'Экспорт данных реестра по счёту №%s от %s' %(strNumber, strDate))
        self.page2.setTitle(u'Укажите директорий для сохранения обменного файла "%s.dbf"' %(self.dbfFileName))


    def setAccountExposeDate(self):
        db = QtGui.qApp.db
        accountRecord = db.table('Account').newRecord(['id', 'exposeDate'])
        accountRecord.setValue('id', self.accountId)
        accountRecord.setValue('exposeDate', QDate.currentDate())
        db.updateRecord('Account', accountRecord)


    def getTmpDir(self):
        if not self.tmpDir:
            self.tmpDir = QtGui.qApp.getTmpDir('eisoms')
        return self.tmpDir


    def getFullDbfFileName(self, suffix=''):
        return os.path.join(self.getTmpDir(), self.dbfFileName + suffix + '.dbf')


    def getFullClientsDbfFileName(self):
        return os.path.join(self.getTmpDir(), 'pat_' + self.dbfFileName + '.dbf')


    def getFullClientsDbtFileName(self):
        return os.path.join(self.getTmpDir(), 'pat_' + self.dbfFileName + '.dbt')


    def setAccountItemsIdList(self, accountItemIdList):
        self.page1.setAccountItemsIdList(accountItemIdList)


    def cleanup(self):
        if self.tmpDir:
            QtGui.qApp.removeTmpDir(self.tmpDir)
            self.tmpDir = ''


    def exec_(self):
        QtGui.QWizard.exec_(self)
        self.cleanup()

    def setAccountItemIdWithException(self, accountItemId):
        self.accountItemIdWithException = accountItemId



class CExportEISOMSPage1(QtGui.QWizardPage, Ui_ExportEISOMSPage1):
    mapDocTypeToEIS = { '1' : '1', # ПАСПОРТ РФ
                        '2' :'10', # ЗГПАСПОРТ
                        '3' : '3', # СВИД О РОЖД
#                        '2' : '6',
                        '5' : '7', # СПРАВКА ОБ ОСВ
                        '6' : '8', # ПАСПОРТ МОРФЛТ
                        '9' : '6', # ИНПАСПОРТ
                        '14': '2', # ПАСПОРТ СССР
                        '16': '8', # ПАСПОРТ МОРЯКА
                        '24':'24', # СВИД О РОЖД НЕ РФ
                      }

    childrenDocTypes = set(
                           (  3, # СВИД О РОЖД
                              6, # ИНПАСПОРТ
                             10, # ЗГПАСПОРТ
                             24, # СВИД О РОЖД НЕ РФ
                           )
                          )

    mapEventOrderToEIS    = {1: u'п', 2: u'э',               6: u'э', None:u'п'}
    mapEventOrderToForPom = {1: 3,    2:1,    3:3, 4:3, 5:3, 6:2,     None:3}
    mapEventOrderToTransf = {         2:2,    3:1,      5:4, 6:2,     None:1}

    streetTypeDict = { u'ул':     1, # улица
                       u'пр-кт':  2, # проспект
                       u'ш':      3, # шоссе
                       u'аллея':  4, # аллея
                       u'б-р':    5, # бульвар
                       u'кв-л':   6, # квартал
                       u'пер':    7, # переулок
                       u'пл':     8, # площадь
                       u'проезд': 9, # проезд
                       u'туп':   10, # тупик
                       u'наб':   11, # набережная
                       u'линия': 12, # линия
                       u'мкр':   13, # микрорайон
                       u'':      14, # другое
                     }
    # это, вероятно, лучше брать из таблицы. Но у меня нет ясного способа получать эти данные в виде таблицы :-(
    # IDOKATOREG.dbf не годится, так как требуется искать название региона в строке с произвольным форматированием
    # Есть предложение использовать RF_REGION@DBMU.GDB, но лучшее что можно сделать - избежать выгрузки поля IDOKATOREG
    mapKladrCodeToIdRerion = { 41: 93, # Камчатская обл.(вошла в состав Камчатского края)
                               59: 92, # Пермская обл.(вошла в состав Пермского края)
                               75: 94, # Читинская обл.(вошла в состав Забайкальского края)
                               80: 94, # Агинский Бурятский авт.окр.(вошел в состав Забайкальского края)
                               81: 92, # Коми-Пермяцкий авт.окр. (вошел в состав Пермского края)
                               82: 93, # Корякский авт.окр.(вошел в состав Камчатского края)
                               84: 24, # Таймырский авт.окр.(вошел в состав Красноярского края)
                               85: 38, # Усть-Ордынский Бурятский авт.окр.(вошел в состав Иркутской области)
                               88: 24, # Эвенкийский авт.окр.(вошел в состав Красноярского края)
                               90: 52, # Арзамас -16 (г.Саров) (вошел в состав Нижегородской области)
                             }

    # по данным SPRAV_D_TYPE_GROUP
    mapDirectionTypeToGroup = { 1: 2, # Направлен на консультацию в медицинскую организацию по месту прикрепления
                                2: 2, # Направлен на консультацию в иную медицинскую организацию
                                3: 2, # Направлен на обследование
                                4: 2, # Направлен в дневной стационар
                                5: 2, # Направлен на госпитализацию
                                6: 2, # Направлен в реабилитационное отделение
                                7: 1, # Талон ВМП
                                8: 3, # Диспансерное наблюдение
                                9: 2, # Направление не выдано
                               10: 4, # Направление на ЭКО
                               11: 5, # Направление на диализ
                               12: 6, # Отказ пациента от прохождения 2 этапа диспансеризации
                               14: 6, # Согласие пациента на прохождение 2 этапа диспансеризации
                               19:11, # Направление на лечение (вх)
                               20:14, # Направление на исследование
                               21:13, # Направление на 2 этап диспансеризации (вх)
                              }

    def __init__(self, parent):
        QtGui.QWizardPage.__init__(self, parent)
        self.setupUi(self)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(1)
        self.progressBar.setText('')

        self.setTitle(u'Экспорт данных реестра по счёту')
        self.setSubTitle(u'для выполнения шага нажмите кнопку "экспорт"')
        self.chkExportClients.setChecked(forceBool(QtGui.qApp.preferences.appPrefs.get('EISOMSExportClients', False)))
        self.chkGroupByProfile.setChecked(forceBool(QtGui.qApp.preferences.appPrefs.get('EISOMSGroupByProfile', False)))
        self.eisLpuId = forceString(QtGui.qApp.preferences.appPrefs.get('EISOMSLpuId', ''))
        self.isHospital = forceInt(QtGui.qApp.db.translate('Organisation', 'id', QtGui.qApp.currentOrgId(), 'isMedical')) == 2
        self.edtEisLpuId.setText(self.eisLpuId)
        self.setExportMode(False)
        self.aborted = False
        self.done = False
        self.idList = []
        self.mkbCache = {}
        self.serviceDetailCache = CServiceDetailCache()
        self.profileCache = {}
        self.profileSpecCache = {}
        self.kindCache = {}
        self.typeCache = {}
        self.mapMesIdToGroupCode = {}
        self.mapOrgIdToEis = {}
        self.mapOrgIdToOffsideLpuId = {}
        self.mapOrgAndOrgStructureIdToEisOrgStructureCode = {}
        self.mapServiceIdToSpravGroupNmlkId = {}
        self.mapServiceIdToDirectionTypeAndGroup = {}
        self.mapPersonIdToEisOrgStructureCode = {}
        self.mapPersonIdToEisPersonId = {}
        self.payers = {}
        self.currentOrgId = QtGui.qApp.currentOrgId()
        self.receivingDepartmentIdentifier = self.getReceivingDepartmentIdentifier()
        self.completedTreatmentCaseUnitCode = None
        self.gynecologicalExaminations = set(['Z30.0', 'Z30.4', 'Z32.0', 'Z32.1', 'Z34.0', 'Z34.9', 'Z35.2', 'Z35.9', 'Z39.0', 'Z39.1', 'Z39.2'])
        self.connect(parent, SIGNAL('rejected()'), self.abort)


    def setAccountItemIdWithException(self, accountItemId):
        self.wizard().setAccountItemIdWithException(accountItemId)


    def setExportMode(self, flag):
        self.btnCancel.setEnabled(flag)
        self.btnExport.setEnabled(not flag)


    def setAccountItemsIdList(self, accountItemIdList):
        self.idList = accountItemIdList


    def prepareToExport(self, ignoreConfirmation, exportClients, includeEvents, includeVisits, includeActions):
        self.done = False
        self.aborted = False
        self.emit(SIGNAL('completeChanged()'))
        self.setExportMode(True)
        self.dbf = self.createDbf()
        self.extServDbf         = self.createExtServDbf()
        self.extDocDbf          = self.createExtDocDbf()
        self.extCaseDbf         = self.createExtCaseDbf()
        self.directionDbf       = self.createDirectionDbf()
        self.clientsDbf         = self.createClientsDbf() if exportClients else None
        self.onkoAddDbf         = self.createOnkoAddDbf()
        self.onkoServDbf        = self.createOnkoServDbf()
        self.onkoDiagnosticsDbf = self.createOnkoDiagnosticsDbf()
        self.onkoConsiliumDbf   = self.createOnkoConsiliumDbf()
        self.onkoDrugsDbf       = self.createOnkoDrugsDbf()
        self.covidAddDbf        = self.createCovidAddDbf()
        self.covidDrugsDbf      = self.createCovidDrugsDbf()
        self.medDevDbf          = self.createMedDevDbf()
        query = self.createQuery(ignoreConfirmation, includeEvents, includeVisits, includeActions)
        self.progressBar.setMaximum(max(query.size(), 1))
        self.progressBar.reset()
        self.progressBar.setValue(0)
        return query


    def export(self,
               ignoreConfirmation,
               exportClients,
               includeEvents,
               includeVisits,
               includeActions,
               groupByProfile,
               eisLpuId):
        QtGui.qApp.call(self,
                        self.exportInt,
                        (ignoreConfirmation,
                         exportClients,
                         includeEvents,
                         includeVisits,
                         includeActions,
                         groupByProfile,
                         eisLpuId))
        self.setExportMode(False)
        if self.aborted:
            self.progressBar.setText(u'прервано')
        else:
            self.progressBar.setText(u'готово')
            self.done = True
            self.emit(SIGNAL('completeChanged()'))


    def exportInt(self,
                  ignoreConfirmation,
                  exportClients,
                  includeEvents,
                  includeVisits,
                  includeActions,
                  groupByProfile,
                  eisLpuId):
        self.groupByProfile = groupByProfile
        self.eisLpuId = eisLpuId
        query = self.prepareToExport(ignoreConfirmation,
                                     exportClients,
                                     includeEvents,
                                     includeVisits,
                                     includeActions)
        self.knownClientIdSet = set()
        self.mapClientIdToNewbornId = {}
        self.caseRegistry = {}
        self.mapEventIdToCount = {}
        self.mapServiceToDBFRecord = {}
        self.cachedLeaveHospitalBedProfileForEventId = None
        self.directionToFix = {}
        prevEventId = None
        self.setAccountItemIdWithException(None)
        if self.idList:
            while query.next():
                QtGui.qApp.processEvents()
                if self.aborted:
                    break
                self.progressBar.step()
                record = query.record()
                eventId = forceRef(record.value('eventId'))
                if prevEventId != eventId:
                    if prevEventId:
                        self.fixDirectionsAtEventFinish()
                    self.mapServiceToDBFRecord = {}
                    self.directionToFix = {}
                    prevEventId = eventId
                try:
                    self.process(record)
                except Exception as e:
                    QtGui.qApp.logCurrentException()
                    self.setAccountItemIdWithException(forceRef(record.value('accountItem_id')))
                    message = exceptionToUnicode(e)
                    eventId = forceRef(record.value('event_id'))
                    clientId = forceRef(record.value('client_id'))
                    clientInfo = getClientInfo(clientId)
                    clientName = formatName(clientInfo.lastName, clientInfo.firstName, clientInfo.patrName)
                    raise Exception(u'%s\nКод карточки: %d\nКод пациента: %d\nПациент: %s' % (message, eventId, clientId, clientName))
        else:
            self.progressBar.step()

        # было обнаружено, что ЕИС не может принять данные, если в выгрузке существует
        # такой case, что не существует записи с ID_PRVS == ID_PRVS_C
        # (это может быть, если исcледование проведено - и выставляется -
        # после выставления других позиций). Принято решение искать такие данные
        # и исправлять ID_PRVS_C на ID_PRVS из первой записи.
        caseFixup = {}
        for eventId, caseInfo in self.caseRegistry.iteritems():
            eventSpecialityCode, itemSpecialityCodeList = caseInfo
            if itemSpecialityCodeList and eventSpecialityCode not in itemSpecialityCodeList:
                caseFixup[eventId] = itemSpecialityCodeList[0]

        for i in xrange(len(self.dbf)):
            dbfRecord = self.dbf[i]
            eventId = dbfRecord['SERV_ID']
            if eventId in caseFixup and dbfRecord['ID_PRVS_C'] != caseFixup[eventId]:
                dbfRecord['ID_PRVS_C'] = caseFixup[eventId]
                dbfRecord.store()

        self.dbf.close()
        self.extServDbf.close()
        self.extDocDbf.close()
        self.extCaseDbf.close()
        self.directionDbf.close()
        if self.clientsDbf is not None:
            self.clientsDbf.close()
        self.onkoAddDbf.close()
        self.onkoServDbf.close()
        self.onkoDiagnosticsDbf.close()
        self.onkoConsiliumDbf.close()
        self.onkoDrugsDbf.close()
        self.covidAddDbf.close()
        self.covidDrugsDbf.close()
        self.medDevDbf.close()

        if len(self.extServDbf) == 0 and len(self.extCaseDbf) == 0:
            os.unlink(self.extServDbf.name)
            os.unlink(self.extCaseDbf.name)
#        if len(self.extDocDbf) == 0:
#            os.unlink(self.extDocDbf.name)
        if len(self.directionDbf) == 0:
            os.unlink(self.directionDbf.name)
        if (    len(self.onkoAddDbf) == 0
            and len(self.onkoServDbf) == 0
            and len(self.onkoDiagnosticsDbf) == 0
            and len(self.onkoConsiliumDbf) == 0
            and len(self.onkoDrugsDbf) == 0
           ):
            os.unlink(self.onkoAddDbf.name)
            os.unlink(self.onkoServDbf.name)
            os.unlink(self.onkoDiagnosticsDbf.name)
            os.unlink(self.onkoConsiliumDbf.name)
            os.unlink(self.onkoDrugsDbf.name)
        if len(self.covidAddDbf) == 0 and len(self.covidDrugsDbf) == 0:
            os.unlink(self.covidAddDbf.name)
            os.unlink(self.covidDrugsDbf.name)
        if len(self.medDevDbf) == 0:
             os.unlink(self.medDevDbf.name)

    def createDbf(self):
        dbf = Dbf(self.wizard().getFullDbfFileName(), new=True, encoding='cp866')
        dbf.addField(
            # 1234567890 - максимум - 10 символов
            ('SURNAME',    'C', 40),    # Фамилия пациента
            ('NAME1',      'C', 40),    # Имя пациента
            ('NAME2',      'C', 40),    # Отчество пациента
            ('BIRTHDAY',   'D'),        # Дата рождения
            ('SEX',        'C',  1),    # Пол (М/Ж)
            ('ORDER',      'C',  1),    # Признак экстренности случая лечения
                                        # (если случай экстренный - принимает значение "э" или "Э")
            ('POLIS_S',    'C', 10),    # Серия полиса
            ('POLIS_N',    'C', 20),    # Номер полиса
#            ('POLIS_W',    'C',  5),    # Код СМО, выдавшей полис (удалить)
            ('PAYER',      'C',  5),    # Код СМО, выдавшей полис?
            ('STREET',     'C', 25),    # Адрес пациента: код улицы
            ('STREETYPE',  'C',  2),    # Адрес пациента: тип улицы
            ('AREA',       'C',  3),    # Адрес пациента: код район
            ('HOUSE',      'C',  7),    # Адрес пациента: номер дома
            ('KORP',       'C',  2),    # Адрес пациента: корпус
            ('FLAT',       'C', 15),    # Адрес пациента: номер квартиры
            ('PROFILE',    'C', 30),    # Код профиля лечения
            ('PROFILENET', 'C',  1),    # Тип сети профиля (в - взрослая, д - детская)
            ('DATEIN',     'D'),        # Дата начала услуги
            ('DATEOUT',    'D'),        # Дата окончания услуги
            ('AMOUNT',     'N', 15, 5), # Объем лечения (кратность услуги)
            ('AMOUNT_D',   'N',  3, 0), # кол-во дней (для случая МЭС ДСТАЦ при ЛПУ)
            ('DIAGNOSIS',  'C', 10),    # Код диагноза (6 - со звездой, нужно 5, - без звезды?)
            ('DIAG_PREF',  'C',  7),    # Код сопутствующего диагноза
            ('SEND',       'L'),        # Флаг обработки записи
            ('ERROR',      'C',250),    # Описание ошибки
            ('TYPEDOC',    'C',  1),    # Тип документа
            ('SER1',       'C', 10),    # Серия документа, левая часть
            ('SER2',       'C', 10),    # Серия документа, левая часть
            ('NPASP',      'C', 10),    # Номер документа
            ('SERV_ID',    'N', 11, 0), # Идентификатор случая
            ('ID_IN_CASE', 'N',  3, 0), # Порядковый номер записи в случае (в пределах одного SERV_ID)
            ('ID_PRVS',    'N', 11),    # Региональный код специальности врача
            ('IDPRVSTYPE', 'N',  6, 0), # код типа указанной услуги для КСГ
            ('PRVS_PR_G',  'N',  6, 0), # номер группы из справочника профилей ЗСКСГ
            ('ID_EXITUS',  'N', 11),    # исход лечения
            ('ILLHISTORY', 'C', 50),    # номер история болезни
            ('CASE_CAST',  'N',  6, 0), # тип случая лечения
            ('ID_PRMP',    'N',  6, 0), # Код профиля по Классификатору профиля
            ('ID_PRMP_C',  'N',  6, 0), # Код профиля по Классификатору профиля для случая лечения
            ('DIAG_C',     'C', 10),    # Код диагноза для случая лечения
            ('DIAG_S_C',   'C', 10),    # Код сопутствующего диагноза для случая лечения
            ('DIAG_P_C',   'C', 10),    # Код предварительного диагноза для случая лечения
            ('QRESULT',    'N',  6, 0), # Результат обращения за медицинской помощью
            ('ID_PRVS_C',  'N', 11, 0), # ID врачебной специальности для случая лечения
            ('ID_SP_PAY',  'N',  6, 0), # ID способа оплаты медицинской помощи
            ('ID_ED_PAY',  'N',  5, 2), # Количество единиц оплаты медицинской помощи
            ('ID_VMP',     'N',  6, 0), # ID вида медицинской помощи
            ('ID_DOC',     'C', 20),    # Идентификатор врача из справочника SPRAV_DOC.DBF (для услуги)
            ('ID_DEPT',    'C', 20),    # Идентификатор отделения МО из справочника SPRAV_DEPTS.DBF (для услуги)
            ('ID_DOC_C',   'C', 20),    # Идентификатор врача из справочника SPRAV_DOC.DBF (для случая)
            ('ID_DEPT_C',  'C', 20),    # Идентификатор отделения МО из справочника SPRAV_DEPTS.DBF (для случая)
            ('IS_CRIM',    'L'),        # криминал F - нет , T - есть
            ('IDSERVDATA', 'N', 11, 0), # Идентификатор пункта карты диспансеризации (SPRAV_PRVS_PROFILE.DBF)
            ('IDSERVMADE', 'N',  6, 0), # Идентификатор порядка выполнения пункта карты диспансеризации (Кодификатор в руководстве пользователя)
            ('IDSERVLPU',  'N', 11, 0), # Идентификатор ЛПУ, выполнившего пункт карты диспансеризации (из справочника SPRAV_LPU.DBF)
            ('ID_GOAL',    'N',  6, 0), # ID цели обращения для услуги (SPRAV_GOAL.DBF)
            ('ID_GOAL_C',  'N',  6, 0), # ID цели обращения для случая (SPRAV_GOAL.DBF)
            ('ID_PAT_CAT', 'N',  6, 0), # статус пациента (0 - без изм. 7 - не работает, 8 - работает)
            ('ID_GOSP',    'N',  6, 0), # Тип госпитализации
            ('IDVIDVME',   'N',  6, 0), # Идентификатор вида мед. вмешательства
            ('IDFORPOM',   'N',  6, 0), # Идентификатор формы оказания помощи
            ('IDMETHMP',   'N',  6, 0), # Идентификатор метода высокотехнологичной мед помощи
            ('ID_LPU',     'N', 11,  0),# Идентификатор БД ЛПУ, в которую загружаются данные
            ('N_BORN',     'N',  1,  0),# Порядковый номер новорожденного
            ('IS_STAGE',   'L'),        # Признак "Этапное лечение"
            ('ID_FINT',    'N', 11, 0), # тип финансирования (SPRAV_FIN_TYPE)
            ('ID_CASE',    'C', 20),    # Идентификатор случая в БД ЕИС (проставляется после принятия)
            ('ID_SERV',    'C', 20),    # Идентификатор услуги в БД ЕИС (проставляется после принятия)
            ('SNILS',      'C', 14),    # СНИЛС пациента (для обновления) - необязательное поле
            ('ID_TRANSF',  'N', 6, 0),  # Признак перевода (для случая)
            ('ID_INCOMPL', 'N', 6, 0),  # Признак "Неполный объём" (для услуги)
            ('ID_MAIN',    'N', 3, 0),  # Идентификатор (поле ID_IN_CASE) главной услуги (для сопутствующих услуг)
            ('ID_LPU_P',   'N',11, 0),  # Идентификатор подразделения МО (для услуги)   Обязательное    SPRAV_LPU   ID_LPU  1.2.3.146
            ('ID_LPU_P_C', 'N',11, 0),  # Идентификатор подразделения МО (для случая)   Обязательное    SPRAV_LPU   ID_LPU  1.2.3.146
            ('ID_B_PROF',  'N',11, 0),  # Идентификатор профиля койки
            ('ID_C_ZAB',   'N',11, 0),  # Идентификатор характера основного заболевания
            ('ID_INTER',   'N',11, 0),  # Идентификатор признака прерванности случая

            # были, но сплыли
#            ('ID_LPU_D',   'N', 11, 0), # Идентификатор ЛПУ, направившего на лечение (из справочника SPRAV_LPU.DBF)
#            ('ID_PRVS_D',  'N', 11),    # Идентификатор специальности направившего врача
#            ('ID_GOAL_D',  'N', 5),     # ID цели обращения при направлении
            ('PRIM',       'C', 255),   # примечание - возврат от страховщиков
#            ('IDVIDHMP',   'N',  2, 0), # Идентификатор вида высокотехнологичной мед помощи
#            ('ID_LPU_RF',  'N',11, 0),  # Идентификатор иногородней МО

            # наши поля
            ('LONGADDR',   'C',120),    # Длинный адрес
            ('ACC_ID',     'N', 11),    # Account.id
            ('ACCITEM_ID', 'C', 255),   # список Account_Item.id через пробел
            ('ACTION_ID',  'N', 11),    #
            ('CLIENT_ID',  'N', 11),    # Client.id
            # 1234567890 - максимум - 10 символов
        )
        return dbf


    def createExtServDbf(self):
        dbf = Dbf(self.wizard().getFullDbfFileName('_V'), new=True, encoding='cp866')
        dbf.addField(
            # 1234567890 - максимум - 10 символов
            ('SERV_ID',    'N', 11, 0), # Идентификатор случая лечения в основном файле импорта услуг
            ('ID_IN_CASE', 'N',  3, 0), # Порядковый номер услуги (записи) в рамках одного SERV_ID
            ('DATE_BEGIN', 'D'),        # Дата начала
            ('DATE_END',   'D'),        # Дата окончания
            ('ID_NMKL',    'N', 11, 0), # ID номенклатуры
            ('V_MULTI',    'N',  6, 0), # Кратность
            ('V_LONG_IVL', 'N',  6, 0), # Кол-во часов ИВЛ
            ('V_LONG_MON', 'N',  6, 0), # Кол-во часов мониторинга
            ('ERROR',      'C',200),    # Описание ошибки
            # 1234567890 - максимум - 10 символов
        )
        return dbf


    def createExtDocDbf(self):
        dbf = Dbf(self.wizard().getFullDbfFileName('_VDOC'), new=True, encoding='cp866')
        dbf.addField(
            # 1234567890 - максимум - 10 символов
            ('SERV_ID',    'N', 11, 0), # Идентификатор случая лечения в основном файле импорта услуг
            ('ID_IN_CASE', 'N',  3, 0), # Порядковый номер услуги (записи) в рамках одного SERV_ID
            ('ID_PRVS',    'N', 11, 0), # Идентификатор врачебной специальности
            ('ID_DOC',     'C', 20),    # Идентификатор медицинского работника
            ('IDDATAOBJ',  'N', 11, 0), # Тип записи: 4 - диспансеризация, 3 - прочее
            ('ERROR',      'C',200),    # Описание ошибки
            # 1234567890 - максимум - 10 символов
        )
        return dbf


    def createExtCaseDbf(self):
        dbf = Dbf(self.wizard().getFullDbfFileName('_ADD'), new=True, encoding='cp866')
        dbf.addField(
            # 1234567890 - максимум - 10 символов
            ('SERV_ID',    'N', 11, 0), # Идентификатор случая лечения в основном файле импорта услуг
            ('ID_OBJECT',  'N',  4, 0), # Идентификатор объекта учета
            ('OBJ_VALUE',  'C', 10),    # Значение объекта учета
            ('DIAG',       'C',  5),    # Пасхалочка...
            ('ERROR',      'C',200),    # Описание ошибки
            # 1234567890 - максимум - 10 символов
        )
        return dbf


    def createDirectionDbf(self):
        dbf = Dbf(self.wizard().getFullDbfFileName('_D'), new=True, encoding='cp866')
        dbf.addField(
            # 1234567890 - максимум - 10 символов
            ('SERV_ID',    'N', 11, 0), # Идентификатор случая лечения в основном файле импорта услуг
            ('ID_IN_CASE', 'N',  3, 0), # Порядковый номер услуги в рамках случая
            ('D_NUMBER',   'C', 20),    # Номер направления (талона)
            ('DATE_ISSUE', 'D'),        # Дата выдачи направления (талона)
            ('DATE_PLANG', 'D'),        # Дата планируемой госпитализации
            ('ID_LPU_F',   'N', 11, 0), # Идентификатор МО (откуда) Пусто   SPRAV_LPU   ID_LPU
            ('ID_LPU_T',   'N', 11, 0), # Идентификатор МО (куда)   Пусто   SPRAV_LPU   ID_LPU
            ('ID_D_TYPE',  'N', 11, 0), # Тип направления (назначения)
            ('ID_D_GROUP', 'N', 11, 0), # Группа направления (назначения)
            ('ID_PRVS',    'N', 11, 0), # Идентификатор специальности врача
            ('ID_OB_TYPE', 'N', 11, 0), # Идентификатор вида обследования
            ('ID_PRMP',    'N', 11, 0), # Идентификатор профиля медицинской помощи
            ('ID_B_PROF',  'N', 11, 0), # Идентификатор профиля койки
            ('ID_DN',      'N', 11, 0), # Идентификатор диспансерного наблюдения    Пусто   SPRAV_DN_ACTION ID_DN   1.2.3.157
            ('ID_GOAL',    'N', 11, 0), # Идентификатор цели обращения  Пусто   SPRAV_GOAL  ID_GOAL 1.2.3.157
            ('ID_DIAGNOS', 'N', 11, 0), # Идентификатор диагноза    Пусто   SPRAV_DIAG  ID_DIAGNOS  1.2.3.157
            ('ID_LPU_RF',  'N', 11, 0), # Идентификатор иногородней МО  Пусто   SPRAV_LPU_RF    ID_LPU_RF   1.2.3.157
            ('IDLPURF_TO', 'N', 11, 0), # Идентификатор иногородней МО (куда)
            ('ID_NMKL',    'N', 11, 0), # Идентификатор номенклатурной услуги
            ('ID_DOC',     'C', 20),    # Код медицинского работника, выдавшего направление
            ('IDDOCPRVS',  'N', 11, 0), # Cпециальность медицинского работника, выдавшего направление
            ('ERROR',      'C',200),    # Описание ошибки
            # Наши поля:
            ('CASE',       'C', 10),    # код причины добавления записи
            ('DIAG',       'C',  5),    # Ненавижу ID_DIAGNOS!
            ('ACTION_ID' , 'N', 11),    # Action.id, если есть...
            # 1234567890 - максимум - 10 символов
        )
        return dbf


    def createClientsDbf(self):
        dbf = Dbf(self.wizard().getFullClientsDbfFileName(), new=True, encoding='cp866')
        dbf.addField(
            # 1234567890 - максимум - 10 символов
            ('SURNAME',    'C', 30),    # Фамилия пациента
            ('NAME',       'C', 30),    # Имя пациента
            ('S_NAME',     'C', 30),    # Отчество пациента
            ('BIRTHDAY',   'D'),        # Дата рождения
            ('SEX',        'C',  1),    # Пол (М/Ж)
            ('ID_PAT_CAT', 'N',  2, 0), # Статус
            ('DOC_TYPE',   'N',  2, 0), # Тип документа
            ('SER_L',      'C', 6),     # Серия документа, левая часть
            ('SER_R',      'C', 6),     # Серия документа, левая часть
            ('DOC_NUMBER', 'C', 12),    # Номер документа
            ('ISSUE_DATE', 'D'),        # Дата выдачи документа
            ('DOCORG',     'M'),        # Наименование органа, выдавшего документ, удостоверяющий личность
            ('SNILS',      'C', 14),    # СНИЛС
            ('C_OKSM',     'C',  3),    # Гражданство
            ('IS_SMP',     'L'),        # Признак "пациент СМП"
            ('POLIS_TYPE', 'C', 1),     # Тип полиса
            ('POLIS_S',    'C', 20),    # Серия полиса
            ('POLIS_N',    'C', 20),    # Номер полиса
            ('ID_SMO',     'N',  3, 0), # СМО
            ('POLIS_BD',   'D'),        # Дата начала действия полиса
            ('POLIS_ED',   'D'),        # Дата окончания действия полиса
            ('ID_SMO_REG', 'N',  4, 0), # Региональная СМО (для иногородних)
            ('ADDR_TYPE',  'C',  1),    # Тип адреса
            ('IDOKATOREG', 'N',  3, 0), # Регион
            ('IDOBLTOWN',  'N',  4, 0), # - не используется
            ('ID_PREFIX',  'N',  4, 0), # - не используется
            ('ID_HOUSE',   'N',  8, 0), # Идентификатор дома (для адресов СПб, тип "г")
            ('HOUSE',      'C', 10),    # Номер дома (для типа "р")
            ('KORPUS',     'C',  5),    # Корпус (для типа "р")
            ('FLAT',       'C',  5),    # Квартира
            ('U_ADDRESS',  'C',200),    # Неструктурированный адрес (для типа "п")
            ('KLADR_CODE', 'C', 13),    # Код КЛАДР (для типа "р")
            ('STREET',     'C',150),    # Название улицы (для типа "р")
            ('IDSTRTYPE',  'N',  2, 0), # Тип улицы (для типа "р")
            ('ADDRTYPE_L', 'C',  1),    # Тип адреса
            ('OKATOREG_L', 'N',  3, 0), # Регион
            ('OBLTOWN_L',  'N',  4, 0), # - не используется
            ('PREFIX_L',   'N',  4, 0), # - не используется
            ('ID_HOUSE_L', 'N',  8, 0), # Идентификатор дома (для адресов СПб, тип "г")
            ('HOUSE_L',    'C', 10),    # Номер дома (для типа "р")
            ('KORPUS_L',   'C',  5),    # Корпус (для типа "р")
            ('FLAT_L',     'C',  5),    # Квартира
            ('U_ADDR_L',   'C',200),    # Неструктурированный адрес (для типа "п")
            ('KLADR_L',    'C', 13),    # Код КЛАДР (для типа "р")
            ('STREET_L',   'C',150),    # Название улицы (для типа "р")
            ('STRTYPE_L',  'N',  2, 0), # Тип улицы (для типа "р")
            ('PLACE_WORK', 'C',254),    # Место работы
            ('ADDR_WORK',  'C',254),    # Адрес места работы
            ('ADDR_PLACE', 'C',254),    # Место взятия
            ('REMARK',     'C',254),    # Примечение
            ('B_PLACE',    'C',100),    # Место рождения
            ('VNOV_D',     'N',  4, 0), # Вес при рождении
            ('ID_G_TYPE',  'N',  2, 0), # Тип представителя
            ('G_SURNAME',  'C', 30),    # Фамилия
            ('G_NAME',     'C', 25),    # Имя
            ('G_S_NAME',   'C', 25),    # Отчество
            ('G_BIRTHDAY', 'D'),        # Дата рождения
            ('G_SEX',      'C',  1),    # Пол
            ('G_DOC_TYPE', 'N',  2, 0), # Тип документа
            ('G_SERIA_L',  'C',  6),    # Левая часть серии документа
            ('G_SERIA_R',  'C',  2),    # Правая часть серии документа
            ('G_DOC_NUM',  'C', 12),    # Номер документа
            ('G_ISSUE_D',  'D'),        # Дата выдачи документа представителя пациента
            ('G_DOCORG',   'M'),        # Наименование органа, выдавшего документ, удостоверяющий личность представителя пациента   макс. 1000 символов
            ('G_B_PLACE',  'C',100),    # Место рождения
            ('N_BORN',     'N',  1, 0), # Порядковый номер новорожденного
            ('SEND',       'L'),        # Признак принят (true/false), default - false
            ('ID_MIS',     'C', 20),    # Идентификатор пациента из внешних данных
            ('ID_PATIENT', 'C', 20),    # Идентификатор записи пациента в БД ЕИС (проставляется после принятия)
            ('LGOTS',      'C', 20),    # Льготы пациента (список ID через запятую)
            ('ERROR',      'C',200),    # Описание ошибки
            # 1234567890 - максимум - 10 символов
        )
        return dbf


    def createOnkoAddDbf(self):
        # Формат файла импорта доп. данных случая (онкология) (файл *_ONKO_ADD.DBF)
        dbf = Dbf(self.wizard().getFullDbfFileName('_ONKO_ADD'), new=True, encoding='cp866')
        dbf.addField(
            # 1234567890 - максимум - 10 символов
            ('SERV_ID',    'N', 11, 0), # Идентификатор случая лечения в основном файле импорта услуг
            ('ID_DIAGNOS', 'N', 11, 0), # Идентификатор диагноза (основной или сопутствующий случая)
            ('DS1_T',      'N',  6, 0), # Повод обращения
            ('ID_ST',      'N', 11, 0), # Стадия заболевания
            ('ID_T',       'N', 11, 0), # Значение Tumor
            ('ID_N',       'N', 11, 0), # Значение Nodus
            ('ID_M',       'N', 11, 0), # Значение Metastasis
            ('MTSTZ',      'N',  6, 0), # Признак выявления отдалённых метастазов
            ('SOD',        'N', 10, 2), # Суммарная очаговая доза
            ('K_FR',       'N',  2, 0), # Количество фракций проведения лучевой терапии
            ('WEI',        'N',  5, 1), # Масса тела (кг)
            ('HEI',        'N',  3, 0), # Рост (см)
            ('BSA',        'N',  4, 2), # Площадь поверхности тела (м2)
            ('ID_MKB_O_T', 'N', 11, 0), # Топографический код диагноза (ID)
            ('ID_MKB_O_M', 'N', 11, 0), # Морфологический код диагноза (ID)
            ('ERROR',      'C',200   ), # Описание ошибки
            # наши поля
            ('DIAGNSTCID', 'N', 11, 0), #
            ('DIAG',       'C',  5   ), # Ненавижу ID_DIAGNOS и ID_MKB_O_T!
            ('MORPHOLOGY', 'C',  6   ), # Ненавижу ID_MKB_O_M!
            # 1234567890 - максимум - 10 символов
        )
        return dbf


    def createOnkoServDbf(self):
        # Формат файла импорта доп. данных по услугам (онкология) (файл *_ONKO_V.DBF)
        dbf = Dbf(self.wizard().getFullDbfFileName('_ONKO_V'), new=True, encoding='cp866')
        dbf.addField(
            # 1234567890 - максимум - 10 символов
            ('SERV_ID',    'N', 11, 0), # Идентификатор случая лечения в основном файле импорта услуг
            ('ID_IN_CASE', 'N',  3, 0), # Порядковый номер услуги (записи) в рамках одного SERV_ID
            ('ID_REC',     'N',  3, 0), # Порядковый номер записи в рамках одного SERV_ID и ID_IN_CASE
            ('DATE_BEGIN', 'D'),        # Дата начала
            ('DATE_END',   'D'),        # Дата окончания
            ('ID_PRVS',    'N', 11,0),  # Идентификатор специальности врача
            ('ID_DOC',     'C', 20),    # Идентификатор врача (для услуги)
            ('PR_CONS',    'N',  6,0),  # Сведения о проведении консилиума
            ('ID_TLECH',   'N',  6,0),  # Тип услуги
            ('ID_THIR',    'N',  6,0),  # Тип хирургического лечения
            ('ID_TLEK_L',  'N',  6,0),  # Линия лекарственной терапии
            ('ID_TLEK_V',  'N',  6,0),  # Цикл лекарственной терапии
            ('ID_TLUCH',   'N',  6,0),  # Тип лучевой терапии
            ('ID_DRUG_SH', 'N', 11,0),  # Код схемы лекарственной терапии
            ('NOTFULLDSH', 'N',  1,0),  # Признак: схема лекарственной терапии проведена не полностью
            ('PPTR',       'N',  1,0),  # Признак проведения профилактики тошноты и рвотного рефлекса
            ('ID_NMKL',    'N', 11,0),  # Идентификатор номенклатуры
            ('ERROR',      'C',  200),  # Описание ошибки
            # 1234567890 - максимум - 10 символов
        )
        return dbf


    def createOnkoDiagnosticsDbf(self):
        # Формат файла импорта данных диагностического блока (файл *_ONKO_MT.DBF)
        dbf = Dbf(self.wizard().getFullDbfFileName('_ONKO_MT'), new=True, encoding='cp866')
        dbf.addField(
            # 1234567890 - максимум - 10 символов
            ('SERV_ID',    'N', 11, 0), # Идентификатор случая лечения в основном файле импорта услуг
            ('DIAG_TIP',   'N', 11, 0), # Тип диагностического показателя
            ('ID_MRF',     'N', 11, 0), # Код диагностического показателя (гистология)
            ('ID_IGH',     'N', 11, 0), # Код диагностического показателя (иммунногистохимия)
            ('ID_R_M',     'N', 11, 0), # Код результата диагностики (гистология)
            ('ID_R_I',     'N', 11, 0), # Код результата диагностики (иммунногистохимия)
            ('TEST_DATE',  'D'),        # Дата взятия материала Пусто
            ('ID_MTEST',   'N', 11,0),  # Код диагностического показателя   Обязательное для DIAG_TIP > 0
            ('ID_MTRSLT',  'N', 11,0),  # Код результата диагностики    Обязательное для DIAG_TIP > 0
            ('REC_RSLT',   'N',  1,0),  # Признак получения результата диагностики  Пусто
            ('ERROR',      'C',  200),  # Описание ошибки
            # 1234567890 - максимум - 10 символов
        )
        return dbf


    def createOnkoConsiliumDbf(self):
        # Формат файла импорта сведения о проведении консилиума (файл *_ONKO_CONS.DBF)
        dbf = Dbf(self.wizard().getFullDbfFileName('_ONKO_CONS'), new=True, encoding='cp866')
        dbf.addField(
            # 1234567890 - максимум - 10 символов
            ('SERV_ID',    'N', 11, 0), # Идентификатор случая лечения в основном файле импорта услуг
            ('ID_PR_CONS', 'N', 11, 0), # Идентификатор цели проведения консилиума, Обязательное
            ('DATE_CONS',  'D'),        # Дата проведения консилиума Обязательно  заполнению, если PR_CONS не равен 0
            ('ERROR',      'C',  200),  # Описание ошибки
            # 1234567890 - максимум - 10 символов
        )
        return dbf


    def createOnkoDrugsDbf(self):
        # Формат файла импорта сведения о введенном противоопухолевом лекарственном препарате (файл *_ONKO_LEK.DBF)
        dbf = Dbf(self.wizard().getFullDbfFileName('_ONKO_LEK'), new=True, encoding='cp866')
        dbf.addField(
            # 1234567890 - максимум - 10 символов
            ('SERV_ID',    'N', 11, 0), # Идентификатор случая лечения в основном файле импорта услуг
            ('ID_IN_CASE', 'N',  3, 0), # Порядковый номер услуги (записи) в рамках одного SERV_ID
            ('ID_REC',     'N',  3, 0), # Порядковый номер записи в рамках одного SERV_ID и ID_IN_CASE
            ('ID_LEK_PR',  'N', 11, 0), # Идентификатор лекарственного препарата
            ('DATE_INJ',   'D'),        # Дата введения лекарственного препарата
            ('ERROR',      'C',  200),  # Описание ошибки
            # 1234567890 - максимум - 10 символов
        )
        return dbf


    def createCovidAddDbf(self):
        # Формат файла импорта доп. данных случая (ковид) (файл *_COVID_ADD.DBF)
        dbf = Dbf(self.wizard().getFullDbfFileName('_COVID_ADD'), new=True, encoding='cp866')
        dbf.addField(
            # 1234567890 - максимум - 10 символов
            ('SERV_ID',    'N', 11, 0), # Идентификатор случая лечения в основном файле импорта услуг
            ('WEI',        'N',  5, 1), # Масса тела (кг)
            ('IDSEVERITY', 'N', 11, 0), # Степень тяжести состояния пациента
            ('ERROR',      'C',  200),  # Описание ошибки
            # 1234567890 - максимум - 10 символов
        )
        return dbf


    def createCovidDrugsDbf(self):
        # Формат файла импорта сведения о введенном лекарственном препарате (ковид) (файл *_COVID_LEK.DBF)
        dbf = Dbf(self.wizard().getFullDbfFileName('_COVID_LEK'), new=True, encoding='cp866')
        dbf.addField(
            # 1234567890 - максимум - 10 символов
            ('SERV_ID',    'N', 11, 0), # Идентификатор случая лечения в основном файле импорта услуг
            ('ID_IN_CASE', 'N',  3, 0), # Порядковый номер услуги (записи) в рамках одного SERV_ID (из основного файла импорта услуг)
            ('ID_DRUG_SH', 'N', 11, 0), # Идентификатор кода схемы лекарственной терапии
            ('NOTFULLDSH', 'N',  1, 0), # Признак - схема лекарственной терапии проведена не полностью (1)
            ('DATE_INJ',   'D'),        # Дата введения лекарственного препарата
            ('ID_LEK_PR',  'N', 11, 0), # Идентификатор лекарственного препарата
            ('COD_MARK',   'C', 100),   # Код маркировки лекарственного препарата
            ('ID_ED_IZM',  'N', 11 ,0), # Идентификатор единицы измерения дозы лекарственного препарата
            ('DOSE_INJ',   'N',  8, 2), # Доза введения лекарственного препарата
            ('ID_MET_INJ', 'N', 11, 0), # Идентификато пути введения лекарственного препарата
            ('COL_INJ',    'N',  5, 0), # Количество введений
            ('ERROR',      'C', 200),   # Описание ошибки
            ('#Nomen_Id',  'N', 11, 0),
            ('#Unit_Id',   'N', 11, 0),
            ('#Route_Id',  'N', 11, 0),
            # 1234567890 - максимум - 10 символов
        )
        return dbf


    def createMedDevDbf(self):
        # Формат файла импорта сведения о медицинских изделиях, имплантируемых в организм человека (файл *_MED_DEV.DBF)
        dbf = Dbf(self.wizard().getFullDbfFileName('_MED_DEV'), new=True, encoding='cp866')
        dbf.addField(
            # 1234567890 - максимум - 10 символов
            ('SERV_ID',    'N', 11, 0), # Идентификатор случая лечения в основном файле импорта услуг
            ('ID_IN_CASE', 'N',  3, 0), # Порядковый номер услуги (записи) в рамках одного SERV_ID
            ('ID_REC',     'N',  3, 0), # Порядковый номер записи в рамках одного SERV_ID и ID_IN_CASE (из файла *_ONKO_V.DBF)
            ('IDDATAOBJ',  'N', 11, 0), # Тип записи: 5 - ссылка на файл  *_ONKO_V.DBF, 3 - ссылка на основной файл услуг
            ('DATE_MED',   'D'),        # Дата установки медицинского изделияа
            ('ID_MED_DEV', 'N', 11, 0), # Идентификатор кода вида медицинского изделия
            ('NUM_SER',    'C',  100),  # Серийный номер
            ('ERROR',      'C',  200),  # Описание ошибки
            # 1234567890 - максимум - 10 символов
        )
        return dbf


    def createQuery(self, ignoreConfirmation, includeEvents, includeVisits, includeActions):
        db = QtGui.qApp.db

        if includeEvents and includeVisits and includeActions:
            includeCond = '1'
        else:
            includeCondList = []
            if includeEvents:
                includeCondList.append('Account_Item.visit_id IS NULL AND Account_Item.action_id IS NULL')
            if includeVisits:
                includeCondList.append('Account_Item.visit_id IS NOT NULL AND Account_Item.action_id IS NULL')
            if includeActions:
                includeCondList.append('Account_Item.visit_id IS NULL AND Account_Item.action_id IS NOT NULL')
            if includeCondList:
                includeCond = db.joinOr(includeCondList)
            else:
                includeCond = '0'

        db = QtGui.qApp.db
        tableAccountItem = db.table('Account_Item')
        stmt = """
            SELECT
              Account_Item.id        AS accountItem_id,
              Account_Item.master_id AS account_id,
              Account_Item.event_id  AS event_id,
              Event.eventType_id     AS eventType_id,
              Event.prevEvent_id     AS prevEvent_id,
              Account_Item.visit_id  AS visit_id,
              Account_Item.action_id AS action_id,
              Event.client_id        AS client_id,
              Event.order            AS eventOrder,
              Event.externalId       AS externalId,
              Event.MES_id           AS MES_id,
              rbMesSpecification.level = 2 AS mesIsDone,
              Event.setDate          AS setDate,
              Event.execDate         AS execDate,
              rbEventTypePurpose.code AS eventTypePurposeCode,
              EventType.serviceReason AS serviceReason,
              EventType.form         AS eventForm,
              rbMedicalAidKind.regionalCode  AS medicalAidKindCode,
              rbMedicalAidType.code  AS medicalAidTypeCode,
              Client.lastName        AS lastName,
              Client.firstName       AS firstName,
              Client.patrName        AS patrName,
              Client.birthDate       AS birthDate,
              Client.sex             AS sex,
              Client.SNILS           AS SNILS,
              Client.birthPlace      AS birthPlace,
              ClientPolicy.serial    AS policySerial,
              ClientPolicy.number    AS policyNumber,
              ClientPolicy.begDate   AS policyBegDate,
              ClientPolicy.endDate   AS policyEndDate,
#              (SELECT COUNT(DISTINCT CP.client_id)
#               FROM ClientPolicy AS CP
#               WHERE CP.deleted = 0
#                 AND CP.client_id != Client.id
#                 AND CP.serial = ClientPolicy.serial
#                 AND CP.number = ClientPolicy.number
##                 AND CP.begDate = ClientPolicy.begDate
#              ) != 0 AS policyIsVicarious,
              EXISTS(SELECT NULL
                     FROM ClientPolicy AS CP
                     WHERE CP.deleted = 0
                       AND CP.serial = ClientPolicy.serial
                       AND CP.number = ClientPolicy.number
#                      AND CP.begDate = ClientPolicy.begDate
                       AND (   EXISTS(SELECT NULL FROM ClientRelation
                                      INNER JOIN rbRelationType ON rbRelationType.id = ClientRelation.relativeType_id
                                      WHERE ClientRelation.client_id = Client.id
                                        AND ClientRelation.relative_id = CP.client_id
                                        AND ClientRelation.deleted = 0
                                        AND rbRelationType.isBackwardRepresentative
                                     )
                            OR EXISTS(SELECT NULL FROM ClientRelation
                                      INNER JOIN rbRelationType ON rbRelationType.id = ClientRelation.relativeType_id
                                      WHERE ClientRelation.client_id = CP.client_id
                                        AND ClientRelation.relative_id = Client.id
                                        AND ClientRelation.deleted = 0
                                        AND rbRelationType.isDirectRepresentative
                                     )
                     )
              ) AS policyIsVicarious,
              rbPolicyKind.regionalCode AS policyKindRegionalCode,
              Insurer.infisCode      AS policyInsurer,
              Insurer.tfomsExtCode   AS tfomsExtCode,
              Insurer.area           AS insurerArea,
              ClientDocument.serial  AS documentSerial,
              ClientDocument.number  AS documentNumber,
              ClientDocument.date    AS documentDate,
              ClientDocument.origin  AS documentOrigin,
              getClientCitizenship(Client.id, Event.setDate) as citizenship,
              rbDocumentType.code    AS documentType,
              rbDocumentType.regionalCode AS documentRegionalCode,
              IFNULL(rbItemService.id, rbVisitService.id) AS service_id,
              VisitDiagnosis.MKB     AS visitDiag,
              VisitDiagnostic.character_id AS visitDiseaseCharacter_id,
              Action.MKB             AS actionDiag,
              Action.actionType_id   AS actionType_id,
              NULL                   AS actionDiseaseCharacter_id,
              EventDiagnosis.MKB     AS eventDiag,
              rbEventDispanser.observed AS eventDispanserObserved,
              EventDiagnostic.character_id AS eventDiseaseCharacter_id,
              CASE ActionType.exposeDateSelector
                  WHEN 0 THEN Action.begDate
                  WHEN 1 THEN Action.begDate
                  WHEN 2 THEN Action.directionDate
                  WHEN 3 THEN TakenTissueJournal.datetimeTaken
                  ELSE Action.begDate
              END                    AS actionBegDate,
              ActionType.serviceType AS actionServiceType,
              Account_Item.serviceDate AS date,
              Account_Item.amount    AS amount,
              rbEventDiagnosticResult.regionalCode AS eventDiagnosticResultCode,
              rbVisitDiagnosticResult.regionalCode AS visitDiagnosticResultCode,
              EventResult.regionalCode AS eventResultCode,
              Event.execPerson_id AS eventPerson_id,
              EventPerson.speciality_id AS eventSpeciality_id,
              rbEventSpeciality.regionalCode AS eventSpecialityCode,
              rbActionSetPersonSpeciality.regionalCode AS actionSetPersonSpecialityCode,
              Contract_Tariff.tariffType AS tariffType,
              rbMedicalAidUnit.regionalCode AS unitCode,
              IF(Account_Item.visit_id IS NOT NULL, VisitPerson.id,
                 IF( Account_Item.action_id IS NOT NULL, ActionPerson.id, EventPerson.id)
                ) AS person_id,
              rbSpeciality.id        AS speciality_id,
              rbSpeciality.regionalCode AS specialityCode,
              rbVisitType.code       AS visitTypeCode,
              Event.relegateOrg_id   AS eventRelegateOrg_id,
              rbRelegateSpeciality.regionalCode AS relegateSpecialityCode,
              Event.srcNumber,
              Event.srcDate,
              EXISTS(
                select NULL from Action as A
                    LEFT JOIN ActionType as AT on AT.id = A.actionType_id
                    WHERE
                        A.event_id = Event.id
                        AND AT.flatCode = 'moving'
                        AND A.deleted = 0
                    LIMIT 1
                ) as 'haveMoving',
            Contract.financeSubtypeCode
            FROM Account_Item
            LEFT JOIN Account ON Account.id = Account_Item.master_id
            LEFT JOIN Contract ON Contract.id = Account.contract_id
            LEFT JOIN rbFinance ON rbFinance.id = Contract.finance_id
            LEFT JOIN Action ON Action.id = Account_Item.action_id
            LEFT JOIN Visit  ON Visit.id  = Account_Item.visit_id
            LEFT JOIN rbVisitType ON rbVisitType.id = Visit.visitType_id
            LEFT JOIN Event  ON Event.id  = Account_Item.event_id
            LEFT JOIN EventType ON EventType.id  = Event.eventType_id
            LEFT JOIN rbEventTypePurpose ON rbEventTypePurpose.id = EventType.purpose_id
            LEFT JOIN rbMedicalAidKind ON rbMedicalAidKind.id = EventType.medicalAidKind_id
            LEFT JOIN rbMedicalAidType ON rbMedicalAidType.id = EventType.medicalAidType_id
            LEFT JOIN Client ON Client.id = Event.client_id
            LEFT JOIN ClientPolicy ON ClientPolicy.id = getClientPolicyIdForDate(Client.id, rbFinance.code != '3', Account_Item.serviceDate)
            LEFT JOIN rbPolicyKind ON rbPolicyKind.id = ClientPolicy.policyKind_id
            LEFT JOIN Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
            LEFT JOIN ClientDocument ON
                ClientDocument.client_id = Client.id AND
                ClientDocument.id = (
                    SELECT MAX(CD.id)
                    FROM   ClientDocument AS CD
                    LEFT JOIN rbDocumentType AS rbDT ON rbDT.id = CD.documentType_id
                    LEFT JOIN rbDocumentTypeGroup AS rbDTG ON rbDTG.id = rbDT.group_id
                    WHERE  rbDTG.code = '1' AND CD.deleted=0 AND CD.client_id = Client.id)
            LEFT JOIN rbDocumentType ON rbDocumentType.id = ClientDocument.documentType_id
            LEFT JOIN Person AS VisitPerson     ON VisitPerson.id  = Visit.person_id
            LEFT JOIN Person AS ActionPerson    ON ActionPerson.id = Action.person_id
            LEFT JOIN Person AS ActionSetPerson ON ActionSetPerson.id = Action.setPerson_id
            LEFT JOIN Person AS EventPerson  ON EventPerson.id  = Event.execPerson_id
            LEFT JOIN rbSpeciality ON rbSpeciality.id = IF(Account_Item.visit_id IS NOT NULL, VisitPerson.speciality_id,
                                               IF( Account_Item.action_id IS NOT NULL, ActionPerson.speciality_id, EventPerson.speciality_id))
            LEFT JOIN rbSpeciality AS rbEventSpeciality ON rbEventSpeciality.id = EventPerson.speciality_id
            LEFT JOIN rbSpeciality AS rbActionSetPersonSpeciality ON rbActionSetPersonSpeciality.id = ActionSetPerson.speciality_id
            LEFT JOIN Diagnostic         AS VisitDiagnostic         ON VisitDiagnostic.id = getEventPersonDiagnostic(Account_Item.event_id, Visit.person_id)
            LEFT JOIN Diagnosis          AS VisitDiagnosis          ON VisitDiagnosis.id = VisitDiagnostic.diagnosis_id
            LEFT JOIN rbDiagnosticResult AS rbVisitDiagnosticResult ON rbVisitDiagnosticResult.id=VisitDiagnostic.result_id
            LEFT JOIN Diagnostic         AS EventDiagnostic         ON EventDiagnostic.id = getEventDiagnostic(Account_Item.event_id)
            LEFT JOIN Diagnosis          AS EventDiagnosis          ON EventDiagnosis.id = EventDiagnostic.diagnosis_id
            LEFT JOIN rbDispanser        AS rbEventDispanser        ON rbEventDispanser.id = EventDiagnostic.dispanser_id
            LEFT JOIN rbDiagnosticResult AS rbEventDiagnosticResult ON rbEventDiagnosticResult.id=EventDiagnostic.result_id
            LEFT JOIN rbResult           AS EventResult             ON EventResult.id=Event.result_id
            LEFT JOIN rbService          AS rbVisitService          ON rbVisitService.id = Visit.service_id
            LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
            LEFT JOIN rbService AS rbItemService ON rbItemService.id = Account_Item.service_id
            LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
            LEFT JOIN Contract_Tariff ON Contract_Tariff.id = Account_Item.tariff_id
            LEFT JOIN rbMedicalAidUnit ON rbMedicalAidUnit.id = Contract_Tariff.unit_id
            LEFT JOIN rbMesSpecification ON rbMesSpecification.id = Event.mesSpecification_id
            LEFT JOIN TakenTissueJournal ON TakenTissueJournal.id = Action.takenTissueJournal_id
            LEFT JOIN Person AS RelegatePerson ON RelegatePerson.id = Event.relegatePerson_id
            LEFT JOIN rbSpeciality AS rbRelegateSpeciality ON rbRelegateSpeciality.id = RelegatePerson.speciality_id
            WHERE
                (Account_Item.visit_id IS NOT NULL
                 OR rbItemService.eisLegacy
                 OR (Account_Item.event_id IS NOT NULL AND Event.MES_id IS NOT NULL)
                )
            AND Account_Item.reexposeItem_id IS NULL
            AND ( %d
                 OR Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s
            AND %s
            ORDER BY Client.id, Event.id, Account_Item.serviceDate
        """ % ((1 if ignoreConfirmation else 0), includeCond, tableAccountItem['id'].inlist(self.idList))
        query = db.query(stmt)
        return query


    def getAddrRecord(self, clientId, addrType):
        db = QtGui.qApp.db
        stmt = '''
            SELECT
                kladr.STREET.NAME AS streetName, kladr.STREET.SOCR AS streetType,
                AddressHouse.number AS number, AddressHouse.corpus AS corpus, AddressHouse.KLADRCode, AddressHouse.KLADRStreetCode,
                Address.flat AS flat, Address.id AS addressId, ClientAddress.freeInput AS freeInput
            FROM ClientAddress
            LEFT JOIN Address ON Address.id = ClientAddress.address_id
            LEFT JOIN AddressHouse ON AddressHouse.id = Address.house_id
            LEFT JOIN kladr.STREET ON kladr.STREET.CODE = AddressHouse.KLADRStreetCode
            WHERE
                ClientAddress.client_id = %d AND
                ClientAddress.id = (
                    SELECT MAX(CA.id)
                    FROM ClientAddress AS CA
                    WHERE  CA.type = %d AND CA.client_id = %d)
        ''' % (clientId, addrType, clientId)
        query = db.query(stmt)
        if query.next():
            return query.record()
        else:
            return None


    def getAreaAndRegion(self, clientId, addrType):
        clientAddressRecord = getClientAddress(clientId, addrType)
        if clientAddressRecord:
            address = getAddress(clientAddressRecord.value('address_id'))
            area, region, npunkt, street, streetType = getInfisCodes(
                address.KLADRCode, address.KLADRStreetCode,
                address.number, address.corpus)
            return area, region
        return '', ''


    def process(self, record):
        accountId = forceInt(record.value('account_id'))
        accountItemId = forceInt(record.value('accountItem_id'))
        eventId  = forceRef(record.value('event_id'))
        actionId = forceRef(record.value('action_id'))
        visitId  = forceRef(record.value('visit_id'))
        serviceId = forceRef(record.value('service_id'))
        serviceDetail = self.serviceDetailCache.get(serviceId)
        eventExternalId = forceString(record.value('externalId'))
        eventSpecialityCode = forceInt(record.value('eventSpecialityCode'))
        if not eventId in self.caseRegistry:
            self.caseRegistry[eventId] = (eventSpecialityCode, [])
        eventTypePurposeCode = forceString(record.value('eventTypePurposeCode'))
        eventTypeAidKindCode = forceString(record.value('medicalAidKindCode'))
        eventTypeAidTypeCode = forceString(record.value('medicalAidTypeCode'))
        actionSetPersonSpecialityCode = forceInt(record.value('actionSetPersonSpecialityCode'))
        prevEventId = forceRef(record.value('prevEvent_id'))
        clientId  = forceInt(record.value('client_id'))
        lastName  = nameCase(forceString(record.value('lastName')))
        firstName = nameCase(forceString(record.value('firstName')))
        patrName  = nameCase(forceString(record.value('patrName')))
        birthDate = forceDate(record.value('birthDate'))
        date = forceDate(record.value('date'))
        dateIn = forceDate(record.value('setDate'))
#        ageInDays = calcAgeInDays(birthDate, date)
        ageInMonths = calcAgeInMonths(birthDate, date)
        age = calcAgeInYears(birthDate, dateIn)
        sex = forceInt(record.value('sex'))
        documentType = self.getDocumentType(forceInt(record.value('documentRegionalCode')),
                                            forceString(record.value('documentType'))
                                           )
        documentSerial=forceStringEx(record.value('documentSerial'))
        documentSeries=self.parseDocumentSerial(documentSerial)
        documentNumber = forceString(record.value('documentNumber')) or '-'
        citizenship = filter(lambda c: c.isdigit(),
                             forceString(record.value('citizenship'))) or '643'

        eventOrder = forceInt(record.value('eventOrder'))
        order = self.mapEventOrderToEIS.get(eventOrder) or self.mapEventOrderToEIS.get(None)
        forPom = self.mapEventOrderToForPom.get(eventOrder) or self.mapEventOrderToForPom.get(None)
        transf = self.mapEventOrderToTransf.get(eventOrder) or self.mapEventOrderToTransf.get(None)
        policySerial = forceString(record.value('policySerial'))
        policyNumber = forceString(record.value('policyNumber'))
        policyBegDate = forceDate(record.value('policyBegDate'))
        if not policyBegDate:
#            policyBegDate = max(QDate(1900, 1, 1), firstYearDay(date))
            policyBegDate = QDate(1900, 1, 1)
        policyEndDate = forceDate(record.value('policyEndDate'))
        if not policyEndDate:
            policyEndDate = QDate(2200, 1, 1)
        policyIsVicarious = forceBool(record.value('policyIsVicarious'))
        policyInsurer = forceString(record.value('policyInsurer'))
        insurerArea = forceString(record.value('insurerArea'))
        tfomsExtCode = forceInt(record.value('tfomsExtCode'))
        snils = formatSNILS(forceString(record.value('SNILS')))
        eventHaveMoving = forceBool(record.value('haveMoving'))
        finType = forceInt(getIdentification('rbService',
                                             serviceId,
                                             'urn:tfoms78:SPRAV_FIN_TYPE',
                                             False))
        if not finType:
            finType = forceInt(record.value('financeSubtypeCode'))
        if not finType:
            if eventTypeAidTypeCode in ('4','5'):
                if not insurerArea or insurerArea.startswith('78'):
                    finType = 4
                else:
                    finType = 1
            else:
                finType = 1

        street = ''
        streetType = ''
        area = ''
        house = ''
        corpus = ''
        flat = ''
        longAddress = ''
        addrRecord = self.getAddrRecord(clientId, 0)
        addrType = 0
        if not addrRecord:
            addrRecord = self.getAddrRecord(clientId, 1)
            addrType = 1
        if addrRecord:
            KLADRCode=forceString(addrRecord.value('KLADRCode'))
            area, region = self.getAreaAndRegion(clientId, addrType)
            if KLADRCode.startswith('78'):
                street = forceString(addrRecord.value('streetName')) # Адрес пациента: код улицы
                streetType = forceString(addrRecord.value('streetType')) # Адрес пациента: тип улицы
                house = forceString(addrRecord.value('number')) # Адрес пациента: номер дома
                corpus  = forceString(addrRecord.value('corpus')) # Адрес пациента: корпус
                flat = forceString(addrRecord.value('flat'))   # Адрес пациента: номер квартиры
            else:
                street = '*'
            addressId = forceInt(addrRecord.value('addressId'))
            longAddress = formatAddress(addressId)

#        if citizenship == '643' and age<1 and documentType not in self.childrenDocTypes: # мелкий и документ - не детский, предположительно - родительский
#            # сбрасываем документ
#            documentType = 5
#            documentNumber = '-'
#            documentSeries = ['-', '-']
#            # устанавливаем отметку "новорожденный"
#            newbornId = self.getNewbornId(clientId)
#        else:
#            newbornId = 0

#        newbornId = self.mapClientIdToNewbornId.get(clientId)
#        if newbornId is not None:
#            pass
#        elif ageInMonths>=3 or (policyNumber and birthDate < policyBegDate <= date):
        if ageInMonths>=4 or (policyNumber and birthDate < policyBegDate and not policyIsVicarious):
            newbornId = 0
        else:
            newbornId = self.getNewbornId(clientId)

        patCat = 0
#        if age<1 and documentType!=3: # мелкий и документ - не свидетельство о рождении
        if newbornId:
            patCat = 9
        elif age<7:
            patCat = 10
        elif age<14:
            patCat = 11
        elif age<18:
#            isStudent = clientIsStudent(clientId)
#            if isStudent:
#                patCat = 12
            patCat = 12
        else:
            isStudent = clientIsStudent(clientId)
            if isStudent:
                patCat = 12
            else:
                isPens = (age>=60 and sex==1) or (age>=55 and sex !=1)
                patCat = (4 if clientIsWorking(clientId) else 6) + (1 if isPens else 0)
        profileNet = u'в' if age>=18 else u'д'
        amount = forceDouble(record.value('amount'))
        actionDiag = forceString(record.value('actionDiag'))
        visitDiag = forceString(record.value('visitDiag'))
        eventDiag = forceString(record.value('eventDiag'))
        actionTypeId = forceRef(record.value('actionType_id'))

        # 0011976: ТФОМС СПб. Изменения правил формирования значения IDVIDVM
        # 1 - Если услуга была сформирована в счет из Действия,
        #     у которого на вкладке Идентификация указано значение по справочнику с urn «urn:tfoms78:SPRAV_NMKL»,
        #     выгружаем в поле IDVIDVME то значение, которое указано в идентификации типа Действия (0010662)
        # 2 - Если протарифицированная услуга имеет идентификацию по справочнику с urn «urn:tfoms78:SPRAV_NMKL_PROFILE»
        #     (rbService_Identification.system_id --> rbAccountingSystem.urn = 'urn:tfoms78:SPRAV_NMKL_PROFILE'),
        #     выгружаем в поле IDVIDVME то значение, которое указано в идентификации данной услуги
        #     (rbService_Identification.value) (для всех строк, в которых указана эта услуга)
        # 3 - В остальных случаях выгружаем 1
        medicalInterventionCode = None
        if actionTypeId:
            medicalInterventionCode = getIdentification('ActionType', actionTypeId, 'urn:tfoms78:SPRAV_NMKL', False)
            medicalInterventionCode = forceInt(medicalInterventionCode) if medicalInterventionCode else None
        if medicalInterventionCode is None:
            medicalInterventionCode = getIdentification('rbService', serviceId, 'urn:tfoms78:SPRAV_NMKL_PROFILE', False)
            medicalInterventionCode = forceInt(medicalInterventionCode) if medicalInterventionCode else None
        if medicalInterventionCode is None:
            medicalInterventionCode = 1

        diseaseCharacterId = None
#        if actionDiag:
#            diseaseCharacterId = forceRef(record.value('actionDiseaseCharacter_id'))
#        elif visitDiag:
#            diseaseCharacterId = forceRef(record.value('visitDiseaseCharacter_id'))
#        else:
#            diseaseCharacterId = forceRef(record.value('eventDiseaseCharacter_id'))
        diseaseCharacterId = forceRef(record.value('eventDiseaseCharacter_id'))
        if diseaseCharacterId:
            diseaseCharacterCode = forceInt(getIdentification('rbDiseaseCharacter', diseaseCharacterId, 'urn:tfoms78:SPRAV_C_ZAB', False))
        else:
            diseaseCharacterCode = 0


#        resultCode = forceInt(record.value('resultCode'))
        specialityId = forceRef(record.value('speciality_id'))
        specialityCode = forceInt(record.value('specialityCode'))
        personId = forceRef(record.value('person_id'))
        eventPersonId = forceRef(record.value('eventPerson_id'))
        eventSpecialityId = forceRef(record.value('eventSpeciality_id'))
        mesId = forceRef(record.value('MES_id'))
        mesIsDone = forceBool(record.value('mesIsDone'))
        tariffType = forceInt(record.value('tariffType'))
        visitTypeCode = forceString(record.value('visitTypeCode'))
        mesGroupCode = self.getMesGroupCode(mesId)

        circumstances = []
        if eventId and mesId and visitId is None and actionId is None:
            # выставление события
            if eventTypeAidTypeCode in ('1', '2', '3', '7') and not mesIsDone:
                eventIncompl = 3
            else:
                eventIncompl = 5
            if tariffType == CTariff.ttVisitsByMES:
                availabilityCounters = {}
                circumstances = getEventVisitsCircumstances(availabilityCounters, eventId, mesId)
                onlyVisitLike = mesGroupCode not in (u'ДиспанС', u'МедОсм')
                circumstances += getEventActionsCircumstances(availabilityCounters, eventId, mesId, onlyVisitLike)
                if mesGroupCode in (u'ДиспанС', u'МедОсм'):
                    circumstances += getInappropriateCircumstances(availabilityCounters, eventId, mesId)
                circumstances = filterUniqueCircumstances(circumstances,
                                                          serviceDetail.infisCode.startswith((u'И',u'и'))
                                                         )
            elif tariffType == CTariff.ttEventByMES or tariffType == CTariff.ttEventByMESLen:
                # событие по МЭС и событие по МЭС с учётом длительности
                circumstances = [CCircumstance(date, personId, specialityId, specialityCode, 0, 1, True, 0, None, 1, eventIncompl, self.currentOrgId)]
            else:
                circumstances = [CCircumstance(date, personId, specialityId, specialityCode, 0, 0, True, 0, None, 1, eventIncompl, self.currentOrgId)]
            amount = 1
        elif visitId is not None and tariffType == CTariff.ttCoupleVisits:
            circumstances = getVisitsFromEventWithSameSevrice(eventId, serviceId)
        else:
            # выставление визита или действия
            circumstances = [CCircumstance(date, personId, specialityId, specialityCode, 0, 0, True, 0, actionId, 1, 5, self.currentOrgId)]

        eventAidProfileCode, eventAidKindCode, eventAidTypeCode, eventAidProfileId = self.getAidCodesAndProfileId(serviceDetail, dateIn, eventSpecialityId, birthDate, sex, eventDiag)
        eventRelegateOrgId      = forceRef(record.value('eventRelegateOrg_id'))
        eventRelegateOrOwnOrgId = eventRelegateOrgId or self.currentOrgId
        eventTypeId = forceRef(record.value('eventType_id'))

        for date, personId, specialityId, specialityCode, prvsTypeId, prvsGroup, important, additionalServiceCode, originatedFromAction, servMade, incompl, orgId in circumstances:
#            print 'date =', date, 'personId =', personId, 'specialityId =', specialityId, 'specialityCode =', specialityCode, 'prvsTypeId =', prvsTypeId, 'prvsGroup =', prvsGroup, 'important =', important, 'additionalServiceCode =', additionalServiceCode, 'originatedFromAction =', originatedFromAction, 'servMade =', servMade, 'incompl =', incompl, 'orgId =', orgId

            serviceAidProfileCode, serviceAidKindCode, serviceAidTypeCode = self.getAidCodes(serviceDetail, dateIn, specialityId, birthDate, sex, actionDiag or eventDiag)
            aidProfileCode = serviceAidProfileCode or eventAidProfileCode
            aidKindCode = serviceAidKindCode or eventAidKindCode or eventTypeAidKindCode
            aidTypeCode = serviceAidTypeCode or eventAidTypeCode or eventTypeAidTypeCode
#            print 'mesGroupCode =', mesGroupCode, 'aidKindCode =', aidKindCode, 'serviceAidKindCode =', serviceAidKindCode, 'eventAidKindCode =', eventAidKindCode, 'eventTypeAidKindCode =', eventTypeAidKindCode
            if mesGroupCode in (u'ВосстД', u'ВосстДСТ'):
                aidKindCodeAsInt = forceInt(QVariant(eventAidKindCode or eventTypeAidKindCode))
#                print '(1) aidKindCodeAsInt=', aidKindCodeAsInt
            else:
                aidKindCodeAsInt = forceInt(QVariant(aidKindCode))
#                print '(2) aidKindCodeAsInt=', aidKindCodeAsInt

            if  (   tariffType == CTariff.ttEventByMES
                 or tariffType == CTariff.ttEventByMESLen
                 or (    eventTypeAidTypeCode == '7'  # Дневной стационар
                     and tariffType in ( CTariff.ttEventAsCoupleVisits,
                                         CTariff.ttHospitalBedDay,
                                         CTariff.ttVisitsByMES,
                                         CTariff.ttCoupleVisits
                                       )
                    )
                ):
                amountDays = forceInt(record.value('amount'))
                amount = 1
                dateIn = forceDate(record.value('setDate'))
            elif(    (   tariffType == CTariff.ttActionAmount
                      or tariffType == CTariff.ttActionUET
                     )
                 and serviceDetail.infisCode.startswith('43')
                ):
                amountDays = forceInt(record.value('amount'))
                amount = 1
                dateIn = forceDate(record.value('actionBegDate')) or date
            else:
                amountDays = 0
                dateIn = date

            spPay = forceInt(record.value('unitCode'))

            caseCast = 0
            serviceCaseCast = getIdentification('rbService',
                                                serviceId,
                                                'urn:tfoms78:SPRAV_CASE_CAST',
                                                False
                                               )
            if serviceCaseCast:
                caseCast = forceInt(serviceCaseCast)

            if not caseCast:
                caseCast = forceInt(record.value('serviceReason'))
            if not caseCast:
                if mesId and mesGroupCode in(u'ДиспанС', u'МедОсм'):
                    if prevEventId:
                        caseCast = (12 if age>=18 else 16)
                    else:
                        caseCast = (10 if age>=18 else 14)
                elif mesId and mesGroupCode == u'ПрофК':
                    caseCast = (19 if age>=18 else 20)
                elif eventTypeAidTypeCode in ('1', '2', '3'):
                    caseCast = 6 # Стационар
                    if not amountDays:
                        amountDays = 1
                elif eventTypeAidTypeCode in ('4', '5'):
                    if mesId:
                        caseCast = 18 # СМП c МЭС
                    else:
                        caseCast = 8 # СМП
                elif visitTypeCode == u'ПД': #
                    caseCast = (19 if age>=18 else 20)
                else:
                    caseCast = (2 if aidTypeCode == '7' else 0) + (1 if mesId else 0) + 1

            modifyPref = QtGui.qApp.getGlobalPreference('24') # Желчь брыжжет фонтаном...
            if caseCast == 2 and actionId and modifyPref==u'да': #0006955: Добавить в описание услуги атрибут для определения CASE_CAST
                caseCast = 1

            # 0008576: ТФОМС СПб. Изменение профиля оплаты при экспорте
            serviceCode = serviceDetail.infisCode
            if (     tariffType == CTariff.ttVisit
                 and serviceCode in (u'аТерУч', u'аВОПУч', u'аПедУч')
               ):
                if order == u'э':
                    serviceCode += u'Н'
                elif self.serviceRepetionCount(eventId, serviceCode) > 1:
                    serviceCode += u'О'

            # 0008580: ТФОМС СПб. Изменение CASE_CAST при экспорте
            if (     tariffType == CTariff.ttVisit
#                 and visitSceneCode in ('2', '3')
                 and serviceCode in (u'кТерап', u'кПедиа', u'кОбщПр')
                 and caseCast in (34, 35, 36, 37)
               ):
                caseCast = 1
            elif (   tariffType == CTariff.ttVisit
                 and serviceCode in (u'аТерУчО', u'аВОПУчО', u'аПедУчО')
                 and caseCast == 35
               ):
                caseCast = 36
                spPay = self.getCompletedTreatmentCaseUnitCode()
            # 8580, ~0019704:
            if caseCast == 39 and (policyInsurer == u'кТФ3' or not insurerArea.startswith('78')):
                caseCast = 2

            # 0010547: ТФОМС СПб. Выгрузка разных CASE_CAST из одного События
            serviceType = forceRef(record.value('actionServiceType'))
            if serviceType in (CActionServiceType.research, CActionServiceType.labResearch):
                eventTypeCaseCast = getIdentification('EventType',
                                                      eventTypeId,
                                                      'urn:tfoms78:SPRAV_CASE_CAST',
                                                      False
                                                     )
                if eventTypeCaseCast:
                    caseCast = forceInt(eventTypeCaseCast)

            ##################################################### beg of ID_GOAL
            # 0010520: ТФОМС СПб. Добавление новых значений ID_GOAL
            # 1. Если значение поля CASE_CAST соответствует 1, 2, 34, 43
            #    а также назначение Типа События имеет код 3 (Event.eventType_id --> EventType.purpose_id --> rbEventTypePurpose.code = 3),
            #    то заполняется 12.
            if (       caseCast in (1, 2, 34, 43)
                   and eventTypePurposeCode == '3'
               ):
                    goalCode = 12 # патронаж
            # 2. Если значение поля CASE_CAST соответствует 1, 2, 34, 37 или 39,
            #    а также порядок события соответствует значению "неотложная помощь",
            #    то заполняется 3.
            elif (     caseCast in (1, 2, 34, 37, 39)
                   and eventOrder in (2, 6)
                 ):
                    goalCode = 3 # Посещение в связи с оказанием неотложной помощи
            # 3. Если значение поля CASE_CAST соответствует 1, 2, 34, 35, 36, 39, 44
            #    и у заключительного (основного) диагноза События указан признак ДН (Diagnostic.dispanser_id, у которого rbDispanser.observed = 1),
            #    то заполняется 8.
            elif (     caseCast in (1, 2, 34, 35, 36, 39, 44)
                   and forceBool(record.value('eventDispanserObserved'))
                   # 0014040: Правка правил выгрузки ID_GOAL
                   and getIdentification('EventType', eventTypeId, 'urn:tfoms78:ID_GOAL', False) == '8'
                 ):
                    goalCode = 8 # диспансерное наблюдение
            # 4. Если значение поля CASE_CAST соответствует 1, 2, 34, 35 или 39,
            #    а также параметр "назначение" типа события соответствует значению "прочее",
            #    заполняется 4.
            elif ( caseCast in (1, 2, 34, 35, 39)
                   and eventTypePurposeCode == '4'
                 ):
                goalCode = 4 # Посещение с иными целями
            # 5. Если значение поля CASE_CAST соответствует 1, 2, 34 или 39,
            #    а также тарифицируется визит с кодом типа="ПД",
            #    либо тарифицируется МЭС с группой из списка ("МедОсм", "ДиспанС", "ПрофК")
            #    заполняется 2.
            elif ( caseCast in (1, 2, 34, 39)
                   and (   visitTypeCode == u'ПД'
                        or mesGroupCode in (u'МедОсм', u'ДиспанС', u'ПрофК')
                       )
                 ):
                goalCode = 2 # Посещение с профилактической целью
            # 6. Если значение поля CASE_CAST соответствует 1  или 34,
            #    а также есть визит с кодом типа="ЗубПр" (возможно, лучше будет назвать как-то по-другому этот Тип визита "Подготовка к зубопротезированию", но я не придумала),
            #    заполняется 6.
            elif ( caseCast in (1, 34)
                   and visitTypeCode == u'ЗубПр'
                 ):
                goalCode = 6 # зубопротезирование
            # 7. Если значение поля CASE_CAST соответствует 1, 2, 34, 36, 39 или 56,
            #    а также заключительный диагноз не начинается на на букву Z (корме диагнозов Z30.0, Z30.4, Z32.0, Z32.1, Z34.0, Z34.9, Z35.2, Z35.9, Z39.0, Z39.1, Z39.2)
            #    и дата начала события не соответствует дате окончания события,
            #    заполняется 5.
            elif ( caseCast in (1, 2, 34, 36, 39, 56)
                   and (    eventDiag in self.gynecologicalExaminations
                         or not eventDiag.startswith('Z')
                       )
                   and forceDate(record.value('setDate')) != forceDate(record.value('execDate'))
                 ):
                goalCode = 5 # Обращение по поводу заболевания
            # 8. Если значение поля CASE_CAST соответствует 1, 2, 34, 35 или 39,
            #    а также заключительный диагноз не начинается на на букву Z (корме диагнозов Z30.0, Z30.4, Z32.0, Z32.1, Z34.0, Z34.9, Z35.2, Z35.9, Z39.0, Z39.1, Z39.2)
            #    и дата начала события соответствует дате окончания события,
            #    заполняется 7.
            elif ( caseCast in (1, 2, 34, 35, 39)
                   and (    eventDiag in self.gynecologicalExaminations
                         or not eventDiag.startswith('Z')
                       )
                   and forceDate(record.value('setDate')) == forceDate(record.value('execDate'))
                 ):
                goalCode = 7 # Разовое обращение по поводу заболевания
            # 9. Если значение поля CASE_CAST соответствует 1, 2, 34, 35 или 39,
            #    а также случай не попал в предыдущие категории,
            #    заполняется 4.
            elif ( caseCast in (1, 2, 34, 35, 39)
                 ):
                goalCode = 4 # Посещение с иными целями
            # 10. Если значение поля CASE_CAST соответствует 10, 11, 12, 13, 14, 15, 16 или 17,
            #    заполняется 2.
            #   0010992: ТФОМС СПб. Добавление новых значений ID_GOAL для CASE_CAST 53 и 54.
            #  Здесь следует добавить:
            #  "10. Если значение поля CASE_CAST соответствует 10, 11, 12, 13, 14, 15, 16, 17, 53 или 54, заполняется 2.".
            #  Таким образом, заполнение ID_GOAL и ID_GOAL_C должно быть одинаковым для CASE_CAST 10, 11, 53 и 54.
            elif ( caseCast in (10, 11, 12, 13, 14, 15, 16, 17,  53, 54)
                 ):
                goalCode = 2 # Посещение с профилактической целью
            # 11. Если значение поля CASE_CAST соответствует 19, 20, 21, 22, 23, 24, 28, 29, 30 или 32,
            # заполняется 2.
            elif ( caseCast in (19, 20, 21, 22, 23, 24, 28, 29, 30, 32)
                 ):
                goalCode = 2 # Посещение с профилактической целью
            # 12. Если значение поля CASE_CAST соответствует 44
            #     и подобранный МЭС является частью группы "ДиспанС",
            #     заполняем ID_GOAL значением 13.
            elif ( caseCast in (44, 48)
                   and mesGroupCode == u'ДиспанС'
                 ):
                goalCode = 13 # 0009766: Диспансеризация 1 раз в 2 года (ID_GOAL = 13)
            # 13. Если значение поля CAST_CAST соответствует 49 или 47, заполняем ID_GOAL значением 13
            elif ( caseCast in (47, 49)
                 ):
                goalCode = 13 # 0009766: Диспансеризация 1 раз в 2 года (ID_GOAL = 13)
            # 14. При всех прочих значениях поля CASE_CAST, заполняется 1.
            else:
                goalCode = 1 # без уточнения
            ##################################################### end of ID_GOAL

            hospType = 5 # нет госпитализации
            if caseCast == 6:
                if not eventHaveMoving:
                    hospType = 2 # приемное отделение
                elif dateIn == date or forceDateTime(record.value('setDate')).secsTo(forceDateTime(record.value('execDate'))) < 86400:
                    hospType = 3 # Досуточная госпитализация
                else:
                    hospType = 1 # Стационар
            elif caseCast == 7:
                if self.isHospital:
                    hospType = 4 # Дневной стационар с МЭС

            if aidKindCodeAsInt == 2: # СМП
                callCardNumber = forceString(QtGui.qApp.db.translate('EmergencyCall', 'event_id', eventId, 'numberCardCall'))
                if callCardNumber:
                    illHistoryId = u'%s s'% (callCardNumber, )
                else:
                    illHistoryId = u'%d i' % (eventId, )

                preliminaryDiag  = ''
#            elif eventExternalId and eventTypeAidTypeCode in ('1', '2', '3', '7'):
            else:
                if eventExternalId:
                    illHistoryId = u'%s' % (eventExternalId, )
                else:
                    illHistoryId = u'%d i' % (eventId, )
                preliminaryDiag = self.formatDiagCode(eventDiag)


            if (      self.groupByProfile
                  and tariffType == CTariff.ttActionAmount
                  and serviceDetail.infisCode in (u'иБХим', u'иКлин', u'иГорм',  u'иИмму')
               ):
                key = (eventId, pyDate(dateIn), serviceDetail.infisCode, )
                if key in self.mapServiceToDBFRecord:
                    dbfRecord = self.mapServiceToDBFRecord[key]
                else:
                    dbfRecord = self.dbf.newRecord()
                    self.mapServiceToDBFRecord[key] = dbfRecord
            else:
                dbfRecord = self.dbf.newRecord()

            serviceCode = serviceDetail.infisCode
            if (     tariffType == CTariff.ttVisit
                 and re.match(u'^а(Пед|Тер|ВОП)Уч$', serviceCode)
               ):
                if order == u'э':
                    serviceCode += u'Н'
                elif self.serviceRepetionCount(eventId, serviceCode) > 1:
                    serviceCode += u'О'

            dbfRecord['SURNAME']    = lastName  or u'-' # Фамилия пациента
            dbfRecord['NAME1']      = firstName or u'-' # Имя пациента
            dbfRecord['NAME2']      = patrName  or u'-' # Отчество пациента
            dbfRecord['BIRTHDAY']   = pyDate(birthDate) # дата рождения
            dbfRecord['SEX']        = formatSex(sex)    # Пол (М/Ж)
            dbfRecord['POLIS_S']    = policySerial  # Серия полиса
            dbfRecord['POLIS_N']    = policyNumber  # Номер полиса
#            dbfRecord['POLIS_W']    = policyInsurer # Код СМО, выдавшей полис
            dbfRecord['PAYER']      = '' # Код СМО, выдавшей полис?
            dbfRecord['TYPEDOC']    = str(documentType)  # Тип документа
            dbfRecord['SER1']       = documentSeries[0] # Серия документа, левая часть
            dbfRecord['SER2']       = documentSeries[1] # Серия документа, левая часть
            dbfRecord['NPASP']      = documentNumber# Номер документа
            dbfRecord['SNILS']      = snils
            dbfRecord['STREET']     = street       # Адрес пациента: код улицы
            dbfRecord['STREETYPE']  = streetType   # Адрес пациента: тип улицы
            dbfRecord['AREA']       = area         # Адрес пациента: код район
            dbfRecord['HOUSE']      = house        # Адрес пациента: номер дома
            dbfRecord['KORP']       = corpus       # Адрес пациента: корпус
            dbfRecord['FLAT']       = flat         # Адрес пациента: номер квартиры
            dbfRecord['LONGADDR']   = longAddress  # дополнительно для поиска пациента
            dbfRecord['ORDER']      = order        # Признак экстренности случая лечения (если случай экстренный - принимает значение "э" или "Э")
            dbfRecord['SERV_ID']    = eventId      # идентификатор случая
            dbfRecord['ID_IN_CASE'] = self.mapEventIdToCount[eventId] = self.mapEventIdToCount.get(eventId, 0)+1 # Порядковый номер записи в случае (в пределах одного SERV_ID)
            dbfRecord['PROFILE']    = serviceCode  # Код профиля лечения
            dbfRecord['PROFILENET'] = profileNet   # Тип сети профиля (в - взрослая, д - детская)

            dbfRecord['DATEIN']     = pyDate(dateIn) # Дата начала услуги
            dbfRecord['DATEOUT']    = pyDate(date) # Дата окончания услуги
            dbfRecord['AMOUNT']     += amount       # Объем (кратность?) лечения
            dbfRecord['AMOUNT_D']   += amountDays   # Длительность лечения в днях
            dbfRecord['DIAGNOSIS']  = self.formatDiagCode(actionDiag or visitDiag or eventDiag) # Код диагноза
            dbfRecord['ID_C_ZAB']   = diseaseCharacterCode \
                                      if diseaseCharacterCode and caseCast not in (8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 28, 29, 30, 32, 44, 45, 46, 47, 48, 49, 53, 54) \
                                      else 2837
            dbfRecord['SEND']       = False        # Флаг обработки записи
            dbfRecord['ERROR']      = ''           # Описание ошибки
            dbfRecord['ID_PRVS']    = specialityCode
            dbfRecord['IDPRVSTYPE'] = prvsTypeId or 1 # говорят, что значение 0 "табу"
            dbfRecord['PRVS_PR_G']  = prvsGroup  or 1 # говорят, что значение 0 "табу"
            dbfRecord['ID_EXITUS']  = forceInt(record.value('visitDiagnosticResultCode')) or forceInt(record.value('eventDiagnosticResultCode'))
            dbfRecord['ILLHISTORY'] = illHistoryId
            dbfRecord['CASE_CAST']  = caseCast
            dbfRecord['ID_INTER']   = (1 if mesIsDone else 2) if (mesId and caseCast in (52,)) else 0
            dbfRecord['ID_GOSP']    = hospType
            dbfRecord['ID_PRMP']    = aidProfileCode # Код профиля по Классификатору профиля
            dbfRecord['ID_PRMP_C']  = eventAidProfileCode # Код профиля по Классификатору профиля для случая лечения
            dbfRecord['DIAG_C']     = self.formatDiagCode(eventDiag)                # Код диагноза для случая лечения
            dbfRecord['DIAG_S_C']   = ''                                            # Код сопутствующего диагноза для случая лечения
            dbfRecord['DIAG_P_C']   = preliminaryDiag                               # Код предварительного диагноза для случая лечения
            dbfRecord['QRESULT']    = forceInt(record.value('eventResultCode'))     # Результат обращения за медицинской помощью
            dbfRecord['ID_PRVS_C']  = eventSpecialityCode                           # Код врачебной специальности для случая лечения
            dbfRecord['ID_SP_PAY']  = spPay                                         # ID способа оплаты медицинской помощи
            dbfRecord['ID_ED_PAY']  = forceDouble(record.value('amount'))           # Количество единиц оплаты медицинской помощи
            dbfRecord['ID_VMP']     = aidKindCodeAsInt                              # ID вида медицинской помощи
            dbfRecord['ID_DOC']     = self.getPersonIdentifier(personId)      # Идентификатор врача из справочника SPRAV_DOC.DBF (для услуги)
            dbfRecord['ID_DOC_C']   = self.getPersonIdentifier(eventPersonId) # Идентификатор врача из справочника SPRAV_DOC.DBF (для случая)
            if dbfRecord['ID_DOC'] == '0':
                dbfRecord['ID_DOC'] = dbfRecord['ID_DOC_C']
            if hospType == 2:
                dbfRecord['ID_DEPT']    = self.receivingDepartmentIdentifier or self.getOrgStructureIdentifier(personId)      # Идентификатор отделения МО из справочника SPRAV_DEPTS.DBF (для услуги)
                dbfRecord['ID_DEPT_C']  = self.receivingDepartmentIdentifier or self.getOrgStructureIdentifier(eventPersonId) # Идентификатор отделения МО из справочника SPRAV_DEPTS.DBF (для случая)
            elif caseCast == 4: # 0014096: Выгрузка данных о подразделении в случаях обслуживания по дневному стационару.
                dbfRecord['ID_DEPT']    = 36
                dbfRecord['ID_DEPT_C']  = 36
            else:
                dbfRecord['ID_DEPT']    = self.getOrgStructureIdentifier(personId) # Идентификатор отделения МО из справочника SPRAV_DEPTS.DBF (для услуги)
                dbfRecord['ID_DEPT_C']  = self.getOrgStructureIdentifier(eventPersonId) # Идентификатор отделения МО из справочника SPRAV_DEPTS.DBF (для случая)

            if tariffType == CTariff.ttActionAmount and actionSetPersonSpecialityCode:
                directionLpuId  = self.getOrgIdentifier(eventRelegateOrOwnOrgId, False)
#                directionSpecialityCode = actionSetPersonSpecialityCode
#                directionGoalId = goalCode
            elif eventRelegateOrOwnOrgId and eventSpecialityCode:
                directionLpuId  = self.getOrgIdentifier(eventRelegateOrOwnOrgId, False)
#                directionSpecialityCode = eventSpecialityCode
#                directionGoalId = goalCode
            else:
                directionLpuId  = 0
#                directionSpecialityCode = 0
#                directionGoalId = 0

            offsideLpuId = self.getOffsideLpuId(eventRelegateOrOwnOrgId)
            if offsideLpuId is None:
                directionLpuIdTuple = ( directionLpuId,   # Идентификатор ЛПУ, направившего на лечение (из справочника SPRAV_LPU.DBF)
                                        0
                                      )
            else:
                directionLpuIdTuple = ( 20578,  # что соответствует по справочнику LPU в ЕИС Иногородней МО
                                        forceInt(toVariant(offsideLpuId))
                                      )

            dbfRecord['IS_CRIM']    = False # криминал F - нет , T - есть

#            dbfRecord['Q_RES']      = resultCode
            dbfRecord['IDSERVDATA'] = additionalServiceCode                         # Идентификатор пункта карты диспансеризации

            if  orgId and orgId != self.currentOrgId:
                orgStructureIdentifier = self.getOrgIdentifier(orgId or self.currentOrgId, False)
            else:
                orgStructureIdentifier = self.getOrgStructureIdentifier2(personId)
            if not orgStructureIdentifier:
                orgStructureIdentifier = self.getOrgIdentifier(orgId, True)
            personOrgStructureIdentifier = orgStructureIdentifier

            eventOrgStructureIdentifier = self.getOrgStructureIdentifier2(eventPersonId)
            if not eventOrgStructureIdentifier:
                eventOrgStructureIdentifier = self.getOrgIdentifier(orgId, True)

            if servMade == 1:
                if personOrgStructureIdentifier != eventOrgStructureIdentifier:
                    servMade = 2
                orgStructureIdentifier = personOrgStructureIdentifier
            elif servMade == 3:
                personOrgStructureIdentifier = eventOrgStructureIdentifier
            elif servMade == 4:
                orgStructureIdentifier = personOrgStructureIdentifier = eventOrgStructureIdentifier
            elif servMade == 5:
                personOrgStructureIdentifier = eventOrgStructureIdentifier
            else:
                personOrgStructureIdentifier = eventOrgStructureIdentifier

            dbfRecord['IDSERVMADE'] = servMade
#            dbfRecord['IDSERVMADE'] = servMade if servMade != 2 else 1 # 0011321: ТФОМС СПб. Изменение условий выгрузки поля IDSERVMADE основного файл; за 2 не плотют, гады :(
            dbfRecord['IDSERVLPU']  = orgStructureIdentifier

            dbfRecord['ID_GOAL_C']  = goalCode
            dbfRecord['ID_GOAL']    = goalCode
            dbfRecord['ID_PAT_CAT'] = patCat                  # статус пациента
            dbfRecord['IDVIDVME']   = medicalInterventionCode # Идентификатор вида мед. вмешательства
            dbfRecord['IDFORPOM']   = forPom                  # Идентификатор формы оказания помощи
#            dbfRecord['IDVIDHMP']   = 0                      # Идентификатор вида высокотехнологичной мед помощи
            dbfRecord['IDMETHMP']   = 0                       # Идентификатор метода высокотехнологичной мед помощи
            dbfRecord['ID_LPU']     = self.eisLpuId  # Идентификатор БД ЛПУ, в которую загружаются данные
            dbfRecord['N_BORN']     = newbornId      # Порядковый номер новорожденного
            dbfRecord['ACC_ID']     = accountId

            if dbfRecord['ACCITEM_ID'] == '':
                dbfRecord['ACCITEM_ID'] = str(accountItemId)
            else:
                dbfRecord['ACCITEM_ID'] += ' ' + str(accountItemId)
            dbfRecord['ACTION_ID']  = originatedFromAction or 0
            dbfRecord['CLIENT_ID']  = clientId
            dbfRecord['ID_FINT']    = finType
            if eventTypeAidTypeCode in ('1', '2', '3', '7'): # 0008916 -- заполнять ID_TRANSF не во всех случаях
                dbfRecord['ID_TRANSF']  = transf
            dbfRecord['ID_INCOMPL'] = incompl
            dbfRecord['ID_LPU_P']   = personOrgStructureIdentifier # Идентификатор подразделения МО (для услуги)
            dbfRecord['ID_LPU_P_C'] = eventOrgStructureIdentifier  # Идентификатор подразделения МО (для случая)


            if eventTypeAidTypeCode in ('1', '2', '3', '7'):
                dbfRecord['ID_B_PROF']  = self.getHospitalBedProfile(eventId,
                                                                     eventAidProfileId if eventTypeAidTypeCode == '7' else None,  # Дневной стационар
                                                                    )
            # специальный случай - ковидный пациент на непрофильной койке и непрофильный врач.
            # Если в реестре счета значение поля ID_B_PROF равно 83, то в поле ID_PRMP выгружаем значение 18, а в поле ID_PRVS выгружаем значение 332
            # см. #0012723
            if dbfRecord['ID_B_PROF'] == 83:
                dbfRecord['ID_PRMP'] = dbfRecord['ID_PRMP_C'] = 18
                dbfRecord['ID_PRVS'] = dbfRecord['ID_PRVS_C'] = 332
            dbfRecord.store()

            self.caseRegistry[eventId][1].append(specialityCode)
            if self.isReanimation(serviceId):
                self.addExtService(eventId, actionId)
            if self.mapEventIdToCount[eventId] == 1: # первая запись для этого eventId
                cancerSuspected = self.cancerSuspected(eventId)
                eventFormIs001  = forceString(record.value('eventForm')) == '001'
                directionNumber = forceString(record.value('srcNumber'))
                directionDate   = forceDate(record.value('srcDate')) or forceDate(record.value('setDate'))
                relegateSpecialityCode = forceInt(record.value('relegateSpecialityCode'))

#                if caseCast in (1,10,11,13,15,19,20,24,34,35,37,45):
#                if caseCast in (1,10,11,13,15,19,20,21,34,35,37,45,47,48,49,53,54):
                if caseCast in (1,10,11,13,15,19,20,21,24,34,35,37,45,47,48,49,53,54):
                    directionType  = None
                    directionGroup = None
                    directionGoalCode = 20
                    case = '1'
                    if self.eventHasResearch(eventId):
                        specialityCode = relegateSpecialityCode or eventSpecialityCode
                        directionType, directionGroup  = self.getDirectionTypeAndGroup(serviceId)
                        if directionGroup:
                            if cancerSuspected:
                                directionGoalCode = 15 # подозрение на онкологическое заболевание
                                case = '1.1'
                            elif self.cancerDispensaryObservation(eventId):
                                directionGoalCode = 17 # диспанс. наблюдение пациента с онк. заболеванием
                                case = '1.2'
                            elif self.cancerObservation(eventId):
                                directionGoalCode = 16 # наблюдение пациента с онк. заболеванием
                                case = '1.3'
                            elif self.afterCancer(eventId) and forceBool(record.value('eventDispanserObserved')):
                                directionGoalCode = 18 # диспанс. наблюдение пациента, перенесшего онк. заболевание
                                case = '1.4'
                            elif mesGroupCode == u'ДиспанС':
                                directionGoalCode = 19 # исследование в рамках диспансеризации
                                case = '1.5'
                            else:
                                directionGoalCode = 20
                                case = '1.6'
                        else:
                            directionGoalCode = goalCode
                            directionType  = 20 # исследование
                            if caseCast in (1,11,13,15,20,21,34,45,47,49,54):
                                directionGroup = 14
                            elif caseCast in (10,19,35,37,48,53):
                                directionGroup = 12
                            else:
                                directionGroup = 14
#                            directionGroup = 14
                            case = '1.7'
                        self.addDirection(eventId,
                                          directionGroup = directionGroup,
                                          directionType = directionType,
                                          number = directionNumber,
                                          date = directionDate,
                                          goalCode = directionGoalCode,
                                          specialityCode = specialityCode,
                                          targetSpecialityCode = specialityCode,
                                          idLpuTuple = directionLpuIdTuple,
                                          case = case,
                                          caseCast = caseCast
                                         )
                    elif caseCast in (11,13,15,20,24,34,45) and directionGroup != 14:
                        specialityCode = relegateSpecialityCode or eventSpecialityCode
                        self.addDirection(eventId,
                                          directionGroup = 14,
                                          directionType = 19, # лечение
                                          number = directionNumber,
                                          date = directionDate,
                                          goalCode = directionGoalCode,
                                          specialityCode = specialityCode,
                                          targetSpecialityCode = specialityCode,
                                          idLpuTuple = directionLpuIdTuple,
                                          case = '2',
                                          caseCast = caseCast
                                         )
                elif (    ( eventRelegateOrgId and not eventFormIs001 ) # есть направление
                     or eventTypeAidTypeCode == '7'  # дневной стационар
                     or caseCast in (12,13,44,45) # Второй этап ДД
                   ) :
                    case = '3'
                    if caseCast in (12,13,44,45): # Второй этап ДД
                        directionType  = 21  # (Направление на ДД2)
                        directionGroup = 13
                        case = '3.1'
                    else:
                        directionType  = 19  # (Направление на лечение)
                        directionGroup = 11
                        case = '3.2'
                    self.addDirection(eventId,
                                      directionGroup = directionGroup,
                                      directionType = directionType,
                                      number = directionNumber,
                                      date   = directionDate,
                                      hospitalBedProfileId = None,
                                      examinationType = None,
                                      specialityCode = relegateSpecialityCode or eventSpecialityCode,
                                      targetSpecialityCode = eventSpecialityCode,
                                      idLpuTuple = directionLpuIdTuple,
                                      case = case,
                                      caseCast = caseCast
                                     )
                if eventTypeAidTypeCode in ('1', '2', '3'):
                    self.addExtCases(eventId)
                    self.addDirections(True, False, False, eventId, goalCode, caseCast)
                else:
                    self.addDirections(False, mesGroupCode in (u'ДиспанС', u'МедОсм'), forceInt(record.value('eventResultCode')) in (89, 90, 91, 94, 95),  eventId, goalCode, caseCast)
                if mesGroupCode == u'реаб':
                    self.addRehabilitationExtCases(eventId)


                # 0009848: ТФОМС СПб. Изменения согласно 59 приказу ФФОМС. Подозрение на онкологию.
                ### ОНКОЛОГИЯ, см. #0010281: ТФОМС СПб. Приказ №200 (ЗНО). Версия декабрь 2018
                if cancerSuspected:
                    # Подозрение на онкологию
                    self.addExtCase(eventId,
                                    objectId=29,  # Подозрение на онкологию
                                    objectValue='1',
                                   )
                    self.detectDirectionsToConsultationToOncologist(eventId, caseCast)
                    self.detectDirectionsToInspection(eventId, caseCast)
                    self.detectDirectionsToMRI(eventId, caseCast)
                    self.detectOnkoConsilium(eventId, forceDate(record.value('execDate')))
                else:
                    diags = self.getCancerCureDiagnoses(eventId)
                    if ( eventTypeAidTypeCode not in ('4', '5')
                         and diags
                       ):
                        # Лечение онкологии
                        if filter(lambda diag: not diag.observed and diag.characterCode != '3',
                                  diags
                                 ):
                            self.addDirection(eventId,
                                              directionGroup = 14, # "Направление на лечение (диагностику, консультацию, госпитализацию) (входящее)"
                                              directionType = 19,  # "Направление на лечение (диагностику, консультацию, госпитализацию) (входящее)"
                                              number = directionNumber,
                                              date   = directionDate,
                                              hospitalBedProfileId = None,
                                              examinationType = None,
                                              specialityCode = relegateSpecialityCode or eventSpecialityCode,
                                              targetSpecialityCode = eventSpecialityCode,
                                              idLpuTuple = directionLpuIdTuple,
                                              case = '3.3',
                                              caseCast = caseCast
                                         )

                        self.addExtCase(eventId,
                                        objectId=30,  # Онкология
                                        objectValue='1',
                                       )
                        for diag in diags:
                            self.addOnkoAddRecord(eventId, diag)
                        self.detectOnkoRejection(eventId, caseCast)
                        self.detectOnkodiagnostics(eventId)
                        self.detectOnkoServs(eventId, eventPersonId, dateIn)
                        self.detectOnkoConsilium(eventId, forceDate(record.value('execDate')))

                # 0009999: ТФОМС СПб. выгрузка данных по ДН
                # 0011065: ТФОМС СПб. Изменения в заполнении данных по ДН в файле *_D.dbf
                # 0011163: ТФОМС СПб. Дополнение к заполнению данных по ДН в файле *_D.dbf
                # 0014008: Выгрузка данных в файл *_D.dbf если ДН не указан
                if caseCast not in (3,4,6,7,8,11,47,49):
                    diags = self.getDispensaryObservationDiagnoses(eventId)
                    toAddMainDiagnosis = True
                    if diags:
                        for (mkb, isMainDiagnosis, dispensaryObservationCode, date) in diags:
                            case = '4'
                            if mesGroupCode in (u'ДиспанС', u'МедОсм') or caseCast in (10, 12, 14, 19, 20, 23, 32, 44, 53):
                                if isMainDiagnosis:
                                    if not toAddMainDiagnosis:
                                        continue
                                    directionGroup = 9
                                    directionType  = 17
                                    diagnosisType  = 4
                                    toAddMainDiagnosis = False
                                    case = '4.1'
                                else:
                                    directionGroup = 10
                                    directionType  = 18
                                    diagnosisType  = 1
                                    case = '4.2'
                            else:
                                if isMainDiagnosis:
                                    if not toAddMainDiagnosis:
                                        continue
                                    directionGroup = 8
                                    directionType  = 16
                                    diagnosisType  = 4
                                    toAddMainDiagnosis = False
                                    case = '4.3'
                                else:
                                    continue
                            self.addDirection(eventId,
                                              directionGroup = directionGroup,
                                              directionType  = directionType,
                                              dispensaryObservationCode = dispensaryObservationCode,
                                              mkb = mkb,
                                              date = date,
                                              case = case,
                                              caseCast = caseCast
                                             )
                            self.addExtCase(eventId,
                                            objectId = diagnosisType,
                                            mkb = mkb
                                           )
                    if toAddMainDiagnosis and caseCast not in (1,2,34,35,36,37,39,56):
                        diagnosisType = 4
                        if mesGroupCode in (u'ДиспанС', u'МедОсм') or caseCast in (10, 12, 14, 19, 20, 23, 32, 44, 53):
                            directionGroup = 9
                            directionType  = 17
                            case = '5.1'
                        else:
                            directionGroup = 8
                            directionType  = 16
                            case = '5.2'
                        self.addDirection(eventId,
                                          directionGroup = directionGroup,
                                          directionType  = directionType,
                                          dispensaryObservationCode = 3,
                                          mkb = eventDiag,
                                          case = case,
                                          caseCast = caseCast
                                         )
                        self.addExtCase(eventId,
                                        objectId = diagnosisType,
                                        mkb = eventDiag
                                       )
                # 0013549: обновление по экспорту счетов
                if eventTypeAidTypeCode in ('1', '2', '3', '6') and eventDiag in ('U07.1', 'U07.2'):
                    weight, severity = self.getCovidAddInfo(eventId)
                    self.addCovidAdd(eventId, weight, severity)
                    self.addCovidDrugs(eventId, severity)
                # 0014061: ТФОМС СПб. ЕИС. Выгрузка данных о впервые выявленном диагнозе
                self.addFirstlyDetectedChronicDiagnoses(eventId, caseCast)

                # 0014079: Выгрузка двнных о ШРМ
                if eventTypeAidTypeCode in ('6',  '7'):
                    self.addRehabilitationRoutingScore(eventId)

                # 0014419: ТФОМС СПб. Передача данных о телемедицинской консультации в ЕИС
                if eventTypeAidTypeCode == '10' and caseCast == 36:
                    self.addDirection(eventId,
                                      directionGroup = 21,
                                      directionType  = 40,
                                      date = forceDate(record.value('setDate')),
                                      targetSpecialityCode = eventSpecialityCode,
                                      case = '6',
                                      caseCast = caseCast
                                     )


            # конец первой записи для этого eventId
            self.fixDirections(dbfRecord)

        if self.clientsDbf is not None and clientId not in self.knownClientIdSet:
            self.knownClientIdSet.add(clientId)
            #if self.clientDoesNotHaveEISId(clientId):
            if True:
                smoReg = 0
                if citizenship != '643': # указано гражданство - не Россия
                    tfomsExtCode = self.getPayer(u'иКом')
                else:
                    if record.isNull('insurerArea'):
                        # будем это считать признаком, что нет полиса
                        tfomsExtCode = self.getPayer(u'кТФ1') # нет полиса
                    else:
                        if not insurerArea.startswith('78'):
                            smoReg = tfomsExtCode
                            tfomsExtCode = self.getPayer(u'кТФ3') # не питер
                dbfRecord = self.clientsDbf.newRecord()
                dbfRecord['SURNAME']   = lastName  or '-'  # Фамилия пациента
                dbfRecord['NAME']      = firstName or '-'  # Имя пациента
                dbfRecord['S_NAME']    = patrName  or '-'  # Отчество пациента
                dbfRecord['BIRTHDAY']  = pyDate(birthDate) # Дата рождения
                dbfRecord['SEX']       = formatSex(sex)    # Пол (М/Ж)
                dbfRecord['ID_PAT_CAT']= patCat            # Статус (2 - неопределено), ?!

                dbfRecord['DOC_TYPE']  = documentType      # Тип документа
                dbfRecord['SER_L']     = documentSeries[0] # Серия документа, левая часть
                dbfRecord['SER_R']     = documentSeries[1] # Серия документа, левая часть
                dbfRecord['DOC_NUMBER']= documentNumber    # Номер документа
                dbfRecord['ISSUE_DATE']= pyDate(forceDate(record.value('documentDate'))) # Дата выдачи документа
                dbfRecord['DOCORG']    = forceString(record.value('documentOrigin'))     # Наименование органа, выдавшего документ, удостоверяющий личность
                dbfRecord['SNILS']     = snils             # СНИЛС
                dbfRecord['C_OKSM']    = citizenship       # Гражданство ('643' - РФ, '000' - Не определено) ?!
                dbfRecord['IS_SMP']    = False             # Признак "пациент СМП"
                if policyInsurer == u'нКом' and (tfomsExtCode == 389 or smoReg == 389):
                    policyKind = '0'
                elif policyInsurer == u'иКом' and (tfomsExtCode == 41 or smoReg == 41):
                    policyKind = '0'
                else:
                    policyKind = forceString(record.value('policyKindRegionalCode'))
                dbfRecord['POLIS_TYPE']= policyKind        # Тип полиса
                dbfRecord['POLIS_S']   = policySerial      # Серия полиса
                dbfRecord['POLIS_N']   = policyNumber      # Номер полиса
                dbfRecord['ID_SMO']    = tfomsExtCode      # СМО
                dbfRecord['POLIS_BD']  = pyDate(policyBegDate) # Дата начала действия полиса
                dbfRecord['POLIS_ED']  = pyDate(policyEndDate) # Дата окончания действия полиса
                dbfRecord['ID_SMO_REG'] = smoReg # Региональная СМО (для иногородних)

                addrType, regOkatoId, houseId, house, corpus, flat, freeInput, KLADRCode, street, streetTypeId  = self.getClientAddressParts(clientId, 0)

                dbfRecord['ADDR_TYPE'] = addrType   # Тип адреса
                dbfRecord['IDOKATOREG']= regOkatoId # Регион
                dbfRecord['ID_HOUSE']  = houseId    # Идентификатор дома (для адресов СПб, тип "г")
                dbfRecord['HOUSE']     = house      # Номер дома (для типа "р")
                dbfRecord['KORPUS']    = corpus     # Корпус (для типа "р")
                dbfRecord['FLAT']      = flat       # Квартира
                dbfRecord['U_ADDRESS'] = freeInput  # Неструктурированный адрес (для типа "п")
                dbfRecord['KLADR_CODE']= KLADRCode  # Код КЛАДР (для типа "р")
                dbfRecord['STREET']    = street     # Название улицы (для типа "р")
                dbfRecord['IDSTRTYPE'] = streetTypeId # Тип улицы (для типа "р")
                addrType, regOkatoId, houseId, house, corpus, flat, freeInput, KLADRCode, street, streetTypeId = self.getClientAddressParts(clientId, 1)
                dbfRecord['ADDRTYPE_L']= addrType   # Тип адреса
                dbfRecord['OKATOREG_L']= regOkatoId # Регион
                dbfRecord['ID_HOUSE_L']= houseId    # Идентификатор дома (для адресов СПб, тип "г")
                dbfRecord['HOUSE_L']   = house      # Номер дома (для типа "р")
                dbfRecord['KORPUS_L']  = corpus     # Корпус (для типа "р")
                dbfRecord['FLAT_L']    = flat       # Квартира
                dbfRecord['U_ADDR_L']  = freeInput  # Неструктурированный адрес (для типа "п")
                dbfRecord['KLADR_L']   = KLADRCode  # Код КЛАДР (для типа "р")
                dbfRecord['STREET_L']  = street     # Название улицы (для типа "р")
                dbfRecord['STRTYPE_L'] = streetTypeId # Тип улицы (для типа "р")

                #dbfRecord['PLACE_WORK'] =   # Место работы
                #dbfRecord['ADDR_WORK'] =   # Адрес места работы
                #dbfRecord['ADDR_PLACE'] =  # Место взятия
                #dbfRecord['REMARK'] =   # Примечение
                dbfRecord['B_PLACE'] = forceString(record.value('birthPlace')) # Место рождения

                dbfRecord['N_BORN'] = newbornId # Порядковый номер новорожденного
                dbfRecord['SEND']   = False    # Признак принят (true/false), default - false
                dbfRecord['ID_MIS'] = clientId # Идентификатор пациента из внешних данных

                if newbornId:
                    representativeInfo = getClientRepresentativeInfo(clientId)
                    if representativeInfo:
                        try:
                            relationType = int(representativeInfo['regionalRelationTypeCode'])
                        except:
                            relationType = 0
                        dbfRecord['ID_G_TYPE'] = relationType # Тип представителя
                        dbfRecord['G_SURNAME'] = representativeInfo['lastName']  or '-' # Фамилия
                        dbfRecord['G_NAME']    = representativeInfo['firstName'] or '-' # Имя
                        dbfRecord['G_S_NAME']  = representativeInfo['patrName']  or '-' # Отчество
                        dbfRecord['G_BIRTHDAY']= pyDate(representativeInfo['birthDate']) # Дата рождения
                        dbfRecord['G_SEX']     = formatSex(representativeInfo['sex'])   # Пол
                        dbfRecord['G_DOC_TYPE']= self.getDocumentType( # Тип документа
                                                    representativeInfo['documentTypeRegionalCode'],
                                                    representativeInfo['documentTypeCode'])
                        dbfRecord['G_SERIA_L'], dbfRecord['G_SERIA_R'] = self.parseDocumentSerial(representativeInfo['serial'])
                        representativeInfo['serial']
                        dbfRecord['G_DOC_NUM'] = representativeInfo['number'] or '-'# Номер документа
                        dbfRecord['G_ISSUE_D'] = pyDate(representativeInfo['date']) # Дата выдачи документа
                        dbfRecord['G_DOCORG']  = representativeInfo['origin']       # Наименование органа, выдавшего документ
                        dbfRecord['G_B_PLACE'] = representativeInfo['birthPlace']   # Место рождения
                dbfRecord.store()


    def getDocumentType(self, regionalCode, code):
        if regionalCode and isinstance(regionalCode, (int, long)):
            return regionalCode
        result = regionalCode or self.mapDocTypeToEIS.get(code, '')
        if result and result.isdigit():
            return int(regionalCode)
        return 5


    def parseDocumentSerial(self, documentSerial):
        if len(documentSerial)==4 and documentSerial.isdigit():
            return [documentSerial[:2], documentSerial[2:]]
        result = trim(documentSerial.replace('-', ' ')).split(None, 1)
        return [ result[0] if len(result)>0 and result[0] else '-',
                 result[1] if len(result)>1 and result[1] else '-'
               ]


    def getPayer(self, code):
        if not code in self.payers:
            db = QtGui.qApp.db
            self.payers[code] = forceInt(db.translate('Organisation', 'infisCode', code, 'tfomsExtCode'))
        return self.payers[code]


    def formatDiagCode(self, mkb):
        result = self.mkbCache.get(mkb, None)
        if result is None:
            prim    = forceString(QtGui.qApp.db.translate('MKB', 'DiagID', MKBwithoutSubclassification(mkb), 'Prim'))
            # новая вводная: в случае субклассификации без пятого знака
            # субклассификация должна помещаться на пятый знак
            result = MKBwithoutSubclassification(mkb.replace(' ', '')) + prim
            self.mkbCache[mkb] = result
        return result


    def getCompletedTreatmentCaseUnitCode(self):
        if self.completedTreatmentCaseUnitCode is None:
            db = QtGui.qApp.db
            self.completedTreatmentCaseUnitCode = forceInt(db.translate('rbMedicalAidUnit', 'name', u'ЗСЛ', 'regionalCode'))
            if not self.completedTreatmentCaseUnitCode:
                self.completedTreatmentCaseUnitCode = 48 # !!!
        return self.completedTreatmentCaseUnitCode


    def getMedicalAidProfileCodes(self, profileId):
        if profileId:
            item = self.profileCache.get(profileId, None)
            if item is None:
                record = QtGui.qApp.db.getRecord('rbMedicalAidProfile', ['regionalCode', 'federalCode'], profileId)
                if record:
                    item = ( forceInt(record.value(0)),
                             forceInt(record.value(1))
                           )
                    self.profileCache[profileId] = item
            if item:
                return item
        return None


    def getAidCodesAndProfileId(self, serviceDetail, date, specialityId, birthDate, sex, diagnosis):
        age = calcAgeTuple(birthDate, date)
        profileId, kindId, typeId = serviceDetail.getMedicalAidIds(specialityId, sex, age, diagnosis)
        profileCodesTuple = self.getMedicalAidProfileCodes(profileId)
        if profileCodesTuple:
            profileRegionalCode, profileFederalCode = profileCodesTuple
        else:
            profileId, profileRegionalCode = self.profileSpecCache.get(specialityId,  (None, None))
            if profileRegionalCode is None:
#               profileRegionalCode = profileFederalCode = 0 # это ноль
                profileRegionalCode = 0 # это ноль
                db = QtGui.qApp.db
                tableSpeciality = db.table('rbSpeciality')
                tableProfile = db.table('rbMedicalAidProfile')
                table = tableSpeciality.leftJoin(tableProfile, tableSpeciality['OKSOName'].eq(tableProfile['name']))
                record = db.getRecordEx(table,
                                        tableProfile['id'],
                                        tableSpeciality['id'].eq(specialityId))
                if record:
                    profileId = forceInt(record.value(0))
                    profileCodesTuple = self.getMedicalAidProfileCodes(profileId)
                    if profileCodesTuple:
                        profileRegionalCode, profileFederalCode = profileCodesTuple
                self.profileSpecCache[specialityId] = profileId, profileRegionalCode
        if kindId:
            kindCode = self.kindCache.get(kindId, None)
            if kindCode is None:
                kindCode = forceString(QtGui.qApp.db.translate('rbMedicalAidKind', 'id', kindId, 'regionalCode'))
                self.kindCache[kindId] = kindCode
        else:
            kindCode = ''
        if typeId:
            typeCode = self.typeCache.get(typeId, None)
            if typeCode is None:
                typeCode = forceString(QtGui.qApp.db.translate('rbMedicalAidType', 'id', typeId, 'code'))
                self.typeCache[typeId] = typeCode
        else:
            typeCode = ''
        return profileRegionalCode, kindCode, typeCode, profileId


    def getAidCodes(self, serviceDetail, date, specialityId, birthDate, sex, diagnosis):
        profileRegionalCode, kindCode, typeCode, profileId = self.getAidCodesAndProfileId(serviceDetail, date, specialityId, birthDate, sex, diagnosis)
        return profileRegionalCode, kindCode, typeCode


    def getMesGroupCode(self, mesId):
        result = self.mapMesIdToGroupCode.get(mesId, None)
        if result is None:
            db = QtGui.qApp.db
            groupId = forceRef(db.translate('mes.MES', 'id', mesId, 'group_id'))
            result  = forceString(db.translate('mes.mrbMESGroup', 'id', groupId, 'code'))
            self.mapMesIdToGroupCode[mesId] = result
        return result


    def getPersonIdentifier(self, personId):
        result = self.mapPersonIdToEisPersonId.get(personId, None)
        if result is None:
            if personId is None:
                result = '0'
            else:
                db = QtGui.qApp.db
                result = forceString(db.translate('Person', 'id', personId, 'regionalCode'))
                if result:
                    if result.find('.') < 0:
                        result = str(self.eisLpuId) + '.' + result
                else:
                    orgId = forceInt(db.translate('Person', 'id', personId, 'org_id'))
                    if orgId != self.currentOrgId:
                        result = '0'
                    else:
                        result = '%s.%s' % (self.getOrgIdentifier(self.currentOrgId, True), personId)
            self.mapPersonIdToEisPersonId[personId] = result
        return result


    def getOrgIdentifier(self, orgId, substOwnCode):
        result = self.mapOrgIdToEis.get(orgId, None)
        if result is None:
            if orgId is None:
                result = 0
            else:
                result = forceInt(QtGui.qApp.db.translate('Organisation', 'id', orgId, 'tfomsExtCode'))
            self.mapOrgIdToEis[orgId] = result

        if substOwnCode and orgId == self.currentOrgId:
            return self.eisLpuId or result
        else:
            return result or self.eisLpuId


    def getOffsideLpuId(self, orgId):
        # для ЛПУ вне СПб - отдельный справочник.
        result = self.mapOrgIdToOffsideLpuId.get(orgId, False)
        if result is False:
            result = getIdentification('Organisation',
                                       orgId,
                                       'urn:tfoms78:SPRAV_LPU_RF',
                                       False
                                      )
            self.mapOrgIdToOffsideLpuId[orgId] = result
        return result


    def getReceivingDepartmentIdentifier(self):
        result = 0
        db = QtGui.qApp.db
        tableOrgStructure = db.table('OrgStructure')
        cond = [ tableOrgStructure['deleted'].eq(0),
                 tableOrgStructure['type'].eq(4), # приёмное отделение
                 tableOrgStructure['organisation_id'].eq(self.currentOrgId),
               ]
        record = db.getRecordEx(tableOrgStructure, 'infisCode', cond, 'id')
        if record:
            result = forceInt(record.value(0))
        return result


    def getOrgStructureIdentifier(self, personId):
        result = 1
        db = QtGui.qApp.db
        tablePerson = db.table('Person')
        tableOrgStructure = db.table('OrgStructure')
        table = tablePerson.leftJoin(tableOrgStructure, tablePerson['orgStructure_id'].eq(tableOrgStructure['id']))
        cond = [tablePerson['id'].eq(personId)]
        record = db.getRecordEx(table, 'OrgStructure.infisCode',  cond)
        if record:
            result = forceInt(record.value(0)) or 1
        return result


    # насрать и розами засыпать.
    def getOrgStructureIdentifier2(self, personId):
        result = self.mapPersonIdToEisOrgStructureCode.get(personId, None)
        if result is None:
            db = QtGui.qApp.db
            record = db.getRecord('Person', ['org_id','orgStructure_id'], personId)
            if record:
                orgId = forceRef(record.value('org_id'))
                orgStructureId = forceRef(record.value('orgStructure_id'))
                result = self.getOrgStructureIdentifier2Int(orgId, orgStructureId)
            else:
                result = 0
            self.mapPersonIdToEisOrgStructureCode[personId] = result
        return result


    def getOrgStructureIdentifier2Int(self, orgId, orgStructureId):
        result = self.mapOrgAndOrgStructureIdToEisOrgStructureCode.get((orgId, orgStructureId), None)
        if result is None:
            db = QtGui.qApp.db
            record = db.getRecord(db.table('OrgStructure'),
                                  ['tfomsCode', 'parent_id', 'organisation_id'],
                                  orgStructureId)
            if record:
                tfomsCode = forceInt(record.value('tfomsCode'))
                parentId  = forceRef(record.value('parent_id'))
                if not orgId:
                    orgId = forceRef(record.value('organisation_id'))
                if tfomsCode:
                    result = tfomsCode
                elif parentId:
                    result = self.getOrgStructureIdentifier2Int(orgId, parentId)
            if result is None:
                result = forceInt(db.translate('Organisation', 'id', orgId, 'tfomsExtCode'))
            self.mapOrgAndOrgStructureIdToEisOrgStructureCode[(orgId, orgStructureId)] = result
        return result



#    def clientDoesNotHaveEISId(self, clientId):
#        asEIS = '2'
#        asEISMU = '3'
#
#        db = QtGui.qApp.db
#        tableClientIdentification = db.table('ClientIdentification')
#        tableAccountingSystem = db.table('rbAccountingSystem')
#        table = tableClientIdentification.leftJoin(tableAccountingSystem, tableAccountingSystem['id'].eq(tableClientIdentification['accountingSystem_id']))
#        cnt = db.getCount(table, where=db.joinAnd([tableClientIdentification['client_id'].eq(clientId),
#                                                   tableClientIdentification['deleted'].eq(0),
#                                                   tableAccountingSystem['code'].inlist((asEIS, asEISMU))
#                                                  ]
#                                                 )
#                         )
#        return cnt == 0


    def getClientAddressParts(self, clientId, addrType):
        addrRecord = self.getAddrRecord(clientId, addrType)
        if not addrRecord and addrType == 0:
            addrRecord = self.getAddrRecord(clientId, 1)

        eisAddrType = u''
        regOkatoId = 0
        houseId = 0
        house = ''
        corpus = ''
        flat = ''
        freeInput = ''
        KLADRCode = ''
        street = ''
        streetTypeId = 0

        if addrRecord:
            KLADRCode=forceString(addrRecord.value('KLADRCode'))
            freeInput = forceString(addrRecord.value('freeInput'))
            street = forceString(addrRecord.value('streetName')) or '-'
            streetType = forceString(addrRecord.value('streetType'))
            streetTypeId = self.streetTypeDict.get(streetType, self.streetTypeDict[''])
            house = forceString(addrRecord.value('number'))
            corpus = forceString(addrRecord.value('corpus'))
            flat = forceString(addrRecord.value('flat'))
            if KLADRCode:
                regOkatoId = int(KLADRCode[:2])
                if KLADRCode.startswith('78'):
                    eisAddrType = u'г'
                    houseId = self.getEisHouseId(addrRecord.value('KLADRCode'), addrRecord.value('KLADRStreetCode'), addrRecord.value('number'), addrRecord.value('corpus'))
                else:
                    eisAddrType = u'р'
                    regOkatoId = self.mapKladrCodeToIdRerion.get(regOkatoId, regOkatoId)
            else:
                eisAddrType = u'п'
        return eisAddrType, regOkatoId, houseId, house, corpus, flat, freeInput, KLADRCode, street, streetTypeId


    def getEisHouseId(self, KLADRCode, KLADRStreetCode, number, corpus):
        db = QtGui.qApp.db
        if corpus == '-':
            corpus = ''
        stmt = 'SELECT kladr.getEisHouseId(%s, %s, %s, %s) AS X' % ( db.formatValueEx(QVariant.String, KLADRCode),
                                                                     db.formatValueEx(QVariant.String, KLADRStreetCode),
                                                                     db.formatValueEx(QVariant.String, number),
                                                                     db.formatValueEx(QVariant.String, corpus)
                                                                   )

        query = db.query(stmt)
        if query.first():
            record=query.record()
            return forceInt(record.value(0))
        else:
            return -1


    def isClientWorking(self, clientId):
        getClientWork(clientId)

# номер новорожденного можно получать как-то так -
    def getNewbornId(self, clientId):
        result = self.mapClientIdToNewbornId.get(clientId)
        if result is None:
            stmt = '''SELECT SQL_NO_CACHE
CA2.client_id FROM
(SELECT CA.type, CA.address_id, CA.freeInput, Client.birthDate
 FROM ClientAddress AS CA
 INNER JOIN Client ON Client.id = CA.client_id
 LEFT JOIN ClientAddress AS CAF ON (CAF.deleted, CAF.type, CAF.client_id) = (0, CA.type, CA.client_id)
                                AND CAF.id>CA.id
 WHERE CA.deleted = 0
   AND CA.type = 1
   AND CA.client_id = %(clientId)d
   AND CAF.id IS NULL
) AS CAS
INNER JOIN ClientAddress AS CA2 ON CA2.type = CAS.type
                                AND CA2.deleted=0
                                AND (CA2.address_id = CAS.address_id OR CA2.freeInput = CAS.freeInput AND CA2.address_id IS NULL AND CAS.address_id IS NULL)
INNER JOIN Client AS Client2 ON Client2.id = CA2.client_id AND Client2.birthDate = CAS.birthDate
LEFT JOIN ClientAddress AS CA2F ON (CA2F.deleted, CA2F.type, CA2F.client_id) = (0, CA2.type, CA2.client_id)
                                AND CA2F.id>CA2.id
WHERE CA2F.id IS NULL
  AND Client2.deleted = 0
ORDER BY CA2.client_id''' % {'clientId':clientId }
            query = QtGui.qApp.db.query(stmt)
            newbornId = 0
            while query.next():
                id = forceInt(query.value(0))
                self.mapClientIdToNewbornId[id] = newbornId = newbornId+1
            result = self.mapClientIdToNewbornId.get(clientId)
            if result is None:
                self.mapClientIdToNewbornId[clientId] = result = 1
        return result


    def isReanimation(self, serviceId):
        result = self.mapServiceIdToSpravGroupNmlkId.get(serviceId, False)
        if result is False:
            result = getIdentification('rbService',
                                       serviceId,
                                       'urn:tfoms78:SPRAV_GROUP_NMKL',
                                       False
                                       )
            self.mapServiceIdToSpravGroupNmlkId[serviceId] = result
        return result


    def getDirectionTypeAndGroup(self, serviceId):
        result = self.mapServiceIdToDirectionTypeAndGroup.get(serviceId, False)
        if result is False:
            groupCode = getIdentification('rbService',
                                          serviceId,
                                          'urn:tfoms78:SPRAV_D_TYPE_GROUP',
                                          False
                                         )
            if groupCode and groupCode.isdigit():
                directionGroup = int(groupCode)
                if directionGroup == 18:
                    directionType = 36
                elif directionGroup == 19:
                    directionType = 37
                else:
                    directionType = 12
            else:
                directionType = directionGroup = None
            self.mapServiceIdToDirectionTypeAndGroup[serviceId] = result = (directionType, directionGroup)
        return result


    def addExtService(self,
                      eventId,
                      actionId
                     ):
        mapPropNameToField = { u'ИВЛ'       : 'V_LONG_IVL',
                               u'Кратность' : 'V_MULTI',
                               u'Мониторинг': 'V_LONG_MON',
                             }

        db = QtGui.qApp.db
        record = db.getRecord('Action', ['begDate', 'endDate'], actionId)
        groupBegDateTime = forceDateTime(record.value('begDate'))
        groupEndDateTime = forceDateTime(record.value('endDate'))
        if not groupBegDateTime:
            groupBegDateTime = QDate(1, 1, 1)
        if not groupEndDateTime:
            groupEndDateTime = QDate(9999, 12, 31)

        tableAction = db.table('Action')
        tableActionType = db.table('ActionType')
        tableActionProperty = db.table('ActionProperty')
        tableActionPropertyType = db.table('ActionPropertyType')
        tableActionPropertyInteger = db.table('ActionProperty_Integer')
        tableService = db.table('rbService')
        tableServiceIdentification = db.table('rbService_Identification')
        tableAccountingSystem = db.table('rbAccountingSystem')

        table = tableAction
        table = table.innerJoin(tableActionType,         tableActionType['id'].eq(tableAction['actionType_id']))
        table = table.innerJoin(tableService,            tableService['id'].eq(tableActionType['nomenclativeService_id']))
        table = table.innerJoin(tableServiceIdentification, tableServiceIdentification['master_id'].eq(tableService['id']))
        table = table.innerJoin(tableAccountingSystem,   tableAccountingSystem['id'].eq(tableServiceIdentification['system_id']))
        table = table.leftJoin(tableActionPropertyType,  [ tableActionPropertyType['actionType_id'].eq(tableAction['actionType_id']),
                                                           tableActionPropertyType['typeName'].eq('Integer'),
                                                           tableActionPropertyType['name'].inlist(mapPropNameToField.keys()),
                                                           tableActionPropertyType['deleted'].eq(0),
                                                         ]
                              )
        table = table.leftJoin(tableActionProperty,      [ tableActionProperty['type_id'].eq(tableActionPropertyType['id']),
                                                           tableActionProperty['action_id'].eq(tableAction['id']),
                                                           tableActionProperty['deleted'].eq(0),
                                                         ]
                              )
        table = table.leftJoin(tableActionPropertyInteger, tableActionPropertyInteger['id'].eq(tableActionProperty['id']))

        cond = [ tableAction['deleted'].eq(0),
                 tableAction['event_id'].eq(eventId),
                 tableAction['endDate'].between(groupBegDateTime, groupEndDateTime),
                 tableServiceIdentification['deleted'].eq(0),
                 tableAccountingSystem['urn'].eq('urn:tfoms78:SPRAV_NMKL'),
               ]

        records = db.getRecordList(table,
                                   [ tableAction['id'],
                                     tableServiceIdentification['value'].alias('nmklId'),
                                     tableAction['begDate'],
                                     tableAction['endDate'],
                                     tableActionPropertyType['name'],
                                     tableActionPropertyInteger['value'],
                                   ],
                                   cond
                                  )
        data = {}
        for record in records:
            id = forceRef(record.value('id'))
            nmklId  = forceInt(record.value('nmklId'))
            begDate = forceDate(record.value('begDate'))
            endDate = forceDate(record.value('endDate'))
            name = forceString(record.value('name'))
            value = forceInt(record.value('value'))
            key = (id, nmklId)
            item = data.setdefault(key, (begDate, endDate, {}))
            item[2][name] = value

        for key, item in data.iteritems():
            id, nmklId = key
            begDate, endDate, values = item
            dbfRecord = self.extServDbf.newRecord()
            dbfRecord['SERV_ID']    = eventId
            dbfRecord['ID_IN_CASE'] = self.mapEventIdToCount[eventId]
            dbfRecord['DATE_BEGIN'] = pyDate(begDate)
            dbfRecord['DATE_END']   = pyDate(endDate)
            dbfRecord['ID_NMKL']    = nmklId
            for propName, fieldName in mapPropNameToField.iteritems():
                value = values.get(propName, None)
                if value:
                    dbfRecord[fieldName] = value
            dbfRecord.store()


    def addExtCase(self, eventId, objectId, objectValue=None, mkb=None):
        if mkb is not None:
            db = QtGui.qApp.db
            assert objectValue is None
            assert isinstance(mkb, basestring)
            mkb = MKBwithoutSubclassification(mkb)
            objectValue = forceInt(db.translate('tfoms78_SPRAV_DIAG', 'DIAG_CODE',  mkb, 'ID_DIAGNOS'))

        dbfRecord = self.extCaseDbf.newRecord()
        dbfRecord['SERV_ID']    = eventId
        dbfRecord['ID_OBJECT']  = objectId
        dbfRecord['OBJ_VALUE']  = objectValue
        dbfRecord['DIAG']       = mkb or ''
        dbfRecord.store()


    def addExtCases(self, eventId):
        mapPropNameToObjectId = { 'ASA'  : 17,
                                  'SOFA1': 1801,
                                  'SOFA2': 1802,
                                  'SOFA3': 1803,
                                  'SOFA4': 1804,
                                  'SOFA5': 1805,
                                  'SOFA6': 1806,
                                }

        db = QtGui.qApp.db
        tableAction = db.table('Action')
        tableActionType = db.table('ActionType')
        tableActionProperty = db.table('ActionProperty')
        tableActionPropertyType = db.table('ActionPropertyType')
        tableActionPropertyString = db.table('ActionProperty_String')

        table = tableActionPropertyString
        table = table.innerJoin(tableActionProperty,     tableActionProperty['id'].eq(tableActionPropertyString['id']))
        table = table.innerJoin(tableActionPropertyType, tableActionPropertyType['id'].eq(tableActionProperty['type_id']))
        table = table.innerJoin(tableAction,             tableAction['id'].eq(tableActionProperty['action_id']))
        table = table.innerJoin(tableActionType,         tableActionType['id'].eq(tableAction['actionType_id']))

        cond = [ tableActionPropertyType['shortName'].inlist(mapPropNameToObjectId.keys()),
                 tableActionPropertyType['deleted'].eq(0),
                 tableActionProperty['deleted'].eq(0),
                 tableAction['deleted'].eq(0),
                 tableActionType['serviceType'].inlist((CActionServiceType.operation,
                                                        CActionServiceType.reanimation,
                                                       )
                                                      ),
                 tableActionPropertyString['value'].ne(''),
                 tableAction['event_id'].eq(eventId)
               ]
        records = db.getRecordList(table,
                                   [ tableAction['id'].alias('action_id'),
                                     tableActionPropertyType['shortName'],
                                     tableActionPropertyString['value'],
                                   ],
                                   cond,
                                   tableAction['endDate'].name()+' desc'
                                  )
        prevActionId = None
        for record in records:
            actionId = forceRef(record.value('action_id'))
            if prevActionId and prevActionId != actionId:
                break
            prevActionId = actionId
            name  = forceString(record.value('shortName'))
            value = forceString(record.value('value'))
            if name == 'ASA':
                value = value[:1]
            objectId = mapPropNameToObjectId.get(name, None)
            if objectId:
                self.addExtCase(eventId, objectId, value)


    def addRehabilitationExtCases(self, eventId):
        db = QtGui.qApp.db
        tableAction     = db.table('Action')
        tableActionType = db.table('ActionType')
        tableService    = db.table('rbService')
        tableServiceIdentification = db.table('rbService_Identification')
        tableAccountingSystem      = db.table('rbAccountingSystem')

        table = tableAction
        table = table.innerJoin(tableActionType,
                                tableActionType['id'].eq(tableAction['actionType_id']))
        table = table.innerJoin(tableService,
                                tableService['id'].eq(tableActionType['nomenclativeService_id']))
        table = table.innerJoin(tableServiceIdentification,
                                tableServiceIdentification['master_id'].eq(tableService['id']))
        table = table.innerJoin(tableAccountingSystem,
                                tableAccountingSystem['id'].eq(tableServiceIdentification['system_id']))

        cond = [ tableAction['deleted'].eq(0),
                 tableAction['event_id'].eq(eventId),
                 tableServiceIdentification['deleted'].eq(0),
                 tableAccountingSystem['urn'].eq('urn:tfoms78:SPRAV_NMKL')
               ]

        records = db.getRecordList(table,
                                   [ tableServiceIdentification['value'],
                                   ],
                                   cond,
                                  )
        for record in records:
            value = forceString(record.value('value'))
            self.addExtCase(eventId, objectId=5, objectValue=value)


    # 0014079: Выгрузка двнных о ШРМ
    def addRehabilitationRoutingScore(self, eventId):
        db = QtGui.qApp.db
        tableAction     = db.table('Action')
        tableActionType = db.table('ActionType')
        tableAPTRrs     = db.table('ActionPropertyType').alias('aptRrs')
        tableAPRrs      = db.table('ActionProperty').alias('apRrs')
        tableAPRrsVal   = db.table('ActionProperty_String').alias('apRrsVal')

        table = tableAction
        table = table.innerJoin(tableActionType,
                                tableActionType['id'].eq(tableAction['actionType_id']))
        table = table.innerJoin(tableAPTRrs,
                                [ tableAPTRrs['actionType_id'].eq(tableActionType['id']),
                                  tableAPTRrs['deleted'].eq(0),
                                  tableAPTRrs['shortName'].eq('rb'),
                                ]
                               )
        table = table.innerJoin(tableAPRrs,
                                [ tableAPRrs['action_id'].eq(tableAction['id']),
                                  tableAPRrs['type_id'].eq(tableAPTRrs['id']),
                                  tableAPRrs['deleted'].eq(0)
                                ]
                               )
        table = table.innerJoin(tableAPRrsVal,
                                tableAPRrsVal['id'].eq(tableAPRrs['id'])
                               )

        cond = [ tableAction['deleted'].eq(0),
                 tableAction['event_id'].eq(eventId),
                 tableActionType['deleted'].eq(0),
                 tableActionType['code'].eq('SHRM'),
                 tableAPRrsVal['value'].regexp('^[ ]*rb[0-9] ')
               ]

        records = db.getRecordList(table,
                                   [ tableAPRrsVal['value'],
                                   ],
                                   cond,
                                   tableAction['endDate'].name()+' desc',
                                   limit = 1
                                  )
        for record in records:
            value = forceString(record.value('value'))
            match = re.match(r'^\s*rb([2-6]) ',  value)
            if match:
                rrs = int(match.group(1))
                self.addExtCase(eventId,
                                objectId    = 28, # значение "Значение ШРМ",
                                objectValue = str(rrs-1)
                               )


    # 0013549: обновление по экспорту счетов
    def getCovidAddInfo(self, eventId):
        db = QtGui.qApp.db
        tableAction        = db.table('Action')
        tableActionType    = db.table('ActionType')
        tableAPTWeight     = db.table('ActionPropertyType').alias('aptWeight')
        tableAPWeight      = db.table('ActionProperty').alias('apWeight')
        tableAPWeightVal   = db.table('ActionProperty_Double').alias('apWeightVal')
        tableAPTSeverity   = db.table('ActionPropertyType').alias('aptSeverity')
        tableAPSeverity    = db.table('ActionProperty').alias('apSeverity')
        tableAPSeverityVal = db.table('ActionProperty_String').alias('apSeverityVal')

        table = tableAction
        table = table.innerJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
        table = table.leftJoin(tableAPTWeight,   [ tableAPTWeight['actionType_id'].eq(tableAction['actionType_id']),
                                                   tableAPTWeight['deleted'].eq(0),
                                                   tableAPTWeight['name'].eq(u'Вес')
                                                 ]
                              )
        table = table.leftJoin(tableAPWeight,    [ tableAPWeight['deleted'].eq(0),
                                                   tableAPWeight['action_id'].eq(tableAction['id']),
                                                   tableAPWeight['type_id'].eq(tableAPTWeight['id'])
                                                 ]
                              )
        table = table.leftJoin(tableAPWeightVal, tableAPWeightVal['id'].eq(tableAPWeight['id']))


        table = table.leftJoin(tableAPTSeverity, [ tableAPTSeverity['actionType_id'].eq(tableAction['actionType_id']),
                                                   tableAPTSeverity['deleted'].eq(0),
                                                   tableAPTSeverity['name'].eq(u'Степень тяжести состояния пациента COVID-19')
                                                 ]
                              )
        table = table.leftJoin(tableAPSeverity,  [ tableAPSeverity['deleted'].eq(0),
                                                   tableAPSeverity['action_id'].eq(tableAction['id']),
                                                   tableAPSeverity['type_id'].eq(tableAPTSeverity['id'])
                                                 ]
                              )
        table = table.leftJoin(tableAPSeverityVal, tableAPSeverityVal['id'].eq(tableAPSeverity['id']))

        cond = [ tableAction['deleted'].eq(0),
                 tableAction['event_id'].eq(eventId),
                 tableActionType['deleted'].eq(0),
                 tableActionType['flatCode'].eq('osmotr'),
               ]
        records = db.getRecordList(table,
                                   [ tableAPWeightVal['value'].alias('weight'),
                                     tableAPSeverityVal['value'].alias('severity')
                                   ],
                                   cond,
                                   tableAction['endDate'].name()+' desc',
                                   limit = 1
                                  )
        if records:
            record = records[0]
            weight = forceDouble(record.value('weight'))
            severity = forceString(record.value('severity'))
            severityId = None
            severityParts = severity.split()
            if severityParts:
                severityCode = severityParts[0]
                if severityCode.isdigit():
                    severityId = int(severityCode)
            if severityId is None:
                severityId = 1
            return weight, severityId
        return 0, 1


    def addCovidAdd(self, eventId, weight, severity):
        dbfRecord = self.covidAddDbf.newRecord()
        dbfRecord['SERV_ID']    = eventId
        dbfRecord['WEI']        = weight
        dbfRecord['IDSEVERITY'] = severity
        dbfRecord.store()


    def addCovidDrugs(self, eventId, severity):
        db = QtGui.qApp.db
        tableAction        = db.table('Action')
        tableActionType    = db.table('ActionType')
        tableAPTNomenclature   = db.table('ActionPropertyType').alias('aptNomenclature')
        tableAPNomenclature    = db.table('ActionProperty').alias('apNomenclature')
        tableAPNomenclatureVal = db.table('ActionProperty_rbNomenclature').alias('apNomenclatureVal')
        tableAPTUnit           = db.table('ActionPropertyType').alias('aptUnit')
        tableAPUnit            = db.table('ActionProperty').alias('apUnit')
        tableAPUnitVal         = db.table('ActionProperty_rbUnit').alias('apUnitVal')
        tableAPTDose           = db.table('ActionPropertyType').alias('aptDose')
        tableAPDose            = db.table('ActionProperty').alias('apDose')
        tableAPDoseVal         = db.table('ActionProperty_Double').alias('apDoseVal')
        tableAPTRoute          = db.table('ActionPropertyType').alias('aptRoute')
        tableAPRoute           = db.table('ActionProperty').alias('apRoute')
        tableAPRouteVal        = db.table('ActionProperty_rbNomenclatureUsingType').alias('apRouteVal')
        tableAPTCount          = db.table('ActionPropertyType').alias('aptCount')
        tableAPCount           = db.table('ActionProperty').alias('apCount')
        tableAPCountVal        = db.table('ActionProperty_Double').alias('apCountVal')

        table = tableAction
        table = table.innerJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
        table = table.leftJoin(tableAPTNomenclature, [ tableAPTNomenclature['actionType_id'].eq(tableAction['actionType_id']),
                                                       tableAPTNomenclature['deleted'].eq(0),
                                                       tableAPTNomenclature['name'].eq(u'ЛСиИМН')
                                                     ]
                              )
        table = table.leftJoin(tableAPNomenclature,  [ tableAPNomenclature['deleted'].eq(0),
                                                       tableAPNomenclature['action_id'].eq(tableAction['id']),
                                                       tableAPNomenclature['type_id'].eq(tableAPTNomenclature['id'])
                                                     ]
                              )
        table = table.leftJoin(tableAPNomenclatureVal, tableAPNomenclatureVal['id'].eq(tableAPNomenclature['id']))
        table = table.leftJoin(tableAPTUnit,         [ tableAPTUnit['actionType_id'].eq(tableAction['actionType_id']),
                                                       tableAPTUnit['deleted'].eq(0),
                                                       tableAPTUnit['name'].eq(u'Код единицы измерения дозы')
                                                     ]
                              )
        table = table.leftJoin(tableAPUnit,          [ tableAPUnit['deleted'].eq(0),
                                                       tableAPUnit['action_id'].eq(tableAction['id']),
                                                       tableAPUnit['type_id'].eq(tableAPTUnit['id'])
                                                     ]
                              )
        table = table.leftJoin(tableAPUnitVal,         tableAPUnitVal['id'].eq(tableAPUnit['id']))
        table = table.leftJoin(tableAPTDose,         [ tableAPTDose['actionType_id'].eq(tableAction['actionType_id']),
                                                       tableAPTDose['deleted'].eq(0),
                                                       tableAPTDose['name'].eq(u'Доза')
                                                     ]
                              )
        table = table.leftJoin(tableAPDose,          [ tableAPDose['deleted'].eq(0),
                                                       tableAPDose['action_id'].eq(tableAction['id']),
                                                       tableAPDose['type_id'].eq(tableAPTDose['id'])
                                                     ]
                              )
        table = table.leftJoin(tableAPDoseVal, tableAPDoseVal['id'].eq(tableAPDose['id']))

        table = table.leftJoin(tableAPTRoute,        [ tableAPTRoute['actionType_id'].eq(tableAction['actionType_id']),
                                                       tableAPTRoute['name'].eq(u'Код пути введения ЛП')
                                                     ]
                              )
        table = table.leftJoin(tableAPRoute,         [ tableAPRoute['deleted'].eq(0),
                                                       tableAPRoute['action_id'].eq(tableAction['id']),
                                                       tableAPRoute['type_id'].eq(tableAPTRoute['id'])
                                                     ]
                              )
        table = table.leftJoin(tableAPRouteVal,        tableAPRouteVal['id'].eq(tableAPRoute['id']))
        table = table.leftJoin(tableAPTCount,        [ tableAPTCount['actionType_id'].eq(tableAction['actionType_id']),
                                                       tableAPTCount['deleted'].eq(0),
                                                       tableAPTCount['name'].eq(u'Количество введений')
                                                     ]
                              )
        table = table.leftJoin(tableAPCount,         [ tableAPCount['deleted'].eq(0),
                                                       tableAPCount['action_id'].eq(tableAction['id']),
                                                       tableAPCount['type_id'].eq(tableAPTCount['id'])
                                                     ]
                              )
        table = table.leftJoin(tableAPCountVal,        tableAPCountVal['id'].eq(tableAPCount['id']))


        cond = [ tableAction['deleted'].eq(0),
                 tableAction['event_id'].eq(eventId),
                 tableActionType['deleted'].eq(0),
                 tableActionType['flatCode'].eq('MedicalSupplies'),
               ]
        records = db.getRecordList(table,
                                   [
                                     tableAction['begDate'].alias('date'),
                                     tableAPNomenclatureVal['value'].alias('nomenclature_id'),
                                     tableAPUnitVal['value'].alias('unit_id'),
                                     tableAPDoseVal['value'].alias('dose'),
                                     tableAPRouteVal['value'].alias('route_id'),
                                     tableAPCountVal['value'].alias('cnt'),
                                   ],
                                   cond,
                                   tableAction['begDate'].name()
                                  )
        drugs = []
        maps = []
        for record in records:
            date           = forceDate(record.value('date'))
            nomenclatureId = forceRef(record.value('nomenclature_id'))
            unitId         = forceRef(record.value('unit_id'))
            dose           = forceDouble(record.value('dose'))
            routeId        = forceRef(record.value('route_id'))
            cnt            = forceDouble(record.value('cnt'))
            if nomenclatureId:
                mapSchemeToIdentificator = self.getSchemeItemIdentificators(nomenclatureId, severity)
                if mapSchemeToIdentificator:
                    drugs.append((date, nomenclatureId, unitId, dose, routeId, cnt, mapSchemeToIdentificator))
                    maps.append(mapSchemeToIdentificator)
        if maps:
            scheme, fullness = self.chooseScheme(maps)
            if scheme:
                for date, nomenclatureId, unitId, dose, routeId, cnt, mapSchemeToIdentificator in drugs:
                    if scheme in mapSchemeToIdentificator:
                        self.addCovidDrug(eventId,
                                          date,
                                          nomenclatureId,
                                          unitId,
                                          dose,
                                          routeId,
                                          cnt,
                                          mapSchemeToIdentificator[scheme],
                                          fullness)


    def getSchemeItemIdentificators(self, nomenclatureId, severity):
        db = QtGui.qApp.db
        tableIdentification = db.table('rbNomenclature_Identification')
        tableAccountingSystem = db.table('rbAccountingSystem')
        table = tableIdentification.innerJoin(tableAccountingSystem,
                                              tableAccountingSystem['id'].eq(tableIdentification['system_id']))
        records = db.getRecordList(table,
                                   [ tableAccountingSystem['urn'],
                                     tableIdentification['value'],
                                   ],
                                   [ tableIdentification['master_id'].eq(nomenclatureId),
                                     tableIdentification['deleted'].eq(0),
                                     tableAccountingSystem['urn'].like('urn:ID_DRUGS:%s-%%' % severity),
                                   ]
                                  )
        mapNumberToIdentificator = {}
        for record in records:
            urn = forceString(record.value('urn'))
            schemeItemIdentificator = forceInt(record.value('value'))
            parts = urn.split('-')
            if len(parts) == 2:
                schemeNumber = forceInt(parts[1])
                mapNumberToIdentificator[schemeNumber] = schemeItemIdentificator
        return mapNumberToIdentificator


    def chooseScheme(self, maps):
        cntUsedSchemes = {}

        for mapSchemeToIdentificator in maps:
            for scheme in mapSchemeToIdentificator.keys():
                cntUsedSchemes[scheme] = cntUsedSchemes.get(scheme, 0)+1
        fullSchemes = [scheme
                       for scheme in cntUsedSchemes
                       if cntUsedSchemes[scheme] == len(maps)
                      ]
        if fullSchemes:
            return min(fullSchemes), True
        scheme, cnt = max( cntUsedSchemes.items(),
                           key = lambda (scheme, cnt): (cnt, -scheme)
                         )
        return scheme, False


    def addCovidDrug(self, eventId, date, nomenclatureId, unitId, dose, routeId, cnt, schemeItem, fullness):
        db = QtGui.qApp.db
        dbfRecord = self.covidDrugsDbf.newRecord()
        dbfRecord['SERV_ID']    = eventId
        dbfRecord['ID_IN_CASE'] = self.mapEventIdToCount[eventId]
        dbfRecord['ID_DRUG_SH'] = schemeItem # Идентификатор кода схемы лекарственной терапии
        dbfRecord['NOTFULLDSH'] = not fullness
        dbfRecord['DATE_INJ']   = pyDate(date)
        dbfRecord['ID_LEK_PR']  = forceInt(getIdentification('rbNomenclature',  nomenclatureId,  'urn:LEK_PR', False))
        dbfRecord['COD_MARK']   = getIdentification('rbNomenclature',  nomenclatureId,  'urn:gtin', False) or ''
        dbfRecord['ID_ED_IZM']  = forceInt(getIdentification('rbUnit', unitId,  'urn:oid:1.2.643.5.1.13.13.11.1358', False))
        dbfRecord['DOSE_INJ']   = dose
        dbfRecord['ID_MET_INJ'] = forceInt(db.translate('rbNomenclatureUsingType', 'id', routeId, 'code'))
        dbfRecord['COL_INJ']    = cnt

        dbfRecord['#Nomen_Id']  = nomenclatureId
        dbfRecord['#Unit_Id']   = unitId
        dbfRecord['#Route_Id']  = routeId

        dbfRecord.store()


    def eventHasResearch(self, eventId):
        db = QtGui.qApp.db
        tableAction = db.table('Action')
        tableActionType = db.table('ActionType')
        table = tableAction.innerJoin(tableActionType,
                                      tableActionType['id'].eq(tableAction['actionType_id']))
        cnt = db.getCount(table,
                          where=db.joinAnd([ tableAction['deleted'].eq(0),
                                             tableAction['event_id'].eq(eventId),
                                             tableActionType['serviceType'].inlist([CActionServiceType.research,
                                                                                    CActionServiceType.labResearch,
                                                                                   ])
                                           ]
                                          )
                         )
        return cnt != 0


    def addDirections(self,
                      hospitalCase,
                      ddCase,
                      checkForRefusalFromDD2,
                      eventId,
                      goalCode,
                      caseCast,
                     ):
        db = QtGui.qApp.db
#        cnt = len(self.directionDbf)
#        refusalDD2 = None
        if hospitalCase:
            table = db.table('vActionLeaved')
            record = db.getRecordEx(table,
                                    '*',
                                    db.joinAnd(['deleted=0',
                                                table['event_id'].eq(eventId)
                                               ]
                                              )
                                   )
            if record:
                actionId = forceRef(record.value('id'))
                outcome = forceString(record.value('propOutcome')).lower()
                hospitalBedProfileId = record.value('propHospitalBedProfle_id')
                if outcome.endswith(u'в дневной стационар'):
                    self.addDirection(eventId,
                                      directionType        = 4,
                                      hospitalBedProfileId = hospitalBedProfileId,
                                      case                 = '10.1',
                                      actionId             = actionId,
                                      caseCast             = caseCast
                                     )
                elif outcome == u'переведен в другой стационар':
#                    self.addDirection(eventId,
#                                      directionType = 5,
#                                      hospitalBedProfileId = hospitalBedProfileId,
#                                      case = '10.2',
#                                      actionId = actionId,
#                                      caseCast = caseCast
#                                     )
                    pass
                elif outcome.endswith((u'в санаторий', u'восстановит лечение')):
                    self.addDirection(eventId,
                                      directionType        = 6,
                                      hospitalBedProfileId = hospitalBedProfileId,
                                      case                 = '10.3',
                                      actionId             = actionId,
                                      caseCast             = caseCast
                                     )
        elif ddCase:
            tableAction = db.table('Action')
            tableActionType = db.table('ActionType')
            tablePerson = db.table('Person')
            tableSpeciality = db.table('rbSpeciality')
            table = tableAction
            table = table.innerJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
            table = table.leftJoin(tablePerson,      tablePerson['id'].eq(tableAction['setPerson_id']))
            table = table.leftJoin(tableSpeciality,  tableSpeciality['id'].eq(tablePerson['speciality_id']))
            for (flatCode, directionType, examinationType) in (
                                                                ('consultationDirection%', 2, None),
                                                                ('hospitalDirection%',     5, None),
                                                                ('inspectionDirection%',   3, 2),
                                                                ('recoveryDirection%',     6, None),
                                                                ('researchDirection%',     3, 3),
                                                              ):
                records = db.getRecordList(table,
                                           'Action.*, rbSpeciality.regionalCode AS specialityCode',
                                            db.joinAnd([ tableAction['deleted'].eq(0),
                                                         tableAction['event_id'].eq(eventId),
                                                         tableActionType['flatCode'].like(flatCode)
                                                       ]
                                                      )
                                          )
                for record in records:
                    actionId = forceRef(record.value('id'))
                    action = CAction(record=record)
                    date = forceDate(record.value('begDate'))
                    plannedDate = forceDate(record.value('plannedEndDate'))
                    lpuIdTuple = ( self.getOrgIdentifier(self.currentOrgId, True), 0)
                    directionOrgId = action.get(u'Целевая МО')
                    offsideLpuId = self.getOffsideLpuId(directionOrgId)
                    if offsideLpuId is None:
                        targetLpuIdTuple = ( self.getOrgIdentifier(directionOrgId, False),
                                             0
                                           )
                    else:
                        targetLpuIdTuple = ( 20578,  # что соответствует по справочнику LPU в ЕИС Иногородней МО
                                             forceInt(toVariant(offsideLpuId))
                                           )

                    targetSpecialityCode = None
                    hospitalBedProfileId = None

                    if directionType in (2, 3, 6):
                       targetSpecialityId = action.get(u'Профиль')
                       targetSpecialityCode = forceInt(db.translate('rbSpeciality', 'id', targetSpecialityId, 'regionalCode'))
                    elif directionType in (5,):
                        hospitalBedProfileId = action.get(u'Профиль'),
                    if directionType == 2:
                        if directionOrgId == self.currentOrgId:
                            directionType = 1

                    self.addDirection(eventId,
                                      directionType        = directionType,
                                      idLpuTuple           = lpuIdTuple,
                                      number               = action.get(u'Номер'),
                                      date                 = date,
                                      targetIdLpuTuple     = targetLpuIdTuple,
                                      targetSpecialityCode = targetSpecialityCode,
                                      plannedDate          = plannedDate or (date.addDays(14) if date else None),
                                      hospitalBedProfileId = hospitalBedProfileId,
                                      examinationType      = examinationType,
                                      goalCode             = goalCode,
                                      personId             = forceRef(record.value('setPerson_id')),
                                      specialityCode       = forceInt(record.value('specialityCode')),
                                      case                 = '11',
                                      actionId             = actionId,
                                      caseCast             = caseCast
                                     )

#            if cnt == len(self.directionDbf):
#                self.addDirection(eventId,
#                                  directionType = 9 # без направления
#                                  caseCast      = caseCast
#                                 )

            if checkForRefusalFromDD2:
                refusalDD2 = db.getCount(table,
                                         '1',
                                         db.joinAnd([ tableAction['deleted'].eq(0),
                                                      tableAction['event_id'].eq(eventId),
                                                      tableActionType['flatCode'].eq('refusal')
                                                    ]
                                                   )
                                         )
                if refusalDD2:
                    self.addDirection(eventId,
                                      directionType = 12,  # отказ от ДД2
                                      case          = '12',
                                      caseCast      = caseCast
                                     )
                else:
                    self.addDirection(eventId,
                                      directionType = 14,  # согласие на ДД2
                                      case          = '13',
                                      caseCast      = caseCast
                                     )


    def addDirection(self,
                     eventId,
                     directionGroup = None,
                     directionType = 0,
                     number = None,
                     date = None,
                     plannedDate = None,
                     hospitalBedProfileId = None,
                     examinationType = None,
                     idLpuTuple = None,
                     targetIdLpuTuple = None,
                     specialityCode = None,
                     targetSpecialityCode = None,
                     dispensaryObservationCode = None,
                     goalCode = None,
                     mkb = None,
                     nmklCode = None,
                     personId = None,
                     case     = None,
                     actionId = None,
                     caseCast = None,
                    ):
        db = QtGui.qApp.db

        # 0014413: ТФОМС СПб. Выгрузка данных о направлении к онкологу файл _D (Диспансеризация CASE_CAST=10)
        if caseCast == 10 and directionGroup == 15 and directionType == 22:
            # не нужно выгружать строку с ID_D_GROUP = 15 и ID_D_TYPE = 22
            return
        # 0015163: Выгрузка данных в файл *_D.dbf Группы ID_D_DROUP = 8 при CASE_CAST =13
        if caseCast == 13 and directionGroup == 8:
            # строку с ID_D_GROUP = 8 и CASE_CAST = 13 не записывать
            return

        if directionGroup is None:
            directionGroup = self.mapDirectionTypeToGroup.get(directionType, 0)
        if hospitalBedProfileId:
            medicalAidProfileId = db.translate('rbHospitalBedProfile', 'id', hospitalBedProfileId, 'medicalAidProfile_id')
            profileCode = forceRef(db.translate('rbMedicalAidProfile', 'id',  medicalAidProfileId, 'regionalCode'))
        else:
            profileCode = None


        dbfRecord = self.directionDbf.newRecord()
        dbfRecord['SERV_ID']    = eventId
        dbfRecord['ID_IN_CASE'] = self.mapEventIdToCount[eventId]
        dbfRecord['ID_D_TYPE']  = directionType
        dbfRecord['ID_D_GROUP'] = directionGroup

        if number is not None:
            assert isinstance(number, basestring)
            dbfRecord['D_NUMBER'] = number
        if date is not None:
            assert isinstance(date, QDate)
            dbfRecord['DATE_ISSUE'] = pyDate(date)
        if plannedDate is not None:
            assert isinstance(plannedDate, QDate)
            dbfRecord['DATE_PLANG'] = pyDate(plannedDate)
        if examinationType is not None:
            assert isinstance(examinationType, (int, long))
            dbfRecord['ID_OB_TYPE'] = examinationType
        if profileCode is not None:
            assert isinstance(profileCode, (int, long))
            dbfRecord['ID_PRMP'] = profileCode
        if idLpuTuple is not None:
            assert isinstance(idLpuTuple, (tuple, list)) and len(idLpuTuple)==2
            dbfRecord['ID_LPU_F'], dbfRecord['ID_LPU_RF'] = idLpuTuple
        if targetIdLpuTuple is not None:
            assert isinstance(targetIdLpuTuple, (tuple, list)) and len(targetIdLpuTuple)==2
            dbfRecord['ID_LPU_T'], dbfRecord['IDLPURF_TO'] = targetIdLpuTuple
        if specialityCode is not None:
            assert isinstance(specialityCode, (int, long))
#            dbfRecord['ID_PRVS'] = specialityCode
            if personId:
                dbfRecord['IDDOCPRVS'] = specialityCode
        if targetSpecialityCode is not None:
            assert isinstance(targetSpecialityCode, (int, long))
            dbfRecord['ID_PRVS'] = targetSpecialityCode

        if dispensaryObservationCode is not None:
            assert isinstance(dispensaryObservationCode,  (int, long))
            dbfRecord['ID_DN'] = dispensaryObservationCode
        if goalCode is not None:
            assert isinstance(goalCode, (int, long))
            dbfRecord['ID_GOAL'] = goalCode
        if mkb is not None:
            assert isinstance(mkb, basestring)
            mkb = MKBwithoutSubclassification(mkb)
            dbfRecord['ID_DIAGNOS'] = forceInt(db.translate('tfoms78_SPRAV_DIAG', 'DIAG_CODE',  mkb, 'ID_DIAGNOS'))
            dbfRecord['DIAG']       = mkb
        if nmklCode is not None:
            assert isinstance(nmklCode, (int, long))
            dbfRecord['ID_NMKL'] = nmklCode
        if personId is not None:
            assert isinstance(personId, (int, long))
            dbfRecord['ID_DOC'] = self.getPersonIdentifier(personId)
        if case is not None:
            assert isinstance(case, basestring)
            dbfRecord['CASE'] = case
        if actionId is not None:
            assert isinstance(actionId, (int, long))
            dbfRecord['ACTION_ID'] = actionId
        dbfRecord.store()
        if directionGroup == 15: # 15 - онкология
            self.directionToFix.setdefault(pyDate(date), []).append(dbfRecord)


    # В соответствии с #9848:28043 исправляем записи направлений, чтобы даты направлений и ID_IN_CASE
    # соответствовали основным записям услуги
    def fixDirections(self, mainServiceDbfRecord):
        date = mainServiceDbfRecord['DATEOUT']
        directionDbfRecords = self.directionToFix.get(date)
        if directionDbfRecords:
            seqNum = mainServiceDbfRecord['ID_IN_CASE']
            for directionDbfRecord in directionDbfRecords:
                directionDbfRecord['ID_IN_CASE'] = seqNum
                directionDbfRecord.store()
            del self.directionToFix[date]


    def fixDirectionsAtEventFinish(self):
        if self.directionToFix:
            mainServiceDbfRecord = self.dbf[len(self.dbf)-1]
            date = mainServiceDbfRecord['DATEOUT']
            seqNum = mainServiceDbfRecord['ID_IN_CASE']
            for directionDbfRecords in self.directionToFix.values():
                for directionDbfRecord in directionDbfRecords:
                    directionDbfRecord['DATE_ISSUE'] = date
                    directionDbfRecord['ID_IN_CASE'] = seqNum
                    directionDbfRecord.store()


    def serviceRepetionCount(self, eventId, serviceCode):
        db = QtGui.qApp.db
        tableAccountItem = db.table('Account_Item')
        tableService     = db.table('rbService')
        table = tableAccountItem
        table = table.innerJoin(tableService, tableService['id'].eq(tableAccountItem['service_id']))
        cond = [ tableAccountItem['id'].inlist(self.idList),
                 tableAccountItem['event_id'].eq(eventId),
                 tableService['infis'].eq(serviceCode),
               ]
        return db.getCount(table, '1', cond)


    def getHospitalBedProfile(self, eventId, medicalAidProfileId):
        cachedEventId, cachedHospitalBedProfileCode = self.cachedLeaveHospitalBedProfileForEventId or (None,  None)
        if eventId == cachedEventId:
            return cachedHospitalBedProfileCode

        db = QtGui.qApp.db
        hospitalBedProfileId = None
        for tableName in ('vActionLeaved', 'vActionMoving'):
            table = db.table(tableName)
            hospitalBedProfileIdList = db.getIdList(table,
                                                    idCol='propHospitalBedProfle_id',
                                                    where=db.joinAnd([table['deleted'].eq(0),
                                                                      table['event_id'].eq(eventId),
                                                                     ]),
                                                    order='id desc',
                                                    limit=1)
            if hospitalBedProfileIdList:
                hospitalBedProfileId = hospitalBedProfileIdList[0]
                if hospitalBedProfileId:
                    break
        if not hospitalBedProfileId and medicalAidProfileId:
            hospitalBedProfileId = forceRef(db.translate('rbHospitalBedProfile', 'medicalAidProfile_id', medicalAidProfileId, 'id'))
        if hospitalBedProfileId:
            hospitalBedProfileCodeAsStr = getIdentification('rbHospitalBedProfile',
                                                            hospitalBedProfileId,
                                                            'urn:tfoms78:SPRAV_BED_PROFILE',
                                                            True
                                                           )
            try:
                hospitalBedProfileCode = int(hospitalBedProfileCodeAsStr)
            except:
                hospitalBedProfileCode = 0
        else:
            hospitalBedProfileCode = 0
        self.cachedLeaveHospitalBedProfileForEventId = (eventId, hospitalBedProfileCode)
        return hospitalBedProfileCode


    #0009848: ТФОМС СПб. Изменения согласно 59 приказу ФФОМС. Подозрение на онкологию.
    def cancerSuspected(self, eventId):
        # Если в заключительном, основном или сопутствующем диагнозе
        # (Diagnostic.diagnosisType_id --> rbDiagnosisType.code IN (1,2,9)) указан
        # диагноз с кодом МКБ, начинающимся на "C" и нейтропении
        # (код диагноза по МКБ-10 D70 с сопутствующим диагнозом C00-C80 или C97),
        # а также фаза заболевания - подозрение (Diagnostic.phase_id --> rbDiseasePhases.code = 10)
        db = QtGui.qApp.db

        tableDiagnostic    = db.table('Diagnostic')
        tableDiagnosis     = db.table('Diagnosis')
        tableDiagnosisType = db.table('rbDiagnosisType')
        tableDiseasePhases = db.table('rbDiseasePhases')
        tableConDiagnostic    = db.table('Diagnostic').alias('ConDiagnostic')
        tableConDiagnosis     = db.table('Diagnosis').alias('ConDiagnosis')
        tableConDiagnosisType = db.table('rbDiagnosisType').alias('rbConDiagnosisType')

        table = tableDiagnostic
        table = table.innerJoin(tableDiagnosis,       tableDiagnosis['id'].eq(tableDiagnostic['diagnosis_id']))
        table = table.innerJoin(tableDiagnosisType,   tableDiagnosisType['id'].eq(tableDiagnostic['diagnosisType_id']))
        table = table.leftJoin(tableDiseasePhases,    tableDiseasePhases['id'].eq(tableDiagnostic['phase_id']))
        table = table.leftJoin(tableConDiagnostic,    tableConDiagnostic['event_id'].eq(tableDiagnostic['event_id']))
        table = table.leftJoin(tableConDiagnosis,     tableConDiagnosis['id'].eq(tableConDiagnostic['diagnosis_id']))
        table = table.leftJoin(tableConDiagnosisType, tableConDiagnosisType['id'].eq(tableConDiagnostic['diagnosisType_id']))

        cnt = db.getCount(table,
                          countCol='1',
                          where=db.joinAnd([ tableDiagnostic['deleted'].eq(0),
                                             tableDiagnostic['event_id'].eq(eventId),
                                             tableDiagnosisType['code'].inlist(('1', '2', '9')),
                                             db.joinOr([
                                                        tableDiagnosis['MKB'].eq('Z03.1'),
                                                        db.joinAnd([
                                                                    db.joinOr([ tableDiagnosis['MKB'].like('C%'),
                                                                                tableDiagnosis['MKB'].like('D0%'),
                                                                                db.joinAnd([ tableDiagnosis['MKB'].like('D70%'),
                                                                                             tableConDiagnostic['deleted'].eq(0),
                                                                                             db.joinOr([ tableConDiagnosis['MKB'].between('C00', 'C80.99'),
                                                                                                         tableConDiagnosis['MKB'].like('C97%')
                                                                                                       ]),
                                                                                             tableConDiagnosisType['code'].eq('9')
                                                                                           ]
                                                                                          )
                                                                              ]
                                                                             ),
                                                                    tableDiseasePhases['code'].eq('10') # подозрение
                                                                   ]
                                                                  ),
                                                       ]
                                                      )
                                           ]
                                          )
                         )
        return cnt != 0


    # наблюдение пациента с онк. заболеванием
    def cancerObservation(self, eventId):
        # Если в заключительном, основном или сопутствующем диагнозе
        # (Diagnostic.diagnosisType_id --> rbDiagnosisType.code IN (1,2,9)) указан
        # диагноз с кодом МКБ, начинающимся на "C" и нейтропении
        # (код диагноза по МКБ-10 D70 с сопутствующим диагнозом C00-C80 или C97),
        # а также без фазы или или с фазой, отличающейся от "Подозрения" (Diagnostic.phase_id --> rbDiseasePhases.code != 10)
        db = QtGui.qApp.db

        tableDiagnostic    = db.table('Diagnostic')
        tableDiagnosis     = db.table('Diagnosis')
        tableDiagnosisType = db.table('rbDiagnosisType')
        tableDiseasePhases = db.table('rbDiseasePhases')
        tableConDiagnostic    = db.table('Diagnostic').alias('ConDiagnostic')
        tableConDiagnosis     = db.table('Diagnosis').alias('ConDiagnosis')
        tableConDiagnosisType = db.table('rbDiagnosisType').alias('rbConDiagnosisType')

        table = tableDiagnostic
        table = table.innerJoin(tableDiagnosis,       tableDiagnosis['id'].eq(tableDiagnostic['diagnosis_id']))
        table = table.innerJoin(tableDiagnosisType,   tableDiagnosisType['id'].eq(tableDiagnostic['diagnosisType_id']))
        table = table.leftJoin(tableDiseasePhases,    tableDiseasePhases['id'].eq(tableDiagnostic['phase_id']))
        table = table.leftJoin(tableConDiagnostic,    tableConDiagnostic['event_id'].eq(tableDiagnostic['event_id']))
        table = table.leftJoin(tableConDiagnosis,     tableConDiagnosis['id'].eq(tableConDiagnostic['diagnosis_id']))
        table = table.leftJoin(tableConDiagnosisType, tableConDiagnosisType['id'].eq(tableConDiagnostic['diagnosisType_id']))

        cnt = db.getCount(table,
                          countCol='1',
                          where=db.joinAnd([ tableDiagnostic['deleted'].eq(0),
                                             tableDiagnostic['event_id'].eq(eventId),
                                             tableDiagnosisType['code'].inlist(('1', '2', '9')),
                                             db.joinAnd([
                                                         db.joinOr([ tableDiagnosis['MKB'].like('C%'),
                                                                     tableDiagnosis['MKB'].like('D0%'),
                                                                     db.joinAnd([ tableDiagnosis['MKB'].like('D70%'),
                                                                                  tableConDiagnostic['deleted'].eq(0),
                                                                                  db.joinOr([ tableConDiagnosis['MKB'].between('C00', 'C80.99'),
                                                                                              tableConDiagnosis['MKB'].like('C97%')
                                                                                            ]),
                                                                                  tableConDiagnosisType['code'].eq('9')
                                                                                ]
                                                                               )
                                                                   ]
                                                                  ),
                                                         db.joinOr([ tableDiseasePhases['id'].isNull(),
                                                                     tableDiseasePhases['code'].ne('10') # подозрение
                                                                   ]
                                                                  ),
                                                        ]
                                                       )
                                           ]
                                          )
                         )
        return cnt != 0


    # Диспансерное наблюдение по поводу онкологии
    def cancerDispensaryObservation(self, eventId):
        # Если в заключительном, основном или сопутствующем диагнозе
        # (Diagnostic.diagnosisType_id --> rbDiagnosisType.code IN (1,2,9)) указан
        # диагноз с кодом МКБ, начинающимся на "C" и нейтропении
        # (код диагноза по МКБ-10 D70 с сопутствующим диагнозом C00-C80 или C97),
        # а также для этого диагноза указан статус ДН с отмеченным параметром "наблюдается" (Diagnostic.dispanser_id --> rbDispanser.observed = 1)
        db = QtGui.qApp.db

        tableDiagnostic    = db.table('Diagnostic')
        tableDiagnosis     = db.table('Diagnosis')
        tableDiagnosisType = db.table('rbDiagnosisType')
        tableDispanser     = db.table('rbDispanser')
        tableConDiagnostic    = db.table('Diagnostic').alias('ConDiagnostic')
        tableConDiagnosis     = db.table('Diagnosis').alias('ConDiagnosis')
        tableConDiagnosisType = db.table('rbDiagnosisType').alias('rbConDiagnosisType')

        table = tableDiagnostic
        table = table.innerJoin(tableDiagnosis,       tableDiagnosis['id'].eq(tableDiagnostic['diagnosis_id']))
        table = table.innerJoin(tableDiagnosisType,   tableDiagnosisType['id'].eq(tableDiagnostic['diagnosisType_id']))
        table = table.leftJoin(tableDispanser,        tableDispanser['id'].eq(tableDiagnostic['dispanser_id']))
        table = table.leftJoin(tableConDiagnostic,    tableConDiagnostic['event_id'].eq(tableDiagnostic['event_id']))
        table = table.leftJoin(tableConDiagnosis,     tableConDiagnosis['id'].eq(tableConDiagnostic['diagnosis_id']))
        table = table.leftJoin(tableConDiagnosisType, tableConDiagnosisType['id'].eq(tableConDiagnostic['diagnosisType_id']))

        cnt = db.getCount(table,
                          countCol='1',
                          where=db.joinAnd([ tableDiagnostic['deleted'].eq(0),
                                             tableDiagnostic['event_id'].eq(eventId),
                                             tableDiagnosisType['code'].inlist(('1', '2', '9')),
                                             db.joinAnd([
                                                            db.joinOr([ tableDiagnosis['MKB'].like('C%'),
                                                                        tableDiagnosis['MKB'].like('D0%'),
                                                                        db.joinAnd([ tableDiagnosis['MKB'].like('D70%'),
                                                                                     tableConDiagnostic['deleted'].eq(0),
                                                                                     db.joinOr([ tableConDiagnosis['MKB'].between('C00', 'C80.99'),
                                                                                                 tableConDiagnosis['MKB'].like('C97%')
                                                                                               ]),
                                                                                     tableConDiagnosisType['code'].eq('9')
                                                                                   ]
                                                                                  )
                                                                      ]
                                                                     ),
                                                            tableDispanser['observed'].eq('1') # наблюдается
                                                        ]
                                                       )
                                           ]
                                          )
                         )
        return cnt != 0


#    def afterCancerDispensaryObservation(self, eventId):
#        return self.afterCancer(eventId) # and self.hasDispensaryObservation(eventId)


    def afterCancer(self, eventId):
        # В событии последнее (по дате начала) действие,
        # имеющее логическое свойство c коротким названием anam_cancer (это осмотр)
        # имеет значение этого свойства True
        ########################################################################
        #    SELECT ActionProperty_Boolean.value
        #    FROM Action
        #    INNER JOIN ActionType            ON ActionType.id = Action.actionType_id
        #    INNER JOIN ActionPropertyType    ON ActionPropertyType.actionType_id = Action.actionType_id
        #    LEFT JOIN ActionProperty         ON     ActionProperty.action_id = Action.id
        #                                        AND ActionProperty.type_id = ActionPropertyType.id
        #                                        AND ActionProperty.deleted=0
        #    LEFT JOIN ActionProperty_Boolean ON ActionProperty_Boolean.id = ActionProperty.id
        #    WHERE Action.event_id = ${eventId}
        #      AND Action.deleted = 0
        #      AND ActionType.deleted = 0
        #      AND ActionPropertyType.deleted=0
        #      AND ActionPropertyType.shortName='anam_cancer'
        #      AND ActionPropertyType.typeName = 'Boolean'
        #    ORDER BY Action.begDate DESC;
        db = QtGui.qApp.db
        tableAction = db.table('Action')
        tableActionType = db.table('ActionType')
        tableActionProperty = db.table('ActionProperty')
        tableActionPropertyType  = db.table('ActionPropertyType')
        tableActionPropertyValue = db.table('ActionProperty_Boolean')

        table = tableAction
        table = table.innerJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
        table = table.innerJoin(tableActionPropertyType, tableActionPropertyType['actionType_id'].eq(tableAction['actionType_id']))
        table = table.innerJoin(tableActionProperty,     [ tableActionProperty['action_id'].eq(tableAction['id']),
                                                           tableActionProperty['type_id'].eq(tableActionPropertyType['id']),
                                                           tableActionProperty['deleted'].eq(0),
                                                         ]
                               )
        table = table.innerJoin(tableActionPropertyValue, tableActionPropertyValue['id'].eq(tableActionProperty['id']))
        cond = [ tableAction['deleted'].eq(0),
                 tableAction['event_id'].eq(eventId),
                 tableActionType['deleted'].eq(0),
                 tableActionPropertyType['deleted'].eq(0),
                 tableActionPropertyType['shortName'].eq('anam_cancer'),
                 tableActionPropertyType['typeName'].eq('Boolean'),
               ]
        record = db.getRecordEx(table,
                                tableActionPropertyValue['value'],
                                cond,
                                tableAction['begDate'].name()+' DESC'
                               )
        return forceBool(record.value('value')) if record else False


    def detectDirectionsToConsultationToOncologist(self, eventId, caseCast):
        # 1. В Событии добавлено Направление на консультацию (flatCode = ConsultationDirection),
        #    и в данном действии в Свойстве "Профиль" указана специальность региональным кодом = 349 (rbSpeciality.regionalCode = 349)
        #    или в данном действии в Свойстве "Профиль" указан профиль койки с кодом ЕГИСЗ = 43 (rbHospitalBedProfile.usishCode = 43).
        #    В таком случае добавляем в файл *_D.dbf строку со следующими значениями:
        #    -SERV_ID - Идентификатор события
        #    -DATE_ISSUE - Action.directionDate - Дата выдачи Направления на консультацию
        #    -ID_D_TYPE  - значение 22, что означает "Выдано направление к онкологу"
        #    -ID_D_GROUP - значение 15, что означает "Вид направления (онкология)"
        #    -ERROR - служебное, не заполняем
        #########################################################################
        #    SELECT
        #           Action.event_id,
        #           Action.directionDate,
        #           Action.directionDate
        #    FROM Action
        #    INNER JOIN ActionType            ON ActionType.id = Action.actionType_id
        #    INNER JOIN ActionPropertyType    ON ActionPropertyType.actionType_id = Action.actionType_id
        #    INNER JOIN ActionProperty        ON ActionProperty.action_id = Action.id AND ActionProperty.type_id = ActionPropertyType.id
        #    LEFT  JOIN ActionProperty_rbHospitalBedProfile ON ActionProperty_rbHospitalBedProfile.`id`=ActionProperty.`id`
        #    LEFT  JOIN rbHospitalBedProfile ON rbHospitalBedProfile.`id`=ActionProperty_rbHospitalBedProfile.`value`
        #    LEFT  JOIN ActionProperty_rbSpeciality ON ActionProperty_rbSpeciality.`id`=ActionProperty.`id`
        #    LEFT  JOIN rbSpeciality ON rbSpeciality.`id`=ActionProperty_rbSpeciality.`value`
        #
        #    WHERE Action.event_id = ${eventId}
        #      AND Action.deleted = 0
        #      AND ActionType.deleted = 0
        #      AND ActionType.flatCode kile 'consultationDirection%'
        #      AND ActionPropertyType.deleted = 0
        #      AND ActionPropertyType.name = 'Профиль'
        #      AND ActionProperty.deleted = 0
        #      AND (rbHospitalBedProfile.usishCode = '43' or rbSpeciality.regionalCode = '349'
        #    ORDER BY Action.directionDate
        #########################################################################
        db = QtGui.qApp.db
        tableAction = db.table('Action')
        tableActionType = db.table('ActionType')
        tableActionProperty = db.table('ActionProperty')
        tableActionPropertyType  = db.table('ActionPropertyType')
        tableAPVHosptalBedProfile= db.table('ActionProperty_rbHospitalBedProfile')
        tableHospitalBedProfile  = db.table('rbHospitalBedProfile')
        tableAPVSpeciality       = db.table('ActionProperty_rbSpeciality')
        tableSpeciality          = db.table('rbSpeciality')

        table = tableAction
        table = table.innerJoin(tableActionType,         tableActionType['id'].eq(tableAction['actionType_id']))
        table = table.innerJoin(tableActionPropertyType, tableActionPropertyType['actionType_id'].eq(tableAction['actionType_id']))
        table = table.innerJoin(tableActionProperty,     [ tableActionProperty['action_id'].eq(tableAction['id']),
                                                           tableActionProperty['type_id'].eq(tableActionPropertyType['id']),
                                                         ]
                               )
        table = table.leftJoin(tableAPVHosptalBedProfile, tableAPVHosptalBedProfile['id'].eq(tableActionProperty['id']))
        table = table.leftJoin(tableHospitalBedProfile, tableHospitalBedProfile['id'].eq(tableAPVHosptalBedProfile['value']))
        table = table.leftJoin(tableAPVSpeciality, tableAPVSpeciality['id'].eq(tableActionProperty['id']))
        table = table.leftJoin(tableSpeciality, tableSpeciality['id'].eq(tableAPVSpeciality['value']))

        cond = [ tableAction['deleted'].eq(0),
                 tableAction['event_id'].eq(eventId),
                 tableActionType['deleted'].eq(0),
                 tableActionType['flatCode'].like('consultationDirection%'),
                 tableActionPropertyType['deleted'].eq(0),
                 tableActionPropertyType['name'].eq(u'Профиль'),
                 tableActionProperty['deleted'].eq(0),
                 db.joinOr([tableHospitalBedProfile['usishCode'].eq('43'),
                            tableSpeciality['regionalCode'].eq('349')
                           ]
                          )
               ]
        records = db.getRecordList(table,
                                   [  tableAction['id'].alias('action_id'),
                                      tableAction['directionDate'],
                                      tableAction['plannedEndDate'],
                                   ],
                                   cond,
                                   tableAction['directionDate'].name()
                                  )
        for record in records:
            directionDate = forceDate(record.value('directionDate'))
            plannedDate = forceDate(record.value('plannedEndDate')) or (directionDate.addDays(14) if directionDate else None)
            self.addDirection(eventId,
                              directionGroup = 15,     # что означает "Вид направления (онкология)",
                              directionType  = 22,     # Выдано направление к онкологу
                              date           = directionDate,
                              plannedDate    = plannedDate,
                              case           = '14',
                              actionId       = forceRef(record.value('action_id')),
                              caseCast       = caseCast
                             )


    def detectDirectionsToInspection(self, eventId, caseCast):
        # 2. В Событии добавлено Направление на обследование (flatCode = inspectionDirection),
        #    и в данном действии в Свойстве "Вид направления" указано значение "на биопсию".
        #    В таком случае добавляем в файл *_D.dbf строку со следующими значениями:
        #    -SERV_ID - Идентификатор события
        #    -DATE_ISSUE - Action.directionDate - Дата выдачи Направления на обследование
        #    -ID_D_TYPE - 23, что означает "Выдано направление на биопсию"
        #    -ID_D_GROUP - 15, что означает "Вид направления (онкология)"
        #    -ERROR - служебное, не заполняем
        # 3. В Событии добавлено Направление на обследование (flatCode = inspectionDirection),
        #    и в данном действии в Свойстве "Вид направления" указано любое значение, кроме значения "на биопсию".
        #    В таком случае добавляем в файл *_D.dbf строку со следующими значениями:
        #    -SERV_ID - Идентификатор события
        #    -DATE_ISSUE - Action.directionDate - Дата выдачи Направления на обследование
        #    -ID_D_TYPE - 24, что означает "Выдано направление на дообследование"
        #    -ID_D_GROUP - 15, что означает "Вид направления (онкология)"
        #    -ID_NMKL - Выгружаем код из вкладки Идентификация (справочник tfoms78.NMKL) номенклатурной услуги, привязанной к Типу Действия, который является предыдущим для Направления (prevAction_id --> Action.actionType_id --> ActionType.nomenclativeService_id --> rbService_Identification.value, при rbService_Identification.system_id --> rbAccountingSystem.code = 'tfoms78.NMKL').
        #    -ERROR - служебное, не заполняем
        #########################################################################
        #    SELECT ActionPropertyValue.value,
        #           Action.directionDate,
        #           PrevActionType.nomenclativeService_id
        #    FROM Action
        #    INNER JOIN ActionType            ON ActionType.id = Action.actionType_id
        #    INNER JOIN ActionPropertyType    ON ActionPropertyType.actionType_id = Action.actionType_id
        #    INNER JOIN ActionProperty        ON ActionProperty.action_id = Action.id AND ActionProperty.type_id = ActionPropertyType.id
        #    INNER JOIN ActionProperty_String AS ActionPropertyValue ON ActionPropertyValue.id = ActionProperty.id
        #    LEFT  JOIN Action AS PrevAction  ON PrevAction.id = Action.prevAction_id
        #    LEFT  JOIN ActionType AS PrevActionType ON PrevActionType.id = PrevAction.actionType_id
        #    WHERE Action.deleted = 0
        #      AND Action.event_id = ${eventId}
        #      AND ActionType.deleted = 0
        #      AND ActionType.flatCode = 'inspectionDirection'
        #      AND ActionPropertyType.deleted = 0
        #      AND ActionPropertyType.name = 'Вид направления'
        #      AND ActionProperty.deleted = 0
        #    ORDER BY Action.directionDate
        #########################################################################
        db = QtGui.qApp.db
        tableAction = db.table('Action')
        tableActionType = db.table('ActionType')
        tableActionProperty = db.table('ActionProperty')
        tableActionPropertyType  = db.table('ActionPropertyType')
        tableActionPropertyValue = db.table('ActionProperty_String')

        tablePrevAction = db.table('Action').alias('PrevAction')
        tablePrevActionType = db.table('ActionType').alias('PrevActionType')

        table = tableAction
        table = table.innerJoin(tableActionType,         tableActionType['id'].eq(tableAction['actionType_id']))
        table = table.innerJoin(tableActionPropertyType, tableActionPropertyType['actionType_id'].eq(tableAction['actionType_id']))
        table = table.innerJoin(tableActionProperty,     [ tableActionProperty['action_id'].eq(tableAction['id']),
                                                           tableActionProperty['type_id'].eq(tableActionPropertyType['id']),
                                                         ]
                               )
        table = table.innerJoin(tableActionPropertyValue, tableActionPropertyValue['id'].eq(tableActionProperty['id']))
        table = table.leftJoin(tablePrevAction,          tablePrevAction['id'].eq(tableAction['prevAction_id']))
        table = table.leftJoin(tablePrevActionType,      tablePrevActionType['id'].eq(tablePrevAction['actionType_id']))

        cond = [ tableAction['deleted'].eq(0),
                 tableAction['event_id'].eq(eventId),
                 tableActionType['deleted'].eq(0),
                 tableActionType['flatCode'].eq('inspectionDirection'),
                 tableActionPropertyType['deleted'].eq(0),
                 tableActionPropertyType['name'].eq(u'Вид направления'),
                 tableActionProperty['deleted'].eq(0),
               ]
        records = db.getRecordList(table,
                                   [#  tableAction['id'].alias('action_id'),
                                      tableAction['directionDate'],
                                      tableActionPropertyValue['value'],
                                      tablePrevActionType['nomenclativeService_id'],
                                   ],
                                   cond,
                                   tableAction['directionDate'].name()
                                  )
        for record in records:
            directionDate = forceDate(record.value('directionDate'))
            directionKind = forceString(record.value('value'))
            serviceId     = forceRef(record.value('nomenclativeService_id'))
            if directionKind.lower() == u'на биопсию':
                self.addDirection(eventId,
                                  directionGroup = 15,     # что означает "Вид направления (онкология)",
                                  directionType  = 23,     # "Выдано направление на биопсию"
                                  date           = directionDate,
                                  caseCast       = caseCast
                                 )
            else:
                if serviceId:
                    nmklId = forceInt(getIdentification('rbService', serviceId, 'urn:tfoms78:SPRAV_NMKL'))
                else:
                    nmklId = 1 # отсутствует
                self.addDirection(eventId,
                                  directionGroup = 15,     # что означает "Вид направления (онкология)",
                                  directionType  = 24,     # "Выдано направление на дообследование"
                                  date           = directionDate,
                                  nmklCode       = nmklId,
                                  caseCast       = caseCast
                                 )


    def detectDirectionsToMRI(self, eventId, caseCast):
        # 4. В Событии добавлено Направление на МРТ(КТ) (flatCode = researchDirection).
        #    В таком случае добавляем в файл *_D.dbf строку со следующими значениями:
        #    -SERV_ID - Идентификатор события
        #    -DATE_ISSUE - Action.directionDate - Дата выдачи Направления на МРТ/КТ
        #    -ID_D_TYPE - 24, что означает "Выдано направление на дообследование"
        #    -ID_D_GROUP - 15, что означает "Вид направления (онкология)"
        #    -ID_NMKL - Выгружаем код из вкладки Идентификация (справочник tfoms78.NMKL) номенклатурной услуги, привязанной к Типу Действия, который является предыдущим для Направления (prevAction_id --> Action.actionType_id --> ActionType.nomenclativeService_id --> rbService_Identification.value, при rbService_Identification.system_id --> rbAccountingSystem.code = 'tfoms78.NMKL').
        #    -ERROR - служебное, не заполняем
        #########################################################################
        #    SELECT Action.directionDate,
        #           PrevActionType.nomenclativeService_id
        #    FROM Action
        #    INNER JOIN ActionType            ON ActionType.id = Action.actionType_id
        #    LEFT  JOIN Action AS PrevAction  ON PrevAction.id = Action.prevAction_id
        #    LEFT  JOIN ActionType AS PrevActionType ON PrevActionType.id = PrevAction.actionType_id
        #    LEFT  JOIN rbService             ON rbService.id = PrevActionType.nomenclativeService_id
        #    WHERE Action.deleted = 0
        #      AND Action.event_id in (1548119, 1548120, 1548121, 1548122, 1548123)
        #      AND ActionType.deleted = 0
        #      AND ActionType.flatCode = 'researchDirection'
        #    ORDER BY Action.directionDate
        #########################################################################
        db = QtGui.qApp.db
        tableAction = db.table('Action')
        tableActionType = db.table('ActionType')
        tablePrevAction = db.table('Action').alias('PrevAction')
        tablePrevActionType = db.table('ActionType').alias('PrevActionType')

        table = tableAction
        table = table.innerJoin(tableActionType,      tableActionType['id'].eq(tableAction['actionType_id']))
        table = table.innerJoin(tablePrevAction,      tablePrevAction['id'].eq(tableAction['prevAction_id']))
        table = table.innerJoin(tablePrevActionType,  tablePrevActionType['id'].eq(tablePrevAction['actionType_id']))

        cond = [ tableAction['deleted'].eq(0),
                 tableAction['event_id'].eq(eventId),
                 tableActionType['deleted'].eq(0),
                 tableActionType['flatCode'].eq('researchDirection'),
               ]
        records = db.getRecordList(table,
                                   [#  tableAction['id'].alias('action_id'),
                                      tableAction['directionDate'],
                                      tablePrevActionType['nomenclativeService_id'],
                                   ],
                                   cond,
                                   tableAction['directionDate'].name()
                                  )
        for record in records:
            directionDate = forceDate(record.value('directionDate'))
            serviceId     = forceRef(record.value('nomenclativeService_id'))
            if serviceId:
                nmklId = forceInt(getIdentification('rbService', serviceId, 'urn:tfoms78:SPRAV_NMKL'))
            else:
                nmklId = 1 # Отсутствует
            self.addDirection(eventId,
                              directionGroup = 15,     # что означает "Вид направления (онкология)",
                              directionType  = 24,     # "Выдано направление на дообследование"
                              date           = directionDate,
                              nmklCode       = nmklId,
                              caseCast       = caseCast
                             )


    # 0009932: ТФОМС СПб. Изменения согласно 59 приказу ФФОМС. Лечение ЗНО.
    # 0010281: ТФОМС СПб. Приказ №200 (ЗНО). Версия декабрь 2018
    def getCancerCureDiagnoses(self, eventId):
        # Если в заключительном, основном или сопутствующем диагнозе
        # (Diagnostic.diagnosisType_id --> rbDiagnosisType.code IN (1,2,9)) указан
        # диагноз с кодом МКБ, начинающимся на "C" и нейтропении
        # (код диагноза по МКБ-10 D70 с сопутствующим диагнозом C00-C80 или C97)
        db = QtGui.qApp.db

        tableDiagnostic    = db.table('Diagnostic')
        tableDiagnosis     = db.table('Diagnosis')
        tableDiagnosisType = db.table('rbDiagnosisType')
        tableDiseasePhases = db.table('rbDiseasePhases')
        tableDispanser     = db.table('rbDispanser')
        tableConDiagnostic    = db.table('Diagnostic').alias('ConDiagnostic')
        tableConDiagnosis     = db.table('Diagnosis').alias('ConDiagnosis')
        tableDiseaseCharacter = db.table('rbDiseaseCharacter')

        table = tableDiagnostic
        table = table.innerJoin(tableDiagnosis,     tableDiagnosis['id'].eq(tableDiagnostic['diagnosis_id']))
        table = table.innerJoin(tableDiagnosisType, tableDiagnosisType['id'].eq(tableDiagnostic['diagnosisType_id']))
        table = table.leftJoin(tableDiseasePhases,  tableDiseasePhases['id'].eq(tableDiagnostic['phase_id']))
        table = table.leftJoin(tableDispanser,      tableDispanser['id'].eq(tableDiagnostic['dispanser_id']))
        table = table.leftJoin(tableConDiagnostic,  tableConDiagnostic['event_id'].eq(tableDiagnostic['event_id']))
        table = table.leftJoin(tableConDiagnosis,   tableConDiagnosis['id'].eq(tableConDiagnostic['diagnosis_id']))
        table = table.leftJoin(tableDiseaseCharacter, tableDiseaseCharacter['id'].eq(tableConDiagnostic['character_id']))

        records = db.getRecordListGroupBy(table,
                          [ tableDiagnostic['id'].alias('diagnostic_id'),
                            tableDiagnosis['MKB'],
                            tableDiagnosis['morphologyMKB'],
                            tableDiseasePhases['code'].alias('phase_code'),
                            tableDiagnostic['pTNMphase_id'],
                            tableDiagnostic['cTNMphase_id'],
                            tableDiagnostic['pTumor_id'],
                            tableDiagnostic['cTumor_id'],
                            tableDiagnostic['pNodus_id'],
                            tableDiagnostic['cNodus_id'],
                            tableDiagnostic['pMetastasis_id'],
                            tableDiagnostic['cMetastasis_id'],
                            tableDispanser['observed'],
                            tableDiseaseCharacter['code'].alias('character_code'),
                          ],
                          where=db.joinAnd([ tableDiagnostic['deleted'].eq(0),
                                             tableDiagnostic['event_id'].eq(eventId),
                                             db.joinOr([ tableDiagnosis['MKB'].like('C%'),
                                                         tableDiagnosis['MKB'].like('D0%'),
                                                         db.joinAnd([ tableDiagnosis['MKB'].like('D70%'),
                                                                      tableConDiagnostic['deleted'].eq(0),
                                                                      db.joinOr([ tableConDiagnosis['MKB'].between('C00', 'C80.99'),
                                                                                  tableConDiagnosis['MKB'].like('C97%')
                                                                                ]),
                                                                    ]
                                                                   )
                                                       ]
                                                      ),
                                            tableDiagnosisType['code'].inlist(('1', '2', '9')),
                                           ]
                                          ),
                          group=tableDiagnostic['id'].name()
                         )
        result = []
        for record in records:
            for prefix in ('p',  'c',  None):
                if prefix:
                    phaseId = forceRef(record.value(prefix+'TNMphase_id'))
                    if not phaseId:
                        continue # try next prefix
                    tumorId = forceRef(record.value(prefix + 'Tumor_id'))
                    nodusId = forceRef(record.value(prefix + 'Nodus_id'))
                    metastasisId = forceRef(record.value(prefix + 'Metastasis_id'))
                else:
                    phaseId = tumorId = nodusId = metastasisId = None
                diag = CCancerCureDiagnosis(diagnosticId  = forceRef(record.value('diagnostic_id')),
                                            mkb           = forceString(record.value('MKB')),
                                            morpology     = forceString(record.value('morphologyMKB')),
                                            phaseCode     = forceString(record.value('phase_code')),
                                            cTNMphaseId   = phaseId,
                                            cTumorId      = tumorId,
                                            cNodusId      = nodusId,
                                            cMetastasisId = metastasisId,
                                            observed      = forceBool(record.value('observed')),
                                            characterCode = forceString(record.value('character_code')),
                                           )

                result.append( diag )
                break # loop by prefix
        return result


    # (Суммарная очаговая доза) -->
    # Если в Событии присутствует Действие с Плоским кодом 'ControlListOnko'
    # (ActionType.flatCode = 'ControlListOnko'),
    # из Свойств данного Действия подбираем такое,
    # для которого указано краткое наименование 'SOD' (ActionPropertyType.shortName = 'SOD')
    # и выгружаем его значение, если данное свойство заполнено (если не заполнено - выгружаем 0).
    # Масса тела (кг) - Значение берется из action, у которого ActionType. flatCode= ControlListOnko, из свойства с ActionPropertyType.shortName = 'WEI'
    # Рост (см) - Значение берется из action, у которого ActionType. flatCode= ControlListOnko, из свойства с ActionPropertyType.shortName = 'HEI'
    # Площадь поверхности тела (м2) - Значение берется из action, у которого ActionType. flatCode= ControlListOnko, из свойства с ActionPropertyType.shortName = 'BSA'

    def getTotalFocalDoseEtc(self, eventId, mkb):
        db = QtGui.qApp.db
        tableAction = db.table('Action')
        tableActionType = db.table('ActionType')
        tableActionProperty = db.table('ActionProperty')
        tableActionPropertyType  = db.table('ActionPropertyType')
        tableActionPropertyStringValue = db.table('ActionProperty_String')
        tableActionPropertyDoubleValue = db.table('ActionProperty_Double')

        table = tableAction
        table = table.innerJoin(tableActionType,         tableActionType['id'].eq(tableAction['actionType_id']))
        table = table.innerJoin(tableActionPropertyType, tableActionPropertyType['actionType_id'].eq(tableAction['actionType_id']))
        table = table.innerJoin(tableActionProperty,     [ tableActionProperty['action_id'].eq(tableAction['id']),
                                                           tableActionProperty['type_id'].eq(tableActionPropertyType['id']),
                                                         ]
                               )
        table = table.leftJoin(tableActionPropertyDoubleValue, tableActionPropertyDoubleValue['id'].eq(tableActionProperty['id']))
        table = table.leftJoin(tableActionPropertyStringValue, tableActionPropertyStringValue['id'].eq(tableActionProperty['id']))

        cond = [ tableAction['deleted'].eq(0),
                 tableAction['event_id'].eq(eventId),
                 db.joinOr( [ tableAction['MKB'].like(mkb + '%'),
                              tableAction['MKB'].eq(''),
                            ]),
                 tableActionType['deleted'].eq(0),
                 tableActionType['flatCode'].eq('ControlListOnko'),
                 tableActionPropertyType['deleted'].eq(0),
                 tableActionPropertyType['shortName'].inlist(('SOD',
                                                              'WEI',
                                                              'HEI',
                                                              'BSA',
                                                              'DS1_T'
                                                             )
                                                            ),
                 tableActionProperty['deleted'].eq(0),
               ]
        records = db.getRecordList(table,
                                   [ tableActionPropertyType['shortName'].alias('code'),
                                     tableActionPropertyType['typeName'],
                                     tableActionPropertyDoubleValue['value'].alias('doubleValue'),
                                     tableActionPropertyStringValue['value'].alias('stringValue'),
                                   ],
                                   cond,
                                   tableAction['id'].name() + ' DESC',
                                  )
        result = {}
        for record in records:
            code  = forceString(record.value('code'))
            if not record.isNull('doubleValue'):
                value = forceDouble(record.value('doubleValue'))
            else:
                 value = forceString(record.value('stringValue'))
#            typeName = forceString(record.value('typeName'))
#            if typeName == 'Double':
#                value = forceDouble(record.value('doubleValue'))
#            else:
#                value = forceString(record.value('stringValue'))

            if code not in result:
                result[code] = value
        return result


    def getRadiotherapyFractionation(self, eventId, mkb):
        db = QtGui.qApp.db
        tableAction = db.table('Action')
        tableActionTypeGroup = db.table('ActionType').alias('atg')
        tableActionType = db.table('ActionType')
        tableActionProperty = db.table('ActionProperty')
        tableActionPropertyType  = db.table('ActionPropertyType')
        tableActionPropertyValue = db.table('ActionProperty_Integer')

        table = tableAction
        table = table.innerJoin(tableActionType,         tableActionType['id'].eq(tableAction['actionType_id']))
        table = table.innerJoin(tableActionTypeGroup,    tableActionTypeGroup['id'].eq(tableActionType['group_id']))
        table = table.innerJoin(tableActionPropertyType, tableActionPropertyType['actionType_id'].eq(tableAction['actionType_id']))
        table = table.innerJoin(tableActionProperty,     [ tableActionProperty['action_id'].eq(tableAction['id']),
                                                           tableActionProperty['type_id'].eq(tableActionPropertyType['id']),
                                                         ]
                               )
        table = table.innerJoin(tableActionPropertyValue, tableActionPropertyValue['id'].eq(tableActionProperty['id']))

        cond = [ tableAction['deleted'].eq(0),
                 tableAction['event_id'].eq(eventId),
                 db.joinOr( [ tableAction['MKB'].like(mkb + '%'),
                              tableAction['MKB'].eq(''),
                            ]),
                 tableActionType['deleted'].eq(0),
                 tableActionTypeGroup['deleted'].eq(0),
                 tableActionTypeGroup['name'].eq(u'Диапазон фракций'),
                 tableActionPropertyType['deleted'].eq(0),
                 tableActionPropertyType['shortName'].eq('K_FR'),
                 tableActionProperty['deleted'].eq(0),
               ]
        records = db.getRecordList(table,
                                   [ tableActionPropertyValue['value'],
                                   ],
                                   cond,
                                   tableAction['id'].name() + ' DESC',
                                   1
                                  )
        if records:
            return forceInt(records[0].value('value'))
        else:
            return 0


    def onkoChecklistPresent(self, eventId):
        db = QtGui.qApp.db
        tableAction = db.table('Action')
        tableActionType = db.table('ActionType')
        table = tableAction
        table = table.innerJoin(tableActionType, tableActionType['id'].eq(tableAction['actionType_id']))
        return db.getCount( table,
                            '1',
                            db.joinAnd([ tableAction['event_id'].eq(eventId),
                                         tableAction['deleted'].eq(0),
                                         tableActionType['flatCode'].eq('ControlListOnko'),
                                       ])
                          )


    def pickDefaultTMNPartId(self, tableName, MKB, codes):
        db = QtGui.qApp.db
        table = db.table(tableName)
        for diag in (MKB, ''):
            for code in codes:
                candidate = db.getRecordEx(table,
                                           'id',
                                            db.joinAnd([ table['MKB'].eq(diag),
                                                         table['code'].eq(code),
                                                       ]),
                                           'id')
                if candidate:
                    return forceRef(candidate.value('id'))
        return None


    def addOnkoAddRecord(self, eventId, diag):
        # 0010281: ТФОМС СПб. Приказ №200 (ЗНО). Версия декабрь 2018
        db = QtGui.qApp.db
        diagnosticId  = diag.diagnosticId
        mkb           = MKBwithoutSubclassification(diag.mkb)
        morpology     = diag.morpology
        phaseCode     = diag.phaseCode
        cTNMphaseId   = diag.cTNMphaseId
        cTumorId      = diag.cTumorId
        cNodusId      = diag.cNodusId
        cMetastasisId = diag.cMetastasisId
        observed      = diag.observed

        if morpology.startswith('M'):
            morpology = morpology[1:]
        params = self.getTotalFocalDoseEtc(eventId, mkb)
        ds1t = params.get('DS1_T', None)
        if ds1t:
            ds1  = {
                     u'первичное лечение (лечение пациента за исключением прогрессирования и рецидива)': 1941,
                     u'лечение при рецидиве':                                                            1942,
                     u'динамическое наблюдение':                                                         2789,
                     u'диспансерное наблюдение (здоров/ремиссия)':                                       2790,
                     u'диагностика (при отсутствии специфического лечения)':                             3388,
                     u'симптоматическое лечение':                                                        3389,
                   }.get(self.__lc(ds1t), 0)
        else:
            if phaseCode == '3':
                ds1 = 1942 # рецедив
            elif phaseCode == '1':
                ds1 = 1943 # Обострение
            elif observed:
                ds1 = 2790 # Диспансерное наблюдение
            elif not self.onkoChecklistPresent(eventId):
                ds1 = 2789 # Динамическое наблюдение
            else:
                ds1 = 1941 # Первичное лечение

        category = mkb[:3]
        if cTNMphaseId is None:
            cTNMphaseId = self.pickDefaultTMNPartId('rbTNMphase', category, ['0'])
        if cTumorId is None:
            cTumorId = self.pickDefaultTMNPartId('rbTumor', category, ['Tx', 'T0'])
        if cNodusId is None:
            cNodusId = self.pickDefaultTMNPartId('rbNodus', category, ['Nx', 'N0'])
        if cMetastasisId is None:
            cMetastasisId = self.pickDefaultTMNPartId('rbMetastasis', category, ['Mx', 'M0'] )

        dbfRecord = self.onkoAddDbf.newRecord()
        dbfRecord['SERV_ID']    = eventId
        dbfRecord['ID_DIAGNOS'] = forceInt(db.translate('tfoms78_SPRAV_DIAG', 'DIAG_CODE',  mkb, 'ID_DIAGNOS'))
        dbfRecord['ID_MKB_O_T'] = forceInt(db.translate('tfoms78_SPRAV_MKB_O_T', 'O_T_CODE',  mkb, 'ID_MKB_O_T'))
        dbfRecord['ID_MKB_O_M'] = forceInt(db.translate('tfoms78_SPRAV_MKB_O_M', 'O_M_CODE',  morpology, 'ID_MKB_O_M'))
        dbfRecord['DS1_T']      = ds1
        dbfRecord['ID_ST']  = forceInt(getIdentification('rbTNMphase', cTNMphaseId, 'urn:tfoms78:SPRAV_ONK_STAD')) if cTNMphaseId else 0
        dbfRecord['ID_T']   = forceInt(getIdentification('rbTumor',    cTumorId,    'urn:tfoms78:SPRAV_ONK_T')) if cTumorId else 0
        dbfRecord['ID_N']   = forceInt(getIdentification('rbNodus',    cNodusId,    'urn:tfoms78:SPRAV_ONK_N')) if cNodusId else 0
        dbfRecord['ID_M']   = forceInt(getIdentification('rbMetastasis',cMetastasisId,'urn:tfoms78:SPRAV_ONK_M')) if cMetastasisId else 0
        # 8) MTSTZ с типом данных Numeric (6,0) - (Признак выявления отделенных метастазов) -->
        #    1.Заполняется значением 1, если все три условия выполняются:
        #      а.DS1_T имеет значение 1942 или 1943;
        #      b.Diagnostic.cMetastasis_id не пустое;
        #      c.Для поля Diagnostic.cMetastasis_id значение rbMetastasis.code не M0 или Mx.
        #    2.Заполняется значением 0 во всех остальных случаях.
        if (     ds1 in (1942, 1943)
             and cMetastasisId
             and forceString(db.translate('rbMetastasis', 'id', cMetastasisId, 'code')) not in (u'M0', u'Mx')
           ):
            dbfRecord['MTSTZ']    = 1
        else:
            dbfRecord['MTSTZ']    = 0
        dbfRecord['SOD'] = params.get('SOD', 0.0)
        dbfRecord['WEI'] = params.get('WEI', 0.0)
        dbfRecord['HEI'] = params.get('НEI', 0.0)
        dbfRecord['BSA'] = params.get('BSA', 0.0)
        dbfRecord['K_FR']= self.getRadiotherapyFractionation(eventId, mkb)
        if diagnosticId is not None:
            dbfRecord['DIAGNSTCID'] = diagnosticId
        dbfRecord['DIAG'] = mkb
        dbfRecord['MORPHOLOGY'] = morpology
        dbfRecord.store()


    def detectOnkoRejection(self, eventId, caseCast):
        # III. Формируем файл *_D.dbf в случае,
        # если в Действии "Контрольный лист учета" с ActionType.flatCode = 'ControlListOnko'
        # заполнено хотя бы одно из свойств, в "Коротком наименовании" которых указано значение PROT
        # (ActionPropertyType.shortName = 'PROT').
        # Выгружаем в файл *_D.dbf столько строк, сколько заполнено свойств с ActionPropertyType.shortName = 'PROT'.
        # -SERV_ID - Идентификатор События
        # -DATE_ISSUE - выгружаем значение, указанное в Свойстве с "Коротким наименованием" PROT (ActionPropertyType.shortName = 'PROT')
        # -ID_D_TYPE - выгружаем значение, указанное в поле "Описание" Свойства Действия (ActionPropertyType.descr)
        # -ID_D_GROUP - значение 16, что означает "Противопоказания и отказы пациента"
        # -ERROR - служебное, не заполняем
        db = QtGui.qApp.db
        tableAction = db.table('Action')
        tableActionType = db.table('ActionType')
        tableActionProperty = db.table('ActionProperty')
        tableActionPropertyType  = db.table('ActionPropertyType')
        tableActionPropertyValue = db.table('ActionProperty_Date')

        table = tableAction
        table = table.innerJoin(tableActionType,         tableActionType['id'].eq(tableAction['actionType_id']))
        table = table.innerJoin(tableActionPropertyType, tableActionPropertyType['actionType_id'].eq(tableAction['actionType_id']))
        table = table.innerJoin(tableActionProperty,     [ tableActionProperty['action_id'].eq(tableAction['id']),
                                                           tableActionProperty['type_id'].eq(tableActionPropertyType['id']),
                                                         ]
                               )
        table = table.innerJoin(tableActionPropertyValue, tableActionPropertyValue['id'].eq(tableActionProperty['id']))

        cond = [ tableAction['deleted'].eq(0),
                 tableAction['event_id'].eq(eventId),
                 tableActionType['deleted'].eq(0),
                 tableActionType['flatCode'].eq('ControlListOnko'),
                 tableActionPropertyType['deleted'].eq(0),
                 tableActionPropertyType['shortName'].eq('PROT'),
                 tableActionProperty['deleted'].eq(0),
                 tableActionPropertyValue['value'].isNotNull(),
               ]
        records = db.getRecordList(table,
                                   [  tableActionPropertyValue['value'].alias('rejection_date'),
                                      tableActionPropertyType['descr'].alias('rejection_type'),
                                   ],
                                   cond,
                                   tableAction['id'].name(),
                                  )
        for record in records:
            self.addDirection(eventId,
                              directionGroup = 16, # что означает "Противопоказания и отказы пациента"
                              directionType  = forceInt(record.value('rejection_type')),
                              date           = forceDate(record.value('rejection_date')),
                              caseCast       = caseCast
                             )


    def addOnkoDiagnositcs(self,
                           eventId,
                           diagnosticsType,
                           begDate,
                           parameter,
                           value
                          ):
        dbfRecord = self.onkoDiagnosticsDbf.newRecord()
        dbfRecord['SERV_ID']   = eventId
        dbfRecord['DIAG_TIP']  = diagnosticsType
        dbfRecord['TEST_DATE'] = pyDate(begDate)
        dbfRecord['ID_MTEST']  = parameter
        dbfRecord['ID_MTRSLT'] = value
        dbfRecord['REC_RSLT']  = 1
        dbfRecord.store()


    def detectOnkoDiagnosticsEx(self,
                                eventId,
                                actionFlatCode,
                                diagnosticsType,
#                                parameterFieldName,
#                                valueFieldName,
                                mapInfoToValue
                               ):
        db = QtGui.qApp.db
        tableAction = db.table('Action')
        tableActionType = db.table('ActionType')
        tableActionProperty = db.table('ActionProperty')
        tableActionPropertyType  = db.table('ActionPropertyType')
        tableActionPropertyValue = db.table('ActionProperty_String')

        table = tableAction
        table = table.innerJoin(tableActionType,         tableActionType['id'].eq(tableAction['actionType_id']))
        table = table.innerJoin(tableActionPropertyType, tableActionPropertyType['actionType_id'].eq(tableAction['actionType_id']))
        table = table.innerJoin(tableActionProperty,     [ tableActionProperty['action_id'].eq(tableAction['id']),
                                                           tableActionProperty['type_id'].eq(tableActionPropertyType['id']),
                                                         ]
                               )
        table = table.innerJoin(tableActionPropertyValue, tableActionPropertyValue['id'].eq(tableActionProperty['id']))

        cond = [ tableAction['deleted'].eq(0),
                 tableAction['event_id'].eq(eventId),
                 tableActionType['deleted'].eq(0),
                 tableActionType['flatCode'].eq(actionFlatCode),
                 tableActionPropertyType['deleted'].eq(0),
                 tableActionProperty['deleted'].eq(0),
                 tableActionPropertyValue['value'].isNotNull(),
               ]
        records = db.getRecordList(table,
                                   [ tableAction['begDate'],
                                     tableActionPropertyValue['value'].alias('text'),
                                     tableActionPropertyType['descr'].alias('parameter'),
                                   ],
                                   cond,
                                   tableAction['id'].name(),
                                  )
        for record in records:
            begDate   = forceDate(record.value('begDate'))
            parameter = forceInt(record.value('parameter'))
            text      = forceString(record.value('text'))
            value     = mapInfoToValue.get((parameter, text))
            if value is not None:
                self.addOnkoDiagnositcs(eventId,
                                        diagnosticsType,
                                        begDate,
                                        parameter,
                                        value
                                       )


    def detectOnkodiagnostics(self, eventId):
        self.detectOnkoDiagnosticsEx(eventId,
                                     'Gistologia',
                                     1948,
                                     {
                                        ( 508, u'Эпителиальный') : 518,
                                        ( 508, u'Неэпителиальный') : 519,
                                        ( 509, u'Светлоклеточный') : 520,
                                        ( 509, u'Несветлоклеточный') : 521,
                                        ( 510, u'Низкодифференцированная') : 522,
                                        ( 510, u'Умереннодифференцированная') : 523,
                                        ( 510, u'Высокодифференцированная') : 524,
                                        ( 510, u'Не определена') : 525,
                                        ( 511, u'Мелкоклеточный') : 526,
                                        ( 511, u'Немелкоклеточный') : 527,
                                        ( 512, u'Почечноклеточный') : 528,
                                        ( 512, u'Не почечноклеточный') : 529,
                                        ( 513, u'Папиллярный') : 530,
                                        ( 513, u'Фолликулярный') : 531,
                                        ( 513, u'Гюртклеточный') : 532,
                                        ( 513, u'Медуллярный') : 533,
                                        ( 513, u'Анапластический') : 534,
                                        ( 514, u'Базальноклеточный') : 535,
                                        ( 514, u'Не базальноклеточный') : 536,
                                        ( 515, u'Плоскоклеточный') : 537,
                                        ( 515, u'Не плоскоклеточный') : 538,
                                        ( 516, u'Эндометриоидные') : 539,
                                        ( 516, u'Не эндометриоидные') : 540,
                                        ( 517, u'Аденокарцинома') : 541,
                                        ( 517, u'Не аденокарцинома') : 542,
                                     }
                                    )
        self.detectOnkoDiagnosticsEx(eventId,
                                     'Immunohistochemistry',
                                     1949,
                                     {
                                        ( 567, u'Гиперэкспрессия белка HER2') : 579,
                                        ( 567, u'Отсутствие гиперэкспрессии белка HER2') : 580,
                                        ( 567, u'Не определён Исследование не проводилось') : 581,
                                        ( 568, u'Наличие мутаций в гене BRAF') : 582,
                                        ( 568, u'Отсутствие мутаций в гене BRAF') : 583,
                                        ( 569, u'Наличие мутаций в гене c-Kit') : 584,
                                        ( 569, u'Отсутствие мутаций в гене c-Kit') : 585,
                                        ( 569, u'Не определён Исследование не проводилось') : 586,
                                        ( 570, u'Наличие мутаций в гене RAS') : 587,
                                        ( 570, u'Отсутствие мутаций в гене RAS') : 588,
                                        ( 571, u'Наличие мутаций в гене EGFR') : 589,
                                        ( 571, u'Отсутствие мутаций в гене EGFR') : 590,
                                        ( 572, u'Наличие транслокации в генах ALK или ROS1') : 591,
                                        ( 572, u'Отсутствие транслокации в генах ALK и ROS1') : 592,
                                        ( 573, u'Повышенная экспрессия белка PD-L1') : 593,
                                        ( 573, u'Отсутствие повышенной экспрессии белка PD-L1') : 594,
                                        ( 574, u'Наличие рецепторов к эстрогенам') : 595,
                                        ( 574, u'Отсутствие рецепторов к эстрогенам') : 596,
                                        ( 575, u'Наличие рецепторов к прогестерону') : 597,
                                        ( 575, u'Отсутствие рецепторов к прогестерону') : 598,
                                        ( 576, u'Высокий Высокий индекс пролиферативной активности экспрессии Ki-67') : 599,
                                        ( 576, u'Низкий Низкий индекс пролиферативной активности экспрессии Ki-67') : 600,
                                        ( 577, u'Гиперэкспрессия белка HER2') : 601,
                                        ( 577, u'Отсутствие гиперэкспрессии белка HER2') : 602,
                                        ( 578, u'Наличие мутаций в генах BRCA') : 603,
                                        ( 578, u'Отсутствие мутаций в генах BRCA') : 604,
                                     }
                                    )

    # #0009932: ТФОМС СПб. Изменения согласно 59 приказу ФФОМС. Лечение ЗНО.
    #    V. Формируем файл *_ONKO_V.DBF в случае, если в Событие добавлено Действие, у которого
    #    ActionType.flatCode = 'ControlListOnko' и заполнены Свойства из описания ниже.
    #    1) Serv_ID с типом данных Numeric (11,0) - (Идентификатор случая лечения в основном файле импорта услуг) --> Event_ID.
    #    2)ID_IN_CASE с типом данных Numeric (3,0) - (Порядковый номер услуги (записи)) в рамках одного SERV_ID
    #    3)DATE_BEGIN с типом поля (Date) - (Дата начала) --> Action.begDate
    #    4)DATE_END с типом данных (Date) - (Дата окончания) --> Action.endDate
    #    5)ID_PRVS с типом данных Numeric (11,0) - (Идентификатор специальности врача) -->
    #    6)ID_DOC с типом данных Character (20) - (Идентификатор врача (для услуги)) -->
    #    7)PR_CONS с типом данных Numeric (6,0) - (Сведения о проведении консилиума) --> для Действия с ActionType.flatCode = 'ControlListOnko', выбираем свойство с коротким наименованием PR_CONS (ActionPropertyType.shortName = 'PR_CONS'):
    #    1. Если в указанном свойстве выбрано значение "Не проводился" выгружаем 2838.
    #    2. "Определена тактика обследования" выгружаем 1945.
    #    3. "Определена тактика лечения" выгружаем 1946.
    #    4. "Изменена тактика лечения" выгружаем 1947.
    #    8)ID_TLECH с типом данных Numeric (6,0) - (Тип услуги) --> для Действия с ActionType.flatCode = 'ControlListOnko' , выбираем свойство с коротким наименованием ID_TLECH (ActionPropertyType.shortName = 'ID_TLECH'):
    #    1. Если в указанном свойстве выбрано значение "Хирургическое лечение" выгружаем 619.
    #    2. "Лекарственная противоопухолевая терапия" выгружаем 620.
    #    3. "Лучевая терапия" выгружаем 621.
    #    4. "Химиолучевая терапия" выгружаем 622.
    #    9)ID_THIR с типом данных Numeric (6,0) - (Тип хирургического лечения) --> для Действия с ActionType.flatCode = 'ControlListOnko' , выбираем свойство с коротким наименованием ID_THIR (ActionPropertyType.shortName = 'ID_THIR'):
    #    1. Если в указанном свойстве выбрано значение "Первичной опухоли, в том числе с удалением регионарных лимфатических узлов" выгружаем 623.
    #    2. "Метастазов" выгружаем 624.
    #    3. "Симптоматическое" выгружаем 625.
    #    4. "Выполнено хирургическое стадирование (может указываться при раке яичника вместо "1")" выгружаем 626.
    #    5. "Регионарных лимфатических узлов без первичной опухоли" выгружаем 627.
    #    10)ID_TLEK_L с типом данных Numeric (6,0) - (Линия лекарственной терапии) --> для Действия с ActionType.flatCode = 'ControlListOnko', выбираем свойство с коротким наименованием ID_TLEK_L (ActionPropertyType.shortName = 'ID_TLEK_L'):
    #    1. Если в указанном свойстве выбрано значение "Первая линия" выгружаем 628.
    #    2. "Вторая линия" выгружаем 629.
    #    3. "Третья линия" выгружаем 630.
    #    4. "Линия после третьей" выгружаем 631.
    #    11)ID_TLEK_V с типом данных Numeric (6,0) - (Цикл лекарственной терапии) --> для Действия с ActionType.flatCode = 'ControlListOnko', выбираем свойство с коротким наименованием ID_TLEK_V (ActionPropertyType.shortName = 'ID_TLEK_V'):
    #    1. Если в указанном свойстве выбрано значение "Первый цикл линии" выгружаем 632.
    #    2. "Последующие циклы линии (кроме последнего" выгружаем 633.
    #    3. "Последний цикл линии (лечение прервано)" выгружаем 634.
    #    4. "Последний цикл линии (лечение завершено)" выгружаем 635.
    #    12)ID_TLUCH с типом данных Numeric (6,0) - (Тип лучевой терапии) --> для Действия с ActionType.flatCode = 'ControlListOnko', выбираем свойство с коротким наименованием ActionPropertyType.shortName = 'ID_TLUCH':
    #    1. Если в указанном свойстве выбрано значение "Первичной опухоли/ ложа опухоли" выгружаем 636.
    #    2. "Метастазов" выгружаем 637.
    #    3. "Симптоматическая" выгружаем 638.
    #    13)ID_DRUG_SH с типом данных Numeric (11,0) - (Код схемы лекарственной терапии) -->
    #    14)ERROR с типом данных Character (200) - (Служебное поле) --> не заполняем.

    @staticmethod
    def __lc(s):
        if isinstance(s, basestring):
            return trim(s).lower()
        else:
            return s


    def addOnkoServ(self,
                    eventId,
                    begDate = None,
                    endDate = None,
                    personId  = None,
                    specialityCode = None,
                    PR_CONS   = None,
                    ID_TLECH  = None,
                    ID_THIR   = None,
                    ID_TLEK_L = None,
                    ID_TLEK_V = None,
                    ID_TLUCH  = None,
                    ID_DRUG_SH= None,
                    PPTR      = None,
                    ID_NMKL   = None,
                  ):
        cnt = self.mapEventIdToCount[eventId]
        recNo = 1
        if len(self.onkoServDbf)>0:
            dbfRecord = self.onkoServDbf[len(self.onkoServDbf)-1]
            if dbfRecord['SERV_ID'] == eventId and dbfRecord['ID_IN_CASE'] == cnt:
                recNo = dbfRecord['ID_REC']+1

        if personId and specialityCode is None:
            db = QtGui.qApp.db
            specialityId = db.translate('Person', 'id', personId, 'speciality_id')
            specialityCode = forceInt(db.translate('rbSpeciality', 'id', specialityId, 'regionalCode'))

        dbfRecord = self.onkoServDbf.newRecord()
        dbfRecord['SERV_ID']    = eventId
        dbfRecord['ID_IN_CASE'] = cnt
        dbfRecord['ID_REC']     = recNo
        dbfRecord['DATE_BEGIN'] = pyDate(begDate)
        dbfRecord['DATE_END']   = pyDate(endDate)
        dbfRecord['ID_DOC']     = self.getPersonIdentifier(personId)
        dbfRecord['ID_PRVS']    = forceInt(specialityCode)
        dbfRecord['PR_CONS']    = { u'':                                2838,
                                    u'не проводился':                   2838,
                                    u'определена тактика обследования': 1945,
                                    u'определена тактика лечения':      1946,
                                    u'изменена тактика лечения':        1947
                                  }.get(self.__lc(PR_CONS), 0)
        dbfRecord['ID_TLECH']   = { u'хирургическое лечение':                   619,
                                    u'лекарственная противоопухолевая терапия': 620,
                                    u'лучевая терапия':                         621,
                                    u'химиолучевая терапия':                    622,
                                  }.get(self.__lc(ID_TLECH), 0) or \
                                  (2038 if ( isinstance(ID_TLECH, basestring)
                                            and u'неспецифическое' in ID_TLECH.lower())
                                        else 0
                                  )
        dbfRecord['ID_THIR']    = { u'первичной опухоли, в том числе с удалением регионарных лимфатических узлов': 623,
                                    u'метастазов': 624,
                                    u'симптоматическое': 625,
                                    u'выполнено хирургическое стадирование (может указываться при раке яичника вместо "1")': 626,
                                    u'регионарных лимфатических узлов без первичной опухоли': 627,
                                  }.get(self.__lc(ID_THIR), 0)
        dbfRecord['ID_TLEK_L']  = { u'первая линия': 628,
                                    u'вторая линия': 629,
                                    u'третья линия': 630,
                                    u'линия после третьей': 631,
                                  }.get(self.__lc(ID_TLEK_L), 0)
        dbfRecord['ID_TLEK_V']  = { u'первый цикл линии':                          632,
                                    u'последующие циклы линии (кроме последнего)': 633,
                                    u'последний цикл линии (лечение прервано)':    634,
                                    u'последний цикл линии (лечение завершено)':   635,
                                  }.get(self.__lc(ID_TLEK_V), 0)
        dbfRecord['ID_TLUCH']   = {
                                    u'метастазов':637,
                                    u'симптоматическая': 638,
                                  }.get(self.__lc(ID_TLUCH), 0)
        dbfRecord['ID_DRUG_SH'] = {
                                  }.get(ID_DRUG_SH, 0)
        dbfRecord['NOTFULLDSH'] = 1 if dbfRecord['ID_DRUG_SH'] else 0
        dbfRecord['PPTR']       = {
                                    u'проведено': 1,
                                  }.get(self.__lc(PPTR), 0)
        dbfRecord['ID_NMKL']    = ID_NMKL or 0
        dbfRecord.store()


    def detectOnkoServs(self, eventId, defaultPersonId, defaultDate):
        db = QtGui.qApp.db
        tableAction = db.table('Action')
        tableActionType = db.table('ActionType')
        tableActionProperty = db.table('ActionProperty')
        tableActionPropertyType  = db.table('ActionPropertyType')
        tableActionPropertyStringValue = db.table('ActionProperty_String')
        tableActionPropertyServiceValue = db.table('ActionProperty_rbService')

        table = tableAction
        table = table.innerJoin(tableActionType,         tableActionType['id'].eq(tableAction['actionType_id']))
        table = table.innerJoin(tableActionPropertyType, tableActionPropertyType['actionType_id'].eq(tableAction['actionType_id']))
        table = table.innerJoin(tableActionProperty,     [ tableActionProperty['action_id'].eq(tableAction['id']),
                                                           tableActionProperty['type_id'].eq(tableActionPropertyType['id']),
                                                         ]
                               )
        table = table.leftJoin(tableActionPropertyStringValue, tableActionPropertyStringValue['id'].eq(tableActionProperty['id']))
        table = table.leftJoin(tableActionPropertyServiceValue, tableActionPropertyServiceValue['id'].eq(tableActionProperty['id']))

        cond = [ tableAction['deleted'].eq(0),
                 tableAction['event_id'].eq(eventId),
                 tableActionType['deleted'].eq(0),
                 tableActionType['flatCode'].eq('ControlListOnko'),
                 tableActionPropertyType['deleted'].eq(0),
                 tableActionPropertyType['shortName'].inlist(('PR_CONS', 'ID_TLECH', 'ID_THIR', 'ID_TLEK_L', 'ID_TLEK_V', 'ID_TLUCH', 'PPTR', 'ID_NMKL')),
                 tableActionProperty['deleted'].eq(0),
               ]

        records = db.getRecordList(table,
                                   [  tableAction['id'],
                                      tableAction['begDate'],
                                      tableAction['endDate'],
                                      tableAction['person_id'],
                                      tableActionPropertyType['shortName'].alias('propName'),
                                      tableActionPropertyStringValue['value'].alias('valString'),
                                      tableActionPropertyServiceValue['value'].alias('valService_id'),
                                   ],
                                   cond,
                                   tableAction['id'].name(),
                                  )
        prevActionId = None
        actionDescr = {}
        for record in records:
            actionId = forceRef(record.value('id'))
            if prevActionId != actionId:
                if actionDescr:
                    self.addOnkoServ(eventId, **actionDescr)
                    actionDescr = {}
                prevActionId = actionId
                actionDescr['begDate'] = forceDate(record.value('begDate'))
                actionDescr['endDate'] = forceDate(record.value('endDate'))
                actionDescr['personId'] = forceRef(record.value('person_id'))
            propName = forceString(record.value('propName'))
            if propName == 'ID_NMKL':
                serviceId = forceRef(record.value('valService_id'))
                if serviceId:
                    value = forceInt(getIdentification('rbService', serviceId, 'urn:tfoms78:SPRAV_NMKL'))
                else:
                    value = 1 # Отсутствует
            else:
                value = forceString(record.value('valString'))
            actionDescr[propName] = value
        if actionDescr:
            self.addOnkoServ(eventId, **actionDescr)

        if not records:
            self.addOnkoServ(eventId,
                             personId = defaultPersonId,
                             begDate  = defaultDate,
                             endDate  = defaultDate,
                             ID_TLECH = u'Неспецифическое'
                            )

    # #10186:
    #    Заполнение файла по консилиуму (*_ONKO_CONS.DBF):
    #    Если в Событии есть Действие с ActionType.flatCode = Consilium, и в Действии заполнено свойство с описанием ActionPropertyType.descr = "PR_CONS", выгружаем столько строк, сколько нашли таких Действий:
    #    SERV_ID - идентификатор События
    #    ID_PR_CONS - выгружаем по заполнению свойства.
    #    Если заполнено "Не проводился" или свойство пустое, выгружаем 2838
    #    Если заполнено "Определена тактика обследования", выгружаем 1945
    #    Если заполнено "Определена тактика лечения", выгружаем 1946
    #    Если заполнено "Изменена тактика лечения", выгружаем 1947
    #    DATE_CONS - выгружаем Action.endDate действия flatCode = Consilium
    #    ERROR - служебное, не заполняем
    #
    #    Если Действия такого нет, но при этом Событие содержит информацию о лечении ЗНО
    #    или подозрении на ЗНО (в *_ADD.DBF выгружали значения с ID_OBJECT 29 или 30),
    #    следует принудительно выгрузить значение 2838 в поле ID_PR_CONS, в качестве DATE_CONS - event.execDate

    def addOnkoConsilium(self,
                         eventId,
                         date = None,
                         PR_CONS = None,
                        ):
        dbfRecord = self.onkoConsiliumDbf.newRecord()
        dbfRecord['SERV_ID']    = eventId
        dbfRecord['DATE_CONS']  = pyDate(date)
        dbfRecord['ID_PR_CONS'] = { u'':                                2838,
                                    u'не проводился':                   2838,
                                    u'определена тактика обследования': 1945,
                                    u'определена тактика лечения':      1946,
                                    u'изменена тактика лечения':        1947
                                  }.get(self.__lc(PR_CONS), 0)
        dbfRecord.store()


    def detectOnkoConsilium(self, eventId, execDate):
        db = QtGui.qApp.db
        tableAction = db.table('Action')
        tableActionType = db.table('ActionType')
        tableActionProperty = db.table('ActionProperty')
        tableActionPropertyType  = db.table('ActionPropertyType')
        tableActionPropertyValue = db.table('ActionProperty_String')

        table = tableAction
        table = table.innerJoin(tableActionType,         tableActionType['id'].eq(tableAction['actionType_id']))
        table = table.innerJoin(tableActionPropertyType, tableActionPropertyType['actionType_id'].eq(tableAction['actionType_id']))
        table = table.innerJoin(tableActionProperty,     [ tableActionProperty['action_id'].eq(tableAction['id']),
                                                           tableActionProperty['type_id'].eq(tableActionPropertyType['id']),
                                                         ]
                               )
        table = table.leftJoin(tableActionPropertyValue, tableActionPropertyValue['id'].eq(tableActionProperty['id']))

        cond = [ tableAction['deleted'].eq(0),
                 tableAction['event_id'].eq(eventId),
                 tableActionType['deleted'].eq(0),
                 tableActionType['flatCode'].eq('Consilium'),
                 tableActionPropertyType['deleted'].eq(0),
                 tableActionPropertyType['descr'].eq('PR_CONS'),
                 tableActionProperty['deleted'].eq(0),
               ]

        records = db.getRecordList(table,
                                   [  tableAction['endDate'],
                                      tableActionPropertyValue['value'],
                                   ],
                                   cond,
                                   tableAction['id'].name(),
                                  )
        prevLen = len(self.onkoConsiliumDbf)
        for record in records:
            date = forceDate(record.value('endDate'))
            value = forceString(record.value('value'))
            self.addOnkoConsilium(eventId, date, value)
        if prevLen == len(self.onkoConsiliumDbf):
            self.addOnkoConsilium(eventId, execDate, u'Не проводился')


    def getDispensaryObservationDiagnoses(self, eventId):
        db = QtGui.qApp.db
        tableDiagnostic    = db.table('Diagnostic')
        tableDiagnosis     = db.table('Diagnosis')
        tableDiagnosisType = db.table('rbDiagnosisType')
        tableDispanser     = db.table('rbDispanser')
        tableDispanserIdentification = db.table('rbDispanser_Identification')
        tableAccountingSystem        = db.table('rbAccountingSystem')
        table = tableDiagnostic
        table = table.innerJoin(tableDiagnosis,     tableDiagnosis['id'].eq(tableDiagnostic['diagnosis_id']))
        table = table.innerJoin(tableDiagnosisType, tableDiagnosisType['id'].eq(tableDiagnostic['diagnosisType_id']))
        table = table.innerJoin(tableDispanser,      tableDispanser['id'].eq(tableDiagnostic['dispanser_id']))
        table = table.innerJoin(tableDispanserIdentification, tableDispanserIdentification['master_id'].eq(tableDispanser['id']))
        table = table.innerJoin(tableAccountingSystem,        tableAccountingSystem['id'].eq(tableDispanserIdentification['system_id']))

        records = db.getRecordList(table,
                          [ tableDiagnosis['MKB'],
                            tableDiagnostic['setDate'],
                            tableDiagnosis['dispanserBegDate'],
                            tableDiagnosisType['code'].alias('diagnosisTypeCode'),
                            tableDispanserIdentification['value'].alias('obseravationCode'),
                          ],
                          where=db.joinAnd([ tableDiagnostic['deleted'].eq(0),
                                             tableDiagnostic['event_id'].eq(eventId),
                                             tableDiagnosisType['code'].inlist(('1', '2', '9')),
                                             tableDispanserIdentification['deleted'].eq(0),
                                             tableAccountingSystem['urn'].eq('urn:tfoms78:SPRAV_DN_ACTION'),
                                             tableDispanserIdentification['value'].isNotNull()
                                           ]
                                          ),
                          order = tableDiagnosisType['code'].name()
                         )
        result = []
        addedDiagnoses = set()
        for record in records:
            mkb = forceString(record.value('MKB'))
            isMainDiagnosis = forceString(record.value('diagnosisTypeCode')) in ('1', '2')
            if (mkb, isMainDiagnosis) not in addedDiagnoses:
                dispensaryObservationCode = forceInt(record.value('obseravationCode'))
                date = forceDate(record.value('dispanserBegDate')) or forceDate(record.value('setDate'))
                result.append( ( mkb,
                                 isMainDiagnosis,
                                 dispensaryObservationCode,
                                 date if dispensaryObservationCode == 2 else None
                               )
                             )
                addedDiagnoses.add((mkb, isMainDiagnosis))
        return result


    def addFirstlyDetectedChronicDiagnoses(self, eventId, caseCast):
        db = QtGui.qApp.db
        tableDiagnostic       = db.table('Diagnostic')
        tableDiseaseCharacter = db.table('rbDiseaseCharacter')
        tableDiagnosis        = db.table('Diagnosis')
        tableDiagnosisType    = db.table('rbDiagnosisType')
        table = tableDiagnostic
        table = table.innerJoin(tableDiseaseCharacter,
                                tableDiseaseCharacter['id'].eq(tableDiagnostic['character_id'])
                               )
        table = table.innerJoin(tableDiagnosis,
                                tableDiagnosis['id'].eq(tableDiagnostic['diagnosis_id'])
                               )
        table = table.innerJoin(tableDiagnosisType,
                                tableDiagnosisType['id'].eq(tableDiagnostic['diagnosisType_id'])
                               )

        records = db.getRecordList(table,
                          [ tableDiagnosis['MKB'],
                            tableDiagnostic['setDate'],
                            tableDiagnosisType['code'].alias('diagnosisTypeCode'),
                          ],
                          where=db.joinAnd([ tableDiagnostic['deleted'].eq(0),
                                             tableDiagnostic['event_id'].eq(eventId),
                                             tableDiagnosisType['code'].inlist(('1', '2', '9')),
                                             tableDiseaseCharacter['code'].eq('2'),
                                           ]
                                          ),
                          order = tableDiagnosisType['code'].name()
                         )
        addedDiagnoses = set()
        for record in records:
            mkb = forceString(record.value('MKB'))
            setDate = forceDate(record.value('setDate'))
            isMainDiagnosis = forceString(record.value('diagnosisTypeCode')) in ('1', '2')
            if mkb not in addedDiagnoses:
                addedDiagnoses.add(mkb)
                directionGroup = 20
                if isMainDiagnosis:
                    self.addExtCase(eventId,
                                    objectId=6,
                                    objectValue='1',
                                   )
                    directionType = 38
                else:
                    self.addExtCase(eventId,
                                    objectId=7,
                                    mkb=mkb,
                                   )
                    directionType = 39
                self.addDirection(eventId,
                                  directionGroup = directionGroup,
                                  directionType  = directionType,
                                  date           = setDate,
                                  mkb            = mkb,
                                  case           = '15',
                                  caseCast       = caseCast
                                 )


    def isComplete(self):
        return self.done


    def abort(self):
        self.aborted = True


    def updateBtnExport(self):
        exportNotEmpty = ( self.chkIncludeEvents.isChecked()
                           or self.chkIncludeVisits.isChecked()
                           or self.chkIncludeActions.isChecked() )
        eisLpuIdPresent = self.edtEisLpuId.text() != ''
        self.btnExport.setEnabled(exportNotEmpty and eisLpuIdPresent)


    @pyqtSignature('bool')
    def on_chkIncludeEvents_toggled(self, value):
        self.updateBtnExport()


    @pyqtSignature('bool')
    def on_chkIncludeVisits_toggled(self, value):
        self.updateBtnExport()


    @pyqtSignature('bool')
    def on_chkIncludeActions_toggled(self, value):
        self.updateBtnExport()


    @pyqtSignature('const QString&')
    def on_edtEisLpuId_textChanged(self, value):
        self.updateBtnExport()


    @pyqtSignature('')
    def on_btnExport_clicked(self):
        exportClients = self.chkExportClients.isChecked()
        includeEvents = self.chkIncludeEvents.isChecked()
        includeVisits = self.chkIncludeVisits.isChecked()
        includeActions = self.chkIncludeActions.isChecked()
        self.groupByProfile = self.chkGroupByProfile.isChecked()
        self.eisLpuId = self.edtEisLpuId.text().toInt()[0]
        if (includeEvents or includeVisits or includeActions) and self.eisLpuId:
            QtGui.qApp.preferences.appPrefs['EISOMSLpuId'] = toVariant(self.eisLpuId)
            QtGui.qApp.preferences.appPrefs['EISOMSGroupByProfile'] = toVariant(self.groupByProfile)
            QtGui.qApp.preferences.appPrefs['EISOMSExportClients'] = toVariant(exportClients)
            self.export(self.chkIgnoreConfirmation.isChecked(), exportClients, includeEvents, includeVisits, includeActions, self.groupByProfile, self.eisLpuId)


    @pyqtSignature('')
    def on_btnCancel_clicked(self):
        self.abort()


class CExportEISOMSPage2(QtGui.QWizardPage, Ui_ExportEISOMSPage2):
    def __init__(self, parent):
        QtGui.QWizardPage.__init__(self, parent)
        self.setupUi(self)
        self.setTitle(u'Экспорт данных реестра по счёту')
        self.setSubTitle(u'для выполнения шага нажмите кнопку "финиш"')

        self.pathIsValid = True
        homePath = QDir.toNativeSeparators(QDir.homePath())
        exportDir = forceString(QtGui.qApp.preferences.appPrefs.get('EISOMSExportDir', homePath))
        self.edtDir.setText(exportDir)


    def isComplete(self):
        return self.pathIsValid


    def validatePage(self):
        success = True
        destDir = forceStringEx(self.edtDir.text())
        for suffix in ('', '_V', '_VDOC', '_ADD', '_D', '_ONKO_ADD', '_ONKO_V', '_ONKO_MT', '_ONKO_CONS', '_ONKO_LEK', '_COVID_ADD', '_COVID_LEK', '_MED_DEV'):
            if success:
                src = self.wizard().getFullDbfFileName(suffix)
                if os.path.isfile(src):
                    dst = os.path.join(destDir, os.path.basename(src))
                    success, result = QtGui.qApp.call(self, shutil.move, (src, dst))
        if success:
                src = self.wizard().getFullClientsDbfFileName()
                if os.path.isfile(src):
                    dst = os.path.join(destDir, os.path.basename(src))
                    success, result = QtGui.qApp.call(self, shutil.move, (src, dst))

                    src = self.wizard().getFullClientsDbtFileName()
                    if os.path.isfile(src):
                        dst = os.path.join(destDir, os.path.basename(src))
                        success, result = QtGui.qApp.call(self, shutil.move, (src, dst))
        if success:
            QtGui.qApp.preferences.appPrefs['EISOMSExportDir'] = toVariant(self.edtDir.text())
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
                u'Выберите директорий для сохранения файла выгрузки в ЕИС-ОМС',
                 forceStringEx(self.edtDir.text()),
                 QtGui.QFileDialog.ShowDirsOnly)
        if forceString(dir):
            self.edtDir.setText(QDir.toNativeSeparators(dir))


CCancerCureDiagnosis = namedtuple('CCancerCureDiagnosis',
                  (
                    'diagnosticId',
                    'mkb',
                    'morpology',
                    'phaseCode',
                    'cTNMphaseId',
                    'cTumorId',
                    'cNodusId',
                    'cMetastasisId',
                    'observed',
                    'characterCode',
                  )
                 )

