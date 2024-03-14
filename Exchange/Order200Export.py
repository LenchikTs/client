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

u"""Экспорт реестра  в по 200 приказу, общая часть"""

from PyQt4 import QtGui
from PyQt4.QtCore import Qt, QDate

from Events.Action import CAction

from library.DbEntityCache import CDbEntityCache
from library.Utils import forceInt, forceString, forceRef, forceDate


mapDiagRslt = {
    u'Эпителиальный': 1,
    u'Неэпителиальный': 2,
    u'Светлоклеточный': 3,
    u'Несветлоклеточный': 4,
    u'Низкодифференцированная': 5,
    u'Умереннодифференцированная': 6,
    u'Высокодифференцированная': 7,
    u'Не определена': 8,
    u'Мелкоклеточный': 9,
    u'Немелкоклеточный': 10,
    u'Почечноклеточный': 11,
    u'Не почечноклеточный': 12,
    u'Папиллярный': 13,
    u'Фолликулярный': 14,
    u'Гюртклеточный': 15,
    u'Медуллярный': 16,
    u'Анапластический': 17,
    u'Базальноклеточный': 18,
    u'Не базальноклеточный': 19,
    u'Плоскоклеточный': 20,
    u'Не плоскоклеточный': 21,
    u'Эндометриоидные': 22,
    u'Не эндометриоидные': 23,
    u'Аденокарцинома': 24,
    u'Не аденокарцинома': 25,

    u'Наличие мутаций в гене BRAF': 4,
    u'Отсутствие мутаций в гене BRAF': 5,
    u'Наличие мутаций в гене c-Kit': 6,
    u'Отсутствие мутаций в гене c-Kit': 7,
    u'Исследование не проводилось': 8,
    u'Наличие мутаций в гене RAS': 9,
    u'Отсутствие мутаций в гене RAS': 10,
    u'Наличие мутаций в гене EGFR': 11,
    u'Отсутствие мутаций в гене EGFR': 12,
    u'Наличие транслокации в генах ALK или ROS1': 13,
    u'Отсутствие транслокации в генах ALK и ROS1': 14,
    u'Повышенная экспрессия белка PD-L1': 15,
    u'Отсутствие повышенной экспрессии белка PD-L1': 16,
    u'Наличие рецепторов к эстрогенам': 17,
    u'Отсутствие рецепторов к эстрогенам': 18,
    u'Наличие рецепторов к прогестерону': 19,
    u'Отсутствие рецепторов к прогестерону': 20,
    u'Высокий индекс пролиферативной активности экспрессии Ki-67' : 21,
    u'Низкий индекс пролиферативной активности экспрессии Ki-67' : 22,
    u'Гиперэкспрессия белка HER2': 23,
    u'Отсутствие гиперэкспрессии белка HER2': 24,
    u'Наличие мутаций в генах BRCA': 25,
    u'Отсутствие мутаций в генах BRCA': 26,
}

mapPrCons = {
    u'определена тактика обследования': 1,
    u'определена тактика лечения': 2,
    u'изменена тактика лечения': 3,
}

mapUslTip = {
    u'Хирургическое лечение': 1,
    u'Лекарственная противоопухолевая терапия': 2,
    u'Лучевая терапия': 3,
    u'Химиолучевая терапия': 4,
    u'Неспецифическое лечение': 5,
    u'ДИАГНОСТИКА': 6
}

mapHirTip = {
    u'Первичной опухоли, в том числе с удалением регионарных '
    u'лимфатических узлов' : 1,
    u'Метастазов': 2,
    u'Симптоматическое': 3,
    u'Выполнено хирургическое стадирование (может указываться при раке яичника '
    u'вместо 1)': 4,
    u'Регионарных лимфатических узлов без первичной опухоли' : 5,
    u'Симптоматическое, то реконструктивно-пластическое, хирургическая '
    u'овариальная суперссия, прочее': 3,
    u'КРИОХИРУРГИЯ/КРИОТЕРАПИЯ, ЛАЗЕРНАЯ ДЕСТРУКЦИЯ, '
    u'ФОТОДИНАМИЧЕСКАЯ ТЕРАПИЯ': 6
}

mapLekTipL = {
    u'Первая линия': 1,
    u'Вторая линия': 2,
    u'Третья линия': 3,
    u'Линия после третьей': 4
}

mapLekTipV = {
    u'Первый цикл линии': 1,
    u'Последующие циклы линии (кроме последнего)': 2,
    u'Последний цикл линии (лечение прервано)': 3,
    u'Последний цикл линии (лечение завершено)': 4,
}

mapLuchTip = {
    u'Первичной опухоли / ложа опухоли': 1,
    u'Первичной опухоли/ложа опухоли': 1,
    u'Метастазов': 2,
    u'Симптоматическая': 3,
}

mapMetIssl = {
    u'на лабораторную диагностику': 1,
    u'лабораторная диагностика': 1,
    u'на инструментальную диагностику': 2,
    u'инструментальная диагностика': 2,
    u'на лучевую диагностику (кроме дорогостоящих)': 3,
    u'методы лучевой диагностики, за исключением дорогостоящих': 3,
    u'на ангиографию': 4,
    u'дорогостоящие методы лучевой диагностики (КТ, МРТ, ангиография)': 4,
}

mapPptr = {
    u'проводилась': '0',
    u'не проводилась': '1',
}

mapOnkUsl = {
    u'Проведение консилиума': ('ONK_USL_PR_CONS', mapPrCons),
    u'PR_CONS': ('ONK_USL_PR_CONS', mapPrCons),
    u'Тип услуги': ('ONK_USL_USL_TIP', mapUslTip),
    u'ID_TLECH': ('ONK_USL_USL_TIP', mapUslTip),
    u'Тип хирургического лечения':('ONK_USL_HIR_TIP', mapHirTip),
    u'ID_THIR': ('ONK_USL_HIR_TIP', mapHirTip),
    u'Линия лекарственной терапии': ('ONK_USL_LEK_TIP_L', mapLekTipL),
    u'ID_TLEK_L': ('ONK_USL_LEK_TIP_L', mapLekTipL),
    u'Цикл лекарственной терапии': ('ONK_USL_LEK_TIP_V', mapLekTipV),
    u'ID_TLEK_V': ('ONK_USL_LEK_TIP_V', mapLekTipV),
    u'Тип лучевой терапии': ('ONK_USL_LUCH_TIP', mapLuchTip),
    u'ID_TLUCH': ('ONK_USL_LUCH_TIP', mapLuchTip),
}


# ******************************************************************************

class COnkologyInfo():
    def __init__(self):
        pass


    def _onkologyMkbStmt(self):
        u'Возвращает sql фильтр для онкологических диагнозов'
        return u"""DS.MKB LIKE 'C%' OR DS.MKB BETWEEN 'D01' AND 'D09' OR DS.MKB = 'D70'"""


    def get(self, _db, idList, parent):
        u"""Возвращает словарь с записями по онкологии и направлениям,
            ключ - идентификатор события"""
        stmt = u"""SELECT Event.id AS eventId,
            rbDiseasePhases.code AS diseasePhaseCode,
            rbEventTypePurpose.regionalCode AS uslOk,
            Diagnosis.MKB,
            AccDiagnosis.MKB AS accMKB,
            IF(GistologiaAction.id IS NOT NULL, 1,
                IF(ImmunohistochemistryAction.id IS NOT NULL, 2,
                    0)) AS DIAG_TIP,
            rbTNMphase_Identification.value AS STAD,
            rbTumor_Identification.value AS ONK_T,
            rbNodus_Identification.value AS ONK_N,
            rbMetastasis_Identification.value AS ONK_M,
            GistologiaAction.id AS gistologiaActionId,
            ImmunohistochemistryAction.id AS immunohistochemistryActionId,
            ControlListOnkoAction.id AS controlListOnkoActionId,
            (SELECT GROUP_CONCAT(A.id)
                FROM Action A
                WHERE A.event_id = Event.id
                  AND A.deleted = 0
                  AND A.actionType_id IN (
                    SELECT AT.id
                    FROM ActionType AT
                    WHERE AT.flatCode ='Consilium'
            )) AS consiliumActionId,
            (SELECT GROUP_CONCAT(A.id)
             FROM Action A
             WHERE A.event_id = Event.id
               AND A.deleted = 0
               AND A.actionType_id IN (
                 SELECT MAX(AT.id)
                 FROM ActionType AT
                 WHERE AT.flatCode = 'directionCancer'
            )) AS directionActionId,
            IF(rbMedicalAidType.code = '6',
                IF(rbDispanser.observed = 1, '1.3',
                    EventType_Identification.value), '') AS pCel,
            (SELECT GROUP_CONCAT(A.id)
             FROM Action A
             WHERE A.event_id = Event.id
               AND A.deleted = 0
               AND A.actionType_id IN (
                 SELECT MAX(AT.id)
                 FROM ActionType AT
                 WHERE AT.flatCode = 'MedicalSupplies')
             ORDER BY A.begDate
            ) AS medicalSuppliesActionId,
            (SELECT AT.code
                FROM Action A
                INNER JOIN ActionType AT ON A.actionType_id = AT.id
                        AND AT.group_id IN (
                            SELECT id FROM ActionType AT1
                            WHERE AT1.flatCode IN ('codeSH', 'МНН ЛП в сочетании с ЛТ'))
                WHERE A.event_id = Event.id AND A.deleted = 0
                LIMIT 0,1
            ) AS LEK_PR_CODE_SH,
            KFrAction.id AS kFrActionId
        FROM Account_Item
        LEFT JOIN rbPayRefuseType ON rbPayRefuseType.id = Account_Item.refuseType_id
        LEFT JOIN Event ON Event.id = Account_Item.event_id
        LEFT JOIN EventType ON EventType.id = Event.eventType_id
        LEFT JOIN Diagnostic ON Diagnostic.id = (
            SELECT D.id FROM Diagnostic D
            LEFT JOIN Diagnosis DS ON DS.id = D.diagnosis_id
            WHERE D.event_id = Account_Item.event_id
              AND D.deleted = 0 AND DS.deleted = 0
              AND ({mkbStmt})
              ORDER BY pTNMphase_id DESC, pTumor_id DESC, pNodus_id DESC,pMetastasis_id DESC, cTNMphase_id DESC, cTumor_id DESC, cNodus_id DESC, cMetastasis_id DESC LIMIT 1)
        LEFT JOIN Diagnosis ON Diagnosis.id = Diagnostic.diagnosis_id
        LEFT JOIN Diagnostic AS AccDiagnostic ON AccDiagnostic.id = (
            SELECT D.id FROM Diagnostic D
            LEFT JOIN Diagnosis DS ON DS.id = D.diagnosis_id
            LEFT JOIN rbDiagnosisType DT ON DT.id = D.diagnosisType_id
            WHERE D.event_id = Account_Item.event_id
              AND D.deleted = 0 AND DS.deleted = 0
              AND DT.code = '9' AND DS.MKB LIKE 'C%'
              ORDER BY pTNMphase_id DESC, pTumor_id DESC, pNodus_id DESC,pMetastasis_id DESC, cTNMphase_id DESC, cTumor_id DESC, cNodus_id DESC, cMetastasis_id DESC LIMIT 1)
        LEFT JOIN Diagnosis AS AccDiagnosis ON AccDiagnosis.id = AccDiagnostic.diagnosis_id
            AND AccDiagnosis.deleted = 0 AND (AccDiagnosis.MKB LIKE 'C%')
        LEFT JOIN Diagnostic AnyDiagnostic ON AnyDiagnostic.id = IFNULL(Diagnostic.id, AccDiagnostic.id)
        LEFT JOIN rbDiseasePhases ON AnyDiagnostic.phase_id = rbDiseasePhases.id
        LEFT JOIN rbTNMphase ON rbTNMphase.id = IFNULL(AnyDiagnostic.pTNMphase_id, AnyDiagnostic.cTNMphase_id)
        LEFT JOIN rbTumor ON rbTumor.id = IFNULL(AnyDiagnostic.pTumor_id, AnyDiagnostic.cTumor_id)
        LEFT JOIN rbNodus ON rbNodus.id = IFNULL(AnyDiagnostic.pNodus_id, AnyDiagnostic.cNodus_id)
        LEFT JOIN rbMetastasis ON rbMetastasis.id = IFNULL(AnyDiagnostic.pMetastasis_id, AnyDiagnostic.cMetastasis_id)
        LEFT JOIN rbEventTypePurpose ON rbEventTypePurpose.id = EventType.purpose_id
        LEFT JOIN Action AS GistologiaAction ON GistologiaAction.id = (
            SELECT MAX(A.id)
            FROM Action A
            WHERE A.event_id = Event.id
              AND A.deleted = 0
              AND A.actionType_id = (
                SELECT MAX(AT.id)
                FROM ActionType AT
                WHERE AT.flatCode ='Gistologia'
              )
        )
        LEFT JOIN Action AS ImmunohistochemistryAction ON ImmunohistochemistryAction.id = (
            SELECT MAX(A.id)
            FROM Action A
            WHERE A.event_id = Event.id
              AND A.deleted = 0
              AND A.actionType_id IN (
                SELECT AT.id
                FROM ActionType AT
                WHERE AT.flatCode ='Immunohistochemistry'
              )
        )
        LEFT JOIN Action AS ControlListOnkoAction ON ControlListOnkoAction.id = (
            SELECT MAX(A.id)
            FROM Action A
            WHERE A.event_id = Event.id
              AND A.deleted = 0
              AND A.actionType_id IN (
                SELECT AT.id
                FROM ActionType AT
                WHERE AT.flatCode ='ControlListOnko'
              )
        )
        LEFT JOIN rbDispanser ON AnyDiagnostic.dispanser_id = rbDispanser.id
        LEFT JOIN EventType_Identification ON
            EventType_Identification.master_id = EventType.id
            AND EventType_Identification.system_id = (
            SELECT MAX(id) FROM rbAccountingSystem
            WHERE rbAccountingSystem.code = 'tfomsPCEL'
        )
        LEFT JOIN rbMedicalAidType ON rbMedicalAidType.id = EventType.medicalAidType_id
        LEFT JOIN rbTNMphase_Identification ON
            rbTNMphase_Identification.master_id = IFNULL(
                AnyDiagnostic.cTNMphase_id, AnyDiagnostic.pTNMphase_id)
            AND rbTNMphase_Identification.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE rbAccountingSystem.code = 'TNMphase'
            )
        LEFT JOIN rbTumor_Identification ON
            rbTumor_Identification.master_id = IFNULL(
                AnyDiagnostic.cTumor_id, AnyDiagnostic.pTumor_id)
            AND rbTumor_Identification.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE rbAccountingSystem.code = 'Tumor'
            )
        LEFT JOIN rbNodus_Identification ON
            rbNodus_Identification.master_id = IFNULL(
                AnyDiagnostic.cNodus_id, AnyDiagnostic.pNodus_id)
            AND rbNodus_Identification.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE rbAccountingSystem.code = 'Nodus'
            )
        LEFT JOIN rbMetastasis_Identification ON
            rbMetastasis_Identification.master_id = IFNULL(
                AnyDiagnostic.cMetastasis_id, AnyDiagnostic.pMetastasis_id)
            AND rbMetastasis_Identification.system_id = (
                SELECT MAX(id) FROM rbAccountingSystem
                WHERE rbAccountingSystem.code = 'Metastasis'
            )
        LEFT JOIN Action AS KFrAction ON KFrAction.id = (
            SELECT MAX(A.id)
            FROM Action A
            WHERE A.event_id = Event.id
              AND A.deleted = 0
              AND A.actionType_id IN (
                SELECT AT.id
                FROM ActionType AT
                WHERE AT.group_id IN (
                    SELECT AT1.id FROM ActionType AT1
                    WHERE AT1.flatCode ='DiapFR')
              )
        )
        WHERE Account_Item.reexposeItem_id IS NULL
          AND (Diagnosis.MKB IS NOT NULL OR AccDiagnosis.MKB IS NOT NULL)
          AND (Account_Item.date IS NULL OR
               (Account_Item.date IS NOT NULL AND rbPayRefuseType.rerun != 0))
          AND {idList}
        GROUP BY Account_Item.event_id""" .format(
            idList=idList, mkbStmt=self._onkologyMkbStmt())

        query = _db.query(stmt)
        result = {}

        while query.next():
            record = query.record()
            eventId = forceRef(record.value('eventId'))
            result[eventId] = self._processOnkRecord(record, parent)

        return result

    __mapDirection__ = {
        u'Направление к онкологу' : 1,
        u'Направление на биопсию': 2,
        u'Направление на дообследование': 3,
        u'на биопсию': 2,
    }

    __mapPrCons__ = {
        u'отсутствует необходимость проведения консилиума': 0,
        u'определена тактика обследования': 1,
        u'определена тактика лечения': 2,
        u'изменена тактика лечения': 3,
        u'консилиум не проведен при наличии необходимости его проведения': 4,
        u'консилиум не проводился': 4
    }

    __mapPropDescr__ = {
        u'WEI': u'ONK_SL_WEI',
        u'HEI': u'ONK_SL_HEI',
        u'BSA': u'ONK_SL_BSA',
    }

    __keysToCheck__ = ('ONK_SL_STAD', 'ONK_SL_ONK_T',
                       'ONK_SL_ONK_N', 'ONK_SL_ONK_M')

    __mapDS1T__ = {
        u'Первичное лечение (лечение пациента за исключением прогрессирования и '
        u'рецидива)': 0,
        u'Лечение при рецидиве': 1,
        u'Лечение при прогрессировании': 2,
        u'Динамическое наблюдение': 3,
        u'Диспансерное наблюдение (здоров/ремиссия)': 4,
        u'Диагностика (при отсутствии специфического лечения)': 5,
        u'Симптоматическое лечение': 6,
    }


    def _isOnkology(self, record):
        mkb = forceString(record.value('MKB'))[:3]
        accMkb = forceString(record.value('accMKB'))[:3]
        phase = forceInt(record.value('diseasePhaseCode'))

        isNeutropenic = (mkb == 'D70' and (
            (accMkb >= 'C00' and accMkb <= 'C80') or accMkb == 'C97'))
        dsOnk = (1 if (phase == 10 and (
            mkb[:1] == 'C' or isNeutropenic or
            (mkb[:3] >= 'D01' and mkb [:3] <= 'D09'))) else 0)
        isOnkology = (mkb[:1] == 'C' or (
                (mkb[:3] >= 'D01' and mkb [:3] <= 'D09') or isNeutropenic)
            ) and dsOnk == 0
        return dsOnk, isOnkology


    def _processOnkRecord(self, record, parent):
        u'Обрабатывает записи из запроса getOnkologyInfo()'
        data = {}
        data['SL_DS_ONK'], data['isOnkology'] = self._isOnkology(
            record)

        data['uslOk'] = forceInt(record.value('uslOk'))

        if data['isOnkology']:
            data['ONK_SL_STAD'] = forceString(record.value('STAD'))
            data['ONK_SL_ONK_T'] = forceString(record.value('ONK_T'))
            data['ONK_SL_ONK_N'] = forceString(record.value('ONK_N'))
            data['ONK_SL_ONK_M'] = forceString(record.value('ONK_M'))

            _id = forceRef(record.value('kFrActionId'))
            action = CAction.getActionById(_id) if _id else None

            if action and action.getProperties():
                data['ONK_SL_K_FR'] = action.getProperties()[0].getValueScalar()

            for key in self.__keysToCheck__:
                if data[key]:
                    break
            else:
                for key in self.__keysToCheck__:
                    data.pop(key)

            self._processControlList(record, data)
            self._processDiagnostics(record, data)
            self._removeUnnessesaryFields(data)

            serviceType = data.get('ONK_USL_USL_TIP')
            SUPPLIES_SERVICE_TYPE = (2, 4, '2', '4')
            if ((isinstance(serviceType, list)
                 and any(x in serviceType for x in SUPPLIES_SERVICE_TYPE))
                or serviceType in SUPPLIES_SERVICE_TYPE):
                self._processMedicalSupplies(record, data)

        self._processDirection(record, data, parent)
        self._processConsilium(record, data)

        if data['isOnkology']:
            data['ONK_SL_MTSTZ'] = (1 if data.get('ONK_SL_DS1_T') in (1, 2)
                                    else None)
        return data

    def _removeUnnessesaryFields(self, data):
        u'Убирает ненужные поля для разных типов услуг'

        if data.get('ONK_USL_USL_TIP') != 1:
            data['ONK_USL_HIR_TIP'] = None

        if data.get('ONK_USL_USL_TIP') not in (3, 4):
            data['ONK_SL_K_FR'] = None
            data['ONK_SL_SOD'] = None
            data['ONK_USL_LUCH_TIP'] = None
        elif data.get('ONK_SL_K_FR') is None:
            data['ONK_SL_K_FR'] = '0'

        if data.get('ONK_USL_USL_TIP') != 2:
            data['ONK_USL_LEK_TIP_L'] = None
            data['ONK_USL_LEK_TIP_V'] = None

        if data.get('ONK_USL_USL_TIP') not in (2, 4):
            data['ONK_USL_PPTR'] = None
            data['ONK_SL_WEI'] = None
            data['ONK_SL_BSA'] = None
            data['ONK_SL_HEI'] = None


    def _processControlList(self, record, data):
        u'Заполняет поля из контрольного листка'
        _id = forceRef(record.value('controlListOnkoActionId'))
        action = CAction.getActionById(_id) if _id else None

        if action:
            for prop in action.getProperties():
                shortName = prop.type().shortName
                name = prop.type().name

                if shortName == 'PROT':
                    date = prop.getValueScalar()

                    if date is not None and isinstance(date,  QDate) and date.isValid() and prop.type().descr:
                        data.setdefault('B_PROT_PROT', []).append(
                            prop.type().descr)
                        data.setdefault('B_PROT_D_PROT', []).append(date)
                if (shortName in ('SOD', u'Суммарная очаговая доза')
                        or name in ('SOD', u'Суммарная очаговая доза')):
                    data['ONK_SL_SOD'] = prop.getValueScalar()
                elif ((mapOnkUsl.has_key(shortName) or
                       mapOnkUsl.has_key(name))):
                    fieldName, mapName = mapOnkUsl.get(
                        shortName, mapOnkUsl.get(name))
                    data[fieldName] = mapName.get(prop.getTextScalar())
                elif self.__mapPropDescr__.has_key(prop.type().descr):
                    data[self.__mapPropDescr__[prop.type().descr]] = prop.getValue()
                elif prop.type().descr == 'PPTR':
                    val = prop.getValue()
                    if val:
                        data['ONK_SL_PPTR'] = mapPptr.get(val.lower())
                elif prop.type().descr == 'DS1_T':
                    data['ONK_SL_DS1_T'] = self.__mapDS1T__.get(prop.getValue())


    def _processDiagnostics(self, record, data):
        u'Заполняет поля для диагностик'
        for field, diagType in (('gistologiaActionId', 1),
                                ('immunohistochemistryActionId', 2)):
            _id = forceRef(record.value(field))
            action = CAction.getActionById(_id) if _id else None

            if not (action and action.getProperties()):
                continue

            diagDate = None

            for prop in action.getProperties():
                if forceString(prop.type().descr) == 'DIAG_DATE':
                    val = prop.getValue()

                    if val and val.isValid():
                        diagDate = val.toString(Qt.ISODate)

                    continue

                text = prop.getTextScalar().strip()
                descr = forceString(prop.type().descr).strip()

                if not text or not descr:
                    continue

                data.setdefault('B_DIAG_DIAG_DATE', []).append(diagDate)
                data.setdefault('B_DIAG_DIAG_TIP', []).append(diagType)
                data.setdefault('B_DIAG_DIAG_CODE', []).append(descr)
                rslt = mapDiagRslt.get(text, 0)
                data.setdefault('B_DIAG_DIAG_RSLT', []).append(rslt)
                data.setdefault('B_DIAG_REC_RSLT', []).append(
                    1 if rslt else None)


    def _processMedicalSupplies(self, record, data):
        u'Заполняет поля для медикаментов'
        idList = forceString(record.value(
            'medicalSuppliesActionId')).split(',')
        nomenclatureDict = {}

        for i in idList:
            _id = forceRef(i)
            action = CAction.getActionById(_id) if _id else None

            if action:
                nomenclatureCode = None
                for prop in action.getProperties():
                    if prop.type().typeName == u'Номенклатура ЛСиИМН':
                        nomenclatureCode = (
                            CTfomsNomenclatureCache.getCode(
                                prop.getValue()))

                for prop in action.getProperties():
                    if prop.type().descr == 'DATE_INJ':
                        val = prop.getValue()
                        nomenclatureDict.setdefault(
                            nomenclatureCode, []).append(
                                val.toString(Qt.ISODate) if val else None)
                else:
                    if nomenclatureCode:
                        nomenclatureDict.setdefault(
                            nomenclatureCode, []).append(None)

        codeSH = forceString(record.value('LEK_PR_CODE_SH'))

        for key, val in nomenclatureDict.iteritems():
            data.setdefault('LEK_PR_REGNUM', []).append(key if key else '-')
            data.setdefault('LEK_PR_DATE_INJ', []).append(val)
            data.setdefault('LEK_PR_CODE_SH', []).append(codeSH)

        return data


    def _processDirection(self, record, data, parent):
        u'Заполняет поля для направлений'
        actionIdList = forceString(record.value(
            'directionActionId'))
        actionIdList = actionIdList.split(',') if actionIdList else []

        for actionId in actionIdList:
            action = CAction.getActionById(forceRef(actionId))
            directionDate = forceDate(action.getRecord().value('endDate'))
            directionOrgId = forceRef(action.getProperty(
                u'Куда направляется').getValue()) if action.hasProperty(
                    u'Куда направляется') else None
            data.setdefault('NAPR_NAPR_MO', []).append(
                COrganisationMiacCodeCache.getCode(
                    directionOrgId if directionOrgId !=
                    QtGui.qApp.currentOrgId() else None))

            if directionDate.isValid():
                data.setdefault('NAPR_NAPR_DATE', []).append(directionDate)
            else:
                data.setdefault('NAPR_NAPR_DATE', []).append(None)

            if action:
                if action.hasProperty(u'Профиль'):
                    bedProfileId = action.getProperty(u'Профиль').getValue()
                    code = parent.getHospitalBedProfileUsishCode(
                        bedProfileId)
                    if code == '43':
                        data.setdefault('NAPR_NAPR_V', []).append(1)
                elif action.hasProperty(u'Вид направления'):
                    val = action.getProperty(
                        u'Вид направления').getTextScalar()
                    data.setdefault('NAPR_NAPR_V', []).append(
                        self.__mapDirection__.get(val, 3))
                else:
                    data.setdefault('NAPR_NAPR_V', []).append(None)

                if (data.get('NAPR_NAPR_V', [])[-1] == 3 and
                        action.hasProperty(
                            u'Метод диагностического исследования')):
                    val = action.getProperty(
                        u'Метод диагностического исследования').getValue()
                    data.setdefault('NAPR_MET_ISSL', []).append(
                        mapMetIssl.get(val))
                else:
                    data.setdefault('NAPR_MET_ISSL', []).append(None)

                if (data.get('NAPR_NAPR_V', [0])[-1] == 3 and data.get(
                        'NAPR_MET_ISSL', [0])[-1] in (1, 2, 3, 4) and
                        action.hasProperty(u'Код услуги')):
                    prop = action.getProperty(u'Код услуги')
                    data.setdefault('NAPR_NAPR_USL', []).append(
                        prop.getValue())
                else:
                    data.setdefault('NAPR_NAPR_USL', []).append(None)


    def _processConsilium(self, record, data):
        u'Заполняет поля для консилиума'

        actionIdList = forceString(record.value(
            'consiliumActionId'))
        actionIdList = actionIdList.split(',') if actionIdList else []

        for actionId in actionIdList:
            action = CAction.getActionById(forceRef(actionId))

            if action:
                flag = False
                for prop in action.getProperties():
                    descr = forceString(prop.type().descr)
                    shortName = forceString(prop.type().shortName)
                    if descr == 'PR_CONS' or shortName == 'PR_CONS':
                        val = self.__mapPrCons__.get(forceString(
                            prop.getValue()).lower())
                        if val is not None:
                            data.setdefault('CONS_PR_CONS', []).append(val)
                            flag = True
                            break

                if flag and data.get('CONS_PR_CONS')[-1] in (1, 2, 3):
                    data.setdefault('CONS_DT_CONS', []).append(
                        forceDate(action.getRecord().value('endDate')).toString(
                            Qt.ISODate))


# ******************************************************************************

class COrganisationMiacCodeCache(CDbEntityCache):
    u'По id огранизации получаем miacCode'
    mapIdToCode = {}

    def __init__(self):
        pass

    @classmethod
    def purge(cls):
        cls.mapIdToCode.clear()


    @classmethod
    def getCode(cls, _id):
        u'По id огранизации получаем miacCode'
        result = cls.mapIdToCode.get(_id, False)
        if result is False:
            cls.connect()
            result = forceString(QtGui.qApp.db.translate(
                'Organisation', 'id', _id, 'miacCode'))
            cls.mapIdToCode[_id] = result
        return result


class CTfomsNomenclatureCache(CDbEntityCache):
    u'По id номенклатуры получаем её код в tfoms08.N020'
    mapIdToCode = {}

    def __init__(self):
        pass


    @classmethod
    def purge(cls):
        cls.mapIdToCode.clear()


    @classmethod
    def getCode(cls, _id):
        u'По id номенклатуры получаем её код в tfoms08.N020'
        result = cls.mapIdToCode.get(_id, False)
        if result is False:
            cls.connect()
            _db = QtGui.qApp.db
            table = _db.table('rbNomenclature_Identification')
            record = QtGui.qApp.db.getRecordEx(table, 'value', [
                table['id'].eq(_id),
                table['system_id'].eqEx(
                    '(SELECT MAX(id) FROM rbAccountingSystem '
                    'WHERE rbAccountingSystem.code = "tfoms08.N020")')])
            result = forceString(record.value(0)) if record else None
            cls.mapIdToCode[_id] = result
        return result
