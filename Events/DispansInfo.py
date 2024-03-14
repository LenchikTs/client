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

# WTF?

from PyQt4 import QtGui
from PyQt4.QtCore import QDate

from library.PrintInfo        import CInfoList
from library.Utils            import forceInt, forceRef, forceString, trim

from Events.EventInfo         import CDiagnosticInfo
from Reports.Report           import normalizeMKB


class CLocDiseasesInfoList(CInfoList):
    def __init__(self, context, MainRows, **reportMainData):
        CInfoList.__init__(self, context)
        self.MainRows = MainRows
        self.reportMainData = reportMainData.get('dictOutData', [])


    def _load(self):
        self._items = []
        if self.reportMainData:
            rowSize = 4
            for row, rowDescr in enumerate(self.MainRows):
                reportLine = self.reportMainData[row]
                item = [rowDescr[0],
                        rowDescr[1],
                        rowDescr[2]
                        ]
                for col in xrange(rowSize):
                    item.append(reportLine[col])
                self._items.append(item)
            return True
        else:
            return False


    def _initByRecord(self, record=None):
        pass


    def _initByNull(self):
        pass


    diseasesItems = property(lambda self: self.load()._items)


class CLocDiagnosticInfoList(CInfoList):
    def __init__(self, context, eventId):
        CInfoList.__init__(self, context)
        self.eventId = eventId


    def _load(self):
        db = QtGui.qApp.db
        table = db.table('Diagnostic')
        idList = db.getIdList(table, 'id', [table['event_id'].eq(self.eventId), table['deleted'].eq(0)], 'id')
        self._items = [ self.getInstance(CDiagnosticInfo, id) for id in idList ]
        return True

    diagnosticItems = property(lambda self: self.load()._items)


class CLocActionDispansPhaseInfo(CInfoList):
    def __init__(self, context, id, phase,  **params):
        CInfoList.__init__(self, context)
        self.params = params
        self.phase = phase
        self.row2Name = {}
        self.mapNumMesVisitCode2Row = {}


    def getCodeRowToPhase(self):
        if self.phase == 1:
            self.mapNumMesVisitCode2Row = {
                        u'1': 1,
                        u'3': 2,
                        u'2': 3,
                        u'4': 4,
                        u'5': 5,
                        u'6': 6,
                        u'86':7,
                        u'15':8,
                        u'18':9,
                        u'14':10,
                        u'19':11,
                        u'8': 12,
                        u'9': 13,
                        u'11':14,
                        u'10':15,
                        u'12':16,
                        u'87':17,
                        u'13':18,
                        u'7': 19,
                        u'17':20
                        }
            self.row2Name = {
                        1: u'Опрос(анкетирование), направленный на выявление хронических неинфекционных заболеваний, факторов риска их развития, потребления наркотических средств и психотропных веществ без назначения врача',
                        2: u'Антропометрия (измерение роста стоя, массы тела, окружности талии), расчет индекса массы тела',
                        3: u'Измерение артериального давления',
                        4: u'Определение уровня общего холестерина в крови',
                        5: u'Определение уровня глюкозы в крови экспресс-методом',
                        6: u'Определение относительного суммарного сердечно-сосудистого риска',
                        7: u'Определение абсолютного суммарного сердечно-сосудистого риска',
                        8: u'Электрокардиография (в покое)',
                        9: u'Осмотр фельдшером (акушеркой), включая взятие мазка (соскоба) с поверхности шейки матки (наружного маточного зева) и цервикального канала на цитологическое исследование',
                        10: u'Флюорография легких',
                        11: u'Маммография обеих молочных желез',
                        12: u'Клинический анализ крови',
                        13: u'Клинический анализ крови развернутый',
                        14: u'Анализ крови биохимический общетерапевтический',
                        15: u'Общий анализ мочи',
                        16: u'Исследование кала на скрытую кровь иммунохимическим методом',
                        17: u'Ультразвуковое исследование (УЗИ) на предмет исключения новообразований органов брюшной полости, малого таза и аневризмы брюшной аорты',
                        18: u'Ультразвуковое исследование (УЗИ) в целях исключения аневризмы брюшной аорты',
                        19: u'Измерение внутриглазного давления',
                        20: u'Прием (осмотр) врача-терапевта'
                        }
        elif self.phase == 2:
            self.mapNumMesVisitCode2Row = {u'55' : 1,
                                           u'44' : 2,
                                           u'56' : 3,
                                           u'50' : 4,
                                           u'45' : 5,
                                           u'46' : 5,
                                           u'58' : 6,
                                           u'53' : 7,
                                           u'90' : 8,
                                           u'48' : 9,
                                           u'54' : 10,
                                           u'91' : 11,
                                           u'92' : 12,
                                           u'47' : 13,
                                           u'52' : 14,
                                           u'59' : 15,
                                           u'17' : 16
                                          }
            self.row2Name = {
                             1 : u'Дуплексное сканирование брахицефальных артерий',
                             2 : u'Осмотр (консультация) врачом-неврологом',
                             3 : u'Эзофагогастродуоденоскопия ',
                             4 : u'Осмотр (консультация) врачом-хирургом или врачом-урологом',
                             5 : u'Осмотр (консультация) врачом-хирургом или врачом-колопроктологом',
                             6 : u'Колоноскопия или ректороманоскопия',
                             7 : u'Определение липидного спектра крови',
                             8 : u'Спирометрия',
                             9 : u'Осмотр (консультация) врачом-акушером-гинекологом',
                             10: u'Определение концентрации гликированного гемоглобина в крови или тест на толерантность к глюкозе',
                             11: u'Осмотр (консультация) врачом-оториноларингологом',
                             12: u'Анализ крови на уровень содержания простатспецифического антигена',
                             13: u'Осмотр (консультация) врачом-офтальмологом',
                             14: u'Индивидуальное углубленное профилактическое консультирование',
                             15: u'Групповое профилактическое консультирование (школа пациента)',
                             16: u'Прием (осмотр) врача-терапевта'
                            }


    def _load(self):
#        db = QtGui.qApp.db
        reportData = self.getReportData()
        self._items = []
        if reportData:
            for numMesVisitCode, reportLine in reportData.items():
                name = self.getName(numMesVisitCode)
                item = [name[0], name[1]]
                for row, val in enumerate(reportLine):
                    item.append(val)
                self._items.append(item)
            return True
        else:
            self._items = []
            return False


    def getLocActionDispansPhase(self, param):
        actionTypeId = param.get('actionTypeId', None)
        mesId = param.get('mesId', None)
        if not actionTypeId and mesId:
            return None
#        MKB = param.get('MKB', '')
        personId = param.get('personId', None)
        db = QtGui.qApp.db
        tableMESVisit = db.table('mes.MES_visit')
        tableMES = db.table('mes.MES')
        tableMESGroup = db.table('mes.mrbMESGroup')
#        tableEvent = db.table('Event')
#        tableAction = db.table('Action')
        tableActionType = db.table('ActionType')
        tableService = db.table('rbService')
        tablePerson = db.table('Person')
        tableMESSpeciality = db.table('mes.mrbSpeciality')
        tableSpeciality = db.table('rbSpeciality')
        queryTable = tableMES.leftJoin(tableMESVisit, tableMESVisit['master_id'].eq(tableMES['id']))
        queryTable = queryTable.leftJoin(tableMESGroup, tableMESGroup['id'].eq(tableMES['group_id']))
        queryTable = queryTable.leftJoin(tableActionType, tableActionType['id'].eq(actionTypeId))
        queryTable = queryTable.leftJoin(tableService, tableService['id'].eq(tableActionType['nomenclativeService_id']))
        if personId:
            queryTable = queryTable.leftJoin(tablePerson, tablePerson['id'].eq(personId))
            queryTable = queryTable.leftJoin(tableSpeciality, tableSpeciality['id'].eq(tablePerson['speciality_id']))
        queryTable = queryTable.leftJoin(tableMESSpeciality, tableMESSpeciality['id'].eq(tableMESVisit['speciality_id']))
        cond = [tableMESGroup['code'].eq(u'ДиспанС'),
                tableMES['id'].eq(mesId),
                '(mes.MES_visit.`serviceCode` = SUBSTR(rbService.`code`,1, CHAR_LENGTH(mes.MES_visit.`serviceCode`))AND SUBSTR(rbService.`code`, CHAR_LENGTH(mes.MES_visit.`serviceCode`)+1) REGEXP \'^([*.]|$)\')',
                ]
        fields = ['CONCAT_WS(" | ", ActionType.`code`, ActionType.`name`) AS actionTypeName',
                  tableService['name'].alias('serviceName'),
                  tableMESVisit['additionalServiceCode'].alias('numMesVisitCode')
                  ]
        stmt = db.selectDistinctStmt(queryTable, fields, cond)
        return db.query(stmt)


    def getReportData(self):
        self.getCodeRowToPhase()
        reportData = self.getDefault()
        uniqueSet = set()
        params = self.params.get('dictOut', None)
        db = QtGui.qApp.db
        for param in params.values():
            query = self.getLocActionDispansPhase(param)
            while query.next():
                record = query.record()
                numMesVisitCode = forceString(record.value('numMesVisitCode'))
                if numMesVisitCode not in self.mapNumMesVisitCode2Row:
                    continue
                serviceName = forceString(record.value('serviceName'))
                key = (numMesVisitCode, serviceName)
                if key in uniqueSet:
                    continue
                actionMkb = param.get('MKB', '')
                directionDate = param.get('directionDate', None)
#                begDate = param.get('begDate', None)
                endDate = param.get('endDate', None)
                status = param.get('status', 0)
                setDate = param.get('setDate', None)
                execDate = param.get('execDate', None)
                actionExecNow = (endDate >= setDate and endDate <= execDate) if execDate and setDate else False
                actionExecPrev = (endDate >= setDate.addYears(-1) and endDate < setDate) if setDate else False
                actionExecRefusal = (status == 6 and not endDate)
                propertyEvaluation = param.get('evaluation', 0)
                uniqueSet.add(key)
                numCode = self.mapNumMesVisitCode2Row.get(numMesVisitCode, None)
                if numCode not in self.row2Name.keys():
                    continue
                data = reportData.get(numCode, [u'-', u'-', u'-', u'-'])
                if not actionExecRefusal:
                    if actionExecNow:
                        data[0] = u'%s' % db.formatDate(endDate)
                        data[3] = u'%s' % db.formatDate(directionDate)
                    elif actionExecPrev:
                        data[2] = u'проведено ранее(%s)' % db.formatDate(endDate)
                elif actionExecRefusal:
                    data[2] = u'отказ(%s)' % db.formatDate(directionDate)
                if actionMkb and actionMkb[0].isalpha() and actionMkb[0].upper() != 'Z':
                    data[1] = u'+'
                elif propertyEvaluation:
                    data[1] = u'+'
                else:
                    data[1] = u'-'
        return reportData


    def getDefault(self):
        result = {}
        for key in self.row2Name.keys():
            result[key] = [u'-', u'-', u'-', u'-']
        return result


    def getName(self, num):
        return [self.row2Name.get(num, ''), num]


    def _initByRecord(self, record=None):
        pass


    def _initByNull(self):
        pass


    dispansItems = property(lambda self: self.load()._items)


class CLocHazardInfoList(CInfoList):
    def __init__(self, context, id, **params):
        CInfoList.__init__(self, context)
        self.params = params


    def getInterviewActionTypeIdList(self):
        db = QtGui.qApp.db
        table = db.table('rbService')
        cond = [db.joinOr([table['code'].like(u'А01.31.024*'),
                           table['code'].like(u'А02.12.002'),
                           table['code'].like(u'A09.05.026'),
                           table['code'].like(u'В03.016.04'),
                           table['code'].like(u'А09.05.023'),
                           table['code'].like(u'А02.07.004')])
                ]
        fields = table['id'].name()
        return [forceRef(record.value('id')) for record in db.getRecordList(table, fields, cond)]


    def getLocActionHazardDispans(self, param):
        actionTypeId = param.get('actionTypeId', None)
        mesId = param.get('mesId', None)
        clientId = param.get('clientId', None)
        endDate = param.get('execDate', None)
        if not actionTypeId and mesId and clientId:
            return None
        db = QtGui.qApp.db
        tableActionType = db.table('ActionType')
        tableClient = db.table('Client')
#        tableActionProperty = db.table('ActionProperty')
#        tableActionPropertyType = db.table('ActionPropertyType')
#        tableActionPropertyString = db.table('ActionProperty_String')
        tableMES = db.table('mes.MES')
        tableMESGroup = db.table('mes.mrbMESGroup')
        tableRBService = db.table('rbService')
        queryTable = tableMES.leftJoin(tableMESGroup, tableMESGroup['id'].eq(tableMES['group_id']))
        queryTable = queryTable.leftJoin(tableClient, tableClient['id'].eq(clientId))
        queryTable = queryTable.innerJoin(tableActionType, tableActionType['id'].eq(actionTypeId))
        queryTable = queryTable.innerJoin(tableRBService, tableRBService['id'].eq(tableActionType['nomenclativeService_id']))
        cond = [tableMESGroup['code'].eq(u'ДиспанС'),
                tableMES['id'].eq(mesId),
                tableActionType['nomenclativeService_id'].inlist(self.getInterviewActionTypeIdList())
                ]
        fields = [tableRBService['code'].alias('codeService'),
                  'age(Client.`birthDate`, \'%s\') AS clientAge' % unicode(QDate(endDate.year(), 12, 31).toString('yyyy-MM-dd')),
                  tableClient['sex'].alias('clientSex'),
                  tableClient['id'].alias('clientId')
                  ]
        stmt = db.selectStmt(queryTable, fields, cond)
        return db.query(stmt)


    def _getRowsDefaults(self):
        rowsService = {u'А02.12.002':[1],
                       u'А09.05.023':[2],
                       u'В03.016.04':[2],
                       u'А02.07.004':[3],
                       u'А01.31.024*':[4, 5, 6, 7, 8, 9]}
        rowsProperty = {1:[],
                        2:[],
                        3:[],
                        4:[u'26'],
                        5:[u'27', u'28', u'29', u'30'],
                        6:[u'39'],
                        7:[u'31'],
                        8:[u'32', u'33', u'34', u'35'],
                        9:[u'12', u'11', u'10', u'11.1', u'11.2']
                       }
        rows = {1: [u'R03.0'],
                2: [u'R73.9'],
                3: [u'R63.5'],
                4: [u'Z72.0'],
                5: [u'Z72.1'],
                6: [u'Z72.2'],
                7: [u'Z72.3'],
                8: [u'Z72.4'],
                9: [u'Z80, Z82.3, Z82.4, Z82.5, Z83.3']
                }
        for rowValueList in rows.values():
            rowValueList.append(u'-')
        return rowsService, rows, rowsProperty


    def getReportData(self):
        def _checkValue(rowRep, row, value):
            if rowRep == 4:
                if row == u'26':
                    return value.lower() == u'да'
            elif rowRep == 5:
                if row in [u'27', u'28', u'29', u'30']:
                    return value.lower() == u'да'
            elif rowRep == 6:
                if row == u'39':
                    return value.lower() == u'да'
            elif rowRep == 7:
                if row == u'31':
                    return value.lower() == u'до 30 мин'
            elif rowRep == 8:
                if row in [u'32', u'33']:
                    return value.lower() == u'нет'
                if row in [u'34', u'35']:
                    return value.lower() == u'да'
            elif rowRep in [9]:
                if row in [u'10', u'11', u'12', u'11.1', u'11.1', u'11.2', u'11.2']:
                    return value.lower() == u'да'
            else:
                return value.lower() == u'да'
        rowsService, reportData, rowsProperty = self._getRowsDefaults()
#        commonColumn = 9
        clientIdAndRowList = []
        clientIdActionRowList = []
        db = QtGui.qApp.db
        params = self.params.get('dictOut', None)
        for param in params.values():
            query = self.getLocActionHazardDispans(param)
            while query.next():
                record = query.record()
                clientId = forceRef(record.value('clientId'))
                codeService = forceString(record.value('codeService'))
                reportService = rowsService.get(codeService, [])
                if not reportService:
                    continue
                actionMkb = param.get('MKB', '')
#                directionDate = param.get('directionDate', None)
#                begDate = param.get('begDate', None)
                endDate = param.get('endDate', None)
#                status = param.get('status', 0)
#                setDate = param.get('setDate', None)
#                execDate = param.get('execDate', None)
#                actionExecNow = (endDate >= setDate and endDate <= execDate) if execDate and setDate else False
#                actionExecPrev = (endDate >= setDate.addYears(-1) and endDate < setDate) if setDate else False
#                actionExecRefusal = (status == 3 and not endDate)
                propertyEvaluation = param.get('evaluation', 0)
                propertyName = param.get('namePropertyType', '')
                descrProperty = param.get('descrPropertyType', '')
                propertyValue = param.get('valueProperty', None)
                clientAge = forceInt(record.value('clientAge'))
#                clientSex = forceInt(record.value('clientSex'))
#                column = 3 if clientSex == 1 else 7
                if codeService == u'А01.31.024*':
                    for rowRep in reportService:
                        reportLine = reportData.get(rowRep, [])
                        if reportLine:
                            propertyLine = rowsProperty.get(rowRep, [])
                            row = trim(forceString(descrProperty))
                            if not row:
                                propertyNameList = forceString(propertyName).split('.')
                                if not(len(propertyNameList) > 0 and trim(propertyNameList[0]).isdigit()):
                                    continue
                                row = trim(propertyNameList[0])
                                if row == u'11' and len(propertyNameList) > 1 and trim(propertyNameList[1]).isdigit():
                                    row = row + u'.' + trim(propertyNameList[1])
                            if row in propertyLine and (clientId, row) not in clientIdAndRowList:
                                clientIdAndRowList.append((clientId, row))
                                if _checkValue(rowRep, row, propertyValue):
                                    reportLine[1] = db.formatDate(endDate)
                else:
                    MKBRec = normalizeMKB(actionMkb)
                    if (MKBRec[:3] >= u'A00' and MKBRec[:3] <= u'T99') or propertyEvaluation:
                        for rowRep in reportService:
                            reportLine = reportData.get(rowRep, None)
                            if reportLine:
                                if codeService == u'А25.12.004*':
                                    if clientAge < 40 or clientAge > 65:
                                        continue
                                    row = trim(forceString(descrProperty))
                                    if not row:
                                        continue
                                    propertyLine = rowsProperty.get(rowRep, [])
                                    if row in propertyLine and (clientId, row) not in clientIdAndRowList:
                                        clientIdAndRowList.append((clientId, row))
                                        if not _checkValue(rowRep, row, propertyValue):
                                            continue
                                else:
                                    if (clientId, rowRep) in clientIdActionRowList:
                                        continue
                                    clientIdActionRowList.append((clientId, rowRep))
                                reportLine[1] = db.formatDate(endDate)
        return reportData


    def _load(self):
#        db = QtGui.qApp.db
        reportData = self.getReportData()
        self._items = []
        if reportData:
            keysRep = reportData.keys()
            keysRep.sort()
            for key in keysRep:
                reportLine = reportData.get(key, [])
                if reportLine:
                    self._items.append(reportLine[1])
            return True
        else:
            self._items = []
            return False


    def _initByRecord(self, record=None):
        pass


    def _initByNull(self):
        pass


    hazardItems = property(lambda self: self.load()._items)


class CLocAdditionInfoList(CInfoList):
    def __init__(self, context, id, **params):
        CInfoList.__init__(self, context)
        self.params = params


    def _load(self):
        params = self.params.get('dictOut', None)
        if params:
            self._relativeSumHazard         = params.get('relativeSumHazard', 0)
            self._absoluteSumHazard         = params.get('absoluteSumHazard', 0)
            self._actionTypeClass           = params.get('actionTypeClass', 0)
            self._followUpSurvey            = params.get('followUpSurvey', 0)
            self._directionHeartDoctor      = params.get('directionHeartDoctor', 0)
            self._directionPsychiaterDoctor = params.get('directionPsychiaterDoctor', 0)
            self._directionWTMP             = params.get('directionWTMP', 0)
            self._directionSanatorium       = params.get('directionSanatorium', 0)
            self._healthGroup               = params.get('healthGroup', u'')
            return True
        else:
            self._relativeSumHazard         = 0
            self._absoluteSumHazard         = 0
            self._actionTypeClass           = 0
            self._followUpSurvey            = 0
            self._directionHeartDoctor      = 0
            self._directionPsychiaterDoctor = 0
            self._directionWTMP             = 0
            self._directionSanatorium       = 0
            self._healthGroup               = u''
            return False


    def _initByRecord(self, record=None):
        pass


    def _initByNull(self):
        pass


    relativeSumHazard         = property(lambda self: self.load()._relativeSumHazard)
    absoluteSumHazard         = property(lambda self: self.load()._absoluteSumHazard)
    actionTypeClass           = property(lambda self: self.load()._actionTypeClass)
    followUpSurvey            = property(lambda self: self.load()._followUpSurvey)
    directionHeartDoctor      = property(lambda self: self.load()._directionHeartDoctor)
    directionPsychiaterDoctor = property(lambda self: self.load()._directionPsychiaterDoctor)
    directionWTMP             = property(lambda self: self.load()._directionWTMP)
    directionSanatorium       = property(lambda self: self.load()._directionSanatorium)
    healthGroup               = property(lambda self: self.load()._healthGroup)

