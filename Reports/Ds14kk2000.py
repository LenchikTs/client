# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2015 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import *
from Reports.Report import CReport
from Reports.ReportBase import *
from Ui_Ds14kkSetupDialog import Ui_ds14kkSetupDialog
from library.Utils import forceString, forceInt, forceDouble
from Reports.Ds14kk1000 import CDs14kkSetupDialog, CDs14kkHelpers


class CReportDs14kk2000(CReport):
    def __init__(self, parent=None):
        CReport.__init__(self, parent)
        self.setTitle(u'Использование коек дневного стационара медицинской организации по профилям')

    def getSetupDialog(self, parent):
        result = CDs14kkSetupDialog(parent, useCbPermanent=True)
        # self.stationaryF14DCSetupDialog = result
        return result

    def selectPatientData(self, params):
        stmt = u'''
select
    rbHospitalBedProfile.id as profile_id,
    rbHospitalBedProfile.name, rbHospitalBedProfile.regionalCode as code,
    OrgStructure.type as orgtype,
    count( distinct case when isClosed and age(Client.birthDate, Event.setDate) < 18 then Client.id else null end) childrens,
    count( distinct case when isClosed and age(Client.birthDate, Event.setDate) >= 18 then Client.id else null end) adults,
    count( distinct case when isClosed and ((Client.sex = 1 and age(Client.birthDate, Event.setDate) >= 60) or (Client.sex = 2 and age(Client.birthDate, Event.setDate) >= 55)) then Client.id else null end) elders,
    sum( IF(age(Client.birthDate, Event.setDate) < 18,
            WorkDays(Event.setDate, Event.execDate, EventType.weekProfileCode, mt.regionalCode),
            0)) as pdchildrens,
    sum( IF(age(Client.birthDate, Event.setDate) >= 18,
            WorkDays(Event.setDate, Event.execDate, EventType.weekProfileCode, mt.regionalCode),
            0)) as pdadults,
    sum( IF((Client.sex = 1 and age(Client.birthDate, Event.setDate) >= 60) or (Client.sex = 2 and age(Client.birthDate, Event.setDate) >= 55),
            WorkDays(Event.setDate, Event.execDate, EventType.weekProfileCode, mt.regionalCode),
            0)) as pdelders
from Event
left join Action on Action.id = (select max(a.id) from Action a where a.event_id = Event.id and a.deleted = 0 and a.actionType_id IN (
                SELECT AT.id FROM ActionType AT WHERE AT.flatCode ='moving' AND AT.deleted = 0))
left join ActionPropertyType on ActionPropertyType.name = 'койка' and ActionPropertyType.actionType_id = Action.actionType_id and ActionPropertyType.deleted = 0
left join ActionProperty on ActionProperty.type_id = ActionPropertyType.id and ActionProperty.action_id = Action.id and ActionProperty.deleted = 0
left join ActionProperty_HospitalBed on ActionProperty_HospitalBed.id = ActionProperty.id
left join OrgStructure_HospitalBed on OrgStructure_HospitalBed.id = ActionProperty_HospitalBed.value
left join OrgStructure on OrgStructure.id = OrgStructure_HospitalBed.master_id
inner join rbHospitalBedProfile on rbHospitalBedProfile.id = OrgStructure_HospitalBed.profile_id
left join rbHospitalBedShedule on rbHospitalBedShedule.id = OrgStructure_HospitalBed.schedule_id
left join Client on Client.id = Event.client_id
left join EventType ON EventType.id = Event.eventType_id
left join rbEventTypePurpose ON rbEventTypePurpose.id = EventType.purpose_id
left join rbMedicalAidType mt ON mt.id = EventType.medicalAidType_id
left join Contract on  Contract.id = Event.contract_id
where
    OrgStructure.type in (0,1) and rbHospitalBedShedule.code = 2 and Event.deleted = 0
    and %(cond)s

group by rbHospitalBedProfile.id, OrgStructure.type

        '''
        db = QtGui.qApp.db
        st = stmt % {'cond': CDs14kkHelpers.getCond(params, 2, permanentBeds=True)}
        return db.query(st)

    def selectBedsData(self, params):
        stmt = u'''
SELECT
    rbHospitalBedProfile.id as profile_id,
    rbHospitalBedProfile.name,
    rbHospitalBedProfile.regionalCode as code,
    sum((case when OrgStructure_HospitalBed.relief = 2 then 2 else 1 end) * isAdult) kAdult,
    sum((case when OrgStructure_HospitalBed.relief = 2 then 2 else 1 end) * isChild) kChild,

    CASE WHEN MAX(inconsistentdates * isAdult) <> 0 THEN "-"
         WHEN MAX(nulldates * isAdult) <> 0 THEN sum((case when OrgStructure_HospitalBed.relief = 2 then 2 else 1 END) * isAdult)
         ELSE sum(wd * isAdult) / (%(wd)d * SUM(1))
    END as sgAdult,
    CASE WHEN MAX(inconsistentdates * isChild) <> 0 THEN "-"
         WHEN MAX(nulldates * isChild) <> 0 THEN sum((case when OrgStructure_HospitalBed.relief = 2 then 2 else 1 END) * isChild)
         ELSE sum(wd * isChild) / (%(wd)d * SUM(1))
    END as sgChild,
    OrgStructure_HospitalBed.type as orgtype
FROM (
    select OrgStructure.type,
    OrgStructure_HospitalBed.*,
    isSexAndAgeSuitable(0, DATE_SUB(NOW(),INTERVAL 18 YEAR), 0, OrgStructure_HospitalBed.age, now()) isAdult,
    isSexAndAgeSuitable(0, DATE_SUB(NOW(),INTERVAL 17 YEAR), 0, OrgStructure_HospitalBed.age, now()) isChild,
    WorkDays(OrgStructure_HospitalBed.begDate, OrgStructure_HospitalBed.endDate, 0, '41') as wd,
    isnull(OrgStructure_HospitalBed.begDate) xor isnull(OrgStructure_HospitalBed.endDate) as inconsistentdates,
    isnull(OrgStructure_HospitalBed.begDate) and isnull(OrgStructure_HospitalBed.endDate) as nulldates
    from OrgStructure_HospitalBed
    left join OrgStructure on OrgStructure.id = OrgStructure_HospitalBed.master_id
    left join rbHospitalBedShedule ON rbHospitalBedShedule.id = OrgStructure_HospitalBed.schedule_id
    where OrgStructure.type in (0,1) and rbHospitalBedShedule.code = 2
    and %(cond)s
    group by OrgStructure_HospitalBed.code, OrgStructure_HospitalBed.name
   ) as OrgStructure_HospitalBed
inner join rbHospitalBedProfile on rbHospitalBedProfile.id = OrgStructure_HospitalBed.profile_id
group by rbHospitalBedProfile.id, OrgStructure_HospitalBed.type
        '''
        db = QtGui.qApp.db
        year = QDate.currentDate()
        if params.get("begDate", None):
            year = params["begDate"]
        elif params.get("endDate", None):
            year = params["endDate"]
        year = year.toString("yyyy")
        q = db.query('select WorkDays("%s-01-01", "%s-12-31", 0, "41")' % (year, year))
        wd = 365
        if q.first():
            wd = forceInt(q.record().value(0))

        st = stmt % {'wd':wd, 'cond': CDs14kkHelpers.getCond(params, permanentBeds=True)}
        return db.query(st)

    def selectDataTbl2500(self, params):
        stmt = u'''
SELECT
    count(distinct case when OrgStructure.type = 0 then Event.id else null end) as amb_deathAll,
    count(distinct case when OrgStructure.type = 0 and
                        isSexAndAgeSuitable(0, DATE_SUB(NOW(),INTERVAL 17 YEAR), 0, OrgStructure_HospitalBed.age, now())
                  then Event.id else null end) as amb_deathChild,
    count(distinct case when OrgStructure.type = 1 then Event.id else null end) as stac_deathAll,
    count(distinct case when OrgStructure.type = 1 and
                        isSexAndAgeSuitable(0, DATE_SUB(NOW(),INTERVAL 17 YEAR), 0, OrgStructure_HospitalBed.age, now())
                  then Event.id else null end) as stac_deathChild

FROM Event
left join rbResult on rbResult.id = Event.result_id
left join OrgStructure_HospitalBed on OrgStructure_HospitalBed.id = (
    select ActionProperty_HospitalBed.value
    from Action as HospitalAction
    left join ActionPropertyType on ActionPropertyType.name = 'койка'
    and ActionPropertyType.actionType_id = HospitalAction.actionType_id and ActionPropertyType.deleted = 0
    left join ActionProperty on ActionProperty.type_id = ActionPropertyType.id
        and ActionProperty.action_id = HospitalAction.id and ActionProperty.deleted = 0
    left join ActionProperty_HospitalBed on ActionProperty_HospitalBed.id = ActionProperty.id
    where HospitalAction.id = (SELECT MAX(A.id) FROM Action A
                WHERE A.event_id = Event.id AND A.deleted = 0 AND A.actionType_id IN (
                                SELECT AT.id
                                FROM ActionType AT
                                WHERE AT.flatCode ='moving'
                                    AND AT.deleted = 0)
                                )

    )
left join OrgStructure on OrgStructure_HospitalBed.master_id = OrgStructure.id
inner join rbHospitalBedProfile on rbHospitalBedProfile.id = OrgStructure_HospitalBed.profile_id
left join rbHospitalBedShedule ON rbHospitalBedShedule.id = OrgStructure_HospitalBed.schedule_id
left join Contract on  Contract.id = Event.contract_id

where
    Event.isClosed and Event.deleted = 0
    and (rbResult.name LIKE 'умер' or rbResult.name like 'умер в приемном покое')
    and rbHospitalBedShedule.code = 2
    and %(cond)s
        '''
        db = QtGui.qApp.db
        st = stmt % {'cond': CDs14kkHelpers.getCond(params, 2, permanentBeds=True)}
        return db.query(st)

    def selectDataTbl2600(self, params):
        stmt = u'''
SELECT
    count(distinct case when OrgStructure.type = 0 then Event.id else null end) as ambAll,
    count(distinct case when OrgStructure.type = 1 then Event.id else null end) as stacAll

FROM Event
left join OrgStructure_HospitalBed on OrgStructure_HospitalBed.id = (
    select ActionProperty_HospitalBed.value
    from Action as HospitalAction
    left join ActionPropertyType on ActionPropertyType.name = 'койка'
    and ActionPropertyType.actionType_id = HospitalAction.actionType_id and ActionPropertyType.deleted = 0
    left join ActionProperty on ActionProperty.type_id = ActionPropertyType.id
        and ActionProperty.action_id = HospitalAction.id and ActionProperty.deleted = 0
    left join ActionProperty_HospitalBed on ActionProperty_HospitalBed.id = ActionProperty.id
    where HospitalAction.id = (SELECT MAX(A.id) FROM Action A
                WHERE A.event_id = Event.id AND A.deleted = 0 AND A.actionType_id IN (
                                SELECT AT.id
                                FROM ActionType AT
                                WHERE AT.flatCode ='moving'
                                    AND AT.deleted = 0)
                                )

)
left join OrgStructure on OrgStructure_HospitalBed.master_id = OrgStructure.id
left join rbHospitalBedShedule ON rbHospitalBedShedule.id = OrgStructure_HospitalBed.schedule_id
left join ClientAddress on ClientAddress.id = getClientLocAddressId(Event.client_id)
left join Address on Address.id = ClientAddress.address_id
left join AddressHouse on AddressHouse.id = Address.house_id
left join Contract on  Contract.id = Event.contract_id
where
    Event.isClosed and Event.deleted = 0
    and rbHospitalBedShedule.code = 2
    and Event.deleted =0
    and SUBSTRING(AddressHouse.KLADRCode,9,3) <> '000'
    and %(cond)s
    '''
        db = QtGui.qApp.db
        st = stmt % {'cond': CDs14kkHelpers.getCond(params, 2, permanentBeds=True)}
        return db.query(st)

    def tbl_2500(self, cursor, params):
        data = {'amb_deathAll': 0, 'amb_deathChild': 0, 'stac_deathAll': 0, 'stac_deathChild': 0}

        def processQuery(query):
            while query.next():
                record = query.record()
                for key in data.keys():
                    data[key] += forceInt(record.value(key))
        processQuery(self.selectDataTbl2500(params))
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertText(u'Умерло в дневном стационаре при подразделениях медицинских организаций, оказывающих медицинскую помощь:')
        cursor.insertText(u'\r\nв стационарных условиях: %d' % data.get('stac_deathAll', 0))
        cursor.insertText(u'\r\nиз них детей: %d' % data.get('stac_deathChild', 0))
        cursor.insertText(u'\r\nв амбулаторных условиях: %d' % data.get('amb_deathAll', 0))
        cursor.insertText(u'\r\nиз них детей: %d' % data.get('amb_deathChild', 0))
        cursor.insertText(u'\r\nна дому: -')
        cursor.insertText(u'\r\nиз них детей: -')

    def tbl_2600(self, cursor, params):
        data = {'ambAll': 0, 'stacAll': 0}
        def processQuery(query):
            while query.next():
                record = query.record()
                for key in data.keys():
                    data[key] += forceInt(record.value(key))
        processQuery(self.selectDataTbl2600(params))
        cursor.setCharFormat(CReportBase.ReportBody)
        cursor.insertText(u'Число выписанных сельских жителей из дневных стационаров медицинских организаций, оказывающий медицинскую помощь:')
        cursor.insertText(u'\r\nв стационарных условиях: %d' % data.get('stacAll', 0))
        cursor.insertText(u'\r\nв амбулаторных условиях: %d' % data.get('ambAll', 0))
        cursor.insertText(u'\r\nна дому: -')

    def build(self, params):

        # nomer, name, regionalCode
        lines = [
            ('1', u'Всего', ['-']),
            ('2', u'аллергологические для взрослых', ['07']),
            ('3', u'аллергологические для детей', ['08']),
            ('4', u'для беременных и рожениц', ['38', '98']),
            ('5', u'для патологии беременности', ['39', '1A']),
            ('6', u'гинекологические для взрослых', ['40']),
            ('6.1', u'гинекологические для вспомогательных репродуктивных технологий', ['1B']),
            ('7', u'гинекологические для детей', ['96']),
            ('8', u'гастроэнтерологические для взрослых', ['05']),
            ('9', u'гастроэнтерологические для детей', ['06']),
            ('10', u'гематологические для взрослых', ['15']),
            ('11', u'гематологические для детей', ['16']),
            ('12', u'геронтологические', ['70']),
            ('13', u'дерматологические для взрослых', ['1C']),
            ('14', u'дерматологические для детей', ['1D']),
            ('15', u'венерологические для взрослых', ['57']),
            ('16', u'венерологические для детей', ['58']),
            ('17', u'инфекционные для взрослых', ['13']),
            ('18', u'инфекционные для детей', ['14']),
            ('19', u'кардиологические для взрослых', ['03']),
            ('20', u'кардиологические для детей', ['77']),
            ('21', u'наркологические', ['52']),
            ('22', u'неврологические для взрослых', ['47']),
            ('23', u'неврологические для детей', ['48']),
            ('23.1', u'психоневрологические для детей', ['50']),
            ('24', u'нефрологические для взрослых', ['17']),
            ('25', u'нефрологические для детей', ['18']),
            ('26', u'онкологические для взрослых', ['36']),
            ('26.1', u'онкологические торакальные', ['2D']),
            ('26.2 7', u'онкологические абдоминальные', ['2E']),
            ('26.3', u'онкоурологические', ['2F']),
            ('26.4', u'онкогинекологические', ['2G']),
            ('26.5', u'онкологические опухолей головы и шеи', ['2H']),
            ('26.6', u'онкологические опухолей костей, кожи и мягких тканей', ['2I']),
            ('26.7', u'онкологические паллиативные', ['2J']),
            ('27', u'онкологические для детей', ['37']),
            ('28', u'оториноларингологические для взрослых', ['55']),
            ('29', u'оториноларингологические для детей', ['56']),
            ('30', u'офтальмологические для взрослых', ['53']),
            ('31', u'офтальмологические для детей', ['54']),
            ('32', u'ожоговые', ['29', '99']),
            ('33', u'паллиативные для взрослых', ['74']),
            ('34', u'паллиативные для детей', ['74']),
            ('35', u'педиатрические соматические', ['60']),
            ('36', u'проктологические', ['63']),
            ('37', u'психиатрические для взрослых', ['49']),
            ('37.1', u'психосоматические', ['51']),
            ('37.2', u'соматопсихиатрические', ['1P']),
            ('38', u'психиатрические для детей', ['50']),
            ('39', u'профпатологические', ['71']),
            ('40', u'пульмонологические для взрослых', ['68']),
            ('41', u'пульмонологические для детей', ['69']),
            ('42', u'радиологические', ['59']),
            ('43', u'реабилитационные соматические для взрослых', ['1X']),
            ('43.1', u'реабилитационные для больных с заболеваниями центральной нервной системы и органов чувств',
             ['1Z', '2A']),
            ('43.2',
             u'реабилитационные для больных с заболеваниями опорно-двигательного аппарата и периферической нервной системы',
             ['2B', '2C']),
            ('43.3', u'реабилитационные для наркологических больных', ['2K']),
            ('44', u'реабилитационные соматические для детей', ['1Y']),
            ('46', u'ревматологические для взрослых', ['64']),
            ('47', u'ревматологические для детей', ['65']),
            ('48', u'сестринского ухода', ['73']),
            ('49', u'скорой медицинской помощи краткосрочного пребывания', ['1K', '1L']),
            ('51', u'терапевтические', ['02']),
            ('52', u'токсикологические', ['72']),
            ('53', u'травматологические для взрослых', ['27']),
            ('54', u'травматологические для детей', ['28']),
            ('55', u'ортопедические для взрослых', ['30']),
            ('56', u'ортопедические для детей', ['31']),
            ('57', u'туберкулезные для взрослых', ['42']),
            ('58', u'туберкулезные для детей', ['45']),
            ('59', u'урологические для взрослых', ['32']),
            ('60', u'урологические для детей', ['33']),
            ('60.1', u'уроандрологические для детей', ['1F']),
            ('61', u'хирургические для взрослых', ['19']),
            ('62', u'абдоминальной хирургии', ['87', '88']),
            ('63', u'хирургические для детей', ['20']),
            ('64', u'нейрохирургические для взрослых', ['21']),
            ('65', u'нейрохирургические для детей', ['22']),
            ('66', u'торакальной хирургии для взрослых', ['23']),
            ('67', u'торакальной хирургии для детей', ['24']),
            ('68', u'кардиохирургические', ['25', '78']),
            ('69', u'сосудистой хирургии', ['26']),
            ('70', u'хирургические гнойные для взрослых', ['66']),
            ('71', u'хирургические гнойные для детей', ['67']),
            ('72', u'челюстно-лицевой хирургии', ['84', '85']),
            ('73', u'стоматологические для детей', ['35']),
            ('74', u'эндокринологические для взрослых', ['11']),
            ('75', u'эндокринологические для детей', ['12'])
        ]
        stacReport = []
        ambReport = []

        def getLineIndex(title, regionalCode):
            for i, line in enumerate(lines):
                if line[1] == title:
                    return i
            for i, line in enumerate(lines):
                for regCode in line[2]:
                    if regCode == regionalCode:
                        return i
            return None

        for line in lines:
            for report in [stacReport, ambReport]:
                row = [0] * 12
                row[0], row[1] = line[1], line[0]
                report.append(row)

        def processQuery(querybeds, querypatient):
            while querybeds.next():
                record = querybeds.record()
                _type = forceInt(record.value('orgtype'))
                if _type == 0:
                    report = ambReport
                elif _type == 1:
                    report = stacReport
                lineIndex = getLineIndex(forceString(record.value('name')), forceString(record.value('code')))
                for li in filter(lambda a: a != None, [0, lineIndex]):
                    nulldates = forceInt(record.value('nulldates'))
                    notnulldates = forceInt(record.value('notnulldates'))

                    report[li][2] += forceInt(record.value('kAdult'))
                    report[li][4] += forceInt(record.value('kChild'))
                    # 1. среднегодовые = кол-во коек-дней(по датам начала и окончания лечения) /на количечтво коек
                    #  (объеденить по коду и наименованию)
                    #  за год (12 месяцев), если заполнены все даты начала (дата окончания не обязательна!
                    #  – считать койку действующей)
                    # 2. среднегодовые = кол-во коек, если не заполнены все даты начала и окончания
                    # 3. среднегодовые = "-" если часть дат начала\окончания заполнены а часть нет
                    if li > 0:
                        report[li][3] = forceString(record.value('sgAdult'))
                        report[li][5] = forceString(record.value('sgChild'))

                        #report[li][3] = float(kd) / sgAdult * 365
                        #report[li][5] = float(kd) / sgChild * 365
            while querypatient.next():
                record = querypatient.record()
                _type = forceInt(record.value('orgtype'))
                if _type == 0:
                    report = ambReport
                elif _type == 1:
                    report = stacReport

                lineIndex = getLineIndex(forceString(record.value('name')), forceString(record.value('code')))
                for li in filter(lambda a: a != None, [0, lineIndex]):
                    report[li][6] += forceInt(record.value('adults')) + forceInt(record.value('elders'))
                    report[li][7] = forceInt(record.value('elders'))
                    report[li][8] += forceInt(record.value('childrens'))
                    report[li][9] += forceInt(record.value('pdadults')) + forceInt(record.value('pdelders'))
                    report[li][10] = forceInt(record.value('pdelders'))
                    report[li][11] += forceInt(record.value('pdchildrens'))

        processQuery(self.selectBedsData(params), self.selectPatientData(params))
        for report in [ambReport, stacReport]:
            report[0][3] = sum([float(i[3]) if i[3] != u'-' else 0 for i in report[1:]])
            report[0][5] = sum([float(i[5]) if i[5] != u'-' else 0 for i in report[1:]])
            if report[0][3] == int(report[0][3]):
                report[0][3] = int(report[0][3])
            if report[0][5] == int(report[0][5]):
                report[0][5] = int(report[0][5])

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.setBlockFormat(CReportBase.AlignCenter)
        cursor.insertText(u'2. Использование коек дневного стационара медицинской организации по профилям')
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        CDs14kkHelpers.splitTitle(cursor, u'(2000)', u'')
        cursor.insertBlock()
        tableColumns = [
            ('20%', [u'Профиль коек'], CReportBase.AlignCenter),
            ('8%', [u'№ строки'], CReportBase.AlignRight),
            ('8%',
             [u'Дневные стационары медицинских организаций, оказывающих медицинскую помощь в стационарных условиях',
              u'число коек', u'для взрослых', u'на конец года'], CReportBase.AlignRight),
            ('8%', [u'', u'', u'', u'среднегодовых'], CReportBase.AlignRight),
            ('8%', [u'', u'', u'для детей', u'на конец года'], CReportBase.AlignRight),
            ('8%', [u'', u'', u'', u'среднегодовых'], CReportBase.AlignRight),
            ('8%', [u'', u'выписано пациентов', u'взрослых'], CReportBase.AlignRight),
            ('8%', [u'', u'', u'из них:', u'лиц старше трудосп. возраста'], CReportBase.AlignRight),
            ('8%', [u'', u'', u'детей 0-17 лет включительно'], CReportBase.AlignRight),
            ('8%', [u'', u'Проведено пациенто-дней', u'взрослыми'], CReportBase.AlignRight),
            ('8%', [u'', u'', u'из них:', u'лицами старше трудосп. возраста'], CReportBase.AlignRight),
            ('8%', [u'', u'', u'детьми 0-17 лет включительно'], CReportBase.AlignRight),
        ]

        table = createTable(cursor, tableColumns)

        autoMergeHeader(table, tableColumns)
        def beatifyfloat(f):
            if f == u'-':
                return f
            f = float(f)
            if f == int(f):
                return int(f)
            return "%.2f" % f


        row = table.addRow()
        for i in range(12):
            table.setText(row, i, i + 1, blockFormat=CReportBase.AlignCenter)
        for line in stacReport:
            row = table.addRow()
            for i in range(12):
                text = line[i]
                if i in [3, 5]:
                    text = beatifyfloat(text)
                table.setText(row, i, text, blockFormat=CReportBase.AlignRight if i != 0 else CReportBase.AlignLeft)

        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        CDs14kkHelpers.splitTitle(cursor, u'(2000)', u'Коды по ОКЕИ: человек - 792, еденица - 642')

        tableColumns[2] = ('8%', [
            u'Дневные стационары медицинских организаций, оказывающих медицинскую помощь в амбулаторных условиях',
            u'число коек', u'для взрослых', u'на конец года'], CReportBase.AlignRight)
        table = createTable(cursor, tableColumns)
        autoMergeHeader(table, tableColumns)
        row = table.addRow()
        thisNumeration = [1, 2] + range(13, 23)
        for i in range(12):
            table.setText(row, i, thisNumeration[i], blockFormat=CReportBase.AlignCenter)
        for line in ambReport:
            row = table.addRow()
            for i in range(12):
                text = line[i]
                if i in [3, 5]:
                    text = beatifyfloat(text)
                table.setText(row, i, text, blockFormat=CReportBase.AlignRight if i != 0 else CReportBase.AlignLeft)

        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        CDs14kkHelpers.splitTitle(cursor, u'(2100)', u'')
        tableColumns[2] = ('8%', [
            u'Дневные стационары медицинских организаций, оказывающих медицинскую помощь на дому',
            u'число коек', u'для взрослых', u'на конец года'], CReportBase.AlignRight)
        table = createTable(cursor, tableColumns)

        autoMergeHeader(table, tableColumns)
        row = table.addRow()
        for i in range(12):
            table.setText(row, i, i + 1, blockFormat=CReportBase.AlignCenter)
        row = table.addRow()
        table.setText(row, 0, u'Всего', blockFormat=CReportBase.AlignLeft)

        for i in range(1, 12):
            table.setText(row, i, u'-')
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        CDs14kkHelpers.splitTitle(cursor, u'(2500)', u'')
        self.tbl_2500(cursor, params)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        CDs14kkHelpers.splitTitle(cursor, u'(2600)', u'')
        self.tbl_2600(cursor, params)

        CDs14kkHelpers.writeFooter(cursor)
        return doc
