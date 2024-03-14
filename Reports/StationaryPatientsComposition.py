# -*- coding: utf-8 -*-
#############################################################################
##
## Copyright (C) 2006-2012 Chuk&Gek and Vista Software. All rights reserved.
## Copyright (C) 2012-2020 SAMSON Group. All rights reserved.
##
#############################################################################
##
## Это программа является свободным программным обеспечением.
## Вы можете использовать, распространять и/или модифицировать её согласно
## условиям GNU GPL версии 3 или любой более поздней версии.
##
#############################################################################

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignature, QDate, QDateTime, QTime


from Reports.ReportBase import CReportBase, createTable
from Reports.Report     import CReport
from Reports.ReportView import CPageFormat
from Reports.Utils      import dateRangeAsStr, getPropertyAPHBP, countMovingDays
from Orgs.Utils         import getOrgStructureFullName
from HospitalBedProfileListDialog import CHospitalBedProfileListDialog
from library.Utils      import forceInt, forceString, forceDateTime

from Ui_StationaryPatientsCompositionSetupDialog import Ui_StationaryPatientsCompositionSetupDialog



class CStationaryPatientsComposition(CReport):
    def __init__(self, parent):
        CReport.__init__(self, parent)
        self.setTitle(u'Состав больных в стационаре, сроки и исходы лечения среди выбывших')
        self.orientation = CPageFormat.Landscape

    def getSetupDialog(self, parent):
        result = CStationaryPatientsCompositionSetup(parent)
        result.setTitle(self.title())
        return result

    def selectData(self, params):
        begDate                = params.get('begDate', QDate())
        endDate                = params.get('endDate', QDate())
        ageFrom = params.get('ageFrom', 0)
        ageTo = params.get('ageTo', 150)
        orgStructureIdList     = params.get('orgStructureIdList', None)
        MKBFilter              = params.get('MKBFilter', False)
        MKBFrom                = params.get('MKBFrom', 'A00.00')
        MKBTo                  = params.get('MKBTo', 'Z99.99')
        groupMKB               = params.get('groupMKB', 0)
        personFilter              = params.get('personFilter', False)
        selectType             = params.get('selectType', 0)
        personId               = params.get('personId', None)
        hospitalBedProfileList = params.get('hospitalBedProfileList', None)
        data = {}
        MKBNames = {}
        db = QtGui.qApp.db
        tableEvent = db.table('Event')
        tableAction = db.table('Action')
        tableDiagnosis = db.table('Diagnosis')
        tablePerson = db.table('Person')
        tableOrgStructure = db.table('OrgStructure')

        medicalDayBegTime = QtGui.qApp.medicalDayBegTime()
        if not medicalDayBegTime:
            medicalDayBegTime = QTime(9,0)
        cond = [tableEvent['execDate'].ge(QDateTime(begDate, medicalDayBegTime)),
                tableEvent['execDate'].le(QDateTime(endDate, medicalDayBegTime.addSecs(-60)))]

        if personFilter:
            if selectType:
                tableFrom = u''' INNER JOIN Person ON Person.id = Event.execPerson_id'''
            else:
                tableFrom = u''' INNER JOIN Person ON Person.id = Action.person_id'''
            if personId:
                if selectType:
                    cond.append(tablePerson['deleted'].eq(0))
                    cond.append(tablePerson['id'].eq(personId))
                else:
                    cond.append(tablePerson['deleted'].eq(0))
                    cond.append(tablePerson['id'].eq(personId))
            if orgStructureIdList:
                if selectType:
                    cond.append(tablePerson['deleted'].eq(0))
                    cond.append(tablePerson['orgStructure_id'].inlist(orgStructureIdList))
                else:
                    cond.append(tablePerson['deleted'].eq(0))
                    cond.append(tablePerson['orgStructure_id'].inlist(orgStructureIdList))
        else:
            tableFrom = u''
        if ageFrom <= ageTo:
            cond.append('Event.execDate >= ADDDATE(Client.birthDate, INTERVAL %d YEAR)'%ageFrom)
            cond.append('Event.execDate < SUBDATE(ADDDATE(Client.birthDate, INTERVAL %d YEAR),1)'%(ageTo+1))
        if MKBFilter:
            cond.append(tableDiagnosis['MKB'].ge(MKBFrom))
            cond.append(tableDiagnosis['MKB'].le(MKBTo))
        orgStructureCond = u'is not NULL'
        if orgStructureIdList:
            #orgStructureCond = u'= \'%s\''%forceString(db.translate(tableOrgStructure, 'id', orgStructure, 'name'))
            orgStructureCond = u'in (%s)'%( ','.join(map(str, orgStructureIdList)) )
        profile = (u' AND ' + getPropertyAPHBP(hospitalBedProfileList, False)) if hospitalBedProfileList else u''
        stmt = u'''
            select
                Event.id as EVNT,
                WorkDays(Event.setDate, Event.execDate, et.weekProfileCode, mat.regionalCode) AS day,
                Diagnosis.MKB as MKB,
                MKB.DiagName as diagName,
                MKB.BlockID as MKBBlockId,
                MKB.BlockName as MKBBlockName,
                MKB.DiagID as MKBDiagID,
                (SELECT MKB2.DiagName
                FROM MKB AS MKB2
                WHERE MKB2.DiagID = LEFT(MKB.DiagID, 3)
                ORDER BY MKB2.DiagID LIMIT 1) AS MKBDiagName,
                MKB.ClassID as MKBClassId,
                MKB.ClassName as MKBClassName,
                (
                    select OrgStructure.id
                        from ActionProperty as AP
                            left join ActionPropertyType AS APT on APT.id = AP.type_id
                            left join ActionProperty_OrgStructure AS APOS on APOS.id = AP.id
                            left join OrgStructure on OrgStructure.id = APOS.value
                        where
                            AP.action_id = Action.id
                            AND AP.deleted = 0
                            and APT.name = 'Отделение'
                             LIMIT 1
                ) as 'orgStructure',
                Event.execDate as 'execDate',
                Event.setDate as 'setDate',
                CASE (
                    select APS.value
                        from ActionProperty as AP
                            left join ActionPropertyType AS APT on APT.id = AP.type_id
                            left join ActionProperty_String AS APS on APS.id = AP.id
                        where
                            AP.action_id = Action.id
                            AND AP.deleted = 0
                            and APT.name = 'Исход госпитализации'
                             LIMIT 1
                )
                WHEN 'Переведен в другой стационар' THEN 'Transfered'
                WHEN 'Умер' THEN 'Dead'
                ELSE 'Leaved'
                END

                    as 'exitStatus',

                CASE rbDResult.name
                    WHEN 'Выздоровление' THEN 'feelFine'
                    WHEN 'Ухудшение' THEN 'youKilledMe'
                    WHEN 'Улучшение' THEN 'muchBetter'
                    ELSE 'whereAmI'
                END
                            as 'result',
                (SELECT OrgStructure_HospitalBed.schedule_id
                    FROM Event as ENT
                        LEFT JOIN Action ON ENT.id = Action.event_id
                        LEFT JOIN ActionProperty AS AP ON AP.action_id = Action.id
                        LEFT JOIN ActionPropertyType AS APT ON APT.id = AP.type_id
                        LEFT JOIN ActionProperty_HospitalBed AS APHB ON APHB.id = AP.id
                        LEFT JOIN OrgStructure_HospitalBed ON OrgStructure_HospitalBed.id = APHB.value
                    WHERE
                        DATE(ENT.execDate)=DATE(Action.endDate)
                        AND AP.deleted = 0
                        AND APT.name = 'койка' 
                        AND ENT.id = Event.id LIMIT 1) AS 'shedule'

            from Event
                left join Diagnostic on Diagnostic.id = getEventDiagnostic(Event.id)
                left join Diagnosis on Diagnosis.id = Diagnostic.diagnosis_id
                left join rbDiagnosisType on rbDiagnosisType.id = Diagnostic.diagnosisType_id
                left join Client on Client.id = Event.client_id
                LEFT JOIN EventType et ON Event.eventType_id = et.id
                LEFT JOIN rbMedicalAidType mat ON et.medicalAidType_id = mat.id
                left join Action on Action.event_id = Event.id
                left join ActionType on ActionType.id = Action.actionType_id
                left join rbDiagnosticResult as rbDResult on rbDResult.id = Diagnostic.result_id
                left join MKB ON MKB.DiagID = Diagnosis.MKB
                %s

            where  ActionType.flatCode = 'leaved' and Action.deleted = 0
                and %s
                %s

            having orgStructure %s
        ''' % (tableFrom, db.joinAnd(cond), profile, orgStructureCond)

        query = db.query(stmt)
        orgStructureNames = {}
        while query.next():
            record = query.record()
            osId = forceInt(record.value('orgStructure'))
            orgStructure = orgStructureNames.get(osId, None) 
            if not orgStructure:
                orgStructure = forceString(db.translate(tableOrgStructure, 'id', osId, 'name'))
                orgStructureNames[osId] = orgStructure
            MKB = forceString(record.value('MKB'))
            kdays = forceInt(record.value('day'))
            diagName = forceString(record.value('diagName'))
            MKBBlockId = forceString(record.value('MKBBlockId'))
            MKBBlockName = forceString(record.value('MKBBlockName'))
            MKBDiagID = forceString(record.value('MKBDiagID'))
            MKBDiagName = forceString(record.value('MKBDiagName'))
            MKBClassId = forceString(record.value('MKBClassId'))
            MKBClassName = forceString(record.value('MKBClassName'))
            fromDate = forceDateTime(record.value('setDate'))
            toDate = forceDateTime(record.value('execDate'))
            exitStatus = forceString(record.value('exitStatus'))
            result = forceString(record.value('result'))
            if groupMKB == 1:
                dCode = MKBDiagID[:3]
                MKBNames[dCode] = MKBDiagName if MKBDiagName else MKBBlockName
            elif groupMKB == 2:
                dCode = MKBBlockId
                MKBNames[dCode] = MKBBlockName
            elif groupMKB == 3:
                dCode = MKBClassId
                MKBNames[dCode] = MKBClassName
            else:
                dCode = MKB
                MKBNames[dCode] = diagName

#            kdays = countMovingDays(fromDate, toDate, QDateTime(begDate), QDateTime(endDate), forceInt(record.value('shedule')))
#            для подсчетка койко-дней по движению
#            additionalCond = u'Event.id = %i'%forceInt(record.value('EVNT'))
#            kdays = getMovingDays(orgStructureIdList,  QDateTime(begDate), QDateTime(endDate), additionalCond = additionalCond, bedsSchedule = forceInt(record.value('shedule')))

            dataByDiag = data.setdefault(orgStructure, {})
            row = dataByDiag.setdefault(dCode, [0]*14)

            if exitStatus == 'Leaved':
                row[0] += 1
                row[1] += kdays
            elif exitStatus == 'Dead':
                row[3] += 1
                row[5] += kdays
            elif exitStatus == 'Transfered':
                row[7] += 1
                row[8] += kdays

            if result == 'feelFine':
                row[10] += 1
            elif result == 'muchBetter':
                row[11] += 1
            elif result == 'youKilledMe':
                row[12] += 1
            else:
                row[13] += 1

        return data, MKBNames


    def dumpParams(self, cursor, params):
        description = []
        begDate = params.get('begDate', QDate())
        endDate = params.get('endDate', QDate())
        ageFrom = params.get('ageFrom', 0)
        ageTo = params.get('ageTo', 150)
        #eventOrder = params.get('eventOrder', 0)
        if begDate and endDate:
            description.append(dateRangeAsStr(u'за период', begDate, endDate))
        if ageFrom <= ageTo:
            if not ageTo:
                description.append(u'возраст: до 1 года')
            else:
                description.append(u'возраст' + u' с '+forceString(ageFrom) + u' по '+forceString(ageTo))
        db = QtGui.qApp.db
        eventTypeId = params.get('eventTypeId', None)
        if eventTypeId:
            description.append(u'тип события %s'%(forceString(db.translate('EventType', 'id', eventTypeId, 'name'))))
        selectType = params.get('selectType', 0)
        description.append(u'выбор: %s'%{0: u'по врачу ответственному за действие',
                                         1: u'по врачу ответственному за событие'}.get(selectType, u'по врачу ответственному за действие'))
        personId = params.get('personId', None)
        if personId:
            description.append(u'врач: %s'%(forceString(QtGui.qApp.db.translate('vrbPersonWithSpeciality', 'id', personId, 'name'))))
        orgStructureId = params.get('orgStructureId', None)
        if orgStructureId:
            description.append(u'подразделение: ' + getOrgStructureFullName(orgStructureId))
        else:
            description.append(u'подразделение: ЛПУ')
        isGroupingOS = params.get('isGroupingOS', False)
        if isGroupingOS:
            description.append(u'с детализацией по операциям')
        selectActionType = params.get('selectActionType', 0)
        description.append(u'отбор по %s'%([u'операциям', u'поступлению', u'движению', u'выписке'][selectActionType]))
        MKBFilter = params.get('MKBFilter', 0)
        MKBFrom = params.get('MKBFrom', '')
        MKBTo = params.get('MKBTo', '')
        if MKBFilter == 1:
            description.append(u'код МКБ с "%s" по "%s"' % (MKBFrom, MKBTo))
        elif MKBFilter == 2:
            description.append(u'код МКБ пуст')
        groupMKB = params.get('groupMKB', 0)
        description.append(u'Группировать диагнозы: %s'%{0: u'не группировать',
                                                         1: u'группировать по рубрикам',
                                                         2: u'группировать по блокам',
                                                         3: u'группировать по классам'}.get(groupMKB, u'не группировать'))
        hospitalBedProfileList = params.get('hospitalBedProfileList', None)
        if hospitalBedProfileList:
            db = QtGui.qApp.db
            table = db.table('rbHospitalBedProfile')
            records = db.getRecordList(table, [table['name']], [table['id'].inlist(hospitalBedProfileList)])
            nameList = []
            for record in records:
                nameList.append(forceString(record.value('name')))
            description.append(u'профиль койки:  %s'%(u','.join(name for name in nameList if name)))
        else:
            description.append(u'профиль койки:  не задано')
        description.append(u'отчёт составлен: '+forceString(QDateTime.currentDateTime()))
        columns = [ ('100%', [], CReportBase.AlignLeft) ]
        table = createTable(cursor, columns, headerRowCount=len(description), border=0, cellPadding=2, cellSpacing=0)
        for i, row in enumerate(description):
            table.setText(i, 0, row)
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertBlock()


    def build(self, params):
        tableColumns = [
            #('22%', [u'Подразделение',  '',  '1'],  CReportBase.AlignLeft),
            ('12%', [u'Диагноз', '',  '1'],     CReportBase.AlignLeft),
            ('18%', [u'Наименование', '',  '2'],     CReportBase.AlignLeft),
            ('5%', [u'Выписано',  u'Всего',  '3'],      CReportBase.AlignRight),
            ('5%', ['', u'Проведено койко-дней', '4'], CReportBase.AlignRight),
            ('5%', ['', u'Средний койко-день', '5'], CReportBase.AlignRight),
            ('5%', [u'Умерло',  u'Всего',  '6'],      CReportBase.AlignRight),
            ('5%', ['', u'Летальность', '7'], CReportBase.AlignRight),
            ('5%', ['', u'Проведено койко-дней', '8'], CReportBase.AlignRight),
            ('5%', ['', u'Средний койко-день', '9'], CReportBase.AlignRight),
            ('5%', [u'Переведено в др. стац.',  u'Всего',  '10'],      CReportBase.AlignRight),
            ('5%', ['', u'Проведено койко-дней', '11'], CReportBase.AlignRight),
            ('5%', ['', u'Средний койко-день', '12'], CReportBase.AlignRight),
            ('5%', [u'Выздоровление', '',  '13'],     CReportBase.AlignRight),
            ('5%', [u'Улучшение', '',  '14'],     CReportBase.AlignRight),
            ('5%', [u'Ухудшение', '',  '15'],     CReportBase.AlignRight),
            ('5%', [u'Прочее', '',  '16'],     CReportBase.AlignRight),
            ]

        doc = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(doc)

        cursor.setCharFormat(CReportBase.ReportTitle)
        cursor.insertText(self.title())
        cursor.insertBlock()
        self.dumpParams(cursor, params)
        cursor.insertBlock()
        table = createTable(cursor, tableColumns)

        table.mergeCells(0, 0, 2, 1)
        table.mergeCells(0, 1, 2, 1)
        table.mergeCells(0, 2, 1, 3)
        table.mergeCells(0, 5, 1, 4)
        table.mergeCells(0, 9, 1, 3)
        table.mergeCells(0, 12, 2, 1)
        table.mergeCells(0, 13, 2, 1)
        table.mergeCells(0, 14, 2, 1)
        table.mergeCells(0, 15, 2, 1)

        fullSum = {}
        data, MKBNames = self.selectData(params)
        i = 0
        totalLine = [0]*14
        for orgStructure in sorted(data.keys()):
            sum = [0]*14
            i = table.addRow()
            table.setText(i, 0, orgStructure, CReportBase.TableTotal, CReportBase.AlignRight)
            table.mergeCells(i, 0, 1, 16)
            for MKB in sorted(data[orgStructure]):
                MKBName = MKBNames[MKB]
                fullSumRow = fullSum.setdefault(MKB, [0]*14)
                row = data[orgStructure][MKB]
                row[2] = round(row[1]*1.0/row[0], 2) if row[0] else 0
                row[6] = round(row[5]*1.0/row[3], 2) if row[3] else 0
                row[9] = round(row[8]*1.0/row[7], 2) if row[7] else 0
                if row[3]:
                    row[4] = row[0]/row[3]
                i = table.addRow()
                for y, num in enumerate(row):
                    table.setText(i, y+2, num)
                    sum[y] += num
                    fullSumRow[y] += num
                    totalLine[y] += num
                table.setText(i, 0, MKB)
                table.setText(i, 1, MKBName)
            i = table.addRow()
            sum[2] = round(sum[1]*1.0/sum[0], 2) if sum[0] else 0
            sum[6] = round(sum[5]*1.0/sum[3], 2) if sum[3] else 0
            sum[9] = round(sum[8]*1.0/sum[7], 2) if sum[7] else 0
            table.setText(i, 0, u'Итого', CReportBase.TableTotal, CReportBase.AlignRight)
            table.mergeCells(i, 0, 1, 2)
            for y, num in enumerate(sum):
                table.setText(i, y+2, num, CReportBase.TableTotal)
        i = table.addRow()
        table.setText(i, 0, u'Итого по стационару', CReportBase.TableTotal, CReportBase.AlignRight)
        table.mergeCells(i, 0, 1, 16)
        for MKB in sorted(fullSum.keys()):
            fullSum[MKB][2] = round(fullSum[MKB][1]*1.0/fullSum[MKB][0], 2) if fullSum[MKB][0] else 0
            fullSum[MKB][6] = round(fullSum[MKB][5]*1.0/fullSum[MKB][3], 2) if fullSum[MKB][3] else 0
            fullSum[MKB][9] = round(fullSum[MKB][8]*1.0/fullSum[MKB][7], 2) if fullSum[MKB][7] else 0
            i = table.addRow()
            MKBName = MKBNames[MKB]
            table.setText(i, 0, MKB, CReportBase.TableTotal)
            table.setText(i, 1, MKBName, CReportBase.TableTotal)
            for y, num in enumerate(fullSum[MKB]):
                table.setText(i, y+2, num, CReportBase.TableTotal)
        i = table.addRow()
        table.setText(i, 0, u'ИТОГО', CReportBase.TableTotal, CReportBase.AlignRight)
        table.mergeCells(i, 0, 1, 2)
        for y, num in enumerate(totalLine):
            table.setText(i, y+2, num, CReportBase.TableTotal)
        return doc



class CStationaryPatientsCompositionSetup(QtGui.QDialog, Ui_StationaryPatientsCompositionSetupDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.cmbOrgStructure.setOrgId(QtGui.qApp.currentOrgId())
        self.cmbOrgStructure.setValue(QtGui.qApp.currentOrgStructureId())
        self.hospitalBedProfileList = []

    def setTitle(self, title):
        self.setWindowTitle(title)

    def setParams(self, params):
        self.edtBegDate.setDate(params.get('begDate', QDate.currentDate()))
        self.edtEndDate.setDate(params.get('endDate', QDate.currentDate()))
        self.edtAgeFrom.setValue(params.get('ageFrom', 0))
        self.edtAgeTo.setValue(params.get('ageTo', 150))
        self.cmbOrgStructure.setValue(params.get('orgStructureId', None))
        self.chkMKBFilter.setChecked(params.get('MKBFilter', 0))
        self.edtMKBFrom.setText(params.get('MKBFrom', 'A0000'))
        self.edtMKBTo.setText(params.get('MKBTo', 'Z9999'))
        self.cmbGroupMKB.setCurrentIndex(params.get('groupMKB', 0))
        self.chkPerson.setChecked(params.get('personFilter', 0))
        self.cmbSelectType.setCurrentIndex(params.get('selectType', 0))
        self.cmbPerson.setValue(params.get('personId', None))
        self.hospitalBedProfileList = params.get('hospitalBedProfileList', [])
        if self.hospitalBedProfileList:
            db = QtGui.qApp.db
            table = db.table('rbHospitalBedProfile')
            records = db.getRecordList(table, [table['name']], [table['id'].inlist(self.hospitalBedProfileList)])
            self.lblHospitalBedProfileList.setText(u', '.join(forceString(record.value('name')) for record in records if forceString(record.value('name'))))
        else:
            self.lblHospitalBedProfileList.setText(u'не задано')


    def params(self):
        result = {}
        result['begDate'] = self.edtBegDate.date()
        result['endDate'] = self.edtEndDate.date()
        result['ageFrom'] = self.edtAgeFrom.value()
        result['ageTo'] = self.edtAgeTo.value()
        result['orgStructureIdList'] = self.getOrgStructureIdList()
        result['orgStructureId'] = self.cmbOrgStructure.value()
        result['groupMKB'] = self.cmbGroupMKB.currentIndex()
        result['MKBFilter'] = True if self.chkMKBFilter.isChecked() else False
        if result['MKBFilter']:
            result['MKBFrom'] = unicode(self.edtMKBFrom.text())
            result['MKBTo'] = unicode(self.edtMKBTo.text())
        result['personFilter'] = True if self.chkPerson.isChecked() else False
        result['selectType'] = self.cmbSelectType.currentIndex()
        result['personId'] = self.cmbPerson.value()
        result['hospitalBedProfileList'] = self.hospitalBedProfileList
        return result


    def getOrgStructureIdList(self):
        treeIndex = self.cmbOrgStructure._model.index(self.cmbOrgStructure.currentIndex(), 0, self.cmbOrgStructure.rootModelIndex())
        treeItem = treeIndex.internalPointer() if treeIndex.isValid() else None
        return treeItem.getItemIdList() if treeItem else []


    @pyqtSignature('')
    def on_btnHospitalBedProfileList_clicked(self):
        self.hospitalBedProfileList = []
        self.lblHospitalBedProfileList.setText(u'не задано')
        dialog = CHospitalBedProfileListDialog(self)
        if dialog.exec_():
            self.hospitalBedProfileList = dialog.values()
            if self.hospitalBedProfileList:
                db = QtGui.qApp.db
                table = db.table('rbHospitalBedProfile')
                records = db.getRecordList(table, [table['name']], [table['id'].inlist(self.hospitalBedProfileList)])
                nameList = []
                for record in records:
                    nameList.append(forceString(record.value('name')))
                self.lblHospitalBedProfileList.setText(u', '.join(name for name in nameList if name))
