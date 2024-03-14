# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2022 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4                  import QtGui
from PyQt4.QtCore           import QDate

from library.MapCode        import createMapCodeToRowIdx
from library.Utils          import forceBool, forceDate, forceInt, forceRef, forceString

from Reports.Report         import normalizeMKB
from Reports.ReportBase     import CReportBase, createTable
from StatReportF12Able_2020 import (CStatReportF12Able_2020,
                                    MainRows,
                                    CompRows,
                                    selectDataClient)
from StatReportF12Adults_2021 import selectData



def getAbleAgesCond(begDate, today='Diagnosis.endDate'):
    cond = 'IF(Client.sex = 1, 60, 55)'
    if begDate:
        if begDate.year() == 2021:
            cond = 'IF(Client.sex = 1, 61, 56)'
        if begDate.year() == 2022 or begDate.year() == 2023:
            cond = 'IF(Client.sex = 1, 62, 57)'
        if begDate.year() >= 2024:
            cond = 'IF(Client.sex = 1, 63, 58)'
    return 'age(Client.birthDate, %s) BETWEEN 18 AND (%s - 1)' % (today, cond)


class CStatReportF12Able_2021(CStatReportF12Able_2020):
    def __init__(self, parent):
        CStatReportF12Able_2020.__init__(self, parent)
        self.setTitle(u'Ф.12. 6.Взрослые трудоспособного возраста.')


    def getSetupDialog(self, parent):
        result = CStatReportF12Able_2020.getSetupDialog(self, parent)
        result.chkRegisteredInPeriod.setChecked(True)
        result.chkOnlyEmptyMKBEx.setVisible(True)
        result.setAllAttachSelectable(True)
        return result


    def build(self, params, reportMainRows=MainRows, reportCompRows=CompRows):
        mapMainRows = createMapCodeToRowIdx( [row[2] for row in reportMainRows] )
        mapCompRows = createMapCodeToRowIdx( [row[2] for row in reportCompRows] )

        registeredInPeriod = params.get('registeredInPeriod', False)
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        eventPurposeId = params.get('eventPurposeId', None)
        eventTypeDDId = params.get('eventTypeDDId', None)
        eventTypeList = params.get('eventTypeList', None)
        orgStructureList = params.get('orgStructureList', None)
        personId = params.get('personId', None)
        sex = params.get('sex', 0)
        ageFrom = params.get('ageFrom', 18)
        ageTo = params.get('ageTo', 150)
        socStatusClassId = params.get('socStatusClassId', None)
        socStatusTypeId = params.get('socStatusTypeId', None)
        isFilterAddressOrgStructure = params.get('isFilterAddressOrgStructure', False)
        addrType = params.get('addressOrgStructureType', 0)
        addressOrgStructureId = params.get('addressOrgStructure', None)
        locality = params.get('locality', 0)
        detailMKB = params.get('detailMKB', False)
        if begDate and endDate:
            params['extraAgesCond'] = getAbleAgesCond(begDate, "DATE('%04d-12-31')"%endDate.year())
        reportLine = None

        rowSize = 8
        rowCompSize = 4
        eventTypeDDSum = 0
        eventIdList = []
        if detailMKB:
            reportMainData = {}  # { MKB: [reportLine] }
            reportCompData = {}  # { MKB: [reportLine] }
        else:
            reportMainData = [ [0]*rowSize for row in xrange(len(reportMainRows)) ]
            reportCompData = [ [0]*rowCompSize for row in xrange(len(reportCompRows)) ]
        query = selectData(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeList, orgStructureList, personId, sex, ageFrom, ageTo, socStatusClassId, socStatusTypeId,  isFilterAddressOrgStructure, addrType, addressOrgStructureId, locality, eventTypeDDId, params)
        while query.next():
            record    = query.record()
            clientId = forceRef(record.value('client_id'))
            MKB       = normalizeMKB(forceString(record.value('MKB')))
            sickCount = forceInt(record.value('sickCount'))
            diseaseCharacter = forceString(record.value('diseaseCharacter'))
            diagnosisType = forceString(record.value('diagnosisType'))
            firstInPeriod = forceBool(record.value('firstInPeriod'))
            observed = forceBool(record.value('observed'))
            closedEvent = forceBool(record.value('closedEvent'))
            getObserved = forceInt(record.value('getObserved'))
            eventId = forceRef(record.value('eventId'))
            getRemovingObserved = forceBool(record.value('getRemovingObserved'))
            getProfilactic      = forceBool(record.value('getProfilactic'))
            isNotPrimary        = forceBool(record.value('isNotPrimary'))
            getAdultsDispans    = forceBool(record.value('getAdultsDispans'))
            if (eventId not in eventIdList) and (diseaseCharacter == 1 or diseaseCharacter == 2):
                eventTypeDDSum += 1
                eventIdList.append(eventId)
            cols = [0]
            if getObserved:
                cols.append(1)
            if getRemovingObserved:
                cols.append(6)
            if observed:
                cols.append(7)
            if diseaseCharacter == u'1': # острое
                cols.append(2)
                if getObserved:
                    cols.append(3)
                if getProfilactic and not getAdultsDispans:
                    cols.append(4)
                if getAdultsDispans:
                    cols.append(5)
            elif firstInPeriod:
                cols.append(2)
                if getObserved:
                    cols.append(3)
                if getProfilactic and not getAdultsDispans:
                    cols.append(4)
                if getAdultsDispans:
                    cols.append(5)

            if detailMKB:
                reportLine = reportMainData.setdefault(MKB, [0]*rowSize)
                for col in cols:
                    reportLine[col] += sickCount
            else:
                for row in mapMainRows.get(MKB, []):
                    reportLine = reportMainData[row]
                    for col in cols:
                        reportLine[col] += sickCount

            if diagnosisType == u'98':
                if detailMKB:
                    reportLine = reportCompData.setdefault(MKB, [0]*rowCompSize)
                    reportLine[0] += sickCount
                    if getProfilactic and isNotPrimary:
                        reportLine[1] += sickCount
                    if closedEvent:
                        reportLine[2] += sickCount
                else:
                    for row in mapCompRows.get(MKB, []):
                        reportLine = reportCompData[row]
                        reportLine[0] += sickCount
                        if getProfilactic and isNotPrimary:
                            reportLine[1] += sickCount
                        if closedEvent:
                            reportLine[2] += sickCount
        registeredAll = 0
        registeredFirst = 0
        consistsByEnd = 0
        thyroidosUnhangAll = 0
        thyroidosUnhangRecovery = 0
        thyroidosUnhangDeath = 0
        clientIdList = []
        clientIdForThyroidosList = []
        queryClient = selectDataClient(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeList, orgStructureList, personId, sex, ageFrom, ageTo, socStatusClassId, socStatusTypeId,  isFilterAddressOrgStructure, addrType, addressOrgStructureId, locality, params)
        while queryClient.next():
            record    = queryClient.record()
            clientId = forceRef(record.value('client_id'))
            diseaseCharacter = forceString(record.value('diseaseCharacter'))
            firstInPeriod = forceBool(record.value('firstInPeriod'))
            observed = forceBool(record.value('observed'))

            if clientId and clientId not in clientIdList:
                clientIdList.append(clientId)
                registeredAll += 1
                if observed:
                    consistsByEnd += 1
                if firstInPeriod:
                   registeredFirst += 1
        queryThyroidos = selectDataClient(registeredInPeriod, begDate, endDate, eventPurposeId, eventTypeList, orgStructureList, personId, sex, ageFrom, ageTo, socStatusClassId, socStatusTypeId,  isFilterAddressOrgStructure, addrType, addressOrgStructureId, locality, params, True)
        while queryThyroidos.next():
            record    = queryThyroidos.record()
            clientId = forceRef(record.value('client_id'))
            if clientId and clientId not in clientIdForThyroidosList:
                clientIdForThyroidosList.append(clientId)
                thyroidosUnhangAll += 1
                deathDate = forceDate(record.value('begDateDeath'))
                if deathDate and (begDate <= deathDate and deathDate <= endDate):
                    thyroidosUnhangDeath += 1
        # now text
        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        if params.get('isFilterAddress', False):
            self.dumpParamsAdress(cursor, params)
        self.dumpParamsMultiSelect(cursor, params)
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        cursor.insertText(u'(4004)')
        cursor.insertBlock()

        tableColumns = [
            ('15%',  [u'Наименование классов и отдельных болезней',       u'',                                                                     u'',                                                                    u'1'], CReportBase.AlignLeft),
            ('5%',   [u'№ строки',                                        u'',                                                                     u'',                                                                    u'2'], CReportBase.AlignLeft),
            ('10%', [u'Код по МКБ-10 пересмотра',                         u'',                                                                     u'',                                                                    u'3'], CReportBase.AlignLeft),
            ('10%', [u'Зарегистрировано пациентов с данным заболеванием', u'Всего',                                                                u'',                                                                    u'4'], CReportBase.AlignRight),
            ('10%', [u'',                                                 u'из них(из гр. 4):',                                                    u'взято под диспансерное наблюдение',                                   u'5'], CReportBase.AlignRight),
            ('10%', [u'',                                                 u'',                                                                     u'с впервые в жизни установленным диагнозом',                           u'6'], CReportBase.AlignRight),
            ('10%', [u'',                                                 u'из заболеваний с впервые в жизни установленным диагнозом (из гр. 6):', u'взято под диспансерное наблюдение',                                   u'7'], CReportBase.AlignRight),
            ('10%', [u'',                                                 u'',                                                                     u'выявлено при профосмотре',                                            u'8'], CReportBase.AlignRight),
            ('10%', [u'',                                                 u'',                                                                     u'выявлено при диспансеризации определенных групп взрослого населения', u'9'], CReportBase.AlignRight),
            ('10%', [u'Снято с диспансерного наблюдения',                 u'',                                                                     u'',                                                                    u'10'], CReportBase.AlignRight),
            ('10%', [u'Состоит на д.н. на конец периода',                 u'',                                                                     u'',                                                                    u'11'], CReportBase.AlignRight)
            ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 3, 1) # Наименование
        table.mergeCells(0, 1, 3, 1) # № стр.
        table.mergeCells(0, 2, 3, 1) # Код МКБ
        table.mergeCells(0, 3, 1, 6) # Всего
        table.mergeCells(1, 3, 2, 1)
        table.mergeCells(1, 4, 1, 2)
        table.mergeCells(1, 6, 1, 3)
        table.mergeCells(0, 9, 3, 1)
        table.mergeCells(0, 10, 3, 1)

        if detailMKB:
            for row, MKB in enumerate(sorted(reportMainData.keys())):
                reportLine = reportMainData[MKB]
                reportLine[7] = reportLine[1] - reportLine[6]
                if not MKB:
                    MKBDescr, MKB = u'', u'Не указано'
                else:
                    MKBDescr = forceString(QtGui.qApp.db.translate('MKB', 'DiagID', MKB, 'DiagName'))
                if MKB.endswith('.0') and not MKBDescr:
                    MKBDescr = forceString(QtGui.qApp.db.translate('MKB', 'DiagID', MKB[:-2], 'DiagName'))
                i = table.addRow()
                table.setText(i, 0, MKBDescr)
                table.setText(i, 1, row+1)
                table.setText(i, 2, MKB)
                for col in xrange(rowSize):
                    table.setText(i, 3+col, reportLine[col])
        else:
            for row, rowDescr in enumerate(reportMainRows):
                reportLine = reportMainData[row]
                reportLine[7] = reportLine[1] - reportLine[6]
                i = table.addRow()
                table.setText(i, 0, rowDescr[0])
                table.setText(i, 1, rowDescr[1])
                table.setText(i, 2, rowDescr[2] + (u' (часть)' if row == 59 else ''))
                for col in xrange(rowSize):
                    table.setText(i, 3+col, reportLine[col])
        thyroidosUnhangRecovery = thyroidosUnhangAll - thyroidosUnhangDeath
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertText(u'''(4004) Число физических лиц зарегистрированных пациентов – всего %d , из них с диагнозом , установленным впервые в жизни %d , состоит под диспансерным наблюдением на конец отчетного года (из гр. 7, стр. 1.0) %d .'''%(registeredAll, registeredFirst, consistsByEnd))
        cursor.insertBlock()
        cursor.insertText(u'''(4005) Из числа состоящих под диспансерным наблюдением пациентов с заболеваниями щитовидной железы (из стр. 5.1) снято с диспансерного наблюдения: всего %d, из них в связи с выздоровлением %d, со смертью %d. '''%(thyroidosUnhangAll, thyroidosUnhangRecovery, thyroidosUnhangDeath))
        cursor.insertBlock()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertBlock()
        cursor.insertText(u'Взрослые трудоспособного возраста (женщины с 18 до 54 лет включительно и мужчины с с 18 до 59 лет включительно).')
        cursor.insertBlock()
        cursor.insertText(u'ФАКТОРЫ, ВЛИЯЮЩИЕ НА СОСТОЯНИЕ ЗДОРОВЬЯ НАСЕЛЕНИЯ')
        cursor.insertBlock()
        cursor.insertText(u'И ОБРАЩЕНИЯ В МЕДИЦИНСКИЕ ОРГАНИЗАЦИИ (С ПРОФИЛАКТИЧЕСКОЙ ЦЕЛЬЮ)')
        cursor.insertBlock()
        cursor.insertText(u'(4006)')
        cursor.insertBlock()
        cursor.insertBlock()

        tableColumns = [
            ('30%', [u'Наименование', u'', u'1'], CReportBase.AlignLeft),
            ('10%', [u'№ строки', u'', u'2'], CReportBase.AlignLeft),
            ('15%', [u'Код МКБ-10', u'', u'3'], CReportBase.AlignLeft),
            ('15%', [u'Обращения', u'всего', u'4'], CReportBase.AlignRight),
            ('15%', [u'', u'из них: повторные', u'5'], CReportBase.AlignRight),
            ('15%', [u'', u'законченные случаи', u'6'], CReportBase.AlignRight),
            ]

        table = createTable(cursor, tableColumns)
        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 2, 1)
        table.mergeCells(0, 3, 1, 3)

        if detailMKB:
            for row, MKB in enumerate(sorted(reportCompData.keys())):
                reportLine = reportCompData[MKB]
                if not MKB:
                    MKBDescr, MKB = u'', u'Не указано'
                else:
                    MKBDescr = forceString(QtGui.qApp.db.translate('MKB', 'DiagID', MKB, 'DiagName'))
                if MKB.endswith('.0') and not MKBDescr:
                    MKBDescr = forceString(QtGui.qApp.db.translate('MKB', 'DiagID', MKB[:-2], 'DiagName'))
                i = table.addRow()
                table.setText(i, 0, MKBDescr)
                table.setText(i, 1, row+1)
                table.setText(i, 2, MKB)
                table.setText(i, 3, reportLine[0])
                table.setText(i, 4, reportLine[1])
                table.setText(i, 5, reportLine[2])
        else:
            for row, rowDescr in enumerate(reportCompRows):
                reportLine = reportCompData[row]
                i = table.addRow()
                table.setText(i, 0, rowDescr[0])
                table.setText(i, 1, rowDescr[1])
                table.setText(i, 2, rowDescr[2])
                table.setText(i, 3, reportLine[0])
                table.setText(i, 4, reportLine[1])
                table.setText(i, 5, reportLine[2])
        return doc
