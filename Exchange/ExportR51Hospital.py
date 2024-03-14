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

u"""Экспорт реестра стационарной и стационарзамещающей медицинской помощи.
    Мурманск"""

import os.path

from PyQt4 import QtGui
from PyQt4.QtCore import QDate

from library.dbfpy.dbf import Dbf
from library.Utils     import (forceBool, forceInt, forceRef, forceString,
    pyDate, toVariant, firstMonthDay, formatSNILS, forceDouble)

from Events.Action import CAction
from Events.ActionServiceType import CActionServiceType
from Exchange.Export import (CExportHelperMixin, CAbstractExportWizard,
                                    CAbstractExportPage1, CAbstractExportPage2)
from Exchange.ExportR51OMS import (getIdsp, mapDiagRslt, getOnkologyInfo,
                                   forceDate, createServTmtDbf)

from Exchange.Ui_ExportR51HospitalPage1 import Ui_ExportPage1


def exportR51Hospital(widget, accountId, accountItemIdList, _=None):
    u"""Создает диалог экспорта реестра счета"""

    wizard = CExportWizard(widget)
    wizard.setAccountId(accountId)
    wizard.setAccountItemsIdList(accountItemIdList)
    wizard.exec_()

# ******************************************************************************

class CExportWizard(CAbstractExportWizard):
    u"""Мастер экспорта в ОМС Мурманской области (стационар)"""

    def __init__(self, parent=None):
        title = u'Мастер экспорта в ОМС Мурманской области (стационар)'
        CAbstractExportWizard.__init__(self, parent, title)

        self.page1 = CExportPage1(self)
        self.page2 = CExportPage2(self)
        self.addPage(self.page1)
        self.addPage(self.page2)


    def getTmpDir(self):
        return CAbstractExportWizard.getTmpDirEx(self, 'R51HOSP')

# ******************************************************************************

class CExportPage1(CAbstractExportPage1, Ui_ExportPage1, CExportHelperMixin):
    u"""Первая страница мастера экспорта"""

    exportTypeSMO = 0 # индексы из cmbExportType
    exportTypeTFOMS = 1
    exportTypeDializ = 2
    exportTypeDS = 3

    exportFormat2019 = 0 # cmbExportFormat
    exportFormat2020 = 1
    exportFormat2021 = 2

    mapEventOrderToHosp = {2: '1', 1: '0'}
    mapPrCons = {
        u'Отсутствует необходимость проведения консилиума': 0,
        u'Определена тактика обследования:': 1,
        u'Определена тактика лечения': 2,
        u'Изменена тактика лечения': 3,
    }
    mapDs1t = {
        u'Первичное лечение': 0,
        u'Лечение при рецидиве': 1,
        u'Лечение при прогрессировании': 2,
        u'Динамическое наблюдение': 3,
        u'Диспансерное наблюдение (здоров/ремиссия)': 4,
    }

    def __init__(self, parent):
        CAbstractExportPage1.__init__(self, parent)
        CExportHelperMixin.__init__(self)

        self.ignoreErrors = False

        prefs = QtGui.qApp.preferences.appPrefs
        self.cmbExportFormat.setCurrentIndex(
            forceInt(prefs.get('ExportR51HospitalExportFormat', 0)))
        self.cmbExportType.setCurrentIndex(
            forceInt(prefs.get('ExportR51HospitalExportType', 0)))
        self.chkVerboseLog.setChecked(
            forceBool(prefs.get('ExportR51HospitalVerboseLog', False)))
        self.chkIgnoreErrors.setChecked(
            forceBool(prefs.get('ExportR51HospitalIgnoreErrors', False)))

        self.actionTypeMovement = None
        self.actionTypeArrival = None
        self.actionTypeIllegalActions = None
        self.actionTypeMultipleBirth = None
        self.actionTypeLeaved = None

        self.hasSenderActionPropertyType = False
        self.hasIllegalActionPropertyType = False

        self.exportFormat = 0
        self.mapEventIdtoIdCase = {}
        self._critDict = {}


    def setExportMode(self, flag):
        self.btnCancel.setEnabled(flag)
        self.btnExport.setEnabled(not flag)
        self.chkIgnoreErrors.setEnabled(not flag)
        self.chkVerboseLog.setEnabled(not flag)
        self.cmbExportType.setEnabled(not flag)
        self.cmbExportFormat.setEnabled(not flag)


    def validatePage(self):
        QtGui.qApp.preferences.appPrefs['ExportR51HospitalIgnoreErrors'] =\
            toVariant(self.chkIgnoreErrors.isChecked())
        QtGui.qApp.preferences.appPrefs['ExportR51HospitalVerboseLog'] =\
            toVariant(self.chkVerboseLog.isChecked())
        QtGui.qApp.preferences.appPrefs['ExportR51HospitalExportType'] = \
            toVariant(self.cmbExportType.currentIndex())
        QtGui.qApp.preferences.appPrefs['ExportR51HospitalExportFormat'] = \
            toVariant(self.cmbExportFormat.currentIndex())
        return CAbstractExportPage1.validatePage(self)

# ******************************************************************************

    def exportInt(self):
        tableOrganisation = self.db.table('Organisation')
        tableActionType = self.db.table('ActionType')
        self.ignoreErrors = self.chkIgnoreErrors.isChecked()
        self.exportFormat = self.cmbExportFormat.currentIndex()
        self.mapEventIdtoIdCase = {}
        self._critDict = self._getCritDict()

        params = {
            'exportedActions': set(),
            'exportType': self.cmbExportType.currentIndex(),
            'operations': dict(self._operationInfo()),
        }

        self.log(u'Выгружаем счет в формате "%d".' % params['exportType'])

        params['operOperFieldName'] = 'service' if (
            params['exportType'] in (self.exportTypeTFOMS, self.exportTypeSMO)
            ) else 'serviceCode'

        lpuId = QtGui.qApp.currentOrgId()
        params['lpuOKPO'] = forceString(self.db.translate(
            tableOrganisation, 'id', lpuId, 'OKPO'))
        params['lpuCode'] = forceString(self.db.translate(
            tableOrganisation, 'id', lpuId, 'infisCode'))
        self.log(u'ЛПУ: ОКПО "%s", код инфис: "%s".' % (
            params['lpuOKPO'], params['lpuCode']))

        if not params['lpuCode']:
            self.log(u'<b><font color=red>ОШИБКА<\font><\b>:'
                     u'Для текущего ЛПУ не задан код инфис', True)
            if not self.ignoreErrors:
                self.abort()
                return

        actionTypes = (
            ('actionTypeArrival', 'received', u'Поступление'),
            ('actionTypeIllegalActions', 'IllegalActions',
                u'Противоправные действия'),
            ('actionTypeMovement', 'moving', u'Движение'),
            ('actionTypeMultipleBirth', 'multipleBirth', u'Многоплодные роды'),
            ('actionTypeLeaved', 'leaved', u'Выписка')
        )

        for (attr, flatCode, desc) in actionTypes:
            _id = forceRef(self.db.translate(tableActionType,
                'flatCode', flatCode, 'id'))

            if not _id:
                self.log(u'<b><font color=red>ОШИБКА<\font><\b>:'
                    u'Не найден тип действия "%s" (плоский код: "%s")' % (
                    desc, flatCode), True)
                if not self.ignoreErrors:
                    self.abort()
                    return

            setattr(self, attr, _id)

        actionPropertyTypes = (
            ('actionTypeArrival', u'Поступление', u'Кем направлен',
                'hasSenderActionPropertyType'),
            ('actionTypeArrival', u'Поступление', u'Направлен в отделение',
                'hasSentToActionPropertyType'),
            ('actionTypeArrival', u'Поступление', u'Вес',
                'hasWeightActionPropertyType'),
            ('actionTypeArrival', u'Поступление', u'Квота',
                'hasArrivalQuotaActionPropertyType'),
            ('actionTypeIllegalActions', u'Противоправные действия',
                u'Признак', 'hasIllegalActionPropertyType'),
            ('actionTypeLeaved', u'Выписка', u'Квота',
                'hasLeavedQuotaActionPropertyType'),
            ('actionTypeMovement', u'Движение', u'Квота',
                'hasMovementQuotaActionPropertyType'),
        )

        for (actionType, desc, _property, attr) in actionPropertyTypes:
            actionTypeId = getattr(self, actionType, None)
            flag = self.getActionPropertyTypeIdByName(actionTypeId,
                                                      _property) is not None

            if not flag:
                self.log(u'<b><font color=red>ОШИБКА<\font><\b>:'
                         u'Не найдено свойство "%s" у типа действия "%s")' % (
                         _property, desc), True)
                if not self.ignoreErrors:
                    self.abort()
                    return

            setattr(self, attr, flag)

        params.update(self.accountInfo())

        orgStructId = params['accOrgStructureId']
        record = self.db.getRecord('OrgStructure',
            'infisCode, tfomsCode', orgStructId)
        if record:
            params['accOrgStructInfisCode'] = forceString(
                record.value('infisCode'))
            params['accOrgStructTfomsCode'] = forceString(
                record.value('tfomsCode'))

        params['payerInfis'] = forceString(self.db.translate(
            tableOrganisation, 'id', params['payerId'], 'infisCode'))
        params['rowNumber'] = 1
        params['onkologyInfo'] = getOnkologyInfo(
            self.db, self.tableAccountItem['id'].inlist(self.idList),
            exportType2019=True)

        self.setProcessParams(params)

        CAbstractExportPage1.exportInt(self)


    def createDbf(self):
        result = (self._createReestrDbf(), self._createDepReeDbf(),
                  self._createAddInfDbf(), self._createOperDbf(),
                  self._createDepAddDbf(), self._createOnkSlDbf(),
                  self._createBDiagDbf(), self._createBProtDbf(),
                  self._createOnkUslDbf(), self._createLekPrDbf(),
                  self._createConsDbf(), self._createNaprDbf())

        if self.exportFormat >= self.exportFormat2020:
            result += (self._createCritDbf(), self._createServTmtDbf())
        else:
            result += (None, None)
        return result


    def _createConsDbf(self):
        u'Сведения о проведении консилиума'
        dbfName = os.path.join(self.getTmpDir(), 'CONS.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('CARD', 'C', 10),   # Номер статталона
            ('PR_CONS', 'N', 1), # Цель проведения консилиума
            ('DT_CONS', 'D', 8), # Дата проведения консилиума
            ('NIB', 'C', 10),       # Номер истории болезни
            ('ID_CASE', 'N', 10),   # Порядковый номер случая в реестре
        )
        return dbf


    def _createReestrDbf(self):
        """ Создает структуру dbf для REESTR.DBF """

        dbfName = os.path.join(self.getTmpDir(), 'REESTR.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('NIB', 'C', 10), # Номер истории болезни
                                    # Не повторяется в отчетном году
            ('INS', 'C', 2), # Код СМО (по справочнику фонда)
            ('DATA1', 'D'), # Начальная дата интервала,
                                        # за который представляется реестр
            ('DATA2', 'D'), # Конечная дата интервала,
                                        # за который представляется реестр
            ('FAM', 'C', 40), # Фамилия пациента
            ('IMM', 'C', 40), # Имя пациента
            ('OTC', 'C', 40), # Отчество пациента
            ('SER_PASP', 'C', 8), # Серия документа, удостоверяющего личность
            ('NUM_PASP', 'C', 8), # Номер документа, удостоверяющего личность
            ('TYP_DOC', 'N', 2), # Тип документа, удостоверяющего личность
            ('SS', 'C', 14), # Страховой номер индивидуального лицевого счета
            ('DROJD', 'D'), # Дата рождения пациента
            ('POL', 'C', 1), # Пол пациента   («М», «Ж»)
            ('RAB', 'C', 1), # Признак работающий- “1”/неработающий – “0”
            ('SPOLIS', 'C', 10), # Серия полиса
            ('NPOLIS', 'C', 20), # Номер полиса
            ('TAUN', 'C', 3), # Код населенного пункта проживания пациента по
                                        #справочнику фонда TAUNS
            ('HOSP', 'C', 1), # Признак поступления экстренное –“1”
                                    #/плановое –“0   У нас дневной стационар =0
            ('DATAP', 'D'), # Дата поступления в ЛПУ
            ('DATAV', 'D'), # Дата выписки из ЛПУ
            ('STOIM', 'N', 10, 2), # Суммарная стоимость пребывания в ЛПУ
            ('KRIM', 'C', 1), # Признак противоправных действий 0 – обычное СБО,
                                        # 1- противоправное действие.
            ('DIAG', 'C', 6), # Заключительный диагноз
            ('DIRECT_LPU', 'C', 3), # Код ЛПУ, направившего на госпитализацию
            ('DIR_SUBLPU', 'C', (3 if self.exportFormat >= self.exportFormat2021
                                 else 2)),
            ('DIR_TOWN', 'C', 3),
            ('MASTER', 'C', 9), # Коды ЛПУ приписки по справочнику фонда
                                            #(поликлиника + стоматология +ЖК)
                                            #В строке через 3 пробела.
                                            # Пример 103   160   121
            ('LPU', 'C', 3), # Код ЛПУ пребывания по справочнику фонда
                                    # 141- это стационар на дому пол-ки 3,
                                   # 951- реабилитация, 605- дневной стационар
            ('SUB_HOSP', 'C', (3 if self.exportFormat >= self.exportFormat2021
                                 else 2)),
            ('TOWN_HOSP', 'C', 3),
            ('COUNT', 'C', 10), # Номер счета представляемого в фонд
            ('STOIM_S', 'N', 10, 2), # Сумма из средств Федеральных субвенций
            ('TPOLIS', 'N', 1), # Тип полиса:   1 – старого образца,
                            #2 – временное свидетельство, 3 – нового образца
            ('VNOV_D', 'N', 4), # Вес при рождении в граммах
            ('P_CODE', 'C', 14), #Личный код врача, закрывшего историю болезни
            ('NPR_DATE', 'D'), #Дата направления на лечение
            ('DOCDATE', 'D'), #
            ('DOCORG', 'C', 250), #
        )

        return dbf


    def _createDepReeDbf(self):
        """ Создает структуру dbf для DEP_REE.DBF """

        dbfName = os.path.join(self.getTmpDir(), 'DEP_REE.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('NIB',        'C', 10),# Номер истории болезни
            ('ID_CASE',    'N', 10),# Порядковый номер случая в реестре
            ('OTD',        'C', 3), # Код отделения по справочнику фонда
            ('DIRECT_OTD', 'C', 3), # Код отделения, откуда переведен пациент
                                    # (при переводе из одного отделения в другое отделение)
            ('HOSP',       'C', 1), # Признак поступления экстренное – “1”
                                    # плановое – “0”/ перевод из отделения в отделение – “2”
            ('DATAP',      'D'),    # Дата поступления  в отделение
            ('DATAV',      'D'),    # Дата выписки из отделения
            ('DOCTOR',     'C', 14),# Код врача лечившего пациента
            ('LEVEL',      'C', 1), # Уровень оказанной помощи
                                    # (“1”- дневные стационары,
                                    # “0” – стационары круглосуточного пребывания)
            ('TALON',      'C', 6), # № направления на госпитализацию
            ('DIAG',       'C', 6), # Код МКБ Х
            ('DS0',        'C', 6), # Диагноз первичный
            ('DS_S',       'C', 6), # Код диагноза сопутствующего заболевания
                                    #(состояния) по МКБ-10
        )

        if self.exportFormat < self.exportFormat2020:
            dbf.addField(
                ('BED_PROF', 'C', 3),   # Код профиля койки    bed_prof
            )

        dbf.addField(
            ('STOIM_S', 'N', 10, 2),# Сумма из средств Федеральных субвенций
            ('STOIM_D', 'N', 10, 2), #Стоимость услуг по гемодиализу
            ('RSLT', 'N', 3),      # Результат обращения/ госпитализации
            ('ISHOD', 'N', 3),     # Исход заболевания
            ('VID_HMP', 'C', 12),  # Вид высокотехнологичной медицинской
                                   # помощи (ВМП)
            ('METOD_HMP', 'N', 3), # Метод высокотехнологичной
                                   # медицинской помощи
            ('PROFIL', 'N', 3),    # Профиль оказанной медицинской помощи
            ('PRVS', 'N', 3),      # Код специальности медицинского работника,
                                   # оказавшего услугу
            ('KSG', 'C', 20),      # Код клинико-статистической группы
            ('DS_P', 'C', 6, 0),
            ('DS3', 'C', 6, 0),
            ('VIDPOM', 'N', 4),    #
            ('VID_FIN', 'N', 1),   # Источник финансирования
            ('MOTHER', 'N', 1),    #
            ('P_MODE', 'N', 1),    #
            ('P_PER','N', 1), #Признак поступления / перевода
            ('NPL',  'N', 1), #Неполный объём
            ('PR_OS','N', 2), #Признак “Особый случай»
            ('IDSP',       'N', 2), #Код способа оплаты медицинской помощи
            ('ADD_CR_KSG', 'C', 5), # Дополнительный классификационный
                                    # критерий для выбора КСГ
            ('STAGE',      'N', 1), #Этап проведения ЭКО
            ('TAL_D',      'D'),    # Дата выдачи талона на ВМП
            ('TAL_NUM',    'C', 20),# Номер талона на ВМП
            ('C_ZAB',      'N', 1), #
            ('ZS', 'N', 1),         # Признак законченного случая (1–законченный случай, 0– прерванный случай
                                        #Выгружаем 1)
             # Код структурного подразделения МО
            ('SUB_HOSP', 'C', (3 if self.exportFormat >= self.exportFormat2021
                                 else 2)),
            ('TAL_P', 'D'), # - пустое, не заполняем
            ('DS_ONK', 'N', 1, 0), #
        )

        if self.exportFormat >= self.exportFormat2020:
            dbf.addField(
                ('PROFIL_K',  'N',  3), #
                ('mpcod',     'C',  8), #
                ('addr_code', 'C', 16), #
            )
        if self.exportFormat >= self.exportFormat2021:
            dbf.addField(
                ('DS_PZ', 'C', 6),
                ('HGR', 'N', 3),
            )

        return dbf


    def _createAddInfDbf(self):
        """ Создает структуру dbf для ADD_INF.DBF """

        dbfName = os.path.join(self.getTmpDir(), 'ADD_INF.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('NIB', 'C', 10),      # Номер истории болезни
            ('MR', 'C', 100),      # Место рождения пациента или представителя
            ('OKATOG', 'C', 11),   # Код места жительства по ОКАТО
            ('OKATOP', 'C', 11),   # Код места пребывания по ОКАТО
            ('OKATO_OMS', 'C', 5), # Код ОКАТО территории страхования по ОМС
                                                        #(по справочнику фонда)
            ('FAMP', 'C', 40), # Фамилия родителя (представителя) пациента
            ('IMP', 'C', 40),  # Имя родителя (представителя) пациента
            ('OTP', 'C', 40),  # Отчество родителя (представителя) пациента
            ('DRP', 'D'),      # Дата рождения родителя (представителя) пациента
            ('WP', 'C', 1),    # Пол родителя (представителя) пациента
            ('C_DOC', 'N', 2), # Код типа документа, удостоверяющего личность
                               # пациента (представителя) (по  справочнику фонда)
            ('S_DOC', 'C', 9), # Серия документа, удостоверяющего личность
                               # пациента (представителя) (по справочнику фонда)
            ('N_DOC', 'C', 8), # Номер документа, удостоверяющего личность
                               # пациента (представителя) (справочник фонда)
            ('NOVOR', 'C', 9), # Признак новорожденного
            ('Q_G', 'C', 7),   # Признак «Особый случай» при регистрации
                                    # обращения  за медицинской помощью
                                    #«1» –  отсутствие у пациента полиса
                                    # обязательного медицинского страхования;
                                    #«2»  - медицинская помощь оказана
                                    # новорожденному;
                                    #«3» – при оказании медицинской помощи
                                    # ребенку до 14 лет был предъявлен документ,
                                    # удостоверяющий личность, и полис ОМС
                                    #одного из его родителей или представителей;
                                    #«4» – отсутствие отчества в документе,
                                    # удостоверяющем личность пациента
                                    # (представителя пациента);
                                    #«5» -  медицинская помощь, оказанная
                                    # новорожденному при  многоплодных родах.
            ('MSE', 'N', 1), # Направление на МСЭ
            ('DOCDATE', 'D'), #
            ('DOCORG', 'C', 250), #
        )
        return dbf


    def _createOperDbf(self):
        """ Создает структуру dbf для OPER.DBF """

        dbfName = os.path.join(self.getTmpDir(), 'OPER.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('NIB', 'C', 10), # Номер истории болезни
            ('IDSERV', 'C', 36), #Номер записи в реестре услуг
            ('ID_CASE', 'N', 10), # Порядковый номер случая в реестре
            ('OTD_O', 'C', 3), # Код отделения, где проведена операция
            ('DATA_O', 'D'), # Дата, когда проведена операция
            ('OPER', 'C', 15), # Код операции
            ('KOL_OPER', 'N', 1), # Количество операций
            ('DOCTOR', 'C', 8), # Код врача лечившего пациента
            ('PROFIL', 'N', 3), # Профиль оказанной медицинской помощи
            ('PRVS', 'N', 4), # Код специальности медицинского работника,
                                        # оказавшего услугу
            ('PR_OPER', 'N', 1), #Дополнительный признак операции
        )

        if self.exportFormat >= self.exportFormat2020:
            dbf.addField(
                ('mpcod', 'C', 8), #
                ('addr_code', 'C', 16), #
            )
        return dbf

    def _createDepAddDbf(self):
        u"""Создает структуру DBF для DEP_ADD.DBF"""

        dbfName = os.path.join(self.getTmpDir(), 'DEP_ADD.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('NIB', 'C', 10), # Номер истории болезни
            ('ID_CASE', 'N', 10), # Порядковый номер случая в реестре
            ('DATE_1', 'D'), # Дата поступления пациента в отделение
                                        #интенсивной терапии и  реанимации
            ('DATE_2', 'D'), # Дата выбытия пациента из отделения
                                        #интенсивной терапии и  реанимации
            ('DS', 'C', 6, 0), # Диагноз основной
            ('DOCTOR', 'C', 8), # Код врача лечившего пациента
            ('PROFIL', 'N', 3), # Профиль оказанной медицинской помощи
            ('PRVS', 'N', 4), # Код специальности медицинского работника,
                                        #оказавшего услугу
        )
        return dbf


    def _createOnkSlDbf(self):
        u'Сведения о случае лечения онкологического заболевания'
        dbfName = os.path.join(self.getTmpDir(), 'ONK_SL.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('NIB', 'C', 10), # Номер истории болезни
            ('ID_CASE', 'N', 10), # Порядковый номер случая в реестре
            ('DS1_T', 'N', 1), # Повод обращения
            ('STAD', 'N', 3), # Стадия заболевания
            ('ONK_T', 'N', 4), #
            ('ONK_N', 'N', 4), #
            ('ONK_M', 'N', 4), #
            ('MTSTZ', 'N', 1), #
            ('SOD', 'N', 6, 2), #
            ('K_FR', 'N', 2, 0), #
            ('WEI', 'N', 5, 1), #
            ('HEI', 'N', 3, 0), #
            ('BSA', 'N', 4, 2), #
        )

        return dbf


    def _createBDiagDbf(self):
        u"""Диагностический блок, содержит сведения о проведенных
            исследованиях и их результатах"""
        dbfName = os.path.join(self.getTmpDir(), 'B_DIAG.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('NIB', 'C', 10), # Номер истории болезни
            ('ID_CASE', 'N', 10),# Порядковый номер случая в реестре
            ('DIAG_DATE', 'D', 8),
            ('DIAG_TIP', 'N', 1),
            ('DIAG_CODE', 'N', 3),
            ('DIAG_RSLT', 'N', 3),
            ('REC_RSLT', 'N', 1),)
        return dbf


    def _createBProtDbf(self):
        u"""Сведения об имеющихся противопоказаниях и отказах"""
        dbfName = os.path.join(self.getTmpDir(), 'B_PROT.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('NIB',     'C', 10), # Номер истории болезни
            ('ID_CASE', 'N', 10), # Порядковый номер случая в реестре
            ('PROT',    'N',  1),
            ('D_PROT',  'D'    ), # Дата регистрации противопоказания или отказа
        )
        return dbf


    def _createOnkUslDbf(self):
        u"""Сведения об услуге при лечении онкологического заболевания"""
        dbfName = os.path.join(self.getTmpDir(), 'ONK_USL.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('NIB', 'C', 10), # Номер истории болезни
            ('ID_CASE', 'N', 10), # Порядковый номер случая в реестре
            ('IDSERV', 'C', 36), #
            ('USL_TIP', 'N', 1), #
            ('HIR_TIP', 'N', 1), #
            ('LEK_TIP_L', 'N', 1), #
            ('LEK_TIP_V', 'N', 1), #
            ('PPTR', 'N', 1), #
            ('LUCH_TIP', 'N', 1), #
        )
        return dbf


    def _createLekPrDbf(self):
        u'Сведения о введенном противоопухолевом лекарственном препарате'
        dbfName = os.path.join(self.getTmpDir(), 'LEK_PR.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('NIB',     'C', 10), # Номер истории болезни
            ('ID_CASE', 'N', 10), # Порядковый номер случая в реестре
            ('IDSERV',  'C', 36), #
            ('REGNUM',  'C',  6), #
            ('CODE_SH', 'C', 10), #
            ('DATE_INJ','D',  8), #
        )
        return dbf


    def _createNaprDbf(self):
        u'Сведения о направлениях'
        dbfName = os.path.join(self.getTmpDir(), 'NAPR.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('NIB', 'C', 10), # Номер истории болезни
            ('ID_CASE',   'N', 10), # Порядковый номер случая в реестре
            ('NAPR_DATE', 'D'    ), #
            ('NAPR_ MO',  'C',  3),
            ('NAPR_V',    'N',  2),
            ('MET_ISSL',  'N',  2),
            ('NAPR_USL',  'C', 15),
        )
        return dbf


    def _createCritDbf(self):
        dbfName = os.path.join(self.getTmpDir(), 'CRIT_KSG.DBF')
        dbf = Dbf(dbfName, new=True, encoding='cp866')
        dbf.addField(
            ('NIB',     'C', 10), # Номер истории болезни
            ('ID_CASE', 'N', 10), # Порядковый номер случая в реестре
            ('CRIT',    'C', 10),
        )
        return dbf


    def _createServTmtDbf(self):
        return createServTmtDbf(self.getTmpDir())

# ******************************************************************************

    def createQuery(self):
        stmt = u"""SELECT Event.client_id,
                Account_Item.event_id,
                ClientPolicy.serial AS policySerial,
                ClientPolicy.number AS policyNumber,
                rbPolicyKind.regionalCode AS policyKind,
                IF(work.title IS NOT NULL,
                    work.title,
                    ClientWork.freeInput) AS workName,
                Event.setDate AS begDate,
                Event.execDate AS endDate,
                Diagnosis.MKB,
                IF(rbDiagnosticResult.regionalCode IS NULL,
                    EventResult.regionalCode,
                    rbDiagnosticResult.regionalCode) AS resultCode,
                EventResult.regionalCode AS eventResultRegionalCode,
                Client.lastName,
                Client.firstName,
                Client.patrName,
                ClientDocument.serial AS documentSerial,
                ClientDocument.number AS documentNumber,
                rbDocumentType.regionalCode AS documentRegionalCode,
                ClientDocument.date AS DOCDATE,
                ClientDocument.origin AS DOCORG,
                Client.SNILS,
                Client.birthDate,
                Client.birthPlace,
                Client.sex,
                RegAddressHouse.KLADRCode,
                RegKLADR.infis AS placeCode,
                LocRegionKLADR.OCATD AS locRegionOKATO,
                RegRegionKLADR.OCATD AS regRegionOKATO,
                AccDiagnosis.MKB AS accMKB,
                IF(Account_Item.visit_id IS NOT NULL, VisitPerson.code,
                    IF(Account_Item.action_id IS NOT NULL,
                        IF(Action.person_id IS NOT NULL, ActionPerson.code,
                            ActionSetPerson.code), Person.code)
                ) AS personCode,
                ActionPerson.regionalCode AS personRegionalCode,
                IF(Account_Item.visit_id IS NOT NULL, VisitSpeciality.regionalCode,
                    IF(Account_Item.action_id IS NOT NULL,
                        IF(Action.person_id IS NOT NULL, ActionSpeciality.regionalCode,
                            ActionSetSpeciality.regionalCode), rbSpeciality.regionalCode)
                )  AS specialityCode,
                IF(Account_Item.visit_id IS NOT NULL, VisitSpeciality.federalCode,
                    IF(Account_Item.action_id IS NOT NULL,
                        IF(Action.person_id IS NOT NULL, ActionSpeciality.federalCode,
                            ActionSetSpeciality.federalCode), rbSpeciality.federalCode)
                )  AS specialityFederalCode,
                IF(Account_Item.service_id IS NOT NULL,
                    rbItemService.infis,
                    IF(Account_Item.visit_id IS NOT NULL, rbVisitService.infis, rbEventService.infis)
                    ) AS service,
                Account_Item.amount,
                Account_Item.`sum` AS `sum`,
                Insurer.OKATO AS insurerOKATO,
                RelegateOrg.smoCode AS relegateOrgSmoCode,
                RelegateOrg.tfomsExtCode AS relegateOrgTfomsExtCode,
                AttachOrg.infisCode AS attachCodeString,
                AttachOrg.smoCode AS attachOrgSmoCode,
                AttachOrg.tfomsExtCode AS attachOrgTfomsExtCode,
                Event.externalId,
                rbMedicalAidType.regionalCode AS medicalAidTypeCode,
                (SELECT GROUP_CONCAT(A.id)
                 FROM Action A
                 WHERE A.event_id = Event.id AND
                          A.deleted = 0 AND
                          A.actionType_id IN (
                                SELECT AT.id
                                FROM ActionType AT
                                WHERE AT.flatCode ='moving'
                )) AS hospitalActionId,
                ActionType.code AS serviceCode,
                mes.MES_ksg.code AS ksgCode,
                Event.order AS eventOrder,
                Hospital.infisCode AS hospitalInfisCode,
                rbMedicalAidKind.regionalCode AS medicalAidKindCode,
                Contract_Tariff.price,
                Action.status AS actionStatus,
                ActionType.serviceType AS serviceType,
                CriterionActionType.code AS criterionCode,
                rbMedicalAidUnit.regionalCode AS medicalAidUnitCode,
                NOT ISNULL(CurrentOrgAttach.id) AS isAttached,
                rbScene.name LIKE "%%на дому%%" AS isHomeVisit,
                Event.srcDate,
                rbMesSpecification.level AS mesSpecificationLevel,
                Person.SNILS AS execPersonSNILS,
                rbSpeciality.federalCode AS federalCodeExecPerson,
                rbSpeciality.regionalCode AS regionalCodeExecPerson,
                IF(SUBSTR(Diagnosis.MKB, 1, 1) = 'Z', 0,
                    rbDiseaseCharacter_Identification.value) AS C_ZAB,
                Action.id AS actionId,
                (SELECT OSI.value
                 FROM OrgStructure_Identification OSI
                 WHERE OSI.master_id = IFNULL(Person.orgStructure_id, (
                        SELECT orgStructure_id
                        FROM Account WHERE Account.id = Account_Item.master_id))
                    AND OSI.deleted = 0
                    AND OSI.system_id = (
                        SELECT MAX(id) FROM rbAccountingSystem
                        WHERE rbAccountingSystem.code = 'mpcod')
                ) AS orgStructMpCod,
                (SELECT OSI.value
                 FROM OrgStructure_Identification OSI
                 WHERE OSI.master_id = Person.orgStructure_id
                    AND OSI.deleted = 0
                    AND OSI.system_id = (
                        SELECT MAX(id) FROM rbAccountingSystem
                        WHERE rbAccountingSystem.code = 'addr_code')
                ) AS orgStructAddrCode,
                (SELECT infisCode FROM OrgStructure OS
                 WHERE OS.id = Person.orgStructure_id
                 LIMIT 1) AS subHospital,
                (SELECT code FROM rbDiseasePhases WHERE
                  Diagnostic.phase_id = rbDiseasePhases.id) AS phaseCode
            FROM Account_Item
            LEFT JOIN Action ON Action.id = Account_Item.action_id
            LEFT JOIN Visit  ON Visit.id  = Account_Item.visit_id
            LEFT JOIN Event  ON Event.id  = Account_Item.event_id
            LEFT JOIN rbMesSpecification ON Event.mesSpecification_id = rbMesSpecification.id
            LEFT JOIN Client ON Client.id = Event.client_id
            LEFT JOIN ClientPolicy ON ClientPolicy.client_id = Client.id AND
                      ClientPolicy.id = (SELECT MAX(CP.id)
                                         FROM   ClientPolicy AS CP
                                         LEFT JOIN rbPolicyType AS CPT ON CPT.id = CP.policyType_id
                                         WHERE  CP.client_id = Client.id AND CP.deleted=0 AND CPT.code IN ('1','2'))
            LEFT JOIN Organisation AS Insurer ON Insurer.id = ClientPolicy.insurer_id
            LEFT JOIN rbPolicyKind ON rbPolicyKind.id = ClientPolicy.policyKind_id
            LEFT JOIN ClientDocument ON ClientDocument.client_id = Client.id AND
                      ClientDocument.id = (SELECT MAX(CD.id)
                                         FROM   ClientDocument AS CD
                                         LEFT JOIN rbDocumentType AS rbDT ON rbDT.id = CD.documentType_id
                                         LEFT JOIN rbDocumentTypeGroup AS rbDTG ON rbDTG.id = rbDT.group_id
                                         WHERE  rbDTG.code = '1' AND CD.client_id = Client.id AND CD.deleted=0)
            LEFT JOIN rbDocumentType ON rbDocumentType.id = ClientDocument.documentType_id
            LEFT JOIN ClientAddress ClientRegAddress ON ClientRegAddress.client_id = Client.id AND
                      ClientRegAddress.id = (SELECT MAX(CRA.id)
                                         FROM   ClientAddress AS CRA
                                         WHERE  CRA.type = 0 AND CRA.client_id = Client.id AND CRA.deleted=0)
            LEFT JOIN ClientAddress ClientLocAddress ON ClientLocAddress.client_id = Client.id AND
                      ClientLocAddress.id = (SELECT MAX(CLA.id)
                                         FROM   ClientAddress AS CLA
                                         WHERE  CLA.type = 1 AND CLA.client_id = Client.id AND CLA.deleted=0)
            LEFT JOIN Address   RegAddress ON RegAddress.id = ClientRegAddress.address_id
            LEFT JOIN AddressHouse RegAddressHouse ON RegAddressHouse.id = RegAddress.house_id
            LEFT JOIN Address   LocAddress ON LocAddress.id = ClientLocAddress.address_id
            LEFT JOIN AddressHouse LocAddressHouse ON LocAddressHouse.id = LocAddress.house_id
            LEFT JOIN kladr.KLADR RegKLADR ON RegKLADR.CODE = RegAddressHouse.KLADRCode
            LEFT JOIN (
                SELECT * FROM kladr.SOCRBASE AS SB
                GROUP BY SB.SCNAME
            ) AS  RegSOCR ON RegSOCR.SCNAME = RegKLADR.SOCR
            LEFT JOIN kladr.KLADR RegRegionKLADR ON RegRegionKLADR.CODE = (
                SELECT RPAD(LEFT(RegAddressHouse.KLADRCode,2),13,'0'))
            LEFT JOIN kladr.KLADR LocRegionKLADR ON LocRegionKLADR.CODE = (
                SELECT RPAD(LEFT(LocAddressHouse.KLADRCode,2),13,'0'))
            LEFT JOIN Person ON Person.id = Event.execPerson_id
                AND Person.id IS NOT NULL
            LEFT JOIN Person AS VisitPerson ON VisitPerson.id = Visit.person_id
                AND VisitPerson.id IS NOT NULL
            LEFT JOIN Person AS ActionPerson ON ActionPerson.id = Action.person_id
                AND ActionPerson.id IS NOT NULL
            LEFT JOIN Person AS ActionSetPerson ON ActionSetPerson.id = Action.setPerson_id
                AND ActionSetPerson.id IS NOT NULL
            LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
                AND rbSpeciality.id IS NOT NULL
            LEFT JOIN rbSpeciality AS VisitSpeciality ON VisitPerson.speciality_id = VisitSpeciality.id
                AND VisitSpeciality.id IS NOT NULL
            LEFT JOIN rbSpeciality AS ActionSpeciality ON ActionPerson.speciality_id = ActionSpeciality.id
                AND ActionSpeciality.id IS NOT NULL
            LEFT JOIN rbSpeciality AS ActionSetSpeciality ON ActionSetPerson.speciality_id = ActionSetSpeciality.id
                AND ActionSetSpeciality.id IS NOT NULL
            LEFT JOIN Diagnostic ON ( Diagnostic.event_id = Account_Item.event_id
                                      AND Diagnostic.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code IN ('1', '2'))
                                      AND Diagnostic.person_id = Event.execPerson_id AND Diagnostic.deleted = 0)
            LEFT JOIN Diagnostic AS AccDiagnostic ON AccDiagnostic.id = (
             SELECT id FROM Diagnostic AS AD
             WHERE AD.event_id = Account_Item.event_id AND
                AD.diagnosisType_id IN (SELECT id FROM rbDiagnosisType WHERE code='9') AND
                AD.person_id = Event.execPerson_id AND
                AD.deleted = 0 LIMIT 1)
            LEFT JOIN Diagnosis AS AccDiagnosis ON
                AccDiagnosis.id = AccDiagnostic.diagnosis_id AND
                AccDiagnosis.deleted = 0
            LEFT JOIN ClientWork ON ClientWork.client_id=Event.client_id AND
                        ClientWork.id = (SELECT max(CW.id)
                                         FROM ClientWork AS CW
                                         WHERE CW.client_id=Client.id AND CW.deleted=0)
            LEFT JOIN Organisation AS work ON work.id=ClientWork.org_id AND work.deleted = 0
            LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id AND Diagnosis.deleted = 0
            LEFT JOIN rbDiagnosticResult ON rbDiagnosticResult.id=Diagnostic.result_id
            LEFT JOIN rbResult AS EventResult ON EventResult.id=Event.result_id
            LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
            LEFT JOIN EventType ON Event.eventType_id = EventType.id
            LEFT JOIN rbService AS rbEventService ON rbEventService.id = EventType.service_id
            LEFT JOIN rbService AS rbVisitService ON rbVisitService.id = Visit.service_id
            LEFT JOIN rbService AS rbItemService ON rbItemService.id = Account_Item.service_id
            LEFT JOIN rbPayRefuseType
                ON rbPayRefuseType.id = Account_Item.refuseType_id
            LEFT JOIN Organisation AS RelegateOrg
                ON Event.relegateOrg_id = RelegateOrg.id
            LEFT JOIN ClientAttach ON ClientAttach.client_id=Event.client_id AND
                        ClientAttach.id = (SELECT max(CA.id)
                                         FROM ClientAttach AS CA
                                         WHERE CA.client_id=Client.id AND CA.deleted=0)
            LEFT JOIN Organisation AS AttachOrg
                ON ClientAttach.LPU_id = AttachOrg.id
            LEFT JOIN mes.MES ON Event.MES_id = mes.MES.id
                AND mes.MES.deleted = 0
            LEFT JOIN mes.MES_ksg ON mes.MES_ksg.id = mes.MES.ksg_id
                AND mes.MES_ksg.deleted = 0
            LEFT JOIN Action AS HospitalAction ON HospitalAction.id = (
                SELECT MAX(A.id)
                FROM Action A
                WHERE A.event_id = Event.id AND
                          A.deleted = 0 AND
                          A.actionType_id IN (
                                SELECT AT.id
                                FROM ActionType AT
                                WHERE AT.flatCode ='moving'
                          )
            )
            LEFT JOIN rbMedicalAidType ON EventType.medicalAidType_id =rbMedicalAidType.id
            LEFT JOIN rbMedicalAidKind ON EventType.medicalAidKind_id = rbMedicalAidKind.id
            LEFT JOIN Organisation AS Hospital ON Hospital.id = Person.org_id
            LEFT JOIN Contract_Tariff ON Contract_Tariff.id = Account_Item.tariff_id
            LEFT JOIN ActionType AS CriterionActionType ON CriterionActionType.id = (
                SELECT MAX(AT.id)
                FROM Action A
                LEFT JOIN ActionType AT ON AT.id = A.actionType_id
                    AND AT.flatCode = 'AddCriterion'
                WHERE A.event_id = Event.id AND A.deleted = 0
            )
            LEFT JOIN rbScene ON rbScene.id = Visit.scene_id
            LEFT JOIN rbMedicalAidUnit ON rbMedicalAidUnit.id = Account_Item.unit_id
            LEFT JOIN ClientAttach AS CurrentOrgAttach ON CurrentOrgAttach.id = (
                SELECT MAX(COA.id)
                FROM ClientAttach COA
                WHERE COA.LPU_id = %d AND COA.client_id = Client.id
                    AND (COA.begDate IS NULL OR COA.begDate <= Event.execDate)
                    AND (COA.endDate IS NULL OR COA.endDate >= Event.execDate)
            )
            LEFT JOIN rbDiseaseCharacter ON rbDiseaseCharacter.id = Diagnosis.character_id
            LEFT JOIN rbDiseaseCharacter_Identification ON rbDiseaseCharacter_Identification.id = (
                SELECT MAX(DId.id)
                FROM rbDiseaseCharacter_Identification DId
                WHERE DId.master_id = rbDiseaseCharacter.id
                AND DId.system_id IN (SELECT id FROM rbAccountingSystem WHERE urn = 'urn:tfoms51:V027')
                AND DId.deleted = 0
            )
            WHERE
                Account_Item.reexposeItem_id IS NULL
            AND (Account_Item.date IS NULL
                 OR (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0)
                )
            AND %s
        """ % (QtGui.qApp.currentOrgId(),
               self.tableAccountItem['id'].inlist(self.idList))
        query = self.db.query(stmt)
        return query


    def _getQuota(self, eventId):
        u"""Возвращает квоту по идентификатору события"""

        try:
            quota = self.getActionPropertyText(eventId,
                                           self.actionTypeLeaved, u'Квота')
        except KeyError:
            quota = None

        if not quota:
            try:
                quota = self.getActionPropertyText(eventId,
                                       self.actionTypeMovement, u'Квота')
            except KeyError:
                quota = None

        if not quota:
            try:
                quota = self.getActionPropertyText(eventId,
                                       self.actionTypeArrival, u'Квота')
            except KeyError:
                quota = None

        if quota:
            code = quota.split("|")
            quota = forceRef(self.db.translate('QuotaType', 'code',
                                                 code[0], 'regionalCode'))

        return quota


    def _operationInfo(self):
        stmt = u'''SELECT Action.id AS actionId,
            Event.id AS eventId,
            ActionType.code AS serviceCode,
            NomenclativeService.infis AS service,
            IFNULL(VisitPerson.code,
                IFNULL(ActionPerson.code,
                    IFNULL(ActionSetPerson.code, Person.code))) AS personCode,
            Action.amount AS amount,
            rbSpeciality.federalCode AS federalCodeExecPerson,
            rbSpeciality.regionalCode AS regionalCodeExecPerson,
            Action.endDate AS actionDate
        FROM Account_Item
        LEFT JOIN Event ON Event.id = Account_Item.event_id
        LEFT JOIN Action ON Action.event_id = Event.id
        LEFT JOIN ActionType ON ActionType.id = Action.actionType_id
        LEFT JOIN Person ON Person.id = Event.execPerson_id
            AND Person.id IS NOT NULL
        LEFT JOIN rbSpeciality ON Person.speciality_id = rbSpeciality.id
            AND rbSpeciality.id IS NOT NULL
        LEFT JOIN rbService AS NomenclativeService ON
            NomenclativeService.id = ActionType.nomenclativeService_id
        LEFT JOIN Visit ON Visit.id  = Account_Item.visit_id
        LEFT JOIN Person AS VisitPerson ON VisitPerson.id = Visit.person_id
            AND VisitPerson.id IS NOT NULL
        LEFT JOIN Person AS ActionPerson ON ActionPerson.id = Action.person_id
            AND ActionPerson.id IS NOT NULL
        LEFT JOIN Person AS ActionSetPerson ON ActionSetPerson.id = Action.setPerson_id
            AND ActionSetPerson.id IS NOT NULL
        LEFT JOIN rbPayRefuseType
            ON rbPayRefuseType.id = Account_Item.refuseType_id
        WHERE Account_Item.reexposeItem_id IS NULL
          AND ActionType.serviceType = 4
          AND (Account_Item.date IS NULL OR
               (Account_Item.date IS NOT NULL
                AND rbPayRefuseType.rerun != 0))
          AND {idList}
        ORDER BY Account_Item.event_id, Account_Item.action_id
            '''.format(idList=self.tableAccountItem['id'].inlist(self.idList))

        query = self.db.query(stmt)
        lastEventId = None
        result = []

        while query.next():
            record = query.record()
            eventId = forceRef(record.value('eventId'))

            if eventId != lastEventId:
                if lastEventId:
                    yield lastEventId, result

                lastEventId = eventId
                result = []

            result.append(record)

        if lastEventId:
            yield lastEventId, result

# ******************************************************************************

    def process(self, dbf, record, params):
        local_params = {
            'begDate': forceDate(record.value('begDate')),
            'endDate': forceDate(record.value('endDate')),
            'eventId': forceRef(record.value('event_id')),
            'eventIdStr': forceString(record.value('event_id')),
            'clientId': forceRef(record.value('client_id')),
            'KLADRCode': forceString(record.value('KLADRCode')),
        }

        if params['lpuCode'] == '037': # для МСЧ 118
            externalId = forceString(record.value('externalId'))

            if externalId:
                local_params['eventIdStr'] = externalId

        local_params['orgStructId'] = self.getActionPropertyValue(
              local_params['eventId'], self.actionTypeArrival,
              u'Направлен в отделение')
        local_params['infisInternalCode'] = (
            self.getOrgStructureInfisInternalCode(local_params['orgStructId']))
        local_params['orgStructInfis'] = self.getOrgStructureInfisCode(
                                                    local_params['orgStructId'])
        local_params['orgStructInfis'] = (0 if not local_params['orgStructInfis'
            ] else forceInt(local_params['orgStructInfis']))
        local_params['orgStructTfoms'] = self.getOrgStructureTfomsCode(
                                                    local_params['orgStructId'])
        local_params['orgStructTfoms'] = (0 if not local_params['orgStructTfoms'
            ] else forceInt(local_params['orgStructTfoms']))

        local_params['policySerial'] = forceString(record.value('policySerial'))
        local_params['policyNumber'] = forceString(record.value('policyNumber'))

        (dbfReestr, dbfDepRee, dbfAddInf, dbfOper, dbfDepAdd, dbfOnkSl,
         dbfBDiag, dbfBProt, dbfOnkUsl, _, dbfCons, _, dbfCrit, _) = dbf

        hospitalActionList = forceString(record.value(
            'hospitalActionId')).split(',')
        local_params.update(params)

        for x in hospitalActionList:
            hospitalActionId = forceRef(x)
            local_params['bedProfileId'] = None
            local_params['isIntensive'] = False

            if hospitalActionId:
                action = CAction.getActionById(hospitalActionId)
                bedId = forceRef(action[u'койка'])

                if bedId:
                    local_params['bedProfileId'] = (
                                        self.getHospitalBedProfileId(bedId))

                    bedTypeCode = (self.getHospitalBedTypeCode(
                        self.getHospitalBedTypeId(bedId)))
                    actRecord = action.getRecord()
                    local_params['isIntensive'] = bedTypeCode in ('2', '3')

                    if local_params['isIntensive']:
                        local_params['bedBegDate'] = forceDate(
                            actRecord.value('begDate'))
                        local_params['bedEndDate'] = forceDate(
                            actRecord.value('endDate'))
                        personId = forceRef(actRecord.value('person_id'))
                        local_params['bedPersonCode'] = self.getPersonRegionalCode(
                            personId)
                        bedPersonSpecialityRegionalCode = self.getPersonSpecialityRegionalCode(personId)
                        local_params['bedPersonSpecialityRegionalCode'] = forceInt(bedPersonSpecialityRegionalCode) if bedPersonSpecialityRegionalCode else 0
                        bedPersonSpecialityFederalCode = self.getPersonSpecialityFederalCode(personId)
                        local_params['bedPersonSpecialityFederalCode'] = forceInt(bedPersonSpecialityFederalCode) if bedPersonSpecialityFederalCode else 0
                        self._processDepAdd(dbfDepAdd, record, local_params)

        local_params['serviceNumber'] = 1

        if not local_params['KLADRCode']:
            self.log(u'Отсутвует КЛАДР адрес проживания и '
                u'регистрации для клиента clientId=%d' %
                local_params['clientId'])

        serviceCode = forceString(record.value('serviceCode'))
        serviceType = forceInt(record.value('serviceType'))

        self.mapEventIdtoIdCase[local_params['eventId']] = (
            params['rowNumber'] % 10000000000)

        if local_params['eventId'] not in params.setdefault(
                'exportedOperations', set()):
            for oper in params['operations'].get(local_params['eventId'], []):
                self._processOper(dbfOper, oper, local_params)

            params['exportedOperations'].add(local_params['eventId'])

        if ((serviceCode[:3] == u'А16'
                and params['exportType'] != self.exportTypeDS)
            or (serviceType == CActionServiceType.operation
                and params['exportType'] == self.exportTypeDS)):
            self._processOper(dbfOper, record, local_params) # операция
        else: # операции не должны попадать в реестр
            self._processReestr(dbfReestr, record, local_params)

        if params['exportType'] == self.exportTypeTFOMS:
            self._processAddInf(dbfAddInf, record, local_params)

        mkb = forceString(record.value('MKB'))
        accMKB = forceString(record.value('accMKB'))
        onkRecord = local_params['onkologyInfo'].get(local_params['eventId'])
        phaseCode = (forceInt(onkRecord.value('diseasePhaseCode')) if onkRecord else None)
        onkDiag = (mkb[:1] == 'C' or ('D00' <= mkb[:3] <= 'D09')
                   or (mkb[:3] == 'D70' and (
                    accMKB[:3] == 'C97' or 'C00' <= accMKB[:3] <= 'C80')))
        local_params['DS_ONK'] = 1 if (phaseCode == 10 and onkDiag) else 0
        if local_params['DS_ONK'] != 1 and onkDiag:
            self._processOnkSl(dbfOnkSl, record, local_params)
            self._processOnkUsl(dbfOnkUsl, record, local_params)
        if onkDiag:
            self._processCons(dbfCons, record, local_params)

        price = forceDouble(record.value('price'))
        if not price == 0.0:
            local_params['mkb'] = mkb
            self._processDepRee(dbfDepRee, record, local_params)
            if self.exportFormat >= self.exportFormat2020:
                self._processCrit(dbfCrit, record, local_params)

        params['rowNumber'] += 1


    def _processCons(self, dbf, _, params): #Задача №0010463:"ТФОМС Мурманск. Изменения по Приказу ФФОМС №285"
        u'Пишет Сведения о проведении консилиума'
        row = dbf.newRecord()
        row['NIB'] = params['eventIdStr']
        row['CARD'] = params['eventId']
        row['ID_CASE'] = self.mapEventIdtoIdCase.get(params['eventId'], 0)
        onkRecord = params['onkologyInfo'].get(params['eventId'])
        if onkRecord:
            row['PR_CONS'] = 0
            row['DT_CONS'] = ''
        row.store()


    def _processReestr(self, dbf, record, params):
        u"""Эспорт данных в REESTR.DBF"""

        row = dbf.newRecord()
        # Номер истории болезни   Не повторяется в отчетном году
        row['NIB'] = params['eventIdStr']
        # Код СМО (по справочнику фонда)
        row['INS'] = params.get('payerInfis', '')
        # Начальная дата интервала, за который представляется реестр
        row['DATA1'] = pyDate(firstMonthDay(params['endDate']))
         # Конечная дата интервала, за который представляется реестр
        exposeDate = params.get('exposeDate', QDate())
        row['DATA2'] = pyDate(exposeDate if exposeDate else QDate.currentDate())
         # Фамилия пациента
        row['FAM'] = forceString(record.value('lastName'))
         # Имя пациента
        row['IMM'] = forceString(record.value('firstName'))
        # Отчество пациента
        row['OTC'] = forceString(record.value('patrName'))
        # Серия документа, удостоверяющего личность
        row['SER_PASP'] = forceString(record.value('documentSerial'))
        # Номер документа, удостоверяющего личность
        row['NUM_PASP'] = forceString(record.value('documentNumber'))
        #, 'N', 2, Тип документа, удостоверяющего личность
        row['TYP_DOC'] = forceInt(record.value('documentRegionalCode'))
        # Страховой номер индивидуального лицевого счета (СНИЛС)
        row['SS'] = formatSNILS(forceString(record.value('SNILS')))
        # Дата рождения пациента
        row['DROJD'] = pyDate(forceDate(record.value('birthDate')))
        # Пол пациента   («М», «Ж»)
        row['POL'] = u'М' if forceInt(record.value('sex')) == 1 else u'Ж'
        # Признак работающий- “1”/неработающий – “0”
        row['RAB'] = '1' if forceString(record.value('workName')) else '0'
        row['SPOLIS'] = params['policySerial'] #, 'C', 10), # Серия полиса
        row['NPOLIS'] = params['policyNumber'] #, 'C', 10), # Номер полиса
        # Код населенного пункта проживания пациента по справочнику фонда
        row['TAUN'] = forceString(record.value('placeCode'))
        # Признак поступления экстренное –“1” /плановое –“0
        # У нас дневной стационар = 0
        row['HOSP'] = self.mapEventOrderToHosp.get(forceInt(
                                        record.value('eventOrder')), '')
        row['DATAP'] = pyDate(params['begDate']) # Дата поступления в ЛПУ
        row['DATAV'] = pyDate(params['endDate']) # Дата выписки из ЛПУ
        # Суммарная стоимость пребывания в ЛПУ
        row['STOIM'] = forceDouble(record.value('sum'))
        row['STOIM_S'] = row['STOIM']
        row['TPOLIS'] = forceInt(record.value('policyKind'))

        # Признак противоправных действий   0 – обычное СБО,
        # 1- противоправное действие.
        criminalSign = self.getActionPropertyText(params['eventId'],
                                self.actionTypeIllegalActions, u'Признак') \
                                if self.hasIllegalActionPropertyType else False

        if criminalSign:
            row['KRIM'] = criminalSign

        row['DIAG'] = forceString(record.value('MKB')) # Заключительный диагноз
        # Код ЛПУ, направившего на госпитализацию
        row['DIRECT_LPU'] = params.get('lpuCode', '')
        # Коды ЛПУ приписки по справочнику фонда
        # (поликлиника + стоматология +ЖК)
        # В строке через 3 пробела. Пример 103   160   121
        row['MASTER'] = forceString(record.value('attachCodeString'))
        # Код ЛПУ пребывания по справочнику фонда
        row['LPU'] = forceString(record.value('hospitalInfisCode'))
        # Номер счета представляемого в фонд
        row['COUNT'] = params.get('accNumber')

        if self.hasWeightActionPropertyType:
            try:
                row['VNOV_D'] = forceInt(self.getActionPropertyValue(
                    params['eventId'], self.actionTypeArrival, u'Вес')) % 10000
            except:
                pass

        relegateOrgTfomsExtCode = forceString(record.value(
            'relegateOrgTfomsExtCode'))
        relegateOrgSmoCode = forceString(record.value('relegateOrgSmoCode'))
        row['DIR_SUBLPU'] = (relegateOrgSmoCode if relegateOrgSmoCode
                         else forceString(record.value('attachOrgSmoCode')))
        row['DIR_TOWN'] = (relegateOrgTfomsExtCode if
            relegateOrgTfomsExtCode else
            forceString(record.value('attachOrgTfomsExtCode')))
        row['SUB_HOSP'] = forceString(record.value('subHospital'))
        row['TOWN_HOSP'] = params.get('accOrgStructTfomsCode', '')
        row['P_CODE'] = formatSNILS(record.value('execPersonSNILS'))
        row['NPR_DATE'] = pyDate(forceDate(record.value('srcDate')))
        row['DOCDATE'] = pyDate(forceDate(record.value('DOCDATE')))
        row['DOCORG'] = forceString(record.value('DOCORG'))[:250]
        row.store()


    def _processDepRee(self, dbf, record, params):
        u"""Экспорт информации в DEP_REE.DBF"""

        eventOrder = forceInt(record.value('eventOrder'))

        row = dbf.newRecord()
        row['NIB'] = params['eventIdStr'] # Номер истории болезни
        # Код отделения по справочнику фонда
        row['OTD'] = self.getOrgStructureInfisDepTypeCode(params['orgStructId'])
        medicalAidTypeCode = forceString(record.value('medicalAidTypeCode'))
        # Код отделения, откуда переведен пациент
        # (при переводе из одного отделения в другое отделение)
        row['DIRECT_OTD'] = self.getActionPropertyText(params['eventId'],
                        self.actionTypeMovement, u'Переведен из отделения')
        # Признак поступления экстренное – “1” /плановое – “0”
        # / перевод из отделения в отделение – “2”
        row['HOSP'] = '2' if row['DIRECT_OTD'] else '0'

        if row['HOSP'] == '0':
            row['HOSP'] = self.mapEventOrderToHosp.get(eventOrder, '0')

        row['DATAP'] = pyDate(params['begDate']) # Дата поступления  в отделение
        row['DATAV'] = pyDate(params['endDate']) # Дата выписки из отделения

        #'C', 8, Код врача лечившего пациента
        row['DOCTOR'] = formatSNILS(record.value('execPersonSNILS'))
        # Уровень оказанной помощи (“1”- дневные стационары,
        # “0” – стационары круглосуточного пребывания)
        row['LEVEL'] = '1' if (medicalAidTypeCode == '7'
                or params['exportType'] == self.exportTypeDializ) else '0'
        # 'C',6), № направления на госпитализацию
        row['TALON'] = self.getActionPropertyText(params['eventId'],
              self.actionTypeArrival, u'№ направления на госпитализацию')
        row['VID_HMP'] = self._getQuota(params['eventId'])
        # Код МКБ Х
        row['DIAG'] = forceString(record.value('MKB'))
        # Код диагноза сопутствующего заболевания (состояния) по МКБ-10
        row['DS_S'] = forceString(record.value('accMKB'))
        # Код профиля койки
        bedProfFieldName = ('PROFIL_K'
            if self.exportFormat >= self.exportFormat2020 else 'BED_PROF')
        row[bedProfFieldName] = self.getHospitalBedProfileRegionalCode(
                                                         params['bedProfileId'])
        if self.exportFormat >= self.exportFormat2020:
            row[bedProfFieldName] = forceInt(row[bedProfFieldName] if row[bedProfFieldName] else 0)

        row['STOIM_S'] = forceDouble(record.value('sum'))
        row['ID_CASE'] = params['rowNumber'] % 10000000000
        # Результат обращения/ госпитализации
        row['RSLT'] = forceInt(record.value(
            'eventResultRegionalCode')) % 1000
        # рофиль оказанной медицинской помощи
        row['ISHOD'] = forceInt(record.value('resultCode')) %1000
        # Профиль оказанной медицинской помощи
        row['PROFIL'] = (forceInt(params['infisInternalCode']
                            if params['infisInternalCode'] else 0)) % 1000
        # Код специальности медицинского работника, оказавшего услугу
        row['PRVS'] = params['orgStructTfoms'] % 1000

        # Код клинико-статистической группы
        row['KSG'] = forceString(record.value('ksgCode'))

        if row['RSLT'] in (102, 103, 104, 202, 203, 204):
            row['DS_P'] = forceString(record.value('accMKB'))


        row['VIDPOM'] = forceInt(record.value(
            'medicalAidKindCode')) % 10000
        row['VID_FIN'] = 1
        row['MOTHER'] = 0 # FIXME
        pMode = 1

        if params['exportType'] == self.exportTypeDS:
            pMode = 6

        row['P_MODE'] = pMode
        row['P_PER'] = 1
        row['PR_OS'] = 0
        try:
            row['NPL'] = forceInt(self.getActionPropertyValue(
                params['eventId'], self.actionTypeLeaved, 'NPL')) % 10
        except:
            pass

        row['ADD_CR_KSG'] = forceString(record.value('criterionCode'))
        row['IDSP'] = getIdsp(forceInt(record.value('medicalAidUnitCode')),
                              forceBool(record.value('isAttached')),
                              forceBool(record.value('isHomeVisit')))
        row['C_ZAB'] = forceInt(record.value('C_ZAB')) % 10
        row['ZS'] = 1 if forceInt(record.value('mesSpecificationLevel')) == 2 else 0   # Задача №0010463:"ТФОМС Мурманск. Изменения по Приказу ФФОМС №285" # Выгружаем 1
        if self.exportFormat >= self.exportFormat2021:
            row['SUB_HOSP'] = forceString(record.value('subHospital'))
        else:
            row['SUB_HOSP'] = params.get('accOrgStructInfisCode', '')
        row['DS_ONK'] = params['DS_ONK']

        if self.exportFormat >= self.exportFormat2020:
            row['mpcod'] = forceString(record.value('orgStructMpCod'))[:8]
            row['addr_code'] = forceString(record.value('orgStructAddrCode'))[:16]
        if (self.exportFormat >= self.exportFormat2021 and
                forceInt(record.value('phaseCode')) == 10):
            row['DS_PZ'] = params['mkb']

        row.store()


    def _processAddInf(self, dbf, record, params):
        u"""Экспорт информации в ADD_INF.DBF"""

        row = dbf.newRecord()

        row['NIB'] = params['eventIdStr'] # Номер истории болезни
        # Место рождения пациента или представителя
        row['MR'] = forceString(record.value('birthPlace'))

        # Код места жительства по ОКАТО
        row['OKATOG'] = forceString(record.value('regRegionOKATO'))
        # Код места пребывания по ОКАТО
        row['OKATOP'] = forceString(record.value('locRegionOKATO'))
        # Код ОКАТО территории страхования по ОМС (по справочнику фонда)
        row['OKATO_OMS'] = forceString(record.value('insurerOKATO'))
        # Статус представителя пациента
        info = self.getClientRepresentativeInfo(params['clientId'])

        # Фамилия родителя (представителя) пациента (п.2 Примечаний)
        if info != {}:
            row['FAMP'] = info.get('lastName', '')
            # Имя родителя (представителя) пациента (п.2 Примечаний)
            row['IMP'] = info.get('firstName', '')
            # Отчество родителя (представителя) пациента (п.2 Примечаний)
            row['OTP'] = info.get('patrName', '')
            # Дата рождения родителя (представителя) пациента
            row['DRP'] = pyDate(info.get('birthDate', QDate()))
            # Пол родителя (представителя) пациента
            row['WP'] = u'М' if info.get('sex', 1) == 1 else u'Ж'

        # Код типа документа, удостоверяющего личность пациента
        # (представителя) (по  справочнику фонда)
        row['C_DOC'] = forceInt(record.value('documentTypeRegionalCode'))
        #, 'C', 9), # Серия документа, удостоверяющего личность пациента
        # (представителя) (по  справочнику фонда)
        row['S_DOC'] = forceString(record.value('documentSerial'))
        # Номер документа, удостоверяющего личность пациента
        # (представителя) (по  справочнику фонда)
        row['N_DOC'] = forceString(record.value('documentNumber'))
        row['NOVOR'] = '' # Признак новорожденного
        specialCase = []
        row['Q_G'] = ' '.join(x for x in specialCase)
        row['MSE'] = 0
        row['DOCDATE'] = pyDate(forceDate(record.value('DOCDATE')))
        row['DOCORG'] = forceString(record.value('DOCORG'))[:250]
        row.store()


    def _processOper(self, dbf, record, params):
        u"""Экспорт информации в OPER.DBF"""
        actionId = forceRef(record.value('actionId'))

        if actionId in params.setdefault('exportedActions', set()):
            return

        row = dbf.newRecord()
        # Номер истории болезни
        row['NIB'] = params['eventIdStr']
        row['IDSERV'] = str(params['serviceNumber'])
        params['serviceNumber'] += 1

        # Порядковый номер случая в реестре
        row['ID_CASE'] = self.mapEventIdtoIdCase.get(params['eventId'], 0)
        # Код отделения, где проведена операция
        row['OTD_O'] = self.getOrgStructureInfisDepTypeCode(
                                                    params['orgStructId'])
        # Дата, когда проведена операция
        row['DATA_O'] = pyDate(forceDate(record.value('actionDate')))
        # Код операции
        row['OPER'] = forceString(record.value(params['operOperFieldName']))
        # Количество операций
        row['KOL_OPER'] = forceInt(record.value('amount')) % 10
        # Код врача лечившего пациента
        row['DOCTOR'] = forceString(record.value('personCode'))

        row['PRVS'] = forceInt(record.value('federalCodeExecPerson')) % 10000
        row['PROFIL'] = forceInt(record.value('regionalCodeExecPerson')) % 10000
        row['PR_OPER'] = (1 if forceString(
            record.value('serviceCode')) == u'A16.20.037' else 0)

        if self.exportFormat >= self.exportFormat2020:
            row['mpcod'] = forceString(record.value('orgStructMpCod'))[:8]
            row['addr_code'] = forceString(record.value('orgStructAddrCode'))[:16]

        row.store()
        params['exportedActions'].add(actionId)


    def _processDepAdd(self, dbf, record, params):
        u"""Экспорт информации в DEP_ADD.DBF"""

        row = dbf.newRecord()
        # Номер истории болезни
        row['NIB'] = forceString(params['eventId'])
        # Порядковый номер случая в реестре
        row['ID_CASE'] = params['rowNumber'] % 10000000000
        # Дата поступления пациента в отделение
        # интенсивной терапии и  реанимации
        row['DATE_1'] = pyDate(params['bedBegDate'])
        # Дата выбытия пациента из отделения
        # интенсивной терапии и  реанимации
        row['DATE_2'] = pyDate(params['bedEndDate'])
        # Диагноз основной
        row['DS'] = forceString(record.value('MKB'))
        # Код врача лечившего пациента
        row['DOCTOR'] = params['bedPersonCode']
        # Профиль оказанной медицинской помощи
        row['PROFIL'] = forceInt(record.value('federalCodeExecPerson')) % 10000
        # Код специальности медицинского работника,
        # оказавшего услугу
        row['PRVS'] = forceInt(record.value('regionalCodeExecPerson')) % 10000
        row.store()


# ******************************************************************************

    def _processOnkSl(self, dbf, record, params):
        u'Пишет cведения о случае лечения онкологического заболевания'
        row = dbf.newRecord()
        row['NIB'] = params['eventIdStr']
        row['ID_CASE'] = self.mapEventIdtoIdCase.get(params['eventId'], 0)
        onkRecord = params['onkologyInfo'].get(params['eventId'])

        if onkRecord:
            row['DS1_T'] = 6  #Задача №0010463:"ТФОМС Мурманск. Изменения по Приказу ФФОМС №285"

            for field in ('STAD', 'ONK_T', 'ONK_M', 'ONK_N'):
                row[field] = forceInt(onkRecord.value(field)) % 1000

            metastasisCode = forceString(onkRecord.value('metastasisCode'))
            row['MTSTZ'] = 1 if (metastasisCode and metastasisCode not in ('M0', 'Mx')) else 0 % 10
            row['SOD'] = forceDouble(onkRecord.value('SOD'))

        row.store()

# ******************************************************************************

    def _processBDiag(self, dbf, record, params):
        u'Пишет сведения о проведенных исследованиях и их результатах'
        row = dbf.newRecord()
        row['NIB'] = params['eventIdStr']
        row['ID_CASE'] = self.mapEventIdtoIdCase.get(params['eventId'], 0)
        onkRecord = params['onkologyInfo'].get(params['eventId'])

        if onkRecord:
            row['DIAG_TIP'] = forceInt(onkRecord.value('DIAG_TIP')) % 10

            gistologiaActionId = forceRef(onkRecord.value(
                'gistologiaActionId'))
            immunohistochemistryActionidId = forceRef(onkRecord.value(
                'immunohistochemistryActionId'))
            action = CAction.getActionById((
                gistologiaActionId if gistologiaActionId else
                    immunohistochemistryActionidId))

            if action:
                actionProperty = action.getProperties()[0]
                text = actionProperty.getTextScalar()
                descr = forceInt(actionProperty.type().descr)
            else:
                text = None
                descr = 0

            row['DIAG_CODE'] = descr % 1000
            row['DIAG_RSLT'] = mapDiagRslt.get((descr, text), 0) % 100
            row['REC_RSLT'] = ''

        row.store()

# ******************************************************************************

    def _processBProt(self, dbf, record, params):
        u'Пишет сведения об имеющихся противопоказаниях и отказах'
        row = dbf.newRecord()
        row['NIB'] = params['eventIdStr']
        row['ID_CASE'] = self.mapEventIdtoIdCase.get(params['eventId'], 0)
        onkRecord = params['onkologyInfo'].get(params['eventId'])
        if onkRecord:
            action = CAction.getActionById(forceRef(onkRecord.value(
                'controlListOnkoActionId')))
            prop = (action['PROT'] if action and action.hasProperty('PROT')
                    else None)

            if prop:
                row['PROT'] = prop.type().descr % 10
                row['D_PROT'] = prop.getValueScalar()


        row.store()

# ******************************************************************************

    def _processOnkUsl(self, dbf, record, params):
        u'Пишет сведения об услуге при лечении онкологического заболевания'
        row = dbf.newRecord()
        row['NIB'] = params['eventIdStr']
        row['ID_CASE'] = self.mapEventIdtoIdCase.get(params['eventId'], 0)
        row['IDSERV'] = forceString(params['serviceNumber'])
        onkRecord = params['onkologyInfo'].get(params['eventId'])

        if onkRecord:
            action = CAction.getActionById(forceRef(record.value(
                'controlListOnkoActionId')))
            if action:
                row['USL_TIP'] = action['ID_TLECH'].getValue() % 10

                if row['USL_TIP'] == 1:
                    row['HIR_TIP'] = action['ID_THIR'].getValue()
                else:
                    row['LUCH_TIP'] = action['ID_TLUCH'].getValue()

                row['LEK_TIP_L'] = action['ID_TLEK_L'].getValue()
                row['LEK_TIP_V'] = action['ID_TLEK_V'].getValue()
            else:
                row['USL_TIP'] = 6
                row['HIR_TIP'] = 0
                row['LUCH_TIP'] = 0
                row['LEK_TIP_L'] = 0
                row['LEK_TIP_V'] = 0

        row.store()


    def _processCrit(self, dbf, record, params):
        u"""Экспорт информации в CRIT_KSG.DBF"""
        eventId = params['eventId']
        critList = self._critDict.get(eventId, [])
        for code in critList:
            row = dbf.newRecord()
            row['NIB'] = params['eventIdStr']
            row['ID_CASE'] = self.mapEventIdtoIdCase.get(eventId, 0)
            row['CRIT'] = code
            row.store()


    def _getCritDict(self):
        result = {}
        stmt = """SELECT Event.id, GROUP_CONCAT(DISTINCT ActionType.code SEPARATOR ',')
        FROM Account_Item
            LEFT JOIN Event ON Account_Item.event_id = Event.id
            LEFT JOIN Action ON Action.event_id = Event.id
            LEFT JOIN ActionType ON Action.actionType_id = ActionType.id
            LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
            WHERE Account_Item.reexposeItem_id IS NULL
              AND Action.deleted = 0
              AND ActionType.flatCode = 'AddCriterion'
              AND (Account_Item.date IS NULL OR
                   (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
              AND {idList}
            GROUP BY Event.id""".format(
                idList=self.tableAccountItem['id'].inlist(self.idList))
        query = self.db.query(stmt)
        while query.next():
            record = query.record()
            eventId = forceRef(record.value(0))
            critList = forceString(record.value(1)).split(',')
            result[eventId] = critList
        return result

# ******************************************************************************

class CExportPage2(CAbstractExportPage2):
    u"""Вторая страница мастера экспорта"""

    def __init__(self, parent):
        CAbstractExportPage2.__init__(self, parent, 'ExportR51Hospital')


    def saveExportResults(self):
        fileList = ('REESTR.DBF', 'DEP_REE.DBF', 'DEP_ADD.DBF', 'ADD_INF.DBF',
                    'ONK_SL.DBF', 'ONK_USL.DBF', 'B_DIAG.DBF', 'B_PROT.DBF',
                    'LEK_PR.DBF', 'CONS.DBF', 'NAPR.DBF')
        exportType = self._parent.page1.cmbExportType.currentIndex()
        exportFormat = self._parent.page1.cmbExportFormat.currentIndex()

        if exportType != CExportPage1.exportTypeDS:
            fileList += ('OPER.DBF', )

        if exportFormat >= CExportPage1.exportFormat2020:
            fileList += ('CRIT_KSG.DBF', 'SERV_TMT.DBF')

        return self.moveFiles(fileList)

# ******************************************************************************

if __name__ == '__main__':
    #pylint: disable=wrong-import-position,ungrouped-imports
    from Exchange.Utils import testAccountExport
    #pylint: enable=wrong-import-position,ungrouped-imports
    testAccountExport(exportR51Hospital, u'17_субвенция-199', '75_38_s11.ini',
                      [4477316])
